from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai11.common import A, K, Q, V, load, signed_image


def forward_pass_picture() -> VGroup:
    """One run of a network: a column of numbers goes in, passes each layer once, a guess comes out; the weights stay
    locked."""
    g = np.random.default_rng(2)
    col = VGroup(*[Square(0.26, stroke_width=0.8, stroke_color=GREY_D, fill_color=C.EMBED,
                          fill_opacity=float(0.25 + 0.6 * abs(v) / 2)) for v in np.clip(g.normal(size=4), -2, 2)])
    col.arrange(DOWN, buff=0)
    layers = VGroup(*[RoundedRectangle(width=0.55, height=1.15, corner_radius=0.08, stroke_color=C.BITS,
                                       stroke_width=2.5, fill_color=C.BITS, fill_opacity=0.12) for _ in range(3)])
    probs = [0.15, 0.6, 0.25]
    bars = VGroup(*[Rectangle(width=0.16, height=0.9 * p + 0.02, stroke_width=0, fill_color=C.PROB, fill_opacity=0.9)
                    for p in probs]).arrange(RIGHT, buff=0.06, aligned_edge=DOWN)
    row = VGroup(col, *layers, bars).arrange(RIGHT, buff=0.5)
    arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.06, color=GREY_B, stroke_width=2.5,
                            max_tip_length_to_length_ratio=0.35) for a, b in zip(row[:-1], row[1:])])
    names = VGroup(label(r"numbers in", font_size=18, color=C.EMBED).next_to(col, DOWN, buff=0.12),
                   label(r"each layer, once", font_size=18, color=C.BITS).next_to(layers, DOWN, buff=0.12),
                   label(r"a guess", font_size=18, color=C.PROB).next_to(bars, DOWN, buff=0.12))
    names[2].align_to(names[0], DOWN)
    body = Rectangle(width=0.26, height=0.2, stroke_width=0, fill_color=GREY_B, fill_opacity=1)
    shackle = Arc(radius=0.09, start_angle=0, angle=PI, color=GREY_B, stroke_width=3).next_to(body, UP, buff=0)
    lock = VGroup(shackle, body).next_to(layers, UP, buff=0.12)
    lock_l = label(r"weights locked", font_size=18, color=GREY_B).next_to(lock, RIGHT, buff=0.1)
    return VGroup(row, arrows, names, lock, lock_l)


