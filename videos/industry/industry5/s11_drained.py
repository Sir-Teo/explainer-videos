from __future__ import annotations

from videos.industry.industry5.common import *  # noqa: F403


class Drained(VoiceoverScene):
    def construct(self):
        card(self, 15, "Moats that drained", "How do the strongest walls come down?",
             "Chapter fifteen. Moats that drained.", lit=("change", "moat"))
        self.papers()
        self.kodak()

    def papers(self):
        D = R["drained"]
        from explainer.industry.register import get
        ads05, ads20, circ20 = D["news2005"], get("news.ads.2020"), get("news.circ.2020")
        press = draw.castle(2.0, moat=0.7, color="#E8EAED").move_to([-4.4, 0.7, 0])
        sheet = VGroup(RoundedRectangle(corner_radius=0.04, width=0.9, height=1.15, stroke_width=0, fill_color=WHITE,
                                        fill_opacity=0.95),
                       *[Line([-0.32, y, 0], [0.32, y, 0], stroke_color="#8C929B", stroke_width=2)
                         for y in np.linspace(0.35, -0.4, 7)]).move_to([-4.4, -1.6, 0])
        name = tx("the local newspaper", 20, WHITE, bold=True).next_to(press, UP, buff=0.2)
        base = -2.6
        u = 0.085

        def col(x, v, color, lab, yr):
            r_ = Rectangle(width=1.0, height=v * u, stroke_width=0, fill_color=color, fill_opacity=0.9).move_to(
                [x, base, 0], aligned_edge=DOWN)
            return VGroup(r_, tx(f"${v:.1f}bn", 19, color, bold=True).next_to(r_, UP, buff=0.06),
                          tx(lab, 15, GREY_B).next_to(r_, DOWN, buff=0.08), tx(yr, 20, WHITE, bold=True))
        a05 = col(-0.4, ads05, GOLD, "advertising", "2005")
        c05 = col(0.8, 10.7, "#7EC8F5", "circulation", "")
        a20 = col(3.4, ads20, GOLD, "advertising", "2020")
        c20 = col(4.6, circ20, "#7EC8F5", "circulation", "")
        for g_, x in ((a05, 0.2), (a20, 4.0)):
            g_[3].move_to([x, 2.55, 0])
        apps = VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.5, height=0.5, stroke_width=0, fill_color=c,
                                         fill_opacity=0.95) for c in ("#3B7DD8", "#7BD88F", "#E8554E", "#F6C453")])
        apps.arrange(RIGHT, buff=0.15).move_to([-4.4, 3.1, 0])
        src = source("Pew Research Center, from the News Media Alliance (to 2012) and newspaper companies' SEC filings "
                     "(Pew's estimates, 2013-2020)", size=13)
        with self.voiceover(
            "Moats do not last for ever. The cleanest example is the newspaper. <bookmark mark='a'/> For most of a "
            "century a city's daily paper was one of the best businesses in America. It owned the printing press "
            "and the delivery vans, and it was the only place a shop could reach the whole town, or a family could "
            "sell a car or find a flat. <bookmark mark='b'/> In 2005 American newspapers took in an estimated "
            f"{ads05:.0f} billion dollars from advertising, and about eleven billion from readers. By 2008, "
            "advertising was down to thirty-eight billion; by 2010, twenty-six. "
            "<bookmark mark='c'/> Then the classified ads moved to free websites, the shoppers' ads moved to search "
            "and social media, and the paper's moat, being the only way to reach the town, was simply walked "
            f"round. <bookmark mark='d'/> By 2020, by Pew's estimate, advertising had fallen to about "
            f"{ads20:.1f} billion, and readers were paying more than advertisers. No rival built a "
            "better newspaper. The thing the moat protected stopped being needed."
        ) as vo:
            self.play(FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(press, shift=UP * 0.2), FadeIn(name), FadeIn(sheet, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(a05[3]), GrowFromEdge(a05[0], DOWN), FadeIn(a05[1:3]), GrowFromEdge(c05[0], DOWN),
                      FadeIn(c05[1:3]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(a_, shift=DOWN * 0.3) for a_ in apps], lag_ratio=0.2),
                      press.moat.animate.set_opacity(0.1), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(a20[3]), GrowFromEdge(a20[0], DOWN), FadeIn(a20[1:3]), GrowFromEdge(c20[0], DOWN),
                      FadeIn(c20[1:3]))
            self.play(Indicate(c20, color=WHITE, scale_factor=1.06))
        self.clear_scene()

    def kodak(self):
        D = R["drained"]
        from explainer.industry.register import get
        film = VGroup(*[RoundedRectangle(corner_radius=0.02, width=0.42, height=0.32, stroke_width=0,
                                         fill_color="#F6C453", fill_opacity=0.9) for _ in range(7)]).arrange(
            RIGHT, buff=0.06)
        holes = VGroup(*[Square(0.06, stroke_width=0, fill_color="#0E1117", fill_opacity=1).move_to(
            film.get_top() + RIGHT * (x - 1.4) + DOWN * 0.04) for x in np.linspace(0, 2.8, 14)])
        reel = VGroup(Rectangle(width=film.width + 0.2, height=0.5, stroke_width=0, fill_color="#3A2A22",
                                fill_opacity=1).move_to(film), film, holes).move_to([-3.2, 1.6, 0])
        phone = viz.phone(1.6, back=False).move_to([3.2, 1.4, 0])
        base = -2.5
        u = 0.32
        k08 = Rectangle(width=1.3, height=D["kodak2008"] * u, stroke_width=0, fill_color=GOLD, fill_opacity=0.9).move_to(
            [-1.2, base, 0], aligned_edge=DOWN)
        k17 = Rectangle(width=1.3, height=D["kodak2017"] * u, stroke_width=0, fill_color=GOLD, fill_opacity=0.9).move_to(
            [1.2, base, 0], aligned_edge=DOWN)
        labs = VGroup(tx(f"${D['kodak2008']:.1f}bn", 22, GOLD, bold=True).next_to(k08, UP, buff=0.08),
                      tx(f"${D['kodak2017']:.1f}bn", 22, GOLD, bold=True).next_to(k17, UP, buff=0.08),
                      tx("2008", 18, GREY_B).next_to(k08, DOWN, buff=0.1), tx("2017", 18, GREY_B).next_to(k17, DOWN,
                                                                                                    buff=0.1))
        ch11 = tx(f"chapter 11: 19 January {int(get('kodak.ch11'))}", 22, COST_, bold=True).move_to([0, 0.6, 0])
        head = tx("Eastman Kodak's sales", 22, WHITE).move_to([0, 2.9, 0])
        src = source("Eastman Kodak Forms 10-K (SEC company facts) and Form 8-K of 19 January 2012", size=13)
        with self.voiceover(
            "The same thing happened to photographic film. <bookmark mark='a'/> For a century Eastman Kodak "
            "sold the film, the chemicals and the paper, and a great deal of the profit came from the film itself, "
            "used once and bought again. <bookmark mark='b'/> Then photographs went digital, and then into the "
            f"phone. In 2008 Kodak still sold {D['kodak2008']:.1f} billion dollars' worth of goods. "
            "<bookmark mark='c'/> In January 2012 it filed for bankruptcy. <bookmark mark='d'/> By 2017 its sales were "
            f"{D['kodak2017']:.1f} billion. A moat protects a castle against rivals who want what is inside. It does "
            "nothing when the world stops wanting it. Part 6 is about how industries move through booms and "
            "busts; this series comes back to disruption in its later acts."
        ) as vo:
            self.play(FadeIn(src), FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(reel, shift=RIGHT * 0.3))
            vo.wait_until("b")
            self.play(FadeIn(phone, shift=LEFT * 0.3), reel.animate.set_opacity(0.4))
            self.play(GrowFromEdge(k08, DOWN), FadeIn(labs[0]), FadeIn(labs[2]))
            vo.wait_until("c")
            self.play(FadeIn(ch11, scale=1.2))
            vo.wait_until("d")
            self.play(GrowFromEdge(k17, DOWN), FadeIn(labs[1]), FadeIn(labs[3]))
        self.clear_scene()
