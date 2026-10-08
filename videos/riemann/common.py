"""Helpers shared by the Riemann-hypothesis scenes: data, the critical strip, curves, lattices."""

from __future__ import annotations

from functools import lru_cache

import numpy as np

from explainer import *  # noqa: F403
from explainer.fluids import colormaps as cm

from .compute import LANDSCAPE, PI_POWERS_OF_TEN, load  # noqa: F401

# ---------------------------------------------------------------------------
# Facts quoted on screen (sources: videos/riemann/README.md).  Anything that can
# be recomputed from the cached data is asserted against it where it is used.
# ---------------------------------------------------------------------------
RELEASE = dict(
    date="October 6, 2026",
    manuscripts=722,
    families=372,
    problems=4000,
    hours_per_result=3,  # "On average, each result used three hours of ChatGPT Pro thinking compute"
    family_id="003",
    pages_78=199,  # The Quasi-Riemann Hypothesis: A Zero-Free Half-Plane Re(s) > 7/8 (Sept 30, 2026)
    pages_1112=49,  # The Quasi-Riemann Hypothesis (alternate 11/12 proof) (Oct 5, 2026)
    pages_siegel=9,  # Uniform exclusion of Landau-Siegel zeros (Oct 1, 2026)
    formalized_manuscripts=162,
    lean_lines=137_000,  # lean/OAI/NumberTheory/DirichletL, 137,158 lines on Oct 7, 2026
)
PLATT_TRUDGIAN_ZEROS = "12{,}363{,}153{,}437{,}138"  # zeros up to height 3,000,175,332,800, all on the line (2021)


# ---------------------------------------------------------------------------
# Text
# ---------------------------------------------------------------------------
# Labels never wrap on their own (line breaks are always explicit, with \\), and are shrunk
# to fit the frame if needed, so a long line can't silently run off screen.
WIDE_TEX = TEX_TEMPLATE.copy()
WIDE_TEX.add_to_preamble(r"\setlength{\textwidth}{40cm}")
MAX_TEXT_WIDTH = 13.6


def label(text: str, color=WHITE, font_size=32, **kw) -> Tex:
    kw.setdefault("tex_template", WIDE_TEX)
    t = Tex(text, color=color, font_size=font_size, **kw)
    if t.width > MAX_TEXT_WIDTH:
        t.width = MAX_TEXT_WIDTH
    return t


def caption_box(mob: Mobject, color=WHITE, buff=0.18) -> SurroundingRectangle:
    return SurroundingRectangle(mob, color=color, buff=buff, corner_radius=0.08, stroke_width=2)


def tagged(text: str, color=WHITE, font_size=28, opacity=0.85) -> Tex:
    t = label(text, color=color, font_size=font_size)
    t.add_background_rectangle(color=BACKGROUND, opacity=opacity, buff=0.06)
    return t


def note(text: str, font_size=22, color=GREY_B) -> Tex:
    """Small grey caption, e.g. 'schematic' or a source line."""
    return label(text, font_size=font_size, color=color)


def schematic_tag(corner=UR) -> Tex:
    return note(r"schematic").to_corner(corner, buff=0.3)


def source(text: str, font_size=20) -> Tex:
    return label(r"Source: " + text, font_size=font_size, color=GREY_B).to_corner(DR, buff=0.25)


def boxed(mob: Mobject, color=YELLOW, buff=0.25, fill=0.0) -> VGroup:
    box = SurroundingRectangle(mob, color=color, buff=buff, corner_radius=0.12, stroke_width=2.5)
    if fill:
        box.set_fill(color, opacity=fill)
    return VGroup(box, mob)


def part_card(number: int, title: str, subtitle: str = "") -> VGroup:
    num = label(rf"Part {number}", font_size=34, color=C.DIM)
    t = label(title, font_size=60)
    g = VGroup(num, t)
    if subtitle:
        g.add(label(subtitle, font_size=32, color=GREY_A))
    return g.arrange(DOWN, buff=0.3)


def fmt_int(n: int | str) -> str:
    """12345678 -> '12{,}345{,}678' for MathTex."""
    s = f"{int(n):,}"
    return s.replace(",", "{,}")


