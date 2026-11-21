from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ58.common import *  # noqa: F403


class Life(VoiceoverScene):
    def construct(self):
        card(self, 4, r"A statistical life", r"What is a small change in the risk of death worth?",
             "Chapter four. A statistical life.", lit={1968: r"Schelling", 1976: r"Thaler and Rosen",
                                                       2003: r"the `senior discount'"},
             scale=("person",), horizon=("a year", "a century"))
        self.arithmetic()
        self.wages()
        self.dial()
        self.age()

    def arithmetic(self):
        grid = VGroup(*[Dot(radius=0.028, color=GREY_C) for _ in range(2000)]).arrange_in_grid(40, 50, buff=0.07)
        grid.to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        lab = label(r"10,000 people \ (2,000 shown)".replace(",", "{,}"), font_size=18, color=GREY_A).next_to(
            grid, UP, buff=0.15)
        eq = VGroup(
            label(r"each accepts \$900 a year \\ for a 1-in-10,000 risk of dying".replace(",", "{,}"), font_size=24,
                  color=TRAV),
            MathTex(r"10{,}000 \times \$900 = \$9 \text{ million}", font_size=34, color=WHITE),
            label(r"= one statistical life, \ priced", font_size=26, color=SAFE),
            label(r"a rate of exchange for small risks, \\ not the worth of a person", font_size=22,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.6)
        hc = history_card(1968, r"Thomas Schelling", r"`The Life You Save May Be Your Own': \ value the risk, \ not "
                          r"the life", color=SAFE, width=5.4, font_size=19).next_to(eq, UP, buff=0.3)
        with self.voiceover(
            "The ferry kills people; the bridge would kill fewer. How is that valued? In 1968 Thomas Schelling "
            "pointed out that the question is not what a life is worth, but what a small change in risk is worth to "
            "the people who bear it. <bookmark mark='a'/> Take ten thousand people. <bookmark mark='b'/> Suppose "
            "each would accept nine hundred dollars a year to bear an extra risk of one in ten thousand of dying "
            "that year. <bookmark mark='c'/> Between them they accept nine million dollars, and on average one of "
            "them dies. That is the value of a statistical life: no one knows whose. <bookmark mark='d'/> It is a "
            "rate of exchange for small risks, measured in what people accept, and not the worth of anyone in "
            "particular."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.1))
            vo.wait_until("a")
            self.play(FadeIn(grid), FadeIn(lab), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(eq[0]))
            vo.wait_until("c")
            self.play(grid[1037].animate.set_color(COST).scale(2.2), FadeIn(eq[1]), FadeIn(eq[2]))
            vo.wait_until("d")
            self.play(FadeIn(eq[3]))
        self.clear_scene()

    def wages(self):
        V = load("vsl")
        r, w = np.array(V["risk"]), np.array(V["wage"])
        ax = plane([0, 3.0], [0, 70], center=LEFT * 2.8 + DOWN * 0.4, x_length=6.6, y_length=5.0,
                   xticks=[0, 1, 2, 3], yticks=[0, 20, 40, 60], xlabel=r"risk of death at work, \ per 10,000 a year"
                   .replace(",", "{,}"), ylabel=r"pay, \ thousands a year", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=15)
        pts = VGroup(*[Dot(ax.ax.c2p(min(x, 2.98), min(max(y, 0.5), 69.5)), radius=0.03, color=GREY_B)
                       .set_opacity(0.6) for x, y in zip(r, w)])
        bars = [(r"pay on risk", V["naive"], V["naive_se"], COST),
                (r"with ability \\ held fixed", V["controls"], V["controls_se"], BEN),
                (r"with ability, \\ risk mismeasured", V["noisy"], V["noisy_se"], SAFE)]
        bx = plane([-0.6, 2.6], [0, 12], center=RIGHT * 3.6 + DOWN * 0.6, x_length=4.6, y_length=4.2, xticks=[],
                   yticks=[0, 3, 6, 9, 12], ylabel=r"implied VSL, \ millions", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        truth = DashedLine(bx.ax.c2p(-0.6, V["truth"]), bx.ax.c2p(2.6, V["truth"]), color=ISL, stroke_width=2)
        tl = label(rf"planted: \ {V['truth']:.0f}", font_size=16, color=ISL).next_to(bx.ax.c2p(2.6, V["truth"]), UP,
                                                                                     buff=0.06).shift(LEFT * 0.5)
        brs, lbs, vls = VGroup(), VGroup(), VGroup()
        for k, (t_, v, se, c_) in enumerate(bars):
            p0, p1 = bx.ax.c2p(k - 0.3, 0), bx.ax.c2p(k + 0.3, v)
            brs.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=c_, fill_opacity=0.8,
                              stroke_width=0).move_to((p0 + p1) / 2))
            lbs.add(label(t_, font_size=14, color=c_).next_to(bx.ax.c2p(k, 0), DOWN, buff=0.12))
            vls.add(label(f"{v:.1f}", font_size=17, color=c_).next_to(brs[-1], UP, buff=0.06))
        tag = island_tag(rf"the Island: \ {V['n']:,} workers, \ 600 shown".replace(",", "{,}"), corner=DR,
                         font_size=12)
        with self.voiceover(
            "Where do such numbers come from? Mostly from pay. Richard Thaler and Sherwin Rosen, in 1976, asked how "
            "much more dangerous jobs pay, other things equal. <bookmark mark='a'/> Here are the Island's workers: "
            "the risk of death in each job, and its pay. On the Island the premium is planted: nine hundred dollars "
            "a year for each extra death in ten thousand, a value of a statistical life of nine million. <bookmark "
            f"mark='b'/> Regress pay on risk, and the value comes out at {V['naive']:.1f} million. Abler workers earn "
            "more and drift, a little, to safer jobs, so the safest jobs look well paid for reasons that have "
            f"nothing to do with safety. <bookmark mark='c'/> Hold ability fixed, and the estimate is "
            f"{V['controls']:.1f} million, close to the truth. <bookmark mark='d'/> But risk itself is measured from "
            "a few deaths in each occupation, and noisy, which pulls the estimate towards zero: "
            f"{V['noisy']:.1f} million. Real studies face both problems with fewer cures, which is part of why "
            "their estimates range from a few million to more than ten."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in pts], lag_ratio=0.002), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(bx), Create(truth), FadeIn(tl), GrowFromEdge(brs[0], DOWN), FadeIn(lbs[0]),
                      FadeIn(vls[0]))
            vo.wait_until("c")
            self.play(GrowFromEdge(brs[1], DOWN), FadeIn(lbs[1]), FadeIn(vls[1]))
            vo.wait_until("d")
            self.play(GrowFromEdge(brs[2], DOWN), FadeIn(lbs[2]), FadeIn(vls[2]))
        self.clear_scene()

    def dial(self):
        dial = dials.DIALS["vsl"]
        head = status_head(dial, r"the value of a statistical life \ (Part 18's Dial)")
        frame, rows = dial_rows(dial, 0, 16, [0, 4, 8, 12, 16], r"millions of 2024 dollars", top=1.6, step=0.75,
                                fmt="{:.1f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 11.6, 17, GREY_A).to_edge(DOWN, buff=0.5)
        tag = published_tag(r"the dial's record: \ explainer/economics/dials.py", corner=DR, font_size=12)
        e = dial.estimates
        with self.voiceover(
            "Part eighteen opened this Dial. <bookmark mark='a'/> The speed limits raised on rural interstates from "
            f"1987 give an upper bound of about {e[0].value:.0f} million of today's dollars. <bookmark mark='b'/> The "
            f"Environmental Protection Agency's value, from mostly wage-risk studies, is about {e[1].value:.1f} "
            f"million, and the Department of Transportation's {e[2].value:.1f}. <bookmark mark='c'/> The number moves "
            "with the method and the people asked, and the Island's own nine million sits inside the range."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()

    def age(self):
        V = load("vsl")
        S = tables.VALUES_58.data
        a40, a75 = V["by_age"]
        rows = VGroup(
            MathTex(r"\text{VSLY} = \frac{\text{VSL}}{\sum_{t=1}^{T} (1.03)^{-t}}", font_size=34, color=WHITE),
            label(rf"a VSL of {V['vsl_dot']:.1f} million for a 40-year-old with 40 years left: \ a life-year worth "
                  rf"{V['vsly']:.2f} million", font_size=22, color=TRAV),
            label(rf"the same life-years for a 75-year-old with 10 left: \ {a75['value']:.1f} million", font_size=22,
                  color=SAFE),
            label(rf"2003: \ an alternative estimate cut older people's VSL by {S['senior_cut']}\%; \ after protests, "
                  r"\ OMB told agencies to stop", font_size=22, color=COST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(DOWN * 0.2)
        head = label(r"the age question", font_size=32, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(r"OIRA memorandum, \ 30 May 2003; \ US DOT VSL guidance (2024)", corner=DL, font_size=12)
        with self.voiceover(
            "Is a statistical life the same at every age? <bookmark mark='a'/> One answer spreads it over the years "
            "left, as a value of a statistical life-year. <bookmark mark='b'/> At the Department of Transportation's "
            f"{V['vsl_dot']:.1f} million for a forty-year-old with forty years ahead, a life-year is worth about "
            f"{V['vsly']:.2f} million. <bookmark mark='c'/> Then saving a seventy-five-year-old with ten years left "
            f"is worth about {a75['value']:.1f} million, not {V['vsl_dot']:.1f}. <bookmark mark='d'/> In 2003 an "
            f"alternative estimate in an environmental analysis cut older people's value by {S['senior_cut']} "
            "percent. Critics called it a senior death discount, and the budget office told agencies to stop using "
            "the adjustment. American agencies use one value for every age; how much an older person's remaining "
            "years should count is a question the method raises and cannot settle."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.15))
        self.clear_scene()
