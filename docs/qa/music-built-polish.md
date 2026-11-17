# Music, Built: sequential polish and QA

Checkpoint: 16 November 2026. Review all 68 episodes in order, emphasizing educational clarity,
accurate explanatory visualizations and aesthetic quality. Base: `eae705a04e5ae8f9ba0a596bf960bc65f53e0075`.

Closure verification: **889 regression cases passed in 674.32 seconds**, with one upstream `audioop` deprecation warning. This run includes all shared numerical and scoring repairs; subsequent changes repaired episode presentation. Evidence: `/workspace/scratch/music-series-closure-regression.log`.

Final cross-episode audit: **Parts 1–68: 1,284 source identities and 866 fresh scene configurations verified**. Recorded sheet hashes were rechecked where available (Parts 27 onward), and every episode's sound and motion results pass. Evidence: `/workspace/scratch/music-series-audit.log`.

All **1,138 episode Python files** parsed after the final changes; `git diff --check` passed. Each episode has an individual polish commit and a linked verification record in `docs/qa/music/`.

| Part | Source and sampled-preview pass | Final narrated production |
|---|---|---|
| 1 — One String | Complete; [repair and verification record](music/part01.md) | Open |
| 2 — Waves in Air | Complete; [repair and verification record](music/part02.md) | Open |
| 3 — The Spectrum | Complete; [repair and verification record](music/part03.md) | Open |
| 4 — The Ear | Complete; [repair and verification record](music/part04.md) | Open |
| 5 — Consonance | Complete; [repair and verification record](music/part05.md) | Open |
| 6 — Tuning | Complete; [repair and verification record](music/part06.md) | Open |
| 7 — Strings, Hammers and Bows | Complete; [repair and verification record](music/part07.md) | Open |
| 8 — Pipes, Reeds and Voices | Complete; [repair and verification record](music/part08.md) | Open |
| 9 — Drums, Bars and Bells | Complete; [repair and verification record](music/part09.md) | Open |
| 10 — Writing It Down | Complete; [repair and verification record](music/part10.md) | Open |
| 11 — Rhythm and Meter | Complete; [repair and verification record](music/part11.md) | Open |
| 12 — Scales and Modes | Complete; [repair and verification record](music/part12.md) | Open |
| 13 — Intervals and Chords | Complete; [repair and verification record](music/part13.md) | Open |
| 14 — Melody | Complete; [repair and verification record](music/part14.md) | Open |
| 15 — Key | Complete; [repair and verification record](music/part15.md) | Open |
| 16 — Two Voices | Complete | Open |
| 17 — Four Voices | Complete | Open |
| 18 — Progressions | Complete | Open |
| 19 — Chromatic Harmony | Complete | Open |
| 20 — Canon and Fugue | Complete | Open |
| 21 — Form | Complete | Open |
| 22 — Analysis | Complete | Open |
| 23 — Chant to Polyphony | Complete | Open |
| 24 — The Renaissance | Complete | Open |
| 25 — The Baroque | Complete | Open |
| 26 — The Classical Style | Complete | Open |
| 27 — The Romantic Century | Complete | Open |
| 28 — New Scales, New Rhythms | Complete | Open |
| 29 — Twelve Tones | Complete | Open |
| 30 — Sound Itself | Complete | Open |
| 31 — Transformations | Complete | Open |
| 32 — The Geometry of Chords | Complete | Open |
| 33 — The Mathematics of Rhythm and Scale | Complete | Open |
| 34 — Raga and Tala | Complete | Open |
| 35 — Maqam | Complete | Open |
| 36 — Bronze and Silk | Complete | Open |
| 37 — Timelines | Complete | Open |
| 38 — Blues and Swing | Complete | Open |
| 39 — Changes | Complete | Open |
| 40 — The Song | Complete | Open |
| 41 — Orchestration | Complete | Open |
| 42 — Composing | Complete | Open |
| 43 — Performing | Complete | Open |
| 44 — Music for Picture and Play | Complete | Open |
| 45 — The Scene | Complete | Open |
| 46 — Expectation and Emotion | Complete | Open |
| 47 — Origins and Universals | Complete | Open |
| 48 — Digital Audio | Complete | Open |
| 49 — Filters, Delay and Reverb | Complete | Open |
| 50 — Dynamics, Distortion and Pitch | Complete | Open |
| 51 — Synthesis I: Oscillators and Filters | Complete | Open |
| 52 — Synthesis II: FM, Grains and Physical Models | Complete | Open |
| 53 — MIDI, Sequencers and the DAW | Complete | Open |
| 54 — Microphones and Loudspeakers | Complete | Open |
| 55 — Rooms and Space | Complete | Open |
| 56 — Recording and Mixing | Complete | Open |
| 57 — Mastering and Loudness | Complete | Open |
| 58 — Compression for the Ear | Complete | Open |
| 59 — Live Sound | Complete | Open |
| 60 — The Business of Music | Complete | Open |
| 61 — Pitch, Onsets and Transcription | Complete | Open |
| 62 — Beat, Chords and Structure | Complete | Open |
| 63 — Finding Music | Complete | Open |
| 64 — Source Separation | Complete | Open |
| 65 — Machines that Compose | Complete | Open |
| 66 — Generative Audio | Complete | Open |
| 67 — Doing Research in Music | Complete | Open |
| 68 — The Variations | Complete | Open |

