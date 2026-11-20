from __future__ import annotations

from videos.economics.econ23.common import *  # noqa: F403


class Volatility(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Do prices move too much?", r"Do stock prices move with the dividends they promise, \ or "
             r"with something else?", "Chapter ten. Do prices move too much?",
             lit={1965: r"Samuelson", 1970: r"Fama", 1981: r"Shiller", 1988: r"Campbell and Shiller"},
             scale=("market",), horizon=("a century",))
        self.shiller()
        self.predict()
        self.efficient()

    def shiller(self):
        v = load("volatility")
        ax = plane([1870, 2010], [0, 2200], center=LEFT * 1.7 + DOWN * 0.4, x_length=8.6, y_length=4.9,
                   xticks=[1880, 1920, 1960, 2000], yticks=[0, 500, 1000, 1500, 2000],
                   ylabel=r"real S\&P composite \ (latest year's dollars)", xfmt=lambda v_: f"{v_:.0f}",
                   yfmt=lambda v_: f"{v_:,.0f}".replace(",", "{,}"), font_size=15)
        p = path(ax, v["years"], v["P"], color=STOCK, width=3, smooth=False)
        ps = path(ax, v["years"], v["Pstar"], color=VALUE, width=4, smooth=False)
        side = VGroup(
            label(r"the price", font_size=21, color=STOCK),
            label(r"$P^*$: \ the present value of the \\ dividends that actually \\ followed \ (constant rate)",
                  font_size=19, color=VALUE),
            label(r"if $P = \mathbb{E}[P^*]$, \ the price \\ should vary \emph{less} than $P^*$", font_size=19,
                  color=WHITE),
            label(rf"s.d.: \ price {v['sd_P']:.0f}, \ $P^*$ {v['sd_Pstar']:.0f}", font_size=21, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Shiller, AER 71(3) (1981): \ 421--436; \ data: \ Shiller, ch.\ 26, \ updated",
                            corner=DR, font_size=12)
        with self.voiceover(
            "In 1981 Robert Shiller asked a simple question of the present-value formula. <bookmark mark='a'/> Here "
            "is the real price of American stocks since 1871. <bookmark mark='b'/> And here is what the market "
            "would have been worth if investors had known all the dividends that were actually going to be paid, "
            "discounted at a constant rate: the ex post rational price, P star. <bookmark mark='c'/> If the price "
            "is the best forecast of P star, it must vary less than P star, because a forecast cannot be more "
            "volatile than the thing forecast. <bookmark mark='d'/> It varies more: a standard deviation of "
            f"{v['sd_P']:.0f} against {v['sd_Pstar']:.0f}. Prices swing far more than the dividends they promise "
            "can justify, unless the discount rate itself moves a great deal."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(p), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(ps), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def predict(self):
        pr = load("predict")
        rows = pr["rows"]
        axes_ = []
        groups = VGroup()
        for k, r in enumerate(rows):
            ax = plane([-4.6, -2.4], [-0.6, 1.8], center=LEFT * 4.4 + RIGHT * 4.4 * k + DOWN * 0.6, x_length=3.8,
                       y_length=3.6, xticks=[-4.5, -3.5, -2.5], yticks=[0, 1], xlabel=r"log dividend yield",
                       xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", font_size=13)
            pts = VGroup(*[Dot(ax.ax.c2p(x, y), radius=0.025, color=STOCK).set_opacity(0.6)
                           for x, y in zip(r["x"], r["y"]) if -4.6 <= x <= -2.4 and -0.6 <= y <= 1.8])
            b = np.polyfit(r["x"], r["y"], 1)
            fit = seg(ax, -4.55, np.polyval(b, -4.55), -2.45, np.polyval(b, -2.45), color=WHITE, width=3)
            head = label(rf"the next {r['k']} year{'s' if r['k'] > 1 else ''}: \ $R^2 = {r['r2']:.2f}$",
                         font_size=19, color=STOCK if k else GREY_A).next_to(ax, UP, buff=0.15)
            groups.add(VGroup(ax, pts, fit, head))
            axes_.append(ax)
        top = label(r"real log return over the next 1, \ 5 and 10 years, \ against today's dividend yield",
                    font_size=22, color=GREY_A).to_edge(UP, buff=0.4)
        note_ = label(r"overlapping windows: \ the long-horizon fits look better than their true precision",
                      font_size=17, color=GREY_B).to_edge(DOWN, buff=0.25)
        tag = data_tag(r"Shiller ch.\ 26 data, \ 1871--2012", corner=DR, font_size=12)
        with self.voiceover(
            "Where does the extra movement go? Into returns that can be forecast. <bookmark mark='a'/> Regress the "
            "next year's real return on today's dividend yield, dividends over price: almost nothing, an R squared "
            f"of {rows[0]['r2']:.2f}. <bookmark mark='b'/> Over the next five years, {rows[1]['r2']:.2f}. "
            f"<bookmark mark='c'/> Over ten, {rows[2]['r2']:.2f}. When prices are high relative to dividends, "
            "returns over the following decade tend to be low. <bookmark mark='d'/> The windows overlap, so the "
            "long-horizon fits look better than their true precision, a trap that Part four would recognize. But "
            "John Campbell and Shiller showed the pattern is the same one as excess volatility: prices move because "
            "expected returns move, not because expected dividends do."
        ) as vo:
            self.play(FadeIn(top), FadeIn(tag), *[FadeIn(g[0]) for g in groups])
            for mk, g in zip("abc", groups):
                vo.wait_until(mk)
                self.play(FadeIn(g[1]), Create(g[2]), FadeIn(g[3]))
            vo.wait_until("d")
            self.play(FadeIn(note_))
        self.clear_scene()

    def efficient(self):
        f = next(x for x in facts.FACTS if x.key == "unpredictable")
        data_m = label(r"next year's return: \\ $R^2$ about 0.03; \\ ten years: \ about 0.24", font_size=19,
                       color=WHITE)
        theory_m = label(r"efficient markets: \\ prices use what is known, \\ so news is unforecastable \\ "
                         r"(Samuelson; \ Fama)", font_size=19, color=VALUE)
        agora_m = label(r"a risk premium that rises \\ in bad times \ (habits, \\ chapter 9) \ makes long-run \\ "
                        r"returns forecastable", font_size=19, color=E.AGORA)
        fc = fact_card(tex_safe(f.statement), columns=((r"the data", data_m), (r"the theory", theory_m),
                                                         (r"Agora", agora_m)), width=12.4, font_size=22,
                       colors=(WHITE, VALUE, None)).move_to(UP * 0.6)
        ptr = label(r"efficient markets, \ anomalies and the evidence in depth: \ \emph{Quant, Built}, \ Parts 1, \ "
                    r"23--25 \ and 43", font_size=20, color=GREY_B).next_to(fc, DOWN, buff=0.45)
        tag = published_tag(r"Samuelson, IMR 6(2) (1965); \ Fama, JF 25(2) (1970); \ Campbell and Shiller, RFS 1(3) "
                            r"(1988)", corner=DR, font_size=12)
        with self.voiceover(
            "This is the efficient markets debate in one card. <bookmark mark='a'/> Paul Samuelson proved in 1965 "
            "that properly anticipated prices fluctuate randomly, and Eugene Fama organized the evidence that prices "
            "reflect what is known. Next year's return is indeed hard to forecast. <bookmark mark='b'/> But over a "
            "decade, prices that are high relative to dividends do predict low returns. Fama and Shiller, who "
            "disagreed about what that means, shared the Nobel prize in 2013 with Hansen. In Agora's reading, a "
            "premium that rises in bad times, like the habit model's, makes long-run returns forecastable without "
            "anyone leaving money on the table. <bookmark mark='c'/> The series' sister course, Quant, Built, takes "
            "up the evidence in depth."
        ) as vo:
            self.play(FadeIn(fc.card), FadeIn(fc[1][0]), *[FadeIn(c[:2]) for c in fc.cols], FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(fc.cols[0][2:]), FadeIn(fc.cols[1][2:]))
            vo.wait_until("b")
            self.play(FadeIn(fc.cols[2][2:]))
            vo.wait_until("c")
            self.play(FadeIn(ptr))
        self.clear_scene()
