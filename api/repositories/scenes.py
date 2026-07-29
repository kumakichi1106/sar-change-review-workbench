import json
from pathlib import Path

SCENES_DIR = Path(__file__).resolve().parents[2] / "public" / "data" / "scenes"


def list_scene_ids() -> list[str]:
    if not SCENES_DIR.exists():
        return []

    return sorted(path.name for path in SCENES_DIR.iterdir() if path.is_dir())


def get_scene_dir(scene_id: str) -> Path:
    if scene_id != Path(scene_id).name:
        raise FileNotFoundError(scene_id)

    scene_dir = SCENES_DIR / scene_id

    if not scene_dir.is_dir():
        raise FileNotFoundError(scene_id)

    return scene_dir


def read_scene_json(scene_id: str, file_name: str) -> dict[str, object]:
    scene_dir = get_scene_dir(scene_id)
    json_path = scene_dir / file_name

    if not json_path.is_file():
        raise FileNotFoundError(json_path)

    with json_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError(f"{json_path} must contain a JSON object")

    return data
