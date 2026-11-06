"""BRDFs and importance sampling (Part 51): Lambert, normalized Phong and Blinn-Phong lobes, the Cook-Torrance
microfacet BRDF with the GGX distribution, Smith masking-shadowing and Fresnel-Schlick; white-furnace tests of energy
conservation, reciprocity, the pdfs of the standard sampling strategies, and multiple importance sampling.

All directions are unit vectors in the local shading frame (the normal is +z), pointing away from the surface; arrays
broadcast over leading axes.  f(wi, wo) is the BRDF; the reflected radiance is L_o = integral f L_i cos(theta_i) dw_i.

Sources: Pharr, Jakob and Humphreys, *Physically Based Rendering* 4th ed. (PBRT), chapters 4 (radiometry), 9
(reflection models: 9.6 the Trowbridge-Reitz / GGX microfacet model) and A.5 (sampling); Cook and Torrance, "A
reflectance model for computer graphics", 1982; Walter, Marschner, Li and Torrance, "Microfacet models for refraction
through rough surfaces", EGSR 2007 (GGX D, Smith G1 and the half-vector pdf D cos / (4 |wo.h|)); Schlick 1994
(Fresnel); Lewis, "Making shaders more physically plausible", 1994 (the (n + 2) / 2 pi normalized Phong); Akenine-Moller
et al., *Real-Time Rendering* 4th ed., 9.8 (the (n + 8) / 8 pi Blinn-Phong normalization, an approximation); Veach,
*Robust Monte Carlo Methods for Light Transport Simulation*, PhD thesis 1997, chapter 9 (multiple importance sampling:
balance and power heuristics); Duff et al., "Building an orthonormal basis, revisited", JCGT 2017.
"""

from __future__ import annotations

import math

import numpy as np

PI = math.pi


def _dot(a, b):
    return np.einsum("...i,...i->...", a, b)


def _normalize(v):
    return v / np.linalg.norm(v, axis=-1, keepdims=True)


def _sph(cos_t, phi):
    cos_t, phi = np.broadcast_arrays(np.asarray(cos_t, float), np.asarray(phi, float))
    s = np.sqrt(np.clip(1 - cos_t * cos_t, 0, None))
    return np.stack([s * np.cos(phi), s * np.sin(phi), cos_t], -1)


def direction(theta_deg: float, phi_deg: float = 0.0) -> np.ndarray:
    t, p = math.radians(theta_deg), math.radians(phi_deg)
    return np.array([math.sin(t) * math.cos(p), math.sin(t) * math.sin(p), math.cos(t)])


def mirror(w):
    """Mirror direction about the normal: (-x, -y, z)."""
    return w * np.array([-1.0, -1.0, 1.0])


def frame(axis):
    """Two unit vectors (t, b) completing ``axis`` (unit, (..., 3)) to a right-handed orthonormal basis (Duff et al.
    2017)."""
    x, y, z = axis[..., 0], axis[..., 1], axis[..., 2]
    s = np.where(z >= 0, 1.0, -1.0)
    a = -1.0 / (s + z)
    b = x * y * a
    t = np.stack([1 + s * x * x * a, s * b, -s * x], -1)
    bb = np.stack([b, s + y * y * a, -y], -1)
    return t, bb


# ---------------------------------------------------------------- BRDFs

def _upper(wi, wo):
    return (wi[..., 2] > 0) & (wo[..., 2] > 0)


def lambert(wi, wo, albedo: float = 1.0):
    """f = albedo / pi: radiance scattered equally in all directions (Lambert's cosine law lives in the cos theta_i of
    the reflection integral).  Its directional albedo is exactly ``albedo``."""
    return np.where(_upper(wi, wo), albedo / PI, 0.0)


def phong(wi, wo, n: float, ks: float = 1.0):
    """Normalized Phong lobe f = ks (n + 2) / (2 pi) cos^n(alpha), alpha the angle between wi and the mirror direction
    of wo (Lewis 1994).  The normalization makes the albedo exactly ks at normal incidence; elsewhere the horizon clips
    the lobe and the albedo is below ks."""
    c = np.clip(_dot(wi, mirror(wo)), 0, None)
    return np.where(_upper(wi, wo), ks * (n + 2) / (2 * PI) * c ** n, 0.0)


def blinn_phong(wi, wo, n: float, ks: float = 1.0):
    """Blinn-Phong lobe f = ks (n + 8) / (8 pi) cos^n(theta_h), theta_h the angle of the half vector h = (wi + wo)/|.|
    from the normal; (n + 8) / 8 pi is the usual approximate normalization (Real-Time Rendering 9.8)."""
    h = _normalize(wi + wo)
    return np.where(_upper(wi, wo), ks * (n + 8) / (8 * PI) * np.clip(h[..., 2], 0, None) ** n, 0.0)


