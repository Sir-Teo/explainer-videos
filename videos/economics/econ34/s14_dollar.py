from __future__ import annotations

from videos.economics.econ34.common import *  # noqa: F403


class Dollar(VoiceoverScene):
    def construct(self):
        card(self, 12, r"The dollar", r"Why does one currency run the world's trade and finance?",
             "Chapter twelve. The dollar.", lit={2013: r"Rey", 2020: r"Gopinath et al."},
             scale=("market", "world"), horizon=("a month", "a decade"))
        self.passthrough()
        self.cycle()
        self.china()

    def passthrough(self):
        Dl = load("dollar")
        cum = -np.array(Dl["pt"]["cumulative"])
        ax = plane([-0.5, 12.5], [0, 1.0], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.6, y_length=4.4,
                   xticks=[0, 3, 6, 9, 12], yticks=[0, 0.25, 0.5, 0.75, 1.0], xlabel=r"months after the dollar moves",
                   ylabel=r"share passed into US import prices \ (excluding fuel)", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.2f}", font_size=14)
        full = seg(ax, -0.5, 1.0, 12.5, 1.0, GREY_C, 1.2, dashed=True)
        ln = path(ax, list(range(13)), cum, USD, 3.5, smooth=False)
        dots = VGroup(*[Dot(ax.ax.c2p(k, v), radius=0.05, color=USD) for k, v in enumerate(cum)])
        side = VGroup(
            label(rf"on impact \ {abs(Dl['pt']['impact']):.2f}; \\ after a year \ {abs(Dl['pt']['long_run']):.2f}",
                  font_size=19, color=USD),
            label(r"most US imports \\ are priced in dollars", font_size=18, color=WHITE),
            label(r"Gopinath, \ Itskhoki and \\ Rigobon (2010): \ 0.25 for \\ goods priced in dollars, \\ 0.95 for "
                  r"the rest", font_size=17, color=DEM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = data_tag(rf"BLS import prices ex fuel; \ the Fed's broad dollar index; \ {Dl['pt_first'][:4]}--"
                       rf"{Dl['pt_last'][:4]}; \ this film's distributed lags", corner=DR, font_size=12)
        with self.voiceover(
            "Most of the world's trade is priced in dollars, even trade that never touches America. Gita Gopinath "
            "and coauthors call it the dominant currency paradigm, and it changes how exchange rates work. "
            "<bookmark mark='a'/> When the dollar rises ten percent, what happens to the dollar prices of what "
            "America imports? Estimated month by month, the answer here is: almost nothing at once, "
            f"{abs(Dl['pt']['impact']):.2f} of the change, and {abs(Dl['pt']['long_run']):.2f} after a year. "
            "<bookmark mark='b'/> Because the prices were set in dollars, the dollar's moves barely reach "
            "American buyers. <bookmark mark='c'/> Gopinath, Oleg Itskhoki and Roberto Rigobon found pass-through of "
            "a quarter for goods priced in dollars and nearly all of it for goods priced in other currencies. The "
            "corollary is uncomfortable for the rest of the world: when a country's currency falls against the "
            "dollar, its imports become dearer at once, but its exports, priced in dollars, do not get cheaper."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(full), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(ln), FadeIn(dots), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def cycle(self):
        Dl = load("dollar")
        ax = plane([1990, 2027], [0, 65], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.8, y_length=4.4,
                   xticks=[1990, 2000, 2010, 2020], yticks=[0, 20, 40, 60], ylabel=r"the VIX, \ monthly average",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        ln = path(ax, Dl["vix_t"], Dl["vix"], CRISIS, 3.0, smooth=False)
        side = VGroup(
            label(r"one global financial cycle: \\ risk appetite, \ credit \\ and capital flows \\ move together",
                  font_size=18, color=WHITE),
            label(r"driven in part by \\ the Fed's policy", font_size=18, color=USD),
            label(r"Rey (2013): \ a dilemma, \\ not a trilemma: \ floating \\ does not insulate you \\ from it",
                  font_size=18, color=DEM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"CBOE, \ via FRED: \ VIXCLS", corner=DR, font_size=12)
        with self.voiceover(
            "The dollar's reach goes beyond trade. <bookmark mark='a'/> Here is a measure of fear on Wall Street, "
            "the VIX. When it rises, capital flows out of emerging markets everywhere at once, credit tightens and "
            "asset prices fall together: one global financial cycle. <bookmark mark='b'/> Helene Rey showed in 2013 "
            "that this cycle moves with the Federal Reserve's policy. <bookmark mark='c'/> Her conclusion was that "
            "the trilemma is really a dilemma: a floating exchange rate does not protect a country from the cycle "
            "if capital moves freely, so the real choice is between open capital markets and control of your own "
            "financial conditions, with the macroprudential tools of Part thirty-three as the middle way."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(ln), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def china(self):
        Dl = load("dollar")
        ax = plane([1994, 2027], [5.5, 9], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.8, y_length=4.4,
                   xticks=[1995, 2000, 2005, 2010, 2015, 2020, 2025], yticks=[6, 7, 8, 9],
                   ylabel=r"yuan per dollar, \ monthly", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        ln = path(ax, Dl["cny_t"], Dl["cny"], CNY, 3.2, smooth=False)
        marks = VGroup(vline(ax, 2005.55, 5.5, 9, GREY_B, 1.5), vline(ax, 2015.6, 5.5, 9, GREY_B, 1.5))
        side = VGroup(
            label(rf"a peg at {Dl['cny_2005']:.2f} \\ until July 2005", font_size=18, color=WHITE),
            label(rf"a managed rise \\ to {Dl['cny_2008']:.2f}, \ held \\ through the crisis", font_size=18,
                  color=CNY),
            label(r"August 2015: \ a small \\ devaluation, \ a large scare", font_size=18, color=GREY_A),
            label(r"the trilemma's third corner: \\ a managed rate, \ its own \\ policy, \ capital controls",
                  font_size=18, color=DEM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Board of Governors (H.10), \ via FRED: \ DEXCHUS", corner=DR, font_size=12)
        with self.voiceover(
            "And the largest currency that does not float. <bookmark mark='a'/> China held the yuan at "
            f"{Dl['cny_2005']:.2f} to the dollar until July 2005, <bookmark mark='b'/> then let it rise slowly, "
            f"to {Dl['cny_2008']:.2f} by 2008, and held it there through the financial crisis. "
            "<bookmark mark='c'/> In August 2015 a small devaluation, under two percent, set off a scare in markets "
            "everywhere, and capital flowed out until controls were tightened. <bookmark mark='d'/> China sits at "
            "the trilemma's third corner: a managed exchange rate and its own monetary policy, bought with limits on "
            "capital. Whether the yuan can rival the dollar depends on giving up those limits, which would mean "
            "giving up one of the other two."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(ln), run_time=2.0)
            for mk, r_ in zip("abcd", side):
                vo.wait_until(mk)
                anims = [FadeIn(r_)]
                if mk == "a":
                    anims.append(FadeIn(marks[0]))
                if mk == "c":
                    anims.append(FadeIn(marks[1]))
                self.play(*anims)
        self.clear_scene()