class InContext(VoiceoverScene):
    def construct(self):
        self.card()
        self.prompt()
        self.matrices()
        self.agree()
        self.deeper()

    def card(self):
        card = chapter_card(6, r"Learning inside the prompt", r"Can a forward pass run a learning algorithm?", part=11)
        with self.voiceover("Chapter six. Learning inside the prompt."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def prompt(self):
        d = load("icl")
        dim, N = int(d["d"]), int(d["N"])
        g = np.random.default_rng(4)
        w = g.normal(size=dim)
        xs = g.normal(size=(8, dim))
        cols = VGroup()
        for j in range(8):
            last = j == 7
            col = VGroup(*[Square(0.34, stroke_width=1, stroke_color=GREY_D, fill_color=K,
                                  fill_opacity=float(0.25 + 0.6 * min(abs(v) / 2, 1))) for v in xs[j]],
                         Square(0.34, stroke_width=1.5 if last else 1, stroke_color=Q if last else GREY_D,
                                fill_color=V if not last else BACKGROUND,
                                fill_opacity=float(0.25 + 0.6 * min(abs(xs[j] @ w) / 3, 1)) if not last else 1))
            col.arrange(DOWN, buff=0.04)
            cols.add(col)
        dots = MathTex(r"\cdots", font_size=40, color=GREY_B)
        row = VGroup(*cols[:6], dots, cols[6], cols[7]).arrange(RIGHT, buff=0.22).move_to(UP * 0.6)
        qm = MathTex(r"?", font_size=30, color=Q).move_to(cols[7][-1])
        xl = label(rf"$x_i$: \ ${dim}$ numbers", font_size=24, color=K).next_to(row, LEFT, buff=0.4).align_to(cols[0][0], UP)
        yl = label(r"$y_i = w \cdot x_i$", font_size=24, color=V).next_to(row, LEFT, buff=0.4).align_to(cols[0][-1], DOWN)
        br = Brace(VGroup(*cols[:6], cols[6]), DOWN, color=GREY_B)
        bl = label(rf"${N}$ examples", font_size=24, color=GREY_B).next_to(br, DOWN, buff=0.1)
        ql = label(r"the question", font_size=24, color=Q).next_to(cols[7], DOWN, buff=0.45)
        hidden = label(r"a different hidden $w$ in every prompt", font_size=28, color=GREY_A).to_edge(DOWN, buff=0.7)
        cite_ = cite(r"S.~Garg, D.~Tsipras, P.~Liang \& G.~Valiant, \textit{What Can Transformers Learn In-Context?} (2022)",
                     corner=UR)
        fp = gloss(r"forward pass", r"one run of the network: numbers go in, flow through \\ each layer once, "
                   r"and a guess comes out. \ No weight changes.", forward_pass_picture(), width=6.2,
                   color=C.BITS).move_to(DOWN * 0.3)
        with self.voiceover(
            "Large models learn from examples in their prompt, without changing a single weight. Show one a few "
            "translations, and it translates the next. How can a forward pass learn? <bookmark mark='f'/> A forward "
            "pass is one run of the network: numbers go in, flow through each layer once, and a guess comes out. "
            "Nothing in it changes a weight. Here's a case small enough to "
            "take apart completely. <bookmark mark='a'/> Each prompt is a list of examples: four numbers x, and an "
            "answer y, which is a fixed weighted sum of them. Then a question: a new x, with the answer missing. "
            "<bookmark mark='b'/> The catch: every prompt uses different hidden weights, so nothing can be "
            "memorized. To answer, the model has to work out the rule from the examples in front of it."
        ) as vo:
            self.play(FadeIn(cite_))
            vo.wait_until("f")
            self.play(FadeIn(fp, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(fp))
            self.play(LaggedStart(*[FadeIn(c_, shift=DOWN * 0.1) for c_ in row], lag_ratio=0.12), FadeIn(xl), FadeIn(yl),
                      run_time=2.0)
            self.play(FadeIn(qm), FadeIn(br), FadeIn(bl), FadeIn(ql))
            vo.wait_until("b")
            self.play(FadeIn(hidden))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def matrices(self):
        d = load("icl")
        dim, N = int(d["d"]), int(d["N"])
        Wkq, Wpv = np.asarray(d["Wkq"]), np.asarray(d["Wpv"])
        colors = {r"W_{KQ}": A, r"W_{PV}": V}
        f = cmath(r"e_j \;\leftarrow\; e_j + \frac{1}{N}\sum_{i}", r"W_{PV}", r"\,e_i\,\big(e_i^{\top}", r"W_{KQ}",
                  r"\,e_j\big)", colors=colors, font_size=38).to_edge(UP, buff=0.4)
        fl = label(r"one layer of attention, \ without the softmax; \ $e_i = (x_i, y_i)$", font_size=24,
                   color=GREY_A).next_to(f, DOWN, buff=0.15)
        S = 2.4
        learned = Group(signed_image(Wkq, S, S), signed_image(Wpv, S, S)).arrange(RIGHT, buff=0.8).move_to([-3.3, -0.9, 0])
        theory_kq = np.zeros((dim + 1, dim + 1))
        theory_kq[:dim, :dim] = np.eye(dim)
        theory_pv = np.zeros((dim + 1, dim + 1))
        theory_pv[dim, dim] = 1
        theory = Group(signed_image(theory_kq, S, S), signed_image(theory_pv, S, S)).arrange(RIGHT, buff=0.8)
        theory.move_to([3.3, -0.9, 0])
        for grp in (learned, theory):
            for img in list(grp):  # a copy: adding to the group while walking it never ends
                grp.add(SurroundingRectangle(img, buff=0, color=GREY_D, stroke_width=1.5))
        names = VGroup(*[MathTex(t, font_size=32, color=c_).next_to(img, UP, buff=0.12)
                         for t, c_, img in ((r"W_{KQ}", A, learned[0]), (r"W_{PV}", V, learned[1]),
                                            (r"W_{KQ}", A, theory[0]), (r"W_{PV}", V, theory[1]))])
        t1 = label(r"learned, \ from $6{,}000$ batches of prompts", font_size=24, color=WHITE).next_to(learned, DOWN, buff=0.3)
        t2 = label(r"one step of gradient descent, \ written as attention", font_size=24, color=C.BITS)
        t2.next_to(theory, DOWN, buff=0.3)
        gd = cmath(r"w_1 = \frac{\eta}{N}\sum_i y_i\, x_i", r"\quad\Rightarrow\quad",
                   r"\hat y = \frac{\eta}{N}\sum_i y_i\,(x_i \cdot x_q)", font_size=32).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Take the simplest attention: one layer, with no softmax. Every token is an example's numbers and its "
            "answer, and attention adds to each token a weighted sum of the others. Train it on many prompts. "
            "<bookmark mark='a'/> Here are the two matrices it learned. Blue is positive, red negative. "
            "<bookmark mark='b'/> Now do something else: one step of gradient descent on the prompt's examples, "
            "starting from zero, for the least-squares loss of part five. The step is a sum of each answer times its "
            "x, and the prediction is a sum of each answer times how well its x matches the question: a dot product "
            "of x's, weighting the y's. <bookmark mark='c'/> That is attention, with these two matrices: an "
            "identity block that compares x's, and one entry that passes on the y's. They're the same pattern the "
            "network found by itself."
        ) as vo:
            self.play(Write(f), FadeIn(fl))
            vo.wait_until("a")
            self.play(FadeIn(learned), FadeIn(names[0]), FadeIn(names[1]), FadeIn(t1))
            vo.wait_until("b")
            self.play(Write(gd), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(theory), FadeIn(names[2]), FadeIn(names[3]), FadeIn(t2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def agree(self):
        d = load("icl")
        pl, pg, tr = np.asarray(d["pred_lsa"]), np.asarray(d["pred_gd"]), np.asarray(d["truth"])
        lim = float(np.ceil(np.percentile(np.abs(np.concatenate([pl, pg])), 98)))
        ax = Axes(x_range=[-lim, lim, lim / 2], y_range=[-lim, lim, lim / 2], x_length=5.0, y_length=5.0, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-3.2, -0.4, 0])
        diag = DashedLine(ax.c2p(-lim, -lim), ax.c2p(lim, lim), color=GREY_B, stroke_width=1.5)
        pts = VGroup(*[Dot(ax.c2p(float(np.clip(a, -lim, lim)), float(np.clip(b, -lim, lim))), radius=0.04, color=Q)
                       for a, b in zip(pg, pl)])
        xn = label(r"one step of gradient descent", font_size=24, color=C.BITS).next_to(ax, DOWN, buff=0.15)
        yn = label(r"the trained attention layer", font_size=24, color=A).rotate(PI / 2).next_to(ax, LEFT, buff=0.15)
        r_ = float(d["agree1"])
        rl = label(rf"correlation ${r_:.3f}$", font_size=32, color=WHITE).move_to([3.2, 1.6, 0])
        expl = label(r"on $4{,}000$ new prompts: \\ the forward pass \emph{is} \\ a step of learning", font_size=28,
                     color=GREY_A).next_to(rl, DOWN, buff=0.5)
        cite_ = cite(r"J.~von Oswald et al., \textit{Transformers Learn In-Context by Gradient Descent} (2023)", corner=DR)
        dl = label(r"same answer", font_size=20, color=GREY_B).next_to(ax.c2p(lim, lim), RIGHT, buff=0.1)
        corr = gloss(r"correlation", r"how closely the dots hug a straight line: \\ $1$ means exactly on it, "
                     r"$0$ means no line at all", width=4.6, color=GREY_A).move_to([3.2, -1.75, 0])
        assert r_ > 0.99
        with self.voiceover(
            "Check it on four thousand new prompts. Each dot is one question: across, the answer from one step of "
            "gradient descent; up, the trained attention layer's answer. <bookmark mark='a'/> They lie on a line. "
            f"The correlation is {r_:.3f}. Correlation measures how closely the dots hug a straight line, and one "
            "would mean exactly on it. The forward pass of this network is a step of learning, run on the "
            "examples in its prompt. Johannes von Oswald and colleagues showed this in 2023."
        ) as vo:
            self.play(Create(ax), Create(diag), FadeIn(dl), FadeIn(xn), FadeIn(yn), FadeIn(cite_))
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.005), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(rl), FadeIn(expl))
            self.play(FadeIn(corr, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def deeper(self):
        d = load("icl")
        zero = float(d["zero"])
        rows = [(rf"guess $0$", zero, GREY_B)]
        for k in (1, 2, 3):
            rows.append((rf"${k}$ step{'s' if k > 1 else ''} of gradient descent", float(d[f"gd{k}"]), C.BITS))
            rows.append((rf"${k}$ attention layer{'s' if k > 1 else ''}, trained", float(d[f"lsa{k}"]), A))
        rows.append((r"least squares, \ solved exactly", float(d["lstsq"]), C.TRUE_P))
        scale = 6.0 / zero
        g = VGroup()
        for i, (t, v, c_) in enumerate(rows):
            y = 2.3 - i * 0.62
            name = label(t, font_size=24, color=c_).move_to([-3.0, y, 0], aligned_edge=RIGHT)
            bar = Rectangle(width=max(v * scale, 0.02), height=0.36, stroke_width=0, fill_color=c_, fill_opacity=0.85)
            bar.move_to([-2.7 + max(v * scale, 0.02) / 2, y, 0])
            val = MathTex(f"{v:.2f}", font_size=26, color=c_).next_to(bar, RIGHT, buff=0.12)
            g.add(VGroup(name, bar, val))
        head = label(r"mean squared error on new prompts", font_size=28, color=GREY_A).to_edge(UP, buff=0.3)
        beats = all(d[f"lsa{k}"] <= d[f"gd{k}"] * 1.02 for k in (2, 3))
        with self.voiceover(
            "Stack more layers, and each can take another step. <bookmark mark='a'/> One layer matches one step of "
            "gradient descent"
            + (f". Two layers beat two plain steps, {d['lsa2']:.2f} against {d['gd2']:.2f}: trained, the network "
               "finds a smarter kind of step than the textbook one. " if beats and d["lsa2"] < 0.8 * d["gd2"] else
               ", and more layers keep pace with more steps. ")
            + "<bookmark mark='b'/> Exact least squares, from part five, gets every answer right here, so there's "
            "room to grow. Real transformers, with softmax attention and many layers, are messier than this, but "
            "the lesson carries over: a forward pass can run a learning algorithm on the prompt."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g[1:-1]], lag_ratio=0.35), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(g[-1]))
        self.wait(0.3)
        self.clear_scene()
