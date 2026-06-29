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


def run_r4_csv_fit(output_dir, *, name="r4-csv", renew=False):
    x, y, yerr, xemi, yemi, yemi_err = load_six_column_spectrum(
        ROOT / "examples" / "r4.txt",
        absorption_format="transmission",
    )
    fig, axes = create_legacy_axes(figsize=(12, 8), dpi=120)
    try:
        spec_fit = SpectraDecomposing(x, y, yerr, xemi, yemi, yemi_err)
        spec_fit.name = name
        spec_fit.v_shift = 4
        spec_fit.peak_abs = []
        spec_fit.peak_emi = [-250, -230]
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


def test_r4_fit_writes_expected_csv_outputs(tmp_path):
    result = run_r4_csv_fit(tmp_path)

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

    assert list(full["Name"]) == ["r4-csv"]
    assert {"NHI_c", "Sigma_NHIc", "NHI_w", "Sigma_NHIw", "f_c", "Tsky"}.issubset(full.columns)
    assert {"tau", "velocity_tau", "fwhm", "mean_Ts", "v_shift", "Order"}.issubset(cnm.columns)
    assert {"TB_WNM", "velocity_TB", "fwhm", "NHI_w", "F_value"}.issubset(wnm.columns)
    assert full.loc[0, "NHI_c"] > 0
    assert full.loc[0, "NHI_w"] > 0
    assert full.loc[0, "Tsky"] == 2.73
    assert cnm.shape[0] >= 1
    assert wnm.shape[0] >= 1
    assert_csv_has_no_array_strings(full_path)
    assert_csv_has_no_array_strings(cnm_path)
    assert_csv_has_no_array_strings(wnm_path)


def test_r4_fit_renew_replaces_existing_source_rows(tmp_path):
    run_r4_csv_fit(tmp_path, name="r4-redo", renew=False)
    run_r4_csv_fit(tmp_path, name="r4-redo", renew=True)

    full = pd.read_csv(tmp_path / "Fulldata.csv")
    cnm = pd.read_csv(tmp_path / "CNMonlydata.csv")
    wnm = pd.read_csv(tmp_path / "WNMonlydata.csv")

    assert list(full["Name"]) == ["r4-redo"]
    assert set(cnm["Name"]) == {"r4-redo"}
    assert set(wnm["Name"]) == {"r4-redo"}
    assert full.shape[0] == 1
    assert cnm.shape[0] == 1
    assert wnm.shape[0] == 2
