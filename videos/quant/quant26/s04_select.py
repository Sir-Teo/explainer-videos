from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant26.common import BAD, HURDLE, NOISE, PART, RULE, ask, fit_right, illustration, load


class Select(VoiceoverScene):
    def construct(self):
        s = load("select")
        self.card()
        self.slide(s)
        self.derive()
        self.formula(s)
        self.butter()
        self.forks()
        self.question()

    def card(self):
        c = chapter_card(3, r"Selection: the best of many", r"How good does the best of N look by chance?", lit=(2014,),
                         part=PART)
        with self.voiceover("Chapter three. Selection: what the best of many strategies looks like when none of them "
                            "works."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def slide(self, s):
        d = s["dist"]
        ns = ["1", "10", "100", "1000", "10000"]
        e = np.asarray(d["1"]["edges"])
        c = (e[:-1] + e[1:]) / 2
        top = max(max(d[n]["hist"]) for n in ns) * 1.08
        g = axes([-1.5, 3.0], [0, top], x_length=8.0, y_length=4.2, xlabel=r"the best annualised Sharpe ratio among $N$ "
                 r"strategies of pure noise (five years of daily returns)", ylabel=r"density", xticks=[-1, 0, 1, 2, 3],
                 yticks=[], font_size=14).to_edge(LEFT, buff=0.5).shift(DOWN * 0.2)
        ax = g.ax
        cols = [NOISE, interpolate_color(ManimColor(NOISE), ManimColor(HURDLE), 0.3),
                interpolate_color(ManimColor(NOISE), ManimColor(HURDLE), 0.6), HURDLE, BAD]

        def shape(n, col):
            h = np.asarray(d[n]["hist"])
            pts = [ax.c2p(e[0], 0)] + [ax.c2p(x, v) for x, v in zip(c, h)] + [ax.c2p(e[-1], 0)]
            return VMobject(color=col, stroke_width=2.5, fill_color=col, fill_opacity=0.25).set_points_smoothly(pts)
        shapes = [shape(n, col) for n, col in zip(ns, cols)]
        tags = VGroup(*[MathTex(rf"N = {int(n):,}".replace(",", "{,}") + rf":\ {d[n]['mean']:.2f}", font_size=24,
                                color=col) for n, col in zip(ns, cols)]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        side = VGroup(tags, wrapped_label(r"the average best, from 2,000 simulated draws of each $N$. No strategy has any "
                                          r"edge; only the number of tries changes".replace("2,000", "2{,}000"), 3.4,
                                          15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "One strategy of pure noise, tested on five years of daily returns. Its Sharpe ratio is centred on zero, "
            "with a spread of about point four five: five years is not long. <bookmark mark='a'/> Now try ten and keep "
            "the best. The best of ten averages point seven. <bookmark mark='b'/> The best of a hundred, one point one. "
            "The best of a thousand, one point five. <bookmark mark='c'/> And the best of ten thousand, about one point "
            "seven, a number that would be called excellent in any hedge fund's marketing. The strategies have not "
            "changed. Only the number of tries has, and the distribution of the winner slides to the right with it."
        ) as vo:
            self.play(FadeIn(g), DrawBorderThenFill(shapes[0]), FadeIn(tags[0]))
            vo.wait_until("a")
            self.play(DrawBorderThenFill(shapes[1]), FadeIn(tags[1]))
            vo.wait_until("b")
            self.play(DrawBorderThenFill(shapes[2]), FadeIn(tags[2]))
            self.play(DrawBorderThenFill(shapes[3]), FadeIn(tags[3]))
            vo.wait_until("c")
            self.play(DrawBorderThenFill(shapes[4]), FadeIn(tags[4]), FadeIn(side[1]))
        self.add(illustration(r"simulated: the House's \texttt{backtest.noise\_max\_sr}"))
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"\Pr\big(\max_{i \le N} Z_i \le c\big)", r"=", r"\Phi(c)^N", font_size=38,
                      colors={r"\Phi(c)^N": HURDLE}),
                cmath(r"\Phi(c_N)", r"=", r"1 - \tfrac{1}{N}", font_size=38, colors={r"\Phi(c_N)": WHITE}),
                cmath(r"\mathbb{E}\big[\max_i Z_i\big]", r"\approx", r"(1 - \gamma)\,\Phi^{-1}\!\big(1 - \tfrac1N\big) + "
                      r"\gamma\,\Phi^{-1}\!\big(1 - \tfrac{1}{Ne}\big)", font_size=34,
                      colors={r"\mathbb{E}\big[\max_i Z_i\big]": HURDLE}),
                cmath(r"\mathbb{E}\big[\max_i \widehat{SR}_i\big]", r"\approx", r"\sqrt{V}\,\Big[(1 - \gamma)\,\Phi^{-1}"
                      r"\!\big(1 - \tfrac1N\big) + \gamma\,\Phi^{-1}\!\big(1 - \tfrac{1}{Ne}\big)\Big]", font_size=32,
                      colors={r"\mathbb{E}\big[\max_i \widehat{SR}_i\big]": HURDLE})]
        whys = [why(r"$N$ independent standard normals: the maximum is below $c$ only if every one of them is"),
                why(r"the typical size of the maximum: the level that one draw in $N$ exceeds"),
                why(r"extreme-value theory: the normal maximum converges to a Gumbel law, whose mean adds Euler's "
                    r"$\gamma \approx 0.5772$ of the way to the next scale; it grows like $\sqrt{2 \ln N}$"),
                why(r"Sharpe estimates of zero-skill strategies are close to normal with variance $V$ (for $T$ "
                    r"independent periods, $V \approx 1/T$): the hurdle the best of $N$ must clear (Bailey and Lopez de "
                    r"Prado, 2014)")]
        step = ladder(self, rows, whys, keep=4, top=3.2, x=-0.5, buff=0.32, edge=6.9)
        with self.voiceover(
            "Why does it slide, and how fast? <bookmark mark='a'/> Take N independent standard normal draws. The "
            "largest is below c only if every one is, so the probability is Phi of c to the power N. "
            "<bookmark mark='b'/> The maximum is typically near the level that one draw in N exceeds. <bookmark "
            "mark='c'/> Extreme-value theory makes this precise: the maximum of normals converges to a Gumbel "
            "distribution, and its mean sits a fraction gamma, Euler's constant, of the way from the one-in-N level to "
            "the one-in-N-e level. It grows like the square root of two log N: slowly, but without limit. "
            "<bookmark mark='d'/> Sharpe ratio estimates of strategies with no skill are close to normal, with "
            "variance V, about one over the number of periods. Scale by the square root of V, and this is the hurdle: "
            "the Sharpe ratio the best of N should reach by luck alone."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def formula(self, s):
        grid, evt = np.log10(np.asarray(s["grid"])), np.asarray(s["evt"])
        g = axes([0, 6], [0, 3.0], x_length=7.6, y_length=4.2, xlabel=r"$N$, strategies tried",
                 ylabel=r"expected best Sharpe ratio, annualised (five years)", xticks=[0, 1, 2, 3, 4, 5, 6],
                 yticks=[0, 1, 2, 3], log_x=True, font_size=14).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, grid, evt, HURDLE, stroke_width=3)
        sims = VGroup(*[Dot(ax.c2p(np.log10(int(n)), s["dist"][n]["mean"]), color=RULE, radius=0.07)
                        for n in ("10", "100", "1000", "10000")])
        bars = VGroup(*[Line(ax.c2p(np.log10(int(n)), s["dist"][n]["q05"]), ax.c2p(np.log10(int(n)), s["dist"][n]["q95"]),
                             color=RULE, stroke_width=2) for n in ("10", "100", "1000", "10000")])
        leg = legend([(HURDLE, r"the extreme-value formula"), (RULE, r"simulation: mean, 5--95\%")], font_size=16).next_to(
            ax, UP, buff=0.1).align_to(ax, LEFT).shift(RIGHT * 0.3)
        side = VGroup(
            MathTex(rf"N = 10^6:\ {evt[-1]:.2f}", font_size=28, color=HURDLE),
            wrapped_label(r"a million configurations is a morning's work for a parameter sweep on a laptop. The formula "
                          r"tracks the simulations; its error is small next to the spread of the winner", 3.4, 15, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        fit_right(side)
        with self.voiceover(
            "The formula against the simulations. <bookmark mark='a'/> It tracks them across four orders of magnitude, "
            "and the spread of the winner, the thin lines, is wider than the formula's error. <bookmark mark='b'/> "
            "Carry it on to a million configurations, a morning's work for a parameter sweep on a laptop, and five years "
            "of noise will hand you a Sharpe ratio above two. If you do not know how many configurations were tried, "
            "you do not know what a backtest's Sharpe ratio means."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(sims), FadeIn(bars), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def butter(self):
        card = crisis_card(r"1995, published 2007", r"Butter in Bangladesh",
                           r"David Leinweber, then at First Quadrant, searched a United Nations database of economic "
                           r"series for the best predictor of the S\&P 500's annual return over ten years, as a warning to "
                           r"colleagues. His 'Stupid Data Miner Tricks' found butter production in Bangladesh; adding US "
                           r"cheese production and the sheep populations of Bangladesh and the US fitted almost perfectly",
                           stats=((r"75\%", r"$R^2$ from Bangladeshi butter alone"),
                                  (r"99\%", r"$R^2$ with cheese and sheep added")), width=8.6, font_size=22)
        card.move_to(ORIGIN)
        src = note(r"Leinweber, D. (2007), ``Stupid data miner tricks: overfitting the S\&P 500'', \textit{Journal of "
                   r"Investing}", font_size=16, color=GREY_C).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The point has been made as a joke. In 1995 David Leinweber, then at the asset manager First Quadrant, "
            "searched a United Nations database of economic series for the best predictor of the S and P five hundred's "
            "annual return, as a warning to his colleagues. <bookmark mark='a'/> The winner was butter production in "
            "Bangladesh, which explained three quarters of the variation. Adding American cheese production and the "
            "sheep populations of Bangladesh and the United States explained ninety-nine percent. Leinweber published "
            "it in 2007 as 'Stupid Data Miner Tricks'. Every search finds its butter. The question is only whether you "
            "can tell."
        ) as vo:
            self.play(FadeIn(card), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[Indicate(s_, color=QC.CRISIS) for s_ in card.stats], lag_ratio=0.5))
        self.wait(0.4)
        self.clear_scene()

    def forks(self):
        cards = VGroup(
            desk_question(r"the sweep", r"a lookback of 10 to 250 days, a threshold, a holding period: a grid of a few "
                          r"hundred is $N$ in the hundreds, even if only the best cell is shown", width=12.2, font_size=19),
            desk_question(r"the quiet choices", r"the start date, the universe, the rebalancing day, the treatment of "
                          r"outliers, the cost model: each tried and kept multiplies $N$", width=12.2, font_size=19),
            desk_question(r"the colleagues", r"ten analysts each testing ten ideas and reporting their best make a "
                          r"firm's $N$ a hundred; the firm's research report shows ten", width=12.2, font_size=19),
            desk_question(r"the literature", r"published results are a selection from everyone's tries: Part 25's zoo",
                          width=12.2, font_size=19),
        ).arrange(DOWN, buff=0.2)
        if cards.height > 7.0:
            cards.scale_to_fit_height(7.0)
        with self.voiceover(
            "Where does N come from in practice? <bookmark mark='a'/> The parameter sweep: a lookback from ten to two "
            "hundred and fifty days, a threshold, a holding period. A grid of a few hundred cells is N in the hundreds, "
            "even if only the best cell is shown. <bookmark mark='b'/> The quiet choices: the start date, the universe, "
            "the rebalancing day, the treatment of outliers, the cost model. <bookmark mark='c'/> The colleagues: ten "
            "analysts each testing ten ideas and reporting their best give the firm an N of a hundred, though its "
            "report shows ten. <bookmark mark='d'/> And the literature itself, the zoo of Part twenty-five, which is a "
            "selection from everyone's tries."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = ask(r"you sweep 400 parameter settings of one idea on ten years of daily data and the best has an "
                r"annualised Sharpe ratio of 1.2. Is it better than noise? What else would you need to know?")
        with self.voiceover(
            "Pause and predict. You sweep four hundred parameter settings of one idea on ten years of daily data, and "
            "the best has a Sharpe ratio of one point two. Is it better than noise, and what else would you need to "
            "know?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
