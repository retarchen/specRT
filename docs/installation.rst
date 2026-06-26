Installation
============

Clone the repository and install the package in editable mode:

.. code-block:: bash

   pip install -e .[dev,docs]

The package depends on ``gaussFitSpec`` for direct Gaussian fitting. If you are
developing both packages locally, install ``GaussianFitSpectra`` first:

.. code-block:: bash

   cd ../GaussianFitSpectra
   pip install -e .
   cd ../Absorption_fitting
   pip install -e .[dev,docs]

To build wheels and source distributions for PyPI:

.. code-block:: bash

   python -m build

To check the distributions before upload:

.. code-block:: bash

   python -m twine check dist/*
