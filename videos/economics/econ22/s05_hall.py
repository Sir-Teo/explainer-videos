from __future__ import annotations

from videos.economics.econ22.common import *  # noqa: F403


class Hall(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Hall's random walk", r"If households plan ahead, \ can anything known today predict how their "
             r"spending will change?", "Chapter four. Hall's random walk.", lit={1978: r"Hall", 1960: r"Working"},
             scale=("household", "nation"), horizon=("a quarter",))
        self.walk()
        self.test()
        self.averaging()

    def walk(self):
        rows = VGroup(
            history_card(1978, r"Robert Hall", r"\emph{Stochastic Implications of the Life Cycle--Permanent Income "
                         r"Hypothesis}, \ Journal of Political Economy", color=INCOME, width=11.4, font_size=22),
            MathTex(r"\mathbb{E}_t\, c_{t+1} = c_t \quad\Longrightarrow\quad c_{t+1} = c_t + "
                    r"\varepsilon_{t+1}, \qquad \mathbb{E}_t\,\varepsilon_{t+1} = 0", font_size=42, color=SPEND),
            label(r"consumption is a random walk: \ its change is news, \ and news cannot be forecast", font_size=24,
                  color=GREY_A),
            label(r"so nothing known at $t$ \ (past income, \ an announced cheque) \ should predict $\Delta c_{t+1}$",
                  font_size=24, color=E.ACCENT),
            label(r"Hall's own test, \ post-war US data: \ lagged income added nothing; \ lagged stock prices did "
                  r"help", font_size=21, color=GREY_B),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Hall, JPE 86(6) (1978): \ 971--987", corner=DR, font_size=12)
        with self.voiceover(
            "In 1978 Robert Hall turned the Euler equation into a prediction anyone could test. "
            "<bookmark mark='a'/> If the household plans so that it expects tomorrow's consumption to equal "
            "today's, then whatever it actually consumes tomorrow differs from today only by a surprise, an error "
            "with mean zero given everything known today. <bookmark mark='b'/> Consumption is a random walk. Its "
            "change is news, and news cannot be forecast. <bookmark mark='c'/> So nothing known today, not past "
            "income, not a cheque whose date was announced, should predict how consumption changes next. You don't "
            "need to know the household's income process, its wealth or its preferences to test that. You only "
            "need a regression. <bookmark mark='d'/> Hall's own test, on post-war American data, found that lagged "
            "income added nothing. Lagged stock prices did help, a little."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def test(self):
        h = load("hall")
        ax = plane([0.5, 3.5], [-0.05, 0.2], center=LEFT * 2.2 + DOWN * 0.5, x_length=6.6, y_length=4.6,
                   xticks=[1, 2, 3], yticks=[0, 0.05, 0.1, 0.15, 0.2], ylabel=r"coefficient",
                   xfmt=lambda v: rf"\Delta y_{{t-{int(v) + 1}}}", yfmt=lambda v: f"{v:.2f}", font_size=17)
        bars = VGroup()
        for k, (b, se) in enumerate(zip(h["lags"], h["lag_se"])):
            x = k + 1
            bar = Rectangle(width=ax.ax.c2p(x + 0.25, 0)[0] - ax.ax.c2p(x - 0.25, 0)[0],
                            height=ax.ax.c2p(0, b)[1] - ax.ax.c2p(0, 0)[1], stroke_width=0, fill_color=INCOME,
                            fill_opacity=0.8).move_to(ax.ax.c2p(x, b / 2))
            err = Line(ax.ax.c2p(x, b - 2 * se), ax.ax.c2p(x, b + 2 * se), color=WHITE, stroke_width=3)
            val = label(f"{b:.2f}", font_size=18, color=INCOME).next_to(err, UP, buff=0.08)
            bars.add(VGroup(bar, err, val))
        zero = seg(ax, 0.5, 0, 3.5, 0, color=GREY_B, width=2)
        eq = MathTex(r"\Delta c_t = a + b_2\,\Delta y_{t-2} + b_3\,\Delta y_{t-3} + b_4\,\Delta y_{t-4} + "
                     r"\varepsilon_t", font_size=32).to_edge(UP, buff=0.45)
        side = VGroup(
            label(rf"US, \ {h['n']} quarters, \ {h['first']:.0f}--{int(h['last'])}", font_size=20, color=GREY_A),
            label(r"$c$: \ real spending on nondurables \\ and services; \ $y$: \ real disposable \\ income; \ "
                  r"changes in logs", font_size=18, color=GREY_B),
            label(r"Hall says: \ every $b$ is zero", font_size=21, color=SPEND),
            label(rf"joint test: \ $F = {h['F']:.1f}$ \\ (1\% critical value {h['F_crit_1pc']:.1f}; \ "
                  rf"$p = {h['p']:.4f}$)", font_size=20, color=HOLD),
            label(r"income from six months to a year ago \\ predicts spending today", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"BEA via FRED, \ quarterly averages of monthly data; \ bars: \ $\pm 2$ s.e.", corner=DR,
                       font_size=12)
        with self.voiceover(
            "So run it. <bookmark mark='a'/> Take sixty years of American quarters, from 1960 to the end of 2019, "
            "before the pandemic's swings. Consumption here is real spending on nondurable goods and services, the "
            "part of spending that is used up as it is bought. Income is real disposable income. "
            "<bookmark mark='b'/> Regress the growth of consumption on the growth of income two, three and four "
            "quarters earlier. Hall says every coefficient is zero. <bookmark mark='c'/> They are "
            f"{h['lags'][0]:.2f}, {h['lags'][1]:.2f} and {h['lags'][2]:.2f}, each with a standard error of about "
            "0.03. <bookmark mark='d'/> Together, an F statistic of "
            f"{h['F']:.1f}, against a one percent critical value of {h['F_crit_1pc']:.1f}. "
            "<bookmark mark='e'/> Income growth from six months to a year ago predicts consumption growth today. "
            "Some of the income households could see coming, they spent only when it came."
        ) as vo:
            self.play(FadeIn(eq), FadeIn(ax), FadeIn(zero), FadeIn(tag), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b_[0], DOWN) for b_ in bars], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(b_[1]) for b_ in bars], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(b_[2]) for b_ in bars], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def averaging(self):
        h = load("hall")
        rows = VGroup(
            label(r"why leave out last quarter's income?", font_size=27, color=E.ACCENT),
            label(r"the data are averages over each quarter, \ and averaging a random walk makes its changes "
                  r"predictable", font_size=23, color=GREY_A),
            MathTex(r"\text{three months averaged:}\quad \operatorname{corr}(\Delta \bar c_t, \Delta \bar c_{t-1}) "
                    r"= \frac{m^2 - 1}{2(2m^2+1)} = " + f"{h['working']:.2f}", font_size=36),
            label(r"Holbrook Working, \ 1960: \ a statistical artefact, \ not a failure of the theory", font_size=22,
                  color=GREY_B),
            label(rf"in the data the correlation is {h['own_lag']:.2f}, \ more than averaging explains; \ "
                  r"so the lags start at two", font_size=23, color=HOLD),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        with self.voiceover(
            "One detail matters here, and it is the kind that trips up careful people. <bookmark mark='a'/> Why "
            "leave out last quarter's income? Because the data are averages. The national accounts report spending "
            "over each quarter, not at an instant, and the average of a random walk over a quarter has changes "
            "that are correlated with each other. <bookmark mark='b'/> Averaging three months, the correlation of "
            f"successive changes is {h['working']:.2f}, with no failure of the theory at all. "
            "<bookmark mark='c'/> Holbrook Working pointed this out in 1960. Any variable from the quarter just "
            "before shares in that artefact, so a clean test starts at the second lag. <bookmark mark='d'/> In the "
            f"data the correlation is {h['own_lag']:.2f}, more than averaging can explain: spending itself moves "
            "more slowly than a random walk."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
