Configuration
=============

``SpectraDecomposing`` keeps the original script-style configuration as
attributes. Set these before calling ``fit_and_plot()``.

Core options
------------

``name``
   Source name written into plots and CSV files.

``align_data``
   If ``True``, interpolate absorption and emission spectra onto a shared
   velocity grid before fitting.

``peak_abs``
   Optional absorption component centers. Leave as ``[]`` for automatic
   Gaussian selection.

``peak_emi``
   Optional emission component centers. Setting this manually can make the
   emission fit much faster.

``Tsmin``
   Lower bound for CNM spin temperature.

``Tsky``
   Background sky temperature. Use ``2.73`` for CMB-only, or add synchrotron
   emission if available.

``F``
   Foreground fraction values tested for WNM components. The default is
   ``[0, 0.5, 1]``.

Output options
--------------

``savecsv``
   If ``True``, write ``Fulldata.csv``, ``CNMonlydata.csv``, and
   ``WNMonlydata.csv``.

``datapath``
   Directory where CSV files are written.

``renew``
   If ``True``, remove old rows with the same ``name`` before writing new
   results. This is useful when redoing a fit.

Example
-------

.. code-block:: python

   spec_fit = SpectraDecomposing(x, y, yerr, xemi, yemi, yemi_err)
   spec_fit.name = "r4"
   spec_fit.v_shift = 4
   spec_fit.peak_abs = []
   spec_fit.peak_emi = [-250, -230]
   spec_fit.Tsmin = 10
   spec_fit.Tsky = 2.73
   spec_fit.F = [0, 0.5, 1]
   spec_fit.align_data = True
   spec_fit.savecsv = True
   spec_fit.renew = True
   spec_fit.datapath = "examples/r4_csv_outputs"
   spec_fit.fit_and_plot()
