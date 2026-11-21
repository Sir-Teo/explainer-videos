from __future__ import annotations

from videos.economics.econ50.common import *  # noqa: F403


def _k(v):
    return f"{v / 1000:.0f}k" if v else "0"


class Market(VoiceoverScene):
    def construct(self):
        card(self, 2, r"The family's budget, \ before and after", r"What does the allowance change for one family?",
             "Chapter two. The family's budget, before and after.", lit={1975: r"the EITC", 2021: r"ARPA"},
             scale=("household",), horizon=("a year",))
        self.credits()
        self.difference()
        self.budget_line()
        self.effects()

    def credits(self):
        S = load("schedules")
        e = np.array(S["earnings"]) / 1000
        ax = plane([0, 150], [0, 8000], center=LEFT * 1.5 + DOWN * 0.35, x_length=8.6, y_length=4.6,
                   xticks=[0, 25, 50, 75, 100, 125, 150], yticks=[0, 2000, 4000, 6000, 8000],
                   xlabel=r"earnings, \ thousands of dollars a year", ylabel=r"credit a year, \ \$",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:,.0f}".replace(",", "{,}"), font_size=14)
        eitc = path(ax, e, S["eitc"], EITC, 3.0, smooth=False)
        old = path(ax, e, S["ctc"], OLD, 3.2, smooth=False)
        new = path(ax, e, S["allowance"], NEW, 3.4, smooth=False)
        side = VGroup(
            label(r"a single parent \\ of two: \ one child \\ under six, \ one older", font_size=18, color=WHITE),
            label(r"blue: \ the EITC, \\ kept in both", font_size=18, color=EITC),
            label(r"grey: \ the old credit, \\ phased in with \\ earnings", font_size=18, color=OLD),
            label(r"gold: \ the allowance, \\ 6,600 from \\ the first dollar".replace("6,600", "6{,}600"),
                  font_size=18, color=NEW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.4)
        tag = published_tag(r"the rules of IRC ss. 24 and 32, \ 2021; \ drawn here", corner=DR, font_size=12)
        with self.voiceover(
            "Before any economics, the arithmetic of one family. Take a single parent with two children, one under "
            "six and one older. <bookmark mark='a'/> Both systems keep the earned income tax credit, the EITC of "
            "Part forty-one: it rises with earnings to almost six thousand dollars, stays flat, then fades out "
            "above twenty thousand. <bookmark mark='b'/> The old child credit also rose with earnings: fifteen "
            "cents per dollar earned above twenty-five hundred, until it reached its full four thousand dollars "
            "once the family earned enough and owed enough tax. <bookmark mark='c'/> The allowance is flat: six "
            "thousand six hundred dollars from the first dollar, or from no dollar at all, fading only above "
            "seventy-five thousand."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(side[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(eitc), FadeIn(side[1]), run_time=1.8)
            vo.wait_until("b")
            self.play(Create(old), FadeIn(side[2]), run_time=1.8)
            vo.wait_until("c")
            self.play(Create(new), FadeIn(side[3]), run_time=1.8)
        self.wait(0.5)
        self.clear_scene()

    def difference(self):
        S = load("schedules")
        e = np.array(S["earnings"]) / 1000
        d = np.array(S["allowance"]) - np.array(S["ctc"])
        ax = plane([0, 150], [0, 7000], center=LEFT * 1.5 + DOWN * 0.35, x_length=8.6, y_length=4.6,
                   xticks=[0, 25, 50, 75, 100, 125, 150], yticks=[0, 2000, 4000, 6000],
                   xlabel=r"earnings, \ thousands of dollars a year", ylabel=r"allowance minus old credit, \ \$",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:,.0f}".replace(",", "{,}"), font_size=14)
        area = band(ax, e, np.zeros_like(d), d, NEW, 0.25)
        line = path(ax, e, d, NEW, 3.2, smooth=False)
        p0 = dot(ax, 0, d[0], NEW, 0.08)
        mid = dot(ax, 50, S["new_full"] - S["old_full"], NEW, 0.08)
        end = dot(ax, S["diff_zero_at"] / 1000, 0, NEW, 0.08)
        notes = VGroup(
            label(rf"no earnings: \ +\${d[0]:,.0f}".replace(",", "{,}"), font_size=16, color=NEW).next_to(p0, UR,
                                                                                                    buff=0.1),
            label(rf"middle: \ +\${S['new_full'] - S['old_full']:,.0f}".replace(",", "{,}"), font_size=16,
                  color=NEW).next_to(mid, UP, buff=0.15),
            label(rf"nothing above \${S['diff_zero_at'] / 1000:.0f}k", font_size=16, color=NEW).next_to(end, UR,
                                                                                                    buff=0.12),
        )
        side = VGroup(
            label(r"the gain is largest \\ where the old credit \\ was smallest", font_size=19, color=WHITE),
        ).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Now subtract: what the allowance adds, at each level of earnings. <bookmark mark='a'/> A family with "
            f"no earnings gains the whole {d[0]:,.0f} dollars. <bookmark mark='b'/> The gain shrinks as the old "
            "credit phases in, <bookmark mark='c'/> and in the middle it is twenty-six hundred dollars, the "
            "difference between the new amounts and the old two thousand a child. <bookmark mark='d'/> Above "
            f"seventy-five thousand the extra fades, and above {S['diff_zero_at'] / 1000:.0f} thousand there is "
            "none. <bookmark mark='e'/> So the allowance gives the most to the families that earn the least: the "
            "gain is largest exactly where the old credit was smallest."
        ) as vo:
            self.play(FadeIn(ax))
            vo.wait_until("a")
            self.play(FadeIn(p0), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(area), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(mid), FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(end), FadeIn(notes[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[0]), Indicate(VGroup(p0, notes[0]), color=WHITE))
        self.clear_scene()

    def budget_line(self):
        S = load("schedules")
        e = np.array(S["earnings"]) / 1000
        k = e <= 40.01
        ax = plane([0, 40], [0, 50], center=LEFT * 1.6 + DOWN * 0.35, x_length=7.6, y_length=4.8,
                   xticks=[0, 10, 20, 30, 40], yticks=[0, 10, 20, 30, 40, 50],
                   xlabel=r"earnings, \ thousands", ylabel=r"income after taxes and credits, \ thousands",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        diag = seg(ax, 0, 0, 40, 40, GREY_C, 1.6, dashed=True)
        old = path(ax, e[k], np.array(S["net_old"])[k] / 1000, OLD, 3.2, smooth=False)
        new = path(ax, e[k], np.array(S["net_new"])[k] / 1000, NEW, 3.4, smooth=False)
        a0 = dot(ax, 0, S["at0_old"] / 1000, OLD, 0.08)
        b0 = dot(ax, 0, S["at0_new"] / 1000, NEW, 0.08)
        go = S["gain_work_old_20k"]
        gn = S["gain_work_new_20k"]
        y_old20 = S["at0_old"] + go
        y_new20 = S["at0_new"] + gn
        a1 = dot(ax, 20, y_old20 / 1000, OLD, 0.08)
        b1 = dot(ax, 20, y_new20 / 1000, NEW, 0.08)
        br_old = Line(ax.ax.c2p(21.2, S["at0_old"] / 1000), ax.ax.c2p(21.2, y_old20 / 1000), color=OLD,
                      stroke_width=2.4)
        br_new = Line(ax.ax.c2p(22.4, S["at0_new"] / 1000), ax.ax.c2p(22.4, y_new20 / 1000), color=NEW,
                      stroke_width=2.4)
        side = VGroup(
            label(r"dashed: \ earnings alone", font_size=18, color=GREY_B),
            label(rf"not working: \ \${S['at0_old']:,.0f} \ against \ \${S['at0_new']:,.0f}".replace(",", "{,}"),
                  font_size=18, color=WHITE),
            label(rf"what working at 20k adds: \\ old \${go:,.0f}, \ new \${gn:,.0f}".replace(",", "{,}"),
                  font_size=18, color=WHITE),
            label(rf"the reward for working \\ falls by {100 * (1 - gn / go):.0f}\%", font_size=20, color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Put the credits into the family's budget line: income after taxes and credits, against earnings. "
            "<bookmark mark='a'/> The grey line is the old system. The parent's income rises faster than earnings "
            "at first, because both credits are phased in. <bookmark mark='b'/> The gold line is the allowance: "
            "higher everywhere, by most at the bottom. <bookmark mark='c'/> A parent who does not work had "
            f"nothing from these credits before, and has {S['at0_new']:,.0f} dollars now. <bookmark mark='d'/> "
            f"Now the decision to work. Under the old credit, working at twenty thousand dollars added {go:,.0f} "
            "dollars to the family's income, earnings plus both credits less a little tax. <bookmark mark='e'/> "
            f"Under the allowance it adds {gn:,.0f}: the {S['old_at_20k']:,.0f} dollars of child credit that work "
            "used to earn now come anyway. <bookmark mark='f'/> The reward for working falls by about a tenth for "
            "this parent. That single number is where the memo's hardest disagreement begins."
        ) as vo:
            self.play(FadeIn(ax), Create(diag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(old), run_time=1.8)
            vo.wait_until("b")
            self.play(Create(new), run_time=1.8)
            vo.wait_until("c")
            self.play(FadeIn(a0), FadeIn(b0), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(a1), Create(br_old), FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(b1), Create(br_new))
            vo.wait_until("f")
            self.play(FadeIn(side[3]), Indicate(VGroup(br_old, br_new), color=WHITE))
        self.clear_scene()

    def effects(self):
        cards = point_cards([
            (r"the income effect", r"6,600 more whether or not the parent works: \ with more money, \ some will "
                                   r"choose to work less".replace("6,600", "6{,}600"), NEW),
            (r"the end of the phase-in", r"the old credit paid 15 cents per dollar earned at the bottom; \ now "
                                         r"nothing: \ a smaller reward for starting work", LOSS),
            (r"in the middle", r"no change at the margin: \ 2,600 more, \ the same reward for an extra hour"
             .replace("2,600", "2{,}600"), GREY_A),
            (r"above 75,000".replace("75,000", "75{,}000"), r"the phase-out takes 5 cents a dollar: \ a small new "
                                                            r"tax on extra earnings", BUDGET),
        ], width=12.4, cols=2, font_size=21).move_to(DOWN * 0.1)
        head = label(r"two effects on work, \ and where they bite", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        foot = label(r"both point the same way at the bottom: \ the size of the response is an empirical question",
                     font_size=21, color=WHITE).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Two effects, from the theory of Part thirty-eight. <bookmark mark='a'/> The income effect: the "
            "family has more money whether or not the parent works, and with more money some people choose to "
            "work less. <bookmark mark='b'/> And the end of the phase-in: the old credit paid fifteen cents for "
            "each dollar earned at the bottom, a reward for starting work that the allowance removes. <bookmark "
            "mark='c'/> In the middle nothing changes at the margin: the family has more, but an extra hour pays "
            "the same. <bookmark mark='d'/> Above seventy-five thousand, the phase-out takes five cents of each "
            "extra dollar, a small new tax. <bookmark mark='e'/> At the bottom both effects point towards less "
            "work. Theory gives the direction; only evidence can give the size."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(foot, shift=UP * 0.1))
        self.clear_scene()
