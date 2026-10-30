from __future__ import annotations

import math

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai16.common import (BLOCKC, DENSEC, EXPERT_COLORS, FULLC, INDEXC, MODE_COLOR, MODES, MOEC, PART, RANDC,
                                   REINITC, ROUTER, TICKETC, TOTALC, WINC, load, load_image, ms)


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
        d = load("mix1991")
        G = np.asarray(d["compete_gate"], float)[-1]
        grid = np.asarray(d["grid"], float)
        a0 = plane([-1, 1, 1], [0, 1, 1])
        out.append((VGroup(*[curve(a0, grid, G[:, i], EXPERT_COLORS[i], 3) for i in range(G.shape[1])]),
                    r"competing experts, 1991", C.HUMAN))
        g = load("gradcheck")["softmax-k"]
        fd = np.asarray(g["fd"], float)
        bars = VGroup(*[Rectangle(width=0.22, height=max(1.6 * abs(v) / np.abs(fd).max(), 0.02), stroke_width=0,
                                  fill_color=C.SURPRISE if abs(v) > 1e-9 else GREY_D, fill_opacity=0.9)
                        .move_to([0.32 * i, 0.8 * v / np.abs(fd).max(), 0]) for i, v in enumerate(fd)])
        out.append((bars, r"the router's gradient", ROUTER))
        m = load("moe")
        a1 = plane([0, 2000, 1], [float(np.asarray(m["moe_curve"])[:, 2:, 1].min()) - 0.05,
                                  float(np.asarray(m["moe_curve"])[:, 2, 1].max()) + 0.1, 1])
        lines = VGroup()
        for k, col in (("dense_active", DENSEC), ("moe", MOEC), ("dense_total", TOTALC)):
            a = np.asarray(m[f"{k}_curve"], float).mean(0)[2:]
            lines.add(curve(a1, a[:, 0], np.minimum(a[:, 1], a1.y_range[1]), col, 3))
        out.append((lines, r"mixture vs.\ dense", MOEC))
        b = load("balance")
        for k, cap in (("none", r"no balancing"), ("moe", r"the loss-free bias")):
            L = np.asarray(b[f"{k}_loads"], float)[0, :, 0]
            out.append((load_image(L, 2.6, 1.3), cap, MODE_COLOR[k]))
        f = load("fine")
        vals = [ms(f[f"{k}_valid"])[0] for k in ("moe", "fine", "shared")]
        lo = min(vals) - 0.02
        fb = VGroup(*[Rectangle(width=0.5, height=max(8 * (v - lo), 0.05), stroke_width=0, fill_color=c_, fill_opacity=0.85)
                      for v, c_ in zip(vals, (MOEC, C.BITS, C.SHARED_EXPERT))]).arrange(RIGHT, buff=0.25, aligned_edge=DOWN)
        out.append((fb, r"fine-grained, \ shared", C.SHARED_EXPERT))
        r = load("recall")
        a2 = plane([0, int(r["steps"]), 1], [0, 1, 1])
        rl = VGroup(*[curve(a2, np.asarray(r[f"{k}_curve"], float)[0, :, 0], np.asarray(r[f"{k}_curve"], float).mean(0)[:, 1], c_, 3)
                      for k, c_ in (("full", FULLC), ("window", WINC), ("blocks", BLOCKC))])
        out.append((rl, r"sparse attention, \ trained", INDEXC))
        lt = load("lottery")
        rem = np.log10(np.concatenate([[1.0], np.asarray(lt["remain_s0"], float)]))
        t = np.array([lt["dense_s0"]] + list(lt["ticket_s0"]))
        ri = np.array([lt["dense_s0"]] + list(lt["reinit_s0"]))
        a3 = plane([float(rem.min()), 0, 1], [float(min(t.min(), ri.min())) - 0.02, float(max(t.max(), ri.max())) + 0.02, 1])
        out.append((VGroup(curve(a3, rem, ri, REINITC, 3), curve(a3, rem, t, TICKETC, 3)), r"lottery tickets", TICKETC))
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
        head = label(rf"Part {PART}, in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        m = load("moe")
        win = ms(m["moe_valid"])[0] < ms(m["dense_active_valid"])[0]
        ours = ("Our own mixture beat a dense model with the same arithmetic. " if win else
                "Our own mixture didn't beat a dense model with the same arithmetic, at our tiny scale. ")
        with self.voiceover(
            "Let's take stock. In 1991 experts learned to compete and specialize. A router learns only from the "
            "experts it tries, which is why it needs noise to explore and help to share. "
            + ours + "<bookmark mark='o'/>Left alone, routers play favourites; Switch's loss and DeepSeek's bias spread the work, and the bias "
            "does it without bending the model. Finer experts, a shared one, capacity and chips, all follow from the "
            "same picture. Attention can choose its keys too, if the choice is learned. And weights can be pruned: "
            "lottery tickets exist, and two-in-four is the pattern hardware can use."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.15, scale=0.95) for t_ in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"tensor cores, \ NVLink, \ $2{:}4$ sparsity in hardware", [17]),
            (r"expert parallelism and its all-to-all, \ at scale", [18]),
            (r"serving experts and sparse attention", [19]),
            (r"experts in image and video models", [22]),
            (r"features that fire sparsely, \ inside the network", [30]),
        ], font_size=24)
        with self.voiceover(
            "All of this comes back. The tensor cores and links that make experts and two-in-four fast are next "
            "time's subject, part seventeen. Part eighteen trains across thousands of chips, with expert parallelism "
            "and its all-to-all. Part nineteen serves experts and sparse attention. Image and video models use experts "
            "too, in part twenty-two. And in part thirty, sparsity shows up inside the network itself: features that "
            "fire only rarely, found with sparse autoencoders."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"For DeepSeek-V3's gates $g_i = \sigma(s_i) / \sum_{j \in \mathcal K} \sigma(s_j)$, \ show that "
            r"$\partial L / \partial s_j = (1 - \sigma(s_j))\, g_j\, (u_j - \bar u)$ for $j \in \mathcal K$, \ and $0$ otherwise.",
            r"Show that if $f = P$, \ Switch's $E \sum_i f_i P_i \ge 1$, \ with equality only when every $f_i = 1/E$. "
            r"\ Why does it matter that $f$ has no gradient?",
            r"Show that $(N/k)^k \le \binom{N}{k} \le (eN/k)^k$, \ and compute $\binom{64}{8} / \binom{16}{2}$.",
            r"Eight experts get these shares of the token-slots: \ $0.3, 0.2, 0.2, 0.1, 0.1, 0.05, 0.03, 0.02$. \ What "
            r"share is dropped at capacity factors $1$ and $1.25$?",
            r"DeepSeek-V4-Pro: \ $d = 7{,}168$, \ experts of width $3{,}072$, \ $6$ routed per token. \ Compute the "
            r"all-to-all bytes per token per layer (FP8 out, BF16 back), \ the experts' FLOPs, \ and their ratio.",
            r"Mixtral 8x7B: \ $32$ layers, \ $d = 4{,}096$, \ SwiGLU experts of width $14{,}336$, \ $32$ query heads "
            r"and $8$ key-value heads of $128$, \ a vocabulary of $32{,}000$. \ Count its total and active parameters.",
        ], font_size=21)
        with self.voiceover(
            "Here are six problems to try, from the router's gradient to counting Mixtral's parameters. Pause here, "
            "and work through them; full solutions are in this part's notes."
        ) as vo:
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows], lag_ratio=0.3),
                      run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 17, \ Silicon", font_size=40).to_edge(UP, buff=0.5)
        n = 8
        cells = VGroup(*[Square(0.5, stroke_color=C.GPU, stroke_width=1.5, fill_color=C.GPU, fill_opacity=0.08)
                         for _ in range(n * n)]).arrange_in_grid(rows=n, cols=n, buff=0.06).move_to(DOWN * 0.4)
        tag = note(r"schematic: \ a systolic array", font_size=18).to_corner(DR, buff=0.3)
        ql = label(r"why AI runs on GPUs: \ arithmetic, \ memory, \ and the wires between", font_size=28,
                   color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Next time: silicon. Why does all of this run on GPUs, and what limits it: arithmetic, memory, and the "
            "wires between chips. <bookmark mark='a'/> Part seventeen."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells), FadeIn(tag))
            for wave in range(2 * n - 1):
                idx = [i * n + j for i in range(n) for j in range(n) if i + j == wave]
                self.play(*[cells[k].animate.set_fill(opacity=0.7) for k in idx], run_time=0.18)
            vo.wait_until("a")
            self.play(FadeIn(ql), cells.animate.set_fill(opacity=0.25))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        card = reference_card(
            [r"S.~J.~D.~Prince, \textit{Understanding Deep Learning} (2023)",
             r"W.~Cai et al., \textit{A Survey on Mixture of Experts in Large Language Models} (2024)"],
            [r"Jacobs, Jordan, Nowlan \& Hinton (1991); \ Jordan \& Jacobs (1994); \ Shazeer et al.\ (2017); \ Lepikhin et al., "
             r"\textit{GShard} (2020); \ Fedus, Zoph \& Shazeer, \textit{Switch} (2021); \ Du et al., \textit{GLaM} (2021)",
             r"Zoph et al., \textit{ST-MoE} (2022); \ Zhou et al., \textit{Expert Choice} (2022); \ Komatsuzaki et al., "
             r"\textit{Sparse Upcycling} (2022); \ Jiang et al., \textit{Mixtral} (2024); \ Muennighoff et al., \textit{OLMoE} (2024)",
             r"Dai et al., \textit{DeepSeekMoE} (2024); \ Wang et al., \textit{Auxiliary-Loss-Free Load Balancing} (2024); \ "
             r"DeepSeek-AI, V2, V3 (2024), V3.2 (2025), V4 (2026); \ Raposo et al., \textit{Mixture-of-Depths} (2024)",
             r"Child et al.\ (2019); \ Beltagy et al., \textit{Longformer} (2020); \ Zaheer et al., \textit{BigBird} (2020); \ "
             r"Yuan et al., \textit{NSA} (2025); \ Lu et al., \textit{MoBA} (2025); \ Arora et al., \textit{Zoology} (2023)",
             r"LeCun, Denker \& Solla (1990); \ Han et al.\ (2015); \ Frankle \& Carbin (2019); \ Frankle et al.\ (2020); "
             r"\ Mishra et al.\ (2021); \ Frantar \& Alistarh, \textit{SparseGPT} (2023); \ Sun et al., \textit{Wanda} (2023)",
             r"Li et al., \textit{The Lazy Neuron Phenomenon} (2023); \ Liu et al., \textit{TEAL} (2024); \ model cards: "
             r"Llama 4, Qwen3, Kimi K2 and K3, GLM-4.5 and 5, gpt-oss, Qwen3-Next, Qwen3.5, MiniMax-M2 and M3, Mistral Large 4"])
        credit = note(narration_credit(), font_size=18).to_edge(DOWN, buff=0.15)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.15:
            card.shift(UP * (credit.get_top()[1] + 0.15 - card.get_bottom()[1]))
        with self.voiceover(
            "To go further, the Switch Transformer and DeepSeek-V3 papers are good places to start. Thanks for "
            "watching, and see you in part seventeen."
        ):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(1.5)
        self.clear_scene()
