# Music, Built: Part 40, The Song

Part 40 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the last part of Act VI. The average introduction of a hit single shrank from over
twenty seconds in the mid-1980s to about five by the mid-2010s, and on streaming services a play counts only after about
thirty seconds. This part follows the popular song from the thirty-two-bar standard to the loop and the drop, and finds
its form shaped by each technology that sold it: forms and loops, riffs and distortion, the backbeat and groove, hooks and
prosody, the drum machine (an 808 built from first principles), the break and the sampler, rap's flow, the build, the
drop and the sidechain, and what corpus studies of the charts show. The tools are Monochord's
(`explainer/music/monochord/song.py`). Every song, riff, beat and verse heard is ours; published chart statistics are
quoted, not recomputed (the chart data's licences were not cleared for redistribution). Published findings are the ones
listed under Sources.

* **Twenty seconds to five.** An ear question (the same song of ours with two intros: when does the voice enter?);
  Léveillé Gauvin's 303 singles and the thirty-second rule; the plan.
* **1. From AABA to verse and chorus.** Tin Pan Alley's 32-bar refrain; an AABA song of ours, heard; verse, pre-chorus
  and chorus, heard; why the change; song factories (the Brill Building, Motown, Max Martin).
* **2. Loops and rock harmony.** Three loops (I–V–vi–IV, ♭VII–IV–I, i–♭VI–♭III–♭VII); the three heard; Temperley's
  melodic-harmonic divorce (4 of our hook's 12 on-beat notes outside the chord); rock's scales; progressions and loops.
* **3. Riffs.** The riff; a rock riff of ours, heard; distortion as a curve; an ear question (triad or power chord, through
  distortion?); a funk riff of ours, heard; a lineage.
* **4. The backbeat and groove.** The backbeat; five beats on a sixteen-step grid; the five heard; the one; swing on the
  sixteenths, heard straight and at 60%; disco to house.
* **5. Hooks and prosody.** Hooks; prosody measured (“beautiful day” set two ways: 100% and 25% of syllables agreeing with
  the beat); setting words; the title; earworms.
* **6. The drum machine.** The TR-808; its kick as a struck resonator (83 Hz at the strike, 52 Hz settled); three decays,
  heard; the kick tuned as a bass line, heard; the hats from six square-wave oscillators; the whole kit, heard; after the
  808.
* **7. The break and the sampler.** Kool Herc's breaks; a break of ours, chopped into sixteen, re-sequenced and sped up,
  heard; samplers; the law (*Grand Upright*, *Bridgeport*).
* **8. Flow.** Rap and flow; a verse of ours placed on the beat and in threes; both heard; measured (40 syllables each,
  2.5 a beat; on the beat 40% against 30%; accents mostly fours and twos against almost all threes); rhyme; the writers.
* **9. The build, the drop and the sidechain.** The drop; a build and drop of ours, heard; the sidechain (14 dB, recovering to within 1 dB in about half a second); an ear question (which pad pumps?); the producer's song.
* **10. Frontier: sixty years of charts.** Mauch and colleagues (about 17,000 Hot 100 songs, three revolutions);
  Serrà and colleagues; platforms; what the charts leave out; ★ research problem: do new platforms change how songs are
  written, or only which songs win?
* **Variation 40, recap and problems.** The Tune as a pop single of ours (the voice entering after 4.6 s; its second
  phrase as the verse, its first as the hook, a sidechained pad), then a beat built from sixteen slices of Variation 7's
  recording with four rests; the ledger; what we found; five problems; where it comes back; in practice; references;
  Part 41.

## What is computed, and what is heard

`python -m videos.music.music40.compute` (under a minute) fills `.cache/music40/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook`, `forms` | two intros; AABA and verse–chorus songs of ours | the intro lengths (tests) |
| `loops`, `riffs`, `power` | three loops; the divorce count; two riffs; triad against power chord | hand counts (tests) |
| `beats`, `swing16` | five step patterns; straight and swung sixteenths | the backbeat share (tests) |
| `eight`, `tuned` | the struck-resonator kick, its pitch and decay; the six-square hat; a tuned kick bass | measured pitch and decay (tests) |
| `breaks` | a break chopped, re-sequenced, sped up | the slicing (tests) |
| `flow` | a verse placed two ways; prosody | hand counts (tests) |
| `drop` | a build and drop; the sidechain's gain curve | ducking depth and recovery (tests) |
| `tune`, `variation` | Variation 40 | — |

Monochord's tools are held in `tests/music/test_song.py`; this part's claims and clips in `tests/music/test_music40.py`.

**Sounds.** Guitar and bass are Part 35's retuned plucked string (the guitar through a model amplifier: soft clipping and a
speaker's band limit); the acoustic kit is Part 9's membrane with filtered noise; the drum-machine voices are built from
their circuits' principles (a struck resonator; noise bursts; six square waves); pads and sub-bass are additive; the
voice is Part 17's model, which sings vowels, not words (clips with it are labelled `synthesized`). Variation 40 samples
the series' own Variation 7. There are no other recordings.

**What the models are, and are not.** *The 808 voices* follow the circuits' principles, not their component values;
the pitch sag is a designed envelope. *The amplifier* is a tanh curve and a band-pass, not a model of any amplifier.
*The voice* cannot speak words, so the rap verse is heard as rhythm and contour only. *The patterns, songs, riffs and
verse* are ours, written to show the features named. *Chart findings* are quoted from the cited studies.

## Build

```bash
python -m videos.music.music40.compute                          # numbers and sounds (under a minute)
EXPLAINER_TTS=silent python tools/build.py music40 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music40 --sync                         # the sound gates
python tools/dead_air.py renders/music40_480p.mp4 --sound music40  # no empty screen; no sound over a still one
python tools/lecture_length.py music40                          # 30 to 60 minutes, listening included
python tools/build.py music40                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 40                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** For the kick model, how long until it falls 60 dB at a decay setting of 0.45 s?

   *Solution.* The amplitude falls as e^(−t/τ); 60 dB is a factor of 1000, so t = τ ln 1000 = 0.45 × 6.91 ≈ 3.1 s. The
   lab prints it for any decay.

2. **Prove.** Prove that a sidechain ducking D dB with release time τ is back within 1 dB after τ ln D seconds.

   *Solution.* After the attack the gain in decibels is −D e^(−t/τ). It is within 1 dB of full level when D e^(−t/τ) ≤ 1,
   that is when t ≥ τ ln D. For 14 dB and τ = 0.18 s, 0.18 × ln 14 ≈ 0.48 s.

3. **Ear.** The lab plays pads under a kick, some sidechained; say which, and how deep.

   *Solution.* The lab prints the depths. At 6 dB the pump is a gentle breathing; at 12 to 18 dB the pad nearly
   disappears on each kick and swells back between them.

4. **Build.** Write a verse of your own on the sixteenth grid and measure its flow.

   *Where to look.* List (syllable, accented, sixteenth, rhyme class) as in `compute.VERSE_RAP_TEXT` and `rap_layout`,
   then call `song.flow`: compare the share on the beat and the gaps between accents for two placements of the same
   words.

5. ★ **Do new platforms change how songs are written, or only which songs win?**

   *Where the frontier is.* Build a corpus of hits with release dates, platform histories and audio; measure intro length,
   time to the hook, song length and repetition year by year; compare songs that spread on short-video platforms with
   those that did not, before and after; separate the composer's choice from the market's selection.

## Sources

* D. Temperley, *The Musical Language of Rock* (2018) and "The melodic-harmonic 'divorce' in rock", *Popular Music*
  (2007); J. Covach and A. Flory, *What's That Sound?* (5th ed., 2018).
* H. Léveillé Gauvin, "Drawing listener attention in popular music: testing five musical features arising from the
  theory of attention economy", *Musicae Scientiae* (2018).
* M. Mauch, R. M. MacCallum, M. Levy and A. M. Leroi, "The evolution of popular music: USA 1960–2010", *Royal Society
  Open Science* (2015); J. Serrà, Á. Corral, M. Boguñá, M. Haro and J. L. Arcos, "Measuring the evolution of
  contemporary western popular music", *Scientific Reports* (2012).
* M. Ohriner, *Flow: The Rhythmic Voice in Rap Music* (2019); A. Krims, *Rap Music and the Poetics of Identity* (2000);
  K. Adams, "On the metrical techniques of flow in rap music", *Music Theory Online* (2009).
* K. Jakubowski, S. Finkel, L. Stewart and D. Müllensiefen, "Dissecting an earworm: melodic features and song
  popularity predict involuntary musical imagery", *Psychology of Aesthetics, Creativity, and the Arts* (2017).
* J. Seabrook, *The Song Machine* (2015); A. Danielsen, *Presence and Pleasure: The Funk Grooves of James Brown and
  Parliament* (2006).
* Part 9 for membranes; Part 21 for form; Part 37 for interlocking; Part 38 for swing and the blues.
* W. Everett, *The Foundations of Rock* (2009); A. F. Moore, *Song Means: Analysing and Interpreting Recorded Popular Song* (2012); R. Middleton, *Studying Popular Music* (1990).

## Interpretation limits

Chart trends describe the cited US samples, not all popular music or proof that streaming caused shorter intros. A stream-count threshold does not define a universal payment rule. Loops can retain tonic goals, and non-chord tones require contextual analysis. Distortion depends on tuning, register and the transfer curve; full chords remain usable. The 808 voices are simplified models, with exponential time constants rather than fixed settling deadlines. Prosody and flow use chosen grid and stress proxies, not universal judgments. Recording and composition rights differ; sampling exceptions and court holdings vary by jurisdiction. Replaying does not automatically remove composition rights.
