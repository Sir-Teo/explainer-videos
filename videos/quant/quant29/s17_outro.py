from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant29.common import BAD, COMB, FORMULA, GOOD, GP_C, HURDLE, PART, RAND_C, RL_C, comma, load

DESK = [('10{,}000 standardised signals, each IC 0.01, equicorrelation 0.3: equal-weight IC?', 'under a feasible joint covariance, $0.01\\sqrt{10000/(1+9999\\cdot0.3)}\\approx0.01826$. Variance breadth is about 3.33, not independent trials'), ('GP reports training IC 0.08 after 25 generations. What evidence is needed?', 'fitness, all seeds and searches, unique evaluations and repeats, chronology and a complete validation protocol; count alone gives no universal hurdle'), ('An LLM agent reports Sharpe 3 on 2015--2022 stocks. First checks?', 'model and retrieval provenance, data vintages, prompts, human choices, outcome and execution timing, costs and valid fresh evaluation; a declared cutoff alone is insufficient'), ('40 selected alphas have fitted Sharpe 6. What live Sharpe follows?', 'no numerical live expectation follows. The Gaussian model needs true population strength, fixed pre-specified signals, known covariance and consistent periods; do not substitute selected training Sharpe'), ('A small-cap long book hedges with large-cap futures. What remains?', 'beta mismatch, size and sector exposures, cash-futures basis, funding, borrow and execution. Equal dollar notionals do not imply risk neutrality'), ('A proposed fiftieth alpha has annual Sharpe 0.3. Add it?', 'not decidable from that number. Use common period units, true incremental residual strength and selection-aware validation; the research threshold applies only to its specified approximate objective')]

