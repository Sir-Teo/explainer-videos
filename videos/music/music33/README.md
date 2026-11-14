# Music, Built: Part 33, The Mathematics of Rhythm and Scale

Part 33 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the last part of Act V. An algorithm written to time pulses in a neutron accelerator
turned out to generate the rhythms of Cuba, Ghana, Bulgaria and Persia: it is Euclid's algorithm. This part follows the
same mathematics to scales, continued fractions, rhythmic oddity and homometry, canons that tile time (to a Vuza canon of
period 72, found by search and verified), Sanskrit prosody's Fibonacci numbers and de Bruijn mnemonic, change ringing,
temperaments as linear maps, and the Bohlen–Pierce scale, ending at an open conjecture about tiling. The mathematics is
Monochord's (`explainer/music/monochord/mathmusic.py`); rhythms are played on Part 11's kit and Part 9's drum, notes on
Part 7's piano, changes on Part 9's bells, and the Bohlen–Pierce tones are synthesized. Published findings are the ones
listed under Sources.

* **A timing problem, solved by Euclid.** The tresillo E(3,8), the cinquillo E(5,8) and the West African bell E(7,12),
  heard as necklaces; Bjorklund (2003) and Toussaint (2005); Toussaint's work on rhythm; the plan.
* **1. Euclid's rhythms.** Bjorklund's process for E(5,13) step by step; why it is Euclid's algorithm; where the cycle
  starts (rotations); Toussaint's catalogue, nine rhythms each checked as a rotation of E(k,n); an ear question (two
  rhythms of five in eight: the cinquillo is the even one); all 7 five-in-eight necklaces ranked by evenness.
* **2. One shape, rhythm and scale.** E(7,12) is the major scale and E(5,12) the pentatonic, heard as rhythms and as
  notes; Clough and Douthett's maximally even sets; three Euclidean rhythms layered, heard; the same shape in calendars,
  pixel lines and Sturmian words.
* **3. Stacks of fifths.** Two step sizes after 2, 3, 5, 7 and 12 fifths, three otherwise; the three-gap theorem;
  continued fractions of the fifth (7/12, 24/41, 31/53) and the moments of symmetry up to 60 (2, 3, 5, 7, 12, 17, 29,
  41, 53); stacks of 5, 7 and 12 heard; the golden ratio, whose sizes are the Fibonacci numbers.
* **4. Oddity and homometry.** Arom's oddity property, impossible above half the pulses; odd rhythms counted (in twelve
  pulses: 20 of four strokes, 16 of five, 6 of six, none of seven); an ear question (two rhythms with the same intervals:
  0 1 2 5 and 0 1 3 4, the only such pair of four in eight; 15 classes of six in twelve); the two properties together;
  what they mean.
* **5. Tiling the line.** A small canon (0 1 4 5 entering at 0 and 2 fills eight pulses), heard, and why it is
  periodic; a Vuza canon of period 72 ({0, 8, 16, 18, 26, 34} entering at {0, 1, 5, 24, 25, 29, 30, 36, 49, 53, 60, 66}),
  heard, with 1,296 tilings by its rhythm and 432 of them aperiodic; how the search works; why 72 (the non-Hajós lengths
  72, 108, 120, 144, 168, 180 ...); composers; from Hajós's cubes to canons.
* **6. Pingala's syllables.** The eight rhythms of five beats, heard; Fibonacci counts (1, 2, 3, 5, 8, 13, 21 ...);
  Halayudha's *meru* (patterns by number of heavy syllables); *yamātārājabhānasalagāḥ* as a de Bruijn sequence, heard;
  combinatorics in prosody.
* **7. Change ringing.** Plain hunt on four bells; plain hunt on six, heard; Plain Bob Minimus, all 24 orders of four
  bells and back to rounds, heard; bells and the symmetric group.
* **8. Temperaments as linear maps.** Vals, monzos and commas in the kernel; a temperament finder (records up to 60: 5,
  7, 9, 10, 12, 19, 22, 31, 34, 53) and which commas each of 12, 19, 31 and 53 tempers out; an ear question (one triad in
  19, just, 12 and 31: which is just?); instruments for more than twelve; regular temperaments.
* **9. A scale without octaves.** The Bohlen–Pierce scale: 13 steps of 146.3 cents in the 3:1 tritave; its scale and its
  3:5:7 chord on odd and on all harmonics, heard; why it works; its life since.
* **10. Frontier: tilings and open problems.** Fuglede's spectral conjecture; Coven and Meyerowitz's conditions; other
  open problems; mathematical music theory as a field; ★ research problem: is maximal evenness a cultural choice or a
  cognitive constraint?
* **Variation 33, recap and problems.** The Tune's first twelve notes as the twelve voices of the Vuza canon; plain hunt
  on bells tuned to its first four pitches; its opening in the Bohlen–Pierce Lambda mode; the ledger; what we found;
  five problems; where it comes back; in practice; references; Part 34.

## What is computed, and what is heard

`python -m videos.music.music33.compute` (about ten seconds) fills `.cache/music33/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook`, `euclid`, `rank`, `layers` | Euclidean rhythms; Bjorklund's stages; the catalogue; evenness of all five-in-eight necklaces; layers | Toussaint's rotations (tests) |
| `even` | E(7,12) and E(5,12) as rhythms and scales | — |
| `mos`, `golden` | continued fractions; moment-of-symmetry sizes for the fifth and the golden ratio | the three-gap theorem |
| `oddity` | odd rhythms counted for 8, 12, 16 pulses; homometric classes | the pigeonhole bound |
| `canon` | a small canon; the Vuza canon at 72 and every tiling by its rhythm | tiling and periodicity checks |
| `prosody`, `meru` | Pingala's counts; the rhythms of five; the de Bruijn mnemonic; heavy-syllable counts | Fibonacci; binomials |
| `ringing`, `hunt6` | plain hunt on four and six bells; Plain Bob Minimus | all 24 rows distinct |
| `temper` | record-setting equal divisions; vals; commas tempered out; four tunings of a triad | known commas |
| `bp` | the Bohlen–Pierce step and its approximations | — |
| `tune`, `variation` | Variation 33 | — |

