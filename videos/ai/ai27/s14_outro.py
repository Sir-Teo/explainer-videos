from __future__ import annotations

import math

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai27.common import (ADAPT, ASSIST, BASE, GOLD, KLC, PART, POLICY, PROXY, REF, REWARD, load, node_box,
                                   rlhf_gains)
from videos.ai.ai27.compute import TOPICS, _demean


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.problems()
        self.next_time()
        self.references()

    # ------------------------------------------------------------------
    def tiles(self):
        """The part in ten pictures, each drawn from its own computed result."""
        TW, TH = 2.3, 1.55
        mk = lambda xr, yr: Axes(x_range=xr, y_range=yr, x_length=TW * 0.9, y_length=TH * 0.85, tips=False,
                                 axis_config={"stroke_color": GREY_D, "include_ticks": False})
        out = []
        s = load("sft")
        ev = np.asarray(s["evals"])
        ax = mk([0, float(ev[-1, 0]), 1], [0, 1, 0.5])
        out.append((VGroup(ax, curve(ax, [0] + list(ev[:, 0]), [s["base_which"]] + list(ev[:, 1]), ASSIST, 3)),
                    r"SFT: \ which book?", ASSIST))
        lo = load("lora")
        S = max(float(e[0]) for r in lo["runs"] for e in r["evals"])
        ax = mk([0, S, 1], [0, 1, 0.5])
        g = VGroup(ax)
        for r in lo["runs"]:
            e = np.asarray(r["evals"])
            g.add(curve(ax, [0] + list(e[:, 0]), [s["base_which"]] + list(e[:, 1]),
                        ASSIST if r["rank"] == "full" else ADAPT, 3))
        out.append((g, r"LoRA: \ a low-rank slice", ADAPT))
        rm = load("rm")
        xs = np.log10(np.asarray(rm["sizes"], float))
        ax = mk([float(xs[0]) - 0.1, float(xs[-1]) + 0.1, 1], [0.5, 1, 0.25])
        ceil = DashedLine(ax.c2p(float(xs[0]) - 0.1, rm["people_agree_gold"]), ax.c2p(float(xs[-1]) + 0.1,
                                                                                       rm["people_agree_gold"]),
                          color=GREY_C, dash_length=0.05)
        out.append((VGroup(ax, ceil, curve(ax, xs, rm["acc"], PROXY, 3)), r"reward models", PROXY))
        ins = load("inside")
        gc_ = _demean(ins["gold"], ins["topic"])
        sc_ = _demean(ins["large_score"], ins["topic"]) / float(ins["large_slope"])
        lo_, hi_ = float(min(gc_.min(), sc_.min())), float(max(gc_.max(), sc_.max()))
        ax = mk([lo_, hi_, 1], [lo_, hi_, 1])
        out.append((VGroup(ax, Line(ax.c2p(lo_, lo_), ax.c2p(hi_, hi_), color=GOLD, stroke_width=2),
                           *[Dot(ax.c2p(a, b), radius=0.012, color=PROXY, fill_opacity=0.6) for a, b in zip(gc_, sc_)]),
                    r"inside it", PROXY))
        cl = load("closed")
        ref, pi = np.asarray(cl["ref"]), np.asarray(cl["pi"])[-1]
        bars = VGroup()
        for i, (a, b) in enumerate(zip(ref, pi)):
            for v, col, dx in ((a, REF, -0.08), (b, POLICY, 0.08)):
                bars.add(Rectangle(width=0.14, height=max(1.6 * v / max(ref.max(), pi.max()), 0.02), stroke_width=0,
                                   fill_color=col, fill_opacity=0.9).move_to([0.32 * i + dx, 0, 0], aligned_edge=DOWN))
        out.append((bars, r"$\pi^* \propto \pi_{\mathrm{ref}}\, e^{r/\beta}$", POLICY))
        rl = load("rlhf")
        h = np.asarray(rl[f"b{rl['betas'][1]:g}".replace(".", "_")])
        x_, pr_, gd_ = rlhf_gains(h, float(ins["large_slope"]), float(np.mean(ins["large_score"])),
                                  float(np.mean(ins["gold"])), len(TOPICS))
        lo_, hi_ = float(min(pr_.min(), gd_.min(), 0)), float(max(pr_.max(), gd_.max()))
        ax = mk([0, float(h[-1, 0]), 1], [lo_ - 0.05, hi_ + 0.05, 1])
        out.append((VGroup(ax, curve(ax, x_, pr_, PROXY, 3), curve(ax, x_, gd_, GOLD, 3)), r"RLHF: \ proxy, gold", KLC))
        bo = load("bon")
        kx = np.sqrt(np.asarray(bo["kl"]))
        # each curve on its own scale, as in the chapter's two panels: the proxy climbs, gold rises and falls
        ys = [np.asarray(bo[k]) for k in ("large_proxy", "large_gold")]
        ys = [(y - y.min()) / (y.max() - y.min() + 1e-9) for y in ys]
        ax = mk([0, float(kx[-1]), 1], [-0.1, 1.1, 1])
        out.append((VGroup(ax, curve(ax, kx, ys[0], PROXY, 3), curve(ax, kx, ys[1], GOLD, 3)), r"Goodhart, \ measured",
                    GOLD))
        dp = np.asarray(load("dpo")["probe"])
        lo_, hi_ = float(dp[:, 1:].min()), float(dp[:, 1:].max())
        ax = mk([0, float(dp[-1, 0]), 1], [min(lo_, 0) - 0.5, max(hi_, 0) + 0.5, 1])
        out.append((VGroup(ax, curve(ax, dp[:, 0], dp[:, 1], REWARD, 3), curve(ax, dp[:, 0], dp[:, 2], C.PENALTY, 3)),
                    r"DPO: \ the gap grows", POLICY))
        di = load("distill")
        ct, cd = np.asarray(di["text"]["curve"]), np.asarray(di["teacher"]["curve"])
        lo_, hi_ = float(min(ct[:, 1].min(), cd[:, 1].min())), float(max(ct[:, 1].max(), cd[:, 1].max()))
        ax = mk([0, float(ct[-1, 0]), 1], [lo_ - 0.05, hi_ + 0.05, 1])
        out.append((VGroup(ax, curve(ax, ct[:, 0], ct[:, 1], BASE, 3), curve(ax, cd[:, 0], cd[:, 1], ASSIST, 3)),
                    r"distillation", ASSIST))
        mg = load("merge")["rows"]
        bars = VGroup()
        for i, (_, acc, _, ended) in enumerate(mg):
            for v, col, dx in ((acc, ASSIST, -0.07), (ended, ADAPT, 0.07)):
                bars.add(Rectangle(width=0.12, height=max(1.4 * v, 0.02), stroke_width=0, fill_color=col,
                                   fill_opacity=0.9).move_to([0.42 * i + dx, 0, 0], aligned_edge=DOWN))
        out.append((bars, r"merging", ADAPT))
        tiles = Group()
        for pic, cap, col in out:
            box, c_ = tile_frame(cap, col, TW, TH)
            if c_.width > TW + 0.1:
                c_.width = TW + 0.1
            pic.move_to(box.get_center() + UP * 0.22)
            if pic.width > TW:
                pic.width = TW
            if pic.height > TH:
                pic.height = TH
            tiles.add(Group(box, pic, c_))
        tiles.arrange_in_grid(rows=2, cols=5, buff=(0.16, 0.3)).move_to(DOWN * 0.3)
        if tiles.width > 13.7:
            tiles.width = 13.7
        return tiles

    def recap(self):
        tiles = self.tiles()
        head = label(rf"Part {PART}, in ten pictures", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. Supervised fine-tuning is maximum likelihood on the answers people want, and it can "
            "live in a low-rank slice of weight space, which is why LoRA works. A reward model learns people's "
            "preferences from comparisons with the Bradley-Terry model, and opening ours showed what it had "
            "learned, and where it was wrong. Reinforcement learning with a KL leash aims "
            "at an exact optimum, the reference model reweighted by the exponential of the reward. Push a learned "
            "reward too hard and it stops measuring what it was meant to: Goodhart's law, which we measured. DPO "
            "reaches the same optimum straight from the comparisons. And written principles, distillation and model "
            "merging make all of this cheaper."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.15, scale=0.95) for t_ in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"rewards from a checker, \ not a person: \ GRPO", [28]),
            (r"post-trained models acting over long tasks", [29]),
            (r"persona vectors: \ what fine-tuning changes inside", [30]),
            (r"reward hacking, \ sycophancy, \ trusting evaluations", [31]),
        ], font_size=26)
        with self.voiceover(
            "All of this comes back. Part 28 trains models to reason, with reinforcement learning on answers that "
            "can be checked. Part 29 trains agents that act over long tasks. Part 30 opens the model up, persona "
            "vectors included. And Part 31 asks whether we can trust what post-training produces."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"Show that the Bradley--Terry likelihood of a set of comparisons is unchanged if a constant $c(x)$ is "
            r"added to $r(x, y)$ for every answer $y$ to a question $x$.",
            r"Prove that $\pi^* \propto \pi_{\mathrm{ref}}\, e^{r/\beta}$ maximizes $\mathbb E_\pi[r] - \beta\, "
            r"\mathrm{KL}(\pi \,\|\, \pi_{\mathrm{ref}})$, \ and that the maximum is $\beta \log Z$.",
            r"Show that best-of-$n$ sampling has $\mathrm{KL}(\pi_{\mathrm{BoN}} \,\|\, \pi_{\mathrm{ref}}) = \log n - "
            r"(n-1)/n$ when the reward has no ties.",
            r"Compute the gradient of the DPO loss for one pair, \ and show that it is weighted by "
            r"$\sigma(\hat r_l - \hat r_w)$, \ where $\hat r = \beta \log \pi_\theta / \pi_{\mathrm{ref}}$.",
            r"A LoRA adapter of rank $r$ on a $d \times k$ matrix has $r(d + k)$ parameters. \ For $d = k = 4096$, at "
            r"what rank does it have as many as the matrix?",
            r"Fit a Gaussian $q$ to any density $p$ by minimizing $\mathrm{KL}(p \,\|\, q)$. \ Show that $q$ has "
            r"the mean and variance of $p$.",
            r"Show that $\mathbb E_{y \sim \pi}[\, b\, \nabla \log \pi(y)] = 0$ for any $b$ that does not depend on "
            r"$y$, \ and that $r_i - \operatorname{mean}(r) = \frac{k-1}{k}\big(r_i - \operatorname{mean}_{j \ne i} "
            r"r_j\big)$ for $k$ answers.",
            r"Let gold $G \sim \mathcal N(0, \sigma_G^2)$ and a proxy $R = G + E$, \ with independent $E \sim "
            r"\mathcal N(0, \sigma_E^2)$. \ Show that $\mathbb E[G \mid R = r] = r\, \sigma_G^2 / (\sigma_G^2 + "
            r"\sigma_E^2)$: \ what choosing by the proxy costs.",
        ], font_size=21)
        with self.voiceover(
            "Here are eight problems to try, from the Bradley-Terry model to regressional Goodhart. Pause here, and "
            "work through them; full solutions are in this part's notes."
        ) as vo:
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows], lag_ratio=0.3),
                      run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 28, \ Reasoning", font_size=40).to_edge(UP, buff=0.5)
        steps = VGroup(*[node_box(t, c, font_size=26) for t, c in ((r"a problem", GREY_B),
                                                                  (r"$k$ chains of thought", ASSIST),
                                                                  (r"a checker: \ right or wrong", REWARD),
                                                                  (r"GRPO: \ compare within the group", POLICY))])
        steps.arrange(RIGHT, buff=0.55).move_to(DOWN * 0.2)
        if steps.width > 13.2:
            steps.width = 13.2
        arrs = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.08, color=GREY_B, stroke_width=2.5)
                        for a, b in zip(steps, steps[1:])])
        more = label(r"and what thinking longer buys", font_size=28, color=GOLD).next_to(steps, DOWN, buff=0.8)
        with self.voiceover(
            "Next time: reasoning. Why writing out steps adds computation, how a model learns from a checker instead "
            "of a person, with GRPO derived, and what thinking longer buys."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[AnimationGroup(FadeIn(s_), *([GrowArrow(arrs[i - 1])] if i else []))
                                    for i, s_ in enumerate(steps)], lag_ratio=0.5), run_time=max(3.0, vo.duration - 2.5))
            self.play(FadeIn(more))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        card = reference_card(
            [r"N.~Lambert, \textit{Reinforcement Learning from Human Feedback} (2025), \ free at rlhfbook.com",
             r"R.~S.~Sutton \& A.~G.~Barto, \textit{Reinforcement Learning: An Introduction}, 2nd ed.\ (2018)"],
            [r"Christiano et al.\ (2017); \ Stiennon et al.\ (2020); \ Ouyang et al., \textit{InstructGPT} (2022); \ "
             r"Bai et al.\ (2022a, 2022b)",
             r"Wei et al., \textit{FLAN} (2021); \ Taori et al., \textit{Alpaca} (2023); \ Zhou et al., \textit{LIMA} "
             r"(2023)",
             r"Li et al.\ (2018); \ Aghajanyan et al.\ (2020); \ Hu et al., \textit{LoRA} (2021); \ Dettmers et al., "
             r"\textit{QLoRA} (2023); \ Biderman et al.\ (2024)",
             r"Bradley \& Terry (1952); \ Gao, Schulman \& Hilton (2023); \ Rafailov et al., \textit{DPO} (2023); \ "
             r"Azar et al.\ (2023); \ Ethayarajh et al.\ (2024)",
             r"Lee et al., \textit{RLAIF} (2023); \ Guan et al., \textit{Deliberative alignment} (2024); \ Anthropic, "
             r"\textit{Claude's constitution} (2026)",
             r"Hinton, Vinyals \& Dean (2015); \ Kim \& Rush (2016); \ Gu et al., \textit{MiniLLM} (2024); \ Agarwal "
             r"et al., \textit{GKD} (2024)",
             r"Frankle et al.\ (2020); \ Wortsman et al.\ (2022); \ Ilharco et al.\ (2023); \ Yadav et al.\ (2023); \ "
             r"Yu et al.\ (2024)",
             r"Sharma et al.\ (2023); \ Zou et al.\ (2023); \ Anil et al.\ (2024); \ Greenblatt et al.\ (2024); \ "
             r"Betley et al.\ (2025); \ Chen et al.\ (2025)",
             r"Touvron et al.\ (2023); \ Tunstall et al.\ (2023); \ Lambert et al., \textit{T\"ulu 3} (2024); \ "
             r"DeepSeek-AI (2025); \ Qwen Team (2025)"])
        credit = note(narration_credit(), font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "The best place to go deeper on this part is Nathan Lambert's free book on reinforcement learning from "
            "human feedback. Thanks for watching, and see you in Part 28."
        ):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(1.5)
        self.clear_scene()
