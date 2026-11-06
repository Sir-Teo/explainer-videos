from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs47.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load


class Hook(VoiceoverScene):
    def construct(self):
        self.history()
        self.pieces()
        self.ours()
        self.plan()

    def history(self):
        head = label(r"Finding things", font_size=38).to_edge(UP, buff=0.35)
        events = [(1990, r"Archie: \ an index of FTP file names \ (McGill)", GREY_A),
                  (1994, r"Lycos, \ WebCrawler, \ Yahoo's directory", DATA),
                  (1995, r"AltaVista: \ the full text of the web, \ fast", LAM),
                  (1998, r"Google: \ links as votes; \ 24 million pages indexed", HEAD),
                  (2010, r"instant results as you type", YES),
                  (2020, r"neural ranking, \ dense vectors beside the index", KERN)]
        x0, x1, y = -6.0, 6.0, 0.4
        axis = Line([x0, y, 0], [x1, y, 0], color=GREY_C)

        def X(yr):
            return x0 + (yr - 1988) / (2024 - 1988) * (x1 - x0)
        marks = VGroup()
        for k, (yr, t, c) in enumerate(events):
            up = k % 2 == 0
            d = Dot([X(yr), y, 0], radius=0.08, color=c)
            stem = Line([X(yr), y, 0], [X(yr), y + (0.9 if up else -0.9), 0], color=c, stroke_width=1.5)
            lb = VGroup(label(f"{yr}", font_size=18, color=c), wrapped_label(t, 2.6, font_size=17, color=GREY_A))
            lb.arrange(DOWN, buff=0.06).next_to(stem, UP if up else DOWN, buff=0.08)
            marks.add(VGroup(d, stem, lb))
        foot = wrapped_label(r"today: \ an index of hundreds of billions of pages, \ answered in a fraction of a "
                             r"second \ (Google, \ \textit{How Search Works})", 12.4, font_size=20,
                             color=WHITE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "How do you find the ten most useful pages among hundreds of billions, in a fraction of a second? "
            "<bookmark mark='a'/> The first search engine, Archie, written at McGill University in 1990, indexed "
            "the names of files on FTP servers, not their contents. By 1994 there were crawlers and directories of "
            "the web, and in 1995 AltaVista searched the full text of the web, quickly. <bookmark mark='b'/> In "
            "1998 Sergey Brin and Larry Page described Google, which treated links between pages as votes, and "
            "began with an index of twenty-four million pages. <bookmark mark='c'/> Today's indexes hold hundreds of "
            "billions of pages, and rank them with learned models and dense vectors as well as words."
        ) as vo:
            self.play(FadeIn(head), Create(axis))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in marks[:3]], lag_ratio=0.5), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(marks[3]))
            vo.wait_until("c")
            self.play(FadeIn(marks[4]), FadeIn(marks[5]), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def pieces(self):
        head = label(r"Five ideas", font_size=36).to_edge(UP, buff=0.3)
        specs = [(r"an inverted index", r"search becomes merging sorted lists", HEAD),
                 (r"compression", r"those lists fit in memory", DATA),
                 (r"a model of relevance", r"probability gives BM25", YES),
                 (r"a random surfer", r"links give PageRank", LAM),
                 (r"vectors", r"meaning as nearness, \ searched by graphs", KERN)]
        tiles = VGroup()
        for t, sub, col in specs:
            frame = RoundedRectangle(width=4.0, height=1.45, corner_radius=0.15, stroke_color=col, stroke_width=2,
                                     fill_color=BG, fill_opacity=1)
            a = label(t, font_size=22, color=col)
            b = wrapped_label(sub, 3.6, font_size=17, color=GREY_A)
            VGroup(a, b).arrange(DOWN, buff=0.15).move_to(frame)
            tiles.add(VGroup(frame, a, b))
        tiles[:3].arrange(RIGHT, buff=0.3)
        tiles[3:].arrange(RIGHT, buff=0.3)
        VGroup(tiles[:3], tiles[3:]).arrange(DOWN, buff=0.35).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "A search engine rests on five ideas, and each is a piece of mathematics this series has met. "
            "<bookmark mark='a'/> An inverted index turns a query into the merging of sorted lists. "
            "<bookmark mark='b'/> Compression keeps those lists small enough to hold in memory. "
            "<bookmark mark='c'/> A probabilistic model of what relevant means produces the ranking formula called "
            "BM25. <bookmark mark='d'/> A random surfer wandering over links produces PageRank. "
            "<bookmark mark='e'/> And vectors place documents near queries that mean the same thing, found by "
            "searching a graph."
        ) as vo:
            self.play(FadeIn(head))
            for mk, t in zip("abcde", tiles):
                vo.wait_until(mk)
                self.play(FadeIn(t, shift=UP * 0.15))
        self.wait(0.4)
        self.clear_scene()

    def ours(self):
        e = load("engine")
        ix = load("index")
        q = e["queries"][0]
        head = label(r"A search engine for thirty novels", font_size=36).to_edge(UP, buff=0.3)
        bar = RoundedRectangle(width=6.0, height=0.6, corner_radius=0.25, stroke_color=GREY_B, stroke_width=1.5,
                               fill_color=BG, fill_opacity=1).next_to(head, DOWN, buff=0.35)
        qt = label(rf"\texttt{{{q['query']}}}", font_size=24, color=WHITE).move_to(bar).align_to(bar, LEFT).shift(
            RIGHT * 0.3)
        results = VGroup()
        for r in q["results"][:4]:
            snip = r["snippet"].replace("\\", "").replace("&", "and").replace("%", "").replace("$", "")
            snip = snip.replace("#", "").replace("_", " ").replace("{", "").replace("}", "").replace("^", "")
            t = VGroup(label(rf"{r['book']} \ --- \ passage {r['doc']:,}", font_size=19, color=HEAD),
                       wrapped_label(rf"\ldots {snip} \ldots", 11.6, font_size=17, color=GREY_A),
                       label(rf"BM25 {r['score']:.2f}", font_size=15, color=GREY_B)).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.06)
            results.add(t)
        results.arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(bar, DOWN, buff=0.35).align_to(bar, LEFT).shift(
            LEFT * 2.5)
        stats = label(rf"{ix['docs']:,} passages, \ {ix['terms']:,} terms, \ {ix['postings']:,} postings",
                      font_size=19, color=DATA).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "In this part we build one, for the thirty novels of this series. <bookmark mark='a'/> The novels are cut "
            f"into {ix['docs']:,} passages of four hundred words, and indexed: {ix['terms']:,} distinct terms, "
            f"{ix['postings']:,} postings. <bookmark mark='b'/> Ask it for the white whale, and it ranks the "
            "passages, and shows each with a snippet around the words that matched. <bookmark mark='c'/> By the end "
            "of the part every step of that will be ours: the tokenizer, the index, the compression, the ranking, "
            "and an evaluation of how good the ranking is."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bar))
            vo.wait_until("a")
            self.play(FadeIn(stats))
            vo.wait_until("b")
            self.play(Write(qt))
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in results], lag_ratio=0.4), run_time=3)
            vo.wait_until("c")
            self.play(Indicate(stats, color=WHITE))
        self.wait(0.4)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Search Engines", font_size=36).to_edge(UP, buff=0.3)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"Zipf's and Heaps' laws on the novels",
            r"the inverted index and fast intersection",
            r"gap codes: \ vbyte, \ Elias, \ Golomb--Rice",
            r"BM25 from the probability ranking principle; \ nDCG",
            r"WAND, \ PageRank, \ SimHash",
            r"learning to rank, \ product quantization and HNSW",
        ], font_size=25).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 47 of Computer Science, Built. <bookmark mark='a'/> We will fit Zipf's and Heaps' laws to "
            "the novels; build an inverted index and intersect its lists with as few comparisons as possible; "
            "compress them with codes whose lengths we derive; derive BM25 from a model of relevance and measure "
            "it; skip most of the work with WAND; rank pages by a random walk; find near-duplicates; and search "
            "by meaning, with vectors compressed by product quantization and searched by a layered graph."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()


_ = (KERN, LAM, NO, YES)
