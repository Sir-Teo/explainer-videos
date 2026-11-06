from __future__ import annotations

from videos.philosophy.philosophy37.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.puzzle()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"There are no objective values.", r"J. L. Mackie",
                       r"\textit{Ethics: \ Inventing Right and Wrong} \ (1977), \ opening sentence", width=8.4,
                       font_size=32).next_to(t, DOWN, buff=0.5)
        with self.voiceover(
            "Parts 35 and 36 asked what we ought to do, and built theories precise enough to compute. This part asks "
            "what such claims are. When we say that cruelty is wrong, are we stating a fact, as when we say that "
            "water boils at a hundred degrees, or expressing an attitude, or making a mistake? "
            "<bookmark mark='a'/>John Mackie opened his book Ethics, in 1977, with a five-word sentence: there are no "
            "objective values. <bookmark mark='b'/>Metaethics is the study of whether he was right, and what follows "
            "either way."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(q, color=ANTI, scale_factor=1.03))
        self.clear_scene()

    def puzzle(self):
        head = label(r"Four questions about morality itself", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"logic", r"can an ought ever follow from premises that only say what is?", IS),
                (r"metaphysics", r"are there moral facts, \ and if so, \ what kind of thing are they?", REAL),
                (r"meaning", r"when we call something wrong, \ do we describe it, \ or express an attitude toward "
                             r"it?", EXPR),
                (r"knowledge", r"if our moral sense was shaped by evolution and culture, \ can it track any truth?",
                 MIND)]
        g = rows_table(rows, top=1.5, gap=0.55, width=8.4, x_text=-2.4)
        with self.voiceover(
            "Four questions run through the part. <bookmark mark='a'/>Logic: can an ought ever follow from premises "
            "that only say what is? <bookmark mark='b'/>Metaphysics: are there moral facts, and if so, what kind of "
            "thing are they? <bookmark mark='c'/>Meaning: when we call something wrong, do we describe it, or express "
            "an attitude toward it? <bookmark mark='d'/>And knowledge: if our moral sense was shaped by evolution "
            "and culture, can it track any truth? The is-ought gap, proved as a theorem, and a puzzle about logic "
            "that faces any view on which moral claims are not descriptions, are this part's brick in the Wall."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Hume's law; \ Prior's counterexamples; \ Schurz's theorem, \ checked on 175,616 models",
            r"Moore's open question; \ the naturalistic fallacy; \ the paradox of analysis",
            r"realism, \ natural and non-natural; \ supervenience; \ moral twin earth",
            r"Mackie's error theory; \ companions in guilt; \ the Price List",
            r"expressivism; \ the Frege--Geach problem; \ Gibbard's norm-world pairs, \ built",
            r"relativism and constructivism; \ Street's Darwinian dilemma, \ as an analogy",
            r"moral psychology: \ Haidt, \ Greene; \ Mencius against Xunzi",
            r"reflective equilibrium as weighted MaxSAT; \ moral progress",
        ], font_size=22)
        with self.voiceover(
            "The plan. <bookmark mark='a'/>Hume's law, Arthur Prior's counterexamples, and Gerhard Schurz's theorem, "
            "checked by the Reasoner on every small model of a deontic logic. <bookmark mark='b'/>Moore's open "
            "question, the naturalistic fallacy, and the paradox of analysis. <bookmark mark='c'/>Moral realism, "
            "natural and non-natural, the supervenience challenge, and moral twin earth. <bookmark mark='d'/>Mackie's "
            "error theory, the companions-in-guilt reply, and the Price List. <bookmark mark='e'/>Expressivism, the "
            "Frege-Geach problem, and Allan Gibbard's norm-world pairs, built. <bookmark mark='f'/>Relativism and "
            "constructivism, and Sharon Street's Darwinian dilemma, run as an analogy. <bookmark mark='g'/>Moral "
            "psychology, from Jonathan Haidt to Joshua Greene, and Mencius against Xunzi on human nature. "
            "<bookmark mark='h'/>And reflective equilibrium, built as an optimization, with a word on moral "
            "progress."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()
