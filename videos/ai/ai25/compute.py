"""Precompute everything numerical in Part 25 of the AI series ("Symmetry and Science").

    python -m videos.ai.ai25.compute                 # everything missing
    python -m videos.ai.ai25.compute --force nbody

Results are cached in ``.cache/ai25/<name>.json`` (+ ``.npz``); trained weights in ``.cache/ai25/models/``; scenes call
``load(name)``.  Every model is trained here, on the CPU, on one or two torch threads (``AI25_THREADS``), seeded (numpy
``default_rng`` and ``torch.manual_seed``, one generator per run).  No multiprocessing.  The sweeps save every run as
it finishes (``CACHE.partial``), so a killed computation resumes where it stopped; the items that need trained
weights train them themselves if they are missing.  About two and a half CPU-hours on a busy 4-core machine.

Symmetry (physics.py, graphs.py):
    nbody_data  the charged five-body system: 3,000 training, 500 validation and 1,000 test systems, and a few
                trajectories to draw
    nbody       predicting where the five particles are at t = 1: an E(3)-equivariant network (EGNN), a message-passing
                network fed raw coordinates, an MLP, and the MLP trained on randomly rotated copies; 100 to 3,000
                training systems, three seeds, the same 3,000 steps each; seed 0 at 3,000 systems replayed
    energy      predicting the potential energy: an invariant network (distances only) against the MLP, with and
                without rotated copies, three seeds
    equivariance  turn the inputs, compare the outputs: every trained model, 500 test systems, random rotations and
                translations; the hook's molecule turned through a full circle
    harmonics   how a rotation acts on the spherical harmonics of degree 0, 1, 2: a block-diagonal matrix
    deepsets    four shapes of sixteen points: Deep Sets against an MLP and an MLP shown reordered copies, 32 to 8,192
                training sets, three seeds; how often a reordering changes the answer
    setcurves   the same three networks trained on 512 sets (seed 0), held-out accuracy every 200 steps
    wl          1-WL colour refinement on decalin and bicyclopentyl, on a hexagon and two triangles, on two trees;
                how often it separates random graphs and random 3-regular graphs
    gin         unions of cycles, "is there a triangle?": GIN (sum, mean, max), GIN with random node features, and a
                network over pairs of nodes, three seeds, seed 0's training curves; the degree task that mean and max
                can't learn
    sbm         a graph of three communities: a GCN against an MLP, three seeds, seed 0 replayed; receptive fields
    oversmooth  repeated averaging and the Dirichlet energy; plain and residual GCNs of depth 2 to 64, three seeds

Proteins (proteins.py):
    fold        a three-helix bundle: classical MDS from its distances; gradient descent on noisy partial distances
                from twelve random starts (the mirror image); FAPE against distance errors
    pair        completing a distance matrix: per-pair updates against triangle updates, and triangle updates with
                recycling, three seeds; one chain's matrix during training and after each recycle
    diffusion   denoising diffusion on compact 2D chains: an E(2)-equivariant denoiser against a plain one trained on
                rotated copies, two seeds; samples, bond lengths, clashes

Fields (fields.py):
    fno         Burgers' equation: a Fourier neural operator and a CNN trained at 64 points, tested from 32 to 1,024,
                three seeds; seed 0 replayed
    weather     forced vorticity on a 32 x 32 periodic square: a mesh graph network (multimesh) and the same network on
                the finest mesh only, trained one step at a time and rolled out 40 steps; persistence and climatology

Discovery (discovery.py):
    materials   a synthetic chemistry of 6,840 candidate compounds: the active-learning flywheel against random picks,
                three seeds; one binary system's hull
    matmul      tensor decompositions of 2 x 2 and 3 x 3 matrix multiplication by alternating least squares from random
                starts, at several ranks
    binpack     evolving priority functions for online bin packing, two seeds, against first fit and best fit
"""

from __future__ import annotations

import os
import time

import numpy as np
import torch

from explainer.ai.cache import Cache
from videos.ai.ai25 import discovery as dc
from videos.ai.ai25 import fields as fd
from videos.ai.ai25 import graphs as gr
from videos.ai.ai25 import physics as ph
from videos.ai.ai25 import proteins as pr

CACHE = Cache("ai25")
load = CACHE.load
MODELS = CACHE.dir / "models"
SEEDS = (0, 1, 2)


def _threads():
    torch.set_num_threads(int(os.environ.get("AI25_THREADS", "1")))


