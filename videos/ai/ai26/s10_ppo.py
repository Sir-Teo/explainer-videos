from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai26.common import (AGENT, LEFT_C, PART, PENALTY, REWARD, RIGHT_C, TDERR, axes, band, cartpole,
                                   curve, heat_image, legend, load, state_map_frame)

RATIO = C.RATIO
REINF, BASE, AC, PPO_C = GREY_B, C.MODEL_Q, C.BASELINE, C.TRUE_P


class PPO(VoiceoverScene):
    def construct(self):
        self.card()
        self.step_size()
        self.surrogate()
        self.clip_plot()
        self.replay_training()
        self.compare()
        self.reach()

    def card(self):
        card = chapter_card(9, r"Trust regions and PPO", r"How big a step can you trust?", lit=(2017,), part=PART)
        with self.voiceover("Chapter nine. Trust regions and PPO."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def step_size(self):
        x = np.linspace(0, 1, 200)
        g = axes([0, 1], [0, 1.1], x_length=6.0, y_length=3.2, xlabel=r"policy parameters $\theta$",
                 ylabel=r"how good the policy is, \ $J(\theta)$", center=[-2.6, -0.3, 0])
        J = 0.9 * np.exp(-((x - 0.62) / 0.12) ** 2) + 0.15 * np.exp(-((x - 0.2) / 0.2) ** 2)
        line = curve(g.ax, x, J, REWARD, 3, smooth=True)
        start = 0.42
        j0 = float(np.interp(start, x, J))
        p0 = glow_dot(g.ax.c2p(start, j0), color=AGENT)
        big = 0.93
        p1 = glow_dot(g.ax.c2p(big, float(np.interp(big, x, J))), color=PENALTY)
        arr = Arrow(g.ax.c2p(start, j0 + 0.08), g.ax.c2p(big, float(np.interp(big, x, J)) + 0.08), buff=0.05,
                    color=PENALTY, stroke_width=3)
        tr = Rectangle(width=g.ax.c2p(start + 0.1, 0)[0] - g.ax.c2p(start - 0.1, 0)[0], height=3.2, stroke_width=0,
                       fill_color=AGENT, fill_opacity=0.12).move_to(g.ax.c2p(start, 0.55))
        tl = label(r"trust region", font_size=20, color=AGENT).next_to(tr, UP, buff=0.05)
        txt = VGroup(label(r"one step too far: \ the policy collapses, \\ and its own bad data can't fix it", font_size=24,
                           color=PENALTY),
                     label(r"data comes from the old policy: \\ how far is it a fair sample?", font_size=24,
                           color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([3.6, 0.3, 0])
        tag = note(r"illustrative").to_corner(DR, buff=0.25)
        with self.voiceover(
            "Policy gradients have a fragile point: the step size. The gradient is only a local guess about which way "
            "is up. <bookmark mark='a'/> Step too far, and the policy can land somewhere terrible. In supervised "
            "learning you'd recover on the next batch, but here the bad policy generates the next batch: it plays "
            "badly, sees only bad states, and may never find its way back. <bookmark mark='b'/> And the data was "
            "collected by the old policy. The further the new one moves, the less that data says about it. "
            "<bookmark mark='c'/> So: only trust steps inside a region where the new policy stays close to the old."
        ) as vo:
            self.play(FadeIn(g), Create(line), FadeIn(p0), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowArrow(arr), FadeIn(p1), FadeIn(txt[0]))
            vo.wait_until("b")
            self.play(FadeIn(txt[1]))
            vo.wait_until("c")
            self.play(FadeIn(tr), FadeIn(tl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def surrogate(self):
        rows = [
            cmath(r"\rho_t(\theta)", r"=", r"\frac{\pi_\theta(a_t \mid s_t)}{\pi_{\mathrm{old}}(a_t \mid s_t)}", font_size=38),
            cmath(r"L(\theta)", r"=", r"\mathbb E_{\pi_{\mathrm{old}}}\big[\,", r"\rho_t(\theta)", r"\hat A_t", r"\,\big]",
                  font_size=38),
            cmath(r"\max_\theta\ L(\theta)", r"\ \text{ s.t. }\ ", r"\mathbb E\big[\mathrm{KL}(\pi_{\mathrm{old}} \,\|\, "
                  r"\pi_\theta)\big] \le \delta", font_size=36),
        ]
        rows[0][0].set_color(RATIO)
        rows[1][3].set_color(RATIO)
        rows[1][4].set_color(TDERR)
        rows[2][2].set_color(C.KL)
        whys = [why(r"the importance ratio: \ new probability over old"),
                why(r"importance sampling, \ Part 5: \ its gradient at $\theta_{\mathrm{old}}$ \\ is the policy gradient"),
                why(r"TRPO (Schulman et al., 2015): \\ a natural-gradient step, \ Part 11")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-2.4, buff=0.65, edge=6.9)
        with self.voiceover(
            "To reuse the old policy's data, weigh each sample by the ratio of the new policy's probability to the "
            "old one's. <bookmark mark='a'/> That gives a surrogate objective, estimated entirely from data already "
            "collected, whose gradient at the old parameters is exactly the policy gradient. <bookmark mark='b'/> "
            "TRPO, John Schulman's trust region method of 2015, maximizes it subject to a limit on the KL divergence "
            "between old and new policies. Solving that constraint leads to the natural gradient of Part 11: "
            "precise, but heavy, with second-order computations at every step."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def clip_plot(self):
        eps = 0.2
        clip = cmath(r"L^{\mathrm{CLIP}}", r"=", r"\mathbb E\Big[\min\big(", r"\rho_t \hat A_t", r",\ ",
                     r"\operatorname{clip}(\rho_t,\, 1-\epsilon,\, 1+\epsilon)\, \hat A_t", r"\big)\Big]", font_size=36)
        clip[3].set_color(RATIO)
        clip[5].set_color(PPO_C)
        clip.to_edge(UP, buff=0.4)
        r = np.linspace(0, 2, 400)

        def panel(A, center, title, col):
            g = axes([0, 2], [-1.6, 1.6], x_length=4.6, y_length=3.0, xlabel=r"$\rho$", xticks=[1 - eps, 1, 1 + eps],
                     xfmt=lambda v: f"{v:g}", center=center)
            y_raw = r * A
            y = np.minimum(r * A, np.clip(r, 1 - eps, 1 + eps) * A)
            raw = DashedLine(g.ax.c2p(0, 0), g.ax.c2p(2, 2 * A), color=GREY_C, dash_length=0.08)
            cl = curve(g.ax, r, y, col, 4)
            t = label(title, font_size=24, color=col).next_to(g, UP, buff=0.1)
            zero = DashedLine(g.ax.c2p(0, 0), g.ax.c2p(2, 0), color=GREY_D, dash_length=0.05, stroke_width=1)
            return VGroup(g, zero, raw, cl, t)

        left = panel(1.0, [-3.3, -0.8, 0], r"good action: \ $\hat A > 0$", REWARD)
        right = panel(-1.0, [3.3, -0.8, 0], r"bad action: \ $\hat A < 0$", PENALTY)
        n1 = label(r"no extra credit for raising it past $1+\epsilon$", font_size=20, color=REWARD)
        n1.next_to(left[0], DOWN, buff=0.15)
        n2 = label(r"no extra credit for lowering it past $1-\epsilon$", font_size=20, color=PENALTY)
        n2.next_to(right[0], DOWN, buff=0.15)
        with self.voiceover(
            "In 2017 Schulman's team found a much simpler way to stay close, and it became the default: proximal "
            "policy optimization, PPO. <bookmark mark='a'/> Clip the ratio to a band, one minus epsilon to one plus "
            "epsilon, typically epsilon is 0.2, and take the smaller of the clipped and unclipped objectives. "
            "<bookmark mark='b'/> For a good action, raising its probability helps, but only until the ratio "
            "reaches 1.2; beyond that the objective goes flat, and so does the gradient. <bookmark mark='c'/> For a "
            "bad action, lowering it helps until 0.8, and no further. Taking the minimum keeps the pessimistic "
            "branch: a step that makes things worse is never clipped away. So you can run several epochs of "
            "gradient steps on the same batch, and the policy can't run off."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(clip))
            vo.wait_until("b")
            self.play(FadeIn(left[0]), FadeIn(left[1]), FadeIn(left[4]), Create(left[2]))
            self.play(Create(left[3]), FadeIn(n1))
            vo.wait_until("c")
            self.play(FadeIn(right[0]), FadeIn(right[1]), FadeIn(right[4]), Create(right[2]))
            self.play(Create(right[3]), FadeIn(n2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay_training(self):
        d = load("pg")
        steps = np.asarray(d["snap_steps"])
        Pm = np.asarray(d["snap_p"])
        T, L = np.asarray(d["snap_traj"]), np.asarray(d["snap_len"])
        run0 = np.asarray(d["run0"])
        g = axes([0, 100_000], [0, 520], x_length=5.0, y_length=2.4, xlabel=r"steps of experience",
                 ylabel=r"length of each episode \ (this run)", xticks=[0, 50_000, 100_000], yticks=[0, 500],
                 xfmt=lambda v: f"{int(v / 1000)}" + (r"\text{k}" if v else ""), center=[3.6, -1.9, 0])
        pts = VGroup(*[Dot(g.ax.c2p(t, r), radius=0.025, color=PPO_C) for t, r in run0])
        marker = Line(g.ax.c2p(0, 0), g.ax.c2p(0, 520), color=C.BITS, stroke_width=3)
        imgs = [heat_image(Pm[i] - 0.5, vmax=0.5, width=3.0, height=3.0).move_to([3.6, 1.55, 0]) for i in range(len(steps))]
        frame = state_map_frame(imgs[0])
        mkey = VGroup(label(r"$\pi(\text{left}) = 1$", font_size=20, color=LEFT_C),
                      label(r"$\pi(\text{right}) = 1$", font_size=20, color=RIGHT_C)).arrange(RIGHT, buff=0.4)
        mkey.next_to(frame[0], UP, buff=0.12)
        ml = label(r"the policy's probabilities, \ cart centred and still", font_size=18, color=GREY_A)
        ml.next_to(mkey, UP, buff=0.1)
        state, snap = ValueTracker(0), ValueTracker(0)

        def pole():
            i = int(snap.get_value())
            n = int(L[i])
            j = min(int(state.get_value()), n - 1)
            x, _, th, _ = T[i, j]
            return cartpole(x, th, center=[-3.3, -0.4, 0], scale=1.25,
                            color=PENALTY if (j == n - 1 and n < 500) else AGENT)

        cp = always_redraw(pole)
        info = always_redraw(lambda: label(
            rf"after ${int(steps[int(snap.get_value())]):,}$ steps: \ balanced "
            rf"${min(int(state.get_value()), int(L[int(snap.get_value())]) - 1)}$ of $500$".replace(",", "{,}"),
            font_size=24, color=GREY_A).move_to([-3.3, 2.6, 0]))
        tag = note(r"computed: \ PPO, \ $\epsilon = 0.2$, \ $4$ epochs per batch").to_corner(DR, buff=0.2)
        img = imgs[0]
        with self.voiceover(
            "Here is PPO learning the cart-pole, replayed. On the right, the policy itself: the probability of "
            "pushing left or right in each state. It starts as a coin flip everywhere, a uniform grey. "
            "<bookmark mark='a'/> Batch by batch, the two colours pull apart along the same tilted line DQN found, "
            "and the episodes get longer. Unlike DQN's, this policy stays soft near the boundary, where it isn't "
            "sure, until training sharpens it."
        ) as vo:
            self.add(cp)
            self.play(FadeIn(info), FadeIn(img), FadeIn(frame), FadeIn(mkey), FadeIn(ml), FadeIn(g), FadeIn(tag))
            self.play(state.animate.set_value(int(L[0]) - 1), run_time=1.0, rate_func=linear)
            vo.wait_until("a")
            self.add(marker)
            for i in range(1, len(steps)):
                state.set_value(0)
                self.play(FadeIn(imgs[i]), FadeOut(img), snap.animate.set_value(i),
                          marker.animate.put_start_and_end_on(g.ax.c2p(steps[i], 0), g.ax.c2p(steps[i], 520)),
                          FadeIn(VGroup(*[p for p, (t, _) in zip(pts, run0) if steps[i - 1] < t <= steps[i]])),
                          run_time=0.8)
                img = imgs[i]
                n = int(L[i])
                self.play(state.animate.set_value(n - 1), run_time=min(0.4 + n / 160, 3.6), rate_func=linear)
        cp.clear_updaters()
        info.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compare(self):
        d = load("pg")
        grid = np.asarray(d["grid"])
        g = axes([0, 100_000], [0, 500], x_length=7.2, y_length=4.0, xlabel=r"steps of experience",
                 ylabel=r"episode length \ (mean of $3$ runs)", xticks=[0, 50_000, 100_000], yticks=[0, 250, 500],
                 xfmt=lambda v: f"{int(v / 1000)}" + (r"\text{k}" if v else ""), center=[-1.2, -0.3, 0])
        items = (("reinforce", REINF, r"REINFORCE"), ("baseline", BASE, r"with a baseline"),
                 ("ac", AC, r"actor-critic (GAE)"), ("ppo", PPO_C, r"PPO"))
        lines = VGroup(*[curve(g.ax, grid, np.nanmean(np.asarray(d[k]), 0), c, 3 if k != "ppo" else 5)
                         for k, c, _ in items])
        lg = legend([(c, t) for _, c, t in items], font_size=20).next_to(g, RIGHT, buff=0.3).shift(UP * 0.8)
        with self.voiceover(
            "Against the policy-gradient methods of the last chapter, PPO, in bold blue, gets more out of each "
            "batch, because it can take several careful steps on it instead of one."
        ) as vo:
            self.play(FadeIn(g), LaggedStart(*[Create(l_) for l_ in lines[:3]], lag_ratio=0.2), FadeIn(lg[:3]))
            self.play(Create(lines[3]), FadeIn(lg[3]), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def reach(self):
        cards = VGroup(
            history_card(2019, r"OpenAI Five", r"PPO at enormous scale beats the world champions at Dota 2: \ about "
                         r"$45{,}000$ years of self-play", width=6.0, color=PPO_C),
            history_card(2018, r"Soft actor-critic", r"maximize reward plus the policy's entropy: \ robots that keep "
                         r"exploring, \ and recover", width=6.0, color=C.ENTROPY),
            history_card(2022, r"RLHF, \ ChatGPT \ (Part 27)", r"PPO, with a learned reward model of human "
                         r"preferences, \ and a KL leash to the original model", width=6.0, color=REWARD),
            history_card(2024, r"GRPO \ (Part 28)", r"PPO's clipped objective without the critic: \ the baseline is "
                         r"the average of a group of answers", width=6.0, color=TDERR),
        ).arrange_in_grid(rows=2, cols=2, buff=0.35).move_to(UP * 0.1)
        cite_ = cite(r"Berner et al.\ (2019); \ Haarnoja et al.\ (2018); \ Ouyang et al.\ (2022); \ Shao et al.\ (2024)")
        with self.voiceover(
            "PPO went everywhere. <bookmark mark='a'/> OpenAI Five used it, at enormous scale, to beat the world "
            "champions at Dota 2 in 2019, after the equivalent of forty-five thousand years of self-play. "
            "<bookmark mark='b'/> For robots, soft actor-critic adds the policy's entropy to the reward, so it keeps "
            "exploring. <bookmark mark='c'/> And it is the RL in RLHF, the step that turned language models into "
            "ChatGPT, in Part 27. <bookmark mark='d'/> Its descendant GRPO, which drops the critic, trains today's "
            "reasoning models, in Part 28."
        ) as vo:
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.15), *([FadeIn(cite_)] if k == 0 else []))
        self.wait(0.3)
        self.clear_scene()
