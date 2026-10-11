"""Symbolic checks (sympy) for part 2 of the general-relativity video.

Every metric, curvature component and identity a scene writes on screen is derived here from its definition and
asserted, so a typo in a slide fails the render instead of reaching the viewer.  Conventions as in part 1 (Carroll):
signature (-, +, +, +), G = c = 1, Gamma^l_{mn} = 1/2 g^{ls}(d_m g_sn + d_n g_sm - d_s g_mn),
R^r_{smn} = d_m Gamma^r_{ns} - d_n Gamma^r_{ms} + Gamma^r_{ml} Gamma^l_{ns} - Gamma^r_{nl} Gamma^l_{ms}.

    python -m videos.relativity2.geometry          # run every check (~1 min; Kerr is the slow one)
"""

from __future__ import annotations

from functools import lru_cache

import sympy as sp


class Curvature:
    """Christoffel symbols and Ricci tensor of ``g`` in coordinates ``xs``.  ``simp`` is the simplifier: ``sp.cancel``
    for metrics whose components are rational functions (exact and fast), ``sp.simplify`` otherwise."""

    def __init__(self, g, xs, simp=sp.simplify):
        self.g = sp.Matrix(g)
        self.xs = list(xs)
        self.n = len(xs)
        self.simp = simp
        self.ginv = self.g.inv(method="LU").applyfunc(simp)
        n, x = self.n, self.xs
        dg = [[[sp.diff(self.g[i, j], x[k]) for k in range(n)] for j in range(n)] for i in range(n)]
        self.gamma = [[[simp(sum(self.ginv[l, s] * (dg[s][b][a] + dg[s][a][b] - dg[a][b][s]) for s in range(n)) / 2)
                        for b in range(n)] for a in range(n)] for l in range(n)]

    def riemann(self, r, s, m, nn):
        G, x, n = self.gamma, self.xs, self.n
        e = sp.diff(G[r][nn][s], x[m]) - sp.diff(G[r][m][s], x[nn])
        e += sum(G[r][m][l] * G[l][nn][s] - G[r][nn][l] * G[l][m][s] for l in range(n))
        return self.simp(e)

    @lru_cache(maxsize=None)
    def ricci_component(self, a, b):
        return self.simp(sum(self.riemann(l, a, l, b) for l in range(self.n)))

    def ricci(self):
        return sp.Matrix(self.n, self.n, lambda a, b: self.ricci_component(min(a, b), max(a, b)))

    def scalar(self):
        R = self.ricci()
        return self.simp(sum(self.ginv[a, b] * R[a, b] for a in range(self.n) for b in range(self.n)))


def same(a, b) -> bool:
    return sp.simplify(sp.sympify(a) - sp.sympify(b)) == 0


