from __future__ import annotations

from videos.economics.econ15.common import *  # noqa: F403


class Wedge(VoiceoverScene):
    def construct(self):
        card(self, 2, r"The wedge between private and social cost", r"When Bo's kiln smokes out Ana's fish, \ how many "
             r"pots does the market make, \ and how many should it?", "Chapter two. The wedge between private and "
             "social cost.", lit={1920: r"Pigou's Economics of Welfare", 1952: r"Meade"},
             scale=("person", "market"), horizon=("a year",))
        self.story()
        self.curves()
        self.signs()

    def story(self):
        rows = VGroup(
            label(r"Bo builds a kiln and fires pots for the island's market", font_size=25, color=BO),
            label(r"downwind, \ Ana dries her fish on racks: \ the smoke spoils some of them", font_size=25,
                  color=ANA),
            label(r"each pot Bo fires costs him clay, \ wood and time: \ his private cost", font_size=24,
                  color=PRIVATE),
            label(r"and it costs Ana some fish: \ a cost Bo never sees on his accounts", font_size=24, color=SMOKE),
            label(r"the social cost of a pot is the two together", font_size=27, color=SOCIAL),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.4)
        who = pair(height=0.8).to_edge(DOWN, buff=0.5)
        tag = island_tag(r"the Island", corner=DR, font_size=13)
        with self.voiceover(
            "Back on the island, Bo has built a kiln. <bookmark mark='a'/> He fires pots and sells them at the "
            "market. <bookmark mark='b'/> Downwind, Ana dries her fish on racks, and the smoke spoils some of them. "
            "<bookmark mark='c'/> Each pot costs Bo clay, firewood and his time: that is his private cost, and he "
            "weighs it against the price. <bookmark mark='d'/> It also costs Ana some fish, and that cost appears "
            "nowhere on Bo's accounts. <bookmark mark='e'/> The social cost of a pot is the two together: the cost to "
            "everyone of making it."
        ) as vo:
            self.play(FadeIn(who), FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def curves(self):
        k = load("kiln")
        qs = np.array(k["qs"])
        ax = plane([0, 70], [0, 110], center=LEFT * 2.7 + DOWN * 0.3, x_length=6.6, y_length=4.8,
                   xticks=[0, 20, 36, 45, 60], yticks=[0, 25, 50, 75, 100], xlabel=r"pots a season",
                   ylabel=r"shells a pot", font_size=16, xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}")
        a = ax.ax
        dem = path(ax, qs, k["demand"], color=DEMAND, width=3.5, smooth=False, yr=(0, 110))
        pri = path(ax, qs, k["private"], color=PRIVATE, width=3.5, smooth=False, yr=(0, 110))
        soc = path(ax, qs, k["social"], color=SOCIAL, width=3.5, smooth=False, yr=(0, 110))
        ld = label(r"demand", font_size=15, color=DEMAND).next_to(a.c2p(8, 92), UR, buff=0.05)
        lp = label(r"Bo's cost", font_size=15, color=PRIVATE).next_to(a.c2p(68, k["c"] + k["e"] * 68), DOWN,
                                                                      buff=0.15, aligned_edge=RIGHT)
        ls = label(r"Bo's cost + Ana's fish", font_size=15, color=SOCIAL).next_to(
            a.c2p(56, k["c"] + (k["e"] + k["d"]) * 56), LEFT, buff=0.15)
        qm, qs_ = k["q_market"], k["q_social"]
        pm = Dot(a.c2p(qm, k["p_market"]), radius=0.08, color=PRIVATE)
        ps = Dot(a.c2p(qs_, k["p_social"]), radius=0.08, color=SOCIAL)
        tri = Polygon(a.c2p(qs_, k["p_social"]), a.c2p(qm, k["c"] + (k["e"] + k["d"]) * qm), a.c2p(qm, k["p_market"]),
                      stroke_width=0, fill_color=SOCIAL, fill_opacity=0.35)
        gap = VGroup(seg(ax, qs_, 0, qs_, k["p_social"], color=SOCIAL, width=1.5, dashed=True),
                     seg(ax, qm, 0, qm, k["p_market"], color=PRIVATE, width=1.5, dashed=True))
        side = VGroup(
            label(rf"Bo fires pots until the price \\ meets his own cost: \ {qm:.0f} a season", font_size=21,
                  color=PRIVATE),
            label(rf"counting Ana's fish, \\ the best number is {qs_:.0f}", font_size=21, color=SOCIAL),
            label(r"the last pots are worth less to buyers \\ than they cost the island", font_size=21),
            label(rf"the loss: \ the red triangle, \\ {k['dwl']:.0f} shells a season", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Draw it. Demand for pots slopes down; Bo's own cost of each extra pot rises. <bookmark mark='a'/> Bo "
            "fires pots until the price just covers his own cost of one more: forty-five pots a season. That is "
            "part two's market, and it maximizes the surplus of everyone in it. <bookmark mark='b'/> But add Ana's "
            "spoiled fish to Bo's cost, and the cost of each pot to the whole island is higher, and rising faster. "
            "Counting her fish, the best number of pots is thirty-six. <bookmark mark='c'/> The last nine pots are "
            "worth less to the people who buy them than they cost the island to make. <bookmark mark='d'/> The loss "
            "is the red triangle, about a hundred shells a season. The first welfare theorem of part nine has failed, "
            "and it failed for a precise reason: a cost with no market, so no price to carry it."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(dem), Create(pri), FadeIn(ld), FadeIn(lp), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(pm, scale=1.5), Create(gap[1]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(soc), FadeIn(ls), FadeIn(ps, scale=1.5), Create(gap[0]), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(tri), FadeIn(side[3]))
        self.clear_scene()

    def signs(self):
        rows = VGroup(
            label(r"a negative spillover: \ too much of it \ (smoke, \ noise, \ traffic, \ carbon)", font_size=24,
                  color=SOCIAL),
            label(r"a positive spillover: \ too little of it \ (vaccination, \ research, \ a tidy garden, \ the bees)",
                  font_size=24, color=GOOD),
            label(r"the market isn't wrong about the costs it sees: \ it can't see the others", font_size=24,
                  color=GREY_A),
            label(r"three remedies: \ a price on the spillover, \ a bargain over it, \ or a rule", font_size=26,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        with self.voiceover(
            "The kiln is a negative spillover. <bookmark mark='a'/> When a choice imposes costs on others, the market "
            "makes too much of it: smoke, noise, traffic, carbon. <bookmark mark='b'/> When a choice benefits "
            "others, it makes too little: vaccinations, research, a tidy front garden, the bees. "
            "<bookmark mark='c'/> In both cases the market weighs correctly every cost and benefit it can see. It "
            "simply can't see the ones that fall outside it. <bookmark mark='d'/> There are three kinds of remedy, "
            "and the next chapters take them in turn: put a price on the spillover, let the people involved bargain "
            "over it, or write a rule."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
