from __future__ import annotations

import numpy as np

from videos.psychology.psych8.common import *  # noqa: F403


class OnYou(VoiceoverScene):
    def construct(self):
        self.card()
        self.three()
        self.answer()

    def card(self):
        card = chapter_card(9, r"On you: \ which of these is impossible?", r"How high can a correlation go?", lit=(),
                            part=PART, scale=("person",), marr=("how",))
        with self.voiceover(
            "Chapter nine. On you: which of these is impossible?"
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def _plots(self, c, stage):
        g = Group()
        for i in range(3):
            A = axes([-3.1, 3.1], [-3.1, 3.1], x_length=2.9, y_length=2.9, xticks=[], yticks=[], xlabel=r"", ylabel=r"",
                     center=stage.box.get_center() + np.array([-4.0 + 4.0 * i, 0.55, 0]))
            dots = VGroup(*[Dot(A.ax.c2p(float(a), float(b)), radius=0.07, color=BLOOD)
                            for a, b in zip(c["x"][i], c["y"][i])])
            cap = label(rf"{'ABC'[i]}: \ $r = {r2(c['shown'][i])}$", font_size=32).next_to(A, DOWN, buff=0.15)
            g.add(VGroup(A, dots, cap))
        return g

    def three(self):
        c = load("ceiling")
        stage = demo_stage(13.4, 6.6, r"On you: \ three results from three papers", center=[0, -0.25, 0])
        plots = self._plots(c, stage)
        given = wrapped_label(rf"In each: \ 16 people; \ across, a questionnaire with reliability {c['scale']:.1f}; "
                              rf"\ up, a brain measure with reliability {c['brain']:.1f}.", 12.2, 28, WHITE)
        given.move_to(stage.box.get_center() + np.array([0, -2.0, 0]))
        ask = label(r"One of these cannot be right. \ Which, and why?", font_size=32, color=P.ACCENT)
        ask.move_to(stage.box.get_center() + np.array([0, -2.75, 0]))
        ring = countdown_ring(0.4).move_to(stage.box.get_corner(UR) + np.array([-0.65, -0.65, 0]))
        with self.voiceover(
            "Your turn. Here are three results of the kind those papers reported. <bookmark mark='a'/> "
            "Each plot is sixteen people. Across is their score on a questionnaire. Upward is a measure "
            "taken from their brain scan. The correlations are point four five, point six two, and point "
            "eight eight. <bookmark mark='b'/> You're told two more things. The questionnaire's "
            f"reliability is {c['scale']:.1f}: give it twice, and the two sets of scores correlate "
            f"{c['scale']:.1f}. The brain measure's reliability is {c['brain']:.1f}. "
            "<bookmark mark='c'/> One of these three results can't be right, whatever the brain is doing. "
            "Which one, and why? You have everything you need from Part 3. Take a few seconds."
        ) as vo:
            self.play(FadeIn(stage))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in plots], lag_ratio=0.6), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(given))
            vo.wait_until("c")
            self.play(FadeIn(ask))
        self.add(ring)
        self.play(ring.t.animate.set_value(0.0), run_time=6.0, rate_func=linear)
        self.clear_scene()

    def answer(self):
        c = load("ceiling")
        head = heading(r"The ceiling: \ $r_{\max} = \sqrt{R_x \, R_y}$, \ with $R$ a measure's reliability")
        A = axes([0, 1], [0, 1], x_length=5.4, y_length=3.9, xticks=[0, 0.5, 1], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}", xlabel=r"reliability of the brain measure",
                 ylabel=r"highest possible correlation", center=[-3.7, -0.6, 0])
        ax = A.ax
        cv = curve(ax, c["rel"], c["ceiling_08"], THRESH, stroke_width=4)
        pt = VGroup(DashedLine(ax.c2p(c["brain"], 0), ax.c2p(c["brain"], c["ceiling"]), color=WHITE, stroke_width=2),
                    DashedLine(ax.c2p(0, c["ceiling"]), ax.c2p(c["brain"], c["ceiling"]), color=WHITE, stroke_width=2),
                    Dot(ax.c2p(c["brain"], c["ceiling"]), radius=0.08, color=WHITE))
        marks = VGroup(*[VGroup(Dot(ax.c2p(c["brain"], float(r)), radius=0.09, color=BAD if r > c["ceiling"] else MODEL),
                                label("ABC"[i], font_size=30, color=BAD if r > c["ceiling"] else MODEL).next_to(
                                    ax.c2p(c["brain"], float(r)), RIGHT, buff=0.1))
                         for i, r in enumerate(c["shown"])])
        cl = wrapped_label(r"with a questionnaire of reliability 0.8", 2.3, 26, THRESH).move_to(ax.c2p(0.79, 0.22))
        rows = rows_of([
            (rf"here: \ $\sqrt{{{c['brain']:.1f} \times {c['scale']:.1f}}} = {r2(c['ceiling'])}$", THRESH),
            (r"A and B are under it. \ C, at .88, is above: \ no pair of measures this noisy can show it", BAD),
            (r"unless it was selected, \ or the sample is small and lucky", WHITE),
            (rf"task fMRI's measured reliability is about .4: \ a ceiling near {r2(c['ceiling_task'])}", DATA),
        ], 5.6, 29, 0.3).move_to([3.9, -0.5, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed")
        src = published_tag(archive.ELLIOTT_2020.cite)
        with self.voiceover(
            "The answer is C. <bookmark mark='a'/> Part 3 gave you the rule. Two measures can't correlate "
            "with each other more strongly than each correlates with itself. If the true quantities "
            "behind them were perfectly related, the correlation you'd observe is the square root of the "
            f"product of the two reliabilities. <bookmark mark='b'/> Here that's {c['ceiling']:.2f}. "
            "<bookmark mark='c'/> A and B are under the ceiling. They might be true. C, at point eight "
            "eight, is far above it. No brain could produce it with instruments this noisy. "
            "<bookmark mark='d'/> So when you meet one, there are two explanations left, and you've now "
            "seen both. The voxels were chosen by the correlation, or the sample was small and this is "
            "the lucky one that got published. <bookmark mark='e'/> And the ceiling is lower than most "
            "people think. When the reliability of common brain-scan measures was finally added up, in "
            "2020, the average came out near point four. With a good questionnaire, that's a ceiling "
            f"near {c['ceiling_task']:.2f}, for a perfect relationship. Real ones are far from perfect."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(A), Create(cv), FadeIn(cl), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(pt), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(marks, lag_ratio=0.3), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()
