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
        print(path)
        print(dataset.width)
        print(dataset.height)
        print(dataset.count)
        print(dataset.dtypes)
        print(dataset.crs)
        print(dataset.bounds)
        print(dataset.transform)

        band = dataset.read(1).astype(np.float32)

    valid = np.isfinite(band)

    values = band[valid]

    print(values.min())
    print(values.max())
    print(values.mean())
    print(np.percentile(values, 2))
    print(np.percentile(values, 50))
    print(np.percentile(values, 98))


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