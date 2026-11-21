from __future__ import annotations

from videos.economics.econ58.common import *  # noqa: F403

ACC = (r"food", r"manuf.", r"labour", r"capital", r"household", r"govt.")


def sam_table(M, highlight=None, font_size=18):
    """A social accounting matrix as a grid: columns pay rows."""
    M = np.asarray(M)
    cells = VGroup()
    head = VGroup(*[label(a, font_size=font_size - 2, color=GREY_B) for a in ACC])
    side = VGroup(*[label(a, font_size=font_size - 2, color=GREY_B) for a in ACC])
    w, h = 1.25, 0.48
    for i in range(6):
        for j in range(6):
            v = M[i, j]
            t = label(f"{v:.1f}" if abs(v) > 1e-9 else r"$\cdot$", font_size=font_size,
                      color=WHITE if abs(v) > 1e-9 else GREY_D)
            t.move_to([j * w, -i * h, 0])
            if highlight is not None and highlight[i][j]:
                t.set_color(E.ACCENT)
            cells.add(t)
    for j, m in enumerate(head):
        m.move_to([j * w, h * 1.0, 0])
    for i, m in enumerate(side):
        m.move_to([-w * 1.05, -i * h, 0])
    tot_r = VGroup(*[label(f"{v:.1f}", font_size=font_size - 2, color=BEN).move_to([6 * w + 0.15, -i * h, 0])
                     for i, v in enumerate(M.sum(axis=1))])
    tot_c = VGroup(*[label(f"{v:.1f}", font_size=font_size - 2, color=BEN).move_to([j * w, -6 * h - 0.1, 0])
                     for j, v in enumerate(M.sum(axis=0))])
    rl = label(r"row totals: \ received", font_size=14, color=BEN).next_to(tot_r, UP, buff=0.12)
    cl = label(r"column totals: \ paid", font_size=14, color=BEN).next_to(tot_c, LEFT, buff=0.3).shift(LEFT * 0.6)
    g = VGroup(head, side, cells, tot_r, tot_c, rl, cl)
    g.cells, g.tot_r, g.tot_c = cells, tot_r, tot_c
    return g


