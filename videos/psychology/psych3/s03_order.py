from __future__ import annotations

import numpy as np

from videos.psychology.psych3.common import *  # noqa: F403


def chance_grid(table, cell: float = 1.3, color=None) -> VGroup:
    """A 3 x 3 table of chances as shaded cells with percentages.  ``.cells[i][j]``."""
    t = np.asarray(table)
    g, cells = VGroup(), []
    for i in range(3):
        row = []
        for j in range(3):
            sq = Square(cell, stroke_color=BACKGROUND, stroke_width=2,
                        fill_color=interpolate_color(ManimColor("#18202E"), ManimColor(color or P.ACCENT), float(t[i, j])),
                        fill_opacity=1).move_to([(j - 1) * cell, (1 - i) * cell, 0])
            num = label(rf"{100 * t[i, j]:.0f}\%", font_size=30, color=WHITE if t[i, j] < 0.6 else BLACK).move_to(sq)
            row.append(VGroup(sq, num))
            g.add(row[-1])
        cells.append(row)
    g.cells = cells
    return g


class Order(VoiceoverScene):
    def construct(self):
        self.card()
        self.conjoint()
        self.crossing()

    def card(self):
        card = chapter_card(2, r"From an order to a scale", r"Can there be measurement where nothing can be added?",
                            lit={1964: r"Luce \& Tukey: conjoint measurement"}, part=PART, scale=("person",), marr=("what",))
        with self.voiceover(
            "Chapter two. From an order to a scale."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def conjoint(self):
        d = load("conjoint")
        head = heading(r"Three people meet three questions")
        # rows listed from the most able person down, so that the chances rise upwards as on a graph
        order = [2, 1, 0]
        table = np.asarray(d["additive"])[order]
        grid = chance_grid(table).move_to([-3.1, -0.25, 0])
        people = VGroup(*[label(t, font_size=28, color=GROUP_A) for t in (r"person C", r"person B", r"person A")])
        for p_, row in zip(people, grid.cells):
            p_.next_to(row[0], LEFT, buff=0.25)
        items = VGroup(*[label(t, font_size=28, color=GROUP_B) for t in (r"easy", r"medium", r"hard")])
        for it, col in zip(items, grid.cells[0]):
            it.next_to(col, UP, buff=0.2)
        cap = label(r"chance of a correct answer", font_size=26, color=GREY_B).next_to(grid, DOWN, buff=0.25)
        steps = VGroup(
            wrapped_label(r"1. \ Use only the order of the nine chances, not their sizes.", 6.0, 29, WHITE),
            wrapped_label(r"2. \ The people come in the same order on every question, and the questions in the "
                          r"same order for every person.", 6.0, 29, WHITE),
            wrapped_label(r"3. \ One more condition on the order, double cancellation, also holds.", 6.0, 29, WHITE),
            wrapped_label(r"Then each person and each question has a number, and the chances are ordered by "
                          r"person minus question.", 6.0, 29, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to([3.75, 0.8, 0])
        # the scale that the order implies: people and questions on one line
        x0, length, lo, hi = 0.75, 6.0, -1.4, 1.6
        ruler = Line([x0, -2.45, 0], [x0 + length, -2.45, 0], color=GREY_B, stroke_width=3)
        marks = VGroup()
        for v, t, c, up in [(a, n, GROUP_A, True) for a, n in zip(d["ability"], "ABC")] + [
                (b, n, GROUP_B, False) for b, n in zip(d["difficulty"], (r"easy", r"medium", r"hard"))]:
            x = x0 + length * (v - lo) / (hi - lo)
            tick = Line([x, -2.61, 0], [x, -2.29, 0], color=c, stroke_width=5)
            name = label(t, font_size=28, color=c).next_to(tick, UP if up else DOWN, buff=0.08)
            marks.add(VGroup(tick, name))
        tag = note(r"illustrative chances, from a model in which only person minus question matters").to_corner(
            DL, buff=0.2)
        # the two roads to a scale, shown while the idea is introduced
        rods = VGroup(Rectangle(width=1.6, height=0.36, stroke_width=0, fill_color=GROUP_A, fill_opacity=0.95),
                      Rectangle(width=2.4, height=0.36, stroke_width=0, fill_color=GROUP_B, fill_opacity=0.95))
        rods.arrange(RIGHT, buff=0)
        chain = VGroup(*[label(t, font_size=40, color=c) for t, c in
                         ((r"a", GROUP_A), (r"$<$", GREY_B), (r"b", P.ACCENT), (r"$<$", GREY_B), (r"c", GROUP_B))])
        chain.arrange(RIGHT, buff=0.3)
        roads = VGroup(
            VGroup(label(r"Campbell's road", font_size=30, color=GREY_A), rods,
                   label(r"add the objects", font_size=34, color=WHITE)).arrange(DOWN, buff=0.35),
            VGroup(label(r"another road", font_size=30, color=GREY_A), chain,
                   label(r"find structure in an order", font_size=34, color=P.ACCENT)).arrange(DOWN, buff=0.35),
        ).arrange(RIGHT, buff=2.0, aligned_edge=UP).move_to([0, 0.2, 0])
        with self.voiceover(
            "Stevens changed the question. Others answered Campbell on his own ground, and the answer is one of "
            "the most beautiful ideas in the subject. <bookmark mark='z'/> It says you can get a real scale, with "
            "equal units, out of nothing but an order. <bookmark mark='a'/> Three people try three questions. "
            "Suppose all we know is each person's chance of getting each question right. <bookmark mark='b'/> First, throw away the "
            "sizes of the nine chances and keep only their order. <bookmark mark='c'/> Second, check that the "
            "order is consistent: person C beats B beats A on every question, and the hard question is hardest "
            "for everyone. <bookmark mark='d'/> Third, check one more condition on the order, called double "
            "cancellation. <bookmark mark='e'/> If the order passes, a theorem of Luce and Tukey, from 1964, "
            "says something remarkable. There must be a number for each person and a number for each question, "
            "<bookmark mark='f'/> on one common scale, such that the chances are ordered by the difference "
            "between them. And those numbers are fixed up to a unit and a zero. That's an interval scale. "
            "Nothing was added to anything. The addition was hiding in the pattern."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            self.play(FadeIn(roads[0], shift=UP * 0.15))
            vo.wait_until("z")
            self.play(FadeIn(roads[1], shift=UP * 0.15))
            vo.wait_until("a")
            self.play(FadeOut(roads), FadeIn(grid, lag_ratio=0.08), FadeIn(people), FadeIn(items), FadeIn(cap),
                      run_time=2.0)
            for m, st in zip("bcde", steps):
                vo.wait_until(m)
                self.play(FadeIn(st, shift=RIGHT * 0.15))
            vo.wait_until("f")
            self.play(Create(ruler), LaggedStart(*[FadeIn(m_, shift=UP * 0.1) for m_ in marks], lag_ratio=0.2),
                      run_time=2.5)
        self.clear_scene()

    def crossing(self):
        d = load("conjoint")
        head = heading(r"And when the order fails the test")
        order = [2, 1, 0]
        ok = chance_grid(np.asarray(d["additive"])[order], cell=1.2).move_to([-4.7, 0.6, 0])
        bad = chance_grid(np.asarray(d["crossing"])[order], cell=1.2, color=P.ERR).move_to([-0.2, 0.6, 0])
        ok_cap = label(r"passes: \ a scale exists", font_size=30, color=TRUE).next_to(ok, DOWN, buff=0.25)
        bad_cap = label(r"fails: \ no scale can exist", font_size=30, color=ERRC).next_to(bad, DOWN, buff=0.25)
        # for person C the "medium" question is easier than the "easy" one
        box = SurroundingRectangle(VGroup(bad.cells[0][0], bad.cells[0][1]), color=WHITE, buff=0.0, stroke_width=3)
        why_ = wrapped_label(r"person C finds the second question easier than the first; \ persons A and B find it "
                             r"harder", 3.9, 28, GREY_A).move_to([4.7, 0.9, 0])
        lines = VGroup(
            label(r"Whether an attribute is a quantity is a question the data can answer.", font_size=30, color=WHITE),
            label(r"Adding objects is one road to measurement. \ Structure in an order is another.", font_size=28,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "And the test can fail, which is what makes it worth something. <bookmark mark='a'/> Here the same "
            "three people meet three different questions. <bookmark mark='b'/> Person C finds the second "
            "question easier than the first, and the other two find it harder. The questions don't come in one "
            "order for everybody, so no single scale can hold both the people and the questions. "
            "<bookmark mark='c'/> So here is the full reply to the committee. Whether loudness, or ability, or an "
            "attitude is a quantity is not something to settle by definition. It's an empirical question, with a "
            "test that data can pass or fail. This is called conjoint measurement, and it's the foundation under "
            "the modern theory of tests, which we reach in Part 46. The embarrassing part is how seldom anyone "
            "runs the test. That's this part's frontier."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ok), FadeIn(ok_cap))
            vo.wait_until("a")
            self.play(FadeIn(bad, lag_ratio=0.08))
            vo.wait_until("b")
            self.play(Create(box), FadeIn(why_), FadeIn(bad_cap))
            vo.wait_until("c")
            self.play(FadeIn(lines[0], shift=UP * 0.15))
            self.play(FadeIn(lines[1]))
        self.clear_scene()
