"""Path tracing (Part 51): the series' scene (a Cornell-like box with a red and a green wall, a square area light in the
ceiling, a mirror sphere and two diffuse spheres) rendered by a Monte Carlo path tracer that solves the rendering
equation L = L_e + T L (Kajiya 1986) one path at a time.  Each path's light is recorded by the number of reflections
it took, so the image splits into the terms of the Neumann series L = L_e + T L_e + T^2 L_e + ...: bounce 0 is the
emitted light seen directly, bounce 1 direct lighting, bounce 2 one indirect bounce, and so on.

The estimator at a diffuse vertex (albedo rho, f = rho / pi) samples a direction with pdf p and multiplies the path
throughput by f cos / p: rho with cosine-weighted sampling (p = cos / pi), 2 rho cos with uniform sampling
(p = 1 / 2 pi).  Next-event estimation adds the light's direct contribution at every diffuse vertex by sampling a
point uniformly on the light (pdf 1 / A over area; the geometry term cos cos' / d^2 converts it to solid angle), and
then ignores light reached by the next bounce so it is not counted twice (except after a mirror bounce, which NEE
cannot sample).  Russian roulette ends a path after ``rr_start`` bounces with probability 1 - q and divides survivors'
throughput by q; the expected contribution is q (X / q) + (1 - q) 0 = X, so it is unbiased.

Sources: Kajiya, "The rendering equation", SIGGRAPH 1986; Pharr, Jakob and Humphreys, *Physically Based Rendering*
4th ed., chapters 13 (path tracing, Russian roulette, NEE) and A.5 (sampling: Malley's method); Veach 1997 (thesis),
chapter 10 (path integral form); Arvo and Kirk, "Particle transport and image synthesis", 1990 (Russian roulette);
Dammertz, Sewtz, Hanika and Lensch, "Edge-avoiding A-trous wavelet transform for fast global illumination
filtering", HPG 2010; Goral et al. 1984 (the Cornell box) for the wall albedos; IEC 61966-2-1 (sRGB).
"""

from __future__ import annotations

import math
import time

import numpy as np
from numba import njit

EPS = 1e-7
OFF = 1e-6


# ---------------------------------------------------------------- scenes

def _rect(axis, pos, lo, hi, sign, albedo, emit=(0.0, 0.0, 0.0)):
    return {"axis": axis, "pos": pos, "lo": lo, "hi": hi, "sign": sign, "albedo": albedo, "emit": emit}


def cornell_scene(light_radiance=(17.0, 14.0, 10.0), spheres: bool = True) -> dict:
    """The series' scene in the unit cube: x from the red wall (x = 0) to the green wall (x = 1), y up, z from the open
    front (z = 0) to the back wall (z = 1).  Rectangles are given by their axis, position, and bounds on the other two
    axes in increasing order (x, y, z without the axis); ``sign`` is the side their normal faces (the side a one-sided
    emitter lights).  Wall albedos are the Cornell box's (white 0.73, red, green).  The light is a 0.25 x 0.25 square
    just below the ceiling, a pure emitter.  Camera at z = -1.35 with a 40 degree field of view."""
    white, red, green = (0.73, 0.73, 0.73), (0.63, 0.065, 0.05), (0.14, 0.45, 0.091)
    rects = [
        _rect(1, 0.0, (0, 0), (1, 1), +1, white),  # floor
        _rect(1, 1.0, (0, 0), (1, 1), -1, white),  # ceiling
        _rect(2, 1.0, (0, 0), (1, 1), -1, white),  # back wall
        _rect(0, 0.0, (0, 0), (1, 1), +1, red),  # left wall
        _rect(0, 1.0, (0, 0), (1, 1), -1, green),  # right wall
        _rect(1, 0.9999, (0.375, 0.375), (0.625, 0.625), -1, (0, 0, 0), light_radiance),  # light
    ]
    sph = []
    if spheres:
        sph = [((0.30, 0.22, 0.64), 0.22, (0.95, 0.95, 0.95), True),  # mirror
               ((0.72, 0.17, 0.36), 0.17, white, False),  # white diffuse
               ((0.50, 0.07, 0.16), 0.07, (0.20, 0.32, 0.75), False)]  # small blue
    return {"rects": rects, "spheres": [{"center": c, "radius": r, "albedo": a, "mirror": m, "emit": (0, 0, 0)}
                                        for c, r, a, m in sph],
            "light": 5, "camera": {"eye": (0.5, 0.5, -1.35), "look": (0.5, 0.5, 0.0), "fov_deg": 40.0}}


