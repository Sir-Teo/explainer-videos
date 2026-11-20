from __future__ import annotations

from videos.economics.econ42.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 16, r"Frontier: \ platform work, \ long-term care, \ automation", r"What is still being worked out?",
             "Chapter sixteen. Frontier: platform work, long-term care, automation.",
             lit={2020: r"pandemic unemployment assistance"}, scale=("person", "nation"), horizon=("a decade",))
        self.open()

    def open(self):
        cards = point_cards([
            (r"platform work", r"drivers and couriers \\ counted as contractors \\ fall outside \\ unemployment "
                               r"insurance: \\ what should cover them?", UNEMP),
            (r"long-term care", r"years of care in old \\ age: \ few buy private \\ cover, \ and the state \\ pays "
                                r"for much of it", HEALTH),
            (r"automation", r"insurance against a \\ skill losing its value: \\ wage insurance that \\ tops up a "
                            r"lower-paid \\ new job", PENSION),
        ], width=12.6, cols=3, font_size=19).move_to(DOWN * 0.2)
        head = label(r"open questions", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"the frontier, \ stated in words", corner=DR, font_size=11)
        with self.voiceover(
            "Three frontiers. <bookmark mark='a'/> Platform work. Drivers and couriers who work through apps are "
            "usually treated as independent contractors, outside unemployment insurance, which was built for "
            "employees with one employer. In 2020 a temporary pandemic programme covered them, and showed both "
            "that it could be done and how hard it is to verify lost earnings for people with many small jobs. "
            "<bookmark mark='b'/> Long-term care. Many people will need years of help in old age, a large and "
            "uncertain cost, yet few buy private insurance against it, partly because the state already pays for "
            "much of that care once savings run out, which leaves less reason to buy cover of one's own. "
            "<bookmark mark='c'/> Automation. When technology makes a skill less valuable, the loss is lasting, "
            "and unemployment insurance, which pays while one is out of work, does not cover it. Wage insurance, "
            "which tops up a new job's lower pay for a while, is one proposal; how to price and pay for such "
            "insurance is still being worked out."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abc", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
