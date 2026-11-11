from __future__ import annotations

import numpy as np
from explainer.quant import *  # noqa: F403
from videos.quant.quant20.common import PART, RISKY, BAD, GOOD, LOGIT, GBMC, load, lesson_cards, grid_fn, surf3d_axes, ask, fit_right


class Models(VoiceoverScene, ThreeDScene):
    def construct(self):
        self.setup_example()
        self.task()
        self.trees()
        self.roc()
        self.scores()
        self.calibration()
        self.surface(self.example)
        self.interpretation()

    def setup_example(self):
        self.example = load("synthetic_credit_example")

    def task(self):
        title, cards = lesson_cards('9. Fit, select, evaluate: an invented population', [
            ('Declared before fitting', 'One fixed nonlinear Bernoulli law; no real issuer observations or default labels'),
            ('Independent samples', 'Fit: 8,000; selection: 4,000; evaluation: 6,000. Fixed seeds 202001--202003'),
            ('Fit and select', 'Fit-only clipping and scaling; logit with fixed ridge; depth-3 boosting with selection early stopping'),
            ('Boundary', 'The evaluation sample is generated after selection. No market trial is registered; no sealed experiment is opened.'),
        ])
        with self.voiceover("Chapter nine. A logit and boosted trees, demonstrated on an invented population. The fixed law makes event risk depend on leverage, profit, the equity cushion and a nonlinear interaction. Twelve financial inputs are generated, with total equity value kept consistent with assets, leverage and the cushion. <bookmark mark='a'/> We use eight thousand independent observations for fitting, four thousand for selecting the stopping point, and six thousand for evaluation, from fixed independent seeds. Only the fit sample determines clipping limits, means and scales. The logit uses a fixed small ridge penalty. The House's boosting algorithm fits up to two hundred forty depth-three trees and uses selection loss for early stopping. <bookmark mark='b'/> The evaluation sample is generated after that selection. The data law, seeds and learner settings are fixed before running the example; we report the resulting numbers without choosing a favorable seed. This is a stationary synthetic classification lesson, not a calendar backtest or evidence of bankruptcy forecasting. It registers no market trial and opens no sealed firm-year experiment.") as vo:
            self.play(FadeIn(title), FadeIn(cards[0]))
            vo.wait_until('a'); self.play(FadeIn(cards[1]))
            vo.wait_until('b'); self.play(FadeIn(cards[2]))
            if len(cards) > 3: self.play(FadeIn(cards[3]))
        self.wait(0.5)
        self.clear_scene()

    def trees(self):
        title, cards = lesson_cards('What the learners can represent', [
            ('Logit', '$p(x)=1/(1+e^{-\\beta_0-\\beta^\\top x})$: linear log-odds in the supplied inputs'),
            ('Boosted trees', '$F_K(x)=F_0+\\eta\\sum_k f_k(x)$: histogram splits and Newton leaf values'),
            ('Interactions', 'A tree can branch on leverage and profitability; a logit can include an explicitly engineered interaction'),
            ('Selection is not assessment', f"Selected trees: {self.example['selected_trees']}. Stop using selection loss; evaluate once afterward."),
        ])
        with self.voiceover("The two learners use the same twelve inputs. A plain logit adds contributions to log-odds. It does not automatically create an interaction, but an analyst can add interaction terms or nonlinear basis functions before fitting. <bookmark mark='a'/> Each small tree partitions the input space and adds a leaf value to the log-odds. Successive trees use gradients and curvature of the loss. Their branches can represent the invented interaction between leverage and weak profitability. More flexible representation also creates more opportunities to fit noise. <bookmark mark='b'/> We use selection loss to choose the stopping point. That makes the selection sample part of model development. Its score is not an independent final assessment. Even the evaluation score remains conditional on this fixed invented law, and one split cannot establish stability under changing base rates, accounting practices or macroeconomic dependence.") as vo:
            self.play(FadeIn(title), FadeIn(cards[0]))
            vo.wait_until('a'); self.play(FadeIn(cards[1]))
            vo.wait_until('b'); self.play(FadeIn(cards[2]))
            if len(cards) > 3: self.play(FadeIn(cards[3]))
        self.wait(0.5)
        self.clear_scene()

    def roc(self):
        m = self.example
        g = axes([0, 1], [0, 1], x_length=5.5, y_length=4.7,
                 xlabel=r"false positive rate", ylabel=r"true positive rate",
                 xticks=[0, .5, 1], yticks=[0, .5, 1], font_size=14).to_edge(LEFT, buff=.8).shift(DOWN*.2)
        lines = VGroup(*[curve(g.ax, *[np.asarray(x) for x in m['roc'][k]], color, stroke_width=3)
                         for k, color in [('altman', RISKY), ('logit', LOGIT), ('gbm', GBMC)]])
        a = m['results']['evaluation']['auc']
        title = label(r"ROC on 6,000 synthetic evaluation observations", font_size=29).to_edge(UP, buff=.35)
        side = VGroup(legend([(RISKY, rf"fixed Z: {a['altman']:.3f}"),
                              (LOGIT, rf"logit: {a['logit']:.3f}"), (GBMC, rf"trees: {a['gbm']:.3f}")],font_size=22),
                      wrapped_label(r"AUC measures ranking, not probability calibration. Tied scores move together.", 4.6, 23, GREY_A),
                      wrapped_label(r"Synthetic law; no real issuer validation.", 4.6, 23, QC.IDEA)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=.45).to_edge(RIGHT,buff=.5)
        with self.voiceover(f"Each ROC curve varies a classification threshold. The horizontal coordinate is the fraction of non-events flagged, and the vertical coordinate is the fraction of events caught. Tied scores move together, so the area agrees with the rank-based AUC including half credit for ties. <bookmark mark='a'/> On the synthetic evaluation sample, fixed Z has AUC {a['altman']:.3f}, logit {a['logit']:.3f}, and trees {a['gbm']:.3f}. These are the actual outputs of the declared example. An AUC is the probability that an event observation outranks a non-event observation, with the tie convention stated. <bookmark mark='b'/> It does not tell us whether a predicted ten percent risk occurs ten percent of the time. It also does not determine the cost of false alarms, screening capacity or realized investment returns. Those questions require a decision rule, event prevalence, loss assumptions and separate probability checks.") as vo:
            self.play(FadeIn(title), FadeIn(g), Create(DashedLine(g.ax.c2p(0,0),g.ax.c2p(1,1),color=GREY_C)))
            vo.wait_until('a'); self.play(LaggedStart(*[Create(x) for x in lines],lag_ratio=.3),FadeIn(side[0]))
            vo.wait_until('b'); self.play(FadeIn(side[1:]))
        self.wait(.5)
        self.clear_scene()

    def scores(self):
        r = self.example['results']
        b = r['evaluation']['brier']
        title, cards = lesson_cards('Report each sample and the relevant benchmark', [
            ('Fit sample', f"8,000 observations; {r['fit']['events']} events. AUC: logit {r['fit']['auc']['logit']:.3f}, trees {r['fit']['auc']['gbm']:.3f}"),
            ('Selection sample', f"4,000 observations; {r['selection']['events']} events. AUC: logit {r['selection']['auc']['logit']:.3f}, trees {r['selection']['auc']['gbm']:.3f}"),
            ('Evaluation sample', f"6,000 observations; {r['evaluation']['events']} events. AUC: logit {r['evaluation']['auc']['logit']:.3f}, trees {r['evaluation']['auc']['gbm']:.3f}"),
            ('Evaluation Brier score (lower is better)', f"Logit {b['logit']:.4f}; trees {b['gbm']:.4f}; constant fit-rate benchmark {b['fit_base']:.4f}"),
        ])
        with self.voiceover("Report all three samples with their event counts, rather than selecting the best-looking score. Fit scores reuse observations that determined the parameters. Selection scores reuse observations that determined the stopping point. <bookmark mark='a'/> Only the independent evaluation sample was generated after model selection. A difference between fit and evaluation performance can reflect adaptation to noise and ordinary sampling variation; it is not a direct measurement of how much each model memorized. We make no claim that a particular model must win. <bookmark mark='b'/> The Brier score is the mean squared probability error. Its benchmark predicts the fit-sample event rate for every evaluation observation, so it uses no evaluation labels. Compare the actual scores displayed here. A rare-event setting can make a constant low probability look numerically strong, but the available improvement depends on event prevalence and the signal. None of these synthetic scores is a claim about real bankruptcies.") as vo:
            self.play(FadeIn(title), FadeIn(cards[0]))
            vo.wait_until('a'); self.play(FadeIn(cards[1]))
            vo.wait_until('b'); self.play(FadeIn(cards[2]))
            if len(cards) > 3: self.play(FadeIn(cards[3]))
        self.wait(0.5)
        self.clear_scene()

    def calibration(self):
        c = self.example['calibration']; pr = np.asarray(c['pred'])*100; re = np.asarray(c['real'])*100
        top = max(5., float(np.ceil(max(pr.max(),re.max())/5)*5+5))
        g = axes([0,top],[0,top],x_length=5.,y_length=4.7,xlabel=r"predicted event rate, \%",
                 ylabel=r"observed event rate, \%",xticks=[0,top/2,top],yticks=[0,top/2,top],font_size=14
                 ).to_edge(LEFT,buff=.9).shift(DOWN*.2)
        dots = VGroup(*[Dot(g.ax.c2p(a,b),color=GBMC,radius=.08) for a,b in zip(pr,re)])
        title = label(r"Calibration: synthetic evaluation sample",font_size=30).to_edge(UP,buff=.35)
        side = VGroup(wrapped_label(r"Ten equal-count score groups: 600 observations each. The split can separate ties.",4.5,23,GREY_A),
                      wrapped_label(r"The diagonal is ideal group calibration; finite event counts fluctuate.",4.5,23,GREY_A),
                      wrapped_label(r"Grouping diagnoses averages, not calibration in every issuer subgroup.",4.5,23,QC.IDEA)
                      ).arrange(DOWN,aligned_edge=LEFT,buff=.5).to_edge(RIGHT,buff=.45)
        with self.voiceover("Now compare probabilities with event frequencies. We sort the independent synthetic evaluation observations into ten groups of six hundred by the trees' score. Equal-count grouping can split a block of tied predictions, which we disclose rather than hiding empty bins. <bookmark mark='a'/> Each point compares a group's average predicted probability with its observed event rate. The axes include every point without clipping. Exact diagonal agreement is not expected from finite Bernoulli counts, even under a perfectly specified model. <bookmark mark='b'/> Group calibration can conceal subgroup errors and does not prove calibration at each individual feature profile. In real credit populations, changes in prevalence, accounting coverage or conditional risk can degrade both ranking and calibration. Recalibration needs new development data and a fresh independent assessment; adjusting a model to improve the evaluation plot would consume that evaluation sample.") as vo:
            self.play(FadeIn(title),FadeIn(g))
            vo.wait_until('a'); self.play(Create(DashedLine(g.ax.c2p(0,0),g.ax.c2p(top,top),color=GREY_C)),FadeIn(dots))
            vo.wait_until('b'); self.play(FadeIn(side))
        self.wait(.5)
        self.clear_scene()

    def surface(self, m):
        p = m["slice"]
        q = np.asarray(p["q"])
        G = np.asarray(p["gbm"]) * 100  # rows: leverage quantile; columns: cushion quantile
        f = grid_fn(q, q, G)
        top = float(np.ceil(G.max()))
        ax = surf3d_axes([0.05, 0.95, 0.3], [0.05, 0.95, 0.3], [0, top, top / 2], x_length=6.0, y_length=4.8, z_length=3.0)
        ax.shift(RIGHT * 0.9 + DOWN * 0.3)
        surf = Surface(lambda u, w: ax.c2p(u, w, f(u, w)), u_range=(0.05, 0.95), v_range=(0.05, 0.95),
                       resolution=(18, 18), fill_opacity=0.85, stroke_width=0.4, stroke_color=GREY_D,
                       checkerboard_colors=False)
        surf.set_fill_by_value(axes=ax, colorscale=[(QC.GAIN, 0), (QC.IMPLIED, top / 3), (QC.LOSS, top)], axis=2)
        lev, cus = np.asarray(p["lev"]), np.asarray(p["cushion"])
        key = wrapped_label(rf"market cushion ME/TL, percentile (across: {cus[0]:.2f} to {cus[-1]:.0f}); leverage TL/TA, "
                    rf"percentile (back: {lev[0]:.2f} to {lev[-1]:.2f}); synthetic event probability, \% (up); other inputs "
                    r"at fit medians; log ME updated for consistency. Synthetic median slice, not a causal effect", 12.6, 22, GREY_A).to_edge(UP, buff=0.25)
        self.set_camera_orientation(phi=65 * DEGREES, theta=-55 * DEGREES, zoom=0.85)
        self.add_fixed_in_frame_mobjects(key)
        self.remove(key)
        with self.voiceover(
            "This surface displays predictions from the fixed synthetic tree model. Leverage and the market-equity cushion vary over fit-sample percentiles. Other inputs stay at fit medians, except log market equity, which is recomputed to preserve its identity with assets, leverage and the cushion. <bookmark mark='a'/> The steps come from tree partitions and the displayed interpolation, rather than established economic default thresholds. This is a median slice, not a partial-dependence average over companies. <bookmark mark='b'/> A logistic model without interaction terms would have linear log-odds, though its probability surface is nonlinear. Either model can be displayed at unusual feature combinations. The surface is descriptive and synthetic: changing leverage in this function does not identify the causal effect of a financing decision."
        ) as vo:
            self.play(Create(ax), FadeIn(key))
            self.play(Create(surf), run_time=2.5)
            vo.wait_until("a")
            self.move_camera(theta=-130 * DEGREES, run_time=5)
            vo.wait_until("b")
        self.wait(0.3)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, run_time=0.5)
        self.clear_scene()
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, gamma=0, zoom=1.0, frame_center=ORIGIN)


    def interpretation(self):
        title, cards = lesson_cards('A fitted surface is a conditional model display', [
            ('Median slice', 'Vary leverage and the equity cushion; hold other inputs at fit medians and update log ME consistently'),
            ('Not partial dependence', 'This display does not average over the observed covariate distribution'),
            ('Not a causal effect', 'Changing a ratio in a prediction function does not identify a balance-sheet intervention'),
            ('Question and answer', 'Report independent evaluation with uncertainty; disclose fit and selection scores and all development choices'),
        ])
        with self.voiceover("The rotating surface is a median slice of the synthetic trees' predictions. We vary leverage and the equity cushion while holding other inputs at fit-sample medians, and recompute log market equity so the accounting identity remains consistent. <bookmark mark='a'/> This is not partial dependence, which averages a prediction function over a covariate distribution. A slice can pass through unusual financial profiles, and the grid and interpolation are just a display of a fitted function. Its steps reflect the tree representation, not established economic thresholds. <bookmark mark='b'/> It is also not a causal response to changing leverage. Pause and predict: which score should appear in a model brochure? The answer is an honestly described independent evaluation with event counts, uncertainty and population limits, alongside transparent development results. Our example illustrates that procedure under an invented stationary law. It establishes no issuer ranking, market forecast or trading return.") as vo:
            self.play(FadeIn(title), FadeIn(cards[0]))
            vo.wait_until('a'); self.play(FadeIn(cards[1]))
            vo.wait_until('b'); self.play(FadeIn(cards[2]))
            if len(cards) > 3: self.play(FadeIn(cards[3]))
        self.wait(0.5)
        self.clear_scene()