def blinn_phong_ndf(cos_h, n: float):
    """The normalized Blinn-Phong microfacet distribution D = (n + 2) / (2 pi) cos^n(theta_h): integral D cos dw = 1."""
    return (n + 2) / (2 * PI) * np.clip(cos_h, 0, None) ** n


def ggx_d(cos_h, alpha: float):
    """GGX (Trowbridge-Reitz) normal distribution D(h) = alpha^2 / (pi ((n.h)^2 (alpha^2 - 1) + 1)^2) (Walter et al.
    2007, eq. 33); normalized so that the projected microfacet area integral D(h) cos(theta_h) dw_h = 1."""
    c = np.asarray(cos_h, float)
    a2 = alpha * alpha
    den = c * c * (a2 - 1) + 1
    return np.where(c > 0, a2 / (PI * den * den), 0.0)


def smith_g1(cos_v, alpha: float):
    """Smith masking for GGX, G1(v) = 2 / (1 + sqrt(1 + alpha^2 tan^2 theta_v)) = 2 cos / (cos + sqrt(alpha^2 +
    (1 - alpha^2) cos^2)) (Walter et al. 2007, eq. 34)."""
    c = np.asarray(cos_v, float)
    a2 = alpha * alpha
    cc = np.clip(c, 0, None)
    return np.where(c > 0, 2 * cc / (cc + np.sqrt(a2 + (1 - a2) * cc * cc)), 0.0)


def fresnel_schlick(cos, f0):
    """F = F0 + (1 - F0)(1 - cos)^5 (Schlick 1994)."""
    return f0 + (1 - f0) * (1 - np.clip(cos, 0, 1)) ** 5


def cook_torrance(wi, wo, alpha: float, f0: float = 1.0):
    """Cook-Torrance microfacet BRDF f = D(h) G(wi, wo) F(wi.h) / (4 cos theta_i cos theta_o) with GGX D, the separable
    Smith G = G1(wi) G1(wo) (each zero when the microfacet is back-facing, Walter's chi+) and Fresnel-Schlick F."""
    h = _normalize(wi + wo)
    ci, co, ch = wi[..., 2], wo[..., 2], h[..., 2]
    hi, ho = _dot(wi, h), _dot(wo, h)
    g = smith_g1(ci, alpha) * smith_g1(co, alpha) * (hi > 0) * (ho > 0)
    ok = _upper(wi, wo)
    with np.errstate(divide="ignore", invalid="ignore"):
        f = ggx_d(ch, alpha) * g * fresnel_schlick(hi, f0) / (4 * ci * co)
    return np.where(ok, f, 0.0)


MODELS = {
    "lambert": lambda wi, wo, p: lambert(wi, wo),
    "phong": lambda wi, wo, p: phong(wi, wo, p),
    "blinn_phong": lambda wi, wo, p: blinn_phong(wi, wo, p),
    "ggx": lambda wi, wo, p: cook_torrance(wi, wo, p),
}


# ---------------------------------------------------------------- sampling (PBRT A.5)

def sample_uniform_hemisphere(u1, u2):
    """cos theta = u1, phi = 2 pi u2: uniform over the hemisphere, pdf 1 / (2 pi)."""
    w = _sph(np.asarray(u1, float), 2 * PI * np.asarray(u2, float))
    return w, np.full(w.shape[:-1], 1 / (2 * PI))


def pdf_uniform_hemisphere(w):
    return np.where(w[..., 2] > 0, 1 / (2 * PI), 0.0)


def sample_cosine_hemisphere(u1, u2):
    """Malley's method: a uniform point on the unit disk (r = sqrt(u1), phi = 2 pi u2) lifted to the hemisphere;
    pdf cos theta / pi."""
    u1 = np.asarray(u1, float)
    w = _sph(np.sqrt(1 - u1), 2 * PI * np.asarray(u2, float))
    return w, w[..., 2] / PI


def pdf_cosine_hemisphere(w):
    return np.clip(w[..., 2], 0, None) / PI


def sample_ggx(wo, alpha: float, u1, u2):
    """Sample a microfacet normal h with density D(h) cos theta_h (tan^2 theta_h = alpha^2 u1 / (1 - u1)), reflect wo
    about it: wi = 2 (wo.h) h - wo, with pdf D(h) cos theta_h / (4 |wo.h|) (the Jacobian dw_h / dw_i = 1 / 4|wo.h|,
    Walter et al. 2007, eq. 14 and 35-36).  Directions below the horizon can come out; their BRDF is zero."""
    u1, u2 = np.asarray(u1, float), np.asarray(u2, float)
    cos_h = 1 / np.sqrt(1 + alpha * alpha * u1 / (1 - u1))
    h = _sph(cos_h, 2 * PI * u2)
    wo = np.broadcast_to(wo, h.shape)
    wi = 2 * _dot(wo, h)[..., None] * h - wo
    return wi, pdf_ggx(wi, wo, alpha)


