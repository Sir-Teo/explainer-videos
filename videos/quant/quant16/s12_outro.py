from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, DELTA, GOOD, METHOD_COL, OPT, PART, load, sci, axes, data_range, pause_card, flat_camera

PROBLEMS = [
    r"For a deterministic coefficient and finite second moments, show that the control-variate estimator $\bar Y - b(\bar C - \mathbb{E}C)$ has minimal variance at "
    r"$b^* = \text{cov}(Y, C)/\text{var}(C)$, and that the variance falls by the factor $1 - \rho_{YC}^2$.",
    r"For importance sampling with a normal shifted by $\theta$, derive the likelihood ratio, and the $\theta$ that "
    r"centres the shifted normal on the strike.",
    r"On a finite exercise grid with integrable rewards and an integrable martingale, show that for $M_0=0$, $\sup_\tau \mathbb{E}[h_\tau] \le \mathbb{E}[\max_t (h_t - M_t)]$.",
    r"Derive the stability condition of the explicit scheme for the heat equation by von Neumann analysis.",
    r"For a scalar-output differentiable tape, show reverse work is $O(\text{tape work})$; contrast computing all "
    r"input directions by forward sweeps. State memory and elementary-operation assumptions.",
    r"Build a mixed estimator of a call's gamma: pathwise once (for delta), then the likelihood ratio.",
    r"Under Giles's bias, independence and allocation conditions, with $\beta = \gamma$: show that $\sum_l \sqrt{V_l C_l}$ grows like $L \sim \log "
    r"\varepsilon^{-1}$, so the cost is $O(\varepsilon^{-2}(\log\varepsilon)^2)$.",
    r"Show that the FFT forces $\lambda\eta = 2\pi/N$ in Carr and Madan's discretisation.",    r"(qual) Show that $\operatorname{Var}(\hat G_{kk}) = (\mathbb E\psi_k^4 - (\mathbb E\psi_k^2)^2)/N$, and that for "
    r"$\psi_k = S^k/\sqrt{\mathbb E S^{2k}}$ with $S = e^{\sigma W_t - \sigma^2t/2}$, $\mathbb E\psi_k^4 = e^{4\sigma^2tk^2}$.",
    r"(qual) For a one-date stopping problem (stop and get $h$, or continue and get $C$), show that using $\hat C$ "
    r"loses $\mathbb E[|C - h|\,\mathbf 1\{\text{wrong}\}] \le \mathbb E[|C - \hat C|\,\mathbf 1\{|C - h| \le |C - \hat C|\}]$, "
    r"and that this is $O(\varepsilon^2)$ if $\Pr(0<|C - h| \le \varepsilon) = O(\varepsilon)$ and $|C - \hat C| \le \varepsilon$.",
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
        rule = wrapped_label(r"Rule 16: report sampling uncertainty separately from bias and numerical-reference error. Use refinement, "
                             r"alternative formulations and dual expectations within their assumptions; noisy point estimates are not sure bounds. "
                             rf"No market strategy trial was added: the part's cumulative counter remains {env['trials']}.",
                             12.4, 24, QC.HOUSE).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            f"The House has a collection of pricing methods, rather than a universal accuracy certificate. <bookmark mark='a'/> Rule sixteen is to separate sampling uncertainty from discretization, truncation, reference and model errors, and choose verification suited to the method. No automated nightly production control is claimed here. These synthetic numerical examples add no market strategy trials; the part's cumulative counter remains {env['trials']}."
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
            (rf"MC pointwise empirical coverage: {100 * ml['coverage']:.1f}\% coverage; a cent costs "
             rf"{ml['cent_paths'] / 1e6:.1f} million paths", OPT),
            (rf"a twin with a formula divides the variance by {ct['summary']['geo']['ratio']:,.0f}".replace(",", "{,}"), GOOD),
            (rf"IS: best tested fixed-grid variance ratio $\div$ {isw['ratio_best']:.0f}", GOOD),
            (rf"Sobol nets, and the bridge or PCA: {q['sd']['pseudo-random'][-1] / ed['pca_sd'][-1]:.0f} times less "
             r"spread on 64 dimensions", METHOD_COL["Sobol + bridge"]),
            (rf"MLMC: estimated step-work ratio {sav:.0f} at a one-cent target", GOOD),
            (rf"Longstaff--Schwartz on fresh paths {lv['eval'][0]:.3f}, the dual {a['ab'][-1]['upper']:.3f}; five "
             rf"assets: difference unresolved at two evaluation s.e." if abs(mc["deep"]["lower"] - mc["lsm"]["200000"]["lower"]) <
             2 * np.hypot(mc["deep"]["se"], mc["lsm"]["200000"]["se"]) else
             rf"Longstaff--Schwartz on fresh paths {lv['eval'][0]:.3f}, the dual {a['ab'][-1]['upper']:.3f}", DELTA),
            (r"Greeks: estimator regularity, common numbers, score weights and bias all matter", DELTA),
            (rf"AAD benchmark: {big['inputs']} input derivatives at {big['t_aad'] / big['t_price']:.1f} prices, bumping "
             rf"{big['t_bump'] / big['t_price']:.0f}", DELTA),
            (rf"grids: stability, Rannacher's start; the American put by penalty, {lc['penalty']['price']:.3f}", BAD),
            (rf"ADI on a stretched grid: {unif[(40, True)] / unif[(40, False)]:.0f} times smaller COS-reference discrepancy in this case",
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
            'Part sixteen in eleven lines. Sampling intervals have assumptions and measured coverage. Controls, shifts and randomized nets can reduce variance in suitable problems. Multilevel allocates correction work under bias and variance conditions. Fixed-policy and dual expectations bound finite-date stopping values, while their numerical estimates remain noisy. Adjoint work scales with a scalar-output tape, with memory and regularity costs. Grids require stability, appropriate boundaries and a careful start. Characteristic-function methods can be fast for suitable products. Every numerical ratio on this page belongs to its saved experiment, rather than a universal method ranking.'
        ):
            self.play(FadeIn(title), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                 run_time=22))
        self.wait(0.5)
        self.clear_scene()

    def desk(self, ml):
        D = [
            (r"How many iid paths for an approximate one-cent 95\% half-width?",
             rf"$n \approx (1.96\,\sigma_Y/\varepsilon)^2$: here $\sigma_Y \approx {ml['sd']:.1f}$, so a cent at 95\% "
             rf"needs about {ml['cent_paths'] / 1e6:.1f} million plain paths; controls, strata or Sobol cut that by orders "
             r"of magnitude in some examples; bias and cost remain separate"),
            (r"What controls AAD work for a scalar price?",
             r"one reverse sweep carries the adjoint to every input at once, one multiply--add per tape edge: a small "
             r"constant times executed tape work under the operation model; pricing work and memory can grow with inputs"),
            (r"Crank--Nicolson's gamma oscillates. Why, and the fix?",
             r"its amplification tends to $-1$ for high frequencies at large $\lambda$, so a payoff's jump rings; a few "
             r"implicit (half-)steps first (Rannacher) damp it"),
            (r"LSM says 6.06, the dual bound 6.41. What next?",
             r"separate outer uncertainty, inner upward bias and dual looseness; increase inner work as a diagnostic, then evaluate policy and martingale approximations"),
        ]
        cards = [desk_question(question, answer, width=12.6, font_size=30).move_to(ORIGIN) for question, answer in D]
        with self.voiceover(
            "Four desk questions. For an unbiased iid estimator under a normal approximation, a target sampling half-width uses variance times one point nine six squared divided by target squared. One cent is one basis point only on a one-hundred-dollar notional; the units must be specified. Bias remains separate. <bookmark mark='a'/> Reverse work is proportional to a scalar-output tape, with memory and implementation costs. <bookmark mark='b'/> Crank–Nicolson can weakly damp high frequencies; a suitable implicit start can improve behaviour. <bookmark mark='c'/> A wide observed dual gap mixes policy quality, dual approximation, inner bias and outer uncertainty. Increasing inner work is a diagnostic, not proof that all remaining gap is policy loss. Worked solutions are in the notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, mk in enumerate("abc", 1):
                vo.wait_until(mk)
                self.play(ReplacementTransform(cards[k - 1], cards[k]))
        self.wait(0.5)
        self.clear_scene()

    def problems(self):
        pages = []
        for start in (0, 5):
            head = label(rf"Problems {start + 1}--{start + 5}", font_size=34)
            rows = VGroup(*[VGroup(MathTex(rf"{i}.", font_size=24, color=QC.IDEA),
                                  wrapped_label(text, 12.0, 24, WHITE)).arrange(RIGHT, buff=0.2, aligned_edge=UP)
                           for i, text in enumerate(PROBLEMS[start:start + 5], start + 1)])
            rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            page = VGroup(head, rows).arrange(DOWN, buff=0.4)
            head.set_x(0)
            if page.height > 7.1:
                page.scale_to_fit_height(7.1)
            pages.append(page.move_to(ORIGIN))
        with self.voiceover(
            'Ten problems cover fixed-coefficient control variates, normal-shift importance sampling, finite-grid optional stopping, heat-equation stability, reverse-tape work, a hybrid gamma estimator, conditional multilevel complexity and the FFT grid constraint. The last two derive a single Gram-diagonal moment diagnostic and a one-date margin-conditioned price-loss bound. State the assumptions as part of each solution. Worked English and Chinese solutions are in the notes.'
        ) as vo:
            self.play(FadeIn(pages[0]), run_time=1.5)
            self.wait(max(1.0, vo.remaining() * 0.45))
            self.play(ReplacementTransform(pages[0], pages[1]))
        self.wait(3.0)
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
            'The notes identify the textbooks, original research and dated industry resource reports. Numerical examples are synthetic fixed-seed CPU runs with varying configurations: the parallel example uses multiple processes and the Part seventeen stopping reference uses two training threads. Published industry and quantum resource figures are external source claims, not local measurements.'
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def next_part(self):
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 17, Deep Pricing and Hedging", font_size=32, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "This part provides numerical methods and evidence for specific pricing problems, with explicit assumptions and unresolved error sources. <bookmark mark='a'/> Next is Part seventeen, deep pricing and hedging: learning price maps, studying high-dimensional equations and training hedging or stopping policies, with their own approximation and evaluation questions."
        ) as vo:
            self.play(FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
