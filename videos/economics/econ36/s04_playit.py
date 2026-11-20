from __future__ import annotations

from videos.economics.econ36.common import *  # noqa: F403

CHIP = ("#7FD1B9", "#F2C14E", "#E8A0B4")
NAMES = {"PRT": "Portugal", "JPN": "Japan", "BRA": "Brazil"}


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Play it: \ guess the trade", r"Where does Spain sell the most?",
             "Chapter three. Play it: guess the trade.", lit={1962: r"Tinbergen"}, scale=("nation", "world"),
             horizon=("a year",))
        self.choose()
        self.reveal()

    def choose(self):
        P = load("playit")["pairs"]
        cards = point_cards([
            (rf"{ch}: \ {NAMES[c]}", rf"GDP \${P[c]['gdp']:.2f} trillion \\ {P[c]['dist']:,.0f} km from Spain", col)
            for ch, c, col in zip("ABC", ("PRT", "JPN", "BRA"), CHIP)
        ], width=12.0, cols=3, font_size=22).move_to(UP * 0.2)
        q = label(r"in 2019, \ to which did Spain sell the most goods?", font_size=28, color=E.ACCENT).to_edge(
            UP, buff=0.7)
        ring = countdown().scale(0.7).next_to(cards, DOWN, buff=0.5)
        tag = data_tag(r"CEPII Gravity database, \ 2019", corner=DR, font_size=12)
        with self.voiceover(
            "Your turn. In 2019, to which of these three countries did Spain sell the most goods? "
            "<bookmark mark='a'/> Portugal, its small neighbour, with a GDP of a quarter of a trillion dollars; "
            "Japan, twenty times as large and ten thousand kilometres away; or Brazil, nearly eight times as "
            "large, Portuguese-speaking and Latin American. Pause, and choose."
        ) as vo:
            self.play(FadeIn(q), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cards.cards], lag_ratio=0.3), FadeIn(ring),
                      run_time=1.5)
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.clear_scene()

    def reveal(self):
        P = load("playit")["pairs"]
        order = ("PRT", "JPN", "BRA")
        ax = plane([0.4, 3.6], [0, 30], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.0, y_length=4.6, xticks=[],
                   yticks=[0, 10, 20, 30], ylabel=r"Spain's exports, \ 2019, \ \$ billion", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        bars, preds, nms = VGroup(), VGroup(), VGroup()
        for k, (c, col) in enumerate(zip(order, CHIP)):
            p0, p1 = ax.ax.c2p(k + 0.7, 0), ax.ax.c2p(k + 1.3, P[c]["actual"])
            bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=col, fill_opacity=0.85,
                               stroke_width=0).move_to((p0 + p1) / 2))
            preds.add(seg(ax, k + 0.6, P[c]["pred"], k + 1.4, P[c]["pred"], WHITE, 3))
            nms.add(VGroup(label(NAMES[c], font_size=18, color=col),
                           label(rf"\${P[c]['actual']:.1f}bn", font_size=17, color=WHITE)).arrange(DOWN, buff=0.05)
                    .next_to(ax.ax.c2p(k + 1, 0), DOWN, buff=0.12))
        side = VGroup(
            label(r"A: \ Portugal, \ by far", font_size=22, color=CHIP[0]),
            label(r"white bars: \\ what gravity predicts \\ from GDP, \ distance, \\ border and language", font_size=18,
                  color=WHITE),
            label(r"trade $\propto$ \\ size $\times$ size $/$ distance", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        tag = data_tag(r"CEPII Gravity database (BACI), \ 2019; \ this film's gravity fit", corner=DR, font_size=12)
        with self.voiceover(
            f"The answer is A, by far. <bookmark mark='a'/> Spain sold Portugal {P['PRT']['actual']:.0f} billion "
            f"dollars of goods, Japan {P['JPN']['actual']:.1f} billion and Brazil {P['BRA']['actual']:.1f} billion. "
            "A country one twentieth the size of Japan, but next door, buys eight times as much. "
            "<bookmark mark='b'/> The white bars are what one equation predicts from nothing but the two countries' "
            "sizes, the distance between them, whether they share a border and whether they share a language. It "
            "gets all three close. <bookmark mark='c'/> Trade is proportional to the product of the sizes, and "
            "falls with distance. That is gravity."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.3),
                      FadeIn(nms), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(p) for p in preds], lag_ratio=0.3), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()
