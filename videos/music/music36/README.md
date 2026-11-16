# Music, Built: Part 36, Bronze and Silk

Part 36 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the third part of Act VI. In 1978 a tomb in Hubei, sealed in 433 BCE, gave up
sixty-five bronze bells. Each sounds two notes, depending on where it is struck, and their inscriptions are a tuning
treatise older than Aristoxenus. This part goes from those bells, through Chinese pitch theory and the guqin, to the
gamelan, an orchestra whose paired instruments are tuned apart on purpose so that the whole shimmers. The models are
Monochord's (`explainer/music/monochord/bronze.py`): a two-tone bell by modal synthesis with designed mode families,
Part 9's bars, gongs and membrane, and Part 35's retuned plucked string for the qin. Every melody is ours, and the
gamelan tunings are illustrative: no two gamelans are tuned alike. Published findings are the ones listed under Sources.

* **Two notes from one bell.** An ear question (three bells, centre then side: same note or two?); the tomb of Marquis
  Yi; listening across traditions; the plan.
* **1. The bells of Marquis Yi.** Why an almond section gives two notes; a minor-third and a major-third bell, heard;
  the set of 65; a melody of ours on two-tone bells, heard; the inscriptions; two kinds of bell.
* **2. Twelve pitches from a pipe.** The rule of three from a length of 81; the first five, the pentatonic, heard; the
  twelve lü and the Pythagorean comma (23.46 cents); the twelve heard as a chromatic scale (semitones of 90 and 114
  cents); the yellow bell; pitches and the calendar.
* **3. Jing Fang's sixty.** How close n fifths come to whole octaves for n up to 60 (12: 23.5 cents; 41: −19.8; 53:
  3.6); 12 and 53 fifths heard against the start (beats of 3.6 and 0.55 per second); fifty-three elsewhere; after Jing
  Fang (Qian Lezhi, He Chengtian, Zhu Zaiyu in 1584); Pythagorean against equal temperament, heard; how Zhu Zaiyu
  computed it.
* **4. Five notes, five modes.** Gong, shang, jue, zhi and yu, heard; a pentatonic melody of ours, then with the bian
  tones, heard; seven from five; five notes on stage; melody without semitones.
* **5. The guqin.** The instrument; the thirteen hui as harmonic nodes; harmonics at six hui, heard; the open strings in
  a common tuning, heard; one pitch as open string, stopped note and harmonic, heard; the repertory; jianzipu.
* **6. Heterophony and gagaku.** Heterophony; the Tune's first phrase three ways at once, heard; gagaku; clusters in the
  manner of the sho (ours), heard; court music in Korea.
