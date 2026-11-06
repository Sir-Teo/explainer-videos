from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs47.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load


def tile(title, body, col, w=4.2, h=3.0):
    frame = RoundedRectangle(width=w, height=h, corner_radius=0.15, stroke_color=col, stroke_width=2, fill_color=BG,
                             fill_opacity=1)
    t = label(title, font_size=22, color=col)
    b = wrapped_label(body, w - 0.4, font_size=18, color=GREY_A)
    VGroup(t, b).arrange(DOWN, buff=0.3).move_to(frame)
    return VGroup(frame, t, b)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.graphs()
        self.learned()
        self.generative()
        self.open()

    def card(self):
        card = chapter_card(15, r"Frontier: \ retrieval and its limits", r"What should a search engine return now?",
                            lit=(2018, 2022), extra=((2018, r"HNSW published"),
                                                     (2022, r"generative retrieval")), part=PART)
        with self.voiceover("Chapter fifteen, the frontier. What should a search engine return, now that machines "
                            "can write the answer?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def graphs(self):
        h = load("hnsw")
        rows = h["rows"]
        head = label(r"Fast, \ but without a guarantee", font_size=36).to_edge(UP, buff=0.3)
        x0, y0, xw, yh = -6.0, -2.0, 6.4, 3.8
        xmax = rows[-1]["distance_calls"] * 1.1

        def pt(r):
            return [x0 + r["distance_calls"] / xmax * xw, y0 + (r["recall10"] - 0.6) / 0.4 * yh, 0]
        ax = VGroup(Line([x0, y0, 0], [x0 + xw, y0, 0], color=GREY_C), Line([x0, y0, 0], [x0, y0 + yh, 0],
                                                                              color=GREY_C))
        curve = VMobject(color=KERN, stroke_width=3).set_points_as_corners([pt(r) for r in rows])
        dots = VGroup(*[Dot(pt(r), radius=0.06, color=KERN) for r in rows])
        labs = VGroup(*[label(rf"ef {r['ef']}", font_size=15, color=GREY_B).next_to(d, DOWN, buff=0.08)
                        for r, d in zip(rows, dots)])
        xl = label(rf"distance computations per query \ (brute force: \ {h['n']:,})", font_size=17,
                   color=GREY_B).next_to(ax[0], DOWN, buff=0.35)
        yl = label(r"recall of the true top ten", font_size=17, color=GREY_B).next_to(ax[1], UP, buff=0.1)
        side = VGroup(
            wrapped_label(rf"our HNSW over {h['n']:,} passage vectors: \ {100 * rows[0]['recall10']:.0f}\% recall "
                          rf"for {rows[0]['distance_calls']:.0f} distances, \ {100 * rows[-1]['recall10']:.0f}\% for "
                          rf"{rows[-1]['distance_calls']:.0f}", 5.2, font_size=19, color=KERN),
            wrapped_label(r"graph indexes rule the benchmarks, \ yet have no worst-case guarantee: \ adversarial data "
                          r"can make the greedy walk stall", 5.2, font_size=19, color=WHITE),
            wrapped_label(r"theory has guarantees for other methods \ (locality-sensitive hashing, \ Part 20) \ and "
                          r"new results for navigable graphs; \ closing the gap is open", 5.2, font_size=19,
                          color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Vector search is where theory lags furthest behind practice. <bookmark mark='a'/> Our own layered graph "
            f"finds {100 * rows[0]['recall10']:.0f} percent of the true ten nearest passages with about "
            f"{rows[0]['distance_calls']:.0f} distance computations, and {100 * rows[-1]['recall10']:.0f} percent with "
            f"about {rows[-1]['distance_calls']:.0f}, against {h['n']:,} for brute force. <bookmark mark='b'/> Graph "
            "indexes like this win the benchmarks, but they carry no worst-case guarantee: on adversarial data the "
            "greedy walk can stall far from the answer. <bookmark mark='c'/> Locality-sensitive hashing has "
            "guarantees but loses in practice, and recent theory is only beginning to explain when navigable graphs "
            "work. Closing that gap is open."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(curve), FadeIn(dots), FadeIn(labs), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def learned(self):
        head = label(r"Learned representations", font_size=36).to_edge(UP, buff=0.3)
        tiles = VGroup(
            tile(r"learned sparse", r"a model rewrites each document as weighted terms, \ adding words it does not "
                 r"contain \ (SPLADE, \ 2021): \ the inverted index survives", HEAD),
            tile(r"late interaction", r"one vector per token, \ matched token by token at query time \ (ColBERT, \ "
                 r"2020): \ more precise, \ far larger", DATA),
            tile(r"hybrid", r"BM25 and a dense retriever, \ scores fused: \ words for names and rare terms, \ "
                 r"vectors for meaning", YES),
        ).arrange(RIGHT, buff=0.3).next_to(head, DOWN, buff=0.6)
        foot = wrapped_label(r"open: \ why BM25 remains so hard to beat on new collections, \ and how to make "
                             r"learned retrievers generalize beyond the data they were trained on \ (Part 57)", 12.4,
                             font_size=20, color=NO).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Between words and vectors, research has found middle grounds. <bookmark mark='a'/> Learned sparse "
            "retrieval has a model rewrite each document as weighted terms, including words it does not contain, so "
            "the inverted index of this part keeps working; SPLADE, in 2021, is the best known. "
            "<bookmark mark='b'/> Late interaction keeps a vector for every token and matches them one by one at "
            "query time, as ColBERT did in 2020: more precise, and far larger. <bookmark mark='c'/> And hybrid "
            "systems simply run both, words for names and rare terms, vectors for meaning, and fuse the scores. "
            "<bookmark mark='d'/> A striking open fact: on collections a model has never seen, BM25 is often still "
            "hard to beat. Why, and how to make learned retrievers generalize, are open questions."
        ) as vo:
            self.play(FadeIn(head))
            for mk, t in zip("abc", tiles):
                vo.wait_until(mk)
                self.play(FadeIn(t, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def generative(self):
        head = label(r"Retrieval for machines that write", font_size=36).to_edge(UP, buff=0.3)
        q = RoundedRectangle(width=2.6, height=0.8, corner_radius=0.12, stroke_color=WHITE, fill_color=BG,
                             fill_opacity=1)
        ret = RoundedRectangle(width=2.8, height=0.8, corner_radius=0.12, stroke_color=HEAD, fill_color=BG,
                               fill_opacity=1)
        llm = RoundedRectangle(width=2.8, height=0.8, corner_radius=0.12, stroke_color=LAM, fill_color=BG,
                               fill_opacity=1)
        ans = RoundedRectangle(width=3.2, height=0.8, corner_radius=0.12, stroke_color=YES, fill_color=BG,
                               fill_opacity=1)
        row = VGroup(q, ret, llm, ans).arrange(RIGHT, buff=0.7).next_to(head, DOWN, buff=0.6)
        names = VGroup(label(r"a question", font_size=19).move_to(q),
                       label(r"retriever", font_size=19, color=HEAD).move_to(ret),
                       label(r"language model", font_size=19, color=LAM).move_to(llm),
                       label(r"an answer, \ with citations", font_size=19, color=YES).move_to(ans))
        arrows = VGroup(*[Arrow(row[i].get_right(), row[i + 1].get_left(), buff=0.05, color=GREY_B, stroke_width=2)
                          for i in range(3)])
        lines = VGroup(
            wrapped_label(r"retrieval-augmented generation \ (AI, Built Part 15): \ the engine of this part becomes "
                          r"the memory of a model; \ the user may never see the ten blue links", 12.4, font_size=20,
                          color=WHITE),
            wrapped_label(r"\textbf{generative retrieval} \ (Tay et al., \ 2022): \ the model itself memorizes the "
                          r"corpus and emits document identifiers; \ updating it is the hard part", 12.4,
                          font_size=20, color=LAM),
            wrapped_label(r"open: \ evaluation when the output is a written answer, \ not a ranked list; \ "
                          r"attribution and faithfulness to the sources; \ an index that changes daily", 12.4,
                          font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Finally, search is changing what it is for. <bookmark mark='a'/> In retrieval-augmented generation, "
            "from AI, Built, an engine like ours finds passages and a language model writes an answer from them, "
            "with citations. The engine becomes a model's memory, and the user may never see a ranked list at all. "
            "<bookmark mark='b'/> Generative retrieval goes further: the model memorizes the collection and emits "
            "the identifiers of relevant documents itself, which makes updating the index the hard part. "
            "<bookmark mark='c'/> How to evaluate a written answer rather than a ranked list, how to check that it "
            "is faithful to its sources, and how to keep a model's memory as fresh as an index, are open."
        ) as vo:
            self.play(FadeIn(head), FadeIn(row), FadeIn(names), *[GrowArrow(a) for a in arrows])
            for mk, ln in zip("abc", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.4)
        self.clear_scene()

    def open(self):
        head = label(r"Open", font_size=36).to_edge(UP, buff=0.3)
        items = VGroup(
            wrapped_label(r"1. \ \textbf{Guarantees for graph search}: \ recall and query-time bounds for "
                          r"navigable graphs on realistic data.", 12.4, font_size=24, color=WHITE),
            wrapped_label(r"2. \ \textbf{Generalization}: \ learned retrievers that beat BM25 on collections they "
                          r"have never seen.", 12.4, font_size=24, color=YES),
            wrapped_label(r"3. \ \textbf{Evaluation without judges}: \ measuring rankings and written answers when "
                          r"human judgments are too few.", 12.4, font_size=24, color=HEAD),
            wrapped_label(r"4. \ \textbf{Fresh learned indexes}: \ adding and deleting documents in a generative "
                          r"index without retraining.", 12.4, font_size=24, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.45)
        star = wrapped_label(r"$\bigstar$ \ this part's research problem: \ a graph-based nearest-neighbour index "
                             r"with provable recall and query time on data with low intrinsic dimension", 12.4,
                             font_size=23, color=LAM).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Open problems. <bookmark mark='a'/> Guarantees for graph-based nearest-neighbour search on the data "
            "people actually have. <bookmark mark='b'/> Learned retrievers that beat BM25 on collections they have "
            "never seen. <bookmark mark='c'/> Evaluation when human judgments are too few, for rankings and for "
            "written answers. <bookmark mark='d'/> And generative indexes that can add and delete documents without "
            "being retrained. <bookmark mark='e'/> This part's research problem asks for a graph index with provable "
            "recall and query time on data whose intrinsic dimension is low, the case real collections seem to "
            "be."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it))
            vo.wait_until("e")
            self.play(FadeIn(star))
        self.wait(0.6)
        self.clear_scene()


_ = (DATA, KERN, LAM, NO, YES)
