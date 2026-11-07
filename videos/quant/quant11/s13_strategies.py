from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import quoting as Q
from videos.quant.quant11.common import (ALT, GAMMA, OPT, PART, SPOT, THETA, VEGA, axes3d, fixed, hint3d, load, pause,
                                         real_data, surf)

NAMES = ["straddle", "strangle", "risk reversal", "butterfly", "call spread", "calendar"]
BETS = {"straddle": (r"+", r"+", r"$\approx0$", r"a big move either way, or vol rising"),
        "strangle": (r"+", r"+", r"$\approx0$", r"a bigger move, for less premium"),
        "risk reversal": (r"$\approx0$", r"$\approx0$", r"+", r"up, and the skew flattening (vanna)"),
        "butterfly": (r"$-$", r"$-$", r"$\approx0$", r"staying put; vol falling"),
        "call spread": (r"$\pm$", r"$\pm$", r"+", r"up, but not too far"),
        "calendar": (r"$-$", r"+", r"$\approx0$", r"a calm near month, later vol holding")}
SIG, T = 0.5, 30 / 365


def legs_of(name):
    return Q.strategies(100.0, T, 0.1)[name]


class Strategies(VoiceoverScene, ThreeDScene):
    def construct(self):
        st = load("strategies")
        self.card()
        self.morph()
        self.bets()
        self.record(st)

    def card(self):
        c = chapter_card(5, r"Strategies: what each bets on, and what it paid", r"What is a butterfly a bet on?",
                         part=PART)
        with self.voiceover("Chapter five. Strategies: what each structure bets on, and what it paid."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def morph(self):
        ax = axes3d([-0.25, 0.25, 0.25], [-0.1, 0.1, 0.1], [-1, 1, 0.5], x_length=7.0, y_length=5.0, z_length=3.0)

        def scale(name):
            P = Q.pnl_surface(legs_of(name), 100.0, SIG, np.linspace(-0.25, 0.25, 11), np.linspace(-0.1, 0.1, 7), 7 / 365)
            return float(np.max(np.abs(P)))

        def mk(name, days):
            L, s = legs_of(name), scale(name)

            def f(x, y):
                return float(np.clip((Q.book_value(L, 100 * (1 + x), max(SIG + y, 1e-3), days / 365)
                                      - Q.book_value(L, 100.0, SIG, 0.0)) / s, -1, 1))
            return surf(ax, f, (-0.25, 0.25), (-0.1, 0.1), [(QC.LOSS, -1), (GREY_D, 0), (QC.GAIN, 1)],
                        resolution=(24, 16), opacity=0.85)
        hint = hint3d((r"spot move, $\pm 25\%$", SPOT), (r"implied-vol move, $\pm 10$ points", VEGA),
                      (r"model P\&L (each surface scaled separately)", OPT), ax=ax)
        name_lab = label(r"straddle", font_size=34, color=OPT).to_corner(UL, buff=0.4)
        fixed(self, hint, name_lab)
        self.set_camera_orientation(phi=64 * DEGREES, theta=-55 * DEGREES, zoom=0.9)
        s0 = mk("straddle", 7)
        with self.voiceover(
            "Every standard structure is a shape. Here is the profit after a week of one-month options, over the "
            "move in spot, left to right, and the move in implied volatility, front to back; green gains, red losses. "
            "The straddle is a valley that turns up at both ends and tilts up with volatility: long gamma, long vega. "
            "<bookmark mark='a'/> Let time pass, three weeks: the whole valley sinks. That is theta. "
            "<bookmark mark='b'/> Now morph. The strangle: the same bet, a wider valley, cheaper. "
            "<bookmark mark='c'/> The risk reversal, long the call above and short the put below: a tilted plane, a "
            "bet on direction with almost no vega. <bookmark mark='d'/> The butterfly: a hill, the straddle upside "
            "down, which wins if nothing happens. <bookmark mark='e'/> The call spread: up, but capped. "
            "<bookmark mark='f'/> And the calendar, long the second month and short the first: it loses on big moves "
            "and gains when volatility rises, short gamma and long vega at once."
        ) as vo:
            self.play(Create(ax), FadeIn(hint), FadeIn(name_lab), run_time=1.2)
            self.play(Create(s0), run_time=2)
            vo.wait_until("a")
            self.play(Transform(s0, mk("straddle", 21)), run_time=2)
            for mark, name in zip("bcdef", NAMES[1:]):
                vo.wait_until(mark)
                new_lab = label(name, font_size=34, color=OPT).to_corner(UL, buff=0.4)
                fixed(self, new_lab)
                self.play(Transform(s0, mk(name, 7)), FadeOut(name_lab), FadeIn(new_lab), run_time=1.8)
                name_lab = new_lab
            self.move_camera(theta=-30 * DEGREES, run_time=min(max(vo.remaining(1.0) - 0.3, 1.0), 8.0))
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, added_anims=[FadeOut(VGroup(ax, s0)), FadeOut(hint),
                                                                             FadeOut(name_lab)], run_time=0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bets(self):
        head = VGroup(label(r"structure", font_size=21, color=GREY_B), label(r"gamma", font_size=21, color=GAMMA),
                      label(r"vega", font_size=21, color=VEGA), label(r"delta", font_size=21, color=QC.DELTA),
                      label(r"the bet", font_size=21, color=GREY_B))
        cells = VGroup(*head)
        for n in NAMES:
            g_, v_, d_, b_ = BETS[n]
            cells.add(label(n, font_size=21, color=OPT), label(g_, font_size=24, color=GAMMA),
                      label(v_, font_size=24, color=VEGA), label(d_, font_size=24, color=QC.DELTA),
                      label(b_, font_size=20, color=GREY_A))
        cells.arrange_in_grid(rows=7, cols=5, buff=(0.45, 0.22), col_alignments="lcccl").to_edge(UP, buff=0.5)
        rows = [cmath(r"\Gamma_{\text{straddle}}", r"=", r"2\,\Gamma_{\text{ATM}},\qquad \mathcal{V}_{\text{cal}} = "
                      r"\mathcal{V}_{2T} - \mathcal{V}_{T} > 0,\quad \Gamma_{\text{cal}} = \Gamma_{2T} - \Gamma_{T} < 0",
                      font_size=30)]
        whys = [why(r"local ATM toy with common IV and short maturities; leg Greeks sum, and signs can change away from this point")]
        rows[0].next_to(cells, DOWN, buff=0.5)
        whys[0].next_to(rows[0], DOWN, buff=0.2)
        pc = pause(r"On real bitcoin smiles, 2024--2025: which structure lost money in the most weeks?", width=5.0,
                   font_size=21)
        with self.voiceover(
            "A local guide near the initial at-the-money toy point, with common IV; zeros mean approximately small exposures. For each structure: the sign of its gamma, its vega, its "
            "delta, and what it is a bet on. <bookmark mark='a'/> The Greeks of a structure are the sums of its legs. "
            "A straddle has twice an at-the-money option's gamma. A calendar is long vega and short gamma at once, "
            "because vega grows like the square root of time and gamma shrinks like one over it. "
            "<bookmark mark='b'/> Pause and predict: bought every week on real Bitcoin smiles, which of these lost "
            "money most often?"
        ) as vo:
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.02, run_time=3))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(FadeIn(pc))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def record(self, st):
        rows = {r_["name"]: r_ for r_ in st["rows"]}
        data = {n: np.clip(np.asarray(st[f"pnl {n}"]), -20, 46) for n in NAMES}
        nW = len(data[NAMES[0]])
        g = axes([0, 6], [-20, 46], x_length=8.4, y_length=4.6, ylabel=r"P\&L of one four-week trade, per 100 of bitcoin",
                 yticks=[-20, 0, 20, 40], font_size=16).to_edge(LEFT, buff=0.6).shift(DOWN * 0.4)
        ax = g.ax
        z = DashedLine(ax.c2p(0, 0), ax.c2p(6, 0), color=GREY_C, stroke_width=1.5)
        names = VGroup(*[label(n, font_size=16, color=OPT).next_to(ax.c2p(i + 0.5, -20), DOWN, buff=0.12)
                         for i, n in enumerate(NAMES)])
        jit = np.random.default_rng(5).uniform(-0.25, 0.25, nW)
        tr = ValueTracker(0)

        def strips():
            k = int(tr.get_value())
            gr = VGroup()
            for i, n in enumerate(NAMES):
                for j in range(k):
                    v = data[n][j]
                    gr.add(Dot(ax.c2p(i + 0.5 + jit[j], v), radius=0.028, color=QC.GAIN if v > 0 else QC.LOSS,
                               fill_opacity=0.75))
            return gr
        dots = always_redraw(strips)
        meds = VGroup(*[Line(ax.c2p(i + 0.2, rows[n]["median"]), ax.c2p(i + 0.8, rows[n]["median"]), color=WHITE,
                             stroke_width=3) for i, n in enumerate(NAMES)])
        means = VGroup(*[Dot(ax.c2p(i + 0.5, rows[n]["mean"]), radius=0.07, color=YELLOW) for i, n in enumerate(NAMES)])
        tab = VGroup()
        for n in NAMES:
            r_ = rows[n]
            tab.add(label(rf"{n}: wins {100 * r_['win']:.0f}\%, mean {r_['mean']:+.1f}, $t = {r_['t']:+.1f}$",
                          font_size=18, color=OPT))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(RIGHT, buff=0.35).shift(UP * 0.6)
        leg = legend([(WHITE, r"median"), (YELLOW, r"mean")], font_size=17).next_to(tab, DOWN, buff=0.3).align_to(tab, LEFT)
        worst = rows[st["worst"]]
        best_t = max(abs(r_["t"]) for r_ in st["rows"])
        src = real_data(rf"{nW} trades each, every Wednesday 2024--2025: priced on that day's Deribit smile (Part 12), "
                        r"settled on Binance 28 days later")
        n_neg = sum(r_["median"] < 0 for r_ in st["rows"])
        med_say = ("below zero for every structure: the theta story." if n_neg == len(NAMES) else
                   f"below zero for {n_neg} of the six: the theta story.")
        rr_say = ("The risk reversal made money on average because Bitcoin rose over these two years, not because of "
                  "anything about volatility." if rows["risk reversal"]["mean"] > 0 else
                  "The risk reversal lost on average, as the smile's tilt cost more than the drift paid.")
        tsay = (f"No structure's mean has a t-statistic above {best_t:.1f}." if best_t < 2 else
                f"The largest t-statistic is {best_t:.1f}.")
        with self.voiceover(
            "Here is the record. Every Wednesday of 2024 and 2025, buy each structure on that day's real Deribit "
            "smile, and settle it twenty-eight days later at Bitcoin's price. "
            f"<bookmark mark='a'/> {nW} trades of each, filling week by week. <bookmark mark='b'/> The answer to the "
            f"question: the {st['worst']}, which lost in {100 * (1 - worst['win']):.0f} percent of weeks. Look at the "
            f"white medians: {med_say} The yellow means sit higher, pulled up by the rare large wins, the tails. "
            f"<bookmark mark='c'/> {rr_say} <bookmark mark='d'/> {tsay} Two years of one asset in a rising market can show what the shapes do; it cannot show that any of "
            "them has an edge."
            " Behind those shapes is one persistent number. Next: the volatility premium."
        ) as vo:
            self.play(FadeIn(g), Create(z), FadeIn(names), FadeIn(src))
            vo.wait_until("a")
            self.add(dots)
            self.play(tr.animate.set_value(nW), run_time=vo.until("b"), rate_func=linear)
            self.play(FadeIn(meds), FadeIn(means), FadeIn(leg), LaggedStart(*[FadeIn(t_) for t_ in tab],
                                                                              lag_ratio=0.2, run_time=2))
            vo.wait_until("c")
            self.play(Indicate(tab[2]))
        dots.clear_updaters()
        self.wait(0.4)
        self.clear_scene()
