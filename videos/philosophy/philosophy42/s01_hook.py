from __future__ import annotations

from videos.philosophy.philosophy42.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.questions()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"If we use, \ to achieve our purposes, \ a mechanical agency with whose operation we cannot "
                       r"interfere effectively \dots \ we had better be quite sure that the purpose put into the "
                       r"machine is the purpose which we really desire.", r"Norbert Wiener",
                       r"`Some Moral and Technical Consequences of Automation' \ (1960)", width=9.6,
                       font_size=26)
        midas = label(r"King Midas asked that all he touched turn to gold, \ and got exactly what he asked for",
                      font_size=22, color=PROXYC)
        with self.voiceover(
            "This is the last part of the series. It began, in Part 1, with Leibniz's dream: when people disagree, "
            "let them sit down and say, let us calculate. Forty one parts later, the Reasoner calculates a great deal: "
            "it decides arguments, updates beliefs, finds causes, counts votes and audits fairness. <bookmark "
            "mark='a'/>In 1960 the mathematician Norbert Wiener, a founder of cybernetics, saw the next question. If "
            "we use a machine to achieve our purposes, and we cannot interfere effectively once it has started, we "
            "had better be quite sure that the purpose put into the machine is the purpose which we really desire. "
            "<bookmark mark='b'/>King Midas asked that everything he touched turn to gold, and got exactly what he "
            "asked for. This finale asks what we want our reasoners to calculate, and whether we can say it."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(t.animate.scale(0.8).to_edge(UP, buff=0.35))
            q.next_to(t, DOWN, buff=0.45)
            midas.next_to(q, DOWN, buff=0.45)
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(midas))
        self.clear_scene()

    def questions(self):
        head = label(r"Four questions about machines that optimize", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"specification", r"can we write down what we want, \ so that optimizing it is safe?", PROXYC),
                (r"learning", r"can a machine learn what we want from what we do?", TRUEV),
                (r"control", r"will a capable machine let us correct it? \ can it trust itself?", ROBOT),
                (r"legitimacy", r"whose values should it have, \ and how would we know it has them?", HUMAN)]
        g = rows_table(rows, top=1.5, gap=0.55, width=8.4, x_text=-2.4)
        with self.voiceover(
            "Four questions run through the finale. <bookmark mark='a'/>Specification: can we write down what we "
            "want, so that optimizing it is safe? <bookmark mark='b'/>Learning: can a machine learn what we want from "
            "what we do? <bookmark mark='c'/>Control: will a capable machine let us correct it, and can it trust "
            "itself, or its successors? <bookmark mark='d'/>And legitimacy: whose values should it have, and how would "
            "we know it has them? Goodhart's law, a no-free-lunch theorem for values and the Löbian obstacle make up "
            "the last brick in the Wall."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Goodhart's law, \ computed: \ a proxy pushed until the true value bends over; \ mild optimization",
            r"specification gaming, \ in games, \ robots and language models",
            r"learning values: \ inverse reinforcement learning; \ no free lunch for preferences \ (the Wall)",
            r"the off-switch game, \ solved: \ uncertainty is what makes a machine defer",
            r"power-seeking, \ counted on a small world; \ instrumental convergence",
            r"Löb's axiom on every small frame; \ proof-based agents that cooperate",
            r"whose values; \ honesty and deception; \ minds we may be making",
            r"the Wall complete; \ the Price List of alignment; \ back to Leibniz",
        ], font_size=22)
        with self.voiceover(
            "The plan. <bookmark mark='a'/>Goodhart's law, computed: a proxy pushed until the true value bends over, "
            "and a gentler way to optimize. <bookmark mark='b'/>Specification gaming, in games, robots and language "
            "models. <bookmark mark='c'/>Learning values from behaviour, and why behaviour alone cannot settle them: "
            "the Wall. <bookmark mark='d'/>The off-switch game, solved. <bookmark mark='e'/>Power-seeking, counted on "
            "a small world. <bookmark mark='f'/>Löb's theorem checked on every small frame, and proof-based agents "
            "that cooperate because of it. <bookmark mark='g'/>Whose values, honesty and deception, and the minds we "
            "may be making. <bookmark mark='h'/>And the Wall complete, the Price List of alignment, and a return to "
            "Leibniz."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()
