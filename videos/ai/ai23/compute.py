"""Precompute everything numerical in Part 23 of the AI series ("Every Sense Is a Token").

    python -m videos.ai.ai23.compute                 # everything missing (Part 1's novels, Part 21's letters)
    python -m videos.ai.ai23.compute --force clip
    AI23_SCALE=0.05 python -m videos.ai.ai23.compute # a smoke test of every code path (into .cache/ai23_quick/)

Results are cached in ``.cache/ai23/<name>.json`` (+ ``.npz``); synthesized speech in ``.cache/ai23/speech/``
(about 20 MB), a few checkpoints in ``.cache/ai23/models/``.  Every model here is trained on the CPU, seeded, one or
two torch threads (``AI23_THREADS``, default 1).  Items made of several runs save each run as it finishes
(``CACHE.partial``), and the long runs checkpoint as they go, so a killed computation resumes where it stopped.  About
two and a half hours on a busy 4-core machine, all told.

Text (text.py)
    bpe        byte-pair encoding learned on two million characters of the novels: the merges and how much each one
               shortens the text; one sentence at 0, 500, 2,000 and 8,000 merges; characters per token; WordPiece's
               first merges for contrast; the series' own model's tokenizer (explainer.ai.novels) on the passage
    unigram    Kudo's unigram language model on the same text: EM and pruning replayed, segmentations, samples
    lms        a small transformer per tokenizer (bytes; BPE and unigram at 1,024 and 4,096 pieces), each spending the
               same FLOPs, three seeds: bits per character on the scoreboard's passage, curves against compute
    patches    entropy patching (BLT) driven by the byte model: patch lengths, and where the surprise falls
Pictures (vq.py)
    codebooks  k-means codebooks of 4 x 4 patches of letters; residual stages against one codebook at equal bits
    vqtrain    a VQ autoencoder five ways (VQ, EMA, EMA + restarts, FSQ, LFQ), 256 codes, three seeds: usage,
               perplexity and error through training
Sound (audio.py)
    speech     Kokoro-82M saying digits, digit strings and sentences in twelve voices (two held out)
    nyquist    tones sampled at 8 kHz and their aliases; speech decimated with and without a filter
    mel        the STFT, the mel filters, and Whisper's log-mel front end (checked against transformers)
    audrey     1952-style templates from one voice, then dynamic time warping: the speaker problem measured
    codec      a small neural codec with residual VQ and quantizer dropout, two seeds: quality and Whisper's word error
               rate at 0.4 to 3.2 kbps
    ctc        a CTC recognizer for digit strings, three seeds: its training replayed and its forward lattice
    whisper    Whisper base.en on the held-out voices: input, tokens, transcripts, errors
    narrator   the narrator's own 12.5 Hz codes (Qwen3-TTS's speech tokenizer, through .venv-tts); empty without it
Pictures and words (clip.py)
    clip       CLIP's and SigLIP's losses at batch sizes 16, 64 and 256, three seeds each, equal pairs: zero-shot
               retrieval, the InfoNCE bound, resolution
    vlm        Qwen2-VL's dynamic-resolution token counts and M-RoPE position ids (the published rules)
"""

from __future__ import annotations

import json
import math
import os
import subprocess
import time
from pathlib import Path

import numpy as np

from explainer.ai.cache import Cache
from videos.ai.ai23 import audio, clip, text, vq

SCALE = text.SCALE
CACHE = Cache("ai23")
if SCALE != 1.0:  # a quick smoke test of every code path: its own cache, never the real one
    CACHE.dir = CACHE.dir.parent / "ai23_quick"
load = CACHE.load
MODELS = CACHE.dir / "models"
rng = text.rng


def threads() -> int:
    return audio.threads()


# ---------------------------------------------------------------------------
# Text
# ---------------------------------------------------------------------------
SENTENCE = "Spade sat down in the armchair and rolled a cigarette."
SIZES = [1024, 4096]


