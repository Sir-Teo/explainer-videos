from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.frontier.common import DSV3, KIMI_K2, label, load, note, schematic_tag, source

EXPERT_COLORS = [PURPLE_B, TEAL_C, GOLD_C, PINK, BLUE_C, GREEN_C, RED_C, ORANGE]


class Architecture(VoiceoverScene):
    def construct(self):
        self.blueprint()
        self.moe_idea()
        self.frontier_moes()
        self.balancing()
        self.other_shifts()

    # ------------------------------------------------------------------
    def blueprint(self):
        rows = [
            (r"normalization", r"LayerNorm", r"RMSNorm"),
            (r"word order", r"learned position vectors", r"rotary embeddings (RoPE)"),
            (r"MLP", r"GELU", r"SwiGLU (gated)"),
            (r"attention", r"multi-head", r"grouped-query or latent (smaller cache)"),
            (r"stability", r"---", r"QK-norm, no biases"),
        ]
        hdr = VGroup(label(r"", font_size=26), label(r"GPT-2 (2019)", font_size=30, color=GREY_A),
                     label(r"open models, 2025--26", font_size=30, color=C.PARAMS))
        table = VGroup(hdr)
        for a, b, c in rows:
            table.add(VGroup(label(a, font_size=26, color=GREY_A), label(b, font_size=26), label(c, font_size=26, color=C.PARAMS)))
        xs = [-4.6, -1.4, 3.3]
        for i, r in enumerate(table):
            for j, cell in enumerate(r):
                cell.move_to([xs[j], 2.2 - i * 0.78, 0])
        head = label(r"The transformer blueprint, refined", font_size=36).to_edge(UP, buff=0.4)
        foot = label(r"our pocket models: RMSNorm, RoPE, SwiGLU, no biases; QK-norm gets its own experiment",
                     font_size=24, color=C.KEPT).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "What gets trained? Still a transformer: the same basic blueprint as GPT-2, which our earlier video took "
            "apart piece by piece. <bookmark mark='r'/> But nearly every component has been refined: a simpler "
            "normalization, rotary position embeddings, gated MLPs, attention that shares or compresses its keys and "
            "values to save memory, and normalization of the queries and keys for stability. <bookmark mark='p'/> Our "
            "pocket models use the first three, and QK-norm gets an experiment of its own later on."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr))
            vo.wait_until("r")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in table[1:]], lag_ratio=0.3), run_time=3.0)
            vo.wait_until("p")
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def moe_idea(self):
        E, k = 8, 2
        tok = VGroup(*[Square(0.22, stroke_width=0, fill_color=C.EMBED, fill_opacity=0.3 + 0.6 * abs(np.sin(i)))
                       for i in range(8)]).arrange(DOWN, buff=0.03).move_to(LEFT * 5.6)
        tl = label(r"a token's vector", font_size=22, color=GREY_A).next_to(tok, DOWN, buff=0.15)
        router = RoundedRectangle(width=1.6, height=1.0, corner_radius=0.12, stroke_color=C.EXPERT, fill_color=C.EXPERT,
                                  fill_opacity=0.15).move_to(LEFT * 3.4)
        rl = label(r"router", font_size=26).move_to(router)
        experts = VGroup()
        for e in range(E):
            r = RoundedRectangle(width=1.5, height=0.55, corner_radius=0.1, stroke_color=EXPERT_COLORS[e],
                                 fill_color=EXPERT_COLORS[e], fill_opacity=0.12)
            r.add(label(rf"expert {e + 1}", font_size=22).move_to(r))
            experts.add(r)
        experts.arrange(DOWN, buff=0.12).move_to(RIGHT * 0.6)
        scores = np.array([0.05, 0.31, 0.04, 0.08, 0.02, 0.38, 0.07, 0.05])
        top = np.argsort(-scores)[:k]
        bars = VGroup(*[Rectangle(width=1.6 * s / scores.max(), height=0.32, stroke_width=0, fill_color=EXPERT_COLORS[e],
                                  fill_opacity=0.9).next_to(experts[e], LEFT, buff=0.25).align_to(experts[e], DOWN).shift(UP * 0.11)
                        for e, s in enumerate(scores)])
        for b, ex in zip(bars, experts):
            b.next_to(ex, LEFT, buff=0.2)
        out = Circle(0.35, color=WHITE).move_to(RIGHT * 3.6)
        ol = MathTex(r"\textstyle\sum", font_size=36).move_to(out)
        arrows = VGroup(*[Arrow(experts[e].get_right(), out.get_left(), buff=0.08, stroke_width=3, color=EXPERT_COLORS[e]) for e in top])
        a0 = Arrow(tok.get_right(), router.get_left(), buff=0.1, stroke_width=3, color=GREY_B)
        res = label(r"weighted sum of the chosen experts' outputs", font_size=24, color=GREY_A).next_to(out, DOWN, buff=0.5).shift(RIGHT * 1.0)
        head = label(r"Mixture of experts: many MLPs, only a few used per token", font_size=34).to_edge(UP, buff=0.4)
        foot = VGroup(label(r"parameters grow with the number of experts", font_size=26, color=C.PARAMS),
                      label(r"compute per token grows only with the number chosen", font_size=26, color=C.COMPUTE)
                      ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The biggest architectural change of the last two years is the mixture of experts. In a standard "
            "transformer, every token passes through the whole MLP in every layer. <bookmark mark='e'/> A "
            "mixture-of-experts layer replaces that one MLP with many smaller ones, the experts, <bookmark mark='r'/> "
            "and a small router that scores them for each token <bookmark mark='k'/> and sends the token to only the "
            "top few. <bookmark mark='f'/> So the number of parameters grows with the number of experts, while the "
            "computation per token grows only with the number chosen."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tok), FadeIn(tl), FadeIn(schematic_tag()))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(x) for x in experts], lag_ratio=0.08))
            vo.wait_until("r")
            self.play(FadeIn(router), FadeIn(rl), GrowArrow(a0))
            self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars], lag_ratio=0.05))
            vo.wait_until("k")
            self.play(*[experts[e].animate.set_fill(opacity=0.55) for e in top],
                      *[experts[e].animate.set_opacity(0.3) for e in range(E) if e not in top],
                      *[bars[e].animate.set_opacity(0.25) for e in range(E) if e not in top])
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2), FadeIn(out), FadeIn(ol), FadeIn(res))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def frontier_moes(self):
        def grid(n, active, shared, cols):
            cells = VGroup()
            rng = np.random.default_rng(n)
            on = set(rng.choice(n, active, replace=False).tolist())
            for i in range(n):
                lit = i in on
                cells.add(Square(0.16, stroke_width=0, fill_color=C.EXPERT if lit else GREY_D,
                                 fill_opacity=1.0 if lit else 0.5))
            cells.arrange_in_grid(cols=cols, buff=0.035)
            sh = VGroup(*[Square(0.16, stroke_width=0, fill_color=C.COMPUTE, fill_opacity=1.0) for _ in range(shared)])
            sh.arrange(RIGHT, buff=0.035).next_to(cells, UP, buff=0.12).align_to(cells, LEFT)
            return VGroup(cells, sh)
        specs = [
            (r"DeepSeek-V3 (Dec 2024)", 256, DSV3["top_k"], 1, 16, r"671B total, 37B active"),
            (r"Kimi K2 (Jul 2025)", 384, KIMI_K2["top_k"], 1, 24, r"1.04T total, 32B active"),
            (r"Kimi K3 (Jul 2026)", 896, 16, 2, 32, r"2.8T total"),
        ]
        assert DSV3["experts"] == 256 and KIMI_K2["experts"] == 384
        assert abs(DSV3["active"] / DSV3["total"] - 0.055) < 0.002
        cols = VGroup()
        for name, n, k, sh, c, sub in specs:
            g = grid(n, k, sh, c)
            t = label(name, font_size=26).next_to(g, UP, buff=0.25)
            s = label(sub, font_size=24, color=GREY_A).next_to(g, DOWN, buff=0.2)
            s2 = label(rf"{k} of {n} experts per token", font_size=22, color=C.EXPERT).next_to(s, DOWN, buff=0.1)
            cols.add(VGroup(t, g, s, s2))
        cols.arrange(RIGHT, buff=0.6, aligned_edge=DOWN)
        head = label(r"Frontier mixtures of experts: more experts, a smaller share used per token", font_size=32).to_edge(UP, buff=0.35)
        key = VGroup(VGroup(Square(0.18, stroke_width=0, fill_color=C.EXPERT, fill_opacity=1), label(r"chosen expert", font_size=22)).arrange(RIGHT, buff=0.1),
                     VGroup(Square(0.18, stroke_width=0, fill_color=C.COMPUTE, fill_opacity=1), label(r"shared expert (always on)", font_size=22)).arrange(RIGHT, buff=0.1),
                     VGroup(Square(0.18, stroke_width=0, fill_color=GREY_D, fill_opacity=0.5), label(r"idle for this token", font_size=22)).arrange(RIGHT, buff=0.1)
                     ).arrange(RIGHT, buff=0.5).next_to(head, DOWN, buff=0.2)
        cols.scale(min(1.0, 13.4 / cols.width, 5.6 / cols.height)).next_to(key, DOWN, buff=0.25)
        src = source(r"DeepSeek-V3 report; Kimi K2 report (arXiv 2507.20534); Kimi K3 report (arXiv 2607.24653)")
        with self.voiceover(
            "Frontier open models push this hard. DeepSeek-V3 has 256 experts per layer and uses eight of them, plus "
            "one shared expert that every token visits: 671 billion parameters in total, but only 37 billion doing work "
            "for any one token. <bookmark mark='k2'/> Kimi K2 has 384 experts and passes a trillion parameters. "
            "<bookmark mark='k3'/> And Kimi K3, from July 2026, picks sixteen of 896, for 2.8 trillion parameters. "
            "Experts keep getting more numerous, and the fraction used per token keeps shrinking, now around three to "
            "five percent."
        ) as vo:
            self.play(FadeIn(head), FadeIn(key), FadeIn(src), FadeIn(cols[0]))
            vo.wait_until("k2")
            self.play(FadeIn(cols[1]))
            vo.wait_until("k3")
            self.play(FadeIn(cols[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def balancing(self):
        res = load("moe")
        names = [("moe_none", r"no balancing"), ("moe_aux", r"auxiliary loss"), ("moe_bias", r"bias (DeepSeek-V3)")]
        panels = VGroup()
        trackers = []
        final = {}
        for key, title in names:
            r = res[key]
            loads = r["loads"]
            steps = np.array([x[0] for x in loads], float)
            L = np.array([x[1:] for x in loads], float)  # (t, layers, experts)
            final[key] = L[-20:].mean(0)
            lay = L[:, -1, :]  # the last of the 4 MoE layers
            bars = VGroup(*[Rectangle(width=0.28, height=0.01, stroke_width=0, fill_color=EXPERT_COLORS[e],
                                      fill_opacity=0.9) for e in range(8)]).arrange(RIGHT, buff=0.06, aligned_edge=DOWN)
            base = Line(bars.get_left() + LEFT * 0.1, bars.get_right() + RIGHT * 0.1, color=GREY_C, stroke_width=1.5)
            fair = DashedLine(base.get_left() + UP * 2.6 * (1 / 8) / 0.5, base.get_right() + UP * 2.6 * (1 / 8) / 0.5,
                              color=WHITE, stroke_width=1.5, dash_length=0.06)
            t = label(title, font_size=26).next_to(base, UP, buff=2.95)
            v = label(rf"val loss {r['final_val']:.3f}", font_size=22, color=GREY_A).next_to(base, DOWN, buff=0.25)
            busy = label(rf"busiest: {8 * final[key][-1].max():.1f}$\times$ fair", font_size=22,
                         color=C.PENALTY if key == "moe_none" else C.KEPT).next_to(v, DOWN, buff=0.12)
            g = VGroup(t, bars, base, fair, v)
            g.busy = busy
            g.bars, g.base, g.lay, g.steps = bars, base, lay, steps
            panels.add(g)
        panels.arrange(RIGHT, buff=1.1).move_to(DOWN * 0.2)
        for g in panels:
            for b in g.bars:
                b.align_to(g.base, DOWN)
            g.busy.next_to(g[4], DOWN, buff=0.12)
        tr = ValueTracker(0)

        def updater_for(g):
            def upd(m):
                i = int(min(len(g.lay) - 1, tr.get_value() * (len(g.lay) - 1)))
                for e, b in enumerate(m):
                    h = max(0.01, 2.6 * g.lay[i, e] / 0.5)
                    b.stretch_to_fit_height(h)
                    b.align_to(g.base, DOWN)
            return upd
        for g in panels:
            g.bars.add_updater(updater_for(g))
            trackers.append(g)
        head = label(r"Load balancing: our three real MoE runs (8 experts, top-2)", font_size=32).to_edge(UP, buff=0.35)
        sub = label(r"share of tokens routed to each expert in the last layer, during training", font_size=24, color=GREY_A).next_to(head, DOWN, buff=0.15)
        fair_l = label(r"dashed: a fair share (1/8)", font_size=22, color=GREY_B).to_edge(DOWN, buff=0.35)
        clock = VGroup(label(r"step", font_size=24, color=GREY_A), Integer(0, font_size=26)).arrange(RIGHT, buff=0.15).to_corner(DR, buff=0.4)
        clock[1].add_updater(lambda m: m.set_value(int(tr.get_value() * panels[0].steps[-1])))
        imb = {k: float(final[k][-1].max() * 8) for k in final}
        self.imbalance = imb
        vals = {k: res[k]["final_val"] for k, _ in names}
        assert round(imb["moe_none"], 1) == 3.0 and final["moe_none"][-1].min() < 0.01
        assert imb["moe_bias"] < 1.2 < imb["moe_aux"] < 1.5 and vals["moe_aux"] < vals["moe_bias"] < vals["moe_none"]
        with self.voiceover(
            "But routers have a failure mode. Experts that get more tokens improve faster and get chosen even more: "
            "the rich get richer. Here are three real runs of our pocket mixture of experts, eight experts, two per "
            "token. <bookmark mark='g'/> Watch the share of tokens each expert receives as training goes. With no "
            "balancing, the busiest expert ends up with three times its fair share, while another gets almost "
            "nothing. <bookmark mark='a'/> The classic fix is an extra loss term that penalizes uneven routing. "
            "<bookmark mark='b'/> DeepSeek-V3 used a gentler trick: a bias added to each expert's score, only for "
            "choosing experts, nudged up after every step if the expert was underused and down if it was overused, "
            "with no extra loss term competing with learning. Here, it balances almost perfectly. "
            "<bookmark mark='c'/> In our tiny runs, the auxiliary loss still finished with a slightly lower loss; in "
            "DeepSeek's experiments, at billions of parameters, the bias came out ahead."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub), FadeIn(panels), FadeIn(fair_l), FadeIn(clock))
            vo.wait_until("g")
            self.play(tr.animate.set_value(1.0), run_time=max(4.0, vo.until("a") - 0.5), rate_func=linear)
            self.play(FadeIn(panels[0].busy))
            vo.wait_until("a")
            self.play(FadeIn(panels[1].busy), Indicate(panels[1][0], color=C.KEPT))
            vo.wait_until("b")
            self.play(Indicate(panels[2][0], color=C.KEPT))
            self.play(FadeIn(panels[2].busy))
            vo.wait_until("c")
            self.play(*[Indicate(g[4], color=WHITE, scale_factor=1.1) for g in panels])
        for g in panels:
            g.bars.clear_updaters()
        clock[1].clear_updaters()
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def other_shifts(self):
        items = VGroup(
            label(r"\textbf{Sparse attention} (DeepSeek-V3.2, GLM-5): each token attends to its top 2{,}048 earlier tokens", font_size=27),
            label(r"\textbf{Hybrid linear attention} (Qwen3.5, Kimi K3): 3 linear-time layers for every full-attention layer", font_size=27),
            label(r"\textbf{Multi-token prediction} (DeepSeek-V3/V4, GLM-5, Qwen3-Next): extra heads predict further ahead", font_size=27),
            label(r"\textbf{1-million-token context}, reached in stages late in training", font_size=27),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN * 0.1)
        head = label(r"Other 2025--26 shifts, mostly for long contexts and cheaper inference", font_size=32).to_edge(UP, buff=0.5)
        with self.voiceover(
            "A few other shifts are reshaping the blueprint, mostly to make long contexts and inference cheaper. "
            "Sparse attention lets each token look at only its most relevant earlier tokens. Hybrid models replace "
            "three of every four attention layers with cheaper linear-time layers. Multi-token prediction adds heads "
            "that guess several tokens ahead, both as extra training signal and to speed up generation. And context "
            "windows of a million tokens are now common, reached in stages near the end of training."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(i, shift=RIGHT * 0.2) for i in items], lag_ratio=0.6), run_time=vo.remaining() * 0.7)
        self.wait(0.4)
        self.clear_scene()
