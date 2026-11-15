# Music, Built: Part 47, Origins and Universals

Part 47 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the last part of Act VIII, *The Mind*. A flute cut from a vulture's wing bone lay in
Hohle Fels cave for at least 35,000 years. Every society that has been studied makes music, and nobody agrees why. This
part sorts what is shared (a few discrete pitches, a beat, simple rhythms, the lullaby) from what is learned (a taste
for consonance), reveals rhythm priors by tapping back, passes melodies through chains of simulated singers, and draws
the Tune's family tree. The tools are Monochord's (`explainer/music/monochord/origins.py`). Every listener, singer and
dancer in it is simulated, and says so; published findings (Conard, Mehr, Savage, Jacoby and McDermott, Patel,
Pietschnig, Sala and Gobet, Niarchou and others) are quoted, not reproduced, and are listed under Sources.

* **A flute in a cave.** The Hohle Fels flute; a pipe its size (21.8 cm, 8 mm bore) with five evenly spaced holes,
  heard on Part 8's flute model (766 Hz with every hole closed; steps of 364, 202, 229, 264 and 312 cents: even holes,
  uneven steps); the questions; the plan.
* **1. The oldest instruments.** A logarithmic timeline from Divje Babe (disputed) to Geißenklösterle, Hohle Fels,
  Jiahu, Ur and Ugarit; what a pipe's length says (766 Hz for the fragment, 496 Hz for one estimate of the whole); what the
  bones say; older than any flute.
* **2. Every society sings.** Mehr's Natural History of Song (315 societies); an ear question (one melody sung as a
  dance song and as a lullaby: which is which?), with the features that tell them apart; form follows function (listeners
  in 60 countries; infants relaxing to foreign lullabies); what song is for.
* **3. Statistical universals.** Savage's 304 recordings; six of his features checked on the series' 54 tunes (at most
  seven pitch classes 96 per cent, small intervals 100, falling or arched phrases 65, two lengths covering three notes in
  four 81, a beat 100, recurring motifs 91); what such a check cannot show; features that travel together.
* **4. What is learned.** The Tsimane's indifference to dissonance; four chords of the kind they rated, heard; the
  gradient with exposure; is the octave universal?; infants born open and tuned by exposure.
* **5. Priors revealed by iteration.** Jacoby and McDermott's method; an ear question (a random rhythm and what it
  became after five rounds: 2.8 : 1 : 1.3 became 1.8 : 1 : 1.9, near 2 : 1 : 2); 400 chains in the rhythm triangle, gathering
  on small-integer ratios (28 per cent near one at the start, 71 after three rounds); two listeners, two priors (a 4/4
  listener's chains end on 1:1:2 51 per cent of the time against a prior of 51; a 7/8 listener's on 2:2:3); Griffiths
  and Kalish's theorem; 39 groups in 15 countries.
* **6. A tune in simulated mouths.** One simulated singer; a random melody after 0, 1, 5, 10, 20 and 40 singers; an ear
  question (which end of the chain could you sing back?); twenty chains measured (pitch levels 11.7 → 5.6, average step
  5.6 → 2.7 semitones, simple lengths 47 → 97 per cent, copying error 0.31 → 0.08 a note); two kinds of learner (the Tune
  after thirty likeliest-value singers 0.25 a note from the original, after thirty samplers 0.38); cultural evolution in
  the lab (Kirby; Ravignani).
* **7. Tune families.** Bayard; the Tune, the Alphabet Song and Baa, Baa, Black Sheep, heard; aligning melodies as genes
  (Needleman–Wunsch: the Tune's first two phrases against Baa, Baa's cost 3.0, two halved lengths and two gaps); eleven
  tunes clustered (the Tune's family a branch of its own: the Alphabet Song 0.15 a note away, Baa, Baa 0.29, every other
  tune at least 0.60); a simulated family rebuilt exactly, and 4.8 of 6 branchings on average over twenty families, against
  0.5 for a random tree; Savage's 10,062 folk melodies.
