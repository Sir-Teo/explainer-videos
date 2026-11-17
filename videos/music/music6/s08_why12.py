from __future__ import annotations

import numpy as np

from videos.music.music6.common import *  # noqa: F403


class WhyTwelve(SoundScene):
    def construct(self):
        chapter(self, 7, r"Why twelve?", r"Is there something special about twelve notes to the octave?", lit=(1584,), extra=((1691, r"Huygens: \ thirty-one"), (1949, r"Partch: \ forty-three")))
        self.scan()
        self.fraction()
        self.others()
        self.partch()

    # ------------------------------------------------------------------
    def scan(self):
        d = load("why12")
        n, fifth, third = d["n"], d["fifth"], d["third"]
        g = axes([1, 61], [0, 42], x_length=11.0, y_length=3.6, xlabel=r"equal steps to the octave", ylabel=r"absolute cents from pure (capped at 42)", xticks=[5, 7, 12, 19, 31, 41, 53], yticks=[0, 10, 20, 30, 40], font_size=20)
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
            "So try them all. <bookmark mark='a'/> For each number of steps from four to sixty, the blue line is "
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
        cf = MathTex(r"\log_2(3/2) = \cfrac{1}{1 + \cfrac{1}{1 + \cfrac{1}{2 + \cfrac{1}{2 + \cfrac{1}{3 + \cdots}}}}}", font_size=30).move_to(LEFT * 3.4 + DOWN * 1.9)
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
            "ones in every octave. These familiar seven-note and five-note collections are not seven- and five-step equal temperaments. Many "
            "melodies use unequal steps derived from chains of fifths. The twelve-note "
            "keyboard contains approximations to both collections."
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
            "the sixteenth century. Each improves some important intervals over twelve, while changing others. Each also needs an unfamiliar keyboard or playing method that "
            "some musicians have chosen to learn. Twelve is not the best division of the octave. It is a compact compromise that "
            "became widely established."
        ) as vo:
            self.play(FadeOut(note))
            for mark, r in zip("abc", hist):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def partch(self):
        # Harry Partch's 43 ratios to the octave, as published in Genesis of a Music (2nd ed., 1974, ch. 8)
        ratios = ("1/1 81/80 33/32 21/20 16/15 12/11 11/10 10/9 9/8 8/7 7/6 32/27 6/5 11/9 5/4 14/11 9/7 21/16 4/3 27/20 "
                  "11/8 7/5 10/7 16/11 40/27 3/2 32/21 14/9 11/7 8/5 18/11 5/3 27/16 12/7 7/4 16/9 9/5 20/11 11/6 15/8 "
                  "40/21 64/33 160/81").split()
        assert len(ratios) == 43
        x0, w = -6.0, 12.0

        def X(cents):
            return x0 + w * cents / 1200.0

        def cents(r):
            p, q = (int(v) for v in r.split("/"))
            return 1200.0 * np.log2(p / q)

        card = history_card(1949, r"Harry Partch, \ \textit{Genesis of a Music}",
                            r"forty-three unequal steps to the octave, \ each a ratio of whole numbers up to eleven; \ "
                            r"then the instruments to play them", width=6.6).to_corner(UL, buff=0.4)
        axis = Line([X(0), 0, 0], [X(1200), 0, 0], color=GREY_D, stroke_width=2).shift(DOWN * 0.4)
        eq = VGroup(*[Line([X(100 * k), 0.15, 0], [X(100 * k), 0.75, 0], color=AIR, stroke_width=3) for k in range(13)]).shift(DOWN * 0.4)
        pa = VGroup(*[Line([X(cents(r)), -0.15, 0], [X(cents(r)), -0.75, 0], color=TUNE, stroke_width=2) for r in ratios + ["2/1"]]).shift(DOWN * 0.4)
        t12 = label(r"12 equal steps", font_size=26, color=AIR).next_to(eq, UP, buff=0.15).align_to(axis, LEFT)
        t43 = label(r"Partch's 43", font_size=26, color=TUNE).next_to(pa, DOWN, buff=0.15).align_to(axis, LEFT)
        keys = VGroup()
        for r, name in (("4/3", r"$\tfrac43$"), ("3/2", r"$\tfrac32$"), ("5/4", r"$\tfrac54$"), ("7/4", r"$\tfrac74$"), ("11/8", r"$\tfrac{11}{8}$")):
            keys.add(label(name, font_size=32, color=TUNE).move_to([X(cents(r)), axis.get_y() - 1.3, 0]))
        foot = label(r"every tuning in this part keeps some ratios and gives up others; \ Partch kept them, \ and built his own orchestra",
                     font_size=24, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "And some musicians left equal steps altogether. In 1949 the American composer Harry Partch published "
            "Genesis of a Music: forty-three unequal steps to the octave, every one a ratio of whole numbers up to "
            "eleven, and then he built the instruments to play them, from an adapted reed organ to marimbas and "
            "kitharas. <bookmark mark='a'/> Here are his steps against the twelve. They crowd together where the pure "
            "intervals are, around the fourth and the fifth and the thirds, and they include the seventh and eleventh "
            "partials that twelve cannot reach at all. <bookmark mark='b'/> Every tuning in this part keeps some ratios "
            "and gives up others. Partch kept them, and paid for it with an orchestra he had to build himself."
        ) as vo:
            self.play(FadeIn(card), Create(axis), FadeIn(t12), LaggedStart(*[Create(m) for m in eq], lag_ratio=0.05), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(t43), LaggedStart(*[Create(m) for m in pa], lag_ratio=0.03), run_time=2.0)
            self.play(LaggedStart(*[FadeIn(k, shift=UP * 0.1) for k in keys], lag_ratio=0.2), run_time=1.2)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()
