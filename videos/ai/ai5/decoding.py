"""Decoding the series' novels model, judged by GPT-2 (the ``decoding`` item of Part 5's compute).

The generator is the series' own small language model (``explainer.ai.novels``, trained on Part 1's thirty novels).
Twelve prompts of 32 tokens are cut from its held-out text; each decoding setting writes eight continuations of 40
tokens per prompt.  Three numbers per setting:

* quality: how likely another, larger model finds the continuation (GPT-2 small's negative log-likelihood of the
  continuation given the prompt, in nats per character: the judge never saw how it was written);
* diversity: of the eight continuations of a prompt, the share of their token pairs (bigrams) that are distinct;
* repetition: within one continuation, the share of its 4-grams that repeat an earlier one.

The real continuations of the prompts (the novels' own next 40 tokens) are judged the same way: the human reference.
Each setting is saved as it finishes (``CACHE.partial``), so a killed run resumes.
"""

from __future__ import annotations

import math

import numpy as np

PROMPTS, SAMPLES, PROMPT_LEN, GEN_LEN = 12, 8, 32, 40
SETTINGS = (
    [("greedy", 0.0)]
    + [("temp", t) for t in (0.5, 0.7, 1.0, 1.3)]
    + [("topk", k) for k in (5, 20, 100)]
    + [("topp", p) for p in (0.5, 0.8, 0.9, 0.95)]
    + [("minp", m) for m in (0.02, 0.05, 0.1, 0.2)]
)


def gpt2():
    """GPT-2 small from the local Hugging Face cache (downloaded once if it isn't there)."""
    from transformers import AutoModelForCausalLM, AutoTokenizer

    for local in (True, False):
        try:
            tok = AutoTokenizer.from_pretrained("openai-community/gpt2", local_files_only=local)
            model = AutoModelForCausalLM.from_pretrained("openai-community/gpt2", local_files_only=local)
            return tok, model.eval()
        except OSError:
            if not local:
                raise
    raise RuntimeError


def filter_probs(p, kind: str, v: float):
    """The distribution actually sampled from: p (rows) after temperature, top-k, top-p (nucleus) or min-p."""
    import torch

    if kind == "topk":
        kth = torch.topk(p, int(v), dim=-1).values[..., -1:]
        q = torch.where(p >= kth, p, torch.zeros_like(p))
    elif kind == "topp":
        s, i = torch.sort(p, dim=-1, descending=True)
        c = torch.cumsum(s, -1)
        keep = (c - s) < v  # keep a token while the mass before it is below p (so at least one is kept)
        q = torch.zeros_like(p).scatter(-1, i, s * keep)
    elif kind == "minp":
        q = torch.where(p >= v * p.max(-1, keepdim=True).values, p, torch.zeros_like(p))
    else:
        q = p
    return q / q.sum(-1, keepdim=True)


def prompts(valid: np.ndarray, seed: int = 2020):
    """Twelve 32-token prompts from the held-out text, each starting after a line break, with the real next 40."""
    from explainer.ai import novels

    g = np.random.Generator(np.random.PCG64(seed))
    nl = [i for i in range(novels.tokenizer().get_vocab_size()) if "\n" in novels.decode([i])]
    is_nl = np.isin(valid, nl)
    out, used = [], set()
    while len(out) < PROMPTS:
        s = int(g.integers(0, len(valid) - 200))
        nxt = np.nonzero(is_nl[s:s + 400])[0]
        if not len(nxt):
            continue
        a = s + int(nxt[0]) + 1
        seg = valid[a:a + PROMPT_LEN + GEN_LEN]
        if a in used or np.isin(seg, nl).sum() > 2 or (seg == novels.special("<|endoftext|>")).any():
            continue
        used.add(a)
        out.append(seg.astype(np.int64))
    return np.stack(out)


def generate(model, ids, kind: str, v: float, seed: int):
    """Continue each row of ids by GEN_LEN tokens; also the number of tokens each step could have chosen from."""
    import torch

    g = torch.Generator().manual_seed(seed)
    x = torch.tensor(ids)
    kept = []
    with torch.no_grad():
        for _ in range(GEN_LEN):
            z = model(x[:, -model.cfg.seq:])[:, -1].double()
            if kind == "greedy":
                nxt = z.argmax(-1, keepdim=True)
                kept.append(np.ones(len(x)))
            else:
                T = v if kind == "temp" else 1.0
                p = torch.softmax(z / T, -1)
                q = filter_probs(p, kind, v)
                kept.append((q > 0).sum(-1).numpy().astype(float))
                nxt = torch.multinomial(q.float(), 1, generator=g)
            x = torch.cat([x, nxt], 1)
    return x[:, ids.shape[1]:].numpy(), float(np.mean(kept))


