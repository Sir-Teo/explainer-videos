from __future__ import annotations

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai13.common import (A, K, OURS, PART, POS, POS_COLORS, Q, SINK_COLORS, V, curve, framed, heat_image,
                                   load, seed_lines)


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
            return Axes(x_range=xr, y_range=yr, x_length=TW, y_length=TH - 0.2, tips=False,
                        axis_config={"stroke_color": GREY_D, "include_ticks": False})

        out = []
        # 1. the kernel smoother
        s = load("smoother")
        x, y, xs = np.asarray(s["x"]), np.asarray(s["y"]), np.asarray(s["xs"])
        a1 = plane([0, x[-1], 10], [0, y.max(), 1])
        out.append((VGroup(*[Dot(a1.c2p(a, b), radius=0.018, color=V) for a, b in zip(x, y)],
                           curve(a1, xs, np.asarray(s["fit2.5"]), Q, 2.5, smooth=True)), r"a weighted average", Q))
        # 2. Hopfield's capacity
        h = load("hopfield")
        Ms = np.log10(np.asarray(h["Ms"], float))
        a2 = plane([Ms[0], Ms[-1], 1], [0, 1.05, 0.5])
        out.append((VGroup(a2, curve(a2, Ms, np.asarray(h["classical"]), C.SURPRISE, 2.5),
                           curve(a2, Ms, np.asarray(h["modern"]), A, 3)), r"a memory that recalls", A))
        # 3. our transformer's heads
        t = load("tf")
        maps = np.asarray(t["maps"])
        out.append((Group(*[heat_image(maps[1, hh], 0.9, 0.9, mask_upper=True) for hh in range(3)]).arrange(RIGHT, buff=0.08),
                    rf"our transformer: \ ${float(t['passage_bits']):.2f}$ bits", OURS))
        # 4. heads as low-rank maps
        hd = load("heads")
        sv = np.asarray(hd["sv_qk"])
        a4 = plane([0, sv.shape[-1], 32], [-17, 1, 4])
        g4 = VGroup(a4)
        for l_ in range(sv.shape[0]):
            for hh in range(sv.shape[1]):
                g4.add(curve(a4, np.arange(1, sv.shape[-1] + 1), np.log10(np.maximum(sv[l_, hh] / sv[l_, hh, 0], 1e-17)),
                             A, 1.2).set_stroke(opacity=0.6))
        out.append((g4, r"heads are low-rank", A))
        # 5. positions, side by side
        p = load("positions")
        R = int(dict(p["cfg"])["read"])
        nb = np.asarray(p["bucket_rope"]).shape[1]
        bx = np.arange(nb) * (R / nb) + R / nb / 2
        allv = np.concatenate([np.asarray(p[f"bucket_{m}"]).ravel() for m in POS_COLORS])
        a5 = plane([0, R, 128], [allv.min() - 0.1, min(allv.max(), allv.min() + 4) + 0.1, 1])
        g5 = VGroup(a5, *[curve(a5, bx, np.clip(np.asarray(p[f"bucket_{m}"]).mean(0), allv.min(), allv.min() + 4),
                                POS_COLORS[m], 2.5) for m in POS_COLORS])
        out.append((g5, r"positions, past the length", POS))
        # 6. sinks
        sk = load("sinks")  # each design's weight on <s> with nothing to copy, during training (mean of the seeds)
        hs = {v: np.asarray(sk[f"{v}_hist"], float) for v in SINK_COLORS}
        hx6 = hs["softmax"][0, :, 0]
        a6 = plane([0, float(hx6[-1]), 500], [0, max(0.6, max(float(h_[:, :, 3].mean(0).max()) for h_ in hs.values())), 0.2])
        g6 = VGroup(a6, *[curve(a6, hx6, hs[v][:, :, 3].mean(0), c_, 2.5) for v, c_ in SINK_COLORS.items()])
        out.append((g6, r"sinks, and ways out", C.SINK))
        # 7. induction heads forming
        d = load("induction")
        c2 = np.asarray(d["curve2"])
        a7 = plane([0, c2[-1, 0], 1000], [0, float(c2[:, 1].max()) + 0.3, 1])
        out.append((VGroup(a7, curve(a7, np.asarray(d["curve1"])[:, 0], np.asarray(d["curve1"])[:, 1], GREY_B, 2),
                           curve(a7, c2[:, 0], c2[:, 1], A, 3)), r"induction heads", A))
        # 8. a program in weights
        r = load("rasp")
        out.append((Group(heat_image(np.asarray(r["sort_A1"]), 1.25, 1.25, color=A, gamma=1.0),
                          heat_image(np.asarray(r["sort_A2"]), 1.25, 1.25, color=A, gamma=1.0)).arrange(RIGHT, buff=0.2),
                    r"a program in weights", Q))
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
        head = label(rf"Part {PART}, \ in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        t = load("tf")
        with self.voiceover(
            "Let's take stock. Attention is a weighted average, Nadaraya and Watson's smoother with a learned "
            "kernel, and a memory read, one step of a modern Hopfield network. Dividing by the square root of d "
            "keeps its softmax from collapsing. Heads compare and move along a few directions, the mask decides who "
            "sees whom, and a block costs twelve d squared weights plus a term that grows with the context. Our "
            f"transformer reached {float(t['passage_bits']):.2f} bits a character. Positions can be added, rotated, "
            "penalized or left out, and stretched with care. Sink logits and gates give the softmax somewhere to "
            "park, and trained heads find algorithms: copying, a step of gradient descent, programs, within limits "
            "that only more steps of thought remove."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.15, scale=0.95) for t_ in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"the models built on this block", [14]),
            (r"keys and values kept: \ the cache, \ MLA, \ linear memories", [15, 19]),
            (r"attention to only some of the past", [16]),
            (r"long context in training; \ QK-norm", [18]),
            (r"FlashAttention, \ and serving long contexts", [19]),
            (r"chains of thought, \ beyond fixed depth", [28]),
            (r"heads and circuits, \ taken apart", [30]),
        ], font_size=24)
        with self.voiceover(
            "This comes back everywhere: the models built on this block in Part 14; the memory of keys and values "
            "in Part 15; attending to only some of the past in Part 16; long contexts and runaway logits in Part "
            "18; fast serving in Part 19; thinking past a fixed depth in Part 28; and circuits in real models in "
            "Part 30."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"If the entries of $q$ and $k$ are independent with mean $0$ and variances $\sigma_q^2$ and $\sigma_k^2$, "
            r"show that $\operatorname{Var}(q \cdot k) = d\,\sigma_q^2 \sigma_k^2$. \ What should the score be divided by?",
            r"Let $R_m$ rotate each pair of a vector by $m\theta_j$. \ Show $(R_m q)\cdot(R_n k)$ depends only on $n - m$, "
            r"and that ALiBi's bias $-m_h (i - j)$ has the same property.",
            r"Show that a pre-norm block with an MLP of width $4d$ has $12 d^2 + 9d$ parameters, and that attention's "
            r"$2LTd$ operations per token equal the weights' $24 L d^2$ at $T = 12d$.",
            r"A head has a sink logit $b$ and $n$ keys with equal scores $s$. \ What share of its attention goes "
            r"nowhere? \ For which $b$ is it one half?",
            r"Show that the modern Hopfield update $\xi \leftarrow X^\top \operatorname{softmax}(\beta X \xi)$ tends to "
            r"the stored pattern of largest overlap as $\beta \to \infty$, and to the average pattern as $\beta \to 0$.",
            r"Show that one step of gradient descent from $w = 0$ on $\tfrac{1}{2N}\sum_i (w\cdot x_i - y_i)^2$ "
            r"predicts $\hat y = \tfrac{\eta}{N}\sum_i y_i\, (x_i \cdot x_q)$: \ linear attention.",
        ], font_size=21)
        with self.voiceover(
            "Here are six problems to try, from the variance of a dot product to gradient descent written as "
            "attention. Pause here and work through them; full solutions are in this part's notes."
        ) as vo:
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows], lag_ratio=0.3),
                      run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 14, \ The Language-Model Lineage", font_size=40).to_edge(UP, buff=0.4)
        models = [(2017, r"Transformer"), (2018, r"GPT-1, \ BERT"), (2019, r"GPT-2"), (2020, r"GPT-3"),
                  (2022, r"ChatGPT"), (2023, r"LLaMA"), (2025, r"DeepSeek-R1"), (2026, r"Kimi K3")]
        xs = np.linspace(-5.8, 5.8, len(models))
        line = Line([-6.4, -0.6, 0], [6.4, -0.6, 0], color=GREY_C, stroke_width=2)
        nodes = VGroup()
        for i, ((yr, nm), x) in enumerate(zip(models, xs)):
            hgt = 0.35 + 0.33 * i
            bar = Rectangle(width=0.55, height=hgt, stroke_width=0, fill_color=C.NEURAL, fill_opacity=0.25 + 0.08 * i)
            bar.move_to([x, -0.6 + hgt / 2, 0])
            nodes.add(VGroup(bar, label(str(yr), font_size=20, color=GREY_B).next_to([x, -0.6, 0], DOWN, buff=0.15),
                             label(nm, font_size=18, color=WHITE).next_to(bar, UP, buff=0.1)))
        tag = note(r"schematic: \ heights only suggest growth").to_corner(DR, buff=0.25)
        sub = label(r"the same block, \ scaled, \ pretrained, \ instructed: \ how today's models came to be",
                    font_size=24, color=GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Next time: the lineage. The block we built today, stacked and scaled from a translation model in 2017 "
            "to GPT-3, ChatGPT and the open-weight frontier of 2026; and our own GPT-style and BERT-style models, "
            "trained side by side on the novels."
        ) as vo:
            self.play(FadeIn(head), Create(line), FadeIn(tag))
            self.play(LaggedStart(*[FadeIn(n_, shift=UP * 0.1) for n_ in nodes], lag_ratio=0.3), FadeIn(sub),
                      run_time=max(3.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        books = [
            r"S.~J.~D.~Prince, \textit{Understanding Deep Learning} (2023), chapter 12",
            r"D.~Jurafsky \& J.~H.~Martin, \textit{Speech and Language Processing} (3rd ed.\ draft), chapters 9--10",
        ]
        papers = [
            r"Nadaraya (1964); \ Watson (1964); \ Hopfield (1982); \ Amit, Gutfreund \& Sompolinsky (1985); \ Krotov \& "
            r"Hopfield (2016); \ Ramsauer et al., \textit{Hopfield Networks is All You Need} (2020)",
            r"Bahdanau, Cho \& Bengio (2014); \ Vaswani et al., \textit{Attention Is All You Need} (2017); \ Elhage et al.\ "
            r"(2021); \ Bhojanapalli et al.\ (2020); \ Kaplan et al.\ (2020)",
            r"Shaw et al.\ (2018); \ Su et al., \textit{RoFormer} (2021); \ Press et al., ALiBi (2021); \ Haviv et al.\ "
            r"(2022); \ Kazemnejad et al.\ (2023); \ Barbero et al.\ (2024)",
            r"Chen et al.\ (2023); \ bloc97 (2023); \ Peng et al., \textit{YaRN} (2023); \ Chiang \& Cholak (2022)",
            r"Xiao et al., \textit{Attention Sinks} (2023); \ Guo et al.\ (2024); \ Qiu et al., \textit{Gated Attention} "
            r"(2025); \ Ye et al., \textit{Differential Transformer} (2024); \ OpenAI, gpt-oss (2025)",
            r"Dehghani et al.\ (2023); \ Gemma Team (2024, 2025); \ Olsson et al., \textit{Induction Heads} (2022); \ "
            r"von Oswald et al.\ (2023); \ Garg et al.\ (2022)",
            r"Weiss et al., \textit{Thinking Like Transformers} (2021); \ Lindner et al., \textit{Tracr} (2023); \ "
            r"Merrill \& Sabharwal (2023, 2024); \ Merrill, Petty \& Sabharwal (2024); \ Zhou et al.\ (2023)",
        ]
        card = reference_card(books, papers, font_size=19)
        data = note(r"Text: Project Gutenberg (Part 1's $30$ novels). \ Every model here is trained by this part's "
                    r"code; \ every number on screen is computed or cited.", font_size=18).to_edge(DOWN, buff=0.2)
        credit = note(rf"Animated with Manim Community; \ narrated by {narration_credit()}.", font_size=18)
        credit.next_to(data, UP, buff=0.08)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.12:
            card.scale((card.height - (credit.get_top()[1] + 0.12 - card.get_bottom()[1])) / card.height)
            card.next_to(credit, UP, buff=0.12)
        with self.voiceover(
            "Anthropic's 'Mathematical Framework for Transformer Circuits' is the best next read. Thanks for "
            "watching, and see you in Part 14."
        ):
            self.play(LaggedStart(FadeIn(card), FadeIn(credit), FadeIn(data), lag_ratio=0.3), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)))
