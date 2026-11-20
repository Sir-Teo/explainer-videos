from __future__ import annotations

from videos.economics.econ41.common import *  # noqa: F403


class Mirrlees(VoiceoverScene):
    def construct(self):
        card(self, 5, r"The income tax as an information problem", r"Why can't the government just tax ability?",
             "Chapter five. The income tax as an information problem.", lit={1971: r"Mirrlees", 1998: r"Diamond"},
             scale=("person", "nation"), horizon=("a year",))
        self.problem()
        self.formula()
        self.factors()

    def problem(self):
        steps = flow_chain([(r"ability \\ (unseen)", WORKER), (r"effort \\ (unseen)", RATE), (r"income \\ (seen)", TOP),
                            (r"the tax", REVENUE)],
                           notes=[r"what society \\ would like \\ to tax", r"what people \\ choose",
                                  r"ability times \\ effort", r"can depend \\ only on income"], box_w=2.6,
                           font_size=20,
                           note_size=15).move_to(UP * 1.0)
        warn = label(r"tax income heavily, \ and the able earn less: \ every schedule trades equity against "
                     r"incentives", font_size=21, color=E.ACCENT).to_edge(DOWN, buff=1.0)
        hc = label(r"James Mirrlees, \ 1971", font_size=22, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "In 1971 James Mirrlees turned the income tax into a precise problem. People differ in ability, and a "
            "government that cared about equality would like to tax ability itself, which no one can change. "
            "<bookmark mark='a'/> But ability is invisible. <bookmark mark='b'/> So is effort, which people choose. "
            "<bookmark mark='c'/> What the tax office sees is income, ability times effort. <bookmark mark='d'/> So "
            "the tax can depend only on income, and an able person facing a high rate can choose to earn less, and "
            "pay less. Every income tax trades equality against incentives, and the question is how to make that "
            "trade as well as possible, rate by rate, along the whole schedule."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(steps.boxes[0]), FadeIn(steps.notes[0]))
            vo.wait_until("a")
            self.play(Indicate(steps.boxes[0], color=WORKER))
            vo.wait_until("b")
            self.play(GrowArrow(steps.arrows[0]), FadeIn(steps.boxes[1]), FadeIn(steps.notes[1]))
            vo.wait_until("c")
            self.play(GrowArrow(steps.arrows[1]), FadeIn(steps.boxes[2]), FadeIn(steps.notes[2]))
            vo.wait_until("d")
            self.play(GrowArrow(steps.arrows[2]), FadeIn(steps.boxes[3]), FadeIn(steps.notes[3]), FadeIn(warn))
        self.clear_scene()

    def formula(self):
        eq = MathTex(r"\frac{T'(z)}{1 - T'(z)}", r"=", r"\Big(1 + \frac{1}{e}\Big)", r"\cdot",
                     r"\frac{1 - F(w)}{w\, f(w)}", r"\cdot", r"\big(1 - \bar g(w)\big)", font_size=42).move_to(UP * 1.2)
        labs = VGroup(
            label(r"A: \ how much people \\ respond to the rate \\ (less response, \\ higher rate)", font_size=18,
                  color=RATE),
            label(r"B: \ how many people \\ earn more, \ against \\ how many are \\ at this level", font_size=18,
                  color=TOP),
            label(r"C: \ how little society \\ values a dollar for \\ everyone above", font_size=18,
                  color=WORKER),
        ).arrange(RIGHT, buff=0.8, aligned_edge=UP).next_to(eq, DOWN, buff=0.7)
        for lab_, part in zip(labs, (eq[2], eq[4], eq[6])):
            lab_.set_x(part.get_x())
        gaps = [labs[k + 1].get_left()[0] - labs[k].get_right()[0] for k in range(2)]
        if min(gaps) < 0.25:
            labs.arrange(RIGHT, buff=0.6, aligned_edge=UP).next_to(eq, DOWN, buff=0.7)
        foot = label(r"Diamond (1998): \ quasi-linear preferences, \ skills $w$ distributed $F$, \ welfare weights "
                     r"$g$", font_size=18, color=GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "In 1998 Peter Diamond wrote the answer in a form anyone can read. The marginal rate at each level of "
            "income, as a ratio of the rate to what it leaves, is a product of three factors. "
            "<bookmark mark='a'/> A: one plus one over the elasticity of earnings. The less people respond, the "
            "higher the rate can be. <bookmark mark='b'/> B: the number of people above this level, against the "
            "number at it, scaled by skill. A higher rate at one income raises revenue from everyone above it, but "
            "distorts only those at it. <bookmark mark='c'/> C: one minus the average value society places on a "
            "dollar for all those above. The less society cares about extra income at the top, the higher the rate."
        ) as vo:
            self.play(Write(eq), FadeIn(foot), run_time=2.0)
            vo.wait_until("a")
            self.play(Indicate(eq[2], color=RATE), FadeIn(labs[0]))
            vo.wait_until("b")
            self.play(Indicate(eq[4], color=TOP), FadeIn(labs[1]))
            vo.wait_until("c")
            self.play(Indicate(eq[6], color=WORKER), FadeIn(labs[2]))
        self.clear_scene()

    def factors(self):
        M = load("mirrlees")
        lz = np.log10(np.array(M["z_rel"]))
        B, C = np.array(M["B"]), np.array(M["C"])
        axb = plane([-0.7, 1.7], [-0.5, 1.2], center=LEFT * 3.3 + DOWN * 0.3, x_length=5.4, y_length=4.2,
                    xticks=[-0.5, 0, 0.5, 1.0, 1.5], yticks=[np.log10(v) for v in (0.5, 1, 2, 5, 10)],
                    xlabel=r"income, \ median = 1 \ (log)", ylabel=r"B \ (log scale)",
                    xfmt=lambda v: f"{10 ** v:.2g}", yfmt=lambda v: f"{10 ** v:g}", font_size=13)
        axc = plane([-0.7, 1.7], [0, 1.0], center=RIGHT * 3.3 + DOWN * 0.3, x_length=5.4, y_length=4.2,
                    xticks=[-0.5, 0, 0.5, 1.0, 1.5], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                    xlabel=r"income, \ median = 1 \ (log)", ylabel=r"C", xfmt=lambda v: f"{10 ** v:.2g}",
                    yfmt=lambda v: f"{v:.2f}", font_size=13)
        m = (lz >= -0.7) & (lz <= 1.7)
        lb = path(axb, lz[m], np.log10(B[m]), TOP, 3.2, yr=(-0.5, 1.2))
        lc = path(axc, lz[m], C[m], WORKER, 3.2)
        tail = seg(axb, 0.6, np.log10(1 / M["alpha"]), 1.7, np.log10(1 / M["alpha"]), GREY_B, 1.8, dashed=True)
        nb = label(rf"in the Pareto tail: \ $1/\alpha$ = {1 / M['alpha']:.1f}", font_size=15, color=GREY_A).next_to(
            axb.ax.c2p(1.15, np.log10(1 / M["alpha"])), UP, buff=0.12)
        head = label(r"the Island: \ skills lognormal, \ with a Pareto tail; \ weights falling with skill",
                     font_size=20, color=GREY_A).to_edge(UP, buff=0.4)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "On the Island, with skills spread like real incomes and a Pareto tail at the top, the factors move in "
            "opposite directions. <bookmark mark='a'/> B is very large at low incomes, where few people sit at each "
            "level and almost everyone is above, and it falls through the middle. <bookmark mark='b'/> In the tail it "
            "settles at one over the Pareto exponent: the shape of the top fixes it. <bookmark mark='c'/> C rises "
            "from zero at the bottom, where those above include nearly everyone and their average weight is the "
            "average, towards one at the top, whose extra dollars society values least. The product of falling B "
            "and rising C is the shape of the optimal schedule, chapter seven's subject."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axb), FadeIn(axc), FadeIn(tag), run_time=1.0)
            self.play(Create(lb), run_time=2.5)
            vo.wait_until("a")
            self.play(Indicate(lb, color=WHITE, scale_factor=1.02))
            vo.wait_until("b")
            self.play(Create(tail), FadeIn(nb))
            vo.wait_until("c")
            self.play(Create(lc), run_time=2.0)
        self.clear_scene()
