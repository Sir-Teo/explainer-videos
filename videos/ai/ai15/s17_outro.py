from __future__ import annotations

import math

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai15.common import (ADD, DECAY, DELTA, MIX_C, PART, RET, SSM_C, STATE, curve, load, signed_grid)


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.problems()
        self.next_time()
        self.references()

    # ------------------------------------------------------------------
    def tiles(self):
        TW, TH = 3.0, 2.0

        def plane(xr, yr):
            return Axes(x_range=xr, y_range=yr, x_length=TW, y_length=TH, tips=False, axis_config={"stroke_width": 0})

        out = []
        k = load("kvcache")
        pt = k["per_token"]
        vals = [pt["llama_mha"], pt["llama"], pt["mla"], pt["qwen"]]
        cols = [GREY_B, C.TRUE_P, C.BITS, C.INTERVAL]
        bars = VGroup(*[Rectangle(width=0.5, height=0.3 + 0.55 * (math.log10(v) - 4), stroke_width=0, fill_color=c_,
                                  fill_opacity=0.85) for v, c_ in zip(vals, cols)]).arrange(RIGHT, buff=0.2, aligned_edge=DOWN)
        out.append((bars, r"shrinking the cache", C.BITS))
        s = load("sinks")
        a2 = plane([0, int(s["n"]), 500], [3, 7, 1])

        def sm(x, n=100):
            x = np.asarray(x, float)
            return np.convolve(x, np.ones(n) / n, mode="valid")

        out.append((VGroup(curve(a2, np.arange(len(sm(s["ref"]))), np.clip(sm(s["ref"]), 3, 7), WHITE, 2),
                           curve(a2, np.arange(len(sm(s["loss_window_64"]))), np.clip(sm(s["loss_window_64"]), 3, 7), C.SURPRISE, 2.5),
                           curve(a2, np.arange(len(sm(s["loss_sinks_64"]))), np.clip(sm(s["loss_sinks_64"]), 3, 7), C.INTERVAL, 2.5)),
                    r"sinks and windows", C.INTERVAL))
        m = load("matrix_rw")
        out.append((signed_grid(np.asarray(m["S_delta"])[4], 1.9), r"a matrix memory", STATE))
        c = load("capacity")
        a4 = plane([0, 256, 64], [0, 2.5, 1])
        out.append((VGroup(curve(a4, np.asarray(c["Ns"]), np.minimum(np.asarray(c["err_add"]), 2.5), ADD, 3)), r"crosstalk", ADD))
        tree = VGroup()
        for lv, kk in enumerate((1, 2, 4)):
            for i in range(8):
                tree.add(Square(0.22, stroke_width=1, stroke_color=GREY_C, fill_color=C.BITS if i < 2 ** (lv + 1) else STATE,
                                fill_opacity=0.5).move_to([i * 0.32, -lv * 0.55, 0]))
        out.append((tree, r"the parallel scan", C.BITS))
        h = load("hippo")
        L = int(h["L"])
        a6 = plane([0, L, 500], [-1.2, 1.2, 1])
        flat = np.asarray(h["snaps_32"])
        out.append((VGroup(curve(a6, np.arange(L)[::4], np.asarray(h["f"])[::4], GREY_B, 2),
                           curve(a6, np.arange(L)[::4], flat[-L:][::4], C.INTERVAL, 2.5)), r"HiPPO memorizes", SSM_C))
        q = load("mqar")
        dks = [int(x) for x in q["dks"]]
        a7 = plane([0, len(dks) - 1, 1], [0, 1, 0.5])
        out.append((VGroup(*[curve(a7, np.arange(len(dks)), np.asarray(q[f"acc_{kk}"]).mean(1), MIX_C[kk], 2.5)
                             for kk in q["mixers"]]), r"recall, measured", MIX_C["gdn"]))
        kn = load("knn")
        snaps = [int(x) for x in kn["snaps"]]
        bits = np.array([kn[f"snap_{x}"]["bits"] for x in snaps])
        lo, hi = float(bits.min()) - 0.01, float(kn["base_bits"]) + 0.005
        a8 = plane([0, len(snaps) - 1, 1], [lo, hi, 0.01])
        out.append((VGroup(curve(a8, np.arange(len(snaps)), bits, RET, 3),
                           DashedLine(a8.c2p(0, float(kn["base_bits"])), a8.c2p(len(snaps) - 1, float(kn["base_bits"])),
                                      color=C.NEURAL, stroke_width=1.5)), r"a memory of the novels", RET))
        tiles = Group()
        for pic, cap, col in out:
            box, c_ = tile_frame(cap, col, TW, TH)
            pic.move_to(box.get_center() + UP * 0.22)
            if pic.width > TW:
                pic.width = TW
            if pic.height > TH:
                pic.height = TH
            tiles.add(Group(box, pic, c_))
        tiles.arrange_in_grid(rows=2, cols=4, buff=(0.22, 0.3)).move_to(DOWN * 0.3)
        return tiles

    def recap(self):
        tiles = self.tiles()
        q, kn = load("mqar"), load("knn")
        gd, hy = float(np.asarray(q["acc_gdn"])[0].mean()), float(np.asarray(q["acc_hybrid"])[0].mean())
        gain = float(kn["base_bits"]) - float(kn[f"snap_{int(kn['snaps'][-1])}"]["bits"])
        r1 = (f"In our recall test, fixed memories needed room or a way to overwrite, and with the smallest memories one "
              f"attention layer on top lifted recall from {100 * gd:.0f} to {100 * hy:.0f} percent; the newest models "
              "are built that way." if hy > gd + 0.1 else
              f"In our recall test, fixed memories needed room or a way to overwrite; with the smallest memories, one "
              f"attention layer on top gave {100 * hy:.0f} percent against {100 * gd:.0f}.")
        r2 = (f"And a memory can live outside the model: a nearest-neighbour vote from the novels took {gain:.3f} bits "
              "per character off our model's score." if gain > 0.002 else
              "And a memory can live outside the model, though for our passage a vote from the novels gained little.")
        head = label(rf"Part {PART}, in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. Attention's memory is its cache; models shrink it by sharing keys and values or "
            "squeezing them into a latent, and a server can evict some of it, as long as it keeps the sink. Drop "
            "the softmax and attention becomes a recurrence on a matrix, the fast weights of 1992, written by "
            "outer products and read with a key; adding fills it with crosstalk, decaying forgets, and the delta "
            "rule, one step of least squares, corrects. An associative scan, or chunks in the WY form, trains such "
            "a recurrence in parallel. State-space models came from the other side, HiPPO's memory of a whole "
            "signal and S4's convolution, and Mamba made them choose. <bookmark mark='a'/> " + r1
            + " <bookmark mark='b'/> " + r2
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.15, scale=0.95) for t_ in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"choosing which tokens to read: \ sparse attention, \ DeepSeek's indexer", [16]),
            (r"serving the cache: \ paging, \ sharing, \ fewer bits", [19]),
            (r"state tracking and parity: \ what depth can and can't do", [28]),
            (r"memory for agents: \ notes, \ compaction, \ retrieval", [29]),
            (r"where a trained model keeps its facts", [30]),
        ], font_size=26)
        with self.voiceover(
            "All of this comes back. Choosing which tokens to read, sparse attention and DeepSeek's indexer, is "
            "Part 16. Serving the cache fast is Part 19. The delta rule's reflections and state tracking meet "
            "reasoning in Part 28. Agents, in Part 29, manage their memory by hand, with notes, compaction and "
            "retrieval. And Part 30 looks for where a trained model keeps its facts."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"A model has $L$ layers and $H$ key-value heads of $d_h$ numbers, \ in bf16. \ How many bytes does its "
            r"cache take per token? \ Evaluate for Llama 3.1 70B ($L = 80$, $H = 8$, $d_h = 128$) at $128{,}000$ "
            r"tokens, \ and with one key-value head.",
            r"For $N$ random unit keys in $d$ dimensions, \ show $\mathbb E[(k_i \cdot k_j)^2] = 1/d$ for $i \ne j$, "
            r"\ and that adding $N$ pairs gives a relative read error of about $(N-1)/d$.",
            r"With $\|k\| = 1$, \ show the delta rule gives $S_t k = (1 - \beta) S_{t-1} k + \beta v$ \ and leaves "
            r"$S_t u = S_{t-1} u$ for $u \perp k$. \ Find the eigenvalues of $I - \beta k k^{\top}$; \ for which $\beta$ "
            r"is it a projection, \ a reflection?",
            r"Show that $(a_1, b_1) \bullet (a_2, b_2) = (a_1 a_2, \ a_2 b_1 + b_2)$ is associative, \ find its identity, "
            r"\ and count the rounds of a scan over $10^6$ tokens.",
            r"For $h' = -\lambda h + x$, \ derive the zero-order hold $\bar A = e^{-\lambda\Delta}$, \ "
            r"$\bar B = (1 - e^{-\lambda\Delta})/\lambda$. \ When is Euler's $\bar A = 1 - \lambda\Delta$ unstable? \ "
            r"For eigenvalues $-0.3 \pm 2i$, \ find the largest stable step.",
            r"A kNN-LM mixes $p = \lambda p_{\mathrm{kNN}} + (1 - \lambda) p_{\mathrm{LM}}$. \ Show it never costs more "
            r"than $\log_2 \tfrac{1}{1-\lambda}$ bits on a token, \ and find when it saves bits.",
        ], font_size=21)
        with self.voiceover(
            "Here are six problems, from pricing a cache to the cost of a nearest-neighbour vote. Pause here and "
            "work through them; full solutions are in this part's notes."
        ) as vo:
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows], lag_ratio=0.3),
                      run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 16, \ Sparsity", font_size=40).to_edge(UP, buff=0.4)
        g = np.random.default_rng(13)
        experts = VGroup(*[RoundedRectangle(width=0.7, height=0.7, corner_radius=0.1, stroke_color=GREY_C, stroke_width=2)
                           for _ in range(16)]).arrange_in_grid(rows=2, cols=8, buff=0.25).move_to(DOWN * 0.6)
        tok = data_text("Spade", font="DejaVu Sans Mono", font_size=30, color=C.BITS).move_to(UP * 1.4)
        chosen = sorted(g.choice(16, 2, replace=False))
        arrows = VGroup(*[Arrow(tok.get_bottom(), experts[i].get_top(), buff=0.1, color=C.BITS, stroke_width=3) for i in chosen])
        tag = note(r"schematic").to_corner(DR, buff=0.3)
        ql = label(r"each token visits only a few experts, \ and reads only some of the past", font_size=28,
                   color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Next time: sparsity. The biggest models don't use all their weights for every token: a router sends "
            "each token to a few experts among hundreds, and attention can read only the tokens that matter. "
            "<bookmark mark='a'/> How do you route, and how do you keep every expert busy?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(experts), FadeIn(tok), FadeIn(tag))
            self.play(LaggedStart(*[GrowArrow(a_) for a_ in arrows], lag_ratio=0.3),
                      *[experts[i].animate.set_fill(C.BITS, opacity=0.4) for i in chosen])
            vo.wait_until("a")
            self.play(FadeIn(ql))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        card = reference_card(
            [r"S.~J.~D.~Prince, \textit{Understanding Deep Learning} (2023), \ ch.~12",
             r"S.~Yang, \textit{DeltaNet Explained} (blog, 2024) \ and the \textit{flash-linear-attention} library",
             r"A.~Gu, \textit{Modeling Sequences with Structured State Spaces} (PhD thesis, Stanford, 2023)"],
            [r"Hopfield (1982); \ Kohonen (1972); \ Anderson (1972); \ Schmidhuber (1992); \ Ba et al.\ (2016); \ Graves et "
             r"al., NTM (2014); \ Weston et al.\ (2014); \ Sukhbaatar et al.\ (2015)",
             r"Shazeer, MQA (2019); \ Ainslie et al., GQA (2023); \ DeepSeek-AI, V2 (2024), V3 (2024); \ Child et al.\ (2019); "
             r"\ Dai et al., Transformer-XL (2019); \ Beltagy et al., Longformer (2020); \ Zaheer et al., BigBird (2020)",
             r"Xiao et al., StreamingLLM (2023); \ Zhang et al., H$_2$O (2023); \ Katharopoulos et al.\ (2020); \ Schlag, Irie "
             r"\& Schmidhuber (2021); \ Widrow \& Hoff (1960)",
             r"Yang et al., DeltaNet (2024); \ Yang, Kautz \& Hatamizadeh, Gated DeltaNet (2025); \ Kimi Team, Kimi Linear "
             r"(2025); \ Beck et al., xLSTM (2024); \ Peng et al., RWKV-7 (2025); \ Grazzi et al.\ (2025)",
             r"Blelloch (1990); \ Martin \& Cundy (2018); \ Gu et al., HiPPO (2020); \ Gu, Goel \& R\'e, S4 (2022); \ Gu "
             r"\& Dao, Mamba (2023); \ Dao \& Gu, Mamba-2 (2024); \ Lahoti et al., Mamba-3 (2026)",
             r"Sun et al., TTT (2024); \ Behrouz, Zhong \& Mirrokni, Titans (2025); \ Wang, Shi \& Fox, Test-time regression "
             r"(2025); \ Arora et al., Zoology (2023)",
             r"Lieber et al., Jamba (2024); \ MiniMax (2025); \ NVIDIA, Nemotron-H (2025), Nemotron 3 (2025); \ Qwen Team, "
             r"Qwen3-Next (2025), Qwen3.5 (2026); \ Moonshot, Kimi K3 (2026); \ DeepSeek-AI, V4 (2026)",
             r"Kamradt (2023); \ Liu et al., Lost in the Middle (2023); \ Hsieh et al., RULER (2024); \ Modarressi et al., "
             r"NoLiMa (2025); \ Hong et al., Context Rot (2025)",
             r"Karpukhin et al., DPR (2020); \ Guu et al., REALM (2020); \ Lewis et al., RAG (2020); \ Khandelwal et al., "
             r"kNN-LM (2020); \ Grave et al.\ (2017); \ Borgeaud et al., RETRO (2021)"])
        credit = note(narration_credit(), font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Songlin Yang's papers and blog on linear attention and the delta rule are the best way in, and Albert "
            "Gu's thesis for state-space models. Thanks for watching, and see you in Part 16."
        ):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(1.5)
        self.clear_scene()
