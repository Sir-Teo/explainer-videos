from __future__ import annotations

from videos.economics.econ14.common import *  # noqa: F403


class Teams(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Teams and the free rider", r"When a team shares its output, \ why does each member work less, \ "
             r"and who should watch them?", "Chapter two. Teams and the free rider.",
             lit={1972: r"Alchian and Demsetz", 1982: r"Holmström's teams"}, scale=("person", "firm"),
             horizon=("a season",))
        self.shares()
        self.fixes()

    def shares(self):
        t = load("team")
        ns = np.array(t["ns"])
        eff = np.array(t["effort"])
        lost = np.array(t["lost"])
        ax = plane([0.5, 20.5], [0, 1.05], center=LEFT * 3.0 + DOWN * 0.3, x_length=6.0, y_length=4.6,
                   xticks=[1, 2, 5, 10, 18], yticks=[0, 0.25, 0.5, 0.75, 1], xlabel=r"households sharing the harvest",
                   ylabel=r"each one's effort \ (alone $= 1$)", font_size=16, xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.2f}")
        a = ax.ax
        dots = VGroup(*[Dot(a.c2p(n, e), radius=0.06, color=TEAM) for n, e in zip(ns, eff)])
        lc = path(ax, ns, 1 - lost, color=RISK, width=2.5, smooth=False)
        ll = label(r"surplus, \ as a share of the best", font_size=15, color=RISK).next_to(a.c2p(3, 1 - lost[2]), RIGHT,
                                                                                         buff=0.2)
        n18 = t["n18"]
        side = VGroup(
            label(r"each household's effort adds to the harvest; \\ the harvest is shared equally", font_size=21),
            label(r"so each keeps $1/n$ of what its effort adds, \\ and works until that matches the cost", font_size=21,
                  color=TEAM),
            label(rf"18 households: \ each works {n18['e_eq']:.3f} as hard \\ as it would alone", font_size=22,
                  color=E.ACCENT),
            label(rf"and the village loses {100 * n18['lost']:.0f}\% of what it could have", font_size=22, color=RISK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Holmström, Bell Journal 13(2) (1982); \ the numbers: \ Agora", corner=DR, font_size=13)
        with self.voiceover(
            "Start with Xiaogang's commune as a model. <bookmark mark='a'/> Each household's effort adds to the "
            "harvest, and the harvest is shared equally. <bookmark mark='b'/> So with n households, each keeps one "
            "nth of what its own effort adds, and works only until that sliver matches the cost of the extra effort. "
            "<bookmark mark='c'/> With eighteen households, each works one eighteenth as hard as it would on its own "
            "land. <bookmark mark='d'/> In Agora's version the village loses eighty-nine percent of the surplus it "
            "could have had. Real communes did better than that, because neighbours watch and shame each other, but "
            "the direction is the same."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in dots], lag_ratio=0.05), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[2]), Indicate(dots[17], scale_factor=2))
            vo.wait_until("d")
            self.play(Create(lc), FadeIn(ll), FadeIn(side[3]))
        self.clear_scene()

    def fixes(self):
        rows = VGroup(
            label(r"Armen Alchian and Harold Demsetz (1972): \ hire a monitor, \ and make the monitor the residual "
                  r"claimant", font_size=23),
            label(r"the one who keeps what is left \ has every reason to watch: \ the classical firm", font_size=23,
                  color=SIGNAL),
            label(r"Bengt Holmström (1982): \ with many members, \ someone outside the team must break the budget",
                  font_size=23, color=TEAM),
            label(r"pay everyone their full contribution if the target is met, \ nothing if not: \ only an outsider can "
                  r"afford the threat", font_size=23, color=GREY_A),
            label(r"or divide the team: \ give each household its own land \ (Xiaogang)", font_size=24,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.36).move_to(UP * 0.1)
        tag = published_tag(r"Alchian and Demsetz, AER 62(5) (1972); \ Holmström, Bell Journal 13(2) (1982)", corner=DR,
                            font_size=13)
        with self.voiceover(
            "What can be done? <bookmark mark='a'/> In 1972 Armen Alchian and Harold Demsetz proposed that a team hire "
            "a monitor, and make the monitor the residual claimant, the one who keeps whatever is left after paying "
            "everyone else. <bookmark mark='b'/> Then the monitor has every reason to watch, and that, they argued, "
            "is what a classical firm and its owner are. <bookmark mark='c'/> In 1982 Bengt Holmström showed that "
            "when effort can't be watched at all, a team needs someone outside it to break the budget. "
            "<bookmark mark='d'/> Promise every member their full contribution if the team hits its target, and "
            "nothing if it misses: no member can afford to shirk, but only an outsider can afford to make that "
            "threat, since the team alone can't throw its output away. <bookmark mark='e'/> Or divide the team: give "
            "each household its own land, which is what Xiaogang did."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
