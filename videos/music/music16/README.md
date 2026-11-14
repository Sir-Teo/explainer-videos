# Music, Built: Part 16, Two Voices

Part 16 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), and the first part of Act III, where music has more than one voice at a time. It
starts from a paradox: parallel fifths were the method of the first written polyphony and are the most famous
prohibition in harmony teaching. It explains both from hearing (tonal fusion, moving together, starting together),
then takes Fux's *Gradus ad Parnassum* (1725) as an engineering problem: it counts every first-species line over
Fux's cantus firmus exactly, removes the rules one at a time and measures what breaks, works through the five
species, and measures how independent two voices are, from organum to florid counterpoint. The counterpoint module
is Monochord's (`explainer/music/monochord/counterpoint.py`), and every sound is computed in `compute.py`.
Published findings are the ones listed under Sources.

* **A forbidden rule that was once the rule.** "Never write parallel fifths"; the Tune with a second voice a fifth
  below it all the way through, and then with a counterpoint above it that obeys Fux's rules (contrary motion at
  54 moves in a hundred, no fused moments): one melody made thicker, and two people each going somewhere; Huron
  (2001): the rules are instructions for keeping two voices audible as two; the plan.
* **1. One voice, made thicker.** The *Musica enchiriadis* (about 900): principal and organal voices, simple and
  composite organum, heard on the Tune's first phrase; three stages heard on the whole Tune and measured:
  parallel organum at the fifth (fused at every move), organum at the fourth with a boundary note, as in the
  handbook and Guido (fused at 57 moves in a hundred, the rest oblique), and free organum of about 1100, chosen by
  dynamic programming to move against the chant (never fused, contrary at 64 in a hundred); the timeline to
  1500.
* **2. When two notes become one.** Stumpf's tonal fusion (1890); the share of the upper note's harmonics that
  are also harmonics of the lower (1/q for a just ratio p:q): octave 1, fifth 1/2, fourth and major sixth 1/3,
  major third 1/4, minor second 1/15; an ear question (a phrase doubled at the octave and at the third).
* **3. Moving together.** The four motions, heard; the law of common fate and Bregman (1990): pitch
  co-modulation; in the 152 good first-species lines contrary motion is 47 moves in a hundred, against 35 in
  lines that are merely consonant.
* **4. Starting together.** An ear question (an octave, the upper note 35 ms late); how late a note must be,
  heard (0, 10, 20, 35 and 60 ms); Hirsh (1959): about 20 ms to tell which of two sounds came first; Rasch
  (1978, 1979): asynchrony helps listeners pick out simultaneous notes, and ensembles play "together" 30 to 50 ms
  apart; notes beginning together, by species: 100, 52, 27 and 5 in a hundred; Huron (1993, 2008) on Bach.
* **5. Fux's exercise.** The *Gradus* (1725) and its readers; the Dorian cantus D F E D G F A G F E D; twelve
  rules as modern textbooks state Fux, each beside the perceptual principle it protects; the line Monochord's
  search liked best, heard: nine of ten moves contrary, octave to octave through C♯ (musica ficta); the exercise
  turned over: a line below the cantus, heard, the octave or unison as first note, the leading note now a third
  below; 42 good lines below against 152 above, and 302 below if any first note is allowed.
* **6. How many good lines?** 4,628,074,479,616 note sequences; the rules added one at a time (consonance leaves
  one in 431; the beginning and the cadence; the rules of melody; direct motion; one highest note): 152 good
  lines, one in thirty billion; counting by hand: a five-note cantus (D F G E D) with the eight rules that look
  one note back, counted backward column by column (4 + 4 + 6 = 14) and a line drawn uniformly from the same
  table; the redundant rule: without the rule against parallel fifths and octaves, still 152, because no perfect
  consonance may be reached by similar motion at all (without that rule instead: 410); over the whole Tune as a
  cantus: 23,921,887,999 good lines, 38,000 years to play.
