from __future__ import annotations

from videos.economics.econ48.common import *  # noqa: F403


class Hotelling(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Exhaustible resources", r"How should the price of something that runs out behave?",
             "Chapter one. Exhaustible resources.", lit={1931: r"Hotelling"}, scale=("firm", "world"),
             horizon=("a decade", "a century"))
        self.rule()
        self.mine()
        self.record()

    def rule(self):
        left = VGroup(label(r"sell a barrel today", font_size=24, color=METAL),
                      MathTex(r"(p_0 - c)\,(1 + r)", font_size=36, color=WHITE),
                      label(r"and invest the proceeds", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.2)
        right = VGroup(label(r"leave it in the ground", font_size=24, color=METAL),
                       MathTex(r"p_1 - c", font_size=36, color=WHITE),
                       label(r"and sell it next year", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.2)
        VGroup(left, right).arrange(RIGHT, buff=2.4).move_to(UP * 1.6)
        eq = MathTex(r"p_1 - c = (1 + r)(p_0 - c) \quad\Longrightarrow\quad \frac{p_{t+1} - c}{p_t - c} = 1 + r",
                     font_size=38, color=THEORY).move_to(DOWN * 0.4)
        notes = VGroup(
            label(r"the scarcity rent, \ price less extraction cost, \ rises at the rate of interest", font_size=22,
                  color=E.ACCENT),
            label(r"and the stock runs out just as the price reaches the level where nobody buys", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.25).next_to(eq, DOWN, buff=0.55)
        tag = published_tag(tables.HOTELLING_1931.tag, corner=DR, font_size=11)
        with self.voiceover(
            "In 1931 Harold Hotelling asked what the price of a resource that runs out should do. Think of the owner "
            "of an oil field. <bookmark mark='a'/> A barrel sold today earns its price less the cost of getting it "
            "out, and the money can be invested at the rate of interest. <bookmark mark='b'/> A barrel left in the "
            "ground can be sold next year instead. <bookmark mark='c'/> If owners are to be willing to hold oil in "
            "the ground and also to sell some now, the two must be worth the same: the price net of extraction "
            "cost, the scarcity rent, must rise at the rate of interest. <bookmark mark='d'/> That is Hotelling's "
            "rule. The oil in the ground is an asset, and it must pay like one. <bookmark mark='e'/> And in a "
            "competitive market the rent starts at just the level that makes the last barrel come out as the price "
            "reaches the point where nobody wants it any more."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(left[0]), FadeIn(right[0]))
            vo.wait_until("a")
            self.play(Write(left[1]), FadeIn(left[2]))
            vo.wait_until("b")
            self.play(Write(right[1]), FadeIn(right[2]))
            vo.wait_until("c")
            self.play(Write(eq), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(notes[0]))
            vo.wait_until("e")
            self.play(FadeIn(notes[1]))
        self.clear_scene()

    def mine(self):
        H = load("hotelling")
        A, B = H["constant"], H["falling"]
        n = max(A["exhausted"], B["exhausted"]) + 3
        ax = plane([0, n], [0, 11], center=LEFT * 2.0 + DOWN * 0.35, x_length=7.4, y_length=4.6,
                   xticks=[0, 10, 20, 30, 40, 50], yticks=[0, 2, 4, 6, 8, 10], xlabel=r"years from now",
                   ylabel=r"price of a ton", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        choke = DashedLine(ax.ax.c2p(0, 10), ax.ax.c2p(n, 10), color=GREY_B, stroke_width=1.4)
        ta, tb = np.arange(A["exhausted"] + 1), np.arange(B["exhausted"] + 1)
        pa = path(ax, ta, A["price"][:len(ta)], METAL, 3.2, smooth=False)
        ca = path(ax, ta, A["cost"][:len(ta)], GREY_B, 2.0, smooth=False)
        pb = path(ax, tb, B["price"][:len(tb)], COOL, 3.2, smooth=False)
        cb = path(ax, tb, B["cost"][:len(tb)], COOL, 1.8, smooth=False).set_stroke(opacity=0.5)
        side = VGroup(
            label(r"the Island's mine: \ 200 tons, \\ demand falls to zero \\ at a price of 10", font_size=18,
                  color=WHITE),
            label(rf"gold: \ cost 2 a ton; \\ the rent starts at {A['rent0']:.2f} \\ and grows 5\% a year; \\ the "
                  rf"mine is empty \\ in year {A['exhausted']}", font_size=18, color=METAL),
            label(rf"blue: \ cost starts at 6 \\ and falls 4\% a year: \\ the price falls for \\ "
                  rf"{H['falling_min_t']} years, \ then rises", font_size=18, color=COOL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Here is the rule at work on an Island mine with two hundred tons of ore, facing a demand that falls to "
            "nothing at a price of ten. <bookmark mark='a'/> With an extraction cost of two a ton, the rent starts "
            f"at {A['rent0']:.2f} and grows five percent a year; the price climbs, people buy less and less, and the "
            f"mine is empty in year {A['exhausted']}, just as the price reaches ten. <bookmark mark='b'/> Now let "
            "the cost of extraction start higher and fall four percent a year, as better machines and better "
            f"geology arrive. The rent still rises at the rate of interest, but for {H['falling_min_t']} years the "
            "falling cost wins, and the price falls before it rises: a U. <bookmark mark='c'/> In 1982 Margaret "
            "Slade argued that technical progress and ever poorer ores give exactly this U, and found it in the "
            "prices of major metals and fuels. The rule says the rent rises. It says nothing about the price, unless "
            "you know what happens to cost."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(choke), FadeIn(side[0]), run_time=1.0)
            self.play(Create(ca), Create(pa), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(side[1]), Indicate(pa, color=WHITE))
            vo.wait_until("b")
            self.play(Create(cb), Create(pb), FadeIn(side[2]), run_time=2.5)
            vo.wait_until("c")
            self.play(Indicate(pb, color=WHITE))
        self.clear_scene()

    def record(self):
        M = load("metals")
        yr = np.array(M["year"])
        ax = plane([1960, 2026], [-1.2, 2.4], center=LEFT * 1.8 + DOWN * 0.35, x_length=8.2, y_length=4.6,
                   xticks=[1960, 1980, 2000, 2020], yticks=[np.log10(x) for x in (0.1, 0.3, 1, 3, 10, 30, 100)],
                   ylabel=r"real price, \ 1960 = 1 \ (log scale)", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{10 ** v:g}", font_size=14)
        one = DashedLine(ax.ax.c2p(1960, 0), ax.ax.c2p(2026, 0), color=GREY_B, stroke_width=1.4)
        rent = path(ax, yr, np.log10(1.05 ** (yr - 1960)), HEAT, 2.4, smooth=False)
        lines = VGroup()
        for k, col in (("copper", COPPER), ("nickel", NICKEL), ("tin", TIN), ("oil", OIL)):
            lines.add(path(ax, yr, np.log10(np.array(M["index"][k]) / 100), col, 2.6, smooth=False))
        R = M["real_2024_vs_1960"]
        side = VGroup(
            label(r"red: \ a rent growing 5\% \\ a year since 1960", font_size=18, color=HEAT),
            label(rf"copper: \ {R['copper']:.2f} times", font_size=18, color=COPPER),
            label(rf"nickel: \ {R['nickel']:.2f}", font_size=18, color=NICKEL),
            label(rf"tin: \ {R['tin']:.2f}", font_size=18, color=TIN),
            label(rf"oil: \ {R['oil']:.1f}", font_size=18, color=OIL),
            label(r"costs fell, \ new deposits \\ were found, \ substitutes \\ arrived; \ the rent is a \\ small part "
                  r"of the price", font_size=17, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"World Bank, \ the Pink Sheet; \ US CPI (BLS via FRED)", corner=DL, font_size=12)
        with self.voiceover(
            "Does the record look like Hotelling? <bookmark mark='a'/> In red, a price that rises five percent a "
            f"year: since {M['year'][0]} it would have grown more than twentyfold. <bookmark mark='b'/> The real "
            f"prices of copper, nickel and tin in {M['year'][-1]} were within about a third of their "
            f"{M['year'][0]} levels: copper {R['copper']:.2f} times, nickel {R['nickel']:.2f}, tin "
            f"{R['tin']:.2f}. <bookmark mark='c'/> Oil, the one most bound up with politics and cartels, rose "
            f"{R['oil']:.1f} times, mostly in two jumps. <bookmark mark='d'/> Why not twentyfold? Because "
            "extraction costs fell, as in the blue path; because new deposits kept being found, so the stock was "
            "never fixed; because substitutes arrived, from aluminium for copper to plastic for tin; and because "
            "for most metals the scarcity rent is a small part of the price. What does rise, as Hotelling said, is "
            "the value of what is truly scarce."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(one), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(rent), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(*[Create(ln) for ln in lines[:3]], *[FadeIn(s_) for s_ in side[1:4]], run_time=3.0)
            vo.wait_until("c")
            self.play(Create(lines[3]), FadeIn(side[4]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(side[5]))
        self.clear_scene()
