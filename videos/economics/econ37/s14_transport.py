from __future__ import annotations

from videos.economics.econ37.common import *  # noqa: F403


class Transport(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Transport", r"What do railways and highways do to places?",
             "Chapter twelve. Transport.", lit={2007: r"Baum-Snow", 2018: r"Donaldson"},
             scale=("city", "nation"), horizon=("a century",))
        self.railways()
        self.highways()
        self.hukou()

    def railways(self):
        TR = load("transport")
        D = TR["donaldson"]
        cards = point_cards([
            (r"trade costs fell", r"and so did the gaps \\ between prices \\ in different districts", ROAD),
            (r"trade rose", r"between districts, \\ and with the world", CITY),
            (r"real income rose", rf"about {D['income']}\% \\ in a district \\ the line reached", GAIN),
            (r"as theory said", r"a trade model's \\ formula for the gains \\ matched the data", E.ACCENT),
        ], width=12.8, cols=4, font_size=20).move_to(DOWN * 0.1)
        head = label(r"the railways of colonial India", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        foot = label(r"the same logic as chapter 2's railway, \ and Part 35's gains from trade", font_size=19,
                     color=GREY_A).to_edge(DOWN, buff=0.6)
        tag = published_tag(tables.DONALDSON_2018.tag, corner=DR, font_size=12)
        with self.voiceover(
            "How much is a railway worth? Dave Donaldson answered for the vast network built in colonial India, "
            "using archival records of prices, trade and harvests district by district. Guided by a model of trade "
            "between districts, he found four things. <bookmark mark='a'/> Railways cut the cost of trade, and the "
            "gaps between prices in different districts shrank. <bookmark mark='b'/> Trade rose, between districts "
            f"and with the world. <bookmark mark='c'/> Real agricultural income rose about {D['income']} percent in "
            "a district once the railway reached it. <bookmark mark='d'/> And the gain was what the trade model's "
            "formula predicted from the change in trade shares, the formula of Parts thirty-five and thirty-six. "
            "<bookmark mark='e'/> Von Thünen's railway, measured."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(Indicate(cards.cards[0], color=WHITE, scale_factor=1.03))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def highways(self):
        TR = load("transport")
        B = TR["bs"]
        ax = plane([0.4, 2.6], [-25, 15], center=LEFT * 3.2 + DOWN * 0.3, x_length=4.8, y_length=4.6, xticks=[],
                   yticks=[-20, -10, 0, 10], ylabel=r"central-city population, \ 1950--1990, \ \%",
                   yfmt=lambda v: f"{v:+.0f}", font_size=14)
        zero = seg(ax, 0.4, 0, 2.6, 0, GREY_B, 1.5)
        vals = ((B["actual"], RENT, r"what happened"), (B["counterfactual"], GAIN, r"without the \\ interstates"))
        bars, nms = VGroup(), VGroup()
        for k, (v, col, n) in enumerate(vals):
            p0, p1 = ax.ax.c2p(k + 0.7, 0), ax.ax.c2p(k + 1.3, v)
            bars.add(Rectangle(width=abs(p1[0] - p0[0]), height=abs(p1[1] - p0[1]), fill_color=col,
                               fill_opacity=0.85, stroke_width=0).move_to((p0 + p1) / 2))
            nms.add(VGroup(label(n, font_size=16, color=col), label(f"{v:+d}\\%", font_size=17, color=WHITE))
                    .arrange(DOWN, buff=0.05).next_to(ax.ax.c2p(k + 1, -25), DOWN, buff=0.1))
        side = VGroup(
            label(rf"each new highway \\ through a central city: \\ {B['per_highway']}\% of its people", font_size=19,
                  color=ROAD),
            label(r"the Island's town, \\ commuting 30\% cheaper:", font_size=19, color=E.AGORA),
            label(rf"living within 8 km: \\ {100 * TR['within8']:.0f}\% $\to$ {100 * TR['within8_hw']:.0f}\%; \\ "
                  rf"edge {TR['edge']:.0f} $\to$ {TR['edge_hw']:.0f} km", font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.6)
        tag = published_tag(tables.BAUM_SNOW_2007.tag + r"; \ the Island", corner=DR, font_size=12)
        with self.voiceover(
            "Highways reshaped American cities. Between 1950 and 1990 the population of central cities "
            f"fell {abs(B['actual'])} percent, while their metropolitan areas grew. <bookmark mark='a'/> Nathaniel "
            "Baum-Snow used the interstate plan of 1947, drawn for other reasons, to predict where highways would "
            "go, and found that each new highway through a central city cut its population by about "
            f"{abs(B['per_highway'])} percent. <bookmark mark='b'/> Without the interstates, central cities would "
            f"have grown about {B['counterfactual']} percent. <bookmark mark='c'/> It is the car of chapter three. "
            f"In the Island's town, commuting thirty percent cheaper moves the share of households within eight "
            f"kilometres of the centre from {100 * TR['within8']:.0f} percent to {100 * TR['within8_hw']:.0f}."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag), GrowFromEdge(bars[0], UP), FadeIn(nms[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[1], DOWN), FadeIn(nms[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.clear_scene()

    def hukou(self):
        F = load("film")
        t_c, v_c = np.array(F["cn_t"]), np.array(F["cn_v"])
        t_w, v_w = np.array(F["t"]), np.array(F["v"])
        keep_c, keep_w = t_c >= 1950, t_w >= 1950
        ax = plane([1950, 2026], [0, 70], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.6, y_length=4.6,
                   xticks=[1950, 1970, 1990, 2010, 2025], yticks=[0, 20, 40, 60],
                   ylabel=r"share living in towns and cities, \ \%", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        lc = path(ax, t_c[keep_c], v_c[keep_c], RENT, 3.4, smooth=False)
        lw = path(ax, t_w[keep_w], v_w[keep_w], E.ACCENT, 2.4, smooth=False)
        c80 = float(np.interp(1980, t_c, v_c))
        c25 = float(np.interp(2025, t_c, v_c))
        side = VGroup(
            label(r"China", font_size=21, color=RENT),
            label(r"the world", font_size=21, color=E.ACCENT),
            label(rf"1980: \ {c80:.0f}\%; \ 2025: \ {c25:.0f}\%", font_size=19, color=WHITE),
            label(r"the hukou: \\ schooling and benefits \\ tied to where \\ you were registered", font_size=18,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5)
        tag = data_tag(r"HYDE 3.5, \ via Our World in Data", corner=DR, font_size=12)
        with self.voiceover(
            "The largest move to the cities in history happened in China. <bookmark mark='a'/> In 1980 about "
            f"{c80:.0f} percent of Chinese lived in towns and cities; by 2025, about {c25:.0f} percent, "
            "<bookmark mark='b'/> catching up with the world. <bookmark mark='c'/> It happened despite the hukou, "
            "a household registration system that ties a family's access to schools, health care and pensions to "
            "the place where it is registered. Hundreds of millions of migrants worked in the cities, often "
            "leaving their children behind in the village. Moving costs, whether made by distance, by highways "
            "or by law, decide how fully people can follow opportunity."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), Create(lc), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(side[2]))
            vo.wait_until("b")
            self.play(Create(lw), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.clear_scene()