* **7. Remove a rule.** Each rule removed, 300 lines drawn uniformly from those that obey the rest, and the damage
  measured: without consonance 184 times as many lines and 37 notes in a hundred clashing; without the rule on
  direct motion 9 moves in a hundred fused; without the melodic rules leaps over a fifth rise from 3 to 11 in a
  hundred; without recovery 15 times as many lines; an ear question (two lines, each breaking one rule: which
  clashes?).
* **8. Two notes against one.** Second species: the weak beat may carry a passing dissonance (D over A between C
  and E); a line over Fux's cantus with its four passing dissonances, on the staff and heard.
* **9. Four notes against one.** Third species: passing and neighbouring notes, a skip between consonances; a line
  with thirteen dissonances, every one reached and left by step, heard.
* **10. Held over.** Fourth species: preparation, suspension, resolution (a seven falling to a six); an ear
  question (the same five notes over a falling cantus, moving with it in parallel sixths and held over as a chain
  of 7–6 suspensions); a fourth-species line, heard: one note in twenty begins with the cantus.
* **11. Florid, and independent.** Fifth species, heard; one table for every texture: notes beginning together,
  fused moments, contrary and parallel motion, from organum (100, 100, 0, 100) through the species; Huron's six
  principles (toneness, minimum masking, tonal fusion, pitch proximity, pitch co-modulation, onset synchrony) and
  the rules that follow from them.
* **12. Frontier: counterpoint by machine.** Schottstaedt's species program (1984, rules as penalties, up to six
  voices); Ebcioğlu's chorales (1988, about 350 rules); constraint solvers and neural networks; corpus tests of
  the perceptual account (the shuffle method of Part 14). ★ research problem: what makes one good line better than
  another.
* **Variation 16, recap and problems.** The Tune as a cantus firmus, a bar to each note: its first phrase in
  organum a fifth below, then a voice above it in each of the five species (one search, so the line runs on); the
  ledger (notes beginning together: 100% in organum, 0% in fourth species); what we found; five problems; where
  it comes back; in practice; references; Part 17.

## What is computed, and what is heard

`python -m videos.music.music16.compute` (about a minute) fills `.cache/music16/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook` | the Tune with a fifth below it; the best first-species line above it; independence of both | the line breaks no rule (`check`) |
| `organum` | simple and composite organum on the Tune's first phrase | — |
| `fusion` | 1/q for each interval's just ratio; the ear question | Part 4's ratios |
| `motions` | the four motions; their shares in good lines and in merely consonant lines | — |
| `onsets` | the octave, together and 35 ms apart; onsets in common by species | — |
| `fux` | the cantus, the best line by Fux's preferences, its intervals and motions; the rules | `check` finds no violation |
| `counting` | the funnel of exact counts; the count over the whole Tune | exhaustive listing on small cantus (tests) |
| `damage` | the count and 300 uniform samples with each rule removed; two broken lines | — |
| `species` | species two to five over Fux's cantus by randomized search; their dissonances and suspensions | every dissonance placed by the species' rules (tests) |
| `independence` | the independence table: organum and the five species | — |
| `tune` | Variation 16 | onsets in common: 100% (organum), 0% (fourth species) |
| `more` | organum's three stages; the five-note count by hand; the line below; the delay ladder; the suspension question | the hand count equals `count` and the list of lines |

Monochord's counterpoint is held against brute force in `tests/music/test_counterpoint.py`; this part's claims and
clips in `tests/music/test_music16.py`.

**Sounds.** Twenty clips: the counterpoint on Part 7's piano (`physical model`), organum, the fusion and onset
questions on organ tones (`synthesized`), all in twelve-tone equal temperament. There are no recordings.

