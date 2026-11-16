# Music, Built: Part 26, The Classical Style

Part 26 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fourth part of Act IV. Part 25 ended with Bach's death; this part follows the
half-century from the galant to Beethoven's middle years. It starts from Mozart's twelve variations on *Ah, vous
dirai-je, maman*, whose tune is the series' Tune, and follows a style of shared expectations through periodic phrasing,
sonata form traced by a key-finder, the string quartet as a conversation, the accompaniment as a motor, three careers, a
fair attribution test, and the instruments and machines that changed the music, ending with style as learned statistics.
The tools are Monochord's (`explainer/music/monochord/classical.py`, with Part 15's key tracker and Part 24's
stylometric test); the music is the thirty-three string-quartet movements by Haydn, Mozart and Beethoven in the music21
corpus (`baroque.load_quartets`). Mozart's K. 265 is not in the corpus, so the film describes it and measures the
quartets instead. Published findings are the ones listed under Sources.

* **Twelve variations on our Tune.** Mozart in Vienna; the Tune over plain Classical chords, heard; the plan.
* **1. A style of shared expectations.** From galant to Classical; C. P. E. Bach's sensitive style; the stock patterns
  (Gjerdingen's schemata); K. 265's twelve variations; Haydn's joke about endings (Op. 33 No. 2); a public for music.
* **2. Periodic phrasing.** An ear question (which four-bar phrase is finished?); the period and the sentence, ours,
  heard; 146 authentic cadences in the quartets, with peaks at 4 and 8 bars but exactly 4 or 8 a minority (Mozart 30,
  Haydn 11 in 100).
* **3. Sonata form on stage.** Haydn's Op. 74 No. 1 read eight bars at a time: C, G, a development through G minor, E♭,
  D minor and A minor, C again; the development, heard; a census: of the 20 movements whose first and last readings
  agree, 14 of 18 in major keys go first to the dominant and both minor-key ones to the relative major; an ear question
  (exposition or recapitulation?); where the form came from (the rounded binary); the Classical concerto; a drama of
  keys.
* **4. The string quartet: a conversation.** The genre; Mozart's 'Hunt' quartet, heard, with who leads bar by bar; the
  first violin leads 62 (Haydn), 59 (Mozart) and 55 (Beethoven) bars in 100; a minuet of Haydn's, heard; Op. 33's
  "new and special way".
* **5. The accompaniment.** The Tune over block chords, an Alberti bass and repeated chords, heard; accompaniment figures
  in about a quarter of the quartets' bars; storm and stress; the learned style returns.
* **6. Haydn, Mozart, Beethoven.** Three careers; their movements measured (Beethoven's three times as long, with nearly
  an octave more range); Haydn in London; a motive worked to exhaustion; Beethoven's Op. 59 No. 2 finale, an E minor
  movement that begins in C major, heard with the tracker undecided; an ear question (which is Beethoven?); *Figaro*'s
  Act II finale; Gluck's reform.
* **7. Who wrote this, fairly.** One genre, related works across several decades: Part 24's features score 42 in 100, eight Classical
  features 52, always guessing Mozart 45; the two best features plotted; 2000 shuffles of the names score 33 on average
  and as well as the real names about 5.4 times in 100; why it is hard.
* **8. The fortepiano and the metronome.** An instrument that can be soft and loud; a crescendo on Part 7's piano,
  heard; the Mannheim orchestra; Maelzel's metronome and Beethoven's marks; Viennese and English pianos; period
  instruments; Beethoven's puzzling marks.
* **9. Frontier: style as learned statistics.** Meyer's style as probabilities; beyond the canon (Bologne, Boccherini,
  Martines); ★ research problem: where in a movement do Haydn's and Mozart's styles differ most?
* **Variation 26, recap and problems.** The Tune as a Classical set: theme with Alberti bass, minore, adagio, finale; the
  ledger; what we found; five problems; where it comes back; in practice; Part 27.

## What is computed, and what is heard

`python -m videos.music.music26.compute` (a few minutes: the bowed strings) fills `.cache/music26/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook`, `figures`, `forms` | the Tune over plain chords and three accompaniments; a period and a sentence, ours | — |
| `phrases` | two four-bar phrases (an ear question); authentic cadences and the gaps between them in 33 movements | the cadence rule (tests) |
| `plan`, `develop` | Op. 74 No. 1's keys, eight bars at a time; its development; an exposition and recapitulation passage | the score's plan |
| `keys` | every movement's first new key; Op. 59 No. 2's finale, four bars at a time | the movements' keys |
| `texture`, `minuet` | who leads each bar; accompaniment figures; the 'Hunt' opening; Haydn's minuet | — |
| `three` | lengths and ranges by composer; Haydn's Op. 1 No. 1 and Beethoven's Op. 59 No. 1 (an ear question) | — |
| `style` | leave-one-out nearest-centroid attribution with two feature sets; a 2000-shuffle permutation null | Part 24's test |
| `dynamics` | a crescendo on Part 7's piano | — |
| `tune` | Variation 26 | — |

Monochord's tools are held in `tests/music/test_classical.py`; this part's claims and clips in
`tests/music/test_music26.py`.

**Sounds.** Quartets: Part 7's bowed string on its violin body, one model for all four instruments (physical model);
the Tune's examples and Variation 26: Part 7's piano (physical model). There are no recordings.

**What the models are, and are not.** *The key tracker* is Part 15's Krumhansl–Schmuckler profile over all four voices
in eight-bar windows; it misreads some openings (a slow introduction, a theme that begins off the tonic), which is why
the census counts only movements whose first and last readings agree. *The cadence detector* is strict: the bass falls
a fifth onto a downbeat and holds, and the top voice is on the bass note or its third, so it misses cadences with other
basses and counts some that a listener would not. *Who leads* is the voice with the most onsets in a bar. *The
attribution test* has thirty-three movements, so a few either way move its score; its permutation null shuffles the
composers' names among the movements. *The excerpts* are played from the encodings at a chosen tempo, all four
instruments on one bowed-string model; the piano is closer to a modern grand than to a Viennese fortepiano, as the film
says.

