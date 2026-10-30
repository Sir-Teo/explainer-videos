from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai30.common import CTRL, FEAT, PART, PROBE, load, spread_bar, ticks

SAEC = C.MLP


class Disagree(VoiceoverScene):
    def construct(self):
        self.card()
        self.probes()
        self.seeds()
        self.random()
        self.ambition()

    def card(self):
        card = chapter_card(17, r"Where the field disagrees", r"Are sparse features the right unit at all?", part=PART)
        with self.voiceover("Chapter seventeen. Where the field disagrees."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def probes(self):
        d = load("disagree")
        ns = [int(n) for n in d["probe_sizes"]]
        xs = np.log2(ns)
        raw, s1, s8 = (np.asarray(d[k]) for k in ("probe_raw", "probe_sae1", "probe_sae8"))  # (sizes, draws, [in, out])
        hc = history_card(r"Mar 2025", r"Google DeepMind's interpretability team", r"autoencoder probes lose to plain "
                          r"linear probes at detecting harmful intent, \ out of distribution most of all; \ the team "
                          r"deprioritized autoencoder research", width=5.6, color=CTRL, font_size=18).to_corner(UL, buff=0.3)
        hc2 = note(r"also Kantamneni et al.\ (2025): \ $113$ datasets, \ no consistent win").next_to(hc, DOWN, buff=0.1).align_to(hc, LEFT)
        lo = float(min(raw.min(), s1.min(), s8.min()))
        g = axes([xs[0] - 0.3, xs[-1] + 0.3], [max(0.4, lo - 0.05), 1.0], x_length=6.0, y_length=3.4,
                 xlabel=r"training examples", ylabel=r"accuracy, \ ``inside a quotation'' \ (novels model)", xticks=list(xs),
                 xfmt=lambda v: f"{int(round(2 ** v))}", yticks=ticks(max(0.4, lo - 0.05), 1.0, 3), center=[3.0, 0.3, 0])
        cols = [(raw, PROBE, r"linear probe, \ all $256$ numbers"), (s8, SAEC, r"$8$ autoencoder latents"),
                (s1, FEAT, r"$1$ latent")]
        plots = VGroup()
        ood_c = VGroup()
        for arr, col, _ in cols:
            m = arr[:, :, 0].mean(1)
            plots.add(VGroup(curve(g.ax, xs, m, col, 3),
                             *[spread_bar(g.ax, x, arr[i, :, 0], col, width=0.08) for i, x in enumerate(xs)]))
            ood_c.add(DashedVMobject(curve(g.ax, xs, np.clip(arr[:, :, 1].mean(1), 0.4, 1.0), col, 2.5), num_dashes=24))
        lg = legend([(c_, t) for _, c_, t in cols], font_size=17).next_to(g, DOWN, buff=0.6).align_to(g, LEFT)
        lg2 = label(r"solid: \ held-out novel text; \ dashed: \ chat transcripts", font_size=17, color=GREY_A).next_to(lg, RIGHT, buff=0.5)
        maj = float(d["probe_majority"])
        ood = [float(a[-1, :, 1].mean()) for a, _, _ in cols]
        ind = [float(a[-1, :, 0].mean()) for a, _, _ in cols]
        res = label(rf"at ${ns[-1]:,}$ examples, \ inside chat transcripts: \\ linear ${100 * ood[0]:.0f}\%$, \ "
                    rf"$8$ latents ${100 * ood[1]:.0f}\%$, \ $1$ latent ${100 * ood[2]:.0f}\%$ \ (always guessing: \ "
                    rf"${100 * float(d['probe_majority_ood']):.0f}\%$)".replace(",", "{,}"),
                    font_size=19, color=WHITE).to_corner(DL, buff=0.35)
        small = [float(a[0, :, 0].mean()) for a, _, _ in cols]
        verdict = (f"With few examples the latents help: at {ns[0]} examples, one latent scores "
                   f"{100 * small[2]:.0f} percent against the linear probe's {100 * small[0]:.0f}. "
                   if small[2] > small[0] + 0.02 else
                   f"Even with few examples the latents do not help: at {ns[0]}, {100 * small[2]:.0f} percent against "
                   f"{100 * small[0]:.0f}. ")
        verdict2 = (f"With plenty, the plain probe wins, {100 * ind[0]:.0f} percent against {100 * ind[1]:.0f} for "
                    f"eight latents, and {100 * ood[0]:.0f} against {100 * ood[1]:.0f} inside chat transcripts, a "
                    "kind of text neither was trained on."
                    if ind[0] >= ind[1] else
                    f"With plenty, eight latents match the probe, {100 * ind[1]:.0f} percent against {100 * ind[0]:.0f}.")
        with self.voiceover(
            "The sharpest argument is about usefulness. <bookmark mark='a'/> In March 2025 Google DeepMind's "
            "interpretability team reported that probes built on autoencoder latents lost to plain linear probes at "
            "detecting harmful intent, especially on new kinds of prompts, and deprioritized the research; a study "
            "of 113 datasets found no consistent win either. <bookmark mark='b'/> Try it on ours: detect 'inside a "
            f"quotation' in the novels model after block {int(d['probe_layer'])}, with a linear probe on all 256 numbers, "
            "or with the eight or the one latents of an autoencoder trained here that differ most, from "
            f"{ns[0]} to {ns[-1]:,} examples, five draws each. "
            f"<bookmark mark='c'/> {verdict}<bookmark mark='d'/>{verdict2}"
        ) as vo:
            self.play(FadeIn(hc), FadeIn(hc2), FadeIn(g))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(lg), FadeIn(lg2))
            vo.wait_until("c")
            self.play(*[Create(p[0]) for p in plots], *[FadeIn(p[1:]) for p in plots], run_time=2)
            vo.wait_until("d")
            self.play(*[Create(c) for c in ood_c], FadeIn(res), run_time=2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def seeds(self):
        d = load("disagree")
        bc = np.asarray(d["seed_best_cos"])
        sh = [float(v) for v in d["seed_share"]]
        h, e = np.histogram(bc, bins=np.linspace(0, 1, 26))
        top = float(h.max())
        g = axes([0, 1], [0, top * 1.1], x_length=6.4, y_length=3.4, xlabel=r"each latent's best match in a second seed's "
                 r"dictionary \ (cosine)", ylabel=r"latents", xticks=[0, 0.5, 0.7, 1], yticks=ticks(0, top, 3),
                 center=[-2.4, -0.4, 0])
        bars_ = VGroup(*[Rectangle(width=6.4 / 25 * 0.9, height=max(v / (top * 1.1) * 3.4, 0.005), stroke_width=0,
                                   fill_color=SAEC if (a + b) / 2 >= 0.7 else CTRL, fill_opacity=0.9)
                         .move_to(g.ax.c2p((a + b) / 2, 0), aligned_edge=DOWN) for v, a, b in zip(h, e, e[1:])])
        cut = DashedLine(g.ax.c2p(0.7, 0), g.ax.c2p(0.7, top * 1.1), color=WHITE, dash_length=0.06)
        hc = history_card(r"Jan 2025", r"G.~Paulo \& N.~Belrose", r"two autoencoders on the same data, \ different seeds: "
                          r"\ only about $30\%$ of latents shared \ (Llama 3 8B, \ $131$K latents)", width=5.0,
                          color=CTRL, font_size=18).to_corner(UR, buff=0.3)
        res = label(rf"ours, \ TopK, \ $512$ latents: \\ ${100 * min(sh):.0f}$--${100 * max(sh):.0f}\%$ recur across "
                    rf"the three pairs of seeds; \\ L1: \ ${100 * float(d['seed_share_l1']):.0f}\%$", font_size=21,
                    color=WHITE).next_to(hc, DOWN, buff=0.4).align_to(hc, LEFT)
        with self.voiceover(
            "A second argument: are the features real, or artefacts of one training run? <bookmark mark='a'/> "
            "Gonçalo Paulo and Nora Belrose trained the same autoencoder twice with different seeds, on Llama 3, and "
            "found only about thirty percent of latents shared. <bookmark mark='b'/> Ours, from chapter nine's runs: "
            "for each latent, the best match in another seed's dictionary. Counting a cosine above 0.7 as the same "
            f"feature, {100 * min(sh):.0f} to {100 * max(sh):.0f} percent recur. A small model with few features is "
            "kinder than a big one, but a dictionary is one answer, not the answer."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(g))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars_], lag_ratio=0.03), Create(cut), run_time=2)
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def random(self):
        d = load("disagree")
        rp, tp = np.asarray(d["random_purity"]), np.asarray(d["trained_purity"])
        bins = np.arange(1, 9) / 8
        hist = lambda v: np.array([np.mean(np.isclose(v, b)) for b in bins])  # noqa: E731
        hr, ht = hist(rp), hist(tp)
        top = float(max(hr.max(), ht.max()))
        g = axes([0, 8], [0, top * 1.1], x_length=6.0, y_length=3.2, xlabel=r"of a latent's $8$ strongest moments, \ how "
                 r"many on one character", ylabel=r"share of latents", xticks=[], yticks=ticks(0, top, 2), center=[-2.6, -0.4, 0])
        bw = 0.28
        b1 = VGroup(*[Rectangle(width=bw, height=max(v / (top * 1.1) * 3.2, 0.01), stroke_width=0, fill_color=SAEC,
                                fill_opacity=0.9).move_to(g.ax.c2p(i + 0.5, 0) + LEFT * 0.16, aligned_edge=DOWN) for i, v in enumerate(ht)])
        b2 = VGroup(*[Rectangle(width=bw, height=max(v / (top * 1.1) * 3.2, 0.01), stroke_width=0, fill_color=CTRL,
                                fill_opacity=0.9).move_to(g.ax.c2p(i + 0.5, 0) + RIGHT * 0.16, aligned_edge=DOWN) for i, v in enumerate(hr)])
        xt = VGroup(*[MathTex(str(i + 1), font_size=20, color=GREY_B).next_to(g.ax.c2p(i + 0.5, 0), DOWN, buff=0.1) for i in range(8)])
        lg = legend([(SAEC, rf"the trained transformer: \ mean ${8 * tp.mean():.1f}$"),
                     (CTRL, rf"the same, \ with random weights: \ mean ${8 * rp.mean():.1f}$")], font_size=18)
        lg.next_to(g, UP, buff=0.15).align_to(g, LEFT)
        hc = history_card(r"Jan 2025", r"T.~Heap, T.~Lawson, L.~Farnik \& L.~Aitchison", r"autoencoders on randomly "
                          r"initialized transformers score about as well on the usual interpretability metrics", width=5.0,
                          color=CTRL, font_size=18).to_corner(UR, buff=0.3)
        fr, ft = float(d["random_fvu"]), float(d["trained_fvu"])
        close = abs(rp.mean() - tp.mean()) < 0.1
        verdict = ("By that measure the random model looks just as interpretable: a score like ours rewards latents "
                   "that track the current character, which even a random network passes along." if close else
                   "Here the trained model's latents do look cleaner, but the gap is a property of our measure as much "
                   "as of the model.")
        with self.voiceover(
            "A third: a baseline that should embarrass us. <bookmark mark='a'/> Thomas Heap and colleagues trained "
            "autoencoders on transformers with random weights, and found they scored about as well on the usual "
            "interpretability metrics. <bookmark mark='b'/> We tried it: the same autoencoder, on a copy of Part 13's "
            "transformer that was never trained. Chapter eight's purity score, how many of a latent's eight strongest "
            f"moments share a character: {8 * tp.mean():.1f} on average for the trained model, {8 * rp.mean():.1f} "
            f"for the random one. {verdict}"
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(g), FadeIn(xt), FadeIn(lg))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in b1], lag_ratio=0.08),
                      LaggedStart(*[GrowFromEdge(b, DOWN) for b in b2], lag_ratio=0.08), run_time=2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ambition(self):
        left = VGroup(label(r"ambitious", font_size=36, color=FEAT),
                      label(r"reverse-engineer the whole model: \\ every feature, \ every circuit", font_size=26),
                      label(r"the obstacle: \ dark matter \ (Claude 3.5 Haiku's \\ best transcoder left $21.7\%$ unexplained)",
                            font_size=23, color=GREY_A),
                      label(r"alternatives: \ decompose the parameters, \\ not the activations; \ train models to be "
                            r"sparse", font_size=23, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        right = VGroup(label(r"pragmatic", font_size=36, color=PROBE),
                       label(r"answer the question at hand: \\ is it deceiving, \ what did fine-tuning change?", font_size=26),
                       label(r"the tools: \ probes, \ steering vectors, \ diffs, \ audits; \\ and simple baselines first",
                             font_size=23, color=GREY_A),
                       label(r"AxBench (2025): \ for steering, \ prompting beat \\ every internal method", font_size=23,
                             color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        both = VGroup(left, right).arrange(RIGHT, buff=1.0, aligned_edge=UP)
        if both.width > 13.2:
            both.scale_to_fit_width(13.2)
        both.move_to(DOWN * 0.1)
        right.set_opacity(0.25)
        cite_ = cite(r"Sharkey et al., \textit{Open Problems in Mechanistic Interpretability} (2025); \ Wu et al., "
                     r"\textit{AxBench} (2025)", corner=DL)
        with self.voiceover(
            "Underneath is a disagreement about the goal. <bookmark mark='a'/> The ambitious programme wants to "
            "reverse-engineer whole models, every feature and every circuit. Its obstacle is the dark matter: "
            "Anthropic's best transcoder for Claude 3.5 Haiku still left about a fifth of the MLPs' output "
            "unexplained, and some researchers now decompose the parameters instead, or train models sparse from "
            "the start. <bookmark mark='b'/> The pragmatic programme asks narrower questions, is this model "
            "deceiving us, what did fine-tuning change, and answers them with whatever works, often simple: in the "
            "AxBench comparison of 2025, plain prompting steered better than any internal method. Both programmes "
            "measure themselves against baselines now, which is perhaps the field's most important change."
        ) as vo:
            self.play(FadeIn(cite_), FadeIn(left[0]), FadeIn(right))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in left[1:]], lag_ratio=0.5), run_time=3)
            vo.wait_until("b")
            self.play(right.animate.set_opacity(1), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()
