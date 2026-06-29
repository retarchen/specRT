from __future__ import annotations

from pathlib import Path
import sys

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
