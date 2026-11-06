from __future__ import annotations

from videos.philosophy.philosophy26.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.puzzle()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"I think I can safely say that nobody understands quantum mechanics.", r"Richard Feynman",
                       r"\textit{The Character of Physical Law} \ (1965)", width=9.2, font_size=28).next_to(
            t, DOWN, buff=0.45)
        with self.voiceover(
            "Part 25 ended at the edge of quantum gravity. This part goes to the theory that every part of physics "
            "now rests on, and that nobody agrees how to read. <bookmark mark='a'/>Richard Feynman, who did as much "
            "as anyone to build it, said in 1965: I think I can safely say that nobody understands quantum "
            "mechanics. <bookmark mark='b'/>The trouble is not the mathematics, which is clean, and not the "
            "predictions, which are the most accurate in science. The trouble is what the theory says the world is "
            "like. This part builds the theorems that force a choice, and the theories that make it."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(q, color=WAVE, scale_factor=1.03))
        self.clear_scene()

    def puzzle(self):
        head = label(r"The puzzle, \ in three lines", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"the success", r"predictions confirmed to twelve decimal places: \ the electron's magnetic moment", OK),
            (r"the silence", r"the theory says how to compute outcomes, \ not what happens when no one measures", BAD),
            (r"the theorems", r"Bell, \ Kochen--Specker, \ PBR, \ Frauchiger--Renner: \ whatever the world is like, \ "
                              r"it is not like a classical world with hidden values", ABS),
            (r"the options", r"Bohm's particles, \ GRW's collapses, \ Everett's many worlds, \ QBism's beliefs: \ each "
                             r"pays a different price", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        with self.voiceover(
            "Here is the puzzle in three lines and a coda. <bookmark mark='a'/>The success: quantum theory's "
            "prediction of the electron's magnetic moment matches experiment to about twelve significant figures. "
            "<bookmark mark='b'/>The silence: the textbook theory tells you how to compute the probabilities of "
            "measurement outcomes, but not what is happening when no one is measuring, or what a measurement is. "
            "<bookmark mark='c'/>The theorems: a series of results, Bell's, Kochen and Specker's, and more recent "
            "ones, prove that whatever the world is like, it is not like a classical world in which every quantity "
            "has a hidden value waiting to be revealed. <bookmark mark='d'/>And the options: Bohm's particles, "
            "GRW's collapses, Everett's many worlds, QBism's beliefs. Each pays a different price, and this part "
            "prices them."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"the formalism: \ states, \ superposition, \ the Born rule, \ sampled",
            r"the measurement problem: \ Maudlin's three claims, \ as a Price List",
            r"EPR; \ Bell and CHSH derived: \ every local strategy enumerated, \ Tsirelson's bound",
            r"the CHSH game, \ classical 3/4 against quantum 0.854 \ (the Wall); \ the experiments",
            r"GHZ and the Peres--Mermin square: \ every assignment checked, \ none works",
            r"PBR: \ the wavefunction is real; \ Everett and decoherence, \ computed",
            r"Bohm's trajectories through two slits, \ built; \ GRW's collapses, \ simulated",
            r"QBism, \ relational views, \ Wigner's friend; \ the free will theorem; \ quantum technology",
        ], font_size=22)
        with self.voiceover(
            "The plan. <bookmark mark='a'/>The formalism in one chapter. <bookmark mark='b'/>The measurement "
            "problem, as three claims that cannot all be true. <bookmark mark='c'/>Einstein, Podolsky and Rosen's "
            "argument, and Bell's theorem, derived step by step, with every local strategy enumerated. "
            "<bookmark mark='d'/>The CHSH game, this part's brick in the Wall, and the experiments that settled it. "
            "<bookmark mark='e'/>Two more no-go results, checked by brute force. <bookmark mark='f'/>A theorem that "
            "the wavefunction is real, and Everett's many worlds, with decoherence computed. "
            "<bookmark mark='g'/>Bohm's particles and their trajectories, and spontaneous collapse, simulated. "
            "<bookmark mark='h'/>And the views that make quantum states perspectival, with what all of it means for "
            "free will and technology."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()
