from __future__ import annotations

import bisect
import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs42.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, axes, grid_table, load, module_box, mono,
                                   tag_box, trace, data_mono)


def _row(text, w=2.3, ticked=False, color=GREY_B):
    """A list row: a box, a checkbox (its input state) and its text."""
    r = Rectangle(width=w, height=0.42, stroke_color=color, stroke_width=1.5, fill_color=BLACK, fill_opacity=0.0)
    box = Square(0.24, stroke_color=GREY_A, stroke_width=1.5).move_to(r.get_left() + RIGHT * 0.3)
    tick = Square(0.14, stroke_width=0, fill_color=HEAD, fill_opacity=1 if ticked else 0).move_to(box)
    t = mono(text, size=17, color=WHITE).next_to(box, RIGHT, buff=0.25)
    return VGroup(r, box, tick, t)


class Frameworks(VoiceoverScene):
    def construct(self):
        self.card()
        self.vdom()
        self.exact()
        self.keyed()
        self.moves()
        self.signals()

    def card(self):
        card = chapter_card(8, r"UI frameworks", r"How do you redraw only what changed?", lit=(1989, 2024),
                            extra=((1989, r"Zhang and Shasha: \ tree edit distance"), (2013, r"React"),
                                   (2024, r"Svelte 5: \ signals")), part=PART)
        with self.voiceover("Chapter eight. User interface frameworks."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def vdom(self):
        head = label(r"Render, \ diff, \ patch", font_size=36).to_edge(UP, buff=0.3)

        def tree(texts, cx, changed=None):
            root = tag_box("ul", color=GREY_B, size=17).move_to([cx, 1.6, 0])
            lis, txt, edges = VGroup(), VGroup(), VGroup()
            for i, s in enumerate(texts):
                li = tag_box("li", color=DATA, size=17).move_to([cx + (i - 1.5) * 1.05, 0.5, 0])
                tx = mono(s, size=16, color=HEAD if i == changed else WHITE).next_to(li, DOWN, buff=0.3)
                lis.add(li)
                txt.add(tx)
                edges.add(Line(root.get_bottom(), li.get_top(), color=GREY_C, stroke_width=1.5))
                edges.add(Line(li.get_bottom(), tx.get_top(), color=GREY_C, stroke_width=1.5))
            g = VGroup(edges, root, lis, txt)
            g.root, g.lis, g.txt = root, lis, txt
            return g
        old_t = ["item 0", "item 1", "item 2", "item 3"]
        new_t = ["item 0", "item 1", "changed", "item 3"]
        old = tree(old_t, -4.3)
        new = tree(new_t, 0.3, changed=2)
        for g in (old, new):
            for t in g.txt:
                if t.width > 0.98:
                    t.width = 0.98
        cap = VGroup(label(r"old virtual tree", font_size=19, color=GREY_A).next_to(old, UP, buff=0.2),
                     label(r"new virtual tree", font_size=19, color=GREY_A).next_to(new, UP, buff=0.2))
        state = label(r"state changes: \ \texttt{render(state)} runs again", font_size=19, color=HEAD).next_to(
            new, DOWN, buff=0.45)
        patch = VGroup(label(r"the patch", font_size=19, color=YES),
                       mono('row 2: text = "changed"', size=16, color=YES)).arrange(DOWN, aligned_edge=LEFT,
                                                                                buff=0.15)
        dom = VGroup(*[mono(s, size=17, color=WHITE) for s in old_t]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        domb = SurroundingRectangle(dom, color=KERN, buff=0.2, corner_radius=0.08)
        doml = label(r"the real DOM", font_size=19, color=KERN).next_to(domb, UP, buff=0.12)
        VGroup(patch, VGroup(doml, domb, dom)).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(
            [4.9, 0.6, 0])
        dom_new = mono("changed", size=17, color=YES).move_to(dom[2], aligned_edge=LEFT)
        ill = note(r"the timing experiment's list, \ drawn with four rows", font_size=17).to_edge(DOWN, buff=1.45)
        lines = wrapped_label(r"the page is a function of the state: \ build a new tree of plain objects, \ compare "
                              r"it with the last one, \ and touch the slow, \ real DOM only where they differ", 12.4,
                              font_size=20, color=WHITE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Keeping every element in step with the program's state by hand is where interface bugs live."
            " React, released in 2013, made a different promise. <bookmark mark='a'/> Describe the page "
            "as a function of the state; when the state changes, call it again, and get a new tree of "
            "plain objects, a virtual DOM. <bookmark mark='b'/> Compare it with the previous tree. Here "
            "one row's text differs. <bookmark mark='c'/> The result is a patch, one text edit, and only "
            "that touches the real DOM, where every change can mean style, layout and paint again."
        ) as vo:
            self.play(FadeIn(head), FadeIn(old), FadeIn(cap[0]), FadeIn(doml), FadeIn(domb), FadeIn(dom),
                      FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(state), FadeIn(new, shift=RIGHT * 0.3), FadeIn(cap[1]), FadeIn(lines))
            vo.wait_until("b")
            for i in range(4):
                self.play(Indicate(old.txt[i], color=WHITE if i != 2 else NO, scale_factor=1.15),
                          Indicate(new.txt[i], color=WHITE if i != 2 else NO, scale_factor=1.15), run_time=0.5)
            vo.wait_until("c")
            self.play(FadeIn(patch))
            self.play(Transform(dom[2], dom_new), Indicate(domb, color=YES))
        self.wait(0.4)
        self.clear_scene()

    def exact(self):
        rows = load("vdom")["timing"]
        head = label(r"The exact answer against a fast heuristic", font_size=36).to_edge(UP, buff=0.3)
        # log10(ms) + 2 on a linear axis, so that the x axis sits at 0.01 ms
        g = axes([0, 130, 20], [0, 5, 1], x_length=6.2, y_length=4.2, x_label=r"rows in the list",
                 y_label=r"time to diff, \ ms \ (log scale)", xticks=[10, 40, 80, 120], yticks=[0, 1, 2, 3, 4, 5],
                 fx=lambda v: f"{v:g}", fy=lambda v: f"{10 ** (v - 2):g}", font=17)
        g.move_to([-2.9, -0.2, 0])
        ax = g.ax
        ex = [(r["n"], math.log10(r["exact_ms"]) + 2) for r in rows]
        he = [(r["n"], math.log10(r["heuristic_ms"]) + 2) for r in rows]
        t_ex, t_he = trace(ax, ex, NO, width=3), trace(ax, he, YES, width=3)
        d_ex = VGroup(*[Dot(ax.c2p(x, y), radius=0.06, color=NO) for x, y in ex])
        d_he = VGroup(*[Dot(ax.c2p(x, y), radius=0.06, color=YES) for x, y in he])
        last = rows[-1]
        l_ex = label(rf"tree edit distance: \ {last['exact_ms']:.0f} ms", font_size=18, color=NO).next_to(
            d_ex[-1], LEFT, buff=0.15).shift(UP * 0.3)
        l_he = label(rf"React-style: \ {last['heuristic_ms']:.2f} ms", font_size=18, color=YES).next_to(
            d_he[-1], LEFT, buff=0.15).shift(UP * 0.3)
        same = all(r["distance"] == r["heuristic_ops"] for r in rows)
        notes = VGroup(
            wrapped_label(r"\textbf{exact}: \ the fewest inserts, \ deletes and relabels turning one tree into the "
                          r"other \ (Zhang and Shasha, \ 1989); \ the best general algorithms are about cubic", 5.2,
                          font_size=19, color=NO),
            wrapped_label(r"\textbf{React's heuristic}, \ linear: \ a different element type replaces the whole "
                          r"subtree; \ children are matched by key, \ or by position", 5.2, font_size=19,
                          color=YES),
            wrapped_label(rf"at {last['n']} rows \ ({last['nodes']} nodes) \ the exact diff takes "
                          rf"{last['exact_ms'] / last['heuristic_ms']:.0f} times as long in our Python, \ and "
                          + (rf"both find the same {last['distance']} edit" if same else r"they differ"), 5.2,
                          font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.9, -0.1, 0])
        with self.voiceover(
            "How should two trees be compared? <bookmark mark='a'/> Exactly, by tree edit distance: the "
            "fewest insertions, deletions and relabellings that turn one into the other. Zhang and "
            "Shasha's algorithm of 1989 is dynamic programming, as in Part 19, and general algorithms are"
            " still about cubic. <bookmark mark='b'/> On lists with one row changed, ours takes three "
            "hundred milliseconds at a hundred and twenty rows. <bookmark mark='c'/> React instead uses "
            "two rules: an element of a different type replaces its whole subtree, and children are "
            "matched by key or by position. That is linear, a third of a millisecond here, and it finds "
            "the same single edit."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Create(t_ex), FadeIn(d_ex), run_time=2)
            self.play(FadeIn(l_ex))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]), Create(t_he), FadeIn(d_he), run_time=1.5)
            self.play(FadeIn(l_he), FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def keyed(self):
        lists = load("vdom")["lists"]
        head = label(r"Keys", font_size=36).to_edge(UP, buff=0.3)
        names = ["a", "b", "c", "d"]
        cols = []
        for cx in (-5.0, -2.1):
            rows = VGroup(*[_row(n, ticked=(n == "b")) for n in names]).arrange(DOWN, buff=0.08)
            rows.move_to([cx, 0.55, 0])
            cols.append(rows)
        titles = VGroup(label(r"matched by position", font_size=19, color=NO).next_to(cols[0], UP, buff=0.25),
                        label(r"matched by key", font_size=19, color=YES).next_to(cols[1], UP, buff=0.25))
        op = mono("prepend one row", size=17, color=HEAD).next_to(VGroup(*titles), UP, buff=0.25)
        step = cols[0][0].height + 0.08
        ill = note(r"illustrative", font_size=17).next_to(VGroup(*cols), DOWN, buff=0.75)
        rows = []
        for case in ("prepend", "append", "remove first", "reverse", "swap two"):
            r = lists[case]
            rows.append([case, f"{r['keyed']}", f"{r['unkeyed']}", f"{r['state_misplaced']}"])
        tab = grid_table([r"100 rows: \ change", r"by key", r"by position", r"state in wrong row"], rows,
                         widths=[2.3, 1.2, 1.6, 2.3], row_h=0.46, font_size=19, mono_cols=())
        tab.move_to([3.15, 0.75, 0])
        tl = label(r"nodes touched", font_size=17, color=GREY_A).next_to(tab, UP, buff=0.12).shift(LEFT * 0.4)
        for i, r in enumerate(rows, 1):
            if int(r[2]) > int(r[1]):
                tab.cells[i][2].set_color(NO)
            if int(r[3]):
                tab.cells[i][3].set_color(NO)
        note_ = wrapped_label(r"the row's checkbox state lives in the real DOM element; \ matched by position, \ "
                              r"elements are reused for different rows and the state goes with the element", 12.4,
                              font_size=19, color=WHITE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Lists need help. Here are four rows, and the user has ticked b. <bookmark mark='a'/> Add a "
            "row at the top. Matched by position, old rows pair with new rows in order: every row's text "
            "is rewritten, a new element appears at the end, and the tick, which lives in the element, "
            "now sits beside a. <bookmark mark='b'/> Give each row a key, a stable identity: one new "
            "element at the top, the others untouched, and the tick stays with b. <bookmark mark='c'/> On"
            " a hundred rows, a prepend touches three nodes by key and a hundred and three by position, "
            "and a hundred rows end up with another row's state."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cols[0]), FadeIn(cols[1]), FadeIn(titles), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(op))
            new_names = ["new"] + names
            self.play(*[Transform(cols[0][i][3], mono(new_names[i], size=17, color=HEAD).move_to(
                cols[0][i][3], aligned_edge=LEFT)) for i in range(4)])
            extra = _row("d").next_to(cols[0][-1], DOWN, buff=0.08)
            self.play(FadeIn(extra, shift=UP * 0.2))
            self.play(cols[0][1][0].animate.set_stroke(NO, width=3), cols[0][1][2].animate.set_fill(NO))
            vo.wait_until("b")
            fresh = _row("new", color=YES).move_to(cols[1][0])
            self.play(cols[1].animate.shift(DOWN * step))
            self.play(FadeIn(fresh, shift=DOWN * 0.2))
            self.play(cols[1][1][0].animate.set_stroke(YES, width=3))
            vo.wait_until("c")
            self.play(FadeIn(tab), FadeIn(tl), FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()

    def moves(self):
        lists = load("vdom")["lists"]
        head = label(r"The fewest moves", font_size=36).to_edge(UP, buff=0.3)
        # an illustrative six-row list with its first and last rows swapped
        new_order = [5, 1, 2, 3, 4, 0]
        react, last = [], -1
        for i in new_order:                    # React's single pass: move whatever is left of the last placed row
            if i < last:
                react.append(i)
            else:
                last = i
        tails, idx, prev = [], [], {}
        for p, x in enumerate(new_order):      # a longest increasing subsequence of old positions stays put
            j = bisect.bisect_left([new_order[t] for t in tails], x)
            prev[p] = tails[j - 1] if j else None
            tails[j:j + 1] = [p]
            idx = tails
        keep, p = set(), idx[-1]
        while p is not None:
            keep.add(new_order[p])
            p = prev[p]
        lis_moved = [i for i in new_order if i not in keep]

        def chips(y, colors):
            g = VGroup(*[tag_box(f"{i}", color=colors[k], size=18, w=0.6) for k, i in enumerate(new_order)])
            return g.arrange(RIGHT, buff=0.15).move_to([-3.4, y, 0])
        old = VGroup(*[tag_box(f"{i}", color=GREY_B, size=18, w=0.6) for i in range(6)]).arrange(
            RIGHT, buff=0.15).move_to([-3.4, 1.9, 0])
        rr = chips(0.7, [GREY_B] * 6)
        ll = chips(-0.6, [GREY_B] * 6)
        lab = VGroup(label(r"old order", font_size=18, color=GREY_A).next_to(old, LEFT, buff=0.3),
                     label(r"React's pass", font_size=18, color=NO).next_to(rr, LEFT, buff=0.3),
                     label(r"LIS", font_size=18, color=YES).next_to(ll, LEFT, buff=0.3))
        res = VGroup(label(rf"{len(react)} moves", font_size=19, color=NO).next_to(rr, RIGHT, buff=0.3),
                     label(rf"{len(lis_moved)} moves", font_size=19, color=YES).next_to(ll, RIGHT, buff=0.3))
        ill = note(r"illustrative: \ six rows, \ first and last swapped", font_size=17).next_to(ll, DOWN, buff=0.3)
        ptr = Triangle(color=HEAD, fill_opacity=1).scale(0.1).next_to(rr[0], UP, buff=0.08)
        rows = [[c, f"{lists[c]['keyed_ops']}", f"{lists[c]['lis_moves']}"] for c in ("reverse", "swap two")]
        tab = grid_table([r"100 rows", r"React's pass", r"LIS"], rows, widths=[2.0, 1.8, 1.0], row_h=0.48,
                         font_size=19, mono_cols=())
        tab.move_to([4.4, 1.0, 0])
        tab.cells[2][1].set_color(NO)
        tab.cells[2][2].set_color(YES)
        tabl = label(r"DOM moves", font_size=17, color=GREY_A).next_to(tab, UP, buff=0.12)
        lines = VGroup(
            wrapped_label(r"React walks the new order once, \ left to right, \ remembering the furthest old position "
                          r"placed so far; \ a row from further left must move", 12.4, font_size=19, color=WHITE),
            wrapped_label(r"keeping a \textbf{longest increasing subsequence} of old positions in place moves the "
                          r"fewest rows \ (Inferno, \ Vue 3); \ found in $O(n \log n)$ \ (Part 19)", 12.4,
                          font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Keys say which rows survive, not how to move them. <bookmark mark='a'/> Swap the first and "
            "last of six rows. React walks the new order once, remembering the furthest old position "
            "placed so far. Row five comes first, so every later row, coming from further left, is moved:"
            " five moves. <bookmark mark='b'/> The fewest moves keep the longest run already in "
            "increasing order, one to four, and move only two. A longest increasing subsequence is a "
            "classic of Part 19, and Inferno and Vue 3 use it. <bookmark mark='c'/> On a hundred rows, "
            "reversing needs ninety-nine moves either way, but swapping two costs React's pass ninety-"
            "nine, against two: an honest weakness, rarely hit in practice."
        ) as vo:
            self.play(FadeIn(head), FadeIn(old), FadeIn(lab[0]))
            vo.wait_until("a")
            self.play(FadeIn(rr), FadeIn(lab[1]), FadeIn(ptr), FadeIn(lines[0]))
            for k, i in enumerate(new_order):
                self.play(ptr.animate.next_to(rr[k], UP, buff=0.08), run_time=0.35)
                self.play(rr[k][0].animate.set_stroke(NO if i in react else YES, width=3), run_time=0.35)
            self.play(FadeIn(res[0]), FadeOut(ptr))
            vo.wait_until("b")
            self.play(FadeIn(ll), FadeIn(lab[2]), FadeIn(ill))
            self.play(*[ll[k][0].animate.set_stroke(NO if i in lis_moved else YES, width=3)
                        for k, i in enumerate(new_order)], FadeIn(res[1]), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab), FadeIn(tabl))
        self.wait(0.4)
        self.clear_scene()

    def signals(self):
        s = load("vdom")["signals"]
        head = label(r"Signals: \ a dependency graph", font_size=36).to_edge(UP, buff=0.3)
        pos = {"first": [-5.4, 1.5], "last": [-5.4, 0.3], "count": [-5.4, -1.2], "full": [-2.5, 0.9],
               "badge": [-2.5, -1.2], "greeting": [0.4, 0.9], "header": [3.4, -0.15]}
        # the inputs signals_demo starts from, and the values its functions give before any write
        vals0 = {"first": "Ada", "last": "Lovelace", "count": "0", "full": "Ada Lovelace",
                 "greeting": "Hello, Ada Lovelace", "badge": "0 new", "header": "Hello, Ada Lovelace | 0 new"}
        vals1 = dict(vals0, count="3", badge=s["values"]["badge"],
                     header=f"{vals0['greeting']} | {s['values']['badge']}")
        vals2 = dict(vals1, last="King", **{k: s["values"][k] for k in ("full", "greeting", "header")})
        nodes, vals, colour = {}, {}, {}
        for k, (x, y) in pos.items():
            col = DATA if k in ("first", "last", "count") else (KERN if k == "header" else LAM)
            colour[k] = col
            nodes[k] = module_box(rf"\texttt{{{k}}}", col, w=1.6, h=0.5, font=19).move_to([x, y, 0])
            vals[k] = data_mono(vals0[k], size=16, color=GREY_A).next_to(nodes[k], DOWN, buff=0.1)
        edges = {}
        for k, ds in s["deps"].items():
            for d in ds:
                edges[(d, k)] = Arrow(nodes[d][0].get_right(), nodes[k][0].get_left(), buff=0.06, stroke_width=2,
                                      color=GREY_C, max_tip_length_to_length_ratio=0.1)
        kinds = VGroup(*[label(t, font_size=17, color=c) for t, c in ((r"signals", DATA), (r"computed", LAM),
                                                                      (r"effect: \ the DOM", KERN))]).arrange(
            RIGHT, buff=0.6).next_to(head, DOWN, buff=0.3)

        def wave(src, value, vnew):
            order = s["reran"][src]
            anims1 = [Indicate(nodes[src], color=HEAD),
                      Transform(vals[src], data_mono(value, size=16, color=HEAD).next_to(nodes[src], DOWN, buff=0.1))]
            anims2 = []
            for k in order:
                anims2.append(nodes[k][0].animate.set_stroke(HEAD, width=4))
                anims2.append(Transform(vals[k], data_mono(vnew[k], size=16, color=HEAD).next_to(nodes[k], DOWN,
                                                                                           buff=0.1)))
            hot = [edges[e] for e in edges if e[1] in order and (e[0] == src or e[0] in order)]
            return anims1, [e.animate.set_color(HEAD) for e in hot], anims2, order

        def reset():
            return [n[0].animate.set_stroke(colour[k], width=2) for k, n in nodes.items()] + [
                e.animate.set_color(GREY_C) for e in edges.values()] + [v.animate.set_color(GREY_A) for v in
                                                                         vals.values()]
        r_count = label(rf"set \texttt{{count}}: \ re-runs {' and '.join(s['reran']['count'])} only", font_size=19,
                        color=HEAD)
        r_last = label(rf"set \texttt{{last}}: \ re-runs {', '.join(s['reran']['last'])}", font_size=19,
                       color=HEAD)
        VGroup(r_count, r_last).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.4, 1.6, 0])
        lines = VGroup(
            wrapped_label(r"no tree to diff: \ reading a signal records a dependency, \ writing one re-runs only what "
                          r"depends on it \ --- \ Part 41's build graph, \ with early cutoff when a value comes out "
                          r"unchanged", 12.4, font_size=19, color=WHITE),
            wrapped_label(r"SolidJS, \ Svelte 5's runes, \ Vue's refs, \ Preact Signals, \ Angular signals", 12.4,
                          font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Another family of frameworks skips the virtual tree. <bookmark mark='a'/> State lives in "
            "signals: a first name, a last name, a count. Computed values read them, and the header reads"
            " those; each read records an edge, so the framework knows the graph. <bookmark mark='b'/> "
            "Set count to three: only the badge and the header re-run. <bookmark mark='c'/> Set the last "
            "name: full name, greeting and header re-run, and the badge does not. <bookmark mark='d'/> It"
            " is Part 41's build graph, recomputed on every write, with its early cutoff: a value that "
            "comes out unchanged stops the wave. SolidJS works this way, and now so do Svelte, Vue, "
            "Preact and Angular."
        ) as vo:
            self.play(FadeIn(head), FadeIn(kinds), *[FadeIn(n) for n in nodes.values()],
                      *[FadeIn(v) for v in vals.values()])
            vo.wait_until("a")
            self.play(*[GrowArrow(e) for e in edges.values()])
            for mk, src, val, vn, r in (("b", "count", "3", vals1, r_count), ("c", "last", "King", vals2, r_last)):
                vo.wait_until(mk)
                a1, a_e, a2, _ = wave(src, val, vn)
                self.play(*a1)
                self.play(*a_e)
                self.play(*a2, FadeIn(r))
                self.wait(0.6)
                self.play(*reset())
            vo.wait_until("d")
            self.play(FadeIn(lines))
        self.wait(0.4)
        self.clear_scene()


_ = (LAM, YES)
