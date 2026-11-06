from __future__ import annotations

from videos.philosophy.philosophy20.common import *  # noqa: F403


class Mereology(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"Mereology, axiom by axiom", r"What is the logic of parts and wholes?",
                            lit=(1916, 1987), part=PART)
        with self.voiceover("Chapter six. Mereology, axiom by axiom."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.axioms()
        self.failures()
        self.census()
        self.boolean()

    def axioms(self):
        head = label(r"Classical extensional mereology", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ax = [
            (r"P1 \ reflexive", r"x \le x", PARTC),
            (r"P2 \ antisymmetric", r"x \le y \land y \le x \to x = y", PARTC),
            (r"P3 \ transitive", r"x \le y \land y \le z \to x \le z", PARTC),
            (r"overlap", r"O(x, y) \;:=\; \exists z \,(z \le x \land z \le y)", GREY_A),
            (r"weak supplementation", r"x < y \to \exists z \,(z \le y \land \lnot O(z, x))", WHOLE),
            (r"strong supplementation", r"y \not\le x \to \exists z \,(z \le y \land \lnot O(z, x))", WHOLE),
            (r"unrestricted fusion", r"S \ne \varnothing \to \exists z \, \forall w \,(O(w, z) \leftrightarrow "
                                     r"\exists s \in S \; O(w, s))", UNIV),
        ]
        rows = VGroup()
        y = 2.0
        for name, f, col in ax:
            a = label(name, font_size=20, color=col)
            b = MathTex(f, font_size=28, color=WHITE)
            a.move_to([-6.2 + a.width / 2, y, 0])
            b.move_to([-1.6 + b.width / 2, y, 0])
            rows.add(VGroup(a, b))
            y -= 0.62
        note = label(r"$x \le y$: \ $x$ is part of $y$; \ \ $x < y$: \ proper part", font_size=18,
                     color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Mereology, the formal theory of parts and wholes, was founded by Stanisław Leśniewski in 1916, as a "
            "nominalist rival to set theory. <bookmark mark='a'/>Its classical form starts with parthood as a partial "
            "order: everything is part of itself; two things that are parts of each other are identical; a part of a "
            "part is a part. <bookmark mark='b'/>Two things overlap if they share a part. <bookmark mark='c'/>Weak "
            "supplementation: if x is a proper part of y, then y has some other part that does not overlap x. A whole "
            "cannot have just one proper part. <bookmark mark='d'/>Strong supplementation: if y is not part of x, "
            "then y has a part that does not overlap x. <bookmark mark='e'/>And unrestricted fusion: any nonempty "
            "collection of things has a fusion, something that overlaps exactly what overlaps some member of the "
            "collection. These together make classical extensional mereology."
        ) as vo:
            self.play(FadeIn(head), FadeIn(note))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[:3]], lag_ratio=0.3))
            for mk, r in zip("bcde", rows[3:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def failures(self):
        d = load("counter")
        head = label(r"Two ways to fail", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        lonely = hasse(2, d["lonely"]["hasse"], names=[r"$a$", r"$x$"], center=[-3.8, 0.4, 0], width=1.0,
                       height=2.0)
        twin = hasse(4, d["twin"]["hasse"], names=[r"$a$", r"$b$", r"$x$", r"$y$"], center=[2.8, 0.4, 0],
                     width=2.4, height=2.0)
        t1 = label(r"a whole with one proper part", font_size=20, color=WHOLE).next_to(lonely, UP, buff=0.4)
        t2 = label(r"two wholes, \ the same two parts", font_size=20, color=WHOLE).next_to(twin, UP, buff=0.4)

        def verdict(p, at):
            rows = [(r"weak supplementation", p["wsp"]), (r"strong supplementation", p["ssp"]),
                    (r"extensionality", p["ext"])]
            g = VGroup(*[label(n + r": \ " + (r"holds" if v else r"fails"), font_size=18, color=OK if v else BAD)
                         for n, v in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            return g.move_to(at)

        v1 = verdict(d["lonely"], [-3.8, -2.2, 0])
        v2 = verdict(d["twin"], [2.8, -2.2, 0])
        with self.voiceover(
            "The Reasoner checks small models. <bookmark mark='a'/>On the left, a whole x with exactly one proper "
            "part, a. Weak supplementation fails: nothing in x is disjoint from a. Most people agree that nothing "
            "could be composed of a single smaller part. <bookmark mark='b'/>On the right, two wholes, x and y, each "
            "composed of the same two parts, a and b. Weak supplementation holds, but strong supplementation fails, "
            "and with it extensionality: x and y are distinct things with exactly the same parts. "
            "<bookmark mark='c'/>Is that possible? A statue and the clay it is made of seem to share all their parts. "
            "Classical mereology says they must be one thing. That is the puzzle of constitution, which returns in "
            "Part 21."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lonely), FadeIn(t1), FadeIn(v1))
            vo.wait_until("b")
            self.play(FadeIn(twin), FadeIn(t2), FadeIn(v2))
            vo.wait_until("c")
            self.play(Indicate(v2[2], color=BAD))
        self.clear_scene()

    def census(self):
        d = load("census")["rows"]
        head = label(r"Every small model, \ tested", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [r"n", r"\text{posets}", r"\text{weak supp.}", r"\text{strong supp.}", r"\text{fusion}",
              r"\text{all (CEM)}"]
        rows = []
        for r in d:
            rows.append([MathTex(str(r["n"]), font_size=26), MathTex(str(r["posets"]), font_size=26),
                         MathTex(str(r["wsp"]), font_size=26, color=WHOLE), MathTex(str(r["ssp"]), font_size=26,
                                                                                   color=WHOLE),
                         MathTex(str(r["uf"]), font_size=26, color=UNIV),
                         MathTex(str(r["cem"]), font_size=28, color=OK if r["cem"] else BAD)])
        grid = ValueGrid(hd, rows, col_w=[0.8, 1.5, 2.0, 2.2, 1.6, 1.9], cell_h=0.55, font_size=20).move_to(
            [-0.4, 0.4, 0])
        notes = stack([(r"posets counted up to isomorphism: \ 1, \ 2, \ 5, \ 16, \ 63, \ 318", GREY_A),
                       (r"only sizes 1 and 3 admit a model of CEM", GOAL)], font_size=20, width=12.0).to_edge(
            DOWN, buff=0.35)
        with self.voiceover(
            "Now the Reasoner tests every possible structure. <bookmark mark='a'/>It generates every partial order on "
            "up to six elements, up to isomorphism: one, two, five, sixteen, sixty-three and three hundred and "
            "eighteen of them, matching the known counts. <bookmark mark='b'/>For each it checks weak and strong "
            "supplementation and unrestricted fusion. Each axiom alone is satisfied by many orders. "
            "<bookmark mark='c'/>All of them together, by exactly two: one with a single element, and one with three. "
            "No model of classical mereology has two, four, five or six elements."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*grid.cell[i][:2])) for i in range(len(d))], lag_ratio=0.2),
                      FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*grid.cell[i][2:5])) for i in range(len(d))], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(grid.cell[i][5]) for i in range(len(d))], lag_ratio=0.2),
                      FadeIn(notes[1]))
            self.play(Create(grid.row_box(0, OK)), Create(grid.row_box(2, OK)))
        self.clear_scene()

    def boolean(self):
        d = load("boolean")
        head = label(r"The theorem: \ Boolean algebras without a bottom", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        import itertools
        subs = [frozenset(s) for r in range(1, 4) for s in itertools.combinations(range(3), r)]
        edges = [(i, j) for i, a in enumerate(subs) for j, b in enumerate(subs) if a < b and len(b) == len(a) + 1]
        nm = [r"$" + "".join("abc"[x] for x in sorted(s)) + r"$" for s in subs]
        h = hasse(len(subs), edges, names=nm, center=[-3.4, -0.4, 0], width=4.0, height=3.2)
        rows = stack([(r"$k$ atoms: \ every nonempty set of them has exactly one fusion", WHITE),
                      (r"sizes $2^k - 1$: \ " + ", \\ ".join(str(d[k]["size"]) for k in sorted(d)), GOAL),
                      (r"each checked: \ both supplementations and fusion hold", OK),
                      (r"Tarski \ (1935): \ CEM is the theory of complete Boolean algebras with zero removed", UNIV),
                      (r"so the parts fix the whole: \ given the atoms, \ the sums are settled", WHOLE)],
                     font_size=20, aligned_edge=LEFT, width=6.6).move_to([3.4, -0.4, 0])
        with self.voiceover(
            "Why one and three? <bookmark mark='a'/>Take k atoms. In classical mereology every nonempty collection of "
            "them has exactly one fusion, and there is nothing else. <bookmark mark='b'/>So a model with k atoms has "
            "two to the k, minus one, elements: one, three, seven, fifteen. Here are the seven of three atoms, ordered "
            "by parthood. <bookmark mark='c'/>The Reasoner checks each: both supplementation principles and fusion "
            "hold. <bookmark mark='d'/>Alfred Tarski showed the general result: classical extensional mereology is "
            "the theory of complete Boolean algebras with the zero removed. <bookmark mark='e'/>The atoms fix "
            "everything. Given the simples, the sums come for free, which is exactly what the next chapter "
            "questions."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(h.dots[:3]), FadeIn(h.names[:3]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(h.lines), FadeIn(h.dots[3:]), FadeIn(h.names[3:]), FadeIn(rows[1]), run_time=2)
            for mk, r in zip("cde", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
