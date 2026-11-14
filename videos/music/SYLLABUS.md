# Music, Built: the syllabus (plan of record, draft 1)

Goal: a music education in video, from the first lesson to the research frontier and into the industry. It aims to
be **as complete as a conservatory and a music-technology degree together, as technical as a graduate seminar, as
practical as a working engineer's or arranger's knowledge, and as close to the frontier as primary sources allow**.
It is made to the standard of *Computer Science, Built* and renders on macOS and Linux. Each part runs **30–60
minutes** and its content decides where in that range it lands. Sixty-eight parts come to about **50 hours**.

The plan has the shape of several degrees laid end to end:
- **Act I** is a course in musical acoustics and psychoacoustics (Benade; Fletcher & Rossing; Hartmann; Moore;
  Sethares).
- **Acts II and III** are the undergraduate theory sequence, fundamentals through chromatic harmony, counterpoint,
  form and analysis (Aldwell & Schachter; Laitz; Fux; Gauldin; Caplin; Hepokoski & Darcy; Lerdahl & Jackendoff),
  with the ear-training sequence run inside every part (§1).
- **Act IV** is the music-history survey (Burkholder, Grout & Palisca; Taruskin), told as technical problems.
- **Act V** is post-tonal theory and the graduate course in mathematical music theory (Straus; Forte; Lewin;
  Cohn; Tymoczko; Toussaint; Amiot).
- **Act VI** is world music and ethnomusicology, jazz theory, and popular-music studies (Nettl; Agawu; Levine;
  Temperley; Ohriner).
- **Act VII** is the composer's and performer's training: orchestration (Adler), composition, performance science,
  media scoring (Collins; Lehman).
- **Act VIII** is the graduate course in music cognition (Huron; Patel; Krumhansl; Bregman; Deutsch).
- **Act IX** is the music-technology and audio-DSP core (Roads; Smith's four online books; Zölzer; Välimäki;
  Bilbao; Puckette).
- **Act X is the industry curriculum** of an audio-engineering or Tonmeister degree and a music-business
  programme: transducers, rooms, recording, mixing, mastering, coding, live sound, rights and money (Kuttruff;
  Beranek; Izhaki; Katz; Bosi & Goldberg; McCarthy; Passman; Krueger).
- **Act XI** is the graduate course in music information retrieval and generative modelling (Müller; Lerch; the
  ISMIR literature).
- **The research tier** runs through the whole series: every part closes its content with a *Frontier* chapter
  (§1.1), and Part 67 is about how each kind of music research is done.

§2.5 maps the series onto degree programmes and onto the jobs people do with them.

## 1. The standard every part meets

The standard is *AI, Built*'s ([`../ai/SYLLABUS.md`](../ai/SYLLABUS.md) §1 and
[`../ai/LECTURE_GUIDE.md`](../ai/LECTURE_GUIDE.md)) with *Computer Science, Built*'s additions
([`../cs/SYLLABUS.md`](../cs/SYLLABUS.md) §1), plus the rules specific to a series that makes sound, marked **(M)**.

**A part is a story.** It opens on a hook: a question, a failure, a famous night, a sound that should not be
possible. It closes on the answer and on the question the next part takes up. Each part below states its story.
A chapter that does not serve the story is cut, or moved to the part it serves. The stories are chosen so that a
viewer who is not a student stays: a court case, a hoax, a prince with an abacus, a pianist who falters on take
one.

**A chapter is a lecture segment of 3–5 minutes**, in this order:

1. A motivating question, sound or failure.
2. A definition card.
3. The derivation on screen, every step, each with a margin reason.
4. A computed experiment or a run of the thing we built, **(M)** heard as well as seen.
5. A worked example or a *pause-and-listen* question.
6. The takeaway, with a forward link.

**Per part:**
- An objectives card.
- Definition, theorem and algorithm cards; code from the repository is excerpted and highlighted as it runs.
- **(M) The ear thread.** Three to six *pause-and-listen* questions per part, graded in difficulty across the
  series the way an aural-skills sequence is: which is higher, which interval, which chord quality, which
  inversion, which cadence, which mode, where the modulation is, which microphone, which compressor setting,
  which bitrate. The answer is always shown as a picture after the pause. The part's interactive on the course
  site drills the same skill with fresh examples.
- **(M) The Variation.** One variation on the Tune (§2.2), 20–60 seconds, written with what the part taught, played
  in full near the end with its score and its ledger row.
- A problem set: 4–6 problems, about 90 s on screen, full solutions in the part's README. At least one is an
  *ear* problem (answered by listening to a file the lab renders), one is a *build* problem against Monochord
  ("add a fourth string to the piano model's unison and measure the double decay"), and one is a research
  problem (★).
- A reference card: textbooks, classic papers, frontier papers, and for repertoire the edition used.
- An *In practice* card in the outro: the jobs, tools and skills the part maps to.
- A *Frontier* chapter before the outro (§1.1).

**The history thread.**
- Every part opens with its era, lit on the timeline strip.
- Every idea is credited with its people and year, its dead ends included: the music of the spheres, the 22
  equal shruti, the Telharmonium, quadraphonic sound, DAT, MQA.
- **(M)** Traditions outside the Western conservatory are taught from their own theory and their own scholars,
  with the terms of the tradition, and each such part is checked against primary sources and recent
  ethnomusicology in its frontier sweep. Variations written in a tradition's idiom are labelled as studies.

**Frontier sweep.** Before a part is written, its literature is checked against primary sources up to the writing
date. Recent or uncertain facts this plan relies on are marked **(verify)** and must be checked before they go on
screen. Industry facts (prices, loudness targets, royalty rates, product behaviour, court outcomes) are dated on
screen ("as of …") and, for law, given with their jurisdiction.

**Numbers are real.** As in the other series: computed numbers come from the part's `compute.py`, cached under
`.cache/musicN/`; published numbers are cited; schematics are labelled `schematic` and made-up examples
`illustrative`. Narration that states a result is an f-string over the data and branches on the computed verdict.
CPU budget: ≤ 2 h per part by default, seeded and resumable; the named exceptions are listed per part.

**(M) Sounds are real.**
- Every sound is produced by Monochord in the part's `compute.py`, seeded, cached as a 48 kHz float WAV under
  `.cache/musicN/audio/`, and addressed by name. A scene never synthesizes sound itself and never loads audio from
  outside the cache.
- Every sound carries a label on screen when it first plays: `physical model`, `synthesized`, `rendered from the
  score (edition)`, or `recording (source, licence)` for the few measured references the Library holds.
- A claim about how a real instrument sounds is checked against a measured reference in `tests/music/` (partial
  frequencies, inharmonicity, odd-even balance, spectral centroid, decay times), with tolerances.
- No third-party recording is played as music, and no copyrighted composition is performed (§2.4).
- Levels are content. A demonstration of +6 dB is +6 dB in the master (§3). Sounds that are loud, harsh or
  piercing are announced on screen two seconds before they play, and nothing exceeds the series' peak ceiling.

**(M) See what you hear.**
- While a sound plays, a picture locked to it is on screen, drawn from the same sample buffer or the same event
  list. `tools/dead_air.py` gains the converse check: no sound over an empty or static screen.
- Every argument made by ear is also made by eye (a difference signal, a measured curve, a count), so the film is
  followable on a phone speaker and with the sound off, and the subtitles describe each example.
- A demonstration that depends on the playback chain says so: `headphones` for binaural and stereo effects,
  `needs bass` for content below 100 Hz, `your platform's codec applies` for differences near transparency. The
  phone-speaker audition of §3 is run on every part.

**Bilingual standard** (subject to §9): as *Computer Science, Built*. The glossary `MUSIC_ZH_GUIDE.md` fixes
note names, solfège and terms (音程, 和弦, 对位, 十二平均律, 泛音, 混响, 响度, 采样定理, …); score text and code are not
translated.

**Gates per part:** `tools/lecture_length.py` (floor 30, ceiling 60; it must count listening windows, §3),
`contact_sheet.py`, `dead_air.py` in both directions, the audio gates of §3, `collect_text.py --check`,
`check_narration.py`, the part's `tests/music/test_musicN_*.py`, and `tools/check_course.py music N`.

### 1.1 The research tier

Every part ends its content with a **Frontier** chapter (4–8 minutes) at the level of a qualifying exam or a
first-year graduate seminar. It does four things, as in *Computer Science, Built*:

1. **The limit.** What is the best possible, and how close is the state of the art? Computed where we can: an
   oracle mask's separation score beside our separator's, the Gabor limit beside a listener's measured acuity,
   the entropy of a corpus beside a model's cross-entropy.
2. **What is open**, stated precisely, with the current record and its date.
3. **Recent papers**: two or three, with what each changed, checked in the frontier sweep.
4. **A research problem (★)** in the problem set, with what is known, how one would attack it, and which module of
   Monochord is the place to start.

Each part's Frontier topic is given in §5. Part 67 collects the ★ problems into the map of open problems.

## 2. The devices

### 2.1 Monochord, the instrument we build

Monochord lives in `explainer/music/monochord/`. It is tested Python on numpy and scipy, with numba where a loop is
hot (it is already a dependency) and torch only for the neural layers of Act XI. Nothing in it imports manim, so
the labs can use all of it. Each layer is built in the part that teaches it and checked against something that does
not share its code.

| Layer | Module | Built in | Checked against |
|---|---|---|---|
| Strings, tubes, membranes, bars by finite differences; modal synthesis | `physics/` | 1, 2, 7–9 | d'Alembert and Fourier solutions; Bessel zeros; energy conservation; Mersenne's laws |
| STFT, constant-Q, windows, resampling, filters | `dsp/` | 3, 48, 49 | `scipy.signal`; Parseval; analytic transforms |
| Gammatone cochlea, loudness, masking, roughness, pitch models | `ear/` | 4, 5, 45 | ISO 226 contours; published Plomp–Levelt and masking data; the missing-fundamental result |
| Pitch, intervals, tunings and temperaments, the tuning lattice | `pitch.py`, `tuning.py` | 6 | exact rational arithmetic; published cent tables |
| The score: spelled pitches, exact rational durations, voices; readers and writers; the engraver bridge | `score/` | 10 | round trips through MusicXML/MEI and MIDI; published examples |
| Rhythm, meter, scales, chords, keys | `theory/` | 11–15 | enumeration against Burnside counts; key finding against the *Well-Tempered Clavier*'s titles |
| Counterpoint and voice-leading checkers, harmonizer, figured-bass realizer, canon solver, form and grammar tools | `voices/` | 16–25 | brute force on small cases; Bach's chorales as held-out data |
| Sets, rows, the T/I and PLR groups, orbifolds, minimal voice leading, DFT of chords, Euclidean rhythms, tilings, temperaments as lattices | `math/` | 28–33 | brute-force group tables; published set-class and row counts |
| Idiom modules: tala and tihai, maqam and jins in cents, gamelan cycles and interlocking, timelines, swing, changes | `idioms/` | 34–40 | published measurements and treatises, cited per item |
| Instruments: plucked, struck and bowed strings, reeds, brass, flute, voice, percussion, bronze | `instruments/` | 7–9, 36 | measured spectra and decay times from the Library's references |
| The performer: expressive timing, dynamics, vibrato, ensemble asynchrony | `perform/` | 43 | published timing profiles; the phase-correction model's stability bounds |
| Oscillators, filters, envelopes, modulation, FM, grains, waveguides, samplers | `synth/` | 51, 52 | alias levels measured; Bessel sideband amplitudes; analog prototypes' responses |
| Effects: EQ, delay, reverb, dynamics, distortion, pitch and time | `fx/` | 49, 50 | `scipy.signal`; closed-form static curves; energy decay against Sabine |
| The sequencer and audio graph; MIDI files; a pattern language | `seq/` | 53 | the MIDI specification's examples; bit-identical offline and block renders |
| Microphones, loudspeakers, rooms, spatial rendering | `studio/` | 54, 55 | closed-box alignments; rectangular-room modes; Sabine and Eyring; a spherical-head model |
| The mixer, the mastering chain, loudness and true-peak meters | `mix/`, `master/` | 56, 57 | pan-law power sums; ffmpeg's `ebur128` readings to 0.1 LU |
| Codecs: a lossless coder, a perceptual MDCT codec, a residual vector quantizer | `codec/` | 58 | bit-exact round trips; perfect reconstruction of the MDCT to machine precision |
| The PA: arrays, feedback loops, RF planning | `live/` | 59 | closed-form array factors; the Nyquist criterion |
| The listeners: f0, onsets, transcription, beat, alignment, chords, structure, fingerprints, recommendation, separation | `mir/` | 61–64 | Monochord's own ground truth; optional independent references in tests (`librosa`, `mir_eval`) |
| The generators: Markov models, a small transformer, a DDSP instrument, a token model | `gen/` | 65, 66 | held-out likelihood; memorization tests; the analyzers of Acts II–III as critics |

Two properties make Monochord more than a prop. **It supplies its own ground truth**: a transcriber, a separator
or a beat tracker is tested on audio whose score, stems and beat times are known exactly, as *Statistics, Built*
tests methods on a World whose truth is known. **It is the series' orchestra**: every instrument heard in Part 68
was derived on screen.

### 2.2 The Tune and the Variations

**The Tune** is *Ah! vous dirai-je, maman* (anonymous, France; first published 1761 **(verify)**), known as
*Twinkle, Twinkle, Little Star*, the alphabet song and *Baa, Baa, Black Sheep*, and the theme of Mozart's
twelve variations K. 265 (1781–82). It was chosen because:
- nearly every viewer in every country can already sing it, so every transformation is audible as a change;
- it is in the public domain everywhere;
- it opens on a rising perfect fifth (the 3:2 of Part 1) and then walks down the scale from the fifth degree to
  the tonic, so it is an interval, a scale and a cadence in twelve bars;
- it is a rounded ternary form with a harmonization any first-year student can write and any later part can
  complicate;
- variation on it is a tradition (Mozart, Dohnányi, generations of piano students), which Part 26 meets head on.

**The Variations** (`explainer.music.variations`, `.cache/music*/variations.json`): each part adds one row.

| Row | Part | The Tune … |
|---|---|---|
| 1–9 | Act I | on one simulated string; on tuned bottles; built from partials; without fundamentals; in parallel intervals that are consonant only for a bent timbre; in eight temperaments; for plucked, struck and bowed strings; for winds and a voice; on bars and bells |
| 10–15 | Act II | in ten notations; in five meters; in every mode; in block chords and re-voiced; ornamented and inverted by a model of surprise; modulating round the circle |
| 16–22 | Act III | as a cantus firmus in five species; as a chorale; over ground basses; reharmonized chromatically; as a round, a crab canon and a fugue exposition; as a miniature sonata; reduced to its skeleton and regrown |
| 23–27 | Act IV | as chant, organum and isorhythmic motet; as a point of imitation; as a French overture and chaconne; as a Classical variation set beside Mozart's; as a nocturne and a Lied |
| 28–33 | Act V | in whole tones and octatonic ostinato; as a twelve-tone row; phased against itself and as a spectrum; as a walk on the Tonnetz; rerouted through chord space; as a tiling canon and in change ringing |
| 34–40 | Act VI | as alap and gat; in Rast, Bayati and Hijaz; as balungan with interlocking parts; emerging from an ensemble's inherent patterns; as a blues and a riff chart; as a bebop head; as a pop single that samples Variation 7 |
| 41–44 | Act VII | orchestrated eight ways; composed by generate-and-test; as written against as performed; as a film cue, a leitmotif and an adaptive game score |
| 45–47 | Act VIII | hidden inside another melody; with three engineered endings; after thirty generations of simulated oral transmission |
| 48–53 | Act IX | at one bit; in simulated rooms and through a phaser; sung, tuned and vocoded; on a modelled analog synthesizer; in FM and grains; as a tracker module and a tempo canon |
| 54–60 | Act X | through virtual microphones and loudspeakers; walked through four halls; recorded and mixed three ways; mastered loud and dynamic; at five bitrates with the discarded residue; from three places in an arena; with its royalty statement |
| 61–66 | Act XI | transcribed and re-rendered five times; followed by an accompanist; recognized from five noisy seconds; separated and recombined; continued by a transformer; rendered by a model trained on our own instruments |
| 67–68 | Coda | as a critical edition; then the suite |

