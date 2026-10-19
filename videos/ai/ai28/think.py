"""Think or answer: Part 28's testbed for length, verifiers, search and test-time budgets.

The question is a list of 2 to 9 digits in ten slots (the unused slots hold PAD, so a PAD always ends the list); the answer is their sum.  The model
writes ``=`` and then either answers at once (``ANS 37``) or thinks first: ``THINK`` and the running total after
each digit, ``THINK 4 11 13 ... ANS 37``.  It may stop thinking at any point and answer.  Supervised training shows
all three (40% at once, 40% the whole chain, 20% a chain cut short), so the starting model thinks about half the
time, whatever the question.  A step of thought is one token here, so "length" is counted in steps.

Items:
    think_sft      the supervised model (weights cached): accuracy by length of list when made to answer at once,
                   made to think, and left to choose; how often it chooses to think
    think_samples  64 sampled solutions per test question from that model, made to think, and 64 made to answer at
                   once: answers, steps, and which steps are right
    think_rl       reinforcement learning on the sum's correctness alone, and with a cost of 0.02 per step of
                   thought; 3 seeds each: accuracy, length, how often it thinks, by length of list, as it trains,
                   and the lengths it chooses replayed checkpoint by checkpoint
    think_budget   test-time compute on 9-digit lists: think for at most m steps, then answer (sequential), against
                   a vote over N answers (parallel), at equal numbers of tokens
    think_verify   an outcome reward model (is the final sum right?) and a process reward model (is each step
                   right?), trained on the same 8,000 solutions; best-of-N with each, against majority vote
    think_search   beam search over steps of thought guided by the process reward model, against best-of-N with it,
                   at equal numbers of tokens; the tree for one question
"""

from __future__ import annotations

import copy
import math

import numpy as np

S, NMIN = 10, 2  # digit slots; the shortest list
PAD, EQ, THINK, ANS, END = 10, 11, 12, 13, 14
V0, VMAX = 15, 9 * S  # value tokens: V0 + 0 .. V0 + 90
VOC = V0 + VMAX + 1
TMAX = S + 1 + 1 + (S + 2) + 1 + 1 + 1  # slots, '=', THINK, steps (with room to spare), ANS, value, END
NMAX = S - 1  # the longest list: a PAD always follows it, which is how the model knows the list has ended
NS = list(range(NMIN, NMAX + 1))
SFT_STEPS = 1500
STEP_COST = 0.02  # reward lost per step of thought, in the length-penalty runs


def _c():
    from videos.ai.ai28 import compute as c

    return c


def model():
    return _c().tiny_gpt(VOC, TMAX + 2, D=64, L=2, H=4)


def questions(g, size, n=None):
    """Digits in S slots (PAD after the list) and the list lengths."""
    ns = np.full(size, n) if n is not None else g.integers(NMIN, NMAX + 1, size)
    d = g.integers(0, 10, (size, S))
    d[np.arange(S)[None] >= ns[:, None]] = PAD
    return d, ns


def truth_of(d):
    return np.where(d == PAD, 0, d).sum(1)


def prefix_sums(d):
    return np.cumsum(np.where(d == PAD, 0, d), 1)


def sft_rows(g, size):
    d, ns = questions(g, size)
    run = prefix_sums(d)
    rows = []
    for i in range(size):
        r = g.random()
        m = -1 if r < 0.4 else (ns[i] if r < 0.8 else int(g.integers(0, ns[i])))
        seq = list(d[i]) + [EQ]
        if m >= 0:
            seq += [THINK] + [V0 + int(v) for v in run[i, :m]]
        seq += [ANS, V0 + int(run[i, ns[i] - 1]), END]
        rows.append(seq)
    return rows


def pad_rows(rows, fill=END):
    L = max(len(r) for r in rows)
    x = np.full((len(rows), L), fill)
    for i, r in enumerate(rows):
        x[i, :len(r)] = r
    return x


