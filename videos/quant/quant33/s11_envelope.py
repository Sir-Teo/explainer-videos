from __future__ import annotations

import math

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant33.common import BAD, COST_C, GOOD, HURDLE, OOS_C, PART, RES_C, comma, fit_right, load


class Envelope(VoiceoverScene):
    def construct(self):
        e = load("envelope")
        self.card()
        self.register(e)
        self.opened(e)
        self.table(e)
        self.years(e)
        self.sensitivity(e)
        self.deflate(e)
        self.reading(e)
        self.next_steps()
        self.question()

    def card(self):
        c = chapter_card(10, r"The residual book, registered and opened", r"Does the residual premium survive five "
                         r"sealed years, after costs?", part=PART)
        with self.voiceover("Chapter ten. One residual book, registered before the envelope is opened, and judged once on "
                            "2021 to 2025, after costs."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def register(self, e):
        card = firm_card(r"One rule, registered", r"Kenneth French's 49 industries, daily; five correlation eigenportfolios "
                         r"from the trailing year, refitted every 21 days; 60-day residual regressions and OU fits; each "
                         r"industry enters at the research chapter's optimal band for the cost of its own hedge, and exits "
                         r"at its mean; 5 bp a side on the industry and on its hedge, charged inside the P\&L",
                         numbers=((rf"{e['n_trials']}", r"trials: the eight Avellaneda--Lee variants of Chapter 5 and "
                                                         r"this one"),),
                         kind=r"Registered", width=10.6, font_size=22).move_to(UP * 0.4)
        n_now = int(e["trials"])
        n_before = n_now - int(e["n_trials"])
        ctr = MathTex(rf"\text{{the counter}}:\ {comma(n_before)}\ \to\ {comma(n_now)}", font_size=30,
                      color=QC.HOUSE).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The registration. <bookmark mark='a'/> Five eigenportfolios, sixty-day residuals, and the research "
            "chapter's band for each industry's own costs, exiting at the mean. Costs are charged on both legs, inside "
            f"the profit and loss. <bookmark mark='b'/> It is charged with {e['n_trials']} trials: the eight variants "
            f"that failed, and itself. The counter moves to {n_now:,}."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(FadeIn(ctr))
        self.wait(0.4)
        self.clear_scene()

    def opened(self, e):
        d = np.asarray(e["hold_dates"], float)
        x = d // 10000 + ((d // 100) % 100 - 0.5) / 12 + ((d % 100) - 15) / 365
        y = 100 * np.asarray(e["cum_hold"], float)
        lo = float(np.floor(min(y.min(), 0) / 2) * 2)
        hi = float(np.ceil(y.max() / 2) * 2)
        g = axes([2021, 2026], [lo, hi], x_length=7.4, y_length=4.4, xlabel=r"2021--2025, sealed until now",
                 ylabel=r"cumulative return after costs, \% of gross", xticks=[2021, 2023, 2025], yticks=[lo, 0, hi],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=15).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        line = curve(ax, x, y, OOS_C, stroke_width=3)
        zero = DashedLine(ax.c2p(2021, 0), ax.c2p(2026, 0), color=GREY_C, stroke_width=1)
        h = e["hold"]
        st = VGroup(label(rf"{100 * h['mean']:+.1f}\% a year", font_size=17, color=OOS_C),
                    label(rf"volatility {100 * h['vol']:.1f}\%", font_size=17, color=GREY_A),
                    label(rf"worst fall {100 * h['maxdd']:.1f}\%", font_size=17, color=GREY_A))
        st.arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(RIGHT, buff=0.4).shift(UP * 1.4)
        fit_right(st)
        with self.voiceover(
            "The envelope. <bookmark mark='a'/> Five sealed years of the residual book, after costs. "
            f"<bookmark mark='b'/> It earned {100 * h['mean']:.1f} percent a year on its gross, at a volatility of "
            f"{100 * h['vol']:.1f} percent, and never fell more than {abs(100 * h['maxdd']):.1f} percent. A small, "
            "steady, market-neutral return: the size of thing stat arb on industries can be."
        ) as vo:
            self.play(FadeIn(g), Create(zero))
            vo.wait_until("a")
            self.play(Create(line), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(st))
        self.wait(0.4)
        self.clear_scene()

    def table(self, e):
        hx = [-3.8, -0.8, 2.0, 4.8]
        head = VGroup(label(r"", font_size=17), label(r"Sharpe, gross", font_size=17, color=RES_C),
                      label(r"Sharpe, net", font_size=17, color=COST_C), label(r"daily turnover", font_size=17,
                                                                              color=GREY_B))
        r, h = e["row"]["research"], e["row"]["holdout"]
        rt = 100 * load("pca")["configs"]["5f/60d/theory"]["turnover"]
        tab = VGroup(head,
                     VGroup(label(r"1994--2020, research", font_size=20), MathTex(f"{e['res_gross']['sharpe']:.2f}",
                                                                                   font_size=26),
                            MathTex(f"{e['res']['sharpe']:.2f}", font_size=26), MathTex(rf"{rt:.0f}\%", font_size=26)),
                     VGroup(label(r"2021--2025, sealed", font_size=20, color=OOS_C),
                            MathTex(f"{e['hold_gross']['sharpe']:.2f}", font_size=26),
                            MathTex(f"{e['hold']['sharpe']:.2f}", font_size=26),
                            MathTex(rf"{100 * e['turn_hold']:.0f}\%", font_size=26)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.6 - 0.9 * j, 0])
        se = h["sharpe_se"]
        foot = wrapped_label(rf"from daily returns; on the Track Record's monthly returns, the sealed Sharpe ratio is "
                             rf"${h['sharpe']:.2f} \pm {se:.2f}$ and the research one ${r['sharpe']:.2f} \pm "
                             rf"{r['sharpe_se']:.2f}$", 11.4, 16, GREY_A).to_edge(DOWN, buff=0.6)
        hg, hn = e["hold_gross"]["sharpe"], e["hold"]["sharpe"]
        with self.voiceover(
            "The numbers. <bookmark mark='a'/> Before costs, the residuals reverted on the sealed years exactly as on "
            f"the research years: a gross Sharpe ratio of {hg:.2f} against {e['res_gross']['sharpe']:.2f}. The premium "
            "did not decay. <bookmark mark='b'/> After costs, "
            f"{hn:.2f}, a little better than the research years. On monthly returns the standard error is "
            f"{se:.2f}: positive, and indistinguishable from zero. Five years cannot prove a Sharpe ratio of a third."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(tab[1][0], tab[1][1], tab[2][0], tab[2][1])))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab[1][2:], *tab[2][2:])))
        self.wait(0.4)
        self.clear_scene()

    def years(self, e):
        ys = e["years"]
        keys = list(ys)
        vals = [100 * ys[k]["mean"] for k in keys]
        bars = VGroup()
        for j, (k, v) in enumerate(zip(keys, vals)):
            col = GOOD if v > 0 else BAD
            rct = Rectangle(width=0.9, height=abs(v) * 0.55, fill_color=col, fill_opacity=0.85, stroke_width=0)
            rct.move_to([-4.0 + 2.0 * j, -0.4, 0], aligned_edge=DOWN if v > 0 else UP)
            bars.add(VGroup(rct, MathTex(rf"{v:+.1f}\%", font_size=24).next_to(rct, UP if v > 0 else DOWN, buff=0.12),
                            label(k, font_size=20, color=GREY_A).move_to([-4.0 + 2.0 * j, -3.2, 0])))
        axis = Line([-5.0, -0.4, 0], [5.0, -0.4, 0], color=GREY_C, stroke_width=1.5)
        head = label(r"The sealed years, one by one, after costs", font_size=28).to_edge(UP, buff=0.5)
        best = keys[int(np.argmax(vals))]
        worst = keys[int(np.argmin(vals))]
        vb, vw = max(vals), min(vals)
        npos = sum(v > 0 for v in vals)
        with self.voiceover(
            f"Year by year. <bookmark mark='a'/> {npos} of the five years were positive. The best was {best}, "
            f"{vb:+.1f} percent, and it did most of the work; the worst {worst}, {vw:+.1f}. <bookmark mark='b'/> None was "
            "a disaster. And 2022, the year stocks and bonds fell together, was a positive year for the residuals: the "
            "book has no market exposure to lose."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axis))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in bars], lag_ratio=0.25))
            vo.wait_until("b")
            self.wait(0.1)
        self.wait(0.4)
        self.clear_scene()

    def sensitivity(self, e):
        rt = load("pca")["configs"]["5f/60d/theory"]["turnover"]
        sets = [(r"1994--2020", e["res_gross"], rt, RES_C), (r"2021--2025", e["hold_gross"], e["turn_hold"], OOS_C)]
        cs = np.linspace(0, 10, 41)
        g = axes([0, 10], [-1.5, 1.5], x_length=7.4, y_length=4.4, xlabel=r"cost per side, bp", ylabel=r"Sharpe ratio "
                 r"after costs", xticks=[0, 5, 10], yticks=[-1, 0, 1], font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(10, 0), color=GREY_C, stroke_width=1)
        five = DashedLine(ax.c2p(5, -1.5), ax.c2p(5, 1.5), color=HURDLE, stroke_width=1.5)
        lines, be = VGroup(), []
        for nm, st, tv, col in sets:
            ys = (st["mean"] - 2 * cs * 1e-4 * tv * 252) / st["vol"]
            lines.add(curve(ax, cs, np.clip(ys, -1.5, 1.5), col, stroke_width=3))
            be.append(st["mean"] / (2 * 1e-4 * tv * 252))
        leg = legend([(c, n) for n, _, _, c in sets], font_size=16).to_edge(RIGHT, buff=0.4).shift(UP * 1.6)
        fit_right(leg)
        b0, b1 = be
        st_ = VGroup(label(rf"break-even: {b0:.1f} bp", font_size=16, color=RES_C),
                     label(rf"break-even: {b1:.1f} bp", font_size=16, color=OOS_C))
        st_.arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(leg, DOWN, buff=0.4).align_to(leg, LEFT)
        fit_right(st_)
        with self.voiceover(
            "How much the verdict depends on the cost. <bookmark mark='a'/> The same gross returns and turnover, charged "
            "at every cost from zero to ten basis points a side. <bookmark mark='b'/> The book breaks even at about "
            f"{b0:.1f} basis points on the research years and {b1:.1f} on the sealed years. The House assumed five. At "
            "four the book is comfortably positive; at eight it loses. The conclusion of this whole part sits within a "
            "few basis points of execution, which is why Part thirty-seven measures it."
        ) as vo:
            self.play(FadeIn(g), Create(zero), Create(five), FadeIn(leg))
            vo.wait_until("a")
            self.play(*[Create(l_) for l_ in lines], run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(st_))
        self.wait(0.4)
        self.clear_scene()

    def deflate(self, e):
        from scipy.stats import norm
        n = int(e["n_trials"])
        r = e["row"]["research"]
        g = 0.5772156649
        emax = (1 - g) * norm.ppf(1 - 1 / n) + g * norm.ppf(1 - 1 / (n * math.e))
        bar = emax * r["sharpe_se"]
        rel = "<" if r["sharpe"] < bar else ">"
        rows = [cmath(r"\mathbb E\big[\max_{i \le N} Z_i\big]", r"\approx", r"(1-\gamma)\Phi^{-1}(1 - \tfrac1N) + "
                      r"\gamma\,\Phi^{-1}(1 - \tfrac{1}{Ne})", font_size=30),
                cmath(rf"N = {n}", r":", rf"\text{{bar}} = {emax:.2f} \times {r['sharpe_se']:.2f} = {bar:.2f}",
                      font_size=32, colors={r"\text{bar}": HURDLE}),
                cmath(r"\text{research Sharpe}", r"=", rf"{r['sharpe']:.2f}\ \ {rel}\ \ {bar:.2f}", font_size=32, colors={r"\text{research Sharpe}": RES_C})]
        whys = [why(r"Part 26: the best of $N$ worthless rules has an expected Sharpe ratio of this many standard errors "
                    r"($\gamma$ is Euler's constant)"),
                why(r"with nine trials and the research years' standard error, the bar a lucky rule would clear"),
                why(r"so the research years alone could not justify the rule: that is why the House opens a sealed "
                    r"envelope rather than trusting the backtest")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        rs = r["sharpe"]
        with self.voiceover(
            "Why the envelope was needed. <bookmark mark='a'/> Part twenty-six: the best of N worthless rules has an "
            "expected Sharpe ratio of a predictable number of standard errors. <bookmark mark='b'/> With nine trials, "
            f"that bar is {bar:.2f}. <bookmark mark='c'/> The research years' net Sharpe ratio is {rs:.2f}, against that bar of "
            f"{bar:.2f}: on the backtest alone, the House could not tell this rule from the luckiest of nine. Only the sealed "
            "years can, and five of them are not enough to be sure."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def reading(self, e):
        rows = [cmath(r"\text{gross}", r":", r"\text{the reversion is real and stable}", font_size=34,
                      colors={r"\text{gross}": RES_C}),
                cmath(r"\text{net}", r":", r"\text{costs take most of it}", font_size=34,
                      colors={r"\text{net}": COST_C}),
                cmath(r"\text{the band}", r":", r"\text{the only lever that turned it positive}", font_size=34,
                      colors={r"\text{the band}": HURDLE})]
        whys = [why(r"the residual premium on industries did not decay between the two periods"),
                why(r"at 5 bp a side on two legs, most of the gross return pays for trading"),
                why(r"trading less, at bands derived from costs, mattered more than any choice of factors or windows")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        hg, hn = e["hold_gross"]["mean"], e["hold"]["mean"]
        share = 100 * (1 - hn / hg)
        with self.voiceover(
            "How to read it. <bookmark mark='a'/> Before costs the reversion is real and stable: it did not decay. "
            f"<bookmark mark='b'/> After costs, trading takes about {share:.0f} percent of it. <bookmark mark='c'/> And "
            "the one lever that turned the book positive was the band: trading less, at thresholds derived from costs. "
            "It mattered more than the number of factors or the window."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def next_steps(self):
        cards = VGroup(
            desk_question(r"more assets, cheaper legs", r"single stocks revert more; trading the hedge as one futures "
                          r"position instead of 48 industries would cut the second leg's cost", width=12.4, font_size=19),
            desk_question(r"net the hedges", r"positions' factor hedges partly cancel; charging the book's net hedge, "
                          r"not each position's, is the next registration", width=12.4, font_size=19),
            desk_question(r"execution", r"5 bp a side is a guess; Part 37 measures what a trade really costs", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What would improve it, each a new registration. <bookmark mark='a'/> More assets with cheaper legs: trade "
            "the hedge as one futures position. <bookmark mark='b'/> Net the hedges across positions, and charge only "
            "the book's net trade. <bookmark mark='c'/> And measure the cost instead of assuming it, which is Part "
            "thirty-seven."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a book's true Sharpe ratio is 0.3. How many years of monthly returns are needed for its "
                       r"estimate to be two standard errors from zero?")
        with self.voiceover(
            "Pause and predict. A book's true Sharpe ratio is point three. How many years of returns are needed before "
            "its estimate is two standard errors from zero?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
