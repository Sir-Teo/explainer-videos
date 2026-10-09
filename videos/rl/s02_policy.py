from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.rl.common import (AnswerTree, label, load, mtex, part_card, real_tag, tokens, union_texts)
from videos.rl.compute import P_SLIP, P_THINK, answer_text, prompt_text


class Policy(VoiceoverScene):
    def construct(self):
        self.t = load("tree")
        self.base = load("base")
        self.card()
        self.mdp()
        self.tree()
        self.objective()
        self.adder()

    def card(self):
        c = part_card(1, r"The policy gradient", r"from one identity to PPO's critic")
        self.play(FadeIn(c, shift=UP * 0.2))
        self.wait(1.6)
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def mdp(self):
        rows = [(r"state $s_t$", r"the prompt and the tokens so far"), (r"action $y_t$", r"the next token"),
                (r"policy $\pi_\theta(y_t \mid s_t)$", r"the language model's softmax"),
                (r"transition", r"append the token (nothing random)"), (r"episode ends", r"at the end-of-answer token"),
                (r"reward $R(x, y)$", r"a checker, a test suite, a reward model\dots\ at the end")]
        cols = [C.TOKEN, C.SCORE, C.RL_POLICY, GREY_B, GREY_B, C.REWARD]
        table = VGroup()
        for (a, b), col in zip(rows, cols):
            table.add(VGroup(label(a, font_size=28, color=col), label(b, font_size=26, color=GREY_A)))
        for i, r in enumerate(table):
            y = 2.3 - i * 0.62
            r[0].move_to([-2.0, y, 0], aligned_edge=RIGHT)
            r[1].move_to([-1.4, y, 0], aligned_edge=LEFT)
        head = label(r"Reinforcement learning's vocabulary, for a language model", font_size=30).to_edge(UP, buff=0.3)
        t = self.t
        prompt = prompt_text(t["a"], t["b"])
        strip = tokens(prompt, answer_text(t["a"], t["b"], False), font_size=28).to_edge(DOWN, buff=1.0)
        n0 = len(prompt)
        cur = ValueTracker(0)
        hl = always_redraw(lambda: SurroundingRectangle(strip[n0 + int(cur.get_value())], color=C.SCORE, buff=0.04, stroke_width=3))
        ctx = always_redraw(lambda: SurroundingRectangle(strip[:n0 + int(cur.get_value())], color=C.TOKEN, buff=0.08, stroke_width=2))
        with self.voiceover(
            "First, the translation. To reinforcement learning, a language model is a policy. "
            "<bookmark mark='s'/> The state is everything written so far: the prompt and the answer's first few "
            "tokens. <bookmark mark='a'/> The action is the next token, drawn from the model's softmax. "
            "<bookmark mark='t'/> The environment couldn't be simpler: it appends the token. <bookmark mark='r'/> "
            "When the answer ends, a reward arrives. Everything else in this video is about that last line."
        ) as vo:
            self.play(FadeIn(head), FadeIn(strip, lag_ratio=0.03))
            vo.wait_until("s")
            self.play(FadeIn(table[0]), Create(ctx))
            vo.wait_until("a")
            self.play(FadeIn(table[1]), FadeIn(table[2]), Create(hl))
            vo.wait_until("t")
            self.play(FadeIn(table[3]), cur.animate.set_value(3), run_time=1.5, rate_func=linear)
            vo.wait_until("r")
            self.play(FadeIn(table[4]), FadeIn(table[5]), cur.animate.set_value(5), run_time=1.0, rate_func=linear)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tree(self):
        t = self.t
        trees = t["trees"]
        texts = union_texts([trees[s] for s in trees], min_p=3e-3)
        T0 = AnswerTree(trees["0"], texts, height=5.4, col_w=0.6, font_size=18)
        prompt = tokens(prompt_text(t["a"], t["b"]), "", font_size=24, cell=0.36, height=0.5)
        prompt.next_to(T0, LEFT, buff=0.25)
        g = VGroup(prompt, T0).move_to(DOWN * 0.15)
        if g.width > 13.6:
            g.width = 13.6
        rl = label(r"right?", font_size=22, color=GREY_A).next_to(T0.leaf_bars, UP, buff=0.12)
        head = label(rf"Every answer the model might give to ${t['a']} + {t['b']}$", font_size=28)
        head.to_edge(UP, buff=0.25)
        # a path: the likeliest direct answer, with its token probabilities
        leaves = sorted(trees["0"], key=lambda L: -L["p"])
        path = next(L for L in leaves if L["mode"] == "direct")["text"]
        blocks = [T0.blocks[path[:i + 1]] for i in range(len(path))]
        probs = []
        for i in range(len(path)):
            parent = T0.mass[path[:i]] if i else 1.0
            probs.append(T0.mass[path[:i + 1]] / parent)
        pm = mtex(r"\pi(y \mid x) = " + r" \times ".join(f"{q:.2f}" for q in probs) + rf" = {np.prod(probs):.2f}", font_size=30)
        pm.to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Here is the whole space of answers for one prompt, as the real model sees it. Reading left to right, "
            "each column is a token, and each block's height is the probability of reaching that prefix. The river "
            "splits wherever the model is unsure. <bookmark mark='w'/> The top stream shows its work, writing the "
            "sum backwards first; the rest answer directly, and fork at every carry. <bookmark mark='p'/> The "
            "probability of a whole answer is the product of its tokens' probabilities, along its path."
        ) as vo:
            self.play(FadeIn(head), FadeIn(prompt), FadeIn(T0.rects, lag_ratio=0.002), FadeIn(T0.glyph_group), run_time=2.5)
            self.play(FadeIn(real_tag(r"real model, exact probabilities")))
            vo.wait_until("w")
            self.play(Indicate(VGroup(*[b for q, b in T0.blocks.items() if q.startswith(">")]), color=C.WORK_TOK, scale_factor=1.02))
            vo.wait_until("p")
            self.play(LaggedStart(*[b.animate.set_fill(C.SCORE, opacity=0.8) for b in blocks], lag_ratio=0.15), FadeIn(pm))
        self.T0, self.tree_group, self.pm, self.head, self.rl = T0, g, pm, head, rl
        self.play(FadeOut(pm), *[b.animate.set_fill(token_fill(q), opacity=0.32) for q, b in zip([path[:i + 1] for i in range(len(path))], blocks)])

    # ------------------------------------------------------------------
    def objective(self):
        T0 = self.T0
        J = mtex(r"J(\theta)", r"=", r"\sum_y \pi_\theta(y \mid x)\, R(x, y)", r"=", r"\text{the green part of the last column}", font_size=34)
        J[0].set_color(C.RL_POLICY)
        J[4].set_color(C.REWARD)
        J.to_edge(DOWN, buff=0.15).shift(RIGHT * 0.9)  # clear of the corner tag
        pc = label(rf"${T0.p_correct * 100:.0f}\%$", font_size=26, color=C.REWARD).next_to(T0.leaf_bars, RIGHT, buff=0.12)
        with self.voiceover(
            "The checker marks each complete answer right or wrong: <bookmark mark='c'/> this last column. With a "
            "reward of one for right and zero for wrong, the expected reward is simply the total probability of the "
            "right answers: the green part of that column. <bookmark mark='g'/> Reinforcement learning, for us, "
            "means one thing: reshape the river so that more of it ends in green."
        ) as vo:
            vo.wait_until("c")
            self.play(FadeIn(T0.leaf_bars, lag_ratio=0.01), FadeIn(self.rl))
            self.play(Write(J), FadeIn(pc))
            vo.wait_until("g")
            self.play(Indicate(T0.leaf_bars, color=C.REWARD, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def adder(self):
        b = self.base
        ev = b["eval"]
        t = self.t
        prompt = prompt_text(t["a"], t["b"])
        wrong = next(L["text"] for L in sorted(t["trees"]["0"], key=lambda L: -L["p"]) if L["mode"] == "direct" and not L["r"])
        ex1 = tokens(prompt, answer_text(t["a"], t["b"], True), font_size=24)
        ex2 = tokens(prompt, answer_text(t["a"], t["b"], False), font_size=24)
        ex3 = tokens(prompt, wrong, font_size=24, answer_color=C.PENALTY)
        l1 = label(rf"{int(P_THINK * 100)}\%: show the work (sum written right to left, then the answer)", font_size=24, color=C.WORK_TOK)
        l2 = label(r"the rest answer at once\dots", font_size=24)
        l3 = label(rf"\dots and forget each carry with probability {P_SLIP:g}", font_size=24, color=C.PENALTY)
        rows = VGroup(*[VGroup(e, l).arrange(DOWN, aligned_edge=LEFT, buff=0.12) for e, l in ((ex1, l1), (ex2, l2), (ex3, l3))])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        rows.move_to(UP * 0.85)
        head = label(rf"The adder: a {b['cfg']['layers']}-layer transformer with {b['params']:,} parameters".replace(",", "{,}", 1),
                     font_size=30).to_edge(UP, buff=0.3)
        res = VGroup(
            label(rf"shows its work {ev['think_frac'] * 100:.0f}\% of the time, and is then right {ev['acc_think'] * 100:.1f}\%", font_size=28, color=C.WORK_TOK),
            label(rf"answers directly otherwise, and is then right {ev['acc_direct'] * 100:.0f}\%", font_size=28),
            label(rf"overall: {ev['pass1'] * 100:.0f}\% right", font_size=30, color=C.REWARD),
        ).arrange(DOWN, buff=0.18).move_to(DOWN * 2.1)
        with self.voiceover(
            "Meet the model behind that picture. It's a pocket-sized transformer, three layers deep, pretrained on "
            "text full of four-digit additions. <bookmark mark='w'/> A quarter of the examples show their work: the "
            "sum written right to left, digit by digit with its carries, then the answer. <bookmark mark='d'/> The "
            "rest answer at once, <bookmark mark='s'/> and like people doing sums in their heads, they sometimes "
            "forget to carry. <bookmark mark='r'/> The model learned both habits faithfully. It shows its work about "
            "a quarter of the time and is then almost always right; otherwise it slips like its teachers. We'll "
            "call it the adder."
        ) as vo:
            self.play(FadeIn(head), FadeIn(real_tag()))
            vo.wait_until("w")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
            vo.wait_until("s")
            self.play(FadeIn(rows[2]))
            vo.wait_until("r")
            self.play(LaggedStart(*[FadeIn(r) for r in res], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()


def token_fill(prefix: str):
    from videos.rl.common import token_color

    return token_color(prefix[-1], len(prefix) - 1, prefix.startswith(">"))
