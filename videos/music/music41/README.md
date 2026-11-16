# Music, Built: Part 41, Orchestration

Part 41 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first part of Act VII, *The Craft*. Ravel called *Boléro* (1928) a piece for
orchestra without music: two alternating melodic strains, stated eighteen times over one snare-drum rhythm, with orchestration, density and dynamics driving most of the change. In one statement a horn, a celesta and two piccolos sit on the tune's harmonics and fuse into an
organ-like colour no single player owns: additive synthesis with players. This part builds an orchestra from the
series' own physical models and asks what an orchestrator controls: ranges and registers, loudness and brightness,
sections and the chorus effect, doubling and balance, spacing, texture, and the melody of timbres; then it turns
Ravel's idea around and lets a solver orchestrate a target spectrum. The tools are Monochord's
(`explainer/music/monochord/orchestra.py`). Every instrument heard is resynthesised from spectra measured on Parts 7–9's
models, or is one of those models itself. Published findings are the ones listed under Sources.

* **A piece for orchestra without music.** An ear question (a phrase on a horn, then again: one, two or four
  instruments?); Ravel's experiment; the plan.
* **1. An orchestra from physical models.** The orchestra's history in brief; sixteen harmonics measured on each model;
  one middle C on eight instruments, heard; an ear question (which of three Cs is the clarinet?); the Tune's phrase on
  each instrument, heard; the players; what the resynthesis leaves out.
* **2. Ranges, registers and transposition.** The ranges chart; registers; Part 8's clarinet model in its two registers
  (its strongest peak moving from 140 to 433 Hz), heard; transposing instruments; why they transpose.
* **3. Loudness and brightness.** An ear question (one trumpet note at one playback level, blown soft and hard: which was
  blown hard?); the centroid nearly doubling (357 to 651 Hz); why louder is brighter; a swell, heard; dynamic range
  across the orchestra; balance.
* **4. Sections and the chorus effect.** The arithmetic of n players (coherent 20 log n, incoherent 10 log n); one violin
  and eight, heard (+10.6 dB measured, between 9 and 18); solo and tutti, heard; the chorus effect; 1, 2, 4, 8 and 16
  violins at one level, heard; seating; section sizes.
