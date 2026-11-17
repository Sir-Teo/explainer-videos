from __future__ import annotations

from videos.psychology.psych27.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.scorecard()
        self.next_()

    def card(self):
        card = chapter_card(15, r"Frontier: \ the scorecard", r"Where do the theories stand?",
                            lit={2022: r"Seth \& Bayne", 2025: r"Cogitate Consortium"},
                            part=PART, scale=("mind", "brain"), marr=("what",))
        with self.voiceover("Chapter fifteen. Frontier: the scorecard."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def scorecard(self):
        head = heading(r"The theories, \ scored on this part's evidence")
        cols = [r"", r"workspace", r"integrated information", r"recurrent", r"higher order"]
        colors = [WHITE, GNW, IIT, RPT, HOT]
        data = [
            (r"all-or-none access", [(r"yes", GOOD), (r"silent", GREY_B), (r"partly", GREY_B), (r"silent", GREY_B)]),
            (r"no-report designs", [(r"strained", LOST), (r"fits", GOOD), (r"fits", GOOD), (r"strained", LOST)]),
            (r"adversarial test", [(r"lost some", LOST), (r"lost some", LOST), (r"not tested", GREY_B),
                                   (r"not tested", GREY_B)]),
            (r"blindsight", [(r"fits", GOOD), (r"fits", GOOD), (r"fits", GOOD), (r"fits, \ best", GOOD)]),
            (r"measurable in patients", [(r"P3b", GREY_B), (r"PCI, \ inspired", GOOD), (r"partly", GREY_B),
                                         (r"no", GREY_B)]),
        ]
        widths = [3.0, 2.2, 3.0, 2.0, 2.2]
        table = VGroup()
        hdr = VGroup(*[label(c, font_size=20, color=col) for c, col in zip(cols, colors)])
        table.add(hdr)
        for name, cells in data:
            row = VGroup(label(name, font_size=19, color=WHITE), *[label(t, font_size=19, color=c) for t, c in cells])
            table.add(row)
        xs = np.cumsum([0] + widths[:-1]) - sum(widths) / 2 + np.array(widths) / 2
        for r_i, row in enumerate(table):
            for c_i, cell in enumerate(row):
                cell.move_to([xs[c_i], 2.0 - 0.62 * r_i, 0])
        rule = Line([-sum(widths) / 2, 1.7, 0], [sum(widths) / 2, 1.7, 0], color=GREY_D)
        foot = wrapped_label(r"a judgement, \ not a measurement: \ the cells summarize this part's chapters, \ and "
                             r"each theory's authors would score themselves differently", 12.0, 22, GREY_A).to_edge(
            DOWN, buff=0.7)
        tag = published_tag(r"Seth \& Bayne (2022); \ Cogitate Consortium (2025)")
        with self.voiceover(
            "Here is a scorecard, a judgement rather than a measurement, built from this part's chapters. "
            "<bookmark mark='a'/> All-or-none access, the attentional blink and ignition, favour the workspace. "
            "<bookmark mark='b'/> No-report designs, which strip away frontal activity tied to reporting, favour the "
            "theories that put experience at the back. <bookmark mark='c'/> The adversarial test cost both of the "
            "theories it tested something. <bookmark mark='d'/> Blindsight fits everyone, which is why it can't "
            "decide between them, though higher-order theories fit the wagering best. <bookmark mark='e'/> And for "
            "patients, the most useful measure so far, the complexity index, was inspired by integrated information "
            "but doesn't depend on it being true. Each theory's authors would fill in these cells differently, and "
            "that disagreement is the frontier."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(hdr), Create(rule))
            for m, row in zip("abcde", table[1:]):
                vo.wait_until(m)
                self.play(FadeIn(row, shift=RIGHT * 0.1))
            self.play(FadeIn(foot))
        self.clear_scene()

    def next_(self):
        head = heading(r"What comes next")
        rows = rows_of([
            (r"more adversarial collaborations, \ pitting other pairs of theories against each other, \ with the "
             r"same rules: \ predictions registered before the data", GNW),
            (r"causal tests in people: \ stimulating or silencing prefrontal cortex while experience is measured "
             r"without report", RPT),
            (r"consciousness in infants and animals, \ judged by markers that do not need language", SEEN),
            (r"predictive accounts, \ in which experience is the brain's best guess about the world and the body "
             r"\ (Part 58)", MODEL),
            (r"and the measurement problem underneath it all: \ every one of these tests still has to decide what "
             r"counts as unseen", HOT),
        ], 12.0, 24, 0.4).move_to([0, -0.2, 0])
        with self.voiceover(
            "What comes next? <bookmark mark='a'/> More adversarial collaborations, pitting other pairs of theories "
            "against each other under the same rules, with predictions registered before any data. "
            "<bookmark mark='b'/> Causal tests in people: stimulating or silencing prefrontal cortex while experience "
            "is measured without report. <bookmark mark='c'/> Consciousness in infants and animals, judged by markers "
            "that don't need language. <bookmark mark='d'/> Predictive accounts, in which experience is the brain's "
            "best guess about the world and the body, which return in Part 58. <bookmark mark='e'/> And underneath it "
            "all, the measurement problem from chapter two: every one of these tests still has to decide what counts "
            "as unseen."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
