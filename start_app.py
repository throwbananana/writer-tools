from __future__ import annotations

import sys
import traceback
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parent


def _ensure_repo_on_path() -> Path:
    root = _repo_root()
    root_str = str(root)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)
    return root


def _show_error(title: str, message: str) -> None:
    try:
        import tkinter as tk
        from tkinter import messagebox

        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(title, message)
        root.destroy()
    except Exception:
        print(f"\n[{title}]\n{message}\n")


def main() -> int:
    root_dir = _ensure_repo_on_path()

    try:
        import tkinter as tk
    except ImportError:
        print("错误: 当前 Python 环境缺少 tkinter，无法启动桌面界面。")
        return 1

    try:
        from writer_app.main import WriterTool
    except ModuleNotFoundError as exc:
        missing = exc.name or "未知模块"
        _show_error(
            "启动失败",
            "Writer Tool 依赖不完整。\n\n"
            f"缺少模块: {missing}\n\n"
            "建议先执行：\n"
            "pip install -r requirements.txt\n"
            "如需语音功能，再执行：\n"
            "pip install -r requirements-audio.txt",
        )
        return 1
    except Exception as exc:
        _show_error(
            "启动失败",
            "加载主程序时发生异常。\n\n"
            f"{exc}\n\n详细堆栈已输出到控制台。",
        )
        traceback.print_exc()
        return 1

    try:
        root = tk.Tk()
        root.title("Writer Tool")
        root.repo_root = root_dir
        WriterTool(root)
        root.mainloop()
        return 0
    except Exception as exc:
        _show_error(
            "运行时错误",
            "程序启动后发生异常。\n\n"
            f"{exc}\n\n详细堆栈已输出到控制台。",
        )
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
