# Music, Built: Part 27, The Romantic Century

Part 27 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fifth and last part of Act IV. Part 26 ended with the Classical style's shared
expectations; this part follows the century that stretched them. It starts from Schubert's *Der Lindenbaum* and follows
the piano's growth, the Lied, the character piece and the mazurka, rubato, programme music, Wagner, national styles and
the concert as a museum, and tests the familiar claim that harmony was stretched until the key could barely hold on a
Library of 827 pieces from 1370 to 1924. The tools are Monochord's (`explainer/music/monochord/romantic.py`, with Part 15's
key profiles); the music is every dated piece in the music21 corpus from C. P. E. Bach to Webern, read whole, beside the
collections Parts 17 and 23 to 26 read. Published findings are the ones listed under Sources.

* **A song under a linden tree.** Schubert in 1827; *Der Lindenbaum*'s prelude and first phrase, heard (Part 7's piano
  and Part 17's synthetic tenor); the plan.
* **1. The piano grows.** Érard's double escapement, Babcock's iron frame, felt hammers, Steinway; documented compasses
  from 54 keys (Cristofori) to 88 (Steinway, 1880s); every C of a 1780s fortepiano and the Cs added since, heard; the
  Library's keyboard pieces by range (Clara Wieck's polonaises of 1831 reach E7, far above Mozart's F6); the piano in
  the parlour.
* **2. The song and its piano.** The Lied and Schubert; *Der Lindenbaum* read two bars at a time (E major, its second
  stanza in E minor, a stormy middle, E major again); the piano plays 1,443 notes to the voice's 205; an ear question
  (the same four bars in major and minor: which is minor?); song cycles.
* **3. Small pieces, large feelings.** The character piece; an ear question on Chopin's Mazurka Op. 6 No. 2 (equal beats
  or a mazurka's uneven ones: which dances?); what recordings show about mazurka timing; Chopin and Poland.
* **4. Stolen time.** Mozart's letter of 1777; Todd's phrase arch drawn; the Tune strict, arched and with stolen time,
  heard; performances measured (Repp, the Mazurka Project).
* **5. Music that tells a story.** Berlioz's programme; the Tune's head as an *idée fixe* in five guises, heard; wind,
  brass and timpani players called for by five symphonies (5, 9, 18, 27, 19); Berlioz's treatise, valves and Sax; Liszt
  and the symphonic poem, Hanslick's objection.
* **6. Wagner: the endless melody.** Verdi and bel canto (*La donna è mobile*: 2 notes in 100 outside its key); the music
  drama; a plain cadence and the Tristan chord, heard; the chord held by 5 keys' scales against 8 for a plain triad; the
  leitmotif; Bruckner, Mahler, Strauss; after *Tristan*.
