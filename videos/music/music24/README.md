# Music, Built: Part 24, The Renaissance

Part 24 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second part of Act IV. Part 23 followed Western music from one line to the
fourteenth century; this part covers the fifteenth and sixteenth. It measures how thirds and sixths became the sound of
the music, how imitation became its structure, and how strictly Palestrina followed the rules later written from his
music; it follows printing and Josquin's name to a statistical test of authorship; and it counts Monteverdi's second
practice where Artusi said it was. The measures are Monochord's (`explainer/music/monochord/palestrina.py`); the
pieces are 1,318 Mass movements by Palestrina (101 Masses, Humdrum encodings) and 48 madrigals by Monteverdi
(Books 3 to 5), from the music21 corpus (`explainer/music/monochord/renaissance.py`), with Part 23's 89
fourteenth-century pieces for comparison; everything heard is sung by Part 17's synthetic choir. Published findings are
the ones listed under Sources.

* **Who wrote this?** Forster's remark of 1540 about Josquin; the opening of the Kyrie of the *Missa Papae Marcelli*,
  sung from the encoding; the plan.
* **1. Thirds and sixths become consonant.** The *contenance angloise*; fauxbourdon on the Tune, heard; sonorities with
  a third, 51 in 100 in the fourteenth century against 84 in Palestrina; full triads 24 against 63; last chords with a
  third 1 in 89 pieces against 90 in 100 movements; two endings heard.
* **2. Imitation as structure.** Points of imitation; one found by a program and heard; 70 in 100 of Palestrina's
  movements open imitatively, 1,669 of 2,062 later entries exact, at the octave, fourth or fifth; Monteverdi 46 in
  100.
* **3. The Mass, three ways.** Cantus firmus, paraphrase and imitation Masses; the corpus; Trent and the legend of the
  *Missa Papae Marcelli*.
* **4. Palestrina's style as rules.** Passing, neighbour, suspension and cambiata, heard; all 102,279 dissonances
  against the bass classified: passing 55 in 100, suspension 31, neighbour 10, free 2.6; an ear question (a seventh
  prepared or struck?).
* **5. The line.** Jeppesen's melodic rules; one voice of Palestrina heard alone; forbidden intervals 0.9 per thousand
  moves in Palestrina, 5 in the fourteenth century, 13 in Monteverdi; leaps turned back by step 38 against 23 in 100.
* **6. Printing, and Josquin's name.** Petrucci's *Odhecaton* (1501); Josquin; Glarean and the first classics; the
  two kinds of evidence.
* **7. Who wrote this? A statistical answer.** Twelve features and a nearest-centroid test with leave-one-out; the
  picture in two dimensions; Palestrina against Monteverdi, 95 in 100, and why that is the wrong question; Monteverdi's
  Book 3 against Books 4–5, 73 in 100 (free dissonance alone 67); an ear question (which is Palestrina?).
* **8. The madrigal and word painting.** The madrigal from Arcadelt to Monteverdi; the opening of Book 3's first
  madrigal, heard; madrigalisms; Morley's rule.
* **9. The second practice.** Artusi's attack (1600); *Cruda Amarilli*, heard, its free dissonances marked; free
  dissonance 2.6 in 100 in Palestrina, 23 in Book 3, 45 in Book 4, 49 in Book 5; the reply of 1605 and 1607.
* **10. Zarlino's triad, Vicentino's thirty-one tones.** The *senario*; an ear question (one chord in Pythagorean, just
  and 31-tone tuning); quarter-comma meantone; Vicentino's archicembalo and the debate with Lusitano.
* **11. Chromaticism and ficta.** Glarean's twelve modes; Gesualdo; seven chords by thirds and semitones, ours, heard;
  the accidentals no one wrote.
* **12. Frontier: attribution and ficta by machine.** The Josquin Research Project; how attribution tests fail;
  ★ research problem: an attribution test held out by source.
* **Variation 24, recap and problems.** The Tune as a four-voice point of imitation (entries four beats apart, then
  free counterpoint by Part 20's search; 12 of 12 beats consonant after the last entry); the ledger; what we found;
  five problems; where it comes back; in practice; references; Part 25.

## What is computed, and what is heard

`python -m videos.music.music24.compute` (a minute or two) fills `.cache/music24/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook` | the opening of the Kyrie of the *Missa Papae Marcelli*, sung from the encoding | — |
| `thirds`, `fauxbourdon` | sonorities with a third, triads, final chords, three repertories; two endings heard; fauxbourdon on the Tune | Part 23's census |
| `imitation` | opening points of imitation in every movement; one heard | hand-built cases (tests) |
| `masses` | the corpus by Mass and number of voices | — |
| `dissonance`, `kinds` | every dissonance against the bass classified; the treatments heard; the ear question | hand-built cases (tests) |
| `melody`, `line` | leaps, recovery, forbidden intervals; one line heard | — |
| `style`, `quiz` | twelve features per piece; nearest-centroid leave-one-out; the ear question | — |
| `madrigal`, `cruda` | Monteverdi's openings, *Cruda Amarilli*'s free dissonances marked | — |
| `tuning`, `chromatic` | one triad in three tunings; a chromatic progression, ours | Part 6's cents |
| `tune` | Variation 24 | consonance after the last entry |

Monochord's tools are held in `tests/music/test_palestrina.py`; this part's claims and clips in
`tests/music/test_music24.py`.

**Sounds.** Part 17's choir (Part 8's source-filter voice), labelled `synthesized`, singing on vowels. There are no
recordings.

