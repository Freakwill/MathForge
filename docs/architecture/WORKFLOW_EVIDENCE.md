# Workflow Evidence and Implementation Limits

Inspection date: **2026-10-20**. Public source baseline: import commit `256a939aa0a3f4a3e0bcbc58387ff6b413a644d9`; the integrated import also preserves the concurrently added branded README and all initialization history. The private workspace was read-only. Its validator passed; historical negative/replay records and module authorization contracts were consulted. No old experiment, proof search or acquisition was replayed.

| Label | Meaning |
| --- | --- |
| CORE IMPLEMENTED | Present in the imported reusable CORE; only the stated scope is supported. |
| INTERNAL | Found in private code or retained research records; absent from this distribution. Some steps require human or agent review. |
| EXPERIMENTAL | A partial or optional implementation exists, with incomplete end-to-end qualification. |
| PLANNED | A design, contract or external future step; no implemented automatic capability is asserted. |

Implementation labels are independent of scientific outcomes. A gate PASS is scoped permission or evidence, not proof of originality or publication. INTERNAL does not mean currently running or universally automated. Solid arrows describe observed component handoffs or reviewed workflow order; dashed arrows denote optional or future handoffs, never a promise of automatic execution.

## Reference convention

Bare module names such as `engine.py`, `queue.py` and `certificates.py` refer to [`src/mathforge/`](../../src/mathforge/). Public paths resolve in this repository. **PRIVATE** paths identify inspected files in the separate internal workspace; they are not bundled here and are intentionally not broken hyperlinks. Directory/record-class references establish artifact availability, not an API. Private statements, paper content, scientific outcomes, machine paths, credentials, queue data and evidence payloads are omitted. A private local inspection index retains the exact inspected source hashes without uploading those sources or their contents.

Full-workflow node IDs below also anchor the corresponding aggregated README, system and lifecycle nodes.