# ---------------------------------------------------------------------------
# Horizons: Eddington-Finkelstein and Kruskal-Szekeres
# ---------------------------------------------------------------------------
def check_eddington_finkelstein():
    """Substituting t = v - r*(r) into Schwarzschild gives ds^2 = -(1 - 2M/r) dv^2 + 2 dv dr + r^2 dOmega^2, which is
    regular at r = 2M and still a vacuum solution; with t~ = v - r, ingoing light moves at 45 degrees."""
    r, M = sp.symbols("r M", positive=True)
    f = 1 - 2 * M / r
    rstar = r + 2 * M * sp.log(r / (2 * M) - 1)
    assert same(sp.diff(rstar, r), 1 / f)
    # dt = dv - dr / f  =>  -f dt^2 + dr^2/f = -f dv^2 + 2 dv dr  (coefficients of dv^2, dv dr, dr^2)
    dv, dr = sp.symbols("dv dr")
    ds2 = sp.expand(-f * (dv - dr / f) ** 2 + dr**2 / f)
    assert same(ds2.coeff(dv, 2), -f) and same(ds2.coeff(dv, 1).coeff(dr, 1), 2) and same(ds2.coeff(dr, 2), 0)
    v, th, ph = sp.symbols("v theta phi")
    g = sp.Matrix([[-f, 1, 0, 0], [1, 0, 0, 0], [0, 0, r**2, 0], [0, 0, 0, r**2 * sp.sin(th) ** 2]])
    assert same(g.det(), -(r**4) * sp.sin(th) ** 2)  # nonzero at r = 2M: no coordinate singularity
    C = Curvature(g, [v, r, th, ph])
    assert all(C.ricci_component(i, j) == 0 for i in range(4) for j in range(i, 4))
    # t~ = v - r: ds^2 = -f dt~^2 + (4M/r) dt~ dr + (1 + 2M/r) dr^2; outgoing light has dt~/dr = (1 + 2M/r)/(1 - 2M/r)
    dtt = sp.symbols("dtt")
    ds2b = sp.expand(-f * (dtt + dr) ** 2 + 2 * (dtt + dr) * dr)
    assert same(ds2b.coeff(dtt, 2), -f) and same(ds2b.coeff(dtt, 1).coeff(dr, 1), 4 * M / r)
    assert same(ds2b.coeff(dr, 2), 1 + 2 * M / r)
    k = sp.symbols("k")  # null directions dt~ = k dr
    roots = sp.solve(sp.expand(ds2b.subs(dtt, k * dr) / dr**2), k)
    assert any(same(x, -1) for x in roots) and any(same(x, (1 + 2 * M / r) / (1 - 2 * M / r)) for x in roots)
    return "ok"


def check_kruskal():
    """With U = -e^{-u/4M}, V = e^{v/4M}: U V = (1 - r/2M) e^{r/2M} and -f du dv = -(32 M^3/r) e^{-r/2M} dU dV."""
    r, M = sp.symbols("r M", positive=True)
    f = 1 - 2 * M / r
    UV = (1 - r / (2 * M)) * sp.exp(r / (2 * M))
    rstar = r + 2 * M * sp.log(r / (2 * M) - 1)
    # region I: U V = -e^{(v - u)/4M} = -e^{r*/2M}
    assert same(sp.simplify(-sp.exp(rstar / (2 * M)) - UV), 0)
    # du dv = (4M)^2 dU dV / (-U V)   =>   -f du dv = -f 16 M^2 / (-U V) dU dV
    coef = -f * 16 * M**2 / (-UV)
    assert same(coef, -32 * M**3 / r * sp.exp(-r / (2 * M)))
    # the conformal factor is finite and positive at r = 2M
    assert same(sp.limit(32 * M**3 / r * sp.exp(-r / (2 * M)), r, 2 * M), 16 * M**2 / sp.E)
    return "ok"


def check_penrose():
    """Minkowski, u = t - r, v = t + r, u~ = arctan u: -du dv = -du~ dv~ / (cos^2 u~ cos^2 v~)."""
    uu, vv = sp.symbols("ut vt", real=True)
    u, v = sp.tan(uu), sp.tan(vv)
    assert same(sp.diff(u, uu) * sp.diff(v, vv), 1 / (sp.cos(uu) ** 2 * sp.cos(vv) ** 2))
    # Schwarzschild's singularity U V = 1 is the straight line arctan U + arctan V = pi/2 (U, V > 0)
    U = sp.symbols("U", positive=True)
    s = sp.atan(U) + sp.atan(1 / U)
    assert same(sp.diff(s, U), 0) and same(s.subs(U, 1), sp.pi / 2)
    return "ok"


