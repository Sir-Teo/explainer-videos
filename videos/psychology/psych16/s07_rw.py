from __future__ import annotations

import numpy as np

from videos.psychology.psych16.common import *  # noqa: F403


class RescorlaWagner(VoiceoverScene):
    def construct(self):
        self.card()
        self.rule()
        self.derive()
        self.curves()
        self.surface()

    def card(self):
        card = chapter_card(6, r"The Rescorla-Wagner rule", r"What machine learns from surprise?",
                            lit={1972: r"Rescorla \& Wagner", 1960: r"Widrow \& Hoff"}, part=PART, scale=("mind",),
                            marr=("what", "how"))
        with self.voiceover("Chapter six. The Rescorla-Wagner rule."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def rule(self):
        head = heading(r"One line, \ 1972")
        eq = MathTex(r"\Delta V_X", r"=", r"\alpha_X", r"\,\beta", r"\,\big(", r"\lambda", r"-", r"\textstyle\sum_{i} V_i",
                     r"\big)", font_size=64).move_to([0, 1.6, 0])
        eq[0].set_color(CR)
        eq[2].set_color(CS)
        eq[3].set_color(US)
        eq[5].set_color(US)
        eq[7].set_color(CUE_A)
        rows = rows_of([
            (r"$V_X$: \ the strength of cue X's association with the outcome, \ its prediction", CR),
            (r"$\lambda$: \ the outcome that actually happened \ (1 for food or shock, \ 0 for nothing)", US),
            (r"$\sum V_i$: \ what all the cues present predicted, \ together", CUE_A),
            (r"$\lambda - \sum V_i$: \ the prediction error, \ Kamin's surprise", YOU),
            (r"$\alpha_X$ and $\beta$: \ learning rates set by how salient the cue and the outcome are", CS),
        ], 12.4, 27, 0.3).move_to([0, -1.2, 0])
        tag = historical_tag(archive.RESCORLA_WAGNER_1972.cite)
        with self.voiceover(
            "In 1972 Robert Rescorla and Allan Wagner wrote the idea of surprise as a single line. "
            "<bookmark mark='a'/> Every cue X carries a number, V of X: the strength of its association with the "
            "outcome, which you can read as the prediction it makes. <bookmark mark='b'/> On each trial an outcome "
            "happens, lambda: one if the food or shock arrives, zero if nothing does. <bookmark mark='c'/> The cues "
            "present make a prediction together, the sum of their strengths. That sum is the important move: cues "
            "share the prediction, so they compete for it. <bookmark mark='d'/> The difference between what happened "
            "and what was predicted is the prediction error, Kamin's surprise. <bookmark mark='e'/> Every cue present "
            "changes its strength in proportion to that error, scaled by two learning rates, alpha for the cue's "
            "salience and beta for the outcome's. If the outcome was fully predicted, the error is zero, and nothing "
            "is learned."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Write(eq))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def derive(self):
        head = heading(r"Derived: \ gradient descent on the squared error")
        lines = VGroup(
            MathTex(r"E = \tfrac12\,\big(\lambda - \textstyle\sum_i x_i V_i\big)^2", font_size=44),
            MathTex(r"\frac{\partial E}{\partial V_X} = -\big(\lambda - \textstyle\sum_i x_i V_i\big)\,x_X",
                    font_size=44),
            MathTex(r"\Delta V_X = -\eta\,\frac{\partial E}{\partial V_X} = \eta\,\big(\lambda - \textstyle\sum_i x_i V_i"
                    r"\big)\,x_X", font_size=44),
        ).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([-1.6, 1.0, 0])
        lines[2].set_color(CR)
        notes = VGroup(
            label(r"$x_i = 1$ if cue $i$ is present, \ 0 if not", font_size=24, color=GREY_A),
            label(r"step downhill, \ with $\eta = \alpha_X \beta$", font_size=24, color=CR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(lines, RIGHT, buff=0.5).shift(DOWN * 0.3)
        keep_in_frame(notes)
        rows = rows_of([
            (r"the same rule as Widrow and Hoff's delta rule for adaptive circuits, \ 1960", CS),
            (r"and the least-mean-squares learning inside every linear neuron of \emph{AI, \ Built}, \ Part 9", US),
            (r"a rat, \ an echo canceller and a linear network learn the same way: \ reduce the squared error of "
             r"a prediction", YOU),
        ], 12.4, 27, 0.28).to_edge(DOWN, buff=0.75)
        with self.voiceover(
            "Here's why the rule has lasted. <bookmark mark='a'/> Define the error of a trial as half the square of "
            "the prediction error. The x's say which cues are present: one if present, zero if not. "
            "<bookmark mark='b'/> Differentiate with respect to cue X's strength, and you get minus the prediction "
            "error, times x. <bookmark mark='c'/> Step a little way downhill, against the gradient, and you have "
            "exactly the Rescorla-Wagner rule, with the step size alpha times beta. Conditioning, on this account, is "
            "gradient descent on the squared error of a prediction. <bookmark mark='d'/> Engineers had found the same "
            "rule twelve years earlier: Bernard Widrow and Ted Hoff's delta rule, which still runs in the echo "
            "cancellers of telephones. <bookmark mark='e'/> And it's the least-mean-squares learning inside a linear "
            "neuron, which the series built from scratch in AI, Built. <bookmark mark='f'/> A rat, an echo "
            "canceller and a neural network learn by the same principle."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(lines[0]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Write(lines[1]))
            vo.wait_until("c")
            self.play(Write(lines[2]), FadeIn(notes[1]))
            for m, r in zip("def", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def curves(self):
        d = load("rw")
        head = heading(r"Acquisition and extinction, \ computed")
        A = axes([0, 60], [0, 1.05], x_length=8.4, y_length=3.8, xticks=[0, 10, 20, 30, 40, 50, 60],
                 yticks=[0, 0.5, 1], xlabel=r"trial", ylabel=r"$V$, \ the cue's strength", center=[-1.6, 0.4, 0])
        ax = A.ax
        x = np.arange(61)
        c1 = curve(ax, x[:31], d["acq_ext"][:31], CR, stroke_width=4)
        c2 = curve(ax, x[30:], d["acq_ext"][30:], INHIB, stroke_width=4)
        lam = DashedLine(ax.c2p(0, 1), ax.c2p(30, 1), color=US, stroke_width=2)
        ll = label(r"$\lambda = 1$", font_size=22, color=US).next_to(ax.c2p(0, 1), UR, buff=0.06).shift(RIGHT * 0.3)
        rows = rows_of([
            (r"big errors early, \ big steps; \ the curve bends as the error shrinks", CR),
            (r"each step is a fixed share of the remaining error: \ an exponential approach", WHITE),
            (r"extinction: \ $\lambda = 0$, \ and $V$ falls back to zero", INHIB),
            (r"but that says extinction is unlearning: \ chapter eight shows it is not", BAD),
        ], 3.9, 24, 0.34).move_to([4.8, 0.3, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ \texttt{conditioning.rescorla\_wagner}, \ $\alpha\beta = 0.15$")
        with self.voiceover(
            "Run it on Pavlov's dog. <bookmark mark='a'/> At first the cue predicts nothing, the error is large and "
            "the strength jumps. As the prediction improves, the error and the steps shrink, and the curve bends over "
            "toward lambda. <bookmark mark='b'/> Each step is a fixed fraction of the remaining error, so the "
            "approach is exponential: the negatively accelerated learning curve seen in experiment after experiment. "
            "<bookmark mark='c'/> Now stop the food. Lambda is zero, the error is negative, and the strength falls "
            "back toward zero by the same rule. <bookmark mark='d'/> Notice what the model has said: that extinction "
            "is unlearning, a return to the state before training. Pavlov's dogs, with their recovery the next day, "
            "have already told us that's wrong. We'll come back to it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag), Create(lam), FadeIn(ll))
            vo.wait_until("a")
            self.play(Create(c1), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(c2), FadeIn(rows[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def surface(self):
        d = load("rw")
        head = heading(r"Blocking, \ seen on the error surface")
        g = d["grid"]
        S = d["surface"]
        A = axes([-0.2, 1.2], [-0.2, 1.2], x_length=5.4, y_length=5.4, xticks=[0, 0.5, 1], yticks=[0, 0.5, 1],
                 xlabel=r"$V_{\text{noise}}$", ylabel=r"$V_{\text{light}}$", center=[-3.0, -0.3, 0])
        ax = A.ax
        cells = VGroup()
        step = g[1] - g[0]
        vmax = S.max()
        for i in range(0, len(g), 2):
            for j in range(0, len(g), 2):
                v = S[i, j] / vmax
                col = interpolate_color(ManimColor("#0E3B2E"), ManimColor("#05070B"), min(1.0, v * 3))
                r = Rectangle(width=ax.c2p(g[j] + 2 * step, 0)[0] - ax.c2p(g[j], 0)[0],
                              height=ax.c2p(0, g[i] + 2 * step)[1] - ax.c2p(0, g[i])[1], stroke_width=0,
                              fill_color=col, fill_opacity=1)
                r.move_to(ax.c2p(g[j] + step, g[i] + step))
                cells.add(r)
        valley = Line(ax.c2p(-0.15, 1.15), ax.c2p(1.15, -0.15), color=CR, stroke_width=3)
        vl = label(r"zero error: \ $V_{\text{noise}} + V_{\text{light}} = 1$", font_size=20, color=CR)
        vl.move_to(ax.c2p(0.62, 0.95))
        pb = d["path_block"]
        pc = d["path_ctrl"]
        dots_b = VGroup(*[Dot(ax.c2p(a, b), radius=0.05, color=CUE_A) for a, b in pb[::3]])
        dots_c = VGroup(*[Dot(ax.c2p(a, b), radius=0.05, color=CS) for a, b in pc[::2]])
        rows = rows_of([
            (r"shaded by the error of a noise-and-light trial; \ the green line is where it vanishes", WHITE),
            (r"control rats start at the origin: \ the gradient points along the diagonal, \ and both cues gain", CS),
            (r"the blocking rats start at $(1, 0)$: \ already on the line, \ no gradient, \ and the light stays at "
             r"zero", CUE_A),
            (r"the rule predicts blocking, \ and Kamin's control, \ without being told about either", YOU),
        ], 5.6, 25, 0.34).move_to([3.5, -0.2, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ phase 2 of Kamin's design under Rescorla-Wagner")
        with self.voiceover(
            "Here is blocking, in pictures. <bookmark mark='a'/> On a trial with both the noise and the light, the "
            "error depends on the two strengths. The surface is shaded by that error, and it's zero all along the "
            "line where the two strengths add up to one. <bookmark mark='b'/> The control rats start at the origin, "
            "knowing nothing. The gradient points straight along the diagonal, so both cues gain strength equally, "
            "and they meet the line at a half each. <bookmark mark='c'/> The blocking rats start at one comma zero: "
            "the noise already predicts the shock fully. They're already on the line. There's no error, no gradient, "
            "and the light never leaves zero. <bookmark mark='d'/> Nobody told the rule about blocking. It falls out "
            "of the sum: cues share one prediction, so a cue gains strength only by reducing an error that something "
            "else has not already removed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cells), FadeIn(A))
            vo.wait_until("a")
            self.play(Create(valley), FadeIn(vl), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in dots_c], lag_ratio=0.2), FadeIn(rows[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(p) for p in dots_b], lag_ratio=0.2), FadeIn(rows[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
