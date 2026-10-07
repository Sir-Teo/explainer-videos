"""Precompute every piece of real-model data used in the LLM video.

    python -m videos.llm.analyze                 # everything missing
    python -m videos.llm.analyze gpt2_small      # specific runs
    python -m videos.llm.analyze --force         # recompute

Results are cached in ``.cache/llm/<name>.json`` (+ ``.npz`` for arrays);
scenes call ``load(name)`` / ``load_arrays(name)`` and never run a model.

Runs:
    gpt2_small       probes of GPT-2 small: tokens, embeddings, attention heads,
                     logit lens, positions, MLP activations, losses (~1 min)
    gpt2_family      the same prompt through GPT-2 small/medium/large/XL, and
                     base-model completions (downloads ~9 GB of weights)
    tiny_shakespeare a 0.8M-parameter character-level GPT trained from scratch
                     on Tiny Shakespeare, with samples along the way (~25 min)
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.request
from pathlib import Path

import numpy as np

from explainer.tts import REPO_ROOT

DATA_DIR = REPO_ROOT / ".cache" / "llm"
SHAKESPEARE_URL = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"

# The running example: one prompt threaded through the whole video.
PROMPT = "The Eiffel Tower is located in the city of"
TARGET = " Paris"

BANK_RIVER = "We walked along the river bank"
BANK_RIVER_2 = "We sat by the river bank"
BANK_MONEY = "We deposited cash at the bank"
BANK_HEAD = (0, 7)  # a first-layer head that sends "bank"'s attention to "river"
PREV_HEAD = (4, 11)  # previous-token head (also identified by Wang et al. 2022, "Interpretability in the Wild")
INDUCTION_HEAD = (5, 5)  # induction head (likewise; head_scores() re-derives both from scratch)

REFERENCE_TEXT = (
    "The history of science is full of surprises. In the spring, farmers plant seeds and wait for rain. "
    "She opened the letter and read it twice before putting it down. Markets fell sharply on Monday after the report. "
    "The museum is open every day except holidays, and tickets can be bought online. He walked to the station, "
    "bought a coffee, and waited for the train to arrive. Scientists measured the temperature of the lake every hour. "
    "Our team finished the project ahead of schedule, which surprised everyone in the office."
)
WORD_GROUPS = {
    "numbers": [" one", " two", " three", " four", " five", " six", " seven"],
    "days": [" Monday", " Tuesday", " Wednesday", " Thursday", " Friday", " Saturday", " Sunday"],
    "countries": [" France", " Germany", " Japan", " China", " Italy", " Spain", " Canada"],
    "animals": [" cat", " dog", " horse", " cow", " pig", " sheep", " lion"],
    "colors": [" red", " blue", " green", " yellow", " purple", " orange", " pink"],
}
ANALOGY_WORDS = [" man", " woman", " king", " queen", " uncle", " aunt"]
SIMILAR_TO = (" cat", [" kitten", " dog", " horse", " car", " banana", " democracy"])
INDUCTION_WORDS = [" " + w for w in "tree river lamp seven orange piano cloud".split()]
RANDOM_WORDS = [" " + w for w in (
    "apple table river music green seven window dance cloud paper train honey silver forest pencil storm"
    " castle coffee ladder tiger engine candle bottle garden mirror rocket violin desert jacket pepper"
).split()]


# ---------------------------------------------------------------------------
def _gpt2_small() -> tuple[dict, dict]:
    from explainer.lm import bpe
    from explainer.lm import gpt2 as g

    tok, model = g.load()
    WE = model.transformer.wte.weight.numpy()
    out: dict = {}
    arrays: dict = {}

    # Hook: greedy continuation of the running example, with the top-8 at each step.
    out["hook"] = g.greedy(PROMPT, steps=4, k=8)

    # Tokens.
    out["tokenize"] = {}
    for s in [PROMPT + TARGET + ".", "Tokenization splits unbelievable words like ChatGPT into pieces."]:
        ids, pieces = g.tokenize(s)
        out["tokenize"][s] = {"ids": ids, "pieces": pieces}
    out["vocab_size"] = int(WE.shape[0])
    out["vocab_samples"] = {str(i): g.decode(i) for i in [0, 1, 2, 262, 464, 6342, 50255, 50256]}
    phrase = "The Eiffel Tower"
    out["granularity"] = {"chars": list(phrase), "words": ["The", " Eiffel", " Tower"],
                          "subwords": g.tokenize(phrase)[1]}
    out["bpe"] = bpe.train({"low": 7, "lower": 4, "lowest": 3, "slow": 5, "slower": 2, "tower": 6, "towers": 3}, 6)

    # Embeddings.
    out["d_model"] = int(WE.shape[1])
    out["paris_vector"] = [float(v) for v in WE[g.single_id(TARGET)][:8]]
    words = [w for ws in WORD_GROUPS.values() for w in ws]
    X = np.stack([WE[g.single_id(w)] for w in words])
    Xc = X - X.mean(0)
    _, _, Vt = np.linalg.svd(Xc, full_matrices=False)
    xy = Xc @ Vt[:2].T
    out["groups"] = {"words": words, "labels": [k for k, ws in WORD_GROUPS.items() for _ in ws], "xy": xy.tolist()}

    vec = {w: WE[g.single_id(w)] for w in ANALOGY_WORDS}
    gdir = np.mean([vec[" woman"] - vec[" man"], vec[" queen"] - vec[" king"], vec[" aunt"] - vec[" uncle"]], axis=0)
    gdir /= np.linalg.norm(gdir)
    rdir = np.mean([vec[" king"] - vec[" man"], vec[" queen"] - vec[" woman"]], axis=0)
    rdir -= (rdir @ gdir) * gdir
    rdir /= np.linalg.norm(rdir)
    origin = vec[" man"]
    vec["result"] = vec[" king"] - vec[" man"] + vec[" woman"]
    out["analogy_plane"] = {w: [float((v - origin) @ gdir), float((v - origin) @ rdir)] for w, v in vec.items()}

    E = WE / np.linalg.norm(WE, axis=1, keepdims=True)

    def nearest(a, b, c, k=5):
        v = WE[g.single_id(b)] - WE[g.single_id(a)] + WE[g.single_id(c)]
        s = E @ (v / np.linalg.norm(v))
        for w in (a, b, c):
            s[g.single_id(w)] = -np.inf
        idx = np.argsort(-s)[:k]
        return [(g.decode(i), float(s[i])) for i in idx]

    res = vec["result"] / np.linalg.norm(vec["result"])
    out["analogy_including_inputs"] = [(g.decode(i), float((E @ res)[i])) for i in np.argsort(-(E @ res))[:3]]
    out["analogies"] = {
        "king": nearest(" man", " woman", " king"),
        "tokyo": nearest(" France", " Paris", " Japan"),
        "dogs": nearest(" cat", " cats", " dog"),
    }
    base, others = SIMILAR_TO
    out["similarity"] = {"word": base, "others": others,
                         "cos": [float(E[g.single_id(base)] @ E[g.single_id(o)]) for o in others]}

    # Context: the same token " bank" drifting apart through the layers.
    # Cosine similarity after subtracting each layer's mean residual vector (measured on a reference paragraph,
    # skipping position 0): GPT-2's residual stream has a few huge shared dimensions that otherwise dominate
    # every cosine (Ethayarajh 2019; Timkey & van Schijndel 2021).
    mu = g.residual_stream(g.tokenize(REFERENCE_TEXT)[0])[:, 1:].mean(axis=1)
    res = {s: g.residual_stream(g.tokenize(s)[0])[:, -1] - mu for s in (BANK_RIVER, BANK_RIVER_2, BANK_MONEY)}

    def cos_layers(a, b):
        return [float(x @ y / np.linalg.norm(x) / np.linalg.norm(y)) for x, y in zip(res[a], res[b])]

    out["bank"] = {"different": cos_layers(BANK_RIVER, BANK_MONEY), "same": cos_layers(BANK_RIVER, BANK_RIVER_2),
                   "sentences": [BANK_RIVER, BANK_RIVER_2, BANK_MONEY]}

    # Attention: a real head where " bank" looks at " river".
    ids, pieces = g.tokenize(BANK_RIVER)
    L, H = BANK_HEAD
    out["bank_head"] = {"layer": L, "head": H, "pieces": pieces, "pattern": g.attention(ids, L, H).tolist(),
                        "scores": g.qk_scores(ids, L, H).tolist()}

    # Previous-token and induction heads.
    ids, pieces = g.tokenize(PROMPT + TARGET + ".")
    L, H = PREV_HEAD
    out["prev_head"] = {"layer": L, "head": H, "pieces": pieces, "pattern": g.attention(ids, L, H).tolist()}
    ind_ids = [g.single_id(w) for w in INDUCTION_WORDS]
    ids = ind_ids + ind_ids
    L, H = INDUCTION_HEAD
    out["induction_head"] = {"layer": L, "head": H, "pieces": [g.decode(i) for i in ids],
                             "pattern": g.attention(ids, L, H).tolist()}
    prev, ind = g.head_scores(ids, len(ind_ids))
    out["head_scores"] = {"prev": prev.tolist(), "induction": ind.tolist()}
    att = g.forward(ids).attentions
    first_head = [float(att[L2][0, H2, 4:, 0].mean()) for L2 in range(12) for H2 in range(12)]
    out["first_token_heads"] = {"mean_attention_to_first": first_head}

    ids, pieces = g.tokenize(PROMPT + TARGET + ".")
    att = g.forward(ids).attentions
    to_first = np.array([[float(att[L2][0, H2, 3:, 0].mean()) for H2 in range(12)] for L2 in range(12)])
    L, H = np.unravel_index(np.argmax(to_first), to_first.shape)
    out["sink_head"] = {"layer": int(L), "head": int(H), "pieces": pieces, "pattern": att[L][0, H].tolist(),
                        "frac_heads_mostly_first": float((to_first > 0.5).mean())}
    out["layer5_heads"] = {"pieces": pieces, "patterns": att[5][0].tolist()}

    rng = np.random.default_rng(0)
    seq = [RANDOM_WORDS[i] for i in rng.permutation(len(RANDOM_WORDS))[:20]]
    ids = [g.single_id(w) for w in seq] * 2
    out["induction_loss"] = {"words": seq, "losses": g.token_losses(ids)}

    # Positions.
    P = model.transformer.wpe.weight.numpy()
    Pc = P - P.mean(0)
    _, S, Vt = np.linalg.svd(Pc, full_matrices=False)
    arrays["pos_pca"] = (Pc @ Vt[:3].T).astype(np.float32)
    # Heat map: every 4th position, the 64 dimensions that vary most across positions (mean removed),
    # ordered by their dominant frequency and phase so the waves line up visually.
    dims = np.argsort(-Pc.var(0))[:64]
    H = Pc[:, dims]
    F = np.fft.rfft(H, axis=0)
    k = np.argmax(np.abs(F[1:40]), axis=0) + 1
    order = np.lexsort((np.angle(F[k, np.arange(len(k))]), k))
    arrays["pos_heat"] = H[:, order][::4].astype(np.float32)
    out["pos_pca_var"] = (S[:3] ** 2 / (S**2).sum()).tolist()

    # MLP neuron activations at the last position of the running example.
    acts = np.stack([g.mlp_activations(PROMPT, L)[-1] for L in range(12)])
    arrays["mlp_acts"] = acts.astype(np.float32)
    out["mlp_frac_active"] = [float((a > 0.5).mean()) for a in acts]

    # Output: final distribution, logit lens, temperature, per-token losses.
    out["final"] = g.next_token(PROMPT, k=10)
    out["logit_lens"] = g.logit_lens(PROMPT, TARGET, k=3)
    ids, _ = g.tokenize("Once upon a time, there was a")
    arrays["temp_logits"] = g.forward(ids).logits[0, -1].numpy().astype(np.float32)
    out["temp_prompt"] = "Once upon a time, there was a"
    order = np.argsort(-arrays["temp_logits"])[:40]
    out["temp_tokens"] = {"ids": order.tolist(), "pieces": [g.decode(i) for i in order]}
    out["sampling"] = {
        "greedy": g.sample(out["temp_prompt"], 30, 0),
        "samples": {str(T): g.sample(out["temp_prompt"], 28, T, seed=3) for T in (0.7, 1.0, 1.6)},
    }
    ids, pieces = g.tokenize(PROMPT + TARGET + ".")
    out["token_losses"] = {"pieces": pieces, "losses": g.token_losses(ids)}

    out["params"] = g.param_breakdown()
    return out, arrays


def _gpt2_family() -> tuple[dict, dict]:
    from explainer.lm import gpt2 as g

    out = {"paris": {}, "completions": {}}
    prompts = ["What is the capital of France?", "Write a short poem about the ocean."]
    for name in ["gpt2", "gpt2-medium", "gpt2-large", "gpt2-xl"]:
        _, model = g.load(name)
        out["paris"][name] = {"params": int(sum(p.numel() for p in model.parameters())), **g.next_token(PROMPT, 5, name)}
        if name == "gpt2-xl":
            out["completions"] = {p: g.generate(p, 40, name) for p in prompts}
        g.load.cache_clear()
    return out, {}


def _tiny_shakespeare() -> tuple[dict, dict]:
    import torch

    from explainer.lm.tiny_gpt import train

    src = DATA_DIR / "tinyshakespeare.txt"
    if not src.exists():
        urllib.request.urlretrieve(SHAKESPEARE_URL, src)
    torch.set_num_threads(4)
    out = train(src.read_text(), steps=4000, batch=32, lr=2e-3, sample_at=(0, 100, 300, 1000, 2000, 4000),
                sample_len=300, d=128, n_layer=4, n_head=4, ctx=128)
    return out, {}


RUNS = {"gpt2_small": _gpt2_small, "gpt2_family": _gpt2_family, "tiny_shakespeare": _tiny_shakespeare}


# ---------------------------------------------------------------------------
def path(name: str) -> Path:
    return DATA_DIR / f"{name}.json"


_loaded: dict[str, dict] = {}


def load(name: str) -> dict:
    if name not in _loaded:
        p = path(name)
        if not p.exists():
            raise FileNotFoundError(f"Missing analysis '{name}'. Run: python -m videos.llm.analyze {name}")
        _loaded[name] = json.loads(p.read_text())
    return _loaded[name]


def load_arrays(name: str) -> dict:
    with np.load(path(name).with_suffix(".npz")) as data:
        return {k: data[k] for k in data.files}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("names", nargs="*", default=list(RUNS))
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for name in args.names:
        if path(name).exists() and not args.force:
            print(f"[skip] {name} (cached)")
            continue
        t = time.time()
        print(f"[run ] {name} ...", flush=True)
        data, arrays = RUNS[name]()
        if arrays:
            tmp = path(name).with_suffix(".tmp.npz")
            np.savez(tmp, **arrays)
            tmp.replace(path(name).with_suffix(".npz"))
        tmp = path(name).with_suffix(".tmp.json")
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1))
        tmp.replace(path(name))
        print(f"[done] {name} in {time.time() - t:.0f}s", flush=True)


if __name__ == "__main__":
    main()
