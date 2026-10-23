"""Part 21's trained models in the plane: small networks learning the "AI" mixture (exact.py), measured against the
exact answers wherever they exist.  Every comparison trains several seeds at the same budget (STEPS steps of BATCH).

    denoiser    the noise-guessing network (cosine schedule), three seeds; the training replay (samples from the same
                noise at checkpoints, the loss); denoising score matching checked: loss = constant + score error,
                at four noise levels, through training; the learned score field; DDPM and DDIM paths
    solvers_net the samplers again, with the trained network as the denoiser
    ablate      where training spends its noise levels (four schedules) and what the network predicts (noise, clean
                point, EDM's mixture), equal budgets, three seeds: distance from the data, error against the exact
                denoiser at each noise level, learning curves
    flow        flow matching (independent pairs), minibatch optimal-transport pairs, reflow and reflow again; Euler
                with 1 to 100 steps; straightness and transport cost; the training replay
    fewstep     MeanFlow and shortcut models (fewstep.py), three seeds
    distill     one-step students of the flow-matching teacher: progressive distillation (64 -> 1 steps),
                consistency distillation, distribution matching distillation (DMD); three seeds
    guidance    two letters, A and I: classifier-free guidance, classifier guidance (a noisy classifier, Bayes) and
                autoguidance (a weaker model of the same kind), swept over the weight w, three seeds; on-target rate,
                precision and recall against the real A
"""

from __future__ import annotations

import math
import os

import numpy as np

from videos.ai.ai21 import exact as E

QUICK = os.environ.get("AI21_QUICK") == "1"
STEPS = 300 if QUICK else 6000
BATCH = 512
SEEDS = (0, 1) if QUICK else (0, 1, 2)
CHECKS = [0, 50, 150, 400, 1000, 2500, STEPS] if not QUICK else [0, 50, 150, STEPS]


def threads():
    import torch

    torch.set_num_threads(int(os.environ.get("AI21_THREADS", "2")))


def cache():
    from videos.ai.ai21.compute import CACHE

    return CACHE


def mixture_torch(g):
    """A function n -> n points from the mixture, drawn with torch generator g."""
    import torch

    C = torch.tensor(E.centers(), dtype=torch.float32)

    def draw(n):
        return C[torch.randint(0, len(C), (n,), generator=g)] + E.S0 * torch.randn(n, 2, generator=g)

    return draw


def lr_sched(opt, steps):
    import torch

    return torch.optim.lr_scheduler.CosineAnnealingLR(opt, steps)


def to_np(t):
    return t.detach().numpy().astype(float)


# ---------------------------------------------------------------------------
# Denoisers: a network of (the VP state, the cosine-schedule time) with three ways to read its output
SIG_D = None


def sigma_data():
    global SIG_D
    if SIG_D is None:
        SIG_D = float(np.sqrt(E.sample(20000, 13).var(0).mean()))
    return SIG_D


def noise_levels(kind, n, g):
    """EDM-style noise levels s (x = x0 + s n) as the schedule `kind` visits them when its own time is uniform."""
    import torch

    u = torch.rand(n, generator=g) * 0.998 + 0.001
    if kind == "cos":  # ours: alpha = cos(pi t / 2), sigma = sin(pi t / 2)
        return torch.tan(math.pi * u / 2)
    if kind == "linb":  # the VP SDE with linear beta (0.1 to 20)
        B = 0.1 * u + 0.5 * 19.9 * u * u
        a = torch.exp(-0.5 * B)
        return torch.sqrt(1 - a * a) / a
    if kind == "fm":  # flow matching's straight line: x = (1 - t) x0 + t eps
        return u / (1 - u)
    if kind == "logn":  # EDM: log s normal, P_mean -1.2 and P_std 1.2, rescaled to this data's spread
        return torch.exp(-1.2 + math.log(sigma_data() / 0.5) + 1.2 * torch.randn(n, generator=g))
    raise ValueError(kind)


class Denoiser:
    """D(x, s) for x = x0 + s n, from a network f(u, t): u the network's input, t = (2/pi) atan(s) the noise level as
    cosine-schedule time.  param: 'eps' (f guesses the noise), 'x0' (the clean point), 'F' (EDM's preconditioning)."""

    def __init__(self, net, param="eps"):
        self.net, self.param = net, param

    def parts(self, x, s):
        import torch

        sd = sigma_data()
        t = 2 / math.pi * torch.atan(s)
        if self.param == "F":
            u = x / torch.sqrt(s * s + sd * sd)[:, None]
        else:
            u = x / torch.sqrt(1 + s * s)[:, None]  # the VP state
        return u, t

    def __call__(self, x, s):
        """Torch: x (n, 2), s (n,) -> D (n, 2)."""
        import torch

        u, t = self.parts(x, s)
        f = self.net(u, t)
        if self.param == "eps":
            return x - s[:, None] * f
        if self.param == "x0":
            return f
        sd = sigma_data()
        c_skip = sd * sd / (s * s + sd * sd)
        c_out = s * sd / torch.sqrt(s * s + sd * sd)
        return c_skip[:, None] * x + c_out[:, None] * f

    def loss(self, x0, n, s):
        import torch

        x = x0 + s[:, None] * n
        u, t = self.parts(x, s)
        f = self.net(u, t)
        if self.param == "eps":
            tgt = n
        elif self.param == "x0":
            tgt = x0
        else:
            sd = sigma_data()
            c_skip = sd * sd / (s * s + sd * sd)
            c_out = s * sd / torch.sqrt(s * s + sd * sd)
            tgt = (x0 - c_skip[:, None] * x) / c_out[:, None]
        return ((f - tgt) ** 2).sum(1).mean() / 2

    def np(self, x, s):
        """numpy, for exact.solve: x (n, 2), s a number."""
        import torch

        with torch.no_grad():
            xt = torch.tensor(x, dtype=torch.float32)
            return to_np(self(xt, torch.full((len(x),), float(s))))


