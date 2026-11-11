from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant43.common import (ACT_C, BAD, COST_C, GOOD, HURDLE, LUCK_C, MKT_C, PART, REC_C, SKILL_C, load)

DESK = [
    (r"A selected fund won five years running among 2,000 funds. Skill?",
     r"specify the null, selection and dependence; a selected streak alone does not identify skill"),
    (r"When does aggregate active money trail passive money?",
     r"same defined universe and holdings identity, positive active share, and higher comparable active costs"),
    (r"Who benefits from manager skill?",
     r"the answer depends on allocation, scale, fees and information; the Bayesian competitive model has zero expected invested-dollar alpha"),
    (r"A strategy worked for fifty years. What should change now?",
     r"nothing follows automatically; examine mechanism stability, implementation and independent evaluation"),
    (r"Research Sharpe is 2. What is the future Sharpe?",
     r"there is no universal shrinkage coefficient; identify the estimand, selection model and independent evidence"),
    (r"Does clipping preserve Storey's raw expectation bound?",
     r"no: perfectly dependent uniform nulls at $\lambda=1/2$ give raw mean 1 but capped mean 1/2"),
]

PROBLEMS = [
    r"Same-universe passive share 40\%, market and passive return 8\%. Derive active gross return and the net gap if active costs are 1 percentage point higher.",
    r"Additive iid Gaussian active returns: zero skill, annual cost 0.75\%, tracking error 4\%. Compute the 10-year probability of positive cumulative active return.",
    r"For 2,000 marginal standard-normal null statistics, find expected counts above 1.96 and 3. Does counting require cross-test independence?",
    r"$m=1{,}000$, 300 $p$-values above $\lambda=.5$: compute the raw and capped null-share estimators. Is either a confidence bound?",
    r"Capped null estimate .8, two-sided level $.2$, right-tail share $.09$: compute the helper's positive-part tail estimate and explain its scope.",
    r"Bayesian allocation: posterior mean $.04$, fee $.01$, scale cost $.001$ per asset unit. Find allocation, conditional expected net alpha and fee revenue.",
    r"Weakly stationary returns: $\rho_1=.2$, all higher autocorrelations zero. Derive $VR(2)$ and $VR(5)$; explain why a sample VR is not a causal test.",
    r"Twenty valid standard-normal one-sided tests: derive the Bonferroni cutoff for family-wise error at most $.05$, without assuming independence.",
    r"All-null indicators at $\lambda=.5$, $m=1{,}000$, pairwise indicator correlation $.3$. Find raw-estimator variance and its large-$m$ limit.",
    r"Normal call with $F=K=100$, $\sigma_N\sqrt T=10$: price it. Separately, price a $K=-5$ call under a positive zero-rate Black forward with $F=10$.",
    r"(qual) Prove the raw null-share expectation identity and general covariance variance formula. Derive the independent case and give an explicit clipping counterexample.",
    r"(qual) For $A_t=\max(0,(\mathbb E_ta-f)/b)$ and conditionally mean-zero return noise, prove zero conditional expected invested-dollar alpha, including the boundary and tower-property result.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load('arith'), load('luck'), load('adaptive'), load('fdr'))
        self.series()
        self.lessons()
        self.formulas()
        self.desk()
        self.answers()
        self.basic_problems()
        self.advanced_problems()
        self.qualifying_problems()
        self.references()
        self.reproduce()
        self.finale()

    def _rows(self, texts, title, start=1):
        rows=VGroup()
        for i,text in enumerate(texts,start):
            n=label(str(i),font_size=23,color=HURDLE)
            t=wrapped_label(text,11.7,22)
            rows.add(VGroup(n,t).arrange(RIGHT,buff=.25,aligned_edge=UP))
        rows.arrange(DOWN,aligned_edge=LEFT,buff=.28)
        head=label(title,font_size=33)
        g=VGroup(head,rows).arrange(DOWN,buff=.45)
        if g.height>7.2:g.scale_to_fit_height(7.2)
        if g.width>13.2:g.scale_to_fit_width(13.2)
        return head,rows

    def recap(self,a,lk,ad,f):
        d=ad['by_decade'];q=f['q']['0.1']
        first=[r"Sharpe's identity needs a common universe and a market-weighted passive comparator",
               rf"additive Gaussian luck: positive active return after 15 years with probability {100*a['theory'][4]:.0f}\%",
               rf"selected null maximum: $t={lk['best_null']:.2f}$ among 2,000 simulated zero-alpha funds",
               r"tail-share decomposition is an estimator, with power, leakage and nonlinear-guard limitations",
               r"competitive Bayesian allocation: zero conditional expected invested-dollar alpha under the model",
               rf"sample autocorrelation: {d['1970']['ac1']:+.2f} in the 1970s, {d['2010']['ac1']:+.2f} in the 2010s; cause unidentified"]
        head,rows=self._rows(first,r"Part 43: findings with assumptions")
        with self.voiceover(
            "The final part, with assumptions retained. Sharpe's identity uses a common universe and market-weighted "
            "passive holdings. The additive Gaussian example shows how luck can survive costs. Selection among many "
            "simulated funds produces impressive null statistics. Tail-share estimates have identification and "
            "nonlinear-guard limits. Competitive Bayesian allocation can give zero expected dollar alpha under its "
            "model. Historical sample correlations differ, without identifying a single cause."
        ):
            self.play(FadeIn(head),FadeIn(rows[0]))
            self.play(LaggedStart(*[FadeIn(r,shift=RIGHT*.2)for r in rows[1:]],lag_ratio=.55),run_time=9)
        self.clear_scene()
        second=[r"an evidence record is designed before observing results: choices, costs, selection and monitoring",
                r"pricing comparisons require matched targets, metrics and evaluation tasks",
                r"raw Storey expectation bound does not automatically survive clipping",
                rf"BH at 10\%: {q['bh']} simulated selections, realised FDP {100*q['bh_fdr']:.0f}\%; FDR is an expectation",
                r"fresh simulation paths and next-day market quotes ask different validation questions",
                r"normal support can accommodate negative forwards; positive Black calls at $K\le0$ have a linear extension",
                r"proposed Rule 43: justify a benchmark and require independent net evidence for changes"]
        head,rows=self._rows(second,r"Part 43: the evidence discipline",7)
        with self.voiceover(
            "The evidence discipline. Design the record before observing results. Compare pricing errors only "
            "after matching their targets and definitions. Distinguish the raw null-share estimator from its cap, "
            "and realised false discovery proportion from its expectation. Fresh simulation paths do not test "
            "tomorrow's quotes. Distinguish negative underlying support from a nonpositive strike. The final "
            "governance proposal puts independent net evidence and risk review before a change from a justified benchmark."
        ):
            self.play(FadeIn(head),FadeIn(rows[0]))
            self.play(LaggedStart(*[FadeIn(r,shift=RIGHT*.2)for r in rows[1:]],lag_ratio=.55),run_time=10)
        self.clear_scene()

    def series(self):
        smap=series_map(current=None,done=PART)
        with self.voiceover(
            "The curriculum in one picture: seven acts followed by this finale, forty-three parts in total. Foundations, derivatives, rates "
            "and credit, asset pricing, the research craft, market machinery and the financial system. The map "
            "organises models and methods. Its completeness does not certify that every economic mechanism is "
            "identified or every proposed implementation is validated."
        ):
            self.play(FadeIn(smap))
        self.clear_scene()

    def lessons(self):
        cards=VGroup(
            desk_question(r"state the object",r"measure, benchmark, information, horizon and economic decision",width=12.4,font_size=19),
            desk_question(r"preserve the assumptions",r"a theorem, a finite simulation and an empirical estimate provide different evidence",width=12.4,font_size=19),
            desk_question(r"test the combined system",r"costs, leverage, liquidity and shared decisions can change outcomes in interaction",width=12.4,font_size=19)
        ).arrange(DOWN,buff=.25)
        with self.voiceover(
            "Three habits to keep. <bookmark mark='a'/> State the object: its measure, benchmark, information and "
            "decision. <bookmark mark='b'/> Preserve assumptions when moving from a theorem to a simulation or "
            "empirical estimate. A successful example is not a universal identification result. "
            "<bookmark mark='c'/> Test the combined system, because implementation costs, leverage, liquidity and "
            "shared decisions can change outcomes in interaction."
        ) as vo:
            self.play(FadeIn(cards[0]))
            for k,mark in enumerate(('a','b','c')):
                vo.wait_until(mark)
                if k:self.play(FadeIn(cards[k],shift=UP*.2))
        self.clear_scene()

    def formulas(self):
        head=label(r"Five formulas, with their domains",font_size=32)
        rows=VGroup(
            MathTex(r"w_Pr_P+w_Ar_A=r_M,\quad r_P=r_M,\ w_A>0\Rightarrow r_A=r_M",font_size=29,color=MKT_C),
            MathTex(r"P(X_T>0)=\Phi(-c\sqrt T/\sigma_{TE}),\quad X_T\sim N(-cT,\sigma_{TE}^2T)",font_size=29,color=LUCK_C),
            MathTex(r"\mathbb E\widetilde\pi_0=\pi_0+\sum_{H_1}P(p_i>\lambda)/[m(1-\lambda)]",font_size=29,color=HURDLE),
            MathTex(r"A_t=\max(0,(\mu_t-f)/b),\quad\mathbb E_t[A_t\eta_{t+1}]=0",font_size=29,color=ACT_C),
            MathTex(r"C_N=(F-K)\Phi(d)+s_N\varphi(d),\quad d=(F-K)/s_N\quad(r=0)",font_size=29,color=MKT_C)
        ).arrange(DOWN,buff=.42)
        VGroup(head,rows).arrange(DOWN,buff=.45)
        with self.voiceover(
            "The mathematical spine. A same-universe holdings identity. A stylised additive Gaussian return "
            "probability. The raw null-share expectation identity with valid uniform nulls and a fixed threshold. "
            "The competitive Bayesian dollar-allocation result with integrability. And the zero-rate normal "
            "forward call price. Each formula retains its own assumptions; they are not interchangeable claims "
            "about physical future returns."
        ):
            self.play(FadeIn(head),FadeIn(rows[0]))
            self.play(LaggedStart(*[FadeIn(r)for r in rows[1:]],lag_ratio=.35),run_time=4)
        self.clear_scene()

    def desk(self):
        cards=VGroup(*[desk_question(q,a,width=12.4,font_size=20)for q,a in DESK[:3]]).arrange(DOWN,buff=.24)
        with self.voiceover(
            "Six final desk questions. A selected winning fund needs an explicit null and selection analysis. "
            "<bookmark mark='a'/> Aggregate active and passive comparisons need matching holdings and costs. "
            "<bookmark mark='b'/> Who benefits from skill depends on information, allocation and scale; the "
            "competitive Bayesian result is one model. Full answers are in both languages in the notes."
        ) as vo:
            self.play(FadeIn(cards[0]));vo.wait_until('a');self.play(FadeIn(cards[1]))
            vo.wait_until('b');self.play(FadeIn(cards[2]))
        self.clear_scene()
        cards=VGroup(*[desk_question(q,a,width=12.4,font_size=20)for q,a in DESK[3:]]).arrange(DOWN,buff=.24)
        with self.voiceover(
            "A long historical record still needs a stable mechanism and independent evaluation. "
            "<bookmark mark='a'/> A research Sharpe of two has no universal future conversion factor. "
            "<bookmark mark='b'/> And clipping does not preserve the raw null-share expectation bound. The "
            "perfectly dependent all-null example is an explicit counterexample, not a claim about every dataset."
        ) as vo:
            self.play(FadeIn(cards[0]));vo.wait_until('a');self.play(FadeIn(cards[1]))
            vo.wait_until('b');self.play(FadeIn(cards[2]))
        self.clear_scene()

    def answers(self):
        rows=VGroup(
            label(r"Raw: $0$ or $2$ with equal probability; expectation $1$",font_size=29,color=HURDLE),
            label(r"Capped: $0$ or $1$ with equal probability; expectation $1/2$",font_size=29,color=BAD),
            wrapped_label(r"Uniform null marginals justify the raw identity. Clipping is nonlinear; the true null share is one.",11.8,23)
        ).arrange(DOWN,buff=.5)
        with self.voiceover(
            "The research pause. <bookmark mark='a'/> With all p-values equal to one uniform draw and lambda one "
            "half, the raw estimate is zero or two, each with probability one half. Its mean is one. "
            "<bookmark mark='b'/> The cap makes it zero or one, so its mean is one half, below the true null share "
            "of one. The raw identity uses marginal validity and linearity; the cap is a different random variable."
        ) as vo:
            self.play(FadeIn(rows[0]));vo.wait_until('a');vo.wait_until('b');self.play(FadeIn(rows[1]),FadeIn(rows[2]))
        self.clear_scene()

    def _problem_page(self,start,end,title):
        rows=VGroup()
        for i in range(start,end):
            rows.add(VGroup(label(rf"{i+1}.",font_size=23,color=HURDLE),wrapped_label(PROBLEMS[i],12.0,23)).arrange(RIGHT,buff=.2,aligned_edge=UP))
        rows.arrange(DOWN,aligned_edge=LEFT,buff=.34)
        head=label(title,font_size=34)
        group=VGroup(head,rows).arrange(DOWN,buff=.45)
        if group.height>7.15:group.scale_to_fit_height(7.15)
        if group.width>13.4:group.scale_to_fit_width(13.4)
        return head,rows

    def basic_problems(self):
        head,rows=self._problem_page(0,6,r"Problems 1--6: foundations")
        with self.voiceover(
            "The first six problems work through the holdings identity and cost gap, additive Gaussian luck, "
            "expected null counts, raw and capped null estimates, descriptive tail subtraction and competitive "
            "allocation. Each answer must state its assumptions. Full worked solutions are in the English and "
            "Chinese notes. Pause the video to solve the page before checking them."
        ):
            self.play(FadeIn(head),FadeIn(rows[0]))
            self.play(LaggedStart(*[FadeIn(r)for r in rows[1:]],lag_ratio=.3),run_time=4)
            self.wait(6)
        self.clear_scene()

    def advanced_problems(self):
        head,rows=self._problem_page(6,10,r"Problems 7--10: inference and model domains")
        with self.voiceover(
            "Four advanced problems: derive a stationary variance ratio; allocate a family-wise error budget; "
            "calculate raw-estimator variance under correlated indicators; and distinguish a normal at-the-money "
            "call from the linear extension of a positive Black call at a negative strike. Explain the inference "
            "and support assumptions as well as giving the numerical answers."
        ):
            self.play(FadeIn(head),FadeIn(rows[0]))
            self.play(LaggedStart(*[FadeIn(r)for r in rows[1:]],lag_ratio=.3),run_time=3)
            self.wait(6)
        self.clear_scene()

    def qualifying_problems(self):
        head,rows=self._problem_page(10,12,r"Problems 11--12: qualifying examination")
        with self.voiceover(
            "Two qualifying-exam problems. Prove the raw null-share expectation and covariance variance identities, "
            "derive the independent special case and give the clipping counterexample. Then prove the Bayesian "
            "competitive allocation result, including zero allocation, integrability and the tower-property "
            "orthogonality statement. The notes give complete bilingual derivations, not just final formulas."
        ):
            self.play(FadeIn(head),FadeIn(rows[0]),FadeIn(rows[1]))
            self.wait(6)
        self.clear_scene()

    def references(self):
        card=reference_card(
            [r"Lo, \textit{Adaptive Markets} (2017); Pedersen, \textit{Efficiently Inefficient} (2015); Ilmanen, \textit{Expected Returns} (2011)"],
            [r"Bachelier (1900); Sharpe (1991); Benjamini--Hochberg (1995); Carhart (1997); Storey (2002); Berk--Green (2004); Lo (2004)",
             r"Barras--Scaillet--Wermers (2010); Fama--French (2010); Berk--van Binsbergen (2015); McLean--Pontiff (2016); Pedersen (2018)",
             r"Data: French daily factors through 2020; authenticated public Surface summaries. Historical notices: CME Clearing 20-171 and 20-320; CFTC 8315-20."])
        with self.voiceover(
            "The references connect the arguments to their authors. Inputs here are the audited ordinary "
            "fixed-seed examples, French daily returns through twenty twenty, authenticated earlier public "
            "pricing summaries and explicit analytical calculations. The historical energy episode uses dated "
            "CME Clearing notices and the CFTC report. Exact sources and evaluation limits are listed in the notes."
        ):self.play(FadeIn(card))
        self.clear_scene()

    def reproduce(self):
        cards=VGroup(
            desk_question(r"approved inputs",r"eight once-only ordinary originals; eight earlier public derived hashes verified before reuse",width=12.4,font_size=19),
            desk_question(r"barriers",r"unknown and excluded names fail before path/count access; missing or changed ordinary outputs do not compute implicitly",width=12.4,font_size=19),
            desk_question(r"future work",r"independently designed data collection and evaluation, with the assumptions and complete result family reported",width=12.4,font_size=19)
        ).arrange(DOWN,buff=.25)
        with self.voiceover(
            "Reproducibility also has boundaries. <bookmark mark='a'/> The eight ordinary originals each ran once, "
            "and all eight reused public derived hashes were verified against prior approvals. "
            "<bookmark mark='b'/> Unknown and excluded names are blocked before path or counted cache access; "
            "missing or changed outputs cannot trigger implicit computation. The complete original compute "
            "command must not be used blindly, because it includes excluded strategy-opening functions. "
            "<bookmark mark='c'/> Future research needs its own justified evaluation design and full reporting. "
            "A reproducible byte sequence alone does not establish economic truth."
        ) as vo:
            self.play(FadeIn(cards[0]))
            for k,mark in enumerate(('a','b','c')):
                vo.wait_until(mark)
                if k:self.play(FadeIn(cards[k],shift=UP*.2))
        self.clear_scene()

    def finale(self):
        chart=house_chart(PART,lit=tuple(DESKS.keys())).scale(.84).to_edge(UP,buff=.3)
        end=wrapped_label(r"Quant, Built: forty-three parts. Thank you for building it with us.",12.4,29,QC.IDEA).to_edge(DOWN,buff=.4)
        with self.voiceover(
            "The House ends as a map of quantitative work: models with assumptions, proofs with domains, "
            "experiments with selection and uncertainty, and decisions with implementation constraints. No one "
            "formula settles whether a particular manager or strategy can beat a justified benchmark after costs. "
            "The durable habit is to define the claim, preserve the information boundary and evaluate before "
            "changing the decision. <bookmark mark='a'/> That is the end of Quant, Built. Thank you for building it with us."
        ) as vo:
            self.play(FadeIn(chart));vo.wait_until('a');self.play(FadeIn(end))
        self.wait(2)
        self.clear_scene()