Rules for the Variations:
- A variation is **written by the series**. Where a part builds a generator (Parts 16, 17, 42, 65, 66), the
  generator's output is shown with its seed and its rejected candidates, and any human edit is shown as a diff.
- A variation's quality claim is measured, not asserted: the counterpoint checker's verdict, the listener model's
  surprise curve, the loudness, the transcription error.
- The ledger keeps, for each row: the score, the audio, the key, tempo and duration, and the part's measurement.
- The full set goes on the course site with a player per part. Part 68 performs a suite chosen and ordered from
  it (10–12 minutes), not all sixty-seven.

### 2.3 The Chain, the timeline and the payoffs

- `explainer.music.chain`: drawn on every chapter card with the part's links lit. The inner loop is *mind → score
  → hands → instrument → air → ear → mind*. The outer loop, lit from Act IX on, is *microphone → console → master
  → codec → stream → loudspeaker*. Act XI adds the return path, *sound → machine → score*, which closes the loop in
  Part 68.
- `explainer.music.timeline`: a strip on a compressed scale: 40,000 BCE, 3000 BCE, 500 BCE, 1000, 1600, 1750,
  1900, 1950, 2000, 2030. Each part's milestones are added as it lands.
- Payoff cards ("where this comes back") link forward. Callbacks link to the other series instead of repeating
  them: the FFT and dynamic programming in *Computer Science, Built* Parts 19 and 21, Shannon's theorems in its
  Part 28, lock-free queues in its Part 33, the path tracer in its Part 51; Fourier analysis in *Analysis, Built*;
  transformers and diffusion in *AI, Built*; meta-analysis, multiple testing and evaluation in *Statistics, Built*
  (Part 67 uses `explainer.stats.kit` directly); present values in *Quant, Built* (Part 60).

### 2.4 The Library, and what the series may play

`explainer/music/library/` holds the series' sources. Each item has a manifest entry: what it is, where it came
from, its licence or public-domain basis with the jurisdictions considered, and the date it was checked. The
snapshot is committed when the licence allows, fetched by `compute.py` otherwise.

- **Scores as data.** Bach's four-part chorales and *The Well-Tempered Clavier*; Mozart's K. 265; Fux's examples;
  Josquin and Palestrina masses; Beethoven and Chopin piano works; Joplin's rags; public-domain folk-tune
  collections. Encodings are taken from open corpora whose licences permit it **(verify each)**, or entered by
  the series.
- **Measured references.** Instrument samples that are free to use (the University of Iowa set **(verify)**), a
  public HRTF set (MIT KEMAR **(verify)**), ISO 226 contours, published tunings (gamelans, maqam and raga
  intonation studies), published timing profiles. These calibrate and test Monochord. They appear on screen as
  measurements, labelled, and are credited in `docs/CREDITS.md`.

**The rights rule (M).** The series plays only (a) its own renderings of compositions in the public domain in the
jurisdictions recorded in the Library, (b) material written for the series, and (c) short measured references
whose licence permits it. Works still in copyright (most jazz standards, almost all popular song, much
twentieth-century concert music) are taught through their published analysis and corpus statistics, through
harmonic and rhythmic skeletons in Roman numerals, and through original pastiche written by the series in the
style. Parts 28–30 and 38–40 depend on this rule most. Each part's README lists every piece it renders with its
Library entry, and the list is reviewed before the part is rendered. This is a production rule set
conservatively; the owner confirms it in §9.

### 2.5 The degrees and the industry

| Programme | Acts and parts |
|---|---|
| BMus core: theory, aural skills, history | II, III, IV; the ear thread; 28–29; 41–43 |
| Acoustics and psychoacoustics | I; 45; 54–55 |
| Music technology / audio engineering (BSc, Tonmeister) | I; IX; X |
| Jazz and popular-music programmes | 11–15; 38–40; 56–57 |
| Ethnomusicology | 34–37; 47; 67 |
| Graduate theory and mathematical music theory | 22; 29; 31–33 |
| Music cognition (MSc/PhD) | 4–5; 14–15; 45–47; 67 |
| MIR and music AI (MSc/PhD) | 3; 61–66; 67 |
| Music business | 40; 60; 63 |

| Role | Where it is taught |
|---|---|
| Composer, arranger, orchestrator, songwriter | 16–22, 38–42 |
| Performer, conductor, teacher | the ear thread, 6, 11, 43 |
| Media composer, game audio designer | 44, 51–53 |
| Recording, mixing, mastering engineer; producer | 48–50, 54–58 |
| Live sound and systems engineer; acoustician | 2, 49, 54, 55, 59 |
| Audio DSP and plug-in developer | 3, 48–53, 58 |
| Instrument and loudspeaker designer | 7–9, 54 |
| MIR, recommender and generative-audio engineer | 61–66 |
| Musicologist, theorist, music psychologist | 22–37, 45–47, 67 |
| Label, publishing, rights and data roles | 60, 63 |

The course material follows `videos/coursekit/`: levels `U` (a first degree in music or music technology), `M`
(a master's or conservatory graduate course), `D` (doctoral research) and `I` (industry practice), four tracks
through the chapters, a lab and an interactive per part.

## 3. Sound: the pipeline

The repository's scenes have so far carried one kind of sound, narration (`explainer/voiceover.py` adds each line's
WAV to manim's file writer, and `tools/build.py` masters the stitched track). A series about music needs a second
layer with stricter requirements. This section is the specification; Phase 0 (§7) builds and tests it.

**Clips.** A clip is a named, cached array: 48 kHz, float32, mono or stereo, produced by the part's `compute.py`
through Monochord, with a sidecar of events (note onsets and offsets, beat times, section boundaries) in seconds.
`load_clip("tune.var06.meantone")` returns both.

**`SoundScene`** (`explainer/music/sound.py`, on `VoiceoverScene`):
- `self.sound(clip, gain_db=0)` starts a clip at the current time, under or between narration.
- `with self.listen(clip) as snd:` opens a **listening window**: narration is silent, the clip plays, and
  `snd.wait_until("bar3")` or `snd.at(event)` times animations to the clip's events exactly as `vo.wait_until`
  times them to words.
- Visual instruments take the clip itself (`Spectrogram(clip)`, `Staff(score).playhead(snd)`), so picture and
  sound cannot drift.
- Each scene writes a cue sheet (`<Scene>.cues.json`: clip, start, gain, bus) beside its narration record.

**Mixing and mastering.** Today `tools/build.py` applies `highpass=f=60` and two-pass `loudnorm` to the whole
soundtrack. That is right for a voice and wrong for music: the high-pass removes the fundamentals of a double
bass, a kick drum and the lowest two octaves of the piano. The series therefore gets its own profile:
- narration and music are kept on separate stems; the cue sheet lets `build.py` mix the music stem itself, in
  stereo, at full resolution, instead of relying on manim's mixer (the pilot checks what manim's `add_sound`
  preserves, and the preview path may still use it);
- the high-pass applies to the narration stem only;
- loudness is anchored on the narration (the same −16 LUFS target), and the music stem's gain is fixed for the
  whole series, so relative levels between examples are the ones written in the code;
- a true-peak ceiling (−1.5 dBTP for every clip, −1.0 dBTP for the mixed film) is enforced on the music by a
  check, not by a limiter: a part that exceeds it fails the gate and is fixed at the source;
- the narration, and only the narration, passes a look-ahead limiter after its gain (found on Part 1's first
  narrated build: the voice has rare peaks some 20 dB above its loudness; limiting them moves its loudness by
  0.1 LU);
- Part 57 explains this chain on screen and measures the series' own masters with the meter it builds.

**Gates** (`tools/qa_sound.py`, new):
- *sync*: a test scene flashes and clicks at known times; the offset measured from the rendered file is under
  one frame;
- *overlap*: no narration over a listening window; music under narration only where the cue says `underscore`;
- *peaks and levels*: the true-peak ceiling; no clip louder than the stated maximum above the narration level;
- *silence*: every cue has signal; every listening window has a moving picture;
- *phone audition*: each part's soundtrack is rendered through a band-limited mono filter (300 Hz–8 kHz) and
  every example is tagged `survives`, `visual carries it` or `labelled`;
- *length*: `tools/lecture_length.py` counts listening windows from the cue sheets.

**What the viewer's chain does.** Video platforms re-encode audio with a lossy codec **(verify the current
formats and bitrates when Part 58 is written)**. Demonstrations near the threshold of audibility (bit depth,
dither, high bitrates, small level differences) are therefore shown as difference signals, amplified residues
and measured curves, labelled as such; the course site carries the lossless files.

**Notation.** Manim has no music engraver. The plan is to keep scores in Monochord's own format and render them
to SVG with an engraving library that tags every note, then import the SVG so that notes can be highlighted in
time. Verovio (a Python wheel, no system install) and LilyPond are the candidates; the pilot of Phase 0 chooses,
on three tests: the SVG imports into manim cleanly, each notehead can be addressed, and macOS and Linux agree.

**The course site.** Interactives make sound with the browser's Web Audio API, started by the reader's first
click, with no libraries and no network. This needs a small addition to the shared widget core and to
`tools/check_widgets.js` (§6). Labs may write a WAV next to their figure when run with `--wav`.

## 4. Visual instruments

Built in `explainer/music/viz/` as they are first needed; each takes a clip, a score or both.

- **Scope and Spectrum**: waveform, partial bars with harmonic markers, phase.
- **Spectrogram**: scrolling, linear, mel or constant-Q, with a playhead and note overlays.
- **String, Tube, Membrane**: the simulated object in motion, slowed, with its mode shapes.
- **Cochlea**: the unrolled basilar membrane with its travelling wave and critical bands.
- **Keyboard**, **Staff** (engraved, with playhead and highlights), **PianoRoll**, **Tablature**.
- **PitchClock** and **CircleOfFifths**: the twelve hues; chords as polygons.
- **TuningLattice**: fifths against thirds, commas as short vectors.
- **DissonanceCurve**: roughness against interval for the timbre on screen.
- **RhythmNecklace** and **MeterGrid**: onsets on a circle; the metric hierarchy as dot columns.
- **Tonnetz**: the plane and the torus, with P, L and R as flips.
- **ChordSpace**: the Möbius strip of dyads and the prism of triads, with voice leadings as paths.
- **KeyTorus**: Krumhansl's map with a piece's path.
- **FormArcs** and **SelfSimilarity**: repetition as arcs and as a matrix.
- **VoiceLeading**: the four voices as coloured threads, errors flashing.
- **SignalFlow**: a live block diagram, levels moving on every wire.
- **PoleZero**: the z-plane beside the response it gives, draggable in the site's interactive.
- **Meters**: peak, RMS, LUFS, correlation, goniometer.
- **Room**: rays, image sources and the impulse response they build.
- **PolarPlot** and **FieldMap**: microphone patterns; the pressure field of a loudspeaker array.
- **NextNote**: a model's probability bars for the next note, with the surprise of what came.
- **Ledger**: the Variations, each a thumbnail score with its measurement.

Rules: one idea per frame, drawn big; the playhead always visible; the same sound shown in several pictures
with the camera moving between them; derivations in place.

## 5. Part by part

Draft 1 gives each part its story, what it covers, what is built and heard, its Variation, its Frontier topic and
its reading. Part 1 is written out chapter by chapter as the model; the other parts get their chapter lists (14–18
chapters each) when their act is opened, after the act's frontier sweep. Lengths in parentheses are targets.

## Act I · Sound

### Part 1 · One String (~45)
*Story:* The founding legend of music theory is false. Pythagoras is said to have heard consonances in a
blacksmith's hammers and found their weights in the ratios 12:9:8:6; hammers do not behave that way, as Vincenzo
Galilei showed by experiment in the 1580s. The monochord does: lengths in the ratio 2:1 give the octave, 3:2 the
fifth. The part asks why a string has a pitch at all, finds the answer in the wave equation, and ends with the
discovery that one string is already a chord.
1. Hook: the hammers, and what happens when you actually weigh them. The Tune's first two notes, a fifth.
2. The monochord: stopping the string at 1/2, 2/3, 3/4. Ratios of length, heard and drawn.
3. What vibrates: tension, mass, length. Mersenne's laws (1636), verified on our string.
4. A wave on a string: the travelling pulse, reflection at a fixed end, superposition.
5. Deriving the wave equation from Newton's law on one small piece.
6. d'Alembert's solution (1747): two travelling waves. The simulation and the formula, overlaid.
7. Standing waves: two travelling waves make a mode. Nodes, and the harmonic touched on a guitar.
8. The quarrel: Bernoulli says every motion is a sum of modes; Euler and d'Alembert object. Fourier settles it
   sixty years later (Part 3).
9. The plucked string: its shape as a sum of modes, amplitudes falling as 1/n², and the harmonics missing at the
   plucking point.
10. Sauveur (1701): the overtones are in the sound. One string, heard as a chord, partial by partial.
11. Why the ratios: the octave shares every second partial, the fifth every third. A first, incomplete answer.
12. Damping and stiffness: why real strings decay and are slightly sharp in their upper partials (paid off in
    Part 7).
13. Monochord, the series' instrument, introduced; the Tune, the Variations and the Chain.
14. Frontier: nonlinear strings (tension modulation, pitch glide, whirling); energy-conserving schemes.
15. Variation 1: the Tune on one simulated string. Outro: problems, payoffs. What carries the sound to the ear?

*Built and computed:* a finite-difference string (numba), checked against d'Alembert and against the modal sum to a
tolerance; Mersenne's three laws recovered by regression; pluck-position spectra.
*Heard and seen:* the monochord's ratios; one mode at a time; the pluck moved along the string.
*In practice:* instrument makers' string scaling; every physical-modelling synthesizer starts here.
*Reading:* Mersenne, *Harmonie universelle* (1636); Fletcher & Rossing ch. 2; Benade; Bilbao, *Numerical Sound
Synthesis*; Cohen, *Quantifying Music*.

### Part 2 · Waves in Air (~35)
*Story:* In 1883 Krakatoa was heard nearly 5,000 km away and its pressure wave was recorded circling the globe.
Sound is a pressure wave, and almost everything odd about it (bass that goes round corners, a bottle that hums
one note, a siren that drops as it passes) follows from its wavelength.
1. Hook: the Tune on six bottles; Krakatoa heard at Rodrigues four hours later; seven passages on the barographs.
2. Sound needs air: Boyle's jar (1660); the monochord at a thousandth of an atmosphere; sound in helium, water, steel.
3. What moves: a row of gas parcels; pressure and displacement; p = ρcu; how small audible motion is.
4. The speed of sound: Newton's 15% error, Laplace's adiabatic correction, both run as simulations; temperature
   and the pitch of a pipe.
5. How loud: intensity, the bel and the decibel; one string and ten; an ear question (3 dB or 6 dB).
6. Spreading: the inverse-square law, simulated on a spherical ray; a string at 1, 2, 4, 8 m; a worked example.
7. Round the corner: wavelength; a wall at 170 Hz and at 1,360 Hz; the loss against Maekawa's chart; the Tune
   behind the wall.
8. Two sources: interference, Young's rule, a walk through the pattern; comb filtering between two loudspeakers.
9. Air in a pipe: open and stopped pipes, simulated; the end correction; flute and clarinet; an ear question.
10. A bottle: Helmholtz's resonator, the exact two-tube root and the simulation; filling it.
11. Why a string needs a box: impedance; a step, air to water, a flare against a sudden opening.
12. A source that moves: Doppler's formula derived; Buys Ballot's train; an ear question.
13. Frontier: steepening against Fubini's solution; shock waves in trombones; thermoacoustics; Tonga 2022.
14. Variation 2: the Tune on six bottles tuned by their filling. Outro: problems, payoffs. Can every sound be
    taken apart?

