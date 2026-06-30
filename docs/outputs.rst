Outputs
=======

When ``savecsv=True``, the fitter writes three CSV files.

``Fulldata.csv``
   One row per source with total CNM/WNM column density estimates, cold gas
   fraction, sky temperature, and fitted uncorrected HI column density.

``CNMonlydata.csv``
   One row per cold component with optical depth, velocity, FWHM, spin
   temperature, velocity shift, ordering, and CNM column density.

``WNMonlydata.csv``
   One row per warm component with brightness temperature, velocity, FWHM,
   WNM column density, and foreground fraction value.

Redoing a fit
-------------

Use ``renew=True`` when repeating a fit for the same source:

.. code-block:: python

   spec_fit.savecsv = True
   spec_fit.renew = True
   spec_fit.datapath = "examples/example_spec_csv_outputs"
   spec_fit.fit_and_plot()

This removes previous rows with the same ``Name`` from the three CSV files
before appending the new results. It prevents duplicated rows when tuning
``peak_abs``, ``peak_emi``, ``Tsmin``, or ``Tsky``.

The package no longer writes ``output.txt``.
