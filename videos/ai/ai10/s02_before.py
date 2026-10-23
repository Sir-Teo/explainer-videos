from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai10.common import (CNN, FMAP, HAND, HIST, KERNEL, PART, box_label, hbars, img_gray, img_rgb, load,
                                   pct)
from videos.ai.ai10.specs import ILSVRC


class Before(VoiceoverScene):
    def construct(self):
        self.card()
        self.cells()
        self.edges()
        self.hog()
        self.pipeline()
        self.compare()

    def card(self):
        card = chapter_card(1, r"Vision before deep learning",
                            r"What did a vision program look like before it learned its features?", lit=(2004,),
                            part=PART)
        with self.voiceover("Chapter one. Vision before deep learning."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def cells(self):
        def field(center, angle, size=1.0):
            box = Square(size, stroke_color=GREY_C, stroke_width=1.5, fill_color="#0B0F17", fill_opacity=1)
            on = Rectangle(width=size * 0.22, height=size * 0.95, stroke_width=0, fill_color=KERNEL,
                           fill_opacity=0.85)
            off1 = Rectangle(width=size * 0.2, height=size * 0.95, stroke_width=0, fill_color="#3D7FE0",
                             fill_opacity=0.6).shift(LEFT * size * 0.22)
            off2 = off1.copy().shift(RIGHT * size * 0.44)
            g = VGroup(box, off1, off2, on)
            VGroup(off1, off2, on).rotate(angle)
            return g.move_to(center)

        simple = VGroup(*[field([-4.6, y, 0], PI / 6) for y in (1.6, 0.0, -1.6)])
        sl = label(r"simple cells", font_size=24, color=KERNEL).next_to(simple, UP, buff=0.25)
        sn = label(r"the same angle, \\ three places", font_size=20, color=GREY_B).next_to(simple, DOWN, buff=0.2)
        cx = Circle(radius=0.5, stroke_color=FMAP, stroke_width=2.5, fill_color=FMAP, fill_opacity=0.15)
        cx.move_to([-0.8, 0, 0])
        cl = label(r"a complex cell", font_size=24, color=FMAP).next_to(cx, UP, buff=0.3)
        cn = label(r"fires if any of them does", font_size=20, color=GREY_B).next_to(cx, DOWN, buff=0.25)
        wires = VGroup(*[Arrow(s.get_right(), cx.get_left(), buff=0.1, stroke_width=2.5, color=GREY_B,
                               max_tip_length_to_length_ratio=0.12) for s in simple])
        legend_ = VGroup(
            VGroup(Square(0.25, stroke_width=0, fill_color=KERNEL, fill_opacity=0.85),
                   label(r"light here excites", font_size=20, color=GREY_A)).arrange(RIGHT, buff=0.15),
            VGroup(Square(0.25, stroke_width=0, fill_color="#3D7FE0", fill_opacity=0.6),
                   label(r"light here inhibits", font_size=20, color=GREY_A)).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DL, buff=0.35)
        hc = history_card(1962, r"Hubel \& Wiesel, \ \textit{J.\ Physiology}",
                          r"simple and complex cells; \ a hierarchy, \ layer upon layer; \ Nobel Prize, 1981",
                          width=5.0, color=HIST).move_to([4.2, 1.3, 0])
        idea = label(r"detect a feature, \\ then pool over position", font_size=28, color=WHITE)
        idea.next_to(hc, DOWN, buff=0.6)
        tag = note(r"schematic").to_corner(DR, buff=0.3)
        with self.voiceover(
            "In 1962 Hubel and Wiesel sorted the cells they found into two kinds. <bookmark mark='a'/> A simple "
            "cell responds to an edge or a bar at one angle, in one small patch of what the eye sees: light on its "
            "bright stripe excites it, light beside the stripe holds it back. <bookmark mark='b'/> A complex cell "
            "responds to the same angle anywhere in a larger patch, as if it collected several simple cells and "
            "fired when any of them did. <bookmark mark='c'/> Detect a feature, then pool over position, and do it "
            "again, layer upon layer. That picture won them a Nobel Prize in 1981, and it is, almost exactly, the "
            "design of the networks in this part."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s) for s in simple], lag_ratio=0.3), FadeIn(sl), FadeIn(sn),
                      FadeIn(legend_))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowArrow(w) for w in wires], lag_ratio=0.2), FadeIn(cx), FadeIn(cl),
                      FadeIn(cn))
            self.play(*[Indicate(s[3], color=WHITE) for s in simple], Flash(cx, color=FMAP), run_time=1.2)
            vo.wait_until("c")
            self.play(FadeIn(idea, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def edges(self):
        h = load("hog")
        d = np.asarray(h["digit"])
        gx, gy = np.asarray(h["digit_gx"]), np.asarray(h["digit_gy"])
        card = definition_card(r"The image gradient",
                               MathTex(r"\nabla I = \Big(\tfrac{\partial I}{\partial x}, \tfrac{\partial I}"
                                       r"{\partial y}\Big),\quad \tfrac{\partial I}{\partial x} \approx "
                                       r"I(x{+}1, y) - I(x{-}1, y)", font_size=30),
                               width=6.8, color=HAND).to_edge(UP, buff=0.35)
        digit = img_gray(d, 3.3).move_to([-3.4, -1.1, 0])
        dframe = SurroundingRectangle(digit, buff=0, color=GREY_D, stroke_width=1.2)
        cell = digit.width / 28
        arrows = VGroup()
        mag = np.hypot(gx, gy)
        top = float(mag.max())
        for i in range(1, 27, 2):
            for j in range(1, 27, 2):
                if mag[i, j] < 0.3 * top:
                    continue
                c = digit.get_corner(UL) + np.array([(j + 0.5) * cell, -(i + 0.5) * cell, 0])
                v = np.array([gx[i, j], -gy[i, j], 0]) / top * cell * 2.4
                arrows.add(Arrow(c - v / 2, c + v / 2, buff=0, stroke_width=3.5, color=HAND,
                                 max_tip_length_to_length_ratio=0.4, max_stroke_width_to_length_ratio=12,
                                 tip_length=0.1))
        dl = label(r"a test digit, \ and its gradient", font_size=20, color=GREY_B).next_to(digit, DOWN, buff=0.15)
        photo = img_rgb(np.asarray(h["photo"]), 2.6, smooth=False).move_to([1.6, -1.1, 0])
        sob = img_gray(np.asarray(h["photo_sobel"]), 2.6, color=HAND).move_to([4.7, -1.1, 0])
        pl = label(r"a CIFAR-10 photograph", font_size=20, color=GREY_B).next_to(photo, DOWN, buff=0.15)
        sl = label(r"$|\nabla I|$ \ (Sobel, 1968)", font_size=20, color=HAND).next_to(sob, DOWN, buff=0.15)
        arr = Arrow(photo.get_right(), sob.get_left(), buff=0.12, color=GREY_B, stroke_width=3)
        tag = note(r"computed").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Computer vision began the same way, with edges. An edge is where the brightness changes quickly, so "
            "take the derivative of the image. <bookmark mark='a'/> In practice, the difference between the "
            "pixels on either side, across and down. <bookmark mark='b'/> On a handwritten digit, each arrow points "
            "uphill in brightness, across the stroke. <bookmark mark='c'/> On a photograph, the length of the "
            "gradient, in Irwin Sobel's 1968 version, draws the outline of the horse. For decades every vision "
            "system started here."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(digit), Create(dframe), FadeIn(dl), FadeIn(tag))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.01), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(photo), FadeIn(pl))
            self.play(GrowArrow(arr), FadeIn(sob), FadeIn(sl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hog(self):
        h = load("hog")
        d = np.asarray(h["digit"])
        cells = np.asarray(h["digit_cells"])  # (4, 4, 9)
        digit = img_gray(d, 4.0, color=GREY_B).move_to([-3.2, -0.4, 0])
        cw = digit.width / 4
        grid = VGroup(*[Square(cw, stroke_color=GREY_C, stroke_width=1.2).move_to(
            digit.get_corner(UL) + np.array([(j + 0.5) * cw, -(i + 0.5) * cw, 0])) for i in range(4) for j in range(4)])
        vmax = cells.max()
        stars = VGroup()
        for i in range(4):
            for j in range(4):
                c = digit.get_corner(UL) + np.array([(j + 0.5) * cw, -(i + 0.5) * cw, 0])
                for k in range(9):
                    th = np.pi * (k + 0.5) / 9 + np.pi / 2  # the edge runs across the gradient
                    L = 0.45 * cw * cells[i, j, k] / vmax
                    if L < 0.02:
                        continue
                    v = L * np.array([np.cos(th), np.sin(th), 0])
                    stars.add(Line(c - v, c + v, color=HAND, stroke_width=3))
        dl = label(r"$4 \times 4$ cells of $7 \times 7$ pixels, \ $9$ orientations each", font_size=20,
                   color=GREY_B).next_to(digit, DOWN, buff=0.15)
        cards = VGroup(
            history_card(2004, r"David Lowe, \ SIFT", r"keypoints found at every scale; \ around each, "
                         r"$4 \times 4$ cells $\times$ $8$ orientations $= 128$ numbers", width=5.6, color=HIST),
            history_card(2005, r"Navneet Dalal \& Bill Triggs, \ HOG",
                         rf"histograms of oriented gradients in cells, \ normalized in blocks: \ here "
                         rf"${h['hog_dims']['mnist']}$ numbers per digit", width=5.6, color=HIST),
        ).arrange(DOWN, buff=0.35).move_to([3.5, -0.2, 0])
        tag = note(r"computed").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Then came the descriptors. Cut the image into cells, and in each cell count the edges by their "
            "angle, each one weighted by its strength. <bookmark mark='a'/> Here are those counts for our digit: "
            "each star is a histogram of nine orientations, the long spokes running along the strokes. "
            "<bookmark mark='b'/> David Lowe's SIFT, published in full in 2004, found distinctive points at every "
            "scale and described each one with 128 such counts. <bookmark mark='c'/> Navneet Dalal and Bill Triggs's "
            "histograms of oriented gradients, in 2005, covered the whole window, normalized block by block, and "
            "found pedestrians. Counted like this, an image survives small shifts and changes of lighting."
        ) as vo:
            self.play(FadeIn(digit), Create(grid), FadeIn(dl), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(s) for s in stars], lag_ratio=0.005), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pipeline(self):
        boxes = VGroup(box_label(r"pixels", GREY_B, font_size=26), box_label(r"hand-made features", HAND, font_size=26),
                       box_label(r"coding \& pooling", HAND, font_size=26),
                       box_label(r"a linear classifier", CNN, font_size=26)).arrange(RIGHT, buff=0.7)
        if boxes.width > 13.2:
            boxes.width = 13.2
        boxes.move_to(UP * 1.4)
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.08, color=GREY_B, stroke_width=3)
                          for a, b in zip(boxes, boxes[1:])])
        designed = Brace(VGroup(boxes[1], boxes[2]), DOWN, color=HAND)
        dlb = label(r"designed by people", font_size=24, color=HAND).next_to(designed, DOWN, buff=0.1)
        learned = Brace(boxes[3], DOWN, color=CNN)
        llb = label(r"learned", font_size=24, color=CNN).next_to(learned, DOWN, buff=0.1)
        win = VGroup(*[label(rf"ILSVRC {y}: \ {team}, \ ${err}\%$ \ ({how})", font_size=24, color=GREY_A)
                       for y, team, err, how in ILSVRC[:2]]).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        win.move_to(DOWN * 1.9)
        wl = label(r"the winners of the first two ImageNet contests \ (top-5 error)", font_size=22,
                   color=GREY_B).next_to(win, UP, buff=0.3)
        cite_ = cite(r"Russakovsky et al.\ (2015)", corner=DR)
        with self.voiceover(
            "By 2010 a good vision system was a pipeline. <bookmark mark='a'/> Pixels went in; hand-designed "
            "features came out, SIFT and its relatives, computed at thousands of places; they were coded, pooled "
            "into one long vector per image, and handed to a linear classifier, usually a support vector machine "
            "from Part 6. <bookmark mark='b'/> Only the last box learned from the data. Everything before it was "
            "designed by people, over decades. <bookmark mark='c'/> Systems like this won the first two ImageNet "
            "contests, in 2010 and 2011, missing the right answer, in five guesses, about a quarter of the time."
        ) as vo:
            self.play(FadeIn(boxes[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(b)) for a, b in zip(arrows, boxes[1:])],
                                  lag_ratio=0.6), run_time=3.0)
            vo.wait_until("b")
            self.play(GrowFromCenter(designed), FadeIn(dlb), GrowFromCenter(learned), FadeIn(llb))
            vo.wait_until("c")
            self.play(FadeIn(wl), LaggedStart(*[FadeIn(w, shift=UP * 0.1) for w in win], lag_ratio=0.4),
                      FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compare(self):
        h = load("hog")
        L = h["linear"]
        e = {k: L[k]["mean"] for k in L}
        top = 100 * max(e["mnist_pixels"], e["mnist_hog"], e["cifar_pixels"], e["cifar_hog"])
        rows = hbars([100 * e["mnist_pixels"], 100 * e["mnist_hog"]],
                     [r"raw pixels", r"HOG features"], [GREY_B, HAND], width=3.0, fmt=lambda v: rf"{v:.1f}\%",
                     font_size=24, vmax=top, height=0.5)
        rows2 = hbars([100 * e["cifar_pixels"], 100 * e["cifar_hog"]],
                      [r"raw pixels", r"HOG features"], [GREY_B, HAND], width=3.0, fmt=lambda v: rf"{v:.1f}\%",
                      font_size=24, vmax=top, height=0.5)
        g1 = VGroup(label(r"handwritten digits (MNIST)", font_size=28, color=WHITE), rows).arrange(DOWN, buff=0.45)
        g2 = VGroup(label(r"photographs (CIFAR-10)", font_size=28, color=WHITE), rows2).arrange(DOWN, buff=0.45)
        g1.move_to([-3.5, 0.5, 0])
        g2.move_to([3.5, 0.5, 0])
        for g in (g1, g2):
            keep_in_frame(g)
        head = label(r"the same linear classifier: \ test error", font_size=30).to_edge(UP, buff=0.45)
        tag = note(r"computed: \ logistic regression, \ three seeds each, \ mean").to_corner(DR, buff=0.25)
        gain = e["mnist_pixels"] / e["mnist_hog"]
        cw = e["cifar_hog"]
        if e["cifar_pixels"] - 0.03 > cw > 0.4:
            photo = (f"On the photographs it helps too, from {pct(e['cifar_pixels'], 0)} to {pct(cw, 0)} percent "
                     "wrong, but that is still wrong about as often as right.")
        elif cw < e["cifar_pixels"] - 0.03:
            photo = (f"On the photographs it helps too, from {pct(e['cifar_pixels'], 0)} to {pct(cw, 0)} percent "
                     "wrong, though photographs stay much harder than digits.")
        else:
            photo = (f"On the photographs it barely helps: {pct(e['cifar_pixels'], 0)} percent wrong on pixels, "
                     f"{pct(cw, 0)} on these features.")
        verdict = ("the gap between our digits and photographs is the gap the pipelines spent the 2000s on, with "
                   "far richer features than ours, and with far more images.")
        nxt = label(r"what if the features were learned too?", font_size=32, color=CNN).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "We can measure what the features buy. <bookmark mark='a'/> Train the same linear classifier twice, "
            "once on the raw pixels and once on our histograms of oriented gradients. On the digits, the pixels "
            f"give {pct(e['mnist_pixels'])} percent errors; the histograms, {pct(e['mnist_hog'])}, about "
            f"{gain:.0f} times fewer. <bookmark mark='b'/> " + photo + " <bookmark mark='c'/> The lesson of the "
            "era: " + verdict + " <bookmark mark='d'/> The question the rest of this part answers: what if the "
            "features were learned too?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(g1[0]), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.5))
            vo.wait_until("b")
            self.play(FadeIn(g2[0]), LaggedStart(*[FadeIn(r) for r in rows2], lag_ratio=0.5))
            vo.wait_until("d")
            self.play(FadeIn(nxt, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
