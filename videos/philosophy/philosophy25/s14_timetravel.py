from __future__ import annotations

from videos.philosophy.philosophy25.common import *  # noqa: F403


class TimeTravel(VoiceoverScene):
    def construct(self):
        card = chapter_card(13, r"Time travel", r"Could you prevent your own birth?", lit=(1949, 1991), part=PART)
        with self.voiceover("Chapter thirteen. Time travel."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.godel()
        self.lewis()
        self.deutsch()
        self.verdict()

    def godel(self):
        hc = history_card(1949, r"Kurt Gödel", r"a rotating universe with closed timelike curves", width=6.0,
                          color=HIST).to_corner(UL, buff=0.3)
        c = np.array([-2.6, -0.8, 0])
        loop = Ellipse(width=4.4, height=2.6, color=TIME, stroke_width=4).move_to(c)
        tip = Arrow(c + np.array([0.0, 1.3, 0]), c + np.array([0.6, 1.26, 0]), buff=0, color=TIME,
                    max_tip_length_to_length_ratio=0.6)
        cones = VGroup()
        for a in np.linspace(0, 2 * PI, 9)[:-1]:
            p = c + np.array([2.2 * math.cos(a), 1.3 * math.sin(a), 0])
            tdir = np.array([-2.2 * math.sin(a), 1.3 * math.cos(a), 0])
            tdir = tdir / np.linalg.norm(tdir)
            nrm = np.array([-tdir[1], tdir[0], 0])
            tri = Polygon(p, p + 0.45 * tdir + 0.25 * nrm, p + 0.45 * tdir - 0.25 * nrm, color=LIGHT,
                          fill_opacity=0.25, stroke_width=1.5)
            cones.add(tri)
        rows = stack([(r"Gödel \ (1949): \ a solution of Einstein's equations for a rotating universe", WHITE),
                      (r"its light cones tip over as you go round: \ a path always heading into its own future \ "
                       r"comes back to its start", LIGHT),
                      (r"a closed timelike curve: \ a possible traveller meets their own past", TIME),
                      (r"Gödel's moral: \ if this is possible, \ time's passage is not objective", ABS)],
                     font_size=20, aligned_edge=LEFT, width=5.6, buff=0.28).move_to([3.6, -0.5, 0])
        with self.voiceover(
            "In 1949 Kurt Gödel, Einstein's friend at Princeton, gave him a birthday present: a solution of the "
            "field equations describing a rotating universe. <bookmark mark='a'/>In it, the light cones tip over "
            "as you travel around, so that a path that always heads into its own local future <bookmark mark='b'/>"
            "can come back to the very event where it started. <bookmark mark='c'/>This is a closed timelike curve: "
            "a traveller along it meets their own past. <bookmark mark='d'/>Gödel drew a philosophical moral: if "
            "such a world is possible, the passage of time cannot be an objective feature of reality."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Create(loop), FadeIn(cones), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(GrowArrow(tip))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Indicate(loop, color=TIME))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def lewis(self):
        hc = history_card(1976, r"David Lewis", r"`The Paradoxes of Time Travel'", width=5.4,
                          color=HIST).to_corner(UL, buff=0.3)
        rows = [
            (r"the grandfather", r"Tim travels back to kill his grandfather before his father is born: \ can he?",
             BAD),
            (r"Lewis: \ yes", r"relative to the local facts \ (a gun, \ a clear shot, \ training), \ he can", OK),
            (r"Lewis: \ no", r"relative to all the facts, \ including that grandfather lived, \ he cannot", BAD),
            (r"so", r"`can' is relative to a set of facts; \ there is no contradiction, \ only a story in which Tim "
                    r"fails", ABS),
            (r"what is ruled out", r"not time travel, \ but changing the past: \ the past happened once, \ with Tim "
                                   r"in it", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.45, width=8.6, x_text=-2.4, label_size=22, text_size=21)
        with self.voiceover(
            "In 1976 David Lewis took on the paradoxes. <bookmark mark='a'/>Tim builds a time machine, travels back, "
            "and sets out to kill his grandfather before his father is born. Can he? <bookmark mark='b'/>Lewis: in "
            "one sense, yes. Relative to the local facts, a gun, a clear shot, years of training, Tim can kill him. "
            "<bookmark mark='c'/>In another sense, no. Relative to all the facts, including that grandfather lived to "
            "have children, Tim cannot. <bookmark mark='d'/>Can is relative to a set of facts, and there is no "
            "contradiction: the story must be one in which Tim fails, perhaps by slipping on a banana peel. "
            "<bookmark mark='e'/>What is ruled out is not time travel but changing the past. The past happened "
            "once, and Tim was already in it."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def deutsch(self):
        d = load("ctc")
        head = label(r"Deutsch's fixed points, \ computed", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        f = MathTex(r"\rho_{\text{CTC}} = \operatorname{Tr}_{\text{CR}}\!\big[\,U (\rho_{\text{in}} \otimes "
                    r"\rho_{\text{CTC}})\, U^\dagger\,\big]", font_size=32, color=ABS).next_to(head, DOWN, buff=0.3)
        T = lambda s, c=WHITE: label(s, font_size=20, color=c)  # noqa: E731
        gf, kn = d["grandfather"], d["knowledge"]

        def cls(v):
            return T(r"none" if not v else ", ".join(map(str, v)), BAD if not v else OK)

        def dm(m):
            return MathTex(rf"\begin{{pmatrix}} {m[0][0]:.1f} & {m[0][1]:.1f} \\ {m[1][0]:.1f} & {m[1][1]:.1f} "
                           r"\end{pmatrix}", font_size=24, color=OK)

        hd = [T(r"circuit", CONN), T(r"classical consistent histories", CONN), T(r"Deutsch's solution", CONN)]
        rows = [[T(r"grandfather: \ the bit comes back flipped"), cls(gf["classical_consistent"]),
                 dm(gf["deutsch"])],
                [T(r"knowledge: \ the bit is copied, \ then sent back"), cls(kn["classical_consistent"]),
                 dm(kn["deutsch"])]]
        grid = ValueGrid(hd, rows, col_w=[4.8, 3.6, 3.0], cell_h=1.0, font_size=20).move_to([0, -0.4, 0])
        side = stack([(r"grandfather: \ no classical history; \ Deutsch: \ the bit is 0 or 1 with probability "
                       r"$\tfrac12$ each", LIGHT),
                      (r"knowledge: \ every history is consistent, \ and nothing chooses; \ Deutsch picks the most "
                       r"mixed", ABS)], font_size=20, aligned_edge=LEFT, width=11.4, buff=0.25).to_edge(DOWN,
                                                                                                buff=0.35)
        with self.voiceover(
            "In 1991 David Deutsch made time travel a problem in quantum computing. <bookmark mark='a'/>A bit, or "
            "qubit, travels along a closed timelike curve, interacting on the way with ordinary bits. Consistency "
            "demands that the state that comes out of the curve is the state that went in: a fixed point of this "
            "map. <bookmark mark='b'/>The grandfather paradox as a circuit: the bit comes back flipped. Classically "
            "there is no consistent history at all: no bit equals its own negation. <bookmark mark='c'/>But "
            "Deutsch's equation has a solution, which the Reasoner computes: the bit is zero or one with probability "
            "a half each, a mixture, and the paradox dissolves into a coin toss. <bookmark mark='d'/>The knowledge "
            "paradox, the unproven theorem that a traveller brings back from the future: the bit is copied and sent "
            "back. Now every history is consistent, and nothing decides which. Deutsch's rule picks the most mixed "
            "state, again a half each."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("b")
            self.play(FadeIn(grid.cell[0][0]), FadeIn(grid.cell[0][1]))
            vo.wait_until("c")
            self.play(FadeIn(grid.cell[0][2]), FadeIn(side[0]))
            vo.wait_until("d")
            self.play(*[FadeIn(c) for c in grid.cell[1]], FadeIn(side[1]))
        self.clear_scene()

    def verdict(self):
        head = label(r"Could it happen?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Novikov", r"the self-consistency principle: \ only consistent histories occur", TIME),
            (r"Hawking \ (1992)", r"chronology protection: \ perhaps quantum effects always destroy a time machine "
                                  r"before it forms", BAD),
            (r"the physics", r"wormholes need exotic, \ negative-energy matter; \ none is known in bulk", MATTER),
            (r"the philosophy", r"time travel is consistent, \ as Lewis showed; \ whether it is physically possible "
                                r"is open", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.6, x_text=-2.4, label_size=22, text_size=21)
        with self.voiceover(
            "Could it really happen? <bookmark mark='a'/>Igor Novikov's self-consistency principle says only "
            "consistent histories occur, which is Lewis's conclusion as a law of physics. <bookmark mark='b'/>"
            "Stephen Hawking conjectured in 1992 that the laws protect chronology: quantum effects might always "
            "destroy a time machine before it could form. <bookmark mark='c'/>Traversable wormholes would need "
            "matter with negative energy in bulk, which no one has. <bookmark mark='d'/>So the verdict is split. "
            "Time travel is logically consistent, as Lewis showed. Whether our laws allow it is an open question in "
            "physics."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
