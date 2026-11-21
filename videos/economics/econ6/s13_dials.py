from __future__ import annotations

from videos.economics.econ6.common import *  # noqa: F403


def dial_rows(dial, lo, hi, ticks, unit, x0=-0.2, x1=6.3, top=2.6, step=0.5, fmt="{:+.2f}", highlight=()):
    """A dial's estimates as dots (with intervals where given) on one axis; the rows named on the left."""

    def X(v):
        return x0 + (x1 - x0) * (v - lo) / (hi - lo)

    n = len(dial.estimates)
    axis_y = top - step * (n - 1) - 0.45
    axis = Line([x0, axis_y, 0], [x1, axis_y, 0], color=GREY_C, stroke_width=2)
    tk = VGroup(*[VGroup(Line([X(v), axis_y - 0.06, 0], [X(v), axis_y + 0.06, 0], color=GREY_C),
                         MathTex(f"{v:g}", font_size=20, color=GREY_B).move_to([X(v), axis_y - 0.28, 0]))
                  for v in ticks])
    un = label(unit, font_size=18, color=GREY_B).next_to(tk, DOWN, buff=0.12)
    zero = DashedLine([X(0), axis_y, 0], [X(0), top + 0.35, 0], color=GREY_D, stroke_width=1.5) if lo < 0 < hi \
        else VMobject()
    rows = VGroup()
    for k, e in enumerate(dial.estimates):
        y = top - step * k
        c = DESIGN_COLOR.get(e.design, GREY_B)
        who = e.who.split(",")[0] + r" et al." if ("," in e.who and not e.who.startswith("this film")) else e.who
        t = VGroup(label(rf"{who} ({e.year})", font_size=18, color=WHITE),
                   label(tex_safe(e.sample), font_size=13, color=GREY_B)).arrange(DOWN, aligned_edge=RIGHT, buff=0.03)
        if t.width > 6.3:
            t.width = 6.3
        t.move_to([x0 - 0.3, y, 0], aligned_edge=RIGHT)
        g = VGroup(t)
        if e.lo is not None and e.hi is not None:
            g.add(Line([X(max(e.lo, lo)), y, 0], [X(min(e.hi, hi)), y, 0], color=c, stroke_width=3))
        dot = Dot([X(e.value), y, 0], radius=0.09, color=c)
        val = label(fmt.format(e.value), font_size=16, color=c).next_to(dot, UP, buff=0.05)
        g.add(dot, val)
        if k in highlight:
            g.add(SurroundingRectangle(VGroup(t, dot), color=GIFF, buff=0.06, stroke_width=1.5, corner_radius=0.06))
        rows.add(g)
    return VGroup(axis, tk, un, zero), rows


def status_head(dial, title):
    color = DIAL_STATUS.get(dial.status, GREY_C)
    pill = VGroup(RoundedRectangle(width=3.6, height=0.4, corner_radius=0.08, stroke_width=0, fill_color=color,
                                   fill_opacity=1), label(dial.status, font_size=19, color=BACKGROUND))
    pill[1].move_to(pill[0])
    head = VGroup(label(title, font_size=28), pill).arrange(RIGHT, buff=0.4)
    return head.to_edge(UP, buff=0.3).to_edge(LEFT, buff=0.5)


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 11, r"The Dials: \ how much do people respond?", r"Across studies, how strongly does demand "
             r"respond to prices and to income?", "Chapter eleven. The Dials: how much do people respond?",
             scale=("household", "market"))
        self.staples()
        self.engel()

    def staples(self):
        dial = dials.DIALS["elasticity_staples"]
        head = status_head(dial, r"price elasticity of demand for staples")
        frame, rows = dial_rows(dial, -1.4, 1.0, [-1.0, -0.5, 0, 0.5, 1.0], r"percent change in quantity per "
                                r"percent change in price", highlight=(6, 7, 8))
        meaning = wrapped_label(tex_safe(dial.meaning), 12.4, 19, GREY_A).to_edge(DOWN, buff=0.2)
        tag = published_tag(r"Part 2's meta-analyses; Jensen and Miller, AER (2008), table 3", corner=UR,
                            font_size=12)
        with self.voiceover(
            "Part two opened a dial for the price elasticity of staples, and this part adds to it. "
            "<bookmark mark='a'/> The rows from Part two are meta-analyses: gasoline in the short run, after "
            "correcting for publication bias, minus nought point nought nine; in the long run, minus nought point "
            "three one; cigarettes about minus a half; beer, wine and spirits from minus nought point four six "
            "to minus nought point eight. All negative, all below one in size. <bookmark mark='b'/> Now the "
            "experiment from Hunan. All households: plus nought point two two, with an interval that includes zero. "
            "Households getting under eighty percent of their calories from rice: plus nought point four five. The "
            "very poorest: minus nought point six one. <bookmark mark='c'/> So the status moves, from settled within "
            "a range to depends on the setting. In markets, demand for staples slopes down, gently. For households "
            "living on one staple, it can slope up, and a subsidy meant to help them eat more can leave them eating "
            "less."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows[:6]], lag_ratio=0.3), run_time=3)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows[6:]], lag_ratio=0.5), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()

    def engel(self):
        dial = dials.DIALS["engel_food"]
        e = load("engel")
        head = status_head(dial, r"income elasticity of spending on food \ (new)")
        frame, rows = dial_rows(dial, 0.0, 1.2, [0, 0.2, 0.4, 0.6, 0.8, 1.0], r"percent change in food spending "
                                r"per percent change in income", top=1.9, step=0.62)
        ours = VGroup(label(r"computed here, \ for comparison:", font_size=20, color=GREY_A),
                      label(rf"America's century: \ {e['century_el']:.2f}", font_size=20, color=E.ACCENT),
                      label(rf"US quintiles, 2024: \ {e['el_bottom_middle']:.2f} and {e['el_middle_top']:.2f}",
                            font_size=20, color=E.ACCENT)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        ours.next_to(frame, DOWN, buff=0.35).to_edge(RIGHT, buff=0.6)
        meaning = wrapped_label(tex_safe(dial.meaning), 12.4, 19, GREY_A).to_edge(DOWN, buff=0.2)
        tag = published_tag(r"Houthakker (1957); Seale and Regmi (2006); both via Anker (2011)", corner=UR,
                            font_size=12).next_to(head, DOWN, buff=0.12).align_to(head, LEFT)
        with self.voiceover(
            "And a new dial: the income elasticity of spending on food. <bookmark mark='a'/> Houthakker, in 1957, "
            "across about forty surveys: one would not be very far astray, he wrote, at nought point six. "
            "<bookmark mark='b'/> Across countries, James Seale and Anita Regmi found it falling with national "
            "income: about nought point seven in low-income countries, nought point six and nought point five in the "
            "middle, and between nought point one and nought point three in rich ones. "
            "<bookmark mark='c'/> Our own computations sit where they should: nought point four seven for America's "
            "century, a third to a half across American households today. <bookmark mark='d'/> Below one "
            "everywhere it's been measured, and falling as people get richer: Engel's law, as a number."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows[1:]], lag_ratio=0.4), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(ours))
            vo.wait_until("d")
            self.play(FadeIn(meaning))
        self.clear_scene()
