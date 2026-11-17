"""Psyche's vision: from quanta to the code the eye sends the brain.

Each stage of early vision can be written as a small piece of mathematics, and this module writes them down:

* **quanta**: a flash delivers a Poisson number of absorptions; the observer sees it when at least ``k`` arrive.
  The frequency-of-seeing curve's steepness on a log axis depends on ``k`` alone (Hecht, Shlaer and Pirenne 1942),
  so ``k`` can be read off without knowing how many quanta were lost on the way in.
* **optics and sampling**: the diffraction-limited modulation transfer function of a round pupil, a Gaussian blur
  for the eye's aberrations, and the cone mosaic's Nyquist limit, with aliasing above it.
* **adaptation**: a saturating response (Naka-Rushton) whose half-saturation follows the background, which turns
  a limited response range into Weber's law over many log units.
* **the retina**: difference-of-Gaussians receptive fields (Rodieck 1965), their band-pass frequency response, and
  Mach bands computed from the filter.
* **cortex**: Gabor receptive fields, orientation tuning, simple cells (half-rectified) and complex cells (the
  energy model, a quadrature pair), and divisive normalization (Heeger 1992).
* **the contrast sensitivity function**: a truncated log-parabola (the form used by Watson and Ahumada and by
  Lesmes et al. 2010), its fit, the Campbell-Robson chart, and an image filtered by a CSF.
* **colour**: spectra to cone excitations with Stockman and Sharpe's fundamentals; matching with three primaries
  as a 3-by-3 linear solve; colour-matching functions derived for any primaries and checked against Stiles and
  Burch's 1955 measurements; metamers built from the null space; CIE 1931 chromaticities and sRGB for display;
  opponent channels; dichromacy as a lost dimension; von Kries constancy and two readings of one image.

Spectra are sampled every 5 nm.  The tables are in :mod:`explainer.psychology.archive` (registered in
``archive/SOURCES.md``).
"""

from __future__ import annotations

import math

import numpy as np
from scipy import optimize, special, stats

from explainer.psychology.archive import _colour_tables as _T

# =============================================================================================== quanta
def frequency_of_seeing(quanta, k: int, efficiency: float = 1.0, dark: float = 0.0):
    """P(seen) for a flash of mean ``quanta`` at the cornea: absorptions ~ Poisson(efficiency * quanta + dark), and
    the flash is seen when at least ``k`` occur."""
    lam = efficiency * np.asarray(quanta, float) + dark
    return stats.poisson.sf(k - 1, lam)


def fos_slope(k: int, p: float = 0.5) -> float:
    """Slope of P(seen) against log10(mean absorptions) at the point where P = ``p``: a function of ``k`` only."""
    lam = float(stats.gamma.ppf(p, k))  # P(N >= k) = P(Gamma(k, 1) <= lam)
    return float(stats.poisson.pmf(k - 1, lam) * lam * math.log(10))


def simulate_fos(k: int, efficiency: float, quanta, trials: int, dark: float = 0.0, rng=None) -> np.ndarray:
    """Counts of 'seen' at each mean intensity, ``trials`` flashes each."""
    rng = rng or np.random.default_rng(0)
    p = frequency_of_seeing(quanta, k, efficiency, dark)
    return rng.binomial(trials, p)


def fit_fos(quanta, seen, trials, ks=range(1, 21), dark: float = 0.0) -> dict:
    """Maximum-likelihood fit of ``k`` (integer) and ``efficiency`` to frequency-of-seeing counts.  Returns the best
    ``k``, its ``efficiency``, and the profile log-likelihood over ``ks``."""
    q = np.asarray(quanta, float)
    n = np.broadcast_to(np.asarray(trials, float), q.shape)
    y = np.asarray(seen, float)
    prof = {}
    best = None
    for k in ks:
        def nll(loga):
            p = np.clip(frequency_of_seeing(q, k, math.exp(loga), dark), 1e-12, 1 - 1e-12)
            return -float(np.sum(y * np.log(p) + (n - y) * np.log(1 - p)))
        r = optimize.minimize_scalar(nll, bounds=(-12, 3), method="bounded")
        prof[k] = -r.fun
        if best is None or -r.fun > best[2]:
            best = (k, math.exp(r.x), -r.fun)
    return {"k": best[0], "efficiency": best[1], "loglik": best[2], "profile": prof}


