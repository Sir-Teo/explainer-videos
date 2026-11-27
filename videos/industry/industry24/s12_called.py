from __future__ import annotations

from videos.industry.industry24.common import *  # noqa: F403


class Called(VoiceoverScene):
    def construct(self):
        card(self, 10, "Called it?", "Will the railway's first stretch open when its plan says?",
             "Chapter ten. Called it? A project's own forecast against the record of projects like it.", lit=("change",))
        self.theirs()
        self.slip()
        self.ours()

    def theirs(self):
        M = R["mega"]
        rows = VGroup(tx(f"November 2008: Los Angeles and Anaheim to San Francisco, about ${M['hsr08']}bn (2008 dollars)", 18, GOOD),
                      tx(f"2026 plan: Merced to Bakersfield, ${M['mb']}bn, finished {M['mb_done']}; first full year of service 2033", 18, PRICE),
                      tx(f"2026 plan: Phase 1 to Los Angeles, ${M['phase1']}bn, finished {M['p1_done']}, full service {M['p1_done'] + 1}", 18, BAD)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 0.6, 0])
        note = tx("the 2026 plan moved the first stretch's completion back a year", 17, GREY_A).move_to([0, -1.6, 0])
        src = source("California High-Speed Rail Authority, Business Plans of November 2008 and 2026", size=12)
        beat(self,
             "The railway's own forecasts. <bookmark mark='a'/> In 2008, a line from Los Angeles and Anaheim to San "
             f"Francisco for about {M['hsr08']} billion dollars. <bookmark mark='b'/> In 2026, the first stretch, Merced to "
             f"Bakersfield, for {M['mb']} billion, finished in {M['mb_done']}, with 2033 as its first full year of service. "
             f"<bookmark mark='c'/> And the first phase to Los Angeles by {M['p1_done']}. <bookmark mark='d'/> The 2026 "
             "plan itself moved the first stretch back a year, 'for optimization and pending policy changes', and says "
             "its schedule depends on reforms still to be approved.",
             base=[src], steps=[rows[0], rows[1], rows[2], note])

    def slip(self):
        M = R["mega"]
        dots = VGroup(*[Circle(radius=0.3, stroke_width=0, fill_color=BAD if i < 9 else GOOD, fill_opacity=0.9) for i in range(10)]
                      ).arrange(RIGHT, buff=0.22).move_to([0, 1.2, 0])
        l1 = tx("nine in ten large projects over budget (Flyvbjerg)", 18, BAD, bold=True).next_to(dots, DOWN, buff=0.25)
        l2 = tx(f"rail projects: {M['rail']}% over on average", 18, PRICE, bold=True).move_to([0, -0.9, 0])
        l3 = tx("this project: a year added to the first stretch in 2026 alone; its trains still being bought", 17, GREY_A).move_to([0, -1.8, 0])
        src = source("Flyvbjerg (2014); California High-Speed Rail Authority, 2026 Business Plan", size=12)
        beat(self,
             "What does the reference class say? <bookmark mark='a'/> Nine in ten large projects run over budget, and by "
             "Flyvbjerg's evidence only about one in ten is on schedule. <bookmark mark='b'/> Rail projects have run "
             f"{M['rail']} per cent over on average. <bookmark mark='c'/> And this project's own record: the first stretch "
             "moved back a year in the latest plan, and its trains were still being procured when the plan was written.",
             base=[src], steps=[[dots, l1], l2, l3])

    def ours(self):
        C = R["called"]
        claim = VGroup(tx("Our call, 27 November 2026", 20, PRICE, bold=True),
                       tx("California's high-speed trains will not carry fare-paying passengers between Merced and", 21, WHITE, bold=True),
                       tx(f"Bakersfield before 1 January {C['call_year']}.", 21, WHITE, bold=True),
                       tx(f"Probability: {100 * C['prob']:.0f}%", 22, PRICE, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([0, 1.7, 0])
        why = bullets(["for: about one large project in ten is on schedule; this one has slipped before; track, power and trains still to come",
                       f"against: {get('hsr26.cvs.done'):.0f} of the {get('hsr26.cvs'):.0f} Central Valley miles are built and ready for rail",
                       "the plan: completion 2032, first full year of service 2033"], size=17).move_to([0, -0.5, 0])
        rule = tx("scored on the Authority's own reports at the end of 2033", 15, GREY_B).to_edge(DOWN, buff=0.7)
        tag = estimate_tag("this series' call, logged in explainer/industry/calls.py", size=12)
        beat(self,
             "Now ours. <bookmark mark='a'/> We say California's high-speed trains will not carry fare-paying passengers "
             f"between Merced and Bakersfield before the first of January {C['call_year']}: at least a year behind the "
             f"plan's first full year of service. We give it {100 * C['prob']:.0f} per cent. <bookmark mark='b'/> For: the "
             "reference class, a project that has slipped before, and the track, the electrification and the trains all "
             f"still to come: a contract of up to {get('hsr26.track'):.1f} billion dollars for the track and power was only "
             f"put out to bid in November 2025. Against: {get('hsr26.cvs.done'):.0f} of the {get('hsr26.cvs'):.0f} miles "
             "of the Central Valley's guideway are built and ready for rail. <bookmark mark='c'/> The Authority's "
             "own reports will settle it, and the call stays in the log either way.",
             base=[tag], steps=[claim, why, rule])