def train_sft(steps=SFT_STEPS, seed=0):
    import torch
    import torch.nn.functional as F

    c = _c()
    c.threads(1)
    torch.manual_seed(2021 + seed)  # 2021: Nye et al., scratchpads
    m = model()
    opt = torch.optim.AdamW(m.parameters(), lr=2e-3, weight_decay=0.01)
    g = c.rng(500 + seed)
    for _ in range(steps):
        rows = sft_rows(g, 128)
        x = torch.tensor(pad_rows(rows))
        z = m(x[:, :-1])
        tgt = x[:, 1:].clone()
        tgt[:, :S] = -100  # the question is given, not predicted: the loss starts at the token after '='
        lens = torch.tensor([len(r) for r in rows])
        tgt[torch.arange(tgt.shape[1])[None] >= (lens[:, None] - 1)] = -100
        loss = F.cross_entropy(z.reshape(-1, VOC), tgt.reshape(-1), ignore_index=-100)
        opt.zero_grad()
        loss.backward()
        opt.step()
    return m


def sft_model():
    import torch

    c = _c()
    p = c.CACHE.dir / "think_sft.pt"
    if not p.exists():
        c.CACHE.dir.mkdir(parents=True, exist_ok=True)
        torch.save(train_sft().state_dict(), p)
    m = model()
    m.load_state_dict(torch.load(p))
    return m.eval()


# ---------------------------------------------------------------------------
# Rollouts
# ---------------------------------------------------------------------------
def rollout(m, d, gen=None, temp=1.0, force=None, max_think=None, prefix_steps=None):
    """Generate from ``d`` (questions, S).  ``force``: 'think' or 'direct' for the first token; ``max_think``: answer
    after at most that many steps of thought; ``prefix_steps``: steps already written (a list per question), as in
    search.  Returns dict: tokens (B, L), gen_mask (generated positions), think (steps written), answer (-1 if the
    output was malformed), valid."""
    import torch

    B = len(d)
    x = torch.cat([torch.tensor(d), torch.full((B, 1), EQ)], 1)
    phase = torch.zeros(B, dtype=torch.long)  # 0: THINK or ANS next; 1: thinking; 2: the answer next; 3: done
    nthink = torch.zeros(B, dtype=torch.long)
    answer = torch.full((B,), -1)
    valid = torch.ones(B, dtype=torch.bool)
    gmask = []
    if prefix_steps is not None:
        pre = torch.tensor([[THINK] + [V0 + v for v in ps] for ps in prefix_steps])
        x = torch.cat([x, pre], 1)
        gmask += [torch.zeros(B, dtype=torch.bool)] * pre.shape[1]
        phase[:] = 1
        nthink[:] = pre.shape[1] - 1
    with torch.no_grad():
        for t in range(S + 5):
            if bool((phase == 3).all()):
                break
            z = m(x)[:, -1] / temp
            c = torch.multinomial(torch.softmax(z, -1), 1, generator=gen)[:, 0]
            live = phase < 3
            if t == 0 and prefix_steps is None and force is not None:
                c = torch.full((B,), THINK if force == "think" else ANS)
            if max_think is not None:
                stop = (phase == 1) & (nthink >= max_think)
                c = torch.where(stop, torch.full((B,), ANS), c)
            cap = (phase == 1) & (nthink >= S + 2)
            c = torch.where(cap, torch.full((B,), ANS), c)
            isval = c >= V0
            bad = live & (((phase == 0) & (c != THINK) & (c != ANS)) | ((phase == 1) & ~isval & (c != ANS))
                          | ((phase == 2) & ~isval))
            valid &= ~bad
            answer = torch.where(live & (phase == 2) & isval, c - V0, answer)
            nthink += (live & (phase == 1) & isval).long()
            new = phase.clone()
            new[live & (phase == 0) & (c == THINK)] = 1
            new[live & ((phase == 0) | (phase == 1)) & (c == ANS)] = 2
            new[live & (phase == 2)] = 3
            new[bad] = 3
            gmask.append(live)
            phase = new
            x = torch.cat([x, c[:, None]], 1)
    gm = torch.stack(gmask, 1) if gmask else torch.zeros(B, 0, dtype=torch.bool)
    full = torch.zeros(x.shape, dtype=torch.bool)
    full[:, S + 1:S + 1 + gm.shape[1]] = gm
    return {"tokens": x, "gen_mask": full, "think": nthink.numpy(), "answer": answer.numpy(), "valid": valid.numpy()}


