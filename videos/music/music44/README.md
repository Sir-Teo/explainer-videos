# Music, Built: Part 44, Music for Picture and Play

Part 44 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the last part of Act VII, *The Craft*. One animated scene, three scores, three different
films. Then a problem film composers never had: in a game nobody knows how long the scene will last. This part works the
arithmetic of hitting a cut on the beat and builds a score that rearranges itself. The tools are Monochord's
(`explainer/music/monochord/screen.py`). Every scene, cue, game and score is ours; film and game scores are described,
never played. Published findings are the ones listed under Sources.

* **One scene, two cuts.** An ear-and-eye question (the same score cut to the picture and 0.6 s late: which fits?); a
  short history (cue sheets, Vitaphone); music for picture and play; the plan.
* **1. What music does to an image.** Boltz's experiment; one scene, three scores (comic, suspense, heroic), heard; what
  film music does; Mickey-Mousing; source and score.
* **2. Leitmotifs.** From Wagner to Hollywood; Part 42's motive in three moods, heard; what the transformations keep;
  motives in games; motives on screen (described).
* **3. Spotting and hit points.** Spotting; a cue sheet for our scene; an ear-and-eye question (a door slam 120 ms
  early, in sync, late); the tolerance of sync (about 45 ms early, 125 ms late); the click track's arithmetic.
* **4. A tempo that hits three actions.** The problem; the worst miss for every tempo from 70 to 160 (two solutions:
  88.28 on beats 4, 11 and 16, and 153.69; eight with half-beats); the beats under the scene, heard; the rounding trap
  (the 16-2 click drifts 1.6 frames); other ways to hit; a variable click, heard; the temp track.
* **5. Harmony on screen.** Lehman's Hollywood harmony; four progressions, heard (C–A♭–C, C–E–C, D/C, C–Fm–C); why they
  work; genre codes.
* **6. Music under dialogue.** The voice comes first; music ducked 10 dB under a model voice, heard (the voice gains 6
  dB in the speech band); the duck drawn; loudness standards; writing for the mix.
* **7. Music for play.** From loops to systems (*Space Invaders*, iMUSE); the techniques; our score as a state machine;
  one change heard switching at once and at the bar line; what makes it work.
* **8. An adaptive score, played.** 48 seconds of a simulated game and its score, heard; what waiting for a boundary
  costs (0.25, 1.0 and 2.0 s on average for beat, bar and phrase, half the boundary as theory says); testing a score
  you cannot hear whole; responsive or musical?
* **9. Music under hardware limits.** Sound chips; one pulse at three duty cycles, heard, with its missing harmonics; the
  noise channel's shift register, heard; an ear question (a chord on three channels or one?); the Tune on the chip;
  after the chips; limits as a style.
* **10. Frontier: scores that compose themselves.** Generative and adaptive scoring; the cognition of film and game music;
  ★ research problem: which transition rule best balances responsiveness and coherence for players?
* **Variation 44, recap and problems.** The Tune as a cue whose 14 beats land on a hit at 9.0 s (98.8 bpm, a 14-5
  click), as a leitmotif in three moods, and as an adaptive loop gaining a layer each pass; the ledger; what we found;
  five problems; where it comes back; in practice; references; Part 45.

## What is computed, and what is heard

`python -m videos.music.music44.compute` (under a minute) fills `.cache/music44/`.

| Item | What it computes | Checked against |
|---|---|---|
| `scene`, `hook`, `three` | the hit points, the tempo finder, the rounded and variable clicks; the scene's scores | every hit within a frame; the variable click lands exactly (tests) |
| `sync` | three door slams | — |
| `motif`, `harmony` | a leitmotif in three moods; four progressions | — |
| `mix` | ducking under a model voice; the speech-band ratio | the ratio improves (tests) |
| `game`, `switch`, `quantise` | a simulated game, its adaptive score, transition delays over 200 games | mean delay = boundary / 2 (tests) |
| `duty`, `noise`, `arp`, `chip` | the chip's pulse, noise, arpeggio; the Tune on the chip | missing harmonics; 4-bit triangle (tests) |
| `tune`, `variation` | Variation 44 | the cue lands on its hit (tests) |

Monochord's tools are held in `tests/music/test_screen.py`; this part's claims and clips in `tests/music/test_music44.py`.