class CGE(VoiceoverScene):
    def construct(self):
        card(self, 9, r"General equilibrium", r"What does a tax on one industry do to all the others?",
             "Chapter nine. General equilibrium.", lit={1962: r"Harberger", 1993: r"NAFTA's models",
                                                        2005: r"Kehoe's audit"},
             scale=("market", "nation"), horizon=("a decade",))
        self.matrix()
        self.tax()
        self.nafta()

    def matrix(self):
        C = load("cge")
        tab = sam_table(C["sam0"]["M"]).scale(0.95).move_to(LEFT * 0.6 + DOWN * 0.2)
        head = label(r"the Island's social accounting matrix: \ each column pays the rows \ (billions)",
                     font_size=24, color=E.ACCENT).to_edge(UP, buff=0.45)
        p = C["params"]
        notes_ = VGroup(
            label(rf"food: \ labour's share {p['alpha']['F']:.0%}".replace("%", r"\%"), font_size=18,
                  color=GREY_A),
            label(rf"manufactures: \ labour's share {p['alpha']['M']:.0%}".replace("%", r"\%"), font_size=18,
                  color=GREY_A),
            label(rf"the household spends {p['share']['F']:.0%} on food".replace("%", r"\%"), font_size=18,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DR, buff=0.4)
        with self.voiceover(
            "Scores and appraisals mostly look at one market at a time. General equilibrium looks at all of them, "
            "and its bookkeeping is Part three's social accounting matrix. <bookmark mark='a'/> Here is a small one "
            "for the Island: two industries, food and manufactures; two factors, labour and capital; a household "
            "that owns both; and a government. Each column pays the rows: the household's column buys food and "
            "manufactures, the industries' columns pay labour and capital, the factors pay the household. <bookmark "
            "mark='b'/> Every account balances: what each receives, along its row, equals what it pays, down its "
            "column. <bookmark mark='c'/> Food uses more labour; manufactures use more capital. A computable general "
            "equilibrium model is this matrix made to respond: prices move until every market clears again."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(tab[1]), LaggedStart(*[FadeIn(c) for c in tab.cells], lag_ratio=0.02),
                      run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(tab.tot_r), FadeIn(tab.tot_c), FadeIn(tab[5]), FadeIn(tab[6]))
            vo.wait_until("c")
            self.play(FadeIn(notes_))
        self.clear_scene()

    def tax(self):
        C = load("cge")
        b, t = C["base"], C["taxed"]
        ts, loss, tri = 100 * np.array(C["ts"]), np.array(C["loss"]), np.array(C["tri"])
        ax = plane([0, 40], [0, 4.0], center=LEFT * 3.4 + DOWN * 0.6, x_length=5.6, y_length=4.2,
                   xticks=[0, 10, 20, 30, 40], yticks=[0, 1, 2, 3, 4], xlabel=r"tax on manufactures, \ \%",
                   ylabel=r"deadweight loss, \ billions", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        cl = path(ax, ts, loss, BEN, 3.0)
        ct = path(ax, ts, tri, WHITE, 2.0).set_stroke(opacity=0.7)
        wr = 100 * (t["w"] / b["w"] - 1)
        rows = VGroup(
            label(r"a 10\% tax on manufactures, \ revenue handed back", font_size=21, color=E.ACCENT),
            label(rf"manufactures: \ {b['X']['M']:.1f} $\to$ {t['X']['M']:.1f}; \ food: \ {b['X']['F']:.1f} $\to$ "
                  rf"{t['X']['F']:.1f}", font_size=19, color=GREY_A),
            label(rf"labour moves to food: \ {b['L']['F']:.1f} $\to$ {t['L']['F']:.1f}", font_size=19,
                  color=GREY_A),
            label(rf"the wage rises {wr:.1f}\% against the return to capital", font_size=19, color=TRAV),
            label(r"so capital bears more of the tax than its owners' spending on manufactures", font_size=17,
                  color=GREY_B),
            label(rf"deadweight loss: \ {C['dwl']:.2f} \ (Harberger's triangle: \ {C['harberger']:.2f}), \ "
                  rf"on revenue of {C['revenue']:.1f}", font_size=19, color=BEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).to_edge(RIGHT, buff=0.3)
        if rows.width > 7.4:
            rows.width = 7.4
            rows.to_edge(RIGHT, buff=0.3)
        key = VGroup(label(r"green: \ general equilibrium", font_size=15, color=BEN),
                     label(r"white: \ the triangle", font_size=15, color=WHITE)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).next_to(ax.ax.c2p(2, 3.8), RIGHT, buff=0.05)
        tag = island_tag(r"the Island: \ agora.appraisal.cge", corner=DR, font_size=12)
        with self.voiceover(
            "Now tax manufactures at ten percent and hand the revenue back. <bookmark mark='a'/> In general "
            f"equilibrium, people buy fewer manufactures, {t['X']['M']:.1f} instead of {b['X']['M']:.1f}, and more "
            "food. <bookmark mark='b'/> Food needs more labour per unit, so labour moves into food, <bookmark "
            f"mark='c'/> and the wage rises by {wr:.1f} percent against the return to capital. Arnold Harberger's "
            "insight of 1962: a tax on one industry tends to fall on the factor it uses most, wherever that factor "
            "works, and here that is capital. <bookmark mark='d'/> The loss to the economy, the deadweight loss, is "
            f"{C['dwl']:.2f} billion, against {C['revenue']:.1f} of revenue. <bookmark mark='e'/> Harberger's "
            f"partial-equilibrium triangle gives {C['harberger']:.2f}: the right order of magnitude, a little high, "
            "because the triangle takes the supply of manufactures as flat, while in general equilibrium the factors "
            "cannot leave without their prices changing, so output falls less. For a small tax, the triangle is "
            "enough; for a large change, the economy-wide model earns its keep."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]), FadeIn(rows[4]))
            vo.wait_until("d")
            self.play(FadeIn(ax), Create(cl), FadeIn(key[0]), FadeIn(rows[5]), run_time=1.6)
            vo.wait_until("e")
            self.play(Create(ct), FadeIn(key[1]))
        self.clear_scene()

    def nafta(self):
        F = tables.FRONTIER58
        hc = history_card(1993, r"the NAFTA debate", r"three of the most prominent applied general equilibrium "
                          r"models predicted how trade between Mexico, Canada and the United States would change, "
                          r"industry by industry", color=TRAV, width=11.0, font_size=22)
        kc = history_card(2005, r"Timothy Kehoe's audit", r"they drastically underestimated the growth of trade; "
                          r"\ their predictions for each industry were roughly uncorrelated with what happened; \ "
                          r"the biggest growth came in goods hardly traded before", color=COST, width=11.0,
                          font_size=22)
        lesson = label(r"a model's structure is a forecast too: \ check it afterwards", font_size=28,
                       color=E.ACCENT)
        VGroup(hc, kc, lesson).arrange(DOWN, buff=0.45).move_to(DOWN * 0.1)
        tag = published_tag(F.tag, corner=DL, font_size=12)
        with self.voiceover(
            "Such models are used to score trade agreements, and they can be checked afterwards. <bookmark "
            "mark='a'/> Before the North American Free Trade Agreement took effect in 1994, the leading applied "
            "general equilibrium models predicted how trade would change, industry by industry. <bookmark "
            "mark='b'/> A decade later Timothy Kehoe compared their predictions with what happened. They had "
            "drastically underestimated how much trade would grow, and their predictions for each industry were "
            "roughly uncorrelated with the outcomes; the biggest growth came in goods that had hardly been traded "
            "before, a margin the models did not have. <bookmark mark='c'/> The lesson is the same as for every "
            "forecast in this series: a model's structure is a forecast too, and it should be scored."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(kc, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(lesson, shift=UP * 0.1))
        self.clear_scene()
