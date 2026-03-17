from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.maintenance.cleanup_workspace import collect_cleanup_targets  # noqa: E402


def test_collect_cleanup_targets_finds_temp_dirs_and_pyc(tmp_path: Path) -> None:
    (tmp_path / "tmpclaude-1234-cwd").mkdir()
    pycache = tmp_path / "pkg" / "__pycache__"
    pycache.mkdir(parents=True)
    pyc = tmp_path / "pkg" / "sample.pyc"
    pyc.write_bytes(b"x")
    keep = tmp_path / ".git" / "config"
    keep.parent.mkdir(parents=True)
    keep.write_text("[core]", encoding="utf-8")

    targets = collect_cleanup_targets(tmp_path)
    rels = {str(p.relative_to(tmp_path)).replace("\\", "/") for p in targets}

    assert "tmpclaude-1234-cwd" in rels
    assert "pkg/__pycache__" in rels
    assert "pkg/sample.pyc" in rels
    assert ".git/config" not in rels
