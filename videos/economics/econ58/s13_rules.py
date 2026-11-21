from __future__ import annotations

from videos.economics.econ58.common import *  # noqa: F403


class Rules(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Regulatory impact analysis", r"When is a rule worth what it costs?",
             "Chapter eleven. Regulatory impact analysis.", lit={1981: r"Executive Order 12291",
                                                                 1993: r"Executive Order 12866"},
             scale=("firm", "nation"), horizon=("a decade",))
        self.history()
        self.rule()

    def history(self):
        cards = VGroup(
            history_card(1981, r"Executive Order 12291", r"agencies must analyse every major rule's costs and "
                         r"benefits, \ and not proceed unless the benefits outweigh the costs; \ a review office in "
                         r"the budget office checks", color=CBO, width=11.4, font_size=22),
            history_card(1993, r"Executive Order 12866", r"replaces it: \ choose the approach that maximizes net "
                         r"benefits, \ for significant rules, \ counting what cannot be quantified too",
                         color=BEN, width=11.4, font_size=22),
            history_card(2003, r"Circular A-4", r"how to do it: \ the baseline, \ the alternatives, \ the rates, \ "
                         r"the uncertainty", color=RATE, width=11.4, font_size=22),
        ).arrange(DOWN, buff=0.35).move_to(DOWN * 0.1)
        with self.voiceover(
            "Laws are scored; regulations are appraised. <bookmark mark='a'/> In February 1981 Ronald Reagan's "
            "Executive Order 12291 required American agencies to analyse the costs and benefits of every major rule, "
            "and not to proceed unless the benefits outweighed the costs, with an office in the budget office to "
            "check. <bookmark mark='b'/> In 1993 Bill Clinton's Executive Order 12866 replaced it, asking agencies to "
            "choose the approach that maximizes net benefits, counting what cannot be quantified too, and every "
            "president since has kept its core. <bookmark mark='c'/> Circular A-4 is the manual: the baseline, the "
            "alternatives, the discount rates of the last chapter, and how to report uncertainty."
        ) as vo:
            for mk, c_ in zip("abc", cards):
                vo.wait_until(mk)
                self.play(FadeIn(c_, shift=UP * 0.1))
        self.clear_scene()

    def rule(self):
        R = load("rule")
        rows, low = R["rows"], R["low_vsl"]
        ax = plane([-0.6, 2.6], [-800, 900], center=LEFT * 2.8 + DOWN * 0.5, x_length=6.4, y_length=5.0, xticks=[],
                   yticks=[-750, -500, -250, 0, 250, 500, 750], ylabel=r"present value, \ millions",
                   yfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0", font_size=14)
        z = Line(ax.ax.c2p(-0.6, 0), ax.ax.c2p(2.6, 0), color=GREY_C, stroke_width=1.2)

        def rect(x, y0, y1, col, w=0.17):
            p0, p1 = ax.ax.c2p(x - w, y0), ax.ax.c2p(x + w, y1)
            return Rectangle(width=p1[0] - p0[0], height=abs(p1[1] - p0[1]), fill_color=col, fill_opacity=0.85,
                             stroke_width=0).move_to((p0 + p1) / 2)

        stacks, nets, labs = VGroup(), VGroup(), VGroup()
        for k, r in enumerate(rows):
            x = k - 0.2
            stacks.add(VGroup(rect(x, 0, r["lives"], SAFE), rect(x, r["lives"], r["lives"] + r["carbon"], NOISE),
                              rect(x + 0.4, 0, -r["cost"], COST)))
            nets.add(label(f"net ${r['net']:+.0f}$".replace("-", "{-}"), font_size=17, color=WHITE).next_to(
                ax.ax.c2p(k, r["lives"] + r["carbon"]), UP, buff=0.1))
            labs.add(label(rf"{100 * r['rate']:g}\%", font_size=18, color=RATE).next_to(ax.ax.c2p(k, -800), DOWN,
                                                                                         buff=0.12))
        side = VGroup(
            label(r"scrubbers at the Island's two power stations", font_size=21, color=E.ACCENT),
            label(rf"yellow: \ {R['deaths']:.0f} deaths a year avoided, \ at a VSL of {R['vsl']:.0f}", font_size=19,
                  color=SAFE),
            label(rf"lilac: \ carbon, \ at {R['scc']:.0f} a tonne", font_size=19, color=NOISE),
            label(r"red: \ 60 to install, \ 40 a year to run, \ 20 years", font_size=19, color=COST),
            label(rf"at a VSL of 5: \ net ${low[1]['net']:+.0f}$ at 3\%".replace("-", "{-}"), font_size=19,
                  color=COST),
            label(rf"break-even: \ {rows[1]['breakeven_deaths']:.1f} deaths a year avoided \ (at 3\%)",
                  font_size=20, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.3)
        tag = island_tag(r"the Island: \ a regulatory impact analysis", corner=DR, font_size=12)
        with self.voiceover(
            "Here is one on the Island. <bookmark mark='a'/> The ministry proposes scrubbers at its two power "
            "stations: sixty million to install, forty a year to run, for twenty years. <bookmark mark='b'/> The "
            f"benefits: about {R['deaths']:.0f} fewer deaths a year from cleaner air, at a value of a statistical life "
            f"of {R['vsl']:.0f} million, <bookmark mark='c'/> and a little less carbon, at a social cost of "
            f"{R['scc']:.0f} dollars a tonne. <bookmark mark='d'/> At two, three and seven percent the rule passes, "
            f"by {rows[0]['net']:.0f}, {rows[1]['net']:.0f} and {rows[2]['net']:.0f} million. <bookmark mark='e'/> "
            f"With a value of a statistical life of five million, it fails at every rate. <bookmark mark='f'/> When "
            "a benefit is hard to value, the honest report is a break-even: the rule is worth it if it prevents more "
            f"than {rows[1]['breakeven_deaths']:.1f} deaths a year. A reader who doubts the epidemiology can then "
            "judge the one number that matters."
        ) as vo:
            self.play(FadeIn(ax), Create(z), FadeIn(labs), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[3]), *[GrowFromEdge(s_[2], UP) for s_ in stacks])
            vo.wait_until("b")
            self.play(FadeIn(side[1]), *[GrowFromEdge(s_[0], DOWN) for s_ in stacks])
            vo.wait_until("c")
            self.play(FadeIn(side[2]), *[FadeIn(s_[1]) for s_ in stacks])
            vo.wait_until("d")
            self.play(FadeIn(nets))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.clear_scene()
