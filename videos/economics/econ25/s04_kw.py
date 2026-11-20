from __future__ import annotations

from videos.economics.econ25.common import *  # noqa: F403

GOOD_C = (SALT, COCO, FISH)


class KW(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Kiyotaki and Wright: \ money as an equilibrium", r"When does a costly good become money "
             r"too, \ and can a useless one?", "Chapter three. Kiyotaki and Wright: money as an equilibrium.",
             lit={1989: r"Kiyotaki and Wright", 1999: r"Duffy and Ochs"}, scale=("market",), horizon=("a month",))
        self.smoked()
        self.values()
        self.region()
        self.lab_fiat()

    def smoked(self):
        k = load("kw")
        s = k["spec"]
        rows = VGroup(
            label(rf"now the fish is smoked: \ it costs {k['c3_smoked']:g} a month to keep, \ not {k['c'][2]:g}",
                  font_size=25, color=FISH),
            label(r"Ana's speculative trade: \ give coconuts, \ take fish, \ though she cannot eat fish", font_size=23,
                  color=COCO),
            label(r"because Dara, \ who holds salt, \ wants fish: \ fish buys salt faster than coconuts do",
                  font_size=23, color=GREY_A),
        ).arrange(DOWN, buff=0.35).to_edge(UP, buff=0.5)
        ax = plane([-0.6, 2.6], [0, 1.0], center=LEFT * 2.6 + DOWN * 1.4, x_length=5.0, y_length=3.0, xticks=[],
                   yticks=[0, 0.5, 1.0], ylabel=r"share of trades where it is passed on", yfmt=lambda v: f"{v:g}",
                   font_size=14)
        bars, names, vals = VGroup(), VGroup(), VGroup()
        for i, (g, col) in enumerate(zip(k["goods"], GOOD_C)):
            lo, hi = ax.ax.c2p(i, 0), ax.ax.c2p(i, max(s["medium"][i], 0.004))
            bars.add(Rectangle(width=0.8, height=hi[1] - lo[1], fill_color=col, fill_opacity=0.85,
                               stroke_width=0).move_to((lo + hi) / 2))
            names.add(label(g, font_size=17, color=col).next_to(lo, DOWN, buff=0.12))
            vals.add(label(rf"{100 * s['medium'][i]:.0f}\%", font_size=18, color=col).next_to(bars[-1], UP, buff=0.08))
        side = label(r"two moneys: \\ salt and fish", font_size=26, color=E.ACCENT).move_to(RIGHT * 3.4 + DOWN * 1.2)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Now change one thing. The islanders learn to smoke fish, and it keeps far better: "
            f"{k['c3_smoked']:g} a month instead of {k['c'][2]:g}. <bookmark mark='a'/> Ana, holding coconuts, now "
            "takes fish when offered, though she cannot eat it. <bookmark mark='b'/> She speculates, because Dara, "
            "who has salt, wants fish, and will trade salt for it at once, while coconuts only buy salt from Bo's "
            "rare spare. Fish is more marketable, and now cheap enough to hold. <bookmark mark='c'/> Run the Island "
            f"again: salt is passed on in {100 * s['medium'][0]:.0f} percent of such trades and fish in "
            f"{100 * s['medium'][2]:.0f}. The Island has two moneys. Which goods become money depends on what they "
            "cost to hold, and on what everyone else accepts."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(ax), FadeIn(names), FadeIn(tag),
                      *[GrowFromEdge(b_, DOWN) for b_ in bars], FadeIn(vals), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(side), Indicate(bars[2], color=WHITE))
        self.clear_scene()

    def values(self):
        k = load("kw")
        rows = VGroup(
            MathTex(r"V_c = -c_2 + \beta\,\mathbb{E}\big[\text{what a month's meeting brings}\mid \text{holding "
                    r"coconuts}\big]", font_size=34, color=COCO),
            MathTex(r"V_f = -c_3 + \beta\,\mathbb{E}\big[\text{what a month's meeting brings}\mid \text{holding "
                    r"fish}\big]", font_size=34, color=FISH),
            label(r"Ana should take fish for coconuts \ if and only if \ $V_f > V_c$", font_size=25, color=WHITE),
            label(rf"fresh fish \ ($c_3 = {k['c'][2]:g}$): \ $V_f - V_c = {k['fresh_fund']['gain']:.2f}$: \ keep "
                  r"the coconuts", font_size=24, color=SALT),
            label(rf"smoked fish \ ($c_3 = {k['c3_smoked']:g}$): \ $V_f - V_c = {k['smoked_spec']['gain']:+.2f}$: \ "
                  r"take the fish", font_size=24, color=FISH),
            label(r"each is an equilibrium only if, \ given what everyone else does, \ no one wants to change",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        tag = published_tag(r"Kiyotaki and Wright, JPE 97(4) (1989): \ 927--954", corner=DR, font_size=12)
        with self.voiceover(
            "Nobuhiro Kiyotaki and Randall Wright built this economy in 1989 to show that money can emerge as an "
            "equilibrium of search. Here is Ana's decision. <bookmark mark='a'/> Holding coconuts is worth minus "
            "their storage cost, plus what next month's meeting is expected to bring, discounted. "
            "<bookmark mark='b'/> Holding fish, the same with fish's storage cost and fish's prospects. "
            "<bookmark mark='c'/> She should take fish exactly when holding fish is worth more. "
            "<bookmark mark='d'/> With fresh fish, Agora's solution says no: by "
            f"{abs(k['fresh_fund']['gain']):.2f} in units of a meal. <bookmark mark='e'/> With smoked fish, given "
            f"that everyone else speculates too, yes: by {k['smoked_spec']['gain']:.2f}. "
            "<bookmark mark='f'/> Each pattern of trade is an equilibrium only if, given what everyone else accepts, "
            "nobody wants to change what they accept."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            for mk, r_ in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def region(self):
        r = load("kw_region")
        k = load("kw")
        c3, bt = r["c3"], r["beta"]
        ax = plane([c3[0], c3[-1]], [bt[0], bt[-1]], center=LEFT * 2.2 + DOWN * 0.3, x_length=7.0, y_length=5.0,
                   xticks=[0.3, 0.4, 0.5, 0.6, 0.7, 0.8], yticks=[0.5, 0.6, 0.7, 0.8, 0.9],
                   xlabel=r"what fish costs to keep, \ $c_3$", ylabel=r"patience, \ $\beta$", xfmt=lambda v: f"{v:g}",
                   yfmt=lambda v: f"{v:g}", font_size=16)
        dx = (c3[1] - c3[0])
        dy = (bt[1] - bt[0])
        cells = VGroup()
        for i, b in enumerate(bt):
            for j, c in enumerate(c3):
                f_, s_ = r["fund"][i][j], r["spec"][i][j]
                col = MONEY if (f_ and s_) else SALT if f_ else FISH if s_ else GREY_D
                p0, p1 = ax.ax.c2p(c - dx / 2, b - dy / 2), ax.ax.c2p(c + dx / 2, b + dy / 2)
                cells.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=col, fill_opacity=0.4,
                                    stroke_width=0).move_to((p0 + p1) / 2))
        fresh = VGroup(dot(ax, k["c"][2], k["beta"], color=E.ACCENT, r=0.11),
                       label(r"fresh", font_size=18, color=E.ACCENT).next_to(ax.ax.c2p(k["c"][2], k["beta"]), UP,
                                                                             buff=0.12))
        smoked = VGroup(dot(ax, k["c3_smoked"], k["beta"], color=E.ACCENT, r=0.11),
                        label(r"smoked", font_size=18, color=E.ACCENT).next_to(ax.ax.c2p(k["c3_smoked"], k["beta"]),
                                                                               UP, buff=0.12))
        side = VGroup(
            label(r"only salt is money", font_size=20, color=SALT),
            label(r"salt and fish are money", font_size=20, color=FISH),
            label(r"neither pattern holds: \\ Ana takes fish \\ only some of the time", font_size=20,
                  color=GREY_B),
            label(r"the Island: \ fresh, \ then smoked", font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Map it. Along the bottom, what fish costs to keep; up the side, how patient the islanders are. Agora "
            "checks both patterns of trade at every point. <bookmark mark='a'/> Where fish is costly, only salt "
            "circulates. <bookmark mark='b'/> Where fish keeps well, salt and fish both do. "
            + "<bookmark mark='c'/> In a thin band between them, neither pattern holds, and Ana takes fish only some "
            "of the time. The boundary moves with patience: patient islanders care more about where a good will take "
            "them, and less about this month's cost of keeping it. "
            + "<bookmark mark='d'/> The Island's two cases sit on either side of the line."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(cells), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(fresh), FadeIn(smoked), FadeIn(side[3]))
        self.clear_scene()

    def lab_fiat(self):
        rows = VGroup(
            label(r"fiat money: \ add a token nobody eats and nobody makes, \ costless to keep", font_size=24,
                  color=MONEY),
            label(r"if everyone expects it to be accepted, \ it is accepted: \ an equilibrium", font_size=23,
                  color=MONEY),
            label(r"and if everyone expects it not to be, \ it is worthless: \ that is an equilibrium too",
                  font_size=23, color=PRICE),
            label(r"the laboratory: \ Duffy and Ochs, \ 1999: \ people played the cheap-to-keep strategies,",
                  font_size=22, color=GREY_A),
            label(r"even where speculating would have paid more", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Kiyotaki and Wright (1989); \ Duffy and Ochs, AER 89(4) (1999): \ 847--877", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Kiyotaki and Wright took one more step. <bookmark mark='a'/> Add a token that nobody eats and nobody "
            "makes, that costs nothing to keep. <bookmark mark='b'/> If everyone expects it to be accepted, it is "
            "accepted, because it buys things: fiat money is an equilibrium. <bookmark mark='c'/> But if everyone "
            "expects it to be refused, it is worthless, and that is an equilibrium too. Paper money rests on "
            "expectations, which is why chapter six's hyperinflations can destroy it. <bookmark mark='d'/> John "
            "Duffy and Jack Ochs ran this economy in the laboratory with paid volunteers. "
            "<bookmark mark='e'/> They mostly played the cheap-to-keep strategies, even in designs where speculating "
            "would have paid them more: money's emergence is easy in theory and slower in practice."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
