"""A Dreamer-lite: Hafner et al.'s recipe (PlaNet 2019, Dreamer 2020, DreamerV2 2021, DreamerV3 2023), shrunk to a
12 x 12 game of catch so that it trains on a laptop's CPU in minutes.

* the world model is a recurrent state-space model (RSSM): a deterministic memory h (a GRU) and a stochastic state z
  (8 categorical variables of 8 classes, sampled with straight-through gradients and 1% uniform mixing, as in V3);
  from (h, z) it decodes the picture (a Bernoulli per pixel) and the reward (regressed in symlog space);
* the KL term is balanced (V3): 0.5 KL(sg(q) || p) trains the prior towards the posterior, 0.1 KL(q || sg(p))
  keeps the posterior predictable, each clipped below at one nat ("free bits");
* the actor and the critic learn only in imagination: from states of real sequences, the world model dreams 15
  steps ahead under the actor; the critic regresses lambda-returns; the actor follows REINFORCE with the critic as
  baseline, advantages divided by a running range of the returns (V3), plus an entropy bonus.

``train(seed, ...)`` runs one seed and returns its learning curve, snapshots (imagined against real futures, the
policy's behaviour in the real game, its dreams) and the KL curves.  It is deterministic for a seed on one machine.
"""

from __future__ import annotations

import numpy as np

from .envs import Catch

S = Catch.S
NPIX = S * S
NA = 3
ZV, ZC = 8, 8  # stochastic state: ZV variables of ZC classes
ZD = ZV * ZC
HD = 128


def symlog(x):
    import torch

    return torch.sign(x) * torch.log1p(torch.abs(x))


def symexp(x):
    import torch

    return torch.sign(x) * (torch.exp(torch.abs(x)) - 1)


def build(torch):
    nn = torch.nn

    def mlp(i, o, h=128, n=1):
        layers, d = [], i
        for _ in range(n):
            layers += [nn.Linear(d, h), nn.LayerNorm(h), nn.SiLU()]
            d = h
        layers.append(nn.Linear(d, o))
        return nn.Sequential(*layers)

    class WorldModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.enc = mlp(NPIX, 128, 256, 1)
            self.inp = nn.Sequential(nn.Linear(ZD + NA, HD), nn.LayerNorm(HD), nn.SiLU())
            self.gru = nn.GRUCell(HD, HD)
            self.prior = mlp(HD, ZD, 128, 1)
            self.post = mlp(HD + 128, ZD, 128, 1)
            self.dec = mlp(HD + ZD, NPIX, 256, 1)
            self.rew = mlp(HD + ZD, 1, 128, 1)

        @staticmethod
        def dist(logits):
            p = torch.softmax(logits.view(*logits.shape[:-1], ZV, ZC), -1)
            p = 0.99 * p + 0.01 / ZC  # unimix
            return p

        @staticmethod
        def sample(p):
            u = torch.rand_like(p).clamp_(1e-9, 1 - 1e-9)
            idx = (torch.log(p) - torch.log(-torch.log(u))).argmax(-1)  # Gumbel-max: a sample of each variable
            hard = torch.nn.functional.one_hot(idx, ZC).float()
            return (hard + p - p.detach()).flatten(-2)  # straight-through

        def step(self, h, z, a):
            return self.gru(self.inp(torch.cat([z, a], -1)), h)

        def observe(self, obs, act):
            """obs (B, T, NPIX), act (B, T, NA) the action taken *before* each frame (zeros at t = 0)."""
            B, T = obs.shape[:2]
            e = self.enc(obs)
            h = torch.zeros(B, HD)
            z = torch.zeros(B, ZD)
            hs, zs, pri, pos = [], [], [], []
            for t in range(T):
                h = self.step(h, z, act[:, t])
                pp = self.dist(self.prior(h))
                qq = self.dist(self.post(torch.cat([h, e[:, t]], -1)))
                z = self.sample(qq)
                hs.append(h)
                zs.append(z)
                pri.append(pp)
                pos.append(qq)
            return torch.stack(hs, 1), torch.stack(zs, 1), torch.stack(pri, 1), torch.stack(pos, 1)

        def imagine_open_loop(self, h, z, acts):
            """From (h, z), follow the given actions (B, H, NA) with the prior only: the model's own dream."""
            frames = []
            for t in range(acts.shape[1]):
                h = self.step(h, z, acts[:, t])
                z = self.sample(self.dist(self.prior(h)))
                frames.append(torch.sigmoid(self.dec(torch.cat([h, z], -1))))
            return torch.stack(frames, 1)

    def kl(p, q):  # KL(p || q) summed over the variables, (..., ZV, ZC)
        return (p * (torch.log(p) - torch.log(q))).sum(-1).sum(-1)

    return WorldModel, mlp, kl


