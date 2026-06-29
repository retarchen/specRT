"""Utility helpers shared by the radiative-transfer fitter."""

from __future__ import annotations

import numpy as np
from scipy.interpolate import interp1d


def filter_positive_error_rows(x, y, y_err):
    """Drop rows where the uncertainty is not strictly positive."""
    mask = np.asarray(y_err) > 0
    return np.asarray(x)[mask], np.asarray(y)[mask], np.asarray(y_err)[mask]


def align_spectra_grids(x, y, y_err, xemi, yemi, yemi_err):
    """Interpolate absorption and emission spectra onto a shared velocity grid."""
    common_x = np.linspace(
        max(np.min(xemi), np.min(x)),
        min(np.max(xemi), np.max(x)),
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
