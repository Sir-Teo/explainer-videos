"""Our rasterizer (Part 51): edge functions, barycentric coordinates, a top-left fill rule, perspective-correct
interpolation and a z-buffer, and the demos built on it: why attributes must be interpolated as a / w and 1 / w,
Lambert, Phong and Blinn-Phong lighting with Gouraud against Phong shading, texture aliasing against mipmaps and
supersampling, and the z-buffer against the painter's algorithm.

Sources.  Edge functions: Pineda, "A parallel algorithm for polygon rasterization" (SIGGRAPH 1988); the edge function
is Part 22's orientation determinant (``explainer.cs.algo.geometry.orient_float``).  Fill rule, barycentrics and
perspective-correct interpolation: Marschner and Shirley, *Fundamentals of Computer Graphics* ch. 8 and 9; Pharr,
Jakob and Humphreys, *Physically Based Rendering* (4th ed.); the top-left rule is Direct3D's.  Z-buffer: Catmull,
*A Subdivision Algorithm for Computer Display of Curved Surfaces* (1974).  Lighting: Lambert's cosine law; Phong,
"Illumination for computer generated pictures" (1975); Blinn, "Models of light reflection" (1977); Gouraud,
"Continuous shading of curved surfaces" (1971).  Mipmaps and trilinear filtering: Williams, "Pyramidal
parametrics" (1983), with the level of detail lambda = log2 rho of the OpenGL specification (sec. 8.14).

Conventions.  Clip space is OpenGL's (``transform.perspective``); triangles are clipped against the near plane
z = -w in homogeneous space (Sutherland-Hodgman), divided by w, and mapped to the screen with y down: pixel (i, j)
has its centre at (i + 0.5, j + 0.5).  Coverage uses vertex positions snapped to 1/256 pixel, as GPUs do, so the
edge functions are exact and two triangles that share an edge never both own, or both miss, a pixel on it;
attributes and depth use the unsnapped barycentrics.  Window depth is (z_ndc + 1) / 2, the buffer is cleared to 1
and the test is GL_LESS.
"""

from __future__ import annotations

import math

import numpy as np

from explainer.cs.graphics import transform as T

SUBPIXEL = 256

# --------------------------------------------------------------------------------------------------- edge functions


def edge(a, b, p):
    """The edge function E_ab(p) = (b - a) x (p - a): twice the signed area of (a, b, p), the orientation test of
    Part 22.  Affine in p, so a rasterizer can step it by adding constants.  Works on arrays of p."""
    return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])


def barycentric(a, b, c, p):
    """(l0, l1, l2) with p = l0 a + l1 b + l2 c and l0 + l1 + l2 = 1: each is a sub-triangle's area over the whole's,
    l0 = E_bc(p) / E_ab(c) and so on."""
    area = edge(a, b, c)
    return edge(b, c, p) / area, edge(c, a, p) / area, edge(a, b, p) / area


