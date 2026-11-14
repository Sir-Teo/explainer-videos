import math

import numpy as np
import pytest
from scipy import stats

from explainer.psychology.psyche import vision as v


def test_frequency_of_seeing_is_a_poisson_tail_and_its_slope_depends_on_k_only():
    assert v.frequency_of_seeing(10, 1, 0.1) == pytest.approx(1 - math.exp(-1))
    assert v.frequency_of_seeing(60, 6, 0.1) == pytest.approx(stats.poisson.sf(5, 6.0))
    slopes = [v.fos_slope(k) for k in (1, 3, 6, 9)]
    assert all(b > a for a, b in zip(slopes, slopes[1:]))
    # the efficiency only shifts the curve along log intensity: the same slope at any efficiency
    q = np.geomspace(1, 1e4, 4001)
    for eff in (0.03, 0.3):
        p = v.frequency_of_seeing(q, 6, eff)
        lq = np.log10(q)
        i = np.argmin(np.abs(p - 0.5))
        assert np.gradient(p, lq)[i] == pytest.approx(v.fos_slope(6), rel=0.02)


def test_fit_fos_recovers_k_with_many_trials():
    q = np.geomspace(20, 400, 12)
    y = v.simulate_fos(6, 0.06, q, 2000, rng=np.random.default_rng(3))
    r = v.fit_fos(q, y, 2000)
    assert r["k"] == 6
    assert r["efficiency"] == pytest.approx(0.06, rel=0.1)


def test_optics_cutoff_nyquist_and_aliasing():
    assert v.cutoff_cpd(3.0, 555.0) == pytest.approx(3e-3 / 555e-9 * math.pi / 180)
    assert v.diffraction_mtf(0.0) == pytest.approx(1.0)
    assert v.diffraction_mtf(v.cutoff_cpd()) == pytest.approx(0.0, abs=1e-12)
    assert v.nyquist_cpd(0.5) == pytest.approx(60.0)
    assert v.alias_cpd(80.0, 120.0) == pytest.approx(40.0)
    assert v.alias_cpd(50.0, 120.0) == pytest.approx(50.0)


def test_gain_control_gives_webers_law_and_a_fixed_gain_saturates():
    b = np.logspace(1, 6, 6)
    ratio = v.increment_threshold(b) / b
    assert np.allclose(ratio, ratio[-1], rtol=0.05)
    assert np.isinf(v.increment_threshold(np.array([1e4]), adapt=False)[0])


def test_dog_is_band_pass_and_makes_mach_bands():
    r = v.dog_response(np.array([0.0, 0.1, 1.0]), 1.0, 3.0, 1.0)
    assert r[0] == pytest.approx(0.0) and r[1] > 0.3 and r[2] < 0.01
    m = v.mach_response(v.mach_profile())
    assert m[148] < m[100] and m[252] > m[300]  # a dark band at the dark corner, a bright one at the bright corner


def test_simple_cells_depend_on_phase_and_complex_cells_do_not():
    rf = v.gabor(64, 12)
    simple = [v.simple_cell(v.grating(64, 12, 0, p), rf) for p in np.linspace(0, 2 * np.pi, 9)]
    cplx = [v.complex_cell(v.grating(64, 12, 0, p), 64, 12) for p in np.linspace(0, 2 * np.pi, 9)]
    assert max(simple) > 5 * (min(simple) + 1e-9)
    assert np.std(cplx) / np.mean(cplx) < 0.01
    th = np.deg2rad(np.arange(-90, 91, 5))
    tc = v.orientation_tuning(th)
    assert th[np.argmax(tc)] == pytest.approx(0.0)
    assert 10 < np.rad2deg(v.half_width(th, tc)) < 40


def test_normalization_keeps_the_pattern_and_a_mask_divides():
    a, b = v.normalize([1, 0.5, 0.2], 0.01), v.normalize([2, 1, 0.4], 0.01)
    assert np.allclose(a / a.sum(), b / b.sum(), atol=1e-3)
    assert v.contrast_response(0.2, mask=0.3) < v.contrast_response(0.2)


def test_csf_shape_fit_and_chart():
    assert v.csf(4.0) == pytest.approx(200.0)
    hw = 2.75 / 2  # octaves from the peak to half height
    assert v.csf(4.0 * 2 ** hw) == pytest.approx(100.0)
    assert v.csf(0.1) == pytest.approx(200 * 10 ** -0.5)  # truncated
    f = np.array([0.5, 1, 2, 4, 8, 16, 32])
    r = v.fit_csf(f, v.csf(f, 150, 3, 3.5, 0.6))
    assert r["peak"] == pytest.approx(3, rel=1e-3) and r["bandwidth"] == pytest.approx(3.5, rel=1e-3)
    assert 40 < v.acuity_cpd() < 70
    cr = v.campbell_robson(pixels_per_degree=128.0)
    assert cr.shape == (256, 512) and np.abs(cr).max() <= 1.0
    assert np.abs(cr[0]).max() < np.abs(cr[-1]).max()  # faint at the top, strong at the bottom
    with pytest.raises(ValueError):
        v.campbell_robson(fmax=40.0, pixels_per_degree=32.0)


def test_colour_matching_reproduces_stiles_and_burch():
    cm = v.matching_functions(v.SB_PRIMARIES)
    idx = [int(np.where(v.WAVELENGTHS == w)[0][0]) for w in v.SB_WAVELENGTHS]
    mine, sb = cm[idx], v.SB_RGB
    for j in range(3):
        assert np.corrcoef(mine[:, j], sb[:, j])[0, 1] > 0.998
    # the red function is negative between the green and blue primaries: a match needs red added to the test
    assert v.match(v.monochromatic(500), v.SB_PRIMARIES)[0] < 0


def test_metamers_share_cone_excitations_but_not_spectra():
    y = v.surface(560, 80, base=0.3, height=0.6)
    m = v.null_space_metamer(y, 0.8)
    assert np.allclose(v.cone_excitations(y), v.cone_excitations(m), rtol=1e-9)
    assert np.abs(y - m).max() > 0.1 * y.max() and m.min() >= 0


def test_dichromat_keeps_neutral_and_anchor_and_merges_red_and_green():
    white = v.cone_excitations(np.ones(len(v.WAVELENGTHS)))
    assert np.allclose(v.dichromat(white, "L"), white)
    anchor = v.cone_excitations(v.monochromatic(575))
    assert np.allclose(v.dichromat(anchor, "M"), anchor)
    # a protanope loses L: a red and a green light that differ in L but agree in M and S become identical
    red = v.cone_excitations(v.monochromatic(620))
    shifted = red.copy()
    shifted[0] *= 2.0
    assert np.allclose(v.dichromat(red, "L"), v.dichromat(shifted, "L"))


def test_tables_peaks_and_srgb():
    assert v.WAVELENGTHS[np.argmax(v.SCOTOPIC)] in (505.0, 510.0)
    assert list(v.WAVELENGTHS[np.argmax(v.LMS, axis=0)]) == [570.0, 545.0, 445.0]
    rgb = v.srgb(v.to_xyz(v.monochromatic(450)))
    assert rgb[2] > rgb[0] and rgb[2] > rgb[1]
    assert v.chromaticity(v.to_xyz(np.ones(len(v.WAVELENGTHS)))) == pytest.approx([1 / 3, 1 / 3], abs=0.01)