# ---------------------------------------------------------------------------
# Kerr, in rational coordinates (t, r, x = cos theta, phi)
# ---------------------------------------------------------------------------
@lru_cache(maxsize=None)
def kerr():
    t, r, x, ph = sp.symbols("t r x phi", real=True)
    M, a = sp.symbols("M a", positive=True)
    S = r**2 + a**2 * x**2
    D = r**2 - 2 * M * r + a**2
    s2 = 1 - x**2
    g = sp.zeros(4, 4)
    g[0, 0] = -(1 - 2 * M * r / S)
    g[0, 3] = g[3, 0] = -2 * M * a * r * s2 / S
    g[1, 1] = S / D
    g[2, 2] = S / s2  # d theta^2 = dx^2 / (1 - x^2)
    g[3, 3] = (r**2 + a**2 + 2 * M * a**2 * r * s2 / S) * s2
    return g, (t, r, x, ph, M, a, S, D)


def check_kerr():
    g, (t, r, x, ph, M, a, S, D) = kerr()
    C = Curvature(g, [t, r, x, ph], simp=lambda e: sp.cancel(sp.together(e)))
    for i in range(4):
        for j in range(i, 4):
            assert C.ricci_component(i, j) == 0, (i, j)
    out = {"ricci_flat": True}
    # a -> 0: Schwarzschild
    assert same(g.subs(a, 0)[0, 0], -(1 - 2 * M / r)) and same(g.subs(a, 0)[1, 1], 1 / (1 - 2 * M / r))
    # M -> 0: flat space (in oblate spheroidal coordinates): every Riemann component vanishes
    g0 = g.subs(M, 0)
    C0 = Curvature(g0, [t, r, x, ph], simp=lambda e: sp.cancel(sp.together(e)))
    for (p, q, m, n) in [(1, 2, 1, 2), (1, 3, 1, 3), (2, 3, 2, 3), (1, 2, 1, 3), (1, 3, 2, 3)]:
        assert C0.riemann(p, q, m, n) == 0
    # far away: g_t phi -> -2 J sin^2 theta / r with J = M a (the gravitomagnetic field of any spinning body)
    J = sp.symbols("J", positive=True)
    far = sp.limit(g[0, 3] * r, r, sp.oo)
    assert same(far, -2 * M * a * (1 - x**2))
    # horizons where g^rr = Delta / Sigma = 0; ergosurface where g_tt = 0
    rp = M + sp.sqrt(M**2 - a**2)
    assert same(D.subs(r, rp), 0)
    rE = M + sp.sqrt(M**2 - a**2 * x**2)
    assert same(g[0, 0].subs(r, rE), 0)
    assert same(C.ginv[1, 1], D / S)
    # Ring singularity: Kretschmann scalar on the equatorial plane (x = 0) is 48 M^2 / r^6 (Schwarzschild's form;
    # the full expression is checked numerically in compute.py)
    return out


def check_kerr_thermo():
    """A = 8 pi (M^2 + sqrt(M^4 - J^2)); dM = (kappa / 8 pi) dA + Omega_H dJ with kappa = (r+ - M)/(r+^2 + a^2),
    Omega_H = a / (r+^2 + a^2); Christodoulou: M^2 = M_irr^2 + J^2 / (4 M_irr^2), M_irr = sqrt(A / 16 pi)."""
    M, J, A = sp.symbols("M J A", positive=True)
    a = J / M
    rp = M + sp.sqrt(M**2 - a**2)
    area = 4 * sp.pi * (rp**2 + a**2)
    assert same(area, 8 * sp.pi * (M**2 + sp.sqrt(M**4 - J**2)))
    assert same(area, 8 * sp.pi * M * rp)
    kappa = (rp - M) / (rp**2 + a**2)
    OmH = a / (rp**2 + a**2)
    # implicit differentiation of A(M, J): dM/dA|_J = 1 / (dA/dM), dM/dJ|_A = -(dA/dJ)/(dA/dM)
    dAdM, dAdJ = sp.diff(area, M), sp.diff(area, J)
    assert same(1 / dAdM, kappa / (8 * sp.pi))
    assert same(-dAdJ / dAdM, OmH)
    # Christodoulou's mass formula
    Mirr2 = area / (16 * sp.pi)
    assert same(Mirr2 + J**2 / (4 * Mirr2), M**2)
    # Schwarzschild: kappa = 1/4M, and it's the redshifted acceleration needed to hover
    r, m = sp.symbols("r m", positive=True)
    accel = m / (r**2 * sp.sqrt(1 - 2 * m / r))  # proper acceleration of a static observer
    assert same(sp.limit(accel * sp.sqrt(1 - 2 * m / r), r, 2 * m), 1 / (4 * m))
    assert same(kappa.subs(J, 0), 1 / (4 * M))
    return "ok"