def bpe_sample() -> str:
    return text.sample_text(max(5, int(100 * SCALE)), 20_000, 2016)  # Sennrich, Haddow & Birch, 2016


def compute_bpe():
    from videos.ai.ai1 import compute as c1

    sample = bpe_sample()
    n_merges = 8000 if SCALE == 1 else 600
    merges, freq, saved = text.learn_bpe(sample, n_merges)
    base = sorted(set(text.norm(sample)) | {" "})
    valid, passage = c1.text("valid")[:200_000], c1.text("passage")
    sizes = [n for n in ((500, 2000, 8000) if SCALE == 1 else (100, 300, 600)) if n <= len(merges)] or [len(merges)]
    L0 = sum(len(w) for w in text.words_of(sample))
    out = dict(first=[a + b for a, b in merges[:40]], first_counts=saved[:40], sizes=sizes, sentence=SENTENCE,
               n_merges=len(merges), merges=[[a, b] for a, b in merges], counts=freq, saved=saved, base=base,
               sample_chars=L0, length=[L0 - int(np.sum(saved[:k])) for k in range(0, len(merges) + 1, 50)])
    # the savings add up: the merged text is exactly as long as the counts say
    check = text.BPE(merges, len(merges))
    assert sum(len(check.word(w)) for w in text.words_of(sample)) == L0 - sum(saved)
    for n in sizes:
        tok = text.BPE(merges, n)
        for name, t in (("valid", valid), ("passage", passage)):
            out[f"cpt_{name}{n}"] = len(" " + text.norm(t)) / len(tok(t))
        out[f"cut{n}"] = tok(SENTENCE)
    out["cut0"] = text.BPE(merges, 0)(SENTENCE)
    out["wordpiece"] = text.wordpiece_merges(sample, 20 if SCALE == 1 else 5)
    import re

    sw = re.findall(r"[a-z']+", sample.lower())
    types = set(sw)
    pw = re.findall(r"[a-z']+", passage.lower())
    unseen = [w for w in pw if w not in types]
    out.update(n_word_types=len(types), n_words_sample=len(sw), oov_passage=len(unseen) / len(pw),
               unseen_examples=sorted(set(unseen), key=lambda w: (-len(w), w))[:12], n_words_passage=len(pw))
    try:  # the series' own model's tokenizer: a byte-level BPE of 4,096 tokens (explainer/ai/novels.py)
        from explainer.ai import novels

        ids = novels.encode(passage)
        out["novels_cpt"] = len(passage) / len(ids)
        out["novels_vocab"] = int(novels.tokenizer().get_vocab_size())
        out["novels_cut"] = [novels.decode([i]) for i in novels.encode(SENTENCE)]
    except Exception as e:  # noqa: BLE001
        print("    (no novels tokenizer:", e, ")")
    print("    BPE: characters per token on the passage: " +
          ", ".join(f"{n}: {out[f'cpt_passage{n}']:.2f}" for n in sizes), flush=True)
    assert len(sizes) == 1 or out["cpt_passage" + str(sizes[-1])] > out["cpt_passage" + str(sizes[0])] > 1.5
    return out


def bpe_tokenizer(V: int):
    b = load("bpe")
    merges = [tuple(m) for m in b["merges"]]
    n = max(0, V - len(b["base"]))
    return text.BPE(merges, n), list(b["base"]) + [a + c for a, c in merges[:n]]


