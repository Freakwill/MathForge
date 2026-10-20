# Full Research Workflow

This is the implementation-grounded lifecycle of MathForge, inspected on 2026-10-20. The original CORE candidate is 58 files / 205,023 bytes before integration documents and existing brand assets. It is an audit framework with synthetic data, not the complete private research node. The private workspace was inspected read-only; no research was started for this documentation.

| Label | Meaning |
| --- | --- |
| CORE IMPLEMENTED | Present in the imported reusable CORE; only the stated scope is supported. |
| INTERNAL | Found in private code or retained research records; absent from this distribution. Some steps require human or agent review. |
| EXPERIMENTAL | A partial or optional implementation exists, with incomplete end-to-end qualification. |
| PLANNED | A design, contract or external future step; no implemented automatic capability is asserted. |

Implementation labels are independent of scientific outcomes. A gate PASS is scoped permission or evidence, not proof of originality or publication. INTERNAL does not mean currently running or universally automated. Solid arrows describe observed component handoffs or reviewed workflow order; dashed arrows denote optional or future handoffs, never a promise of automatic execution.

## End-to-end lifecycle

```mermaid
flowchart TB
  subgraph Startup["Initialization and inputs"]
    F01["Initialize environment and synthetic workspace<br/>CORE IMPLEMENTED"]:::core
    F02["Configure optional proof model and credentials externally<br/>EXPERIMENTAL"]:::experimental
    F03["Represent field, precise problem and source inputs<br/>CORE IMPLEMENTED"]:::core
  end
  subgraph Discovery["Source-first discovery and admission"]
    F04["Acquire and retain primary literature<br/>INTERNAL"]:::internal
    F05["Extract untrusted statement leads<br/>EXPERIMENTAL"]:::experimental
    F06["Review hypotheses and curate source-bound candidates<br/>INTERNAL"]:::internal
    F07["Check identity, aliases and do-not-replay history<br/>CORE IMPLEMENTED"]:::core
    F08["Apply literature and feasibility funnel<br/>INTERNAL"]:::internal
    F09["Curate priority and choose cheapest reviewed oracle<br/>INTERNAL"]:::internal
    F10["Generate general new conjectures autonomously<br/>PLANNED"]:::planned
    F11["Admit a source-bound finite task and budget<br/>INTERNAL"]:::internal
  end
  subgraph Research["Separately authorized bounded research"]
    F12["Claim and schedule admitted local work<br/>INTERNAL"]:::internal
    F13["Run bounded mathematical computation<br/>INTERNAL"]:::internal
    F14["Search for and preserve possible counterexamples<br/>INTERNAL"]:::internal
    F15["Propose restricted proof certificates<br/>EXPERIMENTAL"]:::experimental
    F16["Use diagnostics for a bounded proof repair loop<br/>EXPERIMENTAL"]:::experimental
    F17["Independently recompute supported witnesses<br/>INTERNAL"]:::internal
    F34["Optionally transport or reconcile remote work<br/>EXPERIMENTAL"]:::experimental
    F35["Coordinate a general multi-role autonomous research loop<br/>PLANNED"]:::planned
  end
  subgraph Review["Verification and scientific review"]
    F18["Check an explicit Init-only Lean certificate<br/>CORE IMPLEMENTED"]:::core
    F19["Check reviewed internal Lean or Mathlib targets<br/>INTERNAL"]:::internal
    F20["Review source semantics, scope and proof coverage<br/>INTERNAL"]:::internal
    F21["Review novelty against closest primary work<br/>INTERNAL"]:::internal
    F22["Reconcile scientific review and authorization<br/>INTERNAL"]:::internal
    F23["PASS only the explicitly reviewed scope<br/>INTERNAL"]:::internal
    F24["HOLD pending evidence, review or budget<br/>INTERNAL"]:::internal
    F25["KILL or abandon a rejected route and preserve why<br/>INTERNAL"]:::internal
  end
  subgraph Memory["Evidence, budgets and recovery"]
    F26["Append evidence, hashes, events and receipts<br/>CORE IMPLEMENTED"]:::core
    F27["Account CPU, memory, disk and task budgets<br/>INTERNAL"]:::internal
    F28["Retain failure or interrupted logical task<br/>INTERNAL"]:::internal
    F29["Review a new bounded strategy before rescheduling<br/>INTERNAL"]:::internal
    F33["Close workers and release bounded resources<br/>INTERNAL"]:::internal
    F36["Freeze versioned research recovery and audit packages<br/>INTERNAL"]:::internal
  end
  subgraph Dissemination["Human-accountable dissemination"]
    F30["Prepare manuscript and reproducibility materials<br/>INTERNAL"]:::internal
    F31["Owner-approved preprint or journal submission<br/>PLANNED"]:::planned
    F32["External peer review and editorial decision<br/>PLANNED"]:::planned
  end
  F01 --> F03
  F01 -. optional existing model .-> F02
  F03 --> F04 --> F05 --> F06 --> F07 --> F08 --> F09 --> F11
  F03 -. future generation .-> F10
  F10 -. requires full source review .-> F06
  F07 -->|Replay or known collision| F25
  F08 -->|Incomplete source or gate| F24
  F11 -->|Audited supported task only| F12
  F12 --> F13 --> F14 --> F17
  F12 -. optional qualified backend .-> F34
  F34 -. reconciliation and limits .-> F28
  F14 -. separately reviewed proof target .-> F15
  F02 -. proposal only .-> F15
  F15 --> F16 --> F19
  F19 -->|Diagnostic feedback within remaining budget| F16
  F17 --> F20
  F17 -. explicit Init task only .-> F18
  F17 -. supported internal formalization .-> F19
  F18 -->|Scoped receipt only| F20
  F19 -->|Encoded target receipt only| F20
  F20 --> F21 --> F22
  F22 -->|PASS for stated scope| F23
  F22 -->|HOLD| F24
  F22 -->|KILL route| F25
  F24 -->|New source or scope evidence| F06
  F24 -->|Reviewed strategy amendment| F29 --> F11
  F25 --> F26
  F12 --> F27
  F13 --> F26
  F16 --> F26
  F22 --> F26
  F27 -->|Exhaustion or resource pressure| F24
  F12 -->|Failure or interruption| F28
  F28 --> F26
  F28 -->|Review required, no blind replay| F29
  F13 -->|Completion or stop| F33 --> F26 --> F36
  F26 -->|Negative knowledge informs next review| F07
  F23 -->|If owner selects a writing route| F30
  F36 --> F30
  F30 -->|Correctness, novelty and rights review| F24
  F30 -. explicit owner approval .-> F31 -. external review .-> F32
  F32 -. revision request or new literature .-> F06
  F35 -. future integration, disabled in CORE .-> F12
  classDef core fill:#e9f2ff,stroke:#2864a0,color:#12365b
  classDef internal fill:#f0ebfa,stroke:#7656a3,color:#38245a
  classDef experimental fill:#fff0df,stroke:#b56b18,color:#613803
  classDef planned fill:#f1f3f5,stroke:#7c8792,color:#394550,stroke-dasharray:5 4
```