# ================================================================================== optics and sampling
def cutoff_cpd(pupil_mm: float = 3.0, wavelength_nm: float = 555.0) -> float:
    """The diffraction cutoff of a round pupil, in cycles per degree: D / lambda per radian."""
    return pupil_mm * 1e-3 / (wavelength_nm * 1e-9) * math.pi / 180.0


def diffraction_mtf(f_cpd, pupil_mm: float = 3.0, wavelength_nm: float = 555.0):
    """Incoherent MTF of an aberration-free round pupil: (2/pi)(acos s - s sqrt(1 - s^2)), s = f / cutoff."""
    s = np.clip(np.asarray(f_cpd, float) / cutoff_cpd(pupil_mm, wavelength_nm), 0, 1)
    return (2 / np.pi) * (np.arccos(s) - s * np.sqrt(1 - s * s))


def eye_mtf(f_cpd, pupil_mm: float = 3.0, wavelength_nm: float = 555.0, blur_arcmin: float = 0.5):
    """Diffraction times a Gaussian blur of standard deviation ``blur_arcmin`` (a stand-in for the eye's
    aberrations; illustrative, not fitted)."""
    sig_deg = blur_arcmin / 60.0
    f = np.asarray(f_cpd, float)
    return diffraction_mtf(f, pupil_mm, wavelength_nm) * np.exp(-2 * np.pi ** 2 * sig_deg ** 2 * f ** 2)


def line_spread(x_arcmin, pupil_mm: float = 3.0, wavelength_nm: float = 555.0, blur_arcmin: float = 0.5):
    """The line-spread function: the inverse cosine transform of the MTF, normalized to peak 1."""
    x = np.asarray(x_arcmin, float) / 60.0
    f = np.linspace(0, cutoff_cpd(pupil_mm, wavelength_nm), 2000)
    m = eye_mtf(f, pupil_mm, wavelength_nm, blur_arcmin)
    out = np.trapezoid(m[None, :] * np.cos(2 * np.pi * f[None, :] * x[:, None]), f, axis=1)
    return out / out.max()


def nyquist_cpd(spacing_arcmin: float = 0.5) -> float:
    """The highest grating a row of receptors ``spacing_arcmin`` apart can represent: one cycle per two cones."""
    return 60.0 / (2.0 * spacing_arcmin)


def alias_cpd(f_cpd, sampling_cpd: float):
    """The frequency a grating of ``f_cpd`` appears at after sampling at ``sampling_cpd`` per degree."""
    f = np.asarray(f_cpd, float)
    return np.abs(f - sampling_cpd * np.round(f / sampling_cpd))


# =========================================================================================== adaptation
def naka_rushton(intensity, sigma, n: float = 1.0, rmax: float = 1.0):
    """R = rmax I^n / (I^n + sigma^n)."""
    i = np.asarray(intensity, float)
    return rmax * i ** n / (i ** n + np.asarray(sigma, float) ** n)


def increment_threshold(background, sigma0: float = 1.0, adapt: bool = True, n: float = 1.0, delta: float = 0.01):
    """Smallest increment that raises the response by ``delta`` at a steady ``background``.  With ``adapt`` the
    half-saturation is sigma0 + background (gain control); without it, sigma0 fixed, and the response saturates."""
    b = np.asarray(background, float)
    sig = sigma0 + b if adapt else np.full_like(b, sigma0)
    r0 = naka_rushton(b, sig, n)
    target = r0 + delta
    with np.errstate(divide="ignore", invalid="ignore"):
        ok = target < 1.0
        # invert R = I^n / (I^n + s^n) for I: I = s (R / (1 - R))^(1/n)
        i1 = np.where(ok, sig * (np.clip(target, 0, 1 - 1e-15) / (1 - np.clip(target, 0, 1 - 1e-15))) ** (1 / n), np.inf)
    return i1 - b


# ============================================================================================ the retina
def dog_profile(x, centre: float = 1.0, surround: float = 3.0, balance: float = 1.0):
    """A one-dimensional difference of Gaussians, each of unit area; ``balance`` scales the surround."""
    x = np.asarray(x, float)
    g = lambda s: np.exp(-x ** 2 / (2 * s * s)) / (s * math.sqrt(2 * math.pi))  # noqa: E731
    return g(centre) - balance * g(surround)