**What the models are, and are not.** *The corpus* is one composer's Masses against another's madrigals, from two
encodings, with editorial accidentals included and Monteverdi's continuo parts where the encoding has them; it is not a
sample of the century. *The dissonance classifier* compares every voice with the lowest sounding voice at every onset
and knows passing notes, neighbours, suspensions (prepared, held over a moving bass, falling by step), cambiatas and
anticipations; everything else is "free", including figures it was not told about and slips in the encodings.
*Imitation* is judged on the first four melodic intervals of each voice. *The stylometric test* is nearest-centroid on
twelve standardized features with leave-one-out; its first comparison confounds composer with genre, encoding and date,
as chapter 7 says, and its second has only 48 pieces. *The pieces "ours"* (fauxbourdon on the Tune, the chromatic
progression, the dissonance demonstrations, Variation 24) are computed for the film. *The excerpts* are sung by
synthetic voices on vowels from the encodings' pitches and lengths, at a chosen tempo.

## Build

```bash
python -m videos.music.music24.compute                          # numbers and sounds (a minute or two)
EXPLAINER_TTS=silent python tools/build.py music24 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music24 --sync                         # the sound gates
python tools/dead_air.py renders/music24_480p.mp4 --sound music24  # no empty screen; no sound over a still one
python tools/lecture_length.py music24                          # 30 to 60 minutes, listening included
python tools/build.py music24                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 24                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** Zarlino's triad is 4:5:6. Compute its third and fifth in cents, and the error of each in 12 and in 31
   equal steps.

   *Solution.* 1200 log₂(5/4) = 386.31 cents and 1200 log₂(3/2) = 701.96. In 12 steps: 400 and 700, errors +13.69 and
   −1.96. In 31 steps the nearest are 10 steps, 387.10 (+0.78), and 18 steps, 696.77 (−5.18): the thirds of 31 are
   nearly pure and its fifths are those of quarter-comma meantone (`palestrina.triad_cents`).

2. **Prove.** Prove that two voices entering at the octave or the fifth keep the half steps of a mode in corresponding
   places, and that at the second they do not.

   *Solution.* The white-note scale's half steps are E–F and B–C. A transposition by an octave maps every note to the
   same letter, so the pattern of tones (T) and semitones (S) is unchanged. A fifth up maps C D E F G (T T S T) to
   G A B C D (T T S T), and D E F G A (T S T T) to A B C D E (T S T T): within the scale, a motive and its image a
   fifth higher have the same pattern unless the motive contains B, whose fifth, F, makes a tritone the singers
   corrected (F♯ or B♭), which is why answers are sometimes adjusted. A second up maps C D E F G (T T S T) to
   D E F G A (T S T T): the semitone moves, and the imitation is no longer exact.

3. **Ear.** The lab plays ten cadences, some with prepared and some with struck dissonances. Sort them.

   *Solution.* The lab prints the answers. A prepared seventh is heard first as a consonance that the bass then moves
   under; a struck one arrives at the moment of the clash.

4. **Build.** Add three features to the stylometric test, and measure whether the accuracy on Monteverdi's books
   improves under leave-one-out.

   *Where to look.* `palestrina.features` returns twelve numbers; candidates are the share of sonorities without a
   third, the rate of cadences (Part 23's `medieval.cadences`), and the share of notes on syllables of new words (not
   in this encoding). With 48 pieces, report the accuracy with its spread over resamples; a gain of a few points is
   within noise.

5. ★ **Attribution held out by source.** Design an attribution test held out by source, and say what result would
   show it is recognizing scribes, not composers.

   *Where the frontier is.* Group the pieces by the manuscript or print they come from; train on some sources and test
   on others, for two composers whose works survive in the same sources. If accuracy within sources is high and across
   sources falls toward chance, the features are measuring the source. The Josquin Research Project's tags of
   attribution security are the place to start.

## Sources

* A. W. Atlas, *Renaissance Music* (1998); R. Taruskin, *The Oxford History of Western Music*, vol. 1 (2005).
* K. Jeppesen, *The Style of Palestrina and the Dissonance* (1927); *Counterpoint* (1931); J. J. Fux, *Gradus ad
  Parnassum* (1725).
* G. Zarlino, *Le istitutioni harmoniche* (1558); N. Vicentino, *L'antica musica ridotta alla moderna prattica* (1555);
  H. Glarean, *Dodecachordon* (1547); T. Morley, *A Plaine and Easie Introduction to Practicall Musicke* (1597).
* G. M. Artusi, *L'Artusi, overo delle imperfettioni della moderna musica* (1600); C. Monteverdi, preface to the fifth
  book of madrigals (1605); G. C. Monteverdi, *Dichiaratione* (1607); C. V. Palisca, "The Artusi–Monteverdi
  controversy", in *The Monteverdi Companion* (1968).
* The Josquin Research Project, J. Rodin, C. S. Sapp and others (Stanford); M. S. Cuthbert and C. Ariza, "music21"
  (*ISMIR* 2010), whose corpus holds the encodings.
* Part 6 for tuning and meantone; Part 14 for gap fill; Part 16 for species counterpoint; Part 17 for the choir; Part 20
  for the counterpoint search; Part 23 for the fourteenth-century corpus and *musica ficta*.
