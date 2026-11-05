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
                            extra=((1890, r"Hollerith's tabulator: \ radix sorting by machine"),), part=PART)
        with self.voiceover("Chapter ten. Beating n log n."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def counting(self):
        head = label(r"Sorting without comparing", font_size=34).to_edge(UP, buff=0.3)
        pts = VGroup(
            label(r"the lower bound is about \textit{comparisons}: \ an algorithm that reads the keys can escape it",
                  font_size=22, color=GREY_A),
            label(r"\textbf{counting sort}: \ keys in $0..k$: \ count each value, \ then write them out: \ $O(n + k)$",
                  font_size=22, color=YES),
            label(r"\textbf{radix sort}: \ counting sort on one digit at a time, \ least significant first, \ "
                  r"each pass stable", font_size=22, color=DATA),
            label(r"32-bit keys, \ 8-bit digits: \ 4 passes, \ $O(n)$ for fixed-width keys", font_size=22,
                  color=DATA),
            label(r"Hollerith's punched-card sorters did exactly this, \ a column at a time, \ for the 1890 census",
                  font_size=20, color=GREY_B),
            label(r"on the word-RAM, \ $n$ integers sort in $O(n \sqrt{\log \log n})$ expected time \ (Han and "
                  r"Thorup, \ 2002); \ $O(n)$ is open", font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.22).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "The lower bound has a condition hidden in its name: it is about comparisons. <bookmark mark='a'/> An "
            "algorithm that looks inside the keys can escape it. <bookmark mark='b'/> If the keys are small "
            "integers, counting sort counts how many times each value occurs and writes them back in order, in "
            "time proportional to n plus the range of values. <bookmark mark='c'/> Radix sort applies counting "
            "sort to one digit at a time, starting from the least significant, and because each pass is stable, "
            "the earlier passes' order survives within equal digits. <bookmark mark='d'/> Thirty-two-bit keys, "
            "eight bits at a time: four linear passes. <bookmark mark='e'/> Herman Hollerith's card sorters did "
            "this mechanically for the 1890 census, one column per pass. <bookmark mark='f'/> How fast can "
            "integers be sorted on a word-RAM in general? Han and Thorup reached n times the square root of log log "
            "n in 2002. Whether linear time is possible remains open."
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
            "Here is radix sort on seven three-digit numbers, the example from Hollerith's machines and from the "
            "standard textbook. <bookmark mark='a'/> First, sort by the units digit alone. <bookmark mark='b'/> "
            "Then by the tens digit, keeping the previous order among equal tens. <bookmark mark='c'/> Then by the "
            "hundreds. <bookmark mark='d'/> Now the list is sorted, though no two numbers were ever compared. The "
            "stability of each pass is what makes it work: when two numbers have the same hundreds digit, their "
            "order from the tens pass survives."
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
        big = d["rows"][-1]
        pts = VGroup(
            label(rf"ten million keys: \ radix sort is {big['std_sort'] / big['radix']:.1f}$\times$ faster than "
                  rf"\texttt{{std::sort}}, \ and {big['qsort'] / big['radix']:.1f}$\times$ faster than "
                  r"\texttt{qsort}", font_size=21, color=YES),
            label(r"\texttt{qsort} pays a function call per comparison; \ \texttt{std::sort} inlines it", font_size=20,
                  color=GREY_A),
            label(r"but radix sort needs fixed-width keys and an extra array: \ comparison sorts work on anything "
                  r"ordered", font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.14).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "How much does that buy? <bookmark mark='a'/> We sorted random thirty-two-bit integers in C on this "
            "machine, a hundred thousand, a million and ten million of them. <bookmark mark='b'/> For ten million, "
            "radix sort is several times faster than C++'s std::sort, and faster again than C's qsort, which pays a "
            "function call for every comparison. Counting sort on sixteen-bit keys is faster still. <bookmark "
            "mark='c'/> The price is generality. Radix sort needs keys made of fixed-width digits and a second "
            "array; a comparison sort works on anything that can be ordered, which is why it remains the default."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(pts[:2]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()
