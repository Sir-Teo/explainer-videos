from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai28.common import ADV, CHAIN, MONO, PART, POLICY, RIGHT_C, WRONG_C, chip, load, mark, seeds_plot


class RL(VoiceoverScene):
    def construct(self):
        self.card()
        self.rlvr()
        self.group()
        self.climb()

    def card(self):
        card = chapter_card(4, r"Learning from a checker", r"Can a model learn to reason from right answers alone?",
                            lit=(2024, 2025), part=PART)
        with self.voiceover("Chapter four. Learning from a checker."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def rlvr(self):
        cards = VGroup(
            history_card(2024, r"Z.~Shao et al., \ DeepSeek: \ \textit{DeepSeekMath} \ (February)",
                         r"GRPO: \ PPO without the critic; \ the baseline is the average of a group of answers",
                         width=6.3, color=POLICY),
            history_card(2024, r"OpenAI o1 \ (September)", r"reinforcement learning at scale teaches it to use a chain of "
                         r"thought; \ better with more training, \ and with more time to think", width=6.3, color=POLICY),
            history_card(2024, r"N.~Lambert et al., \ AI2: \ \textit{T\"ulu 3} \ (November)",
                         r"names it: \ reinforcement learning with verifiable rewards, \ RLVR", width=6.3, color=CHAIN),
            history_card(2025, r"DeepSeek-R1 \ (January)", r"GRPO, \ with rewards from rules alone: \ is the answer right, "
                         r"\ is it in the right format", width=6.3, color=CHAIN),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.3)).move_to(UP * 0.2)
        rule = cmath(r"r(x, y)", r"=", r"\begin{cases} 1 & \text{the checker accepts } y \\ 0 & \text{otherwise}"
                     r"\end{cases}", font_size=34).to_edge(DOWN, buff=0.35)
        rule[0].set_color(RIGHT_C)
        with self.voiceover(
            "Chapter one showed that a chain of thought adds computation. But who teaches a model which chain to "
            "write, when nobody can write the steps down for it? <bookmark mark='a'/> In February 2024, DeepSeek's "
            "maths paper introduced an algorithm called GRPO: Part 26's PPO, without the critic. "
            "<bookmark mark='b'/> In September, OpenAI said o1 had learned to think through large-scale "
            "reinforcement learning. <bookmark mark='c'/> In November, the Allen Institute's Tülu 3 gave the method "
            "a name: reinforcement learning with verifiable rewards. <bookmark mark='d'/> And in January 2025, "
            "DeepSeek-R1 showed it at scale, with rewards from simple rules: is the final answer right, and is it "
            "written in the right format. <bookmark mark='e'/> The reward is one if a checker accepts the answer, "
            "zero otherwise. No person grades anything."
        ) as vo:
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.15))
            vo.wait_until("e")
            self.play(Write(rule))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def group(self):
        r = load("rl")
        A, B = np.asarray(r["ex_a"]), np.asarray(r["ex_b"])
        Vb = np.asarray(r["ex_before"])
        G = int(r["G"])
        hits = (Vb == (A + B)[:, None]).sum(1)
        mixed = [i for i in range(len(A)) if 0 < hits[i] < G]
        i = mixed[0] if mixed else 0
        a, b, vals = int(A[i]), int(B[i]), Vb[i]
        rew = (vals == a + b).astype(float)
        adv = (rew - rew.mean()) / (rew.std() + 1e-6)
        q = chip(f"{a}+{b}=", size=0.6, width=2.0, color=GREY_B, font_size=32).move_to([-5.0, 1.8, 0])
        ql = label(r"a question", font_size=22, color=GREY_A).next_to(q, UP, buff=0.15)
        model = RoundedRectangle(width=1.6, height=0.9, corner_radius=0.15, stroke_color=POLICY, stroke_width=2.5,
                                 fill_color=POLICY, fill_opacity=0.12).move_to([-5.0, 0.2, 0])
        ml = label(r"the model", font_size=22, color=POLICY).move_to(model)
        qa = Arrow(q.get_bottom(), model.get_top(), buff=0.08, stroke_width=3, color=GREY_B,
                   max_tip_length_to_length_ratio=0.25)
        xs = np.linspace(-2.6, 5.4, G)
        ans = VGroup(*[chip(f"{int(v)}", size=0.55, width=1.0, color=GREY_B, font_size=28).move_to([x, 1.8, 0])
                       for v, x in zip(vals, xs)])
        al = label(rf"${G}$ answers, \ sampled", font_size=22, color=GREY_A).next_to(ans, UP, buff=0.15)
        fan = VGroup(*[Line(model.get_right(), c_.get_bottom(), stroke_width=1.2, color=GREY_D) for c_ in ans])
        marks = VGroup(*[mark(bool(v), 32).next_to(c_, DOWN, buff=0.12) for v, c_ in zip(rew, ans)])
        rl = label(r"the checker:\ reward $1$ or $0$", font_size=22, color=GREY_A)
        rl.align_to(ans, RIGHT).next_to(marks, DOWN, buff=0.15)
        base_y = -1.2
        zero = Line([xs[0] - 0.7, base_y, 0], [xs[-1] + 0.7, base_y, 0], color=GREY_C, stroke_width=1.5)
        sc = 0.55
        bars = VGroup(*[Rectangle(width=0.55, height=max(abs(v) * sc, 0.01), stroke_width=0,
                                  fill_color=RIGHT_C if v > 0 else WRONG_C, fill_opacity=0.85)
                        .move_to([x, base_y + v * sc / 2, 0]) for v, x in zip(adv, xs)])
        colors = {r"A_i": ADV, r"r_i": RIGHT_C, r"\pi": POLICY}
        f1 = cmath(r"A_i", r"=", r"\frac{", r"r_i", r"- \operatorname{mean}(r)}{\operatorname{std}(r)}", colors=colors,
                   font_size=34)
        f2 = cmath(r"\text{push up}\quad", r"\sum_i", r"A_i", r"\,\log", r"\pi", r"(\text{answer}_i \mid \text{question})",
                   colors=colors, font_size=34)
        VGroup(f1, f2).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.45)
        avl = label(r"how much better than its group", font_size=22, color=ADV).next_to(model, DOWN, buff=0.9)
        avl.align_to(model, LEFT)
        cite_ = cite(r"Z.~Shao et al., \textit{DeepSeekMath} (GRPO, 2024); \ DeepSeek-AI, \textit{DeepSeek-R1} (2025)",
                     corner=UR)
        n_right = int(rew.sum())
        pol = label(r"the policy, \ $\pi$", font_size=22, color=POLICY).next_to(model, DOWN, buff=0.15)
        dash = DashedLine(zero.get_start(), zero.get_end(), color=ADV, stroke_width=2.5, dash_length=0.12)
        bl_ = label(r"baseline: \ the group's average", font_size=20, color=ADV).next_to(zero.get_end(), DOWN, buff=0.12)
        bl_.shift(LEFT * 1.4)
        with self.voiceover(
            "We do it here with a small transformer that has had a little practice at two-digit addition, answering "
            "at once. In this game the model is called the policy, pi: the rule that gives a probability to every "
            f"answer it might write. <bookmark mark='a'/> Give it a question, and sample {G} answers. "
            f"<bookmark mark='b'/> A checker marks each one: here {n_right} of {G} are right. <bookmark mark='c'/> "
            "Each answer's advantage is its reward minus the group's average, divided by the spread: right answers "
            "above the line, wrong ones below. <bookmark mark='d'/> Then nudge the model to make the good answers "
            "more likely and the bad ones less. <bookmark mark='e'/> That's GRPO, group relative policy "
            "optimization: each answer is judged against its own group. Part 26's actor-critic trained a second "
            "network, a critic, to predict the score you'd expect anyway; GRPO uses the group's average instead. "
            "And when every answer in a group is right, or every one wrong, the advantages are all zero: nothing to "
            "learn."
        ) as vo:
            self.play(FadeIn(q), FadeIn(ql), FadeIn(model), FadeIn(ml), GrowArrow(qa), FadeIn(cite_), FadeIn(pol))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(f_) for f_ in fan], lag_ratio=0.1),
                      LaggedStart(*[FadeIn(c_, shift=UP * 0.1) for c_ in ans], lag_ratio=0.1), FadeIn(al), run_time=1.6)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m_, scale=1.4) for m_ in marks], lag_ratio=0.1), FadeIn(rl),
                      *[c_[0].animate.set_stroke(RIGHT_C if v else WRONG_C) for v, c_ in zip(rew, ans)])
            vo.wait_until("c")
            self.play(Create(zero), FadeIn(avl), Write(f1))
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN if v > 0 else UP) for v, b_ in zip(adv, bars)], lag_ratio=0.08))
            vo.wait_until("d")
            self.play(Write(f2))
            self.play(*[c_.animate.scale(1.2) for v, c_ in zip(rew, ans) if v],
                      *[c_.animate.scale(0.8).set_opacity(0.4) for v, c_ in zip(rew, ans) if not v], run_time=1.2)
            vo.wait_until("e")
            self.play(Create(dash), FadeIn(bl_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def climb(self):
        r = load("rl")
        C_ = np.asarray(r["curves"])  # (seeds, checkpoints, 2)
        steps = C_[0, :, 0]
        S = int(steps[-1])
        snaps = np.asarray(r["snaps"])  # (checkpoints, 6, 8)
        A, B = np.asarray(r["ex_a"]), np.asarray(r["ex_b"])
        truth = A + B
        g = axes([0, S], [0, 1], x_length=5.4, y_length=3.4, xlabel=r"GRPO steps",
                 ylabel=r"right on $500$ new questions \ (one try each)", xticks=[0, S // 2, S], yticks=[0, 0.5, 1],
                 yfmt=lambda v: rf"{int(100 * v)}\%", center=[-3.5, -0.5, 0])
        ax = g.ax
        kt = ValueTracker(0)
        Y = C_[:, :, 1]

        def partial():
            i = int(round(kt.get_value()))
            return seeds_plot(ax, steps[:i + 1], Y[:, :i + 1], CHAIN) if i >= 1 else VGroup()

        line = always_redraw(partial)
        dot = always_redraw(lambda: Dot(ax.c2p(steps[int(round(kt.get_value()))],
                                               Y[0, int(round(kt.get_value()))]), radius=0.07, color=C.BITS))
        G = snaps.shape[2]
        cw, chh = 0.6, 0.36

        def grid(k):
            g_ = VGroup()
            for qi in range(len(A)):
                for j in range(G):
                    ok = snaps[k, qi, j] == truth[qi]
                    c_ = chip(f"{int(snaps[k, qi, j])}", size=chh, width=cw, color=RIGHT_C if ok else WRONG_C,
                              font_size=18, fill=0.35 if ok else 0.1)
                    g_.add(c_.move_to([1.35 + j * (cw + 0.06), 1.5 - qi * (chh + 0.14), 0]))
            return g_

        cur = grid(0)
        qs = VGroup(*[data_text(f"{int(a)}+{int(b)}", font=MONO, font_size=18, color=GREY_A)
                      .next_to(cur[qi * G], LEFT, buff=0.15) for qi, (a, b) in enumerate(zip(A, B))])
        gl = label(r"six questions, \ eight tries each \ (run $1$)", font_size=22, color=GREY_A).next_to(cur, UP, buff=0.2)
        cnt = always_redraw(lambda: label(
            rf"step ${int(steps[int(round(kt.get_value()))])}$: \ "
            rf"${int((snaps[int(round(kt.get_value()))] == truth[:, None]).sum())}$ of ${snaps[0].size}$ right",
            font_size=24, color=C.BITS).next_to(cur, DOWN, buff=0.3))
        tag = note(rf"computed: \ ${int(r['seeds'])}$ runs, \ band: lowest to highest").to_corner(DR, buff=0.2)
        nb, na = int((snaps[0] == truth[:, None]).sum()), int((snaps[-1] == truth[:, None]).sum())
        after = 100 * np.asarray(r["after_seeds"])
        if round(after.min()) == round(after.max()):
            finish = f"All {len(after)} runs finish at {after.mean():.0f} percent, taught by nothing but a checker."
        else:
            finish = (f"The runs finish between {after.min():.0f} and {after.max():.0f} percent, taught by nothing "
                      "but a checker.")
        with self.voiceover(
            f"Repeat that for {S} steps of thirty-two questions each, and replay the training. <bookmark mark='a'/> "
            f"On the left, accuracy on five hundred new questions, for {int(r['seeds'])} runs from the same start. On "
            "the right, one run's answers to six questions, eight tries each, at every checkpoint. "
            f"<bookmark mark='b'/> It starts out right {100 * float(r['before']):.0f} percent of the time. "
            f"<bookmark mark='c'/> As it trains, the green spreads: {nb} of {snaps[0].size} right at the start, {na} "
            f"at the end. {finish} "
            "<bookmark mark='d'/> The probability has moved onto the answers that check out."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag), FadeIn(qs), FadeIn(gl), FadeIn(cur))
            self.add(line, dot, cnt)
            vo.wait_until("b")
            vo.wait_until("c")
            K = len(steps)
            dt = max(0.3, min(0.8, (vo.until("d") - 0.5) / K))
            for k in range(1, K):
                self.play(Transform(cur, grid(k)), kt.animate.set_value(k), run_time=dt, rate_func=linear)
            vo.wait_until("d")
            self.play(Indicate(cnt, color=C.BITS))
        for m in (line, dot, cnt):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()
