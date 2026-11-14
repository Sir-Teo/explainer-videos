# Music, Built: Part 23, Chant to Polyphony

Part 23 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first part of Act IV. Act III built and tested the grammar of one tradition; this
part goes back to ask how that tradition came to have more than one voice at all. It follows Western music from chant
to about 1400: the eight modes, Guido's hexachords and staff, organum in three stages, rhythm written first as six
patterns and then note by note, the motet, the Ars nova's mensuration and isorhythm, Machaut, a century of polyphony
counted, and the Ars subtilior. The theory is Monochord's (`explainer/music/monochord/medieval.py`); the
fourteenth-century pieces are 89 transcriptions from *Polyphonic Music of the Fourteenth Century*, as encoded in the
music21 corpus (`explainer/music/monochord/trecento.py`); everything heard is sung by Part 17's synthetic choir.
Published findings are the ones listed under Sources.

* **Paris, about 1200.** Odo of Sully's decrees of 1198 and 1199; an organum on one held F in the manner of the Notre
  Dame quadrupla, ours, heard; the problem of keeping four moving voices together; the plan.
* **1. Chant and the eight modes.** *Ut queant laxis* sung; finals, ranges and reciting tones; psalmody, psalm tones and
  *differentiae*; an ear question (two psalm verses ending on D: which is the first mode?); the theorists' rule as a
  classifier (*Ut queant laxis*: mode 2; all eight psalm tones right).
* **2. Guido's hexachords.** The letter to Brother Michael (about 1030); ut re mi fa sol la; the gamut of 22 notes and
  its seven hexachords; mutation heard (a line through B♭ and then B♮, one mutation at the G), solmization as a
  shortest path; the staff and the clefs; the Guidonian hand.
* **3. Parallel organum.** *Musica enchiriadis* (late ninth century); an ear question (organa at the fifth below a
  psalm verse reciting on F: with B♭, or with B♮ and 9 tritones?); the boundary rule, oblique motion and the
  *occursus*, heard.
* **4. Free and florid organum.** The Winchester Troper; Guido's *Micrologus*; *Ad organum faciendum*; florid organum
  over six chant notes, ours, heard; discant and organum purum; *Congaudeant catholici*.
* **5. The rhythmic modes.** Six patterns of long and short, heard on one line; perfections; reading the mode from
  ligature patterns (a small parser).
* **6. Notre Dame.** Anonymous IV, Léonin and Pérotin, the *Magnus liber*; a discant clausula, ours, heard; consonance
  on the beat and voice exchange in the opening's organum.
* **7. The motet.** Words under a clausula; polytextual motets; a three-voice motet, ours, heard; Franco of Cologne's
  note shapes; Petrus de Cruce and the hocket.
* **8. The Ars nova and mensuration.** De Vitry, de Muris, John XXII and Jacques de Liège; tempus and prolation, one row
  of shapes heard in the four mensurations; imperfection and alteration as a program.
* **9. Isorhythm.** Color against talea (7 pitches and 5 notes meet after 35), heard; a talea scan of de Vitry's four
  motets in the corpus (12, 18 and 33 bars; *Lugentium siccentur*'s tenor repeats 98 bars in 100 at 33, against 72 by
  chance); the opening of *Vos qui admiramini*, sung from the edition.
* **10. Machaut and the cadence.** Machaut's life and books, the *Messe de Nostre Dame*, *Ma fin est mon
  commencement*; an ear question (a cadence to D with and without two leading tones); 1,410 sixth-to-octave cadences
  in the corpus, 71 in 100 with a rising semitone, 459 with two.
* **11. A century, counted.** The corpus; on the beat 59 in 100 intervals perfect and 8 dissonant, elsewhere 34 and
  23; parallel fifths and octaves 2.9 in 100 moves against Bach's 0.05; 88 of 89 pieces end on bare fifths and octaves,
  all 364 of Bach's chorales with a third; the Landini cadence, heard, counted 173 times (Landini 14 in 4 pieces,
  Ciconia 69 in 18, the earlier Italians hardly at all).
