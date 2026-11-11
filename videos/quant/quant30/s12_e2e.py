from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant30.common import BAD, EST_C, EW_C, GOOD, HURDLE, PART, REAL_C, SHRINK_C, TRUE_C, fit_right, load


class EndToEnd(VoiceoverScene):
    def construct(self):
        e = load("e2e")
        self.card()
        self.idea()
        self.paper()
        self.replay(e)
        self.table(e)
        self.reading(e)
        self.spo()
        self.question()

    def card(self):
        c = chapter_card(11, r"End-to-end portfolios", r"Why predict returns and then optimise, when a network could learn "
                         r"the weights directly?", part=PART)
        with self.voiceover("Chapter eleven. The classical pipeline has two steps: forecast, then optimise. A neural "
                            "network can skip the forecast and learn the weights directly, trained on the quantity the "
                            "investor cares about. Does it help?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def idea(self):
        rows = [cmath(r"w_t", r"=", r"\operatorname{softmax}\big(g_\theta(x_{t,1}), \dots, g_\theta(x_{t,N})\big)", font_size=32,
                      colors={r"w_t": SHRINK_C}),
                cmath(r"\mathcal L(\theta)", r"=", r"-\frac{\overline{w_t^\top r_{t+1}}}{\operatorname{sd}(w_t^\top r_{t+1})}\sqrt{12}",
                      font_size=32, colors={r"\mathcal L(\theta)": BAD}),
                cmath(r"x_{t,i}", r"=", r"(\bar r^{12}_{i},\ \sigma^{12}_i,\ r^{1}_{i},\ \bar r^{60}_{i})", font_size=30)]
        whys = [why(r"a small network scores each industry from its own features; the softmax makes the weights positive "
                    r"and sum to one"),
                why(r"trained to maximise the realised Sharpe ratio of the portfolio directly: the decision loss "
                    r"(as in Zhang, Zohren and Roberts 2020)"),
                why(r"four features per industry: the last year's mean, its volatility, the last month, the last five years' "
                    r"mean; 1975--2005 training, 2006--2020 diagnostic validation; scaling uses both periods")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The saved demonstration has an important information leak. <bookmark mark='a'/> A shared small network scores four trailing-return features per industry; softmax gives positive unit-sum weights. <bookmark mark='b'/> Training optimises realised Sharpe, with weight decay, on 1975 through 2005. <bookmark mark='c'/> Nominal validation is 2006 through 2020, but feature centring and scaling use both periods before the split. These are retrospective diagnostic results, not a clean chronological evaluation. The original computation is retained and the leak is disclosed rather than silently retrained."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def paper(self):
        card = firm_card(r"Zhang, Zohren and Roberts (2020)", r"`Deep learning for portfolio optimization', \textit{Journal "
                         r"of Financial Data Science}: a network maps the recent prices of a few exchange-traded index funds "
                         r"directly to weights, trained on the Sharpe ratio",
                         numbers=((r"\text{ETFs}", r"of market indices, not single stocks: a small universe, few weights to learn"),
                                  (r"\checkmark", r"the authors report a higher Sharpe ratio than the classical allocations "
                                                   r"they compare with, over 2011 to April 2020")),
                         source=r"JFDS 2 (2020); arXiv 2005.13665", kind=r"Paper file", width=10.6, font_size=22
                         ).move_to(ORIGIN)
        with self.voiceover(
            "The idea comes from published work. <bookmark mark='a'/> Zihao Zhang, Stefan Zohren and Stephen Roberts "
            "trained a network to map the recent prices of a few index funds directly to portfolio weights, with the "
            "Sharpe ratio as the loss. <bookmark mark='b'/> They report beating the classical allocations they compared "
            "with, from 2011 to 2020. Note the universe: a handful of funds, so very few weights to learn. Ours has "
            "forty-nine."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(Indicate(card.submobjects[-1], color=QC.FIRM, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    def replay(self, e):
        h = e["hist"]
        ep = np.array([x["ep"] for x in h], float)
        tr = np.array([x["train"] for x in h], float)
        va = np.array([x["valid"] for x in h], float)
        hi = float(np.ceil(max(tr.max(), va.max()) * 2) / 2)
        lo = float(np.floor(min(0, va.min()) * 2) / 2)
        g = axes([0, ep[-1]], [lo, hi], x_length=7.4, y_length=4.4, xlabel=r"training epoch", ylabel=r"Sharpe ratio, a year",
                 xticks=[0, ep[-1] / 2, ep[-1]], yticks=[lo, 0, hi], xfmt=lambda v: f"{v:.0f}", font_size=15
                 ).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        lt, lv = curve(ax, ep, tr, TRUE_C, stroke_width=3), curve(ax, ep, va, REAL_C, stroke_width=3)
        ew = DashedLine(ax.c2p(0, e["valid"]["ew"]), ax.c2p(ep[-1], e["valid"]["ew"]), color=EW_C, stroke_width=2)
        leg = legend([(TRUE_C, r"1975--2005, trained on"), (REAL_C, r"2006--2020, validation"),
                      (EW_C, r"1/N on 2006--2020")], font_size=15).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        with self.voiceover(
            f"""Saved score history for one seed. <bookmark mark='a'/> The last logged pre-update training Sharpe is {tr[-1]:.2f}. <bookmark mark='b'/> The corresponding validation score is evaluated after that update and is {va[-1]:.2f}; the equal-weight diagnostic is {e['valid']['ew']:.2f}. Global feature scaling leaks validation moments, and validation is repeatedly inspected. Score curves are saved, but intermediate portfolio-weight snapshots are not, so this is not a replay of changing allocations or a certified independent test."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), Create(ew))
            vo.wait_until("a")
            self.play(Create(lt), run_time=2)
            vo.wait_until("b")
            self.play(Create(lv), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def table(self, e):
        rows = [(r"end-to-end network", "e2e", SHRINK_C), (r"two-step: shrunk inverse direction, clipped positive", "two",
                                                           QC.OPTION), (r"1/N", "ew", EW_C)]
        hx = [-3.0, 2.4, 4.6]
        head = VGroup(label(r"rule", font_size=18, color=GREY_B), label(r"1975--2005", font_size=18, color=TRUE_C),
                      label(r"2006--2020", font_size=18, color=REAL_C))
        tab = VGroup(head)
        for t, k, col in rows:
            tab.add(VGroup(label(t, font_size=18, color=col), MathTex(f"{e['train'][k]:.2f}", font_size=26),
                           MathTex(f"{e['valid'][k]:.2f}", font_size=26)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.8 - 0.8 * j, 0])
            row[0].align_to(np.array([-6.0, 0, 0]), LEFT)
        foot = wrapped_label(r"annualised gross excess-return Sharpe; final weights; leaked scaling, selected diagnostic periods", 11.0, 16, GREY_A
                             ).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            f"""The final saved comparison uses a different score convention from the pre-update training log. <bookmark mark='a'/> All final table scores evaluate final weights. The two-step heuristic solves an inverse shrunk-covariance mean direction, clips negative components and renormalises; that is not the exact long-only mean-variance optimizer. Its training and diagnostic validation Sharpes are {e['train']['two']:.2f} and {e['valid']['two']:.2f}. Different objectives, features and the network's leaked scaling prevent attributing the gap purely to end-to-end versus two-step learning."""
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def reading(self, e):
        n_train = (2005 - 1975 + 1) * 12
        cards = VGroup(
            desk_question(r"it concentrated", rf"in validation its largest weight averaged {100 * e['max_w_valid']:.0f}\%, "
                          rf"and its effective number of holdings {e['eff_n_valid']:.1f}: a Sharpe-ratio loss on "
                          r"monthly data rewards betting on whatever won in sample", width=12.4, font_size=19),
            desk_question(r"limited training and leaked preprocessing", r"the two-step rule's covariance was shrunk "
                          rf"(Chapter 4); the network uses weight decay, global scaling, and {n_train} months to learn from", width=12.4,
                          font_size=19),
            desk_question(r"what a fair comparison needs", r"matched information, frozen preprocessing, constraints, "
                          r"costs, repeated seeds and appropriate validation; no automatic performance advantage",
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            f"""What the saved demonstration establishes. <bookmark mark='a'/> The largest diagnostic-period weight averages {100 * e['max_w_valid']:.0f} percent and effective holdings {e['eff_n_valid']:.0f}, showing concentration in this fit. <bookmark mark='b'/> There are {n_train} training months, a single seed, weight decay and repeated validation inspection; the feature-scaling leak remains. These facts do not isolate the cause of poor generalisation. <bookmark mark='c'/> Decision-focused methods can incorporate costs and constraints, but their value needs matched information, appropriate regularisation, frozen preprocessing and valid evaluation. No new fit is run to improve this result."""
        ) as vo:
            self.add(cards[0])
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def spo(self):
        rows = [cmath(r"\hat c", r"=", r"\arg\min_c \textstyle\sum_t \|c - r_{t+1}\|^2\ \text{(predict)},\quad "
                      r"w(\hat c) = \arg\max_{w \in W} \hat c^\top w\ \text{(optimise)}", font_size=26, colors={r"\hat c": EST_C}),
                cmath(r"\ell_{\text{SPO}}", r"=", r"r^\top w(r) - r^\top w(\hat c)", font_size=32, colors={r"\ell_{\text{SPO}}": BAD}),
                cmath(r"\ell_{\text{SPO+}}", r"\ge", r"\ell_{\text{SPO}},\ \text{convex in } \hat c", font_size=32,
                      colors={r"\ell_{\text{SPO+}}": SHRINK_C})]
        whys = [why(r"the two-step pipeline: fit the forecast for accuracy, then optimise as if it were true"),
                why(r"the regret of the decision: what was lost by acting on the forecast instead of the truth"),
                why(r"Elmachtoub and Grigas (2022), `Smart predict, then optimize': a convex surrogate of the regret, which "
                    r"trains a forecast for the decision it feeds")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "There is a principled middle ground. <bookmark mark='a'/> The classical pipeline fits the forecast for "
            "accuracy, then optimises as if the forecast were true. <bookmark mark='b'/> What matters is the regret of the "
            "decision: what was lost by acting on the forecast. <bookmark mark='c'/> Adam Elmachtoub and Paul Grigas gave a "
            "convex upper bound on that regret, so a forecast can be trained for the decision it feeds while keeping the "
            "optimizer's structure, and its constraints, in place. That is where decision-focused learning is heading."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def question(self):
        q = pause_card(r"how would you add shrinkage to the end-to-end network without changing its loss?")
        with self.voiceover(
            "Pause and predict. How would you build shrinkage into the network, without changing its loss?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
