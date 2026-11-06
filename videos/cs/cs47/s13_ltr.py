from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs47.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load, module_box, mono, tag_box

# an illustrative ranked list for one query: six passages, their judged grades (0-3) and the model's scores
NAMES = ["A", "B", "C", "D", "E", "F"]
GRADES = [1, 0, 3, 0, 2, 0]
SCORES = [2.0, 1.6, 1.2, 0.9, 0.5, 0.2]
ETA = 3.0                         # the step (shrinkage times tree output) in the boosting picture
GRADE_COL = {0: GREY_B, 1: DATA, 2: HEAD, 3: YES}


def dcg(grades):
    return sum((2 ** g - 1) / math.log2(i + 2) for i, g in enumerate(grades))


IDEAL = dcg(sorted(GRADES, reverse=True))


def ndcg_of(scores):
    order = sorted(range(len(scores)), key=lambda k: -scores[k])
    return dcg([GRADES[d] for d in order]) / IDEAL


def lambdas(scores, weighted=True):
    """RankNet's pair gradients, summed per passage; LambdaRank multiplies each by |delta nDCG| of the swap."""
    order = sorted(range(len(scores)), key=lambda k: -scores[k])
    rank = {d: r for r, d in enumerate(order)}
    lam = [0.0] * len(scores)
    for i in range(len(scores)):
        for j in range(len(scores)):
            if GRADES[i] > GRADES[j]:
                w = abs((2 ** GRADES[i] - 2 ** GRADES[j]) * (1 / math.log2(rank[i] + 2) - 1 / math.log2(rank[j] + 2)))
                w = w / IDEAL if weighted else 1.0
                g = w / (1 + math.exp(scores[i] - scores[j]))
                lam[i] += g
                lam[j] -= g
    return lam


def row_mob(k, size=18):
    """One passage of the list: its name and its grade badge."""
    t = tag_box(rf"passage {NAMES[k]}", color=WHITE, size=size - 2, h=0.42, w=1.9)
    gb = tag_box(rf"{GRADES[k]}", color=GRADE_COL[GRADES[k]], size=size - 2, h=0.42, w=0.5)
    return VGroup(t, gb).arrange(RIGHT, buff=0.12)


