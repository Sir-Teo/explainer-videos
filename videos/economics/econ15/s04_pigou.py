from __future__ import annotations

from videos.economics.econ15.common import *  # noqa: F403


class Pigou(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Pigou's tax", r"What price should a spillover carry, \ and is the right amount of smoke zero?",
             "Chapter three. Pigou's tax.", lit={1920: r"Pigou"},
             scale=("market", "nation"), horizon=("a year",))
        self.tax()
        self.notzero()
        self.positive()

    def tax(self):
        k = load("kiln")
        qs = np.array(k["qs"])
        ax = plane([0, 70], [0, 110], center=LEFT * 2.7 + DOWN * 0.3, x_length=6.6, y_length=4.8,
                   xticks=[0, 20, 36, 45, 60], yticks=[0, 25, 50, 75, 100], xlabel=r"pots a season",
                   ylabel=r"shells a pot", font_size=16, xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}")
        a = ax.ax
        dem = path(ax, qs, k["demand"], color=DEMAND, width=3.5, smooth=False, yr=(0, 110))
        pri = path(ax, qs, k["private"], color=PRIVATE, width=3, smooth=False, yr=(0, 110))
        soc = path(ax, qs, k["social"], color=SOCIAL, width=2.5, smooth=False, yr=(0, 110))
        taxed = path(ax, qs, np.array(k["private"]) + k["tax"], color=GOOD, width=3.5, smooth=False, yr=(0, 110))
        lt = label(rf"green: \ Bo's cost $+$ a tax of {k['tax']:.0f}", font_size=15, color=GOOD).move_to(
            a.c2p(14, 64))
        arrow = Arrow(a.c2p(60, k["c"] + k["e"] * 60), a.c2p(60, k["c"] + k["e"] * 60 + k["tax"]), buff=0.05,
                      color=GOOD, stroke_width=3, tip_length=0.15)
        qs_ = k["q_social"]
        dot = Dot(a.c2p(qs_, k["p_social"]), radius=0.09, color=GOOD)
        rev = Rectangle(width=a.c2p(qs_, 0)[0] - a.c2p(0, 0)[0], height=a.c2p(0, k["tax"])[1] - a.c2p(0, 0)[1],
                        stroke_width=0, fill_color=GOOD, fill_opacity=0.18).move_to(a.c2p(0, 0), aligned_edge=DL)
        side = VGroup(
            label(r"Arthur Pigou, \ 1920: \ charge the maker \\ the damage of one more unit", font_size=21),
            label(rf"at the best output, \ {qs_:.0f} pots, \\ one more pot spoils {k['tax']:.0f} shells of fish",
                  font_size=21, color=SOCIAL),
            label(rf"tax each pot {k['tax']:.0f} shells, \\ and Bo stops at {k['q_with_tax']:.0f} by himself",
                  font_size=21, color=GOOD),
            label(rf"the tax raises {k['tax'] * qs_:.0f} shells a season: \\ the green rectangle", font_size=21,
                  color=GOOD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Pigou, The Economics of Welfare (1920); \ the numbers: \ Agora", corner=DR, font_size=13)
        with self.voiceover(
            "The first remedy is a price. <bookmark mark='a'/> In 1920 Arthur Pigou, in Cambridge, proposed charging "
            "the maker of a spillover the damage done by one more unit of it. <bookmark mark='b'/> At the best "
            "output, thirty-six pots, one more pot spoils eighteen shells' worth of Ana's fish. "
            "<bookmark mark='c'/> So tax each pot eighteen shells. Bo's cost now includes the damage, and he stops at "
            "thirty-six pots by himself. Nobody has to tell him how many to make, or how to make them. "
            "<bookmark mark='d'/> The tax also raises money, about six hundred and fifty shells a season, which the "
            "village can spend, or hand back, without changing what Bo does."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(dem), Create(pri), Create(soc), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), Indicate(soc, color=SOCIAL))
            vo.wait_until("c")
            self.play(GrowArrow(arrow), Create(taxed), FadeIn(lt), FadeIn(side[2]), run_time=2)
            self.play(FadeIn(dot, scale=1.5))
            vo.wait_until("d")
            self.play(FadeIn(rev), FadeIn(side[3]))
        self.clear_scene()

    def notzero(self):
        k = load("kiln")
        rows = VGroup(
            label(rf"with the tax, \ Bo still fires {k['q_social']:.0f} pots, \ and still spoils some of Ana's fish",
                  font_size=24),
            label(rf"the damage that remains: \ {k['damage_social']:.0f} shells' worth a season, \ down from "
                  rf"{k['damage_market']:.0f}", font_size=24, color=SMOKE),
            label(r"the right amount of smoke is not zero: \ the last pots are worth more than the fish they spoil",
                  font_size=24, color=E.ACCENT),
            label(r"the tax charges the damage at the margin, \ not the total: \ the price of one more pot's smoke",
                  font_size=23, color=GREY_A),
            label(r"and Bo can cut the damage any way he likes: \ a taller chimney, \ better wood, \ fewer pots",
                  font_size=23, color=GOOD),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Notice what the tax does not do. <bookmark mark='a'/> With it, Bo still fires thirty-six pots, and still "
            "spoils some of Ana's fish. <bookmark mark='b'/> The damage that remains is worth about three hundred and "
            "twenty shells a season, down from five hundred. <bookmark mark='c'/> The right amount of smoke is not "
            "zero. Banning the kiln would lose pots that are worth far more than the fish they spoil. "
            "<bookmark mark='d'/> The tax charges the damage at the margin, the cost of one more pot's smoke, not the "
            "total. <bookmark mark='e'/> And it leaves Bo free to cut the damage in whatever way is cheapest for him: "
            "a taller chimney, drier wood, or fewer pots. A rule that dictated the chimney could not do that."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def positive(self):
        rows = VGroup(
            label(r"a positive spillover works the same way, \ with the sign reversed", font_size=25, color=GOOD),
            label(r"pay the maker the benefit of one more unit to others: \ a Pigouvian subsidy", font_size=24),
            label(r"vaccination subsidies, \ research grants and tax credits, \ grants for planting trees",
                  font_size=24, color=GOOD),
            label(r"the hard part is not the theory: \ it is measuring the damage, \ or the benefit", font_size=24,
                  color=E.ACCENT),
            label(r"chapter fifteen comes back to how that is done", font_size=23, color=GREY_A),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        with self.voiceover(
            "The same logic runs the other way. <bookmark mark='a'/> When a choice benefits others, the remedy is a "
            "subsidy: <bookmark mark='b'/> pay the maker what one more unit is worth to everyone else. "
            "<bookmark mark='c'/> Subsidies for vaccination, grants and tax credits for research, payments for "
            "planting trees: all are Pigou's idea at work. <bookmark mark='d'/> The theory is the easy part. The hard "
            "part is putting a number on the damage, or the benefit, at the margin. <bookmark mark='e'/> Chapter "
            "fifteen comes back to how economists do that."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
