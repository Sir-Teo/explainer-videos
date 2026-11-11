from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant9.common import ALT, ARB, FWD, HEDGE, P_C, PART, Q_C, answer_under, load

H_COL = {"0.4": ALT, "0.5": GREY_B, "0.6": P_C}
E_COL = {"0": WHITE, "1bp": HEDGE, "10bp": ARB}


def _lg(n):
    return np.log10(np.asarray(n, float))


class Research(VoiceoverScene):
    def construct(self):
        t = load("friction_theory")
        self.card()
        self.fbm_law()
        self.sign_bet()
        self.sharpe_plot(t)
        self.costs()
        self.net_plot(t)
        self.cps()
        self.btc(t)
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"Arbitrage with frictions", r"Fractional prices, admissibility, and what small trading costs change", part=PART)
        with self.voiceover("""Fractional Brownian log prices require care: H different from one half excludes semimartingales. We will separate a sign-increment score from investment wealth, then state a no-arbitrage condition with costs."""):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def fbm_law(self):
        rows = [cmath(r"\operatorname{Cov}\big(B^H_s, B^H_t\big)", r"=", r"\tfrac12\big(s^{2H} + t^{2H} - |t - s|^{2H}\big)",
                      font_size=32, colors={r"\operatorname{Cov}\big(B^H_s, B^H_t\big)": P_C}),
                cmath(r"\rho", r"=", r"\operatorname{Corr}\big(\Delta_k, \Delta_{k+1}\big) = 2^{2H - 1} - 1", font_size=32,
                      colors={r"\rho": P_C}),
                cmath(r"\sum_k |\Delta_k|^2", r"\to", r"\begin{cases} 0 & H > \tfrac12 \\ \infty & H < \tfrac12 \end{cases}",
                      font_size=30, colors={r"\sum_k |\Delta_k|^2": ARB})]
        whys = [why(r"fractional Brownian motion (Mandelbrot and Van Ness 1968, Part 14): Gaussian, self-similar, $H = "
                    r"\frac12$ is Brownian motion"),
                why(r"consecutive increments on any grid have the same correlation: $+0.149$ at $H = 0.6$, $-0.129$ at "
                    r"$H = 0.4$. Memory at every scale"),
                why(r"for $H<1/2$, infinite quadratic variation excludes a continuous semimartingale; for $H>1/2$, zero quadratic variation AND infinite total variation exclude one")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            """For fractional Brownian log prices, zero is less than H, less than one. <bookmark mark='a'/> The covariance reduces to Brownian motion at one half. <bookmark mark='b'/> Consecutive equal-length increments have correlation two to the power two H minus one, minus one, at every scale. <bookmark mark='c'/> Below one half, quadratic variation diverges. Above one half it vanishes, while total variation is infinite. A continuous semimartingale cannot have either combination: zero quadratic variation requires finite variation. Arbitrage conclusions additionally depend on the trading class."""
        ) as vo:
            step(0, run_time=0.15)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def sign_bet(self):
        rows = [cmath(r"\pi_k", r"=", r"\operatorname{sign}(\rho)\,\operatorname{sign}(\Delta_{k-1}),\qquad "
                      r"\Delta_k \sim N\big(0, \sigma^2 n^{-2H}\big)", font_size=30, colors={r"\pi_k": FWD}),
                cmath(r"\mathbb E[\pi_k\Delta_k]", r"=", r"\sigma n^{-H}\sqrt{2/\pi}\,|\rho|", font_size=32,
                      colors={r"\mathbb E[\pi_k\Delta_k]": FWD}),
                cmath(r"\mathrm{SR}_{\text{iid reference}}", r"\approx", r"\sqrt n\;\frac{\sqrt{2/\pi}\,|\rho|}{\sqrt{1 - 2\rho^2/\pi}}"
                      r"\ \to\ \infty", font_size=32, colors={r"\mathrm{SR}_{\text{iid reference}}": ARB})]
        whys = [why(r"proxy score $G_n=\sum_k\pi_k\Delta_k$ for log-price increments; this is not exact self-financing wealth in $S=e^{\sigma B^H}$"),
                why(r"for a standard normal pair with correlation $\rho$, $\mathbb E[\operatorname{sign}(X)\,Y] = \rho\,"
                    r"\mathbb E|X| = \rho\sqrt{2/\pi}$"),
                why(r"the $\sqrt n$ scaling assumes independent scores; serial covariance changes annual risk. This reference formula proves neither asymptotic arbitrage nor NFLVR failure")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            """Use the previous increment's sign, <bookmark mark='a'/> following positive correlation or reversing negative correlation. This scores log increments, not self-financing wealth. <bookmark mark='b'/> Conditional normal expectation gives the displayed mean signed increment. <bookmark mark='c'/> Annualizing one-step moments as independent gives the square-root-n reference. Serial covariance invalidates that annual risk formula; neither a positive mean nor a diverging reference Sharpe establishes arbitrage. Rogers and Cheridito analyze specified fractional-market trading classes."""
        ) as vo:
            step(0, run_time=0.15)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def sharpe_plot(self, t):
        n = np.asarray(t["n"], float)
        x = _lg(n)
        g = axes([1.0, 5.0], [-2, 32], x_length=8.2, y_length=4.2, xlabel=r"trades a year, $n$",
                 ylabel=r"annual score mean / SD; iid reference", xticks=list(_lg([16, 256, 4096, 65536])),
                 yticks=[0, 10, 20, 30], xfmt=lambda v: f"{10 ** v:,.0f}".replace(",", r"{,}"), font_size=15,
                 log_x=True).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        lines, dots = VGroup(), VGroup()
        for H in ("0.6", "0.5", "0.4"):
            r = t["H"][H]
            lines.add(curve(ax, x, r["theory"]["0"]["sharpe"], H_COL[H], stroke_width=3))
            dots.add(VGroup(*[Dot(ax.c2p(a, b), radius=0.05, color=H_COL[H]) for a, b in zip(x, r["sim"]["0"]["sharpe"])]))
        leg = legend([(H_COL["0.6"], r"$H = 0.6$: follow the last move"), (H_COL["0.5"], r"$H = 0.5$: Brownian"),
                      (H_COL["0.4"], r"$H = 0.4$: reverse it")], font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        side = wrapped_label(r"lines: iid reference; dots: 160 independent one-year log-increment scores, $\sigma=20\%$, Davies--Harte $2^{16}$ steps; serial dependence retained in dots", 3.3, 14, GREY_A).next_to(
            leg, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            """The existing costless simulations compare <bookmark mark='a'/> annual mean over standard deviation across one hundred and sixty independent yearly paths <bookmark mark='b'/> with the iid one-step reference. Dependence and sampling error explain discrepancies. <bookmark mark='c'/> At H of one half the conditional edge vanishes. These scores do not establish investment arbitrage."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(lines[0]), FadeIn(dots[0]), FadeIn(leg[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lines[2]), FadeIn(dots[2]), FadeIn(leg[2]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(lines[1]), FadeIn(dots[1]), FadeIn(leg[1]))
        self.wait(0.4)
        self.clear_scene()

    def costs(self):
        rows = [cmath(r"\mathbb E|\pi_k - \pi_{k-1}|", r"=", r"2p,\qquad p = \tfrac12 - \tfrac{1}{\pi}\arcsin\rho",
                      font_size=32, colors={r"\mathbb E|\pi_k - \pi_{k-1}|": ARB}),
                cmath(r"m(n)", r"=", r"n\Big[\sigma n^{-H}\sqrt{2/\pi}\,|\rho| - 2\varepsilon p\Big]", font_size=32,
                      colors={r"m(n)": FWD}),
                cmath(r"n^*", r"=", r"\bigg[\frac{(1 - H)\,\sigma\sqrt{2/\pi}\,|\rho|}{2\varepsilon p}\bigg]^{1/H}", font_size=32,
                      colors={r"n^*": HEDGE})]
        whys = [why(r"the position flips when two consecutive increments differ in sign: Sheppard's formula for a normal "
                    r"pair gives the probability $p$, 0.45 at $H = 0.6$"),
                why(r"pay $\varepsilon$ per unit traded: the edge per trade shrinks like $n^{-H}$ as the grid refines, the "
                    r"cost per trade does not"),
                why(r"the proxy mean has a finite optimum: at $H=0.6$, $\sigma=20\%$, 1 bp gives $n^*\approx2{,}300$; 10 bp, about 50. This is not a no-arbitrage theorem")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            """Charge linear turnover in the score proxy. <bookmark mark='a'/> Position changes by two when consecutive signs differ; Sheppard's formula supplies the switching probability. <bookmark mark='b'/> Subtract epsilon times turnover, omitting initial and terminal boundary terms. Gross edge shrinks per step; the turnover charge does not. <bookmark mark='c'/> Differentiating the mean gives a finite optimum for this proxy. It neither proves absence of arbitrage nor represents exact proportional-cost wealth."""
        ) as vo:
            step(0, run_time=0.15)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def net_plot(self, t):
        r = t["H"]["0.6"]
        n = np.asarray(t["n"], float)
        x = _lg(n)
        lo, hi = -0.3, 0.7
        g = axes([1.0, 5.0], [lo, hi], x_length=8.2, y_length=4.2, xlabel=r"trades a year, $n$",
                 ylabel=r"mean log-increment score/year, $H = 0.6$", xticks=list(_lg([16, 256, 4096, 65536])),
                 yticks=[-0.2, 0, 0.2, 0.4, 0.6], xfmt=lambda v: f"{10 ** v:,.0f}".replace(",", r"{,}"),
                 yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=15, log_x=True).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        zero = DashedLine(ax.c2p(1.0, 0), ax.c2p(5.0, 0), color=GREY_C, stroke_width=1.2)
        xf = np.linspace(1.2, 4.82, 200)
        nf = 10 ** xf
        rho, p, sig, H = r["rho"], r["pflip"], t["sigma"], 0.6
        lines, dots, stars = VGroup(), VGroup(), VGroup()
        for k, e in t["eps"].items():
            m = nf * (sig * nf ** -H * np.sqrt(2 / np.pi) * abs(rho) - 2 * e * p)
            keep = (m >= lo) & (m <= hi)
            lines.add(curve(ax, xf[keep], m[keep], E_COL[k], stroke_width=3))
            sm = np.asarray(r["sim"][k]["mean"])
            ok = (sm >= lo) & (sm <= hi)
            dots.add(VGroup(*[Dot(ax.c2p(a, b), radius=0.05, color=E_COL[k]) for a, b in zip(x[ok], sm[ok])]))
            if k in r.get("best", {}):
                b = r["best"][k]
                stars.add(VGroup(Star(n=5, outer_radius=0.13, color=E_COL[k], fill_opacity=1).move_to(
                    ax.c2p(np.log10(b["n_star"]), b["mean"])),
                    MathTex(rf"n^* \approx {b['n_star']:,.0f}".replace(",", "{,}"), font_size=20, color=E_COL[k]).next_to(
                        ax.c2p(np.log10(b["n_star"]), b["mean"]), UP, buff=0.18)))
        leg = legend([(E_COL["0"], r"no cost"), (E_COL["1bp"], r"1 bp per unit traded"),
                      (E_COL["10bp"], r"10 bp per unit traded")], font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        side = wrapped_label(r"lines: proxy $m(n)$; dots: 160 one-year scores. Vertical window omits larger positive and negative scores; 100\% means one log point, not an investment return", 3.3, 14, GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        b1, b10 = r["best"]["1bp"], r["best"]["10bp"]
        with self.voiceover(
            f"""At H of point six, <bookmark mark='a'/> the costless mean rises beyond the chart. <bookmark mark='b'/> One basis point peaks near twenty-three hundred trades yearly and {100 * b1['mean']:.0f} percent, then turns negative beyond ten thousand. <bookmark mark='c'/> Ten basis points peaks near fifty trades and {100 * b10['mean']:.0f} percent. These are log-increment score units, not investment returns; each charge uses the same fixed paths."""
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(lines[0]), FadeIn(dots[0]), FadeIn(leg[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lines[1]), FadeIn(dots[1]), FadeIn(leg[1]), FadeIn(stars[0]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(lines[2]), FadeIn(dots[2]), FadeIn(leg[2]), FadeIn(stars[1]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def cps(self):
        body = VGroup(
            wrapped_label(r"sufficient for no arbitrage under the usual admissibility conditions: $Q\sim P$ and a $Q$-(local) martingale $\tilde S$ inside the discounted bid--ask band. Converse theorems need additional hypotheses", 10.4, 21, GREY_A),
            MathTex(r"\frac{S_t}{1 + \varepsilon}\ \le\ \tilde S_t\ \le\ (1 + \varepsilon)\,S_t\quad\text{for all } t",
                    font_size=32, color=Q_C),
            wrapped_label(r"a strictly positive continuous price with conditional full support admits a consistent price system for every spread. The exponential $S=e^{\sigma B^H}$ qualifies", 10.4, 21,
                          GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        thm = theorem_card(r"Consistent price systems", body,
            who=r"Jouini and Kallal (1995); Guasoni (2006); Guasoni, R\'asonyi and Schachermayer (2008)", width=11.6,
            font_size=22).move_to(UP * 0.5)
        note_ = why(r"rough variance can generate a semimartingale price via a stochastic integral; no arbitrage still needs a valid pricing measure and admissibility").to_edge(DOWN, buff=0.45)
        if note_.width > 12.6:
            note_.scale_to_fit_width(12.6)
        with self.voiceover(
            """A consistent price system suffices for no arbitrage under usual admissibility: <bookmark mark='a'/> an equivalent measure and a discounted local martingale inside the bid and ask at every time. Converses need further hypotheses. This multiplicative spread differs from the score's linear charge. <bookmark mark='b'/> Positive continuous processes with conditional full support admit such systems for every positive spread. Every uniform neighborhood of every positive continuous continuation must have positive conditional probability; exponential fractional Brownian motion qualifies. <bookmark mark='c'/> Rough variance can generate a semimartingale price, but no arbitrage still requires a valid pricing measure and admissibility."""
        ) as vo:
            self.play(FadeIn(thm))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Indicate(body[2], color=Q_C, scale_factor=1.03))
            vo.wait_until("c")
            self.play(FadeIn(note_))
        self.wait(0.5)
        self.clear_scene()

    def btc(self, t):
        b = t["btc"]
        hx = [-4.6, -2.2, 0.0, 2.4, 4.9]
        head = VGroup(label(r"Bitcoin, sampled every", font_size=18, color=GREY_B), label(r"$\rho$", font_size=22),
                      label(r"implied $H$", font_size=20), label(r"break-even cost", font_size=20, color=HEDGE),
                      label(r"net per trade at 1 bp", font_size=20, color=ARB))
        tab = VGroup()
        for j, row in enumerate([head] + [VGroup(label(rf"{m} min", font_size=20, color=FWD),
                                                 MathTex(rf"{b[m]['rho']:+.3f}", font_size=26),
                                                 MathTex(rf"{b[m]['H_implied']:.2f}", font_size=26),
                                                 MathTex(rf"{b[m]['breakeven_bp']:.2f}\ \text{{bp}}", font_size=26),
                                                 MathTex(rf"{1e4 * b[m]['net_1bp'] * int(m) / 525600:+.2f}\ \text{{bp}}",
                                                         font_size=26))
                                          for m in ("1", "5", "15", "60")]):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.6 - 0.72 * j, 0])
            tab.add(row)
        foot = wrapped_label(r"Binance BTCUSDT, 2019--2020. Direction chosen using full-sample $\rho$: retrospective score. Implied $H$ only inverts one correlation; no fBM fit or untouched forecast test. Costs omit spreads, impact and funding",
                             11.8, 16, GREY_A).to_edge(DOWN, buff=0.45)
        be_max = max(v["breakeven_bp"] for v in b.values())
        with self.voiceover(
            f"""The Bitcoin table samples 2019 and 2020 at one, five, fifteen and sixty minutes. <bookmark mark='a'/> Correlations are slightly negative. Inverting the fractional formula labels an H without identifying that model. The same full sample selects reversal, making this retrospective. <bookmark mark='b'/> Existing sign-increment scores, break-even charges and one-basis-point results follow. <bookmark mark='c'/> They omit execution spreads, impact and funding, with no untouched forecasting test. The pricing-system theorem predicts neither these correlations nor their break-even charges."""
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(r_[0], r_[1], r_[2])) for r_ in tab[1:]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(r_[3], r_[4])) for r_ in tab[1:]], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(*[Indicate(r_[3], color=HEDGE) for r_ in tab[1:]])
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"project: construct a price band", r"specify a positive fractional-price model, a spread and admissibility; construct a consistent price system and super-replication bounds", width=12.4, font_size=18),
            desk_question(r"project: utility with memory and costs", r"state the utility, admissible controls and execution model before asking for an optimum or small-cost asymptotics", width=12.4, font_size=18),
            desk_question(r"project: prospective empirical evidence", r"freeze signal direction and sampling rules, then use untouched data and executable costs; no new test is run here", width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            """Three project directions: <bookmark mark='a'/> construct a consistent price system and useful hedge bands for a specified fractional model and spread; <bookmark mark='b'/> study utility with memory, costs and explicit admissibility; <bookmark mark='c'/> predefine empirical direction and sampling, then test untouched data with execution costs. No new test is run here."""
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            for k, mk in ((1, "b"), (2, "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"at $H = 0.6$ the best trading frequency with a 1 bp cost is about 2,300 a year. If the cost "
                       r"doubles to 2 bp, by what factor does $n^*$ change?").move_to(UP * 0.9)
        with self.voiceover(
            """At H of point six, one basis point gives about twenty-three hundred proxy trades a year. Double the charge: how does frequency change? <bookmark mark='a'/> By two to the power minus one over H, about point three one five: roughly seven hundred and thirty yearly."""
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            self.play(FadeIn(answer_under(q, r"$n^*(2\varepsilon)/n^*(\varepsilon)=2^{-1/H}\approx0.315$: about 730/year in this proxy")))
        self.wait(0.5)
        self.clear_scene()
