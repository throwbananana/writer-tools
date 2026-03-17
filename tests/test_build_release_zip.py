from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.release.build_release_zip import iter_release_files  # noqa: E402


def test_iter_release_files_skips_temp_and_cache_dirs(tmp_path: Path) -> None:
    (tmp_path / "writer_app").mkdir()
    (tmp_path / "writer_app" / "main.py").write_text("print('ok')", encoding="utf-8")

    (tmp_path / "dist").mkdir()
    (tmp_path / "dist" / "artifact.zip").write_text("x", encoding="utf-8")

    (tmp_path / "tmpclaude-xyz").mkdir()
    (tmp_path / "tmpclaude-xyz" / "junk.txt").write_text("x", encoding="utf-8")

    (tmp_path / "pkg" / "__pycache__").mkdir(parents=True)
    (tmp_path / "pkg" / "__pycache__" / "a.pyc").write_bytes(b"x")

    files = iter_release_files(tmp_path)
    rels = {str(p.relative_to(tmp_path)).replace("\\", "/") for p in files}

    assert "writer_app/main.py" in rels
    assert "dist/artifact.zip" not in rels
    assert "tmpclaude-xyz/junk.txt" not in rels
    assert "pkg/__pycache__/a.pyc" not in rels