def dog_response(f, centre: float = 1.0, surround: float = 3.0, balance: float = 1.0):
    """The frequency response of :func:`dog_profile` (cycles per unit of x): band-pass when ``balance`` is near 1."""
    f = np.asarray(f, float)
    return np.exp(-2 * np.pi ** 2 * centre ** 2 * f ** 2) - balance * np.exp(-2 * np.pi ** 2 * surround ** 2 * f ** 2)


def filter_1d(signal, kernel):
    """Same-length convolution with edge padding."""
    s = np.asarray(signal, float)
    h = len(kernel) // 2
    pad = np.concatenate([np.full(h, s[0]), s, np.full(h, s[-1])])
    return np.convolve(pad, kernel, mode="same")[h:h + len(s)]


def mach_profile(n: int = 400, ramp=(150, 250), low: float = 0.2, high: float = 0.8) -> np.ndarray:
    """A luminance plateau, a ramp, a plateau: the stimulus of Mach bands."""
    x = np.arange(n, dtype=float)
    a, b = ramp
    return np.where(x < a, low, np.where(x > b, high, low + (high - low) * (x - a) / (b - a)))


def mach_response(profile, centre: float = 3.0, surround: float = 9.0, balance: float = 0.9) -> np.ndarray:
    """Luminance passed through a DoG: overshoots at the ramp's two corners (the bands), flat elsewhere."""
    x = np.arange(-4 * surround, 4 * surround + 1)
    return filter_1d(profile, dog_profile(x, centre, surround, balance))


def dog_image(image, centre: float, surround: float, balance: float = 1.0):
    """A two-dimensional DoG applied by FFT (periodic edges)."""
    img = np.asarray(image, float)
    fy = np.fft.fftfreq(img.shape[0])[:, None]
    fx = np.fft.fftfreq(img.shape[1])[None, :]
    f2 = fx ** 2 + fy ** 2
    h = np.exp(-2 * np.pi ** 2 * centre ** 2 * f2) - balance * np.exp(-2 * np.pi ** 2 * surround ** 2 * f2)
    return np.real(np.fft.ifft2(np.fft.fft2(img) * h))


# ================================================================================================ cortex
def grating(size: int, wavelength: float, theta: float = 0.0, phase: float = 0.0, contrast: float = 1.0):
    """A sinusoidal grating, mean 0, on a ``size`` x ``size`` grid; ``theta`` in radians (0: vertical bars)."""
    y, x = np.mgrid[:size, :size] - (size - 1) / 2
    u = x * math.cos(theta) + y * math.sin(theta)
    return contrast * np.cos(2 * np.pi * u / wavelength + phase)


def gabor(size: int, wavelength: float, theta: float = 0.0, phase: float = 0.0, sigma: float | None = None):
    """A Gabor receptive field: a grating under a Gaussian envelope (sigma defaults to half a wavelength), mean
    removed and scaled to unit norm."""
    sigma = sigma or 0.5 * wavelength
    y, x = np.mgrid[:size, :size] - (size - 1) / 2
    env = np.exp(-(x * x + y * y) / (2 * sigma * sigma))
    g = env * grating(size, wavelength, theta, phase)
    g = g - env * (g.sum() / env.sum())
    return g / np.linalg.norm(g)


def simple_cell(image, rf) -> float:
    """A linear receptive field followed by half-wave rectification."""
    return max(0.0, float(np.sum(image * rf)))


def complex_cell(image, size: int, wavelength: float, theta: float = 0.0, sigma: float | None = None) -> float:
    """The energy model: the summed squares of a quadrature pair (even and odd Gabors), then a square root."""
    even = float(np.sum(image * gabor(size, wavelength, theta, 0.0, sigma)))
    odd = float(np.sum(image * gabor(size, wavelength, theta, np.pi / 2, sigma)))
    return math.hypot(even, odd)


def orientation_tuning(thetas, size: int = 64, wavelength: float = 12.0, preferred: float = 0.0,
                       sigma: float | None = None) -> np.ndarray:
    """A complex cell's response to full-field gratings at each orientation (its tuning curve)."""
    return np.array([complex_cell(grating(size, wavelength, t), size, wavelength, preferred, sigma) for t in thetas])


def half_width(thetas, responses) -> float:
    """Half-width at half-height of a tuning curve, in the units of ``thetas`` (linear interpolation)."""
    t = np.asarray(thetas, float)
    r = np.asarray(responses, float)
    i = int(np.argmax(r))
    half = r[i] / 2
    j = i
    while j + 1 < len(r) and r[j + 1] > half:
        j += 1
    if j + 1 >= len(r):
        return float("nan")
    frac = (r[j] - half) / (r[j] - r[j + 1])
    return float(t[j] + frac * (t[j + 1] - t[j]) - t[i])