| Node | Status | Process | Actual implementation or evidence | Scope and limitation |
| --- | --- | --- | --- | --- |
| F01 | CORE IMPLEMENTED | Initialize environment and synthetic workspace | `pyproject.toml`; `src/mathforge/workspace.py:initialize`; `cli.py:main` | Pinned Windows Python dependencies; fresh synthetic workspace. No toolchain or model auto-install. |
| F02 | EXPERIMENTAL | Configure optional proof model and credentials externally | PRIVATE: `scripts/lean_codex_provider.py:CodexProvider` | Optional existing CLI login; tools disabled, proof DSL only. No general model router or credential distribution. |
| F03 | CORE IMPLEMENTED | Represent field, precise problem and source inputs | `schemas/problem.schema.json`; `schemas/field.schema.json`; `engine.py:load_repository` | Validates curated records and taxonomy. Shipped data are synthetic; no universal natural-language problem importer. |
| F04 | INTERNAL | Acquire and retain primary literature | PRIVATE: `scripts/local_research.py:discover`; `scripts/openai_math.py:parse,ingest` | Bounded feed/HTML acquisition and retained-source parsing. Acquisition failure is infrastructure evidence. |
| F05 | EXPERIMENTAL | Extract untrusted statement leads | PRIVATE: `scripts/extract_counterexample_leads.py:StatementParser,extract` | Numbered HTML statements and math alt text; extraction may lose semantics and never authorizes execution. |
| F06 | INTERNAL | Review hypotheses and curate source-bound candidates | PRIVATE: `scripts/phase2a.py:validate`; `research/phase2a/` | Source-first normalization and full-text review are recorded and checked; mathematical judgments are review inputs. |
| F07 | CORE IMPLEMENTED | Check identity, aliases and do-not-replay history | `src/mathforge/engine.py:normalize,load_repository,replay_blocks` | Structural IDs, aliases, exact scope and replay records; no general semantic theorem-equivalence solver. |
| F08 | INTERNAL | Apply literature and feasibility funnel | PRIVATE: `scripts/phase2a.py:FUNNEL,validate` | Normalization, open status, terminology, stronger theorem, triviality, known computation, replay, tractability. Stops after first failed or unrun gate. |
| F09 | INTERNAL | Curate priority and choose cheapest reviewed oracle | PRIVATE: `scripts/phase2a.py:validate`; `scripts/local_research.py:claim` | Recorded research-value/tractability review; runtime chooses admitted cells in FIFO order. No learned research-priority optimizer. |
| F10 | PLANNED | Generate general new conjectures autonomously | PRIVATE: `agents/conjecturer/CONTRACT.md`; `ROADMAP.md` | Role and schemas are contracts; no general autonomous conjecture engine was established. |
| F11 | INTERNAL | Admit a source-bound finite task and budget | PRIVATE: `scripts/local_research.py:admit`; `scripts/counterexamples.py:admit` | Requires audited supported target, source hash/locator, semantic key and bounded task parameters. Novelty stays UNKNOWN. |
| F12 | INTERNAL | Claim and schedule admitted local work | PRIVATE: `scripts/local_research.py:claim,daemon`; `scripts/round002_service.py` | SQLite transaction, exclusive controller, Windows process identity and resource checks. Separate authorization from the foundational Phase 0 CLI. |
| F13 | INTERNAL | Run bounded mathematical computation | PRIVATE: `scripts/round002_worker.py:main`; `research/counterexamples/round002_graphs.py` | Supported finite generators/oracles, seeds, domain checks, samples and time limits; no arbitrary general mathematics engine. |
| F14 | INTERNAL | Search for and preserve possible counterexamples | PRIVATE: `scripts/round002_worker.py:main`; `scripts/counterexamples.py:cycle` | Retains a candidate screen before independent checking. No witness in sampled inputs is not a proof or UNSAT. |
| F15 | EXPERIMENTAL | Propose restricted proof certificates | PRIVATE: `scripts/lean_codex_provider.py:CodexProvider.propose`; `scripts/lean_trust_gate.py:prove` | Optional provider proposes DSL certificates for fixed targets; cannot decide correctness or change the target. |
| F16 | EXPERIMENTAL | Use diagnostics for a bounded proof repair loop | PRIVATE: `scripts/lean_trust_gate.py:prove` | Immutable requests/proposals/history, at most five attempts and bounded total time. Provider/tool failure stays HOLD, not mathematical falsification. |
| F17 | INTERNAL | Independently recompute supported witnesses | PRIVATE: `scripts/round002_worker.py:main`; `research/counterexamples/round002_graphs.py:independent_check` | Second algorithm or exact arithmetic where implemented; no universal independent scientific referee. |
| F18 | CORE IMPLEMENTED | Check an explicit Init-only Lean certificate | `src/mathforge/lean.py:pin_toolchain,check`; `certificates.py:_inspector`; `assets/Inspector.lean.in` | Reviewed binary/template hashes, fixed target types, declaration and axiom inspection. Only SCOPED_KERNEL_CHECKED; workflow proof acceptance remains false. |
| F19 | INTERNAL | Check reviewed internal Lean or Mathlib targets | PRIVATE: `scripts/lean_trust_gate.py:verify_task`; `formal/trust_gate/Inspector.lean.in` | Reviewed sources/contexts/imports, lock hashes and exact type inspection. VERIFIED applies to encoded targets, not whole-paper semantics or originality. |
| F20 | INTERNAL | Review source semantics, scope and proof coverage | PRIVATE: `scripts/formalize_counterexample.py:formalize`; `reports/PAPER_B_FORMAL_COVERAGE.md`; `research/queueing/` | Retained source comparisons, analytic reviews and coverage records. A written report is not external peer-review certification. |
| F21 | INTERNAL | Review novelty against closest primary work | PRIVATE: `scripts/phase2a.py:validate`; `MathForge_Manuscripts/` novelty-status records | Recorded literature/hypothesis comparison. Novelty UNKNOWN remains HOLD for originality claims; tool acceptance cannot clear it. |
| F22 | INTERNAL | Reconcile scientific review and authorization | PRIVATE: `SCIENTIFIC_CONTRACT.md`; `research/counterexamples/AGENTS.md`; versioned final-gate records | A documented review convention across components, not a single implemented universal ScientificGate API. |
| F23 | INTERNAL | PASS only the explicitly reviewed scope | PRIVATE: `scripts/phase2a.py:validate`; versioned gate records | May mean audit survival or an internal analytic review; never silently converts to whole-paper PROVED, novelty or acceptance. |
| F24 | INTERNAL | HOLD pending evidence, review or budget | PRIVATE: `scripts/local_research.py:finish,recover`; `scripts/lean_trust_gate.py:verify_task` | Retain uncertainty, resource failures and incomplete checks. Re-entry requires explicit review or new evidence. |
| F25 | INTERNAL | KILL or abandon a rejected route and preserve why | PRIVATE: `scripts/phase2a.py:validate`; `negative_knowledge/`; CORE `engine.py:check_transition` | Research-route rejection records; CORE can record supported COLLISION_FOUND/BLOCKED/ABANDONED, not a generic KILL command. |
| F26 | CORE IMPLEMENTED | Append evidence, hashes, events and receipts | `src/mathforge/engine.py:append_transition`; `queue.py:event,run_one`; `lean.py:check` | Local append-only logs and scoped receipts; not signed authorship, distributed durability or automatic full-workspace archiving. |
| F27 | INTERNAL | Account CPU, memory, disk and task budgets | PRIVATE: `scripts/local_research.py:daemon,finish`; `scripts/windows_budget.py` | Local worker caps, daily CPU and per-claim limits; telemetry and immutable job/code/result bindings. No global cost optimizer. |
| F28 | INTERNAL | Retain failure or interrupted logical task | PRIVATE: `scripts/local_research.py:recover,finish`; CORE `queue.py:recover_interrupted` | PID/create-time reconciliation and review states; public queue marks INTERRUPTED without automatic replay. |
| F29 | INTERNAL | Review a new bounded strategy before rescheduling | PRIVATE: `scripts/local_research.py:amend`; versioned strategy-review records | Preserves source and statement; constrained method/seed/size changes and lifetime limits. Same settled cell is not blindly rerun. |
| F30 | INTERNAL | Prepare manuscript and reproducibility materials | PRIVATE: `MathForge_Manuscripts/`; `MathForge_Submission_20261018_RUN001/SUBMISSION_DECISIONS.md` | Source/PDF/supplement/manifest and review artifacts exist. Preparation was owner/agent supervised; no automatic publisher is established. |
| F31 | PLANNED | Owner-approved preprint or journal submission | PRIVATE: submission decision records; `PROJECT_CHARTER.md` | External human-controlled step; no upload/submission implementation or completed submission is established by this audit. |
| F32 | PLANNED | External peer review and editorial decision | External process; no repository implementation | Possible future outcome outside system control. Publication is never guaranteed. |
| F33 | INTERNAL | Close workers and release bounded resources | PRIVATE: `scripts/local_research.py:finish,daemon`; `scripts/windows_budget.py:WindowsMemoryJob` | Close job/process/output handles and reconcile runtime state; preserve scientific files and all failed receipts. |
| F34 | EXPERIMENTAL | Optionally transport or reconcile remote work | PRIVATE: `scripts/paratera_counterexamples.py`; `research/counterexamples/backends.py` | Transport/registry/reconciliation code exists. Successful end-to-end remote research and real interrupted Slurm-job recovery are unqualified. |
| F35 | PLANNED | Coordinate a general multi-role autonomous research loop | PRIVATE: `agents/*/CONTRACT.md`; `ROADMAP.md`; `RESEARCH_STATE.md` | Named roles and full state edges are design contracts, not evidence of ten running agents or a complete autonomous scientist. |
| F36 | INTERNAL | Freeze versioned research recovery and audit packages | PRIVATE: manuscript/submission manifests; `research/queueing/` frozen records | Existing archives/manifests retain originals and anomalies; no unqualified universal automated archive service is claimed. |