def onehot(a, n=NA):
    out = np.zeros((len(a), n), np.float32)
    out[np.arange(len(a)), a] = 1
    return out


class Replay:
    def __init__(self):
        self.obs, self.act, self.rew = [], [], []

    def add(self, obs, act, rew):  # one episode: obs (T, NPIX); act (T,) taken before each frame; rew (T,)
        self.obs.append(obs)
        self.act.append(act)
        self.rew.append(rew)

    def sample(self, g, B, L):
        o, a, r = [], [], []
        for _ in range(B):
            k = int(g.integers(len(self.obs)))
            T = len(self.obs[k])
            s = int(g.integers(0, T - L + 1))
            o.append(self.obs[k][s:s + L])
            a.append(self.act[k][s:s + L])
            r.append(self.rew[k][s:s + L])
        return np.array(o), np.array(a), np.array(r)

    @property
    def steps(self):
        return sum(len(x) for x in self.obs)


def run_episode(env, policy, g):
    """One real episode.  ``policy(obs_history_state) -> action``; returns frames, actions (taken before each frame),
    rewards, and the game's state at each frame (ball x, y, paddle x)."""
    o = env.reset()
    obs, acts, rews, states = [o.reshape(-1)], [1], [0.0], [env.state()]
    done = False
    state = None
    while not done:
        a, state = policy(o, acts[-1], state)
        o, r, done = env.step(a)
        obs.append(o.reshape(-1))
        acts.append(a)
        rews.append(r)
        states.append(env.state())
    return np.array(obs, np.float32), np.array(acts), np.array(rews, np.float32), np.array(states)