def tolist(x):
    """numpy (nested in dicts and lists) to plain JSON values, floats rounded to 7 significant digits."""
    if isinstance(x, dict):
        return {k: tolist(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [tolist(v) for v in x]
    if isinstance(x, np.ndarray):
        if x.dtype.kind in "iub":
            return x.tolist()
        return [float(f"{v:.7g}") for v in x.ravel()] if x.ndim == 1 else [tolist(r) for r in x]
    if isinstance(x, np.floating):
        return float(f"{float(x):.7g}")
    if isinstance(x, np.integer):
        return int(x)
    if isinstance(x, np.bool_):
        return bool(x)
    if isinstance(x, torch.Tensor):
        return tolist(x.detach().numpy())
    if isinstance(x, float):
        return float(f"{x:.7g}")
    return x


def log(msg: str) -> None:
    print(f"    {time.strftime('%H:%M:%S')} {msg}", flush=True)


def save_model(m, name: str) -> None:
    MODELS.mkdir(parents=True, exist_ok=True)
    tmp = MODELS / f"{name}.tmp.pt"
    torch.save(m.state_dict(), tmp)
    tmp.replace(MODELS / f"{name}.pt")


def load_model(m, name: str, item: str):
    p = MODELS / f"{name}.pt"
    if not p.exists():  # the item's json without its weights (deleted by hand): train it again
        CACHE.save(item, ITEMS[item]())
    m.load_state_dict(torch.load(p))
    m.eval()
    return m


def _rng_state(rng: np.random.Generator):
    return rng.bit_generator.state


# ===========================================================================
# Symmetry: the five charged bodies
# ===========================================================================
N_SIZES = (100, 300, 1000, 3000)
DYN_KINDS = ("egnn", "gnn", "mlp", "mlp_aug")
DYN_STEPS = 3000
SNAPS = (0, 50, 150, 300, 600, 1000, 1500, 2200, 3000)


def compute_nbody_data():
    tr = ph.simulate(3000, seed=11)
    va = ph.simulate(500, seed=12)
    te = ph.simulate(1000, seed=13)
    show = ph.simulate(6, seed=14, keep_every=20)
    out = {}
    for name, d in (("train", tr), ("val", va), ("test", te)):
        for k, v in d.items():
            out[f"{name}_{k}"] = v
    for k, v in show.items():
        out[f"show_{k}"] = v
    te_cv = te["x0"] + te["v0"] * 1.0
    out.update(drift=ph.energy_drift(), eps=ph.EPS, dt=ph.DT, steps=ph.STEPS,
               mse_still=float(((te["x0"] - te["xT"]) ** 2).mean()),
               mse_constvel=float(((te_cv - te["xT"]) ** 2).mean()))
    return out


def _split(d, name):
    return {k: d[f"{name}_{k}"] for k in ("x0", "v0", "q", "xT")}


def compute_nbody():
    _threads()
    d = load("nbody_data")
    tr, va, te = _split(d, "train"), _split(d, "val"), _split(d, "test")
    val = [torch.from_numpy(va[k]) for k in ("x0", "v0", "q", "xT")]
    test = [torch.from_numpy(te[k]) for k in ("x0", "v0", "q", "xT")]
    show = [torch.from_numpy(d[f"show_{k}"]) for k in ("x0", "v0", "q")]
    part = CACHE.partial("nbody", dict(sizes=N_SIZES, kinds=DYN_KINDS, steps=DYN_STEPS, seeds=SEEDS, v=1))

    def snap(m):
        with torch.no_grad():
            return m(*show).numpy().tolist()

    for n in N_SIZES[::-1]:
        for kind in DYN_KINDS:
            for s in SEEDS:
                key = f"{kind}_{n}_s{s}"
                if key in part:
                    continue
                replay = n == N_SIZES[-1] and s == 0
                m, r = ph.train_dynamics(kind, tr, n, s, DYN_STEPS, batch=64, val=val,
                                         snaps=SNAPS if replay else (), snap_fn=snap if replay else None)
                with torch.no_grad():
                    mse = float(torch.nn.functional.mse_loss(m(*test[:3]), test[3]))
                if replay:
                    save_model(m, f"dyn_{kind}")
                part[key] = dict(mse=mse, curve=r["curve"], frames=r["frames"], secs=r["secs"], params=r["params"])
                log(f"nbody {key}: test MSE {mse:.4f} ({r['secs']:.0f}s)")
    out = dict(sizes=list(N_SIZES), kinds=list(DYN_KINDS), seeds=list(SEEDS), steps=DYN_STEPS, snaps=list(SNAPS))
    for k in part.done:
        out[k] = part[k]
    out["table"] = {kind: {str(n): [part[f"{kind}_{n}_s{s}"]["mse"] for s in SEEDS] for n in N_SIZES}
                    for kind in DYN_KINDS}
    out["params"] = {kind: part[f"{kind}_{N_SIZES[-1]}_s0"]["params"] for kind in DYN_KINDS}
    return out


def _dyn_model(kind):
    return load_model(ph.DYN_MODELS[kind](), f"dyn_{kind}", "nbody")


E_KINDS = ("inv", "mlp", "mlp_aug")


def compute_energy():
    _threads()
    d = load("nbody_data")
    x, q = torch.from_numpy(d["train_x0"]), torch.from_numpy(d["train_q"])
    u = torch.from_numpy(ph.potential(d["train_x0"], d["train_q"]).astype(np.float32))
    xv, qv = torch.from_numpy(d["val_x0"]), torch.from_numpy(d["val_q"])
    uv = torch.from_numpy(ph.potential(d["val_x0"], d["val_q"]).astype(np.float32))
    xt, qt = torch.from_numpy(d["test_x0"]), torch.from_numpy(d["test_q"])
    ut = ph.potential(d["test_x0"], d["test_q"]).astype(np.float32)
    part = CACHE.partial("energy", dict(kinds=E_KINDS, seeds=SEEDS, steps=DYN_STEPS, v=1))
    for kind in E_KINDS:
        for s in SEEDS:
            key = f"{kind}_s{s}"
            if key in part:
                continue
            m, r = ph.train_energy(kind, x, q, u, s, DYN_STEPS, val=(xv, qv, uv))
            with torch.no_grad():
                pred = m(xt, qt).numpy()
            if s == 0:
                save_model(m, f"energy_{kind}")
            part[key] = dict(mse=float(((pred - ut) ** 2).mean()), curve=r["curve"], secs=r["secs"],
                             params=r["params"])
            log(f"energy {key}: test MSE {part[key]['mse']:.4f}")
    out = dict(kinds=list(E_KINDS), u_var=float(ut.var()))
    for k in part.done:
        out[k] = part[k]
    return out


def _energy_model(kind):
    return load_model(ph.ENERGY_MODELS[kind](), f"energy_{kind}", "energy")


def compute_equivariance():
    """Turn the inputs, compare the outputs.  Dynamics: |f(Rx + t, Rv) - (R f(x, v) + t)|, RMS over particles, against
    the model's own test error.  Energy: |U(Rx + t) - U(x)|.  And one system turned through a full circle."""
    _threads()
    d = load("nbody_data")
    te = _split(d, "test")
    n = 500
    x, v, q = (torch.from_numpy(te[k][:n]) for k in ("x0", "v0", "q"))
    gen = torch.Generator().manual_seed(77)
    R = ph.random_rotations(n, gen)
    t = torch.randn(n, 1, 3, generator=gen) * 2.0
    rot = lambda a: torch.einsum("bij,bnj->bni", R, a)  # noqa: E731
    out = dict(n=n)
    with torch.no_grad():
        for kind in DYN_KINDS:
            m = _dyn_model(kind)
            y = m(x, v, q)
            y_rot = m(rot(x) + t, rot(v), q)
            err = torch.sqrt(((y_rot - (rot(y) + t)) ** 2).sum(-1).mean(-1))
            out[f"dyn_{kind}"] = dict(err=float(err.mean()), err_max=float(err.max()),
                                      test_rmse=float(torch.sqrt(((y - torch.from_numpy(te["xT"][:n])) ** 2)
                                                                 .sum(-1).mean())))
            # translations alone, and a reordering of the particles alone
            y_tr = m(x + t, v, q)
            perm = torch.randperm(5, generator=gen)
            y_perm = m(x[:, perm], v[:, perm], q[:, perm])
            out[f"dyn_{kind}"]["err_translate"] = float(torch.sqrt(((y_tr - (y + t)) ** 2).sum(-1).mean(-1)).mean())
            out[f"dyn_{kind}"]["err_permute"] = float(torch.sqrt(((y_perm - y[:, perm]) ** 2).sum(-1).mean(-1)).mean())
            log(f"equivariance {kind}: {out[f'dyn_{kind}']}")
        for kind in E_KINDS:
            m = _energy_model(kind)
            u0 = m(x, q)
            u1 = m(rot(x) + t, q)
            out[f"energy_{kind}"] = dict(err=float((u1 - u0).abs().mean()), err_max=float((u1 - u0).abs().max()),
                                         spread=float(u0.std()))
        # the hook: one system turned about a tilted axis through a full circle
        k = int(np.argmin(np.abs(ph.potential(te["x0"][:50], te["q"][:50]) + 1.0)))  # an unremarkable one
        x1, v1, q1 = x[k:k + 1], v[k:k + 1], q[k:k + 1]
        thetas = np.linspace(0, 2 * np.pi, 73)
        axis = np.array([0.3, 1.0, 0.2])
        Rs = torch.tensor(np.stack([ph.rot_axis(axis, th) for th in thetas]), dtype=torch.float32)
        xs = torch.einsum("bij,nj->bni", Rs, x1[0])
        vs = torch.einsum("bij,nj->bni", Rs, v1[0])
        qs = q1.expand(len(thetas), -1)
        out["sweep_theta"] = thetas
        out["sweep_k"] = k
        out["sweep_true_energy"] = float(ph.potential(te["x0"][k:k + 1], te["q"][k:k + 1])[0])
        for kind in E_KINDS:
            out[f"sweep_energy_{kind}"] = _energy_model(kind)(xs, qs).numpy()
        for kind in DYN_KINDS:
            y = _dyn_model(kind)(xs, vs, qs)
            back = torch.einsum("bji,bnj->bni", Rs, y)  # R^T f(R x): equals f(x) for an equivariant model
            out[f"sweep_dyn_{kind}"] = back.numpy()
        out["sweep_x0"] = te["x0"][k]
        out["sweep_v0"] = te["v0"][k]
        out["sweep_q"] = te["q"][k]
        out["sweep_xT"] = te["xT"][k]
    return out


def compute_harmonics():
    R = ph.rot_axis([0.4, -0.7, 0.6], 1.1)
    D = ph.wigner_blocks(R)
    blocks = [(0, 1), (1, 4), (4, 9)]
    off = np.ones((9, 9), bool)
    for a, b in blocks:
        off[a:b, a:b] = False
    orth = [float(np.abs(D[a:b, a:b] @ D[a:b, a:b].T - np.eye(b - a)).max()) for a, b in blocks]
    return dict(D=D, off_max=float(np.abs(D[off]).max()), orth_err=orth, R=R)


# ===========================================================================
# Sets
# ===========================================================================
SET_SIZES = (32, 128, 512, 2048, 8192)
SET_KINDS = ("deepsets", "mlp_aug", "mlp")


SET_CURVE_N = 512


def compute_setcurves():
    """The training of the three set networks at one training-set size, test accuracy every 200 steps (seed 0: the
    same networks as in the 'deepsets' item, which ends where these curves end)."""
    _threads()
    Xte, yte = gr.point_sets(4000, np.random.default_rng(0))
    X, y = gr.point_sets(SET_CURVE_N, np.random.default_rng(1000 + SET_CURVE_N))
    out = dict(n=SET_CURVE_N)
    for kind in SET_KINDS:
        m, r = gr.train_sets(kind, X, y, 0, val=(Xte[:1000], yte[:1000]), every=200)
        out[kind] = np.array(r["curve"])
        log(f"setcurves {kind}: final {r['curve'][-1]}")
    return out


def compute_deepsets():
    _threads()
    Xte, yte = gr.point_sets(4000, np.random.default_rng(0))
    part = CACHE.partial("deepsets", dict(sizes=SET_SIZES, kinds=SET_KINDS, seeds=SEEDS, v=3, steps=gr.SET_STEPS))
    for n in SET_SIZES:
        X, y = gr.point_sets(n, np.random.default_rng(1000 + n))
        for kind in SET_KINDS:
            for s in SEEDS:
                key = f"{kind}_{n}_s{s}"
                if key in part:
                    continue
                m, r = gr.train_sets(kind, X, y, s)
                sc = gr.set_scores(m, Xte, yte, torch.Generator().manual_seed(99))
                part[key] = dict(sc, secs=r["secs"], params=r["params"])
                if n == SET_SIZES[-1] and s == 0:
                    save_model(m, f"sets_{kind}")
                log(f"deepsets {key}: {sc}")
    out = dict(sizes=list(SET_SIZES), kinds=list(SET_KINDS), seeds=list(SEEDS), shapes=list(gr.SHAPES),
               steps=gr.SET_STEPS)
    for k in part.done:
        out[k] = part[k]
    # four example sets, one per shape, and one set shown in two orders to both networks
    ex = [Xte[np.flatnonzero(yte == c)[0]] for c in range(4)]
    out["examples"] = np.array(ex)
    ds = load_model(gr.DeepSets(), "sets_deepsets", "deepsets")
    mm = load_model(gr.SetMLP(), "sets_mlp", "deepsets")
    one = torch.from_numpy(ex[0][None])
    perm = torch.from_numpy(np.random.default_rng(5).permutation(gr.SET_N))
    with torch.no_grad():
        out["demo_perm"] = perm.numpy()
        out["demo_ds_latent"] = ds.latent(one)[0].numpy()[:12]
        out["demo_ds_latent_perm"] = ds.latent(one[:, perm])[0].numpy()[:12]
        out["demo_ds_prob"] = torch.softmax(ds(one), -1)[0].numpy()
        out["demo_ds_prob_perm"] = torch.softmax(ds(one[:, perm]), -1)[0].numpy()
        out["demo_mlp_prob"] = torch.softmax(mm(one), -1)[0].numpy()
        out["demo_mlp_prob_perm"] = torch.softmax(mm(one[:, perm]), -1)[0].numpy()
    return out


# ===========================================================================
# Graphs
# ===========================================================================
def _layout(n, edges, seed):
    import networkx as nx

    G = nx.Graph()
    G.add_nodes_from(range(n))
    G.add_edges_from(edges)
    pos = nx.kamada_kawai_layout(G)
    P = np.array([pos[i] for i in range(n)])
    P -= P.mean(0)
    return P / np.abs(P).max()


def compute_wl():
    import networkx as nx

    pairs = {
        "molecules": (gr.decalin(), gr.bicyclopentyl()),
        "cycles": ((6, gr.cycle_edges([6])), (6, gr.cycle_edges([3, 3]))),
        "trees": ((7, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (1, 6)]),
                  (7, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (2, 6)])),
    }
    out = {}
    for name, (g1, g2) in pairs.items():
        r = gr.wl_refine([g1, g2])
        out[name] = dict(n=[g1[0], g2[0]], edges=[g1[1], g2[1]], colors=r["colors"], differ=r["differ"],
                         layout=[_layout(*g1, 0), _layout(*g2, 0)])
    # random graphs: how often does 1-WL tell two non-isomorphic graphs apart?
    rng = np.random.default_rng(3)
    tried = sep = 0
    while tried < 300:
        a = nx.gnp_random_graph(10, 0.3, seed=int(rng.integers(1 << 30)))
        b = nx.gnp_random_graph(10, 0.3, seed=int(rng.integers(1 << 30)))
        if a.number_of_edges() != b.number_of_edges() or nx.is_isomorphic(a, b):
            continue
        tried += 1
        sep += gr.wl_distinguishes((10, list(a.edges())), (10, list(b.edges())))
    out["random_pairs"], out["random_separated"] = tried, sep
    tried = sep = 0
    while tried < 100:
        a = nx.random_regular_graph(3, 10, seed=int(rng.integers(1 << 30)))
        b = nx.random_regular_graph(3, 10, seed=int(rng.integers(1 << 30)))
        if nx.is_isomorphic(a, b):
            continue
        tried += 1
        sep += gr.wl_distinguishes((10, list(a.edges())), (10, list(b.edges())))
    out["regular_pairs"], out["regular_separated"] = tried, sep
    return out