def compute_unigram():
    from videos.ai.ai1 import compute as c1

    sample = bpe_sample()
    sizes = SIZES if SCALE == 1 else [256, 128]
    vocabs, replay = text.learn_unigram(sample, sizes=sizes, seed_size=40_000 if SCALE == 1 else 4000)
    valid, passage = c1.text("valid")[:200_000], c1.text("passage")
    out = dict(sizes=sizes, replay=replay, sentence=SENTENCE)
    g = rng(2018)  # Kudo, 2018
    for V in sizes:
        u = text.Unigram(vocabs[V])
        bt, _ = bpe_tokenizer(V)
        for name, t in (("valid", valid), ("passage", passage)):
            n_chars = len(" " + text.norm(t))
            out[f"cpt_{name}{V}"] = n_chars / len(u(t))
            out[f"bpe_cpt_{name}{V}"] = n_chars / len(bt(t))
        out[f"cut{V}"] = u(SENTENCE)
        out[f"bpe_cut{V}"] = bt(SENTENCE)
        out[f"vocab{V}"] = sorted(vocabs[V].items(), key=lambda kv: -kv[1])
        out[f"samples{V}"] = {w: [u.sample(w, g, alpha=0.3) for _ in range(5)] for w in (" cigarette", " armchair", " rolled")}
        bad = [w for w in text.words_of(passage) if len(u.word(w)) != len(bt.word(w))]
        out[f"differ{V}"] = len(bad) / len(text.words_of(passage))
    print("    unigram: characters per token on the passage: " + ", ".join(
        f"{V}: {out[f'cpt_passage{V}']:.2f} (BPE {out[f'bpe_cpt_passage{V}']:.2f})" for V in sizes), flush=True)
    return out


def unigram_tokenizer(V: int):
    u = load("unigram")
    voc = {p: lp for p, lp in u[f"vocab{V}"]}
    return text.Unigram(voc), [p for p, _ in u[f"vocab{V}"]]


LM_CONFIGS = [("bytes", 256), ("bpe", 1024), ("unigram", 1024), ("bpe", 4096), ("unigram", 4096)]
LM_SEEDS = [0, 1, 2]


def lm_corpora():
    from videos.ai.ai1 import compute as c1

    train = text.sample_text(max(5, int(300 * SCALE)), 20_000, 7)
    valid = c1.text("valid")[:300_000]
    passage = c1.text("passage")
    return train, valid, passage


def encoder_for(kind: str, V: int):
    """(encode: text -> ids, vocabulary size, decode: ids -> text) for one tokenizer."""
    if kind == "bytes":
        return (lambda t: text.byte_ids(" " + text.norm(t))), 256, (lambda ids: bytes(int(i) for i in ids).decode("utf-8", "replace"))
    V_ = V if SCALE == 1 else {1024: 256, 4096: 128}.get(V, V)
    tok, pieces = bpe_tokenizer(V_) if kind == "bpe" else unigram_tokenizer(V_)
    table = {p: i for i, p in enumerate(pieces)}
    table["<unk>"] = len(pieces)
    inv = pieces + ["?"]
    return (lambda t: text.ids_for(tok, t, table)), len(pieces) + 1, (lambda ids: "".join(inv[int(i)] for i in ids))


