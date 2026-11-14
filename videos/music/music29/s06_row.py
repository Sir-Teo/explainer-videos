from __future__ import annotations

import numpy as np

from videos.music.music29.common import *  # noqa: F403


class Row(SoundScene):
    def construct(self):
        chapter(self, 5, r"The row and its forty-eight forms", r"What did Schoenberg put in place of the key?", extra=((1923, r"Schoenberg's first twelve-tone pieces"),))
        self.method()
        self.life()
        self.op25()
        self.matrix()
        self.quiz()
        self.webern()
        self.canon()
        self.webernlife()

    # ------------------------------------------------------------------
    def method(self):
        items = [
            (r"1921--23: \ Schoenberg's `method of composing with twelve tones related only to one another'", WHITE),
            (r"a row: \ all twelve pitch classes in a fixed order, \ none repeated until all have sounded", WHITE),
            (r"the row may be transposed, \ inverted, \ played backwards \ (retrograde), \ or backwards and inverted", WHITE),
            (r"melody and harmony both come from it: \ consecutive notes, \ or several sounded together", TUNE),
            (r"the Piano Suite, \ Op. 25 \ (1921--23), \ among the first pieces built wholly this way", GREY_A),
        ]
        rows_scene(self, r"the method", items,
                   "Schoenberg's answer came around 1921 to 1923. He called it a method of composing with twelve tones related "
                   "only to one another. <bookmark mark='c'/> A piece is built from a row: all twelve pitch classes in a fixed "
                   "order, none repeated before the others have sounded. <bookmark mark='d'/> The row may be transposed, "
                   "inverted, played backwards, which is called retrograde, or backwards and inverted. "
                   "<bookmark mark='e'/> Melody and harmony both come from it, as notes in succession or several sounded "
                   "together. <bookmark mark='f'/> His Piano Suite, Opus 25, is among the first pieces built wholly this way.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def matrix(self):
        d = load("row")
        m = d["matrix"]
        cells = VGroup()
        size = 0.36
        for r in range(12):
            for c_ in range(12):
                v = m[r][c_]
                sq = Square(side_length=size, stroke_width=0.6, stroke_color=GREY_B, fill_color=TUNE if r == 0 else (BLUE if c_ == 0 else BLACK), fill_opacity=0.35 if (r == 0 or c_ == 0) else 0.0)
                sq.move_to([-5.6 + size * c_, 1.9 - size * r, 0])
                cells.add(VGroup(sq, label(str(v), font_size=12, color=WHITE if (r == 0 or c_ == 0) else GREY_A).move_to(sq)))
        side = VGroup(*[label(s, font_size=21, color=c_) for s, c_ in (
            (r"across the top: \ the row, \ $P_0$", TUNE),
            (r"down the side: \ its inversion, \ $I_0$", BLUE),
            (r"each row of the grid: \ a transposition; \ each column: \ an inverted one", WHITE),
            (r"read right to left: \ retrogrades", WHITE),
            (rf"12 $\times$ 4 = 48 forms, \ all different for this row: \ {d['distinct']}", EAR))]).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 6.4))
        side.move_to(RIGHT * 3.0 + DOWN * 0.1)
        head = label(r"a row of our own, \ and its matrix \ (C = 0)", font_size=24, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Composers lay out a row's forms in a twelve by twelve grid. <bookmark mark='a'/> Across the top, the row itself, "
            "here one of our own, starting on C. <bookmark mark='b'/> Down the side, its inversion. <bookmark mark='c'/> "
            "Every row of the grid is then a transposition of the row, every column a transposition of its inversion, "
            "<bookmark mark='d'/> and reading right to left gives the retrogrades. <bookmark mark='e'/> Twelve "
            "transpositions of four kinds: forty-eight forms, and for this row all forty-eight are different."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells), run_time=1.5)
            for mark, r in zip("abcde", side):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("row")
        c = clip("row.quiz")
        card = listen_card(r"Our row, \ then two of its forms: \ the retrograde and the inversion, \ in some order. \ "
                           r"Which is the inversion, \ A or B? \ Listen to the second note.", width=10.4)
        with self.voiceover(
            "Listen. Our row, then two of its forms, its retrograde, played backwards, and its inversion, upside down, in some "
            "order. Which one is the inversion, A or B? A hint: listen to the second note, and compare it with the row's."
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        gP = mroll(d["P0"], width=3.6, height=1.6, lo=58, hi=73, color=GREY_A).move_to(LEFT * 4.4 + DOWN * 0.2)
        gA = mroll(d["R0"], width=3.6, height=1.6, lo=58, hi=73, color=GREY_A).move_to(DOWN * 0.2)
        gB = mroll(d["I0"], width=3.6, height=1.6, lo=58, hi=73, color=GREY_A).move_to(RIGHT * 4.4 + DOWN * 0.2)
        lP = label(r"the row", font_size=26, color=GREY_A).next_to(gP, UP, buff=0.3)
        la = label(r"A", font_size=36, color=GREY_A).next_to(gA, UP, buff=0.3)
        lb = label(r"B", font_size=36, color=GREY_A).next_to(gB, UP, buff=0.3)
        self.play(FadeOut(card), FadeIn(gP), FadeIn(gA), FadeIn(gB), FadeIn(lP), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"the row, \ A, \ B", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for g, k, n in ((gP, "P", "P0"), (gA, "A", "R0"), (gB, "B", "I0")):
                flash(snd, g.notes, [d["starts"][k] + x[1] * d["unit"] for x in d[n]], hot=WHITE, base=GREY_A)
            pulse(snd, lP, d["starts"]["P"], d["starts"]["A"] - 0.5, buff=0.08)
            pulse(snd, la, d["starts"]["A"], d["starts"]["B"] - 0.5, buff=0.08)
            pulse(snd, lb, d["starts"]["B"], c.duration, buff=0.08)
        ans = VGroup(label(r"A: \ the retrograde", font_size=22, color=BLUE).next_to(gA, DOWN, buff=0.35),
                     label(r"B: \ the inversion: \ B becomes C$\sharp$", font_size=22, color=TUNE).next_to(gB, DOWN, buff=0.35))
        with self.voiceover(
            "B is the inversion. The row's second note is B, a semitone below C, played here in the same octave; the "
            "inversion's second note is C sharp, a semitone above, and every later step is flipped the same way, counted "
            "in pitch classes. A is the row backwards, beginning on its last note, A."
        ):
            self.play(FadeIn(ans), gB.animate.set_color(TUNE), gA.animate.set_color(BLUE))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def webern(self):
        d = load("row")["webern"]
        v, k = d["voice"], d["clarinet"]
        g = voices_roll([v, k], width=11.4, height=3.6, colors=[TUNE, BLUE], bar_h=0.09).move_to(DOWN * 0.2)
        head = label(r"Webern, \ \textit{Dormi Jesu}, \ Op. 16 No. 2 \ (1924): \ a canon in inversion", font_size=25, color=GREY_A).to_edge(UP, buff=0.4)
        key = VGroup(label(r"gold: \ the voice", font_size=20, color=TUNE), label(r"blue: \ the clarinet, \ one bar ahead", font_size=20, color=BLUE)).arrange(RIGHT, buff=0.8).next_to(g, DOWN, buff=0.35)
        rows_ = VGroup(*[label(s, font_size=21, color=c_) for s, c_ in (
            (rf"{d['inverted']} of {d['intervals']} intervals: \ exactly inverted", EAR),
            (rf"{d['same_durations']} of {d['notes']} durations: \ the same", WHITE))]).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Webern took the method's symmetries further than anyone. In Dormi Jesu, a short Latin song for voice and "
            "clarinet from 1924, the program compares the two lines in the encoding. <bookmark mark='a'/> The clarinet "
            "starts a bar ahead, and the voice follows with the same line upside down: every one of its forty-five "
            "intervals is the clarinet's interval inverted, <bookmark mark='b'/> and every one of its forty-six durations "
            "is the same. It is a strict canon in inversion, from first note to last."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows_[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows_[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def canon(self):
        d = load("row")["webern"]
        c = clip("row.webern")
        v, k = d["voice"], d["clarinet"]
        g = voices_roll([v, k], width=11.4, height=3.6, colors=[TUNE, BLUE], bar_h=0.09).move_to(DOWN * 0.2)
        head = label(r"\textit{Dormi Jesu}, \ whole: \ a synthetic soprano and a bowed string for the clarinet", font_size=23, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Here it is, whole, from the encoding. The synthetic voice sings on oo rather than the Latin words, and Part 7's "
            "bowed string stands in for the clarinet, so the colours are not Webern's; the lines are. Listen for the "
            "clarinet's leaps answered, a bar later, by the voice leaping the other way."
        ):
            self.play(FadeIn(head), FadeIn(g))
        with self.listen(c) as snd:
            window(snd, r"\textit{Dormi Jesu}", kind="synthesized", detail=r"synthetic voice, \ bowed string", corner=DL, tag_corner=DR)
            flash_voices(snd, g, [v, k], 0.0, d["unit"], colors=[TUNE, BLUE])
            cursor(snd, g, 0.0, d["unit"])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def op25(self):
        d = load("op25")
        c = clip("op25.row")
        g = mroll(d["line"], width=9.0, height=2.2, lo=58, hi=73, color=TUNE, bar_h=0.14).move_to(UP * 0.2)
        x0 = g.frame.get_left()[0]
        W = g.frame.width
        braces = VGroup()
        names = [r"(0 2 3 6)", r"(0 1 4 6): \ all-interval", r"(0 1 2 3): \ chromatic"]
        for k in range(3):
            a, b = x0 + W * (4 * k) / 12, x0 + W * (4 * k + 4) / 12
            braces.add(VGroup(Line([a + 0.05, -1.2, 0], [b - 0.05, -1.2, 0], color=EAR, stroke_width=3),
                              label(names[k], font_size=18, color=EAR).move_to([(a + b) / 2, -1.6, 0])))
        head = label(r"Schoenberg's Piano Suite, \ Op. 25: \ its row", font_size=26, color=GREY_A).to_edge(UP, buff=0.45)
        cap = label(r"E to B$\flat$: \ the row begins and ends a tritone apart, \ and falls into three four-note groups", font_size=21, color=GREY_A).to_edge(DOWN, buff=1.1)
        with self.voiceover(
            "Here is the row of the Piano Suite, Opus 25, once up the keyboard: E, F, G, C sharp, F sharp, E flat, A flat, "
            "D, B, C, A, B flat. Schoenberg used it in groups of four notes: the second group is the all-interval tetrachord "
            "of chapter two, the third a chromatic cluster. And it begins and ends a tritone apart, E and B flat, a fact the "
            "suite exploits by starting forms of the row on either note."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(braces), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"the Op. 25 row", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            flash(snd, g.notes, [n[1] * d["unit"] for n in d["line"]], hot=WHITE, base=TUNE)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def life(self):
        items = [
            (r"Arnold Schoenberg, \ 1874--1951: \ largely self-taught, \ a painter as well as a composer", WHITE),
            (r"1925: \ professor at the Prussian Academy of Arts in Berlin", WHITE),
            (r"1933: \ dismissed as a Jew by the new regime; \ he left Germany and reaffirmed his Jewish faith", WHITE),
            (r"Los Angeles from 1934: \ teaching at USC and UCLA, \ a neighbour of film composers", TUNE),
            (r"he saw his method as continuing Bach and Brahms, \ not breaking with them", GREY_A),
        ]
        rows_scene(self, r"Schoenberg", items,
                   "Who was the man behind the method? <bookmark mark='b'/> Arnold Schoenberg was largely self-taught, and a painter as well as a composer. <bookmark mark='c'/> In 1925 he was appointed to teach composition at the Prussian Academy of Arts in Berlin. <bookmark mark='d'/> In 1933 the new regime dismissed him as a Jew; he left Germany and formally returned to the Jewish faith. <bookmark mark='e'/> From 1934 he lived in Los Angeles, teaching at the University of Southern California and at UCLA. <bookmark mark='f'/> He saw his method as continuing Bach and Brahms, not breaking with them; his essay on Brahms is called Brahms the Progressive.", marks="cdef")

    # ------------------------------------------------------------------
    def webernlife(self):
        items = [
            (r"Anton Webern, \ 1883--1945: \ a musicologist by training, \ a conductor of workers' choirs", WHITE),
            (r"his complete published works fill only a few hours", WHITE),
            (r"canons, \ palindromes, \ rows with internal symmetries", WHITE),
            (r"banned as `degenerate' under the Nazis; \ shot by an American soldier in 1945, \ in a tragic mistake", TUNE),
            (r"after the war, \ his music became the model for a generation", GREY_A),
        ]
        rows_scene(self, r"Webern", items,
                   "A word about Webern himself. <bookmark mark='b'/> He was trained as a musicologist and earned his living conducting, including workers' choirs in Vienna. <bookmark mark='c'/> His published works, all together, last only a few hours, <bookmark mark='d'/> full of canons, palindromes and rows with internal symmetries. <bookmark mark='e'/> Under the Nazis his music was banned as degenerate, and in September 1945, in occupied Austria, he was shot dead by an American soldier in a tragic mistake. <bookmark mark='f'/> After the war his music became the model for a whole generation.", marks="cdef")
