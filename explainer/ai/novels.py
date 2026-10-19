"""The series' own language model: a small modern transformer trained on Part 1's thirty novels.

    python -m explainer.ai.novels                 # build the tokenizer and train the base model (cached)
    python -m explainer.ai.novels --check         # a few sampled continuations from the cached model

    from explainer.ai.novels import encode, decode, load_base, generate

Parts 18 (pretraining), 19 (inference), 27 (post-training) and 30 (inside the model) start from this one model, so
"our model" means the same thing wherever it appears.  The text is Part 1's reading (``videos/ai/ai1/compute.py``:
thirty Project Gutenberg novels, 5% of the paragraphs held out); the tokenizer is a byte-level BPE with a 4,096-token
vocabulary learned from it, plus the chat markers post-training uses; the network is ``explainer.lm.pocket``'s
PocketGPT (RMSNorm, rotary positions, SwiGLU), trained with AdamW and a cosine schedule.

Everything lands in ``.cache/novels/``: ``tokenizer.json``, ``train.npy`` / ``valid.npy`` (token ids), ``base.pt``
(weights and config) and ``base.json`` (the training curve and settings).
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from functools import lru_cache

import numpy as np

from explainer.tts import REPO_ROOT

OUT = REPO_ROOT / ".cache" / "novels"
VOCAB = 4096
SPECIAL = ["<|endoftext|>", "<|user|>", "<|assistant|>", "<|end|>"]  # chat markers: Part 27's templates
BASE = dict(d=256, layers=6, heads=8, seq=256)  # about 6 million parameters
BASE_RUN = dict(lr=3e-3, batch=32, tokens=24_000_000, warmup=200, schedule="cosine", seed=0)


def _texts() -> tuple[str, str]:
    """Part 1's training and held-out text (built by its compute step if missing)."""
    d = REPO_ROOT / ".cache" / "ai1"
    if not (d / "train.txt").exists():
        from videos.ai.ai1 import compute as ai1

        ai1._save("corpus", ai1.compute_corpus())
    return (d / "train.txt").read_text(), (d / "valid.txt").read_text()


@lru_cache(maxsize=None)
def tokenizer():
    from tokenizers import Tokenizer, decoders, models, pre_tokenizers, trainers

    path = OUT / "tokenizer.json"
    if path.exists():
        return Tokenizer.from_file(str(path))
    OUT.mkdir(parents=True, exist_ok=True)
    tok = Tokenizer(models.BPE())
    tok.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)
    tok.decoder = decoders.ByteLevel()
    trainer = trainers.BpeTrainer(vocab_size=VOCAB, special_tokens=SPECIAL, min_frequency=2,
                                  initial_alphabet=pre_tokenizers.ByteLevel.alphabet())
    train, _ = _texts()
    tok.train_from_iterator(train.split("\n"), trainer)
    tok.save(str(path))
    return tok


def encode(text: str) -> list[int]:
    return tokenizer().encode(text).ids


def decode(ids) -> str:
    return tokenizer().decode([int(i) for i in ids], skip_special_tokens=False)


def special(name: str) -> int:
    return tokenizer().token_to_id(name)


def token_arrays() -> tuple[np.ndarray, np.ndarray]:
    """The training and held-out text as token ids (uint16), books separated by <|endoftext|>."""
    tp, vp = OUT / "train.npy", OUT / "valid.npy"
    if not tp.exists():
        train, valid = _texts()
        eot = special("<|endoftext|>")
        for text, p in ((train, tp), (valid, vp)):
            ids = []
            for block in text.split("\n"):
                ids.extend(encode(block + "\n"))
            np.save(p, np.asarray(ids + [eot], np.uint16))
    return np.load(tp), np.load(vp)


def train_base(threads: int = 4, verbose: bool = True) -> dict:
    import torch

    from explainer.lm import pocket

    train, valid = token_arrays()
    cfg = pocket.Config(vocab=tokenizer().get_vocab_size(), **BASE)
    run = pocket.Run(model=cfg, **BASE_RUN)
    data = pocket.TokenStream(train, valid, cfg.seq, seed=0)
    res = pocket.train(run, data, threads=threads, verbose=verbose)
    model = res.pop("_model")
    res.pop("_opts")
    torch.save({"config": asdict(cfg), "model": model.state_dict()}, OUT / "base.pt")
    res["train_tokens"], res["valid_tokens"] = int(len(train)), int(len(valid))
    (OUT / "base.json").write_text(json.dumps(res, indent=1, default=float))
    return res


def load_base():
    """The trained base model, in eval mode (trains it first if it isn't cached)."""
    import torch

    from explainer.lm import pocket

    if not (OUT / "base.pt").exists():
        train_base()
    ck = torch.load(OUT / "base.pt")
    model = pocket.PocketGPT(pocket.Config(**ck["config"]))
    model.load_state_dict(ck["model"])
    return model.eval()


def generate(model, prompt: str | list[int], n: int = 60, temperature: float = 0.8, top_k: int = 0, seed: int = 0,
             stop: str | None = None) -> str:
    """Sample a continuation of ``prompt`` (text or token ids); stops early at the token ``stop`` if given."""
    import torch

    ids = encode(prompt) if isinstance(prompt, str) else list(prompt)
    start = len(ids)
    g = torch.Generator().manual_seed(seed)
    stop_id = special(stop) if stop else None
    with torch.no_grad():
        for _ in range(n):
            logits = model(torch.tensor([ids[-model.cfg.seq:]]))[0, -1] / max(temperature, 1e-6)
            if top_k:
                v, _ = logits.topk(top_k)
                logits[logits < v[-1]] = -float("inf")
            nxt = int(torch.multinomial(logits.softmax(-1), 1, generator=g))
            ids.append(nxt)
            if nxt == stop_id:
                break
    return decode(ids[start:])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--threads", type=int, default=4)
    args = ap.parse_args()
    if not args.check:
        train, valid = token_arrays()
        print(f"tokens: {len(train):,} train, {len(valid):,} held out; vocabulary {tokenizer().get_vocab_size()}")
        if not (OUT / "base.pt").exists():
            train_base(args.threads)
    m = load_base()
    for k, p in enumerate(["It was a dark and stormy night", "\"My dear Watson,\" said", "The sea"]):
        print(repr(p + generate(m, p, 40, seed=k)))


if __name__ == "__main__":
    main()
