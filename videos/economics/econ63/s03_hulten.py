from __future__ import annotations

from videos.economics.econ63.common import *  # noqa: F403


class Hulten(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Hulten's theorem", r"If one sector becomes less productive, \ how much does GDP fall?",
             "Chapter two. Hulten's theorem.", lit={1978: r"Hulten"}, scale=("market", "nation"),
             horizon=("a year",))
        self.theorem()
        self.check()
        self.why()

    def theorem(self):
        eq = label(r"$d \log Y \;=\; \sum_i \lambda_i \, d\log A_i, \qquad \lambda_i = "
                   r"\dfrac{\text{sales}_i}{\text{GDP}}$", font_size=40).move_to(UP * 1.4)
        rows = VGroup(
            label(r"$A_i$: \ sector $i$'s productivity", font_size=24, color=GREY_A),
            label(r"$\lambda_i$: \ its Domar weight, \ sales over GDP", font_size=24, color=GDP),
            label(r"nothing else: \ not its links, \ not how far upstream, \ not its value added", font_size=24,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(eq, DOWN, buff=0.7)
        tag = published_tag(r"Hulten, \ Review of Economic Studies 45(3) (1978); \ Domar, \ Economic Journal 71 "
                            r"(1961)", corner=DL, font_size=12)
        with self.voiceover(
            "In 1978 Charles Hulten proved a result that makes the network disappear. <bookmark mark='a'/> If the "
            "economy is efficient, the change in real GDP from a small change in one sector's productivity is that "
            "change times the sector's Domar weight: its sales divided by GDP. <bookmark mark='b'/> That is all you "
            "need. <bookmark mark='c'/> Not how many sectors it supplies, not how far upstream it sits, not even its "
            "share of value added. Its sales summarize everything the network does with its output."
        ) as vo:
            self.play(FadeIn(eq), FadeIn(tag))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.15))
        self.clear_scene()

    def check(self):
        H = load("hulten")
        T = load("table")
        names = T["sectors"]
        lam = np.array(H["domar"])
        va = lam * np.array(T["labour_share"])
        loss = np.array([-100 * r["loss"] for r in H["rows"]])
        order = np.argsort(-lam)
        ax = plane([-0.6, 7.6], [0, 7], center=LEFT * 2.0 + DOWN * 0.3, x_length=8.0, y_length=4.6, xticks=[],
                   yticks=[0, 2, 4, 6], ylabel=r"GDP's fall from a 10\% fall in the sector's productivity, \ \%",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        vab = bars(ax, [k - 0.18 for k in range(8)], [10 * va[i] for i in order], [GREY_B] * 8, width=0.32)
        lb = bars(ax, [k + 0.18 for k in range(8)], [10 * lam[i] for i in order], [GDP] * 8, width=0.32)
        dots = VGroup(*[dot(ax, k + 0.18, loss[i], SHOCK, 0.06) for k, i in enumerate(order)])
        labs = VGroup(*[label(names[i], font_size=14, color=GREY_A).next_to(ax.ax.c2p(k, 0), DOWN, buff=0.12)
                        for k, i in enumerate(order)])
        key = legend_rows([(GREY_B, r"value added share $\times$ 10\%"), (GDP, r"Domar weight $\times$ 10\%"),
                           (SHOCK, r"computed fall in GDP")], font_size=16).to_corner(UR, buff=0.5)
        e = names.index("energy")
        note_ = label(rf"energy: \ value added {100 * va[e]:.0f}\% of GDP, \ sales {100 * lam[e]:.0f}\%; \ GDP falls "
                      rf"{loss[e]:.1f}\%", font_size=19, color=E.ACCENT).to_edge(DOWN, buff=0.45)
        tag = island_tag(r"the Island: \ Cobb-Douglas technologies; \ agora.network.which\_failure", corner=DL,
                         font_size=12)
        with self.voiceover(
            "Check it on the Island. Lower each sector's productivity by ten percent, one at a time, and solve the "
            "whole network for its new prices and GDP. <bookmark mark='a'/> In grey, the sector's share of value "
            "added: the wages it pays, as a share of GDP. <bookmark mark='b'/> In gold, its Domar weight. "
            "<bookmark mark='c'/> And in red, the fall in GDP that the model actually computes. The red dots sit on "
            "the gold bars, every one. <bookmark mark='d'/> Energy adds only "
            f"{100 * va[e]:.0f} percent of GDP itself, but sells {100 * lam[e]:.0f} percent, and a ten percent "
            f"fall in its productivity costs {loss[e]:.1f} percent of GDP: its sales, not its value added."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(labs), FadeIn(tag))
            vo.wait_until("a")
            self.play(*[GrowFromEdge(b, DOWN) for b in vab], FadeIn(key[0]))
            vo.wait_until("b")
            self.play(*[GrowFromEdge(b, DOWN) for b in lb], FadeIn(key[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.12), FadeIn(key[2]))
            vo.wait_until("d")
            self.play(FadeIn(note_))
        self.clear_scene()

    def why(self):
        steps = flow_chain([(r"energy's productivity rises 10\%", LINK),
                            (r"every unit of energy costs 10\% less", LINK),
                            (r"every buyer saves 10\% of its energy bill", NODE),
                            (r"the saving: \ 10\% of energy's sales", GDP)], box_w=2.8, box_h=1.3, font_size=20)
        steps.move_to(UP * 0.6)
        if steps.width > 13.0:
            steps.width = 13.0
        rows = VGroup(
            label(r"the saving is the same whoever buys the energy, \ and however long the chain", font_size=22,
                  color=WHITE),
            label(r"true for small shocks, \ in an efficient economy; \ chapters four and five break both",
                  font_size=22, color=HOLD),
        ).arrange(DOWN, buff=0.3).next_to(steps, DOWN, buff=0.7)
        with self.voiceover(
            "Why? <bookmark mark='a'/> Suppose energy's productivity rises by ten percent. Every unit of energy now "
            "takes ten percent less to make, so, in a competitive economy, it costs ten percent less. Every buyer, "
            "whether a factory or a farm or a household, saves ten percent of what it spends on energy. And the "
            "total spent on energy, by everyone, is energy's sales. <bookmark mark='b'/> It does not matter who "
            "buys it or how long the chain is: the saving is the same. <bookmark mark='c'/> But notice the small "
            "print. The theorem is about small shocks, in an efficient economy. Chapters four and five break each "
            "of those conditions, and with them the idea that a sector's sales tell you everything."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in steps.boxes], lag_ratio=0.5),
                      LaggedStart(*[GrowArrow(a) for a in steps.arrows], lag_ratio=0.5), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()
