from __future__ import annotations

from videos.psychology.psych41.common import *  # noqa: F403


class Across(VoiceoverScene):
    def construct(self):
        self.card()
        self.table()

    def card(self):
        card = chapter_card(12, r"Across the diagnoses", r"Do the same few dials turn up everywhere?", lit=(),
                            part=PART, scale=("circuit", "person"), marr=("what", "how"))
        with self.voiceover("Chapter twelve. Across the diagnoses."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def table(self):
        head = heading(r"Three dials, \ many diagnoses")
        params = [(r"precision of priors", SYMP), (r"prediction errors and learning", MODEL),
                  (r"discounting the future", PERSON)]
        conds = [r"psychosis", r"autism", r"addiction", r"depression", r"ADHD", r"anxiety"]
        marks = {(0, 0): r"weaker and stronger", (0, 1): r"weaker", (0, 5): r"threat expected",
                 (1, 0): r"aberrant salience", (1, 2): r"a surge never learned away", (1, 3): r"blunted",
                 (2, 2): r"steeper", (2, 4): r"steeper", (2, 3): r"steeper"}
        cell_w, cell_h = 1.75, 0.95
        grid = VGroup()
        for j, cnd in enumerate(conds):
            grid.add(label(cnd, font_size=17, color=GREY_A).move_to([-2.6 + j * cell_w, 2.0, 0]))
        cells = VGroup()
        for i, (p, c) in enumerate(params):
            y = 1.1 - i * cell_h
            grid.add(label(p, font_size=17, color=c).move_to([-5.3, y, 0]))
            for j in range(len(conds)):
                box = Rectangle(width=cell_w - 0.1, height=cell_h - 0.12, stroke_color=GREY_D, stroke_width=1)
                box.move_to([-2.6 + j * cell_w, y, 0])
                grid.add(box)
                if (i, j) in marks:
                    cells.add(VGroup(box.copy().set_fill(c, 0.25).set_stroke(c, 1.5),
                                     wrapped_label(marks[(i, j)], cell_w - 0.25, 13, WHITE).move_to(box)))
        rows = rows_of([
            (r"the same few parameters of the series' models recur across diagnoses that the manuals keep apart", WHITE),
            (r"this is the transdiagnostic view, \ and the research programme of RDoC (Part 39): \ study the dials, "
             r"\ not only the labels", MODEL),
            (r"it is a map of hypotheses, \ not of findings: \ several cells are contested, \ and Part 59 asks whether "
             r"the dials can be measured in one person", YOU),
        ], 12.4, 20, 0.3).move_to([0, -2.55, 0])
        with self.voiceover(
            "Step back from the diagnoses. <bookmark mark='a'/> Three dials from the series' own models keep turning "
            "up. The precision of priors: weaker in autism, both weaker and stronger in psychosis, and tilted toward "
            "threat in anxiety. Prediction errors and learning: aberrant salience in psychosis, a surge never learned "
            "away in addiction, blunted in depression. And discounting the future: steeper in addiction, in ADHD, "
            "and in depression. <bookmark mark='b'/> The same few parameters recur across diagnoses that the manuals "
            "keep apart. That's the transdiagnostic view, and the research programme of Part 39's RDoC: study the "
            "dials, not only the labels. <bookmark mark='c'/> It's a map of hypotheses, not of findings. Several cells "
            "are contested, and Part 59 asks whether the dials can be measured in one person."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.5), run_time=14.0)
            for m, r in zip("abc", rows):
                if m != "a":
                    vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
