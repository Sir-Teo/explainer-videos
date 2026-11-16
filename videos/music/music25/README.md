# Music, Built: Part 25, The Baroque

Part 25 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the third part of Act IV. Part 24 ended with Monteverdi's second practice; this part
follows the century and a half from 1600 to Bach's death. It starts from Vincenzo Galilei's weights on strings and the
Florentine argument for a new kind of song, and follows monody into opera, the figured bass into Corelli's trio sonata,
ornament and affect, the suite, the concerto's ritornello, temperament and the colour of keys, the passage from eight
modes to two keys, and three careers, ending with what the scores do not tell us about pitch and tempo. The tools are
Monochord's (`explainer/music/monochord/baroque.py`, with Part 10's figured-bass realizer and Part 6's temperaments); the
pieces are the Grave of Corelli's Op. 3 No. 1 and the opening of Handel's *Lascia ch'io pianga*, from the music21 corpus's
encodings, with Part 24's Palestrina and Part 17's Bach for the census of modes and keys. Published findings are the ones
listed under Sources.

* **Weights on strings.** Galilei's test of the Pythagorean legend; an ear question (weights 2:1 or 4:1: which is an
  octave?); Mersenne's law; the plan.
* **1. A new kind of song.** The Camerata; monody; a recitative and an aria, ours, heard; the singer's graces; a top and a
  bottom.
* **2. Opera.** Peri's *Euridice*; Monteverdi's *Orfeo*; a lament over a falling ground, ours, heard; Venice's public
  opera and the da capo aria.
* **3. The figured bass.** Figures and the trio sonata; Corelli's first two bars realized three ways; an ear question
  (Corelli's violins or the realizer's chords?); the realizer's chords hold 80 in 100 of Corelli's notes but its top
  voice is the first violin's only 28 times in 100; the Neapolitan partimento.
* **4. Affect and ornament.** The doctrine of the affections; a line plain and ornamented, straight and *inégale*,
  heard; French and Italian taste; tables of ornaments.
* **5. The suite.** Four dances; the Tune's first phrase in four dance rhythms, heard; the binary plan.
* **6. Ritornello and concerto.** Corelli and Vivaldi; a concerto movement in ritornello form, ours, heard; a finder that
  matches intervals catches the returns in C, G and C and misses the head in A minor; *The Four Seasons*.
* **7. Temperament and the colour of keys.** Major thirds of every key in meantone, Werckmeister III and equal
  temperament; the wolf, heard; an ear question (a cadence in C or F♯ in Werckmeister III: which is rougher?); Zhu Zaiyu
  and Stevin; Mattheson's key characters; *The Well-Tempered Clavier*.
* **8. From modes to keys.** Palestrina's movements by mode (Ionian and Aeolian 35 in 100) against Bach's chorales (185
  major, 178 minor); Heinichen's circle; Rameau's *Traité*; the fundamental bass under a Bach chorale, heard.
* **9. Bach, Handel, Rameau.** Three careers; *Lascia ch'io pianga*, heard; Telemann, Scarlatti, Purcell, Jacquet de La
  Guerre.
* **10. Frontier: what pitch, what tempo?** Pitch standards from 392 to 465 Hz, heard; the instruments; tempo from the
  pulse and the dance; ★ research problem: the sarabande's tempo, with its uncertainty.
* **Variation 25, recap and problems.** The Tune as a French overture and as a chaconne on a four-bar ground with an
  ornamented reprise (26 ornament notes added to 14); the ledger; what we found; five problems; where it comes back; in
  practice; references; Part 26.

## What is computed, and what is heard

`python -m videos.music.music25.compute` (under a minute) fills `.cache/music25/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook` | two equal strings under weights 2:1 and 4:1; Mersenne's law | the law (tests) |
| `monody`, `lament` | a recitative, an aria and a lament, ours | — |
| `corelli`, `realize3` | Corelli's Grave as written; its bass figured from the violins and realized; three realizations | Corelli's notes |
| `ornaments`, `dances` | ornaments and inequality; the Tune in four dance rhythms | — |
| `ritornello` | a concerto movement, ours, and the returns the finder finds | the movement's plan |
| `keys`, `wolf` | thirds and fifths of every key in three temperaments; the wolf; a cadence in two keys | Part 6's temperaments |
| `modes`, `fundamental` | mode labels in Palestrina against Bach; a chorale phrase's fundamental bass | — |
| `handel`, `pitch` | *Lascia ch'io pianga*'s opening; one chord at four standards of pitch | — |
| `tune` | Variation 25 | — |

Monochord's tools are held in `tests/music/test_baroque.py`; this part's claims and clips in
`tests/music/test_music25.py`.

**Sounds.** Harpsichord: Part 1's string plucked near its end, on Part 7's soundboard; violins: Part 7's bowed string on
its violin body (physical models); organ tones (additive) and Part 17's choir (synthesized). There are no recordings.

**What the models are, and are not.** *Corelli's figures* are worked out from what the violins sound at each bass
onset, by semitone intervals, so they miss Corelli's chromatic inflections and passing figures; the realizer works in F
major's signature and chooses the smoothest three-voice realization. *The ritornello finder* compares melodic
intervals with one mismatch allowed; the film's concerto is ours, built so that one return changes mode. *Key colours*
are the tuning's arithmetic; key character in the period also came from instruments and convention, as the film says.
*Mode labels* are the Humdrum encoders' for Palestrina and the music21 encoders' for Bach. *The excerpts* are sung or
played from the encodings at a chosen tempo; the Handel encoding is a voice and piano reduction. *The pitch standards*
are representative values from Haynes's survey, not single documented instruments.

