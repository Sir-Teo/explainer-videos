from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai28.common import ENT, PART, POLICY, RIGHT_C, WRONG_C, load, seeds_plot
from videos.ai.ai28.s07_variants import COLS, NAMES


class Entropy(VoiceoverScene):
    def construct(self):
        self.card()
        self.mechanism()
        self.curves()
        self.law()
        self.remedies()

    def card(self):
        card = chapter_card(7, r"Entropy collapse", r"Why does reinforcement learning make a model stop exploring?",
                            lit=(2025,), part=PART)
        with self.voiceover("Chapter seven. Entropy collapse."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def mechanism(self):
        rows = [
            cmath(r"H(\pi)", r"=", r"-\sum_a \pi_a \log \pi_a", font_size=34),
            cmath(r"\frac{\partial H}{\partial z_b}", r"=", r"-\pi_b\big(\log \pi_b - \mathbb E_\pi[\log \pi]\big)",
                  font_size=34),
            cmath(r"\Delta H", r"\approx", r"-\operatorname{Cov}_{a \sim \pi}\big(\log \pi_a,\ \Delta z_a\big)",
                  font_size=34),
            cmath(r"\Delta H", r"\approx", r"-\eta\, \operatorname{Cov}_{a \sim \pi}\big(\log \pi_a,\ \pi_a\, A_a\big)",
                  font_size=34),
        ]
        for r_ in rows:
            r_[0].set_color(ENT)
        whys = [why(r"the model's uncertainty \ ($\pi = \operatorname{softmax}(z)$)"),
                why(r"softmax: \ $\partial \pi_a / \partial z_b = \pi_a(\delta_{ab} - \pi_b)$"),
                why(r"sum over $b$, \ to first order"),
                why(r"a policy-gradient step: \ $\Delta z_a = \eta\, \pi_a A_a$")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.8, buff=0.5, edge=6.9)
        res = label(r"reward what was already likely, \ and the entropy falls", font_size=28, color=ENT)
        res.to_edge(DOWN, buff=0.5)
        cite_ = cite(r"G.~Cui et al., \textit{The Entropy Mechanism of Reinforcement Learning for Reasoning Language "
                     r"Models} (2025)", corner=DR)
        with self.voiceover(
            "At the end of chapter five, the model's entropy fell as it learned. Here is why that always threatens. "
            "Entropy measures how spread out the model's choices are. <bookmark mark='a'/> Write the probabilities as "
            "a softmax of logits z, and differentiate: moving logit b changes the entropy by minus pi b times how "
            "much more surprising b is than average. <bookmark mark='b'/> So, to first order, a step changes the "
            "entropy by minus the covariance, over the model's own choices, between log-probability and the change "
            "in logit. <bookmark mark='c'/> A policy-gradient step raises each logit in proportion to its probability "
            "times its advantage. When the answers the model already likes are the ones that score well, that "
            "covariance is positive, and the entropy falls. <bookmark mark='d'/> Reinforcement learning on a model's "
            "own samples rewards what was already likely, and it compounds. Ganqu Cui and colleagues worked this out "
            "for language models in 2025."
        ) as vo:
            self.play(FadeIn(cite_))
            step(0)
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                step(k + 1)
            vo.wait_until("d")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curves(self):
        o = load("objectives")
        steps = int(o["steps"])
        show = ["grpo", "dapo", "cispo", "pg"]
        Y = {v: np.asarray(o[f"{v}_curves"]) for v in show}
        xs = Y["grpo"][0, :, 0]
        top = math.ceil(max(float(Y[v][:, :, 2].max()) for v in show) * 4) / 4
        g = axes([0, steps], [0, top], x_length=7.0, y_length=4.2, xlabel=r"RL steps",
                 ylabel=r"entropy of each answer digit, \ bits", xticks=[0, steps // 2, steps], yticks=[0, top / 2, top],
                 center=[-1.6, -0.3, 0])
        lines = {v: seeds_plot(g.ax, xs, Y[v][:, :, 2], COLS[v]) for v in show}
        lg = legend([(COLS[v], NAMES[v] + (r" \ (clip $0.8$ to $1.28$)" if v == "dapo" else
                                           r" \ (weight clipped at $1.28$)" if v == "cispo" else
                                           r" \ (clip $0.8$ to $1.2$)" if v == "grpo" else r" \ (no clip)"))
                     for v in show], font_size=19)
        lg.next_to(g, RIGHT, buff=0.3).shift(UP * 1.0)
        if lg.get_right()[0] > 6.9:
            lg.shift(LEFT * (lg.get_right()[0] - 6.9))
        tag = note(r"computed: \ $3$ runs each, \ band: lowest to highest").to_corner(DR, buff=0.2)
        e0 = float(Y["grpo"][:, 0, 2].mean())
        fin = {v: float(Y[v][:, -1, 2].mean()) for v in show}
        if fin["dapo"] > fin["grpo"] + 0.03:
            higher = (f"DAPO's clip-higher keeps more of it: {fin['dapo']:.2f} bits at the end, against "
                      f"{fin['grpo']:.2f} for GRPO's symmetric clip. Letting unlikely tokens grow faster keeps "
                      "alternatives alive.")
        else:
            higher = (f"Here DAPO's clip-higher barely changes it: {fin['dapo']:.2f} bits at the end, against "
                      f"{fin['grpo']:.2f} for GRPO. With three-digit answers there are few unlikely tokens to save; "
                      "on long reasoning, DAPO's authors found it kept the entropy from collapsing.")
        if all(fin[v] < e0 - 0.05 for v in show):
            start = (f"Here it is in our runs. Every objective starts at {e0:.2f} bits of entropy per digit, and every "
                     "one drives it down.")
        else:
            start = f"Here it is in our runs. Every objective starts at {e0:.2f} bits of entropy per digit."
        with self.voiceover(
            f"{start} <bookmark mark='a'/> GRPO, with its symmetric clip, ends at "
            f"{fin['grpo']:.2f}. <bookmark mark='b'/> {higher} <bookmark mark='c'/> CISPO ends at {fin['cispo']:.2f}, "
            f"and the plain gradient, with no clip at all, at {fin['pg']:.2f}."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(lines["grpo"][0]), Create(lines["grpo"][1]), FadeIn(lg[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(lines["dapo"][0]), Create(lines["dapo"][1]), FadeIn(lg[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(lines["cispo"][0]), Create(lines["cispo"][1]), FadeIn(lg[2]),
                      FadeIn(lines["pg"][0]), Create(lines["pg"][1]), FadeIn(lg[3]), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def law(self):
        f = load("entropy_fit")
        H, R = np.asarray(f["H"]), np.asarray(f["R"])
        a, b, r2 = float(f["a"]), float(f["b"]), float(f["r2"])
        hx = math.ceil(H.max() * 4) / 4
        g = axes([0, hx], [0, 1], x_length=6.6, y_length=4.2, xlabel=r"entropy, \ nats per digit",
                 ylabel=r"accuracy", xticks=[0, hx / 2, hx], yticks=[0, 0.5, 1], yfmt=lambda v: rf"{int(100 * v)}\%",
                 center=[-2.0, -0.3, 0])
        V = list(f["variant"])
        dots = VGroup(*[Dot(g.ax.c2p(h, r), radius=0.035, color=COLS[v]).set_opacity(0.75) for h, r, v in zip(H, R, V)])
        hs = np.linspace(0, hx, 80)
        fit = curve(g.ax, hs, np.clip(b - a * np.exp(hs), -0.05, 1.05), WHITE, 3)
        ceil_ = DashedLine(g.ax.c2p(0, min(b - a, 1)), g.ax.c2p(hx, min(b - a, 1)), color=GREY_B, dash_length=0.08)
        law = cmath(r"R", r"=", r"-a\, e^{H} + b", font_size=40).move_to([4.4, 1.6, 0])
        law[0].set_color(RIGHT_C)
        vals = label(rf"$a = {a:.3f}$, \ $b = {b:.2f}$ \\ fit: \ $R^2 = {r2:.2f}$", font_size=22, color=GREY_A)
        vals.next_to(law, DOWN, buff=0.3)
        cl = label(rf"at $H = 0$: \ ${100 * (b - a):.0f}\%$", font_size=22, color=GREY_B).next_to(vals, DOWN, buff=0.4)
        nv = len(set(V))
        tag = note(rf"computed: \ every checkpoint of ${nv * 3}$ runs \ (${nv}$ objectives, $3$ runs each)").to_corner(DR, buff=0.2)
        if r2 > 0.8:
            fits = (f"Fitted to every checkpoint of our runs, it explains {100 * r2:.0f} percent of the variation in "
                    "accuracy, whatever the objective.")
        else:
            fits = (f"On our runs the fit is loose: it explains {100 * r2:.0f} percent of the variation in accuracy; "
                    "the objectives don't all trade entropy for accuracy at the same rate.")
        with self.voiceover(
            "Cui and colleagues found something stranger. Across many runs, accuracy was a simple function of "
            "entropy: R equals minus a times e to the H, plus b. <bookmark mark='a'/> Each dot here is one checkpoint "
            f"of one of our runs, coloured by objective. <bookmark mark='b'/> {fits} <bookmark mark='c'/> And the "
            "law has a sting: at zero entropy, when the model has stopped exploring entirely, it predicts a ceiling, "
            f"here {100 * (b - a):.0f} percent. Entropy is a budget, and reinforcement learning spends it to buy "
            "accuracy."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag), Write(law))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.002), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(vals))
            vo.wait_until("c")
            self.play(Create(ceil_), FadeIn(cl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def remedies(self):
        rows = VGroup(
            label(r"clip-higher: \ let unlikely tokens grow faster \ (DAPO, \ $\varepsilon_{\text{high}} = 0.28$)",
                  font_size=26, color=C.BITS),
            label(r"an entropy bonus: \ a small reward for keeping options open", font_size=26, color=ENT),
            label(r"Clip-Cov and KL-Cov: \ restrain only the tokens with the largest covariance", font_size=26,
                  color=POLICY),
            label(r"long training with resets of the reference model \ (ProRL)", font_size=26, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(UP * 0.6)
        cost = label(r"the price of collapse: \ fewer different answers to try \ (chapter nine)", font_size=26,
                     color=WRONG_C).to_edge(DOWN, buff=0.7)
        cite_ = cite(r"Q.~Yu et al.\ (2025); \ G.~Cui et al.\ (2025); \ M.~Liu et al., \textit{ProRL} (2025)")
        with self.voiceover(
            "So the field fights the collapse. <bookmark mark='a'/> DAPO's clip-higher lets unlikely tokens grow "
            "faster than likely ones shrink. <bookmark mark='b'/> An entropy bonus pays the model a little for "
            "keeping options open. <bookmark mark='c'/> Cui's group restrains just the few tokens with the largest "
            "covariance, the ones driving the collapse. <bookmark mark='d'/> And NVIDIA's ProRL kept training stable "
            "for more than two thousand steps by controlling the KL and periodically resetting the reference model. "
            "<bookmark mark='e'/> Why it matters: a model that has stopped exploring has fewer different answers to "
            "offer when you ask it again. That is the question of chapter nine."
        ) as vo:
            self.play(FadeIn(cite_))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k], shift=UP * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(cost))
        self.wait(0.3)
        self.clear_scene()
