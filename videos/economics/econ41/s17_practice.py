from __future__ import annotations

from videos.economics.econ41.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 15, r"In practice: \ scoring a tax change", r"How do tax offices predict revenue?",
             "Chapter fifteen. In practice: scoring a tax change.", lit={2017: r"the Tax Cuts and Jobs Act"},
             scale=("nation",), horizon=("a decade",))
        self.jobs()
        self.score()
        self.called()

    def jobs(self):
        rows = VGroup(
            label(r"budget offices \ (CBO, \ the Joint Committee on Taxation, \ the OBR): \ revenue estimates",
                  font_size=21, color=TOP),
            label(r"treasuries' tax-policy offices: \ design, \ distributional tables (Part 40)", font_size=21,
                  color=RATE),
            label(r"tax authorities' research units: \ audits, \ the tax gap, \ experiments", font_size=21,
                  color=WORKER),
            label(r"firms and advisers: \ where to book profits, \ how to pay", font_size=21, color=CAPITAL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(DOWN * 0.2)
        head = label(r"the people who do this", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Who does this for a living? <bookmark mark='a'/> Budget offices, like America's Congressional Budget "
            "Office and Joint Committee on Taxation or Britain's Office for Budget Responsibility, estimate what each "
            "proposal will raise. <bookmark mark='b'/> Treasury tax-policy offices design the changes and build "
            "the distributional tables of Part forty. <bookmark mark='c'/> Research units inside tax authorities "
            "measure the tax gap and run experiments, like Denmark's audits. <bookmark mark='d'/> And on the other "
            "side, firms and their advisers decide where profits are booked and how people are paid."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def score(self):
        S = load("score")
        c40, c30 = S["cases"]["0.40"], S["cases"]["0.30"]
        rows = [(r"raise the top rate \\ 37\% $\to$ 40\%", c40), (r"cut it \\ 37\% $\to$ 30\%", c30)]
        groups = VGroup()
        for k, (nm, c) in enumerate(rows):
            y = 1.1 - 2.2 * k
            vals = [(r"static", c["static"], GREY_B), (r"$e$ = 0.25", c["dynamic"]["0.25"], TOP),
                    (r"$e$ = 1", c["dynamic"]["1.0"], LOSS)]
            g = VGroup(label(nm, font_size=20, color=WHITE).move_to(np.array([-4.8, y, 0])))
            for j, (lab_, v, col) in enumerate(vals):
                yy = y + 0.45 - 0.45 * j
                w = abs(v) * 30
                r = Rectangle(width=max(w, 0.03), height=0.32, stroke_width=0, fill_color=col,
                              fill_opacity=0.85).move_to(np.array([-1.4 + (w / 2 if v > 0 else -w / 2), yy, 0]))
                pctv = 100 * v / c["static"]
                g.add(VGroup(r, label(lab_, font_size=16, color=col).next_to(np.array([-1.5 - (w if v < 0 else 0), yy,
                                                                                         0]), LEFT, buff=0.1),
                             label(f"{pctv:.0f}\\% of static", font_size=16, color=col).next_to(
                                 np.array([-1.4 + max(w, 0) if v > 0 else -1.3, yy, 0]), RIGHT, buff=0.1)))
            groups.add(g)
        axis = Line(np.array([-1.4, 2.0, 0]), np.array([-1.4, -2.6, 0]), color=GREY_B, stroke_width=2)
        head = label(r"revenue from the top bracket: \ static against behavioural scores", font_size=24,
                     color=E.ACCENT).to_edge(UP, buff=0.4)
        side = label(r"a static score holds \\ incomes fixed; \\ a behavioural score \\ lets them respond",
                     font_size=18,
                     color=GREY_A).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.3)
        tag = data_tag(rf"computed: \ the 2022 Pareto parameter, \ $a$ = {S['a']:.2f}", corner=DR, font_size=12)
        with self.voiceover(
            "Scoring a tax change means predicting its revenue, and the elasticity decides the answer. Take "
            "America's top bracket, with the Pareto parameter from the tax data. <bookmark mark='a'/> Raise the top "
            "rate from thirty-seven to forty percent. A static score, which holds incomes fixed, counts the full "
            "mechanical gain. <bookmark mark='b'/> With an elasticity of a quarter, the government keeps "
            f"{100 * c40['dynamic']['0.25'] / c40['static']:.0f} percent of it. <bookmark mark='c'/> With an "
            "elasticity "
            "of one, almost nothing: forty percent is near the top of the curve. <bookmark mark='d'/> Now cut the "
            "rate to thirty percent. With an elasticity of a quarter, the government loses "
            f"{100 * c30['dynamic']['0.25'] / c30['static']:.0f} percent of the static loss; with an elasticity of "
            f"one, only {100 * c30['dynamic']['1.0'] / c30['static']:.0f} percent. Tax cuts pay for themselves only "
            "when rates start above the top of the curve."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axis), FadeIn(tag), FadeIn(side), FadeIn(groups[0][0]),
                      FadeIn(groups[1][0]))
            vo.wait_until("a")
            self.play(FadeIn(groups[0][1]))
            vo.wait_until("b")
            self.play(FadeIn(groups[0][2]))
            vo.wait_until("c")
            self.play(FadeIn(groups[0][3]))
            vo.wait_until("d")
            self.play(FadeIn(groups[1][1:]))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["tcja_2017"]
        R = load("receipts")
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.6,
                       font_size=21)
        foot = label(rf"federal receipts: \ {R['r2017']:.1f}\% of GDP in 2017, \ {R['r2018']:.1f}\% in 2018, \ "
                     rf"{R['r2019']:.1f}\% in 2019; \ CBO: \ +\${R['cbo']['cbo_total']} trillion to deficits, "
                     r"2018--28", font_size=18, color=GREY_A).to_edge(DOWN, buff=0.5)
        tag = published_tag(tables.TCJA_2017.tag + r"; \ OMB via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> In September 2017, Steven Mnuchin, Secretary of the Treasury, said of "
            "the tax plan that became law that December: not only will this tax plan pay for itself, but it will pay "
            "down debt. <bookmark mark='b'/> Federal receipts fell from "
            f"{R['r2017']:.1f} percent of GDP in fiscal 2017 to {R['r2018']:.1f} percent in 2018. In April 2018 the "
            f"Congressional Budget Office estimated that the law would add about {R['cbo']['cbo_total']} trillion "
            "dollars to deficits over ten years, after counting the extra growth it expected. "
            "<bookmark mark='c'/> The verdict: wrong. American rates were well below the top of the Laffer curve, "
            "which is where tax cuts lose money."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag))
            vo.wait_until("b")
            self.play(Indicate(cc.right, color=WHITE, scale_factor=1.01), FadeIn(foot))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3))
        self.clear_scene()
