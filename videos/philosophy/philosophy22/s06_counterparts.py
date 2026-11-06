from __future__ import annotations

from videos.philosophy.philosophy22.common import *  # noqa: F403


class Counterparts(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"Counterpart theory, \ translated", r"Who wins, \ in the world where Humphrey wins?",
                            lit=(1968, 1986), part=PART)
        with self.voiceover("Chapter five. Counterpart theory, translated."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.postulates()
        self.scheme()
        self.islands()
        self.census()
        self.reply()

    def postulates(self):
        hc = history_card(1968, r"David Lewis", r"`Counterpart Theory and Quantified Modal Logic'", width=7.0,
                          color=HIST).to_corner(UL, buff=0.3)
        prim = label(r"primitives: \ $Wx$ \ ($x$ is a world); \ $Ixy$ \ ($x$ is in $y$); \ $Cxy$ \ ($x$ is a "
                     r"counterpart of $y$)", font_size=22, color=ABS).next_to(hc, DOWN, buff=0.35).to_edge(LEFT,
                                                                                                    buff=0.6)
        ps = [
            (r"P1", r"$\forall x \forall y\,(Ixy \to Wy)$", r"nothing is in anything but a world"),
            (r"P2", r"$\forall x \forall y \forall z\,(Ixy \land Ixz \to y = z)$", r"nothing is in two worlds"),
            (r"P5", r"$\forall x \forall y \forall z\,(Ixy \land Izy \land Cxz \to x = z)$",
             r"nothing is a counterpart of anything else in its own world"),
            (r"P6", r"$\forall x \forall y\,(Ixy \to Cxx)$", r"anything in a world is its own counterpart"),
        ]
        rows = VGroup()
        for i, (k, f, gl) in enumerate(ps):
            y = 0.4 - 0.62 * i
            a = label(k, font_size=21, color=GOAL).move_to([-6.1, y, 0])
            b = label(f, font_size=21, color=WHITE)
            b.move_to([-5.5 + b.width / 2, y, 0])
            c = label(gl, font_size=19, color=GREY_A)
            c.move_to([0.6 + c.width / 2, y, 0])
            rows.add(VGroup(a, b, c))
        notes = stack([(r"individuals are world-bound: \ Humphrey is in our world only", WORLD),
                       (r"the counterpart relation is similarity: \ not transitive, \ not symmetric, \ not one-one",
                        CPT)], font_size=21, aligned_edge=LEFT, width=12.0).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Lewis's worlds are isolated, so no individual is in two of them. Then how can Humphrey have possibly "
            "won, if Humphrey exists only here? Lewis's answer came in a paper of 1968. <bookmark mark='a'/>Take "
            "three primitives: being a world, being in a world, and being a counterpart of something. "
            "<bookmark mark='b'/>Then postulates. Nothing is in anything but a world. Nothing is in two worlds. "
            "Nothing is a counterpart of anything else in its own world. And anything in a world is a counterpart of "
            "itself. <bookmark mark='c'/>So individuals are world-bound. <bookmark mark='d'/>What links them across "
            "worlds is the counterpart relation, a relation of similarity: your counterparts in another world are "
            "the things there that resemble you closely enough, and more closely than anything else there does. "
            "Similarity need not be transitive, or symmetric, or one-one, and neither need the counterpart relation."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(prim))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.35), run_time=3)
            for mk, r in zip("cd", notes):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def scheme(self):
        head = label(r"The translation scheme", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        lines = [
            (r"\forall x\, \varphi", r"\forall x\,(Ix@ \to \varphi)", r"quantifiers stay in the world of evaluation"),
            (r"\Box\, \varphi(x)", r"\forall w\,\big(Ww \to \forall y\,(Iyw \land Cyx \to \varphi(y))\big)",
             r"in every world, \ every counterpart of $x$"),
            (r"\Diamond\, \varphi(x)", r"\exists w\,\big(Ww \land \exists y\,(Iyw \land Cyx \land \varphi(y))\big)",
             r"in some world, \ some counterpart of $x$"),
        ]
        rows = VGroup()
        for i, (a, b, c) in enumerate(lines):
            y = 1.7 - 1.15 * i
            l = MathTex(a, font_size=34, color=ABS).move_to([-5.2, y, 0])
            arr = MathTex(r"\mapsto", font_size=34).move_to([-3.9, y, 0])
            r = MathTex(b, font_size=32, color=CPT)
            r.move_to([-3.4 + r.width / 2, y, 0])
            g = label(c, font_size=18, color=GREY_A).next_to(r, DOWN, buff=0.1).align_to(r, LEFT)
            rows.add(VGroup(l, arr, r, g))
        d = load("humphrey")
        mt = d["rows"][0]["translation"]
        ex = VGroup(label(r"`Humphrey might have won' \ $\Diamond\, \mathit{Won}\, h$ \ becomes", font_size=21,
                          color=NAME),
                    MathTex(mt, font_size=27, color=CPT)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.45)
        if ex[1].width > 12.6:
            ex[1].width = 12.6
        with self.voiceover(
            "With these primitives, every sentence of quantified modal logic can be translated into plain "
            "first-order logic about worlds and their inhabitants. <bookmark mark='a'/>A quantifier is restricted to "
            "the world of evaluation: for all x becomes for all x in the actual world. <bookmark mark='b'/>A box "
            "over a formula about x becomes: in every world, every counterpart of x satisfies the formula. "
            "<bookmark mark='c'/>A diamond becomes: in some world, some counterpart of x satisfies it. "
            "<bookmark mark='d'/>The Reasoner implements the translation. Humphrey might have won becomes: there is "
            "a world, and something in it that is a counterpart of Humphrey, and it won. Modal logic has been "
            "reduced to first-order logic with an extra relation, and the Reasoner can check the reduction."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r[0]), FadeIn(r[1]), Write(r[2]), FadeIn(r[3]))
            vo.wait_until("d")
            self.play(FadeIn(ex[0]), Write(ex[1]))
        self.clear_scene()

    def islands(self):
        d = load("humphrey")
        head = label(r"Lewis's islands", font_size=30, color=CONN).to_edge(UP, buff=0.25)
        lay = {"@": ([-4.9, -0.3, 0], 2.8, 2.0), "w1": ([-1.3, 1.75, 0], 2.6, 1.15),
               "w2": ([-1.3, -0.2, 0], 2.6, 1.15), "w3": ([-1.3, -2.15, 0], 2.6, 1.15)}
        names = {"@": r"actual", "w1": r"$w_1$", "w2": r"$w_2$", "w3": r"$w_3$"}
        pos = {"h": [-5.5, -0.3, 0], "n": [-4.3, -0.3, 0], "h1": [-1.8, 1.7, 0], "n1": [-0.8, 1.7, 0],
               "h2": [-1.8, -0.25, 0], "h2'": [-0.8, -0.25, 0], "m": [-1.3, -2.2, 0]}
        tags = {"h": r"Humphrey", "n": r"Nixon", "h1": r"$h_1$", "n1": r"$n_1$", "h2": r"$h_2$", "h2'": r"$h_2'$",
                "m": r"$m$"}
        isl = VGroup()
        for k, (w, (c, ww, hh)) in enumerate(lay.items()):
            isl.add(island(c, w=ww, h=hh, seed=120 + k, color=NAME if w == "@" else WORLD, name=names[w],
                           font_size=18))
        folk = VGroup(*[person(p, color=NAME if k in ("h", "h1", "h2", "h2'") else DESC, name=tags[k], font_size=17)
                        for k, p in pos.items()])
        won = VGroup(*[label(r"won", font_size=17, color=GOAL).next_to(np.array(pos[k]), UP, buff=0.18)
                       for k in d["won"]])
        bridges = VGroup()
        for x, y in d["C"]:
            col = NAME if y == "h" else DESC
            bridges.add(CurvedArrow(np.array(pos[y]) + RIGHT * 0.12, np.array(pos[x]) + LEFT * 0.15, angle=-0.35,
                                    color=col, stroke_width=2, tip_length=0.14))
        VGroup(isl, folk, won, bridges).scale(1.1, about_point=np.array([-3.2, -0.2, 0]))
        rows = d["rows"]
        out = VGroup()
        for i, r in enumerate([rows[0], rows[4], rows[2], rows[3]]):
            y = 1.7 - 0.95 * i
            nm = label(r["name"], font_size=21, color=WHITE).move_to([3.3, y + 0.2, 0])
            fm = MathTex(r["formula"], font_size=22, color=GREY_A)
            if fm.width > 4.6:
                fm.width = 4.6
            fm.move_to([3.3, y - 0.18, 0])
            mk = mark(r["direct"]).move_to([6.2, y, 0])
            out.add(VGroup(nm, fm, mk))
        foot = label(r"direct semantics and translation agree on every row", font_size=17, color=GREY_B).move_to(
            [3.3, -2.3, 0])
        with self.voiceover(
            "Here is the model the Reasoner uses. <bookmark mark='a'/>Four worlds. In ours, Humphrey and Nixon ran, "
            "and Nixon won. In w one, Humphrey's counterpart won. In w two, two people resemble Humphrey equally "
            "well: identical twins, both his counterparts. In w three, one person, m, resembles both Humphrey and "
            "Nixon enough to be a counterpart of each. <bookmark mark='b'/>The bridges are the counterpart "
            "relation. <bookmark mark='c'/>Humphrey might have won: true, because his counterpart in w one won. "
            "<bookmark mark='d'/>Everything is necessarily self-identical: true. <bookmark mark='e'/>But the "
            "necessity of identity fails. Let x and y both be Humphrey. In w two, x has one counterpart and y "
            "another, and they are different people, so necessarily x equals y is false. <bookmark mark='f'/>And "
            "the necessity of distinctness fails: Humphrey and Nixon are two, but in w three they share a "
            "counterpart. <bookmark mark='g'/>On each row, evaluating the modal sentence directly and evaluating "
            "its first-order translation give the same answer."
        ) as vo:
            self.play(FadeIn(head), FadeIn(isl), FadeIn(folk))
            vo.wait_until("a")
            self.play(FadeIn(won))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(b) for b in bridges], lag_ratio=0.2), run_time=2.5)
            for mk, r in zip("cdef", out):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("g")
            self.play(FadeIn(foot))
        self.clear_scene()

    def census(self):
        d = load("census")
        head = label(r"Every small model, \ checked", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        P_ = d["principles"]
        keys = ["refl", "NI", "ND", "T", "4", "B", "BF", "CBF", "NE"]
        hd = [r"\text{principle}", r"\text{Kripke, constant}", r"\text{Kripke, varying}", r"\text{counterparts}"]
        rows = []
        for k in keys:
            v = P_[k]
            cells = [label(v["name"], font_size=17)]
            for col in ("k_const_counter", "k_var_counter", "cp_counter"):
                n = v[col]
                cells.append(MathTex(r"\text{valid}" if n == 0 else rf"{n}\ \text{{fail}}", font_size=19,
                                     color=OK if n == 0 else BAD))
            rows.append(cells)
        grid = ValueGrid(hd, rows, col_w=[4.6, 2.5, 2.5, 2.5], cell_h=0.43, font_size=18).move_to([0, -0.2, 0])
        foot = label(r"counterpart models: \ " + f"{d['cp_models']:,}".replace(",", r"\,") +
                     r"; \ Kripke models: \ " + f"{d['k_var_models']}" + r" \ (" + f"{d['k_const_models']}" +
                     r" with constant domains); \ translation checked on " + f"{d['translation_checks']:,}".replace(
            ",", r"\,") + r" cases, \ all agree", font_size=17, color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "One model shows that principles can fail. To see which fail in general, the Reasoner checks every model "
            "up to a size. <bookmark mark='a'/>For counterpart theory: three worlds, up to two individuals in one of "
            "them, every counterpart relation and every extension of a predicate: nearly seventeen thousand models, "
            "each principle evaluated at every world. For Kripke's semantics: every two-world model over two "
            "individuals, with the same domain at both worlds or different ones. <bookmark mark='b'/>With constant "
            "domains, Kripke's semantics validates everything here. With varying domains, the Barcan formula fails, "
            "so does its converse, and so does the claim that everything necessarily exists. <bookmark mark='c'/>"
            "Counterpart theory gives a different logic. The necessity of identity and of distinctness fail; so do "
            "the four and B axioms, because the counterpart relation need not be transitive or symmetric; so does "
            "the Barcan formula. But T holds, since everything is its own counterpart; the converse Barcan formula "
            "holds; and, oddly, so does the claim that everything necessarily exists, because a thing with no "
            "counterpart in a world is simply not considered there. <bookmark mark='d'/>And along the way the "
            "Reasoner checked the translation against the direct semantics on fifteen hundred cases: they always "
            "agree."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(grid.cell[r][0]) for r in range(len(rows))], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(*[FadeIn(grid.cell[r][1]) for r in range(len(rows))])
            self.play(*[FadeIn(grid.cell[r][2]) for r in range(len(rows))])
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(grid.cell[r][3]) for r in range(len(rows))], lag_ratio=0.15),
                      run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def reply(self):
        q = quote_card(r"Probably, \ however, \ Humphrey could not care less whether someone else, \ no matter how "
                       r"much resembling him, \ would have been victorious in another possible world.",
                       r"Saul Kripke", r"\textit{Naming and Necessity} \ (1980), \ p. 45, \ n. 13", width=10.6,
                       font_size=23).to_edge(UP, buff=0.4)
        rows = stack([(r"Lewis: \ the property of possibly winning is Humphrey's own; \ he has it in virtue of a "
                       r"counterpart, \ as he has a reflection in virtue of a mirror", NAME),
                      (r"the counterpart relation is inconstant: \ context picks which similarities matter", CPT),
                      (r"so the statue and the lump can be one thing \ (Part 21): \ a statue-counterpart could not "
                       r"survive squashing; \ a lump-counterpart could", GOAL),
                      (r"and contingent identity, \ Gibbard's Lumpl and Goliath, \ is no paradox", OK)],
                     font_size=21, aligned_edge=LEFT, width=12.2, buff=0.3).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "Kripke's objection is famous. <bookmark mark='a'/>When we say Humphrey might have won, we are talking "
            "about Humphrey. On Lewis's view we seem to be talking about someone else, however much he resembles "
            "Humphrey, and Humphrey could not care less whether someone else would have been victorious in another "
            "world. <bookmark mark='b'/>Lewis replied that the modal property is Humphrey's own. Humphrey himself "
            "has the property of possibly winning; he has it in virtue of his counterpart, as you have the property "
            "of being reflected in virtue of a mirror. <bookmark mark='c'/>And the counterpart relation is "
            "inconstant: context selects which similarities count. <bookmark mark='d'/>That pays off in Part 21's "
            "puzzle. The statue and the lump can be one object. Under the statue counterpart relation, which weighs "
            "shape, it could not survive squashing; under the lump counterpart relation, which weighs matter, it "
            "could. <bookmark mark='e'/>Allan Gibbard's contingent identity of Lumpl and Goliath stops being a "
            "paradox. Counterpart theory pays for that with the necessity of identity."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(q))
            for mk, r in zip("bcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
