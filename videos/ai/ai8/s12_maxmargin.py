from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai8.common import BOUND, HIST, MEAS, NEG, POS, chapter, curve, load

GD, SVM = C.BITS, C.INTERVAL


class MaxMargin(VoiceoverScene):
    def construct(self):
        chapter(self, 11, r"Implicit bias: the widest margin", r"What does a classifier do once it is perfect?",
                "Chapter eleven. Implicit bias: the widest margin.")
        self.replay()
        self.why()
        self.rate()

    # ------------------------------------------------------------------
    def replay(self):
        m = load("maxmargin")
        X, t = np.asarray(m["X"]), np.asarray(m["t"])
        rec = np.asarray(m["rec"])
        ws = np.asarray(m["w_svm"])
        ax = Axes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], x_length=6.0, y_length=6.0, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to([-3.4, -0.3, 0])
        dots = VGroup(*[Dot(ax.c2p(*np.clip(p, -2.9, 2.9)), radius=0.06, color=POS if y > 0 else NEG) for p, y in zip(X, t)])

        def boundary(w, color, dashed=False, sw=3.5):
            u = np.asarray(w, float) / np.linalg.norm(w)
            d = np.array([-u[1], u[0]])
            L = (DashedLine if dashed else Line)(ax.c2p(*(-3.0 * d)), ax.c2p(*(3.0 * d)), color=color, stroke_width=sw)
            return L

        svm = boundary(ws, SVM, dashed=True, sw=3)
        sl = label(r"widest margin \ (SVM)", font_size=22, color=SVM).next_to(svm.get_end(), RIGHT, buff=0.15)
        keep_in_frame(sl)
        k = ValueTracker(0)

        def wk():
            i = int(np.clip(round(k.get_value()), 0, len(rec) - 1))
            return rec[i]

        line = always_redraw(lambda: boundary(wk()[5:7], GD, sw=4))
        read = always_redraw(lambda: VGroup(
            label(rf"step ${fmt_int(wk()[0])}$", font_size=26, color=WHITE),
            label(rf"angle to the widest-margin direction: \ ${wk()[1]:.1f}^\circ$", font_size=24, color=GD),
            label(rf"$|w| = {wk()[2]:.2f}$", font_size=24, color=GREY_A),
            label(rf"loss ${sci(wk()[3], 1)}$", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.4, 1.4, 0]))
        head = label(r"Logistic regression, \ gradient descent, \ separable points", font_size=28).to_edge(UP, buff=0.3)
        idx = [int(np.argmin(np.abs(rec[:, 0] - v))) for v in (100, 10_000, 1_000_000)]
        a0 = float(rec[0, 1])
        with self.voiceover(
            "Classification has its own version. When the classes can be separated, the logistic loss can be made "
            "as small as you like, just by scaling the weights up, so there's no minimum at all, and infinitely "
            "many separating lines. <bookmark mark='a'/> Which direction does gradient descent head in? Here it is, "
            f"step by step on a log scale. After one step the boundary is {a0:.0f} degrees from the widest-margin "
            f"line. <bookmark mark='b'/> After a hundred steps, {rec[idx[0], 1]:.1f}; after ten thousand, "
            f"{rec[idx[1], 1]:.1f}; after a million, {rec[idx[2], 1]:.1f}. It turns toward the support vector "
            "machine's line, slowly, while the weights keep growing and the loss keeps shrinking."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(dots), Create(svm), FadeIn(sl))
            vo.wait_until("a")
            self.add(line, read)
            vo.wait_until("b")
            self.play(k.animate.set_value(len(rec) - 1), run_time=max(4.0, vo.remaining() - 0.5),
                      rate_func=linear)
        line.clear_updaters()
        read.clear_updaters()
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        rows = [
            cmath(r"-\nabla L(w)", r"=", r"\frac1n \sum_i \frac{y_i x_i}{1 + e^{\,y_i\, w \cdot x_i}}", font_size=32),
            cmath(r"-\nabla L(w)", r"\approx", r"\frac1n \sum_i e^{-y_i\, w \cdot x_i}\, y_i x_i", font_size=32),
            cmath(r"-\nabla L(w)", r"\approx", r"\frac1n \sum_{i \in \mathrm{SV}} e^{-y_i\, w \cdot x_i}\, y_i x_i",
                  font_size=32),
            cmath(r"\frac{w(t)}{|w(t)|}", r"\to", r"\frac{\hat w}{|\hat w|}, \quad \hat w = \sum_{i \in \mathrm{SV}} "
                  r"\alpha_i y_i x_i", font_size=32, colors={r"\frac{\hat w}{|\hat w|}, \quad \hat w = \sum_{i \in "
                                                              r"\mathrm{SV}} \alpha_i y_i x_i": SVM}),
        ]
        whys = [why(r"the logistic loss, \ $L = \frac1n\sum_i \ln(1 + e^{-y_i w \cdot x_i})$"),
                why(r"once all are right and $|w|$ is large"),
                why(r"exponential tails: \ the smallest margins dominate"),
                why(r"the SVM's form \ (KKT, \ Part 4)")]
        step = ladder(self, rows, whys, keep=3, top=3.1, x=-1.8, buff=0.42, edge=6.9)
        thm = theorem_card(r"implicit bias on separable data",
                           r"separable linear data, \ sufficiently small positive constant step: \ $|w(t)|$ grows like "
                           r"$\log t$; \ direction tends to the hard-margin SVM's. \ Error: "
                           r"$O(1/\log t)$ for almost all datasets; \ $O(\log\log t/\log t)$ in general.",
                           who=r"D.~Soudry, E.~Hoffer, M.~S.~Nacson, S.~Gunasekar \& N.~Srebro (2018)", width=8.0,
                           font_size=20).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Why that line? <bookmark mark='a'/> The negative gradient is a weighted sum of the examples, each "
            "weighted by how badly it's classified. <bookmark mark='b'/> Once every point is right and the weights "
            "are large, those weights are exponentials of minus the margins. <bookmark mark='c'/> Exponentials "
            "decay so fast that the points with the smallest margins outweigh everything else: only the support "
            "vectors steer. <bookmark mark='d'/> The direction converges to a combination of support vectors with "
            "positive weights, which is exactly the form of the max-margin solution from part four's KKT conditions. "
            "Soudry and colleagues proved it in 2018 for a sufficiently small positive constant step. The weights grow like log t; for almost all datasets, direction "
            "error is bounded by a constant over log t, with an extra log log t factor in degenerate cases. Lyu and Li connected homogeneous neural networks to margin maximization in 2020."
        ) as vo:
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                step(k)
            self.play(FadeIn(thm, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rate(self):
        m = load("maxmargin")
        rec = np.asarray(m["rec"])
        ok = rec[:, 0] >= 10
        lt = np.log10(rec[ok, 0])
        G = axes([1, 6], [0, 32], x_length=5.6, y_length=3.8, xticks=[1, 2, 3, 4, 5, 6],
                 xfmt=lambda v: f"10^{{{int(v)}}}", yticks=[0, 10, 20, 30], yfmt=lambda v: rf"{v:g}^\circ",
                 xlabel=r"step $t$", ylabel=r"angle to the SVM direction", center=(-3.3, -0.4, 0))
        ax = G.ax
        ca = curve(ax, lt, np.clip(rec[ok, 1], 0, 32), GD, 4)
        late = rec[:, 0] >= 1000
        c_end = float(rec[-1, 1] * math.log(rec[-1, 0]))
        ref = curve(ax, lt, np.clip(c_end / np.log(rec[ok, 0]), 0, 32), GREY_B, 2.5)
        rl = label(r"$c/\ln t$, \ through the last point", font_size=19, color=GREY_B).next_to(ax.c2p(3.6, 9.0), UR, buff=0.05)
        H = axes([1, 6], [0, 12], x_length=5.6, y_length=3.8, xticks=[1, 2, 3, 4, 5, 6],
                 xfmt=lambda v: f"10^{{{int(v)}}}", yticks=[0, 4, 8, 12], xlabel=r"step $t$ \ (log scale)",
                 ylabel=r"$|w(t)|$", center=(3.3, -0.4, 0))
        hx = H.ax
        cn = curve(hx, lt, rec[ok, 2], MEAS, 4)
        slope = float(np.polyfit(np.log(rec[late, 0]), rec[late, 2], 1)[0])
        info = label(rf"from $10^3$ steps on: \ $|w|$ gains ${slope * math.log(10):.2f}$ per factor of ten; \ "
                     rf"margin ${m['margin_end']:.3f}$ of the best ${m['gamma']:.3f}$", font_size=22, color=GREY_A)
        info.to_edge(DOWN, buff=0.3)
        ratio = float(m["c_hi"] / m["c_lo"])
        settled = ratio < 1.3
        pace = ("Angle times log t is nearly constant from a thousand steps on, consistent with the generic one over log t rate. "
                if settled else
                f"Angle times log t falls from {m['c_hi']:.0f} to {m['c_lo']:.0f} between a thousand and a million "
                "steps: over this range it falls faster than the one over log t reference. ")
        with self.voiceover(
            "Measure it. <bookmark mark='a'/> On a log axis of steps, the norm of the weights is a straight line: it "
            f"grows by about {slope * math.log(10):.2f} for every factor of ten in steps, logarithmic growth. "
            "<bookmark mark='b'/> The angle falls, slowly. "
            + pace
            + f"After a million steps the margin is {m['margin_end']:.3f}, against the best possible "
            f"{m['gamma']:.3f}. That slowness has a practical side: training long after the training error reaches "
            "zero keeps changing the model, toward larger margins, which is the boosting story again, now as a "
            "theorem about gradient descent."
        ) as vo:
            self.play(FadeIn(G), FadeIn(H))
            vo.wait_until("a")
            self.play(Create(cn), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(ca), run_time=1.6)
            self.play(Create(ref), FadeIn(rl), FadeIn(info))
        self.wait(0.3)
        self.clear_scene()
