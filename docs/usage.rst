Usage
=====

The package exposes the radiative-transfer class and re-exports the
``gaussFitSpec`` Gaussian fitting API:

- ``SpectraDecomposing`` for combined absorption and emission decomposition
- ``fit_spectrum`` from ``gaussFitSpec`` for direct Gaussian component fitting

Basic imports:

.. code-block:: python

   from spec_rt import (
       SpectraDecomposing,
       create_legacy_axes,
       fit_spectrum,
       load_six_column_spectrum,
   )

Direct Gaussian fitting
-----------------------

Use ``fit_spectrum`` when you only need a Gaussian decomposition of one
one-dimensional spectrum:

.. code-block:: python

   result = fit_spectrum(velocity, spectrum, spectrum_err, method="bic")
   print(result.components)

Radiative-transfer fitting
--------------------------

Use ``SpectraDecomposing`` when you have matched absorption and emission
spectra:

.. code-block:: python

   x, y, yerr, xemi, yemi, yemi_err = load_six_column_spectrum(
       "examples/r4.txt",
       absorption_format="transmission",
   )

   fig, axes = create_legacy_axes()
   spec_fit = SpectraDecomposing(x, y, yerr, xemi, yemi, yemi_err)
   spec_fit.name = "r4"
   spec_fit.ax = axes
   spec_fit.align_data = True
   spec_fit.peak_abs = []
   spec_fit.peak_emi = [-250, -230]
   spec_fit.Tsmin = 10
   spec_fit.Tsky = 2.73
   spec_fit.fit_mode = "BIC"
   spec_fit.fit_and_plot()

Saving CSV outputs
------------------

Set ``savecsv=True`` and choose an output directory:

.. code-block:: python

   spec_fit.savecsv = True
   spec_fit.renew = True
   spec_fit.datapath = "examples/r4_csv_outputs"
   spec_fit.fit_and_plot()

``renew=True`` removes old rows for the same source name before appending new
results, which is useful when you redo a fit.