def compute_lms():
    import torch

    from explainer.lm import pocket

    n_threads = threads()
    train, valid, passage = lm_corpora()
    part = CACHE.partial("lms", dict(cfg=text.LM_CFG, budget=text.LM_BUDGET_STEPS, scale=SCALE, seeds=LM_SEEDS,
                                     configs=LM_CONFIGS, v=1))
    MODELS.mkdir(parents=True, exist_ok=True)
    n_pass = len(" " + text.norm(passage))
    n_val = len(" " + text.norm(valid))
    enc_cache = {}
    for kind, V in LM_CONFIGS:
        for seed in LM_SEEDS:
            key = f"{kind}{V}_s{seed}"
            if key in part:
                continue
            if (kind, V) not in enc_cache:
                t0 = time.time()
                enc, vocab, dec = encoder_for(kind, V)
                enc_cache[(kind, V)] = (enc(train), enc(valid), enc(passage), vocab, dec)
                print(f"    {kind} {V}: {len(enc_cache[(kind, V)][0]):,} training tokens ({time.time() - t0:.0f} s)",
                      flush=True)
            ids_tr, ids_va, ids_pa, vocab, dec = enc_cache[(kind, V)]
            t0 = time.time()
            res, budget = text.train_lm(key, ids_tr, ids_va, vocab, seed, ckpt=MODELS / f"lm_{key}.ckpt",
                                        threads=n_threads)
            model = res.pop("_model")
            res.pop("_opts")
            nll = text.nll_per_token(model, ids_pa, text.LM_CFG["seq"])
            cpt_pa = n_pass / len(ids_pa)
            covered = n_pass - cpt_pa  # the first token is never scored
            bpc = float(np.nansum(nll) / math.log(2) / covered)
            cpt_va = n_val / len(ids_va)
            fpt = pocket.flops_per_token(res["counts"], model.cfg)
            curve = [[tok * fpt, ev / math.log(2) / cpt_va] for _, tok, ev in res["evals"]]
            prompt = list(ids_pa[:8])
            sample = dec(pocket.sample(model, prompt, 60 if kind != "bytes" else 200, temperature=0.8, seed=seed))
            part[key] = dict(bpc=bpc, cpt=cpt_pa, curve=curve, steps=res["steps"], tokens_per_step=res["tokens_per_step"],
                             counts=res["counts"], budget=budget, seconds=time.time() - t0, sample=sample,
                             prompt=dec(prompt), train_tokens=int(len(ids_tr)), valid_bpc=curve[-1][1])
            if kind == "bytes" and seed == 0:
                torch.save({"config": vars(model.cfg), "model": model.state_dict()}, MODELS / "bytes_s0.pt")
            (MODELS / f"lm_{key}.ckpt").unlink(missing_ok=True)
            print(f"    {key}: {bpc:.3f} bits per character on the passage ({res['steps']} steps, "
                  f"{time.time() - t0:.0f} s)", flush=True)
    out = dict(configs=[f"{k}{V}" for k, V in LM_CONFIGS], seeds=LM_SEEDS, passage_chars=n_pass, cfg=text.LM_CFG,
               batch=text.LM_BATCH)
    for kind, V in LM_CONFIGS:
        name = f"{kind}{V}"
        runs = [part[f"{name}_s{s}"] for s in LM_SEEDS]
        out[f"bpc_{name}"] = [r["bpc"] for r in runs]
        out[f"cpt_{name}"] = runs[0]["cpt"]
        out[f"steps_{name}"] = runs[0]["steps"]
        out[f"tps_{name}"] = runs[0]["tokens_per_step"]
        out[f"params_{name}"] = runs[0]["counts"]
        out[f"budget_{name}"] = runs[0]["budget"]
        out[f"train_tokens_{name}"] = runs[0]["train_tokens"]
        for s, r in zip(LM_SEEDS, runs):
            out[f"curve_{name}_s{s}"] = np.array(r["curve"])
        out[f"sample_{name}"] = runs[0]["sample"]
        out[f"prompt_{name}"] = runs[0]["prompt"]
    try:
        from videos.ai.ai1 import compute as c1

        sb = c1.load("scoreboard")
        out["scoreboard"] = [[r["label"], r["bits"]] for r in sb["rows"] if "bits" in r]
    except Exception as e:  # noqa: BLE001
        print("    (no scoreboard:", e, ")")
    return out


def byte_model():
    import torch

    from explainer.lm import pocket

    p = MODELS / "bytes_s0.pt"
    if not p.exists():  # the language-model item kept its numbers but not the weights: retrain the byte model alone
        train, valid, _ = lm_corpora()
        enc, vocab, _ = encoder_for("bytes", 256)
        res, _ = text.train_lm("bytes256_s0", enc(train), enc(valid), vocab, 0, ckpt=MODELS / "lm_bytes256_s0.ckpt",
                               threads=threads())
        MODELS.mkdir(parents=True, exist_ok=True)
        torch.save({"config": vars(res["_model"].cfg), "model": res["_model"].state_dict()}, p)
    ck = torch.load(p)
    m = pocket.PocketGPT(pocket.Config(**ck["config"]))
    m.load_state_dict(ck["model"])
    return m.eval()


