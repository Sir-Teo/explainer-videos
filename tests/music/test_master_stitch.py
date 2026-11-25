"""Picture and narration keep the same clock across AAC scene boundaries."""
import json
from fractions import Fraction
import shutil

import pytest

from tools.build import concat_file, normalize_master_audio, picture_duration, run


@pytest.mark.skipif(not (shutil.which("ffmpeg") and shutil.which("ffprobe")), reason="requires FFmpeg tools")
def test_concat_uses_picture_duration_for_both_tracks(tmp_path):
    pictures, soundtracks = [], []
    for index, frames in enumerate((61, 62, 63)):
        scene = tmp_path / f"chapter '{index}'.mp4"
        audio = scene.with_suffix(".m4a")
        # AAC extends beyond each picture. There is a fractional millisecond at
        # two of the joins, and the path exercises ffconcat's quoting rules.
        run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "color=black:s=128x72:r=60:d=2",
             "-f", "lavfi", "-i", "sine=frequency=440:duration=1.4",
             "-frames:v", str(frames), "-c:v", "libx264", "-c:a", "aac", str(scene)])
        duration = picture_duration(scene)
        assert duration == Fraction(frames, 60)
        normalize_master_audio(scene, audio, duration)
        pictures.append((scene, duration))
        soundtracks.append((audio, duration))

    picture_list = concat_file(tmp_path / "picture.txt", pictures)
    audio_list = concat_file(tmp_path / "audio.txt", soundtracks)
    final = tmp_path / "master.mp4"
    run(["ffmpeg", "-v", "error", "-copyts", "-f", "concat", "-safe", "0", "-i", str(picture_list),
         "-f", "concat", "-safe", "0", "-i", str(audio_list), "-map", "0:v:0", "-map", "1:a:0",
         "-c:v", "copy", "-video_track_timescale", "60", "-movie_timescale", "1000", "-c:a", "aac", str(final)])
    probe = run(["ffprobe", "-v", "error", "-show_streams", "-of", "json", str(final)])
    picture, audio = json.loads(probe.stdout)["streams"]
    from tools.music_render import check_picture_clock

    check_picture_clock(final, picture, tmp_path / "verify.log")
    assert picture["avg_frame_rate"] == "60/1"
    assert int(picture["nb_frames"]) == 186
    assert picture_duration(final) == Fraction(186, 60)
    assert (audio["sample_rate"], audio["channels"]) == ("48000", 2)
    assert audio["duration_ts"] == 148800


def test_sparse_music_stem_matches_dense_mix(tmp_path):
    import numpy as np
    from explainer.music.monochord.audio import Clip, SR, mix
    from tools.build import music_stem

    rng = np.random.default_rng(763)
    mono = Clip(rng.normal(0, .1, SR + 7))
    stereo = Clip(rng.normal(0, .1, (SR // 2, 2)))
    seconds = 5.1
    cues, placed = [], []
    for i, (clip, start, gain) in enumerate(((mono, 2.8, -2.7), (stereo, -.17, 2.2), (mono, 2.5, .3),
                                              (stereo, 2.8, -6), (mono, 4.95, 0), (mono, 7, -3))):
        path = tmp_path / f"clip-{i}.wav"
        clip.write(path)
        cues.append({"path": path, "start": start, "gain_db": gain})
        placed.append((Clip(clip.stereo), start, gain))
    for items, clips in ((cues, placed), ([], [])):
        dest = tmp_path / "sparse.wav"
        music_stem(items, seconds, dest)
        reference = tmp_path / "dense.wav"
        mix(clips, duration=seconds).write(reference)
        assert dest.read_bytes() == reference.read_bytes()


def test_probe_diagnostics_stay_out_of_json(tmp_path):
    import sys
    from tools.music_render import run_step

    log = tmp_path / "queue.log"
    source = 'import sys; print("mux diagnostic", file=sys.stderr); print("{\\"frames\\": 60}")'
    data = run_step(log, sys.executable, "-c", source, capture="stdout")
    assert json.loads(data) == {"frames": 60}
    assert "mux diagnostic" in log.read_text()


def test_queue_renders_next_part_during_mastering_and_reports_failure(tmp_path, monkeypatch):
    import sys
    from threading import Event
    from tools import music_render as queue

    first_master, next_scenes = Event(), Event()
    finished = []

    def run_step(log, *cmd):
        if "music2" in cmd and "--scenes-only" in cmd:
            assert first_master.wait(5)
            next_scenes.set()

    def finish(video, build, clean):
        if video == "music1":
            first_master.set()
            assert next_scenes.wait(5)
        finished.append(video)
        return video == "music2"

    monkeypatch.setattr(queue, "run_step", run_step)
    monkeypatch.setattr(queue, "finish_part", finish)
    monkeypatch.setattr(queue, "STATE", tmp_path / "state")
    monkeypatch.setattr(queue, "OUTPUT", tmp_path / "masters")
    monkeypatch.setattr(queue, "free_space", lambda: 20 * 1024**3)
    monkeypatch.setattr(queue, "available_parts", lambda: [1, 2])
    monkeypatch.setenv("EXPLAINER_TTS", "server")
    monkeypatch.setattr(sys, "argv", ["music_render.py", "--clean"])
    assert queue.main() == 1
    assert finished == ["music1", "music2"]
