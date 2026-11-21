from __future__ import annotations

from videos.economics.econ47.common import *  # noqa: F403


class Collective(VoiceoverScene):
    def construct(self):
        card(self, 1, r"The logic of collective action", r"Why do small groups beat large ones?",
             "Chapter one. The logic of collective action.", lit={1965: r"Olson", 2023: r"GAO on sugar"},
             scale=("group", "nation"), horizon=("a year",))
        self.free_riding()
        self.sugar()
        self.stakes()

    def free_riding(self):
        O = load("olson")
        n = np.array(O["n"])
        ax = plane([0, 120], [0, 10], center=LEFT * 2.0 + DOWN * 0.35, x_length=7.2, y_length=4.6,
                   xticks=[1, 20, 40, 60, 80, 100, 120], yticks=[0, 2, 4, 6, 8, 10],
                   xlabel=r"members of the group", ylabel=r"the group's total lobbying effort",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        ln = path(ax, n, O["effort"], FEW, 3.2, smooth=False)
        eq = MathTex(r"E(n) = \sqrt{B K / n} - K", font_size=34, color=THEORY)
        zero_n = int(O["B"] / O["K"])
        side = VGroup(
            label(rf"a policy worth {O['B']:.0f} \\ to the whole group", font_size=19, color=WHITE),
            eq,
            label(r"each member weighs \\ only their own share, \\ $B/n$", font_size=19, color=GREY_A),
            label(rf"one member: \ {O['effort'][0]:.0f}; \\ ten: \ {O['effort'][9]:.1f}; \\ "
                  rf"{zero_n} or more: \ nothing", font_size=19, color=FEW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        marks = VGroup()
        for k, txt in ((0, rf"one member: \\ {O['effort'][0]:.0f}"), (9, rf"ten: \\ {O['effort'][9]:.1f}"),
                       (zero_n - 1, rf"{zero_n}: \\ nothing")):
            p = ax.ax.c2p(n[k], O["effort"][k])
            d = Dot(p, radius=0.07, color=WHITE)
            marks.add(VGroup(d, label(txt, font_size=15, color=WHITE).next_to(d, UR, buff=0.08)))
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "In 1965 Mancur Olson pointed out something odd about groups. A policy may be worth a great deal to a "
            "group as a whole, and yet the group may do nothing to get it. <bookmark mark='a'/> Here is a policy "
            f"worth {O['B']:.0f} to a group, which wins it with a probability that rises with how hard the group "
            "lobbies against fixed resistance. <bookmark mark='b'/> Each member decides how much to put in, and "
            "weighs only their own share of the gain, while bearing all of their own cost. Every member hopes the "
            f"others will do the work. <bookmark mark='c'/> A group of one puts in {O['effort'][0]:.0f}. A group of "
            f"ten, {O['effort'][9]:.1f} in total. <bookmark mark='d'/> A group of {zero_n} or more, nothing at all, "
            "though the policy is worth just as much to it. That is free riding, and it grows with the size of the "
            "group. Olson's conclusion: small groups with a lot at stake per head organize; large groups with a "
            "little at stake per head do not, unless something else, a membership benefit, a law, forces them to."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), Create(ln), run_time=3.0)
            vo.wait_until("b")
            self.play(Write(side[1]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(*[FadeIn(m) for m in marks[:2]])
            vo.wait_until("d")
            self.play(FadeIn(marks[2]), FadeIn(side[3]))
        self.clear_scene()

    def sugar(self):
        S = load("sugar")
        ax = plane([1958, 2028], [0, 1.0], center=LEFT * 1.7 + DOWN * 0.35, x_length=8.6, y_length=4.6,
                   xticks=[1960, 1970, 1980, 1990, 2000, 2010, 2020], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   ylabel=r"dollars per kilogram, \ yearly average", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.2f}", font_size=14)
        us = path(ax, S["year"], S["us"], FEW, 3.2, smooth=False)
        wd = path(ax, S["year"], S["world"], MANY, 3.0, smooth=False)
        side = VGroup(
            label(r"gold: \ the US price", font_size=19, color=FEW),
            label(r"blue: \ the world price", font_size=19, color=MANY),
            label(rf"the US price, \\ as a multiple of the world's: \\ median {S['median_ratio']:.1f}, \\ "
                  rf"{S['recent_ratio']:.1f} since 2015", font_size=19, color=WHITE),
            label(r"import quotas \\ and price supports", font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"World Bank, \ Commodity Price Data (the Pink Sheet): \ Sugar, US; \ Sugar, world", corner=DL,
                       font_size=12)
        with self.voiceover(
            "The classic example is sugar in the United States. <bookmark mark='a'/> Here is the price of sugar in "
            f"America, from the World Bank's monthly price data, {S['year'][0]} to {S['last_year']}. <bookmark "
            "mark='b'/> And the price of sugar on the world market. <bookmark mark='c'/> In most years the American "
            f"price is about twice the world's: a median of {S['median_ratio']:.1f} times, and "
            f"{S['recent_ratio']:.1f} times on average since 2015. <bookmark mark='d'/> The gap is made in "
            "Washington, by import quotas that keep foreign sugar out and loans that put a floor under the price. "
            "In 1974 and 1980, when world prices spiked, the two lines met; the rest of the time, Americans pay "
            "more."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(us), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(wd), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def stakes(self):
        S = load("sugar")
        T = tables.OLSON_1965.data
        C = S["contest"]
        left = VGroup(
            label(r"sugar farms", font_size=28, color=FEW),
            label(rf"about {T['farms']:,}".replace(",", "{,}"), font_size=34, color=WHITE),
            label(rf"gain \${T['producer_lo']}--{T['producer_hi']} billion a year", font_size=20, color=GREY_A),
            label(rf"about \${S['per_farm'] / 1000:,.0f},000 per farm".replace(",", "{,}"), font_size=24, color=FEW),
        ).arrange(DOWN, buff=0.25)
        right = VGroup(
            label(r"consumers", font_size=28, color=MANY),
            label(r"about 335 million", font_size=34, color=WHITE),
            label(rf"lose \${T['consumer_lo']}--{T['consumer_hi']} billion a year", font_size=20, color=GREY_A),
            label(rf"about \${S['per_person']:.0f} a head", font_size=24, color=MANY),
        ).arrange(DOWN, buff=0.25)
        VGroup(left, right).arrange(RIGHT, buff=2.6).move_to(UP * 0.7)
        vs = label(r"versus", font_size=24, color=GREY_B).move_to((left.get_center() + right.get_center()) / 2)
        foot = VGroup(
            label(rf"the economy as a whole loses about \${T['net']:.0f} billion a year", font_size=21, color=LOSS),
            label(rf"on the Island's contest: \ each side lobbies by its stake per head; \ the quota survives with "
                  rf"probability {C['p_pass']:.4f}", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.7)
        x0, y0, wbar = -5.6, -1.25, 9.0
        big = Rectangle(width=wbar, height=0.32, stroke_width=0, fill_color=FEW, fill_opacity=0.85)
        big.move_to([x0 + wbar / 2, y0, 0])
        tiny_w = max(wbar * S["per_person"] / S["per_farm"], 0.01)
        tiny = Rectangle(width=tiny_w, height=0.32, stroke_width=0, fill_color=MANY, fill_opacity=1.0)
        tiny.move_to([x0 + tiny_w / 2, y0 - 0.5, 0])
        bars = VGroup(big, label(r"at stake per farm", font_size=16, color=FEW).next_to(big, RIGHT, buff=0.15),
                      Dot([x0, y0 - 0.5, 0], radius=0.05, color=MANY),
                      label(r"at stake per consumer: \ too small to see on this scale", font_size=16,
                            color=MANY).next_to(tiny, RIGHT, buff=0.25))
        tag = published_tag(tables.OLSON_1965.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Who gains and who loses? <bookmark mark='a'/> About four thousand farms grow sugar beet and sugar "
            "cane in the United States. The Government Accountability Office reviewed the estimates in 2023: the "
            f"program is worth about {T['producer_lo']} to {T['producer_hi']} billion dollars a year to producers. "
            "Per farm, that is hundreds of thousands of dollars. <bookmark mark='b'/> Consumers lose about "
            f"{T['consumer_lo']} to {T['consumer_hi']} billion. Per American, about nine dollars a year. "
            f"<bookmark mark='c'/> So the country as a whole loses about {T['net']:.0f} billion dollars a year. But "
            "nobody writes to their senator about nine dollars, and every sugar farmer has a reason to. "
            "<bookmark mark='d'/> Put the two groups into the kind of contest chapter three builds, each lobbying by "
            "its "
            "stake per head, and the quota survives almost for certain, though it costs consumers more than it "
            "gives farmers. Olson called it the exploitation of the great by the small."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(left[0]), FadeIn(right[0]), FadeIn(vs))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in left[1:]], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in right[1:]], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(GrowFromEdge(bars[0], LEFT), FadeIn(bars[1]), FadeIn(bars[2]), FadeIn(bars[3]), run_time=2.0)
            self.play(FadeIn(foot[1]))
            self.play(Indicate(bars[2], color=WHITE, scale_factor=1.5))
        self.clear_scene()
