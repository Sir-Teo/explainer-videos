"""Symbolic differential geometry (sympy) for the general-relativity video.

Every Christoffel symbol, curvature component and solution the video writes on screen is computed here from its
metric and asserted against the formula shown, so a typo in a slide fails the render instead of reaching the viewer.

Conventions (Carroll, *Spacetime and Geometry*): signature (-, +, +, +),

    Gamma^l_{mn} = 1/2 g^{ls} (d_m g_{sn} + d_n g_{sm} - d_s g_{mn})
    R^r_{smn}    = d_m Gamma^r_{ns} - d_n Gamma^r_{ms} + Gamma^r_{ml} Gamma^l_{ns} - Gamma^r_{nl} Gamma^l_{ms}
    R_{mn}       = R^l_{mln},   R = g^{mn} R_{mn},   G_{mn} = R_{mn} - 1/2 R g_{mn}
"""

from __future__ import annotations

from functools import lru_cache

import sympy as sp


class Geometry:
    """Curvature of the metric ``g`` (a sympy Matrix) in coordinates ``xs``; everything is computed lazily."""

    def __init__(self, g: sp.Matrix, xs: list[sp.Symbol]):
        self.g = sp.Matrix(g)
        self.xs = list(xs)
        self.n = len(xs)
        self.ginv = sp.simplify(self.g.inv())

    @property
    @lru_cache(maxsize=None)
    def gamma(self):
        """gamma[l][m][n] = Gamma^l_{mn}."""
        n, g, gi, x = self.n, self.g, self.ginv, self.xs
        return [[[sp.simplify(sum(gi[l, s] * (sp.diff(g[s, b], x[a]) + sp.diff(g[s, a], x[b]) - sp.diff(g[a, b], x[s]))
                                  for s in range(n)) / 2)
                  for b in range(n)] for a in range(n)] for l in range(n)]

    @lru_cache(maxsize=None)
    def riemann(self, r: int, s: int, m: int, nn: int):
        """R^r_{s m nn}."""
        G, x, n = self.gamma, self.xs, self.n
        e = sp.diff(G[r][nn][s], x[m]) - sp.diff(G[r][m][s], x[nn])
        e += sum(G[r][m][l] * G[l][nn][s] - G[r][nn][l] * G[l][m][s] for l in range(n))
        return sp.simplify(e)

    @property
    @lru_cache(maxsize=None)
    def ricci(self) -> sp.Matrix:
        n = self.n
        return sp.Matrix(n, n, lambda a, b: sp.simplify(sum(self.riemann(l, a, l, b) for l in range(n))))

    @property
    @lru_cache(maxsize=None)
    def scalar(self):
        n = self.n
        return sp.simplify(sum(self.ginv[a, b] * self.ricci[a, b] for a in range(n) for b in range(n)))

    @property
    @lru_cache(maxsize=None)
    def einstein(self) -> sp.Matrix:
        return sp.simplify(self.ricci - self.scalar * self.g / 2)

    def kretschmann(self):
        """R_{abcd} R^{abcd}."""
        n, g, gi = self.n, self.g, self.ginv
        low = {}
        for a in range(n):
            for b in range(n):
                for c in range(n):
                    for d in range(n):
                        low[a, b, c, d] = sum(g[a, e] * self.riemann(e, b, c, d) for e in range(n))
        up = {}
        for k, v in low.items():
            if v == 0:
                continue
            a, b, c, d = k
            up[k] = gi[a, a] * gi[b, b] * gi[c, c] * gi[d, d] * v  # diagonal metrics only
        return sp.simplify(sum(low[k] * up[k] for k in up))

    def nonzero_gammas(self) -> dict[tuple[int, int, int], sp.Expr]:
        """{(l, m, n): Gamma^l_{mn}} for m <= n with a nonzero value."""
        out = {}
        for l in range(self.n):
            for m in range(self.n):
                for nn in range(m, self.n):
                    v = self.gamma[l][m][nn]
                    if v != 0:
                        out[(l, m, nn)] = v
        return out


def same(a, b) -> bool:
    return sp.simplify(sp.sympify(a) - sp.sympify(b)) == 0


# ---------------------------------------------------------------------------
# The metrics of the video
# ---------------------------------------------------------------------------
@lru_cache(maxsize=None)
def sphere():
    th, ph, R = sp.symbols("theta phi R", positive=True)
    return Geometry(sp.diag(R**2, R**2 * sp.sin(th) ** 2), [th, ph]), (th, ph, R)


@lru_cache(maxsize=None)
def polar_plane():
    r, ph = sp.symbols("r phi", positive=True)
    return Geometry(sp.diag(1, r**2), [r, ph]), (r, ph)


@lru_cache(maxsize=None)
def static_spherical():
    """ds^2 = -e^{2 alpha(r)} dt^2 + e^{2 beta(r)} dr^2 + r^2 dOmega^2 (c = 1)."""
    t, r, th, ph = sp.symbols("t r theta phi", positive=True)
    a, b = sp.Function("alpha")(r), sp.Function("beta")(r)
    g = sp.diag(-sp.exp(2 * a), sp.exp(2 * b), r**2, r**2 * sp.sin(th) ** 2)
    return Geometry(g, [t, r, th, ph]), (t, r, th, ph, a, b)


@lru_cache(maxsize=None)
def schwarzschild():
    t, r, th, ph, rs = sp.symbols("t r theta phi r_s", positive=True)
    f = 1 - rs / r
    return Geometry(sp.diag(-f, 1 / f, r**2, r**2 * sp.sin(th) ** 2), [t, r, th, ph]), (t, r, th, ph, rs)