def parse_steps(tokens):
    """The steps of thought in each row (a list of values), and whether the row thought at all."""
    t = np.asarray(tokens)
    out, thought = [], []
    for row in t:
        if len(row) > S + 1 and row[S + 1] == THINK:
            st = []
            for v in row[S + 2:]:
                if v >= V0:
                    st.append(int(v - V0))
                else:
                    break
            out.append(st)
            thought.append(True)
        else:
            out.append([])
            thought.append(False)
    return out, np.array(thought)


def step_labels(d, steps):
    """Each step checked on its own: s_j == s_(j-1) + d_j (s_0 = 0).  And whether it agrees with the true running
    total."""
    loc, tru = [], []
    run = prefix_sums(d)
    for i, st in enumerate(steps):
        prev, li, ti = 0, [], []
        for j, s in enumerate(st):
            dj = 0 if j >= S or d[i, j] == PAD else int(d[i, j])
            li.append(s == prev + dj and j < S and d[i, j] != PAD)
            ti.append(j < S and s == run[i, j])
            prev = s
        loc.append(li)
        tru.append(ti)
    return loc, tru


def evaluate(m, g, per_n=200, force=None, gen=None, max_think=None):
    """Accuracy, how often it thinks, and mean steps of thought, by length of list (one sample each)."""
    acc, pth, ln = [], [], []
    for n in NS:
        d, _ = questions(g, per_n, n)
        r = rollout(m, d, gen=gen, force=force, max_think=max_think)
        ok = (r["answer"] == truth_of(d)) & r["valid"]
        _, thought = parse_steps(r["tokens"].numpy())
        acc.append(float(ok.mean()))
        pth.append(float(thought.mean()))
        ln.append(float(r["think"].mean()))
    return np.array(acc), np.array(pth), np.array(ln)


def compute_think_sft():
    import torch

    c = _c()
    c.threads(1)
    m = sft_model()
    gen = torch.Generator().manual_seed(1)
    out = {"ns": NS, "S": S, "sft_steps": SFT_STEPS}
    for mode in ("direct", "think", None):
        a, p, l_ = evaluate(m, c.rng(61), 300, force=mode, gen=gen)
        key = mode or "free"
        out[f"acc_{key}"], out[f"p_think_{key}"], out[f"len_{key}"] = a, p, l_
    # a few solutions it writes, for the screen
    d = np.array([questions(c.rng(70 + n), 1, n)[0][0] for n in (3, 6, 9)])
    r = rollout(m, np.repeat(d, 4, 0), gen=gen)
    out["ex_d"], out["ex_tokens"] = np.repeat(d, 4, 0), r["tokens"].numpy()
    out["ex_answer"] = r["answer"]
    return out


def compute_think_samples(nq=300, k=64):
    """From the supervised model: k solutions per test question made to think, and k made to answer at once."""
    import torch

    c = _c()
    c.threads(1)
    m = sft_model()
    g = c.rng(81)
    d, ns = questions(g, nq)
    truth = truth_of(d)
    gen = torch.Generator().manual_seed(82)
    out = {"d": d, "n": ns, "truth": truth, "k": k}
    for mode in ("think", "direct"):
        ans, steps, ok_loc, ok_true = np.full((nq, k), -1), np.full((nq, k, S + 2), -1), [], []
        for i0 in range(0, nq, 50):
            dd = np.repeat(d[i0:i0 + 50], k, 0)
            r = rollout(m, dd, gen=gen, force=mode)
            a = np.where(r["valid"], r["answer"], -1).reshape(-1, k)
            ans[i0:i0 + 50] = a
            st, _ = parse_steps(r["tokens"].numpy())
            for j, s_ in enumerate(st):
                q, kk = divmod(j, k)
                steps[i0 + q, kk, :len(s_[:S + 2])] = s_[:S + 2]
        out[f"{mode}_answer"] = ans
        out[f"{mode}_steps"] = steps
        out[f"{mode}_acc"] = float((ans == truth[:, None]).mean())
    # step-level checks on the solutions that thought
    st = [[int(v) for v in row if v >= 0] for row in out["think_steps"].reshape(-1, S + 2)]
    loc, tru = step_labels(np.repeat(d, k, 0), st)
    all_loc = np.array([all(x) and len(x) == n for x, n in zip(loc, np.repeat(ns, k))])
    right = (out["think_answer"] == truth[:, None]).reshape(-1)
    out["right_bad_steps"] = float(np.mean(~all_loc[right])) if right.any() else 0.0  # right answer, a wrong step
    out["wrong_good_steps"] = float(np.mean(all_loc[~right])) if (~right).any() else 0.0
    # how errors compound: the chance a step is right, and a whole chain, by length of list
    step_ok = np.array([x for li in loc for x in li], bool)
    out["p_step"] = float(step_ok.mean())
    out["chain_ok_by_n"] = np.array([float(all_loc.reshape(nq, k)[ns == n].mean()) if (ns == n).any() else np.nan
                                     for n in NS])
    return out


