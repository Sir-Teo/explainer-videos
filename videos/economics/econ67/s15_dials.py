from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ67.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 13, r"The Dials: \ how often results replicate", r"What share of published findings hold up "
             r"when the study is run again?", "Chapter thirteen. The Dials: how often results replicate.",
             scale=("world",), horizon=("a decade",))
        self.replication()
        self.ledger()

    def replication(self):
        dial = dials.DIALS["replication_rate"]
        head = status_head(dial, r"how often results replicate \ (new)")
        frame, rows = dial_rows(dial, 0, 1.0, [0, 0.25, 0.5, 0.75, 1.0], r"share of significant results "
                                r"significant again, \ same direction", top=1.9, step=0.85, fmt="{:.2f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 11.6, 17, GREY_A).to_edge(DOWN, buff=0.4)
        tag = published_tag(r"the dial's record: \ explainer/economics/dials.py", corner=UR, font_size=12)
        e = dial.estimates
        with self.voiceover(
            "One new Dial: how often published results replicate. <bookmark mark='a'/> Laboratory economics, the "
            f"eighteen studies of chapter two: {e[0].value:.2f}, with a wide interval because eighteen is few. "
            f"<bookmark mark='b'/> Social-science experiments in Nature and Science: {e[1].value:.2f}. <bookmark "
            f"mark='c'/> Psychology, in the Open Science Collaboration's hundred studies of 2015: {e[2].value:.2f}. "
            f"<bookmark mark='d'/> And this film's simulated field: {e[3].value:.2f}. <bookmark mark='e'/> The "
            "status: depends on the setting. The rate is not a constant of nature; it is set by a field's power, "
            "its filter on significance and the freedom of its analyses, all of which can be changed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
            vo.wait_until("e")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.wait(0.5)
        self.clear_scene()

    def ledger(self):
        A = load("audit")
        most = A["most_visited"][:4]
        rows = VGroup(*[label(rf"{tex_safe(m['name'])}: \ Parts {', '.join(str(p) for p in m['parts'])}",
                              font_size=20, color=GREY_A) for m in most]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"the Dials most often reopened", font_size=26, color=E.ACCENT)
        foot = label(r"each reopening adds estimates; \ none so far has closed a Dial", font_size=20, color=PUB)
        VGroup(head, rows, foot).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(UP * 0.2)
        tag = published_tag(r"the Dials' records: \ explainer/economics/dials.py", corner=DL, font_size=12)
        with self.voiceover(
            "And the ledger as a whole. <bookmark mark='a'/> Some Dials were opened once and left. Others kept coming "
            "back, as new parts met the same number from another side. <bookmark mark='b'/> The most often reopened: "
            f"the {most[0]['name']}, the {most[1]['name']}, and {most[2]['name']}, each in {len(most[0]['parts'])} "
            "parts. <bookmark mark='c'/> Each reopening added estimates. None has closed a Dial: the range narrows, "
            "or the setting is named, but the record stays open. That is what a cumulative science looks like from "
            "the inside."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in rows], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
