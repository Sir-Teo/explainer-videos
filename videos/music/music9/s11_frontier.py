from __future__ import annotations

import numpy as np

from videos.music.music9.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 10, r"Frontier: \ what the ear knows about things", r"What can be heard about an object, and what can be designed to be heard?", lit=(2009,), extra=((2015, r"instruments designed by optimization"),),
                spoken="Chapter 10. The frontier: what the ear knows about things.")
        self.hearing()
        self.design()

    # ------------------------------------------------------------------
    def hearing(self):
        head = label(r"Hearing what a thing is", font_size=38, color=EAR).to_edge(UP, buff=0.4)
        rows = rows_card([
            (r"what it is made of", r"wood, \ metal and glass are told apart less by their overtones \\ than by how fast each overtone dies: \ the material's own damping."),
            (r"how big it is", r"listeners judge the length of a dropped bar quite well, \\ and the shape of a struck plate only a little better than chance."),
            (r"which shapes \\ can be heard", r"Kac's question is still open for most outlines. \\ Nobody knows whether every smooth, \ convex drum has its own spectrum."),
            (r"a cymbal's crash", r"the cascade of energy through hundreds of modes can now be computed \\ from the plate's equations, \ slowly; \ nobody can yet play one."),
        ], left=-6.5, text_left=-2.9, top=1.9, step=1.42, name_size=26, text_size=23, color=EAR)
        self.play(FadeIn(head), run_time=0.5)
        with self.voiceover(
            "Kac asked what a mathematician could deduce from a spectrum. A different question is what an "
            "ordinary ear does deduce, and it is being worked on now. <bookmark mark='a'/> Tap a table, a "
            "glass, a saucepan. You know at once what each is made of. Experiments show that listeners rely "
            "less on where the overtones are than on how quickly each one dies away, because that is a "
            "property of the material and not of the shape. <bookmark mark='b'/> Size comes through too: "
            "people can judge the length of a dropped bar. Shape hardly does. Asked whether a struck plate "
            "is a circle, a square or a triangle, listeners do only a little better than guessing. "
            "<bookmark mark='c'/> The mathematics is unfinished as well. For most outlines nobody knows "
            "whether a drum's overtones pin down its shape. It is not even known whether every smooth, "
            "convex drum, an egg shape, say, has a spectrum all its own. <bookmark mark='d'/> And the "
            "cymbal of chapter seven. The flow of energy through its hundreds of modes can now be computed "
            "from the equations of a thin plate, at great cost, a few seconds of sound in hours. A cymbal "
            "you could play from a model in real time does not exist yet."
        ) as vo:
            for mark, r in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def design(self):
        d = load("bars")
        head = label(r"Running it backwards", font_size=38, color=GREY_A).to_edge(UP, buff=0.4)
        th = np.asarray(d["profile_marimba"][::4])
        xs = np.linspace(-3.2, 3.2, len(th))
        bar = Polygon(*[np.array([u, 1.75, 0]) for u in xs], *[np.array([u, 1.75 - 0.8 * t, 0]) for u, t in zip(xs, th)][::-1], stroke_color=WOODC, stroke_width=2.5, fill_color=WOODC, fill_opacity=0.3)
        m = d["marimba"]
        tl = MathTex(rf"1 : {m['ratios'][1]:.2f} : {m['ratios'][2]:.1f}", font_size=36, color=WOODC).next_to(bar, RIGHT, buff=0.5)
        rows = VGroup(label(r"shape $\rightarrow$ overtones: \ Bessel, \ Chladni, \ Ritz; \ this part's computations", font_size=26, color=GOOD),
                      label(r"overtones $\rightarrow$ shape: \ a knife, \ a lathe, \ a hammer; \ and now a computer", font_size=26, color=TUNE),
                      label(r"a major-third bell; \ bars in the shapes of animals, \ each one in tune", font_size=26, color=GREY_A),
                      label(r"the makers were solving Kac's problem all along, \ one instrument at a time", font_size=28, color=EAR)).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(DOWN * 1.3)
        with self.voiceover(
            "The other frontier is the makers' problem, turned over to machines. <bookmark mark='a'/> Going "
            "from a shape to its overtones is what this part has done all along. <bookmark mark='b'/> Going "
            "from the overtones you want to a shape that has them is what the knife, the lathe and the "
            "hammer did, slowly, by ear. Now a computer does the carving: it changes a shape a little, "
            "recomputes the modes, and keeps what helps. <bookmark mark='c'/> That is how the major-third "
            "bell was found. In 2015 a group of computer scientists used the same idea to design xylophone "
            "bars in the outlines of animals, each one cut so that its note and its first overtones are "
            "in tune, and built the instrument. <bookmark mark='d'/> The "
            "mathematicians asked whether a sound decides a shape, and found that it need not. The makers "
            "never needed it to. They only needed one shape with the right sound, and for three thousand "
            "years they have been finding one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bar), FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.wait(0.3)
        self.clear_scene()
