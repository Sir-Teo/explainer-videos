"""Text-to-speech backend for narration.

* Default backend: Kokoro-82M (Apache-2.0), an open neural TTS that runs on CPU
  and returns per-word timestamps, which we use for bookmark-level sync.
* ``EXPLAINER_TTS=silent`` swaps in a silent backend that only *estimates*
  durations.  Handy for fast layout iterations or machines without the model.

Every utterance is cached on disk under ``.cache/tts`` keyed by
(backend, voice, speed, spoken text), so re-rendering a scene never
re-synthesizes unchanged lines.
"""

from __future__ import annotations

import difflib
import hashlib
import json
import os
import re
import wave
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CACHE_DIR = Path(os.environ.get("EXPLAINER_CACHE", REPO_ROOT / ".cache")) / "tts"
SAMPLE_RATE = 24_000
VOICE = os.environ.get("EXPLAINER_VOICE", "af_heart")
SPEED = float(os.environ.get("EXPLAINER_SPEED", "1.0"))
BACKEND = os.environ.get("EXPLAINER_TTS", "kokoro")
_CACHE_VERSION = 2

# ---------------------------------------------------------------------------
# Pronunciation lexicon.  Maps display text -> text the TTS engine should read.
# Kokoro (misaki G2P) accepts inline IPA overrides: [word](/ipa/).
# ---------------------------------------------------------------------------
LEXICON: list[tuple[str, str]] = [
    (r"Navier[–—-]Stokes", "[Navier](/nævjˈeɪ/) Stokes"),
    (r"\bNavier\b", "[Navier](/nævjˈeɪ/)"),
    (r"\bLeray\b", "[Leray](/ləɹˈeɪ/)"),
    (r"\bKármán\b", "[Karman](/kˈɑɹmɑn/)"),
    (r"\bRe\b", "[Re](/ˌɑɹˈi/)"),  # "R-E"
    (r"\bdy\b", "[dy](/dˌiwˈI/)"),  # "dee-why", not "die"
    (r"\bdz\b", "[dz](/dˌizˈi/)"),
    (r"\bmu\b", "[mu](/mjˈu/)"),
    (r"\bnu\b", "[nu](/nˈu/)"),
    (r"\brho\b", "[rho](/ɹˈO/)"),
    (r"\bCórdoba\b", "[Córdoba](/kˈɔɹdəbə/)"),
    (r"\bMartínez-Zoroa\b", "[Martínez](/mɑɹtˈinɛz/) [Zoroa](/zəɹˈOə/)"),
    (r"\bAlpöge\b", "[Alpöge](/ˈɑlpəɡə/)"),
    (r"\bGELU\b", "[GELU](/ʤˈilu/)"),
    # Technical terms outside the G2P dictionary (would otherwise go to the espeak fallback).
    (r"\b[Ss]oftmax\b", r"[\g<0>](/sˈɔftmæks/)"),
    (r"\b[Ll]ogits\b", r"[\g<0>](/lˈOʤɪts/)"),
    (r"\b[Ll]ogit\b", r"[\g<0>](/lˈOʤɪt/)"),
    (r"\bEiffel\b", "[Eiffel](/ˈIfᵊl/)"),
    (r"\b[Bb]ackpropagation\b", r"[\g<0>](/bˌækpɹˌɑpəɡˈAʃən/)"),
    (r"\b[Tt]okenizer\b", r"[\g<0>](/tˈOkənˌIzəɹ/)"),
    (r"\b[Cc]ompleter\b", r"[\g<0>](/kəmplˈiTəɹ/)"),
    (r"\b[Ss]ubword\b", r"[\g<0>](/sˈʌbwˌɜɹd/)"),
    (r"\bGloucester\b", "[Gloucester](/ɡlˈɔstəɹ/)"),
    (r"–|—", ", "),  # en/em dashes -> a short pause
]


def to_spoken(text: str) -> str:
    for pattern, repl in LEXICON:
        text = re.sub(pattern, repl, text)
    return text


@dataclass
class Word:
    text: str
    start: float
    end: float


@dataclass
class Utterance:
    text: str
    audio_path: Path
    duration: float
    words: list[Word] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Word alignment: map display words onto TTS tokens via their letters.
