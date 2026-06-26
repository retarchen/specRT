from __future__ import annotations

from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from Absorption_fitting import SpectraDecomposing, fit_spectrum
from Absorption_fitting.spectra_decomposing_io import (
    load_six_column_spectrum,
    validate_absorption_input,
)
from Absorption_fitting.spectra_decomposing_plotting import create_legacy_axes


def test_r4_loader_converts_absorption_input():
    x, y, yerr, xemi, yemi, yemi_err = load_six_column_spectrum(
        ROOT / "examples" / "r4.txt",
        absorption_format="transmission",
    )
    stats = validate_absorption_input(y, yerr)

    assert x.ndim == 1
    assert y.ndim == 1
    assert x.size == y.size == yerr.size
    assert xemi.size == yemi.size == yemi_err.size
    assert abs(stats["baseline_mean"]) < max(stats["noise_level"] * 3.0, stats["baseline_std"] * 3.0)


def test_r4_gaussfitspec_absorption_fit_runs():
    x, y, yerr, _, _, _ = load_six_column_spectrum(
        ROOT / "examples" / "r4.txt",
        absorption_format="transmission",
    )
    result = fit_spectrum(x, y, yerr, method="bic", max_components=8)

    assert result.parameters.ndim == 1
    assert result.parameters.size >= 3
    assert result.best_model.shape == y.shape


def test_r4_full_plot_generation(tmp_path):
    x, y, yerr, xemi, yemi, yemi_err = load_six_column_spectrum(
        ROOT / "examples" / "r4.txt",
        absorption_format="transmission",
    )
    fig, axes = create_legacy_axes(figsize=(12, 8), dpi=150)

    spec_fit = SpectraDecomposing(x, y, yerr, xemi, yemi, yemi_err)
    spec_fit.name = "r4-test"
    spec_fit.v_shift = 4
    spec_fit.peak_abs = []
    spec_fit.peak_emi = [-250, -230]
    spec_fit.Tsmin = 10
    spec_fit.Tsky = 2.73
    spec_fit.fit_mode = "BIC"
    spec_fit.ax = axes
    spec_fit.savecsv = False
    spec_fit.renew = False
    spec_fit.align_data = True
    spec_fit.bic_weight = 10
    result = spec_fit.fit_and_plot()

    output = tmp_path / "r4_fit_test.png"
    fig.savefig(output, bbox_inches="tight")

    assert result is not None
    assert output.exists()
    assert output.stat().st_size > 0
