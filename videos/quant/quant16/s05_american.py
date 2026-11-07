from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, GOOD, OPT, PART, SPOT, illustration, load, polyline, predict, axes, data_range, pause_card, flat_camera

DEG_COL = {1: GREY_B, 2: QC.THETA, 3: QC.GAIN, 4: QC.DELTA, 5: QC.OPTION}


class American(VoiceoverScene):
    def construct(self):
        a = load("american")
        lv = load("lsm_live")
        br = load("bermudan_ref")
        self.card()
        self.backward(lv)
        self.proof()
        self.sweep(lv, a, br)

    def card(self):
        c = chapter_card(8, r"American options I: Longstaff--Schwartz on simulated paths", r"How do you decide when to "
                         r"exercise with only paths?", lit=(2001,), part=PART)
        with self.voiceover('Chapter eight. American options, part one: Longstaff and Schwartz on simulated paths.'):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def backward(self, lv):
        K, n = 100.0, 25
        t = np.linspace(0, 1, n + 1)
        P = np.asarray(lv["paths"])
        tb_t, tb_b = np.asarray(lv["tree_t"]), np.asarray(lv["tree_b"])
        bnd = np.asarray(lv["boundary"], float)
        yr = data_range(P[:150], tb_b, bnd, [K])
        g = axes([0, 1], yr, x_length=6.4, y_length=4.6, xlabel=r"time (years)", ylabel=r"stock price",
                 xticks=[0, 0.5, 1], yticks=[70, 100, 130], font_size=15).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        fan = path_fan(ax, t, P[:150], color=SPOT, opacity=0.18, stroke_width=1)
        strike = DashedLine(ax.c2p(0, K), ax.c2p(1, K), stroke_color=GREY_B, stroke_width=1.5)
        ok = np.isfinite(tb_b)
        tree = DashedVMobject(polyline(ax, tb_t[ok], tb_b[ok], WHITE, stroke_width=2, dots=False)[0],
                              num_dashes=40)
        cursor = ValueTracker(1.0)
        cur_line = always_redraw(lambda: Line(ax.c2p(cursor.get_value(), yr[0]), ax.c2p(cursor.get_value(), yr[1]),
                                              stroke_color=QC.DELTA, stroke_width=2))
        selected = {}
        for key, rec in lv["records"].items():
            ss = np.asarray(rec["S"])[:300]
            yy = np.asarray(rec["Y"])[:300]
            xx = np.linspace(ss.min(), ss.max(), 60)
            selected[key] = (ss, yy, xx, np.polyval(rec["coef"], xx / K))
        xr = data_range(*[v[0] for v in selected.values()], bnd, [K])
        cash_yr = data_range(*[v[j] for v in selected.values() for j in (1, 3)], K - np.asarray(xr), zero=True)
        s = axes(xr, cash_yr, x_length=4.6, y_length=3.4, xlabel=r"spot at this date (in the money)",
                 ylabel=r"realised discounted cash flow", xticks=[70, 85, 100], yticks=[0, 20, 40], font_size=14)
        s.to_edge(RIGHT, buff=0.5).shift(DOWN * 0.3)
        sx = s.ax
        pay = curve(sx, np.linspace(*xr, 40), np.maximum(100 - np.linspace(*xr, 40), 0), BAD, stroke_width=2.5)

        def date_panel(i):
            r = lv["records"][str(i)]
            S_, Y_, xx, yy = selected[str(i)]
            dots = VGroup(*[Dot(sx.c2p(a, b), radius=0.025, color=SPOT) for a, b in zip(S_, Y_)])
            fit = curve(sx, xx, yy, OPT, stroke_width=3)
            parts = VGroup(dots, fit)
            if np.isfinite(bnd[i]):
                parts.add(Dot(sx.c2p(bnd[i], 100 - bnd[i]), radius=0.08, color=QC.DELTA))
            tag = MathTex(rf"t = {t[i]:.2f}", font_size=26, color=QC.DELTA).next_to(s, UP, buff=0.1)
            return VGroup(parts, tag)

        pts = VGroup()
        for i in range(n - 1, 0, -1):
            if np.isfinite(bnd[i]):
                pts.add(Dot(ax.c2p(t[i], bnd[i]), radius=0.06, color=QC.DELTA))
        leg = legend([(SPOT, r"in-the-money paths: realised future"), (OPT, r"cubic fit: expected future"),
                      (BAD, r"exercise now: $K - S$"), (QC.DELTA, r"exercise boundary, date by date"),
                      (WHITE, r"the 2{,}000-step tree's boundary")], font_size=15).to_edge(UP, buff=0.25).to_edge(RIGHT, buff=0.4)
        src = illustration(r"American put, $S_0 = K = 100$, one year, 20\%, 5\%; 25 dates; 200{,}000 paths regressed, "
                           r"150 drawn; right panel: first 300 saved ITM observations per date", corner=DL)
        panel = date_panel(n - 1)
        with self.voiceover(
            "This put can exercise on twenty-five dates, so it is a Bermudan approximation to an American contract. The House simulates two hundred thousand fitting paths; the left panel shows one hundred and fifty without clipping. <bookmark mark='a'/> One date before expiry, take in-the-money paths and their realised discounted cash flows from waiting. The right panel shows the first three hundred saved observations at each date. A cubic regression estimates continuation; exercise where immediate payoff exceeds the fit. The polynomial is drawn over the observed spot range. <bookmark mark='b'/> Step backward and update cash flows under the fitted rule. The common axes retain all selected observations and fitted values, including tails. <bookmark mark='c'/> The dashed continuous-exercise tree boundary is a comparison from a different exercise schedule, rather than exact truth for this twenty-five-date policy. Sparse exercise-region observations, basis choice and Monte Carlo noise all affect the fitted boundary."
        ) as vo:
            self.play(FadeIn(g), FadeIn(fan), FadeIn(strike), FadeIn(src), FadeIn(s), Create(pay), FadeIn(leg[2]))
            vo.wait_until("a")
            self.play(FadeIn(cur_line), cursor.animate.set_value(t[n - 1]), FadeIn(panel), FadeIn(leg[:2]),
                      FadeIn(leg[3]))
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            k = 1
            for i in range(n - 2, 0, -1):
                new = date_panel(i)
                anims = [cursor.animate.set_value(t[i]), Transform(panel, new)]
                if np.isfinite(bnd[i]) and k < len(pts):
                    anims.append(FadeIn(pts[k]))
                    k += 1
                self.play(*anims, run_time=0.5 if i < 20 else 0.9)
            vo.wait_until("c")
            self.play(Create(tree), FadeIn(leg[4]))
        cur_line.clear_updaters()
        self.wait(0.5)
        self.clear_scene()

    def proof(self):
        rows = [
            cmath(r"V_{t_i}", r"=", r"\max\Big(h_{t_i},\ \mathbb{E}\big[e^{-r\Delta t}V_{t_{i+1}} \mid S_{t_i}\big]\Big),"
                  r"\quad V_{t_N} = h_{t_N}", font_size=32, colors={r"V_{t_i}": OPT}),
            cmath(r"\mathbb{E}[Y \mid S]", r"=", r"\arg\min_g \mathbb{E}\big(Y - g(S)\big)^2\ \approx\ "
                  r"\sum_k \hat\beta_k\psi_k(S),\ \ \hat\beta = \Psi^+Y", font_size=30),
            cmath(r"Y", r"=", r"\text{the realised cash flow along the policy, not } \max(h, \hat C)", font_size=30,
                  colors={r"Y": GOOD}),
            cmath(r"\mathbb{E}\big[e^{-r\tau}h_\tau\big]", r"\le", r"V_0\quad\text{for any stopping rule }\tau", font_size=34),
        ]
        whys = [why(r"the Snell envelope by dynamic programming (Part 8): stop, or continue at the conditional "
                    r"expectation of tomorrow's value"),
                why(r"a conditional expectation is the best predictor in mean square, so estimate it by least squares on "
                    r"a basis $\psi_k$ (here $1, s, s^2, s^3$)"),
                why(r"Longstaff and Schwartz: the regression only decides, the payoff is realised; Tsitsiklis and Van "
                    r"Roy inspired the value-regression comparison here; maximising noisy value estimates can create upward bias"),
                why(r"the fitted rule is a strategy, so its value is a lower bound; evaluate it on fresh paths to remove "
                    r"the foresight of fitting and judging on the same paths. Cl\'ement, Lamberton and Protter (2002): "
                    r"consistency requires suitable basis approximation, moments and sample-growth conditions")]
        step = ladder(self, rows, whys, keep=4, top=3.2, x=-0.8, buff=0.42, edge=6.9)
        with self.voiceover(
            "On these finite dates, dynamic programming gives the Snell envelope. Conditioning on spot is valid here because spot is the Markov state; regression theory also requires suitable square-integrable variables. <bookmark mark='a'/> Conditional expectation is the best mean-square predictor. A basis approximation is fitted by least squares, written with a pseudoinverse to allow rank deficiency. <bookmark mark='b'/> Longstaff–Schwartz uses realised policy cash flows as regression targets. Our separate value-regression illustration can introduce upward bias by maximising noisy values; this is not a universal verdict on every Tsitsiklis–Van Roy algorithm. <bookmark mark='c'/> Conditional on a fixed fitted policy, its expected discounted payoff is no greater than the optimal value. A fresh-path Monte Carlo estimate still has sampling error and can lie above the reference. In-sample fitting means have no such lower-bound guarantee. Consistency as basis and sample sizes grow requires additional conditions."
        ) as vo:
            for i, mk in enumerate("abc"):
                step(i)
                vo.wait_until(mk)
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def sweep(self, lv, a, br):
        sw = lv["sweep"]
        ref = br["price"][-1]
        up = a["ab"][-1]["upper"]
        yr = data_range(*sw.values(), [ref, up])
        g = axes([2.8, 5.2], yr, x_length=7.0, y_length=4.4, xlabel=r"paths used to fit the regression",
                 ylabel=r"fresh-path policy estimate (expectation is a lower bound)", xticks=[3, 4, 5],
                 xfmt=lambda v: f"10^{{{int(v)}}}", yticks=[5.95, 6.0, 6.05, 6.1], font_size=15)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        xs = np.array([3.0, 4.0, 5.0])
        bands = VGroup()
        for dg in range(1, 6):
            runs = np.array([sw[f"{dg}_{n}"] for n in (1000, 10000, 100000)]).T
            bands.add(seed_band(ax, xs, runs, DEG_COL[dg], stroke_width=3, opacity=0.12))
        refl = DashedLine(ax.c2p(2.8, ref), ax.c2p(5.2, ref), stroke_color=WHITE, stroke_width=2)
        upl = DashedLine(ax.c2p(2.8, up), ax.c2p(5.2, up), stroke_color=BAD, stroke_width=2)
        leg = legend([(DEG_COL[d], rf"degree {d}") for d in range(1, 6)] +
                     [(WHITE, rf"Bermudan reference (tree): {ref:.3f}"), (BAD, rf"dual upper estimate (ch.\ 9): {up:.3f}")],
                     font_size=15).next_to(g, RIGHT, buff=0.25).align_to(g, UP)
        ev, se = lv["eval"]
        tvr = lv["tvr_in"]
        side = VGroup(
            MathTex(rf"\text{{in-sample}}\ {lv['price_in']:.3f};\ \text{{fresh paths}}\ {ev:.3f} \pm {se:.3f}", font_size=24,
                    color=GOOD),
            MathTex(rf"\text{{value-regression variant, in-sample:}}\ {tvr:.3f}", font_size=24,
                    color=BAD if tvr > ref else GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(leg, DOWN, buff=0.4).align_to(leg, LEFT)
        q = predict(r"Why regress only on in-the-money paths?", width=4.4, font_size=21).to_corner(DR, buff=0.3)
        lin = np.mean(sw["1_100000"])
        best = max(range(1, 6), key=lambda d: np.mean(sw[f"{d}_100000"]))
        best1 = max(range(1, 6), key=lambda d: np.mean(sw[f"{d}_1000"]))
        src = illustration(r"five-seed min--max bands; the same 100{,}000 evaluation paths reused across fits", corner=UR)
        with self.voiceover(
            f"Each training size and polynomial degree has five fitted seeds. All policies share the same evaluation paths, independent of fitting but reused across comparisons; these are not an untouched final holdout. Bands show seed minima and maxima, not confidence intervals. <bookmark mark='a'/> The degree-one mean is {lin:.3f}. The best displayed degree at one hundred thousand fitting paths is {best}, and at one thousand it is {best1}; finite comparisons do not identify a proven optimal degree. The reference {ref:.3f} uses a five-thousand-step tree with the same twenty-five exercise dates. <bookmark mark='b'/> The separate two-hundred-thousand-path fit evaluated on four hundred thousand fresh paths gives {ev:.3f} plus or minus one estimated standard error, {se:.3f}. The value-regression variant has in-sample mean {tvr:.3f}; it illustrates sensitivity to regression targets, rather than certifying an ordering of algorithms. <bookmark mark='c'/> Why fit only in the money? For this nonnegative put, an out-of-the-money state does not strictly benefit from immediate exercise, so focus fitting on the exercise decision region. Next, dual upper expectations and their noisy estimates."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(refl), FadeIn(leg[5]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bands], lag_ratio=0.4, run_time=3), FadeIn(leg[:5]))
            vo.wait_until("b")
            self.play(FadeIn(upl), FadeIn(leg[6]), FadeIn(side))
            vo.wait_until("c")
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
