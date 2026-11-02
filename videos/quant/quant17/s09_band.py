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
        c = chapter_card(8, r"Where not to trade", r"Your hedger has costs. Why does the optimal hedge have a band?",
                         part=PART)
        with self.voiceover("Chapter eight. Where not to trade."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def replay(self, h):
        m = h["mlp_cost"]
        n = h["nocost"]
        P = np.asarray(m["prev"])
        keys = sorted(m["snap_slices"], key=int)
        panels = VGroup()
        for s_ in ("95", "100", "105"):
            g = axes([0, 1], [-0.6, 0.6], x_length=3.7, y_length=3.4, xlabel=r"shares already held",
                     ylabel=r"trade" if s_ == "95" else "", xticks=[0, 0.5, 1], yticks=[-0.5, 0, 0.5] if s_ == "95" else [],
                     font_size=13)
            lo, hi, dl = m["ww_slices"][s_]
            ax = g.ax
            band = Rectangle(width=ax.c2p(min(hi, 1), 0)[0] - ax.c2p(max(lo, 0), 0)[0], height=ax.c2p(0, 0.6)[1] - ax.c2p(0, -0.6)[1],
                             stroke_width=0, fill_color=WHITE, fill_opacity=0.08).move_to(
                [(ax.c2p(max(lo, 0), 0)[0] + ax.c2p(min(hi, 1), 0)[0]) / 2, ax.c2p(0, 0)[1], 0])
            zero = DashedLine(ax.c2p(0, 0), ax.c2p(1, 0), stroke_color=GREY_C, stroke_width=1)
            dmark = DashedLine(ax.c2p(dl, -0.6), ax.c2p(dl, 0.6), stroke_color=DELTA, stroke_width=1.5)
            nc = curve(ax, P, np.clip(np.asarray(n["slices"][s_]), -0.6, 0.6), GREY_B, stroke_width=2.5)
            lines = [curve(ax, P, np.clip(np.asarray(m["snap_slices"][k][s_]), -0.6, 0.6), NET, stroke_width=3.5)
                     for k in keys]
            ttl = label(rf"price {s_}", font_size=19).next_to(g, UP, buff=0.1)
            panels.add(VGroup(g, band, zero, dmark, nc, VGroup(*lines), ttl))
        panels.arrange(RIGHT, buff=0.35).to_edge(UP, buff=0.9)
        leg = legend([(GREY_B, r"network trained without costs"), (NET, r"network trained with 0.5\% costs"),
                      (DELTA, r"Black--Scholes delta"), (GREY_D, r"shaded: Whalley--Wilmott no-trade band")], font_size=16)
        leg.arrange(RIGHT, buff=0.4).next_to(panels, DOWN, buff=0.3)
        counter = label(rf"training step {keys[0]}", font_size=22, color=NET).to_edge(UP, buff=0.35)
        fa = m["flat_atm"]
        ev, ww = m["eval"], h["band"]["rows"]
        ww5 = next(r for r in ww if abs(r["cost"] - m["cost"]) < 1e-9)
        w0 = fa["nocost"][1] - fa["nocost"][0] if fa["nocost"] else 0.0
        w1 = fa["cost"][1] - fa["cost"][0] if fa["cost"] else 0.0
        side = wrapped_label(rf"at the money its do-nothing zone widens from {w0:.2f} to {w1:.2f} shares, and from far away it "
                             rf"buys or sells only part of the way. Its price, {ev['price']:.2f}, matches the Whalley--Wilmott "
                             rf"band's {ww5['ww']['price']:.2f}; daily delta hedging needs {ww5['delta']['price']:.2f}. "
                             r"No sharp band, but the principle: small gaps are cheaper to keep than to close", 12.0, 19,
                             GREY_A).to_edge(DOWN, buff=0.3)
        src = illustration(r"15 days before expiry; a plain network, told nothing about bands", corner=UR)
        with self.voiceover(
            "What does the hedger actually do? Here is its trade, against the holding it already has, at three prices "
            "fifteen days before expiry. In grey, a network trained without costs: whatever it holds, it trades straight "
            "to the Black–Scholes delta, so the line crosses zero exactly there. <bookmark mark='a'/> Now a network "
            "trained with costs of half a percent, told nothing about bands. Watch it learn. <bookmark mark='b'/> The "
            f"line flattens. Near the delta it leaves the position alone over a wider range, {w1:.2f} shares instead of "
            f"{w0:.2f}, and from far away it moves only part of the way. <bookmark mark='c'/> The shaded corridor is the "
            "band Whalley and Wilmott derived in 1997. The network has not drawn it sharply, but it has learned its "
            f"principle, and its price, {ev['price']:.2f}, is the band's to the cent. Small gaps are cheaper to keep "
            "than to close."
        ) as vo:
            self.play(FadeIn(src), *[FadeIn(VGroup(pp[0], pp[2], pp[3], pp[6])) for pp in panels], FadeIn(leg[0]),
                      FadeIn(leg[2]))
            self.play(*[Create(pp[4]) for pp in panels])
            vo.wait_until("a")
            self.play(FadeIn(counter), *[Create(pp[5][0]) for pp in panels], FadeIn(leg[1]))
            vo.wait_until("b")
            for idx, k in enumerate(keys[1:], 1):
                new = label(rf"training step {int(k):,}".replace(",", "{,}"), font_size=22, color=NET).move_to(counter)
                self.play(Transform(counter, new), *[Transform(pp[5][0], pp[5][idx]) for pp in panels], run_time=1.4)
            vo.wait_until("c")
            self.play(*[FadeIn(pp[1]) for pp in panels], FadeIn(leg[3]), FadeIn(side))
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
        side = wrapped_label(rf"a band network (Imaki et al.\ 2021: it outputs how far below and above the Black--Scholes "
                             rf"delta the band reaches, and the hedge moves only to its nearest edge), cost {100 * h['mlp_cost']['cost']:g}\%. At the money its band is "
                             rf"{ratio:.1f} times Whalley--Wilmott's width, and like theirs it is widest where gamma is "
                             r"largest: near the strike, close to expiry", 4.4, 19, GREY_A).next_to(leg, DOWN, buff=0.35).align_to(leg, LEFT)
        with self.voiceover(
            "A second network, from Shota Imaki and colleagues, makes the band explicit: it outputs how far the band "
            "reaches below and above the delta, and the hedge only ever moves to the nearest edge. <bookmark mark='a'/> Here is the width it learned, at three times to expiry, against Whalley "
            f"and Wilmott's formula. At the money it is {ratio:.1f} times theirs. Both are widest where gamma is largest, "
            "near the strike and close to expiry, where trading every wiggle would cost the most. The asymptotic formula "
            "assumes small costs; the network does not have to."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.4, run_time=3), FadeIn(side))
        self.wait(0.5)
        self.clear_scene()
