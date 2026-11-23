from __future__ import annotations

from videos.industry.industry2.common import *  # noqa: F403


class Ripple(VoiceoverScene):
    def construct(self):
        card(self, 9, "Everything a dollar touches", "If you buy a dollar of manufactured goods, how much must the "
             "economy produce?", "Chapter nine. Everything a dollar touches.", lit=("make", "dollar"))
        self.rounds()
        self.totals()

    def rounds(self):
        io = R["io"]
        A = np.array(io["A"])
        names = io["names"]
        m = names.index("Manufacturing")
        e = np.zeros(len(names))
        e[m] = 1.0
        show = ["Manufacturing", "Wholesale", "Business services", "Mining", "Farms", "Finance and real estate",
                "Transport", "Utilities", "Information"]
        idx = [names.index(s) for s in show]
        cum = []
        x, total = e.copy(), np.zeros_like(e)
        for k in range(8):
            total = total + x
            cum.append(total.copy())
            x = A @ x
        L = np.array(io["L"])[:, m]
        pa = viz.plot_axes((-0.6, len(show) - 0.4), (0, 1.7), x_length=11.2, y_length=4.2, yticks=[0, 0.5, 1.0, 1.5],
                           yfmt=lambda v: f"${v:.2f}", size=16).shift(DOWN * 0.55 + RIGHT * 0.2)
        SHORTL = {"Manufacturing": "Factories", "Business services": "Business", "Finance and real estate":
                  "Finance", "Information": "Info"}
        labs = VGroup(*[T(SHORTL.get(s, s), 15, I.TEXT).next_to(pa.ax.c2p(i, 0), DOWN, buff=0.12)
                        for i, s in enumerate(show)])

        def bars(v):
            out = VGroup()
            for i, j in enumerate(idx):
                p0, p1 = pa.ax.c2p(i, 0), pa.ax.c2p(i, v[j])
                out.add(Rectangle(width=0.7, height=max(p1[1] - p0[1], 0.004), fill_color=I.ACCENT if j == m else
                                  "#7EC8F5", fill_opacity=0.9, stroke_width=0).move_to(
                    np.array([p0[0], (p0[1] + p1[1]) / 2, 0])))
            return out
        b = bars(cum[0])
        rnd = T("round 0: the dollar you spend", 22, I.ACCENT).to_edge(UP, buff=0.45)
        tot = TB(f"total output: ${cum[0].sum():.2f}", 26, I.MONEY).to_corner(UR, buff=0.5).shift(DOWN * 0.5)
        src = source("BEA 2023 use table: this film's Leontief inverse", corner=DR)
        with self.voiceover(
            "The table lets you ask a question Leontief built it for. Suppose someone buys one more dollar of "
            "manufactured goods. How much does the whole economy have to produce? <bookmark mark='a'/> Round zero: "
            "the factory makes the dollar's worth of goods. <bookmark mark='b'/> Round one: to make it, the factory "
            "buys 62 cents of inputs, from other factories, wholesalers, mines, farms. <bookmark mark='c'/> Round two: "
            "those suppliers buy inputs of their own, and so on, each round smaller than the last. <bookmark "
            "mark='d'/> Add up all the rounds and the answer converges: 2 dollars 25 of output across the economy for "
            "one dollar of manufactured goods bought. Leontief found a shortcut to the sum of every round, a single "
            "calculation on the table, which now bears his name: the Leontief inverse."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(labs), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(b), FadeIn(rnd), FadeIn(tot))
            vo.wait_until("b")
            nb = bars(cum[1])
            flows = [draw.coin_flow(b[0].get_top(), nb[i].get_top() + UP * 0.12, n=2, r=0.07, arc=-0.8, run_time=1.4)
                     for i in range(1, len(show))]
            self.add(*[c for c, _ in flows])
            self.play(*[a_ for _, a_ in flows])
            self.remove(*[c for c, _ in flows])
            self.play(Transform(b, nb), Transform(rnd, T("round 1: the factory's inputs", 22, I.ACCENT
                                                                   ).move_to(rnd)),
                      Transform(tot, TB(f"total output: ${cum[1].sum():.2f}", 26, I.MONEY).move_to(tot)))
            vo.wait_until("c")
            for k in range(2, 8):
                if k < 4:  # the suppliers' own purchases ripple on
                    nb = bars(cum[k])
                    flows = [draw.coin_flow(b[i].get_top(), nb[j].get_top() + UP * 0.1, n=1, r=0.06, arc=-0.8,
                                            run_time=0.8) for i, j in ((1, 3), (2, 6), (3, 7), (5, 1), (6, 4))]
                    self.add(*[c for c, _ in flows])
                    self.play(*[a_ for _, a_ in flows])
                    self.remove(*[c for c, _ in flows])
                self.play(Transform(b, bars(cum[k])), Transform(rnd, T(f"round {k}: their suppliers' inputs", 22,
                                                                      I.ACCENT).move_to(rnd)),
                          Transform(tot, TB(f"total output: ${cum[k].sum():.2f}", 26, I.MONEY).move_to(tot)),
                          run_time=0.7)
            vo.wait_until("d")
            self.play(Transform(b, bars(L)), Transform(rnd, T("all rounds: the Leontief inverse", 22, I.ACCENT
                                                              ).move_to(rnd)),
                      Transform(tot, TB(f"total output: ${L.sum():.2f}", 26, I.MONEY).move_to(tot)))
        self.clear_scene()

    def totals(self):
        io = R["io"]
        items = sorted([(n, t, "#7EC8F5" if n != "Manufacturing" else I.ACCENT, "") for n, t in
                        zip(io["names"], io["total"])], key=lambda r: -r[1])
        rows = viz.margin_ladder(items, max_value=2.4, bar_len=6.0, row_h=0.38, size=18, name_w=4.2,
                                 fmt=lambda v: f"${v:.2f}")
        rows.move_to(RIGHT * 0.9 + DOWN * 0.3)
        head = T("Output the economy produces for $1 of each industry's goods bought by final users", 22, I.TEXT
                 ).to_edge(UP, buff=0.4)
        caveat = T("It assumes every industry keeps its recipe as it grows: a guide, not a law.", 19, I.DIM).to_edge(
            DOWN, buff=0.35)
        with self.voiceover(
            "Every industry has its own number. <bookmark mark='a'/> Manufacturing and farming reach furthest into "
            "the rest of the economy, more than two dollars of output for each dollar sold to final users, because "
            "they buy so much from others. Professional services, utilities and other services reach least, about "
            "one dollar fifty, because most of what they sell is their own people's time. <bookmark mark='b'/> "
            "These numbers are what consultants mean when they say a new factory supports so many jobs in the "
            "wider economy. Treat them with care: they assume that every industry keeps the same recipe as it "
            "grows, and that its suppliers have room to grow with it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.08), run_time=2.4)
            vo.wait_until("b")
            self.play(FadeIn(caveat))
        self.clear_scene()