Part 1: all 15 chapters rendered and visually sampled; changed sections rerendered and reviewed;
38 tests pass; the lab runs; all 15 sound-gate cases and 40 listening-window motion checks pass.
Three dense layouts also have inspected native 1080p stills. Source/data/render identities are saved locally
in `renders/qa/music1/source-receipt.json`; generated QA media are intentionally excluded from Git.

Part 2: all 14 chapter previews rendered and visually sampled; repaired sections checked again;
29 tests, the lab, 14 sound-gate cases and 18 listening-window motion checks pass. The pressure and bottle
derivations have inspected native 1080p stills. Local identities: `renders/qa/music2/source-receipt.json`.

Part 3: all 13 chapter previews rendered and visually sampled; repaired sections checked again;
30 tests, the lab, 13 sound-gate cases and 15 listening-window motion checks pass. Two dense layouts have
inspected native 1080p stills. Local identities: `renders/qa/music3/source-receipt.json`.

Part 4: all 13 chapter previews rendered and visually sampled; 31 tests, the lab, 13 sound-gate cases and
16 listening-window motion checks pass. Three native 1080p stills were inspected. The final Mask clearance
refresh was rescanned. Local identities: `renders/qa/music4/source-receipt.json`.

Part 5: twelve chapter previews reviewed; 30 tests, the lab, 12 sound-gate cases and 16 listening-window
motion checks pass. Three native 1080p stills inspected. Local identities: `renders/qa/music5/source-receipt.json`.

Part 6: twelve chapter previews reviewed; 28 tests, the lab, 12 sound-gate cases and 16 listening-window
motion checks pass. Three native 1080p stills inspected. Local identities: `renders/qa/music6/source-receipt.json`.

Part 7: twelve chapter previews reviewed; 28 tests, the lab, 12 sound-gate cases and 12 listening-window
motion checks pass. Three native 1080p stills inspected. Local identities: `renders/qa/music7/source-receipt.json`.

Part 8: twelve chapter previews reviewed; 29 tests, the lab, 12 sound-gate cases and 15 listening-window
motion checks pass. Three native 1080p stills inspected. Local identities: `renders/qa/music8/source-receipt.json`.

Part 9: twelve chapter previews reviewed; 26 tests, the lab, 12 sound-gate cases and 16 listening-window
motion checks pass. Five native 1080p stills inspected. Local identities: `renders/qa/music9/source-receipt.json`.

Part 10: twelve chapter previews reviewed; 40 tests, the lab, 12 sound-gate cases and 12 listening-window
motion checks pass. Three native 1080p stills inspected. Local identities: `renders/qa/music10/source-receipt.json`.

Part 11: twelve chapter previews reviewed; 29 tests, the lab, 12 sound-gate cases and 19 listening-window
motion checks pass. Three native 1080p stills inspected. Local identities: `renders/qa/music11/source-receipt.json`.

