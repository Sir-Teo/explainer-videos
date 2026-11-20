from __future__ import annotations

from videos.economics.econ38.common import *  # noqa: F403


class Demand(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Labour demand and a wage floor", r"What does the competitive model predict?",
             "Chapter four. Labour demand and a wage floor.", lit={1946: r"Stigler"}, scale=("firm", "market"),
             horizon=("a year",))
        self.floor()

    def floor(self):
        M = load("market")
        Ls = np.linspace(10, 70, 120)
        w_d = (M["A"] / Ls) ** (1 / M["eps_d"])
        w_s = (Ls / M["B"]) ** (1 / M["eps_s"])
        ax = plane([10, 70], [2, 16], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[10, 20, 30, 40, 50, 60, 70], yticks=[4, 8, 12, 16], xlabel=r"workers",
                   ylabel=r"hourly wage, \ \$", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        dem = path(ax, Ls, w_d, DEMAND, 3.4, yr=(2, 16))
        sup = path(ax, Ls, w_s, SUPPLY, 3.4, yr=(2, 16))
        eq = dot(ax, M["L"], M["w"], WHITE, 0.09)
        m = M["m19"]
        fl = seg(ax, 10, m, 70, m, NJ, 3.0, dashed=True)
        Ld, Ls_ = M["L19"], M["supply_at_m19"]
        dd = dot(ax, Ld, m, DEMAND, 0.09)
        ds = dot(ax, Ls_, m, SUPPLY, 0.09)
        gap = Line(ax.ax.c2p(Ld, m), ax.ax.c2p(Ls_, m), color=LOSS, stroke_width=8, stroke_opacity=0.6)
        side = VGroup(
            label(r"red: \ demand, \ the value \\ of another worker", font_size=18, color=DEMAND),
            label(r"teal: \ supply", font_size=18, color=SUPPLY),
            label(rf"a floor 19\% above \\ the market wage: \\ employment {100 * M['drop19']:.1f}\%", font_size=18,
                  color=NJ),
            label(r"more want work, \\ fewer are hired: \\ unemployment", font_size=18, color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Now the employers. A firm hires another worker as long as that worker adds more to revenue than to cost, "
            "so the demand for labour is the value of the marginal worker, falling as more are hired. "
            "<bookmark mark='a'/> In a competitive market, with many firms and many workers, the wage settles where "
            f"demand meets supply: here {M['w']:.2f} dollars an hour. <bookmark mark='b'/> In 1946 George Stigler "
            "spelled out what a minimum wage above that does. Firms move up their demand curves and hire fewer: with "
            f"a floor nineteen percent higher and a demand elasticity of a half, employment falls about "
            f"{abs(100 * M['drop19']):.0f} percent. <bookmark mark='c'/> More people want work at the higher wage, "
            "so unemployment opens up in between. That is the textbook prediction New Jersey was supposed to confirm, "
            "and its size depends on one number, the elasticity of demand."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(dem), Create(sup), FadeIn(side[0]), FadeIn(side[1]),
                      run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(eq, scale=1.5))
            vo.wait_until("b")
            self.play(Create(fl), FadeIn(dd), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(ds), Create(gap), FadeIn(side[3]))
        self.clear_scene()
