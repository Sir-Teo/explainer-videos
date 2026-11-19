from __future__ import annotations

from videos.economics.econ11.common import *  # noqa: F403

RIGHTC = "#7BD88F"


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 15, r"In practice: \ bargaining, \ standards \ and arms control", r"Where is game theory used, "
             r"and what does it change?", "Chapter fifteen. In practice: bargaining, standards and arms control.",
             lit={1982: r"Rubinstein's bargaining"}, scale=("person", "firm", "nation", "world"),
             horizon=("a year", "a decade"))
        self.bargain()
        self.standards()
        self.arms()

    def bargain(self):
        b = load("bargain")
        ax = plane([0, 1], [0.45, 1.02], center=LEFT * 2.9 + DOWN * 0.3, x_length=6.0, y_length=4.6,
                   xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0.5, 0.75, 1], xlabel=r"patience $\delta$ \ (both)",
                   ylabel=r"the first proposer's share", font_size=16)
        a = ax.ax
        curve = path(ax, b["grid"], b["shares"], color=ANA, width=3.5)
        half = DashedLine(a.c2p(0, 0.5), a.c2p(1, 0.5), color=GREY_B, stroke_width=1.5)
        pt = Dot(a.c2p(b["delta"], b["share"]), radius=0.09, color=EQ)
        side = VGroup(
            label(r"two parties split a pie; \ they take turns proposing; \\ each round of delay shrinks it by "
                  r"$\delta$", font_size=21),
            MathTex(r"\text{share} = \frac{1}{1 + \delta}", font_size=36, color=EQ),
            label(rf"with $\delta = {b['delta']:.1f}$: \ {100 * b['share']:.1f}\% to whoever proposes first, \\ "
                  r"agreed at once", font_size=21, color=ANA),
            label(r"patience is power; \ as delay costs vanish, \\ the split tends to half: \ Nash's bargaining "
                  r"solution (1950)", font_size=21, color=GREY_A),
            label(r"used to think about wage talks, \ mergers, \ peace terms", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        tag = published_tag(r"Rubinstein, Econometrica 50(1) (1982); \ Nash, Econometrica 18(2) (1950)", corner=DR,
                            font_size=13)
        with self.voiceover(
            "Game theory earns its keep in a few big applications. The first is bargaining. "
            "<bookmark mark='a'/> In Ariel Rubinstein's model of 1982, two parties split a pie by taking turns to "
            "make offers, and each round of delay shrinks the pie by a factor delta. <bookmark mark='b'/> The only "
            "subgame-perfect outcome is an immediate agreement, giving the first proposer one over one plus delta. "
            "<bookmark mark='c'/> With delta of nought point nine, that is fifty-two point six percent, agreed at "
            "once. <bookmark mark='d'/> Patience is power: the more costly delay is for you, the less you get. As "
            "delay costs vanish, the split tends to a half, the answer of the bargaining solution Nash proposed in "
            "1950. <bookmark mark='e'/> Models like this frame wage negotiations, mergers and the terms of peace."
        ) as vo:
            self.play(FadeIn(ax), Create(half), Create(curve), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Write(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(pt), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def standards(self):
        hc = history_card(1967, r"Sweden, \ 3 September", r"the whole country switched from driving on the left to "
                          r"driving on the right, \ at five in the morning", color=RIGHTC, width=11.4,
                          font_size=24).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"a coordination game with two equilibria: \ everyone left, \ or everyone right", font_size=24),
            label(r"no driver gains by switching alone: \ the old equilibrium was stable", font_size=24,
                  color=GREY_A),
            label(r"only a coordinated move, \ by everyone at once, \ could change it", font_size=24, color=EQ),
            label(r"the same with plugs, \ rail gauges, \ file formats, \ currencies: \\ standards stick because "
                  r"each user's choice depends on everyone else's", font_size=23, color=LEVEL),
            label(r"networks and platforms: \ Part 44", font_size=24, color=E.ACCENT),
        ).arrange(DOWN, buff=0.36).next_to(hc, DOWN, buff=0.5)
        with self.voiceover(
            "The second is standards. <bookmark mark='a'/> Which side of the road to drive on is a coordination game "
            "with two equilibria. <bookmark mark='b'/> No single driver gains by switching, so whichever equilibrium "
            "a country is in, it stays. <bookmark mark='c'/> Sweden drove on the left until the third of September "
            "1967, when at five in the morning the whole country switched to the right, a move only possible because "
            "everyone made it at once. <bookmark mark='d'/> Plugs, railway gauges, file formats and currencies stick "
            "in the same way, because each user's best choice depends on what everyone else uses. "
            "<bookmark mark='e'/> Part forty-four takes that idea to networks and platforms."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def arms(self):
        f = load("film")
        years = np.array(f["years"])
        tot = np.array(f["us"]) + np.array(f["ussr"])
        k = int(np.argmax(tot))
        ax = plane([1944, 2027], [0, 70000], center=LEFT * 2.6 + DOWN * 0.3, x_length=6.6, y_length=4.6,
                   xticks=[1950, 1970, 1990, 2010], yticks=[0, 20000, 40000, 60000], ylabel=r"warheads, \ both "
                   r"together", font_size=16, xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v / 1000:.0f}k" if v else "0")
        curve = path(ax, years, tot, color=USSR, width=3.5, smooth=False)
        pk = Dot(ax.ax.c2p(years[k], tot[k]), radius=0.08, color=WHITE)
        pl = label(rf"{years[k]}: \ {tot[k]:,}".replace(",", "{,}"), font_size=17).next_to(pk, UP, buff=0.1)
        ld = Dot(ax.ax.c2p(years[-1], tot[-1]), radius=0.08, color=WHITE)
        ll = label(rf"{years[-1]}: \ {tot[-1]:,}".replace(",", "{,}"), font_size=17).next_to(ld, UP, buff=0.1)
        side = VGroup(
            label(r"an arms race is a repeated prisoner's dilemma: \\ each side builds, \ whatever the other does",
                  font_size=21),
            label(r"Schelling and Halperin (1961): \ arms control \\ as a deal between adversaries, \ kept by "
                  r"self-interest", font_size=21, color=GREY_A),
            label(r"what makes it hold: \ seeing what the other does \\ (satellites, \ inspections), \ and a future "
                  r"worth keeping", font_size=21, color=EQ),
            label(r"``trust, but verify'' \ (Reagan, \ signing the INF Treaty, \ 1987)", font_size=21, color=US),
            label(rf"the two stockpiles: \ {tot[k]:,} warheads in {years[k]}, \ {tot[-1]:,} in {years[-1]}".replace(
                ",", "{,}"), font_size=21, color=USSR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        tag = data_tag(r"Federation of American Scientists, \ via Our World in Data", corner=DR, font_size=13)
        with self.voiceover(
            "The third is arms control, and it returns to the intermission. <bookmark mark='a'/> An arms race is a "
            "prisoner's dilemma played every year: each side builds, whatever the other does, and both end up less "
            "safe and poorer. <bookmark mark='b'/> In 1961 Thomas Schelling and Morton Halperin argued that arms "
            "control is a bargain between adversaries, kept only because keeping it serves each side. "
            "<bookmark mark='c'/> What makes such a bargain hold is what makes cooperation hold in a repeated game: "
            "each side can see what the other does, by satellite and inspection, and both have a future worth "
            "protecting. <bookmark mark='d'/> Signing the treaty on intermediate-range missiles in 1987, Ronald Reagan "
            "quoted a Russian proverb: trust, but verify. <bookmark mark='e'/> Together the two stockpiles peaked at "
            "about sixty-three thousand warheads in 1986. The estimate for 2026 is about eight thousand."
        ) as vo:
            self.play(FadeIn(ax), Create(curve), FadeIn(tag), FadeIn(side[0]), run_time=2)
            for mk, r in zip("bcd", side[1:4]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(pk), FadeIn(pl), FadeIn(ld), FadeIn(ll), FadeIn(side[4]))
        self.clear_scene()