*Covers:* Boyle's bell in a vacuum; pressure and particle velocity; the speed of sound, Newton's 15% error and
Laplace's adiabatic correction; intensity and the decibel; the inverse-square law; wavelengths from 17 m to 17 mm
and diffraction; interference; standing waves in open and stopped tubes; the Helmholtz resonator; impedance; the
Doppler effect.
*Built and computed:* a chain of gas parcels, a 2-D finite-difference acoustic simulator and a variable-area tube;
tube and bottle resonances against the formulas.
*Variation 2:* the Tune on bottles tuned by their filling.
*Frontier:* nonlinear propagation and the "brassy" trombone; thermoacoustics.
*Reading:* Kinsler et al.; Pierce, *Acoustics*; Rossing, Moore & Wheeler.

### Part 3 · The Spectrum (~40)
*Story:* In 1807 the Paris Academy declined to publish Fourier's claim that any function is a sum of sines. A
square wave built on screen one harmonic at a time shows why they doubted and why he was right. Then a surprise:
play one plucked note backwards, and its spectrum is unchanged while its sound is another instrument. Timbre is not
only the spectrum.
1. Hook: a square wave assembled from pure tones; Fourier, Lagrange and the Academy; three questions.
2. A sum of sines: why sines; coefficients as averages; partial sums; Gibbs; the transform of a sound that happens
   once; an ear question.
3. From a recipe to a machine: the DFT, the fast algorithm written out and timed, a pluck's spectrum; a worked example.
4. What the ear does with it: Ohm's law, Helmholtz's resonators, a resonator bank on our string; Seebeck.
5. The other half of the recipe: phase, heard at a low note and not at a high one.
6. Time and frequency together: the spectrogram built column by column; how to read one; a gliding pitch.
7. What a window costs: leakage, three windows against Harris's table, a weak tone revealed.
8. The limit: one sound through two windows; counting cycles; Gabor's relation measured; tone bursts; an ear question.
9. A ruler for music: constant Q; the Tune on both rulers.
10. Sounds with no pitch: white, pink and brown noise; why noise spectra are averaged.
11. More than the spectrum: one pluck forwards, backwards and without its attack; attack, brightness, flux.
12. Frontier: reassignment; listeners who beat the uncertainty limit.
13. Variation 3: the Tune assembled additively. Outro: problems, payoffs, and a tone with no fundamental.

*Covers:* Fourier series and transform; the DFT and the FFT; Ohm's acoustic law and Helmholtz's resonators; the
short-time transform; windows and leakage; the Gabor limit; constant-Q and wavelets; phase and when it is audible;
noise colors; attack, decay and spectral flux.
*Built and computed:* an FFT, STFT and constant-Q transform checked against numpy and `scipy.signal`; the
uncertainty product measured; a reassigned spectrogram.
*Variation 3:* the Tune assembled additively, more partials in every phrase.
*Frontier:* reassignment and superresolution; listeners who beat the Gabor limit (Oppenheim & Magnasco 2013).
*Reading:* Hartmann; Müller ch. 2; Smith, *Mathematics of the DFT*.

### Part 4 · The Ear (~50)
*Story:* Békésy won the 1961 Nobel Prize for the travelling wave he saw in the cochleas of cadavers. The living
ear is far more sensitive and so sharply tuned that it must contain an amplifier, as Gold argued in 1948; in 1978
Kemp put a microphone in an ear canal and recorded the ear making sound. The part follows a tone from the eardrum
to a pitch, and finds a pitch that is not in the signal.
1. Hook: two pure tones and the third that the ear adds; Kemp, Gold and Békésy; the plan.
2. From air to water: the impedance mismatch; the middle ear as a transformer (a worked example); the ear canal as
   a stopped pipe.
3. A wave that sorts: the cochlea unrolled; the travelling wave in a model and why it stops; seven octaves, equal
   distances (a worked example); Greenwood's map; hair cells.
4. How fine is the ruler: Fletcher's experiment; the ERB formula (a worked example); beats, roughness, two tones
   (an ear question); a cochleagram; resolved and unresolved partials.
5. How loud is loud: a sweep at constant pressure; the threshold; phons and the A weighting (an ear question);
   sones; a worked example (sixteen violins).
6. What a loud sound hides: the masked threshold (a worked example and an ear question); upward spread; uses.
7. A second clock: phase locking and volleys; where the clock stops; the smallest audible step (an ear question).
8. The pitch that is not there: a note without its fundamental (an ear question); distortion ruled out; the
   autocorrelation model; a worked example; Schouten's shift; uses.
9. Where pitch stops: the Tune above 5 kHz; the model's pitch strength and the piano's range.
10. Two kinds of high: Shepard's scale (an ear question); chroma and height.
11. The only pair you get: hair cells, the noise notch, a safe dose (a worked example); no sound.
12. Frontier: outer hair cells as the amplifier; the cube-root law; the third tone with a guide; emissions; what is
    not known.
13. Variation 4: the Tune without fundamentals, then without octaves. Outro: problems, payoffs, two pairs of strings.

*Covers:* the middle ear as an impedance match; the cochlea's place map; hair cells and the active process;
critical bands (ERB); loudness, phons, sones and the A weighting; masking; just-noticeable differences; place and
timing theories of pitch, phase locking and why the piano stops near 4 kHz; the missing fundamental and the shifted
residue; Shepard tones; noise-induced hearing loss and how to avoid it.
*Built and computed:* Monochord's ear (`monochord/ear.py`): a middle-ear transformer, a long-wave cochlea, a
gammatone bank and cochleagram, a threshold and masking model, an autocorrelation pitch model that predicts the
missing fundamental and Schouten's shift, a Hopf oscillator; masking patterns reused in Part 58.
*Variation 4:* the Tune with its fundamentals removed, still heard at pitch; then as Shepard tones.
*Frontier:* the cochlear amplifier; hidden hearing loss; music through cochlear implants; regeneration.
*Reading:* Moore, *An Introduction to the Psychology of Hearing*; Plack; Pickles.

### Part 5 · Consonance (~50)
*Story:* Six answers in 2,500 years: number (Pythagoras), coinciding pulses (Galileo), the overtone series
(Rameau), a formula (Euler), beats (Helmholtz), fusion (Stumpf). Then Plomp and Levelt (1965) measure it, Sethares
shows that the consonant intervals move when the timbre does, and McDermott's team (2016) finds a society with
no preference at all. The part computes each theory and lets the viewer hear where each fails.
1. Hook: an exact octave that grinds and a wide one that is smooth; six answers; the plan.
2. Number: the monochord's ratios; Euler's gradus (a worked example) for thirteen intervals; a fifth five cents
   wide (an ear question).
3. Pulses that coincide: Galileo; three against two, sped up into a fifth; the same flaw, and why to keep the idea.
4. Beats: the sum of two close tones; 1, 4 and 12 a second; tuning by beats (a worked example); roughness.
5. Roughness, measured: Plomp and Levelt's curve and the critical band; two pure tones gliding apart (an ear
   question); a pure fifth and a pure tritone.
6. A curve with no ratios in it: the partials of two notes; a fifth and a tritone (a worked example); the
   dissonance curve and its valleys; the curve heard.
7. Bend the timbre: stretched partials move every valley; four sounds (an ear question); pianos, bells, gamelan.
8. One note or two: fusion; the note inside 4:5:6 (an ear question); the fundamental bass; harmonicity from Part
   4's pitch model; one tone to each ear.
9. Major and minor: the same intervals (an ear question); 4:5:6 and 10:12:15; four triads; a map of all triads.
10. What is learned: a history of the third; the Tsimane'; three layers.
11. Frontier: a composite model; a quarter of a million judgments online; what is not known.
12. Variation 5: the Tune in a bent timbre. Outro: problems, payoffs, and twelve fifths that do not close.

*Covers:* ratio theories (Pythagoras, Zarlino, Euler, Tenney); Galileo's coincidence theory; beats and roughness;
the critical band and the Plomp–Levelt curve; dissonance curves for harmonic and inharmonic timbres; harmonicity,
fusion and the fundamental bass; why major and minor triads differ though their intervals match; familiarity and
culture.
*Built and computed:* Monochord's consonance layer (`monochord/consonance.py`): Euler's gradus, beats, the
Plomp–Levelt curve in Sethares's form, dissonance curves whose minima fall on the just ratios, a timbre with
stretched partials for which a 2.1:1 "octave" is the smooth one, harmonicity from Part 4's pitch model, a
roughness map of all triads.
*Variation 5:* the Tune in a bent timbre, in parallel intervals that are consonant only for that timbre.
*Frontier:* composite models (Harrison & Pearce 2020); large online experiments on timbre and consonance (Marjieh
et al. 2024); what remains unexplained.
*Reading:* Helmholtz, *On the Sensations of Tone*; Sethares, *Tuning, Timbre, Spectrum, Scale*; McDermott et al.
(2016).

### Part 6 · Tuning (~55)
*Story:* In 1584 Zhu Zaiyu, a prince of the Ming, computed the twelfth root of two to twenty-four decimal places
on an abacus. He was solving a problem every keyboard has: twelve pure fifths overshoot seven octaves, so the
circle does not close. A choir that sings pure chords round one common progression ends a fifth of a semitone
flat. Every tuning system is a decision about where to hide the error.
1. Hook: one progression four times in pure chords, sinking 86 cents; Zhu Zaiyu; the plan.
2. The circle that will not close: twelve fifths and the Pythagorean comma; a worked example (no power of three is a
   power of two); Pythagorean tuning and its wolf.
3. The other comma: four fifths against a pure third (an ear question); three thirds against an octave; just
   intonation as a lattice; its wolf.
4. The comma pump: a worked example in exact fractions; four rounds; Benedetti.
5. Pure thirds, and a wolf: quarter-comma meantone (a worked example); three tunings of one chord; the wolf (an ear
   question); split keys.
6. Well tempered: Werckmeister III; the thirds of four tunings in every key; key character (an ear question); Bach.
7. Equal: the twelfth root of two; an abacus and a guitar (a worked example); what it costs (an ear question); the
   beats a tuner counts (a worked example); three centuries to win.
8. Why twelve: every equal division from 4 to 60; the continued fraction of log₂(3/2) (a worked example); five and
   seven; 19, 31 and 53.
9. The piano's stretched octaves: stiff strings; a model of Railsback's curve.
10. What players do: free instruments; a quartet's open strings; do choirs drift; the pitch of A.
11. Frontier: adaptive tuning; Bach's title page; what is not known.
12. Variation 6: the Tune in eight tunings. Outro: problems, payoffs, and a plucked string.

*Covers:* the Pythagorean and syntonic commas and the diesis; just intonation as a lattice; meantone and its wolf;
the well temperaments and key character; equal temperament (Zhu, Stevin), fret placement and tuning by beats;
continued fractions of log₂(3/2) and why 12, 41 and 53; 19 and 31 for thirds; the comma pump; the piano's stretched
octaves; how choirs and quartets adjust; concert pitch.
*Built and computed:* `tuning.py` in exact rationals, checked against Barbour's tables; beat rates a tuner counts;
the drift of a comma pump; a model of Railsback's curve.
*Variation 6:* the Tune in Pythagorean, quarter-comma meantone (a good key and the wolf key), Werckmeister III,
12, 19, 31 and 53 equal divisions.
*Frontier:* adaptive tuning; what tuning Bach meant (the 2005 hypothesis and its critics); temperaments as
lattices (Part 33).
*Reading:* Barbour; Duffin, *How Equal Temperament Ruined Harmony*; Sethares; Cho, *The Discovery of Musical Equal
Temperament in China and Europe*.

### Part 7 · Strings, Hammers and Bows (~55)
*Story:* In blind tests published in 2012 and 2014, players in a hotel room and soloists in a concert hall preferred
new violins to Stradivaris and could not tell which was which. So what makes a violin? The part builds a guitar, a
piano and a violin from the string of Part 1 and finds where each instrument's character lives.
1. Hook: four notes plucked, struck and bowed, all from one string; the blind tests; the plan.
2. A string cannot be heard: why a string needs a body (an ear question); the body as a filter; a tap; loud or long.
3. A plate, a hole and a box of air: the guitar's two-mass model (a worked example); the dip; the low E.
4. A pluck in three lines: Karplus and Strong; the loop lap by lap; why it is a string; its pitch.
5. The hammer: Cristofori; felt that stiffens; three touches (an ear question); the striking point (a worked example).
6. A string that is also a bar: stiffness and sharp partials (a worked example; an ear question); living with it.
7. Three strings for one note: loud or long (an ear question); Weinreich's coupled strings; the two-stage decay.
8. Stick and slip: rosin; the string under the bow; Helmholtz's corner; the sawtooth on the bridge.
9. How hard to press: speed, force and place (an ear question); Schelleng's diagram; nearer the bridge (a worked
   example); starting the note.
10. The violin's box: the body's response; vibrato as a change of colour; the wolf.
11. Frontier: the blind tests again; what nobody can do yet; instruments made of arithmetic.
12. Variation 7: the Tune for a guitar, a piano and a violin. Outro: problems, payoffs, and the bow's loop in air.

*Covers:* why a string needs a body; the guitar's air and plate resonances; Karplus–Strong; the piano's hammer,
stiffness and inharmonicity, paired strings and the double decay; the bowed string's stick-slip, Helmholtz
motion, the Schelleng diagram and the wolf note; a violin's signature modes and bridge hill; vibrato.
*Built and computed:* `instruments/strings.py`: Karplus–Strong; a felt hammer on a stiff string; two strings on a
yielding bridge; a bowed string with friction that reproduces the Helmholtz corner and, in outline, Schelleng's
limits; guitar and violin bodies as banks of resonances; the two-mass guitar.
*Variation 7:* the Tune for plucked, struck and bowed strings, alone, in pairs and together.
*Frontier:* what violin measurements do and do not explain; rosin that warms; the measured Schelleng diagram;
hammer-felt hysteresis; real-time finite-difference instruments.
*Reading:* Fletcher & Rossing; Cremer; Woodhouse's papers on the bowed string; Weinreich (1977); Fritz et al.
(2012, 2014, 2017).

### Part 8 · Pipes, Reeds and Voices (~55)
*Story:* A flute and a clarinet of the same length: the clarinet sounds an octave lower and its even
harmonics are nearly missing. A singer in Tuva sings two notes at once. Both follow from one idea, a valve
feeding a resonator, and the part ends with Monochord singing.
1. Hook: two pipes of one length (an ear question); one voice, two notes; the plan.
2. A column of air: open and closed ends; odd and whole series; the impedance of a pipe; the end correction; how
   long is a flute (a worked example).
3. A valve that pressure closes: the reed's flow curve; one puff, four trips; a square wave; blowing harder (an ear
   question); why a third.
4. Holes: a hole against a saw; where the holes go (a worked example); the register hole and the twelfth.
5. Cones: a cone has every harmonic; the missing tip and the mouthpiece; cone or cylinder (an ear question).
6. Lips and brass: a valve with its own frequency; what a bell and a mouthpiece do; the staircase and a call; the
   pedal note; three valves (a worked example).
7. A jet and an edge: the flute's valve; overblowing; octave or twelfth (an ear question); the organ's stops.
8. The voice, a source and a filter: the folds; the pulse; formants; a source through three filters.
9. Vowels: a mouth at rest (a worked example); two tubes for ah and ee; the map of two formants; three vowels (an
   ear question).
10. What singers do: ring (an ear question); a soprano's tuned resonance; overtone singing.
11. Frontier: the folds, the player's own tract, shock waves in brass, the jet; instruments designed backwards.
12. Variation 8: the Tune for five valves on five columns of air. Outro: problems, payoffs, and overtones that are
    not harmonics.

