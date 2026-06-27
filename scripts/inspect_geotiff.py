from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import rasterio

def inspect_geotiff(path: Path) -> None:
    """GeoTIFFの基本情報と値の範囲を表示する。

    元のGeoTIFFがどのようなband数、サイズ、座標系、値の範囲を持っているかを確認する。

    Args:
        path: 確認対象のGeoTIFFファイルパス。
    """
    with rasterio.open(path) as dataset:
        print(f"file: {path}")
        print(f"width: {dataset.width}")
        print(f"height: {dataset.height}")
        print(f"band count: {dataset.count}")
        print(f"dtype: {dataset.dtypes}")
        print(f"crs: {dataset.crs}")
        print(f"bounds: {dataset.bounds}")
        print(f"transform: {dataset.transform}")

        band = dataset.read(1).astype(np.float32)

    valid = np.isfinite(band)

    values = band[valid]

    print(f"min: {values.min()}")
    print(f"max: {values.max()}")
    print(f"mean: {values.mean()}")
    print(f"2nd percentile: {np.percentile(values, 2)}")
    print(f"50th percentile: {np.percentile(values, 50)}")
    print(f"98th percentile: {np.percentile(values, 98)}")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "paths",
        nargs="+"
    )
    args = parser.parse_args()

    for path in args.paths:
        inspect_geotiff(Path(path))

if __name__ == "__main__":
    main()