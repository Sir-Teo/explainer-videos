from __future__ import annotations

from videos.philosophy.philosophy6.common import *  # noqa: F403
from videos.philosophy.philosophy6.s09_cone import cone, APEX


class CH(VoiceoverScene):
    def construct(self):
        card = chapter_card(15, r"The continuum hypothesis", r"How many real numbers are there?", lit=(1938, 1963),
                            part=PART)
        with self.voiceover("Chapter fifteen. The continuum hypothesis."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.hilbert()
        self.godel_L()
        self.forcing()
        self.brick()

    def hilbert(self):
        hc = history_card(1900, r"David Hilbert, \ Paris", r"23 problems for the new century: \ the first is Cantor's "
                          r"continuum problem", width=7.0, color=HIST).to_corner(UL, buff=0.35)
        q = VGroup(MathTex(r"2^{\aleph_0} \overset{?}{=} \aleph_1", font_size=60, color=GOAL),
                   label(r"is every infinite set of real numbers either countable, \ or as large as $\mathbb{R}$?",
                         font_size=26)).arrange(DOWN, buff=0.4).move_to([0, -0.4, 0])
        with self.voiceover(
            "In 1900 David Hilbert addressed the International Congress of Mathematicians in Paris with a list of "
            "twenty-three problems for the coming century. <bookmark mark='a'/>The first was Cantor's continuum "
            "problem. Is two to the aleph zero equal to aleph one? Equivalently: is every infinite set of real "
            "numbers either countable, or as large as the whole line?"
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(q[0]), FadeIn(q[1]))
        self.clear_scene()

    def godel_L(self):
        V = cone(color=SETC, opacity=0.06)
        L = cone(color=ORD, halfw=1.5, opacity=0.18)
        vl = MathTex(r"V", font_size=48, color=SETC).move_to(APEX + np.array([-3.3, 5.5, 0]))
        ll = MathTex(r"L", font_size=48, color=ORD).move_to(APEX + np.array([0, 5.3, 0]))
        defs = VGroup(MathTex(r"V_{\alpha+1} = \mathcal{P}(V_\alpha)", font_size=32, color=SETC),
                      MathTex(r"L_{\alpha+1} = \text{the \textit{definable} subsets of } L_\alpha", font_size=32,
                              color=ORD),
                      label(r"$L$: \ only the sets you are forced to have", font_size=24, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, 1.2, 0])
        res = VGroup(history_card(1938, r"Kurt Gödel", r"in $L$, \ choice and the continuum hypothesis are true",
                                  width=5.6, color=HIST),
                     label(r"so if ZF is consistent, \ so is ZFC + CH", font_size=26, color=OK)).arrange(
            DOWN, buff=0.3).move_to([3.4, -1.6, 0])
        with self.voiceover(
            "The first half of the answer came from Gödel in 1938. <bookmark mark='a'/>Inside the full universe V "
            "he built a thinner one, L, the constructible universe. Where V takes every subset at each stage, L "
            "takes only the subsets that can be defined from what is already there. <bookmark mark='b'/>L satisfies "
            "all the axioms of ZF, and in L both the axiom of choice and the continuum hypothesis are true. "
            "<bookmark mark='c'/>So if the axioms are consistent, they remain consistent with the continuum "
            "hypothesis added. They cannot refute it."
        ) as vo:
            self.play(Create(V), FadeIn(vl), Create(L), FadeIn(ll), FadeIn(defs))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(res[0]))
            vo.wait_until("c")
            self.play(FadeIn(res[1]))
        self.clear_scene()

    def forcing(self):
        d = load("forcing")
        hc = history_card(1963, r"Paul Cohen", r"forcing: \ add new real numbers to a model", width=5.6,
                          color=HIST).to_corner(UL, buff=0.3)
        depth = 5
        nodes = {(): np.array([-3.2, 2.0, 0])}
        tree = VGroup()
        for k in range(1, depth + 1):
            for bits in __import__("itertools").product((0, 1), repeat=k):
                parent = nodes[bits[:-1]]
                dx = 3.0 / 2 ** (k - 1)
                p = parent + np.array([-dx / 2 if bits[-1] == 0 else dx / 2, -0.95, 0])
                nodes[bits] = p
                tree.add(Line(parent, p, color=GREY_D, stroke_width=1.8))
        dots = VGroup(*[Dot(p, radius=0.05, color=GREY_B) for p in nodes.values()])
        g = tuple(d["generic"][:depth])
        path = VMobject(stroke_color=GOAL, stroke_width=5).set_points_as_corners([nodes[g[:k]] for k in range(depth + 1)])
        cl = label(r"conditions: \ finite approximations to a new real", font_size=22, color=GREY_A).next_to(
            tree, DOWN, buff=0.25)
        ground = VGroup(*[MathTex("".join(map(str, r)) + r"\dots", font_size=26, color=GREY_B) for r in d["ground"]]
                        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.0, 0.9, 0])
        gl = label(r"the reals already in the model", font_size=22, color=GREY_A).next_to(ground, UP, buff=0.2)
        gen = MathTex(r"g = " + "".join(map(str, d["generic"])) + r"\dots", font_size=32, color=GOAL).next_to(
            ground, DOWN, buff=0.5)
        dense = label(r"dense: \ `differs from $r_k$ somewhere' \ can always be reached", font_size=22).next_to(
            gen, DOWN, buff=0.3)
        res = label(r"$g$ meets every dense set, \ so it is new: \ add $\aleph_2$ of them and CH fails", font_size=24,
                    color=OK).to_edge(DOWN, buff=0.35)
        assert d["differs"]
        with self.voiceover(
            "The second half took twenty-five more years. <bookmark mark='a'/>In 1963 Paul Cohen invented forcing, "
            "a way to enlarge a model of set theory by adding new sets. Here is the idea for a new real number. Its "
            "binary digits are built up by finite approximations, called conditions: a tree of ever longer "
            "strings. <bookmark mark='b'/>The model already contains some reals. For each one, the set of "
            "conditions that disagree with it somewhere is dense: any condition can be extended into it. "
            "<bookmark mark='c'/>A generic path is one that enters every such dense set. So it disagrees with every "
            "real in the model: it is new. <bookmark mark='d'/>Cohen added aleph two such reals at once, and showed "
            "the axioms still hold in the enlarged model. In it, the continuum hypothesis is false. He received the "
            "Fields Medal in 1966."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Create(tree), FadeIn(dots), FadeIn(cl), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(gl), FadeIn(ground), FadeIn(dense))
            vo.wait_until("c")
            self.play(Create(path), FadeIn(gen), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(res))
        self.clear_scene()

    def brick(self):
        w = wall(upto=6, current=6).scale(0.42).move_to([-3.65, -0.2, 0])
        wc = wall_card(6, width=6.4, font_size=22).move_to([3.3, -0.2, 0])
        q = label(r"Scott and Solovay: \ forcing as a model with truth values in a Boolean algebra \ (Part 5's many "
                  r"values, again)", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "This is the sixth brick in the Wall. <bookmark mark='a'/>The dream was that every collection is a set, "
            "and every question about sets has an answer. The wall: Russell's paradox kills the first half, and "
            "Gödel and Cohen together kill the second. The continuum hypothesis can be neither proved nor refuted "
            "from the axioms. What it forces is that axioms are chosen, not simply read off. "
            "<bookmark mark='b'/>A footnote that links to Part 5: Dana Scott and Robert Solovay recast forcing as a "
            "model whose truth values lie in a Boolean algebra, a many-valued logic of exactly the kind we built."
        ) as vo:
            self.play(FadeIn(w))
            vo.wait_until("a")
            self.play(FadeIn(wc))
            vo.wait_until("b")
            self.play(FadeIn(q))
        self.clear_scene()
