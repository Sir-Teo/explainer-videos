# Music, Built: Part 34, Raga and Tala

Part 34 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first part of Act VI. Near the end of a solo the player launches a phrase three
times, and musicians and audience land together on the first beat of the cycle. The tihai is arithmetic done in real
time. This part learns the two systems behind it, raga and tala: the drone and the tanpura's buzzing bridge, the
swaras and the shruti question, ascent, descent and characteristic phrases, gamaka, the thaats and the seventy-two
melakartas, the talas and the tihai equation, how a performance unfolds, the two traditions and how they are taught,
and what computational studies can and cannot say. The models are Monochord's (`explainer/music/monochord/raga.py`);
every sound is ours: a tanpura string modelled by finite differences, tabla strokes by modal synthesis from Part 9's
loaded membrane, and melodic lines as a synthesized bowed tone. Phrases are written in the manner of the ragas named;
no recording is played. Published findings are the ones listed under Sources.

* **Three times to sam.** A cycle of Teentaal and a tihai (dha-ti-dha three times with gaps of two beats, from beat 5,
  its last stroke on sam), heard; a note on the traditions; how to listen; the plan.
* **1. The drone.** Its role; the curved bridge and its thread; one string modelled with a sharp and a curved bridge
  (brightness 474 against 1,217 Hz at 0.1 s, 323 against 1,128 at 0.3 s) and the four-string cycle, heard; the drone
  retuned to Ma, heard; Raman and the physics of jawari.
* **2. Swara and shruti.** The seven swaras and twelve positions; the 22 shrutis as one modern list of just ratios; two
  Res a comma apart (9/8 and 10/9), heard; an ear question (Ga at 400 cents beats about 10 times a second against the
  drone, at 386 it is still); why Sa and Pa never move; intonation measured (Jairazbhoy and Stone; later pitch tracking).
* **3. More than a scale.** What a raga is; an ear question (Bilawal or Yaman: one note and a habit of movement apart);
  Bhupali's five notes, heard; a raga's grammar; vadi and samvadi; time, season and mood.
* **4. Gamaka.** Meend, andolan, kan, gamak; the space between the notes; a phrase plain and ornamented, heard as a
  moving pitch line; the pitch histogram of an ornamented alap of ours; gamaka in Carnatic music; kampita, heard.
* **5. Thaats and melakartas.** Bhatkhande's ten thaats among the 32 possible scales; one phrase in Bilawal, Kalyan and
  Bhairav, heard; the 72 melakartas generated and numbered (29 the major scale, 65 the Lydian); what thaats leave out;
  names that are numbers (katapayadi).
* **6. Tala.** Cycles, claps and waves, theka and bols; Teentaal, Jhaptaal and Rupak, heard; the tala is not the drum
  pattern; Carnatic tala; Adi tala kept by hand, heard; tempo.
* **7. The tihai equation.** (s − 1) + 3p + 2g − 1 ≡ 0 modulo the cycle; a solver's table for Teentaal; an ear question
  (bedam or dumdar?); tihais of tihais; 15 chakkardars found for small phrases and gaps.
* **8. How a performance unfolds.** Alap, jor, jhala, gat; the alap's shape; a jhala of ours, heard; the gat; time and
  the audience; songs and singers.
* **9. Two traditions, and how they are taught.** North and south; teacher and student; rhythm you can say; the
  instruments; today.
* **10. Frontier: computing raga.** What CompMusic's studies can do; what they cannot; machines that play ragas;
  ★ research problem: what do listeners attend to when they recognise a raga?
* **Variation 34, recap and problems.** The Tune as Bilawal: an alap on its first phrase over the drone, its first two
  phrases as a gat in Teentaal with the tabla, then a tihai from beat 5 whose last note, Sa, lands on sam; the ledger;
  what we found; five problems; where it comes back; in practice; references; Part 35.

## What is computed, and what is heard

`python -m videos.music.music34.compute` (about ten seconds) fills `.cache/music34/`.

| Item | What it computes | Checked against |
|---|---|---|
| `tanpura`, `dronema` | a string with and without the curved bridge; brightness over time; the drone with Pa and with Ma | the bridge brightens (tests) |
| `shruti`, `comma`, `ga` | the 22 shrutis in cents; two Res; Ga tempered and just over the drone | the syntonic comma |
| `raga`, `bhupali`, `thaats3` | ascent, descent and phrases for Bilawal, Yaman and Bhupali; one phrase in three thaats | — |
| `gamaka`, `kampita` | contours with meend, andolan and kampita; a pitch histogram | — |
| `thaat` | the 32 scales of the thaat scheme; the 72 melakartas | Venkatamakhin's numbering (tests) |
| `tala`, `adi` | thekas of Teentaal, Jhaptaal, Rupak; Adi tala by hand | — |
| `hook`, `tihai`, `chakkardar` | tihais solved and heard; chakkardars counted | brute-force counting of strokes |
| `tune`, `variation` | Variation 34 | — |

