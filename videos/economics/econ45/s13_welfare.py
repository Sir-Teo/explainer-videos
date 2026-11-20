from __future__ import annotations

from videos.economics.econ45.common import *  # noqa: F403


class Welfare(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Behavioural welfare", r"If choices conflict, which one counts?",
             "Chapter eleven. Behavioural welfare.",
             lit={2003: r"Thaler and Sunstein", 2009: r"Bernheim and Rangel"}, scale=("person", "nation"),
             horizon=("a year",))
        self.frames()
        self.nudge()
        self.disclose()

    def frames(self):
        R = behave.welfare_range({"must sign up": 30.0, "enrolled already": 80.0})
        nl = NumberLine(x_range=[0, 100, 10], length=10.5, include_numbers=False, color=GREY_B).move_to(DOWN * 0.3)
        nums = VGroup(*[label(f"{v}", font_size=16, color=GREY_B).next_to(nl.n2p(v), DOWN, buff=0.15)
                        for v in range(0, 101, 20)])
        cap = label(r"what joining the plan is worth to this worker, \ dollars", font_size=18,
                    color=GREY_A).next_to(nums, DOWN, buff=0.2)
        lo, hi = R["lo"], R["hi"]
        rng_ = Line(nl.n2p(lo), nl.n2p(hi), stroke_width=10, color=HOLD)
        fa = VGroup(Dot(nl.n2p(lo), color=PLAN, radius=0.1),
                    label(rf"frame 1: \ must sign up \\ acts as if worth below \${lo:.0f}", font_size=17,
                          color=PLAN).next_to(nl.n2p(lo), UP, buff=0.35))
        fb = VGroup(Dot(nl.n2p(hi), color=NUDGE, radius=0.1),
                    label(rf"frame 2: \ enrolled already \\ acts as if worth above \${hi:.0f}", font_size=17,
                          color=NUDGE).next_to(nl.n2p(hi), UP, buff=0.35))
        verdicts = VGroup()
        for cost, col in ((20, GAIN), (55, HOLD), (90, LOSS)):
            v = behave.welfare_range({"a": lo, "b": hi}, cost)["verdict"]
            verdicts.add(VGroup(Triangle(color=col, fill_opacity=1).scale(0.1).rotate(PI).next_to(nl.n2p(cost), UP,
                                                                                                 buff=1.5),
                                label(rf"a policy costing \${cost}: \\ {v}", font_size=16, color=col).next_to(
                                    nl.n2p(cost), UP, buff=1.75)))
        head = label(r"Bernheim and Rangel: \ count only what every frame agrees on", font_size=26,
                     color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(tables.WELFARE_45.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Welfare economics, from Part nine to Part forty-two, measured well-being by choices: what you choose "
            "is what you prefer. Behavioural economics breaks that link. <bookmark mark='a'/> Take a worker who "
            "never joins a pension plan when joining means signing up, as if joining were worth less than an "
            f"afternoon of forms, say {lo:.0f} dollars. <bookmark mark='b'/> Enrolled automatically, the same "
            f"worker stays in, as if joining were worth more than {hi:.0f}. Which choice reveals what this worker "
            "wants? "
            "<bookmark mark='c'/> Douglas Bernheim and Antonio Rangel proposed an answer: when choices conflict "
            "across frames that should not matter, trust only what they agree on. The worker's value of joining is "
            "somewhere "
            f"between {lo:.0f} and {hi:.0f}. <bookmark mark='d'/> A policy that costs the worker less than {lo:.0f} "
            f"makes them better off whichever frame you believe. One that costs more than {hi:.0f} makes them worse "
            "off. In between, the choices do not say, and the economist should admit it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Create(nl), FadeIn(nums), FadeIn(cap), run_time=1.2)
            vo.wait_until("a")
            self.play(FadeIn(fa))
            vo.wait_until("b")
            self.play(FadeIn(fb))
            vo.wait_until("c")
            self.play(Create(rng_))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(v, shift=DOWN * 0.1) for v in verdicts], lag_ratio=0.5), run_time=2.0)
        self.clear_scene()

    def nudge(self):
        cols = VGroup()
        spec = [(r"the case for nudges", NUDGE, [r"there is always a default, \\ a menu, \ an order",
                                                  r"choose them to help, \\ and keep every option open",
                                                  r"cheap, \ and easy \\ to opt out of"]),
                (r"the objections", LOSS, [r"who decides what \\ is good for you?",
                                           r"the same tools sell: \\ sludge, \ dark patterns",
                                           r"small effects can \\ crowd out real reform"])]
        for title, col, rows in spec:
            t = label(title, font_size=25, color=col)
            body = VGroup(*[label(r_, font_size=20, color=WHITE) for r_ in rows]).arrange(DOWN, aligned_edge=LEFT,
                                                                                           buff=0.4)
            cols.add(VGroup(t, body).arrange(DOWN, aligned_edge=LEFT, buff=0.45))
        cols.arrange(RIGHT, buff=1.6, aligned_edge=UP).move_to(DOWN * 0.1)
        head = label(r"libertarian paternalism, \ and its critics", font_size=28, color=E.ACCENT).to_edge(UP,
                                                                                                      buff=0.6)
        tag = published_tag(tables.WELFARE_45.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Richard Thaler and Cass Sunstein turned this into a policy philosophy they called libertarian "
            "paternalism, and popularized as nudging. <bookmark mark='a'/> Some default, some menu, some order is "
            "unavoidable, so choose them to help people, as judged by themselves, while keeping every option open "
            "and cheap to take. <bookmark mark='b'/> The objections are serious. Who decides what helps? The "
            "designer may be wrong, or have interests of its own. <bookmark mark='c'/> The same tools sell as "
            "easily as they help: Thaler's own word for frictions that keep people from what they want is sludge, "
            "like the subscription that takes one click to start and an hour to cancel. <bookmark mark='d'/> And "
            "a cheap nudge can become an excuse not to change prices, rules or institutions, where most of the "
            "leverage is."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cols[0][0]), FadeIn(cols[1][0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in cols[0][1]], lag_ratio=0.5), run_time=2.0)
            for mk, r_ in zip("bcd", cols[1][1]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def disclose(self):
        D = load("disclose")
        keys = ("0.0", "0.5", "1.0")
        ax = plane([0, 3], [0, 30], center=LEFT * 2.4 + DOWN * 0.4, x_length=6.4, y_length=4.6, xticks=[],
                   yticks=[0, 10, 20, 30], ylabel=r"members' average real gain, \ dollars a month",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        bars = VGroup()
        for i, (k, nm) in enumerate(zip(keys, (r"no rule", r"half of naifs \\ believe it", r"all believe it"))):
            v = D[k]["gain"]
            p0, p1 = ax.ax.c2p(0.5 + i - 0.32, 0), ax.ax.c2p(0.5 + i + 0.32, v)
            r = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=[GREY_B, SOPH, GAIN][i],
                          fill_opacity=0.85).move_to((p0 + p1) / 2)
            bars.add(VGroup(r, label(nm, font_size=15, color=WHITE).next_to(r, DOWN, buff=0.12),
                            label(dollars(v), font_size=17, color=WHITE).next_to(r, UP, buff=0.08)))
        side = VGroup(
            label(r"the rule: \ tell each member \\ how often members \\ like them actually go", font_size=19,
                  color=WHITE),
            label(rf"monthly contracts: \\ {100 * D['0.0']['monthly']:.0f}\% $\to$ {100 * D['1.0']['monthly']:.0f}\%",
                  font_size=19, color=GYM),
            label(r"nobody is forced; \\ the gain comes from \\ better forecasts", font_size=19, color=E.ACCENT),
            label(r"but only if people \\ believe the number", font_size=19, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The Island can test a rule that respects choice. <bookmark mark='a'/> The gym must tell each would-be "
            "member how often members like them actually go. <bookmark mark='b'/> If no naif believes it, nothing "
            f"changes: members gain {money_words(D['0.0']['gain'])} a month on average from the gym, after paying for "
            f"it. If half of them believe it, {money_words(D['0.5']['gain'])}. If all do, "
            f"{money_words(D['1.0']['gain'])}, and the share on monthly contracts falls from "
            f"{100 * D['0.0']['monthly']:.0f} to {100 * D['1.0']['monthly']:.0f} percent. <bookmark mark='c'/> No "
            "contract was banned and nobody was told what to buy. The gain comes from better forecasts. "
            "<bookmark mark='d'/> But it depends entirely on whether people take the number to apply to them, and "
            "naifs, by definition, think they are the exception."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(bars[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars[1]), FadeIn(bars[2]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
