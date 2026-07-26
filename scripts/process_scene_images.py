from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image
import rasterio


def validate_input_files(before_path: Path, after_path: Path) -> None:
    if not before_path.exists() or not after_path.exists():
        raise FileNotFoundError(
            f"before.tif and after.tif are required in {before_path.parent}"
        )


def load_sar_band_as_uint8(path: Path) -> np.ndarray:
    """GeoTIFFの1バンド目を読み込み、8bit画像配列に変換する。

    GEEから取得したSentinel-1の画像は、通常のPNG/JPEGのような
    0〜255の画素値ではなく、SARの後方散乱強度の値を持つ。

    そのままだとWeb画面で表示しづらいため、値の2〜98パーセンタイルを使って
    0〜255のuint8配列へ変換する。

    Args:
        path: 読み込むGeoTIFFファイルのパス。

    Returns:
        0〜255に正規化されたグレースケール画像配列。
    """
    with rasterio.open(path) as dataset:
        band = dataset.read(1).astype(np.float32)

    valid = np.isfinite(band)
    if not valid.any():
        return np.zeros_like(band, dtype=np.uint8)

    values = band[valid]
    low, high = np.percentile(values, [2, 98])

    if high <= low:
        return np.zeros_like(band, dtype=np.uint8)

    stretched = np.zeros_like(band, dtype=np.float32)
    stretched[valid] = (band[valid] - low) / (high - low)

    return np.clip(stretched * 255, 0, 255).astype(np.uint8)


def build_shape_warnings(before: np.ndarray, after: np.ndarray) -> list[dict]:
    if before.shape == after.shape:
        return []

    return [
        {
            "type": "shape_mismatch",
            "message": "before and after shapes are different. after image was resized to match before image.",
            "beforeShape": list(before.shape),
            "afterShape": list(after.shape),
        }
    ]


def resize_to_match_before(before: np.ndarray, after: np.ndarray) -> np.ndarray:
    after_image = Image.fromarray(after, mode="L").resize(
        (before.shape[1], before.shape[0])
    )
    return np.asarray(after_image, dtype=np.uint8)


def create_diff(before: np.ndarray, after: np.ndarray) -> np.ndarray:
    """before/after画像の絶対差分を生成する。"""
    return np.abs(after.astype(np.int16) - before.astype(np.int16)).astype(np.uint8)


def create_mask(diff: np.ndarray, threshold: int) -> np.ndarray:
    """差分画像から、変化候補を示す半透明の赤色マスクを生成する。

    before/after画像の差分がthreshold以上の画素を「変化候補」とみなし、
    フロント側で重ねて表示しやすいRGBA画像を生成する。

    Args:
        diff: before/afterの差分画像。
        threshold: 変化候補とみなす差分の閾値。

    Returns:
        変化候補を赤色で表したRGBA画像配列。
    """
    mask = diff >= threshold
    rgba = np.zeros((*diff.shape, 4), dtype=np.uint8)
    rgba[mask] = [255, 64, 64, 180]
    return rgba


def save_grayscale(array: np.ndarray, path: Path) -> None:
    """8bitのNumPy配列をグレースケールPNGとして保存する。

    Args:
        array: 0〜255の画素値を持つ2次元配列。
        path: 保存先のPNGファイルパス。
    """
    Image.fromarray(array.astype(np.uint8), mode="L").save(path)


def calculate_metrics(diff: np.ndarray, threshold: int) -> dict:
    changed_pixels = int((diff >= threshold).sum())
    total_pixels = int(diff.size)
    change_ratio = round(changed_pixels / total_pixels, 4)

    return {
        "threshold": threshold,
        "changedPixels": changed_pixels,
        "totalPixels": total_pixels,
        "changeRatio": change_ratio,
        "note": "画像ベースの簡易差分です。本番レベルのSAR変化検知ではありません。",
    }


def write_json(path: Path, data: dict) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def build_processing_report(
    scene_dir: Path,
    before_path: Path,
    after_path: Path,
    threshold: int,
    same_shape: bool,
    warnings: list[dict],
    metrics: dict,
) -> dict:
    return {
        "sceneId": scene_dir.name,
        "inputs": {
            "before": before_path.name,
            "after": after_path.name,
        },
        "parameters": {
            "threshold": threshold,
            "normalization": "percentile_2_98",
        },
        "validation": {
            "sameShape": same_shape,
            "warnings": warnings,
        },
        "outputs": {
            "beforePng": "before.png",
            "afterPng": "after.png",
            "diffPng": "diff.png",
            "maskPng": "mask.png",
            "metricsJson": "metrics.json",
            "processingReportJson": "processing_report.json",
        },
        "metrics": {
            "changedPixels": metrics["changedPixels"],
            "totalPixels": metrics["totalPixels"],
            "changeRatio": metrics["changeRatio"],
        },
        "note": "画像ベースの簡易差分です。本番レベルのSAR変化検知ではありません。",
    }


def process_scene(scene_dir: Path, threshold: int) -> None:
    """1つのシーンディレクトリに対して、Web表示用の画像とメトリクスを生成する。"""
    before_path = scene_dir / "before.tif"
    after_path = scene_dir / "after.tif"

    validate_input_files(before_path, after_path)

    before = load_sar_band_as_uint8(before_path)
    after = load_sar_band_as_uint8(after_path)

    same_shape = before.shape == after.shape
    warnings = build_shape_warnings(before, after)

    if not same_shape:
        after = resize_to_match_before(before, after)

    diff = create_diff(before, after)
    mask = create_mask(diff, threshold)

    save_grayscale(before, scene_dir / "before.png")
    save_grayscale(after, scene_dir / "after.png")
    save_grayscale(diff, scene_dir / "diff.png")
    Image.fromarray(mask, mode="RGBA").save(scene_dir / "mask.png")

    metrics = calculate_metrics(diff, threshold)
    write_json(scene_dir / "metrics.json", metrics)

    processing_report = build_processing_report(
        scene_dir=scene_dir,
        before_path=before_path,
        after_path=after_path,
        threshold=threshold,
        same_shape=same_shape,
        warnings=warnings,
        metrics=metrics,
    )
    write_json(scene_dir / "processing_report.json", processing_report)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scene-dir",
        default="public/data/scenes/yokohama-sentinel-1",
    )
    parser.add_argument("--threshold", type=int, default=35)
    args = parser.parse_args()

    process_scene(Path(args.scene_dir), args.threshold)


if __name__ == "__main__":
    main()
