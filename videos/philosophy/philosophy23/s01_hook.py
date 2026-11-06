from __future__ import annotations

from videos.philosophy.philosophy23.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.questions()
        self.families()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"Why is there something rather than nothing?", r"G. W. Leibniz",
                       r"`The Principles of Nature and Grace' \ (1714), \ \S 7", width=8.6, font_size=27).next_to(
            t, DOWN, buff=0.5)
        with self.voiceover(
            "Part 22 built the logic of what must be and what might have been. This part turns it on the oldest "
            "question that logic has been asked to settle. <bookmark mark='a'/>Leibniz put it in seven words: why is "
            "there something rather than nothing? <bookmark mark='b'/>For two thousand years philosophers have tried "
            "to answer with proofs: that a perfect being must exist, that the world needs a cause, that its order "
            "needs a designer; and others have tried to prove the opposite, from the evil in the world. This part "
            "checks the proofs. Some are valid and rest on a premise that does all the work; one, when a machine "
            "checked it, turned out to prove far too much."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(q, color=DIV, scale_factor=1.03))
        self.clear_scene()

    def questions(self):
        head = label(r"What a proof of God would need", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"valid", r"the conclusion follows: \ the Reasoner checks the logic, \ as in every part", ARG),
            (r"sound", r"the premises are true: \ here the arguments live or die", DIV),
            (r"not too strong", r"a proof that proves everything, \ or proves rival gods, \ proves nothing", BAD),
            (r"the right God", r"from `a first cause' to `a person who loves you' is a long way", HUM),
            (r"and the other side", r"the problem of evil is an argument too, \ and gets the same scrutiny", NAT),
        ]
        g = rows_table(rows, top=1.9, gap=0.5, width=8.8, x_text=-2.4, label_size=22, text_size=22)
        with self.voiceover(
            "What would a proof of God need? <bookmark mark='a'/>To be valid: the conclusion must follow, and the "
            "Reasoner can check that, as it has checked every argument in this series. <bookmark mark='b'/>To be "
            "sound: its premises must be true, and here the arguments live or die. <bookmark mark='c'/>Not to prove "
            "too much: an argument that proves everything, or that proves rival gods equally well, proves nothing. "
            "<bookmark mark='d'/>To reach the right God: from a first cause to a person who knows and loves you is a "
            "long way. <bookmark mark='e'/>And the arguments against God, above all the problem of evil, are "
            "arguments too, and get the same scrutiny."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def families(self):
        head = label(r"Four families of argument", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        boxes = VGroup()
        items = [(r"ontological", r"from the concept of God alone \ (Anselm, \ Descartes, \ Plantinga, \ Gödel)", ABS),
                 (r"cosmological", r"from the existence of anything \ (Aquinas, \ Leibniz, \ al-Ghazālī)", ARG),
                 (r"teleological", r"from order and fine-tuning \ (Paley, \ the physicists' constants)", NAT),
                 (r"practical", r"from what it is rational to do or to trust \ (Pascal, \ James, \ Plantinga)", WARM)]
        for i, (t, d, c) in enumerate(items):
            x, y = -3.3 + 6.6 * (i % 2), 1.0 - 2.3 * (i // 2)
            b = RoundedRectangle(width=6.0, height=1.9, corner_radius=0.15, color=c, fill_opacity=0.08).move_to(
                [x, y, 0])
            tt = label(t, font_size=26, color=c).move_to([x, y + 0.45, 0])
            dd = wrapped_label(d, 5.4, 19, WHITE).move_to([x, y - 0.3, 0])
            boxes.add(VGroup(b, tt, dd))
        with self.voiceover(
            "The arguments fall into four families. <bookmark mark='a'/>Ontological arguments start from the concept "
            "of God alone: Anselm, Descartes, and, with modal logic, Plantinga and Gödel. <bookmark mark='b'/>"
            "Cosmological arguments start from the fact that anything exists at all: Aquinas, Leibniz, and the "
            "Islamic kalām tradition of al-Ghazālī. <bookmark mark='c'/>Teleological arguments start from order: "
            "Paley's watch, and today the fine-tuning of physical constants. <bookmark mark='d'/>And practical "
            "arguments ask what it is rational to do or to trust: Pascal's wager, William James, and Plantinga's "
            "reformed epistemology."
        ) as vo:
            self.play(FadeIn(head))
            for mk, b in zip("abcd", boxes):
                vo.wait_until(mk)
                self.play(FadeIn(b))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Anselm, \ Gaunilo and Kant; \ Plantinga's argument checked on every small frame",
            r"Gödel's proof in a finite higher-order modal logic: \ inconsistency, \ and modal collapse \ (the Wall)",
            r"Aquinas and Leibniz; \ van Inwagen's collapse of the principle of sufficient reason, \ computed",
            r"the kalām and the infinite; \ design, \ fine-tuning and the multiverse, \ computed",
            r"Pascal's wager with infinite utilities; \ Hájek's mixed strategies",
            r"evil: \ Mackie, \ the free-will defence checked, \ Rowe as Bayes, \ a Price List",
            r"Hume on miracles, \ by the numbers; \ foreknowledge and branching time, \ built",
            r"faith and experience; \ Dharmakīrti, \ Udayana and Avicenna",
        ], font_size=22)
        with self.voiceover(
            "The plan. <bookmark mark='a'/>Anselm's argument, its critics, and Plantinga's modal version, checked on "
            "every small model of modal logic. <bookmark mark='b'/>Gödel's proof, formalized in a finite higher-order "
            "modal logic: the Reasoner rediscovers that Gödel's own axioms are inconsistent, and that the repaired "
            "version collapses all possibility into necessity, this part's brick in the Wall. "
            "<bookmark mark='c'/>The cosmological arguments, and van Inwagen's proof that the principle of "
            "sufficient reason makes everything necessary. <bookmark mark='d'/>The kalām argument and the infinite; "
            "design and fine-tuning, with a multiverse in the calculation. <bookmark mark='e'/>Pascal's wager, and "
            "what infinite utilities do to decision theory. <bookmark mark='f'/>The problem of evil in its logical "
            "and evidential forms. <bookmark mark='g'/>Hume on miracles, by the numbers, and whether divine "
            "foreknowledge leaves us free, with branching time built. <bookmark mark='h'/>And faith, experience, and "
            "arguments from Buddhist, Nyāya and Islamic philosophy."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()
