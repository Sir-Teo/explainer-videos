from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs26.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, words)


class Numbers(VoiceoverScene):
    def construct(self):
        self.card()
        self.pseudo()
        self.strong()

    def card(self):
        card = chapter_card(8, r"Strong and weak hardness", r"When is a hard problem only hard because of big "
                            r"numbers?", lit=(1975, 1978), extra=((1975, r"Ibarra--Kim"), (1978, r"Garey--Johnson")),
                            part=PART)
        with self.voiceover("Chapter eight. Strong and weak hardness."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def pseudo(self):
        k = load("knapsack")
        head = label(r"Subset sum: \ NP-complete, \ yet the DP is fast?", font_size=32).to_edge(UP, buff=0.35)
        rows = [[str(r["digits"]), words(r["W"]), f"{r['dp_s'] * 1000:.2f} ms"] for r in k["rows"]]
        tab = grid_table([r"digits per number", r"target $W$", r"DP time"], rows, widths=[2.4, 2.0, 1.8],
                         row_h=0.42, font_size=20, mono_cols=(), colors=[[WHITE, DATA, NO]] * len(rows))
        tab.next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.7)
        tl = label(rf"{k['n']} numbers; \ the DP marks every reachable sum up to $W$ \ (Part 19)", font_size=19,
                   color=GREY_A).next_to(tab, DOWN, buff=0.15).align_to(tab, LEFT)
        notes = VGroup(
            label('scalar DP: $O(nW)$; \\\\ bitset keeps $0\\ldots W$; \\\\ bit/limb costs count', font_size=21, color=WHITE),
            label('binary target: $O(\\log W)$ bits; \\\\ numeric range may grow exponentially',
                  font_size=21, color=NO),
            label('pseudo-polynomial in numeric value; \\\\ not polynomial in binary input length', font_size=21, color=YES),
            label(rf"{k['mitm_digits']}-digit weights: {k['mitm_s']*1000:.0f} ms; \\ meet-in-middle: $O(2^{{n/2}})$ subsets; \\ integer bit costs still count",
                  font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(tab, RIGHT, buff=0.7).align_to(tab, UP)
        if notes.get_right()[0] > 6.9:
            notes.width = 6.9 - notes.get_left()[0]
            notes.next_to(tab, RIGHT, buff=0.7).align_to(tab, UP)
        with self.voiceover(
            "Why can a dynamic program solve subset sum? <bookmark mark='a'/> The familiar dense recurrence uses order n times W scalar work, where W is the target value. Our actual bitset version stores sums from zero through W and shifts many bits at once; each operation still has a limb cost. <bookmark mark='b'/> W can be exponential in its binary encoding length, so this is pseudo-polynomial, not polynomial in the full input length. The digit comparison describes possible numeric-range growth, not an exact law for these timings. <bookmark mark='c'/> The table retains every weight, target, final reachable bitset and explicit subset witness. Separate meet-in-the-middle searches check the answers. <bookmark mark='d'/> For thirty twelve-digit weights, meet in the middle uses exponentially many subsets in half the variable count. It avoids a table proportional to W, while arithmetic and storage still depend on integer bit lengths."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3), FadeIn(tl),
                      FadeIn(notes[0]))
            for mk, n_ in zip("bcd", notes[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def strong(self):
        head = label(r"Weakly against strongly NP-hard", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label('weak numerical hardness: subset sum/partition admit pseudo-polynomial algorithms', font_size=22, color=DATA),
            label('strong hardness persists with polynomially bounded numbers: 3-partition, suitable bin-packing models', font_size=22, color=NO),
            label('graph reductions need no large numbers; subset-sum digits may encode exponentially large values', font_size=22, color=WHITE),
            label('some objectives admit rounding schemes; weak hardness alone does not guarantee an FPTAS', font_size=22, color=YES),
            label('positive-profit 0--1 knapsack: $(1-\\varepsilon)$ approximation in poly(input length, $1/\\varepsilon$)', font_size=22, color=YES),
            label('no FPTAS if strongly hard with bounded integer objectives, unless P = NP; asymptotic schemes differ', font_size=22, color=NO),
            label(r"so ``NP-hard'' is the start of the analysis, \ not the end", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.28).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Numeric encodings refine hardness. <bookmark mark='a'/> Weakly NP-hard numerical problems such as subset sum admit pseudo-polynomial algorithms, but their binary-encoded general cases remain NP-hard. <bookmark mark='b'/> Strong NP-hardness persists even when numeric parameters are polynomially bounded, as in three-partition and suitable bin-packing decision formulations. <bookmark mark='c'/> This distinction is about the input encoding and restrictions; it is not a guarantee about every instance. <bookmark mark='d'/> Some optimization problems admit useful rounding schemes. <bookmark mark='e'/> Positive-profit zero-one knapsack has an FPTAS: for each positive epsilon it obtains at least one minus epsilon of optimum in time polynomial in the input length and one over epsilon. <bookmark mark='f'/> Weak hardness alone does not guarantee an FPTAS. For strongly NP-hard optimization with an integer objective polynomially bounded on the hard restricted instances, an FPTAS would imply P equals NP. Asymptotic schemes such as bin packing's have a different guarantee. <bookmark mark='g'/> State the objective and approximation definition before drawing conclusions from hardness."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdefg", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