# ---------------------------------------------------------------------------
# Reinforcement learning on the sum alone, and with a cost per step of thought
# ---------------------------------------------------------------------------
def seq_logprob(m, tokens, gmask):
    """Sum over generated positions of log pi(token)."""
    import torch

    z = m(tokens[:, :-1])
    lp = torch.log_softmax(z, -1).gather(2, tokens[:, 1:, None])[..., 0]
    return (lp * gmask[:, 1:].float()).sum(1)


def rl_run(cost, seed, steps=300, G=8, Q=32, lr=3e-4, every=10, snap_every=25):
    import torch

    c = _c()
    c.threads(1)
    m = sft_model()
    m.train()
    torch.manual_seed(900 + seed)
    gen, egen = torch.Generator().manual_seed(910 + seed), torch.Generator().manual_seed(920)
    opt = torch.optim.AdamW(m.parameters(), lr=lr)
    g = c.rng(930 + seed)
    hist, snaps = [], []
    shows = np.array([questions(c.rng(70 + n), 1, n)[0][0] for n in (3, 9)])

    def log(step):
        a, p, l_ = evaluate(m, c.rng(940), 100, gen=egen)
        hist.append(np.concatenate([[step], a, p, l_]))
        if step % snap_every == 0:
            # lengths chosen, by length of list: counts of 'at once' and of 0..S+2 steps
            H = np.zeros((len(NS), S + 4))
            for j, n in enumerate(NS):
                d, _ = questions(c.rng(950 + n), 100, n)
                r = rollout(m, d, gen=egen)
                _, th = parse_steps(r["tokens"].numpy())
                for t_, k in zip(th, r["think"]):
                    H[j, 0 if not t_ else 1 + min(int(k), S + 2)] += 1
            r = rollout(m, np.repeat(shows, 3, 0), gen=egen)
            tk = r["tokens"].numpy()
            tk = np.pad(tk, ((0, 0), (0, TMAX + 2 - tk.shape[1])), constant_values=-1)
            snaps.append((step, H, tk, r["answer"]))
        print(f"    think rl cost {cost} seed {seed} step {step}: acc {a.mean():.1%}, thinks {p.mean():.0%}, "
              f"steps {l_.mean():.2f}", flush=True)

    log(0)
    for step in range(1, steps + 1):
        d, ns = questions(g, Q)
        dd = np.repeat(d, G, 0)
        r = rollout(m, dd, gen=gen)
        ok = ((r["answer"] == np.repeat(truth_of(d), G)) & r["valid"]).astype(float)
        rew = (ok - cost * r["think"]).reshape(Q, G)
        adv = (rew - rew.mean(1, keepdims=True)) / (rew.std(1, keepdims=True) + 1e-6)
        A = torch.tensor(adv.reshape(-1), dtype=torch.float32)
        lp = seq_logprob(m, r["tokens"], r["gen_mask"])
        loss = -(A * lp).sum() / (len(A) * (S + 4))  # a constant normalizer (Dr. GRPO), not the answer's length
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0)
        opt.step()
        if step % every == 0:
            log(step)
    out = {"hist": np.array(hist)}
    out["snap_steps"] = np.array([s[0] for s in snaps])
    out["snap_hist"] = np.array([s[1] for s in snaps])
    out["snap_tok"] = np.array([s[2] for s in snaps])
    out["snap_answer"] = np.array([s[3] for s in snaps])
    out["shows"] = np.repeat(shows, 3, 0)
    if seed == 0:
        torch.save(m.state_dict(), c.CACHE.dir / f"think_rl_{'pen' if cost else 'plain'}.pt")
    return out


