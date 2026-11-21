from __future__ import annotations

from videos.economics.econ63.common import *  # noqa: F403

RULES = (("most central", SEED), ("at random", GDP), ("least central", GREY_B))


class Diffusion(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Diffusion: \ who to tell first", r"A lender arrives in a village: \ whom should it tell, \ "
             r"so that word spreads?", "Chapter ten. Diffusion: who to tell first.",
             lit={2013: r"Banerjee et al."}, scale=("household", "city"), horizon=("a year",))
        self.villages()
        self.curves()
        self.evidence()

    def villages(self):
        D = load("diffusion")
        xy, edges = D["xy"], D["edges"]
        graphs = VGroup()
        nodes_by = []
        for k, (name, col) in enumerate(RULES):
            es, ns = graph_mob(xy, edges, center=np.array([-4.6 + 4.6 * k, 0.5, 0]), scale=1.8, node_r=0.035,
                               color=GREY_B, edge_color="#46506A", edge_width=0.7)
            ttl = label(rf"tell the five {name}" if name != "at random" else r"tell five at random", font_size=19,
                        color=col).next_to(VGroup(es, ns), DOWN, buff=0.3)
            cnt = label(r"", font_size=18, color=PEOPLE)
            graphs.add(VGroup(es, ns, ttl))
            nodes_by.append((ns, cnt))
        rnd = label(r"round 0", font_size=26, color=E.ACCENT).to_edge(UP, buff=0.35)
        tag = island_tag(r"the Island's village: \ 200 households; \ each round, \ each informed household tells "
                         r"each neighbour with chance 0.12", corner=DL, font_size=12)
        runs = D["runs"]
        with self.voiceover(
            "Here is one of the Island's villages: two hundred households, each linked to its neighbours and to "
            "a few people further away, with six households that everyone knows. <bookmark mark='a'/> A lender "
            "arrives and can tell five households about its loans. Each round, every household that knows tells "
            "each of its contacts with a chance of about one in eight. <bookmark mark='b'/> On the left, it tells "
            "the five most central households; in the middle, five at random; on the right, the five least "
            "central. <bookmark mark='c'/> Watch eight rounds."
        ) as vo:
            self.play(FadeIn(tag), *[FadeIn(g[0]) for g in graphs], *[FadeIn(g[1]) for g in graphs], run_time=2.0)
            vo.wait_until("a")
            self.play(*[FadeIn(g[2]) for g in graphs])
            vo.wait_until("b")
            self.play(*[nodes_by[k][0][i].animate.set_color(RULES[k][1]).scale(2.2)
                        for k, (name, _) in enumerate(RULES) for i in runs[name][0]], FadeIn(rnd))
            vo.wait_until("c")
        for t in range(1, 9):
            anims = [Transform(rnd, label(rf"round {t}", font_size=26, color=E.ACCENT).to_edge(UP, buff=0.35))]
            for k, (name, _) in enumerate(RULES):
                new = set(runs[name][t]) - set(runs[name][t - 1])
                anims += [nodes_by[k][0][i].animate.set_color(PEOPLE) for i in new]
            self.play(*anims, run_time=0.9)
        shares = VGroup(*[label(rf"{100 * len(runs[name][-1]) / 200:.0f}\% informed", font_size=20,
                                color=RULES[k][1]).next_to(graphs[k][2], DOWN, buff=0.15)
                          for k, (name, _) in enumerate(RULES)])
        with self.voiceover(
            "After eight rounds, in this run, <bookmark mark='a'/> the news has reached most of the village when "
            "it started at the centre, much of it when it started at random, and only a corner of it when it "
            "started at the edge."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(shares))
        self.clear_scene()

    def curves(self):
        D = load("diffusion")
        r = D["rounds"]
        ax = plane([0, 8], [0, 1], center=LEFT * 2.4 + DOWN * 0.3, x_length=6.6, y_length=4.6, xticks=list(range(9)),
                   yticks=[0, 0.25, 0.5, 0.75, 1.0], xlabel=r"round", ylabel=r"share of the village informed",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: rf"{100 * v:.0f}\%", font_size=14)
        ls = VGroup(*[path(ax, r, D[name], col, 3.4) for name, col in RULES])
        side = VGroup(*[label(rf"{name}: \ {100 * D[name][-1]:.0f}\%", font_size=20, color=col)
                        for name, col in RULES],
                      label(r"same village, \ same five letters: \\ the seeds' position decides", font_size=20,
                            color=E.ACCENT)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5)
        tag = island_tag(r"the Island: \ 300 runs of each rule; \ agora.network.diffusion", corner=DL, font_size=12)
        with self.voiceover(
            "Averaged over three hundred runs: <bookmark mark='a'/> starting from the most central households, "
            f"{100 * D['most central'][-1]:.0f} percent of the village knows after eight rounds; <bookmark "
            f"mark='b'/> from households chosen at random, {100 * D['at random'][-1]:.0f} percent; <bookmark "
            f"mark='c'/> from the least central, {100 * D['least central'][-1]:.0f}. <bookmark mark='d'/> Same "
            "village, same five conversations. Where the news starts decides how far it goes. Centrality here is "
            "eigenvector centrality: you are central if your contacts are central."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(Create(ls[k]), FadeIn(side[k]), run_time=1.2)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def evidence(self):
        hc = VGroup(
            history_card(r"43 villages", r"Karnataka, \ south India", r"a microfinance lender, \ entering 43 "
                         r"villages, \ "
                         r"first invites local leaders, \ teachers, \ shopkeepers, \ heads of savings groups, \ and "
                         r"asks them to spread the word", color=PEOPLE, width=11.4, font_size=21),
            history_card(2013, r"Banerjee, \ Chandrasekhar, \ Duflo and Jackson", r"economists had mapped every "
                         r"village's network beforehand; \ take-up was higher where the leaders who were told first "
                         r"were more central", color=SEED, width=11.4, font_size=21),
            history_card(r"since", r"seeding by the network", r"later trials seed with the people villagers name as "
                         r"good at spreading news, \ a cheap way to find the centre without a map", color=GDP,
                         width=11.4, font_size=21),
        ).arrange(DOWN, buff=0.35).move_to(UP * 0.2)
        tag = published_tag(r"Banerjee, \ Chandrasekhar, \ Duflo and Jackson, \ Science 341(6144) (2013)",
                            corner=DL, font_size=12)
        with self.voiceover(
            "This is not only a simulation. <bookmark mark='a'/> In Karnataka, in south India, a microfinance "
            "lender entering forty-three villages first invited local leaders, teachers, shopkeepers and the heads "
            "of savings groups to a meeting, and asked them to spread the word. <bookmark mark='b'/> Abhijit "
            "Banerjee, Arun Chandrasekhar, Esther Duflo and Matthew Jackson had surveyed the villages' networks "
            "beforehand. Where the leaders who heard first were more central, more households took up the loans. "
            "<bookmark mark='c'/> Later trials have seeded information through the people villagers themselves "
            "name as good at spreading news: a cheap way to find the centre of a network without mapping it."
        ) as vo:
            self.play(FadeIn(hc[0], shift=UP * 0.1), FadeIn(tag))
            vo.wait_until("b")
            self.play(FadeIn(hc[1], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(hc[2], shift=UP * 0.1))
        self.clear_scene()