def furnace_scene(rho: float = 0.5, emit: float = 1.0, light: bool = False, mirror: bool = True) -> dict:
    """A closed box in which every surface has albedo rho and emits radiance ``emit`` (with ``light``, also an NEE light
    rectangle like the Cornell one with the same albedo and emission), plus a mirror sphere of reflectance rho that
    also emits.  The rendering equation's solution is L = emit / (1 - rho) everywhere, and its Neumann series term k is
    emit rho^k: an exact answer for every bounce image."""
    g = (rho, rho, rho)
    e = (emit, emit, emit)
    rects = [_rect(1, 0.0, (0, 0), (1, 1), +1, g, e), _rect(1, 1.0, (0, 0), (1, 1), -1, g, e),
             _rect(2, 1.0, (0, 0), (1, 1), -1, g, e), _rect(2, 0.0, (0, 0), (1, 1), +1, g, e),
             _rect(0, 0.0, (0, 0), (1, 1), +1, g, e), _rect(0, 1.0, (0, 0), (1, 1), -1, g, e)]
    if light:
        rects.append(_rect(1, 0.9999, (0.375, 0.375), (0.625, 0.625), -1, g, e))
    sph = [{"center": (0.4, 0.3, 0.55), "radius": 0.2, "albedo": g, "mirror": True, "emit": e}] if mirror else []
    return {"rects": rects, "spheres": sph, "light": 6 if light else -1,
            "camera": {"eye": (0.5, 0.5, 0.02), "look": (0.5, 0.45, 1.0), "fov_deg": 70.0}}


def _pack(scene):
    R = scene["rects"]
    S = scene["spheres"]
    f = lambda key, src, w: np.array([x[key] for x in src], float).reshape(len(src), w)
    sph = np.array([list(s["center"]) + [s["radius"]] for s in S], float).reshape(len(S), 4)
    return (np.array([r["axis"] for r in R], np.int64), np.array([r["pos"] for r in R], float), f("lo", R, 2),
            f("hi", R, 2), np.array([r["sign"] for r in R], float), f("albedo", R, 3), f("emit", R, 3),
            sph, f("albedo", S, 3), f("emit", S, 3), np.array([s["mirror"] for s in S], np.bool_).reshape(len(S)),
            int(scene["light"]))


def _camera(cam, W, H):
    eye, look = np.asarray(cam["eye"], float), np.asarray(cam["look"], float)
    fw = (look - eye) / np.linalg.norm(look - eye)
    rt = np.cross([0, 1.0, 0], fw)
    rt /= np.linalg.norm(rt)
    up = np.cross(fw, rt)
    return eye, fw, rt, up, math.tan(math.radians(cam["fov_deg"]) / 2)


# ---------------------------------------------------------------- the path tracer (numba)

@njit(cache=True)
def _hit(ox, oy, oz, dx, dy, dz, tmax, ra, rp, rlo, rhi, sph):
    """Nearest intersection before tmax with the rectangles and spheres (d is unit): (t, object index or -1);
    rectangles are 0 .. m-1 and spheres m ...  Sphere: t = -b -+ sqrt(b^2 - c) with b = d.(o - c),
    c = |o - c|^2 - r^2."""
    best = tmax
    obj = -1
    m = ra.shape[0]
    for i in range(m):
        a = ra[i]
        if a == 0:
            oa, da = ox, dx
        elif a == 1:
            oa, da = oy, dy
        else:
            oa, da = oz, dz
        if da == 0.0:
            continue
        t = (rp[i] - oa) / da
        if t <= EPS or t >= best:
            continue
        if a == 0:
            u, v = oy + t * dy, oz + t * dz
        elif a == 1:
            u, v = ox + t * dx, oz + t * dz
        else:
            u, v = ox + t * dx, oy + t * dy
        if u < rlo[i, 0] or u > rhi[i, 0] or v < rlo[i, 1] or v > rhi[i, 1]:
            continue
        best = t
        obj = i
    for j in range(sph.shape[0]):
        lx, ly, lz = ox - sph[j, 0], oy - sph[j, 1], oz - sph[j, 2]
        b = lx * dx + ly * dy + lz * dz
        c = lx * lx + ly * ly + lz * lz - sph[j, 3] * sph[j, 3]
        disc = b * b - c
        if disc < 0.0:
            continue
        sq = math.sqrt(disc)
        t = -b - sq
        if t <= EPS:
            t = -b + sq
        if t <= EPS or t >= best:
            continue
        best = t
        obj = m + j
    return best, obj