@lru_cache(maxsize=None)
def weak_static():
    """ds^2 = -(1 + 2 Phi) dt^2 + (1 - 2 Phi) dx^2 (c = 1), to first order in Phi."""
    t, x, y, z, eps = sp.symbols("t x y z epsilon")
    Phi = sp.Function("Phi")(x, y, z)
    g = sp.diag(-(1 + 2 * eps * Phi), 1 - 2 * eps * Phi, 1 - 2 * eps * Phi, 1 - 2 * eps * Phi)
    return Geometry(g, [t, x, y, z]), (t, x, y, z, eps, Phi)


def first_order(expr, eps):
    return sp.simplify(sp.series(expr, eps, 0, 2).removeO())


# ---------------------------------------------------------------------------
# Checks: the formulas the scenes show
# ---------------------------------------------------------------------------
def check_all() -> dict:
    out = {}
    # Sphere: Gamma^theta_{phi phi} = -sin cos, Gamma^phi_{theta phi} = cot; R^theta_{phi theta phi} = sin^2; R = 2/R^2.
    S, (th, ph, R) = sphere()
    assert same(S.gamma[0][1][1], -sp.sin(th) * sp.cos(th))
    assert same(S.gamma[1][0][1], sp.cos(th) / sp.sin(th))
    assert len(S.nonzero_gammas()) == 2
    assert same(S.riemann(0, 1, 0, 1), sp.sin(th) ** 2)
    assert same(S.ricci[0, 0], 1) and same(S.ricci[1, 1], sp.sin(th) ** 2)
    assert same(S.scalar, 2 / R**2)
    out["sphere"] = "ok"

    # Polar coordinates on the flat plane: Gamma^r_{phi phi} = -r, Gamma^phi_{r phi} = 1/r, and zero curvature.
    P, (r, ph2) = polar_plane()
    assert same(P.gamma[0][1][1], -r) and same(P.gamma[1][0][1], 1 / r)
    assert P.riemann(0, 1, 0, 1) == 0 and P.scalar == 0
    out["polar"] = "ok"

    # Static spherical ansatz: Carroll's (5.13)-style Ricci components.
    A, (t, r, th, ph, a, b) = static_spherical()
    ap, app, bp = sp.diff(a, r), sp.diff(a, r, 2), sp.diff(b, r)
    Rtt = sp.exp(2 * (a - b)) * (app + ap**2 - ap * bp + 2 * ap / r)
    Rrr = -app - ap**2 + ap * bp + 2 * bp / r
    Rthth = sp.exp(-2 * b) * (r * (bp - ap) - 1) + 1
    assert same(A.ricci[0, 0], Rtt)
    assert same(A.ricci[1, 1], Rrr)
    assert same(A.ricci[2, 2], Rthth)
    assert same(A.ricci[3, 3], sp.sin(th) ** 2 * Rthth)
    for i in range(4):
        for j in range(4):
            if i != j:
                assert A.ricci[i, j] == 0
    # The combination that kills the second derivatives: e^{2(b-a)} R_tt + R_rr = (2/r)(a' + b')
    assert same(sp.exp(2 * (b - a)) * Rtt + Rrr, 2 * (ap + bp) / r)
    # With beta = -alpha: R_thth = 0  <=>  d/dr (r e^{2 alpha}) = 1
    sub = Rthth.subs(b, -a).doit()
    assert same(sub, 1 - sp.diff(r * sp.exp(2 * a), r))
    # Nonzero Christoffels of the ansatz (shown on screen)
    gam = A.nonzero_gammas()
    assert same(gam[(0, 0, 1)], ap) and same(gam[(1, 0, 0)], sp.exp(2 * (a - b)) * ap) and same(gam[(1, 1, 1)], bp)
    assert same(gam[(2, 1, 2)], 1 / r) and same(gam[(1, 2, 2)], -r * sp.exp(-2 * b))
    assert same(gam[(3, 1, 3)], 1 / r) and same(gam[(1, 3, 3)], -r * sp.exp(-2 * b) * sp.sin(th) ** 2)
    assert same(gam[(3, 2, 3)], sp.cos(th) / sp.sin(th)) and same(gam[(2, 3, 3)], -sp.sin(th) * sp.cos(th))
    assert len(gam) == 9
    out["ansatz"] = "ok"

    # Schwarzschild: Ricci-flat, curvature scalar invariant 12 r_s^2 / r^6.
    Sw, (t, r, th, ph, rs) = schwarzschild()
    assert all(Sw.ricci[i, j] == 0 for i in range(4) for j in range(4))
    K = Sw.kretschmann()
    assert same(K, 12 * rs**2 / r**6)
    out["schwarzschild"] = "ok"

    # Weak static field: Gamma^i_00 = d_i Phi, R_00 = laplacian Phi, to first order.
    W, (t, x, y, z, eps, Phi) = weak_static()
    for i, xi in enumerate([x, y, z], start=1):
        assert same(first_order(W.gamma[i][0][0], eps), eps * sp.diff(Phi, xi))
    R00 = first_order(W.ricci[0, 0], eps)
    lap = sp.diff(Phi, x, 2) + sp.diff(Phi, y, 2) + sp.diff(Phi, z, 2)
    assert same(R00, eps * lap)
    # Tidal part: R^i_{0j0} = d_i d_j Phi
    assert same(first_order(W.riemann(1, 0, 2, 0), eps), eps * sp.diff(Phi, x, y))
    assert same(first_order(W.riemann(1, 0, 1, 0), eps), eps * sp.diff(Phi, x, 2))
    out["weak"] = "ok"
    return out


if __name__ == "__main__":
    print(check_all())
