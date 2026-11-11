from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant27.common import (BAD, COIN, COMPLEX, GOOD, HURDLE, LINEAR, MOM, NET, OOS_C, PART, TREE, comma,
                                         load)

DESK = [('Binary-signal idealisation: $R^2=0.5\\%$, 500 independent bets. Annual Sharpe?', '$\\sqrt{12(500)(0.005)/0.995}\\approx5.49$. This population model is not a universal mapping from measured out-of-sample $R^2$.'), ('More parameters than observations and a perfect training fit. Useless?', 'Rank, regularisation, feature scaling, signal and noise matter. Compare out-of-sample risk and a matched-information baseline.'), ('Direction accuracy 55\\%. Tradable?', 'Need move sizes, base rate, risk, dependence, turnover, execution and costs. Accuracy alone is insufficient.'), ('Two years of returns with annual Sharpe 1. What uncertainty?', 'Under an IID small-per-period-Sharpe approximation, SE is about $1/\\sqrt2=0.71$ annually. Dependence, selection and paired differences need their own inference.'), ('A meta-model keeps one bet in ten and doubles precision. Better?', 'Compare net profit and risk per unit time, including lost breadth, sizes and overlapping positions. Precision alone cannot decide.'), ('A nominal 90\\% interval covers 70\\% in a selected regime. What follows?', 'Marginal coverage is not regime-conditional coverage. Check independent calibration, exchangeability and the actual adaptive boundary conventions.')]

