from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs1.common import COST, CTRL, DATA, HEAD, HIST, NO, PART, YES, fmt, say, load

SQ = [DATA, CTRL, YES]  # the squares cut at each round of the rectangle


def ramp(t: np.ndarray) -> np.ndarray:
    """Steps (0..1) as RGB: deep blue through teal and gold to coral."""
    stops = np.array([[21, 27, 38], [46, 111, 176], [63, 184, 175], [242, 209, 107], [242, 140, 91]], float)
    t = np.clip(t, 0, 1) * (len(stops) - 1)
    i = np.minimum(t.astype(int), len(stops) - 2)
    f = (t - i)[..., None]
    return stops[i] * (1 - f) + stops[i + 1] * f


class Algorithms(VoiceoverScene, MovingCameraScene):
    def construct(self):
        self.card()
        self.rectangle()
        self.correct()
        self.terminates()
        self.how_long()
        self.definition()

    def card(self):
        card = chapter_card(1, r"Algorithms before machines", r"What does it mean to follow a rule?", part=PART)
        with self.voiceover("Chapter one. Algorithms before machines."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def rectangle(self):
        d = load("euclid")
        tr = d["trace"]
        S = 8.6 / 1071  # units per unit length
        origin = np.array([-6.6, -2.6, 0])  # the rectangle's bottom-left corner

        def rect(x, y, w, h, color, fill=0.28):
            r = Rectangle(width=w * S, height=h * S, stroke_color=color, stroke_width=2, fill_color=color,
                          fill_opacity=fill)
            return r.move_to(origin + np.array([(x + w / 2) * S, (y + h / 2) * S, 0]))

        whole = rect(0, 0, 1071, 462, GREY_B, fill=0.06)
        wl = label(r"$1071$", font_size=30, color=GREY_A).next_to(whole, UP, buff=0.12)
        hl = label(r"$462$", font_size=30, color=GREY_A).next_to(whole, LEFT, buff=0.12)
        hl.set_x(max(hl.get_x(), -6.9 + hl.width / 2))
        if hl.get_left()[0] < -6.95:
            hl.next_to(whole, DOWN, buff=0.1).align_to(whole, LEFT)
        eqs = VGroup(*[cmath(rf"{t['a']}", r"=", rf"{t['q']}", r"\times", rf"{t['b']}", r"+", rf"{t['r']}",
                             font_size=36) for t in tr])
        for e, c in zip(eqs, SQ):
            e[2].set_color(c)
            e[4].set_color(c)
        eqs.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([4.6, 2.2, 0])
        lead = VGroup(label(r"Euclid, with division:", font_size=32, color=GREY_A),
                      cmath(r"a", r"=", r"q", r"\times", r"b", r"+", r"r", font_size=44,
                            colors={r"a": DATA, r"b": DATA, r"r": CTRL, r"q": GREY_A}),
                      label(r"take $b$ from $a$ as many times as it fits, \\ keep the remainder $r < b$",
                            font_size=28, color=GREY_B)).arrange(DOWN, buff=0.3).move_to(UP * 0.3)
        eqs.set_x(min(eqs.get_x(), 6.9 - eqs.width / 2))
        # round 1: two squares of side 462 cut from the left
        r1 = VGroup(rect(0, 0, 462, 462, SQ[0]), rect(462, 0, 462, 462, SQ[0]))
        # round 2: the strip 147 x 462 at the right, three squares of 147 stacked
        x2 = 924
        r2 = VGroup(*[rect(x2, k * 147, 147, 147, SQ[1]) for k in range(3)])
        # round 3: the strip 147 x 21 at the top of that strip: seven squares of 21
        y3 = 441
        r3 = VGroup(*[rect(x2 + k * 21, y3, 21, 21, SQ[2], fill=0.6) for k in range(7)])
        strip3 = rect(x2, y3, 147, 21, WHITE, fill=0.0)
        with self.voiceover(
            "Euclid's rule from the opening, with a short cut. Instead of taking the smaller pile away again and again, "
            "take it away as many times as it fits at once, and keep the remainder. <bookmark mark='a'/> Here it is on "
            "a picture. A rectangle, one thousand and seventy-one by four hundred and sixty-two. <bookmark mark='b'/> "
            "Cut off as many squares of side four hundred and sixty-two as fit: two of them. "
            "<bookmark mark='c'/> What is left is a strip one hundred and forty-seven wide. That is the remainder: "
            "one thousand and seventy-one is two times four hundred and sixty-two, plus one hundred and forty-seven."
        ) as vo:
            self.play(FadeIn(lead, shift=UP * 0.15))
            vo.wait_until("a")
            self.play(FadeOut(lead), Create(whole), FadeIn(wl), FadeIn(hl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, scale=0.95) for r in r1], lag_ratio=0.4), run_time=1.6)
            vo.wait_until("c")
            self.play(Write(eqs[0]))
        with self.voiceover(
            "Now the strip is the new rectangle. Cut squares of side one hundred and forty-seven from it: three fit. "
            "<bookmark mark='a'/> The remainder is a sliver twenty-one high. <bookmark mark='b'/> Cut squares of side "
            "twenty-one from the sliver. <bookmark mark='c'/> Seven of them fit exactly, with nothing left over. "
            "<bookmark mark='d'/> So squares of side twenty-one tile the sliver, and therefore the strip, and therefore "
            "the whole rectangle. Twenty-one is the greatest common divisor of one thousand and seventy-one and four "
            "hundred and sixty-two."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(r, scale=0.95) for r in r2], lag_ratio=0.3), Write(eqs[1]), run_time=1.8)
            vo.wait_until("a")
            self.play(Create(strip3))
            vo.wait_until("b")
            self.play(FadeOut(eqs[:2]), frame_to(self, strip3, width=4.2), run_time=1.8)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in r3], lag_ratio=0.15), run_time=1.6)
            vo.wait_until("d")
            self.play(frame_home(self), FadeIn(eqs[:2]), Write(eqs[2]), run_time=1.6)
            box = SurroundingRectangle(eqs[2][4], color=YES, buff=0.08)
            g = label(rf"$\gcd(1071, 462) = {d['gcd']}$", font_size=40, color=YES).next_to(eqs, DOWN, buff=0.45)
            g.align_to(eqs, LEFT)
            self.play(Create(box), FadeIn(g))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def correct(self):
        head = label(r"Why is the answer right?", font_size=40).to_edge(UP, buff=0.4)
        col = {r"d": HEAD, r"a": DATA, r"b": DATA, r"r": CTRL, r"q": GREY_A}
        rows = [
            cmath(r"a", r"=", r"q", r"b", r"+", r"r", font_size=44, colors=col),
            cmath(r"d \mid a", r"\text{ and }", r"d \mid b", r"\;\Longrightarrow\;", r"d \mid a - q b", r"= r",
                  font_size=40, colors={r"d \mid a": HEAD, r"d \mid b": HEAD, r"d \mid a - q b": HEAD, r"= r": CTRL}),
            cmath(r"d \mid b", r"\text{ and }", r"d \mid r", r"\;\Longrightarrow\;", r"d \mid q b + r", r"= a",
                  font_size=40, colors={r"d \mid b": HEAD, r"d \mid r": HEAD, r"d \mid q b + r": HEAD, r"= a": DATA}),
            cmath(r"\gcd(a, b)", r"=", r"\gcd(b, r)", font_size=46, colors={r"\gcd(a, b)": YES, r"\gcd(b, r)": YES}),
        ]
        whys = [why(r"the division step"), why(r"a common divisor of $a, b$ divides $r$"),
                why(r"a common divisor of $b, r$ divides $a$"), why(r"the same common divisors, \\ so the same greatest one")]
        step = ladder(self, rows, whys, keep=4, top=2.3, x=-1.2, buff=0.55, align_index=None)
        foot = label(r"$\gcd(1071, 462) = \gcd(462, 147) = \gcd(147, 21) = \gcd(21, 0) = 21$", font_size=34,
                     color=GREY_A).to_edge(DOWN, buff=0.55)
        with self.voiceover(
            "Why does this work for any two numbers? <bookmark mark='a'/> One step of the rule writes a as q copies "
            "of b, plus a remainder r. <bookmark mark='b'/> Take any number d that divides both a and b. Then it divides "
            "a minus q times b, which is r. <bookmark mark='c'/> And the other way: anything dividing b and r divides q "
            "times b plus r, which is a. <bookmark mark='d'/> So the pair a, b and the pair b, r have exactly the same "
            "common divisors, and so the same greatest one. Each step changes the numbers but not the answer. "
            "<bookmark mark='e'/> When the remainder reaches zero, the answer is in plain sight: the greatest common "
            "divisor of twenty-one and zero is twenty-one."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            self.play(FadeIn(foot, shift=UP * 0.1))
        inv = definition_card(r"Invariant", r"a quantity a procedure never changes. \ Here: the gcd of the pair. "
                              r"\ Prove it holds at the start and survives every step, \ and it holds at the end.",
                              color=YES, width=8.6).to_corner(DR, buff=0.35)
        with self.voiceover(
            "That kind of argument has a name. Something the procedure never changes is an invariant. Show it holds at "
            "the start, and that every step preserves it, and it holds when the procedure stops. Invariants are how we "
            "will prove circuits, algorithms and whole distributed systems correct, all through this series."
        ):
            self.play(FadeOut(foot), FadeIn(inv.move_to(DOWN * 2.45), shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def terminates(self):
        head = label(r"Why does it stop?", font_size=40).to_edge(UP, buff=0.4)
        vals = [1071, 462, 147, 21, 0]
        ax_y = -2.4
        bars = VGroup()
        for i, v in enumerate(vals):
            h = max(v / 1071 * 4.2, 0.02)
            b = Rectangle(width=1.0, height=h, stroke_width=0, fill_color=[DATA, DATA, CTRL, YES, GREY_B][i],
                          fill_opacity=0.85)
            b.move_to([-4 + i * 1.6, ax_y + h / 2, 0])
            t = label(rf"${v}$", font_size=28).next_to(b, UP, buff=0.12)
            bars.add(VGroup(b, t))
        base = Line([-5.0, ax_y, 0], [3.3, ax_y, 0], color=GREY_C, stroke_width=2)
        gts = VGroup(*[MathTex(r">", font_size=40, color=GREY_B).move_to([-3.2 + i * 1.6, ax_y + 0.5, 0])
                       for i in range(4)])
        rule = cmath(r"b", r">", r"r_1", r">", r"r_2", r">", r"r_3", r">", r"\cdots", r"\ge", r"0", font_size=40,
                     colors={r"b": DATA, r"r_1": CTRL, r"r_2": CTRL, r"r_3": CTRL}).move_to([3.6, 1.6, 0])
        rule.set_x(min(rule.get_x(), 6.9 - rule.width / 2))
        note_ = label(r"a decreasing sequence of natural numbers \\ cannot go on forever: \ at most $b$ steps",
                      font_size=28, color=GREY_A).next_to(rule, DOWN, buff=0.4)
        note_.set_x(min(note_.get_x(), 6.9 - note_.width / 2))
        with self.voiceover(
            "And why does it ever stop? <bookmark mark='a'/> Each remainder is smaller than the number it came from: "
            "four hundred and sixty-two, one hundred and forty-seven, twenty-one, zero. <bookmark mark='b'/> In general, "
            "b is bigger than the first remainder, which is bigger than the second, and so on, and none of them can be "
            "negative. <bookmark mark='c'/> A decreasing sequence of natural numbers cannot go on forever, so the "
            "procedure stops after at most b steps. A quantity that shrinks and cannot go below zero is the standard way "
            "to prove that a loop ends. We will meet it again in Part 2, and in Part 54, when we prove programs correct "
            "by machine."
        ) as vo:
            self.play(FadeIn(head), Create(base))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(g) for g in gts], lag_ratio=0.3), run_time=2.4)
            vo.wait_until("b")
            self.play(Write(rule))
            vo.wait_until("c")
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def how_long(self):
        d = load("euclid")
        grid = np.asarray(d["grid"], float)
        N = d["N"]
        rgb = ramp(grid.T / grid.max())[::-1]  # rows: b from N (top) down to 1; columns: a
        img = bitmap(rgb, width=5.6, height=5.6).move_to([-3.1, -0.35, 0])
        frame = SurroundingRectangle(img, buff=0, color=GREY_C, stroke_width=1.5)
        xl = label(r"$a$", font_size=28, color=GREY_A).next_to(img, DOWN, buff=0.15)
        yl = label(r"$b$", font_size=28, color=GREY_A).next_to(img, LEFT, buff=0.15)
        tl = label(rf"steps of Euclid's algorithm, \ $1 \le a, b \le {N}$", font_size=28).next_to(img, UP, buff=0.2)
        # colour bar
        cb = VGroup(*[Rectangle(width=0.32, height=0.4, stroke_width=0, fill_color=rgb_to_color(ramp(np.array(k / 12)) / 255),
                                fill_opacity=1) for k in range(13)]).arrange(UP, buff=0).next_to(img, RIGHT, buff=0.3)
        cbl = VGroup(label(r"$0$", font_size=20, color=GREY_B).next_to(cb, RIGHT, buff=0.1).align_to(cb, DOWN),
                     label(rf"${int(grid.max())}$", font_size=20, color=GREY_B).next_to(cb, RIGHT, buff=0.1).align_to(cb, UP))
        a_, b_ = d["argmax"]  # grid indices are (a, b) from 0 at value 1

        def px(a, b):  # pixel centre of the pair (a, b)
            return img.get_corner(DL) + np.array([(a - 0.5) / N * img.width, (b - 0.5) / N * img.height, 0])

        worst = d["worst"]
        fibs = VGroup(*[Dot(px(*w["pair"]), radius=0.05, color=WHITE) for w in worst if max(w["pair"]) <= N])
        mark = Circle(radius=0.16, color=WHITE, stroke_width=2.5).move_to(px(a_, b_))
        table = VGroup(*[label(rf"${w['pair'][0]}, {w['pair'][1]}$:\ \ ${w['steps']}$ steps", font_size=24,
                               color=GREY_A) for w in worst[3:] if max(w["pair"]) <= N]).arrange(DOWN, aligned_edge=LEFT,
                                                                                               buff=0.1)
        table.move_to([4.6, 0.5, 0])
        th = label(r"worst cases: \ consecutive Fibonacci numbers", font_size=24, color=HEAD).next_to(table, UP, buff=0.25)
        th.set_x(min(th.get_x(), 6.9 - th.width / 2))
        lame = theorem_card(r"Lam\'e (1844)", r"Euclid's algorithm takes at most $5$ steps for each decimal digit of "
                            r"the smaller number.", width=5.4, font_size=22).next_to(table, DOWN, buff=0.35)
        lame.set_x(min(lame.get_x(), 6.95 - lame.width / 2))
        with self.voiceover(
            "How many steps does it take? Here is every pair of numbers up to two hundred and thirty-three, "
            "coloured by the number of steps, computed. <bookmark mark='a'/> Along the diagonal, one step. Near the axes, "
            "few. The bright rays are the hard cases. <bookmark mark='b'/> The very worst cases sit at consecutive "
            "Fibonacci numbers, where every quotient is one and the remainders shrink as slowly as they possibly can: "
            f"the hardest pair here, {say(max(a_, b_))} and {say(min(a_, b_))}, takes {int(grid.max())} steps. "
            "<bookmark mark='c'/> In 1844 Gabriel Lamé turned that into a theorem: the number of steps is at most five "
            "for each decimal digit of the smaller number. It is one of the first proofs of how long an algorithm takes, "
            "and Part 16 makes that question the centre of a whole subject."
        ) as vo:
            self.play(FadeIn(img), Create(frame), FadeIn(tl), FadeIn(xl), FadeIn(yl), FadeIn(cb), FadeIn(cbl))
            vo.wait_until("a")
            self.play(Indicate(tl, color=HEAD), run_time=1.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(f, scale=2) for f in fibs], lag_ratio=0.1), Create(mark), FadeIn(th),
                      LaggedStart(*[FadeIn(t) for t in table], lag_ratio=0.1), run_time=2.4)
            vo.wait_until("c")
            self.play(FadeIn(lame, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def definition(self):
        hc = history_card(r"c. 825", r"Mu\d{h}ammad ibn M\=us\=a al-Khw\=arizm\=\i",
                          r"wrote the book on calculating with the Hindu--Arabic numerals; translated into Latin as "
                          r"\textit{Algoritmi de numero Indorum}. \ His name became \textit{algorithm}.",
                          width=6.4, font_size=24).to_corner(UL, buff=0.4)
        defn = definition_card(r"Algorithm (informally)",
                               r"a finite list of precise instructions \\ that a clerk could carry out without understanding "
                               r"them, \\ step by step, \ and that stops with the answer.", color=CTRL, width=8.4,
                               font_size=28)
        defn.move_to([1.2, -0.4, 0])
        qs = VGroup(*[label(t, font_size=28, color=NO) for t in
                      (r"``precise'': \ how precise?", r"``without understanding'': \ who decides?",
                       r"``a step'': \ how big may a step be?")]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        qs.next_to(defn, DOWN, buff=0.45).align_to(defn, LEFT)
        with self.voiceover(
            "The word algorithm itself comes from a name. <bookmark mark='a'/> Around eight hundred and twenty-five, "
            "in Baghdad, Muhammad ibn Musa al-Khwarizmi wrote the book that taught Europe to calculate with Hindu-Arabic "
            "numerals. In Latin his name became Algoritmi, and a rule for calculating became an algorithm. "
            "<bookmark mark='b'/> For more than a thousand years that was a word, not a definition: a finite list of "
            "precise instructions that a clerk could carry out step by step without understanding them, and that stops "
            "with the answer. <bookmark mark='c'/> Good enough to use. Not good enough to prove anything about. How "
            "precise is precise? Who decides what needs understanding? How much may one step do? Those questions only "
            "mattered once someone wanted to prove that no algorithm exists for a problem. That is where this story "
            "is going."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(defn, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(q, shift=RIGHT * 0.15) for q in qs], lag_ratio=0.4), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()
