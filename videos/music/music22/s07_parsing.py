from __future__ import annotations

import numpy as np

from videos.music.music22.common import *  # noqa: F403


class Parsing(SoundScene):
    def construct(self):
        chapter(self, 6, r"Parsing and ambiguity", r"How many ways can a progression be heard?")
        self.cyk()
        self.count()
        self.missing()

    # ------------------------------------------------------------------
    def cyk(self):
        seq = ["I", "vi", "ii", "V", "I"]
        n = len(seq)
        cell = 1.0
        from explainer.music.monochord import grammar as G
        chart = {}
        grid = VGroup()
        for span in range(1, n + 1):
            for i in range(n - span + 1):
                j = i + span - 1
                regions = {G.FUNCTION[seq[i]]} if span == 1 else {
                    A for A, B, C in G.RULES for split in range(i, j)
                    if B in chart[i, split] and C in chart[split + 1, j]
                }
                chart[i, j] = regions
                sq = Square(side_length=0.82, stroke_color=GREY_B, stroke_width=1.5)
                sq.move_to([(i + (j - i) / 2 - 2) * cell, -1.6 + (j - i) * 0.98, 0])
                content = label(', '.join(sorted(regions)) or '--', font_size=15,
                                color=TUNE if span == n else WHITE).move_to(sq)
                content.scale_to_fit_width(min(content.width, 0.72))
                grid.add(VGroup(sq, content))
        words = VGroup(*[label(tex(w), font_size=26, color=WHITE).move_to([(k - 2) * cell, -2.4, 0]) for k, w in enumerate(seq)])
        grid_g = VGroup(grid, words).move_to(LEFT * 3.0 + DOWN * 0.1)
        rows_ = VGroup(*[label(t, font_size=24, color=c_) for t, c_ in (
            (r"the CYK algorithm \ (1960s): \ fill a triangle of cells", WHITE),
            (r"bottom: \ one chord, \ its strict functional region", WHITE),
            (r"each upper cell: \ regions for the whole span, \\ trying splits into two solved spans", WHITE),
            (r"top: \ the whole progression; \\ probabilities and backpointers give a best tree", TUNE),
            (r"time grows as the cube of the length", GREY_A))]).arrange(DOWN, buff=0.34, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 6.6))
        rows_.move_to(RIGHT * 3.3 + DOWN * 0.1)
        with self.voiceover(
            "How does a program find a tree? With an algorithm from the 1960s named after its three inventors, Cocke, "
            "Younger and Kasami. <bookmark mark='a'/> Fill a triangle of cells. <bookmark mark='b'/> In the bottom row, "
            "each chord, with the regions that could produce it. <bookmark mark='c'/> In each cell above, the regions "
            "that could produce that whole stretch of chords, by splitting it somewhere into two stretches already "
            "solved below. <bookmark mark='d'/> The top cell covers the whole progression. Keep probabilities instead of "
            "yes or no, and the most probable tree can be read back down. <bookmark mark='e'/> The work grows as the "
            "cube of the length, fine for a phrase of a dozen chords."
        ) as vo:
            self.play(FadeIn(grid_g), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def count(self):
        d = load("parses")
        g = d["growth"]
        ns = sorted(g, key=int)
        ch = columns([np.log10(max(1, g[k])) for k in ns], [rf"{k} chords" for k in ns], width=6.0, height=2.6, color=WEAK, hot=(len(ns) - 1,), hot_color=EAR, fmt=None, font_size=20, top=3.5).move_to(LEFT * 2.6 + DOWN * 0.5)
        nums = VGroup(*[label(f"{g[k]:,}".replace(",", "{,}"), font_size=22, color=WHITE).next_to(ch.bars[i], UP, buff=0.1) for i, k in enumerate(ns)])
        t = label(r"trees the grammar allows for I, \ then IV V I repeated \ (log scale)", font_size=21, color=GREY_A).next_to(ch, UP, buff=0.55)
        side = VGroup(label(rf"{d['examples']['I vi ii V I']['parses']} trees for I vi ii V I", font_size=24, color=WHITE),
                      label(r"tree counts grow rapidly under these rules", font_size=22, color=GREY_A),
                      label(r"ambiguity is the normal state: \ probabilities choose", font_size=24, color=TUNE)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * 4.0 + DOWN * 0.3)
        with self.voiceover(
            f"Most progressions have more than one tree. <bookmark mark='a'/> I, vi, ii, V, I has {say(d['examples']['I vi ii V I']['parses'])} under these rules: vi can belong to the opening tonic or begin a new one; ii can group with V or with what came before. <bookmark mark='b'/> Repeat the cadence IV V I and the count explodes: {say(g[ns[1]])} trees for seven chords, {say(g[ns[2]])} for ten, {say(g[ns[3]])} for thirteen, growing like the Catalan numbers that count the ways to bracket a sum. <bookmark mark='c'/> Ambiguity is the normal state of a grammar, in music as in language, and the model’s probabilities rank its trees; this is not a measured account of listeners’ choices."
        ) as vo:
            self.play(FadeIn(ch), FadeIn(nums), FadeIn(t))
            for mark, r in zip("abc", side):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def missing(self):
        d = load("parses")
        ex = d["examples"]["I IV I V I"]
        rows_ = VGroup(*[label(t, font_size=25, color=c_) for t, c_ in (
            (rf"I \ IV \ I \ V \ I: \ {ex['parses']} trees with the six rules", EAR),
            (r"IV going straight back to I, \ the plagal motion of Part 18, \ has no rule", WHITE),
            (r"add one: \ TR $\to$ SR TR, \ and it parses", WHITE),
            (r"a grammar is a theory: \ what it cannot parse, \ it says is ungrammatical", TUNE),
            (r"Bach writes IV--I hundreds of times: \ the theory must grow", GREY_A))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"what the grammar cannot say", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            f"The separate strict function-label counter can assign no trees at all. <bookmark mark='a'/> I, IV, I, V, I has {say(ex['parses'])} under the six rules. <bookmark mark='b'/> The trouble is IV going straight back to I, the plagal move of Part 18: the rules only let a subdominant region lead to a dominant one. <bookmark mark='c'/> Add a rule, a tonic region can be a subdominant region followed by a tonic region, and it parses. <bookmark mark='d'/> That is what it means for a grammar to be a theory: a rejected accepted progression exposes a limitation if the grammar claims to cover that repertoire; a teaching subset need not cover everything. <bookmark mark='e'/> Bach writes IV going to I hundreds of times, so this grammar must grow, and Rohrmeier's full grammar has many more rules than these six."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        pr = load("progressions")
        c = clip("parsing.plagal")
        strip = chord_strip(pr["seqs"]["plagal"], font_size=30, buff=0.8).to_edge(DOWN, buff=0.35)
        with self.voiceover("Hear it. To a listener it is ordinary: the IV leans back to I, and the cadence follows."):
            self.play(FadeIn(strip))
        with self.listen(c) as snd:
            window(snd, r"I IV I V I", detail=r"Part 7's piano", corner=UL, tag_corner=UR)
            flash(snd, list(strip), chord_times(0.0, pr["seqs"]["plagal"], pr["beat"]), hot=WHITE, base=GREY_A)
            pulse(snd, rows_[0], 0.0, c.duration, buff=0.08)
        self.wait(0.4)
        self.clear_scene()
