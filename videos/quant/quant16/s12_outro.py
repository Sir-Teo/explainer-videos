from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, DELTA, GOOD, METHOD_COL, OPT, PART, load, sci, axes, data_range, pause_card, flat_camera

PROBLEMS = [
    r"Show that the control-variate estimator $\bar Y - b(\bar C - \mathbb{E}C)$ has minimal variance at "
    r"$b^* = \text{cov}(Y, C)/\text{var}(C)$, and that the variance falls by the factor $1 - \rho_{YC}^2$.",
    r"For importance sampling with a normal shifted by $\theta$, derive the likelihood ratio, and the $\theta$ that "
    r"centres the shifted normal on the strike.",
    r"Show that for any martingale $M$ with $M_0 = 0$, $\sup_\tau \mathbb{E}[h_\tau] \le \mathbb{E}[\max_t (h_t - M_t)]$.",
    r"Derive the stability condition of the explicit scheme for the heat equation by von Neumann analysis.",
    r"Show that reverse-mode differentiation of $f(g(h(x)))$ for $x \in \mathbb{R}^n$ costs a constant multiple of "
    r"one evaluation, while forward mode costs $n$ times.",
    r"Build a mixed estimator of a call's gamma: pathwise once (for delta), then the likelihood ratio.",
    r"Multilevel Monte Carlo with $\beta = \gamma$: show that $\sum_l \sqrt{V_l C_l}$ grows like $L \sim \log "
    r"\varepsilon^{-1}$, so the cost is $O(\varepsilon^{-2}(\log\varepsilon)^2)$.",
    r"Show that the FFT forces $\lambda\eta = 2\pi/N$ in Carr and Madan's discretisation.",    r"(qual) Show that $\operatorname{Var}(\hat G_{kk}) = (\mathbb E\psi_k^4 - (\mathbb E\psi_k^2)^2)/N$, and that for "
    r"$\psi_k = S^k/\sqrt{\mathbb E S^{2k}}$ with $S = e^{\sigma W_t - \sigma^2t/2}$, $\mathbb E\psi_k^4 = e^{4\sigma^2tk^2}$.",
    r"(qual) For a one-date stopping problem (stop and get $h$, or continue and get $C$), show that using $\hat C$ "
    r"loses $\mathbb E[|C - h|\,\mathbf 1\{\text{wrong}\}] \le \mathbb E[|C - \hat C|\,\mathbf 1\{|C - h| \le |C - \hat C|\}]$, "
    r"and that this is $O(\varepsilon^2)$ if $\Pr(|C - h| \le \varepsilon) = O(\varepsilon)$ and $|C - \hat C| \le \varepsilon$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.house(load("envelope"))
        self.recap(load("mc_live"), load("control"), load("is_sweep"), load("qmc"), load("effdim"), load("mlmc"),
                   load("lsm_live"), load("american"), load("maxcall"), load("greeks"), load("aad_scale"), load("lcp"),
                   load("adi_grid"), load("race"), load("qae"))
        self.desk(load("mc_live"))
        self.problems()
        self.payoffs()
        self.references()
        self.next_part()

    def house(self, env):
        chart = house_chart(PART, lit=("data", "vol")).scale(0.7).to_edge(UP, buff=0.3)
        rule = wrapped_label(r"Rule 16: every price leaves the engine with its error estimate (a standard error, a duality "
                             r"gap or a grid-refinement difference), and every method is checked nightly against a second, "
                             r"independent one on the same product. "
                             rf"No strategy was tested in this part: the trial counter still reads {env['trials']}.",
                             12.4, 22, QC.HOUSE).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The House now has a pricing engine, shared by every desk: simulation with its variance reduction and "
            "quasi-random paths, multilevel estimators, American options bracketed from both sides, Greeks by "
            "adjoints, grids in one and two dimensions, and Fourier pricing. <bookmark mark='a'/> Its rule, the "
            "sixteenth: no price leaves the engine without its error, and every method is checked each night "
            "against an independent one. No strategy was tested, and the trial counter still reads "
            f"{env['trials']}."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeIn(rule))
        self.wait(0.5)
        self.clear_scene()

    def recap(self, ml, ct, isw, q, ed, m, lv, a, mc, g, asc, lc, ag, r, qa):
        okc = [x for x in m["standard"] if np.isfinite(x["cost"])]
        sav = okc[-1]["cost"] / m["mlmc"][len(okc) - 1]["cost"]
        big = asc["rows"][-1]
        unif = {(x["nS"], x["uniform"]): x["err"] for x in ag["rows"]}
        cos_best = min((x for x in r["points"] if x["method"] == "COS"), key=lambda x: x["err"])
        items = [
            (rf"Monte Carlo's error bar is honest: {100 * ml['coverage']:.1f}\% coverage; a cent costs "
             rf"{ml['cent_paths'] / 1e6:.1f} million paths", OPT),
            (rf"a twin with a formula divides the variance by {ct['summary']['geo']['ratio']:,.0f}".replace(",", "{,}"), GOOD),
            (rf"importance sampling, learned in two steps: variance $\div$ {isw['ratio_best']:.0f}", GOOD),
            (rf"Sobol nets, and the bridge or PCA: {q['sd']['pseudo-random'][-1] / ed['pca_sd'][-1]:.0f} times less "
             r"spread on 64 dimensions", METHOD_COL["Sobol + bridge"]),
            (rf"multilevel Monte Carlo: {sav:.0f} times cheaper at one cent", GOOD),
            (rf"Longstaff--Schwartz on fresh paths {lv['eval'][0]:.3f}, the dual {a['ab'][-1]['upper']:.3f}; five "
             rf"assets: a tie with the network" if abs(mc["deep"]["lower"] - mc["lsm"]["200000"]["lower"]) <
             2 * np.hypot(mc["deep"]["se"], mc["lsm"]["200000"]["se"]) else
             rf"Longstaff--Schwartz on fresh paths {lv['eval'][0]:.3f}, the dual {a['ab'][-1]['upper']:.3f}", DELTA),
            (r"Greeks: bumps need common numbers; the likelihood ratio handles jumps", DELTA),
            (rf"AAD: {big['inputs']} Greeks for {big['t_aad'] / big['t_price']:.1f} prices, bumping "
             rf"{big['t_bump'] / big['t_price']:.0f}", DELTA),
            (rf"grids: stability, Rannacher's start; the American put by penalty, {lc['penalty']['price']:.3f}", BAD),
            (rf"ADI on a stretched grid: {unif[(40, True)] / unif[(40, False)]:.0f} times more accurate than uniform",
             METHOD_COL["ADI (Craig-Sneyd)"]),
            (rf"Fourier: COS to ${sci(cos_best['err'])}$ in {cos_best['time'] * 1e3:.2f} ms; amplitude estimation's slope "
             rf"{qa['slope']:.2f}", METHOD_COL["COS"]),
        ]
        rows = VGroup()
        for i, (t, col) in enumerate(items, 1):
            rows.add(VGroup(MathTex(str(i), font_size=26, color=col), label(t, font_size=22)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        title = label(r"Part 16 in eleven lines", font_size=36).to_edge(UP, buff=0.35)
        rows.next_to(title, DOWN, buff=0.35)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        if rows.height > 6.4:
            rows.scale_to_fit_height(6.4)
        with self.voiceover(
            "Part sixteen in eleven lines. Monte Carlo's error bar is honest, and expensive. Controls and importance "
            "sampling shrink it; nets and the bridge make paths cheap; multilevel removes the cost of a fine step. "
            "American options are bracketed from both sides. Adjoints deliver every Greek for a few prices. Grids "
            "need stability and a careful start. And for a vanilla, Fourier wins by orders of magnitude."
        ):
            self.play(FadeIn(title), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                 run_time=22))
        self.wait(0.5)
        self.clear_scene()

    def desk(self, ml):
        D = [
            (r"How many paths for a price to one basis point?",
             rf"$n \approx (1.96\,\sigma_Y/\varepsilon)^2$: here $\sigma_Y \approx {ml['sd']:.1f}$, so a cent at 95\% "
             rf"needs about {ml['cent_paths'] / 1e6:.1f} million plain paths; controls, strata or Sobol cut that by orders "
             r"of magnitude"),
            (r"Why is AAD's cost independent of the number of Greeks?",
             r"one reverse sweep carries the adjoint to every input at once, one multiply--add per tape edge: a small "
             r"constant times one pricing, for five inputs or five thousand"),
            (r"Crank--Nicolson's gamma oscillates. Why, and the fix?",
             r"its amplification tends to $-1$ for high frequencies at large $\lambda$, so a payoff's jump rings; a few "
             r"implicit (half-)steps first (Rannacher) damp it"),
            (r"LSM says 6.06, the dual bound 6.41. What next?",
             r"rerun the dual with more inner paths: if the gap shrinks it was noise; if not, improve the basis"),
        ]
        cards = VGroup(*[desk_question(q, a_, width=12.6, font_size=22) for q, a_ in D]).arrange(DOWN, buff=0.22)
        if cards.height > 7.4:
            cards.scale_to_fit_height(7.4)
        with self.voiceover(
            "Four desk questions. Paths for a basis point: the payoff's standard deviation over the target, squared, "
            "times 1.96 squared; millions of plain paths, far fewer with the tricks of chapters three to six. "
            "<bookmark mark='a'/> Why AAD's cost does not grow with the Greeks: one reverse sweep reaches every input. "
            "<bookmark mark='b'/> Crank–Nicolson's ringing gamma: weak damping of high frequencies; start with "
            "implicit steps. <bookmark mark='c'/> And a wide duality gap: first more inner paths, then a better basis. "
            "Full solutions are in the notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, mk in enumerate("abc", 1):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=18)
        with self.voiceover(
            "And ten problems: the optimal control variate, importance sampling's shift, the duality bound, the "
            "explicit scheme's stability, why reverse mode is cheap, a gamma estimator, the multilevel cost when beta "
            "equals gamma, and the FFT's grid constraint. Two are qualifying-exam problems: the Gram matrix's "
            "fourth moments, and why a wrong exercise rule costs only second order. Solutions, in English and "
            "Chinese, are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=5))
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"networks trained on this engine's prices and adjoint Greeks; deep stopping", [17]),
            (r"rates models on lattices and by simulation", [19]),
            (r"XVA: the whole book under thousands of scenarios", [21]),
            (r"tail risk by simulation, and importance sampling for it", [40]),
        ])
        with self.voiceover(
            "Where this comes back. Part seventeen trains networks on this engine's prices and adjoint Greeks. Rates "
            "models in Part nineteen are priced on lattices and by simulation. Part twenty-one runs the whole book "
            "under thousands of scenarios, and Part forty uses importance sampling for tail risk."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Glasserman, \textit{Monte Carlo Methods in Financial Engineering}; Savine, \textit{Modern Computational "
             r"Finance}", r"Andersen and Piterbarg, \textit{Interest Rate Modeling}, vol.\ I; Duffy, \textit{Finite Difference "
             r"Methods in Financial Engineering}; Seydel, \textit{Tools for Computational Finance}; Oosterlee and Grzelak, "
             r"\textit{Mathematical Modeling and Computation in Finance}"],
            [r"Crank--Nicolson (1947); Metropolis--Ulam (1949); Sobol (1967); Boyle; Schwartz (1977); Brennan--Schwartz (1978)",
             r"Rannacher (1984); Craig--Sneyd (1988); Kemna--Vorst (1990); Paskov--Traub (1995); Broadie--Glasserman (1996)",
             r"Caflisch--Morokoff--Owen (1997); Fourni\'e et al.\ (1999); Carr--Madan (1999); Longstaff--Schwartz; "
             r"Tsitsiklis--Van Roy; Lewis (2001)",
             r"Rogers (2002); Forsyth--Vetzal (2002); Andersen--Broadie; Haugh--Kogan (2004); Giles--Glasserman (2006)",
             r"Giles; Fang--Oosterlee; Joe--Kuo (2008); in 't Hout--Foulon (2010); Capriotti; Salmon et al.\ (2011)",
             r"Rhee--Glynn; Giles (2015); Gass et al.\ (2018); Rebentrost et al.\ (2018); Stamatopoulos et al.\ (2020); "
             r"Suzuki et al.\ (2020)",
             r"Chakrabarti et al.\ (2021); Owen (2022); Pan--Owen (2023); Junike (2024); Stamatopoulos--Zeng (2024)"])
        with self.voiceover(
            "The textbook chapters this part covers, and the papers it draws on. Every number here was computed by the "
            "House's engine on one CPU core."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def next_part(self):
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 17, Deep Pricing and Hedging", font_size=32, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The House can now compute any price it can write down, and say how wrong it might be. "
            "<bookmark mark='a'/> Next, Part seventeen: deep pricing and hedging. Networks that learn prices from "
            "this engine, solve equations in a hundred dimensions, and hedge books that no formula describes."
        ) as vo:
            self.play(FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