@njit(cache=True)
def _onb(nx, ny, nz):
    """Orthonormal basis completing n (Duff et al. 2017)."""
    s = 1.0 if nz >= 0.0 else -1.0
    a = -1.0 / (s + nz)
    b = nx * ny * a
    return 1.0 + s * nx * nx * a, s * b, -s * nx, b, s + ny * ny * a, -ny


@njit(cache=True)
def _kernel(W, H, spp, seed, eye, fw, rt, up, tan_half, nee, cosine, rr, rr_start, max_depth,
            ra, rp, rlo, rhi, rsign, ralb, remit, sph, salb, semit, smirror, light, out, gbn, gba, gbp, stats):
    np.random.seed(seed)
    m = ra.shape[0]
    B = out.shape[0]
    aspect = W / H
    inv = 1.0 / spp
    for py in range(H):
        for px in range(W):
            for s in range(spp):
                sx = (2.0 * (px + np.random.random()) / W - 1.0) * tan_half * aspect
                sy = (1.0 - 2.0 * (py + np.random.random()) / H) * tan_half
                dx = fw[0] + sx * rt[0] + sy * up[0]
                dy = fw[1] + sx * rt[1] + sy * up[1]
                dz = fw[2] + sx * rt[2] + sy * up[2]
                ln = math.sqrt(dx * dx + dy * dy + dz * dz)
                dx, dy, dz = dx / ln, dy / ln, dz / ln
                ox, oy, oz = eye[0], eye[1], eye[2]
                tr, tg, tb = 1.0, 1.0, 1.0
                depth = 0
                spec = True
                segs = 0
                gdone = False
                while True:
                    t, obj = _hit(ox, oy, oz, dx, dy, dz, 1e30, ra, rp, rlo, rhi, sph)
                    segs += 1
                    if obj < 0:
                        break
                    hx, hy, hz = ox + t * dx, oy + t * dy, oz + t * dz
                    if obj < m:
                        a = ra[obj]
                        nx = rsign[obj] if a == 0 else 0.0
                        ny = rsign[obj] if a == 1 else 0.0
                        nz = rsign[obj] if a == 2 else 0.0
                        ar, ag, ab = ralb[obj, 0], ralb[obj, 1], ralb[obj, 2]
                        er, eg, eb = remit[obj, 0], remit[obj, 1], remit[obj, 2]
                        mir = False
                        emits = nx * dx + ny * dy + nz * dz < 0.0  # one-sided: only the front lights
                    else:
                        j = obj - m
                        r = sph[j, 3]
                        nx, ny, nz = (hx - sph[j, 0]) / r, (hy - sph[j, 1]) / r, (hz - sph[j, 2]) / r
                        ar, ag, ab = salb[j, 0], salb[j, 1], salb[j, 2]
                        er, eg, eb = semit[j, 0], semit[j, 1], semit[j, 2]
                        mir = smirror[j]
                        emits = True
                    if nx * dx + ny * dy + nz * dz > 0.0:  # shade on the side the ray came from
                        nx, ny, nz = -nx, -ny, -nz
                    if not gdone and not mir:  # g-buffer: the first non-mirror hit, seen through any mirrors
                        gdone = True
                        if ar + ag + ab > 0.0:
                            gr, gg, gb = tr * ar, tg * ag, tb * ab
                        else:  # an emitter: albedo 1, so demodulation leaves its radiance alone
                            gr, gg, gb = tr, tg, tb
                        gbn[py, px, 0] += nx * inv
                        gbn[py, px, 1] += ny * inv
                        gbn[py, px, 2] += nz * inv
                        gba[py, px, 0] += gr * inv
                        gba[py, px, 1] += gg * inv
                        gba[py, px, 2] += gb * inv
                        gbp[py, px, 0] += hx * inv
                        gbp[py, px, 1] += hy * inv
                        gbp[py, px, 2] += hz * inv
                    if emits and er + eg + eb > 0.0 and ((not nee) or depth == 0 or spec or obj != light):
                        k = depth if depth < B else B - 1
                        out[k, py, px, 0] += tr * er * inv
                        out[k, py, px, 1] += tg * eg * inv
                        out[k, py, px, 2] += tb * eb * inv
                    if depth >= max_depth or ar + ag + ab <= 0.0:
                        break
                    if mir:
                        dn = dx * nx + dy * ny + dz * nz
                        dx, dy, dz = dx - 2 * dn * nx, dy - 2 * dn * ny, dz - 2 * dn * nz
                        tr, tg, tb = tr * ar, tg * ag, tb * ab
                        spec = True
                    else:
                        if nee and light >= 0:
                            la = ra[light]
                            u = rlo[light, 0] + np.random.random() * (rhi[light, 0] - rlo[light, 0])
                            v = rlo[light, 1] + np.random.random() * (rhi[light, 1] - rlo[light, 1])
                            if la == 0:
                                qx, qy, qz = rp[light], u, v
                            elif la == 1:
                                qx, qy, qz = u, rp[light], v
                            else:
                                qx, qy, qz = u, v, rp[light]
                            lx, ly, lz = qx - hx, qy - hy, qz - hz
                            d2 = lx * lx + ly * ly + lz * lz
                            dist = math.sqrt(d2)
                            lx, ly, lz = lx / dist, ly / dist, lz / dist
                            cs = nx * lx + ny * ly + nz * lz
                            cl = -rsign[light] * (lx if la == 0 else (ly if la == 1 else lz))
                            if cs > 0.0 and cl > 0.0:
                                stats[1] += 1
                                t2, o2 = _hit(hx + OFF * nx, hy + OFF * ny, hz + OFF * nz, lx, ly, lz, dist - 1e-5,
                                              ra, rp, rlo, rhi, sph)
                                if o2 < 0:
                                    area = (rhi[light, 0] - rlo[light, 0]) * (rhi[light, 1] - rlo[light, 1])
                                    g = cs * cl / d2 * area / math.pi
                                    k = depth + 1 if depth + 1 < B else B - 1
                                    out[k, py, px, 0] += tr * ar * remit[light, 0] * g * inv
                                    out[k, py, px, 1] += tg * ag * remit[light, 1] * g * inv
                                    out[k, py, px, 2] += tb * ab * remit[light, 2] * g * inv
                        u1, u2 = np.random.random(), np.random.random()
                        phi = 2.0 * math.pi * u2
                        if cosine:  # Malley: pdf cos / pi, throughput *= rho
                            rad = math.sqrt(u1)
                            cz = math.sqrt(max(0.0, 1.0 - u1))
                            wgt = 1.0
                        else:  # uniform: pdf 1 / 2 pi, throughput *= 2 rho cos
                            cz = u1
                            rad = math.sqrt(max(0.0, 1.0 - u1 * u1))
                            wgt = 2.0 * cz
                        lxx, lxy = rad * math.cos(phi), rad * math.sin(phi)
                        t1x, t1y, t1z, b1x, b1y, b1z = _onb(nx, ny, nz)
                        dx = lxx * t1x + lxy * b1x + cz * nx
                        dy = lxx * t1y + lxy * b1y + cz * ny
                        dz = lxx * t1z + lxy * b1z + cz * nz
                        tr, tg, tb = tr * ar * wgt, tg * ag * wgt, tb * ab * wgt
                        spec = False
                    depth += 1
                    ox, oy, oz = hx + OFF * nx, hy + OFF * ny, hz + OFF * nz
                    if rr and depth >= rr_start:
                        q = max(tr, max(tg, tb))
                        if q > 0.95:
                            q = 0.95
                        if np.random.random() >= q:
                            break
                        tr, tg, tb = tr / q, tg / q, tb / q
                stats[0] += segs
                stats[2] += 1
                stats[3] += depth


