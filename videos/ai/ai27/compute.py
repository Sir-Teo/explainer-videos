"""Precompute everything numerical in Part 27 of the AI series ("Post-Training and Alignment").

    python -m explainer.ai.novels            # first: the series' base model (cached in .cache/novels/)
    python -m videos.ai.ai27.compute         # everything missing
    python -m videos.ai.ai27.compute --force rlhf

Results are cached in ``.cache/ai27/<name>.json`` (+ ``.npz``); trained weights in ``.cache/ai27/*.pt``.  Every model
here is the series' 6.8-million-parameter novels model or a descendant of it, trained on this computer.

Two tasks, both made from the novels (questions about held-out paragraphs are kept for testing):

* **Which book?**  ``Which book is this from? "<a sentence>"`` -> the title.  Checkable: an answer is right or wrong.
* **A line about...**  ``Write a line about the sea.`` -> a sentence about the sea.  Graded by a stand-in for human
  taste, ``gold``: it likes cheerful words, dislikes gloomy ones, and dislikes repetition and empty answers.  The
  "people" who compare two answers are simulated from it with Bradley-Terry noise.  Everything that optimizes
  against human preferences here optimizes against a reward model learned from those comparisons, never gold.

Items:
    data       the two tasks: training and test questions
    sft        supervised fine-tuning on both tasks: the base model against the fine-tuned one (accuracy, answers,
               held-out loss on the novels), the training curve
    lora       LoRA at ranks 1, 4 and 16 against full fine-tuning: trainable parameters, accuracy, forgetting
    prefs      comparisons: pairs of the fine-tuned model's lines, labelled by simulated people
    rm         reward models (Bradley-Terry) trained on 100 to 3,200 comparisons: accuracy on held-out pairs
    rlaif      AI feedback in miniature: a reward model from 100 comparisons labels 1,600 more for a fresh one
    closed     the KL-regularized optimum over eight candidate answers: pi* proportional to pi_ref exp(r / beta)
    bon        best-of-n against the reward model, n = 1 .. 256: proxy and gold reward against KL = log n - (n-1)/n
    rlhf       KL-penalized policy gradient against the reward model, at two penalties: reward, gold and KL as it
               trains, and answers along the way
    dpo        direct preference optimization on the same comparisons: gold reward and KL, the chosen and rejected
               answers' log-probabilities as it trains
    distill    a 2-layer student of the base model: from the text alone, and from the teacher's probabilities
    merge      task vectors: each task fine-tuned alone, then added to the base model; the path between them
"""

from __future__ import annotations

import copy
import math
import os
import re

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from explainer.ai import novels as N
from explainer.ai.cache import Cache
from videos.ai.ai27 import post as P

CACHE = Cache("ai27")
load = CACHE.load
# 2 threads by default: on a shared 4-core machine more threads ran slower, not faster
torch.set_num_threads(int(os.environ.get("AI27_THREADS", "2")))


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


# ---------------------------------------------------------------------------
# The tasks
# ---------------------------------------------------------------------------
TOPICS = ["sea", "night", "house", "door", "fire", "river", "garden", "letter", "window", "horse", "ship", "money",
          "church", "road", "rain", "sun", "moon", "wind", "child", "heart", "face", "hand", "eyes", "voice", "room",
          "town", "dinner", "morning", "music", "book"]
TEST_TOPICS = TOPICS  # prompts are few; the comparisons, samples and seeds differ between training and testing

POSITIVE = set("""happy happiness joy joyful joyous delight delighted delightful glad gladness cheerful cheer cheered
bright brightly beautiful lovely love loved loving smile smiled smiles smiling laugh laughed laughing laughter warm
warmly kind kindly kindness gentle gently sweet sweetly pleasant pleasure pleased hope hopeful merry charming
wonderful good best better peace peaceful calm comfort comfortable friend friends friendly grateful thank thanks
blessed blessing golden sunshine sunny glorious splendid admire admired tender cheerfully bliss safe
graceful grace honest generous delicious fresh lively playful proud rejoice rejoiced triumph victory""".split())
NEGATIVE = set("""sad sadness sorrow sorrowful grief grieve dark darkness death dead die died dying fear
feared afraid terror terrible terribly horrible dreadful dread pain painful cruel cruelty misery miserable unhappy
wretched poor weep wept weeping tears cry cried crying angry anger hate hated hatred gloomy gloom blood bloody
murder kill killed lonely despair lost evil sick ill wicked ugly storm ruin ruined bitter bitterly shame ashamed guilt
guilty danger dangerous pale wound wounded suffer suffered suffering hell grim fierce harsh weary wretchedness""".split())
WORD = re.compile(r"[a-z']+")


