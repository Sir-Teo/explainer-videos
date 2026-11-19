from __future__ import annotations

from videos.economics.econ5.common import *  # noqa: F403

SAVE_COLOR = {"10": "#9AA5B8", "20": IC, "30": E.ACCENT}


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 12, r"In practice: \ reading wants from choices", r"Who measures what people want, and how?",
             "Chapter twelve. In practice: reading wants from choices.", lit=("households", "firms"),
             scale=("person", "firm", "market"))
        self.jobs()
        self.ferry()

    def jobs(self):
        head = VGroup(heading(r"In practice"),
                      label(r"who reads what people want from what they choose", font_size=26, color=GREY_B))
        head[1].next_to(head[0], DOWN, buff=0.2)
        items = [
            (r"market researchers", r"conjoint surveys: \ choose between product profiles, \ and the trade-offs "
                                    r"price each feature, \ even a patented one in court", E.ACCENT),
            (r"recommender teams", r"clicks, plays and purchases as revealed preference; \ the Netflix Prize "
                                   r"(2006--09) paid \$1 million for 10\%", "#C9A0FF"),
            (r"demand analysts", r"discrete-choice models of which car, which cereal, \ which airline: \ "
                                 r"the engine of Part 43", IC),
            (r"transport planners", r"the value of time from route and mode choices: \ McFadden's BART model, "
                                    r"\ and every road appraisal since", PASS),
            (r"pricing teams", r"price experiments: \ how many still buy when the price rises \ (Part 61)", BUDGET),
            (r"welfare economists", r"when choices conflict, \ which ones count? \ (Bernheim and Rangel, 2009; "
                                    r"Part 45)", VIOL),
        ]
        pc = point_cards(items, width=12.8, cols=2, font_size=22).move_to(DOWN * 0.55)
        with self.voiceover(
            "Who does this for a living? <bookmark mark='a'/> Market researchers, with conjoint surveys: people "
            "choose between product profiles, and the trade-offs they make put a price on each feature. Courts "
            "have used them to value a single patented feature of a phone. <bookmark mark='b'/> Recommender teams, "
            "who treat every click, play and purchase as revealed preference. Netflix offered a million dollars in "
            "2006 to anyone who could improve its recommendations by ten percent; a team claimed it in 2009. "
            "<bookmark mark='c'/> Demand analysts, who model which car or cereal or airline people pick. Part 43 "
            "builds their engine. <bookmark mark='d'/> Transport planners, who value time from the routes and modes "
            "people choose, as McFadden did. <bookmark mark='e'/> Pricing teams, running price experiments. "
            "<bookmark mark='f'/> And welfare economists, for the hardest question: when someone's choices "
            "contradict each other, which ones reveal what they really want? Douglas Bernheim and Antonio Rangel "
            "proposed an answer in 2009; Part 45 takes it up."
        ) as vo:
            self.play(FadeIn(head))
            for mark, c in zip("abcdef", pc.cards):
                vo.wait_until(mark)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def ferry(self):
        f = load("ferry")
        from explainer.ai.viz import axes

        ax = axes([0, 15], [0, 1], x_length=6.0, y_length=4.2, xticks=[0, 5, 10, 15], yticks=[0, 0.5, 1],
                  xfmt=lambda v: f"\\${v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%",
                  xlabel=r"extra fare for the fast ferry", ylabel=r"share choosing the fast ferry", font_size=18,
                  center=LEFT * 2.9 + DOWN * 0.3)
        a = ax.ax
        bins = np.array(f["bins"])
        mids = 0.5 * (bins[:-1] + bins[1:])
        groups = VGroup()
        curves = VGroup()
        for s in f["saves"]:
            col = SAVE_COLOR[str(s)]
            pts = [(m_, v) for m_, v in zip(mids, f["shares"][str(s)]) if v is not None]
            groups.add(VGroup(*[Dot(a.c2p(m_, v), radius=0.07, color=col) for m_, v in pts]))
            xs = np.linspace(0, 15, 150)
            p = 1 / (1 + np.exp(-(f["a"] * s + f["b"] * xs)))
            curves.add(VMobject(stroke_color=col, stroke_width=3).set_points_smoothly([a.c2p(x, y) for x, y in
                                                                                      zip(xs, p)]))
        half = DashedLine(a.c2p(0, 0.5), a.c2p(15, 0.5), color=GREY_C, stroke_width=1.5)
        x20 = -f["a"] * 20 / f["b"]
        mark = DashedLine(a.c2p(x20, 0), a.c2p(x20, 0.5), color=IC, stroke_width=2)
        key = VGroup(*[VGroup(Dot(radius=0.07, color=SAVE_COLOR[str(s)]),
                              label(rf"saves {s} min", font_size=18, color=SAVE_COLOR[str(s)])).arrange(RIGHT, buff=0.1)
                       for s in f["saves"]]).arrange(RIGHT, buff=0.35).next_to(ax, UP, buff=0.05).shift(RIGHT * 0.6)
        rows = VGroup(
            label(rf"{f['trips']:,} trips: \ a slow ferry, \ or a fast one \\ that saves 10, 20 or 30 minutes \\ for "
                  r"an extra fare".replace(",", "{,}"), font_size=22),
            MathTex(r"P(\text{fast}) = \frac{1}{1 + e^{-(a\,\text{minutes} + b\,\text{fare})}}", font_size=32),
            label(rf"the fare that splits travellers half and half: \\ the value of the time saved: \ "
                  rf"\${x20:.2f} for 20 minutes", font_size=22, color=IC),
            label(rf"value of time $= -a/b$: \ \${f['vot']:.2f} an hour \ (s.e.\ {f['vot_se']:.2f}); \\ planted "
                  rf"\${f['truth']:.0f}", font_size=24, color=E.TRUTH),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.4)
        tag = island_tag(r"simulated: the Island's ferry survey, logistic taste shocks", corner=DR, font_size=13)
        with self.voiceover(
            "Here is the transport planner's job in miniature. <bookmark mark='a'/> The Island's ferry company "
            f"surveys {f['trips']:,} trips. Each time, a traveller chooses between the slow ferry and a fast one "
            "that saves ten, twenty or thirty minutes, for an extra fare. <bookmark mark='b'/> The more it costs, "
            "the fewer take the fast ferry; the more time it saves, the more do. <bookmark mark='c'/> A logit model, "
            "McFadden's random utility, fits a curve to each group. <bookmark mark='d'/> Where a curve crosses "
            "one half, travellers are split evenly: that extra fare is what the time saved is worth to the typical "
            f"traveller, about {x20:.0f} dollars for twenty minutes. <bookmark mark='e'/> The ratio of the two "
            f"coefficients gives the value of time: {f['vot']:.2f} dollars an hour, against the fifteen we "
            "planted. Road and rail projects are judged by numbers like this: most of the benefit of a new bridge "
            "is the time it saves."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[FadeIn(g) for g in groups], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(*[Indicate(g, scale_factor=1.15) for g in groups])
            vo.wait_until("c")
            self.play(Write(rows[1]), LaggedStart(*[Create(c_) for c_ in curves], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("d")
            self.play(Create(half), Create(mark), FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
