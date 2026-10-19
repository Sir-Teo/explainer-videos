#!/usr/bin/env python
"""Narration on a Colab GPU: the batched twin of tools/tts_server.py (same chunking, ASR check, retries, pauses and
word timings, so a line sounds like the server's), run on the VM by tools/colab_narrate.py.

    python colab_tts_worker.py jobs.json --lang en --out /content/tts_out [--batch 16]

``jobs.json`` is a list of {key, text, spoken}; each finished line is written to ``<out>/<key>.wav`` and ``<key>.json``
(the TTS cache's own format), so a restart skips what is done. Needs qwen-tts, qwen-asr, soundfile, pypinyin.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import tts_server as T  # noqa: E402  (its mlx imports are lazy, so it loads without Apple silicon)

os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")
L = T.L
CAP_PER_SEC = 12  # codec frames per second of speech (12 Hz tokenizer)


def frame_cap(chunks: list[str], lang: str) -> int:
    """Generation limit for a batch: a take twice as long as its text needs is a stall, not speech."""
    longest = max(len(c) for c in chunks)
    secs = longest / 8 + 3 if lang == "en" else longest * 0.75 + 3
    return int(secs * CAP_PER_SEC)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("jobs")
    ap.add_argument("--lang", required=True)
    ap.add_argument("--out", default="/content/tts_out")
    ap.add_argument("--voice", default="qwen3-calm-a")
    ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--group", type=int, default=48, help="lines worked on together, then written out")
    args = ap.parse_args()
    import torch
    from qwen_asr import Qwen3ASRModel, Qwen3ForcedAligner
    from qwen_tts import Qwen3TTSModel

    lang = args.lang
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    prof = dict(json.loads((ROOT / "tools" / "voices.json").read_text())[args.voice], name=args.voice)
    vp = prof["voices"][lang]
    accept = prof.get("accept", 0.93)
    max_chars = prof.get("max_chars", {"en": 260, "zh": 90})[lang]
    runaway = 1.2 if lang == "en" else 0.75
    LN = T.LANG_NAME[lang]
    base_temp = vp.get("params", {}).get("temperature", 0.9)

    tts = Qwen3TTSModel.from_pretrained("Qwen/Qwen3-TTS-12Hz-1.7B-Base", device_map="cuda:0", dtype=torch.bfloat16)
    asr = Qwen3ASRModel.from_pretrained("Qwen/Qwen3-ASR-0.6B", dtype=torch.bfloat16, device_map="cuda:0",
                                        max_inference_batch_size=32)
    aligner = Qwen3ForcedAligner.from_pretrained("Qwen/Qwen3-ForcedAligner-0.6B", dtype=torch.bfloat16,
                                                 device_map="cuda:0")
    SR = 24000
    ref_audio = str(ROOT / vp["ref_audio"])

    def takes(texts: list[str], attempt: int) -> list[np.ndarray]:
        try:
            return takes_(texts, attempt)
        except torch.OutOfMemoryError:  # the codec decoder's memory grows with batch x length: split the batch
            torch.cuda.empty_cache()
            if len(texts) == 1:
                raise
            h = len(texts) // 2
            print(f"  out of memory at batch {len(texts)}: halving", flush=True)
            return takes(texts[:h], attempt) + takes(texts[h:], attempt)

    def takes_(texts: list[str], attempt: int) -> list[np.ndarray]:
        temp = max(0.5, base_temp - 0.1 * attempt) if attempt else base_temp
        wavs, sr = tts.generate_voice_clone(text=texts, language=[LN] * len(texts), ref_audio=ref_audio,
                                            ref_text=vp["ref_text"], temperature=temp,
                                            max_new_tokens=frame_cap(texts, lang))
        assert sr == SR, sr
        return [np.asarray(w, dtype=np.float32).reshape(-1) for w in wavs]

    def hear(audios: list[np.ndarray]) -> list[str]:
        res = asr.transcribe([(T.resample(a, SR, 16000), 16000) for a in audios], language=[LN] * len(audios))
        return [r.text for r in res]

    def align(audios, texts):
        res = aligner.align([(T.resample(a, SR, 16000), 16000) for a in audios], text=texts, language=[LN] * len(audios))
        return [[(it.text, float(it.start_time), float(it.end_time)) for it in r.items] for r in res]

    jobs = [j for j in json.loads(Path(args.jobs).read_text()) if not (out / f"{j['key']}.json").exists()]
    print(f"{len(jobs)} lines to narrate ({lang})", flush=True)
    t_start, audio_total = time.time(), 0.0

    for g in range(0, len(jobs), args.group):
        group = jobs[g:g + args.group]
        chunks = [T.sentences(j["spoken"], lang, max_chars) for j in group]
        best = [[None] * len(c) for c in chunks]
        score = [[-1.0] * len(c) for c in chunks]
        said = [[""] * len(c) for c in chunks]
        seen = [[set() for _ in c] for c in chunks]
        pending = [(i, k) for i, c in enumerate(chunks) for k in range(len(c))]
        for attempt in range(4):
            pending.sort(key=lambda ik: len(chunks[ik[0]][ik[1]][0]))
            still = []
            for b in range(0, len(pending), args.batch):
                part = pending[b:b + args.batch]
                texts = [chunks[i][k][0] for i, k in part]
                audios = [T.trim(a, SR) for a in takes(texts, attempt)]
                for (i, k), text, audio, heard in zip(part, texts, audios, hear(audios)):
                    dur = len(audio) / SR
                    per_unit = dur / max(len(L.tokens(text, lang)), 1)
                    s = T.similarity(T.comparable(text, lang), T.comparable(heard, lang))
                    if per_unit > runaway:
                        s -= 0.5
                    if s > score[i][k]:
                        best[i][k], score[i][k], said[i][k] = audio, s, heard
                    if s >= accept:
                        continue
                    h = L.norm(T.comparable(heard, lang))
                    if h in seen[i][k] and per_unit <= runaway:
                        continue
                    seen[i][k].add(h)
                    still.append((i, k))
            pending = still
            print(f"  group {g // args.group + 1}, take {attempt + 1}: {len(pending)} sentences to retry", flush=True)
            if not pending:
                break
        flat = [(i, k) for i, c in enumerate(chunks) for k in range(len(c))]
        timings = {}
        for b in range(0, len(flat), 32):
            part = flat[b:b + 32]
            for ik, tk in zip(part, align([best[i][k] for i, k in part], [chunks[i][k][0] for i, k in part])):
                timings[ik] = tk
        for i, job in enumerate(group):
            pieces, tokens, t = [np.zeros(int(0.12 * SR), np.float32)], [], 0.12
            for k, (chunk, pause) in enumerate(chunks[i]):
                if score[i][k] < accept:
                    with open(out / "qa.jsonl", "a") as f:
                        f.write(json.dumps({"lang": lang, "voice": args.voice, "text": chunk, "heard": said[i][k],
                                            "score": round(score[i][k], 3)}, ensure_ascii=False) + "\n")
                for w, a, b_ in timings[(i, k)]:
                    tokens.append((w, t + a, t + b_))
                pieces.append(best[i][k])
                t += len(best[i][k]) / SR
                gap = np.zeros(int(T.PAUSE[pause] * SR), np.float32)
                pieces.append(gap)
                t += len(gap) / SR
            audio = np.concatenate(pieces)
            peak = float(np.abs(audio).max() or 1.0)
            if peak > 0.98:
                audio = audio * (0.98 / peak)
            sf.write(out / f"{job['key']}.wav", audio, SR, subtype="PCM_16", format="WAV")
            dur = len(audio) / SR
            audio_total += dur
            meta = {"text": job.get("text", job["spoken"]), "spoken": job["spoken"], "duration": dur, "tokens": tokens}
            tmp = out / f"{job['key']}.json.tmp"
            tmp.write_text(json.dumps(meta, ensure_ascii=False, indent=1))
            tmp.replace(out / f"{job['key']}.json")  # the .json lands last: its presence means the line is done
        el = time.time() - t_start
        print(f"{g + len(group)}/{len(jobs)} lines, {audio_total / 60:.1f} min of audio in {el / 60:.1f} min "
              f"({audio_total / el:.2f}x real time)", flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