**Sounds.** Part 7's piano and Part 38's plucked bass (physical models), Part 41's additive orchestra, Part 40's drums,
Part 17's model voice (it sings vowels, not words) and a sound chip of ours. Clips that mix the additive orchestra or the
chip in are labelled `synthesized`. There are no recordings.

**What the models are, and are not.** *The scene* is a cartoon of ours, its music written to its hit points. *The sync
tolerances* are the ITU's broadcast figures. *The game* is a four-state simulation, not a real game; *the adaptive score*
is a small system of ours in the manner of middleware. *The chip* is our own design in the manner of 1980s chips, not
an emulation of any of them.

## Build

```bash
python -m videos.music.music44.compute                          # numbers and sounds (under a minute)
EXPLAINER_TTS=silent python tools/build.py music44 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music44 --sync                         # the sound gates
python tools/dead_air.py renders/music44_480p.mp4 --sound music44  # no empty screen; no sound over a still one
python tools/lecture_length.py music44                          # 30 to 60 minutes, listening included
python tools/build.py music44                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 44                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** A hit falls 9.5 s after a cue's downbeat. Which tempos between 100 and 130 put it on a beat?

   *Solution.* The hit falls on beat 9.5 × tempo / 60, so the tempo must be 60n / 9.5 for a whole number n: n = 16, 17,
   18, 19 and 20 give 101.05, 107.37, 113.68, 120.00 and 126.32 beats a minute. 120 is the easy one: 19 beats, a 12-0
   click.

2. **Prove.** Prove that waiting for the next boundary of length u delays a randomly timed event by u/2 on average.

   *Solution.* If the event's position within the boundary interval is uniform on [0, u), the wait is u minus that
   position, also uniform on (0, u], whose mean is u/2. The 200 simulated games give 0.25, 1.01 and 1.99 s for 0.5, 2 and
   4 s boundaries.

3. **Ear.** The lab plays door slams with random offsets; say early, in sync or late.

   *Solution.* The lab prints them. Two clicks set a pulse and the slam should land on the third: a slam 120 ms early
   jumps ahead of the pulse, one 120 ms late drags; early is usually the easier to hear.

4. **Build.** Add a state ("stealth") to the adaptive score, with its own segment and layers.

   *Where to look.* Add the state to `screen.simulate`'s transitions and intensity levels, and a chord loop for it in
   `STATE_C` in `videos/music/music44/compute.py`; then `adapt` and `render_game` handle it. Give it a thin texture and a
   quiet pulse, and a stinger that differs from combat's.

5. ★ **Which transition rule best balances responsiveness and coherence for players?**

   *Where the frontier is.* Build one game with several transition rules; have players play each; log play, enjoyment and
   every moment the music contradicts the game; model enjoyment against delay and the count of mid-phrase cuts.

## Sources

* F. Karlin and R. Wright, *On the Track* (2nd ed., 2004); F. Lehman, *Hollywood Harmony* (2018); K. Collins, *Game
  Sound* (2008) and (ed.) *From Pac-Man to Pop Music* (2008).
* M. G. Boltz, "Musical soundtracks as a schematic influence on the cognitive processing of filmed events", *Music
  Perception* (2001); A. J. Cohen, "Congruence-association model of music and multimedia" (2013).
* ITU-R BT.1359, "Relative timing of sound and vision for broadcasting" (1998); EBU R 128, loudness normalisation.
* M. Z. Land and P. N. McConnell, the iMUSE patent, US 5,315,057 (1994).
* B. Eno and others on generative music for *Spore* (2008); the procedural soundtrack of *No Man's Sky* (2016).
* C. Gorbman, *Unheard Melodies: Narrative Film Music* (1987), the principles of the classical score in chapter 1.
* M. Chion, *Audio-Vision: Sound on Screen* (1990; tr. C. Gorbman, 1994): added value and synchresis, chapter 1.

## Interpretation limits

Frame arithmetic uses 24 fps for this example; actual formats vary. Synchrony windows and tempo-change detection depend on content, task and listeners. Chromatic-mediant associations describe a film-scoring tradition, not fixed chord emotions. EBU R 128 uses integrated programme loudness, distinct from particular dialogue-gated specifications. Adaptive transition delay averages half a boundary only for uniform event phases. Layer compatibility rules are choices of this simple engine, not universal requirements. The vowel-only dialogue demonstrates band energy and ducking, not measured word intelligibility.