## Mapping of aggregated diagrams

| Diagram | Node-to-evidence grouping |
| --- | --- |
| README initialization/input | F01, F03 |
| README literature and identity | F04-F08 |
| README admission/research/proof | F09-F17, F27, F29 |
| README Lean/semantic/novelty/gate | F18-F25 |
| README evidence and writing/submission | F26, F28, F30-F33, F36 |
| System public CLI/data/engine/journal | F01, F03, F07, F26 |
| System public audit queue/receipts | F26, F28; `src/mathforge/queue.py` |
| System public Lean/Windows bounds | F18; `src/mathforge/windows_budget.py` |
| System private acquisition/extraction/funnel | F04-F09, F11 |
| System private scheduler/workers/budgets | F12-F14, F17, F27-F29, F33 |
| System private provider/formal gate/review | F02, F15-F16, F19-F25 |
| System private evidence/manuscript/remote | F26, F30, F34, F36 |
| System future coordination/submission | F31-F32, F35 |
| Lifecycle scientific review graph | F06-F08, F11, F13-F25, F26, F29 |
| Lifecycle operational graph | `queue.py:enqueue,run_one,recover_interrupted,status`; F28-F29 for the explicitly external review step |

## Evidence strength and negative findings

- Public tests establish synthetic infrastructure behavior. Real Lean positive/negative tests establish only the explicit encoded synthetic tasks; they are not private theorem verification.
- Internal source files establish supported mechanisms, not successful execution for every supported target. Historical computation and review records were inspected as evidence categories, without publishing their findings.
- Source extraction is heuristic; current source/hypothesis and originality review remains necessary. The eight-gate literature funnel validates recorded review decisions, not the truth of a newly scraped claim.
- A generic priority optimizer, universal problem importer, self-certifying scientific agent, general ten-role runner, complete automatic manuscript-to-Lean translator, automatic preprint/journal publisher and guaranteed publication were **not established**.
- The optional remote backend is not end-to-end research-qualified. Transport code and a job registry do not establish successful Slurm research execution or tested interrupted-job recovery.
- Scientific PASS/HOLD/KILL is a documented interpretation across records, not one executable global gate. Operational DONE, internal analytic PASS, a finite exact check, a scoped kernel check, originality clearance and editorial acceptance are distinct.
- Frozen records and manifest anomalies are preserved privately. No baseline was rewritten to make a historical check pass, and those records are not part of this GitHub import.

## Diagram format and validation

All diagrams use ordinary quoted-label Mermaid flowcharts and native Markdown fences, without external icon packs, scripts or experimental diagram types. See [GitHub diagram support](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams) and [Mermaid flowchart syntax](https://mermaid.js.org/syntax/flowchart.html). Browser rendering and link/hash validation are recorded separately from mathematical validation. GitHub's deployed Mermaid version may differ from the local renderer; source compatibility and an authenticated GitHub page check must be reported with their actual scope.
