"""Bounded durable audit queue, adapted from the internal executor's transaction model.

Only validation and export are executable. No shell, research workers or background loop.
"""
from datetime import datetime, timezone
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import sqlite3
import uuid
from . import engine

def now(): return datetime.now(timezone.utc).isoformat()

def evidence_path(root, path):
    p = (root / path).resolve()
    if not p.is_relative_to((root / 'reports/local').resolve()):
        raise engine.IntegrityError('output must stay under reports/local')
    return p

class AuditQueue:
    def __init__(self, workspace):
        self.root = Path(workspace).resolve()
        self.path = evidence_path(self.root, 'reports/local/audit-queue.sqlite3')
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.executescript('''CREATE TABLE IF NOT EXISTS jobs(
                sequence INTEGER PRIMARY KEY AUTOINCREMENT, id TEXT UNIQUE, logical_key TEXT UNIQUE,
                action TEXT, payload TEXT, binding TEXT, state TEXT, created TEXT, receipt TEXT);
                CREATE TABLE IF NOT EXISTS events(sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                job TEXT, kind TEXT, at TEXT, previous_hash TEXT, hash TEXT);''')

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.path, timeout=15, isolation_level=None)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA busy_timeout=15000')
        try:
            with db:
                yield db
        finally:
            db.close()

    def binding(self):
        data = engine.load_repository(self.root)
        return engine.digest({'repository':data,
            'definitions':engine.read_json(self.root/'knowledge/definitions/catalog.json'),
            'schemas':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((self.root/'schemas').glob('*.json'))}})

    def event(self, db, job, kind):
        last = db.execute('SELECT hash FROM events ORDER BY sequence DESC LIMIT 1').fetchone()
        prev = last['hash'] if last else None
        at = now()
        h = engine.digest(dict(job=job, kind=kind, at=at, previous_hash=prev))
        db.execute('INSERT INTO events(job,kind,at,previous_hash,hash) VALUES(?,?,?,?,?)', (job,kind,at,prev,h))

    def enqueue(self, action, payload=None):
        self.status()
        payload = {} if payload is None else payload
        if action not in {'validate','export'} or not isinstance(payload, dict):
            raise engine.IntegrityError('research execution and arbitrary commands are disabled')
        if (action == 'validate' and payload) or (action == 'export' and set(payload) != {'output'}):
            raise engine.IntegrityError('unsupported audit job payload')
        if action == 'export': evidence_path(self.root, payload['output'])
        binding = self.binding()
        key = engine.digest([action, payload, binding])
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            old = db.execute('SELECT id FROM jobs WHERE logical_key=?', (key,)).fetchone()
            if old:
                db.commit()
                return old['id']
            if db.execute('SELECT COUNT(*) FROM jobs').fetchone()[0] >= 1000:
                raise engine.IntegrityError('bounded queue capacity reached')
            uid = uuid.uuid4().hex
            db.execute('INSERT INTO jobs(id,logical_key,action,payload,binding,state,created) VALUES(?,?,?,?,?,?,?)',
                       (uid,key,action,engine.canonical(payload),binding,'QUEUED',now()))
            self.event(db, uid, 'QUEUED')
            db.commit()
        return uid

    def run_one(self):
        self.status()
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute("SELECT * FROM jobs WHERE state='QUEUED' ORDER BY sequence LIMIT 1").fetchone()
            if row is None:
                db.commit(); return None
            db.execute("UPDATE jobs SET state='RUNNING' WHERE id=?", (row['id'],))
            self.event(db, row['id'], 'RUNNING'); db.commit()
        state = 'DONE'
        result = dict(job=row['id'], action=row['action'], scientific_result=False, research_execution_enabled=False)
        try:
            if self.binding() != row['binding']: raise engine.IntegrityError('workspace drift since admission')
            data = engine.load_repository(self.root)
            payload = json.loads(row['payload'])
            if row['action'] == 'validate': result['valid'] = True
            elif row['action'] == 'export':
                p = evidence_path(self.root, payload['output']);p.parent.mkdir(parents=True, exist_ok=True)
                with p.open('x', encoding='utf-8', newline='\n') as f:
                    for card in engine.export_cards(data): f.write(engine.canonical(card)+'\n')
                result['output_sha256'] = __import__('hashlib').sha256(p.read_bytes()).hexdigest()
            else: raise engine.IntegrityError('unreviewed queue action')
        except Exception as e:
            state = 'FAILED';result.update(error=type(e).__name__, reason=str(e))
        result['state'] = state
        rel = 'reports/local/queue-receipts/' + row['id'] + '.json'
        receipt = evidence_path(self.root, rel); receipt.parent.mkdir(parents=True, exist_ok=True)
        with receipt.open('x', encoding='utf-8') as f: json.dump(result, f, indent=2)
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            db.execute('UPDATE jobs SET state=?,receipt=? WHERE id=?', (state,rel,row['id']))
            self.event(db, row['id'], state);db.commit()
        return result

    def recover_interrupted(self, job):
        self.status()
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            n = db.execute("UPDATE jobs SET state='INTERRUPTED' WHERE id=? AND state='RUNNING'", (job,)).rowcount
            if n != 1: raise engine.IntegrityError('only RUNNING tasks may be marked interrupted')
            self.event(db, job, 'INTERRUPTED');db.commit()
        return {'job':job, 'state':'INTERRUPTED', 'replayed':False}

    def status(self):
        with self.connect() as db:
            previous = None
            for e in db.execute('SELECT * FROM events ORDER BY sequence'):
                payload = {k:e[k] for k in ['job','kind','at','previous_hash']}
                if e['previous_hash'] != previous or engine.digest(payload) != e['hash']:
                    raise engine.IntegrityError('queue evidence chain corrupted')
                previous = e['hash']
            return [dict(x) for x in db.execute('SELECT id,action,state,receipt FROM jobs ORDER BY sequence')]
