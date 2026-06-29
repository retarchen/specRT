from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from spec_rt import (
    SpectrumFitResult,
    sd,
    SpectraDecomposing,
    create_legacy_axes,
    fit_spectrum,
    load_six_column_spectrum,
    validate_absorption_input,
)


def test_public_api_exports():
    assert sd is SpectraDecomposing
    assert callable(fit_spectrum)
    assert SpectrumFitResult is not None
    assert callable(load_six_column_spectrum)
    assert callable(validate_absorption_input)
    assert callable(create_legacy_axes)