* **7. The stretching, measured.** Chromaticism and tonal clarity defined; the Library plotted by year; from 1680 to 1900
  the trend over all 31 points is not clear of zero (+2.6 points a century, 95% interval −0.8 to +4.9), over the 23
  instrumental ones it is (+5.6, 2.4 to 8.2); songs (5 in 100) against instrumental music (10); an ear question
  (Schumann's most chromatic passage or a typical Haydn one: which is later?); what the measure cannot say.
* **8. Nations and their songs.** Glinka, the Five, Smetana, Grieg; *Lift Every Voice and Sing* (1900) sung by the
  choir and sixteen bars of the *Maple Leaf Rag* (1899), heard; Dvořák in America, the Fisk Jubilee Singers,
  Liliʻuokalani; whose music?
* **9. The concert becomes a museum.** Paganini and Liszt; the conductor; Mendelssohn's *St Matthew Passion*, the
  complete editions and the canon (Weber); Clara Schumann and Fanny Hensel; Edison and Brahms's cylinder.
* **10. Frontier: harmony and performance as data.** Symbolic corpora; audio corpora (Weiß et al. 2019); early
  recordings; ★ research problem: when, and in which genres, did nineteenth-century harmony change fastest?
* **Variation 27, recap and problems.** The Tune as a nocturne (20 melody notes over 48 in the left hand, under a phrase
  arch), as a Lied (a synthetic tenor over rustling triplets) and as a leitmotif (minor, augmented, darkening chords);
  the ledger; what we found; five problems; where it comes back; in practice; Part 28.

## What is computed, and what is heard

`python -m videos.music.music27.compute` (a few minutes) fills `.cache/music27/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook`, `lied` | *Der Lindenbaum*: bars 1–15; its keys two bars at a time; notes per two bars; the first and second stanzas' opening bars | the score's stanzas |
| `keyboards` | documented compasses; ranges of the Library's keyboard pieces; every C, then the new ones | the makers' compasses |
| `mazurka`, `rubato` | Chopin's Op. 6 No. 2 theme, strict and with uneven beats; the Tune strict, arched, stolen | the models (tests) |
| `idee`, `tristan` | the Tune's head in five guises; a cadence and the Tristan chord; keys whose scales hold each chord | — |
| `library` | chromaticism and clarity for 827 pieces; the 1680–1900 trend with a 4,000-resample bootstrap; songs against instruments; two quartet passages | Part 15's profiles |
| `nations`, `orchestra` | *Lift Every Voice and Sing* and the *Maple Leaf Rag*; the winds that five symphonies call for | the scores |
| `tune` | Variation 27 | — |

Monochord's tools are held in `tests/music/test_romantic.py`; this part's claims and clips in
`tests/music/test_music27.py`.

**Sounds.** Part 7's piano and bowed string (physical models); Part 17's synthetic voice and choir singing a vowel
(synthesized). There are no recordings.

**What the models are, and are not.** *The readers* keep every note of a score (chords whole, ties merged, transposing
instruments at sounding pitch, Humdrum's split spines followed), unlike the line readers of Parts 24–26. *Chromaticism*
is measured against the best Krumhansl–Kessler key of each sixteen-beat window, with the natural, harmonic and melodic
minor all counted as inside; modal music and quick modulations both register as chromatic, so the earliest points carry
the method's bias. *The Library* is what the corpus happens to hold: a few dozen dated Romantic pieces, many songs, no
symphonies; the trend is reported with its interval and split by genre for that reason. *Dates* are of composition
(Clara Wieck's polonaises by their publication, 1831). *The mazurka's beat lengths and the phrase arch's depth* are
illustrations, not measurements of any pianist. *The Tristan chord* is played as textbooks give it, not as Wagner
scored it. *The keyboard compasses* are representative instruments' documented ranges, rounded to the key.

## Build

```bash
python -m videos.music.music27.compute                          # numbers and sounds (a few minutes)
EXPLAINER_TTS=silent python tools/build.py music27 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music27 --sync                         # the sound gates
python tools/dead_air.py renders/music27_480p.mp4 --sound music27  # no empty screen; no sound over a still one
python tools/lecture_length.py music27                          # 30 to 60 minutes, listening included
python tools/build.py music27                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 27                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** A window holds C, E and G for 10 beats and F♯ and B♭ for 2 beats, and its key is C major. Compute its
   chromaticism.

   *Solution.* F♯ and B♭ are outside C major's scale; the share of sounding time on them is 2/(10 + 2) = 1/6, about
   0.17, or 17 in 100.

2. **Prove.** Show that a phrase arch whose tempo is symmetric about the middle of the phrase leaves the phrase's
   midpoint where strict time puts it, if the phrase's total length is unchanged.

   *Solution.* Performance time is T(b) = ∫₀ᵇ du/v(u). If v(u) = v(L − u), then ∫₀^{L/2} du/v(u) = ∫_{L/2}^{L} du/v(u)
   (substitute u → L − u), so each half takes half the total. If the total equals L, as in strict time, the midpoint is
   reached at L/2.

3. **Ear.** The lab plays eight performances of the Tune's first two phrases, strict, arched or stolen. Sort them.

   *Solution.* The lab prints the order. Strict performances have even notes against the bass; arched ones start and
   end slower with the bass bending too; stolen ones keep the bass even while the melody pushes ahead early in each
   bar and arrives with the bass on the bar line.

4. **Build.** Add a third measure to the Library: the share of sounding time on sonorities that are not triads or
   seventh chords, and plot it by year.

   *Where to look.* At every onset, collect the sounding pitch classes (`romantic.all_notes` and the sonority idea of
   `classical.Movement.sonority`), classify the set by its interval content (major, minor, diminished and augmented
   triads, the five seventh chords, any subset of them), weight by duration, and report the trend with the same
   bootstrap; expect the counterpoint of the earliest pieces to score high for a different reason.

5. ★ **When did harmony change fastest?** Answer with intervals, and by genre.

   *Where the frontier is.* Assemble a corpus with balanced dates and genres (symbolic, from encodings with harmonic
   analyses where they exist, and from audio, as Weiß and colleagues did), measure each piece, and fit a model with year
   as a smooth function, genre as a factor and composer as a random effect; report where the derivative is largest and
   with what uncertainty, and whether the answer survives changing the measure.

## Sources

* R. Taruskin, *The Oxford History of Western Music*, vol. 3 (2005); C. Rosen, *The Romantic Generation* (1995);
  C. Dahlhaus, *Nineteenth-Century Music* (1980; trans. 1989).
* W. Weber, *The Great Transformation of Musical Taste* (2008); H. Berlioz, *Grand traité d'instrumentation*
  (1844); E. Hanslick, *Vom Musikalisch-Schönen* (1854); R. Wagner, *Über das Dirigieren* (1869).
* N. P. M. Todd, "The dynamics of dynamics: a model of musical expression", *JASA* (1992); B. H. Repp, "Diversity and
  commonality in music performance: an analysis of timing microstructure in Schumann's *Träumerei*", *JASA* (1992);
  the CHARM Mazurka Project (2006–2009); R. Philip, *Early Recordings and Musical Style* (1992); D. Leech-Wilkinson,
  *The Changing Sound of Music* (2009).
* C. Weiß, M. Mauch, S. Dixon and M. Müller, "Investigating style evolution of Western classical music: a computational
  approach", *Musicae Scientiae* (2019).
* C. L. Krumhansl, *Cognitive Foundations of Musical Pitch* (1990), for the key profiles.
* M. S. Cuthbert and C. Ariza, "music21" (*ISMIR* 2010), whose corpus holds the Library's encodings.
* Part 7 for the piano and the bowed string; Part 15 for keys; Part 17 for the voice and choir; Part 21 for chroma;
  Parts 23 to 26 for the earlier collections.
