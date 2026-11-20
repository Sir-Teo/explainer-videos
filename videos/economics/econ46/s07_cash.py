from __future__ import annotations

from videos.economics.econ46.common import *  # noqa: F403


class Cash(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Cash", r"What happens when you simply give poor people money?",
             "Chapter six. Cash.", lit={2004: r"Schultz", 2016: r"Haushofer and Shapiro", 2022: r"Egger et al."},
             scale=("household", "village"), horizon=("a year", "three years"))
        self.progresa()
        self.givedirectly()
        self.multiplier()
        self.panes()

    def progresa(self):
        T = tables.CASH_46.data
        chain = flow_chain([(r"mothers paid \\ every two months", CASH), (r"if children \\ attend school", SCHOOL),
                            (r"and the family \\ visits the clinic", HEALTH),
                            (r"the roll-out \\ in random order", TRIAL)],
                           notes=[r"Mexico, \ 1997: \\ PROGRESA", r"larger grants \\ for older children",
                                  r"conditional \\ cash transfers", rf"{T['treated']} of {T['localities']} \\ "
                                  r"localities first"],
                           box_w=2.8, font_size=19, note_size=16).move_to(UP * 0.9)
        res = VGroup(
            label(r"primary enrolment was already high: \ about one point more", font_size=21, color=GREY_A),
            label(r"the gains came after primary school, \ where children had dropped out", font_size=21,
                  color=SCHOOL),
            label(r"Schultz, \ 2004: \ a return of about 8\% a year on the grants, \ counted as schooling",
                  font_size=21,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.6)
        tag = published_tag(tables.CASH_46.tag, corner=DR, font_size=11)
        with self.voiceover(
            "In 1997 Mexico's government launched PROGRESA. <bookmark mark='a'/> Poor mothers were paid every two "
            "months, <bookmark mark='b'/> on condition that their children went to school, with larger grants for "
            "older children, who were the ones most likely to leave, <bookmark mark='c'/> and that the family "
            "visited the health clinic. <bookmark mark='d'/> The money could not reach every village at once, and "
            "the designers, led by the economist Santiago Levy, turned that into an experiment: "
            f"{T['treated']} of {T['localities']} localities, drawn at random, started in 1998, and the rest later. "
            "<bookmark mark='e'/> Paul Schultz used the comparison to measure the effect on schooling. Primary "
            "enrolment was already high and barely moved. The gains came after primary school, exactly where "
            "children had been dropping out, and he put the return on the grants, counted as extra schooling, at "
            "about eight percent a year. The design, conditional cash transfers with an evaluation built in, was "
            "copied across Latin America and beyond."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(chain.boxes[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(chain.notes[0]))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in res], lag_ratio=0.6), run_time=3.0)
        self.clear_scene()

    def givedirectly(self):
        T = tables.CASH_46.data
        ax = plane([0, 2], [0, 220], center=LEFT * 2.4 + DOWN * 0.4, x_length=4.6, y_length=4.6, xticks=[],
                   yticks=[0, 50, 100, 150, 200], ylabel=r"monthly consumption, \ \$ (PPP)", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        bars = VGroup()
        for i, (nm, v, col) in enumerate(((r"control", T["hs_before"], CONTROL), (r"transfer", T["hs_after"], CASH))):
            p0, p1 = ax.ax.c2p(0.5 + i - 0.3, 0), ax.ax.c2p(0.5 + i + 0.3, v)
            r = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                          fill_opacity=0.85).move_to((p0 + p1) / 2)
            bars.add(VGroup(r, label(nm, font_size=16, color=WHITE).next_to(r, DOWN, buff=0.1),
                            label(rf"\${v}", font_size=18, color=WHITE).next_to(r, UP, buff=0.06)))
        side = VGroup(
            label(r"GiveDirectly, \ rural Kenya: \\ no conditions", font_size=20, color=WHITE),
            label(rf"\${T['hs_small']} or \${T['hs_large']:,} \ (PPP), \\ by mobile money".replace(",", "{,}"),
                  font_size=20, color=CASH),
            label(rf"consumption up {100 * (T['hs_after'] / T['hs_before'] - 1):.0f}\%; \\ more assets, \ less stress",
                  font_size=20, color=GAIN),
            label(r"not more alcohol \\ or tobacco", font_size=20, color=GREY_A),
            label(r"three years on, \\ the gains in consumption \\ were no longer evident", font_size=20, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.33).to_edge(RIGHT, buff=0.5)
        tag = published_tag(tables.CASH_46.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Then came a simpler question: what if there are no conditions at all? <bookmark mark='a'/> The charity "
            "GiveDirectly sends money to poor households in rural Kenya by mobile phone. Johannes Haushofer and "
            "Jeremy Shapiro evaluated it with a randomized trial. <bookmark mark='b'/> Households received "
            f"{T['hs_small']} or {T['hs_large']:,} dollars at purchasing-power parity. <bookmark mark='c'/> About "
            f"nine months on, monthly consumption was {T['hs_after']} dollars, against {T['hs_before']} in the "
            "control group, and households owned more and reported less stress. <bookmark mark='d'/> They did not "
            "spend it on alcohol or tobacco, a common fear about handing out cash. <bookmark mark='e'/> But in a "
            "follow-up three years later, the gains in consumption were no longer evident. Cash helps; whether it "
            "lasts is a different question."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), FadeIn(bars[0][1]), FadeIn(bars[1][1]), run_time=1.0)
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][2]))
            for mk, r_ in zip("bcde", side[1:]):
                vo.wait_until(mk)
                anims = [FadeIn(r_)]
                if mk == "c":
                    anims += [GrowFromEdge(bars[1][0], DOWN), FadeIn(bars[1][2])]
                self.play(*anims)
        self.clear_scene()

    def multiplier(self):
        M = load("cash")
        T = tables.CASH_46.data
        n = 9
        rounds = M["rounds"][:n]
        stack = VGroup()
        y = -2.4
        for i, r in enumerate(rounds):
            h = r * 1.55
            rect = Rectangle(width=1.4, height=max(h, 0.02), stroke_color=BLACK, stroke_width=1.2,
                             fill_color=CASH if i == 0 else interpolate_color(ManimColor(CASH), ManimColor(TOWN),
                                                                                min(1, i / 5)),
                             fill_opacity=0.85).move_to(np.array([-4.2, y + h / 2, 0]))
            stack.add(rect)
            y += h
        labels = VGroup(
            label(r"the transfer: \ 1", font_size=17, color=CASH).next_to(stack[0], RIGHT, buff=0.2),
            label(rf"spent in the village: \ {M['local_share']:.2f} $\times$ {M['mpc']:.1f} = "
                  rf"{rounds[1]:.2f}", font_size=17, color=WHITE).next_to(stack[1], RIGHT, buff=0.2),
            label(rf"and again: \ {rounds[2]:.2f}", font_size=17, color=WHITE).next_to(stack[2], RIGHT, buff=0.2),
        )
        eq = MathTex(r"1 + a + a^2 + \cdots = \frac{1}{1-a}", font_size=40, color=THEORY)
        eq.move_to(RIGHT * 2.6 + UP * 1.6)
        el = label(rf"$a$ = {M['local_share']:.2f} $\times$ {M['mpc']:.1f} = {M['local_share'] * M['mpc']:.2f}: \ "
                   rf"multiplier {M['multiplier']:.1f}", font_size=20, color=THEORY).next_to(eq, DOWN, buff=0.25)
        real = label(rf"if {100 * (1 - M['real_rounds'][1] / M['rounds'][1]):.0f}\% of each round went into prices: "
                     rf"\ {M['real_multiplier']:.2f} in real terms", font_size=18, color=GREY_A).next_to(el, DOWN,
                                                                                                         buff=0.3)
        egger = VGroup(
            label(rf"Egger et al., \ 2022: \ about \$1,000 each \\ to over {T['egger_hh']:,} households \\ in "
                  rf"{T['egger_villages']} Kenyan villages".replace(",", "{,}"), font_size=18, color=WHITE),
            label(rf"multiplier about {T['egger_m']}; \ prices up \\ about {T['egger_inflation']}\%; \ neighbours "
                  r"gained", font_size=18, color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(real, DOWN, buff=0.45)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "A transfer does not stop at the household that receives it. <bookmark mark='a'/> On the Island, a "
            f"household spends it, and {100 * M['local_share']:.0f} percent of what it spends goes to sellers in "
            f"the same village, <bookmark mark='b'/> who spend {100 * M['mpc']:.0f} percent of what they earn: "
            f"{rounds[1]:.2f} of every dollar comes back as someone else's income. <bookmark mark='c'/> And again, "
            f"{rounds[2]:.2f}, and so on. <bookmark mark='d'/> This is Part twenty-seven's multiplier, at the scale "
            f"of a village: one over one minus {M['local_share'] * M['mpc']:.2f}, or {M['multiplier']:.1f}. "
            "<bookmark mark='e'/> If local sellers could not produce more, the extra demand would raise prices "
            f"instead; here a little of it does, and the real multiplier is {M['real_multiplier']:.2f}. <bookmark "
            "mark='f'/> Dennis Egger, Johannes Haushofer, Edward Miguel, Paul Niehaus and Michael Walker measured "
            f"it, by randomizing how many households in each area received GiveDirectly's transfers: over "
            f"{T['egger_hh']:,} households in {T['egger_villages']} villages, more than fifteen percent of local GDP. "
            f"The multiplier was about {T['egger_m']}, prices rose by about a tenth of a percent, and neighbours who "
            "received nothing gained too."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(stack[0]), FadeIn(labels[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(Indicate(stack[0], color=WHITE))
            vo.wait_until("b")
            self.play(FadeIn(stack[1], shift=DOWN * 0.2), FadeIn(labels[1]))
            vo.wait_until("c")
            self.play(FadeIn(stack[2], shift=DOWN * 0.2), FadeIn(labels[2]))
            self.play(LaggedStart(*[FadeIn(s_, shift=DOWN * 0.1) for s_ in stack[3:]], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("d")
            self.play(Write(eq), FadeIn(el))
            vo.wait_until("e")
            self.play(FadeIn(real))
            vo.wait_until("f")
            self.play(FadeIn(egger, shift=UP * 0.1))
        self.clear_scene()

    def panes(self):
        P = load("panes")
        S = P["support"]
        T = tables.CASH_46.data
        ax = plane([-0.02, 0.02], [0.5, 1.0], center=LEFT * 1.9 + DOWN * 0.35, x_length=8.0, y_length=4.8,
                   xticks=[-0.02, -0.01, 0, 0.01, 0.02], yticks=[0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                   xlabel=r"the eligibility score, \ centred on the cutoff \ (eligible on the left)",
                   ylabel=r"share who favour the government", xfmt=lambda v: f"{v:+.2f}".replace("-", "{-}"),
                   yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=13)
        pts = VGroup(*[dot(ax, x, y, CASH if x < 0 else CONTROL, 0.075) for x, y in zip(S["mids"], S["means"])])
        cut = vline(ax, 0, 0.5, 1.0, WHITE)
        # the local linear fits on the households themselves, one on each side
        fits = VGroup()
        for b, col, (x0, x1) in ((S["fit_in"], CASH, (-0.02, 0.0)), (S["fit_out"], CONTROL, (0.0, 0.02))):
            fits.add(seg(ax, x0, np.polyval(b, x0), x1, np.polyval(b, x1), col, 3.0))
        side = VGroup(
            label(rf"Uruguay's PANES: \ {P['n']:,} \\ households near \\ the cutoff".replace(",", "{,}"), font_size=18,
                  color=WHITE),
            label(r"left: \ eligible, \\ all took part", font_size=18, color=CASH),
            label(r"right: \ not eligible", font_size=18, color=CONTROL),
            label(rf"the jump: \ {100 * S['jump']:.0f} points \\ (s.e. {100 * S['se']:.0f})", font_size=19,
                  color=E.ACCENT),
            label(rf"Manacorda, \ Miguel and \\ Vigorito: \ {T['panes_lo']} to {T['panes_hi']} points", font_size=17,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Manacorda, \ Miguel and Vigorito (2011), \ via the R package causaldata 0.1.4", corner=DL,
                       font_size=12)
        with self.voiceover(
            "Cash also changes politics. Between 2005 and 2007 Uruguay paid a monthly transfer to households below "
            "a cutoff in a poverty score computed from a survey. <bookmark mark='a'/> Households just below and "
            "just above the cutoff are alike in every way except eligibility, which makes Part four's regression "
            f"discontinuity possible. Here are {P['n']:,} of them, from data Marco Manacorda, Edward Miguel and "
            "Andrea Vigorito collected, grouped by score. <bookmark mark='b'/> On the left, the eligible, all of "
            "whom took part. <bookmark mark='c'/> On the right, those just too well off. <bookmark mark='d'/> At "
            f"the cutoff, support for the government jumps by {100 * S['jump']:.0f} points, with a standard error "
            f"of {100 * S['se']:.0f}, computed here by local linear regression on each side. <bookmark mark='e'/> "
            f"The authors' own estimates were {T['panes_lo']} to {T['panes_hi']} points. People notice who helps "
            "them, which is one reason governments like cash transfers, and one reason to design them by rule."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(cut), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.05), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(fits[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(fits[1]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
