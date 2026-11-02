from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant1.common import BTC, GAUSS, PART, PP, QQ, TAIL, load, real_data

C_ = {r"C(K)": QQ, r"q(K)": QQ, r"\mathbb Q": QQ}


def row(*parts, fs=40):
    return cmath(*parts, colors=C_, font_size=fs)


class TwoWorlds(VoiceoverScene):
    def construct(self):
        q = load("pq")
        self.card()
        self.intro()
        self.smile(q)
        self.derive()
        self.densities(q)
        self.martin(q)

    def card(self):
        c = chapter_card(10, r"Two worlds, $\mathbb P$ and $\mathbb Q$", r"What do option prices say about the future?",
                         lit=(1979, 1981), part=PART)
        with self.voiceover("Chapter ten. Two worlds, P and Q."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def intro(self):
        p_ = definition_card(r"$\mathbb P$: the real world", r"The probabilities of what will actually happen. "
                             r"Estimated from history; it is what statisticians, risk managers and investors care "
                             r"about. Prices drift with the risk premium.", width=6.0, color=PP)
        q_ = definition_card(r"$\mathbb Q$: the risk-neutral world", r"The probabilities implied by prices: the "
                             r"weights that make every price an average of its payoffs, with no premium. What "
                             r"derivatives desks care about (Parts 4, 9, 10).", width=6.0, color=QQ)
        pair = VGroup(p_, q_).arrange(RIGHT, buff=0.4, aligned_edge=UP).shift(UP * 1.0)
        acts = VGroup(label(r"Acts III and IV of this series live in these two worlds:", font_size=24, color=GREY_A),
                      label(r"pricing derivatives, in $\mathbb Q$; earning returns, in $\mathbb P$", font_size=26)
                      ).arrange(DOWN, buff=0.15).next_to(pair, DOWN, buff=0.6)
        with self.voiceover(
            "Finance has two sets of probabilities, and most confusion in it comes from mixing them up. P is the "
            "real world: how likely things actually are, the probabilities we have been estimating from history all "
            "part. <bookmark mark='a'/> Q is the risk-neutral world: the probabilities implied by prices. They are "
            "the weights that make every price equal to the average of its payoffs, with no premium for risk. "
            "Parts four, nine and ten build Q properly. <bookmark mark='b'/> Pricing derivatives happens in Q; "
            "earning returns happens in P. Here, for the first time, are both, for one asset, on one morning."
        ) as vo:
            self.play(FadeIn(p_, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q_, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(acts))
        self.wait(0.3)
        self.clear_scene()

    def smile(self, q):
        k, iv = np.asarray(q["k"]), np.asarray(q["iv"])
        g = axes([-0.75, 0.55], [0.35, 0.8], x_length=7.0, y_length=4.2, xlabel=r"log-moneyness $\ln(K/F)$",
                 ylabel=r"implied volatility", xticks=[-0.6, -0.3, 0, 0.3], yticks=[0.4, 0.5, 0.6, 0.7],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=18).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=QQ) for a, b in zip(k, iv) if -0.75 < a < 0.55])
        sk, siv = np.asarray(q["svi_k"]), np.asarray(q["svi_iv"])
        m = (sk > -0.75) & (sk < 0.55)
        line = curve(ax, sk[m], np.clip(siv[m], 0.35, 0.8), WHITE, stroke_width=3)
        info = VGroup(
            label(rf"Deribit BTC options, {q['days']} days to the {q['expiry'][8:].lstrip('0')} January 2026 expiry",
                  font_size=22),
            label(r"10 December 2025, 08:00 UTC (the Surface)", font_size=22, color=GREY_A),
            MathTex(rf"F = \${q['F']:,.0f}".replace(",", "{,}"), font_size=30, color=QQ),
            label(rf"{len(k)} quotes; a smooth curve through them (SVI, Part 12)", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.4).shift(UP * 1.2)
        if info.width > 5.6:
            info.scale_to_fit_width(5.6).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            f"The options are Bitcoin's, on the Surface, the series' frozen options market: the tenth of December "
            f"2025, {q['days']} days before the January expiry. Each dot is the implied volatility of an option at "
            "one strike, from that morning's trades. <bookmark mark='a'/> Through them, a smooth curve, a standard "
            "parametric smile whose derivation waits for Part twelve. From this curve every option price at every "
            "strike follows, and from the prices, the risk-neutral distribution."
        ) as vo:
            self.play(FadeIn(g), FadeIn(info))
            self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.05))
            vo.wait_until("a")
            self.play(Create(line), run_time=2)
        self.wait(0.3)
        self.clear_scene()

    def derive(self):
        rows = [
            row(r"C(K)", r"=", r"\mathbb E^{\mathbb Q}\big[(S_T - K)^+\big]"),
            row(r"\frac{\partial C}{\partial K}", r"=", r"-\,\mathbb Q(S_T > K)"),
            row(r"\frac{\partial^2 C}{\partial K^2}", r"=", r"q(K)"),
        ]
        whys = [why(r"a call is the $\mathbb Q$-average of its payoff (forward prices, no discounting)"),
                why(r"raise the strike by \$1: you lose \$1 in every state where the call pays"),
                why(r"Breeden and Litzenberger (1978): the density is the curvature of call prices")]
        step = ladder(self, rows, whys, keep=3, top=2.2, x=-2.4, buff=0.7, edge=6.9)
        with self.voiceover(
            "The step from prices to probabilities is two derivatives. A call struck at K is worth the risk-neutral "
            "average of its payoff. <bookmark mark='a'/> Raise the strike by a dollar and the call loses a dollar "
            "in every state where it pays: so the slope of the call price is minus the risk-neutral probability of "
            "finishing above the strike. <bookmark mark='b'/> Differentiate again and you get the density. Douglas "
            "Breeden and Robert Litzenberger showed this in 1978: the risk-neutral distribution is the curvature "
            "of option prices across strikes."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.6)
        self.clear_scene()

    def densities(self, q):
        x = np.asarray(q["x"])
        dq, dp = np.asarray(q["dens_q"]), np.asarray(q["dens_p"])
        top = float(max(dq.max(), dp.max())) * 1.12
        g = axes([-0.55, 0.7], [0, top], x_length=8.2, y_length=4.6,
                 xlabel=rf"Bitcoin's return over the next {q['days']} days", ylabel=r"density",
                 xticks=[-0.4, -0.2, 0, 0.2, 0.4, 0.6], xfmt=lambda v: f"{100 * v:+.0f}\\%" if v else "0",
                 font_size=18).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        aq = ax.plot_line_graph(x, dq, line_color=QQ, add_vertex_dots=False, stroke_width=4)
        ap = ax.plot_line_graph(x, dp, line_color=PP, add_vertex_dots=False, stroke_width=4)
        def area(dens, col, op):
            m = x <= -0.2
            pts = [ax.c2p(a, b) for a, b in zip(x[m], dens[m])] + [ax.c2p(x[m][-1], 0), ax.c2p(x[m][0], 0)]
            return Polygon(*pts, stroke_width=0, fill_color=col, fill_opacity=op)

        fq, fp = area(dq, QQ, 0.35), area(dp, PP, 0.25)
        leg = legend([(QQ, r"$\mathbb Q$: from that morning's option prices"),
                      (PP, rf"$\mathbb P$: Bitcoin's {q['days']}-day returns, Dec 2021 -- Dec 2025")], font_size=21)
        leg.to_edge(RIGHT, buff=0.35).shift(UP * 2.3)
        tab = VGroup(
            label(r"", font_size=20), MathTex(r"\mathbb Q", font_size=30, color=QQ), MathTex(r"\mathbb P", font_size=30, color=PP),
            label(r"average", font_size=22), MathTex(r"0", font_size=28, color=QQ),
            MathTex(rf"{100 * q['mean_p']:+.1f}\%", font_size=28, color=PP),
            label(r"spread", font_size=22), MathTex(rf"{100 * q['sd_q']:.1f}\%", font_size=28, color=QQ),
            MathTex(rf"{100 * q['sd_p']:.1f}\%", font_size=28, color=PP),
            label(r"chance of $-20\%$ or worse", font_size=22), MathTex(rf"{100 * q['left_q']:.1f}\%", font_size=28, color=QQ),
            MathTex(rf"{100 * q['left_p']:.1f}\%", font_size=28, color=PP),
        ).arrange_in_grid(4, 3, buff=(0.45, 0.22), col_alignments="lrr").next_to(leg, DOWN, buff=0.5).align_to(leg, LEFT)
        lesson = wrapped_label(r"$\mathbb Q$ is not a forecast: it prices insurance. Crash states cost more than "
                               r"their probability, and the drift is gone.", 5.2, 22, QC.IDEA)
        lesson.next_to(tab, DOWN, buff=0.4).align_to(leg, LEFT)
        with self.voiceover(
            f"Here they are. In violet, Q: the distribution of Bitcoin's price {q['days']} days ahead implied by that "
            "morning's option prices, measured from the forward price. <bookmark mark='a'/> In gold, P: what "
            f"actually happened over every {q['days']}-day window of the four years before that morning. "
            "<bookmark mark='b'/> They are different in telling ways. Q is centred on zero: under Q nothing is "
            f"expected to earn a premium. History drifted up {100 * q['mean_p']:.0f} percent. And Q puts more weight "
            f"on disaster: a {100 * q['left_q']:.0f} percent chance of losing a fifth or more, against "
            f"{100 * q['left_p']:.0f} percent in history. <bookmark mark='c'/> Q is not a worse forecast. It is not a "
            "forecast at all. It is the price of insurance: states of the world where people lose money are the "
            "states they pay most to protect, so Q weights them up. The gap between P and Q is the price of risk, "
            "and Part twenty-three connects them with a single object, the stochastic discount factor."
        ) as vo:
            self.play(FadeIn(g), Create(aq), FadeIn(leg[0]), run_time=2)
            vo.wait_until("a")
            self.play(Create(ap), FadeIn(leg[1]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(tab[:3]), FadeIn(tab[3:6]), FadeIn(tab[6:9]))
            self.play(FadeIn(fq), FadeIn(fp), FadeIn(tab[9:]))
            vo.wait_until("c")
            self.play(FadeIn(lesson))
        self.wait(0.4)
        self.clear_scene()

    def martin(self, q):
        thm = theorem_card(r"Martin (2017), \textit{QJE}", r"Under his negative-correlation condition (it holds, for "
                           r"instance, for an investor with log utility who is fully invested in the asset), the "
                           r"expected excess return is at least the risk-neutral variance: "
                           r"$\ \mathbb E[R_T] - R_f \ \ge\ R_f\,\operatorname{var}^{\mathbb Q}(S_T / F)$, "
                           r"computable from option prices alone.", width=11.6, font_size=24, kind=r"Theorem")
        thm.to_edge(UP, buff=0.5)
        nums = VGroup(
            MathTex(rf"\operatorname{{var}}^{{\mathbb Q}}(S_T/F) = {100 * q['svix2']:.2f}\%\ \ \text{{over {q['days']} days}}",
                    font_size=36, color=QQ),
            MathTex(rf"\Rightarrow\ \ \text{{expected excess return}} \ \ge\ {100 * q['bound_annual']:.0f}\%\ \text{{a year}}",
                    font_size=38, color=QC.IDEA),
        ).arrange(DOWN, buff=0.35).next_to(thm, DOWN, buff=0.6)
        ctx = VGroup(
            label(r"For the S\&P 500, Martin's bound averaged about 5\% a year, and rose above 20\% at the height of "
                  r"the 2008 crisis.", font_size=23, color=GREY_A),
            label(r"For Bitcoin, the condition is an assumption, not a fact: read the bound as what that morning's "
                  r"option prices demand, if it holds.", font_size=23, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(nums, DOWN, buff=0.6)
        if ctx.width > 13.0:
            ctx.scale_to_fit_width(13.0)
        with self.voiceover(
            "One bridge between the two worlds, from the frontier of asset pricing. In 2017 Ian Martin proved that, "
            "under a condition that holds, for instance, for a log-utility investor fully invested in the asset, "
            "the expected excess return is at least the "
            "risk-neutral variance of the return. A lower bound on a real-world expected return, read off option "
            "prices alone, no history needed. <bookmark mark='a'/> On the Surface, Bitcoin's risk-neutral variance "
            f"over the next {q['days']} days is {100 * q['svix2']:.1f} percent. As an annual rate, a lower bound of "
            f"{100 * q['bound_annual']:.0f} percent a year on Bitcoin's expected excess return. "
            "<bookmark mark='b'/> For the S and P five hundred, Martin's bound averaged about five percent a year, "
            "and rose above twenty percent in the autumn of 2008. For Bitcoin, the condition behind it is an "
            "assumption, not a fact. Read the number as what that morning's option prices demand, if it holds."
        ) as vo:
            self.play(FadeIn(thm, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(nums[0]))
            self.play(FadeIn(nums[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in ctx], lag_ratio=0.5))
        self.wait(0.4)
        self.clear_scene()