def train(seed, iters=60, steps_per_iter=40, B=16, L=32, H=15, gamma=0.97, lam=0.95, kl_dyn=0.5, kl_rep=0.1,
          free=1.0, ent=3e-3, starts=256, train_policy=True, init_eps=8, eval_every=5, eval_eps=6, snap_iters=(0, 10, 30, 60),
          log=None):
    import torch

    torch.manual_seed(seed)
    g = np.random.default_rng(seed)
    WorldModel, mlp, kl = build(torch)
    wm = WorldModel()
    feat = HD + ZD
    actor = mlp(feat, NA, 128, 1)
    critic = mlp(feat, 1, 128, 1)
    target = mlp(feat, 1, 128, 1)
    target.load_state_dict(critic.state_dict())
    o_wm = torch.optim.Adam(wm.parameters(), lr=6e-4, eps=1e-6)
    o_ac = torch.optim.Adam(actor.parameters(), lr=3e-4, eps=1e-6)
    o_cr = torch.optim.Adam(critic.parameters(), lr=3e-4, eps=1e-6)
    env = Catch(np.random.default_rng(seed + 10_000))
    rep = Replay()
    ret_lo, ret_hi = None, None

    def random_policy(o, a_prev, st):
        return int(g.integers(NA)), None

    def agent_policy(greedy):
        def pol(o, a_prev, st):
            with torch.no_grad():
                if st is None:
                    st = (torch.zeros(1, HD), torch.zeros(1, ZD))
                h = wm.step(st[0], st[1], torch.tensor(onehot([a_prev])))
                e = wm.enc(torch.tensor(o.reshape(1, -1)))
                q = wm.dist(wm.post(torch.cat([h, e], -1)))
                z = wm.sample(q)
                logits = actor(torch.cat([h, z], -1))[0]
                if greedy:
                    a = int(logits.argmax())
                else:
                    a = int(torch.multinomial(torch.softmax(logits, -1), 1))
            return a, (h, z)

        return pol

    def catch_rate(eps_n, gen):
        ev = Catch(gen)
        rs, traj = [], None
        for k in range(eps_n):
            obs, acts, rews, states = run_episode(ev, agent_policy(True), g)
            rs += [r for r in rews if r != 0]
            if k == 0:
                traj = states
        return float(np.mean(np.array(rs) > 0)), traj

    for _ in range(init_eps):
        obs, acts, rews, _ = run_episode(env, random_policy, g)
        rep.add(obs, onehot(acts), rews)
    # a fixed probe episode (random actions) for the imagined-against-real snapshots
    pg = np.random.default_rng(777)
    probe = run_episode(Catch(np.random.default_rng(778)), lambda o, a, s: (int(pg.integers(NA)), None), g)
    probe_obs = torch.tensor(probe[0][None])
    probe_act = torch.tensor(onehot(probe[1])[None])
    curve, klc, snaps, losses = [], [], {}, []
    rec_hist = []

    def snapshot(it):
        with torch.no_grad():
            ctx = 6
            hs, zs, _, _ = wm.observe(probe_obs[:, :ctx], probe_act[:, :ctx])
            dream = wm.imagine_open_loop(hs[:, -1], zs[:, -1], probe_act[:, ctx:ctx + 18])[0].numpy()
            real = probe_obs[0, ctx:ctx + 18].numpy()
            # the actor's own dream: imagine 15 steps under the actor from the probe's context
            h, z = hs[:, -1], zs[:, -1]
            own = []
            for t in range(15):
                a = actor(torch.cat([h, z], -1)).argmax(-1)
                h = wm.step(h, z, torch.nn.functional.one_hot(a, NA).float())
                z = wm.sample(wm.dist(wm.prior(h)))
                own.append(torch.sigmoid(wm.dec(torch.cat([h, z], -1)))[0].numpy())
        rate, traj = catch_rate(2, np.random.default_rng(4242))
        snaps[str(it)] = dict(dream=dream.reshape(-1, S, S).round(3), real=real.reshape(-1, S, S),
                              own=np.array(own).reshape(-1, S, S).round(3), traj=traj, rate=rate)

    for it in range(iters + 1):
        if it in snap_iters:
            snapshot(it)
        if it % eval_every == 0 or it == iters:
            rate, _ = catch_rate(eval_eps, np.random.default_rng(5000 + it))
            curve.append((it, rep.steps, rate))
            if log:
                log(f"      seed {seed} iter {it:3d}  env steps {rep.steps:5d}  catch rate {rate:.2f}")
        if it == iters:
            break
        for k in range(steps_per_iter):
            o, a, r = rep.sample(g, B, L)
            o, a, r = torch.tensor(o), torch.tensor(a), torch.tensor(r)
            hs, zs, pri, pos = wm.observe(o, a)
            fe = torch.cat([hs, zs], -1)
            rec = torch.nn.functional.binary_cross_entropy_with_logits(wm.dec(fe), o, reduction="none").sum(-1).mean()
            rl = ((wm.rew(fe)[..., 0] - symlog(r)) ** 2).mean()
            k_dyn = kl(pos.detach(), pri)
            k_rep = kl(pos, pri.detach())
            loss = rec + rl + kl_dyn * torch.clamp(k_dyn, min=free).mean() + kl_rep * torch.clamp(k_rep, min=free).mean()
            o_wm.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(wm.parameters(), 100.0)
            o_wm.step()
            if k == 0:
                klc.append((it, float(k_dyn.mean().detach()), float(rec.detach())))
            losses.append(float(loss))
            if not train_policy:
                continue
            # imagination: from every state of the batch, dream H steps ahead under the actor
            with torch.no_grad():
                pick = torch.randperm(B * L)[:starts]
                h = hs.reshape(-1, HD).detach()[pick]
                z = zs.reshape(-1, ZD).detach()[pick]
                feats, acts_ = [torch.cat([h, z], -1)], []
                for t in range(H):
                    logits = actor(feats[-1])
                    act = torch.multinomial(torch.softmax(logits, -1), 1)[:, 0]
                    acts_.append(act)
                    h = wm.step(h, z, torch.nn.functional.one_hot(act, NA).float())
                    z = wm.sample(wm.dist(wm.prior(h)))
                    feats.append(torch.cat([h, z], -1))
                F = torch.stack(feats, 0)  # (H+1, N, feat)
                rew = symexp(wm.rew(F[1:])[..., 0])  # reward on arriving
                v = target(F)[..., 0]
                R = [v[-1]]
                for t in range(H - 1, -1, -1):
                    R.append(rew[t] + gamma * ((1 - lam) * v[t + 1] + lam * R[-1]))
                R = torch.stack(R[::-1][:-1], 0)  # (H, N) lambda-returns from each imagined state
                lo, hi = torch.quantile(R, 0.05), torch.quantile(R, 0.95)
                ret_lo = lo if ret_lo is None else 0.99 * ret_lo + 0.01 * lo
                ret_hi = hi if ret_hi is None else 0.99 * ret_hi + 0.01 * hi
                scale = torch.clamp(ret_hi - ret_lo, min=1.0)
                adv = (R - v[:-1]) / scale
                A = torch.stack(acts_, 0)
            logits = actor(F[:-1])
            logp = torch.log_softmax(logits, -1)
            lp = logp.gather(-1, A[..., None])[..., 0]
            entropy = -(logp.exp() * logp).sum(-1)
            a_loss = -(lp * adv).mean() - ent * entropy.mean()
            o_ac.zero_grad()
            a_loss.backward()
            torch.nn.utils.clip_grad_norm_(actor.parameters(), 100.0)
            o_ac.step()
            c_loss = ((critic(F[:-1])[..., 0] - R) ** 2).mean()
            o_cr.zero_grad()
            c_loss.backward()
            torch.nn.utils.clip_grad_norm_(critic.parameters(), 100.0)
            o_cr.step()
            with torch.no_grad():
                for p_, t_ in zip(critic.parameters(), target.parameters()):
                    t_.mul_(0.98).add_(0.02 * p_)
        # one more real episode with the current actor (sampling), into the replay
        pol = agent_policy(False) if train_policy else random_policy
        obs, acts, rews, _ = run_episode(env, pol, g)
        rep.add(obs, onehot(acts), rews)
    # how far the model's own dream drifts from reality: open-loop prediction error by steps ahead, on fresh episodes
    with torch.no_grad():
        gen = np.random.default_rng(31337)
        errs = []
        for k in range(12):
            ep = run_episode(Catch(gen), random_policy, g)
            ob, ac = torch.tensor(ep[0][None]), torch.tensor(onehot(ep[1])[None])
            hs, zs, _, _ = wm.observe(ob[:, :6], ac[:, :6])
            d = wm.imagine_open_loop(hs[:, -1], zs[:, -1], ac[:, 6:6 + 30])[0]
            errs.append(((d > 0.5).float() != ob[0, 6:36]).float().sum(-1).numpy())  # wrong pixels per frame
        open_err = np.mean(errs, 0)
    return dict(curve=np.array(curve), kl=np.array(klc), snaps=snaps, open_err=open_err,
                loss=np.array(losses[::10]))
