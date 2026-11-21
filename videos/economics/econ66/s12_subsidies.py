from __future__ import annotations

from videos.economics.econ66.common import *  # noqa: F403


class Subsidies(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Chips, \ batteries and solar: \ subsidy races", r"When every large economy subsidizes the "
             r"same industries, \ who gains?", "Chapter ten. Chips, batteries and solar: subsidy races.",
             lit={1985: "Brander and Spencer", 2022: "the CHIPS Act"}, scale=("nation", "world"),
             horizon=("a decade",))
        self.race()
        self.today()
        self.china()

    def race(self):
        Bs = load("subsidies")
        ax = plane([-0.6, 2.6], [0, 28], center=LEFT * 2.2 + DOWN * 0.4, x_length=7.0, y_length=4.8, xticks=[],
                   yticks=[0, 5, 10, 15, 20, 25], ylabel=r"welfare", yfmt=lambda v: f"{v:.0f}", font_size=14)
        groups = VGroup()
        for k, key in enumerate(("none", "one", "both")):
            o = Bs[key]
            groups.add(bars(ax, [k - 0.25, k, k + 0.25], [o["w1"], o["w2"], o["consumers"]], [US, ROW, PRICE],
                            width=0.24))
        names = VGroup(*[label(t, font_size=15, color=GREY_A).next_to(ax.ax.c2p(k, 0), DOWN, buff=0.15)
                         for k, t in enumerate((r"no subsidies", r"only country 1", r"both"))])
        key = legend_rows([(US, "country 1: its firm's profit less the subsidy"), (ROW, "country 2: the same"),
                           (PRICE, "buyers in the third market")], font_size=15).next_to(ax.ax, RIGHT, buff=0.35)
        key.shift(UP * 1.3)
        side = VGroup(
            label(rf"one subsidizes: \ $s = (a-c)/4$; \ country 1 gains {Bs['one']['w1'] - Bs['none']['w1']:.2f}",
                  font_size=17, color=US),
            label(rf"both: \ $s = (a-c)/5$ each; \ each loses {Bs['none']['w1'] - Bs['both']['w1']:.2f}",
                  font_size=17, color=TARIFF),
            label(r"the third market's buyers gain", font_size=17, color=PRICE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(key, DOWN, buff=0.45).align_to(key, LEFT)
        tag = published_tag(r"Brander and Spencer, \ JIE 18(1--2) (1985); \ agora.tradewar.brander\_spencer",
                            corner=DL, font_size=12)
        with self.voiceover(
            "James Brander and Barbara Spencer gave the strategic case for subsidies in 1985. <bookmark mark='a'/> "
            "Two firms, one from each country, compete in quantities to sell to a third market. With no subsidies, "
            "they split the market. <bookmark mark='b'/> Now country one subsidizes its firm's output. The firm "
            "becomes more aggressive, its rival retreats, and country one's welfare, its firm's profit minus the "
            "subsidy bill, rises: the subsidy shifts profit from the foreign firm to the domestic one. <bookmark "
            "mark='c'/> But country two can do the same. When both subsidize, at the Nash subsidies, both firms "
            "produce more, the price falls, and both countries are worse off than with no subsidies at all. The "
            "winners are the buyers in the third market. Another prisoners' dilemma."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(names), FadeIn(key), FadeIn(tag))
            for mk, k in zip("abc", range(3)):
                vo.wait_until(mk)
                self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in groups[k]], lag_ratio=0.2),
                          *([FadeIn(side[k - 1])] if k > 0 else []), run_time=1.4)
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def today(self):
        cards = point_cards([
            (r"chips", r"America's CHIPS and Science Act (2022): \ \$52.7 billion, \ most of it for factories; "
             r"\ Europe, \ Japan, \ Korea and China with their own", STATE),
            (r"clean energy", r"tax credits for batteries, \ solar and electric cars \ (the Inflation Reduction "
             r"Act, \ 2022), \ answered by subsidies elsewhere", FREE),
            (r"the case", r"security of supply, \ learning that spills over, \ and climate: \ an externality "
             r"(Part 48) a subsidy can address", US),
            (r"the risk", r"Brander and Spencer's race: \ each country pays to win business the others also pay "
             r"for; \ buyers elsewhere gain", TARIFF),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.2)
        head = label(r"the subsidy race of the 2020s", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "The 2020s brought the race to life. <bookmark mark='a'/> America's CHIPS and Science Act of 2022 "
            "provided fifty-two point seven billion dollars, most of it for chip factories; Europe, Japan, Korea "
            "and China have programmes of their own. <bookmark mark='b'/> The Inflation Reduction Act of the same "
            "year gave tax credits for batteries, solar panels and electric cars, and others answered. <bookmark "
            "mark='c'/> The best case: security of supply, learning that spills over, and for clean energy an "
            "externality, the climate of Part forty-eight, that a subsidy can correct. <bookmark mark='d'/> The "
            "risk is Brander and Spencer's race: each country pays to win business the others are also paying "
            "for, and the gains leak to buyers abroad."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def china(self):
        cards = point_cards([
            (r"the model", r"state banks, \ local governments and targets: \ capital steered to chosen "
             r"industries, \ on a continental scale", STATE),
            (r"the result", r"more than 80\% of the world's capacity at every stage of making solar panels; \ "
             r"leadership in batteries and electric cars", ROW),
            (r"overcapacity?", r"to its trading partners, \ capacity built by subsidy and sold abroad below cost; "
             r"\ to China, \ scale and learning", PRICE),
            (r"the second China shock", r"Part 36's shock, \ now in industries rich countries chose to "
             r"subsidize themselves: \ the subsidy race, \ at full speed", TARIFF),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.2)
        head = label(r"China's model, \ and the debate over it", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"International Energy Agency, \ \emph{Solar PV Global Supply Chains} (2022); \ Part 36",
                            corner=DL, font_size=12)
        with self.voiceover(
            "The largest industrial policy of all is China's. <bookmark mark='a'/> State banks, local governments "
            "and national targets steer capital into chosen industries, at a continental scale. <bookmark "
            "mark='b'/> The International Energy Agency counted more than eighty percent of the world's capacity "
            "at every stage of making solar panels in China, and China leads in batteries and electric cars. "
            "<bookmark mark='c'/> Its trading partners call this overcapacity: capacity built by subsidy, sold "
            "abroad at prices that would not cover costs without it. China's answer is scale and learning, the "
            "economics of chapter eight. <bookmark mark='d'/> Either way, it brings a second China shock, this time "
            "in the industries that rich countries have chosen to subsidize themselves. The subsidy race, at full "
            "speed, and with Part thirty-six's lesson attached: the losses fall on particular places."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
