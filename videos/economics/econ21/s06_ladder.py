from __future__ import annotations

from videos.economics.econ21.common import *  # noqa: F403


class Ladder(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Creative destruction", r"If each innovation destroys the one before, \ does the market do too "
             r"much research or too little?", "Chapter five. Creative destruction.",
             lit={1942: r"Schumpeter", 1992: r"Aghion and Howitt"}, scale=("firm", "nation"), horizon=("decades",))
        self.ladders()
        self.wedges()
        self.sweep()

    def ladders(self):
        a = load("ah")
        L = a["ladder"]
        t = np.array(L["t"])
        gam = a["params"]["gamma"]
        ax = plane([0, 120], [0, 6 * np.log(gam)], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.6, y_length=4.8,
                   xticks=[0, 30, 60, 90, 120], yticks=[k * np.log(gam) for k in range(0, 7, 2)],
                   xlabel=r"years", ylabel=r"log productivity \ (rungs of $\ln\gamma$)",
                   yfmt=lambda v: f"{v / np.log(gam):.0f}", font_size=16)
        cols = (LIGHT, "#9FB8F2", "#F29E8E", "#7BD88F", "#C9A0FF")
        secs = VGroup(*[path(ax, t, s, color=c, width=2.5, smooth=False).set_stroke(opacity=0.8)
                        for s, c in zip(L["sectors"], cols)])
        mean = path(ax, t, L["mean"], color=WHITE, width=5, smooth=False)
        side = VGroup(
            label(r"each sector climbs by jumps:", font_size=21, color=GREY_A),
            label(rf"an innovation arrives at rate $\lambda n$, \\ and multiplies productivity by $\gamma = {gam:g}$",
                  font_size=19, color=IDEA),
            label(r"the innovator takes the market; \\ the incumbent is destroyed", font_size=19, color=WEDGE),
            label(rf"about {a['ladder']['jumps_per_sector']:.0f} jumps per sector; \\ the average grows smoothly at "
                  rf"$\lambda n \ln\gamma = {pc(L['growth'])}$", font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Aghion and Howitt, Econometrica 60(2) (1992): \ 323--351; \ Schumpeter (1942)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Joseph Schumpeter called capitalism a process of creative destruction: new products and methods "
            "replace old ones, and the firms that made them. In 1992 Philippe Aghion and Peter Howitt turned that "
            "into a growth model. <bookmark mark='a'/> Each industry climbs a quality ladder. Research finds the next "
            "rung at random moments, at a rate proportional to the research done. <bookmark mark='b'/> Each "
            f"innovation multiplies the industry's productivity by gamma, here {gam:g}. <bookmark mark='c'/> The "
            "innovator takes the market, and the incumbent's monopoly is destroyed: that is the destruction. "
            "<bookmark mark='d'/> Each sector's path is a staircase, but the economy is an average over many "
            "sectors, and it grows almost smoothly, at lambda n times the log of gamma: about "
            f"{100 * L['growth']:.0f} percent a year on the island."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(secs[0]), FadeIn(side[0]), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(s) for s in secs[1:]], lag_ratio=0.3), FadeIn(side[2]), run_time=3)
            vo.wait_until("d")
            self.play(Create(mean), FadeIn(side[3]), run_time=2)
        self.clear_scene()

    def wedges(self):
        cards = point_cards([
            (r"appropriability", r"the innovator keeps only a markup: \\ too little research", CONS),
            (r"intertemporal spillover", r"the next innovator builds on yours, \\ free: \ too little research",
             CONS),
            (r"business stealing", r"part of your prize is the incumbent's \\ lost profit: \ too much research",
             WEDGE),
        ], width=12.6, cols=3, font_size=22).move_to(UP * 0.2)
        eq = MathTex(r"\alpha\,(\rho + \lambda n) = \lambda\gamma(1-\alpha)(L-n) \quad\text{against}\quad "
                     r"n^\ast = L - \frac{\alpha\rho}{\lambda\ln\gamma}", font_size=34).to_edge(DOWN, buff=0.8)
        el = label(r"the market's research \ (risk-neutral savers) \quad $\cdot$ \quad a planner's \ (log utility)",
                   font_size=18, color=GREY_B).next_to(eq, DOWN, buff=0.1)
        with self.voiceover(
            "Is there too much research or too little? Three forces pull against each other. "
            "<bookmark mark='a'/> Appropriability: the innovator collects a markup, not the whole gain to society, "
            "as in Romer's model. Too little research. <bookmark mark='b'/> The intertemporal spillover: the next "
            "innovator builds on your rung without paying you. Too little again. <bookmark mark='c'/> But business "
            "stealing pushes the other way. Part of an innovator's prize is not new value at all, it is the profit "
            "the incumbent loses. A step that improves the product only a little can still capture the whole "
            "market. Too much research. <bookmark mark='d'/> Agora solves both: the market's research, where a "
            "researcher's wage equals the expected value of the next patent, and a planner's, who weighs output "
            "now against faster growth."
        ) as vo:
            self.play(FadeIn(cards.cards[0]))
            vo.wait_until("b")
            self.play(FadeIn(cards.cards[1]))
            vo.wait_until("c")
            self.play(FadeIn(cards.cards[2]))
            vo.wait_until("d")
            self.play(Write(eq), FadeIn(el))
        self.clear_scene()

    def sweep(self):
        a = load("ah")
        g = np.array(a["gammas"])
        ax = plane([np.log(1.0), np.log(3.1)], [0, 0.8], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.4,
                   y_length=4.8, xticks=[np.log(v) for v in (1.1, 1.5, 2, 3)], yticks=[0, 0.2, 0.4, 0.6, 0.8],
                   xlabel=r"size of each step, \ $\gamma$ \ (log)", ylabel=r"share of labour in research",
                   xfmt=lambda v: f"{np.exp(v):g}", yfmt=lambda v: f"{v:.1f}", font_size=16)
        dec = path(ax, np.log(g), a["n_dec"], color=IDEA, width=4, smooth=False)
        opt = path(ax, np.log(g), a["n_star"], color=CONS, width=4, smooth=False)
        cx = DashedLine(ax.ax.c2p(np.log(a["cross"]), 0), ax.ax.c2p(np.log(a["cross"]), 0.8), color=GREY_B,
                        stroke_width=2)
        lab = VGroup(label(r"the market", font_size=19, color=IDEA).next_to(ax.ax.c2p(np.log(3.0), a["n_dec"][-1]),
                                                                          DOWN, buff=0.15),
                     label(r"the planner", font_size=19, color=CONS).next_to(ax.ax.c2p(np.log(3.0), a["n_star"][-1]),
                                                                           UP, buff=0.15))
        zones = VGroup(label(r"too much", font_size=19, color=WEDGE).move_to(ax.ax.c2p(np.log(1.12), 0.7)),
                       label(r"too little", font_size=19, color=CONS).move_to(ax.ax.c2p(np.log(2.2), 0.75)))
        s, b = a["small"], a["big"]
        side = VGroup(
            label(rf"$\gamma = 1.2$: \ market {s['n_dec']:.2f}, \ planner {s['n_star']:.2f}", font_size=19,
                  color=WEDGE),
            label(rf"$\gamma = 2.5$: \ market {b['n_dec']:.2f}, \ planner {b['n_star']:.2f}", font_size=19,
                  color=CONS),
            label(rf"they cross near $\gamma = {a['cross']:.2f}$", font_size=19, color=GREY_A),
            label(r"which case holds is an \\ empirical question", font_size=20, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = agora_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Here is the answer across step sizes, with everything else held fixed. <bookmark mark='a'/> The market's "
            "research share, in gold, and the planner's, in green. <bookmark mark='b'/> When each step is small, the "
            "market does research the planner would not do at all: the prize is mostly stolen business. "
            f"<bookmark mark='c'/> When steps are large, spillovers dominate, and the market does too little. Near "
            f"a step of {a['cross']:.2f}, the forces cancel. <bookmark mark='d'/> So theory alone cannot say whether "
            "to subsidize research or tax it. The answer depends on numbers, and those are this part's dial."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(dec), Create(opt), FadeIn(lab), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(zones[0]), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(zones[1]), FadeIn(side[1]), Create(cx), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
