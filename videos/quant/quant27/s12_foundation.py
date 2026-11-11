from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant27.common import BAD, COIN, GOOD, HURDLE, LINEAR, MKT, NET, PART, TREE, ask, comma, fit_right, load

ETFS = ("SPY", "QQQ", "EEM", "GLD", "XLE")


class Foundation(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.tokens()
        self.kronos()
        self.pocket()
        self.result()
        self.lesson()
        self.question()

    def card(self):
        c = chapter_card(11, r"Foundation models", r"Can one model, trained on every market, forecast one it has never "
                         r"seen?", lit=(2024, 2025), part=PART)
        with self.voiceover('Chapter eleven. Foundation-model forecasting: distinguish corpus, target, transfer protocol and genuinely prospective evaluation.'):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def idea(self):
        head=label(r"Pretraining and transfer: corpus, target and timing",font_size=34).to_edge(UP,buff=.4)
        items=[(r"Chronos (2024)",r"Scales observations, discretises numerical tokens and models sequences probabilistically."),(r"TimesFM (2024)",r"Uses patches of numerical observations with a different corpus and forecasting head."),(r"Kronos (2025)",r"Tokenises multivariate financial candlesticks. Authors report more than 12 billion records across 45 exchanges; not run here.")]
        cards=VGroup(*[definition_card(title,wrapped_label(body,3.25,25),width=4.0,font_size=25) for title,body in items]).arrange(RIGHT,buff=.3,aligned_edge=UP)
        src=wrapped_label(r"Ansari et al. (2024); Das, Kong, Sen and Zhou (2024); Shi et al. (2025)",12.0,22,GREY_A).to_edge(DOWN,buff=.4)
        with self.voiceover("Several model families transfer forecasting behaviour across series. <bookmark mark='a'/> Chronos rescales observations, discretises them into tokens and models sequences probabilistically. <bookmark mark='b'/> TimesFM uses patches of numerical observations in a pretrained transformer. Its training corpus and forecasting head differ from Chronos. <bookmark mark='c'/> Kronos tokenises multivariate financial candlesticks. Its authors describe more than twelve billion records across forty-five exchanges. Zero-shot describes adaptation rules for a task; it does not itself establish disjoint training data, prospective timing or economic profitability.") as vo:
            self.play(FadeIn(head),FadeIn(cards[0]),FadeIn(src))
            vo.wait_until("a");self.wait(.1)
            vo.wait_until("b");self.play(FadeIn(cards[1]))
            vo.wait_until("c");self.play(FadeIn(cards[2]))
        self.clear_scene()

    def tokens(self):
        rows = [cmath(r"\tilde x_t", r"=", r"x_t \big/ \tfrac{1}{C}\textstyle\sum_{s \le C} |x_s|", font_size=34,
                      colors={r"\tilde x_t": LINEAR}),
                cmath(r"v_t", r"=", r"\operatorname{bin}(\tilde x_t) \in \{1, \dots, B\}", font_size=34,
                      colors={r"v_t": LINEAR}),
                cmath(r"\mathcal L", r"=", r"-\textstyle\sum_t \log p_\theta(v_{t} \mid v_{<t})", font_size=34,
                      colors={r"\mathcal L": NET}),
                cmath(r"\hat x_{T+h}", r"\sim", r"p_\theta(\,\cdot \mid v_{\le T}),\ \ \text{sampled, then unscaled}",
                      font_size=34, colors={r"\hat x_{T+h}": NET})]
        whys = [why(r"scale by the context's mean absolute value, so a penny stock and an index look alike to the model"),
                why(r"quantise into $B$ bins (Chronos: 4{,}096): a number becomes a token, a word in a vocabulary"),
                why(r"the language model's loss, next-token cross-entropy: it learns a distribution over what comes next, "
                    r"not a single number"),
                why(r"forecasts are sampled paths, so a quantile or a volatility comes from the samples; Kronos's "
                    r"tokenizer codes a whole candlestick into a coarse and a fine token instead of one value")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.5, buff=0.42, edge=6.9)
        with self.voiceover(
            "How does a number become a word? <bookmark mark='a'/> Divide by the context's average size, so that a "
            "penny stock and an index look alike. <bookmark mark='b'/> Cut the scaled range into bins: each value is now "
            "a token from a vocabulary of a few thousand. <bookmark mark='c'/> Train with the language model's own "
            "loss, the probability of the next token given all the earlier ones, which teaches a whole distribution of "
            "what comes next, not one number. <bookmark mark='d'/> Then forecast by sampling paths, as a language model "
            "writes sentences, and read off a median, a quantile, or a volatility. Kronos's tokenizer goes a step "
            "further and codes a whole candlestick into a coarse token and a fine one."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def kronos(self):
        claims = [(r"price forecasting, RankIC", r"+93\%\ \text{vs the best time-series foundation model}", NET),
                  (r"", r"+87\%\ \text{vs the best model trained from scratch}", NET),
                  (r"volatility forecasting, MAE", r"-9\%", TREE),
                  (r"synthetic candlesticks, fidelity", r"+22\%", COIN)]
        tab = VGroup()
        for j, (a, b, col) in enumerate(claims):
            y = 1.95 - 0.6 * j
            row = VGroup(label(a, font_size=20, color=GREY_A) if a else VMobject(), MathTex(b, font_size=28, color=col))
            row[1].move_to([2.2, y, 0])
            if a:
                row[0].move_to([-3.6, y, 0])
            tab.add(row)
        head = label(r"Kronos, zero-shot: the authors' reported gains", font_size=28).to_edge(UP, buff=0.5)
        caveat = VGroup(
            desk_question(r"what the House did not do", r"run Kronos itself: these are the authors' numbers on their own "
                          r"benchmarks, not replicated in this series", width=6.0, font_size=25),
            desk_question(r"what to ask", r"which markets and dates the pretraining corpus covered, against the test "
                          r"windows; and whether a better RankIC survives costs, Chapter 3's question", width=6.0,
                          font_size=25)).arrange(RIGHT,buff=.3,aligned_edge=UP).to_edge(DOWN,buff=.3)
        src = note(r"Shi, Fu, Chen, Zhao, Xu, Zhang and Li (2025), arXiv:2508.02739", font_size=15,
                   color=GREY_C).next_to(head, DOWN, buff=0.15)
        with self.voiceover(
            "The verified Kronos paper is arXiv twenty-five oh-eight, oh-two-seven-three-nine, first posted in August twenty twenty-five. <bookmark mark='a'/> Its abstract reports relative RankIC improvements of ninety-three percent versus a leading time-series foundation model and eighty-seven percent versus the best non-pretrained comparator, nine percent lower volatility-forecast MAE and twenty-two percent higher generative fidelity. These are relative benchmark metrics, not percentage-point accuracy or trading returns. <bookmark mark='b'/> We have not run Kronos. Corpus dates, entities, target definitions, comparator adaptation and trading assumptions require separate examination. Corpus size alone does not demonstrate leakage or transfer success."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(caveat, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def pocket(self):
        rng = np.random.default_rng(3)
        n = 60
        a = np.cumsum(rng.normal(0, 0.25, n + 1))
        a = a - a[:n].mean()
        g = axes([0, n + 1], [a.min() - 0.6, a.max() + 0.8], x_length=5.8, y_length=3.0, xlabel=r"day",
                 ylabel='$\\log(|r_t|+10^{-4})$, context-centred', xticks=[0,30,60], yticks=[round(float(a.min()),1),0,round(float(a.max()),1)], font_size=18).move_to(
            LEFT * 3.0 + UP * 0.9)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(i, a[i]), radius=0.04, color=COIN) for i in range(n)])
        target = Dot(ax.c2p(n, a[n]), radius=0.08, color=NET)
        win = SurroundingRectangle(dots, color=GREY_B, buff=0.08, stroke_width=1.5)
        net = VGroup(label(r"MLP 64--32, three seeds",font_size=26,color=NET),wrapped_label(r"Original training protocol; numerical transfer result unavailable",4.5,24,GREY_A)).arrange(DOWN,aligned_edge=LEFT,buff=.2).to_edge(RIGHT,buff=.4).shift(UP*.9)
        fit_right(net)
        rows = VGroup(
            label('Intended protocol: no ETF fine-tuning of the network', font_size=20, color=NET),
            label(r"EWMA ($\lambda = 0.94$): the RiskMetrics rule, with a fitted offset", font_size=20, color=HURDLE),
            label(r"HAR: 1-, 5- and 22-day averages, regressed on each ETF's first half", font_size=20, color=TREE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.5)
        test = note(r"intended retrospective ETF comparison, not completed: " + ", ".join(ETFS), font_size=16,
                    color=GREY_B).next_to(rows, UP, buff=0.25)
        stamp=note(r"Fixed simulated window; no market result",font_size=20,color=GREY_B).to_corner(UL,buff=.25)
        with self.voiceover(
            "The unchanged pocket-model protocol uses a more specific target. <bookmark mark='a'/> It predicts next-day log absolute return with a small positive offset, centred by the preceding sixty-day context mean. This is not realised integrated volatility or return direction. <bookmark mark='b'/> Eligible crypto histories run from the available archive through twenty twenty, without an explicit twenty eighteen lower cut. Validation randomly splits overlapping windows rather than holding out later dates. <bookmark mark='c'/> The network is not fine-tuned on the five ETFs, while their HAR coefficients and exponential-average offsets use each fund's first half. ETF evaluation can begin before the end of crypto pretraining, so this is retrospective cross-asset transfer rather than a prospective forecast from twenty fifteen."
        ) as vo:
            self.play(FadeIn(g),FadeIn(stamp))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.02, run_time=1.5), Create(win))
            self.play(FadeIn(target, scale=1.5))
            vo.wait_until("b")
            self.play(FadeIn(net))
            vo.wait_until("c")
            self.play(FadeIn(test), LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def result(self):
        head=label(r"Original transfer result unavailable",font_size=36,color=HURDLE).to_edge(UP,buff=.4)
        cards=VGroup(desk_question(r"Frozen SPY input failed verification",r"The unchanged original stopped at its first ETF reader. No accepted transfer-result cache was produced.",width=12,font_size=29),desk_question(r"Subsequent ETF comparisons were not reached",r"QQQ, EEM, GLD and XLE were not evaluated by this attempt. No numerical ranking or improvement is reported.",width=12,font_size=29),desk_question(r"The protocol remains discussable",r"Context-centred log moves, overlapping-window validation and retrospective chronology; no substitute historical strategy test.",width=12,font_size=29)).arrange(DOWN,buff=.3).next_to(head,DOWN,buff=.45)
        if cards.height>6.1:cards.scale_to_fit_height(6.1)
        with self.voiceover("The original transfer calculation is unavailable. Its normal attempt stopped when the frozen SPY input failed the unchanged source hash check. It produced no accepted result cache, and did not reach the other four ETF comparisons. We do not refresh the frozen source, retry the fit or report a numerical ranking. The preceding window is explicitly simulated to explain the source protocol; it is not a replacement transfer experiment. The target, random overlapping-window validation and retrospective chronology can still be audited from code, without claiming empirical transfer success."):
            self.play(FadeIn(head),FadeIn(cards))
        self.clear_scene()

    def lesson(self):
        cards = VGroup(
            desk_question(r"what transfers", 'Shared statistical structure can motivate transfer. Evidence depends on target, chronology, training corpus and comparator adaptation; no universal transfer guarantee.',
                          width=12.2, font_size=29),
            desk_question(r"what does not", 'Return forecasts differ from centred log-move forecasts. Statistical improvement does not establish implementable net returns.', width=12.2, font_size=29),
            desk_question(r"how to read a zero-shot claim", 'Audit corpus dates, entities and model selection. A large corpus creates possible contamination routes but its size alone proves no overlap.', width=12.2, font_size=29),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What can transfer? <bookmark mark='a'/> Shared statistical structures such as clustering may motivate cross-asset learning, but useful transfer needs evidence for the stated target and chronology. It cannot be learned anywhere and safely used everywhere. <bookmark mark='b'/> Return direction and centred log-move prediction are different tasks. A statistical gain need not pay after trading costs. <bookmark mark='c'/> Inspect corpus dates and entities, pretrained checkpoints and adaptation choices. A large corpus creates potential contamination routes, but size alone proves no overlap. Predefine a genuinely later or appropriately entity-disjoint evaluation before consulting its outcomes."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q=ask(r"A model pretrained through 2024 is evaluated on 2023. Identify possible temporal and entity-overlap routes, state what corpus evidence is needed, and design a genuinely prospective evaluation.")
        with self.voiceover("Pause and predict. A model pretrained through twenty twenty-four is evaluated on twenty twenty-three. Identify possible temporal and entity-overlap routes without assuming they occurred. State the corpus evidence needed and design a genuinely prospective evaluation."):
            self.play(FadeIn(q))
        self.clear_scene()
