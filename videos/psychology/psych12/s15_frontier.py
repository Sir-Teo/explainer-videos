from __future__ import annotations

import numpy as np

from videos.psychology.psych12.common import *  # noqa: F403
from videos.psychology.psych12.s04_roc import roc_axes


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.solid()
        self.meta()
        self.open()

    def card(self):
        card = chapter_card(14, r"Frontier: \ knowing what you saw", r"How well does your confidence track your accuracy?",
                            lit={2012: r"meta-$d'$"}, part=PART, scale=("mind",), marr=("what",))
        with self.voiceover(
            "Chapter fourteen. The frontier: knowing what you saw."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def solid(self):
        head = heading(r"What is solid, \ and what is argued")
        left = rows_of([
            (r"what is solid", HIT),
            (r"sensitivity and criterion separate: \ payoffs, \ base rates and ratings move one line", WHITE),
            (r"ROCs curve; \ the gate-like threshold is gone", WHITE),
            (r"the ideal observer as a yardstick: \ how far from optimal are people?", WHITE),
        ], 5.6, 26, 0.3)
        right = rows_of([
            (r"what is argued", MISS),
            (r"what the evidence axis is: \ one number, \ or several summed?", WHITE),
            (r"why recognition's ROC is lopsided (chapters 6 and 8)", WHITE),
            (r"how people learn where to put the line, \ and why they stop short of optimal", WHITE),
        ], 5.6, 26, 0.3)
        g = VGroup(left, right).arrange(RIGHT, buff=0.8, aligned_edge=UP).move_to([0, 0.4, 0])
        reply = wrapped_label(r"Kant's third objection: \ the report does mix seeing with saying, \ but the mixture can be "
                              r"measured and taken apart", 12.0, 28, KANT).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Here's where the theory stands. <bookmark mark='a'/> Solid: sensitivity and criterion come apart, and "
            "payoffs, base rates and confidence ratings all move one line. ROCs curve, so the old threshold, a gate "
            "below which nothing passes, is gone. And the ideal observer gives a yardstick for how close people get "
            "to the best possible decision. <bookmark mark='b'/> Argued: what the evidence axis really is, one number "
            "or many combined; why recognition's curve is lopsided; and how people learn where to put the line, and "
            "why they usually stop short of the optimum. <bookmark mark='c'/> For Kant's third objection, that's a "
            "strong reply. The report does mix seeing with saying. But the mixture can be measured, and taken apart."
        ) as vo:
            self.play(FadeIn(head), FadeIn(left[0]), FadeIn(right[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in left[1:]], lag_ratio=0.8), run_time=4.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in right[1:]], lag_ratio=0.8), run_time=4.0)
            vo.wait_until("c")
            self.play(FadeIn(reply))
        self.clear_scene()

    def meta(self):
        d = load("confidence")
        src = archive.MANISCALCO_LAU_2012
        head = heading(r"Detection theory, \ turned on yourself")
        R = roc_axes([-3.4, -0.3, 0], size=4.6, xlabel=r"P(confident $\mid$ wrong)", ylabel=r"P(confident $\mid$ right)")
        rx = R.ax
        diag = DashedLine(rx.c2p(0, 0), rx.c2p(1, 1), color=GREY_C, stroke_width=2)
        cols = [HIT, CRIT, MISS]
        cs = VGroup(*[curve(rx, d[f"{n}_f2"], d[f"{n}_h2"], c, stroke_width=4)
                      for n, c in zip(("perfect", "noisy", "noisier"), cols)])
        lg = legend([(HIT, rf"exact confidence: \ area {d['perfect_area']:.2f}"),
                     (CRIT, rf"some extra noise: \ {d['noisy_area']:.2f}"),
                     (MISS, rf"more noise: \ {d['noisier_area']:.2f}")], font_size=20).move_to(rx.c2p(0.68, 0.17))
        rows = rows_of([
            (r"the first decision: \ was there a signal? \ The second: \ was I right?", WHITE),
            (r"the ``type 2'' ROC: \ confidence when right against confidence when wrong", ROCC),
            (rf"three observers with the same $d' = {d['d']:.1f}$ and the same accuracy, \ {pct(d['accuracy'])}; \ only "
             r"their confidence differs", MODEL),
            (r"meta-$d'$ (Maniscalco and Lau 2012) puts this in $d'$ units: \ how much of the evidence confidence can "
             r"use", DATA),
            (r"used to study metacognition, \ insight in illness, \ and in Part 25 the timing of decisions", THRESH),
        ], 5.2, 25, 0.28).move_to([3.7, 0.0, 0])
        keep_in_frame(rows)
        tags = VGroup(published_tag(src.cite), psyche_tag(r"computed: \ 200{,}000 trials each"))
        with self.voiceover(
            "The newest use of the theory turns it on the observer's own judgement. <bookmark mark='a'/> After the "
            "first decision, was there a signal, comes a second: was I right? Confidence is a detector too, and its "
            "signal is being correct. <bookmark mark='b'/> So plot confidence when right against confidence when "
            "wrong, and you get a second ROC. <bookmark mark='c'/> Here are three of Psyche's observers with the same "
            "eyes and the same accuracy. Only their confidence differs: one reads the evidence exactly, two add noise "
            "of their own. Their second ROCs fall in order. <bookmark mark='d'/> In 2012 Brian Maniscalco and Hakwan "
            "Lau showed how to put this in d prime's units, meta d prime: how much of the evidence the confidence "
            "can use. <bookmark mark='e'/> It's how metacognition is measured now, in studies of insight in "
            "psychiatric illness, of expertise, and, in Part 25, of how decisions unfold in time."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tags), FadeIn(R), Create(diag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(c) for c in cs], lag_ratio=0.4), FadeIn(lg), FadeIn(rows[2]), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def open(self):
        head = heading(r"Open questions")
        rows = rows_of([
            (r"is the evidence one number? \ When a radiologist looks, \ many features must be combined", ROCC),
            (r"why do people set criteria short of the optimum, \ and how do they learn them?", CRIT),
            (r"what does recognition's lopsided ROC mean: \ wider old items, \ or recollection?", RIVAL),
            (r"$\star$ \ design a study that tells watcher A from watcher B of chapter 11 in a single session", YOU),
        ], 12.4, 30, 0.45).move_to([0, -0.1, 0])
        with self.voiceover(
            "Four questions to carry out of this part. <bookmark mark='a'/> Is the evidence really one number? A "
            "radiologist combines many features of a shadow. How? <bookmark mark='b'/> Why do people set their "
            "criteria short of the optimum, and how do they learn where to put them? <bookmark mark='c'/> What does "
            "recognition's lopsided curve mean? <bookmark mark='d'/> And the starred problem: design a study that "
            "tells chapter eleven's two watchers apart in a single session."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r))
        self.clear_scene()
