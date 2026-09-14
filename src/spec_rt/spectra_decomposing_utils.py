"""Utility helpers shared by the radiative-transfer fitter."""

from __future__ import annotations

import numpy as np
from scipy.interpolate import interp1d


def filter_positive_error_rows(x, y, y_err):
    """Drop invalid rows and return a unique, ascending velocity grid."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    y_err = np.asarray(y_err, dtype=float)
    if x.ndim != 1 or y.ndim != 1 or y_err.ndim != 1 or not (len(x) == len(y) == len(y_err)):
        raise ValueError("x, y, and y_err must be one-dimensional arrays of equal length.")

    mask = np.isfinite(x) & np.isfinite(y) & np.isfinite(y_err) & (y_err > 0)
    x, y, y_err = x[mask], y[mask], y_err[mask]
    if x.size == 0:
        raise ValueError("No finite samples with positive uncertainties remain.")

    order = np.argsort(x)
    x, y, y_err = x[order], y[order], y_err[order]
    if np.any(np.diff(x) == 0):
        raise ValueError("Velocity values must be unique.")
    return x, y, y_err


def align_spectra_grids(x, y, y_err, xemi, yemi, yemi_err):
    """Interpolate absorption and emission spectra onto a shared velocity grid."""
    overlap_min = max(np.min(xemi), np.min(x))
    overlap_max = min(np.max(xemi), np.max(x))
    if overlap_min >= overlap_max:
        raise ValueError("Absorption and emission velocity grids do not overlap.")
    common_x = np.linspace(
        overlap_min,
        overlap_max,
        min(len(xemi), len(x)),
    )
    interp_emi = interp1d(xemi, yemi, kind="linear", fill_value="extrapolate")
    aligned_yemi = interp_emi(common_x)
    interp_emi_err = interp1d(xemi, yemi_err, kind="linear", fill_value="extrapolate")
    aligned_yemi_err = interp_emi_err(common_x)
    interp_abs = interp1d(x, y, kind="linear", fill_value="extrapolate")
    aligned_y = interp_abs(common_x)
    interp_abs_err = interp1d(x, y_err, kind="linear", fill_value="extrapolate")
    aligned_yerr = interp_abs_err(common_x)
    return common_x, aligned_y, aligned_yerr, common_x, aligned_yemi, aligned_yemi_err