def check_near_horizon():
    """r = 2M + rho^2/8M: -f dt^2 + dr^2/f = -(rho/4M)^2 dt^2 + d rho^2 + O(rho^4): Rindler, with kappa = 1/4M."""
    M, rho = sp.symbols("M rho", positive=True)
    r = 2 * M + rho**2 / (8 * M)
    f = 1 - 2 * M / r
    assert same(sp.series(f, rho, 0, 4).removeO(), rho**2 / (16 * M**2))
    grr = sp.diff(r, rho) ** 2 / f
    assert same(sp.series(grr, rho, 0, 2).removeO(), 1)
    return "ok"


# ---------------------------------------------------------------------------
# Gravitational waves: the quadrupole luminosity of a circular binary
# ---------------------------------------------------------------------------
def check_binary_luminosity():
    """L = (1/5) <dddQ_ij dddQ_ij> = (32/5) mu^2 a^4 omega^6 = (32/5) mu^2 M^3 / a^5 (Kepler: omega^2 = M / a^3)."""
    t, mu, a, w, Mt = sp.symbols("t mu a omega M", positive=True)
    n = sp.Matrix([sp.cos(w * t), sp.sin(w * t), 0])
    I = mu * a**2 * (n * n.T)
    Q = I - sp.eye(3) * I.trace() / 3
    Q3 = Q.diff(t, 3)
    L = sp.simplify(sum(Q3[i, j] ** 2 for i in range(3) for j in range(3)) / 5)
    assert same(L, sp.Rational(32, 5) * mu**2 * a**4 * w**6)
    assert same(L.subs(w, sp.sqrt(Mt / a**3)), sp.Rational(32, 5) * mu**2 * Mt**3 / a**5)
    # energy balance: E = -mu M / 2a  =>  da/dt = -(64/5) mu M^2 / a^3
    E = -mu * Mt / (2 * a)
    adot = -sp.Rational(32, 5) * mu**2 * Mt**3 / a**5 / sp.diff(E, a)
    assert same(adot, -sp.Rational(64, 5) * mu * Mt**2 / a**3)
    # f_GW = omega / pi;  df/dt = (96/5) pi^(8/3) Mc^(5/3) f^(11/3) with Mc^(5/3) = mu M^(2/3)
    f = sp.symbols("f", positive=True)
    a_of_f = (Mt / (sp.pi * f) ** 2) ** sp.Rational(1, 3)
    fdot = sp.diff(sp.sqrt(Mt / a**3) / sp.pi, a) * adot
    target = sp.Rational(96, 5) * sp.pi ** sp.Rational(8, 3) * mu * Mt ** sp.Rational(2, 3) * f ** sp.Rational(11, 3)
    assert same(sp.simplify(fdot.subs(a, a_of_f)), target)
    # integrate: f(tau) = (1/pi) (5 / (256 tau))^(3/8) Mc^(-5/8)
    tau, Mc = sp.symbols("tau M_c", positive=True)
    fsol = (5 / (256 * tau)) ** sp.Rational(3, 8) * Mc ** sp.Rational(-5, 8) / sp.pi
    # df/dt = -df/dtau
    lhs = -sp.diff(fsol, tau)
    rhs = sp.Rational(96, 5) * sp.pi ** sp.Rational(8, 3) * Mc ** sp.Rational(5, 3) * fsol ** sp.Rational(11, 3)
    assert same(sp.simplify(lhs / rhs), 1)
    # merger time from separation a0: T = (5/256) a0^4 / (mu M^2)
    a0 = sp.symbols("a0", positive=True)
    T = sp.integrate(-1 / (-sp.Rational(64, 5) * mu * Mt**2 / a**3), (a, 0, a0))
    assert same(T, sp.Rational(5, 256) * a0**4 / (mu * Mt**2))
    return "ok"


