from __future__ import annotations

import numpy as np

from videos.psychology.psych14.common import *  # noqa: F403


class Objects(VoiceoverScene):
    def construct(self):
        self.card()
        self.templates()
        self.marr()
        self.parts()
        self.speed()

    def card(self):
        card = chapter_card(9, r"Recognizing objects", r"How do you know a mug from any angle?",
                            lit={1982: r"Marr", 1987: r"Biederman", 1996: r"Thorpe"}, part=PART, scale=("mind", "circuit"),
                            marr=("what", "how"))
        with self.voiceover("Chapter nine. Recognizing objects."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def templates(self):
        d = load("templates")
        head = heading(r"Why matching pictures fails")
        names = (("square", r"a square", WORLD), ("moved", r"the same square, \ moved", WORLD),
                 ("turned", r"the same square, \ turned", WORLD), ("disc", r"a disc", LIKE))
        tiles = Group()
        for key, cap, col in names:
            img = picture(d[key], 2.2)
            box = frame_box(img)
            tiles.add(Group(img, box, label(cap, font_size=22, color=col).next_to(img, DOWN, buff=0.15)))
        tiles.arrange(RIGHT, buff=0.55).move_to([0, 1.1, 0])
        dists = VGroup()
        for t, key in zip(tiles[1:], ("dist_moved", "dist_turned", "dist_disc")):
            dists.add(label(rf"distance {d[key]:.1f}", font_size=26, color=POST).next_to(t, DOWN, buff=0.15))
        rows = rows_of([
            (r"distance: \ the square root of the summed squared pixel differences from the first square", GREY_A),
            (r"by pixels, \ the disc is closer to the square than the square is to itself, \ moved or turned", BAD),
            (r"recognition needs a description that stays the same when the image changes: \ invariance", POST),
        ], 12.6, 27, 0.28).to_edge(DOWN, buff=0.7)
        tag = psyche_tag(r"computed: \ 40 by 40 pixel images")
        with self.voiceover(
            "The simplest theory of recognition stores a picture of each object and compares new images with the "
            "pictures. It fails, and here's why. <bookmark mark='a'/> Four images: a square; the same square, "
            "moved; the same square, turned; and a disc. <bookmark mark='b'/> Measure how different each is from the "
            "first, pixel by pixel. The moved square differs by eighteen and a half units, the turned one by nine "
            "point four, and the disc by only six point nine. <bookmark mark='c'/> By the pixels, the disc is more "
            "like the square than the square is like itself, moved or turned. And for real objects it's far worse: "
            "changes of lighting, distance and viewpoint make the images of one mug more different from each other "
            "than from the images of a bowl. <bookmark mark='d'/> So recognition needs a description of an object "
            "that stays the same when its image changes. The name for this is invariance, and achieving it is the "
            "central problem of object recognition."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t) for t in tiles], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in dists], lag_ratio=0.5), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def marr(self):
        head = heading(r"Marr's stages, \ 1982")
        boxes = VGroup()
        for t, sub, col in ((r"the image", r"intensities", WORLD),
                            (r"primal sketch", r"edges, \ bars, \ blobs", LIKE),
                            (r"2$\tfrac{1}{2}$-D sketch", r"depth and slant at each point, \ as seen from here", PRIOR),
                            (r"3-D model", r"parts and their arrangement, \ in the object's own frame", POST)):
            b = RoundedRectangle(width=2.8, height=1.7, corner_radius=0.15, stroke_color=col, stroke_width=3)
            tt = label(t, font_size=26, color=col)
            ss = wrapped_label(sub, 2.5, 19, GREY_A)
            VGroup(tt, ss).arrange(DOWN, buff=0.15).move_to(b)
            boxes.add(VGroup(b, tt, ss))
        boxes.arrange(RIGHT, buff=0.55).move_to([0, 0.9, 0])
        arrows = VGroup(*[Arrow(boxes[k].get_right(), boxes[k + 1].get_left(), buff=0.05, color=GREY_B,
                                stroke_width=3) for k in range(3)])
        rows = rows_of([
            (r"each stage is a description, \ computed from the one before", WHITE),
            (r"only the last is invariant: \ the same mug from any angle", POST),
            (r"Marr's levels, \ from Part 1, \ came from this book: \ what is computed, \ how, \ and in what hardware", GREY_A),
        ], 12.4, 28, 0.3).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "David Marr, in a book published in 1982, two years after his death at thirty-five, proposed that vision "
            "builds a series of descriptions. <bookmark mark='a'/> From the image, a primal sketch: edges, bars and "
            "blobs, the kind of thing Part 13's cortical cells signal. From that, a two-and-a-half-D sketch: the depth "
            "and slant of the surface at each point, as seen from where you stand, built from stereo, shading, "
            "texture and motion. And from that, a 3-D model: the object's parts and how they're arranged, described "
            "in the object's own frame, not yours. <bookmark mark='b'/> Only that last description is invariant. A mug "
            "is a cylinder with a curved handle on its side from any viewpoint. <bookmark mark='c'/> The levels of "
            "explanation this series uses, what is computed, how, and in what hardware, come from the same book."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.8), LaggedStart(*[GrowArrow(a) for a in arrows],
                      lag_ratio=0.8), FadeIn(rows[0]), run_time=8.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Indicate(boxes[3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def parts(self):
        head = heading(r"Recognition by components")
        body = VGroup(Ellipse(width=1.8, height=0.5, color=POST, stroke_width=3).move_to([0, 0.9, 0]),
                      Line([-0.9, 0.9, 0], [-0.9, -0.9, 0], color=POST, stroke_width=3),
                      Line([0.9, 0.9, 0], [0.9, -0.9, 0], color=POST, stroke_width=3),
                      Arc(radius=0.9, start_angle=PI, angle=PI, color=POST, stroke_width=3).stretch(0.28, 1).move_to([0, -0.9 - 0.12, 0]))
        handle = Arc(radius=0.55, start_angle=-PI / 2, angle=PI, color=PRIOR, stroke_width=6).move_to([1.25, 0.05, 0])
        mug = VGroup(body, handle).move_to([-4.0, 0.0, 0])
        ml = label(r"a cylinder, \ with a curved tube on its side", font_size=22, color=GREY_A).next_to(mug, DOWN, buff=0.35)
        rows = rows_of([
            (r"1987: \ Biederman: \ objects described by a few dozen simple parts, \ geons, \ and how they join", WHITE),
            (r"a part's kind is visible from almost any view: \ straight or curved, \ parallel or tapering", POST),
            (r"delete a line drawing's joints and recognition fails; \ delete as much line midway, \ and it survives", PRIOR),
            (r"a theory with invariance built in, \ and with limits: \ faces and birds are not told apart by their parts", GREY_A),
            (r"the rival: \ a few remembered views \ (Bülthoff and Edelman, \ 1992); \ most now think both happen", LIKE),
        ], 7.2, 26, 0.32).move_to([2.6, 0.0, 0])
        keep_in_frame(rows)
        tag = note(r"drawn").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Irving Biederman made one version of the 3-D model concrete in 1987. <bookmark mark='a'/> His theory was "
            "that objects are recognized by their parts: a few dozen simple volumes he called geons, cylinders, "
            "blocks, cones, wedges, curved tubes, and how they're joined. A mug is a cylinder with a curved tube "
            "attached to its side. <bookmark mark='b'/> The advantage is that the kind of a part, whether its edges are "
            "straight or curved, parallel or tapering, can be seen from almost any viewpoint. <bookmark mark='c'/> One "
            "of his tests: delete pieces of the lines in a drawing of an object. If you delete the joints, where "
            "parts meet, recognition fails. Delete the same amount of line from the middles of the edges, and people "
            "still recognize the object. <bookmark mark='d'/> It's a theory with invariance built in. But it can't be "
            "the whole story: telling one face or one bird from another isn't a matter of their parts, which are "
            "the same. <bookmark mark='e'/> The rival view, from Heinrich Bülthoff and Shimon Edelman in 1992, is that "
            "we store a few remembered views of an object and interpolate between them. The usual resolution is that "
            "both happen: something like parts for telling a mug from a bowl, and something like views for telling one "
            "mug, or one face, from another."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(body), Create(handle), FadeIn(ml), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def speed(self):
        head = heading(r"How fast?")
        times = [(0, r"light", WORLD), (50, r"V1", LIKE), (80, r"V4", LIKE), (100, r"IT cortex", POST),
                 (150, r"brain responses differ: \ animal or not", PRIOR)]
        A = NumberLine(x_range=[0, 200, 50], length=11.0, include_numbers=True, font_size=24, color=GREY_B)
        A.move_to([0, 0.9, 0])
        al = label(r"milliseconds after the picture appears", font_size=22, color=GREY_B).next_to(A, DOWN, buff=0.45)
        marks = VGroup()
        for t, txt, col in times:
            dot = Dot(A.n2p(t), color=col, radius=0.08)
            lab = wrapped_label(txt, 2.4, 20, col).next_to(dot, UP, buff=0.2)
            marks.add(VGroup(dot, lab))
        rows = rows_of([
            (r"1996: \ Thorpe, \ Fize and Marlot: \ animal or no animal, \ in a photograph shown for 20 ms", WHITE),
            (r"the brain's responses to the two kinds of picture part at about 150 ms", PRIOR),
            (r"too fast for much back-and-forth: \ a first pass up the hierarchy can do a lot", POST),
        ], 12.4, 27, 0.3).to_edge(DOWN, buff=0.9)
        tag = note(r"latencies approximate; \ monkey for the areas, \ human for 150 ms").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Whatever the description, it's computed fast. <bookmark mark='a'/> In 1996, Simon Thorpe, Denis Fize and "
            "Catherine Marlot flashed photographs for twenty milliseconds and asked people whether each contained an "
            "animal. <bookmark mark='b'/> The electrical responses of the brain to animal and non-animal pictures "
            "began to differ about a hundred and fifty milliseconds after the picture appeared. "
            "<bookmark mark='c'/> In monkeys, signals reach primary visual cortex at about fifty milliseconds and the "
            "top of the object pathway, inferior temporal cortex, at about a hundred. That leaves time for little "
            "more than one pass up the hierarchy, each stage firing a few spikes. So a single feedforward sweep, with "
            "little feedback, must be able to do a lot. That's what made the next idea plausible: a deep network, "
            "which is exactly such a sweep."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Create(A), FadeIn(al))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[FadeIn(m) for m in marks[:4]], lag_ratio=0.5), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(marks[4]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
