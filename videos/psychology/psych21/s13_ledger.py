from __future__ import annotations

from videos.psychology.psych21.common import *  # noqa: F403


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        self.row_forgetting_curve()
        self.row_spacing_effect()
        self.row_testing_effect()
        self.row_drm_false_memory()
        self.row_misinformation_effect()
        self.row_implanted_memories()
        self.row_reconsolidation_humans()
        self.row_verbal_overshadowing()

    def card(self):
        card = chapter_card(12, r"The Ledger", r"What happened when today's findings were checked?", lit=(),
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter twelve. The Ledger."):
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

    def row_forgetting_curve(self):
        card = ledger_card(self._row("forgetting_curve"), width=12.8, font_size=24)
        with self.voiceover(
            'Eight rows today. The first: memory, measured by savings, falls fast at first and then ever more slowly.'
            " <bookmark mark='a'/> The original: Ebbinghaus, 1885, one subject. <bookmark mark='b'/> The record: "
            "Heller, Mack and Seitz's two subjects, Wixted and Ebbesen's power functions across measures, and Dros's "
            "seventy hours in 2015. <bookmark mark='c'/> The shape replicates every time. Which law fits a single "
            'memory is a separate question, because averaging can make a power law out of exponentials. <bookmark '
            "mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_spacing_effect(self):
        card = ledger_card(self._row("spacing_effect"), width=12.8, font_size=24)
        with self.voiceover(
            'The second: study spread over time beats the same study massed together, and the best gap grows with how'
            " long you need to remember. <bookmark mark='a'/> The original: Ebbinghaus again. <bookmark mark='b'/> "
            "The record: Cepeda and colleagues' review of the experiments of a century, and their study of more than "
            "thirteen hundred people over a year. <bookmark mark='c'/> One of the most general effects in "
            "experimental psychology, and one of the least used. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_testing_effect(self):
        card = ledger_card(self._row("testing_effect"), width=12.8, font_size=24)
        with self.voiceover(
            'The third: retrieving material improves long-term memory more than studying it again. <bookmark '
            "mark='a'/> The original, for the modern literature: Roediger and Karpicke, 2006. <bookmark mark='b'/> "
            "The record: Christopher Rowland's meta-analysis, about half a standard deviation, and Olusola Adesope "
            "and colleagues' meta-analysis, which found it in classrooms too. <bookmark mark='c'/> Robust, and "
            'largest after a delay. How far it reaches to complex material that has to be understood is argued. '
            "<bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_drm_false_memory(self):
        card = ledger_card(self._row("drm_false_memory"), width=12.8, font_size=24)
        with self.voiceover(
            'The fourth: after a list of associates, people recall and recognise the missing word, and say they '
            "remember it. <bookmark mark='a'/> The original: Roediger and McDermott, 1995. <bookmark mark='b'/> The "
            "record: David Gallo's review of fifteen years of the illusion, and Patihis's people with superior "
            "memory. <bookmark mark='c'/> One of the most reproducible results there is; how far it speaks to "
            "memories of real events is argued. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_misinformation_effect(self):
        card = ledger_card(self._row("misinformation_effect"), width=12.8, font_size=24)
        with self.voiceover(
            "The fifth: misleading information after an event gets into people's reports of the event. <bookmark "
            "mark='a'/> The original: Loftus and Palmer's broken glass, 1974. <bookmark mark='b'/> The record: Loftus, "
            "Miller and Burns's stop sign, and thirty years of studies reviewed by Loftus in 2005. <bookmark mark='c'/> The "
            "effect on reports is robust; what happens to the original detail is still argued. <bookmark mark='d'/> "
            'Replicated.'
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_implanted_memories(self):
        card = ledger_card(self._row("implanted_memories"), width=12.8, font_size=24)
        with self.voiceover(
            'The sixth: suggesting a false childhood event leads a substantial minority to remember it. <bookmark '
            "mark='a'/> The original: Loftus and Pickrell, 1995, twenty-four people. <bookmark mark='b'/> The record:"
            " Scoboria's pooled analysis of eight studies, and Murphy's preregistered replication. <bookmark "
            "mark='c'/> The rate depends on how a report is coded. It shows false memories can be made, not that any "
            "given memory is false. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_reconsolidation_humans(self):
        card = ledger_card(self._row("reconsolidation_humans"), width=12.8, font_size=24)
        with self.voiceover(
            "The seventh: reactivating a human memory makes it open to change by new learning. <bookmark mark='a'/> "
            "The original: Matthew Walker and colleagues, 2003, with a finger-tapping skill. <bookmark mark='b'/> The "
            "record: Daniela Schiller and colleagues' fear that did not return after extinction inside the window, in "
            "2010; Merel Kindt and Marieke Soeter's attempt to repeat it, in which the fear came back; and Hardwicke, Taqi and "
            "Shanks's seven experiments, with no effect. <bookmark mark='c'/> In animals reconsolidation is robust; "
            "in people, the behavioural version has been hard to reproduce. <bookmark mark='d'/> Contested."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_verbal_overshadowing(self):
        card = ledger_card(self._row("verbal_overshadowing"), width=12.8, font_size=24)
        with self.voiceover(
            "And the eighth: describing a face makes it harder to pick from a line-up. <bookmark mark='a'/> The "
            "original: Schooler and Engstler-Schooler, 1990. <bookmark mark='b'/> The record: Meissner and Brigham's "
            "meta-analysis, and the two Registered Replication Reports, sixteen points and four. <bookmark mark='c'/>"
            " Real, smaller than first reported, and sensitive to timing. <bookmark mark='d'/> Replicated, smaller."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()
