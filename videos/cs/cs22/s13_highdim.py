from __future__ import annotations

import random

from explainer.cs import *  # noqa: F403
from videos.cs.cs22.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)


class HighDim(VoiceoverScene):
    def construct(self):
        self.card()
        self.curse()
        self.hnsw()
        self.measured()

    def card(self):
        card = chapter_card(12, r"High dimensions", r"Why does geometry break in a thousand dimensions?",
                            lit=(1998, 2016), extra=((1998, r"Indyk--Motwani LSH"), (2016, r"HNSW")), part=PART)
        with self.voiceover("Chapter twelve. High dimensions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def curse(self):
        d = load("highdim")
        head = label(r"The curse of dimensionality", font_size=34).to_edge(UP, buff=0.35)
        rows = [[str(r["d"]), f"{r['ratio']:.2f}" if r["ratio"] < 100 else words(round(r["ratio"]))] for r in d["conc"]]
        t1 = grid_table([r"dimension $d$", r"farthest $/$ nearest"], rows, widths=[2.2, 2.6], row_h=0.38, font_size=21,
                        mono_cols=(), colors=[[WHITE, LAM]] * len(rows))
        cap1 = label(r"2,000 random points in the unit cube, \\ distances from one random query", font_size=19,
                     color=GREY_A)
        VGroup(t1, cap1.next_to(t1, DOWN, buff=0.2)).to_edge(LEFT, buff=0.7).next_to(head, DOWN, buff=0.4).to_edge(
            LEFT, buff=0.7)
        kd = d["kd"]
        bars = VGroup()
        for k, r in enumerate(kd):
            h = 4.0 * r["share"]
            b = Rectangle(width=0.55, height=max(h, 0.02), stroke_width=0, fill_color=NO if r["share"] > 0.5 else YES,
                          fill_opacity=0.85)
            b.move_to([1.0 + k * 0.95, -2.3 + b.height / 2, 0])
            bars.add(VGroup(b, mono(str(r["d"]), 18, WHITE).next_to(b, DOWN, buff=0.1).set_y(-2.55),
                            label(f"{100 * r['share']:.2f}\\%" if r["share"] < 0.01 else (f"{100 * r['share']:.1f}\\%" if r["share"] < 0.1
                                  else f"{100 * r['share']:.0f}\\%"),
                                  font_size=18, color=GREY_A).next_to(b, UP, buff=0.08)))
        base = Line([0.6, -2.3, 0], [6.6, -2.3, 0], color=GREY_B, stroke_width=1.5)
        cap2 = label(rf"share of a kd-tree's nodes visited \\ to find one nearest neighbour \ ($n = {words(d['kd_n'])}$)",
                     font_size=19, color=GREY_A).move_to([3.6, 2.3, 0])
        dl = label(r"dimension $d$", font_size=18, color=GREY_A).move_to([3.6, -3.05, 0])
        with self.voiceover(
            "Everything so far lives in the plane, but the questions of chapters ten and eleven are asked of data with "
            "hundreds of dimensions: images, documents and the embeddings of the AI series. <bookmark mark='a'/> "
            "There, geometry behaves strangely. Take two thousand random points in a cube and measure their "
            "distances from a random query. In two dimensions the farthest point is a hundred times farther than the "
            "nearest; in a hundred dimensions, less than one and a half times; in a thousand, eleven percent. Almost "
            "every point is almost equally far away, and 'nearest' barely means anything. <bookmark mark='b'/> "
            "That ruins the kd-tree. Its pruning works only when the query's ball is small compared with the cells. "
            "For twenty thousand points, finding one nearest neighbour visits six hundredths of a percent of the nodes in "
            "two dimensions, half of them in twelve, and every single one in twenty-four: worse than a scan. "
            "<bookmark mark='c'/> Exact nearest neighbours in high dimensions seem to need either exponential space "
            "or nearly linear time, and the frontier chapter returns to that."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*t1.cells[0])), FadeIn(t1.rule), FadeIn(cap1),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in t1.cells[1:]], lag_ratio=0.2), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(cap2), Create(base), FadeIn(dl),
                      LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.25), run_time=3.0)
            vo.wait_until("c")
            self.play(Indicate(bars[-1], color=NO))
        self.wait(0.3)
        self.clear_scene()

    def hnsw(self):
        d = load("highdim")
        head = label(r"Navigable small worlds", font_size=34).to_edge(UP, buff=0.3)
        rng = random.Random(3)
        layers = VGroup()
        nodes = {}
        counts = [3, 7, 16]
        ys = [1.8, 0.2, -1.6]
        pts0 = [(rng.uniform(-6.2, 0.4), rng.uniform(-0.45, 0.45)) for _ in range(counts[2])]
        chosen = [pts0]
        for L in (1, 0):
            chosen.insert(0, rng.sample(chosen[0], counts[L]))
        for L, (pts, y) in enumerate(zip(chosen, ys)):
            plane = Polygon([-6.6, y - 0.6, 0], [0.8, y - 0.6, 0], [1.4, y + 0.6, 0], [-6.0, y + 0.6, 0],
                            color=GREY_D, stroke_width=1).set_fill(GREY_E, 0.25)
            ds = VGroup(*[Dot([x, y + yy, 0], radius=0.06, color=[HEAD, LAM, DATA][L]) for x, yy in pts])
            es = VGroup()
            srt = sorted(pts)
            for i in range(len(srt) - 1):
                es.add(Line([srt[i][0], y + srt[i][1], 0], [srt[i + 1][0], y + srt[i + 1][1], 0], color=GREY_B,
                            stroke_width=1.2))
            for i in range(len(srt) - 2):
                if rng.random() < 0.5:
                    es.add(Line([srt[i][0], y + srt[i][1], 0], [srt[i + 2][0], y + srt[i + 2][1], 0], color=GREY_B,
                                stroke_width=1.0))
            layers.add(VGroup(plane, es, ds))
            nodes[L] = [(x, y + yy) for x, yy in pts]
        q = (-1.2, -1.6 + 0.3)
        qd = Star(n=5, outer_radius=0.14, inner_radius=0.06, color=NO, fill_opacity=1).move_to([q[0], q[1], 0])
        path = []
        cur = nodes[0][0]
        for L in range(3):
            if L > 0:
                path.append(((cur[0], cur[1]), (cur[0], cur[1] - (ys[L - 1] - ys[L]))))
                cur = (cur[0], cur[1] - (ys[L - 1] - ys[L]))
            best = min(nodes[L], key=lambda p: (p[0] - q[0]) ** 2)
            path.append((cur, best))
            cur = best
        arrows = VGroup(*[Arrow([a[0], a[1], 0], [b[0], b[1], 0], buff=0.06, color=NO, stroke_width=3,
                                max_tip_length_to_length_ratio=0.15) for a, b in path if np.hypot(a[0] - b[0], a[1] - b[1]) > 0.05])
        side = VGroup(
            label(r"build a graph: \ each point linked to a few \\ near neighbours, \ in diverse directions",
                  font_size=21, color=WHITE),
            label(r"search greedily: \ step to whichever neighbour \\ is closer to the query", font_size=21,
                  color=LAM),
            label(r"HNSW \ (Malkov and Yashunin, 2016): \\ sparser layers above, \ like a skip list \\ (Part 17)",
                  font_size=21, color=HEAD),
            label(rf"ours: \ {words(d['nsw_n'])} points, \ 16 dimensions; \\ layers of " +
                  r", \ ".join(words(x) for x in d["levels"]), font_size=21, color=DATA),
            label(r"no worst-case guarantee, \ but superb in practice: \\ vector databases, \ retrieval for "
                  r"language models", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if side.width > 5.4:
            side.width = 5.4
            side.to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Two ideas rescue nearest neighbours by giving up exactness. Part 20's locality-sensitive hashing is one: "
            "hash so that near points tend to collide. The other, which dominates practice today, is a graph. "
            "<bookmark mark='a'/> Link each point to a few of its near neighbours, chosen to point in different "
            "directions. <bookmark mark='b'/> To answer a query, start anywhere and keep stepping to whichever "
            "neighbour is closer to the query, keeping a short list of the best seen. <bookmark mark='c'/> Yury "
            "Malkov and Dmitry Yashunin's hierarchical version adds sparser layers on top, like the express lanes of "
            "a skip list: a few long hops near the top, then a careful search at the bottom. <bookmark mark='d'/> We "
            "built one over twenty thousand points in sixteen dimensions, clustered around two hundred centres; it "
            "has four layers. <bookmark mark='e'/> There is no worst-case theorem for these graphs, but they are what "
            "vector databases run, behind retrieval for language models."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(l_) for l_ in layers[::-1]], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), Indicate(layers[2][1], color=WHITE))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(qd))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("highdim")
        head = label(r"Recall of the true 10 nearest, \ against distance computations", font_size=30).to_edge(UP, buff=0.35)
        rows = []
        for a, b in zip(d["nsw"], d["hnsw"]):
            rows.append([str(a["ef"]), f"{100 * a['recall']:.1f}\\%", f"{a['evals']:.0f}", f"{100 * b['recall']:.1f}\\%",
                         f"{b['evals']:.0f}"])
        tab = grid_table([r"beam width", r"one layer, \ nearest links", r"computations", r"HNSW, \ diverse links",
                          r"computations"], rows, widths=[2.0, 3.4, 2.2, 3.2, 2.2], row_h=0.48, font_size=21,
                         mono_cols=(), colors=[[WHITE, NO, GREY_A, YES, GREY_A]] * len(rows))
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        notes = VGroup(
            label(rf"brute force: \ {words(d['nsw_n'])} computations per query, \ always right", font_size=22,
                  color=WHITE),
            label(r"linking each point to its nearest neighbours only strands searches inside clusters", font_size=22,
                  color=NO),
            label(r"the diversity rule keeps links between clusters: \ 99.7\% recall for 1\% of the work", font_size=22,
                  color=YES),
            label(r"in practice: \ FAISS, \ pgvector, \ Milvus, \ Lucene; \ the retrieval in \textit{AI, Built}",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.28).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "Here is what the layers and the choice of links buy, on a hundred queries. <bookmark mark='a'/> Brute "
            "force computes all twenty thousand distances for every query. <bookmark mark='b'/> A single-layer graph "
            "that links each point to its plain nearest neighbours does badly on clustered data: links stay inside "
            "clusters, and greedy searches get stuck in the wrong one: with a narrow beam it finds fewer than half "
            "of the true neighbours, and even its widest beam costs over six hundred computations. <bookmark mark='c'/> With HNSW's rule, keep a neighbour only if it is closer to the new "
            "point than to the neighbours already kept, so links fan out and bridge clusters, the layered graph finds "
            "ninety-nine point seven percent of the true ten nearest with under two hundred distance computations, "
            "a hundredth of brute force. <bookmark mark='d'/> Libraries like FAISS and pgvector run exactly this, "
            "under the retrieval systems that feed language models."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]), *[FadeIn(VGroup(*r[:3])) for r in tab.cells[1:]])
            vo.wait_until("c")
            self.play(FadeIn(notes[2]), *[FadeIn(VGroup(*r[3:])) for r in tab.cells[1:]])
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()
