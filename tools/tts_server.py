#!/usr/bin/env python
"""Neural narration server: synthesize, verify, and align every narration line.

Runs in its own environment (MLX on Apple Silicon), separate from the render pipeline:

    uv venv --python 3.12 .venv-tts && source .venv-tts/bin/activate && uv pip install mlx-audio soundfile pypinyin
    python tools/tts_server.py --voice qwen3-ryan-vivian        # serves http://127.0.0.1:8765

Render with ``EXPLAINER_TTS=server EXPLAINER_VOICE=<the same profile>`` (``explainer/tts.py`` caches every line,
so the server is needed only for new or changed lines).  For each line the server

1. splits it into sentences (long ones at clause boundaries) and synthesizes each,
2. transcribes each take with an ASR model and retries (fresh sampling) when the take drops, repeats or garbles
   words, keeping the most faithful take,
3. trims the takes' silences and joins them with even pauses, and
4. forced-aligns the text to the audio: per-word (English) or per-character (Chinese) timings, which drive the
   animation bookmarks and the subtitles.

Voice profiles are in ``tools/voices.json``.  Takes that never pass the check are logged to ``.cache/tts/qa.jsonl``.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parents[1]


def _load_lang():
    """explainer/lang.py by path: importing the explainer package would pull in manim, which this env lacks."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("explainer_lang", ROOT / "explainer" / "lang.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


L = _load_lang()  # tokenization and normalization only

QA_LOG = ROOT / ".cache" / "tts" / "qa.jsonl"
ALIGNER = "mlx-community/Qwen3-ForcedAligner-0.6B-8bit"
ASR = "mlx-community/Qwen3-ASR-0.6B-4bit"
MODELS = Path.home() / "models"  # local copies (curl-resumed on slow links); else fetched from the Hub


def model_path(repo: str) -> str:
    local = MODELS / repo
    return str(local) if (local / "config.json").exists() else repo
LANG_NAME = {"en": "English", "zh": "Chinese"}
PAUSE = {"sentence": 0.38, "clause": 0.22}


# ---------------------------------------------------------------------------
# Text
# ---------------------------------------------------------------------------
def sentences(text: str, lang: str, max_chars: int) -> list[tuple[str, str]]:
    """[(chunk, pause kind after it)]: sentences, with over-long ones split at clause boundaries."""
    if lang == "en":
        parts = re.split(r"(?<=[.?!])\s+(?=[A-Z0-9\"'(])", text)
        clause = r"(?<=[;:])\s+|(?<=,)\s+(?=(?:and|but|so|which|where|because|while)\b)"
    else:
        parts = [p for p in re.split(r"(?<=[。！？])", text) if p.strip()]
        clause = r"(?<=[；：])|(?<=，)"
    out: list[tuple[str, str]] = []
    for p in parts:
        p = p.strip()
        if len(p) <= max_chars:
            out.append((p, "sentence"))
            continue
        pieces, cur = [], ""
        for c in re.split(clause, p):
            if cur and len(cur) + len(c) > max_chars:
                pieces.append(cur)
                cur = c
            else:
                cur = (cur + (" " if lang == "en" and cur else "") + c) if cur else c
        if cur:
            pieces.append(cur)
        out += [(c.strip(), "clause") for c in pieces[:-1]] + [(pieces[-1].strip(), "sentence")]
    return [(c, k) for c, k in out if L.norm(c)]


def similarity(a: str, b: str) -> float:
    a, b = L.norm(a), L.norm(b)
    return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio() if a or b else 1.0


# Spoken forms an ASR writes differently from the script (digits vs. words, spellings): normalize both sides.
_EN_NUM = {"zero": "0", "one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7",
           "eight": "8", "nine": "9", "ten": "10"}
_ZH_NUM = str.maketrans("零〇一二两三四五六七八九", "001223456789")


def comparable(text: str, lang: str) -> str:
    if lang == "en":
        return " ".join(_EN_NUM.get(w, w) for w in re.findall(r"[a-z0-9]+", text.lower()))
    # Compare Chinese by sound (pinyin with tones): the recognizer often writes a homophone (项数 as 橡树), which
    # is the right speech and should not cost a re-take; a wrong tone still shows.
    from pypinyin import Style, lazy_pinyin

    return " ".join(lazy_pinyin(text.translate(_ZH_NUM), style=Style.TONE3)).lower()