def compute_gin():
    _threads()
    A, y, parts = gr.regular_dataset(2000, np.random.default_rng(0))
    At, yt, pt = gr.regular_dataset(600, np.random.default_rng(1))
    X = np.ones(A.shape[:2] + (1,), np.float32)
    Xt = np.ones(At.shape[:2] + (1,), np.float32)
    part = CACHE.partial("gin", dict(v=3, seeds=SEEDS))
    kinds = {"gin": (lambda: gr.GIN(1), False, 1500), "gin_rni": (lambda: gr.GIN(5), True, 4000),
             "pair": (lambda: gr.PairNet(), False, 3000)}
    for kind, (make, rni, steps) in kinds.items():
        for s in SEEDS:
            key = f"{kind}_s{s}"
            if key in part:
                continue
            torch.manual_seed(s)  # the initial weights, too
            m = gr.train_graph_classifier(make(), A, X, y, s, steps=steps, rni=rni,
                                          val=(At[:300], Xt[:300], yt[:300]) if s == 0 else None)
            g = torch.Generator().manual_seed(3)
            acc = gr.graph_accuracy(m, At, Xt, yt, rni=rni, gen=g, reps=8)
            acc_tr = gr.graph_accuracy(m, A[:600], X[:600], y[:600], rni=rni, gen=g, reps=8)
            rec = dict(acc=acc, acc_train=acc_tr, curve=m.curve)
            if kind == "gin":
                with torch.no_grad():
                    o = m(torch.from_numpy(At), torch.from_numpy(Xt))
                rec["spread"] = float(o.std(0).max())
            part[key] = rec
            log(f"gin {key}: {rec}")
    # node degrees from constant features: sum aggregation can count, mean and max cannot
    rng = np.random.default_rng(4)
    As = []
    for _ in range(400):
        Ad = (rng.uniform(size=(12, 12)) < 0.3).astype(np.float32)
        Ad = np.triu(Ad, 1)
        As.append(Ad + Ad.T)
    As = np.array(As)
    deg = As.sum(-1)
    Xd = np.ones(As.shape[:2] + (1,), np.float32)
    for agg in ("sum", "mean", "max"):
        for s in SEEDS:
            key = f"deg_{agg}_s{s}"
            if key in part:
                continue
            torch.manual_seed(s)
            m = gr.GIN(1, 32, 1, 1, agg=agg)
            opt = torch.optim.Adam(m.parameters(), 3e-3)
            Ad_t, Xd_t, dt = torch.from_numpy(As[:300]), torch.from_numpy(Xd[:300]), torch.from_numpy(deg[:300])
            for _ in range(1500):
                pred = m.out(m.node_states(Ad_t, Xd_t)).squeeze(-1)
                loss = ((pred - dt) ** 2).mean()
                opt.zero_grad()
                loss.backward()
                opt.step()
            with torch.no_grad():
                pred = m.out(m.node_states(torch.from_numpy(As[300:]), torch.from_numpy(Xd[300:]))).squeeze(-1)
            part[key] = dict(rmse=float(torch.sqrt(((pred - torch.from_numpy(deg[300:])) ** 2).mean())),
                             exact=float((pred.round() == torch.from_numpy(deg[300:])).float().mean()))
            log(f"gin {key}: {part[key]}")
    out = dict(base_rate=float(yt.mean()), base_rate_train=float(y.mean()), n_nodes=int(A.shape[1]),
               partitions=sorted({tuple(p) for p in parts}), deg_std=float(deg[300:].std()))
    for k in part.done:
        out[k] = part[k]
    # three example graphs to draw
    ex = []
    for p in ([15], [3, 12], [3, 3, 9]):
        ex.append(dict(parts=p, n=15, edges=gr.cycle_edges(p)))
    out["examples"] = ex
    return out


