from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs24.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)


class Bits(VoiceoverScene):
    def construct(self):
        self.card()
        self.tricks()
        self.submasks()
        self.russians()

    def card(self):
        card = chapter_card(7, r"Bits and the Four Russians", r"How many operations does one machine word do?",
                            lit=(1970,), extra=((1970, r"Arlazarov, Dinic, Kronrod, Faradzev"),), part=PART)
        with self.voiceover("Chapter seven. Bits, and the Four Russians."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def tricks(self):
        d = load("bits")
        head = label(r"A word is a set of 64 small things", font_size=32).to_edge(UP, buff=0.3)
        rows = [[str(r["i"]), r["bin"], str(r["pop"]), str(r["low"]), r["gray"]] for r in d["table"]]
        tab = grid_table([r"$i$", r"binary", r"popcount", r"$i \mathbin{\&} -i$", r"Gray code"], rows,
                         widths=[0.8, 1.4, 1.5, 1.6, 1.6], row_h=0.27, font_size=17, mono_cols=(1, 4),
                         colors=[[WHITE, DATA, YES, LAM, HEAD]] * len(rows))
        tab.next_to(head, DOWN, buff=0.35).to_edge(LEFT, buff=0.5)
        notes = VGroup(
            label('\\textbf{popcount}: hardware support depends on the target ISA; \\\\ $x\\mathbin{\\&}(x-1)$ clears the lowest set bit', font_size=21, color=YES),
            label(r"\textbf{lowest set bit}: \ $x \mathbin{\&} -x$ \ (chapter 2's Fenwick tree)", font_size=21,
                  color=LAM),
            label(r"\textbf{Gray code}: \ $i \oplus (i \gg 1)$; \\ neighbours differ in one bit \ (rotary encoders, \ Karnaugh maps)",
                  font_size=21, color=HEAD),
            label(r"sets as words: \ union $|$, \ intersection $\&$, \\ membership by one shift", font_size=21,
                  color=DATA),
            label(r"Warren's \textit{Hacker's Delight}: \ the catalogue", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).next_to(tab, RIGHT, buff=0.5).align_to(tab, UP)
        room = 7.0 - notes.get_left()[0]
        if notes.width > room:
            notes.width = room
        with self.voiceover(
            "A sixty-four-bit machine word can represent a set of sixty-four positions. <bookmark mark='a'/> "
            'Population count may use a hardware instruction when the target ISA supports it. Clearing the '
            "lowest set bit visits the members one at a time. <bookmark mark='b'/> Isolating that bit gives the "
            "Fenwick step. <bookmark mark='c'/> Exclusive-or with a one-bit right shift gives a Gray-code "
            "sequence, whose neighbours differ in one bit. <bookmark mark='d'/> Fixed-width set union and "
            'intersection use a bounded number of word operations. A Python integer can span many machine words, '
            'so its bit-operation cost grows with its stored length. Negative patterns are excluded from these '
            "finite-subset routines. <bookmark mark='e'/> Warren's Hacker's Delight collects such "
            'transformations; check width, signedness and instruction support before translating one to native '
            'code.'
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.05))
            for mk, n_ in zip("abcde", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def submasks(self):
        d = load("bits")
        head = label(r"Enumerating submasks: \ $3^n$, \ not $4^n$", font_size=32).to_edge(UP, buff=0.35)
        code_ = VGroup(*[mono(t, 22, c) for t, c in (("for (s = m; ; s = (s - 1) & m) {", DATA),
                                                      ("    visit(s);", WHITE),
                                                      ("    if (s == 0) break;", WHITE),
                                                      ("}", DATA))]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        code_.next_to(head, DOWN, buff=0.5)
        rows = [[str(r["n"]), words(r["pairs"]), words(r["three"]), words(r["naive"])] for r in d["submasks"]]
        tab = grid_table([r"$n$", r"(mask, submask) pairs visited", r"$3^n$", r"all pairs, \ $4^n$"], rows,
                         widths=[0.8, 4.4, 2.0, 2.4], row_h=0.38, font_size=20, mono_cols=(),
                         colors=[[WHITE, YES, YES, NO]] * len(rows))
        tab.next_to(code_, DOWN, buff=0.4).set_x(0)
        notes = VGroup(
            label(r"subtracting one, \ then masking, \ steps to the next smaller submask: \ every one, \ in order",
                  font_size=21, color=WHITE),
            label(r"over all masks: \ each element is out, \ in the mask only, \ or in both: \ $3^n$ pairs", font_size=21,
                  color=YES),
            label(r"the engine of DP over subsets: \ set partitions, \ scheduling, \ Steiner trees", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.2).next_to(tab, DOWN, buff=0.35)
        with self.voiceover(
            "Some dynamic programs run over every subset of a set, and need every subset of each subset. <bookmark "
            "mark='a'/> These three lines visit every submask of m, from m itself down to zero: subtract one, which "
            "borrows through the lowest member, and mask, which throws away what is not in m. <bookmark mark='b'/> "
            "Over all masks of n elements the loop body runs three to the n times, not four to the n, because each "
            "element is either outside the mask, in the mask but not the submask, or in both. We counted: exactly "
            "three to the n, every time. <bookmark mark='c'/> That is the inner loop of dynamic programming over "
            "subsets, for partitions, schedules and Steiner trees."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code_))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.2), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    def russians(self):
        d = load("bits")
        head = label(r"Word-level parallelism: \ the Four Russians", font_size=32).to_edge(UP, buff=0.35)
        rows = []
        for r in d["rows"]:
            rows.append([rf"closure, \ $n = {words(r['n'])}$", f"{r['closure_plain'] * 1000:.1f} ms",
                         f"{r['closure_bits'] * 1000:.1f} ms", f"{r['closure_plain'] / r['closure_bits']:.0f}$\\times$"])
        for r in d["rows"]:
            rows.append([rf"LCS, \ two strings of {words(r['m'])}", f"{r['lcs_dp'] * 1000:.0f} ms",
                         f"{r['lcs_bits'] * 1000:.1f} ms", f"{r['lcs_dp'] / r['lcs_bits']:.0f}$\\times$"])
        tab = grid_table([r"", r"one element at a time", r"64 per word", r"speedup"], rows,
                         widths=[4.6, 3.2, 2.4, 1.6], row_h=0.44, font_size=21, mono_cols=(),
                         colors=[[WHITE, NO, YES, HEAD]] * len(rows))
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        notes = VGroup(
            label(r"Arlazarov, \ Dinic, \ Kronrod and Faradzev (1970): \ process $\log n$ bits at once, \ by table or "
                  r"by word: \ $O(n^3 / \log n)$", font_size=21, color=WHITE),
            label(r"closure: \ Warshall's loop with each row a bitset; \ reachability for every pair \ (the answers "
                  r"agree)", font_size=21, color=LAM),
            label(r"LCS: \ one DP row per word operation, \ $V \leftarrow (V + (V \mathbin{\&} M)) \mid (V "
                  r"\mathbin{\&} \lnot M)$ \ (Allison and Dix; \ Hyyr\"o)", font_size=21, color=YES),
            label(r"the same trick powers \texttt{diff}, \ DNA aligners, \ and the bit-parallel matcher inside "
                  r"\texttt{agrep}", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.22).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            'Word packing is related to the Four Russians tradition, but the mechanisms should be distinguished. '
            "<bookmark mark='a'/> The historical method groups small subproblems and precomputes their possible "
            'answers. Our experiments below use direct word-parallel operations rather than implementing that '
            "complete table-based algorithm. <bookmark mark='b'/> Packed transitive closure processes sixty-four "
            'columns per stored word. Every reachability result is checked against independent breadth-first '
            "searches. <bookmark mark='c'/> The LCS experiment compares full dynamic programming with a "
            'multiword bit algorithm on the same generated strings. Carry propagation spans all words of a row; '
            'the measured ratios are in the table. Both programs run three times and retain their raw clocks. '
            "<bookmark mark='d'/> Packing can improve constants and word-operation counts, while storage, "
            'preprocessing and multiword work remain part of the cost model.'
        ) as vo:
            self.play(FadeIn(head), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:3]], lag_ratio=0.3), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[3:5]], lag_ratio=0.3), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()