# ---------------------------------------------------------------------------
# Curves from arrays
# ---------------------------------------------------------------------------
def polyline(ax: Axes, xs, ys, color=WHITE, stroke_width=3, **kw) -> VMobject:
    pts = ax.c2p(np.asarray(xs, float), np.asarray(ys, float)).T
    m = VMobject(color=color, stroke_width=stroke_width, **kw)
    m.set_points_as_corners(pts)
    return m


def staircase(ax: Axes, jumps, heights=None, x0=0.0, x1=None, y0=0.0, color=C.PRIME, stroke_width=3) -> VMobject:
    """Right-continuous step function that jumps by ``heights[i]`` at ``jumps[i]``."""
    jumps = np.asarray(jumps, float)
    heights = np.ones_like(jumps) if heights is None else np.asarray(heights, float)
    x1 = jumps[-1] if x1 is None else x1
    xs, ys, y = [x0], [y0], y0
    for j, h in zip(jumps, heights):
        if j < x0 or j > x1:
            continue
        xs += [j, j]
        ys += [y, y + h]
        y += h
    xs.append(x1)
    ys.append(y)
    return polyline(ax, xs, ys, color=color, stroke_width=stroke_width)


# ---------------------------------------------------------------------------
# Zeta-specific numerics (cheap; the expensive parts live in compute.py)
# ---------------------------------------------------------------------------
def gammas(k: int | None = None) -> np.ndarray:
    g = load("zeros")["gamma"]
    return g if k is None else g[:k]


@lru_cache(maxsize=4)
def _psi_waves(x_max: float, n: int):
    xs = np.linspace(1.5, x_max, n)
    rho = 0.5 + 1j * gammas()
    W = 2 * np.real(np.exp(np.outer(rho, np.log(xs))) / rho[:, None])  # one row per conjugate pair
    return xs, W


def psi_approx(K: int, x_max=50.0, n=2400) -> tuple[np.ndarray, np.ndarray]:
    """von Mangoldt's explicit formula truncated after K zero pairs."""
    xs, W = _psi_waves(x_max, n)
    base = xs - np.log(2 * np.pi) - 0.5 * np.log(1 - xs**-2.0)
    return xs, base - W[:K].sum(axis=0)


def psi_wave(k: int, x_max=50.0, n=2400) -> tuple[np.ndarray, np.ndarray]:
    """The k-th conjugate-pair wave 2 Re(x^rho/rho) (k = 0 for the first zero)."""
    xs, W = _psi_waves(x_max, n)
    return xs, W[k]


def psi_steps(x_max=50.0) -> tuple[np.ndarray, np.ndarray]:
    d = load("primes")
    pp, lg = d["prime_powers"], d["prime_power_logs"]
    m = pp <= x_max
    return pp[m], lg[m]


def partial_sums(s: complex, N: int) -> np.ndarray:
    """0, 1, 1 + 2^-s, ..., sum_{n<=N} n^-s as complex numbers."""
    n = np.arange(1, N + 1)
    return np.concatenate([[0], np.cumsum(np.exp(-s * np.log(n)))])


def spiral_center(s: complex, N: int) -> complex:
    """Euler–Maclaurin: zeta(s) = lim (S_N - N^(1-s)/(1-s) - N^-s/2) for Re s > 0, s != 1."""
    S = partial_sums(s, N)[-1]
    return S - N ** (1 - s) / (1 - s) - 0.5 * N ** (-s)


def zeta(s: complex) -> complex:
    import mpmath

    return complex(mpmath.zeta(s))


# ---------------------------------------------------------------------------
# The complex plane and the critical strip
# ---------------------------------------------------------------------------
def strip_axes(t_max=40.0, x_length=4.2, y_length=6.2, sig=(-0.35, 1.35), t_min=0.0, labels=True) -> VGroup:
    """Axes for (sigma, t) with the lines Re s = 0, 1/2, 1 drawn in.

    Returns a VGroup with attributes ``ax`` (the Axes), ``line0``, ``crit``, ``line1``,
    and ``labels``; use ``g.ax.c2p(sigma, t)`` to place things.
    """
    ax = Axes(x_range=[sig[0], sig[1], 0.5], y_range=[t_min, t_max, 10], x_length=x_length, y_length=y_length,
              axis_config={"include_ticks": False, "stroke_color": GREY_C, "stroke_width": 2},
              tips=False)
    g = VGroup(ax)
    g.ax = ax
    g.line0 = Line(ax.c2p(0, t_min), ax.c2p(0, t_max), color=GREY_B, stroke_width=2)
    g.line1 = Line(ax.c2p(1, t_min), ax.c2p(1, t_max), color=GREY_B, stroke_width=2)
    g.crit = DashedLine(ax.c2p(0.5, t_min), ax.c2p(0.5, t_max), color=C.ZERO, stroke_width=2.5, dash_length=0.12)
    g.add(g.line0, g.line1, g.crit)
    g.labels = VGroup(
        MathTex("0", font_size=28).next_to(ax.c2p(0, t_min), DOWN, buff=0.15),
        MathTex(r"\tfrac12", font_size=30, color=C.ZERO).next_to(ax.c2p(0.5, t_min), DOWN, buff=0.12),
        MathTex("1", font_size=28).next_to(ax.c2p(1, t_min), DOWN, buff=0.15),
    )
    if labels:
        g.add(g.labels)
    return g


