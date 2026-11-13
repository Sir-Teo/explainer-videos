from __future__ import annotations

import numpy as np

from videos.music.music6.common import *  # noqa: F403


class WhyTwelve(SoundScene):
    def construct(self):
        chapter(self, 7, r"Why twelve?", r"Is there something special about twelve notes to the octave?", lit=(1584,), extra=((1691, r"Huygens: \ thirty-one"),))
        self.scan()
        self.fraction()
        self.others()

    # ------------------------------------------------------------------
    def scan(self):
        d = load("why12")
        n, fifth, third = d["n"], d["fifth"], d["third"]
        g = axes([1, 61], [0, 42], x_length=11.0, y_length=3.6, xlabel=r"equal steps to the octave", ylabel=r"cents from pure", xticks=[5, 7, 12, 19, 31, 41, 53], yticks=[0, 10, 20, 30, 40], font_size=20)
        g.move_to(DOWN * 0.5)
        keep = n >= 4
        n, fifth, third = n[keep], fifth[keep], third[keep]
        fb = VGroup(*[Line(g.ax.c2p(k, 0), g.ax.c2p(k, min(v, 42)), color=AIR, stroke_width=4) for k, v in zip(n, fifth)])
        tb = VGroup(*[Line(g.ax.c2p(k + 0.4, 0), g.ax.c2p(k + 0.4, min(v, 42)), color=GOOD, stroke_width=3) for k, v in zip(n, third)])
        leg = VGroup(label(r"its best fifth", font_size=24, color=AIR), label(r"its best major third", font_size=24, color=GOOD)).arrange(RIGHT, buff=0.8).to_edge(UP, buff=0.5)
        rec = VGroup(*[VGroup(Dot(g.ax.c2p(k, min(float(fifth[list(n).index(k)]), 42)) + UP * 0.12, radius=0.07, color=TUNE),
                              label(str(k), font_size=24, color=TUNE).move_to(g.ax.c2p(k, min(float(fifth[list(n).index(k)]), 42)) + UP * 0.42))
                       for k in d["record_fifths"] if k >= 5])
        with self.voiceover(
            "Why twelve? If the octave is going to be cut into equal steps, it could be cut into any number. "
            "So try them all. <bookmark mark='a'/> For each number of steps from two to sixty, the blue line is "
            "how far its best fifth is from pure. Most are hopeless. <bookmark mark='b'/> But a few numbers "
            "stand out, each with a better fifth than any smaller number: five, seven, twelve, twenty-nine, "
            "forty-one and fifty-three. Twelve has a fifth only two cents out, and nothing does better until "
            "twenty-nine. <bookmark mark='c'/> Now the thirds, in green. Twelve is mediocre: fourteen cents. "
            "Nineteen is better. Thirty-one has a third less than a cent from pure. And fifty-three has both "
            "its fifth and its third nearly perfect."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(b) for b in fb], lag_ratio=0.02), FadeIn(leg[0]), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(r) for r in rec], lag_ratio=0.4), run_time=4.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(b) for b in tb], lag_ratio=0.02), FadeIn(leg[1]), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fraction(self):
        d = load("why12")
        title = label(r"A worked example: \ where the good numbers come from", font_size=36).to_edge(UP, buff=0.4)
        need = VGroup(label(r"a fifth is the fraction \ $\log_2 \tfrac32 = 0.58496\ldots$ \ of an octave", font_size=30),
                      label(r"with $n$ equal steps, \ the fifth must be a whole number $m$ of them: \ $\tfrac{m}{n} \approx 0.58496$", font_size=28, color=GREY_A)).arrange(DOWN, buff=0.2).move_to(UP * 2.0)
        ask = pause_card(r"Which fraction with a small denominator is closest to 0.58496? \\ Try $\tfrac12$, \ $\tfrac35$, \ $\tfrac47$, \ $\tfrac7{12}$.", width=7.6).move_to(DOWN * 0.6)
        vals = VGroup(*[MathTex(rf"\tfrac{{{m}}}{{{n}}} = {m / n:.4f}", font_size=34, color=GOOD if n == 12 else WHITE) for m, n in ((1, 2), (3, 5), (4, 7), (7, 12))]).arrange(RIGHT, buff=0.7).move_to(UP * 0.4)
        cf = MathTex(r"0.58496 = \cfrac{1}{1 + \cfrac{1}{1 + \cfrac{1}{2 + \cfrac{1}{2 + \cfrac{1}{3 + \cdots}}}}}", font_size=30).move_to(LEFT * 3.4 + DOWN * 1.9)
        conv = VGroup(label(r"cut it off after each term:", font_size=24, color=GREY_B),
                      MathTex(r"\tfrac11,\ \ \tfrac12,\ \ \tfrac35,\ \ \tfrac7{12},\ \ \tfrac{24}{41},\ \ \tfrac{31}{53},\ \ \tfrac{179}{306}", font_size=36, color=TUNE),
                      label(r"the best fraction for its size, \ every time", font_size=24, color=GREY_B)).arrange(DOWN, buff=0.2).move_to(RIGHT * 2.9 + DOWN * 1.9)
        with self.voiceover(
            "Those numbers are not luck, and they can be found without trying every case. A fifth is a fixed "
            "fraction of an octave, when both are measured as logarithms: nought point five eight five. "
            "<bookmark mark='a'/> With n equal steps to the octave, the fifth has to be a whole number of steps. "
            "So we need a fraction with a small denominator that comes close to that number. Try a few. Which "
            "of these is closest?"
        ) as vo:
            self.play(FadeIn(title), FadeIn(need[0]))
            vo.wait_until("a")
            self.play(FadeIn(need[1]), FadeIn(ask, shift=UP * 0.2))
        self.wait(1.5)
        with self.voiceover(
            "A half is nought point five. Three fifths is point six. Four sevenths is point five seven one. "
            "Seven twelfths is point five eight three three, and that is the winner by a long way: seven steps "
            "out of twelve. <bookmark mark='a'/> There is a machine for producing these, called a continued "
            "fraction: write the number as one over one plus one over something, and repeat. "
            "<bookmark mark='b'/> Cut the expression off after each term, and you get, in order, the best "
            "possible fraction for its size. A half. Three fifths. Seven twelfths. Twenty-four forty-firsts. "
            "Thirty-one fifty-thirds. The denominators are the scales: five notes, twelve notes, forty-one, "
            "fifty-three. Twelve is the first division of the octave with a good fifth that a hand can still "
            "play. And look at the two before it. Five and seven. A keyboard has seven white keys and five black "
            "ones in every octave. The seven-note scale and the five-note scale, which between them carry most "
            "of the world's melodies, are the two earlier answers to the same question, and the twelve-note "
            "keyboard contains them both."
        ) as vo:
            self.play(FadeOut(ask), LaggedStart(*[FadeIn(v) for v in vals], lag_ratio=0.5), run_time=5.0)
            vo.wait_until("a")
            self.play(FadeIn(cf))
            vo.wait_until("b")
            self.play(FadeIn(conv))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def others(self):
        d = load("why12")
        c = clip("why12.triads")
        rows = {r["n"]: r for r in d["rows"]}
        note = listen_note(r"The major chord on C in 12, \ 19, \ 31 and 53 equal steps, \ and then pure. \\ Listen to how much each one shimmers.", width=9.6, font_size=26).to_edge(UP, buff=0.35)
        bx = boxes((r"12", r"19", r"31", r"53", r"pure"), buff=0.35, width=2.1, height=1.2, font_size=40).move_to(UP * 0.2)
        vals = VGroup(*[VGroup(label(rf"fifth {rows[n]['fifth_error']:+.1f}", font_size=22, color=AIR), label(rf"third {rows[n]['third_error']:+.1f}", font_size=22, color=GOOD)).arrange(DOWN, buff=0.06).next_to(b, DOWN, buff=0.2)
                        for n, b in zip((12, 19, 31, 53), bx)])
        with self.voiceover(
            "And the others are not just arithmetic. People have built them. Here is the major chord on C in "
            "twelve, nineteen, thirty-one and fifty-three equal steps, and then pure."
        ):
            self.play(FadeIn(note, shift=DOWN * 0.2), FadeIn(bx), FadeIn(vals))
        with self.listen(c) as snd:
            window(snd, r"a major chord in 12, 19, 31, 53 steps, \ then pure", kind="synthesized", detail=r"tones of seven partials", corner=DL, tag_corner=DR)
            for ev, b in zip(("n12", "n19", "n31", "n53", "pure"), bx):
                t0 = snd.time_of(ev)
                pulse(snd, b, t0, t0 + 2.0)
        hist = rows_card([
            (r"53", r"the Chinese theorist Jing Fang carried the fifths to fifty-three in the first century BC; \\ Nicholas Mercator proposed the equal division in the 1660s"),
            (r"31", r"Christiaan Huygens, \ 1691: \ almost exactly quarter-comma meantone, \ with no wolf; \\ an organ with 31 notes to the octave was built in the Netherlands in 1950"),
            (r"19", r"used by sixteenth-century experimenters: \ close to a meantone with pure minor thirds"),
        ], left=-6.4, text_left=-5.3, top=-1.5, step=0.95, name_size=32, text_size=22, color=TUNE)
        with self.voiceover(
            "Twelve shimmers. Nineteen is calmer, with a rather flat fifth. Thirty-one is close to still, and "
            "fifty-three can hardly be told from the pure chord. <bookmark mark='a'/> Fifty-three was reached "
            "by the Chinese theorist Jing Fang in the first century BC, who followed the fifths round until they "
            "almost closed. <bookmark mark='b'/> Thirty-one was worked out by Christiaan Huygens, who saw that "
            "it is quarter-comma meantone with the wolf removed; an organ with thirty-one notes to the octave "
            "was built in the Netherlands in 1950. <bookmark mark='c'/> Nineteen was tried by experimenters in "
            "the sixteenth century. Each of them is better in tune than twelve. And each needs a keyboard that "
            "nobody wants to learn. Twelve is not the best division of the octave. It is the smallest one that "
            "is good enough."
        ) as vo:
            self.play(FadeOut(note))
            for mark, r in zip("abc", hist):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.3)
        self.clear_scene()
