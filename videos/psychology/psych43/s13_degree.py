from __future__ import annotations

from videos.psychology.psych43.common import *  # noqa: F403


class Degree(VoiceoverScene):
    def construct(self):
        self.card()
        self.ledger_so_far()
        self.map_so_far()

    def card(self):
        card = chapter_card(12, r"The degree", r"What has been built, \ and what comes next?", lit=(), part=PART,
                            scale=("molecule", "person", "society"), marr=("what", "how"))
        with self.voiceover("Chapter twelve. The degree."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def ledger_so_far(self):
        counts = ledger.counts(upto=PART)
        order = ["replicated", "replicated, smaller", "story and record", "contested", "not directly tested", "failed",
                 "retracted"]
        total = sum(counts.values())
        head = heading(r"The Ledger so far")
        A = axes([0.3, len(order) + 0.7], [0, max(counts.values()) * 1.15], x_length=7.4, y_length=3.4, xticks=None,
                 yticks=None, ylabel=r"rows", center=[-2.4, 0.6, 0], font_size=13)
        b = bars(A.ax, list(range(1, len(order) + 1)), [counts[s] for s in order], [STATUS_COLOR[s] for s in order],
                 width=0.6)
        nums = VGroup(*[label(str(counts[s]), font_size=16, color=STATUS_COLOR[s]).next_to(b[i], UP, buff=0.08)
                        for i, s in enumerate(order)])
        names = VGroup(*[wrapped_label(s, 1.0, 11, STATUS_COLOR[s]).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.15)
                         for i, s in enumerate(order)])
        held = counts["replicated"] + counts["replicated, smaller"] + counts["story and record"]
        fell = counts["failed"] + counts["retracted"]
        rows = rows_of([
            (rf"{total} findings, \ each with its original, \ its record and its sources", WHITE),
            (rf"{held} hold, \ some smaller or misremembered; \ {counts['contested']} are argued; \ {fell} failed or "
             rf"were withdrawn", PERSON),
            (r"the failures cluster where Part 4 predicted: \ small samples, \ flexible analyses, \ surprising claims", YOU),
        ], 4.0, 18, 0.36).move_to([4.9, 0.3, 0])
        total_s, held_s, fell_s, cont_s = str(total), str(held), str(fell), str(counts["contested"])
        with self.voiceover(
            f"Look back at the degree. <bookmark mark='a'/> The Ledger now holds {total_s} findings, each with its "
            f"original study, its record and its sources. <bookmark mark='b'/> {held_s} hold, some smaller than first "
            f"reported, or misremembered in the textbooks. {cont_s} are argued. {fell_s} failed, or were withdrawn. "
            f"<bookmark mark='c'/> The failures cluster where Part 4 predicted: small samples, flexible analyses, and "
            f"surprising claims."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in b], lag_ratio=0.2),
                      FadeIn(nums), run_time=2.0)
            for m, r in zip("bc", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def map_so_far(self):
        hm = homunculus_map(done=PART, height=6.0).move_to([-3.8, 0.0, 0])
        rows = rows_of([
            (r"Acts I to X: \ the undergraduate degree, \ from Kant's wager to the evidence for therapy", WHITE),
            (r"Act XI, \ the graduate toolkit: \ latent variables, \ item response theory, \ scaling, \ people over "
             r"time, \ models of behaviour and of the brain's data, \ and the weight of evidence", MODEL),
            (r"Act XII, \ psychology at work: \ human factors, \ design, \ organizations, \ learning, \ behaviour "
             r"change, \ law, \ health", PERSON),
            (r"Act XIII, \ the frontier: \ the predictive brain, \ computational psychiatry, \ minds and machines, \ "
             r"and a dissertation", GOOD),
        ], 6.0, 19, 0.4).move_to([3.4, -0.1, 0])
        with self.voiceover(
            "And the map. <bookmark mark='a'/> Acts One to Ten were the undergraduate degree, from Kant's wager to the "
            "evidence for therapy. <bookmark mark='b'/> Act Eleven is the graduate toolkit: latent variables, item "
            "response theory, scaling, people over time, models of behaviour and of the brain's data, and the weight "
            "of evidence. <bookmark mark='c'/> Act Twelve is psychology at work: human factors, design, organizations, "
            "learning, behaviour change, law and health. <bookmark mark='d'/> And Act Thirteen is the frontier: the "
            "predictive brain, computational psychiatry, minds and machines, and a dissertation."
        ) as vo:
            self.play(FadeIn(hm))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
