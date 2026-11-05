from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs16.common import (CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load, mono,
                                   words)


class Amortized(VoiceoverScene):
    def construct(self):
        self.card()
        self.costs()
        self.counter()
        self.methods()
        self.factor()

    def card(self):
        card = chapter_card(13, r"Amortized analysis", r"Can an expensive step be cheap on average?", lit=(1985,),
                            extra=((1985, r"Tarjan: \ amortized complexity"),), part=PART)
        with self.voiceover("Chapter thirteen. Amortized analysis."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def costs(self):
        d = load("amortized")
        head = label(r"A growable array, \ doubling when full", font_size=34).to_edge(UP, buff=0.3)
        seq = d["seq"][:40]
        mx = max(s["cost"] for s in seq)
        ax = Axes(x_range=[0, 41, 8], y_range=[0, mx + 2, 8], x_length=10.0, y_length=3.6,
                  axis_config={"color": GREY_D, "include_numbers": False}).move_to(DOWN * 0.2)
        bars = VGroup()
        for s in seq:
            p0, p1 = ax.c2p(s["i"] - 0.4, 0), ax.c2p(s["i"] + 0.4, s["cost"])
            bars.add(Rectangle(width=p1[0] - p0[0], height=max(p1[1] - p0[1], 0.02), stroke_width=0,
                               fill_color=NO if s["cost"] > 1 else DATA, fill_opacity=0.85).move_to(
                [(p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, 0]))
        avg = DashedLine(ax.c2p(0, 3), ax.c2p(41, 3), color=YES, stroke_width=2)
        al = label(r"3 per append, \ on average, \ always", font_size=18, color=YES).next_to(
            ax.c2p(25, 3), UP, buff=0.08)
        xl = label(r"the $i$-th append", font_size=18, color=GREY_B).next_to(ax, DOWN, buff=0.15)
        yl = label(r"its cost: \ 1, \ or 1 plus copying everything", font_size=18, color=GREY_B).next_to(
            ax, UP, buff=0.1).align_to(ax, LEFT)
        with self.voiceover(
            "Java's ArrayList, C++'s vector and Python's list all grow geometrically. Take the simplest rule, "
            "doubling. <bookmark mark='a'/> Most appends cost one step. But when the array is full, it allocates "
            "one twice as big and copies everything across: an append that costs as much as all the elements so far. <bookmark mark='b'/> The "
            "worst single append is linear. Yet the expensive ones come at sizes one, two, four, eight, and the "
            "copies add up to less than two n. Averaged over any sequence of appends, the cost is at most three "
            "per append. That is an amortized bound: not an average over random inputs, but a guarantee for every "
            "sequence."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.04), run_time=3)
            vo.wait_until("b")
            self.play(Create(avg), FadeIn(al))
        self.wait(0.3)
        self.clear_scene()

    def counter(self):
        head = label(r"A second example: \ a binary counter", font_size=34).to_edge(UP, buff=0.3)
        xs = [0.0, 0.9, 2.9, 3.8]
        rows = VGroup()
        total = 0
        prev = 0
        for v in range(0, 17):
            flips = bin(prev ^ v).count("1") if v else 0
            total += flips
            bits = format(v, "05b")
            cells = [mono(f"{v:2d}", 16, GREY_B), MathTex(r"\;".join(bits), font_size=26),
                     mono(f"+{flips}" if v else "-", 16, NO if flips > 2 else GREY_A), mono(f"{total}", 16, YES)]
            r = VGroup()
            for x, c in zip(xs, cells):
                r.add(c.move_to([x, 0, 0], aligned_edge=LEFT))
            rows.add(r)
            prev = v
        for k, r in enumerate(rows):
            r.shift(DOWN * 0.3 * k)
        rows.next_to(head, DOWN, buff=0.75).to_edge(LEFT, buff=1.2)
        if rows.height > 5.6:
            rows.scale_to_fit_height(5.6).next_to(head, DOWN, buff=0.75).to_edge(LEFT, buff=1.2)
        hdr = VGroup(*[label(t, font_size=17, color=GREY_B) for t in ("count", "bits", "flips", "total")])
        for h_, c in zip(hdr, rows[0]):
            h_.next_to(c, UP, buff=0.15).align_to(c, LEFT)
        pts = VGroup(
            label(r"an increment flips the trailing ones, \ then one zero", font_size=22, color=GREY_A),
            label(r"the worst increment flips every bit", font_size=22, color=NO),
            label(r"but bit $k$ flips only every $2^k$ increments: \ total $< 2n$", font_size=22, color=YES),
            label(r"potential: \ the number of ones; \ amortized cost $\le 2$", font_size=22, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.6)
        with self.voiceover(
            "The second standard example is a binary counter. <bookmark mark='a'/> Adding one flips the trailing "
            "ones to zeros, and the next zero to one. <bookmark mark='b'/> Counting from fifteen to sixteen flips "
            "five bits; in general, the worst increment flips them all. <bookmark mark='c'/> But the lowest bit "
            "flips every time, the next every second time, the next every fourth. Over n increments the total is "
            "less than two n, and the running total in the last column never catches up with twice the count. "
            "<bookmark mark='d'/> As a potential argument: let the potential be the number of ones. An increment "
            "that flips t ones to zero and one zero to one costs t plus one and lowers the potential by t minus "
            "one, so its amortized cost is two."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr))
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.12), run_time=4)
            for mk, p in zip("abcd", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def methods(self):
        head = label(r"Three ways to prove it", font_size=34).to_edge(UP, buff=0.3)
        rows = VGroup(
            VGroup(label(r"\textbf{aggregate}", font_size=23, color=DATA),
                   label(r"total copies $\le 1 + 2 + 4 + \cdots + n < 2n$: \ divide by $n$", font_size=21,
                         color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(r"\textbf{accounting}", font_size=23, color=FUNC),
                   label(r"charge 3 per append: \ 1 to insert, \ 2 saved, \ to pay for copying itself and one older "
                         r"element later", font_size=21, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(r"\textbf{potential}", font_size=23, color=LAM),
                   MathTex(r"\Phi = 2\cdot\text{size} - \text{capacity} \ge 0, \qquad "
                           r"\text{amortized} = \text{actual} + \Delta\Phi \le 3", font_size=28)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.08),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(head, DOWN, buff=0.6)
        note = label(r"Tarjan \ (1985) \ named the method; \ Part 17's splay trees and union--find need it",
                     font_size=20, color=GREY_B).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "There are three standard ways to prove such a bound. <bookmark mark='a'/> Aggregate: add up the whole "
            "sequence. The copies are one plus two plus four, up to n, less than two n, so the total is under three "
            "n. <bookmark mark='b'/> Accounting: charge every append three units. One pays for inserting the "
            "element; two are saved, and when the array doubles, the saved units pay for copying. <bookmark "
            "mark='c'/> Potential: define a potential, two times the size minus the capacity, that rises with "
            "cheap appends and falls when the array doubles. Actual cost plus the change in potential is at most "
            "three, every time. <bookmark mark='d'/> Robert Tarjan made the method a standard tool in 1985, and the "
            "next part's splay trees and union–find depend on it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(note))
        self.wait(0.3)
        self.clear_scene()

    def factor(self):
        d = load("amortized")
        t, h = d["two"], d["one_half"]
        head = label(r"Why not double? \ The growth factor", font_size=34).to_edge(UP, buff=0.3)
        tab = grid_table([r"a million appends", r"growth $\times 2$", r"growth $\times 1.5$"], [
            [r"element copies per append", f"{t['per_append']:.2f}", f"{h['per_append']:.2f}"],
            [r"times the array grew", str(t["growths"]), str(h["growths"])],
            [r"times the new block fits in the space freed so far", str(t["could_reuse"]), str(h["could_reuse"])],
        ], widths=[6.6, 2.4, 2.4], row_h=0.5, font_size=20, mono_cols=(),
            colors=[[WHITE, YES, WHITE], [WHITE, WHITE, WHITE], [WHITE, NO, YES]]).next_to(head, DOWN, buff=0.5)
        pts = VGroup(
            label(r"with factor 2, \ each new block is larger than all the old ones put together: \ freed memory "
                  r"can never be reused", font_size=21, color=NO),
            label(rf"with any factor below the golden ratio, \ $\varphi = {d['golden']:.3f}$, \ it eventually can",
                  font_size=21, color=YES),
            label(r"Facebook's \texttt{folly::fbvector} and Microsoft's C++ library grow by 1.5; \ GCC's and Clang's "
                  r"by 2", font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.15).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "Any constant factor gives constant amortized cost. So why do some libraries grow by one and a half? "
            "<bookmark mark='a'/> We ran a million appends both ways. One and a half copies about twice as many "
            "elements, and grows more often. <bookmark mark='b'/> But look at the last row. With doubling, each new "
            "block is larger than all the blocks freed before it put together, so the allocator can never reuse "
            "them for the array. With a factor below the golden ratio, one point six one eight, the freed blocks "
            "eventually add up to enough, and memory is recycled. <bookmark mark='c'/> Facebook's fbvector and "
            "Microsoft's standard library chose one and a half; GCC and Clang chose two. A trade between time and "
            "memory, decided by a constant."
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
