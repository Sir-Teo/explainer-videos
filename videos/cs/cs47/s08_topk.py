from __future__ import annotations

import random

from explainer.cs import *  # noqa: F403
from videos.cs.cs47.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, mono, tag_box

# a toy query for the pictures (illustrative): three terms, their postings and score upper bounds, a fixed threshold
TOY = {"captain": [2, 5, 9, 14, 20, 27, 31], "ship": [3, 9, 12, 21, 27, 33], "ahab": [9, 18, 27, 34]}
UB = {"captain": 0.8, "ship": 1.2, "ahab": 3.0}
THETA = 2.6


def wand_steps():
    """WAND on the toy lists with theta held fixed: (kind, pivot doc, cursors after the step, sorted order, sum)."""
    cur = {t: 0 for t in TOY}
    steps = []
    while True:
        live = [t for t in TOY if cur[t] < len(TOY[t])]
        if not live:
            break
        live.sort(key=lambda t: TOY[t][cur[t]])
        acc, pivot = 0.0, None
        for t in live:
            acc += UB[t]
            if acc > THETA:
                pivot = t
                break
        if pivot is None:
            break
        pd = TOY[pivot][cur[pivot]]
        order = [(t, TOY[t][cur[t]]) for t in live[:live.index(pivot) + 1]]
        if TOY[live[0]][cur[live[0]]] == pd:
            kind = "score"
            for t in live:
                if TOY[t][cur[t]] == pd:
                    cur[t] += 1
        else:
            kind = "skip"
            for t in live:
                if TOY[t][cur[t]] >= pd:
                    break
                while cur[t] < len(TOY[t]) and TOY[t][cur[t]] < pd:
                    cur[t] += 1
        steps.append((kind, pd, dict(cur), order, acc))
    return steps