* **8. Birds, whales and a cockatoo.** Zebra finch isolates' song restored in three or four tutored generations; humpback
  song revolutions; Snowball; an ear question (two simulated dancers: which is on the beat?); Rayleigh's test (R 0.95 and
  p below 10⁻¹³, against R 0.15 and p 0.57); vocal learning and beat-keeping, and a sea lion.
* **9. Music and language.** Two sound systems; the nPVI (an even rhythm 0, two short and a long 40, long-short at three
  to one 100); the two ends of the corpus, heard (Sur le pont d'Avignon 21, Clementine 74); Grabe and Low, Patel and
  Daniele; the series' folk tunes by language (French 24.7, English 35.8, German 39.1; English minus French 11.1, bootstrap
  interval 3.4 to 19.0, permutation p = 0.16: with five French tunes, we cannot tell); the Library by kind (songs 47.9,
  keyboard 29.2: what a piece is for moves the number more than the composer's language); song against speech (Ozaki).
* **10. Amusia, Mozart and transfer.** Congenital amusia (about 1.5 per cent); an ear question in the Montreal battery's
  style (which pair differed?); the Mozart effect and its meta-analysis; 300 simulated studies of a zero effect, of which
  the 46 published average 0.14; music lessons and transfer (Schellenberg; Mehr; Sala and Gobet); music as treatment.
* **11. Why music?** Darwin, Spencer and Mithen; Pinker's cheesecake; bonding and credible signalling; what each theory
  predicts; what our chains add.
* **12. Frontier: data at the scale of the species.** The Global Jukebox, the Natural History of Song, many-site studies
  and Registered Reports; the genetics of beat synchronization (69 loci, 13–16 per cent); open questions; ★ research
  problem: which universals need which biases, and are those biases universal?
* **Variation 47, recap and problems.** The Tune as written, after fifteen singers and after thirty; the ledger (42 notes
  in, 41 out, 29 kept exactly, 0.28 a note); what we found; five problems; where it comes back; in practice; references;
  Part 48.

## What is computed, and what is heard

`python -m videos.music.music47.compute` (about a minute) fills `.cache/music47/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook` | a five-hole pipe's notes; open-pipe fundamentals | rising notes, uneven steps (tests) |
| `lullaby`, `chords` | one melody as dance song and lullaby; four chords | — |
| `universals` | six statistical universals on the corpus | the shares (tests) |
| `rhythm` | iterated reproduction by two simulated listeners | chains end in each prior's mode (tests) |
| `chains`, `sampling`, `tune47` | transmission chains; samplers against likeliest-value singers; Variation 47 | structure appears, error falls (tests) |
| `family`, `relatives` | alignment, UPGMA, Robinson–Foulds against a known tree | better than random (tests) |
| `npvi`, `rhythms` | nPVI of the corpus by language and of the Library by kind | bootstrap and permutation (tests) |
| `beat`, `amusia`, `mozart` | Rayleigh's test; a Montreal-style pair; publication bias | the p-values; inflation (tests) |

Monochord's tools are held in `tests/music/test_origins.py` (including alignment against hand-built cases and the
chains finding their prior); this part's claims and clips in `tests/music/test_music47.py`.

**Sounds.** Part 8's flute model and voice, Part 7's piano, Part 40's drums, a struck-wood tap. There are no
recordings: the songs of Mehr's and Savage's collections, the whale recordings and Snowball's video are described, not
played.

**What the models are, and are not.** *The pipe* has holes we placed; the Hohle Fels flute's tuning is not known.
*The rhythm listeners* are Bayesian observers with priors we chose (a 4/4 listener and a 7/8 listener); they illustrate
the method and the theorem, not any culture's measured prior. *The singers* are a deliberately simple model of
transmission: blurred hearing, pitch categories, a pull toward simple lengths, a cost on wide leaps, and slips that fall
on whatever is new; real singers protect strong beats and final notes (Savage 2022), which ours do not. *The dancers*
are simulated head-bobs. *The consonance gradient* in chapter 4 sketches McDermott's ordering, not his measured sizes.
*The nPVI comparison* uses tunes grouped by country, written out from memory, with five French tunes: it is a lesson
in what a small sample cannot show.

