from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai1.common import MONO, load, plain_axes


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.next_time()
        self.references()

    # ------------------------------------------------------------------
    def recap(self):
        items = [
            (r"a guess is a probability distribution; \ the chain rule scores a whole text", C.TRUE_P),
            (r"surprise $= \log_2 \frac1p$ bits: \ the only measure that adds up", C.SURPRISE),
            (r"entropy $=$ average surprise; \ at most $\log_2 K$ (Jensen)", C.ENTROPY),
            (r"prefix codes obey Kraft; \ no code beats the entropy; \ Huffman gets within a bit", C.BITS),
            (r"cross-entropy $= H(p) + D_{\mathrm{KL}}(p \,\|\, q)$; \ $D_{\mathrm{KL}} \ge 0$; \ it isn't symmetric",
             C.KL),
            (r"arithmetic coding: \ any predictor is a compressor, and back", C.INTERVAL),
            (r"counting fits the books but not new text: \ generalization", C.COUNTING),
            (r"Shannon's game: \ people need about $1$ bit per letter", C.HUMAN),
            (r"maximum likelihood $=$ minimum cross-entropy; \ the gradient is $q - \hat p$", C.MODEL_Q),
            (r"to guess well: \ knowledge, and a long memory", C.CONTEXT),
            (r"the scoreboard: \ $8$ bits $\to$ $2.32$ (counting) $\to$ $0.87$ (Qwen3-4B)", WHITE),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\; {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.17).move_to(DOWN * 0.2)
        head = label(r"Part 1, in eleven lines", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. We wrote guesses down as probability distributions, and the chain rule turned them "
            "into a score for a whole text. We found that there's only one sensible measure of surprise, and that "
            "entropy, the average surprise, is the speed limit of compression. We met the price of a wrong model, "
            "the cross-entropy, and the divergence inside it. Arithmetic coding showed that predicting and "
            "compressing are the same thing. Counting models showed us generalization, by failing at it. And we "
            "derived the gradient that trains every language model: the guess, minus the truth."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"the chain rule: \ next-token prediction", [11, 16, 17]),
            (r"cross-entropy: \ the training loss", [8, 9, 10]),
            (r"forward and reverse $D_{\mathrm{KL}}$", [14, 17]),
            (r"prediction $=$ compression", [10, 20]),
            (r"memorizing vs.\ generalizing", [6, 7]),
            (r"mutual information, long memory", [11, 12]),
            (r"softmax, and its gradient $q - \hat p$", [3, 9]),
        ], font_size=24)
        with self.voiceover(
            "Almost everything here comes back. The chain rule is how language models generate text, and how "
            "reasoning models think out loud. Cross-entropy is the loss we'll be minimizing for the rest of the "
            "series. The two directions of the divergence return in diffusion models and in reinforcement learning. "
            "Compression returns when we study scaling, and when we look inside the models at the end."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        v = load("vectors")
        words = [w.strip() for w in v["words"]]
        cos = np.asarray(v["cos"])
        i = {w: k for k, w in enumerate(words)}
        assert abs(cos[i["dog"], i["puppy"]] - 0.621) < 0.001 and abs(cos[i["dog"], i["tobacco"]] - 0.229) < 0.001
        head = label(r"Next: \ Part 2, \ Vectors That Mean Things", font_size=40).to_edge(UP, buff=0.3)
        # cosine similarity grid of GPT-2's word vectors
        n, cell = len(words), 0.5
        x0, y0 = -6.2, 1.7
        grid = VGroup()
        for a in range(n):
            for b in range(n):
                c = float(cos[a, b])
                col = interpolate_color(ManimColor("#161C28"), ManimColor(C.TRUE_P), min(1.0, max(0.0, (c - 0.15) / 0.65)))
                sq = Square(cell, stroke_width=0.5, stroke_color=BACKGROUND, fill_color=col, fill_opacity=1)
                sq.move_to([x0 + 1.6 + (b + 0.5) * cell, y0 - (a + 0.5) * cell, 0])
                grid.add(sq)
        rl = VGroup(*[Text(w, font=MONO, font_size=16, color=GREY_A).next_to(grid[a * n], LEFT, buff=0.1)
                      for a, w in enumerate(words)])
        cl = VGroup(*[Text(w, font=MONO, font_size=16, color=GREY_A).rotate(PI / 3).next_to(grid[b], UP, buff=0.08)
                      for b, w in enumerate(words)])
        vals = VGroup(*[MathTex(f"{cos[a, b]:.2f}", font_size=15, color=WHITE).move_to(grid[a * n + b])
                        for a in range(n) for b in range(n) if a != b])
        gcap = label(r"GPT-2's own word vectors: \ cosine similarity", font_size=22, color=GREY_A)
        gcap.next_to(grid, DOWN, buff=0.3)
        # random directions: 3 dimensions versus 768
        ax = plain_axes([-1, 1, 0.5], [0, 1, 0.5], 5.2, 3.0).move_to([3.6, -0.2, 0])
        xl = VGroup(*[MathTex(t, font_size=20, color=GREY_B).next_to(ax.c2p(x, 0), DOWN, buff=0.1)
                      for t, x in (("-1", -1), ("0", 0), ("1", 1))])
        bars = VGroup()
        for dim, col, op in ((3, GREY_B, 0.5), (768, C.BITS, 0.9)):
            h = np.asarray(v[f"random{dim}"], float)
            h = h / h.max()
            w = 2 / len(h)
            for k, hv in enumerate(h):
                if hv <= 0:
                    continue
                x = -1 + (k + 0.5) * w
                bars.add(Rectangle(width=ax.x_length * w / 2 * 0.95, height=ax.y_length * hv * (0.5 if dim == 3 else 1),
                                   stroke_width=0, fill_color=col, fill_opacity=op)
                         .move_to(ax.c2p(x, 0), aligned_edge=DOWN))
        hl = VGroup(label(r"random directions in $3$ dimensions", font_size=20, color=GREY_B),
                    label(r"\ldots in $768$: \ almost all at right angles", font_size=20, color=C.BITS))
        hl.arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(ax, UP, buff=0.2)
        assert abs(v["sd768"] - 0.036) < 0.001
        with self.voiceover(
            "Next time: the problem that broke counting. A counting model can't tell that a dog and a puppy are "
            "alike. <bookmark mark='a'/> Neural models can, because they represent every word as a long list of "
            "numbers, a vector, and similar words get similar vectors. In GPT-2's own vectors, dog sits close to "
            "puppy, and far from tobacco. <bookmark mark='b'/> And high-dimensional space is strange: pick two "
            "random directions in 768 dimensions, and they're almost always at right angles. There's room for an "
            "enormous number of nearly separate meanings. Part two is the linear algebra and geometry behind that."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(grid), FadeIn(rl), FadeIn(cl), FadeIn(gcap), run_time=1.5)
            self.play(FadeIn(vals))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(xl), FadeIn(hl), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars],
                                                                       lag_ratio=0.01), run_time=2.0)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        books = [
            r"T.~M.~Cover \& J.~A.~Thomas, \textit{Elements of Information Theory}, 2nd ed.\ (2006), chapters 2, 5, 13",
            r"D.~J.~C.~MacKay, \textit{Information Theory, Inference, and Learning Algorithms} (2003), chapters 2, 4--6",
            r"C.~M.~Bishop \& H.~Bishop, \textit{Deep Learning: Foundations and Concepts} (2024), chapter 2",
        ]
        papers = [
            r"C.~E.~Shannon, \textit{A Mathematical Theory of Communication}, Bell Syst.~Tech.~J.\ (1948)",
            r"C.~E.~Shannon, \textit{Prediction and Entropy of Printed English}, Bell Syst.~Tech.~J.\ (1951)",
            r"L.~G.~Kraft (1949); \ D.~A.~Huffman, \textit{A Method for the Construction of Minimum-Redundancy Codes} (1952)",
            r"S.~Kullback \& R.~A.~Leibler, \textit{On Information and Sufficiency} (1951); \ R.~A.~Fisher (1922)",
            r"J.~Rissanen (1976); \ R.~Pasco (1976); \ I.~H.~Witten, R.~M.~Neal \& J.~G.~Cleary, \textit{Arithmetic "
            r"Coding for Data Compression} (1987)",
            r"T.~M.~Cover \& R.~C.~King, \textit{A Convergent Gambling Estimate of the Entropy of English} (1978)",
            r"H.~W.~Lin \& M.~Tegmark, \textit{Critical Behavior in Physics and Probabilistic Formal Languages} (2017)",
            r"G.~Del\'etang et al., \textit{Language Modeling Is Compression} (ICLR 2024)",
            r"A.~Radford et al., \textit{Language Models are Unsupervised Multitask Learners} (GPT-2, 2019); \ "
            r"Qwen Team, \textit{Qwen3 Technical Report} (2025)",
        ]
        card = reference_card(books, papers)
        data = note(r"Text: Project Gutenberg (30 novels; \textit{The Maltese Falcon}, eBook \#77600). \ Every "
                    r"number on screen is computed and checked; \ schematics and illustrations are labeled.",
                    font_size=20).to_edge(DOWN, buff=0.25)
        credit = note(rf"Animated with Manim Community; \ narrated by {narration_credit()}.", font_size=20)
        credit.next_to(data, UP, buff=0.1)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.15:
            card.shift(UP * (credit.get_top()[1] + 0.15 - card.get_bottom()[1]))
        with self.voiceover(
            "This part followed the first chapters of Cover and Thomas's Elements of Information Theory, and "
            "MacKay's Information Theory, Inference, and Learning Algorithms, both of which go much further. The "
            "papers are all worth reading, starting with Shannon's two. Thanks for watching, and see you in part two."
        ) as vo:
            self.play(LaggedStart(FadeIn(card), FadeIn(credit), FadeIn(data), lag_ratio=0.3), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)))
