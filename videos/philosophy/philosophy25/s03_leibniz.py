from __future__ import annotations

from videos.philosophy.philosophy25.common import *  # noqa: F403


class Leibniz(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"Leibniz and Clarke", r"Could the whole universe have been somewhere else?",
                            lit=(1715,), part=PART)
        with self.voiceover("Chapter two. Leibniz and Clarke."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.static()
        self.kinematic()
        self.checked()
        self.reply()

    def bodies(self, offset=(0, 0), color=MATTER):
        pts = [(-1.2, 0.6), (0.3, 1.1), (1.1, -0.2), (-0.4, -0.8), (0.6, 0.3)]
        g = VGroup(*[Dot([x + offset[0], y + offset[1], 0], radius=0.12, color=color) for x, y in pts])
        lines = VGroup(*[Line(g[i].get_center(), g[j].get_center(), color=GREY_C, stroke_width=1.5)
                         for i in range(5) for j in range(i + 1, 5)])
        return VGroup(lines, g)

    def static(self):
        hc = history_card(1715, r"Leibniz and Clarke", r"the correspondence, \ 1715--16", width=5.0,
                          color=HIST).to_corner(UL, buff=0.3)
        grid = NumberPlane(x_range=[-7, 7, 1], y_range=[-4, 4, 1], background_line_style={
            "stroke_color": GREY_D, "stroke_width": 1, "stroke_opacity": 0.5}).shift(DOWN * 0.3)
        w1 = self.bodies((-2.2, -0.6))
        w2 = self.bodies((2.2, -0.6), color=CURVE)
        l1 = label(r"the actual universe", font_size=20, color=MATTER).next_to(w1, DOWN, buff=0.3)
        l2 = label(r"the same, \ five metres east", font_size=20, color=CURVE).next_to(w2, DOWN, buff=0.3)
        rows = stack([(r"every relation between bodies is the same in both", WHITE),
                      (r"Leibniz: \ so they are indiscernible, \ and so one and the same", SPACE),
                      (r"and God could have no reason to choose one: \ the principle of sufficient reason", ABS)],
                     font_size=21, aligned_edge=LEFT, width=11.0, buff=0.25).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "From 1715 to 1716, Leibniz exchanged letters with Samuel Clarke, who spoke for Newton. Leibniz's "
            "weapon was the shift argument. <bookmark mark='a'/>If space were a container, God could have created "
            "the whole universe five metres east of where it is. <bookmark mark='b'/>Every distance between bodies, "
            "every relation of any kind, would be exactly the same. <bookmark mark='c'/>So, said Leibniz, the two "
            "situations are indiscernible, and by his principle of the identity of indiscernibles, they are one and "
            "the same. <bookmark mark='d'/>And besides, God could have had no reason to put the universe here rather "
            "than five metres east, which breaks the principle of sufficient reason. Space is nothing but the order "
            "of coexisting things."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(grid))
            vo.wait_until("a")
            self.play(FadeIn(w1), FadeIn(l1))
            self.play(TransformFromCopy(w1, w2), FadeIn(l2), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def kinematic(self):
        head = label(r"The kinematic shift", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        t = ValueTracker(0.0)
        base = self.bodies((-3.5, 0.2))
        moving = always_redraw(lambda: self.bodies((-3.5 + 1.2 * t.get_value(), 0.2), color=CURVE).set_opacity(0.85))
        clock = always_redraw(lambda: label(rf"$t = {t.get_value():.1f}$", font_size=22, color=TIME).move_to(
            [0, -2.0, 0]))
        rows = stack([(r"the universe, \ and the same universe moving uniformly east at 1000 km/s", WHITE),
                      (r"no experiment could tell them apart: \ Newton's laws are the same in both \ (Galileo's ship)",
                       SPACE),
                      (r"so absolute velocity is undetectable, \ even for Newton", BAD)], font_size=21,
                     aligned_edge=LEFT, width=11.0, buff=0.25).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The second shift is in motion. <bookmark mark='a'/>Take the universe, and a copy of it moving uniformly "
            "eastward through absolute space at a thousand kilometres a second, every body with the same extra "
            "velocity. <bookmark mark='b'/>Galileo had already seen the point on board a ship: in a cabin moving "
            "smoothly, every experiment comes out as it would at rest. Newton's laws are the same in both universes, "
            "so no observation could ever tell them apart. <bookmark mark='c'/>Newton accepted this. Absolute "
            "velocity, he admitted, is undetectable. Yet his theory said there was a fact about it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(base), FadeIn(moving), FadeIn(clock))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            self.play(t.animate.set_value(5.0), run_time=4, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        moving.clear_updaters()
        clock.clear_updaters()
        self.clear_scene()

    def checked(self):
        d = load("shifts")
        head = label(r"Checked: \ what the relations see", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        T = lambda s, c=WHITE: label(s, font_size=21, color=c)  # noqa: E731
        hd = [T(r"the whole universe, \ shifted", CONN), T(r"largest change in any distance", CONN),
              T(r"same relations?", CONN), T(r"water curves?", CONN)]
        rows = []
        for r in d["rows"]:
            dev = r["max_change_in_distances"]
            man, ex = f"{dev:.0e}".split("e")
            rows.append([T(r["world"]), MathTex(rf"{man} \times 10^{{{int(ex)}}}", font_size=22),
                         mark(r["relationally_same"]), mark(r["inertial_effects"])])
        grid = ValueGrid(hd, rows, col_w=[3.6, 4.0, 2.2, 2.2], cell_h=0.6, font_size=21).move_to([0, 0.3, 0])
        foot = label(r"relations cannot see rotation; \ the bucket can: \ Clarke's reply", font_size=22,
                     color=GOAL).next_to(grid, DOWN, buff=0.6)
        with self.voiceover(
            "The Reasoner checks both shifts, and two more, on a small universe of six moving bodies. "
            "<bookmark mark='a'/>Move everything five metres; turn the whole universe through an angle; give "
            "everything the same extra velocity; and set the whole universe rotating. <bookmark mark='b'/>In every "
            "case, every distance between every pair of bodies, at every moment, is unchanged, down to rounding "
            "error. Relationally, all four are the same world. <bookmark mark='c'/>But the fourth is the bucket "
            "writ large: in a rotating universe, Newton's water would climb the walls. Clarke's reply to Leibniz was "
            "exactly this: absolute motion has effects, so absolute space is real."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            for r in range(len(rows)):
                self.play(FadeIn(grid.cell[r][0]), run_time=0.4)
            vo.wait_until("b")
            for r in range(len(rows)):
                self.play(*[FadeIn(c) for c in grid.cell[r][1:3]], run_time=0.4)
            vo.wait_until("c")
            self.play(*[FadeIn(grid.cell[r][3]) for r in range(len(rows))])
            self.play(FadeIn(foot))
        self.clear_scene()

    def reply(self):
        head = label(r"Where the correspondence left it", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Leibniz", r"space is the order of coexisting things; \ shifted worlds are one world", SPACE),
            (r"Clarke", r"absolute motion has real effects; \ so space is real, \ `the sensorium of God'", MATTER),
            (r"the debt", r"Leibniz owed an account of rotation without absolute space; \ he never gave one", BAD),
            (r"the lesson", r"what a theory says exists should match what its laws can detect \ (chapter 6)", GOAL),
        ]
        g = rows_table(rows, top=1.5, gap=0.55, width=8.6, x_text=-2.4, label_size=22, text_size=21)
        with self.voiceover(
            "Where did the correspondence leave things? It ended with Leibniz's death in 1716. "
            "<bookmark mark='a'/>Leibniz: space is the order of coexisting things, and the shifted worlds are one "
            "world. <bookmark mark='b'/>Clarke: absolute motion has real effects, so space is real; Newton had even "
            "called it, in a phrase Leibniz mocked, a kind of sensorium of God. <bookmark mark='c'/>Leibniz owed "
            "an account of the bucket, of rotation without absolute space, and he never gave one. "
            "<bookmark mark='d'/>The lasting lesson is a principle of economy: what a theory says exists should "
            "match what its laws can detect. Chapter six follows that principle to a better spacetime than "
            "Newton's."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
