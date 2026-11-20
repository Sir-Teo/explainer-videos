from __future__ import annotations

from videos.economics.econ45.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 15, r"In practice: \ products, \ protection, \ pensions", r"Who uses these ideas, and how?",
             "Chapter fifteen. In practice: products, protection, pensions.",
             lit={2022: r"SECURE 2.0", 2025: r"\emph{click to cancel}, vacated"}, scale=("firm", "nation"),
             horizon=("a year",))
        self.people()
        self.cancel()
        self.pensions()
        self.called()

    def people(self):
        rows = VGroup(
            label(r"product teams: \ defaults, \ sign-up and cancellation flows, \ tested in experiments", font_size=22,
                  color=FIRM),
            label(r"consumer-protection agencies: \ disclosure, \ cancellation and fee rules", font_size=22,
                  color=LOSS),
            label(r"pension designers: \ automatic enrollment and escalation", font_size=22, color=NUDGE),
            label(r"government behavioural teams: \ letters, \ forms and reminders, \ tested at scale", font_size=22,
                  color=PLAN),
            label(r"economists in all four: \ estimating the bias, \ and who gains and loses", font_size=22,
                  color=GYM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN * 0.2)
        head = label(r"the people who use this", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.PRACTICE_45.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Who uses behavioural economics? <bookmark mark='a'/> Product teams, who design defaults and the "
            "steps of signing up and cancelling, and test them in experiments on millions of users. "
            "<bookmark mark='b'/> Consumer-protection agencies, who write rules about disclosure, cancellation and "
            "fees. <bookmark mark='c'/> Pension designers, who choose defaults for whole workforces. "
            "<bookmark mark='d'/> Government behavioural teams, who redesign letters and forms and test them at the "
            "scale of chapter twelve. <bookmark mark='e'/> And economists in all four places, whose job is to "
            "estimate the bias, and to say who gains and who loses from a design."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0], shift=RIGHT * 0.1))
            vo.wait_until("a")
            self.play(Indicate(rows[0], color=WHITE, scale_factor=1.03))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def cancel(self):
        steps = flow_chain([(r"easy to start, \\ hard to stop", LOSS), (r"a federal rule: \\ cancel as easily \\ as "
                                                                        r"you signed up", NUDGE),
                            (r"vacated, \\ 8 July 2025", HOLD), (r"other law \\ remains", PLAN)],
                           notes=[r"subscriptions that \\ renew automatically", r"the FTC's \\ ``click to cancel'' "
                                  r"rule", r"on procedure: \\ a required analysis \\ was not prepared",
                                  r"the 1973 rule, \\ state renewal laws"],
                           box_w=2.8, font_size=19, note_size=16).move_to(UP * 0.4)
        foot = label(r"sludge: \ frictions that keep people from what they want, \ and the gym's renewal of chapter "
                     r"five", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.8)
        tag = published_tag(tables.PRACTICE_45.tag, corner=DR, font_size=11)
        with self.voiceover(
            "A case in consumer protection. <bookmark mark='a'/> Subscriptions that renew automatically are easy to "
            "start and can be hard to stop: the inattention and procrastination of this part, turned into revenue. "
            "<bookmark mark='b'/> America's Federal Trade Commission wrote a rule requiring that cancelling be as "
            "easy as signing up. <bookmark mark='c'/> On the eighth of July 2025, days before it was to take "
            "effect, a federal appeals court vacated it, not on its merits but on procedure: the Commission had not "
            "prepared a preliminary analysis the law requires for rules with large economic effects. "
            "<bookmark mark='d'/> An older rule from 1973 and many states' automatic-renewal laws remain. The "
            "economics of the question is the gym's: a contract that profits when members forget to cancel."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(foot), FadeIn(steps.boxes[0]))
            vo.wait_until("a")
            self.play(FadeIn(steps.notes[0]))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(steps.arrows[k]), FadeIn(steps.boxes[k + 1]), FadeIn(steps.notes[k + 1]))
        self.clear_scene()

    def pensions(self):
        cards = point_cards([
            (r"the law", r"SECURE 2.0 \ (2022): \\ new 401(k) and 403(b) \\ plans must enroll \\ automatically", NUDGE),
            (r"the default rate", r"between 3\% and 10\%, \\ rising each year", GAIN),
            (r"the evidence", r"chapter seven: \\ participation 37\% \\ to 86\%", PLAN),
            (r"the trade-off", r"a low default \\ anchors some \\ who would have \\ saved more", HOLD),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.2)
        head = label(r"pensions: \ the default becomes the law", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.PRACTICE_45.tag, corner=DR, font_size=11)
        with self.voiceover(
            "In pensions, the default has become law. <bookmark mark='a'/> America's SECURE 2.0 Act of 2022 "
            "requires most newly established 401(k) and 403(b) plans to enroll eligible workers automatically. "
            "<bookmark mark='b'/> The default contribution must be between three and ten percent, and rise each "
            "year, which builds in Save More Tomorrow's escalation. <bookmark mark='c'/> The evidence behind it is "
            "chapter seven's. <bookmark mark='d'/> The trade-off is chapter seven's too: a low default brings in "
            "people who would not have saved, but can anchor some who would have saved more, which is why "
            "escalation matters."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(Circumscribe(cards.cards[0], color=WHITE, buff=0.05))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["experts_2018"]
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.6,
                       font_size=19)
        cc.move_to(UP * 1.3)
        ax = plane([0, 3], [0, 150], center=DOWN * 2.0, x_length=6.0, y_length=2.2, xticks=[], yticks=[0, 100],
                   yfmt=lambda v: f"{v:.0f}", font_size=13)
        vals = [(r"no piece rate", 100, GREY_B), (r"0.1 cent", 124, GAIN), (r"1 cent", 133, NUDGE)]
        bars = VGroup()
        for i, (nm, v, col) in enumerate(vals):
            p0, p1 = ax.ax.c2p(0.5 + i - 0.3, 0), ax.ax.c2p(0.5 + i + 0.3, v)
            r = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                          fill_opacity=0.85).move_to((p0 + p1) / 2)
            bars.add(VGroup(r, label(nm, font_size=14, color=WHITE).next_to(r, DOWN, buff=0.08),
                            label(f"{v}", font_size=14, color=WHITE).next_to(r, UP, buff=0.05)))
        cap = label(r"effort, \ no piece rate = 100", font_size=14, color=GREY_A).next_to(ax, LEFT, buff=0.3)
        tag = published_tag(tables.PRACTICE_45.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> Stefano DellaVigna and Devin Pope ran a large online experiment "
            "of a simple real-effort task with eighteen ways of motivating people, and before the results came out "
            "asked 208 "
            "experts to forecast each one. <bookmark mark='a2'/> One arm paid a token piece rate, a tenth of a cent. A "
            "sizeable share of "
            "the experts expected it to crowd out effort: people paid almost nothing would work less than people "
            "paid nothing at all, as with the day-care fine. <bookmark mark='b'/> Instead, effort was 24 percent "
            "higher than with no piece rate, and a full cent added more. <bookmark mark='c'/> The verdict: wrong. "
            "The experts did well on much else, and their average forecast beat most of them individually. But a "
            "famous story is not a law of nature, which is the lesson of this whole part."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1][0]), FadeIn(cc.left), FadeIn(tag))
            vo.wait_until("a2")
            self.play(FadeIn(ax), FadeIn(cap), GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1:]),
                      *[FadeIn(b_[1]) for b_ in bars[1:]])
            vo.wait_until("b")
            self.play(FadeIn(cc.right), LaggedStart(*[GrowFromEdge(b_[0], DOWN) for b_ in bars[1:]], lag_ratio=0.3),
                      *[FadeIn(b_[2]) for b_ in bars[1:]], run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3))
        self.clear_scene()
