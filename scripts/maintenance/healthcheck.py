from __future__ import annotations

import argparse
import importlib
import platform
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

CORE_MODULES = [
    ("requests", "requests"),
    ("PIL", "Pillow"),
    ("pygame", "pygame"),
    ("pystray", "pystray"),
    ("reportlab", "reportlab"),
    ("docx", "python-docx"),
]

OPTIONAL_AUDIO_MODULES = [
    ("speech_recognition", "SpeechRecognition"),
    ("pyaudio", "PyAudio"),
    ("pyttsx3", "pyttsx3"),
]

REQUIRED_PATHS = [
    "start_app.py",
    "start_tools.py",
    "writer_app/main.py",
    "writer_app/core/models.py",
    "writer_app/core/exporter.py",
]


@dataclass
class CheckItem:
    label: str
    ok: bool
    detail: str = ""


@dataclass
class CheckReport:
    core: List[CheckItem]
    optional: List[CheckItem]
    repo: List[CheckItem]
    warnings: List[str]

    @property
    def is_ok(self) -> bool:
        return all(item.ok for item in self.core + self.repo)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _check_module(import_name: str, display_name: str) -> CheckItem:
    try:
        importlib.import_module(import_name)
        return CheckItem(display_name, True, "已安装")
    except Exception as exc:
        return CheckItem(display_name, False, f"未安装或无法导入: {exc}")


def _scan_temp_dirs(root: Path) -> List[str]:
    hits: List[str] = []
    for path in root.iterdir():
        name = path.name
        if not path.is_dir():
            continue
        if name == "__pycache__" or name.startswith("tmpclaude-") or name in {"build", "dist", ".pytest_cache", ".ruff_cache"}:
            hits.append(name)
    return sorted(hits)


def build_report(root: Path | None = None) -> CheckReport:
    root = root or _repo_root()
    core: List[CheckItem] = []
    optional: List[CheckItem] = []
    repo: List[CheckItem] = []
    warnings: List[str] = []

    py_ok = sys.version_info >= (3, 9)
    core.append(CheckItem("Python >= 3.9", py_ok, platform.python_version()))
    core.append(_check_module("tkinter", "tkinter"))
    core.extend(_check_module(name, display) for name, display in CORE_MODULES)
    optional.extend(_check_module(name, display) for name, display in OPTIONAL_AUDIO_MODULES)

    for rel in REQUIRED_PATHS:
        path = root / rel
        repo.append(CheckItem(rel, path.exists(), "存在" if path.exists() else "缺失"))

    junk = _scan_temp_dirs(root)
    if junk:
        warnings.append("发现可清理目录: " + ", ".join(junk))

    if not (root / "requirements-audio.txt").exists():
        warnings.append("未发现 requirements-audio.txt，建议覆盖升级包中的依赖拆分文件。")

    return CheckReport(core=core, optional=optional, repo=repo, warnings=warnings)


def format_report(report: CheckReport, root: Path) -> str:
    lines: List[str] = []
    lines.append(f"Writer Tool 环境体检")
    lines.append(f"项目根目录: {root}")
    lines.append("")

    lines.append("[核心环境]")
    for item in report.core:
        lines.append(f"{'OK ' if item.ok else 'ERR'} {item.label}: {item.detail}")

    lines.append("")
    lines.append("[可选语音能力]")
    for item in report.optional:
        lines.append(f"{'OK ' if item.ok else 'MISS'} {item.label}: {item.detail}")

    lines.append("")
    lines.append("[项目关键文件]")
    for item in report.repo:
        lines.append(f"{'OK ' if item.ok else 'MISS'} {item.label}: {item.detail}")

    if report.warnings:
        lines.append("")
        lines.append("[提醒]")
        for warning in report.warnings:
            lines.append(f"- {warning}")

    lines.append("")
    lines.append("结论: " + ("可正常启动" if report.is_ok else "存在阻塞问题，需要先修复"))
    return "\n".join(lines)


def _show_gui_report(text: str) -> None:
    import tkinter as tk
    from tkinter import ttk

    root = tk.Tk()
    root.title("Writer Tool 环境体检")
    root.geometry("760x620")

    box = tk.Text(root, wrap=tk.WORD, font=("Consolas", 10))
    box.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
    box.insert("1.0", text)
    box.configure(state=tk.DISABLED)

    ttk.Button(root, text="关闭", command=root.destroy).pack(pady=(0, 12))
    root.mainloop()


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Writer Tool 环境体检")
    parser.add_argument("--gui", action="store_true", help="使用图形界面显示结果")
    args = parser.parse_args(list(argv) if argv is not None else None)

    root = _repo_root()
    report = build_report(root)
    text = format_report(report, root)
    print(text)

    if args.gui:
        try:
            _show_gui_report(text)
        except Exception as exc:
            print(f"\n无法打开图形界面: {exc}")

    return 0 if report.is_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
