from __future__ import annotations

from videos.economics.econ35.common import *  # noqa: F403


class Stolper(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Stolper and Samuelson: \ losers inside", r"If the country gains, why do some of its people "
             r"lose?", "Chapter six. Stolper and Samuelson: losers inside.", lit={1941: r"Stolper and Samuelson"},
             scale=("household", "nation"), horizon=("a decade",))
        self.curves()
        self.magnify()
        self.who()

    def curves(self):
        S = load("stolper")
        ax = plane([0.7, 1.4], [0, 1.2], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.4, y_length=4.6,
                   xticks=[0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4], yticks=[0, 0.4, 0.8, 1.2],
                   xlabel=r"the price of cloth \ (machines' price fixed)", ylabel=r"factor prices",
                   xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}", font_size=14)
        w = path(ax, S["grid"], S["w"], LABOUR, 3.5, yr=(0, 1.2))
        r = path(ax, S["grid"], S["r"], CAPITAL, 3.5, yr=(0, 1.2))
        side = VGroup(
            label(r"teal: \ the wage", font_size=19, color=LABOUR),
            label(r"gold: \ the rent on capital", font_size=19, color=CAPITAL),
            label(r"zero profits in both goods: \\ a dearer labour-intensive good \\ must pay labour more \\ and "
                  r"capital less", font_size=18, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Stolper and Samuelson, \ \emph{RES} 9(1) (1941); \ the Island's technologies",
                            corner=DR, font_size=12)
        with self.voiceover(
            "In 1941 Wolfgang Stolper and Paul Samuelson asked who gains from trade inside a country. "
            "<bookmark mark='a'/> Hold the price of machines fixed and raise the price of cloth, the labour-intensive "
            "good. The wage rises, <bookmark mark='b'/> and the rent on capital falls. <bookmark mark='c'/> It has "
            "to: both goods must still just cover their costs, and cloth's costs are mostly wages, so for cloth to "
            "earn exactly its higher price while machines earn the same old one, labour must get more and capital "
            "less."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(w), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(r), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def magnify(self):
        S = load("stolper")
        vals = [("cloth's price", 10.0, CLOTH), ("machines' price", 0.0, GREY_B), ("the wage", 100 * S["dw"], LABOUR),
                ("the rent", 100 * S["dr"], CAPITAL)]
        ax = plane([0.4, 4.6], [-10, 20], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.6, y_length=4.6, xticks=[],
                   yticks=[-10, 0, 10, 20], ylabel=r"percent change", yfmt=lambda v: f"{v:+.0f}\\%" if v else "0",
                   font_size=14)
        zero = seg(ax, 0.4, 0, 4.6, 0, GREY_B, 1.5)
        bars, labs = VGroup(), VGroup()
        for k, (nm, v, col) in enumerate(vals):
            p0, p1 = ax.ax.c2p(k + 0.65, 0), ax.ax.c2p(k + 1.35, v if v else 0.15)
            bars.add(Rectangle(width=p1[0] - p0[0], height=abs(p1[1] - p0[1]), fill_color=col, fill_opacity=0.85,
                               stroke_width=0).move_to((p0 + p1) / 2))
            labs.add(VGroup(label(tex_safe(nm), font_size=16, color=col),
                            label(f"{v:+.1f}\\%", font_size=17, color=col)).arrange(DOWN, buff=0.05).next_to(
                ax.ax.c2p(k + 1, -10), DOWN, buff=0.12))
        side = VGroup(
            label(r"the magnification effect: \\ the wage rises more \\ than any price", font_size=18, color=LABOUR),
            label(r"so workers are better off \\ in cloth and in machines; \\ capital owners worse off \\ in both",
                  font_size=18, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The effect is magnified. <bookmark mark='a'/> Raise the price of cloth by ten percent, leaving machines "
            f"alone. <bookmark mark='b'/> The wage rises by {100 * S['dw']:.0f} percent, more than either price, "
            f"<bookmark mark='c'/> and the rent falls by {abs(100 * S['dr']):.0f} percent. <bookmark mark='d'/> So "
            "workers can buy more of both goods, and capital owners less of both, whatever they like to consume. "
            "There is no ambiguity about who wins."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0], DOWN), FadeIn(labs[0]), FadeIn(bars[1]), FadeIn(labs[1]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[2], DOWN), FadeIn(labs[2]), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[3], UP), FadeIn(labs[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[1]))
        self.clear_scene()

    def who(self):
        H = load("ho")
        I, A = H["island"], H["arch"]
        ch = [("the Island's workers", H["w"] / I["aut_w"] - 1, ISLAND),
              ("the Island's capital", H["r"] / I["aut_r"] - 1,
                                                                         ISLAND),
              ("the Archipelago's workers", H["w"] / A["aut_w"] - 1, ARCH),
              ("the Archipelago's capital", H["r"] / A["aut_r"] - 1, ARCH)]
        ax = plane([0.4, 4.6], [-50, 60], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.6, y_length=4.6, xticks=[],
                   yticks=[-40, -20, 0, 20, 40, 60], ylabel=r"change in the factor's price, \ autarky to trade, \ in "
                   r"cloth", yfmt=lambda v: f"{v:+.0f}\\%" if v else "0", font_size=14)
        zero = seg(ax, 0.4, 0, 4.6, 0, GREY_B, 1.5)
        bars, labs = VGroup(), VGroup()
        for k, (nm, v, col) in enumerate(ch):
            v = 100 * v
            p0, p1 = ax.ax.c2p(k + 0.65, 0), ax.ax.c2p(k + 1.35, v)
            bars.add(Rectangle(width=p1[0] - p0[0], height=abs(p1[1] - p0[1]), fill_color=GAIN if v > 0 else TARIFF,
                               fill_opacity=0.85, stroke_width=0).move_to((p0 + p1) / 2))
            labs.add(VGroup(wrapped_label(tex_safe(nm), 1.8, 15, col), label(f"{v:+.0f}\\%", font_size=17,
                                                                             color=WHITE)).arrange(DOWN, buff=0.05))
            labs[-1].next_to(bars[-1], UP if v > 0 else DOWN, buff=0.08)
        side = VGroup(
            label(r"opening to trade: \\ each country's abundant factor \\ gains, \ its scarce factor \\ loses",
                  font_size=18, color=WHITE),
            label(r"the country gains; \\ not everyone in it", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"the Island; \ Scheve and Slaughter, \ \emph{JIE} 54(2) (2001)", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Now open the two economies to each other. <bookmark mark='a'/> On the Island, where labour is "
            "abundant, trade raises the price of cloth, its export: workers gain and capital owners lose. "
            "<bookmark mark='b'/> In the Archipelago it is the other way round: its workers lose to the Island's "
            "competition and its capital owners gain. <bookmark mark='c'/> That is the theorem's political "
            "content: trade makes a country richer and, in this model, makes its scarce factor poorer, "
            "unambiguously. Surveys in rich countries, where less-skilled labour is the scarce factor, find what the "
            "theorem suggests: less-skilled workers are more likely to favour limits on imports than skilled ones."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0], DOWN), GrowFromEdge(bars[1], UP), FadeIn(labs[0]), FadeIn(labs[1]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[2], UP), GrowFromEdge(bars[3], DOWN), FadeIn(labs[2]), FadeIn(labs[3]))
            vo.wait_until("c")
            self.play(FadeIn(side))
        self.clear_scene()
