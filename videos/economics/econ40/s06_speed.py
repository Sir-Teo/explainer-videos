from __future__ import annotations

from videos.economics.econ40.common import *  # noqa: F403


class Speed(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Why the tail moved so fast", r"Can random growth explain the 1980s?",
             "Chapter five. Why the tail moved so fast.", lit={2016: r"Gabaix, \ Lasry, \ Lions and Moll"},
             scale=("person", "nation"), horizon=("a decade",))
        self.race()
        self.fixes()

    def race(self):
        S = load("speed")
        t = np.array(S["t"])
        ax = plane([0, 50], [0, 24], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.8, y_length=4.8,
                   xticks=[0, 10, 20, 30, 40, 50], yticks=[0, 5, 10, 15, 20],
                   xlabel=r"years after the change \ (America: \ years after 1975)",
                   ylabel=r"top 1\% share of income", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}\\%",
                   font_size=14)
        m = t <= 50
        lp = path(ax, t[m], 100 * np.array(S["pure"])[m], PURE, 3.4)
        lt = path(ax, t[m], 100 * np.array(S["types"])[m], TYPES, 3.4)
        us = VGroup(*[dot(ax, y - 1975, v, DATA, 0.05) for y, v in zip(S["us_years"], S["us_top1"])
                      if y - 1975 <= 50])
        side = VGroup(
            label(r"gold dots: \ America, \\ Piketty and Saez", font_size=18, color=DATA),
            label(rf"grey: \ pure random growth, \\ volatility up; \ half the \\ change takes "
                  rf"{S['hl_pure']:.0f} years", font_size=18, color=PURE),
            label(r"Gabaix, \ Lasry, \ Lions and \\ Moll (2016): \ the standard \\ model is far too slow",
                  font_size=17, color=GREY_A),
            label(rf"red: \ a few high-growth \\ types grow faster; \\ half the change in "
                  rf"{S['hl_types']:.0f} years", font_size=18, color=TYPES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Random growth explains the shape of the tail. Can it explain how fast the tail changed? "
            "<bookmark mark='a'/> In America, the top one percent's share more than doubled between the late 1970s "
            "and the mid 2000s. <bookmark mark='b'/> On the Island, raise the volatility of incomes enough to move the "
            "top share from about seven percent to twenty, and watch the Kolmogorov equation carry the distribution "
            "to its new state. It crawls: half of the change in the log of the top share takes "
            f"{S['hl_pure']:.0f} years, because the tail fills only as careers that began long ago drift upward. "
            "<bookmark mark='g'/> In 2016 Xavier Gabaix, Jean-Michel Lasry, Pierre-Louis Lions and Benjamin Moll "
            "showed that the standard "
            "model is far too slow. <bookmark mark='c'/> Their repair: let a few people be high-growth types, a "
            "founder, a star, whose income grows fast for a while before they become ordinary. Make those types grow "
            "faster, and the top share moves in time with the data: half of the change in "
            f"{S['hl_types']:.0f} years."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(us, lag_ratio=0.05), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), Indicate(us, color=WHITE, scale_factor=1.05))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), run_time=0.8)
            self.play(Create(lp), run_time=8.0, rate_func=linear)
            vo.wait_until("g")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(Create(lt), FadeIn(side[3]), run_time=3.0)
        self.clear_scene()

    def fixes(self):
        S = load("speed")
        cards = point_cards([
            (r"scale dependence", r"growth rates that rise \\ with income: \ stars \\ reach bigger markets \\ "
                                  r"(Part 39's superstars)", TOP),
            (r"type dependence", rf"high-growth types: \\ founders, \ managers; \\ their tail exponent \\ "
                                 rf"{S['zeta_h'][0]:.1f} $\to$ {S['zeta_h'][1]:.1f}", TYPES),
            (r"what to look for", r"top earners' income \\ growth, \ year to year, \\ in panel tax data", MIDDLE),
        ], width=12.6, cols=3, font_size=20).move_to(DOWN * 0.1)
        head = label(r"two ways to make the tail move fast", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.GLLM_2016.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Gabaix and his coauthors found two ways to speed the model up. <bookmark mark='a'/> Scale dependence: "
            "growth rates that rise with income itself, as when the best performers reach ever larger markets, the "
            "superstars of Part thirty-nine. <bookmark mark='b'/> Type dependence: a group whose incomes grow fast "
            "for a time, as in theories of superstar entrepreneurs and managers. On the Island, speeding up the "
            "high-growth types moves their own tail exponent from "
            f"{S['zeta_h'][0]:.1f} to {S['zeta_h'][1]:.1f}. <bookmark mark='c'/> The two differ in what they predict "
            "for the growth of top incomes, year by year, which is why the question moved to panel data that follow "
            "the same top earners over time."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abc", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
