from __future__ import annotations

import numpy as np

from videos.psychology.psych14.common import *  # noqa: F403


class Inverse(VoiceoverScene):
    def construct(self):
        self.card()
        self.many()
        self.ames()

    def card(self):
        card = chapter_card(1, r"The inverse problem", r"Why is every image ambiguous?", lit={1867: r"Helmholtz"},
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter one. The inverse problem."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def many(self):
        d = load("inverse")
        head = heading(r"One image, \ many worlds")
        eye = VGroup(Circle(radius=0.35, color=GREY_B, stroke_width=3), Dot(color=GREY_B, radius=0.05))
        eye.move_to([-6.0, 0.5, 0])
        rays = VGroup()
        objs = VGroup()
        for k, (dist, col) in enumerate(((2.0, LIKE), (4.0, PRIOR), (6.5, WORLD))):
            h = 0.35 * dist
            x = -6.0 + dist * 1.0
            objs.add(Line([x, 0.5 - h / 2, 0], [x, 0.5 + h / 2, 0], color=col, stroke_width=6))
        top = Line(eye[1].get_center(), [-6.0 + 6.5 * 1.0, 0.5 + 0.35 * 6.5 / 2, 0], color=GREY_C, stroke_width=1.5)
        bot = Line(eye[1].get_center(), [-6.0 + 6.5 * 1.0, 0.5 - 0.35 * 6.5 / 2, 0], color=GREY_C, stroke_width=1.5)
        rays.add(top, bot)
        A = axes([0, 10], [0, 0.4], x_length=4.2, y_length=2.4, xticks=[0, 5, 10], yticks=[0, 0.2, 0.4],
                 xlabel=r"distance (m)", ylabel=r"size (m)", center=[4.2, 0.9, 0])
        ax = A.ax
        line = curve(ax, d["d"], d["size"], WORLD, stroke_width=4)
        rows = rows_of([
            (r"a small thing near, \ a large thing far: \ the same image on the retina", WHITE),
            (rf"every point on the line casts the same {d['angle']:g}$^\circ$ image", WORLD),
            (r"seeing size needs a guess about distance, \ and seeing distance needs a guess about something else", PRIOR),
        ], 12.4, 28, 0.3).to_edge(DOWN, buff=0.7)
        tag = psyche_tag(r"computed: \ size = 2 \ distance \ tan(angle / 2)")
        with self.voiceover(
            "Here is the problem in its simplest form. <bookmark mark='a'/> A small object close to the eye, a larger "
            "one further away, and a larger one still: all three cast exactly the same image on the retina. "
            "<bookmark mark='b'/> Every combination of size and distance along this line makes the same two-degree "
            "image. <bookmark mark='c'/> So to see an object's size, the visual system needs a guess about its "
            "distance; and to see distance, it needs a guess about something else. The image alone can't decide. "
            "Mathematicians call this an inverse problem: going from effects back to causes, when many causes give "
            "the same effect."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eye), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(rays), LaggedStart(*[FadeIn(o) for o in objs], lag_ratio=0.4), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(A), Create(line), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def ames(self):
        head = heading(r"The Ames room, \ from above")
        # plan view: a trapezoidal room; the peephole at the bottom
        far_left, far_right = np.array([-3.5, 2.2, 0]), np.array([1.5, 1.0, 0])
        near_left, near_right = np.array([-3.5, -1.0, 0]), np.array([1.5, -1.0, 0])
        room = Polygon(near_left, near_right, far_right, far_left, color=GREY_B, stroke_width=3)
        eye = Dot([-1.0, -2.6, 0], color=WORLD, radius=0.09)
        el = label(r"peephole", font_size=22, color=WORLD).next_to(eye, DOWN, buff=0.1)
        p1 = Dot(far_left + np.array([0.4, -0.3, 0]), color=LIKE, radius=0.16)
        p2 = Dot(far_right + np.array([-0.4, -0.2, 0]), color=VISION, radius=0.16)
        seen = DashedLine([-3.5, 1.0, 0], [1.5, 1.0, 0], color=GREY_C, stroke_width=2)
        sl = label(r"how the back wall looks", font_size=20, color=GREY_C).next_to(seen, UP, buff=0.05).shift(LEFT * 0.4)
        rows = rows_of([
            (r"the back wall really runs away at a slant; \ through the peephole it looks square to you", WHITE),
            (r"the person in the far corner is much further away, \ so casts a smaller image", LIKE),
            (r"the visual system bets the room is rectangular, \ and so sees a giant and a dwarf", PRIOR),
            (r"the prior about rooms beats the prior that people are much the same size", GREY_A),
        ], 5.2, 26, 0.32).move_to([4.4, -0.2, 0])
        keep_in_frame(rows)
        tag = note(r"a plan of the room, \ drawn").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Adelbert Ames built a room in the nineteen-forties that turns this into a show. Here it is from above. "
            "<bookmark mark='a'/> Its back wall runs away at a slant, but the walls and windows are cut so that through a "
            "peephole it looks like an ordinary rectangular room. <bookmark mark='b'/> Put one person in each back "
            "corner. The one in the far corner is much further away, so casts a much smaller image. "
            "<bookmark mark='c'/> The visual system bets the room is rectangular, and so both people must be at the same "
            "distance, and one must be a giant and the other a dwarf. <bookmark mark='d'/> Two assumptions conflict: "
            "that rooms are rectangular, and that adults are roughly the same size. The room wins."
        ) as vo:
            self.play(FadeIn(head), Create(room), FadeIn(eye), FadeIn(el), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(seen), FadeIn(sl), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(p1), FadeIn(p2), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
