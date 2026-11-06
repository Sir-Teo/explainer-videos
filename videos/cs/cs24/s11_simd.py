from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs24.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)


class Simd(VoiceoverScene):
    def construct(self):
        self.card()
        self.scan()
        self.autovec()
        self.swiss()

    def card(self):
        card = chapter_card(10, r"Algorithm engineering II: \ SIMD and hashing", r"What if one instruction could "
                            r"look at 32 bytes?", lit=(2017, 2019), extra=((2017, r"Abseil's Swiss tables"),
                                                                           (2019, r"simdjson")), part=PART)
        with self.voiceover("Chapter ten. Algorithm engineering, part two: vector instructions and hashing."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def scan(self):
        t = load("simd")["token"]
        head = label(r"Finding words, \ 32 bytes at a time", font_size=34).to_edge(UP, buff=0.3)
        text = "It was the best of times, it wa"
        cw = 0.34
        cells = VGroup(*[VGroup(Rectangle(width=cw, height=0.46, stroke_color=GREY_D, stroke_width=1),
                                mono(ch if ch != " " else "_", 18, WHITE)) for ch in text])
        for c in cells:
            c[1].move_to(c[0])
        cells.arrange(RIGHT, buff=0).next_to(head, DOWN, buff=0.5).shift(RIGHT * 0.9)
        is_l = [ch.isalpha() for ch in text]
        bits = VGroup(*[mono("1" if b else "0", 18, YES if b else GREY_C).next_to(c, DOWN, buff=0.12)
                        for b, c in zip(is_l, cells)])
        starts = [b and (i == 0 or not is_l[i - 1]) for i, b in enumerate(is_l)]
        sb = VGroup(*[mono("1" if b else "0", 18, HEAD if b else GREY_C).next_to(x, DOWN, buff=0.12)
                      for b, x in zip(starts, bits)])
        bl = label(r"letters $L$", font_size=18, color=YES).next_to(bits, LEFT, buff=0.2)
        sl = label(r"starts $L \mathbin{\&} \lnot(L \ll 1)$", font_size=18, color=HEAD).next_to(sb, LEFT, buff=0.2)
        steps = VGroup(
            label(r"load 32 bytes; \ OR \texttt{0x20} lower-cases letters; \ subtract \texttt{'a'}; \ letters are "
                  r"those $\le 25$", font_size=21, color=WHITE),
            label(r"one \texttt{movemask} turns 32 comparisons into a 32-bit word $L$", font_size=21, color=YES),
            label(r"word starts and ends are bit operations on $L$; \ popcount counts them", font_size=21, color=HEAD),
            label(rf"the whole corpus, \ {t['bytes'] / 1e6:.0f} MB: \ byte by byte {t['scalar_s'] * 1000:.1f} ms "
                  rf"\ ({t['bytes'] / t['scalar_s'] / 1e9:.2f} GB/s); \ AVX2 {t['simd_s'] * 1000:.1f} ms \ "
                  rf"({t['bytes'] / t['simd_s'] / 1e9:.1f} GB/s): \ {t['scalar_s'] / t['simd_s']:.1f}$\times$",
                  font_size=21, color=YES),
            label(rf"both find {words(t['words'])} words and {words(t['letters'])} letters; \ simdjson parses JSON this "
                  r"way \ (Langdale and Lemire, 2019)", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.2).next_to(sb, DOWN, buff=0.45)
        with self.voiceover(
            "The Job spends much of its time finding words, one byte at a time. A modern core can look at thirty-two "
            "bytes in one instruction. <bookmark mark='a'/> Load thirty-two bytes. OR each with hexadecimal twenty, "
            "which lower-cases every letter, subtract the code for a, and the letters are exactly the bytes that come "
            "out at most twenty-five, all thirty-two compared at once. <bookmark mark='b'/> One more instruction, "
            "movemask, gathers the thirty-two answers into the bits of an ordinary integer. <bookmark mark='c'/> "
            "Now the word boundaries are bit tricks from chapter seven: a start is a letter whose left neighbour is "
            "not one, L and not L shifted. <bookmark mark='d'/> On the whole corpus, twenty-five megabytes, the "
            "byte-at-a-time loop takes forty milliseconds and the vector version four and a half: almost nine times "
            "faster, with the same counts. <bookmark mark='e'/> The simdjson library parses JSON at gigabytes per "
            "second with exactly these ideas."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in bits], lag_ratio=0.03), FadeIn(bl), FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b) for b in sb], lag_ratio=0.03), FadeIn(sl), FadeIn(steps[2]))
            vo.wait_until("d")
            self.play(FadeIn(steps[3]))
            vo.wait_until("e")
            self.play(FadeIn(steps[4]))
        self.wait(0.3)
        self.clear_scene()

    def autovec(self):
        v = load("vector")
        o1, o3 = v["o1"], v["o3"]
        head = label(r"Letting the compiler vectorize", font_size=34).to_edge(UP, buff=0.35)
        rows = [[r"\texttt{y[i] = a * x[i] + y[i]}", f"{o1['saxpy']:.2f}", f"{o3['saxpy']:.2f}",
                 rf"{o1['saxpy'] / o3['saxpy']:.1f}$\times$"],
                [r"\texttt{s += x[i]}", rf"{o1['isum']:.2f}", f"{o3['isum']:.2f}", rf"{o1['isum'] / o3['isum']:.1f}$\times$"],
                [r"\texttt{x[i] += x[i - 1]}", rf"{o1['prefix']:.2f}", f"{o3['prefix']:.2f}",
                 rf"{o1['prefix'] / o3['prefix']:.1f}$\times$"]]
        tab = grid_table([r"loop \ (65,536 elements)", r"\texttt{-O1}, \ ns", r"\texttt{-O3 -march=native}",
                          r"speedup"], rows, widths=[4.8, 2.0, 3.4, 1.6], row_h=0.48, font_size=21, mono_cols=(),
                         colors=[[YES] * 4, [YES] * 4, [NO] * 4])
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        notes = VGroup(
            label(r"independent iterations: \ the compiler packs 8 or 16 values into each vector instruction", font_size=21,
                  color=YES),
            label(r"\texttt{restrict} promises the arrays don't overlap; \ without it the compiler must check or give up",
                  font_size=21, color=WHITE),
            label(r"a prefix sum carries a dependency from each iteration to the next: \ little to vectorize \ "
                  r"(it gains only from unrolling)", font_size=21, color=NO),
            label(r"write simple loops over arrays, \ and read the compiler's report \ (\texttt{-fopt-info-vec})",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.22).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "Writing vector instructions by hand is a last resort. The compiler will often do it for you. <bookmark "
            "mark='a'/> The same three loops, compiled without and with vectorization. A scaled vector addition and "
            "a plain sum run about three times faster, because every iteration is independent and the compiler can "
            "pack eight or sixteen of them into each instruction. <bookmark mark='b'/> It can only do that when it can prove "
            "the arrays don't overlap, which is what the restrict keyword promises. <bookmark mark='c'/> A running "
            "prefix sum carries a dependency from each element to the next, so there is little to vectorize; it gains "
            "less, and only from unrolling. <bookmark mark='d'/> The practical rule: keep hot loops simple, over "
            "arrays, without hidden aliasing, and ask the compiler to report what it vectorized."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[1])), FadeIn(VGroup(*tab.cells[2])), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[3])), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

    def swiss(self):
        s = load("simd")
        head = label(r"Swiss tables: \ probing 16 slots with one compare", font_size=32).to_edge(UP, buff=0.3)
        cw = 0.34
        ctrl = [0x80, 0x15, 0x80, 0x3a, 0x15, 0x80, 0x07, 0x61, 0x80, 0x80, 0x15, 0x22, 0x80, 0x4c, 0x80, 0x09]
        grp = VGroup(*[VGroup(Rectangle(width=cw, height=0.46, stroke_color=GREY_B, stroke_width=1).set_fill(
            GREY_D if c == 0x80 else DATA, 0.25 if c == 0x80 else 0.5),
            mono("--" if c == 0x80 else f"{c:02x}", 13, WHITE)) for c in ctrl])
        for g in grp:
            g[1].move_to(g[0])
        grp.arrange(RIGHT, buff=0).next_to(head, DOWN, buff=0.55).to_edge(LEFT, buff=0.8)
        gl = label(r"one group: \ 16 control bytes", font_size=18, color=GREY_A).next_to(grp, UP, buff=0.1)
        hits = VGroup(*[SurroundingRectangle(grp[i], color=YES, buff=0.02, stroke_width=3)
                        for i, c in enumerate(ctrl) if c == 0x15])
        expl = VGroup(
            label(r"hash $\to$ $H_1$ picks the group, \ $H_2$ = 7 bits", font_size=20, color=WHITE),
            label(r"compare $H_2$ with all 16 bytes: \ a bitmask of candidates", font_size=20, color=YES),
            label(r"an empty byte in the group ends the search", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(grp, RIGHT, buff=0.5)
        if expl.get_right()[0] > 6.9:
            expl.shift(LEFT * (expl.get_right()[0] - 6.9))

        def pick(rows, k):
            return next(r for r in rows if r["logcap"] == k)
        h5 = pick(s["load_0.5"], 24)
        h8 = pick(s["load_0.875"], 24)
        rows = [[r"\texttt{std::unordered\_map} \ (chaining)", f"{h5['umap_get']:.0f}", f"{h8['umap_get']:.0f}",
                 f"{h8['umap_ins']:.0f}"],
                [r"linear probing", f"{h5['linear_get']:.0f}", f"{h8['linear_get']:.0f}", f"{h8['linear_ins']:.0f}"],
                [r"Swiss-style \ (SSE2 groups)", f"{h5['swiss_get']:.0f}", f"{h8['swiss_get']:.0f}",
                 f"{h8['swiss_ins']:.0f}"]]
        tab = grid_table([r"16 M slots, \ ns per operation", r"find, \ $\tfrac12$ full", r"find, \ $\tfrac78$ full",
                          r"insert, \ $\tfrac78$ full"], rows, widths=[5.0, 2.2, 2.2, 2.4], row_h=0.46, font_size=21,
                         mono_cols=(), colors=[[GREY_A] * 4, [NO] * 4, [YES] * 4])
        tab.next_to(grp, DOWN, buff=0.8).set_x(0)
        notes = VGroup(
            label(r"half the finds miss; \ 64-bit keys; \ C++ with \texttt{-O2 -march=native}", font_size=20,
                  color=GREY_A),
            label(rf"at $\tfrac78$ full, \ linear probing's clusters cost {h8['linear_get'] / h8['swiss_get']:.1f}"
                  r"$\times$; \ the control bytes keep probes short and in one cache line", font_size=21, color=YES),
            label(r"chaining pays a pointer chase per node, \ the opening chapter's linked list again", font_size=21,
                  color=NO),
            label(r"Google's Abseil (2017), \ Rust's \texttt{HashMap}, \ Facebook's F14: \ all this design", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.18).next_to(tab, DOWN, buff=0.35)
        with self.voiceover(
            "Vector instructions also rebuilt the hash table. <bookmark mark='a'/> A Swiss table, Google's design from "
            "2017, keeps a separate array of control bytes, one per slot, in groups of sixteen. An empty slot is "
            "marked; a full one stores seven bits of its key's hash. <bookmark mark='b'/> Part of the hash picks a "
            "group; the other seven bits are compared against all sixteen control bytes in one instruction, giving a "
            "mask of the few slots worth checking. Usually there is one, and it is the key. <bookmark mark='c'/> "
            "We timed three tables with sixteen million slots. <bookmark mark='d'/> Half full, the open-addressing "
            "tables are close. Seven eighths full, linear probing's clusters grow long and it falls behind by more "
            "than two and a half times, while the Swiss table barely notices: its probes stay short and inside one "
            "cache line. <bookmark mark='e'/> The standard library's chained map pays for a pointer chase on every "
            "node, the linked list of the opening chapter again. Abseil, Rust's standard HashMap and Facebook's F14 "
            "all use this design."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(grp), FadeIn(gl), FadeIn(expl[0]))
            vo.wait_until("b")
            self.play(Create(hits), FadeIn(expl[1]), FadeIn(expl[2]))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3), FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
            vo.wait_until("e")
            self.play(FadeIn(notes[2]), FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()
