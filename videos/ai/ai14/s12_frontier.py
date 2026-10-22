from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai14.common import (CLOSED, C_COL, DECODER, OPEN, PART, PRIOR, F, config_card, human, load,
                                   month_year, take_away, year_of)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.deepseek()
        self.wave()
        self.sparse()
        self.hybrids()
        self.gap()

    def card(self):
        card = chapter_card(11, r"The open frontier, 2024 to 2026", r"What does a frontier model look like now?",
                            lit=(2025, 2026), part=PART)
        with self.voiceover("Chapter eleven. The open frontier, 2024 to 2026."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def deepseek(self):
        D, R = F.DSV3, F.R1
        P = load("published")
        card = config_card(F.CFG["dsv3"], rows=("layers", "d", "params", "active", "tokens"), width=4.6)
        card.move_to([-4.4, 0.6, 0])
        news = VGroup(
            label(r"$256$ small experts $+ 1$ shared; \ $8$ chosen per token", font_size=22, color=C.EXPERT),
            label(r"multi-head latent attention", font_size=22, color=C.LATENT),
            label(r"experts balanced without an extra loss", font_size=22, color=C.BALANCE),
            label(r"trained to predict two tokens at a time", font_size=22, color=GREY_A),
            label(r"8-bit floating point, \ at this scale for the first time", font_size=22, color=C.QUANT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([2.4, 1.6, 0])
        cost = VGroup(label(rf"${D['gpu_hours'] / 1e6:.3f}$ million H800 GPU-hours $\times$ \${D['rate']:.0f} "
                            rf"$= $ \${P['dsv3_usd'] / 1e6:.3f} million", font_size=24, color=C_COL),
                      label(r"the final run only: \ not the research before it", font_size=20, color=GREY_B))
        cost.arrange(DOWN, buff=0.12).move_to([2.4, -0.6, 0])
        r1 = history_card(2025, r"DeepSeek-R1 \ (January)", rf"reinforcement learning on checkable answers; \ R1-Zero on "
                          rf"AIME 2024: \ ${R['aime_start']}\% \to {R['aime_zero']}\%$ during training; \ open weights, "
                          r"MIT license \ (Part 28)", width=7.4, color=OPEN).move_to([2.4, -2.4, 0])
        with self.voiceover(
            "December 2024: DeepSeek-V3. 671 billion parameters, 37 billion used per token. <bookmark mark='a'/> A "
            "mixture of 256 small experts plus one shared, eight chosen per token; latent attention; a way to keep the "
            "experts balanced without an extra loss; training to predict two tokens at a time; and training in "
            "eight-bit floating point, at this scale, for the first time. Fourteen point eight trillion tokens. "
            "<bookmark mark='b'/> Its report stated the cost: 2.788 million GPU-hours, about 5.6 million dollars at "
            "two dollars an hour, for the final run alone, not the research before it. <bookmark mark='c'/> A month "
            "later, DeepSeek-R1, trained from V3 with reinforcement learning on problems whose answers can be checked. "
            f"Its pure-RL version went from {R['aime_start']} to {R['aime_zero']} percent on the AIME 2024 mathematics "
            "competition during training. Open weights, under the MIT license; Part 28 explains how."
        ) as vo:
            self.play(FadeIn(card, shift=RIGHT * 0.15))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(n_, shift=LEFT * 0.1) for n_ in news], lag_ratio=0.35), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(cost, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(r1, shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def wave(self):
        Q, K, G, O = F.QWEN3, F.KIMIK2, F.GLM45, F.GPTOSS
        k2, g45, oss = F.CFG["kimik2"], F.CFG["glm45"], F.CFG["gptoss"]
        cards = VGroup(
            history_card(2025, r"Qwen3 \ (Alibaba, April)", rf"dense and mixture-of-experts, \ $0.6$B to $235$B; "
                         rf"\ ${Q['tokens'] / 1e12:.0f}$T tokens, \ ${Q['languages']}$ languages; \ thinking and "
                         r"non-thinking modes in one model", width=6.4, color=OPEN),
            history_card(2025, r"Kimi K2 \ (Moonshot AI, July)", rf"{human(k2['params'])} parameters, "
                         rf"{human(k2['active'])} active; \ ${K['tokens'] / 1e12:.1f}$T tokens with the MuonClip "
                         r"optimizer, \ without a single loss spike", width=6.4, color=OPEN),
            history_card(2025, r"GLM-4.5 \ (Zhipu AI, July)", rf"{human(g45['params'])} parameters, "
                         rf"{human(g45['active'])} active; \ ${G['tokens'] / 1e12:.0f}$T tokens", width=6.4,
                         color=OPEN),
            history_card(2025, r"gpt-oss \ (OpenAI, August)", rf"{human(oss['params'])} parameters, "
                         rf"{human(oss['active'])} active; \ 4-bit weights fit one 80 GB GPU; \ Apache 2.0: \ OpenAI's "
                         r"first open weights since GPT-2", width=6.4, color=OPEN),
        ).arrange_in_grid(rows=2, cols=2, buff=0.3).move_to(DOWN * 0.1)
        head = label(r"the open frontier fills in, \ 2025", font_size=34, color=OPEN).to_edge(UP, buff=0.45)
        cite_ = cite(r"Qwen Team (2025); \ Kimi Team (2025); \ GLM-4.5 Team (2025); \ OpenAI (2025)")
        with self.voiceover(
            "Through 2025 the open frontier filled in. <bookmark mark='a'/> Qwen3, in April: dense and "
            "mixture-of-experts models from 0.6 to 235 billion parameters, 36 trillion tokens, 119 languages, and "
            "thinking and non-thinking modes in one model. <bookmark mark='b'/> Kimi K2, from Moonshot AI in July: a "
            "trillion parameters, 32 billion active, trained on 15.5 trillion tokens with a new optimizer, MuonClip, "
            "without a single spike in the loss. <bookmark mark='c'/> GLM-4.5, from Zhipu, the same month. "
            "<bookmark mark='d'/> And in August, OpenAI's first open weights since GPT-2: gpt-oss, 117 billion "
            "parameters with 5.1 billion active, its weights in a four-bit format so that it fits on a single GPU, "
            "under the Apache license."
        ) as vo:
            self.play(FadeIn(cite_), FadeIn(head))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sparse(self):
        P = load("published")
        pts = [c for c in F.CONFIGS if c["key"] in ("gpt3", "palm", "llama", "llama2", "mistral", "llama3") or
               c.get("active")]
        extra = [("Mixtral", 47e9, 13e9, "2023-12-11"), ("DeepSeek-V2", 236e9, 21e9, "2024-05-07"),
                 ("GLM-5", 744e9, 40e9, "2026-02-11"), ("MiMo-V2.6-Pro", 1.02e12, 42e9, "2026-09-21")]
        g = axes([9.5, 12.6], [9.5, 12.6], x_length=5.6, y_length=5.6, xlabel=r"total parameters",
                 ylabel=r"parameters used per token", xticks=[10, 11, 12], yticks=[10, 11, 12],
                 xfmt=lambda v: rf"10^{{{int(v)}}}", yfmt=lambda v: rf"10^{{{int(v)}}}", center=[-2.2, -0.3, 0])
        ax = g.ax
        diag = DashedLine(ax.c2p(9.5, 9.5), ax.c2p(12.6, 12.6), color=GREY_C, dash_length=0.08)
        dl = label(r"dense: \ every parameter, \ every token", font_size=18, color=GREY_B)
        dl.rotate(PI / 4).move_to(ax.c2p(10.3, 10.75))
        dense, moe = VGroup(), VGroup()
        for c in pts:
            n, a = c["params"], c.get("active") or c["params"]
            d = Dot(ax.c2p(math.log10(n), math.log10(a)), radius=0.08, color=PRIOR if a == n else OPEN)
            (dense if a == n else moe).add(d)
        for nm, n, a, _ in extra:
            moe.add(Dot(ax.c2p(math.log10(n), math.log10(a)), radius=0.08, color=OPEN))
        k3 = F.CFG["kimik3"]
        k3d = moe[[c["key"] for c in pts if c.get("active")].index("kimik3")]
        ring = Circle(radius=0.2, color=YELLOW, stroke_width=3).move_to(k3d)
        k3l = label(r"Kimi K3", font_size=20, color=YELLOW).next_to(ring, UP, buff=0.05)
        share = P["active_share"]
        tab = VGroup(*[label(rf"{F.CFG[k]['name']}: \ ${100 * share[k]:.1f}\%$", font_size=22, color=OPEN)
                       for k in ("dsv3", "qwen3", "kimik2", "gptoss", "qwen35", "dsv4", "kimik3")])
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.4, 0.0, 0])
        th = label(r"share of parameters \\ used for each token", font_size=24, color=WHITE).next_to(tab, UP, buff=0.3)
        with self.voiceover(
            "Put the models of this part on one chart: their total parameters against the parameters each token "
            "actually uses. <bookmark mark='a'/> Dense models sit on the diagonal: GPT-3, PaLM, LLaMA, Llama 3.1 use "
            "every parameter for every token. <bookmark mark='b'/> The open frontier moved below it. A mixture of "
            "experts routes each token through a few small networks out of hundreds, so capacity grows while the cost "
            f"per token doesn't. <bookmark mark='c'/> Kimi K3 uses {k3['active'] / 1e9:.0f} billion of its "
            f"{k3['params'] / 1e12:.1f} trillion: {100 * share['kimik3']:.1f} percent. The frontier is sparse, and "
            "Part 16 is about how that works."
        ) as vo:
            self.play(FadeIn(g), Create(diag), FadeIn(dl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in dense], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in moe], lag_ratio=0.12), FadeIn(th),
                      LaggedStart(*[FadeIn(t) for t in tab], lag_ratio=0.2), run_time=3.0)
            vo.wait_until("c")
            self.play(Create(ring), FadeIn(k3l))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hybrids(self):
        H = F.HYBRIDS
        x0, x1 = 2024.0, 2026.8
        line = Line([-6.2, 2.0, 0], [6.2, 2.0, 0], color=GREY_C, stroke_width=2)
        X = lambda y: -6.2 + 12.4 * (y - x0) / (x1 - x0)
        ticks = VGroup(*[VGroup(Line([X(y), 1.92, 0], [X(y), 2.08, 0], color=GREY_C),
                                label(str(y), font_size=18, color=GREY_B).move_to([X(y), 2.35, 0])) for y in (2024, 2025, 2026)])
        marks = VGroup()
        for k, (d, nm, how, org, _) in enumerate(H):
            x = X(year_of(d))
            dot = Dot([x, 2.0, 0], radius=0.08, color=C.MEMORY)
            up = k % 2 == 0
            t = VGroup(label(nm, font_size=20, color=C.MEMORY), label(how, font_size=16, color=GREY_A)).arrange(DOWN, buff=0.04)
            t.move_to([x, 2.0 + (0.85 if up else -0.75), 0])
            if t.get_left()[0] < -6.9:
                t.shift(RIGHT * (-6.9 - t.get_left()[0]))
            if t.get_right()[0] > 6.9:
                t.shift(LEFT * (t.get_right()[0] - 6.9))
            marks.add(VGroup(dot, t))
        flag = [("qwen35", r"Qwen3.5", r"Feb 2026: \ $397$B, \ $17$B active; \ gated DeltaNet $3 : 1$"),
                ("glm5", r"GLM-5", r"Feb 2026: \ $744$B, \ $40$B active; \ sparse attention; \ $28.5$T tokens"),
                ("dsv4", r"DeepSeek-V4", r"Apr 2026: \ $1.6$T, \ $49$B active; \ compressed sparse attention; "
                 r"\ $1$M context"),
                ("kimik3", r"Kimi K3", r"Jul 2026: \ $2.8$T, \ $104$B active; \ $69$ KDA $+ 24$ MLA layers; \ $1$M context")]
        cards = VGroup(*[VGroup(label(nm, font_size=26, color=OPEN), label(t, font_size=20, color=GREY_A))
                         .arrange(DOWN, aligned_edge=LEFT, buff=0.08) for _, nm, t in flag])
        cards.arrange_in_grid(rows=2, cols=2, buff=(0.6, 0.35), cell_alignment=UL).move_to(DOWN * 1.7)
        frames = VGroup(*[SurroundingRectangle(c, color=GREY_D, buff=0.15, corner_radius=0.1) for c in cards])
        cite_ = cite(r"Lieber et al.\ (2024); \ MiniMax (2025); \ NVIDIA (2025); \ Kimi Team (2025); \ model cards: "
                     r"Qwen3-Next, Qwen3.5, GLM-5, DeepSeek-V4, Kimi K3", corner=DL, font_size=16)
        with self.voiceover(
            "And the attention began to change. Its cost grows with the length of the context, and frontier models "
            "now read a million tokens. <bookmark mark='a'/> Hybrids replace most attention layers with layers whose "
            "memory stays a fixed size: AI21's Jamba in 2024; MiniMax-01 and NVIDIA's Nemotron-H in 2025; then Qwen3-Next "
            "and Moonshot's Kimi Linear, with three such layers for every attention layer. <bookmark mark='b'/> By "
            "2026 the flagships were built this way, or with sparse attention. Qwen3.5, in February: a three-to-one "
            "hybrid. GLM-5, the same month: 744 billion parameters with DeepSeek's sparse attention. "
            "<bookmark mark='c'/> DeepSeek-V4, in April: 1.6 trillion parameters, compressed sparse attention, a "
            "million-token context. And Kimi K3, in July: 2.8 trillion parameters, sixty-nine layers of Kimi Delta "
            "Attention and twenty-four of latent attention. <bookmark mark='d'/> Parts 15 and 16 take these apart. "
            "The convergence of 2023 was real, but it was a pause: when contexts grew long and models grew sparse, the "
            "designs began to diverge again."
        ) as vo:
            self.play(Create(line), FadeIn(ticks), FadeIn(cite_))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in marks], lag_ratio=0.3), run_time=3.5)
            vo.wait_until("b")
            self.play(FadeIn(cards[0]), Create(frames[0]))
            self.play(FadeIn(cards[1]), Create(frames[1]))
            vo.wait_until("c")
            self.play(FadeIn(cards[2]), Create(frames[2]))
            self.play(FadeIn(cards[3]), Create(frames[3]))
            vo.wait_until("d")
            self.play(Indicate(cards, scale_factor=1.02))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gap(self):
        A = load("aa")
        op, cl = A["open"], A["closed"]
        top = max(r[1] for r in cl) * 1.08
        g = axes([2022.8, 2026.9], [0, top], x_length=8.2, y_length=4.4, xlabel=r"release date",
                 ylabel=r"Artificial Analysis Intelligence Index \ (running best)", xticks=[2023, 2024, 2025, 2026],
                 yticks=[0, 20, 40], xfmt=lambda v: f"{int(v)}", center=[-1.8, -0.3, 0])
        ax = g.ax

        def steps(best, color):
            pts = []
            for k, (y, s, _) in enumerate(best):
                if k:
                    pts.append(ax.c2p(y, best[k - 1][1]))
                pts.append(ax.c2p(y, s))
            pts.append(ax.c2p(2026.85, best[-1][1]))
            return VMobject(color=color, stroke_width=4).set_points_as_corners(pts)

        lc, lo = steps(cl, CLOSED), steps(op, OPEN)
        lg = legend([(CLOSED, r"best closed model"), (OPEN, r"best open-weights model")], font_size=20)
        lg.move_to(ax.c2p(2023.0, top * 0.92), aligned_edge=UL)
        lags = np.array([l["months"] for l in A["lag"] if l["months"] is not None])
        recent = [l for l in A["lag"] if l["year"] >= 2025.0 and l["months"] is not None]
        med_all, med_recent = float(np.median(lags)), float(np.median([l["months"] for l in recent]))
        last = A["lag"][-1]
        side = VGroup(
            label(r"each new open record \\ had been reached by a \\ closed model earlier by:", font_size=22, color=GREY_A),
            label(rf"median ${med_all:.1f}$ months", font_size=28, color=OPEN),
            label(rf"since 2025: \ ${med_recent:.1f}$ months", font_size=24, color=OPEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.8, 0.3, 0])
        caveat = note(rf"one index, \ AA v4.3.2 as of {A['meta']['fetched']}; \ scores change as the index changes",
                      font_size=18).to_corner(DR, buff=0.2)
        if med_recent < med_all - 0.5:
            verdict = (f"Since 2025 the median lag has been {med_recent:.1f} months, shorter than before: the open models "
                       "have been catching up.")
        else:
            verdict = (f"Since 2025 the median lag has been {med_recent:.1f} months, about the same as before: the open "
                       "models follow closely, but they have not closed the gap.")
        with self.voiceover(
            "How far behind the closed frontier are the open models? One independent index, from Artificial Analysis, "
            "scores models on ten evaluations. <bookmark mark='a'/> Here is the best closed model's score over time, "
            "<bookmark mark='b'/> and the best open model's. <bookmark mark='c'/> For each new open record, ask when a "
            f"closed model first scored as high. Across all of them, the median lag is {med_all:.1f} months. "
            f"<bookmark mark='d'/> " + verdict + f" The latest open record, {last['name']}, trailed by "
            f"{last['months']:.1f} months."
        ) as vo:
            self.play(FadeIn(g), FadeIn(caveat))
            vo.wait_until("a")
            self.play(Create(lc), FadeIn(lg[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(lo), FadeIn(lg[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.wait(0.3)
        self.clear_scene()

