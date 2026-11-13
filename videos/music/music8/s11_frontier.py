from __future__ import annotations

import numpy as np

from videos.music.music8.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 10, r"Frontier: \ the parts we cannot yet compute", r"What do these models leave out, and who is working on it?", lit=(2009,), extra=((1996, r"shock waves found in trombones"),),
                spoken="Chapter 10. The frontier: the parts we cannot yet compute.")
        self.left_out()
        self.design()

    # ------------------------------------------------------------------
    def left_out(self):
        head = label(r"What this part's models leave out", font_size=38, color=EAR).to_edge(UP, buff=0.4)
        rows = rows_card([
            (r"the folds themselves", r"our voice began with a drawn pulse. \ Real folds are layers of soft tissue, \\ driven by the air between them; \ predicting one person's voice \\ from their anatomy is still out of reach."),
            (r"the player's own throat", r"a reed sits between two tubes: \ the instrument, \\ and the player's mouth and throat. \ Saxophonists reach \\ their highest notes by tuning the second one."),
            (r"loud brass", r"at full volume the wave in a trombone steepens as it travels, \ into a shock. \\ That is what ``brassy'' is, \ and no linear tube can do it."),
            (r"the jet", r"a flute's jet is turbulent air meeting a sharp edge. \\ Our two delays and a curve are a sketch of it, \ not a calculation."),
        ], left=-6.6, text_left=-2.6, top=1.9, step=1.45, name_size=26, text_size=22, color=EAR)
        self.play(FadeIn(head), run_time=0.5)
        with self.voiceover(
            "Every model in this part works, in the sense that it plays. Here is what they leave out. "
            "<bookmark mark='a'/> The voice began with a pulse that I drew. Real vocal folds are layers of "
            "soft tissue, driven by the air rushing between them and pushing back on it. The first "
            "mechanical model, two masses on springs, dates from 1972; today the folds are simulated in "
            "three dimensions, air and tissue together. But nobody can yet take a scan of a throat and "
            "predict the voice that will come out of it, which is what a surgeon would like to know before "
            "operating. <bookmark mark='b'/> Our reed had a tube on one side only. A real reed sits between "
            "two: the instrument, and the player's own mouth and throat. In 2008 measurements inside "
            "saxophonists' mouths showed that professionals reach the instrument's highest notes by tuning "
            "that second tube to them, and that amateurs who cannot play those notes do not. The glide at "
            "the opening of Gershwin's Rhapsody in Blue is played the same way. <bookmark mark='c'/> Our "
            "tubes are linear: a loud note is a soft note, scaled up. In a real trombone at full volume the "
            "pressure wave steepens as it travels, exactly as Part 2 said a loud enough wave must, and by "
            "the bell it is a shock wave. That was photographed in 1996. It is why loud brass sounds brassy, "
            "and our trumpet never will. <bookmark mark='d'/> And the flute's jet is turbulent air striking "
            "a sharp edge. Two delays and a curve are a sketch of that, not a calculation of it."
        ) as vo:
            for mark, r in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def design(self):
        d = load("lips")
        head = label(r"Instruments designed by calculation", font_size=38, color=GREY_A).to_edge(UP, buff=0.4)
        shape = bore_shape(d["profile_x"], d["profile_r"], width=8.0, height=1.3, color=BRASS).move_to(UP * 1.7)
        arrow = Arrow(UP * 0.9, UP * 0.1, color=GREY_B, buff=0, stroke_width=3)
        pk = d["peaks"]
        g = axes([0, 900], [0, 1], x_length=8.0, y_length=1.0, xlabel=r"its resonances (Hz)", ylabel="", xticks=[0, 200, 400, 600, 800], yticks=[], font_size=20).move_to(DOWN * 0.8)
        marks = VGroup(*[Line(g.ax.c2p(f, 0), g.ax.c2p(f, 0.9), color=BRASS, stroke_width=5) for f in pk if f < 880])
        rows = VGroup(label(r"shape $\rightarrow$ resonances: \ this part, \ a few lines of arithmetic", font_size=26, color=GOOD),
                      label(r"resonances $\rightarrow$ shape: \ run it backwards, \ thousands of times, \ and print the result", font_size=26, color=TUNE),
                      label(r"which resonances a player will \emph{like}: \ still nobody's to compute", font_size=26, color=EAR)).arrange(DOWN, buff=0.18, aligned_edge=LEFT).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "One frontier is moving quickly, and it uses exactly the tool of this part. Give Monochord a "
            "shape, and it returns the resonances. <bookmark mark='a'/> Makers once found the shape of a "
            "trumpet's bell by building trumpets. Now the calculation is run backwards: ask for the "
            "resonances you want, let a computer adjust the shape thousands of times until it has them, "
            "and print the instrument. Flutes with holes where no hand could reach, horns for players with "
            "one hand, copies of museum instruments too fragile to blow. <bookmark mark='b'/> What the "
            "computer cannot yet be told is what to aim for. Which set of resonances a player will find "
            "easy, and which a listener will find beautiful, is the same open question we met with the "
            "violins of Part 7, and it is still decided the old way: by playing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(shape), GrowArrow(arrow), FadeIn(g), FadeIn(marks), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(arrow.animate.rotate(np.pi), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
        self.wait(0.3)
        self.clear_scene()
