from __future__ import annotations

from videos.philosophy.philosophy9.common import *  # noqa: F403


class Predicative(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"The vicious circle", r"May a definition range over what it defines?",
                            lit=(1906, 1918), part=PART)
        with self.voiceover("Chapter eight. The vicious circle."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.poincare()
        self.typical()
        self.weyl()
        self.godel()

    def poincare(self):
        hc = history_card(1906, r"Henri Poincaré", r"`Les mathématiques et la logique'", width=5.2,
                          color=HIST).to_corner(UL, buff=0.35)
        q = quote_card(r"Whatever involves all of a collection must not be one of the collection.", r"Bertrand Russell",
                       r"the vicious-circle principle, \ 1908", width=7.4, font_size=26).to_corner(UR, buff=0.35)
        nl = NumberLine(x_range=[0, 3, 1], length=9, color=GREY_C, include_numbers=False).move_to([0, -0.2, 0])
        S = [0.4, 0.9, 1.3, 1.62, 1.68, 1.72]
        pts = VGroup(*[Dot(nl.n2p(x), radius=0.07, color=NUM) for x in S])
        sl = label(r"a bounded set $S$", font_size=22, color=NUM).next_to(nl.n2p(0.9), UP, buff=0.35)
        ubs = VGroup(*[Line(nl.n2p(x) + DOWN * 0.15, nl.n2p(x) + UP * 0.15, color=GREY_B, stroke_width=3)
                       for x in (1.9, 2.2, 2.5, 2.8)])
        ul = label(r"upper bounds", font_size=22, color=GREY_B).next_to(nl.n2p(2.35), UP, buff=0.35)
        lub = Line(nl.n2p(1.75) + DOWN * 0.3, nl.n2p(1.75) + UP * 0.3, color=GOAL, stroke_width=5)
        ll = label(r"$\sup S$: \ the least of \textit{all} upper bounds", font_size=22, color=GOAL).next_to(
            nl.n2p(1.75), DOWN, buff=0.45)
        moral = VGroup(label(r"it is defined by quantifying over a totality \ (the reals) \ that contains it", font_size=24),
                       label(r"Poincaré: \ such \textit{impredicative} definitions caused the paradoxes \ (Richard's, "
                             r"Part 8)", font_size=24, color=BAD)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Henri Poincaré, in 1906, had his own diagnosis of the paradoxes. <bookmark mark='a'/>They come, he said, "
            "from definitions that are viciously circular. Russell put the principle in one line: whatever involves "
            "all of a collection must not be one of the collection. <bookmark mark='b'/>The trouble is that ordinary "
            "analysis breaks it. Take a bounded set of real numbers. <bookmark mark='c'/>It has many upper bounds. "
            "<bookmark mark='d'/>Its least upper bound is defined as the least of all of them: a definition that "
            "quantifies over all real numbers, including the one being defined. <bookmark mark='e'/>Poincaré called "
            "such definitions impredicative, and blamed them for Richard's paradox, which we met in Part 8."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Create(nl), FadeIn(pts), FadeIn(sl))
            vo.wait_until("c")
            self.play(FadeIn(ubs), FadeIn(ul))
            vo.wait_until("d")
            self.play(Create(lub), FadeIn(ll))
            vo.wait_until("e")
            self.play(FadeIn(moral))
        self.clear_scene()

    def typical(self):
        d = load("typical")
        people = d["people"]
        names = list(people)
        traits = list(next(iter(people.values())))
        head = label(r"Russell's typical Englishman", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        defn = label(r"`a typical Englishman has every property that a majority of Englishmen have'", font_size=22,
                     color=GREY_A).next_to(head, DOWN, buff=0.15)
        hd = [label(r"", font_size=20)] + [label(t, font_size=20, color=P.CLAIM) for t in traits]
        rows = [[label(n, font_size=21)] + [people[n][t] == 1 for t in traits] for n in names]
        grid = ValueGrid(hd, rows, col_w=[1.5, 1.4, 1.55, 1.4, 1.4], cell_h=0.42, font_size=20).move_to(
            [-3.15, -0.75, 0])
        lv = d["levels"]
        assert lv[0]["typical"] == ["Edith"] and lv[1]["typical"] == [] and lv[-1]["typical"] == []
        edith = names.index("Edith")
        res = VGroup(
            label(r"level 0: \ the four traits, \ each held by 5 of 7", font_size=22, color=WHITE),
            label(r"typical at level 0: \ \textbf{Edith} alone", font_size=22, color=OK),
            label(r"level 1: \ add `typical at level 0' \ and its negation", font_size=22, color=WHITE),
            label(r"`untypical' is a majority property: \ 6 of 7", font_size=22, color=GOAL),
            label(r"typical at level 1: \ nobody", font_size=22, color=BAD),
            label(r"every property whatever \ (all 128 groups): \ nobody", font_size=22, color=BAD),
            label(r"for each person $x$, \ `not $x$' is held by 6 of 7", font_size=20, color=GREY_B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.75, -0.8, 0])
        with self.voiceover(
            "Russell's own example, from Principia Mathematica, shows what goes wrong, and the Reasoner builds it. "
            "<bookmark mark='a'/>A typical Englishman is one who has every property that a majority of Englishmen "
            "have. <bookmark mark='b'/>Here are seven people and four traits. Each trait is held by five of the "
            "seven, a majority. <bookmark mark='c'/>So a typical person, judged by these traits, has all four. "
            "Exactly one person does: Edith. <bookmark mark='d'/>But being typical is itself a property. Add it, "
            "and its negation, to the list. <bookmark mark='e'/>Six of the seven are untypical, so being untypical "
            "is a majority property, and a typical person must have it. <bookmark mark='f'/>Now nobody is typical: "
            "Edith, by being typical, fails to be. <bookmark mark='g'/>And if 'property' ranges over every grouping "
            "of the seven whatever, nobody is typical either, because for each person the group of everyone else is "
            "a majority that excludes them. A definition that ranges over all properties, including the one it "
            "defines, destroys itself."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(defn))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule),
                      LaggedStart(*[FadeIn(VGroup(*grid.cell[r])) for r in range(len(rows))], lag_ratio=0.2),
                      FadeIn(res[0]), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(res[1]), Create(grid.row_box(edith)))
            vo.wait_until("d")
            self.play(FadeIn(res[2]))
            vo.wait_until("e")
            self.play(FadeIn(res[3]))
            vo.wait_until("f")
            self.play(FadeIn(res[4]))
            vo.wait_until("g")
            self.play(FadeIn(res[5]), FadeIn(res[6]))
        self.clear_scene()

    def weyl(self):
        hcs = VGroup(history_card(1918, r"Hermann Weyl", r"\textit{Das Kontinuum}", width=4.2, color=HIST),
                     history_card(1964, r"Solomon Feferman; \ Kurt Schütte", r"the limit of predicativity: \ "
                                  r"$\Gamma_0$", width=5.0, color=HIST),
                     history_card(1988, r"Solomon Feferman", r"`Weyl vindicated'", width=3.8, color=HIST)).arrange(
            RIGHT, buff=0.3).to_edge(UP, buff=0.35)
        rows = VGroup(
            label(r"ramified types: \ properties come in levels, \ each defined only from the levels below", font_size=24,
                  color=PROOF),
            label(r"Weyl: \ rebuild analysis predicatively: \ least upper bounds for sequences, \ not for arbitrary "
                  r"sets", font_size=24),
            label(r"how far can it go? \ exactly up to the ordinal $\Gamma_0$ \ (the ladder of Part 7)", font_size=24),
            label(r"Feferman: \ the mathematics that science actually uses \ is predicative", font_size=24,
                  color=OK),
            label(r"reverse mathematics (Part 7) \ measures which theorems need more", font_size=22,
                  color=GREY_B)).arrange(DOWN, buff=0.3).move_to([0, -0.8, 0])
        with self.voiceover(
            "The cure is to stack the properties in levels. <bookmark mark='a'/>Russell's ramified types allow a "
            "property to be defined only from the levels below it, so 'typical' at one level never ranges over "
            "itself. <bookmark mark='b'/>Hermann Weyl, in his book The Continuum of 1918, rebuilt as much of analysis "
            "as he could on that basis. Least upper bounds survive for sequences of numbers, though not for arbitrary "
            "sets. <bookmark mark='c'/>How far can predicative mathematics go? Solomon Feferman and Kurt Schütte "
            "found the exact limit in 1964: the ordinal Gamma zero, on the ladder of Part 7. "
            "<bookmark mark='d'/>And Feferman argued, in 'Weyl vindicated', that the mathematics science actually "
            "uses fits inside that limit. <bookmark mark='e'/>Reverse mathematics, from Part 7, measures exactly "
            "which theorems need more."
        ) as vo:
            self.play(FadeIn(hcs))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def godel(self):
        hc = history_card(1944, r"Kurt Gödel", r"`Russell's mathematical logic'", width=4.8, color=HIST).to_corner(
            UL, buff=0.35)
        left = VGroup(label(r"if we \textit{make} the objects by defining them", font_size=26, color=PROOF),
                      label(r"a definition cannot use what is not yet made:", font_size=22, color=GREY_A),
                      label(r"impredicativity is circular", font_size=24, color=BAD)).arrange(DOWN, buff=0.2)
        right = VGroup(label(r"if the objects exist anyway", font_size=26, color=ABSTRACT),
                       label(r"a definition only picks one out:", font_size=22, color=GREY_A),
                       label(r"`the tallest person in this room'", font_size=24, color=OK)).arrange(DOWN, buff=0.2)
        cols = VGroup(left, right).arrange(RIGHT, buff=1.6).move_to([0, 0.2, 0])
        moral = label(r"so the dispute over a rule of mathematics \ is a dispute about what mathematics is about",
                      font_size=26, color=GOAL).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Kurt Gödel saw that the dispute was philosophical. <bookmark mark='a'/>If mathematical objects are made "
            "by our definitions, a definition cannot use what is not yet made, and impredicative definitions are "
            "circular. <bookmark mark='b'/>But if the objects exist anyway, a definition only picks one of them out, "
            "and there is nothing circular in describing someone as the tallest person in this room, though the "
            "description ranges over everyone in the room, including them. <bookmark mark='c'/>So a technical rule "
            "about definitions turns on what mathematics is about. The platonist may define impredicatively; the "
            "constructivist may not."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(moral))
        self.clear_scene()
