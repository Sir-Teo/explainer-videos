from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.rl.common import Mono, Plot, bar_rows, label, load, mtex, part_card, real_tag, schematic_tag


class Mismatch(VoiceoverScene):
    def construct(self):
        self.m = load("mismatch")
        seqs = self.m["seqs"]
        self.d32 = [np.array(s["lp_fp32"]) - np.array(s["lp_sampler"]) for s in seqs]
        self.d16 = [np.array(s["lp_bf16"]) - np.array(s["lp_sampler"]) for s in seqs]
        self.lp = [np.array(s["lp_sampler"]) for s in seqs]
        self.card()
        self.two_engines()
        self.per_token()
        self.per_sequence()
        self.fixes()
        self.async_()

    def card(self):
        c = part_card(5, r"RL at scale", r"off-policy data, compute, and the reward itself")
        self.play(FadeIn(c, shift=UP * 0.2))
        self.wait(1.6)
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def two_engines(self):
        def box(t, sub, col, w=5.6):
            r = RoundedRectangle(width=w, height=1.6, corner_radius=0.15, stroke_color=col, fill_color=col, fill_opacity=0.12)
            a = label(t, font_size=30).move_to(r).shift(UP * 0.25)
            b = label(sub, font_size=21, color=GREY_A).next_to(a, DOWN, buff=0.12)
            return VGroup(r, a, b)
        inf = box(r"inference engine", r"vLLM, SGLang: fast kernels, bf16, batching", C.OLD_POLICY).move_to(LEFT * 3.3 + UP * 0.4)
        trn = box(r"trainer", r"FSDP, Megatron: different kernels, other precision", C.RL_POLICY).move_to(RIGHT * 3.3 + UP * 0.4)
        w = label(r"the same weights $\theta$", font_size=28, color=YELLOW).move_to(UP * 2.4)
        a1 = Arrow(w.get_bottom(), inf.get_top(), buff=0.1, color=YELLOW, stroke_width=3)
        a2 = Arrow(w.get_bottom(), trn.get_top(), buff=0.1, color=YELLOW, stroke_width=3)
        p1 = mtex(r"\pi_{\text{sampler}}(y_t)", font_size=36, color=C.OLD_POLICY).next_to(inf, DOWN, buff=0.35)
        p2 = mtex(r"\pi_{\text{learner}}(y_t)", font_size=36, color=C.RL_POLICY).next_to(trn, DOWN, buff=0.35)
        neq = mtex(r"\neq", font_size=48).move_to((p1.get_center() + p2.get_center()) / 2)
        cap = label(r"a ratio that ``should'' be exactly 1 isn't", font_size=28, color=GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "At scale, generation and training run in different software. An inference engine like vLLM writes the "
            "answers, with kernels tuned for speed. A training framework computes the gradients, with different "
            "kernels and often different precision. <bookmark mark='p'/> They hold the same weights, but they don't "
            "compute the same probabilities. So even a perfectly on-policy algorithm is quietly off-policy, and the "
            "importance ratio that should be exactly one isn't."
        ) as vo:
            self.play(FadeIn(w), FadeIn(inf), FadeIn(trn), GrowArrow(a1), GrowArrow(a2), FadeIn(schematic_tag()))
            vo.wait_until("p")
            self.play(FadeIn(p1), FadeIn(p2), FadeIn(neq))
            self.play(FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def per_token(self):
        d = np.concatenate(self.d32)
        d16 = np.concatenate(self.d16)
        lp = np.concatenate(self.lp)
        n_tok = len(d)
        # left: histogram of per-token log ratios, log-count axis so the tails are visible
        bins = np.linspace(-0.3, 0.3, 61)
        h, _ = np.histogram(np.clip(d, -0.3, 0.3), bins=bins)
        top = float(np.ceil(np.log10(h.max() + 1) * 2) / 2)
        plot = Plot(x_range=(-0.3, 0.3), y_range=(0, top), width=5.8, height=3.6, x_ticks=[-0.2, 0, 0.2],
                    y_ticks=[1, 2, 3], y_fmt=lambda v: MathTex(rf"10^{{{int(v)}}}", font_size=22, color=GREY_A),
                    x_label=r"$\log \pi_{\text{fp32}} - \log \pi_{\text{bf16 sampler}}$, per token", y_label=r"tokens")
        plot.move_to(LEFT * 3.4 + DOWN * 0.35)
        hist = VGroup()
        for lo, hi, c in zip(bins[:-1], bins[1:], h):
            if c <= 0:
                continue
            a, b = plot.c2p(lo, 0), plot.c2p(hi, np.log10(1 + c))
            hist.add(Rectangle(width=b[0] - a[0], height=b[1] - a[1], stroke_width=0, fill_color=C.RATIO, fill_opacity=0.8)
                     .move_to((a + b) / 2))
        frac = float(np.mean(np.abs(d) > 0.01))
        big = float(np.mean(np.abs(d) > 0.1))
        frac16 = float(np.mean(np.abs(d16) > 0.01))
        # right: how often a token is off by more than 1%, by how likely the sampler thought it was
        p = np.exp(lp)
        buckets = [(0.9, 1.01, r"$p > 0.9$"), (0.5, 0.9, r"$0.5$--$0.9$"), (0.1, 0.5, r"$0.1$--$0.5$"),
                   (0.01, 0.1, r"$0.01$--$0.1$"), (0.0, 0.01, r"$p < 0.01$")]
        items, shares = [], []
        for lo, hi, name in buckets:
            m = (p >= lo) & (p < hi)
            sh = float(np.mean(np.abs(d[m]) > 0.01)) if m.any() else 0.0
            shares.append(sh)
            items.append((name + rf"\ \ ({m.sum():,} tokens)".replace(",", "{,}"), sh, C.RATIO,
                          rf"{100 * sh:.0f}\%" if sh >= 0.02 else rf"{100 * sh:.1f}\%"))
        rows = bar_rows(items, scale=3.2, font_size=24, bar_h=0.42, buff=0.22)
        rows.move_to(RIGHT * 3.6 + DOWN * 0.15)
        rt = label(r"share off by more than 1\%, by the token's probability", font_size=24, color=GREY_A).next_to(rows, UP, buff=0.35)
        rare = (p < 0.1)
        rare_share = float(np.mean(np.abs(d[rare]) > 0.01))
        assert shares[0] < 0.05 and rare_share > 0.8 and shares == sorted(shares), (shares, rare_share)
        head = label(rf"Qwen3 (0.6B), {len(self.d32)} real reasoning traces, {n_tok:,} tokens: sampled in bf16, re-scored in fp32".replace(",", "{,}"),
                     font_size=26).to_edge(UP, buff=0.35)
        stats = VGroup(
            label(rf"{100 * frac:.0f}\% of tokens differ by more than 1\%;\ \ {100 * big:.1f}\% by more than 10\%", font_size=26, color=YELLOW),
            label(rf"same bf16 weights, one pass instead of token by token: {100 * frac16:.0f}\% differ by more than 1\%",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.1).to_edge(DOWN, buff=0.5)
        self.mm_stats = dict(frac=frac, big=big, frac16=frac16, rare_share=rare_share, sure_share=shares[0])
        snippet = " ".join(self.m["seqs"][0]["text"].split())[:64] + " ..."
        samp = VGroup(label(r"sampler: bf16, one token at a time with a KV cache, 8 traces in a batch", font_size=26, color=C.OLD_POLICY),
                      Mono(snippet, font_size=20, color=GREY_B)).arrange(DOWN, buff=0.2)
        lrn = VGroup(label(r"learner: the same tokens again, in one full forward pass", font_size=26, color=C.RL_POLICY),
                     label(r"in fp32 \emph{and} in bf16", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.15)
        arr = Arrow(UP * 0.4, DOWN * 0.4, color=GREY_B, stroke_width=3)
        setup = VGroup(samp, arr, lrn).arrange(DOWN, buff=0.35).move_to(DOWN * 0.2)
        cmp_ = mtex(r"\log \pi_{\text{learner}}(y_t) - \log \pi_{\text{sampler}}(y_t)\ \ \text{for every token}", font_size=32,
                    color=C.RATIO).next_to(setup, DOWN, buff=0.4)
        with self.voiceover(
            "We measured it. A 0.6-billion-parameter Qwen3 model wrote eight reasoning traces, sampled token by token "
            "in bfloat16, the way an inference engine runs. <bookmark mark='r'/> Then we re-scored exactly the same "
            "tokens in a single float32 pass, the way a trainer might. <bookmark mark='h'/> Most log ratios are tiny, but the tails "
            f"are wide: {100 * frac:.0f} percent of tokens differ by more than one percent. <bookmark mark='b'/> "
            "Re-scoring in the same bfloat16, just in one pass instead of token by token, is no better: "
            f"{100 * frac16:.0f} percent. It's the order of the arithmetic, not only the precision. "
            "<bookmark mark='s'/> And the disagreement lives on the unlikely tokens. Near-certain tokens almost never "
            f"move, but {100 * rare_share:.0f} percent of tokens the sampler gave less than a ten percent chance "
            "are off by more than one percent: exactly the rare choices that exploration depends on."
        ) as vo:
            self.play(FadeIn(head), FadeIn(real_tag(r"real model, on this computer")), FadeIn(samp))
            vo.wait_until("r")
            self.play(GrowArrow(arr), FadeIn(lrn))
            self.play(FadeIn(cmp_))
            vo.wait_until("h")
            self.play(FadeOut(setup), FadeOut(cmp_))
            self.play(FadeIn(plot), FadeIn(hist, lag_ratio=0.01), run_time=1.5)
            self.play(FadeIn(stats[0]))
            vo.wait_until("b")
            self.play(FadeIn(stats[1]))
            vo.wait_until("s")
            self.play(FadeIn(rt), LaggedStart(*[AnimationGroup(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2])) for r in rows],
                                              lag_ratio=0.25), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def per_sequence(self):
        T = max(len(x) for x in self.d32)
        cums = [np.cumsum(x) for x in self.d32]
        lim = max(1.0, max(np.abs(c).max() for c in cums) * 1.1)
        plot = Plot(x_range=(0, T), y_range=(-lim, lim), width=7.8, height=4.0, x_ticks=list(np.linspace(0, T, 5).astype(int)),
                    y_ticks=[-round(lim, 1), 0, round(lim, 1)], x_label=r"position in the answer (tokens)",
                    y_label=r"$\log$ of the whole-sequence ratio $\prod_t \rho_t$")
        plot.move_to(LEFT * 1.5 + DOWN * 0.5)
        cols = [C.RATIO, C.OLD_POLICY, C.ADVANTAGE, C.BASELINE, C.KL, C.ENTROPY, C.LENGTH, C.REWARD]
        walks = VGroup(*[plot.line(np.arange(1, len(c) + 1), c, color=cols[i % len(cols)], stroke_width=2.5) for i, c in enumerate(cums)])
        geo = VGroup(*[plot.line(np.arange(1, len(c) + 1), c / np.arange(1, len(c) + 1), color=cols[i % len(cols)], stroke_width=2.5)
                       for i, c in enumerate(cums)])
        ends = np.array([c[-1] for c in cums])
        head = label(r"The whole answer's importance weight is a product of per-token ratios", font_size=28).to_edge(UP, buff=0.35)
        f1 = mtex(r"\log \prod_t \rho_t = \sum_t \log \rho_t", font_size=34).next_to(plot, RIGHT, buff=0.2).shift(UP * 1.4)
        f2 = mtex(r"s_i = \Big(\prod_t \rho_t\Big)^{1/|y_i|}", font_size=34, color=YELLOW).next_to(f1, DOWN, buff=1.4)
        n2 = label(r"GSPO: the geometric mean", font_size=24, color=YELLOW).next_to(f2, DOWN, buff=0.12)
        rng = label(rf"after the full answer: $\prod \rho$ ranges from ${np.exp(ends.min()):.2f}$ to ${np.exp(ends.max()):.2f}$",
                    font_size=26, color=GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Now look at whole answers. The exact importance weight of a sequence is the product of its token ratios, "
            "so its logarithm is a sum: a random walk. <bookmark mark='w'/> Here are the walks for our eight traces. "
            f"They wander away from zero as the answers get longer: after {T} tokens, one answer's weight is "
            f"{np.exp(ends.max()):.1f} and another's is {np.exp(ends.min()):.2f}, though not one weight of the model "
            "changed. <bookmark mark='g'/> Qwen's GSPO uses the geometric "
            "mean instead, the average log ratio, which shrinks back toward zero as the answer grows."
        ) as vo:
            self.play(FadeIn(head), FadeIn(plot), FadeIn(f1), FadeIn(real_tag(r"real model, on this computer")))
            vo.wait_until("w")
            self.play(LaggedStart(*[Create(w) for w in walks], lag_ratio=0.1), run_time=3)
            self.play(FadeIn(rng))
            vo.wait_until("g")
            self.play(ReplacementTransform(walks, geo), FadeIn(f2), FadeIn(n2), run_time=2)
        self.wait(1.2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fixes(self):
        rows = [
            (r"Truncated IS (Yao et al., 2025)", r"\min\!\Big(\frac{\pi_{\text{learner}}}{\pi_{\text{sampler}}},\; C\Big)\, A\, \nabla \log \pi_\theta", C.RATIO),
            (r"Masked IS / IcePop", r"\rho\cdot\mathbf{1}\big[\alpha \le \rho \le \beta\big]\ \ \text{(drop outliers)}", C.RATIO),
            (r"GSPO (Qwen, 2025)", r"\text{one ratio per answer: } \Big(\frac{\pi_\theta(y)}{\pi_{\text{old}}(y)}\Big)^{1/|y|},\ \text{plus routing replay for MoE}", YELLOW),
            (r"CISPO (MiniMax, 2025)", r"\operatorname{sg}\big[\operatorname{clip}(\rho)\big]\, A \log \pi_\theta\ \ \text{(cap the weight, keep every token's gradient)}", C.ADVANTAGE),
            (r"Fix the numbers", r"\text{fp32 LM head (MiniMax-M1); fp16 rollouts (Qi et al., 2025)}", C.KL),
        ]
        g = VGroup()
        for name, tex, col in rows:
            n = label(name, font_size=26, color=col)
            m = MathTex(tex, font_size=30)
            g.add(VGroup(n, m))
        for i, row in enumerate(g):
            y = 2.2 - i * 1.05
            row[0].move_to([-4.6, y, 0])
            row[1].move_to([1.6, y, 0])
            if row[1].width > 8.2:
                row[1].width = 8.2
            row[1].move_to([1.75, y, 0])
        head = label(r"How the field corrects for it (2025--26)", font_size=32).to_edge(UP, buff=0.3)
        foot = label(r"defaults today: TRL masks whole sequences whose ratio exceeds 3; OLMo 3 truncates token ratios at 2",
                     font_size=24, color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Since 2025 the field has converged on a handful of fixes. <bookmark mark='t'/> Truncated importance "
            "sampling multiplies each token's gradient by its sampler-to-learner ratio, capped at a constant. "
            "<bookmark mark='m'/> Masking simply drops tokens or sequences whose ratios are too extreme. "
            "<bookmark mark='g'/> GSPO uses one ratio per answer, and for mixture-of-experts models replays the "
            "experts the sampler used, since about one expert in ten changes after each update. "
            "<bookmark mark='c'/> MiniMax's CISPO caps the importance weight but never zeroes a token's gradient, so "
            "rare reflective tokens like wait, or however, keep contributing. <bookmark mark='f'/> And some just fix "
            "the arithmetic: a float32 output layer, or float16 rollouts."
        ) as vo:
            self.play(FadeIn(head))
            for k, mark in enumerate(["t", "m", "g", "c", "f"]):
                vo.wait_until(mark)
                self.play(FadeIn(g[k], shift=RIGHT * 0.1))
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def async_(self):
        def lanes(y0, sync: bool):
            g = VGroup()
            x = -4.5
            for k in range(4):
                gen = Rectangle(width=1.8, height=0.42, stroke_width=0, fill_color=C.OLD_POLICY, fill_opacity=0.7)
                tr = Rectangle(width=0.7, height=0.42, stroke_width=0, fill_color=C.RL_POLICY, fill_opacity=0.85)
                if sync:
                    gen.move_to([x + 0.9, y0 + 0.3, 0])
                    tr.move_to([x + 1.8 + 0.35, y0 - 0.3, 0])
                    x += 2.5
                else:
                    gen.move_to([-4.5 + k * 1.85 + 0.9, y0 + 0.3, 0])
                    tr.move_to([-4.5 + (k + 1) * 1.85 + 0.35, y0 - 0.3, 0])
                g.add(gen, tr)
            return g
        s = lanes(1.3, True)
        a = lanes(-1.3, False)
        ls = label(r"synchronous: the trainer waits, then the generators wait", font_size=24, color=GREY_A).next_to(s, UP, buff=0.2)
        la = label(r"asynchronous: both always busy, but data is a step or more stale", font_size=24, color=GREY_A).next_to(a, UP, buff=0.2)
        key = VGroup(VGroup(Square(0.25, stroke_width=0, fill_color=C.OLD_POLICY, fill_opacity=0.7), label(r"generate", font_size=22)).arrange(RIGHT, buff=0.1),
                     VGroup(Square(0.25, stroke_width=0, fill_color=C.RL_POLICY, fill_opacity=0.85), label(r"train", font_size=22)).arrange(RIGHT, buff=0.1)
                     ).arrange(RIGHT, buff=0.5).to_edge(UP, buff=0.4)
        facts = VGroup(
            label(r"OLMo 3: the learner spent 75\% of its time waiting for rollouts (inference used $\sim$5$\times$ the GPUs)", font_size=24),
            label(r"ScaleRL: PipelineRL with up to 8 steps of staleness; open-instruct, prime-rl: up to 8", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Staleness is the other source of off-policy data. Long answers make generation the bottleneck: in "
            "OLMo 3's runs the learner spent three quarters of its time waiting. <bookmark mark='a'/> So large "
            "systems decouple the two, generating with slightly old weights while training continues, and stream new "
            "weights to the generators as they go. Every one of these importance-ratio corrections now has to "
            "absorb that lag too."
        ) as vo:
            self.play(FadeIn(key), FadeIn(ls), FadeIn(s, lag_ratio=0.1), FadeIn(schematic_tag()))
            vo.wait_until("a")
            self.play(FadeIn(la), FadeIn(a, lag_ratio=0.1))
            self.play(FadeIn(facts))
        self.wait(0.4)
        self.clear_scene()