def compute_think_rl(seeds=3):
    c = _c()
    out = {"ns": NS, "cost": STEP_COST, "seeds": seeds, "S": S}
    for name, cost in (("plain", 0.0), ("pen", STEP_COST)):
        runs = []
        for s in range(seeds):
            runs.append(c.memo(f"think_rl_{name}_{s}", lambda: rl_run(cost, s)))
        H = np.stack([np.asarray(r["hist"], float) for r in runs])  # (seeds, logs, 1 + 3 * len(NS))
        k = len(NS)
        out[f"{name}_steps"] = H[0, :, 0]
        out[f"{name}_acc"], out[f"{name}_think"], out[f"{name}_len"] = H[:, :, 1:1 + k], H[:, :, 1 + k:1 + 2 * k], \
            H[:, :, 1 + 2 * k:]
        out[f"{name}_snap_steps"] = np.asarray(runs[0]["snap_steps"])
        out[f"{name}_snap_hist"] = np.asarray(runs[0]["snap_hist"])
        out[f"{name}_snap_tok"] = np.asarray(runs[0]["snap_tok"])
        out[f"{name}_snap_answer"] = np.asarray(runs[0]["snap_answer"])
        out["shows"] = np.asarray(runs[0]["shows"])
    return out


# ---------------------------------------------------------------------------
# Test-time compute: a longer chain against more votes, at equal tokens
# ---------------------------------------------------------------------------
def compute_think_budget(nq=400, n=NMAX):
    import torch

    c = _c()
    c.threads(1)
    gen = torch.Generator().manual_seed(71)
    d, _ = questions(c.rng(72), nq, n)
    truth = truth_of(d)
    out = {"n": n, "nq": nq}
    for name in ("sft", "rl"):
        if name == "sft":
            m = sft_model()
        else:
            p = c.CACHE.dir / "think_rl_plain.pt"
            m = model()
            m.load_state_dict(torch.load(p))
            m.eval()
        seq = []
        for mt in range(0, n + 1):  # think at most mt steps, then answer: tokens = THINK + mt + ANS + value
            r = rollout(m, d, gen=gen, force="think", max_think=mt)
            seq.append(float(((r["answer"] == truth) & r["valid"]).mean()))
        out[f"{name}_seq"] = np.array(seq)
        out[f"{name}_seq_tokens"] = np.array([mt + 3 for mt in range(0, n + 1)])
        # parallel: N answers at once (ANS + value: 2 tokens each), majority vote
        K = 16
        r = rollout(m, np.repeat(d, K, 0), gen=gen, force="direct")
        A = np.where(r["valid"], r["answer"], -1).reshape(nq, K)
        votes = []
        g = c.rng(73)
        for N in (1, 2, 4, 8, 16):
            hits = []
            for _ in range(10):
                idx = np.stack([g.choice(K, N, replace=False) for _ in range(nq)])
                pick = np.take_along_axis(A, idx, 1)
                mode = np.array([np.bincount(row[row >= 0], minlength=VMAX + 1).argmax() if (row >= 0).any() else -1
                                 for row in pick])
                hits.append(float((mode == truth).mean()))
            votes.append(float(np.mean(hits)))
        out[f"{name}_vote"] = np.array(votes)
        out[f"{name}_vote_tokens"] = np.array([2 * N for N in (1, 2, 4, 8, 16)])
    return out


