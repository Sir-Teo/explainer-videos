from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant11.common import ALT, GAMMA, OPT, PART, SPOT, THETA, VEGA, illustration, load, pause


class Early(VoiceoverScene):
    def construct(self):
        e = load("early")
        self.card()
        self.merton()
        self.tree(e)
        self.synthetics()
        self.play_game(e)

    def card(self):
        c = chapter_card(12, r"Early exercise, synthetics, and the dividend play", r"When is an option worth more dead "
                         r"than alive?", part=PART)
        with self.voiceover("Chapter twelve. Early exercise, synthetics, and the dividend play."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def merton(self):
        rows = [
            cmath(r"C^{Am}", r"\ge", r"\max(S - K, 0)", font_size=40),
            cmath(r"C^{Eu}", r"\ge", r"S - Ke^{-r\tau} > S - K \qquad (\text{no dividends},\ r > 0)", font_size=36),
            cmath(r"\text{exercise}", r"<", r"\text{sell}:\quad C^{Am} = C^{Eu}", font_size=38),
            cmath(r"S - K", r"<", r"S - D - Ke^{-r(T - t)} + P(S - D, K, T - t)", font_size=34),
            cmath(r"\text{exercise}", r"\iff", r"D > K\big(1 - e^{-r(T - t)}\big) + P", font_size=38,
                  colors={r"\text{exercise}": GAMMA}),
        ]
        whys = [why(r"an American call can always be exercised, so it is worth at least its intrinsic value"),
                why(r"put--call parity with a non-negative put: a European call is worth at least the forward's "
                    r"intrinsic value, which beats exercising now"),
                why(r"Merton (1973): never exercise an American call on a stock that pays no dividend; sell it, or "
                    r"short the stock against it"),
                why(r"just before an ex-dividend date: exercise gives $S - K$; holding is worth the ex-dividend "
                    r"call, which parity writes with the put"),
                why(r"exercise only when the dividend beats the interest on the strike plus the insurance the put "
                    r"provides")]
        step = ladder(self, rows, whys, keep=4, top=3.0, x=-0.6, buff=0.5, edge=6.9)
        pc = pause(r"No dividends, a deep in-the-money call. Exercise to lock in the gain?", width=5.0, font_size=21)
        with self.voiceover(
            "An American option can be exercised any day. When should it be? Start with a call. Because it can be "
            "exercised now, it is worth at least its intrinsic value. <bookmark mark='a'/> But a European call is "
            "worth at least the stock minus the discounted strike, by put-call parity, since the put is worth "
            "something: that is more than exercising today, which pays the strike now instead of later. "
            "<bookmark mark='b'/> So, Robert Merton's result of 1973: on a stock that pays no dividend, never "
            "exercise an American call early. Pause and predict: a deep in-the-money call, no dividends, should you "
            "exercise to lock in the gain? No: sell it, or short the stock against it. <bookmark mark='c'/> Dividends change this. Just "
            "before the stock goes ex-dividend, exercise gives S minus K. Holding gives the call on the stock after "
            "it drops by the dividend, which parity writes as the stock minus the dividend, minus the discounted "
            "strike, plus a put. <bookmark mark='d'/> So exercise exactly when the dividend is larger than the "
            "interest on the strike plus the put's value: a deep in-the-money call, a big dividend, little time left."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            self.play(FadeIn(pc))
            vo.wait_until("c")
            self.play(FadeOut(pc))
            step(3)
            vo.wait_until("d")
            step(4)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tree(self, e):
        layers = e["layers"]
        N = e["N"]
        region = {(int(n), int(j)) for n, j, _ in e["region"]}
        dx, dy = 1.05, 0.29
        g = VGroup()
        nodes = {}
        for n in range(N + 1):
            for j in range(n + 1):
                p = np.array([n * dx, (2 * j - n) * dy, 0.0])
                s = layers[n][j]
                itm = s > e["K"]
                c = Circle(radius=0.12, stroke_color=GREY_B, stroke_width=1.5,
                           fill_color=interpolate_color(ManimColor(BACKGROUND), ManimColor(OPT), 0.35 if itm else 0.0),
                           fill_opacity=1).move_to(p)
                nodes[(n, j)] = c
        edges = VGroup()
        for n in range(N):
            for j in range(n + 1):
                for jj in (j, j + 1):
                    edges.add(Line(nodes[(n, j)].get_center(), nodes[(n + 1, jj)].get_center(), color=GREY_D,
                                   stroke_width=1))
        circ = VGroup(*nodes.values())
        g.add(edges, circ)
        g.move_to(LEFT * 1.4 + DOWN * 0.2)
        if g.width > 10:
            g.scale_to_fit_width(10)
        x_div = nodes[(0, 0)].get_center()[0] + (nodes[(1, 0)].get_center()[0] - nodes[(0, 0)].get_center()[0]) * e["tD_step"]
        divl = DashedLine([x_div, 3.0, 0], [x_div, -3.3, 0], color=ALT, stroke_width=2)
        dl = label(rf"ex-dividend: $D = {e['D']:.0f}$", font_size=20, color=ALT).next_to([x_div, 3.0, 0], UP, buff=0.05)
        gold = VGroup(*[nodes[k].copy().set_fill(YELLOW, 1).set_stroke(YELLOW) for k in sorted(region)])
        n_, j_, s_ = e["node"]
        side = VGroup(
            label(rf"American {e['price']:.2f}, European {e['european']:.2f}", font_size=22, color=OPT),
            wrapped_label(r"gold: exercise beats holding. Every gold node sits on the last step before the dividend, "
                          r"in the money", 3.6, 19, YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.35)
        # the race at the deepest gold node
        bars = VGroup()
        scale = 1.2 / e["D"]
        for i, (v, c, t) in enumerate(((e["D"], GAMMA, r"dividend"), (e["carry"], THETA, r"interest on $K$"),
                                       (e["put"], VEGA, r"the put"))):
            r_ = Rectangle(width=max(v * scale, 0.02), height=0.28, stroke_width=0, fill_color=c, fill_opacity=0.85)
            r_.move_to([0, -i * 0.4, 0], aligned_edge=LEFT)
            bars.add(VGroup(r_, label(t + rf" {v:.2f}", font_size=17, color=c).next_to(r_, RIGHT, buff=0.1)))
        bars.to_corner(DR, buff=0.5)
        src = illustration(rf"$S = K = 100$, two months, {100 * e['r']:.0f}\% rates, {100 * e['sigma']:.0f}\% vol, "
                           r"a dividend of 2 three weeks before expiry; a 10-step tree (prices: 400 steps)", corner=DL)
        with self.voiceover(
            "See it on a tree. The House's tree for an American call on a stock that pays a dividend of two, three "
            "weeks before a two-month expiry; the dashed line is the ex-dividend date. Shaded nodes are in the money. "
            "<bookmark mark='a'/> At every node, compare exercising with holding. The gold nodes are where exercise "
            "wins, and every one sits on the last step before the dividend, deep in the money: nowhere else. "
            f"<bookmark mark='b'/> At the deepest of them, the dividend of {e['D']:.0f} races the interest on the strike, "
            f"{e['carry']:.2f}, plus the put, {e['put']:.3f}: the dividend wins easily. The right to do this is why the "
            f"American call is worth {e['price']:.2f} against the European {e['european']:.2f}."
        ) as vo:
            self.play(FadeIn(edges), FadeIn(circ), Create(divl), FadeIn(dl), FadeIn(src), run_time=2)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x, scale=1.5) for x in gold], lag_ratio=0.3), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Indicate(gold[-1]), LaggedStart(*[GrowFromEdge(b_[0], LEFT) for b_ in bars], lag_ratio=0.3),
                      FadeIn(VGroup(*[b_[1] for b_ in bars])), run_time=2)
            self.play(FadeIn(side[0]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def synthetics(self):
        rows = [cmath(r"C - P", r"=", r"S - Ke^{-r\tau}", font_size=40),
                cmath(r"\text{conversion}", r"=", r"\text{long } S,\ \text{short } C,\ \text{long } P = Ke^{-r\tau}",
                      font_size=34),
                cmath(r"\text{reversal}", r"=", r"\text{short } S,\ \text{long } C,\ \text{short } P", font_size=34)]
        whys = [why(r"put--call parity (Part 9): a long call and a short put at one strike are a synthetic forward"),
                why(r"stock plus a synthetic short forward: riskless, so it must earn the riskless rate"),
                why(r"the mirror image; a box (Part 9) is a conversion at one strike and a reversal at another")]
        step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.6, buff=0.9, edge=6.9)
        with self.voiceover(
            "Two words from every options floor. A call minus a put at the same strike is a synthetic forward, Part "
            "nine's parity. <bookmark mark='a'/> Stock plus a synthetic short forward is a conversion, riskless. "
            "<bookmark mark='b'/> Its mirror is the reversal: how a market maker turns a call into a put."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def play_game(self, e):
        L = e["lottery"]
        pool = np.asarray(L["pool"])
        hit = np.asarray(L["hit"], bool)
        cells = VGroup()
        for i, mine in enumerate(pool):
            cells.add(Square(0.36, stroke_width=1.5, stroke_color=YELLOW if mine else GREY_B,
                             fill_color=YELLOW if mine else GREY_B, fill_opacity=0.25))
        cells.arrange_in_grid(rows=5, cols=10, buff=0.08).to_edge(LEFT, buff=0.7).shift(UP * 0.4)
        marks = VGroup(*[Cross(cells[i], stroke_width=3, stroke_color=QC.LOSS).scale(0.7) for i in range(len(pool))
                         if hit[i]])
        leg = VGroup(label(rf"{L['others']} short calls held by others (grey)", font_size=19, color=GREY_B),
                     label(rf"{L['mine']} short calls of the player's wash (gold)", font_size=19, color=YELLOW),
                     label(rf"{L['exercised']} exercises, assigned at random (red)", font_size=19, color=QC.LOSS)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(cells, DOWN, buff=0.35).align_to(cells, LEFT)
        rows = [cmath(r"\Pr(\text{assigned})", r"\approx", r"\frac{e\,OI + w}{OI + w}", font_size=34),
                cmath(r"\mathbb{E}[\text{gain}]", r"=", r"w\,D\,\frac{(1 - e)\,OI}{OI + w}", font_size=36,
                      colors={r"\mathbb{E}[\text{gain}]": GAMMA})]
        eqs = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5).shift(UP * 1.6)
        side = VGroup(
            label(rf"this draw: {L['mine_free']} of the player's shorts escape (expected {L['expected_free']:.1f})",
                  font_size=20, color=YELLOW),
            wrapped_label(r"each escaped short call drops by about the dividend overnight: the player collects what "
                          r"the holders who forgot to exercise left on the table", 4.8, 19, GREY_A),
            wrapped_label(r"Pool, Stoll and Whaley (2008): many holders fail to exercise before ex-dates, and traders "
                          r"capture most of it; Hao, Kalay and Mayhew (2010): volume spikes on the last cum-dividend "
                          r"day", 4.8, 18, ALT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(eqs, DOWN, buff=0.4).align_to(eqs, LEFT)
        src = illustration(r"illustration: 60\% of the others' calls are exercised")
        with self.voiceover(
            "And the trading game around it. On the day before an ex-date, some holders of in-the-money calls forget "
            "to exercise. Whoever is short their calls, and not assigned, keeps the dividend's worth. So a trader "
            "buys and sells the same call in equal size, a wash, then exercises all its own long calls. "
            "<bookmark mark='a'/> Exercises are assigned to short positions at random. "
            "<bookmark mark='b'/> In expectation, with open interest OI, an exercised share e and a wash of w, the "
            "gain is w times the dividend times one minus e, times OI over OI plus w: as w grows, it approaches all "
            f"of the forgotten value. In this draw, {L['mine_free']} of the player's shorts escaped. "
            "<bookmark mark='c'/> Veronika Pool, Hans Stoll and Robert Whaley documented the forgotten money in 2008, "
            "and Jia Hao, Avner Kalay and Stewart Mayhew the volume spike it draws."
            " Next: options on an index against options on its members, and the correlation between them."
        ) as vo:
            self.play(FadeIn(cells), FadeIn(leg[:2]), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(m_) for m_ in marks], lag_ratio=0.05, run_time=2.5), FadeIn(leg[2]))
            vo.wait_until("b")
            self.play(FadeIn(eqs), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()