def pdf_ggx(wi, wo, alpha: float):
    h = wi + np.broadcast_to(wo, np.shape(wi))
    h = _normalize(h)
    h = np.where((h[..., 2] < 0)[..., None], -h, h)
    with np.errstate(divide="ignore", invalid="ignore"):
        p = ggx_d(h[..., 2], alpha) * h[..., 2] / (4 * np.abs(_dot(wo, h)))
    return np.nan_to_num(p)


def sample_phong_lobe(axis, n: float, u1, u2):
    """cos alpha = u1^(1/(n+1)) about ``axis``: density (n + 1) / (2 pi) cos^n alpha over the sphere."""
    u1, u2 = np.asarray(u1, float), np.asarray(u2, float)
    loc = _sph(u1 ** (1 / (n + 1)), 2 * PI * u2)
    axis = np.broadcast_to(np.asarray(axis, float), loc.shape)
    t, b = frame(axis)
    w = loc[..., :1] * t + loc[..., 1:2] * b + loc[..., 2:] * axis
    return w, pdf_phong_lobe(w, axis, n)


def pdf_phong_lobe(w, axis, n: float):
    return (n + 1) / (2 * PI) * np.clip(_dot(w, axis), 0, None) ** n


def sample_cone(axis, cos_max: float, u1, u2):
    """Uniform over the cone of directions within angle acos(cos_max) of ``axis`` (the solid angle a sphere subtends):
    cos theta = 1 - u1 (1 - cos_max), pdf 1 / (2 pi (1 - cos_max)) (PBRT 6.2.4)."""
    u1, u2 = np.asarray(u1, float), np.asarray(u2, float)
    loc = _sph(1 - u1 * (1 - cos_max), 2 * PI * u2)
    axis = np.broadcast_to(np.asarray(axis, float), loc.shape)
    t, b = frame(axis)
    w = loc[..., :1] * t + loc[..., 1:2] * b + loc[..., 2:] * axis
    return w, np.full(w.shape[:-1], 1 / (2 * PI * (1 - cos_max)))


def pdf_cone(w, axis, cos_max: float):
    return np.where(_dot(w, axis) >= cos_max, 1 / (2 * PI * (1 - cos_max)), 0.0)


# ---------------------------------------------------------------- quadrature

def _gl(a, b, panels, order=8):
    """Composite Gauss-Legendre nodes and weights on [a, b]."""
    x, w = np.polynomial.legendre.leggauss(order)
    edges = np.linspace(a, b, panels + 1)
    h = (edges[1:] - edges[:-1]) / 2
    mid = (edges[1:] + edges[:-1]) / 2
    return (mid[:, None] + h[:, None] * x).ravel(), (h[:, None] * w).ravel()


def sphere_integral(fn, theta_panels: int = 256, n_phi: int = 512, upper_only: bool = False, chunk: int = 64):
    """Integral of fn(w) over the sphere (or the upper hemisphere) by composite Gauss-Legendre in theta and the
    trapezoid rule in phi (spectrally accurate for periodic integrands): dw = sin theta dtheta dphi."""
    th, wt = _gl(0, PI / 2 if upper_only else PI, theta_panels)
    phi = (np.arange(n_phi) + 0.5) * 2 * PI / n_phi
    total = 0.0
    for i in range(0, len(th), chunk):
        t = th[i:i + chunk]
        w = _sph(np.cos(t)[:, None], phi[None, :])
        total += float((fn(w).sum(1) * (2 * PI / n_phi) * np.sin(t) * wt[i:i + chunk]).sum())
    return total


def albedo_quadrature(model: str, param: float, wo, theta_panels: int = 256, n_phi: int = 1024) -> float:
    """Directional albedo rho(wo) = integral f(wi, wo) cos theta_i dw_i by quadrature over wi (no sampling)."""
    f = MODELS[model]
    return sphere_integral(lambda wi: f(wi, wo, param) * np.clip(wi[..., 2], 0, None), theta_panels, n_phi,
                           upper_only=True)