**What the models are, and are not.** *The twelve rules* are Fux's first species as modern textbooks state it
(Mann's translation, Jeppesen, Salzer and Schachter), made exact: consonances are octaves, fifths, thirds and
sixths; "awkward leaps" are tritones, sevenths and leaps over an octave (a rising minor sixth is allowed); "too
many parallel thirds" is more than three in a row; the compass is a tenth. Fux states some of these as advice,
not law, and other choices give other counts; the counts are exact *for these rules*. *Fux's preferences*
(contrary motion, imperfect consonances, steps, a climax in the middle) are Monochord's score, a crude stand-in
for a teacher, which is the chapter-12 research problem. *The species lines* are found by randomized depth-first
search with a score; they obey the species' rules for dissonance but are not checked against every first-species
rule (the compass and leaps are, the climax is not), and a teacher would correct some of them. *Fusion strength*
1/q is the share of shared harmonics of an idealized harmonic tone, a proxy for Stumpf's judgements, not a
measurement. *Independence* counts, at every moment a note begins, the motion since the last such moment and
whether the voices move together onto an octave, fifth or fourth; Huron's corpus measures are more refined. The
free organum of chapter 1 is chosen by a scoring rule of ours, in the style of the treatises, not transcribed
from one. The delay ladder's thresholds are what most listeners report, not a measurement of ours.

## Build

```bash
python -m videos.music.music16.compute                          # numbers and sounds (about a minute)
EXPLAINER_TTS=silent python tools/build.py music16 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music16 --sync                         # the sound gates
python tools/dead_air.py renders/music16_480p.mp4 --sound music16  # no empty screen; no sound over a still one
python tools/lecture_length.py music16                          # 30 to 60 minutes, listening included
python tools/build.py music16                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 16                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** Against the cantus C D F E D C, write every first-species line above it that begins and ends on
   the C an octave above, obeying the twelve rules, and say which you prefer and why.

   *Solution.* There are seven good lines in all (`counterpoint.count([60, 62, 65, 64, 62, 60])`), and three
   begin and end on C5: C A D C B C, C B D C B C and C B D E B C. Each falls to B over D at the cadence (a major
   sixth opening to the octave). The third is the best by Fux's preferences (score 12.4 against 10.9 and 11.5):
   it reaches its single highest note, E, by contrary motion onto an octave in the middle of the line, and has
   three contrary moves of five; the first moves in similar motion three times in a row, and the second has a
   pair of parallel sixths and a repeated shape (C B … C B).

2. **Prove.** Show that if no perfect consonance may be reached by similar motion, then no parallel fifths or
   octaves can occur. Is the converse true?

   *Solution.* Parallel motion is the special case of similar motion in which the interval stays the same. Two
   successive fifths (or octaves) in which both voices move are reached by motion in the same direction, so they
   are a perfect consonance reached by similar motion, which the stronger rule forbids. (Two fifths with neither
   voice moving are a repeated note, forbidden separately.) The converse is false: the weaker rule allows a
   perfect consonance reached by similar motion from a *different* interval, a third or a sixth moving to a fifth
   or an octave with both voices rising or falling: the "hidden" or "direct" fifths and octaves. Over Fux's
   cantus this difference is the whole of the gap between 410 lines and 152, and the parallel-fifths rule adds
   nothing once the direct-motion rule is in force.

3. **Ear.** The lab plays eight pairs of two-voice chords. For each, say whether the voices move in parallel,
   similar, contrary or oblique motion.

   *Solution.* The lab prints the answers. Listen to each voice in turn. If one voice stays put, oblique. If they
   go opposite ways, contrary. If both go the same way, listen to the interval: unchanged (here a step each) is
   parallel, opening or closing (a fourth against a step) is similar.

4. **Build.** With `counterpoint.count`, remove each rule in turn, above Fux's cantus and below it. Which rules
   bind harder below, and why?

   *Solution.* Above, 152 lines; below, 42. Removing each rule multiplies the count by (above, below):
   consonance 184, 408; start 2.7, 7.2; cadence 10, 9.0; unison 2.2, 2.0; parallel 1, 1; direct 2.7, 2.0;
   melodic 3.2, 6.7; repeat 4.4, 5.2; recovery 15, 19; run 1, 1; spacing 1.8, 2.7; climax 1.5, 1.8. The rule on
   the first note binds almost three times harder below: above, the line may begin on the octave or the fifth;
   below it must begin on the octave or unison, because a fifth below D is G, and a bass on G names G as home.
   The melodic rules also bind harder (6.7 times against 3.2), but differently: the lines they remove below
   leap mostly by major sixths, major sevenths and minor ninths; above, mostly by tritones and falling minor
   sixths. Why a line below the cantus is drawn to those leaps is a good extension.

5. ★ **Which good line is best?** Of the 152 good lines over Fux's cantus, which would a teacher grade highest?
   Propose a score, and a way to check it against human judgements.

   *Where the frontier is.* Rules of avoidance are well understood; rules of preference are not. Candidate
   scores combine shape (a single climax in the middle third, a balance of rising and falling, steps
   outweighing leaps), variety (imperfect consonances, few repeated intervals or motions) and direction (motion
   toward the cadence), with weights. Schottstaedt (1984) turned Fux's preferences into penalties by hand;
   Farbood and Schoner (2001) learned them from examples with a Markov model; Komosinski and Szachewicz (2015)
   and others search with several objectives at once. The check is the hard part: collect blind rankings of a
   sample of the 152 lines from several counterpoint teachers, measure how far teachers agree with one another
   (if they do not, there is nothing to fit), fit the weights on half the lines and test the ranking on the
   rest. As far as we know no such data set of expert rankings exists for species counterpoint.

## Sources

Books: J. J. Fux, *Gradus ad Parnassum* (1725), trans. A. Mann, *The Study of Counterpoint* (1965); K. Jeppesen,
*Counterpoint: The Polyphonic Vocal Style of the Sixteenth Century* (1931, trans. 1939); F. Salzer and C.
Schachter, *Counterpoint in Composition* (1969); A. S. Bregman, *Auditory Scene Analysis* (1990); C. Stumpf,
*Tonpsychologie*, vol. 2 (1890); R. Crocker, "Discant, counterpoint and harmony", *JAMS* 15 (1962); S. Fuller,
"Early polyphony", in *The New Oxford History of Music*, vol. 2 (1990); the *Musica enchiriadis* and *Scolica
enchiriadis*, trans. R. Erickson (1995); Guido of Arezzo, *Micrologus* (about 1026), trans. W. Babb in *Hucbald,
Guido, and John on Music* (1978).

Papers: D. Huron, "Tone and voice: a derivation of the rules of voice-leading from perceptual principles", *Music
Perception* 19 (2001); D. Huron, "Voice denumerability in polyphonic music of homogeneous timbres", *Music
Perception* 6 (1989), and "Asynchronous preparation of tonally fused intervals in polyphonic music", *Empirical
Musicology Review* 3 (2008); D. Huron and P. Sellmer, "Critical bands and the spelling of vertical sonorities",
*Music Perception* 10 (1992); I. J. Hirsh, "Auditory perception of temporal order", *JASA* 31 (1959); R. A.
Rasch, "The perception of simultaneous notes such as in polyphonic music", *Acustica* 40 (1978), and
"Synchronization in performed ensemble music", *Acustica* 43 (1979); B. Schottstaedt, *Automatic Species
Counterpoint*, CCRMA report STAN-M-19 (1984); K. Ebcioğlu, "An expert system for harmonizing four-part chorales",
*Computer Music Journal* 12 (1988); M. Farbood and B. Schoner, "Analysis and synthesis of Palestrina-style
counterpoint using Markov chains", *Proceedings of the ICMC* (2001); M. Komosinski and P. Szachewicz, "Automatic
species counterpoint composition by means of the dominance relation", *Journal of Mathematics and Music* 9
(2015).