# ---------------------------------------------------------------------------
# Cosmology: FLRW -> Friedmann
# ---------------------------------------------------------------------------
def check_flrw():
    t, r, th, ph = sp.symbols("t r theta phi", positive=True)
    k = sp.symbols("k", real=True)
    a = sp.Function("a")(t)
    g = sp.diag(-1, a**2 / (1 - k * r**2), a**2 * r**2, a**2 * r**2 * sp.sin(th) ** 2)
    C = Curvature(g, [t, r, th, ph])
    ad, add = sp.diff(a, t), sp.diff(a, t, 2)
    # Christoffels shown on screen: Gamma^t_rr = a a' / (1 - k r^2), Gamma^r_tr = a'/a
    assert same(C.gamma[0][1][1], a * ad / (1 - k * r**2)) and same(C.gamma[1][0][1], ad / a)
    R = C.ricci()
    assert same(R[0, 0], -3 * add / a)
    assert same(R[1, 1], (a * add + 2 * ad**2 + 2 * k) / (1 - k * r**2))
    assert same(R[2, 2], r**2 * (a * add + 2 * ad**2 + 2 * k))
    Rs = C.scalar()
    assert same(Rs, 6 * (add / a + ad**2 / a**2 + k / a**2))
    G = (R - Rs * g / 2).applyfunc(sp.simplify)
    rho, p, Lam = sp.symbols("rho p Lambda", real=True)
    # G_tt + Lambda g_tt = 8 pi T_tt = 8 pi rho  =>  (a'/a)^2 = 8 pi rho / 3 - k / a^2 + Lambda / 3
    assert same(G[0, 0], 3 * (ad**2 + k) / a**2)
    # G_rr = -(2 a a'' + a'^2 + k) / (1 - k r^2);  T_rr = p g_rr
    assert same(G[1, 1], -(2 * a * add + ad**2 + k) / (1 - k * r**2))
    # combine: a''/a = -(4 pi / 3)(rho + 3p) + Lambda/3
    H2 = 8 * sp.pi * rho / 3 - k / a**2 + Lam / 3  # (a'/a)^2 from the tt equation
    # rr equation: -(2 a''/a + (a'/a)^2 + k/a^2) + Lambda = 8 pi p
    acc = sp.solve(sp.Eq(-(2 * sp.Symbol("q") + H2 + k / a**2) + Lam, 8 * sp.pi * p), sp.Symbol("q"))[0]
    assert same(acc, -sp.Rational(4, 3) * sp.pi * (rho + 3 * p) + Lam / 3)
    # conservation: d rho/dt = -3 (a'/a)(rho + p)  =>  rho ~ a^{-3(1+w)} for p = w rho
    w, a0 = sp.symbols("w a0", positive=True)
    A = sp.symbols("A", positive=True)
    rho_a = A ** (-3 * (1 + w))
    assert same(sp.diff(rho_a, A) * A, -3 * (1 + w) * rho_a)
    return "ok"


def check_all() -> dict:
    out = {}
    out["eddington_finkelstein"] = check_eddington_finkelstein()
    out["kruskal"] = check_kruskal()
    out["penrose"] = check_penrose()
    out["near_horizon"] = check_near_horizon()
    out["kerr_thermo"] = check_kerr_thermo()
    out["binary"] = check_binary_luminosity()
    out["flrw"] = check_flrw()
    out["kerr"] = check_kerr()
    return out


if __name__ == "__main__":
    import time

    t0 = time.time()
    print(check_all(), f"{time.time() - t0:.0f}s")
