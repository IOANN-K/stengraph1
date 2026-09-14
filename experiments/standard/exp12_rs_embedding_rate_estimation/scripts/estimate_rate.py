import numpy as np


def prepare_calibration(
    points,
):
    points = sorted(
        points,
        key=lambda item: item[0],
    )

    rates = np.array(
        [
            point[0]
            for point in points
        ],
        dtype=np.float64,
    )

    gaps = np.array(
        [
            point[1]
            for point in points
        ],
        dtype=np.float64,
    )

    order = np.argsort(
        gaps
    )

    return (
        gaps[order],
        rates[order],
    )


def estimate_rate(
    gap,
    calibration_points,
):
    gaps, rates = prepare_calibration(
        calibration_points
    )

    estimate = np.interp(
        gap,
        gaps,
        rates,
    )

    return float(
        np.clip(
            estimate,
            0.0,
            100.0,
        )
    )