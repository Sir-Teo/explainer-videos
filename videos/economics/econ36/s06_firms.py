from __future__ import annotations

from videos.economics.econ36.common import *  # noqa: F403


class Firms(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Exporters are rare", r"Which firms trade?", "Chapter five. Exporters are rare.",
             lit={1995: r"Bernard and Jensen"}, scale=("firm", "nation"), horizon=("a year",))
        self.facts()
        self.island()
        self.profits()

    def facts(self):
        F = load("firms")
        cards = point_cards([
            (r"few", rf"exporting plants: \\ {F['bj76']:.1f}\% of US manufacturing \\ plants in 1976, \\ "
                     rf"{F['bj87']:.1f}\% in 1987", FIRM),
            (r"large", r"they made \\ over half \\ of all shipments", ARCH),
            (r"better", r"more productive, \\ more capital-intensive, \\ higher wages, \\ before they export",
             GAIN),
        ], width=12.6, cols=3, font_size=21).move_to(DOWN * 0.1)
        head = label(r"Bernard and Jensen (1995): \ inside the plants", font_size=28, color=E.ACCENT).to_edge(
            UP, buff=0.6)
        tag = published_tag(tables.BERNARD_JENSEN_1995.tag, corner=DR, font_size=12)
        with self.voiceover(
            "Until the 1990s, trade theory talked about countries and industries. Then Andrew Bernard and Bradford "
            "Jensen opened the American census of manufacturing plants. <bookmark mark='a'/> Exporters were rare: "
            f"{F['bj76']:.1f} percent of plants in 1976, {F['bj87']:.1f} percent in 1987. <bookmark mark='b'/> But "
            "they were large, making over half of all shipments. <bookmark mark='c'/> And they were better: more "
            "productive, more capital-intensive, paying higher wages, and they were so before they started to "
            "export. Good firms export; exporting is not what made them good."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abc", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def island(self):
        F = load("firms")
        phi, sales, ex = np.array(F["phi"]), np.array(F["sales"]), np.array(F["exporter"], bool)
        order = np.argsort(phi)
        ax = plane([0, len(phi) + 1], [0, float(np.log10(sales.max())) + 0.3], center=LEFT * 1.6 + DOWN * 0.4,
                   x_length=8.8, y_length=4.6, xticks=[], yticks=[0, 1, 2], ylabel=r"sales (log scale)",
                   xlabel=r"the Island's firms, \ least to most productive", yfmt=lambda v: f"{10 ** v:g}",
                   font_size=14)
        bars = VGroup()
        for k, i in enumerate(order):
            h = float(np.log10(max(sales[i], 1.0)))
            p0, p1 = ax.ax.c2p(k + 0.6, 0), ax.ax.c2p(k + 1.4, max(h, 0.02))
            bars.add(Rectangle(width=max(p1[0] - p0[0], 0.01), height=p1[1] - p0[1],
                               fill_color=ARCH if ex[i] else GREY_B, fill_opacity=0.9, stroke_width=0).move_to(
                (p0 + p1) / 2))
        side = VGroup(
            label(rf"{F['n_alive']} firms survive", font_size=19, color=WHITE),
            label(rf"gold: \ the {100 * F['share_exporters']:.0f}\% \\ that export", font_size=19, color=ARCH),
            label(rf"they sell {100 * F['sales_share_exporters']:.0f}\% \\ of all output", font_size=19,
                  color=ARCH),
            label(rf"{F['size_ratio']:.0f} times larger, \\ {F['prod_ratio']:.2f} times \\ as productive",
                  font_size=19, color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The Island's firms look the same, by construction of the model in the next chapter. "
            f"<bookmark mark='a'/> Of four thousand would-be firms, {F['n_alive']} survive, lined up here from "
            f"least to most productive. <bookmark mark='b'/> Only the most productive "
            f"{100 * F['share_exporters']:.0f} percent export, the gold bars, <bookmark mark='c'/> yet they sell "
            f"{100 * F['sales_share_exporters']:.0f} percent of all output. <bookmark mark='d'/> On average they "
            f"are {F['size_ratio']:.0f} times as large as the firms that sell only at home."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.005), FadeIn(side[0]),
                      run_time=2.5)
            for mk, r_ in zip("bcd", side[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
        self.clear_scene()

    def profits(self):
        M = load("melitz")
        sig, f, fx, tau = M["sigma"], M["f"], M["fx"], M["tau"]
        xt, xx = M["phi_trade"] ** (sig - 1), M["phi_export"] ** (sig - 1)
        A = f / xt
        ax = plane([0, 30], [-2.0, 6.0], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.6, y_length=4.6,
                   xticks=[0, 10, 20, 30], yticks=[-2, 0, 2, 4, 6], xlabel=r"productivity, \ $\varphi^{\sigma - 1}$",
                   ylabel=r"profit", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:+.0f}", font_size=14)
        x = np.linspace(0, 30, 60)
        zero = seg(ax, 0, 0, 30, 0, GREY_B, 1.5, dashed=True)
        pd = path(ax, x, A * x - f, ISLAND, 3.4, smooth=False, yr=(-2.0, 6.0))
        px = path(ax, x, A * tau ** (1 - sig) * x - fx, ARCH, 3.4, smooth=False, yr=(-2.0, 6.0))
        c1, c2 = vline(ax, xt, -2.0, 6.0, ISLAND), vline(ax, xx, -2.0, 6.0, ARCH)
        side = VGroup(
            label(r"teal: \ profit at home: \\ sales, \ less a fixed cost", font_size=17, color=ISLAND),
            label(r"gold: \ profit abroad: \\ shipping shrinks sales, \\ a larger fixed cost", font_size=17,
                  color=ARCH),
            label(r"the two cut-offs sort firms: \\ exit, \ home only, \ export", font_size=17, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Why are exporters so few, and so much better? Draw each firm's profit against its productivity. "
            "<bookmark mark='a'/> At home, profit rises with productivity, less a fixed cost of producing at all: "
            "firms to the left of the teal cut-off lose money and close. <bookmark mark='b'/> Abroad, shipping costs "
            "shrink every sale, and setting up to export costs more again, so the line starts lower and rises more "
            "slowly. <bookmark mark='c'/> Only firms past the gold cut-off make money exporting. The same two lines "
            "explain all of Bernard and Jensen's facts: exporters are rare, because few firms clear the higher bar; "
            "and they are large and productive, because only the large and productive can."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(pd), Create(c1), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(px), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(c2), FadeIn(side[2]))
        self.clear_scene()