def render(spp: int = 16, W: int = 128, H: int = 128, seed: int = 0, nee: bool = True, cosine: bool = True,
           roulette: bool = True, rr_start: int = 3, max_depth: int = 32, bins: int = 8,
           scene: dict | None = None) -> dict:
    """Path-trace ``scene`` (default the series' Cornell scene) at ``spp`` jittered samples per pixel.  Returns
    image (H x W x 3 linear radiance, the sum of the bounce images), bounces (bins x H x W x 3: light that reflected
    k times, the last bin holding k >= bins - 1), bounce_mean (the mean radiance of each bounce image), gbuffer
    (normal, albedo and position of the first non-mirror hit, seen through any mirrors with the mirror reflectance
    folded into the albedo, albedo 1 for an emitter; averaged over the pixel), mean_path_length (rays per camera path),
    mean_bounces (scattering events per path), shadow_rays, paths and seconds.  Paths are capped at ``max_depth``
    reflections with or without roulette, so the two estimate the same quantity."""
    sc = scene or cornell_scene()
    eye, fw, rt, up, th = _camera(sc["camera"], W, H)
    out = np.zeros((bins, H, W, 3))
    gbn, gba, gbp = np.zeros((H, W, 3)), np.zeros((H, W, 3)), np.zeros((H, W, 3))
    stats = np.zeros(4, np.int64)
    t0 = time.perf_counter()
    _kernel(W, H, spp, seed, eye, fw, rt, up, th, nee, cosine, roulette, rr_start, max_depth, *_pack(sc), out, gbn, gba,
            gbp, stats)
    secs = time.perf_counter() - t0
    return {"image": out.sum(0), "bounces": out, "bounce_mean": out.mean((1, 2, 3)).tolist(),
            "gbuffer": {"normal": gbn, "albedo": gba, "position": gbp}, "spp": spp, "W": W, "H": H,
            "mean_path_length": float(stats[0] / stats[2]), "mean_bounces": float(stats[3] / stats[2]),
            "shadow_rays": int(stats[1]), "paths": int(stats[2]), "seconds": secs}