## Build

```bash
python -m videos.music.music25.compute                          # numbers and sounds (under a minute)
EXPLAINER_TTS=silent python tools/build.py music25 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music25 --sync                         # the sound gates
python tools/dead_air.py renders/music25_480p.mp4 --sound music25  # no empty screen; no sound over a still one
python tools/lecture_length.py music25                          # 30 to 60 minutes, listening included
python tools/build.py music25                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 25                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** A string sounds 196 Hz under 4 kg. What weight makes it sound 294 Hz, a fifth higher? And what did the
   legend predict?

   *Solution.* f ∝ √T, so T = 4 × (294/196)² = 4 × 2.25 = 9 kg. The legend, weights in proportion to the ratio, predicted
   4 × 3/2 = 6 kg, which gives 196 × √1.5 = 240 Hz, about 351 cents: between a minor and a major third.

2. **Prove.** Show that a quarter-comma meantone fifth is 1200 log₂(5)/4 ≈ 696.6 cents, and that four of them, less two
   octaves, make a pure third.

   *Solution.* The syntonic comma is 81/80. A pure fifth narrowed by a quarter of it is (3/2)(80/81)^(1/4) =
   (3⁴/2⁴ · 80/81)^(1/4) = (80/16)^(1/4) = 5^(1/4), which is 1200 log₂ 5 / 4 = 696.58 cents. Four of them make 5, and two
   octaves down, 5/4: the pure major third.

3. **Ear.** The lab plays a cadence in each of the twelve keys in Werckmeister III, shuffled. Rank them from smoothest to
   roughest.

   *Solution.* The lab prints each key's major third error: C and F are smoothest (3.9 cents wide), then G, D and B♭
   (9.8), then E♭, E, A and B (15.6), and C♯, F♯ and G♯ roughest (21.5, the Pythagorean third).

4. **Build.** Extend the ritornello finder so that it allows for mode, and test it on the film's concerto.

   *Where to look.* `baroque.ritornello_returns` compares intervals exactly with one mismatch. Compare instead the
   scale-step intervals (map each pitch to its degree in the current key, found with Part 15's key finder), or allow a
   semitone difference on intervals of a third; the A minor head should then be found without false returns in the
   episodes.

5. ★ **The sarabande's tempo.** Estimate the tempo range of the sarabande from treatises and documented timings, with its
   uncertainty.

   *Where the frontier is.* Collect statements of tempo for the dance (Quantz's pulse rule, dance treatises' step
   counts, any recorded durations of balls or operas), express each as a range in beats per minute with its own
   uncertainty, and combine them in a model that allows the tempo to differ by country and decade; report an interval,
   not a number.

## Sources

* M. Bukofzer, *Music in the Baroque Era* (1947); R. Taruskin, *The Oxford History of Western Music*, vol. 2 (2005);
  R. Donington, *The Interpretation of Early Music* (1963).
* V. Galilei, *Dialogo della musica antica et della moderna* (1581) and *Discorso* (1589); M. Mersenne, *Harmonie
  universelle* (1636); G. Caccini, *Le nuove musiche* (1602).
* J. Mattheson, *Das neu-eröffnete Orchestre* (1713) and *Der vollkommene Capellmeister* (1739); J.-P. Rameau, *Traité de
  l'harmonie* (1722); J. D. Heinichen, *Neu erfundene und gründliche Anweisung* (1711); J. J. Quantz, *Versuch einer
  Anweisung die Flöte traversiere zu spielen* (1752).
* B. Haynes, *A History of Performing Pitch: The Story of "A"* (2002); R. Gjerdingen, *Music in the Galant Style* (2007),
  for the partimento.
* M. S. Cuthbert and C. Ariza, "music21" (*ISMIR* 2010), whose corpus holds the Corelli and Handel encodings.
* Part 6 for temperaments; Part 10 for figures and the realizer; Part 15 for keys; Part 17 for the chorales and the choir;
  Part 18 for the rule of the octave; Part 21 for binary form; Part 24 for Palestrina's modes.

## Interpretation and model scope

The pitch demonstration spans 392–465 Hz, about 296 cents: approximately a minor third, not a fourth. A=415 is a modern convention near some historical levels, rather than the single Baroque standard. Instrument construction, string tension and response varied.

Corelli’s figures are inferred from the violin parts later compared with the realization. Pitch-class inclusion therefore measures reconstruction with supplied harmonic information, not independent prediction from an unfigured bass. The voicing realizer enforces selected constraints and does not recreate Corelli’s complete counterpoint.

Werckmeister III has repeated third sizes; not every key has a unique third. Equal temperament preserves transposed interval ratios, not instrument/register identity. Modern modal and key tags are editorial metadata, not a direct census of historical conceptual categories. Changes toward major-minor practice had multiple causes.

One affect per movement, fixed ornament lengths, national styles and continuo prevalence are teaching generalizations with contextual exceptions. Bach’s reception predates 1829, and Handel developed English oratorio from earlier practices. Galilei’s experiment refutes the proposed weight ratio for an ideal string; it does not remove mathematical relationships from acoustics.