def normalize(drive, sigma: float = 0.1, n: float = 2.0, weights=None) -> np.ndarray:
    """Divisive normalization (Heeger 1992): R_i = d_i^n / (sigma^n + sum_j w_j d_j^n); weights default to all 1."""
    d = np.maximum(np.asarray(drive, float), 0.0) ** n
    w = np.ones_like(d) if weights is None else np.asarray(weights, float)
    return d / (sigma ** n + np.sum(w * d))


def contrast_response(contrast, c50: float = 0.2, n: float = 2.0, rmax: float = 1.0, mask: float = 0.0):
    """A V1 contrast-response function with an optional orthogonal mask in the normalization pool:
    R = rmax c^n / (c50^n + c^n + mask^n).  The mask drives nothing itself but divides the response."""
    c = np.asarray(contrast, float)
    return rmax * c ** n / (c50 ** n + c ** n + mask ** n)


# ======================================================================= the contrast sensitivity function
def csf(f_cpd, gain: float = 200.0, peak: float = 4.0, bandwidth: float = 2.75, truncation: float = 0.5):
    """A truncated log-parabola, the shape Lesmes et al. (2010) fit with four parameters: sensitivity ``gain`` at
    the ``peak`` frequency, falling by half ``bandwidth`` / 2 octaves either side (``bandwidth`` is the full width at
    half height, in octaves), with the low-frequency side held at most ``truncation`` log10 units below the peak."""
    f = np.asarray(f_cpd, float)
    half = bandwidth * math.log10(2.0) / 2.0  # half-width at half height, in log10 units of frequency
    top = math.log10(gain)
    logs = top - math.log10(2.0) * ((np.log10(f) - math.log10(peak)) / half) ** 2
    logs = np.where((f < peak) & (logs < top - truncation), top - truncation, logs)
    return 10 ** logs


def fit_csf(f_cpd, sensitivity, start=(100.0, 3.0, 3.0, 0.5)) -> dict:
    """Least squares in log sensitivity for the four parameters of :func:`csf`."""
    f = np.asarray(f_cpd, float)
    y = np.log10(np.asarray(sensitivity, float))

    def resid(p):
        g, pk, bw, tr = p
        return np.log10(csf(f, 10 ** g, 10 ** pk, 10 ** bw, abs(tr))) - y

    r = optimize.least_squares(resid, [math.log10(start[0]), math.log10(start[1]), math.log10(start[2]), start[3]])
    g, pk, bw, tr = r.x
    return {"gain": 10 ** g, "peak": 10 ** pk, "bandwidth": 10 ** bw, "truncation": abs(tr),
            "rms": float(np.sqrt(np.mean(r.fun ** 2)))}


def acuity_cpd(gain: float = 200.0, peak: float = 4.0, bandwidth: float = 2.75) -> float:
    """Where the CSF falls to 1 (full contrast just visible): the grating acuity the curve implies."""
    root = optimize.brentq(lambda lf: math.log10(csf(10 ** lf, gain, peak, bandwidth, 9.0)), math.log10(peak), 4.0)
    return float(10 ** root)


def campbell_robson(width: int = 512, height: int = 256, fmin: float = 0.5, fmax: float = 40.0, cmin: float = 0.002,
                    cmax: float = 1.0, pixels_per_degree: float = 128.0) -> np.ndarray:
    """The Campbell-Robson chart: frequency rises logarithmically left to right, contrast falls logarithmically
    bottom to top (row 0 is the top, as in an image).  Values in [-1, 1] around a mean of 0; frequencies in cycles
    per degree at the stated scale, which must keep ``fmax`` below half a cycle per pixel."""
    if fmax / pixels_per_degree >= 0.5:
        raise ValueError("fmax is above the pixel grid's Nyquist limit: raise pixels_per_degree")
    x = np.arange(width) / pixels_per_degree
    lf = np.linspace(math.log(fmin), math.log(fmax), width)
    # phase = integral of 2 pi f(x) dx keeps the bars continuous
    f = np.exp(lf)
    phase = 2 * np.pi * np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(x))])
    c = np.exp(np.linspace(math.log(cmin), math.log(cmax), height))[:, None]  # row 0, the top: the faintest
    return c * np.sin(phase)[None, :]


