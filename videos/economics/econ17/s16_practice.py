from __future__ import annotations

from videos.economics.econ17.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 14, r"In practice: \ clearinghouses and platforms", r"Who designs matching markets today, \ and "
             r"what does the work involve?", "Chapter fourteen. In practice: clearinghouses and platforms.",
             lit={1998: r"the doctors' redesign", 2004: r"New England's kidney exchange"},
             scale=("firm", "city", "nation"), horizon=("a year",))
        self.where()
        self.work()

    def where(self):
        rows = point_cards([
            (r"clearinghouses", r"doctors, \ psychologists, \\ dentists, \ pharmacists", STABLE),
            (r"school districts", r"enrolment offices that \\ run a match each year", SCHOOL),
            (r"kidney exchanges", r"national and regional \\ programmes", KIDNEY),
            (r"platforms", r"rides, \ rooms, \ dates, \\ freelance work", MECH),
            (r"resettlement agencies", r"placing refugee \\ families", HELD),
            (r"governments", r"university entrance, \\ public housing", GREY_A),
        ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
        head = label(r"where matching markets are designed", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Matching markets are designed in many places now. <bookmark mark='a'/> Clearinghouses place doctors, "
            "and also clinical psychologists, dentists and pharmacists, among others. School districts run a match "
            "each year. Kidney exchanges run national and regional programmes. Platforms match riders with drivers, "
            "guests with rooms, people with people, and clients with freelancers, usually with prices as well. "
            "Resettlement agencies place refugee families. <bookmark mark='b'/> And governments allocate university "
            "places and public housing."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2), FadeIn(rows.cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in rows.cards[1:5]], lag_ratio=0.8), run_time=10)
            vo.wait_until("b")
            self.play(FadeIn(rows.cards[5], shift=UP * 0.1))
        self.clear_scene()

    def work(self):
        rows = VGroup(
            label(r"learn the market's rules and frictions: \ who wants what, \ who may decide, \ what is forbidden",
                  font_size=22),
            label(r"choose the algorithm: \ stability, \ efficiency, \ safety of the truth; \ who asks",
                  font_size=22, color=STABLE),
            label(r"handle the details theory leaves out: \ couples, \ siblings, \ ties, \ quotas, \ capacities",
                  font_size=22, color=HELD),
            label(r"simulate it on last year's lists before anyone relies on it", font_size=22, color=PROPOSE),
            label(r"explain it to parents, \ doctors and surgeons, \ and persuade them to trust it", font_size=22,
                  color=E.ACCENT),
            label(r"then evaluate: \ the match's lotteries are experiments \ (chapter twelve)", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        tag = published_tag(r"Roth, Econometrica 70(4) (2002), ``The Economist as Engineer''", corner=DR,
                            font_size=13)
        with self.voiceover(
            "Roth called this work the economist as engineer. <bookmark mark='a'/> It starts by learning the "
            "market: who wants what, who has the right to decide, and what is forbidden. <bookmark mark='b'/> Then "
            "choosing the algorithm, weighing stability, efficiency and the safety of telling the truth, and "
            "deciding who asks. <bookmark mark='c'/> Then the details theory leaves out: couples, siblings, ties, "
            "quotas, places that come in pairs. <bookmark mark='d'/> Then simulating the design on last year's "
            "lists before anyone depends on it. <bookmark mark='e'/> Then explaining it to parents, doctors and "
            "surgeons, and persuading them to trust it, which is often the hardest part. "
            "<bookmark mark='f'/> And finally evaluating, using the lotteries the match itself runs."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