def albedo_mc(model: str, param: float, wo, samples: int = 200_000, seed: int = 0) -> tuple[float, float]:
    """Directional albedo by Monte Carlo with each model's importance sampling (cosine for Lambert, the Phong lobe
    about the mirror direction for Phong, uniform hemisphere for Blinn-Phong, GGX half-vector sampling for GGX).
    Returns (estimate, standard error)."""
    rng = np.random.default_rng(seed)
    u1, u2 = rng.random(samples), rng.random(samples)
    if model == "lambert":
        wi, pdf = sample_cosine_hemisphere(u1, u2)
    elif model == "phong":
        wi, pdf = sample_phong_lobe(mirror(wo), param, u1, u2)
    elif model == "blinn_phong":
        wi, pdf = sample_uniform_hemisphere(u1, u2)
    else:
        wi, pdf = sample_ggx(wo, param, u1, u2)
    with np.errstate(divide="ignore", invalid="ignore"):
        x = np.where(pdf > 0, MODELS[model](wi, wo, param) * np.clip(wi[..., 2], 0, None) / pdf, 0.0)
    return float(x.mean()), float(x.std() / math.sqrt(samples))


def white_furnace(roughness=(0.05, 0.1, 0.25, 0.5, 0.75, 1.0), view_deg=(0, 30, 60, 80), exponents=(1, 10, 100),
                  samples: int = 200_000, seed: int = 0) -> list[dict]:
    """The white furnace: under uniform unit illumination a surface reflects its directional albedo
    rho(wo) = integral f cos theta_i dw_i, which energy conservation keeps at most 1.  For GGX (F0 = 1, so only masking
    and shadowing lose energy) at each roughness alpha, for normalized Phong and Blinn-Phong at each exponent, and for
    Lambert, at each view angle: rows of model, param, theta_deg, mc, mc_se (Monte Carlo with importance sampling) and
    quad (deterministic quadrature over wi)."""
    rows = []
    cases = [("ggx", a) for a in roughness] + [("phong", n) for n in exponents] + \
        [("blinn_phong", n) for n in exponents] + [("lambert", 1.0)]
    for model, p in cases:
        for th in view_deg:
            wo = direction(th)
            mc, se = albedo_mc(model, p, wo, samples, seed)
            rows.append({"model": model, "param": float(p), "theta_deg": float(th), "mc": mc, "mc_se": se,
                         "quad": albedo_quadrature(model, p, wo)})
    return rows


def reciprocity(pairs: int = 10_000, seed: int = 0, params=None) -> dict:
    """Helmholtz reciprocity f(wi, wo) = f(wo, wi), checked on random direction pairs: for each model the largest
    relative difference |f(wi, wo) - f(wo, wi)| / max(f) over the pairs."""
    rng = np.random.default_rng(seed)
    a, _ = sample_uniform_hemisphere(rng.random(pairs), rng.random(pairs))
    b, _ = sample_uniform_hemisphere(rng.random(pairs), rng.random(pairs))
    params = params or {"lambert": 1.0, "phong": 20.0, "blinn_phong": 20.0, "ggx": 0.3}
    out = {}
    for m, p in params.items():
        f1, f2 = MODELS[m](a, b, p), MODELS[m](b, a, p)
        if m == "ggx":  # with Fresnel too
            f1, f2 = cook_torrance(a, b, p, 0.04), cook_torrance(b, a, p, 0.04)
        out[m] = float(np.max(np.abs(f1 - f2)) / np.max(np.abs(f1)))
    return out


def pdf_integrals() -> dict:
    """Each sampling pdf integrated over the sphere by quadrature (independently of its sampler): all should be 1."""
    wo = direction(45)
    out = {"uniform_hemisphere": sphere_integral(pdf_uniform_hemisphere),
           "cosine_hemisphere": sphere_integral(pdf_cosine_hemisphere)}
    for a in (0.2, 0.5, 1.0):
        out[f"ggx_{a}"] = sphere_integral(lambda w: pdf_ggx(w, wo, a), 512, 1024)
    for n in (10, 100):
        out[f"phong_lobe_{n}"] = sphere_integral(lambda w: pdf_phong_lobe(w, mirror(wo), n), 512, 1024)
    ax = _normalize(np.array([0.3, -0.2, 0.9]))
    out["cone_0.9"] = sphere_integral(lambda w: pdf_cone(w, ax, 0.9), 2048, 1024)
    out["ggx_ndf_0.1"] = sphere_integral(lambda h: ggx_d(h[..., 2], 0.1) * np.clip(h[..., 2], 0, None), 2048, 64,
                                         upper_only=True)
    return out


# ---------------------------------------------------------------- multiple importance sampling

