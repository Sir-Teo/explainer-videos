from __future__ import annotations

import random

from explainer.cs import *  # noqa: F403
from videos.cs.cs47.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load, mono, tag_box


class Index(VoiceoverScene):
    def construct(self):
        self.card()
        self.matrix()
        self.postings()
        self.sorting()
        self.spimi()
        self.segments()

    def card(self):
        card = chapter_card(2, r"The inverted index", r"Which passages contain this word?", lit=(1994, 2003),
                            extra=((1994, r"Witten, \ Moffat and Bell: \ \textit{Managing Gigabytes}"),
                                   (1999, r"Cutting: \ Lucene"),
                                   (2003, r"Heinz and Zobel: \ single-pass indexing")), part=PART)
        with self.voiceover("Chapter two. The inverted index."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def matrix(self):
        ix = load("index")
        head = label(r"Every term, \ every passage", font_size=36).to_edge(UP, buff=0.3)
        # an illustrative incidence matrix: three "books" of eight passages each, terms clustered by book
        terms = ["the", "and", "whale", "sea", "ahab", "ship", "love", "darci", "holm", "moor"]
        dens = {"the": (0.97, 0.97, 0.97), "and": (0.92, 0.92, 0.92), "whale": (0, 0.6, 0), "sea": (0.1, 0.55, 0.1),
                "ahab": (0, 0.35, 0), "ship": (0.05, 0.4, 0.05), "love": (0.35, 0.1, 0.1), "darci": (0.5, 0, 0),
                "holm": (0, 0, 0.6), "moor": (0, 0, 0.3)}
        rng = random.Random(47)
        cell, ncol = 0.36, 20
        x0, y0 = -5.3, 1.85
        grid = VGroup()
        for i in range(ncol + 1):
            grid.add(Line([x0 + i * cell, y0, 0], [x0 + i * cell, y0 - len(terms) * cell, 0], color=GREY_D,
                          stroke_width=1))
        for j in range(len(terms) + 1):
            grid.add(Line([x0, y0 - j * cell, 0], [x0 + ncol * cell, y0 - j * cell, 0], color=GREY_D,
                          stroke_width=1))
        names = VGroup(*[mono(t, size=19, color=WHITE).move_to([0, y0 - (j + 0.5) * cell, 0]).align_to(
            [x0 - 0.12, 0, 0], RIGHT) for j, t in enumerate(terms)])
        cap = label(r"passages $\rightarrow$", font_size=20, color=GREY_A).next_to(grid, UP, buff=0.12).align_to(
            grid, LEFT)
        rows = []
        for j, t in enumerate(terms):
            row = VGroup()
            for i in range(ncol):
                if rng.random() < dens[t][i * 3 // ncol]:
                    row.add(Dot([x0 + (i + 0.5) * cell, y0 - (j + 0.5) * cell, 0], radius=0.1, color=DATA))
            rows.append(row)
        dots = VGroup(*rows)
        illus = note(r"illustrative", font_size=16).next_to(grid, DOWN, buff=0.15).align_to(grid, LEFT)
        cells = ix["terms"] * ix["docs"]
        notes = VGroup(
            wrapped_label(rf"for the novels: \ a row for each of {ix['terms']:,} terms, \ a column for each of "
                          rf"{ix['docs']:,} passages: \ {cells / 1e6:.0f} million cells", 4.6, font_size=20,
                          color=WHITE),
            wrapped_label(rf"only {ix['postings']:,} are marked: \ {100 * ix['postings'] / cells:.2f}\%", 4.6,
                          font_size=20, color=HEAD),
            wrapped_label(r"keep only the marks: \ for each term, \ the sorted list of passages that contain it, \ "
                          r"its \textbf{postings}", 4.6, font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([4.45, 0.1, 0])
        packed = VGroup(*[VGroup(*[d.copy().move_to([x0 + (k + 0.5) * cell, d.get_y(), 0]).set_color(YES)
                                   for k, d in enumerate(r)]) for r in rows])
        with self.voiceover(
            "Without an index, every query must read all four and a half million tokens of the novels. "
            "<bookmark mark='a'/> Picture instead a table with a row for every term and a column for every passage, "
            "marked where the term occurs. For our novels that is forty thousand six hundred and ninety-two rows by "
            "eleven thousand two hundred and sixty-one columns: four hundred and fifty-eight million cells. "
            "<bookmark mark='b'/> Only two point three six million are marked, about half of one per cent. "
            "<bookmark mark='c'/> So keep only the marks: for each term, the sorted list of passages that contain "
            "it, called its postings. The text, turned on its side, has become an inverted index: from words to "
            "passages."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(grid), FadeIn(names), FadeIn(cap), FadeIn(illus), run_time=1.5)
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15), FadeIn(notes[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeOut(grid), FadeOut(cap), Transform(dots, packed), FadeIn(notes[2]), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def postings(self):
        ix = load("index")
        head = label(r"Dictionary and postings", font_size=36).to_edge(UP, buff=0.3)
        terms = ["whale", "ahab", "darci", "holm"]
        rows = VGroup()
        for k, t in enumerate(terms):
            y = 1.55 - k * 0.95
            box = RoundedRectangle(width=2.3, height=0.56, corner_radius=0.08, stroke_color=HEAD, stroke_width=1.6,
                                   fill_color=BG, fill_opacity=1).move_to([-5.55, y, 0])
            tt = mono(t, size=20, color=WHITE).move_to(box).align_to(box, LEFT).shift(RIGHT * 0.15)
            df = label(f"{ix['df'][t]}", font_size=22, color=HEAD).move_to(box).align_to(box, RIGHT).shift(LEFT * 0.15)
            ids = VGroup(*[tag_box(str(d), color=DATA, size=18, w=0.78, h=0.5) for d in ix["sample"][t][:11]])
            ids.arrange(RIGHT, buff=0.07).move_to([0, y, 0]).align_to([-3.55, 0, 0], LEFT)
            more = label(r"\dots", font_size=22, color=GREY_B).next_to(ids, RIGHT, buff=0.12)
            arr = Arrow(box.get_right(), ids.get_left(), buff=0.06, stroke_width=2, color=GREY_B,
                        max_tip_length_to_length_ratio=0.3)
            rows.add(VGroup(VGroup(box, tt, df), arr, ids, more))
        h1 = label(r"dictionary: \ term, \ df", font_size=21, color=HEAD).next_to(rows[0][0], UP, buff=0.2)
        h2 = label(r"postings: \ passage ids, \ each with its positions", font_size=21, color=DATA).next_to(
            rows[0][2], UP, buff=0.2).align_to(rows[0][2], LEFT)
        wl = ix["sample"]["whale"]
        n_run = next((k for k in range(1, len(wl)) if wl[k] != wl[k - 1] + 1), len(wl))
        run = SurroundingRectangle(VGroup(*rows[0][2][:min(n_run, 11)]), color=YES, buff=0.06, stroke_width=2.5)
        notes = VGroup(
            wrapped_label(r"\textbf{dictionary}: \ each term, \ its document frequency \ (df), \ and where its list "
                          r"begins; \ a hash table \ (Part 17), \ or a sorted array or tree for prefix searches",
                          12.4, font_size=20, color=HEAD),
            wrapped_label(rf"\textbf{{postings}}: \ passage ids in increasing order, \ each with the positions of "
                          rf"the term; \ a passage averages {ix['tokens'] / ix['docs']:.0f} tokens and "
                          rf"{ix['postings'] / ix['docs']:.0f} distinct terms", 12.4, font_size=20, color=DATA),
            wrapped_label(rf"\texttt{{whale}} opens with a run, \ {wl[0]} to {wl[n_run - 1]}: \ the first passages of "
                          r"\textit{Moby-Dick}, \ with its pages of quotations about whales; \ runs mean small gaps "
                          r"\ (Chapter 4)", 12.4, font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "An inverted index has two parts. <bookmark mark='a'/> The dictionary holds every term with its "
            "document frequency, the number of passages that contain it, and the place where its list begins. "
            "Whale is in three hundred and ninety passages, Ahab in a hundred and eighty-one. The dictionary can be "
            "a hash table, from Part 17, or a sorted tree, which also allows prefix searches. "
            "<bookmark mark='b'/> The postings hold passage numbers in increasing order, each with the positions "
            "where the term occurs. The next chapters rely on that order: sorted lists merge, and neighbours are "
            "close. <bookmark mark='c'/> Whale begins with a run, passages six hundred and "
            "fifty-nine to six hundred and sixty-nine: the opening of Moby-Dick, with its pages of quotations about "
            "whales. Words cluster, and clusters compress."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(h1), *[FadeIn(r[0]) for r in rows], FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(h2), *[GrowArrow(r[1]) for r in rows], FadeIn(notes[1]))
            self.play(LaggedStart(*[FadeIn(VGroup(r[2], r[3]), shift=RIGHT * 0.2) for r in rows], lag_ratio=0.3),
                      run_time=2)
            vo.wait_until("c")
            self.play(Create(run), FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def sorting(self):
        ix = load("index")
        head = label(r"Building it by sorting", font_size=36).to_edge(UP, buff=0.3)
        passages = ["the whale and the sea", "the white whale", "the sea"]
        docs = label(r"\ \qquad ".join(rf"{k}: \ \texttt{{{p}}}" for k, p in enumerate(passages, 1)), font_size=20,
                     color=GREY_A).next_to(head, DOWN, buff=0.3)
        illus = note(r"illustrative", font_size=17).next_to(docs, RIGHT, buff=0.3)
        pairs = []
        for k, p in enumerate(passages, 1):
            for t in dict.fromkeys(p.split()):
                pairs.append((t, k))
        order = sorted(range(len(pairs)), key=lambda i: pairs[i])

        def pbox(t, d, col):
            return tag_box(f"{t:<6}{d}", color=col, size=19, w=1.85, h=0.4)
        col1 = VGroup(*[pbox(t, d, DATA) for t, d in pairs]).arrange(DOWN, buff=0.07)
        col1.move_to([-5.7, 0, 0]).align_to([0, 1.6, 0], UP)
        col2 = VGroup(*[pbox(*pairs[i], HEAD) for i in order]).arrange(DOWN, buff=0.07)
        col2.move_to([-3.25, 0, 0]).align_to([0, 1.6, 0], UP)
        t1 = label(r"pairs, \ in passage order", font_size=20, color=DATA).next_to(col1, UP, buff=0.15)
        t2 = label(r"sorted", font_size=20, color=HEAD).next_to(col2, UP, buff=0.15)
        t3 = label(r"postings", font_size=20, color=YES).next_to(col2, UP, buff=0.15).set_x(-0.55)
        groups = {}
        for slot, i in enumerate(order):
            groups.setdefault(pairs[i][0], []).append((slot, pairs[i][1]))
        col3 = VGroup()
        for t, items in groups.items():
            y = sum(col2[s].get_y() for s, _ in items) / len(items)
            term = mono(t, size=19, color=YES).move_to([0, y, 0]).align_to([-1.2, 0, 0], RIGHT)
            ids = VGroup(*[tag_box(str(d), color=YES, size=19, w=0.46, h=0.4) for _, d in items])
            ids.arrange(RIGHT, buff=0.07).move_to([0, y, 0]).align_to([-1.05, 0, 0], LEFT)
            col3.add(VGroup(term, ids))
        notes = VGroup(
            wrapped_label(rf"the novels give {ix['postings']:,} (term, \ passage) pairs; \ at 8 bytes a pair, \ "
                          rf"{8 * ix['postings'] / 1e6:.0f} MB: \ one sort in memory", 5.2, font_size=21,
                          color=WHITE),
            wrapped_label(r"a web crawl will not fit: \ sort blocks that do, \ write each to disk as a sorted run, \ "
                          r"then merge the runs \ --- \ Part 16's external sort; \ this is \textbf{blocked "
                          r"sort-based indexing}", 5.2, font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([4.15, -0.2, 0])
        with self.voiceover(
            "How is the index built? The simplest way is to sort. <bookmark mark='a'/> Read the passages in order, "
            "and write down a pair for every term in each: the term and the passage number. "
            "<bookmark mark='b'/> Sort the pairs by term, and within a term by passage. <bookmark mark='c'/> Now "
            "each term's pairs sit together, and reading them off gives its postings, already in order. The novels "
            "make two point three six million pairs; at eight bytes a pair, that is nineteen megabytes, one sort in "
            "memory. <bookmark mark='d'/> A crawl of the web makes far more pairs than any memory holds. So sort as "
            "many as fit, write each sorted block to disk as a run, and merge the runs: Part 16's external sort, "
            "unchanged. This is blocked sort-based indexing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(docs), FadeIn(illus))
            vo.wait_until("a")
            self.play(FadeIn(t1), LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in col1], lag_ratio=0.15),
                      run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(t2), *[TransformFromCopy(col1[i], col2[slot], path_arc=-0.6)
                                    for slot, i in enumerate(order)], run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(t3), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in col3], lag_ratio=0.2),
                      run_time=1.5)
            self.play(FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def spimi(self):
        ix = load("index")
        head = label(r"Single pass, \ in memory", font_size=36).to_edge(UP, buff=0.3)
        stream = [(1, ["the", "whale", "sea"]), (2, ["the", "ahab", "whale"]), (3, ["the", "sea", "ship"])]
        pbs = VGroup(*[tag_box(f"passage {k}", color=DATA, size=19, h=0.5) for k, _ in stream]).arrange(
            DOWN, buff=0.35).move_to([-5.6, 0.85, 0])
        frame = RoundedRectangle(width=4.9, height=3.0, corner_radius=0.12, stroke_color=KERN, stroke_width=2)
        frame.move_to([-1.2, 0.65, 0])
        ftitle = label(r"memory: \ a hash table", font_size=20, color=KERN).next_to(frame, UP, buff=0.1)
        xs = frame.get_left()[0] + 0.25
        slots = [frame.get_top()[1] - 0.38 - k * 0.55 for k in range(5)]
        rows, row_of = {}, []
        steps = []
        for k, ts in stream:
            anims = []
            for t in ts:
                if t not in rows:
                    term = mono(t, size=20, color=WHITE).move_to([0, slots[len(rows)], 0]).align_to([xs, 0, 0], LEFT)
                    rows[t] = VGroup(term)
                    row_of.append(t)
                    anims.append(FadeIn(term))
                r = rows[t]
                num = mono(str(k), size=20, color=DATA).move_to([xs + 1.5 + 0.5 * (len(r) - 1), r[0].get_y(), 0])
                r.add(num)
                anims.append(FadeIn(num, shift=LEFT * 0.3))
            steps.append((k - 1, anims))
        content = VGroup(*[rows[t] for t in row_of])
        disk_t = label(r"disk", font_size=20, color=GREY_A).move_to([4.4, 2.35, 0])
        blocks = VGroup()
        for b in range(3):
            r = Rectangle(width=1.5, height=1.1, stroke_color=LAM, stroke_width=2, fill_color=LAM,
                          fill_opacity=0.12)
            t = label(rf"block {b + 1}", font_size=19, color=WHITE).move_to(r).shift(UP * 0.17)
            s = label(r"sorted", font_size=17, color=GREY_A).move_to(r).shift(DOWN * 0.2)
            blocks.add(VGroup(r, t, s))
        blocks.arrange(RIGHT, buff=0.15).move_to([4.4, 1.45, 0])
        final = RoundedRectangle(width=3.6, height=0.6, corner_radius=0.1, stroke_color=YES, stroke_width=2,
                                 fill_color=YES, fill_opacity=0.12).move_to([4.4, -0.2, 0])
        final_t = label(r"the index", font_size=21, color=WHITE).move_to(final)
        merges = VGroup(*[Arrow(b.get_bottom(), final.get_top(), buff=0.06, stroke_width=2, color=YES,
                                max_tip_length_to_length_ratio=0.2) for b in blocks])
        notes = VGroup(
            wrapped_label(r"Heinz and Zobel \ (2003): \ no table of term ids; \ a hash table maps each term to a "
                          r"growing list, \ and since passages arrive in order, \ every list is born sorted", 12.4,
                          font_size=20, color=WHITE),
            wrapped_label(r"when memory fills: \ sort the terms, \ write the block to disk, \ empty the table, \ "
                          r"go on", 12.4, font_size=20, color=LAM),
            wrapped_label(rf"at the end, \ merge all the blocks at once \ (a $k$-way merge, \ Part 16); \ our builder "
                          rf"is this with a single block: \ one pass over {ix['docs']:,} passages", 12.4,
                          font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(frame, DOWN, buff=0.7).set_x(0)
        with self.voiceover(
            "Blocked sorting needs a table from every term to an integer, kept in memory throughout, and it sorts "
            "pairs that could have been grouped as they arrived. <bookmark mark='a'/> Single-pass in-memory "
            "indexing, described by Steffen Heinz and Justin Zobel in 2003, uses a hash table instead. Each term "
            "maps to a growing list, and because passages arrive in order, every list is born sorted. "
            "<bookmark mark='b'/> When memory fills, the terms are sorted, the block is written to disk, and the "
            "table starts again, empty. <bookmark mark='c'/> At the end, all the blocks are merged at once, as in "
            "Part 16. Our own builder is this algorithm with a single block: one pass over every passage."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pbs), Create(frame), FadeIn(ftitle), FadeIn(disk_t))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            for k, anims in steps:
                self.play(Indicate(pbs[k], color=HEAD, scale_factor=1.1), run_time=0.5)
                self.play(*anims, run_time=0.8)
            vo.wait_until("b")
            ordered = sorted(row_of)
            self.play(*[rows[t].animate.set_y(slots[ordered.index(t)]) for t in row_of], run_time=1.2)
            self.play(FadeIn(notes[1]), FadeTransform(content.copy(), blocks[0]), run_time=1.2)
            self.play(FadeOut(content), FadeIn(blocks[1]), run_time=0.8)
            self.play(FadeIn(blocks[2]), run_time=0.8)
            vo.wait_until("c")
            self.play(*[GrowArrow(a) for a in merges], FadeIn(final), FadeIn(final_t), FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def segments(self):
        head = label(r"Indexes that change", font_size=36).to_edge(UP, buff=0.3)
        unit = 1.0

        def state(sizes):
            g = VGroup()
            for s in sizes:
                r = Rectangle(width=unit * s - 0.1, height=0.8, stroke_color=LAM, stroke_width=2, fill_color=LAM,
                              fill_opacity=0.25)
                g.add(VGroup(r, label(f"{s}", font_size=22, color=WHITE).move_to(r)))
            g.arrange(RIGHT, buff=0.1)
            return g.move_to([0, 1.0, 0]).align_to([-4.4, 0, 0], LEFT)
        seq = [[1], [1, 1], [2], [2, 1], [2, 1, 1], [2, 2], [4], [4, 1], [4, 1, 1], [4, 2], [4, 2, 1], [4, 2, 1, 1],
               [4, 2, 2], [4, 4], [8]]
        cap = label(r"segments on disk, \ oldest on the left \ (sizes in flushes of the memory index)", font_size=20,
                    color=GREY_A).move_to([0, 2.1, 0]).align_to([-4.4, 0, 0], LEFT)
        illus = note(r"illustrative", font_size=16).next_to(cap, RIGHT, buff=0.3)
        row = state(seq[0])
        bits = VGroup(*[Square(side_length=0.36, stroke_color=GREY_C, stroke_width=1.2,
                               fill_color=NO if k in (3, 9, 10) else BG, fill_opacity=0.9 if k in (3, 9, 10) else 1)
                        for k in range(16)]).arrange(RIGHT, buff=0.05)
        bl = label(r"deleted documents: \ a bitmap", font_size=21, color=NO)
        bitrow = VGroup(bl, bits).arrange(RIGHT, buff=0.3).move_to([0, -0.35, 0]).align_to([-4.4, 0, 0], LEFT)
        notes = VGroup(
            wrapped_label(r"new documents go into a small index in memory, \ searched beside the others; \ when it "
                          r"fills, \ it is written out as a \textbf{segment}", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"segments of equal size are merged, \ like carries in a binary counter: \ each posting "
                          r"is copied only about $\log_2 n$ times in $n$ flushes", 12.4, font_size=20, color=LAM),
            wrapped_label(r"deletions are marked in a bitmap and dropped at the next merge; \ Lucene, \ beneath "
                          r"Elasticsearch and OpenSearch, \ keeps immutable segments merged in much this way, \ like "
                          r"Part 34's LSM trees", 12.4, font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(bitrow, DOWN, buff=0.9).set_x(0)
        with self.voiceover(
            "Real collections change. <bookmark mark='a'/> New documents go into a small index in memory, searched "
            "beside the others, and when it fills it is written out as a segment. <bookmark mark='b'/> Segments of "
            "equal size are merged, like the carries of a binary counter, so each posting is copied only a "
            "logarithmic number of times. <bookmark mark='c'/> Deleted documents are marked in a bitmap, and "
            "dropped at the next merge. Lucene, the library beneath Elasticsearch and OpenSearch, keeps its index "
            "as immutable segments merged in much this way: the design of Part 34's log-structured merge trees."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap), FadeIn(illus))
            vo.wait_until("a")
            self.play(FadeIn(row), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            for s in seq[1:]:
                self.play(Transform(row, state(s)), run_time=0.5)
            vo.wait_until("c")
            self.play(FadeIn(bitrow), FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()