# ---------------------------------------------------------------------------
# Outcome and process reward models
# ---------------------------------------------------------------------------
def verifier_data(m, g, gen, nq, k):
    """k solutions (made to think) per question from model m: tokens, the answer position, and labels."""
    d, ns = questions(g, nq)
    dd = np.repeat(d, k, 0)
    r = rollout(m, dd, gen=gen, force="think")
    tok = r["tokens"].numpy()
    steps, _ = parse_steps(tok)
    loc, _ = step_labels(dd, steps)
    truth = truth_of(dd)
    final = (r["answer"] == truth) & r["valid"]
    # positions: step j's value sits at S + 2 + j; the answer at S + 2 + len(steps) + 1
    step_pos = [[S + 2 + j for j in range(len(st))] for st in steps]
    ans_pos = np.array([S + 3 + len(st) for st in steps])
    # the answer step is right if it equals the last running total written (plus any digits not yet added)
    last = np.array([st[-1] if st else 0 for st in steps])
    rest = np.array([int(np.where(row == PAD, 0, row)[len(st):].sum()) for row, st in zip(dd, steps)])
    ans_local = (r["answer"] == last + rest) & r["valid"]
    return dict(tokens=tok, step_pos=step_pos, step_ok=loc, ans_pos=ans_pos, final=final, ans_local=ans_local,
                answer=np.where(r["valid"], r["answer"], -1), truth=truth, d=dd, n=np.repeat(ns, k))


def train_verifier(data, kind, steps=1500, seed=0):
    """kind 'orm': one label per solution, at its answer (is the sum right?).  kind 'prm': a label at every step and
    at the answer (is this step right, given the one before?)."""
    import torch
    import torch.nn.functional as F

    c = _c()
    c.threads(1)
    torch.manual_seed(3000 + seed)
    v = model()
    opt = torch.optim.AdamW(v.parameters(), lr=1e-3, weight_decay=0.01)
    tok = torch.tensor(data["tokens"])
    B, L = tok.shape
    lab = torch.full((B, L), -1.0)
    rows = np.arange(B)
    ap = np.minimum(data["ans_pos"], L - 1)
    if kind == "orm":
        lab[rows, ap] = torch.tensor(data["final"], dtype=torch.float32)
    else:
        for i, (ps, ok) in enumerate(zip(data["step_pos"], data["step_ok"])):
            for p_, o in zip(ps, ok):
                if p_ < L:
                    lab[i, p_] = float(o)
        lab[rows, ap] = torch.tensor(data["ans_local"], dtype=torch.float32)
    g = c.rng(3100 + seed)
    for _ in range(steps):
        idx = g.integers(0, B, 128)
        z = v(tok[idx])[..., 0]
        y = lab[idx]
        msk = y >= 0
        loss = F.binary_cross_entropy_with_logits(z[msk], y[msk])
        opt.zero_grad()
        loss.backward()
        opt.step()
    return v.eval()


def verifier_scores(v, data, kind):
    """A solution's score: the ORM's probability at the answer; the PRM's product over steps and the answer."""
    import torch

    tok = torch.tensor(data["tokens"])
    L = tok.shape[1]
    out, per_step = [], []
    with torch.no_grad():
        for i0 in range(0, len(tok), 4096):
            p = torch.sigmoid(v(tok[i0:i0 + 4096])[..., 0]).numpy()
            for j, row in enumerate(p):
                i = i0 + j
                ap = min(int(data["ans_pos"][i]), L - 1)
                if kind == "orm":
                    out.append(float(row[ap]))
                else:
                    ps = [row[q] for q in data["step_pos"][i] if q < L]
                    per_step.append(ps + [row[ap]])
                    out.append(float(np.prod(ps) * row[ap]))
    return np.array(out), per_step


