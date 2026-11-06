from __future__ import annotations

from videos.philosophy.philosophy36.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.puzzle()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"I believe that if we destroy mankind, \ as we now can, \ this outcome will be much worse than "
                       r"most people think.", r"Derek Parfit", r"\textit{Reasons and Persons} \ (1984)", width=9.6,
                       font_size=28).next_to(t, DOWN, buff=0.45)
        with self.voiceover(
            "Part 35 asked what makes an act right when the people affected are fixed. This part asks what happens "
            "when our choices decide who will exist, and how many: in having children, in setting climate policy, in "
            "guarding against catastrophe. <bookmark mark='a'/>Derek Parfit ended Reasons and Persons, in 1984, with "
            "a sentence: I believe that if we destroy mankind, as we now can, this outcome will be much worse than "
            "most people think. <bookmark mark='b'/>Population ethics, the study of such choices, is young, "
            "technical, and full of theorems saying that no theory can have everything we want."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(q, color=FUT, scale_factor=1.03))
        self.clear_scene()

    def puzzle(self):
        head = label(r"Four questions about lives not yet lived", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"numbers", r"how do we compare outcomes that contain different numbers of people?", POP),
                (r"quality and quantity", r"is a world of very many lives barely worth living better than one of fewer, "
                                          r"flourishing lives?", WELL),
                (r"time", r"how much should the far future count against the present?", FUT),
                (r"extremes", r"what follows when tiny probabilities meet enormous stakes, \ or the number of lives is "
                              r"infinite?", RISK)]
        g = rows_table(rows, top=1.5, gap=0.55, width=8.2, x_text=-2.2)
        with self.voiceover(
            "Four questions run through the part. <bookmark mark='a'/>How do we compare outcomes that contain "
            "different numbers of people? <bookmark mark='b'/>Is a world of very many lives barely worth living better "
            "than a world of fewer, flourishing ones? <bookmark mark='c'/>How much should the far future count against "
            "the present? <bookmark mark='d'/>And what follows when tiny probabilities meet enormous stakes, or the "
            "number of lives is infinite? Gustaf Arrhenius's impossibility theorems are this part's brick in the "
            "Wall."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"total, \ average, \ critical-level, \ variable value: \ each a formula, \ scored",
            r"the repugnant conclusion; \ mere addition, \ and its Price List",
            r"every view against six conditions, \ by search: \ Arrhenius \ (the Wall)",
            r"the asymmetry; \ the non-identity problem",
            r"discounting: \ the Ramsey rule, \ Stern against Nordhaus",
            r"existential risk: \ when reducing it is worth a great deal",
            r"fanaticism; \ infinite populations, \ with a theorem proved",
            r"cost-effectiveness and QALYs; \ the value of a statistical life",
        ], font_size=22)
        with self.voiceover(
            "The plan. <bookmark mark='a'/>The total, average, critical-level and variable-value views, each a "
            "formula, scored on Parfit's famous sequence. <bookmark mark='b'/>The repugnant conclusion, and the mere "
            "addition paradox with its Price List. <bookmark mark='c'/>An exhaustive search for every view's "
            "counterexamples, and Arrhenius's theorem, this part's brick in the Wall. <bookmark mark='d'/>The "
            "asymmetry, and the non-identity problem. <bookmark mark='e'/>Discounting the future: the Ramsey rule, "
            "derived, and the dispute between Nicholas Stern and William Nordhaus, computed. "
            "<bookmark mark='f'/>Existential risk, and the conditions under which reducing it is worth a great deal. "
            "<bookmark mark='g'/>Fanaticism, and infinite populations, with a theorem proved. "
            "<bookmark mark='h'/>And the tools of practice: cost-effectiveness, quality-adjusted life years, and the "
            "value of a statistical life."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()
