from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs47.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES


def tile(content, caption, color, TW=3.6, TH=2.3):
    frame = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D,
                             stroke_width=1.5, fill_color=BG, fill_opacity=1)
    if content.width > TW:
        content.scale_to_fit_width(TW)
    if content.height > TH:
        content.scale_to_fit_height(TH)
    content.move_to(frame.get_center() + UP * 0.25)
    cap = label(caption, font_size=22, color=color).move_to(frame.get_bottom() + UP * 0.3)
    return Group(frame, content, cap)


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.practice()
        self.problems()
        self.next_time()
        self.references()

    def recap(self):
        head = label(rf"Part {PART}: \ Search Engines", font_size=34).to_edge(UP, buff=0.3)
        tiles = Group(
            tile(MathTex(r"f \propto r^{-1}", font_size=60, color=GREY_A), r"Zipf's law", GREY_A),
            tile(label(r"term $\to$ sorted ids", font_size=40, color=HEAD), r"the inverted index", HEAD),
            tile(MathTex(r"2\lfloor\log_2 g\rfloor + 1", font_size=48, color=DATA), r"Elias gamma", DATA),
            tile(MathTex(r"\frac{tf\,(k_1+1)}{tf + k_1 \cdots}", font_size=48, color=YES), r"BM25", YES),
            tile(MathTex(r"r = \tfrac{1-d}{N} + d\,M r", font_size=46, color=LAM), r"PageRank", LAM),
            tile(label(r"layers of neighbours", font_size=38, color=KERN), r"HNSW", KERN),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        with self.voiceover(
            "What we built in this part. Zipf's and Heaps' laws, fitted on the novels. An inverted index, and three "
            "ways to intersect its lists, from a linear merge to galloping search. Gap codes whose lengths we "
            "derived, which shrink a posting from thirty-two bits to about five. BM25, from the probability ranking "
            "principle, measured with nDCG; WAND, which finds the same top ten while fully scoring a fraction of the "
            "candidates; PageRank as the stationary distribution of a random surfer; SimHash for near-duplicates; and "
            "vectors compressed by product quantization and searched through a layered graph. One idea runs through "
            "it: a good index does almost all of the work before the query arrives."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"designing a search service: \ sharding, \ caching, \ freshness", [48, 49]),
            (r"keeping a large serving system healthy", [50]),
            (r"spectral methods behind PageRank", [56]),
            (r"why learned rankers generalize, \ or do not", [57]),
            (r"hardware for vector search and inference", [60]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. Parts 48 and 49 design a search service: how to shard it, cache it and keep it "
            "fresh. Part 50 keeps a serving system like it healthy. Part 56 returns to the eigenvectors behind "
            "PageRank with spectral graph theory. Part 57 asks when a learned ranker will generalize. And Part 60 "
            "looks at the hardware built for vector search and inference."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"text", r"normalize the way users type; \ stem with care; \ keep the original for phrases"),
            (r"indexes", r"sorted postings, \ compressed in blocks, \ with skip data and score bounds"),
            (r"ranking", r"BM25 as the baseline to beat; \ tune $k_1$ and $b$ on judged queries"),
            (r"evaluation", r"a judged query set, \ nDCG, \ and significance before shipping a change"),
            (r"vectors", r"hybrid lexical plus dense; \ measure recall of the approximate search"),
        ])
        with self.voiceover(
            "In practice. Normalize text the way your users type it, stem with care, and keep the original words "
            "for phrase queries. Store postings sorted and compressed in blocks, with skip data and score bounds. "
            "Treat BM25 as the baseline to beat, and tune it on judged queries. Keep a set of judged queries, "
            "measure nDCG, and test significance before shipping a ranking change. And combine lexical and dense "
            "retrieval, measuring how much the approximate vector search misses."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Show that galloping intersection of lists of sizes $m \le n$ takes $O(m \log(n/m))$ comparisons, \ "
            r"and that this is optimal up to a constant.",
            r"Derive the lengths of Elias $\gamma$ and $\delta$ codes, \ and the Golomb parameter that is optimal "
            r"for geometric gaps.",
            r"Derive BM25's term weight from the binary independence model with a two-Poisson approximation, \ "
            r"and explain $k_1$ and $b$.",
            r"Show that PageRank is the stationary distribution of a Markov chain, \ and that power iteration "
            r"converges at rate $d$.",
            r"\textit{Build.} \ Add block-max WAND to our engine \ (score bounds per block of postings) \ and "
            r"measure how many more documents it skips.",
            r"$\bigstar$ \textit{Research.} \ A graph-based nearest-neighbour index with provable recall and "
            r"query time on realistic data.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: give our engine block-max WAND, with a score bound for every block of postings, and measure "
            "how much more it skips. The last, marked with a star, is a research problem: a graph index for "
            "nearest neighbours with guarantees on recall and speed for the kind of data people actually search."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 48, \ System Design I: \ Building Blocks", font_size=40).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"back-of-the-envelope numbers every designer should know", HEAD),
            (r"load balancers, \ caches and their hit rates", DATA),
            (r"sharding, \ replication and consistent hashing again", YES),
            (r"rate limiters, \ queues and the shape of a design", LAM))]).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "Next time, Part 48: system design, and its building blocks. The numbers every designer should carry, "
            "load balancers and caches and the arithmetic of their hit rates, sharding and replication, rate "
            "limiters and queues, and how to put them together into the shape of a design."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Manning, \ Raghavan and Sch\"utze, \textit{Introduction to Information Retrieval}; \ B\"uttcher, \ "
             r"Clarke and Cormack, \textit{Information Retrieval}",
             r"Witten, \ Moffat and Bell, \textit{Managing Gigabytes}"],
            [r"Porter \ (1980); \ Zobel and Moffat \ (2006); \ Robertson and Zaragoza \ (2009); \ J\"arvelin and "
             r"Kek\"al\"ainen \ (2002)",
             r"Brin and Page \ (1998); \ Kleinberg \ (1999); \ Broder et al. \ (2003); \ Ding and Suel \ (2011)",
             r"Charikar \ (2002); \ J\'egou, \ Douze and Schmid \ (2011); \ Malkov and Yashunin \ (2018)",
             r"Burges \ (2010, \ LambdaMART); \ Karpukhin et al. \ (2020, \ dense retrieval)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(2.0)


_ = (NO, YES, KERN, LAM, DATA)
