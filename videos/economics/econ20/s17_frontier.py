from __future__ import annotations

from videos.economics.econ20.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 15, r"Frontier: \ the slowdown, \ and convergence at last", r"Why has growth at the frontier "
             r"slowed since 2005, \ and are poor countries finally catching up?",
             "Chapter fifteen. Frontier: the slowdown, and convergence at last.",
             lit={2015: r"Fernald", 2017: r"Syverson", 2022: r"Kremer, Willis and You"}, scale=("nation", "world"),
             horizon=("decades",))
        self.slowdown()
        self.converging()
        self.dispute()
        self.open_()

    def slowdown(self):
        s = load("slowdown")["periods"]
        ax = plane([-0.5, 3.5], [0, 0.03], center=LEFT * 1.4 + DOWN * 0.4, x_length=8.6, y_length=4.8, xticks=[],
                   yticks=[0, 0.01, 0.02, 0.03], ylabel=r"United States, \ a year", yfmt=lambda v: f"{100 * v:.0f}\\%",
                   font_size=15)
        groups = VGroup()
        for i, (k, v) in enumerate(s.items()):
            g_ = VGroup()
            for j, (key, col) in enumerate((("per_hour", OUTPUT), ("tfp", TFP))):
                h = ax.ax.c2p(0, v[key])[1] - ax.ax.c2p(0, 0)[1]
                r = Rectangle(width=0.55, height=max(h, 0.01), stroke_width=0, fill_color=col,
                              fill_opacity=0.9).move_to(ax.ax.c2p(i - 0.17 + 0.34 * j, 0), aligned_edge=DOWN)
                g_.add(VGroup(r, label(pc(v[key]), font_size=14, color=col).next_to(r, UP, buff=0.05)))
            g_.add(label(k.replace("-", "--"), font_size=16, color=GREY_A).next_to(ax.ax.c2p(i, 0), DOWN, buff=0.15))
            groups.add(g_)
        key_ = VGroup(*[VGroup(Square(0.2, stroke_width=0, fill_color=c, fill_opacity=0.9),
                               label(t, font_size=16, color=c)).arrange(RIGHT, buff=0.1)
                        for t, c in ((r"output per hour", OUTPUT), (r"the residual", TFP))]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).move_to(ax.ax.c2p(0.4, 0.027))
        side = VGroup(
            label(r"the slowdown began before \\ the financial crisis \ (Fernald, \ 2015)", font_size=19,
                  color=GREY_A),
            label(r"is it mismeasurement? \\ free digital goods would need \\ to be worth trillions \\ (Syverson, "
                  r"2017): \ probably not", font_size=19, color=HOLD),
            label(r"ideas getting harder to find? \\ Part 21", font_size=19, color=TFP),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Fernald, NBER Macroeconomics Annual 29 (2015); \ Syverson, JEP 31(2) (2017)",
                            corner=DR, font_size=11)
        src = data_tag(r"Penn World Table 11.0", corner=DL, font_size=11)
        with self.voiceover(
            "Two questions are open at the frontier. The first is the slowdown. <bookmark mark='a'/> Here is "
            "American output per hour and its residual, period by period. Fast growth to 1973, a slowdown, a "
            "decade of revival as information technology spread, and since 2005, a slowdown again, to half a percent "
            "a year of residual. <bookmark mark='b'/> John Fernald showed that it began before the financial crisis, "
            "so the crisis is not the cause. <bookmark mark='c'/> Could the statistics be missing free digital goods? "
            "Chad Syverson calculated that the missing output would have to be worth trillions of dollars, "
            "far more than plausible estimates of what people would pay for those goods. Probably not. "
            "<bookmark mark='d'/> The leading suspect is that ideas are getting harder to find, which is where "
            "part twenty-one begins."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(key_), FadeIn(tag), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(g_, shift=UP * 0.1) for g_ in groups], lag_ratio=0.4), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def converging(self):
        s = load("slowdown")
        roll = s["rolling"]
        xs = [r_["start"] + 5 for r_ in roll]
        ys = [r_["slope"] for r_ in roll]
        lo = [r_["slope"] - 2 * r_["se"] for r_ in roll]
        hi = [r_["slope"] + 2 * r_["se"] for r_ in roll]
        ax = plane([1963, 2015], [-0.012, 0.012], center=LEFT * 1.4 + DOWN * 0.4, x_length=8.8, y_length=4.8,
                   xticks=[1970, 1980, 1990, 2000, 2010], yticks=[-0.01, -0.005, 0, 0.005, 0.01],
                   ylabel=r"slope of 10-year growth on initial log income \ (points)", xlabel=r"middle of the decade",
                   xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: "0" if abs(v) < 1e-12 else f"{100 * v:+.1f}".replace("-", "{-}"), font_size=15)
        zero = DashedLine(ax.ax.c2p(1963, 0), ax.ax.c2p(2015, 0), color=GREY_B, stroke_width=1.5)
        band = Polygon(*[ax.ax.c2p(x, y) for x, y in zip(xs, hi)], *[ax.ax.c2p(x, y) for x, y in
                                                                     zip(xs[::-1], lo[::-1])],
                       stroke_width=0, fill_color=OUTPUT, fill_opacity=0.2)
        line = path(ax, xs, ys, color=OUTPUT, width=4, smooth=False)
        div = label(r"above zero: \ the rich grew faster", font_size=18, color=LABOUR).move_to(
            ax.ax.c2p(1975, 0.0105))
        con = label(r"below zero: \ the poor grew faster", font_size=18, color=CONS).move_to(
            ax.ax.c2p(1985, -0.0105))
        kwy = s["kwy"]
        a20 = s["absolute_2000_2019"]
        side = VGroup(
            label(r"Kremer, \ Willis and You, \ 2022:", font_size=20, color=E.ACCENT),
            label(rf"divergence of about {pc(kwy['diverge_1985_1995'])} a year \\ in 1985--1995", font_size=19,
                  color=LABOUR),
            label(rf"convergence of about {pc(kwy['converge_2005_2015'])} \\ in 2005--2015", font_size=19, color=CONS),
            label(rf"this film, \ 2000--2019: \\ slope ${100 * a20['slope']:.2f}$ points \ (s.e. "
                  rf"{100 * a20['se']:.2f})".replace("-", "{-}"), font_size=19, color=OUTPUT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Kremer, Willis and You, NBER Macroeconomics Annual 36 (2022): \ 337--412", corner=DR,
                            font_size=11)
        with self.voiceover(
            "The second question is the one this part began with. Are poor countries catching up? "
            "<bookmark mark='a'/> Run the absolute convergence regression on every ten-year window since 1960: "
            "growth over the decade against income at its start, for every country with a million people. "
            "<bookmark mark='b'/> Through the 1960s, 70s and 80s the slope is at or above zero: the rich grew as "
            "fast or faster. <bookmark mark='c'/> From the late 1990s it turns negative, and stays there. "
            "<bookmark mark='d'/> Michael Kremer, Jack Willis and Yang You documented exactly this: divergence of "
            "about half a percent a year in the decade to 1995, convergence of about seven tenths of a percent in "
            "the decade to 2015. Growth in poor countries sped up, and growth at the frontier slowed. "
            "<bookmark mark='e'/> And they found that the correlates of growth, schooling, policies and "
            "institutions, have themselves converged, so unconditional convergence is approaching the conditional "
            "kind."
        ) as vo:
            self.play(FadeIn(ax), Create(zero), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(band), Create(line), run_time=3, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(div))
            vo.wait_until("c")
            self.play(FadeIn(con))
            vo.wait_until("d")
            self.play(*[FadeIn(m) for m in side])
            vo.wait_until("e")
            self.play(Indicate(side[2], color=WHITE))
        self.clear_scene()

    def dispute(self):
        rows = VGroup(
            label(r"the critics: \ Daron Acemoglu and Carlos Molina, \ 2022", font_size=25, color=HOLD),
            label(r"give each country its own constant, \ as Islam did, \ and the change in convergence largely "
                  r"disappears", font_size=22, color=GREY_A),
            label(r"so is the world converging, \ or are poor countries converging to their own, \ lower, \ steady "
                  r"states?", font_size=22, color=GREY_A),
            label(r"the same argument as in chapter six, \ thirty years on", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Acemoglu and Molina, \emph{Converging to Converge?} \ NBER Macroeconomics Annual 36 "
                            r"(2022)", corner=DR, font_size=11)
        with self.voiceover(
            "The finding is disputed. <bookmark mark='a'/> In a comment published alongside it, Daron Acemoglu and "
            "Carlos Molina argued that once each country is given its own constant, as in Islam's panels, the "
            "change in the pattern of convergence largely disappears. <bookmark mark='b'/> So the question is "
            "whether the world is converging, or poor countries are converging faster to their own, lower, steady "
            "states. <bookmark mark='c'/> It is chapter six's argument again, thirty years on, and the dial on the "
            "speed of convergence will be reset by whoever settles it."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("abc", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def open_(self):
        cards = point_cards([
            (r"the residual", r"what drives it, \\ and why it slowed", TFP),
            (r"convergence", r"to one steady state, \\ or to many?", OUTPUT),
            (r"the labour share", r"why capital's share rose, \\ and what it does to growth", LABOUR),
            (r"r and g", r"why interest rates fell \\ below growth, \ and for how long", RATE),
        ], width=12.6, cols=2, font_size=23).move_to(DOWN * 0.2)
        head = label(r"open questions", font_size=34, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Four questions for a doctoral student. <bookmark mark='a'/> What drives the residual, and why it slowed. "
            "<bookmark mark='b'/> Whether countries converge to one steady state or to many. "
            "<bookmark mark='c'/> Why capital's share of income rose, and what that does to growth. "
            "<bookmark mark='d'/> And why interest rates fell below growth rates, and whether they will stay there."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
