from __future__ import annotations

from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from spec_rt import SpectraDecomposing
from spec_rt.spectra_decomposing_io import load_six_column_spectrum
from spec_rt.spectra_decomposing_plotting import create_legacy_axes


def assert_csv_has_no_array_strings(path):
    df = pd.read_csv(path, dtype=str)
    contains_bracket = df.apply(
        lambda column: column.str.contains(r"\[|\]", regex=True, na=False)
    ).any()
    assert not contains_bracket.any()


def run_example_spec_csv_fit(output_dir, *, name="example-spec-csv", renew=False):
    x, y, yerr, xemi, yemi, yemi_err = load_six_column_spectrum(
        ROOT / "examples" / "example_spec.txt",
        absorption_format="one_minus_exp_tau",
    )
    fig, axes = create_legacy_axes(figsize=(12, 8), dpi=120)
    try:
        spec_fit = SpectraDecomposing(x, y, yerr, xemi, yemi, yemi_err)
        spec_fit.name = name
        spec_fit.v_shift = 4
        spec_fit.peak_abs = []
        spec_fit.peak_emi = []
        spec_fit.max_auto_warm_components = 1
        spec_fit.Tsmin = 10
        spec_fit.Tsky = 2.73
        spec_fit.fit_mode = "BIC"
        spec_fit.ax = axes
        spec_fit.savecsv = True
        spec_fit.renew = renew
        spec_fit.datapath = str(output_dir)
        spec_fit.align_data = True
        spec_fit.bic_weight = 10
        return spec_fit.fit_and_plot()
    finally:
        plt.close(fig)


def test_example_spec_fit_writes_expected_csv_outputs(tmp_path):
    result = run_example_spec_csv_fit(tmp_path)

    full_path = tmp_path / "Fulldata.csv"
    cnm_path = tmp_path / "CNMonlydata.csv"
    wnm_path = tmp_path / "WNMonlydata.csv"

    assert result is not None
    assert full_path.exists()
    assert cnm_path.exists()
    assert wnm_path.exists()
    assert not (tmp_path / "output.txt").exists()

    full = pd.read_csv(full_path)
    cnm = pd.read_csv(cnm_path)
    wnm = pd.read_csv(wnm_path)

    assert list(full["Name"]) == ["example-spec-csv"]
    assert {"NHI_c", "Sigma_NHIc", "NHI_w", "Sigma_NHIw", "f_c", "Tsky"}.issubset(full.columns)
    assert {"tau", "velocity_tau", "fwhm", "mean_Ts", "v_shift", "Order"}.issubset(cnm.columns)
    assert {"TB_WNM", "velocity_TB", "fwhm", "NHI_w", "F_value"}.issubset(wnm.columns)
    assert full.loc[0, "NHI_c"] > 0
    assert full.loc[0, "NHI_w"] > 0
    assert full.loc[0, "Tsky"] == 2.73
    assert cnm.shape[0] >= 1
    assert cnm["velocity_tau"].between(235.0, 250.0).all()
    assert wnm.shape[0] >= 1
    assert_csv_has_no_array_strings(full_path)
    assert_csv_has_no_array_strings(cnm_path)
    assert_csv_has_no_array_strings(wnm_path)


def test_example_spec_fit_renew_replaces_existing_source_rows(tmp_path):
    run_example_spec_csv_fit(tmp_path, name="example-spec-redo", renew=False)
    first_cnm_count = pd.read_csv(tmp_path / "CNMonlydata.csv").shape[0]
    first_wnm_count = pd.read_csv(tmp_path / "WNMonlydata.csv").shape[0]

    run_example_spec_csv_fit(tmp_path, name="example-spec-redo", renew=True)

    full = pd.read_csv(tmp_path / "Fulldata.csv")
    cnm = pd.read_csv(tmp_path / "CNMonlydata.csv")
    wnm = pd.read_csv(tmp_path / "WNMonlydata.csv")

    assert list(full["Name"]) == ["example-spec-redo"]
    assert set(cnm["Name"]) == {"example-spec-redo"}
    assert set(wnm["Name"]) == {"example-spec-redo"}
    assert full.shape[0] == 1
    assert cnm.shape[0] == first_cnm_count
    assert wnm.shape[0] == first_wnm_count
