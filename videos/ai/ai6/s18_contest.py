from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai6.common import BAD, GOOD, HIST, HL, chapter, era_strip, load

C2, C70 = C.TRUE_P, C.BITS
AUTH = ("#E86F8A", "#58A6FF")
LO = 0.70  # the bars start at 70% right


def board_leaders(rows):
    """All procedures tied at the highest finite seventy-rate fold mean."""
    finite = [r for r in rows if "70" in r and math.isfinite(r["70"]["cv"])]
    if not finite:
        return []
    best = max(r["70"]["cv"] for r in finite)
    return [r for r in finite if r["70"]["cv"] == best]


class Contest(VoiceoverScene):
    def construct(self):
        chapter(self, 17, r"The contest, and two cultures", r"Which method wins, and why do trees still rule tables?",
                "Chapter seventeen. The contest.", lit=(2001,))
        self.board()
        self.cultures()
        self.tables()
        self.today()

    # ------------------------------------------------------------------
    def board(self):
        b = load("board")
        rows = b["rows"]
        W = 2.5
        col2, col70 = -0.5, 3.4
        title = label(rf"Ten-fold cross-validation on all ${b['n']}$ pages: \ mean, \ and one standard deviation over folds",
                      font_size=28).to_edge(UP, buff=0.25)
        head = VGroup(label(r"$2$ rates", font_size=26, color=C2).move_to([col2 + W / 2, 2.85, 0]),
                      label(r"all $70$ rates", font_size=26, color=C70).move_to([col70 + W / 2, 2.85, 0]))
        lines = VGroup()
        for k, r in enumerate(rows):
            yv = 2.35 - 0.47 * k
            g = VGroup(label(r["name"], font_size=22, color=WHITE).move_to([-0.75, yv, 0], aligned_edge=RIGHT))
            for key, x0, col in (("2", col2, C2), ("70", col70, C70)):
                if key not in r:
                    g.add(VGroup(MathTex(r"\text{---}", font_size=22, color=GREY_D).move_to([x0 + 0.3, yv, 0])))
                    continue
                a, sd = r[key]["cv"], r[key]["sd"]
                L = W * (a - LO) / (1 - LO)
                bar = Rectangle(width=max(L, 0.02), height=0.26, stroke_width=0, fill_color=col, fill_opacity=0.85)
                bar.move_to([x0 + L / 2, yv, 0])
                e0, e1 = x0 + W * (max(a - sd, LO) - LO) / (1 - LO), x0 + W * (min(a + sd, 1.0) - LO) / (1 - LO)
                err = Line([e0, yv, 0], [e1, yv, 0], color=WHITE, stroke_width=2)
                val = MathTex(rf"{100 * a:.1f}", font_size=22, color=col).move_to([x0 + W + 0.45, yv, 0])
                g.add(VGroup(bar, err, val))
            lines.add(g)
        scale = note(r"bars: $70$--$100\%$; \ white: $\pm$ one s.d. across folds \\ error bars capped at the displayed axis limits", font_size=20).to_corner(DR, buff=0.20)
        a2 = [r["2"]["cv"] for r in rows if "2" in r]
        lo2, hi2 = min(a2), max(a2)
        leaders70 = board_leaders(rows)
        if not leaders70:
            winner_s = "No finite seventy-rate mean accuracy is available here."
        elif len(leaders70) == 1:
            best70 = leaders70[0]
            winner_s = f"{best70['name']} has the highest mean accuracy, at {100 * best70['70']['cv']:.1f} percent."
        else:
            best_mean = leaders70[0]["70"]["cv"]
            winner_s = f"{len(leaders70)} procedures tie for the highest mean accuracy, at {100 * best_mean:.1f} percent."
        tree70 = next(r for r in rows if r["key"] == "tree")["70"]["cv"]
        xgb70 = next(r for r in rows if r["key"] == "xgb")["70"]["cv"]
        lr70 = next(r for r in rows if r["key"] == "lr")["70"]["cv"]
        if not (math.isfinite(lr70) and math.isfinite(xgb70)):
            line_s = "A finite paired logistic-versus-boosting comparison is unavailable here."
        elif lr70 > xgb70:
            line_s = ("Logistic regression scores higher than boosted trees in these folds. "
                      "On this fixed-corpus task, a sum of small word effects is a useful description.")
        elif lr70 == xgb70:
            line_s = "Logistic regression and boosted trees tie on mean accuracy in these folds."
        else:
            line_s = "Boosted trees score higher than logistic regression in these folds."
        with self.voiceover(
            "Here's the contest: twelve named procedures on the same ten folds of these same-five-novel pages, "
            "with a fixed full-corpus dictionary and settings fixed in "
            f"advance. <bookmark mark='a'/> With two rates, every method lands between {100 * lo2:.0f} and "
            f"{100 * hi2:.0f} percent for these tested procedures on these folds. <bookmark mark='b'/> With all seventy, "
            f"{winner_s} A single tree manages "
            f"{100 * tree70:.0f}. {line_s} "
            "<bookmark mark='c'/> The lesson of classical machine learning: the description of the data mattered "
            "more than the cleverness of the method. Choosing seventy small words did most of the work."
        ) as vo:
            self.play(FadeIn(title), FadeIn(head), FadeIn(scale))
            self.play(LaggedStart(*[FadeIn(g[0]) for g in lines], lag_ratio=0.08), run_time=1.5)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(g[1]) for g in lines], lag_ratio=0.1), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(g[2]) for g in lines], lag_ratio=0.1), run_time=2.0)
            vo.wait_until("c")
            if leaders70:
                self.play(*[Indicate(lines[rows.index(r)][2], color=WHITE, scale_factor=1.05)
                            for r in leaders70], run_time=1.0)
            else:
                self.wait(1.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cultures(self):
        card = history_card(2001, r"Leo Breiman, \ \textit{Statistical Modeling: The Two Cultures}",
                            r"data modeling: \ assume how the data was made, \ then estimate it \ (his estimate: $98\%$ of "
                            r"statisticians). \ Algorithmic modeling: \ treat nature as a black box, \ judge by predictions "
                            r"on new data \ ($2\%$).", color=HIST, width=10.5, font_size=26).to_edge(UP, buff=0.35)
        events = [(2006, r"Netflix Prize: \\ \$1M for $10\%$"), (2009, r"won by a blend \\ of hundreds of models"),
                  (2010, r"Kaggle"), (2015, r"XGBoost: \ $17$ of $29$ \\ Kaggle winners")]
        axis, skel, marks = era_strip(events, y0=-2.1, width=4.6, font_size=20)
        cite_ = note(r"Chen \& Guestrin (2016): \ solutions on Kaggle's blog in 2015")
        with self.voiceover(
            "In 2001 Leo Breiman, who had left statistics for consulting and come back, described two cultures. "
            "Most statisticians assumed a model of how the data was made, and estimated it. A few, mostly outside "
            "statistics, treated nature as a black box, and judged a method only by how well it predicted new data. "
            "This part has belonged to the second culture. <bookmark mark='a'/> Competitions made it the norm. In "
            "2006 Netflix offered a million dollars for predicting ratings ten percent better; <bookmark mark='b'/> "
            "a blend of hundreds of models won in 2009. <bookmark mark='c'/> Kaggle turned the contest into a "
            "profession, <bookmark mark='d'/> and in 2015, seventeen of the twenty-nine winning solutions on Kaggle's "
            "blog used XGBoost."
        ) as vo:
            cite_.next_to(card, DOWN, buff=0.2)
            self.play(FadeIn(card, shift=DOWN * 0.2), Create(axis), FadeIn(skel))
            vo.wait_until("a")
            self.play(FadeIn(marks[0]))
            vo.wait_until("b")
            self.play(FadeIn(marks[1]))
            vo.wait_until("c")
            self.play(FadeIn(marks[2]))
            vo.wait_until("d")
            self.play(FadeIn(marks[3]), FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tables(self):
        why_ = VGroup(label(r"Why trees still win on tables", font_size=30, color=HL),
                      label(r"$45$ data sets of about $10{,}000$ rows: \ tree ensembles ahead of deep networks", font_size=22,
                            color=WHITE),
                      label(r"$\cdot$ \ uninformative columns: \ trees ignore them", font_size=22, color=GREY_A),
                      label(r"$\cdot$ \ columns mean something: \ trees don't mix them (no rotation)", font_size=22, color=GREY_A),
                      label(r"$\cdot$ \ irregular targets: \ steps, \ not smooth surfaces", font_size=22, color=GREY_A),
                      note(r"Grinsztajn, Oyallon \& Varoquaux (NeurIPS 2022)"))
        why_.arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_corner(UL, buff=0.35)
        # schematic: a table read in context, one forward pass
        cells = VGroup()
        g_ = np.random.default_rng(3)
        for r in range(7):
            for c in range(5):
                last = c == 4
                q = r >= 5
                col = (AUTH[g_.integers(2)] if last and not q else GREY_D)
                sq = Square(0.26, stroke_width=1, stroke_color=GREY_B, fill_color=col,
                            fill_opacity=0.8 if last and not q else 0.35)
                sq.move_to([c * 0.28, -r * 0.28, 0])
                cells.add(sq)
                if last and q:
                    cells.add(MathTex("?", font_size=20, color=WHITE).move_to(sq))
        cells.move_to([2.6, 1.6, 0])
        tf = RoundedRectangle(width=1.9, height=1.1, corner_radius=0.15, stroke_color=GOOD, stroke_width=2,
                              fill_color="#121722", fill_opacity=1).move_to([4.75, 1.6, 0])
        tfl = label(r"transformer \\ (synthetic tables)", font_size=18, color=GOOD).move_to(tf)
        outs = VGroup(*[Square(0.26, stroke_width=1, stroke_color=GREY_B, fill_color=AUTH[k], fill_opacity=0.8)
                        for k in (1, 0)]).arrange(DOWN, buff=0.02).move_to([6.3, 1.6, 0])
        a1 = Arrow(cells.get_right(), tf.get_left(), buff=0.1, stroke_width=3, color=GREY_B, max_tip_length_to_length_ratio=0.25)
        a2 = Arrow(tf.get_right(), outs.get_left(), buff=0.1, stroke_width=3, color=GREY_B, max_tip_length_to_length_ratio=0.3)
        sch = VGroup(cells, a1, tf, tfl, a2, outs)
        sch_t = note(r"schematic: \ training rows in, \ answers out, \ no training").next_to(sch, DOWN, buff=0.15)
        # schematic: an irregular target, a tree's steps and a network's smooth fit
        pa = Axes(x_range=[0, 10, 1], y_range=[0, 3, 1], x_length=4.2, y_length=1.9, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([4.0, 1.7, 0])
        steps_x = [0, 2.1, 2.1, 4.4, 4.4, 6.0, 6.0, 8.3, 8.3, 10]
        steps_y = [0.6, 0.6, 2.4, 2.4, 1.1, 1.1, 2.7, 2.7, 0.9, 0.9]
        tgt = VMobject(color=C.BITS, stroke_width=4).set_points_as_corners([pa.c2p(a, b) for a, b in zip(steps_x, steps_y)])
        smooth = pa.plot(lambda t: 1.6 + 0.75 * math.sin(0.62 * t - 1.4), x_range=[0, 10], color=C.MODEL_Q, stroke_width=3)
        pic = VGroup(pa, tgt, smooth,
                     label(r"trees: \ steps", font_size=20, color=C.BITS).next_to(pa, DOWN, buff=0.1).shift(LEFT * 1.0),
                     label(r"networks: \ smooth", font_size=20, color=C.MODEL_Q).next_to(pa, DOWN, buff=0.1).shift(RIGHT * 1.0))
        pic_t = note(r"schematic").next_to(pic, UP, buff=0.1)
        fm = VGroup(label(r"The frontier: \ foundation models for tables", font_size=30, color=GOOD),
                    label(r"a transformer pretrained on millions of \emph{synthetic} tables \\ reads the training rows "
                          r"and predicts in one forward pass", font_size=22, color=WHITE),
                    label(r"TabPFN (\textit{Nature}, Jan 2025): \ up to $10{,}000$ rows; \ $2.8$ s \\ "
                          r"reported classification benchmark; \ ensemble tuned for $4$ hours", font_size=22, color=GREY_A),
                    label(r"TabPFN-2.5 (Nov 2025): \ $50{,}000$ rows, \ $2{,}000$ columns", font_size=22, color=GREY_A),
                    label(r"TabPFN-3 (May 2026): \ $10^6$ rows at $200$ features; \\ first on TabArena \ (its authors' report)",
                          font_size=22, color=GREY_A),
                    label(r"Beyond IID (June 2026): \ TabPFN-2.6, not 3; \ includes model authors \\ "
                          r"boundary cases: \ tree and deep baselines", font_size=22, color=BAD))
        fm.arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(DOWN, buff=0.35).to_edge(LEFT, buff=0.35)
        with self.voiceover(
            "Deep learning took over images, sound and language. Why not tables? In 2022, Grinsztajn, Oyallon and "
            "Varoquaux tested forty-five tabular data sets of around ten thousand rows, and tree ensembles still "
            "beat deep networks. <bookmark mark='a'/> Their reasons: tables carry useless columns, which trees "
            "simply never ask about; each column means something, and networks blur them together; and the answers "
            "jump in steps, which trees draw easily. <bookmark mark='b'/> The challenger is a transformer trained "
            "only on millions of synthetic tables, which reads your training rows as its prompt and predicts in one "
            "pass. TabPFN's second version, in Nature in January 2025, beat a four-hour tuned ensemble in under three "
            "seconds in its reported classification benchmark configuration, on tables of up to ten thousand rows. "
            "<bookmark mark='c'/> Its successors reach fifty thousand rows, then, in May 2026, a million rows at "
            "two hundred features, top of the TabArena leaderboard by their makers' report. "
            "<bookmark mark='d'/> A broader June 2026 benchmark included model authors among its coauthors and "
            "tested TabPFN two point six, not TabPFN three. Foundation models were strong on small and medium "
            "IID tables; traditional tree and deep models exposed boundary cases on non-IID, large or very wide "
            "data. These are version- and task-specific comparisons, with both tree and deep models necessary "
            "baselines."
        ) as vo:
            self.play(FadeIn(why_[0]), FadeIn(why_[1]), FadeIn(why_[5]), FadeIn(pic), FadeIn(pic_t))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in why_[2:5]], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeOut(pic), FadeOut(pic_t))
            self.play(FadeIn(sch), FadeIn(sch_t), FadeIn(fm[0]), FadeIn(fm[1]), FadeIn(fm[2]))
            vo.wait_until("c")
            self.play(FadeIn(fm[3]), FadeIn(fm[4]))
            vo.wait_until("d")
            self.play(FadeIn(fm[5]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def today(self):
        rows = [
            (r"logistic regression", r"the softmax at the top of every language model", r"Parts 9, 13"),
            (r"least squares, \ ridge", r"linear probes that read concepts out of networks; \ weight decay", r"Parts 11, 30"),
            (r"the lasso's $|w|$ penalty", r"sparse autoencoders, \ which pull features out of a model", r"Part 30"),
            (r"kernels", r"the neural tangent kernel; \ attention as a kernel smoother", r"Parts 8, 13"),
            (r"the widest margin", r"where gradient descent drifts on separable data", r"Part 8"),
            (r"nearest neighbours", r"retrieval, \ and language models that look things up", r"Part 15"),
            (r"boosted trees", r"tables and search ranking, \ still", r"this chapter"),
            (r"calibration", r"do a language model's probabilities mean anything?", r"Part 31"),
        ]
        head = label(r"How the classics live on", font_size=38).to_edge(UP, buff=0.3)
        lines = VGroup()
        for a, b, c_ in rows:
            la = label(a, font_size=27, color=HL)
            lb = label(b, font_size=25, color=WHITE)
            lc = label(c_, font_size=22, color=GREY_B)
            lines.add(VGroup(la, lb, lc))
        for k, ln in enumerate(lines):
            y = 2.45 - 0.73 * k
            ln[0].move_to([-3.4, y, 0], aligned_edge=RIGHT)
            ln[1].move_to([-3.1, y, 0], aligned_edge=LEFT)
            ln[2].move_to([6.7, y, 0], aligned_edge=RIGHT)
            if ln[1].get_right()[0] > ln[2].get_left()[0] - 0.2:
                ln[1].scale_to_fit_width(ln[2].get_left()[0] - 0.2 - ln[1].get_left()[0]).align_to([-3.1, 0, 0], LEFT)
        arrows = VGroup(*[MathTex(r"\rightarrow", font_size=26, color=GREY_C).move_to([-3.25, ln.get_y(), 0]) for ln in lines])
        for a_, ln in zip(arrows, lines):
            ln[0].shift(LEFT * 0.12)
        with self.voiceover(
            "None of this went away; it moved inside the big models. <bookmark mark='a'/> The last layer of every "
            "language model is a logistic regression over its vocabulary. Linear probes, fitted by least squares, "
            "read concepts out of a network, and ridge's penalty is weight decay. <bookmark mark='b'/> The lasso's "
            "absolute-value penalty is how sparse autoencoders pull features out of a model. Kernels describe very "
            "wide networks, and attention is a kernel smoother. <bookmark mark='c'/> Nearest neighbours became "
            "retrieval. And boosted trees still run the world's tables and search rankings, while the question "
            "naive Bayes raised, whether a model's probabilities mean anything, is asked of every chatbot."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(lines[k], arrows[k])) for k in range(2)], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(lines[k], arrows[k])) for k in range(2, 5)], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(VGroup(lines[k], arrows[k])) for k in range(5, 8)], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()
