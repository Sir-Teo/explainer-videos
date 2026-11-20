from __future__ import annotations

from videos.economics.econ38.common import *  # noqa: F403


class Demand(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Labour demand and a wage floor", r"What does the competitive model predict?",
             "Chapter four. Labour demand and a wage floor.", lit={1890: r"Marshall", 1932: r"Hicks", 1946: r"Stigler"},
             scale=("firm", "market"),
             horizon=("a year",))
        self.floor()
        self.hicks()

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

    def hicks(self):
        H = load("hicks")
        ax = plane([0, 1], [0, 2.2], center=LEFT * 2.2 + DOWN * 0.6, x_length=7.0, y_length=4.2,
                   xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[0, 0.5, 1.0, 1.5, 2.0],
                   xlabel=r"labour's share of the firm's costs, \ $s$",
                   ylabel=r"elasticity of labour demand \ (absolute value)", xfmt=lambda v: f"{100 * v:.0f}\\%",
                   yfmt=lambda v: f"{v:.1f}", font_size=14)
        cols = (DEMAND, NJ, SUPPLY)
        lines = VGroup(*[path(ax, H["s"], ln, c, 3.2, smooth=False) for ln, c in zip(H["lines"], cols)])
        I = H["island"]
        isl = dot(ax, I["s"], I["eta"], WHITE, 0.09)
        eq = MathTex(r"\eta_{LL} = -\big[(1 - s)\,\sigma + s\,\varepsilon\big]", font_size=34).to_edge(UP, buff=0.35)
        keys = VGroup(*[label(rf"$\sigma$ = {sg:g}, \ $\varepsilon$ = {ep:g}", font_size=18, color=c)
                        for (sg, ep), c in zip(H["cases"], cols)])
        rules = VGroup(
            label(r"$\sigma$: \ how easily machines \\ and other inputs replace workers", font_size=17, color=WHITE),
            label(r"$\varepsilon$: \ how much customers \\ cut back when prices rise", font_size=17, color=WHITE),
            label(r"$s$: \ labour's share of cost \\ (it matters when $\varepsilon > \sigma$)", font_size=17,
                  color=WHITE),
            label(rf"the Island's restaurants: \\ $s$ = {I['s']:.1f}, \ $\sigma$ = {I['sigma']:.1f}, \ "
                  rf"$\varepsilon$ = {I['eps']:.1f} \\ $\Rightarrow$ {I['eta']:.1f}, \ the elasticity above",
                  font_size=17, color=E.ACCENT),
        )
        VGroup(*keys, *rules).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "How elastic is the demand for labour? Alfred Marshall gave rules in 1890, and John Hicks turned them "
            "into a formula in 1932. In a competitive industry with constant returns, the elasticity is a weighted "
            "average of two responses. <bookmark mark='a'/> First, substitution: at a higher wage the firm "
            "replaces some workers with machines or other inputs, as easily as the elasticity of substitution, "
            "sigma, allows, weighted by the share of costs that is not labour. <bookmark mark='b'/> Second, scale: "
            "the higher wage raises the price of the product, customers buy less, as the product's demand "
            "elasticity, epsilon, says, and the firm needs fewer of everything; that weighs as much as labour's "
            "share of costs. <bookmark mark='c'/> So labour demand is most elastic where machines replace people "
            "easily and customers can walk away, and a large labour share matters only when customers are more "
            "sensitive than the technology. <bookmark mark='d'/> On the Island, labour is thirty percent of a "
            "restaurant's costs, and both sigma and epsilon are a half: the elasticity of a half used above."
        ) as vo:
            self.play(Write(eq), FadeIn(ax), FadeIn(tag), FadeIn(rules[0]), Create(lines[0]), FadeIn(keys[0]),
                      run_time=2.0)
            vo.wait_until("a")
            self.play(Indicate(lines[0], color=WHITE, scale_factor=1.0), Indicate(rules[0], color=WHITE))
            vo.wait_until("b")
            self.play(Create(lines[1]), FadeIn(keys[1]), FadeIn(rules[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(lines[2]), FadeIn(keys[2]), FadeIn(rules[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(isl, scale=1.5), FadeIn(rules[3]))
        self.clear_scene()