class Ltr(VoiceoverScene):
    def construct(self):
        self.card()
        self.features()
        self.three()
        self.lambdas()
        self.mart()
        self.clicks()

    def card(self):
        card = chapter_card(12, r"Learning to rank", r"Hundreds of signals: \ how should they be combined?",
                            lit=(2005, 2010, 2017),
                            extra=((2005, r"Burges et al.: \ RankNet"), (2010, r"Burges: \ LambdaMART"),
                                   (2017, r"Joachims et al.: \ unbiased learning to rank")), part=PART)
        with self.voiceover("Chapter twelve. Learning to rank."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def features(self):
        ev = load("bm25")
        n_q = len(ev["rows"])
        head = label(r"Ranking as learning", font_size=36).to_edge(UP, buff=0.3)
        pair = VGroup(tag_box(r"query", color=DATA, size=17, h=0.45), label(r"$+$", font_size=26),
                      tag_box(r"passage", color=LAM, size=17, h=0.45)).arrange(DOWN, buff=0.15)
        pair.move_to([-5.6, 0.6, 0])
        feats = [(r"BM25", 0.8, DATA), (r"tf-idf cosine", 0.6, DATA), (r"phrase match", 0.3, HEAD),
                 (r"terms close together", 0.5, HEAD), (r"passage length", 0.4, GREY_B),
                 (r"PageRank \ (web)", 0.7, KERN), (r"clicks \ (web)", 0.55, LAM)]
        bars = VGroup()
        for r, (name, v, c) in enumerate(feats):
            y = 2.1 - r * 0.5
            b = Rectangle(width=2.0 * v, height=0.32, stroke_width=0, fill_color=c, fill_opacity=0.85)
            b.move_to([-0.15 + v, y, 0])
            t = label(name, font_size=19, color=c).move_to([-0.3, y, 0], aligned_edge=RIGHT)
            bars.add(VGroup(t, b))
        fbrace = Brace(bars, LEFT, buff=0.12, color=GREY_B)
        a1 = Arrow(pair.get_right(), fbrace.get_left(), buff=0.12, color=GREY_B, stroke_width=2)
        model = module_box(r"model $f$", YES, w=1.8, h=0.75).move_to([3.0, bars.get_y(), 0])
        a2 = Arrow(bars.get_right(), model.get_left(), buff=0.15, color=GREY_B, stroke_width=2)
        score = label(r"a score; \ sort", font_size=19, color=YES).next_to(model, RIGHT, buff=0.25)
        a3 = Arrow(model.get_right(), score.get_left(), buff=0.05, color=GREY_B, stroke_width=2)
        ill = label(r"feature values illustrative", font_size=16, color=GREY_B).next_to(bars, DOWN, buff=0.15)
        lines = VGroup(
            wrapped_label(rf"learn $f$ from judged queries: \ our {n_q}, \ graded by rule \ (Chapter 6), \ "
                          r"would be a tiny training set; \ Microsoft's MSLR-WEB30K describes each query and page "
                          r"by 136 features", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"the question is the loss: \ what, \ exactly, \ should $f$ get right?", 12.4,
                          font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "BM25 is one signal. A web engine has hundreds. <bookmark mark='a'/> For each query and passage it "
            "computes a vector of features: BM25 and tf-idf, whether the phrase occurs, how close the terms sit, "
            "the length, and on the web PageRank and the clicks of past users. <bookmark mark='b'/> Hand-tuning a "
            "formula that weighs a hundred of these is hopeless, so a model learns it from graded queries, like "
            f"our {n_q} from Chapter 6, but thousands of them, graded by people. "
            "Microsoft's public MSLR data set describes each query and page by a hundred and thirty-six features. "
            "<bookmark mark='c'/> The model outputs a score to sort by. The real question is what loss to "
            "train it on."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pair))
            vo.wait_until("a")
            self.play(GrowArrow(a1), GrowFromCenter(fbrace), LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.2),
                      FadeIn(ill), run_time=2.5)
            vo.wait_until("b")
            self.play(GrowArrow(a2), FadeIn(model), FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(GrowArrow(a3), FadeIn(score), FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def three(self):
        head = label(r"Pointwise, \ pairwise, \ listwise", font_size=36).to_edge(UP, buff=0.3)

        def mini(ks):
            return VGroup(*[row_mob(k, size=17) for k in ks]).arrange(DOWN, buff=0.14)
        ks = [0, 1, 2, 4]
        cols = VGroup()
        for _ in range(3):
            cols.add(mini(ks))
        cols.arrange(RIGHT, buff=1.55).next_to(head, DOWN, buff=1.0)
        titles = VGroup(*[label(t, font_size=24, color=c).next_to(col, UP, buff=0.3)
                          for t, c, col in zip((r"pointwise", r"pairwise", r"listwise"), (DATA, HEAD, YES), cols)])
        # pointwise: each passage regressed on its own grade
        pw = VGroup(*[Arrow(r.get_right(), r.get_right() + RIGHT * 0.5, buff=0.02, color=DATA, stroke_width=2,
                            max_tip_length_to_length_ratio=0.35) for r in cols[0]])
        # pairwise: arcs from the better passage of each pair to the worse
        pairs = [(i, j) for i in range(4) for j in range(4) if GRADES[ks[i]] > GRADES[ks[j]]]
        pp = VGroup(*[CurvedArrow(cols[1][i].get_right() + RIGHT * 0.05, cols[1][j].get_right() + RIGHT * 0.05,
                                  angle=-TAU / 5 if i < j else TAU / 5, color=HEAD, stroke_width=1.6, tip_length=0.12)
                      for i, j in pairs])
        lw = Brace(cols[2], RIGHT, color=YES, buff=0.08)
        lw_t = label(r"nDCG", font_size=18, color=YES).next_to(lw, RIGHT, buff=0.08)
        notes = VGroup(
            wrapped_label(r"predict each grade by regression; \ but only the order matters, \ and grades are not "
                          r"comparable across queries", 3.7, font_size=18, color=DATA),
            wrapped_label(r"for each pair the better passage should score higher: \ RankNet's loss "
                          r"$\log(1 + e^{-(s_i - s_j)})$ \ (Burges et al., \ 2005); \ every swap counts the same", 3.7,
                          font_size=18, color=HEAD),
            wrapped_label(r"score the whole list by the metric itself; \ but nDCG jumps when two scores cross and is "
                          r"flat between: \ no gradient \ (ListNet, \ 2007, \ smooths it)", 3.7, font_size=18,
                          color=YES),
        )
        for n, col in zip(notes, cols):
            n.next_to(col, DOWN, buff=0.45).set_x(col.get_x() + 0.2)
        ill = label(r"grades illustrative", font_size=16, color=GREY_B).next_to(titles, UP, buff=0.1).set_x(5.6)
        with self.voiceover(
            "There are three families of loss. <bookmark mark='a'/> Pointwise methods predict each passage's grade "
            "by regression, one at a time. But the user only ever sees an order, and grades are not comparable "
            "across queries. <bookmark mark='b'/> Pairwise methods look at pairs: "
            "whenever one passage is better than another, it should score higher. Burges and colleagues' RankNet, "
            "in 2005, used a logistic loss on the difference of the two scores. But it counts every misordered "
            "pair the same, whether at the top of the page or far below it. <bookmark mark='c'/> Listwise methods "
            "judge the whole list by the measure we care about, such as nDCG. But nDCG only changes when two scores "
            "cross, so it has no useful gradient."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cols), FadeIn(titles), FadeIn(ill))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a) for a in pw], lag_ratio=0.2), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(a) for a in pp], lag_ratio=0.2), FadeIn(notes[1]), run_time=2)
            vo.wait_until("c")
            self.play(GrowFromCenter(lw), FadeIn(lw_t), FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def lambdas(self):
        head = label(r"LambdaRank: \ the gradient nDCG would have", font_size=36).to_edge(UP, buff=0.3)
        formula = MathTex(r"\lambda_{ij} \;=\; \frac{1}{1 + e^{\,s_i - s_j}} \;\cdot\; "
                          r"\bigl|\Delta \mathrm{nDCG}_{ij}\bigr|", font_size=36).next_to(head, DOWN, buff=0.3)
        rows = VGroup()
        for r, k in enumerate(range(6)):
            rk = label(rf"{r + 1}", font_size=18, color=GREY_B)
            sc = label(rf"$s = {SCORES[k]:.1f}$", font_size=18, color=GREY_A)
            rows.add(VGroup(rk, row_mob(k), sc).arrange(RIGHT, buff=0.25))
        rows.arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to([-4.3, -0.45, 0])
        zero_x, half = 1.0, 2.2
        axis = Line([zero_x, rows.get_top()[1] + 0.1, 0], [zero_x, rows.get_bottom()[1] - 0.1, 0], color=GREY_C)
        up_l = label(r"push up", font_size=17, color=YES).next_to(axis.get_top(), UR, buff=0.08)
        dn_l = label(r"push down", font_size=17, color=NO).next_to(axis.get_top(), UL, buff=0.08)
        l_rank = lambdas(SCORES, weighted=False)
        l_lam = lambdas(SCORES)

        def bars(lam):
            m = max(abs(v) for v in lam)
            g = VGroup()
            for row, v in zip(rows, lam):
                w = max(0.02, half * abs(v) / m)
                b = Rectangle(width=w, height=0.34, stroke_width=0, fill_color=YES if v > 0 else NO,
                              fill_opacity=0.85)
                b.move_to([zero_x + (w / 2 if v > 0 else -w / 2), row.get_y(), 0])
                g.add(b)
            return g
        b_rank, b_lam = bars(l_rank), bars(l_lam)
        cap_rank = label(r"RankNet's pair gradients alone", font_size=18, color=HEAD)
        cap_lam = label(r"times the nDCG change of each swap", font_size=18, color=YES)
        for c in (cap_rank, cap_lam):
            c.next_to(axis, DOWN, buff=0.2)
        nd = label(rf"this order: \ nDCG $= {ndcg_of(SCORES):.2f}$ \ (illustrative grades and scores)",
                   font_size=18, color=GREY_A).next_to(rows, DOWN, buff=0.3).align_to(rows, LEFT)
        note = wrapped_label(r"never write the loss down: \ define its gradient. \ Passage C, \ grade 3 at rank 3, "
                             r"\ gets the strongest push, \ because moving it to the top changes nDCG most", 12.4,
                             font_size=19, color=WHITE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Burges and colleagues found a way round that in 2006. <bookmark mark='a'/> Take six graded "
            "passages, in the model's current order. <bookmark mark='b'/> RankNet's gradient pushes "
            "each passage up for every worse passage above it, and down for every better one below, by an amount "
            "that depends only on the two scores. <bookmark mark='c'/> LambdaRank multiplies each pair's push by how "
            "much nDCG would change if the two swapped places. Pairs near the top now dominate, and pairs low on "
            "the page barely count. <bookmark mark='d'/> The trick is to never write a loss down at all: define the "
            "gradient you want, the lambdas, and follow it. Passage C, the best, gets the strongest push."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows), FadeIn(nd))
            vo.wait_until("a")
            self.play(Create(axis), FadeIn(up_l), FadeIn(dn_l))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, LEFT if v > 0 else RIGHT) for b, v in zip(b_rank, l_rank)],
                                  lag_ratio=0.15), FadeIn(cap_rank))
            vo.wait_until("c")
            self.play(Write(formula))
            self.play(Transform(b_rank, b_lam), ReplacementTransform(cap_rank, cap_lam), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(note), Indicate(rows[2], color=YES))
        self.wait(0.4)
        self.clear_scene()

    def mart(self):
        head = label(r"LambdaMART: \ boosted trees on lambdas", font_size=36).to_edge(UP, buff=0.3)
        # rounds of boosting, each tree taken to fit the lambdas exactly (illustrative)
        states = [list(SCORES)]
        for _ in range(2):
            s = states[-1]
            states.append([a + ETA * b for a, b in zip(s, lambdas(s))])
        y_top, dy = 1.55, 0.58

        def place(scores):
            order = sorted(range(6), key=lambda k: -scores[k])
            return {k: y_top - r * dy for r, k in enumerate(order)}
        mobs = [row_mob(k) for k in range(6)]
        x_list = -4.6
        for k, y in place(states[0]).items():
            mobs[k].move_to([x_list, y, 0])
        ranks = VGroup(*[label(rf"{r + 1}", font_size=18, color=GREY_B).move_to([x_list - 1.65, y_top - r * dy, 0])
                         for r in range(6)])
        nd = [ndcg_of(s) for s in states]
        nd_t = [label(rf"nDCG $= {v:.2f}$", font_size=21, color=YES if v > 0.99 else HEAD) for v in nd]
        for t in nd_t:
            t.move_to([x_list, y_top - 6 * dy - 0.05, 0])

        def tree(feat, col):
            root = tag_box(feat, color=col, size=17, h=0.42)
            l1 = mono(r"+0.4", size=17, color=YES)
            l2 = mono(r"-0.2", size=17, color=NO)
            leaves = VGroup(l1, l2).arrange(RIGHT, buff=0.3).next_to(root, DOWN, buff=0.4)
            ed = VGroup(Line(root.get_bottom(), l1.get_top(), color=GREY_C, stroke_width=1.5),
                        Line(root.get_bottom(), l2.get_top(), color=GREY_C, stroke_width=1.5))
            return VGroup(root, leaves, ed)
        trees = VGroup(tree(r"BM25>8?", DATA), tree(r"phrase?", HEAD), tree(r"len<300?", GREY_B))
        plus = [label(r"$\eta\,\cdot$" if i == 0 else r"$+\;\eta\,\cdot$", font_size=26) for i in range(3)]
        f0 = label(r"$f(x) \;=\;$", font_size=26)
        dots = label(r"$+ \cdots$", font_size=24)
        expr = VGroup(f0, plus[0], trees[0], plus[1], trees[1], plus[2], trees[2], dots).arrange(RIGHT, buff=0.15)
        if expr.width > 9.4:
            expr.scale_to_fit_width(9.4)
        expr.move_to([2.0, 1.3, 0])
        ill = label(r"illustrative: \ scores, \ trees, \ and each tree fitting the lambdas exactly", font_size=16,
                    color=GREY_B).next_to(expr, DOWN, buff=0.25)
        lines = VGroup(
            wrapped_label(r"gradient boosting \ (\textit{AI, Built} \ Part 6): \ each round fits a small regression "
                          r"tree to the current lambdas, \ over the features, \ and adds it, \ shrunk by $\eta$", 8.6,
                          font_size=19, color=WHITE),
            wrapped_label(r"an ensemble of lambda-gradient models won the Yahoo! \ Learning to Rank Challenge \ "
                          r"(2010); \ LightGBM and XGBoost ship it as an objective today", 8.6, font_size=19,
                          color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([2.2, -1.55, 0])
        last = "one, the ideal order" if nd[2] > 0.999 else f"{nd[2]:.2f}"
        with self.voiceover(
            "Lambdas are gradients, and AI, Built Part 6 showed what to do with gradients over tabular features: "
            "boost trees. <bookmark mark='a'/> LambdaMART starts from some scores, computes every passage's lambda, "
            "and fits a small regression tree that predicts them from the features, added with a small weight. "
            "<bookmark mark='b'/> Then the lambdas are recomputed, and another tree fits them. In our picture "
            f"nDCG climbs from {nd[0]:.2f} to {nd[1]:.2f}, and "
            f"then to {last}. <bookmark mark='c'/> Because trees split on features, the model generalizes to "
            "queries it never saw. An ensemble built on these lambda gradients won Yahoo's Learning to Rank "
            "Challenge in 2010, and LightGBM and XGBoost offer it as a standard objective."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ranks), *[FadeIn(m) for m in mobs], FadeIn(nd_t[0]))
            vo.wait_until("a")
            self.play(FadeIn(f0), FadeIn(plus[0]), FadeIn(trees[0]), FadeIn(ill), FadeIn(lines[0]))
            for r in (1, 2):
                if r == 2:
                    vo.wait_until("b")
                self.play(*[mobs[k].animate.move_to([x_list, y, 0]) for k, y in place(states[r]).items()],
                          ReplacementTransform(nd_t[r - 1], nd_t[r]),
                          FadeIn(plus[r]), FadeIn(trees[r]), run_time=1.5)
            self.play(FadeIn(dots))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def clicks(self):
        head = label(r"Clicks and position bias", font_size=36).to_edge(UP, buff=0.3)
        n = 10
        exam = [1 / (1 + 0.45 * r) for r in range(n)]          # an illustrative examination curve
        attract = [0.5, 0.3, 0.7, 0.2, 0.4, 0.6, 0.3, 0.2, 0.5, 0.3]
        bw, gap, hmax = 0.42, 0.14, 3.0
        x0, y0 = -6.2, -1.4
        ex_bars, cl_bars, nums = VGroup(), VGroup(), VGroup()
        for r in range(n):
            x = x0 + r * (bw + gap) + bw / 2
            eb = Rectangle(width=bw, height=hmax * exam[r], stroke_color=DATA, stroke_width=1.5, fill_opacity=0)
            eb.move_to([x, y0 + hmax * exam[r] / 2, 0])
            cb = Rectangle(width=bw, height=hmax * exam[r] * attract[r], stroke_width=0, fill_color=LAM,
                           fill_opacity=0.85)
            cb.move_to([x, y0 + hmax * exam[r] * attract[r] / 2, 0])
            ex_bars.add(eb)
            cl_bars.add(cb)
            nums.add(label(rf"{r + 1}", font_size=16, color=GREY_B).move_to([x, y0 - 0.25, 0]))
        base = Line([x0 - 0.1, y0, 0], [x0 + n * (bw + gap), y0, 0], color=GREY_C)
        xl = label(r"rank on the page", font_size=17, color=GREY_B).next_to(nums, DOWN, buff=0.15)
        legend = VGroup(
            VGroup(Rectangle(width=0.3, height=0.2, stroke_color=DATA, stroke_width=1.5), label(
                r"chance the user looks", font_size=17, color=DATA)).arrange(RIGHT, buff=0.1),
            VGroup(Rectangle(width=0.3, height=0.2, stroke_width=0, fill_color=LAM, fill_opacity=0.85), label(
                r"chance of a click", font_size=17, color=LAM)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(ex_bars, UP, buff=0.3).align_to(base, LEFT)
        ill = label(r"illustrative", font_size=16, color=GREY_B).next_to(legend, RIGHT, buff=0.4).align_to(legend,
                                                                                                          DOWN)
        formula = MathTex(r"P(\text{click at } k) \;=\; P(\text{looked at } k)\; P(\text{relevant})",
                          font_size=28, color=WHITE)
        if formula.width > 5.5:
            formula.scale_to_fit_width(5.5)
        notes = VGroup(
            formula,
            wrapped_label(r"Joachims et al. \ (2005), \ eye tracking: \ users clicked the top result more often even "
                          r"when the top two were secretly swapped", 5.5, font_size=19, color=WHITE),
            wrapped_label(r"the cascade model \ (Craswell et al., \ 2008): \ read down the page, \ click the first "
                          r"attractive result, \ stop", 5.5, font_size=19, color=DATA),
            wrapped_label(r"\textbf{inverse propensity weighting} \ (Joachims, \ Swaminathan and Schnabel, \ 2017): "
                          r"\ weight a click at rank $k$ by $1 / P(\text{looked at } k)$, \ estimated by randomly "
                          r"swapping results", 5.5, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.75, -0.3, 0])
        with self.voiceover(
            "Judged queries are expensive; clicks are free, but biased. "
            "<bookmark mark='a'/> People mostly look at the top of the page, so a click depends on where a result "
            "was shown as well as on whether it was relevant. <bookmark mark='b'/> Joachims and colleagues showed "
            "this in 2005 with eye tracking: when the top two results were secretly swapped, users still clicked "
            "the first more often. <bookmark mark='c'/> In the cascade model of Craswell and colleagues, the user "
            "reads down the page and clicks the first result that looks right. <bookmark mark='d'/> To learn from "
            "clicks without learning the old ranking back, weight each click by one over the chance its position "
            "was looked at, measured by randomly swapping results: unbiased learning to rank."
        ) as vo:
            self.play(FadeIn(head), Create(base), FadeIn(nums), FadeIn(xl))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in ex_bars], lag_ratio=0.1), FadeIn(legend),
                      FadeIn(ill))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in cl_bars], lag_ratio=0.1), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, mono)
