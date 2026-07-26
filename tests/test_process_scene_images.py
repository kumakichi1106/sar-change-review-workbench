import numpy as np

from scripts.process_scene_images import (
    build_shape_warnings,
    calculate_metrics,
    create_diff,
    create_mask,
)


def test_create_diff_calculates_absolute_difference() -> None:
    before = np.array([[10, 250]], dtype=np.uint8)
    after = np.array([[20, 240]], dtype=np.uint8)

    diff = create_diff(before, after)

    assert diff.tolist() == [[10, 10]]
    assert diff.dtype == np.uint8


def test_create_diff_avoids_uint8_underflow() -> None:
    before = np.array([[250]], dtype=np.uint8)
    after = np.array([[10]], dtype=np.uint8)

    diff = create_diff(before, after)

    assert diff.tolist() == [[240]]


def test_create_mask_marks_pixels_greater_than_or_equal_to_threshold() -> None:
    diff = np.array([[10, 35], [36, 0]], dtype=np.uint8)

    mask = create_mask(diff, threshold=35)

    assert mask[0, 0].tolist() == [0, 0, 0, 0]
    assert mask[0, 1].tolist() == [255, 64, 64, 180]
    assert mask[1, 0].tolist() == [255, 64, 64, 180]
    assert mask[1, 1].tolist() == [0, 0, 0, 0]


def test_calculate_metrics_counts_changed_pixels() -> None:
    diff = np.array([[10, 35], [36, 0]], dtype=np.uint8)

    metrics = calculate_metrics(diff, threshold=35)

    assert metrics["threshold"] == 35
    assert metrics["changedPixels"] == 2
    assert metrics["totalPixels"] == 4
    assert metrics["changeRatio"] == 0.5


def test_build_shape_warnings_returns_empty_when_shapes_match() -> None:
    before = np.zeros((2, 3), dtype=np.uint8)
    after = np.zeros((2, 3), dtype=np.uint8)

    warnings = build_shape_warnings(before, after)

    assert warnings == []


def test_build_shape_warnings_returns_warning_when_shapes_differ() -> None:
    before = np.zeros((2, 3), dtype=np.uint8)
    after = np.zeros((2, 4), dtype=np.uint8)

    warnings = build_shape_warnings(before, after)

    assert len(warnings) == 1
    assert warnings[0]["type"] == "shape_mismatch"
    assert warnings[0]["beforeShape"] == [2, 3]
    assert warnings[0]["afterShape"] == [2, 4]