Monochord's tools are held in `tests/music/test_mathmusic.py`; this part's claims and clips in
`tests/music/test_music33.py`.

**Sounds.** Part 11's clave, woodblock and hat and Part 9's drum and bells (physical models), Part 7's piano (retuned
for the temperaments), and additive tones for the Bohlen–Pierce scale. There are no recordings; the traditional
rhythms are played as bare timelines, not as the music they belong to.

**What the models are, and are not.** *A timeline* here is a pattern of strokes on one instrument; in the music it comes
from it is one part among many, with its own sound, accents and dance. *Evenness* is a distance to the perfectly even
spacing; Toussaint and others use several other measures. *The Vuza canon* was found by this part's own search from one
chosen rhythm; it is one of many. *The temperament finder* looks only at the fifth and the major third (the 5-limit),
with each prime mapped to its nearest step.

## Build

```bash
python -m videos.music.music33.compute                          # numbers and sounds (about ten seconds)
EXPLAINER_TTS=silent python tools/build.py music33 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music33 --sync                         # the sound gates
python tools/dead_air.py renders/music33_480p.mp4 --sound music33  # no empty screen; no sound over a still one
python tools/lecture_length.py music33                          # 30 to 60 minutes, listening included
python tools/build.py music33                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 33                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** Compute E(5, 9) and E(4, 11) by Bjorklund's process, and find a tradition that uses one of them.

   *Solution.* E(5,9): x.x.x.x.x (gaps 2, 2, 2, 2, 1); Toussaint lists it as the Arabic rhythm *aqsaq samāʿī* and in other traditions.
   E(4,11): x..x..x..x. (gaps 3, 3, 3, 2); Toussaint notes it in Frank Zappa's use of an eleven-pulse pattern. The lab
   prints both.

2. **Prove.** Prove that a rhythm with the oddity property has at most n/2 strokes in n pulses.

   *Solution.* Pair each pulse i with its opposite i + n/2: there are n/2 such pairs, and an odd rhythm takes at most one
   pulse from each pair. So it has at most n/2 strokes (pigeonhole).

3. **Ear.** The lab plays rhythms of five strokes in twelve pulses; say which are Euclidean.

   *Solution.* The lab prints the answers. The Euclidean ones have gaps of only two sizes, 2 and 3, never two 2s in a
   row more than once; the others contain a run of strokes or a long hole.

4. **Build.** Write a temperament finder for the 7-limit, and find which divisions temper out 225/224.

   *Where to look.* Extend `mathmusic.PRIMES` to (2, 3, 5, 7) and `patent_val` accordingly; 225/224 = [−5, 2, 2, −1⟩.
   Among small divisions, 12 (⟨12 19 28 34]: −60 + 38 + 56 − 34 = 0), 31 and 72 temper it out; check others by the dot
   product, and rank by the worst error on 3/2, 5/4 and 7/4.

5. ★ **Is maximal evenness a cultural choice or a cognitive constraint?**

   *Where the frontier is.* Assemble timelines from many traditions with documented sources; compare their evenness with
   random rhythms of the same size and with rhythms from the same traditions that are not timelines; test whether
   evenness predicts ease of tapping, memory and perceived stability in listeners from several cultures; report effects
   with intervals and the uncertainty in the corpus.

## Sources

* G. Toussaint, "The Euclidean algorithm generates traditional musical rhythms", *BRIDGES* (2005), and *The Geometry of
  Musical Rhythm* (2013; 2nd ed. 2019); E. Bjorklund, "The theory of rep-rate pattern generation in the SNS timing
  system", SNS-NOTE-CNTRL-99 (2003).
* J. Clough and J. Douthett, "Maximally even sets", *Journal of Music Theory* (1991); N. Carey and D. Clampitt, "Aspects
  of well-formed scales", *Music Theory Spectrum* (1989).
* S. Arom, *African Polyphony and Polyrhythm* (1991); M. Chemillier and C. Truchet, "Computation of words satisfying the
  rhythmic oddity property", *Information Processing Letters* (2003).
* D. T. Vuza, "Supplementary sets and regular complementary unending canons", *Perspectives of New Music* (1991–93); E.
  Amiot, *Music Through Fourier Space* (2016); E. M. Coven and A. Meyerowitz, "Tiling the integers with translates of one
  finite set", *Journal of Algebra* (1999); T. Tao, "Fuglede's conjecture is false in 5 and higher dimensions" (2004).
* P. Singh, "The so-called Fibonacci numbers in ancient and medieval India", *Historia Mathematica* (1985); N. G. de
  Bruijn, "A combinatorial problem" (1946).
* F. Stedman, *Campanalogia* (1677); A. T. White, "Fabian Stedman: the first group theorist?", *American Mathematical
  Monthly* (1996).
* P. Erlich, "A middle path between just intonation and the equal temperaments" (2006); D. J. Benson, *Music: A
  Mathematical Offering* (2006).
* M. Mathews, J. R. Pierce, A. Reeves and L. A. Roberts, "Theoretical and experimental explorations of the
  Bohlen–Pierce scale", *JASA* (1988).
* Part 6 for temperaments; Part 11 for rhythm; Part 12 for maximal evenness; Part 29 for homometry.