Part 12: twelve chapter previews reviewed; 25 tests, the lab, 12 sound-gate cases and 16 listening-window
motion checks pass. Three native 1080p stills inspected. Local identities: `renders/qa/music12/source-receipt.json`.

Part 13: thirteen chapter previews reviewed; 37 tests, the lab, 13 sound-gate cases and 27 listening-window
motion checks pass. Three native 1080p stills inspected. Local identities: `renders/qa/music13/source-receipt.json`.

Part 14: fourteen chapter previews reviewed; 25 tests, the lab, 14 sound-gate cases and 18 listening-window
motion checks pass. Three native 1080p stills inspected. Local identities: `renders/qa/music14/source-receipt.json`.

Part 15: fourteen chapter previews reviewed; 23 tests, the lab, 14 sound-gate cases and 14 listening-window
motion checks pass. Three native 1080p stills inspected. Local identities: `renders/qa/music15/source-receipt.json`.

Part 16: fourteen chapter previews reviewed; 27 tests, the lab, 14 sound-gate cases and 16 listening-window
motion checks pass. Three native 1080p stills inspected. Local identities: `renders/qa/music16/source-receipt.json`.

Part 17: fourteen chapter previews reviewed; 25 tests, the lab, 14 sound-gate cases and 14 listening-window
motion checks pass. Three native 1080p stills inspected. Local identities: `renders/qa/music17/source-receipt.json`.

Part 18: fourteen chapter previews reviewed; 22 tests, the lab, 14 sound-gate cases and 14 listening-window
motion checks pass. Four native 1080p stills inspected. Local identities: `renders/qa/music18/source-receipt.json`.

Part 19: fourteen chapter previews reviewed; 24 tests, the lab, 14 sound cases and 12 listening-window motion checks pass. Three native stills inspected. Identities: `renders/qa/music19/source-receipt.json`.

Part 20: fourteen chapter previews reviewed; 25 tests, the lab, 14 sound cases and 15 listening-window motion checks pass. Three native stills inspected. Identities: `renders/qa/music20/source-receipt.json`.

Part 21: fourteen chapter previews reviewed; 23 tests, the lab, 14 sound cases and 13 listening-window motion checks pass. Four native stills inspected. Identities: `renders/qa/music21/source-receipt.json`.

Part 22: fourteen chapter previews reviewed; 24 tests, the lab, 14 sound cases and 11 listening-window motion checks pass. Three native stills inspected. Identities: `renders/qa/music22/source-receipt.json`.

Part 23: fifteen chapter previews reviewed; 26 tests, the lab, 15 sound cases and 17 listening-window motion checks pass. Three native stills inspected. Identities: `renders/qa/music23/source-receipt.json`.

Part 24: fourteen chapter previews reviewed; 23 tests, the lab, 14 sound cases and 13 listening-window motion checks pass. Three native stills inspected. Identities: `renders/qa/music24/source-receipt.json`.

Part 25: twelve chapter previews reviewed; 22 tests, the lab, 12 sound cases and 14 listening-window motion checks pass. Three native stills inspected. Identities: `renders/qa/music25/source-receipt.json`.

Part 26: all 11 chapter preview sheets reviewed; sound and 12 listening-window motion checks pass. Local identities: `renders/qa/music26/source-receipt.json`.

Part 27: all 12 chapter preview sheets reviewed; sound and 10 listening-window motion checks pass. Local identities: `renders/qa/music27/source-receipt.json`.

Part 28: all 12 chapter preview sheets reviewed; sound and 14 listening-window motion checks pass. Local identities: `renders/qa/music28/source-receipt.json`.

Part 29: all 12 chapter preview sheets reviewed; sound and 14 listening-window motion checks pass. Local identities: `renders/qa/music29/source-receipt.json`.

Part 30: all 11 chapter preview sheets reviewed; sound and 17 listening-window motion checks pass. Local identities: `renders/qa/music30/source-receipt.json`.

Part 31: all 10 chapter preview sheets reviewed; sound and 17 listening-window motion checks pass. Local identities: `renders/qa/music31/source-receipt.json`.

Part 32: all 12 chapter preview sheets reviewed; sound and 13 listening-window motion checks pass. Local identities: `renders/qa/music32/source-receipt.json`.

