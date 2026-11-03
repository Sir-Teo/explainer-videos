from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant3.common import GAIN, LOSS, PART, load, real_data

SIG_COLORS = {"AC": QC.LOSS, "OP": QC.GAIN, "INV": QC.SPOT, "BE-ME": QC.IDEA, "E-P": QC.OPTION}
SHORT = {"AC": r"accruals", "OP": r"profitability", "INV": r"investment", "BE-ME": r"book-to-market",
         "E-P": r"earnings yield"}


class Signals(VoiceoverScene):
    def construct(self):
        f = load("factors")
        e = load("envelope")
        self.card()
        o = load("osap")
        self.fscore(o)
        self.curves(f)
        self.decay(f)
        self.zoo(o)
        self.counter(e)

    def card(self):
        c = chapter_card(14, r"Accounting signals that became factors", r"Do the statements predict returns, and "
                         r"for how long?", lit=(1996,), part=PART)
        with self.voiceover("Chapter fourteen. Accounting signals that became factors, and decayed."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def curves(self, f):
        g = axes([1963, 2021], [np.log10(0.4), np.log10(16)], x_length=6.9, y_length=4.8,
                 ylabel=r"growth of \$1 in the long-short portfolio (log scale)", xticks=[1970, 1990, 2010],
                 xfmt=lambda x: f"{int(x)}", yticks=list(np.log10([0.5, 1, 2, 4, 8, 16])),
                 yfmt=lambda u: f"{10 ** u:g}", font_size=18).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        lines, pubs, legs = VGroup(), VGroup(), []
        for k in f["order"]:
            s = f["signals"][k]
            t, c = np.asarray(s["t"]), np.log10(np.asarray(s["cum"]))
            col = SIG_COLORS[k]
            lines.add(curve(ax, t, c, col, stroke_width=2.6))
            i = int(np.searchsorted(t, s["year"] + 1))
            if i < len(t):
                pubs.add(Dot(ax.c2p(t[i], c[i]), radius=0.08, color=col).set_stroke(WHITE, width=1.5))
            legs.append((col, rf"{SHORT[k]}: {s['who']}"))
        leg = legend(legs, font_size=18)
        hint = VGroup(Dot(radius=0.07, color=GREY_B).set_stroke(WHITE, width=1.5),
                      label(r"the year after publication", font_size=19, color=GREY_B)).arrange(RIGHT, buff=0.12)
        how = wrapped_label(r"each line buys the top decile and sells the bottom, value-weighted, rebalanced yearly; "
                            r"before costs", 4.6, 19, GREY_B)
        VGroup(leg, hint, how).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)
        src = real_data(r"Kenneth French's sorts, July 1963 -- December 2020")
        with self.voiceover(
            "Accounting signals became the first factors. Five of them on Kenneth French's portfolios since 1963, each long the "
            "tenth of stocks with the best value of the signal and short the worst: low accruals, high profitability, low "
            "investment, cheap on book, cheap on earnings. <bookmark mark='a'/> Over the whole sample most made money: a dollar "
            "in the investment spread became about eight. <bookmark mark='b'/> The dots mark the year after each was published. "
            "Watch what the lines do after their dot."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(how))
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3, run_time=5), FadeIn(leg))
            vo.wait_until("a")
            self.play(Indicate(lines[2], scale_factor=1.0), Indicate(lines[0], scale_factor=1.0))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p, scale=1.5) for p in pubs], lag_ratio=0.3), FadeIn(hint))
        self.wait(0.6)
        self.clear_scene()

    def decay(self, f):
        order = f["order"]
        g = axes([0, len(order)], [-0.02, 0.08], x_length=7.6, y_length=4.4, ylabel=r"average return a year",
                 xticks=[], yticks=[-0.02, 0, 0.02, 0.04, 0.06, 0.08], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=18)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        w = (ax.c2p(0.3, 0)[0] - ax.c2p(0, 0)[0])
        pre_b, post_b, names = VGroup(), VGroup(), VGroup()
        for i, k in enumerate(order):
            s = f["signals"][k]
            for j, (key, col, grp) in enumerate([("pre", SIG_COLORS[k], pre_b), ("post", GREY_B, post_b)]):
                v = s[key]["mean"]
                x = i + 0.33 + 0.34 * j
                top, bot = ax.c2p(x, max(v, 0)), ax.c2p(x, min(v, 0))
                r = Rectangle(width=w, height=max(top[1] - bot[1], 0.01), stroke_width=0, fill_color=col,
                              fill_opacity=0.9 if j == 0 else 0.6).move_to((top + bot) / 2)
                t_ = MathTex(rf"{100 * v:.1f}", font_size=18, color=col).next_to(r, UP if v >= 0 else DOWN, buff=0.06)
                grp.add(VGroup(r, t_))
            names.add(label(SHORT[k], font_size=17, color=SIG_COLORS[k]).move_to(ax.c2p(i + 0.5, -0.02) + DOWN * 0.3))
        leg = VGroup(
            label(r"bright: before publication", font_size=21, color=WHITE),
            label(r"grey: after publication", font_size=21, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        avg_pre = np.mean([f["signals"][k]["pre"]["mean"] for k in order])
        avg_post = np.mean([f["signals"][k]["post"]["mean"] for k in order])
        side = VGroup(
            leg,
            MathTex(rf"\text{{average: }}{100 * avg_pre:.1f}\% \to {100 * avg_post:.1f}\%", font_size=32),
            wrapped_label(r"five signals are a small sample: next, every published predictor", 4.6, 22, QC.IDEA),
            wrapped_label(r"profitability, published in 2013, has too few years after to judge", 4.6, 19, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Split each history at publication: bright before, grey after. <bookmark mark='a'/> Accruals fell from five percent a "
            "year to two; investment, from six to slightly negative; book-to-market, from seven to one; earnings yield from seven "
            "and a half to under three. <bookmark mark='b'/> Five signals could be five unlucky draws. To know whether a backtest "
            "of a published signal overstates its future, you need every published signal."
        ) as vo:
            self.play(FadeIn(g), FadeIn(names), FadeIn(leg))
            self.play(LaggedStart(*[GrowFromEdge(b[0], DOWN) for b in pre_b], lag_ratio=0.2),
                      LaggedStart(*[FadeIn(b[1]) for b in pre_b], lag_ratio=0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in post_b], lag_ratio=0.4, run_time=4))
            self.play(FadeIn(side[1]), FadeIn(side[3]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def fscore(self, o):
        tests = [r"ROA $> 0$", r"CFO $> 0$", r"$\Delta$ROA $> 0$", r"CFO $>$ ROA", r"$\Delta$leverage $< 0$",
                 r"$\Delta$current ratio $> 0$", r"no new shares", r"$\Delta$gross margin $> 0$",
                 r"$\Delta$asset turnover $> 0$"]
        groups = [(r"profitability", QC.GAIN, 4), (r"leverage and liquidity", QC.SPOT, 3), (r"efficiency", QC.IDEA, 2)]
        cells = VGroup()
        k = 0
        for name, col, n in groups:
            col_g = VGroup(label(name, font_size=20, color=col))
            for _ in range(n):
                col_g.add(VGroup(Square(0.32, stroke_color=col, stroke_width=2),
                                 label(tests[k], font_size=20, color=GREY_A)).arrange(RIGHT, buff=0.2))
                k += 1
            col_g.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
            cells.add(col_g)
        cells.arrange(RIGHT, buff=0.6, aligned_edge=UP).to_edge(UP, buff=0.6)
        ex = o["examples"]
        ps, gp = ex["PS"], ex["GP"]
        rows = VGroup(
            wrapped_label(r"Piotroski (2000): one point per test passed, 0 to 9. Among high book-to-market stocks, "
                          r"buying high scores and selling low ones earned about 23\% a year, 1976--1996.", 12.0, 22,
                          GREY_A),
            wrapped_label(r"Novy-Marx (2013): gross profits over assets, (revenue $-$ cost of goods sold)/assets: the "
                          r"cleanest measure of profitability, high up the income statement, before accrual choices.",
                          12.0, 22, GREY_A),
            MathTex(rf"\text{{F-score long-short: }}{ps['in']:.2f}\%\ \text{{a month in sample}} \to {ps['post']:.2f}\%"
                    rf"\ \text{{after }}{ps['year']};\quad \text{{GP: }}{gp['in']:.2f}\% \to {gp['post']:.2f}\%"
                    rf"\ \text{{after }}{gp['year']}", font_size=26, color=QC.HOUSE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(cells, DOWN, buff=0.5)
        with self.voiceover(
            "Sloan's accruals were one statement-based signal. Joseph Piotroski combined nine. Each test scores a point: is the firm "
            "profitable, does it generate operating cash, is profitability rising, is cash flow above earnings, which is Sloan "
            "again; is leverage falling, liquidity rising, has it avoided issuing shares; are margins and turnover improving. "
            "<bookmark mark='a'/> Among cheap stocks, he reported that buying high scores and shorting low ones earned about "
            "twenty-three percent a year from 1976 to 1996. <bookmark mark='b'/> Robert Novy-Marx argued in 2013 that the cleanest "
            "profit measure sits high on the income statement, gross profit over assets, before most accounting choices bite. "
            "<bookmark mark='c'/> Both have open-source replications. Unusually, both did as well or better after publication than "
            "before; keep them in mind as exceptions."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.4, run_time=4))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.wait(0.4)
        self.clear_scene()

    def zoo(self, o):
        recs = o["recs"]
        yrs = np.array([r_["year"] for r_ in recs])
        ins = np.array([r_["in"] for r_ in recs])
        post = np.array([r_["post"] for r_ in recs])
        acc = np.array([r_["cat"] == "Accounting" for r_ in recs])
        g = axes([1968, 2018], [-1.0, 3.0], x_length=8.0, y_length=4.6, xlabel=r"year the predictor was published",
                 ylabel=r"long-short return, \% a month", xticks=[1970, 1980, 1990, 2000, 2010],
                 xfmt=lambda v: f"{int(v)}", yticks=[-1, 0, 1, 2, 3], font_size=17).to_edge(LEFT, buff=0.5)
        g.shift(DOWN * 0.2)
        ax = g.ax
        zero = DashedLine(ax.c2p(1968, 0), ax.c2p(2018, 0), color=GREY_D, stroke_width=1.5)
        rng = np.random.default_rng(0)
        jit = rng.uniform(-0.35, 0.35, len(recs))
        f = ValueTracker(0.0)

        def dots():
            a = f.get_value()
            out = VGroup()
            for x, j, i_, p_, c in zip(yrs, jit, ins, post, acc):
                y = float(np.clip((1 - a) * i_ + a * p_, -1.0, 3.0))
                col = interpolate_color(ManimColor(QC.IDEA if c else QC.SPOT), ManimColor(GREY_B), a * 0.6)
                out.add(Dot(ax.c2p(np.clip(x + j, 1968, 2018), y), radius=0.04, color=col, fill_opacity=0.8))
            return out

        dd = always_redraw(dots)
        A, Ac = o["all"], o["acc"]
        bars = VGroup()
        for i, (v, col, txt) in enumerate(((A["in"], QC.IDEA, r"in sample"), (A["oos"], GREY_A, r"before publication"),
                                           (A["post"], GREY_B, r"after publication"))):
            h = v * 1.6
            r_ = Rectangle(width=0.9, height=h, stroke_width=0, fill_color=col, fill_opacity=0.9)
            r_.move_to([3.4 + 1.25 * i, -2.2, 0], aligned_edge=DOWN)
            bars.add(VGroup(r_, MathTex(rf"{v:.2f}", font_size=26, color=col).next_to(r_, UP, buff=0.08),
                            wrapped_label(txt, 1.2, 15, GREY_B).next_to(r_, DOWN, buff=0.1)))
        side = VGroup(
            label(rf"all {A['n']} predictors: after/in $= {A['post_ratio']:.2f}$", font_size=21),
            label(rf"bootstrap over predictors, 95\%: {o['boot_lo']:.2f} to {o['boot_hi']:.2f}", font_size=18,
                  color=GREY_B),
            label(rf"{Ac['n']} accounting ones: {Ac['in']:.2f} $\to$ {Ac['oos']:.2f} $\to$ {Ac['post']:.2f}",
                  font_size=21, color=QC.IDEA),
            wrapped_label(r"McLean and Pontiff (2016), 97 predictors: 26\% lower out of sample, 58\% lower after "
                          r"publication", 4.4, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR, buff=0.35)
        leg = legend([(QC.IDEA, r"accounting"), (QC.SPOT, r"price, analyst, other")], font_size=18)
        leg.next_to(g, UP, buff=0.05).align_to(g, RIGHT)
        src = real_data(r"Chen and Zimmermann (2022), open-source asset pricing, release 2024.10, original-paper "
                        r"portfolios, through 2020")
        ex = o["examples"]
        with self.voiceover(
            "Andrew Chen and Tom Zimmermann rebuilt the long-short portfolio of every predictor in the published literature and "
            f"released the code and data; {A['n']} of them have two years both in their paper's sample and after publication. "
            "Each dot is one, at its publication year, at the height of its in-sample return. <bookmark mark='a'/> Now let every "
            "dot fall to what it earned after publication. <bookmark mark='b'/> Collapse them into three averages: "
            f"{A['in']:.2f} percent a month in sample, {A['oos']:.2f} just outside it but before publication, {A['post']:.2f} after. "
            "The first drop is what luck predicts; the second is what traders reading the papers predict. McLean and Pontiff "
            f"found the same on their ninety-seven. <bookmark mark='c'/> Sloan's accruals went from {ex['Accruals']['in']:.2f} to "
            f"{ex['Accruals']['post']:.2f}."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(src), FadeIn(leg))
            self.add(dd)
            vo.wait_until("a")
            self.play(f.animate.set_value(1.0), run_time=5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in bars], lag_ratio=0.4), FadeIn(side[:2]))
            self.play(FadeIn(side[2:]))
            vo.wait_until("c")
            self.play(Indicate(bars[2], color=QC.LOSS, scale_factor=1.05))
        dd.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def counter(self, e):
        big = MathTex(str(e["trials"]), font_size=150, color=QC.HOUSE)
        cap = label(r"the trial counter: configurations tried so far, across the whole series", font_size=26,
                    color=GREY_A).next_to(big, DOWN, buff=0.3)
        add = VGroup(
            label(r"this part: 5 accounting signals, 208 published predictors, 8 forecaster settings, 1 CAPE forecast", font_size=22,
                  color=GREY_B),
            label(r"their hold-outs, 2021 onward, are sealed", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.15).next_to(cap, DOWN, buff=0.5)
        VGroup(big, cap, add).move_to(ORIGIN)
        with self.voiceover(
            "And every signal we look at is a trial. The House counts them all, across the series, because the more configurations "
            "a researcher tries, the more one of them will look good by chance; the two hundred and eight published predictors count "
            "as two hundred and eight trials, one each. Part twenty-six shows how to deflate a result by that count, and the hold-out years, 2021 "
            "onward, are sealed until then."
            " Not every event-driven trade starts from the statements. Next, one whose payoff is written into a contract: merger arbitrage."
        ):
            self.play(FadeIn(big, scale=0.8), FadeIn(cap))
            self.play(FadeIn(add))
        self.wait(0.4)
        self.clear_scene()
