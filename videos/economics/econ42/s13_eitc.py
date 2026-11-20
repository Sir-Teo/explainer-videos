from __future__ import annotations

from videos.economics.econ42.common import *  # noqa: F403


class EITC(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Help for the working poor", r"How do you help the poor without discouraging work?",
             "Chapter eleven. Help for the working poor.", lit={1968: r"the negative income tax experiments",
                                                               1978: r"Akerlof", 1996: r"Eissa and Liebman"},
             scale=("household", "nation"), horizon=("a year",))
        self.nit()
        self.schedule()
        self.response()
        self.tagging()

    def nit(self):
        N = tables.NIT_1968.data
        vals = [(r"husbands", N["husbands"], UNEMP), (r"wives", N["wives"], HEALTH),
                (r"single mothers", N["single"], PENSION)]
        bars = VGroup()
        for k, (nm, v, col) in enumerate(vals):
            y = 0.9 - 1.1 * k
            w = v * 0.2
            r = Rectangle(width=w, height=0.5, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                np.array([-1.0 + w / 2, y, 0]))
            bars.add(VGroup(label(nm, font_size=21, color=WHITE).next_to(np.array([-1.1, y, 0]), LEFT, buff=0.1),
                            r, label(rf"about $-${v}\%", font_size=20, color=col).next_to(r, RIGHT, buff=0.12)))
        head = label(r"the negative income tax experiments, \ 1968--1982: \ change in hours worked", font_size=24,
                     color=E.ACCENT).to_edge(UP, buff=0.5)
        sub = label(rf"four American experiments; \ the largest, \ in Seattle and Denver, \ about "
                    rf"{N['families_sd']:,} families", font_size=19, color=GREY_A).next_to(head, DOWN, buff=0.2)
        foot = label(r"a guaranteed income, \ withdrawn as earnings rise, \ taxes work twice", font_size=21,
                     color=HOLD).to_edge(DOWN, buff=0.8)
        tag = published_tag(tables.NIT_1968.tag, corner=DR, font_size=11)
        with self.voiceover(
            "How do you help people with low incomes without discouraging the work that would raise them? In the "
            "late 1960s the United States ran experiments on Milton Friedman's idea of a negative income tax: a "
            "guaranteed income, withdrawn gradually as earnings rise. Four experiments ran between 1968 and 1982; "
            "the largest, in Seattle and Denver, enrolled about 4,800 families. <bookmark mark='a'/> In Philip "
            "Robins's summary, husbands worked about five percent fewer hours, <bookmark mark='b'/> wives about "
            "twenty percent fewer, <bookmark mark='c'/> and single mothers about thirteen percent fewer. "
            "<bookmark mark='d'/> The reason is built in: a guarantee pays people who do not work, and withdrawing it "
            "as earnings rise is a tax on every extra hour."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub), FadeIn(tag), *[FadeIn(b_[0]) for b_ in bars])
            self.play(*[GrowFromEdge(b_[1], LEFT) for b_ in bars], run_time=1.5)
            for mk, b_ in zip("abc", bars):
                vo.wait_until(mk)
                self.play(FadeIn(b_[2]), Indicate(b_[1], color=WHITE, scale_factor=1.03))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def schedule(self):
        E_ = load("eitc")
        T = E_["table"]
        z = np.array(E_["z"]) / 1000
        cr = np.array(E_["credit"]) / 1000
        ax = plane([0, 70], [0, 9], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[0, 10, 20, 30, 40, 50, 60, 70], yticks=[0, 2, 4, 6, 8],
                   xlabel=r"earnings, \ thousands of dollars", ylabel=r"credit, \ thousands of dollars",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        ln = path(ax, z, cr, GAIN, 3.6, smooth=False)
        side = VGroup(
            label(r"2025, \ three or more \\ children, \ single filer", font_size=17, color=GREY_A),
            label(rf"phase-in: \ {100 * T['rate_in']:.0f}\% of earnings \\ up to \${T['top']:,}: \ a wage "
                  rf"subsidy", font_size=18, color=GAIN),
            label(rf"plateau: \ \${T['max']:,}", font_size=18, color=WHITE),
            label(rf"phase-out: \ {100 * T['rate_out']:.2f}\% from \\ \${T['start_out']:,}, \ gone at \\ "
                  rf"\${E_['check_end']:,.0f}", font_size=18, color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        tag = published_tag(tables.EITC_2025.tag, corner=DR, font_size=11)
        with self.voiceover(
            "America chose a different design: the Earned Income Tax Credit, paid only to those who work. "
            "<bookmark mark='a'/> Here is the 2025 schedule for a single parent with three or more children. "
            f"<bookmark mark='b'/> For the first {T['top']:,} dollars of earnings, the credit adds forty-five cents "
            "to each dollar earned: a wage subsidy, a negative marginal tax rate. <bookmark mark='c'/> It then stays "
            f"at its maximum, {T['max']:,} dollars, <bookmark mark='d'/> and from {T['start_out']:,} dollars it is "
            f"withdrawn at about twenty-one cents per dollar, until it is gone at about "
            f"{E_['check_end']:,.0f} dollars. The withdrawal is a tax on extra work, but only for those already "
            "working; for someone deciding whether to work at all, the credit is pure reward."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=1.0)
            self.play(Create(ln), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), Indicate(ln, color=WHITE, scale_factor=1.0))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def response(self):
        E_ = load("eitc")
        T = E_["table"]
        M = E_["mvpf"]
        rows = VGroup(
            label(rf"Eissa and Liebman: \ after the 1986 expansion, \ single mothers' participation rose \ (by "
                  rf"{T['el_pp']} points from {T['el_base']}\%, \ working paper)", font_size=20, color=GAIN),
            label(r"and those already working did not cut their hours", font_size=20, color=GREY_A),
            label(rf"the Island: \ a 10\% larger credit draws in {100 * (M['work1'] - M['work0']):.1f}\% more "
                  rf"parents \ ({100 * M['work0']:.1f}\% $\to$ {100 * M['work1']:.1f}\%)", font_size=20,
                  color=UNEMP),
            label(rf"they pay tax and stop drawing welfare: \ {abs(100 * M['per_dollar_fe']):.0f} cents of each "
                  r"dollar come back", font_size=20, color=GAIN),
            label(rf"value per net dollar: \ {M['mvpf']:.2f} \ (chapter 13)", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(UP * 0.1)
        head = label(r"what the credit does to work", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(tables.EITC_2025.tag + r"; \ the Island", corner=DR, font_size=11)
        with self.voiceover(
            "Does it work? <bookmark mark='a'/> In 1996 Nada Eissa and Jeffrey Liebman compared single women with "
            "and without children, before and after the credit was expanded in 1986: the mothers' participation "
            "in the labour force rose, <bookmark mark='b'/> and those already working did not cut their hours. "
            "<bookmark mark='c'/> On the Island, single parents decide whether to work, weighing earnings, the "
            "credit and the cost of a job against a welfare benefit. A credit ten percent larger draws in "
            f"{say_pct(M['work1'] - M['work0'], 1)} more parents. <bookmark mark='d'/> Those new workers pay "
            f"payroll tax and stop drawing welfare, so about {abs(100 * M['per_dollar_fe']):.0f} cents of each "
            f"dollar comes back. <bookmark mark='e'/> Each net dollar spent delivers {M['mvpf']:.2f} dollars of "
            "value: a number that chapter thirteen puts on a common scale."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0]))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def tagging(self):
        G = load("eitc")["tagging"]
        cells = VGroup()
        for k, (nm, v, col) in enumerate(((r"a payment to everyone", G["universal"], GREY_B),
                                          (r"a payment to the tagged", G["tagged"], GAIN))):
            x = -3.4 + 4.2 * k
            sq = VGroup(*[Square(side_length=0.3, stroke_width=0, fill_color=col if j < round(100 * v) else GREY_D,
                                 fill_opacity=0.9) for j in range(100)])
            sq.arrange_in_grid(rows=10, cols=10, buff=0.05).move_to(np.array([x, -0.2, 0]))
            cells.add(VGroup(sq, label(nm, font_size=20, color=col).next_to(sq, UP, buff=0.2),
                             label(rf"{100 * v:.0f}\% reaches the needy", font_size=19, color=col).next_to(
                                 sq, DOWN, buff=0.2)))
        side = VGroup(
            label(rf"the Island: \ {100 * G['universal']:.0f}\% \\ are needy", font_size=18, color=GREY_A),
            label(r"a tag \ (a disability, \\ children, \ age) \ catches \\ 70\% of them, \\ 10\% of the rest",
                  font_size=17, color=WHITE),
            label(rf"but misses {100 * G['missed']:.0f}\% \\ of the needy", font_size=18, color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Akerlof, \ \emph{AER} (1978); \ the Island", corner=DR, font_size=11)
        with self.voiceover(
            "There is another way to avoid taxing work: base help on something people cannot easily change. "
            "George Akerlof called it tagging in 1978. <bookmark mark='a'/> On the Island a fifth of people are "
            "needy. A payment to everyone sends only a fifth of each dollar to them. <bookmark mark='b'/> A tag, "
            "such as a disability, young children or old age, catches seventy percent of the needy and ten percent "
            f"of the rest. Pay only the tagged, and {say_pct(G['tagged'], 0)} of each dollar reaches the needy, "
            "and because the tag cannot be earned by working less, it does not discourage work. "
            f"<bookmark mark='c'/> The price: {say_pct(G['missed'], 0)} of the needy have no tag and get nothing. "
            "Every targeted programme makes this trade between reaching the needy and leaving some out."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(cells[0]), FadeIn(side[0]), run_time=1.2)
            vo.wait_until("b")
            self.play(FadeIn(cells[1]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()