## Build

```bash
python -m videos.music.music47.compute                          # numbers and sounds (about a minute)
EXPLAINER_TTS=silent python tools/build.py music47 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music47 --sync                         # the sound gates
python tools/dead_air.py renders/music47_480p.mp4 --sound music47  # no empty screen; no sound over a still one
python tools/lecture_length.py music47                          # 30 to 60 minutes, listening included
python tools/build.py music47                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 47                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** Compute the nPVI of the durations 1, 1, 2, 1, 1, 2. What does doubling every duration do to it?

   *Solution.* The five neighbouring pairs give |1−1|/1 = 0, |1−2|/1.5 = 2/3, 2/3, 0, 2/3; their mean is 2/5, so the nPVI
   is 40. Doubling every duration doubles each difference and each average, so nothing changes: the index depends only on
   ratios, which is why it can compare a slow tune with a fast one.

2. **Prove.** Prove that a chain of learners who sample their posterior has the prior as a stationary distribution.

   *Solution.* Let a learner's hypothesis θ be drawn from the prior p(θ), let it produce data d ~ p(d | θ), and let the
   next learner draw θ′ ~ p(θ′ | d). Then the distribution of θ′ is ∫∫ p(θ′ | d) p(d | θ) p(θ) dθ dd = ∫ p(θ′ | d) p(d) dd =
   p(θ′), by Bayes's rule. So the prior is stationary; if the chain is irreducible and aperiodic it converges to it from
   any start (Griffiths and Kalish 2007). Learners who take the most probable hypothesis instead do not have this property,
   and preserve what they hear far longer, as chapter 6's two kinds of singer show.

3. **Ear.** The lab plays rhythms before and after five tap-backs; say which is which.

   *Solution.* The lab prints them. A chain's end lies near a ratio of small integers, so it sounds like a pattern you
   could clap (long, short, long; or short, short, long); a random start sounds lopsided and keeps slipping.

4. **Build.** Switch off the singer's categories and run the chains: which universals still appear?

   *Where to look.* `transmit(mel, rng, {"category": 0.0})` keeps every heard pitch; set `novel` to 0 to make memory
   indifferent to novelty, or `leap_cost` to 0. Measure `structure` after forty singers for twenty chains each way: lengths
   still settle on simple ratios (the timing prior does that), while pitch levels merge less: in twenty chains, about
   7.6 levels remain instead of 5.5, and what merging is left comes from memory refilling lost notes with familiar ones.

5. ★ **Which universals need which biases, and are the biases themselves universal?**

   *Where the frontier is.* Switch biases off one at a time in simulated chains to see which universals each produces;
   then estimate the biases from real transmission chains, in the lab across many cultures (as Jacoby's rhythm studies
   do) and from tune families (as Savage's alignments do), and ask whether they vary as the music does.

## Sources

* N. J. Conard, M. Malina and S. C. Münzel, "New flutes document the earliest musical tradition in southwestern
  Germany", *Nature* (2009); T. Higham and others, *Journal of Human Evolution* (2012), on Geißenklösterle; J. Zhang and
  others, "Oldest playable musical instruments found at Jiahu early Neolithic site in China", *Nature* (1999).
* S. A. Mehr and others, "Universality and diversity in human song", *Science* (2019); S. A. Mehr and others, "Form and
  function in human song", *Current Biology* (2018); C. M. Bainbridge and others, "Infants relax in response to
  unfamiliar foreign lullabies", *Nature Human Behaviour* (2021).
* P. E. Savage, S. Brown, E. Sakai and T. E. Currie, "Statistical universals reveal the structures and functions of
  human music", *PNAS* (2015); P. E. Savage and others, "Sequence alignment of folk song melodies reveals cross-cultural
  regularities of musical evolution", *Current Biology* (2022); S. P. Bayard, "Prolegomena to a study of the principal
  melodic families of British-American folk song", *Journal of American Folklore* (1950).
* J. H. McDermott, A. F. Schultz, E. A. Undurraga and R. A. Godoy, "Indifference to dissonance in native Amazonians
  reveals cultural variation in music perception", *Nature* (2016); N. Jacoby and others, *Current Biology* (2019), on
  octaves; M. P. Lynch and others, *Psychological Science* (1990); E. E. Hannon and S. E. Trehub, *Psychological
  Science* and *PNAS* (2005).
* N. Jacoby and J. H. McDermott, "Integer ratio priors on musical rhythm revealed cross-culturally by iterated
  reproduction", *Current Biology* (2017); N. Jacoby and others, *Nature Human Behaviour* (2024); T. L. Griffiths and
  M. L. Kalish, "Language evolution by iterated learning with Bayesian agents", *Cognitive Science* (2007).
* S. Kirby, H. Cornish and K. Smith, *PNAS* (2008); A. Ravignani, T. Delgado and S. Kirby, "Musical evolution in the lab
  exhibits rhythmic universals", *Nature Human Behaviour* (2016); O. Fehér and others, "De novo establishment of
  wild-type song culture in the zebra finch", *Nature* (2009).
* R. S. Payne and S. McVay, "Songs of humpback whales", *Science* (1971); M. J. Noad and others, "Cultural revolution in
  whale songs", *Nature* (2000); A. D. Patel, J. R. Iversen, M. R. Bregman and I. Schulz, "Experimental evidence for
  synchronization to a musical beat in a nonhuman animal", *Current Biology* (2009); A. D. Patel, *Music Perception*
  (2006); P. Cook and others, *Journal of Comparative Psychology* (2013).
* A. D. Patel, *Music, Language, and the Brain* (2008); E. Grabe and E. L. Low (2002); A. D. Patel and J. R. Daniele,
  "An empirical comparison of rhythm in language and music", *Cognition* (2003); Y. Ozaki and others, "Globally, songs
  and instrumental melodies are slower and higher and use more stable pitches than speech", *Science Advances* (2024).
* I. Peretz and D. T. Vuvan, "Prevalence of congenital amusia", *European Journal of Human Genetics* (2017); F. H.
  Rauscher, G. L. Shaw and K. N. Ky, *Nature* (1993); J. Pietschnig, M. Voracek and A. K. Formann, "Mozart effect–Shmozart
  effect: a meta-analysis", *Intelligence* (2010); W. F. Thompson, E. G. Schellenberg and G. Husain, *Psychological
  Science* (2001).
* E. G. Schellenberg, *Psychological Science* (2004); S. A. Mehr and others, *PLoS ONE* (2013); G. Sala and F. Gobet,
  *Memory & Cognition* (2020); J. Hole and others, *The Lancet* (2015); the Cochrane review of music therapy for
  depression (2017); Ł. Bieleninik and others, *JAMA* (2017).
* C. Darwin, *The Descent of Man* (1871); H. Spencer, "The origin and function of music" (1857); S. Mithen, *The Singing
  Neanderthals* (2005); S. Pinker, *How the Mind Works* (1997); P. E. Savage and others, "Music as a coevolved system for
  social bonding", and S. A. Mehr, M. M. Krasnow, G. A. Bryant and E. H. Hagen, "Origins of music in credible
  signaling", *Behavioral and Brain Sciences* (2021); H. Honing (ed.), *The Origins of Musicality* (2018).
* A. L. C. Wood and others, "The Global Jukebox", *PLOS ONE* (2022); M. Niarchou and others, "Genome-wide association
  study of musical beat synchronization demonstrates high polygenicity", *Nature Human Behaviour* (2022); B. Nettl, *The
  Study of Ethnomusicology* (3rd ed., 2015).