def is_top_left(a, b) -> bool:
    """The top-left rule for an edge a -> b of a triangle whose interior has E > 0, with y pointing down: the inward
    normal of the edge is (-dy, dx), so a left edge has dy < 0 and a top edge has dy = 0 and dx > 0.  Pixel centres
    exactly on a top or left edge belong to the triangle; on any other edge, to its neighbour."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    return dy < 0 or (dy == 0 and dx > 0)


def _snap(v):
    return np.round(np.asarray(v, float) * SUBPIXEL) / SUBPIXEL


def _bbox(xs, ys, W, H):
    i0 = max(0, math.ceil(min(xs) - 0.5))
    i1 = min(W - 1, math.floor(max(xs) - 0.5))
    j0 = max(0, math.ceil(min(ys) - 0.5))
    j1 = min(H - 1, math.floor(max(ys) - 0.5))
    return i0, i1, j0, j1


def coverage(v0, v1, v2, W: int, H: int):
    """The pixels a screen-space triangle owns: pixel centres inside all three (snapped) edge functions, ties settled
    by the top-left rule.  Returns (mask, (i0, i1, j0, j1)) over the clipped bounding box, or (None, None) for a
    degenerate or off-screen triangle.  Either winding is accepted."""
    a, b, c = _snap(v0), _snap(v1), _snap(v2)
    area = edge(a, b, c)
    if area == 0:
        return None, None
    if area < 0:
        b, c = c, b
    i0, i1, j0, j1 = _bbox((a[0], b[0], c[0]), (a[1], b[1], c[1]), W, H)
    if i0 > i1 or j0 > j1:
        return None, None
    px, py = np.meshgrid(np.arange(i0, i1 + 1) + 0.5, np.arange(j0, j1 + 1) + 0.5)
    m = np.ones(px.shape, bool)
    for (s, t) in ((b, c), (c, a), (a, b)):
        E = edge(s, t, (px, py))
        m &= (E > 0) | ((E == 0) & is_top_left(s, t))
    return m, (i0, i1, j0, j1)


# --------------------------------------------------------------------------------------------------- the rasterizer


def clip_near(clip, attr):
    """Sutherland-Hodgman against the near plane z >= -w in homogeneous space; attributes are interpolated linearly
    there, which is correct because clip space is linear in the eye-space position.  Returns a list of triangles."""
    clip, attr = np.asarray(clip, float), np.asarray(attr, float)
    s = clip[:, 2] + clip[:, 3]
    if (s >= 0).all():
        return [(clip, attr)]
    if (s < 0).all():
        return []
    P, A = [], []
    for i in range(3):
        j = (i + 1) % 3
        if s[i] >= 0:
            P.append(clip[i])
            A.append(attr[i])
        if (s[i] >= 0) != (s[j] >= 0):
            t = s[i] / (s[i] - s[j])
            P.append(clip[i] + t * (clip[j] - clip[i]))
            A.append(attr[i] + t * (attr[j] - attr[i]))
    return [(np.array([P[0], P[k], P[k + 1]]), np.array([A[0], A[k], A[k + 1]])) for k in range(1, len(P) - 1)]


def rasterize(triangles, W: int, H: int, perspective_correct: bool = True, depth_test: bool = True,
              cull_backfaces: bool = False, background=(0.0, 0.0, 0.0)) -> dict:
    """Rasterize ``triangles``, each a dict with ``clip`` (3 x 4 clip-space vertices x, y, z, w) and ``attr`` (3 x k
    per-vertex attributes, k >= 0; the first three are taken as the colour), in order.

    Per triangle: clip against the near plane, divide by w, map to the viewport, scan the bounding box with the edge
    functions, and for each covered pixel interpolate depth linearly in screen space (z_ndc is affine there) and the
    attributes either affinely, sum l_i a_i, or perspective-correctly, (sum l_i a_i / w_i) / (sum l_i / w_i), since
    a / w and 1 / w are what is affine in screen space.  The z-buffer keeps the nearest fragment (GL_LESS); with
    ``depth_test`` False later triangles simply overwrite (the painter's algorithm).

    Returns ``image`` (H x W x 3), ``depth`` (H x W, 1 where empty), ``attr`` (H x W x k, the surviving fragment's
    attributes), ``tri`` (H x W, index of the triangle that owns the pixel, -1 for none) and ``counters``: pixels
    ``tested`` (bounding-box pixels scanned), ``covered`` (inside the triangle), ``depth_pass``, ``depth_fail``,
    ``triangles`` drawn after clipping."""
    k = max((np.asarray(t.get("attr", np.zeros((3, 0)))).shape[1] for t in triangles), default=0)
    image = np.empty((H, W, 3))
    image[:] = background
    depth = np.ones((H, W))
    abuf = np.zeros((H, W, k))
    tri = np.full((H, W), -1, int)
    ctr = {"tested": 0, "covered": 0, "depth_pass": 0, "depth_fail": 0, "triangles": 0}
    for tid, t in enumerate(triangles):
        attr0 = np.asarray(t.get("attr", np.zeros((3, 0))), float).reshape(3, -1)
        attr0 = np.c_[attr0, np.zeros((3, k - attr0.shape[1]))]
        for C, A in clip_near(t["clip"], attr0):
            w = C[:, 3]
            ndc = C[:, :3] / w[:, None]
            sx, sy, z = (ndc[:, 0] + 1) * W / 2, (1 - ndc[:, 1]) * H / 2, (ndc[:, 2] + 1) / 2
            v = [(sx[i], sy[i]) for i in range(3)]
            area = edge(*v)
            if area == 0 or (cull_backfaces and area > 0):      # y down: counter-clockwise in NDC has area < 0
                continue
            m, box = coverage(*v, W, H)
            ctr["triangles"] += 1
            if m is None:
                continue
            i0, i1, j0, j1 = box
            ctr["tested"] += m.size
            ctr["covered"] += int(m.sum())
            px, py = np.meshgrid(np.arange(i0, i1 + 1) + 0.5, np.arange(j0, j1 + 1) + 0.5)
            l0, l1, l2 = barycentric(v[0], v[1], v[2], (px, py))
            zf = l0 * z[0] + l1 * z[1] + l2 * z[2]
            region = (slice(j0, j1 + 1), slice(i0, i1 + 1))
            if depth_test:
                ok = m & (zf < depth[region])
                ctr["depth_pass"] += int(ok.sum())
                ctr["depth_fail"] += int((m & ~ok).sum())
            else:
                ok = m
                ctr["depth_pass"] += int(ok.sum())
            if not ok.any():
                continue
            L = np.stack([l0[ok], l1[ok], l2[ok]], 1)
            if perspective_correct:
                L = L / w
                L = L / L.sum(1, keepdims=True)
            a = L @ A
            depth[region][ok] = zf[ok]
            abuf[region][ok] = a
            tri[region][ok] = tid
            if k >= 3:
                image[region][ok] = a[:, :3]
    return {"image": image, "depth": depth, "attr": abuf, "tri": tri, "counters": ctr}


def pixel_rays(W: int, H: int, fovy_deg: float, aspect: float, sx=None, sy=None):
    """Eye-space ray directions (x, y, -1) through screen points (default: the pixel centres), the inverse of the
    projection and viewport, for ray-cast ground truths."""
    if sx is None:
        sx, sy = np.meshgrid(np.arange(W) + 0.5, np.arange(H) + 0.5)
    t = math.tan(math.radians(fovy_deg) / 2)
    x = (2 * sx / W - 1) * t * aspect
    y = (1 - 2 * sy / H) * t
    return x, y, -np.ones_like(x)


def _tris(P, eye_vertices, faces, attrs):
    """Triangles for ``rasterize`` from eye-space vertices, index triples and per-vertex attributes (n x k)."""
    clip = T.apply_h(P, eye_vertices)
    attrs = np.asarray(attrs, float)
    return [{"clip": clip[list(f)], "attr": attrs[list(f)]} for f in faces]


# --------------------------------------------------------------------------------------------------- demos


def barycentric_demo(W: int = 160, H: int = 120) -> dict:
    """One triangle with red, green and blue corners: the colour at each pixel is its barycentric coordinates.
    Returns ``image``, ``counters`` and the screen-space ``vertices``."""
    P = T.perspective(60, W / H, 0.1, 100)
    V = [(-1.6, -1.1, -3), (1.7, -0.9, -3), (0.1, 1.4, -3)]
    r = rasterize(_tris(P, V, [(0, 1, 2)], np.eye(3)), W, H)
    ndc = T.apply(P, V)
    scr = [((x + 1) * W / 2, (1 - y) * H / 2) for x, y, _ in ndc]
    return {"image": r["image"], "counters": r["counters"], "vertices": [list(map(float, s)) for s in scr]}


CHECK_LIGHT, CHECK_DARK = (0.92, 0.92, 0.88), (0.16, 0.17, 0.22)
SKY = (0.05, 0.06, 0.09)
PHASE = (0.1234567, 0.2345678)      # checker offset, so no pixel centre lands exactly on a square's border


def _checker(u, v):
    return ((np.floor(u) + np.floor(v)) % 2).astype(int)


def _paint(label, mask, H, W):
    img = np.empty((H, W, 3))
    img[:] = SKY
    img[mask & (label == 0)] = CHECK_LIGHT
    img[mask & (label == 1)] = CHECK_DARK
    return img


def perspective_correct_demo(W: int = 160, H: int = 120, half_width: float = 1.5, z_near: float = 2.0,
                             z_far: float = 12.0, checks=(6, 8)) -> dict:
    """A checkerboard floor (y = -1 in eye space, |x| <= ``half_width``, z from -``z_near`` to -``z_far``), two
    triangles wholly in view of a 60 degree camera at the origin, textured with ``checks`` = (6, 8) squares across
    and along it: (u, v) runs from (0, 0) at the near-left corner to (6, 8) at the far-right one (plus ``PHASE``).  Rendered with affine interpolation of (u, v)
    (texture swims and bends along the diagonal), with perspective-correct interpolation of (u/w, v/w, 1/w), and by
    ray casting each pixel centre against the plane (the truth).  Returns the three images (``affine``,
    ``perspective``, ``truth``), the share of floor pixels each method colours wrongly (``wrong_affine``,
    ``wrong_perspective``), the floor pixel count, and ``uv_error_max`` (perspective-correct against ray cast)."""
    fov, asp = 60.0, W / H
    P = T.perspective(fov, asp, 0.1, 100)
    hw = half_width
    V = [(-hw, -1, -z_near), (hw, -1, -z_near), (hw, -1, -z_far), (-hw, -1, -z_far)]
    to_uv = lambda x, z: ((x + hw) / (2 * hw) * checks[0] + PHASE[0],
                          (-z - z_near) / (z_far - z_near) * checks[1] + PHASE[1])
    uv = [to_uv(x, z) for x, _, z in V]
    tris = _tris(P, V, [(0, 1, 2), (0, 2, 3)], uv)
    out = {}
    for name, pc in (("affine", False), ("perspective", True)):
        r = rasterize(tris, W, H, perspective_correct=pc)
        cov = r["tri"] >= 0
        out[name] = (_checker(r["attr"][..., 0], r["attr"][..., 1]), cov, r["attr"])
    dx, dy, dz = pixel_rays(W, H, fov, asp)
    with np.errstate(divide="ignore", invalid="ignore"):
        t = np.where(dy < 0, -1.0 / dy, np.inf)
    X, Z = t * dx, t * dz
    truth_cov = np.isfinite(t) & (np.abs(X) <= hw) & (Z <= -z_near) & (Z >= -z_far)
    Ut, Vt = to_uv(np.where(truth_cov, X, 0), np.where(truth_cov, Z, 0))
    truth = _checker(Ut, Vt)
    n = int(truth_cov.sum())
    res = {"floor_pixels": n, "truth": _paint(truth, truth_cov, H, W)}
    for name, (lab, cov, _) in out.items():
        res[name] = _paint(lab, cov, H, W)
        wrong = (cov != truth_cov) | (truth_cov & cov & (lab != truth))
        res["wrong_" + name] = float(wrong.sum() / n)
    lab, cov, A = out["perspective"]
    both = cov & truth_cov
    res["uv_error_max"] = float(max(np.abs(A[..., 0] - Ut)[both].max(), np.abs(A[..., 1] - Vt)[both].max()))
    return res


def lighting(P, N, light, eye=(0.0, 0.0, 0.0), kd=(0.25, 0.45, 0.85), ks: float = 0.7, ka: float = 0.05,
             shininess: float = 32.0, blinn_shininess: float | None = None) -> dict:
    """The local lighting terms at points P with unit normals N (arrays n x 3) for a white point light: ``ambient``,
    Lambert's ``diffuse`` kd max(0, N.L), ``phong`` ks max(0, R.V)^s with R = 2 (N.L) N - L, and ``blinn`` ks
    max(0, N.H)^s' with H = (L + V) / |L + V| and s' = 4 s by default (N.H ~ cos(theta / 2) where R.V = cos theta, so
    cos^4s(theta/2) ~ cos^s(theta) near the peak).  Specular terms are zero where N.L <= 0.  Colours n x 3."""
    P, N = np.atleast_2d(P), np.atleast_2d(N)
    sb = 4 * shininess if blinn_shininess is None else blinn_shininess
    L = np.asarray(light, float) - P
    L /= np.linalg.norm(L, axis=1, keepdims=True)
    V = np.asarray(eye, float) - P
    V /= np.linalg.norm(V, axis=1, keepdims=True)
    nl = np.sum(N * L, 1)
    R = 2 * nl[:, None] * N - L
    Hh = L + V
    Hh /= np.linalg.norm(Hh, axis=1, keepdims=True)
    lit = nl > 0
    kd = np.asarray(kd, float)
    diffuse = np.maximum(nl, 0)[:, None] * kd
    phong = np.where(lit, ks * np.maximum(np.sum(R * V, 1), 0) ** shininess, 0)[:, None] * np.ones(3)
    blinn = np.where(lit, ks * np.maximum(np.sum(N * Hh, 1), 0) ** sb, 0)[:, None] * np.ones(3)
    return {"ambient": ka * kd * np.ones_like(diffuse), "diffuse": diffuse, "phong": phong, "blinn": blinn}


def uv_sphere(n_lat: int = 10, n_lon: int = 20, radius: float = 1.0, centre=(0.0, 0.0, 0.0)):
    """A latitude-longitude sphere: vertices, unit normals and counter-clockwise (outward) index triples; 2 n_lon
    (n_lat - 1) triangles."""
    c = np.asarray(centre, float)
    V, N = [], []
    for i in range(n_lat + 1):
        th = math.pi * i / n_lat
        for j in range(n_lon):
            ph = 2 * math.pi * j / n_lon
            n = (math.sin(th) * math.cos(ph), math.cos(th), -math.sin(th) * math.sin(ph))
            N.append(n)
            V.append(c + radius * np.array(n))
    F = []
    idx = lambda i, j: i * n_lon + j % n_lon
    for i in range(n_lat):
        for j in range(n_lon):
            a, b, cc, d = idx(i, j), idx(i + 1, j), idx(i + 1, j + 1), idx(i, j + 1)
            if i > 0:
                F.append((a, b, d))
            if i < n_lat - 1:
                F.append((b, cc, d))
    return np.array(V), np.array(N), F


def shading_demo(W: int = 160, H: int = 120, n_lat: int = 10, n_lon: int = 20, light=(3.0, 3.0, 0.5),
                 shininess: float = 32.0) -> dict:
    """A coarse sphere (``uv_sphere``, 2 n_lon (n_lat - 1) triangles, radius 1 at eye-space (0, 0, -3.2)) lit by one
    point light.  Images: ``lambert`` (ambient + diffuse per pixel), ``phong`` and ``blinn_phong`` (per-pixel Phong
    shading: normals interpolated and renormalized), ``gouraud`` (the Phong model evaluated at the vertices and the
    colours interpolated), and ``truth`` (the exact sphere ray cast, Phong model per pixel).  Stats:
    ``max_diff_gouraud_phong`` (largest per-pixel channel difference) and where it is, the highlight peaks, and RMSE
    of Gouraud and of per-pixel Phong against the truth."""
    fov, asp = 40.0, W / H
    centre = np.array([0.0, 0.0, -3.2])
    V, N, F = uv_sphere(n_lat, n_lon, 1.0, centre)
    lv = lighting(V, N, light, shininess=shininess)
    gour = np.clip(lv["ambient"] + lv["diffuse"] + lv["phong"], 0, 1)
    P = T.perspective(fov, asp, 0.1, 100)
    r = rasterize(_tris(P, V, F, np.c_[gour, V, N]), W, H, cull_backfaces=True)
    cov = r["tri"] >= 0
    A = r["attr"][cov]
    Pp, Np = A[:, 3:6], A[:, 6:9]
    Np = Np / np.linalg.norm(Np, axis=1, keepdims=True)
    lp = lighting(Pp, Np, light, shininess=shininess)
    imgs = {}
    for name, col in (("lambert", lp["ambient"] + lp["diffuse"]), ("phong", lp["ambient"] + lp["diffuse"] + lp["phong"]),
                      ("blinn_phong", lp["ambient"] + lp["diffuse"] + lp["blinn"]), ("gouraud", A[:, :3])):
        im = np.zeros((H, W, 3))
        im[cov] = np.clip(col, 0, 1)
        imgs[name] = im
    # ground truth: the exact sphere
    dx, dy, dz = pixel_rays(W, H, fov, asp)
    D = np.stack([dx, dy, dz], -1)
    D /= np.linalg.norm(D, axis=-1, keepdims=True)
    b = D @ centre
    disc = b * b - centre @ centre + 1.0
    hit = disc >= 0
    tt = b - np.sqrt(np.where(hit, disc, 0))
    Pt = D[hit] * tt[hit][:, None]
    lt = lighting(Pt, Pt - centre, light, shininess=shininess)
    truth = np.zeros((H, W, 3))
    truth[hit] = np.clip(lt["ambient"] + lt["diffuse"] + lt["phong"], 0, 1)
    diff = np.abs(imgs["gouraud"] - imgs["phong"]).max(-1)
    j, i = np.unravel_index(np.argmax(diff), diff.shape)
    both = cov & hit
    rmse = lambda im: float(np.sqrt(np.mean((im[both] - truth[both]) ** 2)))
    return {**imgs, "truth": truth, "triangles": len(F), "counters": r["counters"],
            "max_diff_gouraud_phong": float(diff.max()), "max_diff_at": [int(i), int(j)],
            "peak_gouraud": float(imgs["gouraud"].max()), "peak_phong": float(imgs["phong"].max()),
            "rmse_gouraud": rmse(imgs["gouraud"]), "rmse_phong": rmse(imgs["phong"])}


# --------------------------------------------------------------------------------------------------- textures


def checker_texture(n: int = 128, check: int = 16, lo: float = 0.1, hi: float = 0.9) -> np.ndarray:
    """An n x n single-channel checkerboard with ``check``-texel squares."""
    i = np.arange(n) // check
    return np.where((i[:, None] + i[None, :]) % 2 == 0, hi, lo).astype(float)


def mip_pyramid(tex: np.ndarray) -> list[np.ndarray]:
    """Williams's pyramid: each level the 2 x 2 box-filtered average of the one before, down to 1 x 1."""
    levels = [tex]
    while levels[-1].shape[0] > 1:
        t = levels[-1]
        levels.append(0.25 * (t[0::2, 0::2] + t[1::2, 0::2] + t[0::2, 1::2] + t[1::2, 1::2]))
    return levels


def mip_overhead(n: int = 128) -> dict:
    """Level sizes of an n x n pyramid and the extra memory over the base: sum 4^-k -> 1/3."""
    sizes = []
    while True:
        sizes.append(n)
        if n == 1:
            break
        n //= 2
    texels = [s * s for s in sizes]
    return {"sizes": sizes, "texels": texels, "overhead": (sum(texels) - texels[0]) / texels[0]}


def sample_nearest(tex, u, v):
    """Point sampling with wrap: the texel containing (u, v), in texel units (u along columns, v along rows)."""
    n = tex.shape[0]
    return tex[np.floor(v).astype(int) % n, np.floor(u).astype(int) % n]


def sample_bilinear(tex, u, v):
    n = tex.shape[0]
    x, y = u - 0.5, v - 0.5
    x0, y0 = np.floor(x), np.floor(y)
    fx, fy = x - x0, y - y0
    x0, y0 = x0.astype(int) % n, y0.astype(int) % n
    x1, y1 = (x0 + 1) % n, (y0 + 1) % n
    return ((1 - fx) * (1 - fy) * tex[y0, x0] + fx * (1 - fy) * tex[y0, x1] + (1 - fx) * fy * tex[y1, x0]
            + fx * fy * tex[y1, x1])


def sample_trilinear(pyr, u, v, rho):
    """Trilinear mip filtering: lambda = log2 rho (rho = texels per pixel step), clamped to the pyramid; bilinear on
    levels floor(lambda) and floor(lambda) + 1, blended by the fraction.  (u, v) in level-0 texel units."""
    L = len(pyr) - 1
    lam = np.clip(np.log2(np.maximum(rho, 1e-12)), 0, L)
    l0 = np.floor(lam).astype(int)
    f = lam - l0
    l1 = np.minimum(l0 + 1, L)
    out = np.zeros_like(u)
    for lv in range(L + 1):
        s = 2.0 ** -lv
        for sel, wt in ((l0 == lv, 1 - f), (l1 == lv, f)):
            if sel.any():
                out[sel] += wt[sel] * sample_bilinear(pyr[lv], u[sel] * s, v[sel] * s)
    return out


class _Ground:
    """The texture demo's camera: height 1 above the plane y = 0, pitched down so the plane fills the frame at a
    grazing angle.  ``uv(sx, sy)`` ray-casts screen points to level-0 texel coordinates."""

    def __init__(self, W, H, fovy, pitch, texels_per_unit):
        self.W, self.H, self.fovy, self.asp = W, H, fovy, W / H
        self.R = T.rotate_x(-pitch)[:3, :3]                     # camera to world
        self.view = T.compose(T.rotate_x(pitch), T.translate(0, -1, 0))
        self.k = texels_per_unit

    def uv(self, sx, sy):
        dx, dy, dz = pixel_rays(self.W, self.H, self.fovy, self.asp, sx, sy)
        D = np.stack([dx, dy, dz], -1) @ self.R.T
        t = -1.0 / D[..., 1]
        return t * D[..., 0] * self.k, -t * D[..., 2] * self.k


def texture_demo(W: int = 160, H: int = 120, fovy: float = 40.0, pitch: float = 22.0, tex_size: int = 128,
                 check: int = 16, units_per_tile: float = 2.0, seed: int = 51) -> dict:
    """A repeating checkerboard (``tex_size`` texels per tile, ``check``-texel squares, a tile every
    ``units_per_tile``) on the ground under a camera 1 unit up, pitched down ``pitch`` degrees so the top row grazes
    the plane at 2 degrees.  Samplers: ``point`` (one nearest-texel sample at each pixel centre, from our
    rasterizer's perspective-correct (u, v): moire), ``mip`` (trilinear, lambda from the screen-space derivatives of
    (u, v)), ``ss16`` (a 4 x 4 grid of point samples per pixel, averaged) and ``reference`` (256 stratified jittered
    samples per pixel, seeded).  Images are H x W grey (and ``lod``, the mip level used); ``rmse`` against the
    reference for each; ``pyramid`` holds the level sizes and the memory overhead; ``uv_raster_error`` checks the rasterizer against the ray cast."""
    k = tex_size / units_per_tile
    g = _Ground(W, H, fovy, pitch, k)
    tex = checker_texture(tex_size, check)
    pyr = mip_pyramid(tex)
    # one sample per pixel through the rasterizer
    P = T.perspective(fovy, W / H, 0.1, 200)
    quad = [(-80, 0, 2), (80, 0, 2), (80, 0, -120), (-80, 0, -120)]
    eye = T.apply(g.view, quad)
    r = rasterize(_tris(P, eye, [(0, 1, 2), (0, 2, 3)], [(x * k, -z * k) for x, _, z in quad]), W, H)
    U, Vv = r["attr"][..., 0], r["attr"][..., 1]
    sx, sy = np.meshgrid(np.arange(W) + 0.5, np.arange(H) + 0.5)
    ur, vr = g.uv(sx, sy)
    point = sample_nearest(tex, U, Vv)
    # derivatives of (u, v) per pixel step, by central differences of the exact mapping
    ux1, vx1 = g.uv(sx + 0.5, sy)
    ux0, vx0 = g.uv(sx - 0.5, sy)
    uy1, vy1 = g.uv(sx, sy + 0.5)
    uy0, vy0 = g.uv(sx, sy - 0.5)
    rho = np.maximum(np.hypot(ux1 - ux0, vx1 - vx0), np.hypot(uy1 - uy0, vy1 - vy0))
    mip = sample_trilinear(pyr, U, Vv, rho)

    def supersample(n, jitter):
        acc = np.zeros((H, W))
        rng = np.random.default_rng(seed)
        for a in range(n):
            for b in range(n):
                ox = (a + (rng.random((H, W)) if jitter else 0.5)) / n
                oy = (b + (rng.random((H, W)) if jitter else 0.5)) / n
                u, v = g.uv(sx - 0.5 + ox, sy - 0.5 + oy)
                acc += sample_nearest(tex, u, v)
        return acc / (n * n)

    ss16 = supersample(4, False)
    ref = supersample(16, True)
    rmse = lambda im: float(np.sqrt(np.mean((im - ref) ** 2)))
    lam = np.clip(np.log2(rho), 0, len(pyr) - 1)
    return {"point": point, "mip": mip, "ss16": ss16, "reference": ref, "lod": lam,
            "rmse": {"point": rmse(point), "mip": rmse(mip), "ss16": rmse(ss16)},
            "pyramid": mip_overhead(tex_size), "lod_range": [float(lam.min()), float(lam.max())],
            "covered": int((r["tri"] >= 0).sum()), "pixels": W * H,
            "uv_raster_error": float(max(np.abs(U - ur).max(), np.abs(Vv - vr).max())), "counters": r["counters"]}


# --------------------------------------------------------------------------------------------------- visibility


ZB_A = [(-1.6, -1.1, -3.0), (1.6, -0.7, -5.0), (-1.1, 1.3, -3.0)]
ZB_B = [(1.6, -1.1, -3.2), (-1.6, -0.7, -5.2), (1.1, 1.3, -3.2)]
ZB_COLORS = ((0.96, 0.58, 0.22), (0.27, 0.52, 0.96))


def zbuffer_demo(W: int = 160, H: int = 120) -> dict:
    """Two interpenetrating triangles (A leans away to the right, B to the left, so each is in front over part of
    the overlap).  The z-buffer resolves every pixel; the painter's algorithm sorts whole triangles by centroid depth
    (B is farther on average, drawn first) and paints A over all of B, wrong wherever B is in front.  Truth: per pixel
    the nearer of the two planes, ray cast.  Returns ``zbuffer`` and ``painter`` images, both ``counters``,
    ``overlap`` pixels, ``painter_wrong`` and ``zbuffer_wrong`` (pixels whose owner differs from the truth), and the
    painter's ``order``."""
    fov, asp = 60.0, W / H
    P = T.perspective(fov, asp, 0.1, 100)
    tris = [_tris(P, Vt, [(0, 1, 2)], [c] * 3)[0] for Vt, c in ((ZB_A, ZB_COLORS[0]), (ZB_B, ZB_COLORS[1]))]
    zb = rasterize(tris, W, H)
    cz = [float(np.mean([p[2] for p in Vt])) for Vt in (ZB_A, ZB_B)]
    order = sorted(range(2), key=lambda i: cz[i])          # most negative z (farthest) first
    pt = rasterize([tris[i] for i in order], W, H, depth_test=False)
    painter_tri = np.where(pt["tri"] >= 0, np.array(order)[np.maximum(pt["tri"], 0)], -1)
    # ray-cast truth: the eye distance to each triangle's plane where the ray is inside it
    dx, dy, dz = pixel_rays(W, H, fov, asp)
    D = np.stack([dx, dy, dz], -1)
    dist = []
    for Vt in (ZB_A, ZB_B):
        a, b, c = map(np.asarray, Vt)
        n = np.cross(b - a, c - a)
        t = (a @ n) / (D @ n)
        X = D * t[..., None]
        inside = np.ones(t.shape, bool)
        for p, q in ((a, b), (b, c), (c, a)):
            inside &= (np.cross(q - p, X - p) @ n) >= 0
        dist.append(np.where(inside & (t > 0), t, np.inf))
    owner = np.where(np.isfinite(np.minimum(*dist)), np.argmin(np.stack(dist), 0), -1)
    overlap = np.isfinite(dist[0]) & np.isfinite(dist[1])
    return {"zbuffer": zb["image"], "painter": pt["image"], "counters_zbuffer": zb["counters"],
            "counters_painter": pt["counters"], "order": order, "centroid_z": cz, "overlap": int(overlap.sum()),
            "painter_wrong": int((painter_tri != owner).sum()), "zbuffer_wrong": int((zb["tri"] != owner).sum()),
            "a_in_front": int((overlap & (owner == 0)).sum()), "b_in_front": int((overlap & (owner == 1)).sum())}
