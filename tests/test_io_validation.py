from __future__ import annotations

from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from spec_rt.spectra_decomposing_io import (
    load_six_column_spectrum,
    validate_absorption_input,
)


def assert_raises(expected_exception, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except expected_exception as exc:
        return exc
    raise AssertionError(f"Expected {expected_exception.__name__} to be raised.")


def test_loader_rejects_non_six_column_table(tmp_path):
    path = tmp_path / "bad_columns.txt"
    np.savetxt(path, np.ones((3, 5)))

    exc = assert_raises(ValueError, load_six_column_spectrum, path)

    assert "six columns" in str(exc)


def test_loader_rejects_unknown_absorption_format(tmp_path):
    path = tmp_path / "six_columns.txt"
    np.savetxt(path, np.ones((3, 6)))

    exc = assert_raises(ValueError, load_six_column_spectrum, path, absorption_format="tau")

    assert "absorption_format" in str(exc)


def test_loader_transmission_conversion_and_emission_nan_drop(tmp_path):
    path = tmp_path / "sample.txt"
    data = np.array(
        [
            [-2.0, 0.95, 0.1, -2.0, 8.0, 0.5],
            [-1.0, 0.90, 0.1, np.nan, np.nan, np.nan],
            [0.0, 0.80, 0.1, 0.0, 10.0, 0.6],
        ]
    )
    np.savetxt(path, data)

    x, y, yerr, xemi, yemi, yemi_err = load_six_column_spectrum(path)

    assert np.allclose(x, [-2.0, -1.0, 0.0])
    assert np.allclose(y, [0.05, 0.10, 0.20])
    assert np.allclose(yerr, [0.1, 0.1, 0.1])
    assert np.allclose(xemi, [-2.0, 0.0])
    assert np.allclose(yemi, [8.0, 10.0])
    assert np.allclose(yemi_err, [0.5, 0.6])


def test_loader_keeps_one_minus_exp_tau_format(tmp_path):
    path = tmp_path / "sample.txt"
    data = np.array(
        [
            [-2.0, 0.05, 0.1, -2.0, 8.0, 0.5],
            [-1.0, 0.10, 0.1, -1.0, 9.0, 0.5],
            [0.0, 0.20, 0.1, 0.0, 10.0, 0.6],
        ]
    )
    np.savetxt(path, data)

    _, y, _, _, _, _ = load_six_column_spectrum(path, absorption_format="one_minus_exp_tau")

    assert np.allclose(y, [0.05, 0.10, 0.20])


def test_validate_absorption_input_accepts_zero_baseline():
    y = np.zeros(20)
    y[9:12] = [0.15, 0.2, 0.15]
    yerr = np.full_like(y, 0.05)

    stats = validate_absorption_input(y, yerr, edge_fraction=0.2)

    assert stats["noise_level"] == 0.05
    assert abs(stats["baseline_mean"]) < 0.05


def test_validate_absorption_input_rejects_shape_mismatch():
    exc = assert_raises(
        ValueError,
        validate_absorption_input,
        np.array([0.0, 0.1]),
        np.array([0.1]),
    )

    assert "equal length" in str(exc)


def test_validate_absorption_input_rejects_offset_baseline():
    y = np.full(20, 0.5)
    yerr = np.full(20, 0.01)

    exc = assert_raises(ValueError, validate_absorption_input, y, yerr, sigma_limit=2.0)

    assert "baseline" in str(exc)


def test_validate_absorption_input_rejects_out_of_range_absorption():
    y = np.array([0.0, 0.0, 1.6, 0.0, 0.0])
    yerr = np.full_like(y, 0.1)

    exc = assert_raises(ValueError, validate_absorption_input, y, yerr)

    assert "expected" in str(exc)
