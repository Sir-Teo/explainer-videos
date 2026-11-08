from __future__ import annotations

from videos.philosophy.philosophy25.common import *  # noqa: F403


class Convention(VoiceoverScene):
    R = 2.6

    def construct(self):
        card = chapter_card(5, r"Geometry by convention?", r"Could we ever find out the shape of space?",
                            lit=(1902, 1928), part=PART)
        with self.voiceover("Chapter five. Geometry by convention?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.world()
        self.measured()
        self.forces()
        self.holism()

    def world(self):
        hc = history_card(1902, r"Henri Poincaré", r"\textit{Science and Hypothesis}", width=5.4,
                          color=HIST).to_corner(UL, buff=0.3)
        c = np.array([-3.2, -0.7, 0])
        heat = VGroup(*[Circle(radius=self.R * (1 - k / 12), stroke_width=0, fill_color=interpolate_color(
            ManimColor(CURVE), ManimColor(SPACE), k / 11), fill_opacity=0.18).move_to(c) for k in range(12)][::-1])
        rim = Circle(radius=self.R, color=GREY_B, stroke_width=2.5).move_to(c)
        t = ValueTracker(0.0)

        def ruler():
            r = 0.92 * math.tanh(t.get_value())
            length = 0.5 * (1 - r * r)        # a ruler of measured length 1/4 at the point r
            p = c + np.array([r * self.R, 0, 0])
            bar = Line(p - np.array([length * self.R / 2, 0, 0]), p + np.array([length * self.R / 2, 0, 0]),
                       color=LIGHT, stroke_width=7)
            return bar

        bar = always_redraw(ruler)
        rows = stack([(r"a disk, \ hot at the centre, \ cold at the rim: \ $T \propto 1 - r^2/R^2$", CURVE),
                      (r"every body shrinks with the temperature, \ in the same proportion", WHITE),
                      (r"the inhabitants' rulers shrink too, \ so they cannot see it", LIGHT),
                      (r"walking toward the rim, \ they never arrive", SPACE)], font_size=21, aligned_edge=LEFT,
                     width=5.8, buff=0.3).move_to([3.6, -0.3, 0])
        with self.voiceover(
            "Henri Poincaré argued in 1902 that geometry is not something we discover. He asked us to imagine a "
            "world. <bookmark mark='a'/>A flat disk, hot at the centre and growing colder toward the rim, with the "
            "temperature falling off as one minus r squared over R squared. <bookmark mark='b'/>Every body in this "
            "world expands and shrinks with the temperature, all in the same proportion. "
            "<bookmark mark='c'/>So the inhabitants' rulers shrink as they carry them outward, and since everything "
            "shrinks together, they can never notice it. <bookmark mark='d'/>Walking toward the rim, they take "
            "smaller and smaller steps, and never arrive. To them, their world is infinite."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(heat), Create(rim))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(bar))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), t.animate.set_value(2.6), run_time=4, rate_func=linear)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        bar.clear_updaters()
        self.clear_scene()

    def measured(self):
        d = load("diskworld")
        head = label(r"What their rulers measure", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        f = MathTex(r"ds = \frac{2\,|dx|}{1 - r^2}", font_size=42, color=LIGHT).move_to([-3.4, 1.6, 0])
        hd = [r"r", r"\text{measured radius}", r"\text{measured circumference}", r"C / (\pi \cdot 2\rho)"]
        rows = [[MathTex(f"{r['r']:.2f}", font_size=22), MathTex(f"{r['measured_radius']:.2f}", font_size=22),
                 MathTex(f"{r['measured_circumference']:.1f}", font_size=22, color=SPACE),
                 MathTex(f"{r['ratio_over_pi']:.2f}", font_size=22, color=CURVE)] for r in d["rows"]]
        grid = ValueGrid(hd, rows, col_w=[1.2, 2.8, 3.6, 2.4], cell_h=0.46, font_size=20).move_to([0.6, -0.6, 0])
        note = label(r"circles with more than $\pi$ times their diameter: \ the inhabitants find hyperbolic geometry",
                     font_size=21, color=GOAL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "What do their rulers measure? <bookmark mark='a'/>If every length shrinks in proportion to one minus r "
            "squared, a step of coordinate size dx measures as twice dx over one minus r squared: exactly the "
            "distance of the Poincaré disk from the last chapter. <bookmark mark='b'/>The Reasoner measures circles "
            "as the inhabitants would. The measured radius grows without bound toward the rim. And the "
            "circumference grows faster still: the ratio of circumference to diameter, divided by pi, rises from "
            "just over one to nearly nineteen. <bookmark mark='c'/>The inhabitants, measuring carefully, conclude "
            "that they live in an infinite hyperbolic plane. And they could equally say: our space is a flat, "
            "finite disk, and a universal force shrinks every ruler. The two descriptions agree on every observation."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(len(rows)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.5)
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.clear_scene()

    def forces(self):
        head = label(r"Geometry plus physics", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        f = MathTex(r"\text{observations} \;=\; ", r"\text{geometry}", r"\;+\;", r"\text{physics}", font_size=40
                    ).move_to([0, 1.5, 0])
        f[1].set_color(SPACE)
        f[3].set_color(CURVE)
        rows = [
            (r"Poincaré \ (1902)", r"only the combination is tested; \ choose the geometry, \ adjust the physics: \ "
                                   r"Euclid is simplest, \ so keep it", HIST),
            (r"Reichenbach \ (1928)", r"`universal forces' affect everything alike and cannot be detected: \ set them "
                                      r"to zero, \ by definition", ABS),
            (r"Einstein", r"geometry alone says nothing about experience; \ only geometry together with physics", TIME),
            (r"the outcome", r"general relativity kept curved geometry and no universal forces: \ simplicity chose "
                             r"Riemann, \ not Euclid", GOAL),
        ]
        g = rows_table(rows, top=0.6, gap=0.42, width=8.6, x_text=-2.6, label_size=21, text_size=20)
        with self.voiceover(
            "The moral is Poincaré's conventionalism. <bookmark mark='a'/>What experience tests is never geometry "
            "alone, but geometry plus physics: how rulers and light behave. <bookmark mark='b'/>Choose any geometry "
            "you like and adjust the physics to match. Poincaré thought we would always choose Euclid, because it is "
            "simplest. <bookmark mark='c'/>Hans Reichenbach sharpened the point in 1928. Forces that act on all "
            "bodies alike, universal forces, cannot be detected; set them to zero by definition, and the geometry "
            "becomes a matter of fact relative to that definition. <bookmark mark='d'/>Einstein agreed that geometry "
            "alone says nothing about experience. <bookmark mark='e'/>But history turned Poincaré's prediction "
            "upside down: general relativity keeps a curved geometry and no universal forces, because that combination "
            "is simpler overall. This is Duhem and Quine's holism from Part 18, applied to space."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f))
            for mk, r in zip("bcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def holism(self):
        head = label(r"Is it really a convention?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"for", r"two theories that agree on every possible observation say the same thing \ (Part 18's "
                     r"verificationism)", OK),
            (r"against", r"Putnam: \ the realist can say that one of them is true \ and the other only empirically "
                         r"equivalent", BAD),
            (r"a test case", r"if the disk dwellers' forces have no source and no other effect, \ are they real?",
             CURVE),
            (r"what is at stake", r"the next chapter's question: \ how much structure should we believe space has?",
             GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.8, x_text=-2.8, label_size=22, text_size=21)
        with self.voiceover(
            "Is it really a matter of convention? <bookmark mark='a'/>For: two theories that agree on every possible "
            "observation say the same thing, as the verificationists of Part 18 held. <bookmark mark='b'/>Against: "
            "Hilary Putnam argued that a realist can hold that one of two empirically equivalent theories is true "
            "and the other false. <bookmark mark='c'/>The disk dwellers' universal force is a test case: a force "
            "with no source, no other effect, and no way to switch it off. Is it real, or an artefact of a choice of "
            "words? <bookmark mark='d'/>Behind the debate is the next chapter's question: how much structure should "
            "we believe space and time have?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
