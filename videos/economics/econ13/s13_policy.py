from __future__ import annotations

from videos.economics.econ13.common import *  # noqa: F403


class Policy(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Mandates, \ subsidies \ and risk adjustment", r"What can policy do about adverse selection, "
             r"\ and what does each remedy cost?", "Chapter eleven. Mandates, subsidies and risk adjustment.",
             lit={2010: r"the Affordable Care Act"}, scale=("person", "market", "nation"), horizon=("a year",
                                                                                                   "a decade"))
        self.tools()
        self.evidence()

    def tools(self):
        rows = point_cards([
            (r"a mandate", r"everyone must buy: \\ the healthy stay in", GOOD),
            (r"subsidies", r"a lower price \\ keeps more people in", SIGNAL),
            (r"community rating", r"one price for all: \\ fair, \ but invites selection", POOL),
            (r"guaranteed issue", r"insurers can't refuse: \\ cover for the sick", LEMON),
            (r"risk adjustment", r"insurers paid more \\ for sicker members", USED),
            (r"default plans", r"inertia keeps \\ people enrolled", LOSS),
        ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.2)
        head = label(r"the remedies, \ and what each one costs", font_size=32, color=E.ACCENT).to_edge(UP, buff=0.5)
        foot = label(r"a mandate makes people buy cover worth less to them than it costs; \ a subsidy costs taxes; \ "
                     r"rating rules invite selection", font_size=21, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Policy has a short list of remedies, and each one costs something. <bookmark mark='a'/> A mandate requires "
            "everyone to buy, so the healthy stay in the pool. Subsidies lower the price, which keeps more people in. "
            "Community rating charges everyone the same price, which is fair to the sick but invites the healthy to "
            "leave. Guaranteed issue forbids insurers to refuse anyone. Risk adjustment pays insurers more for sicker "
            "members, so that none of them gains by courting the healthy. And default plans use inertia to keep "
            "people enrolled. <bookmark mark='b'/> The costs: a mandate makes some people buy cover worth less to them "
            "than it costs; a subsidy has to be paid for with taxes; and rating rules, by stopping insurers from "
            "pricing risk, create the selection that the mandate and subsidy then have to fight."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in rows.cards], lag_ratio=0.6), run_time=18)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def evidence(self):
        h = tables.HKK_2015.data
        rows = VGroup(
            label(r"America's Affordable Care Act (2010): \ guaranteed issue, \ community rating, \ subsidies, \ and "
                  r"a mandate", font_size=22),
            label(r"its model was Massachusetts's reform of 2006", font_size=22, color=GREY_A),
            label(rf"Hackmann, \ Kolstad and Kowalski (2015): \ there, \ the mandate's reduction in selection gained "
                  rf"about {100 * h['hkk_gain']:.1f}\% per person, \\ some \${h['hkk_total_musd']:.1f} million a year",
                  font_size=22, color=GOOD),
            label(r"from 2019 the federal mandate's penalty was set to zero, \ and the marketplaces carried on, \ "
                  r"cushioned by subsidies that rise with premiums", font_size=22, color=SIGNAL),
            label(rf"Benjamin Handel (2013): \ helping employees choose better would have worsened selection, \\ "
                  rf"doubling its welfare loss to {100 * h['handel_loss']:.1f}\% of premiums", font_size=22, color=LOSS),
            label(r"in a selection market, \ even good choices by individuals can hurt the pool", font_size=24,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.3).move_to(UP * 0.1)
        tag = published_tag(r"Hackmann, Kolstad and Kowalski, AER 105(3) (2015); \ Handel, AER 103(7) (2013)",
                            corner=DR, font_size=13)
        with self.voiceover(
            "The Affordable Care Act of 2010 used nearly all of these at once. <bookmark mark='a'/> Insurers in its "
            "marketplaces had to accept everyone, and could vary prices only by age, place, family size and smoking; "
            "buyers got subsidies; "
            "and everyone had to have cover or pay a penalty. <bookmark mark='b'/> Its model was Massachusetts's "
            "reform of 2006. <bookmark mark='c'/> Studying Massachusetts, Martin Hackmann, Jonathan Kolstad and Amanda "
            "Kowalski estimated that the mandate's reduction in adverse selection gained about four percent per "
            "person, some fifty-one million dollars a year. <bookmark mark='d'/> From 2019 the federal mandate's "
            "penalty was set to zero, and the marketplaces carried on, cushioned by subsidies that rise with "
            "premiums. "
            "<bookmark mark='e'/> A last twist comes from Benjamin Handel. At a large employer, he estimated that "
            "helping employees overcome their inertia and choose better plans would have worsened selection, "
            "doubling its welfare loss to over eight percent of premiums. <bookmark mark='f'/> In a market with "
            "selection, even better choices by individuals can hurt the pool."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
