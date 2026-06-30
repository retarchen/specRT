"""Run the bundled example_spec.txt radiative-transfer fit."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from spec_rt import SpectraDecomposing
from spec_rt.spectra_decomposing_io import load_six_column_spectrum
from spec_rt.spectra_decomposing_plotting import create_legacy_axes


def main():
    """Fit the new six-column example spectrum and save plot/CSV outputs."""
    x, y, yerr, xemi, yemi, yemi_err = load_six_column_spectrum(
        ROOT / "examples" / "example_spec.txt",
        absorption_format="one_minus_exp_tau",
    )
    fig, axes = create_legacy_axes(figsize=(12, 8), dpi=300)

    spec_fit = SpectraDecomposing(x, y, yerr, xemi, yemi, yemi_err)
    spec_fit.name = "example_spec"
    spec_fit.v_shift = 4
    spec_fit.peak_abs = []
    spec_fit.peak_emi = []
    spec_fit.max_auto_warm_components = 1
    spec_fit.Tsmin = 3.8306300449371338
    spec_fit.Tsky = 3.8306300449371338
    spec_fit.fit_mode = "BIC"
    spec_fit.ax = axes
    spec_fit.savecsv = True
    spec_fit.renew = True
    spec_fit.datapath = str(ROOT / "examples" / "example_spec_csv_outputs")
    spec_fit.align_data = True
    spec_fit.bic_weight = 10

    result = spec_fit.fit_and_plot()
    output = ROOT / "examples" / "example_spec_fit.png"
    fig.savefig(output, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved plot to {output}")
    print(f"Saved CSV outputs to {spec_fit.datapath}")
    return result


if __name__ == "__main__":
    main()
