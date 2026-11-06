from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant6.common import ALT, BAD, DATA_C, EST, GOOD, PART, hist_bars, load, predict, show_card, tbar


class Designs(VoiceoverScene):
    def construct(self):
        d = load("designs")
        self.card()
        self.iv(d)
        self.derive()
        self.did(d)
        self.staggered(d)
        self.rd(d)

    def card(self):
        c = chapter_card(14, r"Causal designs: instruments, differences, discontinuities", r"Does $X$ cause $Y$, or do "
                         r"they only move together?", part=PART)
        with self.voiceover("Chapter fourteen. Causal designs: instruments, differences, and discontinuities."):
            show_card(self, c)
        self.play(FadeOut(c))

    def iv(self, d):
        z = Circle(radius=0.32, color=ALT).set_fill(ALT, 0.15)
        xx = Circle(radius=0.32, color=DATA_C).set_fill(DATA_C, 0.15)
        yy = Circle(radius=0.32, color=EST).set_fill(EST, 0.15)
        u = Circle(radius=0.32, color=BAD).set_fill(BAD, 0.15)
        VGroup(z, xx, yy).arrange(RIGHT, buff=0.9)
        u.next_to(VGroup(xx, yy), UP, buff=0.55)
        lbl = VGroup(*[MathTex(t, font_size=28).move_to(c) for t, c in zip("ZXYU", (z, xx, yy, u))])
        arrows = VGroup(Arrow(z.get_right(), xx.get_left(), buff=0.05, stroke_width=3, color=GREY_A),
                        Arrow(xx.get_right(), yy.get_left(), buff=0.05, stroke_width=3, color=GREY_A),
                        Arrow(u.get_bottom(), xx.get_top(), buff=0.05, stroke_width=2, color=BAD),
                        Arrow(u.get_bottom(), yy.get_top(), buff=0.05, stroke_width=2, color=BAD))
        dag = VGroup(z, xx, yy, u, lbl, arrows).scale(0.9).to_corner(UL, buff=0.5)
        panels = VGroup()
        for name, title in (("weak", r"weak instrument"), ("strong", r"strong instrument")):
            g = axes([-1.0, 2.0], [0, 6], x_length=4.6, y_length=2.2, xticks=[0, 0.5, 1.0], yticks=[], font_size=14,
                     xlabel=r"estimated effect (truth 0.5)")
            ax = g.ax
            edges = np.linspace(-1, 2, 46)
            h_iv = hist_bars(ax, d[name]["iv"], edges, GOOD, opacity=0.7, cap=6)
            h_ols = hist_bars(ax, d[name]["ols"], edges, BAD, opacity=0.5, cap=6)
            truth = DashedLine(ax.c2p(0.5, 0), ax.c2p(0.5, 6), color=WHITE, stroke_width=2)
            t = label(rf"{title}: first-stage $F \approx {d[name]['F']:.0f}$", font_size=19, color=GREY_A).next_to(
                g, UP, buff=0.05)
            panels.add(VGroup(g, h_ols, h_iv, truth, t))
        panels.arrange(DOWN, buff=0.45).to_edge(RIGHT, buff=0.5)
        leg = legend([(BAD, r"OLS"), (GOOD, r"2SLS")], font_size=18).next_to(dag, DOWN, buff=0.5).align_to(dag, LEFT)
        w, s = d["weak"], d["strong"]
        with self.voiceover(
            "Regressions describe; they do not explain. Causal questions, does joining an index raise a price, does a "
            "rule change liquidity, face a confounder, U, that moves both cause and outcome. <bookmark mark='a'/> An "
            "instrument, Z, moves the cause but touches the outcome only through it. In two hundred simulated markets "
            f"with a true effect of a half, least squares finds about {s['ols_mean']:.1f}. <bookmark mark='b'/> With a "
            f"strong instrument, two-stage least squares centres on {s['iv_median']:.2f}. <bookmark mark='c'/> With a weak "
            f"one, first-stage F near {w['F']:.0f}, its middle half runs from {w['iv_iqr'][0]:.1f} to "
            f"{w['iv_iqr'][1]:.1f}. F above ten is only a rough diagnostic, not a universal validity guarantee."
        ) as vo:
            self.play(FadeIn(dag))
            vo.wait_until("a")
            self.play(FadeIn(leg), FadeIn(panels[1][0]), FadeIn(panels[1][4]), FadeIn(panels[1][3]),
                      LaggedStart(*[GrowFromEdge(b, DOWN) for b in panels[1][1]], lag_ratio=0.02))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in panels[1][2]], lag_ratio=0.02))
            vo.wait_until("c")
            self.play(FadeIn(panels[0][0]), FadeIn(panels[0][4]), FadeIn(panels[0][3]),
                      LaggedStart(*[GrowFromEdge(b, DOWN) for b in panels[0][1]], lag_ratio=0.02))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in panels[0][2]], lag_ratio=0.02))
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        C_ = {r"\beta_{IV}": GOOD, r"\hat\beta_{DiD}": EST, r"w_k": BAD, r"\tau_{RD}": ALT}
        rows = [cmath(r"\beta_{IV}", r"=", r"\frac{\mathrm{cov}(z, y)}{\mathrm{cov}(z, x)}", font_size=36, colors=C_),
                cmath(r"\hat\beta_{DiD}", r"=", r"(\bar y_{T,1} - \bar y_{T,0}) - (\bar y_{C,1} - \bar y_{C,0})",
                      font_size=36, colors=C_),
                cmath(r"\hat\beta_{TWFE}", r"=", r"\textstyle\sum_{g,t} w_{gt}\,ATT_{gt},\ \ \text{some } w_{gt} < 0",
                      font_size=36, colors=C_),
                cmath(r"\tau_{RD}", r"=", r"\lim_{r \downarrow c}\mathbb{E}[y \mid r] - \lim_{r \uparrow c}\mathbb{E}[y \mid r]",
                      font_size=36, colors=C_)]
        whys = [why(r"$z \perp u$: the reduced form divided by the first stage (Wald)"),
                why(r"parallel trends: without treatment both groups would have changed alike, so the common change "
                    r"cancels"),
                why(r"Treatment-effect weights can be negative. Goodman-Bacon's two-by-two comparison weights are "
                    r"nonnegative; already-treated controls can contaminate those comparisons."),
                why(r"continuity of potential outcomes at the cutoff: just above and just below are alike")]
        step = ladder(self, rows, whys, keep=4, top=3.2, x=-0.6, buff=0.45, edge=6.8)
        with self.voiceover(
            "Each design in one line. The instrument: because z is unrelated to the confounder, the reduced form over "
            "the first stage isolates the causal slope. <bookmark mark='a'/> Difference in differences: the treated "
            "group's change minus the control group's change; if both would have trended alike, the common change "
            "cancels. <bookmark mark='b'/> Its regression version, two-way fixed effects, is a weighted sum of every "
            "two-by-two comparison in the data, as Andrew Goodman-Bacon showed in 2021, and under staggered timing some "
            "comparisons use already-treated units as controls. Those comparison weights are nonnegative, but the "
            "implied weights on cohort-period treatment effects can be negative. <bookmark mark='c'/> The "
            "discontinuity: the jump in the outcome's average exactly at a cutoff, valid if nothing else jumps there."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def did(self, d):
        dd = d["did"]
        tt, ctrl, trt = np.asarray(dd["t"]), np.asarray(dd["ctrl"]), np.asarray(dd["trt"])
        g = axes([-6.5, 6.5], [0.4, 2.6], x_length=6.8, y_length=4.0, xlabel=r"months from the rule change",
                 ylabel=r"outcome (simulated)", xticks=[-6, 0, 6], yticks=[], font_size=16).to_edge(LEFT, buff=0.7)
        g.shift(DOWN * 0.2)
        ax = g.ax
        lc = curve(ax, tt, ctrl, DATA_C, stroke_width=3)
        lt = curve(ax, tt, trt, EST, stroke_width=3)
        cut = DashedLine(ax.c2p(0, 0.4), ax.c2p(0, 2.6), color=GREY_B, stroke_width=1.5)
        pre = trt[tt < 0].mean() - ctrl[tt < 0].mean()
        ghost = DashedLine(ax.c2p(0, ctrl[tt >= 0][0] + pre), ax.c2p(6, ctrl[-1] + pre), color=GREY_A, stroke_width=2.5)
        gap = DoubleArrow(ax.c2p(6.2, ctrl[-1] + pre), ax.c2p(6.2, trt[-1]), buff=0, color=YELLOW, stroke_width=3,
                          tip_length=0.15)
        side = VGroup(
            legend([(EST, r"treated"), (DATA_C, r"control"), (GREY_A, r"treated, had it followed the control")],
                   font_size=19),
            MathTex(rf"\widehat{{DiD}} = {dd['est']:.3f}\ \ (\text{{truth }} {dd['truth']})", font_size=30, color=YELLOW),
            wrapped_label(r"a real design: in 2004 the SEC ordered a pilot that, from May 2005, suspended the "
                          r"short-sale price tests for about a third of the Russell 3000, chosen by rule: treated and "
                          r"control firms, a date", 5.0, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Difference in differences as a picture: treated and control, before and after. <bookmark mark='a'/> Copy "
            "the control's change onto the treated group's start: the ghost line. The gap is the effect, "
            f"{dd['est']:.3f} against a planted {dd['truth']}. <bookmark mark='b'/> Finance has experiments of this shape: "
            "in 2004 the SEC ordered a pilot under Regulation SHO; from May 2005 about a third of the Russell 3000, picked "
            "by rule, traded without the short-sale price test."
        ) as vo:
            self.play(FadeIn(g), Create(lc), Create(lt), Create(cut), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(ghost))
            self.play(GrowFromCenter(gap), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def staggered(self, d):
        s = d["staggered"]
        W = np.asarray(s["weights"])
        coh = s["cohorts"]
        T = s["T"]
        g = axes([0, 3 * T + 2], [-0.2, 0.2], x_length=7.0, y_length=3.0, ylabel=r"TWFE weight on each treated "
                 r"cohort-period", xticks=[], yticks=[-0.1, 0, 0.1, 0.2], font_size=15).to_edge(LEFT, buff=0.6)
        g.to_edge(UP, buff=0.9)
        ax = g.ax
        bars = VGroup()
        for i, c in enumerate(coh):
            for t in range(T):
                v = W[i, t]
                if abs(v) < 1e-9:
                    continue
                bars.add(tbar(ax, i * (T + 1) + t + 0.5, v, BAD if v < 0 else [DATA_C, ALT, EST][i], width=0.8))
        clab = VGroup(*[label(rf"treated from period {c}", font_size=17, color=[DATA_C, ALT, EST][i]).next_to(
            ax.c2p(i * (T + 1) + T / 2, -0.2), DOWN, buff=0.1) for i, c in enumerate(coh)])
        h = axes([-0.2, 1.4], [0, 1], x_length=5.6, y_length=2.4, xlabel=r"estimated average effect, 200 panels",
                 xticks=[0, 0.5, 1.0], yticks=[], font_size=15).to_edge(LEFT, buff=0.8).to_edge(DOWN, buff=0.4)
        edges = np.linspace(-0.2, 1.4, 49)
        ht = hist_bars(h.ax, s["twfe"], edges, BAD, opacity=0.7, density=False)
        hc = hist_bars(h.ax, s["cs"], edges, GOOD, opacity=0.7, density=False)
        mx = max(max(b.height for b in ht), max(b.height for b in hc))
        for grp in (ht, hc):
            for b in grp:
                b.stretch_to_fit_height(max(b.height / mx * 2.0, 0.001), about_edge=DOWN)
        truth = DashedLine(h.ax.c2p(s["truth"], 0), h.ax.c2p(s["truth"], 1), color=YELLOW, stroke_width=3)
        side = VGroup(
            legend([(BAD, rf"two-way fixed effects: {s['twfe_mean']:.2f}"),
                    (GOOD, rf"Callaway--Sant'Anna: {s['cs_mean']:.2f}"), (YELLOW, rf"supported-cell truth: {s['truth']:.2f}")],
                   font_size=19),
            wrapped_label(r"three cohorts, effects growing 0.3 a period after treatment; every unit is eventually "
                          r"treated; the target shown averages only cells with not-yet-treated controls", 4.6, 18, GREY_B),
            wrapped_label(r"Baker, Larcker and Wang (2022): re-estimating published staggered designs in finance and "
                          r"accounting with robust estimators often changed the conclusions", 4.6, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.8)
        with self.voiceover(
            "Most rules arrive in waves, and the standard regression quietly uses early-treated firms as controls for "
            "later ones. <bookmark mark='a'/> Here are its weights on each treated cohort and period when effects grow "
            "after treatment: the first cohort's late periods get negative weight. <bookmark mark='b'/> Over two hundred "
            f"panels, the target averages cells with not-yet-treated controls. Later effects lack those controls. The target is {s['truth']:.2f}; two-way fixed effects finds {s['twfe_mean']:.2f}, about "
            f"{100 * s['twfe_mean'] / s['truth']:.0f} percent of it. Callaway and Sant'Anna's estimator, comparing each "
            f"cohort only with units not yet treated in this simplified implementation, centres on {s['cs_mean']:.2f}. <bookmark mark='c'/> Baker, Larcker "
            "and Wang re-ran published staggered studies in 2022, and conclusions often changed."
        ) as vo:
            self.play(FadeIn(g), FadeIn(clab))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN if b.get_center()[1] > ax.c2p(0, 0)[1] else UP)
                                    for b in bars], lag_ratio=0.1, run_time=2))
            self.play(*[Indicate(b, color=WHITE, scale_factor=1) for b in bars if b.get_center()[1] < ax.c2p(0, 0)[1]])
            vo.wait_until("b")
            self.play(FadeIn(h), Create(truth), FadeIn(side[0]), FadeIn(side[1]))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in ht], lag_ratio=0.02))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in hc], lag_ratio=0.02))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def rd(self, d):
        r = d["rd"]
        ex = r["example"]
        x, y = np.asarray(ex["x"]), np.asarray(ex["y"])
        bws = r["bw"]
        g = axes([-5, 5], [-26, 28], x_length=6.6, y_length=4.4, xlabel=r"index rank minus 1{,}000 (hundreds)",
                 ylabel=r"outcome, simulated", xticks=[-4, -2, 0, 2, 4], yticks=[-20, 0, 20], font_size=15)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        pick = np.random.default_rng(0).choice(len(x), 700, replace=False)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.022, color=DATA_C if a < 0 else EST,
                            fill_opacity=0.6) for a, b in zip(x[pick], y[pick])])
        cut = DashedLine(ax.c2p(0, -26), ax.c2p(0, 28), color=GREY_B, stroke_width=1.5)
        k = ValueTracker(0)

        def fits():
            i = int(min(k.get_value(), len(bws) - 1))
            bw = bws[i] / 100
            f = ex["fits"][str(bws[i])]
            L, R = f["left"], f["right"]
            win = Rectangle(width=ax.c2p(bw, 0)[0] - ax.c2p(-bw, 0)[0], height=ax.c2p(0, 28)[1] - ax.c2p(0, -26)[1],
                            stroke_width=0, fill_color=YELLOW, fill_opacity=0.07).move_to(ax.c2p(0, 1))
            ll = Line(ax.c2p(-bw, L[0] - L[1] * bw), ax.c2p(0, L[0]), color=DATA_C, stroke_width=4)
            rr = Line(ax.c2p(0, R[0]), ax.c2p(bw, R[0] + R[1] * bw), color=EST, stroke_width=4)
            jump = Line(ax.c2p(0, L[0]), ax.c2p(0, R[0]), color=YELLOW, stroke_width=5)
            ro = MathTex(rf"\text{{window}} \pm {bws[i]}\ \text{{ranks: jump}} = {f['jump']:.2f} \pm {2 * f['se']:.2f}",
                         font_size=26, color=YELLOW).next_to(g, UP, buff=0.05)
            return VGroup(win, ll, rr, jump, ro)
        fm = always_redraw(fits)
        e = axes([0, 320], [0, 1.6], x_length=4.4, y_length=2.6, xlabel=r"window, ranks either side",
                 ylabel=r"error of the jump, 200 samples", xticks=[50, 150, 300], yticks=[0.5, 1.0, 1.5], font_size=14)
        e.to_edge(RIGHT, buff=0.4).shift(UP * 0.6)
        rm = curve(e.ax, bws, r["rmse"], ALT, stroke_width=3)
        sdc = curve(e.ax, bws, r["sd"], GREY_B, stroke_width=2)
        bias = curve(e.ax, bws, np.abs(np.asarray(r["mean"]) - r["truth"]), BAD, stroke_width=2)
        leg = legend([(ALT, r"root mean squared error"), (GREY_B, r"spread"), (BAD, r"bias")], font_size=16).next_to(
            e, DOWN, buff=0.25).align_to(e, LEFT)
        best = bws[int(np.argmin(r["rmse"]))]
        cite = wrapped_label(r"real data: Chang, Hong and Liskovich (2015), the Russell 1000/2000 cutoff", 4.6, 18,
                             GREY_B).next_to(leg, DOWN, buff=0.25).align_to(e, LEFT)
        q = predict(r"In the shown three-cohort design with growing effects, is the TWFE estimate too big "
                    r"or too small?", width=5.6).to_corner(DR, buff=0.3)
        with self.voiceover(
            "The discontinuity. Russell ranks stocks by size: number one thousand joins the large-cap index, one "
            "thousand and one leads the small-cap index, where index funds hold far more of it. Chang, Hong and "
            "Liskovich used this cutoff in 2015 to measure the price effect of indexing. A simulated version, with a "
            "planted jump of two: <bookmark mark='a'/> fit a line on each side within a window, read the jump, and widen "
            "the window. Narrow windows are noisy; wide ones reach where the relation curves, and are biased. "
            f"<bookmark mark='b'/> Over two hundred samples the error is smallest near {best} ranks: the bandwidth "
            "trade-off again. <bookmark mark='c'/> Pause and predict: in the shown staggered-adoption design with growing "
            "effects, is two-way "
            "fixed effects too big or too small? Too small, possibly negative."
            " When there are too many controls for any design, machine learning can help, carefully. Next."
        ) as vo:
            self.play(FadeIn(g), Create(cut), LaggedStart(*[FadeIn(dd) for dd in dots], lag_ratio=0.002, run_time=2))
            vo.wait_until("a")
            self.add(fm)
            self.play(k.animate.set_value(len(bws) - 1), run_time=vo.until("b") - 0.5, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(e), Create(rm), Create(sdc), Create(bias), FadeIn(leg), FadeIn(cite))
            vo.wait_until("c")
            # the bias legend and citation have been read; the question takes their corner
            self.play(FadeOut(leg), FadeOut(cite), FadeIn(q, shift=UP * 0.2))
        fm.clear_updaters()
        self.wait(0.4)
        self.clear_scene()
