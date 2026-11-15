# Part 10 — Writing It Down

Review date: 15 November 2026. Base: `eb358b82`. Source and sampled-preview review complete; final production remains open.

## Changes

- Identify the tablet as a schematic, fit its terms inside the drawing, qualify disputed interpretations and
  replace universal claims about historical chant training with the relevant oral-practice context.
- Identify the three-sign neume display as a contour toy. Distinguish code-length budgets from the information
  in historical notation, and qualify Guido's role in consolidating staff practice.
- Distinguish event order and diatonic staff position from uniform elapsed time and acoustic frequency.
  Qualify historical notation timelines and distinguish later mensuration practices from Franco's shapes.
- Correct the claim that binary values replaced all triple groupings. Explain that no finite binary sum
  equals one third. Qualify partbook/score history and the development of tempo and dynamic instructions.
- Correct Seeger's descriptive/prescriptive distinction: staff scores and tablature can both prescribe
  performance. Identify the displayed staff as sounding pitch and the fingering metric as travel cost.
  Disclose the octave-shifted bass in the piano rolls; qualify figured-bass defaults and chart analogies.
- Scope gongche mappings and jianpu tonic conventions; correct the C-to-F diatonic displacement. Restore
  `1 = C` after the transposition example so the following C audio agrees with the displayed notation.
  Qualify guqin timing conventions and Cardew's lack of a fixed symbol-to-sound key.
- Distinguish the 1983 MIDI protocol from later Standard MIDI Files, and nine-byte example events from a
  fixed per-note cost. Acknowledge controllers, bends, tuning, lyrics and key metadata; distinguish this
  reader's losses from the format's capabilities. Scope enharmonic pitch differences to the meantone model.
- Identify MusicXML 1.0's 2004 release as a milestone, not the format's origin. Describe structured notation
  and implementation-specific round trips rather than preservation of identical rendered pages.
- Correct the waveform format to 48 kHz mono PCM16, rather than CD audio. Present the symbolic codes as
  illustrative budgets with shared vocabulary/decoder assumptions; distinguish them from lossless waveform
  compression. Scope codec ratios to the selected bitrates and identify both performance examples as synthetic.
- Clarify the illustrative performance budget's quantization and ranges. Fix the onset-resolution comment
  (the original ±64 ms range did not cover the approximately 69 ms example); waveforms and counts unchanged.
- Scope the OMR toy's blob/duration rules, label accuracy as a fraction and remove the artificial curve
  offset. Explain flipped-pixel errors; qualify real-system performance, metrics and standards claims.
- Align the recap with what the chosen score examples leave implicit; MIDI and notation encodings can record
  many performance details when supplied. Qualify subjective grouping in the transition to Part 11.

## Verification

Numerical items generated. Numerical payloads and waveforms unchanged; `compute.py` changes a budget comment.

- Chapter/notation/score/performance/audio/loader tests: **40 passed**, one `audioop` deprecation warning;
  `/workspace/scratch/music10-final-tests.log`.
- `python -m videos.music.labs 10`: passed; `/workspace/scratch/music10-lab.log`.
- Three native 1920×1080 stills inspected: MIDI event decoding, code-length comparison and jianpu layout;
  `/workspace/scratch/music10-native/images/music10_native/`.
- All twelve full chapter previews rendered and their 48-sample contact sheets inspected. Hook, Mensural,
  Tab, East and Frontier refreshes were reviewed. No chapter source postdates its final render.
- Sound gate: **12 scenes, zero failures**; `/workspace/scratch/music10-final-sound.log`.
- Motion gate: **12 scenes, 12 listening windows, zero failures**, at 4 fps; no blank/sparse runs ≥1.5 s
  or still-listening runs ≥2.5 s. `/workspace/scratch/music10-motion-results.json`.
- Source/movie/cue identities: `renders/qa/music10/source-receipt.json`; silent-narration previews total
  **49.99 minutes**.
- Source-based narration estimate: 40.9 minutes, including 3.4 minutes of listening; not final runtime.

## Production gates still open

Regenerate changed narration, inspect pronunciation and continuous listening/playback, measure final-film
alignment, and check complete-episode joins, native motion and mastering. No publication was performed.
