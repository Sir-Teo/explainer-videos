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
        ax = Axes(x_range=[-4, 4, 1], y_range=[-3, 3, 1], x_length=7.0, y_length=5.4, tips=False,
                  axis_config={"stroke_width": 0}).move_to([-3.3, -0.2, 0])
        docs = VGroup(*[Dot(ax.c2p(*p), radius=0.08, color=GREY_B) for p in pts])
        qd = Star(n=5, outer_radius=0.18, color=Q, fill_opacity=1).move_to(ax.c2p(*q))
        links = VGroup(*[Line(ax.c2p(*q), ax.c2p(*pts[i]), color=RET, stroke_width=2) for i in near])
        dl = label(r"passages, \ each an embedding", font_size=24, color=GREY_B).next_to(ax, DOWN, buff=0.05)
        ql = label(r"the question", font_size=24, color=Q).next_to(ax, UP, buff=0.2)
        question_leader = Arrow(ql.get_bottom(), qd.get_top(), buff=0.12, color=Q, stroke_width=2,
                                max_tip_length_to_length_ratio=0.08)
        tag = note(r"二维欧氏距离示意；DPR用点积打分" if zh() else
                   r"2D Euclidean proximity sketch; \ DPR uses dot-product scores",
                   font_size=16).to_corner(DL, buff=0.25)
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
            "find the passages, put them in the context, and generate. <bookmark mark='c'/> An assistant can search "
            "a library larger than its context window, then read the selected passages within that window."
        ) as vo:
            self.play(FadeIn(docs), FadeIn(dl), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(qd), FadeIn(ql), GrowArrow(question_leader))
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
        cg = VGroup(cl, ctx).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        if cg.width > 4.3:
            cg.width = 4.3
        cg.move_to([-4.65, -0.9, 0])
        gg = np.random.default_rng(7)
        store = VGroup()
        for i_, w in enumerate(ex["neighbours"]):
            vals = gg.normal(size=8)
            strip = VGroup(*[Square(0.22, stroke_width=0.5, stroke_color=GREY_D, fill_opacity=0.9,
                                    fill_color=interpolate_color(BLUE_E if x < 0 else RED_E, WHITE, 0.15) if abs(x) > 0.3 else GREY_E)
                             for x in vals]).arrange(RIGHT, buff=0)
            arr = MathTex(r"\rightarrow", font_size=24, color=GREY_B)
            tok = data_text(repr(w)[1:-1] or " ", font=MONO, font_size=22, color=GREY_B)
            store.add(VGroup(strip, arr, tok).arrange(RIGHT, buff=0.15))
        store.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        dots_ = MathTex(r"\vdots", font_size=26, color=GREY_B).next_to(store, DOWN, buff=0.08).align_to(store[0][0], LEFT).shift(RIGHT * 0.8)
        sl = label(r"the memory: \ one (hidden state, \ next token) \\ pair for every token of the novels", font_size=19, color=GREY_A)
        nl = label(r"只展示64个邻居中的8个；投票使用全部64个" if zh() else
                   r"8 of the 64 neighbours shown; \\ the vote uses all 64", font_size=19, color=KNN_C)
        ng = VGroup(sl, store, dots_).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([0.9, -1.25, 0])
        nl.move_to(sl, aligned_edge=LEFT)
        tg = VGroup(label(r"the true next token:", font_size=18, color=GREY_A),
                    data_text(repr(ex["target"])[1:-1], font=MONO, font_size=22, color=WHITE),
                    label(rf"the model alone: \ ${100 * float(ex['p_lm']):.2g}\%$", font_size=18, color=LM_C),
                    label(rf"the neighbours' vote: \ ${100 * float(ex['p_knn']):.0f}\%$", font_size=18, color=KNN_C))
        tg.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([5.0, -1.0, 0])
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
            f"token {100 * float(ex['p_lm']):.2g} percent; <bookmark mark='d'/> the nearest stored states, from "
            f"places in the novels that looked the same, vote {100 * float(ex['p_knn']):.0f} percent for it."
        ) as vo:
            self.play(Write(f1), FadeIn(cite_), FadeIn(cg), FadeIn(tg[0]), FadeIn(tg[1]))
            self.play(FadeIn(sl), LaggedStart(*[FadeIn(r_) for r_ in store], lag_ratio=0.1), FadeIn(dots_))
            vo.wait_until("a")
            self.play(Write(f2))
            vo.wait_until("b")
            self.play(Indicate(cg, color=Q, scale_factor=1.03))
            vo.wait_until("c")
            self.play(FadeIn(tg[2]))
            vo.wait_until("d")
            self.play(FadeOut(sl), FadeIn(nl), *[r_[2].animate.set_color(KNN_C) for r_ in store],
                      *[r_[0].animate.set_stroke(KNN_C, width=1.5) for r_ in store], FadeIn(tg[3]))
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
        snapshot_note = note(
            "各比例快照在整批处理后记录；中间计数近似，最终计数精确" if zh() else
            r"fractional snapshots at complete batches; \ intermediate counts approximate, \ final count exact",
            font_size=16).to_edge(DOWN, buff=0.2)
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
            self.play(FadeIn(g1), FadeIn(g2), FadeIn(snapshot_note))
            vo.wait_until("a")
            self.play(Create(c1), run_time=1.5)
            self.play(Create(mark), FadeIn(ml))
            vo.wait_until("b")
            self.play(Create(bl), FadeIn(bll))
            self.play(Create(c2), FadeIn(d2), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def where(self):
        kn, sc = load("knn"), load("selfcache")
        best = kn["best_tokens"][:10]
        head = label(r"where the memories help", font_size=34).to_edge(UP, buff=0.35)
        tl = label(r"the novels: \ tokens of the passage it helps most \ (bits saved)", font_size=23, color=KNN_C)
        toks = VGroup(*[VGroup(data_text(repr(w)[1:-1] or " ", font=MONO, font_size=28, color=WHITE),
                               MathTex(f"{float(gn):.1f}", font_size=28, color=KNN_C)).arrange(RIGHT, buff=0.25)
                        for w, gn in best]).arrange_in_grid(rows=5, cols=2, buff=(0.9, 0.25), cell_alignment=LEFT)
        left = VGroup(tl, toks).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        if left.width > 6.4:
            left.width = 6.4
        left.move_to([-3.5, -0.3, 0])
        base = float(sc["base_bits"])
        gain = base - float(sc["bits"])
        hc = history_card(2017, r"a continuous cache \ (Grave, Joulin \& Usunier)",
                          r"相似的思路：按状态相似度，对已经读过的文本投票" if zh() else
                          r"a similar idea: \ a state-weighted vote over the text read so far",
                          color=HIST, width=5.6, font_size=22)
        res = label(rf"the passage's own past, \ beyond the $256$-token window: \\ ${base:.3f}$ $\rightarrow$ "
                    rf"${float(sc['bits']):.3f}$ bits per character \ ($\lambda = {float(sc['lam']):g}$)", font_size=23, color=RET)
        adaptation = note(r"原论文：点积权重；本例：最多32个最近的先前状态，平方欧氏距离" if zh() else
                          r"paper: \ dot-product weights; \\ ours: \ up to 32 nearest earlier states, \ squared Euclidean distance",
                          font_size=16)
        right = VGroup(hc, res, adaptation).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        if right.width > 6.2:
            right.width = 6.2
        right.move_to([3.5, -0.3, 0])
        names = [w.strip() for w, _ in best if w.strip()[:1].isupper()]
        v = (f"Some are capitalized tokens, like {names[0]}; here we show their measured gains. " if names else
             "The numbers beside them report the bits saved for each token on this passage. ")
        v2 = (f"Edouard Grave and colleagues proposed a similar idea in 2017, a continuous cache over the text read so far. "
              f"Our adaptation votes with up to thirty-two nearest earlier states using squared Euclidean distance. "
              f"On this passage, the aggregate score moves from {base:.3f} to {float(sc['bits']):.3f}: "
              "an improvement from its own past." if gain > 0.005 else
              f"Edouard Grave and colleagues proposed a similar idea in 2017, a continuous cache over the text read so far. "
              f"Our adaptation votes with up to thirty-two nearest earlier states using squared Euclidean distance. "
              f"On our passage it scores {float(sc['bits']):.3f} against {base:.3f}, little aggregate gain.")
        with self.voiceover(
            "Where does the memory of the novels help? <bookmark mark='a'/> Here are the tokens of the passage "
            "where it saves the most bits. " + v + "<bookmark mark='b'/> " + v2
        ) as vo:
            veil = Rectangle(width=right.width + 0.2, height=right.height + 0.2, stroke_width=0, fill_color=BACKGROUND,
                             fill_opacity=0.82).move_to(right)
            self.play(FadeIn(head), FadeIn(tl), LaggedStart(*[FadeIn(t_) for t_ in toks], lag_ratio=0.1), FadeIn(right), FadeIn(veil))
            vo.wait_until("a")
            self.play(Indicate(toks, color=KNN_C, scale_factor=1.03))
            vo.wait_until("b")
            self.play(FadeOut(veil))
            self.play(Indicate(res, color=RET, scale_factor=1.03))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def board(self):
        S = load("scoreboard")
        rows = [dict(r) for r in S["rows"]]
        mine = [i for i, r in enumerate(rows) if r.get("part") == 15]
        board = scoreboard(rows, highlight=tuple(mine), max_bits=3.6, row_h=0.52, font_size=24, bar_width=3.8,
                           label_width=5.4)
        board.scale_to_fit_height(min(board.height, 6.0))
        if board.width > 9.8:
            board.scale_to_fit_width(9.8)
        board.move_to([-1.7, -0.45, 0])
        head = label(r"The scoreboard: \ \textit{The Maltese Falcon}, \ chapter 2", font_size=30).to_edge(UP, buff=0.3)
        hc = history_card(2021, r"RETRO \ (Borgeaud et al., DeepMind)",
                          r"从$2$万亿词元检索；在Pile上接近GPT-3，参数少$25$倍" if zh() else
                          r"retrieval from $2$ trillion tokens; \ about GPT-3's quality on the Pile \ with $25\times$ "
                          r"fewer parameters", color=HIST, width=3.1, font_size=19)
        hc.move_to([5.35, 0.6, 0])
        protocol_note = wrapped_label(
            "沿用各部分原始评分流程；评分目标集合有所不同。第13部分末尾29个字符未评分。比较细小分差前，应先统一评分目标集合。" if zh() else
            r"Original scoring protocols retained; \ scored target cohorts differ across parts. \ Part 13 leaves 29 "
            r"suffix characters unscored. \ Small gaps require aligned target cohorts.",
            3.1, font_size=14, color=GREY_B).next_to(hc, DOWN, buff=0.25).align_to(hc, LEFT)
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
            self.play(FadeIn(head), FadeIn(hc), FadeIn(board), FadeIn(protocol_note))
            vo.wait_until("a")
            for i in mine:
                self.play(Indicate(board.rows[i], color=C.BITS, scale_factor=1.02), run_time=0.6)
        self.wait(0.3)
        self.clear_scene()
