from __future__ import annotations

import numpy as np

from videos.music.music10.common import *  # noqa: F403


def shape_plot(steps, color, width: float = 3.0, height: float = 1.5, levels: int = 6) -> VGroup:
    """A melody as dots at their heights, joined: what the signs do not say."""
    xs = np.linspace(-width / 2, width / 2, len(steps))
    grid = VGroup(*[Line([-width / 2 - 0.15, -height / 2 + k * height / (levels - 1), 0], [width / 2 + 0.15, -height / 2 + k * height / (levels - 1), 0], color=GREY_D, stroke_width=1) for k in range(levels)])
    pts = [np.array([x, -height / 2 + s * height / (levels - 1), 0]) for x, s in zip(xs, steps)]
    path = VMobject(color=color, stroke_width=2.5).set_points_as_corners(pts)
    dots = VGroup(*[Dot(p, radius=0.07, color=color) for p in pts])
    g = VGroup(grid, path, dots)
    g.dots = dots
    return g


class Neumes(SoundScene):
    def construct(self):
        chapter(self, 1, r"A reminder", r"What is the least you can write down?", extra=((900, r"neumes"),))
        self.signs()
        self.three()
        self.count()
        self.heights()

    # ------------------------------------------------------------------
    def signs(self):
        d = load("neumes")
        self.nm = nm = neumes(d["steps"], words=WORDS, width=10.0, size=0.6, word_size=34).move_to(UP * 1.5)
        where = label(r"signs over the words: \ the ninth century", font_size=26, color=GREY_A).to_edge(UP, buff=0.5)
        legend = VGroup(*[VGroup(neume_sign(k, 0.6), label(t, font_size=28, color=GREY_A)).arrange(RIGHT, buff=0.3)
                          for k, t in ((1, r"higher than the last note"), (0, r"the same note again"), (-1, r"lower"))]).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(DOWN * 1.6)
        with self.voiceover(
            "In the ninth century, in monasteries such as Saint Gall, scribes who were copying out the words "
            "of chants began to add small signs above the syllables. They are called neumes. Here is the "
            "first phrase of our Tune, marked in that way; I have simplified the signs to three. "
            "<bookmark mark='a'/> A rising stroke says: this note is higher than the last one. "
            "<bookmark mark='b'/> A dash: the same note again. <bookmark mark='c'/> A dot: lower."
        ) as vo:
            self.play(FadeIn(where), FadeIn(nm.words))
            self.play(LaggedStart(*[FadeIn(n, shift=DOWN * 0.1) for n in nm.notes], lag_ratio=0.2), run_time=2.0)
            for mark, row in zip("abc", legend):
                vo.wait_until(mark)
                self.play(FadeIn(row), run_time=0.5)
        self.wait(0.3)
        self.play(FadeOut(legend), FadeOut(where))

    # ------------------------------------------------------------------
    def three(self):
        d = load("neumes")
        c = clip("neumes.three")
        nm = self.nm
        card = listen_card(r"Three melodies. \ Which one do these signs describe?", width=8.4).move_to(DOWN * 1.0)
        with self.voiceover("Here are three melodies. Which one do these signs describe?"):
            self.play(FadeIn(card))
        self.wait(1.0)
        bx = boxes(("A", "B", "C"), buff=0.8, width=1.9, height=1.0, font_size=44).move_to(DOWN * 1.7)
        self.play(FadeOut(card), FadeIn(bx))
        times = d["times"]["A"] + d["times"]["B"] + d["times"]["C"]
        with self.listen(c) as snd:
            window(snd, r"three melodies", detail=r"Part 1's string", corner=DL, tag_corner=DR)
            for k, nmx in enumerate("ABC"):
                pulse(snd, bx[k], snd.time_of(nmx), snd.time_of(nmx) + 5.2)
            light(snd, list(nm.notes) * 3, times, base=PARCHMENT)
            for t in times:                                      # the sign steps as its note sounds
                snd.wait_until(t)
                k = times.index(t) % 7
                self.play(nm.notes[k].animate(rate_func=there_and_back).shift(UP * 0.1), run_time=0.25)
        for n in nm.notes:
            n.set_color(PARCHMENT)
        cols = [GREY_A, TUNE, GREY_A]
        plots = VGroup(*[VGroup(shape_plot(m, col), label(r" \ ".join(nmz), font_size=24, color=col)).arrange(DOWN, buff=0.25) for m, nmz, col in zip(d["melodies"], d["names"], cols)])
        plots.arrange(RIGHT, buff=0.7).move_to(DOWN * 1.5)
        tags = VGroup(*[label(t, font_size=30, color=col).next_to(p, UP, buff=0.2) for t, p, col in zip("ABC", plots, cols)])
        with self.voiceover(
            "All three. <bookmark mark='a'/> Each of them stays, rises, stays, rises, stays, and falls, "
            "exactly as the signs say. The second one is the Tune. The first leaps a fourth where the Tune "
            "leaps a fifth; the third ends by dropping a fourth where the Tune drops a step. The signs say "
            "which way the melody goes. They never say how far."
        ) as vo:
            self.play(FadeOut(bx))
            vo.wait_until("a")
            self.play(FadeIn(plots), FadeIn(tags))
        self.wait(0.4)
        self.play(FadeOut(plots), FadeOut(tags))

    # ------------------------------------------------------------------
    def count(self):
        d = load("neumes")
        rows = VGroup(
            VGroup(label(r"six notes to choose from", font_size=32, color=GREY_A), label(rf"{d['counts']['6']} melodies fit", font_size=40, color=TUNE)),
            VGroup(label(r"eight notes", font_size=32, color=GREY_A), label(rf"{d['counts']['8']} melodies fit", font_size=40, color=TUNE)),
            VGroup(label(r"the whole Tune, \ eight notes", font_size=32, color=GREY_A), label(r"{:,} fit".format(d["whole_tune_octave"]).replace(",", "{,}"), font_size=40, color=BAD)),
        )
        for r in rows:
            r.arrange(RIGHT, buff=0.5)
        rows.arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(DOWN * 0.9 + LEFT * 2.6)
        bits = VGroup(label(r"which way:", font_size=30, color=GREY_A), label(rf"{d['contour_bits']:.1f} bits", font_size=36, color=GOOD),
                      label(r"which notes:", font_size=30, color=GREY_A), label(rf"{d['pitch_bits']:.1f} bits", font_size=36, color=EAR)).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.3), cell_alignment=LEFT).move_to(DOWN * 2.9 + LEFT * 2.0)
        with self.voiceover(
            f"How many melodies fit? Monochord counted. If a singer has six notes to choose from, "
            f"{say(d['counts']['6'])} different melodies fit these seven signs. <bookmark mark='a'/> With "
            f"eight notes, {say(d['counts']['8'])}. <bookmark mark='b'/> And for the whole Tune, forty-two "
            "notes on the eight notes of an octave, more than three hundred million. <bookmark mark='c'/> "
            f"Measured in bits, the signs for this phrase carry about {say(d['contour_bits'], 1)}; naming "
            f"its notes would take {say(d['pitch_bits'], 1)}. Half the message is not there. So neumes were "
            "never a way to learn a tune. They reminded a singer of a tune already learned by ear, from "
            "another singer. The page helped the memory. It could not replace it."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(bits))
        self.wait(0.4)
        self.play(FadeOut(rows), FadeOut(bits))

    # ------------------------------------------------------------------
    def heights(self):
        d = load("neumes")
        nm = self.nm
        high = neumes(d["steps"], words=WORDS, width=10.0, size=0.6, word_size=34, heighted=0.3).move_to(nm.words.get_center(), aligned_edge=DOWN).align_to(nm.words, DOWN)
        lined = neumes(d["steps"], words=WORDS, width=10.0, size=0.6, word_size=34, heighted=0.3, line=3)
        lined.shift(high.words.get_center() - lined.words.get_center())
        fa = Text("F", font_size=30, color=RED_LINE, weight="BOLD").next_to(lined.line, LEFT, buff=0.15)
        year = label(r"about the year 1000", font_size=26, color=GREY_A).to_edge(DOWN, buff=0.6)
        self.play(nm.animate.shift(DOWN * 1.6), run_time=0.6)
        high.shift(DOWN * 1.6)
        lined.shift(DOWN * 1.6)
        fa.shift(DOWN * 1.6)
        with self.voiceover(
            "Then, around the year 1000, some scribes began to do something that seems obvious now. They "
            "wrote a sign higher on the page when its note was higher. <bookmark mark='a'/> Then someone "
            "scratched a line into the parchment to keep the heights honest, and inked it red, and wrote a "
            "letter beside it: this line is F. <bookmark mark='b'/> Now the height of a sign means "
            "something. One line fixes one note, and the notes near it can be judged by eye. The next "
            "idea belongs to one man. He added more lines."
        ) as vo:
            self.play(*[n.animate.move_to(h) for n, h in zip(nm.notes, high.notes)], FadeIn(year), run_time=2.0)
            vo.wait_until("a")
            self.play(Create(lined.line), FadeIn(fa), run_time=1.5)
            vo.wait_until("b")
            self.play(Indicate(lined.line, color=RED_LINE))
        self.wait(0.4)
        self.clear_scene()
