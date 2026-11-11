"""Colour (Part 44): sRGB and its transfer curve, CIE XYZ and CIELAB, Ottosson's OKLab (2020), the WCAG contrast
ratio, and colour-vision deficiency simulated with the matrices of Machado, Oliveira and Fernandes (2009) on this
series' own palette."""

from __future__ import annotations

import math


def hex_rgb(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def rgb_hex(rgb):
    return "#" + "".join(f"{max(0, min(255, round(c * 255))):02x}" for c in rgb)


def to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def to_srgb(c: float) -> float:
    c = max(0.0, min(1.0, c))
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def linear(h):
    return tuple(to_linear(c) for c in hex_rgb(h))


M_XYZ = ((0.4124, 0.3576, 0.1805), (0.2126, 0.7152, 0.0722), (0.0193, 0.1192, 0.9505))
WHITE_D65 = (0.95047, 1.0, 1.08883)


def mat(m, v):
    return tuple(sum(m[i][j] * v[j] for j in range(3)) for i in range(3))


def xyz(h):
    return mat(M_XYZ, linear(h))


def lab(h):
    def f(t):
        d = 6 / 29
        return t ** (1 / 3) if t > d ** 3 else t / (3 * d * d) + 4 / 29
    X, Y, Z = xyz(h)
    fx, fy, fz = f(X / WHITE_D65[0]), f(Y / WHITE_D65[1]), f(Z / WHITE_D65[2])
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def oklab_lin(rgb):
    r, g, b = rgb
    l_ = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m_ = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s_ = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = (math.copysign(abs(x) ** (1 / 3), x) for x in (l_, m_, s_))
    return (0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
            1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
            0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_)


def oklab(h):
    return oklab_lin(linear(h))


def de_ok(a, b):
    return math.dist(oklab(a), oklab(b))


def luminance(h):
    r, g, b = linear(h)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


# Machado, Oliveira and Fernandes (2009), severity 1.0, applied to linear RGB
CVD = {
    "protanopia": ((0.152286, 1.052583, -0.204868), (0.114503, 0.786281, 0.099216), (-0.003882, -0.048116, 1.051998)),
    "deuteranopia": ((0.367322, 0.860646, -0.227968), (0.280085, 0.672501, 0.047413), (-0.011820, 0.042940, 0.968881)),
    "tritanopia": ((1.255528, -0.076749, -0.178779), (-0.078411, 0.930809, 0.147602), (0.004733, 0.691367, 0.303900)),
}


def simulate(h, kind):
    v = mat(CVD[kind], linear(h))
    return rgb_hex(tuple(to_srgb(c) for c in v))


PALETTE = {"data": "#58A6FF", "here": "#F7D154", "true": "#5BD17A", "false": "#FF5C5C", "lambda": "#9b8cd6",
           "kernel": "#d98c5f"}
BG = "#121722"


def palette_report(threshold=0.08):
    """Each palette colour under each deficiency, and the pairs whose OKLab distance falls below threshold (a
    rough line for 'easily confused' between small marks)."""
    names = list(PALETTE)
    views = {"normal": dict(PALETTE)}
    for k in CVD:
        views[k] = {n: simulate(c, k) for n, c in PALETTE.items()}
    pairs = {}
    for v, cols in views.items():
        rows = []
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                d = de_ok(cols[names[i]], cols[names[j]])
                rows.append((names[i], names[j], d))
        rows.sort(key=lambda r: r[2])
        pairs[v] = {"closest": rows[:3], "confusable": [r for r in rows if r[2] < threshold]}
    contrast_bg = {n: contrast(c, BG) for n, c in PALETTE.items()}
    return {"views": views, "pairs": pairs, "contrast": contrast_bg, "threshold": threshold}


def checks():
    """Sanity checks against known values: white and black in each space."""
    return {"white_lab": lab("#ffffff"), "white_oklab": oklab("#ffffff"), "black_oklab": oklab("#000000"),
            "red_oklab": oklab("#ff0000"), "grey_lab": lab("#777777")}


def gamma_ramp(n=11):
    """Equal steps in sRGB code values against equal steps in light: why 50% grey is #bcbcbc in light, not #808080."""
    rows = []
    for k in range(n):
        v = k / (n - 1)
        rows.append({"code": v, "light": to_linear(v), "oklab_L": oklab_lin((to_linear(v),) * 3)[0]})
    half_light = rgb_hex((to_srgb(0.5),) * 3)
    return {"rows": rows, "half_light": half_light, "code_128_light": to_linear(128 / 255)}
