"""The bootstrap resampler copies tokens into resample slots; the kernel sum integrates to one."""

import numpy as np

from explainer.stats import BootstrapResampler, KernelSum, axes


def test_resampler():
    b = BootstrapResampler(list(range(1, 6)), width=4)
    anim = b.resample([0, 0, 2, 4, 4])
    assert len(b.copies) == 5
    assert np.allclose(b.copies[1].get_center(), b.bottom[1])
    A = axes([0, 1], [0, 1])
    d1, d2 = b.drop(A.ax, 0.5, 0.1), b.drop(A.ax, 0.5, 0.1)
    assert d2.get_y() > d1.get_y()
    del anim


def test_kernel_sum():
    A = axes([-4, 4], [0, 1])
    k = KernelSum(A.ax, [0.0, 1.0, -1.0], 0.5, grid=np.linspace(-4, 4, 801))
    assert np.trapezoid(k.values, np.linspace(-4, 4, 801)) == np.float64(np.trapezoid(k.values, np.linspace(-4, 4, 801)))
    assert abs(np.trapezoid(k.values, np.linspace(-4, 4, 801)) - 1) < 1e-3
    assert len(k.bumps) == 3
