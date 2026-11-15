# Music, Built: Part 63, Finding Music

Part 63 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the third part of Act XI, *Listening Machines*. Five seconds in a noisy bar are enough
for a phone to name a song among a hundred million; a service with millions of listeners chooses what each of them hears
next. This part builds both kinds of finder: Wang's constellation fingerprint with its hash table and votes, tested
through noise, codecs, speed changes and samples, and a melody search that finds the song rather than the recording;
then content embeddings, a classifier that was right for the wrong reason, implicit matrix factorization on simulated
listeners, the cold start, a recommender feeding on its own popularity, and playlists. The tools are Monochord's
(`explainer/music/monochord/mir/finder.py`); the library searched is every sound of Parts 1 to 60 (908 clips, 3.7 hours,
1.15 million hashes), and the listeners are simulated with tastes known, so every answer can be checked.

* **A song from a noisy bar.** Five seconds of Variation 40, the music no louder than the bar, named with its offset
  (23 votes against the runner-up's 12); how the search began (Shazam, 2002); the plan.
* **1. A constellation of peaks.** Why not compare waveforms; a Variation's spectrogram reduced to its peaks (about 20 a
  second); the peaks alone, heard.
* **2. Hashes and votes.** Pairs of peaks as 24-bit hashes; the table; voting for a clip and an offset; what a match looks
  like (44 of the true clip's 179 shared hashes on one diagonal, the Tune's repeats on shorter ones; the runner-up's 32
  scattered).
* **3. Noise, codecs and chance.** One query in three bars, heard (named at +10 and 0 dB, lost at −5); recognition against
  white noise and bar noise (bar noise is harder: 61 % at 0 dB, 25 % at −5); how long a query must be (at 0 dB, 9 % at one
  second, 65 % at five, 81 % at eight), one second and eight heard; an ear question on a 16 kbit/s codec (the first was
  coded; 75 % still named); the arithmetic of chance (27 chance hits per query, scattered); a hundred million tracks (six
  chance hits in one place stays below one in 10¹⁶).
