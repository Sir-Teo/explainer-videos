from __future__ import annotations

from videos.economics.econ27.common import *  # noqa: F403


class Thrift(VoiceoverScene):
    def construct(self):
        card(self, 5, r"The paradox of thrift", r"If everyone saves more, \ does the economy save more?",
             "Chapter five. The paradox of thrift.", lit={1714: r"Mandeville", 1936: r"Keynes"},
             scale=("household", "nation"), horizon=("a year",))
        self.fixed()
        self.induced()
        self.meaning()

    def fixed(self):
        T = load("thrift")
        f = T["fixed"]
        ax = plane([0, 1600], [0, 600], center=LEFT * 2.2 + DOWN * 0.3, x_length=6.8, y_length=4.8,
                   xticks=[0, 400, 800, 1200, 1600], yticks=[0, 200, 400, 600], xlabel=r"income $Y$",
                   ylabel=r"saving and investment", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=15)
        inv = seg(ax, 0, T["I"], 1600, T["I"], color=INVEST, width=4)
        s0 = seg(ax, T["a"] / (1 - T["b"]), 0, 1600, -T["a"] + (1 - T["b"]) * 1600, color=SAVE, width=4)
        a1 = T["a"] - T["da"]
        s1 = seg(ax, a1 / (1 - T["b"]), 0, 1600, -a1 + (1 - T["b"]) * 1600, color=PRICE, width=4)
        d0 = dot(ax, f["Y0"], f["S0"], color=OUTPUT, r=0.09)
        d1 = dot(ax, f["Y1"], f["S1"], color=PRICE, r=0.09)
        side = VGroup(
            label(r"saving $S = Y - C$ rises with income", font_size=20, color=SAVE),
            label(rf"investment fixed at {T['I']:.0f}", font_size=20, color=INVEST),
            label(rf"equilibrium where $S = I$: \ $Y = {f['Y0']:.0f}$", font_size=21, color=OUTPUT),
            label(rf"everyone tries to save {T['da']:.0f} more", font_size=21, color=PRICE),
            label(rf"income falls to {f['Y1']:.0f}; \\ saving is still {f['S1']:.0f}", font_size=21, color=PRICE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).to_edge(RIGHT, buff=0.45)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Here is the co-op's lesson as arithmetic. Leave the government out, so that what households do not "
            "consume, they save. <bookmark mark='a'/> Saving rises with income, in violet. "
            f"<bookmark mark='b'/> Investment, firms' spending on machines and buildings, is fixed at {T['I']:.0f}. "
            "<bookmark mark='c'/> The economy settles where saving equals investment, because only then is "
            f"everything produced either consumed or invested: at an income of {f['Y0']:,.0f}. "
            f"<bookmark mark='d'/> Now every household decides to save {T['da']:.0f} more, at any income. "
            f"<bookmark mark='e'/> Income falls, to {f['Y1']:,.0f}, by two and a half times the extra thrift, and "
            f"total saving ends exactly where it began, at {f['S1']:.0f}. Each household tried to save more; "
            "together they saved nothing more, and are poorer."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.8)
            vo.wait_until("a")
            self.play(Create(s0), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(inv), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(GrowFromCenter(d0), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(s1), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(GrowFromCenter(d1), FadeIn(side[4]))
        self.clear_scene()

    def induced(self):
        T = load("thrift")
        g = T["induced"]
        rows = VGroup(
            label(rf"now let investment rise with income: \ $I = {T['I']:.0f} + {T['h']}\,Y$", font_size=25,
                  color=INVEST),
            label(r"firms build more when they sell more", font_size=23, color=GREY_A),
            label(rf"income: \ {g['Y0']:,.0f} $\to$ {g['Y1']:,.0f}", font_size=25, color=PRICE),
            label(rf"saving: \ {g['S0']:.0f} $\to$ {g['S1']:.0f}: \ an attempt to save more ends with less",
                  font_size=25, color=PRICE),
            label(r"the paradox of thrift: \ Mandeville's bees (1714), \ and Keynes's chapter 23", font_size=21,
                  color=GREY_B),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "It can be worse. <bookmark mark='a'/> Suppose investment is not fixed, but rises with income, "
            "because firms build more when they sell more. <bookmark mark='b'/> Then thrift that cuts spending also "
            f"cuts investment. <bookmark mark='c'/> Income falls from {g['Y0']:,.0f} to {g['Y1']:,.0f}, "
            f"<bookmark mark='d'/> and total saving falls too, from {g['S0']:.0f} to {g['S1']:.0f}. An attempt to "
            "save more ends with less saved. <bookmark mark='e'/> It is called the paradox of thrift. Bernard "
            "Mandeville's Fable of the Bees made a version of the point in 1714, and Keynes quoted it."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def meaning(self):
        rows = VGroup(
            label(r"what it does and does not say", font_size=28, color=E.ACCENT),
            label(r"it holds when output is set by demand: \ idle workers, \ idle machines", font_size=23,
                  color=OUTPUT),
            label(r"at full employment, \ saving pays for investment and raises future income \ (Part 20)",
                  font_size=23, color=INVEST),
            label(r"so thrift is a vice in a slump and a virtue in a boom: \ the same act, \ two economies",
                  font_size=23, color=GREY_A),
            label(r"2009: \ households, \ firms and governments all tried to save at once", font_size=23,
                  color=PRICE),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        with self.voiceover(
            "Be careful what this says. <bookmark mark='a'/> It holds when output is set by demand: when there are "
            "idle workers and idle machines, so that spending less means producing less. <bookmark mark='b'/> At "
            "full employment, the arithmetic changes. Saving frees resources for investment, and investment raises "
            "future income, which is the growth story of Part twenty. <bookmark mark='c'/> So thrift can be a vice "
            "in a slump and a virtue in a boom: the same act, in two different economies. "
            "<bookmark mark='d'/> After 2008, households paying down debts, firms hoarding cash and governments "
            "cutting deficits all tried to save at once, and the argument returned."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
