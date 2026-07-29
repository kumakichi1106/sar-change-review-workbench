from pathlib import Path


SCENES_DIR = Path(__file__).resolve().parents[2] / "public" / "data" / "scenes"


def list_scene_ids() -> list[str]:
    if not SCENES_DIR.exists():
        return []

    return sorted(path.name for path in SCENES_DIR.iterdir() if path.is_dir())