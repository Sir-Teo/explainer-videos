from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ53.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 14, r"The Dials: \ how deeply people reason", r"Do real people reason like Bayesian players?",
             "Chapter fourteen. The Dials: how deeply people reason.",
             lit={1995: r"Nagel", 2004: r"Camerer, Ho and Chong", 2007: r"DellaVigna and Kaplan"},
             scale=("person",), horizon=("a day",))
        self.dial()
        self.persuasion()

    def dial(self):
        d = dials.DIALS["reasoning_depth"]
        head = status_head(d, r"the depth of strategic reasoning")
        frame, rows = dial_rows(d, -0.2, 5.2, [0, 1, 2, 3, 4, 5], r"average steps of thinking ahead of a naive "
                                                                    r"player", top=1.6, step=0.75, fmt="{:.1f}")
        meaning = wrapped_label(tex_safe(d.meaning), 11.2, 15, GREY_A).to_edge(DOWN, buff=0.35)
        tag = published_tag(r"explainer.economics.dials, \ checked 2026-11-19", corner=UR, font_size=12)
        with self.voiceover(
            "Every equilibrium in this part assumed that people reason all the way through: I think about what you "
            "think about what I think, without end. The Dial from Part eleven measures how far real people go. "
            "<bookmark mark='a'/> Across nearly a hundred games, Colin Camerer, Teck-Hua Ho and Juin-Kuan Chong "
            "estimated one and a half steps on average. <bookmark mark='b'/> Rosemarie Nagel's students, guessing "
            "two thirds of the average, about one step. <bookmark mark='c'/> Newspaper readers with time to think, "
            "about four. <bookmark mark='d'/> The status: it depends on the setting. Common knowledge, cascades "
            "and global games all rest on long chains of reasoning; people manage a few links. Theory that matters "
            "in practice is theory that survives that."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Indicate(rows[0], color=WHITE, scale_factor=1.02))
            for mk, r in zip("bc", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r), run_time=0.6)
            vo.wait_until("d")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()

    def persuasion(self):
        rows = VGroup(
            label(r"how persuasive is persuasion, \ in the field?", font_size=26, color=E.ACCENT),
            label(r"the persuasion rate: \ of those who hear a message \\ and did not already agree, \ the share who "
                  r"change their behaviour", font_size=22, color=WHITE),
            label(r"Fox News's arrival in cable markets, \ 1996--2000: \\ 3 to 8\% of viewers who were not already "
                  r"Republican \\ voted Republican \ (11 to 28\% on narrower audience measures)", font_size=21,
                  color=SENDER),
            label(r"far from total, \ far from zero: \ beliefs move, \ but not as much as a designer would like",
                  font_size=22, color=BELIEF),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(UP * 0.2)
        tag = published_tag(r"DellaVigna and Kaplan, \ QJE 122(3) (2007); \ DellaVigna and Gentzkow, \ ARE (2010)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "And how persuasive is persuasion in the field? <bookmark mark='a'/> Stefano DellaVigna and Matthew "
            "Gentzkow measure it by the persuasion rate: of the people who receive a message and did not already "
            "agree with it, the share who change what they do. <bookmark mark='b'/> When Fox News arrived in "
            "American cable markets between 1996 and 2000, Stefano DellaVigna and Ethan Kaplan estimated that "
            "between three and eight percent of viewers who were not already Republican were persuaded to vote "
            "Republican, more on narrower measures of the audience. <bookmark mark='c'/> Far from total, and far "
            "from zero. Beliefs move, but real receivers are not the perfect Bayesians of the theory, and the "
            "evidence on how much they move is still being gathered."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abc", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()
