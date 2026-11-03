from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import bs
from videos.quant.quant11.common import (ALT, GAMMA, OPT, PART, SPOT, THETA, VEGA, axes3d, fixed, hint3d, illustration,
                                         load, pause, real_data, surf)


class Expiry(VoiceoverScene, ThreeDScene):
    def construct(self):
        self.card()
        self.spike()
        self.pin()
        self.derive()
        self.pinning(load("pin_sim"))
        self.btc(load("pin_btc"))

    def card(self):
        c = chapter_card(11, r"Expiry and pin risk", r"What happens in the last hour?", part=PART)
        with self.voiceover("Chapter eleven. Expiry, and pin risk."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def spike(self):
        ax = axes3d([96, 104, 2], [0, 24, 6], [0, 2.5, 0.5], x_length=7.4, y_length=5.0, z_length=3.2)

        def gam(S, h):
            return float(min(bs.greeks(S, 100.0, max(h, 0.25) / (365 * 24), 0.5)["gamma"], 2.5))
        sf = surf(ax, gam, (96, 104), (0.25, 24), [(QC.SPOT, 0.05), (GAMMA, 0.8), (QC.LOSS, 2.3)], resolution=(28, 20),
                  opacity=0.8)
        hint = hint3d((r"underlying near the strike of 100", SPOT), (r"hours to expiry", THETA),
                      (r"gamma of one call (clipped at 2.5)", GAMMA))
        gd = float(bs.greeks(100.0, 100.0, 1 / 365, 0.5)["gamma"])
        gh = float(bs.greeks(100.0, 100.0, 1 / (365 * 24), 0.5)["gamma"])
        gm = float(bs.greeks(100.0, 100.0, 1 / (365 * 24 * 60), 0.5)["gamma"])
        cap = VGroup(MathTex(r"\Gamma_{\text{ATM}} \approx \frac{1}{S\,\sigma\sqrt{2\pi\,\tau}}", font_size=32, color=GAMMA),
                     MathTex(rf"\text{{a day: }} {gd:.2f},\ \text{{an hour: }} {gh:.2f},\ \text{{a minute: }} {gm:.1f}",
                             font_size=26)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DL, buff=0.35)
        self.set_camera_orientation(phi=64 * DEGREES, theta=-48 * DEGREES, zoom=0.9)
        fixed(self, hint, cap)
        with self.voiceover(
            "Options are most dangerous at the end. Here is gamma over the last day, near the strike: a ridge that "
            "becomes a spike as expiry approaches. <bookmark mark='a'/> At the strike it grows like one over the "
            f"square root of the time left. At fifty percent volatility it is {gd:.2f} a day before expiry, "
            f"{gh:.2f} an hour before, and {gm:.1f} a minute before. Away from the strike it collapses to nothing."
        ) as vo:
            self.play(Create(ax), FadeIn(hint), run_time=1.2)
            self.play(Create(sf), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(cap))
            self.move_camera(theta=-15 * DEGREES, phi=72 * DEGREES, run_time=max(vo.remaining(1.0) - 0.3, 1.0))
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, added_anims=[FadeOut(VGroup(ax, sf)), FadeOut(hint),
                                                                             FadeOut(cap)], run_time=1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pin(self):
        S = np.linspace(96, 104, 161)
        g = axes([96, 104], [0, 1], x_length=6.2, y_length=3.8, xlabel=r"underlying near the strike of 100",
                 ylabel=r"call delta", xticks=[96, 98, 100, 102, 104], yticks=[0, 0.5, 1], font_size=17)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        cols = [ALT, VEGA, THETA]
        labs = [r"a day left", r"an hour left", r"a minute left"]
        taus = [1 / 365, 1 / (365 * 24), 1 / (365 * 24 * 60)]
        lines = VGroup(*[curve(ax, S, bs.greeks(S, 100.0, tau, 0.5)["delta"], c, stroke_width=3) for tau, c in zip(taus, cols)])
        leg = legend(list(zip(cols, labs)), font_size=19).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        side = VGroup(
            wrapped_label(r"delta becomes a step: a tiny move across the strike flips it from 0 to 1, and a hedger "
                          r"trades its whole position back and forth", 4.4, 20, GREY_A),
            wrapped_label(r"pin risk: short an option struck where the stock closes, you do not know until the next "
                          r"day whether you will be assigned, so you hold a full unit of delta of unknown sign "
                          r"overnight (Taleb)", 4.4, 20, THETA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Gamma is how fast delta moves, so delta becomes a step. With a day left, it rises smoothly across the "
            "strike; with a minute left, a tiny move flips it from zero to one, and a hedger must trade its whole "
            "position back and forth on noise. <bookmark mark='a'/> Pin risk is the related problem for a seller. "
            "If the stock closes right at the strike of an option you are short, you will not know until the next "
            "morning whether you are assigned: a full unit of delta, of unknown sign, over the weekend."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.5), run_time=3)
            self.play(FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        rows = [
            cmath(r"\Gamma_{\text{ATM}}", r"=", r"\frac{\varphi(d_1)}{S\sigma\sqrt\tau} \to \frac{1}{S\sigma\sqrt{2\pi\tau}}",
                  font_size=36, colors={r"\Gamma_{\text{ATM}}": GAMMA}),
            cmath(r"\text{hedgers' flow}", r"=", r"-\Gamma_{\text{net}}\,dS", font_size=36),
            cmath(r"dS", r"=", r"\sigma S\,dW - \kappa\,\Gamma_{\text{net}}\,dS", font_size=36),
            cmath(r"\sigma_{\text{eff}}", r"=", r"\frac{\sigma}{1 + \kappa\,\Gamma_{\text{net}}(S, \tau)}", font_size=38,
                  colors={r"\sigma_{\text{eff}}": VEGA}),
        ]
        whys = [why(r"chapter 1's formula at the money, where $d_1 \to 0$ and $\varphi(0) = 1/\sqrt{2\pi}$"),
                why(r"a book net long gamma re-hedges by selling into rises and buying into falls"),
                why(r"with linear price impact $\kappa$, that flow pushes back on every move"),
                why(r"Avellaneda and Lipkin (2003): solve for $dS$; near the strike, close to expiry, volatility is "
                    r"damped toward zero, and the price is pinned. Net short gamma, the sign flips: hedgers chase")]
        step = ladder(self, rows, whys, keep=4, top=3.0, x=-0.4, buff=0.55, edge=6.9)
        pc = pause(r"Market makers are net short gamma at a strike into expiry. Pin, or repel?", width=5.0, font_size=21, corner=UR)  # the top row makes way for it
        with self.voiceover(
            "Can hedging move the price itself? First, gamma at the money: chapter one's formula with d one at zero. "
            "<bookmark mark='a'/> A book that is net long gamma re-hedges against every move: it sells when the "
            "price rises and buys when it falls. <bookmark mark='b'/> If its trades move the price, with a linear "
            "impact kappa, that flow pushes back on the move. <bookmark mark='c'/> Solve for the price change: "
            "volatility is divided by one plus kappa times the hedgers' gamma. Marco Avellaneda and Michael Lipkin's "
            "insight: near the strike and close to expiry, gamma explodes, so the effective volatility collapses, "
            "and the price is pinned. <bookmark mark='d'/> Pause and predict: if the hedgers are net short gamma "
            "instead, pin, or repel?"
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            self.play(FadeOut(rows[0]), FadeOut(whys[0]), FadeIn(pc))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pinning(self, p):
        t = np.asarray(p["t"])
        panels = VGroup()
        objs = []
        for name, title, col in (("long", r"hedgers net long gamma at 100", GAMMA),
                                 ("short", r"hedgers net short gamma at 100", THETA)):
            g = axes([0, 48], [94, 106], x_length=4.6, y_length=3.4, xlabel=r"hours", ylabel=title,
                     xticks=[0, 24, 48], yticks=[95, 100, 105], font_size=15)
            panels.add(g)
            objs.append((g, name, col))
        panels.arrange(RIGHT, buff=1.8).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        fans, hists = VGroup(), VGroup()
        for g, name, col in objs:
            P = np.clip(np.asarray(p[name]["paths"]), 94, 106)
            fans.add(path_fan(g.ax, t, P, color=col, opacity=0.35, max_paths=60))
            hists.add(side_density(g.ax, np.asarray(p[name]["terminal"]), (94, 106), bins=48, width=1.1, color=col))
        side = VGroup(
            label(rf"ending within 0.5 of the strike:", font_size=20, color=GREY_A),
            label(rf"no hedgers {100 * p['none']['near']:.0f}\%", font_size=20, color=GREY_B),
            label(rf"net long {100 * p['long']['near']:.0f}\%", font_size=20, color=GAMMA),
            label(rf"net short {100 * p['short']['near']:.1f}\%", font_size=20, color=THETA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UR, buff=0.4)
        src = illustration(r"simulated: 2{,}000 paths over the last two days, 50\% vol; the House's \texttt{pin\_simulation}")
        with self.voiceover(
            "Simulate it. Two thousand paths over an option's last two days, with hedgers net long gamma at a strike "
            "of a hundred, and their trades moving the price. <bookmark mark='a'/> The paths fan out, then are drawn "
            "in toward the strike as expiry nears, and the histogram of where they end grows a spike at a hundred: "
            f"{100 * p['long']['near']:.0f} percent end within half a point of it, against "
            f"{100 * p['none']['near']:.0f} percent with no hedgers. <bookmark mark='b'/> Flip the sign. Hedgers net "
            "short gamma buy into rises and sell into falls, and the strike repels: a hole where the spike was, "
            f"{100 * p['short']['near']:.1f} percent. That is the answer to the question: short gamma repels."
        ) as vo:
            self.play(FadeIn(panels[0]), FadeIn(src), FadeIn(side[0]), FadeIn(side[1]))
            self.play(Create(fans[0]), run_time=max(vo.until("a") - 0.2, 1.5), lag_ratio=0.02)
            self.play(FadeIn(hists[0]), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(FadeIn(panels[1]), Create(fans[1], lag_ratio=0.02), run_time=2.5)
            self.play(FadeIn(hists[1]), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def btc(self, b):
        G = b["groups"]
        card = theorem_card(r"Ni, Pearson and Poteshman (2005)", r"US stocks with listed options close near a strike "
                            r"price more often on expiration Fridays than on other days, most of all where option market "
                            r"makers' re-hedging should pin them: pinning, in the data.", who=r"\textit{Stock price clustering on option "
                            r"expiration dates}, JFE", color=QC.IDEA, width=6.0, font_size=20).to_corner(UL, buff=0.35)
        g = axes([0, 0.5], [0, 0.3], x_length=5.6, y_length=3.0, xlabel=r"distance from the nearest \$1{,}000 strike "
                 r"(share of the spacing)", ylabel=r"share of hours", xticks=[0, 0.1, 0.25, 0.5], yticks=[0, 0.1, 0.2],
                 font_size=15).to_corner(DL, buff=0.5)
        ax = g.ax

        def hist(h, col, off, op):
            gr = VGroup()
            for j, v in enumerate(h):
                a, c = ax.c2p(j * 0.05 + off, 0), ax.c2p(j * 0.05 + off + 0.022, min(v, 0.3))
                gr.add(Rectangle(width=c[0] - a[0], height=max(c[1] - a[1], 0.005), stroke_width=0, fill_color=col,
                                 fill_opacity=op).move_to((a + c) / 2))
            return gr
        h_all = hist(G["all hours"]["hist"], GREY_B, 0.002, 0.7)
        h_fri = hist(G["Fridays 08:00"]["hist"], YELLOW, 0.025, 0.85)
        leg = legend([(GREY_B, r"all hours"), (YELLOW, r"Fridays, 08:00 UTC (expiry)")], font_size=16).next_to(
            g, UP, buff=0.05).align_to(g, RIGHT)
        f8, f7, mo, al = G["Fridays 08:00"], G["Fridays 07:00"], G["monthly expiries"], G["all hours"]
        side = VGroup(
            label(r"within \$100 of a \$1{,}000 strike:", font_size=21, color=GREY_A),
            label(rf"all hours: {100 * al['share']:.1f}\%", font_size=21, color=GREY_B),
            label(rf"Friday expiries: {100 * f8['share']:.1f}\% (n = {f8['n']}), $z = {f8['z']:.1f}$", font_size=21,
                  color=YELLOW),
            label(rf"monthly expiries: {100 * mo['share']:.1f}\% (n = {mo['n']})", font_size=21, color=ALT),
            label(rf"control, an hour before: {100 * f7['share']:.1f}\%", font_size=21, color=GREY_B),
            wrapped_label(r"Deribit settles at 08:00 UTC on a 30-minute average of its index; Binance's 08:00 hourly "
                          r"close stands in for it here", 5.4, 18, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.3)
        src = real_data(rf"Binance BTCUSDT hourly, {b['first']} to {b['last']}")
        strong = f8["z"] > 2.5
        verdict = (f"With a z of {f8['z']:.1f} on {f8['n']} Fridays, that is suggestive, not conclusive: the honest "
                   "test would use the thirty-minute average itself." if not strong else
                   f"With a z of {f8['z']:.1f}, that is strong evidence of pinning.")
        with self.voiceover(
            "Does it happen? Xiaoyan Ni, Neil Pearson and Allen Poteshman found in 2005 that American stocks with "
            "listed options close near a strike more often on expiration Fridays, most of all where market makers' "
            "re-hedging should pin them. Joseph Golez and Jens Jackwerth found the same in S&P 500 futures. <bookmark mark='a'/> Try it "
            "on Bitcoin. Deribit's options expire on Fridays at eight in the morning, UTC, settled on a thirty-minute "
            "average of its index, and its strikes sit every thousand dollars. Measure how far Bitcoin is from the "
            "nearest thousand at every hour of five years, and at the Friday expiries. <bookmark mark='b'/> At all "
            f"hours, {100 * al['share']:.1f} percent of closes fall within a hundred dollars of a strike, as chance "
            f"predicts. At the Friday expiries, {100 * f8['share']:.1f} percent; at the monthly expiries "
            f"{100 * mo['share']:.1f}; an hour before expiry, {100 * f7['share']:.1f}, no different from chance. "
            f"{verdict}"
            " Some options never reach expiry. Next: early exercise, and the money it leaves behind."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(g), FadeIn(src), FadeIn(h_all), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(FadeIn(h_fri), FadeIn(leg[1]))
            self.play(LaggedStart(*[FadeIn(s_) for s_ in side], lag_ratio=0.3, run_time=3))
        self.wait(0.4)
        self.clear_scene()
