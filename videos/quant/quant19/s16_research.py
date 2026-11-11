from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant19.common import FWD, GOOD, PART, POLICY, SHORT, VAS, ZERO, load

S_COL = {"-0.03": QC.LOSS, "-0.01": QC.THETA, "0": FWD, "0.01": VAS, "0.03": GOOD}


class Research(VoiceoverScene):
    def construct(self):
        t = load("shadow_theory")
        self.card()
        self.black()
        self.wuxia()
        self.derive()
        self.check(t)
        self.premium(t)
        self.sensitivity(t)
        self.treasury(t)
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"The zero lower bound and the shadow rate", r"How does a term-structure model respect a floor "
                          r"on rates, and what does the floor do to the curve?", part=PART)
        with self.voiceover("For the researcher: Chapter 6 let rates go negative and switched to Bachelier. But from 2009 "
                            "to 2015 American rates sat at zero for years, and Gaussian models put large probability on "
                            "rates far below it. Here is the model that respects a floor, the approximation that makes it "
                            "practical, and what the floor did to the Treasury curve."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def black(self):
        rows = [cmath(r"r_t", r"=", r"\max(s_t, r_{\min}),\qquad ds_t = \kappa(\theta - s_t)\,dt + \sigma\,dW_t^{\mathbb Q}",
                      font_size=30, colors={r"r_t": SHORT}),
                cmath(r"P(t, T)", r"=", r"\mathbb E^{\mathbb Q}_t\Big[e^{-\int_t^T \max(s_u, r_{\min})\,du}\Big]", font_size=32,
                      colors={r"P(t, T)": ZERO}),
                cmath(r"\partial_\tau P", r"=", r"\kappa(\theta - s)\,\partial_s P + \tfrac12\sigma^2\partial_{ss}P - \max(s, "
                      r"r_{\min})\,P", font_size=30, colors={r"\partial_\tau P": ZERO})]
        whys = [why(r"Black (1995): a shadow rate $s$ moves freely, Gaussian here; the short rate is $\max(s,r_{\min})$, using an effective floor; "
                    r"the floor need not be zero"),
                why(r"bond prices are no longer exponential-affine in the state: the floor is an option, and it makes "
                    r"the model nonlinear"),
                why(r"one state gives a one-dimensional pricing PDE; several states require a larger numerical problem, and "
                    r"an approximation may reduce its cost")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Black's 1995 shadow-rate idea imposes a lower bound through an option-like payoff. <bookmark mark='a'/> Let a Gaussian shadow rate move freely, but set the observable short rate to the maximum of that state and a chosen floor. A zero floor is an idealization; storage, transactions, institutional constraints and policy can make the effective bound negative or variable. <bookmark mark='b'/> Bond prices still discount the actual floored rate under a pricing measure. Because the discount-rate function is nonlinear, the familiar exponential-affine bond formula no longer applies. <bookmark mark='c'/> One factor leads to a one-dimensional pricing PDE. We solve it numerically with finite boundaries and steps, not exactly. Multiple factors still admit higher-dimensional pricing equations; computational cost grows, making approximations or other numerical methods useful."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def wuxia(self):
        rows = [cmath(r"f_t(n)", r"\approx", r"r_{\min} + \sigma_n\,g\Big(\frac{a_n - r_{\min}}{\sigma_n}\Big),\qquad g(z) = "
                      r"z\Phi(z) + \varphi(z)", font_size=30, colors={r"f_t(n)": FWD}),
                cmath(r"a_n", r"=", r"\theta + (s_t - \theta)e^{-\kappa n} - \frac{\sigma^2}{2\kappa^2}\big(1 - e^{-\kappa n}\big)^2",
                      font_size=30, colors={r"a_n": VAS}),
                cmath(r"\frac{\partial f_t(n)}{\partial s_t}", r"\approx", r"\Phi(z_n)\,e^{-\kappa n}", font_size=32,
                      colors={r"\frac{\partial f_t(n)}{\partial s_t}": POLICY})]
        whys = [why(r"Wu and Xia (2016): the forward rate is approximately the floor plus a normal-call expectation; $g$ is Bachelier's "
                    r"call (Chapter 6) per unit of volatility, and $\sigma_n^2 = \sigma^2(1 - e^{-2\kappa n})/(2\kappa)$"),
                why(r"the shadow model's own forward: its expected rate less the Gaussian convexity term"),
                why(r"since $g'(z) = \Phi(z)$: deep below the floor ($z \ll 0$) forward rates stop responding to the "
                    r"shadow rate, exactly as an option far out of the money stops responding to its underlying")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The Wu-Xia style approximation uses a Gaussian shadow-model forward calculation to approximate the floored model's forward rate. Its accuracy depends on the model and parameter region. <bookmark mark='a'/> The displayed forward is approximately the floor plus a normal-call expectation, with g of z equal to z Phi of z plus the standard normal density. Here sigma n is a conditional standard deviation at the horizon, not an annualized volatility quote. <bookmark mark='b'/> The mean a n is the unfloored Vasicek forward-measure mean, including its Gaussian convexity correction. Substituting that distribution into the floored model is the approximation. <bookmark mark='c'/> Holding the parameters and variance fixed, the derivative of g is Phi. The approximate forward's sensitivity to today's shadow state is Phi of z times exponential minus kappa n. This is a local derivative, not an exact formula for a large finite policy move."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"f_t(n)", r"=", r"\mathbb E^{\mathbb Q^{t+n}}_t\big[r_{t+n}\big]", font_size=32, colors={r"f_t(n)": FWD}),
                cmath(r"\phantom{f_t(n)}", r"=", r"r_{\min} + \mathbb E^{\mathbb Q^{t+n}}_t\big[(s_{t+n} - r_{\min})^+\big]",
                      font_size=32),
                cmath(r"s_{t+n}", r"\overset{\text{approx}}{\sim}", r"N\big(a_n, \sigma_n^2\big)\ \Rightarrow\ "
                      r"\mathbb E[(s - r_{\min})^+] = \sigma_n\,g\Big(\frac{a_n - r_{\min}}{\sigma_n}\Big)", font_size=28,
                      colors={r"s_{t+n}": VAS})]
        whys = [why(r"an instantaneous forward rate is the expected future short rate under the forward measure for that "
                    r"date (the forward measure of chapter 5's caplets)"),
                why(r"and $\max(s, r_{\min}) = r_{\min} + (s - r_{\min})^+$: the floor plus a call on the shadow rate"),
                why(r"the approximation: under that measure, treat $s$ as Gaussian with the shadow model's forward and "
                    r"variance, ignoring how the floor itself tilts the measure; then the call is Bachelier's")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Start with a regular short-rate pricing model. <bookmark mark='a'/> Its instantaneous forward for a maturity date equals the expected short rate at that date under the corresponding bond-forward measure. That measure is determined by the actual floored model. <bookmark mark='b'/> Write the short rate as the floor plus the positive part of the shadow rate minus the floor. If that shadow state were Gaussian under this measure, a normal-call expectation would give the displayed formula. <bookmark mark='c'/> The approximation replaces its generally non-Gaussian floored-model distribution with the unfloored Gaussian model's forward-measure mean and variance. The floor changes bond prices and therefore changes the measure tilt. Ignoring that effect creates model-dependent error, which need not grow monotonically with maturity. A one-factor numerical benchmark can measure it for the chosen parameters, but does not establish universal accuracy."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def check(self, t):
        taus = np.asarray(t["taus"], float)
        g = axes([0, 10.3], [-3.2, 4.0], x_length=8.0, y_length=4.3, xlabel=r"maturity $n$, years",
                 ylabel=r"instantaneous forward rate, \%", xticks=[0, 2, 4, 6, 8, 10], yticks=[-3, -2, -1, 0, 1, 2, 3, 4],
                 font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(10.3, 0), color=GREY_C, stroke_width=1.5)
        sh, ex, wx = VGroup(), VGroup(), VGroup()
        for k in ("-0.03", "-0.01", "0.01"):
            r = t["rows"][k]
            col = S_COL[k]
            sh.add(DashedVMobject(curve(ax, taus, 100 * np.asarray(r["shadow"]), col, stroke_width=2), num_dashes=24))
            ex.add(curve(ax, taus, 100 * np.asarray(r["exact"]), col, stroke_width=3.5))
            wx.add(VGroup(*[Dot(ax.c2p(a_, 100 * b_), radius=0.06, color=WHITE) for a_, b_ in zip(taus, r["wu_xia"])]))
        leg = legend([(S_COL[k], rf"shadow rate today {100 * float(k):+.0f}\%") for k in ("-0.03", "-0.01", "0.01")]
                     + [(WHITE, r"Wu--Xia approximation")], font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        r3 = t["rows"]["-0.03"]
        err = max(abs(a_ - b_) for k in t["rows"] for a_, b_ in zip(t["rows"][k]["exact"], t["rows"][k]["wu_xia"]))
        err_bp = 1e4 * err
        side = wrapped_label(rf"$\kappa = {t['kappa']}$, $\theta = {100 * t['theta']:.0f}\%$, $\sigma = "
                             rf"{100 * t['sigma']:.1f}\%$, floor 0; solid: finite-difference benchmark in $s$; dashed: the "
                             rf"shadow model's own forwards; the largest gap, {1e4 * err:.0f} bp, at ten years", 3.3, 14,
                             GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"Compare the approximation with this one-factor finite-difference benchmark. <bookmark mark='a'/> Dashed lines show the unfloored shadow model's forwards, which may be negative. <bookmark mark='b'/> Solid lines come from numerical bond prices with the floor. The pricing equation is exact for the model, but its finite-grid solution and forward differentiation are approximate. <bookmark mark='c'/> Across the displayed state and maturity grid, the largest approximation-to-benchmark difference is about {err_bp:.0f} basis points. This measures agreement in this example, not the benchmark's total numerical error or the accuracy of a multi-factor market fit. The saved benchmark uses fixed finite boundaries and a daily time step, so independent grid and boundary convergence checks would be needed for stronger precision claims."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(side))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c_) for c_ in sh], lag_ratio=0.3), FadeIn(leg[:3]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c_) for c_ in ex], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(wx), FadeIn(leg[3]))
        self.wait(0.4)
        self.clear_scene()

    def premium(self, t):
        taus = list(t["taus"])
        picks = [taus.index(x) for x in (1, 2, 5, 10)]
        hx = [-4.6, -2.2, 0.2, 2.6, 5.0]
        head = VGroup(label(r"shadow rate today", font_size=18, color=GREY_B),
                      *[label(rf"{taus[i]:g} years", font_size=20) for i in picks])
        tab = VGroup(head)
        for k in ("-0.03", "-0.01", "0.01"):
            r = t["rows"][k]
            tab.add(VGroup(label(rf"{100 * float(k):+.0f}\%", font_size=20, color=S_COL[k]),
                           *[MathTex(rf"+{1e4 * (r['exact'][i] - r['shadow'][i]):.0f}", font_size=26) for i in picks]))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.5 - 0.75 * j, 0])
        foot = wrapped_label(r"floor adjustment: numerical forward rate less the shadow model's forward, in basis points. "
                             r"Black's reading: the right to hold cash at the floor is an option, and forward rates pay for "
                             r"it; the premium is largest where the shadow rate is most likely to be below the floor", 11.6,
                             16, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "What is the floor worth? <bookmark mark='a'/> Subtract the shadow model's forward rate from the exact one. "
            "With the shadow rate at minus three percent, the floor adds two hundred basis points to the one-year "
            "forward, and still forty at ten years. Even with the shadow rate at plus one percent, ten to twenty. "
            "<bookmark mark='b'/> Black's reading: the right to hold cash rather than lend below the floor is an option "
            "held by every lender, and forward rates pay for it, most where the shadow rate is most likely to be "
            "beneath the floor."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def sensitivity(self, t):
        mb = t["model_beta"]
        s = 100 * np.array([b["s"] for b in mb])
        ratio = np.array([b["ratio"] for b in mb])
        rel = ratio / ratio[-1]
        g = axes([-5, 5], [0, 1.1], x_length=8.0, y_length=4.0, xlabel=r"shadow rate today, \%",
                 ylabel=r"response of the 1-year yield to the 10-year, relative to normal times", xticks=[-4, -2, 0, 2, 4],
                 yticks=[0, 0.5, 1.0], font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        c_ = curve(ax, s, rel, POLICY, stroke_width=3.5)
        side = wrapped_label(r"in the one-factor shadow model: the ratio of the 1-year and 10-year yields' sensitivities to "
                             r"the shadow rate, divided by its value at $s = 5\%$. Below about $-2\%$, the short end is "
                             r"almost dead", 3.3, 14, GREY_A).to_edge(RIGHT, buff=0.3).shift(UP * 1.0)
        fit_right(side)
        with self.voiceover(
            "The chosen one-factor model predicts reduced local sensitivity near its floor. <bookmark mark='a'/> The plotted response compares the one-year and ten-year zero yields as the shadow state changes, with parameters held fixed. At a shadow rate near minus two and a half percent, that ratio is about a tenth of its higher-state reference in this numerical example. A zero yield is an average of forwards, so its derivative averages the forward sensitivities over maturity. These statements concern this pricing model and this state shock; they do not imply that all economic news affects only the shadow state, or that a long yield is unaffected by the bound."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(c_), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def treasury(self, t):
        yrs = t["treasury"]
        x = np.array([y["year"] for y in yrs], float)
        b = np.array([y["beta"] for y in yrs])
        y1 = np.array([y["y1"] for y in yrs])
        g = axes([1989.5, 2019.5], [0, 1.0], x_length=8.0, y_length=4.0, xlabel=r"year",
                 ylabel=r"slope of daily 1-year changes on 10-year changes", xticks=[1990, 2000, 2010, 2019],
                 yticks=[0, 0.25, 0.5, 0.75, 1.0], xfmt=lambda v: f"{v:.0f}", font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        zlb = Rectangle(width=ax.c2p(2015.9, 0)[0] - ax.c2p(2008.9, 0)[0], height=ax.c2p(0, 1.0)[1] - ax.c2p(0, 0)[1],
                        stroke_width=0, fill_color=GREY_D, fill_opacity=0.5).move_to(ax.c2p(2012.4, 0.5))
        zl = label(r"rates at the floor", font_size=14, color=GREY_B).next_to(zlb, UP, buff=0.05)
        bars = VGroup()
        w = ax.c2p(0.7, 0)[0] - ax.c2p(0, 0)[0]
        for xi, bi in zip(x, b):
            p0, p1 = ax.c2p(xi, 0), ax.c2p(xi, max(bi, 0.005))
            bars.add(Rectangle(width=w, height=p1[1] - p0[1], stroke_width=0, fill_color=POLICY, fill_opacity=0.85).move_to(
                (p0 + p1) / 2))
        pre = b[(x >= 1990) & (x <= 2007)].mean()
        zl_ = b[(x >= 2010) & (x <= 2014)].mean()
        side = wrapped_label(rf"Gürkaynak, Sack and Wright's zero yields, daily changes, one regression a year. "
                             rf"1990--2007: {pre:.2f} on average; 2010--2014: {zl_:.2f}; the 1-year yield averaged "
                             rf"{y1[(x >= 2010) & (x <= 2014)].mean():.2f}\% then. Swanson and Williams (2014) studied "
                             r"macroeconomic-news responses in a different design", 3.3, 14, GREY_A).to_edge(
            RIGHT, buff=0.3).shift(UP * 0.6)
        fit_right(side)
        with self.voiceover(
            f"Now a descriptive Treasury-curve comparison. Each year, regress the daily change in the one-year zero yield on the change in the ten-year zero yield. <bookmark mark='a'/> The average of those annual slopes is {pre:.2f} over 1990 to 2007. <bookmark mark='b'/> It falls to {zl_:.2f} over 2010 to 2014, when short yields were low. This is consistent with a constrained short end, but the regression mixes shocks, policy regimes and changing risk premia; it does not identify the shadow-rate mechanism. <bookmark mark='c'/> The slope later recovers. Swanson and Williams's 2014 study used responses to macroeconomic news, a different design. Our unconditional daily co-movement regression does not reproduce their event-study estimates or establish that every maturity responded in the same way."
        ) as vo:
            self.play(FadeIn(g), FadeIn(zlb), FadeIn(zl), FadeIn(side))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bars[:18]], lag_ratio=0.05))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bars[18:25]], lag_ratio=0.1))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bars[25:]], lag_ratio=0.1))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: is the shadow rate a policy stance?", r"estimated shadow rates differ by several points "
                          r"across models and samples (Krippner 2020); whether they measure the stance of unconventional "
                          r"policy is disputed", width=12.4, font_size=18),
            desk_question(r"open: where is the floor?", r"negative policy rates in Europe and Japan showed the lower bound "
                          r"is not zero and may move; models with a floor that is itself uncertain are young", width=12.4,
                          font_size=18),
            desk_question(r"open: options near the floor", r"caps, floors and swaptions near the bound need the whole "
                          r"distribution, not just its mean; joint fits of the curve and its options in shadow models "
                          r"are hard to make stable", width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> Estimated shadow rates differ by several points across models "
            "and samples, and whether they measure the stance of unconventional policy is disputed. "
            "<bookmark mark='b'/> Negative policy rates in Europe and Japan showed that the floor is not zero, and may "
            "move; models with an uncertain floor are young. <bookmark mark='c'/> And options near the bound depend on "
            "the whole distribution; joint fits of the curve and its options in shadow models are hard to make stable."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"with the shadow forward at $a_n = -1\%$ and $\sigma_n = 1\%$, what is the Wu--Xia forward rate, "
                       r"and how much does it move if the shadow rate falls another 50 bp ($e^{-\kappa n} = 0.8$)?")
        with self.voiceover(
            "Pause and predict. With the shadow forward at minus one percent and its volatility at one percent, what is "
            "the forward rate? And how much does it move if the shadow rate falls another fifty basis points?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
        answer = VGroup(
            label(r"Zero floor; keep the horizon variance fixed", font_size=30),
            MathTex(r"z=-1,\quad f=0.01[\phi(1)-\Phi(-1)]=0.000833\approx8.33\ \mathrm{bp}", font_size=34),
            MathTex(r"\Delta s=-50\ \mathrm{bp}:\quad \Delta f_{\mathrm{linear}}=\Phi(-1)\times0.8\times(-50)=-6.35\ \mathrm{bp}", font_size=30),
            MathTex(r"a_{\mathrm{new}}=-1.4\%,\quad f_{\mathrm{new}}=3.67\ \mathrm{bp},\quad \Delta f=-4.66\ \mathrm{bp}", font_size=32),
            wrapped_label(r"a 50-bp shadow-state move is not infinitesimal; the local derivative overstates this decline", 11.8, 23, GREY_A),
        ).arrange(DOWN, buff=0.5)
        with self.voiceover("With a zero floor, z is minus one. The normal-call expectation gives eight point three three basis points. <bookmark mark='a'/> The local derivative predicts a decline of six point three five basis points for a fifty-basis-point drop in today's shadow state, using the given loading of point eight. <bookmark mark='b'/> For the actual finite move, the horizon mean becomes minus one point four percent while its variance stays fixed. Recomputing the formula gives three point six seven basis points, a decline of four point six six. The local approximation and the finite change differ because the sensitivity itself falls as the state moves deeper below the floor.") as vo:
            self.play(FadeIn(answer[0]), FadeIn(answer[1]))
            vo.wait_until("a"); self.play(FadeIn(answer[2]))
            vo.wait_until("b"); self.play(FadeIn(answer[3]), FadeIn(answer[4]))
        self.wait(0.4)
        self.clear_scene()
