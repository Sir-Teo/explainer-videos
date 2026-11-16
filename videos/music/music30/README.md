# Music, Built: Part 30, Sound Itself

Part 30 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the third part of Act V. Part 29 ordered pitch with rows, and total serialism ordered
everything else; this part follows the composers who stopped arranging notes and started arranging sound, chance and
process, from Schaeffer's closed groove in 1948 to the computer that sang in 1961 and the spectral composers of the
1970s. The tools are Monochord's (`explainer/music/monochord/soundmass.py`). The music of this era is in copyright, so
every sound in the film is the film's own, made from the series' instruments (SYLLABUS §2.4); the works are described.

* **A groove that closes.** Schaeffer in 1948; a closed groove of our own (Part 9's woodblock and drum over a low bowed
  string), heard; the plan.
* **1. Music from recordings.** Tape and its operations; the Tune at normal, double and half speed, heard; an ear question
  (a bell four ways: which is untouched?); the sound object and reduced listening; Lucier's room; Oram, Derbyshire,
  El-Dabh, Oliveros.
* **2. Chance and silence.** Cage, the prepared piano and the *I Ching*; *4'33''*; the Tune's notes by dice, heard;
  happenings and Fluxus; open works.
* **3. The electronic studio.** Cologne and sine waves; five mixtures on Studie II's scale (81 frequencies, 111.45 cents
  apart), heard; Tokyo, Copenhagen, the Barrons; Varèse and the Philips Pavilion; Columbia-Princeton.
* **4. Xenakis: clouds and sieves.** The engineer; a cloud of forty glissandi, heard; an ear question (random or even?);
  ten minutes of a cloud counted against Poisson's law; a cloud thickening from 1 to 24 notes a second, heard; UPIC;
  sieves (whole-tone, octatonic, the diatonic in seven terms, 5n ∪ 7n+2 with period 35, heard).
* **5. Sound masses.** Penderecki and Ligeti; eight bowed strings half a semitone apart, heard; their beats (about 8 a
  second); the same strings as an open chord, heard; notating a mass; Scelsi, Feldman, Young, Oliveros.
* **6. Process and phasing.** Reich; a twelve-note figure of ours phased against itself, heard; its twelve alignments
  (unisons 12, 0, 2, 6, ...; richest at 4, 5, 7, 8 notes ahead); *Different Trains*; minimalism; an additive figure,
  heard.
* **7. A spectrum, orchestrated.** Grisey's *Partiels*; an ear question (a brass tone from Part 8's lips, or its sixteen
  harmonics played by piano, bowed strings and voice?); the harmonics measured and assigned; the spectrum assembling,
  heard; harmonics against the piano's keys; Dufourt, Rădulescu, Haas; Murail, Saariaho, IRCAM.
* **8. The computer sings.** CSIRAC, Ferranti, Mathews's MUSIC; a unit-generator patch (oscillator, envelope, filter),
  heard; *Daisy Bell*; Carlos, Spiegel, Ciani, Radigue, Tomita; Chowning's FM; what changed.
* **9. Frontier: composing with machines, listening to data.** Computer-assisted composition; learned sound; sonification;
  ★ research problem: for which patterns in data does listening beat looking?
* **Variation 30, recap and problems.** The Tune's first phrase phased against itself; a cloud of thirty glissandi drawn to
  its first two phrases; the phrases on the harmonics of Part 1's low C string (its A 59 cents flat, its F 51 sharp); the
  ledger; what we found; five problems; where it comes back; in practice; Part 31.

## What is computed, and what is heard

`python -m videos.music.music30.compute` (about a minute) fills `.cache/music30/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook`, `tape`, `speeds` | a looped fragment; a bell untouched, reversed, halved and cut; the Tune re-speeded; attack times | the tape law (tests) |
| `chance`, `studie` | the Tune's notes by dice; sine mixtures on the 5^(1/25) scale | — |
| `clouds`, `density`, `gliss` | Poisson and even clouds; ten minutes of counts against Poisson's law; a rising rate; glissandi | Poisson's law |
| `sieves`, `mass`, `spread` | sieve scales and periods; a cluster's beat rates; the open chord | the Chinese remainder theorem |
| `phasing`, `additive` | a figure's twelve alignments and the drifting loops; an additive figure | symmetry (tests) |
| `spectral`, `buildup` | a brass tone's harmonic levels, orchestrated; the spectrum assembling | — |
| `unitgen` | a sawtooth oscillator, envelope and falling low-pass filter | — |
| `tune` | Variation 30 | — |

