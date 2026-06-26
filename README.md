# Absorption_fitting

`Absorption_fitting` packages the existing Gaussian absorption/emission
spectral fitting code as an installable Python project.

## Features

- Gaussian spectrum fitting through the external `gaussFitSpec` package
- Joint absorption/emission decomposition with `SpectraDecomposing`
- PyPI-ready `pyproject.toml` metadata
- Sphinx documentation scaffolding

## Installation

Install locally from the repository root:

```bash
pip install -e .[dev,docs]
```

Build distribution files for PyPI:

```bash
python -m build
```

## Quick Start

```python
from Absorption_fitting import (
    SpectraDecomposing,
    create_legacy_axes,
    fit_spectrum,
    load_six_column_spectrum,
)
```

Load the bundled six-column example and convert the absorption column from
``exp(-tau)`` to ``1 - exp(-tau)``:

```python
x, y, yerr, xemi, yemi, yemi_err = load_six_column_spectrum(
    "examples/r4.txt",
    absorption_format="transmission",
)
```

Create the legacy four-panel layout and run the radiative-transfer fit:

```python
fig, axes = create_legacy_axes()
spec_fit = SpectraDecomposing(x, y, yerr, xemi, yemi, yemi_err)
spec_fit.ax = axes
spec_fit.align_data = True
spec_fit.fit_and_plot()
```

## Repository Layout

```text
Absorption_fitting/
├── pyproject.toml
├── README.md
├── MANIFEST.in
├── docs/
├── src/
│   └── Absorption_fitting/
│       ├── __init__.py
│       ├── spectra_decomposing.py
│       ├── spectra_decomposing_io.py
│       ├── spectra_decomposing_plotting.py
│       └── spectra_decomposing_utils.py
└── tests/
```

## Before Publishing

- Replace the placeholder project URLs in `pyproject.toml`
- Add a `LICENSE` file once you choose the license you want
- Add more usage examples and validation tests for your data workflows
