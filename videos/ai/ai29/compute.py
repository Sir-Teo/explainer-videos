"""Precompute everything numerical in Part 29 of the AI series ("Agents and Worlds").

    python -m videos.ai.ai29.compute              # everything missing
    python -m videos.ai.ai29.compute --force world

Results are cached in ``.cache/ai29/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.

Items:
    belief     a robot in a corridor of 40 cells with 4 doors, unsure where it is: it moves (sometimes slipping) and
               senses doors (sometimes wrongly); its belief, updated by Bayes' rule step by step (Part 7's forward
               algorithm), and how sure it ends up
    horizon    long tasks: the chance of finishing a task of n steps when each step succeeds with probability p, and
               the task length an agent finishes half the time, as p rises
    world      a small world model: frames of a ball bouncing in a box (16 x 16 pixels); an encoder to 8 numbers, a
               network that predicts the next 8 numbers, a decoder; its imagined future against the real one, and how
               its error grows with the horizon
"""

from __future__ import annotations

import math

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("ai29")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


# ---------------------------------------------------------------------------
def compute_belief():
    n = 40
    doors = np.zeros(n, bool)
    doors[[3, 8, 19, 33]] = True  # unevenly spaced, so the pattern of doors tells places apart
    p_hit, p_false = 0.9, 0.05  # sees a door when at one / when not
    p_move = 0.8  # a step of +1 succeeds; otherwise it stays
    g = rng(2005)  # Thrun, Burgard & Fox, Probabilistic Robotics
    pos = 2
    belief = np.full(n, 1 / n)
    beliefs, poss, obs = [belief.copy()], [pos], []
    for t in range(40):
        # move right by one (circular corridor), with a chance of slipping
        pos = (pos + 1) % n if g.random() < p_move else pos
        belief = p_move * np.roll(belief, 1) + (1 - p_move) * belief  # predict
        z = (g.random() < p_hit) if doors[pos] else (g.random() < p_false)
        like = np.where(doors, p_hit if z else 1 - p_hit, p_false if z else 1 - p_false)
        belief = belief * like
        belief /= belief.sum()  # update: Bayes' rule
        beliefs.append(belief.copy())
        poss.append(pos)
        obs.append(bool(z))
    beliefs = np.array(beliefs)
    ent = -(beliefs * np.log2(np.maximum(beliefs, 1e-300))).sum(1)
    out = dict(n=n, doors=np.where(doors)[0], beliefs=beliefs, pos=np.array(poss), obs=np.array(obs), entropy=ent,
               p_hit=p_hit, p_false=p_false, p_move=p_move)
    assert beliefs[-1].argmax() in (poss[-1] - 1, poss[-1], poss[-1] + 1) and ent[-1] < 0.5 * ent[0]
    return out


# ---------------------------------------------------------------------------
def compute_horizon():
    ps = [0.9, 0.99, 0.999]
    ns = np.unique(np.round(np.logspace(0, 4, 200)).astype(int))
    out = dict(ps=ps, ns=ns)
    for p in ps:
        out[f"succ{p:g}"] = p ** ns.astype(float)
    pr = np.linspace(0.5, 0.9999, 400)
    out["p_range"] = pr
    out["half_len"] = np.log(0.5) / np.log(pr)  # p^n = 1/2
    assert abs(out["half_len"][-1] - math.log(0.5) / math.log(0.9999)) < 1e-6
    # sixty simulated runs of a 30-step task at 97% a step: the step at which each first goes wrong
    g = rng(30)
    fails = g.geometric(1 - 0.97, size=60)
    out["runs_fail"] = fails
    out["runs_ok"] = float((fails > 30).mean())
    assert abs(out["runs_ok"] - 0.97 ** 30) < 0.15
    return out


# ---------------------------------------------------------------------------
def frames(g, n_seq, T, size=16):
    """Balls bouncing in a box: positions and velocities, drawn as soft dots."""
    seqs = np.zeros((n_seq, T, size, size))
    yy, xx = np.mgrid[0:size, 0:size]
    for s in range(n_seq):
        p = g.uniform(3, size - 3, 2)
        v = g.uniform(-1.2, 1.2, 2)
        for t in range(T):
            seqs[s, t] = np.exp(-((xx - p[0]) ** 2 + (yy - p[1]) ** 2) / (2 * 1.2 ** 2))
            p = p + v
            for d in range(2):
                if p[d] < 1.5 or p[d] > size - 2.5:
                    v[d] = -v[d]
                    p[d] = np.clip(p[d], 1.5, size - 2.5)
    return seqs


