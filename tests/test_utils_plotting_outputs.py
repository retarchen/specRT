from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from Absorption_fitting.spectra_decomposing_io import write_table_outputs
from Absorption_fitting.spectra_decomposing_plotting import create_legacy_axes
from Absorption_fitting.spectra_decomposing_utils import (
    align_spectra_grids,
    filter_positive_error_rows,
)


def assert_csv_has_no_array_strings(path):
    df = pd.read_csv(path, dtype=str)
    contains_bracket = df.apply(
        lambda column: column.str.contains(r"\[|\]", regex=True, na=False)
    ).any()
    assert not contains_bracket.any()


@dataclass
class OutputModel:
    datapath: str
    renew: bool = False
    Tsky: float = 2.73


def test_filter_positive_error_rows_drops_zero_negative_and_nan_errors():
    x = np.array([0.0, 1.0, 2.0, 3.0])
    y = np.array([10.0, 11.0, 12.0, 13.0])
    yerr = np.array([0.1, 0.0, -1.0, np.nan])

    filtered_x, filtered_y, filtered_yerr = filter_positive_error_rows(x, y, yerr)

    assert np.allclose(filtered_x, [0.0])
    assert np.allclose(filtered_y, [10.0])
    assert np.allclose(filtered_yerr, [0.1])


def test_align_spectra_grids_uses_overlap_and_shorter_length():
    x = np.array([0.0, 1.0, 2.0, 3.0])
    y = x**2
    yerr = np.full_like(x, 0.1)
    xemi = np.array([1.0, 2.0, 3.0])
    yemi = np.array([10.0, 20.0, 30.0])
    yemi_err = np.full_like(xemi, 0.5)

    aligned = align_spectra_grids(x, y, yerr, xemi, yemi, yemi_err)
    common_x, aligned_y, aligned_yerr, common_xemi, aligned_yemi, aligned_yemi_err = aligned

    assert np.allclose(common_x, [1.0, 2.0, 3.0])
    assert np.allclose(common_xemi, common_x)
    assert np.allclose(aligned_y, [1.0, 4.0, 9.0])
    assert np.allclose(aligned_yerr, [0.1, 0.1, 0.1])
    assert np.allclose(aligned_yemi, [10.0, 20.0, 30.0])
    assert np.allclose(aligned_yemi_err, [0.5, 0.5, 0.5])


def test_create_legacy_axes_returns_four_shared_axes():
    fig, axes = create_legacy_axes(figsize=(4, 3), dpi=80)

    try:
        assert len(axes) == 4
        assert all(axis.figure is fig for axis in axes)
        assert axes[1].get_shared_x_axes().joined(axes[0], axes[1])
        assert axes[2].get_shared_x_axes().joined(axes[0], axes[2])
        assert axes[3].get_shared_x_axes().joined(axes[0], axes[3])
    finally:
        plt.close(fig)


def test_write_table_outputs_creates_expected_csv_files(tmp_path):
    model = OutputModel(datapath=str(tmp_path), renew=False, Tsky=2.73)
    summary = write_table_outputs(
        model,
        name="case-a",
        popt=np.array([0.3, -10.0, 2.0]),
        pcov=np.array([0.01, 0.02, 0.03]),
        gausf=np.array([12.0, -8.0, 4.0]),
        funT=np.array([1.0, 2.0, 3.0]),
        xemi=np.array([-1.0, 0.0, 1.0]),
        Or=np.array([0]),
        fit_e=np.array([0.1, 0.2, 0.3]),
        mean_Ts=np.array([50.0]),
        sigma_meanTsf=np.array([5.0]),
        v_shift=np.array([0.2]),
        F_values=np.array([0.5]),
    )

    assert summary["NHI_c"] > 0
    assert (tmp_path / "Fulldata.csv").exists()
    assert (tmp_path / "CNMonlydata.csv").exists()
    assert (tmp_path / "WNMonlydata.csv").exists()
    assert not (tmp_path / "output.txt").exists()

    full = pd.read_csv(tmp_path / "Fulldata.csv")
    cnm = pd.read_csv(tmp_path / "CNMonlydata.csv")
    wnm = pd.read_csv(tmp_path / "WNMonlydata.csv")
    assert full.loc[0, "Name"] == "case-a"
    assert cnm.loc[0, "Order"] == 0
    assert wnm.loc[0, "F_value"] == 0.5
    assert_csv_has_no_array_strings(tmp_path / "Fulldata.csv")
    assert_csv_has_no_array_strings(tmp_path / "CNMonlydata.csv")
    assert_csv_has_no_array_strings(tmp_path / "WNMonlydata.csv")


