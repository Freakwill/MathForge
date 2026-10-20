# Installation and Verification

The qualified target is **Windows x64 / CPython 3.13.9**. Use a fresh virtual environment; no private workspace, old environment, Mathlib installation, SSH profile or application login is required for CORE. Runtime and build locks contain platform-specific artifact SHA-256 values. Dependency artifacts are not bundled.

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install --require-hashes -r requirements-build.lock
.venv\Scripts\python -m pip install --require-hashes -r requirements.lock
.venv\Scripts\python -m pip install --no-deps --no-build-isolation .
.venv\Scripts\python -m pip check
.venv\Scripts\python scripts/mathforge.py validate
.venv\Scripts\python -m mathforge demo --output reports/local/demo001
.venv\Scripts\python -m unittest discover -s tests -v
```

Choose a new output directory. The demo initializes one synthetic card, completes two audit jobs (`validate` and `export`), and reports `research_results=0`. To create another synthetic workspace use `python -m mathforge init --output reports/local/work001`; select it using `--root`. Existing workspaces, exports and receipts are not overwritten.

## Optional explicit Lean interface

Lean is an operator-installed and reviewed optional tool. The adapter supports **Lean 4.24.0**, Init-only targets and Windows resource bounds. It does not download or bundle Lean/Mathlib. The CORE CLI has no automatic proof-generation or Lean-research command; this interface is an explicit Python API.

```python
from pathlib import Path
from mathforge.workspace import initialize
from mathforge.lean import pin_toolchain, check

root = initialize(Path('reports/local/lean-demo001'))
# Resolve an operator-selected executable, outside any untrusted task proposal.
executable = Path('lean.exe').resolve()
policy = pin_toolchain(executable)
# Review this version/hash/template policy before supplying it to check().
task = {'natural_language': 'Synthetic interface smoke only: True.',
        'imports': ['Init'],
        'targets': [{'name': 'Smoke', 'type': 'True',
                     'proof': {'kind': 'exact', 'term': 'True.intro'}}]}
receipt = check(task, root/'reports/local/check001', workspace=root,
                lean=executable, reviewed_policy=policy, timeout=90)
print(receipt['status'])
```

`SCOPED_KERNEL_CHECKED` applies only to the exact encoded task. Natural-language translation, novelty and workflow proof acceptance are not established. `pin_toolchain` records hashes; it cannot certify provenance or perform the administrator's review.

The compiler and inspector share a bounded wall-time budget and a Windows Job memory cap. Unsupported resource adapters, missing tools, changed hashes, denied imports, invalid certificates, type errors and timeouts remain HOLD. This is not a general sandbox for arbitrary Lean source, or an independent security certification of the compiler, standard library or operating system.

To opt into the real synthetic integration test, set an operator-reviewed local executable path:

```powershell
$env:MATHFORGE_TEST_LEAN = (Resolve-Path .\operator-selected-lean\bin\lean.exe).Path
.venv\Scripts\python -m unittest discover -s tests -v
```

Replace the illustrative executable location with your reviewed installation. Without that environment variable, the integration test explicitly skips; it does not fabricate a Lean success. All 29 tests passed locally with this integration enabled. Windows GitHub Actions passed the import checks and runs 29 cases with that one optional test skipped by default. CI verifies synthetic infrastructure, not private research results.

Other operating systems/Python versions and cross-platform dependency locks have not been qualified. See the [capability matrix](architecture/CORE_VS_INTERNAL.md), [scientific lifecycle](architecture/RESEARCH_LIFECYCLE.md), and [license review notice](legal/LICENSE_REVIEW_NOTICE.txt).
