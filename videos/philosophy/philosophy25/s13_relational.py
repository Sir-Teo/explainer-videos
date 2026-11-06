from __future__ import annotations

from videos.philosophy.philosophy25.common import *  # noqa: F403


class Relational(VoiceoverScene):
    def construct(self):
        card = chapter_card(12, r"Relationalism rebuilt", r"Can physics be done with relations alone?",
                            lit=(1999,), part=PART)
        with self.voiceover("Chapter twelve. Relationalism rebuilt."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.problem()
        self.matching()
        self.dragging()
        self.machian()

    def problem(self):
        head = label(r"Leibniz's unpaid debt", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"the debt", r"explain inertia and the bucket using only relations between bodies", BAD),
            (r"the snapshots", r"a history is a sequence of configurations: \ shapes, \ with no place or "
                               r"orientation", SPACE),
            (r"the question", r"comparing two snapshots, \ what changed? \ which body went where?", LIGHT),
            (r"Barbour and Bertotti \ (1982)", r"slide and turn one over the other until they fit best: \ what "
                                               r"remains is the real change", OK),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.4, x_text=-2.2, label_size=22, text_size=21)
        with self.voiceover(
            "Leibniz left a debt: explain inertia, and the bucket, using only relations between bodies. "
            "<bookmark mark='a'/>For a long time no one paid it. <bookmark mark='b'/>Julian Barbour's approach "
            "starts from snapshots. A history is a sequence of configurations of bodies, shapes only, with no "
            "position or orientation in any absolute space. <bookmark mark='c'/>The question is how to compare two "
            "snapshots: what changed, and which body went where? <bookmark mark='d'/>Barbour and Bruno Bertotti's "
            "answer in 1982 was best matching: slide and turn one snapshot over the other until they fit as well as "
            "possible. Whatever difference remains is the real change."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def matching(self):
        d = load("match")
        head = label(r"Best matching, \ built", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        sc, c = 0.9, np.array([-2.6, -0.4, 0])
        P = [c + sc * np.array([x, y, 0]) for x, y in d["P"]]
        Q = [c + sc * np.array([x, y, 0]) for x, y in d["Q"]]
        M = [c + sc * np.array([x, y, 0]) for x, y in d["matched"]]

        def shape(pts, col):
            n = len(pts)
            g = VGroup(*[Line(pts[i], pts[j], color=col, stroke_width=1.5, stroke_opacity=0.6)
                         for i in range(n) for j in range(i + 1, n)])
            g.add(*[Dot(p, radius=0.09, color=col) for p in pts])
            return g

        sP = shape(P, SPACE)
        sQ = shape(Q, MATTER)
        sM = shape(M, MATTER)
        side = stack([(r"blue: \ one instant; \ orange: \ the next, \ as recorded", WHITE),
                      (rf"raw difference: \ {d['raw_distance']:.2f}", BAD),
                      (r"best matching: \ the shift and rotation that minimize the difference \ (Kabsch's "
                       r"algorithm)", ABS),
                      (rf"what remains: \ {d['intrinsic_distance']:.2f}: \ the intrinsic change", OK),
                      (rf"the rotation found, \ {d['angle_found']:.2f} rad, \ was arbitrary: \ it is not physics",
                       GOAL)], font_size=20, aligned_edge=LEFT, width=5.2, buff=0.28).move_to([3.9, -0.3, 0])
        assert d["intrinsic_distance"] < 0.2 * d["raw_distance"]
        with self.voiceover(
            "Here it is built. <bookmark mark='a'/>Five bodies at one instant, in blue, and at the next, in orange, "
            "as some arbitrary observer recorded them, shifted and turned. <bookmark mark='b'/>Measured naively, "
            "point by point, the two differ a great deal. <bookmark mark='c'/>Now best-match them: find the shift "
            "and rotation of the orange configuration that bring it as close as possible to the blue, using an "
            "algorithm from crystallography, Wolfgang Kabsch's. <bookmark mark='d'/>What remains is small: the "
            "intrinsic change in the shape, the only change a relationalist recognizes. <bookmark mark='e'/>The "
            "shift and the rotation it found were artefacts of the recording, not physics. Barbour showed that "
            "dynamics built from best-matched intrinsic changes reproduces Newtonian physics for a universe with no "
            "total angular momentum, and that a version of it reproduces general relativity."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sP))
            vo.wait_until("a")
            self.play(FadeIn(sQ), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Transform(sQ, sM), FadeIn(side[2]), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def dragging(self):
        head = label(r"Is general relativity Machian?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        earth = Circle(radius=0.9, color=SPACE, fill_color=SPACE, fill_opacity=0.3).move_to([-3.6, -0.6, 0])
        spin = Arc(radius=1.2, start_angle=PI / 6, angle=4 * PI / 3, color=SPACE, stroke_width=3).move_to(
            earth.get_center()).add_tip(tip_length=0.18)
        orbit = Circle(radius=2.0, color=GREY_C, stroke_width=1.5).move_to(earth)
        gyro = Dot(earth.get_center() + UP * 2.0, radius=0.12, color=MATTER)
        rows = [
            (r"Lense--Thirring \ (1918)", r"a spinning mass drags the inertial frames around it", SPACE),
            (r"Gravity Probe B \ (2011)", r"gyroscopes in polar orbit: \ frame dragging of 37 $\pm$ 7 "
                                          r"milliarcseconds a year, \ against 39 predicted", OK),
            (r"so", r"distant matter does shape local inertia, \ a little", MATTER),
            (r"but", r"empty Minkowski spacetime has inertia with no matter at all; \ Gödel's universe rotates "
                     r"relative to its matter", BAD),
        ]
        g = rows_table(rows, x_label=-1.0, x_text=1.8, top=1.5, gap=0.45, width=5.0, label_size=20, text_size=19)
        with self.voiceover(
            "How Machian is general relativity? <bookmark mark='a'/>In 1918 Josef Lense and Hans Thirring showed that "
            "a spinning mass drags the inertial frames near it around with it. <bookmark mark='b'/>In 2011 Gravity "
            "Probe B, four gyroscopes in polar orbit around the Earth, measured the effect: a drift of thirty-seven "
            "milliarcseconds a year, give or take seven, against thirty-nine predicted. <bookmark mark='c'/>So matter "
            "does shape local inertia, as Mach hoped, a little. <bookmark mark='d'/>But the theory also has empty "
            "spacetimes with perfectly good inertia and no matter at all, and Gödel's universe, whose matter rotates "
            "relative to the local compass of inertia. General relativity is not Mach's principle; Barbour's "
            "best-matching version of it builds the principle in."
        ) as vo:
            self.play(FadeIn(head), FadeIn(earth), Create(orbit), FadeIn(gyro))
            vo.wait_until("a")
            self.play(Create(spin), FadeIn(g[0]))
            vo.wait_until("b")
            self.play(Rotate(gyro, angle=PI / 2, about_point=earth.get_center()), FadeIn(g[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(g[2]))
            vo.wait_until("d")
            self.play(FadeIn(g[3]))
        self.clear_scene()

    def machian(self):
        head = label(r"What relationalism buys, \ and costs", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"the bucket", r"in a universe with no total rotation, \ the water's curvature tracks rotation relative "
                            r"to everything else: \ Mach, \ made precise", OK),
            (r"the cost", r"a universe with net rotation is ruled out by fiat; \ Newton allows it", BAD),
            (r"time", r"Barbour, \ \textit{The End of Time} \ (1999): \ even time is a relation among "
                      r"configurations", TIME),
            (r"the debate today", r"sophisticated substantivalists and relationalists may differ only in words: \ "
                                  r"Belot; \ Pooley and Brown", ABS),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.6, x_text=-2.4, label_size=22, text_size=21)
        with self.voiceover(
            "What does it buy? <bookmark mark='a'/>The bucket. In a universe with no total rotation, best matching "
            "makes the water's curvature track its rotation relative to all the other matter: Mach's principle, "
            "made precise. <bookmark mark='b'/>The cost: a whole universe in net rotation is ruled out by fiat, "
            "where Newton allows it, and we cannot check which is right. <bookmark mark='c'/>Barbour went further in "
            "The End of Time, in 1999, arguing that time itself is nothing but the ordering of configurations. "
            "<bookmark mark='d'/>And many now suspect that sophisticated substantivalism and relationalism differ "
            "less than they seem: both say that what is physically real is the pattern of relations, not which "
            "point has which field."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
