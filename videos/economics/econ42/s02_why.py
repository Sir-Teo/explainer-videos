from __future__ import annotations

from videos.economics.econ42.common import *  # noqa: F403


class Why(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Why markets underinsure, \ and what the state can pool",
             r"What can a government insure that a company cannot?",
             "Chapter one. Why markets underinsure, and what the state can pool.",
             lit={1963: r"Arrow", 1976: r"Rothschild and Stiglitz"}, scale=("person", "nation"),
             horizon=("a year", "a decade"))
        self.pooling()
        self.failures()
        self.reach()

    def pooling(self):
        P = load("pooling")
        n = np.log10(np.array(P["n"]))
        ax = plane([1, 6], [0, 1.0], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[1, 2, 3, 4, 5, 6], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   xlabel=r"members of the pool \ (log scale)",
                   ylabel=r"spread of the claim per member, \ relative to its mean",
                   xfmt=lambda v: f"{10 ** v:,.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        ind = path(ax, n, P["independent"], GAIN, 3.4, yr=(0, 1.0))
        cor = path(ax, n, P["correlated"], LOSS, 3.4, yr=(0, 1.0))
        floor = seg(ax, 1, P["floor"], 6, P["floor"], LOSS, 1.6, dashed=True)
        m = P["marks"]
        side = VGroup(
            label(rf"each member loses their job \\ with chance {100 * P['p_low']:.0f}\% in a normal year, \\ "
                  rf"{100 * P['p_high']:.0f}\% in a recession \\ (one year in seven)", font_size=17, color=GREY_A),
            label(rf"green: \ risks independent; \\ 10,000 members: \ {100 * m['10000']['independent']:.0f}\%",
                  font_size=18, color=GAIN),
            label(rf"red: \ a recession hits \\ everyone at once: \\ never below {100 * P['floor']:.0f}\%",
                  font_size=18, color=LOSS),
            label(r"pooling removes \\ the first kind of risk, \\ not the second", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Insurance works by pooling. <bookmark mark='a'/> On the Island, each worker has a three percent chance "
            "of losing their job in a normal year, and nine percent in a recession, which comes one year in seven. "
            "<bookmark mark='b'/> If job losses were independent, an insurer with ten thousand members would know "
            "almost exactly what it would pay: the spread of the claim per member falls with the square root of "
            f"the pool, to {100 * m['10000']['independent']:.0f} percent of the average at ten thousand. "
            "<bookmark mark='c'/> But unemployment comes in waves. In a recession everyone's risk rises at once, "
            f"and no pool, however large, brings the spread below {100 * P['floor']:.0f} percent of the average. "
            "<bookmark mark='d'/> A private insurer would need enormous reserves for the bad years. A government "
            "can do what a company cannot: borrow in the recession and repay in the boom, spreading the risk across "
            "years and generations."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=1.2)
            vo.wait_until("a")
            self.play(Create(ind), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), Indicate(ind, color=WHITE, scale_factor=1.0))
            vo.wait_until("c")
            self.play(Create(cor), Create(floor), FadeIn(side[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def failures(self):
        cards = point_cards([
            (r"adverse selection", r"those who know they \\ are risky buy most; \\ prices rise, \ the safe \\ leave "
                                   r"(Part 13)", RISK),
            (r"moral hazard", r"the insured take \\ less care, \ or stay \\ unemployed longer", HAZARD),
            (r"common shocks", r"recessions and \\ pandemics hit \\ everyone at once", LOSS),
            (r"risks before birth", r"no one can buy \\ insurance against \\ the family or health \\ they are born "
                                    r"with", HEALTH),
        ], width=12.8, cols=4, font_size=19).move_to(UP * 0.3)
        tools = label(r"the state's tools: \ make everyone join \ $\cdot$ \ borrow across the cycle \ $\cdot$ \ "
                      r"insure behind the veil, \ through taxes", font_size=21, color=GAIN).to_edge(DOWN, buff=0.7)
        head = label(r"why private markets leave risks uninsured", font_size=28, color=E.ACCENT).to_edge(UP,
                                                                                                  buff=0.5)
        tag = published_tag(r"Arrow (1963); \ Rothschild and Stiglitz (1976); \ Part 13", corner=DR, font_size=11)
        with self.voiceover(
            "Kenneth Arrow's 1963 article on medical care began the study of why insurance markets fail. There are "
            "four main reasons. <bookmark mark='a'/> Adverse selection: those who know they are risky buy the most "
            "insurance, prices rise, and the safe drop out, which Part thirteen showed can unravel a market. "
            "<bookmark mark='b'/> Moral hazard: the insured take less care, or search less hard for work. "
            "<bookmark mark='c'/> Common shocks: recessions and pandemics hit everyone at once. "
            "<bookmark mark='d'/> And risks that are settled before anyone can buy cover: no one can insure, before "
            "birth, against the family or the health they will be born with. <bookmark mark='e'/> The state has "
            "tools no company has. It can make everyone join, which ends adverse selection. It can borrow across "
            "the cycle. And through taxes and transfers it can insure people against the luck of the draw, as if "
            "the contract had been signed before anyone knew their lot."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(tools, shift=UP * 0.1))
        self.clear_scene()

    def reach(self):
        C = load("claims")
        ys = np.array(C["years"])
        sh = np.array(C["share"])
        ax = plane([1967, 2027], [0, 0.8], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.8, y_length=4.8,
                   xticks=[1970, 1980, 1990, 2000, 2010, 2020], yticks=[0, 0.2, 0.4, 0.6, 0.8],
                   ylabel=r"continued claims for state unemployment insurance, \ as a share of the unemployed",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        ln = path(ax, ys, sh, UNEMP, 3.2, smooth=False)
        avg = seg(ax, 1967, C["mean"], 2027, C["mean"], GREY_B, 1.6, dashed=True)
        pk = dot(ax, C["peak_y"], C["peak"], LOSS, 0.08)
        side = VGroup(
            label(rf"average since 1967: \\ {100 * C['mean']:.0f}\%", font_size=19, color=GREY_A),
            label(rf"2019: \ {100 * C['y2019']:.0f}\%", font_size=19, color=UNEMP),
            label(rf"{C['peak_y']}: \ {100 * C['peak']:.0f}\%: \\ the pandemic", font_size=19, color=LOSS),
            label(rf"{C['last_y']}: \ {100 * C['last']:.0f}\%", font_size=19, color=UNEMP),
            label(r"the rest: \ not eligible, \\ benefits run out, \\ or never claimed", font_size=18,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"Employment and Training Administration (CCSA) \ and BLS (UNEMPLOY), \ via FRED; \ "
                       r"computed", corner=DR, font_size=11)
        with self.voiceover(
            "America's unemployment insurance is run by the states. How much of the risk does it actually cover? "
            "Divide the number claiming state benefits each week by the number of unemployed counted by the "
            f"household survey. <bookmark mark='a'/> Since 1967 the share has averaged {say_pct(C['mean'], 0)}. "
            f"<bookmark mark='b'/> In 2019, a year of low unemployment, it was {say_pct(C['y2019'], 0)}. "
            f"<bookmark mark='c'/> In {C['peak_y']}, when the pandemic closed whole industries at once, it rose to "
            f"{say_pct(C['peak'], 0)}. <bookmark mark='d'/> In {C['last_y']} it is {say_pct(C['last'], 0)}. "
            "<bookmark mark='e'/> Most of the unemployed draw nothing: they did not work long enough to qualify, "
            "they quit, their benefits ran out, or they never applied. How generous benefits should be, for those "
            "who get them, is the next question."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(ln), run_time=2.5)
            vo.wait_until("a")
            self.play(Create(avg), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(pk, scale=1.5), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
