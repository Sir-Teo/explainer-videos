from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ64.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 13, r"The Dials: \ algorithms against judges", r"How much does ranking cases by a model add to a "
             r"judge's decision?", "Chapter thirteen. The Dials: algorithms against judges.",
             scale=("person", "city"), horizon=("a year",))
        self.gain()

    def gain(self):
        dial = dials.DIALS["algorithm_gain"]
        head = status_head(dial, r"what an algorithm adds to a judge \ (new)")
        frame, rows = dial_rows(dial, 0, 0.4, [0, 0.1, 0.2, 0.3, 0.4], r"proportional fall in the bad outcome, \ "
                                r"same detention rate", top=1.4, step=0.9, fmt="{:.2f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 11.6, 17, GREY_A).to_edge(DOWN, buff=0.5)
        tag = published_tag(r"the dial's record: \ explainer/economics/dials.py", corner=DR, font_size=12)
        e = dial.estimates
        with self.voiceover(
            "This part opens one Dial: how much an algorithm's ranking adds to a judge's decision, measured as the "
            "fall in the outcome the decision is meant to prevent, at the same detention rate. <bookmark mark='a'/> "
            f"Kleinberg and his coauthors in New York City: up to {e[0].value:.2f}, about a quarter. <bookmark "
            f"mark='b'/> The Island, where the truth is known: {e[1].value:.2f}. <bookmark mark='c'/> And the "
            f"Island again, by the contraction design, using only outcomes that were seen: {e[2].lo:.2f} to "
            f"{e[2].hi:.2f}, a little below the truth, because contraction can only detain more of the lenient "
            "judges' released, not release anyone they jailed. <bookmark mark='d'/> The status: depends on the "
            "setting. Where the decision is a prediction and the records carry most of the signal, the gains are "
            "large. Where the judge sees what the records do not, they shrink, and only a design that copes with "
            "selective labels can tell."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k]))
            vo.wait_until("d")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.wait(0.5)
        self.clear_scene()
