Examples
========

The repository currently includes:

- ``examples/example_spec.txt`` as a real six-column absorption plus emission spectrum
- ``examples/run_example_spec.py`` to reproduce the legacy four-panel plot
- ``examples/example_spec_fit.png`` as the saved output from the packaged workflow
- ``examples/example_spec_csv_outputs/`` with example CSV products

Run the bundled example
-----------------------

.. code-block:: bash

   python examples/run_example_spec.py

This creates:

- ``examples/example_spec_fit.png``
- ``examples/example_spec_csv_outputs/Fulldata.csv``
- ``examples/example_spec_csv_outputs/CNMonlydata.csv``
- ``examples/example_spec_csv_outputs/WNMonlydata.csv``

Example plot
------------

.. image:: ../examples/example_spec_fit.png
   :alt: Four-panel example_spec absorption and emission fit
   :width: 100%

The upper two panels show the emission spectrum, best-fit model, and emission
residual. The lower two panels show the absorption spectrum in
``1 - exp(-tau)`` form, the absorption fit, and its residual.
