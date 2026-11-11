from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant12.common import BAD, IV, LV, OPT, PART, RV, SPOT, curve_in, load, real_data


class Forward(VoiceoverScene):
    def construct(self):
        m = load("lv_mc")
        self.card()
        self.against(m)
        self.derive(m)
        self.fan(m)

    def card(self):
        c = chapter_card(8, r"Local volatility's future", r"What does local vol predict about tomorrow's smile?",
                         lit=(2002,), part=PART)
        with self.voiceover("Chapter eight. Local volatility's future."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def against(self, m):
        kk = np.asarray(m["kk"])
        sh = np.asarray(m["shifts"])
        lv = np.asarray(m["move"]["lv"])
        mo = np.asarray(m["move"]["moneyness"])
        g = axes([-0.3, 0.3], [0.3, 0.6], x_length=6.6, y_length=4.4, xlabel=r"strike, as $\ln K/F_0$",
                 ylabel=r"30-day implied volatility", xticks=[-0.2, 0, 0.2], yticks=[0.35, 0.45, 0.55],
                 yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=17).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        tr = ValueTracker(4.0)

        def at_i(arr):
            x = tr.get_value()
            i = int(np.clip(np.floor(x), 0, len(arr) - 2))
            f = x - i
            return (1 - f) * arr[i] + f * arr[i + 1]
        today = curve_in(ax, kk, lv[4], 0.3, 0.6, GREY_C, stroke_width=2)
        c_lv = always_redraw(lambda: curve_in(ax, kk, at_i(lv), 0.3, 0.6, LV, stroke_width=4))
        c_mo = always_redraw(lambda: curve_in(ax, kk, at_i(mo), 0.3, 0.6, IV, stroke_width=3))
        spot = always_redraw(lambda: DashedLine(ax.c2p(float(at_i(sh)), 0.3), ax.c2p(float(at_i(sh)), 0.6), color=GREY_B))
        arrow_s = Arrow(LEFT, RIGHT, color=SPOT).scale(0.6).next_to(g, UP, buff=0.15).shift(LEFT * 1.5)
        arrow_l = Arrow(RIGHT, LEFT, color=LV).scale(0.6).next_to(arrow_s, RIGHT, buff=1.2)
        tags = VGroup(label(r"spot", font_size=18, color=SPOT).next_to(arrow_s, UP, buff=0.05),
                      label(r"local vol's smile", font_size=18, color=LV).next_to(arrow_l, UP, buff=0.05))
        leg = legend([(GREY_C, r"today"), (IV, r"sticky moneyness"), (LV, r"local volatility")], font_size=17
                     ).to_edge(RIGHT, buff=0.5).shift(UP * 1.6)
        side = VGroup(MathTex(rf"R_{{\text{{LV}}}} = {m['R_lv']:.2f}", font_size=36, color=LV),
                      wrapped_label(r"measured on the Surface's local vol: close to 2, as the formula below says", 3.9,
                                    19, GREY_A),
                      wrapped_label(r"Hagan, Kumar, Lesniewski and Woodward (2002): local vol's smile moves the wrong "
                                    r"way, so its hedges are wrong; their answer was SABR (Part 13)", 3.9, 19, GREY_B)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(leg, DOWN, buff=0.5).to_edge(RIGHT, buff=0.3)
        leg.align_to(side, LEFT)
        src = real_data(r"the Surface's local vol; smiles by the BBF average")
        R = m["R_lv"]
        with self.voiceover(
            f"In the ideal continuous model, local volatility reproduces a suitable arbitrage-free input surface. Numerical fits retain discretization error. What does it say about tomorrow? Move the spot up, and watch the smile it implies. <bookmark mark='a'/> Under sticky moneyness the smile rides along with the spot. Under local volatility it slides the other way: the local volatility function is pinned to absolute prices, and when the spot climbs past the low-volatility region, the average along the path to each strike changes against it. <bookmark mark='b'/> Measured on the Surface's own local volatility, the skew-stickiness ratio is {R:.2f}. In 2002 Patrick Hagan, Deep Kumar, Andrew Lesniewski and Diana Woodward made this their complaint: a model whose smile moves against the market's gets the delta wrong, however perfectly it fits today."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(today), FadeIn(leg))
            self.add(spot, c_mo, c_lv)
            vo.wait_until("a")
            self.play(FadeIn(arrow_s), FadeIn(arrow_l), FadeIn(tags))
            self.play(tr.animate.set_value(8.0), run_time=3)
            self.play(tr.animate.set_value(0.0), run_time=3.5)
            self.play(tr.animate.set_value(4.0), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(side))
        for x in (c_lv, c_mo, spot):
            x.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def derive(self, m):
        rows = [cmath(r"\sigma_{\text{imp}}(K; S)", r"\approx", r"\sigma_{\text{loc}}\Big(\frac{S + K}{2}\Big)", font_size=38,
                      colors={r"\sigma_{\text{imp}}(K; S)": IV}),
                cmath(r"\partial_K\sigma_{\text{imp}}", r"=", r"\tfrac12\,\sigma'_{\text{loc}},\qquad \partial_S\sigma_{\text{imp}}"
                      r"(K; S) = \tfrac12\,\sigma'_{\text{loc}} = \partial_K\sigma_{\text{imp}}", font_size=34),
                cmath(r"\frac{d\sigma_{\text{ATM}}}{dS}", r"=", r"\sigma'_{\text{loc}} \approx 2\,\partial_K\sigma_{\text{imp}}"
                      r"\ \Rightarrow\ R_{\text{LV}} \approx 2", font_size=36, colors={r"\frac{d\sigma_{\text{ATM}}}{dS}": LV}),
                cmath(r"\text{forward start: }\Big(\frac{S_{T_2}}{S_{T_1}} - e^k\Big)^+", r"\to",
                      r"\text{the law of } S_{T_2}/S_{T_1}\text{: simulate}", font_size=32, colors={}),
                cmath(r"\partial_k\sigma_{\text{loc}}(k, t)", r"\downarrow", r"\text{ as } t \text{ grows} \Rightarrow "
                      r"\text{fading here (calibration dependent)}", font_size=34, colors={r"\partial_k\sigma_{\text{loc}}(k, t)": BAD})]
        whys = [why(r"BBF to first order: the average of local vol along the line from spot to strike is about its value "
                    r"at the midpoint"),
                why(r"differentiate in $K$ and in $S$: both pick up half the local slope"),
                why(r"at the money $K = S$ moves too: the two halves add, twice the implied skew; with a put skew, a rise "
                    r"in $S$ lowers every fixed strike's vol"),
                why(r"a forward-start option struck at the money in the future depends on tomorrow's smile, which no "
                    r"vanilla pins down"),
                why('in this calibration the simulated forward smiles flatten; this is not a universal local-volatility theorem')]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.8, buff=0.72, edge=6.9)
        with self.voiceover(
            "Here is why, in three lines. To first order, implied volatility at strike K is local volatility at the "
            "midpoint between spot and strike. <bookmark mark='a'/> Differentiate in the strike: half the local slope. "
            "Differentiate in the spot, holding the strike: also half the local slope. With a put skew that is "
            "negative, so a rise in the spot lowers the implied volatility of every fixed strike: the smile shifts "
            "against the move. <bookmark mark='b'/> At the money, strike and spot move together, the halves add, and "
            "the at-the-money volatility moves with the full local slope: twice the implied skew. The ratio is two. "
            "<bookmark mark='c'/> Which products care? A forward-start option pays on the ratio of two future prices: "
            "its value is a future smile, which no vanilla pins down. <bookmark mark='d'/> And local volatility's skew "
            "flattens with time, so its future smiles are flatter than today's."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
        self.wait(0.4)
        self.clear_scene()

    def fan(self, m):
        ks = np.asarray(m["ks"])
        fwd = m["fwd"]
        g = axes([-0.3, 0.3], [0.3, 0.65], x_length=6.8, y_length=4.2, xlabel=r"log-moneyness of a 30-day option",
                 ylabel=r"implied volatility", xticks=[-0.2, 0, 0.2], yticks=[0.4, 0.5, 0.6],
                 yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=16).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        today = curve_in(g.ax, ks, m["today30"], 0.3, 0.65, IV, stroke_width=4)
        starts = sorted(fwd, key=int)
        cols = [LV, QC.IDEA, OPT, SPOT, BAD]
        lines = VGroup(*[curve_in(g.ax, ks, fwd[s_], 0.3, 0.65, c, stroke_width=2.5)
                         for s_, c in zip(starts, cols)])
        leg = legend([(IV, r"today's 30-day smile (the Surface)")] + [(c, rf"local vol: starting in {s_} days")
                                                                        for s_, c in zip(starts, cols)],
                     font_size=16).next_to(g, RIGHT, buff=0.4).align_to(g, UP)
        sk = m["fwd_skew"]
        g2 = axes([0, 100], [0, 0.08], x_length=4.2, y_length=2.0, xlabel=r"start (days from now)",
                  ylabel=r"skew $\sigma(-0.1) - \sigma(0.1)$", xticks=[0, 30, 60, 90], yticks=[0, 0.04, 0.08],
                  yfmt=lambda u: f"{100 * u:.0f}", font_size=14).next_to(leg, DOWN, buff=0.45).align_to(leg, LEFT)
        pts = VGroup(*[Dot(g2.ax.c2p(int(s_), sk[s_]), radius=0.06, color=c) for s_, c in zip(starts, cols)])
        tline = DashedLine(g2.ax.c2p(0, m["today_skew"]), g2.ax.c2p(100, m["today_skew"]), color=IV)
        src = real_data(r"40{,}000 local-vol paths on the Surface; forward 30-day returns")
        s0, s90, st = 100 * sk[starts[0]], 100 * sk[starts[-1]], 100 * m["today_skew"]
        with self.voiceover(
            f"""Simulate forty thousand paths and price unit payoffs on the return ratio over each following thirty-day window. These ratio options omit the start-date spot multiplier in an asset-weighted forward-start payoff. <bookmark mark='a'/> Starting now, the skew between ninety and hundred-and-ten percent strikes is {s0:.1f} points, against {st:.1f} on the Surface. <bookmark mark='b'/> With starts fifteen through ninety days ahead, this model's skew fades to {s90:.1f}. That behavior depends on this calibration; it is not a universal local-volatility theorem or a forecast of future market smiles. Pause and predict: identical single-date marginals imply identical prices for a thirty-day ratio option starting in sixty days? No: the joint law matters. Part thirteen compares models."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(today), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(Create(lines[0]), FadeIn(leg[1]), FadeIn(g2), Create(tline), FadeIn(pts[0]))
            vo.wait_until("b")
            for i in range(1, len(lines)):
                self.play(Create(lines[i]), FadeIn(leg[i + 1]), FadeIn(pts[i]), run_time=1.0)
        self.wait(0.4)
        self.clear_scene()
