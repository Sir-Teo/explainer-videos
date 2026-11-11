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
        rows = [[str(r["eps"]), words(r["segments"]), f"{r['model_bytes'] / 1024:,.1f} KiB", f"{r['binary_ns']:.0f}",
                 f"{r['learned_ns']:.0f}"] for r in f["rows"]]
        tab = grid_table([r"error $\varepsilon$", r"segments", r"model", r"binary search, \ ns",
                          r"learned, \ ns"], rows, widths=[1.6, 1.8, 1.8, 2.8, 2.0], row_h=0.42, font_size=20,
                         mono_cols=(), colors=[[WHITE, LAM, HEAD, NO, YES]] * len(rows))
        tab.next_to(head, DOWN, buff=0.4).set_x(0)
        notes = VGroup(
            label(rf"keys: \ the {words(f['n'])} byte offsets where words start \ ({f['key_bytes'] / 1e6:.0f} MB)",
                  font_size=21, color=WHITE),
            label('anchored greedy fit; validate each search bracket; full-search fallback \\\\ every actual query checked independently', font_size=21, color=LAM),
            label(r"Kraska, \ Beutel, \ Chi, \ Dean and Polyzotis (2018): \ ``The case for learned index structures''; "
                  r"\ Ferragina and Vinciguerra's PGM index (2020)", font_size=20, color=GREY_A),
            label('model bytes include native structs, padding and separator keys \\\\ active storage differs from peak requested storage',
                  font_size=21, color=YES),
        ).arrange(DOWN, buff=0.2).next_to(tab, DOWN, buff=0.35)
        with self.voiceover(
            "A learned index predicts positions from keys. <bookmark mark='a'/> Our keys are the corpus's "
            "word-start byte offsets; their storage is reported separately. <bookmark mark='b'/> This teaching "
            'implementation greedily fits lines anchored at segment starts. It evaluates every stored-key error, '
            "then certifies each query's predicted search bracket and falls back to full binary search if "
            "needed. Every actual query is independently checked with NumPy searchsorted. <bookmark mark='c'/> "
            'Kraska and colleagues developed learned-index systems, while the PGM work provides stronger '
            'indexing constructions; our floating-point anchored fit is not its optimal segmentation algorithm. '
            "<bookmark mark='d'/> The table counts native segment structs and separator keys, including padding. "
            'It also records peak requested model storage. Lookup clocks exclude fitting and validation, and a '
            'smaller model can still incur segment-search and fallback costs.'
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
        tab = grid_table([r"$\lambda$"] + [rf"noise {sg:g}$B$" for sg in sigmas] + [r"worst case"], rows,
                         widths=[1.6] + [1.6] * len(sigmas) + [1.8], row_h=0.44, font_size=20, mono_cols=(),
                         colors=[[WHITE] + [YES] * len(sigmas) + [NO]] * len(rows))
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        notes = VGroup(
            label('forecast long: buy on $\\lceil\\lambda B\\rceil$; short: $\\lceil B/\\lambda\\rceil$ \\\\ buy at start of day; rent one unit per earlier day', font_size=21, color=WHITE),
            label('published upper bounds: $1+\\lambda$ consistency, $1+1/\\lambda$ robustness \\\\ table: exact discrete worst ratio; two buy-day witnesses', font_size=21, color=YES),
            label('Gaussian noise SD $\\sigma B$; 4,000 seasons per cell; $B=10$ \\\\ finite means are separate from the exact discrete worst bound', font_size=20, color=GREY_A),
            label(r"the same bargain for caching \ (Lykouris and Vassilvitskii, 2018), \ scheduling, \ and Part 23's "
                  r"online problems", font_size=21, color=LAM),
        ).arrange(DOWN, buff=0.2).next_to(tab, DOWN, buff=0.35)
        with self.voiceover(
            "Predictions can also guide an online decision. <bookmark mark='a'/> In discrete ski rental, buying "
            'costs B and each rental day costs one. If the forecast is at least B, buy at the start of day '
            'ceiling lambda B; otherwise use day ceiling B over lambda. Lambda lies above zero and at most one. '
            "<bookmark mark='b'/> The literature's one plus lambda consistency and one plus one over lambda "
            'robustness are upper bounds. Our table gives the tighter exact discrete worst case, attained at one '
            "of the two buy-day witnesses. <bookmark mark='c'/> With B ten and lambda one tenth, a short "
            'forecast and a hundred-day season cost a hundred and nine against optimum ten: ratio ten point '
            'nine. Synthetic Gaussian forecast experiments provide means, not worst-case proofs or trained-model '
            "performance. <bookmark mark='d'/> This deterministic policy illustrates the tradeoff studied by "
            'Purohit, Svitkina and Kumar. A forecast can help, while the guarantee must cover forecasts that are '
            'completely wrong.'
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
            label('four lower-bound implementations; different comparisons and SIMD work',
                  font_size=22, color=WHITE),
            label('word-RAM: bounded-width operations; external memory: block transfers', font_size=22,
                  color=NO),
            label(r"external memory \ (Aggarwal and Vitter, 1988): \ count block transfers of size $B$", font_size=22,
                  color=LAM),
            label('cache-oblivious search: $O(1+\\log_B n)$ transfers in an ideal-cache model \\\\ model and layout assumptions are required', font_size=22, color=HEAD),
            label('research task: specify a model, then test held-out workload predictions', font_size=22,
                  color=YES),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Cost models describe selected resources. <bookmark mark='a'/> Our four searches share a lower-bound "
            'specification while performing different scalar comparisons, vector work and memory accesses. '
            "<bookmark mark='b'/> The word-RAM model counts bounded-width operations under its assumptions, not "
            "elapsed host nanoseconds. <bookmark mark='c'/> External-memory analysis instead counts transfers "
            "between memory levels with a specified block size and capacity. <bookmark mark='d'/> In an "
            'ideal-cache model, suitable cache-oblivious search layouts can achieve logarithmic-in-block-base '
            "transfer bounds without encoding the block size. Optimality requires the model's cache, block and "
            "problem assumptions; it is not a blanket statement about every real cache. <bookmark mark='e'/> "
            'Prefetching, SIMD, branches and shared-host interference call for additional modeling or controlled '
            'experiments. The research task is to specify a useful model and test its predictions on held-out '
            'workloads.'
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
        head = label('Research plans and established baselines', font_size=36).to_edge(UP, buff=0.4)
        qs = VGroup(
            label(r"a cost model that ranks real implementations: \ caches, \ prefetching, \ SIMD, \ branches",
                  font_size=23, color=YES),
            label('dynamic PGM already exists: reproduce it, then scope a narrower update question', font_size=23,
                  color=LAM),
            label('finite corpus slope versus the IID fixed-slope MET baseline: \\\\ different procedures and regimes; reproduce before comparing', font_size=23, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(head, DOWN, buff=0.8)
        star = label(r"$\bigstar$ \ the part's research problem takes the third", font_size=22, color=GREY_A
                     ).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Here are three concrete research directions. <bookmark mark='a'/> Specify a cost model and evaluate "
            "whether it ranks unseen implementations and workloads. <bookmark mark='b'/> Dynamic learned indexes "
            'with worst-case guarantees already exist, including the PGM work. Reproduce an existing baseline '
            'before asking a narrower question about update patterns, adversarial keys or resource tradeoffs. '
            "<bookmark mark='c'/> For the segment experiment, separate a finite corpus fit from the "
            'probabilistic theorem. Under positive independent identically distributed gaps with finite nonzero '
            'variance, the paper analyzes a fixed-slope mean-exit-time construction in a suitable large-epsilon '
            "regime. Our anchored greedy fit is a different procedure. <bookmark mark='d'/> First reproduce that "
            'baseline on generated independent gaps. Then compare real, shuffled and correlated gaps across '
            'scales and seeds. A slope through a few corpus points is a descriptive statistic, not a new '
            'asymptotic law or a contradiction of the theorem.'
        ) as vo:
            self.play(FadeIn(head))
            for mk, q in zip("abc", qs):
                vo.wait_until(mk)
                self.play(FadeIn(q, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(star))
        self.wait(0.5)
        self.clear_scene()
