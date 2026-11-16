# Music, Built: Part 43, Performing

Part 43 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the third part of Act VII, *The Craft*. In 2007 a critic put a celebrated pianist's CD
into a computer and the track database named another pianist: over a hundred recordings released under Joyce Hatto's
name were other people's, and timing analysis showed it, using detailed timing and corroborating audio evidence. This part asks what a
performer adds to the notes and measures it in milliseconds: rules of expression and the kinematics of slowing down,
loudness and articulation, vibrato and intonation, ensembles that stay together by correcting each other, the timing
fingerprint, and what practice, anxiety and the body have to do with it. The tools are Monochord's
(`explainer/music/monochord/perform.py`). Every performance heard is a model's; the pianists are model pianists; no
recording of a real performer is played, and the Hatto case is described, not heard. Published findings are the ones
listed under Sources.

* **Who is playing?** An ear question (three recordings: which two are one?); the Hatto affair; the plan.
* **1. What a performer adds.** Seashore's "deviation from the exact"; the Tune's first two phrases written and
  performed, heard; the difference drawn (phrase-final notes up to 26% longer; loudness arched); what a performer
  controls; Repp's 28 *Träumerei* recordings.
* **2. Rules of expression.** The KTH rule system; each of five rules alone, heard; how rules combine; all five at
  strengths 0, 1 and 2, heard; what rules can and cannot do.
* **3. Slowing down.** Runners and ritardandi (Friberg and Sundberg); the formula v(x) = [1 + (w^q − 1)x]^(1/q); three
  ritardandi, heard; phrase-final lengthening in speech; Todd's music as motion.
* **4. Loudness and articulation.** Loudness across the whole Tune; legato, as written and staccato, heard; legato
  measured (Repp); touch.
* **5. Vibrato and intonation.** An ear question (a 60-cent vibrato: higher, lower or the same?); rates of 3, 6 and 10
  Hz, heard; vibrato in practice; intonation in practice.
* **6. Playing together.** Linear phase correction (Vorberg and Wing); an ear question (three duos: which has nobody
  listening?), with the asynchronies drawn (264 ms behind after 24 beats with no correction; an over-correcting duo
  shaking apart); the spread against the total correction, exact and simulated (stable only between 0 and 2; best near
  0.85); the negative mean asynchrony; what the model says.
* **7. Quartets and conductors.** Wing and colleagues' two quartets; a democratic and an autocratic model quartet (spreads
  31 and 31 ms), drawn and heard; the conductor; other ways to stay together.
* **8. Who is playing?** A timing fingerprint; three tempo curves; the Hatto test on ten model pianists (the copy 0.9999,
  the pianist's own second take 0.988, others at most 0.90); performance history; caveats.
* **9. Practice and the performer's body.** Deliberate practice (Ericsson and colleagues); what practice explains (about
  21% in music, Macnamara and colleagues); how to practise; memory and anxiety; injury, dystonia and hearing.
* **10. Frontier: learning to perform.** Performance as data (MAESTRO, ASAP); learned models of expression; machines
  that play along; ★ research problem: is an interpretation a measurable object?
* **Variation 43, recap and problems.** The Tune as written (28.8 s) and as performed (32.0 s), the differences drawn;
  the ledger; what we found; five problems; where it comes back; in practice; references; Part 44.

## What is computed, and what is heard

`python -m videos.music.music43.compute` (under a minute) fills `.cache/music43/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook`, `identity` | model pianists' recordings; tempo curves; the copy test | a stretched copy correlates above 0.999 (tests) |
| `written`, `rules`, `strength` | the Tune written and performed; each rule; three strengths | phrase starts slower than middles (tests) |
| `ritard` | three kinematic ritardandi | v² linear for q = 2 (tests) |
| `artic` | legato, written, staccato | — |
| `vibrato`, `rates` | a vibrato tone's mean pitch; three rates | the spectral centroid at 440 Hz (tests) |
| `duo`, `duo_curve` | three duos; the spread against the correction | the closed form against 20,000 simulated beats (tests) |
| `quartet` | two model quartets, simulated and heard | equal spreads (tests) |
| `tune`, `variation` | Variation 43 | the ledger (tests) |

Monochord's tools are held in `tests/music/test_perform.py`; this part's claims and clips in `tests/music/test_music43.py`.

**Sounds.** Part 7's piano (a struck string on a soundboard) with Part 38's plucked bass, physical models; the vibrato
tones are additive, from Part 41's bowed-string spectrum (labelled `synthesized`). There are no recordings.

**What the models are, and are not.** *The rules* are five of the KTH system's, simplified, with our own constants.
*The model pianists* differ by rule weights, tempo and a personal timing habit; real pianists differ in far more.
*The ensembles* follow linear phase correction with our noise levels; the quartet matrices are ours, in the spirit of
Wing and colleagues', not their estimates. *Practice, anxiety and health* findings are quoted from the cited studies.

## Build