Monochord's tools are held in `tests/music/test_soundmass.py`; this part's claims and clips in
`tests/music/test_music30.py`.

**Sounds.** Part 1's string; Part 7's piano and bowed string; Part 8's lips on a long bore; Part 9's bells, woodblock and
drums (physical models). The glissandi, sine mixtures, unit-generator patch and synthetic voice are synthesized. There
are no recordings.

**What the models are, and are not.** *The brass tone* is Part 8's lips on a trumpet-shaped bore stretched to a
trombone's length, not a measured trombone; its spectrum is the model's. *The ensemble's* harmonics are played at their
exact frequencies by instruments whose own timbres add partials of their own, which is part of why the result does not
quite fuse. *The clouds* are random with stated rates; Xenakis's own clouds were computed cell by cell with his own
parameters. *The phasing figure* is ours; Reich's patterns are his. *The cluster's beats* are between neighbours only;
all pairs beat.

## Build

```bash
python -m videos.music.music30.compute                          # numbers and sounds (about a minute)
EXPLAINER_TTS=silent python tools/build.py music30 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music30 --sync                         # the sound gates
python tools/dead_air.py renders/music30_480p.mp4 --sound music30  # no empty screen; no sound over a still one
python tools/lecture_length.py music30                          # 30 to 60 minutes, listening included
python tools/build.py music30                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 30                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** A tape is played at 1.5 times its speed. By how many cents does every pitch rise, and how long does a
   3-second sound last?

   *Solution.* 1200 log₂ 1.5 ≈ 702 cents, a perfect fifth (just); the sound lasts 3 / 1.5 = 2 seconds.

2. **Prove.** Show that for a Poisson process of rate λ the gaps between events have mean and standard deviation 1/λ.

   *Solution.* The gaps are exponential with density λe^(−λt). The mean is ∫ t λe^(−λt) dt = 1/λ; the second moment is
   ∫ t² λe^(−λt) dt = 2/λ², so the variance is 2/λ² − 1/λ² = 1/λ² and the standard deviation 1/λ.

3. **Ear.** The lab plays six clouds; some at Poisson times, some evenly spaced. Sort them.

   *Solution.* The lab prints the order. Even clouds are heard as a pulse within a second or two; Poisson clouds clump and
   pause.

4. **Build.** Write the phasing engine for any figure, and find the figures whose alignments are distinct after identifying k with 12 − k.

   *Where to look.* `soundmass.phase_patterns` gives the pairs at each shift; describe each alignment by its multiset of
   pairs up to the symmetry k ↔ 12 − k, and search figures (for instance, all sequences over a small pitch set) for
   those whose seven alignment classes are pairwise different. With unordered simultaneous pairs, opposite shifts necessarily match, so twelve distinct textures are impossible under this descriptor.

5. ★ **For which patterns in data does listening beat looking?**

   *Where the frontier is.* Generate series with planted patterns (a weak periodicity, a change of rate, a rare burst, a
   slow phase drift), present them as plots, as sound and as both, measure detection rate and time against chance, and
   model which properties of a pattern predict an advantage for the ear; report effects with intervals.

## Sources

* I. Xenakis, *Formalized Music* (1963; rev. 1992); S. Reich, *Writings on Music, 1965–2000* (2002); J. Fineberg (ed.),
  "Spectral music: history and techniques", *Contemporary Music Review* (2000); A. Ross, *The Rest Is Noise* (2007).
* P. Schaeffer, *Traité des objets musicaux* (1966); J. Cage, *Silence* (1961); K. Stockhausen, *Studie II* score
  (1956), for the scale.
* M. V. Mathews, "The digital computer as a musical instrument", *Science* (1963); J. L. Kelly and C. C. Lochbaum,
  "Speech synthesis" (1962); J. M. Chowning, "The synthesis of complex audio spectra by means of frequency modulation",
  *JAES* (1973).
* T. Hermann, A. Hunt and J. G. Neuhoff (eds.), *The Sonification Handbook* (2011).
* Part 1 for the string; Part 2 for tape speed; Part 3 for Fourier; Part 5 for beats; Parts 7–9 for the instruments.

## Interpretation limits

Eight-hertz beating can sound like flutter or pulses; roughness depends on spectral spacing, level and auditory filtering. Wider-spaced fundamentals can still have interacting partials. Poisson clouds assume a steady rate and independent events; they illustrate one model, not every Xenakis process. Phase-pair diversity is a combinatorial descriptor, not a listener rating. Historical studio controls specify parameters within a finite machine, and the 1961 Daisy example is attributed to a Bell Labs computer without an uncertain model number.
