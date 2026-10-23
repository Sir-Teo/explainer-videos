from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai24.common import (EST, LOGN, MI, NEG, PART, POS, SIMCLR, arrow, axes, curve, load, node_box,
                                   take_away)

COLS = {r"x": SIMCLR, r"y_1": POS, r"y_j": NEG, r"K": C.BITS}


class InfoNCE(VoiceoverScene):
    def construct(self):
        self.card()
        self.nce()
        self.word2vec()
        self.infonce()
        self.derive()
        self.check()
        self.cpc()

    def card(self):
        card = chapter_card(3, r"Telling the real from the fake", r"What does a contrastive loss actually measure?",
                            lit=(2013,), part=PART)
        with self.voiceover("Chapter three. Telling the real from the fake."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def nce(self):
        rng = np.random.default_rng(4)
        ang = rng.uniform(0, 2 * np.pi, 160)
        data = np.c_[1.4 * np.cos(ang), 0.9 * np.sin(ang)] + rng.normal(0, 0.12, (160, 2))
        noise = rng.uniform(-2.2, 2.2, (160, 2))
        c0 = np.array([-3.6, -0.3])
        dd = VGroup(*[Dot([c0[0] + 1.0 * p[0], c0[1] + 1.0 * p[1], 0], radius=0.04, color=C.TRUE_P) for p in data])
        nn = VGroup(*[Dot([c0[0] + 1.0 * p[0], c0[1] + 1.0 * p[1], 0], radius=0.04, color=GREY_C) for p in noise])
        box = Square(4.6, color=GREY_D, stroke_width=1.2).move_to([c0[0], c0[1], 0])
        ld = label(r"data", font_size=22, color=C.TRUE_P).next_to(box, UP, buff=0.12).shift(LEFT * 1.2)
        ln = label(r"noise you chose", font_size=22, color=GREY_B).next_to(box, UP, buff=0.12).shift(RIGHT * 0.9)
        f1 = MathTex(r"P(\text{data} \mid x) = \sigma\big(\log p_\theta(x) - \log k\,q(x)\big)", font_size=32)
        f1.move_to([2.9, 1.3, 0])
        f1[0][2:6].set_color(C.TRUE_P)
        n1 = label(r"a logistic classifier: \ data or noise?", font_size=24, color=GREY_A).next_to(f1, UP, buff=0.3)
        n2 = label(r"its best answer \ is the density ratio, \\ so it learns $p_\theta$ without ever computing \\ "
                   r"the normalizing sum", font_size=24, color=GREY_A).next_to(f1, DOWN, buff=0.45)
        src = cite(r"Gutmann \& Hyv\"arinen (2010)")
        with self.voiceover(
            "Contrastive learning starts from a statistics trick of 2010. You want a model of your data, but its "
            "probabilities need a normalizing sum over every possible input, which you cannot compute. <bookmark "
            "mark='a'/> So add noise you chose yourself, and train a classifier to tell data from noise. "
            "<bookmark mark='b'/> Michael Gutmann and Aapo Hyvärinen showed that the best such classifier has to "
            "know the ratio of the data's density to the noise's, so it learns the model without the sum. They "
            "called it noise-contrastive estimation."
        ) as vo:
            self.play(Create(box), FadeIn(dd), FadeIn(ld), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(nn), FadeIn(ln))
            self.play(FadeIn(n1), Write(f1))
            vo.wait_until("b")
            self.play(FadeIn(n2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def word2vec(self):
        centre = data_text("dog", font_size=34, color=SIMCLR)
        pos = data_text("barked", font_size=30, color=POS)
        negs = VGroup(*[data_text(w, font_size=26, color=NEG) for w in ("tariff", "of", "quietly", "violin", "the")])
        centre.move_to([-4.2, 0.4, 0])
        pos.move_to([-1.2, 1.6, 0])
        negs.arrange(DOWN, buff=0.22).move_to([-1.2, -1.1, 0])
        a_pos = arrow(centre.get_right(), pos.get_left(), color=POS)
        a_negs = VGroup(*[arrow(centre.get_right(), n.get_left(), color=NEG, stroke_width=1.8) for n in negs])
        f = MathTex(r"\log \sigma(u_{o}^{\top} v_c)", r"+", r"\sum_{i=1}^{k} \log \sigma(-u_{i}^{\top} v_c)",
                    font_size=36).move_to([3.4, 0.9, 0])
        f[0].set_color(POS)
        f[2].set_color(NEG)
        b1 = brace_note(f[0], r"a real neighbour: \ score up", direction=UP, color=POS, font_size=22)
        b2 = brace_note(f[2], r"$k$ random words: \ scores down", direction=DOWN, color=NEG, font_size=22)
        ex = label(r"noise: \ word frequencies$^{3/4}$; \ $k = 5$--$20$ on small corpora", font_size=22,
                   color=GREY_A).move_to([3.4, -1.9, 0])
        back = label(r"Part 3 trained this on the books", font_size=22, color=GREY_B).to_corner(DR, buff=0.3)
        src = cite(r"Mikolov, Sutskever, Chen, Corrado \& Dean (2013)")
        with self.voiceover(
            "Three years later, word2vec turned the trick into the most copied objective in the field. Take a word, "
            "dog, and a word that really appeared near it, barked. <bookmark mark='a'/> Push their vectors' score "
            "up. <bookmark mark='b'/> Then draw a handful of words at random, from the word frequencies raised to "
            "three quarters, and push their scores down. <bookmark mark='c'/> This is negative sampling, a "
            "simplified noise-contrastive estimate, and it is the version Part 3 trained on the books. A real pair "
            "against fake ones: every method in the next three chapters has this shape."
        ) as vo:
            self.play(FadeIn(centre), FadeIn(pos), GrowArrow(a_pos), FadeIn(src))
            vo.wait_until("a")
            self.play(Write(f[0]), FadeIn(b1))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(n)) for a, n in zip(a_negs, negs)],
                                  lag_ratio=0.2), Write(f[1:]), FadeIn(b2), run_time=2.0)
            self.play(FadeIn(ex))
            vo.wait_until("c")
            self.play(FadeIn(back))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def infonce(self):
        x = node_box(r"$x$", SIMCLR, font_size=34, height=0.8).move_to([-4.6, 0, 0])
        ys = VGroup(*[node_box(rf"$y_{{{j}}}$", POS if j == 1 else NEG, font_size=28, height=0.6) for j in range(1, 7)])
        ys.arrange(DOWN, buff=0.18).move_to([-1.6, 0, 0])
        dots = MathTex(r"\vdots", font_size=30, color=GREY_B).next_to(ys, DOWN, buff=0.1)
        arrs = VGroup(*[arrow(x.get_right(), y.get_left(), color=POS if j == 0 else GREY_C, stroke_width=2)
                        for j, y in enumerate(ys)])
        f = MathTex(r"\mathcal L_N", r"=", r"\mathbb E\Big[-\log", r"\frac{e^{f(x, y_1)}}{\sum_{j=1}^{N} e^{f(x, y_j)}}",
                    r"\Big]", font_size=40).move_to([3.4, 0.8, 0])
        f[3].set_color(POS)
        n1 = label(r"one partner $y_1 \sim p(y \mid x)$, \\ $N - 1$ others $y_j \sim p(y)$", font_size=24,
                   color=GREY_A).next_to(f, DOWN, buff=0.45)
        n2 = label(r"an $N$-way classification: \ \textbf{which one is the partner?}", font_size=24,
                   color=C.BITS).next_to(n1, DOWN, buff=0.35)
        src = cite(r"van den Oord, Li \& Vinyals (2018): \ InfoNCE")
        with self.voiceover(
            "In 2018 Aaron van den Oord, Yazhe Li and Oriol Vinyals wrote the modern form. Take an x, and N "
            "candidates. <bookmark mark='a'/> One of them, y one, really goes with x; the other N minus one were "
            "drawn at random. <bookmark mark='b'/> A scoring function f rates every pair, a softmax turns the scores "
            "into a guess, and the loss is the cross-entropy of guessing the partner. They called it InfoNCE, "
            "<bookmark mark='c'/> because it is noise-contrastive estimation turned into an N-way choice, and "
            "because of what it measures: information."
        ) as vo:
            self.play(FadeIn(x), FadeIn(ys), FadeIn(dots), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.1), Indicate(ys[0], color=POS))
            vo.wait_until("b")
            self.play(Write(f), FadeIn(n1))
            vo.wait_until("c")
            self.play(FadeIn(n2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        rows = [
            cmath(r"\mathcal L_N", r"=", r"\mathbb E\big[-\log q_f(K \mid x, y_{1:N})\big]", font_size=34),
            cmath(r"\mathcal L_N", r"\ge", r"H(K \mid X, Y_{1:N})", font_size=34),
            cmath(r"\mathcal L_N", r"\ge", r"\log N - I(K;\, X, Y_{1:N})", font_size=34),
            cmath(r"\mathcal L_N", r"\ge", r"\log N - I(K;\, X \mid Y_{1:N})", font_size=34),
            cmath(r"\mathcal L_N", r"\ge", r"\log N - I(X;\, K, Y_{1:N})", font_size=34),
            cmath(r"\mathcal L_N", r"\ge", r"\log N - I(X;\, Y)", font_size=34),
        ]
        whys = [why(r"$K$: \ the partner's slot, \ a classifier's guess"), why(r"cross-entropy $\ge$ entropy (Gibbs)"),
                why(r"$K$ is uniform on $N$ slots"), why(r"the candidates alone say nothing about $K$"),
                why(r"chain rule; \ information $\ge 0$"), why(r"given the partner, \ the rest is noise")]
        for r in rows:
            r[0].set_color(C.LOSS)
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-2.4, buff=0.5, edge=6.9)
        res = cmath(r"I(X;\,Y)", r"\ge", r"\log N - \mathcal L_N", r"\le", r"\log N", font_size=42)
        res[0].set_color(MI)
        res[2].set_color(EST)
        res[4].set_color(LOGN)
        box = SurroundingRectangle(res, color=C.BITS, buff=0.2, corner_radius=0.1)
        fin = VGroup(res, box).to_edge(DOWN, buff=0.6)
        caveat = label(r"the estimate can never exceed $\log N$, \ since $\mathcal L_N \ge 0$", font_size=24,
                       color=GREY_A).next_to(fin, UP, buff=0.25)
        with self.voiceover(
            "Why information? Call K the slot where the partner sits. The loss is the cross-entropy of a classifier "
            "guessing K. <bookmark mark='a'/> A cross-entropy is never smaller than the true entropy of what it "
            "guesses. <bookmark mark='b'/> K was uniform over N slots, so that entropy is log N, minus whatever x "
            "and the candidates reveal about K. <bookmark mark='c'/> The candidates by themselves reveal nothing: "
            "the partner, on its own, looks like any other draw. <bookmark mark='d'/> By the chain rule, what x "
            "reveals about K is at most what x shares with the whole set, <bookmark mark='e'/> and that is exactly "
            "what x shares with its partner, the mutual information. <bookmark mark='f'/> So log N minus the loss "
            "is a lower bound on the mutual information. And because a loss is never negative, the bound can never "
            "say more than log N."
        ) as vo:
            step(0)
            for i, mk in enumerate("abcde", 1):
                vo.wait_until(mk)
                step(i)
            vo.wait_until("f")
            self.play(FadeIn(fin, shift=UP * 0.15))
            self.play(FadeIn(caveat))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def check(self):
        r = load("infonce")
        Ns, mis = list(r["Ns"]), list(r["mis"])
        est = r["est"]
        lx = [math.log2(n) for n in Ns]
        top = max(mis) + 1
        ax = axes([0.5, lx[-1] + 0.5], [0, top], x_length=8.2, y_length=4.6, xlabel=r"candidates $N$ (log scale)",
                  ylabel=r"nats", xticks=lx, yticks=[0, 2, 4, 6, 8, 10],
                  xfmt=lambda v: f"{int(round(2 ** v))}", center=[-1.2, -0.3, 0])
        A = ax.ax
        ceil = DashedLine(A.c2p(0.5, math.log(2 ** 0.5)), A.c2p(lx[-1] + 0.5, math.log(2 ** (lx[-1] + 0.5))),
                          color=LOGN, stroke_width=2.5)
        cl = MathTex(r"\log N", font_size=30, color=LOGN).next_to(ceil.get_end(), UP, buff=0.1).shift(LEFT * 0.4)
        truths, pts = VGroup(), VGroup()
        cols = [C.INTERVAL, EST, C.SURPRISE]
        for I, col in zip(mis, cols):
            truths.add(DashedLine(A.c2p(0.5, I), A.c2p(lx[-1] + 0.5, I), color=col, stroke_width=1.5,
                                  dash_length=0.05).set_opacity(0.7))
            truths.add(MathTex(rf"I = {I:g}", font_size=26, color=col).next_to(A.c2p(lx[-1] + 0.5, I), RIGHT,
                                                                                buff=0.15))
            g = VGroup()
            for N, x_ in zip(Ns, lx):
                e = [est[f"I{I:g}_N{N}_s{s}"] for s in (0, 1)]
                g.add(VGroup(Line(A.c2p(x_, min(e)), A.c2p(x_, max(e)), color=col, stroke_width=2),
                             Dot(A.c2p(x_, float(np.mean(e))), radius=0.06, color=col)))
            g.add(curve(A, lx, [np.mean([est[f"I{I:g}_N{N}_s{s}"] for s in (0, 1)]) for N in Ns], col, 2))
            pts.add(g)
        setup = label(rf"$X, Y \in \mathbb R^{{{int(r['d'])}}}$: \ correlated Gaussians, \\ $I(X;Y)$ known exactly",
                      font_size=22, color=GREY_A).to_corner(UR, buff=0.4)
        tg = tag(r"computed: \ a critic trained at each $N$, \ two seeds")
        big = max(mis)
        e_big = max(est[f"I{big:g}_N{Ns[-1]}_s{s}"] for s in (0, 1))
        small = min(mis)
        near = [N for N in Ns if np.mean([est[f"I{small:g}_N{N}_s{s}"] for s in (0, 1)]) >= 0.9 * small]
        s_line = (f"With {small:g} nats to find, the estimate comes within ten percent of the truth once there are "
                  f"{near[0]} candidates." if near else
                  f"Even with {small:g} nats to find, the estimate never comes within ten percent of the truth.")
        with self.voiceover(
            "We can watch the ceiling. Take pairs of Gaussian vectors with a known amount of shared information: "
            f"{mis[0]:g}, {mis[1]:g} or {mis[2]:g} nats. Train a small scoring network with InfoNCE at each number "
            "of candidates N, from two to five hundred and twelve, and read off log N minus the loss. <bookmark "
            f"mark='a'/> {s_line} <bookmark mark='b'/> But with {big:g} nats to find, the estimate climbs along the "
            f"log N line and stops at {e_big:.1f} nats, even with {Ns[-1]} candidates. The loss cannot see more "
            "information than the number of candidates lets it. <bookmark mark='c'/> That is one reason "
            "contrastive learning wants big batches."
        ) as vo:
            self.play(FadeIn(ax), Create(ceil), FadeIn(cl), FadeIn(setup), FadeIn(tg))
            self.play(FadeIn(truths))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in pts[0][:-1]], lag_ratio=0.1), Create(pts[0][-1]),
                      run_time=2.0)
            self.play(LaggedStart(*[FadeIn(m) for m in pts[1][:-1]], lag_ratio=0.1), Create(pts[1][-1]),
                      run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m) for m in pts[2][:-1]], lag_ratio=0.1), Create(pts[2][-1]),
                      run_time=2.0)
            vo.wait_until("c")
            self.play(Indicate(ceil, color=LOGN))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cpc(self):
        xs = VGroup(*[Rectangle(width=0.5, height=0.9, stroke_color=GREY_C, stroke_width=1.5, fill_color=SIMCLR,
                                fill_opacity=0.15 + 0.08 * i) for i in range(6)]).arrange(RIGHT, buff=0.1)
        xs.move_to([-3.4, -0.6, 0])
        zs = VGroup(*[Circle(radius=0.16, stroke_color=SIMCLR, fill_color=SIMCLR, fill_opacity=0.5).next_to(b, UP,
                                                                                                         buff=0.5)
                      for b in xs])
        c = node_box(r"context $c_t$", C.CONTEXT, font_size=22).next_to(zs[3], UP, buff=0.6)
        fut = VGroup(*[Circle(radius=0.16, stroke_color=POS, fill_color=POS, fill_opacity=0.5) for _ in range(2)])
        fut.arrange(RIGHT, buff=0.35).next_to(xs, RIGHT, buff=0.5).align_to(zs, UP)
        fx = VGroup(*[Rectangle(width=0.5, height=0.9, stroke_color=GREY_D, stroke_width=1.2) for _ in range(2)])
        fx.arrange(RIGHT, buff=0.1).next_to(xs, RIGHT, buff=0.45)
        arr = VGroup(*[arrow(z.get_top(), c.get_bottom(), color=GREY_C, stroke_width=1.5) for z in zs[:4]])
        parr = VGroup(*[CurvedArrow(c.get_right(), f_.get_top(), color=POS, angle=-0.6, stroke_width=2)
                        for f_ in fut])
        cap = label(r"from the past, \ pick the real future \\ out of $N$ candidates: \ InfoNCE", font_size=24,
                    color=GREY_A).move_to([3.6, 1.6, 0])
        doms = label(r"speech, \ images, \ text, \ 3D games", font_size=22, color=GREY_B).next_to(cap, DOWN, buff=0.3)
        src = cite(r"van den Oord, Li \& Vinyals (2018): \ contrastive predictive coding")
        tk = take_away(r"a contrastive loss is a classifier over $N$ candidates, \ and a bound on information "
                       r"capped at $\log N$")
        with self.voiceover(
            "The paper's own model, contrastive predictive coding, applied this to sequences. Encode a stretch of "
            "speech or a row of image patches, <bookmark mark='a'/> summarize the past in a context vector, "
            "<bookmark mark='b'/> and from it pick the real future encodings out of N candidates. It worked on "
            "speech, images, text and 3D games. <bookmark mark='c'/> Everything contrastive in this part is this "
            "loss with a different choice of what counts as a partner."
        ) as vo:
            self.play(FadeIn(xs), FadeIn(fx), FadeIn(zs), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(c), LaggedStart(*[GrowArrow(a) for a in arr], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(fut), *[Create(p) for p in parr], FadeIn(cap))
            self.play(FadeIn(doms))
            vo.wait_until("c")
            self.play(FadeIn(tk, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
