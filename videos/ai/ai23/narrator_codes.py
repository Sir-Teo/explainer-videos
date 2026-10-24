"""The narrator's own codes: run by ``.venv-tts/bin/python`` (which has ``qwen_tts``), never imported by the part.

    .venv-tts/bin/python videos/ai/ai23/narrator_codes.py OUT.npz REF.wav "REF TEXT" "SENTENCE" [--no-generate]

Qwen3-TTS-12Hz (the series' narrator) turns sound into 16 codes every 80 ms with its speech tokenizer.  This script
(1) encodes the clip the narrator clones its English voice from, and decodes the codes back to sound; (2) unless
``--no-generate``, has the narrator say SENTENCE in that voice (as tools/tts_server.py does) and keeps the codes its
talker wrote.  Everything is saved to OUT.npz; Part 23's compute step (``compute_narrator``) calls this and caches the
result, and does without it when ``.venv-tts`` or the model is missing.
"""

from __future__ import annotations

import glob
import os
import sys
import time
import warnings

warnings.filterwarnings("ignore")


def main():
    import numpy as np
    import soundfile as sf
    import torch
    from scipy.signal import resample_poly

    out, ref, ref_text, sentence = sys.argv[1:5]
    generate = "--no-generate" not in sys.argv
    torch.set_num_threads(int(os.environ.get("AI23_THREADS", "2")))
    torch.manual_seed(0)
    hub = os.environ.get("HF_HOME", os.path.expanduser("~/.cache/huggingface"))
    snaps = sorted(glob.glob(os.path.join(hub, "hub", "models--Qwen--Qwen3-TTS-12Hz-1.7B-Base", "snapshots", "*")))
    if not snaps:
        sys.exit("Qwen3-TTS-12Hz-1.7B-Base is not in the Hugging Face cache")
    snap = snaps[-1]
    from qwen_tts import Qwen3TTSTokenizer

    a, sr = sf.read(ref, dtype="float32")
    a = a.reshape(len(a), -1).mean(1)
    res = {}
    t = time.time()
    tok = Qwen3TTSTokenizer.from_pretrained(os.path.join(snap, "speech_tokenizer"), device_map="cpu")
    enc = tok.encode(a, sr=sr)
    codes = enc.audio_codes[0].cpu().numpy()
    wavs, osr = tok.decode(enc)
    res["ref_codes"] = codes.astype(np.int16)
    res["ref_wav"] = (np.clip(resample_poly(a.astype(np.float64), 16000, sr), -1, 1) * 32767).astype(np.int16)
    res["dec_wav"] = (np.clip(resample_poly(np.asarray(wavs[0], np.float64), 16000, osr), -1, 1) * 32767).astype(np.int16)
    print(f"encoded {len(a) / sr:.1f} s into {codes.shape} codes in {time.time() - t:.0f} s", flush=True)
    del tok
    if generate:
        from qwen_tts import Qwen3TTSModel

        t = time.time()
        m = Qwen3TTSModel.from_pretrained(snap, device_map="cpu", dtype=torch.bfloat16)
        seen = {}
        inner = m.model.generate

        def capture(*args, **kw):
            r = inner(*args, **kw)
            seen["codes"] = r[0][0].detach().cpu().numpy()
            return r

        m.model.generate = capture
        torch.manual_seed(0)
        wavs, osr = m.generate_voice_clone(text=[sentence], language=["English"], ref_audio=ref, ref_text=ref_text,
                                           temperature=0.7, max_new_tokens=int((len(sentence) / 8 + 3) * 12))
        w = np.asarray(wavs[0], np.float64).reshape(-1)
        res["gen_codes"] = seen["codes"].astype(np.int16)
        res["gen_wav"] = (np.clip(resample_poly(w, 16000, osr), -1, 1) * 32767).astype(np.int16)
        res["gen_seconds"] = np.array(time.time() - t)
        print(f"said {sentence!r}: {res['gen_codes'].shape} codes, {len(w) / osr:.1f} s, in {time.time() - t:.0f} s",
              flush=True)
    np.savez_compressed(out, **res)


if __name__ == "__main__":
    main()
