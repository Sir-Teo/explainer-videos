from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import rates as R
from videos.quant.quant18.common import FWD, PAR, PART, ZERO, ask, house_lab, illustration, load, sci


class Bootstrap(VoiceoverScene):
    def construct(self):
        cd = load("curve_day")
        self.card()
        self.ladder_()
        self.build(cd["20251231"])
        self.lab(cd["20251231"])
        self.inverted(cd["20230308"])

    def card(self):
        c = chapter_card(5, r"Bootstrapping a curve", r"How do you get zero rates from bond prices?", part=PART)
        with self.voiceover('Chapter five. An illustrative bootstrap from published par-curve points.'):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def ladder_(self):
        rows = [cmath(r"Z_{\rm model}(t)", r"=", r"\big(1 + \tfrac{y_t}{2}\big)^{-2t},\quad t \le 1", font_size=40,
                      colors={r"Z(t)": ZERO}),
                cmath(r"100", r"=", r"\tfrac{c_T}{2}\sum_{t_i < T} Z(t_i;Z(T)) + \big(100 + \tfrac{c_T}{2}\big) Z(T)",
                      font_size=40, colors={r"100": PAR}),
                cmath(r"z(t)\,t", r"\ \text{linear between nodes}", r"\Leftrightarrow\ f\ \text{flat between nodes}",
                      font_size=38, colors={r"z(t)\,t": ZERO}),
                cmath(r"Z(T)", r"=", r"\text{the one unknown: solve, then move to the next } T", font_size=38,
                      colors={r"Z(T)": ZERO})]
        whys = [why(r"a simplifying short-node conversion of published CMT par yields; these are not observed zero prices, and the one-year par bond is not repriced exactly"),
                why(r"a synthetic par bond with annual coupon cash amount $c_T$ per 100 face. Coupons in the new interval depend on its unknown endpoint through the interpolation rule"),
                why(r"between nodes, interpolate: the simplest rule keeps the forward rate constant"),
                why(r"each longer coupon node adds one scalar unknown. A valid root bracket and consistent cash-flow conventions are needed; the tiny saved residual covers only $T>1$ year")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.6, buff=0.55, edge=6.9)
        with self.voiceover(
            "Treasury publishes constant-maturity par-curve points derived from its own fitted curve. Our example builds a different simplified curve from those rounded points. At maturities up to one year it assumes the displayed semiannual-equivalent conversion to a single-payment discount factor. This is a modelling convention, not an exact reconstruction of Treasury bill prices. <bookmark mark='a'/> Beyond one year use a synthetic semiannual coupon bond priced at a hundred. For a two-year bond, the one-and-a-half-year coupon lies in the new interpolation interval and depends on the unknown two-year endpoint too. <bookmark mark='b'/> Linear interpolation of log discount factors fills such gaps, giving constant forwards away from nodes. <bookmark mark='c'/> The whole new interval is still controlled by one scalar endpoint, so a bracketed root solve can reprice the longer coupon bond. This does not establish that every published short point is an exactly repriced par instrument."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def build(self, c):
        T, y = np.asarray(c["tenor"]), np.asarray(c["par"]) * 100
        nt, nz = np.asarray(c["nodes_t"]), np.asarray(c["nodes_z"]) * 100
        g = axes([0, 30], [3, 5.5], x_length=9.0, y_length=4.6, xlabel=r"maturity, years", ylabel=r"percent",
                 xticks=[0, 2, 5, 10, 20, 30], yticks=[3, 3.5, 4, 4.5, 5, 5.5], font_size=14).to_edge(
            LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        pd = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=PAR) for a, b in zip(T, y)])
        zd = VGroup(*[Dot(ax.c2p(a, b), radius=0.07, color=ZERO) for a, b in zip(nt, nz)])
        leg = legend([(PAR, r"published Treasury CMT par point"), (ZERO, r"zero rate (bootstrapped, continuous)")],
                     font_size=18).to_edge(RIGHT, buff=0.3).shift(UP * 2.2)
        tr = ValueTracker(0)
        readout_box = always_redraw(lambda: VGroup(
            MathTex((rf"T = {12 * nt[int(tr.get_value())]:.1f}".rstrip("0").rstrip(".") + r"\ \text{mo}")
                    if nt[int(tr.get_value())] < 1 else rf"T = {nt[int(tr.get_value())]:g}\ \text{{yr}}", font_size=30),
            MathTex(rf"y = {y[int(tr.get_value())]:.2f}\% \to z = {nz[int(tr.get_value())]:.3f}\%", font_size=30,
                    color=ZERO)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(leg, DOWN, buff=0.6,
                                                                                    aligned_edge=LEFT))
        cv = R.Curve(nt, nz / 100)
        one_year_gap_bp = 1e4 * (cv.par(1.0) - np.asarray(c["par"])[list(T).index(1.0)])
        s = np.linspace(0.08, 30, 300)
        line = curve(ax, s, cv.zero(s) * 100, ZERO, stroke_width=3)
        note_ = VGroup(
            wrapped_label(rf"coupon nodes $T>1$ year: max par-rate residual $\approx {sci(c['reprice_max_bp'])}$ bp", 3.8, 18, GREY_A),
            wrapped_label(rf"one-year par-rate residual: {one_year_gap_bp:+.3f} bp under the short-node simplification", 3.8, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(leg, DOWN, buff=2.0, aligned_edge=LEFT)
        with self.voiceover(
            f"Here are fourteen published par-curve maturities on December thirty-first, 2025. They are not fourteen separately executable security quotes. <bookmark mark='a'/> At short nodes the conversion is imposed; at longer nodes the endpoint is solved using synthetic coupon cash flows and the chosen interpolation. Converting compounding conventions and changing coupon weights both affect the relation between zero and par rates. <bookmark mark='b'/> The saved tiny residual applies only to coupon nodes beyond one year. As a one-year semiannual par bond, the short-node approximation instead has a par-rate discrepancy of {one_year_gap_bp:.3f} basis points on this date. The connected curve is one construction compatible with these choices, not a uniquely identified discount curve or a complete independent reproduction of Treasury's method."
        ) as vo:
            self.play(FadeIn(g), FadeIn(pd), FadeIn(leg))
            vo.wait_until("a")
            self.add(readout_box)
            for i in range(len(nt)):
                tr.set_value(i)
                self.play(FadeIn(zd[i], scale=1.6), run_time=0.45)
            vo.wait_until("b")
            self.play(Create(line), FadeIn(note_), run_time=2)
        readout_box.clear_updaters()
        self.add(illustration(r"Treasury daily par yield curve, 31 December 2025"))
        self.wait(0.4)
        self.clear_scene()

    def lab(self, c):
        card = house_lab(r"bootstrap a par curve", R.bootstrap_par, "for Ti, yi in zip(T, y):", 13, width=7.4)
        card.to_edge(LEFT, buff=0.4).to_edge(UP, buff=0.4)
        cv = R.Curve(c["nodes_t"], c["nodes_z"])
        out = [rf"zero rates: 2y {100 * cv.zero(2.0):.3f}%  10y {100 * cv.zero(10.0):.3f}%  30y "
               rf"{100 * cv.zero(30.0):.3f}%",
               rf"par check: 10y {100 * cv.par(10):.4f}% (quoted {100 * c['par'][list(c['tenor']).index(10.0)]:.2f}%)",
               rf"forward 10y->20y: {100 * cv.fwd(10.0, 20.0):.3f}%"]
        with self.voiceover(
            "The unchanged House routine makes its conventions visible. It directly converts short CMT inputs, then solves one longer-node endpoint at a time using the interpolated curve for coupon dates. It uses regular coupon schedules rather than full settlement-date and day-count logic. <bookmark mark='a'/> The ten-year synthetic par check returns the supplied ten-year input within numerical tolerance. That checks implementation consistency for this instrument; it does not validate the short-end approximation, interpolation between observations or executable market prices."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, out)
        self.wait(0.4)
        self.clear_scene()

    def inverted(self, c):
        s = np.asarray(c["s"])
        z, f, gsw = (np.asarray(c[k]) * 100 for k in ("zero", "fwd", "gsw"))
        T, y = np.asarray(c["tenor"]), np.asarray(c["par"]) * 100
        g = axes([0, 30], [2, 6], x_length=8.0, y_length=4.6, xlabel=r"maturity, years", ylabel=r"percent",
                 xticks=[0, 2, 5, 10, 20, 30], yticks=[2, 3, 4, 5, 6], font_size=14).to_edge(LEFT, buff=0.6).shift(
            DOWN * 0.3)
        ax = g.ax
        pd = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=PAR) for a, b in zip(T, y)])
        lz = curve(ax, s, z, ZERO, stroke_width=3.5)
        lf = curve(ax, s, f, FWD, stroke_width=2.5)
        lg = DashedVMobject(curve(ax, s, gsw, WHITE, stroke_width=2), num_dashes=60)
        m2 = s >= 2
        gap = float(np.max(np.abs(gsw[m2] - z[m2])) * 100)
        leg = legend([(PAR, r"par yields"), (ZERO, r"zero rates (bootstrap)"), (FWD, r"forwards (bootstrap)"),
                      (WHITE, r"the Fed's fitted curve (GSW)")], font_size=17).to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        side = VGroup(
            MathTex(rf"10\text{{y}} - 2\text{{y}} = {c['spread_2s10s_bp']:.0f}\ \text{{bp}}", font_size=32,
                    color=QC.LOSS),
            wrapped_label(rf"on the displayed grid from two years out, this bootstrap and GSW zero-yield fit differ by at most {gap:.0f} bp; the "
                          r"fits use different instruments and conventions; short GSW maturities are model extrapolations", 3.3, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(leg, DOWN, buff=0.4, aligned_edge=LEFT)
        side.shift(LEFT * max(0.0, side.get_right()[0] - 6.75))
        with self.voiceover(
            f"March eighth, 2023, gives a very different curve. The published ten-year minus two-year par-rate spread is {c['spread_2s10s_bp']:.0f} basis points. <bookmark mark='a'/> The downward forward segments are rates implied by this discount-curve construction. They are compatible with expected future easing, but term premia and conventions mean they are not direct forecasts of the Fed's decisions. No historical ranking or causal recession claim follows from this one date. <bookmark mark='b'/> The white line is the separate GSW fitted zero-yield curve. On the displayed grid from two years out the difference reaches {gap:.0f} basis points. The methods use different instrument selections, short-end assumptions and fitting criteria. Agreement is a comparison, not proof of truth; disagreement can reveal those modelling choices. All finite displayed rates are retained without clipping."
        ) as vo:
            self.play(FadeIn(g), FadeIn(pd), FadeIn(leg[0]), Create(lz), FadeIn(leg[1]), run_time=2)
            vo.wait_until("a")
            self.play(Create(lf), FadeIn(leg[2]), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(lg), FadeIn(leg[3]), FadeIn(side[1]), run_time=2)
        q = ask(r"Even an exact fit to specified calibration instruments leaves what assumptions and risks unvalidated?")
        with self.voiceover('Pause and predict: even if a curve fits every specified calibration instrument exactly, which interpolation, convention and risk assumptions remain unvalidated?'):
            self.play(FadeIn(q))
        self.add(illustration(r"Treasury par yields and the Fed's GSW curve, 8 March 2023"))
        self.wait(0.5)
        self.clear_scene()
