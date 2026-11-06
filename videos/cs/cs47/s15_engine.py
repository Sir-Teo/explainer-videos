from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs47.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load


def _clean(s: str) -> str:
    for a, b in (("\\", ""), ("&", "and"), ("%", ""), ("$", ""), ("#", ""), ("_", " "), ("{", ""), ("}", ""),
                 ("^", ""), ("~", "")):
        s = s.replace(a, b)
    return s


class Engine(VoiceoverScene):
    def construct(self):
        self.card()
        self.pipeline()
        self.answers()
        self.size()
        self.missing()

    def card(self):
        card = chapter_card(14, r"A search engine for the novels", r"What does it take to answer a query well?",
                            lit=(1980, 1994), extra=((1980, r"Porter's stemmer"),
                                                     (1994, r"Okapi BM25 at TREC")), part=PART)
        with self.voiceover("Chapter fourteen. A search engine for the novels."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def pipeline(self):
        ix = load("index")
        e = load("engine")
        q = e["queries"][3]
        head = label(r"From a query to ten passages", font_size=36).to_edge(UP, buff=0.3)
        steps = [(rf"``{q['query']}''", WHITE), (r"tokens, \ stop words dropped, \ stems: \ "
                                                   + r", \ ".join(rf"\texttt{{{t}}}" for t in q["terms"]), HEAD),
                 (rf"postings of each stem, \ from {ix['postings']:,}", DATA),
                 (r"BM25 for every candidate \ (WAND skips most)", YES),
                 (r"the top ten, \ each with a snippet", LAM)]
        boxes = VGroup()
        for t, c in steps:
            r = RoundedRectangle(width=8.6, height=0.7, corner_radius=0.12, stroke_color=c, stroke_width=1.8,
                                 fill_color=BG, fill_opacity=1)
            boxes.add(VGroup(r, label(t, font_size=20, color=c).move_to(r)))
        boxes.arrange(DOWN, buff=0.28).next_to(head, DOWN, buff=0.4)
        arrows = VGroup(*[Arrow(boxes[i].get_bottom(), boxes[i + 1].get_top(), buff=0.03, stroke_width=2,
                                color=GREY_C, max_tip_length_to_length_ratio=0.3) for i in range(4)])
        with self.voiceover(
            "Here is our engine, end to end. <bookmark mark='a'/> A query arrives: the hound on the moor. "
            "<bookmark mark='b'/> It is tokenized exactly as the passages were, stop words are dropped, and the "
            "rest are stemmed, so that it matches the index's terms. <bookmark mark='c'/> The engine fetches the "
            "postings of each term. <bookmark mark='d'/> It scores the candidates with BM25, letting WAND skip "
            "those that cannot reach the top ten. <bookmark mark='e'/> And it returns the ten best passages, each "
            "with a snippet cut around the first word that matched."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcde"):
                vo.wait_until(mk)
                self.play(FadeIn(boxes[k]), *([GrowArrow(arrows[k - 1])] if k else []))
        self.wait(0.4)
        self.clear_scene()

    def answers(self):
        e = load("engine")
        head = label(r"Four queries", font_size=36).to_edge(UP, buff=0.3)
        cols = VGroup()
        for q in e["queries"]:
            r = q["results"][0]
            card = VGroup(label(rf"``{q['query']}''", font_size=20, color=HEAD),
                          label(rf"{r['book']}, \ passage {r['doc']:,} \ (BM25 {r['score']:.1f})", font_size=17,
                                color=DATA),
                          wrapped_label(rf"\ldots {_clean(r['snippet'])} \ldots", 5.6, font_size=16, color=GREY_A))
            card.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            cols.add(card)
        cols.arrange_in_grid(rows=2, cols=2, buff=(0.6, 0.5)).next_to(head, DOWN, buff=0.5)
        foot = wrapped_label(r"every top result comes from the book a reader would expect; \ the snippet shows why "
                             r"it matched", 12.4, font_size=20, color=YES).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Four queries and their best answers. <bookmark mark='a'/> The white whale, and call me Ishmael, both go "
            "to Moby-Dick, to passages where those words cluster. <bookmark mark='b'/> Pride and prejudice "
            "goes to Jane Austen's novel, and the hound on the moor to The Hound of the Baskervilles. "
            "<bookmark mark='c'/> Nothing here knows what the books are about. The ranking comes entirely from which "
            "words are rare, where they occur, and how long the passages are."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cols[0]), FadeIn(cols[1]))
            vo.wait_until("b")
            self.play(FadeIn(cols[2]), FadeIn(cols[3]))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def size(self):
        c = load("codes")
        ix = load("index")
        bnd = load("bound")
        n = c["postings"]
        rows = []
        for key, name in (("raw32", r"32-bit integers"), ("vbyte", r"variable byte"), ("gamma", r"Elias $\gamma$"),
                          ("delta", r"Elias $\delta$"), ("rice", r"Golomb--Rice")):
            b = c["bits_per_posting"][key]
            rows.append([name, f"{b:.2f}", f"{b * n / 8 / 1e6:.1f} MB"])
        rows.append([r"lower bound, \ $\log_2 \binom{N}{f}$", f"{bnd['bound_bits_per_posting']:.2f}",
                     f"{bnd['bound_bits_per_posting'] * n / 8 / 1e6:.1f} MB"])
        tab = grid_table([r"document ids stored as", r"bits per posting", r"index of ids"], rows,
                         widths=[4.6, 2.6, 2.6], row_h=0.48, font_size=19, mono_cols=())
        tab.next_to(head := label(r"How big is the index?", font_size=36).to_edge(UP, buff=0.3), DOWN, buff=0.5)
        for cell in tab.cells[5]:
            cell.set_color(YES)
        for cell in tab.cells[6]:
            cell.set_color(HEAD)
        txt = ix["tokens"]
        foot = VGroup(
            wrapped_label(rf"{n:,} postings for {ix['terms']:,} terms; \ the novels' text is about "
                          rf"{txt:,} words", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"positions for phrase queries cost more, \ compressed the same way", 12.4, font_size=20,
                          color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "How big is it? <bookmark mark='a'/> Our index holds "
            f"{n / 1e6:.1f} million postings. Stored as plain thirty-two-bit integers, the document ids alone take "
            f"about {32 * n / 8 / 1e6:.0f} megabytes. <bookmark mark='b'/> As gaps in Golomb–Rice code, about "
            f"{c['bits_per_posting']['rice'] * n / 8 / 1e6:.1f}, five bits a posting. <bookmark mark='c'/> And no "
            "code can do much better: choosing which f of N documents contain a term carries log of N choose f "
            f"bits of information, which comes to {bnd['bound_bits_per_posting']:.2f} bits a posting here. Golomb–"
            "Rice is within a few percent of that limit, unless a code can exploit how postings cluster."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])), FadeIn(foot[0]))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[1])), FadeIn(VGroup(*tab.cells[2])))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[3:6]], lag_ratio=0.3), FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[6])))
        self.wait(0.4)
        self.clear_scene()

    def missing(self):
        head = label(r"What a web search engine adds", font_size=36).to_edge(UP, buff=0.3)
        rows = [
            [r"documents", r"11,261 passages", r"hundreds of billions of pages, \ re-crawled continuously"],
            [r"text", r"one language, \ Porter stems", r"hundreds of languages, \ synonyms, \ entities"],
            [r"ranking", r"BM25", r"hundreds of signals, \ learned rankers, \ neural models"],
            [r"links", r"none", r"PageRank-like authority, \ spam defences"],
            [r"serving", r"one process", r"thousands of machines, \ replicas, \ caches \ (chapter 10)"],
            [r"freshness", r"fixed", r"news indexed in minutes"],
        ]
        tab = grid_table([r"", r"ours", r"a web engine"], rows, widths=[2.2, 3.8, 7.0], row_h=0.52, font_size=18,
                         mono_cols=())
        tab.next_to(head, DOWN, buff=0.4)
        foot = wrapped_label(r"Lucene, \ the open-source library under Elasticsearch, \ OpenSearch and Solr, \ uses "
                             r"BM25 by default and the same ideas, \ engineered for decades", 12.4, font_size=20,
                             color=HEAD).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "And what a web search engine adds. <bookmark mark='a'/> Hundreds of billions of pages instead of eleven "
            "thousand passages, crawled again and again; hundreds of languages, with synonyms and entities; hundreds "
            "of ranking signals combined by learned models; link authority and defences against spam; thousands of "
            "machines; and news that must be searchable minutes after it is published. <bookmark mark='b'/> But "
            "the core is the same. Lucene, the open-source library under Elasticsearch, OpenSearch and Solr, ranks "
            "with BM25 by default, over compressed inverted lists like ours."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])))
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3), run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (DATA, KERN, LAM, NO)
