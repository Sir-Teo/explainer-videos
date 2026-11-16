from __future__ import annotations

from videos.psychology.psych50.common import *  # noqa: F403


class Pool(VoiceoverScene):
    def construct(self):
        self.card()
        self.weights()
        self.forest()
        self.interval()

    def card(self):
        card = chapter_card(2, r"Combining studies", r"How do many studies make one estimate?", lit=(), part=PART,
                            scale=("society",), marr=("what",))
        with self.voiceover("Chapter two. Combining studies."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def weights(self):
        head = heading(r"Two models of a literature")
        fe = MathTex(r"\text{fixed: } y_i = \mu + e_i,\quad \hat\mu = \frac{\sum w_i y_i}{\sum w_i},\quad w_i = "
                     r"\frac{1}{v_i}", font_size=32, color=SYMP)
        re = MathTex(r"\text{random: } y_i = \mu + u_i + e_i,\quad u_i \sim N(0, \tau^2),\quad w_i = \frac{1}{v_i + "
                     r"\tau^2}", font_size=32, color=MODEL)
        eqs = VGroup(fe, re).arrange(DOWN, buff=0.45).move_to([0, 1.3, 0])
        rows = rows_of([
            (r"fixed effect: \ every study estimates the same true effect; \ weight each by its precision", SYMP),
            (r"random effects: \ each study has its own true effect, \ spread with SD $\tau$ around a mean", MODEL),
            (r"with $\tau > 0$, \ big studies count for less and small ones for more than under fixed weights; \ "
             r"$I^2$ is the share of the variation that is real", PERSON),
            (r"psychology's effects vary with samples, \ materials and labs: \ random effects is the usual default "
             r"(\emph{Statistics, Built} Part 25 derives both)", YOU),
        ], 12.4, 21, 0.34).move_to([0, -1.7, 0])
        tag = published_tag(r"Borenstein et al.\ (2009)")
        with self.voiceover(
            "There are two models of a literature. <bookmark mark='a'/> The fixed-effect model says every study "
            "estimates the same true effect, so each is weighted by its precision. <bookmark mark='b'/> The "
            "random-effects model says each study has its own true effect, spread with a standard deviation tau "
            "around a mean. <bookmark mark='c'/> With tau above zero, big studies count for less and small ones for "
            "more than under fixed weights, and I squared is the share of the variation that's real. "
            "<bookmark mark='d'/> Psychology's effects vary with samples, materials and labs, so random effects is the "
            "usual default. Statistics, Built derives both in its Part 25."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(fe), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(re), FadeIn(rows[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def forest(self):
        d = load("forest")
        head = heading(r"A forest plot, \ by hand")
        y, se, n = np.asarray(d["d"]), np.asarray(d["se"]), np.asarray(d["n"])
        k = len(y)
        A = axes([-0.4, 1.4], [-2.5, k + 0.5], x_length=6.0, y_length=4.8, xticks=[0, 0.5, 1.0], yticks=None,
                 xfmt=lambda v: f"{v:g}", xlabel=r"effect $d$", center=[-3.0, -0.1, 0], font_size=12)
        zero = DashedLine(A.ax.c2p(0, -2.5), A.ax.c2p(0, k + 0.5), color=GREY_D, stroke_width=1)
        lines = VGroup()
        for i in range(k):
            yy = k - i
            lines.add(Line(A.ax.c2p(y[i] - 1.96 * se[i], yy), A.ax.c2p(y[i] + 1.96 * se[i], yy), color=GREY_B,
                           stroke_width=2))
            w = 1 / (se[i] ** 2 + d["tau"] ** 2)
            lines.add(Square(0.05 + 0.006 * np.sqrt(w), stroke_width=0, fill_color=SYMP, fill_opacity=1)
                      .move_to(A.ax.c2p(y[i], yy)))
        dia = Polygon(A.ax.c2p(d["lo"], -1), A.ax.c2p(d["mu"], -0.6), A.ax.c2p(d["hi"], -1), A.ax.c2p(d["mu"], -1.4),
                      stroke_width=0, fill_color=THRESH, fill_opacity=1)
        pi = Line(A.ax.c2p(d["pi_lo"], -2.0), A.ax.c2p(d["pi_hi"], -2.0), color=AUTH, stroke_width=4)
        rows = rows_of([
            (r"15 simulated studies (true mean 0.4, \ $\tau$ = 0.15); \ square size is weight", WHITE),
            (rf"random effects: \ $\hat\mu$ = {d['mu']:.2f}, \ 95\% interval {d['lo']:.2f} to {d['hi']:.2f} "
             rf"(the gold diamond)", THRESH),
            (rf"$\hat\tau$ = {d['tau']:.2f}, \ $I^2$ = {100 * d['I2']:.0f}\%: \ about half the spread between studies "
             rf"is real", MODEL),
            (rf"the red line: \ where a new study's true effect is likely to fall, \ {d['pi_lo']:.2f} to "
             rf"{d['pi_hi']:.2f}", AUTH),
        ], 5.8, 19, 0.34).move_to([3.5, -0.1, 0])
        tag = psyche_tag(r"\texttt{meta.random\_effects}")
        with self.voiceover(
            "Here's a forest plot, built by hand. <bookmark mark='a'/> Fifteen simulated studies, each a square sized "
            "by its weight, with its interval. <bookmark mark='b'/> The random-effects mean is about zero point four "
            "one, with an interval from about zero point three to zero point five: the gold diamond. "
            "<bookmark mark='c'/> Tau is about zero point one seven, and I squared about half: half the spread between "
            "studies is real. <bookmark mark='d'/> And the red line is the prediction interval: where a new study's "
            "true effect is likely to fall. From almost nothing to nearly zero point eight."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(zero))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[FadeIn(x) for x in lines], lag_ratio=0.04), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(dia))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), Create(pi))
        self.clear_scene()

    def interval(self):
        head = heading(r"Which interval answers your question?")
        rows = rows_of([
            (r"the confidence interval is about the average effect across studies like these", THRESH),
            (r"the prediction interval is about the effect in the next study, \ or in your setting", AUTH),
            (r"with real heterogeneity, \ the second is much wider, \ and is the one a practitioner needs", PERSON),
            (r"with few studies, \ use Hartung and Knapp's $t$-based interval: \ the usual one is too narrow", MODEL),
            (r"report $\tau$, \ not only $I^2$: \ $I^2$ depends on how precise the studies are, \ $\tau$ is in the "
             r"units of the effect", YOU),
        ], 12.4, 22, 0.42).move_to([0, -0.3, 0])
        with self.voiceover(
            "Two intervals, two questions. <bookmark mark='a'/> The confidence interval is about the average effect "
            "across studies like these. <bookmark mark='b'/> The prediction interval is about the effect in the next "
            "study, or in your own setting. <bookmark mark='c'/> With real heterogeneity the second is much wider, and "
            "it's the one a practitioner needs. <bookmark mark='d'/> With few studies, use Hartung and Knapp's "
            "t-based interval, because the usual one is too narrow. <bookmark mark='e'/> And report tau, not only I "
            "squared. I squared depends on how precise the studies are. Tau is in the units of the effect."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
