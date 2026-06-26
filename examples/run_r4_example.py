"""Run the legacy-style radiative-transfer fit on ``examples/r4.txt``."""

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

from Absorption_fitting import SpectraDecomposing
from Absorption_fitting.spectra_decomposing_io import load_six_column_spectrum
from Absorption_fitting.spectra_decomposing_plotting import create_legacy_axes


def main():
    """Fit the bundled example spectrum and save the diagnostic outputs."""
    x, y, yerr, xemi, yemi, yemi_err = load_six_column_spectrum(
        ROOT / "examples" / "r4.txt",
        absorption_format="transmission",
    )

    fig, axes = create_legacy_axes(figsize=(12, 8), dpi=300)
    spec_fit = SpectraDecomposing(x, y, yerr, xemi, yemi, yemi_err)
    spec_fit.name = "r4"
    spec_fit.v_shift = 4
    spec_fit.peak_abs = []
    spec_fit.peak_emi = [-250, -230]
    spec_fit.Tsmin = 10
    spec_fit.Tsky = 2.73
    spec_fit.fit_mode = "BIC"
    spec_fit.ax = axes
    spec_fit.savecsv = True
    spec_fit.renew = True
    spec_fit.datapath = str(ROOT / "examples" / "r4_csv_outputs")
    spec_fit.align_data = True
    spec_fit.bic_weight = 10
    spec_fit.fit_and_plot()

    output_path = ROOT / "examples" / "r4_fit.png"
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    return output_path


if __name__ == "__main__":
    main()