def compute_world():
    import torch
    import torch.nn as nn

    torch.set_num_threads(2)
    torch.manual_seed(2018)  # Ha & Schmidhuber, World Models
    g = rng(2018)
    S = 16
    data = torch.tensor(frames(g, 600, 24), dtype=torch.float32)
    Z = 8
    enc = nn.Sequential(nn.Linear(S * S, 256), nn.ReLU(), nn.Linear(256, Z))
    dec = nn.Sequential(nn.Linear(Z, 256), nn.ReLU(), nn.Linear(256, S * S))
    dyn = nn.Sequential(nn.Linear(2 * Z, 128), nn.ReLU(), nn.Linear(128, 128), nn.ReLU(), nn.Linear(128, Z))
    params = [*enc.parameters(), *dec.parameters(), *dyn.parameters()]
    opt = torch.optim.Adam(params, lr=1e-3)
    flat = data.reshape(600, 24, -1)
    probe = torch.tensor(frames(rng(7), 50, 40), dtype=torch.float32).reshape(50, 40, -1)[:1]
    checks, snaps, losses = [0, 100, 300, 800, 2000, 5000], [], []

    def dream(n=12):  # how it learns: from the probe clip's first two frames, imagine the next n
        with torch.no_grad():
            z = enc(probe[:, :2])
            z1, z2, out_ = z[:, 0], z[:, 1], []
            for _ in range(n):
                z3 = z2 + dyn(torch.cat([z1, z2], -1))
                out_.append(torch.sigmoid(dec(z3))[0].numpy().reshape(S, S))
                z1, z2 = z2, z3
        return np.array(out_)

    for step in range(5000):
        if step in checks:
            snaps.append(dream())
        i = torch.randint(0, 600, (64,))
        x = flat[i]  # (64, 24, 256)
        z = enc(x)
        rec = torch.sigmoid(dec(z))
        # dynamics: from two frames' codes, predict the next code (two frames give the velocity)
        zin = torch.cat([z[:, :-2], z[:, 1:-1]], -1)
        zp = z[:, 1:-1] + dyn(zin)
        pred = torch.sigmoid(dec(zp))
        loss = ((rec - x) ** 2).mean() + ((pred - x[:, 2:]) ** 2).mean() + 0.1 * ((zp - z[:, 2:].detach()) ** 2).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
        if step % 25 == 0:
            losses.append((step, float(loss)))
    snaps.append(dream())
    test = torch.tensor(frames(rng(7), 50, 40), dtype=torch.float32).reshape(50, 40, -1)
    with torch.no_grad():
        z = enc(test[:, :2])
        z1, z2 = z[:, 0], z[:, 1]
        imag = []
        for t in range(38):  # imagine: feed its own predictions back in
            z3 = z2 + dyn(torch.cat([z1, z2], -1))
            imag.append(torch.sigmoid(dec(z3)))
            z1, z2 = z2, z3
        imag = torch.stack(imag, 1)
        real = test[:, 2:]
        err = ((imag - real) ** 2).mean((0, 2)).numpy()

        def centre(fr):
            w = fr.reshape(-1, S, S).numpy()
            yy, xx = np.mgrid[0:S, 0:S]
            m = w.sum((1, 2)) + 1e-9
            return np.stack([(w * xx).sum((1, 2)) / m, (w * yy).sum((1, 2)) / m], 1)

        pos_err = np.array([np.linalg.norm(centre(imag[:, t]) - centre(real[:, t]), axis=1).mean() for t in range(38)])
    out = dict(S=S, Z=Z, real=real[0, :24].numpy().reshape(-1, S, S), imag=imag[0, :24].numpy().reshape(-1, S, S),
               err=err, pos_err=pos_err, first=test[0, :2].numpy().reshape(-1, S, S),
               checks=checks, dreams=np.array(snaps), losses=np.array(losses), probe_real=test[0, 2:14].numpy().reshape(-1, S, S))
    print(f"    position error after 1, 5, 20 imagined steps: {pos_err[0]:.2f}, {pos_err[4]:.2f}, {pos_err[19]:.2f} pixels",
          flush=True)
    assert pos_err[0] < 1.5 and pos_err[19] > pos_err[0]
    return out


ITEMS = {
    "belief": compute_belief,
    "horizon": compute_horizon,
    "world": compute_world,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
