from __future__ import annotations

import numpy as np
from explainer.quant import *  # noqa: F403
from videos.quant.quant20.common import PART, RISKY, BAD, GOOD, LOGIT, GBMC, load, lesson_cards


class Altman(VoiceoverScene):
    def construct(self):
        self.history()
        self.zones()
        self.refit()
        self.protocol()

    def history(self):
        title, cards = lesson_cards("8. Altman's Z: a discriminant score", [
            ('The 1968 setting', '66 manufacturing firms, half bankrupt; a selected case-control sample'),
            ('Five ratios', 'WC/TA, RE/TA, EBIT/TA, market equity/TL and sales/TA'),
            ('The conventional score', '$Z=1.2X_1+1.4X_2+3.3X_3+0.6X_4+X_5$'),
            ('Historical zones', 'Below 1.81: distress; 1.81--2.99: grey; at least 2.99: safe. These names do not guarantee outcomes.'),
        ])
        with self.voiceover("Chapter eight. Edward Altman's nineteen sixty-eight study used sixty-six manufacturing firms, half bankrupt, to construct a linear discriminant score. The five ratios describe working capital, retained earnings, operating profit, the market equity cushion and sales. This familiar coefficient convention uses ratios in ordinary units. <bookmark mark='a'/> The original sample was deliberately balanced and selected. Its bankruptcy share is not a population annual default rate. The score ranks financial profiles; it is not itself a number between zero and one. <bookmark mark='b'/> The familiar distress, grey and safe zones are historical conventions. They do not certify safety for today's issuers, for banks or for another country. Changing accounting conventions or the equity-value definition changes the inputs, and a useful application needs target-population validation. We now apply the fixed formula to invented financial ratios, so every subsequent event rate on this chapter's screen is synthetic.") as vo:
            self.play(FadeIn(title), FadeIn(cards[0]))
            vo.wait_until('a'); self.play(FadeIn(cards[1]))
            vo.wait_until('b'); self.play(FadeIn(cards[2]))
            if len(cards) > 3: self.play(FadeIn(cards[3]))
        self.wait(0.5)
        self.clear_scene()

    def zones(self):
        a = load('synthetic_credit_example')['zones']
        title, cards = lesson_cards('Historical zones, synthetic events', [
            ('Distress zone', f"{a['events'][0]} events / {a['n'][0]} observations; {100*a['rate'][0]:.2f}\\%"),
            ('Grey zone', f"{a['events'][1]} events / {a['n'][1]} observations; {100*a['rate'][1]:.2f}\\%"),
            ('Safe zone', f"{a['events'][2]} events / {a['n'][2]} observations; {100*a['rate'][2]:.2f}\\%"),
            ('Interpretation', 'One fixed synthetic evaluation sample; zone names are not probability forecasts'),
        ])
        with self.voiceover("These are actual counts from the fixed synthetic evaluation sample, grouped by the historical zones. Every rate has its event count and denominator. <bookmark mark='a'/> The synthetic population was defined before fitting, with event probabilities depending on leverage, profitability, the equity cushion and a nonlinear interaction. We have not estimated that law from real bankruptcies. <bookmark mark='b'/> A lower Z can rank risk under this invented law, but neither that ranking nor the displayed zone rates establish performance on real firms. Sparse events make rates noisy. Even in one stable population, a different independent sample would produce different counts. A practical assessment would report confidence intervals and test transport to the intended issuer population, rather than treating a historical zone name as a guarantee.") as vo:
            self.play(FadeIn(title), FadeIn(cards[0]))
            vo.wait_until('a'); self.play(FadeIn(cards[1]))
            vo.wait_until('b'); self.play(FadeIn(cards[2]))
            if len(cards) > 3: self.play(FadeIn(cards[3]))
        self.wait(0.5)
        self.clear_scene()

    def refit(self):
        a = load('synthetic_credit_example')['results']['selection']['auc']
        title, cards = lesson_cards('Reweighting changes the statistical question', [
            ('Original discriminant', 'Weights separate selected groups; higher Z conventionally means safer'),
            ('Five-ratio logit', 'An intercept and standardized inputs model synthetic event log-odds; positive means riskier'),
            ('Selection-sample AUC', f"Fixed Z {a['altman']:.3f}; five-ratio logit {a['five_ratio_logit']:.3f}"),
            ('Coefficient comparison', 'Sign, objective, units, correlation and regularization all differ; magnitudes are not directly comparable'),
        ])
        with self.voiceover(f"Keep the same five ratios and fit a logistic model on the synthetic fit sample only. Fit-sample clipping limits, means and scales are frozen before selection or evaluation. <bookmark mark='a'/> The new model estimates event log-odds with an intercept and a fixed small ridge penalty. Its positive coefficients mean more event risk, while a positive contribution to Z conventionally means greater safety. A sign reversal alone does not make coefficient magnitudes comparable: the objective, units, covariance and regularization differ. <bookmark mark='b'/> The selection-sample AUC for fixed Z is {a['altman']:.3f}, and for the five-ratio logit {a['five_ratio_logit']:.3f}. These observed numbers describe this invented population. They do not show that modern accounting weights beat the original formula in a market test. The next chapter adds inputs and a nonlinear learner while keeping the population and sample boundaries explicit.") as vo:
            self.play(FadeIn(title), FadeIn(cards[0]))
            vo.wait_until('a'); self.play(FadeIn(cards[1]))
            vo.wait_until('b'); self.play(FadeIn(cards[2]))
            if len(cards) > 3: self.play(FadeIn(cards[3]))
        self.wait(0.5)
        self.clear_scene()

    def protocol(self):
        title, cards = lesson_cards('Before reporting an accounting model', [
            ('Freeze the population and target', 'Entity resolution, event dates, outcome window and censoring'),
            ('Freeze available inputs', 'As-filed accounts and publication lags; fit preprocessing only on the fit sample'),
            ('Select before evaluating', 'Choose settings using selection data; preserve an independent evaluation sample'),
            ('Report limits', 'Ranking, calibration, event counts, dependence and uncertainty; no causal coefficient claims'),
        ])
        with self.voiceover("Pause and predict. Why is a high score on the sample used to fit the weights insufficient? <bookmark mark='a'/> Fitting can exploit noise, and repeated tuning can overfit selection data too. In real accounting panels, later information can also leak through restatements, matching rules or a target window that crosses a split date. <bookmark mark='b'/> Freeze the population, event, horizon, feature availability, preprocessing and model selection before evaluation. Then report ranking and probability calibration separately, with event counts and uncertainty. Treat a learned coefficient as a conditional association in the fitted model, not an intervention on a firm's balance sheet. Our independent synthetic samples make these boundaries easy to see, but do not remove the harder availability and dependence problems of real issuer data.") as vo:
            self.play(FadeIn(title), FadeIn(cards[0]))
            vo.wait_until('a'); self.play(FadeIn(cards[1]))
            vo.wait_until('b'); self.play(FadeIn(cards[2]))
            if len(cards) > 3: self.play(FadeIn(cards[3]))
        self.wait(0.5)
        self.clear_scene()