class Topk(VoiceoverScene):
    def construct(self):
        self.card()
        self.everything()
        self.bounds()
        self.wand()
        self.savings()
        self.blockmax()
        self.tiers()

    def card(self):
        card = chapter_card(7, r"Top $k$, fast", r"Why score a passage that cannot make the top ten?",
                            lit=(2003, 2011),
                            extra=((1995, r"Turtle and Flood: \ max-score"), (2003, r"Broder et al.: \ WAND"),
                                   (2011, r"Ding and Suel: \ block-max WAND")), part=PART)
        with self.voiceover("Chapter seven. Top k, fast."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def everything(self):
        ix = load("index")
        sea = next(r for r in load("wand")["rows"] if r["query"] == "the sea")
        head = label(r"Scoring everything", font_size=36).to_edge(UP, buff=0.3)
        strip = Rectangle(width=11.6, height=0.45, stroke_color=GREY_C, stroke_width=1.5).move_to([0, 2.0, 0])
        strip_l = label(rf"all {ix['docs']:,} passages, \ in document order", font_size=18,
                        color=GREY_A).next_to(strip, UP, buff=0.1).align_to(strip, LEFT)
        sweep = ValueTracker(0.001)
        fill = always_redraw(lambda: Rectangle(width=11.6 * sweep.get_value(), height=0.45, stroke_width=0,
                                               fill_color=DATA, fill_opacity=0.55).align_to(strip, LEFT).set_y(2.0))
        cursor = always_redraw(lambda: Line([-5.8 + 11.6 * sweep.get_value(), 1.65, 0],
                                            [-5.8 + 11.6 * sweep.get_value(), 2.35, 0], color=HEAD, stroke_width=3))
        slots = VGroup(*[Square(0.55, stroke_color=GREY_B, stroke_width=1.5) for _ in range(10)]).arrange(
            RIGHT, buff=0.12).move_to([-1.6, 0.3, 0])
        slots_l = label(r"the ten best so far: \ a min-heap", font_size=19, color=WHITE).next_to(slots, LEFT,
                                                                                               buff=0.3)
        if slots_l.get_left()[0] < -6.8:
            VGroup(slots_l, slots).shift(RIGHT * (-6.8 - slots_l.get_left()[0]))
        theta = label(r"$\theta$", font_size=26, color=HEAD).next_to(slots[0], DOWN, buff=0.12)
        theta_l = label(r"its smallest score: \ the score to beat", font_size=18, color=HEAD).next_to(
            theta, RIGHT, buff=0.15)
        count = label(rf"\textit{{the sea}}: \ {sea['candidates']:,} of the {ix['docs']:,} passages contain a "
                      r"query term, \ and every one of them is scored", font_size=21,
                      color=WHITE).next_to(slots, DOWN, buff=1.1).set_x(0)
        notes = VGroup(
            wrapped_label(r"term at a time: \ one list after another, \ adding into an accumulator per passage; \ "
                          r"document at a time: \ all lists in step, \ one passage finished before the next", 12.4,
                          font_size=19, color=GREY_A),
        ).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "A reader wants ten results, not a ranking of every passage. <bookmark mark='a'/> The simplest evaluation"
            " walks the postings of all the query's terms together, in document order, scores every passage "
            "containing any of them, and keeps the best ten in a min-heap. <bookmark mark='b'/> The smallest score in"
            " that heap is the threshold, theta: the score to beat. <bookmark mark='c'/> For the query the sea, "
            "eleven thousand two hundred and fifty-seven of our eleven thousand two hundred and sixty-one passages "
            "are scored, and all but ten scores are thrown away."
        ) as vo:
            self.play(FadeIn(head), Create(strip), FadeIn(strip_l))
            self.add(fill, cursor)
            vo.wait_until("a")
            self.play(FadeIn(slots), FadeIn(slots_l))
            self.play(sweep.animate.set_value(0.5),
                      LaggedStart(*[s.animate.set_fill(DATA, opacity=0.6) for s in slots], lag_ratio=0.3),
                      run_time=3, rate_func=linear)
            vo.wait_until("b")
            self.play(slots[0].animate.set_stroke(HEAD, width=4), FadeIn(theta), FadeIn(theta_l))
            vo.wait_until("c")
            self.play(sweep.animate.set_value(1.0), run_time=2.5, rate_func=linear)
            self.play(FadeIn(count), FadeIn(notes))
        self.wait(0.4)
        fill.clear_updaters()
        cursor.clear_updaters()
        self.clear_scene()

    def bounds(self):
        head = label(r"An upper bound per term", font_size=36).to_edge(UP, buff=0.3)
        base, sc, w = -2.0, 1.3, 0.6
        xs = {"captain": -5.7, "ship": -4.8, "ahab": -3.9}
        cols = {"captain": DATA, "ship": LAM, "ahab": KERN}
        bars, names, vals = VGroup(), VGroup(), VGroup()
        for t, x in xs.items():
            b = Rectangle(width=w, height=UB[t] * sc, stroke_width=0, fill_color=cols[t], fill_opacity=0.8)
            b.move_to([x, base + UB[t] * sc / 2, 0])
            bars.add(b)
            names.add(mono(t, size=15, color=cols[t]).next_to([x, base, 0], DOWN, buff=0.15))
            vals.add(label(f"{UB[t]:.1f}", font_size=18, color=cols[t]).next_to(b, UP, buff=0.08))
        xs2 = -2.4
        st1 = Rectangle(width=w, height=UB["captain"] * sc, stroke_width=0, fill_color=DATA, fill_opacity=0.8)
        st1.move_to([xs2, base + UB["captain"] * sc / 2, 0])
        st2 = Rectangle(width=w, height=UB["ship"] * sc, stroke_width=0, fill_color=LAM, fill_opacity=0.8)
        st2.next_to(st1, UP, buff=0)
        st_l = label(r"captain + ship", font_size=16, color=GREY_A).next_to([xs2, base, 0], DOWN, buff=0.15)
        st_v = label(f"{UB['captain'] + UB['ship']:.1f}", font_size=18, color=NO).next_to(st2, UP, buff=0.08)
        cross = Cross(VGroup(st1, st2), stroke_color=NO, stroke_width=4)
        axis = Line([-6.2, base, 0], [-1.8, base, 0], color=GREY_C, stroke_width=1.5)
        th = DashedLine([-6.2, base + THETA * sc, 0], [-1.8, base + THETA * sc, 0], color=HEAD, stroke_width=2.5)
        th_l = label(rf"$\theta = {THETA}$", font_size=20, color=HEAD).next_to(th, UP, buff=0.08).align_to(th, LEFT)
        ill = label(r"illustrative", font_size=16, color=GREY_B).next_to(names, DOWN, buff=0.3).set_x(-4.0)
        notes = VGroup(
            wrapped_label(r"at index time, \ store with each term the largest contribution it makes to any "
                          r"passage's score", 5.6, font_size=20, color=WHITE),
            wrapped_label(r"chapter 5's saturation caps a BM25 term at $\mathrm{idf}\,(k_1 + 1)$; \ the stored "
                          r"maximum is tighter", 5.6, font_size=20, color=GREY_A),
            wrapped_label(r"a passage with only \texttt{captain} and \texttt{ship} scores at most 2.0 $< \theta$: "
                          r"\ it cannot enter the top ten, \ so it need not be scored", 5.6, font_size=20, color=NO),
            wrapped_label(r"\textbf{max-score} \ (Turtle and Flood, 1995): \ terms whose bounds together cannot "
                          r"reach $\theta$ never propose a candidate; \ their lists are only consulted", 5.6,
                          font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.7, -0.2, 0])
        with self.voiceover(
            "Better to know, before scoring, the most a passage could score. <bookmark mark='a'/> When the index is "
            "built, store with each term the largest contribution it makes to any passage. Chapter five's saturation "
            "caps it anyway; the stored maximum is tighter. <bookmark mark='b'/> Suppose theta is two point six. A "
            "passage with only captain and ship scores at most two, so it cannot enter the top ten and need not be "
            "scored. <bookmark mark='c'/> Only passages with ahab can. Turtle and Flood's max-score, in 1995, used "
            "exactly this: terms whose bounds together cannot reach theta never propose a candidate."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(names), FadeIn(ill))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.3), FadeIn(vals),
                      FadeIn(notes[0]), FadeIn(notes[1]))
            vo.wait_until("b")
            self.play(Create(th), FadeIn(th_l))
            self.play(GrowFromEdge(st1, DOWN), FadeIn(st_l))
            self.play(GrowFromEdge(st2, DOWN), FadeIn(st_v))
            self.play(Create(cross), FadeIn(notes[2]))
            vo.wait_until("c")
            self.play(Indicate(bars[2], color=YES), FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def wand(self):
        head = label(r"WAND: \ the pivot", font_size=36).to_edge(UP, buff=0.3)
        x0, dx = -3.0, 0.27
        ys = {"captain": 2.1, "ship": 1.35, "ahab": 0.6}
        cols = {"captain": DATA, "ship": LAM, "ahab": KERN}
        boxes = {}
        rows = VGroup()
        for t, ds in TOY.items():
            nm = VGroup(mono(t, size=16, color=cols[t]),
                        label(rf"UB {UB[t]:.1f}", font_size=17, color=GREY_A)).arrange(RIGHT, buff=0.2)
            nm.move_to([-4.6, ys[t], 0])
            row = VGroup(nm)
            for d in ds:
                b = tag_box(str(d), color=cols[t], size=15, w=0.44, h=0.42).move_to([x0 + d * dx, ys[t], 0])
                boxes[(t, d)] = b
                row.add(b)
            rows.add(row)
        th = label(rf"$\theta = {THETA}$, \ held fixed \ (illustrative)", font_size=18,
                   color=HEAD).next_to(rows, DOWN, buff=0.25).align_to(rows, RIGHT)

        def tri(t, i):
            ds = TOY[t]
            x = x0 + (ds[i] * dx if i < len(ds) else 36 * dx)
            return Triangle(color=HEAD, fill_opacity=1).scale(0.09).move_to([x, ys[t] - 0.32, 0])
        cur0 = {t: 0 for t in TOY}
        cursors = {t: tri(t, 0) for t in TOY}
        status = None
        steps = wand_steps()
        n_union = len({d for ds in TOY.values() for d in ds})
        scored = [pd for k, pd, _, _, _ in steps if k == "score"]
        notes = VGroup(
            wrapped_label(r"sort the cursors by the document they point at; \ add their upper bounds in that order; "
                          r"\ the first cursor where the sum passes $\theta$ is the \textbf{pivot}", 12.4,
                          font_size=19, color=WHITE),
            wrapped_label(r"no document before the pivot's can reach $\theta$: \ earlier cursors jump to it \ "
                          r"(skip pointers, \ galloping: \ chapter 3)", 12.4, font_size=19, color=HEAD),
            wrapped_label(rf"when they all land on it, \ score that one document in full: \ here {len(scored)} of "
                          rf"the {n_union} documents, \ exactly those containing \texttt{{ahab}}, \ the only ones "
                          r"that can beat $\theta$", 12.4, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.35)

        def status_for(order, acc, pd, kind):
            terms = r" $+$ ".join(rf"\texttt{{{t}}}@{d}" for t, d in order)
            act = r"score it" if kind == "score" else r"skip to it"
            return label(rf"{terms}: \ bounds pass $\theta$ at doc {pd}: \ {act}", font_size=19,
                         color=YES if kind == "score" else HEAD).move_to([0, -0.5, 0])
        with self.voiceover(
            "Broder and his colleagues, in 2003, made the bound into a walk called WAND, for weak, or weighted, and. "
            "<bookmark mark='a'/> Each term has a cursor. Sort the cursors by the document they point at, and add up "
            "their bounds in that order: the first cursor where the sum passes theta is the pivot. "
            "<bookmark mark='b'/> No earlier document can reach theta, so every earlier cursor jumps straight to the "
            "pivot document, with chapter three's skip pointers or galloping. <bookmark mark='c'/> When they all land"
            " on it, that document is scored in full. Here four of thirteen documents are scored: exactly those with "
            "ahab."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows), FadeIn(th), *[FadeIn(c) for c in cursors.values()])
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            prev = dict(cur0)
            for kind, pd, cur, order, acc in steps:
                new = status_for(order, acc, pd, kind)
                piv = [boxes[(t, pd)] for t in TOY if (t, pd) in boxes]
                swap = FadeIn(new) if status is None else FadeTransform(status, new)
                self.play(swap, *[Indicate(p, color=HEAD, scale_factor=1.15) for p in piv], run_time=0.8)
                status = new
                anims = []
                for t in TOY:
                    for i in range(prev[t], cur[t]):
                        d = TOY[t][i]
                        if kind == "score" and d == pd:
                            anims.append(boxes[(t, d)][0].animate.set_fill(YES, opacity=0.45))
                        else:
                            anims.append(boxes[(t, d)].animate.set_opacity(0.3))
                    if cur[t] != prev[t]:
                        if cur[t] >= len(TOY[t]):
                            anims.append(cursors[t].animate.move_to(tri(t, cur[t])).set_opacity(0))
                        else:
                            anims.append(cursors[t].animate.move_to(tri(t, cur[t])))
                if anims:
                    self.play(*anims, run_time=0.7)
                prev = cur
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def savings(self):
        ix = load("index")
        rows_d = load("wand")["rows"]
        head = label(r"WAND on the novels", font_size=36).to_edge(UP, buff=0.3)
        rows = [[rf"\textit{{{r['query']}}}", f"{r['candidates']:,}", f"{r['scored']:,}", ""] for r in rows_d]
        widths = [3.4, 3.0, 2.2, 3.8]
        tab = grid_table([r"query \ (BM25, top ten)", r"passages with a term", r"fully scored",
                          r"share scored"], rows, widths=widths, row_h=0.5, font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        left = tab.cells[0][3].get_x() - widths[3] / 2 + 0.2
        bars, pct = VGroup(), VGroup()
        for i, r in enumerate(rows_d, 1):
            s = r["scored"] / r["candidates"]
            y = tab.cells[i][0].get_y()
            b = Rectangle(width=max(0.03, s * 5.0), height=0.26, stroke_width=0, fill_color=YES if s < 0.2 else HEAD,
                          fill_opacity=0.85).move_to([left, y, 0], aligned_edge=LEFT)
            bars.add(b)
            pct.add(label(rf"{100 * s:.0f}\%", font_size=18, color=GREY_A).next_to(b, RIGHT, buff=0.12))
        same = all(r["same_top10"] for r in rows_d)
        notes = VGroup(
            wrapped_label(r"\textit{the sea}: \ \textit{the} is in nearly every passage, \ but its bound is tiny; "
                          r"\ once $\theta$ rises, \ only passages with \textit{sea} can drive the walk", 12.4,
                          font_size=20, color=WHITE),
            wrapped_label(r"\textit{pride prejudice}: \ both words are rare, \ their bounds are high, \ and little "
                          r"can be pruned", 12.4, font_size=20, color=HEAD),
            wrapped_label((r"in all five queries the top ten is identical to exhaustive scoring, \ score for score: "
                           r"\ WAND is \textbf{safe}" if same else r"the top tens differ"), 12.4, font_size=20,
                          color=YES if same else NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        foot = label(rf"{ix['docs']:,} passages; \ $\theta$ rises as better passages are found", font_size=16,
                     color=GREY_B).next_to(tab, DOWN, buff=0.15).align_to(tab, RIGHT)
        notes.next_to(foot, DOWN, buff=0.6).set_x(0)
        with self.voiceover(
            "On the novels, with BM25 and a real, rising threshold, the savings are large. <bookmark mark='a'/> For "
            "white whale, WAND scores two hundred and thirty-five of the sixteen hundred and ten passages that "
            "contain a term. For the sea, about a tenth: the word the is everywhere, but its bound is tiny. "
            "<bookmark mark='b'/> Pride prejudice saves least: both words are rare, their bounds high, and nearly "
            "half the candidates must be checked. <bookmark mark='c'/> In every query the top ten is identical to "
            "exhaustive scoring, score for score. WAND is safe: it never trades accuracy for speed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars], lag_ratio=0.25), FadeIn(pct),
                      run_time=2)
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Indicate(tab.cells[5][0], color=HEAD), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def blockmax(self):
        head = label(r"Block-max WAND", font_size=36).to_edge(UP, buff=0.3)
        rng = random.Random(7)
        caps = [0.48, 1.0, 0.42, 0.8]           # each block's best (illustrative)
        hs = []
        for c in caps:
            blk = [rng.uniform(0.08, c * 0.9) for _ in range(8)]
            blk[rng.randrange(8)] = c
            hs += blk
        base, sc, bw = -1.5, 3.0, 0.2
        x0 = -6.3
        theta = 0.6
        bars = VGroup(*[Rectangle(width=bw * 0.75, height=h * sc, stroke_width=0, fill_color=DATA,
                                  fill_opacity=0.85).move_to([x0 + (i + 0.5) * bw, base + h * sc / 2, 0])
                        for i, h in enumerate(hs)])
        axis = Line([x0, base, 0], [x0 + 32 * bw, base, 0], color=GREY_C, stroke_width=1.5)
        gmax = DashedLine([x0, base + sc, 0], [x0 + 32 * bw, base + sc, 0], color=NO, stroke_width=2)
        gmax_l = label(r"one bound for the whole list", font_size=17, color=NO).next_to(gmax, UP, buff=0.08).align_to(
            gmax, LEFT)
        bmax = VGroup(*[Line([x0 + k * 8 * bw, base + c * sc, 0], [x0 + (k + 1) * 8 * bw, base + c * sc, 0],
                             color=LAM, stroke_width=4) for k, c in enumerate(caps)])
        seps = VGroup(*[DashedLine([x0 + k * 8 * bw, base, 0], [x0 + k * 8 * bw, base + sc + 0.2, 0], color=GREY_D,
                                   stroke_width=1) for k in range(1, 4)])
        th = DashedLine([x0, base + theta * sc, 0], [x0 + 32 * bw, base + theta * sc, 0], color=HEAD,
                        stroke_width=2.5)
        th_l = label(r"$\theta$", font_size=22, color=HEAD).next_to(th, RIGHT, buff=0.1)
        cap_l = label(r"one term's postings: \ score contributions in blocks \ (illustrative)", font_size=17,
                      color=GREY_A).next_to(axis, DOWN, buff=0.15).align_to(axis, LEFT)
        skip = [k for k, c in enumerate(caps) if c < theta]
        dim = [bars[k * 8 + j] for k in skip for j in range(8)]
        notes = VGroup(
            wrapped_label(r"one long list's single maximum is loose: \ one passage that says \textit{whale} forty "
                          r"times sets the bound for all", 5.0, font_size=19, color=WHITE),
            wrapped_label(r"Ding and Suel \ (2011): \ store a maximum for every block of postings, \ beside the "
                          r"skip data", 5.0, font_size=19, color=LAM),
            wrapped_label(r"after WAND picks a pivot, \ check the block maxima: \ a block whose best cannot reach "
                          r"$\theta$ is skipped without being decoded", 5.0, font_size=19, color=YES),
            wrapped_label(r"still safe; \ Lucene adopted it in 2019", 5.0, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.2, 0.1, 0])
        with self.voiceover(
            "One maximum per term is loose: a single passage that says whale forty times sets the bound for the whole"
            " list. <bookmark mark='a'/> Ding and Suel, in 2011, stored a maximum for every block of postings, beside"
            " the skip data. <bookmark mark='b'/> After WAND picks a pivot, block-max WAND checks these tighter "
            "maxima, and skips whole blocks that cannot reach theta, without even decoding them. <bookmark mark='c'/>"
            " It is still safe. Lucene adopted it in 2019; since then Elasticsearch, by default, counts matches "
            "exactly only up to ten thousand, since counting all would mean visiting all."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(bars), FadeIn(cap_l), Create(gmax), FadeIn(gmax_l),
                      FadeIn(notes[0]))
            self.play(Create(th), FadeIn(th_l))
            vo.wait_until("a")
            self.play(FadeIn(seps), Create(bmax), FadeIn(notes[1]))
            vo.wait_until("b")
            self.play(*[b.animate.set_fill(GREY_D, opacity=0.5) for b in dim],
                      *[bmax[k].animate.set_color(GREY_B) for k in skip], FadeIn(notes[2]))
            vo.wait_until("c")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def tiers(self):
        head = label(r"Tiers and champion lists", font_size=36).to_edge(UP, buff=0.3)
        terms = [("captain", DATA, 7.0), ("ahab", KERN, 4.5), ("ship", LAM, 8.5)]
        x0 = -4.2
        rows = VGroup()
        t1s, t2s = VGroup(), VGroup()
        for k, (t, c, w2) in enumerate(terms):
            y = 1.9 - k * 0.75
            nm = mono(t, size=16, color=c).move_to([-5.6, y, 0])
            t1 = Rectangle(width=1.4, height=0.38, stroke_color=c, stroke_width=1.5, fill_color=c,
                           fill_opacity=0.7).move_to([x0, y, 0], aligned_edge=LEFT)
            t2 = Rectangle(width=w2 * 0.95, height=0.38, stroke_color=GREY_C, stroke_width=1.5, fill_color=GREY_D,
                           fill_opacity=0.3).next_to(t1, RIGHT, buff=0.1)
            if t2.get_right()[0] > 6.8:
                t2.stretch_to_fit_width(6.8 - t2.get_left()[0]).align_to(t1.get_right() + RIGHT * 0.1, LEFT)
            rows.add(VGroup(nm, t1, t2))
            t1s.add(t1)
            t2s.add(t2)
        tl1 = label(r"tier 1: \ each term's highest-scoring postings", font_size=17, color=YES).next_to(
            t1s, UP, buff=0.15).align_to(t1s, LEFT)
        tl2 = label(r"tier 2: \ the rest", font_size=17, color=GREY_A).next_to(t2s[0], UP, buff=0.15).align_to(
            t2s[0], RIGHT)
        ill = label(r"illustrative", font_size=16, color=GREY_B).next_to(rows, DOWN, buff=0.12).align_to(rows, RIGHT)
        scan = Rectangle(width=0.08, height=2.3, stroke_width=0, fill_color=HEAD, fill_opacity=0.9).move_to(
            [x0, 1.15, 0])
        found = label(r"ten good answers in tier 1: \ stop", font_size=19, color=YES).next_to(t1s, DOWN, buff=0.4)
        found.align_to(t1s, LEFT)
        lines = VGroup(
            wrapped_label(r"search tier 1 first; \ go on to tier 2 only if fewer than ten good answers came back",
                          12.4, font_size=20, color=WHITE),
            wrapped_label(r"\textbf{champion lists} \ (Manning, Raghavan and Sch\"utze): \ one tier, \ each term's "
                          r"best $r$ documents", 12.4, font_size=20, color=LAM),
            wrapped_label(r"\textbf{unsafe}: \ a passage strong only in the combination of its terms can be missed; "
                          r"\ chapter 6's metrics measure the loss", 12.4, font_size=20, color=NO),
            wrapped_label(r"the order can also be a quality score for each page: \ next, \ links", 12.4,
                          font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Other shortcuts trade a little exactness for speed. <bookmark mark='a'/> A tiered index splits each "
            "term's postings: the highest-scoring in tier one, the rest in tier two. <bookmark mark='b'/> A query "
            "searches tier one, and goes on only if fewer than ten good answers came back. Champion lists, in "
            "Manning, Raghavan and Schütze's textbook, keep just each term's best few documents. <bookmark mark='c'/>"
            " These are unsafe: a passage strong only in the combination of its terms can be missed, and chapter "
            "six's metrics measure the loss. <bookmark mark='d'/> Tiers can also be ordered by a quality score for "
            "each page, such as one computed from links."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(tl1), FadeIn(tl2), Indicate(t1s, color=YES))
            vo.wait_until("b")
            self.play(FadeIn(scan), FadeIn(lines[0]))
            self.play(scan.animate.move_to([x0 + 1.4, 1.15, 0]), run_time=1.5, rate_func=linear)
            self.play(FadeIn(found), FadeOut(scan), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, NO)