*Covers:* cylinders and cones; input impedance; the reed as a pressure-controlled valve and its threshold; tone
holes and register holes; brass lips, the bell and mouthpiece and the pedal note; valves; the flute's jet and
overblowing; the organ as additive synthesis; the voice: folds, source and filter, formants and vowels, the
singer's formant, a soprano's resonance tuning, overtone singing.
*Built and computed:* `instruments/winds.py`: bore impedances by transfer matrices and reflection functions; a
reed, a lip and a jet model on any bore; a source-filter voice; formants of tubes.
*Variation 8:* the Tune for a flute, a clarinet, a saxophone, a trumpet and a voice.
*Frontier:* vocal-fold models; the player's vocal tract; nonlinear propagation in brass; computed and printed
bores.
*Reading:* Benade; Fletcher & Rossing; Sundberg, *The Science of the Singing Voice*; McIntyre, Schumacher &
Woodhouse (1983).

### Part 9 · Drums, Bars and Bells (~45)
*Story:* "Can one hear the shape of a drum?" Kac asked in 1966. In 1992 the answer came: no, and here are two
different drums with identical spectra. Meanwhile instrument makers had solved the opposite problem for
centuries: how to make a membrane or a bar, which nature tunes badly, sing in tune.
1. Hook: a string and a drum on one note; Kac's question; the plan.
2. A skin: its modes; the first interval of a drum (a worked example); where it is struck (an ear question).
3. A drum with a note: the kettledrum's modes, bare, estimated and measured (an ear question); which octave.
4. A patch of paste: Raman on the tabla; a loaded skin computed; bare and loaded.
5. Bars: thickness over length squared (a worked example); a free bar's modes; the arch; plain or carved (an ear
   question); the tube beneath.
6. Bells: the partials; the strike note as a missing fundamental; the minor third (an ear question); the
   major-third bell.
7. Plates and sand: Chladni's figures; what the sand started.
8. Gongs and cymbals: pitch that follows loudness; a crash.
9. The steelpan: a dome tuned with a hammer.
10. Hearing a shape: Weyl's law; the two drums of 1992, computed (an ear question); the answer.
11. Frontier: hearing material, size and shape; design run backwards.
12. Variation 9: the Tune on marimba, bells, steelpan and kettledrums. Outro: problems, payoffs, the end of Act I.

*Covers:* membrane modes and Bessel zeros; how air loading makes the timpani nearly harmonic, and how a loaded
skin does it for the tabla (Raman); bars and their undercut tuning; the bell's partials, its strike note and its
minor third; Chladni's figures; gongs and cymbals; the steelpan; Weyl's law and the isospectral drums.
*Built and computed:* `instruments/percussion.py`: a membrane solver for any polygon (the isospectral pair
computed), a loaded membrane, a beam solver for carved bars, modal synthesis.
*Variation 9:* the Tune on marimba, bells, steelpan and kettledrums.
*Frontier:* hearing material and size; which shapes can be heard; nonlinear plates and gongs; inverse design.
*Reading:* Rossing, *Science of Percussion Instruments*; Kac (1966); Gordon, Webb & Wolpert (1992).

## Act II · Notes

### Part 10 · Writing It Down (~45)
*Story:* A clay tablet from Ugarit, about 1400 BCE, holds the oldest notated song, and scholars disagree on how it
goes. Around 1025 Guido of Arezzo claimed that with his lines a singer could learn in a year or two what had taken
ten. Notation is a coordinate system, time against pitch, drawn three centuries before Oresme. The part asks what
each system keeps and what it throws away.
1. Hook: the tablet's first line, read two ways; Isidore: sounds cannot be written down; the plan.
2. A reminder: neumes; three melodies that fit the same signs (an ear question); counting them; the first line.
3. Guido's lines: the staff and its clefs; the staff as a graph; *Ut queant laxis*; the hidden half step.
4. How long? Franco's shapes; perfect and imperfect time; a note read by its neighbours; dots and ties (a
   predict-pause); the rule for dots.
5. Bars and scores: part books; the score and the bar line; a note cut at a bar line; what was added later.
6. What to do: tablature and its count of fingerings, by dynamic programming; figured bass, realized twice.
7. Numbers and characters: gongche; Rousseau and jianpu; guqin tablature; graphic scores.
8. Holes and bytes: the piano roll; MIDI's bytes; what a key number forgets (an ear question: G♯ and A♭).
9. The page as data: MusicXML and MEI; round trips; the table of what each notation keeps.
10. How many bits? Files; 168 bits against 21 million; the page played exactly and played well (an ear question).
11. Frontier: reading a page back, as a toy that a tilt breaks (an ear question); where the field stands.
12. Variation 10: the Tune in ten notations, and a last phrase as none of them says. Outro: problems, payoffs.

*Covers:* neumes; the staff and the hexachord; mensural notation and the invention of written duration; barlines
and scores; tablature; figured bass; jianpu, gongche and guqin tablature; graphic scores; piano rolls; MIDI,
MusicXML and MEI; the bits in a score against the bits in its recording.
*Built and computed:* Monochord's `score` module (spelled pitches, exact durations; MusicXML, MEI, MIDI, ABC,
LilyPond and jianpu writers; MusicXML and MIDI readers; contours, tablature, figured bass, mensural lengths,
performance rules, a toy page reader), and the series' engraver (`explainer/music/staff.py`).
*Variation 10:* the Tune in ten notations, then what none of them recorded.
*Frontier:* optical music recognition; encoding standards; digital critical editions.
*Reading:* Kelly, *Capturing Music*; Gould, *Behind Bars*; Selfridge-Field (ed.), *Beyond MIDI*.

### Part 11 · Rhythm and Meter (~50)
*Story:* Play identical clicks and listeners hear them in twos: tick, tock. Meter is something the listener adds.
The part builds rhythm from a pulse, and ends by speeding a 3:2 polyrhythm up until it turns into a perfect
fifth, the rhythm of Part 1's ratio.
1. Hook: sixteen identical strokes, heard in pairs (an ear question) and measured; Bolton; the plan.
2. A pulse: tempo; clicks from slow to fifty a second; the window of the beat; two tempos (an ear question).
3. Meter: nested pulses and their weights; three-four and six-eight; a pulse finder taps the Tune.
4. Accent: louder, longer, higher; which sound begins a pair (an ear question); Woodrow.
5. Dividing the beat: twos, threes and fours; milliseconds (a predict-pause); simple and compound meters.
6. Syncopation: Longuet-Higgins and Lee's index, worked; four rhythms; two to compare (an ear question); the arch.
7. Three against two: hemiola; polyrhythm on a circle; four against three.
8. Long beats and short: seven three ways; counting the meters of twos and threes; four dances.
9. Swing: three ratios; the short note of 100 ms; what the page does not say.
10. Where rhythm becomes pitch: three against two, sped up into a fifth (an ear question); intervals as polyrhythms.
11. Frontier: the telephone game on rhythms, simulated; what fifteen countries showed; what is not known.
12. Variation 11: the Tune in four, as a waltz, in five, in seven, swung, with a hemiola. Outro: problems, payoffs.

*Covers:* pulse, tempo and its limits; meter as nested periodicities; note values and tuplets; accent;
syncopation and how to measure it; hemiola; polyrhythm and polymeter; additive meters; swing; the rhythm–pitch
continuum.
*Built and computed:* the rhythm engine (`monochord/rhythm.py`: metric weights, a syncopation index, a pulse
finder, polyrhythms, compositions into twos and threes, swing, click trains, the telephone game); a kit of struck
things (`instruments/drumkit.py`); the pictures of rhythm (`explainer/music/rhythmviz.py`).
*Variation 11:* the Tune as a waltz, in five, in seven, swung, and with hemiola.
*Frontier:* rhythm priors across cultures (Jacoby and others, 2024); microtiming and groove.
*Reading:* London, *Hearing in Time*; Lerdahl & Jackendoff ch. 4; Sethares, *Rhythm and Transforms*.

### Part 12 · Scales and Modes (~50)
*Story:* Why seven white keys and five black? Stack fifths and fold them into an octave: at 5, 7 and 12 notes the
steps come in just two sizes. Those are the pentatonic, the diatonic and the chromatic. The part derives the
scales most of the world uses from one construction, then counts every scale there could be.
1. Hook: the white keys and the black keys; why seven and five; the plan.
2. Stacking fifths: steps of two sizes at five, seven and twelve notes; the three stacks, heard.
3. Three gaps: the theorem; where a stack has two sizes (a predict-pause); 17, 53 and Part 6's continued fraction.
4. Seven notes, seven modes: the chain of fifths; brightness; all seven on C (an ear question); the Tune's blind spot.
5. Why this scale: maximally even; two sizes of every interval; deep; a scale moved by a fifth.
6. Minor's three forms: natural, harmonic, melodic; the leading note (an ear question).
7. Fewer notes, and more: pentatonic, whole-tone, octatonic, blues; scales with two and three transpositions.
8. A scale in two halves: tetrachords; the 72 melakartas.
9. Other maps of the octave: Rast, slendro, Mayamalavagowla; what a scale leaves out.
10. Every scale there is: Burnside's lemma, 352 shapes; the 66 with seven notes; three; one (an ear question).
11. Frontier: the white keys against the other 65; seven equal steps (an ear question); four explanations.
12. Variation 12: the Tune in ten scales. Outro: problems, payoffs.

*Covers:* generating scales by fifths and the three-gap theorem; maximal evenness, Myhill's property and the deep
scale; the seven modes ordered by brightness; minor's forms; pentatonic, whole-tone, octatonic and blues scales;
a first look at raga, maqam and slendro; necklaces counted with Burnside's lemma.
*Built and computed:* the scale module (`monochord/scales.py`); all 352 necklaces of twelve beads, classified; the
pictures of scales (`explainer/music/scaleviz.py`).
*Variation 12:* the Tune in all seven modes, then pentatonic, whole-tone and octatonic.
*Frontier:* why scales have five to seven unequal steps: the competing explanations.
*Reading:* Clough & Douthett (1991); Carey & Clampitt (1989); Tymoczko, *A Geometry of Music* ch. 4.

### Part 13 · Intervals and Chords (~45)
*Story:* In 1722 Rameau made a radical claim: C–E–G and E–G–C are the same chord. Inversion, the root and the
fundamental bass turned a thicket of intervals into a small vocabulary. The part builds chords, explains why the
same third is clear in the treble and muddy in the bass, and draws Euler's Tonnetz for later.
*Covers:* interval names and spelling on the line of fifths; interval classes; triads and sevenths; inversion and
figured bass; roots and virtual pitch; voicing, spacing and the critical band; doubling; chord symbols; the
Tonnetz (Euler 1739).
*Built and computed:* the chord module with a root finder; the low-interval limit from Part 5's model.
*Variation 13:* the Tune in block triads, then re-voiced.
*Frontier:* models of chord perception; automatic harmonic analysis.
*Reading:* Rameau, *Traité de l'harmonie*; Parncutt, *Harmony: A Psychoacoustical Approach*; Laitz.

### Part 14 · Melody (~50)
*Story:* Textbooks say a leap should be followed by a step back. In 2000 von Hippel and Huron showed that the
"rule" is what any melody confined to a range does by chance: regression to the mean. The part separates what
melodies do because of composers from what they do because of arithmetic, and builds a model that is surprised
in the right places.
*Covers:* contour; the predominance of steps; the arch; range and tessitura; gap-fill; tendency tones; motive and
sequence; phrase and breath; entropy and Zipf's law; n-gram and variable-order models of expectation; text and
tone.
*Built and computed:* an n-gram model on public-domain folk tunes; step and leap statistics; the regression
argument run as a simulation; the Tune's surprise curve.
*Variation 14:* the Tune ornamented, inverted, and with its least and most expected continuations.
*Frontier:* IDyOM and neural predictors of expectation; memory for melody.
*Reading:* Huron, *Sweet Anticipation*; von Hippel & Huron (2000); Temperley, *Music and Probability*.

