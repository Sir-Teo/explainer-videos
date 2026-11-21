from __future__ import annotations

from videos.economics.econ61.common import *  # noqa: F403


class Gig(VoiceoverScene):
    def construct(self):
        card(self, 11, r"The gig economy", r"What is flexibility worth to a driver, \ and what should the law call "
             r"them?", "Chapter eleven. The gig economy.",
             lit={2019: r"Chen et al.; \ AB5", 2021: r"Uber v Aslam"}, scale=("person", "nation"),
             horizon=("a day", "a decade"))
        self.flexibility()
        self.findings()
        self.law()

    def flexibility(self):
        F = load("flex")
        rng = np.random.default_rng(7)
        r = 25.0 + rng.normal(0, 9.0, 24)
        hrs = np.arange(24)
        ax = plane([-0.5, 23.5], [0, 50], center=LEFT * 3.0 + DOWN * 0.3, x_length=6.4, y_length=4.4,
                   xticks=[0, 6, 12, 18, 23], yticks=[0, 10, 20, 30, 40, 50], xlabel=r"hour of the day",
                   ylabel=r"one driver's reservation wage, \ \$ an hour", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        wage = seg(ax, -0.5, 20, 23.5, 20, DRIVER, 2.4)
        bs = VGroup()
        for h, v in zip(hrs, r):
            p0, p1 = ax.ax.c2p(h - 0.35, 0), ax.ax.c2p(h + 0.35, float(np.clip(v, 0.5, 49)))
            bs.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0,
                             fill_color=GAIN if v < 20 else GREY_C, fill_opacity=0.85).move_to((p0 + p1) / 2))
        g = 20.0 - r
        best = max(range(17), key=lambda s: g[s:s + 8].sum())
        p0, p1 = ax.ax.c2p(best - 0.5, 0), ax.ax.c2p(best + 7.5, 50)
        shift_box = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_color=SURGE, stroke_width=2.4,
                              fill_opacity=0).move_to((p0 + p1) / 2)
        side = VGroup(
            label(r"each hour, \ what it would take to get this driver on the road", font_size=19, color=GREY_A),
            label(r"gold line: \ the pay, \ \$20 an hour; \ green: \ hours worth driving, \\ which a flexible "
                  r"driver drives, \ and no others", font_size=19, color=GAIN),
            label(r"red box: \ the best fixed eight-hour shift, \\ taken whole or not at all", font_size=19,
                  color=SURGE),
            label(rf"5,000 Island drivers: \ surplus \${F['flex']:.0f} a day flexible, \ "
                  rf"\${F['fixed']:.0f} with shifts".replace(",", "{,}"), font_size=20, color=WHITE),
            label(rf"flexibility worth {F['ratio']:.1f} times the shift's surplus; \\ only "
                  rf"{100 * F['share_fixed_work']:.0f}\% would take a shift at all", font_size=20, color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if side.width > 5.8:
            side.width = 5.8
            side.to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ agora.platform.flexibility; \ reservation wages planted", corner=DL,
                         font_size=12)
        with self.voiceover(
            "Ride-hailing drivers choose their own hours, minute by minute. What is that worth to them? <bookmark "
            "mark='a'/> Take one Island driver. Each bar is what it would take to get them on the road in that "
            "hour: low when the children are at school, high at dinner time, different every day. <bookmark "
            "mark='b'/> The app pays twenty dollars an hour. A flexible driver drives exactly the green hours, "
            "when the pay beats the alternative, and earns the gap. <bookmark mark='c'/> A taxi company would "
            "offer a fixed eight-hour shift instead: the best block of eight hours, taken whole, bad hours "
            "included, or not at all. <bookmark mark='d'/> Across five thousand Island drivers, the surplus from "
            f"driving is {F['flex']:.0f} dollars a day with flexible hours and {F['fixed']:.0f} with shifts. "
            f"<bookmark mark='e'/> Flexibility is worth {F['ratio']:.1f} times what the shift leaves, and only "
            f"{100 * F['share_fixed_work']:.0f} percent of these drivers would take a shift at all."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bs], lag_ratio=0.05), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(wage), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(shift_box), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def findings(self):
        cards = point_cards([
            (r"the value of flexibility", r"Chen, \ Chevalier, \ Rossi and Oehlsen: \ drivers' hour-by-hour "
             r"choices imply they earn more than twice the surplus of less flexible arrangements", GAIN),
            (r"who drives", r"most drive part time, \ around other work and family; \ the hours move with the pay",
             DRIVER),
            (r"the pay gap without a pay formula", r"Cook, \ Diamond, \ Hall, \ List and Oyer: \ among over a "
             r"million drivers, \ men earned about 7\% more an hour, \ from experience, \ where they drove and "
             r"how fast", RIDER),
            (r"what flexibility costs", r"no minimum for waiting time, \ no sick pay, \ no pension: \ the risk "
             r"sits with the driver", SURGE),
        ], width=12.6, cols=2, font_size=20).move_to(DOWN * 0.2)
        head = label(r"what the drivers' data show", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Chen, \ Chevalier, \ Rossi and Oehlsen, \ Journal of Political Economy 127(6) "
                            r"(2019); \ Cook et al., \ Review of Economic Studies 88(5) (2021)", corner=DL,
                            font_size=12)
        with self.voiceover(
            "The platform's own data show what drivers do. <bookmark mark='a'/> M. Keith Chen, Judith Chevalier, "
            "Peter Rossi and Emily Oehlsen used drivers' hour-by-hour choices to recover their reservation wages, "
            "as the Island does. They found that drivers earn more than twice the surplus they would in less "
            "flexible arrangements. <bookmark mark='b'/> Most drive part time, around other work and family, and "
            "their hours move with the pay. <bookmark mark='c'/> Cody Cook, Rebecca Diamond, Jonathan Hall, John "
            "List and Paul Oyer found that among over a million drivers men earned about seven percent more an "
            "hour, on a platform whose pay formula never looks at gender. The gap came from experience, from "
            "where and when they drove, and from driving faster. <bookmark mark='d'/> What flexibility costs is "
            "everything a job usually carries: pay for waiting, sick pay, a pension. The risk sits with the "
            "driver."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()

    def law(self):
        rows = VGroup(
            history_card(2019, r"California's AB5", r"a test that treats most such workers as employees", color=SURGE,
                         width=11.4, font_size=21),
            history_card(2020, r"California's Proposition 22", r"voters exempt app-based drivers, \ with an earnings "
                         r"floor and some benefits", color=DRIVER, width=11.4, font_size=21),
            history_card(2021, r"Uber v Aslam, \ UK Supreme Court", r"drivers are workers, \ entitled to the minimum "
                         r"wage and holiday pay", color=RIDER, width=11.4, font_size=21),
        ).arrange(DOWN, buff=0.3).move_to(UP * 0.4)
        foot = label(r"the economist's question: \ what do employee status's protections cost in flexibility, \ and "
                     r"who pays?", font_size=21, color=E.ACCENT).next_to(rows, DOWN, buff=0.45)
        tag = published_tag(r"California Assembly Bill 5 (2019); \ Proposition 22 (2020); \ [2021] UKSC 5",
                            corner=DL, font_size=12)
        with self.voiceover(
            "And then there is the law. Is a driver an employee? <bookmark mark='a'/> In 2019 California passed a "
            "law whose test would treat most such workers as employees. <bookmark mark='b'/> In 2020 its voters "
            "passed Proposition twenty-two, exempting app-based drivers, with an earnings floor and some benefits "
            "instead. <bookmark mark='c'/> In 2021 Britain's Supreme Court ruled that Uber's drivers are workers, "
            "entitled to the minimum wage and holiday pay. <bookmark mark='d'/> The economist's question is the "
            "trade the chapter has measured: what employment's protections cost in flexibility, and who ends up "
            "paying, riders through fares, drivers through fewer hours, or the platform through its margin."
        ) as vo:
            self.play(FadeIn(tag))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()
