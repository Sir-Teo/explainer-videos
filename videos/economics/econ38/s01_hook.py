from __future__ import annotations

from videos.economics.econ38.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.calls()
        self.timeline()
        self.question()
        self.title()
        self.objectives()

    def calls(self):
        rng = np.random.default_rng(1992)
        river = VMobject(stroke_color="#3B6E8F", stroke_width=10).set_points_smoothly(
            [np.array([0.4 + 0.35 * np.sin(k), 3.2 - 1.0 * k, 0]) for k in np.linspace(0, 6.4, 12)])
        nj = VGroup(*[Dot(np.array([rng.uniform(-6.2, -0.6), rng.uniform(-2.9, 2.6), 0]), radius=0.045, color=NJ)
                      for _ in range(331)])
        pa = VGroup(*[Dot(np.array([rng.uniform(1.2, 6.2), rng.uniform(-2.9, 2.6), 0]), radius=0.045, color=PA)
                      for _ in range(79)])
        ln = label(r"New Jersey: \ 331 restaurants", font_size=24, color=NJ).move_to(np.array([-3.4, 3.2, 0]))
        lp = label(r"eastern Pennsylvania: \ 79", font_size=24, color=PA).move_to(np.array([3.7, 3.2, 0]))
        lr = label(r"the Delaware", font_size=16, color="#5F9EC0").move_to(np.array([0.9, -3.4, 0]))
        chains = label(r"Burger King, \ KFC, \ Roy Rogers, \ Wendy's", font_size=18, color=GREY_A).to_edge(DOWN,
                                                                                                   buff=0.2)
        tag = data_tag(r"Card and Krueger (1994), \ public data", corner=DR, font_size=12)
        mw = VGroup(
            VGroup(label(r"New Jersey's minimum wage", font_size=26, color=NJ),
                   label(r"\$4.25 $\to$ \$5.05", font_size=48, color=NJ),
                   label(r"from 1 April 1992: \ +19\%", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.25).move_to(
                np.array([-3.4, 0.2, 0])),
            VGroup(label(r"Pennsylvania's", font_size=26, color=PA), label(r"\$4.25", font_size=48, color=PA),
                   label(r"unchanged", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.25).move_to(
                np.array([3.7, 0.2, 0])))
        with self.voiceover(
            "Early in 1992, New Jersey was about to raise its minimum wage, on the first of April, from four dollars "
            "and twenty-five cents an hour to five dollars and five cents, a rise of nearly a fifth. Pennsylvania, "
            "across the Delaware, would stay at four twenty-five. <bookmark mark='a'/> Two economists at Princeton, "
            "David Card and Alan Krueger, saw an experiment. In February and March they telephoned 410 fast-food "
            "restaurants, <bookmark mark='b'/> 331 in New Jersey <bookmark mark='c'/> and 79 in eastern "
            "Pennsylvania, Burger Kings, KFCs, Roy Rogers and Wendy's, and asked how many people they employed and "
            "what they paid. <bookmark mark='d'/> In November and December they called them all again."
        ) as vo:
            self.play(Create(river), FadeIn(lr), FadeIn(tag), run_time=1.5)
            self.play(FadeIn(mw[0], shift=UP * 0.15))
            self.play(FadeIn(mw[1], shift=UP * 0.15))
            vo.wait_until("a")
            self.play(FadeIn(chains))
            vo.wait_until("b")
            self.play(FadeOut(mw), run_time=0.6)
            self.play(FadeIn(ln), LaggedStart(*[FadeIn(d, scale=2) for d in nj], lag_ratio=0.004), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(lp), LaggedStart(*[FadeIn(d, scale=2) for d in pa], lag_ratio=0.02), run_time=1.5)
            vo.wait_until("d")
            self.play(LaggedStart(*[Indicate(d, color=WHITE, scale_factor=2.0) for d in list(nj)[::6] + list(pa)[::2]],
                                  lag_ratio=0.01), run_time=3.0)
        self.clear_scene()

    def timeline(self):
        tl = NumberLine(x_range=[0, 12, 1], length=11.0, include_numbers=False, color=GREY_B).move_to(DOWN * 0.3)
        months = VGroup(*[label(m, font_size=16, color=GREY_A).next_to(tl.n2p(k + 0.5), DOWN, buff=0.15)
                          for k, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split())])
        w1 = Rectangle(width=tl.n2p(3)[0] - tl.n2p(1)[0], height=0.5, fill_color=GREY_B, fill_opacity=0.5,
                       stroke_width=0).move_to((tl.n2p(1) + tl.n2p(3)) / 2 + UP * 0.45)
        w2 = Rectangle(width=tl.n2p(12)[0] - tl.n2p(10)[0], height=0.5, fill_color=GREY_B, fill_opacity=0.5,
                       stroke_width=0).move_to((tl.n2p(10) + tl.n2p(12)) / 2 + UP * 0.45)
        l1 = label(r"first calls", font_size=18, color=WHITE).next_to(w1, UP, buff=0.1)
        l2 = label(r"second calls", font_size=18, color=WHITE).next_to(w2, UP, buff=0.1)
        rise = Arrow(tl.n2p(3) + UP * 2.2, tl.n2p(3) + UP * 0.2, color=NJ, buff=0, stroke_width=4)
        lr = label(r"1 April: \ New Jersey \\ \$4.25 $\to$ \$5.05", font_size=20, color=NJ).next_to(rise, UP,
                                                                                              buff=0.1)
        pred = label(r"the textbook: \ employment in New Jersey falls", font_size=24, color=LOSS).to_edge(DOWN,
                                                                                                    buff=0.8)
        head = label(r"1992", font_size=34, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(tables.CK_1994.tag, corner=DR, font_size=12)
        with self.voiceover(
            "Here is their year. <bookmark mark='a'/> The first calls, before the rise. <bookmark mark='b'/> On "
            "the first of April New Jersey's minimum went up. <bookmark mark='c'/> The second calls, eight months "
            "later. <bookmark mark='d'/> The textbook made a clear prediction: a price floor above the market wage "
            "means employers hire fewer workers, so employment in New Jersey's restaurants should fall relative to "
            "Pennsylvania's. What happened is the subject of this part's first game."
        ) as vo:
            self.play(FadeIn(head), Create(tl), FadeIn(months), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(w1), FadeIn(l1))
            vo.wait_until("b")
            self.play(GrowArrow(rise), FadeIn(lr))
            vo.wait_until("c")
            self.play(FadeIn(w2), FadeIn(l2))
            vo.wait_until("d")
            self.play(FadeIn(pred))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 38, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"how much do people choose to work, \ and why?", font_size=26, color=SUPPLY),
            label(r"what does a minimum wage do to jobs, \ and why do studies disagree?", font_size=26, color=NJ),
            label(r"what is a year of school worth, \ and how can we tell?", font_size=26, color=SCHOOL),
            label(r"who chooses which work, \ and what does that hide?", font_size=26, color=FISH),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(q, DOWN, buff=0.6)
        with self.voiceover(
            "This part's question: what sets a wage, and what happens when the law sets it instead? "
            "<bookmark mark='a'/> How much do people choose to work, and why? <bookmark mark='b'/> What does a "
            "minimum wage do to jobs, and why do careful studies disagree? <bookmark mark='c'/> What is a year of "
            "school worth, and how could anyone tell? <bookmark mark='d'/> And who chooses which work, and what does "
            "that choice hide from a researcher?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        F = load("film")
        mini = plane([1938, 2025], [0, 16], x_length=4.2, y_length=1.4)
        logo = path(mini, F["t"], F["v"], WAGE, 2.6, smooth=False)
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 38 \ $\cdot$ \ Work and Wages", font_size=34, color=E.ACCENT)
        VGroup(logo, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part thirty-eight: work and wages."):
            self.play(Create(logo), run_time=1.6)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act VIII \ $\cdot$ \ Work and the State", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"a game; \ labour supply and its three elasticities; \ cab drivers and Uber",
            r"labour demand and a wage floor; \ Card and Krueger's border; \ the bunching estimator",
            r"monopsony, \ and the same design run on the Island under both theories",
            r"human capital; \ Mincer's equation; \ the return to schooling by several designs",
            r"selection and Roy's model; \ the Mariel boatlift; \ three dials",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "Here is the plan. <bookmark mark='a'/> A game; how much people choose to work, with three different "
            "elasticities; and cab drivers. <bookmark mark='b'/> Labour demand and a wage floor; Card and Krueger's "
            "border; and a newer way to count missing jobs. <bookmark mark='c'/> Monopsony, and the same design run on "
            "the Island under both theories. <bookmark mark='d'/> Human capital and Mincer's equation, and the return "
            "to a year of school by several designs. <bookmark mark='e'/> Selection and Roy's model, the Mariel "
            "boatlift, and three dials."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