### Part 15 · Key (~50)
*Story:* Play a scale, then one tone, and ask a listener how well it fits. Krumhansl's probe-tone profiles (1982)
show the key is a hierarchy in the listener's head, and that it matches how often each note occurs in the music
they grew up with. A key is learned statistics.
*Covers:* scale degrees and their qualities; tonic, dominant and predominant; cadences; the probe-tone experiment;
key finding (Krumhansl–Schmuckler, Temperley's Bayesian model); the torus of keys; relative and parallel keys;
tonicization and modulation.
*Built and computed:* a key finder scored on the forty-eight preludes and fugues; a piece's path on the torus.
*Variation 15:* the Tune modulating round the circle of fifths, ending on a deceptive cadence.
*Frontier:* tonal hierarchies in other traditions; when tonality emerged, read from corpora.
*Reading:* Krumhansl, *Cognitive Foundations of Musical Pitch*; Temperley, *The Cognition of Basic Musical
Structures*.

## Act III · Voices

### Part 16 · Two Voices (~55)
*Story:* Every harmony student is told that parallel fifths are forbidden. In the ninth century they were the
rule. In 2001 Huron derived the textbook's rules from experiments on how hearing separates sounds into streams:
the rules are instructions for keeping two voices audible as two. The part teaches Fux's species as engineering.
*Covers:* organum; cantus firmus; the four motions; species one to five; passing tones, neighbours and
suspensions; stream segregation, fusion and onset synchrony; independence measured; Bach's inventions.
*Built and computed:* a species checker and a search-based generator; every valid first-species line against the
Tune, counted; rules removed one at a time and the damage measured.
*Variation 16:* the Tune as cantus firmus through the five species.
*Frontier:* corpus tests of the perceptual account; counterpoint as constraint satisfaction.
*Reading:* Fux, *Gradus ad Parnassum* (1725); Huron (2001); Jeppesen; Salzer & Schachter.

### Part 17 · Four Voices (~55)
*Story:* Bach left some 370 four-part chorales, several tunes harmonized four or five different ways. They became
the exercise book of every harmony class and, three centuries later, the first benchmark of music-generating
machines. The part learns the craft, counts how often Bach breaks the rules, and builds a harmonizer to be judged
against him.
*Covers:* ranges, spacing and doubling; the voice-leading rules; cadences; non-chord tones; figured bass;
harmonization as search over chords and voicings.
*Built and computed:* a harmonizer (a chord model with a voice-leading cost, solved by dynamic programming);
rule violations in the chorales counted; our harmonizations scored against Bach's on held-out tunes.
*Variation 17:* the Tune as a chorale, ours and the corrected one, with the corrections shown.
*Frontier:* DeepBach and Coconet; how to evaluate style.
*Reading:* Aldwell & Schachter; Kostka & Payne; Allan & Williams (2005).

### Part 18 · Progressions (~50)
*Story:* In the conservatories of eighteenth-century Naples, orphans were trained into the most employable
composers in Europe by memorizing bass patterns. Gjerdingen showed that the galant style is assembled from a few
dozen such schemata. Harmony has a syntax, and the part measures it.
*Covers:* function and root motion; the descending-fifths sequence and its relatives; harmonic rhythm; the rule of
the octave; partimento; the Romanesca, Prinner, Monte, Fonte and Ponte; ground basses from the Folia to the
lament.
*Built and computed:* chord-transition matrices from the chorales; the entropy of harmony; a schema detector.
*Variation 18:* the Tune over the Romanesca, the Folia and a lament bass.
*Frontier:* corpus harmony at scale; schema learning.
*Reading:* Gjerdingen, *Music in the Galant Style*; Sanguinetti, *The Art of Partimento*; Laitz.

### Part 19 · Chromatic Harmony (~55)
*Story:* Four notes at the opening of *Tristan* (1859) have been argued over for 160 years. They are the end of a
road that starts with one borrowed leading tone. The part walks that road and shows that its trapdoors, the
enharmonic modulations, exist only because of the temperament chosen in Part 6.
*Covers:* secondary dominants; mixture; the Neapolitan; augmented sixths; the diminished seventh's symmetry;
enharmonic reinterpretation and the comma it hides; chromatic mediants; the omnibus; altered dominants; tonal
ambiguity from Schubert to Wolf.
*Built and computed:* a pathfinder for the shortest modulation between any two keys; a tension curve from tonal
pitch space.
*Variation 19:* the Tune reharmonized by degrees from Schubert to Wagner, with an enharmonic trapdoor.
*Frontier:* models of extended tonality; the Tristan chord's analyses compared.
*Reading:* Aldwell & Schachter; Lerdahl, *Tonal Pitch Space*; Cohn, *Audacious Euphony*.

### Part 20 · Canon and Fugue (~55)
*Story:* On 7 May 1747 Frederick the Great gave Bach a theme designed to resist counterpoint and asked for a fugue
in six voices. Bach sent back the *Musical Offering*, with canons posed as riddles: one played backwards against
itself, one that rises a tone each time round and never arrives. The part asks which melodies can be combined with
themselves, and solves for them.
*Covers:* rounds; canon at every interval; invertible counterpoint; inversion, retrograde, augmentation and the
group they form; the fugue: subject, real and tonal answers, countersubject, episode, stretto, pedal; *The Art of
Fugue*.
*Built and computed:* a canon solver; the stretto possibilities of the *Well-Tempered Clavier*'s subjects, found
and compared with what Bach used; the rising canon rendered with Shepard tones.
*Variation 20:* the Tune as a round, a crab canon and a three-voice exposition.
*Frontier:* automatic fugue analysis and generation.
*Reading:* Mann, *The Study of Fugue*; Gauldin; Hofstadter, *Gödel, Escher, Bach*.

### Part 21 · Form (~50)
*Story:* Loop a spoken phrase a few times and it turns into song (Deutsch's illusion). Music repeats far more than
any other art, and form is the plan of what returns. The part teaches the forms and then finds them from the audio
alone.
*Covers:* motive, phrase, period and sentence; binary and ternary; rondo; variation; sonata form as a drama of
keys; song forms from strophic to verse-chorus and the twelve-bar blues; repetition; self-similarity; the
golden-section claims, tested.
*Built and computed:* self-similarity matrices from scores and from audio; a novelty-based segmenter; repetition
rates across the Library.
*Variation 21:* the Tune as a miniature sonata whose second theme is its own inversion.
*Frontier:* do listeners hear large-scale tonal form? The experiments and the arguments.
*Reading:* Caplin, *Classical Form*; Hepokoski & Darcy; Margulis, *On Repeat*.

### Part 22 · Analysis (~55)
*Story:* Schenker claimed that every tonal masterpiece elaborates one stepwise descent to the tonic. The Tune
does it on its surface: it climbs to the fifth and walks down. The part takes the claim seriously as a theory,
states it as a grammar, parses with it, and reports what the grammar explains, what it cannot, and why the theory
and its author are argued over.
*Covers:* reduction and prolongation; the Ursatz; Lerdahl and Jackendoff's grouping, meter and reductions as
preference rules; harmony as a context-free grammar; parsing and ambiguity; other approaches (implication,
semiotics, topics); the 2020 controversy.
*Built and computed:* a probabilistic grammar of chord sequences trained on the Library; a time-span reduction
of the Tune, each level played.
*Variation 22:* the Tune reduced to its skeleton and regrown along a different derivation.
*Frontier:* grammars induced from data; whether harmony is recursive: the evidence.
*Reading:* Cadwallader & Gagné; Lerdahl & Jackendoff (1983); Rohrmeier (2011).

## Act IV · A Thousand Years

### Part 23 · Chant to Polyphony (~50)
*Story:* Paris, about 1200. Under the unfinished vault of Notre Dame, Pérotin stretches one syllable of chant for
a minute beneath three dancing upper voices. To keep four singers together he needs something no one has had:
a way to write rhythm.
*Covers:* chant and the eight modes; Guido's hexachord; parallel, free and florid organum; the rhythmic modes;
the motet; the Ars Nova and mensuration; isorhythm; Machaut; the Ars subtilior.
*Built and computed:* an isorhythm engine (talea against color, their periods and realignment); a mode classifier.
*Variation 23:* the Tune as chant, organum and an isorhythmic motet.
*Frontier:* computational chant studies; what the notation does not settle.
*Reading:* Hoppin, *Medieval Music*; Taruskin vol. 1; Kelly, *Capturing Music*.

### Part 24 · The Renaissance (~50)
*Story:* Josquin des Prez was the first composer made famous by the printing press, and the press also put his
name on other people's music. A large share of what once carried his name is now doubted. The part learns the
style well enough to ask a statistical question: who wrote this?
*Covers:* thirds and sixths become consonant; imitation as structure; mass types; the madrigal and word painting;
Palestrina's style as rules; Petrucci (1501); Zarlino's just triad; musica ficta; Gesualdo; Vicentino's
thirty-one tones.
*Built and computed:* a stylometric attribution test on secure works; adherence to Palestrina's rules measured.
*Variation 24:* the Tune as a four-voice point of imitation.
*Frontier:* computational attribution; modelling ficta.
*Reading:* Atlas, *Renaissance Music*; Jeppesen; Rodin (ed.), the Josquin Research Project **(verify licence)**.

### Part 25 · The Baroque (~50)
*Story:* Around 1600 a Bologna theorist attacked Monteverdi for a dissonance that broke the rules, and Monteverdi
answered that the words required it. At the same time Vincenzo Galilei, the astronomer's father, was hanging
weights on strings to argue for a new kind of song. Out of the quarrel came opera, the figured bass, and the
major-minor system.
*Covers:* the two practices; monody, recitative and aria; basso continuo; the ritornello; the suite; affect;
ornament; the trio sonata and concerto; temperament and key character; Bach, Handel, Rameau.
*Built and computed:* a figured-bass realizer; a ritornello finder.
*Variation 25:* the Tune as a French overture and as a chaconne with ornamented reprise.
*Frontier:* historical pitch and tempo: the evidence from instruments and treatises.
*Reading:* Bukofzer; Taruskin vol. 2; Donington.

### Part 26 · The Classical Style (~50)
*Story:* In Vienna in the early 1780s Mozart wrote twelve variations on our Tune. The part reads them as data,
variation by variation, and uses them to explain a style built on shared expectations so strong that Haydn could
end a quartet with a joke about where the ending is.
*Covers:* schemata in use; periodic phrasing; sonata form on stage; the quartet, symphony and concerto; Haydn's
economy; Mozart's ensembles; Beethoven's motives and expansions; the fortepiano; the metronome and Beethoven's
puzzling marks.
*Built and computed:* K. 265 measured (density, register, harmony, figuration); a phrase-structure parser; the
tempo study recomputed from published data.
*Variation 26:* our own Classical set (Alberti bass, minore, adagio, finale) beside Mozart's.
*Frontier:* style as learned statistics; the Beethoven tempo debate.
*Reading:* Rosen, *The Classical Style*; Caplin; Gjerdingen.

### Part 27 · The Romantic Century (~55)
*Story:* Between 1800 and 1870 the piano gained an iron frame, two octaves and several times the loudness, and
the orchestra doubled. The music grew to fit, harmony was stretched until the key could barely hold, and the
concert became a museum. The part measures the stretching.
*Covers:* the Lied; the character piece; programme music and the idée fixe; the leitmotif as a network; chromatic
expansion; nationalism and folk modes; virtuosity; the conductor; rubato; canon formation; the first recordings.
*Built and computed:* a chromaticism index and tonal-clarity measure across the Library from 1700 to 1900;
orchestra sizes over time from published rosters.
*Variation 27:* the Tune as a nocturne, as a Lied accompaniment, and as a transformed leitmotif.
*Frontier:* corpus studies of nineteenth-century harmony; performance style read from early recordings.
*Reading:* Taruskin vol. 3; Rosen, *The Romantic Generation*; Dahlhaus.

## Act V · After Tonality

### Part 28 · New Scales, New Rhythms (~50)
*Story:* At the 1889 Paris Exposition Debussy heard a Javanese gamelan and wrote that it made Western percussion sound
like the noise of a country fair. Within twenty-five years composers had rebuilt music from other scales and other
rhythms, and one première in 1913 became a legend of riot. The part enumerates the symmetric scales they used.
*Covers:* whole-tone, pentatonic and octatonic collections; planing; ostinato and displaced accents; polychords;
Bartók's fieldwork, symmetry and additive rhythm; Messiaen's modes of limited transposition and non-retrogradable
rhythms; the golden-section claims.
*Built and computed:* every transposition-symmetric scale enumerated; a statistical test of the golden-section
claim on a null model.
*Variation 28:* the Tune in whole-tone planing, then as an octatonic ostinato with moving accents.
*Frontier:* the octatonic debate; computational analysis of early modernism.
*Rights:* analysis and original pastiche where a work is in copyright (§2.4).
*Reading:* Taruskin vol. 4; Antokoletz; Tymoczko (2002).

### Part 29 · Twelve Tones (~50)
*Story:* In 1908 a soprano enters a string quartet singing "I feel the air of another planet", and the key
dissolves. Schoenberg then spent a decade looking for a law to replace it. The part builds the mathematics that
theorists later found underneath: sets, symmetries, and a theorem about hexachords that turns out to be a fact
of crystallography.
*Covers:* free atonality; pitch-class sets under transposition and inversion; prime form; the interval vector;
Z-related sets; the hexachord theorem; rows and their forty-eight forms; invariance and combinatoriality; total
serialism; whether listeners can hear any of it.
*Built and computed:* the set classes derived by Burnside's lemma and checked against the published table; the
all-interval rows enumerated; the hexachord theorem verified exhaustively and proved on screen.
*Variation 29:* the Tune's intervals as the source of a row; a pointillist variation.
*Frontier:* homometric sets; perception studies of serial music.
*Reading:* Straus, *Introduction to Post-Tonal Theory*; Forte (1973); Babbitt's essays.

### Part 30 · Sound Itself (~55)
*Story:* 1948, a Paris radio studio: Pierre Schaeffer closes the groove of a disc of train noises and hears music.
1952: a pianist sits in silence for four minutes and thirty-three seconds. 1965: two tape loops of one preacher
drift apart. After the war composers stopped arranging notes and started arranging sound, chance and process.
*Covers:* musique concrète; chance and indeterminacy; the electronic studio; Xenakis's stochastic music and
sieves; sound masses; minimalism and phasing; spectral music (a spectrum orchestrated); early computer music.
*Built and computed:* a phasing engine and the resulting patterns it passes through; stochastic clouds from
Poisson onsets; the spectrum of our trombone model orchestrated for our ensemble.
*Variation 30:* the Tune phased against itself; as a cloud of glissandi; as the spectrum of Part 1's string.
*Frontier:* computer-assisted composition; sonification.
*Reading:* Xenakis, *Formalized Music*; Reich, *Writings on Music*; Fineberg (ed.) on spectral music; Ross, *The
Rest Is Noise*.

### Part 31 · Transformations (~50)
*Story:* A film score moves between two major chords that share no key and the audience feels wonder. Functional
harmony has nothing to say about it. Lewin's idea (1987) does: stop naming chords and name the moves between
them. The moves form a group, and the part computes it.
*Covers:* intervals as a group acting on a space; the T/I group on the twenty-four triads; P, L and R; the PLR
group and its duality with T/I; the Tonnetz as a torus; hexatonic and octatonic cycles; the long chain in
Beethoven's Ninth; third-related cycles in jazz (Part 39).
*Built and computed:* both groups built by brute force, their order and duality checked; shortest PLR paths.
*Variation 31:* the Tune harmonized by a walk on the Tonnetz.
*Frontier:* generalized Tonnetze; how listeners judge distance between triads.
*Reading:* Lewin (1987); Cohn, *Audacious Euphony*; Crans, Fiore & Satyendra (2009); Lehman, *Hollywood Harmony*.

### Part 32 · The Geometry of Chords (~55)
*Story:* In 2006 *Science* published a paper on music theory: the space of two-note chords is a Möbius strip. In
Tymoczko's geometry a voice leading is a path and its size is a length, and the familiar chords of Western music
sit exactly where short paths connect them to their own transpositions. That is why harmony and counterpoint
could be made to agree.
*Covers:* chords as unordered points; the orbifolds for two, three and four notes; voice-leading size;
near-evenness; the OPTIC symmetries; scales as chords; the Fourier transform of a pitch-class set and what each
coefficient hears.
*Built and computed:* chord space as an instrument; a minimal voice-leading solver; the DFT of every set class;
how close Bach's voice leadings are to minimal.
*Variation 32:* the Tune's harmony as a path, then rerouted through distant chords by the shortest steps.
*Frontier:* Fourier approaches to harmony; what the geometry does not explain.
*Reading:* Tymoczko (2006) and *A Geometry of Music*; Callender, Quinn & Tymoczko (2008); Amiot, *Music Through
Fourier Space*.

### Part 33 · The Mathematics of Rhythm and Scale (~55)
*Story:* An algorithm written to time pulses in a neutron accelerator turned out to generate the rhythms of
Cuba, Ghana, Bulgaria and Persia: it is Euclid's algorithm. The same mathematics makes scales. The part follows
it to a question about tiling the line that touches an open conjecture.
*Covers:* Euclidean rhythms and maximal evenness; well-formed scales and continued fractions; rhythmic oddity;
homometry; tiling canons and Vuza's aperiodic canons; de Bruijn sequences and Fibonacci numbers in Sanskrit
prosody; change ringing as walks on a Cayley graph; regular temperaments as linear maps with commas in the
kernel; the Bohlen–Pierce scale.
*Built and computed:* the Euclidean generator; a Vuza canon found and verified at period 72; a ringing method
generated; a temperament finder that rediscovers 12, 19, 31 and 53.
*Variation 33:* the Tune as a tiling canon; rung on bells; in Bohlen–Pierce.
*Frontier:* tilings and the spectral conjecture; open problems in mathematical music theory.
*Reading:* Toussaint, *The Geometry of Musical Rhythm*; Amiot; Hall's and Benson's surveys.

## Act VI · Many Musics

### Part 34 · Raga and Tala (~55)
*Story:* Near the end of a solo the player launches a phrase three times, and musicians and audience land
together on the first beat of the cycle. The tihai is arithmetic done in real time. The part learns the two
systems behind it: raga, which is far more than a scale, and tala.
*Covers:* the drone and the tanpura's buzzing bridge; swara and the shruti question, with measured intonation;
ascent, descent and characteristic phrases; gamaka; thaat and the seventy-two melakartas; alap, jor, jhala and
gat; tala cycles; the tihai equation; Hindustani and Carnatic practice; how it is taught.
*Built and computed:* a tihai solver; the melakarta table generated; a tanpura model; pitch histograms.
*Variation 34:* a study: the Tune's scale as Bilawal, an alap over the drone, then a gat with a tihai.
*Frontier:* computational raga analysis; intonation studies.
*Reading:* Jairazbhoy; Bor (ed.), *The Raga Guide*; Clayton, *Time in Indian Music*; the CompMusic studies.

### Part 35 · Maqam (~50)
*Story:* Cairo, 1932: a congress meets to fix the Arab scale in equal quarter tones, and the measurements show
that the best musicians play nothing of the kind. A thousand years earlier al-Fārābī had written the most
advanced treatise on tuning in the world. The part learns a system whose notes lie between the piano's keys.
*Covers:* al-Fārābī and Ṣafī al-Dīn's seventeen tones; the ajnas; the maqam families and their paths; neutral
intervals; modulation and the taqsim; Turkish theory in commas; the Persian dastgah; rhythmic cycles; the
instruments.
*Built and computed:* a maqam engine in cents; theory against published measurements; 24 and 53 equal divisions
as approximations, with their errors.
*Variation 35:* a study: the Tune in Rast, Bayati and Hijaz with a taqsim opening.
*Frontier:* computational makam analysis; standardization and its critics.
*Reading:* Marcus; Touma; Farhat; Signell; Bozkurt et al.

### Part 36 · Bronze and Silk (~55)
*Story:* In 1978 a tomb in Hubei, sealed in 433 BCE, gave up sixty-five bronze bells. Each sounds two notes,
depending on where it is struck, and their inscriptions are a tuning treatise older than Aristoxenus. The part
goes from those bells to the gamelan, an orchestra whose two halves are tuned apart on purpose so that the whole
shimmers.
*Covers:* the two-tone bell; generating the twelve lü; Jing Fang's sixty and the near-closing fifty-third; the
five modes; the guqin, its harmonics and its tablature; heterophony; gagaku; gamelan: slendro and pelog without a
standard, bronze spectra and their scales, paired tuning and beating, the gong cycle, interlocking parts.
*Built and computed:* a two-tone bell; Jing Fang's computation repeated; a bronze ensemble with designed beats;
a gong-cycle renderer and an interlocking splitter.
*Variation 36:* a study: the Tune for qin harmonics, then as balungan with interlocking elaboration.
*Frontier:* the acoustics and archaeology of the bells; measured gamelan tunings.
*Reading:* von Falkenhausen, *Suspended Music*; Tenzer, *Gamelan Gong Kebyar*; Sumarsam; Sethares ch. 10.

### Part 37 · Timelines (~50)
*Story:* One bell pattern, seven strokes in twelve pulses, is heard from Ghana to Cuba to Brazil. Written as
steps it reads 2-2-1-2-2-2-1: the major scale, turned into time. The part studies musics organized around such
timelines, and an instrument whose best-known melodies are played by no one: they form in the listener's ear.
*Covers:* the standard pattern; Ewe ensemble parts; three against two as a generating idea; the debate over how
to write and count it; interlocking and hocket; the mbira and its inherent patterns; the clave; samba; call and
response.
*Built and computed:* evenness, oddity and off-beatness for a table of timelines; inherent patterns predicted
by the streaming model.
*Variation 37:* a study: the Tune emerging as an inherent pattern from interlocking parts; then over a clave.
*Frontier:* non-isochronous subdivision measured; meter across cultures; archives and ethics.
*Reading:* Agawu, *Representing African Music*; Locke; Berliner, *The Soul of Mbira*; Arom; Toussaint.

### Part 38 · Blues and Swing (~55)
*Story:* "What is swing?" The proverbial answer is that if you have to ask you will never know. It can be
measured: the long-short ratio falls from about three to one in a slow tempo to even in a fast one, and soloists
place their downbeats late and their off-beats on time. The part builds the blues, ragtime and the swing band,
and a model that swings.
*Covers:* the twelve-bar form and its harmony; blue notes; call and response; ragtime and stride; the big band;
walking bass and ride pattern; seventh chords as the unit; guide tones; ii–V–I; turnarounds; the tritone
substitution.
*Built and computed:* a swing model fitted to published ratios; a guide-tone solver; Joplin rendered from the
score.
*Variation 38:* the Tune as a twelve-bar blues, a rag and a riff chart.
*Frontier:* microtiming studies of swing **(verify the 2022 paper)**; jazz corpora.
*Rights:* public-domain rags and blues; later standards by their changes and by original lines (§2.4).
*Reading:* Schuller, *Early Jazz*; Levine, *The Jazz Theory Book*; Friberg & Sundström (2002).

### Part 39 · Changes (~55)
*Story:* 5 May 1959. A pianist is handed a tune with twenty-six chords in sixteen bars, moving through three keys
a major third apart at nearly three hundred beats a minute, and the tape rolls. The part explains why those
changes are hard, shows them as a triangle on the Tonnetz of Part 31, and builds an improviser.
*Covers:* bebop and the contrafact; the bebop scale and why it lands chord tones on the beat; enclosures and
formulas; chord-scale theory; modal jazz; third-related cycles; reharmonization; quartal voicings; free jazz;
what improvisers are doing, cognitively.
*Built and computed:* an improviser (a phrase grammar constrained by chord scales and guide tones), judged by
the series' own analyzers; the bebop-scale claim proved and checked.
*Variation 39:* the Tune as a bebop head with an improvised chorus, then over third-cycle changes.
*Frontier:* pattern mining in solo corpora; machine improvisers; improvisation in the scanner.
*Reading:* Owens, *Bebop*; Berliner, *Thinking in Jazz*; Levine; the Weimar Jazz Database papers.

### Part 40 · The Song (~55)
*Story:* The average introduction of a hit single shrank from about twenty seconds in the 1980s to about five by
the 2010s. A stream that is skipped before thirty seconds pays nothing. The part follows the popular song from
the thirty-two-bar standard to the loop and the drop, and finds its form shaped by each technology that sold it.
*Covers:* AABA and verse-chorus; loops and rock harmony; riffs; the backbeat and groove; hooks and prosody;
funk; disco to house; the breakbeat, sampling and the drum machine; flow; the drop and the sidechain; corpus
studies of sixty years of charts.
*Built and computed:* chart statistics from open annotations **(verify licence)**; an 808 from first
principles; a flow analyzer on an original verse.
*Variation 40:* the Tune as a pop single, and as a beat that samples Variation 7.
*Frontier:* corpus studies; how short-video platforms are changing form **(verify)**.
*Rights:* statistics, skeletons and original songs (§2.4).
*Reading:* Temperley, *The Musical Language of Rock*; Ohriner, *Flow*; Serrà et al. (2012); Mauch et al. (2015).

## Act VII · The Craft

### Part 41 · Orchestration (~50)
*Story:* Ravel called *Boléro* (1928) a piece for orchestra without music: one melody, eighteen times, only the
instruments change. In one pass a horn, a celesta and two piccolos in different keys fuse into a single timbre
that no instrument has. Ravel is doing additive synthesis with players.
*Covers:* ranges, registers and transposition; loudness and brightness; blend, doubling and balance; why a
section is not one loud player; spacing; textures; melody of timbres; orchestration as a search problem.
*Built and computed:* the chorus effect of a section; a blend measure; a solver that matches a target spectrum
with combinations of our instruments.
*Variation 41:* the Tune in eight orchestrations, the last matched to a vowel.
*Frontier:* timbre research and computer-aided orchestration.
*Reading:* Adler; Rimsky-Korsakov; Berlioz; McAdams's work on blend.

### Part 42 · Composing (~50)
*Story:* Beethoven's sketchbooks show the "Ode to Joy" being found over years, draft after rejected draft. In
1757 Kirnberger published a way to compose minuets with dice; in 1957 a computer in Illinois wrote a string
quartet by generating notes and rejecting those that broke the rules. Composing is search under constraints, and
the part builds a searcher.
*Covers:* the operations on a motive; developing variation; kinds of variation; planning tension and pacing;
constraints as engines; dice games; the *Illiac Suite*; grammars, automata and evolution; Cope's experiments;
what creativity might mean.
*Built and computed:* a dice-game engine with its count of distinct pieces; a generate-and-test composer that
uses Act III's checkers as critics, with its rejected drafts kept.
*Variation 42:* a variation composed by the searcher, shown with what it threw away.
*Frontier:* evaluating computational creativity; co-creative tools.
*Reading:* Schoenberg, *Fundamentals of Musical Composition*; Hiller & Isaacson (1959); Boden.

### Part 43 · Performing (~55)
*Story:* In 2007 a critic put a celebrated pianist's CD into a computer and the track database named another
pianist. Over a hundred recordings released under Joyce Hatto's name were other people's, and timing analysis
proved it: no two humans shape time the same way. The part asks what a performer adds to the notes, and
measures it in milliseconds.
*Covers:* expressive timing and its models; dynamics; articulation; vibrato; intonation in practice; ensemble
synchronization as phase correction; the conductor; practice and what the evidence says about it; memory and
anxiety; injury and hearing.
*Built and computed:* an expressive performer on rule-based and kinematic models; an ensemble simulation with
its stability bounds; a Hatto-style identity test on tempo curves.
*Variation 43:* the Tune as written and as performed, same notes, the differences drawn.
*Frontier:* learned models of expression; ensemble coordination.
*Reading:* Gabrielsson's reviews; Friberg, Bresin & Sundberg (2006); Wing et al. (2014); Repp's studies.

### Part 44 · Music for Picture and Play (~50)
*Story:* One animated scene, three scores, three different films. Then a problem film composers never had: in a
game nobody knows how long the scene will last. The part works the arithmetic of hitting a cut on the beat and
builds a score that rearranges itself.
*Covers:* what music does to an image; leitmotifs; spotting and hit points; click-track arithmetic; harmony and
affect on screen; mixing against dialogue; game music: resequencing, layering, transitions, stingers; chiptune
under three-channel limits; middleware.
*Built and computed:* a tempo finder that hits three sync points; an adaptive score as a state machine driven by
a simulated game; a three-channel chip synthesizer.
*Variation 44:* the Tune as a cue, as a leitmotif in three moods, and as an adaptive loop.
*Frontier:* generative and adaptive scoring; the cognition of film music.
*Reading:* Karlin & Wright, *On the Track*; Lehman, *Hollywood Harmony*; Collins, *Game Sound*.

## Act VIII · The Mind

### Part 45 · The Scene (~50)
*Story:* Send jumping notes to each ear and the listener hears two smooth scales, one on each side, which neither
ear was given (Deutsch, 1973; `headphones`). The ear receives one pressure wave and the mind returns a scene of
separate voices. The part builds the rules of that separation and shows the rules of Part 16 falling out of them.
*Covers:* sequential and simultaneous grouping; streaming and its boundary; continuity; timbre space; pitch
models; octave equivalence; absolute and relative pitch; pitch memory; the illusions.
*Built and computed:* a streaming model against published boundaries; a timbre space of Monochord's own
instruments.
*Variation 45:* the Tune interleaved with another melody and inaudible, then released by timbre.
*Frontier:* deep networks as models of auditory cortex; absolute pitch.
*Reading:* Bregman, *Auditory Scene Analysis*; Deutsch (ed.), *The Psychology of Music*; McAdams.

### Part 46 · Expectation and Emotion (~50)
*Story:* In 2011 a PET study caught dopamine being released twice: at the moment of a musical chill, and in the
seconds of anticipation before it. Meyer had argued in 1956 that musical emotion is expectation delayed and
fulfilled. The part builds a listener model and engineers three endings for the Tune.
*Covers:* Meyer; statistical learning; surprise and uncertainty and their interplay; brain responses to syntax;
tension; groove and syncopation; the cues of expressed emotion; the pleasure of sad music; preference and
complexity; what does not replicate.
*Built and computed:* a variable-order listener model; surprise and entropy curves across the Variations;
published data points beside the model's.
*Variation 46:* the Tune with three endings: expected, delayed, denied.
*Frontier:* predictive-processing accounts; models as listeners.
*Reading:* Meyer (1956); Huron (2006); Salimpoor et al. (2011); Cheung et al. (2019); Witek et al. (2014).

### Part 47 · Origins and Universals (~55)
*Story:* A flute carved from a vulture's wing bone lay in a German cave for some 40,000 years. Every known
society makes music, and no one agrees why. The part sorts what is shared (discrete pitches, a beat, small-integer
rhythms, the lullaby) from what is not (a taste for consonance), and watches a tune evolve in simulated mouths.
*Covers:* the cross-cultural evidence; theories of origin; birdsong, whales and a dancing cockatoo; infants and
enculturation; music and language; amusia; the Mozart effect and what transfer studies show; therapy evidence;
cultural evolution and tune families.
*Built and computed:* an iterated-learning simulation; rhythmic variability of themes by composers' language,
recomputed on the Library; a family tree of the Tune's relatives by edit distance.
*Variation 47:* the Tune after thirty generations of imperfect transmission.
*Frontier:* large cross-cultural datasets; the genetics of rhythm **(verify)**; the origins debate.
*Reading:* Patel, *Music, Language, and the Brain*; Savage et al. (2015); Mehr et al. (2019); Honing (ed.), *The
Origins of Musicality*.

## Act IX · Electric Sound

### Part 48 · Digital Audio (~50)
*Story:* Why 44,100 samples a second? Because the first digital recorders stored audio on video cassettes: three
samples a line, 245 lines, 60 fields. Behind the accident is a theorem that sounds impossible: a smooth wave can
be recovered exactly from its samples. The part proves it and then listens to one-bit audio.
*Covers:* the sampling theorem; aliasing; reconstruction and the stair-step myth; quantization noise and the six
decibels per bit; dither; noise shaping; delta-sigma conversion; jitter; resampling; the high-resolution debate.
*Built and computed:* converters simulated; error spectra with and without dither; a delta-sigma modulator's
noise shaping measured.
*Variation 48:* the Tune at 16, 8, 4 and 1 bit, with and without dither (shown as residues; §3).
*Frontier:* converter limits; sampling beyond Nyquist.
*Reading:* Pohlmann; Lipshitz, Wannamaker & Vanderkooy (1992); Smith, *Mathematics of the DFT*.

### Part 49 · Filters, Delay and Reverb (~55)
*Story:* In 1947 an engineer put a loudspeaker and a microphone in the studio's tiled bathroom and sold the echo
as art. In 1962 Schroeder at Bell Labs built a room out of arithmetic: four comb filters and two all-passes.
Everything an effect rack does is delay and addition.
*Covers:* impulse responses and convolution; poles and zeros; equalizers; phase; analog prototypes; combs,
flangers, choruses and phasers; the room's response; Schroeder's reverberator; feedback delay networks; plates
and springs; convolution reverb and sweep measurement.
*Built and computed:* the filter and reverb modules; a plate by finite differences; a room response measured by
sweep in our own simulated room and compared with Sabine.
*Variation 49:* the Tune dry, then in a bathroom, a plate, a spring and a cathedral.
*Frontier:* virtual analog; differentiable effects.
*Reading:* Smith, *Introduction to Digital Filters* and *Physical Audio Signal Processing*; Zölzer, *DAFX*;
Välimäki et al. (2012).

### Part 50 · Dynamics, Distortion and Pitch (~55)
*Story:* Two accidents made two genres. A damaged amplifier in 1951 gave rock its fuzz. In 1998 a pitch corrector,
invented by a geophysicist who had used autocorrelation to find oil, was set to act instantly, and the sound of a
voice snapping between notes became a style.
*Covers:* nonlinearity and new frequencies; Chebyshev waveshaping; intermodulation and the power chord; aliasing
in nonlinear effects; compressors, limiters and gates; sidechains; time and pitch: resampling, overlap-add, the
phase vocoder, PSOLA; formants; pitch correction; vocoders and ring modulation.
*Built and computed:* a compressor with measured curves; a shaper with exact harmonics; a phase vocoder; a pitch
corrector for Part 8's voice.
*Variation 50:* the Tune sung, hard-tuned, vocoded and stretched eightfold.
*Frontier:* neural models of analog gear; antialiasing nonlinearities.
*Reading:* Zölzer; Giannoulis, Massberg & Reiss (2012); Laroche & Dolson (1999).

### Part 51 · Synthesis I: Oscillators and Filters (~50)
*Story:* The first synthesizer weighed two hundred tons. Cahill's Telharmonium (1906) made tones with dynamos and
sent them down telephone lines to subscribers, and it failed. Sixty years later a module the size of a book did
the same job, and *Switched-On Bach* sold a million copies.
*Covers:* additive synthesis from organ to Hammond; subtractive synthesis; why digital sawtooths alias and how
to stop it; the ladder filter; envelopes; modulation; sync and pulse width; unison; wavetables; drum circuits.
*Built and computed:* an analog-modelled voice with alias levels measured; the ladder against its circuit
equations; fitting a patch to a target spectrum.
*Variation 51:* the Tune as a multitracked "switched-on" arrangement.
*Frontier:* sound matching by learning; differentiable synthesizers.
*Reading:* Roads, *The Computer Music Tutorial*; Pirkle; Välimäki & Huovilainen (2006); Pinch & Trocco, *Analog
Days*.

### Part 52 · Synthesis II: FM, Grains and Physical Models (~55)
*Story:* In 1967 John Chowning turned a vibrato up until it was faster than the note itself and heard bells. The
mathematics is a Bessel function per sideband, the patent made Stanford a fortune, and the DX7 (1983) put the
sound on every record of its decade. The part builds FM, then two other ways out of the oscillator.
*Covers:* frequency modulation and its sidebands; ratios and inharmonicity; operators and algorithms; granular
synthesis from Gabor to Roads; spectral models; samplers; Karplus–Strong; digital waveguides (d'Alembert again);
modal synthesis; what each method costs and controls.
*Built and computed:* an FM engine with sidebands checked against Bessel functions; a granular engine; waveguide
and modal instruments compared with Part 7's finite-difference string as the reference.
*Variation 52:* the Tune on FM keys and bells, dissolved into grains and back.
*Frontier:* neural and differentiable physical models.
*Reading:* Chowning (1973); Karplus & Strong (1983); Smith, *Physical Audio Signal Processing*; Roads,
*Microsound*.

### Part 53 · MIDI, Sequencers and the DAW (~55)
*Story:* January 1983, a trade-show floor: two synthesizers from rival firms are joined by a five-pin cable, and
a key pressed on one sounds the other. The specification fitted on a few pages and has run the industry for forty
years. The part reads it byte by byte, then builds what sits on top: the sequencer and the audio engine with its
hard real-time deadline.
*Covers:* automata, music boxes and player pianos; Nancarrow; MUSIC N and unit generators; the MIDI protocol and
its limits; MPE and MIDI 2.0 **(verify)**; step sequencers, piano rolls and trackers; the audio callback;
latency; the processing graph and delay compensation; plug-ins; dataflow and live-coding languages.
*Built and computed:* a sequencer and audio graph, identical offline and in blocks, with its per-block cost
`measured on this machine`; a MIDI file reader and writer; a small pattern language.
*Variation 53:* the Tune as a tracker module and as a tempo canon no human could play.
*Frontier:* learning in the audio thread; networked performance.
*Reading:* the MIDI 1.0 specification; Mathews, *The Technology of Computer Music*; Puckette; McCartney (2002).

## Act X · The Studio and the Stage

### Part 54 · Microphones and Loudspeakers (~50)
*Story:* Plug headphones into a microphone socket and speak into them: they work. A loudspeaker is a microphone
run backwards. When microphones became electrical in 1925, singers no longer had to fill a hall, and the
intimate voice of the crooner was invented. A transducer changed what a voice could be.
*Covers:* the transduction principles; electrical, mechanical and acoustical circuits; polar patterns; the
proximity effect; noise; balanced lines; the loudspeaker as a filter; Thiele–Small parameters; sealed and ported
boxes (Part 2's resonator again); horns; crossovers; amplifiers; headphones and noise cancelling.
*Built and computed:* a lumped-element simulator checked against closed-form alignments; polar patterns and
proximity derived and drawn; an adaptive canceller.
*Variation 54:* the Tune through three microphone patterns and three loudspeakers.
*Frontier:* arrays and beamforming; loudspeaker linearization.
*Reading:* Eargle, *The Microphone Book*; Small's papers; Beranek & Mellow.

### Part 55 · Rooms and Space (~55)
*Story:* In 1895 Harvard opened a lecture hall in which nobody could understand a word. A young physicist,
Wallace Sabine, spent his nights there with a stopwatch, an organ pipe and the seat cushions of a nearby theatre,
found the law of reverberation, and used it to design Boston's Symphony Hall. Sixty years on, a hall designed
with far more science had to be gutted. The part explains both.
*Covers:* modes; the diffuse field; Sabine and Eyring; absorption and diffusion (and the number theory in a
diffuser); early reflections and spaciousness; hall shapes; simulation by images and rays; localization cues;
stereo; panning laws; Ambisonics; wave-field synthesis; binaural rendering; object audio.
*Built and computed:* an image-source room against Sabine and the exact modes; a diffuser's scattering; panning
and Ambisonic decoders; a binaural renderer.
*Variation 55:* the Tune walked through four spaces, then circling the listener (`headphones`).
*Frontier:* personalized HRTFs; real-time wave simulation.
*Reading:* Kuttruff, *Room Acoustics*; Beranek, *Concert Halls and Opera Houses*; Blauert, *Spatial Hearing*;
Zotter & Frank.

### Part 56 · Recording and Mixing (~55)
*Story:* Take one multitrack recording and mix it three times: close and dry, a wall of sound, a dub. It is three
different pieces of music. Since the 1960s the studio has been an instrument, and the part learns to play it.
*Covers:* the history from the horn to the workstation; stereo microphone arrays and their arithmetic; phase
between microphones; gain staging; editing; balance; panning; masking between tracks; dynamics and buses; depth
and width; monitoring; automatic mixing.
*Built and computed:* the mixer, with pan laws checked; localization curves of the stereo arrays; a masking map;
an automatic mix against ours.
*Variation 56:* the session: our instruments recorded with virtual microphones and mixed three ways.
*Frontier:* intelligent music production; differentiable consoles.
*Reading:* Izhaki, *Mixing Audio*; Senior; Milner, *Perfecting Sound Forever*; De Man, Stables & Reiss.

### Part 57 · Mastering and Loudness (~50)
*Story:* In 2008 fans of a rock band found that the version of its new album inside a video game sounded better
than the CD, which had been mastered so loud that the peaks were shaved flat. The loudness war had a casualty
with waveforms to prove it. Then streaming services began turning loud records down, and the incentive vanished.
*Covers:* what mastering is for; the chain; inter-sample peaks; meters; BS.1770, LUFS and gating; normalization;
the war in numbers; level-matched comparison as method; dither to delivery; vinyl's equalization and geometry;
delivery formats; this series' own mastering chain, explained and measured.
*Built and computed:* a gated loudness meter and a true-peak meter agreeing with ffmpeg; a limiter; one mix
mastered at six loudness levels, then normalized.
*Variation 57:* an album side of Variations, and one of them "war-mastered" beside itself, level-matched.
*Frontier:* loudness and listener preference: what experiments found.
*Reading:* Katz, *Mastering Audio*; ITU-R BS.1770; EBU R 128; Deruty & Tardieu (2014).

### Part 58 · Compression for the Ear (~55)
*Story:* The engineer tuning the first MP3 encoder tested it on an unaccompanied voice, Suzanne Vega's "Tom's
Diner", because it sounded dreadful. Twelve years of research into what the ear cannot hear produced a file a
tenth the size, and a few years later that file broke the record industry's business.
*Covers:* entropy and lossless coding by prediction; masking thresholds; the MDCT and why its aliases cancel;
window switching and pre-echo; bit allocation; stereo coding; MP3, AAC and Opus; listening tests and their
statistics; transcoding; neural codecs and residual vector quantization.
*Built and computed:* a lossless coder with bit-exact round trip; a perceptual codec on Part 4's masking model;
the cancellation verified to machine precision; the power of an ABX test.
*Variation 58:* the Tune at five bitrates, and the residue the codec discards, played alone.
*Frontier:* neural codecs; learned perceptual metrics.
*Reading:* Bosi & Goldberg; Brandenburg (1999); Valin et al. on Opus; Sterne, *MP3: The Meaning of a Format*.

### Part 59 · Live Sound (~50)
*Story:* August 1965: fifty-five thousand people fill a baseball stadium and nobody, including the band, can hear
the band. The modern concert system was built to solve that night. The part works out why a microphone howls,
why speakers are hung in curved lines, and how loud is too loud.
*Covers:* gain before feedback and the stability criterion; ringing out; monitors; point and line sources;
arrays, lobes and curvature; subwoofer arrays; delay towers; wind and temperature; measurement with transfer
functions; wireless planning; networks and clocks; intelligibility; noise dose and protecting hearing.
*Built and computed:* field maps of arrays; a feedback loop that predicts its howl; an intermodulation-free
channel planner; a dose calculator.
*Variation 59:* the Tune at an arena: front of house, the back row, the car park.
*Frontier:* steered arrays; immersive live systems; festival noise control.
*Reading:* McCarthy, *Sound Systems: Design and Optimization*; Davis & Patronis; Ballou.

### Part 60 · The Business of Music (~55)
*Story:* Follow one stream's fraction of a cent from a phone to a songwriter. On the way it passes two
copyrights, four kinds of licence and half a dozen intermediaries, each created when a new machine (the player
piano, radio, the sampler, the file, the model) broke the old arrangement.
*Covers:* the two copyrights and their rights; collecting societies; deals, advances and recoupment; the
streaming pool and how to divide it; superstars and power laws; social influence and unpredictability; charts;
the cost disease of live performance; ticket pricing; similarity lawsuits and how many melodies there are;
sampling; AI and rights; the map of careers. Everything dated, with jurisdiction, and labelled as not legal
advice.
*Built and computed:* a royalty waterfall on illustrative terms; pro-rata against user-centric division on a
simulated population; a cumulative-advantage market; the chance that two independent melodies coincide, from
Part 14's model.
*Variation 60:* the Tune's own family of copyrights, and a variation's statement after a million simulated
streams.
*Frontier:* payout reform; training-data litigation and licensing **(verify, dated)**.
*Reading:* Passman; Krueger, *Rockonomics*; Salganik, Dodds & Watts (2006); Baumol & Bowen (1966).

## Act XI · Listening Machines

### Part 61 · Pitch, Onsets and Transcription (~55)
*Story:* The fourteen-year-old Mozart is said to have written out a guarded nine-voice choral work after one
hearing. Making a machine do that has been called the holy grail of music computing. Monochord gives us what the
field lacks: unlimited audio with a perfect answer key.
*Covers:* representations for pitch; autocorrelation and YIN; salience; onset detection; non-negative matrix
factorization and its updates; neural transcription; from notes to a readable score; evaluation.
*Built and computed:* YIN with accuracy against noise; onset detection; NMF and a small network on Monochord
renders, scored on a timbre they never heard.
*Variation 61:* the Tune performed, transcribed and re-rendered, five times round.
*Frontier:* multi-instrument transcription **(verify current results)**; score-level output.
*Reading:* Müller; de Cheveigné & Kawahara (2002); Smaragdis & Brown (2003); Benetos et al. (2019).

### Part 62 · Beat, Chords and Structure (~55)
*Story:* A child can clap along; a program could not do it reliably for decades, and still taps at half or
double speed. The part builds the listeners that make DJ software, practice apps and accompaniment systems work,
ending with an accompanist that follows a soloist's rubato.
*Covers:* novelty curves and tempograms; beat tracking by dynamic programming; downbeats; time warping and score
following; chroma; chord recognition with a hidden Markov model (Part 18's matrix as the prior); structure by
spectral clustering; cover-song detection; annotator disagreement as a ceiling.
*Built and computed:* a beat tracker scored on performances with known beats; an aligner's error in
milliseconds; chord recognition with and without the prior; structure boundaries on Variation 21.
*Variation 62:* Variation 40 heard by the machine, then Variation 43 accompanied live.
*Frontier:* expressive and non-Western meter; joint models **(verify)**.
*Reading:* Müller; Ellis (2007); McFee & Ellis (2014); Dannenberg & Raphael (2006).

### Part 63 · Finding Music (~55)
*Story:* In 2002 a Londoner could dial four digits, hold a phone up in a noisy bar, and receive the song's name
by text. Matching ten bad seconds against millions of tracks was done with spectrogram peaks and a hash table.
The part builds it, then the systems that decide what a billion people hear next.
*Covers:* fingerprinting and its false-match arithmetic; tagging and embeddings; the benchmark that turned out
to be flawed, and classifiers that were right for the wrong reasons; collaborative filtering and implicit
feedback; cold start; exploration; popularity feedback; fairness; metadata.
*Built and computed:* a fingerprinter over every sound in the series, with recognition against noise and
bitrate; a recommender on simulated listeners whose tastes are known; a feedback-loop simulation.
*Variation 63:* any five noisy seconds named; all the Variations ordered into one smooth playlist.
*Frontier:* music foundation models **(verify)**; creator-side effects of recommendation.
*Reading:* Wang (2003); Hu, Koren & Volinsky (2008); Sturm (2013); Schedl et al. (2018).

### Part 64 · Source Separation (~55)
*Story:* In 2023 a voice was lifted off a 1970s home cassette, away from the piano recorded on the same
track, and a finished song was built around it **(verify details)**. Separation is the un-baking of a cake. We
own the ingredients, so the part can say exactly how well it was done.
*Covers:* the mixing model; panning and centre cancellation; independent components; harmonic against
percussive; factorization; masks, the Wiener filter and oracle bounds; the phase problem; networks on
spectrograms and on waveforms; metrics and their faults; what it is used for.
*Built and computed:* oracle bounds on our multitracks; median-filter, factorization and a small network
(named exception: up to 6 h, resumable) placed against them.
*Variation 64:* a mashup from separated stems of four earlier Variations, beside the same from true stems.
*Frontier:* generative and query-based separation; metrics that track perception.
*Reading:* Vincent, Virtanen & Gannot (eds.); Rafii et al. (2018); Le Roux et al. (2019); Défossez et al.

### Part 65 · Machines that Compose (~55)
*Story:* In 1997 an audience heard three pieces: one by Bach, one by a music professor in Bach's style, one by a
program. They took the program's for Bach. The part builds generators from a Markov chain to a transformer and
measures the trade nobody escapes: a model that copies less also coheres less.
*Covers:* n-gram models and the novelty-plagiarism curve; constraints; grammars; recombination; recurrent
networks; token representations; DeepBach's sampling; the Music Transformer's relative attention; infilling;
control; evaluation and its pitfalls; memorization.
*Built and computed:* Markov models of orders 1–8 on the chorales; a small transformer (on *AI, Built*'s pocket
language model) on public-domain tunes; samples judged by Acts II–III's analyzers; the longest copied passage.
*Variation 65:* the Tune's first phrase continued at five temperatures, uncurated and labelled.
*Frontier:* long-range form; control; attribution.
*Reading:* Hiller & Isaacson; Cope; Hadjeres et al. (2017); Huang et al. (2018); Briot et al., *Deep Learning
Techniques for Music Generation*.

### Part 66 · Generative Audio (~60)
*Story:* In 2016 a network generated sound one sample at a time, sixteen thousand decisions a second, and its
piano noodled nowhere. Eight years later a line of text returned a finished song with a singer, and the record
labels went to court **(verify, dated)**. The part explains the three ideas that closed the gap and builds the
smallest honest version of each.
*Covers:* why raw audio is hard; autoregression on samples; spectrograms and vocoders; discrete tokens and
neural codecs; language models over tokens; diffusion and flow models in a latent space; differentiable DSP;
singing synthesis and voice cloning; evaluation; watermarking and detection; data, consent and what is unsolved.
*Built and computed:* a DDSP instrument trained on our own bowed-string model; a token model on a
Monochord-rendered corpus (named exception: up to 8 h, resumable); a Fréchet-style distance; a memorization test.
Quality is reported as it is.
*Variation 66:* the Tune sung, re-rendered as a violin by the DDSP model, and continued by the token model.
*Frontier:* the frontier is the subject: swept at the writing date.
*Reading:* van den Oord et al. (2016); Engel et al. (2020); Zeghidour et al. (2021); Agostinelli et al. (2023);
Copet et al. (2023).

## Act XII · Coda

### Part 67 · Doing Research in Music (~50)
*Story:* In 1993 a study of thirty-six students reported that ten minutes of Mozart raised a spatial score, and
within five years a governor was sending classical CDs to every newborn in his state. The effect did not
replicate. In another corner of the field a benchmark dataset used in a hundred papers turned out to contain
duplicates and mislabels. The part asks how each kind of music research knows what it claims.
*Covers:* sources, editions and attribution; analysis as argument and the corpus turn; fieldwork, transcription
and ethics; experiments, psychophysics and online studies; listening tests; dataset leakage and annotator
ceilings; measurement standards; practice as research; reading a paper in each subfield; finding a problem.
*Built and computed:* the series audits itself: every computed verdict of Parts 1–66 re-run across seeds with
intervals; a listening test's power; corpus results on the canon against the wider Library; a leakage
demonstration; a manuscript family tree recovered; the Mozart-effect literature as a funnel plot using
`explainer.stats.kit`.
*Variation 67:* the critical edition of the Variations: sources, variants, errata.
*Frontier:* the map of open problems, built from every part's ★.
*Reading:* Clarke & Cook (eds.), *Empirical Musicology*; Nettl, *The Study of Ethnomusicology*; Sturm (2014);
Pietschnig et al. (2010).

### Part 68 · The Variations (~60; the finale)
*Story:* Bach's *Goldberg Variations* end by playing the opening aria again, the same notes, and it does not
sound the same. The series runs its whole chain once, from a score to a listener and back to a score, measures
what survives the journey, and then plays the suite. It ends on one string.
*Covers:* ordering sixty-seven variations into a piece; the chain end to end: score, performer, instruments,
room, microphones, mix, master, codec; then the return: transcription, beat and chords, identification; what the
chain preserves (pitch and time) and what it loses (timbre and space), and why notation chose as it did; what was
built; what is still unknown about the question of Part 1.
*Built and computed:* a suite assembler; the round-trip error from score to sound to score at each bitrate; the
final ledger; Monochord's layers, tests and references in one table.
*Heard and seen:* the suite, ten to twelve minutes, every instrument of §4 running; then Variation 1 again.

## 6. What must exist before Part 1

| Item | Where | Notes |
|---|---|---|
| The sound layer: clips, `SoundScene`, cue sheets | `explainer/music/sound.py` | §3 |
| A music mastering profile and stem mixing | `tools/build.py` | narration-only high-pass; fixed music gain; peak gate |
| Sound QA | `tools/qa_sound.py`, `tools/dead_air.py` | sync, overlap, peaks, silence, phone audition |
| Listening time in the length estimate; floor 30, ceiling 60 | `tools/lecture_length.py` | reads cue sheets |
| The engraver | `explainer/music/staff.py` (`Staff`), `explainer/music/notations.py` | the series' own, on the installed FreeSerif music symbols (Part 10); Verovio or LilyPond behind the same interface if the owner chooses (§9) |
| Series registration | `explainer/paths.py`, `tools/series_site.py`, `tools/make.py`, `tests/test_series_site.py` | when Part 1 lands |
| Sound in interactives | the widget core, `tools/check_widgets.js` | Web Audio, started by a click |
| Optional test references | `pyproject.toml` extra `music-qa` | `librosa`, `mir_eval`; never needed to build a film |
| Chapter cards with the Chain and timeline | `explainer/music/cards.py` | |

## 7. Phases

Production is sequential: one agent, one part at a time, in order, with no parallel fleets. Each part is finished
(computed, previewed at 480p, gates clean, course material written) before the next is opened.

- **Phase 0, the pipeline.** Build §6. Prove it on a two-minute test film: a tone, a click track against flashes,
  an engraved bar with a playhead, a stereo pan, a listening window, a master that passes the gates on macOS and
  Linux.
- **Phase 1, two pilots.** Part 1 (physics and sound) and Part 16 (score, voices and a generator). Their lessons
  go into `videos/music/LECTURE_GUIDE.md`, the working guide for the series.
- **Phase 2, Acts I–III** (Parts 2–15, 17–22): the foundation every later part calls on.
- **Phase 3, Acts IV–VIII** (Parts 23–47), each act opened with its frontier sweep and chapter lists, and for Act
  VI a sources review per tradition.
- **Phase 4, Acts IX–X** (Parts 48–60): Monochord becomes a studio.
- **Phase 5, Act XI and the Coda** (Parts 61–68).
- **Phase 6, masters.** Narrated masters, the Chinese edition if confirmed, the course site with players.

## 8. Progress

| Date | What landed |
|---|---|
| 2026-11-13 | The plan (this file and `README.md`). |
| 2026-11-13 | **Phase 0**: the clip store and loudness meter, `SoundScene` and cue sheets, stem mixing and the music master in `tools/build.py`, `tools/qa_sound.py`, Monochord's first layer (the stiff, lossy, stretching string, checked three ways), the scene instruments of §4 that Part 1 needs, and the test film `videos/music/soundcheck/` (picture-to-sound offsets within one frame). |
| 2026-11-13 | **Part 1, *One String***: 15 chapters, 46.9 min narrated (English, 480p preview) of which 3.4 min listening in 40 windows; 3 pause-and-listen questions and a worked example with a predict-pause; Variation 1; Lab 1 and the plucked-string interactive; every gate clean, the narration listen-tested (`tools/check_narration.py`). Lessons in `LECTURE_GUIDE.md`. |
| 2026-11-13 | **Part 2, *Waves in Air***: 14 chapters, 33.5 min narrated of which 1.9 min listening in 18 windows; 3 pause-and-listen questions, 3 worked examples with predict-pauses; Variation 2 (six bottles); Lab 2 and the bottle interactive; Monochord's air layer (`physics/air.py`: gas parcels, sound in a plane, tubes; `tests/music/test_air.py`); the kits for later parts (`monochord/partkit.py`, `explainer/music/kit.py`, `tests/music/partcheck.py`); every gate clean, narration listen-tested. |
| 2026-11-13 | **Part 3, *The Spectrum***: 13 chapters, 32.5 min narrated of which 1.8 min listening in 15 windows; 3 pause-and-listen questions, 2 worked examples with predict-pauses; Variation 3 (additive); Lab 3 and the Fourier-sum interactive; Monochord's analysis layer (`dsp/fourier.py`: FFT, windows, STFT, constant Q, uncertainty, noise, reassignment; `tests/music/test_fourier.py`); every gate clean, narration listen-tested. |
| 2026-11-13 | **Part 4, *The Ear***: 13 chapters, 48.1 min narrated of which 1.9 min listening in 16 windows; 6 pause-and-listen questions, 4 demonstrations to listen for, 8 worked examples with predict-pauses; Variation 4 (no fundamentals, then no octaves); Lab 4 and the missing-fundamental interactive; Monochord's ear (`monochord/ear.py`: middle ear, long-wave cochlea, gammatone bank, threshold and masking, nerve and autocorrelation pitch, Shepard tones, noise dose, Hopf oscillator; `tests/music/test_ear.py`); shared scene helpers moved into `explainer/music/kit.py`; every gate clean, narration listen-tested. Forward references in Parts 2 and 3 corrected to the syllabus numbering. |
| 2026-11-13 | **Part 5, *Consonance***: 12 chapters, 38.7 min narrated of which 2.5 min listening in 16 windows; 6 pause-and-listen questions, 3 demonstrations to listen for, 3 worked examples with predict-pauses; Variation 5 (a bent timbre and its own intervals); Lab 5 and the dissonance-curve interactive; Monochord's consonance layer (`monochord/consonance.py`: Euler's gradus, beats, the Plomp–Levelt curve, dissonance curves, stretched partials, harmonicity, the fundamental bass; `tests/music/test_consonance.py`); every gate clean, narration listen-tested. |
| 2026-11-13 | **Part 6, *Tuning***: 12 chapters, 37.3 min narrated of which 2.3 min listening in 16 windows; 4 pause-and-listen questions, 4 demonstrations to listen for, 6 worked examples with predict-pauses; Variation 6 (the Tune with chords in eight tunings); Lab 6 and the temperament interactive; Monochord's tuning layer (`monochord/tuning.py`: commas, Pythagorean, just, meantone, Werckmeister III, equal divisions, continued fractions, beat rates, the comma pump, stretched octaves; `tests/music/test_tuning.py`, against Barbour's tables); sustained-tone helpers in `partkit.py`; every gate clean. |
| 2026-11-13 | **Part 7, *Strings, Hammers and Bows***: 12 chapters, 39.2 min narrated of which 1.7 min listening in 12 windows; 5 pause-and-listen questions, 1 demonstration to listen for, 4 worked examples with predict-pauses; Variation 7 (a guitar, a piano and a violin from one string); Lab 7 and the bowed-string interactive (Schelleng's wedge, simulated in the page); Monochord's string instruments (`instruments/strings.py`: Karplus–Strong, a felt hammer on a stiff string, coupled unisons, a bowed string with stick-slip friction, Schelleng's limits, the two-mass guitar, bodies as banks of resonances; `tests/music/test_strings.py`); every gate clean, narration listen-tested. |
| 2026-11-13 | **Part 8, *Pipes, Reeds and Voices***: 12 chapters, 40.6 min narrated of which 1.6 min listening in 15 windows; 6 pause-and-listen questions, 6 demonstrations to listen for, 4 worked examples with predict-pauses; Variation 8 (a flute, a clarinet, a saxophone, a trumpet and a voice, each tuned by being built, blown and trimmed); Lab 8 and the vowel interactive (a two-tube mouth, its formants computed in the page); Monochord's winds (`instruments/winds.py`: bores by transfer matrices with wall losses and radiation, reflection functions, a reed valve, a lip valve, a jet, a source-filter voice, formants of tubes; `tests/music/test_winds.py`); every gate clean, narration listen-tested. |
| 2026-11-13 | **Part 9, *Drums, Bars and Bells***: 12 chapters, 34.1 min narrated of which 1.8 min listening in 16 windows; 5 pause-and-listen questions, 7 demonstrations to listen for, 3 worked examples with predict-pauses; Variation 9 (marimba, bells, steelpan and kettledrums); Lab 9 and the drum interactive (where a skin is struck, bare, as a kettledrum and as a tabla); Monochord's percussion (`instruments/percussion.py`: Bessel modes, a finite-element membrane for any polygon with the isospectral drums of 1992 computed and checked against Driscoll's values, a loaded membrane, a beam solver for carved bars, bells from published partials, Chladni figures, gliding gongs, modal synthesis; `tests/music/test_percussion.py`); every gate clean, narration listen-tested. **Act I is complete.** The engraver pilot for Part 10 could not be run in this session: installing Verovio's wheel was refused by the session's permission policy, so the choice of engraver (§9, item 5) is still the owner's to make. |
| 2026-11-14 | **Part 10, *Writing It Down***: 12 chapters, 37.7 min narrated of which 3.4 min listening in 12 windows; 4 pause-and-listen questions, 5 demonstrations to listen for, 1 predict-pause; Variation 10 (the Tune read from ten notations, two to a phrase, and a sixth phrase played by four rules of performance); Lab 10 and the notation interactive (every melody that fits a row of neumes, on a staff, as a piano roll and in numbers); Monochord's score (`monochord/score/`: spelled pitches and exact durations, MusicXML, MEI, MIDI, ABC, LilyPond and jianpu writers, MusicXML and MIDI readers, contour counts, tablature by dynamic programming, figured-bass realizations, Franco's rules, performance rules, a toy page reader; `tests/music/test_score.py`, `test_notations.py`); every gate clean, narration listen-tested. **The engraver:** with Verovio not installable in this session, the series now has its own (`explainer/music/staff.py`, tested in `tests/music/test_staff.py`): one voice to a staff, clefs, key and time signatures, beams, dots, ties, accidentals, ledger lines, rests and words, drawn from the installed FreeSerif music symbols, with a time-to-page map for cursors. It needs no new dependency; it has no chords, slurs or second voices yet, and can be replaced behind the same `Staff` interface if the owner prefers Verovio (§9, item 5). Part 9's closing line about Guido was corrected (a year or two in place of ten) and its film rebuilt. |
| 2026-11-14 | **Part 11, *Rhythm and Meter***: 12 chapters, 31.6 min narrated of which 4.8 min listening in 19 windows; 5 pause-and-listen questions, 7 demonstrations to listen for, 1 predict-pause, 1 worked example; Variation 11 (the Tune in four, as a waltz, in five, in seven, swung and with a hemiola); Lab 11 and the rhythm interactive (a rhythm slid against the metre's grid, with its syncopation index at every position); Monochord's rhythm engine (`monochord/rhythm.py`: metric weights, Longuet-Higgins and Lee's index, a pulse finder, polyrhythms, compositions into twos and threes, swing, click trains, the telephone game on rhythms; `tests/music/test_rhythm.py`), a kit of struck things (`instruments/drumkit.py`) and the pictures of rhythm (`explainer/music/rhythmviz.py`: dot grids, necklaces, tick rows, stick notation); every gate clean, narration listen-tested. The first cut ran 27.9 min; five passages were added (taps ahead of the click, off-beats that become beats, a rhythm against itself, rhythm into timbre, animals that keep a beat). |
| 2026-11-14 | **Part 12, *Scales and Modes***: 12 chapters, 31.5 min narrated of which 3.6 min listening in 16 windows; 5 pause-and-listen questions, 4 demonstrations to listen for, 1 predict-pause; Variation 12 (the Tune in the seven modes, brightest to darkest, then in pentatonic, whole-tone and octatonic scales); Lab 12 and the scale interactive (a stack of any generator, its notes round the octave and its sizes of step); Monochord's scales (`monochord/scales.py`: stacks and their gaps, moments of symmetry, modes and brightness, maximal evenness, interval vectors, deep scales, Myhill's property, transpositions, Burnside counts and the full classification of the 352 shapes, tetrachords, the 72 melakartas; `tests/music/test_scales.py`) and the pictures of scales (`explainer/music/scaleviz.py`: keyboards, octave circles, twelve-place clocks, step bars, chains of fifths, interval-vector bars); every gate clean, narration listen-tested. The first cut ran 26.7 minutes; six passages were added (the comma at twelve, the names of the degrees, relative and parallel minor, a random walk on each scale, the neutral third, Burnside on four beads). A claim in the draft, that the diatonic is the only deep seven-note scale, was false (seven consecutive semitones are deep too) and is corrected in the film and tested. |

**Still open from §6:** chords, slurs and a second voice on a staff in the series' engraver (needed from Parts 13
and 16), `tools/make.py` registration, the optional `music-qa` extra. **Not yet done for
Part 1:** the 1080p master (the narrated film has been built and gated at 480p), a human listening pass (every
sound so far has been judged by measurement and by spectrogram, none by ear), and the Chinese edition (Phase 6).

**Changes to the plan made by the pilot.**
- Levels are set by the loudest 400 ms, not by integrated loudness (§3), because plucked sounds are peaky.
- The narration alone passes a limiter (§3); the music still never does.
- The subtitles carry a line for every listening window (`[sound: lower, upper, both, physical model]`), written
  from the cue sheets, so the film can be followed with the sound off (§1, *See what you hear*).
- Parts 2 and 3 run 33 minutes, under the ~40 and ~50 first planned: fourteen and thirteen chapters of two to
  three minutes. The gate (30 to 60) is met; from Part 4 on, a part is drafted at 6,500 words or more.
- The narrator reads about 172 words a minute, not 140: a silent preview (which keeps time at 140) of Part 1 runs
  57 minutes, the narrated film 47. `tools/lecture_length.py` now estimates the series at the measured pace.

## 9. Decisions for the owner

*2026-11-13: the owner read the plan and said to proceed. Production therefore runs on the proposed defaults:
items 1, 2, 4, 6 and 7 as written; item 3 English first, Chinese in Phase 6; item 5 after the engraver pilot,
before Part 10. Any of them can still be changed; the Tune (item 1) is the only one that gets more expensive to
change with every part.*

1. **The Tune.** *Ah! vous dirai-je, maman* is proposed for the reasons in §2.2. The alternative is a theme
   written for the series. A familiar tune makes every transformation audible to everyone; an original one avoids
   the nursery association.
2. **The rights rule** (§2.4): own renderings of public-domain scores and original pastiche only, no third-party
   recordings as music, no performance of works in copyright. It limits Parts 28–30 and 38–40 to analysis,
   statistics and pastiche. Confirm, or name the exceptions to pursue with licences.
3. **Languages.** English and Chinese as planned, or English first.
4. **The number of parts.** Sixty-eight is the comprehensive plan. A fifty-part cut would merge 8–9, 23–24, 34–37
   into two, 51–52, 61–62, and 65–66, and fold 67 into 68.
5. **The engraver.** Part 10 was built with the series' own engraver (`explainer/music/staff.py`), which needs no
   new dependency, because installing Verovio's wheel was refused by the build session's permission policy. It
   draws one voice to a staff and will have to grow chords, slurs and second voices for Parts 13 to 22. The
   alternative is still open: approve one dependency (Verovio's wheel, or a system LilyPond) and the scenes keep
   working, since they use only the `Staff` interface.
6. **The compute exceptions** for Parts 64 and 66 (up to 6 h and 8 h on CPU, resumable), or smaller models with
   weaker results.
7. **Length.** The gate is 30–60 minutes including listening windows; Part 68 is planned at the ceiling.
