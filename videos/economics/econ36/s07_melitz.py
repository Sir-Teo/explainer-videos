from __future__ import annotations

from videos.economics.econ36.common import *  # noqa: F403


class Melitz(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Melitz: \ selection", r"How can trade raise productivity without any firm improving?",
             "Chapter six. Melitz: selection.", lit={2003: r"Melitz"}, scale=("firm", "nation"),
             horizon=("a decade",))
        self.cutoffs()
        self.gains()

    def cutoffs(self):
        M = load("melitz")
        ax = plane([1.0, 4.0], [0, 1.0], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.8, y_length=4.4,
                   xticks=[1, 2, 3, 4], yticks=[0, 0.5, 1.0], xlabel=r"productivity, \ $\varphi$",
                   ylabel=r"share of would-be firms above $\varphi$", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.1f}", font_size=14)
        x = np.linspace(1, 4, 200)
        surv = path(ax, x, x ** (-M["k"]), FIRM, 3.2)
        va = vline(ax, M["phi_autarky"], 0, 1.0, GREY_B, 2)
        vt = vline(ax, M["phi_trade"], 0, 1.0, TARIFF, 2.5)
        vx = vline(ax, M["phi_export"], 0, 1.0, ARCH, 2.5)
        labs = VGroup(
            label(r"alone: \\ survive", font_size=15, color=GREY_B).next_to(ax.ax.c2p(M["phi_autarky"], 0.9), LEFT,
                                                                            buff=0.08),
            label(r"with trade: \\ survive", font_size=15, color=TARIFF).next_to(ax.ax.c2p(M["phi_trade"], 0.7),
                                                                                 RIGHT, buff=0.08),
            label(r"export", font_size=15, color=ARCH).next_to(ax.ax.c2p(M["phi_export"], 0.5), RIGHT, buff=0.08),
        )
        side = VGroup(
            label(r"a fixed cost to produce, \\ a larger one to export, \\ shipping on top", font_size=17,
                  color=WHITE),
            label(rf"trade raises the bar: \\ {100 * M['exit_share']:.0f}\% of survivors exit", font_size=17,
                  color=TARIFF),
            label(rf"the best {100 * M['export_share']:.0f}\% export \\ and grow", font_size=17, color=ARCH),
            label(rf"average productivity, \\ and real wages, \\ +{100 * M['welfare_gain']:.1f}\%", font_size=18,
                  color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Melitz, \ \emph{Econometrica} 71(6) (2003); \ the Island", corner=DR, font_size=12)
        with self.voiceover(
            "In 2003 Marc Melitz built the model. <bookmark mark='a'/> Firms are born with a random productivity, "
            "drawn here from a Pareto distribution: the curve is the share of would-be firms above each level. "
            "Producing has a fixed cost, so only firms above a cutoff survive. Exporting has a further fixed cost "
            "and shipping costs, so only the best of those export. <bookmark mark='b'/> Now open the economy. "
            "Exporters expand and bid up wages, and the bar for survival rises: "
            f"{100 * M['exit_share']:.0f} percent of the firms that survived alone now exit. "
            f"<bookmark mark='c'/> The best {100 * M['export_share']:.0f} percent export and grow. "
            "<bookmark mark='d'/> No firm has improved, yet output has moved from the weakest firms to the "
            f"strongest, and average productivity, and with it real wages, rise by {100 * M['welfare_gain']:.1f} "
            "percent. Trade raises productivity by killing firms."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(surv), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(va), FadeIn(labs[0]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(vt), FadeIn(labs[1]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(vx), FadeIn(labs[2]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def gains(self):
        M = load("melitz")
        ax = plane([1.0, 2.5], [0, 0.6], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.6, y_length=4.4,
                   xticks=[1.0, 1.5, 2.0, 2.5], yticks=[0, 0.2, 0.4, 0.6], xlabel=r"shipping cost, \ $\tau$",
                   ylabel=r"share", xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        g = path(ax, M["tau_grid"], M["gains"], GAIN, 3.2)
        e = path(ax, M["tau_grid"], M["export_shares"], ARCH, 3.2)
        side = VGroup(
            label(r"green: \ the gain \\ from opening", font_size=18, color=GAIN),
            label(r"gold: \ the share \\ of firms that export", font_size=18, color=ARCH),
            label(r"cheaper shipping: \\ more exporters, \\ more selection, \\ larger gains", font_size=18,
                  color=WHITE),
            label(r"Pavcnik (2002), \ Trefler (2004): \\ plant productivity rose \\ after trade liberalizations",
                  font_size=17, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Melitz (2003); \ Pavcnik, \ \emph{REStud} 69(1) (2002); \ Trefler, \ \emph{AER} "
                            r"94(4) (2004)", corner=DR, font_size=12)
        with self.voiceover(
            "Lower the cost of shipping and both rise. <bookmark mark='a'/> The gain from opening grows <bookmark "
            "mark='b'/> as more firms find it worth exporting <bookmark mark='c'/> and the selection becomes "
            "sharper. <bookmark mark='d'/> The evidence agrees: after Chile's liberalization, Nina Pavcnik found "
            "productivity rose in its import-competing plants, much of it by reallocation; after the Canada-US Free "
            "Trade Agreement, Daniel Trefler found large productivity gains in the Canadian industries that lost "
            "protection, alongside real job losses in them."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(g), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(e), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
