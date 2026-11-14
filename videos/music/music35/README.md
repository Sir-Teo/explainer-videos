# Music, Built: Part 35, Maqam

Part 35 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second part of Act VI. Cairo, 1932: a congress meets to settle the Arab scale,
perhaps as equal quarter tones, and cannot agree, because the best musicians do not play a grid. A thousand years
earlier al-Fārābī had written one of the most advanced treatises on tuning in the world. This part learns a system
whose notes lie between the piano's keys: ajnas and maqamat, neutral intervals from al-Fārābī and Ṣafī al-Dīn to 24
and 53 equal steps, the Cairo congress, Turkish theory in commas, the Persian dastgah, rhythmic cycles, the taqsim,
the instruments, and what measurement can and cannot settle. The engine is Monochord's
(`explainer/music/monochord/maqam.py`); the oud is a plucked string retuned to exact pitches (within a fraction of a
cent) through Part 7's guitar body, the darbuka Part 9's membrane. Every phrase is ours. Published findings are the
ones listed under Sources.

* **Between the keys.** An ear question (C with thirds of 300, 400 and 350 cents: which lies between?); the Cairo
  congress; where maqam lives; the plan.
* **1. Ajnas: the building blocks.** The jins and its Greek roots; eight ajnas from C, heard; the step sizes (100, 150,
  200, 300 cents); jins Bayati on D, G and A, heard; what the names mean.
* **2. Maqamat and their paths.** Rast, Bayati, Hijaz and Saba as two ajnas joined, heard; Rast up with B half-flat
  and down with B flat, heard; Saba, which reaches D flat where its octave would be, heard; sayr; where maqamat
  travel; families.
* **3. Neutral intervals, old and new.** Zalzal's fret at 27/22 (355 cents), recorded by al-Fārābī; the Greek
  inheritance; Ṣafī al-Dīn's seventeen notes from a chain of fourths (steps of 90, 90 and 24 cents); the old ratios
  against 24 and 53 equal steps (24 fits the neutral intervals within five cents, 53 the just and Pythagorean ones
  within two); three neutral thirds (350, 355, 362), heard; quarter tones in the West; why neutral intervals.
* **4. Cairo, 1932.** Mushāqa's 24-step grid; the congress; Bartók and the European guests; what musicians do, with an
  illustration (values ours) of one written E half-flat placed at 360 cents in Rast and 340 in Bayati, heard; the
  twentieth-century orchestra; after the congress.
* **5. Turkish makam in commas.** Arel–Ezgi–Uzdilek's 53 commas; Turkish Rast (9, 8, 5, 9, 9, 8, 5 commas; segah at
  385 cents); an ear question (Arabic or Turkish third?); Ottoman music; writing commas down; theory against practice.
* **6. The Persian dastgah.** Seven dastgahs and five avazes; the radif; Vaziri's koron and sori and Farhat's
  measurements; a phrase of ours with a koron, heard; song and poetry.
* **7. Rhythmic cycles.** Dum and tek; an ear question (maqsum, samai thaqil, aksak: which has ten beats?); maqsum and
  baladi, one stroke apart, heard; rhythm and dance; speaking the cycles; long Ottoman cycles.
* **8. Taqsim and modulation.** The taqsim; a taqsim of ours in Bayati visiting Saba, heard and drawn; learning to
  improvise; a second, in Hijaz, heard; tarab.
* **9. The instruments.** The oud; tuning the oud; the qanun and its levers, with a course lowered lever by lever,
  heard; the ney and the ensemble; a ney-like tone, heard.
* **10. Frontier: measuring makam.** Computational makam analysis; standards and their critics; machines and maqam;
  studying a living tradition fairly; ★ research problem: what determines where a musician places a neutral note?
* **Variation 35, recap and problems.** A short taqsim in Rast, then the Tune's first two phrases in Rast on C (2 of
  14 notes leave the piano's keys), Bayati on D (6 change) and Hijaz on D (4 change), over maqsum; the ledger; what we
  found; five problems; where it comes back; in practice; references; Part 36.

## What is computed, and what is heard

`python -m videos.music.music35.compute` (about ten seconds) fills `.cache/music35/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook`, `thirds3`, `ehalf` | thirds of 300, 400, 350; three neutral thirds; an illustration of context-dependent placement | — |
| `ajnas`, `tonics`, `maqamat`, `descent`, `saba` | ajnas and maqamat in cents, heard | the scale definitions (tests) |
| `neutral`, `safi` | medieval ratios; errors in 24 and 53 equal steps; the 17-tone gamut | the chain of fourths |
| `turkish` | Rast in Arel–Ezgi–Uzdilek commas against the Arabic Rast | 53 commas to the octave |
| `iqa`, `baladi` | maqsum, baladi, samai thaqil, aksak on the darbuka | cycle lengths |
| `taqsim`, `hijaz`, `koron` | taqsims and a phrase of ours | — |
| `mandal`, `ney` | a course lowered by lever steps; a ney-like tone | — |
| `tune`, `variation` | Variation 35 | — |