def gold(text: str) -> float:
    """The stand-in for human taste on 'a line about...': cheerful beats gloomy, but not by repeating words, and an
    empty or broken line is worst.  In [-2, 1]."""
    words = WORD.findall(text.lower())
    if len(words) < 4:
        return -1.0
    pos = sum(w in POSITIVE for w in words)
    neg = sum(w in NEGATIVE for w in words)
    repeat = 1 - len(set(words)) / len(words)  # 0 for all-different words
    return float(math.tanh((pos - neg) / 2) - 2.5 * max(0.0, repeat - 0.15))


def _paragraphs():
    """Each novel's paragraphs, split as Part 1 split them (every 20th block of 40 paragraphs held out)."""
    from videos.ai.ai1 import compute as ai1

    out = {}
    for n, title in ai1.BOOKS.items():
        raw = (ai1.BOOK_DIR / f"{n}.txt").read_text(encoding="utf-8", errors="replace")
        paras = ai1.clean(ai1.strip_gutenberg(raw)).split("\n")
        train, valid = [], []
        for k in range(0, len(paras), 40):
            (valid if (k // 40) % 20 == 7 else train).extend(paras[k:k + 40])
        out[title] = (train, valid)
    return out


SPLIT = re.compile(r'(?<=[.!?])\s+(?=[A-Z"])')
PLAIN = re.compile(r"^[A-Za-z0-9 ,.;:!?'\"-]+$")


def _sentences(paras):
    for p in paras:
        for s in SPLIT.split(p):
            s = s.strip()
            if 8 <= len(s.split()) <= 26 and PLAIN.match(s) and s[0].isupper():
                yield s


def compute_data(per_book_train=200, per_book_test=20, per_topic=200):
    g = rng(0)
    books = _paragraphs()
    which_train, which_test, lines = [], [], {t: [] for t in TOPICS}
    for title, (train, valid) in books.items():
        tr, te = list(_sentences(train)), list(_sentences(valid))
        for s in g.choice(tr, min(per_book_train, len(tr)), replace=False):
            which_train.append((str(s), title))
        for s in g.choice(te, min(per_book_test, len(te)), replace=False) if te else []:
            which_test.append((str(s), title))
        for s in tr:
            low = set(WORD.findall(s.lower()))
            for t in TOPICS:
                if t in low:
                    lines[t].append(s)
    line_train = []
    for t in TOPICS:
        pick = g.choice(lines[t], min(per_topic, len(lines[t])), replace=False)
        line_train += [(t, str(s)) for s in pick]
    golds = [gold(s) for _, s in line_train]
    return {"which_train": which_train, "which_test": which_test, "line_train": line_train,
            "titles": list(books), "topics": TOPICS, "line_gold_mean": float(np.mean(golds)),
            "line_gold": np.array(golds)}


def which_q(s: str) -> str:
    return f'Which book is this from? "{s}"'


def line_q(topic: str) -> str:
    return f"Write a line about the {topic}."


def sft_examples(d, tasks=("which", "line")):
    ex = []
    if "which" in tasks:
        ex += [(P.chat(which_q(s)), N.encode(t) + [N.special("<|end|>")]) for s, t in d["which_train"]]
    if "line" in tasks:
        ex += [(P.chat(line_q(t)), N.encode(s) + [N.special("<|end|>")]) for t, s in d["line_train"]]
    return ex


def which_accuracy(model, d, n: int | None = None) -> float:
    test = d["which_test"][:n] if n else d["which_test"]
    ok = 0
    for s, title in test:
        ans = P.text_of(P.greedy(model, P.chat(which_q(s)), 16)).rstrip(".")
        ok += ans == title
    return ok / len(test)


def line_eval(model, n_per_topic=4, seed=0, temperature=1.0):
    """Mean gold reward of sampled lines, the share that end cleanly, and a few examples."""
    golds, ended, examples = [], [], []
    end = N.special("<|end|>")
    for k, t in enumerate(TOPICS):
        for ids in P.sample(model, P.chat(line_q(t)), n_per_topic, 40, temperature, seed=1000 * seed + k):
            txt = P.text_of(ids)
            golds.append(gold(txt))
            ended.append(end in ids)
            if len(examples) < 8 and k % 4 == 0:
                examples.append((t, txt))
    return float(np.mean(golds)), float(np.mean(ended)), examples


def _base():
    return N.load_base()


def _save_model(model, name):
    CACHE.dir.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), CACHE.dir / f"{name}.pt")


