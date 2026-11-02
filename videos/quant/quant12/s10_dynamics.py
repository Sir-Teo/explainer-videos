from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant12.common import (BAD, IV, LV, OPT, PART, RV, SPOT, axes3, fixed, grid_fn, load, real_data,
                                         surf3)


class Dynamics(VoiceoverScene, ThreeDScene):
    def construct(self):
        d = load("dynamics")
        m = load("lv_mc")
        self.card()
        self.sticky(m, d)
        self.derive(d)
        self.weekly(d)
        self.pca(d)

    def card(self):
        c = chapter_card(2, r"How the surface moves", r"When spot moves, where does the smile go?", part=PART)
        with self.voiceover("Chapter two. How the surface moves."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sticky(self, m, d):
        kk = np.asarray(m["kk"])
        sh = np.asarray(m["shifts"])
        mv = {x: np.asarray(m["move"][x]) for x in ("strike", "moneyness", "lv")}
        at = {x: np.asarray(m["atm"][x]) for x in ("strike", "moneyness", "lv")}
        g = axes([-0.3, 0.3], [0.3, 0.6], x_length=7.4, y_length=4.4, xlabel=r"strike, as $\ln K/F_0$ (today's forward)",
                 ylabel=r"30-day implied volatility", xticks=[-0.2, 0, 0.2], yticks=[0.35, 0.45, 0.55],
                 yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=17).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        tr = ValueTracker(4.0)  # index into the shifts; 4 = no move

        def at_i(arr):
            x = tr.get_value()
            i = int(np.clip(np.floor(x), 0, len(arr) - 2))
            f = x - i
            return (1 - f) * arr[i] + f * arr[i + 1]
        cols = {"strike": SPOT, "moneyness": IV, "lv": LV}
        curves = {x: always_redraw(lambda x=x: curve(ax, kk, np.clip(at_i(mv[x]), 0.3, 0.6), cols[x], stroke_width=3))
                  for x in cols}
        dots = {x: always_redraw(lambda x=x: Dot(ax.c2p(float(at_i(sh)), float(np.clip(at_i(at[x]), 0.3, 0.6))),
                                               radius=0.08, color=cols[x])) for x in cols}
        spot = always_redraw(lambda: DashedLine(ax.c2p(float(at_i(sh)), 0.3), ax.c2p(float(at_i(sh)), 0.6),
                                                color=GREY_B, stroke_width=2))
        leg = legend([(SPOT, r"sticky strike"), (IV, r"sticky moneyness (delta)"), (LV, r"local volatility")],
                     font_size=18).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        ro = VGroup(
            readout(r"\ln S/F_0 =", lambda: float(at_i(sh)), digits=2, font_size=28, color=GREY_A),
            readout(r"\sigma_{\text{ATM}}^{\text{strike}} =", lambda: 100 * float(at_i(at["strike"])), digits=1,
                    font_size=28, color=SPOT),
            readout(r"\sigma_{\text{ATM}}^{\text{moneyness}} =", lambda: 100 * float(at_i(at["moneyness"])), digits=1,
                    font_size=28, color=IV),
            readout(r"\sigma_{\text{ATM}}^{\text{local vol}} =", lambda: 100 * float(at_i(at["lv"])), digits=1,
                    font_size=28, color=LV),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5).shift(UP * 0.6)
        q = wrapped_label(r"pause and predict: spot falls 5\%, the skew is $-0.4$ vol points per 1\% of moneyness, "
                          r"sticky strike. Where is ATM vol?", 4.6, 19, QC.HOUSE).next_to(ro, DOWN, buff=0.4)
        src = real_data(r"the Surface's 30-day smile (SSVI); local vol by Berestycki--Busca--Florent's average")
        with self.voiceover(
            "Here is the Surface's thirty-day smile, against fixed strikes. Move the spot: where does the smile go? "
            "<bookmark mark='a'/> Sticky strike: every strike keeps its volatility, the curve stays put, and the "
            "at-the-money point slides along it. Sticky moneyness, or sticky delta: the smile travels with the spot. "
            "<bookmark mark='b'/> And local volatility, Chapter six's model, moves it the other way. Emanuel Derman "
            "called these the regimes of volatility in 1999. Pause and predict: spot falls five percent, the skew is "
            "four tenths of a point per percent, sticky strike. At-the-money volatility? Two points higher."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(leg))
            self.add(spot, curves["strike"], dots["strike"])
            self.play(FadeIn(ro[0]), FadeIn(ro[1]))
            vo.wait_until("a")
            self.add(curves["moneyness"], dots["moneyness"])
            self.play(FadeIn(ro[2]))
            self.play(tr.animate.set_value(0.0), run_time=2.5)
            self.play(tr.animate.set_value(8.0), run_time=3.5)
            vo.wait_until("b")
            self.add(curves["lv"], dots["lv"])
            self.play(FadeIn(ro[3]))
            self.play(tr.animate.set_value(0.0), run_time=3)
            self.play(tr.animate.set_value(4.0), FadeIn(q), run_time=2)
        self.wait(0.4)
        for mob in list(curves.values()) + list(dots.values()) + [spot] + list(ro):
            mob.clear_updaters()
        self.clear_scene()

    def derive(self, d):
        rows = [cmath(r"\Delta_C = N(d_1) = 0.25", r"\Rightarrow", r"k_{25C} = 0.674\,\sigma\sqrt T + \tfrac12\sigma^2 T",
                      font_size=34, colors={r"\Delta_C = N(d_1) = 0.25": IV}),
                cmath(r"\text{RR}_{25} = \sigma_{25C} - \sigma_{25P}", r"\approx", r"\partial_k\sigma\cdot(k_{25C} - k_{25P}),"
                      r"\quad \text{BF}_{25} = \tfrac12(\sigma_{25C} + \sigma_{25P}) - \sigma_{\text{ATM}}", font_size=30,
                      colors={r"\text{RR}_{25} = \sigma_{25C} - \sigma_{25P}": BAD}),
                cmath(r"R", r"=", r"\frac{d\sigma_{\text{ATM}}/d\ln S}{\partial_k\sigma\,|_{k=0}}", font_size=36,
                      colors={r"R": LV}),
                cmath(r"\sigma_{\text{ATM}}(S) = \sigma(k{=}\ln S/S_0)", r"\Rightarrow", r"R = 1;\qquad "
                      r"\sigma(\ln K/S)\ \text{fixed} \Rightarrow R = 0", font_size=32),
                cmath(r"\Delta", r"=", r"\Delta_{BS} + \mathcal{V}\,\frac{(R - 1)\,\partial_k\sigma}{S}", font_size=36,
                      colors={r"\Delta": OPT})]
        whys = [why(r"$d_1 = (-k + w/2)/\sqrt w$; invert $N(d_1) = 0.25$: a 25-delta call is about two-thirds of a standard "
                    r"deviation out"),
                why(rf"first order in the smile's slope; on the Surface, 30 days: RR$_{{25}}$ = {100 * d['rr25']:+.1f}, "
                    rf"BF$_{{25}}$ = {100 * d['bf25']:+.1f} vol points"),
                why(r"the skew-stickiness ratio (Bergomi): how much of the skew the at-the-money point rides"),
                why(r"differentiate each rule at $S = S_0$"),
                why(r"chain rule: a fixed strike's vol moves by $(R-1)\,\partial_k\sigma$ per unit of $\ln S$, and the vega "
                    r"of that move belongs in the hedge")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-1.0, buff=0.7, edge=6.9)
        rr, bf = 100 * d["rr25"], 100 * d["bf25"]
        with self.voiceover(
            "Desks quote by delta. A twenty-five-delta call solves N of d one equals a quarter: about two thirds of a "
            "standard deviation above the forward. <bookmark mark='a'/> The risk reversal reads the slope, the "
            f"butterfly the curvature: on the Surface at thirty days, {rr:+.1f} and {bf:+.1f} points. "
            "<bookmark mark='b'/> To measure the regime, Lorenzo Bergomi's skew-stickiness ratio R divides the move in "
            "at-the-money volatility per unit of log spot by the skew. <bookmark mark='c'/> Sticky strike gives one; "
            "sticky moneyness, zero. <bookmark mark='d'/> And when R is not one, every fixed strike's volatility moves "
            "with the spot, so the delta picks up a vega term."
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

    def weekly(self, d):
        em, es = np.asarray(d["sticky_m"]), np.asarray(d["sticky_s"])
        n = len(em)
        g = axes([0, n], [0, 15], x_length=7.2, y_length=3.6, xlabel=r"week", ylabel=r"error predicting next week's "
                 r"30-day smile (vol points)", xticks=[0, n], yticks=[0, 5, 10, 15], font_size=16
                 ).to_edge(LEFT, buff=0.6).shift(UP * 0.4)
        ax = g.ax
        x = np.arange(n)
        lm = curve(ax, x, np.clip(em, 0, 15), IV, stroke_width=2)
        ls = curve(ax, x, np.clip(es, 0, 15), SPOT, stroke_width=2)
        leg = legend([(IV, rf"sticky moneyness: mean {d['sticky_m_mean']:.2f}"), (SPOT, rf"sticky strike: mean "
                                                                                      rf"{d['sticky_s_mean']:.2f}")],
                     font_size=17).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        R = d["ssr"]
        # the dial: 0 (moneyness), 1 (strike), 2 (local vol)
        dial = VGroup()
        arc = Arc(radius=1.7, start_angle=PI, angle=-PI, color=GREY_C, stroke_width=4)
        dial.add(arc)
        for v_, name, col in ((0, r"sticky moneyness", IV), (1, r"sticky strike", SPOT), (2, r"local vol", LV)):
            ang = PI - PI * v_ / 2
            p_ = arc.get_arc_center() + 1.7 * np.array([np.cos(ang), np.sin(ang), 0])
            dial.add(Dot(p_, color=col, radius=0.07), label(name, font_size=16, color=col).next_to(p_, UP if v_ == 1 else
                                                                                                   (LEFT if v_ == 0 else RIGHT), buff=0.1))
        rv = float(np.clip(R["R"], -0.3, 2.3))
        ang = PI - PI * rv / 2
        needle = Arrow(arc.get_arc_center(), arc.get_arc_center() + 1.5 * np.array([np.cos(ang), np.sin(ang), 0]),
                       buff=0, color=QC.HOUSE, stroke_width=5)
        dial.add(needle)
        dial.to_edge(RIGHT, buff=0.9).shift(UP * 0.6)
        ident = abs(R["t"]) >= 2
        verdict = (r"identified: the slope is significant" if ident else
                   r"not identified: the slope is noise, and the mean skew is near zero")
        side = VGroup(MathTex(rf"\hat R = {R['R']:.1f},\ \ t = {R['t']:.1f},\ \ \text{{corr}} = {R['corr']:.2f}",
                              font_size=28, color=QC.HOUSE),
                      wrapped_label(verdict, 4.6, 19, GREY_A)).arrange(DOWN, buff=0.2).next_to(dial, DOWN, buff=0.3)
        foot = wrapped_label(rf"sticky strike predicted better in {100 * d['strike_better']:.0f}\% of {n} weekly pairs",
                             7.2, 19, GREY_B).next_to(g, DOWN, buff=0.35).align_to(g, LEFT)
        src = real_data(r"weekly Deribit surfaces, 2021--2025; the 30-day row, strikes within $\pm 20\%$")
        mm, ms, sb = d["sticky_m_mean"], d["sticky_s_mean"], 100 * d["strike_better"]
        rhat, tstat = R["R"], R["t"]
        branch = ("This time the slope is clearly not zero: at-the-money volatility falls when Bitcoin rises. Divided by "
                  "an average skew that is small, the ratio lands near two, the local-volatility value; trust the sign "
                  "of the slope more than the size of the ratio. " if ident else
                  "Do not believe it. The slope is indistinguishable from zero, and Bitcoin's average skew is close to "
                  "zero too, so the ratio of two small, noisy numbers is not identified. ")
        with self.voiceover(
            f"Test the rules on {n} pairs of consecutive weeks: predict next week's thirty-day smile from this "
            f"week's, holding moneyness or holding strikes. Sticky moneyness misses by {mm:.2f} volatility points on "
            f"average, sticky strike by {ms:.2f}, and sticky strike wins in only {sb:.0f} percent of weeks. "
            "<bookmark mark='a'/> Now estimate the ratio itself, by regressing the weekly change in at-the-money "
            f"volatility on the change in log spot and dividing by the average skew. The point estimate is "
            f"{rhat:.1f}, with a t-statistic of {tstat:.1f}. "
            + branch
            + "In equity indices, where the skew is steep and stable, the same regression is informative; on this market, "
            "the honest answer is that we cannot tell."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(lm), Create(ls), FadeIn(leg), run_time=2.5)
            self.play(FadeIn(foot))
            vo.wait_until("a")
            self.play(Create(arc), FadeIn(dial[1:-1]))
            self.play(GrowArrow(needle), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def pca(self, d):
        comp = np.asarray(d["comp"])  # (3, 6, 17)
        ev = np.asarray(d["explained"])
        sd = np.asarray(d["score_sd"])
        kg = np.linspace(-0.4, 0.4, comp.shape[2])
        Tg = np.asarray(d["pc_T"]) / 365
        base_s = load("surface")
        base = np.log(np.asarray(base_s["grid_iv"])[2:])
        ax = axes3([-0.4, 0.4, 0.2], [0, 0.5, 0.1], [0.2, 1.0, 0.2], x_length=6.4, y_length=4.4, z_length=3.0,
                   shift=LEFT * 1.8 + DOWN * 0.6)
        self.set_camera_orientation(phi=66 * DEGREES, theta=-60 * DEGREES, zoom=0.85)
        amp = ValueTracker(0.0)
        which = [0]

        def f(u, v):
            z = base + amp.get_value() * 2 * sd[which[0]] * comp[which[0]]
            return float(np.exp(grid_fn(kg, Tg, z)(u, v)))
        s = always_redraw(lambda: surf3(ax, f, (-0.4, 0.4), (Tg[0], Tg[-1]), 0.2, 1.0, resolution=(18, 10)))
        bars = VGroup()
        bw = 0.5
        for i in range(4):
            h = 3.0 * ev[i]
            r = Rectangle(width=bw, height=max(h, 0.02), stroke_width=0, fill_color=[IV, LV, BAD, GREY_B][i],
                          fill_opacity=0.85)
            bars.add(VGroup(r, label(rf"PC{i + 1}", font_size=16, color=GREY_B), label(f"{100 * ev[i]:.0f}\\%",
                                                                                         font_size=16)))
        for i, b in enumerate(bars):
            b[0].move_to([3.6 + i * 0.75, -2.2 + b[0].height / 2, 0])
            b[1].next_to(b[0], DOWN, buff=0.1)
            b[2].next_to(b[0], UP, buff=0.08)
        names = [label(r"PC1: the level breathes", font_size=21, color=IV),
                 label(r"PC2: the skew tilts", font_size=21, color=LV),
                 label(r"PC3: short end against long; the smile bends", font_size=21, color=BAD)]
        for nm in names:
            nm.to_corner(UR, buff=0.4)
        head = label(r"principal components of weekly surface moves (Cont and da Fonseca 2002)", font_size=21,
                     color=GREY_A).to_edge(UP, buff=0.3).shift(LEFT * 1.5)
        src = real_data(r"weekly changes of the log-vol grid, 17 strikes $\times$ 4 expiries (30--180 days), 2021--2025")
        fixed(self, bars, *names, head, src)
        e1, e2, e3 = 100 * ev[0], 100 * ev[1], 100 * ev[2]
        tot = e1 + e2 + e3
        with self.voiceover(
            "Real surfaces do not follow any one rule. So measure how they move. Take every week's change in the log of "
            "the grid from one month to six, sixty-eight numbers, and find its principal components, as Rama Cont and "
            "José da Fonseca did for index options in 2002. <bookmark mark='a'/> The first component is a level: the "
            f"whole surface breathes up and down together. It explains {e1:.0f} percent of the variance. "
            f"<bookmark mark='b'/> The second tilts the skew, puts against calls: {e2:.0f} percent. "
            "<bookmark mark='c'/> The third moves the short end against the long, and bends the smile: "
            f"{e3:.0f} percent. Three numbers a week carry {tot:.0f} percent of the motion of sixty-eight, the same "
            "low dimension, and nearly the same three shapes, that Cont and da Fonseca found for the S&P 500. "
            "Chapter seventeen will let a neural network find its own coordinates."
        ) as vo:
            self.play(Create(ax), FadeIn(head), FadeIn(src))
            self.add(s)
            vo.wait_until("a")
            self.play(FadeIn(names[0]), FadeIn(bars[0]))
            self.play(amp.animate.set_value(1.0), run_time=1.5)
            self.play(amp.animate.set_value(-1.0), run_time=2)
            self.play(amp.animate.set_value(0.0), run_time=1)
            vo.wait_until("b")
            which[0] = 1
            self.play(FadeOut(names[0]), FadeIn(names[1]), FadeIn(bars[1]))
            self.play(amp.animate.set_value(1.0), run_time=1.5)
            self.play(amp.animate.set_value(-1.0), run_time=2)
            self.play(amp.animate.set_value(0.0), run_time=1)
            vo.wait_until("c")
            which[0] = 2
            self.play(FadeOut(names[1]), FadeIn(names[2]), FadeIn(bars[2]), FadeIn(bars[3]))
            self.play(amp.animate.set_value(1.0), run_time=1.5)
            self.play(amp.animate.set_value(-1.0), run_time=2)
            self.play(amp.animate.set_value(0.0), run_time=1)
        s.clear_updaters()
        self.move_camera(phi=0, theta=-90 * DEGREES, run_time=0.5)
        self.wait(0.3)
        self.clear_scene()
