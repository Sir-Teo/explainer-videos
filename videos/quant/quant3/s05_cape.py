from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant3.common import CASH, PART, PRICE, VALUE, live, load, real_data

C_ = {r"P": PRICE, r"E_1": VALUE, r"b": CASH, r"r": QC.IMPLIED, r"g": CASH}


class CAPE(VoiceoverScene):
    def construct(self):
        c = load("cape")
        cs = load("campbell_shiller")
        self.card()
        self.multiples()
        self.series(c)
        self.scatter(c)
        self.cs_derive(cs)
        self.tug(cs)

    def card(self):
        c = chapter_card(9, r"Multiples, the CAPE, and the dividend yield", r"Is the market expensive, and what "
                         r"does that predict?", part=PART)
        with self.voiceover("Chapter nine. Multiples, the CAPE, and what the dividend yield predicts."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def multiples(self):
        rows = [cmath(r"P", r"=", r"\frac{D_1}{r - g}", r"=", r"\frac{b\,E_1}{r - g}", colors=C_, font_size=42),
                cmath(r"\frac{P}{E_1}", r"=", r"\frac{b}{r - g}", colors=C_, font_size=46),
                cmath(r"P", r"=", r"\frac{E_1}{r}", r"+", r"\text{PVGO}", colors=C_, font_size=42)]
        whys = [why(r"Gordon, with dividends a fraction $b$ of earnings: the payout ratio"),
                why(r"a P/E is a compressed DCF: a high multiple means low $r$ or high $g$"),
                why(r"the value of today's earnings as a perpetuity, plus the present value of growth opportunities")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-2.6, buff=0.7, edge=6.9)
        ev = VGroup(
            MathTex(r"\frac{\text{EV}}{\text{EBITDA}}", font_size=40),
            wrapped_label(r"enterprise value (equity plus debt minus cash) over earnings before interest, tax, "
                          r"depreciation and amortisation: compares firms however they are financed", 7.4, 23, GREY_A),
        ).arrange(RIGHT, buff=0.4).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "Analysts rarely run a full DCF; they use multiples, which are DCFs folded up. Write the dividend as a payout ratio "
            "b times earnings. <bookmark mark='a'/> Divide by earnings: the P/E is b over r minus g, a bet on low rates or high "
            "growth. <bookmark mark='b'/> Or split the price into today's earnings as a perpetuity, plus the present value of "
            "growth opportunities. <bookmark mark='c'/> And to compare firms with different debt, desks use enterprise value "
            "over EBITDA."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(FadeIn(ev))
        self.wait(0.4)
        self.clear_scene()

    def series(self, c):
        t, v = np.asarray(c["cape_series_t"]), np.asarray(c["cape_series"])
        g = axes([1880, 2021], [0, 46], x_length=10.6, y_length=4.6, ylabel=r"CAPE: real price over ten years of real "
                 r"earnings", xticks=[1900, 1930, 1960, 1990, 2020], yticks=[0, 10, 20, 30, 40],
                 xfmt=lambda x: f"{int(x)}", font_size=18).move_to(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, t, v, PRICE, stroke_width=2.5)
        mean = DashedLine(ax.c2p(1880, c["mean_cape"]), ax.c2p(2021, c["mean_cape"]), color=GREY_B, stroke_width=2)
        mlab = label(rf"average {c['mean_cape']:.0f}", font_size=20, color=GREY_B).next_to(mean, RIGHT, buff=0.1)
        marks = VGroup()
        for when, val, txt in [(1929.67, 32.6, r"Sept.\ 1929: 32.6"), (1920.92, 4.8, r"Dec.\ 1920: 4.8"),
                               (1982.5, 6.6, r"1982: 6.6"), (1999.92, 44.2, r"Dec.\ 1999: 44.2"),
                               (2020.92, c["cape_now"], rf"Dec.\ 2020: {c['cape_now']:.1f}")]:
            d = Dot(ax.c2p(when, val), radius=0.06, color=YELLOW)
            lab = label(txt, font_size=19, color=YELLOW).next_to(d, UP if val > 20 else DOWN, buff=0.1)
            marks.add(VGroup(d, lab))
        marks[4][1].next_to(marks[4][0], LEFT, buff=0.1).shift(UP * 0.15)
        src = real_data(r"Shiller's data; CAPE from Campbell and Shiller (1988, 1998)")
        with self.voiceover(
            "One year of earnings is noisy, so in 1988 Campbell and Shiller divided the real price by ten years of average real "
            "earnings: the cyclically adjusted P/E, or CAPE, here since 1881. <bookmark mark='a'/> Its average is about "
            f"{c['mean_cape']:.0f}; it reached forty-four in December 1999 and fell below seven in 1982. "
            "<bookmark mark='b'/> At the end of 2020, where our research window closes, it stood near thirty-four."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src))
            self.play(Create(line), run_time=3)
            vo.wait_until("a")
            self.play(Create(mean), FadeIn(mlab))
            self.play(LaggedStart(*[FadeIn(m) for m in marks[:4]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(marks[4]))
        self.wait(0.4)
        self.clear_scene()

    def scatter(self, c):
        x, y, t = np.log(np.asarray(c["cape"])), np.asarray(c["fwd"]), np.asarray(c["t"])
        g = axes([np.log(4), np.log(50)], [-0.08, 0.22], x_length=6.4, y_length=5.0,
                 xlabel=r"CAPE at the start (log scale)", ylabel=r"real return a year over the next ten years",
                 xticks=list(np.log([5, 10, 20, 40])), xfmt=lambda u: f"{np.exp(u):.0f}",
                 yticks=[-0.05, 0, 0.05, 0.10, 0.15, 0.20], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=18)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        cols = color_gradient([QC.SPOT, QC.IDEA], 8)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.022, color=cols[min(int((tt - 1881) / 130 * 8), 7)],
                            fill_opacity=0.7) for a, b, tt in zip(x, y, t)])
        xs = np.linspace(np.log(4.5), np.log(48), 50)
        fit = curve(ax, xs, c["intercept"] + c["slope"] * xs, WHITE, stroke_width=3)
        now = np.log(c["cape_now"])
        vline = DashedLine(ax.c2p(now, -0.08), ax.c2p(now, 0.22), color=QC.HOUSE, stroke_width=2)
        pred = Dot(ax.c2p(now, c["pred_now"]), radius=0.1, color=QC.HOUSE)
        side = VGroup(
            label(r"each dot: a month from 1881 to 2010, and the", font_size=21, color=GREY_A),
            label(r"real total return over the following ten years", font_size=21, color=GREY_A),
            MathTex(rf"R^2 = {c['r2']:.2f}", font_size=36),
            label(rf"{c['n']:,} starting months, but only about {c['n_indep']} independent decades".replace(",", "{,}"),
                  font_size=21, color=QC.LOSS),
            MathTex(rf"\text{{Dec.\ 2020: CAPE }} {c['cape_now']:.1f} \Rightarrow {100 * c['pred_now']:.1f}\%"
                    r"\text{ a year}", font_size=30, color=QC.HOUSE),
            label(r"sealed: the envelope opens on 2021--2030 in the finale", font_size=21, color=QC.HOUSE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.35)
        leg = VGroup(Dot(radius=0.05, color=cols[0]), label(r"1880s", font_size=17, color=GREY_B),
                     Dot(radius=0.05, color=cols[-1]), label(r"2000s", font_size=17, color=GREY_B)).arrange(RIGHT, buff=0.1)
        leg.next_to(g, UP, buff=0.05).align_to(g, RIGHT)
        with self.voiceover(
            "Does the CAPE tell you anything? Plot each month's CAPE against the real return of the next ten years. "
            "<bookmark mark='a'/> The cloud slopes down: high valuations have been followed by low decades, and low ones by high "
            "decades. The fit explains about a third of the variation. <bookmark mark='b'/> But be careful with the count. There are "
            "over fifteen hundred dots, and each shares nine years and eleven months of its future with its neighbour. There are "
            "only about thirteen independent decades here, and the slope is far less certain than it looks. Part six makes that "
            "precise. <bookmark mark='c'/> Read off the line at the end of 2020: a CAPE near thirty-four predicted a real return of "
            "about half a percent a year for the 2020s. That forecast goes into the sealed envelope, to be opened in the finale."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(side[:2]))
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.002, run_time=3))
            vo.wait_until("a")
            self.play(Create(fit), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(FadeIn(side[3]))
            vo.wait_until("c")
            self.play(Create(vline), FadeIn(pred), FadeIn(side[4]))
            self.play(FadeIn(side[5]))
        self.wait(0.4)
        self.clear_scene()

    def cs_derive(self, cs):
        F = cs["full"]
        rows = [
            cmath(r"r_{t+1}", r"\approx", r"\kappa + \rho\, pd_{t+1} + \Delta d_{t+1} - pd_t", font_size=40),
            cmath(r"pd_t", r"\approx", r"\text{const} + \sum_{j \ge 1} \rho^{j-1}\big(\Delta d_{t+j} - r_{t+j}\big)",
                  font_size=40),
            cmath(r"1", r"\approx", r"\frac{\text{cov}(dp_t, \sum \rho^{j-1} r_{t+j})}{\text{var}(dp_t)} - "
                  r"\frac{\text{cov}(dp_t, \sum \rho^{j-1}\Delta d_{t+j})}{\text{var}(dp_t)}", font_size=36),
            cmath(r"b_r^{lr} - b_d^{lr}", r"=", r"1,\qquad b^{lr} = \frac{b}{1 - \rho\phi}", font_size=40),
            cmath(rf"{F['lr_r']:.2f} - ({F['lr_d']:.2f})", r"=", rf"{F['lr_r'] - F['lr_d']:.2f}", font_size=40),
        ]
        whys = [why(r"log return $= \ln\big((P_{t+1} + D_{t+1})/P_t\big)$, Taylor-expanded in $pd = \ln(P/D)$ around its "
                    r"mean; $\rho = 1/(1 + e^{\overline{dp}})$"),
                why(r"iterate forward and rule out bubbles: Campbell and Shiller (1988)"),
                why(r"multiply by $dp_t = -pd_t$ and take covariances: a high yield must be followed by high returns "
                    r"or low dividend growth"),
                why(r"with $dp$ an AR(1) with persistence $\phi$, the long-run slopes are the one-year slopes "
                    r"over $1 - \rho\phi$ (Cochrane 2008)"),
                why(rf"Shiller's annual data, {cs['years'][0]}--{cs['years'][1]}, real; identity gap "
                    rf"{F['identity_gap']:+.3f} from the linearisation")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Why should a valuation ratio predict anything? Campbell and Shiller showed in 1988 that it must. Expand the log "
            "return to first order in the price-dividend ratio. <bookmark mark='a'/> Solve forward, ruling out bubbles: today's "
            "ratio is discounted future dividend growth minus future returns. <bookmark mark='b'/> Take covariances with the "
            "dividend yield: a high yield must be paid for by high returns or low dividend growth. <bookmark mark='c'/> Cochrane's "
            "2008 version: the long-run return slope minus the long-run dividend slope is one. <bookmark mark='d'/> On Shiller's "
            f"data: {F['lr_r']:.2f} for returns, {F['lr_d']:.2f} for dividends, up to the linearisation."
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

    def tug(self, cs):
        S = [("1871--2020", cs["full"]), ("1871--1945", cs["subs"]["1871-1945"]),
             ("1946--2020", cs["subs"]["1946-2020"])]
        k = ValueTracker(0)
        W = 10.0

        def shares(i):
            s = S[i][1]
            a, b = max(s["lr_r"], 0.0), max(-s["lr_d"], 0.0)
            tot = a + b if a + b > 0 else 1.0
            return a / tot, s["lr_r"], s["lr_d"]

        def rope():
            x = k.get_value()
            i0 = int(np.clip(np.floor(x), 0, len(S) - 1))
            i1 = min(i0 + 1, len(S) - 1)
            f = x - i0
            a0, r0, d0 = shares(i0)
            a1, r1, d1 = shares(i1)
            a = (1 - f) * a0 + f * a1
            rr, dd = (1 - f) * r0 + f * r1, (1 - f) * d0 + f * d1
            y = 0.2
            left = Line([-W / 2, y, 0], [-W / 2 + a * W, y, 0], color=QC.LOSS, stroke_width=16)
            right = Line([-W / 2 + a * W, y, 0], [W / 2, y, 0], color=QC.GAIN, stroke_width=16)
            knot = Dot([-W / 2 + a * W, y, 0], radius=0.18, color=WHITE)
            lt = live(r"\text{returns}\ b_r^{lr} =", rr, 2, font_size=32, color=QC.LOSS)
            lt.next_to([-W / 2, y, 0], UP, buff=0.3).align_to(left, LEFT)
            rt = live(r"\text{dividend growth}\ b_d^{lr} =", dd, 2, font_size=32, color=QC.GAIN)
            rt.next_to([W / 2, y, 0], UP, buff=0.3).align_to(right, RIGHT)
            per = label(S[int(round(x))][0], font_size=34, color=QC.IDEA).move_to(UP * 2.6)
            return VGroup(left, right, knot, lt, rt, per)

        rp = always_redraw(rope)
        cap = wrapped_label(r"who pays for a high dividend yield: later returns (red) or later dividend growth (green); "
                            r"their long-run slopes always differ by one", 11.0, 22, GREY_A).to_edge(DOWN, buff=1.6)
        sims = np.asarray(cs["boot_slopes"])
        F = cs["full"]
        boot = VGroup(
            MathTex(rf"\text{{one-year slope of returns on }} dp:\ {F['b_r']:.3f},\ t_{{NW}} = {cs['t_r']:.2f}",
                    font_size=28),
            MathTex(rf"\text{{Stambaugh bootstrap, no predictability: }} P(\hat b \ge {F['b_r']:.3f}) = "
                    rf"{cs['boot_p']:.2f};\ \text{{mean slope under the null}}\ {cs['boot_mean']:.3f}", font_size=26,
                    color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        s1, s2 = S[1][1], S[2][1]
        with self.voiceover(
            "As a tug of war: a rope of length one, red for future returns, green for dividend growth, and the knot where a high "
            f"yield is paid for. <bookmark mark='a'/> Over the whole sample, returns pull {F['lr_r']:.2f}. "
            f"<bookmark mark='b'/> Before 1946, dividends did most of the work, {s1['lr_d']:.2f}. <bookmark mark='c'/> After "
            f"1945 the green rope goes slack, {s2['lr_d']:.2f}, and returns carry everything: Cochrane's dog that did not bark. "
            "<bookmark mark='d'/> But the one-year slope is weak, and biased up by a persistent predictor. In a world with no "
            f"predictability, slopes this large appear {100 * cs['boot_p']:.0f} percent of the time."
            " So far the firm's financing has been taken as given. Next: does it matter at all?"
        ) as vo:
            self.add(rp)
            self.play(FadeIn(cap))
            vo.wait_until("a")
            self.wait(0.5)
            vo.wait_until("b")
            self.play(k.animate.set_value(1), run_time=3)
            vo.wait_until("c")
            self.play(k.animate.set_value(2), run_time=3)
            vo.wait_until("d")
            self.play(FadeOut(cap), FadeIn(boot))
        rp.clear_updaters()
        self.wait(0.4)
        self.clear_scene()
