from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs24.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.learned()
        self.predictions()
        self.gap()
        self.open_()

    def card(self):
        card = chapter_card(15, r"Frontier: \ learned indexes and predictions", r"Can an algorithm learn its input?",
                            lit=(2018, 2020), extra=((2018, r"Kraska et al.; \ Lykouris--Vassilvitskii"),
                                                     (2020, r"the PGM index")), part=PART)
        with self.voiceover("Chapter fifteen. Frontier: learned indexes, and algorithms with predictions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def learned(self):
        f = load("frontier")
        head = label(r"A learned index over the corpus's word offsets", font_size=30).to_edge(UP, buff=0.3)
        rows = [[str(r["eps"]), words(r["segments"]), f"{r['model_bytes'] / 1024:,.1f} KB", f"{r['binary_ns']:.0f}",
                 f"{r['learned_ns']:.0f}"] for r in f["rows"]]
        tab = grid_table([r"error $\varepsilon$", r"segments", r"model", r"binary search, \ ns",
                          r"learned, \ ns"], rows, widths=[1.6, 1.8, 1.8, 2.8, 2.0], row_h=0.42, font_size=20,
                         mono_cols=(), colors=[[WHITE, LAM, HEAD, NO, YES]] * len(rows))
        tab.next_to(head, DOWN, buff=0.4).set_x(0)
        notes = VGroup(
            label(rf"keys: \ the {words(f['n'])} byte offsets where words start \ ({f['key_bytes'] / 1e6:.0f} MB)",
                  font_size=21, color=WHITE),
            label(r"the model: \ straight lines, \ each guaranteed within $\varepsilon$ positions of the truth \ "
                  r"(a greedy PGM-style fit); \ then binary-search only $\pm\varepsilon$", font_size=21, color=LAM),
            label(r"Kraska, \ Beutel, \ Chi, \ Dean and Polyzotis (2018): \ ``The case for learned index structures''; "
                  r"\ Ferragina and Vinciguerra's PGM index (2020)", font_size=20, color=GREY_A),
            label(r"1.5 KB of lines index 37 MB of keys, \ and find them faster: \ the data's regularity is the index",
                  font_size=21, color=YES),
        ).arrange(DOWN, buff=0.2).next_to(tab, DOWN, buff=0.35)
        with self.voiceover(
            "The frontier has a simple question: what if a data structure could learn the shape of its data? "
            "<bookmark mark='a'/> Take the four point six million positions where words begin in our corpus, a "
            "sorted array of thirty-seven megabytes. <bookmark mark='b'/> A sorted array is a function from keys to "
            "positions, and this one is nearly a straight line. Fit it with line segments, each guaranteed to "
            "predict every position within epsilon. To look a key up, find its segment, predict, and binary-search "
            "only the small window around the prediction. <bookmark mark='c'/> Tim Kraska and colleagues at Google "
            "proposed learned indexes in 2018; Paolo Ferragina and Giorgio Vinciguerra's PGM index made the "
            "guarantees exact. <bookmark mark='d'/> Here sixty-four segments, a kilobyte and a half, index the whole "
            "array to within two hundred and fifty-six positions, and lookups are about one and a half times faster "
            "than binary search."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

    def predictions(self):
        f = load("frontier")
        head = label(r"Algorithms with predictions: \ ski rental, \ again", font_size=32).to_edge(UP, buff=0.3)
        lams = sorted({s["lam"] for s in f["ski"]})
        sigmas = sorted({s["sigma"] for s in f["ski"]})
        get = {(s["lam"], s["sigma"]): s for s in f["ski"]}
        rows = [[f"{lam:g}"] + [f"{get[(lam, sg)]['mean']:.2f}" for sg in sigmas] +
                [f"{get[(lam, sigmas[0])]['worst_case']:.1f}"] for lam in lams]
        tab = grid_table([r"trust $\lambda$"] + [rf"error {sg:g}$B$" for sg in sigmas] + [r"worst case"], rows,
                         widths=[1.6] + [1.6] * len(sigmas) + [1.8], row_h=0.44, font_size=20, mono_cols=(),
                         colors=[[WHITE] + [YES] * len(sigmas) + [NO]] * len(rows))
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        notes = VGroup(
            label(r"a model predicts the season's length; \ with parameter $\lambda$, \ buy early if it says long, \ "
                  r"late if short \ (Purohit, \ Svitkina and Kumar, 2018)", font_size=21, color=WHITE),
            label(r"\textbf{consistency} $1 + \lambda$ when the prediction is right; \ \textbf{robustness} "
                  r"$1 + 1/\lambda$ however wrong it is", font_size=21, color=YES),
            label(r"mean ratio to the clairvoyant, \ 4,000 seasons per cell, \ $B = 10$", font_size=20, color=GREY_A),
            label(r"the same bargain for caching \ (Lykouris and Vassilvitskii, 2018), \ scheduling, \ and Part 23's "
                  r"online problems", font_size=21, color=LAM),
        ).arrange(DOWN, buff=0.2).next_to(tab, DOWN, buff=0.35)
        with self.voiceover(
            "Part 23's online algorithms assumed nothing about the future. In practice we often have a forecast. "
            "<bookmark mark='a'/> Give ski rental a prediction of the season's length, and a trust parameter lambda: "
            "if the forecast says long, buy after lambda B days; if short, wait until B over lambda. <bookmark "
            "mark='b'/> If the forecast is right the cost is at most one plus lambda times the best, and however wrong "
            "it is, never more than one plus one over lambda. <bookmark mark='c'/> With lambda a tenth and a perfect "
            "forecast we pay exactly what the clairvoyant pays; as the forecast's error grows, the cost rises "
            "gracefully, and the worst case stays bounded. With lambda equal to one we are back at Part 23's "
            "break-even rule, which ignores the forecast. <bookmark mark='d'/> Manish Purohit, Zoya Svitkina and "
            "Ravi Kumar, and Thodoris Lykouris and Sergei Vassilvitskii for caching, started this field in 2018: "
            "use machine learning when it is right, and keep a worst-case guarantee when it is not."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

    def gap(self):
        lay = load("layouts")["rows"][-1]
        head = label(r"The theory--practice gap, \ measured", font_size=32).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(rf"four searches, \ the same $\log_2 n$ comparisons: \ {lay['branchy']:.0f}, \ "
                  rf"{lay['branchless']:.0f}, \ {lay['eytzinger']:.0f} and {lay['btree']:.0f} ns \ (chapter 9)",
                  font_size=22, color=WHITE),
            label(r"the RAM model of Part 16 counts operations; \ the machine charges for distance", font_size=22,
                  color=NO),
            label(r"external memory \ (Aggarwal and Vitter, 1988): \ count block transfers of size $B$", font_size=22,
                  color=LAM),
            label(r"cache-oblivious \ (Frigo, \ Leiserson, \ Prokop and Ramachandran, 1999): \ optimal for every $B$ "
                  r"at once, \ the van Emde Boas layout", font_size=22, color=HEAD),
            label(r"neither predicts prefetching, \ SIMD or branch prediction: \ a model that does is open", font_size=22,
                  color=YES),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Underneath this whole part runs a gap between theory and practice. <bookmark mark='a'/> Four searches "
            "with exactly the same comparisons differ fivefold on sixty-four million keys. <bookmark mark='b'/> The "
            "random-access machine of Part 16 counts operations; real machines charge for distance. <bookmark "
            "mark='c'/> Alok Aggarwal and Jeffrey Vitter's external-memory model counts the transfers of blocks "
            "between a small fast memory and a large slow one. <bookmark mark='d'/> The cache-oblivious model of "
            "Matteo Frigo, Charles Leiserson and colleagues asks for algorithms that are optimal for every block size "
            "at once, without knowing it, like the van Emde Boas tree layout. <bookmark mark='e'/> Neither captures "
            "prefetching, vector units or branch prediction, which decided several of this part's measurements. A "
            "model simple enough to reason with and accurate enough to rank real implementations is still missing."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def open_(self):
        f = load("frontier")
        rr = f["rows"]
        xs = np.log([r["eps"] for r in rr[:4]])
        ys = np.log([f["n"] / r["segments"] for r in rr[:4]])
        slope = float(np.polyfit(xs, ys, 1)[0])
        head = label(r"Open questions", font_size=36).to_edge(UP, buff=0.4)
        qs = VGroup(
            label(r"a cost model that ranks real implementations: \ caches, \ prefetching, \ SIMD, \ branches",
                  font_size=23, color=YES),
            label(r"learned indexes with worst-case guarantees under inserts and adversarial keys", font_size=23,
                  color=LAM),
            label(rf"why our corpus needs segments of length $\sim\varepsilon^{{{slope:.1f}}}$, \ when independent "
                  r"gaps give $\varepsilon^2$", font_size=23, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(head, DOWN, buff=0.8)
        star = label(r"$\bigstar$ \ the part's research problem takes the third", font_size=22, color=GREY_A
                     ).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Here is where things stand. <bookmark mark='a'/> Is there a cost model that ranks real implementations "
            "correctly, accounting for caches, prefetching, vector units and branches, and is still simple enough to "
            "prove things in? <bookmark mark='b'/> Can learned indexes keep worst-case guarantees when keys are "
            "inserted, or chosen by an adversary? <bookmark mark='c'/> And a puzzle from our own measurements. "
            "Ferragina, Lillo and Vinciguerra proved that if the gaps between keys are independent, the segments "
            "grow like epsilon squared. On our corpus they grow more slowly, roughly like epsilon to the one point "
            "four. Why? <bookmark mark='d'/> This part's research problem takes the third."
        ) as vo:
            self.play(FadeIn(head))
            for mk, q in zip("abc", qs):
                vo.wait_until(mk)
                self.play(FadeIn(q, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(star))
        self.wait(0.5)
        self.clear_scene()
