from __future__ import annotations

import math

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai14.common import (CONTEXT, C_COL, DECODER, ENCDEC, ENCODER, OPEN, PART, PRIOR, F, arch_diagram,
                                   load, node_box)


class Outro(VoiceoverScene):
    def construct(self):
        self.family_tree()
        self.recap()
        self.payoffs()
        self.problems()
        self.next_time()
        self.references()


    # ------------------------------------------------------------------
    def family_tree(self):
        """The lineage on one page: time left to right, one lane per branch or lab (schematic)."""
        X = lambda t: -5.9 + (t - 2017.0) * 1.25  # noqa: E731
        lanes = {"encoder": 2.75, "encdec": 1.9, "openai": 1.05, "meta": 0.2, "mistral": -0.65, "deepseek": -1.5,
                 "kimi": -2.35, "qwen": -3.2}
        lane_of = dict(transformer="encdec", t5="encdec", t0="encdec", bert="encoder", roberta="encoder",
                       electra="encoder", llama="meta", llama2="meta", llama3="meta", mistral="mistral",
                       mixtral="mistral", dsv3="deepseek", dsv4="deepseek", qwen3="qwen", qwen35="qwen",
                       kimik2="kimi", kimik3="kimi")
        names = {"openai": r"OpenAI", "meta": r"Meta", "mistral": r"Mistral AI", "deepseek": r"DeepSeek",
                 "kimi": r"Moonshot (Kimi)", "qwen": r"Alibaba (Qwen)"}
        arch_col = {"encoder": ENCODER, "encdec": ENCDEC, "decoder": DECODER}
        rows = [r for r in F.TREE if r[0] != "r1"]
        pos, nodes, labels, seen = {}, {}, {}, {}
        for key, name, t, arch, open_, parent in rows:
            lane = lane_of.get(key, "openai")
            p = np.array([X(t), lanes[lane], 0.0])
            pos[key] = p
            col = arch_col[arch]
            d = (Dot(p, radius=0.085, color=col) if open_ else
                 Circle(radius=0.085, stroke_color=col, stroke_width=2.5, fill_color=BLACK, fill_opacity=1).move_to(p))
            nodes[key] = d
            k = seen.get(lane, 0)
            seen[lane] = k + 1
            txt = r"DeepSeek-V3, R1" if key == "dsv3" else name
            lb = label(txt, font_size=17, color=GREY_A)
            if key == "transformer":
                lb.next_to(d, LEFT, buff=0.12)
            else:
                lb.next_to(d, UP if k % 2 == 0 else DOWN, buff=0.08)
            labels[key] = lb
        edges = {}
        prev = {}
        for key, name, t, arch, open_, parent in rows:
            lane = lane_of.get(key, "openai")
            col = arch_col[arch]
            if lane in prev:  # same lane: a straight line from the lab's previous model
                a, b = pos[prev[lane]], pos[key]
                edges[key] = Line(a + RIGHT * 0.085, b + LEFT * 0.085, color=col, stroke_width=2.5, stroke_opacity=0.7)
            elif parent is not None:  # a new lane: down (or up) from the model it built on, then along
                a, b = pos[parent], pos[key]
                corner = np.array([a[0], b[1], 0.0])
                e = VMobject(stroke_color=col, stroke_width=2.5, stroke_opacity=0.7)
                start = a + (DOWN if b[1] < a[1] else UP) * 0.085
                e.set_points([start, corner, corner, b + LEFT * 0.085])
                edges[key] = e
            prev[lane] = key
        lane_names = VGroup(*[label(nm, font_size=17, color=GREY_B).move_to([-6.5, lanes[k], 0], aligned_edge=LEFT)
                              for k, nm in names.items()])
        ends = VGroup(label(r"encoders", font_size=20, color=ENCODER).next_to(nodes["electra"], RIGHT, buff=0.35),
                      label(r"encoder-decoders", font_size=20, color=ENCDEC).next_to(nodes["t0"], RIGHT, buff=0.35))
        years = VGroup(Line([X(2017.0), 3.35, 0], [X(2026.8), 3.35, 0], color=GREY_D, stroke_width=1.5))
        for y in range(2017, 2027):
            years.add(Line([X(y), 3.3, 0], [X(y), 3.4, 0], color=GREY_D, stroke_width=1.5),
                      label(str(y), font_size=17, color=GREY_B).move_to([X(y + 0.5), 3.6, 0]))
        lg = VGroup(
            VGroup(Dot(radius=0.085, color=GREY_A), label(r"open weights", font_size=18, color=GREY_A)).arrange(RIGHT, buff=0.15),
            VGroup(Circle(radius=0.085, stroke_color=GREY_A, stroke_width=2.5), label(r"closed", font_size=18,
                                                                                         color=GREY_A)).arrange(RIGHT, buff=0.15),
        ).arrange(RIGHT, buff=0.5).move_to([4.6, 2.75, 0])
        sch = note(r"schematic: \ a line joins a model to its lab's previous one, or to the published design it built on")
        sch.to_corner(DL, buff=0.2)

        def show(keys):
            anims = []
            for k_ in keys:
                if k_ in edges:
                    anims.append(Create(edges[k_]))
                anims += [FadeIn(nodes[k_], scale=1.5), FadeIn(labels[k_])]
            return anims

        first = ["transformer"]
        branches = ["bert", "roberta", "electra", "t5", "t0", "gpt1", "gpt2"]
        scale_up = ["gpt3", "codex", "instructgpt", "chatgpt", "gpt4"]
        open_ = ["llama", "llama2", "llama3", "mistral", "mixtral"]
        china = ["dsv3", "dsv4", "kimik2", "kimik3", "qwen3", "qwen35", "gptoss"]
        assert {r[0] for r in rows} == set(first + branches + scale_up + open_ + china)
        with self.voiceover(
            "Before the recap, here is the whole lineage on one page, with time running left to right. "
            "<bookmark mark='a'/> In 2017, the Transformer: an encoder and a decoder, built to translate. "
            "<bookmark mark='b'/> Within two years it had split into three branches: encoders, like BERT, which won "
            "the benchmarks; encoder-decoders, like T5; and decoders, like GPT. <bookmark mark='c'/> The decoder "
            "branch scaled: GPT-3, Codex, InstructGPT, ChatGPT, GPT-4. And as it scaled, it closed. "
            "<bookmark mark='d'/> From 2023, open lanes appear beside it: Meta's LLaMA, then Mistral, each built on "
            "the published designs before it. <bookmark mark='e'/> Then DeepSeek, Moonshot's Kimi, Alibaba's Qwen, "
            "and even OpenAI again, with open weights. <bookmark mark='f'/> Every open model at today's frontier is a "
            "decoder. The encoders live on, in search and classification, but the frontier grew from one branch."
        ) as vo:
            self.play(FadeIn(years), FadeIn(sch), FadeIn(lg))
            vo.wait_until("a")
            self.play(*show(first))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(*show([k_])) for k_ in branches], lag_ratio=0.4),
                      FadeIn(ends), run_time=3.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(*show([k_])) for k_ in scale_up], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("d")
            self.play(LaggedStart(*[AnimationGroup(*show([k_])) for k_ in open_], lag_ratio=0.5),
                      FadeIn(VGroup(*lane_names[1:3])), FadeIn(lane_names[0]), run_time=3.0)
            vo.wait_until("e")
            self.play(LaggedStart(*[AnimationGroup(*show([k_])) for k_ in china], lag_ratio=0.4),
                      FadeIn(VGroup(*lane_names[3:])), run_time=3.5)
            vo.wait_until("f")
            dec = [k_ for k_, n_, t_, a_, o_, p_ in rows if a_ == "decoder" and o_ and t_ > 2024.9]
            self.play(*[Indicate(nodes[k_], color=YELLOW, scale_factor=1.8) for k_ in dec])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tiles(self):
        TW, TH = 3.0, 2.0
        out = []
        # 1. the Transformer
        out.append((arch_diagram("encdec", 0.8, label_on=False), r"2017: \ the Transformer", ENCDEC))
        # 2. masked against left to right (BERT's Table 5)
        ab = F.BERT["ablation"]
        g = VGroup()
        for k, (_, m, l_) in enumerate(ab):
            g.add(Rectangle(width=0.18, height=1.6 * (m - 70) / 25, stroke_width=0, fill_color=ENCODER,
                            fill_opacity=0.9).move_to([0.6 * k - 0.1, 0, 0], aligned_edge=DOWN),
                  Rectangle(width=0.18, height=1.6 * (l_ - 70) / 25, stroke_width=0, fill_color=DECODER,
                            fill_opacity=0.9).move_to([0.6 * k + 0.1, 0, 0], aligned_edge=DOWN))
        out.append((g, r"masked beats left to right", ENCODER))
        # 3. 6ND
        P = load("published")
        out.append((VGroup(MathTex(r"C \approx 6ND", font_size=44, color=C_COL),
                           MathTex(sci(P["gpt3_6nd"], 1) + r"\ \text{FLOP}", font_size=30)).arrange(DOWN, buff=0.2),
                    r"GPT-3's compute", C_COL))
        # 4. learning in context: LAMBADA zero, one, few
        lam = F.GPT3["lambada"]
        g4 = VGroup(*[Rectangle(width=0.45, height=1.7 * v / 100, stroke_width=0,
                                fill_color=interpolate_color(ManimColor(GREY_B), ManimColor(CONTEXT), k / 2),
                                fill_opacity=0.9).move_to([0.65 * k, 0, 0], aligned_edge=DOWN)
                      for k, v in enumerate((lam["zero"], lam["one"], lam["few"]))])
        out.append((g4, r"learning in context", CONTEXT))
        # 5. the recipe converges: the convergence matrix in miniature
        from videos.ai.ai14.s11_converge import COLS, MATRIX, WIN

        m = VGroup()
        for i, key in enumerate(MATRIX):
            c = F.CFG[key]
            for j, (f, _) in enumerate(COLS):
                won = c.get(f) in WIN[f]
                m.add(Square(0.16, stroke_width=0, fill_color=C.REWARD if won else GREY_D,
                             fill_opacity=0.9 if won else 0.5).move_to([0.2 * j, -0.17 * i, 0]))
        out.append((m, r"the recipe converges", C.REWARD))
        # 6. sparse: active share of parameters
        sh = P["active_share"]
        g6 = VGroup(*[Rectangle(width=0.3, height=max(1.6 * sh[k] * 4, 0.03), stroke_width=0, fill_color=OPEN,
                                fill_opacity=0.9).move_to([0.42 * i, 0, 0], aligned_edge=DOWN)
                      for i, k in enumerate(("dsv3", "qwen3", "kimik2", "gptoss", "qwen35", "dsv4", "kimik3"))])
        out.append((g6, r"a sparse frontier", OPEN))
        # 7. compute growth: Epoch's frontier models and the fit
        E = load("epoch")
        f = E["frontier"]
        ax = Axes(x_range=[2017, 2026.5, 3], y_range=[18, 27.5, 3], x_length=TW * 0.9, y_length=TH * 0.85, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False})
        g7 = VGroup(ax, *[Dot(ax.c2p(a, b), radius=0.03, color=C_COL) for a, b in zip(f["x"], f["y"])],
                    Line(ax.c2p(2017.3, f["icept"] + f["slope"] * -2.7), ax.c2p(2026.4, f["icept"] + f["slope"] * 6.4),
                         color=WHITE, stroke_width=2))
        out.append((g7, rf"compute: \ ${f['per_year']:.1f}\times$ a year", C_COL))
        # 8. ours: the cloze test
        L = load("lineage")
        g8 = VGroup(*[Rectangle(width=0.55, height=max(1.7 * v, 0.03), stroke_width=0, fill_color=c, fill_opacity=0.9)
                      .move_to([0.8 * k, 0, 0], aligned_edge=DOWN)
                      for k, (v, c) in enumerate(((L["cloze_gpt_left"], PRIOR), (L["cloze_gpt"], DECODER),
                                                  (L["cloze_bert"], ENCODER)))])
        out.append((g8, r"our GPT against BERT", DECODER))
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
            "Let's take stock. In 2017 a translation model made attention the whole architecture. In 2018, pretraining "
            "on raw text, then fine-tuning, became the recipe, and masked models like BERT won the benchmarks of the "
            "day. Then the decoder scaled: GPT-2 did tasks it was never trained for, and GPT-3, at three times ten to "
            "the twenty-three operations, learned from examples in its prompt. Instruction tuning and human feedback "
            "turned it into ChatGPT. Open models converged on one recipe, then grew sparse and began to diverge "
            "again, while compute grew about five times a year. And on our own small models, at equal compute, we "
            "measured what each objective buys."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.15, scale=0.95) for t_ in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"the KV cache, latent attention, hybrids", [15]),
            (r"mixtures of experts, sparse attention", [16]),
            (r"the hardware that made scale possible", [17]),
            (r"data, parallelism, precision at scale", [18]),
            (r"serving: \ 4-bit weights, speculative decoding", [19]),
            (r"instruction tuning, RLHF, DPO", [27]),
            (r"reasoning with reinforcement learning", [28]),
        ], font_size=24)
        with self.voiceover(
            "All of this comes back. The memory of past tokens, latent attention and hybrids are Part 15. Mixtures of "
            "experts and sparse attention, Part 16. The hardware that made scale possible, Part 17, and how a "
            "frontier run is actually organized, Part 18. Serving these models cheaply, Part 19. Instruction tuning "
            "and human feedback, built on our own model, Part 27; and reasoning, Part 28."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"Show that a decoder layer with a feed-forward width of $4d$ has $12d^2$ weights (ignoring norms and "
            r"biases). \ With $L = 96$, $d = 12{,}288$, a vocabulary of $50{,}257$ and $2{,}048$ positions, check "
            r"GPT-3's $174.6$ billion.",
            r"Argue that training costs about $6$ operations per parameter per token, two forward and four backward. "
            r"\ Compute GPT-3's $C \approx 6ND$ with $D = 300$ billion, in operations and in petaflop/s-days.",
            r"A SwiGLU feed-forward network has three $d \times h$ matrices. \ For which $h$ does it match a ReLU "
            r"network of width $4d$? \ Find $h$ for $d = 4096$, rounded up to a multiple of $256$.",
            r"Show that the KV cache costs $4 L\, n_{\mathrm{kv}}\, d_{\mathrm{head}}$ bytes per token in 16-bit "
            r"numbers. \ For Llama 3.1 405B ($L = 126$, $d_{\mathrm{head}} = 128$), compare $8$ and $128$ key-value "
            r"heads at $131{,}072$ tokens.",
            r"A masked model predicts a fraction $m$ of the positions. \ How many targets per sequence of $n$ does it "
            r"get, against a causal model? \ What does an equal-compute comparison hold fixed, and what not?",
            r"If training compute grows $4.5\times$ a year and cost $2.4\times$, find the doubling time of compute in "
            r"months, its growth over a decade, and the yearly gain in operations per dollar.",
        ], font_size=22)
        with self.voiceover(
            "Here are six problems to try, from counting GPT-3's parameters to the trends of the last chapter. Pause "
            "here, and work through them; full solutions are in this part's notes."
        ) as vo:
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows], lag_ratio=0.3),
                      run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        P = load("published")
        head = label(r"Next: \ Part 15, \ Memory", font_size=40).to_edge(UP, buff=0.5)
        ctx = np.array([1, 4, 16, 64, 128])
        bars = VGroup()
        for k, c in enumerate(ctx):
            gb = P["kv_llama3_gqa"] * c * 1024 / 1e9
            h = 2.6 * math.log10(1 + gb) / math.log10(1 + P["kv_llama3_gqa"] * 128 * 1024 / 1e9)
            b = Rectangle(width=0.55, height=max(h, 0.03), stroke_width=0, fill_color=C.KEY, fill_opacity=0.85)
            b.move_to([-5.4 + 0.85 * k, -2.0, 0], aligned_edge=DOWN)
            t = label(rf"{c}K", font_size=18, color=GREY_B).next_to(b, DOWN, buff=0.1)
            bars.add(VGroup(b, t))
        bl = label(r"a cache that grows with every token", font_size=22, color=C.KEY).next_to(bars, UP, buff=0.3)
        mem = Square(1.6, stroke_color=C.MEMORY, stroke_width=3, fill_color=C.MEMORY, fill_opacity=0.15)
        mem.move_to([3.6, -1.2, 0])
        ml = label(r"or a memory of fixed size?", font_size=22, color=C.MEMORY).next_to(mem, UP, buff=0.3)
        body = VGroup(
            label(r"KV caches, \ grouped-query and latent attention", font_size=26, color=WHITE),
            label(r"linear attention, \ the delta rule, \ state-space models, \ hybrids", font_size=26, color=WHITE),
        ).arrange(DOWN, buff=0.25).move_to(UP * 1.6)
        sch = note(r"schematic: \ Llama 3.1 405B's cache, log scale").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Next time: memory. A model reading a million tokens has to keep something of every one of them. "
            "<bookmark mark='a'/> Grouped-query and latent attention shrink the cache that grows with every token; "
            "<bookmark mark='b'/> linear attention, the delta rule and state-space models replace it with a memory "
            "of fixed size; and the hybrids of this part's frontier mix the two. That is Part 15."
        ) as vo:
            self.play(FadeIn(head), FadeIn(body))
            vo.wait_until("a")
            self.play(FadeIn(bl), LaggedStart(*[GrowFromEdge(b[0], DOWN) for b in bars], lag_ratio=0.2),
                      FadeIn(VGroup(*[b[1] for b in bars])), FadeIn(sch))
            vo.wait_until("b")
            self.play(FadeIn(mem), FadeIn(ml))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        card = reference_card(
            [r"D.~Jurafsky \& J.~H.~Martin, \textit{Speech and Language Processing}, 3rd ed.\ draft, chapters on "
             r"Transformers and large language models",
             r"S.~Raschka, \textit{Build a Large Language Model (From Scratch)} (2024)",
             r"S.~J.~D.~Prince, \textit{Understanding Deep Learning} (2023), ch.~12"],
            [r"Vaswani et al.\ (2017); \ Howard \& Ruder (2018); \ Peters et al.\ (2018); \ Radford et al.\ (2018, "
             r"2019); \ Devlin et al.\ (2018)",
             r"Wang et al., GLUE (2018), SuperGLUE (2019); \ Liu et al., RoBERTa (2019); \ Clark et al., ELECTRA "
             r"(2020); \ Raffel et al., T5 (2019)",
             r"Kaplan et al.\ (2020); \ Brown et al., GPT-3 (2020); \ Zhao et al.\ (2021); \ Hoffmann et al., "
             r"Chinchilla (2022); \ Wang et al.\ (2022)",
             r"Chen et al., Codex (2021); \ Wei et al., FLAN (2021); \ Sanh et al., T0 (2021); \ Ouyang et al.\ (2022); "
             r"\ OpenAI, GPT-4 (2023)",
             r"Touvron et al., LLaMA, Llama 2 (2023); \ Jiang et al., Mistral, Mixtral (2023--24); \ Llama Team (2024); "
             r"\ Chowdhery et al., PaLM (2022)",
             r"Shazeer (2019, 2020); \ Zhang \& Sennrich (2019); \ Xiong et al.\ (2020); \ Su et al., RoPE (2021); \ "
             r"Ainslie et al., GQA (2023)",
             r"DeepSeek-AI, V2, V3, R1 (2024--25); \ Qwen Team (2025); \ Kimi Team (2025); \ GLM-4.5 Team (2025); \ "
             r"OpenAI, gpt-oss (2025)",
             r"model cards: \ Qwen3.5, GLM-5, DeepSeek-V4, Kimi K3, MiMo-V2.6 (2026); \ Epoch AI (2024); \ Cottier et al.\ "
             r"(2024)"])
        credit = note(narration_credit(), font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "The history in this part is best read in the papers themselves, most of them short and clear. Thanks for "
            "watching, and see you in Part 15."
        ):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(1.5)
        self.clear_scene()
