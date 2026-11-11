from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs47.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, mono, tag_box

# a small vocabulary for the BK-tree picture (illustrative), inserted in this order, and a typo to look up
BK_WORDS = ["whale", "while", "white", "wheel", "shall", "whole", "shale", "hale", "whales"]
BK_QUERY, BK_TOL = "whsle", 1


def lev(a: str, b: str) -> int:
    """Levenshtein distance by the dynamic programme of Parts 19 and 21."""
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def lev_table(a: str, b: str):
    D = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) + 1):
        for j in range(len(b) + 1):
            if i == 0 or j == 0:
                D[i][j] = i + j
            else:
                D[i][j] = min(D[i - 1][j] + 1, D[i][j - 1] + 1, D[i - 1][j - 1] + (a[i - 1] != b[j - 1]))
    return D


def bk_tree(words):
    """Nodes as (word, parent index, edge distance), in insertion order."""
    nodes = [(words[0], None, None)]
    kids = {0: {}}
    for w in words[1:]:
        n = 0
        while True:
            d = lev(w, nodes[n][0])
            if d in kids[n]:
                n = kids[n][d]
            else:
                nodes.append((w, n, d))
                kids[n][d] = len(nodes) - 1
                kids[len(nodes) - 1] = {}
                break
    return nodes, kids


def bk_search(nodes, kids, q, tol):
    """Visit order, matches, and the subtrees pruned by the triangle inequality."""
    visited, found, pruned, stack = [], [], [], [0]
    while stack:
        n = stack.pop(0)
        visited.append(n)
        d = lev(q, nodes[n][0])
        if d <= tol:
            found.append(n)
        for k, c in sorted(kids[n].items()):
            (stack if d - tol <= k <= d + tol else pruned).append(c)
    return visited, found, pruned


def tree_layout(parent_of, order, dx, dy, top):
    """x by leaf order, y by depth: a tidy picture of a small tree."""
    children = {n: [c for c in order if parent_of[c] == n] for n in order}
    depth, x, nxt = {}, {}, [0.0]

    def walk(n, dep):
        depth[n] = dep
        if not children[n]:
            x[n] = nxt[0]
            nxt[0] += dx
        else:
            for c in children[n]:
                walk(c, dep + 1)
            x[n] = sum(x[c] for c in children[n]) / len(children[n])
    walk(order[0], 0)
    mid = (min(x.values()) + max(x.values())) / 2
    return {n: [x[n] - mid, top - depth[n] * dy, 0] for n in order}


