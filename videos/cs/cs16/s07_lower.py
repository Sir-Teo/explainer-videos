from __future__ import annotations

import itertools

from explainer.cs import *  # noqa: F403
from videos.cs.cs16.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load,
                                   mono, words)


def insertion_tree():
    """Insertion sort on three symbolic keys a, b, c: the decision tree as nested (comparison, yes, no) or a leaf."""
    paths = {}
    for perm in itertools.permutations(range(3)):
        rank = dict(zip("abc", perm))
        a = ["a", "b", "c"]
        path = []
        for i in range(1, 3):
            x = a[i]
            j = i - 1
            while j >= 0:
                r = rank[x] < rank[a[j]]
                path.append((f"{x}<{a[j]}", r))
                if not r:
                    break
                a[j + 1] = a[j]
                j -= 1
            a[j + 1] = x
        paths[tuple(path)] = "".join(a)

    def build(prefix):
        nxt = {p[len(prefix)] for p in paths if p[:len(prefix)] == prefix and len(p) > len(prefix)}
        if not nxt:
            return paths[prefix]
        q = next(iter(nxt))[0]
        return (q, build(prefix + ((q, True),)), build(prefix + ((q, False),)))
    return build(())


class Lower(VoiceoverScene):
    def construct(self):
        self.card()
        self.tree()
        self.bound()
        self.small()
        self.adversary()

    def card(self):
        card = chapter_card(6, r"The comparison lower bound", r"Can any sort beat $n \log n$?", lit=(1959,),
                            extra=((1959, r"Ford and Johnson: \ merge insertion"),), part=PART)
        with self.voiceover("Chapter six. The comparison lower bound."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def tree(self):
        head = label(r"Every comparison sort is a tree", font_size=34).to_edge(UP, buff=0.3)
        t = insertion_tree()
        nodes, edges, leaves = VGroup(), VGroup(), VGroup()

        def place(t, x, y, dx):
            if isinstance(t, str):
                m = VGroup(RoundedRectangle(width=0.95, height=0.48, corner_radius=0.08, color=YES,
                                            stroke_width=2).set_fill(YES, 0.12), mono(t, 18, YES))
                m[1].move_to(m[0])
                m.move_to([x, y, 0])
                leaves.add(m)
                return m
            q, yes, no = t
            m = VGroup(Circle(radius=0.36, color=DATA, stroke_width=2).set_fill(BG, 1),
                       MathTex(q.replace("<", " < "), font_size=22, color=DATA))
            m[1].move_to(m[0])
            m.move_to([x, y, 0])
            nodes.add(m)
            for child, sx, lab in ((yes, -1, "yes"), (no, 1, "no")):
                cm = place(child, x + sx * dx, y - 1.25, dx / 2)
                e = Line(m.get_bottom(), cm.get_top(), color=GREY_B, stroke_width=1.6)
                edges.add(e, label(lab, font_size=15, color=GREY_B).move_to(e.get_center() + [sx * 0.28, 0.08, 0]))
            return m
        place(t, 0, 2.0, 3.0)
        tree = VGroup(edges, nodes, leaves).next_to(head, DOWN, buff=0.3)
        pts = VGroup(
            label(r"insertion sort on three keys $a, b, c$: \ each node a comparison, \ each leaf an order",
                  font_size=20, color=GREY_A),
            label(r"$3! = 6$ orders need 6 leaves; \ a binary tree of height $h$ has at most $2^h$ leaves", font_size=21,
                  color=YES),
            label(r"so the worst case needs $h \ge \lceil \lg 6 \rceil = 3$ comparisons", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "To prove that no sort can be faster, we need a picture of every possible sort. <bookmark mark='a'/> "
            "Run insertion sort on three keys, a, b and c. Its first move is to compare b with a. Depending on the "
            "answer it compares something else, and so on, until it knows the order. Draw every possible run as a "
            "tree: each node a comparison, each branch an outcome, each leaf the order the sort outputs. <bookmark "
            "mark='b'/> Every algorithm that sorts by comparing is such a tree, for each n. Since it must be able "
            "to output any of the three factorial, six, orders, it needs at least six leaves. A binary tree of "
            "height h has at most two to the h leaves. <bookmark mark='c'/> So some input forces at least the log "
            "of six, rounded up, three comparisons. No cleverness can avoid it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(nodes), Create(edges), run_time=2)
            self.play(LaggedStart(*[FadeIn(l) for l in leaves], lag_ratio=0.2), FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    def bound(self):
        d = load("lower")
        head = label(r"A bound from information", font_size=34).to_edge(UP, buff=0.3)
        eq = MathTex(r"h \;\ge\; \lg n! \;=\; n \lg n - n \lg e + O(\log n) \;\approx\; n \lg n - 1.44\, n",
                     font_size=36).next_to(head, DOWN, buff=0.5)
        rows = [[words(r["n"]), words(round(r["log2fact"])), words(round(r["nlgn"]))] for r in d["big"]
                if r["n"] >= 1000]
        tab = grid_table([r"$n$", r"$\lg n!$", r"$n \lg n$"], rows, widths=[2.4, 3.0, 3.0], row_h=0.48,
                         font_size=20).next_to(eq, DOWN, buff=0.45)
        pts = VGroup(
            label(r"each comparison has two outcomes: \ it yields at most one \textbf{bit}", font_size=22,
                  color=GREY_A),
            label(r"the input is one of $n!$ orders: \ $\lg n!$ bits are needed to say which \ "
                  r"(\textit{AI, Built}, \ Part 1)", font_size=22, color=GREY_A),
            label(r"so every comparison sort makes $\Omega(n \log n)$ comparisons, \ in the worst case \textit{and} on "
                  r"average over uniform distinct-key permutations", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            (
            "Now assume n distinct keys and a binary comparison model. <bookmark mark='a'/> A correct sort must "
            "distinguish n factorial input orders, requiring at least that many leaves. Its worst-case depth is "
            "at least log base two of n factorial. Stirling gives n log n minus about one point four four n, plus "
            "lower-order terms. <bookmark mark='b'/> Each binary answer supplies at most one bit of information. "
            "<bookmark mark='c'/> If all distinct-key permutations are equally likely, the average leaf depth is "
            "also at least log n factorial. The distribution matters: a promise that input is already sorted "
            "changes the average-case question. In this unrestricted comparison problem, merge sort and heapsort "
            "have optimal asymptotic worst-case growth."
        )
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq), FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(pts[:2]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    def adversary(self):
        head = label(r"Lower bounds by adversary: \ minimum and maximum", font_size=32).to_edge(UP, buff=0.3)
        pts = VGroup(
            label(r"finding the maximum alone: \ every other element must lose once: \ $n - 1$ comparisons, \ "
                  r"exactly", font_size=21, color=GREY_A),
            label(r"both at once, \ naively: \ $2n - 3$", font_size=21, color=GREY_A),
            label(r"better: \ compare in pairs ($n/2$), \ then the winners for the max and the losers for the min",
                  font_size=21, color=YES),
            MathTex(r"\lfloor n/2\rfloor+2(\lceil n/2\rceil-1)=\lceil3n/2\rceil-2\quad(n\ge1)",
                    font_size=34, color=YES),
            label(r"the adversary: \ answer each comparison to destroy as little ``uncertainty'' as possible; \ "
                  r"only untouched pairs need yield two new facts; \ at most $\lfloor n/2\rfloor$ such pairs", font_size=20, color=GREY_A),
            label(r"so $\lceil 3n/2 \rceil - 2$ is optimal \ (Pohl, \ 1972): \ problem 3", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.2).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            (
            "An adversary can also prove a lower bound. <bookmark mark='a'/> To find the maximum among distinct "
            "items, every other item must lose a comparison: n minus one are necessary and sufficient. <bookmark "
            "mark='b'/> Separate scans for minimum and maximum cost nearly twice n. <bookmark mark='c'/> Pair the "
            "items first. Search the winners for the maximum and the losers for the minimum; an unpaired item "
            "participates in both searches. <bookmark mark='d'/> The count is floor of n over two plus twice "
            "ceiling of n over two minus one: ceiling of three n over two minus two, valid for odd and even n. "
            "<bookmark mark='e'/> For the lower bound, all but the maximum must lose, and all but the minimum "
            "must win. Only comparisons between two untouched items need provide two new facts; the adversary can "
            "limit the others to one. At most floor of n over two comparisons join untouched pairs. <bookmark "
            "mark='f'/> Counting those facts yields the same bound. Problem three completes the proof."
        )
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcdef", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def small(self):
        d = load("lower")
        head = label(r"How close can we get? \ Merge insertion", font_size=34).to_edge(UP, buff=0.3)
        rows = []
        cols = []
        for r in d["rows"]:
            if r["n"] < 3:
                continue
            rows.append([str(r["n"]), str(r["bound"]), str(r["merge"]), str(r["binary"]), str(r["fj"]),
                         str(r["optimal"])])
            cols.append([WHITE, YES, WHITE, WHITE, DATA if r["fj"] == r["bound"] else NO, HEAD])
        tab = grid_table([r"$n$", r"$\lceil \lg n! \rceil$", r"merge sort", r"binary insertion",
                          r"merge insertion", r"best possible"], rows, widths=[1.0, 1.9, 1.9, 2.4, 2.4, 2.2],
                         row_h=0.38, font_size=18, colors=cols).next_to(head, DOWN, buff=0.35)
        pts = VGroup(
            label(r"worst-case comparisons; \ merge insertion checked by trying every order for $n \le 8$",
                  font_size=19, color=GREY_B),
            label(r"Ford and Johnson \ (1959): \ meets the bound for every $n \le 11$", font_size=21, color=DATA),
            label(r"at $n = 12$ the bound says 29, \ but 30 is the best possible \ (Wells, \ 1965, \ by exhaustive "
                  r"search)", font_size=21, color=NO),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "How close to the bound can a sort come, for small n? <bookmark mark='a'/> Here are the worst-case "
            "comparison counts for sorting three to twelve items. Merge sort and binary insertion fall behind the "
            "bound from five items on. <bookmark mark='b'/> Lester Ford and Selmer Johnson's merge insertion, from "
            "1959, pairs the items, sorts the winners, and inserts the losers in a carefully chosen order, so that "
            "each binary search runs on a chain of just under a power of two. It meets the information bound "
            "exactly for every n up to eleven. We checked our implementation's worst case by running it on every "
            "order for n up to eight. <bookmark mark='c'/> At twelve, the bound says twenty-nine, and merge "
            "insertion needs thirty. Mark Wells showed in 1965, by exhaustive search, that thirty is the best any "
            "algorithm can do. The bound is a floor, not always a door."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]), Indicate(VGroup(*tab.cells[-1]), color=NO))
        self.wait(0.3)
        self.clear_scene()