def _load_model(name):
    m = _base()
    m.load_state_dict(torch.load(CACHE.dir / f"{name}.pt"))
    return m.eval()


# ---------------------------------------------------------------------------
# Supervised fine-tuning, LoRA
# ---------------------------------------------------------------------------
SFT_STEPS, SFT_LR = 1500, 5e-4


def compute_sft():
    d = load("data")
    _, valid = N.token_arrays()
    base = _base()
    out = {"base_heldout": P.heldout_loss(base, valid)}
    out["base_which"] = which_accuracy(base, d, 120)
    out["base_answers"] = [(s, t, P.text_of(P.sample(base, P.chat(which_q(s)), 1, 30, 0.8, seed=i)[0]))
                           for i, (s, t) in enumerate(d["which_test"][:3])]
    out["base_lines"] = [(t, P.text_of(P.sample(base, P.chat(line_q(t)), 1, 30, 0.8, seed=i)[0]))
                         for i, t in enumerate(TOPICS[:3])]
    model = copy.deepcopy(base)
    curve, evals = P.sft(model, sft_examples(d), SFT_STEPS, SFT_LR, eval_fn=lambda m: which_accuracy(m, d, 150),
                         eval_every=250)
    _save_model(model, "sft")
    out["curve"], out["evals"] = np.array(curve), np.array(evals)
    out["sft_which"] = which_accuracy(model, d)
    out["sft_heldout"] = P.heldout_loss(model, valid)
    out["sft_line_gold"], out["sft_line_ended"], out["sft_lines"] = line_eval(model)
    out["sft_answers"] = [(s, t, P.text_of(P.greedy(model, P.chat(which_q(s)), 16)))
                          for s, t in d["which_test"][:6]]
    out["chance"] = 1 / len(d["titles"])
    return out


def compute_lora(ranks=(1, 4, 16)):
    d = load("data")
    _, valid = N.token_arrays()
    ex = sft_examples(d, ("which",))
    out = {"ranks": list(ranks)}
    runs = []
    for r in list(ranks) + ["full"]:
        model = copy.deepcopy(_base())
        if r == "full":
            params, lr = [p for p in model.parameters()], SFT_LR
            n = sum(p.numel() for p in params)
        else:
            params, lr = P.add_lora(model, r), 2e-3
            n = sum(p.numel() for p in params)
        curve, evals = P.sft(model, ex, SFT_STEPS, lr, params=params, eval_fn=lambda m: which_accuracy(m, d, 150),
                             eval_every=300)
        runs.append({"rank": r, "params": int(n), "which": which_accuracy(model, d),
                     "heldout": P.heldout_loss(model, valid), "evals": evals, "loss": [c[1] for c in curve]})
    out["runs"] = runs
    out["total_params"] = int(sum(p.numel() for p in _base().parameters()))
    out["base_heldout"] = P.heldout_loss(_base(), valid)
    return out


# ---------------------------------------------------------------------------
# Comparisons, reward models
# ---------------------------------------------------------------------------
TAU = 0.25  # the simulated people's noise: P(a beats b) = sigmoid((gold a - gold b) / TAU)


def compute_prefs(per_topic=32, n_test=8, seed=0):
    """Lines from the fine-tuned model, paired within a topic and judged by simulated people.  Each topic's lines are
    split before pairing: the test comparisons are between lines no reward model has seen in training."""
    g = rng(seed)
    sft = _load_model("sft")
    train, test = [], []
    for k, t in enumerate(TOPICS):
        outs = [P.text_of(ids) for ids in P.sample(sft, P.chat(line_q(t)), per_topic, 40, 1.0, seed=50 + k)]
        idx = g.permutation(per_topic)
        tr, te = idx[n_test:], idx[:n_test]
        cand = [(tr[i], tr[j]) for i in range(0, len(tr) - 1, 2) for j in range(i + 1, len(tr), 3)]
        cand_te = [(te[i], te[j]) for i in range(len(te)) for j in range(i + 1, len(te))]
        for dest, cs in ((train, cand), (test, cand_te)):
            for i, j in cs:
                a, b = outs[i], outs[j]
                if a == b:
                    continue
                pa = 1 / (1 + math.exp(-(gold(a) - gold(b)) / TAU))
                win = g.random() < pa
                dest.append({"topic": t, "chosen": a if win else b, "rejected": b if win else a})
    g.shuffle(train)  # (lists of dicts: shuffled in place)
    g.shuffle(test)
    return {"test": test, "train": train}


