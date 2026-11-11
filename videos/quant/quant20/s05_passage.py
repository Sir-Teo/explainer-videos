from __future__ import annotations

from videos.quant.quant20.common import lesson_cards

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant20.common import ASSET, BAD, DEBT, PART, ask, fit_right, illustration, load


class Passage(VoiceoverScene):
    def construct(self):
        b = load("blackcox")
        self.card()
        self.paths(b)
        self.curves(b)
        self.leland()
        self.optimal(load("leland"))
        self.feedback()

    def card(self):
        c = chapter_card(4, r"First passage and the choice to default", r"What if default can come before maturity?",
                         part=PART)
        with self.voiceover("Chapter four. Default before maturity: first passage, and the firm's own choice."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def paths(self, b):
        rng = np.random.default_rng(3)
        T, n = 5.0, 250
        t = np.linspace(0, T, n + 1)
        sampled = [np.exp(np.log(b["V"]) + np.r_[0, np.cumsum((b["mu"]-.5*b["s"]**2)*(T/n)
                   + b["s"]*np.sqrt(T/n)*rng.standard_normal(n))]) for _ in range(14)]
        low, high = 0., float(np.ceil(max(np.max(v) for v in sampled)/50)*50+50)
        g = axes([0, 5], [low, high], x_length=7.6, y_length=4.4, xlabel=r"years", ylabel=r"asset value",
                 xticks=[0, 1, 2, 3, 4, 5], yticks=np.linspace(low, high, 5), font_size=14).to_edge(LEFT, buff=0.6).shift(
            DOWN * 0.3)
        ax = g.ax
        K = b["K"]
        bar = DashedLine(ax.c2p(0, K), ax.c2p(5, K), color=BAD, stroke_width=3)
        lines, hits = VGroup(), VGroup()
        for i in range(14):
            v = sampled[i]
            k = np.argmax(v <= K) if (v <= K).any() else None
            if k:
                lines.add(curve(ax, t[:k + 1], v[:k + 1], BAD, stroke_width=1.6).set_stroke(opacity=0.85))
                hits.add(Dot(ax.c2p(t[k], K), color=BAD, radius=0.06))
            else:
                lines.add(curve(ax, t, v, ASSET, stroke_width=1.4).set_stroke(opacity=0.6))
        side = VGroup(
            MathTex(rf"V_0 = {b['V']:.0f},\ \ \text{{barrier}}\ K = {K:.0f}", font_size=26),
            wrapped_label(r"Black and Cox (1976): bond covenants let creditors take control as soon as the assets touch "
                          r"a barrier, not only at maturity. Paths that touch it stop; Merton would let them recover",
                          3.8, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        fit_right(side)
        with self.voiceover(
            "Merton's firm can only default on one day, at maturity. Real bonds carry covenants: if the assets fall "
            "far enough, creditors can act at once. Fischer Black and John Cox, in 1976, made default the first time "
            "the assets touch a barrier. <bookmark mark='a'/> Fourteen paths of the same firm. The red ones touch the "
            "barrier and stop there; under Merton's rule, several of them would have recovered by maturity and never "
            "defaulted."
        ) as vo:
            self.play(FadeIn(g), Create(bar), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.12, run_time=4), FadeIn(hits),
                      FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()

    def curves(self, b):
        T, a, f = np.asarray(b["T"]), np.asarray(b["terminal"]) * 100, np.asarray(b["first"]) * 100
        rows = [cmath(r"\mathbb{P}(\tau \le T)", r"=", r"N\Big(\frac{\ln\frac{K}{V_0} - mT}{\sigma\sqrt T}\Big) + "
                      r"\Big(\frac{K}{V_0}\Big)^{2m/\sigma^2} N\Big(\frac{\ln\frac{K}{V_0} + mT}{\sigma\sqrt T}\Big)",
                      font_size=30, colors={r"\mathbb{P}(\tau \le T)": BAD})]
        hdr = rows[0].to_edge(UP, buff=0.5)
        g = axes([0, 10], [0, 60], x_length=7.0, y_length=3.8, xlabel=r"horizon, years", ylabel=r"default probability, \%",
                 xticks=[0, 2, 4, 6, 8, 10], yticks=[0, 20, 40, 60], font_size=14).to_edge(LEFT, buff=0.6).shift(
            DOWN * 0.8)
        ax = g.ax
        la = curve(ax, T, a, DEBT, stroke_width=3.5)
        lf = curve(ax, T, f, BAD, stroke_width=3.5)
        side = VGroup(
            legend([(DEBT, r"Merton: below $K$ at $T$"), (BAD, r"Black--Cox: touches $K$ before $T$")], font_size=17),
            MathTex(rf"\text{{10 years: }} {a[-1]:.0f}\%\ \text{{against}}\ {f[-1]:.0f}\%", font_size=26),
            wrapped_label(r"$m = \mu - \frac12\sigma^2$; the reflection principle (Part 5) gives the second term. "
                          r"Touching is always at least as likely as ending below", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35).shift(DOWN * 0.6)
        fit_right(side)
        with self.voiceover(
            f"For geometric Brownian assets and a constant barrier, the reflection principle gives a continuous-monitoring first-passage probability. It includes paths that touch the barrier and later recover. <bookmark mark='a'/> With the stated parameters, the ten-year terminal probability is {a[-1]:.0f} percent and the passage probability {f[-1]:.0f}. The sampled path drawing checks only discrete dates and can miss crossings; it is not the exact probability calculation. A fixed positive diffusion distance still makes very short-horizon default unlikely. CreditGrades adds uncertainty about the default boundary and other conventions, which can generate larger short spreads. That is a modeling response, not proof that every observed spread is explained."
        ) as vo:
            self.play(FadeIn(hdr), FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(la), Create(lf), FadeIn(side[1]), FadeIn(side[2]), run_time=2)
        self.add(illustration(rf"$V_0 = {b['V']:.0f}$, $K = {b['K']:.0f}$, $\sigma = {100 * b['s']:.0f}\%$, "
                              rf"$\mu = {100 * b['mu']:.0f}\%$"))
        self.wait(0.4)
        self.clear_scene()

    def optimal(self, L):
        C = np.asarray(L["C"])
        g = axes([0, 12], [0, 140], x_length=7.4, y_length=4.4, xlabel=r"coupon $C$ a year (assets 100)",
                 ylabel=r"value", xticks=[0, 3, 6, 9, 12], yticks=[0, 40, 80, 120], font_size=14).to_edge(LEFT, buff=0.6
                                                                                                   ).shift(DOWN * 0.3)
        ax = g.ax
        lf = curve(ax, C, np.asarray(L["firm"]), ASSET, stroke_width=3.5)
        ld = curve(ax, C, np.asarray(L["debt"]), DEBT, stroke_width=3)
        le = curve(ax, C, np.asarray(L["equity"]), QC.OPTION, stroke_width=3)
        o = L["opt"]
        star = Dot(ax.c2p(o["C"], max(L["firm"])), color=WHITE)
        side = VGroup(
            legend([(ASSET, r"firm value"), (DEBT, r"debt"), (QC.OPTION, r"equity")], font_size=17),
            MathTex(rf"C^* = {o['C']:.1f},\ \ \text{{leverage}} = {100 * o['lev']:.0f}\%", font_size=26),
            MathTex(rf"V_B = {o['VB']:.1f},\ \ \text{{spread}} = {o['spread_bp']:.0f}\ \text{{bp}}", font_size=24),
            wrapped_label(rf"taxes {100 * L['tax']:.0f}\%, bankruptcy costs {100 * L['alpha']:.0f}\% of the assets, "
                          rf"$\sigma$ = {100 * L['sigma']:.0f}\%, $r$ = {100 * L['r']:.0f}\%. Debt adds the tax shield "
                          r"until expected default costs dominate. Firm-value and debt-value maxima occur at different coupons", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"Run the perpetual Leland illustration with initial assets of one hundred and the displayed fixed inputs. <bookmark mark='a'/> Increasing the coupon initially increases the tax benefit and debt value. <bookmark mark='b'/> It also raises the endogenous default barrier and expected bankruptcy costs. Total firm value peaks at coupon {o['C']:.1f}, with leverage {100 * o['lev']:.0f} percent and debt yield spread {o['spread_bp']:.0f} basis points in this numerical grid. The debt-value maximum is a different point, near coupon {C[int(np.argmax(L['debt']))]:.1f}. Past the firm-value optimum, debt value can still rise while equity and total value decline. These are model and grid results, not an empirical optimal-leverage recommendation. Tax usability, debt maturity, agency costs and other financing constraints alter the comparison."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(lf), Create(ld), Create(le), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(star, scale=1.5), FadeIn(side[1]), FadeIn(side[2]), FadeIn(side[3]))
        self.add(illustration(r"Leland (1994), perpetual debt"))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"in Leland's model, what happens to the default barrier when asset volatility rises, and why does "
                r"that help shareholders?")
        with self.voiceover("In Leland's model, what happens to the default barrier when the assets become more "
                            "volatile, and why does that suit the shareholders?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def leland(self):
        rows = [cmath(r"V_B^*", r"=", r"\frac{(1 - t_c)\,C}{r + \frac12\sigma^2}", font_size=38, colors={r"V_B^*": BAD}),
                cmath(r"\text{debt}", r"=", r"\frac{C}{r} + \Big((1 - \alpha) V_B - \frac{C}{r}\Big)\Big(\frac{V}{V_B}"
                      r"\Big)^{-X},\ \ X = \frac{2r}{\sigma^2}", font_size=34, colors={r"\text{debt}": DEBT})]
        whys = [why(r"Leland (1994): perpetual debt paying coupon $C$, taxes $t_c$ that make debt attractive, and "
                    r"shareholders who stop paying exactly when keeping the firm is no longer worth it: the barrier is "
                    r"chosen, not imposed"),
                why(r"debt is a riskless perpetuity plus a claim on the assets left at the barrier after a "
                    r"bankruptcy cost $\alpha$, weighted by $(V/V_B)^{-X}$, the value of a dollar paid on reaching it; "
                    r"with it comes an optimal amount of debt, the first structural "
                    r"theory of capital structure")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Who sets the barrier? In 1994 Hayne Leland let the shareholders choose. They keep paying the coupon as "
            "long as the firm is worth more to them alive; the moment it is not, they stop. Solving that choice gives "
            "the default barrier in closed form. <bookmark mark='a'/> The debt is then a riskless perpetuity, "
            "adjusted for the chance of reaching the barrier and what is recovered there, and the tax benefit of debt "
            "against the cost of default gives an optimal amount of borrowing."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def feedback(self):
        title = wrapped_label('Answer: more volatility lowers the fixed-coupon Leland barrier', 12.4, 32, QC.IDEA).to_edge(UP, buff=.6)
        answer = wrapped_label('$V_B^*=(1-t_c)C/(r+\\sigma^2/2)$ decreases with $\\sigma$ at fixed $C,r,t_c$. Shareholders wait longer; the full capital-structure optimum is a separate comparison.', 11.8, 27, GREY_A).move_to(ORIGIN)
        with self.voiceover("With coupon, tax rate and interest rate fixed in the displayed perpetual Leland model, a higher asset volatility increases the denominator of the optimal barrier, so the barrier falls. The shareholders value the option to wait and continue at lower asset values. This does not say that the firm's chosen coupon or optimal leverage stays fixed when volatility changes.") as vo:
            self.play(FadeIn(title), FadeIn(answer))
        self.wait(.5)
        self.clear_scene()
