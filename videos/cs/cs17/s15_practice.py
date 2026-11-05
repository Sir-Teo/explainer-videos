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
            [r"C++ \texttt{std::unordered\_map}", r"chaining, \ forced by the standard's iterator rules",
             r"\texttt{std::hash}"],
            [r"Rust \texttt{HashMap}, \ Abseil", r"Swiss table: \ open addressing, \ 16 control bytes probed at once",
             r"SipHash, \ or a fast keyed hash"],
            [r"Go \texttt{map}", r"buckets of 8, \ then Swiss tables \ (Go 1.24)", r"AES-based, \ random seed"],
        ]
        tab = grid_table([r"library", r"collisions", r"hash"], rows, widths=[3.6, 6.8, 3.0], row_h=0.66,
                         font_size=19, mono_cols=(), colors=[[DATA, GREY_A, GREY_B]] * len(rows)).next_to(
            head, DOWN, buff=0.5)
        note_ = label(r"every one randomizes its hash per process: \ the lesson of hash flooding", font_size=22,
                      color=YES).next_to(tab, DOWN, buff=0.5)
        with self.voiceover(
            "Every major language ships a hash table, and their designs tell the story of this part. <bookmark "
            "mark='a'/> Python's dictionary uses open addressing with a probe sequence perturbed by the high bits "
            "of the hash, and since version three point seven it keeps entries in a dense array, which also "
            "preserves insertion order. Java's HashMap chains, and since Java 8 a chain that grows too long becomes "
            "a red–black tree, so even an attack costs only log n. C++'s unordered map must chain, because the "
            "standard promises that pointers to elements stay valid. Rust and Google's Abseil use Swiss tables, "
            "probing sixteen control bytes at once; Go moved its map to Swiss tables in 2025. <bookmark mark='b'/> "
            "And every one of them seeds its hash function randomly for each process, the lesson of hash flooding."
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
            label(rf"all thirty novels, \ {d['bytes'] / 1e6:.1f} MB: \ read, \ count, \ top twenty", font_size=21,
                  color=GREY_A),
            label(r"every output checked against the reference", font_size=21, color=GREY_B),
            label(rf"C: \ {d['bytes'] / d['open addressing'] / 1e6:.0f} MB per second, \ about "
                  rf"{1e9 * d['open addressing'] / d['bytes']:.1f} ns per byte", font_size=22, color=YES),
            label(r"Python pays for objects and dispatch, \ not for its hash table", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5)
        if side.width > 5.6:
            side.scale_to_fit_width(5.6).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "Before Pebble's ledger row, here is the Job done natively on this machine. <bookmark mark='a'/> Python, "
            "with a dictionary of counts, reads and counts the thirty novels in under a second. C++'s unordered map "
            "takes a fifth of a second, and a hand-written open-addressing table in C about a tenth. Every output "
            "was checked against the reference. <bookmark mark='b'/> The C version runs at hundreds of megabytes "
            "per second, a few nanoseconds per byte of text. <bookmark mark='c'/> Python's time goes on creating "
            "a string object for every word and dispatching every operation, not on its hash table, which is "
            "among the best engineered anywhere."
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
