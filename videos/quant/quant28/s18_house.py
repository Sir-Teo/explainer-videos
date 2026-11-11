from __future__ import annotations

from explainer.quant import *  # noqa: F403
from explainer.quant.house import text as TX, pit
from videos.quant.quant28.common import BAD, GOOD, HURDLE, MODEL_A, MODEL_B, MODEL_C, PART, WORD, comma, house_lab, load


class House(VoiceoverScene):
    def construct(self):
        self.card()
        self.sheet(load("corpus"), load("tone"), load("sestm"), load("embed"), load("lookahead"))
        self.lab()
        self.module()
        self.test()

    def card(self):
        c = chapter_card(17, r"Rule 28: text features", r"What must a feature made of words survive before the House "
                         r"trades it?", part=PART)
        with self.voiceover("Chapter seventeen. The House's twenty-eighth rule: what a feature made of words must survive."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sheet(self, c, t, s, e, la):
        A, B, C = la["A"], la["B"], la["C"]
        rows = [(r"the corpus: statements and minutes to 2020", rf"{c['n_statements']} + {c['n_minutes']},\ "
                 rf"{c['n_tokens'] / 1e6:.1f}\text{{m words}}", WORD),
                (r"Zipf's slope", rf"{c['zipf_slope']:.2f}", WORD),
                (r"dictionary tone and the two-year move: $t$", rf"{t['regs']['net']['t']:.2f}", BAD),
                (r"SESTM, rank correlation: trained on, then unseen", rf"{s['rho_train']:.2f}\ \to\ {s['rho']:.2f}", HURDLE),
                (r"embeddings: tightening $-$ raise $+$ lower", rf"\text{{{e['analogies'][0]['best'][0]}}}" if e["analogies"]
                 else r"-", GOOD),
                (r"bits per character on 2008--12 minutes: A, C, B", rf"{A['bpc_test']:.2f},\ {C['bpc_test']:.2f},\ "
                 rf"{B['bpc_test']:.2f}", MODEL_C),
                (r"sealed strategy result", r"\text{excluded; not read or scored}", BAD),
                (r"existing cumulative registrations through Part 28", comma(pit.trials_upto(PART)), QC.HOUSE)]
        hx = [-2.4, 4.3]
        tab = VGroup()
        for j, (txt, v, col) in enumerate(rows):
            y = 2.4 - 0.6 * j
            tab.add(VGroup(label(txt, font_size=18, color=col).move_to([hx[0], y, 0]),
                           MathTex(v, font_size=24).move_to([hx[1], y, 0])))
        title = label(r"The text desk's first sheet", font_size=28).to_edge(UP, buff=0.3)
        foot = wrapped_label(r"ordinary original research outputs and existing ledger metadata; descriptive comparisons, not an attainable-return promise", 12.0, 16, GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The first sheet. <bookmark mark='a'/> Thirty years of the committee's words, obeying Zipf's law. The "
            "dictionary showed little evidence of a linear association with this daily yield change. SESTM found words that fitted the "
            "past and did not travel. Embeddings learned that easing is to lower what tightening is to raise. The "
            "earlier-corpus language model was more surprised by the crisis, and the ones that had read the future much less. "
            "The strategy experiment remains excluded: no cached payoff, opening or score is read here. The count of 10,470 through Part twenty-eight is existing ledger metadata, with thirteen already-recorded configurations relative to Part twenty-seven; no new registration is made."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in tab], lag_ratio=0.4), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def lab(self):
        card = house_lab(r"Point in time, for words", TX.point_in_time_vocab, "return vocabulary", 1,
                         extra=((TX.first_use, "out = {}", 7),), width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "Part one's first rule, applied to words, is two small functions in the House. A model dated t may only "
            "know the vocabulary of documents dated before t; and for every word we keep the date it first appeared, "
            "in the supplied corpus. Pandemic existed before 2020, and first occurrence in a sample is not first existence or proof of public availability. These helpers filter date integers only: meeting date, release timestamp and archive vintage can differ. The original validation vocabulary and model C also use later text; do not call every pipeline point in time."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def module(self):
        chart = house_chart(PART, lit=("research",)).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{tokenize}, \texttt{vocabulary}, \texttt{dtm}, \texttt{tfidf}, \texttt{zipf}", r"counting"),
            (r"\texttt{tone}, \texttt{lm\_sets}", r"dictionaries"),
            (r"\texttt{sestm\_screen}, \texttt{sestm\_topics}, \texttt{sestm\_score}", r"supervised words"),
            (r"\texttt{cooccurrence}, \texttt{ppmi\_svd}, \texttt{neighbours}, \texttt{nmf\_topics}", r"meaning"),
            (r"\texttt{fog}, \texttt{word\_diff}", r"form"),
            (r"\texttt{point\_in\_time\_vocab}, \texttt{first\_use}", r"time"),
        ]
        tab = VGroup(*[VGroup(label(a_, font_size=15, color=QC.HOUSE), label(b_, font_size=15, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a_, b_ in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 8.6)
        tab.next_to(chart, DOWN, buff=0.25)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 28: a text feature enters the House only if every document carries the time it became "
                             r"public, every model and tokenizer that reads it was trained on text from before that time, "
                             r"and the feature's model version is recorded; if it beats the dictionary and a simple "
                             r"bag-of-words baseline out of sample; and if its signal survives the delay between the words' "
                             r"release and the trade.", 12.4, 18, QC.HOUSE).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "The tools this part adds. <bookmark mark='a'/> Counting; dictionaries; supervised words; meaning; form; "
            "and time. <bookmark mark='b'/> And the twenty-eighth rule. A text feature enters the House only if every "
            "document carries the moment it became public; every model and tokenizer that reads it was trained only "
            "on text from before that moment, with its version recorded; it beats the dictionary and a simple bag of "
            "words out of sample; and its signal survives the delay between the release of the words and the trade."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["research"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=5))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()

    def test(self):
        cards = VGroup(
            desk_question(r"the LLM signal with a Sharpe ratio of 4 on 2015--2020 news", r"first check the model's "
                          r"training cut-off; then anonymise and re-run; then use a model dated before 2015",
                          width=12.0, font_size=19),
            desk_question(r"the dictionary score that explains the day's move", r"it is explaining, not predicting: "
                          r"measure from the moment after release, not from the close before", width=12.0, font_size=19),
            desk_question(r"the new data set that everyone is buying", r"Chapter 14: ask how many funds have it, and when "
                          r"they started", width=12.0, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The rule against three cases. <bookmark mark='a'/> A language-model signal with a Sharpe ratio of four on "
            "news from 2015 to 2020: check the model's training cut-off, anonymise and re-run, then use a model dated "
            "before 2015. <bookmark mark='b'/> A dictionary score that explains the day's move: it explains, it does not "
            "predict; measure from the moment after release. <bookmark mark='c'/> A new data set everyone is buying: "
            "ask how many funds have it, and since when."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k > 0:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