PROBLEMS = ['Binary signal $S=\\pm1$, $r=aS+\\varepsilon$: derive population $R^2$, sign-strategy Sharpe and independent-bet scaling.', 'Paired means: derive $\\operatorname{Var}(A-B)$. For unit SDs, correlation 0.8 and 100 independent pairs, find the SE.', 'Use the SVD to derive the zero-penalty ridge limit. State when it interpolates.', 'Gaussian random Fourier features: derive the kernel expectation and pointwise Monte Carlo error rate.', 'For $M=1-w^\\top R$, derive the unconditional canonical weights and the correctly normalised Hansen--Jagannathan bound.', 'Brownian drift $\\mu$, volatility $\\sigma>0$, barriers $\\pm b$: derive the upper-first probability without a time limit.', 'For noninteger $0<d<1$, derive fractional-filter weights and their asymptotic decay. What does truncation not prove?', 'Inclusive labels $[i,i+h]$: derive interior concurrency and uniqueness. Compare half-open spans and independent sample size.', 'Prove row-permutation equivariance of attention. Distinguish fixed slot embeddings from identities that move with assets.', 'Derive the adaptive-level telescoping identity and its bounded-state condition. Give a finite-maximum counterexample.', '(qual) Prove split-conformal marginal coverage with independent fitting and exchangeable scores; include ties and $k>n$.', '(qual) Derive finite-sample Gaussian OLS/minimum-norm excess risks and proportional limits. For unit signal and noise, compare ridgeless risk with zero.']


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("zoo"),load("sdf"),load("images"),load("conformal"))
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def _rows(self,items,title):
        rows=VGroup(*[VGroup(MathTex(str(j),font_size=28,color=col),wrapped_label(text,11.5,26)).arrange(RIGHT,buff=.3) for j,(text,col) in items]).arrange(DOWN,aligned_edge=LEFT,buff=.25)
        head=label(title,font_size=36).to_edge(UP,buff=.3)
        if rows.height>6.1: rows.scale_to_fit_height(6.1)
        if rows.width>13: rows.scale_to_fit_width(13)
        rows.next_to(head,DOWN,buff=.35)
        return head,rows

    def recap(self,z,s,im,c):
        r2s=[z["rows"][m]["r2"] for m in z["models"]]
        pages=[[
            (r"Weak forecasts and breadth: an explicit binary-signal idealisation",MOM),
            (rf"Crypto zoo: zero-benchmark $R^2$ {100*min(r2s):.1f}\% to {100*max(r2s):.1f}\%; imperfect calendar boundaries",BAD),
            (r"Liquidity splits and turnover scenarios: descriptive, gross and capacity-limited",COIN),
            (r"Random features and positive ridge: capacity does not imply interpolation",COMPLEX),
            (r"Synthetic reversal: the baseline had different information",HURDLE),
            (r"Gaussian proportional limits: excess risk differs from total error",COMPLEX),
            (r"Autoencoder: contemporaneous factor extraction differs from forecasting",LINEAR)], [
            (rf"Adversarial portfolio: market correlation {s['corr_mkt_adv']:.2f}; no general SDF certificate",NET),
            (r"Attention: interactions beyond already ranked inputs; one selected heatmap",NET),
            (rf"Chart CNN gross Sharpe {im['sr_cnn']:.2f}, momentum {im['sr_mom']:.2f}; no isolated causal diagnosis",TREE),
            (r"Foundation transfer: distinguish target, training chronology and adaptation",OOS_C),
            (r"Practitioner tools: finite filters, daily-close barriers and concurrency",COIN),
            (rf"Split coverage {100*c['0.1']['cover']:.1f}\% is descriptive; adaptive boundary rules matter",GOOD),
            (r"Governance and protocol: existing registrations, no sealed scores",QC.HOUSE)]]
        for i,items in enumerate(pages):
            head,rows=self._rows(list(enumerate(items,1+7*i)),r"Part 27 in fourteen lines")
            if i == 0:
                with self.voiceover("Part twenty-seven in fourteen qualified lines. Weak signals and breadth need a stated data-generating model. The crypto illustration retains calendar and execution limitations. Liquidity differences and fee scenarios are descriptive. Positive ridge does not automatically interpolate. The artificial reversal baseline has a different information set. Gaussian risk limits separate excess error from total mean squared error. Autoencoder total fit extracts factors using contemporaneous returns, rather than forecasting those returns."):
                    self.play(FadeIn(head),FadeIn(rows))
            else:
                with self.voiceover("The adversarial portfolio's market correlation does not certify pricing moments or identify a cause. Attention adds interactions beyond already ranked inputs, and a selected heatmap is not a general interpretation. Chart comparisons do not isolate why an architecture succeeds or fails. Foundation transfer needs an explicit target, chronology and adaptation protocol. Practitioner tools require precise finite-sample conventions. Empirical conformal coverage is descriptive when assumptions fail, and adaptive boundary rules matter. Governance and full-protocol evaluation close the part; the sealed experiment remains unopened and unscored."):
                    self.play(FadeIn(head),FadeIn(rows))
            self.clear_scene()

    def desk(self):
        def page(items,start):
            head=label(r"Six desk questions",font_size=34).to_edge(UP,buff=.3)
            rows=VGroup()
            for j,(question,answer) in enumerate(items,start):
                body=VGroup(wrapped_label(question,11.5,29,QC.HOUSE),wrapped_label(answer,11.5,25,GREY_A)).arrange(DOWN,aligned_edge=LEFT,buff=.17)
                row=VGroup(label(rf"{j}.",font_size=29,color=QC.HOUSE),body).arrange(RIGHT,buff=.28,aligned_edge=UP);rows.add(row)
            rows.arrange(DOWN,aligned_edge=LEFT,buff=.42)
            if rows.height>6.25:rows.scale_to_fit_height(6.25)
            rows.next_to(head,DOWN,buff=.4)
            self.play(FadeIn(head),FadeIn(rows))
        with self.voiceover('Six desk questions. The binary-signal idealisation gives about five point four nine annual Sharpe for five hundred independent bets, rather than a universal promise from measured R squared. Perfect training fit alone is inconclusive. Direction accuracy alone omits move sizes, risk and costs.'):
            page(DESK[:3],1)
        self.clear_scene()
        with self.voiceover("Two years give an approximate annual Sharpe standard error of point seven one only under suitable independent-return assumptions. A meta-model must justify lost breadth and costs rather than precision alone. A regime's coverage need not equal marginal coverage. Check independent calibration, exchangeability and the actual adaptive implementation before claiming a guarantee."):
            page(DESK[3:],4)
        self.clear_scene()

    def problems(self):
        def page(start,end):
            ps=problem_set(PROBLEMS[start:end],font_size=26)
            for number,row in enumerate(ps.rows,start+1):
                old=row[0];new=label(rf"{number}.",font_size=26,color=old.get_color());new.match_height(old).move_to(old).align_to(old,RIGHT);old.become(new)
            self.play(FadeIn(ps.head),FadeIn(ps.rows))
        with self.voiceover("The first six problems derive the explicit binary-signal calculation, a paired-mean standard error, the zero-penalty ridge limit, a Gaussian random-feature kernel, canonical linear discount-factor weights and Brownian barrier probabilities. Each solution states the information and mathematical assumptions."):
            page(0,6)
        self.clear_scene()
        with self.voiceover("Problems seven through ten derive fractional-weight decay, inclusive-label uniqueness, attention equivariance and the adaptive-level telescoping identity. The adaptive solution includes a counterexample for finite-maximum boundary rules. Uniqueness weights do not automatically count independent observations."):
            page(6,10)
        self.clear_scene()
        with self.voiceover("Two qualifying problems establish the split-conformal rank theorem under independent fitting and exchangeable scores, then derive finite-sample and proportional-limit Gaussian regression risk. The last comparison fixes signal and noise explicitly. All twelve problems have full English and Chinese solutions in the notes."):
            page(10,12)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"text and language models: the same validation, and a new look-ahead bias", [28]),
            (r"alpha miners: the zoo, automated, against the counter", [29]),
            (r"Marchenko--Pastur again: cleaning covariance matrices for portfolios", [30]),
            (r"costs, capacity and the fundamental law of breadth", [31]),
            (r"model risk as a firm's problem: who may change a model", [34]),
            (r"the finale: research evidence, selection and the recorded count", [43]),
        ])
        with self.voiceover(
            'These questions return in text models, automated alpha search, covariance estimation, costs and capacity, and firm model governance. Later parts must keep the same discipline: clear information clocks, honest search accounting and inference matched to the implementation. The finale can discuss the research record without reopening or scoring sealed experiments.'
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Kelly and Xiu, \textit{Financial Machine Learning} (2023); Lopez de Prado, \textit{Advances in Financial "
             r"Machine Learning}, ch.\ 2--5, 10; Hastie, Tibshirani and Friedman, \textit{The Elements of Statistical "
             r"Learning}; Goodfellow, Bengio and Courville, \textit{Deep Learning}; Isichenko, \textit{Quantitative "
             r"Portfolio Management}, ch.\ 2"],
            [r"Marchenko and Pastur (1967); Grinold (1989); Vovk, Gammerman and Shafer (2005); Rahimi and Recht (2007); "
             r"Welch and Goyal (2008); Zaheer et al.\ (2017); Dobriban and Wager (2018); Lei et al.\ (2018); Belkin, Hsu, "
             r"Ma and Mandal (2019); Kelly, Pruitt and Su (2019); Bartlett, Long, Lugosi and Tsigler (2020); Gu, Kelly "
             r"and Xiu (2020, 2021); Israel, Kelly and Moskowitz (2020)",
             r"Gibbs and Cand\`es (2021); Giannone, Lenza and Primiceri (2021); Hastie, Montanari, Rosset and Tibshirani "
             r"(2022); Leippold, Wang and Zhou (2022); Mei and Montanari (2022); Avramov, Cheng and Metzker (2023); "
             r"Jiang, Kelly and Xiu (2023); Chen, Pelger and Zhu (2024); Kelly, Malamud and Zhou (2024); Ansari et al.\ "
             r"(2024); Das et al.\ (2024); Nagel (2025); Kelly, Kuznetsov, Malamud and Xu (2025); Shi et al.\ (2025). "
             r"Data: Binance public archive; Amit Goyal; Yahoo Finance"])
        with self.voiceover(
            "The textbooks and papers distinguish published evidence from our smaller illustrations. Gu, Kelly and Xiu's stock results and the Kronos benchmark improvements are author-reported, not replicated here. The January sixteen, twenty twenty-five SEC release documents the dated firm settlement. Numerical illustrations use labelled mathematical examples or successfully verified ordinary originals. The panel and sealed experiment originals are excluded."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("research",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 28, Text, LLMs and Alternative Data", font_size=30, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The House now has a model shop: every learner from least squares to a transformer, the theory that says "
            "when size helps, and the discipline that says when to believe it. It has learned that the hardest part "
            "of machine learning for returns is not the model but the test. <bookmark mark='a'/> Next, Part "
            "twenty-eight: text, language models and alternative data. Models that read the news and the Fed, and the "
            "subtle ways in which a model trained on the internet already knows how the story ends."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