## How to read the feedback loops

1. **Literature loop:** extraction produces untrusted leads. A source/hypothesis gap or a newly found stronger result returns the task to source review. Semantic equivalence and mathematical judgment are not automated by schema validation.
2. **Research loop:** only separately authorized, admitted finite targets enter internal workers. Numerical screens lead to exact or independent checks where supported. No-witness sampling and timeouts remain bounded observations or failures.
3. **Proof loop:** an optional provider proposes restricted certificates for a fixed target. Compiler/kernel diagnostics may guide a bounded repair attempt. The provider has no verification authority; exhausted attempts remain HOLD.
4. **Scientific loop:** formal acceptance, source translation, analytic review and novelty are distinct. A failed encoded proof is not a false mathematical statement. New hypotheses require a newly reviewed record rather than rewriting old evidence.
5. **Recovery loop:** evidence survives crashes and exhausted budgets. Interrupted cells require reconciliation; new strategy cells require review, source/statement preservation and remaining lifetime budget.
6. **Dissemination loop:** manuscript preparation has internal artifact evidence. Preprint upload, journal submission and external review are owner-controlled future steps in this map. Reviewer feedback may reopen source/claim review; acceptance is not guaranteed.

## Execution boundaries

The foundational internal Phase 0 CLI and the distributed CORE both refuse research/proof state promotions. A separate private module has additive, owner-authorized bounded execution; it does not enable the foundational CLI. The public `AuditQueue` only executes `validate` and `export`. There is no hidden flag for enabling private research workers.

The public Lean adapter checks explicit Init-only tasks on the tested Windows toolchain. The internal verifier supports additional reviewed contexts/sources and Mathlib imports. Neither supplies automatic proof-to-natural-language equivalence, novelty clearance or whole-paper acceptance.

PASS / HOLD / KILL are workflow interpretations over component-specific receipts and review records. They are not one shared database enum or a universal gate API. See [actual states and loops](RESEARCH_LIFECYCLE.md), [module/data flow](SYSTEM_ARCHITECTURE.md), [capability matrix](CORE_VS_INTERNAL.md), and [every node's evidence and limits](WORKFLOW_EVIDENCE.md).
