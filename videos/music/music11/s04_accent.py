from __future__ import annotations

import numpy as np

from videos.music.music11.common import *  # noqa: F403


def marks_row(kind: str, n: int = 12, gap: float = 0.75) -> VGroup:
    """Twelve sounds, every third marked: by size (loud), by width (long) or by height (high)."""
    g = VGroup()
    for k in range(n):
        strong = k % 3 == 0
        if kind == "loud":
            m = Circle(radius=0.2 if strong else 0.1, stroke_width=0, fill_color=TUNE if strong else WEAK, fill_opacity=1.0)
        elif kind == "long":
            m = RoundedRectangle(width=0.62 if strong else 0.22, height=0.2, corner_radius=0.08, stroke_width=0, fill_color=TUNE if strong else WEAK, fill_opacity=1.0)
        else:
            m = Circle(radius=0.12, stroke_width=0, fill_color=TUNE if strong else WEAK, fill_opacity=1.0).shift(UP * (0.3 if strong else 0.0))
        m.shift(RIGHT * k * gap + (LEFT * 0.2 if kind == "long" and not strong else ORIGIN) * 0)
        if kind == "long":
            m.align_to(np.array([k * gap - 0.11, 0, 0]), LEFT)
        g.add(m)
    return g


class Accent(SoundScene):
    def construct(self):
        chapter(self, 3, r"Accent", r"What makes a beat strong?", extra=((1909, r"Woodrow's experiments"),))
        self.three()
        self.law()

    # ------------------------------------------------------------------
    def three(self):
        d = load("accent")
        c = clip("accent.three")
        rows = VGroup(*[marks_row(k) for k in ("loud", "long", "high")]).arrange(DOWN, buff=1.0, aligned_edge=LEFT).move_to(RIGHT * 0.9 + UP * 0.3)
        names = VGroup(*[label(t, font_size=30, color=GREY_A).next_to(r, LEFT, buff=0.5) for t, r in zip((r"louder", r"longer", r"higher"), rows)])
        note = listen_note(r"twelve tones, \ three times. \ Every third one is marked: \ by loudness, \ then by length, \ then by pitch", width=10.4, font_size=26).to_edge(DOWN, buff=0.4)
        plain = VGroup(*[Circle(radius=0.13, stroke_width=0, fill_color=WEAK, fill_opacity=1.0) for _ in range(12)]).arrange(RIGHT, buff=0.5).move_to(UP * 0.6)
        ask = label(r"twelve equal sounds. \ Which are the strong ones? \ The listener will decide, \ unless the musician does.", font_size=30, color=GREY_A).next_to(plain, DOWN, buff=0.7)
        with self.voiceover(
            "A listener will supply strong and weak beats unasked. A musician who wants a particular "
            "meter has to say which beats are the strong ones, and there are three plain ways to do it. "
            "<bookmark mark='a'/> Make a note louder than its neighbours. <bookmark mark='b'/> Make it "
            "longer. <bookmark mark='c'/> Or make it higher. Here are twelve tones, three times over, "
            "with every third one marked in each of those ways in turn."
        ) as vo:
            self.play(FadeIn(plain), FadeIn(ask))
            vo.wait_until("a")
            self.play(FadeOut(plain), FadeOut(ask))
            for mark, r, nm in zip("abc", rows, names):
                vo.wait_until(mark)
                self.play(FadeIn(r), FadeIn(nm), run_time=0.6)
            self.play(FadeIn(note))
        self.play(FadeOut(note))
        with self.listen(c) as snd:
            window(snd, r"groups of three, \ made three ways", kind="synthesized", detail=r"organ tones", corner=DL, tag_corner=DR)
            for key, r, nm in zip(("loud", "long", "high"), rows, names):
                ts = d["times"][key]
                pulse(snd, nm, ts[0], ts[-1] + 0.4, buff=0.1)
                for k, t in enumerate(ts):
                    snd.wait_until(t)
                    self.play(r[k].animate(rate_func=there_and_back).shift(UP * 0.14), run_time=0.2)
        with self.voiceover(
            "Each time you heard threes: a waltz with no tune. Musicians call the first kind a dynamic "
            "accent and the second an agogic accent, from a Greek word for leading. In real music the "
            "three usually agree, and a change of harmony or a low bass note agrees with them. When a "
            "composer sets them against each other, the meter becomes uncertain, and that is a resource "
            "too."
        ):
            self.play(*[Indicate(VGroup(*[r[k] for k in range(0, 12, 3)]), color=TUNE, scale_factor=1.15) for r in rows], run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def law(self):
        d = load("accent")
        c = clip("accent.law")
        card = listen_card(r"Two streams of sounds in pairs, \ fading in so that you cannot hear where they start. \\ A: \ loud and soft. \ \ B: \ long and short. \ \ In each, \ which sound begins the pair?", width=10.6, font_size=26)
        with self.voiceover(
            "Loudness and length do not do the same job, though. Listen to two streams of sounds in "
            "pairs. Each fades in, so you cannot hear where it starts. In A, loud and soft alternate. In "
            "B, long and short. In each stream, which sound begins the pair?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        bx = boxes(("A", "B"), buff=1.2, width=2.4, height=1.2, font_size=48).move_to(UP * 1.5)
        self.play(FadeOut(card), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", kind="synthesized", detail=r"organ tones", corner=DL, tag_corner=DR)
            pulse(snd, bx[0], snd.time_of("A"), snd.time_of("B") - 1.0)
            pulse(snd, bx[1], snd.time_of("B"), c.duration)
        a_row = VGroup(*[Circle(radius=0.2 if k % 2 == 0 else 0.1, stroke_width=0, fill_color=TUNE if k % 2 == 0 else WEAK, fill_opacity=1.0) for k in range(8)]).arrange(RIGHT, buff=0.3)
        b_row = VGroup(*[RoundedRectangle(width=0.22 if k % 2 == 0 else 0.62, height=0.2, corner_radius=0.08, stroke_width=0, fill_color=WEAK if k % 2 == 0 else TUNE, fill_opacity=1.0) for k in range(8)]).arrange(RIGHT, buff=0.3)
        a_row.move_to(LEFT * 3.3 + DOWN * 0.6)
        b_row.move_to(RIGHT * 3.3 + DOWN * 0.6)
        ba = VGroup(*[bracket(a_row[k].get_left()[0] - 0.08, a_row[k + 1].get_right()[0] + 0.08, a_row.get_y() - 0.5, color=TUNE) for k in range(0, 8, 2)])
        bb = VGroup(*[bracket(b_row[k].get_left()[0] - 0.08, b_row[k + 1].get_right()[0] + 0.08, b_row.get_y() - 0.5, color=TUNE) for k in range(0, 8, 2)])
        la = label(r"LOUD, \ soft: \ the loud sound begins", font_size=26, color=GREY_A).next_to(ba, DOWN, buff=0.3)
        lb = label(r"short, \ LONG: \ the long sound ends", font_size=26, color=GREY_A).next_to(bb, DOWN, buff=0.3)
        with self.voiceover(
            "Most listeners hear A as loud, soft; loud, soft. The loud sound begins the pair. "
            "<bookmark mark='a'/> And most hear B as short, long; short, long. The long sound ends the "
            "pair. <bookmark mark='b'/> Herbert Woodrow measured this in 1909, and it has held up since: "
            "a louder sound tends to start a group, and a longer sound tends to finish one. That is why "
            "a drummer marks the start of a bar with a stroke, and a melody marks the end of a phrase "
            "with a long note. The Tune does exactly that: six short notes and a long one. The half about "
            "length is the weaker of the two; it seems to depend on the rhythms of the language a "
            "listener grew up with."
        ) as vo:
            self.play(FadeIn(a_row), FadeIn(ba), FadeIn(la))
            vo.wait_until("a")
            self.play(FadeIn(b_row), FadeIn(bb), FadeIn(lb))
            vo.wait_until("b")
            self.play(Indicate(la, color=TUNE, scale_factor=1.05), Indicate(lb, color=TUNE, scale_factor=1.05))
        self.wait(0.4)
        self.clear_scene()