* **5. Doubling, blend and balance.** A held C on flute, clarinet, both, and flute with a louder trumpet, heard;
  measured (the flute's share of the power falling from one half to one fifth); masking; doubling at the octave, heard;
  blend studies (Sandell; Lembke and McAdams).
* **6. Spacing.** The harmonic series as a guide; one C major chord three ways, heard; their roughness (1.33 close and
  low, 0.96 open, 0.19 close and high); registral layers; rules of spacing.
* **7. Textures and the melody of timbres.** The Tune's phrase in four textures, heard; the four textures; an
  orchestrator's order of work; a melody of timbres, heard; Schoenberg's *Klangfarbenmelodie* and Webern's *Ricercar*.
* **8. Ravel's harmonics.** The horn's series and where the celesta and piccolos sit; the combination assembled one
  instrument at a time, heard; the tempered notes' errors (0, −2.0 and +13.7 cents); the organ's mixture stops;
  *Boléro*'s plan; its crescendo in miniature, heard.
* **9. Orchestration as search.** The problem; the solver (non-negative least squares over 42 candidates, then every
  group of up to four); the target, a sung "ah" on C3; errors of 18.3, 10.7, 8.2 and 7.1 dB a band for one to four
  instruments; a bell as a harder target (31.5 dB with four), heard; the vowel and its matches, heard; IRCAM's tools.
* **10. Frontier: timbre measured.** Timbre space (Grey; McAdams and colleagues); our orchestra mapped by attack and
  brightness; timbre as identity; the treatises tested (the ACTOR project); machines; ★ research problem: can blend and
  layering be predicted from the score alone?
* **Variation 41, recap and problems.** The Tune in eight orchestrations (strings; woodwinds; brass; flute and clarinet
  in unison; Ravel's combination; a melody of timbres; tutti in octaves; matched to the vowel "ah"); the ledger; what we
  found; five problems; where it comes back; in practice; references; Part 42.

## What is computed, and what is heard

`python -m videos.music.music41.compute` (about a minute) fills `.cache/music41/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook`, `build`, `cresc` | Ravel's combination; its tempered errors; its fusion | the harmonic series (tests) |
| `same`, `which`, `tour` | one C on eight instruments; the clarinet quiz; the phrase on each | the measured spectra (tests) |
| `registers`, `bright`, `swell` | Part 8's clarinet in two registers; the trumpet soft and hard; a swell | spectral peaks and centroids (tests) |
| `section`, `sizes`, `solo` | one player against eight; 1 to 16 violins; solo and tutti | 10 log n and 20 log n (tests) |
| `blend`, `octave` | unison and octave doublings and their power shares | the centroids (tests) |
| `spacing` | three voicings and their roughness | Part 5's roughness (tests) |
| `texture`, `klang` | four textures; a melody of timbres | — |
| `match`, `bell`, `space` | the solver on a vowel and a bell; attack and brightness | errors shrinking with budget (tests) |
| `tune`, `variation` | Variation 41 | the ledger (tests) |

Monochord's tools are held in `tests/music/test_orchestra.py`; this part's claims and clips in `tests/music/test_music41.py`.

**Sounds.** The flute, clarinet, saxophone, trumpet and bowed string are Parts 7–8's physical models, measured once
(sixteen harmonics each) and resynthesised additively, with attacks and vibrato by family; the horn, piccolo and cello
are derived from those spectra; the celesta is a struck bar's inharmonic partials (Part 9); the voice is Part 17's model.
These clips are labelled `synthesized`. The soft and loud trumpet notes, the swell and the clarinet's registers are the
physical models themselves. There are no recordings.

**What the models are, and are not.** *One spectrum per instrument*: a real instrument's spectrum changes with pitch,
loudness and time, so ours sound alike from note to note (Part 52 builds better ones). *The horn, piccolo and cello* are
derived, not modelled. *The solver* matches an average spectrum in 32 bands, not how it moves in time.

## Build

```bash
python -m videos.music.music41.compute                          # numbers and sounds (about a minute)
EXPLAINER_TTS=silent python tools/build.py music41 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music41 --sync                         # the sound gates
python tools/dead_air.py renders/music41_480p.mp4 --sound music41  # no empty screen; no sound over a still one
python tools/lecture_length.py music41                          # 30 to 60 minutes, listening included
python tools/build.py music41                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 41                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** How many violins does it take to be 6 dB louder than four violins?

   *Solution.* Independent players add in power, so n players are 10 log₁₀ n dB above one. Six decibels more than four
   needs 10 log₁₀(n/4) = 6, n = 4 × 10^0.6 ≈ 16. Our measured sections give 12.7 dB for sixteen and 5.5 for four: 7.2 dB,
   close to the 6 predicted.

2. **Prove.** Prove that n incoherent equal sources are 10 log₁₀ n dB louder than one, and coherent ones 20 log₁₀ n.

   *Solution.* Coherent copies add in amplitude: the sum is n times the amplitude, n² times the power, 20 log₁₀ n dB.
   With independent random phases the cross terms average to zero, so the powers add: n times the power, 10 log₁₀ n dB.
   Eight violins: 18.1 and 9.0 dB; our section, with small detunings and onsets, measured 10.6.

3. **Ear.** The lab plays one held note on sections of different sizes; say how many players each time.

   *Solution.* The lab prints the sizes. The levels are matched, so listen for the chorus: one player has a clean, steady
   vibrato; three a slow beating; twelve a broad shimmer with no single pitch line.

4. **Build.** Give the solver a target of your own (another vowel, a bell) and compare budgets.

   *Where to look.* Set `FORMANTS` and `BUDGET` in `videos/music/labs/lab41.py`, or call `orchestra.match` with any list
   of (frequency, amplitude). Harmonic targets fall below 10 dB with two or three instruments; inharmonic ones do not,
   because every candidate is harmonic.

5. ★ **Can blend and layering be predicted from the score alone?**

   *Where the frontier is.* Collect orchestral excerpts with scores, recordings and listeners' judgements of what blends
   and what forms separate layers; predict them from the score and the instruments' spectra (harmonicity, onset
   synchrony, brightness); test on new excerpts and new listeners.

## Sources

* M. Ravel, *Boléro* (1928); H. Berlioz, *Grand traité d'instrumentation et d'orchestration modernes* (1844);
  N. Rimsky-Korsakov, *Principles of Orchestration* (1913); S. Adler, *The Study of Orchestration* (1982).
* J. M. Grey, "Multidimensional perceptual scaling of musical timbres", *JASA* (1977); S. McAdams, S. Winsberg,
  S. Donnadieu, G. De Soete and J. Krimphoff, "Perceptual scaling of synthesized musical timbres", *Psychological
  Research* (1995).
* G. J. Sandell, "Roles for spectral centroid and other factors in determining 'blended' instrument pairings in
  orchestration", *Music Perception* (1995); S.-A. Lembke and S. McAdams, "The role of spectral-envelope characteristics
  in perceptual blending of wind-instrument sounds", *Acta Acustica united with Acustica* (2015).
* A. Schoenberg, *Harmonielehre* (1911); A. Webern, orchestration of Bach's six-part *Ricercar* (1935).
* P. Esling, G. Carpentier and others on computer-aided orchestration (*Orchidée*, *Orchids*, *Orchidea*), IRCAM.
* W. A. Sethares, *Tuning, Timbre, Spectrum, Scale* (2nd ed., 2005), for the roughness model.

## Interpretation limits

Ranges and balance ratios are approximate guides, not universal limits. Incoherent power addition predicts about 3 dB per doubling under stated assumptions. The blend fraction and 20-cent harmonicity proxy are descriptive models, not measured listener fusion or masking probabilities. Boléro alternates two strains and changes dynamics and density as well as instrumentation. Tempered pitch errors refer to this model; players adjust intonation. The solver prunes candidates before subset search, fits linear band powers, and ranks fits by an RMS dB metric. It is not a global orchestration optimum or a perceptual quality test. Its restricted harmonic candidate list, rather than an inability of orchestras to play inharmonic collections, limits its bell match.
