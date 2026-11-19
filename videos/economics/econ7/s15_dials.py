from __future__ import annotations

from videos.economics.econ7.common import *  # noqa: F403


def dial_rows(dial, lo, hi, ticks, unit, x0=-0.2, x1=6.3, top=2.75, step=0.47, log=False, fmt="{:.2f}"):
    """A dial's estimates as dots (with intervals where given) on one axis, linear or log; the rows named on the
    left."""

    def X(v):
        if log:
            v = np.log10(max(v, 10 ** lo))
        return x0 + (x1 - x0) * (v - lo) / (hi - lo)

    n = len(dial.estimates)
    axis_y = top - step * (n - 1) - 0.45
    axis = Line([x0, axis_y, 0], [x1, axis_y, 0], color=GREY_C, stroke_width=2)
    tk = VGroup(*[VGroup(Line([X(v), axis_y - 0.06, 0], [X(v), axis_y + 0.06, 0], color=GREY_C),
                         MathTex(f"{v:g}", font_size=20, color=GREY_B).move_to([X(v), axis_y - 0.28, 0]))
                  for v in ticks])
    un = label(unit, font_size=17, color=GREY_B).next_to(tk, DOWN, buff=0.1)
    rows = VGroup()
    for k, e in enumerate(dial.estimates):
        y = top - step * k
        c = DESIGN_COLOR.get(e.design, GREY_B)
        who = e.who.split(",")[0] + r" et al." if "," in e.who else e.who
        t = VGroup(label(rf"{who} ({e.year}) \ $\cdot$ \ {e.design}", font_size=17, color=WHITE),
                   label(tex_safe(e.sample), font_size=12, color=GREY_B)).arrange(DOWN, aligned_edge=RIGHT, buff=0.03)
        if t.width > 6.4:
            t.width = 6.4
        t.move_to([x0 - 0.3, y, 0], aligned_edge=RIGHT)
        g = VGroup(t)
        if e.lo is not None and e.hi is not None:
            g.add(Line([X(e.lo), y, 0], [X(e.hi), y, 0], color=c, stroke_width=3))
        v = e.value if not log else max(e.value, 10 ** lo)
        dot = Dot([X(v), y, 0], radius=0.085, color=c)
        val = label(fmt.format(e.value), font_size=15, color=c).next_to(dot, UP, buff=0.04)
        g.add(dot, val)
        rows.add(g)
    return VGroup(axis, tk, un), rows


def status_head(dial, title):
    color = DIAL_STATUS.get(dial.status, GREY_C)
    pill = VGroup(RoundedRectangle(width=2.6, height=0.4, corner_radius=0.08, stroke_width=0, fill_color=color,
                                   fill_opacity=1), label(dial.status, font_size=19, color=BACKGROUND))
    pill[1].move_to(pill[0])
    head = VGroup(label(title, font_size=28), pill).arrange(RIGHT, buff=0.4)
    return head.to_edge(UP, buff=0.3).to_edge(LEFT, buff=0.5)


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 13, r"The Dials: \ how risk averse, \ how willing to wait?", r"Across studies, how large are "
             r"relative risk aversion and the elasticity of intertemporal substitution?", "Chapter thirteen. The "
             "Dials: how risk averse, how willing to wait?", scale=("person", "household", "market", "nation"))
        self.risk()
        self.eis()

    def risk(self):
        dial = dials.DIALS["risk_aversion"]
        head = status_head(dial, r"relative risk aversion \ (new)")
        frame, rows = dial_rows(dial, np.log10(0.15), np.log10(15), [0.2, 0.5, 1, 2, 5, 10],
                                r"relative risk aversion $\gamma$ \ (log scale)", log=True)
        meaning = wrapped_label(tex_safe(dial.meaning), 12.6, 17, GREY_A).to_edge(DOWN, buff=0.12)
        with self.voiceover(
            "Two dials open in this part. The first is relative risk aversion. <bookmark mark='a'/> In the "
            "laboratory, with a few dollars at stake, Holt and Laury's subjects come out at about nought point three; "
            "with stakes ninety times larger, about nought point eight. <bookmark mark='b'/> From labour supply, Raj "
            "Chetty put it at about one. A meta-analysis of a thousand estimates from the Euler equation, by "
            "Elminejad, Havranek and Irsova, finds about one in economics once publication bias is "
            "removed, and two to seven in finance; the median reported estimate is nearly four. The survey gambles "
            "give about four. <bookmark mark='c'/> And the values models are calibrated with sit higher still: a "
            "median of six across two hundred studies, and ten in the long-run risks model. "
            "<bookmark mark='d'/> So the status is contested. The number depends on the stakes, the method and the "
            "question, and expected utility, which says it should be one number, can't reconcile them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows[:2]], lag_ratio=0.4), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows[2:7]], lag_ratio=0.4), run_time=4)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows[7:]], lag_ratio=0.4), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()

    def eis(self):
        dial = dials.DIALS["eis"]
        head = status_head(dial, r"elasticity of intertemporal substitution \ (new)")
        frame, rows = dial_rows(dial, -0.1, 2.2, [0, 0.5, 1, 1.5, 2], r"percent change in consumption growth per "
                                r"point of the real interest rate", step=0.5, top=2.7)
        f = load("film")
        ours = label(rf"computed here, \ the intermission's century: \ OLS {f['full']['ols']:.2f}, \ instrumented "
                     rf"{signed(f['full']['iv'], 2)}", font_size=19, color=E.ACCENT).next_to(frame, DOWN, buff=0.2)
        meaning = wrapped_label(tex_safe(dial.meaning), 12.6, 17, GREY_A).to_edge(DOWN, buff=0.12)
        with self.voiceover(
            "The second dial is the elasticity of intertemporal substitution. <bookmark mark='a'/> Robert Hall, in "
            "1988, found no strong evidence that it's positive at all in American aggregate data, and our own "
            "century of data in the intermission agreed. Barsky's survey gave about nought point two. "
            "<bookmark mark='b'/> Annette Vissing-Jorgensen pointed out that only people who hold assets can respond "
            "to their returns: for stockholders she found a third, for bondholders nearly one. Jonathan Gruber, using "
            "differences in taxes on interest, found about two. <bookmark mark='c'/> Tomas Havranek's meta-analysis "
            "of two thousand seven hundred estimates found that selective reporting had pulled the average up by "
            "about a half: corrected, about zero in aggregate data and a third for asset holders. And the "
            "long-run risks calibration uses one and a half. <bookmark mark='d'/> Contested again. A small elasticity "
            "means interest rates move saving little, which is a large question for monetary policy and for taxes "
            "on saving, and it comes back in Parts twenty-two and twenty-three."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows[:2]], lag_ratio=0.4), FadeIn(ours), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows[2:5]], lag_ratio=0.4), run_time=3)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows[5:]], lag_ratio=0.4), run_time=3)
            vo.wait_until("d")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()
