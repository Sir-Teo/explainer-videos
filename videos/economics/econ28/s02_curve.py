from __future__ import annotations

from videos.economics.econ28.common import *  # noqa: F403


class Curve(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Phillips's curve", r"Does unemployment set the pace of inflation?", "Chapter one. Phillips's "
             "curve.", lit={1958: r"Phillips", 1960: r"Samuelson and Solow"}, scale=("nation",),
             horizon=("a century",))
        self.phillips()
        self.menu()

    def phillips(self):
        p = load("phillips")
        ax = plane([0, 11], [-2, 10], center=LEFT * 2.0 + DOWN * 0.3, x_length=7.6, y_length=4.8,
                   xticks=[0, 2, 4, 6, 8, 10], yticks=[-2, 0, 2, 4, 6, 8, 10], xlabel=r"unemployment, \ \%",
                   ylabel=r"change in money wage rates, \ \% a year", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=15)
        zero = seg(ax, 0, 0, 11, 0, color=GREY_D, width=2)
        curve = path(ax, p["u"], p["w"], color=WAGE, width=4, yr=(-2, 10))
        d0 = dot(ax, 5.5, p["w55"], color=OUTPUT, r=0.09)
        d1 = dot(ax, 2.5, p["w25"], color=INFL, r=0.09)
        side = VGroup(
            MathTex(r"\dot w + 0.900 = 9.638\,u^{-1.394}", font_size=32, color=WAGE),
            label(r"fitted to Britain, \ 1861--1913, \\ and it fitted 1948--57 too", font_size=19, color=GREY_A),
            label(r"wages stable at about \\ 5\tfrac12\% unemployment", font_size=20, color=OUTPUT),
            label(rf"at 2\tfrac12\%: \ wages rise {p['w25']:.1f}\%, \\ about as fast as productivity, \\ so prices "
                  r"stay stable", font_size=19, color=INFL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Phillips, \ Economica 25(100) (1958): \ 283--299", corner=DR, font_size=12)
        with self.voiceover(
            "In 1958 Bill Phillips, the engineer of Part twenty-seven's water machine, published a curve. "
            "<bookmark mark='a'/> He took British unemployment and the growth of money wages from 1861 to 1913 and "
            "fitted this equation. <bookmark mark='b'/> It also fitted the years after the Second World War. "
            "<bookmark mark='c'/> Wages were stable when about five and a half percent of workers were unemployed. "
            f"<bookmark mark='d'/> At two and a half percent, wages rose about {p['w25']:.0f} percent a year, roughly "
            "the pace at which productivity grew, so prices could stay stable. The tighter the labour market, the "
            "faster wages rose."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(zero), run_time=0.8)
            vo.wait_until("a")
            self.play(Create(curve), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(GrowFromCenter(d0), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(GrowFromCenter(d1), FadeIn(side[3]))
        self.clear_scene()

    def menu(self):
        u = load("us")
        p = load("phillips")
        ys = np.array(u["years"])
        k = (ys >= 1961) & (ys <= 1969)
        ax = plane([2, 8], [0, 7], center=LEFT * 2.0 + DOWN * 0.3, x_length=7.6, y_length=4.8,
                   xticks=[2, 3, 4, 5, 6, 7, 8], yticks=[0, 2, 4, 6], xlabel=r"unemployment, \ \%",
                   ylabel=r"inflation, \ \%", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=15)
        (u1, p1), (u2, p2) = p["menu"]
        menu = seg(ax, u2, p2, u1, p1, color=CB, width=4)
        m1 = dot(ax, u1, p1, color=CB, r=0.09)
        m2 = dot(ax, u2, p2, color=CB, r=0.09)
        pts = VGroup(*[dot(ax, x, y, color=EXPECT, r=0.07) for x, y in zip(np.array(u["unemployment"])[k],
                                                                          np.array(u["inflation"])[k])])
        yrs_ = VGroup(*[label(f"{yy}", font_size=12, color=GREY_B).next_to(ax.ax.c2p(x, y), RIGHT, buff=0.05)
                        for x, y, yy in zip(np.array(u["unemployment"])[k], np.array(u["inflation"])[k], ys[k])
                        if yy in (1961, 1965, 1969)])
        side = VGroup(
            label(r"Samuelson and Solow, \ 1960: \\ the menu for America", font_size=20, color=CB),
            label(r"stable prices: \\ 5--6\% unemployment", font_size=19, color=CB),
            label(r"3\% unemployment: \\ prices rising 4--5\% a year", font_size=19, color=CB),
            label(r"the 1960s marched up it: \\ 1961 to 1969", font_size=20, color=EXPECT),
            label(r"they warned it might shift; \\ few listened", font_size=19, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Samuelson and Solow, \ AER 50(2) (1960): \ 177--194; \ BLS via FRED", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Two years later, Paul Samuelson and Robert Solow drew the American version for prices instead of "
            "wages, <bookmark mark='a'/> and turned it into a menu for policy. <bookmark mark='b'/> To keep prices "
            "stable, America would need five to six percent unemployment. <bookmark mark='c'/> To get unemployment "
            "down to three percent, it would have to accept prices rising four or five percent a year. "
            "<bookmark mark='d'/> And through the 1960s the economy marched up the menu, year by year, from high "
            "unemployment and low inflation in 1961 to low unemployment and rising inflation in 1969. "
            "<bookmark mark='e'/> Samuelson and Solow had warned that the menu might shift over time. That warning "
            "was the part most people forgot."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.8)
            vo.wait_until("a")
            self.play(Create(menu), FadeIn(side[0]), run_time=1.2)
            vo.wait_until("b")
            self.play(GrowFromCenter(m1), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(GrowFromCenter(m2), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowFromCenter(d) for d in pts], lag_ratio=0.3), FadeIn(yrs_), FadeIn(side[3]),
                      run_time=2.5)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
