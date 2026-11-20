from __future__ import annotations

from videos.economics.econ23.common import *  # noqa: F403


class Repairs(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Three repairs: \ habits, \ long-run risk, \ disasters", r"What would people have to fear for "
             r"the premium to make sense?", "Chapter nine. Three repairs: habits, long-run risk, disasters.",
             lit={1988: r"Rietz", 1999: r"Campbell and Cochrane", 2004: r"Bansal and Yaron", 2006: r"Barro"},
             scale=("market", "nation"), horizon=("a century",))
        self.habits()
        self.longrun()
        self.disasters()

    def habits(self):
        h = load("habit")
        t = np.arange(1, len(h["S"]) + 1)
        a1 = plane([0, 100], [0, 0.12], center=UP * 1.35 + LEFT * 1.6, x_length=8.4, y_length=2.4,
                   xticks=[0, 25, 50, 75, 100], yticks=[0, 0.05, 0.10], ylabel=r"surplus ratio $S = (C - X)/C$",
                   xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", font_size=14)
        a2 = plane([0, 100], [0, 1.2], center=DOWN * 2.0 + LEFT * 1.6, x_length=8.4, y_length=2.4,
                   xticks=[0, 25, 50, 75, 100], yticks=[0, 0.5, 1.0], xlabel=r"years \ (simulated)",
                   ylabel=r"price of risk \ (maximum Sharpe ratio)", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}",
                   font_size=14)
        s_line = path(a1, t, h["S"], color=CONS, width=3, smooth=False)
        p_line = path(a2, t, h["price_of_risk"], color=RISK, width=3, smooth=False)
        stocks = seg(a2, 0, 0.3, 100, 0.3, color=STOCK, width=2, dashed=True)
        side = VGroup(
            label(r"John Campbell and \\ John Cochrane, \ 1999", font_size=21, color=E.ACCENT),
            label(r"utility from consumption \\ above a habit $X$ that \\ follows past consumption", font_size=18,
                  color=GREY_A),
            label(r"near the habit, \ a small \\ fall in consumption \\ hurts enormously", font_size=18, color=RISK),
            label(rf"price of risk: \ {h['steady_price']:.2f} at the \\ average, \ up to "
                  rf"{max(h['price_of_risk']):.2f} in bad times", font_size=18, color=RISK),
            label(r"stocks' Sharpe ratio: \ 0.3", font_size=18, color=STOCK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Campbell and Cochrane, JPE 107(2) (1999): \ 205--251", corner=DR, font_size=12)
        with self.voiceover(
            "If the data are right, people must fear something the simple model leaves out. There are three "
            "leading answers. <bookmark mark='a'/> The first is habit. John Campbell and John Cochrane let people "
            "care about consumption above a habit level that follows their own past consumption. "
            "<bookmark mark='b'/> What matters is the surplus, the share of consumption above the habit, which "
            "wanders with luck: here a century of it, simulated with their calibration. <bookmark mark='c'/> When the "
            "surplus is thin, a small fall in consumption is felt as a disaster, and the price of risk soars: "
            f"{h['steady_price']:.2f} at the average surplus, up to {max(h['price_of_risk']):.2f} after bad "
            "years. Stocks' Sharpe ratio of 0.3 fits comfortably inside. <bookmark mark='d'/> The premium then "
            "rises in recessions and falls in booms, which is also why, as chapter ten shows, returns are "
            "predictable over long horizons."
        ) as vo:
            self.play(FadeIn(a1), FadeIn(a2), FadeIn(tag), FadeIn(side[0]), Create(s_line), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Indicate(s_line, color=WHITE))
            vo.wait_until("c")
            self.play(Create(p_line), FadeIn(stocks), FadeIn(side[2]), FadeIn(side[3]), FadeIn(side[4]), run_time=2.5)
            vo.wait_until("d")
            self.play(Indicate(side[3], color=WHITE))
        self.clear_scene()

    def longrun(self):
        rows = VGroup(
            label(r"the second: \ long-run risk \ (Ravi Bansal and Amir Yaron, \ 2004)", font_size=26, color=E.ACCENT),
            MathTex(r"\Delta \ln c_{t+1} \;=\; \mu + x_t + \sigma\,\eta_{t+1}, \qquad x_{t+1} = \rho\,x_t + "
                    r"\varphi_e\,\sigma\,e_{t+1}", font_size=38, color=CONS),
            label(r"a small, \ very persistent component of growth, \ almost invisible in a few decades of data",
                  font_size=22, color=GREY_A),
            label(r"with preferences that separate risk aversion from the will to substitute over time \ "
                  r"(Epstein and Zin, \ 1989)", font_size=22, color=SDF),
            label(r"people fear news about the distant future, \ and stocks fall on exactly that news", font_size=24,
                  color=RISK),
            label(r"its weakness: \ the persistent component is hard to find in the data", font_size=22, color=HOLD),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Bansal and Yaron, JF 59(4) (2004); \ Epstein and Zin, Econometrica 57(4) (1989)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "The second answer is long-run risk. <bookmark mark='a'/> Ravi Bansal and Amir Yaron let consumption "
            "growth carry a small component that is extremely persistent: a slow drift in the economy's growth "
            "rate. <bookmark mark='b'/> It is almost invisible in a few decades of data. <bookmark mark='c'/> With "
            "preferences, due to Larry Epstein and Stanley Zin, that separate aversion to risk from willingness to "
            "move consumption over time, people care intensely about news of the distant future. "
            "<bookmark mark='d'/> And stocks, claims on dividends far ahead, fall on exactly that news, so they "
            "must pay a premium. <bookmark mark='e'/> Its weakness is the mirror of its strength: the persistent "
            "component that drives everything is hard to find in the data."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def disasters(self):
        d = load("disasters")
        gam = d["gamma"]
        a1 = plane([0.5, 4.2], [0, 0.08], center=LEFT * 3.3 + DOWN * 0.6, x_length=5.4, y_length=4.0,
                   xticks=[1, 2, 3, 4], yticks=[0, 0.02, 0.04, 0.06, 0.08], xlabel=r"risk aversion $\gamma$",
                   ylabel=r"equity premium", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{100 * v:.0f}\\%",
                   font_size=14)
        a2 = plane([0.5, 4.2], [-0.02, 0.14], center=RIGHT * 3.1 + DOWN * 0.6, x_length=5.4, y_length=4.0,
                   xticks=[1, 2, 3, 4], yticks=[0, 0.04, 0.08, 0.12], xlabel=r"risk aversion $\gamma$",
                   ylabel=r"risk-free rate", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{100 * v:.0f}\\%",
                   font_size=14)
        pw = path(a1, gam, d["premium_with"], color=RISK, width=4, yr=(0, 0.08))
        po = path(a1, gam, d["premium_without"], color=GREY_B, width=3, yr=(0, 0.08))
        rw = path(a2, gam, d["rf_with"], color=RISK, width=4, yr=(-0.02, 0.14))
        ro = path(a2, gam, d["rf_without"], color=GREY_B, width=3, yr=(-0.02, 0.14))
        row35 = next(r for r in d["rows"] if abs(r["gamma"] - 3.5) < 1e-9)
        head = label(rf"rare disasters: \ a {100 * d['p']:.1f}\% chance a year that consumption falls by 15--65\% "
                     rf"\ (average {100 * d['mean_size']:.0f}\%)", font_size=22, color=GREY_A).to_edge(UP, buff=0.45)
        leg = VGroup(label(r"with disasters", font_size=18, color=RISK),
                     label(r"without", font_size=18, color=GREY_B)).arrange(RIGHT, buff=0.5).next_to(head, DOWN,
                                                                                                  buff=0.2)
        note_ = label(rf"$\gamma = 3.5$: \ premium {100 * row35['with']['premium']:.1f}\%, \ safe rate "
                      rf"{100 * row35['with']['rf']:.1f}\% \ (without disasters: \ "
                      rf"{100 * row35['without']['premium']:.2f}\% and {100 * row35['without']['rf']:.0f}\%)",
                      font_size=21, color=E.ACCENT).next_to(leg, DOWN, buff=0.2)
        tag = published_tag(r"Rietz, JME 22(1) (1988); \ Barro, QJE 121(3) (2006)", corner=DR, font_size=12)
        with self.voiceover(
            "The third answer is disaster. In 1988 Thomas Rietz suggested that stock investors are paid for the "
            "small chance of a catastrophe the century's American data happened not to contain. Robert Barro "
            "measured it in 2006 from the twentieth century's wars and depressions around the world: sixty "
            "disasters, about a 1.7 percent chance a year, with output per head falling on average by about "
            "twenty-nine percent. <bookmark mark='a'/> Agora gives the Island the same odds, with falls from fifteen "
            "to sixty-five percent. <bookmark mark='b'/> Without disasters, the premium stays near zero at any "
            "plausible risk aversion, in grey. With them, in red, it rises steeply. <bookmark mark='c'/> And the "
            "safe rate falls, because in a disaster a safe bond is what you want to hold. "
            f"<bookmark mark='d'/> At a risk aversion of 3.5 the Island's premium is "
            f"{100 * row35['with']['premium']:.1f} percent with a safe rate of {100 * row35['with']['rf']:.1f}: both "
            "puzzles at once, with ordinary risk aversion. The price is a claim that cannot easily be tested: "
            "disasters are rare by definition."
        ) as vo:
            self.play(FadeIn(head), FadeIn(a1), FadeIn(a2), FadeIn(tag), Create(po), Create(ro), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(leg))
            vo.wait_until("b")
            self.play(Create(pw), run_time=2)
            vo.wait_until("c")
            self.play(Create(rw), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(note_))
        self.clear_scene()