def csf_filter(image, pixels_per_degree: float, **csf_params) -> np.ndarray:
    """Weight each spatial frequency of ``image`` (mean removed) by the CSF relative to its peak: an approximation to
    what survives at threshold, used to show what an observer at that distance can and cannot see."""
    img = np.asarray(image, float)
    m = img.mean()
    fy = np.fft.fftfreq(img.shape[0])[:, None] * pixels_per_degree
    fx = np.fft.fftfreq(img.shape[1])[None, :] * pixels_per_degree
    f = np.sqrt(fx ** 2 + fy ** 2)
    f[0, 0] = 1e-6
    s = csf(f, **csf_params)
    w = s / s.max()
    w[0, 0] = 1.0
    return m + np.real(np.fft.ifft2(np.fft.fft2(img - m) * w))


# ================================================================================================ colour
def _table(rows, lo: int, hi: int) -> tuple[np.ndarray, np.ndarray]:
    a = np.array(rows, float)
    keep = (a[:, 0] >= lo) & (a[:, 0] <= hi)
    return a[keep, 0], a[keep, 1:]


WAVELENGTHS = np.arange(390, 781, 5, dtype=float)  # the common grid


def _on_grid(rows) -> np.ndarray:
    a = np.array(rows, float)
    return np.column_stack([np.interp(WAVELENGTHS, a[:, 0], a[:, j], left=0.0, right=0.0) for j in range(1, a.shape[1])])


LMS = _on_grid(_T.STOCKMAN_SHARPE_2000_LMS)  # 79 x 3, each peak 1
XYZ = _on_grid(_T.CIE_1931_XYZ)  # 79 x 3
SCOTOPIC = _on_grid(_T.CIE_1951_SCOTOPIC)[:, 0]
SB_WAVELENGTHS, SB_RGB = _table(_T.STILES_BURCH_1955_RGB, 390, 730)
SB_PRIMARIES = (645.2, 526.3, 444.4)


def monochromatic(nm: float, width: float = 0.0) -> np.ndarray:
    """A spectrum on the grid: one sample at ``nm`` (interpolated between neighbours), or a Gaussian of s.d.
    ``width`` nm, with unit total power."""
    if width > 0:
        s = np.exp(-0.5 * ((WAVELENGTHS - nm) / width) ** 2)
    else:
        s = np.maximum(0.0, 1 - np.abs(WAVELENGTHS - nm) / 5.0)
    return s / s.sum()


def cone_excitations(spectrum) -> np.ndarray:
    """L, M and S excitations of a spectrum (or of each row of an array of spectra): a 3-by-N matrix product."""
    return np.asarray(spectrum, float) @ LMS


def to_xyz(spectrum) -> np.ndarray:
    return np.asarray(spectrum, float) @ XYZ


def chromaticity(xyz) -> np.ndarray:
    v = np.asarray(xyz, float)
    s = v.sum(axis=-1, keepdims=True)
    return v[..., :2] / s


def spectral_locus(lo: float = 390, hi: float = 700) -> np.ndarray:
    keep = (WAVELENGTHS >= lo) & (WAVELENGTHS <= hi)
    return chromaticity(XYZ[keep])


_XYZ_TO_SRGB = np.array([[3.2406, -1.5372, -0.4986], [-0.9689, 1.8758, 0.0415], [0.0557, -0.2040, 1.0570]])


def srgb(xyz, scale: float | None = None) -> np.ndarray:
    """XYZ to gamma-encoded sRGB in [0, 1] (clipped), for display.  ``scale`` divides XYZ first (default: so that
    the largest linear channel is 1)."""
    lin = np.asarray(xyz, float) @ _XYZ_TO_SRGB.T
    if scale is None:
        scale = max(float(np.max(lin)), 1e-12)
    lin = np.clip(lin / scale, 0, 1)
    return np.where(lin <= 0.0031308, 12.92 * lin, 1.055 * lin ** (1 / 2.4) - 0.055)


def primaries_matrix(primaries) -> np.ndarray:
    """Columns: the cone excitations of each primary (monochromatic lights at the given wavelengths, or spectra)."""
    cols = []
    for p in primaries:
        s = monochromatic(p) if np.isscalar(p) else np.asarray(p, float)
        cols.append(cone_excitations(s))
    return np.column_stack(cols)


