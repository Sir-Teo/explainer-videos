from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import BAD, DELTA, GOOD, NET, PART, REF, illustration, load


def trade_map(ax, S, P, Z, vmax=0.3, stride=2):
    """Cells coloured by the trade the network makes: buying (green), selling (red), nothing (dark); every
    ``stride``-th grid point, so a map is a few hundred cells."""
    S, P, Z = S[::stride], P[::stride], np.asarray(Z)[::stride, ::stride]
    dS, dP = S[1] - S[0], P[1] - P[0]
    cells = VGroup()
    for i in range(len(P)):
        for j in range(len(S)):
            z = float(np.clip(Z[i][j] / vmax, -1, 1))
            col = interpolate_color(ManimColor("#0E1117"), ManimColor(GOOD if z > 0 else BAD), abs(z) ** 0.7)
            p0 = ax.c2p(S[j] - dS / 2, P[i] - dP / 2)
            p1 = ax.c2p(S[j] + dS / 2, P[i] + dP / 2)
            cells.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                                fill_opacity=1).move_to((p0 + p1) / 2))
    return cells


class Band(VoiceoverScene):
    def construct(self):
        h = load("hedge")
        self.card()
        self.replay(h)
        self.surface(h)

    def card(self):
        c = chapter_card(8, r"The band, rediscovered", r"Your hedger has costs. Why does the optimal hedge have a band?",
                         part=PART)
        with self.voiceover("Chapter eight. The band, rediscovered."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def replay(self, h):
        m = h["mlp_cost"]
        S, P = np.asarray(m["S"]), np.asarray(m["prev"])
        keys = sorted(m["snaps"], key=int)
        g = axes([S[0], S[-1]], [0, 1], x_length=6.4, y_length=4.6, xlabel=r"price, 15 days before expiry",
                 ylabel=r"shares already held", xticks=[90, 100, 110], yticks=[0, 0.5, 1],
                 font_size=15).to_edge(LEFT, buff=0.7).shift(DOWN * 0.25)
        ax = g.ax
        maps = [trade_map(ax, S, P, np.asarray(m["snaps"][k])) for k in keys]
        ww = VGroup(DashedVMobject(curve(ax, S, np.clip(np.asarray(m["ww_lo"]), 0, 1), WHITE, stroke_width=2.5), num_dashes=30),
                    DashedVMobject(curve(ax, S, np.clip(np.asarray(m["ww_hi"]), 0, 1), WHITE, stroke_width=2.5), num_dashes=30))
        dl = curve(ax, S, np.asarray(m["delta"]), DELTA, stroke_width=2)
        counter = label(rf"training step {keys[0]}", font_size=24, color=NET).next_to(g, UP, buff=0.15).align_to(g, LEFT)
        leg = legend([(GOOD, r"the network buys"), (BAD, r"the network sells"), (GREY_D, r"it does nothing"),
                      (DELTA, r"Black--Scholes delta"), (WHITE, r"Whalley--Wilmott band (1997)")], font_size=17)
        leg.next_to(g, RIGHT, buff=0.4).align_to(g, UP)
        side = wrapped_label(rf"cost {100 * m['cost']:g}\% a trade. The network sees the price, the time left and its own "
                             r"holding; no one told it about bands. It learns to leave the holding alone inside a corridor "
                             r"around delta and to trade only to the nearest edge: the shape Whalley and Wilmott derived "
                             r"for small costs", 4.4, 19, GREY_A).next_to(leg, DOWN, buff=0.35).align_to(leg, LEFT)
        src = illustration(r"a plain network (no band built in), snapshots during training")
        with self.voiceover(
            "This is the hedger's decision, fifteen days before expiry, over every price and every holding it might "
            "already have. Green means it buys, red that it sells, dark that it does nothing. At the start of training "
            "it is noise. <bookmark mark='a'/> Watch it learn. <bookmark mark='b'/> A dark corridor opens around the "
            "Black–Scholes delta: inside it, the holding is left alone; outside it, the network trades back to the "
            "nearest edge, not to the delta. <bookmark mark='c'/> That corridor is the no-trade band that Whalley and "
            "Wilmott derived in 1997, for small costs and exponential utility. Nobody told the network: it found it "
            "from the costs alone."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(maps[0]), FadeIn(counter), FadeIn(leg[:3]))
            vo.wait_until("a")
            for k, mp in zip(keys[1:], maps[1:]):
                new = label(rf"training step {int(k):,}".replace(",", "{,}"), font_size=24, color=NET).move_to(counter, aligned_edge=LEFT)
                self.play(FadeOut(maps[0]) if mp is maps[1] else Wait(0.01), FadeIn(mp), Transform(counter, new), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(dl), FadeIn(leg[3]))
            vo.wait_until("c")
            self.play(Create(ww), FadeIn(leg[4]), FadeIn(side))
        self.wait(0.5)
        self.clear_scene()

    def surface(self, h):
        s = h["band"]["surface"]
        tau = np.asarray(s["tau"]) * 30
        S = np.asarray(s["S"])
        lo, hi, wl, wh = (np.asarray(s[k]) for k in ("lo", "hi", "ww_lo", "ww_hi"))
        width = hi - lo
        wwidth = wh - wl
        g = axes([S[0], S[-1]], [0, 0.6], x_length=7.0, y_length=4.4, xlabel=r"price",
                 ylabel=r"width of the no-trade band (shares)", xticks=[90, 100, 110], yticks=[0, 0.2, 0.4, 0.6],
                 font_size=15).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        picks = [i for i, t in enumerate(tau) if t in (tau[2], tau[9], tau[-1])]
        cols = [GOOD, NET, DELTA]
        lines = VGroup()
        legs = []
        for c, i in zip(cols, picks):
            lines.add(VGroup(curve(ax, S, np.clip(width[i], 0, 0.6), c, stroke_width=3.5),
                             DashedVMobject(curve(ax, S, np.clip(wwidth[i], 0, 0.6), c, stroke_width=2), num_dashes=30)))
            legs.append((c, rf"{tau[i]:.0f} days left"))
        leg = legend(legs + [(GREY_B, r"solid: learned; dashed: Whalley--Wilmott")], font_size=17)
        leg.next_to(g, RIGHT, buff=0.4).align_to(g, UP)
        near = int(np.argmin(np.abs(S - 100)))
        ratio = float(np.median(width[:, near] / np.maximum(wwidth[:, near], 1e-6)))
        side = wrapped_label(rf"a band network (Imaki et al.\ 2021: it outputs the band, and the hedge moves only to its "
                             rf"edge), cost {100 * h['mlp_cost']['cost']:g}\%. At the money its band is "
                             rf"{ratio:.1f} times Whalley--Wilmott's width, and like theirs it is widest where gamma is "
                             r"largest: near the strike, close to expiry", 4.4, 19, GREY_A).next_to(leg, DOWN, buff=0.35).align_to(leg, LEFT)
        with self.voiceover(
            "A second network makes the band explicit: it outputs the two edges, and the hedge only ever moves to the "
            "nearest one. <bookmark mark='a'/> Here is the width it learned, at three times to expiry, against Whalley "
            f"and Wilmott's formula. At the money it is {ratio:.1f} times theirs. Both are widest where gamma is largest, "
            "near the strike and close to expiry, where trading every wiggle would cost the most. The asymptotic formula "
            "assumes small costs; the network does not have to."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.4, run_time=3), FadeIn(side))
        self.wait(0.5)
        self.clear_scene()
