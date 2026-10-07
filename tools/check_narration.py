#!/usr/bin/env python
"""Listen-test the narration: transcribe every TTS line with Whisper and diff it
against the script, so mispronunciations show up as word mismatches.

    python tools/check_narration.py navier_stokes                # all lines
    python tools/check_narration.py navier_stokes --grep "Re|dy" # only lines matching a regex

Typical catches: symbols read as words ("dy" -> "die"), names, abbreviations.
Fix them with an entry in ``explainer/tts.py: LEXICON`` (or by rewording) and
re-render the affected scenes.  ASR is imperfect, so treat output as leads.
"""

from __future__ import annotations

import argparse
import difflib
import importlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.export_script import narration_by_class  # noqa: E402


def norm_words(text: str) -> list[str]:
    return re.sub(r"[^a-z0-9' ]", " ", text.lower().replace("-", " ")).split()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--grep", help="only check lines matching this regex")
    ap.add_argument("--model", default="openai/whisper-base.en")
    args = ap.parse_args()

    import numpy as np
    import soundfile as sf
    from scipy.signal import resample_poly
    from transformers import pipeline

    from explainer import tts

    manifest = importlib.import_module(f"videos.{args.video}.manifest")
    asr = pipeline("automatic-speech-recognition", model=args.model, device="cpu")
    flagged = 0
    for module, cls, _ in manifest.SCENES:
        for line in narration_by_class(ROOT / "videos" / args.video / f"{module}.py").get(cls, []):
            if args.grep and not re.search(args.grep, line):
                continue
            utt = tts.synthesize(line)
            audio, sr = sf.read(utt.audio_path)
            audio = resample_poly(audio, 16000, sr).astype(np.float32)
            heard = asr({"raw": audio, "sampling_rate": 16000}, chunk_length_s=30)["text"]
            a, b = norm_words(line), norm_words(heard)
            diffs = [
                (" ".join(a[i1:i2]), " ".join(b[j1:j2]))
                for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b).get_opcodes()
                if op != "equal"
            ]
            if diffs:
                flagged += 1
                print(f"[{cls}] {line[:90]}...")
                for said, heard_ in diffs:
                    print(f"    script: {said!r:<28} heard: {heard_!r}")
    print(f"\n{flagged} line(s) with differences (many are harmless ASR spelling variants).")


if __name__ == "__main__":
    main()
