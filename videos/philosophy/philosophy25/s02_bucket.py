from __future__ import annotations

from videos.philosophy.philosophy25.common import *  # noqa: F403


class Bucket(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"Newton's bucket", r"Is there a motion that is not relative to anything?",
                            lit=(1687,), part=PART)
        with self.voiceover("Chapter one. Newton's bucket."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.absolute()
        self.experiment()
        self.computed()
        self.mach()

    def absolute(self):
        q = quote_card(r"Absolute space, \ in its own nature, \ without relation to anything external, \ remains "
                       r"always similar and immovable.", r"Isaac Newton",
                       r"\textit{Principia} \ (1687), \ Scholium to the Definitions", width=10.0,
                       font_size=26).to_edge(UP, buff=0.5)
        rows = stack([(r"absolute space: \ a container, \ existing whether or not anything is in it", SPACE),
                      (r"absolute motion: \ change of place in that container", MATTER),
                      (r"but we only ever see bodies move relative to other bodies", BAD),
                      (r"Newton's answer: \ some motions show themselves, \ by their effects", GOAL)], font_size=22,
                     aligned_edge=LEFT, width=11.2, buff=0.3).move_to([0, -1.1, 0])
        with self.voiceover(
            "In the Principia of 1687, Newton set out his view of space. <bookmark mark='a'/>Absolute space, in its "
            "own nature, without relation to anything external, remains always similar and immovable. "
            "<bookmark mark='b'/>Space is a container, and it would exist even if nothing were in it. "
            "<bookmark mark='c'/>Absolute motion is change of place in that container. <bookmark mark='d'/>The "
            "obvious objection: we only ever see bodies move relative to other bodies. How could we know anything "
            "about motion relative to space itself? <bookmark mark='e'/>Newton's answer was that some motions show "
            "themselves by their effects, and his example was a bucket of water."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            for mk, r in zip("bcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def experiment(self):
        d = load("bucket")
        head = label(r"The bucket, \ in four stages", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rad = d["radius"]
        cx, base, wpx, hpx = -3.0, -1.8, 2.2, 2.6
        scale = wpx / rad
        wall = VGroup(Line([cx - wpx, base, 0], [cx - wpx, base + hpx, 0], color=GREY_B, stroke_width=4),
                      Line([cx + wpx, base, 0], [cx + wpx, base + hpx, 0], color=GREY_B, stroke_width=4),
                      Line([cx - wpx, base, 0], [cx + wpx, base, 0], color=GREY_B, stroke_width=4))
        w = ValueTracker(0.0)
        level = 1.3

        def surface():
            om = w.get_value()
            # conserve volume: the paraboloid's mean height over the disk is z_max / 2
            zmax = om ** 2 * rad ** 2 / (2 * 9.81)
            z0 = level - 30 * zmax / 2
            pts = [[cx + x * scale, base + z0 + 30 * om ** 2 * x ** 2 / (2 * 9.81), 0]
                   for x in np.linspace(-rad, rad, 41)]
            water = Polygon(*([[cx - wpx, base, 0]] + pts + [[cx + wpx, base, 0]]), stroke_width=0,
                            fill_color=SPACE, fill_opacity=0.45)
            top = VMobject(stroke_color=SPACE, stroke_width=3).set_points_smoothly(pts)
            return VGroup(water, top)

        water = always_redraw(surface)
        spin_b = ValueTracker(0.0)
        arrow_b = always_redraw(lambda: label(r"bucket spinning" if spin_b.get_value() > 0.5 else r"bucket at rest",
                                              font_size=19, color=MATTER).next_to(wall, DOWN, buff=0.25))
        steps = stack([(r"1. \ bucket and water at rest: \ the surface is flat", WHITE),
                       (r"2. \ spin the bucket: \ at first the water lags, \ still flat", MATTER),
                       (r"3. \ the water catches up: \ no motion relative to the bucket, \ yet the surface is curved",
                        CURVE),
                       (r"4. \ stop the bucket: \ the water still spins, \ still curved", TIME),
                       (r"the curvature tracks rotation, \ not motion relative to the bucket", GOAL)], font_size=20,
                      aligned_edge=LEFT, width=6.0, buff=0.28).move_to([3.6, -0.3, 0])
        with self.voiceover(
            "Hang a bucket of water from a twisted rope and let it go. <bookmark mark='a'/>At the start, bucket and "
            "water are at rest, and the surface is flat. <bookmark mark='b'/>The rope unwinds and spins the bucket. "
            "At first the water lags behind: it moves relative to the bucket, and its surface stays flat. "
            "<bookmark mark='c'/>Friction slowly brings the water up to speed. Now the water and the bucket turn "
            "together, with no motion relative to each other, and the surface is curved, climbing the walls. "
            "<bookmark mark='d'/>Grab the bucket and stop it. The water keeps spinning, now in motion relative to the "
            "bucket again, and the surface stays curved. <bookmark mark='e'/>So the curvature does not track motion "
            "relative to the bucket. Newton concluded that it tracks rotation relative to absolute space."
        ) as vo:
            self.play(FadeIn(head), Create(wall), FadeIn(water), FadeIn(arrow_b))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(spin_b.animate.set_value(1.0), FadeIn(steps[1]), run_time=0.5)
            vo.wait_until("c")
            self.play(w.animate.set_value(6.0), FadeIn(steps[2]), run_time=3)
            vo.wait_until("d")
            self.play(spin_b.animate.set_value(0.0), FadeIn(steps[3]), run_time=0.5)
            vo.wait_until("e")
            self.play(FadeIn(steps[4]))
        water.clear_updaters()
        arrow_b.clear_updaters()
        self.clear_scene()

    def computed(self):
        d = load("bucket")
        head = label(r"How much does the water climb?", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        f = MathTex(r"z(r) = \frac{\omega^2 r^2}{2g}", font_size=44, color=CURVE).move_to([3.6, 1.5, 0])
        ax = Axes(x_range=[-0.15, 0.15, 0.05], y_range=[0, 0.045, 0.01], x_length=6.0, y_length=3.6,
                  axis_config={"color": GREY_B, "font_size": 16}, y_axis_config={"include_numbers": True},
                  x_axis_config={"include_numbers": True}).move_to([-3.0, -0.6, 0])
        xl = label(r"distance from the axis (m)", font_size=17, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.4)
        yl = label(r"height above the centre (m)", font_size=17, color=GREY_A).next_to(ax.y_axis, UP,
                                                                                      buff=0.1).align_to(ax, LEFT)
        cols = [GREY_B, SPACE, MATTER, CURVE]
        curves = VGroup(*[series_plot(ax, r["z"], c, xs=d["r"], width=3) for r, c in zip(d["rows"], cols)])
        hd = [r"\omega\ (\text{rad/s})", r"\text{rise at the wall (mm)}"]
        rows = [[MathTex(f"{r['omega']:.0f}", font_size=24, color=c), MathTex(f"{r['rise_mm']:.1f}", font_size=24)]
                for r, c in zip(d["rows"], cols)]
        grid = ValueGrid(hd, rows, col_w=[2.2, 3.4], cell_h=0.46, font_size=20).move_to([3.6, -0.6, 0])
        note = label(r"radius 15 cm, \ about one turn a second: \ the water climbs about 4 cm", font_size=20,
                     color=GOAL).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The shape is easy to compute. <bookmark mark='a'/>In a rotating bucket the surface is a paraboloid: its "
            "height grows as omega squared r squared over twice g. <bookmark mark='b'/>The Reasoner draws it for a "
            "bucket fifteen centimetres in radius, at rest and at two, four and six radians a second. "
            "<bookmark mark='c'/>At about one turn a second, the water at the wall rises some four centimetres above "
            "the centre. <bookmark mark='d'/>The size of the effect depends only on the rotation rate, which is "
            "exactly Newton's point: the rotation is a definite physical quantity, and it is not relative to the "
            "bucket."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Write(f))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.3), FadeIn(grid.head), Create(grid.rule))
            for r in range(len(rows)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.4)
            vo.wait_until("c")
            self.play(FadeIn(note))
            vo.wait_until("d")
            self.play(Indicate(curves[-1], color=GOAL))
        self.clear_scene()

    def mach(self):
        head = label(r"Relative to what?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Newton", r"rotation relative to absolute space", SPACE),
            (r"Mach \ (1883)", r"rotation relative to the fixed stars, \ the bulk of the universe's matter: \ spin "
                               r"the universe instead, \ and the water would curve", MATTER),
            (r"the test", r"we cannot spin the universe; \ but does the distant matter matter?", BAD),
            (r"Einstein", r"Mach's principle inspired general relativity, \ which only partly obeys it \ "
                          r"(chapter 11)", TIME),
            (r"Maudlin's moral", r"the bucket shows that rotation is absolute, \ not that position or velocity is "
                                 r"\ (chapter 6)", GOAL),
        ]
        g = rows_table(rows, top=1.7, gap=0.48, width=8.6, x_text=-2.4, label_size=22, text_size=21)
        with self.voiceover(
            "Relative to what, though? <bookmark mark='a'/>For Newton, rotation relative to absolute space. "
            "<bookmark mark='b'/>In 1883 Ernst Mach proposed instead: rotation relative to the fixed stars, the "
            "bulk of the matter in the universe. Hold the bucket still and spin the whole universe around it, and "
            "the water, Mach suggested, would curve just the same. <bookmark mark='c'/>No one can spin the universe, "
            "so the proposal is hard to test; but it raises a real question, whether distant matter makes the "
            "difference. <bookmark mark='d'/>Mach's principle inspired Einstein, and general relativity obeys it "
            "only in part. <bookmark mark='e'/>Tim Maudlin draws a sharper moral, which chapter six will build: the "
            "bucket shows that rotation, and acceleration generally, is absolute. It does not show that there is "
            "absolute position, or absolute velocity."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
