from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


REQUIRED_INPUT_FILES = [
    "before.tif",
    "after.tif",
]

REQUIRED_OUTPUT_FILES = [
    "before.png",
    "after.png",
    "diff.png",
    "mask.png",
    "metrics.json",
]

REQUIRED_METRICS_KEYS = [
    "threshold",
    "changedPixels",
    "totalPixels",
    "changeRatio",
    "note",
]

def validate_files(scene_dir: Path, file_names: list[str], label: str) -> bool:
    """指定されたファイル一覧がシーンディレクトリに存在するか確認する。"""
    is_valid = True

    print(label)

    for file_name in file_names:
        file_path = scene_dir / file_name

        if file_path.exists():
            print(f"  OK: {file_name}")
        else:
            print(f"  NG: {file_name} is missing")
            is_valid = False

    return is_valid

def validate_required_files(scene_dir: Path) -> bool:
    """必要な入力ファイルと出力ファイルが揃っているか確認する。"""
    input_ok = validate_files(
        scene_dir,
        REQUIRED_INPUT_FILES,
        "required input files:",
    )

    output_ok = validate_files(
        scene_dir,
        REQUIRED_OUTPUT_FILES,
        "required output files:",
    )

    return input_ok and output_ok


def validate_metrics_json(scene_dir: Path) -> bool:
    """metrics.jsonに必要なキーが含まれているか確認する。

    Args:
        scene_dir: metrics.jsonが配置されているシーンディレクトリ。

    Returns:
        metrics.jsonが存在し、必要なキーがすべて含まれている場合はTrue。
    """
    metrics_path = scene_dir / "metrics.json"

    if not metrics_path.exists():
        print("metrics.json: NG, file is missing")
        return False

    with open(metrics_path, encoding="utf-8") as file:
        metrics = json.load(file)

    is_valid = True

    print("metrics keys:")

    for key in REQUIRED_METRICS_KEYS:
        if key in metrics:
            print(f"  OK: {key} = {metrics[key]}")
        else:
            print(f"  NG: {key} is missing")
            is_valid = False

    return is_valid


def validate_scene(scene_dir: Path) -> bool:
    """想定通りのファイルが揃っているか確認する。

    手動処理で生成した入力・出力ファイルが揃っているかを確認する。

    Args:
        scene_dir: 検証対象のシーンディレクトリ。

    Returns:
        ファイルとmetrics.jsonの検証が通った場合はTrue。
    """
    print(f"scene_dir: {scene_dir}")

    files_ok = validate_required_files(scene_dir)

    metrics_ok = validate_metrics_json(scene_dir)


    if files_ok and metrics_ok:
        print("result: OK")
        return True

    print("result: NG")
    return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scene-dir",
        default="public/data/scenes/yokohama-sentinel-1",
    )
    args = parser.parse_args()

    is_valid = validate_scene(Path(args.scene_dir))

    if not is_valid:
        raise SystemExit(1)


if __name__ == "__main__":
    main()