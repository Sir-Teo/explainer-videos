from __future__ import annotations

from videos.economics.econ44.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 14, r"In practice: \ platform strategy and the agencies", r"Who uses these tools, and how?",
             "Chapter fourteen. In practice: platform strategy and the agencies.", lit={2007: r"the iPhone"},
             scale=("firm", "market"), horizon=("a year", "a decade"))
        self.who()
        self.strategy()
        self.called()

    def who(self):
        rows = VGroup(
            label(r"agency economists: \ dynamic and platform cases, \ retrospectives of past mergers", font_size=20,
                  color=PATIENT),
            label(r"platform firms: \ pricing each side, \ subsidizing the side others follow", font_size=20,
                  color=FIRM2),
            label(r"utilities' regulators: \ price caps, \ cost sharing, \ the information problem", font_size=20,
                  color=FIRM1),
            label(r"operations teams: \ replacement and maintenance, \ Zurcher's problem at scale", font_size=20,
                  color=BUS),
            label(r"pricing teams: \ learning algorithms, \ and what they may and may not do", font_size=20,
                  color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN * 0.1)
        head = label(r"the people who do this", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Who uses these tools? <bookmark mark='a'/> Economists at the agencies, who analyse dynamic and platform "
            "cases and study past mergers to learn from them. <bookmark mark='b'/> Platform firms themselves, which "
            "set a price on each side and decide which side to subsidize. <bookmark mark='c'/> Regulators of "
            "utilities, who design price caps and cost-sharing rules under the information problem of chapter "
            "twelve. <bookmark mark='d'/> Operations teams at airlines, railways and fleets, who solve Zurcher's "
            "problem every day, at scale. <bookmark mark='e'/> And pricing teams, who deploy learning algorithms "
            "and must now ask what those algorithms are allowed to learn."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def strategy(self):
        steps = flow_chain([(r"find the side \\ others follow", FIRM1), (r"subsidize it", PATIENT),
                            (r"charge the \\ other side", FIRM2), (r"keep both", GAIN)],
                           notes=[r"developers follow \\ users; \ advertisers \\ follow readers", r"free accounts, \\ "
                                  r"rewards, \ cheap \\ hardware", r"fees, \ commissions, \\ advertising",
                                  r"multihoming, \ switching \\ costs, \ quality"],
                           box_w=2.8, font_size=19, note_size=16).move_to(UP * 0.5)
        foot = label(r"the same strategy, \ seen from the agency, \ is the question of chapter six", font_size=21,
                     color=E.ACCENT).to_edge(DOWN, buff=0.9)
        tag = published_tag(tables.PLATFORMS.tag, corner=DR, font_size=11)
        with self.voiceover(
            "A platform's strategy, in four steps. <bookmark mark='a'/> Find the side the other side follows: "
            "developers follow users, advertisers follow readers. <bookmark mark='b'/> Subsidize it, with free "
            "accounts, rewards or cheap hardware. <bookmark mark='c'/> Charge the other side, in fees, commissions "
            "or advertising. <bookmark mark='d'/> And keep both, against rivals who would like users to join "
            "several platforms at once. <bookmark mark='e'/> Seen from the agency, the same strategy raises the "
            "questions of chapter six: is a price below cost efficient, or the start of a lock-in?"
        ) as vo:
            self.play(FadeIn(tag), FadeIn(steps.boxes[0]))
            vo.wait_until("a")
            self.play(FadeIn(steps.notes[0]))
            for k, mk in zip(range(3), "bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(steps.arrows[k]), FadeIn(steps.boxes[k + 1]), FadeIn(steps.notes[k + 1]))
            vo.wait_until("e")
            self.play(FadeIn(foot, shift=UP * 0.1))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["ballmer_2007"]
        A = tables.APPLE.data
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.6,
                       font_size=20)
        cc.move_to(UP * 1.25)
        loop = flow_chain([(r"buyers", FIRM2), (r"developers", PATIENT), (r"apps", PATIENT), (r"more buyers", FIRM2)],
                          box_w=2.3, box_h=0.75, buff=0.5, font_size=19).move_to(DOWN * 1.9)
        why = label(r"the reasoning: \ an expensive phone, \ against software that ran \\ on many makers' "
                    r"handsets", font_size=20, color=E.PRED).move_to(DOWN * 1.9)
        tag = published_tag(tables.APPLE.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> In April 2007, months before the first iPhone went on sale, Microsoft's "
            "chief executive, Steve Ballmer, told USA Today: there's no chance that the iPhone is going to get any "
            "significant market share. No chance. <bookmark mark='a2'/> The phone was expensive, and Microsoft's own "
            "mobile software ran "
            "on handsets from many makers. <bookmark mark='b'/> What followed was a two-sided platform: buyers "
            "attracted developers, whose apps attracted more buyers. <bookmark mark='b2'/> In 2023 Apple shipped "
            f"{A['units']} million smartphones, {A['share']} percent of the world market and the most of any maker, "
            "according to IDC, and Microsoft had left the phone business. <bookmark mark='c'/> The verdict: "
            "wrong. Network effects can lock a market in, but a new platform that wins one side can also tip it the "
            "other way."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1][0]), FadeIn(cc.left), FadeIn(tag))
            vo.wait_until("a2")
            self.play(FadeIn(why, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeOut(why), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(b) for b in loop.boxes], lag_ratio=0.4),
                      LaggedStart(*[GrowArrow(a) for a in loop.arrows], lag_ratio=0.4), run_time=2.6)
            vo.wait_until("b2")
            self.play(FadeIn(cc.right, shift=LEFT * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3))
        self.clear_scene()
