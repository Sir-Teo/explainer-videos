from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs47.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, mono, tag_box


def finger(color=HEAD):
    return Triangle(color=color, fill_color=color, fill_opacity=1, stroke_width=0).scale(0.11)


def lit(box, color=YES):
    """Recolour a boxed id (frame and number) without filling the box."""
    return [box[0].animate.set_stroke(color, width=3), box[1].animate.set_color(color)]


def counter(c, color=HEAD, text=r"comparisons"):
    return label(rf"{text}: \ {c}", font_size=22, color=color)


def merge_events(a, b):
    """The linear merge of explainer/cs/search/index.py (merge), step by step: (kind, i, j, comparisons)."""
    i = j = c = 0
    ev = []
    while i < len(a) and j < len(b):
        c += 1
        if a[i] == b[j]:
            ev.append(("hit", i, j, c))
            i, j = i + 1, j + 1
        elif a[i] < b[j]:
            ev.append(("a", i, j, c))
            i += 1
        else:
            ev.append(("b", i, j, c))
            j += 1
    return ev


def skip_events(a, b):
    """The skip-pointer merge of explainer/cs/search/index.py (skips), step by step."""
    sa, sb = max(1, int(math.sqrt(len(a)))), max(1, int(math.sqrt(len(b))))
    i = j = c = 0
    ev = []
    while i < len(a) and j < len(b):
        c += 1
        ev.append(("cmp", i, j, c))
        if a[i] == b[j]:
            ev.append(("hit", i, j, c))
            i, j = i + 1, j + 1
        elif a[i] < b[j]:
            if i % sa == 0 and i + sa < len(a):
                c += 1
                if a[i + sa] <= b[j]:
                    ev.append(("jump", i, i + sa, c))
                    i += sa
                    continue
                ev.append(("nojump", i, i + sa, c))
            ev.append(("a", i, i + 1, c))
            i += 1
        else:
            if j % sb == 0 and j + sb < len(b):
                c += 1
                if b[j + sb] <= a[i]:
                    ev.append(("bjump", j, j + sb, c))
                    j += sb
                    continue
            ev.append(("b", j, j + 1, c))
            j += 1
    return ev, c


