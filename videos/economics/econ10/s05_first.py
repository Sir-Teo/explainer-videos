from __future__ import annotations

from videos.economics.econ10.common import *  # noqa: F403


class FirstDegree(VoiceoverScene):
    def construct(self):
        card(self, 4, r"First-degree discrimination: \ a price for every buyer", r"What if the seller knew what each "
             r"buyer would pay?", "Chapter four. First-degree discrimination: a price for every buyer.")
        self.perfect()
        self.lesson()

    def perfect(self):
        f = load("ferry")
        v = np.array(f["values"])
        ax = plane([0, 100], [0, 10], center=LEFT * 2.8 + DOWN * 0.3, x_length=6.6, y_length=5.0,
                   xticks=[0, 25, 50, 75, 100], yticks=[0, 5, 10], xlabel=r"islanders, \ highest value first",
                   ylabel=r"\$", font_size=17)
        a = ax.ax

        def bars(color, upto=None, height=None):
            g = VGroup()
            for k, x in enumerate(v):
                h = x if height is None else min(x, height)
                g.add(Rectangle(width=0.085, height=max(a.c2p(0, h)[1] - a.c2p(0, 0)[1], 1e-3), stroke_width=0,
                                fill_color=color, fill_opacity=0.85).move_to(a.c2p(k + 0.5, 0), aligned_edge=DOWN))
            return g

        values = bars(DEM)
        one = DashedLine(a.c2p(0, 5), a.c2p(100, 5), color=PROFIT, stroke_width=2)
        paid = bars(PROFIT)
        side = VGroup(
            label(r"one fare of \$5: \ 52 cross, \ Bo takes \$260", font_size=23, color=GREY_A),
            label(r"suppose Bo knew each islander's value, \\ and could stop them reselling tickets", font_size=22),
            label(r"he charges each exactly what crossing is worth to them", font_size=22, color=PROFIT),
            label(rf"everyone crosses; \ Bo takes all \${f['total_value']:.0f}; \ the passengers keep nothing",
                  font_size=22, color=PROFIT),
            label(r"no deadweight loss: \ every crossing worth making is made", font_size=23, color=CS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45)
        tag = island_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Go back to the hundred islanders and their values. <bookmark mark='a'/> With one fare of five dollars, "
            "fifty-two cross and Bo takes two hundred and sixty. <bookmark mark='b'/> Now suppose Bo knew exactly "
            "what each islander would pay, and could stop them reselling tickets to each other. "
            "<bookmark mark='c'/> He would charge each of them exactly their value: nine dollars ninety-one to the most "
            "eager, a few cents to the least. <bookmark mark='d'/> Then everyone crosses, and Bo takes the whole "
            "five hundred and fourteen dollars that the crossings are worth. The passengers keep nothing. "
            "<bookmark mark='e'/> But nothing is wasted either. Every crossing worth making is made, and the "
            "deadweight loss is zero. Perfect discrimination is efficient; it just gives all the gains to the seller."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(values), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(one), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeOut(one), Transform(values, paid), FadeIn(side[2]), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def lesson(self):
        head = label(r"what perfect discrimination needs", font_size=32, color=E.ACCENT).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"to know each buyer's value: \ rarely possible, \ though data are bringing it closer", font_size=25),
            label(r"to stop resale: \ a ticket with a name on it, \ a service that can't be passed on", font_size=25),
            label(r"efficiency and equity part company: \\ the allocation is efficient, \ the surplus all goes to "
                  r"the seller", font_size=25, color=PROFIT),
            label(r"in practice, \ sellers sort buyers into groups, \ or let them sort themselves: \ next", font_size=25,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.42).next_to(head, DOWN, buff=0.6)
        hc = label(r"the classification is A.\ C.\ Pigou's (1920): \ first, \ second and third degree", font_size=21,
                   color=GREY_B).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "So perfect discrimination needs two things. <bookmark mark='a'/> The seller must know each buyer's "
            "value, which is rarely possible, though data are bringing it closer, as the frontier chapter shows. "
            "<bookmark mark='b'/> And buyers must not be able to resell, which is why discounted tickets carry "
            "names. <bookmark mark='c'/> It's a clean case of efficiency and fairness parting company. "
            "<bookmark mark='d'/> In practice sellers do something cruder: they sort buyers into groups they can "
            "see, or design menus that make buyers sort themselves. Arthur Pigou named the three kinds in 1920, "
            "and we take the other two next."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
            self.play(FadeIn(hc))
        self.clear_scene()
