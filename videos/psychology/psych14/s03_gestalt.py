from __future__ import annotations

import numpy as np

from videos.psychology.psych14.common import *  # noqa: F403


def dot_grid(nx, ny, dx, dy, color=WHITE, radius=0.09, colors=None):
    g = VGroup()
    for j in range(ny):
        for i in range(nx):
            c = colors(i, j) if colors else color
            g.add(Dot([i * dx, -j * dy, 0], radius=radius, color=c))
    return g.center()


def pacman(radius, gap_dir, centre):
    """A disc with a 60-degree wedge cut out, the wedge facing ``gap_dir`` (radians)."""
    return Sector(radius=radius, angle=5 * PI / 3, start_angle=gap_dir + PI / 6, arc_center=centre, fill_color=GREY_A,
                  fill_opacity=1, stroke_width=0)


class Gestalt(VoiceoverScene):
    def construct(self):
        self.card()
        self.laws()
        self.kanizsa()
        self.figure()

    def card(self):
        card = chapter_card(2, r"Grouping and the Gestalt laws", r"Which parts of an image belong together?",
                            lit={1923: r"Wertheimer", 1955: r"Kanizsa"}, part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter two. Grouping, and the Gestalt laws."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def laws(self):
        head = heading(r"Four rules for what goes with what")
        prox = dot_grid(4, 6, 0.5, 0.2)
        prox_l = label(r"proximity", font_size=28, color=PRIOR)
        sim = dot_grid(6, 4, 0.4, 0.4, colors=lambda i, j: LIKE if j % 2 else VISION)
        sim_l = label(r"similarity", font_size=28, color=PRIOR)
        # continuation: two smooth curves crossing
        c1 = ParametricFunction(lambda t: [t, 0.6 * np.sin(2.2 * t), 0], t_range=[-1.3, 1.3], color=WHITE, stroke_width=4)
        c2 = ParametricFunction(lambda t: [t, -0.6 * np.sin(2.2 * t), 0], t_range=[-1.3, 1.3], color=WHITE, stroke_width=4)
        cont = VGroup(c1, c2)
        cont_l = label(r"good continuation", font_size=28, color=PRIOR)
        arcs = VGroup(*[Arc(radius=0.8, start_angle=a, angle=PI / 2 - 0.45, color=WHITE, stroke_width=5)
                        for a in (0.22, PI / 2 + 0.22, PI + 0.22, 3 * PI / 2 + 0.22)])
        clos_l = label(r"closure", font_size=28, color=PRIOR)
        panels = VGroup(*[VGroup(p, l_.next_to(p, DOWN, buff=0.35)) for p, l_ in
                          ((prox, prox_l), (sim, sim_l), (cont, cont_l), (arcs, clos_l))]).arrange(RIGHT, buff=0.9)
        panels.move_to([0, 1.0, 0])
        keep_in_frame(panels)
        rows = rows_of([
            (r"proximity: \ you see columns, \ not rows; \ similarity: \ rows, \ not columns", WHITE),
            (r"continuation: \ two smooth curves crossing, \ not two V's touching; \ closure: \ a circle with gaps", WHITE),
            (r"each rule is a regularity of the world: \ the parts of one object are near, \ alike, \ and smooth", POST),
        ], 12.6, 28, 0.3).to_edge(DOWN, buff=0.7)
        tag = note(r"drawn after Wertheimer (1923)").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Before the visual system can recognize anything, it has to decide which bits of the image belong "
            "together. Max Wertheimer laid out rules for this in 1923, and they are still taught as the Gestalt laws. "
            "<bookmark mark='a'/> Proximity: dots that are closer group together, so here you see columns. Similarity: "
            "dots that look alike group together, so here you see rows, though every dot is equally spaced. "
            "<bookmark mark='b'/> Good continuation: you see two smooth curves crossing, not two pointed shapes "
            "touching at their tips. Closure: four arcs with gaps, seen as one circle. <bookmark mark='c'/> The "
            "Gestalt psychologists thought of these as laws of the brain's own organization. The modern reading is "
            "statistical. Each rule is a regularity of the world: the parts of one object tend to be close together, "
            "to look alike, and to have smooth edges. Measured in photographs of natural scenes, edges that belong "
            "to one contour really do tend to continue smoothly. The laws are priors."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            self.play(LaggedStart(*[FadeIn(p) for p in panels], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Indicate(panels[0]), Indicate(panels[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Indicate(panels[2]), Indicate(panels[3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def kanizsa(self):
        head = heading(r"A triangle that is not there")
        R = 1.7
        corners = [np.array([R * np.cos(a), R * np.sin(a), 0]) for a in (PI / 2, PI / 2 + 2 * PI / 3, PI / 2 + 4 * PI / 3)]
        discs = VGroup()
        for c in corners:
            gap = np.arctan2(-c[1], -c[0])  # the wedge points at the centre
            discs.add(pacman(0.55, gap, c))
        # an outline triangle, pointing down, drawn as three separate corners
        inv = [np.array([R * 0.95 * np.cos(a), R * 0.95 * np.sin(a), 0]) for a in (-PI / 2, -PI / 2 + 2 * PI / 3, -PI / 2 + 4 * PI / 3)]
        outline = VGroup()
        for k, c in enumerate(inv):
            for other in (inv[(k + 1) % 3], inv[(k + 2) % 3]):
                u = (other - c) / np.linalg.norm(other - c)
                outline.add(Line(c, c + 0.75 * u, color=GREY_A, stroke_width=4))
        fig = VGroup(discs, outline).move_to([-3.4, -0.3, 0])
        rows = rows_of([
            (r"a white triangle, \ brighter than the page, \ with sharp edges across empty paper", WHITE),
            (r"the edges are not in the image: \ no light changes where you see them", LIKE),
            (r"the best explanation of three cut discs, \ lined up exactly, \ is a triangle lying on top", PRIOR),
            (r"V2 neurons fire to illusory contours \ (von der Heydt and colleagues, \ 1984)", GREY_A),
        ], 5.6, 27, 0.34).move_to([3.5, -0.2, 0])
        keep_in_frame(rows)
        tag = note(r"drawn after Kanizsa (1955)").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Grouping can go further than joining pieces. It can make things up. <bookmark mark='a'/> This figure was "
            "published by Gaetano Kanizsa in 1955. Most people see a white triangle lying on top of three discs and "
            "an outline triangle, and the white triangle looks slightly brighter than the page around it, with sharp "
            "edges. <bookmark mark='b'/> But those edges aren't in the image. Along most of their length, nothing on "
            "the page changes. <bookmark mark='c'/> Why see them? Because three discs, each with a wedge missing, "
            "with the wedges lined up exactly, would be a remarkable coincidence. A triangle lying on top, covering "
            "them, explains all of it at once. The visual system takes the explanation, and draws its edges in. "
            "<bookmark mark='d'/> And not just in experience: in 1984, Rüdiger von der Heydt and colleagues found "
            "neurons in the monkey's second visual area that fire to these illusory edges as if they were real."
        ) as vo:
            self.play(FadeIn(head), FadeIn(fig), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def figure(self):
        head = heading(r"Figure and ground")
        # a vase whose two edges are face profiles: (y, x) points of the right edge
        prof = [(1.6, 0.95), (1.25, 0.9), (0.95, 0.72), (0.7, 0.42), (0.45, 0.62), (0.2, 0.5), (0.0, 0.62),
                (-0.25, 0.48), (-0.5, 0.46), (-0.8, 0.62), (-1.2, 0.9), (-1.6, 1.0)]
        right = [np.array([x, y, 0]) for y, x in prof]
        left = [np.array([-x, y, 0]) for y, x in prof[::-1]]
        vase = VMobject(fill_color=GREY_A, fill_opacity=1, stroke_width=0)
        vase.set_points_smoothly(right + left + [right[0]])
        bg = Rectangle(width=3.6, height=3.2, fill_color=BLACK, fill_opacity=1, stroke_color=GREY_C, stroke_width=2)
        fig = VGroup(bg, vase).move_to([-3.6, -0.3, 0])
        rows = rows_of([
            (r"a vase, \ or two faces: \ the same edges, \ owned by one side or the other", WHITE),
            (r"the edges can belong to only one region at a time, \ and the view flips", PRIOR),
            (r"the region that owns the edge is seen as in front, \ with a shape; \ the other is background", POST),
            (r"V2 cells signal which side owns an edge \ (Zhou, \ Friedman and von der Heydt, \ 2000)", GREY_A),
        ], 5.6, 27, 0.34).move_to([3.5, -0.2, 0])
        keep_in_frame(rows)
        tag = note(r"drawn after Rubin (1915)").to_corner(DR, buff=0.3)
        with self.voiceover(
            "One more decision the visual system makes before it recognizes anything: which side of an edge is the "
            "object. <bookmark mark='a'/> Edgar Rubin's figure of 1915 can be a white vase on black, or two black "
            "faces in profile, looking at each other. <bookmark mark='b'/> The edges are the same either way. What "
            "changes is which side owns them, and they can belong to only one side at a time: most people see the "
            "vase or the faces, and flip between them, rarely both. <bookmark mark='c'/> Whichever region owns the "
            "edge is seen as in front, and as having a shape; the other becomes shapeless background, running on "
            "behind. <bookmark mark='d'/> This too has been found in single cells: in 2000, Zhou, Friedman and von der "
            "Heydt found cells in the second visual area that signal which side of an edge is the figure. These "
            "aren't decorations on vision. They are early, fast, and the rest of seeing builds on them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(fig), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Indicate(vase, color=PRIOR))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
