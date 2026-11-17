from __future__ import annotations

from videos.psychology.psych62.common import *  # noqa: F403


class StageTwo(VoiceoverScene):
    def construct(self):
        card_section(self, 6, r"Stage 2: \ the data", r"What did the data say?", marr=("what",))
        self.deviation()
        self.result()
        self.verdict()
        self.consequence()

    def deviation(self):
        d = load("stage2")
        p = load("plan")
        rows_section(self, r"First, \ a deviation", [
            (rf"the registered rule (at least {p['registered_min']} usable trials per angle in each half) kept "
             rf"{d['kept_strict']} of 54 people", AUTH),
            (r"the data have fewer ``same'' trials per angle than the plan assumed: \ as few as three in a half, \ "
             r"before errors", MODEL),
            (rf"the change, \ decided on those counts alone, \ before any reliability was computed: \ a minimum of "
             rf"{p['used_min']}; \ {d['n']} people kept", PERSON),
            (r"reported here, \ in the paper and in the code, \ with the original rule beside it", GOOD),
            (r"a registered report does not forbid changes; \ it makes every change visible", YOU),
        ], "The plan met the data, and the first thing to report is a deviation. <bookmark mark='a'/> The registered "
           "rule, at least four usable trials per angle in each half, kept nobody: zero of fifty-four people. "
           "<bookmark mark='b'/> The data have fewer same trials per angle than the plan assumed, as few as three in "
           "a half before errors. <bookmark mark='c'/> The change was decided on those counts alone, before any "
           "reliability was computed: a minimum of two, which kept forty people. <bookmark mark='d'/> It's reported "
           "here, in the paper and in the code, with the original rule beside it. <bookmark mark='e'/> A registered "
           "report doesn't forbid changes. It makes every change visible.")

    def result(self):
        d = load("stage2")
        head = heading(r"Each person's slope, \ odd trials against even")
        so, se = np.asarray(d["slope_odd"]), np.asarray(d["slope_even"])
        A = axes([-2, 28], [-2, 28], x_length=4.2, y_length=4.0, xticks=[0, 10, 20], yticks=[0, 10, 20],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", xlabel=r"slope, \ odd trials (ms per degree)",
                 ylabel=r"slope, \ even trials", center=[-3.8, 0.0, 0], font_size=12)
        diag = DashedLine(A.ax.c2p(-2, -2), A.ax.c2p(28, 28), color=GREY_B, stroke_width=1.5)
        pts = scatter(A.ax, np.clip(so, -1.9, 27.9), np.clip(se, -1.9, 27.9), PERSON, radius=0.06)
        r_half = float(np.corrcoef(so, se)[0, 1])
        rows = rows_of([
            (rf"{d['n']} people; \ the median slope {d['median_slope']:.1f} ms per degree: \ the robust effect, \ "
             rf"again", WHITE),
            (rf"the halves correlate {r_half:.2f}; \ corrected for length, \ the slope's reliability is "
             rf"{d['slope_rel']:.2f}", MODEL),
            (rf"95\% interval: \ {d['slope_ci'][0]:.2f} to {d['slope_ci'][1]:.2f}: \ it contains 0.70", AUTH),
            (rf"the mean time: \ {d['mean_rel']:.2f} ({d['mean_ci'][0]:.2f} to {d['mean_ci'][1]:.2f}), \ "
             rf"clearly more reliable", GOOD),
        ], 6.4, 19, 0.36).move_to([3.0, -0.1, 0])
        tag = published_tag(r"Ganis \& Kievit (2015)").to_corner(DL, buff=0.3)
        tag2 = psyche_tag(r"\texttt{thesis.analyse}, \ the registered analysis")
        with self.voiceover(
            "Now the result. <bookmark mark='a'/> Forty people, with a median slope of about twelve milliseconds "
            "per degree: the robust effect, again. <bookmark mark='b'/> Here's each person's slope in the odd trials "
            "against the even ones. The halves correlate zero point five eight, and corrected for length the "
            "slope's reliability is zero point seven four. <bookmark mark='c'/> The ninety-five percent interval runs "
            "from zero point five one to zero point eight seven. It contains zero point seven. "
            "<bookmark mark='d'/> And the mean time's reliability is zero point nine four, clearly higher."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tag2), FadeIn(A), Create(diag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(pts))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def verdict(self):
        d = load("stage2")
        head = heading(r"The verdict, \ by the rule fixed in advance")
        rows = VGroup(
            VGroup(label(r"H1", font_size=40, color=AUTH),
                   wrapped_label(r"the slope's reliability is below 0.70", 6.0, 24, WHITE),
                   label(d["H1"], font_size=34, color=GREY_B)).arrange(RIGHT, buff=0.5),
            VGroup(label(r"H2", font_size=40, color=MODEL),
                   wrapped_label(r"the mean time is more reliable than the slope", 6.0, 24, WHITE),
                   label(d["H2"], font_size=34, color=GOOD)).arrange(RIGHT, buff=0.5),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to([0, 0.6, 0])
        foot = wrapped_label(r"the paradox's strong prediction was not supported, \ and not refuted; \ the estimate "
                             r"leans against it; \ the corollary held", 12.0, 23, YOU).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "So here's the verdict, by the rule fixed in advance. <bookmark mark='a'/> H1, that the slope's "
            "reliability is below zero point seven: inconclusive. <bookmark mark='b'/> H2, that the mean time is "
            "more reliable than the slope: supported. <bookmark mark='c'/> The paradox's strong prediction was not "
            "supported, and not refuted, and the estimate leans against it. The corollary held. That's the result, "
            "and the narration follows it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0], shift=RIGHT * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(rows[1], shift=RIGHT * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(1.5)
        self.clear_scene()

    def consequence(self):
        d = load("stage2")
        rel_slope, rel_mean, rel_y, true_r = float(d["slope_rel"]), float(d["mean_rel"]), 0.80, 0.40
        z = 1.959964 + 0.841621

        def n_for(r):
            return (z / np.arctanh(r)) ** 2 + 3

        obs = [true_r, true_r * np.sqrt(rel_mean * rel_y), true_r * np.sqrt(rel_slope * rel_y)]
        ns = [n_for(r) for r in obs]
        head = heading(r"What a reliability of 0.74 costs")
        A = axes([0.3, 3.7], [0, 100], x_length=4.6, y_length=3.0, xticks=None, yticks=[0, 40, 80],
                 yfmt=lambda v: f"{v:.0f}", ylabel=r"people for 80\% power", center=[-3.6, 0.3, 0], font_size=12)
        b = bars(A.ax, [1, 2, 3], ns, [GOOD, PERSON, MODEL], width=0.6)
        names = VGroup(*[wrapped_label(t, 1.3, 12, GREY_A).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.12)
                         for i, t in enumerate([r"perfect measures", r"mean time", r"rotation slope"])])
        rows = rows_of([
            (rf"suppose a person's rotation speed truly correlates {true_r:.1f} with some criterion measured with "
             rf"reliability {rel_y:.2f} (illustrative)", WHITE),
            (rf"with perfect measures, \ about {ns[0]:.0f} people detect it (80\% power, \ 5\% two-sided)", GOOD),
            (rf"the mean time's reliability ({rel_mean:.2f}) lowers the observed $r$ to {obs[1]:.2f}: \ about "
             rf"{ns[1]:.0f} people", PERSON),
            (rf"the slope's ({rel_slope:.2f}) lowers it to {obs[2]:.2f}: \ about {ns[2]:.0f} people", MODEL),
            (r"a reliability of 0.74 is usable: \ it costs about 70\% more people, \ not a lost cause; \ "
             r"the paradox bites at reliabilities near 0.3", YOU),
        ], 6.4, 18, 0.32).move_to([3.0, -0.2, 0])
        with self.voiceover(
            "What does a reliability of zero point seven four cost a study? <bookmark mark='a'/> Suppose a person's "
            "rotation speed truly correlates zero point four with some criterion, measured with a reliability of "
            "zero point eight. The numbers are illustrative. <bookmark mark='b'/> With perfect measures, about forty-"
            "seven people detect it. <bookmark mark='c'/> The mean time's reliability lowers the observed "
            "correlation to about zero point three five, and needs about sixty-three people. <bookmark mark='d'/> "
            "The slope's lowers it to about zero point three one, and needs about eighty. <bookmark mark='e'/> So a "
            "reliability of zero point seven four is usable. It costs about seventy percent more people. It isn't a "
            "lost cause. The paradox bites at reliabilities near zero point three."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            for m, r, bb in zip("bcd", rows[1:4], b):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15), GrowFromEdge(bb, DOWN))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