Part 33: all 12 chapter preview sheets reviewed; sound and 15 listening-window motion checks pass. Local identities: `renders/qa/music33/source-receipt.json`.

Part 34: all 12 chapter preview sheets reviewed; sound and 15 listening-window motion checks pass. Local identities: `renders/qa/music34/source-receipt.json`.

Part 35: all 12 chapter preview sheets reviewed; sound and 17 listening-window motion checks pass. Local identities: `renders/qa/music35/source-receipt.json`.

Part 36: all 12 chapter preview sheets reviewed; sound and 25 listening-window motion checks pass. Local identities: `renders/qa/music36/source-receipt.json`.

Part 37: all 12 chapter preview sheets reviewed; sound and 25 listening-window motion checks pass. Local identities: `renders/qa/music37/source-receipt.json`.

Part 38: all 12 chapter preview sheets reviewed; sound and 18 listening-window motion checks pass. Local identities: `renders/qa/music38/source-receipt.json`.

Part 39: all 12 chapter preview sheets reviewed; sound and 14 listening-window motion checks pass. Local identities: `renders/qa/music39/source-receipt.json`.

Part 40: all 12 chapter preview sheets reviewed; sound and 19 listening-window motion checks pass. Local identities: `renders/qa/music40/source-receipt.json`.

Part 41: all 12 chapter preview sheets reviewed; sound and 20 listening-window motion checks pass. Local identities: `renders/qa/music41/source-receipt.json`.

Part 42: all 12 chapter preview sheets reviewed; sound and 14 listening-window motion checks pass. Local identities: `renders/qa/music42/source-receipt.json`.

Part 43: all 12 chapter preview sheets reviewed; sound and 11 listening-window motion checks pass. Local identities: `renders/qa/music43/source-receipt.json`.

Part 44: all 12 chapter preview sheets reviewed; sound and 15 listening-window motion checks pass. Local identities: `renders/qa/music44/source-receipt.json`.

Part 45: all 12 chapter preview sheets reviewed; sound and 22 listening-window motion checks pass. Local identities: `renders/qa/music45/source-receipt.json`.

Part 46: all 12 chapter preview sheets reviewed; sound and 16 listening-window motion checks pass. Local identities: `renders/qa/music46/source-receipt.json`.

Part 47: all 14 chapter preview sheets reviewed; sound and 10 listening-window motion checks pass. Local identities: `renders/qa/music47/source-receipt.json`.

Part 48: all 13 chapter preview sheets reviewed; sound and 11 listening-window motion checks pass. Local identities: `renders/qa/music48/source-receipt.json`.

Part 49: all 13 chapter preview sheets reviewed; sound and 14 listening-window motion checks pass. Local identities: `renders/qa/music49/source-receipt.json`.

Part 50: all 13 chapter preview sheets reviewed; sound and 15 listening-window motion checks pass. Local identities: `renders/qa/music50/source-receipt.json`.

Part 51: all 13 chapter preview sheets reviewed; sound and 16 listening-window motion checks pass. Local identities: `renders/qa/music51/source-receipt.json`.

Part 52: all 13 chapter preview sheets reviewed; sound and 13 listening-window motion checks pass. Local identities: `renders/qa/music52/source-receipt.json`.

Part 53: all 13 chapter preview sheets reviewed; sound and 11 listening-window motion checks pass. Local identities: `renders/qa/music53/source-receipt.json`.

Part 54: all 13 chapter preview sheets reviewed; sound and 10 listening-window motion checks pass. Local identities: `renders/qa/music54/source-receipt.json`.

Part 55: all 13 chapter preview sheets reviewed; sound and 10 listening-window motion checks pass. Local identities: `renders/qa/music55/source-receipt.json`.

Part 56: all 13 chapter preview sheets reviewed; sound and 12 listening-window motion checks pass. Local identities: `renders/qa/music56/source-receipt.json`.

Part 57: all 13 chapter preview sheets reviewed; sound and 10 listening-window motion checks pass. Local identities: `renders/qa/music57/source-receipt.json`.

