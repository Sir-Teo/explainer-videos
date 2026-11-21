from __future__ import annotations

from videos.economics.econ62.common import *  # noqa: F403


class Dispersion(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Productivity dispersion", r"Why do some plants make twice as much from the same inputs, \ and "
             r"why do the laggards survive?", "Chapter one. Productivity dispersion.",
             lit={2004: r"Syverson's concrete", 2011: r"Syverson's survey"}, scale=("firm", "market"),
             horizon=("a decade",))
        self.spread()
        self.competition()

    def spread(self):
        D = load("dispersion")
        bins = np.array(D["bins"])
        mid = (bins[:-1] + bins[1:]) / 2
        entry = np.array(D["entry_hist"], float)
        rows = {r["sigma"]: r for r in D["rows"]}
        r3 = rows[3.0]
        h3 = np.array(r3["hist"], float)
        top = entry.max() * 1.15
        ax = plane([-1.5, 1.5], [0, top], center=LEFT * 3.0 + DOWN * 0.4, x_length=6.4, y_length=4.4,
                   xticks=[-1, 0, 1], yticks=[], xlabel=r"log productivity (TFP)", ylabel=r"plants",
                   xfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0", font_size=14)
        b0 = bars(ax, mid, entry, [GREY_C] * len(mid), width=0.09)
        b1 = bars(ax, mid, h3, [PLANT] * len(mid), width=0.09)
        lo = np.percentile(np.repeat(mid, h3.astype(int)), 10)
        hi = np.percentile(np.repeat(mid, h3.astype(int)), 90)
        v10, v90 = vline(ax, lo, 0, top * 0.9, WHITE, 1.6), vline(ax, hi, 0, top * 0.9, WHITE, 1.6)
        side = VGroup(
            label(r"grey: \ 4,000 plants that try to enter".replace(",", "{,}"), font_size=19, color=GREY_B),
            label(rf"green: \ the {r3['survivors']:,} that cover their costs".replace(",", "{,}"), font_size=19,
                  color=PLANT),
            label(rf"90th percentile over 10th: \ {r3['ratio_90_10']:.2f}", font_size=22, color=WHITE),
            label(r"the same inputs, \ nearly twice the output", font_size=19, color=GREY_A),
            label(r"American manufacturing, \ within narrow industries: \ about 1.92 \ (Syverson)", font_size=19,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if side.width > 6.0:
            side.width = 6.0
            side.to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Syverson, \ Journal of Economic Literature 49(2) (2011); \ the Island: \ "
                            r"agora.org.dispersion", corner=DL, font_size=12)
        with self.voiceover(
            "Start with a fact that surprised economists when plant-level data first arrived. <bookmark "
            "mark='a'/> Take the Island's weaving industry: four thousand plants try to enter, with productivity, "
            "output for given inputs, spread out like this. <bookmark mark='b'/> The ones that survive are those "
            "that can cover their costs. <bookmark mark='c'/> Among the survivors, the plant at the ninetieth "
            f"percentile produces {r3['ratio_90_10']:.2f} times as much as the plant at the tenth from the same "
            "labour, capital and materials. <bookmark mark='d'/> Nearly twice the output, from the same inputs, in "
            "the same industry. <bookmark mark='e'/> That number was planted to match the data: Chad Syverson, "
            "surveying the evidence, reports that within narrowly defined American manufacturing industries the "
            "ninetieth-percentile plant makes on average about 1.92 times as much as the tenth with the same "
            "measured inputs, and the gaps are larger still in China and India."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in b0], lag_ratio=0.03), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in b1], lag_ratio=0.03), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(v10), Create(v90), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def competition(self):
        D = load("dispersion")
        sig = np.array([r["sigma"] for r in D["rows"]])
        rat = np.array([r["ratio_90_10"] for r in D["rows"]])
        ax = plane([1.5, 10.5], [1.0, 3.0], center=LEFT * 3.0 + DOWN * 0.4, x_length=6.2, y_length=4.4,
                   xticks=[2, 4, 6, 8, 10], yticks=[1.0, 1.5, 2.0, 2.5, 3.0],
                   xlabel=r"how easily buyers switch between plants \ (elasticity)", ylabel=r"90/10 productivity "
                   r"ratio of survivors", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", font_size=14)
        curve = path(ax, sig, rat, PLANT, 3.0)
        dots_ = VGroup(*[dot(ax, s_, r_, PLANT, 0.07) for s_, r_ in zip(sig, rat)])
        side = VGroup(
            label(r"when buyers can switch easily, \ sales go to the best plants, \\ and the worst cannot cover "
                  r"their costs", font_size=19, color=WHITE),
            label(rf"easy switching: \ survivors' 90/10 ratio {rat[-1]:.2f}", font_size=20, color=PLANT),
            label(rf"hard switching: \ {rat[0]:.2f}", font_size=20, color=COST),
            label(r"why laggards survive: \ distance, \ loyalty, \ differentiated products, \\ protection, \ and "
                  r"owners content with less", font_size=19, color=GREY_A),
            label(r"Syverson's ready-mixed concrete: \ denser markets, \\ less dispersion and higher average "
                  r"productivity", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if side.width > 6.0:
            side.width = 6.0
            side.to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Syverson, \ Journal of Political Economy 112(6) (2004); \ the Island: \ "
                            r"agora.org.dispersion", corner=DL, font_size=12)
        with self.voiceover(
            "Why do the laggards survive? Part of the answer is competition. <bookmark mark='a'/> When buyers can "
            "switch easily between plants, sales flow to the best ones, and the worst cannot cover their costs. "
            "<bookmark mark='b'/> On the Island, with easy switching, the survivors' ninety-ten ratio falls to "
            f"{rat[-1]:.2f}; <bookmark mark='c'/> when switching is hard, it is {rat[0]:.2f}. <bookmark mark='d'/> "
            "Distance, loyalty, differentiated products, protection from imports, and owners content with less "
            "all let weak plants live. <bookmark mark='e'/> Syverson showed it with ready-mixed concrete, which "
            "cannot travel far before it sets: in denser markets, where buyers have more plants within reach, "
            "productivity is less dispersed and higher on average. But competition explains only part of the gap. "
            "The rest, the next chapters argue, is management."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(curve), LaggedStart(*[FadeIn(d) for d in dots_], lag_ratio=0.2), FadeIn(side[0]),
                      run_time=2.0)
            for k, mk in enumerate("bcde"):
                vo.wait_until(mk)
                self.play(FadeIn(side[1 + k]))
        self.clear_scene()
