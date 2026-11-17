from __future__ import annotations

from videos.psychology.psych22.common import *  # noqa: F403


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        self.row_typicality()
        self.row_basic_level()
        self.row_prototype_effect()
        self.row_shj_ordering()
        self.row_shepard_law()
        self.row_similarity_asymmetry()
        self.row_hierarchical_network()
        self.row_semantic_priming()
        self.tally()

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

    def row_typicality(self):
        card = ledger_card(self._row("typicality"), width=12.8, font_size=24)
        with self.voiceover(
            "Eight rows today. The first: members of a category differ reliably in how typical they are, and typical "
            "members are classified faster. <bookmark mark='a'/> The original: Rips, Shoben and Smith, 1973, timing "
            "sentences like a robin is a bird. <bookmark mark='b'/> The record: Rosch's ratings of about fifty members of "
            "ten categories, and McCloskey and Glucksberg's people, who agreed on typicality but changed their minds "
            "about borderline members. <bookmark mark='c'/> One of the sturdiest regularities in cognition. What explains "
            "it is another matter. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_basic_level(self):
        card = ledger_card(self._row("basic_level"), width=12.8, font_size=24)
        with self.voiceover(
            "The second: things are named, verified and first learned at a middle level of abstraction. <bookmark "
            "mark='a'/> The original: Rosch and colleagues, 1976. <bookmark mark='b'/> The record: Murphy and Smith's "
            "artificial tools, and Tanaka and Taylor's experts. <bookmark mark='c'/> Robust, and it moves with expertise. "
            "<bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_prototype_effect(self):
        card = ledger_card(self._row("prototype_effect"), width=12.8, font_size=24)
        with self.voiceover(
            "The third: after learning distortions of a prototype, people classify the unseen prototype as well as the "
            "items they studied. <bookmark mark='a'/> The original: Posner and Keele's dot patterns, 1968. <bookmark "
            "mark='b'/> The record: Homa and Vosburgh's categories of different sizes, whose data we used, and Medin's "
            "two tests where the prototype account lost. <bookmark mark='c'/> The effect is solid. That it shows a stored "
            "prototype is not, because exemplar models predict it too. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_shj_ordering(self):
        card = ledger_card(self._row("shj_ordering"), width=12.8, font_size=24)
        with self.voiceover(
            "The fourth: the six problems of Shepard, Hovland and Jenkins are learned in the order one, two, then three "
            "to five, then six. <bookmark mark='a'/> The original: 1961. <bookmark mark='b'/> The record: Nosofsky and "
            "colleagues' replication in 1994, whose data we fitted, and Kurtz and colleagues in 2013, who did not always "
            "find Type Two easier than Type Four. <bookmark mark='c'/> One first and six last is robust; two's place "
            "depends on the task. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_shepard_law(self):
        card = ledger_card(self._row("shepard_law"), width=12.8, font_size=24)
        with self.voiceover(
            "The fifth: generalization falls off exponentially with distance in psychological space. <bookmark mark='a'/> "
            "The original: Shepard, 1957. <bookmark mark='b'/> The record: Nosofsky's practised observers, whose "
            "gradients were Gaussian; Shepard's twelve data sets in 1987; Sims's derivation from efficient coding in "
            "2018; and this part's reanalysis of Rothkopf's table. <bookmark mark='c'/> Exponential across many data "
            "sets, with exceptions the theory can account for. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_similarity_asymmetry(self):
        card = ledger_card(self._row("similarity_asymmetry"), width=12.8, font_size=24)
        with self.voiceover(
            "The sixth: similarity is asymmetric, the lesser thing more like the greater than the reverse. <bookmark "
            "mark='a'/> The original: Tversky, 1977. <bookmark mark='b'/> The record: Tversky and Gati in 1978; Aguilar "
            "and Medin in 1999, who found no reliable asymmetry in rated similarity at first, and asymmetries only under "
            "some conditions; and this part's recount of Rothkopf. <bookmark mark='c'/> The preference for one phrasing "
            "is strong. Asymmetries in rated similarity are small and fragile. <bookmark mark='d'/> Replicated, smaller."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_hierarchical_network(self):
        card = ledger_card(self._row("hierarchical_network"), width=12.8, font_size=24)
        with self.voiceover(
            "The seventh: knowledge is a hierarchy with each fact stored once, so a fact takes longer to check the more "
            "links it crosses. <bookmark mark='a'/> The original: Collins and Quillian, 1969. <bookmark mark='b'/> The "
            "record: Conrad's familiarity confound in 1972, and the typicality and level reversals of Rips and "
            "colleagues. <bookmark mark='c'/> The strict hierarchy did not survive. The network did. <bookmark mark='d'/> "
            "Failed."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_semantic_priming(self):
        card = ledger_card(self._row("semantic_priming"), width=12.8, font_size=24)
        with self.voiceover(
            "And the eighth: a word is recognized faster after a related word. <bookmark mark='a'/> The original: Meyer "
            "and Schvaneveldt, 1971. <bookmark mark='b'/> The record: Lucas's meta-analysis of priming by meaning alone, "
            "and the Semantic Priming Project's seven hundred and sixty-eight people and sixteen hundred targets. "
            "<bookmark mark='c'/> Real and very reliable, but about nineteen milliseconds, smaller than the hand-picked "
            "pairs of earlier studies suggested. <bookmark mark='d'/> Replicated, smaller."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def tally(self):
        rows = ledger.rows(part=PART)
        head = heading(r"Part 22 in the Ledger")
        counts = {}
        for f in rows:
            counts[f.status] = counts.get(f.status, 0) + 1
        lines = VGroup(*[label(rf"{st}: \ {n}", font_size=30, color=GREY_A) for st, n in counts.items()]).arrange(
            DOWN, buff=0.3, aligned_edge=LEFT).move_to([-3.0, 0.5, 0])
        rows_ = rows_of([
            (r"the regularities held: \ typicality, \ the basic level, \ the prototype effect, \ the ordering, \ "
             r"the law", MODEL),
            (r"what failed was a theory, \ the tidy hierarchy, \ and what shrank were effects first measured on "
             r"the most favourable items", LOST),
            (r"a lesson for the theory chapters: \ data that every model predicts can't choose between them", CAT_A),
        ], 6.2, 22, 0.32).move_to([3.3, 0.3, 0])
        with self.voiceover(
            "Here is the part's tally. <bookmark mark='a'/> The regularities held: typicality, the basic level, the "
            "prototype effect, the ordering of the six problems, and Shepard's law. <bookmark mark='b'/> What failed "
            "was a theory, the tidy hierarchy. What shrank were effects first measured on the most favourable "
            "items. <bookmark mark='c'/> And a lesson for every theory chapter in this part: a result that every "
            "model predicts can't tell you which model is right. It took designs like the five-four structure, and "
            "the six problems, to make the theories disagree."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines))
            for m, r in zip("abc", rows_):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
