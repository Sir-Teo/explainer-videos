from __future__ import annotations

from videos.psychology.psych59.common import *  # noqa: F403

CRITERIA = [r"reliable", r"out of sample", r"changes with treatment", r"change comes first", r"in new sites"]
CANDS = [
    (r"model-based control", ["?", "y", "?", "-", "y"]),
    (r"learning rate under volatility", ["?", "?", "-", "-", "?"]),
    (r"mood integrator", ["?", "-", "-", "-", "-"]),
    (r"connectivity biotypes", ["n", "n", "?", "-", "n"]),
]
MARK = {"y": (r"yes", GOOD), "n": (r"no", AUTH), "?": (r"mixed", PERSON), "-": (r"untested", GREY_B)}


class Targets(VoiceoverScene):
    def construct(self):
        card_section(self, 12, r"What would count as a computational target", r"When is a parameter ready for the "
                     r"clinic?", marr=("how",))
        self.criteria()
        self.scorecard()

    def criteria(self):
        chips_section(self, r"Five tests for a parameter", [
            (r"reliable", r"retest reliability high enough to place a person, \ about 0.8 or more", MODEL),
            (r"out of sample", r"its link to symptoms holds in a new sample, \ not just the one it was found in", PERSON),
            (r"changes with treatment", r"effective treatments move it", GOOD),
            (r"change comes first", r"the parameter changes before the symptoms do, \ and mediates the effect", SYMP),
            (r"in new sites", r"the same results in other clinics, \ countries and devices", AUTH),
        ], "When is a parameter ready for the clinic? Here are five tests. <bookmark mark='a'/> It's reliable: retest "
           "reliability high enough to place a person, about zero point eight or more. <bookmark mark='b'/> Its link "
           "to symptoms holds out of sample, in a new sample, not just the one it was found in. <bookmark mark='c'/> "
           "Effective treatments move it. <bookmark mark='d'/> Its change comes first: the parameter changes before "
           "the symptoms do, and carries the effect. <bookmark mark='e'/> And the same results hold in new sites: "
           "other clinics, countries and devices.")

    def scorecard(self):
        head = heading(r"Four candidates, \ scored")
        cw, rw = 1.95, 3.6
        top = VGroup(*[wrapped_label(c, cw - 0.1, 16, GREY_A) for c in CRITERIA])
        for j, t in enumerate(top):
            t.move_to([-6.6 + rw + cw * (j + 0.5), 2.0, 0])
        rows = []
        for i, (name, marks) in enumerate(CANDS):
            y = 1.0 - 1.0 * i
            nm = wrapped_label(name, rw - 0.2, 19, WHITE).move_to([-6.6 + rw / 2, y, 0])
            cells = VGroup(*[label(MARK[m][0], font_size=19, color=MARK[m][1]).move_to(
                [-6.6 + rw + cw * (j + 0.5), y, 0]) for j, m in enumerate(marks)])
            rows.append(VGroup(nm, cells))
        foot = wrapped_label(r"no parameter passes all five yet: \ the honest state of a young field", 12.0, 21,
                             YOU).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Here are four candidates from this part, scored against the five tests, as the published record stands. "
            "<bookmark mark='a'/> Model-based control: its link to compulsivity has replicated out of sample and "
            "across sites; its reliability is mixed, better with hierarchical models. Whether treatment moves it is mixed, and "
            "whether its change comes first is untested. <bookmark mark='b'/> The learning rate under volatility: "
            "reliability and replication are mixed, and the rest untested. <bookmark mark='c'/> The mood integrator: "
            "promising, mostly untested. <bookmark mark='d'/> And connectivity biotypes failed the stability and "
            "replication tests. <bookmark mark='e'/> No parameter passes all five yet. That's the honest state of a "
            "young field."
        ) as vo:
            self.play(FadeIn(head), FadeIn(top))
            for m, r_ in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r_[0]), LaggedStart(*[FadeIn(c, scale=1.2) for c in r_[1]], lag_ratio=0.2))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()
