from __future__ import annotations

from videos.economics.econ47.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 15, r"In practice: \ governance, \ regulation, \ political risk", r"Who uses these ideas, and how?",
             "Chapter fifteen. In practice: governance, regulation and political risk.",
             lit={2016: r"HM Treasury"}, scale=("organization", "nation"), horizon=("a year",))
        self.people()
        self.design()
        self.called()

    def people(self):
        rows = VGroup(
            label(r"governance teams: \ audits, \ procurement, \ published budgets, \ at development banks and "
                  r"ministries", font_size=21, color=AUDIT),
            label(r"regulators: \ designing agencies that are hard to capture", font_size=21, color=LOBBY),
            label(r"political-risk analysts: \ for investors, \ the odds of expropriation, \ unrest, \ a change "
                  r"of rules", font_size=21, color=LOSS),
            label(r"campaigns and governments: \ the persuasion rates of chapter twelve, \ every election",
                  font_size=21,
                  color=VOTER),
            label(r"economists in all four: \ measuring what is hidden, \ and designing institutions", font_size=21,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN * 0.2)
        head = label(r"the people who use this", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.PRACTICE_47.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Who uses political economy? <bookmark mark='a'/> Governance teams at development banks and finance "
            "ministries, who design audits, procurement rules and published budgets, the tools of chapters seven "
            "and eight. <bookmark mark='b'/> Those who design regulators, trying to make them hard to capture. "
            "<bookmark mark='c'/> Political-risk analysts, who price for investors the chance that a government "
            "expropriates, that unrest breaks out, or that the rules change. <bookmark mark='d'/> Campaigns and "
            "governments, who measure persuasion at every election. <bookmark mark='e'/> And economists in each of "
            "these places, measuring what is hidden, and designing institutions that do not depend on everyone "
            "being honest."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0], shift=RIGHT * 0.1))
            vo.wait_until("a")
            self.play(Indicate(rows[0], color=WHITE, scale_factor=1.03))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def design(self):
        cards = point_cards([
            (r"publish", r"what was paid, \\ to whom: \ Uganda's \\ newspapers", AUDIT),
            (r"audit at random", r"so that everyone \\ expects it: \\ Olken, \ Brazil", AUDIT),
            (r"cooling-off", r"limits on moving \\ from regulator \\ to industry", LOBBY),
            (r"rules over \\ discretion", r"where discretion \\ is what gets \\ bought", ELITE),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.2)
        head = label(r"designing against capture and theft", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.PRACTICE_47.tag, corner=DR, font_size=11)
        with self.voiceover(
            "The lessons of this part turn into design rules. <bookmark mark='a'/> Publish what was paid and to "
            "whom, as Uganda did. <bookmark mark='b'/> Audit at random, so that everyone expects to be checked, as "
            "in Indonesia's roads and Brazil's towns. <bookmark mark='c'/> Slow the revolving door between "
            "regulators and the industries they oversee. <bookmark mark='d'/> And prefer rules to discretion where "
            "discretion is exactly what would be bought, at the cost of flexibility when circumstances change."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(Circumscribe(cards.cards[0], color=WHITE, buff=0.05))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["treasury_2016"]
        T = tables.PRACTICE_47.data
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.6,
                       font_size=18)
        cc.move_to(UP * 1.45)
        ax = plane([0, 2], [-5, 3], center=DOWN * 2.0, x_length=5.2, y_length=2.4, xticks=[], yticks=[-4, -2, 0, 2],
                   yfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0", font_size=12)
        bars = VGroup()
        for i, (nm, v, col) in enumerate(((r"forecast: \ GDP after \\ two years, \ vs remain", -T["gdp"], LOSS),
                                          (r"outcome: \ growth \\ in 2016", T["growth_2016"], GAIN))):
            p0, p1 = ax.ax.c2p(0.5 + i - 0.3, 0), ax.ax.c2p(0.5 + i + 0.3, v)
            r = Rectangle(width=p1[0] - p0[0], height=abs(p1[1] - p0[1]), stroke_width=0, fill_color=col,
                          fill_opacity=0.85).move_to((p0 + p1) / 2)
            bars.add(VGroup(r, label(nm, font_size=12, color=WHITE).next_to(ax.ax.c2p(0.5 + i, -5), DOWN, buff=0.08),
                            label(rf"{v:+.1f}\%".replace("-", "{-}"), font_size=14, color=WHITE).next_to(
                                r, UP if v > 0 else DOWN, buff=0.04)))
        cap = label(r"not the same quantity: \\ a level against a \\ counterfactual, \ and \\ a growth rate",
                    font_size=13, color=GREY_A).next_to(ax, RIGHT, buff=0.4)
        tag = published_tag(tables.PRACTICE_47.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Called it? Political economy also studies forecasts made in political campaigns. <bookmark mark='a'/> "
            "In May 2016, a month before Britain's referendum on leaving the European Union, the Treasury, run by "
            "a government campaigning to remain, published its analysis of the immediate impact of a vote to "
            "leave. It forecast a year-long recession, with the economy about 3.6 percent smaller after two years "
            "than after a vote to remain, and about half a million more people out of work. <bookmark mark='a2'/> "
            "The two bars are not the same quantity, a level against a counterfactual and a growth rate, but they "
            "point in opposite directions. <bookmark mark='b'/> There was no recession: the economy grew by about "
            "two percent in 2016, and unemployment kept falling. Business investment did fall well short of "
            "earlier forecasts, and the longer-run costs of leaving are a separate argument. <bookmark mark='c'/> "
            "On the recession, the verdict: wrong. A forecast made by one side of a campaign is evidence to weigh, "
            "not a neutral fact."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1][0]), FadeIn(cc.left), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(ax), GrowFromEdge(bars[0][0], UP), FadeIn(bars[0][1:]), FadeIn(bars[1][1]))
            vo.wait_until("a2")
            self.play(FadeIn(cap), Indicate(bars[0][0], color=WHITE))
            vo.wait_until("b")
            self.play(FadeIn(cc.right), GrowFromEdge(bars[1][0], DOWN), FadeIn(bars[1][2]))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3))
        self.clear_scene()
