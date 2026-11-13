# Writing a part of *Music, Built*: the working guide

[SYLLABUS.md](SYLLABUS.md) says what each part covers and the standard it meets. This file says how a part gets
made, with the lessons of the pilot (Part 1, *One String*). Read Part 1's code (`videos/music/music1/`) next to it:
it is the reference. Everything in [`videos/ai/LECTURE_GUIDE.md`](../ai/LECTURE_GUIDE.md) about chapters, numbers
and claims holds here too; this file is about what is different when a film has sound of its own.

## Layout of a part

```
videos/music/musicN/
  manifest.py     TITLE and SCENES = [(module, Scene class, chapter title)], film order
  compute.py      every number and every sound: CACHE = Cache("musicN"), CLIPS = ClipStore("musicN"),
                  one compute_<item>() per experiment, ITEMS = {...}
  common.py       PART = N, colours, load / clip (cached results and clips), small drawing helpers
  sNN_<name>.py   one chapter per module, one SoundScene class each
  README.md       chapters, what was computed, the sounds and their rights, problems with solutions, sources
videos/music/course/parts_AA_BB.py     the part's row in the course table
videos/music/labs/labNN.py             the part's lab (numpy/scipy and Monochord; writes a .wav you can play)
videos/music/course/site/widgets/*.js  the part's interactive (it must make sound)
tests/music/test_musicN.py             the film's claims, and the rules every clip keeps
```

Monochord, the instrument, is `explainer/music/monochord/` and never imports manim. The scene tools are
`explainer/music/` (`sound.py`: `SoundScene`, `SoundTracker`; `viz.py`: `StringView`, `Lens`, `Scope`,
`partial_bars`, `Spectrogram`, `MonochordView`; `__init__.py`: the chapter card, the Chain, the timeline, the
series map, the listening tag and the ledger of variations).

## Order of work

1. **`compute.py` first, complete, with its checks.** A sound is a result. Write the experiment, save the numbers
   in the cache and the clips in the clip store, and assert the physics before any scene exists.
2. **Look at every clip.** The author of this series cannot hear. Each clip is judged by a spectrogram image, its
   measured pitch and partials, its loudness and true peak, and by agreement with an independent route to the same
   signal (Part 1: beads against d'Alembert's formula against the modal sum; the bridge force against the Fourier
   series of a rectangular wave). A clip that has not been measured is not played.
3. **Scenes**, one at a time, each rendered with `tools/qa_scene.py` and read on its contact sheet.
4. **The full silent build**, then the gates (below), then the README, course row, lab, interactive and tests.

## Sound

- **One loudness.** `Clip.at_level(EXAMPLE_LEVEL)` sets the *loudest 400 ms* (BS.1770 momentary), not the
  integrated loudness: a pluck and a held chord set to the same integrated level are not equally loud, and the
  pluck clips. Peaky sources need a part-wide offset (Part 1 plays 2.5 dB under `EXAMPLE_LEVEL` because a string
  plucked near its end is nearly an impulse train). `tests/music/test_musicN.py` holds every clip between −24 and
  −15 LUFS momentary and under −1.5 dBTP.
- **Nothing is normalized after the fact.** The build mixes the music stem with a fixed gain and checks the
  true-peak ceiling; it does not limit. If the ceiling fails, lower the clip in `compute.py`.
- **Comparisons are honest.** Two clips the viewer is asked to compare keep their computed relative level (save
  them with one gain from one `mix` or one `concat`), unless the comparison is about something other than level,
  in which case both are set to the same level and the narration says so.
- **Every clip carries a label** (`physical model` or `synthesized`; later `sampled`, `recorded for this series`),
  shown in the corner while it plays (`window(snd, ...)` in `common.py` puts up the tag and the listening bar).
- **Narration never talks over an example.** `with self.listen(clip) as snd:` opens a window with no narration in
  it; a clip under narration is an underscore (`self.sound(clip, underscore=True)`) and must sit 12 dB or more
  under the voice. Keep underscores rare.

## Picture