def match(test, primaries) -> np.ndarray:
    """The amounts of three primaries whose mixture has the same cone excitations as ``test`` (a spectrum).  A
    negative amount means that primary must be added to the test field instead: the 3-by-3 solve P w = LMS(test)."""
    return np.linalg.solve(primaries_matrix(primaries), cone_excitations(test))


def matching_functions(primaries) -> np.ndarray:
    """Colour-matching functions for three primaries, one row per wavelength on the grid: the amounts of each primary
    that match a unit monochromatic light, row k = P^-1 LMS(lambda_k).  Where a row is negative, that primary has to
    be added to the test side."""
    return np.linalg.solve(primaries_matrix(primaries), LMS.T).T


def null_space_metamer(spectrum, amplitude: float = 1.0, seed: int = 0, smooth: float = 25.0) -> np.ndarray:
    """A metamer of ``spectrum``: add a smooth spectral wiggle projected onto the null space of the cone matrix
    (so L, M and S do not change), scaled by ``amplitude`` relative to the spectrum's peak and kept non-negative."""
    s = np.asarray(spectrum, float)
    rng = np.random.default_rng(seed)
    wig = np.convolve(rng.normal(size=len(WAVELENGTHS) + 60),
                      np.exp(-0.5 * (np.arange(-30, 31) * 5.0 / smooth) ** 2), mode="valid")[: len(WAVELENGTHS)]
    A = LMS.T  # 3 x N
    proj = wig - A.T @ np.linalg.solve(A @ A.T, A @ wig)
    proj = proj / np.abs(proj).max() * amplitude * s.max()
    # keep it physical: shrink until non-negative
    t = 1.0
    while np.min(s + t * proj) < 0 and t > 1e-3:
        t *= 0.9
    return s + t * proj


def opponent(lms) -> np.ndarray:
    """Three post-receptoral channels: luminance L + M, red-green L - M, blue-yellow S - (L + M)/2."""
    v = np.asarray(lms, float)
    L, M, S = v[..., 0], v[..., 1], v[..., 2]
    return np.stack([L + M, L - M, S - (L + M) / 2], axis=-1)


def dichromat(lms, missing: str = "L") -> np.ndarray:
    """What a dichromat's two cone types cannot tell apart: replace the missing cone's excitation with the value
    that keeps a neutral (equal-energy) light and a reference light unchanged (the reduction-plane construction of
    Brettel, Vienot and Mollon, simplified to one plane: 475 nm and 575 nm anchors for L or M, 485 and 660 for S)."""
    v = np.array(lms, float)
    e = cone_excitations(np.ones(len(WAVELENGTHS)))
    anchors = {"L": 575.0, "M": 575.0, "S": 660.0}
    a = cone_excitations(monochromatic(anchors[missing]))
    j = "LMS".index(missing)
    keep = [i for i in range(3) if i != j]
    # the missing coordinate as a linear function of the two kept ones through the plane spanned by e and a
    basis = np.column_stack([e[keep], a[keep]])
    coef = np.linalg.solve(basis, v[..., keep].T if v.ndim > 1 else v[keep])
    out = v.copy()
    if v.ndim > 1:
        out[:, j] = (np.array([e[j], a[j]]) @ coef)
    else:
        out[j] = float(np.array([e[j], a[j]]) @ coef)
    return out


def planck(temperature_k: float) -> np.ndarray:
    """A blackbody's spectral power on the grid, peak 1 (CIE illuminant A is 2856 K)."""
    lam = WAVELENGTHS * 1e-9
    c2 = 1.4388e-2
    s = 1.0 / (lam ** 5 * (np.exp(c2 / (lam * temperature_k)) - 1.0))
    return s / s.max()


def von_kries(lms, illuminant_lms, reference_lms=None) -> np.ndarray:
    """Discount an illuminant by scaling each cone class by reference / illuminant (von Kries 1905)."""
    ref = np.ones(3) if reference_lms is None else np.asarray(reference_lms, float)
    return np.asarray(lms, float) * ref / np.asarray(illuminant_lms, float)


def surface(peak_nm: float, width: float = 60.0, base: float = 0.05, height: float = 0.8) -> np.ndarray:
    """A smooth reflectance: a Gaussian bump on a floor, in [0, 1]."""
    return base + height * np.exp(-0.5 * ((WAVELENGTHS - peak_nm) / width) ** 2)
