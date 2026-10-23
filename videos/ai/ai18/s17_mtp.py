from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai18.common import (BASE_C, F, MTP_C, PART, hbars, load, node_box, said, spoken_int, take_away)


class MTP(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.module()
        self.ours()
        self.drafts()

    def card(self):
        card = chapter_card(16, r"Predicting two tokens ahead", r"Can a model learn more by guessing further?",
                            lit=(2024,), part=PART)
        with self.voiceover("Chapter sixteen. Predicting two tokens ahead."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def idea(self):
        M = F.MTP
        trunk = node_box(r"shared trunk", GREY_B, font_size=24, height=1.0).move_to([-3.6, 0.85, 0])
        heads = VGroup(*[node_box(rf"head {k}: \ token $t+{k}$", MTP_C if k > 1 else C.PROB, font_size=22)
                         for k in range(1, 5)]).arrange(UP, buff=0.18).next_to(trunk, RIGHT, buff=1.2)
        arrows = VGroup(*[Arrow(trunk.get_right(), h.get_left(), buff=0.08, color=GREY_B, stroke_width=2.5) for h in heads])
        facts = VGroup(
            label(r"Gloeckle et al.\ (Meta, 2024): \ $n$ heads on one trunk", font_size=22, color=MTP_C),
            label(rf"a ${M['params'] / 1e9:.0f}$B code model: \ $+{M['humaneval']}\%$ problems solved on HumanEval, \ "
                  rf"$+{M['mbpp']}\%$ on MBPP", font_size=20, color=GREY_A),
            label(r"more useful the larger the model; \ at their smallest sizes, \ worse", font_size=20, color=GREY_A),
            label(rf"the extra heads as drafters: \ up to ${M['speed']}\times$ faster decoding", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        if facts.width > 13.0:
            facts.width = 13.0
        facts.move_to([0.4, -2.45, 0])
        src = cite(r"Gloeckle et al., \textit{Better \& Faster Large Language Models via Multi-token Prediction} "
                   r"(ICML 2024)", corner=UL, font_size=17)
        with self.voiceover(
            "Next-token prediction asks for one token at a time, which lets a model get by on local patterns. What if "
            "it had to look further? <bookmark mark='a'/> In 2024, Fabian Gloeckle and colleagues at Meta gave a "
            "model several output heads on a shared trunk, predicting the next token, the one after, and so on. "
            "<bookmark mark='b'/> On code, a thirteen-billion-parameter model solved twelve percent more HumanEval "
            "problems and seventeen percent more of MBPP. <bookmark mark='c'/> The gain grew with size; at their "
            "smallest models the extra heads hurt. <bookmark mark='d'/> And the heads double as a fast way to "
            "guess ahead at inference, up to three times faster."
        ) as vo:
            self.play(FadeIn(trunk), FadeIn(heads[0]), GrowArrow(arrows[0]), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(h), GrowArrow(a)) for h, a in zip(heads[1:], arrows[1:])],
                                  lag_ratio=0.3), FadeIn(facts[0]))
            vo.wait_until("b")
            self.play(FadeIn(facts[1]))
            vo.wait_until("c")
            self.play(FadeIn(facts[2]))
            vo.wait_until("d")
            self.play(FadeIn(facts[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def module(self):
        D, P = F.DSV3, load("published")
        main = node_box(r"main model", C.PROB, font_size=22, height=1.6).move_to([-4.6, 0.3, 0])
        emb = node_box(r"embedding of $t_{i+1}$", C.EMBED, font_size=20).move_to([-3.4, -1.5, 0])
        n1 = node_box(r"RMSNorm", GREY_B, font_size=18).move_to([-1.5, 0.3, 0])
        n2 = node_box(r"RMSNorm", GREY_B, font_size=18).move_to([-0.3, -1.5, 0])
        cat = node_box(r"concatenate, \ project", GREY_A, font_size=18).move_to([0.6, 0.3, 0])
        blk = node_box(r"one transformer block", MTP_C, font_size=18).move_to([3.0, 0.3, 0])
        head = node_box(r"shared head: \ $t_{i+2}$", MTP_C, font_size=18).move_to([5.3, 0.3, 0])
        ar = VGroup(Arrow(main.get_right(), n1.get_left(), buff=0.1, color=GREY_B, stroke_width=2.5),
                    Arrow(emb.get_right(), n2.get_left(), buff=0.1, color=GREY_B, stroke_width=2.5),
                    Arrow(n1.get_right(), cat.get_left(), buff=0.1, color=GREY_B, stroke_width=2.5),
                    Arrow(n2.get_top(), cat.get_bottom(), buff=0.1, color=GREY_B, stroke_width=2.5),
                    Arrow(cat.get_right(), blk.get_left(), buff=0.1, color=GREY_B, stroke_width=2.5),
                    Arrow(blk.get_right(), head.get_left(), buff=0.1, color=GREY_B, stroke_width=2.5))
        h = label(r"$h_i$", font_size=26, color=C.PROB).next_to(ar[0], UP, buff=0.08)
        out1 = label(r"$t_{i+1}$", font_size=24, color=C.PROB).next_to(main, UP, buff=0.2)
        loss = cmath(r"L", r"=", r"L_{\text{next}} + \lambda\, L_{\text{MTP}}", font_size=30).to_edge(UP, buff=0.5)
        lam = label(rf"$\lambda = {D['mtp_lambda'][0]}$ for the first $10$T tokens, \ then ${D['mtp_lambda'][1]}$",
                    font_size=22, color=MTP_C).next_to(loss, DOWN, buff=0.15)
        acc = VGroup(
            label(rf"at inference, as a drafter: \ the second token accepted ${D['mtp_accept'][0]}$--"
                  rf"${D['mtp_accept'][1]}\%$ of the time", font_size=22, color=GREY_A),
            label(rf"$1 + a$ tokens per step: \ ${P['dsv3_mtp_tokens'][0]:.2f}$--${P['dsv3_mtp_tokens'][1]:.2f}$; \ "
                  rf"reported: \ ${D['mtp_tps']}\times$ the tokens per second", font_size=22, color=GREY_A),
            label(r"also in DeepSeek-V4, GLM-4.5, Nemotron 3 Super", font_size=20, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.4)
        src = cite(r"DeepSeek-AI (2024), Secs.\ 2.2, 4.2, 5.4.3", corner=DR, font_size=16)
        with self.voiceover(
            "DeepSeek-V3 made the extra prediction sequential. The main model predicts the next token as usual. "
            "<bookmark mark='a'/> A small module then takes the main model's last hidden state at position i and the "
            "embedding of the true next token, <bookmark mark='b'/> normalizes both, joins them, passes them through "
            "one more "
            "transformer block, and predicts the token after next with the same output head. <bookmark mark='c'/> Its "
            "loss is "
            "added with a weight of 0.3 for the first ten trillion tokens, then 0.1. <bookmark mark='d'/> At "
            "inference the "
            "module can be dropped, or used to guess the second token for the main model to check: DeepSeek reports "
            "the guess "
            "accepted 85 to 90 percent of the time, and 1.8 times the speed."
        ) as vo:
            self.play(FadeIn(main), FadeIn(out1), FadeIn(src))
            vo.wait_until("a")
            self.play(GrowArrow(ar[0]), FadeIn(n1), FadeIn(h), FadeIn(emb), GrowArrow(ar[1]), FadeIn(n2))
            vo.wait_until("b")
            self.play(GrowArrow(ar[2]), GrowArrow(ar[3]), FadeIn(cat))
            self.play(GrowArrow(ar[4]), FadeIn(blk), GrowArrow(ar[5]), FadeIn(head))
            vo.wait_until("c")
            self.play(Write(loss), FadeIn(lam))
            vo.wait_until("d")
            self.play(FadeIn(acc, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ours(self):
        Mt, MC = load("mtp"), load("mtp_cost")
        runs = Mt["runs"]
        seeds = Mt["seeds"]
        evs = {k: np.asarray(v["evals"]) for k, v in runs.items()}
        allv = np.concatenate([e[:, 2] for e in evs.values()])
        lo = math.floor(allv.min() * 4) / 4
        hi = lo + 2.0
        g = axes([0, Mt["steps"]], [lo, hi], x_length=6.0, y_length=3.6, xlabel=r"step",
                 ylabel=r"held-out next-token loss (nats)", xticks=[0, Mt["steps"]], yticks=[lo, hi],
                 yfmt=lambda v: f"{v:.2f}", center=[-3.0, -0.3, 0], font_size=18)
        lines = VGroup()
        for lam, col in (("0", BASE_C), ("0.3", MTP_C)):
            for s in seeds:
                e = evs[f"{lam}_{s}"]
                sel = e[:, 2] <= hi
                lines.add(curve(g.ax, e[sel, 0], e[sel, 2], col, 2.5))
        fin = Mt["final"]
        ntp, mtp = np.mean(fin["0"]), np.mean(fin["0.3"])
        spread = max(abs(fin["0"][0] - fin["0"][1]), abs(fin["0.3"][0] - fin["0.3"][1]))
        res = VGroup(
            label(rf"next token only: \ ${min(fin['0']):.3f}$--${max(fin['0']):.3f}$", font_size=22, color=BASE_C),
            label(rf"with the MTP module: \ ${min(fin['0.3']):.3f}$--${max(fin['0.3']):.3f}$", font_size=22,
                  color=MTP_C),
            label(rf"the module's extra arithmetic: \ $+{100 * MC['extra_share']:.0f}\%$ per step", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.6, -0.9, 0])
        # the module's weight over the run, as trained (the spec stored with the run)
        sp = runs[f"0.3_{seeds[0]}"]["spec"]
        cut = int(sp["steps"] * (1 - sp["decay_frac"]))
        gl = axes([0, sp["steps"]], [0, 0.4], x_length=4.2, y_length=1.3, xlabel=r"step",
                  ylabel=r"the module's weight $\lambda$", xticks=[0, cut, sp["steps"]], yticks=[sp["mtp_late"], sp["mtp"]],
                  yfmt=lambda v: f"{v:.1f}", center=[3.6, 1.75, 0], font_size=18)
        lam_l = VMobject(color=MTP_C, stroke_width=3).set_points_as_corners(
            [gl.ax.c2p(0, sp["mtp"]), gl.ax.c2p(cut, sp["mtp"]), gl.ax.c2p(cut, sp["mtp_late"]),
             gl.ax.c2p(sp["steps"], sp["mtp_late"])])
        tag = note(rf"computed: \ our small model, \ ${Mt['steps']}$ steps, \ the same tokens, \ two seeds each",
                   font_size=18).to_corner(DR, buff=0.2)
        if ntp - mtp > max(spread, 0.01):
            verdict = (f"With the module, the held-out loss for the next token ends at {mtp:.3f} nats, against "
                       f"{ntp:.3f} without: predicting further ahead helped, even at our scale.")
        elif mtp - ntp > max(spread, 0.01):
            verdict = (f"With the module, the held-out loss for the next token ends at {mtp:.3f} nats, against "
                       f"{ntp:.3f} without: at our scale the extra task costs a little, as Gloeckle found for their "
                       "smallest models.")
        else:
            verdict = (f"With the module, the held-out loss for the next token ends at {mtp:.3f} nats, against "
                       f"{ntp:.3f} without, inside the spread between seeds: at our scale the extra task neither helps "
                       "nor hurts.")
        mostly = ("mostly the second pass through the output head, which is large in a model this small" if
                  MC["head_share"] > 0.5 else "mostly its own transformer block")
        with self.voiceover(
            "We added DeepSeek-V3's module to our small model and trained it on the same tokens, two seeds each, "
            "with the weight dropping from 0.3 to 0.1 near the end. <bookmark mark='a'/> " + verdict +
            f" <bookmark mark='b'/> The module costs about {100 * MC['extra_share']:.0f} percent more arithmetic per "
            "step, " + mostly + "."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag), LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.2), run_time=3.0)
            self.play(FadeIn(gl), Create(lam_l), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(res[0]), FadeIn(res[1]))
            vo.wait_until("b")
            self.play(FadeIn(res[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def drafts(self):
        Mt, D = load("mtp"), F.DSV3
        acc = Mt["accept"]
        a = float(np.mean(acc))
        rows = hbars([(r"DeepSeek-V3 (reported)", np.mean(D["mtp_accept"]) / 100, MTP_C),
                      (r"ours, \ two seeds", a, MTP_C)], 1.0, width=6.0, bar_h=0.55, gap=0.3, font_size=26,
                     label_width=4.4, fmt=lambda v: rf"${100 * v:.0f}\%$")
        rows.move_to([0.9, 0.5, 0])
        rh = label(r"how often the module's guess for the token after next is right", font_size=27, color=GREY_A)
        rh.next_to(rows, UP, buff=0.35)
        tk = label(rf"tokens per step of the main model: \ $1 + a = {1 + a:.2f}$ \ (ours), \ "
                   rf"${1 + np.mean(D['mtp_accept']) / 100:.2f}$ \ (DeepSeek-V3)", font_size=27, color=MTP_C)
        tk.next_to(rows, DOWN, buff=0.5)
        tw = take_away(r"one more block, \ one more token: \ a training signal, \ and a free drafter", color=MTP_C,
                       font_size=24)
        tag = note(r"computed: \ greedy decoding from $24$ held-out openings", font_size=18).to_corner(DR, buff=0.2)
        if a < 0.8:
            how = (f"The guess was right {100 * a:.0f} percent of the time, against DeepSeek-V3's 85 to 90: a small "
                   "model's guesses two tokens ahead are harder to get right.")
        else:
            how = f"The guess was right {100 * a:.0f} percent of the time, close to DeepSeek-V3's 85 to 90."
        with self.voiceover(
            "And as a drafter? We let our main model write greedily from held-out openings, while its module "
            "guessed each token after next. <bookmark mark='a'/> " + how + " <bookmark mark='b'/> Each step of the "
            f"main model would then yield {1 + a:.2f} tokens instead of one. Part 19 builds speculative decoding "
            "properly."
        ) as vo:
            self.play(FadeIn(rh), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(tk), FadeIn(tw))
        self.wait(0.3)
        self.clear_scene()
