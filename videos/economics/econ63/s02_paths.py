from __future__ import annotations

from videos.economics.econ63.common import *  # noqa: F403

LEN_COLS = (GDP, LINK, NODE, GREY_B)


class Paths(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Leontief's paths", r"How does an input-output table become a network, \ and how far does each "
             r"sector's output travel?", "Chapter one. Leontief's paths.", lit={1936: r"Leontief", 1961: r"Domar"},
             scale=("market", "nation"), horizon=("a year",))
        self.table()
        self.network()
        self.paths()
        self.upstream()

    def table(self):
        T = load("table")
        S = np.array(T["shares"])
        names = T["sectors"]
        n = len(names)
        cell = 0.62
        grid = VGroup()
        for i in range(n):
            for j in range(n):
                v = S[i, j]
                sq = Square(side_length=cell, stroke_color=GREY_D, stroke_width=0.8, fill_color=LINK,
                            fill_opacity=min(0.9, 3.2 * v)).move_to([j * cell, -i * cell, 0])
                txt = label(f"{v:.2f}" if v > 0 else "", font_size=13, color=WHITE).move_to(sq)
                grid.add(VGroup(sq, txt))
        lab_col = VGroup()
        for i in range(n):
            v = T["labour_share"][i]
            sq = Square(side_length=cell, stroke_color=GREY_D, stroke_width=0.8, fill_color=GDP,
                        fill_opacity=0.5 * v).move_to([(n + 0.4) * cell, -i * cell, 0])
            lab_col.add(VGroup(sq, label(f"{v:.2f}", font_size=13, color=WHITE).move_to(sq)))
        rows = VGroup(*[label(nm, font_size=15, color=GREY_A).next_to(grid[i * n][0], LEFT, buff=0.15)
                        for i, nm in enumerate(names)])
        cols = VGroup(*[label(nm, font_size=14, color=GREY_A).rotate(PI / 3).next_to(grid[j][0], UP, buff=0.1)
                        for j, nm in enumerate(names)])
        lc = label(r"labour", font_size=14, color=GDP).rotate(PI / 3).next_to(lab_col[0][0], UP, buff=0.1)
        tbl = VGroup(grid, lab_col, rows, cols, lc).move_to(LEFT * 2.0 + DOWN * 0.3)
        if tbl.height > 6.2:
            tbl.scale_to_fit_height(6.2)
            tbl.move_to(LEFT * 2.0 + DOWN * 0.3)
        side = VGroup(
            label(r"rows: \ who buys", font_size=20, color=WHITE),
            label(r"columns: \ who sells", font_size=20, color=LINK),
            label(r"each row: \ where a sector's \\ costs go; \ labour gets the rest", font_size=20, color=GDP),
            label(r"retail spends 0.20 \\ of its costs on factories", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5)
        tag = island_tag(r"the Island's input-output table: \ agora.network.SHARES", corner=DL, font_size=12)
        with self.voiceover(
            "Part three met Wassily Leontief's input-output table. Here is the Island's, for eight sectors. "
            "<bookmark mark='a'/> Each row is a buyer; <bookmark mark='b'/> each column a seller. <bookmark "
            "mark='c'/> A row says where a sector's costs go: so much to energy, so much to transport, and the "
            "rest, in the last column, to the people who work in it. <bookmark mark='d'/> Retail, for example, "
            "spends a fifth of its costs on the goods factories make, and fifteen cents in the dollar on farms."
        ) as vo:
            self.play(FadeIn(tbl), FadeIn(tag), run_time=1.5)
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(side[k], shift=LEFT * 0.1))
        self.clear_scene()

    def network(self):
        T = load("table")
        ring = sector_ring(radius=2.6, center=LEFT * 2.2 + DOWN * 0.3, font_size=18, node_r=0.5)
        arr = flow_arrows(ring, T["shares"], cut=0.08)
        side = VGroup(
            label(r"an arrow for every input \\ worth 8\% or more of a buyer's costs", font_size=20, color=LINK),
            label(r"energy sells to every sector", font_size=20, color=WHITE),
            label(r"most households buy services and retail; \\ few buy metals at all", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "Draw the same table as a network. <bookmark mark='a'/> Each sector is a node, and an arrow runs from "
            "seller to buyer whenever an input is a large part of the buyer's costs. <bookmark mark='b'/> Energy "
            "sells to every sector, metals mostly to factories. <bookmark mark='c'/> And households buy mainly "
            "services and retail, almost nothing from the metal works. The question of this chapter: when "
            "households spend a dollar, how much of it ends up as sales of each sector, and along which paths?"
        ) as vo:
            self.play(FadeIn(ring), run_time=1.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a) for a in arr], lag_ratio=0.05), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(Indicate(ring[1], color=LINK, scale_factor=1.15), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def paths(self):
        T = load("table")
        names = T["sectors"]
        lam = np.array(T["domar"])
        P = np.array(T["partial"])
        order = np.argsort(-lam)
        parts = [P[0], P[1] - P[0], P[2] - P[1], lam - P[2]]
        ax = plane([0, 0.7], [-0.5, 7.5], center=LEFT * 2.1 + DOWN * 0.35, x_length=6.6, y_length=5.0,
                   xticks=[0, 0.2, 0.4, 0.6], yticks=[], xlabel=r"sales per dollar of GDP \ (Domar weight)",
                   xfmt=lambda v: f"{v:.1f}", font_size=15)
        rows = VGroup()
        names_m = VGroup()
        for r, i in enumerate(order):
            y = 7 - r
            x0 = 0.0
            row = VGroup()
            for k, part in enumerate(parts):
                w = part[i]
                p0, p1 = ax.ax.c2p(x0, y - 0.32), ax.ax.c2p(x0 + w, y + 0.32)
                row.add(Rectangle(width=max(p1[0] - p0[0], 0.001), height=p1[1] - p0[1], fill_color=LEN_COLS[k],
                                  fill_opacity=0.85, stroke_width=0).move_to((p0 + p1) / 2))
                x0 += w
            rows.add(row)
            names_m.add(label(rf"{names[i]} \ \ {lam[i]:.2f}", font_size=15, color=GREY_A).next_to(
                ax.ax.c2p(0, y), LEFT, buff=0.1))
        key = legend_rows([(GDP, r"sold straight to households"), (LINK, r"through one buyer"),
                           (NODE, r"through two"), (GREY_B, r"three or more")], font_size=17)
        eq = label(r"$\lambda' = \beta'(I - \Omega)^{-1} = \beta'(I + \Omega + \Omega^2 + \cdots)$", font_size=26)
        tot = label(rf"the weights add to {lam.sum():.2f}: \ sales count \\ every input again at each step",
                    font_size=19, color=GDP)
        side = VGroup(eq, key, tot).arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(RIGHT, buff=0.4)
        if side.width > 5.6:
            side.width = 5.6
            side.to_edge(RIGHT, buff=0.4)
        tag = island_tag(r"computed: \ agora.network.leontief", corner=DL, font_size=12)
        with self.voiceover(
            "Follow a dollar of household spending. <bookmark mark='a'/> Some of it goes straight to a sector: "
            "forty-five cents to services, twenty-eight to retail. <bookmark mark='b'/> But retail spends part of "
            "its dollar on factories, which spend part of theirs on metals, which buy energy. Each step is one "
            "more power of the matrix of input shares, and the sum of all the paths is Leontief's inverse. "
            f"<bookmark mark='c'/> The result is each sector's sales per dollar of GDP, its Domar weight, after "
            f"Evsey Domar. Services sell {lam[6]:.2f}, mostly straight to households. Energy sells "
            f"{lam[1]:.2f}, and only a fifth of that goes to households directly: the rest travels along chains "
            f"of one, two or more buyers. <bookmark mark='d'/> The weights add up to {lam.sum():.2f}, not one, "
            "because sales count an input again every time it changes hands."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(names_m), FadeIn(tag), FadeIn(eq))
            vo.wait_until("a")
            self.play(*[GrowFromEdge(r[0], LEFT) for r in rows], FadeIn(key[0]))
            vo.wait_until("b")
            self.play(*[GrowFromEdge(r[1], LEFT) for r in rows], FadeIn(key[1]), run_time=0.8)
            self.play(*[GrowFromEdge(r[2], LEFT) for r in rows], FadeIn(key[2]), run_time=0.8)
            self.play(*[GrowFromEdge(r[3], LEFT) for r in rows], FadeIn(key[3]), run_time=0.8)
            vo.wait_until("c")
            self.play(Indicate(names_m[list(order).index(1)], color=LINK))
            vo.wait_until("d")
            self.play(FadeIn(tot))
        self.clear_scene()

    def upstream(self):
        T = load("table")
        names = T["sectors"]
        up = np.array(T["upstreamness"])
        order = np.argsort(-up)
        ax = plane([0, 4], [-0.5, 7.5], center=LEFT * 2.4 + DOWN * 0.35, x_length=6.0, y_length=5.0,
                   xticks=[1, 2, 3, 4], yticks=[], xlabel=r"average steps from the household \ (upstreamness)",
                   xfmt=lambda v: f"{v:.0f}", font_size=15)
        bs = VGroup()
        nm = VGroup()
        for r, i in enumerate(order):
            y = 7 - r
            p0, p1 = ax.ax.c2p(0, y - 0.3), ax.ax.c2p(up[i], y + 0.3)
            bs.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=NODE, fill_opacity=0.8,
                             stroke_width=0).move_to((p0 + p1) / 2))
            nm.add(label(rf"{names[i]} \ \ {up[i]:.1f}", font_size=15, color=GREY_A).next_to(ax.ax.c2p(0, y), LEFT,
                                                                                         buff=0.1))
        side = VGroup(
            label(r"metals: \ 3.4 steps before \\ anyone eats, \ drives or watches", font_size=20, color=NODE),
            label(r"retail: \ one step", font_size=20, color=GREY_A),
            label(r"so: \ does a sector far upstream \\ matter more when it fails?", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.5)
        tag = island_tag(r"computed: \ agora.network.leontief \ (after Antr\`as, \ Chor, \ Fally and Hillberry)",
                         corner=DL, font_size=12)
        with self.voiceover(
            "One more measure of where a sector sits. <bookmark mark='a'/> Count, on average, how many steps its "
            "sales travel before they reach a household. That is its upstreamness. Metals are three and a half "
            "steps away: ore becomes steel, steel becomes a part, the part becomes a machine. <bookmark mark='b'/> "
            "Retail is one step: it sells to us. <bookmark mark='c'/> It is tempting to think that a sector deep "
            "upstream, feeding everything, must matter most when it fails. The next chapter says that, to a first "
            "approximation, it does not."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(nm), FadeIn(tag))
            self.play(*[GrowFromEdge(b, LEFT) for b in bs], run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()
