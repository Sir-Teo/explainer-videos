# Music, Built: Part 10, Writing It Down

Part 10 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), and the first part of Act II. For nine parts the series made sounds; now it has
to say which ones, and when, to someone who is not in the room. Every way of doing that keeps some things and
throws the rest away, and the part asks of each notation what it kept: neumes, Guido's staff, mensural notes, bar
lines and scores, tablature, figured bass, gongche, jianpu, guqin tablature, graphic scores, piano rolls, MIDI,
MusicXML and MEI. It ends by counting: the bits on the page of the Tune against the bits in its sound. The score
model, its readers and writers, and the counting are Monochord's (`explainer/music/monochord/score/`); the staff
is drawn by the series' own engraver (`explainer/music/staff.py`) and the other notations by
`explainer/music/notations.py`; every sound is computed in `compute.py`. Dates and attributions are the published
ones, listed under Sources.

* **A song nobody can read.** The tablet h.6 from Ugarit (about 1400 BCE): names of pairs of lyre strings, each
  with a number; its first line read two ways (neither a reconstruction); at least five published
  reconstructions, no two alike; Isidore of Seville (about 630): sounds "cannot be written down"; a tune as a
  picture with two axes; the plan.
* **1. A reminder.** Neumes, simplified to three signs; an ear question (three melodies, and all three fit the
  signs); counting the melodies that fit a contour (85 on six notes, 322 on eight; 309,538,560 for the whole Tune
  on eight); 9.5 bits against 18.1; heighted neumes and the first ruled line.
* **2. Guido's lines.** Four lines and a letter (about 1025); clefs as letters; Guido's claim (a year or two in
  place of ten); the staff as a graph, three centuries before Oresme; *Ut queant laxis* sung line by line (each
  line starts a step higher); ut, re, mi, fa, sol, la; the half step the staff does not show.
* **3. How long?** Two voices and no lengths; Franco of Cologne (about 1280); long, breve, semibreve, minim and
  their descendants; perfect and imperfect time, the circle and the broken circle (the C of common time); one
  row of marks read in twos and in threes; imperfection and alteration (breve, semibreve, semibreve, breve = 3,
  1, 2, 3); the modern system: halvings, dots and ties; a predict-pause (5/8 and 7/8); n dots give 2 − 2⁻ⁿ; why
  a third needs a triplet.
