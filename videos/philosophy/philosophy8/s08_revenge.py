from __future__ import annotations

from videos.philosophy.philosophy8.common import *  # noqa: F403


class Revenge(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"Revenge", r"Can a stronger liar defeat the gap?", lit=(1975,), part=PART)
        with self.voiceover("Chapter seven. Revenge."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.strengthened()
        self.run()
        self.field()
        self.context()
        self.brick()

    def strengthened(self):
        head = label(r"The liar comes back", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"Kripke: \ the liar is \textit{neither} true nor false", font_size=28),
            label(r"so the liar is not true", font_size=28, color=GOAL),
            label(r"but that is exactly what the liar says: \ so it is true after all?", font_size=28, color=BAD),
            label(r"the theory cannot say, in its own language, what it says about the liar", font_size=26,
                  color=GREY_A)).arrange(DOWN, buff=0.35).move_to([0, 0.3, 0])
        q = quote_card(r"The ghost of the Tarski hierarchy is still with us.", r"Saul Kripke", r"1975", width=8.4,
                       font_size=28).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Kripke's answer has a weak point, and he saw it. <bookmark mark='a'/>On his theory the liar is "
            "neither true nor false. <bookmark mark='b'/>So, in particular, the liar is not true. "
            "<bookmark mark='c'/>But 'the liar is not true' is what the liar says. Have we just asserted it? "
            "<bookmark mark='d'/>The theorist's verdict, 'neither true nor false', cannot be stated inside the "
            "language the theory is about. Kripke conceded: the ghost of the Tarski hierarchy is still with us."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", rows[:3]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=DOWN * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(q))
        self.clear_scene()

    def run(self):
        d = load("revenge")
        head = label(r"Add the missing words, \ and the construction breaks", font_size=32, color=CONN).to_edge(
            UP, buff=0.45)
        r = sentence_node("R", r"`R' is not true \ (false, or neither)", width=4.0, font_size=22).move_to([-4.4, 1.2, 0])
        op = VGroup(label(r"exclusion negation: \ `not true' is true \ when the sentence is false \textit{or} "
                          r"neither", font_size=22, color=GREY_A)).next_to(r, DOWN, buff=0.35).align_to(r, LEFT)
        chips = VGroup()
        for i, it in enumerate(d["iterates"]):
            c = value_chip(it["R"], 24).move_to([0.6 + 0.9 * i, 1.2, 0])
            s = label(rf"{i}", font_size=20, color=GREY_B).next_to(c, DOWN, buff=0.12)
            chips.add(VGroup(c, s))
        cl = label(r"stage", font_size=20, color=GREY_B).next_to(chips, DOWN, buff=0.5)
        res = VGroup(label(r"it never settles: \ neither, true, false, true, false, \dots", font_size=26, color=BAD),
                     label(rf"the Reasoner checks all three values: \ \textit{{no}} fixed point", font_size=26,
                           color=BAD),
                     label(r"Kripke's construction works only for \textit{monotone} operators: \ ones that never "
                           r"retract", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.6)
        assert d["fixed"] == []
        with self.voiceover(
            "The Reasoner can show the problem directly. <bookmark mark='a'/>Give the language a stronger negation, "
            "'is not true', meaning false or neither. And take the sentence R that says: R is not true, in that "
            "strong sense. <bookmark mark='b'/>Run the construction. At stage zero, R is neither. So 'R is not "
            "true' holds, and at stage one R is true. Then it is false. Then true again. "
            "<bookmark mark='c'/>It never settles, and the Reasoner checks all three possible values: none is a "
            "fixed point. <bookmark mark='d'/>The construction only works because Kripke's logic has no way to say "
            "'neither'. Every gap theory faces this revenge: say what the gap is, and a new liar falls into it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(r))
            vo.wait_until("a")
            self.play(FadeIn(op))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1) for c in chips], lag_ratio=0.4), FadeIn(cl),
                      run_time=4)
            vo.wait_until("c")
            self.play(FadeIn(res[0]), FadeIn(res[1]))
            vo.wait_until("d")
            self.play(FadeIn(res[2]))
        self.clear_scene()

    def field(self):
        hc = history_card(2008, r"Hartry Field", r"\textit{Saving Truth from Paradox}", width=5.6, color=HIST).to_corner(
            UL, buff=0.35)
        rows = VGroup(
            label(r"keep the T-schema for every sentence; \ give up excluded middle \ (a paracomplete logic)",
                  font_size=24),
            label(r"add a determinacy operator $D$: \ the liar is not \textit{determinately} true", font_size=24),
            label(r"but `I am not determinately true' \ is not determinately determinately true \dots", font_size=24,
                  color=SELF),
            label(r"a hierarchy of $D, DD, DDD, \dots$ \ that never closes: \ the ghost, \ tamed but not gone",
                  font_size=24, color=GOAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, -0.3, 0])
        with self.voiceover(
            "The most developed gap theory today is Hartry Field's, from 2008. <bookmark mark='a'/>Field keeps the "
            "T-schema for every sentence, and gives up the law of excluded middle, with a conditional strong "
            "enough to do real reasoning. <bookmark mark='b'/>To describe the liar, he adds an operator for "
            "determinate truth: the liar is not determinately true. <bookmark mark='c'/>But then there is a "
            "sentence that says it is not determinately true, and it is not determinately determinately true. "
            "<bookmark mark='d'/>The determinacy operators form a hierarchy that never closes. The ghost is tamed, "
            "Field argues, but not exorcised."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
        self.clear_scene()


    def context(self):
        hcs = VGroup(history_card(1979, r"Tyler Burge", r"`Semantical paradox'", width=4.6, color=HIST),
                     history_card(2004, r"Michael Glanzberg", r"`A contextual-hierarchical approach to truth and the "
                                  r"liar paradox'", width=6.8, color=HIST)).arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.4)
        rows = VGroup(
            label(r"the strengthened liar is an argument in three steps:", font_size=26),
            label(r"1. \ $L$ is defective, \ so not true \ \ \ 2. \ but that is what $L$ says \ \ \ 3. \ so `$L$ is not "
                  r"true' is true", font_size=24, color=GREY_A),
            label(r"contextualists: \ step 3 is made in a \textit{new context}, \ where `true' has a wider extension",
                  font_size=26, color=GOAL),
            label(r"the hierarchy is real, \ but it is built by conversation, \ not fixed in advance", font_size=26,
                  color=OK),
            label(r"the cost: \ `true in every context' \ invites its own revenge", font_size=24,
                  color=BAD)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(hcs, DOWN, buff=0.5)
        with self.voiceover(
            "One response takes the revenge reasoning seriously. <bookmark mark='a'/>The strengthened liar is an "
            "argument in three steps. The liar is defective, so it is not true. But 'not true' is what it says. "
            "So, we conclude, 'the liar is not true' is true. <bookmark mark='b'/>Contextualists, starting with "
            "Charles Parsons and Tyler Burge in the 1970s, and Michael Glanzberg more recently, say that the last "
            "step happens in a new context, in which the word 'true' has a wider extension than it had before. "
            "<bookmark mark='c'/>Tarski's hierarchy is real, but it is built up by the conversation as it goes, "
            "rather than fixed in advance, which answers Kripke's complaint about Nixon and Jones. "
            "<bookmark mark='d'/>The cost is the familiar one: a sentence that says it is not true in any context "
            "brings the revenge back."
        ) as vo:
            self.play(FadeIn(hcs))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def brick(self):
        w = wall(upto=8, current=8).scale(0.42).move_to([-3.65, -0.2, 0])
        wc = wall_card(8, width=6.4, font_size=22).move_to([3.3, -0.2, 0])
        with self.voiceover(
            "This is the eighth brick in the Wall. <bookmark mark='a'/>The dream: a language that contains its own "
            "truth predicate, and can say everything there is to say about it. The wall: the liar, and its revenge, "
            "which returns against every consistent account that tries to describe its own verdicts. What it "
            "forces: a gap, a glut, or a hierarchy. The next chapters look at the other choices."
        ) as vo:
            self.play(FadeIn(w))
            self.play(Indicate(w.brick[8], color=P.CONCL, scale_factor=1.08))
            vo.wait_until("a")
            self.play(FadeIn(wc))
        self.wait(1)
        self.clear_scene()