def warm():
    """Compile the kernel (once per machine with numba's cache) so timings exclude compilation."""
    render(1, 4, 4)


def reference(spp: int = 2048, W: int = 128, H: int = 128, seed: int = 987654) -> dict:
    """The converged image everything is measured against (about 30 s at 128 x 128 x 2048 on one core)."""
    warm()
    return render(spp, W, H, seed)


def rmse(a, b, mask=None) -> float:
    """Root-mean-square difference over pixels and channels (over the pixels where ``mask`` is true, if given)."""
    d2 = ((np.asarray(a) - np.asarray(b)) ** 2).mean(-1)
    return float(np.sqrt(d2[mask].mean() if mask is not None else d2.mean()))


def _ref(ref, W, H):
    """(reference image, surface mask).  The mask keeps the pixels that do not show the light, directly or in the
    mirror (reference radiance below 1 in every channel; lit surfaces stay below about 0.5, the light is 10 to 17):
    a pixel on the light's edge is part light, part ceiling, and that anti-aliasing noise, which no sampling strategy
    or filter changes, would otherwise dominate the RMSE."""
    if ref is None:
        ref = reference(W=W, H=H)
    R = ref["image"] if isinstance(ref, dict) else np.asarray(ref)
    return R, R.max(-1) < 1.0


def _errors(img, R, mask):
    m = float(R.mean())
    ms = float(R[mask].mean())
    return {"rmse": rmse(img, R), "rel_rmse": rmse(img, R) / m, "rmse_surfaces": rmse(img, R, mask),
            "rel_rmse_surfaces": rmse(img, R, mask) / ms}


def convergence(spps=(1, 4, 16, 64, 256), ref=None, W: int = 128, H: int = 128, seed: int = 1) -> dict:
    """RMSE against the reference at each spp (rmse, rel_rmse over all pixels; rmse_surfaces, rel_rmse_surfaces over
    the pixels that do not show the light, see _ref) and the least-squares slopes of log RMSE on log spp (slope,
    slope_surfaces; Monte Carlo predicts -1/2, so 4x the samples halves the noise).  ``ref`` is a render() result or
    its image, computed if None.  The reference's own noise (RMSE about
    rmse(1) / sqrt(2048)) flattens the last point slightly."""
    warm()
    R, mask = _ref(ref, W, H)
    rows = []
    for k, n in enumerate(spps):
        r = render(n, W, H, seed + 1000 * k)
        rows.append({"spp": n, **_errors(r["image"], R, mask), "seconds": r["seconds"]})
    x = np.log([r["spp"] for r in rows])
    out = {"rows": rows, "ref_mean": float(R.mean())}
    for key in ("rmse", "rmse_surfaces"):
        out["slope" + key[4:]] = float(np.polyfit(x, np.log([r[key] for r in rows]), 1)[0])
    return out


