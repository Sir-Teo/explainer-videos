from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs47.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, tag_box

# An illustrative ranked list of ten passages with graded judgments (2 highly relevant, 1 relevant, 0 not), and the
# number of relevant passages in the whole collection (one relevant passage is never retrieved).
GRADES = [2, 0, 1, 2, 0, 0, 1, 0, 2, 0]
TOTAL_REL = 6
ALL_GRADES = [2, 2, 2, 1, 1, 1]          # every judged relevant passage: the ideal order


def _row(grades, size=0.62):
    """The ranked list as a row of squares, coloured by grade, with ranks above."""
    g = VGroup()
    for i, gr in enumerate(grades):
        col = (GREY_D, DATA, YES)[gr]
        sq = Square(size, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.35 if gr else 0.1)
        rk = label(f"{i + 1}", font_size=16, color=GREY_B).next_to(sq, UP, buff=0.08)
        g.add(VGroup(sq, rk))
    return g.arrange(RIGHT, buff=0.16)


class Evaluation(WatchScene):
    def construct(self):
        self.card()
        self.precision()
        self.average()
        self.ndcg()
        self.ours()
        self.significance()

    def card(self):
        self.chapter(6, r"Is the ranking good?", r"How do you know one ranking beats another?", lit=(1992, 2002), extra=((1992, r"the first TREC, \ at NIST"),
                                                     (2002, r"J\"arvelin \& Kek\"al\"ainen: \ nDCG")), part=PART, said="Chapter six. Is the ranking good?")

    def precision(self):
        head = label(r"Precision and recall", font_size=36).to_edge(UP, buff=0.3)
        row = _row(GRADES, size=0.75).move_to([0.6, 1.95, 0])
        rel = [1 if g else 0 for g in GRADES]
        hits = [sum(rel[:k + 1]) for k in range(10)]
        pk = VGroup(*[label(f"{hits[k] / (k + 1):.2f}", font_size=18, color=HEAD).next_to(row[k][0], DOWN, buff=0.35)
                      for k in range(10)])
        rk = VGroup(*[label(f"{hits[k] / TOTAL_REL:.2f}", font_size=18, color=LAM).next_to(pk[k], DOWN, buff=0.22)
                      for k in range(10)])
        pl = label(r"P@$k$", font_size=19, color=HEAD).next_to(pk, LEFT, buff=0.35)
        rl = label(r"R@$k$", font_size=19, color=LAM).next_to(rk, LEFT, buff=0.35)
        ll = label(r"rank", font_size=17, color=GREY_B).next_to(row, LEFT, buff=0.35).shift(UP * 0.35)
        ill = note(rf"illustrative: \ a ranking of ten passages; \ {TOTAL_REL} relevant passages exist, \ one never "
                   r"retrieved", font_size=18).next_to(rk, DOWN, buff=0.4)
        defs = VGroup(
            MathTex(r"\text{P@}k = \frac{|\,\text{relevant} \cap \text{top } k\,|}{k}", font_size=32, color=HEAD),
            MathTex(r"\text{R@}k = \frac{|\,\text{relevant} \cap \text{top } k\,|}{|\,\text{relevant}\,|}",
                    font_size=32, color=LAM),
        ).arrange(RIGHT, buff=1.2).next_to(ill, DOWN, buff=0.6)
        foot = wrapped_label(r"read further down the list and recall can only rise, \ while precision tends to fall: "
                             r"\ one number per cutoff is not enough", 12.4, font_size=20,
                             color=WHITE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "To improve a ranking, we have to measure it. <bookmark mark='a'/> Here is a ranking of ten passages, the "
            "relevant ones in colour. <bookmark mark='b'/> Precision at k is the fraction of the top k that is "
            "relevant: how much of what the reader sees is useful. <bookmark mark='c'/> Recall at k is the fraction "
            "of all relevant passages that the top k contains. Six exist here, and one is never retrieved. <bookmark "
            "mark='d'/> Reading further down, recall can only rise, while precision tends to fall, so one cutoff "
            "tells only part of the story."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s) for s in row], lag_ratio=0.1), FadeIn(ll), FadeIn(ill), run_time=1.5)
            vo.wait_until("b")
            self.play(Write(defs[0]), FadeIn(pl), LaggedStart(*[FadeIn(t) for t in pk], lag_ratio=0.1), run_time=2)
            vo.wait_until("c")
            self.play(Write(defs[1]), FadeIn(rl), LaggedStart(*[FadeIn(t) for t in rk], lag_ratio=0.1), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def average(self):
        b = load("bm25")["mean"]
        head = label(r"Average precision", font_size=36).to_edge(UP, buff=0.3)
        row = _row(GRADES, size=0.7).move_to([0, 2.0, 0])
        rel = [1 if g else 0 for g in GRADES]
        terms, marks = [], VGroup()
        h = 0
        for k, r in enumerate(rel):
            if r:
                h += 1
                terms.append(h / (k + 1))
                marks.add(VGroup(SurroundingRectangle(row[k][0], color=HEAD, buff=0.07, stroke_width=3),
                                 label(rf"$\frac{{{h}}}{{{k + 1}}}$", font_size=32, color=HEAD).next_to(
                                     row[k][0], DOWN, buff=0.3)))
        ap = sum(terms) / TOTAL_REL
        sumtex = " + ".join(f"{t:.2f}" for t in terms)
        eq = MathTex(r"\text{AP} = \frac{1}{|\,\text{relevant}\,|} \sum_{k \,:\, \text{rank } k \text{ relevant}} "
                     r"\text{P@}k", font_size=34, color=WHITE).next_to(row, DOWN, buff=1.3)
        calc = MathTex(rf"= \frac{{{sumtex} + 0}}{{{TOTAL_REL}}} = {ap:.2f}", font_size=32, color=HEAD)
        calc.next_to(eq, DOWN, buff=0.3)
        miss = label(r"the passage never retrieved adds 0", font_size=18, color=NO).next_to(calc, DOWN, buff=0.2)
        lines = VGroup(
            wrapped_label(r"one number that rewards putting relevant passages high and finding all of them; \ "
                          r"roughly the area under the precision--recall curve", 12.4, font_size=20, color=GREY_A),
            wrapped_label(rf"\textbf{{MAP}}: \ the mean over queries; \ on our nine \ (cut at ten): \ BM25 "
                          rf"{b['bm25']['ap']:.2f}, \ tf-idf {b['tfidf']['ap']:.2f}", 12.4, font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Average precision folds the list into one number. <bookmark mark='a'/> At each rank where a relevant "
            "passage appears, take the precision so far: one of one, two of three, three of four, and so on. "
            "<bookmark mark='b'/> Add them up and divide by the number of relevant passages, so the one never "
            "retrieved counts zero: here, point five nine. It rewards ranking relevant passages high and finding them "
            "all. <bookmark mark='c'/> Its mean over queries is MAP. On our nine test queries, cut at ten results, "
            "BM25 scores point eight zero and tf-idf point seven five."
        ) as vo:
            self.play(FadeIn(head), FadeIn(row))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.3), run_time=2)
            vo.wait_until("b")
            self.play(Write(eq))
            self.play(FadeIn(calc), FadeIn(miss), FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def ndcg(self):
        self.ask(r"A relevant passage at rank 10, against rank 1. \\ It counts...", [r"the same",
                 r"less, discounted by the log of its rank"], 1,
                 say="A relevant passage appears at rank ten instead of rank one. How much does it count?",
                 reveal="Less, discounted by the logarithm of its rank: readers rarely look that far.")
        head = label(r"Graded relevance: \ nDCG", font_size=36).to_edge(UP, buff=0.3)
        unit, bw, gap = 0.55, 0.42, 0.14
        x0 = -6.3

        def bars(grades, base_y, discount):
            g = VGroup()
            for i, gr in enumerate(grades):
                gain = 2 ** gr - 1
                v = gain / math.log2(i + 2) if discount else gain
                col = (GREY_D, DATA, YES)[gr]
                h = max(0.02, v * unit)
                g.add(Rectangle(width=bw, height=h, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                    [x0 + i * (bw + gap) + bw / 2, base_y + h / 2, 0]))
            return g
        ideal_grades = (ALL_GRADES + [0] * 10)[:10]
        y1, y2 = 0.2, -2.6
        raw = bars(GRADES, y1, False)
        disc = bars(GRADES, y1, True)
        ideal = bars(ideal_grades, y2, True)
        span = 10 * (bw + gap) - gap
        base1 = Line([x0 - 0.1, y1, 0], [x0 + span + 0.1, y1, 0], color=GREY_C, stroke_width=1.5)
        base2 = Line([x0 - 0.1, y2, 0], [x0 + span + 0.1, y2, 0], color=GREY_C, stroke_width=1.5)
        t1 = label(r"this ranking: \ gain at each rank", font_size=18, color=GREY_A).next_to(base1, DOWN, buff=0.12)
        t1.align_to(base1, LEFT)
        t1b = label(r"this ranking: \ gain $\times$ discount", font_size=18, color=GREY_A)
        t1b.move_to(t1, aligned_edge=LEFT)
        t2 = label(r"the ideal order of all judged passages", font_size=18, color=GREY_A)
        t2.next_to(base2, DOWN, buff=0.12)
        t2.align_to(base2, LEFT)

        def dcg(gs):
            return sum((2 ** g - 1) / math.log2(i + 2) for i, g in enumerate(gs[:10]))
        D, ID = dcg(GRADES), dcg(ideal_grades)
        W = 6.6
        right = VGroup(
            MathTex(r"\text{gain} = 2^{g} - 1", font_size=32, color=WHITE),
            wrapped_label(r"grades $g = 0, 1, 2$: \ a highly relevant passage is worth three relevant ones", W,
                          font_size=18, color=GREY_B),
            MathTex(r"\text{DCG@}k = \sum_{i=1}^{k} \frac{2^{g_i} - 1}{\log_2(i + 1)}", font_size=32, color=DATA),
            wrapped_label(r"readers work down from the top: \ rank 1 counts in full, \ rank 10 under a third", W,
                          font_size=18, color=GREY_B),
            MathTex(r"\text{nDCG@}k = \frac{\text{DCG@}k}{\text{IDCG@}k}", font_size=32, color=YES),
            wrapped_label(r"divide by the DCG of the ideal order, \ so every query scores between 0 and 1", W,
                          font_size=18, color=GREY_B),
            label(rf"here: \ {D:.2f} / {ID:.2f} = {D / ID:.2f}", font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        right.next_to(head, DOWN, buff=0.45).to_edge(RIGHT, buff=0.35)
        ill = note(r"the illustrative ranking again", font_size=17).next_to(head, DOWN, buff=0.35).to_edge(LEFT,
                                                                                                      buff=0.6)
        with self.voiceover(
            "But relevance comes in degrees, and readers rarely reach the bottom. Järvelin and Kekäläinen's measure "
            "of 2002 handles both. <bookmark mark='a'/> Each passage gets a grade, and a gain of two to the grade "
            "minus one, so a highly relevant passage is worth three relevant ones. <bookmark mark='b'/> Discount each "
            "gain by the log of its rank plus one: rank one counts in full, rank ten under a third. The sum is the "
            "discounted cumulative gain. <bookmark mark='c'/> Divide by the same sum for the ideal order of every "
            "judged passage, and each query scores between zero and one, however many relevant passages it has. Here, "
            "point eight zero."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ill), Create(base1), FadeIn(t1))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in raw], lag_ratio=0.08), Write(right[0]),
                      FadeIn(right[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(Transform(raw, disc), Transform(t1, t1b), Write(right[2]), FadeIn(right[3]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(base2), FadeIn(t2), LaggedStart(*[GrowFromEdge(r, DOWN) for r in ideal],
                                                             lag_ratio=0.08), run_time=1.5)
            self.play(Write(right[4]), FadeIn(right[5]))
            self.play(FadeIn(right[6]))
        self.wait(0.4)
        self.clear_scene()


    def ours(self):
        b = load("bm25")
        rows_d = b["rows"]
        head = label(r"Our nine queries", font_size=36).to_edge(UP, buff=0.3)
        rows = [[rf"``{r['query']}''", rf"\textit{{{r['book']}}}", f"{r['relevant']}", f"{r['bm25']['ndcg']:.2f}",
                 f"{r['tfidf']['ndcg']:.2f}"] for r in rows_d]
        rows.append([r"\textbf{mean}", "", "", f"{b['mean']['bm25']['ndcg']:.2f}", f"{b['mean']['tfidf']['ndcg']:.2f}"])
        tab = grid_table([r"query", r"meant for", r"grade-2 passages", r"nDCG@10 BM25", r"tf-idf"], rows,
                         widths=[3.3, 4.3, 2.0, 1.8, 1.3], row_h=0.37, font_size=18, mono_cols=())
        tab.next_to(head, DOWN, buff=0.35)
        sh = next(i for i, r in enumerate(rows_d) if r["query"] == "sherlock holmes")
        vc = next(i for i, r in enumerate(rows_d) if r["query"] == "vampire count")
        for i in (sh, vc):
            for cell in tab.cells[i + 1]:
                cell.set_color(NO)
        for cell in tab.cells[len(rows)]:
            cell.set_color(HEAD)
        wrong = round((1 - rows_d[sh]["bm25"]["p10"]) * 10)
        notes = VGroup(
            wrapped_label(rf"``sherlock holmes'': \ {wrong} of BM25's top ten come from \textit{{The Hound of the "
                          r"Baskervilles}, \ which our rule cannot count: \ the judgments are wrong, \ not the "
                          r"ranking", 12.4, font_size=19, color=NO),
            wrapped_label(r"``vampire count'': \ \textit{The Count of Monte Cristo} is full of the word "
                          r"\textit{count}: \ the query is ambiguous", 12.4, font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(tab, DOWN, buff=0.5).set_x(0)
        with self.voiceover(
            "Here are our nine queries. <bookmark mark='a'/> For most, both rankers fill the top ten with relevant "
            "passages, and nDCG is one: names are easy. <bookmark mark='b'/> Sherlock Holmes scores point six zero "
            "for both, and the fault is ours. Four of the top ten come from The Hound of the Baskervilles, which has "
            "Holmes in it too, but our rule counts only the Adventures. A bad score can be a bad judgment. <bookmark "
            "mark='c'/> Vampire count is a real failure: The Count of Monte Cristo is full of the word count. "
            "<bookmark mark='d'/> On average, BM25 scores point eight five and tf-idf point eight three."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:len(rows)]], lag_ratio=0.15),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(Indicate(VGroup(*tab.cells[sh + 1]), color=NO), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(Indicate(VGroup(*tab.cells[vc + 1]), color=NO), FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*tab.cells[len(rows)])))
        self.wait(0.4)
        self.clear_scene()

    def significance(self):
        b = load("bm25")
        diffs = [r["bm25"]["ndcg"] - r["tfidf"]["ndcg"] for r in b["rows"]]
        wins = sum(1 for d in diffs if d > 1e-12)
        losses = sum(1 for d in diffs if d < -1e-12)
        ties = len(diffs) - wins - losses
        n = wins + losses
        p = min(1.0, 2 * sum(math.comb(n, i) for i in range(min(wins, losses) + 1)) / 2 ** n) if n else 1.0
        head = label(r"Is the difference real?", font_size=36).to_edge(UP, buff=0.3)
        x0, x1, y = -5.6, 0.4, 0.6
        lo, hi = -0.1, 0.1

        def X(v):
            return x0 + (v - lo) / (hi - lo) * (x1 - x0)
        axis = Line([x0, y, 0], [x1, y, 0], color=GREY_C, stroke_width=1.5)
        tks = VGroup(*[VGroup(Line([X(v), y - 0.07, 0], [X(v), y + 0.07, 0], color=GREY_C),
                              label(f"{v:+.2f}" if v else "0", font_size=16, color=GREY_B).next_to([X(v), y, 0], DOWN,
                                                                                                  buff=0.15))
                       for v in (-0.1, -0.05, 0, 0.05, 0.1)])
        cap = label(r"nDCG@10, \ BM25 minus tf-idf, \ one dot per query", font_size=18, color=GREY_A).next_to(
            axis, DOWN, buff=0.6)
        dots, stack = VGroup(), {}
        for d in diffs:
            key = round(d, 3)
            k = stack.get(key, 0)
            stack[key] = k + 1
            col = YES if d > 1e-12 else (NO if d < -1e-12 else GREY_B)
            dots.add(Dot([X(d), y + 0.25 + 0.28 * k, 0], radius=0.1, color=col))
        means = label(rf"means: \ BM25 {b['mean']['bm25']['ndcg']:.3f}, \ tf-idf {b['mean']['tfidf']['ndcg']:.3f}",
                      font_size=20, color=WHITE).next_to(cap, DOWN, buff=0.35)
        W = 5.6
        right = VGroup(
            wrapped_label(rf"{ties} queries tie; \ {wins} favour BM25; \ {losses} favour tf-idf", W, font_size=20,
                          color=WHITE),
            wrapped_label(r"\textbf{sign test}: \ if neither ranker were better, \ each untied query would be a fair "
                          r"coin", W, font_size=19, color=GREY_A),
            wrapped_label(rf"{wins} heads in {n}: \ $p = 2 \times 2^{{-{n}}} = {p:.2f}$", W, font_size=21,
                          color=HEAD),
            wrapped_label(r"nine queries cannot tell; \ TREC tracks use about fifty topics, \ and the same paired "
                          r"tests and power calculations as Part 44's experiments", W, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        right.next_to(head, DOWN, buff=0.7).to_edge(RIGHT, buff=0.4)
        foot = wrapped_label(r"in production, \ judged sets are joined by clicks and online experiments: \ "
                             r"chapter 12", 12.4, font_size=19, color=LAM).next_to(means, DOWN, buff=0.8).set_x(0)
        with self.voiceover(
            "Is that difference real, or luck? <bookmark mark='a'/> Pair the rankers query by query. Six queries tie, "
            "three favour BM25, and none favour tf-idf. <bookmark mark='b'/> If neither were better, each untied "
            "query would be a fair coin. <bookmark mark='c'/> Three heads in three tosses has probability one in "
            "eight, or one in four counting tails as well: p is point two five. Nine queries cannot tell. <bookmark "
            "mark='d'/> That is why TREC tracks use about fifty topics, with the paired tests and power calculations "
            "of Part 44; and in production, judged sets are joined by clicks and online experiments, which chapter "
            "twelve takes up."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(tks), FadeIn(cap))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.15), FadeIn(means),
                      FadeIn(right[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(right[1]))
            vo.wait_until("c")
            self.play(FadeIn(right[2]))
            vo.wait_until("d")
            self.play(FadeIn(right[3]))
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, KERN)
