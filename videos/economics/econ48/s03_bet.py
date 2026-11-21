from __future__ import annotations

from videos.economics.econ48.common import *  # noqa: F403


class Bet(VoiceoverScene):
    def construct(self):
        card(self, 2, r"The bet, \ rerun", r"Was Simon right, or lucky?",
             "Chapter two. The bet, rerun.", lit={1980: r"Simon and Ehrlich", 2010: r"Kiel, Matheson and Golembiewski"},
             scale=("market", "world"), horizon=("a decade",))
        self.windows()
        self.verdict()

    def windows(self):
        B = load("bet")
        st, ch = np.array(B["start"]), np.array(B["change"])
        ax = plane([1959, 2016], [-0.7, 3.1], center=LEFT * 1.8 + DOWN * 0.35, x_length=8.4, y_length=4.6,
                   xticks=[1960, 1970, 1980, 1990, 2000, 2010], yticks=[-0.5, 0, 1.0, 2.0, 3.0],
                   xlabel=r"the year the ten-year bet starts",
                   ylabel=r"real change in the bundle's value", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{100 * v:+.0f}\\%".replace("-", "{-}") if v else "0", font_size=14)
        zero = Line(ax.ax.c2p(1959, 0), ax.ax.c2p(2016, 0), color=GREY_B, stroke_width=1.6)
        bars = VGroup()
        for s_, c_ in zip(st, ch):
            p0, p1 = ax.ax.c2p(s_ - 0.38, 0), ax.ax.c2p(s_ + 0.38, c_)
            r = Rectangle(width=p1[0] - p0[0], height=max(abs(p1[1] - p0[1]), 0.01), stroke_width=0,
                          fill_color=LOSS if c_ > 0 else GAIN, fill_opacity=0.9).move_to((p0 + p1) / 2)
            bars.add(r)
        k80 = int(np.where(st == 1980)[0][0])
        ring = SurroundingRectangle(bars[k80], color=WHITE, buff=0.05)
        wins = int(np.sum(ch > 0))
        side = VGroup(
            label(r"copper, \ nickel, \ tin: \\ equal shares, \\ after inflation", font_size=18, color=WHITE),
            label(r"red: \ prices rose, \\ Ehrlich wins", font_size=18, color=LOSS),
            label(r"green: \ prices fell, \\ Simon wins", font_size=18, color=GAIN),
            label(rf"Ehrlich wins {wins} of \\ {B['n']} windows: \\ {100 * B['ehrlich_share']:.0f}\%", font_size=20,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"World Bank, \ the Pink Sheet; \ US CPI (BLS via FRED); \ computed here", corner=DL,
                       font_size=12)
        with self.voiceover(
            "Suppose the bet had been made in another year. Take the three metals with world prices since 1960, "
            "and for every starting year buy equal amounts, then see ten years later whether the bundle is worth "
            f"more or less after inflation. <bookmark mark='a'/> There are {B['n']} such bets, starting from "
            f"{B['first']} to {B['last']}. <bookmark mark='b'/> Red bars are the decades when real prices rose and "
            "Ehrlich would have won; green, when they fell and Simon would have. <bookmark mark='c'/> The real bet "
            f"started in 1980, one of the worst decades for metals: {100 * B['bet_1980']:+.0f} percent. "
            f"<bookmark mark='d'/> Over all the windows, Ehrlich would have won {wins} of {B['n']}: about half. A "
            "ten-year bet on metal prices is close to a coin toss, decided by booms and busts in demand, not by "
            "the slow march of scarcity."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(zero), FadeIn(side[0]), run_time=1.0)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN if c_ > 0 else UP) for b, c_ in zip(bars, ch)],
                                  lag_ratio=0.05), run_time=4.0)
            vo.wait_until("a")
            self.play(Indicate(bars, color=WHITE, scale_factor=1.0))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(Create(ring))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def verdict(self):
        T = tables.BET_1980.data
        cards = point_cards([
            (r"the long run", rf"Kiel, \ Matheson and \\ Golembiewski: \ Ehrlich's \\ five metals, \ "
                              rf"{T['kiel_from']}--{T['kiel_to']}: \\ he wins {T['kiel_share']:.0f}\% \\ of "
                              rf"{T['kiel_n']} decades", METAL),
            (r"Simon's point", r"real prices of metals \\ have not climbed \\ as Hotelling's \\ rent would", GAIN),
            (r"Ehrlich's point", r"in many decades \\ they rose: \\ booms in demand \\ outrun supply", LOSS),
            (r"the deeper point", r"prices work \\ where there are \\ owners and markets: \\ the next chapters "
                                  r"\\ are where there \\ are none", E.ACCENT),
        ], width=12.8, cols=4, font_size=17).move_to(DOWN * 0.2)
        head = label(r"right, \ or lucky?", font_size=32, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.BET_1980.tag, corner=DR, font_size=11)
        with self.voiceover(
            "So who was right? <bookmark mark='a'/> Katherine Kiel, Victor Matheson and Kevin Golembiewski reran "
            f"the bet with Ehrlich's own five metals for every decade from {T['kiel_from']} to {T['kiel_to']}. "
            f"Ehrlich would have won {T['kiel_share']:.0f} percent of them. <bookmark mark='b'/> Simon's deeper "
            "claim survives: over a century the real prices of metals have not climbed the way a scarcity rent "
            "would, because human ingenuity kept adding to what could be extracted. <bookmark mark='c'/> But "
            "Ehrlich was not foolish to bet: in many decades prices rose, when booms in demand outran supply. "
            "<bookmark mark='d'/> And the deeper lesson is about when Simon's mechanism works at all. Metals have "
            "owners, and owners have a reason to save what will be worth more later. Fish in the open sea, and "
            "the air, have no owners. The rest of this part is about them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(Circumscribe(cards.cards[0], color=WHITE, buff=0.05))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