* **4. Bars and scores.** Part books; the score and the bar line (printed scores from the 1570s); two voices
  with one cursor; a note cut and tied at a bar line (Monochord's exact fractions); what was added later: tempo
  words, dynamics, hairpins, the metronome mark (1815).
* **5. What to do.** Tablature (printed for the lute in 1507); Seeger's descriptive and prescriptive writing
  (1958); middle C in three places on a guitar; 2,125,764 tablatures of fourteen notes and about 2 × 10¹⁹ of the
  Tune; the one with the least movement, by dynamic programming; figured bass (about 1600); one bass realized
  twice, among 6,291,456 ways.
* **6. Numbers and characters.** Gongche; Rousseau's numbers (1742) and jianpu; changing key by changing one
  sign; the Tune in numbers and characters, on Part 8's flute; a guqin character assembled from its parts, and
  no rhythm; graphic scores (after Feldman, 1950, and in the manner of Cardew's *Treatise*).
* **7. Holes and bytes.** The piano roll (the 1890s; Welte's reproducing piano, 1904); MIDI (1983): the first
  bytes of the Tune's file, decoded (nine bytes a note, 425 for the Tune); what a key number forgets (E♭ G B♭
  E♭ comes back as D♯ G A♯ D♯); an ear question (G♯ and A♭ in quarter-comma meantone, 41 cents apart).
* **8. The page as data.** MIDI, MusicXML (2004) and MEI; the first note of the Tune three ways; round trips
  (MusicXML returns all 42 notes with spelling, lengths and words; MIDI returns keys and lengths only); the
  table of what each notation keeps.
* **9. How many bits?** The Tune in bytes, from 126 (gongche as text) to 2.7 million (sound as on a CD); 42
  notes × 4 bits = 168 bits; 96 with its repeats; 21.3 million bits of sound: 127,000 to 1, against 6 to 1 for
  an MP3; an ear question (the page played exactly, and by four rules of performance); how far the performance
  strays (69 ms, 8 dB, a last note 1.5 times its length), and what it costs to write that down (798 bits).
* **10. Frontier: reading the page back.** Optical music recognition as a toy: row sums, line removal, blobs;
  42 of 42 on a clean page; nothing at all on a page tilted by 0.4 degrees; straightening; specks; an ear
  question (a speckled scan read back, with four mistakes); where the field and the encoding standards stand.
  ★ research problem.
* **Variation 10, recap and problems.** The Tune read from ten notations, two to a phrase, and its sixth phrase
  played as none of them says; the ledger; what we found; five problems; where it comes back; in practice;
  references; Part 11.

## What is computed, and what is heard

`python -m videos.music.music10.compute` (under a minute) fills `.cache/music10/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook` | the first line of h.6's notation, read two ways on a Pythagorean scale | the line as published; the pairs of strings of CBS 10996 |
| `neumes` | the melodies on 6, 7, 8 notes with the contour of the Tune's first phrase; two others drawn at random | brute force over all 6⁷ melodies |
| `guido` | *Ut queant laxis* sung by Part 8's voice | the first notes of its six lines: C D E F G A |
| `mensural` | one row of marks read under imperfect and perfect time; imperfection and alteration; dots and ties | Franco's rules as Apel states them; every length k/64 |
| `score` | the Tune's first two phrases with a bass, on Part 7's piano | — |
| `tab` | every place each note can be played on a guitar; the fingering with the least movement | it sounds the Tune; it beats the one-string fingering |
| `figured` | every realization of each figure within a hand's reach; two smooth ones | each chord holds the notes its figure asks for; no parallel fifths or octaves |
| `east` | the Tune in jianpu and gongche | — |
| `midi` | the bytes of the Tune's MIDI file; a round trip that loses spelling; G♯ and A♭ in meantone | the Standard MIDI File format; 128/125 = 41.06 cents |
| `xml` | MusicXML and MEI of the Tune; what each round trip returns | the score itself |
| `bits` | the bytes of seven encodings and four audio codecs (ffmpeg); bits spelled out, by entropy and by structure; a performance by rule | — |
| `omr` | a page as a bitmap, read back; accuracy against tilt and specks; deskewing | the page's own notes |
| `tune` | Variation 10 | the first 35 notes are on the page's beat exactly |

Monochord's score model and the engraver are held against these in `tests/music/test_score.py`,
`tests/music/test_staff.py` and `tests/music/test_notations.py`; this part's claims and clips in
`tests/music/test_music10.py`.

**Sounds.** Twelve clips, labelled on screen. `physical model`: Part 1's plucked string, Part 7's piano and
guitar, Part 8's flute and voice, playing notes that this part's code read from a notation. `synthesized`: the
two organ tones of chapter 7. There are no recordings.

**What the models are, and are not.** *The tablet.* The two readings of h.6's first line are not
reconstructions: they are two of the ways the same signs can be read (strings together or in turn; the lyre
counted from either end; the numbers as strokes), on a seven-note scale tuned by fifths. The pairs of strings
are those of the Babylonian tablet CBS 10996 as Kilmer and West give them. *Neumes* are reduced to three signs
(higher, the same, lower); real neumes also show groups of notes on a syllable and, in some scripts, lengthening.
*The hymn* is sung in equal notes, each line on the vowel of its first syllable, by Part 8's source-filter voice;
its melody is the one in modern chant books. *Mensural notation* is shown for breves and semibreves only, with
Franco's rules of imperfection and alteration; the film uses the three simplest cases. *The engraver* draws one
voice to a staff, with no chords or slurs. *Tablature's* cost of a move is a plain rule (travel along the neck is
dear, crossing strings is cheap), not a model of a hand. *Figured bass* is realized within a fixed range with
three upper notes, choosing by total movement and forbidding parallel fifths and octaves; real continuo playing
has many more rules and freedoms. *The performance* follows four rules from the literature (Todd; Friberg and
Sundberg) with constants chosen to be audible; it is one plausible reading, and the film says a machine made it.
*The bit counts* are for this tune and these files: 168 bits is a fixed-length code for this tune's six pitches
and two lengths, not a universal figure. *The page reader* reads only what `raster.page` draws; it is there to
show why the first step of the classical pipeline is fragile, and it is not a music reader.

## Build

```bash
python -m videos.music.music10.compute                          # numbers and sounds (under a minute)
EXPLAINER_TTS=silent python tools/build.py music10 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music10 --sync                         # the sound gates
python tools/dead_air.py renders/music10_480p.mp4 --sound music10  # no empty screen; no sound over a still one
python tools/lecture_length.py music10                          # 30 to 60 minutes, listening included
python tools/build.py music10                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 10                                  # the lab (writes a figure and a short WAV)
```

The staff needs a font with the Unicode musical symbols (GNU FreeFont's FreeSerif is used here) and the gongche
and guqin characters a CJK font (AR PL UMing); `explainer/music/staff.py` says which fonts it looks for.

## Problems, with solutions

1. **Neumes.** How many melodies on the seven notes C to B have the contour up, up, down, down, up? Count them
   with a table: for each note, the number of ways to finish the melody from there.

   *Solution.* Work backwards. From the last note there is one way to finish, wherever it is: 1, 1, 1, 1, 1, 1, 1
   (for C … B). The step before it must rise, so from each note the ways are the number of notes above it: 6, 5,
   4, 3, 2, 1, 0. The step before that falls, so add up the entries below each note: 0, 6, 11, 15, 18, 20, 21.
   Another fall: 0, 0, 6, 17, 32, 50, 70. Then a rise (add the entries above): 175, 175, 169, 152, 120, 70, 0.
   And a rise again: 686, 511, 342, 190, 70, 0, 0. The total is 686 + 511 + 342 + 190 + 70 = **1799** melodies,
   of 7⁶ = 117,649: the five signs carry log₂(117649/1799) ≈ 6.0 of the 16.8 bits. (The lab prints the table.)

2. **Dots and ties.** Show that a note with *n* dots lasts 2 − 2⁻ⁿ times its plain length, and that any length
   k/2ᵐ of a whole note can be written with no more tied notes than there are ones in the binary expansion of k.

   *Solution.* Each dot adds half of what the one before added, so the length is 1 + ½ + ¼ + … + 2⁻ⁿ, a geometric
   series with sum (1 − 2⁻ⁿ⁻¹)/(1 − ½) = 2 − 2⁻ⁿ. For the second part, write k in binary: k/2ᵐ is then a sum of
   distinct note values 2ʲ/2ᵐ, one for each 1 in k, and tying those notes gives the length. That is the bound.
   Dots do better: a run of adjacent ones in k is one dotted note (7/8 = ½ + ¼ + ⅛ is a half note with two
   dots), so the least number of notes is the number of runs of ones, if any number of dots is allowed.

3. **Ear.** The lab plays six pairs of notes in quarter-comma meantone. For each pair, say whether you heard a
   sharp and the flat next to it, 41 cents apart, or the same note twice.

   *Solution.* The lab prints the order. 41 cents is about eight times the smallest difference a practised
   listener can hear near 400 Hz, so with attention every pair can be got right; it is easiest to sing the first
   note and feel whether the second asks the voice to move.

4. **Build.** With `score.tab`, change the cost of a move so that open strings are avoided, and find the best
   fingering of the Tune. How many frets does the hand now span, and how many tablatures did you rule out?

   *Solution.* In the lab set `OPEN = 10.0`. The only note of the Tune with an open string is E (the top string),
   which now moves to the fifth fret of the B string, and the F beside it to the sixth: the Tune sits on the B
   and top strings from fret 1 to fret 6, with no open strings. Each of the Tune's eight Es had three places and
   now has two, so the tablatures left are (2/3)⁸ ≈ 3.9% of the 2.16 × 10¹⁹: about 96% are ruled out, and
   8.4 × 10¹⁷ remain. (With `OPEN = 3.0` the open E survives where the hand would otherwise have to shift.)

5. ★ **A notation for the performance.** Design a notation for the Tune that also keeps the four rules of
   performance from chapter 9, in fewer than 300 bits in all. What must its reader already know? Is your notation
   descriptive or prescriptive?

   *Where the frontier is.* Writing the performance note by note costs about 800 bits, but the performance was
   generated by four rules with half a dozen constants, so 168 bits of notes plus a few dozen bits of constants
   reproduce it exactly, provided the reader holds the rules. That is the bargain of every notation in the part:
   the shorter the page, the more the reader must know. It is also a research programme. Rule systems for
   performance (Sundberg and Friberg's at KTH; Todd's models) explain part of what players do; models fitted to
   recorded performances predict timing and dynamics measurably better than rules, and none yet accounts for why
   two great players differ. Whether "expression" can be written down in few bits is the question of how much of
   it is rule and how much is choice.

## Sources

Books: T. F. Kelly, *Capturing Music: The Story of Notation* (2015); E. Gould, *Behind Bars: The Definitive Guide
to Music Notation* (2011); E. Selfridge-Field (ed.), *Beyond MIDI: The Handbook of Musical Codes* (1997); W. Apel,
*The Notation of Polyphonic Music, 900–1600* (5th ed., 1953), for mensural notation and the rules of imperfection
and alteration; O. Strunk (ed.), *Source Readings in Music History* (1950), for Isidore, Guido's *Prologus* and
*Epistola de ignoto cantu*, and Franco's *Ars cantus mensurabilis*; D. Pesce, *Guido d'Arezzo's Regule rithmice,
Prologus in antiphonarium, and Epistola ad Michahelem* (1999); A. Barbera (ed.), *Music Theory and Its Sources:
Antiquity and the Middle Ages* (1990); B. Yung, *Celestial Airs of Antiquity: Music of the Seven-String Zither of
China* (1997); the MIDI 1.0 Detailed Specification (1983; 1996) and the Standard MIDI Files 1.0 specification.

Papers: A. D. Kilmer, "The discovery of an ancient Mesopotamian theory of music", *Proceedings of the American
Philosophical Society* 115 (1971), and "The cult song with music from ancient Ugarit: another interpretation",
*Revue d'Assyriologie* 68 (1974); M. L. West, "The Babylonian musical notation and the Hurrian melodic texts",
*Music & Letters* 75 (1994) (whose remark on rival decipherments "each yielding entirely different results" the
film paraphrases); C. Seeger, "Prescriptive and descriptive music-writing", *The Musical Quarterly* 44 (1958);
N. P. McA. Todd, "A model of expressive timing in tonal music", *Music Perception* 3 (1985), and "The dynamics of
dynamics: a model of musical expression", *JASA* 91 (1992); A. Friberg and J. Sundberg, "Does music performance
allude to locomotion? A model of final ritardandi derived from measurements of stopping runners", *JASA* 105
(1999); M. Good, "MusicXML for notation and analysis", in *The Virtual Score* (2001); P. Roland, "The Music
Encoding Initiative (MEI)", *Proceedings of the First International Conference on Musical Applications Using XML*
(2002); D. Pruslin, "Automatic recognition of sheet music", ScD thesis, MIT (1966); J. Calvo-Zaragoza and D. Rizo,
"End-to-end neural optical music recognition of monophonic scores", *Applied Sciences* 8 (2018); J. Calvo-Zaragoza,
J. Hajič jr. and A. Pacha, "Understanding optical music recognition", *ACM Computing Surveys* 53 (2020).
