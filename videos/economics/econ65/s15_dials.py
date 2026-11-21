from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ65.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 13, r"The Dials: \ AI on tasks, \ AI in aggregate", r"How large is the effect of AI on a task, "
             r"\ and on the growth of the whole economy?", "Chapter thirteen. The Dials: AI on tasks, AI in "
             "aggregate.", scale=("person", "nation"), horizon=("a day", "a decade"))
        self.task()
        self.aggregate()

    def task(self):
        dial = dials.DIALS["genai_task_effect"]
        head = status_head(dial, r"generative AI on a task \ (new)")
        frame, rows = dial_rows(dial, -25, 65, [-20, 0, 20, 40, 60], r"percent gain in the measured outcome, \ as "
                                r"reported", top=2.3, step=0.72, fmt="{:.1f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 11.6, 16, GREY_A).to_edge(DOWN, buff=0.35)
        tag = published_tag(r"the dial's record: \ explainer/economics/dials.py", corner=DR, font_size=12)
        e = dial.estimates
        with self.voiceover(
            "This part opens two Dials. The first: the effect of generative AI on a task, measured as the studies "
            "report it, in time saved or output per hour. <bookmark mark='a'/> Writing: forty percent less time. "
            f"<bookmark mark='b'/> A small coding job: {e[1].value:.0f} percent less, with a wide interval. "
            "<bookmark mark='c'/> Consulting tasks inside the frontier: a quarter faster. <bookmark mark='d'/> "
            "Customer support: fourteen percent more resolutions per hour. <bookmark mark='e'/> Experienced "
            "developers in their own code, in early 2025: nineteen percent slower. <bookmark mark='f'/> And the "
            f"Island's desk, where the truth is planted: {e[5].value:.0f} percent. <bookmark mark='g'/> The "
            "status: depends on the setting. The gains are large on short, well-defined tasks and for the least "
            "experienced, and can turn negative where the work is long, familiar and complicated."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            for k, mk in enumerate("abcdef"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k]))
            vo.wait_until("g")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.wait(0.5)
        self.clear_scene()

    def aggregate(self):
        dial = dials.DIALS["ai_productivity_decade"]
        head = status_head(dial, r"AI's addition to productivity growth \ (new)")
        frame, rows = dial_rows(dial, 0, 1.6, [0, 0.5, 1.0, 1.5], r"percentage points a year, \ over about ten "
                                r"years", top=1.9, step=0.9, fmt="{:.2f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 11.6, 17, GREY_A).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"the dial's record: \ explainer/economics/dials.py", corner=DR, font_size=12)
        e = dial.estimates
        with self.voiceover(
            "The second Dial: AI's addition to productivity growth over the next decade, in percentage points a "
            f"year. <bookmark mark='a'/> Acemoglu's arithmetic: {e[0].value:.2f}, less with hard tasks. <bookmark "
            f"mark='b'/> Aghion and Bunel, with the same formula and a broader reading of the experiments: a median "
            f"of {e[1].value:.2f}, with a range from almost nothing to over a point. <bookmark mark='c'/> By "
            "analogy with electricity and computers: 0.8 to 1.3. <bookmark mark='d'/> Goldman Sachs, with "
            "widespread adoption: one and a half. <bookmark mark='e'/> The status: contested. The estimates differ "
            "by a factor of twenty, mostly because they assume different adoption, and none includes AI's effect "
            "on the rate of invention, which could dwarf them all, or come to nothing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k]))
            vo.wait_until("e")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.wait(0.5)
        self.clear_scene()
