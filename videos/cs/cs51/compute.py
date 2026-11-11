"""Precompute everything numerical in Part 51 of *Computer Science, Built* ("Light and Pixels").

    python -m videos.cs.cs51.compute              # everything missing
    python -m videos.cs.cs51.compute --force path

Results are cached in ``.cache/cs51/<name>.json`` with images in ``<name>.npz`` (8-bit sRGB or grey); scenes call
``load(name)``.  The instruments are in ``explainer/cs/graphics/`` (transform, raster, curves, ray, brdf, path);
tests in tests/test_cs51_raster.py and tests/test_cs51_light.py.

Items:
    order       composition order: rotate then translate against translate then rotate
    frustum     the frustum's corners and their interpolation into the NDC cube
    depth       depth precision: resolvable distance by near plane and bits; z-fighting counts and masks
    gimbal      the Euler map's singular values as pitch nears 90 degrees
    slerp       slerp against linear Euler interpolation: angle per step, path on the sphere
    bary        a triangle coloured by its barycentric coordinates
    persp       affine against perspective-correct texture interpolation, against ray-cast truth
    shading     Lambert, Phong, Blinn-Phong; Gouraud against Phong; the exact sphere
    texture     point sampling, trilinear mipmaps and 16x supersampling against a reference
    zbuffer     the z-buffer against the painter's algorithm
    casteljau   de Casteljau's construction of a cubic at several t
    bspline     a uniform cubic B-spline's continuity at its knots
    subdiv      Catmull-Clark on a cube: counts and vertices by level
    bvh         triangle tests per ray: brute force, median-split and SAH BVHs, n = 100 to 100,000
    whitted     a Whitted ray-traced image and its ray counts
    furnace     white-furnace albedos of Lambert, Phong, Blinn-Phong and GGX
    mis         light, BRDF and multiple importance sampling across lobe widths and light sizes
    path        the path tracer: images at 1 to 256 spp, the reference, the bounces, convergence
    sampling    cosine against uniform sampling, with and without next-event estimation
    roulette    Russian roulette: unbiased, and how much it saves
    denoise     an a-trous denoiser at 16 spp against 256 spp
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("cs51")
load = CACHE.load


def _u8(img, srgb=False):
    a = np.asarray(img, float)
    if srgb:
        from explainer.cs.graphics.path import to_srgb8
        return to_srgb8(a)
    return (np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8)


def _split(d: dict, images=(), prefix="") -> dict:
    """Lift numpy arrays to top-level keys (the cache stores top-level arrays in the .npz); images become uint8."""
    out = {}
    for k, v in d.items():
        key = f"{prefix}{k}"
        if isinstance(v, np.ndarray):
            if k in images or v.ndim >= 2:
                out[key] = _u8(v) if v.dtype != np.uint8 and v.ndim >= 2 and v.max() <= 1.0 + 1e-6 else v
            else:
                out[key] = v.tolist()
        elif isinstance(v, dict):
            sub = _split(v, images, prefix=f"{key}_")
            arrays = {kk: vv for kk, vv in sub.items() if isinstance(vv, np.ndarray)}
            out.update(arrays)
            out[key] = {kk[len(key) + 1:]: vv for kk, vv in sub.items() if not isinstance(vv, np.ndarray)}
        elif isinstance(v, (list, tuple)) and v and isinstance(v[0], dict):
            out[key] = [_split(x) if not any(isinstance(y, np.ndarray) for y in x.values()) else
                        {kk: (vv.tolist() if isinstance(vv, np.ndarray) else vv) for kk, vv in x.items()} for x in v]
        elif isinstance(v, (np.floating, np.integer, np.bool_)):
            out[key] = v.item()
        else:
            out[key] = v
    return out


def _T():
    from explainer.cs.graphics import transform
    return transform


def _R():
    from explainer.cs.graphics import raster
    return raster


def compute_order() -> dict:
    return _split(_T().composition_order_demo())


def compute_frustum() -> dict:
    return _split(_T().frustum_to_cube())


def compute_depth() -> dict:
    T = _T()
    zf = T.z_fighting_table()
    return {"table": _split({"rows": T.depth_table()})["rows"], "curve": _split(T.depth_curve(0.1, 1000, 200)),
            "fighting": [{k: (v.tolist() if isinstance(v, np.ndarray) and v.ndim < 2 else v) for k, v in r.items()
                          if not (isinstance(v, np.ndarray) and v.ndim >= 2)} for r in zf]}


def compute_gimbal() -> dict:
    return _split({"rows": _T().gimbal_lock()})


def compute_slerp() -> dict:
    return _split(_T().slerp_vs_euler())


def compute_bary() -> dict:
    return _split(_R().barycentric_demo())


def compute_persp() -> dict:
    return _split(_R().perspective_correct_demo())


def compute_shading() -> dict:
    return _split(_R().shading_demo())


def compute_texture() -> dict:
    return _split(_R().texture_demo())


def compute_zbuffer() -> dict:
    return _split(_R().zbuffer_demo())


def compute_casteljau() -> dict:
    from explainer.cs.graphics import curves as C
    P = [(0.0, 0.0), (1.0, 2.0), (3.0, 2.2), (4.0, 0.2)]
    return {"points": P, "steps": [_split(C.de_casteljau(P, t)) for t in (0.25, 0.5, 0.75)],
            "curve": np.asarray(C.bezier(P, np.linspace(0, 1, 60))).tolist()}


def compute_bspline() -> dict:
    from explainer.cs.graphics import curves as C
    return {"rows": [_split(r) for r in C.bspline_continuity()]}


def compute_subdiv() -> dict:
    from explainer.cs.graphics import curves as C
    return _split(C.catmull_clark(levels=4))


def compute_bvh() -> dict:
    from explainer.cs.graphics import ray
    return {"rows": [_split(r) for r in ray.bvh_experiment()]}


def compute_whitted() -> dict:
    from explainer.cs.graphics import ray
    r = ray.whitted()
    r["image"] = _u8(r["image"], srgb=True)
    return _split(r)


def compute_furnace() -> dict:
    from explainer.cs.graphics import brdf
    return {"rows": [_split(r) for r in brdf.white_furnace()], "reciprocity": _split(brdf.reciprocity()),
            "pdfs": _split(brdf.pdf_integrals())}


def compute_mis() -> dict:
    from explainer.cs.graphics import brdf
    return {"rows": [_split(r) for r in brdf.mis_experiment()]}


def compute_path() -> dict:
    from explainer.cs.graphics import path as P
    ref = P.reference()
    out = {"reference": _u8(ref["image"], srgb=True)}
    for spp in (1, 4, 16, 64, 256):
        r = P.render(spp=spp, seed=100 + spp)
        out[f"spp{spp}"] = _u8(r["image"], srgb=True)
    for k in range(ref["bounces"].shape[0]):
        out[f"bounce{k}"] = _u8(ref["bounces"][k], srgb=True)
    out["bounce_mean"] = np.asarray(ref["bounce_mean"]).tolist()
    out["mean_path_length"] = float(ref["mean_path_length"])
    out["convergence"] = _split(P.convergence(ref=ref))
    return out


def compute_sampling() -> dict:
    from explainer.cs.graphics import path as P
    return {"rows": [_split(r) for r in P.sampling_comparison()]}


def compute_roulette() -> dict:
    from explainer.cs.graphics import path as P
    return _split(P.roulette_check())


def compute_denoise() -> dict:
    from explainer.cs.graphics import path as P
    r = P.denoise_experiment()
    r["noisy"] = _u8(r["noisy"], srgb=True)
    r["denoised"] = _u8(r["denoised"], srgb=True)
    r.pop("gbuffer", None)
    return _split(r)


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
