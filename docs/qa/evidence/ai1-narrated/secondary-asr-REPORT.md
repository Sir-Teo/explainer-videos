# Independent secondary ASR: Information chapter

**Whisper agrees with the scripted millionths and minus wording.** The existing server-ASR “millions” lead was not reproduced by this independent recognizer. This is automated recognition evidence, not manual hearing or a pronunciation/production sign-off.

Decoded the exact corrected stress probe plus **all six current Information clips** using the official public `openai/whisper-base.en` model, pinned to revision `911407f4214e0e1d82085af863093ec0b66f9cd6`. Execution followed root's explicit confirmation that the TTS server had stopped; no TTS synthesis or narration edits occurred.

## Observed text

| Input | Secondary ASR wording |
|---|---|
| Stress probe, 9.75s | “7.32 millionths of a bit” and “minus 0.69 millionths of a bit” |
| Information block 2 | 4.08, 3.33, 0.75, 1.36 and 0.27 bits appear as expected |
| Information block 4 | “Of the 0.75 bits, 0.35 survive” |
| Information block 5, 37.68s | 1,000 letters; 7.32 **millionths**; **minus** 0.69 millionths. The overlapping20–37.68s window repeats the negative control value correctly. |
| Information block 6 | 20 to1,000 letters; the descriptive-fit/finite-measurement qualifications and Part13 callback remain in the raw transcripts |

Probe transcript (no expected-text decoder prompt):

> At 1000 letters, the corrected estimate is about 7.32 millionths of a bit. One shuffled version gives about minus 0.69 millionths of a bit.

Block5, 0–30s transcript:

> How far back does that reach? Measure pairs of letters at distance D across our books. These are finite sample estimates with an approximate bias correction. The neighboring letter estimate is 0.75 bits. At our largest measured distance, 1,000 letters, the corrected estimate is about 7.32 millionths of a bit. One shuffled version of the same letters gives about minus 0.69 millionths of a bit. The shuffled control is a reference realization, not an uncertainty interval.

All raw windows for all seven inputs remain in `transcripts.json`; `comparison.json` records the explicit numeric/unit term comparisons. Blocks1 and3 were also decoded; neither introduced a numeric/unit concern in the text comparison. Punctuation, capitalization, neighboring/neighbouring spelling and digit formatting vary without a detected meaning change. No transcript was manually substituted for recognizer output.

## Reproducibility and provenance

- CPU float32, **one Torch thread**, greedy decoding, `num_beams=1`, no source-text prompt. The model's normal English control-token configuration was retained.
- Source WAVs were resampled to mono16kHz only in `/workspace/runtime/asr-second/`, leaving cached input WAVs unchanged.
- Thirty-second windows use a20s stride (10s overlap); raw window transcripts are deliberately retained separately. Window boundaries are not word-alignment measurements.
- Inference finished in **58.8s**, with peak process RSS **800,668KiB** (about782MiB). The inference process exited normally.
- Stress-probe audio SHA-256: `0bae80b96b25a3b2b9567dd654246da6338b715d091567cf2bd96301474ce8f6`.
- Block5 audio SHA-256: `a1c84134b80ec1acd76ba4f3c98f18a4b5ea5d44b1949d67d142a7bea09c9119`.
- Every source audio hash matched again after decoding. The source `audio_result.json` path and hash at execution time, each input filename/hash, per-window durations/transcripts, pinned model revision, script hash and memory snapshots are retained in `transcripts.json`.
- `download-manifest.json` records the official model/config URLs and hashes; only one weight format was fetched,294,340,404bytes total. The model tensor file matches official Hub LFS SHA-256 metadata.

Run after the TTS-stop/memory handoff:

```bash
source /workspace/runtime/activate.sh
PYTHONDONTWRITEBYTECODE=1 python /workspace/runtime/asr-second/transcribe.py --tts-stopped-confirmed --all-information
```

Existing server ASR heard “millions”; Whisper heard “millionths”. That disagreement supports retaining the server result as a review lead rather than treating it as a confirmed speech defect. ASR agreement still cannot prove unambiguous pronunciation to a human. No manual listening, speech-content approval, word-level alignment, narrated-video synchronization, Chinese coverage, or full playback QA was performed. Repository narration, caches and QA statuses were not changed.