def train_denoiser(seed, kind="cos", param="eps", steps=STEPS, on_check=None, curve=None, checks=None):
    import torch

    from videos.ai.ai21.compute import mlp

    torch.manual_seed(2020 + seed)  # Ho, Jain & Abbeel, DDPM
    net = mlp(2, 2)
    D = Denoiser(net, param)
    opt = torch.optim.Adam(net.parameters(), lr=2e-3)
    sched = lr_sched(opt, steps)
    g = torch.Generator().manual_seed(seed)
    draw = mixture_torch(g)
    if on_check is not None:
        on_check(0, D)
    run = []
    for step in range(1, steps + 1):
        x0 = draw(BATCH)
        n = torch.randn(BATCH, 2, generator=g)
        s = noise_levels(kind, BATCH, g)
        loss = D.loss(x0, n, s)
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
        run.append(float(loss))
        if curve is not None and step % 25 == 0:
            curve.append((step, float(np.mean(run))))
            run = []
        if on_check is not None and step in (checks or CHECKS)[1:]:
            on_check(step, D)
    return D


def ddim_vp(D, z, steps, keep_every=None):
    """DDIM on the cosine schedule's time grid, uniform from t = 1 to 0 (as in DDPM-era samplers)."""
    ts = np.linspace(1, 0, steps + 1)
    x = z.copy()
    path = [x[:300].copy()]
    for i in range(steps):
        a, s = math.cos(math.pi * ts[i] / 2), math.sin(math.pi * ts[i] / 2)
        an, sn = math.cos(math.pi * ts[i + 1] / 2), math.sin(math.pi * ts[i + 1] / 2)
        x0 = np.clip(D.np(x / max(a, 1e-3), s / max(a, 1e-3)), -4, 4)  # at pure noise the clean guess is ill-posed
        e = (x - a * x0) / s
        x = an * x0 + sn * e
        if keep_every and (i + 1) % keep_every == 0:
            path.append(x[:300].copy())
    return x, np.array(path)


def ddpm_vp(D, z, steps, seed, keep_every=10):
    """DDPM's ancestral sampler on the same grid: guess the clean point, step to the posterior, add fresh noise."""
    g = E.rng(seed)
    ts = np.linspace(1, 0, steps + 1)
    x = z.copy()
    path = [x[:300].copy()]
    for i in range(steps):
        a, s = math.cos(math.pi * ts[i] / 2), math.sin(math.pi * ts[i] / 2)
        an, sn = math.cos(math.pi * ts[i + 1] / 2), math.sin(math.pi * ts[i + 1] / 2)
        x0 = np.clip(D.np(x / max(a, 1e-3), s / max(a, 1e-3)), -4, 4)
        a_ts = a / an
        s2_ts = s ** 2 - a_ts ** 2 * sn ** 2
        mean = (a_ts * sn ** 2 / s ** 2) * x + (an * s2_ts / s ** 2) * x0
        var = s2_ts * sn ** 2 / s ** 2
        x = mean + (math.sqrt(max(var, 0)) * g.normal(size=x.shape) if i < steps - 1 else 0)
        if (i + 1) % keep_every == 0:
            path.append(x[:300].copy())
    return x, np.array(path)


DSM_TS = [0.1, 0.3, 0.6, 0.9]


def dsm_terms(D, x0, n):
    """Denoising score matching, term by term, at four noise levels: the loss on fresh noise, the constant (the loss
    of the exact score), the error against the exact score, and the cross term (which the theorem says vanishes)."""
    import torch

    rows = []
    for t in DSM_TS:
        a, s = math.cos(math.pi * t / 2), math.sin(math.pi * t / 2)
        xv = a * x0 + s * n
        ex0 = E.posterior(xv, a, s)[0]
        e_star = (xv - a * ex0) / s
        with torch.no_grad():
            e_hat = to_np(D.net(torch.tensor(xv, dtype=torch.float32), torch.full((len(xv),), t)))
        rows.append(dict(t=t, loss=float(((e_hat - n) ** 2).sum(1).mean()), const=float(((n - e_star) ** 2).sum(1).mean()),
                         err=float(((e_hat - e_star) ** 2).sum(1).mean()),
                         cross=float(2 * ((e_hat - e_star) * (e_star - n)).sum(1).mean())))
    return rows


