# Music, Built: Part 28, New Scales, New Rhythms

Part 28 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first part of Act V. Part 27 ended with a jump in chromaticism after 1900; this
part follows the composers who loosened the key with other scales and other rhythms, from the gamelan Debussy heard in
1889 to Messiaen. It enumerates every scale with limited transposition, hears planing, the octatonic, displaced accents,
additive rhythm and two keys at once, and tests two famous analytical claims, the golden section in Bartók and the
octatonic in Stravinsky, against what chance would give. The tools are Monochord's
(`explainer/music/monochord/modern.py`). Most of the period's music is still in copyright, so every example in the film
is an original sketch built on the Tune or on a stated rule (SYLLABUS §2.4); the works themselves are described.

* **A gamelan in Paris.** The 1889 Exposition; a gamelan texture of our own in an idealized slendro (Part 9's bars and
  gongs), heard; the plan.
* **1. A scale without a home.** The whole-tone clock (2 transpositions, no half steps); an ear question (the Tune in C
  major and in whole tones: which has no half steps?); Scriabin's mystic chord; Debussy's *Voiles*; the pentatonic; the
  same melody on five equal steps and on the black keys, heard (they differ by up to 80 cents); Busoni, Hába, Carrillo.
* **2. Every symmetric scale.** 4,096 sets, 352 shapes up to transposition; the 15 with limited transposition, of which
  the seven largest are Messiaen's modes; modes 1 to 3 heard; the hexatonic and Cohn's hexatonic poles; the proof that
  every symmetric set repeats a pattern every 1, 2, 3, 4 or 6 semitones; Messiaen's *Technique*.
* **3. Chords that slide.** Planing; an ear question (planed major triads or functional chords?); planing in jazz and
  film; *La cathédrale engloutie*.
* **4. The octatonic.** The scale and its four major triads, heard; C and F♯ major together, broken, and an octatonic
  ostinato, heard; Rimsky-Korsakov, Stravinsky, the Petrushka chord.
* **5. Rhythm set loose.** *The Rite of Spring*; an ear question (accents on every fourth pulse or at random: where is
  the downbeat?); why the ear gives up; changing metres; ostinatos of 3, 4 and 5 pulses layered, realigning after 60,
  heard.
* **6. Bartók: fieldwork, symmetry, proportion.** Bartók and Kodály's collecting; additive rhythms of 5, 7, 8 and 9
  pulses, heard, and counted (the Padovan numbers); Lendvai's axis system; Lendvai's golden-section claim and Howat's
  critique; the null model (88 bars, one fixed landmark within a bar: 4.5 in 100; five: 21; ten within two bars: 61).
* **7. Two keys at once.** Bitonality; Ives; the Tune in C over F♯ major, heard; the key-finder fits the tune (C major,
  0.96) and the chords (F♯ major, 0.83) but finds no single key for both (best B♭ minor, 0.74); Paris between the wars.
* **8. Messiaen: modes and palindromes.** The *Quartet for the End of Time*; a non-retrogradable rhythm with mode 2
  chords, heard; palindromes counted (193 of 20,569 rhythms of sixteen sixteenths); an added value, heard; more
  techniques.
* **9. 1913, and after.** Not impressionism; the first night of the *Rite*; how much of the riot is legend; after the
  *Rite*; Lili and Nadia Boulanger, Tailleferre, Crawford Seeger.
* **10. Frontier: is it octatonic?** Van den Toorn, Taruskin and Tymoczko; the exact chance that a k-note passage fits
  a scale (four notes: octatonic 42, diatonic 49 in 100; seven: 3 and 1.5); Forte's set classes (224 up to inversion);
  ★ research problem: how much of a repertoire is octatonic beyond chance, and where?
* **Variation 28, recap and problems.** The Tune on the whole-tone scale with augmented triads planed under every note,
  then on the octatonic scale over an ostinato whose accents chance placed; the ledger; what we found; five problems;
  where it comes back; in practice; Part 29.

## What is computed, and what is heard

`python -m videos.music.music28.compute` (about a minute) fills `.cache/music28/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook`, `slendro` | a gamelan texture of our own; its core melody on equal steps and on the black keys | — |
| `wholetone`, `modes`, `census` | the Tune moved degree for degree; Messiaen's modes 1–3; every set's period and shape | the theorem (tests) |
| `planing`, `octatonic`, `triads` | planed and functional harmony; the scale, its triads, the Petrushka chord, an ostinato; chance fits | exact enumeration |
| `accents`, `blocks`, `bartok` | regular and random accents; layered ostinatos; additive rhythms and their counts; the golden-section null | the recurrence (tests) |
| `polychord`, `messiaen`, `added` | the Tune over F♯ with key fits; a palindrome with mode 2 chords and palindrome counts; added values | Part 15's profiles |
| `tune` | Variation 28 | — |