# ---------------------------------------------------------------------------
def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def align_words(display_text: str, tokens: list[tuple[str, float, float]], duration: float) -> list[Word]:
    dwords = display_text.split()
    if not dwords:
        return []
    d_chars, d_owner = [], []
    for i, w in enumerate(dwords):
        for ch in _norm(w):
            d_chars.append(ch)
            d_owner.append(i)
    t_chars, t_owner = [], []
    for j, (tt, _, _) in enumerate(tokens):
        for ch in _norm(tt):
            t_chars.append(ch)
            t_owner.append(j)

    starts: list[float | None] = [None] * len(dwords)
    ends: list[float | None] = [None] * len(dwords)
    sm = difflib.SequenceMatcher(None, "".join(d_chars), "".join(t_chars), autojunk=False)
    for a, b, size in sm.get_matching_blocks():
        for k in range(size):
            wi, tj = d_owner[a + k], t_owner[b + k]
            ts, te = tokens[tj][1], tokens[tj][2]
            starts[wi] = ts if starts[wi] is None else min(starts[wi], ts)
            ends[wi] = te if ends[wi] is None else max(ends[wi], te)

    # Fill gaps (words with no letters, or unmatched) by linear interpolation.
    known = [i for i, s in enumerate(starts) if s is not None]
    if not known:
        n = len(dwords)
        return [Word(w, duration * i / n, duration * (i + 1) / n) for i, w in enumerate(dwords)]
    for i in range(len(dwords)):
        if starts[i] is None:
            prev = max((k for k in known if k < i), default=None)
            nxt = min((k for k in known if k > i), default=None)
            s = ends[prev] if prev is not None else 0.0
            e = starts[nxt] if nxt is not None else duration
            starts[i], ends[i] = s, e
    return [Word(w, float(s), float(e)) for w, s, e in zip(dwords, starts, ends)]


# ---------------------------------------------------------------------------
# Backends
# ---------------------------------------------------------------------------
_pipeline = None


def _kokoro_pipeline():
    global _pipeline
    if _pipeline is None:
        import warnings

        warnings.filterwarnings("ignore")
        from kokoro import KPipeline

        _pipeline = KPipeline(lang_code=VOICE[0], repo_id="hexgrad/Kokoro-82M")
    return _pipeline


def _synth_kokoro(spoken: str):
    import numpy as np

    pipe = _kokoro_pipeline()
    chunks, tokens, offset = [], [], 0.0
    for result in pipe(spoken, voice=VOICE, speed=SPEED):
        audio = result.audio
        if audio is None:
            continue
        audio = audio.numpy() if hasattr(audio, "numpy") else np.asarray(audio)
        for tok in result.tokens or []:
            if tok.start_ts is None or tok.end_ts is None:
                continue
            tokens.append((tok.text, offset + tok.start_ts, offset + tok.end_ts))
        chunks.append(audio)
        offset += len(audio) / SAMPLE_RATE
    audio = np.concatenate(chunks) if chunks else np.zeros(SAMPLE_RATE // 2, dtype="float32")
    return audio, tokens


def _synth_silent(spoken: str):
    import numpy as np

    plain = re.sub(r"\[([^\]]*)\]\(/[^)]*/\)", r"\1", spoken)
    words = plain.split()
    # ~2.7 words/s plus punctuation pauses, roughly matching Kokoro's pacing.
    dur = 0.4 + len(words) / 2.7 + 0.25 * len(re.findall(r"[.,;:?!]", plain))
    tokens, t = [], 0.3
    per = (dur - 0.4) / max(len(words), 1)
    for w in words:
        tokens.append((w, t, t + per))
        t += per
    return np.zeros(int(dur * SAMPLE_RATE), dtype="float32"), tokens


def _write_wav(path: Path, audio) -> None:
    import numpy as np

    pcm = (np.clip(audio, -1, 1) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(pcm.tobytes())


def synthesize(text: str) -> Utterance:
    """Return audio + word timings for ``text`` (display text, no markup)."""
    text = " ".join(text.split())
    spoken = to_spoken(text)
    key_src = json.dumps([_CACHE_VERSION, BACKEND, VOICE, SPEED, spoken])
    key = hashlib.sha1(key_src.encode()).hexdigest()[:16]
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    wav_path = CACHE_DIR / f"{key}.wav"
    meta_path = CACHE_DIR / f"{key}.json"

    if wav_path.exists() and meta_path.exists():
        meta = json.loads(meta_path.read_text())
    else:
        synth = _synth_silent if BACKEND == "silent" else _synth_kokoro
        audio, tokens = synth(spoken)
        # Atomic, process-unique temp files: parallel scene renders share this cache.
        tmp = wav_path.with_suffix(f".{os.getpid()}.tmp.wav")
        _write_wav(tmp, audio)
        tmp.replace(wav_path)
        meta = {"text": text, "spoken": spoken, "duration": len(audio) / SAMPLE_RATE, "tokens": tokens}
        tmp_meta = meta_path.with_suffix(f".{os.getpid()}.tmp.json")
        tmp_meta.write_text(json.dumps(meta, ensure_ascii=False, indent=1))
        tmp_meta.replace(meta_path)

    words = align_words(text, [tuple(t) for t in meta["tokens"]], meta["duration"])
    return Utterance(text=text, audio_path=wav_path, duration=meta["duration"], words=words)
