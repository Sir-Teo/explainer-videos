from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs47.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, bar_chart, load, trace


class Ranking(VoiceoverScene):
    def construct(self):
        self.card()
        self.tfidf()
        self.cosine()
        self.prp()
        self.bim()
        self.saturation()
        self.length()

    def card(self):
        card = chapter_card(5, r"From tf-idf to BM25", r"Which passage should come first?",
                            lit=(1972, 1977, 1994), extra=((1972, r"Sp\"arck Jones: \ idf"),
                                                           (1977, r"the probability ranking principle"),
                                                           (1994, r"Okapi BM25 at TREC-3")), part=PART)
        with self.voiceover("Chapter five. From tf-idf to BM25."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def tfidf(self):
        ix = load("index")
        N = ix["docs"]
        terms = sorted(ix["df"], key=lambda t: -ix["df"][t])
        idfs = [math.log(N / ix["df"][t]) for t in terms]
        head = label(r"Term frequency, \ inverse document frequency", font_size=36).to_edge(UP, buff=0.3)
        chart = bar_chart(idfs, [rf"\texttt{{{t}}}" for t in terms], [DATA, DATA, LAM, LAM], height=3.0, bar_w=0.9,
                          gap=0.55, vmax=5.0, fmt_=lambda v: f"{v:.2f}", font_size=20)
        dfs = VGroup(*[label(rf"df {ix['df'][t]}", font_size=17, color=GREY_B).next_to(n, DOWN, buff=0.12)
                       for t, n in zip(terms, chart.names)])
        ttl = label(rf"$\ln(N/\mathrm{{df}})$ \ on our {N:,} passages \ (stems)", font_size=19, color=GREY_A)
        left = VGroup(ttl, VGroup(chart, dfs)).arrange(DOWN, buff=0.35).next_to(head, DOWN, buff=0.6)
        left.to_edge(LEFT, buff=0.6)
        W = 6.0
        right = VGroup(
            MathTex(r"w_{t,d} = (1 + \ln \mathrm{tf}_{t,d}) \cdot \ln \frac{N}{\mathrm{df}_t}", font_size=36,
                    color=WHITE),
            wrapped_label(r"term frequency, \ damped by a logarithm: \ the tenth \textit{whale} in a passage says "
                          r"less than the first", W, font_size=19, color=DATA),
            wrapped_label(r"inverse document frequency \ (Sp\"arck Jones, \ 1972): \ a rare word says more; \ a "
                          r"word in every passage scores $\ln 1 = 0$", W, font_size=19, color=LAM),
            MathTex(r"\mathrm{score}(q, d) = \sum_{t \in q} w_{t,d}", font_size=34, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        right.next_to(head, DOWN, buff=0.8).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "Boolean retrieval answers yes or no, but a reader wants the best passage first. <bookmark mark='a'/> A "
            "word that recurs in a passage says more about it, so weight it by its term frequency, damped by a "
            "logarithm: the tenth whale adds less than the first. <bookmark mark='b'/> And a rare word says more than "
            "a common one: Karen Spärck Jones, in 1972, weighted each term by the log of N over its document "
            "frequency. <bookmark mark='c'/> Whale, in three hundred and ninety of our passages, gets three point "
            "three six; Darcy, in a hundred and seventy-one, four point one nine."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(right[0]), FadeIn(right[1]))
            vo.wait_until("b")
            self.play(FadeIn(right[2]))
            vo.wait_until("c")
            self.play(FadeIn(ttl), Create(chart[0]), *[GrowFromEdge(b, DOWN) for b in chart.bars],
                      FadeIn(chart.vals), FadeIn(chart.names), FadeIn(dfs), run_time=1.5)
            self.play(FadeIn(right[3]))
        self.wait(0.4)
        self.clear_scene()

    def cosine(self):
        head = label(r"Passages as vectors", font_size=36).to_edge(UP, buff=0.3)
        ax = axes([0, 4, 1], [0, 4, 1], x_length=4.4, y_length=4.4, x_label=r"weight of \texttt{whale}",
                  y_label=r"weight of \texttt{white}")
        ax.next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.9)
        a = ax.ax
        o = a.c2p(0, 0)
        vecs = {"q": ((1.2, 1.2), HEAD, r"query"), "d1": ((3.0, 2.4), YES, r"passage A"),
                "d2": ((3.6, 0.5), DATA, r"passage B")}
        arrows, names = VGroup(), VGroup()
        for key, ((x, y), col, nm) in vecs.items():
            ar = Arrow(o, a.c2p(x, y), buff=0, stroke_width=4, color=col, max_tip_length_to_length_ratio=0.12)
            arrows.add(ar)
            names.add(label(nm, font_size=18, color=col).next_to(a.c2p(x, y), {"q": UL, "d1": UR}.get(key, RIGHT),
                                                                 buff=0.08))

        def ang(v):
            return math.atan2(v[1], v[0])

        def cos(u, v):
            return (u[0] * v[0] + u[1] * v[1]) / (math.hypot(*u) * math.hypot(*v))
        q, d1, d2 = (vecs[k][0] for k in ("q", "d1", "d2"))
        arcs = VGroup(Arc(radius=1.1, start_angle=ang(d1), angle=ang(q) - ang(d1), arc_center=o, color=YES),
                      Arc(radius=1.6, start_angle=ang(d2), angle=ang(q) - ang(d2), arc_center=o, color=DATA))
        ill = note(r"illustrative", font_size=17).next_to(ax, DOWN, buff=0.1).align_to(ax, RIGHT)
        W = 6.2
        right = VGroup(
            MathTex(r"\cos\theta = \frac{\vec q \cdot \vec d}{|\vec q|\,|\vec d|}", font_size=40, color=WHITE),
            wrapped_label(r"Salton's SMART system: \ one dimension per term, \ tf-idf weights as coordinates; \ the "
                          r"query is a vector too", W, font_size=19, color=GREY_A),
            wrapped_label(rf"rank by the angle: \ A {cos(q, d1):.2f}, \ B {cos(q, d2):.2f}", W, font_size=20,
                          color=YES),
            wrapped_label(r"dividing by $|\vec d|$ stops a long passage winning by being long; \ our tf-idf divides "
                          r"by $\sqrt{\text{length}}$, \ a cheap stand-in", W, font_size=19, color=HEAD),
            wrapped_label(r"but why these weights? \ Nothing so far says", W, font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        right.next_to(head, DOWN, buff=0.6).to_edge(RIGHT, buff=0.45)
        with self.voiceover(
            "Gerard Salton's SMART system made this geometry. <bookmark mark='a'/> A passage is a vector, one "
            "dimension per term, with these weights as coordinates; the query is a vector too. <bookmark mark='b'/> "
            "Rank passages by the cosine of the angle to the query: the dot product over both lengths. <bookmark "
            "mark='c'/> Dividing by length stops a long passage winning just by being long; our tf-idf divides by the "
            "square root of the length, a cheap stand-in. <bookmark mark='d'/> But why these weights? Nothing so far "
            "says."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(ill))
            vo.wait_until("a")
            self.play(GrowArrow(arrows[1]), GrowArrow(arrows[2]), FadeIn(names[1:]), FadeIn(right[1]))
            self.play(GrowArrow(arrows[0]), FadeIn(names[0]))
            vo.wait_until("b")
            self.play(Write(right[0]), Create(arcs))
            self.play(FadeIn(right[2]))
            vo.wait_until("c")
            self.play(FadeIn(right[3]))
            vo.wait_until("d")
            self.play(FadeIn(right[4]))
        self.wait(0.4)
        self.clear_scene()

    def prp(self):
        head = label(r"The probability ranking principle", font_size=36).to_edge(UP, buff=0.3)
        probs = [0.9, 0.8, 0.6, 0.5, 0.3, 0.2, 0.1, 0.05]
        k = 3
        rows = VGroup()
        for i, p in enumerate(probs):
            name = label(rf"passage {chr(65 + i)}", font_size=18, color=GREY_A)
            bar = Rectangle(width=4.0 * p, height=0.3, stroke_width=0, fill_color=DATA, fill_opacity=0.85)
            val = label(f"{p:.2f}", font_size=17, color=DATA)
            rows.add(VGroup(name, bar, val))
        y0, dy, x0 = 2.1, 0.52, -6.5
        for i, r in enumerate(rows):
            r[0].move_to([x0, y0 - i * dy, 0], aligned_edge=LEFT)
            r[1].move_to([x0 + 1.6, y0 - i * dy, 0], aligned_edge=LEFT)
            r[2].next_to(r[1], RIGHT, buff=0.12)
        cut_y = y0 - (k - 0.5) * dy
        cut = DashedLine([x0, cut_y, 0], [-1.2, cut_y, 0], color=HEAD, stroke_width=2)
        cut_l = label(rf"top {k}", font_size=17, color=HEAD).next_to(cut, RIGHT, buff=0.1)

        def exp_label(ps, col):
            return label(rf"expected relevant in the top {k}: \ {sum(ps[:k]):.1f}", font_size=20,
                         color=col).move_to([-3.9, y0 - len(probs) * dy - 0.25, 0])
        e1 = exp_label(probs, YES)
        swapped = probs[:]
        swapped[2], swapped[4] = swapped[4], swapped[2]
        e2 = exp_label(swapped, NO)
        ill = note(r"illustrative probabilities", font_size=17).next_to(e1, DOWN, buff=0.2)
        W = 6.0
        right = VGroup(
            wrapped_label(r"\textbf{Robertson \ (1977)}: \ rank documents by $P(\text{relevant} \mid d, q)$", W,
                          font_size=21, color=WHITE),
            wrapped_label(r"if each probability is estimated correctly and documents are relevant independently, "
                          r"\ no other order puts more relevant documents, \ in expectation, \ into the top $k$, \ "
                          r"for every $k$", W, font_size=19, color=YES),
            wrapped_label(r"proof: \ an exchange; \ swap a likelier document below the cut with a less likely one "
                          r"above it, \ and the expected count above the cut falls", W, font_size=19, color=HEAD),
            wrapped_label(r"what is left: \ estimate that probability from words", W, font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        right.next_to(head, DOWN, buff=0.6).to_edge(RIGHT, buff=0.45)
        with self.voiceover(
            "In 1977 Stephen Robertson stated the principle that answers it. <bookmark mark='a'/> Rank documents by "
            "their probability of being relevant. <bookmark mark='b'/> If those probabilities are right, and "
            "documents are relevant independently, no other order puts more relevant documents, in expectation, into "
            "the top k, for any k. <bookmark mark='c'/> The proof is an exchange: swap a likelier document below the "
            "cut with a less likely one above it, and the expected count falls. <bookmark mark='d'/> So ranking "
            "reduces to estimating one probability from words."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.1), FadeIn(ill),
                      run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(right[0]), Create(cut), FadeIn(cut_l))
            vo.wait_until("b")
            self.play(FadeIn(right[1]), FadeIn(e1))
            vo.wait_until("c")
            self.play(FadeIn(right[2]))
            ya, yb = rows[2].get_y(), rows[4].get_y()
            self.play(rows[2].animate.set_y(yb), rows[4].animate.set_y(ya), Transform(e1, e2), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(right[3]))
        self.wait(0.4)
        self.clear_scene()

    def bim(self):
        head = label(r"The binary independence model", font_size=36).to_edge(UP, buff=0.3)
        maths = [
            r"P(R \mid d) \;\stackrel{\text{rank}}{=}\; \frac{P(R \mid d)}{P(\bar R \mid d)}",
            r"\stackrel{\text{rank}}{=}\; \frac{P(d \mid R)}{P(d \mid \bar R)}",
            r"=\; \prod_t \frac{P(x_t \mid R)}{P(x_t \mid \bar R)}",
            r"\log O \;\stackrel{\text{rank}}{=}\; \sum_{t \in q \cap d} \log \frac{p_t\,(1-u_t)}{u_t\,(1-p_t)}",
            r"w_t = \log \frac{N - \mathrm{df}_t + 0.5}{\mathrm{df}_t + 0.5}",
        ]
        whys = [
            r"odds rise with probability: \ the same order",
            r"Bayes' rule; \ the prior odds $P(R)/P(\bar R)$ are the same for every passage",
            r"a passage as present or absent terms $x_t$, \ independent given relevance",
            r"$p_t$, \ $u_t$: \ the chance $t$ occurs in a relevant, \ an irrelevant passage; \ assume $p_t = u_t$ "
            r"off the query, \ and those terms cancel",
            r"no relevance information: \ $p_t = \tfrac12$; \ almost every passage is irrelevant: \ "
            r"$u_t \approx \mathrm{df}_t/N$. \ Robertson \& Sp\"arck Jones \ (1976)",
        ]
        cols = [WHITE, WHITE, WHITE, DATA, YES]
        rows = VGroup()
        for m, w, c in zip(maths, whys, cols):
            mt = MathTex(m, font_size=30, color=c)
            if mt.width > 6.8:
                mt.width = 6.8
            rows.add(VGroup(mt, wrapped_label(w, 6.4, font_size=19, color=GREY_B)))
        y = 2.45
        for r in rows:
            h = max(r[0].height, r[1].height)
            r[0].move_to([-6.2, y - h / 2, 0], aligned_edge=LEFT)
            r[1].move_to([0.1, y - h / 2, 0], aligned_edge=LEFT)
            y -= h + 0.32
        box = SurroundingRectangle(rows[4][0], color=YES, buff=0.12, corner_radius=0.08)
        foot = wrapped_label(r"idf, \ derived rather than guessed; \ our engine uses "
                             r"$\log\big(1 + \frac{N - \mathrm{df} + 0.5}{\mathrm{df} + 0.5}\big)$, \ Lucene's "
                             r"form, \ which never goes below zero", 12.4, font_size=20, color=HEAD)
        foot.to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The binary independence model is the simplest estimate. <bookmark mark='a'/> Ranking by probability is "
            "ranking by odds. <bookmark mark='b'/> Bayes' rule turns the odds around, and the prior odds are the same "
            "for every passage, so they drop out. <bookmark mark='c'/> Treat a passage as present or absent terms, "
            "independent given relevance. <bookmark mark='d'/> The log odds become a sum over the query terms the "
            "passage contains, each weighted by how much likelier it is in relevant passages. <bookmark mark='e'/> "
            "Knowing nothing about relevance, set p to one half; since almost every passage is irrelevant, set u to "
            "the document frequency over N. Out comes idf, derived rather than guessed: Robertson and Spärck Jones, "
            "1976."
        ) as vo:
            self.play(FadeIn(head))
            for i, mk in enumerate("abcde"):
                vo.wait_until(mk)
                self.play(Write(rows[i][0]), FadeIn(rows[i][1]))
            self.play(Create(box), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def saturation(self):
        s = load("bm25")["saturation"]
        head = label(r"Saturation: \ $k_1$", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, 20, 5], [0, 6, 1], x_length=6.0, y_length=4.2, x_label=r"term frequency in the passage",
                 y_label=r"BM25's tf factor", xticks=[0, 5, 10, 15, 20], yticks=[0, 1, 2, 3, 4, 5, 6])
        g.next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.8)
        a = g.ax
        colors = [GREY_B, YES, DATA, LAM]
        curves, tags, asym = VGroup(), VGroup(), VGroup()
        for (k1, pts), col in zip(sorted(s.items(), key=lambda kv: float(kv[0])), colors):
            curves.add(trace(a, pts, col, width=3))
            tags.add(label(rf"$k_1 = {float(k1):g}$", font_size=17, color=col).next_to(a.c2p(*pts[-1]), RIGHT,
                                                                                       buff=0.1))
            top = float(k1) + 1
            if top <= 6:
                asym.add(DashedLine(a.c2p(0, top), a.c2p(20, top), color=col, stroke_width=1.2, dash_length=0.08))
        W = 5.4
        right = VGroup(
            wrapped_label(r"the binary model counts a word once, \ however often it occurs", W, font_size=19,
                          color=WHITE),
            wrapped_label(r"Harter's \textbf{two-Poisson} model \ (1975): \ a passage is about the term or not, \ with "
                          r"the count Poisson in each; \ the weight it implies rises with tf and levels off", W,
                          font_size=19, color=GREY_A),
            MathTex(r"\frac{\mathrm{tf}\,(k_1 + 1)}{\mathrm{tf} + k_1}", font_size=40, color=YES),
            wrapped_label(r"Robertson \& Walker \ (1994): \ 1 at $\mathrm{tf} = 1$, \ rising towards $k_1 + 1$ \ "
                          r"(dashed)", W, font_size=19, color=YES),
            wrapped_label(r"$k_1 \to 0$: \ the binary model again; \ $k_1 \to \infty$: \ raw counts", W, font_size=19,
                          color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        right.next_to(head, DOWN, buff=0.5).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "But that model counts a word once, however often it appears, and a passage that says whale twenty times "
            "is likelier to be about whales. <bookmark mark='a'/> Stephen Harter's two-Poisson model of 1975 says a "
            "passage either is about the term or is not, with the count Poisson in each case; the weight it implies "
            "grows with the count and levels off. <bookmark mark='b'/> Robertson and Walker, in 1994, approximated it "
            "with one curve: term frequency times k one plus one, over term frequency plus k one. It is one at a "
            "single occurrence and rises towards k one plus one. <bookmark mark='c'/> With k one near zero, it is the "
            "binary model again; as k one grows, raw counts."
        ) as vo:
            self.play(FadeIn(head), Create(g), FadeIn(right[0]))
            vo.wait_until("a")
            self.play(FadeIn(right[1]))
            vo.wait_until("b")
            self.play(Write(right[2]), FadeIn(right[3]))
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.3), FadeIn(tags), Create(asym),
                      run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(right[4]))
        self.wait(0.4)
        self.clear_scene()

    def length(self):
        head = label(r"Length normalization: \ $b$, \ and BM25", font_size=36).to_edge(UP, buff=0.3)
        k1, b = 1.2, 0.75
        parts = VGroup(
            MathTex(r"\mathrm{BM25}(q, d) = \sum_{t \in q}", font_size=34, color=WHITE),
            MathTex(r"\log\Big(1 + \frac{N - \mathrm{df}_t + 0.5}{\mathrm{df}_t + 0.5}\Big)", font_size=34,
                    color=LAM),
            MathTex(r"\cdot", font_size=34, color=WHITE),
            MathTex(r"\frac{\mathrm{tf}_{t,d}\,(k_1 + 1)}{\mathrm{tf}_{t,d} + K}", font_size=34, color=YES),
        ).arrange(RIGHT, buff=0.15)
        kdef = MathTex(r"K = k_1\Big(1 - b + b\,\frac{|d|}{\mathrm{avgdl}}\Big)", font_size=34, color=HEAD)
        formula = VGroup(parts, kdef).arrange(RIGHT, buff=0.6)
        if formula.width > 13.4:
            formula.width = 13.4
        formula.next_to(head, DOWN, buff=0.4)
        braces = VGroup(BraceLabel(parts[1], r"\text{idf: binary model}", DOWN, font_size=22, color=LAM),
                        BraceLabel(parts[3], r"\text{saturation}", DOWN, font_size=22, color=YES),
                        BraceLabel(kdef, r"\text{length}", DOWN, font_size=22, color=HEAD))
        g = axes([0, 12, 2], [0, 2.4, 0.5], x_length=5.4, y_length=2.9, x_label=r"term frequency",
                 y_label=r"tf factor, \ $k_1 = 1.2$, \ $b = 0.75$", xticks=[0, 4, 8, 12], yticks=[0, 1, 2])
        g.to_edge(LEFT, buff=0.8).to_edge(DOWN, buff=0.45)
        a = g.ax
        curves, tags = VGroup(), VGroup()
        for r, col, nm in ((0.5, YES, r"half the average"), (1.0, DATA, r"average length"),
                           (2.0, NO, r"twice the average")):
            K = k1 * (1 - b + b * r)
            pts = [(t / 4, (t / 4) * (k1 + 1) / (t / 4 + K)) for t in range(0, 49)]
            curves.add(trace(a, pts, col, width=3))
            tags.add(VGroup(Line(ORIGIN, RIGHT * 0.4, color=col, stroke_width=3),
                            label(nm, font_size=17, color=col)).arrange(RIGHT, buff=0.12))
        tags.arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(a.c2p(12, 0.1), UL, buff=0.1)
        W = 5.6
        notes = VGroup(
            wrapped_label(r"a long passage repeats words because it is long, \ not because it is more about them", W,
                          font_size=19, color=WHITE),
            wrapped_label(r"$b = 0$: \ no normalization; \ $b = 1$: \ $k_1$ scaled by the full relative length", W,
                          font_size=19, color=HEAD),
            wrapped_label(r"Lucene's defaults: \ $k_1 = 1.2$, \ $b = 0.75$; \ tune both on judged queries", W,
                          font_size=19, color=GREY_A),
            wrapped_label(r"our passages are cut to the same 400 words, \ so here $b$ has little to do", W,
                          font_size=19, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        notes.to_edge(RIGHT, buff=0.4).align_to(g, DOWN)
        with self.voiceover(
            "One more correction. <bookmark mark='a'/> A long passage repeats words because it is long, not because "
            "it is more about them. So BM25 scales k one by one minus b, plus b times the passage's length over the "
            "average. <bookmark mark='b'/> A passage twice the average needs more occurrences for the same weight; "
            "with b zero there is no normalization, with b one, full. <bookmark mark='c'/> Put together: idf from the "
            "binary model, saturation from two Poissons, and length. That is BM25, first run at TREC in 1994, and "
            "Lucene's default, with k one of one point two and b of three quarters."
        ) as vo:
            self.play(FadeIn(head), FadeIn(parts), FadeIn(kdef))
            vo.wait_until("a")
            self.play(FadeIn(braces[2]), FadeIn(notes[0]), Create(g))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.3), FadeIn(tags), FadeIn(notes[1]),
                      run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(braces[0]), FadeIn(braces[1]))
            self.play(FadeIn(notes[2]), FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, KERN)
