from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant12.common import BAD, IV, LV, OPT, PART, RV, SPOT, load, simulated


class Gamma(VoiceoverScene):
    def construct(self):
        g = load("gamma_toy")
        self.card()
        self.paths(g)
        self.derive()
        self.measure(g)
        self.record()

    def card(self):
        c = chapter_card(16, r"Dealer gamma and same-day options", r"Can hedging move the market?", part=PART)
        with self.voiceover("Chapter sixteen. Dealer gamma, and options that expire the same day."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def paths(self, g):
        e, lo, hi = (np.asarray(g[x]) for x in ("demo_eps", "demo_long", "demo_short"))
        n = len(e)
        m = np.arange(n)
        ax = axes([0, n], [-0.05, 0.05], x_length=8.4, y_length=4.2, xlabel=r"minutes of a trading day",
                  ylabel='cumulative minute return (linear toy)', xticks=[0, 360, 390], yticks=[-0.04, 0, 0.04],
                  yfmt=lambda u: f"{100 * u:+.0f}\\%", font_size=16).to_edge(LEFT, buff=0.5).shift(DOWN * 0.2)
        tr = ValueTracker(2)
        close = Rectangle(width=ax.ax.c2p(390, 0)[0] - ax.ax.c2p(360, 0)[0], height=ax.ax.c2p(0, 0.05)[1] - ax.ax.c2p(0, -0.05)[1],
                          stroke_width=0, fill_color=QC.HOUSE, fill_opacity=0.12).move_to(ax.ax.c2p(375, 0))
        cl = label(r"last 30 min", font_size=16, color=QC.HOUSE).next_to(close, UP, buff=0.05)

        def upto(y, col, sw=3):
            i = int(max(tr.get_value(), 2))
            return curve(ax.ax, m[:i], np.clip(y[:i], -0.05, 0.05), col, stroke_width=sw)
        ce = always_redraw(lambda: upto(e, GREY_C, 1.5))
        cl_ = always_redraw(lambda: upto(lo, RV))
        ch = always_redraw(lambda: upto(hi, BAD))
        leg = legend([(GREY_C, r"no dealers"), (RV, r"dealers long gamma ($k = +0.5$)"), (BAD, r"dealers short gamma ($k = -0.5$)")],
                     font_size=17).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        rd = lambda y: (lambda: float(np.std(np.diff(y[:int(max(tr.get_value(), 3))])) * np.sqrt(390) * 100))  # noqa: E731
        ro = VGroup(readout(r"\sigma_{\text{day}}^{\text{none}} =", rd(e), digits=2, font_size=26, color=GREY_B, unit=r"\%"),
                    readout(r"\sigma_{\text{day}}^{\text{long}} =", rd(lo), digits=2, font_size=26, color=RV, unit=r"\%"),
                    readout(r"\sigma_{\text{day}}^{\text{short}} =", rd(hi), digits=2, font_size=26, color=BAD, unit=r"\%")
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4).shift(UP * 0.5)
        src = simulated(r"simulated: the same minute shocks, three dealer positions; half the hedge left for the close")
        with self.voiceover(
            "Dealers hedge the options they sell, and the sign of their gamma decides which way the hedging pushes. "
            "One simulated day, three times over, with the same news each minute. Grey: no dealers. "
            "<bookmark mark='a'/> Green: dealers long gamma, selling rises and buying dips; the path is calmer. Red: "
            "dealers short gamma, because the public bought options from them; they chase every move, and the path "
            "swings wider. <bookmark mark='b'/> And in the "
            "last half hour, where the dealers finish the hedging they put off during the day, the short-gamma path "
            "keeps going in the direction it was already going."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(src), FadeIn(leg), FadeIn(close), FadeIn(cl), FadeIn(ro))
            self.add(ce, cl_, ch)
            vo.wait_until("a")
            self.play(tr.animate.set_value(360), run_time=10, rate_func=linear)
            vo.wait_until("b")
            self.play(tr.animate.set_value(n), run_time=3, rate_func=linear)
        for x in (ce, cl_, ch, *[r_.num for r_ in ro]):
            x.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"h", r"=", r"-\Gamma_d\,S\,\Delta S", font_size=40, colors={r"h": OPT}),
                cmath(r"\Delta S", r"=", r"\Delta S_0 + \lambda h\ \ \Rightarrow\ \ \Delta S = \frac{\Delta S_0}{1 + \lambda\Gamma_d S}",
                      font_size=38, colors={r"\Delta S": SPOT}),
                cmath(r"\Gamma_d > 0", r"\Rightarrow", r"\text{damped};\qquad \Gamma_d < 0 \Rightarrow \text{amplified, "
                      r"diverging as } \lambda|\Gamma_d|S \to 1", font_size=32),
                cmath(r"r_{\text{last 30}}", r"=", r"-c\,k\,r_{\text{rest of day}} + \varepsilon,\qquad k = \lambda\Gamma_d S",
                      font_size=36, colors={r"r_{\text{last 30}}": BAD}),
                cmath(r"\text{GEX}", r"=", r"\sum_i \Gamma_i\,S^2\,\text{OI}_i\,s_i", font_size=40, colors={r"\text{GEX}": LV})]
        whys = [why('h is dollar notional; shares traded are $-\\Gamma_d\\Delta S$, with position size in $\\Gamma_d$'),
                why('$\\lambda$ is price change per dollar traded; this row assumes the full hedge is immediate'),
                why(r"long gamma leans against moves; short gamma chases them"),
                why(r"if a share $c$ of the hedge waits for the close, the last half hour continues the day when $k < 0$: "
                    r"intraday momentum"),
                why('GEX per unit fractional move; contract gamma includes its multiplier; dealer signs require assumptions')]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.6, buff=0.72, edge=6.9)
        with self.voiceover(
            """Here is a linear feedback model. Gamma is the position's delta sensitivity per unit price move. The neutralizing share trade is minus Gamma times the price change; h is its dollar notional, so it also multiplies by S. <bookmark mark='a'/> Define lambda as price impact per dollar traded. If the whole hedge is immediate, solving the fixed point divides the external move by one plus lambda Gamma S. <bookmark mark='b'/> Long gamma damps; stable short-gamma feedback amplifies. The singularity is a limit of this linear toy, not a prediction of infinite real prices. <bookmark mark='c'/> The simulation defers half the hedge: its intraday denominator is one plus half k, and the closing return includes minus half k times the earlier return. <bookmark mark='d'/> GEX requires contract size and an assumed dealer side; open interest alone does not identify that side."""
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

    def measure(self, g):
        ks = np.asarray(g["k"])
        vol, sl = np.asarray(g["vol"]), np.asarray(g["slope"])
        g1 = axes([-0.6, 0.6], [0.5, 2.0], x_length=5.4, y_length=3.4, xlabel=r"dealer gamma $k = \lambda\Gamma_d S$",
                  ylabel='s.d. of pre-close return / no-dealer s.d.', xticks=[-0.5, 0, 0.5], yticks=[0.5, 1, 1.5, 2], font_size=15)
        g2 = axes([-0.6, 0.6], [-0.4, 0.4], x_length=5.4, y_length=3.4, xlabel=r"dealer gamma $k$",
                  ylabel=r"slope: last 30 min on the rest of the day", xticks=[-0.5, 0, 0.5], yticks=[-0.3, 0, 0.3],
                  font_size=15)
        VGroup(g1, g2).arrange(RIGHT, buff=1.0).to_edge(UP, buff=0.8)
        b1 = seed_band(g1.ax, ks, np.clip(vol, 0.5, 2.0), BAD)
        b2 = seed_band(g2.ax, ks, np.clip(sl, -0.4, 0.4), OPT)
        th = curve(g1.ax, ks, np.clip(1 / (1 + 0.5 * ks), 0.5, 2.0), GREY_B, stroke_width=2)
        thd = DashedVMobject(th, num_dashes=30)
        z = DashedLine(g2.ax.c2p(-0.6, 0), g2.ax.c2p(0.6, 0), color=GREY_C)
        foot = VGroup(
            label(rf"short gamma ($k = {g['k_short']:.1f}$): volatility $\times {g['vol_short']:.2f}$, closing slope "
                  rf"${g['slope_short']:+.2f}$", font_size=20, color=BAD),
            label(rf"long gamma ($k = {g['k_long']:+.1f}$): volatility $\times {g['vol_long']:.2f}$, closing slope "
                  rf"${g['slope_long']:+.2f}$", font_size=20, color=RV),
            label(r"dashed: the formula $1/(1 + (1 - c)k)$; bands: five seeds of 2{,}000 days", font_size=18, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.4)
        src = simulated(r"simulated", corner=UR)
        vs, vl, ss = g["vol_short"], g["vol_long"], g["slope_short"]
        with self.voiceover(
            f"""Sweep k over two thousand simulated days per value and five seeds. The bands show the full minimum-to-maximum range, not confidence intervals. <bookmark mark='a'/> The left panel measures the standard deviation across days of the return BEFORE the final half hour, relative to the no-dealer version. It is not each day's sum of squared minute returns. With half the hedge deferred, minus-one-half k gives {vs:.2f} times this standard deviation, and plus-one-half gives {vl:.2f}. <bookmark mark='b'/> The closing-on-earlier-return slope is {ss:+.2f} in the short case. These relations follow the specified simulation, rather than identifying causal dealer effects in observed markets."""
        ) as vo:
            self.play(FadeIn(g1), FadeIn(src), Create(thd))
            vo.wait_until("a")
            self.play(FadeIn(b1), FadeIn(foot[0]), FadeIn(foot[1]))
            vo.wait_until("b")
            self.play(FadeIn(g2), Create(z), FadeIn(b2), FadeIn(foot[2]))
        self.wait(0.4)
        self.clear_scene()

    def record(self):
        cards = VGroup(
            firm_card(r"Intraday momentum, measured",
                      r"Baltussen, Da, Lammers and Martens (2021, \emph{JFE}): across more than 60 futures markets since 1974, "
                      r"the last half hour's return is predicted by the rest of the day's; the effect is strongest when "
                      r"hedgers of index options and leveraged ETFs are short gamma.", width=6.4, font_size=20),
            firm_card(r"Same-day options",
                      'VIX1D launched 24 April 2023. Same-day options were 62.4\\% of SPX option volume in August 2025 (Cboe).', width=6.4, font_size=20),
            firm_card(r"Do they move the index? The evidence is mixed",
                      r"Andersen, Fusari and Todorov (2017) priced weekly options' short-term risks; Bandi, Fusari and "
                      r"Ren\`o (2023) price 0DTE options with jumps for the wings; Dim, Eraker and Vilkov (2024) find that "
                      r"high 0DTE open-interest gamma does not propagate past volatility.", width=6.4, font_size=20),
            firm_card(r"Who trades them",
                      r"Beckmeyer, Branger and Gayda (2023): retail traders lose on 0DTE options on average, mostly through "
                      r"spreads and fees; Bloomberg reported their estimate of about \$358{,}000 a day.", width=6.4,
                      font_size=20),
        )
        grid = VGroup(VGroup(cards[0], cards[1]).arrange(RIGHT, buff=0.3, aligned_edge=UP),
                      VGroup(cards[2], cards[3]).arrange(RIGHT, buff=0.3, aligned_edge=UP)).arrange(DOWN, buff=0.25)
        if grid.height > 7.3:
            grid.scale_to_fit_height(7.3)
        grid.move_to(ORIGIN)
        q = label(r"pause and predict: dealers short gamma at 6{,}000, spot 6{,}010, one hour to expiry", font_size=20,
                  color=QC.HOUSE).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            """The public record. Baltussen, Da, Lammers and Martens document intraday momentum across more than sixty futures markets, with evidence consistent with hedging feedback. <bookmark mark='a'/> Cboe reports that zero-day contracts were 62.4 percent of SPX option volume in August 2025, not all options tied to the S&P 500. <bookmark mark='b'/> Short-maturity pricing and feedback studies reach different conclusions under different position and flow measures; a large open-interest number by itself does not establish destabilizing dealer demand. <bookmark mark='c'/> Research also documents retail trading costs and losses in specific samples. Pause and predict: under our toy assumptions, short gamma amplifies local moves and long gamma damps them. Neither sign alone guarantees a pin at a particular listed strike in a real market."""
        ) as vo:
            self.play(FadeIn(cards[0]))
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
            vo.wait_until("c")
            self.play(FadeIn(cards[3]), FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
