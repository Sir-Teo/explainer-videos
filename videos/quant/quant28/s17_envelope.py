from __future__ import annotations

from explainer.quant import *  # noqa: F403
from explainer.quant.house import pit
from videos.quant.quant28.common import PART, WORD, HURDLE, comma


class Envelope(VoiceoverScene):
    def construct(self):
        self.card()
        self.clocks()
        self.target()
        self.example()
        self.ledger()
        self.limits()
        self.question()

    def card(self):
        c = chapter_card(16, r"Text-signal evaluation protocol",
                         r"What would turn a statement score into reviewable trading evidence?", part=PART)
        with self.voiceover(
            "Chapter sixteen. Explaining the statement day's move and forecasting a later return are different tasks. We now specify what a text signal would have to survive before anyone could interpret it as trading evidence. The original strategy experiment is excluded from this review: no cached payoff, registration, opening or score is read."
        ):
            self.play(FadeIn(c[0]), FadeIn(c[1]))
        self.clear_scene()

    def clocks(self):
        cards = VGroup(
            desk_question(r"document clock", r"meeting date, first public release, revisions and the archived text actually available", width=12, font_size=22),
            desk_question(r"model clock", r"training and tokenizer inputs, model version, selection history and inference timestamp", width=12, font_size=22),
            desk_question(r"execution clock", r"when the signal is calculated, when an order can arrive and which executable price follows", width=12, font_size=22),
        ).arrange(DOWN, buff=0.28)
        with self.voiceover(
            "Start with three clocks. <bookmark mark='a'/> A document's meeting date is not necessarily its first release date; later archives can revise text. <bookmark mark='b'/> A model has its own clock: training corpus, tokenizer, version and tuning history. <bookmark mark='c'/> An order has another: collection, inference, transmission and execution delay. Keeping only a date integer does not establish any of these three boundaries."
        ) as vo:
            self.play(FadeIn(cards[0]))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(FadeIn(cards[1]))
            vo.wait_until("c")
            self.play(FadeIn(cards[2]))
        self.clear_scene()

    def target(self):
        rows = VGroup(
            MathTex(r"\Delta y_{\rm day}=y_{\rm close}-y_{\rm prior\ close}", font_size=34),
            MathTex(r"\Delta y_{\rm future}=y_{t+h}-y_{\rm executable\ entry}", font_size=34, color=HURDLE),
            wrapped_label(r"Different targets require separate fitting, selection and later evaluation. A score trained to explain a reaction is not automatically a forecast of the remaining drift.", 11.4, 23),
        ).arrange(DOWN, buff=0.55)
        with self.voiceover(
            "Write the target before fitting. <bookmark mark='a'/> The daily reaction runs from the prior close to the release day's close. By that closing trade, most of this label is already observed. <bookmark mark='b'/> A future target begins at an executable entry after the signal is available. A contemporaneous correlation supplies no automatic direction, size or significance for that later target. Evaluation must also account for coupons, carry, curve changes and the instruments actually traded."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(FadeIn(rows[1:]))
        self.clear_scene()

    def example(self):
        rows = VGroup(
            label(r"Fixed duration arithmetic; not a historical strategy", font_size=29, color=WORD),
            MathTex(r"D_{\rm mod}=1.9,\quad \Delta y=10\ {\rm bp}=0.001", font_size=32),
            MathTex(r"\Delta P/P\approx-D_{\rm mod}\Delta y=-19\ {\rm bp}", font_size=34),
            MathTex(r"\text{short-position example: }19-1.9=17.1\ {\rm bp}", font_size=30, color=HURDLE),
            wrapped_label(r"Cost assumption: one basis point of yield per round trip, converted using the same fixed duration. Ignores convexity, coupons, carry, curve risk and financing.", 11.4, 20),
        ).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "A fixed arithmetic example, with no market sample. <bookmark mark='a'/> Modified duration is one point nine, and yields rise ten basis points. The first-order long-bond price change is minus nineteen basis points of price. <bookmark mark='b'/> An ideal short earns nineteen before costs. If a round trip costs one basis point of yield, the duration approximation converts that to one point nine basis points of price, leaving seventeen point one. This is local duration arithmetic, not a total-return backtest, a measured cost or a strategy result."
        ) as vo:
            self.play(FadeIn(rows[:2]))
            vo.wait_until("a")
            self.play(FadeIn(rows[2]))
            vo.wait_until("b")
            self.play(FadeIn(rows[3:]))
        self.clear_scene()

    def ledger(self):
        count = pit.trials_upto(PART)
        card = firm_card(r"Existing ledger metadata", r"Thirteen additional recorded configurations relative to Part 27: twelve threshold pairs and one strategy specification. This review adds none.",
                         numbers=((comma(count), r"existing cumulative registrations through Part 28"),),
                         source=r"read-only cumulative metadata; not a score or independent-trial estimate", kind=r"Protocol", width=10.8, font_size=23)
        with self.voiceover(
            f"The ledger already records {count:,} configurations through Part twenty-eight, thirteen more than through Part twenty-seven. That is existing metadata, not a registration by this review. A recorded count is a lower bound on research choices, and correlated thresholds are not independent trials. None of these counts tells us the excluded strategy's payoff or its statistical significance."
        ):
            self.play(FadeIn(card))
        self.clear_scene()

    def limits(self):
        cards = VGroup(
            desk_question(r"before evaluation", r"freeze the target, clocks, features, preprocessing, model, thresholds, costs and comparison rules", width=12, font_size=21),
            desk_question(r"during evaluation", r"use temporal separation; purge labels that have not matured; preserve every attempted specification", width=12, font_size=21),
            desk_question(r"after evaluation", r"report gross and net uncertainty with dependence and selection assumptions; a PSR is not automatically a posterior probability", width=12, font_size=21),
        ).arrange(DOWN, buff=0.28)
        with self.voiceover(
            "A defensible protocol freezes the specification before later evaluation. <bookmark mark='a'/> Preprocessing and tuning belong inside the training boundary, with release and label-maturity clocks checked. <bookmark mark='b'/> Report all tried specifications and use uncertainty that reflects dependent events, non-normal returns and selection. An IID normal Sharpe precision approximation is not a power calculation, and a probabilistic Sharpe statistic is not automatically a Bayesian probability that an edge is real. The excluded experiment supplies no evidence here."
        ) as vo:
            self.play(FadeIn(cards[0]))
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.clear_scene()

    def question(self):
        q = pause_card(r"A score explains the prior-close-to-release-close move. What must change before you test a trade entered after that close?")
        with self.voiceover(
            "Pause and predict. A score explains the move from the prior close to the release day's close. What target, data clock and execution assumptions must change before you test a trade entered after that close?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
