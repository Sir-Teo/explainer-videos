from __future__ import annotations

import numpy as np

from videos.psychology.psych14.common import *  # noqa: F403


def board_picture(d, key: str = "lum", height: float = 5.0):
    img = picture(np.asarray(d[key]), height, smooth=True, lo=0.0, hi=0.85)
    return img


def square_marker(img, d, rc, text, color):
    n = np.asarray(d["lum"]).shape[0]
    r, c = rc
    x = img.get_left()[0] + (c + 0.5) / n * img.width
    y = img.get_top()[1] - (r + 0.5) / n * img.height
    lab = label(text, font_size=34, color=color).move_to([x, y, 0])
    return lab, np.array([x, y, 0])


class Hook(VoiceoverScene):
    def construct(self):
        self.squares()
        self.reveal()
        self.question()
        self.objectives()

    def squares(self):
        d = load("shadow")
        head = heading(r"Two squares")
        img = board_picture(d).move_to([-3.2, -0.4, 0])
        la, pa = square_marker(img, d, d["A"], "A", WHITE)
        lb, pb = square_marker(img, d, d["B"], "B", BLACK)
        rows = rows_of([
            (r"a checkerboard, \ part of it in shadow", WHITE),
            (r"square A looks dark grey; \ square B looks light grey", YOU),
            (r"which is lighter? \ Most people do not hesitate", GREY_A),
        ], 5.2, 30, 0.4).move_to([3.6, 0.2, 0])
        keep_in_frame(rows)
        tag = VGroup(psyche_tag(r"computed: \ a checkerboard under a soft shadow"),
                     published_tag(rf"the demonstration: \ {archive.ADELSON_1995.cite}", corner=DL))
        with self.voiceover(
            "Look at this checkerboard. Part of it lies in a soft shadow. <bookmark mark='a'/> Square A, out in the "
            "light, is one of the dark squares. Square B, in the shadow, is one of the light ones. "
            "<bookmark mark='b'/> Which of the two is lighter? Most people don't hesitate."
        ) as vo:
            self.play(FadeIn(head), FadeIn(img), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(la), FadeIn(lb), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def reveal(self):
        d = load("shadow")
        head = heading(r"Now measure them")
        img = board_picture(d).move_to([-3.2, -0.4, 0])
        la, pa = square_marker(img, d, d["A"], "A", WHITE)
        lb, pb = square_marker(img, d, d["B"], "B", BLACK)
        grey = float(d["lum_A"]) / 0.85
        ca = Square(0.9, stroke_color=WORLD, stroke_width=3, fill_color=ManimColor.from_rgb([grey] * 3), fill_opacity=1)
        cb = ca.copy()
        pair = VGroup(ca, cb).arrange(RIGHT, buff=0.0).move_to([3.6, 1.3, 0])
        cap = label(r"A \ \ \ \ \ B", font_size=26, color=WORLD).next_to(pair, UP, buff=0.15)
        rows = rows_of([
            (rf"the light from A: \ {d['lum_A']:.2f}; \ from B: \ {d['lum_B']:.2f}", WORLD),
            (r"cut out of the picture and set side by side, \ they are the same grey", WHITE),
            (r"you did not see the light; \ you saw the surfaces, \ with the shadow taken out", POST),
        ], 5.2, 28, 0.36).move_to([3.6, -1.3, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ luminance at the two squares' centres")
        with self.voiceover(
            "Now measure them. <bookmark mark='a'/> The light coming from square A and the light coming from square "
            "B are the same: point four, in this picture's units. <bookmark mark='b'/> Cut them out and set them side "
            "by side, and they are the same grey. Edward Adelson made the classic version of this in 1995. "
            "<bookmark mark='c'/> You weren't seeing light. You were seeing surfaces, with the shadow taken out: A is a "
            "dark square in bright light, B a light square in shadow. That's what you saw, and it's correct about the "
            "board, and wrong about the picture."
        ) as vo:
            self.play(FadeIn(head), FadeIn(img), FadeIn(la), FadeIn(lb), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Indicate(la), Indicate(lb))
            vo.wait_until("b")
            self.play(TransformFromCopy(la, ca), TransformFromCopy(lb, cb), FadeIn(cap), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def question(self):
        head = heading(r"Seeing is a bet")
        rows = rows_of([
            (r"the image on the retina does not fix the world: \ many scenes could have made it", LIKE),
            (r"so the visual system must guess, \ using what it knows about how worlds usually are", PRIOR),
            (r"Helmholtz, \ 1867: \ unconscious inference", WHITE),
            (r"today's question: \ what is the bet, \ and how good is it?", YOU),
        ], 11.8, 32, 0.45).move_to([0, -0.2, 0])
        with self.voiceover(
            "The image on the back of your eye doesn't fix the world in front of it. <bookmark mark='a'/> Many "
            "different scenes could have produced exactly the same image. <bookmark mark='b'/> So the visual system has "
            "to guess, using what it knows about how worlds usually are: that light comes from above, that shadows have "
            "soft edges, that surfaces don't change colour where a shadow begins. <bookmark mark='c'/> Hermann von "
            "Helmholtz called it unconscious inference, in his handbook of physiological optics, completed in 1867. "
            "<bookmark mark='d'/> Today's question: what exactly is the bet, and how good is it? The surprising answer "
            "is that in some cases we can write down the best possible bet, and people come remarkably close to it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.15))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 14", font_size=34, color=GREY_B), label(r"Seeing as Inference", font_size=64))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"the inverse problem: \ why every image is ambiguous",
            r"grouping, \ depth from two eyes, \ and the constancies, \ with the illusions they produce",
            r"Bayes for perception: \ prior, \ likelihood, \ posterior, \ derived with Gaussians",
            r"cue combination, \ and priors you can see: \ light from above, \ slow motion",
            r"recognizing objects and faces, \ and deep networks as models of the ventral stream",
            r"headsets, \ camouflage, \ machine vision, \ and where priors come from",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 14 of Psychology, Built: seeing as inference. <bookmark mark='a'/> We'll start with the "
            "inverse problem, the reason every image is ambiguous. Then three things the visual system does about it: "
            "grouping, depth from two eyes, and the constancies, with the illusions they produce when they're applied "
            "in the wrong place. Then the mathematics of the bet, Bayes's rule for perception, derived with Gaussians; "
            "how two cues should be combined, and how people do combine them; and two priors you can see for yourself. "
            "Then recognizing objects and faces, and deep networks as models of the brain's object pathway. And at the "
            "end, virtual-reality headsets, camouflage, machine vision, and the open question of where priors come "
            "from."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=24.0)
        self.clear_scene()