- **Everything you hear, you see, on the clip's clock.** Inside a window, drive the picture from the sound:
  `snd.drive(mob, lambda m, t: ...)` gives each mobject the time elapsed in the clip. Do not animate with
  `self.play(..., run_time=clip.duration)` and hope: updaters accumulate their own `dt`, so the picture stays with
  the sound whatever else the scene does. `tools/qa_sound.py --sync` measures it on the stitched film; the
  tolerance is one frame.
- **A sound never plays over a still screen.** `tools/dead_air.py <film> --sound musicN` fails a window in which
  the picture is empty or does not move for 2.5 s. A ringing string needs something that rings with it: a `Lens`
  whose amplitude follows the clip's envelope, a playhead on a `Spectrogram`, partial bars that decay.
- **Slow motion is labelled.** A string at 131 Hz cannot be filmed at 60 frames a second. Show the motion slowed
  (`film(view, frames, ...)`), say by how much, and play the sound at its true speed.
- **A string's displacement is exaggerated** and the screen says so once, where the instrument first appears.
- The dark-screen rules of the other series hold: something on screen from the first word; no lone card for
  fifteen seconds; move a group before taking coordinates from it (a `Lens` built on a bench that is then shifted
  draws at the old place); a `Spectrogram` is a `Group`, so anything that contains one is a `Group`;
  `always_redraw` must return the same kind of mobject every frame.

## Numbers that went wrong in the pilot, and the rule each one left

- **A pickup at a quarter of the string hears no fourth or eighth partial.** Observation points sit at an
  irrational-looking fraction (0.2371) unless the node is the point.
- **An initial condition must respect the boundary.** A "pulse travelling right" built as a single odd-periodic
  wave let an image pulse walk in from the fixed end. Build travelling waves as `P(x − ct) − P(−x − ct)` with `P`
  of period `2L`, and assert that the ends stay still.
- **Autocorrelation pitch estimates are biased by cents on bright tones** unless the lag is refined
  (`f0_autocorr` upsamples eight times and takes the first strong peak, not the highest). Any claim finer than
  ten cents is measured two ways.
- **A partial measured over a window has already decayed inside it.** Compare a measured spectrum with a formula
  only after putting the same decay into the formula.
- **An estimate is narrated as an estimate.** The pitch glide of a hard pluck is 73 cents; the textbook estimate
  from the mean tension gives 65. The film shows both and says why they differ.

## Length

The plan gave Part 1 about 45 minutes; the first draft ran 62. A part is 30 to 60 minutes *including* its
listening windows and pauses (`tools/lecture_length.py musicN` counts them and fails above 60). Budget before
writing: at 140 words a minute, twelve to fourteen chapters of 450 to 520 words, three to four minutes of
listening, and no chapter over four and a half minutes. When a part runs long, cut a worked example whose result
the lab already has, not a derivation step.

## The ear thread, the Tune, the Chain

- Each part has at least two pause-and-listen moments where the viewer commits to an answer before the picture
  gives it (Part 1: which interval is this, by stopping the string; which pluck position, from the missing
  partials).
- The last chapter plays the part's variation on the Tune, built only from what the part has made, over the
  ledger of variations (`variations_ledger`). Its clip is `variation.<name>` in the part's clip store and its
  notes are checked in the tests.
- Each chapter card lights the links of the Chain the chapter touches and the years it visits on the timeline.

## Gates

```
python -m videos.music.musicN.compute                       # numbers and clips
EXPLAINER_TTS=silent python tools/build.py musicN -q l --fps 15 -j 3
python tools/qa_sound.py musicN --sync                      # overlap, labels, peaks, levels, phone audition, sync
python tools/dead_air.py renders/musicN_480p.mp4 --sound musicN
python tools/lecture_length.py musicN                       # 30 to 60 minutes, listening included
python tools/check_course.py music N                        # course row, lab, interactive (in a browser)
python -m pytest -q tests/music
```

## Rights

Only two kinds of sound are played: what Monochord computes, and (from Part 10 on) the series' own renderings of
public-domain scores. No recording made by anyone else is played, however short. A part's README lists every clip
family and where it came from.