def _fit_node(model, X, Ah, y, tr, epochs=300, lr=0.01, wd=5e-4, snaps=(), seed=0):
    torch.manual_seed(seed)
    opt = torch.optim.Adam(model.parameters(), lr, weight_decay=wd)
    Xt, yt, trm = torch.from_numpy(X), torch.from_numpy(y).long(), torch.from_numpy(tr)
    frames, curve = [], []
    for e in range(epochs + 1):
        if e in snaps:
            model.eval()
            with torch.no_grad():
                frames.append(model(Xt, Ah).argmax(1).numpy().tolist())
        if e % 10 == 0:
            model.eval()
            with torch.no_grad():
                p = model(Xt, Ah).argmax(1).numpy()
            curve.append((e, float((p[~tr] == y[~tr]).mean())))
        if e == epochs:
            break
        model.train()
        loss = torch.nn.functional.cross_entropy(model(Xt, Ah)[trm], yt[trm])
        opt.zero_grad()
        loss.backward()
        opt.step()
    model.eval()
    with torch.no_grad():
        p = model(Xt, Ah).argmax(1).numpy()
    return float((p[~tr] == y[~tr]).mean()), frames, curve


SBM_SNAPS = (0, 2, 5, 10, 20, 40, 80, 300)


def compute_sbm():
    _threads()
    out = dict(snaps=list(SBM_SNAPS))
    for s in SEEDS:
        rng = np.random.default_rng(s)
        A, X, y = gr.sbm(rng)
        tr = gr.split_masks(y, rng)
        Ah = torch.from_numpy(gr.norm_adj(A))
        torch.manual_seed(s)
        acc_m, fm, cm = _fit_node(gr.NodeMLP(8, 16, 3), X, Ah, y, tr, snaps=SBM_SNAPS if s == 0 else (), seed=s)
        torch.manual_seed(s)
        acc_g, fg, cg = _fit_node(gr.GCN(8, 16, 3, 2), X, Ah, y, tr, snaps=SBM_SNAPS if s == 0 else (), seed=s)
        out[f"s{s}"] = dict(mlp=acc_m, gcn=acc_g, deg=float(A.sum(1).mean()),
                            intra=float((A * (y[:, None] == y[None])).sum() / A.sum()))
        log(f"sbm s{s}: MLP {acc_m:.3f}, GCN {acc_g:.3f}")
        if s == 0:
            iu = np.argwhere(np.triu(A, 1) > 0)
            out.update(edges=iu, y=y, train=tr, frames_gcn=fg, frames_mlp=fm, curve_gcn=cg, curve_mlp=cm,
                       layout=_layout(len(A), [tuple(e) for e in iu], 0))
            # receptive fields: the nodes within k hops of one node
            v = int(np.argmax(A.sum(1) == np.median(A.sum(1))))
            d = gr.bfs_dist(A, v)
            out["rf_node"], out["rf_dist"] = v, np.minimum(d, 99)
    return out


