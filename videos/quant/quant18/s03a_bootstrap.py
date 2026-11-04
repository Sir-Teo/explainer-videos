from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import rates as R
from videos.quant.quant18.common import FWD, PAR, PART, ZERO, ask, house_lab, illustration, load


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
        with self.voiceover("Chapter five. Bootstrapping a curve from the market's quotes."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def ladder_(self):
        rows = [cmath(r"Z(t)", r"=", r"\big(1 + \tfrac{y_t}{2}\big)^{-2t},\quad t \le 1", font_size=40,
                      colors={r"Z(t)": ZERO}),
                cmath(r"100", r"=", r"\tfrac{c_T}{2}\sum_{t_i < T} Z(t_i) + \big(100 + \tfrac{c_T}{2}\big) Z(T)",
                      font_size=40, colors={r"100": PAR}),
                cmath(r"z(t)\,t", r"\ \text{linear between nodes}", r"\Leftrightarrow\ f\ \text{flat between nodes}",
                      font_size=38, colors={r"z(t)\,t": ZERO}),
                cmath(r"Z(T)", r"=", r"\text{the one unknown: solve, then move to the next } T", font_size=38,
                      colors={r"Z(T)": ZERO})]
        whys = [why(r"bills (a year or less) pay once: their quoted yield gives the discount factor directly"),
                why(r"a par bond: coupon $c_T$ equal to its yield, so it prices at 100. Every coupon date before $T$ is "
                    r"already known or lies between known nodes"),
                why(r"between nodes, interpolate: the simplest rule keeps the forward rate constant"),
                why(r"so each bond adds exactly one unknown: a root in one variable. Ten bonds, ten nodes, every input "
                    r"repriced to the cent")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.6, buff=0.55, edge=6.9)
        with self.voiceover(
            "Treasury publishes par yields, not zero rates. The bootstrap gets one from the other. Bills pay once, so "
            "a bill's yield is already a discount factor. <bookmark mark='a'/> A two-year note at par pays its coupon "
            "four times; the first three dates are covered by the bills, so the only unknown is the discount factor at "
            "two years. <bookmark mark='b'/> For a ten-year note, the coupons fall between known nodes, so we need a rule "
            "for the gaps; the simplest keeps the forward rate constant between quoted maturities. "
            "<bookmark mark='c'/> Then each new bond adds exactly one unknown, solved by a one-dimensional root search, "
            "and we move on to the next."
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
        leg = legend([(PAR, r"par yield (Treasury)"), (ZERO, r"zero rate (bootstrapped, continuous)")],
                     font_size=18).to_edge(RIGHT, buff=0.3).shift(UP * 2.2)
        tr = ValueTracker(0)
        readout_box = always_redraw(lambda: VGroup(
            MathTex(rf"T = {nt[int(tr.get_value())]:g}\ \text{{yr}}", font_size=30),
            MathTex(rf"y = {y[int(tr.get_value())]:.2f}\% \to z = {nz[int(tr.get_value())]:.3f}\%", font_size=30,
                    color=ZERO)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(leg, DOWN, buff=0.6,
                                                                                    aligned_edge=LEFT))
        cv = R.Curve(nt, nz / 100)
        s = np.linspace(0.08, 30, 300)
        line = curve(ax, s, cv.zero(s) * 100, ZERO, stroke_width=3)
        note_ = wrapped_label(rf"every par bond repriced to within {c['reprice_max_bp']:.0e} bp", 3.8, 18,
                              GREY_A).next_to(leg, DOWN, buff=2.0, aligned_edge=LEFT)
        with self.voiceover(
            "Here it is on the last day of 2025, with Treasury's fourteen quotes from one month to thirty years. "
            "<bookmark mark='a'/> Node by node: each zero rate solved from its bond and everything to its left. At the "
            "short end the zero rates sit a little below the par yields, because these are continuously compounded. "
            "Out at ten years and beyond they pull above the par yields: on a rising curve a coupon bond's yield is an "
            "average that leans on the cheaper early coupons. <bookmark mark='b'/> Joined up, the zero curve. Every "
            "one of the quotes is repriced exactly."
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
        card = house_lab(r"Lab: bootstrap a par curve", R.bootstrap_par, "for Ti, yi in zip(T, y):", 13, width=7.4)
        card.to_edge(LEFT, buff=0.4).to_edge(UP, buff=0.4)
        cv = R.Curve(c["nodes_t"], c["nodes_z"])
        out = [rf"zero rates: 2y {100 * cv.zero(2.0):.3f}%  10y {100 * cv.zero(10.0):.3f}%  30y "
               rf"{100 * cv.zero(30.0):.3f}%",
               rf"par check: 10y {100 * cv.par(10):.4f}% (quoted {100 * c['par'][list(c['tenor']).index(10.0)]:.2f}%)",
               rf"forward 10y->20y: {100 * cv.fwd(10.0, 20.0):.3f}%"]
        with self.voiceover(
            "The House's version is a dozen lines. For bills, take the quote. For each coupon bond, write its cash "
            "flows, and find the one zero rate at its maturity that makes the price exactly a hundred, using the curve "
            "built so far for the dates in between. <bookmark mark='a'/> Run it, and check: the ten-year par yield "
            "comes back exactly as quoted."
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
        g = axes([0, 30], [3, 6], x_length=8.4, y_length=4.6, xlabel=r"maturity, years", ylabel=r"percent",
                 xticks=[0, 2, 5, 10, 20, 30], yticks=[3, 4, 5, 6], font_size=14).to_edge(LEFT, buff=0.6).shift(
            DOWN * 0.3)
        ax = g.ax
        pd = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=PAR) for a, b in zip(T, y)])
        lz = curve(ax, s, np.clip(z, 3, 6), ZERO, stroke_width=3.5)
        lf = curve(ax, s, np.clip(f, 3, 6), FWD, stroke_width=2.5)
        lg = DashedVMobject(curve(ax, s, np.clip(gsw, 3, 6), WHITE, stroke_width=2), num_dashes=60)
        m2 = s >= 2
        gap = float(np.max(np.abs(gsw[m2] - z[m2])) * 100)
        leg = legend([(PAR, r"par yields"), (ZERO, r"zero rates (bootstrap)"), (FWD, r"forwards (bootstrap)"),
                      (WHITE, r"the Fed's fitted curve (GSW)")], font_size=17).to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        side = VGroup(
            MathTex(rf"10\text{{y}} - 2\text{{y}} = {c['spread_2s10s_bp']:.0f}\ \text{{bp}}", font_size=32,
                    color=QC.LOSS),
            wrapped_label(rf"from two years out, the bootstrap and the Fed's fit differ by at most {gap:.0f} bp; the "
                          r"Fed's fit leaves out bills, so at the short end it is an extrapolation", 3.8, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(leg, DOWN, buff=0.4, aligned_edge=LEFT)
        with self.voiceover(
            "A very different day: the eighth of March 2023, two days before Silicon Valley Bank failed. Short rates "
            "were above five percent; ten-year yields were near four. <bookmark mark='a'/> The ten-year minus two-year "
            f"spread was {c['spread_2s10s_bp']:.0f} basis points, deeper than on any day since 1981; only one day that July "
            "went a basis point further. The forwards "
            "plunge: the market expected the Fed to be cutting within a year or two. <bookmark mark='b'/> In white, "
            "the Fed's own fitted curve for the same day. Past two years the two agree to within "
            f"{gap:.0f} basis points; at the very short end the Fed's curve is an extrapolation, because it is fitted "
            "to notes and bonds only."
        ) as vo:
            self.play(FadeIn(g), FadeIn(pd), FadeIn(leg[0]), Create(lz), FadeIn(leg[1]), run_time=2)
            vo.wait_until("a")
            self.play(Create(lf), FadeIn(leg[2]), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(lg), FadeIn(leg[3]), FadeIn(side[1]), run_time=2)
        q = ask(r"your bootstrap reprices every quote exactly. Does that make it right?")
        with self.voiceover("Your bootstrap reprices every input exactly. Does that make it right?"):
            self.play(FadeIn(q))
        self.add(illustration(r"Treasury par yields and the Fed's GSW curve, 8 March 2023"))
        self.wait(0.5)
        self.clear_scene()
