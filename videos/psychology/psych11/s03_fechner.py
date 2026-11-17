from __future__ import annotations

import numpy as np

from videos.psychology.psych11.common import *  # noqa: F403


class Fechner(VoiceoverScene):
    def construct(self):
        self.card()
        self.staircase()
        self.derive()
        self.claim()

    def card(self):
        card = chapter_card(2, r"Fechner's step", r"Can a fraction become a scale of sensation?",
                            lit={1860: r"Fechner's \emph{Elements}"}, part=PART, scale=("mind",), marr=("what",))
        with self.voiceover(
            "Chapter two. Fechner's step."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def staircase(self):
        d = load("fechner")
        head = heading(r"Count the just noticeable steps")
        A = axes([0, 1000], [0, 95], x_length=7.2, y_length=4.4, xticks=[0, 250, 500, 750, 1000], yticks=[0, 30, 60, 90],
                 xlabel=r"intensity, $I$", ylabel=r"steps counted from the threshold", center=[-2.9, -0.35, 0])
        ax = A.ax
        st = d["steps"]
        pts = []
        for n in range(len(st) - 1):
            pts += [ax.c2p(min(st[n], 1000), n), ax.c2p(min(st[n + 1], 1000), n)]
        stairs = VMobject(color=WEBERC, stroke_width=3).set_points_as_corners(pts)
        smooth = curve(ax, d["i"], d["log_law"], FECHC, stroke_width=4)
        rows = rows_of([
            (rf"start at the absolute threshold, \ $I_0$; \ each step is Weber's fraction ($k = {d['w']:.2f}$) of the "
             r"intensity below it", WHITE),
            (r"near the bottom the steps are tiny; \ high up they are long", WEBERC),
            (rf"from 1 to 1{{,}}000: \ ${d['jnds_to_1000']:.0f}$ steps; \ from 1 to 10, \ 10 to 100, \ 100 to 1{{,}}000: \ "
             rf"${d['jnds_to_1000'] / 3:.0f}$ each", THRESH),
            (r"equal ratios of intensity, \ equal numbers of steps: \ a logarithm", FECHC),
        ], 5.0, 28, 0.28).move_to([4.3, -0.3, 0])
        keep_in_frame(rows)
        tag = psyche_tag(rf"computed: steps of {100 * d['w']:.0f}\%, \ from an intensity of 1")
        with self.voiceover(
            "Fechner's step was to turn Weber's fraction into a scale. Start at the absolute threshold, "
            "the weakest stimulus that can be felt at all. Add one just noticeable difference. Then "
            "another. <bookmark mark='a'/> Each step is Weber's fraction of the intensity below it, "
            f"{100 * d['w']:.0f} percent here. So near the bottom the steps are tiny, and high up they're "
            "long. <bookmark mark='b'/> Now count them. From an intensity of 1 to an intensity of a "
            f"thousand there are {d['jnds_to_1000']:.0f} just noticeable steps. And from 1 to 10, from "
            f"10 to 100, and from 100 to a thousand, there are {d['jnds_to_1000'] / 3:.0f} each. "
            "<bookmark mark='c'/> Equal ratios of intensity give equal numbers of steps. That is the "
            "signature of a logarithm."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Create(stairs), FadeIn(rows[1]), run_time=5.0, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(Create(smooth), FadeIn(rows[3]), run_time=2.0)
        self.clear_scene()

    def derive(self):
        head = heading(r"Fechner's law in four lines")
        lines = VGroup(
            VGroup(label(r"Weber:", font_size=30, color=WEBERC), MathTex(r"\Delta I = k\,I", font_size=40)),
            VGroup(label(r"Fechner's assumption: \ every just noticeable step is one unit of sensation:", font_size=30,
                         color=FECHC), MathTex(r"\Delta S = 1", font_size=40)),
            VGroup(label(r"so", font_size=30, color=GREY_A), MathTex(r"\frac{\Delta S}{\Delta I} = \frac{1}{k\,I}", font_size=40)),
            VGroup(label(r"make the steps small, \ and add them up:", font_size=30, color=GREY_A),
                   MathTex(r"S = \frac{1}{k}\,\ln\frac{I}{I_0}", font_size=46, color=THRESH)),
        )
        for ln in lines:
            ln.arrange(RIGHT, buff=0.4)
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, 0.35, 0])
        keep_in_frame(lines)
        end = wrapped_label(r"Sensation grows as the logarithm of intensity. \ The constant comes from the fraction, \ and "
                            r"the zero from the absolute threshold.", 12.2, 30, FECHC).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Here is the same argument in four lines. <bookmark mark='a'/> Weber: the just noticeable "
            "difference is k times I. <bookmark mark='b'/> Fechner's assumption, and it is an assumption: "
            "every just noticeable step is one unit of sensation, the same size at the bottom of the scale "
            "and at the top. <bookmark mark='c'/> So sensation grows by one unit for every k I of "
            "intensity. <bookmark mark='d'/> Make the steps small and add them up, which is to "
            "integrate, and out comes Fechner's law: sensation is one over k times the logarithm of I over "
            "I nought. <bookmark mark='e'/> The constant comes from Weber's fraction, and the zero of the "
            "scale from the absolute threshold."
        ) as vo:
            self.play(FadeIn(head))
            for mark_, ln in zip("abcd", lines):
                vo.wait_until(mark_)
                self.play(FadeIn(ln, shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def claim(self):
        d = load("fechner")
        head = heading(r"What Fechner claimed, \ and what it rests on")
        A = axes([0, 1000], [0, 1.05], x_length=6.4, y_length=3.8, xticks=[0, 500, 1000], yticks=[0, 1],
                 xlabel=r"intensity", ylabel=r"sensation, \ as a share of its value at 1{,}000", center=[-3.2, -0.3, 0])
        ax = A.ax
        lg = curve(ax, d["i"], d["log_norm"], FECHC, stroke_width=5)
        ll = label(r"Fechner: \ a logarithm", font_size=28, color=FECHC).move_to(ax.c2p(640, 0.62))
        rows = rows_of([
            (r"the first quantitative law of the mind: \ sensation measured in counted steps", FECHC),
            (r"it rests on one assumption: \ that a just noticeable difference is the same amount of sensation "
             r"everywhere", THRESH),
            (r"nothing in the data forces that. \ Change it, \ and the law changes (chapter 9)", BAD),
            (r"first, \ the steps themselves have to be measured: \ the methods", WHITE),
        ], 5.4, 29, 0.3).move_to([4.1, -0.3, 0])
        keep_in_frame(rows)
        src = published_tag(archive.FECHNER_1860.cite)
        with self.voiceover(
            "Here is what Fechner claimed. The first quantitative law of the mind, with sensation "
            "measured, not by a ruler, but by counting steps that can each be found by experiment. "
            "<bookmark mark='a'/> It rests on one assumption: that a just noticeable difference is the "
            "same amount of sensation everywhere, the step from 1 to 1.08 as large as the step from 900 "
            "to 972. <bookmark mark='b'/> Nothing in the data forces that. Change the assumption, and "
            "the law changes, which is what happened a century later, in chapter nine. "
            "<bookmark mark='c'/> But first the steps have to be measured, and Fechner's other lasting "
            "gift was a set of methods for doing it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(A), Create(lg), FadeIn(ll), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()
