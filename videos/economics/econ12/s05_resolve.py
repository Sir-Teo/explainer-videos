from __future__ import annotations

from videos.economics.econ12.common import *  # noqa: F403


class Resolve(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Resolving the paradox: \ capacity, \ difference, \ repetition", r"Bertrand assumed firms "
             r"can serve everyone, \ sell the same thing, \ and meet once. \ What if they can't, \ don't, \ and don't?",
             "Chapter four. Resolving the paradox: capacity, difference, repetition.",
             lit={1983: r"Kreps and Scheinkman"}, scale=("firm", "market"), horizon=("a season", "a year"))
        self.capacity()
        self.kreps()
        self.difference()
        self.repetition()

    def capacity(self):
        rows = VGroup(
            label(r"Bertrand's undercutter takes every buyer: \ but only if the yard can serve them all", font_size=24),
            label(r"Francis Edgeworth (1897): \ with limited capacity, \ a price cut wins only the customers you "
                  r"can serve", font_size=24, color=LEADER),
            label(r"then raising your price can pay: \ the rival's customers it can't serve come to you anyway",
                  font_size=24, color=GREY_A),
            label(r"so prices may never settle: \ cut, \ cut, \ cut, \ then a jump back up", font_size=24,
                  color=CARTEL),
            label(r"some cities' petrol prices do this, \ week after week: \ Edgeworth cycles \ (Maskin and Tirole, "
                  r"1988)", font_size=23, color=PUMP),
        ).arrange(DOWN, buff=0.34).move_to(UP * 0.2)
        head = label(r"the first escape: \ capacity", font_size=34, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Edgeworth, Giornale degli Economisti (1897); \ Maskin and Tirole, Econometrica 56(3) "
                            r"(1988)", corner=DR, font_size=13)
        with self.voiceover(
            "Bertrand's argument has three quiet assumptions, and each can fail. <bookmark mark='a'/> The first is "
            "that the firm that undercuts can serve every buyer. A boatyard has only so many slips. "
            "<bookmark mark='b'/> In 1897 the English economist Francis Edgeworth pointed out that with limited "
            "capacity, a price cut wins only the customers you can serve. <bookmark mark='c'/> And raising your "
            "price can pay, because the customers your rival cannot serve come to you anyway. "
            "<bookmark mark='d'/> Then prices may never settle: cut after cut, then a jump back up, and again. "
            "<bookmark mark='e'/> The petrol prices of some cities in Canada and Australia move in just such a saw "
            "tooth, week after week, and economists call them Edgeworth cycles, after a dynamic model by Eric "
            "Maskin and Jean Tirole."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2), FadeIn(tag))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def kreps(self):
        r = load("resolve")
        b = load("boats")
        ax = plane([0, 100], [0, 100], center=LEFT * 3.0 + DOWN * 0.3, x_length=5.6, y_length=5.0,
                   xticks=[0, 30, 60, 90], yticks=[0, 10, 40, 55, 100], xlabel=r"repairs a season",
                   ylabel=r"price, \ \$", font_size=16, xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}")
        a = ax.ax
        dem = seg(ax, 0, 100, 100, 0, color=WHITE, width=3)
        dl = label(r"demand", font_size=16).next_to(a.c2p(80, 20), UR, buff=0.05)
        k = r["k"]
        c1 = Polygon(a.c2p(0, 0), a.c2p(k, 0), a.c2p(k, r["P"]), a.c2p(0, r["P"]), stroke_width=0,
                     fill_color=CRUSOE, fill_opacity=0.55)
        c2 = Polygon(a.c2p(k, 0), a.c2p(2 * k, 0), a.c2p(2 * k, r["P"]), a.c2p(k, r["P"]), stroke_width=0,
                     fill_color=DARA, fill_opacity=0.55)
        pl = DashedLine(a.c2p(0, r["P"]), a.c2p(2 * k, r["P"]), color=EQ, stroke_width=2)
        side = VGroup(
            label(r"David Kreps and Jose Scheinkman (1983): \\ first each yard builds its slips, \\ then they "
                  r"compete in prices", font_size=21),
            label(rf"in the subgame-perfect equilibrium: \\ {k:.0f} slips each, \ and a price of \${r['P']:.0f}",
                  font_size=22, color=EQ),
            label(r"undercutting wins nothing: \ both are full; \\ raising the price loses more than it gains \\ "
                  r"(Agora checks every higher price)", font_size=21, color=GREY_A),
            label(r"Bertrand pricing on top of Cournot capacities \\ gives Cournot's outcome", font_size=22,
                  color=LEADER),
            label(r"Cournot fits industries that commit to capacity: \\ cement, \ steel, \ airlines' fleets",
                  font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Kreps and Scheinkman, Bell Journal 14(2) (1983); \ the check: \ Agora", corner=DR,
                            font_size=13)
        with self.voiceover(
            "Capacity also explains when Cournot is right. <bookmark mark='a'/> In 1983 David Kreps and Jose "
            "Scheinkman studied a two-stage game: first each firm builds capacity, then the two compete in prices. "
            "<bookmark mark='b'/> On the Island, each yard builds thirty slips, and the price settles at forty "
            "dollars. <bookmark mark='c'/> Undercutting wins nothing, because both yards are already full, and "
            "raising the price loses more customers than it gains in margin; Agora checks every higher price. "
            "<bookmark mark='d'/> So Bertrand's price competition, played on top of capacities chosen in advance, "
            "gives exactly Cournot's outcome. <bookmark mark='e'/> That is why economists model industries that "
            "commit to capacity, like cement, steel or an airline's fleet, with Cournot's quantities."
        ) as vo:
            self.play(FadeIn(ax), Create(dem), FadeIn(dl), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(c1), FadeIn(c2), Create(pl), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        del b
        self.clear_scene()

    def difference(self):
        r = load("resolve")
        d = r["diff"]
        pj = np.array(r["pj"])
        br = np.array(r["br"])
        ax = plane([0, 75], [0, 75], center=LEFT * 3.1 + DOWN * 0.3, x_length=5.2, y_length=5.2,
                   xticks=[0, 25, 50, 75], yticks=[0, 25, 50, 75], xlabel=r"Dara's price, \ \$",
                   ylabel=r"Crusoe's price, \ \$", font_size=16, xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}")
        a = ax.ax
        rc = path(ax, pj, br, color=CRUSOE, width=3.5, smooth=False, xr=(0, 75), yr=(0, 75))
        rd = path(ax, br, pj, color=DARA, width=3.5, smooth=False, xr=(0, 75), yr=(0, 75))
        rcl = label(r"Crusoe's best price", font_size=15, color=CRUSOE).next_to(a.c2p(58, 42), UP, buff=0.2)
        rdl = label(r"Dara's best price", font_size=15, color=DARA).next_to(a.c2p(45.5, 70), RIGHT, buff=0.15)
        eq = Dot(a.c2p(r["diff_p"], r["diff_p"]), radius=0.1, color=EQ)
        joint = Dot(a.c2p(r["joint_p"], r["joint_p"]), radius=0.1, color=CARTEL)
        jl = label(r"joint best", font_size=15, color=CARTEL).next_to(joint, UR, buff=0.05)
        side = VGroup(
            label(r"Crusoe's boats are fast, \ Dara's are sturdy: \\ a cheaper rival takes some buyers, \ not all",
                  font_size=21),
            MathTex(r"q_C = 90 - 2 p_C + p_D", font_size=34, color=CRUSOE),
            label(r"best replies slope up: \ if Dara raises her price, \\ so does Crusoe \ (strategic "
                  r"complements)", font_size=21, color=GREY_A),
            label(rf"equilibrium: \ \${r['diff_p']:.2f} each, \\ \${r['diff_profit']:,.0f} profit each".replace(
                ",", "{,}"), font_size=22, color=EQ),
            label(rf"above cost, \ below the joint best of \${r['joint_p']:.0f}: \\ difference softens price "
                  r"competition", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "The second assumption is that the two firms sell exactly the same thing. <bookmark mark='a'/> Suppose "
            "Crusoe's boats are fast and Dara's are sturdy, so a cheaper rival takes some of your buyers, but not "
            "all. <bookmark mark='b'/> Crusoe now sells ninety minus twice his price, plus Dara's price, and Dara "
            "the mirror image; each costs ten dollars to build. <bookmark mark='c'/> Best replies in prices slope "
            "upward: if Dara raises her price, Crusoe's best price rises too. Economists call such choices strategic "
            "complements; Cournot's quantities, whose reply curves slope down, are strategic substitutes. "
            "<bookmark mark='d'/> The curves cross at thirty-six dollars and sixty-seven cents each, with about "
            "fourteen hundred and twenty-two dollars of profit for each yard. <bookmark mark='e'/> That is well "
            "above cost, though below the fifty dollars that would maximize their joint profit. Being different "
            "softens price competition, which is one reason firms work so hard to be different."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Write(side[1]))
            vo.wait_until("c")
            self.play(Create(rc), Create(rd), FadeIn(rcl), FadeIn(rdl), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(eq, scale=1.5), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(joint), FadeIn(jl), FadeIn(side[4]))
        del d
        self.clear_scene()

    def repetition(self):
        rows = VGroup(
            label(r"the third assumption: \ the yards meet once", font_size=26),
            label(r"but they post prices every season, \ for years", font_size=25, color=GREY_A),
            label(r"Part 11: \ in a repeated game, \ a cut today can be punished tomorrow", font_size=25,
                  color=LEADER),
            label(r"so the high price can be an equilibrium \ without any agreement: \ chapter 8", font_size=25,
                  color=CARTEL),
            label(r"capacity, \ difference and repetition: \ why most markets with few firms \ price above cost",
                  font_size=25, color=E.ACCENT),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        with self.voiceover(
            "The third assumption is that the yards meet only once. <bookmark mark='a'/> In fact they post prices "
            "every season, for years. <bookmark mark='b'/> And Part eleven showed that in a repeated game, a cut "
            "today can be punished tomorrow. <bookmark mark='c'/> So a high price can be an equilibrium, without "
            "any agreement at all, as chapter eight will show. <bookmark mark='d'/> Capacity, difference and "
            "repetition: between them, they explain why most markets with only a few sellers price above cost."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
