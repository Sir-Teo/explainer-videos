from __future__ import annotations

from videos.economics.econ36.common import *  # noqa: F403


class Krugman(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Variety and scale", r"Why would two identical countries trade?", "Chapter two. Variety and "
             "scale.", lit={1979: r"Krugman", 1980: r"the home-market effect"}, scale=("firm", "world"),
             horizon=("a decade",))
        self.variety()
        self.home()

    def variety(self):
        K = load("krugman")
        cards = point_cards([
            (r"love of variety", r"people value \\ many kinds of a good, \\ not just more of one", CLOTH),
            (r"economies of scale", r"each variety has \\ a fixed cost: \\ one firm makes it", ARCH),
            (r"the limit", rf"a market of {K['L']:.0f} workers \\ supports {K['n']:.0f} varieties", WHITE),
            (r"trade", rf"two such countries: \\ {2 * K['n']:.0f} varieties, \\ real wages "
                       rf"+{100 * K['gain2']:.0f}\%", GAIN),
        ], width=12.8, cols=4, font_size=19).move_to(DOWN * 0.1)
        head = label(r"Krugman (1979, 1980): \ trade between identical countries", font_size=28,
                     color=E.ACCENT).to_edge(UP, buff=0.5)
        foot = label(rf"each firm still sells {K['q']:.0f} units at a markup of {K['markup']:.2f}; \ the gain is in "
                     r"choice", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.7)
        tag = published_tag(r"Krugman, \ \emph{JIE} 9(4) (1979); \ \emph{AER} 70(5) (1980); \ the Island", corner=DR,
                            font_size=12)
        with self.voiceover(
            "In 1979 a young Paul Krugman offered a third reason to trade, which needs no difference between "
            "countries at all. <bookmark mark='a'/> People like variety: not just more cars, but different cars. "
            "<bookmark mark='b'/> But each variety has a fixed cost of design and tooling, so it pays to make each "
            f"in one place, by one firm. <bookmark mark='c'/> A market of {K['L']:.0f} workers on the Island can "
            f"support only {K['n']:.0f} varieties. <bookmark mark='d'/> Put two such islands together and buyers "
            f"in both choose among {2 * K['n']:.0f}. With an elasticity of substitution of {K['sigma']:.0f}, that "
            f"raises real wages by {100 * K['gain2']:.0f} percent, though every firm sells the same amount at the "
            "same markup as before. Each country exports some varieties and imports others of the same good: cars "
            "for cars."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            self.play(FadeIn(foot))
        self.clear_scene()

    def home(self):
        K = load("krugman")
        ax = plane([0.3, 0.7], [0, 1.0], center=LEFT * 1.6 + DOWN * 0.4, x_length=6.6, y_length=4.6,
                   xticks=[0.3, 0.4, 0.5, 0.6, 0.7], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   xlabel=r"the Island's share of world demand", ylabel=r"its share of the industry's firms",
                   xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.2f}", font_size=14)
        diag = seg(ax, 0.3, 0.3, 0.7, 0.7, GREY_B, 1.5, dashed=True)
        hm = path(ax, K["s"], K["hm"], ARCH, 3.5, smooth=False)
        pt = dot(ax, 0.55, K["hm_55"], WHITE, 0.08)
        side = VGroup(
            label(r"dashed: \ firms in proportion \\ to demand", font_size=18, color=GREY_B),
            label(r"gold: \ with shipping costs, \\ the larger market \\ gets more than its share", font_size=18,
                  color=ARCH),
            label(rf"55\% of demand: \\ {100 * K['hm_55']:.0f}\% of the firms", font_size=19, color=WHITE),
            label(r"so the larger country \\ exports the good: \\ demand creates \\ comparative advantage",
                  font_size=18, color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5)
        tag = published_tag(r"Krugman, \ \emph{AER} 70(5) (1980); \ the Island", corner=DR, font_size=12)
        with self.voiceover(
            "Add shipping costs and something else appears. <bookmark mark='a'/> If firms located in proportion "
            "to demand, the line would be the dashed diagonal. <bookmark mark='b'/> In fact the larger market gets "
            "more than its share of the industry, because firms that must pick one place to produce pick the one "
            f"where most of their buyers are. <bookmark mark='c'/> With fifty-five percent of demand, the Island "
            f"has {100 * K['hm_55']:.0f} percent of the firms. <bookmark mark='d'/> So the larger country ends up "
            "exporting the good it most wants. Krugman called it the home-market effect: here demand creates "
            "comparative advantage, rather than the other way round."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(diag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(hm), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(pt, scale=1.5), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
