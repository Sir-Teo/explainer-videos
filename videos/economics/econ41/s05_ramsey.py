from __future__ import annotations

from videos.economics.econ41.common import *  # noqa: F403


class Ramsey(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Taxing goods: \ Ramsey's rule", r"Which goods should carry the most tax?",
             "Chapter four. Taxing goods: Ramsey's rule.", lit={1927: r"Ramsey", 1971: r"Diamond and Mirrlees",
                                                                1976: r"Atkinson and Stiglitz"},
             scale=("household", "nation"), horizon=("a year",))
        self.rule()
        self.compare()
        self.limits()

    def rule(self):
        R = load("ramsey")
        hc = history_card(1927, r"Frank Ramsey", r"takes up Arthur Pigou's question, \ how to raise a given revenue by "
                          r"taxing goods at the least cost: \ cut the demand for every good by the same proportion",
                          color=E.ACCENT, width=10.4, font_size=24).to_edge(UP, buff=0.5)
        eq = MathTex(r"\frac{t_i}{1 + t_i} = \frac{k}{\varepsilon_i}", font_size=44).next_to(hc, DOWN, buff=0.5)
        rows = VGroup(*[label(rf"{g}: \ demand elasticity {e:g} \ $\Rightarrow$ \ tax {100 * t:.1f}\%", font_size=22,
                              color=c) for g, e, t, c in zip(R["goods"], R["eps"], R["ramsey"], GOODS)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(eq, DOWN, buff=0.5)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Now the theory of taxing well. In 1927 Frank Ramsey, a Cambridge mathematician in his twenties, took up "
            "a question Arthur Pigou had put to him: how to raise a given revenue from taxes on goods at the least "
            "cost. <bookmark mark='a'/> Ramsey's "
            "answer: set the taxes so that the demand for every good falls by the same proportion. When the goods "
            "are independent, that means each tax, as a share of the price, is inversely proportional to the good's "
            "elasticity of demand. <bookmark mark='b'/> On the Island: bread, whose demand barely responds, "
            f"carries {100 * R['ramsey'][0]:.0f} percent; <bookmark mark='c'/> clothes, "
            f"{100 * R['ramsey'][1]:.1f}; <bookmark mark='d'/> travel, whose demand is elastic, "
            f"{100 * R['ramsey'][2]:.1f}. Tax what people cannot avoid buying, because that changes behaviour least."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.1), FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(eq))
            for mk, r_ in zip("bcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def compare(self):
        R = load("ramsey")
        bars = VGroup()
        scale = 160.0
        for k, (g, dr, du, c) in enumerate(zip(R["goods"], R["dwl_ramsey"], R["dwl_uniform"], GOODS)):
            y = 1.3 - 1.25 * k
            ru = Rectangle(width=max(du * scale, 0.02), height=0.35, stroke_width=0, fill_color=GREY_B,
                           fill_opacity=0.8).move_to(np.array([-1.0 + du * scale / 2, y + 0.22, 0]))
            rr = Rectangle(width=max(dr * scale, 0.02), height=0.35, stroke_width=0, fill_color=c,
                           fill_opacity=0.9).move_to(np.array([-1.0 + dr * scale / 2, y - 0.22, 0]))
            bars.add(VGroup(label(g, font_size=22, color=c).next_to(np.array([-1.1, y, 0]), LEFT, buff=0.2), ru,
                            label(f"{du:.4f}", font_size=16, color=GREY_A).next_to(ru, RIGHT, buff=0.1), rr,
                            label(f"{dr:.4f}", font_size=16, color=c).next_to(rr, RIGHT, buff=0.1)))
        head = label(rf"the same revenue, \ {R['revenue']:g}: \ deadweight loss by good", font_size=26,
                     color=E.ACCENT).to_edge(UP, buff=0.5)
        keys = label(rf"grey: \ one uniform rate, \ {100 * R['uniform']:.1f}\% on everything; \ colour: \ Ramsey's "
                     r"rates", font_size=19, color=GREY_A).next_to(head, DOWN, buff=0.2)
        total = label(rf"total loss: \ uniform {R['total_uniform']:.4f}, \ Ramsey {R['total_ramsey']:.4f}, \ "
                      rf"{R['total_uniform'] / R['total_ramsey']:.1f} times smaller", font_size=22,
                      color=GAIN).to_edge(DOWN, buff=0.7)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "How much does it matter? Raise the same revenue two ways. <bookmark mark='a'/> With one uniform rate, "
            f"{100 * R['uniform']:.1f} percent on everything, most of the loss comes from travel, whose buyers flee "
            "the tax. <bookmark mark='b'/> With Ramsey's rates, the loss on travel and clothes nearly vanishes, and "
            "bread's rises only a little. <bookmark mark='c'/> In total, Ramsey's taxes cost "
            f"{R['total_uniform'] / R['total_ramsey']:.1f} times less for the same revenue."
        ) as vo:
            self.play(FadeIn(head), FadeIn(keys), FadeIn(tag), *[FadeIn(b_[0]) for b_ in bars])
            vo.wait_until("a")
            self.play(*[GrowFromEdge(b_[1], LEFT) for b_ in bars], *[FadeIn(b_[2]) for b_ in bars])
            vo.wait_until("b")
            self.play(*[GrowFromEdge(b_[3], LEFT) for b_ in bars], *[FadeIn(b_[4]) for b_ in bars])
            vo.wait_until("c")
            self.play(FadeIn(total))
        self.clear_scene()

    def limits(self):
        cards = point_cards([
            (r"equity", r"inelastic goods \\ are often necessities: \\ the rule taxes \\ the poor hardest", LOSS),
            (r"Diamond and Mirrlees", r"do not tax the inputs \\ firms buy from \\ each other: \ keep \\ production "
                                      r"efficient", THEORY),
            (r"Atkinson and Stiglitz", r"with a good income tax \\ and separable tastes, \\ tax all goods \\ alike",
             TOP),
            (r"in practice", r"broad value-added \\ taxes with few \\ exemptions", GAIN),
        ], width=12.8, cols=4, font_size=19).move_to(DOWN * 0.1)
        head = label(r"what Ramsey's rule leaves out", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.RAMSEY_1927.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Ramsey's rule is about efficiency only. <bookmark mark='a'/> The goods with the least elastic demand "
            "are often necessities, so the rule taxes the poor hardest. <bookmark mark='b'/> In 1971 Peter Diamond "
            "and James Mirrlees showed that an optimal system keeps production efficient: it should not tax the "
            "goods firms sell to each other, only what households finally buy. <bookmark mark='c'/> And in 1976 "
            "Anthony Atkinson and Joseph Stiglitz showed that if the income tax is well designed and tastes for "
            "goods do not depend on how hard one works, differential taxes on goods add nothing: redistribute "
            "through the income tax. <bookmark mark='d'/> That is roughly where practice has landed: broad value-"
            "added taxes on final consumption, with few exemptions."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
