# Music, Built: the sound check

A two-minute test film for the series' sound pipeline (`videos/music/SYLLABUS.md` §3). It is not a part of the course.
It plays every kind of cue once: narration, a listening window with a playhead, events timed like bookmarks, a picture
driven by the clip's own clock, stereo, three levels, and five clicks with a square that lights on each.

```bash
python -m videos.music.soundcheck.compute            # the clips, into .cache/soundcheck/audio/
EXPLAINER_TTS=silent python tools/build.py soundcheck -q l --fps 15
python tools/qa_sound.py soundcheck --sync           # the sound gates, and picture-to-sound sync on the clicks
```

`qa_sound.py --sync` decodes the stitched film and reports, for each click, when it sounds and when its frame lights.
The offset must be under one frame. Run it after any change to `explainer/music/sound.py`, to the music path of
`tools/build.py`, or to manim.
