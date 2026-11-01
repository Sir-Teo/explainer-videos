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
from pathlib import Path

from . import decoding_contract as contract

import numpy as np

PROMPTS, SAMPLES, PROMPT_LEN, GEN_LEN = 12, 8, 32, 40
SETTINGS = (
    [("greedy", 0.0)]
    + [("temp", t) for t in (0.5, 0.7, 1.0, 1.3)]
    + [("topk", k) for k in (5, 20, 100)]
    + [("topp", p) for p in (0.5, 0.8, 0.9, 0.95)]
    + [("minp", m) for m in (0.02, 0.05, 0.1, 0.2)]
)


def configuration():
    return dict(settings=SETTINGS, prompts=PROMPTS, samples=SAMPLES, prompt_len=PROMPT_LEN, gen_len=GEN_LEN,
                prompt_seed=2020, generation_seed_base=100, greedy_samples=1)


def cache_identity(repo_root=None, hub_dir=None):
    """Pure pre-model API used by the Part 5 cache recipe."""
    root = Path(repo_root) if repo_root is not None else Path(__file__).resolve().parents[3]
    return contract.cache_identity(root, configuration(), hub_dir)


def gpt2():
    """The reviewed GPT-2 snapshot, strictly local; missing files never download."""
    path = contract.snapshot_dir()
    for name in contract.GPT2_FILES:
        contract.file_identity(path / name)
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(str(path), local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(str(path), local_files_only=True)
    return tok, model.eval()


def filter_probs(p, kind: str, v: float):
    """The distribution actually sampled from: p (rows) after temperature, top-k, top-p (nucleus) or min-p."""
    import torch

    if kind == "topk":
        values, indices = torch.topk(p, int(v), dim=-1)
        q = torch.zeros_like(p).scatter(-1, indices, values)
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


def prompts(valid: np.ndarray, tokenizer, seed: int = 2020):
    """Deterministically select admissible held-out segments; fail if insufficient."""
    if valid.ndim != 1 or len(valid) < PROMPT_LEN + GEN_LEN:
        raise ValueError("Held-out token array is too short for a prompt and continuation")
    nl = [i for i in range(tokenizer.get_vocab_size()) if "\n" in tokenizer.decode([i], skip_special_tokens=False)]
    eot = tokenizer.token_to_id("<|endoftext|>")
    if not nl or eot is None:
        raise ValueError("Novels tokenizer needs newline tokens and <|endoftext|>")
    is_nl = np.isin(valid, nl)
    starts = np.flatnonzero(is_nl) + 1
    starts = starts[starts + PROMPT_LEN + GEN_LEN <= len(valid)]
    g = np.random.Generator(np.random.PCG64(seed))
    out = []
    for a in g.permutation(starts):
        seg = valid[a:a + PROMPT_LEN + GEN_LEN]
        if np.isin(seg, nl).sum() > 2 or (seg == eot).any():
            continue
        out.append(seg.astype(np.int64))
        if len(out) == PROMPTS:
            return np.stack(out)
    raise ValueError(f"Only {len(out)} admissible held-out prompts; need {PROMPTS}")


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
    """Boundary-preserving conditional NLL and true continuation character count.

    v3 encodes the two strings separately, avoiding a BPE token that crosses the
    boundary and charges prompt characters to the continuation. No text is
    silently truncated; empty or over-context examples fail explicitly.
    """
    import torch

    if len(prompt_texts) != len(cont_texts):
        raise ValueError("Prompt and continuation cohorts differ")
    limit = getattr(model.config, "max_position_embeddings", None) or getattr(model.config, "n_positions", 1024)
    out = []
    with torch.no_grad():
        for a, b in zip(prompt_texts, cont_texts):
            pa = tok(a, add_special_tokens=False)["input_ids"]
            cb = tok(b, add_special_tokens=False)["input_ids"]
            if not pa or not cb or not b:
                raise ValueError("Judge needs nonempty prompt and continuation text/tokens")
            if len(pa) + len(cb) > limit:
                raise ValueError(f"Judge context exceeds {limit} tokens; no continuation was truncated")
            x = torch.tensor([pa + cb])
            logits = model(x).logits[0, len(pa)-1:-1].double()
            lp = torch.log_softmax(logits, -1)
            nll = -lp[torch.arange(len(cb)), torch.tensor(cb)].sum().item()
            if not math.isfinite(nll):
                raise ValueError("Nonfinite judge NLL")
            out.append((nll, len(b)))
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
    from explainer.cache_lock import cache_lock
    with cache_lock(cache.path("decoding")):
        return _compute(cache)


def _compute(cache) -> dict:
    import torch

    from tokenizers import Tokenizer
    from explainer.lm import pocket

    identity = cache_identity()  # fail before tokenizer/model construction; no implicit upstream producers
    root = Path(__file__).resolve().parents[3]
    tokenizer = Tokenizer.from_file(str(root / ".cache/novels/tokenizer.json"))
    decode = lambda ids: tokenizer.decode([int(i) for i in ids], skip_special_tokens=False)
    valid = np.load(root / ".cache/novels/valid.npy", allow_pickle=False)
    if valid.ndim != 1 or valid.dtype != np.uint16 or (valid.size and valid.max() >= tokenizer.get_vocab_size()):
        raise ValueError("Held-out novels array has invalid shape, dtype or token IDs")
    P = prompts(valid, tokenizer)
    ptexts = [decode(p[:PROMPT_LEN]) for p in P]
    identity["selected_prompts_sha256"] = contract.prompt_identity(P, ptexts)
    part = contract.checked_partial(cache, identity, [f"{k}{v}" for k, v in SETTINGS], PROMPTS)
    ck = torch.load(root / ".cache/novels/base.pt", map_location="cpu", weights_only=True)
    model = pocket.PocketGPT(pocket.Config(**ck["config"]))
    model.load_state_dict(ck["model"])
    model.eval()
    tok, judge_model = gpt2()
    if "human" not in part:
        human = [decode(p[PROMPT_LEN:]) for p in P]
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
        texts = [decode(c) for c in cont]
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
    with torch.no_grad():
        z = model(torch.tensor(P[:1, :PROMPT_LEN]))[0, -1].double()
        p0 = torch.softmax(z, -1).numpy()
    top = np.argsort(-p0)[:60]
    out = dict(provenance=identity, metric_version=contract.METRIC_VERSION, prompt_count=PROMPTS, stochastic_samples=SAMPLES, greedy_samples=1, settings=[f"{k}{v}" for k, v in SETTINGS], kinds=[k for k, _ in SETTINGS], values=[v for _, v in SETTINGS],
               prompt0=ptexts[0], prompt3=ptexts[3], human=part["human"], next_p=p0[top], next_tok=[decode([int(i)])
                                                                                                 for i in top])
    for kind, v in SETTINGS:
        out[f"{kind}{v}"] = part[f"{kind}{v}"]
    final_identity = cache_identity()
    if any(identity[k] != final_identity[k] for k in final_identity):
        raise RuntimeError("Decoding inputs changed during computation; result not published")
    return out
