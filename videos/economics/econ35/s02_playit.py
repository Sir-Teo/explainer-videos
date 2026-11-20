from __future__ import annotations

from videos.economics.econ35.common import *  # noqa: F403

CHIP = ("#E8A0B4", "#F2C14E", "#7FD1B9")


def hours_table(P, font_size=26):
    """The four numbers: hours per unit of fish and of cloth on the Island and in the Archipelago."""
    cells = [["", r"a fish", r"a bolt of cloth"],
             [r"the Island", f"{P['hours_island'][0]:.0f} hours", f"{P['hours_island'][1]:.0f} hours"],
             [r"the Archipelago", f"{P['hours_arch'][0]:.0f} hour", f"{P['hours_arch'][1]:.0f} hours"]]
    cols = [ISLAND, ARCH]
    g = VGroup()
    for i, row in enumerate(cells):
        for j, txt in enumerate(row):
            col = (FISH if j == 1 else CLOTH) if i == 0 and j else (cols[i - 1] if j == 0 and i else WHITE)
            m = label(txt, font_size=font_size, color=col) if txt else Dot(radius=0.001, fill_opacity=0)
            m.move_to(np.array([(-3.4, 0.6, 3.6)[j], 1.0 - 1.0 * i, 0]))
            g.add(m)
    rule = Line(LEFT * 5.2, RIGHT * 5.2, color=GREY_C, stroke_width=1.5).move_to(UP * 0.5)
    return VGroup(g, rule)


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Play it: \ four numbers", r"One island is worse at everything. Who should make what?",
             "Chapter one. Play it: four numbers.", lit={1817: r"Ricardo"}, scale=("nation",),
             horizon=("a year",))
        self.desk()
        self.choose()
        self.reveal()
        self.wages()

    def _chips(self):
        P = load("playit")
        chips = VGroup(*[VGroup(RoundedRectangle(width=4.0, height=0.95, corner_radius=0.12, stroke_color=c,
                                                 stroke_width=3, fill_color=c, fill_opacity=0.12),
                                label(rf"{ch}: \ {tex_safe(t)}", font_size=20, color=c))
                         for c, ch, t in zip(CHIP, "ABC", P["options"])]).arrange(RIGHT, buff=0.3)
        for ch in chips:
            ch[1].move_to(ch[0])
        return chips

    def desk(self):
        P = load("playit")
        tab = hours_table(P).move_to(UP * 0.4)
        head = label(r"hours of work for one unit", font_size=26, color=E.ACCENT).to_edge(UP, buff=0.6)
        foot = VGroup(
            label(rf"the Island has {P['L_island']:.0f} hours a week; \ the Archipelago {P['L_arch']:.0f}",
                  font_size=22, color=GREY_A),
            label(r"each spends half its income on fish \ and half on cloth", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.8)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Your turn. The Island and its neighbour, the Archipelago, make two things: fish and cloth. "
            "<bookmark mark='a'/> Here are the hours of work each needs for one unit. The Island needs three hours "
            "to land a fish and six to weave a bolt of cloth. The Archipelago, with better boats and better looms, "
            "needs one hour for a fish and four for a bolt. <bookmark mark='b'/> The Archipelago is better at both. "
            "<bookmark mark='c'/> The Island has twice as many hours of work to offer each week, and people in both "
            "spend half their income on fish and half on cloth."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tab[1]), FadeIn(tab[0][:3]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in tab[0][3:]], lag_ratio=0.25), run_time=2.0)
            vo.wait_until("b")
            self.play(Indicate(VGroup(tab[0][7], tab[0][8]), color=WHITE, scale_factor=1.1))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def choose(self):
        P = load("playit")
        tab = hours_table(P, font_size=22).scale(0.85).to_edge(UP, buff=0.5)
        q = label(r"if they trade, \ who should make what?", font_size=30, color=E.ACCENT).next_to(tab, DOWN,
                                                                                                  buff=0.5)
        chips = self._chips().next_to(q, DOWN, buff=0.5)
        ring = countdown().scale(0.7).next_to(chips, DOWN, buff=0.4)
        with self.voiceover(
            "If they trade, who should make what? <bookmark mark='a'/> Should the Archipelago make both, since it "
            "is better at both? Should the Island make the cloth and the Archipelago the fish? Or the other way "
            "round? Pause, and choose."
        ) as vo:
            self.play(FadeIn(tab), FadeIn(q))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chips], lag_ratio=0.3), FadeIn(ring),
                      run_time=1.5)
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.clear_scene()

    def reveal(self):
        P = load("playit")
        aI, aA = P["hours_island"], P["hours_arch"]
        axI = plane([0, 620], [0, 220], center=LEFT * 3.6 + DOWN * 0.6, x_length=5.2, y_length=4.0,
                    xticks=[0, 200, 400, 600], yticks=[0, 100, 200], xlabel=r"fish", ylabel=r"cloth",
                    xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        axA = plane([0, 620], [0, 220], center=RIGHT * 2.6 + DOWN * 0.6, x_length=5.2, y_length=4.0,
                    xticks=[0, 200, 400, 600], yticks=[0, 100, 200], xlabel=r"fish", ylabel=r"cloth",
                    xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        tI = label(r"the Island", font_size=22, color=ISLAND).next_to(axI, UP, buff=0.12)
        tA = label(r"the Archipelago", font_size=22, color=ARCH).next_to(axA, UP, buff=0.12)
        fI = seg(axI, P["L_island"] / aI[0], 0, 0, P["L_island"] / aI[1], ISLAND, 3)
        fA = seg(axA, P["L_arch"] / aA[0], 0, 0, P["L_arch"] / aA[1], ARCH, 3)
        I_, A_ = P["aut_island"], P["aut_arch"]
        Ic, Ac = P["island"], P["arch"]
        autI, autA = dot(axI, I_["c1"], I_["c2"], WHITE), dot(axA, A_["c1"], A_["c2"], WHITE)
        # trade lines through each country's production point at the world price (3 fish per bolt)
        p = P["p"]
        qI, qA = (Ic["q1"], Ic["q2"]), (Ac["q1"], Ac["q2"])
        tlI = seg(axI, qI[0] + p * qI[1], 0, 0, qI[1] + qI[0] / p, GAIN, 2.5, dashed=True)
        tlA = seg(axA, qA[0] + p * qA[1], 0, 0, qA[1] + qA[0] / p, GAIN, 2.5, dashed=True)
        cI, cA = dot(axI, Ic["c1"], Ic["c2"], GAIN, 0.09), dot(axA, Ac["c1"], Ac["c2"], GAIN, 0.09)
        opp = VGroup(
            label(rf"a bolt of cloth costs the Island {aI[1] / aI[0]:.0f} fish", font_size=21, color=ISLAND),
            label(rf"and the Archipelago {aA[1] / aA[0]:.0f} fish", font_size=21, color=ARCH),
        ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.25)
        verdict = label(r"B: \ the Island makes cloth; \ the Archipelago, \ fish", font_size=24,
                        color=CHIP[1]).to_edge(DOWN, buff=0.3)
        gains = VGroup(
            label(rf"+{100 * Ic['gain']:.0f}\%", font_size=24, color=GAIN).next_to(cI, UR, buff=0.08),
            label(rf"+{100 * Ac['gain']:.0f}\%", font_size=24, color=GAIN).next_to(cA, UR, buff=0.08),
        )
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The answer is B, and the reason is in what each good costs in terms of the other. "
            "<bookmark mark='a'/> On the Island, the six hours that weave a bolt of cloth could land two fish; so a "
            "bolt costs two fish. In the Archipelago, four hours of weaving could land four fish: a bolt costs four. "
            "Cloth is relatively cheap on the Island. That is its comparative advantage, even though it is worse "
            "at weaving in absolute terms. <bookmark mark='b'/> Here is what each can make alone: its production "
            "frontier, and the white dot, what it consumes with half its income on each good. "
            f"<bookmark mark='c'/> Now let them trade at a price between the two costs, {p:.0f} fish a bolt, which "
            "is where the market settles. The Island weaves only cloth and sells half of it for fish; the "
            "Archipelago fishes only, and buys cloth. <bookmark mark='d'/> Each can now reach the dashed line, "
            "beyond its own frontier. <bookmark mark='e'/> The Island consumes the same cloth and half as much fish "
            f"again; the Archipelago the same fish and a third more cloth: gains of {100 * Ic['gain']:.0f} and "
            f"{100 * Ac['gain']:.0f} percent, for both, from the same hours of work."
        ) as vo:
            self.play(FadeIn(opp[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(opp[1]))
            vo.wait_until("b")
            self.play(FadeIn(axI), FadeIn(axA), FadeIn(tI), FadeIn(tA), Create(fI), Create(fA), FadeIn(autI),
                      FadeIn(autA), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(verdict), Create(tlI), Create(tlA))
            vo.wait_until("d")
            self.play(FadeIn(cI, scale=1.4), FadeIn(cA, scale=1.4))
            vo.wait_until("e")
            self.play(FadeIn(gains))
        self.clear_scene()

    def wages(self):
        P = load("playit")
        Ic, Ac = P["island"], P["arch"]
        rows = VGroup(
            label(r"wages, \ in fish per hour", font_size=28, color=E.ACCENT),
            label(rf"the Island: \ {Ic['w1']:.1f}; \ the Archipelago: \ {Ac['w1']:.1f}", font_size=26,
                  color=WHITE),
            label(r"the Archipelago fears the Island's cheap labour", font_size=24, color=ARCH),
            label(r"the Island fears the Archipelago's better boats and looms", font_size=24, color=ISLAND),
            label(r"both gain: \ wages follow productivity, \ trade follows comparative cost", font_size=24,
                  color=GAIN),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "One more number. <bookmark mark='a'/> After trade an Islander earns half a fish an hour, and an "
            f"Archipelagan {Ac['w1']:.0f} fish: the Island's wage is half the Archipelago's, because its workers "
            "are less productive. <bookmark mark='b'/> So both sides have a fear. In the Archipelago people say "
            "they cannot compete with the Island's cheap labour. <bookmark mark='c'/> On the Island people say they "
            "cannot compete with the Archipelago's better boats and looms. <bookmark mark='d'/> Both are wrong. "
            "Wages follow productivity, trade follows comparative cost, and the gains go to both."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
