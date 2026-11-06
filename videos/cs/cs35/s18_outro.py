from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs35.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES)


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
        head = label(rf"Part {PART}: \ Databases", font_size=38).to_edge(UP, buff=0.3)
        tiles = Group(
            tile(MathTex(r"\sigma\ \pi\ \bowtie", font_size=60, color=DATA), r"Codd's algebra", DATA),
            tile(MathTex(r"3(M + N)", font_size=56, color=YES), r"joins, \ counted in pages", YES),
            tile(MathTex(r"2^n \ll n!", font_size=56, color=HEAD), r"Selinger's search", HEAD),
            tile(MathTex(r"\log_{400} n", font_size=56, color=LAM), r"B+ trees", LAM),
            tile(MathTex(r"T_1 \rightleftarrows T_2", font_size=56, color=NO), r"serializability and its cycles", NO),
            tile(MathTex(r"\textsf{redo, undo}", font_size=50, color=KERN), r"ARIES", KERN),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        with self.voiceover(
            "What we built in this part. A relational database: Codd's algebra over tables, the theory of good "
            "design, a SQL parser, iterators, four join algorithms whose page counts match their formulas, and "
            "Selinger's optimizer, searching subsets instead of orders, with the statistics it relies on and the ways "
            "they fail. B-plus trees. Then transactions: serializability and its graph, two-phase locking and "
            "deadlock, snapshots and write skew, the isolation levels, and ARIES recovering from five hundred crashes. "
            "Column stores, and the Job as one line of SQL."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"transactions across machines: \ two-phase commit, \ Spanner", [39]),
            (r"services over a database: \ idempotency, \ sagas, \ the outbox", [43]),
            (r"the log as a stream, \ and warehouses on column stores", [46]),
            (r"inverted indexes at web scale", [47]),
            (r"shards, \ replicas and caches in front of a database", [48]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. Part 39 stretches transactions across machines, with two-phase commit and "
            "Spanner's clocks. Part 43 builds services on top of a database, with idempotent requests and sagas in "
            "place of distributed transactions. Part 46 turns the write-ahead log into a stream that other systems "
            "follow, and builds warehouses on column stores. Part 47 scales the inverted index to the web. And Part 48 "
            "puts shards, replicas and caches in front of a database."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"choose", r"PostgreSQL by default; \ SQLite inside a program; \ DuckDB for analytics on one machine"),
            (r"read plans", r"\texttt{EXPLAIN ANALYZE}: \ compare estimated rows with actual; \ big gaps mean stale or "
                            r"missing statistics"),
            (r"index", r"for the queries you run: \ columns in \texttt{WHERE}, \ \texttt{JOIN} and \texttt{ORDER BY}; "
                       r"\ each index slows writes"),
            (r"isolation", r"know your default \ (usually read committed); \ use \texttt{SERIALIZABLE} and retry on "
                           r"aborts when invariants span rows"),
            (r"design", r"normalize first, \ denormalize when measured; \ let the database enforce keys and "
                        r"constraints"),
        ])
        with self.voiceover(
            "In practice. Start with PostgreSQL; use SQLite inside a program and DuckDB for analysis on one machine. "
            "When a query is slow, run EXPLAIN ANALYZE and compare the estimated rows with the actual rows: a large gap "
            "means the statistics are stale or the columns are correlated. Index the columns your queries filter, join "
            "and sort on, and remember that every index slows every write. Know your isolation level, which is usually "
            "read committed, and when an invariant spans several rows, like the doctors on call, use serializable and "
            "retry on aborts. And normalize first; denormalize only when you have measured why."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Prove that a schedule is conflict-serializable if and only if its precedence graph is acyclic.",
            r"Prove that every schedule produced by two-phase locking is conflict-serializable, \ and give a "
            r"serializable schedule that 2PL cannot produce.",
            r"Derive the I/O cost of external merge sort with $B$ buffers, \ and the memory Grace hash join needs "
            r"for one partitioning pass \ ($B \gtrsim \sqrt{M}$).",
            r"Count the bushy join trees over $n$ tables \ ($n! \, C_{n-1}$), \ and the work of Selinger's dynamic "
            r"program on chain, \ star and clique queries.",
            r"\textit{Build.} \ Add a histogram per column to our database's statistics; \ measure the "
            r"\texttt{word = 'the'} estimate before and after.",
            r"$\bigstar$ \textit{Research.} \ False aborts: \ on random workloads, \ how many of SSI's aborts were "
            r"unnecessary? \ Find the fewest aborts any online scheduler that sees only rw-edges can make, \ and a "
            r"rule that achieves it.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: give our database histograms, and watch the estimate for the most common word come right. The "
            "last, marked with a star, is a research problem: how many of serializable snapshot isolation's aborts "
            "were really necessary, and how few can any scheduler that sees only read-write conflicts make?"
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 36, \ Networks I: \ Moving Bits", font_size=42).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"circuits against packets: \ Baran, \ Davies, \ ARPANET", HEAD),
            (r"layers and the end-to-end argument", DATA),
            (r"Shannon's capacity, \ ALOHA's $1/2e$, \ Ethernet's backoff", YES),
            (r"IP, \ forwarding, \ routing, \ and BGP", KERN))]).arrange(DOWN, buff=0.35)
        q = label(r"the Job's words leave the machine", font_size=26, color=GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Next time, Part 36: Networks, moving bits. The telephone network reserved a wire for every call; Paul "
            "Baran and Donald Davies proposed cutting messages into packets that find their own way. We derive what "
            "limits each layer of the Internet, from Shannon's capacity to ALOHA's one over two e, and route packets "
            "across a network of our own. Part 36, Networks."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Silberschatz, Korth and Sudarshan, \textit{Database System Concepts}; \ Ramakrishnan and Gehrke, "
             r"\textit{Database Management Systems}",
             r"Hellerstein and Stonebraker, \textit{Readings in Database Systems}; \ Gray and Reuter, "
             r"\textit{Transaction Processing}",
             r"Bernstein, Hadzilacos and Goodman, \textit{Concurrency Control and Recovery}; \ Abiteboul, Hull and "
             r"Vianu"],
            [r"Codd \ (1970); \ Selinger et al. \ (1979); \ Eswaran et al. \ (1976); \ Bayer and McCreight \ (1972)",
             r"Mohan et al., \ ARIES \ (1992); \ Berenson et al. \ (1995); \ Adya \ (1999); \ Cahill et al. \ (2008)",
             r"Graefe, \ Volcano \ (1994); \ Leis et al. \ (2015); \ Stonebraker et al., \ C-Store \ (2005); \ Boncz "
             r"et al. \ (2005)",
             r"Atserias, Grohe and Marx \ (2008); \ Ngo et al. \ (2012); \ Marcus et al., \ Bao \ (2021); \ Kingsbury "
             r"and Alvaro, \ Elle \ (2020)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()


_ = (YES, NO)