def compute_think_verify(n_train=1000, k_train=8, nq=300, k=64):
    import torch

    c = _c()
    c.threads(1)
    m = sft_model()
    gen = torch.Generator().manual_seed(91)
    train = verifier_data(m, c.rng(92), gen, n_train, k_train)
    test = verifier_data(m, c.rng(93), gen, nq, k)
    scores = {}
    for kind in ("orm", "prm"):
        v = train_verifier(train, kind)
        scores[kind], per = verifier_scores(v, test, kind)
        if kind == "prm":
            prm_steps = per
    ans = test["answer"].reshape(nq, k)
    truth = test["truth"].reshape(nq, k)[:, 0]
    right = ans == truth[:, None]
    Ns = [N for N in (1, 2, 4, 8, 16, 32, 64) if N <= k]
    g = c.rng(94)
    res = {key: [] for key in ("orm", "prm", "vote", "oracle", "first")}
    for N in Ns:
        acc = {key: [] for key in res}
        for _ in range(20 if N < k else 1):
            idx = np.stack([g.choice(k, N, replace=False) for _ in range(nq)])
            R = np.take_along_axis(right, idx, 1)
            acc["oracle"].append(R.any(1).mean())
            acc["first"].append(R[:, 0].mean())
            for kind in ("orm", "prm"):
                sc = np.take_along_axis(scores[kind].reshape(nq, k), idx, 1)
                acc[kind].append(R[np.arange(nq), sc.argmax(1)].mean())
            A = np.take_along_axis(ans, idx, 1)
            mode = np.array([np.bincount(row[row >= 0], minlength=VMAX + 1).argmax() if (row >= 0).any() else -1
                             for row in A])
            acc["vote"].append((mode == truth).mean())
        for key in res:
            res[key].append(float(np.mean(acc[key])))
    # one solution with a wrong step, scored step by step, for the screen
    flat_ok = [all(o) for o in test["step_ok"]]
    pick = next((i for i in range(len(flat_ok)) if not flat_ok[i] and test["n"][i] >= 6 and len(test["step_ok"][i]) >= 5),
                0)
    out = dict(Ns=Ns, n_train=n_train * k_train, nq=nq, k=k, **{f"bo_{key}": np.array(v_) for key, v_ in res.items()})
    out["ex_d"] = test["d"][pick]
    out["ex_tokens"] = test["tokens"][pick]
    out["ex_step_ok"] = np.array(test["step_ok"][pick] + [bool(test["ans_local"][pick])])
    out["ex_prm"] = np.array(prm_steps[pick])
    out["ex_orm"] = float(scores["orm"][pick])
    out["ex_final"] = bool(test["final"][pick])
    # how well each separates right from wrong solutions (area under the ROC curve)
    for kind in ("orm", "prm"):
        s_, y_ = scores[kind], test["final"]
        order = np.argsort(s_)
        ranks = np.empty(len(s_))
        ranks[order] = np.arange(1, len(s_) + 1)
        npos, nneg = y_.sum(), (~y_).sum()
        out[f"auc_{kind}"] = float((ranks[y_].sum() - npos * (npos + 1) / 2) / max(npos * nneg, 1))
    out["sample_acc"] = float(right.mean())
    torch.save(v.state_dict(), c.CACHE.dir / "think_prm.pt")
    return out


# ---------------------------------------------------------------------------
# Search over steps of thought
# ---------------------------------------------------------------------------
def prm_model():
    import torch

    c = _c()
    v = model()
    v.load_state_dict(torch.load(c.CACHE.dir / "think_prm.pt"))
    return v.eval()


def beam_search(m, v, d, beam=4, expand=4, gen=None, keep_tree=False):
    """Step-level beam search: each beam proposes ``expand`` next steps (sampled), the process reward model scores
    every partial chain (product of its step scores), the best ``beam`` survive.  After n steps: ANS and the model's
    answer.  Tokens generated: beam * expand per step."""
    import torch

    nq = len(d)
    n = (d != PAD).sum(1)
    beams = [[([], 1.0)] for _ in range(nq)]
    tree = []
    for j in range(int(n.max())):
        cand_q, cand_steps, cand_parent = [], [], []
        for i in range(nq):
            if j >= n[i]:
                continue
            for b_, (st, sc) in enumerate(beams[i]):
                cand_q += [i] * expand
                cand_steps += [st] * expand
                cand_parent += [b_] * expand
        if not cand_q:
            break
        dq = d[cand_q]
        base = torch.cat([torch.tensor(dq), torch.full((len(dq), 1), EQ),
                          torch.tensor([[THINK] + [V0 + s for s in st] for st in cand_steps])], 1)
        with torch.no_grad():
            p = torch.softmax(m(base)[:, -1], -1)
            p[:, :V0] = 0  # a step of thought is a running total
            nxt = torch.multinomial(p / p.sum(1, keepdim=True), 1, generator=gen)[:, 0] - V0
            ext = torch.cat([base, (nxt + V0)[:, None]], 1)
            sc = torch.sigmoid(v(ext)[:, -1, 0]).numpy()
        new = [dict() for _ in range(nq)]
        for c_, (i, st, par) in enumerate(zip(cand_q, cand_steps, cand_parent)):
            key = tuple(st) + (int(nxt[c_]),)
            score = beams[i][par][1] * float(sc[c_])
            if key not in new[i] or new[i][key] < score:
                new[i][key] = score
        level = []
        for i in range(nq):
            if j >= n[i]:
                continue
            ranked = sorted(new[i].items(), key=lambda kv: -kv[1])
            if keep_tree and i == 0:
                level.append([(list(k_), s_, r_ < beam) for r_, (k_, s_) in enumerate(ranked)])
            beams[i] = [(list(k_), s_) for k_, s_ in ranked[:beam]]
        if keep_tree:
            tree.append(level[0] if level else [])
    best = [max(b, key=lambda t_: t_[1])[0] for b in beams]
    dd = np.asarray(d)
    x = torch.cat([torch.tensor(dd), torch.full((nq, 1), EQ),
                   torch.tensor(np.array([[THINK] + [V0 + s for s in st] + [END] * (S - len(st)) for st in best]))], 1)
    # answer after each chain (rows have different lengths: run them one length at a time)
    answer = np.zeros(nq, int)
    for L in set(len(st) for st in best):
        idx = [i for i, st in enumerate(best) if len(st) == L]
        xi = torch.cat([x[idx, :S + 2 + L], torch.full((len(idx), 1), ANS)], 1)
        with torch.no_grad():
            z = m(xi)[:, -1, V0:]
        answer[idx] = z.argmax(-1).numpy()
    return answer, best, tree


