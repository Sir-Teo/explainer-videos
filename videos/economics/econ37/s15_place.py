from __future__ import annotations

from videos.economics.econ37.common import *  # noqa: F403


class Place(VoiceoverScene):
    def construct(self):
        card(self, 13, r"Place-based policy", r"Can a government make a place prosper, and who gains if it does?",
             "Chapter thirteen. Place-based policy.",
             lit={1933: r"the Tennessee Valley Authority", 1980: r"Shenzhen's zone", 2014: r"Kline and Moretti"},
             scale=("city", "nation"), horizon=("a century",))
        self.shenzhen()
        self.tva()
        self.incidence()

    def shenzhen(self):
        P = load("place")
        S = P["shenzhen"]
        ax = plane([0.4, 2.6], [0, 20], center=LEFT * 2.6 + DOWN * 0.4, x_length=4.8, y_length=4.6, xticks=[],
                   yticks=[0, 5, 10, 15, 20], ylabel=r"people, \ millions", yfmt=lambda v: f"{v:.0f}", font_size=14)
        vals = ((S["pop1979"] / 1e6, GREY_B, r"1979"), (S["pop2020"] / 1e6, RENT, r"2020 census"))
        bars, nms = VGroup(), VGroup()
        for k, (v, col, n) in enumerate(vals):
            p0, p1 = ax.ax.c2p(k + 0.7, 0), ax.ax.c2p(k + 1.3, v)
            bars.add(Rectangle(width=p1[0] - p0[0], height=max(p1[1] - p0[1], 0.02), fill_color=col,
                               fill_opacity=0.85, stroke_width=0).move_to((p0 + p1) / 2))
            nms.add(VGroup(label(n, font_size=17, color=col), label(f"{v:.2f}m", font_size=17, color=WHITE))
                    .arrange(DOWN, buff=0.05).next_to(ax.ax.c2p(k + 1, 0), DOWN, buff=0.1))
        side = VGroup(
            label(rf"{S['sez']}: \ a special economic zone \\ beside Hong Kong", font_size=20, color=RENT),
            label(r"different rules for foreign \\ firms, \ land and labour", font_size=19, color=WHITE),
            label(rf"{S['pop2020'] / S['pop1979']:.0f} times as many people \\ four decades later", font_size=20,
                  color=E.ACCENT),
            label(r"but the zone was also \\ China's whole opening: \\ no control group", font_size=18,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5)
        tag = published_tag(tables.SHENZHEN.tag, corner=DR, font_size=12)
        with self.voiceover(
            "Can policy make a place? The most dramatic case is Shenzhen. <bookmark mark='a'/> In 1980 China made "
            "this small city across the border from Hong Kong a special economic zone, with its own rules for "
            f"foreign firms, land and labour. In 1979 it had about {S['pop1979'] / 1e3:.0f} thousand residents; "
            f"<bookmark mark='b'/> the census of 2020 counted {S['pop2020'] / 1e6:.2f} million, "
            f"<bookmark mark='c'/> {S['pop2020'] / S['pop1979']:.0f} times as many. <bookmark mark='d'/> But "
            "Shenzhen was a door through which a whole country opened to the world, so it is hard to say what the "
            "zone itself did, and there is no Shenzhen without China."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(bars[0]), FadeIn(nms[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[1], DOWN), FadeIn(nms[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def tva(self):
        cards = point_cards([
            (r"1933", r"dams, \ electricity, \\ roads and canals \\ for a poor region", WHITE),
            (r"farming", r"gains while the \\ money flowed, \\ reversed after", FARM),
            (r"manufacturing", r"gains that kept \\ growing after \\ the money stopped", WAGE),
            (r"the nation", r"local gains offset \\ elsewhere; \ the \\ infrastructure paid", E.ACCENT),
        ], width=12.8, cols=4, font_size=20).move_to(DOWN * 0.1)
        head = label(r"the Tennessee Valley Authority", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.KLINE_MORETTI_2014.tag, corner=DR, font_size=12)
        with self.voiceover(
            "America's largest experiment was the Tennessee Valley Authority. <bookmark mark='a'/> From 1933 the "
            "federal government built dams, power lines, roads and canals across one of the poorest regions in the "
            "country. Patrick Kline and Enrico Moretti compared the region with others that had been proposed for "
            "similar authorities but never got them. <bookmark mark='b'/> Gains in farming lasted only as long "
            "as the money, and reversed when the transfers wound down. <bookmark mark='c'/> Gains in manufacturing "
            "kept growing long after: a big push that, once started, sustained itself through agglomeration. "
            "<bookmark mark='d'/> But for the nation the local agglomeration largely moved activity from elsewhere; "
            "what raised national productivity, by more than it cost, was the infrastructure itself."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def incidence(self):
        P = load("place")["towns"]
        rows = [(r"rents", "dlogr", RENT), (r"people", "dlogN", CITY), (r"wages", "dlogw", WAGE),
                (r"everyone's utility", "dv", AMENITY)]

        def panel(d, x0, title, col):
            g = VGroup(label(title, font_size=21, color=col).move_to(np.array([x0, 2.3, 0])))
            for k, (nm, key, c) in enumerate(rows):
                v = d[key]
                y = 1.3 - 0.85 * k
                r = Rectangle(width=max(abs(v) * 14, 0.02), height=0.42, stroke_width=0, fill_color=c,
                              fill_opacity=0.85).move_to(np.array([x0 + 0.2 + v * 7, y, 0]))
                g.add(VGroup(label(nm, font_size=16, color=GREY_A).move_to(np.array([x0 - 1.7, y, 0])), r,
                             label(f"{100 * v:+.1f}\\%", font_size=16, color=WHITE).next_to(r, RIGHT, buff=0.08)))
            g.add(Line(np.array([x0 + 0.2, 1.75, 0]), np.array([x0 + 0.2, 1.3 - 0.85 * 3 - 0.45, 0]),
                       color=GREY_B, stroke_width=1.5))
            return g

        h, gr = P["Harbour"], P["Grove"]
        left = panel(h, -3.6, rf"Harbour: \ housing elasticity {h['eta']:.1f}", RENT)
        right = panel(gr, 3.2, rf"Grove: \ housing elasticity {gr['eta']:.1f}", GAIN)
        head = label(r"the same subsidy, \ productivity +10\%, \ in two towns", font_size=22, color=WHITE).to_edge(
            UP, buff=0.3)
        foot = wrapped_label(r"where housing is tight, \ a subsidy to a place becomes rent for its landowners; \ "
                             r"workers gain little anywhere, \ because they can move", 12.0, 19, E.ACCENT).to_edge(
            DOWN, buff=0.4)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Who gains from a subsidy to a place? The Island answers with spatial equilibrium. "
            "<bookmark mark='a'/> Give Harbour, where housing is hard to build, a subsidy worth ten percent of "
            f"productivity. Its rents rise {100 * h['dlogr']:.0f} percent and its population "
            f"{100 * h['dlogN']:.0f}; everyone's utility on the Island rises {100 * h['dv']:.1f} percent. "
            "<bookmark mark='b'/> Give the same subsidy to Grove, where building is easy: rents rise only "
            f"{100 * gr['dlogr']:.0f} percent, the town grows {100 * gr['dlogN']:.0f} percent, and everyone gains "
            f"{100 * gr['dv']:.1f} percent. <bookmark mark='c'/> Where housing is tight, much of a place-based "
            "subsidy ends up as rent for local landowners. Some economists conclude that policy should help "
            "people, not places; others answer that where joblessness is concentrated and persistent, as in Part "
            "thirty-six's China-shock towns, places are how you reach the people."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(left, lag_ratio=0.1), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(right, lag_ratio=0.1), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
