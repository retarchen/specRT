"""Plotting helpers for the radiative-transfer workflow."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

LINESTYLES = ["--", "dotted", "-.", "solid", "--", "dotted", "-.", "solid"]


def create_legacy_axes(*, figsize=(12, 8), dpi=300):
    """Create the four-panel subplot layout used by the original notebook."""
    fig = plt.figure(figsize=figsize, dpi=dpi)
    ax1_first = plt.subplot2grid((8, 2), (0, 0), rowspan=3, fig=fig)
    axes = [
        ax1_first,
        plt.subplot2grid((8, 2), (3, 0), rowspan=1, fig=fig, sharex=ax1_first),
        plt.subplot2grid((8, 2), (4, 0), rowspan=3, fig=fig, sharex=ax1_first),
        plt.subplot2grid((8, 2), (7, 0), fig=fig, sharex=ax1_first),
    ]
    return fig, axes


def plot_fit_panels(
    model,
    *,
    ax,
    x,
    y,
    yerr,
    xemi,
    yemi,
    yemi_err,
    name,
    popt_ori,
    popt,
    Ts,
    gausf,
    funT,
    mean_Ts,
    sigma_meanTsf,
    nwarm,
    v_shift,
    F_values,
):
    """Render the four-panel legacy diagnostic figure."""

    ncold = int(len(popt) / 3)
    ax[0].plot(xemi, yemi, label="GASKAP emission", linewidth=1.2, c="tab:blue", zorder=20)
    ax[0].plot(xemi, funT, label="Best fit", linewidth=3, alpha=0.9, c="tab:orange")
    for i in range(ncold):
        j = i * 3
        _popt = popt[j : j + 3].copy()
        _popt[1] = _popt[1] + v_shift[i]
        ax[0].plot(
            xemi,
            (1 - np.exp(-model.gaussian_func(xemi, *_popt))) * Ts[i],
            label="CNM,Ts=%.0f$\\pm$%.0f K" % (mean_Ts[i], sigma_meanTsf[i]),
            linewidth=1.8,
            linestyle=LINESTYLES[i],
            color="green",
        )

    for i in range(int(len(gausf) / 3)):
        j = i * 3
        _popt = gausf[j : j + 3]
        ax[0].plot(
            xemi,
            model.gaussian_func(xemi, *_popt),
            label="WNM,F=%.1f \n [%.2f,%.2f,%.2f]"
            % (F_values[i], _popt[0], _popt[1], 2.35482 * _popt[2]),
            linewidth=1.8,
            linestyle=LINESTYLES[i],
            color="gray",
        )

    ax[0].set_title(name)
    ax[0].set_ylabel(r"$T_B$ (K)")
    nco = 2 if nwarm > 4 else 1
    ax[0].legend(framealpha=0, fontsize="x-small", ncol=nco)
    plt.subplots_adjust(hspace=0)

    ax[1].plot(xemi, yemi - funT, linewidth=1.2, c="black")
    ax[1].fill_between(xemi, yemi_err, -yemi_err, alpha=0.2, facecolor="gray", edgecolor="gray")
    ax[1].set_ylabel("Residual")
    ax[1].set_xlabel("vlsr (km/s)")
    ax[1].plot(xemi, np.zeros_like(xemi), linewidth=1, c="black")
    plt.subplots_adjust(hspace=0)

    a = 1 - np.exp(-model.gaussian_func_multi(x, *popt_ori))
    ax[2].plot(x, y, label="GASKAP absorption", linewidth=1.2, c="tab:blue", zorder=20)
    ax[2].plot(x, a, label="Best fit", linewidth=3, alpha=0.9, c="tab:orange")
    for i in range(ncold):
        j = i * 3
        _popt = popt_ori[j : j + 3]
        ax[2].plot(
            x,
            1 - np.exp(-model.gaussian_func(x, *_popt)),
            label=r"$\tau$ Fitting parameters:" + "\n [%.2f,%.2f,%.2f]"
            % (_popt[0], _popt[1], 2.35482 * _popt[2]),
            linewidth=1.8,
            linestyle=LINESTYLES[i],
            c="green",
        )
    ax[2].set_ylabel(r"$1-e^{-\tau}$")
    ax[2].legend(framealpha=0, fontsize="small")
    plt.subplots_adjust(hspace=0)

    ax[3].plot(x, y - a, linewidth=1.2, c="black")
    ax[3].fill_between(x, yerr, -yerr, alpha=0.2, facecolor="gray", edgecolor="gray")
    ax[3].set_ylabel("Residual")
    ax[3].set_xlabel("vlsr (km/s)")
    ax[3].plot(x, np.zeros_like(x), linewidth=1, c="black")
    return ax
