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
            "The isolated tokenizer finds ASCII words and lower-cases letters. <bookmark mark='a'/> On this "
            'AVX2-capable host it loads thirty-two bytes, combines case bits, subtracts the code for a, and '
            "compares the lanes. Several vector instructions implement that sequence. <bookmark mark='b'/> "
            "Movemask gathers the lane results into an integer mask. <bookmark mark='c'/> A word begins where a "
            'letter has a non-letter predecessor; the mask carries boundary state between vector blocks. '
            "<bookmark mark='d'/> The table reports scalar and vector timings on the complete corpus. After each "
            'trial, we check every transformed byte and every word-start mask, as well as total words and '
            "letters. <bookmark mark='e'/> The simdjson work illustrates related classification techniques. An "
            "isolated tokenizer's timing is not a measured phase fraction of the complete word-count program."
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
            label(r"prefix iterations are dependent; \ this timer also includes an array copy \\ the build comparison changes several optimizations", font_size=21, color=NO),
            label(r"write simple loops over arrays, \ and read the compiler's report \ (\texttt{-fopt-info-vec})",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.22).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "Compilers can vectorize some loops automatically. <bookmark mark='a'/> We compile the same three "
            'kernels at O one and at O three with the native ISA enabled. The table gives measured costs per '
            "element, amortized over fixed loop counts; the disassembly is retained. <bookmark mark='b'/> "
            'Restrict promises the relevant pointer regions do not overlap. It is a contract the caller must '
            "obey, rather than a request that makes arbitrary aliasing safe. <bookmark mark='c'/> The prefix "
            'kernel carries a dependency; an ordinary scalar loop is not the parallel scan shown earlier. Every '
            "final array element and reduction is checked outside the timers. <bookmark mark='d'/> These builds "
            'change several optimizations together. Inspect the actual assembly to identify vector instructions, '
            'and avoid attributing the entire timing difference to vectorization alone.'
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
        tab = grid_table([r"OA cap $2^{24}$, \ ns per operation", r"find, \ request $\tfrac12$", r"find, \ request $\tfrac78$",
                          r"insert, \ request $\tfrac78$"], rows, widths=[5.0, 2.2, 2.2, 2.4], row_h=0.46, font_size=21,
                         mono_cols=(), colors=[[GREY_A] * 4, [NO] * 4, [YES] * 4])
        tab.next_to(grp, DOWN, buff=0.8).set_x(0)
        notes = VGroup(
            label('half the probes reuse inserted keys; half are random; every answer checked', font_size=20,
                  color=GREY_A),
            label('load requests apply to OA tables; unordered map has its own bucket count', font_size=21, color=YES),
            label('teaching SSE2 groups and this GCC chained map; no hardware-miss counters', font_size=21,
                  color=NO),
            label(r"Google's Abseil (2017), \ Rust's \texttt{HashMap}, \ Facebook's F14: \ all this design", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.18).next_to(tab, DOWN, buff=0.35)
        with self.voiceover(
            "Vector comparisons also help hash-table lookup. <bookmark mark='a'/> Our teaching Swiss-style table "
            'stores sixteen control bytes per group, each carrying an empty marker or seven hash bits. <bookmark '
            "mark='b'/> An SSE2 comparison filters candidate slots, followed by full key checks. Group probing "
            "and collisions still require work. <bookmark mark='c'/> The two open-addressing tables use the same "
            'requested capacity and occupancies. The standard unordered map chooses its own bucket count, which '
            "is recorded separately. Its occupancy is not automatically seven eighths. <bookmark mark='d'/> Read "
            'insertion and lookup times for each workload. Every inserted-key count and every lookup is checked '
            "against an independently sorted multiset after timing. <bookmark mark='e'/> Production Abseil and "
            'other modern tables develop related ideas with additional policies and guarantees; this small '
            'implementation does not reproduce every production design.'
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