def zero_dots(ax: Axes, ts, sigma=0.5, color=C.ZERO, radius=0.055) -> VGroup:
    return VGroup(*[Dot(ax.c2p(sigma, t), radius=radius, color=color) for t in ts])


def region(ax: Axes, sig0, sig1, t0, t1, color=C.ZERO_FREE, opacity=0.28) -> Polygon:
    return Polygon(ax.c2p(sig0, t0), ax.c2p(sig1, t0), ax.c2p(sig1, t1), ax.c2p(sig0, t1),
                   stroke_width=0, fill_color=color, fill_opacity=opacity)


def classical_region(ax: Axes, c=0.35, t0=2.0, t1=40.0, color=C.ZERO_FREE, opacity=0.35, n=200) -> VMobject:
    """Schematic de la Vallée Poussin region sigma > 1 - c/log(t) (c exaggerated so it is visible)."""
    ts = np.linspace(t0, t1, n)
    left = 1 - c / np.log(ts + 1.8)
    pts = [ax.c2p(s, t) for s, t in zip(left, ts)] + [ax.c2p(1, t1), ax.c2p(1, t0)]
    poly = Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=opacity)
    edge = polyline(ax, left, ts, color=color, stroke_width=2.5)
    return VGroup(poly, edge)


# ---------------------------------------------------------------------------
# Domain coloring of zeta (from compute.py's "landscape" grid)
# ---------------------------------------------------------------------------
def _hsv_to_rgb(h, s, v):
    i = np.floor(h * 6).astype(int) % 6
    f = h * 6 - np.floor(h * 6)
    p, q, t = v * (1 - s), v * (1 - f * s), v * (1 - (1 - f) * s)
    r = np.choose(i, [v, q, p, p, t, v])
    g = np.choose(i, [t, v, v, q, p, p])
    b = np.choose(i, [p, p, t, v, v, q])
    return np.stack([r, g, b], axis=-1)


def domain_rgb(Z: np.ndarray, sat=0.74) -> np.ndarray:
    """Hue = arg(zeta); brightness rises with |zeta| (black at zeros, bright where |zeta| is large);
    faint rings at |zeta| = 2^k show the size."""
    Z = np.asarray(Z, dtype=np.complex128)
    finite = np.isfinite(Z)
    Z = np.where(finite, Z, 1e8)
    mag = np.abs(Z)
    h = (np.angle(Z) / (2 * np.pi)) % 1.0
    m = mag**0.55
    v = 0.12 + 0.8 * m / (1 + m)  # 0.12 at a zero, 0.52 where |zeta| = 1, -> 0.92 for large |zeta|
    v = np.where(mag < 1e-3, 0.0, v)
    lm = np.log2(np.maximum(mag, 1e-12))
    v = v * (0.86 + 0.14 * (lm - np.floor(lm)))
    v = v * np.clip(mag / 0.08, 0, 1) ** 0.5  # sink to black right at the zeros
    s = np.full_like(v, sat)
    s = np.where(mag > 50, sat * 0.75, s)
    return _hsv_to_rgb(h, s, np.clip(v, 0, 1)) * 0.9


