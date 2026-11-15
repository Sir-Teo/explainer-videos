# Music, Built: Part 56, Recording and Mixing

Part 56 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the third part of Act X, *The Studio and the Stage*. Take one multitrack recording and mix
it three times: close and dry, a wall of sound, a dub. It is three different pieces of music. Since the 1960s the studio
has been an instrument, and this part learns to play it, with a session band built from earlier parts: Part 8's voice,
Part 38's piano, guitar and bass, and Part 40's drums, nine tracks of the Tune. The tools are Monochord's
(`explainer/music/monochord/studio.py`); every microphone, room, console and loudspeaker is simulated. Several sounds are
rendered for headphones.

* **Three mixes of one recording.** An ear question (the session mixed as a wall of sound, a dub and close and dry: which
  was the dub? the second); what each did (crest factor 11 dB in the wall against 18 dry); Les Paul, Spector, King Tubby
  and Eno; the session; the plan.
* **1. From the horn to the workstation.** Tracks against years (one in 1877, eight in 1957, 24 by 1974, hundreds now);
  tape and the razor blade; bouncing; the workstation.
* **2. Stereo microphone pairs.** Five pairs (XY, Blumlein, ORTF, NOS, AB); the level and time differences each makes;
  where the images fall, by a trading rule (15 dB or 1.1 ms to a loudspeaker), and the recording angles (Blumlein 70°,
  AB 78°, ORTF 109°, XY beyond 180°); one stage through three pairs, heard; choosing a pair.
* **3. Phase between microphones.** One source, two microphones; the comb (5.8 ms apart: notches from 86 Hz); the 3 : 1
  rule (+2.5 and −3.5 dB); a snare from both sides; an ear question (which snare was left as recorded? the second, its
  body 6 dB weaker); putting it right.
* **4. Gain staging.** From the air to the converter; three gains in dBFS (too low: 54 dB of range; right: 73 dB with 16 dB
  of headroom; too hot: 8 dB past full scale); heard; twenty-four bits and floating point; reference levels.
