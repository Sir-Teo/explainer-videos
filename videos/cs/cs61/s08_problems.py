from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs7.compute import load as load7
from videos.cs.cs61.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load

_ONES = ("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen "
         "seventeen eighteen nineteen").split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def say(n) -> str:
    """A whole number as a speaker says it (British: 'three hundred and fifty')."""
    n = int(round(n))
    if n < 20:
        return _ONES[n]
    if n < 100:
        return _TENS[n // 10] + ("" if n % 10 == 0 else "-" + _ONES[n % 10])
    if n < 1000:
        return _ONES[n // 100] + " hundred" + ("" if n % 100 == 0 else " and " + say(n % 100))
    return say(n // 1000) + " thousand" + ("" if n % 1000 == 0 else " " + say(n % 1000))


def say1(x: float) -> str:
    """A number with one decimal, spoken: 'five point seven'."""
    whole, tenth = divmod(int(round(10 * x)), 10)
    return say(whole) + ("" if tenth == 0 else " point " + _ONES[tenth])


def box(text: str, color, size=19, w=None, h=0.6, fill=0.12):
    """A rounded box with a Tex caption (``\\\\`` for a second line)."""
    t = Tex(r"\begin{tabular}{@{}c@{}}" + text + r"\end{tabular}", font_size=size, color=WHITE)
    r = RoundedRectangle(width=w or t.width + 0.35, height=max(h, t.height + 0.2), corner_radius=0.1,
                         stroke_color=color, stroke_width=1.8, fill_color=color, fill_opacity=fill)
    if t.width > r.width - 0.15:
        t.width = r.width - 0.15
    t.move_to(r)
    return VGroup(r, t)


def pails(a: int, b: int, unit=0.15):
    """A four-quart and a nine-quart pail holding ``a`` and ``b`` quarts."""
    g = VGroup()
    for cap, v, w in ((4, a, 0.34), (9, b, 0.44)):
        out = Rectangle(width=w, height=cap * unit, stroke_color=GREY_B, stroke_width=1.6)
        water = Rectangle(width=w, height=max(v * unit, 0.001), stroke_width=0, fill_color=DATA,
                          fill_opacity=0.8 if v else 0).align_to(out, DOWN)
        num = label(str(v), font_size=18, color=DATA if v else GREY_C).next_to(out, DOWN, buff=0.06)
        g.add(VGroup(out, water, num))
    g.arrange(RIGHT, buff=0.18, aligned_edge=DOWN)
    return g


FR = load7("frontier")
TWO = load7("predictors")["table"]["the Job, chapter 1"]["rows"]["2-bit"]["accuracy"]
TAGE9 = FR["tage"][2]
PPM = FR["ppm"]["accuracy"]
AM = load7("amdahl")
ROWS = {r["part"]: r for r in load("ledger")["rows"]}
R13, R17, R60 = ROWS[13], ROWS[17], ROWS[60]
YEARS2 = math.log(2) / math.log(1.1)
# cycles per byte of the Job with Part 17's hash table: its cycles over the corpus size (Part 6's row gives both)
CPB17 = R17["cycles"] / (ROWS[6]["cycles"] / ROWS[6]["cycles_per_byte"])


class Problems(VoiceoverScene):
    def construct(self):
        self.card()
        self.hamming()
        self.compound()
        self.polya()
        self.headroom()
        self.ideal()

    def card(self):
        card = chapter_card(7, r"Finding problems", r"Which problem is worth your years?", lit=(1945, 1991),
                            extra=((1945, r"P\'olya: \ \textit{How to Solve It}"), (1966, r"Belady: \ the ideal cache"),
                                   (1986, r"Hamming: \ You and Your Research"), (1991, r"Wall: \ limits of ILP")),
                            part=PART)
        with self.voiceover("Chapter seven. Finding problems."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def hamming(self):
        head = label(r"Hamming: \ important means attackable", font_size=36).to_edge(UP, buff=0.3)
        x0, y0, w, h = -5.6, -2.7, 6.0, 5.0
        quads = VGroup()
        spec = [  # (column, row, text, colour)
            (0, 1, r"it would matter, \ but there is no attack: \ time travel, \ teleportation, \ antigravity",
             NO),
            (1, 1, r"it would matter, \ and you can see a way in: \ \textbf{important}", YES),
            (0, 0, r"neither", GREY_C),
            (1, 0, r"an attack, \ but it would not matter much: \ safe, \ and small", GREY_B),
        ]
        for k, (c, r, t, col) in enumerate(spec):
            strong = k < 2
            rect = Rectangle(width=w / 2, height=h / 2, stroke_color=GREY_D, stroke_width=1.5, fill_color=col,
                             fill_opacity=0.12 if strong else 0.04)
            rect.move_to([x0 + w / 4 + c * w / 2, y0 + h / 4 + r * h / 2, 0])
            txt = wrapped_label(t, w / 2 - 0.4, font_size=19, color=col if strong else GREY_A)
            quads.add(VGroup(rect, txt.move_to(rect)))
        xa = Arrow([x0, y0 - 0.05, 0], [x0 + w + 0.2, y0 - 0.05, 0], buff=0, color=GREY_B, stroke_width=2,
                   max_tip_length_to_length_ratio=0.03)
        ya = Arrow([x0 - 0.05, y0, 0], [x0 - 0.05, y0 + h + 0.2, 0], buff=0, color=GREY_B, stroke_width=2,
                   max_tip_length_to_length_ratio=0.03)
        xl = label(r"do you have an attack?", font_size=19, color=GREY_A).next_to(xa, DOWN, buff=0.1)
        yl = label(r"would it matter?", font_size=19, color=GREY_A).rotate(PI / 2).next_to(ya, LEFT, buff=0.1)
        lunch = VGroup(
            label(r"at lunch, \ with the chemists:", font_size=20, color=GREY_A),
            wrapped_label(r"1. \ What are the important problems of your field?", 5.4, font_size=20, color=WHITE),
            wrapped_label(r"2. \ What important problems are you working on?", 5.4, font_size=20, color=WHITE),
            wrapped_label(r"3. \ If it is not important, \ why are you working on it?", 5.4, font_size=20,
                          color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        keep = wrapped_label(r"great scientists keep ten to twenty important problems in mind, \ and when a new "
                             r"idea bears on one, \ they drop other things and go after it", 5.4, font_size=19,
                             color=YES)
        src = note(r"Hamming, \ \textit{You and Your Research}, \ a talk at Bellcore, \ 1986", font_size=17)
        VGroup(lunch, keep, src).arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "In 1986 Richard Hamming, who spent three decades at Bell Labs, gave a talk called You and Your "
            "Research. Its best-known story is about lunch. <bookmark mark='a'/> Hamming sat with the chemists and "
            "asked what the important problems of their field were. A week later he asked which important "
            "problems they were working on. And later still: if what you are doing is not important, why are you "
            "working on it? <bookmark mark='b'/> He was careful about what important means. "
            "<bookmark mark='c'/> Time travel, teleportation and antigravity would matter enormously, he said, but "
            "they are not important problems, because we have no attack. <bookmark mark='d'/> A problem is "
            "important when it would matter and you can see a way in. <bookmark mark='e'/> Great scientists, he "
            "observed, keep ten to twenty such problems in mind, and when a new idea bears on one, they drop "
            "other things and go after it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in lunch], lag_ratio=0.6), run_time=4)
            vo.wait_until("b")
            self.play(GrowArrow(xa), GrowArrow(ya), FadeIn(xl), FadeIn(yl),
                      *[FadeIn(q[0]) for q in quads])
            self.play(FadeIn(quads[2][1]), FadeIn(quads[3][1]))
            vo.wait_until("c")
            self.play(FadeIn(quads[0][1]))
            vo.wait_until("d")
            self.play(FadeIn(quads[1][1]), Indicate(quads[1][0], color=YES))
            vo.wait_until("e")
            self.play(FadeIn(keep))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compound(self):
        head = label(r"Knowledge compounds", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 20, 5], y_range=[0, 7, 1], x_length=5.6, y_length=4.0, tips=False,
                  axis_config={"color": GREY_C, "font_size": 18, "include_numbers": True}).to_edge(LEFT, buff=0.8)
        xl = label(r"years", font_size=18, color=GREY_A).next_to(ax, DOWN, buff=0.35)
        yl = label(r"output, \ relative", font_size=18, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        base = ax.plot(lambda n: 1.0, x_range=[0, 20], color=GREY_B, stroke_width=2.5)
        grow = ax.plot(lambda n: 1.1 ** n, x_range=[0, 20], color=YES, stroke_width=3)
        bl = label(r"the same ability", font_size=17, color=GREY_B).next_to(ax.c2p(20, 1), UP, buff=0.1).align_to(
            ax.c2p(20, 1), RIGHT)
        gl = label(r"ten percent more, \ compounding", font_size=17, color=YES).next_to(ax.c2p(17, 1.1 ** 17), LEFT,
                                                                                         buff=0.15)
        two = DashedLine(ax.c2p(0, 2), ax.c2p(YEARS2, 2), color=HEAD, stroke_width=2)
        drop = DashedLine(ax.c2p(YEARS2, 2), ax.c2p(YEARS2, 0), color=HEAD, stroke_width=2)
        dot = Dot(ax.c2p(YEARS2, 2), radius=0.07, color=HEAD)
        cols = {r"(1.1)^n": YES, r"2": HEAD}
        rows = VGroup(
            cmath(r"\frac{\text{output}_A}{\text{output}_B}", r"=", r"(1.1)^n", colors=cols, font_size=32),
            cmath(r"(1.1)^n", r"=", r"2", colors=cols, font_size=32),
            cmath(r"n \ln 1.1", r"=", r"\ln 2", colors=cols, font_size=32),
            cmath(r"n", r"=", r"\frac{\ln 2}{\ln 1.1}", r"\approx", r"\frac{0.693}{0.0953}", r"\approx",
                  rf"{YEARS2:.1f}", colors=cols, font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        rows.next_to(ax, RIGHT, buff=1.0).align_to(ax, UP).shift(UP * 0.3)
        whys = VGroup(label(r"each year builds on the last", font_size=17, color=GREY_B),
                      label(r"when is it twice as much?", font_size=17, color=GREY_B),
                      label(r"take logarithms", font_size=17, color=GREY_B),
                      label(r"just over seven years", font_size=17, color=GREY_B))
        for wl, r in zip(whys, rows):
            wl.next_to(r, DOWN, buff=0.08).align_to(r, LEFT)
        ill = note(r"illustrative: \ Hamming's metaphor, \ taken literally", font_size=16).next_to(
            xl, DOWN, buff=0.1).align_to(ax, LEFT)
        habits = wrapped_label(r"also from the talk: \ keep the door open, \ for the clues that interruptions "
                               r"bring; \ keep Friday afternoons for great thoughts", 12.4, font_size=20,
                               color=WHITE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Hamming said that knowledge and productivity are like compound interest: of two people of about the "
            "same ability, one who works ten percent more will, over a career, produce more than twice as much. "
            "<bookmark mark='a'/> Take the metaphor literally, as an illustration: grow ten percent a year on top "
            "of what you already have, and after n years the ratio is one point one to the n. "
            "<bookmark mark='b'/> When is that two? <bookmark mark='c'/> Take logarithms: n times the log of one "
            "point one equals the log of two. <bookmark mark='d'/> So n is about nought point six nine three over "
            "nought point nought nine five: just over seven years. <bookmark mark='e'/> The talk has other habits "
            "too: keep your door open, for the clues that interruptions bring, and keep Friday afternoons for "
            "great thoughts."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(ill))
            vo.wait_until("a")
            self.play(Create(base), FadeIn(bl))
            self.play(Create(grow), FadeIn(gl), Write(rows[0]), FadeIn(whys[0]), run_time=2)
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]), Create(two))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[2].copy(), rows[3]), FadeIn(whys[3]))
            self.play(Create(drop), FadeIn(dot))
            vo.wait_until("e")
            self.play(FadeIn(habits))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def polya(self):
        head = label(r"P\'olya: \ \textit{How to Solve It} \ (1945)", font_size=36).to_edge(UP, buff=0.3)
        phases = VGroup(box(r"understand \\ the problem", HEAD, w=2.6, h=0.8),
                        box(r"devise \\ a plan", DATA, w=2.6, h=0.8),
                        box(r"carry \\ it out", KERN, w=2.6, h=0.8),
                        box(r"look \\ back", YES, w=2.6, h=0.8)).arrange(RIGHT, buff=0.55)
        phases.next_to(head, DOWN, buff=0.35)
        parr = VGroup(*[Arrow(phases[i].get_right(), phases[i + 1].get_left(), buff=0.05, color=GREY_B,
                              stroke_width=2, max_tip_length_to_length_ratio=0.35) for i in range(3)])
        back = CurvedArrow(phases[3].get_bottom() + DOWN * 0.05, phases[0].get_bottom() + DOWN * 0.05,
                           angle=-PI / 8, color=GREY_C, stroke_width=1.6, tip_length=0.15)
        heur = VGroup(*[label(t, font_size=19, color=DATA) for t in (
            r"a related problem?", r"a special case?", r"a generalization?", r"draw a figure",
            r"work backwards")]).arrange(RIGHT, buff=0.45)
        heur.next_to(back, DOWN, buff=0.12)
        q = label(r"bring up exactly 6 quarts, \ with a 4-quart pail and a 9-quart pail", font_size=21,
                  color=WHITE).next_to(heur, DOWN, buff=0.35)
        states = [(0, 9), (0, 1), (1, 0), (1, 9), (4, 6)]
        caps = [r"fill the 9", r"pour off 4, \ twice", r"move the 1", r"fill the 9 again", r"pour 3: \ \textbf{6}"]
        cells = VGroup()
        for (a, b), cp, i in zip(states, caps, range(5)):
            p = pails(a, b)
            t = label(cp, font_size=19, color=YES if i == 4 else GREY_A).next_to(p, DOWN, buff=0.12)
            cells.add(VGroup(p, t))
        ybot = q.get_bottom()[1] - 0.45 - cells[0][0].height
        for i, c in enumerate(cells):
            c.shift(np.array([-5.2 + 2.6 * i, ybot, 0]) - np.array([c[0].get_x(), c[0].get_bottom()[1], 0]))
        backs = VGroup(*[Arrow(cells[i + 1][0].get_left(), cells[i][0].get_right(), buff=0.12, color=HEAD,
                               stroke_width=2.5, max_tip_length_to_length_ratio=0.3) for i in range(4)])
        whyb = [r"$6 = 9 - 3$", r"the 4 takes 3 \\ if it holds 1", r"", r"$1 = 9 - 4 - 4$"]
        notes_b = VGroup()
        for i, t in zip((3, 2, 1, 0), whyb):
            m = Tex(r"\begin{tabular}{@{}c@{}}" + t + r"\end{tabular}", font_size=17, color=HEAD) if t else \
                VectorizedPoint()
            notes_b.add(m.next_to(backs[i], UP, buff=0.08))
        fwd = label(r"read it forwards: \ the solution", font_size=19, color=YES).to_corner(DR, buff=0.3)
        part2 = label(r"Part 2 searched every state of a jug puzzle; \ working backwards needs none",
                      font_size=18, color=GREY_B).to_corner(DL, buff=0.3)
        with self.voiceover(
            "George Pólya's How to Solve It, from 1945, is a short book about finding solutions. "
            "<bookmark mark='a'/> It has four phases: understand the problem, devise a plan, carry it out, and look "
            "back. <bookmark mark='b'/> For the plan, it offers questions. Do you know a related problem? A special "
            "case, or a more general one? Can you draw a figure, or work backwards? <bookmark mark='c'/> Pólya's "
            "own example: bring up exactly six quarts of water with a four-quart pail and a nine-quart pail. Start "
            "from the goal. <bookmark mark='d'/> Six in the big pail is nine less three. <bookmark mark='e'/> The "
            "small pail takes exactly three if it already holds one. <bookmark mark='f'/> And one is nine less "
            "four, less four again. <bookmark mark='g'/> Read the chain forwards: that is the solution. Part 2 "
            "searched every state of a jug puzzle; working backwards needs no search."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in phases], lag_ratio=0.4), Create(parr), run_time=2.5)
            self.play(Create(back))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(h, shift=UP * 0.1) for h in heur], lag_ratio=0.4), run_time=2.5)
            self.play(Indicate(heur[4], color=HEAD))
            vo.wait_until("c")
            self.play(FadeIn(q), FadeIn(cells[4]))
            vo.wait_until("d")
            self.play(GrowArrow(backs[3]), FadeIn(notes_b[0]), FadeIn(cells[3]))
            vo.wait_until("e")
            self.play(GrowArrow(backs[2]), FadeIn(notes_b[1]), FadeIn(cells[2]))
            vo.wait_until("f")
            self.play(GrowArrow(backs[1]), FadeIn(cells[1]))
            self.play(GrowArrow(backs[0]), FadeIn(notes_b[3]), FadeIn(cells[0]))
            vo.wait_until("g")
            self.play(LaggedStart(*[Indicate(c[0], color=YES) for c in cells], lag_ratio=0.3), FadeIn(fwd),
                      FadeIn(part2), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def headroom(self):
        head = label(r"Limit studies: \ how much is left?", font_size=36).to_edge(UP, buff=0.3)
        wrong = [(r"2-bit counters, \ $\tfrac14$ KB", 100 * (1 - TWO), GREY_B),
                 (rf"TAGE, \ {TAGE9['kb']:.0f} KB", 100 * (1 - TAGE9["accuracy"]), YES),
                 (r"no storage limit", 100 * (1 - PPM), HEAD)]
        sc = 0.62
        x0 = -6.6
        bars = VGroup()
        for i, (t, v, c) in enumerate(wrong):
            y = 1.6 - 0.95 * i
            nm = label(t, font_size=18, color=c).move_to([x0, y + 0.36, 0], aligned_edge=LEFT)
            r = Rectangle(width=v * sc, height=0.34, stroke_width=0, fill_color=c, fill_opacity=0.75).move_to(
                [x0, y, 0], aligned_edge=LEFT)
            val = label(rf"{v:.1f}\%", font_size=18, color=c).next_to(r, RIGHT, buff=0.1)
            bars.add(VGroup(nm, r, val))
        cap = label(r"the Job's branches mispredicted \ (Part 7)", font_size=18, color=GREY_A).next_to(
            bars, UP, buff=0.2).align_to([x0, 0, 0], LEFT)

        def bracket(a, b, y, text, color):
            ln = Line([x0 + a * sc, y, 0], [x0 + b * sc, y, 0], color=color, stroke_width=3)
            ticks = VGroup(*[Line([x, y - 0.08, 0], [x, y + 0.08, 0], color=color, stroke_width=3)
                             for x in (x0 + a * sc, x0 + b * sc)])
            t = label(text, font_size=17, color=color).next_to(ln, DOWN, buff=0.08).align_to(ln, LEFT)
            return VGroup(ln, ticks, t)
        w0, w1, w2 = (v for _, v, _ in wrong)
        yb = bars[2].get_bottom()[1] - 0.35
        br1 = bracket(w2, w1, yb, r"headroom from storage", YES)
        br2 = bracket(0, w2, yb - 0.75, r"needs a different kind of predictor", NO)
        cols = {r"\frac{1}{1 - p}": YES, r"350": YES}
        rows = VGroup(
            cmath(r"S", r"=", r"\frac{1}{(1 - p) + p / s}", colors=cols, font_size=30),
            cmath(r"S", r"\to", r"\frac{1}{1 - p}", r"\quad (s \to \infty)", colors=cols, font_size=30),
            cmath(rf"1 - p = {1 - AM['job_scan_share']:.6f}", r"\ \Rightarrow\ ", r"S \le",
                  rf"{AM['job_limit']:.0f}", colors=cols, font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        rows[2][3].set_color(YES)
        rows.move_to([3.6, 1.0, 0])
        whys = VGroup(label(r"Amdahl: \ a fraction $p$ of the work, \ $s$ times faster", font_size=17, color=GREY_B),
                      label(r"the limit: \ that part costs nothing", font_size=17, color=GREY_B),
                      label(r"the Job's linear search \ (Part 7)", font_size=17, color=GREY_B))
        for wl, r in zip(whys, rows):
            wl.next_to(r, DOWN, buff=0.08).align_to(r, LEFT)
        led = wrapped_label(rf"the ledger: \ {R13['seconds']:.0f} s in Part 13, \ {R17['seconds']:.2f} s with Part "
                            rf"17's hash table: \ about {R13['seconds'] / R17['seconds']:.0f} times", 5.6,
                            font_size=19, color=WHITE).next_to(whys[2], DOWN, buff=0.35).align_to(rows, LEFT)
        with self.voiceover(
            "A limit study measures the headroom before you spend years chasing it. <bookmark mark='a'/> Part 7 "
            f"asked how good branch prediction could be on the Job. Two-bit counters mispredict {say1(w0)} "
            f"branches in a hundred; our TAGE, at nine kilobytes, {say1(w1)}. <bookmark mark='b'/> With no storage "
            f"limit at all, {say1(w2)}. So storage alone can win about three more in a hundred, and the rest needs "
            "a different kind of predictor. <bookmark mark='c'/> Amdahl's law is a limit study in one line: make a "
            "fraction p of the work s times faster. <bookmark mark='d'/> Let s grow without bound, and the gain is "
            "capped at one over one minus p. <bookmark mark='e'/> The Job spent ninety-nine point seven percent of "
            "its instructions in one linear search, so removing it could give at most "
            f"{say(AM['job_limit'])} times. <bookmark mark='f'/> The ledger shows the headroom was real: "
            f"{say(R13['seconds'])} seconds in Part 13, under a second with Part 17's hash table."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(bars[0][0]), GrowFromEdge(bars[0][1], LEFT), FadeIn(bars[0][2]))
            self.play(FadeIn(bars[1][0]), GrowFromEdge(bars[1][1], LEFT), FadeIn(bars[1][2]))
            vo.wait_until("b")
            self.play(FadeIn(bars[2][0]), GrowFromEdge(bars[2][1], LEFT), FadeIn(bars[2][2]))
            self.play(FadeIn(br1), FadeIn(br2))
            vo.wait_until("c")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]), FadeIn(whys[2]))
            vo.wait_until("f")
            self.play(FadeIn(led))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ideal(self):
        head = label(r"Work backwards from the ideal", font_size=36).to_edge(UP, buff=0.3)
        tops = VGroup(label(r"today", font_size=21, color=GREY_A), label(r"the research problem", font_size=21,
                                                                         color=HEAD),
                      label(r"what stands in the way", font_size=21, color=NO),
                      label(r"the ideal", font_size=21, color=YES))
        xs = (-5.3, -1.8, 1.7, 5.2)
        for t, x in zip(tops, xs):
            t.move_to([x, 2.35, 0])
        rows_spec = [
            (r"caches \ (Part 9, \ Part 32)",
             [r"evict the least \\ recently used block", r"predict reuse \\ from the past", r"the future \\ is unknown",
              r"Belady \ (1966): \ evict \\ the block needed \\ furthest in the future"]),
            (r"the Job \ (the ledger)",
             [rf"a hash table: \\ {R17['seconds']:.2f} s \ (Part 17)", r"less work \\ per byte",
              rf"a core spends about \\ {CPB17:.0f} cycles per byte",
              rf"touch each byte once: \\ {1000 * R60['seconds']:.0f} ms \ (Part 60)"]),
        ]
        rows = VGroup()
        for i, (name, cells) in enumerate(rows_spec):
            y = 0.9 - 2.05 * i
            nm = label(name, font_size=19, color=GREY_B).move_to([0, y + 0.85, 0])
            bs = VGroup()
            for t, x, c in zip(cells, xs, (GREY_B, HEAD, NO, YES)):
                bs.add(box(t, c, size=18, w=3.0, h=1.15).move_to([x, y, 0]))
            arr = VGroup(*[Arrow(bs[k + 1].get_left(), bs[k].get_right(), buff=0.04, color=GREY_B, stroke_width=2,
                                 max_tip_length_to_length_ratio=0.3) for k in range(3)])
            rows.add(VGroup(nm, bs, arr))
        foot = wrapped_label(r"the ideal says what success would be worth; \ the obstacle names the problem; \ "
                             r"Hamming's test asks whether you have an attack", 12.4, font_size=20,
                             color=WHITE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Working backwards scales up to research: start from the ideal, and ask what stands in the way. "
            "<bookmark mark='a'/> For a cache the ideal is known. In 1966 Laszlo Belady described it: evict the "
            "block that will be needed furthest in the future, and no policy misses less. <bookmark mark='b'/> What "
            "stands in the way is that the future is unknown. <bookmark mark='c'/> So the problem is to predict "
            "reuse from the past, and every policy, from least recently used onwards, can be measured by how close "
            "it comes. <bookmark mark='d'/> The Job too: the ideal is to touch each byte once, and Part 60 built "
            f"that in hardware, about {say(1000 * R60['seconds'])} milliseconds. Part 17's hash table spends about "
            f"{say(CPB17)} cycles on each byte, so the problem is less work per byte. <bookmark mark='e'/> The "
            "ideal says what success would be worth, the obstacle names the problem, and Hamming's test asks "
            "whether you have an attack."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tops))
            vo.wait_until("a")
            self.play(FadeIn(rows[0][0]), FadeIn(rows[0][1][3], shift=LEFT * 0.2))
            vo.wait_until("b")
            self.play(GrowArrow(rows[0][2][2]), FadeIn(rows[0][1][2], shift=LEFT * 0.2))
            vo.wait_until("c")
            self.play(GrowArrow(rows[0][2][1]), FadeIn(rows[0][1][1], shift=LEFT * 0.2))
            self.play(GrowArrow(rows[0][2][0]), FadeIn(rows[0][1][0], shift=LEFT * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(rows[1][0]), FadeIn(rows[1][1][3], shift=LEFT * 0.2))
            self.play(GrowArrow(rows[1][2][2]), FadeIn(rows[1][1][2], shift=LEFT * 0.2))
            self.play(GrowArrow(rows[1][2][1]), FadeIn(rows[1][1][1], shift=LEFT * 0.2))
            self.play(GrowArrow(rows[1][2][0]), FadeIn(rows[1][1][0], shift=LEFT * 0.2))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, LAM)
