from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Iterable, List
from zipfile import ZIP_DEFLATED, ZipFile

EXCLUDE_DIR_NAMES = {
    ".git",
    ".venv",
    "venv",
    ".idea",
    ".vscode",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    "build",
    "dist",
}
EXCLUDE_PREFIXES = ("tmpclaude-", "tmpgemini-", "tmpgpt-")
EXCLUDE_FILE_SUFFIXES = (".pyc", ".pyo", ".log", ".tmp")
EXCLUDE_FILE_NAMES = {"Thumbs.db", ".DS_Store"}


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def should_skip(path: Path, root: Path) -> bool:
    rel = path.relative_to(root)
    for part in rel.parts:
        if part in EXCLUDE_DIR_NAMES:
            return True
        if any(part.startswith(prefix) for prefix in EXCLUDE_PREFIXES):
            return True
    return False


def iter_release_files(root: Path) -> List[Path]:
    files: List[Path] = []
    for path in root.rglob("*"):
        if should_skip(path, root):
            continue
        if path.is_dir():
            continue
        if path.name in EXCLUDE_FILE_NAMES:
            continue
        if path.suffix.lower() in EXCLUDE_FILE_SUFFIXES:
            continue
        files.append(path)
    files.sort()
    return files


def build_release_zip(root: Path, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    zip_path = output_dir / f"writer-tools-release-{stamp}.zip"
    manifest = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "root": str(root),
        "file_count": 0,
        "files": [],
    }

    files = iter_release_files(root)
    with ZipFile(zip_path, "w", compression=ZIP_DEFLATED) as zf:
        for path in files:
            arcname = path.relative_to(root)
            zf.write(path, arcname)
            manifest["files"].append(str(arcname).replace("\\", "/"))
        manifest["file_count"] = len(files)
        zf.writestr("release_manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))

    return zip_path


def _run_gui(root: Path, output_dir: Path) -> int:
    import tkinter as tk
    from tkinter import messagebox

    preview_count = len(iter_release_files(root))
    win = tk.Tk()
    win.withdraw()
    ok = messagebox.askyesno(
        "打包发布 ZIP",
        f"将把 {preview_count} 个文件打进发布包。\n\n输出目录: {output_dir}\n\n是否继续？",
    )
    win.destroy()
    if not ok:
        return 0

    zip_path = build_release_zip(root, output_dir)

    win = tk.Tk()
    win.withdraw()
    messagebox.showinfo("打包完成", f"已生成发布包:\n{zip_path}")
    win.destroy()
    print(zip_path)
    return 0


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="构建 Writer Tool 发布 ZIP")
    parser.add_argument("--output-dir", default="dist", help="输出目录，默认 dist")
    parser.add_argument("--gui", action="store_true", help="使用图形界面")
    args = parser.parse_args(list(argv) if argv is not None else None)

    root = _repo_root()
    output_dir = root / args.output_dir

    if args.gui:
        try:
            return _run_gui(root, output_dir)
        except Exception as exc:
            print(f"图形模式失败，切回命令行模式: {exc}")

    zip_path = build_release_zip(root, output_dir)
    print(f"已生成发布包: {zip_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
