from __future__ import annotations

from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from spec_rt import SpectraDecomposing, fit_spectrum
from spec_rt.spectra_decomposing_io import (
    load_six_column_spectrum,
    validate_absorption_input,
)
from spec_rt.spectra_decomposing_plotting import create_legacy_axes


def test_example_spec_loader_keeps_absorption_input():
    x, y, yerr, xemi, yemi, yemi_err = load_six_column_spectrum(
        ROOT / "examples" / "example_spec.txt",
        absorption_format="one_minus_exp_tau",
    )
    stats = validate_absorption_input(y, yerr)

    assert x.ndim == 1
    assert y.ndim == 1
    assert x.size == y.size == yerr.size
    assert xemi.size == yemi.size == yemi_err.size
    assert abs(stats["baseline_mean"]) < max(stats["noise_level"] * 3.0, stats["baseline_std"] * 3.0)


def test_example_spec_gaussfitspec_absorption_fit_runs():
    x, y, yerr, _, _, _ = load_six_column_spectrum(
        ROOT / "examples" / "example_spec.txt",
        absorption_format="one_minus_exp_tau",
    )
    result = fit_spectrum(
        x,
        y,
        yerr,
        method="bic",
        max_components=8,
    )

    assert result.parameters.ndim == 1
    assert result.parameters.size >= 3
    assert result.best_model.shape == y.shape


def test_example_spec_full_plot_generation(tmp_path):
    x, y, yerr, xemi, yemi, yemi_err = load_six_column_spectrum(
        ROOT / "examples" / "example_spec.txt",
        absorption_format="one_minus_exp_tau",
    )
    fig, axes = create_legacy_axes(figsize=(12, 8), dpi=150)

    spec_fit = SpectraDecomposing(x, y, yerr, xemi, yemi, yemi_err)
    spec_fit.name = "example-spec-test"
    spec_fit.v_shift = 4
    spec_fit.peak_abs = []
    spec_fit.peak_emi = []
    spec_fit.max_auto_warm_components = 1
    spec_fit.Tsmin = 10
    spec_fit.Tsky = 2.73
    spec_fit.fit_mode = "BIC"
    spec_fit.ax = axes
    spec_fit.savecsv = False
    spec_fit.renew = False
    spec_fit.align_data = True
    spec_fit.bic_weight = 10
    result = spec_fit.fit_and_plot()

    output = tmp_path / "example_spec_fit_test.png"
    fig.savefig(output, bbox_inches="tight")

    assert result is not None
    assert output.exists()
    assert output.stat().st_size > 0
