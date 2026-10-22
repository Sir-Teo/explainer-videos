from __future__ import annotations

import math

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai28.common import (CHAIN, DIRECT, ENT, LEN, ORM_C, PART, PASS, POLICY, PRM_C, REF, RIGHT_C, VOTE,
                                   WRONG_C, heat, load, tile_frame)


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

        def box_axes(xr, yr):
            return Axes(x_range=xr, y_range=yr, x_length=TW * 0.9, y_length=TH * 0.85, tips=False,
                        axis_config={"stroke_color": GREY_D, "include_ticks": False})

        out = []
        p = load("parity")
        bars = VGroup()
        for i, n in enumerate(p["ns"]):
            for j, (m, col) in enumerate((("direct", DIRECT), ("chain", CHAIN))):
                v = float(np.mean(p[f"accs_{m}{n}"]))
                bars.add(Rectangle(width=0.3, height=max(1.6 * v, 0.01), stroke_width=0, fill_color=col, fill_opacity=0.9)
                         .move_to([i * 0.9 + j * 0.34, 0.8 * v, 0]))
        out.append((bars, r"a chain is computation", CHAIN))
        v = load("think_vote")
        ks = np.log2(v["ks"])
        ax = box_axes([0, ks[-1]], [0.4, 1])
        out.append((VGroup(ax, curve(ax, ks, v["think_vote"], VOTE, 3), curve(ax, ks, v["think_pass"], PASS, 3)),
                    r"many chains, \ one vote", VOTE))
        f = load("think_verify")
        Ns = np.log2(f["Ns"])
        ax = box_axes([0, Ns[-1]], [0.4, 1])
        out.append((VGroup(ax, curve(ax, Ns, f["bo_orm"], ORM_C, 3), curve(ax, Ns, f["bo_prm"], PRM_C, 3)),
                    r"grading steps or answers", PRM_C))
        r = load("rl")
        cv = np.asarray(r["curve"])
        ax = box_axes([0, cv[-1, 0]], [0, 1])
        out.append((VGroup(ax, curve(ax, cv[:, 0], cv[:, 1], CHAIN, 3)), r"learning from a checker", POLICY))
        o = load("objectives")
        ax = box_axes([0, int(o["steps"])], [0, 3])
        ent = VGroup(ax)
        for vv, col in (("grpo", CHAIN), ("dapo", C.BITS), ("pg", GREY_B)):
            Cm = np.asarray(o[f"{vv}_curve"])
            ent.add(curve(ax, Cm[:, 0], Cm[:, 2], col, 3))
        out.append((ent, r"entropy falls", ENT))
        d = load("think_rl")
        Hs = np.asarray(d["gentle_snap_hist"])[-1][:, :max(d["ns"]) + 2]
        out.append((heat(Hs / np.maximum(Hs.sum(1, keepdims=True), 1), 2.6, 1.8, color=CHAIN, vmax=1.0),
                    r"how long to think", LEN))
        ksk = np.log2(o["ks"])
        ax = box_axes([0, ksk[-1]], [0.3, 1])
        out.append((VGroup(ax, curve(ax, ksk, o["passk_base"], REF, 3), curve(ax, ksk, o["passk_grpo"], POLICY, 3)),
                    r"sharper, \ or wider?", REF))
        b = load("think_budget")
        ax = box_axes([0, float(max(np.max(b["sft_seq_tokens"]), np.max(b["sft_vote_tokens"])))], [0, 1])
        out.append((VGroup(ax, curve(ax, b["sft_seq_tokens"], b["sft_seq"], CHAIN, 3),
                           curve(ax, b["sft_vote_tokens"], b["sft_vote"], VOTE, 3)), r"longer, \ or more often?", PASS))
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
            "Let's take stock. Writing out steps lets a model of fixed depth compute for longer: each token buys "
            "another pass through the network. Sampling many chains and voting amplifies whatever answer the model "
            "already prefers; a checker, or a grader of steps, does better. Reinforcement learning from a checker, "
            "with GRPO's group baseline and its clip, moves probability onto answers that check out, and spends the "
            "model's entropy to do it. Left alone, it learns to think longer, sometimes too long, until thought is "
            "given a price. It sharpens what the model could already do, and may, with long enough training, widen "
            "it. And at answer time, more computation buys more right answers, in parallel or in sequence."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.15, scale=0.95) for t_ in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"reasoning over hundreds of steps, \ with tools", [29]),
            (r"every token of thought costs time", [19]),
            (r"is the written chain how the model really decided?", [30]),
            (r"reward hacking; \ watching the chain of thought", [31]),
        ], font_size=26)
        with self.voiceover(
            "All of this comes back. Reasoning over hundreds of steps, with tools, is what agents do, in Part 29. "
            "Every token of thought costs time to generate, and Part 19's inference tricks are what make long "
            "thinking affordable. Whether the chain a model writes is really how it reached its answer is a question "
            "for Part 30. And reward hacking, and watching a model's chain of thought for signs of it, come back in "
            "the last part."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"GRPO's baseline includes the answer's own reward. \ Show that the leave-one-out mean "
            r"$\frac{1}{G-1}\sum_{j \ne i} r_j$ gives an unbiased gradient, \ and that the plain group mean scales it by "
            r"$\frac{G-1}{G}$.",
            r"With $r = \pi_{\mathrm{ref}}(y) / \pi_\theta(y)$ and $y \sim \pi_\theta$, \ show that $k_3 = (r - 1) - \log r$ "
            r"is never negative and that $\mathbb E[k_3] = \mathrm{KL}(\pi_\theta \,\|\, \pi_{\mathrm{ref}})$.",
            r"If $c$ of $n$ independent samples are right, \ prove that $\mathbb E\big[\binom{n-c}{k} / \binom{n}{k}\big] "
            r"= (1-p)^k$.",
            r"Answers $y$ have probabilities $p_y$, \ the right one $p^* > p_y + \Delta$ for every wrong $y$. \ Bound the "
            r"chance a vote over $k$ samples is wrong, \ with $m$ possible answers.",
            r"For best-of-$N$ with a $0/1$ checker, \ show $\mathrm{KL}(\pi_N \,\|\, \pi) = \mathrm{KL}\big("
            r"\text{Bern}(1-q) \,\|\, \text{Bern}(p)\big)$, \ $q = (1-p)^N$, \ and find its limit.",
            r"For $\pi = \operatorname{softmax}(z)$, \ show $\partial H / \partial z_b = -\pi_b(\log \pi_b - "
            r"\mathbb E_\pi[\log \pi])$, \ and that a step $\Delta z$ changes the entropy by $-\operatorname{Cov}_\pi"
            r"(\log \pi, \Delta z)$ to first order.",
        ], font_size=22)
        with self.voiceover(
            "Here are six problems to try, from GRPO's baseline to the entropy's fall. Pause here, and work through "
            "them; full solutions are in this part's notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows], lag_ratio=0.3),
                      run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        s = load("think_samples")
        ps = float(s["p_step"])
        ns = np.arange(1, 201)
        head = label(r"Next: \ Part 29, \ Agents and Worlds", font_size=40).to_edge(UP, buff=0.4)
        g = axes([0, 200], [0, 1], x_length=7.2, y_length=3.6, xlabel=r"steps in a row",
                 ylabel=r"chance every step is right", xticks=[0, 100, 200], yticks=[0, 0.5, 1],
                 yfmt=lambda v: rf"{int(100 * v)}\%", center=[-1.2, -0.6, 0])
        c_ = curve(g.ax, ns, ps ** ns, WRONG_C, 4)
        n50 = math.log(0.5) / math.log(ps) if ps < 1 else float("inf")
        mk = DashedLine(g.ax.c2p(n50, 0), g.ax.c2p(n50, 0.5), color=GREY_B, dash_length=0.06) if n50 < 200 else VMobject()
        eq = cmath(r"P(\text{all } n \text{ right})", r"=", rf"{ps:.3f}^{{\,n}}", font_size=34).move_to([4.4, 1.6, 0])
        nl = label(rf"our model's steps: \ right ${100 * ps:.1f}\%$ of the time", font_size=20, color=GREY_A)
        nl.next_to(eq, DOWN, buff=0.25)
        tag = note(r"computed: \ the think-or-answer model before RL, \ every step checked").to_corner(DR, buff=0.2)
        if n50 < 200:
            half = (f"Even at {100 * ps:.1f} percent a step, a chain of {n50:.0f} steps is a coin flip, and of two "
                    "hundred, almost hopeless.")
        else:
            half = f"At {100 * ps:.1f} percent a step, even two hundred steps usually survive."
        with self.voiceover(
            "Next time: agents, models that act over many steps, in the world or on a computer. Here is the problem "
            "they face, measured on our own chains. Each step of thought our adding model writes is right "
            f"{100 * ps:.1f} percent of the time. <bookmark mark='a'/> But a long task needs every step right, and "
            f"those chances multiply. {half} <bookmark mark='b'/> How agents plan, check themselves and recover over "
            "long horizons, and how they learn models of the worlds they act in: Part 29."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(tag), Write(eq), FadeIn(nl))
            vo.wait_until("a")
            self.play(Create(c_), run_time=2.0)
            self.play(Create(mk))
            vo.wait_until("b")
            self.play(Indicate(eq, color=WRONG_C))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        books = [r"N.~Lambert, \textit{Reinforcement Learning from Human Feedback} (2025), \ chapters on RLVR and "
                 r"reasoning; \ R.~S.~Sutton \& A.~G.~Barto, \textit{Reinforcement Learning} (2nd ed., 2018)"]
        papers = [
            r"Nye et al.\ (2021); \ Wei et al.\ (2022); \ Kojima et al.\ (2022); \ Wang et al.\ (2022); \ Merrill \& "
            r"Sabharwal (2023, 2024); \ Li et al.\ (2024); \ Pfau, Merrill \& Bowman (2024)",
            r"Cobbe et al.\ (2021); \ Uesato et al.\ (2022); \ Lightman et al.\ (2023); \ Wang et al., "
            r"\textit{Math-Shepherd} (2023); \ Chen et al., \textit{Codex} (2021)",
            r"Shao et al., \textit{DeepSeekMath} (2024); \ Lambert et al., \textit{T\"ulu 3} (2024); \ DeepSeek-AI, "
            r"\textit{R1} (2025); \ Kimi Team, \textit{k1.5} (2025)",
            r"Liu et al., \textit{Dr.~GRPO} (2025); \ Yu et al., \textit{DAPO} (2025); \ Zheng et al., \textit{GSPO} "
            r"(2025); \ MiniMax, \textit{M1} (2025); \ Schulman (2020); \ Tang \& Munos (2025)",
            r"Cui et al.\ (2025); \ Yue et al.\ (2025); \ Liu et al., \textit{ProRL} (2025); \ Chen et al.\ (2024); \ "
            r"Aggarwal \& Welleck, \textit{L1} (2025)",
            r"Snell et al.\ (2024); \ Muennighoff et al., \textit{s1} (2025); \ Beirami et al.\ (2024); \ Yao et al., "
            r"\textit{Tree of Thoughts} (2023); \ Guan et al., \textit{rStar-Math} (2025)",
            r"Hao et al., \textit{Coconut} (2024); \ Wang et al., \textit{HRM} (2025); \ Jolicoeur-Martineau, "
            r"\textit{TRM} (2025); \ Korbak et al.\ (2025)",
            r"Hubert et al., \textit{AlphaProof} (2025); \ Chollet (2019); \ ARC Prize reports (2024--2026); \ OpenAI, "
            r"\textit{Learning to Reason with LLMs} (2024)",
        ]
        card = reference_card(books, papers)
        data = note(r"Every number here is computed on this computer or cited; \ schematics and illustrations are "
                    r"labelled.", font_size=20).to_edge(DOWN, buff=0.25)
        credit = note(rf"Animated with Manim Community; \ narrated by {narration_credit()}.", font_size=20)
        credit.next_to(data, UP, buff=0.1)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.15:
            card.scale((card.height - (credit.get_top()[1] + 0.15 - card.get_bottom()[1])) / card.height).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Nathan Lambert's free book on reinforcement learning from human feedback is the place to go deeper; it "
            "covers reinforcement learning with verifiable rewards and reasoning too. Thanks for watching, "
            "and see you in Part 29."
        ):
            self.play(LaggedStart(FadeIn(card), FadeIn(credit), FadeIn(data), lag_ratio=0.3), run_time=3)
        self.wait(2.0)
        self.clear_scene()
