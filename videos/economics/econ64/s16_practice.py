from __future__ import annotations

from videos.economics.econ64.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 14, r"In practice: \ credit, \ targeting, \ public services", r"Where are these methods used, "
             r"\ and what goes wrong?", "Chapter fourteen. In practice: credit, targeting, public services.",
             scale=("person", "nation"), horizon=("a year",))
        self.jobs()
        self.cautions()

    def jobs(self):
        cards = point_cards([
            (r"credit", r"lenders score borrowers with machine learning; \ better prediction moves who gets credit "
             r"and at what price, \ not always in the same direction for every group \ (Fuster et al., \ 2022)",
             ALGO),
            (r"targeting", r"proxy means tests for cash transfers, \ outreach for programmes: \ the effect, \ not "
             r"the risk, \ is what to rank by", CAUSE),
            (r"public services", r"inspections, \ tax audits, \ child-welfare screening: \ prediction policy "
             r"problems, \ with selective labels everywhere", JUDGE),
            (r"the platforms", r"Part 61's ranking, \ pricing and experiments: \ the largest users of all", NET),
        ], width=12.6, cols=2, font_size=20).move_to(DOWN * 0.2)
        head = label(r"where machine learning meets policy", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Fuster, \ Goldsmith-Pinkham, \ Ramadorai and Walther, \ Journal of Finance 77(1) "
                            r"(2022)", corner=DL, font_size=12)
        with self.voiceover(
            "Where is this used? <bookmark mark='a'/> In credit: lenders score borrowers with machine learning. "
            "Andreas Fuster and coauthors showed that better prediction changes who gets a mortgage and at what "
            "price, and not in the same direction for every group. <bookmark mark='b'/> In targeting: proxy means "
            "tests that decide who receives a cash transfer, and outreach for programmes, where chapter four's "
            "lesson applies: rank by effect, not by risk. <bookmark mark='c'/> In public services: inspections, "
            "tax audits, screening of calls to child-welfare agencies, all prediction policy problems, all with "
            "selective labels. <bookmark mark='d'/> And on the platforms of Part sixty-one, the largest users of "
            "all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()

    def cautions(self):
        head = label(r"three cautions from this part", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        rows = VGroup(
            VGroup(label(r"1. \ Ask what the decision hides", font_size=26, color=JUDGE),
                   label(r"outcomes exist only where the decision allowed them: \ evaluate with a design, \ not by "
                         r"filling in", font_size=19, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
            VGroup(label(r"2. \ Ask what is being predicted", font_size=26, color=NAIVE),
                   label(r"costs are not needs, \ risk is not benefit: \ the label is a policy choice",
                         font_size=19, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
            VGroup(label(r"3. \ A prediction is a measurement", font_size=26, color=CAUSE),
                   label(r"it carries error into whatever is built on it: \ correct, \ validate, \ and report",
                         font_size=19, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.55).next_to(head, DOWN, buff=0.7)
        with self.voiceover(
            "And three cautions this part teaches. <bookmark mark='a'/> Ask what the decision hides: outcomes exist "
            "only where the decision allowed them, so evaluate with a design, not by filling in. <bookmark "
            "mark='b'/> Ask what is being predicted: costs are not needs, and risk is not benefit; choosing the "
            "label is a policy choice. <bookmark mark='c'/> And a prediction is a measurement: it carries its error "
            "into whatever is built on it, so correct for it, validate it, and report how it was made."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.15))
        self.clear_scene()
