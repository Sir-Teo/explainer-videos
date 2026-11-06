from __future__ import annotations

from videos.philosophy.philosophy27.common import *  # noqa: F403

PROPS = [("conservative", r"\text{cons.}"), ("left_up", r"\uparrow\!\text{noun}"), ("left_down", r"\downarrow\!\text{noun}"),
         ("right_up", r"\uparrow\!\text{verb}"), ("right_down", r"\downarrow\!\text{verb}")]
DEFS = {"every": r"A \subseteq B", "some": r"A \cap B \neq \emptyset", "no": r"A \cap B = \emptyset",
        "most": r"|A \cap B| > |A - B|", "exactly two": r"|A \cap B| = 2", "at least half": r"2|A \cap B| \geq |A|",
        "only": r"B \subseteq A"}


def mark(v, size=24):
    return MathTex(r"\checkmark" if v else r"\times", font_size=size, color=OK if v else BAD)


class Quantifiers(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"Generalized quantifiers", r"What can `most' mean?", lit=(1981, 1986), part=PART)
        with self.voiceover("Chapter eleven. Generalized quantifiers."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.relations()
        self.conservativity()
        self.monotonicity()
        self.game()
        self.theorem()

    def relations(self):
        hc = history_card(1981, r"Jon Barwise and Robin Cooper", r"`Generalized Quantifiers and Natural Language'",
                          width=7.2, color=HIST).to_corner(UL, buff=0.3)
        A = Circle(1.2, color=NAME, fill_opacity=0.12).move_to([-4.6, -0.8, 0])
        B = Circle(1.2, color=REF, fill_opacity=0.12).move_to([-3.2, -0.8, 0])
        tags = VGroup(label(r"$A$: \ students", font_size=19, color=NAME).next_to(A, DOWN, buff=0.1).shift(LEFT * 0.4),
                      label(r"$B$: \ smokers", font_size=19, color=REF).next_to(B, DOWN, buff=0.1).shift(RIGHT * 0.4))
        regions = VGroup(MathTex(r"A - B", font_size=20, color=NAME).move_to([-5.1, -0.8, 0]),
                         MathTex(r"A \cap B", font_size=20, color=TRUTH).move_to([-3.9, -0.8, 0]))
        hd = [r"\text{determiner}", r"Q(A, B)"]
        cells = [[label(k, font_size=21, color=SENSE), MathTex(v, font_size=24)] for k, v in DEFS.items()
                 if k != "only"]
        grid = ValueGrid(hd, cells, col_w=[3.0, 3.6], cell_h=0.48, font_size=21).move_to([3.0, -0.6, 0])
        with self.voiceover(
            "Montague treated every as a relation between two properties. Jon Barwise and Robin Cooper, in 1981, "
            "made that the basis of a general theory. <bookmark mark='a'/>A determiner relates two sets: the noun's "
            "set A, the students, and the verb phrase's set B, the smokers. <bookmark mark='b'/>Every A is B says A "
            "is included in B. Some A is B says they overlap; no A is B, that they do not. <bookmark mark='c'/>Most A "
            "are B compares two regions of the diagram: more students who smoke than students who do not. "
            "<bookmark mark='d'/>Exactly two, at least half, and many more fit the same pattern: each determiner "
            "is a condition on the sizes and inclusions of two sets."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(B), FadeIn(tags), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("b")
            for r in range(3):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.5)
            vo.wait_until("c")
            self.play(FadeIn(regions), *[FadeIn(c) for c in grid.cell[3]])
            vo.wait_until("d")
            for r in range(4, len(cells)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.5)
        self.clear_scene()

    def conservativity(self):
        d, c = load("gq"), load("conscount")
        head = label(r"Conservativity", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        law = MathTex(r"Q(A, B) \iff Q(A, A \cap B)", font_size=36, color=GOAL).move_to([0, 2.0, 0])
        ex = label(r"`every student smokes' \ $\iff$ \ `every student is a student who smokes'", font_size=21,
                   color=GREY_A).next_to(law, DOWN, buff=0.25)
        rows_d = d["rows"]
        assert all(rows_d[k]["conservative"] for k in rows_d if k != "only") and not rows_d["only"]["conservative"]
        hd = [r"\text{determiner}", r"\text{conservative, on all } %d \text{ pairs}" % d["pairs"]]
        cells = [[label(k, font_size=20, color=BAD if k == "only" else SENSE), mark(v["conservative"])]
                 for k, v in rows_d.items()]
        grid = ValueGrid(hd, cells, col_w=[2.8, 5.2], cell_h=0.4, font_size=19).move_to([-2.6, -1.0, 0])
        assert c["all"] == 65536 and c["conservative"] == 512 == c["formula"]
        side = stack([(r"`only' fails: \ `only students smoke' is not `only students are students who smoke'", BAD),
                      (r"and `only' is not a determiner: \ it also attaches to names and verbs", HIST),
                      (r"on a 2-element universe: \ 65\,536 possible determiner meanings; \ 512 conservative", TRUTH),
                      (r"Keenan and Stavi \ (1986): \ every natural-language determiner is conservative", GOAL)],
                     font_size=20, aligned_edge=LEFT, width=5.0, buff=0.28).move_to([4.2, -1.0, 0])
        with self.voiceover(
            "Now a surprise about natural language. <bookmark mark='a'/>Every determiner the theory has found obeys "
            "a law called conservativity: whether Q A's are B depends only on the A's. Every student smokes is "
            "equivalent to every student is a student who smokes. <bookmark mark='b'/>The Reasoner checks seven "
            "candidates on every pair of sets over a four-element universe, two hundred and fifty-six pairs. Six "
            "pass. <bookmark mark='c'/>The one that fails is only. Only students smoke is not equivalent to only "
            "students are students who smoke, which is trivially true. And only is not a determiner at all: it "
            "attaches to names and verbs too. <bookmark mark='d'/>Conservativity is a strong restriction. On a "
            "universe of just two things, there are sixty-five thousand five hundred and thirty-six relations "
            "between sets; the Reasoner counts the conservative ones by brute force: five hundred and twelve. "
            "<bookmark mark='e'/>Edward Keenan and Jonathan Stavi conjectured in 1986 that every determiner in every "
            "human language is among them."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(law), FadeIn(ex))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(len(cells)):
                self.play(*[FadeIn(x) for x in grid.cell[r]], run_time=0.3)
            for mk, r in zip("cde", (side[:2], side[2:3], side[3:])):
                vo.wait_until(mk)
                self.play(*[FadeIn(x) for x in r])
        self.clear_scene()

    def monotonicity(self):
        d = load("gq")
        head = label(r"Monotonicity, \ and the inferences it licenses", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rows_d = d["rows"]
        hd = [r"\text{determiner}"] + [t for _, t in PROPS[1:]]
        cells = [[label(k, font_size=20, color=SENSE)] + [mark(rows_d[k][p], 22) for p, _ in PROPS[1:]]
                 for k in ("every", "some", "no", "most", "exactly two")]
        grid = ValueGrid(hd, cells, col_w=[2.6, 1.9, 1.9, 1.9, 1.9], cell_h=0.45, font_size=19).move_to([0, 0.8, 0])
        assert rows_d["every"]["left_down"] and rows_d["every"]["right_up"] and not rows_d["every"]["left_up"]
        assert rows_d["most"]["right_up"] and not rows_d["most"]["left_down"] and not rows_d["most"]["left_up"]
        ex = stack([(r"every: \ `every dog barks' $\Rightarrow$ `every small dog barks' \ (noun $\downarrow$), \ "
                     r"$\Rightarrow$ `every dog makes noise' \ (verb $\uparrow$)", NAME),
                    (r"some: \ upward in both; \ no: \ downward in both", REF),
                    (r"most: \ upward in the verb, \ but neither way in the noun", BAD),
                    (r"these patterns decide much of everyday inference: \ chapter 15 tests machines on them", GOAL)],
                   font_size=20, aligned_edge=LEFT, width=12.4, buff=0.22).move_to([0, -2.1, 0])
        with self.voiceover(
            "Determiners also differ in which inferences they license. <bookmark mark='a'/>The Reasoner checks, for "
            "each, whether making the noun's set bigger or smaller, or the verb's set bigger or smaller, preserves "
            "truth, on every choice of sets. <bookmark mark='b'/>Every is downward in the noun and upward in the "
            "verb: every dog barks entails every small dog barks, and every dog makes noise. "
            "<bookmark mark='c'/>Some is upward in both places, and no is downward in both. "
            "<bookmark mark='d'/>Most is upward in the verb but neither way in the noun: most dogs bark does not "
            "tell you whether most small dogs do. <bookmark mark='e'/>These monotonicity patterns decide a large "
            "share of everyday reasoning, and chapter fifteen tests machines on them."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("b")
            self.play(*[FadeIn(x) for x in grid.cell[0]], FadeIn(ex[0]))
            vo.wait_until("c")
            self.play(*[FadeIn(x) for x in grid.cell[1]], *[FadeIn(x) for x in grid.cell[2]], FadeIn(ex[1]))
            vo.wait_until("d")
            self.play(*[FadeIn(x) for x in grid.cell[3]], *[FadeIn(x) for x in grid.cell[4]], FadeIn(ex[2]))
            vo.wait_until("e")
            self.play(FadeIn(ex[3]))
        self.clear_scene()

    def game(self):
        d = load("ef")
        head = label(r"An Ehrenfeucht--Fraïssé game", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        k = 3
        row = next(r for r in d["rows"] if r["k"] == k)
        assert row["duplicator_k"] and not row["duplicator_k_plus_1"] and row["most_M1"] and not row["most_M2"]

        def structure(p, q, y, name, most):
            dots = VGroup(*[Dot(radius=0.16, color=TRUTH) for _ in range(p)] +
                          [Dot(radius=0.16, color=GREY_B) for _ in range(q)]).arrange(RIGHT, buff=0.45)
            dots.move_to([0.6, y, 0])
            nm = label(name, font_size=22, color=WORLD).next_to(dots, LEFT, buff=0.6)
            mt = label((r"`most things are $P$': \ " + ("true" if most else "false")), font_size=18,
                       color=OK if most else BAD).next_to(dots, RIGHT, buff=0.5)
            return VGroup(dots, nm, mt)

        m1 = structure(*row["M1"], 1.3, r"$M_1$", True)
        m2 = structure(*row["M2"], -0.4, r"$M_2$", False)
        key = label(r"gold: \ $P$; \ grey: \ not $P$", font_size=18, color=GREY_A).next_to(m2, DOWN, buff=0.35)
        # three rounds: (structure, index) chosen by Spoiler, Duplicator's answer
        moves = [((0, 0), (1, 0)), ((1, 5), (0, 5)), ((0, 1), (1, 1))]
        pebble_cols = [SPEAK, NAME, SENSE]
        rows = stack([(r"Spoiler picks an element in either structure; \ Duplicator answers in the other", WHITE),
                      (r"Duplicator wins if the picks always match: \ same colour, \ same equalities", OK),
                      (r"with 3 rounds, \ Duplicator always can: \ each colour has at least 3 elements on both sides",
                       GOAL)], font_size=20, aligned_edge=LEFT, width=12.4, buff=0.2).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Can most be defined in first-order logic, from every, some and not? The answer is no, and the proof is "
            "a game. <bookmark mark='a'/>Take two structures. The first has four things that are P and three that "
            "are not, so most things are P. The second has three that are P and four that are not, so most things "
            "are not. <bookmark mark='b'/>Two players, Spoiler and Duplicator, play for three rounds. Each round, "
            "Spoiler places a pebble on an element of either structure, and Duplicator answers with a pebble in the "
            "other. <bookmark mark='c'/>Duplicator wins if, at the end, the pebbled elements match: the same colours, "
            "and the same pattern of which are equal. <bookmark mark='d'/>Spoiler picks a P in the first; Duplicator "
            "answers with a P. Spoiler picks a non-P in the second; Duplicator answers in kind. Spoiler picks "
            "another P; Duplicator still has one to give. <bookmark mark='e'/>With three rounds, Duplicator can "
            "always keep up, because each colour has at least three elements on both sides."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(m1), FadeIn(m2), FadeIn(key))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            for (sp, du), col in zip(moves, pebble_cols):
                s_dot = (m1 if sp[0] == 0 else m2)[0][sp[1]]
                d_dot = (m1 if du[0] == 0 else m2)[0][du[1]]
                ring_s = Circle(0.27, color=col, stroke_width=5).move_to(s_dot)
                ring_d = Circle(0.27, color=col, stroke_width=5).move_to(d_dot)
                self.play(Create(ring_s), run_time=0.6)
                self.play(Create(ring_d), run_time=0.6)
                self.wait(0.6)
            vo.wait_until("e")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def theorem(self):
        d = load("ef")
        head = label(r"`Most' is not first-order", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [r"k", r"M_1 \; (P,\ \text{not } P)", r"M_2", r"\text{Duplicator wins } k \text{ rounds}",
              r"k + 1 \text{ rounds}"]
        cells = [[MathTex(str(r["k"]), font_size=24), MathTex(f"({r['M1'][0]},\\ {r['M1'][1]})", font_size=24),
                  MathTex(f"({r['M2'][0]},\\ {r['M2'][1]})", font_size=24), mark(r["duplicator_k"]),
                  mark(r["duplicator_k_plus_1"])] for r in d["rows"]]
        assert all(r["duplicator_k"] and not r["duplicator_k_plus_1"] for r in d["rows"])
        grid = ValueGrid(hd, cells, col_w=[0.8, 2.6, 1.8, 3.8, 2.4], cell_h=0.45, font_size=20).move_to([0, 0.9, 0])
        rows = stack([(r"Ehrenfeucht \ (1961), \ Fraïssé \ (1954): \ Duplicator wins $k$ rounds iff the structures "
                       r"agree on every sentence with $k$ nested quantifiers", HIST),
                      (r"so no first-order sentence of depth $k$ separates $M_1$ from $M_2$; \ but `most' does", BAD),
                      (r"$k$ was arbitrary: \ `most' is not definable in first-order logic, \ even on finite "
                       r"structures", GOAL),
                      (r"natural language outruns the logic of Frege and Russell", TRUTH)], font_size=20,
                     aligned_edge=LEFT, width=12.4, buff=0.22).move_to([0, -1.8, 0])
        with self.voiceover(
            "The Reasoner plays the game exhaustively for four sizes. <bookmark mark='a'/>For each k, the first "
            "structure has k plus one P's and k others, the second the reverse. Duplicator wins every k-round game, "
            "and loses with one round more. <bookmark mark='b'/>The theorem of Andrzej Ehrenfeucht and Roland "
            "Fraïssé says Duplicator wins the k-round game exactly when the two structures satisfy the same "
            "sentences with at most k nested quantifiers. <bookmark mark='c'/>So no first-order sentence of depth k "
            "can tell these two structures apart. But most things are P is true in one and false in the other. "
            "<bookmark mark='d'/>Since every first-order sentence has some depth k, none of them means most. "
            "<bookmark mark='e'/>Natural language, in one small word, outruns the logic that Frege and Russell "
            "built to analyse it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(len(cells)):
                self.play(*[FadeIn(x) for x in grid.cell[r]], run_time=0.4)
            for mk, r in zip("bcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
