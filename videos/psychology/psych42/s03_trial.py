from __future__ import annotations

from videos.psychology.psych42.common import *  # noqa: F403


class Trial(VoiceoverScene):
    def construct(self):
        self.card()
        self.regression()
        self.controls()
        self.allegiance_bias()

    def card(self):
        card = chapter_card(2, r"The trial, \ and the control problem", r"Better than what?", lit=(), part=PART,
                            scale=("person",), marr=("what",))
        with self.voiceover("Chapter two. The trial, and the control problem."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def regression(self):
        d = load("arms")
        head = heading(r"Everyone improves")
        A = axes([0, 1], [0, 0.12], x_length=5.4, y_length=2.6, xticks=None, yticks=None,
                 xlabel=r"symptom score", ylabel=r"people", center=[-3.4, 0.7, 0], font_size=13)
        x = np.linspace(0, 1, 300)
        s = 0 + 40 * x
        dens = np.exp(-0.5 * ((s - 14) / 7.07) ** 2)
        dens = 0.1 * dens / dens.max()
        full = curve(A.ax, x, dens, GREY_B, stroke_width=2)
        thr = DashedLine(A.ax.c2p(0.5, 0), A.ax.c2p(0.5, 0.11), color=AUTH, stroke_width=2)
        t_l = label(r"enrol at 20 or more", font_size=12, color=AUTH).next_to(A.ax.c2p(0.5, 0.11), UP, buff=0.05)
        xt = np.linspace(0.5, 1, 60)
        tail = area_under(A.ax, xt, 0.1 * np.exp(-0.5 * ((40 * xt - 14) / 7.07) ** 2), AUTH, 0.5)
        rows = rows_of([
            (r"Psyche: \ each person's score wanders around their own mean; \ they come for help when it reaches 20 or "
             r"more, \ at their worst", WHITE),
            (rf"with no treatment at all, \ the group's average falls from {d['none_pre']:.1f} to {d['none_post']:.1f}",
             PERSON),
            (r"regression to the mean: \ a score picked for being high is followed, \ on average, \ by a lower one; \ "
             r"and episodes end on their own", MODEL),
            (r"so improvement in treated people is no evidence that treatment works; \ only a comparison is", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = psyche_tag(r"\texttt{clinic.therapy\_trial}, \ 200 people")
        with self.voiceover(
            "Why does everyone improve? <bookmark mark='a'/> In Psyche, each person's score wanders around their own "
            "average, and they come for help when it reaches twenty or more, at their worst. "
            "<bookmark mark='b'/> With no treatment at all, the group's average falls by more than five points. "
            "<bookmark mark='c'/> That's regression to the mean. A score picked for being high is followed, on "
            "average, by a lower one. And real episodes end on their own as well. <bookmark mark='d'/> So the "
            "improvement of treated people is no evidence that treatment works. Only a comparison is."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(full))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(thr), FadeIn(t_l), FadeIn(tail))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def controls(self):
        d = load("arms")
        head = heading(r"The control sets the effect")
        arms = (("waitlist", r"waiting list", GREY_B), ("none", r"no treatment", GREY_A),
                ("placebo", r"placebo therapy", SYMP), ("active", r"active therapy", GOOD))
        A = axes([0.3, 4.7], [0, 24], x_length=5.6, y_length=3.0, xticks=None, yticks=[0, 10, 20],
                 yfmt=lambda v: f"{v:.0f}", ylabel=r"symptoms at the end", center=[-3.3, 0.6, 0], font_size=13)
        b = bars(A.ax, [1, 2, 3, 4], [d[f"{a}_post"] for a, _, _ in arms], [c for _, _, c in arms], width=0.6)
        start = DashedLine(A.ax.c2p(0.3, d["none_pre"]), A.ax.c2p(4.7, d["none_pre"]), color=AUTH, stroke_width=1.5)
        s_l = label(r"at entry", font_size=12, color=AUTH).next_to(A.ax.c2p(4.7, d["none_pre"]), UP, buff=0.05)
        names = VGroup(*[wrapped_label(t, 1.3, 12, c).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.15)
                         for i, (_, t, c) in enumerate(arms)])
        rows = rows_of([
            (r"the same active therapy, \ compared with three controls, \ in 2{,}000 people per arm", WHITE),
            (rf"against a waiting list, \ $d = {d['d_waitlist']:.2f}$: \ waiting may itself harm, \ by holding "
             rf"people back from seeking help elsewhere", GREY_A),
            (rf"against no treatment, \ $d = {d['d_none']:.2f}$; \ against a credible placebo therapy, \ only "
             rf"$d = {d['d_placebo']:.2f}$", SYMP),
            (r"patients cannot be blind to talking therapy, \ and researchers often favour their own: \ the effect "
             r"is a property of the comparison", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = psyche_tag(r"\texttt{clinic.trial\_effect}")
        with self.voiceover(
            "So compare. But with what? <bookmark mark='a'/> Psyche runs the same active therapy against three "
            "controls, in two thousand people per arm. <bookmark mark='b'/> Against a waiting list the effect is "
            "biggest, partly because waiting may itself do harm, holding people back from seeking help elsewhere. "
            "<bookmark mark='c'/> Against no treatment it's smaller. And against a credible placebo therapy, with a "
            "warm listener but no specific technique, it's less than half as big. <bookmark mark='d'/> Patients can't "
            "be blind to talking therapy, and researchers often favour their own. The effect is a property of the "
            "comparison, not of the therapy alone."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(start), FadeIn(s_l))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in b], lag_ratio=0.3))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def allegiance_bias(self):
        d = load("allegiance")
        head = heading(r"Whose therapy wins?")
        A = axes([-1.2, 1.2], [0, 61], x_length=5.4, y_length=3.4, xticks=[-1, 0, 1], yticks=None,
                 xfmt=lambda v: f"{v:+.0f}" if v else "0", xlabel=r"observed advantage of A over B", center=[-3.3, 0.3, 0],
                 font_size=13)
        dots = VGroup()
        for i, (x, l) in enumerate(zip(d["d"], d["loyal"])):
            dots.add(Dot(A.ax.c2p(float(np.clip(x, -1.15, 1.15)), i + 0.5), radius=0.045,
                         color=GOOD if l > 0 else SYMP))
        zero = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(0, 61), color=GREY_B, stroke_width=1.5)
        key = VGroup(label(r"team loyal to A", font_size=13, color=GOOD),
                     label(r"team loyal to B", font_size=13, color=SYMP)).arrange(RIGHT, buff=0.5).next_to(A, DOWN, buff=0.3)
        rows = rows_of([
            (r"Psyche: \ 60 trials comparing two equally good therapies; \ each team's loyalty adds a little to its "
             r"own side's result", WHITE),
            (rf"pooled across all trials, \ A's advantage is {d['mu_all']:+.2f}: \ the truth", GREY_A),
            (rf"but trials by A's loyalists find {d['mu_a']:+.2f}, \ and B's find {d['mu_b']:+.2f}", AUTH),
            (r"researcher allegiance predicts the results of comparisons between therapies in real meta-analyses too", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = psyche_tag(r"\texttt{clinic.allegiance}")
        with self.voiceover(
            "One more bias. <bookmark mark='a'/> Psyche runs sixty trials comparing two equally good therapies. Each "
            "trial is run by a team loyal to one of them, and loyalty adds a little to its own side's result, through "
            "better training, more enthusiasm, or kinder analysis. <bookmark mark='b'/> Pooled across all the "
            "trials, the advantage is almost exactly zero, the truth. <bookmark mark='c'/> But trials by one side's "
            "loyalists find their therapy ahead, and so do the other side's. <bookmark mark='d'/> In real "
            "meta-analyses too, researcher allegiance predicts the results of comparisons between therapies."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(zero), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.03), run_time=2.0)
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
