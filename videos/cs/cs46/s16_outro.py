from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs46.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES


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
        head = label(rf"Part {PART}: \ Logs, \ Streams and Warehouses", font_size=34).to_edge(UP, buff=0.3)
        tiles = Group(
            tile(label(r"(partition, \ offset)", font_size=40, color=HEAD), r"the partitioned log", HEAD),
            tile(label(r"state $=$ fold(events)", font_size=40, color=DATA), r"event sourcing", DATA),
            tile(label(r"event time $\ne$ arrival", font_size=38, color=NO), r"watermarks", NO),
            tile(label(r"barriers $\to$ snapshots", font_size=38, color=YES), r"exactly-once state", YES),
            tile(label(r"dictionary, \ RLE, \ delta", font_size=38, color=KERN), r"columnar encodings", KERN),
            tile(MathTex(r"(r,\ d)", font_size=60, color=LAM), r"Dremel's levels", LAM),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        with self.voiceover(
            "What we built in this part. A partitioned log, where order holds per key and consumer groups share the "
            "partitions, and a compacted log that rebuilds the same state from fifty records instead of two "
            "thousand. State as a fold over events. Windows over event time, and watermarks that trade completeness "
            "for latency, unless an answer may be corrected later. Barrier snapshots that let a computation crash "
            "and recover with exactly-once state. Columnar files, whose dictionaries and run lengths make a column "
            "of words a fraction of its size, and Dremel's two levels that put nested records into flat columns. "
            "One idea runs through it: record what happened, in order, once, and every answer can be derived, and "
            "derived again."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"indexes built from logs, \ updated as documents change", [47]),
            (r"system design: \ feeds, \ timelines and analytics", [48, 49]),
            (r"metrics, \ logs and traces for running systems", [50]),
            (r"learning from data at scale", [57]),
            (r"privacy and trust in data pipelines", [55]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. Part 47 builds a search index from a log of documents and keeps it current. "
            "Parts 48 and 49 design feeds, timelines and analytics systems from these pieces. Part 50 turns logs, "
            "metrics and traces on the running system itself. Part 57 asks what can be learned from data at this "
            "scale, and Part 55 what it takes to trust the pipeline that delivered it."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"logs", r"key by what must stay ordered; \ enough partitions for the future; \ compaction for state"),
            (r"streams", r"event time, \ not arrival time; \ choose lateness on purpose; \ idempotent sinks"),
            (r"changes", r"capture from the WAL or an outbox, \ never by dual writes"),
            (r"tables", r"columnar files, \ sorted or clustered by the common filter; \ partitions that prune"),
            (r"joins", r"broadcast the small side; \ watch for hot keys, \ and salt them"),
        ])
        with self.voiceover(
            "In practice. Key a log by whatever must stay in order, give it enough partitions for the future, and "
            "compact the logs that hold state. Window streams by event time, choose their lateness on purpose, and "
            "write results to sinks that tolerate repeats. Capture changes from the database's log or an outbox, "
            "never by writing twice. Store tables as columnar files, sorted or clustered by the filter people use "
            "most. And broadcast the small side of a join, and look for hot keys before they find you."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Show that a consumer of one partition sees each key's events in order, \ and give an example where a "
            r"consumer of two partitions sees two keys' events in an order no producer wrote.",
            r"Prove that a watermark lag of $L$ drops exactly the events whose delay exceeds $L$ plus the window's "
            r"slack, \ and compute the share dropped for exponential delays.",
            r"Show that asynchronous barrier snapshots give a consistent cut \ (Part 38), \ and hence exactly-once "
            r"state after recovery.",
            r"Compute the repetition and definition levels of a three-level nested column by hand, \ and rebuild "
            r"the records from them.",
            r"\textit{Build.} \ Add sliding windows and allowed lateness to our stream processor, \ and measure "
            r"the state it must keep.",
            r"$\bigstar$ \textit{Research.} \ Which windowed stream joins can be maintained exactly in space "
            r"sublinear in the window?",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: give our stream processor sliding windows and allowed lateness, and measure how much state it "
            "has to keep. The last, marked with a star, is a research problem: which joins over windows of a "
            "stream can be maintained exactly with less memory than the window itself."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 47, \ Search Engines", font_size=40).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"an inverted index: \ search as merging sorted lists", HEAD),
            (r"compression that keeps the lists in memory", DATA),
            (r"BM25 from a probabilistic model of relevance", YES),
            (r"PageRank, \ and dense vectors beside it", LAM))]).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "Next time, Part 47: search engines. How do you find the ten most relevant pages among billions in a "
            "fifth of a second? An inverted index turns search into merging sorted lists, compression keeps them in "
            "memory, a probabilistic model of relevance gives BM25, and a random surfer gives PageRank."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Kleppmann, \textit{Designing Data-Intensive Applications}, \ ch. 3, 10--12; \ Akidau, \ Chernyak and "
             r"Lax, \textit{Streaming Systems}",
             r"Kimball and Ross, \textit{The Data Warehouse Toolkit}"],
            [r"Kreps \ (2013); \ Kreps, \ Narkhede and Rao \ (2011, \ Kafka); \ Akidau et al. \ (2015, \ Dataflow)",
             r"Carbone et al. \ (2015); \ Melnik et al. \ (2010, \ Dremel); \ Armbrust et al. \ (2020, \ Delta Lake)",
             r"Karnin, \ Lang and Liberty \ (2016); \ McSherry et al. \ (2013); \ Budiu et al. \ (2023)",
             r"the Apache Parquet format specification"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(2.0)


_ = (NO, YES, KERN, LAM, DATA)