* **12. The Ars subtilior.** The Schism, Avignon, Foix and Aragon; three voices in proportion, ours, heard; Cordier's
  heart and circle; what the corpus cannot say.
* **13. Frontier: what the notation does not settle.** *Musica ficta*: 2,149 of 65,681 notes outside Guido's gamut,
  64 in 100 of them rising a semitone, mostly editorial; chant rhythm (Solesmes, Cardine); the Cantus database and mode
  classifiers. ★ research problem: learning the rules of ficta from editions.
* **Variation 23, recap and problems.** The Tune as chant, as organum and as an isorhythmic motet (a color of 7
  pitches through a talea of 4 notes, meeting after 28); the ledger; what we found; five problems; where it comes back;
  in practice; references; Part 24.

## What is computed, and what is heard

`python -m videos.music.music23.compute` (under a minute) fills `.cache/music23/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook` | an organum on a held F, upper voices in the first mode, consonant on every perfection, with voice exchange | its own rules (tests) |
| `chant` | *Ut queant laxis*; the eight modes; psalm tones; the mode classifier | the eight psalm tones |
| `guido` | the gamut, the hexachords, solmization by fewest mutations | brute force (tests) |
| `organum` | parallel organum at the fifth with B♭ and with B♮; the Enchiriadis rule; florid organum | tritone counts |
| `rhythm` | the six rhythmic modes on one line; ligature patterns | the parser (tests) |
| `notre`, `motet` | a discant clausula; a three-voice motet with a tenor ordo | — |
| `mensuration` | one row of shapes in the four mensurations; Franco's imperfection and alteration | whole perfections (tests) |
| `isorhythm` | the engine; talea scans of every piece, de Vitry's motets in detail | shuffled bars |
| `vitry`, `landini` | excerpts sung from the edition's pitches; Landini cadences by composer | — |
| `census` | intervals on and off the beat, parallels, cadences, final sonorities, notes outside the gamut | Part 17's chorales |
| `cadence`, `subtilior` | the double leading-tone cadence; three voices in proportion | — |
| `tune` | Variation 23 | — |

Monochord's tools are held in `tests/music/test_medieval.py`; this part's claims and clips in
`tests/music/test_music23.py`.

**Sounds.** Part 17's choir (Part 8's source-filter voice), labelled `synthesized`. There are no recordings.

**What the models are, and are not.** *The pieces "ours"* (the hook's organum, the florid organum, the clausula, the
motet, the proportions) are computed in the manner of their repertories; they are not reconstructions of real works.
*The psalm tones* are simplified formulas with the right finals and reciting tones, not the Liber Usualis's tones with
their *differentiae*. *Ut queant laxis* is given in pitches only, after the Liber Usualis, in equal notes; chant's
rhythm is one of the open questions of chapter 13. *The corpus* is 89 pieces, mostly Italian and mostly Mass
movements, with no Machaut and no Ars subtilior songs; its pitches include the editors' accidentals, so its counts of
leading tones are partly counts of editorial decisions, and its bars are the edition's. *The talea scan* compares bars
by rhythm alone; it finds de Vitry's taleae but its chance level is high for tenors of plain long notes. *The excerpts*
are sung by synthetic voices on vowels, without the texts. *The Landini cadence* is detected as the top voice moving
leading tone, step down, third up onto an octave or unison with the lowest voice.

## Build

