"""Real tiny clips verify end-of-file and adaptive transition extraction."""

import shutil
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw

from tools.qa_motion import audit, extract


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg is required")
class TemporalAuditTests(unittest.TestCase):
    def test_equal_luminance_color_change_is_detected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            frames = root / "colors"
            frames.mkdir()
            red, green = (255, 0, 0), (0, 130, 0)
            # These have identical rounded BT.601 luminance. Verify that the
            # actual decoder's grayscale output would also miss this change.
            self.assertEqual(Image.new("RGB", (1, 1), red).convert("L").getpixel((0, 0)),
                             Image.new("RGB", (1, 1), green).convert("L").getpixel((0, 0)))
            for i in range(40):
                Image.new("RGB", (96, 64), red if i < 20 else green).save(frames / f"{i:03d}.png")
            clip = root / "colors.mkv"
            subprocess.run(["ffmpeg", "-v", "error", "-threads", "1", "-framerate", "10", "-i", str(frames / "%03d.png"),
                            "-c:v", "ffv1", "-threads", "1", "-pix_fmt", "bgr0", str(clip)], check=True)
            gray = subprocess.run(["ffmpeg", "-v", "error", "-threads", "1", "-i", str(clip), "-filter_threads", "1",
                                   "-vf", "format=gray", "-f", "rawvideo", "-"], check=True, capture_output=True).stdout
            pixels = 96 * 64
            self.assertLess(max(abs(a - b) for a, b in zip(gray[:pixels], gray[-pixels:])), 8)
            result = audit(clip, root / "audit", width=96)
            self.assertEqual(result["color_space"], "RGB24")
            self.assertEqual(len(result["tool_sha256"]), 64)
            self.assertEqual(len(result["motion_intervals"]), 1)
            selected = {f["source_frame"] for f in result["selected_frames"]}
            self.assertTrue({19, 20, 21} <= selected)

    def test_many_selected_frames_do_not_overflow_ffmpeg_expression_parser(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            clip = root / "many.mp4"
            subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "testsrc=size=32x24:rate=10:duration=24",
                            "-filter_threads", "1", "-c:v", "libx264", "-threads", "1", "-pix_fmt", "yuv420p",
                            str(clip)], check=True)
            selected = [{"source_frame": i, "time": i / 10} for i in range(240)]
            extract(clip, root / "frames", selected)
            self.assertEqual(len(list((root / "frames").glob("*.png"))), 240)
            self.assertEqual(selected[-1]["source_frame"], 239)

    def make_clip(self, root, moving):
        frames = root / "input"
        frames.mkdir()
        for i in range(40):
            image = Image.new("RGB", (96, 64), "black")
            if moving:
                x = 10 if i < 10 else min(i, 19) * 2 - 8
                ImageDraw.Draw(image).rectangle((x, 20, x + 15, 40), fill="white")
                if i == 30:
                    ImageDraw.Draw(image).rectangle((60, 5, 90, 15), fill="white")
            image.save(frames / f"{i:03d}.png")
        clip = root / "clip.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-threads", "1", "-framerate", "10", "-i", str(frames / "%03d.png"),
                        "-c:v", "libx264", "-threads", "1", "-pix_fmt", "yuv420p", str(clip)], check=True)
        return clip

    def test_transition_clusters_and_late_single_frame_flash_are_retained(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            result = audit(self.make_clip(root, True), root / "audit", width=96, dense=0.4)
            self.assertEqual(result["analysis"]["decoded_frames"], 40)
            self.assertAlmostEqual(result["last_decoded_time"], 3.9)
            self.assertEqual(len(result["motion_intervals"]), 2)
            selected = {f["source_frame"] for f in result["selected_frames"]}
            self.assertTrue({0, 9, 10, 19, 20, 29, 30, 31, 32, 39} <= selected)
            self.assertTrue(any("dense" in reason for f in result["selected_frames"] for reason in f["reasons"]))
            self.assertEqual(result["manual_frame_review"], "pending")
            self.assertEqual(result["continuous_perceptual_playback"], "unverified")
            for frame in result["selected_frames"]:
                with Image.open(root / "audit" / frame["file"]) as image:
                    self.assertEqual(image.size, (96, 64))

    def test_static_file_is_decoded_to_end_and_gets_a_static_midpoint(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            result = audit(self.make_clip(root, False), root / "audit", width=96)
            self.assertEqual(result["analysis"]["decoded_frames"], 40)
            self.assertFalse(result["motion_intervals"])
            self.assertEqual(len(result["selected_frames"]), 3)
            self.assertEqual(result["selected_frames"][-1]["source_frame"], 39)

    def test_invalid_input_cannot_produce_completed_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            clip = root / "broken.mp4"
            clip.write_bytes(b"not a video")
            with self.assertRaises(subprocess.CalledProcessError):
                audit(clip, root / "audit")
            self.assertEqual(json.loads((root / "audit" / "result.json").read_text())["status"], "failed")

    def test_failed_refresh_replaces_previous_completed_status(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            clip = self.make_clip(root, False)
            audit(clip, root / "audit", width=96)
            clip.write_bytes(b"broken refresh")
            with self.assertRaises(subprocess.CalledProcessError):
                audit(clip, root / "audit", width=96)
            self.assertEqual(json.loads((root / "audit" / "result.json").read_text())["status"], "failed")
