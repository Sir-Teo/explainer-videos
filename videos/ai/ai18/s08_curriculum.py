from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai18.common import (BASE_C, EDU, F, FULL_C, KEPT, LR_COL, PART, load, spoken_int, take_away)


class Curriculum(VoiceoverScene):
    def construct(self):
        self.card()
        self.wsd()
        self.anneal()
        self.long_context()

    def card(self):
        card = chapter_card(7, r"Annealing, \ mid-training, \ long context", r"Why does the end of a run matter so "
                            r"much?", part=PART)
        with self.voiceover("Chapter seven. Annealing, mid-training, long context."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def wsd(self):
        full, base, br, R = load("recipe_full"), load("recipe_base"), load("recipe_branch"), load("recipe")
        steps = full["spec"]["steps"]
        bstep = br["spec"]["steps"]
        start = br["spec"]["decay_start"]
        cf = np.asarray(full["curve"])
        cb = np.asarray(base["curve"])
        cbr = np.asarray(br["curve"])
        g = axes([0, steps], [0, 1.1], x_length=10.0, y_length=1.6, ylabel=r"learning rate \ (share of the peak)",
                 yticks=[0, 1], center=[0.4, 2.2, 0], font_size=18)
        lr_b = curve(g.ax, cb[:, 0], cb[:, 3], BASE_C, 3)
        lr_f = curve(g.ax, cf[:, 0], cf[:, 3], FULL_C, 3)
        sel = cbr[:, 0] >= start - 2
        lr_br = curve(g.ax, cbr[sel, 0], cbr[sel, 3], KEPT, 3)
        ev_f = np.asarray(full["evals"])
        ev_br = np.asarray(br["evals"])
        lo = math.floor(min(ev_f[:, 2].min(), ev_br[:, 2].min()) * 10) / 10 - 0.1
        hi = lo + 1.6
        g2 = axes([0, steps], [lo, hi], x_length=10.0, y_length=3.2, xlabel=r"step \ ($16 \times 256$ tokens each)",
                  ylabel=r"held-out loss (nats per token)", xticks=[0, start, bstep, steps], yticks=[lo, hi],
                  yfmt=lambda v: f"{v:.1f}", center=[0.4, -1.3, 0], font_size=18)
        sel_f = ev_f[:, 2] <= hi
        loss_f = curve(g2.ax, ev_f[sel_f, 0], ev_f[sel_f, 2], FULL_C, 3)
        sel_b = (ev_br[:, 0] >= start) & (ev_br[:, 2] <= hi)
        loss_br = curve(g2.ax, ev_br[sel_b, 0], ev_br[sel_b, 2], KEPT, 3)
        lg = legend([(BASE_C, r"cosine: \ decays from the start, \ needs the end in advance"),
                     (FULL_C, r"warmup--stable--decay: \ flat, \ then a short cooldown"),
                     (KEPT, rf"a cooldown branched at step ${start}$")], font_size=18)
        lg.move_to([2.9, 0.2, 0])
        # the schedules first, large; they move up when the losses come in
        big = VGroup(g, lr_b, lr_f)
        home = big.get_center()
        lg_home = lg.get_center()
        big.scale(1.25).move_to([0.3, 0.8, 0])
        lg.move_to([0.6, -2.4, 0])
        b = R["branch"]
        gain = b["stable_val"] - b["val"]
        # does the loss fall faster in the main run's cooldown than over as many steps of its stable phase?
        d0 = steps - int(round(full["spec"]["decay_frac"] * steps))
        at = lambda st: float(np.interp(st, ev_f[:, 0], ev_f[:, 2]))  # noqa: E731
        cool, flat = at(d0) - at(steps), at(2 * d0 - steps) - at(d0)
        shape = ("The held-out loss creeps down during the stable phase, and drops faster in the cooldown."
                 if cool > 1.5 * flat else "The held-out loss falls through the stable phase and the cooldown alike.")
        dot1 = Dot(g2.ax.c2p(b["stable_step"], b["stable_val"]), radius=0.07, color=FULL_C)
        dot2 = Dot(g2.ax.c2p(b["steps"], b["val"]), radius=0.07, color=KEPT)
        tag = note(r"computed: \ our 2026 recipe's run, \ and a branch of it", font_size=18).to_corner(DR, buff=0.2)
        src = cite(r"Hu et al., MiniCPM (2024); \ Hägele et al.\ (2024)", font_size=17)
        if gain > 0.03:
            verdict = (f"At step {bstep}, the branch's held-out loss is {b['val']:.2f}, against {b['stable_val']:.2f} "
                       "for the run still at its peak learning rate: a finished model, without starting again.")
        else:
            verdict = (f"At step {bstep}, the branch's held-out loss is {b['val']:.2f}, against {b['stable_val']:.2f} "
                       "for the run still at its peak: at our scale the cooldown gains little.")
        with self.voiceover(
            "The learning rate falls as a run ends, and how it falls matters. Part 11's cosine starts decaying at "
            "once, "
            "so you must know the length of the run in advance. <bookmark mark='a'/> Since 2024 more runs use warmup, "
            "stable, decay: hold the peak learning rate, and cool down only over the last tenth or fifth of the steps. "
            "<bookmark mark='b'/> Here is the run of our own 2026 recipe, from chapter eighteen. " + shape +
            " <bookmark mark='c'/> The payoff: from any checkpoint "
            f"of the stable phase you can branch off a short cooldown. We branched one at step {start}. "
            "<bookmark mark='d'/> " + verdict + " So one run can try many lengths of training."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(lr_b), FadeIn(lg[0]))
            vo.wait_until("a")
            self.play(Create(lr_f), FadeIn(lg[1]))
            vo.wait_until("b")
            self.play(big.animate.scale(1 / 1.25).move_to(home), lg.animate.move_to(lg_home))
            self.play(FadeIn(g2), FadeIn(tag))
            self.play(Create(loss_f), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(lr_br), FadeIn(lg[2]))
            self.play(Create(loss_br), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(dot1, scale=1.5), FadeIn(dot2, scale=1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def anneal(self):
        L, O2, S, Q = F.LLAMA3, F.OLMO2, F.SMOLLM3, F.QWEN3
        stages = S["stages"]
        bars = VGroup()
        cols = [GREY_B, "#6EA8FE", EDU]
        for k, (a, b, web, code, math_) in enumerate(stages):
            col = VGroup()
            y = 0.0
            for share, c in zip((web, code, math_), cols):
                h = 3.0 * share / 100
                r_ = Rectangle(width=1.0, height=h, stroke_width=1, stroke_color=BLACK, fill_color=c, fill_opacity=0.85)
                r_.move_to([0, y + h / 2, 0])
                col.add(r_)
                y += h
            col.add(label(rf"${a / 1e12:.0f}$--${b / 1e12:.1f}$T", font_size=18, color=GREY_A).next_to(col, DOWN,
                                                                                                    buff=0.1))
            bars.add(col)
        bars.arrange(RIGHT, buff=0.35, aligned_edge=DOWN).move_to([-4.0, 0.1, 0])
        bl = label(r"SmolLM3's three stages", font_size=22, color=EDU).next_to(bars, UP, buff=0.25)
        key = legend([(GREY_B, r"web"), (cols[1], r"code"), (cols[2], r"maths")], font_size=18)
        key.next_to(bars, DOWN, buff=0.35)
        # where the best data goes: the cooldown at the end of the learning rate (schematic)
        o_ = np.array([0.4, -0.6, 0])
        flat = Line(o_ + UP * 1.8, o_ + UP * 1.8 + RIGHT * 3.6, color=GREY_B, stroke_width=4)
        drop = Line(o_ + UP * 1.8 + RIGHT * 3.6, o_ + UP * 0.15 + RIGHT * 4.8, color=EDU, stroke_width=6)
        base_ = Line(o_, o_ + RIGHT * 5.2, color=GREY_D, stroke_width=2)
        lr_l = label(r"learning rate", font_size=20, color=GREY_B).next_to(flat, UP, buff=0.12).align_to(flat, LEFT)
        best_ = label(r"the cooldown: \\ the best data goes here", font_size=21, color=EDU)
        best_.move_to([4.8, 1.8, 0])
        cool_sch = VGroup(base_, flat, drop, lr_l, best_, note(r"schematic", font_size=17).next_to(base_, DOWN,
                                                                                                  buff=0.12))
        facts = VGroup(
            label(rf"Llama 3: \ the last ${L['anneal_tokens'] / 1e6:.0f}$M tokens at a learning rate falling to $0$, "
                  r"\\ the best sources upsampled, \ checkpoints averaged", font_size=21, color=GREY_A),
            label(rf"Qwen3, stage 2: \ ${Q['s2'] / 1e12:.0f}$T tokens with more science, code, reasoning \\ and "
                  r"synthetic data, \ the learning rate decaying faster", font_size=21, color=GREY_A),
            label(rf"Olmo 2: \ mid-training ${O2['mid_share'][0]}$--${O2['mid_share'][1]}\%$ of the FLOPs; \ "
                  rf"${O2['microanneals']}$ small ``microanneals'' \\ (${O2['microanneal_tokens'] / 1e9:.0f}$B tokens in "
                  r"all) to choose its maths data", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([2.6, 0.0, 0])
        src = cite(r"Llama Team (2024); \ Qwen Team (2025); \ Team OLMo (2025); \ Hugging Face (2025)", font_size=17)
        with self.voiceover(
            "The end of a run is also where the best data goes. What a model reads while its learning rate falls "
            "leaves "
            "a strong mark, so labs save their best text for the cooldown and call it annealing, or mid-training. "
            "<bookmark mark='a'/> SmolLM3 trained in three stages, from 85 percent web text to 63, with code and maths "
            "rising from 15 percent to 37. <bookmark mark='b'/> Llama 3 annealed its last forty million tokens to a "
            "learning rate of zero on its best sources, and averaged the checkpoints. <bookmark mark='c'/> Qwen3's "
            "second "
            "stage was five trillion tokens heavy in science, code and reasoning, with a faster decay. "
            "<bookmark mark='d'/> And Olmo 2 spends five to ten percent of its compute on mid-training, choosing the "
            "data "
            "with small annealing runs from a checkpoint: nineteen microanneals to pick its maths."
        ) as vo:
            self.play(FadeIn(src), Create(cool_sch[0]), Create(cool_sch[1]), FadeIn(cool_sch[3]), FadeIn(cool_sch[5]))
            self.play(Create(cool_sch[2]), FadeIn(cool_sch[4]), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(bl), FadeIn(key), LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in bars], lag_ratio=0.4),
                      run_time=2.0)
            vo.wait_until("b")
            self.play(FadeOut(cool_sch))
            self.play(FadeIn(facts[0], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(facts[1], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(facts[2], shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def long_context(self):
        P = load("published")
        why_ = label(r"attention costs grow with the square of the length: \ train short, \ extend at the end",
                     font_size=24, color=GREY_A).to_edge(UP, buff=0.45)
        # context length by stage, log scale
        runs = [(r"Llama 3", [8192, 131072], r"$6$ stages, \ about $800$B tokens"),
                (r"DeepSeek-V3", [4096, 32768, 131072], r"YaRN, \ $1{,}000$ steps each"),
                (r"Qwen3", [4096, 32768], r"base $10^4 \to 10^6$, \ hundreds of billions of tokens"),
                (r"Olmo 3", [8192, 65536], r"$50$--$100$B tokens"),
                (r"DeepSeek-V4", [4096, 16384, 65536, 1048576], r"pretraining itself grows the length")]
        lo, hi = math.log2(4096), math.log2(1048576)
        X = lambda n: -2.6 + 6.0 * (math.log2(n) - lo) / (hi - lo)  # noqa: E731
        rows = VGroup()
        for i, (name, seq, note_) in enumerate(runs):
            y = 1.9 - 0.62 * i
            nm = label(name, font_size=22, color=WHITE).move_to([-3.4, y, 0], aligned_edge=RIGHT)
            dots = VGroup(*[Dot([X(n), y, 0], radius=0.07, color=C.POSITION) for n in seq])
            line = Line([X(seq[0]), y, 0], [X(seq[-1]), y, 0], color=C.POSITION, stroke_width=3)
            nt = label(note_, font_size=17, color=GREY_B).next_to([X(seq[-1]), y, 0], RIGHT, buff=0.2)
            if nt.get_right()[0] > 6.9:
                nt.next_to([X(seq[0]), y, 0], LEFT, buff=0.2).shift(DOWN * 0.27).set_x(X(seq[0]) + nt.width / 2)
            rows.add(VGroup(nm, line, dots, nt))
        ticks = VGroup()
        for n, t in ((4096, r"4K"), (32768, r"32K"), (131072, r"128K"), (1048576, r"1M")):
            ticks.add(label(t, font_size=18, color=GREY_B).move_to([X(n), 2.5, 0]))
        rope = P["rope"]
        colors = {r"\theta": C.POSITION}
        eq = cmath(r"\text{pair } i \text{ turns at } \theta^{-2i/d} \text{ radians a token}", r";", r"\lambda_{\max}",
                   r"=", r"2\pi\,\theta^{(d-2)/d}", colors=colors, font_size=28).move_to(DOWN * 1.45)
        wl = VGroup(*[label(rf"base ${r_['base']:,}$: \ ${r_['longest'] / 1e3:,.0f}$k tokens".replace(",", "{,}"),
                            font_size=21, color=C.POSITION) for r_ in rope[:3]]).arrange(RIGHT, buff=0.5)
        wl.next_to(eq, DOWN, buff=0.3)
        abf = note(r"the slowest pair's wavelength, \ head dimension $d = 128$ (computed); \ raising the base: "
                   r"Xiong et al.\ (2023)", font_size=18).next_to(wl, DOWN, buff=0.2)
        src = cite(r"Llama Team (2024); \ DeepSeek-AI (2024, 2026); \ Qwen Team (2025); \ Team OLMo (2025)",
                   corner=DR, font_size=16)
        with self.voiceover(
            "The last stage teaches length. Attention's cost grows with the square of the context, so models "
            "pretrain on four or eight thousand tokens and stretch at the end. <bookmark mark='a'/> Llama 3 went from "
            "eight thousand to 128 thousand in six stages, on about 800 billion tokens; DeepSeek-V3 to 32 thousand, "
            "then "
            "128 thousand, a thousand steps each; Qwen3 and Olmo 3 stretched once; and DeepSeek-V4 grows its length "
            "during pretraining itself, from four thousand to a million. <bookmark mark='b'/> Stretching needs "
            "positions "
            "to stay distinguishable. Rotary embeddings, from Part 13, turn each pair of dimensions by an angle per "
            "token, "
            "slower and slower down the pairs. <bookmark mark='c'/> With the usual base of ten thousand, the slowest "
            "pair "
            f"takes {rope[0]['longest'] / 1e3:.0f} thousand tokens to turn once. Raise the base, as Llama 3 did to "
            "half "
            f"a million and Qwen3 to a million, and it takes {rope[1]['longest'] / 1e6:.1f} and "
            f"{rope[2]['longest'] / 1e6:.1f} million: room for long documents."
        ) as vo:
            self.play(FadeIn(why_), FadeIn(ticks), FadeIn(src), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in rows[1:]], lag_ratio=0.6), run_time=4.0)
            vo.wait_until("b")
            self.play(Write(eq))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(w_) for w_ in wl], lag_ratio=0.5), FadeIn(abf), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()
