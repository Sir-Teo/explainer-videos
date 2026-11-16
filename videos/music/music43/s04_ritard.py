from __future__ import annotations

import numpy as np

from videos.music.music43.common import *  # noqa: F403

QC = {"1": BLUE, "2": TUNE, "3": EAR}


class Ritard(SoundScene):
    def construct(self):
        chapter(self, 3, r"Slowing down", r"Why does a final ritardando sound like a body coming to rest?")
        self.runners()
        self.model()
        self.hear()
        self.speech()
        self.todd()

    # ------------------------------------------------------------------
    def runners(self):
        items = [
            (r"Friberg and Sundberg \ (1999) \ measured runners stopping after a sprint, \ and ritardandi in recordings", WHITE),
            (r"a runner braking with constant force loses speed squared in proportion to distance", WHITE),
            (r"so speed falls as the square root of the distance left: \ fast at first, \ then a sudden settling", WHITE),
            (r"musicians' final ritardandi, \ measured against score position, \ follow nearly the same curve", TUNE),
            (r"tempo behaves like the speed of a body in motion", GREY_A),
        ]
        rows_scene(self, r"runners and ritardandi", items,
                   "In 1999 Anders Friberg and Johan Sundberg compared two things: runners stopping after a sprint, and final "
                   "ritardandi in recordings. <bookmark mark='b'/> A runner braking with constant force loses speed squared in "
                   "proportion to distance, <bookmark mark='c'/> so the speed falls as the square root of the distance left: "
                   "gently at first, then quickly at the very end. <bookmark mark='d'/> Musicians' final ritardandi, measured "
                   "against position in the score, follow nearly the same curve. <bookmark mark='e'/> Tempo behaves like the "
                   "speed of a body in motion.", marks="bcde")

    # ------------------------------------------------------------------
    def model(self):
        d = load("ritard")
        x = np.array(d["x"])
        x0, y0, W, H = -5.4, -1.9, 6.4, 3.4
        ax = VGroup(Line([x0, y0, 0], [x0 + W, y0, 0], color=GREY_B), Line([x0, y0, 0], [x0, y0 + H, 0], color=GREY_B))
        lines_ = VGroup()
        for q, ys in d["curves"].items():
            pts = [[x0 + W * xi, y0 + H * yi, 0] for xi, yi in zip(x, ys)]
            lines_.add(VMobject(color=QC[q], stroke_width=4).set_points_as_corners(pts))
        labs = VGroup(label(r"position in the ritardando", font_size=16, color=GREY_A).move_to([x0 + W / 2, y0 - 0.4, 0]),
                      label(r"tempo", font_size=16, color=GREY_A).move_to([x0 + 0.5, y0 + H + 0.3, 0]),
                      label(r"1", font_size=14, color=GREY_A).move_to([x0 - 0.2, y0 + H, 0]), label(rf"{d['w']}", font_size=14, color=GREY_A).move_to([x0 - 0.25, y0 + H * d["w"], 0]))
        eq = VGroup(label(r"$v(x) = \left[1 + (w^q - 1)\,x\right]^{1/q}$", font_size=30, color=WHITE),
                    label(r"x: \ position, \ 0 to 1; \ \ w: \ final tempo", font_size=18, color=GREY_A),
                    label(r"q = 1: \ tempo falls in a straight line", font_size=19, color=BLUE),
                    label(r"q = 2: \ constant braking force, \ the runner", font_size=19, color=TUNE),
                    label(r"q = 3: \ steeper still at the very end", font_size=19, color=EAR)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(RIGHT * 3.9 + UP * 0.2)
        eq.scale_to_fit_width(min(eq.width, 5.4)).move_to(RIGHT * 3.9 + UP * 0.2)
        head = label(r"the kinematic ritardando", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Their model is one formula. <bookmark mark='a'/> Tempo v, at position x through the ritardando, equals one plus "
            "w to the q minus one, times x, all to the power one over q, where w is the final tempo. <bookmark mark='b'/> With "
            "q equal to one, the tempo falls in a straight line. <bookmark mark='c'/> With q equal to two, it falls like the "
            "runner's speed under constant braking. <bookmark mark='d'/> With q equal to three, it holds on longer and drops "
            "more steeply at the very end. The recordings Friberg and Sundberg measured sat around q of two to three."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(labs))
            vo.wait_until("a")
            self.play(FadeIn(eq[:2]))
            for i, mark in enumerate("bcd"):
                vo.wait_until(mark)
                self.play(Create(lines_[i]), FadeIn(eq[2 + i]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("ritard")
        c = clip("ritard.three")
        tot = max(p["t"] + p["dur"] for v in d["perfs"].values() for p in v)
        rolls = VGroup(*[VGroup(label(rf"q = {q}", font_size=19, color=QC[q]), perf_roll(d["perfs"][q], width=9.0, height=0.9, lo=58, hi=68, total=tot, color=QC[q])).arrange(RIGHT, buff=0.4)
                         for q in ("1", "2", "3")]).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(UP * 0.2)
        cap = label(r"the Tune's last phrase, \ slowing over its whole length to half speed", font_size=18, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"three ways to stop", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Hear the Tune's last phrase slowing to half speed along the three curves, q equals one, two and three. Which "
            "one comes to rest most naturally?"
        ):
            self.play(FadeIn(head), FadeIn(rolls), FadeIn(cap))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"three ritardandi", detail=r"Part 7's piano, \ a plucked bass", corner=DL, tag_corner=DR)
            for i, q in enumerate(("1", "2", "3")):
                flash(snd, rolls[i][1].notes, [st[f"q{q}"] + p["t"] for p in d["perfs"][q]], hot=WHITE, base=QC[q])
                cursor(snd, rolls[i][1], st[f"q{q}"], 1.0)
        with self.voiceover(
            "In listening tests, ritardandi with q around two or three were preferred to the straight line, which tends "
            "to sound as if it brakes too early. The differences are tens of milliseconds a note, and the ear notices them."
        ):
            self.play(Indicate(rolls[1][0]), Indicate(rolls[2][0]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def todd(self):
        items = [
            (r"Neil Todd \ (1992): \ the phrase arch as motion \ --- \ tempo and loudness rise and fall together like speed", WHITE),
            (r"his model's tempo is the velocity of a mass pushed by the phrase structure", WHITE),
            (r"why should music move like a body? \ we hear it with brains that track motion \ (Part 46)", WHITE),
            (r"performers talk of `weight', \ `momentum' and `arrival'; \ the models take the words literally", TUNE),
            (r"chapter 4: \ loudness and articulation", GREY_A),
        ]
        rows_scene(self, r"music as motion", items,
                   "The idea goes further. <bookmark mark='b'/> Neil Todd modelled the whole phrase arch as motion: tempo and "
                   "loudness rising and falling together like speed. <bookmark mark='c'/> In his model the tempo is the velocity "
                   "of a mass pushed by the phrase structure. <bookmark mark='d'/> Why should music move like a body? Perhaps "
                   "because we hear it with brains that track motion, a question for Part 46. <bookmark mark='e'/> Performers "
                   "talk of weight, momentum and arrival; these models take the words literally. <bookmark mark='f'/> Chapter "
                   "four turns to loudness and articulation.", marks="bcdef")

    # ------------------------------------------------------------------
    def speech(self):
        items = [
            (r"speech slows at the ends of phrases too: \ the last syllable before a pause is lengthened", WHITE),
            (r"phrase-final lengthening is found in language after language", WHITE),
            (r"infants and adults use it to find where phrases end, \ in speech and in melodies", WHITE),
            (r"a performer's slowing at a phrase end may borrow a cue every listener already knows", TUNE),
            (r"Part 47 asks which features of music are shared with speech, \ and which are universal", GREY_A),
        ]
        rows_scene(self, r"slowing down in speech", items,
                   "Slowing at a boundary is not only musical. <bookmark mark='b'/> Speech slows at the ends of phrases too: the "
                   "last syllable before a pause is lengthened, <bookmark mark='c'/> in language after language. "
                   "<bookmark mark='d'/> Infants and adults use that lengthening to find where phrases end, in speech and in "
                   "melodies. <bookmark mark='e'/> A performer slowing at a phrase end may be borrowing a cue every listener "
                   "already knows. <bookmark mark='f'/> Part 47 asks which features of music are shared with speech, and which "
                   "are universal.", marks="bcdef")