* **4. Recordings, not songs.** The Tune rendered afresh (its best guess 38 votes, a tenth of a true excerpt's); an ear
  question on a Variation played 4 % fast (not named: at 1 % fast 59 %, at 2 % 25 %); a Variation as a sample under another
  (found 93 % level, 47 % at −12 dB; the demo at −12 is missed); a hummed query, slower, in another key and a little out of
  tune, missed by the fingerprint and found first of 30 melodies by a pitch contour and time warping.
* **5. Tags and embeddings.** Tags and who writes them; Monochord's 62-number embedding; all 908 clips on its first two
  principal components (the acts overlap almost completely: it knows sound, not subject); an ear question on neighbours
  (the second, Part 48's test tones, is the farthest clip in the series); GTZAN's faults.
* **6. Right for the wrong reasons.** Clever Hans; an ear question (a Variation with a faint mains hum: the second); a
  classifier of first-half against second-half Variations scores 83 % with the hum, 43 % with it removed, and 48 % trained
  honestly and split by clip, no better than guessing the commoner half (56 %); its weight on the three lowest bands
  (9 % against 3 %); how to catch a horse.
* **7. Learning from listening.** Collaborative filtering; the play matrix (500 listeners by 300 clips, 11 % of cells lit)
  and its factorization; implicit ALS (Hu, Koren and Volinsky, 2008); recall at 10 (random 0.038, popularity 0.077, ALS
  0.127); one listener's top three, heard.
* **8. Cold start and exploring.** Thirty clips nobody has played, scored from content (recall at 5: 0.28 against 0.17 at
  random); a cold clip and its nearest played neighbour, heard; exploring.
* **9. Popularity feeding on itself.** A recommender that shows the most played; the Gini of plays over thirty rounds (0.97;
  0.71 exploring 30 %; 0.13 with no recommender); Lorenz curves (the top tenth of clips gets 99 %, 73 % and 14 % of plays);
  what it means.
* **10. Playlists, fairness and metadata.** An ear question (random order or smooth? the second was ordered); nearest
  neighbour and 2-opt (path 226 against 439); the path on the map; who gets heard; credits and metadata.
* **11. Frontier: foundation models and creators.** Music foundation models and text-to-audio search; effects on
  creators; the evidence so far (Léveillé Gauvin, 2018: introductions from about 20 seconds to about 5); ★ research
  problem: how much of the change in music over the streaming era did recommenders cause?
* **Variation 63, recap and problems.** Five noisy seconds of three earlier Variations (27, 34 and 56), each named; the
  ledger; what we found; five problems; where it comes back; in practice; references; Part 64.

## What is computed, and what is heard

`python -m videos.music.music63.compute` (several minutes: every clip of Parts 1 to 60 is read and indexed) fills
`.cache/music63/`.

| Item | What it computes | Checked against |
|---|---|---|
| `library`, `hook`, `constellation`, `matches` | the index; a noisy query named with its offset; peaks and hashes; shared hashes | the excerpt's true clip and offset (tests) |
| `robust`, `length`, `lengthpair`, `speed`, `sampled` | recognition through noise, codecs, short queries, speed changes and samples | the true clips, with duplicate audio counted as aliases (tests) |
| `falsematch`, `scale` | chance agreement, by the Poisson tail; pure-noise queries; a fresh recording | votes for pure noise against true excerpts (tests) |
| `hum` | a sung query's YIN contour against thirty melodies by time warping | the melody sung (tests) |
| `horse`, `map`, `neighbours` | the hum classifier, split by clip; the embedding's principal components; nearest and farthest | the hum and the clips' parts (tests) |
| `recs`, `matrix`, `loop`, `lorenz`, `playlist` | ALS against popularity; the cold start; the feedback loop; playlists | the simulated tastes (tests) |

Monochord's tools are held in `tests/music/test_finder.py`; this part's claims and clips in `tests/music/test_music63.py`.

**Sounds.** Every clip of Parts 1 to 60, as each part stored it; simulated bar noise (voices and glasses); Part 58's coder;
Part 38's piano; Part 8's alto voice for the hummed query.

**What the models are, and are not.** *The fingerprint* follows Wang (2003): 8 kHz, 1024-point frames, peaks in 15 × 11
neighbourhoods, five partners per anchor, 24-bit hashes; real services tune all of these and add verification. Some
parts reuse a Variation's audio in another clip; such duplicates are counted as correct. *The embedding* is 62 hand-made
numbers; learnt embeddings are far richer, and the map's overlap is a property of this one. *The listeners* are simulated:
tastes on six factors, partly predictable from content, plays drawn from them; real data have none of this tidiness.
*The melody search* compares against thirty melodies by full time warping; real services index millions.

## Build

```bash
python -m videos.music.music63.compute                          # numbers and sounds (several minutes)
EXPLAINER_TTS=silent python tools/build.py music63 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music63 --sync                         # the sound gates
python tools/dead_air.py renders/music63_480p.mp4 --sound music63  # no empty screen; no sound over a still one
python tools/lecture_length.py music63                          # 30 to 60 minutes, listening included
python tools/build.py music63                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 63                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** A query has 300 hashes; the library 50 million; hashes are 24 bits. How many chance hits? Spread over a
   million clip-offsets, how many per bin?

   *Solution.* Each query hash equals a given stored hash with probability 2⁻²⁴ ≈ 6.0 × 10⁻⁸, so the expected chance hits
   are 300 × 5 × 10⁷ × 2⁻²⁴ ≈ 894. Spread over 10⁶ bins that is about 0.0009 per bin; the chance that some bin collects five
   is, by the Poisson tail and a union bound, about 10⁶ × 0.0009⁵ / 120 ≈ 5 × 10⁻¹². A true match's dozens of aligned votes
   stand far above chance.

2. **Prove.** Show that with confidences c_ui fixed, each ALS step solves a weighted least-squares problem exactly, so the
   loss never increases.

   *Solution.* The loss Σ c_ui (p_ui − x_uᵀ y_i)² + λ(Σ‖x_u‖² + Σ‖y_i‖²) is, for fixed Y, a sum over users of independent
   quadratics in each x_u, with minimizer x_u = (YᵀC_uY + λI)⁻¹ YᵀC_u p_u; the matrix is positive definite, so this is the
   unique minimum. Replacing X by it cannot raise the loss; the same holds for Y given X. Alternating, the loss is
   non-increasing and bounded below, so it converges (to a stationary point, not necessarily the global minimum).

3. **Ear.** The lab plays queries at several noise levels; guess where the fingerprinter fails, then check.

   *Solution.* The lab prints which were named. Compare with the level at which you stopped hearing the piece: the ear
   follows a tune through noise by its continuity, while the fingerprinter needs enough of its exact peaks to survive.

4. **Build.** Add exploration by Thompson sampling to the feedback loop, and measure inequality and recall.

   *Where to look.* Keep a Beta posterior on each song's chance of being played when shown; each round, draw from every
   posterior and show each listener the five highest draws; update with the plays. Report the Gini of plays and the recall
   against the listeners' true tastes, against plain popularity and against random exploration at the same rate.

5. ★ **How much of the change in music over the streaming era did recommenders cause?**

   *Where the frontier is.* Simulate listeners, artists who adapt to what is rewarded and a recommender between them; fit
   the simulation to what can be observed (release patterns, song lengths, introductions, concentration of plays over
   time); compare worlds with popularity ranking, personal ranking, exploration and no recommender. Natural experiments
   (changes in a platform's ranking, by country and date) would sharpen it.

## Sources

* M. Müller, *Fundamentals of Music Processing* (2nd ed., 2021); O. Celma, *Music Recommendation and Discovery* (2010);
  M. Schedl et al., "Current challenges and visions in music recommender systems research", *IJMIR* (2018).
* A. Wang, "An industrial-strength audio search algorithm" (ISMIR, 2003); J. Haitsma and T. Kalker, "A highly robust audio
  fingerprinting system" (ISMIR, 2002); A. Ghias et al., "Query by humming" (ACM Multimedia, 1995).
* G. Tzanetakis and P. Cook, "Musical genre classification of audio signals", *IEEE Trans. Speech and Audio Processing*
  (2002); B. L. Sturm, "The GTZAN dataset: its contents, its faults, their effects on evaluation, and its future use"
  (2013); B. L. Sturm, "A simple method to determine if a music information retrieval system is a horse", *IEEE Trans.
  Multimedia* (2014).
* Y. Hu, Y. Koren and C. Volinsky, "Collaborative filtering for implicit feedback datasets" (ICDM, 2008); M. J. Salganik,
  P. S. Dodds and D. J. Watts, "Experimental study of inequality and unpredictability in an artificial cultural market",
  *Science* (2006); O. Celma and P. Cano, "From hits to niches?" (2008).
* H. Léveillé Gauvin, "Drawing listener attention in popular music: testing five musical features arising from the theory
  of attention economy", *Musicae Scientiae* (2018).