def compute_think_search(nq=300, n=NMAX):
    import torch

    c = _c()
    c.threads(1)
    m, v = sft_model(), prm_model()
    gen = torch.Generator().manual_seed(95)
    d, _ = questions(c.rng(96), nq, n)
    truth = truth_of(d)
    out = {"n": n, "nq": nq}
    configs = [(1, 2), (2, 2), (2, 4), (4, 4), (4, 8)]  # (beam, expand): tokens per step = beam * expand
    bs = []
    for b, e in configs:
        ans, _, _ = beam_search(m, v, d, b, e, gen=gen)
        bs.append(float((ans == truth).mean()))
    out["beam_cfg"] = np.array(configs)
    out["beam_acc"] = np.array(bs)
    out["beam_width"] = np.array([b * e for b, e in configs])  # samples per step, the same budget as best-of-N
    # best-of-N with the same verifier at the same budget: N whole solutions made to think
    Ns = sorted(set(b * e for b, e in configs))
    K = max(Ns)
    dd = np.repeat(d, K, 0)
    r = rollout(m, dd, gen=gen, force="think")
    tok = r["tokens"].numpy()
    steps, _ = parse_steps(tok)
    sd = dict(tokens=tok, step_pos=[[S + 2 + j for j in range(len(st))] for st in steps],
              ans_pos=np.array([S + 3 + len(st) for st in steps]))
    sc, _ = verifier_scores(v, sd, "prm")
    A = np.where(r["valid"], r["answer"], -1).reshape(nq, K)
    sc = sc.reshape(nq, K)
    g = c.rng(97)
    bon = []
    for N in Ns:
        hits = []
        for _ in range(10 if N < K else 1):
            idx = np.stack([g.choice(K, N, replace=False) for _ in range(nq)])
            pick = np.take_along_axis(A, idx, 1)[np.arange(nq), np.take_along_axis(sc, idx, 1).argmax(1)]
            hits.append(float((pick == truth).mean()))
        bon.append(float(np.mean(hits)))
    out["bon_N"], out["bon_acc"] = np.array(Ns), np.array(bon)
    # the tree for one question, for the screen
    _, best, tree = beam_search(m, v, d[:1], 3, 3, gen=gen, keep_tree=True)
    out["tree_d"] = d[0]
    out["tree"] = [[(list(map(int, k_)), float(s_), bool(kept)) for k_, s_, kept in lev] for lev in tree]
    out["tree_best"] = list(map(int, best[0]))
    return out


ITEMS = {
    "think_sft": compute_think_sft,
    "think_samples": compute_think_samples,
    "think_rl": compute_think_rl,
    "think_budget": compute_think_budget,
    "think_verify": compute_think_verify,
    "think_search": compute_think_search,
}
