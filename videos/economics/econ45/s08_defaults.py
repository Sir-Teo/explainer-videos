from __future__ import annotations

from videos.economics.econ45.common import *  # noqa: F403


class Defaults(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Defaults and inertia", r"Why does the box that is already ticked win?",
             "Chapter seven. Defaults and inertia.",
             lit={2001: r"Madrian and Shea", 2004: r"Thaler and Benartzi"}, scale=("person", "firm"),
             horizon=("a year", "a decade"))
        self.madrian()
        self.island()
        self.why()
        self.smart()

    def madrian(self):
        steps = flow_chain([(r"before: \\ sign up to join", GREY_B), (r"after: \\ enrolled unless \\ you opt out",
                                                                      NUDGE),
                            (r"participation \\ jumps", GAIN), (r"and many stay \\ at the default", HOLD)],
                           notes=[r"the employer's \\ retirement plan", r"the same plan, \\ the same match",
                                  r"among new hires", r"its low rate \\ and safe fund"],
                           box_w=2.8, font_size=20, note_size=16).move_to(UP * 0.3)
        foot = label(r"Part 42 met defaults in pensions; \ this chapter asks why they stick", font_size=21,
                     color=GREY_A).to_edge(DOWN, buff=0.9)
        tag = published_tag(tables.DEFAULTS_45.tag, corner=DR, font_size=11)
        with self.voiceover(
            "In 2001 Brigitte Madrian and Dennis Shea studied a large American company that changed one thing in "
            "its retirement plan. <bookmark mark='a'/> Before, new employees had to sign up to join. "
            "<bookmark mark='b'/> After, new employees were enrolled automatically unless they chose to opt out. The "
            "plan, the employer's matching contribution and the investment choices were the same. "
            "<bookmark mark='c'/> Participation among new hires jumped, from 37 percent to 86 percent, as the "
            "authors later summarized it. <bookmark mark='d'/> And many of the new "
            "participants stayed exactly at the default: its low contribution rate and its conservative fund, "
            "which few had chosen before. For the agent of Part five, which box is ticked when you arrive should "
            "not matter. It matters enormously."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(foot), FadeIn(steps.boxes[0]), FadeIn(steps.notes[0]))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(steps.arrows[k]), FadeIn(steps.boxes[k + 1]), FadeIn(steps.notes[k + 1]))
        self.clear_scene()

    def island(self):
        N = load("enrol")
        months = np.arange(1, N["months"] + 1)
        ax = plane([0, N["months"]], [0, 1], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[0, 6, 12, 18, 24, 30, 36], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   xlabel=r"months since hire", ylabel=r"share saving in the plan", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        lines = {}
        for key, col, dash in (("opt_in_tc", TC, True), ("auto_tc", TC, False), ("opt_in_naif", NAIF, True),
                               ("auto_naif", NAIF, False)):
            ln = path(ax, months, N[key]["participation"], col, 3.0, smooth=False)
            lines[key] = DashedVMobject(ln, num_dashes=50) if dash else ln
        a12, o12 = N["auto_naif"]["participation"][11], N["opt_in_naif"]["participation"][11]
        side = VGroup(
            label(r"solid: \ enrolled unless \\ they opt out; \\ dashed: \ sign up to join", font_size=18, color=WHITE),
            label(r"grey: \ Part 5's workers: \\ the default does \\ not matter", font_size=18, color=TC),
            label(rf"pink: \ present-biased \\ naifs: \ {100 * o12:.0f}\% against \\ {100 * a12:.0f}\% after a year",
                  font_size=18, color=NAIF),
            label(rf"{100 * N['auto_naif']['at_default'][-1]:.0f}\% still at the default \\ rate after three years",
                  font_size=18, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.33).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The Island's new hires each have an ideal saving rate, zero for a few. Changing the rate takes an "
            "afternoon of forms, a cost paid now, while the gain comes over decades. <bookmark mark='a'/> For Part "
            "five's workers the default barely matters: within weeks nearly everyone is at their ideal rate, "
            "whichever box was ticked. <bookmark mark='b'/> Present-biased naifs are another story. Signing up "
            f"always looks better next month. A year in, {100 * o12:.0f} percent of them save when they must sign up, "
            f"and {100 * a12:.0f} percent when they are enrolled automatically. <bookmark mark='c'/> And after three "
            f"years, {100 * N['auto_naif']['at_default'][-1]:.0f} percent are still at the default rate, whatever "
            "their ideal. The default decides because the decision is put off."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(lines["opt_in_tc"]), Create(lines["auto_tc"]), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lines["opt_in_naif"]), Create(lines["auto_naif"]), FadeIn(side[2]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def why(self):
        eq = MathTex(r"\text{act now if}\quad k\,(1 - \beta\delta) \;\le\; \beta\, g", font_size=40,
                     color=THEORY).move_to(UP * 2.2)
        cards = point_cards([
            (r"procrastination", r"the effort is now, \\ the gain later; \\ next month always \\ looks better", NAIF),
            (r"endorsement", r"the default looks \\ like advice from \\ the employer", PLAN),
            (r"reference point", r"leaving the default \\ feels like a loss", SELL),
            (r"the designer's choice", r"there is always a \\ default: \ choosing it \\ is a policy", NUDGE),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.7)
        tag = published_tag(tables.DEFAULTS_45.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Why do defaults stick? <bookmark mark='a'/> The Island's answer is procrastination. Acting now costs "
            "the effort k now; waiting a month costs one month's gain g. A naif, believing next month's self will "
            "act, compares the two with the present cut by beta, and with a beta of 0.7 that means acting only when "
            "the effort is a small fraction of what a time-consistent worker would bear. <bookmark mark='b'/> In "
            "real plans, a default also reads as advice: the employer must think this is sensible. "
            "<bookmark mark='c'/> And it becomes the reference point, so leaving it feels like a loss. "
            "<bookmark mark='d'/> Whatever the reason, there is no neutral design. Some box is always ticked. Gabriel "
            "Carroll, James Choi, David Laibson, Brigitte Madrian and Andrew Metrick showed how to choose it: a "
            "default works well when people's needs are alike, and requiring an active choice works better when "
            "needs differ widely and people are prone to put decisions off."
        ) as vo:
            self.play(FadeIn(tag), Write(eq), FadeIn(cards.cards[0], shift=UP * 0.1), run_time=1.5)
            vo.wait_until("a")
            self.play(Indicate(eq, scale_factor=1.05))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def smart(self):
        N = load("enrol")
        S = N["smart"]
        path_ = np.array(S["path"])
        ax = plane([0, len(path_) - 1], [0, 0.16], center=LEFT * 2.2 + DOWN * 0.4, x_length=6.6, y_length=4.6,
                   xticks=list(range(len(path_))), yticks=[0, 0.04, 0.08, 0.12, 0.16], xlabel=r"pay rises",
                   ylabel=r"saving rate", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        ln = path(ax, range(len(path_)), path_, GAIN, 3.2, smooth=False)
        pts = VGroup(*[dot(ax, i, v, GAIN, 0.08) for i, v in enumerate(path_)])
        side = VGroup(
            label(r"Save More Tomorrow: \\ commit now to save \\ part of each future rise", font_size=19,
                  color=WHITE),
            label(r"the cost comes later \\ (present bias spares it) \\ and is never a cut in \\ take-home pay "
                  r"(no loss)", font_size=17, color=GREY_A),
            label(rf"Island: \ {100 * S['join_now']:.0f}\% would save \\ more now; \ "
                  rf"{100 * S['join_later']:.0f}\% sign up \\ for later", font_size=18, color=NUDGE),
            label(r"Thaler and Benartzi: \\ 3.5\% to 13.6\% \\ in 40 months", font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.33).to_edge(RIGHT, buff=0.35)
        tag = published_tag(tables.DEFAULTS_45.tag + r"; \ the Island", corner=DR, font_size=11)
        with self.voiceover(
            "If biases can block saving, can they be turned around to help it? <bookmark mark='a'/> Richard Thaler "
            "and Shlomo Benartzi designed Save More Tomorrow: workers commit today to put part of each future pay "
            "rise into saving. <bookmark mark='b'/> The design uses present bias, since the cost comes later, and "
            "loss aversion, since take-home pay never falls; and inertia then keeps people in. "
            f"<bookmark mark='c'/> On the Island, only {100 * S['join_now']:.0f} percent would raise their saving "
            f"now, but {100 * S['join_later']:.0f} percent sign up to raise it later, and with four rises their "
            f"rate climbs from {100 * path_[0]:.1f} to {100 * path_[-1]:.0f} percent. <bookmark mark='d'/> In the "
            "first company to use it, 78 percent of those offered the plan joined, and their average saving rate "
            "rose from three and a half percent to thirteen point six percent over forty months."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), FadeIn(pts[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(ln), LaggedStart(*[FadeIn(p) for p in pts[1:]], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