Monochord's tools are held in `tests/music/test_maqam.py` (including the oud's pitch, within two cents); this part's
claims and clips in `tests/music/test_music35.py`.

**Sounds.** The oud is Part 7's Karplus–Strong string generated at four times the output rate and read back at the
rate that puts it exactly on pitch, through Part 7's guitar body (a physical model); the darbuka is Part 9's membrane;
the ney-like tone is synthesized. There are no recordings.

**What the models are, and are not.** *The ajnas* are given on the 24-step grid, as modern Arabic theory writes them;
musicians' intonation differs by maqam, phrase and performer, and the film's one illustration of that uses values of
its own, not measurements. *The oud* has no fingered slides or vibrato. *The rhythms* are bare cycles; in practice
they are filled and ornamented. *The phrases* are ours, written to show the features named.

## Build

```bash
python -m videos.music.music35.compute                          # numbers and sounds (about ten seconds)
EXPLAINER_TTS=silent python tools/build.py music35 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music35 --sync                         # the sound gates
python tools/dead_air.py renders/music35_480p.mp4 --sound music35  # no empty screen; no sound over a still one
python tools/lecture_length.py music35                          # 30 to 60 minutes, listening included
python tools/build.py music35                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 35                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** Build maqam Saba on D in cents, and find the nearest steps of 24 and of 53 equal divisions for each note.

   *Solution.* Saba = jins Saba on D (0, 150, 300, 400) and jins Hijaz on F (300, 400, 700, 800): 0, 150, 300, 400, 700,
   800. In 24 steps: 0, 3, 6, 8, 14, 16, exactly. In 53: 0, 7, 13, 18, 31, 35, with errors of +8.5, −5.7, +7.5, +1.9 and
   −7.5 cents. The lab prints any maqam.

2. **Prove.** Prove that a chain of 17 pure fourths, folded into the octave, gives steps of only two sizes plus one
   comma.

   *Solution.* By the three-gap theorem (Part 33) the folded points leave at most three gap sizes, the largest the sum of
   the other two. Computing them: the limma (256/243, 90.2 cents) and the Pythagorean comma (23.5 cents) appear, and
   their sum, the apotome (113.7 cents), would be the third size; with 17 points the gaps are 12 limmas and 5 commas,
   since 12 × 90.2 + 5 × 23.5 = 1200 (to rounding).

3. **Ear.** The lab plays phrases in Rast, Bayati and Hijaz; name the maqam of each.

   *Solution.* The lab prints them. Hijaz has the wide step (300 cents) between its second and third notes; Bayati starts
   with a three-quarter tone; Rast starts with a whole tone and then a three-quarter tone.

4. **Build.** Add mandal levers to the oud model's qanun cousin: a string set that retunes mid-phrase.

   *Where to look.* Give each course a list of lever positions in cents (for an Arabic qanun, quarter tones; for a
   Turkish one, finer steps) and a schedule of lever changes; render with `maqam.oud` at the course's current pitch, and
   play a taqsim that modulates from Bayati to Saba by moving one lever.

5. ★ **What determines where a musician places a neutral note?**

   *Where the frontier is.* Collect recordings of one maqam by many performers across regions and decades; track
   pitch and segment notes; model each note's pitch as a function of maqam, melodic direction, metrical position,
   performer and era, with uncertainty; and test the model's predictions against musicians' own descriptions.

## Sources

* S. Marcus, *Music in Egypt* (2007); H. H. Touma, *The Music of the Arabs* (1996); A. J. Racy, *Making Music in the Arab
  World* (2003); J. Farraj and S. Abu Shumays, *Inside Arabic Music* (2019).
* al-Fārābī, *Kitāb al-Mūsīqī al-Kabīr* (10th century); O. Wright, *The Modal System of Arab and Persian Music,
  A.D. 1250–1300* (1978), on Ṣafī al-Dīn.
* *Recueil des travaux du Congrès de musique arabe* (Cairo, 1934); A. J. Racy, "Historical worldviews of early
  ethnomusicologists: an East-West encounter in Cairo, 1932" (1991).
* K. Signell, *Makam: Modal Practice in Turkish Art Music* (1977); B. Bozkurt, O. Yarman, M. K. Karaosmanoğlu and
  C. Akkoç, "Weighing diverse theoretical models on Turkish maqam music against pitch measurements", *Journal of New
  Music Research* (2009).
* H. Farhat, *The Dastgah Concept in Persian Music* (1990).
* Part 5 for roughness; Part 6 for commas; Part 33 for temperaments; Part 34 for raga.
