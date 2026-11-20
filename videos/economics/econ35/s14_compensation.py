from __future__ import annotations

from videos.economics.econ35.common import *  # noqa: F403


class Compensation(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Compensation", r"Could the winners pay the losers, and do they?",
             "Chapter twelve. Compensation.", lit={1939: r"Kaldor; \ Hicks", 1962: r"trade adjustment assistance"},
             scale=("household", "nation"), horizon=("a year", "a decade"))
        self.opening()
        self.ought()
        self.record()

    def opening(self):
        C = load("compensation")
        groups = (("workers", LABOUR), ("capital", CAPITAL), ("land", LAND))
        ax = plane([0.4, 3.6], [-30, 30], center=LEFT * 2.0 + DOWN * 0.4, x_length=7.0, y_length=4.6, xticks=[],
                   yticks=[-30, -15, 0, 15, 30], ylabel=r"change in real income", yfmt=lambda v: f"{v:+.0f}\\%" if v
                   else "0", font_size=14)
        zero = seg(ax, 0.4, 0, 3.6, 0, GREY_B, 1.5)
        bars, labs = VGroup(), VGroup()
        for k, (g, col) in enumerate(groups):
            v = 100 * C["real"][g]
            p0, p1 = ax.ax.c2p(k + 0.65, 0), ax.ax.c2p(k + 1.35, v)
            bars.add(Rectangle(width=p1[0] - p0[0], height=max(abs(p1[1] - p0[1]), 0.02), fill_color=col,
                               fill_opacity=0.85, stroke_width=0).move_to((p0 + p1) / 2))
            labs.add(VGroup(label(g, font_size=17, color=col), label(f"{v:+.0f}\\%", font_size=18, color=WHITE))
                     .arrange(DOWN, buff=0.05).next_to(bars[-1], UP if v >= 0 else DOWN, buff=0.08))
        side = VGroup(
            label(rf"the Island opens; \\ food falls {100 * C['food_fall']:.0f}\%", font_size=19, color=WHITE),
            label(rf"winners gain {C['winners']:.1f}; \\ losers lose {C['losers']:.1f}", font_size=19, color=GAIN),
            label(rf"the difference, \ {C['total']:.1f}, \\ is the gain from trade", font_size=19, color=E.ACCENT),
            label(r"so the winners \\ could pay the losers \\ and still be ahead", font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Go back to the specific-factors Island and open it to the world, so that imported food is twenty "
            "percent cheaper. <bookmark mark='a'/> In real terms, landowners lose about a fifth of their income. "
            "Factory owners gain about a quarter, and workers a little. <bookmark mark='b'/> Add it up in money: "
            f"the winners gain {C['winners']:.1f}, the losers lose {C['losers']:.1f}. "
            f"<bookmark mark='c'/> The difference, {C['total']:.1f}, is the Island's gain from trade, and it is "
            "positive, as it must be: the economy can now consume a bundle it could not make. "
            "<bookmark mark='d'/> So the winners could compensate the losers in full and still be better off. In "
            "1939 Nicholas Kaldor and John Hicks proposed that test as the meaning of an efficient change."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN if C["real"][g] >= 0 else UP)
                                    for b, (g, _) in zip(bars, groups)], lag_ratio=0.3), FadeIn(labs), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def ought(self):
        io = is_ought_card(r"Opening to trade raises the Island's income: the winners could compensate the losers "
                           r"and still be better off.",
                           r"The Island should open to trade.",
                           r"That a gain that could be shared is enough, whether or not it is; or that the losers "
                           r"will in fact be compensated, or that their loss weighs no more than others' gain.",
                           width=12.0, font_size=23).move_to(UP * 0.2)
        tag = published_tag(r"Kaldor, \ \emph{EJ} 49 (1939); \ Hicks, \ \emph{EJ} 49 (1939); \ Part 18", corner=DR,
                            font_size=12)
        with self.voiceover(
            "But could is not would. <bookmark mark='a'/> What economics shows is that opening to trade raises "
            "total income, so the winners could compensate the losers and still be ahead. "
            "<bookmark mark='b'/> The step to saying the Island should open needs a value judgment: either that a "
            "gain that could be shared is enough, whether or not it is; or that the losers will in fact be "
            "compensated; or that their loss weighs no more than someone else's gain. Part eighteen showed that "
            "economics cannot make that choice for us. <bookmark mark='c'/> It can tell us whether compensation "
            "happens."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(io.card))
            vo.wait_until("a")
            self.play(FadeIn(io.is_row))
            vo.wait_until("b")
            self.play(FadeIn(io.judgment), FadeIn(io.ought))
            vo.wait_until("c")
            self.play(Indicate(io.judgment, color=E.OUGHT, scale_factor=1.02))
        self.clear_scene()

    def record(self):
        C = load("compensation")
        rows = VGroup(
            label(r"trade adjustment assistance, \ America", font_size=28, color=E.ACCENT),
            label(rf"created by the Trade Expansion Act, \ {C['taa_enacted']}: \ retraining, \ allowances, \ "
                  r"longer benefits", font_size=21, color=WHITE),
            label(r"small and uneven: \ many displaced workers never apply", font_size=22, color=GREY_A),
            label(rf"Hyman (2018): \ approved workers earned about \${C['taa_hyman_gain']:,.0f} more \ over "
                  rf"{C['taa_hyman_years']} years", font_size=22, color=GAIN),
            label(r"the large losses from the China shock \ (Part 36) \ were mostly not compensated", font_size=22,
                  color=TARIFF),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Public Law 87-794 (1962); \ CRS R41922; \ Hyman (2018)", corner=DR, font_size=12)
        with self.voiceover(
            "America has tried. <bookmark mark='a'/> In 1962, in the same law that launched a round of tariff "
            "cuts, Congress created trade adjustment assistance: retraining, relocation allowances and longer "
            "unemployment benefits for workers who lose their jobs to imports. <bookmark mark='b'/> It has always "
            "been small, and many eligible workers never apply. <bookmark mark='c'/> Where it reaches people it "
            "seems to work: Benjamin Hyman, comparing workers whose cases happened to go to stricter or more "
            f"lenient investigators, found that approved workers earned about {C['taa_hyman_gain']:,.0f} dollars "
            f"more over the next {C['taa_hyman_years']} years. <bookmark mark='d'/> But the biggest trade shock "
            "of recent times, the surge of imports from China after 2000, fell on particular towns, and most of "
            "its losers were never compensated. That is where Part thirty-six begins."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
