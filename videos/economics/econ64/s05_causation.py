from __future__ import annotations

from videos.economics.econ64.common import *  # noqa: F403

RULES = (("at random", GREY_B), ("highest risk", NAIVE), ("largest effect (estimated)", ALGO),
         ("largest effect (truth)", TRUTHC))


class Causation(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Prediction is not causation", r"Should a programme go to the people most at risk?",
             "Chapter four. Prediction is not causation.", lit={2019: r"Obermeyer et al."},
             scale=("person", "nation"), horizon=("a year",))
        self.hump()
        self.targets()
        self.proxy()

    def hump(self):
        T = load("targeting")
        x, e = np.array(T["risk_bins"]), np.array(T["effect_by_risk"])
        ax = plane([0, 1], [0, 0.35], center=LEFT * 2.4 + DOWN * 0.3, x_length=6.6, y_length=4.6,
                   xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[0, 0.1, 0.2, 0.3],
                   xlabel=r"chance of still being out of work in a year, \ without the programme",
                   ylabel=r"the programme's effect on that chance", xfmt=lambda v: f"{v:.2f}",
                   yfmt=lambda v: f"{v:.1f}", font_size=14)
        b = bars(ax, x, e, [TRUTHC] * len(x), width=0.08)
        side = VGroup(
            label(r"the Island's job programme: \ places for a fifth \\ of the unemployed", font_size=20,
                  color=WHITE),
            label(r"those likely to find work anyway \\ gain little", font_size=20, color=GREY_A),
            label(r"those far from any job \\ gain little too", font_size=20, color=GREY_A),
            label(r"the most at risk are not \\ the most helped", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.5)
        tag = island_tag(r"the Island: \ effects planted; \ agora.learn.targeting", corner=DL, font_size=12)
        with self.voiceover(
            "Prediction is the right tool when the decision does not change the outcome. Most policies are meant "
            "to change it. <bookmark mark='a'/> The Island has a job programme with places for a fifth of its "
            "unemployed. Who should get them? A natural answer: predict who is most likely to stay out of work, and "
            "start there. <bookmark mark='b'/> But look at the programme's effect, which the Island knows, by "
            "risk. People likely to find work anyway gain little. <bookmark mark='c'/> And people far from any job "
            "gain little too: a few weeks of training do not bridge that distance. <bookmark mark='d'/> The effect "
            "is largest in the middle. The most at risk are not the most helped."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(*[GrowFromEdge(r, DOWN) for r in b], FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def targets(self):
        T = load("targeting")
        P = T["per100"]
        vals = [P[k] for k, _ in RULES]
        ax = plane([-0.6, 3.6], [0, 35], center=LEFT * 2.6 + DOWN * 0.3, x_length=6.4, y_length=4.6, xticks=[],
                   yticks=[0, 10, 20, 30], ylabel=r"people kept out of unemployment, \ per 100 places",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        b = bars(ax, range(4), vals, [c for _, c in RULES], width=0.55)
        names = (r"at random", r"highest \\ risk", r"largest effect, \\ estimated", r"largest effect, \\ true")
        labs = VGroup(*[label(n, font_size=14, color=c).next_to(ax.ax.c2p(k, 0), DOWN, buff=0.12)
                        for k, (n, (_, c)) in enumerate(zip(names, RULES))])
        vl = VGroup(*[label(f"{v:.0f}", font_size=15, color=c).next_to(x, UP, buff=0.06)
                      for v, (_, c), x in zip(vals, RULES, b)])
        side = VGroup(
            label(rf"by risk: \ {vals[1]:.0f} per 100, \ worse than at random", font_size=20, color=NAIVE),
            label(rf"by an estimated effect: \ {vals[2]:.0f} \\ (a causal forest on a trial of "
                  rf"{T['trial']:,} people)".replace(",", "{,}"), font_size=20, color=ALGO),
            label(rf"the best possible: \ {vals[3]:.0f}", font_size=20, color=TRUTHC),
            label(r"targeting needs effects, \\ and effects need experiments", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).to_edge(RIGHT, buff=0.4)
        tag = island_tag(r"the Island: \ 20,000 unemployed; \ agora.learn.targeting".replace(",", "{,}"), corner=DL,
                         font_size=12)
        with self.voiceover(
            "Now give out the places four ways and count the people kept out of unemployment per hundred places. "
            f"<bookmark mark='a'/> At random: {vals[0]:.0f}. <bookmark mark='b'/> To the highest predicted risk: "
            f"{vals[1]:.0f}, worse than at random. <bookmark mark='c'/> To the people with the largest effect, as "
            "estimated by a causal forest from a randomized trial: "
            f"{vals[2]:.0f}. <bookmark mark='d'/> And to the largest true effect, which no one ever knows: "
            f"{vals[3]:.0f}. <bookmark mark='e'/> A perfect forecast of who will stay unemployed would not help "
            "here. Targeting needs effects, and effects need experiments, which chapter six returns to."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(labs), FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(GrowFromEdge(b[k], DOWN), FadeIn(vl[k]))
                if k:
                    self.play(FadeIn(side[k - 1]), run_time=0.6)
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def proxy(self):
        hc = VGroup(
            history_card(2019, r"a health system's algorithm", r"trained to predict each patient's future medical "
                         r"costs, \ and used to pick who gets extra care", color=ALGO, width=11.2, font_size=21),
            history_card(r"the catch", r"costs are not needs", r"less is spent on Black patients with the same "
                         r"illness, \ so at the same score they were sicker", color=NAIVE, width=11.2, font_size=21),
            history_card(r"17.7\% $\to$ 46.5\%", r"Black patients among those flagged", r"after the label was "
                         r"changed from costs to a measure of health", color=GAIN, width=11.2, font_size=21),
        ).arrange(DOWN, buff=0.35).move_to(UP * 0.2)
        tag = published_tag(r"Obermeyer, \ Powers, \ Vogeli and Mullainathan, \ Science 366(6464) (2019)", corner=DL,
                            font_size=12)
        with self.voiceover(
            "Even when prediction is the right tool, what you predict is a choice. <bookmark mark='a'/> Ziad "
            "Obermeyer, Brian Powers, Christine Vogeli and Sendhil Mullainathan studied an algorithm used by a large "
            "health system to pick patients for extra care. It predicted each patient's future medical costs. "
            "<bookmark mark='b'/> Costs are not needs. Less was spent on Black patients with the same illnesses, "
            "so at the same score they were sicker. <bookmark mark='c'/> Changing the label from costs to a "
            "measure of health would raise the share of Black patients among those flagged from 17.7 percent to "
            "46.5. The algorithm predicted costs very well. It was the wrong target."
        ) as vo:
            self.play(FadeIn(hc[0], shift=UP * 0.1), FadeIn(tag))
            vo.wait_until("b")
            self.play(FadeIn(hc[1], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(hc[2], shift=UP * 0.1))
        self.clear_scene()
