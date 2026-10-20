<p align="center">
  <img src="./MathForgeBanner.png" alt="MathForge — Automated Mathematical Research" width="100%" />
</p>

  # MathForge

  **Forge mathematical ideas. Verify the evidence.**

  A research-oriented framework for structured mathematical exploration, verification gates, and reproducible evidence.

  [![Status: pre-release](https://img.shields.io/badge/status-pre--release-555555)](#development-status)
  [![License: Apache-2.0 proposed](https://img.shields.io/badge/license-Apache--2.0%20proposed-D57D43)](#license-and-provenance)
  [![Validation: local](https://img.shields.io/badge/validation-local%20candidate-91603B)](#local-validation)

  **[Overview](#what-is-mathforge) · [Research workflow](#research-workflow) · [Current status](#development-status) · [Roadmap](#roadmap) · [中文简介](#中文简介)**
</div>

---

## What is MathForge?

Mathematical research is not just the production of plausible proofs. It is a cycle of **forming precise claims, exploring possible arguments or counterexamples, checking those claims independently, and preserving enough evidence for others to scrutinize the result**.

MathForge is being developed around that cycle. Its long-term goal is a modular, auditable environment in which human researchers, language models, computational tools, and formal proof assistants can participate in mathematical investigation **without confusing generated hypotheses with established results**.

The distinguishing design priority is **evidence before announcement**: a promising candidate should remain a candidate until the required verification and review have been completed.

> **Scope notice:** This repository is currently a private, pre-release project. As of October 20, 2026, it contains the brand assets, license text, project documentation and the reviewed synthetic CORE source and CI workflow introduced by this private import PR. The full autonomous research system is not being represented as a publicly runnable product.

## Research workflow

The following diagram is the **intended end-to-end research lifecycle**, not a claim that every step is implemented in this repository today. The definitive implementation map will be published alongside the audited Core source.

~~~mermaid
flowchart TD
    A["Research input<br/>Problem · conjecture · paper"] --> B["Candidate intake<br/>Normalize claims and constraints"]
    B --> C["Prior-work and identity checks<br/>Screen duplicates and known results"]
    C --> D["Research exploration<br/>Proof ideas · counterexamples · computation"]
    D --> E["Verification<br/>Independent checks · formal tools where applicable"]
    E --> F{"Scientific gate"}
    F -->|PASS| G["Evidence package<br/>Auditable records and independent review"]
    F -->|HOLD| H["Review queue<br/>Missing evidence or unresolved issues"]
    F -->|KILL| I["Record rejection<br/>Preserve the audit trail"]
    H -->|New evidence / revised approach| D
    G --> J["Human-reviewed research output<br/>Writing · replication · submission"]
~~~

A **PASS** is a gate decision supported by its defined checks, **not** an automatic assertion of novelty, a completed formalization, peer-review acceptance, or publication. A **HOLD** preserves uncertainty; a **KILL** records why a claim or route should stop. Scientific conclusions require domain-specific standards and review.

### Design principles

| Principle | Meaning |
| --- | --- |
| **Traceability** | Keep track of the candidate, inputs, checks, and supporting records behind each decision. |
| **Independent verification** | Separate proposing a claim from determining whether the claim has been substantiated. |
| **Explicit gates** | Make rejection, uncertainty, and evidence requirements visible rather than silently promoting drafts. |
| **Reproducibility** | Prefer inspectable procedures, recorded artifacts, and testable interfaces to opaque success narratives. |
| **Human accountability** | Reserve scientific interpretation, authorship, and publication decisions for responsible researchers. |

## Development status

MathForge has **two different scopes**: an internal research workspace, and a deliberately smaller Core intended for independent use and eventual open-source distribution. They are not equivalent.

| Area | Verified or current state | Boundary |
| --- | --- | --- |
| **Repository contents** | README, brand assets, and Apache-2.0 license text are present. | The executable Core has not been pushed to this repository yet. |
| **Extracted Core candidate** | 58 files, approximately 205 KB, assembled from a reviewed subset of the original engineering workspace. | Local release candidate only; not a publication of the full workspace. |
| **Schemas, scientific contracts, state graph** | Included in the locally checked Core candidate. | Public APIs and compatibility guarantees are not finalized. |
| **Audit queue, replay, resource adapters, Inspector** | Core candidate exercised locally in validation. | These are framework mechanisms, not evidence of autonomous research success. |
| **Lean integration** | A synthetic positive check and invalid-type rejection passed using the real Lean kernel. | This does **not** establish formal proofs of the private research claims. |
| **Autonomous discovery and paper production** | Long-term research direction; additional internal components and experiments are outside this repository. | No claim of independently verified end-to-end discovery performance. |
| **Cloud CI and public installation** | Not yet verified for this GitHub repository. | To be tested after the Core source import. |

The repository will distinguish **implemented**, **experimental**, **internal-only**, and **planned** functionality as the source and documentation expand. A module appearing on a diagram is not, by itself, a verified product capability.

## Local validation

The extracted candidate was audited locally on October 20, 2026. The recorded checks included:

- installation into a fresh isolated Python environment and installation of a built wheel;
- **29 passing unit and adversarial tests**;
- synthetic Lean kernel acceptance and rejection checks;
- state and structure validation, persisted audit queue, export, replay, and package checks;
- ZIP integrity and file hash verification;
- confirmation that the original tracked research files were not rewritten.

Earlier validation attempts exposed a SQLite connection-lifetime issue, a Lean timeout, and a Python import-shadowing issue. Those were corrected and the final candidate was retested. **These results are local validation, not a GitHub Actions pass and not a scientific discovery benchmark.**

## Getting started

The imported candidate supports Windows x64 / CPython 3.13.9. The demo creates synthetic data and executes validation and export only; it produces no research results.

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install --require-hashes -r requirements-build.lock
.venv\Scripts\python -m pip install --require-hashes -r requirements.lock
.venv\Scripts\python -m pip install --no-deps --no-build-isolation .
.venv\Scripts\python scripts/mathforge.py validate
.venv\Scripts\python -m mathforge demo --output reports/local/demo001
.venv\Scripts\python -m unittest discover -s tests -v
```

Use a new output directory. See [installation](docs/INSTALL.md), [candidate architecture](docs/ARCHITECTURE.md), and [the license review notice](docs/legal/LICENSE_REVIEW_NOTICE.txt). GitHub Actions passed on the initial import commit; this integration with the concurrent README update must pass CI again before merge. The optional real Lean integration was exercised locally and is skipped by cloud CI unless an explicit reviewed toolchain is supplied.

`FILE_MANIFEST.json` is the immutable 58-file pre-import candidate baseline (57 entries plus itself). `IMPORT_PROVENANCE.json` records the initial import mapping and hashes, including its README merge and relocated license review notice. Subsequent documentation updates do not rewrite that historical baseline. Original research history and private audit/validation files are excluded.

## Repository and research boundaries

The intended open-source release is a **clean, reusable Core**, not a mirror of the internal research environment. The original engineering inventory was roughly 94.7 MB and contained substantial third-party mathematical source material. The smaller public candidate deliberately excludes original research states, papers, private results, system-specific configuration, cached environments, and historical Git objects.

Publication of framework code should not be construed as:

- a release of unpublished mathematical results or private evidence;
- permission to redistribute unrelated third-party code or data;
- proof that an automatically generated claim is correct or novel;
- a guarantee that future experimental modules or hosted services will be released.

## Roadmap

| Stage | Goal |
| --- | --- |
| **01 · Foundation** | Import the audited Core, verify a clean installation, and run GitHub CI. |
| **02 · Documentation** | Publish the implementation-grounded system map, full research lifecycle, API contracts, and a minimal synthetic example. |
| **03 · Research tooling** | Improve tool adapters, evidence handling, formal-verification workflows, and clearly defined scientific gates. |
| **04 · Evaluation** | Compare research workflows under controlled budgets, including failure analysis, independent validation, and ablations. |
| **05 · Research dissemination** | Release reviewed case studies and methodological papers only when their correctness, provenance, and scientific contributions are substantiated. |

The roadmap is an intention, not a delivery schedule or a claim of completed scientific work.

## Contributions and responsible use

MathForge is at a pre-release stage. After the public source is available, contributions should prioritize reproducible bug reports, tests, documentation, validation adapters, and clearly scoped improvements. Research submissions should identify assumptions, provenance, verification limits, and remaining uncertainty.

If you use any automated mathematical research workflow, **do not present model-generated reasoning as an established theorem without independent checking**. Formal proof assistants check statements under their encoded assumptions; they do not automatically settle whether those statements faithfully capture an original scientific question.

## 中文简介

**MathForge** 是一个面向数学研究的自动化框架项目，核心理念是：**生成数学候选结果只是开始，独立验证、科学门禁与可复现证据同样重要。**

长期目标是将数学问题输入、历史去重、证明与反例探索、计算验证、Lean 等形式化工具以及证据归档组织为可审计的研究流程，并明确区分 **PASS / HOLD / KILL** 等研究状态。

**当前状态：** GitHub 仓库仍处于私有预发布阶段，已包含品牌素材和文档。一个独立提取的精简 Core 候选已在本地通过 29 项测试与合成 Lean 检查，；精简 CORE 源码现已在本私有导入 PR 中提交，公开分发仍待权属和授权审核，也不能据此声称已经验证完整自主数学发现能力。未发表科研资产不属于计划中的开源 Core。

欢迎关注后续代码导入、正式架构图与可复现演示。本 README 将随实际实现与独立验证进度更新。

---

## License and provenance

This repository contains the text of the [Apache License, Version 2.0](./LICENSE), which is the **intended license** for the reviewed Core release. Before public distribution, maintainers must confirm contributor ownership, institutional and collaborator rights, third-party attribution, and the precise files authorized for release. The presence of a license file is **not** a substitute for those checks.

**MathForge · Research with evidence.**
