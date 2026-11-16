from __future__ import annotations

from videos.psychology.psych50.common import *  # noqa: F403


class Analysts(VoiceoverScene):
    def construct(self):
        self.card()
        self.redcards()
        self.curve_()

    def card(self):
        card = chapter_card(10, r"Many analysts, \ one dataset", r"How much does the analyst matter?", lit=(),
                            part=PART, scale=("society",), marr=("how",))
        with self.voiceover("Chapter ten. Many analysts, one dataset."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def redcards(self):
        head = heading(r"Twenty-nine teams and the red cards")
        rows = rows_of([
            (r"2018: \ Raphael Silberzahn, \ Eric Uhlmann and colleagues gave 29 teams the same data and one question: "
             r"\ are footballers with darker skin given more red cards by referees?", WHITE),
            (r"the teams chose different models, \ covariates and exclusions; \ their estimated odds ratios ran from "
             r"slightly below 1 to nearly 3", PERSON),
            (r"about two thirds found a significant effect, \ a third did not", AUTH),
            (r"the spread came from the analyses, \ like Part 49's seventy teams, \ with no one behaving badly", YOU),
        ], 12.4, 23, 0.44).move_to([0, -0.3, 0])
        tag = published_tag(r"Silberzahn et al.\ (2018)")
        with self.voiceover(
            "How much does the analyst matter? <bookmark mark='a'/> In 2018 Raphael Silberzahn, Eric Uhlmann and "
            "colleagues gave twenty-nine teams the same data and one question: are footballers with darker skin "
            "given more red cards by referees? <bookmark mark='b'/> The teams chose different models, covariates and "
            "exclusions. Their estimates ran from no effect to nearly three times the odds. <bookmark mark='c'/> About "
            "two thirds found a significant effect, and a third did not. <bookmark mark='d'/> The spread came from the "
            "analyses, like Part 49's seventy teams, with no one behaving badly."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def curve_(self):
        d = load("specs")
        head = heading(r"A specification curve")
        est = np.asarray(d["est"]); p = np.asarray(d["p"])
        n = len(est)
        A = axes([0, n + 1], [-0.05, 0.25], x_length=6.4, y_length=3.0, xticks=[1, 24, 48, 72, 96],
                 yticks=[0, 0.1, 0.2], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}",
                 xlabel=r"specifications, \ sorted by estimate", ylabel=r"estimate", center=[-2.9, 0.4, 0], font_size=12)
        zero = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(n + 1, 0), color=GREY_D, stroke_width=1)
        dots = VGroup(*[Dot(A.ax.c2p(i + 1, e), radius=0.045, color=THRESH if pv < 0.05 else GREY_B)
                        for i, (e, pv) in enumerate(zip(est, p))])
        rows = rows_of([
            (r"one simulated dataset with a small true effect; \ 96 defensible analyses: \ which covariates, \ which "
             r"outlier rule, \ raw or logged", WHITE),
            (rf"the estimates run from {est.min():.2f} to {est.max():.2f}; \ gold ones are significant: \ "
             rf"{100 * d['share_sig']:.0f}\%", THRESH),
            (r"Steegen and colleagues (2016) called it a multiverse; \ Simonsohn, \ Simmons and Nelson (2020) the "
             r"specification curve", MODEL),
            (r"show the whole curve, \ not the one analysis you liked", YOU),
        ], 5.2, 18, 0.34).move_to([3.9, -0.1, 0])
        tag = psyche_tag(r"\texttt{meta.spec\_curve}")
        tag2 = published_tag(r"Steegen et al.\ (2016); \ Simonsohn, \ Simmons \& Nelson (2020)").to_corner(DL, buff=0.3)
        with self.voiceover(
            "The remedy is to show every analysis at once. <bookmark mark='a'/> One simulated dataset with a small "
            "true effect, and ninety-six defensible analyses: which covariates, which outlier rule, raw or logged. "
            "<bookmark mark='b'/> Sorted, the estimates run from almost nothing to about zero point two, and the gold "
            "ones are significant: about half. <bookmark mark='c'/> Sara Steegen and colleagues called this a "
            "multiverse, and Uri Simonsohn, Joseph Simmons and Leif Nelson the specification curve. "
            "<bookmark mark='d'/> Show the whole curve, not the one analysis you liked."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tag2), FadeIn(A), FadeIn(zero))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.01), run_time=2.0)
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