class Boolean(VoiceoverScene):
    def construct(self):
        self.card()
        self.merge()
        self.skips()
        self.gallop()
        self.compare()
        self.phrases()

    def card(self):
        card = chapter_card(3, r"Merging postings", r"Which passages contain all the words?", lit=(1976, 2000),
                            extra=((1976, r"Bentley and Yao: \ unbounded search"),
                                   (1996, r"Moffat and Zobel: \ skips in postings"),
                                   (2000, r"Demaine, \ L\'opez-Ortiz and Munro: \ adaptive intersection")),
                            part=PART)
        with self.voiceover("Chapter three. Merging postings."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def merge(self):
        head = label(r"AND is a merge", font_size=36).to_edge(UP, buff=0.3)
        A, B = [2, 5, 8, 13, 21, 34, 40, 55], [3, 8, 21, 22, 40, 61]
        ra = VGroup(*[tag_box(str(v), color=DATA, size=20, w=0.8, h=0.5) for v in A]).arrange(RIGHT, buff=0.18)
        ra.move_to([-0.7, 1.75, 0])
        rb = VGroup(*[tag_box(str(v), color=LAM, size=20, w=0.8, h=0.5) for v in B]).arrange(RIGHT, buff=0.18)
        rb.move_to([0, 0.55, 0]).align_to(ra, LEFT)
        na = mono("whale", size=19, color=DATA).next_to(ra, LEFT, buff=0.35)
        nb = mono("sea", size=19, color=LAM).next_to(rb, LEFT, buff=0.35).align_to(na, RIGHT)
        nr = label(r"both:", font_size=21, color=YES).move_to([0, -0.65, 0]).align_to(na, RIGHT)
        illus = note(r"illustrative passage ids", font_size=16).next_to(rb, DOWN, buff=0.4).align_to(rb, LEFT)
        illus.shift(DOWN * 0.02)
        fa, fb = finger(), finger()
        fa.next_to(ra[0], DOWN, buff=0.06)
        fb.next_to(rb[0], DOWN, buff=0.06)
        cnt = counter(0).move_to([5.2, 1.15, 0])
        ev = merge_events(A, B)
        hits = [A[i] for k, i, _, _ in ev if k == "hit"]
        res = VGroup(*[tag_box(str(v), color=YES, size=20, w=0.8, h=0.5) for v in hits]).arrange(RIGHT, buff=0.18)
        res.move_to([0, -0.65, 0]).next_to(nr, RIGHT, buff=0.35)
        bound = label(rf"{ev[-1][3]} comparisons, \ at most {len(A)} + {len(B)} = {len(A) + len(B)}", font_size=21,
                      color=HEAD).next_to(nr, DOWN, buff=0.5).align_to(nr, LEFT)
        notes = VGroup(
            wrapped_label(r"compare the two fingers: \ equal, \ an answer, \ move both; \ otherwise move the smaller",
                          12.4, font_size=20, color=WHITE),
            wrapped_label(r"each comparison moves at least one finger: \ at most $m + n$ comparisons for lists of "
                          r"$m$ and $n$", 12.4, font_size=20, color=HEAD),
            wrapped_label(r"the same walk gives OR \ (keep everything) \ and AND NOT; \ for several terms, \ start "
                          r"with the shortest lists, \ since an intersection only shrinks", 12.4, font_size=20,
                          color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(bound, DOWN, buff=0.55).set_x(0)
        with self.voiceover(
            "A query for whale and sea wants the passages on both postings lists. <bookmark mark='a'/> Because both "
            "lists are sorted, one walk finds them. Keep a finger on each list and compare the two numbers. If they "
            "are equal, that passage is an answer, and both fingers move on; if not, the finger on the smaller "
            "number moves. <bookmark mark='b'/> Every comparison moves at least one finger, so the walk costs at "
            "most the sum of the two lengths. <bookmark mark='c'/> The same walk computes OR, keeping everything it "
            "passes, and AND NOT. With more than two terms, begin with the shortest lists, because an intersection "
            "can only shrink."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ra), FadeIn(rb), FadeIn(na), FadeIn(nb), FadeIn(illus))
            vo.wait_until("a")
            self.play(FadeIn(fa), FadeIn(fb), FadeIn(cnt), FadeIn(nr), FadeIn(notes[0]))
            got = 0
            for kind, i, j, c in ev:
                self.play(ra[i][0].animate.set_stroke(HEAD, width=4), rb[j][0].animate.set_stroke(HEAD, width=4),
                          Transform(cnt, counter(c).move_to(cnt)), run_time=0.35)
                moves = []
                if kind == "hit":
                    self.play(*lit(ra[i]), *lit(rb[j]),
                              TransformFromCopy(ra[i], res[got]), run_time=0.5)
                    got += 1
                if kind in ("hit", "a"):
                    if i + 1 < len(A):
                        moves.append(fa.animate.next_to(ra[i + 1], DOWN, buff=0.06))
                    else:
                        moves.append(FadeOut(fa))
                    if kind == "a":
                        moves.append(ra[i][0].animate.set_stroke(GREY_D, width=1.6))
                if kind in ("hit", "b"):
                    if j + 1 < len(B):
                        moves.append(fb.animate.next_to(rb[j + 1], DOWN, buff=0.06))
                    else:
                        moves.append(FadeOut(fb))
                    if kind == "b":
                        moves.append(rb[j][0].animate.set_stroke(GREY_D, width=1.6))
                self.play(*moves, run_time=0.35)
            vo.wait_until("b")
            self.play(FadeIn(bound), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def skips(self):
        rows = {tuple(r["terms"]): r for r in load("intersect")["rows"]}
        tw = rows[("the", "whale")]
        head = label(r"Skip pointers", font_size=36).to_edge(UP, buff=0.3)
        L = [3, 5, 9, 12, 16, 20, 23, 27, 31, 36, 40, 44, 48, 53, 57, 62]
        S = [44, 60]
        rl = VGroup(*[tag_box(str(v), color=DATA, size=18, w=0.62, h=0.46) for v in L]).arrange(RIGHT, buff=0.12)
        rl.move_to([0.3, 0.75, 0])
        rs = VGroup(*[tag_box(str(v), color=LAM, size=18, w=0.62, h=0.46) for v in S]).arrange(RIGHT, buff=0.12)
        rs.move_to([0, -0.55, 0]).align_to(rl, LEFT)
        nl = label(r"long", font_size=19, color=DATA).next_to(rl, LEFT, buff=0.2)
        ns = label(r"short", font_size=19, color=LAM).next_to(rs, LEFT, buff=0.2).align_to(nl, RIGHT)
        sa = int(math.sqrt(len(L)))
        arcs = {}
        for i in range(0, len(L) - sa, sa):
            arcs[i] = CurvedArrow(rl[i].get_top() + UP * 0.05, rl[i + sa].get_top() + UP * 0.05, angle=-PI / 2.2,
                                  color=GREY_B, stroke_width=2, tip_length=0.15)
        illus = note(r"illustrative: \ 16 postings, \ a skip every $\sqrt{16} = 4$", font_size=16).next_to(
            rs, RIGHT, buff=0.6)
        fa, fb = finger(), finger()
        fa.next_to(rl[0], DOWN, buff=0.06)
        fb.next_to(rs[0], DOWN, buff=0.06)
        ev, total = skip_events(L, S)
        plain = merge_events(L, S)[-1][3]
        cnt = counter(0).move_to([4.3, -1.15, 0])
        cmp_plain = label(rf"without skips: \ {plain}", font_size=20, color=GREY_A).next_to(cnt, DOWN, buff=0.15)
        notes = VGroup(
            wrapped_label(r"every $\sqrt{n}$-th posting points $\sqrt{n}$ ahead; \ jump if the target is still no "
                          r"larger than the other list's current id", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"$\sqrt{n}$ balances them: \ more skips cost space and checks, \ longer ones overshoot "
                          r"more often \ (Moffat and Zobel, \ 1996)", 12.4, font_size=20, color=HEAD),
            wrapped_label(rf"\texttt{{the}} AND \texttt{{whale}}, \ {tw['sizes'][0]:,} and {tw['sizes'][1]:,} "
                          rf"postings: \ merge {tw['merge']:,} comparisons, \ with skips {tw['skips']:,}", 12.4,
                          font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "When one list is much longer than the other, most of the walk along it is wasted. "
            "<bookmark mark='a'/> So add shortcuts. In a list of n postings, every square-root-of-n-th posting also "
            "points square root of n places ahead. Before stepping, check the shortcut: if its target is still no "
            "larger than the other list's current passage, jump. <bookmark mark='b'/> The square root balances the "
            "costs: more shortcuts take more space and more checks, and longer ones overshoot more often. Alistair "
            "Moffat and Justin Zobel studied skips in compressed postings in 1996. <bookmark mark='c'/> On the "
            "novels, the AND whale drops from eleven thousand one hundred and thirty-seven comparisons to one "
            "thousand seven hundred and ninety."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rl), FadeIn(rs), FadeIn(nl), FadeIn(ns), FadeIn(illus))
            vo.wait_until("a")
            self.play(*[Create(a) for a in arcs.values()], FadeIn(fa), FadeIn(fb), FadeIn(cnt), FadeIn(notes[0]))
            for kind, x, y, c in ev:
                if kind == "cmp":
                    self.play(rl[x][0].animate.set_stroke(HEAD, width=4), rs[y][0].animate.set_stroke(HEAD, width=4),
                              Transform(cnt, counter(c).move_to(cnt)), run_time=0.3)
                elif kind == "hit":
                    self.play(*lit(rl[x]), *lit(rs[y]), run_time=0.4)
                    anims = [FadeOut(fb)] if y + 1 >= len(S) else [fb.animate.next_to(rs[y + 1], DOWN, buff=0.06)]
                    if x + 1 < len(L):
                        anims.append(fa.animate.next_to(rl[x + 1], DOWN, buff=0.06))
                    self.play(*anims, run_time=0.3)
                elif kind == "jump":
                    self.play(arcs[x].animate.set_color(YES), Transform(cnt, counter(c).move_to(cnt)), run_time=0.3)
                    self.play(fa.animate.next_to(rl[y], DOWN, buff=0.06), rl[x][0].animate.set_stroke(GREY_D, 1.6),
                              *[rl[k].animate.set_opacity(0.3) for k in range(x + 1, y)], run_time=0.5)
                elif kind == "nojump":
                    self.play(arcs[x].animate.set_color(NO), Transform(cnt, counter(c).move_to(cnt)), run_time=0.3)
                elif kind == "a":
                    anims = [rl[x][0].animate.set_stroke(GREY_D, width=1.6)]
                    if y < len(L):
                        anims.append(fa.animate.next_to(rl[y], DOWN, buff=0.06))
                    self.play(*anims, run_time=0.3)
                elif kind in ("b", "bjump"):
                    nxt = fb.animate.next_to(rs[y], DOWN, buff=0.06) if y < len(S) else FadeOut(fb)
                    self.play(rs[x][0].animate.set_stroke(GREY_D, width=1.6), nxt, run_time=0.3)
            self.play(FadeIn(cmp_plain))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def gallop(self):
        rows = {tuple(r["terms"]): r for r in load("intersect")["rows"]}
        tw, lm = rows[("the", "whale")], rows[("love", "marriag")]
        head = label(r"Galloping", font_size=36).to_edge(UP, buff=0.3)
        vals = [2, 5, 7, 11, 14, 18, 19, 23, 26, 30, 33, 35, 38, 41, 45, 47, 50, 54, 57, 59, 62, 66, 69, 71, 75, 78,
                80, 83, 87, 90, 92, 96]
        x = 66
        cw = 0.4
        cells = VGroup()
        for k, v in enumerate(vals):
            r = Rectangle(width=cw, height=0.62, stroke_color=GREY_C, stroke_width=1.2, fill_color=BG, fill_opacity=1)
            r.move_to([-6.4 + cw / 2 + k * cw, 0.75, 0])
            cells.add(VGroup(r, mono(str(v), size=18, color=DATA).move_to(r)))
        start = label(r"last match", font_size=17, color=GREY_A).next_to(cells[0], DOWN, buff=0.15).align_to(
            cells[0], LEFT)
        tgt = label(rf"next id of the short list: \ {x}", font_size=21, color=LAM).move_to([0, 2.7, 0]).align_to(
            cells, LEFT)
        illus = note(r"illustrative", font_size=16).next_to(tgt, RIGHT, buff=0.4)
        probes, p, step = [], 0, 1
        while True:                                   # doubling probes from the last match
            q = min(p + step, len(vals) - 1)
            probes.append((q, step))
            if vals[q] >= x or q == len(vals) - 1:
                break
            step *= 2
        lo, hi = probes[-2][0] + 1, probes[-1][0]
        brackets = [(lo, hi)]
        bin_probes = []
        while lo < hi:
            m = (lo + hi) // 2
            bin_probes.append(m)
            if vals[m] < x:
                lo = m + 1
            else:
                hi = m
            brackets.append((lo, hi))

        def bracket(a, b):
            return SurroundingRectangle(VGroup(*cells[a:b + 1]), color=LAM, buff=0.05, stroke_width=3)
        arrows = VGroup()
        for q, s in probes:
            top = cells[q].get_top()
            arr = Arrow(top + UP * 0.85, top + UP * 0.05, buff=0, stroke_width=2.5, color=HEAD,
                        max_tip_length_to_length_ratio=0.25)
            t = label(rf"+{s}" if q < len(vals) - 1 or vals[q] < x else r"end", font_size=16, color=HEAD)
            t.next_to(arr, UP, buff=0.05)
            arrows.add(VGroup(arr, t))
        n_cmp = len(probes) + len(bin_probes) + 1
        found = label(rf"found after {n_cmp} comparisons; \ stepping one place at a time takes "
                      rf"{brackets[-1][0] + 1}", font_size=21, color=YES).next_to(cells, DOWN, buff=0.55).align_to(
            cells, LEFT)
        notes = VGroup(
            wrapped_label(r"then binary search the last gap \ (Bentley and Yao, \ 1976; \ Part 24)", 12.4,
                          font_size=20, color=LAM),
            wrapped_label(r"$m$ lookups in a list of $n$: \ about $m \log_2(n/m)$ comparisons, \ against $m + n$ for "
                          r"the walk", 12.4, font_size=20, color=WHITE),
            wrapped_label(rf"\texttt{{the}} AND \texttt{{whale}}: \ {tw['gallop']:,} comparisons \ (merge "
                          rf"{tw['merge']:,}); \ \texttt{{love}} AND \texttt{{marriag}}: \ {lm['gallop']:,} \ (merge "
                          rf"{lm['merge']:,})", 12.4, font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(found, DOWN, buff=0.6).set_x(0)
        with self.voiceover(
            "Galloping, from Part 24, goes further. <bookmark mark='a'/> Take each passage of the short list in "
            "turn and look for it in the long list: probe one place ahead, then two, four, eight and sixteen, "
            "doubling until a probe overshoots. <bookmark mark='b'/> Then binary search the last gap. Jon Bentley "
            "and Andrew Yao described this unbounded search in 1976. <bookmark mark='c'/> Finding m items in a list "
            "of n this way costs about m times the logarithm of n over m, far less than the walk when m is small. "
            "The AND whale now takes one thousand four hundred and eighteen comparisons, and love AND marriage one "
            "thousand nine hundred and fifteen, against two thousand six hundred and eighty for the merge."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells), FadeIn(start), FadeIn(tgt), FadeIn(illus))
            vo.wait_until("a")
            for (q, _), a in zip(probes, arrows):
                self.play(GrowArrow(a[0]), FadeIn(a[1]), cells[q][0].animate.set_stroke(HEAD, width=3), run_time=0.5)
            vo.wait_until("b")
            br = bracket(*brackets[0])
            self.play(Create(br), FadeIn(notes[0]))
            for m, (a, b) in zip(bin_probes, brackets[1:]):
                self.play(Indicate(cells[m], color=LAM, scale_factor=1.15), run_time=0.45)
                self.play(Transform(br, bracket(a, b)), run_time=0.45)
            self.play(cells[brackets[-1][0]][1].animate.set_color(YES), FadeIn(found))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def compare(self):
        rows = load("intersect")["rows"]
        head = label(r"Which intersection wins?", font_size=36).to_edge(UP, buff=0.3)
        algs = ("merge", "skips", "gallop")
        body = []
        for r in rows:
            a, b = r["terms"]
            m, n = r["sizes"]
            body.append([rf"\texttt{{{a}}} AND \texttt{{{b}}}", rf"{m:,}, \ {n:,}", f"{max(m, n) / min(m, n):.1f}",
                         f"{r['hits']:,}"] + [f"{r[k]:,}" for k in algs])
        tab = grid_table([r"query \ (stems)", r"lengths", r"ratio", r"in both", r"merge", r"skips", r"galloping"],
                         body, widths=[3.6, 2.2, 1.2, 1.4, 1.5, 1.5, 1.8], row_h=0.52, font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        for i, r in enumerate(rows, 1):
            best = min(algs, key=lambda k: r[k])
            worst = max(algs, key=lambda k: r[k])
            tab.cells[i][4 + algs.index(best)].set_color(YES)
            tab.cells[i][4 + algs.index(worst)].set_color(NO)
        src = note(r"comparisons counted by our instruments; \ best in green, \ worst in red", font_size=17).next_to(
            tab, DOWN, buff=0.2).align_to(tab, LEFT)
        tw = next(r for r in rows if r["terms"] == ["the", "whale"])
        big_r = sorted(max(r["sizes"]) / min(r["sizes"]) for r in rows if max(r["sizes"]) / min(r["sizes"]) >= 3)
        notes = VGroup(
            wrapped_label(r"lists of similar length \ (ratio under 3): \ the merge or skips win, \ and galloping "
                          r"wastes its probes", 12.4, font_size=20, color=WHITE),
            wrapped_label(rf"one list {' or '.join(f'{q:.0f}' for q in big_r)} times longer: \ galloping wins, \ "
                          rf"{tw['merge'] / tw['gallop']:.1f} times fewer comparisons than the merge for "
                          rf"\texttt{{the}} AND \texttt{{whale}}", 12.4, font_size=20, color=YES),
            wrapped_label(r"engines choose by the ratio, \ or use adaptive algorithms \ (Demaine, \ L\'opez-Ortiz and "
                          r"Munro, \ 2000); \ branch-free and SIMD loops \ (Part 24) \ cut the cost of each "
                          r"comparison", 12.4, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(src, DOWN, buff=0.4).align_to(tab, LEFT)
        with self.voiceover(
            "Here are all three on five queries over the novels. "
            "<bookmark mark='a'/> When the two lists are of similar length, like whale and sea, or Elizabeth and "
            "Darcy, the merge or skips win, and galloping wastes its probes. <bookmark mark='b'/> When one list is "
            "five or twenty-nine times longer, galloping wins, nearly eight times over for the AND whale. "
            "<bookmark mark='c'/> So engines choose by the ratio of the lengths, or use adaptive algorithms, like "
            "those of Erik Demaine, Alejandro López-Ortiz and Ian Munro, which do well on any mix. And comparisons "
            "are not the whole cost: Part 24's branch-free loops and SIMD instructions, "
            "comparing several ids at once, matter as much."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), Create(tab.rule),
                      *[FadeIn(VGroup(*row)) for row in tab.cells[1:]], FadeIn(src))
            vo.wait_until("a")
            sim = [i for i, r in enumerate(rows, 1) if max(r["sizes"]) / min(r["sizes"]) < 3]
            self.play(*[Indicate(VGroup(*tab.cells[i]), color=WHITE, scale_factor=1.03) for i in sim],
                      FadeIn(notes[0]))
            vo.wait_until("b")
            big = [i for i, r in enumerate(rows, 1) if max(r["sizes"]) / min(r["sizes"]) >= 3]
            self.play(*[Indicate(VGroup(*tab.cells[i]), color=YES, scale_factor=1.03) for i in big],
                      FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def phrases(self):
        ph = load("phrase")
        ix = load("index")
        head = label(r"Phrases: \ positions in the postings", font_size=36).to_edge(UP, buff=0.3)
        white, whale = [14, 102, 233], [15, 61, 234]
        shifted = [p - 1 for p in whale]

        def prow(name, ps, col):
            bs = VGroup(*[tag_box(str(p), color=col, size=19, w=0.85, h=0.48) for p in ps]).arrange(RIGHT, buff=0.15)
            n = label(name, font_size=20, color=col)
            return VGroup(n, bs)
        r1 = prow(r"\texttt{white} at", white, DATA)
        r2 = prow(r"\texttt{whale} at", whale, LAM)
        r3 = prow(r"\texttt{whale} $-\,1$", shifted, HEAD)
        left = VGroup(r1, r2, r3)
        for r in left:
            r[1].next_to(r[0], RIGHT, buff=0.25)
        left.arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        xr = max(r[0].get_right()[0] for r in left)
        for r in left:
            r[0].align_to([xr, 0, 0], RIGHT)
            r[1].shift(RIGHT * (xr + 0.25 - r[1].get_left()[0]))
        cap = label(r"inside one passage that has both words", font_size=18, color=GREY_A)
        illus = note(r"illustrative positions", font_size=16)
        top = VGroup(cap, illus).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        VGroup(top, left).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(head, DOWN, buff=0.45).to_edge(
            LEFT, buff=0.4)
        match = [k for k, p in enumerate(shifted) if p in white]
        hit = label(r"the phrase begins at "
                    + r" and ".join(str(shifted[k]) for k in match), font_size=20, color=YES).next_to(
            left, DOWN, buff=0.35).align_to(left, LEFT)
        body = [[rf"\texttt{{{k}}}", f"{v['all_words_docs']:,}", f"{v['phrase_docs']:,}"] for k, v in ph.items()]
        tab = grid_table([r"phrase", r"all the words", r"the phrase"], body, widths=[3.3, 2.0, 1.7], row_h=0.6,
                         font_size=22, mono_cols=())
        tab.next_to(head, DOWN, buff=0.6).to_edge(RIGHT, buff=0.35)
        for i in range(1, len(body) + 1):
            tab.cells[i][2].set_color(YES)
        tl = note(r"passages of the novels", font_size=17).next_to(tab, DOWN, buff=0.15).align_to(tab, LEFT)
        notes = VGroup(
            wrapped_label(r"intersect the passage lists first; \ then, \ in each common passage, \ shift the second "
                          r"word's positions back by one and intersect with the first's", 12.4, font_size=20,
                          color=WHITE),
            wrapped_label(rf"positions cost space: \ {ix['tokens']:,} positions beside {ix['postings']:,} "
                          rf"passage ids; \ Chapter 4 compresses both", 12.4, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(VGroup(hit, tl), DOWN, buff=0.8).set_x(0)
        with self.voiceover(
            "Some queries are phrases: white whale, the two words adjacent and in order. <bookmark mark='a'/> "
            "That is why our postings keep positions. First intersect the passage lists, as before. Then, inside "
            "each passage that has both words, shift every position of whale back by one, and intersect with the "
            "positions of white. <bookmark mark='b'/> Each survivor is a place where the phrase begins. "
            "<bookmark mark='c'/> In the novels, a hundred and twenty-five passages contain both white and whale, "
            "but only sixty-four contain the phrase. Three passages contain call, me and Ishmael, and exactly one "
            "has the phrase: the first line of chapter one. <bookmark mark='d'/> Positions are not free: four and a "
            "half million of them, beside two point four million passage ids. The next chapter makes all of it "
            "small."
        ) as vo:
            self.play(FadeIn(head), FadeIn(top), FadeIn(r1), FadeIn(r2))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]), TransformFromCopy(r2, r3), run_time=1.5)
            vo.wait_until("b")
            self.play(*[a for k in match for a in lit(r1[1][k]) + lit(r3[1][k])], FadeIn(hit))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[0])), Create(tab.rule), FadeIn(tl),
                      LaggedStart(*[FadeIn(VGroup(*row)) for row in tab.cells[1:]], lag_ratio=0.3), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN,)