def compute_denoiser():
    import torch

    from videos.ai.ai21.compute import sw_distance, vp

    threads()
    C = cache()
    part = C.partial("denoiser", dict(steps=STEPS, seeds=list(SEEDS), checks=CHECKS))
    x0e, ne = E.sample(4000, 32), E.rng(33).normal(size=(4000, 2))
    z = E.rng(1).normal(size=(4000, 2))
    data = E.sample(4000, 31)
    for seed in SEEDS:
        key = f"s{seed}"
        wpath = C.dir / f"denoiser_s{seed}.pt"
        if key in part and wpath.exists():
            continue
        snaps, terms, curve = [], [], []

        def on_check(step, D):
            terms.append(dict(step=step, rows=dsm_terms(D, x0e, ne)))
            if seed == 0:
                snaps.append(ddim_vp(D, z[:600], 50)[0])

        D = train_denoiser(seed, on_check=on_check, curve=curve)
        torch.save(D.net.state_dict(), wpath)
        part[key] = dict(terms=terms, curve=curve, snaps=[s_.tolist() for s_ in snaps],
                         sw=[E.dist(s_) for s_ in snaps])
        print(f"    seed {seed}: final loss {curve[-1][1]:.4f}; score error at t=" +
              ", ".join(f"{r['t']}: {r['err']:.4f}" for r in terms[-1]["rows"]), flush=True)
    D = load_denoiser(0)
    out = dict(checks=CHECKS, seeds=list(SEEDS), dsm_ts=DSM_TS, steps=STEPS, batch=BATCH)
    for seed in SEEDS:
        p = part[f"s{seed}"]
        out[f"terms_s{seed}"] = np.array([[[r["loss"], r["const"], r["err"], r["cross"]] for r in c["rows"]]
                                          for c in p["terms"]])  # check, noise level, (loss, const, err, cross)
        out[f"curve_s{seed}"] = np.array(p["curve"])
    out["snaps"] = np.array(part["s0"]["snaps"])
    out["snap_sw"] = part["s0"]["sw"]
    out["losses"] = out["curve_s0"]
    # the learned score on a grid at four noise levels, beside the exact one
    gx, gy = np.meshgrid(np.linspace(-3, 3, 25), np.linspace(-2, 2, 17))
    grid = np.stack([gx.ravel(), gy.ravel()], 1)
    out["grid"], out["field_ts"] = grid, [0.8, 0.5, 0.25, 0.08]
    for t in out["field_ts"]:
        a, s = vp(t)
        with torch.no_grad():
            e = to_np(D.net(torch.tensor(grid, dtype=torch.float32), torch.full((len(grid),), t)))
        out[f"field{t:g}"] = -e / s
        out[f"exact{t:g}"] = E.posterior(grid, a, s)[1]
    # samplers: DDPM (200 steps), DDIM (5 to 100 steps), the same noise
    xs, P = ddpm_vp(D, z, 200, seed=7, keep_every=10)
    out["ddpm"], out["ddpm_path"], out["sw_ddpm"] = xs[:600], P, E.dist(xs)
    out["ddim_steps"] = [5, 10, 20, 50, 100]
    for k in out["ddim_steps"]:
        xs, P = ddim_vp(D, z, k, keep_every=1)
        out[f"ddim{k}"], out[f"sw_ddim{k}"] = xs[:600], E.dist(xs)
        if k == 50:
            out["ddim_path"] = P
    out["data"], out["sw_noise"] = data[:1500], E.dist(z)
    out["sw_floor"] = E.floor(len(z))
    # Tweedie, with the network: its guess of the clean point against the exact posterior mean
    out["tw_rows"] = []
    for t in (0.2, 0.5, 0.8):
        a, s = vp(t)
        xv = a * x0e[:2000] + s * ne[:2000]
        ex0 = E.posterior(xv, a, s)[0]
        with torch.no_grad():
            e = to_np(D.net(torch.tensor(xv, dtype=torch.float32), torch.full((len(xv),), t)))
        net_x0 = (xv - s * e) / a
        out["tw_rows"].append(dict(t=t, err=float(np.linalg.norm(net_x0 - ex0, axis=1).mean()),
                                   spread=float(np.linalg.norm(ex0 - ex0.mean(0), axis=1).mean())))
    print("    DDPM {:.3f}; DDIM {}; noise {:.3f}; floor {:.3f}".format(
        out["sw_ddpm"], [round(out[f"sw_ddim{k}"], 3) for k in out["ddim_steps"]], out["sw_noise"], out["sw_floor"]),
        flush=True)
    return out


def load_denoiser(seed, kind="cos", param="eps"):
    import torch

    from videos.ai.ai21.compute import mlp

    C = cache()
    name = f"denoiser_s{seed}.pt" if (kind, param) == ("cos", "eps") else f"ablate_{kind}_{param}_s{seed}.pt"
    if not (C.dir / name).exists():
        C.load("denoiser" if (kind, param) == ("cos", "eps") else "ablate")
    net = mlp(2, 2)
    net.load_state_dict(torch.load(C.dir / name))
    net.eval()
    return Denoiser(net, param)


