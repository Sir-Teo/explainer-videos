from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant10.common import (DEL, GAIN, GAM, IMP, LOSS, OPT, PART, REA, SPOT, THE, load)

C_ = {r"\Theta": THE, r"\Gamma": GAM, r"\sigma_i^2": IMP, r"\sigma_r^2": REA, r"dS^2": SPOT, r"(dS)^2": SPOT,
      r"\Delta": DEL, r"dV": OPT, r"dS": SPOT, r"S^2": SPOT}


def row(*parts, fs=38):
    return cmath(*parts, colors=C_, font_size=fs)


class Ledger(VoiceoverScene):
    def construct(self):
        L = load("ledger")
        self.card()
        self.derive()
        self.breakeven(L)
        self.lab(L)
        self.three_paths(L)
        self.distributions(L)

    def card(self):
        c = chapter_card(7, r"Where the hedger's money comes from", r"What does a hedged option book bet on?",
                         lit=(1973,), part=PART)
        with self.voiceover("Chapter seven. Where the hedger's money comes from."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def derive(self):
        rows = [
            row(r"d(\text{book})", r"=", r"-\big(", r"dV", r"-", r"\Delta", r"\,", r"dS", r"\big)"),
            row(r"d(\text{book})", r"=", r"-\big(", r"\Theta", r"\,dt", r"+", r"\tfrac12", r"\Gamma", r"\,",
                r"(dS)^2", r"\big)"),
            row(r"d(\text{book})", r"=", r"-\big(", r"\Theta", r"\,dt", r"+", r"\tfrac12", r"\Gamma", r"\,",
                r"S^2", r"\sigma_r^2", r"\,dt", r"\big)"),
            row(r"d(\text{book})", r"=", r"\tfrac12", r"\Gamma", r"\,", r"S^2", r"\big(", r"\sigma_i^2", r"-",
                r"\sigma_r^2", r"\big)", r"\,dt", fs=46),
        ]
        whys = [why(r"short one option, long $\Delta$ shares (marked at $\sigma_i$; $r = 0$)"),
                why(r"Taylor to second order; the $\Delta$ term cancels the slope"),
                why(r"It\^o: the stock really moves with $\sigma_r$, so $(dS)^2 = S^2\sigma_r^2\,dt$"),
                why(r"chapter six: $\Theta = -\tfrac12\sigma_i^2 S^2\Gamma$")]
        step = ladder(self, rows, whys, keep=4, top=3.0, x=-2.4, buff=0.6, edge=6.9)
        legend_ = VGroup(
            VGroup(MathTex(r"\sigma_i", font_size=34, color=IMP), label(r"implied: the volatility the option was "
                                                                         r"sold at, and is hedged at",
                                                                         font_size=24, color=IMP)).arrange(RIGHT),
            VGroup(MathTex(r"\sigma_r", font_size=34, color=REA), label(r"realized: the volatility the stock "
                                                                         r"actually moves with",
                                                                         font_size=24, color=REA)).arrange(RIGHT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Take the seller's side: short one option, long delta shares, the option marked at the volatility it "
            "was sold at, sigma i, implied. The stock moves with the volatility the world delivers, sigma r, "
            "realized. <bookmark mark='a'/> Expand the option's change to second order: the hedge cancels the "
            "first-order term, leaving theta dt plus half gamma times the squared move. <bookmark mark='b'/> By "
            "Ito, the squared move is S squared times the realized variance times dt. <bookmark mark='c'/> And "
            "theta is minus half the implied variance times S squared gamma. So the book earns half gamma S "
            "squared times the gap between implied and realized variance, every instant: a bet that the stock "
            "moves less than you charged for, weighted by gamma."
        ) as vo:
            step(0)
            self.play(FadeIn(legend_))
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            self.play(Create(SurroundingRectangle(rows[3], color=GAM, buff=0.18, corner_radius=0.1)))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def breakeven(self, L):
        j = 2  # the 28% path: plenty of days on both sides of the line
        S = np.asarray(L[f"S_{j}"], float)
        t = np.asarray(L["t"], float)
        dt = t[1] - t[0]
        ret = np.diff(np.log(S))
        be = L["sigma_i"] * np.sqrt(dt)
        n = 80
        g = axes([0, n], [-0.034, 0.034], x_length=9.6, y_length=4.0, xlabel=r"hedging interval (four a day)",
                 ylabel=r"the stock's move", yticks=[-0.03, 0, 0.03], yfmt=lambda v: f"{100 * v:+.0f}\\%" if v else "0",
                 font_size=20).shift(DOWN * 0.5)
        ax = g.ax
        bars = VGroup()
        cols = []
        for i in range(n):
            col = GREY_B
            cols.append(GAIN if abs(ret[i]) < be else LOSS)
            y0, y1 = ax.c2p(i + 0.5, 0)[1], ax.c2p(i + 0.5, ret[i])[1]
            bars.add(Rectangle(width=ax.x_length / n * 0.7, height=max(abs(y1 - y0), 0.004), stroke_width=0,
                               fill_color=col, fill_opacity=0.9).move_to([ax.c2p(i + 0.5, 0)[0], (y0 + y1) / 2, 0]))
        band = Rectangle(width=ax.x_length, height=ax.c2p(0, be)[1] - ax.c2p(0, -be)[1], stroke_width=0,
                         fill_color=IMP, fill_opacity=0.12).move_to(ax.c2p(n / 2, 0))
        edges = VGroup(DashedLine(ax.c2p(0, be), ax.c2p(n, be), color=IMP, stroke_width=1.5),
                       DashedLine(ax.c2p(0, -be), ax.c2p(n, -be), color=IMP, stroke_width=1.5))
        be_lab = MathTex(rf"\pm\,\sigma_i\sqrt{{dt}} = \pm{100 * be:.2f}\%", font_size=30, color=IMP)
        be_lab.next_to(g, UP, buff=0.15).align_to(g, RIGHT)
        key = VGroup(VGroup(Square(0.22, fill_color=GAIN, fill_opacity=0.9, stroke_width=0),
                            label(r"inside: theta wins, a profitable interval", font_size=22, color=GAIN))
                     .arrange(RIGHT, buff=0.15),
                     VGroup(Square(0.22, fill_color=LOSS, fill_opacity=0.9, stroke_width=0),
                            label(r"outside: gamma wins, a losing interval", font_size=22, color=LOSS))
                     .arrange(RIGHT, buff=0.15)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        key.next_to(g, UP, buff=0.55).align_to(g, LEFT)
        frac_in = float(np.mean(np.abs(ret) < be))
        with self.voiceover(
            "One interval at a time: the seller collects theta and pays half gamma times the squared move; they "
            "cancel when the move is sigma i times root dt, the breakeven. <bookmark mark='a'/> A path hedged four "
            f"times a day at twenty percent: green intervals stay inside the band and win; red ones lose, "
            f"quadratically. This path realizes {100 * L['rows'][j]['realized']:.0f} percent; "
            f"{100 * frac_in:.0f} percent of its intervals win, and the seller still loses."
        ) as vo:
            self.play(FadeIn(g), LaggedStart(*[GrowFromEdge(b, DOWN if b.get_y() > ax.c2p(0, 0)[1] else UP)
                                               for b in bars], lag_ratio=0.02, run_time=3))
            self.play(FadeIn(band), Create(edges), FadeIn(be_lab))
            vo.wait_until("a")
            self.play(FadeIn(key), LaggedStart(*[b.animate.set_fill(c) for b, c in zip(bars, cols)],
                                               lag_ratio=0.03, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lab(self, L):
        card = lab_card(r"the hedger's ledger", [
            "for i in range(1, n1):",
            "    gi = bs.greeks(S[:, i], K, tau[i], sig_h, r, q, cp)",
            "    dS = S[:, i] - s_prev",
            "    step = w * (gi['price'] - v_prev - delta * dS)",
            "    mtm += step                           # the book's change",
            "    gam_acc += w * 0.5 * gam_prev * dS**2      # gamma",
            "    the_acc += -w * 0.5 * gam_prev * s_prev**2 * sig_h**2 * dt",
            "    delta = gi['delta']                   # rebalance",
            "residual = mtm - gam_acc - the_acc",
        ], source="explainer/quant/house/hedge.py (delta_hedge, at r = q = 0; abridged)", width=8.2)
        card.to_edge(UP, buff=0.45)
        outs = []
        for j in (0, 2, 1):
            g, th = float(L[f"gamma_{j}"][-1]), float(L[f"theta_{j}"][-1])
            pnl = float(L["rows"][j]["pnl"])
            outs.append(f"realized {100 * L['rows'][j]['realized']:.0f}%:  gamma {g:+.2f}  theta {th:+.2f}  "
                        f"residual {pnl - g - th:+.2f}  P&L {pnl:+.2f}")
        res = [abs(float(L["rows"][j]["pnl"]) - float(L[f"gamma_{j}"][-1]) - float(L[f"theta_{j}"][-1])) for j in range(3)]
        with self.voiceover(
            "The House's hedger keeps the score: each step it marks the option, books the change against the "
            "shares, and splits it into the gamma term, the theta term, and what is left. <bookmark mark='a'/> On "
            "quarters realizing twelve, twenty-eight and twenty percent, the residual, what the expansion misses, "
            f"is never more than {max(res):.2f}."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, outs)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def three_paths(self, L):
        t = np.asarray(L["t"], float)
        days = t * 252
        n = len(t) - 1
        k = ValueTracker(0)
        top = axes([0, 63], [85, 118], x_length=9.4, y_length=2.7, ylabel=r"the stock", yticks=[90, 100, 110],
                   xlabel=r"trading days", xticks=[0, 21, 42, 63], font_size=20).to_corner(UL, buff=0.45)
        ax = top.ax
        kline = DashedLine(ax.c2p(0, 100), ax.c2p(63, 100), color=QC.STRIKE, stroke_width=1.2)
        title = VGroup()
        ledger_pos = DOWN * 2.05 + RIGHT * 0.6
        rv_box = VGroup()
        stage = {}

        def build(j):
            S = np.asarray(L[f"S_{j}"], float)
            path = tracing(ax, days, S, k, SPOT, stroke_width=2.5)
            led = HedgeLedger(L[f"gamma_{j}"], L[f"theta_{j}"], L[f"book_{j}"], k, scale=3.0, half_width=3.3,
                              bar_h=0.5, font_size=28,
                              names=(r"gamma: $-\tfrac12\Gamma\,\Delta S^2$", r"theta: $-\Theta\,\Delta t$",
                                     r"the book"))
            led.move_to(ledger_pos)
            rv = L["rows"][j]["realized"]
            head = VGroup(MathTex(r"\sigma_i = 20\%", font_size=36, color=IMP),
                          MathTex(rf"\sigma_r = {100 * rv:.0f}\%", font_size=36, color=REA)).arrange(DOWN, buff=0.2,
                                                                                                aligned_edge=LEFT)
            head.to_corner(UR, buff=0.7)
            return path, led, head

        with self.voiceover(
            "Now watch those three quarters, each hedged four times a day, short a three-month at-the-money call "
            "sold at twenty percent. Pink: the gamma term, what the squared moves cost. Blue: the theta term, "
            "what time paid. White: the book. <bookmark mark='a'/> At twelve percent realized, theta's income "
            "outruns gamma's bill all quarter, and the book ends up "
            f"{L['rows'][0]['pnl']:.2f}, on a premium of {L['premium']:.2f}. <bookmark mark='b'/> At twenty-eight, "
            f"gamma's bill wins and the book loses {-L['rows'][2]['pnl']:.2f}. <bookmark mark='c'/> At twenty, the "
            f"volatility it was sold at, the two cancel: {L['rows'][1]['pnl']:.2f}. The direction of the stock "
            "never entered."
        ) as vo:
            self.play(FadeIn(top), Create(kline))
            first = build(0)
            self.add(first[0])
            self.play(FadeIn(first[1]), FadeIn(first[2]))
            for led_part in (first[1].names[0], first[1].names[1], first[1].names[2]):
                self.play(Indicate(led_part, scale_factor=1.15), run_time=0.8)
            for idx, (j, mark) in enumerate(((0, "a"), (2, "b"), (1, "c"))):
                vo.wait_until(mark)
                if idx:
                    old = stage["objs"]
                    self.play(FadeOut(old), run_time=0.6)
                    k.set_value(0)
                    path, led, head = build(j)
                    self.add(path)
                    self.play(FadeIn(led), FadeIn(head))
                else:
                    path, led, head = first
                self.play(k.animate.set_value(n), run_time=7 if idx < 2 else 6, rate_func=linear)
                stage["objs"] = VGroup(path, led, head)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def distributions(self, L):
        rows = L["rows"]
        lo, hi = -4.5, 3.5
        panels = VGroup()
        for j, col in ((0, GAIN), (1, GREY_B), (2, LOSS)):
            pnl = np.asarray(L[f"pnl_many_{j}"], float)
            g = axes([lo, hi], [0, 1.05], x_length=3.8, y_length=2.2, xlabel=r"P\&L at expiry",
                     xticks=[-4, -2, 0, 2], font_size=18)
            h, e = np.histogram(np.clip(pnl, lo, hi), bins=60, range=(lo, hi))
            h = h / h.max()
            bars = VGroup(*[Rectangle(width=g.ax.x_length / 60 * 0.95, height=max(g.ax.y_length * v, 0.002),
                                      stroke_width=0, fill_color=col, fill_opacity=0.85)
                            .move_to(g.ax.c2p((e[i] + e[i + 1]) / 2, 0), aligned_edge=DOWN)
                            for i, v in enumerate(h)])
            zero = DashedLine(g.ax.c2p(0, 0), g.ax.c2p(0, 1.05), color=GREY_C, stroke_width=1.2)
            head = MathTex(rf"\sigma_r = {100 * rows[j]['sigma_r']:.0f}\%", font_size=32, color=REA)
            stat = MathTex(rf"\text{{mean}}\ {rows[j]['mean']:+.2f},\ \text{{sd}}\ {rows[j]['sd']:.2f}",
                           font_size=26, color=col)
            head.next_to(g, UP, buff=0.15)
            stat.next_to(g, DOWN, buff=0.15)
            panels.add(VGroup(g, bars, zero, head, stat))
        panels.arrange(RIGHT, buff=0.45).shift(UP * 0.4)
        cap = label(r"20,000 paths at each realized volatility, all hedged at $\sigma_i = 20\%$", font_size=24,
                    color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Pause and predict: when realized equals implied, does every path end at zero? Twenty thousand paths "
            f"each. At twelve percent the seller makes {rows[0]['mean']:.2f} on average, and "
            f"{100 * rows[0]['p_loss']:.0f} percent of paths lose. At twenty-eight, the seller loses "
            f"{-rows[2]['mean']:.2f} on average. At twenty the average is {rows[1]['mean']:+.2f}, with a spread of "
            f"{rows[1]['sd']:.2f} from hedging four times a day: chapter nine. The profit is the gap between two "
            "volatilities, one quoted, one lived."
        ):
            self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in panels], lag_ratio=0.4, run_time=3),
                      FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()
