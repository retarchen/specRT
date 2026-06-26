Performance
===========

The emission fit can become slow when the absorption fit contains many CNM
components. The expensive part is testing possible CNM foreground/background
orders and WNM foreground fractions.

For ``ncold`` cold components and ``nwarm`` warm components, the number of
candidate nonlinear emission fits can scale roughly as:

.. code-block:: text

   ncold! * len(F) ** nwarm

Practical speed tips
--------------------

- Set ``peak_emi`` manually when you know the likely emission component
  centers. This avoids a larger automatic search.
- Reduce ``F`` during exploration. For example, use ``spec_fit.F = [0.5]`` for
  a fast first pass, then restore ``[0, 0.5, 1]`` for a final run.
- Limit absorption components by setting ``peak_abs`` manually or using
  ``num_cold`` when the automatic fit over-splits noisy absorption spectra.
- Keep ``align_data=True`` when absorption and emission velocity grids differ.

Example fast first pass
-----------------------

.. code-block:: python

   spec_fit.peak_emi = [-250, -230]
   spec_fit.F = [0.5]
   spec_fit.num_cold = 5
   spec_fit.fit_and_plot()

After the fit is stable, rerun with the fuller configuration if needed:

.. code-block:: python

   spec_fit.F = [0, 0.5, 1]
   spec_fit.num_cold = 0
   spec_fit.renew = True
   spec_fit.fit_and_plot()