def compute_patches():
    from videos.ai.ai1 import compute as c1

    threads()
    passage = (" " + text.norm(c1.text("passage"))).encode("utf-8")
    ids = np.frombuffer(passage, np.uint8).astype(np.int64)
    model = byte_model()
    H, S = text.entropies(model, ids, text.LM_CFG["seq"])
    ok = ~np.isnan(H)
    Hs, Ss = H[ok], S[ok]
    qs = np.linspace(0.05, 0.95, 37)
    sweep = []
    for q in qs:
        th = float(np.quantile(Hs, q))
        start = Hs > th
        n_p = int(start.sum()) + 1
        sweep.append(dict(threshold=th, mean_len=float(len(Hs) / n_p), surprise_share=float(Ss[start].sum() / Ss.sum()),
                          start_share=float(start.mean())))
    # BPE's token starts on the same bytes, for comparison (the 4,096-piece vocabulary)
    tok, _ = bpe_tokenizer(4096 if SCALE == 1 else 128)
    pieces = tok(passage.decode("utf-8"))
    bstart = np.zeros(len(ids), bool)
    k = 0
    for p_ in pieces:
        bstart[k] = True
        k += len(p_.encode("utf-8"))
    bpe_len = len(ids) / len(pieces)
    bshare = float(S[1:][bstart[1:] & ok[1:]].sum() / Ss.sum())
    # the threshold whose patches are as long as BPE's tokens, and the example sentence under it
    lens = np.array([s_["mean_len"] for s_ in sweep])
    j = int(np.argmin(np.abs(lens - bpe_len)))
    th = sweep[j]["threshold"]
    i0 = passage.find(b" Spade")
    i0 = i0 if i0 >= 0 else 200
    seg = slice(i0, i0 + 64)
    out = dict(sweep=sweep, bpe_len=bpe_len, bpe_share=bshare, bpe_start_share=float(bstart[ok].mean()), match=j,
               threshold=th, example=passage[seg].decode("utf-8", "replace"), example_H=H[seg], example_S=S[seg], example_bpe=bstart[seg],
               mean_H=float(Hs.mean()), bits_per_byte=float(Ss.mean()), n_bytes=int(ok.sum()),
               H_hist=np.histogram(Hs, bins=30, range=(0, 6))[0])
    m = sweep[j]
    print(f"    entropy patches as long as BPE tokens ({bpe_len:.2f} bytes): {100 * m['start_share']:.0f}% of bytes start "
          f"one and carry {100 * m['surprise_share']:.0f}% of the surprise; BPE's token starts carry "
          f"{100 * bshare:.0f}%", flush=True)
    return out


# ---------------------------------------------------------------------------
# Pictures
# ---------------------------------------------------------------------------
def compute_codebooks():
    return vq.compute_codebooks()