Monochord's tools are held in `tests/music/test_modern.py`; this part's claims and clips in
`tests/music/test_music28.py`.

**Sounds.** Part 7's piano and bowed string; Part 9's bars, gongs, drums and woodblock (physical models). There are no
recordings, and no copyrighted music is played.

**What the models are, and are not.** *The gamelan* is a sketch in an idealized slendro of five equal steps; real
Javanese tunings vary from set to set and are not equal, and real gamelan pieces are organized far more richly. *The
octatonic and diatonic chance fits* count pitch-class sets, not passages: a real passage's notes are not chosen at
random, which is why the research problem calls for a null built from music. *The golden-section null* places landmarks
uniformly at random; real climaxes cluster in the second half of a piece, which makes chance hits more likely, not less.
*The accents* of the *Rite*-like example are placed by a random generator, not taken from the score. *The bitonal key
fits* weight every note by its duration.

## Build

```bash
python -m videos.music.music28.compute                          # numbers and sounds (about a minute)
EXPLAINER_TTS=silent python tools/build.py music28 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music28 --sync                         # the sound gates
python tools/dead_air.py renders/music28_480p.mp4 --sound music28  # no empty screen; no sound over a still one
python tools/lecture_length.py music28                          # 30 to 60 minutes, listening included
python tools/build.py music28                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 28                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** How many different transpositions does the set {0, 1, 4, 5, 8, 9} have? Name the pattern it repeats.

   *Solution.* Transposing by 4 maps it onto itself (0→4, 1→5, 4→8, 5→9, 8→0, 9→1), and no smaller step does, so it
   has 4 different transpositions. It repeats the pattern {0, 1} every 4 semitones: the hexatonic scale.

2. **Prove.** Show that the number of ways to group n pulses into 2s and 3s satisfies a(n) = a(n−2) + a(n−3).

   *Solution.* Every grouping of n pulses ends with a group of 2 or a group of 3. Removing it leaves a grouping of n−2 or
   of n−3 pulses, and every such grouping extends in exactly one way, so the two kinds are counted by a(n−2) and a(n−3),
   with a(0) = 1, a(1) = 0, a(2) = 1.

3. **Ear.** The lab plays eight short ostinatos, some with an accent on every fourth pulse, some with accents at random.
   Sort them.

   *Solution.* The lab prints the order. The regular ones let you tap a four-pulse beat after two accents; the random ones
   keep defeating the attempt.

4. **Build.** Write a program that finds, for any passage, the scale collection holding the most of its sounding time,
   with a chance baseline.

   *Where to look.* `modern.best_fit` scores each transposition of a scale by duration; for the baseline, keep the
   passage's rhythm and register and shuffle its pitch classes (or draw passages of the same length from other music),
   and report how often the shuffled passage fits as well as the real one.

5. ★ **How much of a repertoire is octatonic beyond chance, and where?**

   *Where the frontier is.* Segment a corpus of scores (by phrase, by texture change, or by a fixed window), find each
   segment's best-fitting collection under rival models (one octatonic collection; two diatonic layers; a mode), compare
   them by likelihood with a penalty for flexibility, and compare the real corpus with shuffled and with other composers'
   music; report the share of music that is octatonic beyond chance, with an interval, and where in the pieces it lies.

## Sources

* R. Taruskin, *The Oxford History of Western Music*, vol. 4 (2005), and *Stravinsky and the Russian Traditions*
  (1996); P. van den Toorn, *The Music of Igor Stravinsky* (1983); A. Berger, "Problems of pitch organization in
  Stravinsky", *Perspectives of New Music* (1963); D. Tymoczko, "Stravinsky and the octatonic: a reconsideration",
  *Music Theory Spectrum* (2002).
* E. Antokoletz, *The Music of Béla Bartók* (1984); E. Lendvai, *Béla Bartók: An Analysis of his Music* (1971);
  R. Howat, "Bartók, Lendvai and the principles of proportional analysis", *Music Analysis* (1983).
* O. Messiaen, *Technique de mon langage musical* (1944); R. Cohn, *Audacious Euphony* (2012), for hexatonic poles;
  A. Forte, *The Structure of Atonal Music* (1973).
* F. Busoni, *Sketch of a New Esthetic of Music* (1907).
* Part 6 for temperaments; Part 9 for bars and gongs; Part 11 for syncopation and polyrhythm; Part 12 for scales and
  Burnside's count; Part 15 for key profiles; Part 21 for the golden section.
