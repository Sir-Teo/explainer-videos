"""Run Manim with a frame-conversion fast path for H.264 renders."""
from __future__ import annotations

import runpy


def optimize_static_frames():
    # This uses private encoder fields, so activate only on the tested release.
    from manim import __version__

    if __version__ != "0.22.0":
        return
    import av
    if av.__version__ != "19.0.1":
        return
    from av.video.reformatter import VideoReformatter
    from manim.scene.video_segment_encoder import VideoSegmentEncoder

    original = VideoSegmentEncoder.write_frame

    def write_frame(self, pixels, *, repeat=1):
        if (self.spec.codec, self.spec.pixel_format) != ("libx264", "yuv420p"):
            return original(self, pixels, repeat=repeat)
        self._validate_frame(pixels, repeat)
        try:
            # Wrap the contiguous RGBA array, then convert immediately to an
            # independent frame. A static hold needs one conversion for the
            # entire run, with the original timestamp for every submission.
            if self._next_pts == 0:
                self._rgba_reformatter = VideoReformatter()
            rgba = av.VideoFrame.from_numpy_buffer(pixels, format="rgba")
            frame = self._rgba_reformatter.reformat(rgba, format="yuv420p")
            frame.time_base = 1 / self.spec.frame_rate
            for _ in range(repeat):
                frame.pts = self._next_pts
                self._next_pts += 1
                for packet in self._stream.encode(frame):
                    self._container.mux(packet)
        except BaseException as error:
            raise self._operation_error("encode", error) from error

    VideoSegmentEncoder.write_frame = write_frame


if __name__ == "__main__":
    optimize_static_frames()
    runpy.run_module("manim", run_name="__main__")
