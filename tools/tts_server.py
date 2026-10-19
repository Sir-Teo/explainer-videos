#!/usr/bin/env python
"""Local narration server: synthesize each sentence, check it by speech recognition (re-taking garbled ones), and
force-align words (Chinese: characters) for the animation bookmarks and subtitles.

    .venv-tts/bin/python tools/tts_server.py --voice qwen3-calm-a                  # MLX on Apple Silicon (default)
    .venv-tts/bin/python tools/tts_server.py --voice qwen3-calm-a --engine torch   # PyTorch: Linux (CUDA, or CPU)

Both engines run the same Qwen3-TTS Base model cloning the same reference voice (profiles in tools/voices.json), the
same Qwen3-ASR check and the same forced aligner, so a line sounds the same whichever machine narrates it. The torch
engine needs ``pip install qwen-tts qwen-asr`` (as tools/colab_tts_worker.py does); on CPU it works, but slowly:
expect several times slower than real time.
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
    import types

    # lang.py imports explainer.paths: give it a bare package and load paths.py by path, too
    pkg = types.ModuleType("explainer")
    pkg.__path__ = [str(ROOT / "explainer")]
    sys.modules["explainer"] = pkg
    spec = importlib.util.spec_from_file_location("explainer.paths", ROOT / "explainer" / "paths.py")
    paths = importlib.util.module_from_spec(spec)
    sys.modules["explainer.paths"] = paths
    spec.loader.exec_module(paths)
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
    """Qwen3-TTS Base, cloning the profile's reference voice (a short, calm recording and its transcript)."""

    def __init__(self, profile: dict):
        from mlx_audio.tts.utils import load_model

        self.profile = profile
        self.model = load_model(model_path(profile["model"]))
        self.sr = self.model.sample_rate

    def takes(self, texts: list[str], lang: str, attempt: int) -> list[np.ndarray]:
        """One take of each text."""
        return [self.take(t_, lang, attempt) for t_ in texts]

    def take(self, text: str, lang: str, attempt: int) -> np.ndarray:
        p = self.profile["voices"][lang]
        kw = dict(p.get("params", {}))
        if attempt:  # resample on retries; a slightly cooler temperature steadies a hard sentence
            kw["temperature"] = max(0.5, kw.get("temperature", 0.9) - 0.1 * attempt)
        gen = self.model.generate(text=text, ref_audio=str(ROOT / p["ref_audio"]), ref_text=p["ref_text"],
                                  lang_code=LANG_NAME[lang].lower(), **kw)
        return np.concatenate([np.asarray(r.audio, dtype=np.float32).reshape(-1) for r in gen])


class TorchEngine(Engine):
    """The same model in PyTorch (qwen-tts), on CUDA if there is a GPU, else on the CPU."""

    MODEL = "Qwen/Qwen3-TTS-12Hz-1.7B-Base"

    def __init__(self, profile: dict):
        import torch
        from qwen_tts import Qwen3TTSModel

        self.profile = profile
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        dtype = torch.bfloat16 if self.device != "cpu" else torch.float32
        self.model = Qwen3TTSModel.from_pretrained(model_path(self.MODEL), device_map=self.device, dtype=dtype)
        self.sr = 24000

    def takes(self, texts: list[str], lang: str, attempt: int) -> list[np.ndarray]:
        p = self.profile["voices"][lang]
        base = p.get("params", {}).get("temperature", 0.9)
        temp = max(0.5, base - 0.1 * attempt) if attempt else base
        longest = max(len(t_) for t_ in texts)
        secs = longest / 8 + 3 if lang == "en" else longest * 0.75 + 3  # a take twice as long as its text is a stall
        wavs, sr = self.model.generate_voice_clone(text=texts, language=[LANG_NAME[lang]] * len(texts),
                                                   ref_audio=str(ROOT / p["ref_audio"]), ref_text=p["ref_text"],
                                                   temperature=temp, max_new_tokens=int(secs * 12))
        assert sr == self.sr, sr
        return [np.asarray(w, dtype=np.float32).reshape(-1) for w in wavs]

    def take(self, text: str, lang: str, attempt: int) -> np.ndarray:
        return self.takes([text], lang, attempt)[0]


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


class TorchChecker(Checker):
    def __init__(self):
        import torch
        from qwen_asr import Qwen3ASRModel, Qwen3ForcedAligner

        dev = "cuda:0" if torch.cuda.is_available() else "cpu"
        dtype = torch.bfloat16 if dev != "cpu" else torch.float32
        self.asr = Qwen3ASRModel.from_pretrained(model_path("Qwen/Qwen3-ASR-0.6B"), dtype=dtype, device_map=dev)
        self.aligner = Qwen3ForcedAligner.from_pretrained(model_path("Qwen/Qwen3-ForcedAligner-0.6B"), dtype=dtype,
                                                          device_map=dev)

    def transcribe(self, audio: np.ndarray, sr: int, lang: str) -> str:
        return self.asr.transcribe([(resample(audio, sr, 16000), 16000)], language=[LANG_NAME[lang]])[0].text

    def align(self, audio: np.ndarray, sr: int, text: str, lang: str) -> list[tuple[str, float, float]]:
        r = self.aligner.align([(resample(audio, sr, 16000), 16000)], text=[text], language=[LANG_NAME[lang]])[0]
        return [(it.text, float(it.start_time), float(it.end_time)) for it in r.items]


def default_engine() -> str:
    import platform

    return "mlx" if sys.platform == "darwin" and platform.machine() == "arm64" else "torch"


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
    ap.add_argument("--engine", choices=["mlx", "torch"], default=default_engine(),
                    help="mlx (Apple Silicon) or torch (Linux: CUDA, or CPU); default: by platform")
    args = ap.parse_args()
    profiles = json.loads((ROOT / "tools" / "voices.json").read_text())
    profile = dict(profiles[args.voice], name=args.voice)
    if args.engine == "mlx":
        import mlx.core as mx

        mx.set_cache_limit(512 * 1024 ** 2)  # freed GPU buffers kept for reuse: shares the machine with the renders
        engine, checker = Engine(profile), Checker()
        release = mx.clear_cache
    else:
        engine, checker = TorchEngine(profile), TorchChecker()

        def release():
            import torch

            if torch.cuda.is_available():
                torch.cuda.empty_cache()
    lock = threading.Lock()
    print(f"voice {args.voice} ({args.engine}: {profile['model'] if args.engine == 'mlx' else TorchEngine.MODEL}, "
          f"{engine.sr} Hz) on :{args.port}", flush=True)

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
                release()
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
