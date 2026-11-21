from __future__ import annotations

from videos.economics.econ55.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 13, r"In practice: \ research departments", r"Where is this done every day?",
             "Chapter thirteen. In practice: research departments.", lit={1996: r"FRB/US"}, scale=("nation",),
             horizon=("a year",))
        self.places()

    def places(self):
        chain = flow_chain([(r"large estimated models", MODEL), (r"estimated DSGE models", EST),
                            (r"surprises and narratives", GAIN), (r"VARs and projections", DATA),
                            (r"the briefing", E.ACCENT)], direction=DOWN, box_w=3.3, box_h=0.8, buff=0.32,
                           font_size=21,
                           notes=[r"FRB/US at the Federal Reserve Board: \ forecasts, \ and what other policies "
                                  r"would do",
                                  r"alongside them; \ the New York Fed publishes its model's forecasts",
                                  r"the market's surprise around every announcement; \ narrative series of the "
                                  r"bank's own decisions",
                                  r"for every new question, \ first of all: \ what did the last hike do?",
                                  r"this part's arguments about which assumption to trust: \ usually three answers "
                                  r"on the table"], note_size=18)
        chain.move_to(DOWN * 0.35)
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
            for k, mk in enumerate("abcde"):
                vo.wait_until(mk)
                anims = [FadeIn(chain.boxes[k], shift=DOWN * 0.1), FadeIn(chain.notes[k], shift=RIGHT * 0.1)]
                if k:
                    anims.append(GrowArrow(chain.arrows[k - 1]))
                self.play(*anims)
        self.clear_scene()