class Spelling(VoiceoverScene):
    def construct(self):
        self.card()
        self.channel()
        self.distance()
        self.bktree()
        self.corrections()
        self.complete()

    def card(self):
        card = chapter_card(11, r"Spelling and autocomplete", r"What did the user mean to type?",
                            lit=(1964, 1973, 1990),
                            extra=((1964, r"Damerau: \ transpositions"), (1973, r"Burkhard and Keller: \ BK-trees"),
                                   (1990, r"Kernighan, \ Church and Gale: \ the noisy channel")), part=PART)
        with self.voiceover("Chapter eleven. Spelling and autocomplete."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def channel(self):
        sp = load("spell")
        row = next(r for r in sp["rows"] if r["typed"] == "captian")
        head = label(r"The noisy channel", font_size=36).to_edge(UP, buff=0.3)
        meant = VGroup(*[mono(ch, size=30, color=DATA) for ch in row["correction"]]).arrange(RIGHT, buff=0.06)
        src = label(r"what the user meant", font_size=19, color=DATA)
        chan = RoundedRectangle(width=2.6, height=1.0, corner_radius=0.15, stroke_color=KERN, fill_color=KERN,
                                fill_opacity=0.12)
        chan_l = label(r"the channel: \ fingers", font_size=19, color=KERN).move_to(chan)
        typed_l = label(r"what arrived", font_size=19, color=NO)
        meant.move_to([-4.6, 1.4, 0])
        src.next_to(meant, UP, buff=0.25)
        chan.move_to([0, 1.4, 0])
        chan_l.move_to(chan)
        a1 = Arrow(meant.get_right(), chan.get_left(), buff=0.2, color=GREY_B, stroke_width=2)
        out = meant.copy().move_to([4.6, 1.4, 0])
        a2 = Arrow(chan.get_right(), out.get_left(), buff=0.2, color=GREY_B, stroke_width=2)
        typed_l.next_to(out, UP, buff=0.25)
        i, j = row["correction"].index("a", 4), row["correction"].index("i")    # the swapped pair: "ai"
        formula = MathTex(r"\hat w \;=\; \arg\max_{w}\; P(w)\; P(t \mid w)", font_size=40).move_to([0, -0.3, 0])
        lab_p = wrapped_label(r"$P(w)$: \ the language model, \ how often $w$ is meant \ (here: \ its count in the "
                              r"novels)", 5.6, font_size=19, color=DATA).move_to([-3.3, -1.75, 0])
        lab_c = wrapped_label(r"$P(t \mid w)$: \ the channel, \ how likely the slip from $w$ to $t$ \ (here: \ a "
                              r"fixed penalty per edit)", 5.6, font_size=19, color=KERN).move_to([3.3, -1.75, 0])
        foot = wrapped_label(r"Bayes' rule, \ with $P(t)$ dropped because it is the same for every candidate", 12.4,
                             font_size=19, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            f"A user types {' '.join(row['typed'])}. What did they mean? <bookmark mark='a'/> Model the error as a "
            "message sent through a noisy channel: the intended word goes in, the fingers garble it, and a typo "
            "comes out. Here two letters were swapped. <bookmark mark='b'/> To decode, pick the word maximizing "
            "its prior probability times the probability that the channel turned it into this typo. "
            "<bookmark mark='c'/> The prior is a language model; ours is simply each word's count in the novels. "
            "The channel model says which slips are likely; ours "
            "charges a fixed penalty per edit. Kernighan, Church and Gale learned it instead, from real typing "
            "errors, in 1990. <bookmark mark='d'/> It is Bayes' rule."
        ) as vo:
            self.play(FadeIn(head), FadeIn(meant), FadeIn(src), FadeIn(chan), FadeIn(chan_l))
            vo.wait_until("a")
            self.play(GrowArrow(a1), GrowArrow(a2), TransformFromCopy(meant, out), FadeIn(typed_l), run_time=1.5)
            self.play(out[i].animate.move_to(out[j].get_center()), out[j].animate.move_to(out[i].get_center()),
                      run_time=1.0)
            self.play(out[i].animate.set_color(NO), out[j].animate.set_color(NO))
            vo.wait_until("b")
            self.play(Write(formula))
            vo.wait_until("c")
            self.play(FadeIn(lab_p))
            self.play(FadeIn(lab_c))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def distance(self):
        row = next(r for r in load("spell")["rows"] if r["typed"] == "captian")
        a, b = row["typed"], row["correction"]
        D = lev_table(a, b)
        head = label(r"Counting the edits", font_size=36).to_edge(UP, buff=0.3)
        cell = 0.55
        x0, y0 = -5.7, 1.9
        cells = {}
        for i in range(len(a) + 1):
            for j in range(len(b) + 1):
                sq = Square(cell, stroke_color=GREY_D, stroke_width=1).move_to([x0 + j * cell, y0 - i * cell, 0])
                t = label(str(D[i][j]), font_size=19, color=GREY_A if i == 0 or j == 0 else WHITE).move_to(sq)
                cells[i, j] = VGroup(sq, t)
        top = VGroup(*[mono(ch, size=19, color=YES).move_to([x0 + (j + 1) * cell, y0 + cell, 0])
                       for j, ch in enumerate(b)])
        side = VGroup(*[mono(ch, size=19, color=NO).move_to([x0 - cell, y0 - (i + 1) * cell, 0])
                        for i, ch in enumerate(a)])
        border = VGroup(*[cells[i, j] for i in range(len(a) + 1) for j in range(len(b) + 1) if i == 0 or j == 0])
        inner = [cells[i, j] for i in range(1, len(a) + 1) for j in range(1, len(b) + 1)]
        last = cells[len(a), len(b)]
        ring = SurroundingRectangle(last, color=HEAD, buff=0.02, stroke_width=3)
        notes = VGroup(
            wrapped_label(r"cell $(i, j)$: \ the fewest insertions, \ deletions and substitutions turning the first "
                          r"$i$ letters of one word into the first $j$ of the other", 5.4, font_size=19, color=WHITE),
            wrapped_label(r"each cell is the cheapest of three neighbours plus one, \ or the diagonal for free when "
                          r"the letters agree: \ Part 19's dynamic programming, \ Part 21's edit distance", 5.4,
                          font_size=19, color=DATA),
            wrapped_label(rf"Levenshtein: \ {D[len(a)][len(b)]} edits for one swap; \ Damerau \ (1964) \ adds the "
                          r"transposition of neighbours as a single edit, \ the commonest slip of all, \ so "
                          r"\texttt{captian} is one edit from \texttt{captain}", 5.4, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.9, -0.3, 0])
        with self.voiceover(
            "The channel needs a distance between a typo and a word. <bookmark mark='a'/> It is the edit "
            "distance of Part 21: the fewest insertions, deletions and substitutions turning one string into the "
            "other. <bookmark mark='b'/> Lay one word across the top and the other down the side. Each cell is the "
            "cheapest of its three neighbours plus one, or its diagonal neighbour for free when the letters agree. "
            "That is the dynamic programming of Part 19, filled row by row. <bookmark mark='c'/> The corner says "
            f"{D[len(a)][len(b)]}: a single swap of neighbouring letters costs two substitutions. Damerau "
            "observed in 1964 that transposing two neighbours is among the commonest slips, and counted it as one "
            "edit."
        ) as vo:
            self.play(FadeIn(head), FadeIn(top), FadeIn(side), FadeIn(border))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            self.play(LaggedStart(*[FadeIn(c) for c in inner], lag_ratio=0.06), run_time=4)
            vo.wait_until("c")
            self.play(Create(ring), FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def bktree(self):
        sp = load("spell")
        nodes, kids = bk_tree(BK_WORDS)
        order = list(range(len(nodes)))
        pos = tree_layout({n: nodes[n][1] for n in order}, order, dx=1.25, dy=1.05, top=1.9)
        head = label(r"BK-trees: \ pruning by the triangle inequality", font_size=36).to_edge(UP, buff=0.3)
        shift = LEFT * 3.4
        boxes = {n: tag_box(nodes[n][0], color=GREY_A, size=16, h=0.42).move_to(pos[n]).shift(shift) for n in order}
        edges, elabs = VGroup(), VGroup()
        for n in order[1:]:
            p = nodes[n][1]
            ln = Line(boxes[p].get_bottom(), boxes[n].get_top(), color=GREY_C, stroke_width=1.5)
            edges.add(ln)
            elabs.add(label(str(nodes[n][2]), font_size=16, color=HEAD).move_to(ln.get_center() + LEFT * 0.18))
        visited, found, pruned = bk_search(nodes, kids, BK_QUERY, BK_TOL)
        q = tag_box(BK_QUERY, color=NO, size=17, h=0.44)
        q_l = label(rf"look up \texttt{{{BK_QUERY}}}, \ tolerance {BK_TOL}", font_size=19, color=NO)
        VGroup(q_l, q).arrange(RIGHT, buff=0.2).to_edge(DOWN, buff=0.4).set_x(-3.4)

        def subtree(n):
            out = [n]
            for c in kids[n].values():
                out += subtree(c)
            return out
        dead = [m for p in pruned for m in subtree(p)]
        illus = label(r"illustrative vocabulary", font_size=16, color=GREY_B).next_to(q_l, UP, buff=0.25)
        notes = VGroup(
            wrapped_label(r"each child hangs under its parent by its edit distance to it", 4.8, font_size=19,
                          color=WHITE),
            wrapped_label(rf"at a node $d$ edits from the query, \ only children on edges $d - {BK_TOL}$ to "
                          rf"$d + {BK_TOL}$ can hold a match: \ edit distance is a metric, \ so the triangle "
                          r"inequality rules the rest out", 4.8, font_size=19, color=HEAD),
            wrapped_label(rf"on the novels' {sp['vocab']:,} words, \ tolerance 2: \ "
                          rf"{min(r['distance_calls'] for r in sp['rows']):,} to "
                          rf"{max(r['distance_calls'] for r in sp['rows']):,} distances per typo, \ about a third: \ "
                          r"pruning is weak when the tolerance is large against the word", 4.8, font_size=19,
                          color=DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.3, 0.0, 0])
        with self.voiceover(
            "Comparing a typo with every word in the vocabulary is wasteful. Burkhard and Keller's tree of 1973 "
            "does better. <bookmark mark='a'/> Each word hangs below its parent on an edge labelled with the edit "
            "distance between them. <bookmark mark='b'/> To find words within one edit of a typo, compute its "
            "distance d to the root. Because edit distance is a metric, the triangle inequality says that a match "
            "can only lie under the edges labelled d minus one to d plus one, and every other subtree is skipped "
            "unvisited. <bookmark mark='c'/> On the novels' vocabulary, at a tolerance of two, our tree still "
            "computes about a third of all the distances: pruning is weak when the tolerance is large compared "
            "with the words themselves."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(b) for b in boxes.values()], Create(edges))
            vo.wait_until("a")
            self.play(FadeIn(elabs), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(q_l), FadeIn(q), FadeIn(illus), FadeIn(notes[1]))
            for n in visited:
                col = YES if n in found else GREY_B
                self.play(boxes[n][0].animate.set_stroke(col, width=3), boxes[n][1].animate.set_color(col),
                          run_time=0.4)
            self.play(*[boxes[m].animate.set_opacity(0.25) for m in dead])
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def corrections(self):
        sp = load("spell")
        head = label(r"Correcting typos with the novels", font_size=36).to_edge(UP, buff=0.3)
        rows = [[r["typed"], f"{r['candidates']}", r["correction"], f"{r['distance_calls']:,}"] for r in sp["rows"]]
        bad = [k for k, r in enumerate(sp["rows"]) if r["typed"] == "recieve"]
        colors = [[NO if k in bad else WHITE] * 4 for k in range(len(rows))]
        tab = grid_table([r"typed", r"words within 2 edits", r"chosen", r"distances computed"], rows,
                         widths=[2.0, 3.0, 2.2, 3.0], row_h=0.44, font_size=19, colors=colors, mono_cols=(0, 2))
        tab.next_to(head, DOWN, buff=0.45)
        for k in bad:
            for c in tab.cells[k + 1]:
                c.set_color(NO)
        same = next(r for r in sp["rows"] if r["typed"] == r["correction"])
        lines = VGroup(
            wrapped_label(rf"\texttt{{{same['typed']}}} is a word: \ of its {same['candidates']} neighbours, \ "
                          r"none is common enough to pay for an edit, \ so it stays", 12.4, font_size=20, color=YES),
            wrapped_label(r"\texttt{recieve}: \ \texttt{relieve} is one substitution away, \ \texttt{receive} two, "
                          r"\ because the swapped \textit{ie} costs two edits under Levenshtein; \ Damerau's "
                          r"transposition, \ or a channel learned from real slips, \ fixes it", 12.4, font_size=20,
                          color=NO),
            wrapped_label(r"real correctors add context \ (\textit{I will recieve the letter}), \ and query logs: "
                          r"\ what people retyped next", 12.4, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, DOWN, buff=0.6).set_x(0)
        with self.voiceover(
            f"Here is the whole corrector on seven inputs, with a vocabulary of {sp['vocab']:,} words from the "
            "novels. <bookmark mark='a'/> Misspelt captain, Elizabeth, separate, monster and London are all "
            f"repaired. <bookmark mark='b'/> {same['typed'].capitalize()} is already a word: it has "
            f"{same['candidates']} neighbours within two edits, but none is common enough to pay for the change, "
            "so it stays. <bookmark mark='c'/> And one is wrong. Recieve becomes relieve, because relieve is one "
            "substitution away while receive, under plain edit distance, is two. Damerau's transposition, or a "
            "channel learned from real slips, would put it right. <bookmark mark='d'/> Real correctors also read "
            "the surrounding words, and learn from query logs what people retyped next."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.cells[0][0]), FadeIn(tab.cells[0][1]), FadeIn(tab.cells[0][2]),
                      FadeIn(tab.cells[0][3]), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*tab.cells[k])) for k in range(1, len(rows) + 1)],
                                  lag_ratio=0.25), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(*[Indicate(c, color=NO) for k in bad for c in tab.cells[k + 1]], FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
        self.wait(0.4)
        self.clear_scene()

    def complete(self):
        comp = load("spell")["complete"]
        prefix = "ca"
        words = comp[prefix]
        head = label(r"Autocomplete: \ the best $k$ below a trie node", font_size=36).to_edge(UP, buff=0.3)
        # the trie of the five completions: nodes are prefixes
        pref = [""]
        for w in words:
            for i in range(1, len(w) + 1):
                if w[:i] not in pref:
                    pref.append(w[:i])
        parent = {p: (p[:-1] if p else None) for p in pref}
        order = [""] + [p for p in pref if p]
        idx = {p: k for k, p in enumerate(order)}
        pos = tree_layout({idx[p]: (idx[parent[p]] if parent[p] is not None else None) for p in order},
                          list(range(len(order))), dx=1.35, dy=0.68, top=2.45)
        shift = LEFT * 3.6
        circ = {}
        for p in order:
            c = Circle(radius=0.24, stroke_color=GREY_B, stroke_width=1.5, fill_color=BG, fill_opacity=1)
            c.move_to(pos[idx[p]]).shift(shift)
            t = mono(p[-1] if p else "*", size=18, color=WHITE).move_to(c)
            circ[p] = VGroup(c, t)
        edges = VGroup(*[Line(circ[parent[p]].get_center(), circ[p].get_center(), color=GREY_D, stroke_width=1.5)
                         for p in order if p])
        path = [p for p in order if p and prefix.startswith(p)]
        ends = VGroup()
        for r, w in enumerate(words):
            ring = Circle(radius=0.31, stroke_color=YES, stroke_width=3).move_to(circ[w])
            leaf = not any(q != w and q.startswith(w) for q in order)
            rk = VGroup(label(rf"{r + 1}", font_size=18, color=YES), mono(w, size=16, color=YES)).arrange(
                RIGHT, buff=0.1).next_to(ring, DOWN if leaf else LEFT, buff=0.08)
            ends.add(VGroup(ring, rk))
        rows = [[p, ", ".join(ws)] for p, ws in comp.items()]
        tab = grid_table([r"typed", r"top five completions, \ by count in the novels"], rows, widths=[1.1, 5.6],
                         row_h=0.42, font_size=18, mono_cols=(0, 1))
        tab.move_to([3.35, 1.2, 0])
        lines = VGroup(
            wrapped_label(r"store at every node the best count anywhere below it; \ a priority queue then "
                          r"expands the most promising node first, \ and the $k$ best come out in about $k$ times "
                          r"the depth steps \ (tries: \ Part 17)", 6.6, font_size=19, color=WHITE),
            wrapped_label(r"or keep the top $k$ at each node: \ memory bought for speed; \ real systems rank by "
                          r"query logs and forgive a typo in the prefix", 6.6, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.35, -1.85, 0])
        with self.voiceover(
            "Better still is to catch the query before it is finished. <bookmark mark='a'/> Autocompletion is a "
            "walk down a trie, the tree of prefixes from Part 17. Type c, a, and every word below that node is a "
            "candidate. <bookmark mark='b'/> The best five, ranked by their counts in the novels, are can, came, "
            "called, cannot and can't. <bookmark mark='c'/> To find them without visiting the whole subtree, store "
            "at every node the best count anywhere beneath it. A priority queue then always expands the most "
            "promising node, and the top k come out after about k times the depth steps, however big the "
            "vocabulary. <bookmark mark='d'/> Or store the top few at each node outright, buying speed with memory. "
            "Real engines rank completions by what people search for."
        ) as vo:
            self.play(FadeIn(head), Create(edges), *[FadeIn(c) for c in circ.values()])
            vo.wait_until("a")
            for p in path:
                self.play(circ[p][0].animate.set_stroke(HEAD, width=3), circ[p][1].animate.set_color(HEAD),
                          run_time=0.4)
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(e) for e in ends], lag_ratio=0.3), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(lines[0]))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (LAM,)
