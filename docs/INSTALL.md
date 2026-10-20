# 安装与验收

使用新建虚拟环境，不能依赖旧工作区的 .venv、reports/local、Mathlib、SSH 或应用登录。根 README 给出了完整安装命令。依赖锁下载自公共 PyPI，要求哈希校验；未附带第三方 wheel。锁文件针对 Windows CPython 3.13 x64 构件。

已有合成示例可直接运行 `python scripts/mathforge.py validate`。也可 `python -m mathforge init --output reports/local/work001` 创建全新示例，再以 `--root` 指定该目录。所有示例与测试输出只能写入 reports/local。重复目录、导出文件和收据不会被覆盖。

## 可选 Lean 接口

Lean 为用户自行安装、审查的可选工具；当前适配版本为 4.24.0。不下载、捆绑或自动安装 Lean/Mathlib。

```python
from pathlib import Path
from mathforge.workspace import initialize
from mathforge.lean import pin_toolchain, check

root = initialize(Path('reports/local/lean-demo001'))
# 操作者提供并审查自己的 Lean 可执行文件；不从任务提议中读取工具链配置。
executable = Path('lean.exe').resolve()
policy = pin_toolchain(executable)
task = {'natural_language': 'Synthetic interface smoke only: True.',
        'imports': ['Init'],
        'targets': [{'name': 'Smoke', 'type': 'True',
                     'proof': {'kind': 'exact', 'term': 'True.intro'}}]}
receipt = check(task, root/'reports/local/check001', workspace=root,
                lean=executable, reviewed_policy=policy)
print(receipt['status'])
```

Windows Job Object 限制内存，编译与检查共享超时预算。其他操作系统的此资源适配器返回 HOLD。缺工具、哈希变化、非法导入、非法证书、错误类型、超时均不能报告成功。工具链哈希不等于对编译器、标准库或操作系统的独立安全认证；这里不提供执行任意 Lean 源码的安全沙箱。

设置 `MATHFORGE_TEST_LEAN` 为已审查的本地 Lean 4.24.0 可执行文件路径，可启用测试中的真实 `True` 检查与错误类型拒绝。未设置时该项明确跳过，不伪造 Lean 成功。CI 默认只验证核心和失败关闭行为；云端 CI 尚未实际运行。
