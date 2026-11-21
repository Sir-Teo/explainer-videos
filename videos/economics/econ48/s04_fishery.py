from __future__ import annotations

from videos.economics.econ48.common import *  # noqa: F403


class Fishery(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Renewable resources: \ the fishery", r"Why is a resource that renews itself used up anyway?",
             "Chapter three. Renewable resources: the fishery.", lit={1954: r"Gordon", 2008: r"Costello et al."},
             scale=("market", "world"), horizon=("a year", "a decade"))
        self.yields()
        self.dynamics()
        self.world()

    def yields(self):
        F = load("fishery")["curves"]
        E = np.array(F["effort"])
        ax = plane([0, 0.52], [0, 0.16], center=LEFT * 2.0 + DOWN * 0.35, x_length=7.4, y_length=4.6,
                   xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5], yticks=[0, 0.04, 0.08, 0.12, 0.16],
                   xlabel=r"fishing effort, \ boats at sea", ylabel=r"catch a year, \ sustained \ (= revenue)",
                   xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.2f}", font_size=14)
        rev = path(ax, E, F["revenue"], FISH, 3.2)
        cost = seg(ax, 0, 0, 0.52, 0.2 * 0.52, LOSS, 2.6)
        e_oa, e_mey, e_msy = F["e_open"], F["e_mey"], F["e_msy"]
        y = lambda e: e * (1 - e / 0.5)  # noqa: E731
        marks = VGroup(
            VGroup(vline(ax, e_mey, 0, y(e_mey), OPT), label(r"most rent", font_size=15, color=OPT).next_to(
                ax.ax.c2p(e_mey, y(e_mey)), UL, buff=0.08)),
            VGroup(vline(ax, e_msy, 0, y(e_msy), GREY_B), label(r"most fish", font_size=15, color=GREY_B).next_to(
                ax.ax.c2p(e_msy, y(e_msy)), UP, buff=0.12)),
            VGroup(vline(ax, e_oa, 0, y(e_oa), LOSS), label(r"open access", font_size=15, color=LOSS).next_to(
                ax.ax.c2p(e_oa, 0.0), UR, buff=0.08)),
        )
        rent = VGroup(Line(ax.ax.c2p(e_mey, 0.2 * e_mey), ax.ax.c2p(e_mey, y(e_mey)), color=OPT, stroke_width=9),
                      label(r"rent", font_size=15, color=OPT).next_to(ax.ax.c2p(e_mey, 0.12 * e_mey + 0.5 * y(e_mey)),
                                                                     LEFT, buff=0.12))
        side = VGroup(
            label(r"the stock grows \\ logistically; \ more boats \\ catch more, \ until \\ the stock shrinks",
                  font_size=18, color=WHITE),
            label(r"red line: \ the cost \\ of the boats", font_size=18, color=LOSS),
            label(rf"open access: \ boats \\ enter until the rent \\ is gone; \ stock {F['stock_open']:.1f}",
                  font_size=18, color=LOSS),
            label(rf"an owner or a quota: \\ half the boats; \\ stock {F['stock_mey']:.1f}, \ rent \\ "
                  rf"{F['rent_mey']:.2f} a year", font_size=18, color=OPT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Fish renew themselves, so how can they run out? Scott Gordon answered in 1954. <bookmark mark='a'/> A "
            "fish stock grows fastest at middling size. Send out more boats and the catch rises at first, but past "
            "a point the stock shrinks so much that the sustained catch falls: the green hill. <bookmark mark='b'/> "
            "The red line is what the boats cost. <bookmark mark='c'/> Where anyone may fish, boats keep coming as "
            "long as fishing pays, until revenue equals cost and the rent is gone: the sea is fished to where the "
            f"stock is {F['stock_open']:.1f} of its natural size. <bookmark mark='d'/> A single owner, or a quota "
            "that limits the catch, stops at the effort where the gap between revenue and cost is greatest: half "
            f"the boats, a stock of {F['stock_mey']:.1f}, and a rent worth having. Notice that this is fewer boats "
            "even than the effort that catches the most fish. The fish are not lost because they are taken, but "
            "because nobody owns the ones left behind."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(rev), FadeIn(marks[1]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(cost), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(marks[2]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(marks[0]), FadeIn(rent), FadeIn(side[3]))
        self.clear_scene()

    def dynamics(self):
        D = load("fishery")
        O, Q = D["open"], D["quota"]
        ax = plane([0, 80], [0, 1.05], center=LEFT * 2.0 + DOWN * 0.35, x_length=7.4, y_length=4.6,
                   xticks=[0, 20, 40, 60, 80], yticks=[0, 0.25, 0.5, 0.75, 1.0], xlabel=r"years",
                   ylabel=r"stock, \ share of its natural size", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.2f}", font_size=14)
        so = path(ax, O["t"], O["stock"], LOSS, 3.2, smooth=False)
        sq = path(ax, Q["t"], Q["stock"], OPT, 3.2, smooth=False)
        k = int(np.argmin(O["stock"]))
        low = dot(ax, O["t"][k], O["stock"][k], WHITE, 0.07)
        low_l = label(rf"year {O['t'][k]:.0f}: \ {D['open_min']:.2f}", font_size=16, color=WHITE).next_to(
            low, UR, buff=0.1)
        side = VGroup(
            label(r"red: \ open access, \\ boats enter while \\ fishing pays", font_size=18, color=LOSS),
            label(rf"the fleet overshoots: \\ the stock falls to \\ {D['open_min']:.2f}, \ then settles \\ at "
                  rf"{D['open_end']:.1f}", font_size=18, color=LOSS),
            label(rf"green: \ a quota of \\ {D['quota_level']} a year, \ traded: \\ the stock settles \\ at "
                  rf"{D['quota_end']:.2f}", font_size=18, color=OPT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Over time it is worse than the static picture. <bookmark mark='a'/> Start an Island fishery at its "
            "natural size, and let boats enter while fishing pays, as Vernon Smith modelled it in 1969. <bookmark "
            "mark='b'/> The fleet grows on yesterday's profits, and by the time catches fall there are far too many "
            f"boats: in year {O['t'][k]:.0f} the stock is down to {100 * D['open_min']:.0f} percent of its natural "
            f"size, before boats leave and it recovers to {100 * D['open_end']:.0f}. Real fisheries have collapsed "
            "this way and not come back. <bookmark mark='c'/> Now cap the total catch at "
            f"{D['quota_level']} a year and let the boats trade their shares of it. The stock settles at "
            f"{100 * D['quota_end']:.0f} percent, and the race to fish first is over, because a share is worth more "
            "if the stock is kept healthy."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(so), run_time=3.0)
            self.play(FadeIn(low), FadeIn(low_l), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(sq), FadeIn(side[2]), run_time=2.5)
        self.clear_scene()

    def world(self):
        Fa = load("fao")
        T = tables.FISH_48.data
        ax = plane([1972, 2023], [0, 40], center=LEFT * 2.0 + DOWN * 0.35, x_length=7.4, y_length=4.6,
                   xticks=[1975, 1985, 1995, 2005, 2015], yticks=[0, 10, 20, 30, 40],
                   ylabel=r"share of assessed fish stocks overexploited", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}\\%", font_size=14)
        ln = path(ax, Fa["year"], Fa["overexploited"], LOSS, 3.2, smooth=False)
        dots = VGroup(*[dot(ax, y, v, LOSS, 0.045) for y, v in zip(Fa["year"], Fa["overexploited"])])
        side = VGroup(
            label(rf"{Fa['first_year']}: \ {Fa['first']:.0f}\% \\ overexploited", font_size=19, color=LOSS),
            label(rf"{Fa['last_year']}: \ {Fa['last']:.1f}\%", font_size=19, color=LOSS),
            label(rf"Costello, \ Gaines and \\ Lynham, \ 2008: \ over \\ {T['fisheries']:,} fisheries; \\ catch "
                  r"shares halt, \\ even reverse, \\ the slide to collapse".replace(",", "{,}"), font_size=18,
                  color=OPT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"FAO, \ The State of World Fisheries and Aquaculture (2025), \ via Our World in Data",
                       corner=DL, font_size=12)
        with self.voiceover(
            "And in the world's oceans? <bookmark mark='a'/> The UN's Food and Agriculture Organization assesses "
            f"the world's fish stocks. In {Fa['first_year']}, {Fa['first']:.0f} percent were overexploited. "
            f"<bookmark mark='b'/> By {Fa['last_year']}, {Fa['last']:.1f} percent. <bookmark mark='c'/> Christopher "
            f"Costello, Steven Gaines and John Lynham studied over {T['fisheries']:,} fisheries and found that "
            "catch shares, quotas owned and traded by fishers, halt and even reverse the slide toward collapse: by "
            "2003, the share of quota fisheries that had collapsed was half that of the rest. Property rights did "
            "for fish what prices did for metals. The air has no such owner. That is the next chapter."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(dots[0]))
            vo.wait_until("b")
            self.play(Create(ln), FadeIn(dots[1:]), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()
