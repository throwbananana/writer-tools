# writer-tools 修复说明（工程基线版）

这个补丁包针对当前仓库最紧急的工程问题做了一轮可落地修复，重点不是改业务功能，而是先补齐“能稳定安装、能跑最小校验、能接入 CI”的基础设施。

## 本次修复内容

- 重写 `requirements.txt`，改为通过 `constraints.txt` 约束版本。
- 新增 `requirements-dev.txt`，拆分开发依赖。
- 新增 `pytest.ini`，稳定测试发现行为。
- 新增 `.github/workflows/ci.yml`，提供跨平台最小 CI。
- 新增 `.gitignore`，清理临时目录与本地产物。
- 新增 `tests/test_smoke_project_manager.py`，先把无 GUI / 无音频的基础回归跑起来。
- 新增 `docs/REPAIR_NOTES.md`，说明此次修复范围与后续建议。

## 为什么先修这些

当前项目已经是一个较大的桌面工具工程，根目录可见多个启动脚本，`writer_app` 目录下也已经拆分出 `core / ui / controllers / utils`，其中 `writer_app/main.py` 本身就超过两千行。对这类工程，先建立依赖、测试和 CI 护栏，比直接猜测业务代码更安全。

## 安装建议

### 运行依赖

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 开发依赖

```bash
python -m pip install -r requirements-dev.txt
```

## 音频依赖说明

项目包含语音相关依赖（`SpeechRecognition` / `PyAudio` / `pyttsx3`）。

- Windows：通常可直接 `pip install PyAudio`
- macOS：先安装 `portaudio`
- Debian/Ubuntu：建议先装 `portaudio19-dev` 与 Python 开发头文件

如果你只是先做核心逻辑开发或跑最小 smoke test，建议优先在 CI 和本地验证 `ProjectManager` 这一类无设备依赖模块。

## CI 当前策略

当前工作流是“保守起步”：

1. 安装依赖
2. 运行 Ruff
3. 只跑 `tests/test_smoke_project_manager.py`
4. 运行 `pip-audit`（暂不阻塞）

这样做的目的，是先让仓库拥有稳定、可执行的最小质量门禁，再逐步把现有测试纳入矩阵。

## 推荐下一步

- 把现有 `tests/` 中已有测试逐个接入 CI，按模块分组。
- 为 `writer_app/core/backup.py`、`writer_app/core/commands.py`、`writer_app/core/audio.py` 增加更细粒度单测。
- 将音频依赖进一步模块化，降低默认安装失败率。
- 逐步把 `writer_app/main.py` 继续拆分，减轻主入口耦合。