def landscape_image(ax: Axes, alpha: float = 1.0, mask=None) -> ImageMobject:
    """ImageMobject covering the landscape's (sigma, t) rectangle on ``ax``.

    ``mask(sig, t) -> bool array`` hides (makes transparent) the pixels where it is False.
    """
    d = load("landscape")
    rgb = domain_rgb(d["Z"])
    ny, nx = rgb.shape[:2]
    (s0, s1), (t0, t1) = d["sig"], d["t"]
    a = np.full((ny, nx, 1), alpha)
    if mask is not None:
        S, T = np.meshgrid(np.linspace(s0, s1, nx), np.linspace(t1, t0, ny))
        a = a * mask(S, T)[..., None]
    img = ImageMobject(cm.to_uint8(np.concatenate([rgb, a], axis=2)))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
    p0, p1 = ax.c2p(s0, t0), ax.c2p(s1, t1)
    img.stretch_to_fit_width(p1[0] - p0[0]).stretch_to_fit_height(p1[1] - p0[1])
    img.move_to((p0 + p1) / 2)
    return img


def color_wheel(radius=0.7, n=96) -> VGroup:
    """Legend for the domain coloring: angle of zeta -> hue."""
    g = VGroup()
    for k in range(n):
        a0, a1 = 2 * PI * k / n, 2 * PI * (k + 1) / n
        rgb = _hsv_to_rgb(np.array([(k + 0.5) / n]), np.array([0.78]), np.array([0.92]))[0]
        g.add(AnnularSector(inner_radius=radius * 0.55, outer_radius=radius, angle=a1 - a0, start_angle=a0,
                            fill_color=rgb_to_color(rgb), fill_opacity=1, stroke_width=0))
    return g


# ---------------------------------------------------------------------------
# Eisenstein integers  a + b*omega,  omega = e^{2 pi i / 3}
# ---------------------------------------------------------------------------
OMEGA = complex(-0.5, np.sqrt(3) / 2)


def eis(a, b) -> complex:
    return a + b * OMEGA


def eis_norm(a, b):
    return a * a - a * b + b * b


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    r = int(n**0.5)
    return all(n % p for p in range(3, r + 1, 2))


def eisenstein_primes(radius: float) -> list[tuple[int, int]]:
    """All Eisenstein primes a + b omega with |a + b omega| <= radius."""
    R = int(radius * 1.3) + 2
    out = []
    for a in range(-R, R + 1):
        for b in range(-R, R + 1):
            if abs(eis(a, b)) > radius:
                continue
            N = eis_norm(a, b)
            if _is_prime(N):  # N = 3 or N = p = 1 mod 3
                out.append((a, b))
            else:
                q = int(round(np.sqrt(N)))
                if q * q == N and _is_prime(q) and q % 3 == 2 and (a, b) in {
                    (q, 0), (0, q), (-q, -q), (-q, 0), (0, -q), (q, q)
                }:
                    out.append((a, b))
    return out


def sextic_symbol_table(a: int, b: int):
    """For the Eisenstein prime pi = a + b omega with prime norm p = 1 mod 6, return a function
    k(x, y) giving the sextic residue symbol (x + y omega / pi)_6 = zeta6^k  (zeta6 = e^{i pi/3}),
    or None where pi divides x + y omega."""
    p = eis_norm(a, b)
    assert _is_prime(p) and p % 6 == 1, p
    r = (-a * pow(b, -1, p)) % p  # omega -> r in Z[omega]/(pi) = F_p
    assert (r * r + r + 1) % p == 0
    z6 = (-r * r) % p  # image of zeta6 = -omega^2
    powers = {pow(z6, k, p): k for k in range(6)}
    assert len(powers) == 6
    e = (p - 1) // 6

    def k(x: int, y: int):
        u = (x + y * r) % p
        if u == 0:
            return None
        return powers[pow(u, e, p)]

    return k


def lattice_point(plane: Axes | NumberPlane, a, b) -> np.ndarray:
    z = eis(a, b)
    return plane.c2p(z.real, z.imag)


# ---------------------------------------------------------------------------
# Number-theory helpers for small displays
# ---------------------------------------------------------------------------
def mobius_small(n: int) -> int:
    m, k, p = n, 0, 2
    while p * p <= m:
        if m % p == 0:
            m //= p
            if m % p == 0:
                return 0
            k += 1
        p += 1
    if m > 1:
        k += 1
    return -1 if k % 2 else 1


MU_COLORS = {1: TEAL_B, -1: MAROON_B, 0: GREY_D}  # mu(n) = +1, -1, 0


def legendre(a: int, p: int) -> int:
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1