# ---------------------------------------------------------------------------
def compute_solvers_net():
    threads()
    D = load_denoiser(0)
    n = 2000
    z = E.rng(2022).normal(size=(n, 2))
    ref, _ = E.solve(D.np, z, "dpm2", 512, "edm")
    out = dict(nfes=E.NFES, solvers=[k for k, _ in E.SOLVERS], ref_sw=E.dist(ref), floor=E.floor(n))
    out.update(E.solver_sweep(D.np, z, ref, label="net "))
    print(f"    the network's own ODE solution: distance from the data {out['ref_sw']:.4f} (floor {out['floor']:.4f})",
          flush=True)
    return out


# ---------------------------------------------------------------------------
ABLATE = [("cos", "eps"), ("linb", "eps"), ("fm", "eps"), ("logn", "eps"), ("logn", "x0"), ("logn", "F")]
ABL_SIG = [0.02, 0.1, 0.3, 1.0, 3.0, 10.0]
ABL_CHECKS = [0, 500, 1500, 3000, STEPS] if not QUICK else [0, 100, STEPS]


def compute_ablate():
    import torch

    threads()
    C = cache()
    part = C.partial("ablate", dict(steps=STEPS, seeds=list(SEEDS), configs=ABLATE))
    n = 2000
    z = E.rng(2022).normal(size=(n, 2))
    data = E.sample(n, 11)
    x0e, ne = E.sample(2000, 35), E.rng(36).normal(size=(2000, 2))
    D_star = {s: E.denoise_edm(x0e + s * ne, s) for s in ABL_SIG}

    def evaluate(D):
        x_heun, _ = E.solve(D.np, z, "heun", 18, "edm")
        x_ddim, _ = E.solve(D.np, z, "ddim", 10, "edm")
        derr = [float(((D.np(x0e + s * ne, s) - D_star[s]) ** 2).sum(1).mean()) for s in ABL_SIG]
        return dict(sw_heun=E.dist(x_heun), sw_ddim10=E.dist(x_ddim), derr=derr)

    for kind, param in ABLATE:
        for seed in SEEDS:
            key = f"{kind}_{param}_s{seed}"
            if key in part:
                continue
            if (kind, param) == ("cos", "eps"):
                D = load_denoiser(seed)
                lc = []
            else:
                lc = []

                def on_check(step, D_):
                    lc.append((step, E.dist(E.solve(D_.np, z[:1000], "ddim", 20, "edm")[0])))

                D = train_denoiser(seed, kind, param, on_check=on_check, checks=ABL_CHECKS)
                torch.save(D.net.state_dict(), C.dir / f"ablate_{kind}_{param}_s{seed}.pt")
            r = evaluate(D)
            r["curve"] = lc
            part[key] = r
            print(f"    {key}: Heun-35 {r['sw_heun']:.4f}, DDIM-10 {r['sw_ddim10']:.4f}; D error by noise level "
                  + " ".join(f"{v:.4f}" for v in r["derr"]), flush=True)
    out = dict(configs=[f"{k}_{p}" for k, p in ABLATE], seeds=list(SEEDS), sig=ABL_SIG, floor=E.floor(n),
               checks=ABL_CHECKS)
    for kind, param in ABLATE:
        c = f"{kind}_{param}"
        rs = [part[f"{c}_s{s}"] for s in SEEDS]
        out[f"{c}_heun"] = [r["sw_heun"] for r in rs]
        out[f"{c}_ddim10"] = [r["sw_ddim10"] for r in rs]
        out[f"{c}_derr"] = np.array([r["derr"] for r in rs])
        if rs[0]["curve"]:
            out[f"{c}_curve"] = np.array([[v for _, v in r["curve"]] for r in rs])
    return out


# ---------------------------------------------------------------------------
# Flow matching: a velocity network v(x, tau), tau = 0 noise, 1 data
FM_CHECKS = [0, 100, 300, 1000, 3000, STEPS] if not QUICK else [0, 100, STEPS]
FM_STEPS = [1, 2, 4, 8, 16, 100]


def euler(net, z, steps, keep=False):
    import torch

    x = torch.tensor(z, dtype=torch.float32)
    path = [x.numpy().copy()] if keep else None
    with torch.no_grad():
        for i in range(steps):
            x = x + net(x, torch.full((len(x),), i / steps)) / steps
            if keep:
                path.append(x.numpy().copy())
    return x.numpy().astype(float), (np.array(path) if keep else None)


