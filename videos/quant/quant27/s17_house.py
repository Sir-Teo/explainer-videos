from __future__ import annotations
from explainer.quant import *
from explainer.quant.house import ml as ML
from videos.quant.quant27.common import BAD, COMPLEX, GOOD, HURDLE, LINEAR, NET, PART, TREE, house_lab, load

class House(VoiceoverScene):
    def construct(self):
        self.card()
        self.sheet(load("zoo"), load("sdf"), load("images"), load("conformal"))
        self.lab()
        self.module()
        self.rule()
        self.test()

    def card(self):
        c = chapter_card(16, r"Rule 27: the model desk", r"What evidence supports a learned forecast?", part=PART)
        with self.voiceover("Chapter sixteen. The House's twenty-seventh rule: evaluate the full forecasting protocol, including its limitations."):
            self.play(FadeIn(c))
        self.clear_scene()

    def sheet(self, z, s, im, c):
        r2s = [z["rows"][m]["r2"] for m in z["models"]]
        entries = [
            (rf"Crypto zoo: zero-benchmark out-of-sample $R^2$ from {100*min(r2s):.1f}\% to {100*max(r2s):.1f}\%", BAD),
            (r"Original date-integer cuts do not calendar-purge seven-day labels", HURDLE),
            (r"Ridge theory: proportional Gaussian limits; finite numerical quadrature", COMPLEX),
            (r"Autoencoder total fit uses contemporaneous test returns to extract factors", LINEAR),
            (rf"Adversarial portfolio: gross Sharpe {s['sr_adv']:.2f}, market correlation {s['corr_mkt_adv']:.3f}; not a pricing certificate", NET),
            (rf"Chart CNN: gross Sharpe {im['sr_cnn']:.2f}; momentum {im['sr_mom']:.2f}; selected short sample", TREE),
            (rf"Empirical split coverage {100*c['0.1']['cover']:.1f}\%; calibration reused selection labels", HURDLE),
            (r"Adaptive finite quantiles do not establish arbitrary-sequence coverage", BAD),
            (r"Panel and sealed experiment originals remain excluded; no sealed scores", GOOD)]
        title = label(r"Evidence and its scope", font_size=34).to_edge(UP, buff=.3)
        rows = VGroup(*[wrapped_label(text, 12.0, 25, col) for text,col in entries]).arrange(DOWN, aligned_edge=LEFT, buff=.19)
        if rows.height>6.15: rows.scale_to_fit_height(6.15)
        rows.next_to(title,DOWN,buff=.3)
        with self.voiceover(f"The evidence sheet separates measurements from guarantees. The original crypto zoo's zero-benchmark R squared ranges from {100*min(r2s):.1f} to {100*max(r2s):.1f} percent. Calendar label boundaries remain imperfect. Ridge theory is asymptotic, and autoencoder total fit extracts factors from contemporaneous test returns. The adversarial portfolio and chart network are descriptive gross-return illustrations. Split coverage is {100*c['0.1']['cover']:.1f} percent, but reused calibration labels prevent the standard theorem from certifying it. Finite adaptive quantiles lack a universal sequence guarantee. The panel and sealed experiment originals remain excluded."):
            self.play(FadeIn(title),FadeIn(rows))
        self.clear_scene()

    def lab(self):
        card=house_lab(r"Asymptotic Gaussian ridge excess risk", ML.ridge_risk_theory, "atom = max", 9, width=10.6)
        with self.voiceover("This unchanged House routine evaluates proportional-limit Gaussian excess prediction risk. Fresh observation noise is excluded. The zero-eigenvalue atom contributes lost signal, while the positive spectrum contributes bias and variance. The integrals use finite numerical quadrature, and finite simulation draws need not agree exactly. The misspecified helper uses a different convention: total mean squared error, including noise."):
            self.play(FadeIn(card))
        self.clear_scene()

    def module(self):
        chart=house_chart(PART,lit=("research",)).scale(.6).to_edge(UP,buff=.25)
        entries=[r"Linear models, trees and networks: competing inductive biases", r"Random features and kernels: capacity and scaling assumptions", r"Gaussian ridge limits: a mathematical yardstick", r"Autoencoders, discount-factor portfolios, sets and images", r"Activity bars, fractional filters and overlapping labels", r"Calibration and scoring: guarantees require their assumptions"]
        rows=VGroup(*[wrapped_label(t,11.8,25,QC.HOUSE) for t in entries]).arrange(DOWN,aligned_edge=LEFT,buff=.24).next_to(chart,DOWN,buff=.3)
        if rows.height>4.4: rows.scale_to_fit_height(4.4)
        with self.voiceover("The model shop now contains linear models, trees and networks; random features and kernels; Gaussian risk limits; autoencoders, discount-factor portfolios, set models and chart images. It also contains activity bars, fractional filters, overlapping-label diagnostics and calibration tools. Each comes with a stated information set and mathematical scope."):
            self.play(FadeIn(chart),FadeIn(rows))
        self.clear_scene()

    def rule(self):
        head=label(r"Rule 27: judge the complete protocol",font_size=36,color=QC.HOUSE).to_edge(UP,buff=.45)
        rows=VGroup(*[wrapped_label(t,11.7,29) for t in [r"Match information, tuning effort and simple baselines",r"Respect availability clocks, actual label spans and selection",r"Report paired uncertainty, dependence and search history",r"State calibration assumptions, execution, costs and capacity",r"Distinguish descriptive fit from a deployable forecast"]]).arrange(DOWN,aligned_edge=LEFT,buff=.38).next_to(head,DOWN,buff=.65)
        with self.voiceover("Rule twenty-seven. Judge the complete protocol. Match information, tuning effort and simple baselines. Respect availability clocks, actual label spans and selection. Report paired uncertainty, dependence and the search history. State calibration assumptions, execution, costs and capacity. Distinguish descriptive fit from a forecast that could have been made and traded at the time. A fashionable architecture and a narrow empirical interval do not supply missing assumptions."):
            self.play(FadeIn(head),FadeIn(rows))
        self.clear_scene()

    def test(self):
        cases=[(r"Perfect training fit",r"Check rank, regularisation, risk and a matched baseline"),(r"Two years of competing forecasts",r"Use paired returns and justified dependence and selection adjustments"),(r"Near-nominal interval coverage",r"Check independent calibration and the implementation's boundary rules"),(r"Synthetic reversal comparison",r"Give every model the same lagged information before attributing failure")]
        cards=VGroup(*[desk_question(q,a,width=6.0,font_size=28) for q,a in cases]).arrange_in_grid(rows=2,cols=2,buff=.4)
        if cards.height>6.8: cards.scale_to_fit_height(6.8)
        with self.voiceover("Apply the rule. Perfect training fit alone decides little; check rank, regularisation and out-of-sample risk. A short comparison needs paired returns and justified inference. Near-nominal coverage needs an independently calibrated predictor and correct boundary conventions. A synthetic reversal comparison needs the same lagged information for every learner. These are questions for evaluating evidence, rather than new historical strategy tests."):
            self.play(FadeIn(cards))
        self.clear_scene()