def test_write_table_outputs_converts_array_like_values_to_scalars(tmp_path):
    model = OutputModel(datapath=str(tmp_path), renew=False, Tsky=2.73)
    write_table_outputs(
        model,
        name="array-like",
        popt=np.array([0.3, -10.0, 2.0]),
        pcov=np.array([0.01, 0.02, 0.03]),
        gausf=np.array([12.0, -8.0, 4.0]),
        funT=np.array([1.0, 2.0, 3.0]),
        xemi=np.array([-1.0, 0.0, 1.0]),
        Or=[np.array([0])],
        fit_e=np.array([0.1, 0.2, 0.3]),
        mean_Ts=[np.array([50.0])],
        sigma_meanTsf=[np.array([5.0])],
        v_shift=[np.array([0.2])],
        F_values=[np.array([0.5])],
    )

    assert_csv_has_no_array_strings(tmp_path / "Fulldata.csv")
    assert_csv_has_no_array_strings(tmp_path / "CNMonlydata.csv")
    assert_csv_has_no_array_strings(tmp_path / "WNMonlydata.csv")

    cnm = pd.read_csv(tmp_path / "CNMonlydata.csv")
    wnm = pd.read_csv(tmp_path / "WNMonlydata.csv")
    assert cnm.loc[0, "mean_Ts"] == 50.0
    assert cnm.loc[0, "sigma_mean_Ts"] == 5.0
    assert cnm.loc[0, "Order"] == 0.0
    assert wnm.loc[0, "F_value"] == 0.5


def test_write_table_outputs_renew_replaces_existing_named_rows(tmp_path):
    base_model = OutputModel(datapath=str(tmp_path), renew=False, Tsky=2.73)
    for name in ["case-a", "case-b"]:
        write_table_outputs(
            base_model,
            name=name,
            popt=np.array([0.3, -10.0, 2.0]),
            pcov=np.array([0.01, 0.02, 0.03]),
            gausf=np.array([12.0, -8.0, 4.0]),
            funT=np.array([1.0, 2.0, 3.0]),
            xemi=np.array([-1.0, 0.0, 1.0]),
            Or=np.array([0]),
            fit_e=np.array([0.1, 0.2, 0.3]),
            mean_Ts=np.array([50.0]),
            sigma_meanTsf=np.array([5.0]),
            v_shift=np.array([0.2]),
            F_values=np.array([0.5]),
        )

    renew_model = OutputModel(datapath=str(tmp_path), renew=True, Tsky=2.73)
    write_table_outputs(
        renew_model,
        name="case-a",
        popt=np.array([0.3, -10.0, 2.0]),
        pcov=np.array([0.01, 0.02, 0.03]),
        gausf=np.array([12.0, -8.0, 4.0]),
        funT=np.array([1.0, 2.0, 3.0]),
        xemi=np.array([-1.0, 0.0, 1.0]),
        Or=np.array([0]),
        fit_e=np.array([0.1, 0.2, 0.3]),
        mean_Ts=np.array([50.0]),
        sigma_meanTsf=np.array([5.0]),
        v_shift=np.array([0.2]),
        F_values=np.array([0.5]),
    )

    full = pd.read_csv(tmp_path / "Fulldata.csv")
    assert list(full["Name"]) == ["case-b", "case-a"]
