from __future__ import annotations

import numpy as np

from videos.music.music22.common import *  # noqa: F403


class Learned(SoundScene):
    def construct(self):
        chapter(self, 7, r"A grammar learned from Bach", r"Does a grammar predict Bach's next chord better than chord pairs?")
        self.method()
        self.scores()
        self.learned()
        self.meaning()

    # ------------------------------------------------------------------
    def method(self):
        d = load("learned")
        rows_ = VGroup(*[label(t, font_size=25, color=c_) for t, c_ in (
            (rf"Part 17's chorales, \ cut at their fermatas: \ {d['train_phrases']} phrases to learn from, \ {d['test_phrases']} held out", WHITE),
            (rf"each phrase a sequence of chord names, \ {d['mean_length']:.1f} long on average", WHITE),
            (r"start from the six rules; \ learn every probability by the inside-outside algorithm", WHITE),
            (r"(expectation-maximization: \ guess, \ parse every phrase every way, \ count, \ re-estimate)", GREY_A),
            (r"score: \ bits per chord on the held-out phrases, \ the end of the phrase counted as a chord", TUNE))]).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"training a grammar", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Can such a grammar be learned from music, and does it describe it better than the chord-pair model of "
            f"Part 18? <bookmark mark='a'/> Take Part 17's chorales and cut them at their fermatas: {say(d['train_phrases'])} "
            f"phrases to learn from, {say(d['test_phrases'])} from chorales with other tunes held out. "
            f"<bookmark mark='b'/> Each phrase is a sequence of chord names, about {say(round(d['mean_length']))} long. "
            "<bookmark mark='c'/> Start from the six rules and learn all the probabilities, which rule a region uses and "
            "which chord it emits, by the inside-outside algorithm: <bookmark mark='d'/> guess the probabilities, parse "
            "every phrase in every possible way, count how often each rule was used, weighted by the probability of "
            "its tree, re-estimate, and repeat. <bookmark mark='e'/> Then score every model by the bits it needs per "
            "chord on the held-out phrases, counting the end of the phrase as one more symbol."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def scores(self):
        d = load("learned")
        b = d["bits"]
        names = [r"no context", r"chord pairs", r"chord triples", r"6-rule grammar", r"12 invented symbols"]
        vals = [b["unigram"], b["bigram"], b["trigram"], b["functional"], b["latent"]["12"]["test"]]
        ch = columns(vals, names, width=9.0, height=2.8, color=WEAK, hot=(1,), hot_color=TUNE, fmt="{:.2f}", font_size=19).move_to(LEFT * 1.0 + DOWN * 0.5)
        t = label(r"bits per chord on held-out chorale phrases \ (lower is better)", font_size=22, color=GREY_A).next_to(ch, UP, buff=0.4)
        side = VGroup(label(r"pairs win", font_size=28, color=TUNE),
                      label(r"the 6-rule grammar: \ worse than pairs", font_size=22, color=WHITE),
                      label(r"a grammar free to invent its symbols: \ close behind", font_size=22, color=WHITE)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * 5.0 + DOWN * 0.3)
        side.scale_to_fit_width(min(side.width, 3.6))
        side.move_to(RIGHT * 5.2 + DOWN * 0.3)
        with self.voiceover(
            f"The scores. Knowing nothing about order costs {say(b['unigram'], 1)} bits a chord. Chord pairs, Part 18's "
            f"model, cost {say(b['bigram'], 1)}; triples do worse, {say(b['trigram'], 1)}, since there is too little data "
            f"to learn them. <bookmark mark='a'/> The six-rule grammar costs {say(b['functional'], 1)}: worse than pairs. "
            "<bookmark mark='b'/> Give a grammar twelve symbols of its own, every rule allowed, and let it invent its "
            f"categories: after training it costs {say(b['latent']['12']['test'], 1)}, close to pairs but not better. "
            "<bookmark mark='c'/> On this data, a tree does not predict the next chord better than the chord before it."
        ) as vo:
            self.play(FadeIn(ch), FadeIn(t))
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[0]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def learned(self):
        d = load("learned")
        cols = VGroup()
        for nt in ("TR", "DR", "SR"):
            rows_ = VGroup(*[label(tex(v) + rf": \ {100 * p:.0f}", font_size=22, color=WHITE) for p, v in d["emit"][nt][:5]])
            rows_.arrange(DOWN, buff=0.18, aligned_edge=LEFT)
            cols.add(VGroup(label(nt, font_size=30, color=REGION_C[nt]), rows_).arrange(DOWN, buff=0.3))
        cols.arrange(RIGHT, buff=1.4, aligned_edge=UP).move_to(UP * 0.4)
        t = label(r"what each region emits after training, \ in a hundred", font_size=22, color=GREY_A).next_to(cols, UP, buff=0.35)
        cap = label(r"tonic and dominant regions: \ as the theory says; \ the subdominant region: \ drifted", font_size=24, color=TUNE).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "What did the six-rule grammar learn? Look at the chords each region emits after training. "
            f"<bookmark mark='a'/> The tonic region emits I {say(round(100 * d['emit']['TR'][0][0]))} times in a hundred and vi "
            f"{say(round(100 * d['emit']['TR'][1][0]))}: as the theory says. The dominant region emits V and V seven, and "
            "sometimes IV, which Bach often places just before a cadence. <bookmark mark='b'/> But the subdominant region "
            "drifted: training found it more useful as a second kind of tonic, and its most frequent chord is I. Nothing "
            "in the algorithm keeps the names honest; it only makes the phrases likely."
        ) as vo:
            self.play(FadeIn(t), FadeIn(cols[0]), FadeIn(cols[1]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(cols[2]), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def meaning(self):
        rows_ = VGroup(*[label(t, font_size=25, color=c_) for t, c_ in (
            (r"a known result in language too: \ simple grammars predict words worse than n-grams", WHITE),
            (r"a grammar's strength is not the next chord: \ it is the long-range dependency", WHITE),
            (r"a phrase that opens on I must close on I: \ the grammar says so; \ pairs cannot", TUNE),
            (r"chorale phrases are short: \ about six chords, \ little room for depth", WHITE),
            (r"prediction and explanation are different tests", EAR))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"what that means", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "What does that mean? <bookmark mark='a'/> The same result is well known in language: simple grammars "
            "predict the next word worse than counting pairs and triples of words. <bookmark mark='b'/> A grammar's "
            "strength is elsewhere, in dependencies across a distance: <bookmark mark='c'/> a phrase that opens on the "
            "tonic must close on it, however long the middle, which a tree states and a chain of pairs cannot. "
            "<bookmark mark='d'/> Chorale phrases are short, about six chords, which leaves little room for depth to "
            "pay off. <bookmark mark='e'/> And prediction and explanation are different tests: a grammar can be the "
            "better description of how a progression is organized and still be the worse guesser of what comes next."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
