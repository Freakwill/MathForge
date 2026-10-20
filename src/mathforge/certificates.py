"""Adapted pure certificate DSL and trusted inspector; not an execution sandbox."""
import hashlib,json,re
from pathlib import Path

FOUNDATIONS={'propext','Classical.choice','Quot.sound'}


IDENT=re.compile(r'[A-Za-z_][A-Za-z_0-9]*(?:\.[A-Za-z_][A-Za-z_0-9]*)*\Z')


TOKEN=re.compile(r'\s+|[A-Za-z_][A-Za-z_0-9]*(?:\.[A-Za-z_][A-Za-z_0-9]*)*|\d+|[()\[\]{},:∀∃→↔∧∨¬≤≥≠=<>+*/^|.!_−-]|[ℝℤℚℕ]|⟨|⟩')


RESERVED={'by','run_tac','run_elab','by_elab','run_cmd','run_meta','eval_expr','do','unsafe','sorry','sorryAx','admit','axiom','native_decide','initialize','builtin_initialize','elab','elab_rules','macro','macro_rules','syntax','attribute','set_option','import','end','namespace','where','partial','opaque','def','theorem','example','instance','abbrev','class','structure','inductive','variable','open','export','noncomputable','mutual','section','infix','infixl','infixr','notation','local','scoped'}


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def dump(p,v):
    with Path(p).open('x',encoding='utf8') as f:json.dump(v,f,ensure_ascii=False,indent=2)


def pure_term(value):
    if not isinstance(value,str) or not value.strip() or len(value)>50000:raise ValueError('empty/oversized term')
    pos=0
    for m in TOKEN.finditer(value):
        if m.start()!=pos:raise ValueError('unsupported term syntax')
        token=m.group();pos=m.end()
        if token in RESERVED:raise ValueError('executable or untrusted term syntax')
    if pos!=len(value) or '/-' in value or '--' in value:raise ValueError('unsupported term syntax')
    return ' '.join(value.split())


def name(value):
    if not isinstance(value,str) or not IDENT.fullmatch(value) or value.startswith('_Gate'):raise ValueError('invalid declaration name')
    return value


def proof(d,depth=0):
    if depth>12 or not isinstance(d,dict):raise ValueError('invalid proof certificate')
    k=d.get('kind')
    if k=='rfl' and set(d)=={'kind'}:return 'by rfl'
    if k=='decide' and set(d)=={'kind'}:return 'by decide +kernel'
    if k=='exact' and set(d)=={'kind','term'}:
        term=pure_term(d['term'])
        # Exact proposals are applications/lambdas of pure constants, never term elaborators.
        if not re.fullmatch(r'[A-Za-z_0-9.()\s=>]+',term) or any(x in term.split() for x in ['abbrev','class','inductive','structure','variable','open','export','noncomputable','run_cmd','run_meta','by_elab']):raise ValueError('exact term outside pure application language')
        return 'by exact '+' '.join(term.split())
    if k=='exists_decide' and set(d)=={'kind','witness'}:
        w=d['witness']
        if not isinstance(w,list) or len(w)>160 or not all(type(i)is int and 0<=i<=10000 for i in w):raise ValueError('invalid finite witness')
        return 'by exact ⟨['+','.join(map(str,w))+'], by decide +kernel⟩'
    if k=='steps' and set(d)=={'kind','steps'}:
        if not isinstance(d['steps'],list) or not 1<=len(d['steps'])<=32:raise ValueError('invalid steps')
        lines=[]
        for s in d['steps']:
            if not isinstance(s,dict) or len(s)!=1:raise ValueError('invalid step')
            op,arg=next(iter(s.items()))
            if op=='intro' and isinstance(arg,list) and 1<=len(arg)<=20:lines.append('intro '+' '.join(name(x) for x in arg))
            elif op=='have' and isinstance(arg,dict) and set(arg)=={'name','type','proof'}:lines.append('have '+name(arg['name'])+' : '+pure_term(arg['type'])+' := '+proof(arg['proof'],depth+1))
            elif op in {'ring','rfl','field_simp'} and arg is True:lines.append(op)
            elif op=='field_simp' and isinstance(arg,list) and len(arg)<=16:lines.append('field_simp ['+', '.join(name(x) for x in arg)+']')
            elif op=='exact':lines.append(proof({'kind':'exact','term':arg},depth+1).removeprefix('by '))
            else:raise ValueError('step outside certificate language')
        return 'by\n  '+'\n  '.join(lines)
    raise ValueError('unsupported proof certificate')


def _inspector(targets,folder,module):
    expected=[];checks=[]
    for i,t in enumerate(targets):
        n=name(t['name']);typ=pure_term(t['type']);expected.append(f'def _GateExpected{i} : Prop := {typ}')
        checks.append(f'''let target{i} ← getConstInfo `{n}
  let .thmInfo theorem{i} := target{i} | throwError "target is not a theorem: {n}"
  let .defnInfo expected{i} ← getConstInfo `_GateExpected{i} | throwError "missing expected type"
  let env{i} ← getEnv
  unless (env{i}.getModuleIdxFor? `{n}).map ModuleIdx.toNat == some candidateIdx do
    throwError "target was not declared in the candidate module"
  match env{i}.addDeclCore 10000000 (.thmDecl {{ theorem{i} with name := `_GateRechecked{i}, type := expected{i}.value }}) none with
  | .error _ => throwError "kernel rejected expected statement"
  | .ok _ => pure ()
  let axioms{i} ← collectAxioms `{n}
  let expectedAxioms{i} ← collectAxioms `_GateExpected{i}
  for ax in axioms{i} ++ expectedAxioms{i} do
    unless ax == `propext || ax == `Classical.choice || ax == `Quot.sound do
      throwError "unapproved axiom: {{ax}}"
  rows := rows.push <| Json.mkObj [("name", toJson "{n}"), ("kernel_rechecked", toJson true), ("axioms", toJson (axioms{i}.map Name.toString)), ("expected_axioms", toJson (expectedAxioms{i}.map Name.toString)), ("actual_type_expr", toJson (reprStr theorem{i}.type)), ("expected_type_expr", toJson (reprStr expected{i}.value))]''')
    template=(Path(__file__).with_name('assets')/'Inspector.lean.in').read_text(encoding='utf8')
    return template.replace('@@MODULE@@',module).replace('@@EXPECTED@@','\n'.join(expected)).replace('@@CHECKS@@','\n  '.join(checks)).replace('@@OUTPUT@@',json.dumps(str(folder/'inspection.json')))

