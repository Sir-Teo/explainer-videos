from __future__ import annotations

from videos.philosophy.philosophy25.common import *  # noqa: F403


class Structures(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"Spacetime structures", r"How much structure do the laws need?", lit=(1687, 1989),
                            part=PART)
        with self.voiceover("Chapter six. Spacetime structures."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.panels()
        self.boost()
        self.table()
        self.symmetry()

    def panel(self, cx, kind):
        w, h = 3.6, 3.4
        frame = Rectangle(width=w, height=h, color=GREY_D, stroke_width=1.5).move_to([cx, -0.4, 0])
        slices = VGroup(*[Line([cx - w / 2, -0.4 - h / 2 + k * h / 6, 0], [cx + w / 2, -0.4 - h / 2 + k * h / 6, 0],
                               color=TIME, stroke_width=1.5, stroke_opacity=0.6) for k in range(1, 6)])
        extra = VGroup()
        if kind == "newton":
            extra = VGroup(*[Line([cx + x, -0.4 - h / 2, 0], [cx + x, -0.4 + h / 2, 0], color=SPACE, stroke_width=2)
                             for x in (-1.2, -0.4, 0.4, 1.2)])
        elif kind == "galileo":
            for s in (-0.5, 0.0, 0.5):
                for x0 in (-1.0, 0.2):
                    extra.add(Line([cx + x0 - s * h / 2, -0.4 - h / 2, 0], [cx + x0 + s * h / 2, -0.4 + h / 2, 0],
                                   color=SPACE, stroke_width=1.6, stroke_opacity=0.8))
        curved = ParametricFunction(lambda u: np.array([cx + 0.6 * math.sin(2.2 * u), -0.4 + u, 0]),
                                    t_range=[-h / 2, h / 2], color=MATTER, stroke_width=3)
        return VGroup(frame, slices, extra, curved)

    def panels(self):
        head = label(r"Three spacetimes", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        kinds = [("newton", r"Newtonian", r"absolute rest: \ vertical lines"),
                 ("galileo", r"Galilean", r"straight lines: \ inertial motion, \ no rest"),
                 ("leibniz", r"Leibnizian", r"slices only: \ no inertial structure")]
        ps = VGroup()
        caps = VGroup()
        for (k, name, cap), cx in zip(kinds, (-4.6, 0.0, 4.6)):
            p = self.panel(cx, k)
            ps.add(p)
            caps.add(VGroup(label(name, font_size=22, color=SPACE),
                            label(cap, font_size=17, color=GREY_A)).arrange(DOWN, buff=0.08).next_to(p, DOWN,
                                                                                                  buff=0.2))
        tl = label(r"time runs up, \ space across; \ the orange path is a wiggling body", font_size=18,
                   color=GREY_A).next_to(head, DOWN, buff=0.2)
        with self.voiceover(
            "Picture spacetime as a stack of instants, each instant a slice of space, time running upward. "
            "<bookmark mark='a'/>Newton's spacetime has two kinds of structure: the slices, which say what is "
            "simultaneous; and vertical lines through them, which say what is at the same place from one moment to "
            "the next. Those lines are absolute rest. <bookmark mark='b'/>Galilean spacetime, sometimes called "
            "neo-Newtonian, keeps the slices but replaces the vertical lines with a family of straight lines at "
            "every slope: the paths of bodies moving inertially. It can tell a straight path from a wiggling one, "
            "but it has no notion of rest. <bookmark mark='c'/>Leibnizian spacetime keeps only the slices, with "
            "their distances. In it, no path is straighter than any other."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tl))
            for mk, i in zip("abc", range(3)):
                vo.wait_until(mk)
                self.play(FadeIn(ps[i][0]), Create(ps[i][1]), Create(ps[i][2]), Create(ps[i][3]), FadeIn(caps[i]))
        self.clear_scene()

    def boost(self):
        d = load("boost")
        head = label(r"A Galilean boost, \ computed", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[-2.2, 2.2, 1], y_range=[-1.7, 1.7, 1], x_length=6.0, y_length=4.4, tips=False,
                  axis_config={"color": GREY_D}).move_to([-3.0, -0.5, 0])
        ts, xs, xb, rb = d["t"], d["path"], d["path_boosted"], d["rest_boosted"]

        def curve(vals, col, w=3):
            return VMobject(stroke_color=col, stroke_width=w).set_points_smoothly(
                [ax.c2p(x, t) for x, t in zip(vals, ts)])

        path, path_b = curve(xs, MATTER), curve(xb, MATTER)
        rest = Line(ax.c2p(0, -1.7), ax.c2p(0, 1.7), color=SPACE, stroke_width=3)
        rest_b = curve(rb, SPACE)
        v = d["v"]
        man, ex = f"{d['max_acceleration_change']:.0e}".split("e")
        side = stack([(rf"shear every worldline: \ $x \to x - {v}\,t$", ABS),
                      (r"the body at rest now moves: \ rest is frame-relative", SPACE),
                      (rf"every velocity shifts by ${d['velocity_shift']:+.1f}$", WHITE),
                      (rf"every acceleration is unchanged: \ largest change ${man} \times 10^{{{int(ex)}}}$", OK),
                      (r"so the laws can mention acceleration, \ never absolute velocity", GOAL)], font_size=20,
                     aligned_edge=LEFT, width=5.2, buff=0.3).move_to([3.7, -0.4, 0])
        with self.voiceover(
            "Here is the key symmetry, computed. <bookmark mark='a'/>A Galilean boost shears every worldline: each "
            "position x becomes x minus v t. <bookmark mark='b'/>The body at rest, the vertical line, now leans: "
            "it is moving. So whether something is at rest depends on the frame. <bookmark mark='c'/>The Reasoner "
            "checks the wiggling body by finite differences: every velocity changes by the same amount, minus the "
            "boost speed, <bookmark mark='d'/>and every acceleration is unchanged, to rounding error. "
            "<bookmark mark='e'/>That is why Newton's laws can be stated in terms of acceleration, and why absolute "
            "velocity never enters them."
        ) as vo:
            self.play(FadeIn(head), Create(ax), Create(rest), Create(path))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Transform(rest, rest_b), Transform(path, path_b), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def table(self):
        head = label(r"What each structure makes absolute", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        T = lambda s, c=WHITE: label(s, font_size=20, color=c)  # noqa: E731
        hd = [T(r"spacetime", CONN), T(r"simultaneity", CONN), T(r"distance", CONN), T(r"velocity", CONN),
              T(r"acceleration, \ rotation", CONN)]
        data = [(r"Aristotelian", True, True, True, True), (r"Newtonian", True, True, True, True),
                (r"Galilean", True, True, False, True), (r"Leibnizian", True, True, False, False)]
        rows = [[T(n, SPACE), mark(a), mark(b), mark(c), mark(e)] for n, a, b, c, e in data]
        grid = ValueGrid(hd, rows, col_w=[2.8, 2.4, 1.9, 1.9, 3.2], cell_h=0.62, font_size=20).move_to([0, 0.4, 0])
        notes = stack([(r"Aristotle adds a centre of the universe, \ and natural places", HIST),
                       (r"each row drops one structure from the row above", ABS)], font_size=20,
                      buff=0.2).next_to(grid, DOWN, buff=0.5)
        with self.voiceover(
            "Tabulate what each structure makes absolute. <bookmark mark='a'/>Aristotle's universe had all of it, "
            "and a centre too, the natural place toward which heavy things fall. <bookmark mark='b'/>Newton's "
            "keeps absolute simultaneity, distance, velocity and acceleration, and drops the centre. "
            "<bookmark mark='c'/>Galilean spacetime drops absolute velocity, and keeps acceleration and rotation. "
            "<bookmark mark='d'/>Leibnizian spacetime drops acceleration too. <bookmark mark='e'/>Each row takes "
            "one structure away. Which row is right?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            for mk, r in zip("abcd", range(4)):
                vo.wait_until(mk)
                self.play(*[FadeIn(c) for c in grid.cell[r]])
            vo.wait_until("e")
            self.play(FadeIn(notes))
        self.clear_scene()

    def symmetry(self):
        head = label(r"Just enough structure", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Earman's principles", r"the symmetries of the laws should be the symmetries of spacetime, \ and vice "
                                     r"versa", ABS),
            (r"too much", r"Newton's laws are unchanged by a uniform boost, \ so absolute velocity is idle structure: "
                          r"\ Newtonian spacetime has too much", BAD),
            (r"too little", r"$F = ma$ needs a difference between straight and curved paths: \ Leibnizian spacetime "
                            r"cannot state it, \ nor explain the bucket", BAD),
            (r"just right", r"Galilean spacetime: \ rotation is absolute, \ velocity is not; \ Leibniz was half "
                            r"right, \ Newton was half right", OK),
            (r"Maudlin's lesson", r"ask what the laws need, \ and believe in that much spacetime", GOAL),
        ]
        g = rows_table(rows, top=1.7, gap=0.42, width=8.6, x_text=-2.6, label_size=21, text_size=20)
        with self.voiceover(
            "John Earman gave a principle for choosing. <bookmark mark='a'/>The symmetries of the laws should be "
            "the symmetries of spacetime, and the other way round. <bookmark mark='b'/>Newton's laws are unchanged "
            "if everything is given the same extra velocity, so absolute velocity is idle structure, making no "
            "difference to anything: Newtonian spacetime has too much. <bookmark mark='c'/>But F equals m a needs "
            "a difference between a straight path and a curved one, an acceleration, and Leibnizian spacetime cannot "
            "even state it, let alone explain the bucket: it has too little. <bookmark mark='d'/>Galilean spacetime "
            "is just right. Rotation is absolute, velocity is not. Leibniz was right that the shifted worlds are the "
            "same, and Newton was right about the bucket. <bookmark mark='e'/>Tim Maudlin's lesson: ask what the laws "
            "need, and believe in that much spacetime structure. Relativity is about to change what the laws need."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