DEPTHS = (2, 4, 8, 16, 32, 64)


class _ResGCN(torch.nn.Module):
    """h <- h + relu(LayerNorm(A_hat h W)); dropout on the input and the output only (deep nets otherwise drown in
    it).  ``residual=False``: h <- relu(A_hat h W)."""

    def __init__(self, din, hidden, dout, depth, residual):
        super().__init__()
        self.inp = torch.nn.Linear(din, hidden)
        self.layers = torch.nn.ModuleList([torch.nn.Linear(hidden, hidden) for _ in range(depth)])
        self.norms = torch.nn.ModuleList([torch.nn.LayerNorm(hidden) for _ in range(depth)])
        self.out = torch.nn.Linear(hidden, dout)
        self.residual = residual

    def hidden(self, X, Ah):
        F = torch.nn.functional
        h = F.relu(self.inp(F.dropout(X, 0.5, self.training)))
        for L, N in zip(self.layers, self.norms):
            h = h + F.relu(N(Ah @ L(h))) if self.residual else F.relu(Ah @ L(h))
        return h

    def forward(self, X, Ah):
        return self.out(torch.nn.functional.dropout(self.hidden(X, Ah), 0.5, self.training))


def compute_oversmooth():
    _threads()
    rng = np.random.default_rng(0)
    A, X, y = gr.sbm(rng)
    Ahn = gr.norm_adj(A)
    # repeated averaging, no learning: X <- A_hat X
    w = np.sort(np.abs(np.linalg.eigvalsh(Ahn)))[::-1]
    H = X.astype(np.float64)
    energies, snaps = [], {}
    show_k = (0, 1, 4, 16, 64)
    for k in range(0, 65):
        if k:
            H = Ahn @ H
        energies.append(gr.dirichlet(H, A))
        if k in show_k:
            Z = H - H.mean(0)
            U, S, Vt = np.linalg.svd(Z, full_matrices=False)
            snaps[k] = (Z @ Vt[:2].T)
    lam2 = float(w[w < 1 - 1e-8].max())  # the slowest-dying direction (eigenvalue 1 repeats once per component)
    out = dict(energy=np.array(energies), lam2=lam2, lam1=float(w[0]), show_k=list(show_k), y=y,
               n_components=int(gr.components(A).max() + 1),
               pca={str(k): v for k, v in snaps.items()})
    tr = gr.split_masks(y, rng)
    Ah = torch.from_numpy(Ahn)
    part = CACHE.partial("oversmooth", dict(depths=DEPTHS, seeds=SEEDS, v=1))
    for depth in DEPTHS:
        for res in (False, True):
            for s in SEEDS:
                key = f"{'res' if res else 'plain'}_{depth}_s{s}"
                if key in part:
                    continue
                rng_s = np.random.default_rng(100 + s)
                A_s, X_s, y_s = gr.sbm(rng_s)
                tr_s = gr.split_masks(y_s, rng_s)
                Ah_s = torch.from_numpy(gr.norm_adj(A_s))
                torch.manual_seed(s)
                m = _ResGCN(8, 16, 3, depth, res)
                acc, _, _ = _fit_node(m, X_s, Ah_s, y_s, tr_s, seed=s)
                with torch.no_grad():
                    h = m.hidden(torch.from_numpy(X_s), Ah_s).numpy().astype(np.float64)
                e = gr.dirichlet(h / max(np.sqrt((h ** 2).sum(1).mean()), 1e-12), A_s)
                part[key] = dict(acc=acc, energy=e)
                log(f"oversmooth {key}: {acc:.3f}, energy {e:.3g}")
    out["depths"] = list(DEPTHS)
    for k in part.done:
        out[k] = part[k]
    return out


# ===========================================================================
# Proteins
# ===========================================================================
FOLD_RESTARTS = 12
FOLD_SNAPS = (0, 20, 60, 150, 300, 600, 1000, 1500, 2200, 3000)


