from __future__ import annotations

from videos.philosophy.philosophy21.common import *  # noqa: F403


class Relative(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"Relative identity and sortals", r"The same what?", lit=(1967, 1980), part=PART)
        with self.voiceover("Chapter five. Relative identity and sortals."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.geach()
        self.sortals()
        self.criteria()
        self.opaque()

    def geach(self):
        hc = history_card(1967, r"Peter Geach", r"`Identity', \ \textit{Review of Metaphysics}", width=6.0,
                          color=HIST).to_corner(UL, buff=0.3)
        f = MathTex(r"a =_F b \;\;\land\;\; a \ne_G b", font_size=40, color=UNIV).move_to([1.4, 1.6, 0])
        fl = label(r"the same $F$, \ but not the same $G$", font_size=18, color=GREY_A).next_to(f, DOWN, buff=0.15)
        rows = stack([(r"there is no absolute identity, \ only `the same $F$' for sortals $F$", UNIV),
                      (r"the same river, \ not the same water \ (Heraclitus)", PARTC),
                      (r"the same word-type, \ not the same word-token: \ `cat cat' has two of one", WHOLE),
                      (r"the same Trinity doctrine: \ the same God, \ not the same person", ABS),
                      (r"Perry \ (1970): \ each case is two things \textit{related}, \ with absolute identity intact",
                       BAD)], font_size=20, aligned_edge=LEFT, width=9.4).move_to([0.6, -1.2, 0])
        with self.voiceover(
            "Peter Geach argued that identity is always relative to a kind. <bookmark mark='a'/>There is no such "
            "thing as being the same, simply. There is being the same river, the same person, the same word; and a "
            "and b can be the same F but not the same G. <bookmark mark='b'/>The river today is the same river as "
            "yesterday, but not the same water. <bookmark mark='c'/>Cat cat contains the same word twice, but two "
            "tokens. <bookmark mark='d'/>Geach thought the doctrine of the Trinity could be stated coherently this way: "
            "the same God, but not the same person. <bookmark mark='e'/>John Perry replied that each case involves two "
            "distinct things standing in a relation: the waters are not identical, but both constitute one river. "
            "Absolute identity survives."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(fl), FadeIn(rows[0]))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def sortals(self):
        head = label(r"Sortals \ (Wiggins, \ \textit{Sameness and Substance}, \ 1980)", font_size=30,
                     color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"count nouns", r"`cat', \ `ship', \ `person': \ they tell us how to count, \ and when one ends", WHOLE),
            (r"Wiggins", r"identity is absolute, \ but every true identity has a covering sortal that supplies its "
                         r"criterion", GOAL),
            (r"persistence conditions", r"a cat survives losing its tail; \ a ship survives new planks; \ each by "
                                        r"its own kind's rules", PARTC),
            (r"`thing' is not enough", r"`the same thing' has no persistence conditions until we say the same "
                                       r"\textit{what}", BAD),
            (r"ontology in practice", r"OntoClean's identity criteria \ (Part 20) \ are sortals, \ engineered", UNIV),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.6, x_text=-2.2, label_size=20)
        with self.voiceover(
            "David Wiggins kept absolute identity but kept Geach's insight about kinds. <bookmark mark='a'/>Count "
            "nouns, cat, ship, person, tell us how to count things, and when one of them ends. <bookmark mark='b'/>For "
            "Wiggins, identity is absolute, but every true identity statement has a covering sortal that supplies the "
            "criterion for it. <bookmark mark='c'/>A cat survives losing its tail; a ship survives new planks; each by "
            "the rules of its own kind. <bookmark mark='d'/>So the same thing, with no kind specified, has no "
            "persistence conditions at all. <bookmark mark='e'/>Part 20's OntoClean asks engineers for exactly these "
            "identity criteria: sortals, put to work."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def criteria(self):
        head = label(r"Criteria of identity", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [r"\text{kind}", r"\text{criterion}", r"\text{source}"]
        data = [(r"\text{sets}", r"\text{same members}", r"\text{extensionality}"),
                (r"\text{directions}", r"\text{parallel lines}", r"\text{Frege (Part 20)}"),
                (r"\text{numbers}", r"\text{one-to-one correspondence}", r"\text{Hume's principle}"),
                (r"\text{events}", r"\text{same causes and effects}", r"\text{Davidson (1969)}"),
                (r"\text{events}", r"\text{same spacetime region}", r"\text{Quine (1985)}"),
                (r"\text{persons}", r"\text{?}", r"\text{this part}")]
        rows = [[MathTex(a, font_size=22, color=UNIV), MathTex(b, font_size=22), MathTex(c, font_size=20,
                                                                                         color=GREY_A)]
                for a, b, c in data]
        grid = ValueGrid(hd, rows, col_w=[2.4, 4.6, 3.6], cell_h=0.52, font_size=20).move_to([0, 0.3, 0])
        notes = stack([(r"Quine: \ `no entity without identity' \ (Part 20): \ a kind earns its place by having a "
                        r"criterion", GOAL),
                       (r"Davidson's criterion is circular \ (causes are events too); \ he later took Quine's", BAD)],
                      font_size=19, width=12.0).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Sortals bring criteria of identity: principles saying when an F and a G are the same. "
            "<bookmark mark='a'/>Sets are identical when they have the same members. Directions, when their lines "
            "are parallel; numbers, when their concepts correspond one to one, as in Part 20. "
            "<bookmark mark='b'/>Donald Davidson proposed that events are identical when they have the same causes "
            "and effects. <bookmark mark='c'/>Quine objected that this is circular, since causes and effects are "
            "events too, and proposed the same region of spacetime instead; Davidson eventually agreed. "
            "<bookmark mark='d'/>And persons? That is the question of the rest of this part. "
            "<bookmark mark='e'/>Quine's slogan, no entity without identity, says a kind earns its place in our "
            "ontology by having such a criterion."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*grid.cell[i])) for i in range(3)], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*grid.cell[3])))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*grid.cell[4])), FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*grid.cell[5])))
            vo.wait_until("e")
            self.play(FadeIn(notes[0]))
        self.clear_scene()

    def opaque(self):
        head = label(r"When Leibniz's law seems to fail", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        f = VGroup(MathTex(r"\text{Superman} = \text{Clark Kent}", font_size=32, color=OK),
                   MathTex(r"\text{Lois believes Superman can fly}", font_size=30, color=WHITE),
                   MathTex(r"\text{Lois does not believe Clark Kent can fly}", font_size=30, color=BAD)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25).move_to([-2.4, 1.0, 0])
        rows = stack([(r"`believed by Lois to fly' seems true of Superman, \ false of Clark Kent", GOAL),
                      (r"so they differ in a property, \ and are two?", BAD),
                      (r"the standard answer: \ belief contexts are \textit{opaque}; \ `Lois believes $\_$ can fly' "
                       r"is not a property of the man, \ but of how he is presented", UNIV),
                      (r"Quine \ (1956): \ the referential opacity of `believes'; \ Frege's senses \ (Part 27)", ABS),
                      (r"the same diagnosis applies to Evans's step (2), \ and to `could survive squashing'", GREY_A)],
                     font_size=19, aligned_edge=LEFT, width=11.6).move_to([0, -1.5, 0])
        with self.voiceover(
            "Leibniz's law can seem to fail. <bookmark mark='a'/>Superman is Clark Kent. Lois Lane believes Superman "
            "can fly, but does not believe Clark Kent can fly. <bookmark mark='b'/>So being believed by Lois to fly "
            "seems true of Superman and false of Clark Kent. Are they two? <bookmark mark='c'/>The standard answer: "
            "belief contexts are opaque. Lois believes that blank can fly does not express a property of the man, but "
            "of the way he is presented to her. <bookmark mark='d'/>Quine called this referential opacity; Frege's "
            "theory of sense, in Part 27, explains it. <bookmark mark='e'/>The same diagnosis is offered for Evans's "
            "abstraction step, and for the modal predicates of the statue and the lump: perhaps they too depend on "
            "how the object is described."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in f], lag_ratio=0.4))
            for mk, r in zip("bcde", [VGroup(rows[0], rows[1]), rows[2], rows[3], rows[4]]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