Part 58: all 13 chapter preview sheets reviewed; sound and 10 listening-window motion checks pass. Local identities: `renders/qa/music58/source-receipt.json`.

Part 59: all 13 chapter preview sheets reviewed; sound and 10 listening-window motion checks pass. Local identities: `renders/qa/music59/source-receipt.json`.

Part 60: all 13 chapter preview sheets reviewed; sound and 10 listening-window motion checks pass. Local identities: `renders/qa/music60/source-receipt.json`.

Part 61: all 13 chapter preview sheets reviewed; sound and 14 listening-window motion checks pass. Local identities: `renders/qa/music61/source-receipt.json`.

Part 62: all 13 chapter preview sheets reviewed; sound and 11 listening-window motion checks pass. Local identities: `renders/qa/music62/source-receipt.json`.

Part 63: all 13 chapter preview sheets reviewed; sound and 15 listening-window motion checks pass. Local identities: `renders/qa/music63/source-receipt.json`.

Part 64: all 13 chapter preview sheets reviewed; sound and 15 listening-window motion checks pass. Local identities: `renders/qa/music64/source-receipt.json`.

Part 65: all 13 chapter preview sheets reviewed; sound and 13 listening-window motion checks pass. Local identities: `renders/qa/music65/source-receipt.json`.

Part 66: all 13 chapter preview sheets reviewed; sound and 13 listening-window motion checks pass. Local identities: `renders/qa/music66/source-receipt.json`.

Part 67: all 13 chapter preview sheets reviewed; sound and 10 listening-window motion checks pass. Local identities: `renders/qa/music67/source-receipt.json`.

Part 68: all 13 chapter preview sheets reviewed; sound and 13 listening-window motion checks pass. Local identities: `renders/qa/music68/source-receipt.json`.

**Source and sampled-preview review complete for all 68 episodes.** Every episode has its own reviewed chapter previews, passing sound and listening-window motion checks, and recorded source identities. Final narrated production, full listening and playback, synchronization, joins, and mastering remain open.

The source/preview pass is separate from final production: revised neural narration, pronunciation and
listening, complete-episode joins, measured final-film synchronization, native-resolution motion and final
mastering remain open. The source and sampled-preview pass is complete across the series; final production approval remains open.

## Round 2: bridges, sign-offs and the reading map

- **Bridges.** Every outro from Part 12 to Part 67 ends on `play_next_part` (`explainer/music/__init__.py`). It shows
  the Chain lit for this part and then the next, a kicker naming the scene the next hook opens on, the question, and
  the act strip, which marks an act boundary ("Act VI · Many Musics begins"). Fifty teasers were rewritten after
  reading the next part's hook. Every card was checked to fit the frame without shrinking the question.
- **Sign-offs.** Each part from 12 to 67 now ends on the first six seconds of its own Variation (`bridge.signoff`,
  made by `partkit.signoff` at −18 LUFS momentary), played in a captioned listening window under the next part's
  title. The next part's bead carries a halo that swells with the clip's envelope. Rendered and checked: Parts 18, 33
  (an act boundary) and 59 (a custom ending that clears its own heading). Part 63's fingerprint library leaves
  `bridge.signoff` out, since it copies audio already in the library.
- **Coverage.** `videos/music/READING.md`, written by `python -m videos.music.reading` and kept true by
  `tests/music/test_reading.py`, maps about 125 textbooks and 56 theories to the parts that teach them. The following
  were added to the reference cards and the narration where a part's subject called for them: Zwicker and the Bark
  (Part 4), Fechner (Part 4), Partch's 43 (Part 6), Piston (Part 18), Armstrong (Part 38), Gorbman and Chion (Part 44),
  Kivy and Juslin–Laukka (Part 46), Merriam and Blacking (Part 47), and Hood, Kerman, Goehr and Small (Part 67).
- **Layout fixes found on contact sheets:**
  - Part 4: the cochleagram heading sat under the sound tag.
  - Part 18: the Piston citation collided with the heading.
  - Part 6: the Partch beat now draws its 43 ratios against 12 equal steps.
  - Part 67: the "six ways of knowing" table overprinted its own columns. It is now three fixed columns, with the six
    names up from the first word.
