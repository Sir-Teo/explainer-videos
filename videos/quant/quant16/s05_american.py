from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, GOOD, OPT, PART, SPOT, illustration, load, polyline, predict

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
        c = chapter_card(8, r"American options I: Longstaff--Schwartz on real paths", r"How do you decide when to "
                         r"exercise with only paths?", lit=(2001,), part=PART)
        with self.voiceover("Chapter eight. American options, part one: Longstaff and Schwartz, run on real paths."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def backward(self, lv):
        K, n = 100.0, 25
        t = np.linspace(0, 1, n + 1)
        P = np.asarray(lv["paths"])
        g = axes([0, 1], [60, 140], x_length=6.4, y_length=4.6, xlabel=r"time (years)", ylabel=r"stock price",
                 xticks=[0, 0.5, 1], yticks=[70, 100, 130], font_size=15).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        fan = path_fan(ax, t, np.clip(P[:150], 60, 140), color=SPOT, opacity=0.18, stroke_width=1)
        strike = DashedLine(ax.c2p(0, K), ax.c2p(1, K), stroke_color=GREY_B, stroke_width=1.5)
        tb_t, tb_b = np.asarray(lv["tree_t"]), np.asarray(lv["tree_b"])
        ok = np.isfinite(tb_b)
        tree = DashedVMobject(polyline(ax, tb_t[ok], np.clip(tb_b[ok], 60, 140), WHITE, stroke_width=2, dots=False)[0],
                              num_dashes=40)
        bnd = np.asarray(lv["boundary"], float)
        cursor = ValueTracker(1.0)
        cur_line = always_redraw(lambda: Line(ax.c2p(cursor.get_value(), 60), ax.c2p(cursor.get_value(), 140),
                                              stroke_color=QC.DELTA, stroke_width=2))
        s = axes([60, 100], [0, 40], x_length=4.6, y_length=3.4, xlabel=r"spot at this date (in the money)",
                 ylabel=r"realised discounted cash flow", xticks=[70, 85, 100], yticks=[0, 20, 40], font_size=14)
        s.to_edge(RIGHT, buff=0.5).shift(DOWN * 0.3)
        sx = s.ax
        pay = curve(sx, np.linspace(60, 100, 40), 100 - np.linspace(60, 100, 40), BAD, stroke_width=2.5)

        def date_panel(i):
            r = lv["records"][str(i)]
            S_, Y_ = np.asarray(r["S"]), np.asarray(r["Y"])
            keep = (S_ > 60)
            S_, Y_ = S_[keep][:600], Y_[keep][:600]
            dots = VGroup(*[Dot(sx.c2p(a, min(b, 40)), radius=0.025, color=SPOT) for a, b in zip(S_, Y_)])
            xx = np.linspace(max(60, S_.min() if len(S_) else 60), 100, 60)
            fit = curve(sx, xx, np.clip(np.polyval(r["coef"], xx / K), 0, 40), OPT, stroke_width=3)
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
                           r"150 drawn", corner=DL)
        panel = date_panel(n - 1)
        with self.voiceover(
            "Monte Carlo runs forward in time, but exercise decisions are made backward: to decide today you need "
            "the value of waiting. Here are real paths of the American put from the House's run, two hundred thousand "
            "regressed and a hundred and fifty drawn, with twenty-five exercise dates. <bookmark mark='a'/> Start "
            "one date before expiry. Take the paths that are in the money, and plot what each one actually earned by "
            "waiting, discounted. Regress those numbers on a cubic in today's price: the fitted curve estimates the "
            "value of continuing. Where the payoff of exercising beats the curve, exercise. The crossing is that "
            "date's boundary. <bookmark mark='b'/> Then step back a date, and repeat with the updated cash flows. "
            "Date by date the boundary traces a curve back toward today. <bookmark mark='c'/> Dashed, the "
            "boundary of a fine binomial tree: close, slightly higher early on, where few paths are in the money to "
            "teach the regression."
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
                  r"\sum_k \hat\beta_k\psi_k(S),\ \ \hat\beta = (\Psi^\top\Psi)^{-1}\Psi^\top Y", font_size=30),
            cmath(r"Y", r"=", r"\text{the realised cash flow along the policy, not } \max(h, \hat C)", font_size=30,
                  colors={r"Y": GOOD}),
            cmath(r"\mathbb{E}\big[e^{-r\tau}h_\tau\big]", r"\le", r"V_0\quad\text{for any stopping rule }\tau", font_size=34),
        ]
        whys = [why(r"the Snell envelope by dynamic programming (Part 8): stop, or continue at the conditional "
                    r"expectation of tomorrow's value"),
                why(r"a conditional expectation is the best predictor in mean square, so estimate it by least squares on "
                    r"a basis $\psi_k$ (here $1, s, s^2, s^3$)"),
                why(r"Longstaff and Schwartz: the regression only decides, the payoff is realised; Tsitsiklis and Van "
                    r"Roy regress the estimated value, which is biased high"),
                why(r"the fitted rule is a strategy, so its value is a lower bound; evaluate it on fresh paths to remove "
                    r"the foresight of fitting and judging on the same paths. Cl\'ement, Lamberton and Protter (2002): "
                    r"it converges as basis and paths grow")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.8, buff=0.6, edge=6.9)
        with self.voiceover(
            "In symbols. The option's value is the Snell envelope of Part eight: at each date, the larger of "
            "exercising and the expected discounted value of tomorrow. <bookmark mark='a'/> A conditional "
            "expectation is the best predictor in mean square, so it can be estimated by least squares on a few basis "
            "functions of today's price. <bookmark mark='b'/> The subtle choice: regress the cash flow the policy "
            "actually realises. Tsitsiklis and Van Roy, the same year, regressed the estimated value instead, the "
            "maximum of payoff and fit, and the maximum of noisy numbers is biased upward. <bookmark mark='c'/> And "
            "because the fitted rule is a genuine strategy, its value is a lower bound, provided we judge it on fresh "
            "paths it was not fitted to."
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
        g = axes([2.8, 5.2], [5.9, 6.12], x_length=7.0, y_length=4.4, xlabel=r"paths used to fit the regression",
                 ylabel=r"out-of-sample value of the policy (lower bound)", xticks=[3, 4, 5],
                 xfmt=lambda v: f"10^{{{int(v)}}}", yticks=[5.95, 6.0, 6.05, 6.1], font_size=15)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        xs = np.array([3.0, 4.0, 5.0])
        bands = VGroup()
        for dg in range(1, 6):
            runs = np.array([sw[f"{dg}_{n}"] for n in (1000, 10000, 100000)]).T
            bands.add(seed_band(ax, xs, np.clip(runs, 5.9, 6.12), DEG_COL[dg], stroke_width=3, opacity=0.12))
        refl = DashedLine(ax.c2p(2.8, ref), ax.c2p(5.2, ref), stroke_color=WHITE, stroke_width=2)
        upl = DashedLine(ax.c2p(2.8, up), ax.c2p(5.2, up), stroke_color=BAD, stroke_width=2)
        leg = legend([(DEG_COL[d], rf"degree {d}") for d in range(1, 6)] +
                     [(WHITE, rf"Bermudan reference (tree): {ref:.3f}"), (BAD, rf"dual upper bound (ch.\ 9): {up:.3f}")],
                     font_size=15).next_to(g, RIGHT, buff=0.25).align_to(g, UP)
        ev, se = lv["eval"]
        tvr = lv["tvr_in"]
        side = VGroup(
            MathTex(rf"\text{{in-sample}}\ {lv['price_in']:.3f};\ \text{{fresh paths}}\ {ev:.3f} \pm {se:.3f}", font_size=24,
                    color=GOOD),
            MathTex(rf"\text{{regress the value (TvR), in-sample:}}\ {tvr:.3f}", font_size=24,
                    color=BAD if tvr > ref else GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(leg, DOWN, buff=0.4).align_to(leg, LEFT)
        q = predict(r"Why regress only on in-the-money paths?", width=4.4, font_size=21).to_corner(DR, buff=0.3)
        lin = np.mean(sw["1_100000"])
        best = max(range(1, 6), key=lambda d: np.mean(sw[f"{d}_100000"]))
        best1 = max(range(1, 6), key=lambda d: np.mean(sw[f"{d}_1000"]))
        src = illustration(r"each band: five seeds, judged on 100{,}000 fresh paths", corner=UR)
        with self.voiceover(
            "How good is the rule? Fit it with a thousand, ten thousand or a hundred thousand paths, with polynomials "
            "of degree one to five, five seeds each, and judge every fitted rule on a hundred thousand fresh paths. "
            "<bookmark mark='a'/> A straight line is not enough: it plateaus near "
            f"{lin:.3f}. Cubics and above, with a hundred thousand paths, reach the Bermudan reference of "
            f"{ref:.3f} from a two-thousand-five-hundred-step tree that may exercise only on the twenty-five dates; "
            f"the best here is degree {best}. With only a thousand paths the best is degree {best1}: higher degrees "
            "overfit. "
            "<bookmark mark='b'/> The full run, two hundred thousand paths judged on four hundred thousand fresh ones, "
            f"gives {ev:.3f} plus or minus {se:.3f}. Regressing the value instead, the Tsitsiklis–Van Roy way, gives "
            f"{tvr:.3f} in sample: {'above' if tvr > ref else 'below'} the true price, as the theory warned. "
            "<bookmark mark='c'/> Pause and predict: why regress only on paths that are in the money? "
            "Out-of-the-money paths never exercise there, and fitting them would spend the basis on the wrong region."
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
