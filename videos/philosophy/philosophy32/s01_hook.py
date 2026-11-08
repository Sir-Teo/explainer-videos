from __future__ import annotations

from videos.philosophy.philosophy32.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.puzzle()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"A man can do what he wills, \ but he cannot will what he wills.", r"Arthur Schopenhauer",
                       r"\textit{On the Freedom of the Will} \ (1839), \ as often quoted", width=8.8,
                       font_size=30).next_to(t, DOWN, buff=0.45)
        with self.voiceover(
            "Part 31 asked what it is like to be a mind. This part asks what a mind can do: whether anything we do "
            "is up to us. <bookmark mark='a'/>Arthur Schopenhauer put the worry in 1839, in a line usually quoted "
            "this way: a man can do what he wills, but he cannot will what he wills. <bookmark mark='b'/>If our "
            "willing has causes we did not choose, in what sense are we free, and in what sense are we to blame?"
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(q, color=WILL, scale_factor=1.03))
        self.clear_scene()

    def puzzle(self):
        head = label(r"Four questions about freedom", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"the dilemma", r"if every act is determined, \ is it up to us? \ if it is not determined, \ is it "
                             r"anything but luck?", LAW),
            (r"the arguments", r"can the incompatibility of freedom and determinism be proved? \ the proofs, \ "
                               r"checked on models", FUNC),
            (r"the science", r"does the brain decide before we do? \ can a mind be predicted, \ by itself?", CHANCE),
            (r"the stakes", r"praise and blame, \ luck, \ and machines that act with no one to answer", BLAME),
        ]
        g = rows_table(rows, top=1.6, gap=0.55)
        with self.voiceover(
            "Four questions run through it. <bookmark mark='a'/>The dilemma: if every act is determined by what came "
            "before, is any of it up to us? And if some acts are not determined, are they anything but luck? "
            "<bookmark mark='b'/>The arguments: can the incompatibility of freedom and determinism be proved? Its "
            "proofs use a modal operator whose rules the Reasoner can check on models, and one of them fails. This "
            "is the consequence argument, this part's brick in the Wall. <bookmark mark='c'/>The science: does the "
            "brain decide before we do, and can a mind be predicted, even by itself? <bookmark mark='d'/>And the "
            "stakes: praise and blame, luck, and machines that act with no one left to answer for them."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"determinism defined; \ Laplace's demon; \ the dilemma of luck",
            r"Aristotle's sea battle; \ Chrysippus's cylinder and the lazy argument",
            r"the consequence argument, \ with the operator $N$ and its rules",
            r"rule $\beta$ fails on a model, \ built \ (the Wall); \ the repaired rule holds",
            r"Frankfurt cases, \ modelled; \ compatibilism; \ the free will Price List",
            r"libertarianism and rollback, \ simulated; \ hard incompatibilism; \ Strawson",
            r"Libet's readiness potential, \ from a noisy accumulator; \ self-prediction's diagonal",
            r"the free will theorem; \ moral luck; \ responsibility gaps for machines",
        ], font_size=22)
        with self.voiceover(
            "The plan. <bookmark mark='a'/>What determinism is, Laplace's demon, and the dilemma of luck. "
            "<bookmark mark='b'/>Aristotle's sea battle, and the Stoics' answer to fate. <bookmark mark='c'/>The "
            "consequence argument, with its operator N. <bookmark mark='d'/>A model on which one of its rules fails, "
            "this part's brick in the Wall, and a repaired rule that holds. <bookmark mark='e'/>Frankfurt's cases, "
            "modelled, compatibilism, and the free will Price List. <bookmark mark='f'/>Libertarianism, with a "
            "rollback simulated, the case against free will, and Strawson's reactive attitudes. "
            "<bookmark mark='g'/>Libet's readiness potential, rebuilt from noise, and the diagonal that stops a mind "
            "predicting itself. <bookmark mark='h'/>And the free will theorem of physics, moral luck, and machines "
            "that leave a gap where responsibility should be."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()
