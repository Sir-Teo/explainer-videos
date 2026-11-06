from __future__ import annotations

import random

from explainer.cs import *  # noqa: F403
from videos.cs.cs47.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, bar_chart, grid_table, load,
                                   module_box, tag_box)

RRF_K = 60          # Cormack, Clarke and Buettcher (2009)


def _pts(n, seed):
    rng = random.Random(seed)
    return [(rng.random(), rng.random()) for _ in range(n)]


def _d2(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


class Dense(VoiceoverScene):
    def construct(self):
        self.card()
        self.mismatch()
        self.pq()
        self.pq_cost()
        self.hnsw()
        self.hybrid()

    def card(self):
        card = chapter_card(13, r"Dense retrieval", r"How do you find a passage that shares no words with the query?",
                            lit=(2011, 2018, 2020),
                            extra=((2011, r"J\'egou, \ Douze and Schmid: \ product quantization"),
                                   (2018, r"Malkov and Yashunin: \ HNSW"), (2020, r"Karpukhin et al.: \ DPR")),
                            part=PART)
        with self.voiceover("Chapter thirteen. Dense retrieval."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def mismatch(self):
        ix = load("index")
        dim = load("pq")["dim"]
        float_bytes = load("pq")["rows"][0]["float_bytes"]
        head = label(r"Meaning as geometry", font_size=36).to_edge(UP, buff=0.3)
        # an illustrative embedding space: three clusters of passages and a query
        rng = random.Random(3)
        centres = [((-5.0, 0.9), DATA, r"the sea"), ((-2.2, -0.9), LAM, r"marriage"),
                   ((-5.0, -1.6), KERN, r"crime")]
        dots, names = VGroup(), VGroup()
        for (cx, cy), c, nm in centres:
            for _ in range(14):
                dots.add(Dot([cx + rng.gauss(0, 0.45), cy + rng.gauss(0, 0.35), 0], radius=0.05, color=c))
            names.add(label(nm, font_size=17, color=c).move_to([cx, cy + 0.95, 0]))
        frame = Rectangle(width=6.0, height=4.6, stroke_color=GREY_D, stroke_width=1).move_to([-3.75, -0.2, 0])
        qpos = [-4.7, 0.8, 0]
        q = Star(n=5, outer_radius=0.14, color=HEAD, fill_opacity=1).move_to(qpos)
        q_l = tag_box(r"a voyage on the ocean", color=HEAD, size=14, h=0.36).next_to(q, RIGHT, buff=0.6)
        near = sorted(dots, key=lambda d: (d.get_x() - qpos[0]) ** 2 + (d.get_y() - qpos[1]) ** 2)[:10]
        rings = VGroup(*[Circle(radius=0.1, color=HEAD, stroke_width=2).move_to(d) for d in near])
        ill = label(r"illustrative space", font_size=16, color=GREY_B).next_to(frame, DOWN, buff=0.1).align_to(
            frame, LEFT)
        # two towers
        enc_q = module_box(r"encoder", YES, w=1.6, h=0.55)
        enc_p = module_box(r"encoder", YES, w=1.6, h=0.55)
        qin = tag_box(r"query", color=HEAD, size=15, h=0.38)
        pin = tag_box(r"passage", color=DATA, size=15, h=0.38)
        qv = label(r"$\mathbf{q}$", font_size=24, color=HEAD)
        pv = label(r"$\mathbf{p}$", font_size=24, color=DATA)
        t1 = VGroup(qin, enc_q, qv).arrange(DOWN, buff=0.35)
        t2 = VGroup(pin, enc_p, pv).arrange(DOWN, buff=0.35)
        towers = VGroup(t1, t2).arrange(RIGHT, buff=1.0).move_to([3.6, 1.45, 0])
        arrs = VGroup(*[Arrow(a.get_bottom(), b.get_top(), buff=0.05, color=GREY_B, stroke_width=2,
                              max_tip_length_to_length_ratio=0.3) for t in (t1, t2) for a, b in zip(t, t[1:])])
        dot = label(r"score $= \mathbf{q} \cdot \mathbf{p}$", font_size=21, color=WHITE).next_to(towers, DOWN,
                                                                                               buff=0.25)
        notes = VGroup(
            wrapped_label(r"BM25 scores zero for a passage that says \textit{sea} and \textit{ship} when the query "
                          r"says \textit{ocean} and \textit{voyage}", 6.0, font_size=19, color=NO),
            wrapped_label(rf"our stand-in vectors: \ tf-idf projected to {dim} dimensions by a random matrix \ "
                          rf"(Part 20); \ {ix['docs']:,} passages $\times$ {float_bytes} bytes; \ a trained encoder "
                          r"\ (\textit{AI, Built} \ Part 24) \ would also place synonyms together", 6.0, font_size=19,
                          color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, -1.85, 0])
        with self.voiceover(
            "Everything so far matches words. <bookmark mark='a'/> A query about a voyage on the ocean scores zero "
            "against a passage about a ship at sea, because they share no terms. <bookmark mark='b'/> Dense "
            "retrieval moves the problem into geometry. An encoder, the embeddings of AI, Built Part 24, maps "
            "every passage to a vector, once, offline; at query time it maps the query too, and relevance is a "
            "dot product. <bookmark mark='c'/> Related passages land near each other, and retrieval "
            "becomes nearest-neighbour search. <bookmark mark='d'/> Our own vectors are a stand-in: tf-idf "
            f"projected down to {dim} dimensions by a random matrix, the trick of Part 20. They keep the geometry "
            "of words, not of meaning; a trained encoder, such as Karpukhin and colleagues' of 2020, learns "
            "meaning from examples."
        ) as vo:
            self.play(FadeIn(head), Create(frame), FadeIn(dots), FadeIn(names), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(t1), FadeIn(t2), *[GrowArrow(a) for a in arrs], FadeIn(dot))
            vo.wait_until("c")
            self.play(GrowFromCenter(q), FadeIn(q_l))
            self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.1))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def pq(self):
        p = load("pq")
        dim = p["dim"]
        row8 = next(r for r in p["rows"] if r["m"] == 8)
        m = row8["m"]
        s = dim // m
        head = label(r"Product quantization", font_size=36).to_edge(UP, buff=0.3)
        cw = 0.18
        rng = random.Random(5)
        cells = VGroup(*[Rectangle(width=cw, height=0.5, stroke_width=0.5, stroke_color=BG,
                                   fill_color=interpolate_color(DATA, LAM, rng.random()), fill_opacity=0.9)
                         for _ in range(dim)]).arrange(RIGHT, buff=0)
        cells.next_to(head, DOWN, buff=0.75)
        top_l = label(rf"one passage vector: \ {dim} floats, \ {row8['float_bytes']} bytes", font_size=19,
                      color=DATA).next_to(cells, UP, buff=0.15)
        groups = VGroup(*[VGroup(*cells[j * s:(j + 1) * s]) for j in range(m)])
        codes = [rng.randrange(256) for _ in range(m)]
        braces = VGroup(*[Brace(g, DOWN, buff=0.05, color=GREY_B) for g in groups])
        code_boxes = VGroup(*[tag_box(f"{c}", color=HEAD, size=16, w=s * cw - 0.06, h=0.42) for c in codes])
        for b, g in zip(code_boxes, groups):
            b.next_to(g, DOWN, buff=0.55)
        code_l = wrapped_label(rf"{m} sub-vectors of {s} dimensions, \ each replaced by the number of its nearest "
                               rf"centroid \ (one byte: \ 256 centroids): \ {row8['bytes']} bytes", 12.4,
                               font_size=19, color=HEAD).next_to(code_boxes, DOWN, buff=0.25)
        notes = VGroup(
            wrapped_label(r"the centroids: \ $k$-means clustering in each sub-space, \ trained once",
                          5.9, font_size=19, color=WHITE),
            wrapped_label(rf"$256^{{{m}}}$ possible codes from only ${m} \times 256$ centroids: \ the product of "
                          r"the sub-spaces' codebooks", 5.9, font_size=19, color=LAM),
            wrapped_label(rf"to search, \ compute a table of the query's distance to every centroid, \ "
                          rf"${m} \times 256$ numbers; \ each passage's distance is then {m} lookups and adds", 5.9,
                          font_size=19, color=YES),
        )
        notes[0].next_to(code_l, DOWN, buff=0.4).to_edge(LEFT, buff=0.5)
        notes[1].next_to(notes[0], DOWN, buff=0.3).align_to(notes[0], LEFT)
        notes[2].next_to(code_l, DOWN, buff=0.4).to_edge(RIGHT, buff=0.5)
        ill = label(r"codes illustrative", font_size=16, color=GREY_B).next_to(top_l, RIGHT, buff=0.5)
        with self.voiceover(
            f"A float vector per passage costs {row8['float_bytes']} bytes; a billion passages would need "
            "hundreds of gigabytes. Jegou, Douze and Schmid's product quantization, of 2011, shrinks it. "
            f"<bookmark mark='a'/> Cut each vector into {m} pieces of {s} dimensions. <bookmark mark='b'/> In each "
            "piece's space, cluster all passages into two hundred and fifty-six groups, and store only the number "
            f"of the nearest centre: one byte. The vector becomes {row8['bytes']} bytes. "
            "<bookmark mark='c'/> Two hundred and fifty-six choices in each of eight places give an astronomical "
            "number of codes, from very few centres. <bookmark mark='d'/> Searching needs no decompression: "
            "compute the query's distance to every centre once, and each passage's distance is a sum of eight "
            "table lookups."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells), FadeIn(top_l))
            vo.wait_until("a")
            self.play(*[g.animate.shift(RIGHT * (j - (m - 1) / 2) * 0.12) for j, g in enumerate(groups)])
            for b, g in zip(braces, groups):
                b.become(Brace(g, DOWN, buff=0.05, color=GREY_B))
            self.play(FadeIn(braces))
            vo.wait_until("b")
            self.play(*[TransformFromCopy(g, b) for g, b in zip(groups, code_boxes)], run_time=1.5)
            self.play(FadeIn(code_l), FadeIn(ill), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def pq_cost(self):
        p = load("pq")
        rows = p["rows"]
        head = label(r"What the bytes buy", font_size=36).to_edge(UP, buff=0.3)
        vals = [r["recall10"] for r in rows]
        names = [rf"{r['bytes']} bytes" for r in rows]
        chart = bar_chart(vals, names, [GREY_B, DATA, LAM, YES], height=3.2, bar_w=0.85, gap=0.55, vmax=1.0,
                          fmt_=lambda v: rf"{100 * v:.0f}\%", font_size=19)
        chart.move_to([-3.4, -0.3, 0])
        exact = DashedLine(chart.bars[0].get_bottom() + UP * 3.2 + LEFT * 0.5,
                           chart.bars[-1].get_bottom() + UP * 3.2 + RIGHT * 0.5, color=GREY_B)
        cap = label(r"recall of the true top ten, \ per query", font_size=19, color=GREY_A).next_to(exact, UP,
                                                                                                    buff=0.25)
        exact_l = label(rf"exact: \ {rows[0]['float_bytes']} bytes", font_size=17, color=GREY_B).next_to(
            exact, RIGHT, buff=0.1)
        tab = grid_table([r"bytes", r"squared error"], [[f"{r['bytes']}", f"{r['mse']:.2f}"] for r in rows],
                         widths=[1.4, 2.2], row_h=0.42, font_size=19, mono_cols=())
        tab.move_to([3.7, 1.35, 0])
        notes = VGroup(
            wrapped_label(r"our vectors have unit length, \ so an error of 1 would be as large as the vector "
                          r"itself", 5.4, font_size=19, color=GREY_A),
            wrapped_label(r"so compressed codes only shortlist: \ an inverted file picks a few clusters to scan, \ "
                          r"and the shortlist is re-ranked with exact vectors \ (as in Faiss)", 5.4, font_size=19,
                          color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            f"How much does compression cost? We measured it on {p['dim']}-dimensional passage vectors with a "
            "hundred queries. <bookmark mark='a'/> With two bytes per passage, PQ finds "
            f"{100 * rows[0]['recall10']:.0f} percent of the true ten nearest; with eight bytes "
            f"{100 * rows[2]['recall10']:.0f} percent; with sixteen, {100 * rows[3]['recall10']:.0f}, at a "
            f"sixteenth of the {rows[0]['float_bytes']} bytes of the exact vector. <bookmark mark='b'/> The squared "
            f"error falls from {rows[0]['mse']:.2f} to {rows[-1]['mse']:.2f} of a unit vector. <bookmark mark='c'/> "
            "So real systems use the codes only for a shortlist: an inverted file picks a few clusters to scan, "
            "the codes rank their contents, and the best are re-scored exactly, as in the Faiss library."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap), FadeIn(chart.names), Create(exact), FadeIn(exact_l))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in chart.bars], lag_ratio=0.2), FadeIn(chart.vals),
                      FadeIn(chart[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(tab), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def hnsw(self):
        h = load("hnsw")
        lv = {int(k): v for k, v in h["levels"].items()}
        top = max(lv)
        head = label(r"HNSW: \ descending a navigable graph", font_size=36).to_edge(UP, buff=0.3)
        W, H, skew = 4.6, 0.85, 1.3
        x0 = -6.4
        ys = {L: -2.75 + (L) * 1.3 for L in range(top + 1)}
        shown = {top: 4, 2: 10, 1: 22, 0: 48}           # dots drawn per level (illustrative layout)
        pts = _pts(shown[0], 11)
        qp = (0.82, 0.25)

        def at(L, uv):
            u, v = uv
            return [x0 + u * W + v * skew, ys[L] + v * H, 0]
        planes, dots_by = VGroup(), {}
        for L in range(top + 1):
            pl = Polygon(at(L, (0, 0)), at(L, (1, 0)), at(L, (1, 1)), at(L, (0, 1)), stroke_color=GREY_D,
                         stroke_width=1.2, fill_color=GREY_E, fill_opacity=0.25)
            planes.add(pl)
            dots_by[L] = VGroup(*[Dot(at(L, pts[i]), radius=0.045, color=GREY_A) for i in range(shown[L])])
        lab = VGroup(*[label(rf"level {L}: \ {lv[L]:,} points", font_size=17, color=GREY_A).next_to(
            at(L, (1, 0.5)), RIGHT, buff=0.15) for L in range(top + 1)])
        qs = VGroup(*[Star(n=5, outer_radius=0.1, color=HEAD, fill_opacity=1).move_to(at(L, qp))
                      for L in range(top + 1)])
        # greedy descent: on each level walk to the neighbour closest to the query, then drop a level
        path, drops = {L: VGroup() for L in range(top + 1)}, VGroup()
        cur = 0
        for L in range(top, -1, -1):
            cand = list(range(shown[L]))
            while True:
                nbrs = sorted((c for c in cand if c != cur), key=lambda c: _d2(pts[c], pts[cur]))[:4]
                best = min(nbrs + [cur], key=lambda c: _d2(pts[c], qp))
                if best == cur:
                    break
                path[L].add(Line(at(L, pts[cur]), at(L, pts[best]), color=YES, stroke_width=3))
                cur = best
            if L > 0:
                drops.add(DashedLine(at(L, pts[cur]), at(L - 1, pts[cur]), color=YES, stroke_width=1.5))
        entry = Circle(radius=0.11, color=YES, stroke_width=3).move_to(at(top, pts[0]))
        rows = [[f"{r['ef']}", rf"{100 * r['recall10']:.0f}\%", f"{r['distance_calls']:.0f}"] for r in h["rows"]]
        tab = grid_table([r"beam width", r"recall", r"distances"], rows, widths=[1.5, 1.2, 1.5], row_h=0.4,
                         font_size=18, mono_cols=())
        tab.move_to([4.6, 1.5, 0])
        notes = VGroup(
            wrapped_label(rf"{h['n']:,} of our passage vectors; \ brute force computes {h['n']:,} distances per "
                          rf"query; \ building the graph took {h['build_distance_calls']:,}", 4.3, font_size=18,
                          color=WHITE),
            wrapped_label(r"levels thin out geometrically, \ like a skip list: \ long hops high up, \ short ones "
                          r"below \ (Malkov and Yashunin)", 4.3, font_size=18, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, DOWN, buff=0.35)
        ill = label(r"layout illustrative; \ counts ours", font_size=16, color=GREY_B).to_edge(DOWN, buff=0.15).set_x(
            -3.0)
        mid = next(r for r in h["rows"] if r["ef"] == 40)
        frac = {5: "fifth", 6: "sixth", 7: "seventh", 8: "eighth"}.get(round(h["n"] / mid["distance_calls"]),
                                                                      "fraction")
        with self.voiceover(
            "Even compressed, a full scan is too slow at web scale. Malkov and Yashunin's "
            "hierarchical navigable small world graph avoids it. <bookmark mark='a'/> Each point is given a random "
            f"level, and the levels thin out geometrically: in our graph of {h['n']:,} passage vectors, {lv[0]:,} "
            f"live only on the bottom, and just {lv[top]} reach level {top}. Each level links near "
            "neighbours, like a skip list's express lanes. <bookmark mark='b'/> A search enters at the top, "
            "walks greedily towards the query with long hops, drops a level, and repeats with shorter hops, until "
            "a beam search on the bottom level collects the nearest. <bookmark mark='c'/> A wider beam buys recall: "
            f"with a beam of {mid['ef']}, {100 * mid['recall10']:.0f} percent of the true top ten for "
            f"{mid['distance_calls']:.0f} distance computations, about a {frac} of brute force."
        ) as vo:
            self.play(FadeIn(head), FadeIn(planes), FadeIn(ill))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(dots_by[L]) for L in range(top + 1)], lag_ratio=0.3), FadeIn(lab),
                      FadeIn(notes[1]))
            vo.wait_until("b")
            self.play(FadeIn(qs), Create(entry))
            k = 0
            for L in range(top, -1, -1):
                if len(path[L]):
                    self.play(*[Create(sg) for sg in path[L]], run_time=0.8)
                if L > 0:
                    self.play(Create(drops[k]), run_time=0.5)
                    k += 1
            vo.wait_until("c")
            self.play(FadeIn(tab), FadeIn(notes[0]))
        self.wait(0.4)
        self.clear_scene()

    def hybrid(self):
        head = label(r"Words and vectors together", font_size=36).to_edge(UP, buff=0.3)
        lex = ["C", "A", "F", "B", "E"]          # an illustrative BM25 ranking and a dense ranking
        den = ["A", "D", "C", "G", "B"]
        fused = {}
        for lst in (lex, den):
            for r, d in enumerate(lst, 1):
                fused[d] = fused.get(d, 0.0) + 1 / (RRF_K + r)
        order = sorted(fused, key=lambda d: -fused[d])

        def col(title, items, color, x):
            t = label(title, font_size=20, color=color)
            bs = VGroup(*[tag_box(rf"passage {d}", color=color, size=15, h=0.38, w=1.7) for d in items])
            bs.arrange(DOWN, buff=0.12)
            g = VGroup(t, bs).arrange(DOWN, buff=0.2).move_to([x, 0.75, 0])
            return g
        c1 = col(r"BM25", lex, DATA, -5.4)
        c2 = col(r"dense", den, LAM, -3.2)
        fb = VGroup(*[VGroup(tag_box(rf"passage {d}", color=YES, size=15, h=0.38, w=1.7),
                             label(rf"{fused[d]:.4f}", font_size=16, color=GREY_A)).arrange(RIGHT, buff=0.12)
                      for d in order])
        fb.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        ft = label(r"fused", font_size=20, color=YES)
        VGroup(ft, fb).arrange(DOWN, buff=0.2).move_to([0.2, 0.3, 0])
        formula = MathTex(r"\mathrm{RRF}(d) \;=\; \sum_{\text{lists}} \frac{1}{60 + \mathrm{rank}(d)}",
                          font_size=30).move_to([4.3, 2.0, 0])
        notes = VGroup(
            wrapped_label(r"reciprocal rank fusion \ (Cormack, \ Clarke and B\"uttcher, \ 2009): \ only ranks, \ "
                          r"so scores on different scales need no calibration", 4.6, font_size=18, color=WHITE),
            wrapped_label(r"words catch names and rare terms, \ vectors catch paraphrase; \ on new collections BM25 "
                          r"is often still hard to beat \ (BEIR, \ 2021)", 4.6, font_size=18, color=HEAD),
            wrapped_label(r"and the reader may be a model: \ retrieval-augmented generation \ (\textit{AI, Built} \ "
                          r"Part 15) \ puts the top passages into its prompt \ (Chapter 15)", 4.6, font_size=18,
                          color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(formula, DOWN, buff=0.35)
        ill = label(r"rankings illustrative", font_size=16, color=GREY_B).next_to(VGroup(c1, c2), DOWN, buff=0.3)
        with self.voiceover(
            "In practice both kinds run side by side. <bookmark mark='a'/> BM25 gives one "
            "ranking, the dense retriever another, and their scores are on unrelated scales. "
            "<bookmark mark='b'/> Reciprocal rank fusion, from Cormack, Clarke and Buettcher in 2009, ignores the "
            "scores: each list gives a passage one over sixty plus its rank, and the sums decide. Passages both "
            "lists like rise to the top. <bookmark mark='c'/> Words catch names and rare terms; vectors catch "
            "paraphrase. And on collections the encoder never saw, the BEIR benchmark of 2021 found BM25 often "
            "still hard to beat. <bookmark mark='d'/> Increasingly the reader of the top passages is a language "
            "model, as in the retrieval-augmented generation of AI, Built Part 15."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(c1), FadeIn(c2))
            vo.wait_until("b")
            self.play(Write(formula), FadeIn(notes[0]))
            self.play(FadeIn(ft), LaggedStart(*[TransformFromCopy(
                (c1[1][lex.index(d)] if d in lex else c2[1][den.index(d)]), fb[k]) for k, d in enumerate(order)],
                lag_ratio=0.15), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG,)
