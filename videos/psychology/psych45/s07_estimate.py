from __future__ import annotations

from videos.psychology.psych45.common import *  # noqa: F403


class Estimate(VoiceoverScene):
    def construct(self):
        self.card()
        self.three_ways()
        self.em()
        self.ability()

    def card(self):
        card = chapter_card(6, r"Estimation", r"How do you estimate items when no one's ability is known?",
                            lit={1970: r"Bock \& Lieberman", 1981: r"Bock \& Aitkin"}, part=PART, scale=("person",),
                            marr=("how",))
        with self.voiceover("Chapter six. Estimation."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def three_ways(self):
        head = heading(r"Three ways to estimate items")
        data = (
            (r"joint", r"estimate every person's ability and every item together; \ the abilities multiply with the "
                       r"people, \ and the item estimates stay biased however many people you add (the "
                       r"Neyman-Scott problem)", AUTH),
            (r"conditional", r"condition on each person's sum score, \ so ability vanishes (chapter 3); \ exact, \ but "
                             r"only for the Rasch model", SYMP),
            (r"marginal", r"treat ability as drawn from a population, \ say normal, \ and integrate it out: \ the "
                          r"likelihood of each answer pattern, \ averaged over abilities", MODEL),
        )
        rows = VGroup()
        for name, how, c in data:
            rows.add(VGroup(word_chip(name, color=c, font_size=18, width=2.6), wrapped_label(how, 9.2, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, 0.4, 0])
        eq = MathTex(r"L(a, b) = \prod_p \int \prod_i P_i(\theta)^{x_{pi}}\,\big(1 - P_i(\theta)\big)^{1 - x_{pi}}\,"
                     r"\phi(\theta)\,d\theta", font_size=34, color=MODEL).move_to([0, -2.4, 0])
        with self.voiceover(
            "Here's the puzzle. To estimate the items, you need the people's abilities, and to estimate abilities, "
            "you need the items. <bookmark mark='a'/> The joint approach estimates both at once. But the abilities "
            "multiply with the people, and the item estimates stay biased however many people you add. "
            "<bookmark mark='b'/> The conditional approach conditions on each sum score, so ability vanishes. It's "
            "exact, but only for the Rasch model. <bookmark mark='c'/> The marginal approach treats ability as drawn "
            "from a population, say a normal one, and integrates it out. <bookmark mark='d'/> The likelihood of each "
            "answer pattern, averaged over abilities."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(eq))
        self.clear_scene()

    def em(self):
        d = load("em")
        head = heading(r"Bock and Aitkin's EM")
        A = axes([0, 40], [-2476, -2466], x_length=5.2, y_length=3.0, xticks=[0, 10, 20, 30, 40],
                 yticks=[-2475, -2470, -2466], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                 xlabel=r"EM cycle", ylabel=r"log-likelihood", center=[-3.4, 0.2, 0], font_size=13)
        tr = curve(A.ax, np.arange(1, 41), d["trace"], MODEL, stroke_width=4)
        rows = rows_of([
            (r"replace the integral by a grid of abilities, \ weighted by the normal curve", WHITE),
            (r"E step: \ for each person, \ the posterior over the grid, \ given their answers and the current items",
             SYMP),
            (r"M step: \ each item becomes a weighted logistic regression on the grid: \ expected people and expected "
             r"right answers at each ability", MODEL),
            (rf"on the LSAT: \ the log-likelihood climbs to {d['trace'][-1]:.1f} and stops; \ the estimates match the "
             rf"published fits to three decimals", GOOD),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{irt.fit\_mml}; \ checked by direct maximization and against ltm")
        with self.voiceover(
            "Darrell Bock and Murray Aitkin made the marginal approach practical in 1981, with EM. "
            "<bookmark mark='a'/> Replace the integral by a grid of abilities, weighted by the normal curve. "
            "<bookmark mark='b'/> In the E step, find each person's posterior over the grid, given their answers and "
            "the current items. <bookmark mark='c'/> In the M step, each item becomes a weighted logistic regression "
            "on the grid: so many expected people, and so many expected right answers, at each ability. "
            "<bookmark mark='d'/> On the law-school items, the log-likelihood climbs and stops. The estimates match "
            "the published fits to three decimal places."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(tr), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def ability(self):
        d = load("em")
        head = heading(r"Then each person's ability")
        A = axes([-0.5, 5.5], [-3, 2], x_length=5.2, y_length=3.2, xticks=[0, 1, 2, 3, 4, 5], yticks=[-3, -2, -1, 0, 1, 2],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"sum score (of 5)",
                 ylabel=r"ability", center=[-3.4, 0.2, 0], font_size=13)
        bars_ = VGroup(*[Line(A.ax.c2p(r, d["eap"][r] - 1.96 * d["sd"][r]), A.ax.c2p(r, min(2, d["eap"][r] + 1.96 * d["sd"][r])),
                              color=MODEL, stroke_width=5, stroke_opacity=0.5) for r in range(6)])
        dots = VGroup(*[Dot(A.ax.c2p(r, d["eap"][r]), radius=0.07, color=MODEL) for r in range(6)])
        mle = VGroup(*[Dot(A.ax.c2p(r, d["mle"][r]), radius=0.06, color=PERSON) for r in range(1, 5)])
        rows = rows_of([
            (r"maximum likelihood: \ the ability that makes the answers most likely; \ infinite for all right or all "
             r"wrong (yellow, \ scores 1 to 4 only)", PERSON),
            (r"expected a posteriori: \ the mean of the posterior, \ with the population as prior: \ always finite, \ "
             r"pulled toward the mean", MODEL),
            (rf"with five items, \ the posterior SD stays near {d['sd'].mean():.1f}: \ the prior's 1 barely shrinks", AUTH),
            (r"the shrinkage is right for one person's best guess, \ and wrong for describing a population (chapter "
             r"11)", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{irt.eap}, \ \texttt{irt.mle\_theta}; \ the LSAT's Rasch fit")
        with self.voiceover(
            "With the items known, each person's ability follows. <bookmark mark='a'/> Maximum likelihood finds the "
            "ability that makes the answers most likely. For all right or all wrong, it's infinite. "
            "<bookmark mark='b'/> The expected a posteriori estimate is the mean of the posterior, with the "
            "population as the prior. It's always finite, and pulled toward the mean. <bookmark mark='c'/> With five "
            "items, the posterior standard deviation stays near zero point eight. The prior's one barely shrinks. "
            "<bookmark mark='d'/> That shrinkage is right for one person's best guess, and wrong for describing a "
            "population, as chapter eleven will show."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(mle))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(bars_), FadeIn(dots))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