def compute_vqtrain():
    part = CACHE.partial("vqtrain", dict(steps=int(vq.VQ_STEPS * SCALE), methods=vq.VQ_METHODS, seeds=vq.VQ_SEEDS, v=1))
    n = threads()
    for m in vq.VQ_METHODS:
        for s in vq.VQ_SEEDS:
            key = f"{m}_s{s}"
            if key in part:
                continue
            t0 = time.time()
            r = vq.run_vq(m, s, threads=n)
            if s != vq.VQ_SEEDS[0]:  # the replays are kept for the first seed only
                r = {k_: v_ for k_, v_ in r.items() if k_ not in ("recon", "z", "book")}
            part[key] = r
            print(f"    {key}: {r['final_used']} of {vq.VQ_K} codes in use, perplexity {r['final_ppl']:.1f}, "
                  f"error {r['final_mse']:.4f} ({time.time() - t0:.0f} s)", flush=True)
    out = dict(methods=vq.VQ_METHODS, seeds=vq.VQ_SEEDS, K=vq.VQ_K, steps=int(vq.VQ_STEPS * SCALE), batch=vq.VQ_BATCH)
    _, test, _ = vq.vq_data()
    out["test"] = test[:6]
    for m in vq.VQ_METHODS:
        runs = [part[f"{m}_s{s}"] for s in vq.VQ_SEEDS]
        out[f"used_{m}"] = [r["final_used"] for r in runs]
        out[f"ppl_{m}"] = [r["final_ppl"] for r in runs]
        out[f"mse_{m}"] = [r["final_mse"] for r in runs]
        out[f"curve_{m}"] = np.array([r["curve"] for r in runs])  # seeds x points x (step, rec, codes in batch)
        out[f"used_t_{m}"] = np.array([r["used"] for r in runs])
        out[f"ppl_t_{m}"] = np.array([r["ppl"] for r in runs])
        r0 = runs[0]
        out["checks"] = r0["checks"]
        out[f"recon_{m}"] = np.array(r0["recon"], np.float32)
        out[f"z_{m}"] = np.array(r0["z"], np.float32)
        out[f"book_{m}"] = np.array(r0["book"], np.float32)
        out[f"counts_{m}"] = np.array(r0["counts"])
    return out


# ---------------------------------------------------------------------------
# Sound
# ---------------------------------------------------------------------------
def compute_speech():
    plan = audio.synthesize_all(CACHE)
    out = dict(voices_train=audio.VOICES_TRAIN, voices_test=audio.VOICES_TEST, digits=audio.DIGITS)
    secs = {}
    for v in plan:
        cl = audio.clips(CACHE, v)
        for kind in ("word", "string", "sentence"):
            secs.setdefault(kind, 0.0)
            secs[kind] += sum(len(a) for k, _, _, a in cl if k == kind) / audio.SR
        out[f"n_{v}"] = len(cl)
    out["seconds"] = secs
    k, t, s, a = audio.clips(CACHE, audio.VOICES_TEST[0], "sentence")[1]
    out["hook_text"], out["hook_mel"] = t, audio.whisper_logmel(a, pad_to=0)
    out["hook_wave"] = a[::8]
    return out


def compute_nyquist():
    load("speech")
    return audio.compute_nyquist(CACHE)


def compute_mel():
    load("speech")
    return audio.compute_mel(CACHE)


def compute_audrey():
    load("speech")
    return audio.compute_audrey(CACHE)


def compute_codec():
    load("speech")
    return audio.compute_codec(CACHE)


def compute_whisper():
    load("speech")
    return audio.compute_whisper(CACHE)


def compute_ctc():
    load("speech")
    part = CACHE.partial("ctc", dict(steps=int(audio.CTC_STEPS * SCALE), seeds=audio.CTC_SEEDS, v=1))
    for s in audio.CTC_SEEDS:
        if f"s{s}" in part:
            continue
        t0 = time.time()
        r = audio.run_ctc(CACHE, s)
        if s != audio.CTC_SEEDS[0]:
            r = {k: v for k, v in r.items() if k not in ("snaps", "lattice")}
        part[f"s{s}"] = r
        print(f"    ctc seed {s}: word error {r['wer']:.1%} on held-out voices, {r['wer_seen']:.1%} on training voices "
              f"({time.time() - t0:.0f} s)", flush=True)
    r0 = part[f"s{audio.CTC_SEEDS[0]}"]
    out = dict(seeds=audio.CTC_SEEDS, wer=[part[f"s{s}"]["wer"] for s in audio.CTC_SEEDS],
               wer_seen=[part[f"s{s}"]["wer_seen"] for s in audio.CTC_SEEDS],
               curves=np.array([part[f"s{s}"]["curve"] for s in audio.CTC_SEEDS]),
               hyps=r0["hyps"], hyps_seen=r0["hyps_seen"], params=r0["params"], steps=r0["steps"],
               alphabet=audio.ALPHA, snap_steps=[s_["step"] for s_ in r0["snaps"]],
               snap_text=[s_["text"] for s_ in r0["snaps"]],
               snap_lp=np.array([s_["lp"] for s_ in r0["snaps"]], np.float32))
    lat = r0["lattice"]
    out.update(lat_text=lat["text"], lat_ext=lat["ext"], lat_total=lat["total"], lat_path=np.array(lat["path"]),
               lat_alpha=np.array(lat["log_alpha"], np.float32), lat_gamma=np.array(lat["gamma"], np.float32),
               lat_lp=np.array(lat["lp"], np.float32))
    test = [t for v in audio.VOICES_TEST for k, t, s, a in audio.clips(CACHE, v, "string")]
    out["refs"] = test
    return out


