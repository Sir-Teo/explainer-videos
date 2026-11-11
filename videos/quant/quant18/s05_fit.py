from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import rates as R
from videos.quant.quant18.common import CURV, LEVEL, PART, SLOPE, ZERO, ask, house_lab, illustration, load

HUMP2 = QC.SPOT


class Fit(VoiceoverScene):
    def construct(self):
        cd = load("curve_day")
        self.card()
        self.loadings()
        self.sculpt()
        self.fits(cd)
        self.lab(cd["20251231"])

    def card(self):
        c = chapter_card(8, r"Fitting the curve: Nelson--Siegel and Svensson", r"Four loadings, two positive time scales",
                         part=PART)
        with self.voiceover("Chapter eight. Fitting the whole curve with a handful of numbers."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def loadings(self):
        rows = [cmath(r"y(t)", r"=", r"\beta_0 + \beta_1\,\frac{1 - e^{-t/\tau_1}}{t/\tau_1} + \beta_2\Big(\frac{1 - "
                      r"e^{-t/\tau_1}}{t/\tau_1} - e^{-t/\tau_1}\Big)", font_size=36, colors={r"y(t)": ZERO}),
                cmath(r"", r"+", r"\beta_3\Big(\frac{1 - e^{-t/\tau_2}}{t/\tau_2} - e^{-t/\tau_2}\Big)", font_size=36,
                      colors={r"+": HUMP2})]
        whys = [why(r"Nelson and Siegel (1987): a level, a slope that dies out with maturity, and a hump"),
                why(r"Svensson (1994): a second hump, for long maturities")]
        step = ladder(self, rows, whys, keep=2, top=3.1, x=-2.4, buff=0.5, edge=6.9, highlight=False)
        t = np.linspace(0.05, 30, 200)
        L = R.nss_loadings(t, 1.5, 12.0)
        g = axes([0, 30], [0, 1.05], x_length=8.0, y_length=2.6, xlabel=r"maturity, years", ylabel=r"loading",
                 xticks=[0, 5, 10, 20, 30], yticks=[0, 0.5, 1], font_size=14).to_edge(DOWN, buff=0.3).shift(LEFT * 1.0)
        ax = g.ax
        cols = [LEVEL, SLOPE, CURV, HUMP2]
        lines = VGroup(*[curve(ax, t, L[:, i], c_, stroke_width=3) for i, c_ in enumerate(cols)])
        leg = legend([(LEVEL, r"level: $\beta_0$, the long end"), (SLOPE, r"slope: $\beta_1$, short minus long"),
                      (CURV, r"curvature: $\beta_2$, peak at $1.79\tau_1$"), (HUMP2, r"second hump: $1.79\tau_2$")],
                     font_size=17).next_to(g, RIGHT, buff=0.3)
        with self.voiceover(
            "The earlier bootstrap is an interpolation and short-end approximation, not an exact fit to every market security. Nelson and Siegel proposed a low-dimensional smooth yield family. For positive time scales, <bookmark mark='a'/> beta zero is the long-maturity limit. <bookmark mark='b'/> The slope loading starts at one and decays, so beta zero plus beta one is the short-maturity limit. <bookmark mark='c'/> The hump vanishes at both ends and peaks at about one-point-seven-nine times its time scale, rather than exactly at tau. <bookmark mark='d'/> Svensson adds a second hump and time scale. Nelson-Siegel has four parameters in total; Svensson has six. Smoothness alone establishes neither a dynamic no-arbitrage model nor reliable forward-rate derivatives."
        ) as vo:
            step(0)
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(lines[0]), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(Create(lines[1]), FadeIn(leg[1]))
            vo.wait_until("c")
            self.play(Create(lines[2]), FadeIn(leg[2]))
            vo.wait_until("d")
            step(1)
            self.play(Create(lines[3]), FadeIn(leg[3]))
        self.wait(0.4)
        self.clear_scene()

    def sculpt(self):
        t = np.linspace(0.05, 30, 200)
        b0, b1, b2, b3 = (ValueTracker(v) for v in (4.0, 0.0, 0.0, 0.0))
        g = axes([0, 30], [0, 8], x_length=8.4, y_length=4.6, xlabel=r"maturity, years", ylabel=r"zero yield, \%",
                 xticks=[0, 5, 10, 20, 30], yticks=[0, 2, 4, 6, 8], font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        cv = always_redraw(lambda: curve(ax, t, R.nss(t, [b0.get_value(), b1.get_value(), b2.get_value(),
                                                             b3.get_value()], (1.5, 12.0)), ZERO,
                                         stroke_width=4))
        rd = always_redraw(lambda: VGroup(*[MathTex(rf"\beta_{i} = {v.get_value():+.2f}", font_size=30, color=c_)
                                             for i, (v, c_) in enumerate(zip((b0, b1, b2, b3),
                                                                             (LEVEL, SLOPE, CURV, HUMP2)))]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.8))
        cap = always_redraw(lambda: label(
            r"normal" if b1.get_value() < -0.5 and b2.get_value() > -0.1 else
            (r"inverted" if b1.get_value() > 0.5 else r"flat"), font_size=28, color=GREY_A).next_to(rd, UP, buff=0.4))
        with self.voiceover(
            "Here the two time scales are fixed at one-point-five and twelve years; only the four beta coefficients move. Start flat at four percent. <bookmark mark='a'/> A negative slope coefficient lowers the short end relative to the long end. <bookmark mark='b'/> Add a positive hump. <bookmark mark='c'/> A positive slope coefficient instead raises the short end above the long end. This is a schematic inversion, not a fit to a dated market curve. <bookmark mark='d'/> A negative hump makes a dip, and the second hump bends longer maturities. This restricted family approximates many observed shapes, but cannot represent every possible curve. The display retains the full calculated yields."
        ) as vo:
            self.play(FadeIn(g), FadeIn(rd), FadeIn(cap))
            self.add(cv)
            vo.wait_until("a")
            self.play(b1.animate.set_value(-3.0), run_time=2)
            vo.wait_until("b")
            self.play(b2.animate.set_value(2.0), run_time=2)
            vo.wait_until("c")
            self.play(b1.animate.set_value(1.5), b2.animate.set_value(0.0), run_time=2.5)
            vo.wait_until("d")
            self.play(b2.animate.set_value(-2.5), run_time=1.5)
            self.play(b3.animate.set_value(2.0), run_time=1.5)
        for m in (cv, rd, cap):
            m.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def fits(self, cd):
        panels = VGroup()
        texts = []
        for day, title in (("20251231", r"31 December 2025"), ("20230308", r"8 March 2023")):
            c = cd[day]
            s = np.asarray(c["s"])
            g = axes([0, 30], [2.5, 6], x_length=5.6, y_length=3.6, xlabel=r"maturity, years", ylabel=title,
                     xticks=[0, 10, 20, 30], yticks=[3, 4, 5, 6], font_size=13)
            ax = g.ax
            nodes = VGroup(*[Dot(ax.c2p(a, 100 * b), radius=0.05, color=ZERO) for a, b in zip(c["nodes_t"],
                                                                                            c["nodes_z"])])
            fit = curve(ax, s, np.asarray(c["nss"]["y"]) * 100, QC.DELTA, stroke_width=3)
            gsw = DashedVMobject(curve(ax, s, np.asarray(c["gsw"]) * 100, WHITE, stroke_width=2),
                                 num_dashes=50)
            tau = c["nss"]["tau"]
            txt = MathTex(rf"\text{{RMSE}} = {c['nss']['rmse_bp']:.1f}\ \text{{bp}},\ \ \tau = {tau[0]:.2f},\ "
                          rf"{tau[1]:.1f}", font_size=24, color=QC.DELTA).next_to(g, DOWN, buff=0.15)
            panels.add(VGroup(g, nodes, fit, gsw, txt))
            texts.append(c["nss"]["rmse_bp"])
        panels.arrange(RIGHT, buff=0.7).shift(DOWN * 0.3)
        leg = legend([(ZERO, r"bootstrapped zero rates"), (QC.DELTA, r"Svensson, fitted by the House"),
                      (WHITE, r"the Fed's Svensson curve (GSW)")], font_size=17).arrange(RIGHT, buff=0.4).to_edge(
            UP, buff=0.4)
        with self.voiceover(
            f"We fit six Svensson parameters by unweighted least squares to the House's derived zero-yield nodes, rather than directly to market bond prices. <bookmark mark='a'/> For December thirty-first, 2025, the root mean squared yield residual is {texts[0]:.1f} basis points. <bookmark mark='b'/> For March eighth, 2023, it is {texts[1]:.1f}. These are not average price errors. <bookmark mark='c'/> White dashes show the Fed staff's Gürkaynak-Sack-Wright curve. It uses off-the-run coupon Treasuries, excluding bills and the on-the-run and first-off-the-run issues. Its targets and conventions differ from our synthetic bootstrap. The historical file uses Nelson-Siegel before 1980 and Svensson thereafter. It is a revisable research estimate, not a record of curves available to traders in real time. All plotted samples are retained."
        ) as vo:
            self.play(FadeIn(leg), FadeIn(panels[0][0]), FadeIn(panels[0][1]), FadeIn(panels[1][0]),
                      FadeIn(panels[1][1]))
            vo.wait_until("a")
            self.play(Create(panels[0][2]), FadeIn(panels[0][4]))
            vo.wait_until("b")
            self.play(Create(panels[1][2]), FadeIn(panels[1][4]))
            vo.wait_until("c")
            self.play(Create(panels[0][3]), Create(panels[1][3]))
        self.add(illustration(r"GSW: Fed staff research; daily estimates, periodically updated and revisable"))
        self.wait(0.4)
        self.clear_scene()

    def lab(self, c):
        card = house_lab(r"fit Nelson--Siegel--Svensson", R.fit_nss, "for a, b in pairs:", 12, width=7.6)
        card.to_edge(LEFT, buff=0.4).to_edge(UP, buff=0.4)
        n = c["nss"]
        out = [rf"beta = {n['beta'][0]:.3f}, {n['beta'][1]:.3f}, {n['beta'][2]:.3f}, {n['beta'][3]:.3f}",
               rf"tau  = {n['tau'][0]:.3f}, {n['tau'][1]:.3f}",
               rf"rmse = {n['rmse_bp']:.2f} bp on {len(c['nodes_t'])} zero rates"]
        with self.voiceover(
            "Conditional on positive taus, the four beta coefficients solve a linear least-squares problem. The implementation searches a restricted grid of time-scale pairs, then uses the best pair to seed a joint local nonlinear refinement. <bookmark mark='a'/> Here is the December 2025 result. This procedure does not certify a global optimum, identify every parameter precisely, or supply confidence intervals. A small residual is a statement about the chosen zero-yield targets and loss function."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, out)
        q = ask(r"A smooth curve misses derived zero-yield nodes. Which targets, conventions and fitting objective should you check?")
        with self.voiceover('The smooth curve misses derived zero-yield nodes. Which targets, conventions and fitting objective should you check?'):
            self.play(FadeIn(q))
        self.wait(2.5)
        self.clear_scene()
        q.to_edge(UP, buff=0.6)
        answer = wrapped_label(r"Check instrument selection, coupon and compounding conventions, short-end approximation, interpolation and yield-versus-price weighting. A residual alone does not diagnose bad quotes.", 11.8, 26, QC.DELTA).move_to(ORIGIN)
        with self.voiceover("Check instrument selection, coupon and compounding conventions, the short-end approximation, interpolation and yield-versus-price weighting. A residual alone does not diagnose bad quotes."):
            self.play(FadeIn(q), FadeIn(answer))
        self.clear_scene()