def train_fm(seed, coupling="indep", pairs=None, steps=STEPS, on_check=None, curve=None, width=256, label=None):
    import torch

    from videos.ai.ai21.compute import mlp

    torch.manual_seed(2022 + seed)  # Lipman et al.; Liu et al.
    net = mlp(2, 2, width=width)
    if label is not None:
        net.net[0] = torch.nn.Linear(2 + 32 + 3, width)  # + a one-hot label: A, I, or none
    opt = torch.optim.Adam(net.parameters(), lr=2e-3)
    sched = lr_sched(opt, steps)
    g = torch.Generator().manual_seed(seed)
    draw = mixture_torch(g)
    if on_check is not None:
        on_check(0, net)
    run = []
    for step in range(1, steps + 1):
        extra = None
        if pairs is not None:
            i = torch.randint(0, len(pairs[0]), (BATCH,), generator=g)
            x0, x1 = pairs[0][i], pairs[1][i]
        elif label is not None:
            X, Y = label
            i = torch.randint(0, len(X), (BATCH,), generator=g)
            x1, y = X[i], Y[i]
            drop = torch.rand(BATCH, generator=g) < 0.2  # one time in five, don't say which letter
            extra = torch.nn.functional.one_hot(torch.where(drop, torch.full_like(y, 2), y), 3).float()
            x0 = torch.randn(BATCH, 2, generator=g)
        else:
            x1 = draw(BATCH)
            x0 = torch.randn(BATCH, 2, generator=g)
            if coupling == "ot":  # pair this batch's noise and data optimally (Tong et al.; Pooladian et al.)
                from scipy.optimize import linear_sum_assignment

                cm = torch.cdist(x0, x1).pow(2).numpy()
                _, c = linear_sum_assignment(cm)
                x1 = x1[torch.tensor(c)]
        t = torch.rand(BATCH, generator=g)
        xt = (1 - t[:, None]) * x0 + t[:, None] * x1
        loss = ((net(xt, t, extra) - (x1 - x0)) ** 2).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
        run.append(float(loss))
        if curve is not None and step % 25 == 0:
            curve.append((step, float(np.mean(run))))
            run = []
        if on_check is not None and step in FM_CHECKS[1:]:
            on_check(step, net)
    net.eval()
    return net


def fm_eval(net, z, data):
    from videos.ai.ai21.compute import sw_distance

    r = {}
    for k in FM_STEPS:
        xs, P = euler(net, z, k, keep=(k == 100))
        r[f"sw{k}"] = E.dist(xs)
        r[f"x{k}"] = xs[:600].tolist()
        if k == 100:
            r["straight"] = E.straightness(P[:, :600])
            r["cost"] = float(((xs - z) ** 2).sum(1).mean())
            r["action"] = float((np.linalg.norm(np.diff(P, axis=0), axis=-1) ** 2).sum(0).mean() * 100)
            r["path"] = P[::5, :300].tolist()
    return r


def load_fm(name):
    import torch

    from videos.ai.ai21.compute import mlp

    C = cache()
    if not (C.dir / f"{name}.pt").exists():
        C.load("flow")
    net = mlp(2, 2)
    net.load_state_dict(torch.load(C.dir / f"{name}.pt"))
    net.eval()
    return net


def compute_flow():
    import torch

    threads()
    C = cache()
    part = C.partial("flow", dict(steps=STEPS, seeds=list(SEEDS)))
    n = 4000
    z = E.rng(1).normal(size=(n, 2))
    data = E.sample(n, 41)
    for seed in SEEDS:
        for kind in ("fm", "ot", "rf1", "rf2"):
            key = f"{kind}_s{seed}"
            if key in part and (C.dir / f"{key}.pt").exists():
                continue
            snaps, curve = [], []

            def on_check(step, net):
                if seed == 0 and kind == "fm":
                    snaps.append(euler(net, z[:600], 100)[0].tolist())

            if kind in ("fm", "ot"):
                net = train_fm(seed, coupling="indep" if kind == "fm" else "ot", on_check=on_check, curve=curve)
            else:
                teacher = load_fm(f"{'fm' if kind == 'rf1' else 'rf1'}_s{seed}")
                zz = E.rng(100 + seed + (0 if kind == "rf1" else 50)).normal(size=(20000, 2))
                x1, _ = euler(teacher, zz, 100)  # pair each noise point with where the teacher takes it
                net = train_fm(seed + 10 * (1 if kind == "rf1" else 2), curve=curve,
                               pairs=(torch.tensor(zz, dtype=torch.float32), torch.tensor(x1, dtype=torch.float32)))
            torch.save(net.state_dict(), C.dir / f"{key}.pt")
            r = fm_eval(net, z, data)
            r["curve"], r["snaps"] = curve, snaps
            part[key] = r
            print(f"    {key}: " + " ".join(f"{k}:{r[f'sw{k}']:.3f}" for k in FM_STEPS)
                  + f"; straightness {r['straight']:.3f}; cost {r['cost']:.3f}", flush=True)
    out = dict(kinds=["fm", "ot", "rf1", "rf2"], seeds=list(SEEDS), steps=FM_STEPS, checks=FM_CHECKS,
               sw_noise=E.dist(z), floor=E.floor(n))
    for kind in out["kinds"]:
        rs = [part[f"{kind}_s{s}"] for s in SEEDS]
        out[f"{kind}_sw"] = np.array([[r[f"sw{k}"] for k in FM_STEPS] for r in rs])  # seed, steps
        for m in ("straight", "cost", "action"):
            out[f"{kind}_{m}"] = [r[m] for r in rs]
        out[f"{kind}_path"] = np.array(rs[0]["path"])
        for k in (1, 2, 4):
            out[f"{kind}{k}"] = np.array(rs[0][f"x{k}"])
        out[f"{kind}100"] = np.array(rs[0]["x100"])
        out[f"{kind}_curve"] = np.array(rs[0]["curve"])
    out["fm_snaps"] = np.array(part["fm_s0"]["snaps"])
    return out