* **5. Editing.** Takes and comps; why a cut clicks (our splice jumps by half the voice's swing in one sample); a splice
  and a crossfade, heard; crossfade laws for related and unrelated material; time and pitch.
* **6. Balance and panning.** One channel of a console; faders; four pan laws; stereo against mono (the −3 dB law's centre
  3 dB louder in mono, the −6 dB law's 3 dB quieter in stereo); our faders and pans.
* **7. Masking between tracks.** One track hides another; a masking map (an ideal binary mask, band by band, left and right
  apart); our session's map, rough and carved (the guitar from 49 to 35 per cent masked, the voice from 9 to 4); the
  carving; heard; what the map teaches.
* **8. Dynamics and buses.** A compressor on the voice (its level's wander from 12.7 to 4.8 dB); parallel compression (the
  drums' spread from 37 to 32 dB); heard; buses and side-chains; automation.
* **9. Depth and width.** Cues for depth; one voice at three distances (direct-to-reverberant +36, +14 and +6 dB); heard;
  mid-side and the Haas trick (correlation 0.09; notches from 42 Hz every 83 Hz in mono); a widened guitar in stereo and in
  mono, heard.
* **10. Monitoring.** The mixing room; how loud to listen; a phone's loudspeaker (the bass's fundamentals 40 dB and more
  down, 29 per cent of its energy above 844 Hz); one mix, two playbacks, heard; checking a mix.
* **11. Frontier: automatic mixing.** Machines that mix, from Dugan's automixer to differentiable consoles; Monochord's four
  rules; an ear question (which was the machine? the second, its hi-hat 8 dB too loud); the two mixes setting by setting
  (the machine's masking numbers look fine; its bass is buried); differentiable consoles; ★ research problem: is there an
  objective, other than imitation, that predicts which mix listeners prefer?
* **Variation 56, recap and problems.** The session's first three phrases mixed close and dry, as a wall of sound and as a
  dub; the ledger (crest factor 18 dB dry, 11 in the wall; the dub's echo every 0.45 s); what we found; five problems;
  where it comes back; in practice; references; Part 57.

## What is computed, and what is heard

`python -m videos.music.music56.compute` (under a minute) fills `.cache/music56/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook`, `tune56` | the session (nine tracks) and three mixes through Monochord's console | crest factors and correlations (tests) |
| `history` | tracks against years | — |
| `arrays` | five stereo pairs' cues, image positions and recording angles; one stage through three pairs | symmetry; the delays (tests) |
| `phase` | the comb of two microphones; a snare's two microphones in and out of polarity | the comb's closed form (tests) |
| `gain` | levels and noise from the air to a 16-bit converter at three gains | dBu arithmetic (tests) |
| `edit` | a butt splice and a crossfade; crossfade laws | constant amplitude and power (tests) |
| `pan` | four pan laws in stereo and in mono | −3.01 and +3.01 dB (tests) |
| `masking` | the masking map, rough and carved | a masked tone; panning unmasks (tests) |
| `dynamics`, `depth`, `monitor` | a vocal compressor, parallel compression; depth and width; Part 54's phone | correlation and mono loss (tests) |
| `automix` | a rule-based automatic mix against ours | the rules (tests) |

Monochord's tools are held in `tests/music/test_studio.py`; this part's claims and clips in `tests/music/test_music56.py`.

**Sounds.** Part 8's voice, Part 38's piano, guitar and bass, Part 40's kick, snare and hi-hat, recorded by simulated close
microphones and an ORTF room pair, and mixed on Monochord's console.

**What the models are, and are not.** *The session* is played by models, not musicians; the close microphones hear only
their own instrument (no spill) except in the snare's two microphones. *The image rule* is a linear trading of level and
time differences, a rule of thumb from Simonsen's and Williams's work; more careful charts differ by up to about ten
degrees. *The masking map* is an ideal binary mask on 24 ERB-spaced bands, a stand-in for partial loudness, not a model of
it. *The converter* adds white noise at its floor and rounds to 16 bits. *The automatic mixer* is four stated rules, not a
learned model.

## Build

```bash
python -m videos.music.music56.compute                          # numbers and sounds (under a minute)
EXPLAINER_TTS=silent python tools/build.py music56 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music56 --sync                         # the sound gates
python tools/dead_air.py renders/music56_480p.mp4 --sound music56  # no empty screen; no sound over a still one
python tools/lecture_length.py music56                          # 30 to 60 minutes, listening included
python tools/build.py music56                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 56                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** Two microphones hear a source from 0.5 m and 2 m. Find the delay, the first notch of their sum, and the
   comb's peak and dip.

   *Solution.* The delay is 1.5 / 343 = 4.37 ms, so the first notch is at 1 / (2 × 4.37 ms) = 114 Hz, and the others every
   229 Hz. The far microphone is four times as far, so by the inverse square law it hears g = 1/4 of the pressure: the
   peaks are 20 log₁₀(1.25) = +1.9 dB and the dips 20 log₁₀(0.75) = −2.5 dB.

2. **Prove.** Prove that the −3 dB pan law keeps stereo power constant, and that its centre is 3 dB louder in mono than a
   hard pan.

   *Solution.* g_L = cos φ and g_R = sin φ with φ = π(p + 1)/4, so g_L² + g_R² = 1 for every p. In mono the channels add:
   (g_L + g_R)/2 is 1/2 for a hard pan (φ = 0) and (√2/2 + √2/2)/2 = √2/2 at the centre (φ = π/4); their ratio is √2,
   +3.01 dB.

3. **Ear.** The lab mixes a voice-like tone at random depths in front of a band; order them, near to far.

   *Solution.* The lab prints them. Listen for the reverberation's share first, then the level: the far ones are wetter
   and quieter, and their attacks are softened by the tail.

4. **Build.** Give the automatic mixer a rule that reads the masking map, and see whether the bass comes back.

   *Where to look.* After the loudness and panning rules, compute `studio.masking_map` on the stems; for the most masked
   track, find its most masked band and cut that band by a few decibels on whichever other track contributes most energy
   there; repeat until no track is more than, say, 30 per cent masked, or the cuts stop helping. Then listen: a mix can
   satisfy the map and still sound wrong, which is the point of problem 5.

5. ★ **Is there an objective, other than imitating a mix, that predicts which mix listeners prefer?**

   *Where the frontier is.* Collect multitracks with several engineers' mixes of each and listeners' blind preferences;
   fit a model of preference from measurable properties (loudness, masking, space, dynamics) and from learned features;
   optimize a differentiable console against it; and test the results blind against engineers.

## Sources

* R. Izhaki, *Mixing Audio* (3rd ed., 2018); M. Senior, *Mixing Secrets for the Small Studio* (2nd ed., 2018); B. Owsinski,
  *The Mixing Engineer's Handbook* (5th ed., 2022); G. Milner, *Perfecting Sound Forever* (2009).
* A. D. Blumlein, British patent 394,325 (1931); M. Williams, *Microphone Arrays for Stereo and Multichannel Sound
  Recording* (2004), with G. Simonsen's localization data (1984); H. Wittek and G. Theile,
  "The recording angle: based on localisation curves", AES Convention (2002).
* B. Eno, "The recording studio as a compositional tool" (lecture, 1979; *Down Beat*, 1983); M. Veal, *Dub: Soundscapes
  and Shattered Songs in Jamaican Reggae* (2007).
* H. Fletcher and W. A. Munson, "Loudness, its definition, measurement and calculation", *JASA* (1933).
* D. Dugan, "Automatic microphone mixing", *JAES* (1975); E. Perez-Gonzalez and J. D. Reiss, "Automatic gain and fader
  control for live mixing", IEEE WASPAA (2009); B. De Man, J. D. Reiss and R. Stables, "Ten years of automatic mixing",
  Workshop on Intelligent Music Production (2017); C. J. Steinmetz, J. Pons, S. Pascual and J. Serrà, "Automatic multitrack
  mixing with a differentiable mixing console of neural audio effects", ICASSP (2021).
* D. Wang, "On ideal binary mask as the computational goal of auditory scene analysis" (2005).
