from __future__ import annotations

from videos.economics.econ19.common import *  # noqa: F403


class Plague(VoiceoverScene):
    def construct(self):
        card(self, 4, r"The Black Death as an experiment", r"What happens to wages when nearly half the workers die?",
             "Chapter four. The Black Death as an experiment.",
             lit={1348: r"the plague reaches England", 1351: r"the Statute of Labourers", 1381: r"the Peasants' Revolt"},
             scale=("nation",), horizon=("a century",))
        self.series()
        self.lessons()

    def series(self):
        b = load("plague")
        t = np.array(b["years"], float)
        top = plane([1300, 1700], [0, 6000], center=UP * 1.35 + LEFT * 0.7, x_length=10.4, y_length=2.3,
                    xticks=[1300, 1400, 1500, 1600, 1700], yticks=[0, 2000, 4000, 6000],
                    ylabel=r"England's population, \ thousands", xfmt=lambda v: f"{v:.0f}",
                    yfmt=lambda v: f"{v:,.0f}".replace(",", "{,}"), font_size=16)
        bot = plane([1300, 1700], [0, 80], center=DOWN * 1.85 + LEFT * 0.7, x_length=10.4, y_length=2.3,
                    xticks=[1300, 1400, 1500, 1600, 1700], yticks=[0, 20, 40, 60, 80],
                    ylabel=r"real wages, \ 1900 = 100", xfmt=lambda v: f"{v:.0f}", font_size=16)
        cp = path(top, t, b["pop"], color=POP, width=3.5, smooth=False)
        cw = path(bot, t, b["wage"], color=WAGE, width=3.5, smooth=False)
        band = VGroup(*[Rectangle(width=max(abs(a.ax.c2p(1351, 0)[0] - a.ax.c2p(1348, 0)[0]), 0.06), height=2.3,
                                  stroke_width=0, fill_color=DEATH, fill_opacity=0.3).move_to(
            [(a.ax.c2p(1348, 0)[0] + a.ax.c2p(1351, 0)[0]) / 2, a.ax.get_center()[1], 0]) for a in (top, bot)])
        k = b["key"]
        n1 = label(rf"1348--51: \ {k['1348']['pop'] / 1000:.1f} \ million \ $\to$ \ {k['1351']['pop'] / 1000:.1f}: \ "
                   rf"{100 * b['drop']:.0f}\% die", font_size=19, color=POP).move_to(top.ax.c2p(1490, 5300))
        n2 = label(rf"real wages: \ $\times${b['wage_x_1400']:.1f} by 1400, \ $\times${b['wage_x_1450']:.1f} by 1450",
                   font_size=19, color=WAGE).move_to(bot.ax.c2p(1610, 70))
        n3 = label(rf"by 1650: \ {k['1650']['pop'] / 1000:.1f} \ million, \ and wages back to {k['1650']['wage']:.0f}",
                   font_size=19, color=GREY_A).move_to(bot.ax.c2p(1560, 14))
        src = data_tag(data.cite("millennium"), corner=DR, font_size=12)
        with self.voiceover(
            "In the summer of 1348 the plague reached England. <bookmark mark='a'/> Within three years, by the "
            f"estimates in the Bank of England's dataset, the population fell from about {k['1348']['pop'] / 1000:.1f} "
            f"million to {k['1351']['pop'] / 1000:.1f} million: {100 * b['drop']:.0f} percent of the people died. "
            "Later outbreaks kept it falling for a century. <bookmark mark='b'/> Nothing else had changed: the land, "
            "the tools, the crops. So Malthus's model makes a sharp prediction, and it came true. Real wages rose to "
            f"about {b['wage_x_1400']:.1f} times their level of 1348 by 1400, and {b['wage_x_1450']:.1f} times by 1450. "
            "<bookmark mark='c'/> Then the reversal. As the population recovered, reaching about "
            f"{k['1650']['pop'] / 1000:.1f} million by 1650, wages fell back to where they had been before the plague. "
            "The mechanism ran backwards and then forwards again, over three centuries."
        ) as vo:
            self.play(FadeIn(top), FadeIn(bot), FadeIn(src), FadeIn(band))
            vo.wait_until("a")
            self.play(Create(cp), run_time=3, rate_func=linear)
            self.play(FadeIn(n1))
            vo.wait_until("b")
            self.play(Create(cw), run_time=3, rate_func=linear)
            self.play(FadeIn(n2))
            vo.wait_until("c")
            self.play(FadeIn(n3))
        self.clear_scene()

    def lessons(self):
        rows = VGroup(
            label(r"landlords and employers fought it: \ the Statute of Labourers, \ 1351, \ capped wages", font_size=23),
            label(r"the cap failed; \ in 1381 the Peasants' Revolt", font_size=23, color=DEATH),
            label(r"a fifteenth-century golden age of labour: \ meat, \ ale, \ better clothes", font_size=23,
                  color=WAGE),
            label(r"in north-western Europe the gain partly stuck: \ more towns, \ later marriage, \ higher wages",
                  font_size=22, color=GDP),
            label(r"Voigtländer and Voth, \ 2013: \ plague, \ war and towns kept Europe richer than its technology",
                  font_size=21, color=TECH),
            label(r"but not out of the trap: \ by 1650 English wages were back to about their level of 1300", font_size=22,
                  color=HOLD),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        tag = published_tag(r"Voigtländer and Voth, RES 80(2) (2013)", corner=DR, font_size=13)
        with self.voiceover(
            "The plague also showed who gained and who resisted. <bookmark mark='a'/> Landlords and employers tried "
            "to hold wages down by law: the Statute of Labourers of 1351 capped them at their old levels. "
            "<bookmark mark='b'/> The cap failed, and in 1381 the Peasants' Revolt rose partly against such rules. "
            "<bookmark mark='c'/> For the survivors, the fifteenth century was a golden age of labour, with more "
            "meat, more ale and better clothes. <bookmark mark='d'/> In north-western Europe part of the gain stuck: "
            "more people lived in towns, married later, and kept wages higher. <bookmark mark='e'/> Nico Voigtländer "
            "and Joachim Voth argued that plague, war and towns, the three horsemen of riches, kept Europe richer "
            "than its technology alone would allow. <bookmark mark='f'/> But not out of the trap. By 1650, English "
            "wages were back to about their level of 1300."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
