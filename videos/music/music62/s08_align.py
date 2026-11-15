from __future__ import annotations

import numpy as np

from videos.music.music62.common import *  # noqa: F403


class Align(SoundScene):
    def construct(self):
        chapter(self, 7, r"Time warping", r"How do you line up a score with a performance?")
        self.heard()
        self.dtw()
        self.slope()
        self.origins()
        self.uses()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("align")
        c = clip("align.two")
        dp, rb = np.array(d["deadpan"]), np.array(d["rubato"])
        ax1 = frame_axes(width=10.0, height=0.5, xlo=0, xhi=max(rb[-1], dp[-1]) + 0.5, ylo=0, yhi=1, center=UP * 0.9)
        ax2 = frame_axes(width=10.0, height=0.5, xlo=0, xhi=max(rb[-1], dp[-1]) + 0.5, ylo=0, yhi=1, center=DOWN * 0.9)
        t1 = VGroup(*[Dot(ax1.to(t, 0.5), radius=0.06, color=GREY_B) for t in dp])
        t2 = VGroup(*[Dot(ax2.to(t, 0.5), radius=0.06, color=TUNE) for t in rb])
        links = VGroup(*[Line(ax1.to(a, 0.5), ax2.to(b, 0.5), stroke_width=1, color=GREY_D) for a, b in zip(dp, rb)])
        l1 = label(r"played strictly: \ a beat every 0.5 s", font_size=16, color=GREY_B).next_to(ax1, UP, buff=0.1).align_to(ax1, LEFT)
        l2 = label(r"played with rubato", font_size=16, color=TUNE).next_to(ax2, UP, buff=0.1).align_to(ax2, LEFT)
        head = label(r"one score, \ two timings", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Here is the Tune with its chords played strictly, a beat every half second, then with rubato. Same notes, different times."):
            self.play(FadeIn(head), FadeIn(ax1), FadeIn(ax2), FadeIn(t1), FadeIn(t2), FadeIn(l1), FadeIn(l2))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"strict, \ then rubato", kind="physical model", detail=r"Part 38's piano", corner=DL, tag_corner=DR)
            pulse(snd, VGroup(ax1, t1), st["deadpan"], st["rubato"] - 0.4, buff=0.1)
            pulse(snd, VGroup(ax2, t2), st["rubato"], c.duration, buff=0.1)
        with self.voiceover("Aligning them means finding, for every moment of one, the matching moment of the other: these lines."):
            self.play(Create(links), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dtw(self):
        d = load("align")
        Cm = np.array(d["cost"])
        pic = picture(1 - Cm.T, 0, 1, 4.6, 4.6).move_to(LEFT * 3.2 + DOWN * 0.3)
        path = np.array(d["path"])
        n, m = Cm.shape
        x0, y0 = pic.get_left()[0], pic.get_bottom()[1]
        pts = [[x0 + 4.6 * (p[0] / 2 + 0.5) / n, y0 + 4.6 * (p[1] / 2 + 0.5) / m, 0] for p in path]
        line = VMobject(stroke_color=TUNE, stroke_width=3).set_points_as_corners(pts)
        xl = label(r"strict \ (time $\rightarrow$)", font_size=14, color=GREY_A).next_to(pic, DOWN, buff=0.1)
        yl = label(r"rubato", font_size=14, color=GREY_A).rotate(PI / 2).next_to(pic, LEFT, buff=0.1)
        eqs = VGroup(
            MathTex(r"D(i, j) = c(i, j) + \min\{D(i{-}1, j{-}1),\ D(i{-}1, j),\ D(i, j{-}1)\}", font_size=28, color=WHITE),
            label(r"$c$: \ 1 $-$ the cosine between chroma frames", font_size=16, color=GREY_A),
            label(rf"offline: \ every beat placed within {d['err_ms']:.0f} ms \ (median), \ {d['err_max_ms']:.0f} at worst", font_size=17, color=TUNE),
            label(rf"online, \ hearing only the past: \ {d['online_ms']:.0f} ms median, \ {d['online_max_ms']:.0f} at worst", font_size=17, color=BLUE),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * 3.0 + DOWN * 0.3)
        head = label(r"dynamic time warping", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Dynamic time warping does it. <bookmark mark='a'/> Compare every chroma frame of one with every frame of the "
            "other: bright where they match. <bookmark mark='b'/> Then find the cheapest path from the start of both to the end "
            "of both, moving forward in one, the other or both at each step: dynamic programming, a third time. "
            f"<bookmark mark='c'/> Offline, with both recordings whole, the path places every beat within {say(d['err_ms'])} "
            f"milliseconds, at the median. <bookmark mark='d'/> Online, hearing only the past, as a live accompanist must, the "
            f"median is {say(d['online_ms'])} milliseconds, with a worst moment of {say(d['online_max_ms'])}, at a held note where "
            "nothing new arrives."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pic), FadeIn(xl), FadeIn(yl))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(eqs[0]), FadeIn(eqs[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(eqs[2]))
            vo.wait_until("d")
            self.play(FadeIn(eqs[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def origins(self):
        items = [
            (r"speech first: \\ Sakoe and Chiba \\ (1978) \\ matched a spoken word against stored examples, \\ said faster or slower", WHITE),
            (r"the cost grows with the product of the lengths: \\ two three-minute recordings at 20 frames a second: \\ 13 million cells", WHITE),
            (r"so paths are kept near the diagonal \\ (a band), \\ or found coarse to fine \\ (multiscale DTW)", WHITE),
            (r"music added chroma, \\ and the knowledge that a performance never goes backwards \\ (except for repeats)", TUNE),
        ]
        rows_scene(self, r"where time warping came from", items,
                   "Time warping came from speech. <bookmark mark='b'/> In 1978 Hiroaki Sakoe and Seibi Chiba matched a spoken word "
                   "against stored examples, however fast or slow it was said. <bookmark mark='c'/> Its cost grows with the product "
                   "of the two lengths: two three-minute recordings at twenty frames a second make thirteen million cells. "
                   "<bookmark mark='d'/> So paths are kept in a band near the diagonal, or found coarse to fine. "
                   "<bookmark mark='e'/> Music added chroma, and the knowledge that a performance never goes backwards, except "
                   "for the repeats.", marks="bcde")

    # ------------------------------------------------------------------
    def slope(self):
        d = load("align")
        ratio = np.array(d["ratio"])
        true = np.array(d["true_ratio"])
        beats = np.arange(len(ratio) + 1)
        ax = frame_axes(width=9.0, height=3.0, xlo=0, xhi=len(ratio), ylo=0.5, yhi=1.8, center=DOWN * 0.3 + LEFT * 0.6)
        ct = curve(beats[:-1] + 0.5, true, ax.to, color=GREY_B, width=5)
        ce = curve(beats[:-1] + 0.5, ratio, ax.to, color=TUNE, width=3)
        one = DashedLine(ax.to(0, 1.0), ax.to(len(ratio), 1.0), color=GREY_D, stroke_width=1.5)
        yt = VGroup(*[label(f"{v:g}", font_size=13, color=GREY_A).next_to(ax.to(0, v), LEFT, buff=0.1) for v in (0.5, 1.0, 1.5)])
        xl = label(r"beat", font_size=14, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        key = VGroup(label(r"each beat's length, \ relative to strict \ (the truth)", font_size=15, color=GREY_B),
                     label(r"read from the warping path's slope", font_size=15, color=TUNE)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.3)
        head = label(r"a tempo curve, \ from the path", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The warping path is also a measurement. <bookmark mark='a'/> Its slope says how much longer each beat of the "
            "performance is than the same beat played strictly: a tempo curve. <bookmark mark='b'/> Read from the path, it "
            "follows the truth, beat by beat: the stretching through each phrase and the held phrase end, all but the very last "
            "beat, where the path runs out. This is how Part 43's tempo curves "
            "of real pianists are measured, recording by recording."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(yt), FadeIn(xl), FadeIn(one))
            vo.wait_until("a")
            self.play(Create(ct), FadeIn(key[0]), run_time=1.2)
            vo.wait_until("b")
            self.play(Create(ce), FadeIn(key[1]), run_time=1.2)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def uses(self):
        items = [
            (r"page turning: \ a tablet follows the pianist and turns the page", WHITE),
            (r"study: \ line up fifty recordings of one sonata and compare their tempos bar by bar \ (Part 43)", WHITE),
            (r"answer keys: \ align a score to a recording and you have its notes' times, \ for Part 61's transcribers", WHITE),
            (r"subtitles for music: \ lyrics shown as they are sung", WHITE),
            (r"and the accompanist: \ Chapter 8", TUNE),
        ]
        rows_scene(self, r"what alignment is for", items,
                   "Alignment has many uses. <bookmark mark='b'/> Page turning: a tablet follows the pianist and turns the page. "
                   "<bookmark mark='c'/> Study: line up fifty recordings of one sonata and compare their tempos bar by bar, as "
                   "Part 43 did. <bookmark mark='d'/> Answer keys: align a score to a recording and you have its notes' times, which "
                   "Part 61's transcribers need. <bookmark mark='e'/> Lyrics shown as they are sung. <bookmark mark='f'/> And the "
                   "accompanist of the next chapter.", marks="bcdef")
