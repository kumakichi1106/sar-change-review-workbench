from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image
import rasterio


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


def save_grayscale(array: np.ndarray, path: Path) -> None:
    """8bitのNumPy配列をグレースケールPNGとして保存する。

    Args:
        array: 0〜255の画素値を持つ2次元配列。
        path: 保存先のPNGファイルパス。
    """
    Image.fromarray(array.astype(np.uint8), mode="L").save(path)


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


def process_scene(scene_dir: Path, threshold: int) -> None:
    """1つのシーンディレクトリに対して、Web表示用の画像とメトリクスを生成する。

    同じ地域の異なる時期に取得したbefore.tifとafter.tifを想定する。
    それぞれを表示用PNGへ変換し、画像ベースの差分からdiff.png、mask.png、metrics.jsonを生成する。

    GEEで取得したSentinel-1画像を題材に、処理結果をアプリ上で比較・確認・判断する流れを学ぶための処理。

    Args:
        scene_dir: before.tifとafter.tifが配置されたディレクトリ。
        threshold: mask.png生成時に使う差分閾値。
    """
    before_path = scene_dir / "before.tif"
    after_path = scene_dir / "after.tif"

    if not before_path.exists() or not after_path.exists():
        raise FileNotFoundError(f"before.tif and after.tif are required in {scene_dir}")

    before = load_sar_band_as_uint8(before_path)
    after = load_sar_band_as_uint8(after_path)

    if before.shape != after.shape:
        after_image = Image.fromarray(after, mode="L").resize(
            (before.shape[1], before.shape[0])
        )
        after = np.asarray(after_image, dtype=np.uint8)
    # uint8のまま引き算すると負の値が扱えないため、一度int16へ変換する。
    diff = np.abs(after.astype(np.int16) - before.astype(np.int16)).astype(np.uint8)
    mask = create_mask(diff, threshold)

    save_grayscale(before, scene_dir / "before.png")
    save_grayscale(after, scene_dir / "after.png")
    save_grayscale(diff, scene_dir / "diff.png")
    Image.fromarray(mask, mode="RGBA").save(scene_dir / "mask.png")

    changed_pixels = int((diff >= threshold).sum())
    total_pixels = int(diff.size)

    metrics = {
        "threshold": threshold,
        "changedPixels": changed_pixels,
        "totalPixels": total_pixels,
        "changeRatio": round(changed_pixels / total_pixels, 4),
        "note": "画像ベースの簡易差分です。本番レベルのSAR変化検知ではありません。",
    }

    with (scene_dir / "metrics.json").open("w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)


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