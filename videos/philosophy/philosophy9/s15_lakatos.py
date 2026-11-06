from __future__ import annotations

from videos.philosophy.philosophy9.common import *  # noqa: F403

OCTA_PTS = {0: (0, 1, 0), 1: (0, -1, 0), 2: (1, 0, 0), 3: (-1, 0, 0), 4: (0, 0, 1), 5: (0, 0, -1)}


class Lakatos(VoiceoverScene):
    def construct(self):
        card = chapter_card(14, r"Proofs and refutations", r"How does mathematics actually grow?", lit=(1976,),
                            part=PART)
        with self.voiceover("Chapter fourteen. Proofs and refutations."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.euler()
        self.monsters()
        self.responses()

    def solids(self, names, scale=1.3):
        pts = {"tetrahedron": TETRA_PTS, "cube": CUBE_PTS, "octahedron": OCTA_PTS, "twin tetrahedra": TWIN_PTS,
               "picture frame": frame_pts()}
        out = VGroup()
        for n in names:
            s = 0.55 if n == "picture frame" else scale
            out.add(wire(pts[n], M.POLYHEDRA[n], scale=s, fill=ABSTRACT))
        return out

    def euler(self):
        d = load("euler")["rows"]
        hc = history_card(1750, r"Leonhard Euler", r"letter to Goldbach", width=4.0, color=HIST).to_corner(UL, buff=0.35)
        eq = MathTex(r"V - E + F = 2", font_size=52, color=NUM).move_to([1.6, 2.6, 0])
        names = ["tetrahedron", "cube", "octahedron"]
        shapes = self.solids(names).arrange(RIGHT, buff=1.4).move_to([0, 0.6, 0])
        caps = VGroup()
        for n, s in zip(names, shapes):
            r = d[n]
            caps.add(VGroup(label(n, font_size=22, color=WHITE),
                            MathTex(rf"{r['V']} - {r['E']} + {r['F']} = {r['chi']}", font_size=30,
                                    color=OK)).arrange(DOWN, buff=0.12).next_to(s, DOWN, buff=0.35))
        cauchy = VGroup(label(r"Cauchy's proof (1813): \ remove one face, \ stretch the rest flat on the table,",
                              font_size=22, color=GREY_A),
                        label(r"triangulate, \ then remove triangles one by one: \ $V - E + F$ never changes, \ and "
                              r"ends at 1", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Imre Lakatos looked at mathematics as it is actually done, and his favourite example came from "
            "Euler. <bookmark mark='a'/>In 1750 Euler noticed that for a polyhedron, the number of vertices, minus "
            "the number of edges, plus the number of faces, is two. <bookmark mark='b'/>The Reasoner counts. A "
            "tetrahedron: four minus six plus four is two. A cube: eight minus twelve plus six is two. An octahedron: "
            "six minus twelve plus eight is two. <bookmark mark='c'/>In 1813 Cauchy gave a proof. Remove one face, "
            "and stretch the rest flat on the table. Divide the faces into triangles, then remove triangles one at a "
            "time. The count never changes, and at the end a single triangle gives one. Add back the missing face, "
            "and the answer is two."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(eq))
            vo.wait_until("b")
            for s, c in zip(shapes, caps):
                self.play(Create(s), FadeIn(c), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(cauchy))
        self.clear_scene()

    def monsters(self):
        d = load("euler")
        head = label(r"The counterexamples", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        names = ["picture frame", "twin tetrahedra"]
        shapes = self.solids(names, scale=1.2)
        urchin = VGroup(Star(5, outer_radius=1.0, inner_radius=0.38, color=BAD, stroke_width=3, fill_color=BAD,
                             fill_opacity=0.12),
                        RegularPolygon(5, radius=1.0, color=GREY_D, stroke_width=1.5))
        allshapes = VGroup(*shapes, urchin).arrange(RIGHT, buff=1.6).move_to([0, 0.7, 0])
        rows = [d["rows"]["picture frame"], d["rows"]["twin tetrahedra"], d["urchin"]]
        titles = [r"a picture frame", r"two tetrahedra, \ touching at a point", r"Kepler's urchin \ (faces are "
                  r"pentagrams)"]
        caps = VGroup()
        for s, r, t in zip(allshapes, rows, titles):
            caps.add(VGroup(label(t, font_size=21, color=WHITE),
                            MathTex(rf"{r['V']} - {r['E']} + {r['F']} = {r['chi']}", font_size=30,
                                    color=BAD)).arrange(DOWN, buff=0.12).next_to(s, DOWN, buff=0.35))
        assert [r["chi"] for r in rows] == [0, 3, -6]
        hc = label(r"Lakatos, \textit{Proofs and Refutations} \ (1976; \ from his thesis of 1961): \ a classroom "
                   r"argues it out", font_size=22, color=HIST).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Then the counterexamples arrived, and Lakatos's book Proofs and Refutations, published in 1976 after his "
            "death, stages the history as an argument in a classroom. <bookmark mark='a'/>A picture frame: a square "
            "ring with a hole through it. The Reasoner counts sixteen vertices, thirty-two edges and sixteen faces: "
            "the answer is zero. <bookmark mark='b'/>Two tetrahedra touching at a single vertex: seven, twelve, "
            "eight, so three. <bookmark mark='c'/>And Kepler's small stellated dodecahedron, the urchin, if its faces "
            "are read as twelve star pentagons: twelve vertices, thirty edges, twelve faces, so minus six. Euler's "
            "theorem was proved, and false."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hc))
            for mk, s, c in zip("abc", allshapes, caps):
                vo.wait_until(mk)
                self.play(Create(s), FadeIn(c), run_time=1.5)
        self.clear_scene()

    def responses(self):
        head = label(r"What to do with a counterexample", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        rows = rows_at([
            (r"monster-barring", r"`a picture frame is not a polyhedron': \ redefine the word"),
            (r"exception-barring", r"`the theorem holds for convex polyhedra': \ retreat to safety"),
            (r"lemma-incorporation", r"the proof's hidden lemma: \ `the rest can be stretched flat'"),
        ], x_left=-6.3, x_right=-2.0, y0=1.7, dy=0.8, font_size=25, left_color=GOAL)
        eq = MathTex(r"V - E + F = 2 - 2g", font_size=44, color=NUM).move_to([0, -0.6, 0])
        gl = label(r"for a surface with $g$ holes: \ the frame has one hole, \ so $0$; \ the Euler characteristic, \ "
                   r"and topology begins", font_size=22, color=OK).next_to(eq, DOWN, buff=0.25)
        moral = label(r"Lakatos: \ mathematics grows by conjecture, \ proof and refutation, \ like Popper's science "
                      r"\ (Part 15)", font_size=24, color=GOAL).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Lakatos's characters try three responses. <bookmark mark='a'/>Monster-barring: a picture frame is not "
            "really a polyhedron, so redefine the word. <bookmark mark='b'/>Exception-barring: retreat to the convex "
            "polyhedra, where the theorem is safe. <bookmark mark='c'/>And the response Lakatos favoured, lemma "
            "incorporation: find the hidden assumption in the proof. Cauchy's proof assumed that, after removing a "
            "face, the rest can be stretched flat. That fails for the frame. Make the assumption a condition of the "
            "theorem, and the counterexample becomes a new theorem. <bookmark mark='d'/>For a surface with g holes, "
            "the count is two minus two g: the frame, with one hole, gives zero. This is the Euler characteristic, "
            "and with it topology begins. <bookmark mark='e'/>Mathematics, for Lakatos, grows the way Karl Popper "
            "said science grows: by conjectures, proofs and refutations, not by piling up certainties."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            vo.wait_until("d")
            self.play(Write(eq), FadeIn(gl))
            vo.wait_until("e")
            self.play(FadeIn(moral))
        self.clear_scene()