Monochord's tools are held in `tests/music/test_raga.py`; this part's claims and clips in
`tests/music/test_music34.py`.

**Sounds.** The tanpura is a string by finite differences over a curved obstacle (a physical model); the tabla is
modal synthesis on the modes of Part 9's loaded membrane; the melodic voice is an additive bowed-string-like tone
following computed pitch contours (synthesized); the hand claps are filtered noise. There are no recordings.

**What the models are, and are not.** *The tanpura* model is one string in one plane, a rigid bridge with no thread,
and an inelastic contact: it shows the jawari's added brightness but not its long, evolving shimmer, which depends on
the thread and a gentler contact. *The tabla* has no pressure of the heel on the bayan beyond a fixed glide, and its
bols are simplified. *The phrases* are ours, written to show the features named, not compositions or performances of
the ragas; ragas are taught by teachers and learned by listening, and nothing here replaces that. *The shruti list*
is one of several modern reconstructions.

## Build

```bash
python -m videos.music.music34.compute                          # numbers and sounds (about ten seconds)
EXPLAINER_TTS=silent python tools/build.py music34 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music34 --sync                         # the sound gates
python tools/dead_air.py renders/music34_480p.mp4 --sound music34  # no empty screen; no sound over a still one
python tools/lecture_length.py music34                          # 30 to 60 minutes, listening included
python tools/build.py music34                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 34                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** Find every tihai in Jhaptaal (10 beats) that starts on beat 6, with phrases up to 6 beats.

   *Solution.* With s = 6 the condition is 5 + 3p + 2g − 1 ≡ 0 (mod 10), i.e. 3p + 2g ≡ 6 (mod 10). With gaps up to 3
   there are two: p = 2, g = 0 (a bedam tihai of six beats, landing on the next sam) and p = 4, g = 2 (sixteen beats,
   landing a cycle later). The lab prints the list for any tala, start and range.

2. **Prove.** Prove that there are exactly 72 melakartas under Venkatamakhin's rule.

   *Solution.* Sa and Pa are fixed. Ma takes one of two forms. Ri and Ga occupy two of the four semitone places between
   Sa and Ma (C(4, 2) = 6 ways, each with Ri below Ga), and Dha and Ni two of the four places between Pa and the upper
   Sa (6 ways). Choices are independent: 2 × 6 × 6 = 72.

3. **Ear.** The lab plays phrases in Bilawal and in Yaman; name the raga of each.

   *Solution.* The lab prints them. Listen for Ma: Yaman's is raised (a semitone below Pa) and its phrases often begin
   from Ni below Sa; Bilawal's Ma is natural.

4. **Build.** Add a moving thread to the tanpura model, and measure how the buzz changes.

   *Where to look.* `raga.jawari_string` clamps the string to a fixed parabolic surface. Model the thread as a second,
   point-like obstacle at a chosen position near the bridge edge, move it in steps, and plot the brightness (spectral
   centroid) over the first second for each position; compare with published simulations of the tanpura bridge.

5. ★ **What do listeners attend to when they recognise a raga?**

   *Where the frontier is.* Use performances of ragas with the same scale, annotated by musicians; build stimuli that
   keep or remove the phrases, the gamakas or the note weights; test trained and untrained listeners' recognition and
   confidence; report which features carry recognition, with intervals, and check the results with practitioners.

## Sources

* N. A. Jairazbhoy, *The Rāgs of North Indian Music* (1971); J. Bor (ed.), *The Raga Guide* (1999); M. Clayton, *Time in
  Indian Music* (2000); T. Viswanathan and M. H. Allen, *Music in South India* (2004).
* N. A. Jairazbhoy and A. W. Stone, "Intonation in present-day North Indian classical music", *Bulletin of SOAS* (1963).
* C. V. Raman, "On some Indian stringed instruments", *Proceedings of the Indian Association for the Cultivation of
  Science* (1921); C. P. Vyasarayani, S. Birkett and J. McPhee, "Modeling the dynamics of a vibrating string with a
  finite distributed unilateral constraint: application to the sitar", *JASA* (2009).
* X. Serra, "A multicultural approach in music information research", *ISMIR* (2011), and the CompMusic project's
  publications on tonic identification, raga recognition and rhythm (2011–2017).
* V. N. Bhatkhande, *Hindusthani Sangeet Paddhati* (1909–32); Venkatamakhin, *Caturdaṇḍīprakāśikā* (about 1660).
* Part 5 for consonance; Part 6 for commas; Part 9 for the tabla's membrane; Part 11 for metre; Part 33 for cycles.
