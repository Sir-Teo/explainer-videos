from __future__ import annotations

import numpy as np

from videos.music.music57.common import *  # noqa: F403


class Meters(SoundScene):
    def construct(self):
        chapter(self, 2, r"Meters", r"What should a meter measure?")
        self.kinds()
        self.drum()
        self.weighting()
        self.tones()
        self.limits()

    # ------------------------------------------------------------------
    def kinds(self):
        items = [
            (r"a sample-peak meter: \ the largest sample; \ it says when the converter will clip, \ nothing about loudness", WHITE),
            (r"the VU meter \ (1939): \ a needle that averages over about 300 ms, \ roughly how loud speech and music seem", WHITE),
            (r"the peak programme meter \ (BBC, \ 1930s): \ rises in 10 ms, \ falls slowly; \ broadcasters' guard against overload", WHITE),
            (r"none of them hears like an ear: \ a deep bass and a bright tone at the same voltage are not equally loud \ (Part 4)", WHITE),
            (r"from 2006: \ ITU-R BS.1770, \ a meter built on listening tests", TUNE),
        ]
        rows_scene(self, r"three old meters", items,
                   "What should a meter measure? <bookmark mark='b'/> A sample-peak meter shows the largest sample. It flags sample overload, but cannot by itself rule out reconstructed inter-sample overload, and nothing about how loud anything is. <bookmark mark='c'/> The VU meter of 1939 is a needle that averages over about three hundred milliseconds, roughly how loud speech and music seem. <bookmark mark='d'/> The BBC's peak programme meter rises in ten milliseconds and falls slowly, a broadcaster's guard against overload. <bookmark mark='e'/> None of them hears like an ear: as Part 4 showed, a deep bass and a bright tone at the same voltage are not equally loud. <bookmark mark='f'/> From 2006 there is a meter built on listening tests: the ITU's BS.1770.", marks="bcdef")

    # ------------------------------------------------------------------
    def drum(self):
        d = load("meters")["drum"]
        t = np.array(d["t"])
        ax = frame_axes(width=10.0, height=1.4, xlo=0, xhi=t[-1], ylo=-1, yhi=1, center=UP * 1.2)
        wave = VMobject(stroke_color=GREY_B, stroke_width=1.5).set_points_as_corners([ax.to(x, v) for x, v in zip(t, d["wave"])])
        a2 = frame_axes(width=10.0, height=2.2, xlo=0, xhi=t[-1], ylo=-40, yhi=0, center=DOWN * 1.3)
        pk = DashedLine(a2.to(0, d["peak"]), a2.to(t[-1], d["peak"]), color=RED, stroke_width=2)
        vu = curve(t, np.clip(d["vu"], -40, 0), a2.to, color=TUNE, width=3)
        pp = curve(t, np.clip(d["ppm"], -40, 0), a2.to, color=BLUE, width=3)
        yt = VGroup(*[label(f"{v} dB", font_size=13, color=GREY_A).next_to(a2.to(0, v), LEFT, buff=0.1) for v in (0, -20, -40)])
        xt = VGroup(*[label(f"{v:.1f} s", font_size=13, color=GREY_A).next_to(a2.to(v, -40), DOWN, buff=0.08) for v in (0, 0.4, 0.8, 1.2)])
        key = VGroup(label(rf"sample peak \ ({d['peak']:.1f} dBFS)", font_size=16, color=RED), label(rf"PPM \ (peak {max(d['ppm']):.0f})", font_size=16, color=BLUE),
                     label(rf"VU \ (peak {max(d['vu']):.0f})", font_size=16, color=TUNE)).arrange(RIGHT, buff=0.7).next_to(a2, UP, buff=0.15)
        wl = label(r"one snare hit", font_size=15, color=GREY_A).next_to(ax, UP, buff=0.05).align_to(ax, LEFT)
        head = label(r"three meters, \ one drum hit", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Watch the three meters on a single snare hit. <bookmark mark='a'/> Its largest sample is at minus "
            f"{say(-d['peak'], 1)} dBFS. <bookmark mark='b'/> The peak programme meter climbs to about "
            f"{say(-max(d['ppm']))} below full scale and falls away slowly. <bookmark mark='c'/> The VU needle, averaging, "
            f"never gets above minus {say(-max(d['vu']))}: twenty decibels below the peak. A meter is a choice of what to "
            "ignore."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(wl), FadeIn(wave), FadeIn(a2), FadeIn(yt), FadeIn(xt), FadeIn(ghost(VGroup(vu, pp), 0.25)))
            vo.wait_until("a")
            self.play(Create(pk), FadeIn(key[0]))
            vo.wait_until("b")
            self.play(Create(pp), FadeIn(key[1]), run_time=1.2)
            vo.wait_until("c")
            self.play(Create(vu), FadeIn(key[2]), run_time=1.2)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def weighting(self):
        d = load("meters")
        f = np.array(d["f"])
        ax = logf_axes(width=9.6, height=3.0, flo=20, fhi=20000, ylo=-15, yhi=6, center=DOWN * 0.3)
        cv = curve(f, np.clip(d["k_db"], -15, 6), ax.to, color=TUNE, width=3)
        yt = VGroup(*[label(f"{v:+d} dB" if v else "0 dB", font_size=14, color=GREY_A).next_to(ax.to(20, v), LEFT, buff=0.1) for v in (6, 0, -10)])
        n1 = label(r"a high-pass near 40 Hz: \ the revised low-frequency B curve", font_size=16, color=WHITE).next_to(ax.to(60, -12), UR, buff=0.1)
        n2 = label(r"a +4 dB shelf above about 1.5 kHz: \ the head's effect on sound", font_size=16, color=WHITE).next_to(ax.to(1500, 4.5), UP, buff=0.15)
        head = label(r"K-weighting", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "BS.1770 begins by filtering the signal. <bookmark mark='a'/> The K-weighting curve is two filters. "
            "<bookmark mark='b'/> A high-pass near forty hertz, so that deep bass counts for less, as the ear hears it at "
            "ordinary levels. <bookmark mark='c'/> And a shelf of four decibels above about one and a half kilohertz, which "
            "models the head: sound arriving at the ear is boosted there by diffraction round the head. Gilbert Soulodre's "
            "listening tests at the Communications Research Centre in Ottawa chose it, around 2004, as the simplest filter "
            "that predicted how loud people judged music to be."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(yt), FadeIn(ghost(cv, 0.3)))
            vo.wait_until("a")
            self.play(Create(cv), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(n1))
            vo.wait_until("c")
            self.play(FadeIn(n2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tones(self):
        d = load("meters")
        c = clip("meters.two")
        boxes = choice_boxes([r"60 Hz", r"2 kHz"], width=3.0, height=0.9, buff=1.4, size=22).move_to(UP * 0.6)
        res = VGroup(label(r"the same RMS level", font_size=19, color=GREY_A),
                     label(rf"K-weighted: \ {d['tones']['low']:.1f} LUFS \ against \ {d['tones']['high']:.1f} LUFS", font_size=20, color=TUNE)).arrange(DOWN, buff=0.3).move_to(DOWN * 1.2)
        head = label(r"two tones, \ one voltage", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear it: a sixty-hertz tone and a two-kilohertz tone with exactly the same RMS level, the same voltage on a meter."):
            self.play(FadeIn(head), FadeIn(boxes), FadeIn(res[0]))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"60 Hz, \ then 2 kHz", kind="synthesized", detail=r"two sine tones", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["low"], st["high"] - 0.3, buff=0.08)
            pulse(snd, boxes[1], st["high"], c.duration, buff=0.08)
        with self.voiceover(
            "The low tone sounds much quieter. A VU meter calls them equal; the K-weighted meter puts them "
            f"{say(d['tones']['high'] - d['tones']['low'])} loudness units apart, in the direction your ears do."
        ):
            self.play(FadeIn(res[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def limits(self):
        items = [
            (r"one number for a whole song works because listeners judge a song's loudness much as they judge its average", WHITE),
            (r"it fails at the edges: \ very bass-heavy music, \ very sparse music, \ and listening far quieter or louder than usual", WHITE),
            (r"Part 4's loudness models \ (Zwicker's, \ Moore and Glasberg's) \ do better, \ band by band, \ at great cost in computation", WHITE),
            (r"BS.1770 won by being simple enough to put in every meter, \ every player and every television", TUNE),
        ]
        rows_scene(self, r"one number", items,
                   "Can one number really stand for a song's loudness? <bookmark mark='b'/> It works because listeners judge a "
                   "song's loudness much as they judge its average. <bookmark mark='c'/> It fails at the edges: very bass-heavy "
                   "music, very sparse music, and listening far quieter or louder than usual. <bookmark mark='d'/> The loudness "
                   "models of Part 4, Zwicker's and Moore and Glasberg's, do better, band by band, at a great cost in computation. "
                   "<bookmark mark='e'/> BS.1770 won by being simple enough to put in every meter, every player and every "
                   "television.", marks="bcde")
