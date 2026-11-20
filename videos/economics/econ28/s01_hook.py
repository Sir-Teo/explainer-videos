from __future__ import annotations

from videos.economics.econ28.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.address()
        self.decade()
        self.question()
        self.title()
        self.objectives()

    def address(self):
        rows = VGroup(
            label(r"Washington, \ 29 December 1967", font_size=30, color=E.ACCENT),
            label(r"Milton Friedman's presidential address to the American Economic Association", font_size=24,
                  color=GREY_A),
            label(r"the profession steers by a menu: \ a little more inflation buys a little less unemployment",
                  font_size=23, color=CB),
            label(r"``there is always a temporary trade-off between inflation and unemployment; \ there is no "
                  r"permanent trade-off''", font_size=23, color=EXPECT),
            label(r"the menu will vanish once people come to expect the inflation", font_size=24, color=INFL),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Friedman, \ ``The Role of Monetary Policy'', \ AER 58(1) (1968): \ 1--17", corner=DR,
                            font_size=12)
        with self.voiceover(
            "On the twenty-ninth of December 1967, in Washington, Milton Friedman gave his presidential address to "
            "the American Economic Association. <bookmark mark='a'/> Most of his audience believed that a government "
            "could choose from a menu: a little more inflation, and a little less unemployment, for as long as it "
            "liked. <bookmark mark='b'/> Friedman told them that there is always a temporary trade-off between "
            "inflation and unemployment, but no permanent one. <bookmark mark='c'/> Once people came to expect the "
            "inflation, the menu would vanish, and the unemployment would come back."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(rows[1]), FadeIn(tag))
            for mk, r_ in zip("abc", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def decade(self):
        u = load("us")
        ys = np.array(u["years"])
        k = (ys >= 1960) & (ys <= 1982)
        ax = plane([2, 11], [0, 15], center=LEFT * 1.8 + DOWN * 0.3, x_length=8.0, y_length=4.8,
                   xticks=[2, 4, 6, 8, 10], yticks=[0, 5, 10, 15], xlabel=r"unemployment, \ \%",
                   ylabel=r"inflation, \ \%", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=16)
        pts = [(x, y, yr) for x, y, yr in zip(np.array(u["unemployment"])[k], np.array(u["inflation"])[k], ys[k])]
        sixties = VGroup(*[dot(ax, x, y, color=CB, r=0.07) for x, y, yr in pts if yr <= 1969])
        later = VGroup(*[dot(ax, x, y, color=INFL, r=0.07) for x, y, yr in pts if yr > 1969])
        line60 = VMobject(stroke_color=CB, stroke_width=2).set_points_as_corners(
            [ax.ax.c2p(x, y) for x, y, yr in pts if yr <= 1969])
        line70 = VMobject(stroke_color=INFL, stroke_width=2).set_points_as_corners(
            [ax.ax.c2p(x, y) for x, y, yr in pts if yr >= 1969])
        side = VGroup(
            label(r"1960s: \\ a tidy curve, \\ the menu", font_size=21, color=CB),
            label(rf"1969: \ {u['u1969']:.1f}\% unemployed, \\ {u['pi1969']:.1f}\% inflation", font_size=20,
                  color=CB),
            label(rf"1975: \ {u['u1975']:.1f}\% and {u['pi1975']:.1f}\%", font_size=20, color=INFL),
            label(rf"1980: \ {u['u1980']:.1f}\% and {u['pi1980']:.1f}\%", font_size=20, color=INFL),
            label(r"more of both", font_size=24, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).to_edge(RIGHT, buff=0.4)
        tag = data_tag(r"BLS: \ the CPI and the unemployment rate, \ annual averages, \ via FRED", corner=DR,
                       font_size=12)
        with self.voiceover(
            "Here is what happened. America's unemployment rate across the bottom, inflation up the side, one dot "
            "a year. <bookmark mark='a'/> Through the 1960s the dots traced a neat curve: the menu. "
            f"<bookmark mark='b'/> In 1969, unemployment was {u['u1969']:.1f} percent and inflation "
            f"{u['pi1969']:.1f}. <bookmark mark='c'/> Then the curve came apart. By 1975, unemployment was "
            f"{u['u1975']:.1f} percent and inflation {u['pi1975']:.0f}. <bookmark mark='d'/> In 1980, "
            f"{u['u1980']:.1f} percent unemployed with inflation at {u['pi1980']:.1f}. "
            "<bookmark mark='e'/> Within a decade of the address, America had more inflation and more unemployment "
            "than at any time since the war."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.8)
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromCenter(d) for d in sixties], lag_ratio=0.2), Create(line60),
                      FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromCenter(d) for d in later], lag_ratio=0.15), Create(line70),
                      FadeIn(side[2]), run_time=3)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 40, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"why did the menu of the 1960s vanish?", font_size=26, color=INFL),
            label(r"how do people form their expectations, \ and why do they matter so much?", font_size=26,
                  color=EXPECT),
            label(r"and how do you bring inflation down once everyone expects it?", font_size=26, color=CB),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "This part's question: can a country buy lower unemployment with higher inflation? "
            "<bookmark mark='a'/> Why did the menu of the 1960s vanish? <bookmark mark='b'/> How do people form "
            "their expectations of inflation, and why do those expectations matter so much? "
            "<bookmark mark='c'/> And how do you bring inflation down once everyone expects it?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        p = load("phillips")
        mini = plane([1, 11], [-1, 6], x_length=4.2, y_length=1.6)
        a = load("accelerate")
        logo = VGroup(path(mini, p["u"], p["w"], CB, width=3, yr=(-1, 6)),
                      seg(mini, 5, -1, 5, 6, INFL, width=3))
        t = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 28 \ $\cdot$ \ Inflation and Expectations", font_size=34, color=E.ACCENT)
        VGroup(logo, t, sub).arrange(DOWN, buff=0.45)
        del a
        with self.voiceover("Economics, Built. Part twenty-eight: inflation and expectations."):
            self.play(Create(logo), run_time=1.6)
            self.play(Write(t), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act VI \ $\cdot$ \ Money and the Cycle", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"Phillips's curve; \ forecast inflation yourself; \ the natural rate",
            r"the Great Inflation; \ adaptive and rational expectations",
            r"Lucas's islands and his critique; \ the inflation bias as a game",
            r"Volcker's disinflation; \ the fixes: \ conservative bankers, \ independence, \ targets",
            r"the flat curve; \ 2021--23; \ two dials; \ forecasting; \ how people really form expectations",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "Here is the plan. <bookmark mark='a'/> Phillips's curve, a forecast for you to make, and Friedman's "
            "natural rate. <bookmark mark='b'/> The Great Inflation, and two ways of modelling expectations. "
            "<bookmark mark='c'/> Lucas's islands, his critique of policy models, and inflation as a game a central "
            "bank cannot win. <bookmark mark='d'/> How Volcker ended the inflation, at what cost, and the "
            "institutions built to stop it returning. <bookmark mark='e'/> And the flat curve of the 2000s, the "
            "surge of 2021, two dials, the forecaster's job, and what surveys say about how people actually form "
            "expectations."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
