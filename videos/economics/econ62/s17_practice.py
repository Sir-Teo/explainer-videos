from __future__ import annotations

from videos.economics.econ62.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 15, r"In practice: \ strategy, \ finance, \ people analytics", r"Where does this economics get "
             r"used, \ and by whom?", "Chapter fifteen. In practice: strategy, finance, people analytics.",
             scale=("firm",), horizon=("a year",))
        self.jobs()
        self.cautions()

    def jobs(self):
        cards = point_cards([
            (r"strategy and operations", r"consultants and in-house teams who find chapter four's practices, \ "
             r"benchmark plants and run the turnaround", MGR),
            (r"corporate finance", r"valuing projects and acquisitions, \ choosing debt, \ chapter seven and "
             r"chapter thirteen's work", FIN),
            (r"people analytics", r"hiring, \ pay and promotion measured with the firm's own data, \ and tested "
             r"where possible", WORK),
            (r"boards and investors", r"setting executive pay, \ watching managers, \ private equity's operating "
             r"partners", OWN),
        ], width=12.6, cols=2, font_size=20).move_to(DOWN * 0.2)
        head = label(r"where the economics of the firm is used", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Where is this economics used? <bookmark mark='a'/> In strategy and operations, by consultants and "
            "in-house teams who find and install chapter four's practices. <bookmark mark='b'/> In corporate "
            "finance, valuing projects and acquisitions and choosing how much to borrow. <bookmark mark='c'/> In "
            "people analytics: hiring, pay and promotion measured with the firm's own records, and tested where "
            "possible, as Part sixty-one's platforms test their prices. <bookmark mark='d'/> And by boards and "
            "investors who set executive pay and watch managers."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()

    def cautions(self):
        head = label(r"three cautions from this part", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        rows = VGroup(
            VGroup(label(r"1. \ Correlation is not management's effect", font_size=26, color=MGR),
                   label(r"well-run firms are more productive, \ and more productive firms can afford to be well "
                         r"run: \ chapter four needed an experiment", font_size=19, color=GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.1),
            VGroup(label(r"2. \ People respond to what is measured", font_size=26, color=WORK),
                   label(r"piece rates raise what is counted; \ promotion by sales picks sellers, \ not managers",
                         font_size=19, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
            VGroup(label(r"3. \ Ask what was there before", font_size=26, color=FIN),
                   label(r"buyouts, \ conglomerates and merger returns all need the comparison before the event",
                         font_size=19, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.55).next_to(head, DOWN, buff=0.7)
        with self.voiceover(
            "And three cautions this part teaches. <bookmark mark='a'/> Correlation is not management's effect: "
            "well-run firms are more productive, but more productive firms can also afford to be well run, which "
            "is why chapter four needed an experiment. <bookmark mark='b'/> People respond to what is measured: "
            "piece rates raise what is counted, and promotion by sales picks sellers, not managers. <bookmark "
            "mark='c'/> And ask what was there before: buyouts, conglomerates and merger returns all need a "
            "comparison from before the event."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.15))
        self.clear_scene()
