from __future__ import annotations

from videos.psychology.psych42.common import *  # noqa: F403


class Meta(VoiceoverScene):
    def construct(self):
        self.card()
        self.glass()
        self.forest()

    def card(self):
        card = chapter_card(3, r"Meta-analysis is born", r"How do you add up 375 studies?",
                            lit={1976: r"Glass", 1977: r"Smith \& Glass"}, part=PART, scale=("person",),
                            marr=("what", "how"))
        with self.voiceover("Chapter three. Meta-analysis is born."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def glass(self):
        head = heading(r"One scale for every study")
        eq = MathTex(r"d = \frac{\bar{x}_{\text{control}} - \bar{x}_{\text{treated}}}{s}", font_size=40,
                     color=MODEL).move_to([-3.6, 0.9, 0])
        A = axes([-3, 4], [0, 0.45], x_length=5.0, y_length=2.0, xticks=None, yticks=None, center=[-3.6, -1.4, 0],
                 font_size=12)
        x = np.linspace(-3, 4, 300)
        ctrl = curve(A.ax, x, np.exp(-x ** 2 / 2) / np.sqrt(2 * np.pi), GREY_B, stroke_width=3)
        trt = curve(A.ax, x, np.exp(-(x - 0.68) ** 2 / 2) / np.sqrt(2 * np.pi), GOOD, stroke_width=3)
        l = label(r"shifted by 0.68 SD: \ the average treated client is better off than 75\% of the untreated",
                  font_size=13, color=GOOD).next_to(A, DOWN, buff=0.2)
        rows = rows_of([
            (r"Glass, \ 1976, \ named it meta-analysis: \ the analysis of analyses", WHITE),
            (r"every outcome, \ on every scale, \ becomes a standardized difference $d$", MODEL),
            (r"Smith and Glass, \ 1977: \ 375 controlled studies, \ an average $d$ of 0.68", GOOD),
            (r"critics called it ``mega-silliness'': \ good and bad studies mixed, \ and apples with oranges", AUTH),
        ], 6.0, 20, 0.4).move_to([3.4, -0.2, 0])
        tag = published_tag(r"Smith \& Glass (1977)")
        with self.voiceover(
            "To answer Eysenck, the studies had to be put on one scale. <bookmark mark='a'/> In 1976 Gene Glass named "
            "the method meta-analysis, the analysis of analyses. <bookmark mark='b'/> Every outcome, on every scale, "
            "becomes a standardized difference: the gap between the groups, in units of the spread. "
            "<bookmark mark='c'/> Smith and Glass applied it to three hundred and seventy-five controlled studies. The "
            "average effect was zero point six eight. The average treated client ended better off than three "
            "quarters of the untreated. <bookmark mark='d'/> Eysenck called it mega-silliness: good studies and bad "
            "mixed together, apples with oranges. The answer to that would be to weigh studies by their quality, and "
            "by their size."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(eq))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(ctrl), Create(trt), FadeIn(l))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def forest(self):
        d = load("forest")
        head = heading(r"A forest plot, \ by hand")
        k = len(d["d"])
        A = axes([-0.6, 1.6], [-1.5, k + 0.5], x_length=5.6, y_length=4.6, xticks=[0, 0.5, 1, 1.5], yticks=None,
                 xfmt=lambda v: f"{v:g}", xlabel=r"effect size $d$", center=[-3.3, 0.1, 0], font_size=13)
        rows_g = VGroup()
        wmax = float(np.max(1 / d["v"]))
        for i, (y, v) in enumerate(zip(d["d"], d["v"])):
            yy = k - i
            se = np.sqrt(v)
            rows_g.add(VGroup(Line(A.ax.c2p(max(-0.6, y - 1.96 * se), yy), A.ax.c2p(min(1.6, y + 1.96 * se), yy),
                                   color=GREY_A, stroke_width=2),
                              Square(0.06 + 0.16 * np.sqrt((1 / v) / wmax), stroke_width=0, fill_color=PERSON,
                                     fill_opacity=1).move_to(A.ax.c2p(y, yy))))
        mu, se = d["mu"], d["se"]
        diamond = Polygon(A.ax.c2p(mu - 1.96 * se, -0.6), A.ax.c2p(mu, -0.25), A.ax.c2p(mu + 1.96 * se, -0.6),
                          A.ax.c2p(mu, -0.95), stroke_width=0, fill_color=GOOD, fill_opacity=1)
        zero = DashedLine(A.ax.c2p(0, -1.5), A.ax.c2p(0, k + 0.5), color=GREY_B, stroke_width=1.5)
        eqs = VGroup(MathTex(r"w_i = \frac{1}{v_i + \hat\tau^2}", font_size=28, color=MODEL),
                     MathTex(r"\hat\mu = \frac{\sum w_i d_i}{\sum w_i}, \quad \mathrm{SE} = \frac{1}{\sqrt{\sum w_i}}",
                             font_size=28, color=MODEL)).arrange(DOWN, buff=0.25)
        rows = rows_of([
            (r"twelve simulated trials: \ each a square sized by its weight, \ with its 95\% interval", WHITE),
            (r"random effects (DerSimonian and Laird): \ each trial has its own true effect, \ spread by $\tau$; \ "
             r"weights fall as $\tau^2$ grows", MODEL),
            (rf"pooled: \ $\hat\mu = {d['mu']:.2f}$, \ SE {d['se']:.2f}, \ $\hat\tau^2 = {d['tau2']:.3f}$, \ "
             rf"$I^2 = {100 * d['I2']:.0f}\%$; \ the truth was 0.5", GOOD),
            (r"the mathematics, \ and how to read heterogeneity, \ is Part 50", YOU),
        ], 5.8, 19, 0.34).move_to([3.5, 0.6, 0])
        eqs.next_to(rows, DOWN, buff=0.35)
        tag = psyche_tag(r"\texttt{clinic.random\_effects}")
        with self.voiceover(
            "Here's a meta-analysis by hand. <bookmark mark='a'/> Twelve simulated trials, each drawn as a square "
            "sized by its weight, with its ninety-five percent interval. Small trials have wide intervals. "
            "<bookmark mark='b'/> The random-effects model of DerSimonian and Laird lets each trial have its own true "
            "effect, spread by a standard deviation tau. Each trial is weighted by one over its variance plus tau "
            "squared. <bookmark mark='c'/> The pooled effect, the green diamond, lands close to the true value of a "
            "half. <bookmark mark='d'/> The mathematics, and how to read heterogeneity, is Part 50."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(zero))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[FadeIn(r) for r in rows_g], lag_ratio=0.2), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(eqs))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(diamond))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