class RewardModel(nn.Module):
    """The fine-tuned model's body with a scalar head on the last token: r(question, answer)."""

    def __init__(self, body):
        super().__init__()
        self.body = body
        self.head = nn.Linear(body.cfg.d, 1)
        nn.init.zeros_(self.head.weight)
        nn.init.zeros_(self.head.bias)

    def forward(self, examples):
        x, _, m = P.pack(examples)
        h = self.body.emb(x)
        for b in self.body.blocks:
            h = b(h)
        h = self.body.norm(h)
        last = (m.argmax(-1) + m.sum(-1) - 1).long()  # the position of the answer's last input token
        return self.head(h[torch.arange(len(examples)), last]).squeeze(-1)


def _pair_examples(pairs):
    w = [(P.chat(line_q(p["topic"])), N.encode(p["chosen"]) + [N.special("<|end|>")]) for p in pairs]
    l_ = [(P.chat(line_q(p["topic"])), N.encode(p["rejected"]) + [N.special("<|end|>")]) for p in pairs]
    return w, l_


def train_rm(pairs, steps=600, batch=32, lr=3e-4, seed=0):
    torch.manual_seed(seed)
    g = rng(seed)
    rm = RewardModel(copy.deepcopy(_load_model("sft")))
    opt = torch.optim.AdamW(rm.parameters(), lr=lr, weight_decay=0.0)
    w, l_ = _pair_examples(pairs)
    rm.train()
    for step in range(steps):
        idx = g.integers(0, len(pairs), batch)
        rw, rl = rm([w[i] for i in idx]), rm([l_[i] for i in idx])
        loss = -F.logsigmoid(rw - rl).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
    return rm.eval()


@torch.no_grad()
def rm_accuracy(rm, pairs):
    w, l_ = _pair_examples(pairs)
    ok = 0
    for i in range(0, len(pairs), 64):
        ok += int((rm(w[i:i + 64]) > rm(l_[i:i + 64])).sum())
    return ok / len(pairs)


@torch.no_grad()
def rm_score(rm, topic, texts):
    ex = [(P.chat(line_q(topic)), N.encode(t) + [N.special("<|end|>")]) for t in texts]
    return torch.cat([rm(ex[i:i + 64]) for i in range(0, len(ex), 64)]).numpy()


def compute_rm(sizes=(100, 400, 1600)):
    pr = load("prefs")
    train, test = pr["train"], pr["test"]
    sizes = [s for s in sizes if s <= len(train)] + [len(train)]
    # how often the simulated people agree with gold's ranking: the ceiling on any reward model's accuracy
    agree = float(np.mean([gold(p["chosen"]) >= gold(p["rejected"]) for p in test]))
    acc = []
    for n in sizes:
        rm = train_rm(train[:n], steps=min(600, 30 + 4 * n))
        acc.append(rm_accuracy(rm, test))
        if n == sizes[-1]:
            torch.save(rm.state_dict(), CACHE.dir / "rm.pt")
        if n == sizes[0]:
            torch.save(rm.state_dict(), CACHE.dir / "rm_small.pt")
    return {"sizes": sizes, "acc": acc, "people_agree_gold": agree, "n_test": len(test)}


def _load_rm(name="rm"):
    rm = RewardModel(_load_model("sft"))
    rm.load_state_dict(torch.load(CACHE.dir / f"{name}.pt"))
    return rm.eval()