def judge(tok, model, prompt_texts, cont_texts):
    """GPT-2's negative log-likelihood of each continuation given its prompt: (nats, characters)."""
    import torch

    out = []
    with torch.no_grad():
        for a, b in zip(prompt_texts, cont_texts):
            pa = tok(a)["input_ids"]
            full = tok(a + b)["input_ids"][:1024]
            k = len(pa)
            while k > 0 and full[:k] != pa[:k]:  # the boundary, if the tokenizer merged across it
                k -= 1
            x = torch.tensor([full])
            lp = torch.log_softmax(model(x).logits[0, :-1].double(), -1)
            tgt = x[0, 1:]
            nll = -lp[torch.arange(len(tgt)), tgt][k - 1:].sum().item()
            out.append((nll, len(tok.decode(full[k:]))))
    return out


def distinct2(rows) -> float:
    pairs = [(int(a), int(b)) for r in rows for a, b in zip(r[:-1], r[1:])]
    return len(set(pairs)) / max(len(pairs), 1)


def rep4(r) -> float:
    grams = [tuple(int(t) for t in r[i:i + 4]) for i in range(len(r) - 3)]
    seen, rep = set(), 0
    for gm in grams:
        rep += gm in seen
        seen.add(gm)
    return rep / max(len(grams), 1)


def compute(cache) -> dict:
    import torch

    from explainer.ai import novels

    torch.set_grad_enabled(False)
    model = novels.load_base()
    _, valid = novels.token_arrays()
    P = prompts(valid)
    ptexts = [novels.decode(p[:PROMPT_LEN]) for p in P]
    tok, judge_model = gpt2()
    part = cache.partial("decoding", dict(settings=SETTINGS, prompts=PROMPTS, samples=SAMPLES, gen=GEN_LEN, v=2))
    if "human" not in part:
        human = [novels.decode(p[PROMPT_LEN:]) for p in P]
        j = judge(tok, judge_model, ptexts, human)
        part["human"] = dict(nll=sum(a for a, _ in j) / sum(c for _, c in j), rep=float(np.mean(
            [rep4(p[PROMPT_LEN:]) for p in P])), text=human[0])
    for si, (kind, v) in enumerate(SETTINGS):
        key = f"{kind}{v}"
        if key in part:
            continue
        n_s = 1 if kind == "greedy" else SAMPLES
        ids = np.repeat(P[:, :PROMPT_LEN], n_s, 0)
        cont, kept = generate(model, ids, kind, v, seed=100 + si)
        texts = [novels.decode(c) for c in cont]
        j = judge(tok, judge_model, [ptexts[i // n_s] for i in range(len(cont))], texts)
        per_prompt = [cont[i * n_s:(i + 1) * n_s] for i in range(PROMPTS)]
        nll_p = [sum(a for a, _ in j[i * n_s:(i + 1) * n_s]) / sum(c for _, c in j[i * n_s:(i + 1) * n_s])
                 for i in range(PROMPTS)]
        part[key] = dict(nll=sum(a for a, _ in j) / sum(c for _, c in j), nll_prompt=nll_p,
                         div=float(np.mean([distinct2(r) for r in per_prompt])) if n_s > 1 else None,
                         rep=float(np.mean([rep4(c) for c in cont])), kept=kept, examples=texts[:2] if n_s > 1 else
                         texts[:1], ex_prompt=[t for t in texts[n_s * 3:n_s * 3 + 2]])
        print(f"    {key}: nll {part[key]['nll']:.3f} nats/char, distinct-2 {part[key]['div']}, "
              f"rep-4 {part[key]['rep']:.3f}, kept {kept:.1f}", flush=True)
    # the same prompts' novels-model next-token distribution after the first prompt, for the picture
    z = model(torch.tensor(P[:1, :PROMPT_LEN]))[0, -1].double()
    p0 = torch.softmax(z, -1).numpy()
    top = np.argsort(-p0)[:60]
    out = dict(settings=[f"{k}{v}" for k, v in SETTINGS], kinds=[k for k, _ in SETTINGS], values=[v for _, v in SETTINGS],
               prompt0=ptexts[0], prompt3=ptexts[3], human=part["human"], next_p=p0[top], next_tok=[novels.decode([int(i)])
                                                                                                 for i in top])
    for kind, v in SETTINGS:
        out[f"{kind}{v}"] = part[f"{kind}{v}"]
    return out