def _mis_exact(n, cos_max, axis, Le, theta_panels=96):
    """Reflected radiance by quadrature over the light's cone in cone coordinates (theta' from the axis, phi'):
    dw = sin theta' dtheta' dphi', with panels refined to the Phong lobe width."""
    tmax = math.acos(cos_max)
    knee = min(tmax, 8 / math.sqrt(n))
    t1, w1 = _gl(0, knee, theta_panels, 16)
    if knee < tmax:
        t2, w2 = _gl(knee, tmax, theta_panels, 16)
        t1, w1 = np.concatenate([t1, t2]), np.concatenate([w1, w2])
    phi = (np.arange(512) + 0.5) * 2 * PI / 512
    loc = _sph(np.cos(t1)[:, None], phi[None, :])
    tt, bb = frame(axis)
    w = loc[..., :1] * tt + loc[..., 1:2] * bb + loc[..., 2:] * axis
    g = (n + 2) / (2 * PI) * np.clip(_dot(w, axis), 0, None) ** n * np.clip(w[..., 2], 0, None) * Le
    return float((g.sum(1) * (2 * PI / 512) * np.sin(t1) * w1).sum())


def mis_experiment(exponents=(10, 100, 1000), radii=(0.05, 0.3, 1.0), samples: int = 32, trials: int = 4000,
                   view_deg: float = 45.0, distance: float = 3.0, seed: int = 0) -> list[dict]:
    """One shading point (normal +z, viewed from ``view_deg``) on a glossy normalized-Phong surface of exponent n, lit
    by a spherical light of radius r and radiance 1 centred on the mirror direction at ``distance``.  The reflected
    radiance L = integral over the light's cone of f(wi, wo) cos theta_i dw_i is estimated with ``samples`` samples by
    light sampling (uniform over the cone), BRDF sampling (the Phong lobe), and MIS with half the samples from each
    (Veach 1997): the balance heuristic w_s = p_s / (p_l + p_b) and the power heuristic w_s = p_s^2 / (p_l^2 + p_b^2).
    For each (n, r): the exact value (quadrature), the relative RMSE of each estimator over ``trials`` trials
    (rel_rmse_light, rel_rmse_brdf, rel_rmse_balance, rel_rmse_power), their means and the best method.  Each pure
    strategy fails in one corner; MIS, with half its samples from each, stays within Veach's bound (its variance
    exceeds the best strategy's by at most (2/N - 1/N) L^2 with N samples), so it is never far off."""
    rng = np.random.default_rng(seed)
    wo = direction(view_deg)
    axis = mirror(wo)
    rows = []
    for n in exponents:
        for r in radii:
            cos_max = math.sqrt(1 - (r / distance) ** 2)
            exact = _mis_exact(n, cos_max, axis, 1.0)

            def integrand(w):
                inside = _dot(w, axis) >= cos_max
                return np.where(inside, phong(w, wo, n), 0.0) * np.clip(w[..., 2], 0, None)

            def light(k):
                w, p = sample_cone(axis, cos_max, rng.random((trials, k)), rng.random((trials, k)))
                return w, p, pdf_phong_lobe(w, axis, n)

            def brdf(k):
                w, p = sample_phong_lobe(axis, n, rng.random((trials, k)), rng.random((trials, k)))
                return w, p, pdf_cone(w, axis, cos_max)

            wl, pl, pbl = light(samples)
            est_l = (integrand(wl) / pl).mean(1)
            wb, pb, plb = brdf(samples)
            est_b = (integrand(wb) / pb).mean(1)
            h = samples // 2
            wl, pl, pbl = light(h)
            wb, pb, plb = brdf(h)
            fl, fb = integrand(wl), integrand(wb)
            est = {}
            for name, beta in (("balance", 1), ("power", 2)):
                wl_ = pl ** beta / (pl ** beta + pbl ** beta)
                wb_ = pb ** beta / (pb ** beta + plb ** beta)
                est[name] = (wl_ * fl / pl).sum(1) / h + (wb_ * fb / pb).sum(1) / h
            rel = {k: float(np.sqrt(np.mean((v - exact) ** 2)) / exact)
                   for k, v in (("light", est_l), ("brdf", est_b), ("balance", est["balance"]),
                                ("power", est["power"]))}
            rows.append({"n": n, "r": r, "exact": exact, "best": min(rel, key=rel.get),
                         "cone_half_angle_deg": math.degrees(math.acos(cos_max)),
                         "lobe_width_deg": math.degrees(1 / math.sqrt(n)),
                         "mean": {"light": float(est_l.mean()), "brdf": float(est_b.mean()),
                                  "balance": float(est["balance"].mean()), "power": float(est["power"].mean())},
                         **{f"rel_rmse_{k}": v for k, v in rel.items()}})
    return rows
