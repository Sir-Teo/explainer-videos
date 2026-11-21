from __future__ import annotations

from videos.economics.econ64.common import *  # noqa: F403


class Agents(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Learning agents", r"What happens when the agents in a market are algorithms that learn?",
             "Chapter nine. Learning agents.", lit={2020: r"Calvano et al.", 2022: r"the AI Economist"},
             scale=("firm", "market"), horizon=("a year",))
        self.pricing()
        self.planner()

    def pricing(self):
        A = load("agents")
        rows = A["rows"]
        n = len(rows)
        ax = plane([0.4, n + 0.6], [1.4, 2.0], center=LEFT * 2.2 + DOWN * 0.3, x_length=7.2, y_length=4.6,
                   xticks=list(range(1, n + 1)), yticks=[1.4, 1.6, 1.8, 2.0], xlabel=r"session",
                   ylabel=r"price each algorithm settles on", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}",
                   font_size=14)
        nash = seg(ax, 0.4, A["nash"], n + 0.6, A["nash"], GAIN, 2.2, dashed=True)
        mono = seg(ax, 0.4, A["monopoly"], n + 0.6, A["monopoly"], COST, 2.2, dashed=True)
        nl = label(r"competition \ (Nash)", font_size=15, color=GAIN).next_to(ax.ax.c2p(n + 0.6, A["nash"]), RIGHT,
                                                                               buff=0.1)
        ml = label(r"monopoly", font_size=15, color=COST).next_to(ax.ax.c2p(n + 0.6, A["monopoly"]), RIGHT, buff=0.1)
        dots_ = VGroup()
        for k, r in enumerate(rows):
            for j, pr in enumerate(r["prices"]):
                dots_.add(dot(ax, k + 1 + (j - 0.5) * 0.25, pr, ALGO if j == 0 else NET, 0.08))
        side = VGroup(
            label(r"two Q-learning price setters, \\ Part 44's game, \ no communication", font_size=19, color=WHITE),
            label(rf"profit gain: \ {A['mean_gain']:.2f} on average \\ (0 = competition, \ 1 = monopoly)",
                  font_size=19, color=COST),
            label(r"held up by punishment: \\ undercut, \ and the rival cuts back", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Calvano, \ Calzolari, \ Denicolò and Pastorello, \ AER 110(10) (2020); \ the Island: \ "
                            r"agora.learn.pricing\_agents", corner=DL, font_size=12)
        with self.voiceover(
            "Part forty-four put two learning algorithms in charge of prices. Here they are again, in "
            f"{n} sessions. <bookmark mark='a'/> Each is a Q-learner: it tries prices, keeps a table of how well "
            "each did after each pair of last prices, and slowly stops experimenting. They never communicate. "
            "<bookmark mark='b'/> In almost every session they settle well above the competitive price, most of "
            f"the way to monopoly: a profit gain of {A['mean_gain']:.2f} on average. <bookmark mark='c'/> Emilio "
            "Calvano, Giacomo Calzolari, Vincenzo Denicolò and Sergio Pastorello showed why: the learned strategies "
            "punish a rival who undercuts, so undercutting does not pay. Nobody programmed collusion; it was "
            "learned. Whether the law can reach it is Part forty-four's open question."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(nash), FadeIn(mono), FadeIn(nl), FadeIn(ml), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots_], lag_ratio=0.05), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def planner(self):
        cards = point_cards([
            (r"the AI Economist", r"a planner that learns a tax schedule while the workers it taxes learn how much "
             r"to work and trade, \ in a simulated economy \ (Zheng et al., \ 2022)", NET),
            (r"why it is interesting", r"no closed form is needed: \ the agents can be as rich as a simulation "
             r"allows, \ and the planner adapts to how they respond", ALGO),
            (r"why to be careful", r"the agents learn what the simulation rewards; \ real people bring habits, \ "
             r"rules of thumb and politics no simulation was trained on", HOLD),
            (r"where it fits", r"a laboratory for mechanisms, \ beside theory and experiments, \ not a replacement "
             r"for either", TRUTHC),
        ], cols=2, width=12.8, font_size=20).move_to(DOWN * 0.2)
        head = label(r"learning agents as a laboratory", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Zheng, \ Trott, \ Srinivasa, \ Parkes and Socher, \ Science Advances 8(18) (2022)",
                            corner=DL, font_size=12)
        with self.voiceover(
            "Learning agents are also a laboratory. <bookmark mark='a'/> Stephan Zheng and coauthors' AI Economist "
            "trains a planner to choose a tax schedule while the simulated workers it taxes learn how much to "
            "work, build and trade. <bookmark mark='b'/> No closed form is needed, the agents can be as rich as the "
            "simulation allows, and the planner adapts to how they respond. <bookmark mark='c'/> The caution: the "
            "agents learn what the simulation rewards. Real people bring habits and rules of thumb, Part "
            "forty-five's biases, and politics, that no simulation was trained on. <bookmark mark='d'/> So it is a "
            "laboratory for mechanisms, beside theory and experiments, not a replacement for either."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()
