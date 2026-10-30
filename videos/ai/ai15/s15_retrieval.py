from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai15.common import HIST, K, MONO, PART, Q, RET, V, axes, curve, fmt_int, load, said

LM_C, KNN_C = C.NEURAL, RET


class Retrieval(VoiceoverScene):
    def construct(self):
        self.card()
        self.dense()
        self.knnlm()
        self.measured()
        self.where()
        self.board()

    def card(self):
        card = chapter_card(14, r"Retrieval as memory", r"Can a memory live outside the model?", part=PART)
        with self.voiceover("Chapter fourteen. Retrieval as memory."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def dense(self):
        g = np.random.default_rng(5)
        pts = g.normal(size=(40, 2)) * 1.3
        q = np.array([0.9, 0.6])
        d = np.linalg.norm(pts - q, axis=1)
        near = np.argsort(d)[:4]
        ax = Axes(x_range=[-4, 4, 1], y_range=[-3, 3, 1], x_length=6.0, y_length=4.5, tips=False,
                  axis_config={"stroke_width": 0}).move_to([-3.2, -0.5, 0])
        docs = VGroup(*[Dot(ax.c2p(*p), radius=0.06, color=GREY_B) for p in pts])
        qd = Star(n=5, outer_radius=0.14, color=Q, fill_opacity=1).move_to(ax.c2p(*q))
        links = VGroup(*[Line(ax.c2p(*q), ax.c2p(*pts[i]), color=RET, stroke_width=2) for i in near])
        dl = label(r"passages, \ each an embedding", font_size=20, color=GREY_B).next_to(ax, DOWN, buff=0.05)
        ql = label(r"the question", font_size=20, color=Q).next_to(qd, UR, buff=0.05)
        tag = note(r"schematic: \ in two of the hundreds of dimensions", font_size=16).to_corner(DL, buff=0.25)
        d_card = definition_card(r"retrieval-augmented generation", r"embed the question; \ find the nearest passages in "
                                 r"a large store \ (a dot product, \ over millions); \ put them in the context, \ and "
                                 r"generate", color=RET, width=6.0, font_size=21).move_to([3.6, 1.2, 0])
        hist = VGroup(
            label(r"2020: \ DPR \ (Karpukhin et al.): \ two encoders, \\ trained so questions land near their answers",
                  font_size=18, color=HIST),
            label(r"2020: \ REALM \ (Guu et al.): \ the retriever trained with the language model", font_size=18, color=HIST),
            label(r"2020: \ RAG \ (Lewis et al.): \ retrieve, \ then generate", font_size=18, color=HIST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        if hist.width > 6.4:
            hist.width = 6.4
        hist.move_to([3.4, -1.7, 0])
        with self.voiceover(
            "Every memory so far lives inside the model. The other way is to keep memory outside it, as a library. "
            "<bookmark mark='a'/> Turn every passage of a large collection into a vector, an embedding, and the "
            "question into another; the passages nearest the question are the ones to read. "
            "<bookmark mark='b'/> In 2020 Vladimir Karpukhin and colleagues trained two encoders so that questions "
            "land near their answers, dense passage retrieval; REALM trained the retriever together with the "
            "language model; and Patrick Lewis and colleagues named the recipe: retrieval-augmented generation, "
            "find the passages, put them in the context, and generate. <bookmark mark='c'/> It's how most chat "
            "assistants search documents today, and the memory never has to fit in a context window."
        ) as vo:
            self.play(FadeIn(docs), FadeIn(dl), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(qd), FadeIn(ql))
            self.play(LaggedStart(*[Create(l_) for l_ in links], lag_ratio=0.3),
                      *[docs[i].animate.set_color(RET).scale(1.6) for i in near])
            vo.wait_until("b")
            self.play(FadeIn(d_card, shift=UP * 0.1))
            self.play(LaggedStart(*[FadeIn(h_, shift=RIGHT * 0.1) for h_ in hist], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(Indicate(d_card, color=RET, scale_factor=1.02))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def knnlm(self):
        kn = load("knn")
        ex = kn["example"]
        colors = {r"\lambda": RET, r"p_{\text{kNN}}": KNN_C, r"p_{\text{LM}}": LM_C}
        f1 = cmath(r"p(w \mid \text{context})", "=", r"\lambda", r"\, p_{\text{kNN}}(w)", "+", r"(1 - \lambda)",
                   r"\, p_{\text{LM}}(w)", colors=colors, font_size=36).to_edge(UP, buff=0.4)
        f2 = cmath(r"p_{\text{kNN}}(w)", r"\;\propto\;", r"\sum_{\text{neighbours with next token } w}", r"e^{-\|h - h_i\|^2 / T}",
                   colors=colors, font_size=30).next_to(f1, DOWN, buff=0.3)
        ctx = said(ex["context"] + " ...", chars=48, font_size=19, max_lines=2, box_color=Q)
        cl = label(r"from the passage: \ the context so far", font_size=18, color=Q)
        cg = VGroup(cl, ctx).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([-3.6, -0.9, 0])
        neigh = VGroup(*[VGroup(data_text(repr(w)[1:-1] or " ", font=MONO, font_size=20, color=KNN_C),).arrange(RIGHT)
                         for w in ex["neighbours"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        nl = label(r"the next tokens of its \\ 8 nearest stored states", font_size=18, color=KNN_C)
        ng = VGroup(nl, neigh).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([1.4, -1.2, 0])
        tg = VGroup(label(r"the true next token:", font_size=18, color=GREY_A),
                    data_text(repr(ex["target"])[1:-1], font=MONO, font_size=22, color=WHITE),
                    label(rf"the model alone: \ ${100 * float(ex['p_lm']):.2g}\%$", font_size=18, color=LM_C),
                    label(rf"the neighbours' vote: \ ${100 * float(ex['p_knn']):.0f}\%$", font_size=18, color=KNN_C))
        tg.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([4.8, -1.0, 0])
        n_all = int(kn["n_all"])
        cite_ = cite(r"U.~Khandelwal, O.~Levy, D.~Jurafsky, L.~Zettlemoyer \& M.~Lewis, \textit{Generalization through "
                     r"Memorization: Nearest Neighbor Language Models} (2020)", corner=DR, font_size=16)
        with self.voiceover(
            "A language model can retrieve too, one token at a time. Urvashi Khandelwal and colleagues, in 2020, "
            "stored every token of the training text as a pair: the model's hidden state just before it, and the "
            "token itself. <bookmark mark='a'/> At test time, find the stored states nearest to the current one, "
            "and let their next tokens vote, weighted by closeness. Mix the vote with the model's own prediction, "
            "a share lambda to the memory. With no extra training, it took 2.9 points off the perplexity of the "
            "best model of the day on Wikipedia text. <bookmark mark='b'/> We built one for the series' model: "
            f"all {n_all / 1e6:.1f} million tokens of the thirty novels, as hidden states. <bookmark mark='c'/> Here "
            "is the token where it helps most in the scoreboard's passage. The model alone gives the right next "
            f"token {100 * float(ex['p_lm']):.1f} percent; <bookmark mark='d'/> the nearest stored states, from "
            f"places in the novels that looked the same, vote {100 * float(ex['p_knn']):.0f} percent for it."
        ) as vo:
            self.play(Write(f1), FadeIn(cite_), FadeIn(cg), FadeIn(tg[0]), FadeIn(tg[1]))
            vo.wait_until("a")
            self.play(Write(f2))
            vo.wait_until("b")
            self.play(Indicate(cg, color=Q, scale_factor=1.03))
            vo.wait_until("c")
            self.play(FadeIn(tg[2]))
            vo.wait_until("d")
            self.play(FadeIn(nl), LaggedStart(*[FadeIn(n_, shift=LEFT * 0.1) for n_ in neigh], lag_ratio=0.15), FadeIn(tg[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measured(self):
        kn = load("knn")
        snaps = [int(s_) for s_ in kn["snaps"]]
        lams = np.asarray(kn["lams"], float)
        base = float(kn["base_bits"])
        full = kn[f"snap_{snaps[-1]}"]
        curve_full = np.asarray(full["lam_curve"])
        lo = math.floor(min(curve_full.min(), base) * 50 - 1) / 50
        hi = math.ceil(max(curve_full.max(), base) * 50 + 1) / 50
        g1 = axes([0, lams[-1]], [lo, hi], x_length=5.4, y_length=3.6, xlabel=r"$\lambda$, \ the memory's share",
                  ylabel=r"bits per character, \ the passage", xticks=[0, 0.25, 0.5], yticks=[lo, hi],
                  center=[-3.5, -0.3, 0], yfmt=lambda v: f"{v:.2f}")
        ax1 = g1.ax
        c1 = curve(ax1, lams, curve_full, KNN_C, 3.5)
        lam = float(full["lam"])
        mark = DashedLine(ax1.c2p(lam, lo), ax1.c2p(lam, hi), dash_length=0.06, color=WHITE, stroke_width=1.5)
        ml = label(rf"$\lambda = {lam:g}$: \\ chosen on \\ held-out novels", font_size=16, color=WHITE).next_to(ax1.c2p(lam, (lo + hi) / 2), RIGHT, buff=0.12)
        keys = np.array([kn[f"snap_{s_}"]["keys"] for s_ in snaps], float)
        bits = np.array([kn[f"snap_{s_}"]["bits"] for s_ in snaps])
        lk = np.log10(keys)
        lo2 = math.floor(min(bits.min(), base) * 50 - 1) / 50
        g2 = axes([lk[0] - 0.2, lk[-1] + 0.2], [lo2, base + 0.01], x_length=5.0, y_length=3.6, xlabel=r"stored states",
                  ylabel=r"bits per character", xticks=list(lk), yticks=[lo2, base], center=[3.5, -0.3, 0],
                  xfmt=lambda v: f"{10 ** v / 1e6:.2g}" + r"\,\text{M}", yfmt=lambda v: f"{v:.2f}", font_size=16)
        ax2 = g2.ax
        c2 = curve(ax2, lk, bits, KNN_C, 3.5)
        d2 = VGroup(*[Dot(ax2.c2p(x, y), radius=0.06, color=KNN_C) for x, y in zip(lk, bits)])
        bl = DashedLine(ax2.c2p(lk[0] - 0.2, base), ax2.c2p(lk[-1] + 0.2, base), dash_length=0.06, color=LM_C, stroke_width=2)
        bll = label(r"the model alone", font_size=16, color=LM_C).next_to(bl, DOWN, buff=0.05).align_to(bl, RIGHT)
        gain = base - float(full["bits"])
        rel = gain / base
        v1 = (f"On the passage, the model alone scores {base:.3f} bits per character. With the memory of the "
              f"novels, mixed in at lambda {lam:g}, chosen on held-out novel text and never on the passage, it scores "
              f"{float(full['bits']):.3f}: {gain:.3f} bits less, {100 * rel:.1f} percent. " if gain > 0.002 else
              f"On the passage, the model alone scores {base:.3f} bits per character, and with the memory "
              f"{float(full['bits']):.3f}: no real gain. ")
        lam0 = float(kn[f"snap_{snaps[0]}"]["lam"])
        grows = bits[-1] < bits[0] - 0.002
        v2 = (f"And it takes a big memory: with {keys[0] / 1e6:.2f} million stored states, the best share for the vote "
              f"is {lam0:g}, and the score {bits[0]:.3f}; only with all {keys[-1] / 1e6:.1f} million does it reach "
              f"{bits[-1]:.3f}." if grows else
              f"A bigger memory hardly helps here: {bits[0]:.3f} with {keys[0] / 1e6:.2f} million stored states, "
              f"{bits[-1]:.3f} with {keys[-1] / 1e6:.1f} million.")
        with self.voiceover(
            "How much does it help? <bookmark mark='a'/> " + v1 + "<bookmark mark='b'/> " + v2 + " The passage, "
            "chapter two of The Maltese Falcon, is not among the thirty novels, so the memory can't simply recall "
            "it: it helps with what novels share."
        ) as vo:
            self.play(FadeIn(g1))
            vo.wait_until("a")
            self.play(Create(c1), run_time=1.5)
            self.play(Create(mark), FadeIn(ml))
            vo.wait_until("b")
            self.play(FadeIn(g2), Create(bl), FadeIn(bll))
            self.play(Create(c2), FadeIn(d2), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def where(self):
        kn, sc = load("knn"), load("selfcache")
        best = kn["best_tokens"][:10]
        head = label(r"where the memories help", font_size=34).to_edge(UP, buff=0.35)
        tl = label(r"the novels: \ tokens of the passage it helps most \ (bits saved)", font_size=20, color=KNN_C)
        toks = VGroup(*[VGroup(data_text(repr(w)[1:-1] or " ", font=MONO, font_size=20, color=WHITE),
                               MathTex(f"{float(gn):.1f}", font_size=20, color=KNN_C)).arrange(RIGHT, buff=0.2)
                        for w, gn in best]).arrange_in_grid(rows=5, cols=2, buff=(0.6, 0.15), cell_alignment=LEFT)
        left = VGroup(tl, toks).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([-3.4, -0.3, 0])
        base = float(sc["base_bits"])
        gain = base - float(sc["bits"])
        hc = history_card(2017, r"a continuous cache \ (Grave, Joulin \& Usunier)", r"the same vote, \ over the text read "
                          r"so far", color=HIST, width=5.0, font_size=19)
        res = label(rf"the passage's own past, \ beyond the $256$-token window: \\ ${base:.3f}$ $\rightarrow$ "
                    rf"${float(sc['bits']):.3f}$ bits per character \ ($\lambda = {float(sc['lam']):g}$)", font_size=20, color=RET)
        right = VGroup(hc, res).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.4, -0.3, 0])
        names = [w.strip() for w, _ in best if w.strip()[:1].isupper()]
        v = (f"Many are names and capitals, like {names[0]}: the memory has seen how novels use them. " if names else
             "Mostly they finish a word that has already begun, like the example's: completions the novels have seen "
             "many times. ")
        v2 = (f"Edouard Grave and colleagues had done the same in 2017 with the text read so far, a continuous cache. "
              f"For our passage, which runs far past the model's 256-token window, a memory of its own earlier hidden "
              f"states takes the score from {base:.3f} to {float(sc['bits']):.3f}: names that appeared a page "
              "earlier come back." if gain > 0.005 else
              f"Edouard Grave and colleagues had done the same in 2017 with the text read so far, a continuous cache; "
              f"for our passage it gives {float(sc['bits']):.3f} against {base:.3f}, little.")
        with self.voiceover(
            "Where does the memory of the novels help? <bookmark mark='a'/> Here are the tokens of the passage "
            "where it saves the most bits. " + v + "<bookmark mark='b'/> " + v2
        ) as vo:
            self.play(FadeIn(head), FadeIn(tl), LaggedStart(*[FadeIn(t_) for t_ in toks], lag_ratio=0.1))
            vo.wait_until("a")
            self.play(Indicate(toks, color=KNN_C, scale_factor=1.03))
            vo.wait_until("b")
            self.play(FadeIn(hc, shift=UP * 0.1))
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def board(self):
        S = load("scoreboard")
        rows = [dict(r) for r in S["rows"]]
        mine = [i for i, r in enumerate(rows) if r.get("part") == 15]
        board = scoreboard(rows, highlight=tuple(mine), max_bits=4.0, row_h=0.44, font_size=19, bar_width=5.6,
                           label_width=5.0)
        board.scale_to_fit_height(min(board.height, 5.6))
        if board.width > 9.4:
            board.scale_to_fit_width(9.4)
        board.move_to([-1.9, -0.5, 0])
        head = label(r"The scoreboard: \ \textit{The Maltese Falcon}, \ chapter 2", font_size=30).to_edge(UP, buff=0.3)
        hc = history_card(2021, r"RETRO \ (Borgeaud et al., DeepMind)", r"retrieval from $2$ trillion tokens; \ about "
                          r"GPT-3's quality \ with $25\times$ fewer parameters", color=HIST, width=3.5, font_size=16)
        hc.move_to([5.2, 0.6, 0])
        by = {r.get("key"): r for r in rows}
        tf, hy, kn, sc = by["tf15"], by["hybrid15"], by["knn"], by["selfcache"]
        base = next(r for r in rows if r["label"] == "the series' model")
        rp = base["params"] / hy["params"]
        rt = float(S["base_tokens"]) / float(S["ours_tokens"])
        v = (f"Our small hybrid and transformer, with {rp:.0f} times fewer weights than the series' model and {rt:.0f} "
             f"times fewer training tokens, land at {hy['bits']:.2f} and {tf['bits']:.2f}. The series' model with its memory of the "
             f"novels reaches {kn['bits']:.3f}, and with a memory of the passage so far, {sc['bits']:.3f}, against "
             f"{base['bits']:.3f} alone.")
        with self.voiceover(
            "Retrieval scales too: in 2021 DeepMind's RETRO looked up chunks of a two-trillion-token library and "
            "came close to GPT-3 on the Pile with a twenty-fifth of the parameters. <bookmark mark='a'/> And here is the scoreboard. "
            + v
        ) as vo:
            self.play(FadeIn(head), FadeIn(hc), FadeIn(board))
            vo.wait_until("a")
            for i in mine:
                self.play(Indicate(board.rows[i], color=C.BITS, scale_factor=1.02), run_time=0.6)
        self.wait(0.3)
        self.clear_scene()
