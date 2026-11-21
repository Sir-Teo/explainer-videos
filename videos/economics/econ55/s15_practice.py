from __future__ import annotations

from videos.economics.econ55.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 13, r"In practice: \ research departments", r"Where is this done every day?",
             "Chapter thirteen. In practice: research departments.", lit={1996: r"FRB/US"}, scale=("nation",),
             horizon=("a year",))
        self.places()

    def places(self):
        rows = VGroup(
            label(r"large estimated models, \ like the Federal Reserve Board's FRB/US, \ for forecasts and "
                  r"scenarios", font_size=22, color=MODEL),
            label(r"estimated DSGE models alongside them; \ the New York Fed publishes its model's forecasts",
                  font_size=22, color=EST),
            label(r"monetary surprises measured around every announcement, \ and narrative series kept up to "
                  r"date", font_size=22, color=GAIN),
            label(r"vector autoregressions and local projections for every new question: \ what did the last "
                  r"hike do?", font_size=22, color=DATA),
            label(r"and the same arguments as this part, \ inside every policy meeting's briefing", font_size=22,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(DOWN * 0.1)
        if rows.width > 13.2:
            rows.width = 13.2
        head = label(r"inside a central bank's research department", font_size=28, color=E.ACCENT).to_edge(
            UP, buff=0.6)
        with self.voiceover(
            "Where is this done every day? In the research departments of central banks. <bookmark mark='a'/> "
            "They keep large estimated models, like the Federal Reserve Board's FRB/US, for forecasts and for "
            "asking what would happen under other policies. <bookmark mark='b'/> Most keep estimated DSGE models "
            "alongside them, and the New York Fed publishes its model's forecasts. <bookmark mark='c'/> They "
            "measure the market's surprise around every announcement, and keep narrative series of their own "
            "decisions up to date. <bookmark mark='d'/> They run autoregressions and projections for every new "
            "question, the first being always: what did the last hike do? <bookmark mark='e'/> And the arguments of "
            "this part, about which assumption to trust, happen inside every policy meeting's briefing, usually "
            "with three answers on the table."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()
