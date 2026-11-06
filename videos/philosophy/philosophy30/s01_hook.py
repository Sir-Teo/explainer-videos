from __future__ import annotations

from videos.philosophy.philosophy30.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.puzzle()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"I propose to consider the question, \ `Can machines think?'\,", r"Alan Turing",
                       r"`Computing Machinery and Intelligence' \ (1950)", width=8.6, font_size=30).next_to(t, DOWN,
                                                                                                  buff=0.45)
        with self.voiceover(
            "Part 29 ended with a question: what is a mind, and could a machine have one? This part takes it head on. "
            "<bookmark mark='a'/>In 1950 Alan Turing opened a paper with it: I propose to consider the question, can "
            "machines think? <bookmark mark='b'/>To answer, we need a theory of what minds are. This part follows the "
            "theories, from Descartes's two substances through behaviourism, the identity theory and functionalism, "
            "and tests each against machines that philosophers have imagined, and some that the Reasoner builds."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(q, color=FUNC, scale_factor=1.03))
        self.clear_scene()

    def puzzle(self):
        head = label(r"Four questions about minds", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"what minds are", r"a substance, \ a way of behaving, \ a brain state, \ or a role that anything could "
                                r"play?", MIND),
            (r"what they do", r"if every physical event has a physical cause, \ what is left for the mind to cause?",
             PHYS),
            (r"what they mean", r"how can a state of a brain, \ or a machine, \ be \textit{about} anything?", SYM),
            (r"machines", r"would a program that passed every test understand anything at all?", FUNC),
        ]
        g = rows_table(rows, top=1.6, gap=0.55)
        with self.voiceover(
            "Four questions run through it. <bookmark mark='a'/>What minds are: a separate substance, a way of "
            "behaving, a state of the brain, or a role that anything, brain or silicon, could play. "
            "<bookmark mark='b'/>What minds do: if every physical event has a physical cause, what is left for the "
            "mind to cause? This is the problem of causal exclusion, this part's brick in the Wall. "
            "<bookmark mark='c'/>What mental states mean: how can a state of a brain, or of a machine, be about "
            "anything, Brentano's question from Part 29? <bookmark mark='d'/>And machines: would a program that "
            "passed every test understand anything at all?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Descartes's dualism and Elisabeth's question; \ Avicenna's floating man",
            r"behaviourism, \ the identity theory, \ and Kripke's objection",
            r"functionalism: \ one machine table, \ two substrates, \ built; \ a role's occupants, \ counted",
            r"Turing's test and his nine objections; \ Searle's Chinese room, \ with a rulebook built",
            r"Blockhead's table, \ measured; \ the China brain and absent qualia",
            r"supervenience checked on worlds; \ Kim's exclusion \ (the Wall; \ a Price List); \ Yablo's pigeon",
            r"emergence: \ a glider gun firing; \ eliminativism; \ Dennett's real patterns, \ measured",
            r"content naturalized; \ the language of thought; \ representation in networks, \ probed",
        ], font_size=22)
        with self.voiceover(
            "The plan. <bookmark mark='a'/>Descartes's two substances, and the question Princess Elisabeth asked "
            "him. <bookmark mark='b'/>Behaviourism, and the theory that the mind is the brain. "
            "<bookmark mark='c'/>Functionalism, with one machine table realized in two very different substrates, and "
            "the occupants of a role counted. "
            "<bookmark mark='d'/>Turing's imitation game, and Searle's Chinese room, with a rulebook the Reasoner "
            "writes. <bookmark mark='e'/>Block's lookup table, measured against the universe, and the China brain. "
            "<bookmark mark='f'/>Supervenience, checked on small sets of worlds, and Kim's exclusion argument, this "
            "part's brick in the Wall and its Price List, and a pigeon that complicates it. "
            "<bookmark mark='g'/>Emergence, with a glider gun firing, the proposal to eliminate the mind altogether, "
            "and Dennett's real patterns, measured. <bookmark mark='h'/>And how mental states could have "
            "content, the language of thought, and what it means for a network to represent something."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()
