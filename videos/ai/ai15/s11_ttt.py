from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai15.common import (ADD, DECAY, DELTA, GATED, K, PART, SSM_C, STATE, V, axes, band, curve, load,
                                   ttt_picture, ttt_step)

LIN_C, MLP_C = DELTA, C.NEURAL


class TTT(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.toy()
        self.titans()
        self.table()

    def card(self):
        card = chapter_card(10, r"A memory that learns", r"What if the memory were a whole network?", part=PART)
        with self.voiceover("Chapter ten. A memory that learns."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def idea(self):
        colors = {r"W_t": STATE, r"W_{t-1}": STATE, r"\eta": DELTA, r"\ell": C.LOSS, r"x_t": K}
        f1 = cmath(r"W_t", "=", r"W_{t-1}", "-", r"\eta", r"\,\nabla", r"\ell", r"(W_{t-1};\, x_t)", colors=colors,
                   font_size=40).to_edge(UP, buff=0.5)
        f2 = cmath(r"\ell", r"(W; x_t)", "=", r"\big\|\, f_W(\theta_K x_t) - \theta_V x_t \big\|^2", colors=colors,
                   font_size=34).next_to(f1, DOWN, buff=0.35)
        l2 = label(r"a self-supervised loss on the token being read: \ rebuild one view of it from another", font_size=20,
                   color=GREY_A).next_to(f2, DOWN, buff=0.15)
        ttt = gloss(r"test-time training", r"the hidden state is a model's weights; \\ reading a token is one step of "
                    r"training on it", ttt_picture(), width=5.6, color=STATE).move_to([-3.2, -1.6, 0])
        tp = ttt[1][-1]
        kinds = VGroup(label(r"$f_W(k) = W k$: \ TTT-Linear \ (the delta rule)", font_size=22, color=LIN_C),
                       label(r"$f_W$ a two-layer network: \ TTT-MLP", font_size=22, color=MLP_C))
        kinds.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.3, -1.1, 0])
        res = label(r"reported: \ Mamba stops improving past $16$k tokens of context; \\ the TTT layers keep going "
                    r"\ ($125$M--$1.3$B parameters)", font_size=18, color=GREY_B).next_to(kinds, DOWN, buff=0.4).align_to(kinds, LEFT)
        cite_ = cite(r"Y.~Sun, X.~Li, K.~Dalal et al., \textit{Learning to (Learn at Test Time): RNNs with Expressive "
                     r"Hidden States} (2024)", corner=DR, font_size=17)
        with self.voiceover(
            "Chapter five ended with a thought: the delta rule is one step of gradient descent, so the memory is a "
            "model, trained on the text as it is read. Yu Sun and colleagues took that literally in 2024. "
            "<bookmark mark='a'/> The hidden state is the weights W of a small model, and reading a token is one "
            "training step on a loss made from that token: rebuild one learned view of it from another. "
            "<bookmark mark='b'/> If the model is linear, that is the delta rule again: TTT-Linear. "
            "<bookmark mark='c'/> But it can be anything trainable, a two-layer network, TTT-MLP, whose weights are "
            "a richer memory than one matrix. <bookmark mark='d'/> They reported that, from 125 million to 1.3 "
            "billion parameters, Mamba stopped improving with more than sixteen thousand tokens of context, and "
            "their layers kept improving."
        ) as vo:
            self.play(Write(f1), FadeIn(cite_))
            vo.wait_until("a")
            self.play(Write(f2), FadeIn(l2), FadeIn(ttt, shift=UP * 0.1))
            for k_ in range(1, len(tp[0]) + 1):
                w_, t_ = ttt_step(tp, k_)
                self.play(Transform(tp[2][0], w_), Transform(tp[0], t_), run_time=0.35)
            vo.wait_until("b")
            self.play(FadeIn(kinds[0], shift=RIGHT * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(kinds[1], shift=RIGHT * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def toy(self):
        t = load("ttt")
        every = int(t["every"])
        n_read = int(t["n_read"])
        El, Em = np.asarray(t["err_linear"]), np.asarray(t["err_mlp"])
        xs = np.arange(1, El.shape[1] + 1) * every
        top = 1.2
        g = axes([0, n_read], [0, top], x_length=7.4, y_length=4.0, xlabel=r"pairs read",
                 ylabel=r"error on fresh keys of the same rule \ (relative)", xticks=[0, 64, 128, 192, 256],
                 yticks=[0, 0.5, 1.0], center=[-1.9, -0.5, 0])
        ax = g.ax
        bands, lines = VGroup(), VGroup()
        for E, c_ in ((El, LIN_C), (Em, MLP_C)):
            q1, med, q3 = (np.quantile(np.minimum(E, top), q, axis=0) for q in (0.25, 0.5, 0.75))
            bands.add(band(ax, xs, q1, q3, c_, 0.18))
            lines.add(curve(ax, xs, med, c_, 4))
        pl, pm = int(t["params_linear"]), int(t["params_mlp"])
        leg = legend([(LIN_C, rf"linear memory, \ ${pl}$ numbers \ (TTT-Linear)"),
                      (MLP_C, rf"two-layer memory, \ ${pm}$ numbers \ (TTT-MLP)")], font_size=18).move_to([4.2, 1.9, 0])
        bl = note(r"median of $32$ sequences; \ band: \ the middle half; \ each step size chosen on $16$ other sequences",
                  font_size=16).to_edge(DOWN, buff=0.2)
        task = label(rf"each sequence: \ its own hidden rule $v = f(k)$, \ a random small network, \ keys of ${int(t['d'])}$ "
                     r"numbers", font_size=20, color=GREY_A).to_edge(UP, buff=0.35)
        el, em = float(np.median(El[:, -1])), float(np.median(Em[:, -1]))
        verdict = (f"The linear memory levels off at {el:.2f}: the best a matrix can do for a curved rule. The "
                   f"two-layer memory keeps learning, down to {em:.2f}: a richer memory, at {pm // pl} times the numbers."
                   if em < 0.8 * el else
                   f"The two-layer memory ends a little lower, {em:.2f} against {el:.2f} for the matrix: a richer memory "
                   f"helps, modestly here, at {pm // pl} times the numbers." if em < 0.95 * el else
                   f"The two-layer memory does no better here: {em:.2f} against {el:.2f} for the matrix, at {pm // pl} "
                   "times the numbers.")
        with self.voiceover(
            "We can test that on a toy. Each sequence has its own hidden rule, a small random network that turns a "
            "key into a value, and the memory reads one pair at a time, taking one gradient step on each. "
            "<bookmark mark='a'/> After every sixteen pairs we ask it about keys it has never seen, under the same "
            "rule. It isn't looking anything up: it has to have learned the rule. <bookmark mark='b'/> " + verdict
        ) as vo:
            self.play(FadeIn(task), FadeIn(g), FadeIn(bl))
            self.play(FadeIn(leg[0]), FadeIn(bands[0]), Create(lines[0]), run_time=2.0)
            vo.wait_until("a")
            self.play(Indicate(lines[0], color=WHITE, scale_factor=1.0))
            vo.wait_until("b")
            self.play(FadeIn(leg[1]), FadeIn(bands[1]), Create(lines[1]), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def titans(self):
        t = load("ttt")
        sw = int(t["switch"])
        Sp, St = np.asarray(t["switch_surprise_plain"]), np.asarray(t["switch_surprise_titans"])
        Ep, Et = np.asarray(t["switch_err_plain"]), np.asarray(t["switch_err_titans"])
        n = Sp.shape[1]
        sp, st = np.median(Sp, 0), np.median(St, 0)
        ep, et = np.median(Ep, 0), np.median(Et, 0)

        def smooth(x, k=5):
            return np.convolve(x, np.ones(k) / k, mode="same")

        sp, st = smooth(sp), smooth(st)
        top_s = float(max(sp.max(), st.max())) * 1.1
        g1 = axes([0, n], [0, top_s], x_length=5.6, y_length=2.1, ylabel=r"surprise: \ $\|\nabla \ell\|$",
                  center=[-3.4, 1.55, 0])
        g2 = axes([0, n], [0, 1.2], x_length=5.6, y_length=2.1, xlabel=r"pairs read",
                  ylabel=r"error on the current rule", yticks=[0, 1], center=[-3.4, -1.75, 0])
        for gg, yt in ((g1, top_s), (g2, 1.2)):
            gg.add(DashedLine(gg.ax.c2p(sw, 0), gg.ax.c2p(sw, yt), dash_length=0.06, color=GREY_B, stroke_width=1.5))
        xs = np.arange(n)
        c_s = VGroup(curve(g1.ax, xs, sp, GREY_B, 2.5), curve(g1.ax, xs, st, SSM_C, 3))
        c_e = VGroup(curve(g2.ax, xs, np.minimum(ep, 1.2), GREY_B, 2.5), curve(g2.ax, xs, np.minimum(et, 1.2), SSM_C, 3))
        sl = label(r"the rule changes", font_size=16, color=GREY_B).next_to(g1.ax.c2p(sw, top_s), UP, buff=0.05)
        colors = {r"S_t": SSM_C, r"S_{t-1}": SSM_C, r"M_t": STATE, r"M_{t-1}": STATE, r"\eta": DELTA, r"\theta": DELTA,
                  r"\alpha": DECAY}
        f1 = cmath(r"S_t", "=", r"\eta\, S_{t-1}", "-", r"\theta\, \nabla \ell(M_{t-1}; x_t)", colors=colors, font_size=30)
        f2 = cmath(r"M_t", "=", r"(1 - \alpha)\, M_{t-1}", "+", r"S_t", colors=colors, font_size=30)
        fs = VGroup(f1, f2).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.5, 2.1, 0])
        l1 = label(r"surprise, with momentum: \ past surprise carries on", font_size=17, color=SSM_C).next_to(f1, DOWN, buff=0.08)
        l1.align_to(f1, LEFT)
        l2 = label(r"a forgetting gate $\alpha$: \ weight decay on the memory", font_size=17, color=DECAY).next_to(f2, DOWN, buff=0.08)
        l2.align_to(f2, LEFT)
        leg = legend([(GREY_B, r"one gradient step per pair"), (SSM_C, r"with momentum and forgetting \ (Titans)")],
                     font_size=17).move_to([3.4, -0.25, 0])
        after = slice(sw + 8, min(sw + 40, n))
        ap, at_ = float(np.mean(ep[after])), float(np.mean(et[after]))
        hc = history_card(2025, r"Titans", r"Behrouz, Zhong \& Mirrokni: \ a deep neural memory beside attention; \ reported "
                          r"beyond $2$ million tokens", color=SSM_C, width=4.4, font_size=17).move_to([3.4, -2.1, 0])
        verdict = (f"In the thirty-two pairs after the change, momentum and forgetting adapt faster: an error of "
                   f"{at_:.2f} on average, against {ap:.2f}." if at_ < ap - 0.03 else
                   f"In the thirty-two pairs after the change, the two adapt at about the same rate: {at_:.2f} against "
                   f"{ap:.2f}: in this toy, momentum and forgetting don't help.")
        with self.voiceover(
            "Ali Behrouz, Peilin Zhong and Vahab Mirrokni at Google built the idea into Titans, at the turn of 2025. "
            "Their memory is a small deep network beside a window of ordinary attention, and they call the "
            "gradient surprise: <bookmark mark='a'/> a token the memory gets badly wrong produces a large gradient, "
            "and gets written in hard. <bookmark mark='b'/> They add momentum, so a surprise keeps being written for "
            "a few steps after, and a forgetting gate, a weight decay that clears old memories out. "
            "<bookmark mark='c'/> Here is our toy again, with the hidden rule swapped for a new one halfway. The "
            "surprise jumps when the rule changes. <bookmark mark='d'/> " + verdict + " <bookmark mark='e'/> The "
            "paper reports needle tests passed beyond two million tokens; we can't check that here."
        ) as vo:
            self.play(Write(f1), FadeIn(l1), FadeIn(g1), FadeIn(g2))
            vo.wait_until("a")
            self.play(Create(c_s[0]), Create(c_s[1]), FadeIn(sl), run_time=2.0)
            vo.wait_until("b")
            self.play(Write(f2), FadeIn(l2))
            vo.wait_until("c")
            self.play(FadeIn(leg), Create(c_e[0]), Create(c_e[1]), run_time=2.0)
            vo.wait_until("d")
            self.play(Indicate(c_e[1], color=WHITE, scale_factor=1.0))
            vo.wait_until("e")
            self.play(FadeIn(hc))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        head = label(r"Every memory in this part is a learner", font_size=34).to_edge(UP, buff=0.4)
        rows = [
            (r"linear attention", r"$-\langle S k, v\rangle$", r"one gradient step", ADD),
            (r"decay \ (Mamba-2, \ GLA)", r"$-\langle S k, v\rangle + \tfrac{\lambda}{2}\|S\|^2$", r"a step, \ and weight decay", DECAY),
            (r"delta rule \ (DeltaNet, \ TTT-Linear)", r"$\tfrac12 \|S k - v\|^2$", r"one gradient step", DELTA),
            (r"gated delta \ (Qwen3-Next, \ Kimi)", r"$\tfrac12 \|S k - v\|^2$", r"a step, \ and weight decay", GATED),
            (r"Titans", r"$\tfrac12 \|M(k) - v\|^2$", r"momentum, \ weight decay; \ a deep $M$", SSM_C),
            (r"softmax attention", r"--", r"no training: \ a kernel regression \ over every pair kept", C.ATTN),
        ]
        hdr = VGroup(label(r"memory", font_size=20, color=GREY_B), label(r"loss it lowers, \ each token", font_size=20, color=GREY_B),
                     label(r"how it learns", font_size=20, color=GREY_B))
        xs = [-4.3, 0.2, 4.2]
        for h_, x in zip(hdr, xs):
            h_.move_to([x, 2.3, 0])
        tbl = VGroup()
        for i, (a, b, c, col) in enumerate(rows):
            y = 1.6 - i * 0.68
            tbl.add(VGroup(label(a, font_size=21, color=col).move_to([xs[0], y, 0]), label(b, font_size=22).move_to([xs[1], y, 0]),
                           label(c, font_size=20, color=GREY_A).move_to([xs[2], y, 0])))
        line = Line([-6.6, 2.0, 0], [6.6, 2.0, 0], color=GREY_D, stroke_width=1)
        cite_ = cite(r"after S.~Yang's notes on linear attention, \ and K.~A.~Wang, J.~Shi \& E.~B.~Fox, \textit{Test-time "
                     r"regression} (2025)", corner=DR, font_size=16)
        with self.voiceover(
            "Step back, and every memory in this part is a learner. <bookmark mark='a'/> Linear attention takes a "
            "gradient step on a loss that rewards the memory for agreeing with the value: it can only add. Decay "
            "adds weight decay. <bookmark mark='b'/> The delta rule steps on the squared error, so it corrects; the "
            "gated delta rule adds weight decay to that. <bookmark mark='c'/> Titans and TTT make the memory a deeper "
            "model and use a better optimizer. <bookmark mark='d'/> And softmax attention trains nothing: it keeps "
            "every pair and answers with a weighted average of their values, Part 13's kernel regression, paying "
            "for it with a growing cache. Which of these can actually look things up? "
            "That's the next chapter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr), Create(line), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(tbl[0], shift=RIGHT * 0.1), FadeIn(tbl[1], shift=RIGHT * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(tbl[2], shift=RIGHT * 0.1), FadeIn(tbl[3], shift=RIGHT * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(tbl[4], shift=RIGHT * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(tbl[5], shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()
