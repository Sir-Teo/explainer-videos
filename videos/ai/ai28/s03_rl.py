from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai28.common import CHAIN, RIGHT_C, WRONG_C, chip, curve, load, mark

POLICY = C.NEURAL


class RL(VoiceoverScene):
    def construct(self):
        self.card()
        self.group()
        self.climb()
        self.process()

    def card(self):
        card = chapter_card(2, r"Learning from a checker", r"Can a model learn to reason from right answers alone?",
                            lit=(2024,), part=28)
        with self.voiceover("Chapter two. Learning from a checker."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

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
        qa = Arrow(q.get_bottom(), model.get_top(), buff=0.08, stroke_width=3, color=GREY_B, max_tip_length_to_length_ratio=0.25)
        xs = np.linspace(-2.6, 5.4, G)
        ans = VGroup(*[chip(f"{int(v)}", size=0.55, width=1.0, color=GREY_B, font_size=28).move_to([x, 1.8, 0]) for v, x in zip(vals, xs)])
        al = label(rf"${G}$ answers, \ sampled", font_size=22, color=GREY_A).next_to(ans, UP, buff=0.15)
        fan = VGroup(*[Line(model.get_right(), c_.get_bottom(), stroke_width=1.2, color=GREY_D) for c_ in ans])
        marks = VGroup(*[mark(bool(v), 32).next_to(c_, DOWN, buff=0.12) for v, c_ in zip(rew, ans)])
        rl = label(r"the checker:\ reward $1$ or $0$", font_size=22, color=GREY_A).next_to(marks, RIGHT, buff=0.2)
        rl.align_to(ans, RIGHT).next_to(marks, DOWN, buff=0.15)
        base_y = -1.2
        zero = Line([xs[0] - 0.7, base_y, 0], [xs[-1] + 0.7, base_y, 0], color=GREY_C, stroke_width=1.5)
        sc = 0.55
        bars = VGroup(*[Rectangle(width=0.55, height=max(abs(v) * sc, 0.01), stroke_width=0, fill_color=RIGHT_C if v > 0 else WRONG_C,
                                  fill_opacity=0.85).move_to([x, base_y + v * sc / 2, 0]) for v, x in zip(adv, xs)])
        colors = {r"A_i": C.BITS, r"r_i": RIGHT_C, r"\pi": POLICY}
        f1 = cmath(r"A_i", r"=", r"\frac{", r"r_i", r"- \operatorname{mean}(r)}{\operatorname{std}(r)}", colors=colors, font_size=34)
        f2 = cmath(r"\text{push up}\quad", r"\sum_i", r"A_i", r"\,\log", r"\pi", r"(\text{answer}_i \mid \text{question})",
                   colors=colors, font_size=34)
        fs = VGroup(f1, f2).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.45)
        avl = label(r"how much better than its group", font_size=22, color=C.BITS).next_to(zero, LEFT, buff=0.2)
        if avl.get_left()[0] < -6.9:
            avl.next_to(model, DOWN, buff=0.9).align_to(model, LEFT)
        cite_ = cite(r"Z.~Shao et al., \textit{DeepSeekMath} (GRPO, 2024); \ DeepSeek-AI, \textit{DeepSeek-R1} (2025)", corner=UR)
        n_right = int(rew.sum())
        # reinforcement learning, the loop: the model answers, a checker scores, the score nudges the model
        def node(text, col):
            t_ = label(text, font_size=22, color=col)
            return VGroup(RoundedRectangle(width=t_.width + 0.4, height=0.6, corner_radius=0.1, stroke_color=col, stroke_width=2), t_)

        nodes = VGroup(node(r"the model, \ $\pi$", POLICY), node(r"answers", GREY_A), node(r"checker", GREY_A),
                       node(r"reward", C.BITS))
        for n_, xy in zip(nodes, [(-1.7, 0.7), (1.7, 0.7), (1.7, -0.7), (-1.7, -0.7)]):
            n_.move_to([xy[0], xy[1], 0])
        ends = [(RIGHT, LEFT), (DOWN, UP), (LEFT, RIGHT), (UP, DOWN)]
        loop = VGroup(nodes, *[Arrow(a_.get_edge_center(s_), b_.get_edge_center(e_), buff=0.1, stroke_width=2.5, color=GREY_B,
                                     max_tip_length_to_length_ratio=0.15)
                               for (s_, e_), a_, b_ in zip(ends, nodes, list(nodes[1:]) + [nodes[0]])])
        rlc = gloss(r"reinforcement learning", r"try, \ get a score, \\ do more of what scored well: \\ trial and error, \\ not worked examples",
                    picture=loop, width=5.6, color=POLICY)
        rlc.move_to([1.6, -0.2, 0])
        loop = rlc[1][2]
        pol = label(r"the policy, \ $\pi$", font_size=22, color=POLICY).next_to(model, DOWN, buff=0.15)
        # GRPO, spelled out, and the baseline it uses in place of a critic
        gw = VGroup(label(r"GRPO:", font_size=22, color=WHITE), label(r"Group", font_size=22, color=C.BITS),
                    label(r"Relative", font_size=22, color=C.BITS), label(r"Policy Optimization", font_size=22, color=GREY_A))
        gw.arrange(RIGHT, buff=0.15, aligned_edge=UP)
        gp = label(r"baseline: \ the score you'd expect anyway. \ Older methods train a second network, \\ a critic, to predict it; "
                   r"\ GRPO uses the group's average instead", font_size=17, color=GREY_A)
        gb = VGroup(gw, gp).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        gcard = VGroup(RoundedRectangle(width=gb.width + 0.36, height=gb.height + 0.3, corner_radius=0.12, stroke_color=C.BITS,
                                        stroke_width=1.5, fill_color="#0B0F17", fill_opacity=0.92), gb)
        gb.move_to(gcard[0])
        gcard.move_to([2.4, -2.12, 0])
        dash = DashedLine(zero.get_start(), zero.get_end(), color=C.BITS, stroke_width=2.5, dash_length=0.12)
        bl_ = label(r"baseline", font_size=20, color=C.BITS).next_to(zero.get_end(), DOWN, buff=0.12).shift(LEFT * 0.45)
        with self.voiceover(
            "How do you teach a model to reason, when nobody can write down the steps for it? DeepSeek-R1 used "
            "a recipe with almost no human help: questions with checkable answers, and reinforcement learning. "
            "<bookmark mark='r'/> The model tries, gets a score, and is nudged to do more of what scored well: trial "
            "and error, not worked examples. <bookmark mark='p'/> In this game the model is called the policy, pi: "
            "the rule that gives a probability to every answer it might write. "
            "We do it here with a small transformer that has had a little practice at two-digit addition. "
            f"<bookmark mark='a'/> Give it a question, and sample {G} answers. <bookmark mark='b'/> A checker marks "
            f"each one: here {n_right} of {G} are right. <bookmark mark='c'/> Each answer's advantage is its reward "
            "minus the group's average, divided by the spread: right answers above the line, wrong ones below. "
            "<bookmark mark='d'/> Then nudge the model to make the good answers more likely and the bad ones less. "
            "<bookmark mark='e'/> That's GRPO, group relative policy optimization: each answer is judged relative to "
            "its own group. No one judges the steps. <bookmark mark='f'/> Older methods compare each reward with a "
            "baseline, the score you'd expect anyway, and train a second network, a critic, to predict it. GRPO needs "
            "no critic: the group's average is its baseline. "
            "And when every answer is right, or every one wrong, the advantages are all zero: nothing to learn."
        ) as vo:
            self.play(FadeIn(q), FadeIn(ql), FadeIn(model), FadeIn(ml), GrowArrow(qa), FadeIn(cite_))
            vo.wait_until("r")
            self.play(FadeIn(rlc[0]), FadeIn(rlc[1][:2]), FadeIn(loop[0][0]))
            self.play(Succession(*[AnimationGroup(GrowArrow(a_), *([FadeIn(loop[0][k + 1])] if k < 3 else []))
                                   for k, a_ in enumerate(loop[1:])]), run_time=2.4)
            vo.wait_until("p")
            self.play(FadeIn(pol), Indicate(loop[0][0], color=POLICY))
            vo.wait_until("a")
            self.play(FadeOut(rlc), run_time=0.5)
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
            self.play(FadeIn(gcard[0]), FadeIn(gw))
            vo.wait_until("f")
            self.play(FadeIn(gp), Create(dash), FadeIn(bl_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def climb(self):
        r = load("rl")
        cv = np.asarray(r["curve"])
        before, after = float(r["before"]), float(r["after"])
        A, B = np.asarray(r["ex_a"]), np.asarray(r["ex_b"])
        Vb, Va = np.asarray(r["ex_before"]), np.asarray(r["ex_after"])
        steps = float(cv[:, 0].max())
        ax = Axes(x_range=[0, steps, steps / 3], y_range=[0, 1, 0.25], x_length=5.4, y_length=3.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-3.4, -0.4, 0])
        xt = VGroup(*[MathTex(f"{int(v)}", font_size=20, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1) for v in (0, steps / 2, steps)])
        yt = VGroup(*[MathTex(rf"{int(100 * v)}\%", font_size=20, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1) for v in (0, 0.5, 1)])
        xn = label(r"GRPO steps", font_size=20, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yn = label(r"right on $500$ new questions \ (one sample each)", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.15)
        yn.align_to(ax, LEFT)
        line = curve(ax, cv[:, 0], cv[:, 1], CHAIN, 4)
        t = ValueTracker(0)

        def pos():
            s = t.get_value()
            return ax.c2p(s, float(np.interp(s, cv[:, 0], cv[:, 1])))

        dot = always_redraw(lambda: Dot(pos(), radius=0.08, color=C.BITS))
        val = always_redraw(lambda: DecimalNumber(100 * float(np.interp(t.get_value(), cv[:, 0], cv[:, 1])), num_decimal_places=0,
                                                  unit=r"\%", font_size=30, color=C.BITS).next_to(pos(), UP, buff=0.15))
        # six questions, eight answers each: before and after
        G = Vb.shape[1]
        cw, chh = 0.62, 0.36

        def grid(V):
            g = VGroup()
            for qi in range(len(A)):
                for j in range(G):
                    ok = V[qi, j] == A[qi] + B[qi]
                    c_ = chip(f"{int(V[qi, j])}", size=chh, width=cw, color=RIGHT_C if ok else WRONG_C, font_size=18,
                              fill=0.35 if ok else 0.1)
                    g.add(c_.move_to([0.9 + j * (cw + 0.06), 1.4 - qi * (chh + 0.12), 0]))
            return g

        gb, ga = grid(Vb), grid(Va)
        qs = VGroup(*[Text(f"{int(a)}+{int(b)}", font="DejaVu Sans Mono", font_size=18, color=GREY_A).next_to(gb[qi * G], LEFT, buff=0.15)
                      for qi, (a, b) in enumerate(zip(A, B))])
        gl = label(r"before", font_size=24, color=GREY_A).next_to(gb, UP, buff=0.2)
        gl2 = label(r"after", font_size=24, color=CHAIN).move_to(gl)
        nb, na = int((Vb == (A + B)[:, None]).sum()), int((Va == (A + B)[:, None]).sum())
        with self.voiceover(
            f"Repeat that for {int(r['rl_steps'])} steps of thirty-two questions. <bookmark mark='a'/> Our model starts "
            f"out right {100 * before:.0f} percent of the time, and climbs to {100 * after:.0f} percent, "
            "taught by nothing but a checker. <bookmark mark='b'/> Here are its answers to six questions, eight "
            f"tries each: {nb} of {Vb.size} right before, <bookmark mark='c'/> {na} after. The probability moved onto "
            "the answers that check out."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn))
            vo.wait_until("a")
            self.add(dot, val)
            self.play(Create(line), t.animate.set_value(steps), run_time=4.0, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(qs), FadeIn(gl), LaggedStart(*[FadeIn(c_) for c_ in gb], lag_ratio=0.01), run_time=1.5)
            vo.wait_until("c")
            self.play(Transform(gb, ga), Transform(gl, gl2), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def process(self):
        n = 5
        steps = VGroup(*[RoundedRectangle(width=1.5, height=0.55, corner_radius=0.1, stroke_color=GREY_B, stroke_width=2,
                                          fill_color=GREY_B, fill_opacity=0.1) for _ in range(n)]).arrange(RIGHT, buff=0.35)
        for k, s_ in enumerate(steps):
            s_.add(label(rf"step ${k + 1}$" if k < n - 1 else r"answer", font_size=20, color=GREY_A).move_to(s_))
        top = steps.copy().move_to(UP * 1.4)
        bot = steps.copy().move_to(DOWN * 1.3)
        arr = lambda g: VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.04, stroke_width=2, color=GREY_D,
                                       max_tip_length_to_length_ratio=0.4) for a, b in zip(g, g[1:])])
        ta, ba = arr(top), arr(bot)
        tl = label(r"outcome reward: \ check only the answer", font_size=26, color=C.BITS).next_to(top, UP, buff=0.35)
        bl = label(r"process reward: \ a learned grader scores every step", font_size=26, color=C.TRUE_P).next_to(bot, UP, buff=0.35)
        tm = mark(True, 34).next_to(top[-1], DOWN, buff=0.15)
        bm = VGroup(*[mark(k != 2, 30).next_to(s_, DOWN, buff=0.15) for k, s_ in enumerate(bot)])
        tag = note(r"schematic").to_corner(DR, buff=0.25)
        cite_ = cite(r"H.~Lightman et al., \textit{Let's Verify Step by Step} (2023)", corner=DL)
        with self.voiceover(
            "What we used is an outcome reward: only the final answer is checked. <bookmark mark='a'/> The other "
            "way is a process reward: a second model, trained on people's judgments, scores every step, so a lucky "
            "guess after a wrong step earns nothing. <bookmark mark='b'/> Process rewards catch more, but a learned "
            "grader can be fooled, and a model under pressure learns to fool it. The big reasoning models of 2025 "
            "mostly rely on checkable outcomes: math with known answers, code with tests. Trained that way, "
            "DeepSeek-R1's chains of thought grew longer on their own, and started to double-check their own work."
        ) as vo:
            self.play(FadeIn(top), FadeIn(ta), FadeIn(tl), FadeIn(tag))
            self.play(FadeIn(tm, scale=1.4))
            vo.wait_until("a")
            self.play(FadeIn(bot), FadeIn(ba), FadeIn(bl), FadeIn(cite_))
            self.play(LaggedStart(*[FadeIn(m_, scale=1.4) for m_ in bm], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(Indicate(bm[2], color=WRONG_C, scale_factor=1.6))
        self.wait(0.3)
        self.clear_scene()
