from __future__ import annotations

from videos.psychology.psych47.common import *  # noqa: F403


class Shrink(VoiceoverScene):
    def construct(self):
        self.card()
        self.shrinkage()
        self.weight()

    def card(self):
        card = chapter_card(3, r"Random intercepts and slopes", r"What is one person's slope?", lit={1977: r"Efron \& Morris"},
                            part=PART, scale=("person",), marr=("how",))
        with self.voiceover("Chapter three. Random intercepts and slopes."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def shrinkage(self):
        d = load("slopes")
        head = heading(r"Partial pooling")
        A = axes([-0.4, 1.4], [0, 4], x_length=6.0, y_length=3.4, xticks=[0, 0.5, 1], yticks=None,
                 xfmt=lambda v: f"{v:g}", xlabel=r"slope", center=[-3.0, 0.2, 0], font_size=13)
        order = np.argsort(d["ols"])[::2]
        lines = VGroup()
        for k, i in enumerate(order):
            y = 3.5 - 3.0 * k / len(order)
            lines.add(VGroup(Dot(A.ax.c2p(d["ols"][i], y), radius=0.05, color=AUTH),
                             Arrow(A.ax.c2p(d["ols"][i], y), A.ax.c2p(d["blup"][i], y), buff=0, color=MODEL,
                                   stroke_width=2, max_tip_length_to_length_ratio=0.25),
                             Dot(A.ax.c2p(d["true"][i], y), radius=0.04, color=YOU)))
        mean = DashedLine(A.ax.c2p(d["beta"][1], 0), A.ax.c2p(d["beta"][1], 4), color=GREY_B, stroke_width=1.5)
        key = VGroup(label(r"own line", font_size=13, color=AUTH), label(r"multilevel", font_size=13, color=MODEL),
                     label(r"truth", font_size=13, color=YOU)).arrange(RIGHT, buff=0.4).next_to(A, UP, buff=0.05)
        rows = rows_of([
            (r"Psyche: \ 40 people, \ 15 noisy observations each, \ slopes that truly differ (SD 0.3)", WHITE),
            (r"each person's own regression is unbiased but noisy; \ the multilevel model pulls each slope toward the "
             r"average, \ more for noisier people", MODEL),
            (rf"the error falls from {d['rmse_ols']:.2f} to {d['rmse_blup']:.2f}: \ borrowing strength from everyone "
             rf"else describes each person better", GOOD),
            (r"James and Stein's shrinkage (\emph{Statistics, Built}), \ here for people: \ but it "
             r"assumes each person is like the others", PERSON),
        ], 5.6, 19, 0.38).move_to([3.6, -0.1, 0])
        tag = psyche_tag(r"\texttt{within.person\_slopes}; \ statkit's \texttt{lmm}")
        with self.voiceover(
            "What's one person's slope? <bookmark mark='a'/> Psyche makes forty people, with fifteen noisy "
            "observations each, whose slopes truly differ. <bookmark mark='b'/> Each person's own regression is "
            "unbiased but noisy. The multilevel model pulls each slope toward the average, more for noisier people. "
            "It's called partial pooling. <bookmark mark='c'/> The error falls by about a third. Borrowing strength "
            "from everyone else describes each person better. <bookmark mark='d'/> It's the shrinkage of James and "
            "Stein, here for people. But it assumes each person is like the others."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key), FadeIn(mean))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[FadeIn(l[0]) for l in lines], lag_ratio=0.05), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), LaggedStart(*[GrowArrow(l[1]) for l in lines], lag_ratio=0.05), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(VGroup(*[l[2] for l in lines])))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def weight(self):
        d = load("shrinkw")
        head = heading(r"How much to trust one person")
        eq = MathTex(r"\hat b_p = w\,\hat b_p^{\text{own}} + (1 - w)\,\hat\beta, \qquad "
                     r"w = \frac{G}{G + \sigma^2 / (n\,s_x^2)}", font_size=34, color=MODEL).move_to([0, 2.0, 0])
        A = axes([0, 62], [0, 1], x_length=5.6, y_length=2.8, xticks=[0, 15, 30, 45, 60], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"observations per person",
                 ylabel=r"weight on own slope", center=[-3.3, -0.9, 0], font_size=13)
        c = curve(A.ax, d["n"], d["w"], MODEL, stroke_width=4)
        w15 = float(d["w"][list(d["n"]).index(15)])
        rows = rows_of([
            (r"the multilevel estimate is a weighted average of the person's own slope and the population's", WHITE),
            (r"the weight is the share of the variation in own slopes that is real, \ not noise", MODEL),
            (rf"with 15 observations each, \ the model gives each person's own slope a weight of {w15:.2f}; \ "
             rf"with 60, \ most of it", PERSON),
            (r"so people with fewer data are pulled further: \ fair to the data, \ but unusual people with few "
             r"observations will look more ordinary than they are", AUTH),
        ], 6.0, 19, 0.38).move_to([3.4, -0.6, 0])
        with self.voiceover(
            "How hard does the model pull? <bookmark mark='a'/> The multilevel estimate is a weighted average of the "
            "person's own slope and the population's. <bookmark mark='b'/> The weight is the share of the variation "
            "in own slopes that's real rather than noise. <bookmark mark='c'/> With fifteen observations each, the "
            "model gives each person's own slope a weight of a little over a half. With sixty, most of the weight. "
            "<bookmark mark='d'/> So people with fewer data are pulled further. That's fair to the data, but an "
            "unusual person with few observations will look more ordinary than they are."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eq), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(c))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
