from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant11.common import GAMMA, OPT, PART, SPOT, THETA, VEGA, load, real_data


class Scalp(VoiceoverScene):
    def construct(self):
        s = load("scalp")
        self.card()
        self.trades(s)
        self.ledger(s)

    def card(self):
        c = chapter_card(2, r"Gamma scalping on a real path", r"How does a long straddle turn moves into money?",
                         part=PART)
        with self.voiceover("Chapter two. Gamma scalping, on a real path."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def trades(self, s):
        t, S, sh = np.asarray(s["t"]), np.asarray(s["S"]), np.asarray(s["shares"])
        g1 = axes([0, 30], [50, 110], x_length=7.4, y_length=2.6, ylabel=r"bitcoin (per 100)", xticks=[0, 10, 20, 30],
                  yticks=[60, 80, 100], font_size=16)
        g2 = axes([0, 30], [-1, 1], x_length=7.4, y_length=2.2, xlabel=r"days from 1 May 2021",
                  ylabel=r"hedge: units of bitcoin held", xticks=[0, 10, 20, 30], yticks=[-1, 0, 1], font_size=16)
        VGroup(g1, g2).arrange(DOWN, buff=0.4).to_edge(LEFT, buff=0.6).shift(DOWN * 0.1)
        ls = curve(g1.ax, t[::2], S[::2], SPOT, stroke_width=2.5)
        lh = curve(g2.ax, t[::2], np.clip(sh[::2], -1, 1), OPT, stroke_width=2.5)
        d = np.diff(sh)
        buys = VGroup(*[Dot(g1.ax.c2p(t[i + 1], S[i + 1]), radius=0.04, color=GAMMA) for i in range(0, len(d), 3) if d[i] > 0.01])
        sells = VGroup(*[Dot(g1.ax.c2p(t[i + 1], S[i + 1]), radius=0.04, color=THETA) for i in range(0, len(d), 3) if d[i] < -0.01])
        leg = legend([(GAMMA, r"hedge buys"), (THETA, r"hedge sells")], font_size=18).next_to(g1, UP, buff=0.05).align_to(g1, RIGHT)
        side = VGroup(
            wrapped_label(r"long gamma means the hedge always trades against the move: it buys after falls and sells "
                          r"after rises, locking in a little of each swing", 4.2, 20, GREY_A),
            wrapped_label(r"the straddle's delta runs from zero toward $-1$ as bitcoin falls: by the low, the hedge "
                          r"holds almost a full unit, bought all the way down", 4.2, 20, OPT),
            wrapped_label(r"after the crash the strike is far away: the hedge barely trades, and theta keeps charging", 4.2,
                          20, THETA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        src = real_data(r"Binance BTCUSDT hourly; hedge rebalanced every hour (the House's \texttt{hedge})")
        with self.voiceover(
            "Here is the scalper at work. Every hour the hedge resets to the straddle's delta. Because the straddle is "
            "long gamma, the hedge always trades against the market: it buys after falls and sells after rises, and "
            "each round trip locks in a little of the swing. <bookmark mark='a'/> When Bitcoin slid in the middle of "
            "the month, the straddle's delta ran toward minus one, and the hedge bought all the way down, ending "
            "with almost a whole Bitcoin. <bookmark mark='b'/> After the crash, the strike was far away. The "
            "straddle had become a put deep in the money, nearly linear, with little gamma, and the hedge barely "
            "traded, while theta kept charging."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(src), Create(ls), FadeIn(side[0]), run_time=2)
            self.play(FadeIn(buys), FadeIn(sells), FadeIn(leg))
            vo.wait_until("a")
            self.play(FadeIn(g2), Create(lh), FadeIn(side[1]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def ledger(self, s):
        t, gam, the, book = (np.asarray(s[k]) for k in ("t", "gamma", "theta", "book"))
        lo, hi = float(min(the.min(), book.min(), 0)) - 1, float(max(gam.max(), book.max())) + 1
        g = axes([0, 30], [lo, hi], x_length=7.4, y_length=4.4, xlabel=r"days from 1 May 2021",
                 ylabel=r"cumulative, per 100 of bitcoin", xticks=[0, 10, 20, 30], yticks=[-10, 0, 10, 20], font_size=17)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        lg = curve(ax, t[::2], gam[::2], GAMMA, stroke_width=3)
        lt = curve(ax, t[::2], the[::2], THETA, stroke_width=3)
        lb = curve(ax, t[::2], book[::2], OPT, stroke_width=4)
        leg = legend([(GAMMA, r"gamma: $\frac12\Gamma\,dS^2$, summed"), (THETA, r"theta: $-\frac12\Gamma S^2\sigma_{imp}^2 dt$"),
                      (OPT, r"the hedged straddle")], font_size=19).next_to(g, UP, buff=0.05).align_to(g, LEFT)
        side = VGroup(
            MathTex(rf"\text{{gamma }} {gam[-1]:+.1f},\ \ \text{{theta }} {the[-1]:+.1f}", font_size=30),
            MathTex(rf"\text{{net }} {s['pnl']:+.1f}", font_size=34, color=OPT),
            wrapped_label(r"gamma's earnings are weighted by gamma at the time of the move, so they come from the days "
                          r"spot was near the strike; Part 10's identity, on a real crash", 4.2, 20, GREY_A),
            wrapped_label(r"a variance swap pays the realized variance without this weighting: Part 12 builds one from "
                          r"a strip of options", 4.2, 20, VEGA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Add up the ledger. The gamma terms, one half gamma times each squared move, came to "
            f"{gam[-1]:.1f}. The theta terms, the implied variance charged hour by hour, came to {the[-1]:.1f}. "
            f"<bookmark mark='a'/> The net, {s['pnl']:+.1f}. Gamma earns most when the move happens near the strike; "
            "the biggest moves of the month happened far from it. <bookmark mark='b'/> If you want to be paid the "
            "realized variance without that weighting, you trade a variance swap, which Part twelve builds from a "
            "strip of options."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), Create(lg), Create(lt), run_time=2.5)
            self.play(FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(lb), FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()