## Build

```bash
python -m videos.music.music26.compute                          # numbers and sounds (a few minutes)
EXPLAINER_TTS=silent python tools/build.py music26 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music26 --sync                         # the sound gates
python tools/dead_air.py renders/music26_480p.mp4 --sound music26  # no empty screen; no sound over a still one
python tools/lecture_length.py music26                          # 30 to 60 minutes, listening included
python tools/build.py music26                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 26                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** A movement has cadences at bars 4, 8, 16, 22, 30 and 38. Compute its phrase gaps and the share that
   are 4 or 8 bars.

   *Solution.* The gaps are 4, 8, 6, 8 and 8; four of the five (80 in 100) are 4 or 8 bars.

2. **Prove.** Show that a nearest-centroid classifier with two classes and one feature is a threshold at the midpoint of
   the class means.

   *Solution.* With means μ₁ < μ₂, a value x is assigned to class 1 when |x − μ₁| < |x − μ₂|. Squaring, x² − 2μ₁x + μ₁² <
   x² − 2μ₂x + μ₂², so 2(μ₂ − μ₁)x < μ₂² − μ₁², and since μ₂ − μ₁ > 0, x < (μ₁ + μ₂)/2. The rule is a threshold at the
   midpoint.

3. **Ear.** The lab plays eight phrases on the Tune, some ending on a half cadence, some on an authentic one. Sort them.

   *Solution.* The lab prints the answer key: a phrase is a half cadence when it ends on the dominant chord with the
   melody on G or B or D, and authentic when its bass falls from G to C with the melody on C.

4. **Build.** Add a feature to the attribution test that measures surprise under a model of chord pairs, and report the
   leave-one-out accuracy.

   *Where to look.* Turn each beat's sounding pitch classes (`Movement.sonority`) into a chord label, fit a smoothed
   bigram model on the training movements of each composer (Part 18's n-grams), and add each held-out movement's mean
   surprise under each model as two features; refit inside the leave-one-out loop, so that the held-out movement never
   trains its own model, and compare against the permutation null.

5. ★ **Beethoven's metronome.** Recompute the 2020 study of Beethoven's metronome marks from its published data, and
   test its central claim.

   *Where the frontier is.* Collect the marks and a sample of recorded tempos, model the recorded tempo as a function of
   the mark with a systematic offset (and a performer and era effect), and ask whether an offset of the size claimed
   explains the gap better than a proportional slowing or no offset at all; report the uncertainty, and what data would
   distinguish the explanations.

## Sources

* C. Rosen, *The Classical Style* (1971; expanded 1997); L. Ratner, *Classic Music* (1980); R. Taruskin, *The Oxford
  History of Western Music*, vol. 2 (2005).
* R. Gjerdingen, *Music in the Galant Style* (2007); W. Caplin, *Classical Form* (1998); J. Hepokoski and W. Darcy,
  *Elements of Sonata Theory* (2006); H. C. Koch, *Versuch einer Anleitung zur Composition* (1782–1793); A. B. Marx,
  *Die Lehre von der musikalischen Komposition*, vol. 3 (1845).
* C. P. E. Bach, *Versuch über die wahre Art das Clavier zu spielen* (1753, 1762); C. W. Gluck, preface to *Alceste*
  (1769); L. B. Meyer, *Style and Music* (1989).
* A. Martín-Castro and I. Ucar, "Conductors' tempo choices shed light over Beethoven's metronome", *PLOS ONE* (2020).
* M. S. Cuthbert and C. Ariza, "music21" (*ISMIR* 2010), whose corpus holds the quartet encodings.
* Part 7 for the bowed string and the piano; Part 15 for keys; Part 18 for n-grams; Part 21 for the period, the sentence
  and sonata theory; Part 22 for topics; Part 24 for the attribution test; Part 25 for the binary dance and the
  ritornello.

## Scope of the measurements

Cadence detection finds selected bass-fifth arrivals with upper tonic/third conditions, not every authentic cadence. Key-profile estimates can suggest tonal regions but do not independently identify themes, formal boundaries or a listener’s sense of home. Four- and eight-bar gaps are measured between detected events, not verified complete phrases.

Note-attack counts are a proxy for activity, with ties favoring earlier instruments, rather than thematic leadership. The accompaniment detector finds broad repeated/chordal figures, not specifically Alberti bass. Movement length in notated bars is not duration, and the uneven sample does not establish universal composer tendencies.

The attribution task holds genre more nearly fixed than Part 24, but date, edition, source and generation still differ. Leave-one-movement-out permits other movements of the same quartet in training; a genuinely independent test should hold out whole quartets and sources. The permutation test assumes exchangeable movements, which related movements undermine. Best single features are selected on this dataset. There is no measured human-listener baseline. Scaling uses the corrected training-fold-only routine from Part 24.

Periods can have weaker authentic antecedent closes as well as half cadences. Sonata and concerto descriptions are common templates with historical alternatives. Dynamics, measured tempo and independent chamber parts all have precedents; the fortepiano’s touch response and metronome’s adoption expanded existing possibilities.

With training-fold-only scaling, the Classical-feature classifier gets 17/33 (51.5%), the counterpoint features 14/33 (42.4%), and the majority baseline 15/33 (45.5%). The 2,000-shuffle tail is 109/2001 ≈ 0.0545; this is not below 0.05, even before addressing related-movement dependence.
