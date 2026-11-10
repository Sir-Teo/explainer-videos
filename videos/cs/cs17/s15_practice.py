from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs17.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, bar_chart, grid_table,
                                   load, mono, words)


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.libraries()
        self.native()

    def card(self):
        card = chapter_card(14, r"Hash tables in practice", r"What do real systems build?", lit=(2017,),
                            extra=((2012, r"SipHash"), (2017, r"Swiss tables")), part=PART)
        with self.voiceover("Chapter fourteen. Hash tables in practice."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def libraries(self):
        head = label(r"What the standard libraries chose", font_size=34).to_edge(UP, buff=0.3)
        rows = [
            [r"Python \texttt{dict}", r"open addressing, \ perturbed probing; \ compact entry array, \ insertion "
                                      r"order kept \ (3.7)", r"SipHash for strings"],
            [r"Java \texttt{HashMap}", r"chaining; \ a long chain becomes a red--black tree \ (Java 8)",
             r"key's \texttt{hashCode}"],
            [r"C++ \texttt{std::unordered\_map}", r"common node-based implementations; \ reference stability constrains layout",
             r"\texttt{std::hash}"],
            [r"Rust \texttt{HashMap}, \ Abseil", r"Swiss family: \ grouped metadata scans; \ width depends on target",
             r"SipHash, \ or a fast keyed hash"],
            [r"Go \texttt{map}", r"Swiss tables with 8-slot groups \ (Go 1.24)", r"per-map random seed; \ platform-dependent hash"],
        ]
        tab = grid_table([r"library", r"collisions", r"hash"], rows, widths=[3.6, 6.8, 3.0], row_h=0.66,
                         font_size=19, mono_cols=(), colors=[[DATA, GREY_A, GREY_B]] * len(rows)).next_to(
            head, DOWN, buff=0.5)
        note_ = label(r"randomization varies: \ ordinary Java hashCode and C++ std::hash are not secret-key defenses", font_size=22,
                      color=YES).next_to(tab, DOWN, buff=0.5)
        with self.voiceover(
            "Library designs share ideas but differ in guarantees. <bookmark mark='a'/> CPython uses open"
            " addressing and a compact insertion-ordered entry array; insertion order became a language "
            "guarantee in three point seven. Java HashMap can treeify long bins, with collision benefits "
            "depending on key ordering. Common C++ unordered-map implementations use nodes to satisfy "
            "reference stability, but the standard does not require one particular chain layout. Rust "
            "uses a SwissTable-derived design. Abseil's SIMD example scans sixteen metadata bytes; Go one"
            " point twenty-four uses eight-slot groups. <bookmark mark='b'/> Randomization is not "
            "universal: CPython string hashes and Rust's default hasher are seeded, whereas Java hashCode"
            " and ordinary C++ std hash are not generally secret-key defenses. Check the exact library, "
            "key type, version and configuration before relying on attack resistance."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab.rule), LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells], lag_ratio=0.35),
                      run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    def native(self):
        d = load("practice")
        head = label(r"The Job, \ natively, \ on this machine", font_size=34).to_edge(UP, buff=0.3)
        vals = [d["python"], d["unordered_map"], d["open addressing"]]
        names = [r"Python \texttt{dict}", r"C++ \texttt{unordered\_map}", r"C, \ open addressing"]
        ch = bar_chart(vals, names, [GREY_A, LAM, YES], height=3.2, bar_w=1.2, gap=1.3,
                       fmt_=lambda v: f"{v:.2f} s" if v >= 1 else f"{1000 * v:.0f} ms", font_size=20).move_to(
            LEFT * 2.0 + DOWN * 0.3)
        side = VGroup(
            label(rf"all thirty novels, \ {d['bytes'] / 1e6:.1f} MB: \ count + top twenty; \ file input excluded", font_size=21,
                  color=GREY_A),
            label(r"every output checked against the reference", font_size=21, color=GREY_B),
            label(rf"C: \ {d['bytes'] / d['open addressing'] / 1e6:.0f} MB per second, \ about "
                  rf"{1e9 * d['open addressing'] / d['bytes']:.1f} ns per byte", font_size=22, color=YES),
            label(r"complete implementations differ; \ this does not isolate container cost", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5)
        if side.width > 5.6:
            side.scale_to_fit_width(5.6).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "Here is the complete word-count task natively on this host. <bookmark mark='a'/> Each "
            "implementation counts the same corpus and selects the top twenty, breaking ties by first "
            "appearance. Every repeat's complete report matches the reference. The bars show the minimum "
            "of three Python repeats or five native repeats. <bookmark mark='b'/> File reading, compiler "
            "startup and output formatting are excluded; allocation, tokenization, counting and report "
            "selection are included. The displayed throughput uses that timed scope. <bookmark mark='c'/>"
            " Languages, parsers, hash functions, allocation and containers all differ. These results "
            "compare complete implementations; they do not isolate the cost of Python's dictionary or "
            "prove one collision scheme universally faster."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ch[0]), FadeIn(ch.names))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in ch.bars], lag_ratio=0.3), FadeIn(ch.vals),
                      FadeIn(side[:2]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.wait(0.3)
        self.clear_scene()
