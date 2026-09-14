# Changelog

## 1.0.3

- Correct manual WNM center initialization and emission-grid noise indexing.
- Keep emission bounds finite for spectra with weak or missing detected peaks.
- Filter non-finite samples, sort velocity grids, and reject duplicate velocities.
- Use SciPy's trapezoid integration for compatibility with supported NumPy versions.

## 1.0.0

- Keep the existing Gaussian absorption and radiative-transfer emission method.
- Add overlap-aware CNM ordering to avoid equivalent factorial permutations.
- Add an analytic emission-model Jacobian for faster nonlinear fitting.
- Stop automatic WNM selection at the first non-improving BIC step.
- Cap automatic WNM selection at six components by default.
- Retain exhaustive CNM ordering and numerical derivatives as compatibility options.
