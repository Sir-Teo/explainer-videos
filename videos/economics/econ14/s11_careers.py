from __future__ import annotations

from videos.economics.econ14.common import *  # noqa: F403


class Careers(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Career concerns and the ratchet", r"Without any bonus, \ why do the young work hard, \ and why "
             r"does a good year get punished?", "Chapter nine. Career concerns and the ratchet.",
             lit={1980: r"Weitzman's ratchet", 1982: r"Holmström's careers", 1992: r"Gibbons and Murphy"},
             scale=("person", "firm"), horizon=("a career",))
        self.careers()
        self.ratchet()
        self.remedies()

    def careers(self):
        k = load("careers")
        yrs, m, ex = np.array(k["year"]), np.array(k["implicit"]), np.array(k["explicit"])
        ax = plane([0.5, 30.5], [0, 1.0], center=LEFT * 2.8 + DOWN * 0.3, x_length=6.2, y_length=4.6,
                   xticks=[1, 10, 20, 30], yticks=[0, 0.25, 0.5, 0.75, 1], xlabel=r"year of a career",
                   ylabel=r"incentive per unit of output", font_size=16, xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.2f}")
        a = ax.ax
        cm = path(ax, yrs, m, color=SIGNAL, width=3.5)
        ce = path(ax, yrs, ex, color=PAY, width=3.5)
        lm = label(r"from the market's learning", font_size=15, color=SIGNAL).next_to(a.c2p(5, m[4]), RIGHT, buff=0.15)
        le = label(r"the best explicit bonus", font_size=15, color=PAY).next_to(a.c2p(20, ex[19]), UL, buff=0.08)
        side = VGroup(
            label(r"no one knows how able you are, \\ not even you", font_size=21),
            label(r"employers learn it from your record, \\ and pay what they believe", font_size=21, color=SIGNAL),
            label(r"so good work early raises \\ every later year's pay", font_size=21, color=SIGNAL),
            label(r"as the record grows, \ and the years left shrink, \\ that incentive fades", font_size=21,
                  color=RISK),
            label(r"so explicit pay should rise with age: \\ Gibbons and Murphy found it does, \\ for chief executives",
                  font_size=21, color=PAY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Holmström, RES 66(1) (1999; written 1982); \ Gibbons and Murphy, JPE 100(3) (1992); "
                            r"\ the curves: \ Agora", corner=DR, font_size=12)
        with self.voiceover(
            "There is a third kind of incentive, which needs no contract at all. <bookmark mark='a'/> Nobody knows "
            "for certain how able you are, not even you. <bookmark mark='b'/> Employers learn it from your record, "
            "and pay you what they believe you're worth. <bookmark mark='c'/> So good work early in a career raises "
            "your pay in every later year, through what it tells the market. Bengt Holmström worked this out in "
            "1982. Here the incentive is in Agora, for a thirty-year career. <bookmark mark='d'/> It is strongest at "
            "the start. As the record grows, each year's work tells employers less that is new, and fewer years "
            "remain to collect on it, so the incentive fades, to nothing in the last year. "
            "<bookmark mark='e'/> So explicit incentives should take over as careers age. In 1992 Robert Gibbons and "
            "Kevin Murphy derived the best explicit bonus on top of career concerns, rising as they fade, and found "
            "that chief executives' pay was indeed more tightly tied to performance in their last years before "
            "retirement."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cm), FadeIn(lm), FadeIn(side[2]), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(side[3]), Indicate(lm, color=RISK))
            vo.wait_until("e")
            self.play(Create(ce), FadeIn(le), FadeIn(side[4]), run_time=2)
        self.clear_scene()

    def ratchet(self):
        r = load("ratchet")
        years = [r"year 1", r"year 2", r"year 3", r"year 4"]
        out = [10, 14, 14, 14]
        target = [10, 10, 14, 14]
        ax = plane([0.4, 4.6], [0, 17], center=LEFT * 3.0 + DOWN * 0.4, x_length=5.6, y_length=4.4, xticks=[],
                   yticks=[0, 5, 10, 15], xlabel="", ylabel=r"output, \ and the target", font_size=16,
                   yfmt=lambda v: f"{v:.0f}")
        a = ax.ax
        u, uy = a.x_axis.get_unit_size(), a.y_axis.get_unit_size()
        bars = VGroup(*[Rectangle(width=0.45 * u, height=v * uy, stroke_width=0, fill_color=EFFORT,
                                  fill_opacity=0.8).move_to(a.c2p(i + 1, 0), aligned_edge=DOWN)
                        for i, v in enumerate(out)])
        tgts = VGroup(*[Line(a.c2p(i + 0.62, v), a.c2p(i + 1.38, v), color=RISK, stroke_width=4)
                        for i, v in enumerate(target)])
        names = VGroup(*[label(y_, font_size=16, color=GREY_B).next_to(a.c2p(i + 1, 0), DOWN, buff=0.15)
                         for i, y_ in enumerate(years)])
        key = VGroup(label(r"output", font_size=15, color=EFFORT), label(r"the target", font_size=15, color=RISK)
                     ).arrange(RIGHT, buff=0.4).next_to(ax, UP, buff=0.05).align_to(ax, RIGHT)
        side = VGroup(
            label(r"a bonus for each unit above the target", font_size=21),
            label(r"a good year: \ the planner learns what you can do, \\ and next year's target rises to it",
                  font_size=21, color=RISK),
            label(r"so each extra unit now \\ costs you a unit of bonus later", font_size=21, color=PAY),
            label(rf"with a target that ratchets up one for one, \\ and next year worth {r['delta']:.1f} of this one: "
                  rf"\\ effort falls from {r['effort_fixed_target']:.1f} to {r['effort_ratchet']:.1f}", font_size=21,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Weitzman, Bell Journal 11(1) (1980); \ the bars: \ illustrative; \ the effort: \ Agora",
                            corner=DR, font_size=13)
        with self.voiceover(
            "Learning can also work against effort. Soviet factories were set targets for each year's output, and "
            "their managers earned bonuses for beating them. <bookmark mark='a'/> Here is a bonus for each unit "
            "above the target. <bookmark mark='b'/> But the planners set next year's target from this year's "
            "output: a good year tells them what the factory can do, and the target rises to meet it. Soviet "
            "managers called it planning from the achieved level. <bookmark mark='c'/> So each extra unit this year "
            "costs the manager a unit of bonus next year. <bookmark mark='d'/> Martin Weitzman put it in a formula in "
            "1980. With a target that rises one for one, and next year worth nine tenths of this one, effort falls "
            "to a tenth of what a fixed target would get. The manager's best plan is to do just well "
            "enough, every year."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(names), FadeIn(key), FadeIn(side[0]), FadeIn(tag))
            self.play(GrowFromEdge(bars[0], DOWN), Create(tgts[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[1], DOWN), Create(tgts[1]), FadeIn(side[1]))
            self.play(Create(tgts[2]), GrowFromEdge(bars[2], DOWN))
            vo.wait_until("c")
            self.play(Create(tgts[3]), GrowFromEdge(bars[3], DOWN), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def remedies(self):
        rows = VGroup(
            label(r"the ratchet is everywhere a target is set from the record", font_size=25, color=E.ACCENT),
            label(r"sales quotas raised after a good year; \ budgets cut when a department spends less", font_size=23),
            label(r"the cure is commitment: \ fix the targets before the results are in", font_size=24,
                  color=EFFORT),
            label(r"Britain's privatized utilities: \ price caps fixed for years at a time, \ so savings are kept "
                  r"until the next review", font_size=22, color=PAY),
            label(r"but a principal who has learnt something is tempted to use it: \ commitment is hard", font_size=23,
                  color=RISK),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        tag = published_tag(r"Weitzman (1980); \ Laffont and Tirole, \ A Theory of Incentives in Procurement and "
                            r"Regulation (1993)", corner=DR, font_size=13)
        with self.voiceover(
            "The ratchet was not only a Soviet problem. <bookmark mark='a'/> It appears wherever a target is set "
            "from the record. <bookmark mark='b'/> Sales quotas are raised after a good year; a department that "
            "spends less than its budget has the budget cut. <bookmark mark='c'/> The cure is commitment: fix the "
            "targets before the results come in, and keep them fixed. <bookmark mark='d'/> When Britain privatized "
            "its utilities, their prices were capped for several years at a time, often five, so that a company that "
            "cut its costs kept the savings until the next review. <bookmark mark='e'/> But a principal who has learnt something "
            "is tempted to use it, and the agent knows that. Jean-Jacques Laffont and Jean Tirole worked out what "
            "that does to contracts when the principal can't commit."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