def compute_rlaif(n_human=100, n_ai=1600):
    """AI feedback, in miniature: a reward model trained on few human comparisons labels many more, and a fresh
    reward model learns from its labels."""
    pr = load("prefs")
    train, test = pr["train"], pr["test"]
    n_ai = min(n_ai, len(train) - n_human)
    judge = train_rm(train[:n_human], steps=min(600, 30 + 4 * n_human))
    fresh = train[n_human:n_human + n_ai]
    relabel = []
    for k in range(0, len(fresh), 64):
        chunk = fresh[k:k + 64]
        w, l_ = _pair_examples(chunk)
        with torch.no_grad():
            keep = (judge(w) >= judge(l_)).numpy()
        for p_, ok in zip(chunk, keep):
            relabel.append(p_ if ok else {"topic": p_["topic"], "chosen": p_["rejected"], "rejected": p_["chosen"]})
    agree = float(np.mean([r is p_ for r, p_ in zip(relabel, fresh)]))
    ai_rm = train_rm(relabel, steps=min(600, 30 + 4 * n_ai))
    full_rm = train_rm(fresh, steps=min(600, 30 + 4 * n_ai))
    return {"n_human": n_human, "n_ai": n_ai, "acc_small": rm_accuracy(judge, test), "acc_ai": rm_accuracy(ai_rm, test),
            "acc_full": rm_accuracy(full_rm, test), "judge_agrees_people": agree}


# ---------------------------------------------------------------------------
# The KL-regularized optimum, best-of-n
# ---------------------------------------------------------------------------
def compute_closed(k=8, topic="sea"):
    """pi*(y) proportional to pi_ref(y) exp(r(y) / beta), over k sampled candidates (pi_ref renormalized over them)."""
    sft = _load_model("sft")
    outs = [P.text_of(ids) for ids in P.sample(sft, P.chat(line_q(topic)), 64, 40, 1.0, seed=7)]
    seen, cand = set(), []
    for o in outs:
        if o not in seen and len(o.split()) >= 4:
            seen.add(o)
            cand.append(o)
    golds = np.array([gold(c) for c in cand])
    order = np.argsort(golds)
    pick = [cand[i] for i in order[np.linspace(0, len(cand) - 1, k).astype(int)]]
    with torch.no_grad():
        lp = P.seq_logprob(sft, [(P.chat(line_q(topic)), N.encode(c) + [N.special("<|end|>")]) for c in pick]).numpy()
    ref = np.exp(lp - lp.max())
    ref /= ref.sum()
    r = np.array([gold(c) for c in pick])
    betas = [10.0, 1.0, 0.3, 0.1]
    pis = []
    for b in betas:
        w = ref * np.exp((r - r.max()) / b)
        pis.append(w / w.sum())
    return {"topic": topic, "cands": pick, "r": r, "ref": ref, "betas": betas, "pi": np.array(pis)}


def compute_bon(pool=256, topics=12):
    """Best-of-n by the reward model, scored by gold.  Expected values over random n-subsets of a pool of samples:
    the item ranked i-th of N by the proxy is the subset's best with probability C(i-1, n-1) / C(N, n)."""
    sft = _load_model("sft")
    rms = {"large": _load_rm("rm"), "small": _load_rm("rm_small")}
    ns = [1, 2, 4, 8, 16, 32, 64, 128, 256]
    res = {k: {"proxy": np.zeros(len(ns)), "gold": np.zeros(len(ns))} for k in rms}
    worst = []
    for k, t in enumerate(TOPICS[:topics]):
        texts = [P.text_of(ids) for ids in P.sample(sft, P.chat(line_q(t)), pool, 40, 1.0, seed=300 + k)]
        gl = np.array([gold(x) for x in texts])
        for name, rm in rms.items():
            pr = rm_score(rm, t, texts)
            order = np.argsort(pr)  # ascending: rank i (1-based) = position + 1
            for j, n in enumerate(ns):
                i = np.arange(1, pool + 1)
                w = np.array([math.comb(int(a) - 1, n - 1) for a in i], float) / math.comb(pool, n)
                res[name]["proxy"][j] += float((w * pr[order]).sum()) / topics
                res[name]["gold"][j] += float((w * gl[order]).sum()) / topics
            if name == "small":
                top = int(order[-1])
                worst.append((t, texts[top], float(pr[top]), float(gl[top])))
    kl = np.array([math.log(n) - (n - 1) / n for n in ns])
    out = {"ns": ns, "kl": kl, "examples": worst[:6]}
    for name in rms:
        out[f"{name}_proxy"], out[f"{name}_gold"] = res[name]["proxy"], res[name]["gold"]
    return out