# ---------------------------------------------------------------------------
# Audio
# ---------------------------------------------------------------------------
def trim(audio: np.ndarray, sr: int, keep: float = 0.04) -> np.ndarray:
    """Cut leading/trailing silence (frame RMS below -45 dBFS), keeping a few ms of air."""
    hop = int(sr * 0.01)
    if len(audio) < hop * 3:
        return audio
    frames = audio[: len(audio) // hop * hop].reshape(-1, hop)
    rms = np.sqrt((frames ** 2).mean(axis=1) + 1e-12)
    loud = np.where(20 * np.log10(rms) > -45)[0]
    if not len(loud):
        return audio
    a = max(0, loud[0] * hop - int(keep * sr))
    b = min(len(audio), (loud[-1] + 1) * hop + int(keep * sr))
    return audio[a:b]


# ---------------------------------------------------------------------------
# Engines
# ---------------------------------------------------------------------------
class Engine:
    def __init__(self, profile: dict):
        from mlx_audio.tts.utils import load_model

        self.profile = profile
        self.model = load_model(model_path(profile["model"]))
        self.sr = self.model.sample_rate
        self.batch = profile.get("batch", True)

    def takes(self, texts: list[str], lang: str, attempt: int) -> list[np.ndarray]:
        """One take of each text.  The CustomVoice model decodes them as one batch: decoding is bound by reading
        the weights, and one read per step serves every sentence, so a line costs little more than its longest."""
        p = self.profile["voices"][lang]
        if self.profile["kind"] != "qwen3-custom" or not self.batch or len(texts) == 1:
            return [self.take(t_, lang, attempt) for t_ in texts]
        kw = dict(p.get("params", {}))
        if attempt:
            kw["temperature"] = max(0.5, kw.get("temperature", 0.9) - 0.1 * attempt)
        parts: dict[int, list] = {i: [] for i in range(len(texts))}
        for r in self.model.batch_generate(texts, voices=[p["speaker"]] * len(texts),
                                           instructs=[p.get("instruct")] * len(texts), lang_code=LANG_NAME[lang],
                                           **kw):
            parts[r.sequence_idx].append(np.asarray(r.audio, dtype=np.float32).reshape(-1))
        return [np.concatenate(parts[i]) if parts[i] else np.zeros(self.sr // 10, np.float32)
                for i in range(len(texts))]

    def take(self, text: str, lang: str, attempt: int) -> np.ndarray:
        p = self.profile["voices"][lang]
        kind = self.profile["kind"]
        kw = dict(p.get("params", {}))
        if attempt:  # resample on retries; a slightly cooler temperature steadies a hard sentence
            kw["temperature"] = max(0.5, kw.get("temperature", 0.9) - 0.1 * attempt)
        if kind == "qwen3-custom":
            gen = self.model.generate_custom_voice(text=text, speaker=p["speaker"], language=LANG_NAME[lang],
                                                   instruct=p.get("instruct"), **kw)
        elif kind == "qwen3-clone":
            gen = self.model.generate(text=text, ref_audio=str(ROOT / p["ref_audio"]), ref_text=p["ref_text"],
                                      lang_code=LANG_NAME[lang].lower(), **kw)
        elif kind == "voxcpm2":
            kw.pop("temperature", None)
            if "ref_audio" in p:
                kw.update(prompt_audio=str(ROOT / p["ref_audio"]), prompt_text=p["ref_text"])
            gen = self.model.generate(text=text, instruct=p.get("instruct"), **kw)
        else:
            raise ValueError(kind)
        return np.concatenate([np.asarray(r.audio, dtype=np.float32).reshape(-1) for r in gen])


class Checker:
    """ASR for verifying takes, and the forced aligner for timings."""

    def __init__(self):
        from mlx_audio.stt.utils import load_model

        self.asr = load_model(model_path(ASR))
        self.aligner = load_model(model_path(ALIGNER))

    def transcribe(self, audio: np.ndarray, sr: int, lang: str) -> str:
        a16 = resample(audio, sr, 16000)
        out = self.asr.generate(a16, language=LANG_NAME[lang])
        return getattr(out, "text", str(out))

    def align(self, audio: np.ndarray, sr: int, text: str, lang: str) -> list[tuple[str, float, float]]:
        a16 = resample(audio, sr, 16000)
        res = self.aligner.generate(a16, text=text, language=LANG_NAME[lang])
        return [(it.text, float(it.start_time), float(it.end_time)) for it in res]


def resample(audio: np.ndarray, sr: int, to: int) -> np.ndarray:
    if sr == to:
        return audio
    n = int(round(len(audio) * to / sr))
    return np.interp(np.linspace(0, len(audio) - 1, n), np.arange(len(audio)), audio).astype(np.float32)


# ---------------------------------------------------------------------------
# One narration line
# ---------------------------------------------------------------------------
def narrate(engine: Engine, checker: Checker, text: str, lang: str, max_tries: int = 4) -> tuple[np.ndarray, list]:
    sr = engine.sr
    prof = engine.profile
    accept = prof.get("accept", 0.93)
    runaway = 1.2 if lang == "en" else 0.75  # seconds per token: a take far longer than its text babbles or stalls
    chunks = sentences(text, lang, prof.get("max_chars", {"en": 260, "zh": 90})[lang])
    n = len(chunks)
    best: list[np.ndarray | None] = [None] * n
    best_score, best_heard = [-1.0] * n, [""] * n
    heard_before: list[set] = [set() for _ in range(n)]
    pending = list(range(n))
    # Every round takes all the sentences still pending at once (one batch), checks each by ear, and keeps
    # the ones that still fail for the next round.
    for attempt in range(max_tries):
        takes = engine.takes([chunks[i][0] for i in pending], lang, attempt)
        still = []
        for i, raw in zip(pending, takes):
            chunk = chunks[i][0]
            audio = trim(raw, sr)
            dur = len(audio) / sr
            per_unit = dur / max(len(L.tokens(chunk, lang)), 1)
            heard = checker.transcribe(audio, sr, lang)
            score = similarity(comparable(chunk, lang), comparable(heard, lang))
            if per_unit > runaway:
                score -= 0.5
            print(f"    take {attempt + 1}: {score:.3f} {dur:5.1f}s  {chunk[:40]!r} -> {heard[:60]!r}", flush=True)
            if score > best_score[i]:
                best[i], best_score[i], best_heard[i] = audio, score, heard
            if score >= accept:
                continue
            # Two different takes heard as the same words: the gap to the script is the recognizer's spelling
            # (a symbol, a homophone), not the voice, so more takes would not close it.
            said = L.norm(comparable(heard, lang))
            if said in heard_before[i] and per_unit <= runaway:
                continue
            heard_before[i].add(said)
            still.append(i)
        pending = still
        if not pending:
            break
    pieces, tokens, t = [np.zeros(int(0.12 * sr), np.float32)], [], 0.12
    for i, (chunk, pause) in enumerate(chunks):
        if best_score[i] < accept:
            QA_LOG.parent.mkdir(parents=True, exist_ok=True)
            with open(QA_LOG, "a") as f:
                f.write(json.dumps({"lang": lang, "voice": prof["name"], "text": chunk, "heard": best_heard[i],
                                    "score": round(best_score[i], 3)}, ensure_ascii=False) + "\n")
        for w, a, b in checker.align(best[i], sr, chunk, lang):
            tokens.append((w, t + a, t + b))
        pieces.append(best[i])
        t += len(best[i]) / sr
        gap = np.zeros(int(PAUSE[pause] * sr), np.float32)
        pieces.append(gap)
        t += len(gap) / sr
    audio = np.concatenate(pieces)
    return audio, tokens


# ---------------------------------------------------------------------------
# Server
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", required=True, help="profile name in tools/voices.json")
    ap.add_argument("--port", type=int, default=8765)
    args = ap.parse_args()
    profiles = json.loads((ROOT / "tools" / "voices.json").read_text())
    profile = dict(profiles[args.voice], name=args.voice)
    engine, checker = Engine(profile), Checker()
    lock = threading.Lock()
    print(f"voice {args.voice} ({profile['model']}, {engine.sr} Hz) on :{args.port}", flush=True)

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            req = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            if req.get("voice") != args.voice:
                self.send_error(409, f"server voice is {args.voice}, request wants {req.get('voice')}")
                return
            with lock:
                t0 = time.time()
                try:
                    audio, tokens = narrate(engine, checker, req["text"], req["lang"])
                except Exception as e:  # report, keep serving
                    self.send_error(500, repr(e)[:300])
                    return
                peak = float(np.abs(audio).max() or 1.0)
                if peak > 0.98:
                    audio = audio * (0.98 / peak)
                sf.write(req["out"], audio, engine.sr, subtype="PCM_16", format="WAV")
                dur = len(audio) / engine.sr
                print(f"{dur:6.1f}s audio in {time.time() - t0:6.1f}s  {req['text'][:70]}", flush=True)
            body = json.dumps({"duration": dur, "tokens": tokens}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *a):
            pass

    HTTPServer(("127.0.0.1", args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
