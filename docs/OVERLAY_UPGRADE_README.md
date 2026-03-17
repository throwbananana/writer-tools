# Writer Tool 覆盖升级包（工程增强版）

这个升级包优先解决四类问题：

1. **安装门槛高**：把运行依赖拆成 `requirements-core.txt` 和 `requirements-audio.txt`
2. **启动报错不友好**：增强 `start_app.py`，缺依赖时给出更直接的提示
3. **仓库临时目录太多**：新增工作区清理脚本
4. **对外打包容易带垃圾文件**：新增发布 ZIP 构建脚本

## 覆盖方式

把 ZIP 里的文件直接解压到仓库根目录，选择“覆盖全部”。

## 建议升级顺序

1. 解压覆盖
2. 执行 `launch_healthcheck.bat`
3. 执行 `launch_cleanup.bat`
4. 正常运行 `python start_app.py`
5. 需要对外分发时执行 `launch_build_release.bat`

## 依赖安装

仅安装核心功能：

```bash
pip install -r requirements.txt
```

需要语音/音频功能时再额外安装：

```bash
pip install -r requirements-audio.txt
```

## 新增脚本

- `scripts/maintenance/healthcheck.py`：环境体检
- `scripts/maintenance/cleanup_workspace.py`：清理缓存和临时目录
- `scripts/release/build_release_zip.py`：生成干净发布 ZIP

## 风险说明

本升级包故意避免大改 `writer_app/main.py` 主业务逻辑，属于**低风险工程增强包**。
主程序核心功能、项目数据格式和现有控制器逻辑都不做侵入式改动。