```bash
python -m videos.music.music23.compute                          # numbers and sounds (under a minute)
EXPLAINER_TTS=silent python tools/build.py music23 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music23 --sync                         # the sound gates
python tools/dead_air.py renders/music23_480p.mp4 --sound music23  # no empty screen; no sound over a still one
python tools/lecture_length.py music23                          # 30 to 60 minutes, listening included
python tools/build.py music23                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 23                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** A tenor's color has 28 pitches and its talea 8 notes. After how many notes do they begin together
   again, and how many statements of each is that?

   *Solution.* lcm(28, 8) = 56 notes: 2 statements of the color and 7 of the talea (`medieval.periods(28, 8)`).
   Machaut's motets often divide a color into whole taleae instead, so that the two align at every color.

2. **Prove.** Prove that Franco's rules (imperfection and alteration) read any row of breves and semibreves between
   breves in perfect time as whole perfections.

   *Solution.* A breve alone is a perfection (3). A run of n semibreves between breves has n = 3q + r. The 3q fill q
   perfections. If r = 1, the single semibreve imperfects the breve before it: 2 + 1 = 3. If r = 2, the second is
   altered: 1 + 2 = 3. So every run, with its neighbouring breve where needed, fills whole perfections, and so does the
   row (`medieval.read_perfect`; the tests check it).

3. **Ear.** The lab sings psalm verses in the eight modes in random order. Name each one's mode.

   *Solution.* The lab prints the answers. Listen for the final (where the verse ends) and the reciting tone (the note
   repeated most); a reciting tone a fifth above the final, or C above E or F, is authentic; a third or fourth above
   it, plagal.

4. **Build.** Improve the talea scan so that it also requires the pitches to change while the rhythm repeats, and run
   it on the corpus.

   *Where to look.* `medieval.talea_scan` compares bars by rhythm; add the pitch sequence of each bar and count a lag
   only where the rhythm matches and the pitches do not (or match the color's own period, `color_scan`). The chance
   level for tenors of plain long notes should fall, and *Vos qui admiramini* and *Rex quem metrorum* should separate
   from chance more clearly.

5. ★ **Musica ficta.** Learn the rules of *musica ficta* from edited pieces, and measure where two editions of the same
   piece disagree.

   *Where the frontier is.* Treat each note as a choice (written, raised or lowered), with features from its voice
   (the next note, whether a cadence follows) and from the other voices (the interval it makes, the tritones it would
   cause); train on edited pieces and test on held-out ones. Different editions of the same works exist for parts of
   this repertory; the disagreements between editors are the ground truth for how uncertain the answer is. Bent's
   *Counterpoint, Composition, and Musica Ficta* (2002) sets out what the theorists required.

## Sources

* R. H. Hoppin, *Medieval Music* (1978); R. Taruskin, *The Oxford History of Western Music*, vol. 1 (2005);
  T. F. Kelly, *Capturing Music: The Story of Notation* (2014); D. Hiley, *Western Plainchant: A Handbook* (1993).
* *Musica enchiriadis* and *Scolica enchiriadis* (late ninth century); Guido of Arezzo, *Micrologus* (about 1026) and
  the letter to Michael (about 1032); Johannes de Garlandia, *De mensurabili musica* (about 1250); Franco of Cologne,
  *Ars cantus mensurabilis* (about 1280); Anonymous IV (about 1280); the *Ars nova* treatises (about 1320).
* *Polyphonic Music of the Fourteenth Century*, ed. L. Schrade and others (Monaco: Éditions de l'Oiseau-Lyre,
  1956–1991); M. S. Cuthbert and C. Ariza, "music21: a toolkit for computer-aided musicology and symbolic music data",
  *ISMIR* (2010), whose corpus holds the encodings.
* U. Günther, "Das Ende der ars nova", *Die Musikforschung* 16 (1963); F. Ludwig on isorhythm (1904).
* M. Bent, *Counterpoint, Composition, and Musica Ficta* (2002); E. Cardine, *Sémiologie grégorienne* (1970).
* The Cantus database (cantus.uwaterloo.ca and Cantus Index); P. Cornelissen, W. Zuidema and J. A. Burgoyne, "Mode
  classification and natural units in plainchant", *ISMIR* (2020).
* Part 11 for polyrhythms and least common multiples; Part 16 for organum and the rules of counterpoint; Part 17 for
  the chorales and the choir; Part 20 for the crab canon.
