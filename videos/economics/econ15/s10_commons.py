from __future__ import annotations

from videos.economics.econ15.common import *  # noqa: F403


class Commons(VoiceoverScene):
    def construct(self):
        card(self, 8, r"The commons: \ Gordon, \ Hardin and Ostrom", r"When nobody owns the fish, \ how many boats go "
             r"out, \ and who can stop them?", "Chapter eight. The commons: Gordon, Hardin and Ostrom.",
             lit={1954: r"Gordon's fishery", 1968: r"Hardin", 1990: r"Ostrom", 1992: r"the cod moratorium",
                  2009: r"the Nobel"}, scale=("community", "nation"), horizon=("a decade",))
        self.fishery()
        self.tragedy()
        self.ostrom()

    def fishery(self):
        f = load("fishery")
        es = np.array(f["effort"])
        ax = plane([0, 52], [0, 14.5], center=LEFT * 2.8 + DOWN * 0.3, x_length=6.4, y_length=4.6,
                   xticks=[0, 10, 20, 30, 40, 50], yticks=[0, 4, 8, 12], xlabel=r"boats fishing the lagoon",
                   ylabel=r"shells a season", font_size=16, xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}")
        a = ax.ax
        rev = path(ax, es, f["revenue"], color=FISH, width=3.5, xr=(0, 52), yr=(0, 14.5))
        cost = path(ax, es, f["cost"], color=SOCIAL, width=3, smooth=False, xr=(0, 52), yr=(0, 14.5))
        lr = label(r"the catch's value, \ season after season", font_size=15, color=FISH).next_to(
            a.c2p(25, f["p"] * f["y_msy"]), UP, buff=0.12)
        lc = label(r"the boats' cost", font_size=15, color=SOCIAL).next_to(a.c2p(47, f["c"] * 47), RIGHT, buff=0.12)
        e_oa, e_mey, e_msy = f["e_oa"], f["e_mey"], f["e_msy"]
        oa = Dot(a.c2p(e_oa, f["c"] * e_oa), radius=0.09, color=SOCIAL)
        mey = VGroup(seg(ax, e_mey, f["c"] * e_mey, e_mey, f["p"] * f["y_mey"], color=GOOD, width=4),
                     Dot(a.c2p(e_mey, f["p"] * f["y_mey"]), radius=0.08, color=GOOD))
        side = VGroup(
            label(r"more boats catch more, \ up to a point: \\ then they deplete the stock, \ and catch less",
                  font_size=20, color=FISH),
            label(rf"open access: \ boats come \\ until the catch just pays their cost: \ {e_oa:.0f} boats", font_size=20,
                  color=SOCIAL),
            label(r"the lagoon's rent, \ the gap between the curves, \\ is gone", font_size=20, color=SOCIAL),
            label(rf"the best: \ {e_mey:.1f} boats, \ a rent of {f['rent_mey']:.1f} shells, \\ and fish left: \ "
                  rf"{100 * f['stock_mey']:.0f}\% of the stock against {100 * f['stock_oa']:.0f}\%", font_size=20,
                  color=GOOD),
            label(rf"the most fish of all comes at {e_msy:.0f} boats: \\ not the best either", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Gordon, JPE 62(2) (1954); \ the curves: \ Agora (Schaefer's growth)", corner=DR,
                            font_size=13)
        with self.voiceover(
            "A common resource is rival but open to all. In 1954 Scott Gordon worked out what that does to a "
            "fishery. Take the island's lagoon. <bookmark mark='a'/> More boats catch more fish, up to a point; then "
            "they thin the stock faster than it breeds, and every boat catches less. The green curve is what the "
            "catch is worth, season after season, for each number of boats. <bookmark mark='b'/> Nobody owns the "
            "fish, so boats keep coming as long as a boat's share of the catch covers its cost: thirty-five boats. "
            "<bookmark mark='c'/> There, the gap between the two curves, the lagoon's rent, is gone. Each new boat "
            "takes fish from the others, and pays them nothing: a spillover. <bookmark mark='d'/> The best number is "
            "half that, seventeen and a half boats, with a rent of about six shells a season and sixty-five percent "
            "of the stock left in the water, against thirty. <bookmark mark='e'/> And the largest catch, at "
            "twenty-five boats, is not the best either: past seventeen and a half, the extra fish cost more to catch "
            "than they are worth."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(cost), FadeIn(lc))
            vo.wait_until("a")
            self.play(Create(rev), FadeIn(lr), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(oa, scale=1.5), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), Indicate(oa, color=SOCIAL))
            vo.wait_until("d")
            self.play(Create(mey), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def tragedy(self):
        rows = VGroup(
            label(r"Garrett Hardin, \ 1968: \ ``freedom in a commons brings ruin to all''", font_size=25, color=SOCIAL),
            label(r"Hardin's remedies: \ private property, \ or coercion by the state", font_size=24),
            label(r"the northern cod off Newfoundland: \ fished for five centuries", font_size=24, color=FISH),
            label(r"2 July 1992: \ the stock has collapsed; \ fishing is stopped", font_size=24, color=SOCIAL),
            label(r"about 30,000 people in Newfoundland and Labrador lose their work: \ the largest layoff in Canada's "
                  r"history", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        tag = published_tag(r"Hardin, Science 162 (1968); \ the cod moratorium (Fisheries and Oceans Canada, 1992)",
                            corner=DR, font_size=13)
        with self.voiceover(
            "In 1968 the biologist Garrett Hardin gave the problem a name. <bookmark mark='a'/> Freedom in a commons, "
            "Hardin wrote, brings ruin to all. <bookmark mark='b'/> Hardin's remedies were private property, or coercion by "
            "the state. <bookmark mark='c'/> The northern cod off Newfoundland had been fished for five centuries. "
            "<bookmark mark='d'/> On the second of July 1992, with the stock collapsed, Canada stopped the fishery. "
            "<bookmark mark='e'/> About thirty thousand people in Newfoundland and Labrador lost their work, the "
            "largest layoff in Canada's history, and the cod have not fully come back."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def ostrom(self):
        hc = history_card(1990, r"Elinor Ostrom, \ Governing the Commons", r"commons that people have managed, \ some "
                          r"for centuries, \ without owners or a state", color=GOOD, width=11.4, font_size=24
                          ).to_edge(UP, buff=0.4)
        rows = VGroup(
            label(r"Törbel, \ a Swiss village: \ an association to manage its alpine pastures since 1483", font_size=22),
            label(r"a rule: \ no one sends more cows up to the alp \ than they can feed through the winter",
                  font_size=22, color=GOOD),
            label(r"Ostrom's design principles: \ clear boundaries; \ rules fitted to the place; \ the users make them;",
                  font_size=21, color=DEMAND),
            label(r"monitoring by the users; \ graduated sanctions; \ cheap ways to settle disputes; \ rights the state "
                  r"respects", font_size=21, color=DEMAND),
            label(r"Hardin was right about open access, \ and wrong about the commons", font_size=25,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.32).next_to(hc, DOWN, buff=0.45)
        tag = published_tag(r"Ostrom, Governing the Commons (1990); \ the Nobel Foundation (2009)", corner=DR,
                            font_size=13)
        with self.voiceover(
            "Elinor Ostrom spent a career showing that Hardin's choice was too narrow. In the 1990 book Governing "
            "the Commons, Ostrom gathered pastures, forests, fisheries and irrigation systems that their users had "
            "managed well, some for centuries, without either an owner or a state. <bookmark mark='a'/> In Törbel, a "
            "village in the Swiss Alps, an association has managed the high pastures since 1483. "
            "<bookmark mark='b'/> One of its rules: no one may send more cows up to the summer pasture than they can "
            "feed through the winter. <bookmark mark='c'/> From cases like these Ostrom drew design principles. "
            "Clear boundaries, of the resource and of who may use it. Rules fitted to the place. Rules made by the "
            "people they bind. <bookmark mark='d'/> Monitoring by the users themselves; sanctions that start small "
            "and grow; cheap ways to settle disputes; and a state that respects the users' right to organize. "
            "<bookmark mark='e'/> Hardin was right about open access, and wrong about the commons. In 2009 Ostrom "
            "became the first woman to win the Nobel prize in economics."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