```bash
python -m videos.music.music43.compute                          # numbers and sounds (under a minute)
EXPLAINER_TTS=silent python tools/build.py music43 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music43 --sync                         # the sound gates
python tools/dead_air.py renders/music43_480p.mp4 --sound music43  # no empty screen; no sound over a still one
python tools/lecture_length.py music43                          # 30 to 60 minutes, listening included
python tools/build.py music43                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 43                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** A ritardando falls to half tempo with q = 2. At what point of it is the tempo 0.8?

   *Solution.* v² = 1 + (w² − 1)x = 1 − 0.75x. Setting v = 0.8 gives 0.64 = 1 − 0.75x, so x = 0.48: just before
   halfway, the tempo has lost only a fifth; the rest of the slowing comes late.

2. **Prove.** Prove that a duo's asynchrony has variance 2σ_T²/(1 − b²) + 4σ_M²/(1 + b), with b = 1 − α₁ − α₂.

   *Solution.* Subtracting the two players' updates gives A_{k+1} = b A_k + (T₂ − T₁) + (M₂,ₖ₊₁ − M₂,ₖ) − (M₁,ₖ₊₁ − M₁,ₖ).
   The timekeeper part is white with variance 2σ_T², so it contributes 2σ_T²/(1 − b²). The motor part is u_{k+1} − u_k
   with u = M₂ − M₁ of variance 2σ_M²: an ARMA(1, 1) with θ = 1, whose variance is 2σ_M²(1 + 1 − 2b)/(1 − b²) =
   4σ_M²/(1 + b). The two parts are independent, so the variances add. Both are finite only for |b| < 1, that is
   0 < α₁ + α₂ < 2.

3. **Ear.** The lab plays duos with random corrections; say which drift, which hold, which shake.

   *Solution.* The lab prints them. A drifting duo's two notes separate steadily into a flam and then an echo; a holding
   duo stays a single sound with a slight smear; a shaking duo alternates which player is ahead, more each beat.

4. **Build.** Write a rule of your own (for example "faster uphill") and hear it on the Tune.

   *Where to look.* A rule in `perform.py` is a function of the score and phrases returning per-note `stretch` and `vel`;
   add it to `RULES` and to `WEIGHTS` in the lab. "Faster uphill" shortens notes that rise from the previous one by a
   few per cent.

5. ★ **Is an interpretation a measurable object?**

   *Where the frontier is.* Align many recordings of one piece to the score; model each tempo curve as the structure's
   prediction plus a residual; ask blind listeners which recordings share an interpretation; test whether residuals
   cluster as listeners do, and whether a model conditioned on a cluster can reproduce it.

## Sources

* C. E. Seashore, *Psychology of Music* (1938); A. Gabrielsson, "Music performance research at the millennium",
  *Psychology of Music* (2003).
* A. Friberg, R. Bresin and J. Sundberg, "Overview of the KTH rule system for musical performance", *Advances in
  Cognitive Psychology* (2006); A. Friberg and J. Sundberg, "Does music performance allude to locomotion? A model of final
  ritardandi derived from measurements of stopping runners", *JASA* (1999); N. P. M. Todd, "The dynamics of dynamics",
  *JASA* (1992); G. Widmer, "Machine discoveries: a few simple, robust local expression principles", *JNMR* (2002).
* B. H. Repp, "Diversity and commonality in music performance: an analysis of timing microstructure in Schumann's
  *Träumerei*", *JASA* (1992); B. H. Repp, "Acoustics, perception, and production of legato articulation on a
  computer-controlled grand piano", *JASA* (1997); B. H. Repp, "Sensorimotor synchronization: a review of the tapping
  literature" (2005) and B. H. Repp and Y.-H. Su (2013).
* E. Shonle and K. E. Horan, "The pitch of vibrato tones", *JASA* (1980).
* D. Vorberg and A. M. Wing, "Modeling variability and dependence in timing" (1996); A. M. Wing, S. Endo, A. Bradbury and
  D. Vorberg, "Optimal feedback correction in string quartet synchronization", *J. R. Soc. Interface* (2014);
  C. Chafe, J.-P. Cáceres and M. Gurevich, "Effect of temporal separation on synchronization in rhythmic performance",
  *Perception* (2010).
* N. Cook, *Beyond the Score* (2013); C. S. Sapp and N. Cook on the Hatto recordings (CHARM, 2007); R. Philip, *Early
  Recordings and Musical Style* (1992).
* K. A. Ericsson, R. T. Krampe and C. Tesch-Römer, "The role of deliberate practice in the acquisition of expert
  performance", *Psychological Review* (1993); B. N. Macnamara, D. Z. Hambrick and F. L. Oswald, "Deliberate practice and
  performance in music, games, sports, education, and professions: a meta-analysis", *Psychological Science* (2014).
* C. Hawthorne and others, "Enabling factorized piano music modeling and generation with the MAESTRO dataset" (2019);
  D. Jeong and others, "VirtuosoNet" (2019); R. B. Dannenberg, "An on-line algorithm for real-time accompaniment"
  (1984); C. Raphael, *Music Plus One*.

## Interpretation limits

All heard pianists are synthetic models; the Hatto recordings are not played. Identification uses standardized log inter-onset intervals and uniform time scaling; no universal correlation threshold proves copying. Piano controls include pedals and instrument mechanics beyond three note parameters. Vibrato center judgments depend on rate and waveform, and hertz and cent averages differ. Duo stability applies to the stated linear model; quartet stability depends on its interaction matrix. Conductors supplement listening. Practice meta-analysis reports observational explained variance, not causal shares or a limit on individual potential.
