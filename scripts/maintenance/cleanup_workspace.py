from __future__ import annotations

import argparse
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

REMOVE_DIR_NAMES = {
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    "build",
    "dist",
}
REMOVE_PREFIXES = ("tmpclaude-", "tmpgemini-", "tmpgpt-")
REMOVE_FILE_SUFFIXES = (".pyc", ".pyo", ".log", ".tmp")
SKIP_DIR_NAMES = {".git", ".venv", "venv", ".idea", ".vscode", "node_modules"}


@dataclass
class CleanupResult:
    removed: List[Path]
    failed: List[str]


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def should_remove_dir(path: Path) -> bool:
    name = path.name
    return name in REMOVE_DIR_NAMES or any(name.startswith(prefix) for prefix in REMOVE_PREFIXES)


def should_remove_file(path: Path) -> bool:
    return path.suffix.lower() in REMOVE_FILE_SUFFIXES


def collect_cleanup_targets(root: Path) -> List[Path]:
    targets: List[Path] = []
    for path in root.rglob("*"):
        if any(part in SKIP_DIR_NAMES for part in path.parts):
            continue
        if path.is_dir() and should_remove_dir(path):
            targets.append(path)
        elif path.is_file() and should_remove_file(path):
            targets.append(path)
    targets.sort(key=lambda p: (len(p.parts), str(p)), reverse=True)
    return targets


def cleanup(root: Path, dry_run: bool = False) -> CleanupResult:
    removed: List[Path] = []
    failed: List[str] = []
    for path in collect_cleanup_targets(root):
        if dry_run:
            removed.append(path)
            continue
        try:
            if path.is_dir():
                shutil.rmtree(path)
            elif path.exists():
                path.unlink()
            removed.append(path)
        except Exception as exc:
            failed.append(f"{path}: {exc}")
    return CleanupResult(removed=removed, failed=failed)


def format_result(result: CleanupResult, dry_run: bool) -> str:
    lines: List[str] = []
    title = "Writer Tool 工作区清理（预演）" if dry_run else "Writer Tool 工作区清理"
    lines.append(title)
    lines.append("")
    if result.removed:
        lines.append("目标:")
        for item in result.removed:
            lines.append(f"- {item}")
    else:
        lines.append("未发现可清理项。")

    if result.failed:
        lines.append("")
        lines.append("失败项:")
        for item in result.failed:
            lines.append(f"- {item}")

    lines.append("")
    lines.append(f"总计: {len(result.removed)} 项")
    return "\n".join(lines)


def _run_gui(root: Path, dry_run: bool) -> int:
    import tkinter as tk
    from tkinter import messagebox, ttk

    preview = cleanup(root, dry_run=True)
    preview_text = format_result(preview, True)

    win = tk.Tk()
    win.withdraw()
    if not preview.removed:
        messagebox.showinfo("工作区清理", "未发现可清理项。")
        win.destroy()
        return 0

    proceed = messagebox.askyesno("工作区清理", preview_text + "\n\n确认执行清理？")
    win.destroy()
    if not proceed:
        return 0

    result = cleanup(root, dry_run=False)
    text = format_result(result, False)

    root_win = tk.Tk()
    root_win.title("工作区清理结果")
    root_win.geometry("720x560")
    box = tk.Text(root_win, wrap=tk.WORD, font=("Consolas", 10))
    box.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
    box.insert("1.0", text)
    box.configure(state=tk.DISABLED)
    ttk.Button(root_win, text="关闭", command=root_win.destroy).pack(pady=(0, 12))
    root_win.mainloop()
    return 0 if not result.failed else 1


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="清理 Writer Tool 仓库中的临时目录和缓存")
    parser.add_argument("--dry-run", action="store_true", help="仅预览，不执行删除")
    parser.add_argument("--gui", action="store_true", help="使用图形界面")
    args = parser.parse_args(list(argv) if argv is not None else None)

    root = _repo_root()

    if args.gui:
        try:
            return _run_gui(root, args.dry_run)
        except Exception as exc:
            print(f"图形模式失败，切回命令行模式: {exc}")

    result = cleanup(root, dry_run=args.dry_run)
    print(format_result(result, args.dry_run))
    return 0 if not result.failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
