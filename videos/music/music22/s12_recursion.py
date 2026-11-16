from __future__ import annotations

import numpy as np

from videos.music.music22.common import *  # noqa: F403


class Recursion(SoundScene):
    def construct(self):
        chapter(self, 11, r"Is harmony recursive?", r"Do listeners hear nested structure?", extra=((2013, r"Koelsch's nested chorales"),))
        self.depths()
        self.nesting()
        self.evidence()

    # ------------------------------------------------------------------
    def depths(self):
        d = load("learned")
        dep = d["depths"]
        by_len = {}
        for n, h in dep:
            by_len.setdefault(n, []).append(h)
        ns = sorted(k for k in by_len if len(by_len[k]) >= 3)
        mean_depth = [float(np.mean(by_len[k])) for k in ns]
        flat = [float(k) for k in ns]
        balanced = [float(np.ceil(np.log2(k)) + 1) for k in ns]
        ch1 = columns(mean_depth, [rf"{k}" for k in ns], width=7.0, height=2.6, color=TUNE, fmt="{:.1f}", font_size=18, top=max(flat) + 1)
        ch1.move_to(LEFT * 2.2 + DOWN * 0.5)
        t = label(r"held-out chorale phrases: \ depth of the best tree, \ by number of chords", font_size=21, color=GREY_A).next_to(ch1, UP, buff=0.4)
        side = VGroup(label(r"a chain would be as deep as it is long", font_size=22, color=WHITE),
                      label(r"a balanced tree: \ about $\log_2$ of the length", font_size=22, color=WHITE),
                      label(rf"selected phrases: \\ deep best trees; \\ {100 * d['parsed_share']:.0f} in 100 pass the vocabulary filter", font_size=22, color=TUNE)).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 4.6))
        side.move_to(RIGHT * 4.4 + DOWN * 0.3)
        with self.voiceover(
            "Tree depth is one descriptive property; recursive grammars need not produce deeply nested examples. Parse every held-out chorale phrase that the six rules can parse, and measure the depth of its best tree. <bookmark mark='a'/> A pure chain, each chord attached to the next, would be as deep as the phrase is long. <bookmark mark='b'/> A perfectly balanced tree would be only about the logarithm of the length. <bookmark mark='c'/> For the subset whose labels lie in the restricted vocabulary, the soft-emission grammar’s best trees are almost as deep as the phrases are long: chains of preparation and resolution, each chord leaning on the next, a tree that branches only one way. On phrases this short, a nested grammar and a chain of pairs describe nearly the same thing, and the data cannot tell them apart, let alone show what a listener hears."
        ) as vo:
            self.play(FadeIn(ch1), FadeIn(t))
            for mark, r in zip("abc", side):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def nesting(self):
        pr = load("progressions")
        c = clip("recursion.nest")
        a, b = pr["seqs"]["nest1"], pr["seqs"]["nest3"]
        sa = chord_strip(a, font_size=28, buff=0.9).move_to(UP * 1.3)
        sb = chord_strip(b, font_size=28, buff=0.6).move_to(DOWN * 0.6)
        la = label(r"one dominant inside another", font_size=22, color=GREY_B).next_to(sa, UP, buff=0.35)
        lb = label(r"four deep: \ E7 \ A7 \ D7 \ G \ C, \ each a dominant of the next", font_size=22, color=GREY_B).next_to(sb, UP, buff=0.35)
        cap = label(r"each level is heard as wanting the next: \ but is that a tree, \ or a chain of pairs?", font_size=24, color=TUNE).to_edge(DOWN, buff=0.55)
        with self.voiceover(
            "What would nesting sound like? <bookmark mark='a'/> First, one dominant inside another: I, the dominant of "
            "the dominant, the dominant, I. <bookmark mark='b'/> Then four deep: E seven, A seven, D seven, G, and home "
            "to C, each chord the dominant of the next, the chain of applied dominants from Part 19."
        ) as vo:
            self.play(FadeIn(la), FadeIn(sa))
            vo.wait_until("b")
            self.play(FadeIn(lb), FadeIn(sb))
        with self.listen(c) as snd:
            window(snd, r"one level, \ then four", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            flash(snd, list(sa), chord_times(pr["nest_starts"]["nest1"], a, pr["beat"]), hot=WHITE, base=GREY_A)
            flash(snd, list(sb), chord_times(pr["nest_starts"]["nest3"], b, pr["beat"]), hot=WHITE, base=GREY_A)
            pulse(snd, la, pr["nest_starts"]["nest1"], pr["nest_starts"]["nest3"] - 0.5, buff=0.08)
            pulse(snd, lb, pr["nest_starts"]["nest3"], c.duration, buff=0.08)
        with self.voiceover(
            "Every chord is heard as wanting the next. But a listener could hear that without any tree: each chord "
            "pulls toward the one after it, a chain of pairs, and the chain arrives home. Whether the opening C is "
            "still held in mind when the last C arrives is exactly what the tree claims, and what only an experiment "
            "can show."
        ):
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def evidence(self):
        rows_ = VGroup(*[label(t, font_size=24, color=c_) for t, c_ in (
            (r"2002: \ Hauser, \ Chomsky and Fitch: \ recursion may be what is special about human language", WHITE),
            (r"2013: \ Koelsch and colleagues rewrote Bach chorales so that an opening key was not resolved at the end", WHITE),
            (r"across an embedded passage in another key: \ a long-distance dependency", WHITE),
            (r"listeners' brains responded to the broken dependency, \ as to a grammatical error", TUNE),
            (r"but Part 21: \ for longer pieces, \ listeners barely notice the wrong key at the end", EAR),
            (r"so nesting is heard over seconds, \ perhaps not over minutes", GREY_A))]).arrange(DOWN, buff=0.34, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"the evidence", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The question matters beyond music. <bookmark mark='a'/> In 2002 Marc Hauser, Noam Chomsky and Tecumseh Fitch proposed that recursion might be the one thing special to human language. If music has it too, the two may share machinery. <bookmark mark='b'/> In 2013 Stefan Koelsch and colleagues, Rohrmeier among them, rewrote Bach chorales so that the key a phrase opened in was not the key it closed in, <bookmark mark='c'/> with a passage in another key embedded between: a dependency across a distance, like the subject and verb of a long sentence. <bookmark mark='d'/> The study reported an electrophysiological response to the manipulation, consistent with sensitivity to a nonlocal dependency; it does not establish identical language processing or recursion by itself. <bookmark mark='e'/> Yet, as Part 21 found, over several minutes listeners hardly notice a piece ending in the wrong key. <bookmark mark='f'/> Together these task-specific results motivate further tests across timescales, rather than a fixed limit on musical nesting: harmony may be recursive in the short range, and something else holds long pieces together."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcdef", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
