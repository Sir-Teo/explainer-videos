#!/usr/bin/env python
"""Score narration audio for naturalness and intelligibility.

    python tools/score_voice.py samples/*.wav --text lines.json
    python tools/score_voice.py renders/llm.mp4 --clips 6       # spot-check a finished video

* Naturalness: UTMOSv2 (sarulab-speech/UTMOSv2 on Hugging Face), the
  VoiceMOS 2024 winner, predicts a 1-5 mean opinion score per file.
* Intelligibility (needs ``--text``, a JSON list indexed by the trailing
  number in each file name, e.g. ``voice_3.wav`` -> entry 3): word error
  rate of a Whisper transcription (openai/whisper-small.en) against the script.
* ``--clips N`` cuts N evenly spaced 12 s clips out of a video and scores them,
  to check the final mixed, compressed soundtrack.

UTMOSv2 pins its own torch/torchvision versions, so run this from a separate
environment (it is not a dependency of the render pipeline):

    uv venv .venv-eval && source .venv-eval/bin/activate
    uv pip install --index-url https://download.pytorch.org/whl/cpu torch==2.8.0 torchvision==0.23.0 torchaudio==2.8.0
    uv pip install git+https://github.com/sarulab-speech/UTMOSv2.git soundfile scipy
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import tempfile
import warnings
from collections import defaultdict
from pathlib import Path

warnings.filterwarnings("ignore")


def norm_words(t: str) -> list[str]:
    return re.sub(r"[^a-z0-9' ]", " ", t.lower().replace("-", " ")).split()


def wer(ref: str, hyp: str) -> float:
    import numpy as np

    r, h = norm_words(ref), norm_words(hyp)
    d = np.zeros((len(r) + 1, len(h) + 1), dtype=int)
    d[:, 0], d[0, :] = range(len(r) + 1), range(len(h) + 1)
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            d[i, j] = min(d[i - 1, j] + 1, d[i, j - 1] + 1, d[i - 1, j - 1] + (r[i - 1] != h[j - 1]))
    return d[-1, -1] / max(1, len(r))


def video_clips(video: Path, n: int, tmp: Path, length: float = 12.0) -> list[Path]:
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                str(video)], check=True, capture_output=True, text=True).stdout)
    out = []
    for k in range(n):
        t0 = (k + 0.5) * dur / n
        f = tmp / f"{video.stem}_clip_{k}.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.2f}", "-t", str(length), "-i", str(video),
                        "-vn", "-ac", "1", "-ar", "24000", str(f)], check=True)
        out.append(f)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", type=Path)
    ap.add_argument("--text", type=Path, help="JSON list of reference transcripts (enables WER)")
    ap.add_argument("--clips", type=int, default=0, help="score N clips of each input video")
    args = ap.parse_args()

    import numpy as np
    import soundfile as sf
    import torch
    import utmosv2
    from scipy.signal import resample_poly

    torch.set_num_threads(4)
    refs = json.loads(args.text.read_text()) if args.text else None
    asr = None
    if refs is not None:
        from transformers import pipeline

        asr = pipeline("automatic-speech-recognition", model="openai/whisper-small.en", device="cpu")
    mos_model = utmosv2.create_model(pretrained=True, device="cpu")

    with tempfile.TemporaryDirectory() as tmpdir:
        files: list[Path] = []
        for p in args.inputs:
            files += video_clips(p, args.clips, Path(tmpdir)) if args.clips else [p]
        groups = defaultdict(list)
        for f in files:
            mos = float(mos_model.predict(input_path=str(f), device="cpu", num_workers=0))
            row = {"mos": mos}
            if asr is not None:
                audio, sr = sf.read(f)
                audio = audio.mean(1) if audio.ndim > 1 else audio
                heard = asr({"raw": resample_poly(audio, 16000, sr).astype(np.float32), "sampling_rate": 16000},
                            chunk_length_s=30)["text"]
                row["wer"] = wer(refs[int(f.stem.rsplit("_", 1)[1])], heard)
            groups[f.stem.rsplit("_", 1)[0]].append(row)
            print(f"{f.stem:<32} MOS {mos:.2f}" + (f"  WER {row['wer']:.3f}" if "wer" in row else ""), flush=True)

    print(f"\n{'system':<32} {'MOS':>5}  {'WER':>6}")
    for name, rows in sorted(groups.items(), key=lambda kv: -np.mean([r["mos"] for r in kv[1]])):
        w = f"{np.mean([r['wer'] for r in rows]):.3f}" if "wer" in rows[0] else "-"
        print(f"{name:<32} {np.mean([r['mos'] for r in rows]):5.2f}  {w:>6}")


if __name__ == "__main__":
    main()
