from __future__ import annotations

import math

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai30.common import (CAUSE, CHAT, CTRL, FEAT, PART, PROBE, RESID, heat_image, load, node_box)

PH = [GREY_D, C.TRUE_P, C.BITS]


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
        mk = lambda xr, yr: Axes(x_range=xr, y_range=yr, x_length=TW * 0.9, y_length=TH * 0.85, tips=False,  # noqa: E731
                                 axis_config={"stroke_color": GREY_D, "include_ticks": False})
        out = []
        p = load("probes")
        L = int(p["layers"])
        ax = mk([0, L - 1, 1], [0.5, 1, 0.25])
        out.append((VGroup(ax, curve(ax, range(L), np.asarray(p["lin_task"]).mean(0), PROBE, 3),
                           DashedVMobject(curve(ax, range(L), np.asarray(p["lin_ctrl"]).mean(0), PROBE, 2), num_dashes=20)),
                    r"probes, \ and controls", PROBE))
        le = load("lens")
        lk, tk = np.asarray(le["logit_kl"]), np.asarray(le["tuned_kl"])
        ax = mk([0, len(lk) - 1, 1], [0, float(lk.max()), 1])
        out.append((VGroup(ax, curve(ax, range(len(lk)), lk, PROBE, 3), curve(ax, range(len(tk)), tk, C.MLP, 3)),
                    r"logit and tuned lens", C.MLP))
        ind = load("induction")
        H = np.clip(np.asarray(ind["heat"])[:, : int(ind["target"]) + 4], 0, 1)
        out.append((heat_image(H[::-1], TW, TH * 0.6, color=CAUSE, gamma=0.7), r"activation patching", CAUSE))
        kp = np.asarray(ind["snap_kpath"])
        cv = np.asarray(ind["curve"])
        ax = mk([0, float(cv[-1, 0]), 1], [0, float(cv[:, 1].max()), 1])
        dm = np.clip(kp[:, 1], 0, None)
        out.append((VGroup(ax, curve(ax, cv[:, 0], cv[:, 1], CAUSE, 3),
                           curve(ax, kp[:, 0], dm / max(dm.max(), 1e-9) * float(cv[:, 1].max()), C.BITS, 3)),
                    r"an induction circuit", C.BITS))
        ph = load("phase")
        emp = np.asarray(ph["emp"])
        n, m = emp.shape
        cell = min(TW / m, TH / n)
        out.append((VGroup(*[Square(cell, stroke_width=0, fill_color=PH[int(emp[i, j])], fill_opacity=0.9)
                             .move_to([j * cell, i * cell, 0]) for i in range(n) for j in range(m)]),
                    r"the phase diagram", C.BITS))
        fr = load("frontier")
        g = VGroup(mk([1, 6, 1], [0, 1, 0.5]))
        for kind, key, col in (("l1", "l1s", C.SURPRISE), ("jumprelu", "jumps", C.TRUE_P), ("topk", "ks", C.BITS)):
            pts = sorted((math.log2(max(np.mean([fr[f"{kind}_{q:g}_{s}_l0"] for s in fr["seeds"]]), 1)),
                          float(np.mean([fr[f"{kind}_{q:g}_{s}_fvu"] for s in fr["seeds"]]))) for q in fr[key])
            g.add(curve(g[0], [a for a, _ in pts], [min(b, 1) for _, b in pts], col, 3))
        out.append((g, r"three dictionaries", FEAT))
        gr = load("graph")
        ms, pr = np.asarray(gr["measured"]), np.asarray(gr["predicted"])
        lo, hi = float(min(ms.min(), pr.min())), float(max(ms.max(), pr.max()))
        ax = mk([lo, hi, 1], [lo, hi, 1])
        out.append((VGroup(ax, *[Dot(ax.c2p(a, b), radius=0.03, color=FEAT) for a, b in zip(pr, ms)]),
                    r"an attribution graph, \ tested", FEAT))
        df = load("diffing")
        r = np.asarray(df["rel"])[np.asarray(df["alive"]) > 0]
        h, _ = np.histogram(r, bins=np.linspace(0, 1, 21))
        out.append((VGroup(*[Rectangle(width=TW / 22, height=max(1.3 * v / h.max(), 0.01), stroke_width=0,
                                       fill_color=CHAT if i >= 18 else (GREY_B if i < 2 else C.BITS), fill_opacity=0.9)
                             .move_to([i * TW / 21, 0, 0], aligned_edge=DOWN) for i, v in enumerate(h)]),
                    r"model diffing", CHAT))
        st = load("steering")
        sm = st["speech_mean"]
        vals = [float(sm[f"{a:g}"]) for a in st["alphas"]] + [float(np.mean(st["random_speech"]))]
        out.append((VGroup(*[Rectangle(width=0.35, height=max(1.3 * v / max(max(vals), 1e-9), 0.01), stroke_width=0,
                                       fill_color=C.SURPRISE if i < len(vals) - 1 else CTRL, fill_opacity=0.9)
                             .move_to([0.5 * i, 0, 0], aligned_edge=DOWN) for i, v in enumerate(vals)]),
                    r"steering", C.SURPRISE))
        gk = load("grok")
        s_ = np.asarray(gk["step"], float)
        ax = mk([0, float(s_[-1]), 1], [-8, 2, 1])
        lg = lambda k: np.clip(np.log10(np.clip(np.asarray(gk[k], float), 1e-8, None)), -8, 2)  # noqa: E731
        out.append((VGroup(ax, curve(ax, s_, lg("train_loss"), C.TRUE_P, 3), curve(ax, s_, lg("test_loss"), C.SURPRISE, 3),
                           curve(ax, s_, lg("restricted_loss"), C.BITS, 3)), r"grokking, \ from inside", C.BITS))
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
            "Let's take stock. A probe reads what a layer knows, but only a control task says whether the probe did "
            "the work, and only an intervention says whether the model uses it. Lenses read the stream as it flows. "
            "Patching finds causes, down to two heads that copy, read off their weights and watched forming. "
            "Superposition packs more features than dimensions, a phase the network enters when features are rare; "
            "sparse dictionaries pull them apart, better with TopK and JumpReLU than with L1, though they split and "
            "absorb. Transcoders turn a prediction into a graph we can test, crosscoders diff a model against its "
            "fine-tune, and a direction can steer. Grokking turned out to be a circuit built quietly under a "
            "memorized table."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.15, scale=0.95) for t_ in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"probes on a model's own activations, \ guarding live traffic", [31]),
            (r"auditing for hidden objectives; \ model diffing", [31]),
            (r"reading, and monitoring, \ the chain of thought", [31]),
            (r"understanding the model: \ an open problem", [31]),
        ], font_size=26)
        with self.voiceover(
            "All of it comes back in the finale. Part 31 puts probes in front of a frontier model, audits models "
            "for what they hide, reads and monitors chains of thought, and lists understanding the model among "
            "the open problems."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"An L1 autoencoder rebuilds $x = a\,d$ ($\|d\| = 1$, \ $a > 0$) from one latent: \ minimize $\|x - f d\|^2 + "
            r"\lambda f$ over $f \ge 0$. \ Show $f^* = \max(a - \lambda/2, 0)$, \ and that TopK has no such bias.",
            r"For independent random unit vectors $u, v \in \mathbb{R}^d$, \ show $\mathbb{E}[u \cdot v] = 0$ and "
            r"$\mathbb{E}[(u \cdot v)^2] = 1/d$.",
            r"Show that the composition score $\|A B\|_F / (\|A\|_F \|B\|_F)$ lies in $[0, 1]$, \ and that it is $1$ "
            r"exactly when $A$ and $B$ are rank one and $A$'s right singular vector is $B$'s left one.",
            r"Two inputs feed $y = x_1 \wedge x_2$. \ Clean: \ both true; \ corrupted: \ both false. \ Show that "
            r"noising either input alone destroys $y$, \ while denoising either alone restores nothing.",
            r"Two features, one dimension, density $\rho$, importances $1$ and $r$, \ $x_i \sim U[0, 1]$ when on: \ show "
            r"that keeping feature 1 alone costs $r\rho/3$, \ keeping feature 2 alone $\rho/3$.",
            r"Let $L(c) = \sum_{k \in K} \cos\!\big(2\pi k (a + b - c)/p\big)$ for a prime $p$ and $0 < k < p$. \ Show "
            r"that $c = (a + b) \bmod p$ maximizes $L$, \ uniquely.",
        ], font_size=21)
        with self.voiceover(
            "Here are six problems to try, from soft thresholding to the trigonometry of grokking. Pause here, and "
            "work through them; full solutions are in this part's notes."
        ) as vo:
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows], lag_ratio=0.3),
                      run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 31, \ Can We Trust It?", font_size=40).to_edge(UP, buff=0.5)
        steps = VGroup(*[node_box(t, c, font_size=24) for t, c in ((r"a score", GREY_B), (r"is it real?", C.INTERVAL),
                                                                  (r"is it what we meant?", C.PENALTY),
                                                                  (r"can we oversee it?", C.KL),
                                                                  (r"can we control it?", C.TRUE_P))])
        steps.arrange(RIGHT, buff=0.5).move_to(DOWN * 0.2)
        if steps.width > 13.2:
            steps.width = 13.2
        arrs = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.08, color=GREY_B, stroke_width=2.5)
                        for a, b in zip(steps, steps[1:])])
        more = label(r"and, \ one last time, \ the scoreboard", font_size=28, color=C.BITS).next_to(steps, DOWN, buff=0.8)
        with self.voiceover(
            "Next time, the finale: can we trust it? How to measure a model honestly, what happens when an objective "
            "has a loophole, how to supervise a model stronger than its supervisor, the evidence that models can "
            "deceive, and how to watch and control them. And, one last time, the scoreboard."
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
            [r"C.~Olah et al., \textit{Zoom In: An Introduction to Circuits} (Distill, 2020); \ the Transformer Circuits "
             r"thread, \ transformer-circuits.pub",
             r"L.~Sharkey et al., \textit{Open Problems in Mechanistic Interpretability} (2025)"],
            [r"Simonyan, Vedaldi \& Zisserman (2013); \ Zeiler \& Fergus (2014); \ Adebayo et al.\ (2018); \ Bau et al.\ "
             r"(2017); \ Olah, Mordvintsev \& Schubert (2017); \ Goh et al.\ (2021)",
             r"Alain \& Bengio (2016); \ Hewitt \& Liang (2019); \ Elazar et al.\ (2021); \ nostalgebraist (2020); \ "
             r"Belrose et al., \textit{Tuned Lens} (2023)",
             r"Vig et al.\ (2020); \ Meng et al.\ (2022); \ Wang et al., \textit{IOI} (2022); \ Goldowsky-Dill et al.\ "
             r"(2023); \ Elhage et al.\ (2021); \ Olsson et al.\ (2022)",
             r"Elhage et al., \textit{Toy Models of Superposition} (2022); \ Bricken et al.\ (2023); \ Cunningham et al.\ "
             r"(2023); \ Templeton et al.\ (2024)",
             r"Gao et al.\ (2024); \ Rajamanoharan et al.\ (2024); \ Bussmann et al.\ (2024, 2025); \ Chanin et al.\ "
             r"(2024); \ Paulo \& Belrose (2025); \ Heap et al.\ (2025)",
             r"Dunefsky et al.\ (2024); \ Ameisen et al., \textit{Circuit Tracing} (2025); \ Lindsey et al., \textit{"
             r"Biology} (2025); \ Lindsey et al., \textit{Crosscoders} (2024); \ Minder et al.\ (2025a, b)",
             r"Turner et al.\ (2023); \ Rimsky et al.\ (2024); \ Arditi et al.\ (2024); \ Chen et al., \textit{Persona "
             r"Vectors} (2025); \ Wu et al., \textit{AxBench} (2025)",
             r"Power et al.\ (2022); \ Nanda et al.\ (2023); \ Turpin et al.\ (2023); \ Lanham et al.\ (2023); \ Chen et "
             r"al.\ (2025)",
             r"Marks et al.\ (2025); \ Lindsey (2025); \ Gao et al., \textit{weight-sparse transformers} (2025); \ "
             r"Anthropic, \textit{emotion concepts} and \textit{natural-language autoencoders} (2026)"])
        credit = note(narration_credit(), font_size=18).to_edge(DOWN, buff=0.15)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.1:
            card.shift(UP * (credit.get_top()[1] + 0.1 - card.get_bottom()[1]))
        with self.voiceover(
            "The best place to go deeper is the Transformer Circuits thread, which is free online, and the open "
            "problems survey of 2025. Thanks for watching, and see you in Part 31, the finale."
        ):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(1.5)
        self.clear_scene()
