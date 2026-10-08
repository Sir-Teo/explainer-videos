from __future__ import annotations

from math import comb

import numpy as np

from explainer import *  # noqa: F403
from videos.rl.common import (Plot, color_grpo, exact_tag, grpo_objective, label, load, mtex, note, part_card, real_tag,
                              source, tokens, why)
from videos.rl.compute import prompt_text


def kappa(G: int, p: np.ndarray) -> np.ndarray:
    """Exact expected GRPO weight on grad p for a group of G binary rewards (population std, ddof 0):
    E[A_i grad log pi(y_i)] = kappa_G(p) grad p."""
    p = np.asarray(p, float)
    out = np.zeros_like(p)
    for s in range(G):
        w = comb(G - 1, s) * p**s * (1 - p) ** (G - 1 - s)
        out += w * (np.sqrt((G - 1 - s) / (s + 1)) + np.sqrt(s / (G - s)))
    return out


class GRPO(VoiceoverScene):
    def construct(self):
        self.t = load("tree")
        self.card()
        self.group()
        self.loo()
        self.stdnorm()
        self.zero_var()
        self.full()

    def card(self):
        c = part_card(4, r"Reasoning, with a checker", r"GRPO and the algorithms behind reasoning models")
        self.play(FadeIn(c, shift=UP * 0.2))
        self.wait(1.6)
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def pick_group(self):
        best = None
        for g in self.t["groups"]:
            r = np.array(g["r"])
            k = r.sum()
            modes = {t.startswith(">") for t in g["texts"]}
            score = abs(k - 5) + (0 if len(modes) == 2 else 2)
            if best is None or score < best[0]:
                best = (score, g)
        return best[1]

    def group(self):
        g = self.pick_group()
        self.grp = g
        prompt = prompt_text(self.t["a"], self.t["b"])
        r = np.array(g["r"], float)
        G = len(r)
        rows = VGroup()
        for t, ri in zip(g["texts"], r):
            strip = tokens("", t, font_size=20, cell=0.3, height=0.38, buff=0.02)
            mark = label(r"\checkmark" if ri else r"$\times$", font_size=28, color=C.REWARD if ri else C.PENALTY)
            rr = MathTex(rf"R={int(ri)}", font_size=28, color=C.REWARD if ri else C.PENALTY)
            rows.add(VGroup(strip, mark, rr))
        for i, row in enumerate(rows):
            y = 2.0 - i * 0.55
            row[0].move_to([-3.2, y, 0], aligned_edge=LEFT).shift(LEFT * 0.0)
            row[0].align_to(np.array([-4.6, 0, 0]), LEFT)
            row[1].move_to([0.9, y, 0])
            row[2].move_to([1.9, y, 0])
        ptxt = tokens(prompt, "", font_size=24, cell=0.36, height=0.46).to_edge(UP, buff=0.25).to_edge(LEFT, buff=0.6)
        pl = label(rf"one prompt, a group of $G = {G}$ real answers from the starting model", font_size=24, color=GREY_A)
        pl.next_to(ptxt, RIGHT, buff=0.4)
        rows.next_to(ptxt, DOWN, buff=0.35).align_to(ptxt, LEFT)
        mean = r.mean()
        base = mtex(rf"\bar R = {mean:.3g}", font_size=40, color=C.BASELINE).move_to(RIGHT * 5.3 + UP * 1.4)
        bl = label(r"the group's average:\\a free estimate of $V(x)$", font_size=26, color=C.BASELINE).next_to(base, DOWN, buff=0.2)
        A = mtex(r"A_i = R_i - \bar R", font_size=38, color=C.ADVANTAGE)
        advs = VGroup(*[MathTex(rf"{ri - mean:+.3g}", font_size=28, color=C.REWARD if ri > mean else C.PENALTY)
                        .move_to([3.0, row.get_y(), 0]) for ri, row in zip(r, rows)])
        A.move_to(RIGHT * 5.3 + DOWN * 0.6)
        cap = label(r"no critic network: the other answers to the same prompt are the baseline", font_size=26, color=YELLOW)
        cap.to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "In 2024, DeepSeek's math model introduced the algorithm behind many of today's open reasoning models: "
            "group relative policy optimization, GRPO. Its idea is to replace the critic with something free. "
            f"<bookmark mark='g'/> For each prompt, sample a group of answers. Here are {G} real ones from our pocket "
            "model. <bookmark mark='r'/> A checker grades each one: one if right, zero if wrong. "
            "<bookmark mark='b'/> The group's average reward is an estimate of the value of the prompt, the very "
            "thing the critic was trained to predict. <bookmark mark='a'/> Subtract it, and you have an advantage "
            "for every answer, with no value network at all."
        ) as vo:
            self.play(FadeIn(ptxt), FadeIn(pl), FadeIn(real_tag()))
            vo.wait_until("g")
            self.play(LaggedStart(*[FadeIn(row[0], shift=RIGHT * 0.2) for row in rows], lag_ratio=0.08), run_time=1.5)
            vo.wait_until("r")
            self.play(LaggedStart(*[FadeIn(VGroup(row[1], row[2])) for row in rows], lag_ratio=0.06))
            vo.wait_until("b")
            self.play(FadeIn(base), FadeIn(bl))
            vo.wait_until("a")
            self.play(FadeIn(A), LaggedStart(*[FadeIn(a) for a in advs], lag_ratio=0.06))
            self.play(FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def loo(self):
        l1 = mtex(r"\bar R", r"=", r"\tfrac1G R_i", r"+", r"\tfrac{G-1}{G}\,\bar R_{-i}", font_size=42)
        l1[4].set_color(C.BASELINE)
        l2 = mtex(r"R_i - \bar R", r"=", r"\frac{G-1}{G}", r"\Big(R_i - \bar R_{-i}\Big)", font_size=42)
        l2[2].set_color(YELLOW)
        l2[3].set_color(C.ADVANTAGE)
        col = VGroup(l1, l2).arrange(DOWN, buff=0.5).move_to(UP * 0.8)
        n1 = why(r"$\bar R_{-i}$: the average of the \emph{other} $G - 1$ answers").next_to(l1, DOWN, buff=0.12)
        b = Brace(l2[3], DOWN, color=C.ADVANTAGE)
        bl = label(r"leave-one-out (RLOO): independent of answer $i$, so unbiased", font_size=26, color=C.ADVANTAGE).next_to(b, DOWN, buff=0.1)
        concl = label(r"GRPO's centered advantage $=$ RLOO's, times a constant: the same unbiased gradient", font_size=28, color=YELLOW)
        concl.to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Is that baseline legal? It includes the answer itself, and a baseline isn't allowed to depend on the "
            "sampled answer. But split the average into answer i's own share and the average of the other answers. "
            "<bookmark mark='r'/> Rearranged, answer i minus the group mean is exactly a constant times answer i "
            "minus the average of the others, <bookmark mark='l'/> and that leave-one-out baseline is independent "
            "of answer i. So the group mean gives an unbiased gradient, just scaled by G minus one over G. This "
            "leave-one-out version is known as RLOO."
        ) as vo:
            self.play(Write(l1), FadeIn(n1))
            vo.wait_until("r")
            self.play(Write(l2))
            vo.wait_until("l")
            self.play(GrowFromCenter(b), FadeIn(bl))
            self.play(FadeIn(concl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def stdnorm(self):
        A = mtex(r"\hat A_i", r"=", r"\frac{R_i - \operatorname{mean}(R)}{\operatorname{std}(R)}", font_size=44).to_edge(UP, buff=0.4).shift(LEFT * 4.2)
        A[0].set_color(C.ADVANTAGE)
        bin_ = VGroup(mtex(r"\text{right: } +\sqrt{\tfrac{1-p}{p}}", font_size=32, color=C.REWARD),
                      mtex(r"\text{wrong: } -\sqrt{\tfrac{p}{1-p}}", font_size=32, color=C.PENALTY)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        bin_.next_to(A, DOWN, buff=0.35).align_to(A, LEFT)
        bn = why(r"rewards 0 or 1, success rate $p$:\ \ std $= \sqrt{p(1-p)}$").next_to(bin_, DOWN, buff=0.2).align_to(A, LEFT)
        e1 = mtex(r"\mathbb{E}\big[\hat A\, \nabla \log \pi\big]", r"=", r"\frac{\nabla p}{\sqrt{p(1-p)}}", r"=",
                  r"\nabla\big[\,2\arcsin\sqrt{p}\,\big]", font_size=36)
        e1[4].set_color(YELLOW)
        e1.next_to(bn, DOWN, buff=0.45).align_to(A, LEFT)
        plot = Plot(x_range=(0, 1), y_range=(0, 6), width=4.9, height=3.6, x_ticks=[0, 0.25, 0.5, 0.75, 1], y_ticks=[0, 2, 4, 6],
                    x_label=r"$p$: chance the model gets this prompt right", y_label=r"weight on $\nabla p$")
        plot.to_edge(RIGHT, buff=0.3).shift(DOWN * 0.3)
        ps = np.linspace(0.004, 0.996, 300)
        inf = plot.line(ps, np.minimum(1 / np.sqrt(ps * (1 - ps)), 6), color=YELLOW, stroke_width=4)
        cols = {2: GREY_B, 4: C.BASELINE, 8: C.ADVANTAGE, 64: C.KL}
        finite = VGroup(*[plot.line(ps, np.minimum(kappa(G, ps), 6), color=c, stroke_width=2.5) for G, c in cols.items()])
        keys = VGroup(label(r"$G \to \infty$: $1/\sqrt{p(1-p)}$", font_size=22, color=YELLOW),
                      *[label(rf"$G = {G}$", font_size=22, color=c) for G, c in cols.items()]).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        keys.next_to(plot.c2p(0.5, 6), DOWN, buff=0.1)
        assert abs(kappa(2, np.array([0.3]))[0] - 1.0) < 1e-12
        assert abs(kappa(8, np.array([0.1]))[0] * np.sqrt(0.09) - 0.698) < 0.002
        refl = mtex(r"\mathbb{E}\big[(R - p)\nabla \log \pi\big] = \nabla p", font_size=30, color=C.BASELINE)
        refl.next_to(e1, DOWN, buff=0.35).align_to(A, LEFT)
        rn = why(r"(without the std: plain expected reward, the same weight for every prompt)").next_to(refl, DOWN, buff=0.1).align_to(A, LEFT)
        with self.voiceover(
            "GRPO does one more thing: it divides by the group's standard deviation. That looks like a harmless "
            "normalization, but it changes what's being optimized. <bookmark mark='b'/> With rewards of zero and one "
            "and a success rate p, the standard deviation is the square root of p times one minus p, so a right "
            "answer gets this advantage, and a wrong one this. <bookmark mark='e'/> Average over the samples, and "
            "the expected update is the gradient of p, divided by that same square root. "
            "<bookmark mark='a'/> And that's the derivative of two arcsine root p."
        ) as vo:
            self.play(Write(A))
            vo.wait_until("b")
            self.play(FadeIn(bin_), FadeIn(bn))
            vo.wait_until("e")
            self.play(Write(e1[:3]))
            vo.wait_until("a")
            self.play(Write(e1[3:]))
            self.play(FadeIn(refl), FadeIn(rn))
        with self.voiceover(
            "So GRPO doesn't maximize the success rate itself. It maximizes the arcsine of its square root, which "
            "puts extra weight on prompts the model almost always fails or almost always solves. "
            "<bookmark mark='w'/> Here's that weight, as a function of p. With a finite group it's tamer: "
            "<bookmark mark='g'/> these are the exact curves for groups of two to sixty-four. With two answers, the "
            "normalization does nothing at all. <bookmark mark='f'/> And two arcsine root p has a meaning: it's the "
            "distance along the family of coin flips, measured with the Fisher information, the same geometry as "
            "the natural gradient. Some labs keep this weighting; others, like OLMo 3, DeepSeek-V3.2 and Dr. GRPO, "
            "drop the division."
        ) as vo:
            vo.wait_until("w")
            self.play(FadeIn(plot), Create(inf), FadeIn(keys[0]), FadeIn(exact_tag(r"exact, finite-$G$ formula")))
            vo.wait_until("g")
            self.play(LaggedStart(*[Create(f) for f in finite], lag_ratio=0.2), FadeIn(keys[1:]), run_time=2)
            vo.wait_until("f")
            fr = label(r"$2\arcsin\sqrt{p} = \int_0^p \frac{dt}{\sqrt{t(1-t)}}$:\ \ Fisher--Rao arc length of a coin",
                       font_size=24, color=YELLOW).to_edge(DOWN, buff=0.55)
            self.play(FadeIn(fr))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def zero_var(self):
        plot = Plot(x_range=(0, 1), y_range=(0, 1), width=6.6, height=3.8, x_ticks=[0, 0.25, 0.5, 0.75, 1], y_ticks=[0, 0.5, 1],
                    y_fmt=lambda v: MathTex(rf"{int(100 * v)}\%", font_size=24, color=GREY_A),
                    x_label=r"$p$: the prompt's success rate", y_label=r"chance the whole group agrees")
        plot.move_to(DOWN * 0.4 + LEFT * 1.4)
        ps = np.linspace(0, 1, 300)
        cols = {4: C.BASELINE, 8: C.ADVANTAGE, 16: C.KL}
        lines = VGroup(*[plot.line(ps, ps**G + (1 - ps) ** G, color=c, stroke_width=4) for G, c in cols.items()])
        keys = VGroup(*[label(rf"$G = {G}$", font_size=24, color=c) for G, c in cols.items()]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        keys.next_to(plot, RIGHT, buff=0.3).shift(UP * 0.8)
        f = mtex(r"P(\text{all equal}) = p^G + (1-p)^G", font_size=36).to_edge(UP, buff=0.4)
        n = VGroup(label(r"all right or all wrong: every advantage is $0$, and the group teaches nothing", font_size=26),
                   label(r"DAPO's \emph{dynamic sampling}: drop such groups, sample more prompts", font_size=26, color=GREY_A)
                   ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "There's a catch hiding in the group. If every answer in a group is right, or every one is wrong, "
            "every advantage is zero, and the whole group teaches nothing. <bookmark mark='p'/> That happens with "
            "probability p to the G plus one minus p to the G. On easy prompts, late in training, most groups are "
            "wasted compute. <bookmark mark='d'/> ByteDance's DAPO filters these groups out and keeps sampling "
            "until the batch is full of informative ones."
        ) as vo:
            self.play(Write(f))
            vo.wait_until("p")
            self.play(FadeIn(plot), LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.2), FadeIn(keys), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(n))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def full(self):
        m = color_grpo(grpo_objective(font_size=30)).move_to(UP * 0.6)
        if m.width > 13.4:
            m.width = 13.4
        notes = [
            (m[1], r"sampled by the old policy", C.OLD_POLICY, UP),
            (m[2], r"a group per prompt", C.BASELINE, DOWN),
            (m[5], r"importance ratio", C.RATIO, UP),
            (m[6], r"group-relative advantage", C.ADVANTAGE, DOWN),
            (m[7], r"PPO's clip", C.RATIO, UP),
            (m[10], r"leash to the reference ($k_3$)", C.KL, DOWN),
        ]
        braces = VGroup()
        for part, txt, col, d in notes:
            br = Brace(part, d, color=col, buff=0.08)
            lb = label(txt, font_size=22, color=col).next_to(br, d, buff=0.06)
            braces.add(VGroup(br, lb))
        q = Brace(m[3], DOWN, color=C.LENGTH, buff=0.08)
        ql = label(r"average over the answer's tokens: \emph{a trap}", font_size=22, color=C.LENGTH).next_to(q, DOWN, buff=0.55)
        qline = Line(q.get_bottom(), ql.get_top(), color=C.LENGTH, stroke_width=1.5)
        head = label(r"GRPO, as written in DeepSeekMath (2024)", font_size=30).to_edge(UP, buff=0.35)
        src = source(r"Shao et al., \emph{DeepSeekMath}, arXiv 2402.03300 (eq.\ 3; $G = 64$, $\beta = 0.04$)")
        with self.voiceover(
            "Now we can read the whole GRPO objective, the formula from the start of the video. Answers sampled by "
            "the old policy, in groups. The importance ratio, <bookmark mark='c'/> clipped as in PPO, times the "
            "group-relative advantage. <bookmark mark='k'/> And the leash to the reference model, estimated with "
            "k3. <bookmark mark='t'/> There's one piece we haven't explained: inside, each answer's tokens are "
            "averaged, one over the length of answer i. That innocent-looking average turns out to be a trap. But "
            "first, let's watch GRPO train a real model."
        ) as vo:
            self.play(FadeIn(head), Write(m), FadeIn(src), run_time=2)
            self.play(FadeIn(braces[0]), FadeIn(braces[1]), FadeIn(braces[2]))
            vo.wait_until("c")
            self.play(FadeIn(braces[4]), FadeIn(braces[3]))
            vo.wait_until("k")
            self.play(FadeIn(braces[5]))
            vo.wait_until("t")
            self.play(GrowFromCenter(q), Create(qline), FadeIn(ql))
        self.wait(0.4)
        self.clear_scene()