def compute_fold():
    _threads()
    X, pattern = pr.bundle(0, tries=6000)
    D = pr.dist(X)
    Y, w = pr.mds(D)
    out = dict(X=X, pattern=pattern, D=D, eig=w[:8], mds_rmsd=pr.kabsch(Y, X)[0],
               mds_rmsd_mirror=pr.kabsch(Y, X * np.array([1, 1, -1]))[0], rg=pr.rg(X))
    rng = np.random.default_rng(1)
    cut, noise = 15.0, 1.0
    W = (D < cut).astype(float)
    np.fill_diagonal(W, 0)
    Dn = D + rng.normal(0, noise, D.shape)
    Dn = (Dn + Dn.T) / 2
    np.fill_diagonal(Dn, 0)
    mirror = X * np.array([1, 1, -1])
    runs = []
    for s in range(FOLD_RESTARTS):
        Xf, frames, curve = pr.fold_by_descent(Dn, W, s, steps=3000, lr=0.3, snaps=FOLD_SNAPS if s < 2 else ())
        r_true = pr.kabsch(Xf, X)[0]
        r_mirror = pr.kabsch(Xf, mirror)[0]
        rec = dict(rmsd=r_true, rmsd_mirror=r_mirror, drmsd=pr.drmsd(Xf, X), fape=pr.fape(Xf, X), curve=curve)
        if frames:
            rec["frames"] = [pr.kabsch(f, X if r_true < r_mirror else mirror)[1] for f in frames]
            rec["final"] = pr.kabsch(Xf, X if r_true < r_mirror else mirror)[1]
        runs.append(rec)
        log(f"fold restart {s}: RMSD {r_true:.2f}, to the mirror {r_mirror:.2f}, FAPE {rec['fape']:.3f}")
    out.update(runs=runs, cut=cut, noise=noise, frac_seen=float(W[np.triu_indices(len(W), 1)].mean()),
               snaps=list(FOLD_SNAPS))
    # what each measure says about the mirror image and about small errors
    noisy = X + np.random.default_rng(2).normal(0, 1.0, X.shape)
    out.update(fape_mirror=pr.fape(mirror, X), drmsd_mirror=pr.drmsd(mirror, X),
               rmsd_mirror=pr.kabsch(mirror, X)[0], rmsd_mirror_reflect=pr.kabsch(mirror, X, True)[0],
               fape_noisy=pr.fape(noisy, X), drmsd_noisy=pr.drmsd(noisy, X), rmsd_noisy=pr.kabsch(noisy, X)[0])
    return out


PAIR_KINDS = ("pairwise", "triangle", "recycle")
PAIR_SNAPS = (0, 100, 300, 700, 1500, 2500)


def compute_pair():
    _threads()
    val = pr.pair_batch(np.random.default_rng(99), 200)
    part = CACHE.partial("pair", dict(kinds=PAIR_KINDS, seeds=SEEDS, v=2, n=pr.PAIR_N, snaps=PAIR_SNAPS))
    ex = torch.from_numpy(val[0][3:4])

    def snap(m_):
        with torch.no_grad():
            return m_(ex)[0].numpy().tolist()

    for kind in PAIR_KINDS:
        for s in SEEDS:
            key = f"{kind}_s{s}"
            if key in part:
                continue
            replay = s == 0 and kind != "recycle"
            m, r = pr.train_pair(kind, s, val=val, snaps=PAIR_SNAPS if replay else (), snap_fn=snap if replay else None)
            rec = dict(curve=r["curve"], secs=r["secs"], params=r["params"], frames=r["frames"])
            if kind == "recycle":
                rec["by_cycle"] = [pr.pair_error(m, val, c) for c in range(1, 7)]
                rec.update(rec["by_cycle"][3])
            else:
                rec.update(pr.pair_error(m, val))
            if s == 0:
                save_model(m, f"pair_{kind}")
            part[key] = rec
            log(f"pair {key}: hidden RMSE {rec['hidden']:.2f}, seen {rec['seen']:.2f}, violations {rec['viol']:.4f}")
    out = dict(kinds=list(PAIR_KINDS), n=pr.PAIR_N, snaps=list(PAIR_SNAPS))
    for k in part.done:
        out[k] = part[k]
    inp, D, M = val
    k = 3
    out["ex_true"], out["ex_seen"], out["ex_mask"] = D[k], inp[k, :, :, 0] * 10.0, M[k]
    with torch.no_grad():
        for kind in ("pairwise", "triangle"):
            m = load_model(pr.PairModel(triangle=kind != "pairwise", blocks=3 if kind != "pairwise" else 4),
                           f"pair_{kind}", "pair")
            out[f"ex_{kind}"] = m(torch.from_numpy(inp[k:k + 1]))[0].numpy()
        m = load_model(pr.PairModel(triangle=True, recycle=True), "pair_recycle", "pair")
        out["ex_recycle"] = np.array([m(torch.from_numpy(inp[k:k + 1]), cycles=c)[0].numpy() for c in range(1, 5)])
    # a baseline that knows only the separation along the chain: the average distance at each |i - j|
    rngb = np.random.default_rng(5)
    _, Db, _ = pr.pair_batch(rngb, 400)
    sep = np.abs(np.arange(pr.PAIR_N)[None] - np.arange(pr.PAIR_N)[:, None])
    mean_by_sep = np.array([Db[:, sep == s_].mean() for s_ in range(pr.PAIR_N)])
    P0 = mean_by_sep[sep][None].repeat(len(D), 0)
    hid = (~M) & (sep[None] >= 3)
    out["sep_baseline"] = float(np.sqrt(((P0 - D) ** 2)[hid].mean()))
    return out


DIFF_KINDS = ("egnn", "mlp")
DIFF_STEPS = 8000
DIFF_SNAPS = (0, 500, 1500, 3000, 5000, 8000)


