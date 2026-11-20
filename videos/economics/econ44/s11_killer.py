from __future__ import annotations

from videos.economics.econ44.common import *  # noqa: F403


class Killer(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Killer acquisitions", r"Why buy a rival's project, only to stop it?",
             "Chapter nine. Killer acquisitions.", lit={2021: r"Cunningham, \ Ederer and Ma"},
             scale=("firm",), horizon=("a decade",))
        self.numbers()
        self.evidence()

    def numbers(self):
        K = load("killer")
        rows = VGroup(
            label(rf"a start-up's new drug would compete with an incumbent's; \ developing it costs {K['cost']:.0f}",
                  font_size=21, color=WHITE),
            label(rf"alone, \ the start-up would earn {K['pi_duo']:.0f}: \ {K['pi_duo']:.0f} $>$ {K['cost']:.0f}, \ "
                  r"it develops the drug", font_size=21, color=PATIENT),
            label(rf"the incumbent earns {K['pi_one']:.0f} now; \ with both drugs, \ {K['pi_two']:.0f}: \ the new "
                  rf"one adds only {K['pi_two'] - K['pi_one']:.0f}", font_size=21, color=FIRM1),
            label(rf"bought by the incumbent: \ {K['pi_two'] - K['pi_one']:.0f} $<$ {K['cost']:.0f}, \ the project "
                  r"is shelved", font_size=21, color=LOSS),
            label(rf"the incumbent would pay up to {K['pay_up_to']:.0f} to keep its monopoly; \ the start-up's "
                  rf"own project is worth {K['entrant_gain']:.0f}", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN * 0.1)
        head = label(r"a killer acquisition, \ in numbers", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(tables.INNOVATION.tag, corner=DR, font_size=11)
        with self.voiceover(
            f"Here is the logic in numbers. <bookmark mark='a'/> A start-up has a promising drug that would compete "
            f"with an incumbent's best seller. Developing it costs {K['cost']:.0f}. <bookmark mark='b'/> On its own, "
            f"the start-up would earn {K['pi_duo']:.0f} in competition, more than the cost, so it would develop the "
            f"drug. <bookmark mark='c'/> The incumbent earns {K['pi_one']:.0f} today. Owning both drugs, it would "
            f"earn {K['pi_two']:.0f}: the new drug mostly steals its own sales, adding only "
            f"{K['pi_two'] - K['pi_one']:.0f}. <bookmark mark='d'/> So if the incumbent buys the start-up, the "
            "project is shelved. <bookmark mark='e'/> And the incumbent will gladly buy: keeping its monopoly is "
            f"worth up to {K['pay_up_to']:.0f} to it, far more than the project is worth to the start-up. Patients "
            "lose a drug that would have been made."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def evidence(self):
        cards = point_cards([
            (r"the data", r"thousands of drug \\ projects, \ before and \\ after acquisitions", BUS),
            (r"the finding", r"projects bought by an \\ incumbent with an \\ overlapping drug are \\ markedly less "
                             r"likely \\ to be developed", LOSS),
            (r"the signs", r"many such deals fall \\ just below the size \\ that must be reported \\ to the "
                           r"agencies", FIRM1),
            (r"for policy", r"review of small deals, \\ and of what the \\ target was working on", GAIN),
        ], width=12.8, cols=4, font_size=17).move_to(DOWN * 0.1)
        head = label(r"Cunningham, \ Ederer and Ma \ (2021)", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.INNOVATION.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Colleen Cunningham, Florian Ederer and Song Ma went looking for this in pharmaceuticals. "
            "<bookmark mark='a'/> They followed thousands of drug projects before and after their developers were "
            "acquired. <bookmark mark='b'/> Projects bought by an incumbent that already sold an overlapping drug "
            "were markedly less likely to be developed further than other acquired projects. "
            "<bookmark mark='c'/> And such deals cluster just below the size at which a merger must be reported to "
            "the American agencies, where they escape review. <bookmark mark='d'/> The policy question that "
            "followed is whether small deals, and what the target was working on, deserve a closer look."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
