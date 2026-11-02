from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant4.common import DRIFT, LOSS, MART, P_C, PART, load

GAME_C = {"fair coin": MART, "European roulette": P_C, "American roulette": LOSS}


class Ruin(VoiceoverScene):
    def construct(self):
        r = load("ruin")
        rd = load("ruin_duration")
        self.card()
        self.derive()
        self.duration(rd)
        self.curves(r)
        self.bold(r)

    def card(self):
        c = chapter_card(9, r"Gambler's ruin and bold play", r"How should you bet in a game you will lose?",
                         lit=(1965,), part=PART)
        with self.voiceover("Chapter nine. Gambler's ruin, and bold play."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def derive(self):
        rows = [cmath(r"\mathbb{E}[X_\tau]", r"=", r"X_0", font_size=42, colors={r"X_0": MART}),
                cmath(r"b \cdot P(\text{hit } b)", r"+", r"0 \cdot P(\text{hit } 0)", r"=", r"a", font_size=40),
                cmath(r"P(\text{hit } b \text{ before } 0)", r"=", r"\frac{a}{b}", font_size=42,
                      colors={r"\frac{a}{b}": MART}),
                cmath(r"\Big(\tfrac{q}{p}\Big)^{X_n}\ \text{is a martingale}", r"\;\Rightarrow\;",
                      r"P(\text{hit } b) = \frac{1 - (q/p)^a}{1 - (q/p)^b}", font_size=36,
                      colors={r"P(\text{hit } b) = \frac{1 - (q/p)^a}{1 - (q/p)^b}": P_C})]
        whys = [why(r"a fair walk from $a$, stopped at $0$ or $b$: the steps are bounded, so optional stopping holds"),
                why(r"the walk ends at one barrier or the other"),
                why(r"the gambler's ruin, solved in one line"),
                why(r"a biased game, win probability $p$, $q = 1 - p$ (de Moivre's trick)")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-2.4, buff=0.75, edge=6.9)
        with self.voiceover(
            "Optional stopping solves the oldest problem in probability in one line. A gambler starts with a units "
            "in a fair game and stops on reaching b or going broke. The steps are bounded, so the expected wealth at "
            "the end equals the start. <bookmark mark='a'/> At the end the wealth is either b or zero. "
            "<bookmark mark='b'/> So the chance of reaching b first is a over b. <bookmark mark='c'/> If the game is "
            "biased, with win probability p, the trick, due to de Moivre, is to find a different martingale: q over "
            "p raised to the power of the wealth. The same argument gives the general formula."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def curves(self, r):
        a = np.asarray(r["a"])
        g = axes([0, 100], [0, 1], x_length=7.0, y_length=4.4, xlabel=r"starting bankroll (target 100, one-unit bets)",
                 ylabel=r"chance of reaching 100 before 0", xticks=[0, 25, 50, 75, 100], yticks=[0, 0.5, 1],
                 font_size=18).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        lines = VGroup(*[curve(ax, a, np.asarray(r["curves"][k]), c, stroke_width=3.5) for k, c in GAME_C.items()])
        leg = legend([(GAME_C["fair coin"], r"fair coin, $p = 1/2$"), (GAME_C["European roulette"], r"European "
                      r"roulette, $p = 18/37$"), (GAME_C["American roulette"], r"American roulette, $p = 18/38$")],
                     font_size=21).to_edge(RIGHT, buff=0.5).shift(UP * 1.6)
        mid = VGroup(*[MathTex(rf"{100 * r['curves'][k][50]:.1f}\%" if r['curves'][k][50] > 0.001 else
                               rf"{100 * r['curves'][k][50]:.3f}\%", font_size=28, color=c)
                       for k, c in GAME_C.items()])
        cap = label(r"starting with 50, aiming for 100:", font_size=22, color=GREY_A)
        side = VGroup(cap, *mid).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(leg, DOWN, buff=0.6).align_to(leg, LEFT)
        with self.voiceover(
            "Here is what that formula means at a casino. Start with fifty units, bet one at a time, and try to "
            "reach a hundred. In a fair game your chance is a half: a straight line. <bookmark mark='a'/> On a "
            "European roulette wheel, betting on red, you win eighteen times in thirty-seven, an edge against you of "
            "only one thirty-seventh. Yet the chance of doubling fifty units falls to six percent. On an American "
            "wheel, with its extra zero, to half a percent. A small edge, repeated, is a certainty."
        ) as vo:
            self.play(FadeIn(g), Create(lines[0]), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(Create(lines[1]), Create(lines[2]), FadeIn(leg[1:]), run_time=2)
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def bold(self, r):
        units = r["units"]
        timid = np.asarray(r["timid"]["European roulette"])
        bold = r["bold"]["European roulette"]
        y = np.log10(np.maximum(timid, 1e-13))
        g = axes([0, len(units)], [-13, 0], x_length=7.4, y_length=4.4, xlabel=r"bankroll, in one-unit bets",
                 ylabel=r"chance of doubling it on European roulette (log scale)", xticks=[], yticks=[0, -3, -6, -9, -12],
                 yfmt=lambda u: rf"10^{{{int(u)}}}" if u else "1", font_size=18).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        w = ax.c2p(0.55, 0)[0] - ax.c2p(0, 0)[0]
        bars = VGroup()
        for i, v in enumerate(y):
            top, bot = ax.c2p(i + 0.5, v), ax.c2p(i + 0.5, -13)
            bars.add(Rectangle(width=w, height=top[1] - bot[1], stroke_width=0, fill_color=P_C, fill_opacity=0.85).move_to(
                (top + bot) / 2))
        xl = VGroup(*[MathTex(str(u), font_size=20, color=GREY_B).next_to(ax.c2p(i + 0.5, -13), DOWN, buff=0.1)
                      for i, u in enumerate(units)])
        bline = DashedLine(ax.c2p(0, np.log10(bold)), ax.c2p(len(units), np.log10(bold)), color=DRIFT, stroke_width=3)
        side = VGroup(
            label(r"timid play: one unit at a time", font_size=22, color=P_C),
            MathTex(rf"100 \text{{ units: }} {100 * timid[units.index(100)]:.2f}\%", font_size=30, color=P_C),
            label(r"bold play: everything on one spin", font_size=22, color=DRIFT),
            MathTex(rf"18/37 = {100 * bold:.1f}\%", font_size=30, color=DRIFT),
            wrapped_label(r"Dubins and Savage (1965), \textit{How to Gamble If You Must}: in a game against you, bold "
                          r"play is optimal", 4.6, 21, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "So if you must double your money tonight at a roulette table, how should you bet? Bet one unit at a "
            "time from a bankroll of a hundred, and your chance of doubling it is under half a percent; from five "
            "hundred units, about one in five hundred billion. The edge has more spins to work. "
            "<bookmark mark='a'/> Put everything on red once, and the chance is eighteen in thirty-seven, nearly "
            "forty-nine percent. <bookmark mark='b'/> Lester Dubins and Leonard Savage proved in 1965 that in a game "
            "biased against you, bold play is optimal: expose the money to the edge as few times as possible. It is "
            "the mirror image of the lesson for anyone with an edge: bet small and often, and let the law of large "
            "numbers work for you, which is Part eight's Kelly criterion."
        ) as vo:
            self.play(FadeIn(g), FadeIn(xl), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.15),
                      FadeIn(side[:2]))
            vo.wait_until("a")
            self.play(Create(bline), FadeIn(side[2:4]))
            vo.wait_until("b")
            self.play(FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()

    def duration(self, rd):
        F, R = rd["fair"], rd["roulette"]
        rows = [cmath(r"\mathbb{E}[S_\tau^2 - \tau]", r"=", r"0", font_size=40),
                cmath(r"\mathbb{E}\tau", r"=", r"(b - a)^2\,\tfrac{a}{b} + a^2\,\tfrac{b - a}{b}", font_size=40),
                cmath(r"\mathbb{E}\tau", r"=", r"a\,(b - a) = 50 \cdot 50 = 2{,}500", font_size=40,
                      colors={r"a\,(b - a) = 50 \cdot 50 = 2{,}500": MART})]
        whys = [why(r"$S_n^2 - n$ is a martingale (chapter 3), started at 0 with barriers $-a$ and $b - a$; bounded "
                    r"steps and $\mathbb{E}\tau < \infty$: condition (c)"),
                why(r"$S_\tau$ is $b - a$ with probability $a/b$ and $-a$ otherwise"),
                why(r"from 50, aiming for 100: two and a half thousand bets")]
        step = ladder(self, rows, whys, keep=3, top=3.2, x=-2.0, buff=0.6, edge=6.9)
        n_show = 60
        paths = [np.asarray(p_, float) for p_ in F["paths"][:n_show]]
        T = max(len(p_) for p_ in paths)
        g = axes([0, 25 * (T - 1)], [0, 100], x_length=8.4, y_length=2.8, xlabel=r"bets (fair coin, from 50)",
                 xticks=[0, 5000, 10000], yticks=[0, 50, 100], font_size=16).to_edge(DOWN, buff=0.6).to_edge(LEFT, buff=0.7)
        ax = g.ax
        tk = ValueTracker(0.0)
        taus = np.asarray(F["tau"])[:n_show]
        tops = np.asarray(F["top"])[:n_show]

        def fan():
            t = tk.get_value()
            m = int(np.clip(t / 25, 1, T - 1))
            grp = VGroup()
            for i, p_ in enumerate(paths):
                k = min(m, len(p_) - 1)
                pts = [ax.c2p(25 * j, p_[j]) for j in range(k + 1)]
                done = taus[i] <= t
                col = (QC.IDEA if tops[i] else LOSS) if done else P_C
                grp.add(VMobject(stroke_width=1.2, stroke_color=col, stroke_opacity=0.6 if done else 0.35)
                        .set_points_as_corners(pts))
            return grp

        live = always_redraw(fan)
        cnt = always_redraw(lambda: MathTex(
            rf"\text{{finished: }} {int(np.sum(taus <= tk.get_value()))}/{n_show}"
            rf"\quad \text{{at }} 100\text{{: }} {int(np.sum((taus <= tk.get_value()) & tops))}",
            font_size=26, color=QC.IDEA).next_to(g, UP, buff=0.15).align_to(g, LEFT))
        side = VGroup(
            MathTex(rf"\text{{4{{,}}000 games: }} {F['mean']:,.0f} \pm {F['se']:.0f}".replace(",", "{,}"), font_size=28,
                    color=MART),
            MathTex(rf"\text{{reach 100: }} {100 * F['frac_top']:.1f}\%", font_size=28, color=QC.IDEA),
            MathTex(rf"\text{{roulette: }} {R['mean']:,.0f}\ (\text{{theory }} {R['theory']:,.0f})".replace(",", "{,}"),
                    font_size=26, color=P_C),
            MathTex(rf"\text{{reach 100: }} {100 * R['frac_top']:.1f}\%", font_size=26, color=P_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DR, buff=0.4)
        ok = abs(F["mean"] - 2500) <= 2 * F["se"]
        verdict = (f"Four thousand simulated games average {F['mean']:,.0f}, within sampling error of the formula."
                   if ok else f"Four thousand simulated games average {F['mean']:,.0f}, a little off the formula: "
                              "the long games are rare and dominate the average.")
        with self.voiceover(
            "How long does it take? Use the other martingale of chapter three, the square of the walk minus the "
            "number of steps. Start the walk at zero, with barriers at minus a and b minus a. The steps are bounded "
            "and the expected time is finite, so its expected value at the end is zero. <bookmark mark='a'/> At the "
            "end the walk is at one barrier or the other, with the probabilities we just found. <bookmark mark='b'/> "
            "So the expected number of bets is a times b minus a. From fifty, aiming for a hundred: two thousand five "
            "hundred bets. <bookmark mark='c'/> Here are sixty of those games, each turning gold if it reaches a hundred "
            "and red if it goes broke. " + verdict + " On European roulette the games end sooner, and only "
            f"{100 * R['frac_top']:.1f} percent of them at a hundred."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(FadeIn(g))
            self.add(live, cnt)
            self.play(tk.animate.set_value(float(25 * (T - 1))), run_time=8, rate_func=lambda u: u ** 1.5)
            live.clear_updaters()
            cnt.clear_updaters()
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()
