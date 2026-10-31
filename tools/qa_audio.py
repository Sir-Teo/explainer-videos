#!/usr/bin/env python
"""Synthesize and inspect actual narration lines captured by qa_series.py.

Requires the documented TTS server. This checks signal/timing integrity;
the server checks speech recognition. Listening and narrated playback remain
separate production checks. Results retain the exact narration and input hash.
"""

import argparse
import hashlib
import importlib
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("video")
    ap.add_argument("--lang", choices=("en", "zh"), default="en")
    ap.add_argument("--only", nargs="+")
    args = ap.parse_args()
    os.environ.update(EXPLAINER_LANG=args.lang, EXPLAINER_VIDEO=args.video)
    os.environ.setdefault("EXPLAINER_TTS", "server")
    os.environ.setdefault("EXPLAINER_VOICE", "qwen3-calm-a")
    import numpy as np
    import soundfile as sf
    from explainer import lang, tts
    from explainer.paths import video_package
    from explainer.voiceover import _strip_bookmarks
    from tools.qa_series import OUT, fingerprint, inputs_current

    manifest = importlib.import_module(f"{video_package(args.video)}.manifest")
    for _, scene, _ in manifest.SCENES:
        if args.only and scene not in args.only:
            continue
        candidates = [OUT / args.video / "en" / name / "result.json" for name in (scene, scene + "_motion")]
        records = [(p, json.loads(p.read_text())) for p in candidates if p.exists()]
        records = [(p, d) for p, d in records if d.get("status") == "passed" and d.get("narration")]
        if not records:
            print(f"{args.video} {scene}: no successful English narration capture", flush=True)
            continue
        p, evidence = max(records, key=lambda pair: pair[0].stat().st_mtime_ns)
        report = {"video": args.video, "scene": scene, "lang": args.lang,
                  "backend": tts.BACKEND, "voice": tts.VOICE,
                  "input_record": str(p.relative_to(ROOT)),
                  "input_sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                  "source_current": evidence.get("fingerprint") == fingerprint(args.video)
                                    and inputs_current(evidence),
                  "scope": "signal and alignment integrity; listening and narrated playback pending",
                  "expected_lines": len(evidence["narration"]), "lines": [], "issues": []}
        target = OUT / args.video / args.lang / scene / "audio_result.json"
        target.parent.mkdir(parents=True, exist_ok=True)

        def save():
            temp = target.with_suffix(".tmp.json")
            temp.write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n")
            temp.replace(target)

        save()
        for i, line in enumerate(evidence["narration"]):
            raw = line["raw"]
            spoken, _ = _strip_bookmarks(lang.translate(raw, ROOT / "videos" / "ai" / args.video, scene))
            start = time.monotonic()
            try:
                utterance = tts.synthesize(spoken)
                samples, sr = sf.read(utterance.audio_path)
                duration = len(samples) / sr
                issues = []
                if not len(samples) or not np.isfinite(samples).all() or not np.any(samples):
                    issues.append("empty, silent or non-finite waveform")
                if abs(duration - utterance.duration) > max(0.05, 2 / sr):
                    issues.append("waveform and metadata duration disagree")
                tokens = utterance.words
                if not tokens:
                    issues.append("no aligned tokens")
                previous = -1.0
                for token in tokens:
                    begin, end = token.start, token.end
                    if not (0 <= begin <= end <= duration + 0.05) or begin + 0.02 < previous:
                        issues.append("invalid or non-monotonic token alignment")
                        break
                    previous = begin
                result = {"raw": raw, "spoken": spoken, "audio_path": str(utterance.audio_path),
                          "duration": duration, "tokens": len(tokens),
                          "peak": float(np.abs(samples).max()) if len(samples) else 0,
                          "issues": issues, "elapsed": round(time.monotonic() - start, 2)}
                # ASR mismatches are review leads, separate from waveform and
                # alignment checks. They include harmless number spellings but
                # can also expose a mispronounced model or mathematical term.
                qa_log = tts.CACHE_DIR / "qa.jsonl"
                actual_spoken = tts.cache_key(spoken)[1]
                leads = {}
                if qa_log.exists():
                    for entry in qa_log.read_text().splitlines():
                        try:
                            candidate = json.loads(entry)
                        except json.JSONDecodeError:
                            continue  # a server may be appending its next lead
                        if (candidate.get("lang") == args.lang and candidate.get("voice") == tts.VOICE
                                and candidate.get("text") and candidate["text"] in actual_spoken):
                            leads[candidate["text"]] = candidate
                result["asr_review_leads"] = list(leads.values())
                report["lines"].append(result)
                report["issues"].extend({"line": i, "issue": issue} for issue in issues)
                print(f"{args.video} {args.lang} {scene} {i + 1}/{len(evidence['narration'])}: "
                      f"{duration:.1f}s, {len(issues)} signal/timing issues", flush=True)
            except Exception as error:
                report["issues"].append({"line": i, "issue": repr(error)})
                save()
                raise
            save()


if __name__ == "__main__":
    main()
