from __future__ import annotations

from videos.economics.econ42.common import *  # noqa: F403


class Pensions(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Pensions", r"Can pay-as-you-go pensions survive fewer workers per retiree?",
             "Chapter eight. Pensions.", lit={1958: r"Samuelson", 1983: r"the Social Security Amendments"},
             scale=("nation",), horizon=("a decade", "a century"))
        self.identity()
        self.returns()
        self.reforms()

    def identity(self):
        P = load("pensions")
        rows = [(r"1960", P["r1960"], P["rows"][str(P["r1960"])]["replacement"], GAIN),
                (r"2024", P["r2024"], P["rows"][str(P["r2024"])]["replacement"], PENSION),
                (r"2035 \ (projected)", P["r2035"], P["rows"][str(P["r2035"])]["replacement"], LOSS)]
        grp = VGroup()
        for k, (yr, ratio, rep, col) in enumerate(rows):
            y = 1.2 - 1.3 * k
            people = VGroup(*[Dot(radius=0.09, color=col) for _ in range(int(round(ratio * 2)))]).arrange(
                RIGHT, buff=0.08)
            people.move_to(np.array([-2.6, y, 0]), aligned_edge=LEFT)
            bar = Rectangle(width=rep * 5, height=0.45, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                np.array([2.3 + rep * 2.5, y, 0]))
            grp.add(VGroup(label(yr, font_size=22, color=WHITE).move_to(np.array([-4.6, y, 0])),
                           label(rf"{ratio:g} workers \ per beneficiary", font_size=17, color=col).next_to(
                               people, DOWN, buff=0.12, aligned_edge=LEFT), people,
                           bar, label(rf"{100 * rep:.0f}\%", font_size=22, color=col).next_to(bar, RIGHT, buff=0.12)))
        eq = MathTex(r"\frac{\text{benefit}}{\text{wage}} \;=\; \text{contribution rate} \times "
                     r"\frac{\text{workers}}{\text{retirees}}", font_size=34).to_edge(UP, buff=0.35)
        colh = VGroup(label(r"each dot: \ half a worker", font_size=16, color=GREY_B).move_to(
            np.array([-1.6, 2.15, 0])),
                      label(r"benefit the 12.4\% tax \\ could pay, \ share of the wage", font_size=16,
                            color=GREY_B).move_to(np.array([3.6, 2.15, 0])))
        tag = published_tag(tables.PENSIONS.tag + r"; \ computed", corner=DR, font_size=11)
        with self.voiceover(
            "Most public pensions are pay-as-you-go: today's workers pay for today's retirees. Part twenty-two "
            "showed, after Paul Samuelson, why that can be a good deal. Its arithmetic is simple. "
            "<bookmark mark='a'/> If the pension is paid only from contributions, the benefit as a share of the "
            "wage equals the contribution rate times the number of workers per retiree. America's Social Security "
            "is financed by a payroll tax of 12.4 percent, shared by employer and employee. "
            f"<bookmark mark='b'/> In 1960 there were {P['r1960']:g} covered workers per beneficiary: that tax "
            f"could pay each beneficiary {say_pct(P['rows'][str(P['r1960'])]['replacement'], 0)} of the average "
            f"wage. <bookmark mark='c'/> Today there are {P['r2024']:g}, enough for "
            f"{say_pct(P['rows'][str(P['r2024'])]['replacement'], 0)}. <bookmark mark='d'/> By 2035 the trustees "
            f"project {P['r2035']:g}, enough for {say_pct(P['rows'][str(P['r2035'])]['replacement'], 0)}. The "
            "trust fund, built up from past surpluses, fills the gap for now; the trustees expect it to run out in "
            f"{P['depletion']}."
        ) as vo:
            self.play(Write(eq), FadeIn(tag), FadeIn(colh), run_time=1.5)
            self.play(*[FadeIn(g[0]) for g in grp], *[FadeIn(g[1]) for g in grp],
                      *[LaggedStart(*[FadeIn(d) for d in g[2]], lag_ratio=0.1) for g in grp], run_time=2.0)
            for mk, g in zip("bcd", grp):
                vo.wait_until(mk)
                self.play(Indicate(g[2], color=WHITE, scale_factor=1.05), GrowFromEdge(g[3], LEFT), FadeIn(g[4]),
                          run_time=1.5)
        self.clear_scene()

    def returns(self):
        P = load("pensions")
        b = P["base"]
        rows = VGroup(
            label(rf"pay-as-you-go returns the growth of the wage bill: \ about {100 * b['annual_paygo']:.1f}\% a "
                  rf"year \ (Island)", font_size=21, color=PENSION),
            label(rf"a funded account earns $r$: \ {100 * b['annual_funded']:.0f}\% a year", font_size=21,
                  color=GAIN),
            label(rf"over a 30-year career, \ \$1 contributed becomes \${b['paygo_return']:.2f} against "
                  rf"\${b['funded_return']:.2f}: \ {100 * b['loss_share']:.0f}\% less", font_size=21, color=WHITE),
            label(r"why not switch? \ the first retirees were paid without contributing; \ that promise is a debt",
                  font_size=21, color=LOSS),
            label(rf"the interest on that debt is exactly the gap: \ {100 * b['interest_on_debt']:.0f}\% of each "
                  r"contribution", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(UP * 0.1)
        head = label(r"the return on a pay-as-you-go pension", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "What return does a pay-as-you-go pension pay? <bookmark mark='a'/> The growth of the total wage bill: "
            f"on the Island, with workers growing by half a percent a year and wages by one, about "
            f"{say_pct(b['annual_paygo'], 1)}. <bookmark mark='b'/> A funded account, invested, earns the return "
            "on capital, here three percent. <bookmark mark='c'/> Over a thirty-year career a dollar paid in "
            f"becomes {money_words(b['paygo_return'])} in pay-as-you-go, against {money_words(b['funded_return'])} "
            f"in a fund: {say_pct(b['loss_share'], 0)} less. <bookmark mark='d'/> So why not switch? Because the "
            "first generation of retirees was paid without having contributed, and every later generation was "
            "promised the same. That promise is a debt, owed to today's retirees and workers. "
            "<bookmark mark='e'/> Paying it off, or paying interest on it, costs exactly the gap in returns. A switch "
            "to funding moves the cost between generations; it does not make it disappear."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0]))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def reforms(self):
        cards = point_cards([
            (r"work longer", r"a later retirement \\ age adds workers \\ and removes \\ retirees", PENSION),
            (r"notional accounts", r"Sweden, \ late 1990s: \\ benefits follow your \\ contributions and \\ life "
                                   r"expectancy", GAIN),
            (r"pre-fund", r"build a reserve now, \\ so later workers \\ pay less", UNEMP),
            (r"the 1983 fix", r"Called it? \\ in chapter 15", HOLD),
        ], width=12.8, cols=4, font_size=19).move_to(DOWN * 0.1)
        head = label(r"what reforms can do", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.PENSIONS.tag, corner=DR, font_size=11)
        with self.voiceover(
            "What can reform do? <bookmark mark='a'/> A later retirement age adds workers and removes retirees, "
            "attacking both sides of the ratio. <bookmark mark='b'/> Sweden's reform of the late 1990s kept "
            "pay-as-you-go financing but gave each worker a notional account: benefits follow what you paid in, and "
            "adjust to how long your generation is expected to live, so longer lives do not break the budget. "
            "<bookmark mark='c'/> Building a reserve now, partly pre-funding, lets later workers pay less. "
            "<bookmark mark='d'/> America chose a mix of these in 1983, with a promise that chapter fifteen checks."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
