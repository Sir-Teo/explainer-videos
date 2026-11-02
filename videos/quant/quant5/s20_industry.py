from __future__ import annotations

from datetime import date

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant5.common import BM, DRIFT, ITO, JUMP, PART, STRAT, load, pause, real_data


def _frac_year(d):
    d = int(d)
    x = date(d // 10000, d // 100 % 100, d % 100)
    return (x - date(2020, 3, 1)).days


class Industry(VoiceoverScene):
    def construct(self):
        w = load("wti")
        vs = load("varswap")
        o = load("orders")
        self.card()
        self.crisis(w)
        self.firm()
        self.clearing()
        self.vix(vs)
        self.validation(o)

    def card(self):
        c = chapter_card(17, r"Industry: how desks build, test and run SDE models", r"What happens when the model's "
                         r"state space is wrong?", lit=(2020,), part=PART)
        with self.voiceover("Chapter seventeen. How exchanges, brokers, clearing houses and banks actually use this "
                            "calculus, from the public record."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def crisis(self, w):
        d, v = np.asarray(w["date"]), np.asarray(w["value"])
        x = np.array([_frac_year(a) for a in d])
        g = axes([0, x.max() + 1], [-42, 35], x_length=6.2, y_length=3.4, ylabel=r"WTI spot, Cushing, \$ a barrel",
                 xticks=[0, 31, 61], xfmt=lambda u: {0: "1 Mar", 31: "1 Apr", 61: "1 May"}[int(u)], yticks=[-40, 0, 20],
                 font_size=15).to_corner(UL, buff=0.4)
        ax = g.ax
        line = curve(ax, x, v, BM, stroke_width=2.5)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(x.max() + 1, 0), color=GREY_C, stroke_width=1.5)
        i = int(np.argmin(v))
        dot = Dot(ax.c2p(x[i], v[i]), radius=0.07, color=QC.CRISIS)
        card = crisis_card(r"20 April 2020", r"Oil below zero", r"The May NYMEX WTI future settled at $-\$37.63$ a barrel "
                           r"(CFTC); Cushing spot, on FRED, $-\$36.98$. Under geometric Brownian motion, $\log S$ does "
                           r"not exist below zero.", stats=[(rf"{v[i]:.2f}", r"FRED DCOILWTICO, 20 April 2020"),
                                                            (r"-37.63", r"May contract settlement")], width=6.4,
                           font_size=20).to_corner(UR, buff=0.3)
        rng = np.random.default_rng(71)
        tt = np.linspace(0, 1, 60)
        z = np.cumsum(rng.standard_normal((30, 59)) * np.sqrt(1 / 59), axis=1)
        z = np.concatenate([np.zeros((30, 1)), z], axis=1)
        gbm = 18 * np.exp(-0.5 * tt + 1.0 * z)
        abm = 18 + 18 * 1.0 * z
        g2 = axes([0, 1], [-30, 60], x_length=3.0, y_length=2.6, xlabel=r"GBM", xticks=[], yticks=[0], font_size=14)
        g3 = axes([0, 1], [-30, 60], x_length=3.0, y_length=2.6, xlabel=r"Bachelier", xticks=[], yticks=[0], font_size=14)
        VGroup(g2, g3).arrange(RIGHT, buff=0.5).to_corner(DL, buff=0.4)
        f2 = path_fan(g2.ax, tt, np.clip(gbm, -30, 60), color=BM, opacity=0.35)
        f3 = path_fan(g3.ax, tt, np.clip(abm, -30, 60), color=DRIFT, opacity=0.35)
        z2 = VGroup(*[DashedLine(gg.ax.c2p(0, 0), gg.ax.c2p(1, 0), color=JUMP, stroke_width=1.5) for gg in (g2, g3)])
        sim_l = label(r"simulated, from 18 at 100\% volatility", font_size=15, color=GREY_B).next_to(VGroup(g2, g3), UP,
                                                                                                   buff=0.1)
        F = np.asarray(w["F"])
        g4 = axes([-20, 20], [0, 32], x_length=4.4, y_length=2.6, xlabel=r"futures price $F$",
                  ylabel=r"one-month put, strike 10", xticks=[-20, 0, 10, 20], yticks=[0, 10, 30], font_size=14)
        g4.to_corner(DR, buff=0.4)
        lb = curve(g4.ax, F, np.asarray(w["bach"]), DRIFT, stroke_width=3)
        lbl = curve(g4.ax, F, np.asarray(w["black"], float), BM, stroke_width=3)
        leg = legend([(BM, r"Black-76: undefined for $F \le 0$"), (DRIFT, r"Bachelier")], font_size=15).next_to(
            g4, UP, buff=0.1).align_to(g4, LEFT)
        cme = wrapped_label(r"CME Clearing Advisory 20-171: options on WTI and other energy futures switched to the "
                            r"Bachelier model from the margin cycle of 22 April 2020, to allow negative prices and "
                            r"strikes; back to Black-76 and Whaley on 31 August 2020 (Advisory 20-320)", 6.4, 16, GREY_A)
        cme.next_to(card, DOWN, buff=0.2).align_to(card, LEFT)
        src = real_data(r"FRED DCOILWTICO; CFTC press release 8432-21; CME Clearing advisories", corner=DR)
        with self.voiceover(
            "The crisis file. On the twentieth of April 2020, with storage at Cushing, Oklahoma, filling up, the May "
            "oil future settled at minus thirty-seven dollars and sixty-three cents a barrel; the Cushing spot price "
            f"on FRED reads {v[i]:.2f}. <bookmark mark='a'/> Geometric Brownian motion says that cannot happen: the "
            "log of a negative number does not exist. Bachelier's arithmetic Brownian motion crosses zero without "
            "noticing. <bookmark mark='b'/> CME Clearing moved options on WTI and related energy futures to the "
            "Bachelier model, effective the twenty-second of April, to allow negative prices and strikes, and moved "
            "back at the end of August. <bookmark mark='c'/> In a put, Black's formula stops at a zero futures price; "
            "Bachelier's carries on."
        ) as vo:
            self.play(FadeIn(g), Create(zero), Create(line), FadeIn(src), run_time=2)
            self.play(FadeIn(dot, scale=2), FadeIn(card))
            vo.wait_until("a")
            self.play(FadeIn(g2), FadeIn(g3), FadeIn(z2), FadeIn(sim_l), Create(f2), Create(f3), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(cme))
            vo.wait_until("c")
            self.play(FadeIn(g4), FadeIn(leg), Create(lbl), Create(lb), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def firm(self):
        card = firm_card(r"Interactive Brokers", r"An online broker. In a settled order of 28 September 2021, the CFTC "
                         r"found that it ``did not adequately prepare and configure its electronic trading system to "
                         r"recognize negative prices'', although it was on notice that they were possible.",
                         numbers=[(r"\$1.75\text{M}", r"civil penalty"), (r"\$82.57\text{M}", r"restitution, credited: "
                                                                                                r"already paid to customers"),
                                  (r"\$104\text{M}", r"the firm's own loss, 2020 (10-Q)")],
                         source=r"CFTC press release 8432-21; Interactive Brokers press release 21 April 2020 "
                                r"(provisional loss about \$88M) and Form 10-Q for Q2 2020", width=9.4, font_size=21)
        with self.voiceover(
            "The firm file. In a settled order in September 2021, the Commodity Futures Trading Commission found that "
            "Interactive Brokers did not adequately prepare and configure its trading system to recognize negative "
            "prices, although it was on notice that they were possible. <bookmark mark='a'/> It imposed a penalty of "
            "one point seven five million dollars and restitution of eighty-two point five seven million, credited "
            "because the firm had already compensated customers. The firm reported a loss of about a hundred and four "
            "million. A state space is a modelling assumption, and here it was also a software assumption."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Indicate(card, color=QC.FIRM, scale_factor=1.01))
        self.wait(0.4)
        self.clear_scene()

    def clearing(self):
        steps = VGroup(*[VGroup(RoundedRectangle(width=2.3, height=1.0, corner_radius=0.1, stroke_color=ITO,
                                                 stroke_width=2, fill_color=ITO, fill_opacity=0.12),
                                wrapped_label(t, 2.0, 18, WHITE)) for t in
                         (r"calibrate each risk factor's model daily", r"a copula ties the factors together",
                          r"Monte Carlo: 10{,}000 scenarios per factor", r"reprice every position in every scenario",
                          r"aggregate: the portfolio's margin")])
        for s_ in steps:
            s_[1].move_to(s_[0])
        steps.arrange(RIGHT, buff=0.35).shift(UP * 0.6)
        arrows = VGroup(*[Arrow(steps[k].get_right(), steps[k + 1].get_left(), buff=0.05, stroke_width=3,
                                color=GREY_B, tip_length=0.15) for k in range(4)])
        head = label(r"OCC's STANS margin system", font_size=34, color=ITO).next_to(steps, UP, buff=0.6)
        q = wrapped_label(r"``STANS utilizes large-scale Monte Carlo simulations to forecast price and volatility "
                          r"movements in determining a Clearing Member's margin requirement'' --- SEC Release No.\ "
                          r"34-90763 (2020), on the Options Clearing Corporation's methodology", 11.6, 20, GREY_A)
        q.next_to(steps, DOWN, buff=0.6)
        with self.voiceover(
            "Clearing houses run this calculus every night. According to its filings with the Securities and Exchange "
            "Commission, the Options Clearing Corporation's margin system, STANS, calibrates a model for each risk "
            "factor, ties them together with a copula, and simulates ten thousand Monte Carlo scenarios per factor, "
            "<bookmark mark='a'/> then reprices every position in every scenario and aggregates the losses into a "
            "margin requirement."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(s_) for s_ in steps[:3]], lag_ratio=0.5),
                      LaggedStart(*[GrowArrow(a) for a in arrows[:2]], lag_ratio=0.5), run_time=4)
            vo.wait_until("a")
            self.play(FadeIn(steps[3:]), GrowArrow(arrows[2]), GrowArrow(arrows[3]), FadeIn(q))
        self.wait(0.4)
        self.clear_scene()

    def vix(self, vs):
        rows = [cmath(r"d\log S", r"=", r"\frac{dS}{S} - \tfrac12\sigma^2\,dt", font_size=32),
                cmath(r"\int_0^T \sigma_t^2\,dt", r"=", r"2\Big(\int_0^T \frac{dS_t}{S_t} - \log\frac{S_T}{S_0}\Big)", font_size=32,
                      colors={r"2\Big(\int_0^T \frac{dS_t}{S_t} - \log\frac{S_T}{S_0}\Big)": ITO}),
                cmath(r"-\log\frac{S_T}{F}", r"=", r"-\frac{S_T - F}{F} + \int_0^F \frac{(K - S_T)^+}{K^2}dK + "
                      r"\int_F^\infty \frac{(S_T - K)^+}{K^2}dK", font_size=30, colors={r"K^2}dK": DRIFT})]
        whys = [why(r"It\^o's lemma for the logarithm", 19),
                why(r"rearrange and integrate: realized variance is a delta hedge plus a log contract", 19),
                why(r"Taylor's formula with integral remainder: the log contract is a strip of options weighted "
                    r"$1/K^2$ (Demeterfi, Derman, Kamal and Zou 1999; the VIX's weights, Cboe)", 19)]
        step = ladder(self, rows, whys, keep=3, top=3.3, x=-1.4, buff=0.55, edge=6.9)
        tab = VGroup(
            label(r"replication error against realized variance, 10{,}000 paths", font_size=19, color=GREY_A),
            MathTex(rf"\text{{Heston, 252 steps: mean }} {vs['252_heston']['mean'] * 1e4:+.2f},\ \text{{sd }} "
                    rf"{vs['252_heston']['sd'] * 1e4:.2f}", font_size=24, color=ITO),
            MathTex(rf"\text{{Heston, 2{{,}}520 steps: sd }} {vs['2520_heston']['sd'] * 1e4:.2f}", font_size=24,
                    color=ITO),
            MathTex(rf"\text{{with jumps: mean }} {vs['2520_jump']['mean'] * 1e4:+.1f} \text{{ against }} \lambda\,\mathbb{{E}}"
                    rf"\big[2(e^J - 1 - J) - J^2\big] = {vs['jump_bias_theory'] * 1e4:+.1f}", font_size=24, color=JUMP),
            label(r"(variance units $\times 10^{4}$; realized variance about 400)", font_size=17, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.3)
        pc, ans = pause(r"Why does the VIX weight strikes by $1/K^2$?", r"Those weights replicate $-\log S$, the payoff "
                        r"whose It\^o drift is exactly $\tfrac12\sigma^2$.", width=5.0, font_size=19)
        VGroup(pc, ans).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(DR, buff=0.3)
        with self.voiceover(
            "Itô's lemma is also a product. Apply it to the logarithm of the price. <bookmark mark='a'/> Rearranged, "
            "realized variance is twice the gain from holding one over S shares, minus twice the log return. "
            "<bookmark mark='b'/> And by Taylor's formula the log payoff is a forward plus puts and calls weighted by "
            "one over strike squared: the variance swap of Demeterfi, Derman, Kamal and Zou, and the weights of "
            "Cboe's VIX. <bookmark mark='c'/> On ten thousand Heston paths, the replication misses by "
            f"{vs['252_heston']['sd'] * 1e4:.1f} ten-thousandths of variance with daily steps, and "
            f"{vs['2520_heston']['sd'] * 1e4:.2f} with ten times as many. Add jumps, and a bias appears, exactly "
            f"chapter twelve's jump term: {vs['2520_jump']['mean'] * 1e4:+.1f} against a predicted "
            f"{vs['jump_bias_theory'] * 1e4:+.1f}."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            self.play(FadeIn(pc), FadeIn(ans))
            vo.wait_until("c")
            self.play(FadeOut(pc), FadeOut(ans), FadeIn(tab))
        self.wait(0.4)
        self.clear_scene()

    def validation(self, o):
        rows = [
            (r"\texttt{levy\_construction}", r"midpoint variance $\tfrac14$ of the gap; increments $2^{-k}$"),
            (r"\texttt{euler\_maruyama}, \texttt{milstein}", rf"strong orders {o['slope_strong_euler']:.2f} and "
                                                             rf"{o['slope_strong_milstein']:.2f} on GBM"),
            (r"\texttt{ou\_exact}, \texttt{cir\_exact}, \texttt{cir\_mle}", r"stationary moments; MLE recovers simulated "
                                                                            r"parameters"),
            (r"\texttt{local\_time}", r"$\mathbb{E}L^0_1 = \sqrt{2/\pi}$"),
            (r"\texttt{merton\_jumps}, \texttt{heston\_euler}", r"$\mathbb{E}S_T = S_0e^{\mu T}$; $\mathbb{E}v_T$ exact"),
            (r"\texttt{hawkes\_thinning}, \texttt{hawkes\_fit}, \texttt{hawkes\_compensator}",
             r"rate $\mu/(1 - n)$; MLE; rescaled gaps Exp(1)"),
            (r"\texttt{fbm}, \texttt{hurst\_from\_increments}, \texttt{signature}", r"$H$ recovered; Chen; unit-square "
                                                                                     r"area 1"),
        ]
        tab = VGroup(*[VGroup(label(a, font_size=18, color=QC.HOUSE), label(b, font_size=18, color=GREY_A))
                       for a, b in rows])
        for r_ in tab:
            r_[1].next_to(r_[0], RIGHT, buff=0.3)
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 6.6)
        tab.to_edge(LEFT, buff=0.4).shift(DOWN * 1.1)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        sr = VGroup(
            label(r"SR 11-7 (Fed and OCC, 2011) $\to$ SR 26-2 (Fed, OCC and FDIC, 17 April 2026)", font_size=24,
                  color=ITO),
            label(r"kept: effective challenge, conceptual soundness, ongoing monitoring, outcomes analysis, a model "
                  r"inventory", font_size=19, color=GREY_A),
            label(r"added: tailoring to materiality; aimed at banks over \$30 billion; generative and agentic AI "
                  r"outside its scope", font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(UP, buff=0.35)
        th = label(r"the House's validation report: each simulator against a case with a known answer (Rule 6)",
                   font_size=21, color=QC.HOUSE).next_to(sr, DOWN, buff=0.3).align_to(sr, LEFT)
        with self.voiceover(
            "Finally, who checks the models. American banks' model risk was supervised under SR 11-7, from 2011. On "
            "the seventeenth of April 2026 the Federal Reserve, the OCC and the FDIC replaced it with SR 26-2, which "
            "keeps effective challenge, conceptual soundness, ongoing monitoring, outcomes analysis and a model "
            "inventory, adds tailoring to materiality, is aimed mainly at banks above thirty billion dollars, and "
            "leaves generative and agentic AI outside its scope. <bookmark mark='a'/> The House's version is Rule 6: "
            "no simulator prices anything until it has reproduced a known answer. Here is this part's validation "
            "report."
            " Last, the frontier."
        ) as vo:
            self.play(FadeIn(sr[0]))
            self.play(FadeIn(sr[1]), FadeIn(sr[2]))
            vo.wait_until("a")
            self.play(FadeIn(th), LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.3, run_time=4))
        self.wait(0.4)
        self.clear_scene()
