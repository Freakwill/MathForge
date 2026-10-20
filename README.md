# MathForge Framework — 本地公开候选

**LOCAL REVIEW ONLY：尚未授权公开分发。Apache-2.0 为候选许可证，权属与正式授权仍待确认。**

这是从研究工作区提取的通用基础设施。包含严格 schema、证据引用、追加式状态日志、重放禁止、科学 Gate、持久审计队列及显式 Lean 接口。随包仅有新生成的合成示例，不含原始论文、未发表结果、实验数据、研究任务、机器配置、凭据、依赖源码或旧 Git 历史。

## 安装与最小演示

当前验收目标为 **Windows x64 / CPython 3.13.9**。锁文件包含该平台下载构件的 SHA-256；其他平台需另行审核锁文件，不宣称已经验证。

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install --require-hashes -r requirements-build.lock
.venv\Scripts\python -m pip install --require-hashes -r requirements.lock
.venv\Scripts\python -m pip install --no-deps --no-build-isolation .
.venv\Scripts\python scripts/mathforge.py validate
.venv\Scripts\python -m mathforge demo --output reports/local/demo001
.venv\Scripts\python -m unittest discover -s tests -v
```

输出目录必须是新的目录。演示创建一个明确标记为 synthetic 的记录，执行两个审计任务：验证与导出。`research_results=0`；示例不是数学实验或原创成果。

## 使用边界

- `validate` 检查结构、引用、状态、哈希链；不认证数学真伪或原创性。
- `transition` 使用排他写锁与 fsync 追加日志，拒绝过期写入及研究／证明状态提升。
- `queue` 支持去重入队、原子领取、失败收据及人工标记中断。仅允许 validate/export，没有 shell、研究 worker 或后台循环。
- `replay-check` 保留永久负知识。`GO_TO_LITERATURE_AUDIT` 仅为审计许可。
- Lean 接口仅支持显式调用的 Init 检查，要求管理员审查的工具链哈希；成功只产生 scoped kernel receipt，不提升工作流为 PROVED。

```powershell
python -m mathforge --root reports/local/demo001 replay-check MF-0000
python -m mathforge --root reports/local/demo001 queue status
```

详见 [安装文档](docs/INSTALL.md)、[架构与边界](docs/ARCHITECTURE.md)、[许可证候选](LICENSE_CANDIDATE.md)。本候选没有仓库远程、上传、发布或自动研究入口。

## Project vision and import scope

An open-source framework for autonomous mathematical research, conjecture generation, formal verification, and reproducible scientific discovery.

The preceding vision describes a long-term goal. This imported CORE implements audit infrastructure and a scoped Lean interface only; autonomous research execution and proof acceptance remain disabled. The existing repository Apache-2.0 text is preserved. Rights review for the imported candidate remains HOLD; see [review notice](docs/legal/LICENSE_REVIEW_NOTICE.txt) and [license candidate](LICENSE_CANDIDATE.md). Private import is authorized; public distribution and Releases are not authorized.
