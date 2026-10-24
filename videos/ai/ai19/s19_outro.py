from __future__ import annotations

import math

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai19.common import (ATTNC, CONTC, DECODEC, DRAFTC, EAGLEC, ERRC, GPTQC, LEVELC, PAGEDC, PART,
                                   PREFILLC, ROTC, RTNC, COSTC, load, node_box)
from videos.ai.ai19.s05_scheduling import gantt
from videos.ai.ai19.s06_paging import memory_map
from videos.ai.ai30.compute import load as load30


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

        def mk(xr, yr):
            return Axes(x_range=xr, y_range=yr, x_length=TW * 0.9, y_length=TH * 0.85, tips=False,
                        axis_config={"stroke_color": GREY_D, "include_ticks": False})

        out = []
        ph = load("phases")
        T, B = np.log10(ph["prefill_T"]), np.log10(ph["decode_B"])
        pt, dt = np.log10(ph["prefill_tps"]), np.log10(ph["decode_tps"])
        ax = mk([0, 2.5, 1], [2.4, float(max(pt.max(), dt.max())) + 0.2, 1])
        out.append((VGroup(ax, curve(ax, T, pt, PREFILLC, 3), curve(ax, B, dt, DECODEC, 3)), r"prefill and decode",
                    DECODEC))
        ec = load("economics")
        d1 = ec["c1024"]
        u, c = np.log10(d1["user"]), np.log10(d1["cost"])
        ax = mk([float(u.min()) - 0.1, float(u.max()) + 0.1, 1], [float(c.min()) - 0.1, float(c.max()) + 0.1, 1])
        out.append((VGroup(ax, curve(ax, u, c, COSTC, 3)), r"batching's price", COSTC))
        sv = load("serving")
        g = gantt(np.asarray(sv["gantt_cont"]), float(np.asarray(sv["gantt_cont"])[:, 2].max()), width=2.8, row_h=0.22)
        out.append((g, r"continuous batching", CONTC))
        pg = load("paging")
        mm = memory_map(pg["snap_paged"], int(pg["pool"]), cols=32, cell=0.085, center=(0, 0))
        out.append((mm, r"pages", PAGEDC))
        dr = load("drafters")
        ev_d, ev_e = np.asarray(dr["draft"]["evals"]), np.asarray(dr["eagle"]["evals"])
        ax = mk([0, float(max(ev_d[-1, 0], ev_e[-1, 0])), 1], [0, 1, 0.5])
        out.append((VGroup(ax, curve(ax, ev_d[:, 0], ev_d[:, 2], DRAFTC, 3), curve(ax, ev_e[:, 0], ev_e[:, 2], EAGLEC, 3)),
                    r"drafters, \ trained", EAGLEC))
        rd = load("rounding")
        bits = np.asarray(rd["mse_bits"])
        ax = mk([1.5, 8.5, 1], [float(np.log10(rd["mse_row"]).min()) - 0.3, float(np.log10(rd["pred_row"]).max()) + 0.3, 1])
        out.append((VGroup(ax, curve(ax, bits, np.log10(rd["pred_row"]), LEVELC, 3),
                           *[Dot(ax.c2p(b_, math.log10(v)), radius=0.04, color=ERRC) for b_, v in zip(bits, rd["mse_row"])]),
                    r"$\Delta^2 / 12$", LEVELC))
        rt = load("rotation")
        base = float(rt["fp32"])
        vals = [rt["loss"]["w4a4_plain"] - base, rt["loss"]["w4a4_hadamard"] - base]
        q = load("gptq")
        g3 = float(np.mean([q["res"][f"gptq_3_row_s{s}"] for s in q["seeds"]])) - float(q["fp32"])
        r3 = q["res"]["rtn_3_row"] - float(q["fp32"])
        top = max(vals + [r3, g3])
        bars = VGroup(*[Rectangle(width=0.32, height=max(1.6 * v / top, 0.02), stroke_width=0, fill_color=col,
                                  fill_opacity=0.9).move_to([0.42 * i, 0.8 * v / top, 0])
                        for i, (v, col) in enumerate(zip([r3, g3, vals[0], vals[1]], [RTNC, GPTQC, RTNC, ROTC]))])
        out.append((bars, r"GPTQ; \ rotations", ROTC))
        fl = load("flash")
        Ns = np.log10(np.asarray(fl["Ns"], float))
        ax = mk([float(Ns[0]), float(Ns[-1]), 1], [5, 11.5, 1])
        out.append((VGroup(ax, curve(ax, Ns, np.log10(np.asarray(fl["io_std_64"], float)), ATTNC, 3),
                           curve(ax, Ns, np.log10(np.asarray(fl["io_flash_64"], float)), C.BITS, 3)),
                    r"FlashAttention's traffic", ATTNC))
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
        with self.voiceover(
            "Let's take stock. Reading a prompt is arithmetic and writing an answer is reading memory, so a server "
            "batches the writing, and the price of a token follows from the batch it can afford. Continuous "
            "batching keeps the batch full, and pages keep the memory full. A drafter guesses ahead and the big "
            "model checks in one pass, with exactly the same output. Rounding error is delta squared over twelve; "
            "GPTQ and rotations spend it where it hurts least, and four-bit floats store it compactly. And "
            "FlashAttention never writes its table down."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.15, scale=0.95) for t_ in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"sampling one step at a time, \ and needing fewer steps", [20, 21]),
            (r"thinking longer: \ tokens of thought, \ paid for by decoding", [28]),
            (r"agents: \ long contexts, \ many calls, \ shared prefixes", [29]),
            (r"outlier channels: \ what the directions inside a model mean", [30]),
            (r"structured output, \ checked: \ evaluations you can trust", [31]),
        ], font_size=24)
        card.move_to([-1.2, 0.2, 0])
        sp = load30("superposition")
        W = np.asarray(sp["W0.97"])
        c0 = np.array([5.3, -2.2, 0])
        sc = 0.75 / max(np.linalg.norm(W, axis=0).max(), 1e-6)
        circ = Circle(radius=0.75, stroke_color=GREY_D, stroke_width=1.5).move_to(c0)
        arrows = VGroup(*[Arrow(c0, c0 + sc * np.array([W[0, i], W[1, i], 0]), buff=0, stroke_width=3, color=col,
                                max_tip_length_to_length_ratio=0.15)
                          for i, col in enumerate((C.TRUE_P, C.BITS, C.INTERVAL, C.SURPRISE, C.NEURAL))])
        cap = label(r"Part 30: \ $5$ features in $2$ dimensions", font_size=16, color=GREY_A).next_to(circ, UP, buff=0.12)
        with self.voiceover(
            "All of this comes back. Generating images one pixel at a time, and the race to take fewer steps, are "
            "Parts 20 and 21. Reasoning models think in tokens that decoding pays for, Part 28; agents run long "
            "contexts and many calls with shared prefixes, Part 29. The outlier channels of chapter nine are a "
            "clue to what the directions inside a model mean: Part 30 shows a network packing more features than "
            "it has dimensions. And Part 31 asks how to trust what comes out."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      Create(circ), FadeIn(cap), LaggedStart(*[GrowArrow(a_) for a_ in arrows], lag_ratio=0.2),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"With each draft accepted independently with probability $\alpha$, \ show that a pass writes "
            r"$(1 - \alpha^{k+1})/(1 - \alpha)$ tokens on average. \ For $\alpha = 0.8$ and a draft step costing "
            r"$c = 0.05$ passes, \ which $k$ is fastest?",
            r"Show that speculative sampling outputs $x$ with probability exactly $p(x)$, \ and that its acceptance "
            r"rate is $1 - \mathrm{TV}(p, q)$.",
            r"Derive $\mathbb E[e^2] = \Delta^2/12$ for rounding to a grid of step $\Delta$, \ and show that one more "
            r"bit lowers the error by $10 \log_{10} 4 \approx 6.02$ dB.",
            r"A model has $48$ layers and $8$ key-value heads of $128$ in $16$ bits. \ How many bytes does its cache "
            r"keep per token, \ and at what context does one conversation's cache weigh $60$ GB?",
            r"Minimize $\tfrac12 \delta^\top H \delta$ subject to $e_q^\top \delta = \hat w_q - w_q$: \ derive the Optimal "
            r"Brain Surgeon update and the error it leaves.",
            r"Two chunks of keys give partial results $(m_1, \ell_1, o_1)$ and $(m_2, \ell_2, o_2)$. \ Show how to "
            r"combine them into exact attention, \ and that the order doesn't matter.",
        ], font_size=21)
        with self.voiceover(
            "Here are six problems to try, from the drafter's formula to Flash-Decoding's combination. Pause here, "
            "and work through them; full solutions are in this part's notes."
        ) as vo:
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows], lag_ratio=0.3),
                      run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 20, \ Four Ways to Generate", font_size=40).to_edge(UP, buff=0.5)
        g = np.random.default_rng(20)
        # four families, as pictures (schematic)
        ar = VGroup(*[Square(0.22, stroke_width=0.5, stroke_color=GREY_D, fill_color=WHITE,
                             fill_opacity=float(g.uniform(0.1, 0.9)) if k < 23 else 0.0) for k in range(36)])
        ar.arrange_in_grid(rows=6, cols=6, buff=0.02)
        vae = VGroup(Polygon([-0.7, 0.6, 0], [0, 0.15, 0], [0, -0.15, 0], [-0.7, -0.6, 0], stroke_color=C.EMBED,
                             stroke_width=2, fill_color=C.EMBED, fill_opacity=0.2),
                     Polygon([0.7, 0.6, 0], [0, 0.15, 0], [0, -0.15, 0], [0.7, -0.6, 0], stroke_color=C.MLP,
                             stroke_width=2, fill_color=C.MLP, fill_opacity=0.2))
        gan = VGroup(node_box(r"$G$", C.PROB, font_size=24), node_box(r"$D$", C.SURPRISE, font_size=24)).arrange(RIGHT,
                                                                                                            buff=0.6)
        gan.add(DoubleArrow(gan[0].get_right(), gan[1].get_left(), buff=0.05, stroke_width=2, color=GREY_B,
                            max_tip_length_to_length_ratio=0.2))
        grid = NumberPlane(x_range=[-1, 1, 0.25], y_range=[-1, 1, 0.25], x_length=1.4, y_length=1.4,
                           background_line_style={"stroke_color": C.BITS, "stroke_width": 1})
        grid.apply_function(lambda p: p + 0.15 * np.array([math.sin(2 * p[1]), math.sin(2 * p[0]), 0]))
        fams = Group()
        for pic, t, col in ((ar, r"one pixel at a time", WHITE), (vae, r"through a code: \ VAEs", C.EMBED),
                            (gan, r"a game: \ GANs", C.PROB), (grid, r"bend space: \ flows", C.BITS)):
            fams.add(Group(pic, label(t, font_size=22, color=col).next_to(pic, DOWN, buff=0.3)))
        fams.arrange(RIGHT, buff=0.9).move_to(DOWN * 0.2)
        tag = schematic_tag(corner=DR)
        with self.voiceover(
            "Next time, the fourth act begins: generation. Before diffusion, there were four ways to make a model "
            "that invents: one pixel at a time, through a learned code, as a game between two networks, or by "
            "bending space itself. Part 20: four ways to generate."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            self.play(LaggedStart(*[FadeIn(f_, shift=UP * 0.2) for f_ in fams], lag_ratio=0.5),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        card = reference_card(
            [r"J.~L.~Hennessy \& D.~A.~Patterson, \textit{Computer Architecture: A Quantitative Approach}, 6th ed.\ "
             r"(2017)",
             r"R.~M.~Gray \& D.~L.~Neuhoff, \textit{Quantization}, IEEE Trans.\ Information Theory (1998), a survey"],
            [r"Pope et al.\ (2022); \ Yu et al., \textit{Orca} (2022); \ Kwon et al., \textit{vLLM} (2023); \ Zheng et "
             r"al., \textit{SGLang} (2023); \ Agrawal et al., \textit{Sarathi-Serve} (2024); \ Zhong et al., "
             r"\textit{DistServe} (2024); \ Patel et al., \textit{Splitwise} (2024)",
             r"Shazeer (2019); \ Ainslie et al., \textit{GQA} (2023); \ DeepSeek-AI, V2, V3 (2024), V3.2 (2025); \ "
             r"Gemma Team (2025); \ OpenAI, \textit{gpt-oss} (2025)",
             r"Stern, Shazeer \& Uszkoreit (2018); \ Leviathan, Kalman \& Matias (2022); \ Chen et al.\ (2023); \ Cai "
             r"et al., \textit{Medusa} (2024); \ Li et al., \textit{EAGLE} (2024), \textit{EAGLE-3} (2025)",
             r"Bennett (1948); \ LeCun, Denker \& Solla (1990); \ Hassibi \& Stork (1993); \ Dettmers et al., "
             r"\textit{LLM.int8()} (2022); \ Frantar et al., \textit{GPTQ} (2022); \ Xiao et al., \textit{SmoothQuant} "
             r"(2022); \ Lin et al., \textit{AWQ} (2023)",
             r"Ashkboos et al., \textit{QuaRot} (2024); \ Liu et al., \textit{SpinQuant} (2024); \ Rouhani et al., "
             r"\textit{MX} (2023); \ NVIDIA, \textit{NVFP4} (2025); \ Liu et al., \textit{KIVI} (2024)",
             r"Milakov \& Gimelshein (2018); \ Dao et al., \textit{FlashAttention} (2022); \ Dao (2023); \ Shah et al.\ "
             r"(2024); \ Dao, Haziza, Massa \& Sizov, \textit{Flash-Decoding} (2023)",
             r"Willard \& Louf (2023); \ Dong et al., \textit{XGrammar} (2024); \ Park et al.\ (2024); \ Cottier et "
             r"al., Epoch AI (2025); \ Apple (2025); \ DeepSeek-AI, \textit{R1-0528} (2025)"])
        credit = note(narration_credit(), font_size=18).to_edge(DOWN, buff=0.15)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.15:
            card.shift(UP * (credit.get_top()[1] + 0.15 - card.get_bottom()[1]))
        with self.voiceover(
            "To go further, the vLLM and FlashAttention papers are good places to start. Thanks for watching, and "
            "see you in Part 20."
        ):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(1.5)
        self.clear_scene()
