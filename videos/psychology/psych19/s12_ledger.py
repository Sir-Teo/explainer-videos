from __future__ import annotations

from videos.psychology.psych19.common import *  # noqa: F403


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        self.partial()
        self.forgetting()
        self.word_length()
        self.scanning()
        self.four()
        self.training()

    def card(self):
        card = chapter_card(11, r"The Ledger", r"What happened when today's findings were checked?", lit=(),
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter eleven. The Ledger."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    @staticmethod
    def _row(key):
        return {f.key: f for f in ledger.rows(part=PART)}[key]

    def _show(self, card, vo, marks="abcd"):
        self.play(FadeIn(card.box), FadeIn(card.tag), FadeIn(card.claim))
        vo.wait_until(marks[0])
        self.play(FadeIn(card.original, shift=RIGHT * 0.15))
        vo.wait_until(marks[1])
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.record], lag_ratio=0.6), run_time=1.5)
        vo.wait_until(marks[2])
        self.play(FadeIn(card.note))
        vo.wait_until(marks[3])
        self.play(FadeIn(card.status, scale=1.3))

    def partial(self):
        card = ledger_card(self._row("partial_report"), width=12.8, font_size=25)
        with self.voiceover(
            "Six rows today. The first: right after a brief display, a cued part of it can be reported far better "
            "than whole report suggests, and the advantage fades within about a second. <bookmark mark='a'/> The "
            "original: Sperling, 1960. <bookmark mark='b'/> The record: Max Coltheart's 1980 review gathered two "
            "decades of partial-report studies. The advantage is large for cues that pick a location, and absent for "
            "cues that pick a category, such as report the digits. <bookmark mark='c'/> What the store holds, and how "
            "much of it reaches awareness, is argued. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def forgetting(self):
        card = ledger_card(self._row("brown_peterson"), width=12.8, font_size=25)
        with self.voiceover(
            "The second: without rehearsal, three consonants are mostly forgotten within eighteen seconds, because "
            "their trace decays. <bookmark mark='a'/> The original: Peterson and Peterson, 1959. "
            "<bookmark mark='b'/> The record: Keppel and Underwood, 1962, who looked at the first trial. "
            "<bookmark mark='c'/> The forgetting is real and reproduces; the cause in the textbook account does not "
            "survive the first trial. <bookmark mark='d'/> A story and a record: the finding stands, the "
            "explanation attached to it was wrong."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def word_length(self):
        card = ledger_card(self._row("word_length"), width=12.8, font_size=25)
        with self.voiceover(
            "The third: span is shorter for words that take longer to say, and suppression removes the difference. "
            "<bookmark mark='a'/> The original: Baddeley, Thomson and Buchanan, 1975. <bookmark mark='b'/> The "
            "record: the effect of word length reproduces easily, but Peter Lovatt and his colleagues found, with "
            "two-syllable words that differ only in spoken duration, no reliable effect for some word sets. "
            "<bookmark mark='c'/> So whether duration itself is the cause, or something that travels with it in the "
            "classic word lists, is argued. <bookmark mark='d'/> Replicated, with the cause under review."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def scanning(self):
        card = ledger_card(self._row("sternberg"), width=12.8, font_size=25)
        with self.voiceover(
            "The fourth: deciding whether a probe is in a short list takes time that rises linearly with the list, "
            "equally for yes and no. <bookmark mark='a'/> The original: Sternberg, 1966. <bookmark mark='b'/> The "
            "record: Sternberg's own review in 1975 found linear functions for digits, letters, words and faces, "
            "with slopes that depend on the material. <bookmark mark='c'/> The line reproduces; its reading as a "
            "serial search does not follow from it, as Townsend showed. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def four(self):
        card = ledger_card(self._row("capacity_four"), width=12.8, font_size=24)
        with self.voiceover(
            "The fifth: without rehearsal or chunking, people hold about three or four items. "
            "<bookmark mark='a'/> The original: Luck and Vogel, 1997. <bookmark mark='b'/> The record: Cowan's "
            "review found three to five across many tasks, and van den Berg, Awh and Ma's comparison of thirty-two "
            "models across ten datasets found precision falling continuously with load. <bookmark mark='c'/> The "
            "number reproduces wherever rehearsal is blocked; what it counts is the open question. "
            "<bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def training(self):
        card = ledger_card(self._row("wm_training"), width=12.8, font_size=24)
        with self.voiceover(
            "And the sixth: training working memory raises fluid intelligence. <bookmark mark='a'/> The original: "
            "Jaeggi and colleagues, 2008. <bookmark mark='b'/> The record: Redick and colleagues' placebo-controlled "
            "trial in 2013, and Melby-Lervåg, Redick and Hulme's meta-analysis of a hundred and forty-five "
            "comparisons in 2016. <bookmark mark='c'/> Practice improves what is practised. The far transfer that "
            "would matter is not found against placebo training. <bookmark mark='d'/> Failed."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()
