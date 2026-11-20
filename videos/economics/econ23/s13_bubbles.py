from __future__ import annotations

from videos.economics.econ23.common import *  # noqa: F403


class Bubbles(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Bubbles", r"Can a price stay above value, \ and why do bubbles appear even in the "
             r"laboratory?", "Chapter eleven. Bubbles.", lit={1985: r"Tirole", 1988: r"Smith, Suchanek, Williams",
                                                               1929: r"the crash"}, scale=("market",),
             horizon=("a year", "a decade"))
        self.rational()
        self.lab()
        self.call()

    def rational(self):
        rows = VGroup(
            MathTex(r"p_t \;=\; \underbrace{\sum_{s \ge 1} \mathbb{E}_t[m_{t,t+s}\,d_{t+s}]}_{\text{fundamental}} "
                    r"\;+\; \underbrace{b_t}_{\text{bubble}}, \qquad b_t = \mathbb{E}_t[m_{t+1}\,b_{t+1}]",
                    font_size=40),
            label(r"a rational bubble must be expected to grow at the rate of interest, \ for ever", font_size=24,
                  color=GREY_A),
            label(r"so it cannot exist on an asset with a last date, \ or if it would outgrow the economy", font_size=23,
                  color=RISK),
            label(r"Jean Tirole, \ 1985: \ possible only when interest is below growth: \ Part 22's inefficient "
                  r"economy", font_size=23, color=VALUE),
            label(r"Samuelson's money is such a bubble: \ paper worth nothing, \ held because others will take it",
                  font_size=23, color=BILL),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Tirole, Econometrica 53(6) (1985): \ 1499--1528", corner=DR, font_size=12)
        with self.voiceover(
            "Can a price stay above value even if everyone is rational? <bookmark mark='a'/> Split any price into "
            "the present value of its dividends, the fundamental, and whatever is left, a bubble. For people to hold "
            "the bubble, it must be expected to grow at the rate of interest, for ever. <bookmark mark='b'/> So it "
            "cannot exist on an asset with a last date, because at the last date it is worth nothing, and by "
            "backward induction worth nothing before. <bookmark mark='c'/> Nor can it grow faster than the economy "
            "for ever. <bookmark mark='d'/> Jean Tirole showed in 1985 that a rational bubble is possible only when "
            "the interest rate is below the growth rate: Part twenty-two's dynamically inefficient economy. "
            "<bookmark mark='e'/> Samuelson's money was exactly such a bubble: paper worth nothing in itself, held "
            "because the next generation will take it."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def lab(self):
        s = load("ssw")
        t = np.arange(1, s["periods"] + 1)
        ax = plane([0.5, 15.5], [0, 4.2], center=LEFT * 1.8 + DOWN * 0.5, x_length=8.2, y_length=4.6,
                   xticks=[1, 5, 10, 15], yticks=[0, 1, 2, 3, 4], xlabel=r"trading period",
                   ylabel=r"price \ (dollars)", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", font_size=16)
        fv = path(ax, t, s["fv"], color=VALUE, width=4, smooth=False)
        pr = path(ax, t, s["price"], color=STOCK, width=4, smooth=False)
        pdots = VGroup(*[dot(ax, x, y, color=STOCK, r=0.06) for x, y in zip(t, s["price"])])
        sc = VGroup(
            label(r"Smith, \ Suchanek and Williams, \ 1988", font_size=21, color=E.ACCENT),
            label(r"an asset that pays a random \\ dividend after each of fifteen \\ periods, \ then nothing", font_size=18,
                  color=GREY_A),
            label(r"its value falls in a straight \\ line: \ everyone can compute it", font_size=18, color=VALUE),
            label(r"14 of their 22 markets \\ bubbled and crashed", font_size=20, color=RISK),
            label(rf"the Island's version: \ {s['trend_followers']} of {s['n']} \\ traders follow the trend", font_size=18,
                  color=STOCK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = VGroup(published_tag(r"Smith, Suchanek and Williams, Econometrica 56(5) (1988): \ 1119--1151",
                                   corner=DR, font_size=12))
        itag = island_tag(r"the price path: \ simulated, \ the Island", corner=DL, font_size=13)
        with self.voiceover(
            "Bubbles appear even where everything is known. <bookmark mark='a'/> In 1988 Vernon Smith, Gerry "
            "Suchanek and Arlington Williams set up laboratory markets in an asset that paid a random dividend after "
            "each of fifteen periods, and nothing after. <bookmark mark='b'/> Its fundamental value falls in a "
            "straight line, and anyone can compute it: on the Island, the expected dividend is "
            f"{100 * s['expected_dividend']:.0f} cents, so the value starts at "
            f"{s['fv'][0]:.2f} dollars. <bookmark mark='c'/> In fourteen of their twenty-two markets, prices rose "
            "far above value and then crashed near the end. <bookmark mark='d'/> The Island's version needs only "
            f"{s['trend_followers']} traders of {s['n']} who extrapolate the last price change: the price starts "
            "low, climbs past value, rides above it for half the session, and collapses as the end comes into "
            "view. Experience reduced bubbles in the laboratory, but did not end them."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(sc[0]))
            vo.wait_until("a")
            self.play(FadeIn(sc[1]))
            vo.wait_until("b")
            self.play(Create(fv), FadeIn(sc[2]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(sc[3]))
            vo.wait_until("d")
            self.play(FadeIn(sc[4]), FadeIn(itag), Create(pr), LaggedStart(*[FadeIn(d) for d in pdots],
                                                                           lag_ratio=0.1), run_time=3)
        self.clear_scene()

    def call(self):
        c = calls.CALLS["fisher_plateau"]
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.4,
                       font_size=21).move_to(UP * 0.1)
        tag = published_tag(r"Fisher, as reported in the New York Times, 16 October 1929; \ Shiller ch.\ 26 data",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> In October 1929 Irving Fisher, then America's most famous economist, "
            "told an audience in New York that stock prices had reached what looked like a permanently high "
            "plateau. <bookmark mark='b'/> The market crashed within days. In Shiller's January figures the S and P "
            "composite was worth two-thirds less in 1932 than in 1929, three-fifths less after inflation, and it did "
            "not regain its 1929 real level until the 1950s. <bookmark mark='c'/> Wrong. Fisher's work on interest "
            "and money is still taught in Parts seven and twenty-eight. His forecast is taught here."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag))
            vo.wait_until("b")
            self.play(Indicate(cc.right, color=WHITE, scale_factor=1.01))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3))
        self.clear_scene()
