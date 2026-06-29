Input Format
============

The bundled ``examples/r4.txt`` file uses six columns:

1. absorption velocity
2. absorption spectrum
3. absorption spectrum error
4. emission velocity
5. emission spectrum
6. emission spectrum error

In the original notebook workflow the second column is stored as
``exp(-tau)`` and is converted before fitting:

.. code-block:: python

   from spec_rt import load_six_column_spectrum

   x, y, yerr, xemi, yemi, yemi_err = load_six_column_spectrum(
       "examples/r4.txt",
       absorption_format="transmission",
   )

After loading, ``y`` is guaranteed to be in the expected ``1 - exp(-tau)``
form, and the helper also drops non-finite emission rows.

Use :func:`spec_rt.validate_absorption_input` to confirm that the
absorption baseline remains close to zero before fitting.

Common checks
-------------

- The absorption array passed to ``SpectraDecomposing`` must already be
  ``1 - exp(-tau)``.
- The absorption baseline should be close to zero outside the line.
- Error columns must be positive; rows with non-positive errors are dropped
  before fitting.
- Emission rows with non-finite velocity, intensity, or error values are
  dropped by ``load_six_column_spectrum``.

If your raw absorption file stores transmission as ``exp(-tau)``, use:

.. code-block:: python

   load_six_column_spectrum("examples/r4.txt", absorption_format="transmission")

If your file already stores ``1 - exp(-tau)``, use:

.. code-block:: python

   load_six_column_spectrum("my_file.txt", absorption_format="one_minus_exp_tau")