# ---------------------------------------------------------------------------
def compute_distill():
    """One-step students of the flow-matching teacher (seed s teaches seed s)."""
    import torch

    from videos.ai.ai21.compute import mlp, sw_distance

    threads()
    C = cache()
    C.load("flow")
    part = C.partial("distill", dict(steps=STEPS, seeds=list(SEEDS)))
    n = 4000
    z = E.rng(1).normal(size=(n, 2))
    data = E.sample(n, 41)
    zw = z[:600]
    rounds = [64, 32, 16, 8, 4, 2, 1]
    per_round = max(STEPS // 6, 50)
    for seed in SEEDS:
        teacher = load_fm(f"fm_s{seed}")
        for p_ in teacher.parameters():
            p_.requires_grad_(False)
        draw = None
        # ---------------- progressive distillation (Salimans & Ho): halve the steps, six times
        key = f"prog_s{seed}"
        if key not in part:
            torch.manual_seed(2022 + seed)
            g = torch.Generator().manual_seed(500 + seed)
            draw = mixture_torch(g)
            student = mlp(2, 2)
            student.load_state_dict(teacher.state_dict())
            prev = teacher
            rows, snaps = [dict(steps=64, sw=E.dist(euler(teacher, z, 64)[0]))], [euler(teacher, zw, 64)[0].tolist()]
            for N in rounds[1:]:
                opt = torch.optim.Adam(student.parameters(), lr=5e-4)
                h = 1 / (2 * N)  # the previous model's step
                for step in range(per_round):
                    x1 = draw(BATCH)
                    x0 = torch.randn(BATCH, 2, generator=g)
                    k = torch.randint(0, N, (BATCH,), generator=g).float()
                    t = k / N
                    xt = (1 - t[:, None]) * x0 + t[:, None] * x1
                    with torch.no_grad():  # two of the previous model's steps ...
                        xm = xt + h * prev(xt, t)
                        x2 = xm + h * prev(xm, t + h)
                        tgt = (x2 - xt) / (2 * h)
                    loss = ((student(xt, t) - tgt) ** 2).mean()  # ... in one of the student's
                    opt.zero_grad()
                    loss.backward()
                    opt.step()
                prev = mlp(2, 2)
                prev.load_state_dict(student.state_dict())
                for p_ in prev.parameters():
                    p_.requires_grad_(False)
                rows.append(dict(steps=N, sw=E.dist(euler(student, z, N)[0])))
                snaps.append(euler(student, zw, N)[0].tolist())
            part[key] = dict(rows=rows, snaps=snaps, one=euler(student, z, 1)[0][:600].tolist())
            print(f"    {key}: " + " ".join(f"{r['steps']}:{r['sw']:.3f}" for r in rows), flush=True)
        # ---------------- consistency distillation (Song et al. 2023): f(x, tau) jumps to the data end
        key = f"cd_s{seed}"
        if key not in part:
            torch.manual_seed(2023 + seed)
            g = torch.Generator().manual_seed(600 + seed)
            draw = mixture_torch(g)
            F_ = mlp(2, 2)
            F_.load_state_dict(teacher.state_dict())  # start from the teacher: f(x, tau) = x + (1 - tau) v

            def f(x, t):
                return x + (1 - t)[:, None] * F_(x, t)

            opt = torch.optim.Adam(F_.parameters(), lr=5e-4)
            sched = lr_sched(opt, STEPS)
            snaps, snap_at = [], [0, STEPS // 20, STEPS // 6, STEPS // 2, STEPS]
            for step in range(STEPS + 1):
                if step in snap_at:
                    with torch.no_grad():
                        snaps.append(to_np(f(torch.tensor(zw, dtype=torch.float32), torch.zeros(len(zw)))).tolist())
                if step == STEPS:
                    break
                Nk = 16 if step < STEPS // 3 else (32 if step < 2 * STEPS // 3 else 64)  # a coarse-to-fine curriculum
                x1 = draw(BATCH)
                x0 = torch.randn(BATCH, 2, generator=g)
                k = torch.randint(0, Nk, (BATCH,), generator=g).float()
                t, tn = k / Nk, (k + 1) / Nk
                xt = (1 - t[:, None]) * x0 + t[:, None] * x1
                with torch.no_grad():
                    xn = xt + (tn - t)[:, None] * teacher(xt, t)  # one teacher step along the ODE
                    tgt = f(xn, tn)  # the target: the student's own jump from there, held fixed
                loss = ((f(xt, t) - tgt) ** 2).sum(1).mean()
                opt.zero_grad()
                loss.backward()
                opt.step()
                sched.step()
            with torch.no_grad():
                one = to_np(f(torch.tensor(z, dtype=torch.float32), torch.zeros(n)))
            part[key] = dict(sw=E.dist(one), one=one[:600].tolist(), snaps=snaps, snap_at=snap_at)
            print(f"    {key}: one step {part[key]['sw']:.3f}", flush=True)
        # ---------------- distribution matching distillation (Yin et al. 2024)
        key = f"dmd_s{seed}"
        if key not in part:
            torch.manual_seed(2024 + seed)
            g = torch.Generator().manual_seed(700 + seed)
            G = mlp(2, 2)
            G.load_state_dict(teacher.state_dict())  # the generator x = z + v(z, 0): the teacher's one blurry step
            fake = mlp(2, 2)
            fake.load_state_dict(teacher.state_dict())  # a flow model of the generator's own samples

            def gen(zz):
                return zz + G(zz, torch.zeros(len(zz)))

            og = torch.optim.Adam(G.parameters(), lr=2e-4, betas=(0.0, 0.99))
            of = torch.optim.Adam(fake.parameters(), lr=1e-3, betas=(0.0, 0.99))
            g_steps = STEPS // 2
            snaps, snap_at = [], [0, g_steps // 20, g_steps // 6, g_steps // 2, g_steps]
            for step in range(g_steps + 1):
                if step in snap_at:
                    with torch.no_grad():
                        snaps.append(to_np(gen(torch.tensor(zw, dtype=torch.float32))).tolist())
                if step == g_steps:
                    break
                for _ in range(2):  # keep the fake model up to date with the generator (two updates a step)
                    with torch.no_grad():
                        x1 = gen(torch.randn(BATCH, 2, generator=g))
                    x0 = torch.randn(BATCH, 2, generator=g)
                    t = torch.rand(BATCH, generator=g)
                    xt = (1 - t[:, None]) * x0 + t[:, None] * x1
                    lf = ((fake(xt, t) - (x1 - x0)) ** 2).mean()
                    of.zero_grad()
                    lf.backward()
                    of.step()
                x1 = gen(torch.randn(BATCH, 2, generator=g))
                x0 = torch.randn(BATCH, 2, generator=g)
                t = 0.02 + 0.96 * torch.rand(BATCH, generator=g)
                xt = (1 - t[:, None]) * x0 + t[:, None] * x1
                with torch.no_grad():
                    # each model's guess of the clean end: x + (1 - t) v; their difference is the KL's gradient
                    real = xt + (1 - t)[:, None] * teacher(xt, t)
                    fk = xt + (1 - t)[:, None] * fake(xt, t)
                    w = (x1 - real).abs().mean(1, keepdim=True) + 1e-3  # DMD's normalization
                    grad = (fk - real) / w
                loss = 0.5 * ((x1 - (x1 - grad).detach()) ** 2).sum(1).mean()
                og.zero_grad()
                loss.backward()
                og.step()
            with torch.no_grad():
                one = to_np(gen(torch.tensor(z, dtype=torch.float32)))
            part[key] = dict(sw=E.dist(one), one=one[:600].tolist(), snaps=snaps, snap_at=snap_at)
            print(f"    {key}: one step {part[key]['sw']:.3f}", flush=True)
    out = dict(seeds=list(SEEDS), rounds=rounds, per_round=per_round, steps=STEPS, batch=BATCH,
               sw_noise=E.dist(z), floor=E.floor(n))
    out["prog_sw"] = np.array([[r["sw"] for r in part[f"prog_s{s}"]["rows"]] for s in SEEDS])
    out["prog_snaps"] = np.array(part["prog_s0"]["snaps"])
    for k in ("cd", "dmd"):
        out[f"{k}_sw"] = [part[f"{k}_s{s}"]["sw"] for s in SEEDS]
        out[f"{k}_one"] = np.array(part[f"{k}_s0"]["one"])
        out[f"{k}_snaps"] = np.array(part[f"{k}_s0"]["snaps"])
        out[f"{k}_snap_at"] = part[f"{k}_s0"]["snap_at"]
    out["prog_one"] = np.array(part["prog_s0"]["one"])
    return out


# ---------------------------------------------------------------------------
GUIDE_W = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0]
AUTO_W = [1.0, 1.5, 2.0, 3.0, 4.0]
CLS_W = [0.0, 0.5, 1.0, 2.0, 4.0, 8.0]


def letters():
    from videos.ai.ai21.compute import ai_points

    A = ai_points(text="A", n=3000, seed=0) * 0.8 + np.array([-1.6, 0])
    I_ = ai_points(text="I", n=3000, seed=1) * 0.8 + np.array([1.6, 0])
    return A, I_


def prec_recall(gen, real, k=5):
    """Kynkaanniemi et al.: precision = share of generated points inside some real point's k-NN ball; recall = share
    of real points inside some generated point's k-NN ball."""
    def radii(X):
        d = np.sqrt(((X[:, None] - X[None]) ** 2).sum(-1))
        return np.sort(d, 1)[:, k]

    rr, rg = radii(real), radii(gen)
    d = np.sqrt(((gen[:, None] - real[None]) ** 2).sum(-1))  # gen x real
    prec = float((d <= rr[None]).any(1).mean())
    rec = float((d <= rg[:, None]).any(0).mean())
    return prec, rec


def compute_guidance():
    import torch

    from videos.ai.ai21.compute import mlp, sw_distance

    threads()
    C = cache()
    part = C.partial("guidance", dict(steps=STEPS, seeds=list(SEEDS), w=GUIDE_W, auto=AUTO_W, cls=CLS_W))
    A, I_ = letters()
    X = torch.tensor(np.concatenate([A, I_]), dtype=torch.float32)
    Y = torch.tensor([0] * len(A) + [1] * len(I_))
    z = E.rng(3).normal(size=(1000, 2))
    realA = A[E.rng(4).permutation(len(A))[:1000]]
    oh = lambda c, m: torch.nn.functional.one_hot(torch.full((m,), c), 3).float()

    def sample(vfun, steps=60):
        x = torch.tensor(z, dtype=torch.float32)
        with torch.no_grad():
            for k in range(steps):
                t = torch.full((len(x),), k / steps)
                x = x + vfun(x, t) / steps
        return x.numpy().astype(float)

    def measure(xs):
        p, r = prec_recall(xs, realA)
        return dict(onA=float((xs[:, 0] < 0).mean()), prec=p, rec=r, sw=sw_distance(xs, A),
                    spread=float(np.linalg.norm(xs[xs[:, 0] < 0] - xs[xs[:, 0] < 0].mean(0), axis=1).mean())
                    if (xs[:, 0] < 0).any() else 0.0)

    for seed in SEEDS:
        key = f"s{seed}"
        if key in part:
            continue
        snaps = []

        def on_check(step, net):
            if seed == 0:
                snaps.append(sample(lambda x, t: net(x, t, oh(0, len(x))), 30)[:500].tolist())

        strong = train_fm(seed, label=(X, Y), on_check=on_check)
        weak = train_fm(seed + 100, label=(X, Y), steps=max(STEPS // 8, 50), width=64)  # smaller, and trained less
        # a noisy classifier p(letter | x_tau, tau): Bayes turns its gradient into guidance
        torch.manual_seed(3000 + seed)
        clf = mlp(2, 2, width=128)
        oc = torch.optim.Adam(clf.parameters(), lr=2e-3)
        g = torch.Generator().manual_seed(800 + seed)
        for step in range(STEPS // 2):
            i = torch.randint(0, len(X), (BATCH,), generator=g)
            x1, y = X[i], Y[i]
            x0 = torch.randn(BATCH, 2, generator=g)
            t = torch.rand(BATCH, generator=g)
            lc = torch.nn.functional.cross_entropy(clf((1 - t[:, None]) * x0 + t[:, None] * x1, t), y)
            oc.zero_grad()
            lc.backward()
            oc.step()
        for p_ in clf.parameters():
            p_.requires_grad_(False)

        def cls_vel(w):
            def v(x, t):
                vu = strong(x, t, oh(2, len(x)))
                if w == 0:
                    return vu
                with torch.enable_grad():
                    xg = x.clone().requires_grad_(True)
                    lp = torch.log_softmax(clf(xg, t), 1)[:, 0].sum()
                    gr = torch.autograd.grad(lp, xg)[0]
                # the score gains w grad log p(A | x); for the straight path that moves the velocity by (1 - t)/t times it
                tt = torch.clamp(t, min=0.05)
                return vu + w * ((1 - tt) / tt)[:, None] * gr
            return v

        res = {"cfg": [], "auto": [], "cls": []}
        for w in GUIDE_W:
            xs = sample(lambda x, t: (lambda vc, vu: vu + w * (vc - vu))(strong(x, t, oh(0, len(x))), strong(x, t, oh(2, len(x)))))
            res["cfg"].append(dict(w=w, **measure(xs), x=xs[:500].tolist()))
        for w in AUTO_W:
            xs = sample(lambda x, t: (lambda vs, vw: vw + w * (vs - vw))(strong(x, t, oh(0, len(x))), weak(x, t, oh(0, len(x)))))
            res["auto"].append(dict(w=w, **measure(xs), x=xs[:500].tolist()))
        for w in CLS_W:
            xs = sample(cls_vel(w))
            res["cls"].append(dict(w=w, **measure(xs), x=xs[:500].tolist()))
        res["snaps"] = snaps
        part[key] = res
        for m in ("cfg", "auto", "cls"):
            print(f"    seed {seed} {m}: " + " ".join(f"w={r['w']:g}: A {r['onA']:.0%} P {r['prec']:.2f} R {r['rec']:.2f}"
                                                   for r in res[m]), flush=True)
    out = dict(seeds=list(SEEDS), w=GUIDE_W, auto_w=AUTO_W, cls_w=CLS_W, A=A[:800], I=I_[:800], steps=STEPS)
    for m in ("cfg", "auto", "cls"):
        for q in ("onA", "prec", "rec", "sw", "spread"):
            out[f"{m}_{q}"] = np.array([[r[q] for r in part[f"s{s}"][m]] for s in SEEDS])  # seed, w
        out[f"{m}_x"] = np.array([r["x"] for r in part["s0"][m]])
    out["snaps"] = np.array(part["s0"]["snaps"])
    out["snap_steps"] = FM_CHECKS
    p_real, r_real = prec_recall(A[E.rng(5).permutation(len(A))[:1000]], realA)
    out["real_prec"], out["real_rec"] = p_real, r_real
    return out
