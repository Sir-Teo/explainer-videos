from __future__ import annotations

import numpy as np

from videos.music.music22.common import *  # noqa: F403


class Grammar(SoundScene):
    def construct(self):
        chapter(self, 5, r"Harmony as a grammar", r"Can chord progressions be parsed like sentences?", extra=((2011, r"Rohrmeier's grammar of harmony"),))
        self.rules()
        self.trees()
        self.recursion()

    # ------------------------------------------------------------------
    def rules(self):
        d = load("parses")
        rl = VGroup(*[label(rf"{a} $\to$ {b} \ {c}", font_size=30, color=WHITE) for a, b, c in d["rules"]]).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(LEFT * 3.6 + DOWN * 0.1)
        lex = VGroup(label(r"TR $\to$ I, \ vi, \ iii", font_size=28, color=REGION_C["TR"]),
                     label(r"DR $\to$ V, \ V7, \ vii$^\circ$", font_size=28, color=REGION_C["DR"]),
                     label(r"SR $\to$ IV, \ ii, \ ii7", font_size=28, color=REGION_C["SR"])).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(RIGHT * 3.0 + UP * 0.6)
        expl = VGroup(label(r"TR, \ DR, \ SR: \ tonic, \ dominant, \ subdominant regions", font_size=22, color=GREY_A),
                      label(r"a region either splits in two, \ or is a single chord", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(lex, DOWN, buff=0.5)
        with self.voiceover(
            "Linguists describe sentences with grammars: a sentence is a noun phrase and a verb phrase, a noun phrase a "
            "determiner and a noun, and so on, down to words. In 2011 Martin Rohrmeier wrote harmony the same way. "
            "<bookmark mark='a'/> Here is a small teaching grammar inspired by that work. A tonic region can be a dominant region followed by a tonic "
            "region: the cadence. A dominant region can be a subdominant region followed by a dominant region: the "
            "preparation. Any region can be two regions of the same kind: prolongation. <bookmark mark='b'/> And at the "
            "bottom, each region is a chord of its function. <bookmark mark='c'/> Six rules and three lists, and every "
            "progression they generate is a tree."
        ) as vo:
            self.play(FadeIn(rl[1]), FadeIn(rl[2]))
            vo.wait_until("a")
            self.play(FadeIn(rl[0]), FadeIn(rl[3:]))
            vo.wait_until("b")
            self.play(FadeIn(lex))
            vo.wait_until("c")
            self.play(FadeIn(expl))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def trees(self):
        d = load("parses")
        ex = d["examples"]
        t1 = tree_mob(ex["I IV V I"]["tree"], width=4.6, level_h=0.7).move_to(LEFT * 3.4 + DOWN * 0.4)
        t2 = tree_mob(ex["I vi ii V I"]["tree"], width=5.6, level_h=0.6).move_to(RIGHT * 3.2 + DOWN * 0.4)
        c1 = label(r"I \ IV \ V \ I", font_size=26, color=GREY_A).next_to(t1, UP, buff=0.3)
        c2 = label(r"I \ vi \ ii \ V \ I", font_size=26, color=GREY_A).next_to(t2, UP, buff=0.3)
        with self.voiceover(
            "Two parses, the most probable trees under a soft-emission version of these rules. <bookmark mark='a'/> I, IV, V, I: an opening tonic "
            "prolonged by a cadence, the cadence a dominant region, prepared by IV, resolving to the final I. "
            "<bookmark mark='b'/> I, vi, ii, V, I: the first two chords group together as one tonic region, vi "
            "prolonging I, and the rest is the same cadence, prepared by ii. <bookmark mark='c'/> The tree says what a "
            "musician means by the function of a chord: not what it is, but what it does, and to which other chord it "
            "belongs."
        ) as vo:
            self.play(FadeIn(c1), FadeIn(t1))
            vo.wait_until("b")
            self.play(FadeIn(c2), FadeIn(t2))
            vo.wait_until("c")
        pr = load("progressions")
        c = clip("grammar.two")
        s1, s2 = t1.leaves, t2.leaves
        with self.voiceover("Hear them, each tree's chords lighting as they sound."):
            self.play(Indicate(VGroup(*s1, *s2), color=WHITE, scale_factor=1.1))
        with self.listen(c) as snd:
            window(snd, r"I IV V I, \ then I vi ii V I", detail=r"Part 7's piano", corner=UL, tag_corner=UR)
            flash(snd, list(s1), chord_times(pr["two_starts"]["cadence"], pr["seqs"]["cadence"], pr["beat"]), hot=TUNE, base=WHITE)
            flash(snd, list(s2), chord_times(pr["two_starts"]["longer"], pr["seqs"]["longer"], pr["beat"]), hot=TUNE, base=WHITE)
            pulse(snd, c1, pr["two_starts"]["cadence"], pr["two_starts"]["longer"] - 0.5, buff=0.08)
            pulse(snd, c2, pr["two_starts"]["longer"], c.duration, buff=0.08)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recursion(self):
        rows_ = VGroup(*[label(t, font_size=25, color=c_) for t, c_ in (
            (r"DR $\to$ SR DR: \ a dominant region can contain a dominant region", WHITE),
            (r"so cadences nest inside cadences: \ V of V of V \ ... \ (Part 19's applied dominants)", WHITE),
            (r"a grammar with a rule that contains itself is recursive", TUNE),
            (r"in language, \ recursion is what makes sentences unbounded", WHITE),
            (r"in music: \ is it heard, \ or only drawn? \ (chapter 11)", EAR))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"recursion", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "One feature of these rules matters more than the rest. <bookmark mark='a'/> A dominant region can contain "
            "a dominant region. <bookmark mark='b'/> So cadences can nest inside cadences: the dominant of the dominant "
            "of the dominant, Part 19's chain of applied dominants, each one preparing the next. "
            "<bookmark mark='c'/> A productive self-embedding rule permits recursive derivations; recursion can also involve several mutually dependent symbols. "
            "<bookmark mark='d'/> In language, recursion is what lets sentences grow without limit: the cat that the dog "
            "that the man owned chased. <bookmark mark='e'/> Whether listeners actually hear nested harmony, or whether "
            "it exists only in the analyst's tree, is the question of chapter eleven."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
