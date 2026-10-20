"""Explicit, scoped Lean interface; no research generation or workflow promotion.

The certificate renderer and trusted inspector derive from the private framework.
Only Init is supported here. The administrator's reviewed binary hash is mandatory.
Windows Job Objects enforce the existing memory bound; other platforms return HOLD.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
import uuid
from .certificates import sha, dump, name, pure_term, proof, _inspector, FOUNDATIONS

def pin_toolchain(lean):
    executable = Path(lean).resolve()
    version = subprocess.run([str(executable), '--version'], capture_output=True, timeout=10, check=True).stdout.decode('utf-8', 'replace').strip()
    if 'version 4.24.0,' not in version: raise ValueError('only the tested Lean 4.24.0 adapter is supported')
    return dict(protocol='mathforge-public-adapter-v1', lean_sha256=sha(executable), version=version,
                inspector_sha256=sha(Path(__file__).with_name('assets')/'Inspector.lean.in'),
                administrator_review_required=True)

def execute(command, cwd, folder, label, timeout, extra_env=None):
    from .windows_budget import WindowsMemoryJob
    with (folder/(label+'.stdout.txt')).open('x', encoding='utf-8') as stdout, (folder/(label+'.stderr.txt')).open('x', encoding='utf-8') as stderr:
        with WindowsMemoryJob(2*1024**3) as job:
            env = {**os.environ, 'OMP_NUM_THREADS':'1', 'LEAN_NUM_THREADS':'1', **(extra_env or {})}
            process = subprocess.Popen(list(map(str, command)), cwd=cwd, stdout=stdout, stderr=stderr,
                                       env=env, creationflags=0x08000000)
            try:
                job.assign(process.pid)
                try: code = process.wait(timeout=timeout)
                except subprocess.TimeoutExpired:
                    process.kill();process.wait();raise TimeoutError('Lean verification timeout')
            finally:
                if process.poll() is None: process.kill();process.wait()
    return {'stage':label, 'exit_code':code}

def check(task, output, *, workspace, lean, reviewed_policy, timeout=30):
    root = Path(workspace).resolve()
    folder = Path(output).resolve()
    if not folder.is_relative_to(root/'reports/local'): raise ValueError('receipts must stay under reports/local')
    folder.mkdir(parents=True, exist_ok=False)
    receipt = dict(status='HOLD', scoped_kernel_checked=False, research_execution_enabled=False,
                   workflow_proof_acceptance=False, novelty='UNKNOWN', natural_language_translation_verified=False,
                   stages=[])
    start = time.monotonic()
    try:
        dump(folder/'TASK.json', task)
        if not .001 <= timeout <= 120: raise ValueError('wall budget out of range')
        if not isinstance(task,dict) or set(task) != {'natural_language','imports','targets'}: raise ValueError('unsupported task fields')
        if not isinstance(task['natural_language'],str) or not task['natural_language'].strip(): raise ValueError('statement required')
        if task['imports'] != ['Init']: raise ValueError('only the reviewed Init interface is enabled')
        targets = task['targets']
        if not isinstance(targets,list) or not 1 <= len(targets) <= 8: raise ValueError('target budget exceeded')
        for t in targets:
            if set(t) != {'name','type','proof'}: raise ValueError('unsupported target fields')
            name(t['name']); pure_term(t['type']); proof(t['proof'])
        if len({t['name'] for t in targets}) != len(targets): raise ValueError('duplicate target')
        if reviewed_policy.get('protocol') != 'mathforge-public-adapter-v1': raise ValueError('reviewed toolchain policy required')
        executable = Path(lean).resolve()
        template = Path(__file__).with_name('assets')/'Inspector.lean.in'
        if sha(executable) != reviewed_policy['lean_sha256'] or sha(template) != reviewed_policy['inspector_sha256']:
            raise ValueError('reviewed toolchain/inspector hash mismatch')
        if 'version 4.24.0,' not in reviewed_policy['version']: raise ValueError('unsupported toolchain version')
        candidate = 'import Init\n' + '\n'.join('theorem '+name(t['name'])+' : '+pure_term(t['type'])+' := '+proof(t['proof']) for t in targets)+'\n'
        module = 'MFProof' + uuid.uuid4().hex
        (folder/'Candidate.lean').write_text(candidate, encoding='utf-8')
        (folder/(module+'.lean')).write_text(candidate, encoding='utf-8')
        (folder/'Inspect.lean').write_text(_inspector(targets, folder, module), encoding='utf-8')
        remaining = lambda: max(.001, timeout-(time.monotonic()-start))
        prefix = [executable, '--threads=1', '-M', '2048']
        stage = execute([*prefix,'--root='+str(folder),'-o',folder/(module+'.olean'),folder/(module+'.lean')], root, folder, 'compile', remaining())
        receipt['stages'].append(stage)
        if stage['exit_code']: raise ValueError('Lean compilation failed')
        stage = execute([*prefix,folder/'Inspect.lean'], root, folder, 'inspect', remaining(), {'LEAN_PATH':str(folder)})
        receipt['stages'].append(stage)
        if stage['exit_code']: raise ValueError('kernel inspection failed')
        data = json.loads((folder/'inspection.json').read_text(encoding='utf-8'))
        if data.get('protocol') != 'mathforge-kernel-v1' or data.get('all_candidate_declarations_audited') is not True:
            raise ValueError('inspector protocol rejected')
        rows = data.get('targets',[])
        if [x['name'] for x in rows] != [x['name'] for x in targets]: raise ValueError('target binding rejected')
        if any(x.get('kernel_rechecked') is not True or not set(x['axioms']) <= FOUNDATIONS or not set(x['expected_axioms']) <= FOUNDATIONS for x in rows):
            raise ValueError('unapproved axiom or missing kernel check')
        receipt.update(status='SCOPED_KERNEL_CHECKED', scoped_kernel_checked=True, inspection=data,
                       lean_sha256=reviewed_policy['lean_sha256'], inspector_sha256=reviewed_policy['inspector_sha256'],
                       candidate_sha256=sha(folder/'Candidate.lean'))
    except Exception as error:
        receipt.update(error=type(error).__name__, reason=str(error))
    receipt['elapsed_seconds'] = time.monotonic()-start
    receipt['artifacts'] = {p.name:sha(p) for p in folder.iterdir() if p.is_file()}
    dump(folder/'RECEIPT.json', receipt)
    return receipt