def compute_diffusion():
    _threads()
    data = pr.chain_dataset(4000, 0)
    ref = pr.chain_stats(data[:1000])
    part = CACHE.partial("diffusion", dict(kinds=DIFF_KINDS, seeds=(0, 1), steps=DIFF_STEPS, v=1))
    for kind in DIFF_KINDS:
        for s in (0, 1):
            key = f"{kind}_s{s}"
            if key in part:
                continue
            snap = (lambda m_: pr.sample(m_, 8, 123)[0].tolist()) if s == 0 else None
            m, r = pr.train_diffusion(kind, data, s, DIFF_STEPS, snaps=DIFF_SNAPS if s == 0 else (), snap_fn=snap)
            S, path = pr.sample(m, 500, 7 + s, keep=(200, 150, 100, 60, 30, 10, 0) if s == 0 else ())
            st = pr.chain_stats(S)
            nn_s = pr.nearest_rmsd(S[:200], data)
            rec = dict(nn_median=float(np.median(nn_s)), curve=r["curve"], frames=r["frames"], secs=r["secs"], params=r["params"],
                       bond_mad=st["bond_mad"], clash=st["clash"], rg_mean=float(st["rg"].mean()),
                       rg_hist=np.histogram(st["rg"], bins=24, range=(0.5, 2.9))[0].tolist(), samples=S[:24].tolist())
            if s == 0:
                rec["path"] = {str(t): v[:4].tolist() for t, v in path.items()}
            part[key] = rec
            log(f"diffusion {key}: bond MAD {st['bond_mad']:.3f}, clashes {st['clash']:.3f} ({r['secs']:.0f}s)")
    held = pr.chain_dataset(200, 1)
    out = dict(kinds=list(DIFF_KINDS), data=data[:24], ref_bond_mad=ref["bond_mad"], ref_clash=ref["clash"],
               nn_heldout_median=float(np.median(pr.nearest_rmsd(held, data))),
               ref_rg_mean=float(ref["rg"].mean()),
               ref_rg_hist=np.histogram(ref["rg"], bins=24, range=(0.5, 2.9))[0], T=pr.T_DIFF, steps=DIFF_STEPS,
               snaps=list(DIFF_SNAPS))
    for k in part.done:
        out[k] = part[k]
    return out


# ===========================================================================
# Fields
# ===========================================================================
FNO_RES = 64
TEST_RES = (32, 64, 128, 256, 512, 1024)
FNO_SNAPS = (0, 100, 300, 1000, 3000, 7500)


def compute_fno():
    _threads()
    rng = np.random.default_rng(21)
    U0 = fd.grf(rng, 1200, fd.FINE)
    t0 = time.time()
    UT = np.concatenate([fd.burgers(U0[a:a + 100], dt=5e-4) for a in range(0, 1200, 100)])
    log(f"fno: Burgers solved for 1,200 starts ({time.time() - t0:.0f}s)")
    tr0, trT = fd.subsample(U0[:1000], FNO_RES), fd.subsample(UT[:1000], FNO_RES)
    te0, teT = U0[1000:], UT[1000:]
    val = (torch.from_numpy(fd.subsample(te0[:100], FNO_RES)).float(),
           torch.from_numpy(fd.subsample(teT[:100], FNO_RES)).float())
    show = torch.from_numpy(fd.subsample(te0[:3], FNO_RES)).float()
    part = CACHE.partial("fno", dict(res=FNO_RES, test=TEST_RES, seeds=SEEDS, v=2))
    for kind in ("fno", "cnn"):
        for s in SEEDS:
            key = f"{kind}_s{s}"
            if key in part:
                continue
            snap = (lambda m_: m_(show).detach().numpy().tolist()) if s == 0 else None
            m, r = fd.train_operator(kind, tr0, trT, s, epochs=150, snaps=FNO_SNAPS if s == 0 else (), snap_fn=snap,
                                     val=val)
            errs = {}
            with torch.no_grad():
                for res in TEST_RES:
                    p = m(torch.from_numpy(fd.subsample(te0, res)).float()).numpy()
                    errs[str(res)] = float(fd.rel_l2(p, fd.subsample(teT, res)).mean())
                if s == 0:
                    pred_hi = {str(res): m(torch.from_numpy(fd.subsample(te0[:3], res)).float()).numpy().tolist()
                               for res in (64, 256, 1024)}
            rec = dict(err=errs, curve=r["curve"], frames=r["frames"], secs=r["secs"], params=r["params"],
                       steps=r["steps"])
            if s == 0:
                rec["pred"] = pred_hi
                save_model(m, f"op_{kind}")
            part[key] = rec
            log(f"fno {key}: {errs} ({r['secs']:.0f}s)")
    out = dict(res=FNO_RES, test_res=list(TEST_RES), nu=fd.NU, n_train=1000, n_test=200, snaps=list(FNO_SNAPS),
               show_u0=te0[:3], show_uT=teT[:3], modes=16)
    for k in part.done:
        out[k] = part[k]
    return out


W_STEPS = 3000
W_SNAPS = (0, 250, 1000, 2000, 3000)


def compute_weather():
    _threads()
    t0 = time.time()
    runs = fd.weather_runs(32, 120, seed=31)
    test = fd.weather_runs(8, 50, seed=32)
    log(f"weather: trajectories ({time.time() - t0:.0f}s)")
    sw, sd = float(runs.std()), float(np.diff(runs, axis=1).std())
    lead = 40
    truth = test[:, 2:2 + lead]
    clim = runs.mean((0, 1))
    out = dict(scale=[sw, sd], lead=lead, dt=fd.DT_SOLVE * fd.SUB, grid=fd.GRID,
               persistence=np.sqrt(((test[:, 1:2] - truth) ** 2).mean((0, 2, 3))),
               climatology=np.sqrt(((clim[None, None] - truth) ** 2).mean((0, 2, 3))),
               field_std=float(test.std()), show_truth=test[0, 2:2 + lead:4])
    part = CACHE.partial("weather", dict(steps=W_STEPS, v=1))
    variants = {"multimesh": (16, 8, 4), "finest": (16,)}
    for name, levels in variants.items():
        key = name
        if key in part:
            continue
        mesh = fd.build_mesh(levels)
        show = (torch.from_numpy(test[:1, 0]) / sw, torch.from_numpy(test[:1, 1]) / sw)

        def snap(m_):
            return fd.rollout(m_, test[:1, 0], test[:1, 1], 20, (sw, sd))[0, ::5].tolist()

        m, r = fd.train_weather(mesh, runs, 0, W_STEPS, rollout_from=int(W_STEPS * 0.8), scale=(sw, sd),
                                snaps=W_SNAPS if name == "multimesh" else (), snap_fn=snap)
        R = fd.rollout(m, test[:, 0], test[:, 1], lead, (sw, sd))
        rmse = np.sqrt(((R - truth) ** 2).mean((0, 2, 3)))
        a = (R - clim) .reshape(len(R), lead, -1)
        b = (truth - clim).reshape(len(R), lead, -1)
        acc = ((a * b).sum(-1) / np.sqrt((a ** 2).sum(-1) * (b ** 2).sum(-1))).mean(0)
        rec = dict(rmse=rmse.tolist(), acc=acc.tolist(), curve=r["curve"], frames=r["frames"], secs=r["secs"],
                   params=r["params"], mesh_nodes=len(mesh["pos"]), mesh_edges=len(mesh["edges"]))
        if name == "multimesh":
            rec["show"] = R[0, ::4].tolist()
            save_model(m, "weather_multimesh")
        part[key] = rec
        log(f"weather {name}: RMSE at steps 1, 10, 40: {rmse[0]:.3f}, {rmse[9]:.3f}, {rmse[-1]:.3f} ({r['secs']:.0f}s)")
    for k in part.done:
        out[k] = part[k]
    a_ = (truth[:, :1] - clim).reshape(len(truth), 1, -1)
    b_ = (truth - clim).reshape(len(truth), lead, -1)
    pa = (test[:, 1:2] - clim).reshape(len(truth), 1, -1)
    out["persistence_acc"] = ((pa * b_).sum(-1) / np.sqrt((pa ** 2).sum(-1) * (b_ ** 2).sum(-1))).mean(0)
    mesh = fd.build_mesh((16, 8, 4))
    out.update(mesh_pos=mesh["pos"], mesh_edges=mesh["edges"])
    return out


