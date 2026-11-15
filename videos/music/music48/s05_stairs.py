from __future__ import annotations

import numpy as np

from videos.music.music48.common import *  # noqa: F403


class Stairs(SoundScene):
    def construct(self):
        chapter(self, 4, r"The stair-step myth", r"Does digital audio come out in steps?")
        self.myth()
        self.hold()
        self.images()
        self.hear()
        self.oversampled()

    # ------------------------------------------------------------------
    def myth(self):
        d = load("stairstep")
        fs = d["fs2"]
        n = np.array(d["n"])
        x = np.array(d["x"])
        ax = frame_axes(width=11.6, height=3.2, xlo=0, xhi=2.0, ylo=-1.3, yhi=1.3, center=DOWN * 0.3)
        pts = []
        for k, v in zip(n, x):
            pts += [ax.to(k / fs, v), ax.to(min((k + 1) / fs, 2.0), v)]
        stair = VMobject(stroke_color=EAR, stroke_width=3).set_points_as_corners(pts)
        tt = np.linspace(0, 2.0, 500)
        from explainer.music.monochord import digital as DG
        xx = np.array([d["x"]]).ravel()
        smooth = curve(tt, DG.sinc_interp(xx, fs, tt, taps=16), ax.to, color=WHITE, width=4)
        st = stems(n / fs, x, ax.to, color=TUNE)
        head = label(r"the picture in every advertisement", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Advertisements for high-resolution audio often draw digital sound as a staircase, <bookmark mark='a'/> each "
            "sample held flat until the next, with more samples making smaller steps. <bookmark mark='b'/> That is not what "
            "comes out of a converter. The samples are points, and what comes out is the one smooth curve through them that "
            "contains no frequency above the Nyquist frequency, the curve of the last chapter. The stair-step is a picture of "
            "a device, not of the sound."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(st))
            vo.wait_until("a")
            self.play(Create(stair), run_time=1.5)
            vo.wait_until("b")
            self.play(stair.animate.set_stroke(opacity=0.35), Create(smooth), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hold(self):
        items = [
            (r"a simple converter does hold each value for one sample period: \ a zero-order hold", WHITE),
            (r"the steps are made of high frequencies: \ copies of the music around 44.1, \ 88.2, \ 132.3 kHz", WHITE),
            (r"a low-pass reconstruction filter after the converter removes them, \ and the steps with them", WHITE),
            (r"what is left is the smooth curve, \ with a small dip at the top of the band to correct", TUNE),
            (r"the stairs never reach the loudspeaker", GREY_A),
        ]
        rows_scene(self, r"where the stairs go", items,
                   "There is a grain of truth in it. <bookmark mark='b'/> A simple converter does hold each value for one sample "
                   "period: a zero-order hold. <bookmark mark='c'/> But the steps are made of high frequencies: copies of the "
                   "music around 44.1, 88.2 and 132.3 kilohertz. <bookmark mark='d'/> A low-pass reconstruction filter after the "
                   "converter removes those copies, and the steps go with them. <bookmark mark='e'/> What is left is the smooth "
                   "curve, with a small dip at the top of the band to correct. <bookmark mark='f'/> The stairs never reach the "
                   "loudspeaker.", marks="bcdef")

    # ------------------------------------------------------------------
    def images(self):
        d = load("stairstep")
        fs = d["fs"]
        ax = frame_axes(width=11.0, height=3.0, xlo=0, xhi=100000, ylo=-60, yhi=5, center=DOWN * 0.4)
        f = np.linspace(1, 100000, 600)
        env = curve(f, np.maximum(20 * np.log10(np.abs(np.sinc(f / fs)) + 1e-6), -60), ax.to, color=GREY_A, width=2)
        lines = VGroup(Line(ax.to(1000, -60), ax.to(1000, 0), color=TUNE, stroke_width=5))
        tags = VGroup(label(r"1 kHz", font_size=16, color=TUNE).next_to(ax.to(1000, 0), UP, buff=0.1))
        for im in d["images"]:
            lines.add(Line(ax.to(im["hz"], -60), ax.to(im["hz"], im["db"]), color=EAR, stroke_width=4))
        for im in d["images"][::2]:
            tags.add(label(rf"{im['db']:.0f} dB", font_size=15, color=EAR).next_to(ax.to(im["hz"] + 1000, im["db"]), UP, buff=0.1))
        ticks = VGroup(*[label(f"{v // 1000} k", font_size=15, color=GREY_A).next_to(ax.to(v, -60), DOWN, buff=0.12) for v in (0, 22050, 44100, 88200)])
        dr = d["droop"]
        cap = label(rf"grey: \ the hold's response, \ $\mathrm{{sinc}}(f/f_s)$; \ at 20 kHz it is already {dr['20000']:.1f} dB", font_size=17, color=GREY_A).to_edge(DOWN, buff=0.4)
        head = label(r"a 1 kHz tone through a zero-order hold at 44.1 kHz", font_size=24, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Measure the staircase. A one-kilohertz tone held at forty-four point one kilohertz. <bookmark mark='a'/> The tone "
            "itself comes out at full strength. <bookmark mark='b'/> Its copies, the images, sit either side of every multiple "
            f"of the sample rate: around forty-four kilohertz they are about {say(-d['images'][0]['db'])} decibels down, around "
            f"eighty-eight about {say(-d['images'][2]['db'])}. They are the steps. <bookmark mark='c'/> The hold also tilts the "
            f"band itself: at twenty kilohertz it loses {say(-dr['20000'], 1)} decibels, which a converter's filter corrects."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(ticks), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]), FadeIn(tags[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1:]), FadeIn(tags[1:]))
            vo.wait_until("c")
            self.play(Create(env), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("stairs")
        c = clip("stairs.two")
        f = np.array(d["f"])
        def pan(key, title, col):
            ax = frame_axes(width=5.2, height=2.4, xlo=0, xhi=24000, ylo=-140, yhi=-20, center=ORIGIN)
            ticks = VGroup(*[label(f"{v // 1000} k", font_size=14, color=GREY_A).next_to(ax.to(v, -140), DOWN, buff=0.1) for v in (0, 4000, 8000, 16000, 24000)])
            return VGroup(ax, ticks, curve(f, np.clip(d[key], -140, -20), ax.to, color=col, width=2.5), label(title, font_size=18, color=col).next_to(ax, UP, buff=0.15))
        g = VGroup(pan("stair", r"held steps, \ no filter", EAR), pan("smooth", r"the smooth curve", TUNE)).arrange(RIGHT, buff=1.0).move_to(UP * 0.3)
        cap = label(rf"the Tune sampled at 8 kHz; \ the steps put {-d['image_db']:.0f} dB less energy above 4.5 kHz than in total, \ all of it images", font_size=16, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"the stairs, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "What would the stairs sound like if they did reach the loudspeaker? Here is the Tune sampled at eight kilohertz, "
            "where the effect is easy to hear: first played as held steps with no filter, then as the smooth curve. The steps "
            "add a metallic shimmer: the images, every copy of the music above four kilohertz."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(cap))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"steps, \ then smooth", kind="synthesized", detail=r"Part 7's piano, \ sampled at 8 kHz", corner=DL, tag_corner=DR)
            pulse(snd, g[0], st["first"], st["second"] - 0.4, buff=0.1)
            pulse(snd, g[1], st["second"], c.duration, buff=0.1)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def oversampled(self):
        items = [
            (r"modern converters first raise the rate digitally, \ 4, \ 8 or 64 times, \ with an exact interpolation filter", WHITE),
            (r"the images move far above hearing, \ so a gentle analogue filter can remove them", WHITE),
            (r"the droop is corrected in the digital filter", WHITE),
            (r"the result: \ the theorem's smooth curve, \ to within the converter's noise", TUNE),
            (r"more samples a second would not make the curve smoother; \ they would only widen the band", GREY_A),
        ]
        rows_scene(self, r"how converters really do it", items,
                   "How do modern converters really do it? <bookmark mark='b'/> They first raise the rate digitally, four, eight "
                   "or sixty-four times, with an accurate interpolation filter, <bookmark mark='c'/> so the images move far above "
                   "hearing and a gentle analogue filter can remove them. <bookmark mark='d'/> The droop is corrected in the "
                   "digital filter. <bookmark mark='e'/> The result is the theorem's smooth curve, to within the converter's "
                   "noise. <bookmark mark='f'/> More samples a second would not make the curve smoother; they would only widen "
                   "the band.", marks="bcdef")
