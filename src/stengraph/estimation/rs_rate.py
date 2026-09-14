import numpy as np


def prepare_calibration(points: list[tuple[float, float]]) -> tuple[np.ndarray, np.ndarray]:
    if len(points) < 2:
        raise ValueError("At least two calibration points are required")
    points = sorted(points, key=lambda item: item[0])
    rates = np.array([point[0] for point in points], dtype=np.float64)
    gaps = np.array([point[1] for point in points], dtype=np.float64)
    order = np.argsort(gaps)
    return gaps[order], rates[order]


def estimate_rate(gap: float, calibration_points: list[tuple[float, float]]) -> float:
    gaps, rates = prepare_calibration(calibration_points)
    return float(np.clip(np.interp(gap, gaps, rates), 0.0, 100.0))
