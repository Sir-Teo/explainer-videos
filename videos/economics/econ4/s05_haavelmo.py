from __future__ import annotations

from videos.economics.econ4.common import *  # noqa: F403


class Haavelmo(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Haavelmo: \ identification", r"When can a system of equations be learned from data at all?",
             "Chapter four. Haavelmo: identification.", scale=("market", "nation"), horizon=("decades",))
        self.probability()
        self.counting()

    def probability(self):
        who = history_card(r"1944", r"Trygve Haavelmo, \emph{The Probability Approach in Econometrics}",
                           r"economic data come from a system of equations with random shocks; ask first which of "
                           r"its parameters the data could ever reveal", color=E.ACCENT, width=7.6, font_size=25)
        who.to_corner(UL, buff=0.5)
        cowles = history_card(r"1940s--50s", r"the Cowles Commission, Chicago",
                              r"Koopmans, Marschak, Klein and others: \ systems of equations, \ the rules of "
                              r"identification, \ early models of whole economies", color=E.WORLD, width=7.0,
                              font_size=23)
        cowles.to_corner(DR, buff=0.5).shift(UP * 0.4)
        nobel = label(r"Nobel prize: \ Haavelmo, 1989", font_size=26, color=E.ACCENT).to_corner(DL, buff=0.6)
        chain = flow_chain([(r"a system of equations with random shocks", E.ACCENT), (r"the data we see", GREY_A),
                            (r"which parameters could the data reveal?", E.ACCENT)], box_w=3.4, box_h=1.2,
                           buff=0.8, font_size=25)
        chain.move_to(DOWN * 0.15)
        with self.voiceover(
            "In 1944 a Norwegian economist, Trygve Haavelmo, turned Working's and Wright's insight into a "
            "programme. <bookmark mark='a'/> Economic data, he argued, are produced by a system of equations, each "
            "with random shocks: demand and supply, consumption and investment. Before estimating anything, ask "
            "which of the system's parameters the data could reveal even in principle. That question has a name: "
            "identification. <bookmark mark='b'/> A group of economists at the Cowles Commission in Chicago worked "
            "out its rules, and built some of the first statistical models of whole economies. <bookmark mark='c'/> "
            "Haavelmo received the Nobel prize for it in 1989."
        ) as vo:
            self.play(FadeIn(who, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(chain.boxes[0]))
            self.play(GrowArrow(chain.arrows[0]), FadeIn(chain.boxes[1]))
            self.play(GrowArrow(chain.arrows[1]), FadeIn(chain.boxes[2]))
            vo.wait_until("b")
            self.play(FadeIn(cowles, shift=LEFT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(nobel))
        self.clear_scene()

    def counting(self):
        eqs = VGroup(
            MathTex(r"\text{demand:}\quad q = a - b\,p + F\cdot\text{feast} + u", font_size=40, color=E.DEMAND),
            MathTex(r"\text{supply:}\quad q = c + d\,p - S\cdot\text{storm} + v", font_size=40, color=E.SUPPLY),
        ).arrange(DOWN, buff=0.4).to_edge(UP, buff=0.6)
        rules = VGroup(
            label(r"the storm is \emph{excluded} from demand: \ so demand is identified", font_size=26, color=E.DEMAND),
            label(r"the feast is \emph{excluded} from supply: \ so supply is identified", font_size=26,
                  color=E.SUPPLY),
            label(r"the order condition: \ an equation needs at least as many variables left out \\ as it has "
                  r"variables determined inside the system, \ less one", font_size=24, color=GREY_A),
            label(r"exclusions are assumptions about the world, \ not facts in the data", font_size=27,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(eqs, DOWN, buff=0.6)
        with self.voiceover(
            "On the Island the rules are easy to see. <bookmark mark='a'/> Write the two curves with everything "
            "that moves them. <bookmark mark='b'/> The storm appears in supply and is left out of demand, so "
            "demand is identified: the storm can trace it. <bookmark mark='c'/> The feast appears in demand and is "
            "left out of supply, so supply is identified. <bookmark mark='d'/> In a bigger system the rule becomes "
            "a count: each equation needs at least as many variables left out of it as it has variables "
            "determined inside the system, less one. <bookmark mark='e'/> But every exclusion is an assumption: "
            "that storms don't change appetite, that feasts don't change the catch. The data can't confirm them. "
            "The argument of the next forty years was about which assumptions to believe."
        ) as vo:
            self.play(Write(eqs[0]))
            vo.wait_until("a")
            self.play(Write(eqs[1]))
            for mk, r in zip("bcde", rules):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
