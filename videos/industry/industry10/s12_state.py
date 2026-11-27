from __future__ import annotations

from videos.industry.industry10.common import *  # noqa: F403


class State(VoiceoverScene):
    def construct(self):
        card(self, 10, "The state on the farm", "Why do governments pay farmers, and stop their exports?",
             "Chapter ten. The state on the farm.", lit=("dollar", "change"))
        self.payments()
        self.rice()

    def payments(self):
        I = R["income"]
        g = I["gov_real"]
        sh = I["gov_share"]
        ys = sorted(g)
        pa = viz.plot_axes([1932, 2027], [0, 62], x_length=11.0, y_length=4.4, xticks=[1935, 1955, 1975, 1995, 2015, 2026],
                           yticks=[10, 20, 30, 40, 50, 60], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:g}bn", size=14
                           ).move_to([0.1, -0.5, 0])
        bars = viz.year_bars(pa, ys, [g[y] for y in ys], STATE, width=0.09)
        top = sorted(g, key=g.get, reverse=True)[:2]
        notes = VGroup()
        for y, txt_ in ((1933, "the New Deal pays farmers to grow less"), (2000, "a farm crisis of low prices"),
                        (2020, "the trade war with China and the pandemic"), (2026, "2026, forecast")):
            p = pa.ax.c2p(y, g[y])
            notes.add(VGroup(Dot(p, radius=0.05, color=WHITE), VGroup(tx(txt_, 14, WHITE), tx(f"${g[y]:.0f}bn; {100 * sh[y]:.0f}% of "
                                                                                              "farm income", 12, GREY_A)
                                                                     ).arrange(DOWN, buff=0.02)))
        notes[0][1].next_to(notes[0][0], UP, buff=0.5).shift(RIGHT * 1.0)
        notes[1][1].next_to(notes[1][0], UP, buff=0.12).shift(LEFT * 1.6)
        notes[2][1].next_to(notes[2][0], LEFT, buff=0.15)
        notes[3][1].next_to(notes[3][0], UP, buff=0.12).shift(LEFT * 0.4)
        del top
        head = tx("US government payments to farms, in 2026 dollars", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("USDA ERS, Farm Income and Wealth Statistics (3 September 2026; 2026 forecast), deflated with ERS's "
                     "GDP deflator", size=13)
        with self.voiceover(
            "Every rich country pays its farmers, and the United States has done so since the Depression. "
            "<bookmark mark='a'/> In 1933 the New Deal began paying farmers to plant less, to lift prices that the "
            "treadmill and the slump had crushed. <bookmark mark='b'/> Since then, the payments have risen whenever "
            "prices fell. Around 2000, when crop prices were very low, government payments made up almost half of all "
            "farm income. <bookmark mark='c'/> The biggest year of all was 2020: payments to make up for China's "
            "retaliation against American soybeans in the trade war, and then pandemic relief, came to about "
            f"{g[2020]:.0f} billion of today's dollars, again close to half of farm income. <bookmark mark='d'/> And the "
            f"Department's forecast for 2026 is about {g[2026]:.0f} billion dollars, the second-largest on record. "
            "Why pay at all? Partly because farm income swings so violently, as you saw in the intermission. Partly "
            "because farmers, though few, are spread across many states, each with two senators. And partly because "
            "every government fears being unable to feed its people."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[:8]], lag_ratio=0.05), FadeIn(notes[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[8:68]], lag_ratio=0.02), run_time=3.0)
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[68:-1]], lag_ratio=0.05), run_time=2.0)
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(GrowFromEdge(bars[-1], DOWN), FadeIn(notes[3]))
        self.clear_scene()

    def rice(self):
        Rc = R["rice"]
        ms, pr = Rc["months"], Rc["price"]
        sel = [(m, v) for m, v in zip(ms, pr) if m >= "2021-01"]
        pa = viz.plot_axes([2021, 2027], [300, 700], x_length=7.4, y_length=4.2, xticks=[2021, 2022, 2023, 2024, 2025, 2026],
                           yticks=[400, 500, 600, 700], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:g}", size=14).move_to(
            [-1.6, -0.5, 0])
        ln = VMobject(stroke_color="#E8EAED", stroke_width=3).set_points_as_corners([pa.ax.c2p(mx(m), v) for m, v in sel])
        ban = DashedLine(pa.ax.c2p(2023.55, 300), pa.ax.c2p(2023.55, 690), stroke_color=STATE, stroke_width=2)
        bl = VGroup(tx("20 July 2023", 14, STATE, bold=True), tx("India bans exports of", 13, WHITE),
                    tx("ordinary white rice", 13, WHITE)).arrange(DOWN, buff=0.02).next_to(pa.ax.c2p(2023.55, 690), LEFT, buff=0.1)
        lift = DashedLine(pa.ax.c2p(2024.75, 300), pa.ax.c2p(2024.75, 690), stroke_color=FARM, stroke_width=2)
        ll = VGroup(tx("Sept-Oct 2024", 14, FARM, bold=True), tx("the ban is lifted", 13, WHITE)).arrange(DOWN, buff=0.02).next_to(
            pa.ax.c2p(2024.75, 690), RIGHT, buff=0.1)
        pk = Dot(pa.ax.c2p(mx(Rc["peak"]), Rc["peak_val"]), color=WHITE, radius=0.07)
        pkl = tx(f"{mlabel(Rc['peak'])}: ${Rc['peak_val']:.0f}", 15, WHITE, bold=True).next_to(pk, DOWN, buff=0.12)
        pt = tx("rice, dollars a tonne (world export price)", 16, GREY_A).next_to(pa, UP, buff=0.1)
        side = VGroup(tx("Other states, other tools:", 18, WHITE, bold=True),
                      tx("India sets minimum prices for its farmers", 15, GREY_A),
                      tx("and buys their grain for public stores;", 15, GREY_A),
                      tx("China keeps vast state grain reserves;", 15, GREY_A),
                      tx("the European Union pays its farmers", 15, GREY_A),
                      tx("through its Common Agricultural Policy.", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.07
                                                                                         ).move_to([4.6, -0.6, 0])
        src = source("IMF rice price via FRED; DGFT notifications as reported by ThePrint (23 October 2024)", size=13)
        with self.voiceover(
            "Governments also act on the other side: when food gets dear, they stop it leaving. "
            "<bookmark mark='a'/> India is the world's largest exporter of rice. On the twentieth of July 2023, to keep "
            "rice cheap and plentiful at home, it banned exports of ordinary white rice. "
            f"<bookmark mark='b'/> The world price jumped, from about {Rc['before']:.0f} dollars a tonne before the ban "
            f"to {Rc['peak_val']:.0f} in {mlabel(Rc['peak'])}, and importing countries in Africa and Asia paid more. "
            "<bookmark mark='c'/> In September and October 2024, with its own stores well stocked, India lifted the ban, and the "
            f"price fell back, to about {Rc['last']:.0f} dollars now. <bookmark mark='d'/> Every big farming country "
            "manages its food this way, with minimum prices, public stores, subsidies and trade rules. Food is the one "
            "market no government leaves alone."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(pt), FadeIn(src))
            self.play(Create(ln), run_time=3.0, rate_func=linear)
            vo.wait_until("a")
            self.play(Create(ban), FadeIn(bl))
            vo.wait_until("b")
            self.play(FadeIn(pk, scale=2), FadeIn(pkl))
            vo.wait_until("c")
            self.play(Create(lift), FadeIn(ll))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in side], lag_ratio=0.2), run_time=2.0)
        self.clear_scene()
