"""Local audit commands. No proof search, remote services or persistent scheduler."""
import argparse
import json
from pathlib import Path
import sys
from . import engine
from .workspace import initialize
from .queue import AuditQueue, evidence_path

def summary(data):
    return dict(valid=True, problems=len(data['problems']), sources=len(data['sources']),
                events=len(data['events']), stale_open_status=data['stale_open_status'],
                research_execution_enabled=False, proof_acceptance_enabled=False)

def demo(output):
    root = initialize(output)
    initial = summary(engine.load_repository(root))
    queue = AuditQueue(root)
    queue.enqueue('validate')
    queue.enqueue('export', {'output':'reports/local/demo-export.jsonl'})
    results = [queue.run_one(), queue.run_one()]
    if any(r['state'] != 'DONE' for r in results): raise engine.IntegrityError('synthetic demo failed')
    return dict(synthetic_only=True, initial=initial, jobs=results, queue=queue.status(), research_results=0)

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('validate');sub.add_parser('shortlist')
    p=sub.add_parser('replay-check');p.add_argument('problem_id')
    p=sub.add_parser('transition');p.add_argument('--request',type=Path,required=True)
    p=sub.add_parser('export');p.add_argument('--output',required=True)
    for n in ['init','demo']:
        p=sub.add_parser(n);p.add_argument('--output',type=Path,required=True)
    p=sub.add_parser('queue');p.add_argument('operation',choices=['validate','export','run-one','status','recover']);p.add_argument('--output');p.add_argument('--job')
    args=parser.parse_args(argv)
    root=args.root.resolve()
    try:
        if args.command=='init': result={'created':str(initialize(args.output)), 'synthetic_only':True}
        elif args.command=='demo': result=demo(args.output)
        elif args.command=='queue':
            q=AuditQueue(root)
            if args.operation in {'validate','export'}:
                if args.operation=='export' and not args.output: raise ValueError('export output required')
                result={'job':q.enqueue(args.operation, {'output':args.output} if args.operation=='export' else {})}
            elif args.operation=='run-one': result=q.run_one()
            elif args.operation=='recover':
                if not args.job: raise ValueError('job required')
                result=q.recover_interrupted(args.job)
            else: result=q.status()
        else:
            data=engine.load_repository(root)
            if args.command=='validate': result=summary(data)
            elif args.command=='shortlist': result=data['candidates']
            elif args.command=='replay-check':
                engine.require(args.problem_id in data['problems'],'unknown problem')
                result={'blocked_by':engine.replay_blocks(args.problem_id,data['negatives']), 'research_execution_enabled':False}
            elif args.command=='transition': result=engine.append_transition(root,engine.read_json(args.request))
            elif args.command=='export':
                target=evidence_path(root,args.output);target.parent.mkdir(parents=True,exist_ok=True)
                with target.open('x',encoding='utf-8',newline='\n') as f:
                    for card in engine.export_cards(data): f.write(engine.canonical(card)+'\n')
                result={'exported':target.relative_to(root).as_posix()}
        print(json.dumps(result,ensure_ascii=True));return 0
    except (ValueError,OSError,KeyError,TypeError) as error:
        print(json.dumps({'ok':False,'error':str(error)},ensure_ascii=True),file=sys.stderr);return 2
