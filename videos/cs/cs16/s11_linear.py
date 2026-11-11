from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs16.common import (CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load, mono,
                                   value_bars, words)


class Linear(VoiceoverScene):
    def construct(self):
        self.card()
        self.counting()
        self.radix()
        self.timed()

    def card(self):
        card = chapter_card(10, r"Beating $n \log n$", r"What if we do more than compare?", lit=(1890,),
                            extra=((1890, r"Hollerith: \ punched-card tabulation"),), part=PART)
        with self.voiceover("Chapter ten. Beating n log n."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def counting(self):
        head = label(r"Sorting without comparing", font_size=34).to_edge(UP, buff=0.3)
        pts = VGroup(
            label(r"the lower bound is about \textit{comparisons}: \ an algorithm that reads the keys can escape it",
                  font_size=22, color=GREY_A),
            label(r"\textbf{counting sort}: \ keys in $0..k-1$: \ count each value, \ then write them out: \ $O(n + k)$",
                  font_size=22, color=YES),
            label(r"\textbf{radix sort}: \ counting sort on one digit at a time, \ least significant first, \ "
                  r"each pass stable", font_size=22, color=DATA),
            label(r"32-bit keys, \ 8-bit digits: \ 4 passes, \ $O(n)$ for fixed-width keys", font_size=22,
                  color=DATA),
            label(r"digit-by-digit organization was a physical operation in punched-card equipment",
                  font_size=20, color=GREY_B),
            label(r"on the word-RAM, \ $n$ integers sort in $O(n \sqrt{\log \log n})$ expected time \ (Han and "
                  r"Thorup, \ 2002); \ linear bounds require word-width/model conditions", font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.22).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            (
            "The comparison lower bound restricts which operations reveal information. <bookmark mark='a'/> "
            "Integer algorithms may inspect digits and index arrays instead. <bookmark mark='b'/> Counting sort "
            "handles keys from zero through k minus one in O of n plus k time, with O of k counters. <bookmark "
            "mark='c'/> Least-significant-digit radix sort applies a stable distribution pass to each digit. "
            "Order from earlier digits survives ties in later passes. <bookmark mark='d'/> For fixed "
            "thirty-two-bit keys and eight-bit digits, four passes suffice; the bound includes the digit "
            "counters. <bookmark mark='e'/> Punched-card equipment made digit-by-digit organization a physical "
            "operation, long before modern computers. <bookmark mark='f'/> For growing word widths, linear time "
            "is a different question. Historical word-RAM bounds depend on the instruction set, randomization and "
            "the relation between word width and input size."
        )
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcdef", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def radix(self):
        head = label(r"Radix sort, \ one digit at a time", font_size=34).to_edge(UP, buff=0.3)
        vals = [329, 457, 657, 839, 436, 720, 355]
        passes = [vals]
        for d in range(3):
            cur = passes[-1]
            passes.append(sorted(cur, key=lambda v: (v // 10 ** d) % 10))
        cols = VGroup()
        for k, ps in enumerate(passes):
            col = VGroup()
            for v in ps:
                t = MathTex(*list(str(v)), font_size=34)
                if k > 0:
                    t[3 - k].set_color(YES)
                col.add(t)
            col.arrange(DOWN, buff=0.18)
            cols.add(col)
        cols.arrange(RIGHT, buff=1.4).next_to(head, DOWN, buff=0.5)
        caps = VGroup(*[label(t, font_size=19, color=GREY_B).next_to(c, DOWN, buff=0.25) for t, c in zip(
            (r"input", r"by the units", r"by the tens", r"by the hundreds"), cols)])
        ars = VGroup(*[Arrow(cols[k].get_right(), cols[k + 1].get_left(), buff=0.15, color=GREY_B, stroke_width=2,
                             tip_length=0.14) for k in range(3)])
        note = label(r"each pass is a stable counting sort on one digit: \ ties keep the order of the previous pass",
                     font_size=21, color=HEAD).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            (
            "Watch seven three-digit keys pass through a textbook radix sort. <bookmark mark='a'/> The first "
            "stable pass orders the units. <bookmark mark='b'/> The second orders the tens, preserving units "
            "order among equal tens. <bookmark mark='c'/> The third orders the hundreds while preserving the "
            "lower two digits' order among ties. <bookmark mark='d'/> The final order is sorted. The invariant "
            "after each pass is order by the suffix of digits processed so far. That stability condition is "
            "essential; an arbitrary unstable digit sort would not establish it."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(cols[0]), FadeIn(caps[0]))
            for mk, k in zip("abc", range(1, 4)):
                vo.wait_until(mk)
                self.play(GrowArrow(ars[k - 1]), FadeIn(cols[k]), FadeIn(caps[k]))
            vo.wait_until("d")
            self.play(FadeIn(note))
        self.wait(0.3)
        self.clear_scene()

    def timed(self):
        d = load("linear")
        head = label(r"Timed on this machine", font_size=34).to_edge(UP, buff=0.3)
        rows = []
        for r in d["rows"]:
            rows.append([words(r["n"]), human_time(r["qsort"]), human_time(r["std_sort"]), human_time(r["radix"]),
                         human_time(r["counting"])])
        tab = grid_table([r"$n$ random 32-bit keys", r"C \texttt{qsort}", r"C++ \texttt{std::sort}",
                          r"radix, \ 4 passes", r"counting \ (16-bit keys)"], rows, widths=[3.2, 2.2, 2.6, 2.4, 2.8],
                         row_h=0.5, font_size=20,
                         colors=[[WHITE, NO, CTRL, YES, YES]] * len(rows)).next_to(head, DOWN, buff=0.5)
        protocol = VGroup(label(r"three runs per size, minimum shown; every result checked against a full sorted reference",font_size=18,color=GREY_B),
                          label(r"counting uses a separate 16-bit domain; input copies/checks excluded; counter allocation included",font_size=18,color=GREY_B),
                          label(d["gcc"]+r"; \ "+d["gxx"],font_size=16,color=GREY_B)).arrange(DOWN,buff=0.08).to_edge(DOWN,buff=0.32)
        if protocol.width>12.7:protocol.scale_to_fit_width(12.7)
        big = d["rows"][-1]
        pts = VGroup(
            label(rf"ten million keys: \ radix sort is {big['std_sort'] / big['radix']:.1f}$\times$ faster than "
                  rf"\texttt{{std::sort}}, \ and {big['qsort'] / big['radix']:.1f}$\times$ faster than "
                  r"\texttt{qsort}", font_size=21, color=YES),
            label(r"\texttt{qsort} pays a function call per comparison; \ \texttt{std::sort} inlines it", font_size=20,
                  color=GREY_A),
            label(r"this four-pass radix sort uses 32-bit keys and an extra array; \ compare general objects with a consistent ordering",
                  font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.14).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            (
            "These are checked host measurements, not a universal ranking. <bookmark mark='a'/> C qsort, C++ "
            "std::sort and our radix sort receive the same deterministic thirty-two-bit input. Each result is "
            "validated outside the timer against a full sorted reference. The separate counting-sort column masks "
            "that source to sixteen bits, so it solves a smaller-domain problem. <bookmark mark='b'/> Each "
            "displayed time is the minimum of three runs at that size. Input copies and reference checks are "
            "excluded; counting-sort counter allocation is included. Read the observed ratios from the table, "
            "with the compiler versions and protocol below. <bookmark mark='c'/> Key width, extra storage, cache "
            "state and implementation all affect the result. Comparison sorts remain useful for general ordered "
            "objects."
        )
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(protocol))
            vo.wait_until("b")
            self.play(FadeIn(pts[:2]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()