def sampling_comparison(spp: int = 16, ref=None, W: int = 128, H: int = 128, seed: int = 2) -> list[dict]:
    """At equal spp: cosine-weighted against uniform hemisphere sampling, each with and without next-event estimation.
    Rows of name, cosine, nee, rmse, rel_rmse (and the _surfaces versions, see _ref), seconds, mean_path_length and
    efficiency 1 / (rmse_surfaces^2 seconds) relative to the first row."""
    warm()
    R, mask = _ref(ref, W, H)
    rows = []
    for name, cos, nee in (("cosine + NEE", True, True), ("uniform + NEE", False, True),
                           ("cosine, no NEE", True, False), ("uniform, no NEE", False, False)):
        r = render(spp, W, H, seed, nee=nee, cosine=cos)
        rows.append({"name": name, "cosine": cos, "nee": nee, **_errors(r["image"], R, mask), "seconds": r["seconds"],
                     "mean_path_length": r["mean_path_length"]})
    for r in rows:  # efficiency = 1 / (variance x time), relative to the first row
        r["efficiency"] = rows[0]["rmse_surfaces"] ** 2 * rows[0]["seconds"] / (r["rmse_surfaces"] ** 2 * r["seconds"])
    return rows


def roulette_check(renders: int = 12, spp: int = 16, W: int = 64, H: int = 64, rr_start: int = 3,
                   seed: int = 3) -> dict:
    """``renders`` independent renders with and without Russian roulette (same cap of 32 reflections).  Their mean
    images agree within noise: the difference of the image means in standard errors (z), and the RMS over pixels of
    the per-pixel z-scores (about 1 when the only difference is noise).  Also the mean path length and time of each."""
    warm()
    res = {}
    for rr in (True, False):
        imgs, lengths, secs = [], [], 0.0
        for k in range(renders):
            r = render(spp, W, H, seed + 7919 * k + (0 if rr else 104729), roulette=rr, rr_start=rr_start)
            imgs.append(r["image"])
            lengths.append(r["mean_path_length"])
            secs += r["seconds"]
        A = np.stack(imgs)
        means = A.mean((1, 2, 3))
        res[rr] = {"mean": float(means.mean()), "se": float(means.std(ddof=1) / math.sqrt(renders)),
                   "pix_mean": A.mean(0), "pix_var": A.var(0, ddof=1) / renders,
                   "mean_path_length": float(np.mean(lengths)), "seconds": secs}
    a, b = res[True], res[False]
    z = (a["mean"] - b["mean"]) / math.sqrt(a["se"] ** 2 + b["se"] ** 2)
    pz = (a["pix_mean"] - b["pix_mean"]) / np.sqrt(a["pix_var"] + b["pix_var"] + 1e-30)
    return {"mean_rr": a["mean"], "se_rr": a["se"], "mean_no_rr": b["mean"], "se_no_rr": b["se"], "z": float(z),
            "pixel_z_rms": float(np.sqrt(np.mean(pz ** 2))), "path_length_rr": a["mean_path_length"],
            "path_length_no_rr": b["mean_path_length"], "seconds_rr": a["seconds"], "seconds_no_rr": b["seconds"],
            "saved": 1 - a["mean_path_length"] / b["mean_path_length"]}


# ---------------------------------------------------------------- denoising

B3 = np.array([1 / 16, 1 / 4, 3 / 8, 1 / 4, 1 / 16])


