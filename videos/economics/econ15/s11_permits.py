from __future__ import annotations

from videos.economics.econ15.common import *  # noqa: F403


class Permits(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Permits: \ the acid-rain market", r"Can a market in the right to pollute cut pollution cheaply, "
             r"\ and what happens when the state changes its mind?", "Chapter nine. Permits: the acid-rain market.",
             lit={1968: r"Dales", 1990: r"the Clean Air Act Amendments", 1995: r"trading begins",
                  2013: r"Schmalensee and Stavins"}, scale=("market", "nation"), horizon=("a decade",))
        self.idea()
        self.record()
        self.prices()
        self.called()

    def idea(self):
        rows = VGroup(
            label(r"John Dales, \ 1968: \ instead of a price, \ fix the quantity, \ and sell the right to it",
                  font_size=24),
            label(r"the state caps total emissions, \ and issues permits that add up to the cap", font_size=24,
                  color=SOCIAL),
            label(r"a firm that can cut cheaply cuts more, \ and sells its spare permits", font_size=24, color=GOOD),
            label(r"a firm for which cutting is dear buys them", font_size=24, color=DEMAND),
            label(r"the cap is met by whoever cuts most cheaply: \ the permit's price is the cost of the last tonne cut",
                  font_size=23, color=E.ACCENT),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        tag = published_tag(r"Dales, Pollution, Property and Prices (1968); \ Montgomery, JET 5(3) (1972)",
                            corner=DR, font_size=13)
        with self.voiceover(
            "The third remedy turns Coase's idea into policy. <bookmark mark='a'/> In 1968 the Canadian economist "
            "John Dales proposed that, instead of setting a price on pollution, the state should fix the quantity, "
            "and sell the right to it. <bookmark mark='b'/> It caps total emissions, and issues permits that add up "
            "to the cap. <bookmark mark='c'/> A firm that can cut its emissions cheaply cuts more, and sells its spare "
            "permits. <bookmark mark='d'/> A firm for which cutting is expensive buys them. <bookmark mark='e'/> So "
            "the cap is met by whoever can cut most cheaply, and the permit's price settles at the cost of cutting "
            "the last tonne: a Pigouvian tax, discovered by the market. David Montgomery proved in 1972 that it "
            "reaches the cap at the least total cost."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def record(self):
        ac = load("acid")
        u = ac["utility_so2_mt"]
        ys = [1990, 2004, 2010]
        vals = [u[str(y)] if str(y) in u else u[y] for y in ys]
        ax = plane([1987, 2013], [0, 18], center=LEFT * 2.8 + DOWN * 0.3, x_length=6.2, y_length=4.6,
                   xticks=[1990, 1995, 2000, 2005, 2010], yticks=[0, 5, 10, 15], xlabel="",
                   ylabel=r"power plants' SO$_2$, \ million tons", font_size=16, xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}")
        a = ax.ax
        dots = VGroup(*[Dot(a.c2p(y, v), radius=0.09, color=SOCIAL) for y, v in zip(ys, vals)])
        line = VMobject(stroke_color=SOCIAL, stroke_width=3).set_points_as_corners([a.c2p(y, v) for y, v in
                                                                                    zip(ys, vals)])
        vl = VGroup(*[label(f"{v:.1f}", font_size=17, color=SOCIAL).next_to(d, UR, buff=0.08) for v, d in
                      zip(vals, dots)])
        goal = seg(ax, 1987, ac["goal_mt"], 2013, ac["goal_mt"], color=GOOD, width=2, dashed=True)
        gl = label(rf"the long-run cap, \ {ac['goal_mt']} million tons: \ met in {ac['goal_year']}", font_size=15,
                   color=GOOD).next_to(a.c2p(1988, ac["goal_mt"]), DOWN, buff=0.1, aligned_edge=LEFT)
        side = VGroup(
            label(r"1990: \ the Clean Air Act Amendments \\ cap power stations' sulphur; \ trading from 1995",
                  font_size=20),
            label(rf"emissions fell a third by 2004, \\ while coal-fired power rose "
                  rf"{100 * ac['coal_generation_rise_1990_2004']:.0f}\%", font_size=20, color=SOCIAL),
            label(r"a \$2,000 fine a ton over, \ and monitors in every stack: \\ compliance close to 100\%",
                  font_size=20),
            label(rf"cheaper than rules would have been: \\ by {100 * ac['savings_vs_command'][0]:.0f} to "
                  rf"{100 * ac['savings_vs_command'][1]:.0f}\%, \ by the estimates", font_size=20, color=GOOD),
            label(r"the surprise: \ railroad deregulation \\ had made low-sulphur coal from Wyoming cheap",
                  font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Schmalensee and Stavins, JEP 27(1) (2013)", corner=DR, font_size=13)
        with self.voiceover(
            "In 1990 the United States tried it, at scale. <bookmark mark='a'/> The Clean Air Act Amendments capped "
            "the sulphur dioxide from power stations, the main cause of acid rain, and from 1995 the permits, called "
            "allowances, could be traded. <bookmark mark='b'/> Emissions from power plants fell by more than a third "
            "by 2004, from sixteen million tons to ten, even though coal-fired power rose by a quarter. The long-run "
            "cap was met in 2007, and by 2010 emissions were down to five million tons. <bookmark mark='c'/> With a "
            "fine of two thousand dollars for every ton over, and monitors in every smokestack, compliance was "
            "nearly perfect. <bookmark mark='d'/> Studies put the savings, against rules that would have dictated "
            "how to cut, at fifteen to ninety percent. <bookmark mark='e'/> And part of the saving was a surprise: "
            "the deregulation of the railroads, years earlier, had made it cheap to haul low-sulphur coal from "
            "Wyoming to power stations in the east."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), Create(goal), FadeIn(gl))
            vo.wait_until("b")
            self.play(Create(line), LaggedStart(*[FadeIn(d, scale=1.5) for d in dots], lag_ratio=0.3), FadeIn(vl),
                      FadeIn(side[1]), run_time=2)
            for mk, r in zip("cde", side[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def prices(self):
        ac = load("acid")
        p = ac["prices"]
        pts = [(2004.2, p["2004 auction"], r"2004 auction"), (2005.2, p["2005 auction"], r"2005 auction"),
               (2005.9, p["2005 peak"], r"peak, \ 2005"), (2008.2, p["2008 auction"], r"2008 auction"),
               (2008.53, p["11 July 2008, before"], r""), (2008.54, p["11 July 2008, after"], r"11 July 2008"),
               (2009.2, p["2009 auction"], r"2009 auction"), (2012.2, p["2012 spot auction"], r"2012 auction")]
        ax = plane([2003.5, 2013], [0, 1350], center=LEFT * 2.8 + DOWN * 0.3, x_length=6.4, y_length=4.6,
                   xticks=[2004, 2006, 2008, 2010, 2012], yticks=[0, 300, 600, 900, 1200], xlabel="",
                   ylabel=r"dollars a ton", font_size=16, xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:,.0f}")
        a = ax.ax
        dots = VGroup(*[Dot(a.c2p(x, y), radius=0.07, color=DEMAND) for x, y, _ in pts])
        line = VMobject(stroke_color=DEMAND, stroke_width=2.5).set_points_as_corners([a.c2p(x, y) for x, y, _ in pts])
        sides = [RIGHT, LEFT, RIGHT, LEFT, None, LEFT, RIGHT, UL]
        labs = VGroup()
        for (x, y, t_), d, sd in zip(pts, dots, sides):
            if t_:
                labs.add(label(rf"{t_}: \ \${y:,.2f}".replace(".00", ""), font_size=14, color=GREY_A).next_to(
                    d, sd, buff=0.1))
        side = VGroup(
            label(r"for a decade the price was steady", font_size=21),
            label(r"then expectations of a tighter cap \\ sent it past \$1,200 a ton", font_size=21, color=DEMAND),
            label(r"a court struck down the new rule: \\ in a day, \ \$315 to \$115", font_size=21, color=SOCIAL),
            label(r"the rules that replaced it \\ allowed little trading between states: \\ by 2012, \ 56 cents",
                  font_size=21, color=SOCIAL),
            label(r"a market the state creates, \\ the state can end", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Schmalensee and Stavins, JEP 27(1) (2013); \ EPA's auctions", corner=DR, font_size=13)
        with self.voiceover(
            "The market's prices tell the rest. <bookmark mark='a'/> For its first decade the allowance price was "
            "remarkably steady. <bookmark mark='b'/> Then, from 2004, the expectation of a tighter cap under a new "
            "rule sent it up: two hundred and seventy-three dollars a ton at the 2004 auction, seven hundred and "
            "three a year later, and past twelve hundred at the peak in 2005. <bookmark mark='c'/> In July 2008 a "
            "court struck down the new rule, and in one day the price fell from three hundred and fifteen dollars "
            "to a hundred and fifteen. <bookmark mark='d'/> The rules that replaced it set caps state by state, "
            "with little trading between them, and by the 2012 auction an allowance sold for fifty-six cents. "
            "<bookmark mark='e'/> A market the state creates, the state can end."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(VMobject(stroke_color=DEMAND, stroke_width=2.5).set_points_as_corners(
                [a.c2p(x, y) for x, y, _ in pts[:3]])), FadeIn(dots[:3]), FadeIn(labs[:3]), FadeIn(side[1]),
                run_time=2)
            vo.wait_until("c")
            self.play(Create(line), FadeIn(dots[3:6]), FadeIn(labs[3:5]), FadeIn(side[2]), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(dots[6:]), FadeIn(labs[5:]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["acid_rain_benefits"]
        ac = load("acid")
        b, k = ac["benefits_bn"], ac["costs_bn"]
        cc = call_card(r"Paul Portney and others, \ on the 1990 amendments", c.when,
                       r"the acid-rain programme's benefits \ would be about equal to its costs",
                       rf"benefits of \${b[0]} to \${b[1]} billion a year \ against costs of \${k[0]} to \${k[1]:.0f} "
                       r"billion; \ more than 95\% of the benefits from cleaner air in people's lungs, \ which "
                       r"nobody had counted", c.verdict, width=12.4, font_size=23).move_to(UP * 0.6)
        q = label(r"the ecological benefits alone \ probably did not cover the costs: \ the health benefits did, \ "
                  r"fifty times over", font_size=22, color=E.ACCENT).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"Portney, JEP 4(4) (1990); \ Schmalensee and Stavins, JEP 27(1) (2013), Table 1",
                            corner=DR, font_size=13)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> When the amendments passed, some careful estimates, Paul Portney's "
            "among them, put the acid-rain programme's benefits at about its costs. <bookmark mark='b'/> Twenty years "
            "on, the tally Schmalensee and Stavins gathered put the benefits at fifty-nine to a hundred and sixteen "
            "billion dollars a year, against costs of half a billion to two billion. More than ninety-five percent "
            "of the benefits came from something nobody had counted in 1990: fewer fine sulphate particles in the "
            "air people breathe, and fewer early deaths. <bookmark mark='c'/> Wrong, by a factor of fifty, and in "
            "the programme's favour: the benefits it was designed for, to lakes and forests, probably did not cover "
            "its costs; the ones nobody planned for did, many times over."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag))
            vo.wait_until("b")
            self.play(Indicate(cc.right, color=WHITE, scale_factor=1.01))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3), FadeIn(q))
        self.clear_scene()
