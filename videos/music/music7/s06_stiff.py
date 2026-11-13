from __future__ import annotations

import numpy as np

from videos.music.music7.common import *  # noqa: F403


class Stiff(SoundScene):
    def construct(self):
        chapter(self, 5, r"A string that is also a bar", r"What does a thick steel string do to its own partials?", lit=(1877,))
        self.sharp()
        self.quiz()
        self.cures()

    # ------------------------------------------------------------------
    def sharp(self):
        d = load("stiff")
        g = axes([0, 20.5], [0, 130], x_length=6.6, y_length=3.2, xlabel=r"partial number", ylabel=r"cents sharp of a whole multiple", xticks=[1, 5, 10, 15, 20], yticks=[0, 25, 50, 75, 100, 125], font_size=20)
        g.move_to(RIGHT * 3.0 + DOWN * 1.0)
        cu = curve_from(g, d["n"], d["cents"], STR)
        dots = VGroup(*[Dot(g.ax.c2p(n, c), radius=0.05, color=STR) for n, c in zip(d["n"], d["cents"])])
        semi = DashedLine(g.ax.c2p(0, 100), g.ax.c2p(20.5, 100), color=GREY_B, stroke_width=1.5)
        sl = label(r"a whole semitone", font_size=20, color=GREY_B).next_to(g.ax.c2p(6, 100), UP, buff=0.06)
        why = VGroup(label(r"an ideal string is pulled straight only by its tension", font_size=26, color=GREY_A),
                     label(r"a steel wire a millimetre thick also resists bending, \ like a bar", font_size=26, color=STR),
                     label(r"bending matters most for short waves: \ the high partials", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.14).to_edge(UP, buff=0.35)
        form = MathTex(r"f_n = n\,f_1\,\sqrt{\frac{1 + B\,n^2}{1 + B}}", font_size=36).move_to(LEFT * 3.7 + UP * 0.5)
        bval = label(rf"middle C: \ $B = {d['B']:.5f}$", font_size=26, color=STR).next_to(form, DOWN, buff=0.25)
        ask = pause_card(r"With $B = 0.00038$, \ how sharp is the tenth partial? \\ (1200 $\log_2$ of the factor gives cents.)", width=5.6, font_size=24).move_to(LEFT * 3.7 + DOWN * 2.1)
        c10 = float(d["cents"][9])
        ans = VGroup(MathTex(r"\sqrt{\tfrac{1.038}{1.0004}} = 1.0186", font_size=30), MathTex(rf"1200\log_2 1.0186 = {c10:.0f}\ \text{{cents}}", font_size=32, color=GOOD)).arrange(DOWN, buff=0.18).move_to(LEFT * 3.7 + DOWN * 2.1)
        with self.voiceover(
            "There is a second thing about a piano string that a guitar string hardly has. In Part 1 we saw "
            "that an ideal string is held straight by its tension alone. <bookmark mark='a'/> But a steel wire "
            "a millimetre thick also resists being bent, the way a bar does. And bending matters most where "
            "the string is most sharply curved: in the short waves, the high partials. So the high partials "
            "feel an extra stiffness, and vibrate a little faster than they should. <bookmark mark='b'/> The "
            "formula from Part 1: the n-th partial is n times the fundamental, times a factor that grows with "
            "n squared. The single number B says how stiff the string is. For our middle C it is about four "
            "parts in ten thousand. <bookmark mark='c'/> That sounds like nothing. Work it out for the tenth "
            "partial. Pause here."
        ) as vo:
            self.play(FadeIn(why[0]))
            vo.wait_until("a")
            self.play(FadeIn(why[1]), FadeIn(why[2]))
            vo.wait_until("b")
            self.play(FadeIn(form), FadeIn(bval))
            vo.wait_until("c")
            self.play(FadeIn(ask, shift=UP * 0.2))
        self.wait(1.5)
        with self.voiceover(
            f"A hundred times B is nought point nought three eight. The square root of the factor is one point "
            f"nought one eight six, and that is {say(c10)} cents: a third of a semitone. <bookmark mark='a'/> "
            f"Here are all of them. The seventh partial is {say(d['seventh_cents'])} cents sharp. The sixteenth "
            f"is {say(d['sixteenth_cents'])} cents sharp, most of a semitone. A piano string's partials are not "
            "a harmonic series. They are a stretched one."
        ) as vo:
            self.play(FadeOut(ask), FadeIn(ans))
            vo.wait_until("a")
            self.play(FadeIn(g), FadeIn(semi), FadeIn(sl), Create(cu), FadeIn(dots), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("stiff")
        c = clip("stiff.pair")
        q = listen_card(r"One piano note, \ twice. \ In one, \ the partials sit where a stiff string puts them. \\ In the other they have been moved onto exact whole multiples. \ Which is the real string?",
                        width=10.4, font_size=26).to_edge(UP, buff=0.35)
        bx = boxes(buff=2.6, width=3.0, height=1.4).move_to(DOWN * 0.5)
        with self.voiceover(
            "Can you hear it? Here is our middle C twice. In one version the partials are where the stiff "
            "string puts them. In the other, the same partials, with the same strengths and the same decays, "
            "have been moved onto exact whole multiples. Which is the real string?"
        ):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"middle C, \ twice", detail=r"partials stretched, \ or straightened", corner=DL, tag_corner=DR)
            for ev, b in zip("AB", bx):
                t0 = snd.time_of(ev)
                pulse(snd, b, t0, t0 + 2.4)
        ans = VGroup(label(r"straightened: \\ smooth, \ a little like an organ", font_size=26, color=AIR).next_to(bx[0], DOWN, buff=0.25),
                     label(r"the real string: \\ a slight shimmer and bite", font_size=26, color=STR).next_to(bx[1], DOWN, buff=0.25))
        with self.voiceover(
            "B was the real one. The difference is small on a single note in the middle of the keyboard: the "
            "real string has a faint shimmer, a liveliness, where the straightened one is smooth and a little "
            "dead, like an electric organ. Listeners asked to choose prefer some stretch: it is part of what "
            "says piano. In the bass, where the strings are thickest, it is far from small."
        ):
            self.play(FadeOut(q), FadeIn(ans))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cures(self):
        rows = rows_card([
            (r"the bass strings", r"a plain steel string for the lowest note would be seven metres long. \\ So a thin core is wrapped in copper: \ a thick string's mass, \ a thin one's stiffness."),
            (r"the size of the piano", r"a longer string can be thinner for the same note, \ so it is less stiff. \\ A concert grand is nearly three metres long for the sake of its bass strings."),
            (r"the tuning", r"octaves are tuned to the partials the strings really have: \\ the stretched octaves and Railsback's curve of Part 6."),
            (r"the scale itself", r"Part 5: \ a timbre with stretched partials has stretched consonances. \\ A piano is, \ very slightly, \ in a tuning of its own."),
        ], left=-6.5, text_left=-3.2, top=1.75, step=1.4, name_size=28, text_size=23, color=STR)
        head = label(r"Living with stiffness", font_size=38, color=GREY_A).to_edge(UP, buff=0.35)
        self.play(FadeIn(head), run_time=0.5)
        with self.voiceover(
            "Stiffness shapes the whole instrument. <bookmark mark='a'/> A plain steel string for the lowest "
            "note of a piano would have to be about seven metres long. So the bass strings are a thin steel "
            "core wrapped in copper wire: the wrapping adds mass, which lowers the pitch, without adding "
            "stiffness. <bookmark mark='b'/> It is why pianos are big. A longer string can be thinner for the "
            "same note, and so less stiff. A concert grand is nearly three metres long for the sake of its "
            "bass, and a small upright, with its short fat strings, can never sound like one. "
            "<bookmark mark='c'/> It decides the tuning: the stretched octaves of Part 6 are these partials, "
            "followed by a tuner's ear. <bookmark mark='d'/> And by Part 5, an instrument with stretched "
            "partials has stretched consonances. A piano is, very slightly, in a tuning of its own."
        ) as vo:
            for mark, r in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.3)
        self.clear_scene()
