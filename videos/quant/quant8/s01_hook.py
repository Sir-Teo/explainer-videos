from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant8.common import ALT, GOOD, KELLY, OVER, PART, UNDER, VALUE, illustration, load, tbar


class Hook(VoiceoverScene):
    def construct(self):
        c = load("coin")
        live = load("coin_live")
        self.title_card()
        self.game(c)
        self.live(live)
        self.answer(c)
        self.history()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"How much to bet")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part eight. Decisions and control. Part seven forecast how much the market will move. This part asks "
            "the question every trader faces next: given what you believe, how much should you bet?"
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def game(self, c):
        q = desk_question(r"You have \$25 and a coin that lands heads 60\% of the time. For 30 minutes you may bet any "
                          r"amount on either side, at even odds, as often as you like; winnings are capped at \$250. "
                          r"How much do you bet each time?", width=10.6, font_size=28).to_edge(UP, buff=0.5)
        facts = VGroup(
            label(r"Haghani and Dewey (2016) gave this game to 61 people trained in finance and economics.",
                  font_size=24, color=GREY_A),
            label(r"About 30\% of them went bust.", font_size=30, color=OVER),
            label(r"Many over-bet, some bet erratically, some even bet on tails.", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(q, DOWN, buff=0.6)
        with self.voiceover(
            "Here is a game. You get twenty-five dollars and a coin that lands heads sixty percent of the time. For half "
            "an hour you may bet any amount, on either side, at even odds, as often as you like, up to winnings of two "
            "hundred and fifty dollars. How much do you bet? <bookmark mark='a'/> In 2016 Victor Haghani and Richard Dewey "
            "gave this game to sixty-one people trained in finance and economics. About thirty percent of them went bust."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(f) for f in facts], lag_ratio=0.6, run_time=4))
        self.wait(0.5)
        self.clear_scene()

    def live(self, L):
        fr = ["0.1", "0.2", "0.4", "1.0"]
        cols = [UNDER, KELLY, ALT, OVER]
        g = axes([0, 4], [-2, 2.5], x_length=8.2, y_length=5.0, ylabel=r"wealth (log scale)", xticks=[],
                 yticks=[-2, -1, 0, 1, 2], yfmt=lambda u: {-2: r"\$0.01", -1: r"\$0.10", 0: r"\$1", 1: r"\$10",
                                                            2: r"\$100"}[int(u)], font_size=17)
        g.to_edge(LEFT, buff=0.8).shift(DOWN * 0.35)
        ax = g.ax
        cap = DashedLine(ax.c2p(0, np.log10(250)), ax.c2p(4, np.log10(250)), color=GOOD, stroke_width=2)
        capl = label(r"cap \$250", font_size=18, color=GOOD).next_to(ax.c2p(4, np.log10(250)), RIGHT, buff=0.1)
        start = DashedLine(ax.c2p(0, np.log10(25)), ax.c2p(4, np.log10(25)), color=GREY_C, stroke_width=1.5)
        startl = label(r"start \$25", font_size=18, color=GREY_B).next_to(ax.c2p(4, np.log10(25)), RIGHT, buff=0.1)
        heads = VGroup(*[label(rf"bet {100 * float(f):.0f}\%", font_size=22, color=c_).next_to(
            ax.c2p(i + 0.5, -2), DOWN, buff=0.15) for i, (f, c_) in enumerate(zip(fr, cols))])
        rng = np.random.default_rng(1)
        jit = rng.uniform(-0.38, 0.38, (4, L["n"]))
        paths = [np.asarray(L["by_fraction"][f]["logw"]) for f in fr]
        tk = ValueTracker(0)

        dots = VGroup(*[Dot(ax.c2p(i + 0.5 + jit[i, j], paths[i][j, 0]), radius=0.028, color=cols[i]).set_opacity(0.8)
                        for i in range(4) for j in range(L["n"])])

        def move(grp):
            n = int(tk.get_value())
            k = 0
            for i, P in enumerate(paths):
                y = np.clip(P[:, n], -2, 2.45)
                for j in range(len(y)):
                    grp[k].move_to(ax.c2p(i + 0.5 + jit[i, j], y[j]))
                    k += 1

        dots.add_updater(move)
        num = Integer(0, font_size=34, color=GREY_A)
        cnt = VGroup(label(r"flip", font_size=28, color=GREY_A), num).arrange(RIGHT, buff=0.2).to_corner(UR, buff=0.5)
        num.add_updater(lambda m: m.set_value(int(tk.get_value())))
        q = pause_card(r"Before the flips: which column goes bust most often, 40\% or 100\%? And does 40\% grow at "
                       r"all?", width=5.0, font_size=22).to_corner(UR, buff=0.4).shift(DOWN * 0.8)
        b = L["by_fraction"]
        res = VGroup(*[label(rf"{100 * float(f):.0f}\%: {100 * b[f]['p_cap']:.0f}\% at the cap, "
                             rf"{100 * b[f]['p_bust']:.0f}\% bust", font_size=20, color=c_)
                       for f, c_ in zip(fr, cols)]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        res.to_edge(RIGHT, buff=0.35).shift(DOWN * 0.6)
        src = illustration(r"simulation: 160 players per column, the same 300 coin flips for all")
        with self.voiceover(
            "Let the game play itself first. A hundred and sixty players in each of four columns see the same coin; each "
            "column stakes a different fraction of wealth on every flip: ten, twenty, forty or a hundred percent. "
            "<bookmark mark='a'/> Pause and predict: which column goes bust most often, forty or a hundred? Does forty "
            "grow at all? <bookmark mark='b'/> Three hundred flips, on a log scale."
        ) as vo:
            self.play(FadeIn(g), Create(cap), FadeIn(capl), Create(start), FadeIn(startl), FadeIn(heads), FadeIn(src))
            self.add(dots)
            vo.wait_until("a")
            self.play(FadeIn(q, shift=LEFT * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(q), run_time=0.5)
            self.add(cnt)
            self.play(tk.animate.set_value(300), run_time=max(vo.remaining(12.0), 12.0), rate_func=linear)
        dots.clear_updaters()
        num.clear_updaters()
        with self.voiceover(
            f"All in was wiped out: {100 * b['1.0']['p_bust']:.0f} percent went bust, because one tail takes everything. "
            "At forty percent the typical player barely grows, and the cap rescues most of them; still "
            f"{100 * b['0.4']['p_bust']:.0f} percent went bust. At twenty percent, {100 * b['0.2']['p_cap']:.0f} percent "
            "reached the cap and nobody went bust."
        ):
            self.play(LaggedStart(*[FadeIn(r_, shift=LEFT * 0.2) for r_ in res], lag_ratio=0.4, run_time=3))
        self.wait(0.4)
        self.clear_scene()

    def answer(self, c):
        f, gr = np.asarray(c["f"]), np.asarray(c["growth"])
        ok = np.isfinite(gr) & (gr > -0.06)
        g = axes([0, 0.6], [-0.06, 0.03], x_length=5.6, y_length=3.6, xlabel=r"fraction of wealth bet each flip",
                 ylabel=r"growth per flip", xticks=[0, 0.2, 0.4, 0.6], xfmt=lambda u: f"{100 * u:.0f}\\%",
                 yticks=[-0.04, 0, 0.02], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=17)
        g.to_corner(UL, buff=0.6)
        ax = g.ax
        line = curve(ax, f[ok], gr[ok], KELLY, stroke_width=4)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(0.6, 0), color=GREY_C, stroke_width=1.5)
        top = Dot(ax.c2p(0.2, c["g_kelly"]), color=KELLY)
        tl = MathTex(r"f^* = p - q = 20\%", font_size=28, color=KELLY).next_to(top, UP, buff=0.12)
        eq = MathTex(r"g(f) = p\log(1 + f) + q\log(1 - f)", font_size=30).next_to(g, DOWN, buff=0.35).align_to(g, LEFT)
        fr = [k for k in c["by_fraction"]]
        g2 = axes([0, len(fr)], [0, 1], x_length=5.8, y_length=3.6, ylabel=r"share of 20{,}000 simulated players",
                  xticks=[], yticks=[0, 0.5, 1], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=17)
        g2.to_corner(UR, buff=0.6)
        a2 = g2.ax
        cap = VGroup(*[tbar(a2, i + 0.3, c["by_fraction"][k]["p_cap"], KELLY if k == "0.20" else UNDER, width=0.36)
                       for i, k in enumerate(fr)])
        bust = VGroup(*[tbar(a2, i + 0.7, c["by_fraction"][k]["p_bust"], OVER, width=0.36) for i, k in enumerate(fr)])
        labs = VGroup(*[label(f"{100 * float(k):.0f}\\%", font_size=16, color=GREY_A).next_to(a2.c2p(i + 0.5, 0), DOWN,
                                                                                            buff=0.1)
                        for i, k in enumerate(fr)])
        leg = legend([(UNDER, r"reached \$250"), (OVER, r"went bust (under 1 cent)")], font_size=18)
        leg.next_to(g2, DOWN, buff=0.35).align_to(g2, LEFT)
        k20 = c["by_fraction"]["0.20"]
        k100 = c["by_fraction"]["1.00"]
        src = illustration(r"simulation: 300 flips, 20{,}000 players per fraction")
        with self.voiceover(
            "The answer is older than the game. Bet a fraction f each time, and wealth grows at p log of one plus f, plus "
            "q log of one minus f, per flip. <bookmark mark='a'/> The curve peaks at p minus q, twenty percent: the Kelly "
            "criterion, from 1956. At twice that, forty percent, growth stops; beyond it, a sure edge makes you poorer. "
            "<bookmark mark='b'/> With twenty thousand players per fraction: at twenty percent, "
            f"{100 * k20['p_cap']:.0f} percent reach the cap and none go bust; all in, {100 * k100['p_bust']:.0f} percent "
            "go bust."
        ) as vo:
            self.play(FadeIn(g), Create(zero), Create(line), FadeIn(eq), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(top), FadeIn(tl))
            vo.wait_until("b")
            self.play(FadeIn(g2), FadeIn(labs), FadeIn(leg), FadeIn(src),
                      LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in cap], lag_ratio=0.1),
                      LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bust], lag_ratio=0.1), run_time=3)
        self.wait(0.5)
        self.clear_scene()

    def history(self):
        # a strip from 1730 to 2020 with a break: Bernoulli far left, then 1940-2020 to scale
        x0, x1 = -5.6, 6.2

        def X(y):
            return -6.4 if y < 1900 else x0 + (x1 - x0) * (y - 1940) / (2020 - 1940)

        line = VGroup(Line([-6.6, 0, 0], [-6.1, 0, 0], color=GREY_D, stroke_width=2),
                      Line([x0 - 0.2, 0, 0], [x1, 0, 0], color=GREY_D, stroke_width=2),
                      label(r"//", font_size=20, color=GREY_D).move_to([-5.95, 0, 0]))
        for yr in (1940, 1960, 1980, 2000, 2020):
            line.add(label(str(yr), font_size=15, color=GREY_D).next_to([X(yr), 0, 0], DOWN, buff=0.12))
        ev = [(1738, r"Bernoulli: log utility"), (1944, r"von Neumann--Morgenstern"), (1956, r"Kelly"),
              (1957, r"Bellman"), (1969, r"Merton"), (1979, r"Samuelson; Kahneman--Tversky"),
              (1983, r"Crandall--Lions"), (1990, r"Davis--Norman; Pardoux--Peng"), (2006, r"mean-field games"),
              (2017, r"PPO")]
        dots, labs = VGroup(), VGroup()
        for i, (yr, name) in enumerate(ev):
            d = Dot([X(yr), 0, 0], radius=0.07, color=QC.IDEA)
            t = label(rf"{yr}\; {name}", font_size=16, color=QC.IDEA)
            up = i % 2 == 0
            t.next_to(d, UP if up else DOWN, buff=0.35 + (0.45 if i % 4 in (2, 3) else 0.0))
            keep_in_frame(t, margin=0.2)
            dots.add(d)
            labs.add(t)
        strip = VGroup(line, dots, labs).shift(UP * 1.6)
        root = label(r"maximize expected utility", font_size=28, color=VALUE).move_to(DOWN * 1.0)
        kids = [(r"how much: Kelly, Merton, Samuelson", KELLY), (r"over time: Bellman, HJB, viscosity, BSDE", VALUE),
                (r"against a crowd: mean-field games", ALT), (r"how people decide: prospect theory", OVER),
                (r"learn it: reinforcement learning", GOOD)]
        leaves = VGroup(*[label(t, font_size=22, color=c_) for t, c_ in kids])
        VGroup(VGroup(*leaves[:3]).arrange(RIGHT, buff=0.5), VGroup(*leaves[3:]).arrange(RIGHT, buff=0.5)).arrange(
            DOWN, buff=0.35).move_to(DOWN * 2.6)
        edges = VGroup(*[Line(root.get_bottom(), lf.get_top(), color=GREY_C, stroke_width=1.5) for lf in leaves])
        with self.voiceover(
            "How we got here. Daniel Bernoulli proposed log utility in 1738; von Neumann and Morgenstern built expected "
            "utility on axioms in 1944; John Kelly found the growth rule in 1956, and Richard Bellman the recursion behind "
            "every multi-stage decision in 1957. <bookmark mark='a'/> Robert Merton solved the investor's problem in 1969; "
            "in 1979 Paul Samuelson attacked Kelly, and Kahneman and Tversky showed how people really choose. Crandall and "
            "Lions made the Bellman equation rigorous in 1983, and 1990 brought Davis and Norman's trading costs and "
            "Pardoux and Peng's backward equations. <bookmark mark='b'/> Then games with a continuum of players, in 2006, "
            "and in 2017 the learning algorithm we will test. <bookmark mark='c'/> One tree, rooted in expected utility: how "
            "much to bet, how to decide over time, against a crowd, how people really decide, and how a machine learns it."
        ) as vo:
            self.play(Create(line), run_time=1)
            for k in range(4):
                self.play(FadeIn(dots[k], scale=1.5), FadeIn(labs[k], shift=UP * 0.1), run_time=0.6)
            vo.wait_until("a")
            for k in range(4, 8):
                self.play(FadeIn(dots[k], scale=1.5), FadeIn(labs[k], shift=UP * 0.1), run_time=0.6)
            vo.wait_until("b")
            for k in range(8, 10):
                self.play(FadeIn(dots[k], scale=1.5), FadeIn(labs[k], shift=UP * 0.1), run_time=0.6)
            vo.wait_until("c")
            self.play(FadeIn(root, shift=UP * 0.2))
            self.play(LaggedStart(*[AnimationGroup(Create(e), FadeIn(lf)) for e, lf in zip(edges, leaves)],
                                  lag_ratio=0.3, run_time=3))
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Expected utility, risk aversion, and the Arrow--Pratt premium derived",
            r"Bellman's recursion, the HJB equation, the verification theorem, viscosity solutions",
            r"Merton's problem with consumption, the martingale method, and the no-trade band of trading costs",
            r"Kelly and Breiman proved; fractional Kelly, LTCM, Samuelson's objection, ergodicity",
            r"Optimal stopping: the Snell envelope and smooth fit; prospect theory and robust control",
            r"BSDEs, mean-field games, and a reinforcement learner checked against the answers",
            r"How funds size bets in practice, and the 2023--2026 frontier",
        ], color=QC.IDEA, font_size=24)
        with self.voiceover(
            "The plan. Utility and the price of risk. Bellman's recursion, the HJB equation and the theory behind it. "
            "Merton's problem with consumption and trading costs. Kelly, proved and criticized. When to stop, and how "
            "people really decide. Backward equations, crowds and a learning machine. And how funds size bets in practice."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.5, run_time=10))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("data",))
        with self.voiceover(
            "In the House, this part builds the sizing module: utility, the Merton and Kelly fractions, and the "
            "solvers behind them. <bookmark mark='a'/> Every position the House takes, from Part ten's options to "
            "Part thirty's portfolios, will be sized by it."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["data"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(Indicate(chart.desk["portfolio"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
