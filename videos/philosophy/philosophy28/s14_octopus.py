from __future__ import annotations

from videos.philosophy.philosophy28.common import *  # noqa: F403


class Octopus(VoiceoverScene):
    def construct(self):
        card = chapter_card(13, r"Do language models mean?", r"Can form alone give meaning?", lit=(1990, 2020),
                            part=PART)
        with self.voiceover("Chapter thirteen. Do language models mean?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.octopus()
        self.grounding()
        self.score()
        self.price()

    def octopus(self):
        hc = history_card(2020, r"Emily Bender and Alexander Koller", r"`Climbing towards NLU'", width=6.4,
                          color=HIST).to_corner(UL, buff=0.3)
        isl = VGroup(Ellipse(width=2.2, height=0.9, color=WORLD, fill_opacity=0.3).move_to([-4.6, -0.6, 0]),
                     Ellipse(width=2.2, height=0.9, color=WORLD, fill_opacity=0.3).move_to([4.6, -0.6, 0]))
        names = VGroup(label(r"A", font_size=22, color=USE).next_to(isl[0], UP, buff=0.1),
                       label(r"B", font_size=22, color=USE).next_to(isl[1], UP, buff=0.1))
        cable = Line(isl[0].get_right(), isl[1].get_left(), color=GREY_B, stroke_width=3)
        octo = VGroup(Circle(0.3, color=HEAR, fill_opacity=0.7), *[Line(ORIGIN, 0.45 * np.array([math.cos(a), math.sin(a), 0]),
                                                                       color=HEAR, stroke_width=3).shift(DOWN * 0.15)
                                                                  for a in np.linspace(-PI * 0.9, -PI * 0.1, 6)]
                      ).move_to([0, -1.4, 0])
        otag = label(r"O, \ a hyperintelligent octopus, \ taps the cable", font_size=18, color=HEAR).next_to(octo, DOWN,
                                                                                                         buff=0.15)
        rows = stack([(r"A and B, \ stranded on two islands, \ talk by telegraph", WHITE),
                      (r"O learns the statistics of their messages perfectly, \ and starts replying as B", HEAR),
                      (r"then A writes: \ `a bear is chasing me; \ I have two sticks: \ what do I do?'", BAD),
                      (r"O has never seen a bear or a stick: \ form alone, \ they argue, \ cannot give meaning", GOAL)],
                     font_size=20, aligned_edge=LEFT, width=12.0, buff=0.22).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "In 2020 Emily Bender and Alexander Koller made the sceptical case with a thought experiment. "
            "<bookmark mark='a'/>A and B are stranded on two islands and talk by telegraph cable. "
            "<bookmark mark='b'/>An octopus, O, very intelligent, taps the cable. It learns the statistics of their "
            "messages perfectly, cuts B off, and starts replying in B's place. A notices nothing. "
            "<bookmark mark='c'/>Then A writes: a bear is chasing me, and all I have are two sticks; what should I do? "
            "<bookmark mark='d'/>The octopus has never seen a bear or a stick. Its reply will be a plausible string, "
            "but it cannot connect the words to the world. Form alone, they argue, cannot give meaning, and a model "
            "trained only on text learns form."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(isl), FadeIn(names), Create(cable), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(octo), FadeIn(otag), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def grounding(self):
        head = label(r"Grounding, \ and the replies", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Harnad \ (1990)", r"the symbol grounding problem: \ symbols defined only by other symbols are like a "
                                 r"Chinese--Chinese dictionary to someone who knows no Chinese", HIST),
            (r"conceptual role", r"Piantadosi and Hill \ (2022): \ meaning is in the web of relations among concepts, \ "
                                 r"which text can teach", WORD),
            (r"grounding", r"Mollo and Millière \ (2023): \ grounding can come through causal links carried by the "
                           r"training data, \ and through feedback in fine-tuning", WORLD),
            (r"inferentialism", r"Brandom \ (1994): \ to mean is to take part in the game of giving and asking for "
                                r"reasons", USE),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        with self.voiceover(
            "The argument has a history, and replies. <bookmark mark='a'/>Stevan Harnad named the symbol grounding "
            "problem in 1990: symbols defined only by other symbols are like a Chinese-to-Chinese dictionary for "
            "someone who knows no Chinese. <bookmark mark='b'/>Steven Piantadosi and Felix Hill replied in 2022 that "
            "much of meaning is conceptual role: the web of relations among concepts, which text can teach. "
            "<bookmark mark='c'/>Dimitri Coelho Mollo and Raphaël Millière argued in 2023 that a model's "
            "representations can be grounded after all: through the causal links to the world that its training "
            "data carry, in the spirit of Part 27's externalism, and through the feedback it receives in "
            "fine-tuning. <bookmark mark='d'/>And Robert Brandom's inferentialism, from "
            "1994, says that to mean something is to take part in the game of giving and asking for reasons, a game "
            "that might be played in text."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def score(self):
        d = load("score")
        head = label(r"The game of giving and asking for reasons, \ built", font_size=30, color=CONN).to_edge(UP,
                                                                                                          buff=0.3)
        cols = [("A", "red"), ("A", "coloured"), ("A", "west"), ("A", "east"), ("A", "green"), ("B", "red"),
                ("B", "coloured")]
        moves_txt = [r"A: \ `the apple is red'", r"B: \ `how do you know?'", r"A: \ `I can see it'",
                     r"B: \ `it is red, \ as A says'", r"A: \ `Pittsburgh is west of Philadelphia'",
                     r"A: \ `the apple is green'"]

        def sym(v):
            if v is None:
                return MathTex(r"\cdot", font_size=24, color=GREY_C)
            return MathTex(r"\checkmark" if v else r"\times", font_size=24, color=OK if v else BAD)

        cells = []
        for m, t in zip(d["moves"], moves_txt):
            row = [label(t, font_size=16, color=WORD if m["who"] == "A" else HEAR)]
            for who, c in cols:
                row.append(sym(m["score"][who].get(c)))
            cells.append(row)
        hd = [r"\text{move}"] + [rf"\text{{{w}: {c}}}" for w, c in cols]
        grid = ValueGrid(hd, cells, col_w=[3.9] + [1.2] * 7, cell_h=0.46, font_size=16).move_to([0, 0.5, 0])
        last = d["moves"][-1]["score"]
        assert d["moves"][1]["score"]["A"] == {"red": False, "coloured": False}
        assert d["moves"][3]["score"]["B"] == {"red": True, "coloured": True}
        assert last["A"] == {"red": False, "green": False, "coloured": False, "west": True, "east": True}
        assert last["B"] == {"red": False, "coloured": False}
        key = label(r"$\checkmark$ \ committed and entitled; \ $\times$ \ committed, \ not entitled; \ $\cdot$ \ "
                    r"not committed", font_size=17, color=GREY_A).next_to(grid, DOWN, buff=0.25)
        rules = stack([(r"material inferences: \ red $\Rightarrow$ coloured; \ west of $\Rightarrow$ east of; \ "
                        r"red and green are incompatible", RULE_C),
                       (r"to grasp `red' is to know its place in this game: \ what it commits you to, \ and what it "
                        r"rules out", GOAL)], font_size=19, aligned_edge=LEFT, width=12.0, buff=0.2).to_edge(DOWN,
                                                                                                  buff=0.35)
        with self.voiceover(
            "Brandom's picture can itself be built. <bookmark mark='a'/>A scorekeeper keeps a score for each "
            "speaker: what she is committed to, and which of those commitments she is entitled to. "
            "<bookmark mark='b'/>A asserts that the apple is red. That commits her to it, and to what it materially "
            "implies: that the apple is coloured. <bookmark mark='c'/>B challenges, and A's entitlement is "
            "suspended. <bookmark mark='d'/>A gives a reason: she can see it. The entitlement returns. "
            "<bookmark mark='e'/>B defers to A, and inherits both the commitment and the entitlement. "
            "<bookmark mark='f'/>A asserts something unrelated, that Pittsburgh is west of Philadelphia, and is "
            "committed to its converse as well. <bookmark mark='g'/>Then A asserts that the apple is green. Red and "
            "green are incompatible, so A loses her entitlement to both, and to coloured, which rested on them. B, "
            "who relied on A, loses hers too. Pittsburgh is untouched. <bookmark mark='h'/>On this view, to grasp "
            "red is to know its place in such a game: what it commits you to, and what it rules out. Nothing in the "
            "game requires seeing an apple, though a reason like I can see it is one move in it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(grid.head), Create(grid.rule), FadeIn(key), FadeIn(rules[0]))
            for mk, r in zip("bcdefg", range(6)):
                vo.wait_until(mk)
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.6)
            vo.wait_until("h")
            self.play(FadeIn(rules[1]))
        self.clear_scene()

    def price(self):
        d = load("ground")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        assert sorted(d["mcs"]) == [["M"], ["O"], ["R"], ["T"]]
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.4, width=3.8, font_size=19,
                       center=[0, -0.6, 0], title=r"The Price List: \ the grounding question")
        positions = [(("O",), r"Bender and Koller", r"the outputs only seem meaningful; \ meaning is in the reader"),
                     (("T",), r"Mollo and Millière", r"text carries causal contact, \ at second hand"),
                     (("R",), r"conceptual role", r"reference needs no causal contact; \ inferential role suffices"),
                     (("M",), r"meaning as use", r"meaning is not reference at all: \ Wittgenstein's slogan")]
        with self.voiceover(
            "Four claims cannot all be true. <bookmark mark='a'/>Meaning requires reference. Reference requires causal "
            "contact with what is referred to. A model trained only on text has no such contact. And a language "
            "model's outputs are meaningful. <bookmark mark='b'/>Something has to give. <bookmark mark='c'/>Bender "
            "and Koller give up the last: the outputs only seem meaningful, and the meaning is supplied by the "
            "reader. <bookmark mark='d'/>Mollo and Millière give up the third: text carries causal contact, at "
            "second hand. <bookmark mark='e'/>Conceptual role theorists give up the second: reference needs only the "
            "right inferential role. <bookmark mark='f'/>And a follower of the later Wittgenstein can give up the "
            "first: meaning is use, not reference, and a model's use of words is a use."
        ) as vo:
            self.play(FadeIn(pl.title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(Create(pl.conflict))
            first = True
            for mk, (mcs, name, who) in zip("cdef", positions):
                vo.wait_until(mk)
                if not first:
                    self.play(*pl.reset())
                first = False
                anims, centre = pl.position(mcs, name, who, width=3.0)
                self.play(*anims)
        self.clear_scene()