* **7. Slendro and pelog.** Gamelan; illustrative slendro and pelog, heard; two pelog subsets, heard; the Tune's phrase
  in both, heard; no standard (Surjodiningrat and colleagues); how a gamelan is tuned; spectrum and scale (dissonance
  curves for a harmonic spectrum and a uniform free bar, whose minima fall at 870, 1,002 and 1,166 cents with none at
  the octave; Sethares's measured spectra), heard on both tones.
* **8. Tuned apart on purpose.** Ombak; an ear question (which pair shimmers?), with 6 Hz needing 78, 39 and 20 cents of
  detuning in three octaves; slow and fast shimmer, heard; a beat by design; gamelan and the West.
* **9. The gong cycle and interlocking parts.** Colotomic structure; a lancaran of ours, heard; an ear question (one
  player or two?) on kotekan; irama at two and four notes per beat, heard; layers of speed; a kebyar-style burst, heard;
  gamelan worldwide.
* **10. Frontier: bells and tunings measured.** The bells as data; tunings as data; heritage and ownership;
  ★ research problem: do gamelan tunings fit their instruments' spectra?
* **Variation 36, recap and problems.** The Tune's first two phrases as natural harmonics on a qin tuned by pure fifths
  and fourths (the program choosing string and harmonic; the worst 8 cents from equal temperament), then as a balungan
  in an illustrative pelog with interlocking elaboration, kenong and gong; the ledger; what we found; five problems;
  where it comes back; in practice; references; Part 37.

## What is computed, and what is heard

`python -m videos.music.music36.compute` (about ten seconds) fills `.cache/music36/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook`, `thirds`, `bellsong` | two-tone bells struck at centre and side; a melody on them | the side note's interval (tests) |
| `lu`, `twelve`, `jingfang`, `zhu` | the rule of three; the twelve lü; closeness of chains of fifths; Pythagorean and equal | Jing Fang's 53 |
| `modes`, `melody` | the five modes; a melody with and without bian tones | — |
| `qin`, `openqin`, `stopped` | harmonics at the hui; the open strings; one pitch three ways | harmonic node positions |
| `hetero`, `sho` | heterophony; sho-like clusters | — |
| `spectra`, `scales`, `patet`, `two_scales` | dissonance curves for two spectra; illustrative slendro and pelog | no octave minimum for a bar |
| `ombak`, `rates` | paired tuning by beat rate | cents shrink with pitch |
| `cycle`, `kotekan`, `irama`, `kebyar` | a lancaran; interlocking parts; densities; a burst | every pulse once |
| `tune`, `variation` | Variation 36 | — |

Monochord's tools are held in `tests/music/test_bronze.py`; this part's claims and clips in
`tests/music/test_music36.py`.

**Sounds.** Two-tone bells by modal synthesis with designed mode families (a model of the principle, not of a measured
bell); metallophones as Part 9's free bar; gongs and the kempul as Part 9's gong; the qin as Part 35's plucked string at
exact pitches; sho-like clusters, pure tones and harmonic tones by additive synthesis. There are no recordings.

**What the models are, and are not.** *The bells* have designed mode ratios; real bells' partials come from their
measured shapes. *The gamelan tunings* are illustrative: real gamelans each have their own embat, and measured tunings
differ by tens of cents. *The bar* is uniform; real gamelan keys are shaped, which is why Sethares's measured spectra
behave differently from ours. *The qin* model has no slides or touch noise. *All melodies* are ours.

## Build

```bash
python -m videos.music.music36.compute                          # numbers and sounds (about ten seconds)
EXPLAINER_TTS=silent python tools/build.py music36 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music36 --sync                         # the sound gates
python tools/dead_air.py renders/music36_480p.mp4 --sound music36  # no empty screen; no sound over a still one
python tools/lecture_length.py music36                          # 30 to 60 minutes, listening included
python tools/build.py music36                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 36                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** Using the rule of three from a length of 81, compute the first seven lengths and their pitches in cents.

   *Solution.* 81, 54, 72, 48, 64, 128/3 ≈ 42.67, 512/9 ≈ 56.89; folded into one octave above the first: 0, 702, 204,
   906, 408, 1110 and 612 cents. The first five are the pentatonic; the sixth and seventh are B and F♯, the bian tones.

2. **Prove.** Prove that n pure fifths can never exactly equal a whole number of octaves.

   *Solution.* (3/2)ⁿ = 2ᵐ would mean 3ⁿ = 2ⁿ⁺ᵐ; the left side is odd and the right side even for n ≥ 1, which is
   impossible. So every chain of fifths misses, however long; Jing Fang's 53 merely misses by little.

3. **Ear.** The lab plays pairs of metallophones; say which pairs are tuned apart, and how fast they beat.

   *Solution.* The lab prints the answers. Count the slow swells: four a second is a gentle wave, seven a fast shimmer;
   a pair in unison sounds like one instrument, louder.

4. **Build.** Write a colotomic renderer for ladrang (32 beats) and play a balungan of your own in it.

   *Where to look.* Extend `bronze.COLOTOMIC` with a ladrang pattern (kenong every 8 beats, kempul between, ketuk on the
   odd beats or at the chosen irama, gong at 32), reuse `compute_cycle`'s rendering, and check that the gong falls on the
   last beat of every cycle.

5. ★ **Do gamelan tunings fit their instruments' spectra?**

   *Where the frontier is.* Measure keys and gongs of many gamelans (spectra and tunings); compute each set's dissonance
   minima from its own spectra; test, against tunings drawn at random from plausible ranges, whether real tunings sit
   nearer the minima; report effect sizes with uncertainty, and discuss with makers what they aim for.

## Sources

* L. von Falkenhausen, *Suspended Music: Chime-Bells in the Culture of Bronze Age China* (1993); Chen Cheng-Yih (ed.),
  *Two-Tone Set-Bells of Marquis Yi* (1994).
* J. Needham, *Science and Civilisation in China*, vol. 4 part 1 (1962), on acoustics and pitch; K. G. Y. Robinson, *A
  Critical Study of Chu Tsai-yü's Contribution to the Theory of Equal Temperament in Chinese Music* (1980).
* R. van Gulik, *The Lore of the Chinese Lute* (1940).
* M. Tenzer, *Gamelan Gong Kebyar* (2000); Sumarsam, *Gamelan: Cultural Interaction and Musical Development in Central
  Java* (1995); C. McPhee, *Music in Bali* (1966).
* W. Surjodiningrat, P. J. Sudarjana and A. Susanto, *Tone Measurements of Outstanding Javanese Gamelans in Jogjakarta
  and Surakarta* (1972); W. A. Sethares, *Tuning, Timbre, Spectrum, Scale* (2nd ed. 2005), chapter 10.
* Part 5 for dissonance curves; Part 9 for bars, bells and gongs; Part 33 for continued fractions and tilings.

## Interpretation limits

The tomb’s full 65-bell assemblage is not uniformly the same two-tone bell type. Inscribed pitch names are not modern absolute frequency standards. Twelve generated notes require eleven generator steps, while twelve fifths produce the comma comparison. Pentatonic collections can establish tonic attraction without a semitone leading tone. Gagaku is a continuing tradition, not a frozen historical exhibit. Heterophony can coexist with counterpoint and chordal effects. The gamelan tunings, beat-rate profile and alternating interlock are illustrative choices; practices vary by ensemble, genre and region. Javanese performance can include prominent solo and leading parts. Timbre and tradition are joint explanations, not exclusive alternatives.
