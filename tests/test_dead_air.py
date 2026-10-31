import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class DeadAirTests(unittest.TestCase):
    def test_bad_video_cannot_be_reported_as_zero_blank_frames(self):
        with tempfile.TemporaryDirectory() as directory:
            video = Path(directory) / "broken.mp4"
            video.write_text("not a video")
            process = subprocess.run([sys.executable, str(Path(__file__).resolve().parents[1] / "tools/dead_air.py"),
                                      str(video)], capture_output=True, text=True)
        self.assertNotEqual(process.returncode, 0)
        self.assertIn("dead-air QA did not run", process.stderr)


if __name__ == "__main__":
    unittest.main()
