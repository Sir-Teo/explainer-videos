"""Agora's labour market with frictions (Part 24): the searcher, the DMP model, Hosios, the volatility formula, the
flows and the job ladder."""

import numpy as np

from explainer.economics.agora import search as sr


def test_mccall_reservation_wage_solves_its_equation():
    lo, hi, b, beta = 50.0, 150.0, 40.0, 0.95
    w = np.linspace(lo, hi, 20001)
    r = sr.mccall(b=b, beta=beta, wages=w)["reservation"]
    # w* - b = beta/(1-beta) E[(w - w*)+], with E[(w - x)+] = (hi - x)^2 / (2 (hi - lo)) for a uniform
    lhs = r - b
    rhs = beta / (1 - beta) * (hi - r) ** 2 / (2 * (hi - lo))
    assert abs(lhs - rhs) < 0.05
    # more benefit or more patience: a higher reservation wage and a longer search
    a = sr.mccall(b=b + 20, beta=beta, wages=w)
    c = sr.mccall(b=b, beta=0.98, wages=w)
    base = sr.mccall(b=b, beta=beta, wages=w)
    assert a["reservation"] > base["reservation"] and a["duration"] > base["duration"]
    assert c["reservation"] > base["reservation"]


def test_dmp_steady_state_satisfies_both_curves():
    kw = dict(p=1.0, b=0.4, beta=0.5, eta=0.5, A=0.6, s=0.03, r=0.004, c=0.3)
    st = sr.dmp_steady(**kw)
    q = kw["A"] * st["theta"] ** (-kw["eta"])
    # job creation: c / q = (p - w) / (r + s)
    assert abs(kw["c"] / q - (kw["p"] - st["w"]) / (kw["r"] + kw["s"])) < 1e-8
    # the wage curve and the Beveridge curve
    assert abs(st["w"] - ((1 - kw["beta"]) * kw["b"] + kw["beta"] * (kw["p"] + kw["c"] * st["theta"]))) < 1e-12
    assert abs(st["u"] - kw["s"] / (kw["s"] + st["f"])) < 1e-12
    assert abs(st["v"] - st["theta"] * st["u"]) < 1e-12


def test_dmp_comparative_statics_signs():
    kw = dict(p=1.0, b=0.4, beta=0.5, eta=0.5, A=0.6, s=0.03, r=0.004, c=0.3)
    u0 = sr.dmp_steady(**kw)["u"]
    assert sr.dmp_steady(**{**kw, "b": 0.5})["u"] > u0
    assert sr.dmp_steady(**{**kw, "p": 1.05})["u"] < u0
    assert sr.dmp_steady(**{**kw, "s": 0.045})["u"] > u0
    assert sr.dmp_steady(**{**kw, "beta": 0.6})["u"] > u0
    # lower matching efficiency shifts the Beveridge curve out: more of both at the same productivity
    bev = sr.beveridge(ps=[1.0], As=(0.6, 0.48), **{k: v for k, v in kw.items() if k not in ("p", "A")})["curves"]
    assert bev[1]["u"][0] > bev[0]["u"][0] and bev[1]["v"][0] > bev[0]["v"][0]


def test_hosios_condition():
    for eta in (0.3, 0.5, 0.7):
        h = sr.hosios(betas=np.linspace(0.05, 0.95, 181), p=1.0, b=0.4, eta=eta, A=0.6, s=0.03, c=0.3)
        assert abs(h["best"] - eta) < 0.011


def test_volatility_matches_the_fundamental_surplus_formula():
    for b, beta, eta in ((0.4, 0.72, 0.72), (0.9, 0.2, 0.5)):
        kw = dict(b=b, beta=beta, eta=eta, A=1.355, s=0.1, r=0.012, c=0.2)
        e = sr.elasticity(dp=1e-4, **kw)
        st = e["steady"]
        f = st["f"]
        formula = (kw["r"] + kw["s"] + beta * f) / (eta * (kw["r"] + kw["s"]) + beta * f) / (1 - b)
        assert abs(e["theta"] - formula) / formula < 1e-3
    # the smaller the fundamental surplus, the larger the response
    lo = sr.elasticity(b=0.4, beta=0.72, eta=0.72, A=1.355, s=0.1, r=0.012, c=0.2)["theta"]
    hi = sr.elasticity(b=0.95, beta=0.72, eta=0.72, A=1.355, s=0.1, r=0.012, c=0.02)["theta"]
    assert hi > 5 * lo


def test_flows_recover_known_rates():
    # monthly data generated from known job-finding and separation rates in continuous time
    rng = np.random.default_rng(0)
    n = 240
    f_true = 0.5 + 0.1 * np.sin(np.arange(n) / 12)
    s_true = 0.03 + 0.005 * rng.standard_normal(n).cumsum() / 20
    lf = np.full(n + 1, 1000.0)
    u = [60.0]
    us = [30.0]
    for t in range(n):
        f, s = f_true[t], s_true[t]
        lam = f + s
        ss = s / lam * lf[t]
        u_next = ss + np.exp(-lam) * (u[-1] - ss)
        us.append(u_next - u[-1] * np.exp(-f))   # the unemployed who were not unemployed at the start of the month
        u.append(u_next)
    out = sr.flows(np.array(u), np.array(us), lf)
    assert np.allclose(out["f"], f_true, atol=1e-6)
    assert np.allclose(out["s"], s_true, atol=1e-4)


def test_ins_outs_shares_sum_to_about_one():
    rng = np.random.default_rng(1)
    t = np.arange(200)
    f = 0.5 * np.exp(0.2 * np.sin(t / 8) + 0.02 * rng.standard_normal(200))
    s = 0.03 * np.exp(0.05 * np.sin(t / 8 + 0.5) + 0.02 * rng.standard_normal(200))
    io = sr.ins_outs(f, s)
    assert 0.9 < io["share_f"] + io["share_s"] < 1.1
    assert io["share_f"] > io["share_s"]


def test_job_ladder():
    lad = sr.burdett_mortensen(p=1.0, b=0.4, lam=0.1, delta=0.02)
    w, F, G = np.array(lad["w"]), np.array(lad["F"]), np.array(lad["G"])
    assert abs(F[0]) < 1e-9 and abs(F[-1] - 1) < 1e-6 and abs(G[-1] - 1) < 1e-6
    assert np.all(G <= F + 1e-12)                       # earnings dominate offers
    assert abs(lad["u"] - 0.02 / 0.12) < 1e-12
    assert abs(lad["w_hi"] - (1 - 0.6 / 36)) < 1e-9     # p - (p - b)/(1 + k)^2 with k = 5
    assert lad["mean_earned"] > lad["mean_offer"]
    assert np.all(np.diff(w) > 0)
