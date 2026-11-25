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
    run(["ffmpeg", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(picture_list),
         "-f", "concat", "-safe", "0", "-i", str(audio_list), "-map", "0:v:0", "-map", "1:a:0",
         "-c:v", "copy", "-c:a", "aac", str(final)])
    probe = run(["ffprobe", "-v", "error", "-show_streams", "-of", "json", str(final)])
    picture, audio = json.loads(probe.stdout)["streams"]
    assert picture["avg_frame_rate"] == "60/1"
    assert int(picture["nb_frames"]) == 186
    assert picture_duration(final) == Fraction(186, 60)
    assert (audio["sample_rate"], audio["channels"]) == ("48000", 2)
    assert audio["duration_ts"] == 148800