NARRATOR_SENTENCE = "Every sense is a token: text, pictures and sound."


def compute_narrator():
    """The narrator's own codes, through ``.venv-tts`` if it has ``qwen_tts`` and the model is cached; otherwise an
    empty record (the scene then says so and draws the codec of chapter nine instead)."""
    from explainer.paths import ROOT

    py = ROOT / ".venv-tts" / "bin" / "python"
    prof = json.loads((ROOT / "tools" / "voices.json").read_text())["qwen3-calm-a"]["voices"]["en"]
    hub = Path(os.environ.get("HF_HOME", Path.home() / ".cache" / "huggingface")) / "hub"
    snap = sorted(hub.glob("models--Qwen--Qwen3-TTS-12Hz-1.7B-Base/snapshots/*/speech_tokenizer/config.json"))
    if not py.exists() or not snap:
        print("    (no .venv-tts or no Qwen3-TTS in the Hugging Face cache: the narrator's codes are skipped)")
        return dict(available=False, sentence=NARRATOR_SENTENCE)
    cfg = json.loads(snap[-1].read_text())
    tmp = CACHE.dir / "narrator.tmp.npz"
    args = [str(py), str(ROOT / "videos" / "ai" / "ai23" / "narrator_codes.py"), str(tmp), str(ROOT / prof["ref_audio"]),
            prof["ref_text"], NARRATOR_SENTENCE]
    if os.environ.get("AI23_NARRATOR_GENERATE", "1") == "0" or SCALE != 1:
        args.append("--no-generate")
    env = dict(os.environ, AI23_THREADS=os.environ.get("AI23_THREADS", "2"))
    t0 = time.time()
    r = subprocess.run(args, env=env, capture_output=True, text=True)
    if r.returncode or not tmp.exists():
        print("    (the narrator's codes failed:", (r.stderr or r.stdout)[-600:], ")")
        return dict(available=False, sentence=NARRATOR_SENTENCE)
    with np.load(tmp) as z:
        d = {k: z[k] for k in z.files}
    tmp.unlink()
    ref = d["ref_wav"].astype(np.float32) / 32767
    dec = d["dec_wav"].astype(np.float32) / 32767
    n_q = int(cfg.get("encoder_valid_num_quantizers", d["ref_codes"].shape[1]))
    K = int(cfg["encoder_config"]["codebook_size"])
    hz = float(cfg["encoder_config"].get("_frame_rate", 12.5))
    out = dict(available=True, ref_text=prof["ref_text"], ref_codes=d["ref_codes"].astype(np.int64),
               ref_mel=audio.whisper_logmel(ref, pad_to=0), dec_mel=audio.whisper_logmel(dec, pad_to=0),
               ref_seconds=len(ref) / audio.SR, n_q=n_q, K=K, hz=hz, bps=hz * n_q * math.log2(K),
               mel_dist=audio.mel_distance(ref, dec), sentence=NARRATOR_SENTENCE, generated="gen_codes" in d,
               seconds=time.time() - t0)
    out["ref_hyp"], out["dec_hyp"] = audio.transcribe([ref[:8 * audio.SR], dec[:8 * audio.SR]])
    if "gen_codes" in d:
        gw = d["gen_wav"].astype(np.float32) / 32767
        out.update(gen_codes=d["gen_codes"].astype(np.int64), gen_mel=audio.whisper_logmel(gw, pad_to=0),
                   gen_seconds=len(gw) / audio.SR, gen_hyp=audio.transcribe([gw])[0])
    print(f"    narrator: {out['ref_seconds']:.1f} s as {d['ref_codes'].shape[0]} frames x {n_q} codes "
          f"({out['bps']:.0f} bits a second); generated: {out['generated']}", flush=True)
    return out