# ---------------------------------------------------------------------------
# RLHF: policy gradient on the reward model, with a KL penalty to the fine-tuned model
# ---------------------------------------------------------------------------
def rlhf_run(beta, steps=240, batch=16, lr=2e-5, seed=0, snaps=(0, 40, 80, 160, 240)):
    torch.manual_seed(seed)
    ref = _load_model("sft")
    pol = copy.deepcopy(ref)
    rm = _load_rm("rm")
    opt = torch.optim.AdamW(pol.parameters(), lr=lr, weight_decay=0.0)
    hist, samples = [], []
    for step in range(steps + 1):
        t = TOPICS[step % len(TOPICS)]
        prompt = P.chat(line_q(t))
        pol.eval()
        outs = P.sample(pol, prompt, batch, 40, 1.0, seed=10_000 * seed + step)
        texts = [P.text_of(o) for o in outs]
        ex = [(prompt, o) for o in outs]
        with torch.no_grad():
            r = torch.from_numpy(rm_score(rm, t, texts)).float()
            lref = P.seq_logprob(ref, ex)
        pol.train()
        lpol = P.seq_logprob(pol, ex)
        kl = (lpol.detach() - lref)  # a sample of KL(pi || pi_ref), per answer
        total = r - beta * kl
        adv = total - total.mean()
        loss = -(adv * lpol).mean()
        if step < steps:
            opt.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(pol.parameters(), 1.0)
            opt.step()
        hist.append((step, float(r.mean()), float(np.mean([gold(x) for x in texts])), float(kl.mean())))
        if step in snaps:
            samples.append((step, t, texts[:3]))
    return np.array(hist), samples, pol


def compute_rlhf(betas=(0.1, 0.01), seeds=3):
    """Per beta: the mean history over seeds (step, reward model, gold, KL), every seed's, and seed 0's samples."""
    out = {"betas": list(betas), "seeds": seeds}
    for b in betas:
        key = f"b{b:g}".replace(".", "_")
        runs = []
        for sd in range(seeds):
            hist, samples, pol = rlhf_run(b, seed=sd)
            runs.append(hist)
            if sd == 0:
                out[key + "_samples"] = samples
                g, e, ex = line_eval(pol, 4, seed=5)
                out[key + "_final"] = {"gold": g, "ended": e, "examples": ex}
        out[key + "_seeds"] = np.stack(runs)
        out[key] = out[key + "_seeds"].mean(0)
    return out


# ---------------------------------------------------------------------------
# DPO (Rafailov et al. 2023): the same optimum, fitted straight from the comparisons
# ---------------------------------------------------------------------------
def compute_dpo(beta=0.1, steps=600, batch=16, lr=2e-5, seed=0):
    torch.manual_seed(seed)
    g = rng(seed)
    pr = load("prefs")
    pairs = pr["train"]
    w, l_ = _pair_examples(pairs)
    ref = _load_model("sft")
    pol = copy.deepcopy(ref)
    opt = torch.optim.AdamW(pol.parameters(), lr=lr, weight_decay=0.0)
    probe = list(range(32))  # fixed pairs whose log-probabilities are tracked
    with torch.no_grad():
        ref_w_all, ref_l_all = P.seq_logprob(ref, w), P.seq_logprob(ref, l_)
    hist, probe_hist = [], []
    for step in range(steps + 1):
        if step % 50 == 0:
            with torch.no_grad():
                pol.eval()
                pw = P.seq_logprob(pol, [w[i] for i in probe]) - ref_w_all[probe]
                pl = P.seq_logprob(pol, [l_[i] for i in probe]) - ref_l_all[probe]
            probe_hist.append((step, float(pw.mean()), float(pl.mean())))
        if step == steps:
            break
        pol.train()
        idx = g.integers(0, len(pairs), batch)
        lw = P.seq_logprob(pol, [w[i] for i in idx]) - ref_w_all[idx]
        ll = P.seq_logprob(pol, [l_[i] for i in idx]) - ref_l_all[idx]
        margin = beta * (lw - ll)
        loss = -F.logsigmoid(margin).mean()
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(pol.parameters(), 1.0)
        opt.step()
        hist.append((step, float(loss), float((margin > 0).float().mean())))
    pol.eval()
    gl, ended, ex = line_eval(pol, 4, seed=5)
    rm = _load_rm("rm")
    kls = []
    for k, t in enumerate(TOPICS[:10]):
        outs = P.sample(pol, P.chat(line_q(t)), 8, 40, 1.0, seed=900 + k)
        exs = [(P.chat(line_q(t)), o) for o in outs]
        with torch.no_grad():
            kls.append(float((P.seq_logprob(pol, exs) - P.seq_logprob(ref, exs)).mean()))
    return {"beta": beta, "hist": np.array(hist), "probe": np.array(probe_hist), "gold": gl, "ended": ended,
            "examples": ex, "kl": float(np.mean(kls))}


