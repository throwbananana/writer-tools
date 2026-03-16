from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from writer_app.core.models import ProjectManager  # noqa: E402


def test_project_manager_can_create_and_save_project(tmp_path: Path) -> None:
    pm = ProjectManager()
    pm.new_project()

    output = tmp_path / "smoke.writerproj"
    assert pm.save_project(str(output)) is True
    assert output.exists()

    payload = json.loads(output.read_text(encoding="utf-8"))
    assert "meta" in payload
    assert "outline" in payload
    assert "script" in payload


def test_project_manager_can_roundtrip_saved_project(tmp_path: Path) -> None:
    original = ProjectManager()
    original.new_project()

    output = tmp_path / "roundtrip.writerproj"
    original.save_project(str(output))

    restored = ProjectManager()
    assert restored.load_project(str(output)) is True
    assert restored.get_project_data()["meta"]["type"]
    assert isinstance(restored.get_outline(), dict)