def denoise(image, gbuffer, iterations: int = 3, sigma_color: float = 30.0, sigma_normal: float = 0.3,
            sigma_albedo: float = 0.1, sigma_position: float = 0.1, demodulate: bool = True):
    """Edge-avoiding a-trous wavelet filter (Dammertz et al. 2010).  Iteration i convolves with the 5 x 5 B3-spline
    kernel h with holes (taps 2^i pixels apart), each tap weighted by h times the edge-stopping functions
    exp(-|c_p - c_q|^2 / sigma_c^2) exp(-|n_p - n_q|^2 / sigma_n^2) exp(-|a_p - a_q|^2 / sigma_a^2)
    exp(-|x_p - x_q|^2 / sigma_x^2) on colour, first-hit normal, albedo and position; sigma_c halves each iteration
    (2^-i) as in the paper.  With ``demodulate`` the filter runs on the image divided by the albedo (the
    illumination), and the albedo is multiplied back, so textures and wall colours stay sharp.  The colour sigma is
    relative to the median of the filtered signal.  The defaults were tuned on the series' scene at 16 spp: a tight
    colour sigma hurts there, because a firefly (a caustic path through the mirror) is unlike its neighbours and a
    tight colour weight keeps it; the g-buffer terms carry the edges.  Returns the filtered H x W x 3 image."""
    alb = np.asarray(gbuffer["albedo"], float)
    nrm = np.asarray(gbuffer["normal"], float)
    pos = np.asarray(gbuffer["position"], float)
    img = np.asarray(image, float)
    a = np.where(alb > 1e-3, alb, 1.0)
    c = img / a if demodulate else img.copy()
    sc = sigma_color * max(float(np.median(c)), 1e-12)
    H, W = c.shape[:2]
    for i in range(iterations):
        step = 2 ** i
        pad = 2 * step
        P = lambda x: np.pad(x, ((pad, pad), (pad, pad), (0, 0)), mode="edge")
        cp, np_, ap, xp = P(c), P(nrm), P(alb), P(pos)
        acc = np.zeros_like(c)
        wsum = np.zeros(c.shape[:2])
        s2 = (sc * 2.0 ** -i) ** 2
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                sl = (slice(pad + dy * step, pad + dy * step + H), slice(pad + dx * step, pad + dx * step + W))
                cq, nq, aq, xq = cp[sl], np_[sl], ap[sl], xp[sl]
                w = B3[dy + 2] * B3[dx + 2] * np.exp(
                    -((c - cq) ** 2).sum(-1) / s2 - ((nrm - nq) ** 2).sum(-1) / sigma_normal ** 2
                    - ((alb - aq) ** 2).sum(-1) / sigma_albedo ** 2 - ((pos - xq) ** 2).sum(-1) / sigma_position ** 2)
                acc += w[..., None] * cq
                wsum += w
        c = acc / wsum[..., None]
    return c * a if demodulate else c


def denoise_experiment(spp: int = 16, ref=None, W: int = 128, H: int = 128, seed: int = 4, **kw) -> dict:
    """Render at ``spp``, filter with denoise(), and compare with the reference: rmse_before, rmse_after, the relative
    versions and the _surfaces versions (see _ref; the filter cannot remove the light's anti-aliasing noise), the
    filter time, plus the noisy and denoised images and the g-buffer for display."""
    warm()
    R, mask = _ref(ref, W, H)
    r = render(spp, W, H, seed)
    t0 = time.perf_counter()
    d = denoise(r["image"], r["gbuffer"], **kw)
    secs = time.perf_counter() - t0
    before, after = _errors(r["image"], R, mask), _errors(d, R, mask)
    return {"spp": spp, **{k + "_before": v for k, v in before.items()}, **{k + "_after": v for k, v in after.items()},
            "filter_seconds": secs, "noisy": r["image"], "denoised": d, "gbuffer": r["gbuffer"]}


# ---------------------------------------------------------------- display

def to_srgb8(image, exposure: float = 1.0, curve: str = "reinhard") -> np.ndarray:
    """Linear radiance to 8-bit sRGB: scale by ``exposure``, compress with Reinhard x / (1 + x) (``curve="reinhard"``)
    or clip to [0, 1] (``"clip"``), then apply the sRGB transfer function (12.92 x below 0.0031308, else
    1.055 x^(1/2.4) - 0.055; IEC 61966-2-1).  Returns an H x W x 3 uint8 array."""
    x = np.asarray(image, float) * exposure
    x = x / (1 + x) if curve == "reinhard" else x
    x = np.clip(x, 0, 1)
    s = np.where(x <= 0.0031308, 12.92 * x, 1.055 * np.power(x, 1 / 2.4) - 0.055)
    return np.round(s * 255).astype(np.uint8)