PROBLEMS = ['With 6 fields, 5 unary operators, 7 time-series operators and correlation over 4 windows, and 4 binary operators, count trees of depth at most 2.', 'IID daily IC noise has standard deviation 0.10 over 500 days. Give the leading independent Gaussian maximum scale for 10{,}000 signed means; also count both selectable signs.', 'In the ideal independent, equal-risk, unconstrained fundamental-law toy, IC is 0.02 across 100 bets. Compute $IC\\sqrt{100}$ and its 365-day annualisation; state why this is not implied by 100 coins alone.', 'For feasible standardised equicorrelated signals with equal target correlation $c$, derive $c\\sqrt{N/(1+(N-1)\\rho)}$; evaluate $N=10000,c=0.01,\\rho=0.3$ and state the joint PSD restriction.', 'GP fitness is absolute mean IC minus 0.0005 per node. What gain pays for ten extra nodes? Does fitness monotonicity imply monotone raw IC?', 'An agent scores 500 hypotheses over 4 windows. Count 2{,}000 nominal evaluations and compare independent Gaussian maximum scales with 500. Explain why adaptive counts need further calibration.', 'For a fixed policy and an action-independent baseline conditional on state, prove $\\mathbb E[b\\nabla\\log\\pi(a)]=0$. Must every baseline lower variance?', 'Fixed equal initial notionals: long small caps, short index futures. Simple returns are $-20\\%$ and $-5\\%$. Compute P\\&L per dollar long before basis, costs and funding; distinguish a toy from attribution.', 'A chosen exponential IC half-life is 2 years, starting at 0.03. When is IC strictly below 0.01? Is the half-life established by three yearly observations?', '20 fixed independent Gaussian return coordinates have daily Sharpe 0.02, known covariance and 365 observation days. Compute population optimum and the plug-in approximation, daily and 365-day annualised.', '(qual) Derive the known-covariance Gaussian Sharpe identity and bounded-strength $K/T$ limit. For $f(S,K)=S/\\sqrt{S+K/T}$ derive the exact finite-addition quadratic/root and distinguish the first-order sufficient threshold.', '(qual) For standardised signals with positive definite $C$ and target correlations $c$, derive maximal Pearson IC $\\sqrt{c^\\top C^{-1}c}$, joint PSD feasibility, and the equal-IC equicorrelation special case.']


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("classic"), load("space"), load("random"), load("gp"), load("rl"), load("combine"),
                   load("decay"), load("theory"))
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def _rows(self, items, title):
        rows = VGroup()
        for j, (t, col) in items:
            rows.add(VGroup(MathTex(str(j), font_size=24, color=col), label(t, font_size=21)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(title, font_size=36).to_edge(UP, buff=0.3)
        rows.next_to(head, DOWN, buff=0.35)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        if rows.height > 6.4:
            rows.scale_to_fit_height(6.4)
        return head, rows

    def recap(self, cl, sp, r, g, rl, c, dc, th):
        best = r["best_by_n"][-1]
        groups = [
            [(r"formulaic alphas: adapted fields, ordinal ranks and idealised execution", FORMULA),
             (r"search space: repeated strings and rounded mean scores are not independent trials", FORMULA),
             (rf"random winner: training {best['train']:.3f}, labelled 2020 validation {best['valid']:+.3f}", RAND_C),
             (r"GP: penalised training fitness, three seeds and cached unique strings", GP_C),
             (rf"RL pool: training {rl['train']['ic']:.3f}, validation {rl['valid']['ic']:+.3f}; adaptive selection", RL_C),
             (r"agents: versioned author reports and unresolved information-set assumptions", GREY_A),
             (rf"combination: mean training return correlation {c['rho']:.2f}; participation ratio {c['n_eff']:.1f}", COMB)],
            [(r"counter: existing registrations through Part 29, 23{,}480; no new trial", HURDLE),
             (r"shuffle: fixed design, exchangeability assumption, no full-search extrapolation", HURDLE),
             (r"decay and China: distinguish reported context, stylised mechanisms and attribution", BAD),
             (r"High-Flyer and DeepSeek: scoped infrastructure and official-training cost reports", GREY_A),
             (r"humans: hypotheses, information provenance, selection and execution judgement", GOOD),
             (r"evaluation protocol and fixed arithmetic; sealed strategy result excluded", QC.HOUSE),
             (r"research: stated Gaussian regime; finite-addition versus first-order threshold", COMB)],
        ]
        with self.voiceover(f"Seven research lessons. The fields and ranking rules are adapted to a retrospective archive, with idealised timing. Repeated strings and rounded scores do not count independent ideas. The training-selected random winner scores {best['train']:.3f} then {best['valid']:+.3f} on labelled validation. GP optimises penalised training fitness; RL rewards marginal fitted-pool IC. Their search histories are adaptive. Agent papers supply versioned author reports. Correlation and participation ratios describe selected sample exposures, not independent trials or causal economic factors."):
            head, rows = self._rows(list(enumerate(groups[0], 1)), r"Part 29: research lessons")
            self.play(FadeIn(head), FadeIn(rows))
        self.clear_scene()
        with self.voiceover("Seven evaluation lessons. Existing registrations through this part total 23,480; restoration adds no market trial. The fixed shared shuffle does not replay the full adaptive search and supports no independent-count extrapolation. Horizon diagnostics, industry reports and crowding mechanisms need separate interpretations. Infrastructure comparisons and official training cost reports have stated boundaries. People still specify hypotheses, provenance and execution. The strategy result is excluded, and the fixed toy supplies arithmetic only. The Gaussian estimation model needs a fixed library and explicit regime; its exact finite-addition criterion belongs to an already approximate objective."):
            head, rows = self._rows(list(enumerate(groups[1], 8)), r"Part 29: evaluation lessons")
            self.play(FadeIn(head), FadeIn(rows))
        self.clear_scene()

    def desk(self):
        def page(items):
            return VGroup(*[desk_question(q,a,width=12.4,font_size=18) for q,a in items]).arrange(DOWN,buff=0.25)
        cards=page(DESK[:3])
        with self.voiceover("Three desk checks. The equal-correlation toy gives about 0.01826 IC, subject to joint covariance feasibility; its breadth is not independent trials. <bookmark mark='a'/> For GP, audit the full search and chronology, not just a tree count. <bookmark mark='b'/> For an LLM agent, model and retrieval provenance, dates, selection and costs matter; a declared cutoff alone is not proof of a clean historical information set.") as vo:
            self.play(FadeIn(cards[0]))
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.wait(0.4)
        self.clear_scene()
        cards=page(DESK[3:])
        with self.voiceover("Three more checks. A selected training Sharpe 6 does not identify expected live performance; do not plug it into a fixed-library theorem as true population strength. <bookmark mark='a'/> Dollar-neutral stock and futures notionals retain basis, size, beta and financing risks. <bookmark mark='b'/> A proposed annual Sharpe 0.3 alone cannot decide admission: true residual strength, period units, estimation, selection and costs all matter. Full English and Chinese solutions are in the notes.") as vo:
            self.play(FadeIn(cards[0]))
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.wait(0.4)
        self.clear_scene()

    def problems(self):
        def page(start,end,title):
            ps=problem_set(PROBLEMS[start:end],font_size=25,title=title)
            for number,row in enumerate(ps.rows,start+1):
                old=row[0]
                new=label(rf"{number}.",font_size=25,color=old.get_color())
                new.match_height(old).move_to(old).align_to(old,RIGHT)
                old.become(new)
            self.play(FadeIn(ps.head),FadeIn(ps.rows))
        with self.voiceover("Twelve problems, in three groups. The first six count the grammar, calculate independent Gaussian reference scales under stated assumptions, qualify the fundamental law, derive feasible equicorrelation, compare GP fitness and count nominal agent evaluations. <bookmark mark='a'/> Problems seven through ten prove the baseline identity, work a fixed hedge example, calculate an assumed half-life and evaluate the plug-in approximation in consistent daily units. <bookmark mark='b'/> Two qualifying problems prove the Gaussian concentration limit and exact finite-addition criterion for its approximate objective, then derive the optimal Pearson combination and joint covariance restriction. All twelve have full English and Chinese solutions in the notes.") as vo:
            page(0,6,r"Problems 1--6")
            vo.wait_until("a")
            self.clear_scene()
            page(6,10,r"Problems 7--10")
            vo.wait_until("b")
            self.clear_scene()
            page(10,12,r"Problems 11--12: qualifying")
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"estimation error in the optimizer; shrinkage and $1/N$", [30]),
            (r"the fundamental law, derived; combining alphas under costs, capacity and crowding", [31]),
            (r"the quant quake of 2007: crowded statistical arbitrage", [33]),
            (r"the finale: the mined combination's row, deflated by the full count", [43]),
        ])
        with self.voiceover(
            "These distinctions return in portfolio construction, where means and covariances are estimated; in trading costs and capacity, where book arithmetic must become executable orders; and in statistical-arbitrage crowding, where related exposures can unwind together. The finale's historical strategy results remain outside this presentation review. No future chapter reference supplies a performance verdict for an excluded experiment."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Kakushadze and Serur, \textit{151 Trading Strategies} (2018); Isichenko, \textit{Quantitative Portfolio "
             r"Management} (2021), chapters 2--3; Koza, \textit{Genetic Programming} (1992); Sutton and Barto, "
             r"\textit{Reinforcement Learning} (2018)"],
            [r"Brown (1976); Williams (1992); Allen and Karjalainen (1999); Kan and Zhou (2007); Kakushadze (2016); "
             r"Harvey and Liu (2015); Yu, Xue, Ao, Pan, He, Tu and He (2023); Wang et al.\ (2023), Alpha-GPT; "
             r"Tang et al.\ (2025), AlphaAgent; Li et al.\ (2025), R\&D-Agent-Quant",
             r"China, February 2024: as reported by Reuters, Bloomberg and Caixin; High-Flyer and DeepSeek: company "
             r"statements and press reports. Data: Binance public daily candles"])
        with self.voiceover(
            "The notes distinguish original ordinary calculations, explicitly fixed mathematical toys and versioned primary reports. The computational algorithms and existing registry remain unchanged. Public-source breadth does not by itself prove historical availability, and a paper's reported comparison is not our independent replication. The reading list covers symbolic search, policy gradients, estimation risk and the2023-2025 agent papers, with their specific limitations."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("research",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 30, Portfolio Construction", font_size=30, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The House now has tools for a formula grammar, random and adaptive searches, selected combinations and estimation-risk analysis. Counts record parts of the search history, while full information, selection and execution audits remain necessary. No sealed result was opened or scored. <bookmark mark='a'/> Next is portfolio construction: how noisy inputs influence an optimiser, and what specified constraints, shrinkage and validation can address."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
