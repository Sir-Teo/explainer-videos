from __future__ import annotations

from videos.economics.econ18.common import *  # noqa: F403


class VSL(VoiceoverScene):
    def construct(self):
        card(self, 11, r"The value of a statistical life", r"How can a regulator put a dollar figure on a risk to life, "
             r"\ and what does the figure mean?", "Chapter eleven. The value of a statistical life.",
             lit={1968: r"Schelling", 1976: r"Thaler and Rosen", 2004: r"Ashenfelter and Greenstone"},
             scale=("person", "nation"), horizon=("a year",))
        self.arithmetic()
        self.sources()
        self.not_it()

    def arithmetic(self):
        v = load("vsl")
        n_side = 100
        grid = VGroup(*[Dot(radius=0.022, color=GREY_C) for _ in range(n_side * n_side)])
        grid.arrange_in_grid(n_side, n_side, buff=0.026).move_to(LEFT * 3.4 + DOWN * 0.3)
        one = grid[n_side * 46 + 61]
        rows = VGroup(
            label(r"Thomas Schelling, \ 1968: \ identified lives and statistical lives", font_size=22),
            label(r"a job carries an extra risk of death of 1 in 10{,}000 a year", font_size=21, color=LIFE),
            label(r"workers take it only for \$1{,}000 a year more", font_size=21, color=MONEY),
            label(r"10{,}000 such workers: \ one extra death expected, \ \$10 million paid", font_size=21,
                  color=WHITE),
            label(rf"value of a statistical life: \ \${v['extra_pay']:,.0f} $\div$ {v['extra_risk']:g} \ = \ "
                  rf"\${v['vsl'] / 1e6:.0f} million".replace(",", "{,}"), font_size=22, color=E.ACCENT),
            label(r"a price on small risks, \ not on anyone's life", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.4)
        tag = published_tag(r"Schelling, ``The Life You Save May Be Your Own'' (1968)", corner=DR, font_size=12)
        with self.voiceover(
            "Every safety rule saves some lives at some cost, so a regulator must decide how much a risk to life "
            "is worth. <bookmark mark='a'/> In 1968 Thomas Schelling separated identified lives, like a miner "
            "trapped underground, whom we will spend almost anything to save, from statistical lives: small risks "
            "spread over many people. <bookmark mark='b'/> Suppose a job carries an extra risk of death of one in "
            "ten thousand a year, <bookmark mark='c'/> and workers take it only if they are paid a thousand dollars "
            "a year more. <bookmark mark='d'/> Among ten thousand such workers, one more death is expected each "
            "year, and ten million dollars in all is paid for accepting it. <bookmark mark='e'/> So the value of a "
            "statistical life is ten million dollars: a thousand dollars divided by one in ten thousand. "
            "<bookmark mark='f'/> It is the rate at which people trade money for small risks, not the price of "
            "anybody's life."
        ) as vo:
            self.play(FadeIn(grid, lag_ratio=0.0005, run_time=2.0), FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
                if mk == "d":
                    self.play(one.animate.set_color(LIFE).scale(5), run_time=1.2)
        self.clear_scene()

    def sources(self):
        t = load("vsl")["table"]
        cards = point_cards([
            (r"wages and risks", r"compare jobs with different \\ fatality rates \ (Thaler and Rosen, \ 1976)",
             MONEY),
            (r"stated preference", r"ask what people would pay \\ for a safer car or route", RULE),
            (r"behaviour", r"speed limits, \ smoke alarms, \\ bicycle helmets", WELF),
        ], width=12.6, cols=3, font_size=21).move_to(UP * 1.6)
        rows = VGroup(
            label(r"Ashenfelter and Greenstone: \ from 1987, \ states could raise rural interstate limits to 65 mph",
                  font_size=21),
            label(r"those that did saw speeds up about 2.5 mph \ (4\%) \ and fatality rates up about 35\%",
                  font_size=21, color=LIFE),
            label(rf"about {t['ag_hours_per_life']:,} hours of travel saved per extra death".replace(",", "{,}"),
                  font_size=21, color=MONEY),
            label(rf"valued at the wage: \ about \${t['ag_1997']:.2f} million per life \ (1997 dollars), \ an upper "
                  rf"bound on what voters were willing to accept", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"Thaler and Rosen (1976); \ Ashenfelter and Greenstone, JPE 112(S1) (2004)", corner=UR,
                            font_size=12)
        with self.voiceover(
            "Where does the number come from? <bookmark mark='a'/> Mostly from wages: comparing jobs with different "
            "risks of death, as Richard Thaler and Sherwin Rosen first did in 1976. Also from surveys that ask what "
            "people would pay for a safer car or route, and from behaviour: speed limits, smoke alarms, helmets. "
            "<bookmark mark='b'/> Orley Ashenfelter and Michael Greenstone used a natural experiment. From 1987, "
            "American states were allowed to raise the speed limit on rural interstates to sixty-five miles an hour. "
            "<bookmark mark='c'/> The states that did saw speeds rise by about two and a half miles an hour, four "
            "percent, and fatality rates by about thirty-five percent. <bookmark mark='d'/> They saved about a "
            "hundred and twenty-five thousand hours of travel for each extra death. <bookmark mark='e'/> Valued at "
            "the wage, that is about one and a half million dollars per life, in 1997 dollars: an upper bound on "
            "the value those states' voters placed on a statistical life."
        ) as vo:
            self.play(FadeIn(cards.cards[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cards.cards[1:]], lag_ratio=0.8),
                      run_time=6)
            for mk, r in zip("bcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def not_it(self):
        rows = VGroup(
            label(r"not the value of a person: \ it prices a small change in risk spread over many", font_size=23),
            label(r"not what you would pay to avoid certain death: \ that is limited by what you have", font_size=23,
                  color=GREY_A),
            label(r"higher where people are richer: \ the same rule can count lives differently by income",
                  font_size=23, color=MONEY),
            label(r"by age? \ in 2003, \ after protests, \ the EPA dropped a lower value for people over seventy",
                  font_size=23, color=LIFE),
            label(r"most agencies use one number for everyone: \ an ethical choice, \ like chapter ten's weights",
                  font_size=23, color=E.ACCENT),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        with self.voiceover(
            "The number is easy to misread. <bookmark mark='a'/> It is not the value of a person. It prices a "
            "small change in risk, spread over many people. <bookmark mark='b'/> Nor is it what anyone would pay to "
            "avoid certain death: that is limited by what they have, and no wage makes certain death acceptable. "
            "<bookmark mark='c'/> It is higher where people are richer, since they can afford to pay more for "
            "safety, so a rule that used each group's own figure would count the lives of the poor for less. "
            "<bookmark mark='d'/> It may vary with age. In 2003, after public protest, the Environmental Protection "
            "Agency stopped using an analysis that put a lower value on the lives of people over seventy. "
            "<bookmark mark='e'/> So most agencies use one number for everyone, whatever their income or age. That "
            "too is an ethical choice, of the same kind as chapter ten's weights: it counts the willingness to pay of "
            "poorer people for more than their own."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