# ===========================================================================
# Discovery
# ===========================================================================
def compute_materials():
    _threads()
    rows, X, E = dc.chemistry(0)
    stable = dc.true_stable(rows, E)
    part = CACHE.partial("materials", dict(seeds=SEEDS, v=2))
    for policy in ("model", "random"):
        for s in SEEDS:
            key = f"{policy}_s{s}"
            if key in part:
                continue
            hist, _ = dc.flywheel(rows, X, E, s, rounds=8, per_round=60, start=0.03, policy=policy)
            part[key] = hist
            log(f"materials {key}: hit rates {[round(h['hit_rate'], 2) for h in hist]}")
    out = dict(n_candidates=len(rows), n_stable=int(stable.sum()), n_elements=dc.N_ELEM, n_proto=dc.N_PROTO,
               comps=list(dc.COMPS))
    for k in part.done:
        out[k] = part[k]
    # one binary system to draw: its candidates, its hull
    sys_ = dc.systems_of(rows)
    key = max(sys_, key=lambda k_: stable[sys_[k_]].sum())
    idx = sys_[key]
    pts = [(0.0, 0.0), (1.0, 0.0)] + [(rows[i, 2], E[i]) for i in idx]
    h = dc.lower_hull(pts)
    out.update(sys_x=rows[idx, 2], sys_E=E[idx], sys_proto=rows[idx, 3], sys_stable=stable[idx], sys_hull=h,
               sys_pair=list(key))
    return out


def compute_matmul():
    rng = np.random.default_rng(8)
    out = {}
    T2 = dc.matmul_tensor(2)
    for R in (6, 7, 8):
        res = []
        best = None
        for k in range(30):
            r, f = dc.cp_als(T2, R, rng, iters=3000)
            res.append(r)
            if best is None or r < best[0]:
                best = (r, f)
        out[f"n2_r{R}"] = dict(res=res, success=int(sum(r_ < 1e-6 for r_ in res)), best=min(res))
        if R == 7:
            U, V, W = best[1]
            out["n2_r7_verify"] = dc.verify_algorithm(U, V, W, 2, rng)
            out["n2_r7_U"], out["n2_r7_V"], out["n2_r7_W"] = U, V, W
        log(f"matmul 2x2 rank {R}: {out[f'n2_r{R}']['success']} of 30 reach zero (best {min(res):.2e})")
    T3 = dc.matmul_tensor(3)
    for R in (23, 26):
        res = []
        t0 = time.time()
        for k in range(10):
            r, _ = dc.cp_als(T3, R, rng, iters=3000)
            res.append(r)
        out[f"n3_r{R}"] = dict(res=res, success=int(sum(r_ < 1e-6 for r_ in res)), best=min(res))
        log(f"matmul 3x3 rank {R}: {out[f'n3_r{R}']['success']} of 10 reach zero (best {min(res):.2e}, "
            f"{time.time() - t0:.0f}s)")
    return out


def compute_binpack():
    train = [dc.weibull_instance(np.random.default_rng(100 + i), 300) for i in range(8)]
    test = [dc.weibull_instance(np.random.default_rng(500 + i), 1000) for i in range(10)]
    out = dict(ff_test=dc.excess(test, dc.first_fit), bf_test=dc.excess(test, dc.best_fit),
               ff_train=dc.excess(train, dc.first_fit), bf_train=dc.excess(train, dc.best_fit))
    part = CACHE.partial("binpack", dict(v=2, seeds=(0, 1)))
    for s in (0, 1):
        key = f"s{s}"
        if key in part:
            continue
        hist, best = dc.evolve(train, s, pop=60, gens=40, log=log)
        part[key] = dict(history=hist, best=dc.to_text(best), tree=repr(best),
                         test=dc.excess(test, dc.compile_tree(best)))
    for k in part.done:
        out[k] = part[k]
    sizes = np.concatenate(test)
    out["size_hist"] = np.histogram(sizes, bins=20, range=(0, 100))[0]
    return out


def _item(fn):
    """Top-level numpy arrays go to the item's .npz; anything nested (dicts, lists of arrays) becomes plain JSON."""
    def run():
        out = fn()
        return {k: (v if isinstance(v, np.ndarray) else tolist(v)) for k, v in out.items()}
    run.__name__ = fn.__name__
    return run


ITEMS = {
    "nbody_data": compute_nbody_data,
    "harmonics": compute_harmonics,
    "wl": compute_wl,
    "deepsets": compute_deepsets,
    "setcurves": compute_setcurves,
    "gin": compute_gin,
    "sbm": compute_sbm,
    "oversmooth": compute_oversmooth,
    "fold": compute_fold,
    "matmul": compute_matmul,
    "binpack": compute_binpack,
    "nbody": compute_nbody,
    "energy": compute_energy,
    "equivariance": compute_equivariance,
    "pair": compute_pair,
    "fno": compute_fno,
    "weather": compute_weather,
    "materials": compute_materials,
    "diffusion": compute_diffusion,
}
ITEMS = {k: _item(v) for k, v in ITEMS.items()}

if __name__ == "__main__":
    _threads()
    CACHE.main(ITEMS, __doc__)
