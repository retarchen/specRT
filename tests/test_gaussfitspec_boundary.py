from __future__ import annotations

from pathlib import Path
import sys
import contextlib
import io

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from spec_rt import fit_spectrum
from spec_rt.spectra_decomposing import _GaussianFitSpecAdapter


def test_fit_spectrum_fixed_component_boundary_case():
    velocity = np.linspace(-5.0, 5.0, 41)
    spectrum = 0.8 * np.exp(-0.5 * ((velocity - 0.5) / 1.0) ** 2)
    spectrum_err = np.full_like(velocity, 0.05)

    result = fit_spectrum(
        velocity,
        spectrum,
        spectrum_err,
        method="bic",
        fixed_n_components=1,
    )

    assert result.n_components == 1
    assert result.best_model.shape == spectrum.shape
    assert abs(result.parameters[1] - 0.5) < 0.25
    assert result.parameters[2] > 0


def test_private_adapter_preserves_legacy_return_shape_with_manual_peak():
    velocity = np.linspace(-5.0, 5.0, 41)
    spectrum = 0.8 * np.exp(-0.5 * ((velocity - 0.5) / 1.0) ** 2)
    spectrum_err = np.full_like(velocity, 0.05)

    adapter = _GaussianFitSpecAdapter(velocity, spectrum, spectrum_err)
    adapter.x_peak = [0.5]
    params, errors = adapter.fitting()

    assert params.shape == errors.shape
    assert params.size == 3
    assert abs(params[1] - 0.5) < 0.25
    assert np.all(params[0::3] >= 0)


def test_private_adapter_uses_gaussfitspec_automatic_selection():
    velocity = np.linspace(-8.0, 8.0, 81)
    spectrum = 0.45 * np.exp(-0.5 * ((velocity - 1.0) / 1.2) ** 2)
    spectrum_err = np.full_like(velocity, 0.03)

    adapter = _GaussianFitSpecAdapter(velocity, spectrum, spectrum_err)
    adapter.nGaussianMax = 4
    params, errors = adapter.fitting()

    assert params.shape == errors.shape
    assert params.size >= 3
    assert np.all(params[0::3] >= 0)
    assert adapter.last_result is not None
    assert adapter.last_result.n_components == params.size // 3


def test_private_adapter_prints_gaussfitspec_bic_iterations_for_auto_fit():
    velocity = np.linspace(-5.0, 5.0, 41)
    spectrum = 0.8 * np.exp(-0.5 * ((velocity - 0.5) / 1.0) ** 2)
    spectrum_err = np.full_like(velocity, 0.05)

    adapter = _GaussianFitSpecAdapter(velocity, spectrum, spectrum_err)
    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        adapter.fitting()

    output = stdout.getvalue()
    assert "BIC " in output
    assert "n=1" in output
    assert "final BIC=" in output


def test_private_adapter_manual_peak_does_not_run_auto_bic_iterations():
    velocity = np.linspace(-5.0, 5.0, 41)
    spectrum = 0.8 * np.exp(-0.5 * ((velocity - 0.5) / 1.0) ** 2)
    spectrum_err = np.full_like(velocity, 0.05)

    adapter = _GaussianFitSpecAdapter(velocity, spectrum, spectrum_err)
    adapter.x_peak = [0.5]
    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        adapter.fitting()

    assert stdout.getvalue() == ""
    assert adapter.last_result is not None
    assert adapter.last_result.n_components == 1


def test_private_adapter_manual_center_window_prevents_far_component_jump():
    velocity = np.linspace(-10.0, 10.0, 101)
    spectrum = 0.9 * np.exp(-0.5 * ((velocity - 5.0) / 1.0) ** 2)
    spectrum_err = np.full_like(velocity, 0.03)

    adapter = _GaussianFitSpecAdapter(velocity, spectrum, spectrum_err)
    adapter.x_peak = [0.0]
    adapter.initial_center_window = 1.0
    adapter.filter_components = True
    params, _ = adapter.fitting()

    assert abs(params[1]) <= 1.0 + 1.0e-6
