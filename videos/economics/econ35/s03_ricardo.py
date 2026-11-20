from __future__ import annotations

from videos.economics.econ35.common import *  # noqa: F403


class Ricardo(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Ricardo's four numbers", r"Why does Portugal buy cloth it could make more cheaply?",
             "Chapter two. Ricardo's four numbers.", lit={1817: r"Ricardo, \emph{Principles}, ch.\ 7"},
             scale=("nation", "world"), horizon=("a year", "a decade"))
        self.numbers()
        self.market()
        self.wages()

    def numbers(self):
        R = load("ricardo")
        cells = [["", r"cloth", r"wine", r"a unit of wine costs"],
                 [r"England", f"{R['aE'][0]}", f"{R['aE'][1]}", rf"{R['pE']:.2f} cloth"],
                 [r"Portugal", f"{R['aP'][0]}", f"{R['aP'][1]}", rf"{R['pP']:.2f} cloth"]]
        xs = (-4.6, -1.6, 0.6, 3.8)
        g = VGroup()
        for i, row in enumerate(cells):
            for j, txt in enumerate(row):
                if not txt:
                    continue
                col = (CLOTH if j == 1 else WINE if j == 2 else GREY_A) if i == 0 else \
                    ((GBR, ARCH)[i - 1] if j == 0 else WHITE)
                g.add(label(txt, font_size=26 if i else 22, color=col).move_to(np.array([xs[j], 1.2 - 0.9 * i, 0])))
        head = label(r"the labour of men for a year, \ to make a quantity of each", font_size=24,
                     color=E.ACCENT).to_edge(UP, buff=0.6)
        price_col = VGroup(*[m for m in g if abs(m.get_center()[0] - xs[3]) < 0.01])
        foot = VGroup(
            label(r"Portugal needs fewer men for both", font_size=22, color=ARCH),
            label(r"but wine is relatively cheap in Portugal, \ cloth in England", font_size=22, color=WHITE),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.7)
        tag = published_tag(r"Ricardo, \ \emph{On the Principles of Political Economy and Taxation} (1817), \ ch.\ 7",
                            corner=DR, font_size=12)
        with self.voiceover(
            "In 1817 David Ricardo, a stockbroker who had made a fortune and turned to economics, put the idea in "
            "four numbers. <bookmark mark='a'/> England needs the labour of a hundred men for a year to make a "
            "certain quantity of cloth, and a hundred and twenty to make a quantity of wine. Portugal needs ninety "
            "and eighty. <bookmark mark='b'/> Portugal is better at both. <bookmark mark='c'/> Yet in England a "
            "unit of wine costs the labour of one point two units of cloth, and in Portugal under nine tenths. "
            "Wine is relatively cheap in Portugal and cloth in England, and that, Ricardo argued, decides the "
            "trade."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(VGroup(*[m for m in g if m not in price_col])))
            vo.wait_until("a")
            self.play(Indicate(g[1], color=WHITE), Indicate(g[2], color=WHITE))
            vo.wait_until("b")
            self.play(FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(price_col), FadeIn(foot[1]))
        self.clear_scene()

    def market(self):
        R = load("ricardo")
        S = R["supply"]
        ax = plane([0, 2.2], [0.6, 1.6], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.0, y_length=4.6,
                   xticks=[0, 0.5, 1.0, 1.5, 2.0], yticks=[0.6, 0.8, 1.0, 1.2, 1.4, 1.6],
                   xlabel=r"wine relative to cloth, \ world quantities", ylabel=r"price of wine, \ in cloth",
                   xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}", font_size=14)
        rs = VMobject(stroke_color=WINE, stroke_width=3.5).set_points_as_corners([
            ax.ax.c2p(0, S["p_low"]), ax.ax.c2p(S["full"], S["p_low"]), ax.ax.c2p(S["full"], S["p_high"]),
            ax.ax.c2p(2.2, S["p_high"])])
        rd = path(ax, [1 / p for p in R["ps"]], R["ps"], CLOTH, 3.0, xr=(0, 2.2), yr=(0.6, 1.6))
        eq = dot(ax, S["full"], R["p"], GAIN, 0.1)
        side = VGroup(
            label(r"purple: \ world supply \\ flat at Portugal's cost, \\ then at England's", font_size=18,
                  color=WINE),
            label(r"pink: \ world demand", font_size=18, color=CLOTH),
            label(rf"the price: \ {R['p']:.2f} cloth a wine, \\ between the two costs", font_size=19, color=GAIN),
            label(rf"England saves {R['saving_E']:.0f} men \\ on each unit of wine; \\ Portugal {R['saving_P']:.0f} "
                  r"\\ on each of cloth", font_size=18, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Ricardo (1817); \ England with a quarter more workers than Portugal", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Let them trade. <bookmark mark='a'/> The world's supply of wine relative to cloth is a staircase. At "
            "any price below Portugal's own cost, under nine tenths of a unit of cloth, nobody makes wine. At "
            "Portugal's cost, Portugal will make any amount. Between the two costs, Portugal makes only wine and "
            "England only cloth, and at England's cost England starts making wine too. <bookmark mark='b'/> The "
            "world's demand slopes down. <bookmark mark='c'/> If England has a quarter more workers than Portugal, "
            f"the two meet at a price of one unit of cloth for a unit of wine, between the two costs, and each "
            f"country makes only its cheaper good. <bookmark mark='d'/> Now England gets a unit of wine for the "
            f"labour of a hundred men instead of a hundred and twenty, and Portugal gets cloth for eighty instead "
            f"of ninety. Both save labour. In consumption, England gains {100 * R['gain_E']:.0f} percent and "
            f"Portugal {100 * R['gain_P']:.0f}."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(rs), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(rd), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(eq, scale=1.4), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def wages(self):
        R = load("ricardo")
        ratio = 1 / R["wage_ratio"]
        lo, hi = R["wage_lo"], R["wage_hi"]
        n = NumberLine(x_range=[1.0, 1.6, 0.1], length=9.0, include_numbers=False, color=GREY_B).move_to(UP * 0.2)
        ticks = VGroup(*[label(f"{x:.1f}", font_size=18, color=GREY_B).next_to(n.n2p(x), DOWN, buff=0.15)
                         for x in (1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6)])
        bandg = Rectangle(width=n.n2p(hi)[0] - n.n2p(lo)[0], height=0.35, fill_color=GAIN, fill_opacity=0.25,
                          stroke_width=0).move_to((n.n2p(lo) + n.n2p(hi)) / 2)
        mk = Triangle(color=WHITE, fill_opacity=1).scale(0.12).rotate(PI).next_to(n.n2p(ratio), UP, buff=0.05)
        head = label(r"Portugal's wage, \ relative to England's", font_size=26, color=E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(rf"at least {lo:.2f}: \ or Portugal would undersell England's cloth \ ($100/90$)", font_size=21,
                  color=CLOTH),
            label(rf"at most {hi:.2f}: \ or England would undersell Portugal's wine \ ($120/80$)", font_size=21,
                  color=WINE),
            label(rf"here: \ {ratio:.2f}, \ set by the demand for each country's good", font_size=22, color=WHITE),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.7)
        tag = published_tag(r"Ricardo (1817); \ this film's world", corner=DR, font_size=12)
        with self.voiceover(
            "What do workers earn? <bookmark mark='a'/> Portugal's wage must be higher than England's, since its "
            "workers are more productive at both; but not too much higher. <bookmark mark='b'/> If it were less than "
            "a hundred over ninety times England's, Portugal could undersell England's cloth too. "
            "<bookmark mark='c'/> If it were more than a hundred and twenty over eighty, England could undersell "
            f"Portugal's wine. <bookmark mark='d'/> In between, where demand puts it, here at {ratio:.2f}, each "
            "country sells what it is relatively good at. A country with low productivity competes through low "
            "wages; a country with high productivity can afford high ones. Ricardo's insight is that it is "
            "relative, not absolute, cost that decides who sells what."
        ) as vo:
            self.play(FadeIn(head), FadeIn(n), FadeIn(ticks), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(bandg))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(mk), FadeIn(rows[2]))
        self.clear_scene()