# ---------------------------------------------------------------------------
# Pictures and words
# ---------------------------------------------------------------------------
def compute_clip():
    part = CACHE.partial("clip", dict(pairs=int(clip.PAIRS * SCALE), batches=clip.BATCHES, seeds=clip.SEEDS, v=1))
    n = threads()
    for L in clip.LOSSES:
        for B in clip.BATCHES:
            for s in clip.SEEDS:
                key = f"{L}_{B}_s{s}"
                if key in part:
                    continue
                t0 = time.time()
                r = clip.run(L, B, s, snaps_wanted=(B == clip.BATCHES[-1] and s == clip.SEEDS[0]), threads=n)
                part[key] = r
                print(f"    {key}: unseen captions {r['unseen']:.1%}, seen {r['seen']:.1%}, InfoNCE estimate "
                      f"{r['mi'][str(B)]:.2f} nats (log N = {math.log(B):.2f}) ({time.time() - t0:.0f} s)", flush=True)
    imgs, caps, timgs, tcaps, uniq, vocab, held = clip.data()
    out = dict(losses=clip.LOSSES, batches=clip.BATCHES, seeds=clip.SEEDS, pairs=int(clip.PAIRS * SCALE),
               n_captions=len(uniq), n_held=len(held), n_images=len(imgs), vocab=vocab, res=clip.RES,
               H_caption=math.log(len(uniq) - len(held)))
    for L in clip.LOSSES:
        for B in clip.BATCHES:
            runs = [part[f"{L}_{B}_s{s}"] for s in clip.SEEDS]
            for k in ("seen", "unseen", "letter_seen", "letter_unseen"):
                out[f"{k}_{L}_{B}"] = [r[k] for r in runs]
            out[f"mi_{L}_{B}"] = [[r["mi"][str(N)] for N in clip.BATCHES] for r in runs]
            out[f"res_{L}_{B}"] = [[r["res"][str(x)] for x in clip.RES] for r in runs]
            out[f"steps_{L}_{B}"] = runs[0]["steps"]
            out[f"losses_{L}_{B}"] = np.array(runs[0]["losses"])
        r0 = part[f"{L}_{clip.BATCHES[-1]}_s{clip.SEEDS[0]}"]
        out[f"snaps_{L}"] = np.array(r0["snaps"], np.float32)
        out[f"checks_{L}"] = r0["checks"]
        out[f"sim_{L}"] = np.array(r0["sim"], np.float32)
        out["batch_imgs"] = np.array(r0["batch_imgs"], np.float32)
        out["batch_caps"] = r0["batch_caps"]
    return out


def compute_vlm():
    return clip.compute_vlm_arith()


ITEMS = {
    "bpe": compute_bpe,
    "unigram": compute_unigram,
    "lms": compute_lms,
    "patches": compute_patches,
    "codebooks": compute_codebooks,
    "vqtrain": compute_vqtrain,
    "speech": compute_speech,
    "nyquist": compute_nyquist,
    "mel": compute_mel,
    "audrey": compute_audrey,
    "ctc": compute_ctc,
    "whisper": compute_whisper,
    "codec": compute_codec,
    "narrator": compute_narrator,
    "clip": compute_clip,
    "vlm": compute_vlm,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