# ---------------------------------------------------------------------------
# Distillation, merging
# ---------------------------------------------------------------------------
def compute_distill(tokens=2_000_000, T=1.0):
    from explainer.lm import pocket

    train, valid = N.token_arrays()
    teacher = _base()
    cfg = pocket.Config(vocab=teacher.cfg.vocab, d=128, layers=2, heads=4, seq=256)
    out = {"student_params": int(sum(p.numel() for p in pocket.PocketGPT(cfg).parameters())),
           "teacher_params": int(sum(p.numel() for p in teacher.parameters())),
           "teacher_heldout": P.heldout_loss(teacher, valid)}
    for mode in ("text", "teacher"):
        torch.manual_seed(0)
        stu = pocket.PocketGPT(cfg)
        opt = torch.optim.AdamW(stu.parameters(), lr=3e-3, weight_decay=0.1)
        data = pocket.TokenStream(train, valid, cfg.seq, seed=1)
        steps = tokens // (16 * cfg.seq)
        curve = []
        for step in range(steps):
            for gr in opt.param_groups:
                gr["lr"] = 3e-3 * min(1, (step + 1) / 50) * 0.5 * (1 + math.cos(math.pi * step / steps))
            x, y = data.batch(16)
            logits = stu(x)
            if mode == "text":
                loss = F.cross_entropy(logits.flatten(0, 1), y.flatten())
            else:  # forward KL to the teacher's next-token distribution (Hinton et al. 2015)
                with torch.no_grad():
                    tp = F.softmax(teacher(x) / T, -1)
                loss = -(tp * F.log_softmax(logits / T, -1)).sum(-1).mean() * T * T
            opt.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(stu.parameters(), 1.0)
            opt.step()
            if (step + 1) % max(1, steps // 10) == 0:
                curve.append(((step + 1) * 16 * cfg.seq, P.heldout_loss(stu, valid, n=4)))
        out[mode] = {"curve": curve, "heldout": P.heldout_loss(stu, valid)}
    return out


def _vec(model):
    return {k: v.detach().clone() for k, v in model.state_dict().items()}


def compute_merge(lams=(0.0, 0.5, 1.0)):
    """Task arithmetic (Ilharco et al. 2023): fine-tune each task alone; tau = theta_task - theta_base; add them."""
    d = load("data")
    base = _base()
    tb = _vec(base)
    taus = {}
    for task in ("which", "line"):
        m = copy.deepcopy(base)
        P.sft(m, sft_examples(d, (task,)), SFT_STEPS, SFT_LR)
        taus[task] = {k: v - tb[k] for k, v in _vec(m).items()}

    def with_weights(ws):
        m = copy.deepcopy(base)
        m.load_state_dict({k: tb[k] + sum(w * taus[t][k] for t, w in ws.items()) for k in tb})
        return m.eval()

    rows = []
    for name, ws in (("which only", {"which": 1.0}), ("line only", {"line": 1.0})):
        m = with_weights(ws)
        g_, e_, _ = line_eval(m, 2)
        rows.append((name, which_accuracy(m, d, 200), g_, e_))
    for lam in lams:
        m = with_weights({"which": lam, "line": lam})
        g_, e_, _ = line_eval(m, 2)
        rows.append((f"sum x {lam:g}", which_accuracy(m, d, 200), g_, e_))
    # the straight path from one fine-tuned model to the other
    path = []
    for a in np.linspace(0, 1, 6):
        m = with_weights({"which": 1 - a, "line": a})
        path.append((float(a), which_accuracy(m, d, 100), line_eval(m, 1)[1]))
    sft = load("sft")
    return {"rows": rows, "path": path, "multitask_which": sft["sft_which"], "multitask_line": sft["sft_line_gold"]}


ITEMS = {
    "data": compute_data,
    "sft": compute_sft,
    "lora": compute_lora,
    "prefs": compute_prefs,
    "rm": compute_rm,
    "rlaif": compute_rlaif,
    "closed": compute_closed,
    "bon": compute_bon,
    "rlhf": compute_rlhf,
    "dpo": compute_dpo,
    "distill": compute_distill,
    "merge": compute_merge,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
