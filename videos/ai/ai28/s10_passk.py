from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai28.common import DIRECT, PART, PASS, POLICY, REF, RIGHT_C, WRONG_C, load, seeds_plot
from videos.ai.ai28.s07_variants import COLS, NAMES, SAY


class PassK(VoiceoverScene):
    def construct(self):
        self.card()
        self.estimator()
        self.bias()
        self.debate()
        self.ours()
        self.caveat()

    def card(self):
        card = chapter_card(9, r"Sharper, or wider?", r"Does reinforcement learning teach a model anything new?",
                            lit=(2021, 2025), part=PART)
        with self.voiceover("Chapter nine. Sharper, or wider?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def estimator(self):
        colors = {r"k": PASS, r"c": RIGHT_C, r"p": RIGHT_C}
        rows = [
            cmath(r"\text{pass@}k", r"=", r"\mathbb E_x\big[1 - (1 - p_x)^k\big]", font_size=34),
            cmath(r"\widehat{\text{pass@}k}_{\text{naive}}", r"=", r"1 - \big(1 - \tfrac{c}{n}\big)^k", font_size=34),
            cmath(r"\mathbb E\big[(1 - \tfrac{c}{n})^k\big]", r"\ge", r"\big(1 - \mathbb E\,\tfrac{c}{n}\big)^k = (1 - p)^k",
                  font_size=34),
            cmath(r"\widehat{\text{pass@}k}", r"=", r"1 - \binom{n - c}{k} \Big/ \binom{n}{k}", font_size=34),
            cmath(r"\mathbb E\Big[\binom{n - c}{k} \Big/ \binom{n}{k}\Big]", r"=", r"(1 - p)^k", font_size=34),
        ]
        whys = [why(r"$p_x$: \ the chance one try at question $x$ is right"),
                why(r"$c$ of $n$ samples right: \ plug in $c/n$"),
                why(r"Jensen: \ $(1 - \cdot)^k$ is convex, \ so the naive guess is too low"),
                why(r"choose $k$ of the $n$ samples: \ all wrong?"),
                why(r"any $k$ of $n$ independent tries \ are $k$ independent tries")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.4, buff=0.5, edge=6.9)
        hc = history_card(2021, r"M.~Chen et al., \ OpenAI: \ \textit{Codex}", r"pass@$k$ and its unbiased estimator: "
                          r"\ $28.8\%$ of programming problems solved with one sample, \ $70.2\%$ with $100$",
                          width=5.4, color=PASS).to_corner(DR, buff=0.3)
        with self.voiceover(
            "To ask whether reinforcement learning teaches anything new, we need to measure what a model can do with "
            "many tries. The measure is pass at k: the chance that at least one of k tries is right, with a checker "
            "to say which. For a question where one try succeeds with probability p, that's one minus one minus p to "
            "the k. <bookmark mark='a'/> In practice we have n samples, c of them right. The obvious estimate plugs in "
            "c over n. <bookmark mark='b'/> But it is biased: one minus x to the k is convex, so by Jensen's "
            "inequality the plug-in estimate comes out too low on average. <bookmark mark='c'/> The fix, from "
            "OpenAI's Codex paper in 2021: choose k of your n samples at random, without replacement, and ask how "
            "likely they are to be all wrong. <bookmark mark='d'/> Any k of n independent tries are themselves k "
            "independent tries, so on average this is exactly one minus p to the k. Unbiased."
        ) as vo:
            step(0)
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                step(k + 1)
                if k == 2:
                    self.play(FadeIn(hc, shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bias(self):
        s = load("sampling")
        ks = [int(k) for k in s["ks"]]
        lk = np.log2(ks)
        ex, un, nv = (np.asarray(s[k], float) for k in ("exact", "unbiased", "naive"))
        lo = float(np.floor(min(nv.min(), ex.min()) * 10) / 10)
        g = axes([0, lk[-1]], [lo, 1.0], x_length=5.6, y_length=3.6, xlabel=r"tries, \ $k$",
                 ylabel=rf"pass@$k$ \ from $n = {int(s['n'])}$ samples", xticks=list(lk), xfmt=lambda x: f"{int(2 ** x)}",
                 yticks=[lo, 1.0], yfmt=lambda y: rf"{int(round(100 * y))}\%", center=[-3.4, -0.3, 0])
        ce = DashedVMobject(curve(g.ax, lk, ex, WHITE, 3), num_dashes=30)
        cu, cn = curve(g.ax, lk, un, PASS, 4), curve(g.ax, lk, nv, WRONG_C, 4)
        lg = legend([(WHITE, r"exact"), (PASS, r"unbiased estimate"), (WRONG_C, r"plug-in estimate")], font_size=19)
        lg.next_to(g.ax, UP, buff=0.4).align_to(g.ax, LEFT)
        # one question, many draws of n samples: the two estimates' spread at k = 8
        qn, qu = np.asarray(s["q_naive"]), np.asarray(s["q_unbiased"])
        qe = float(s["q_exact"])
        bins = np.linspace(0, 1, 26)
        h = axes([0, 1], [0, 1], x_length=4.6, y_length=2.8, xlabel=rf"one question's pass@${int(s['q_k'])}$ estimate",
                 xticks=[0, 0.5, 1], xfmt=lambda v: rf"{int(100 * v)}\%", center=[3.6, -0.6, 0])
        hb = {}
        for key, vals, col in (("u", qu, PASS), ("n", qn, WRONG_C)):
            cnt, _ = np.histogram(vals, bins)
            cnt = cnt / max(cnt.max(), 1)
            bw = h.ax.x_length / (len(bins) - 1)
            hb[key] = VGroup(*[Rectangle(width=bw * 0.42, height=max(2.6 * v, 0.004), stroke_width=0, fill_color=col,
                                         fill_opacity=0.85).move_to(h.ax.c2p((a + b) / 2, 0) + RIGHT * (bw * 0.22 if key == "u"
                                                                                                         else -bw * 0.22),
                                                                    aligned_edge=DOWN)
                               for v, a, b in zip(cnt, bins[:-1], bins[1:])])
        el = Line(h.ax.c2p(qe, 0), h.ax.c2p(qe, 1.05), color=WHITE, stroke_width=3)
        hl = label(rf"exact: \ ${100 * qe:.0f}\%$", font_size=20).next_to(el, UP, buff=0.05)
        tag = note(rf"computed: \ the addition model before RL, \ ${int(s['trials'])}$ draws of $n$ samples").to_corner(DR, buff=0.2)
        gap = 100 * float(np.max(ex - nv))
        with self.voiceover(
            "Here are both estimates on our addition model before reinforcement learning, where we know the exact "
            f"answer. <bookmark mark='a'/> The plug-in estimate falls short, by up to {gap:.0f} points. The unbiased "
            "one lies on the exact curve. <bookmark mark='b'/> For a single question the unbiased estimate is "
            "noisy, but centred on the truth; the plug-in one is centred too low. With a large benchmark, the noise "
            "averages out, and the bias doesn't."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(ce), FadeIn(lg[0]))
            self.play(Create(cn), FadeIn(lg[2]), Create(cu), FadeIn(lg[1]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(h), LaggedStart(*[GrowFromEdge(b, DOWN) for b in hb["n"]], lag_ratio=0.02),
                      LaggedStart(*[GrowFromEdge(b, DOWN) for b in hb["u"]], lag_ratio=0.02), Create(el), FadeIn(hl),
                      run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def debate(self):
        cards = VGroup(
            history_card(2025, r"Y.~Yue et al., \ Tsinghua: \ \textit{Does Reinforcement Learning Really Incentivize "
                         r"Reasoning Capacity in LLMs Beyond the Base Model?}", r"RL wins at small $k$; \ the base model "
                         r"wins at large $k$. \ RL sharpens what the base model could already find; \ distillation "
                         r"from a stronger teacher can add new reasoning", width=6.4, color=REF),
            history_card(2025, r"M.~Liu et al., \ NVIDIA: \ \textit{ProRL}", r"train long enough, \ with the KL controlled "
                         r"and the reference reset, \ and RL finds strategies the base model never reaches", width=6.4,
                         color=POLICY),
        ).arrange(RIGHT, buff=0.3, aligned_edge=UP).move_to(UP * 1.0)
        pic = VGroup()
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 1, 0.5], x_length=4.6, y_length=1.9, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([0, -2.3, 0])
        base = ax.plot(lambda x: 1 - math.exp(-0.45 * x) * 0.92 - 0.0, x_range=[0, 10], color=REF, stroke_width=3)
        rl = ax.plot(lambda x: 0.85 - 0.45 * math.exp(-0.9 * x), x_range=[0, 10], color=POLICY, stroke_width=3)
        pl = VGroup(label(r"base", font_size=18, color=REF).next_to(ax.c2p(10, 0.99), RIGHT, buff=0.08),
                    label(r"after RL", font_size=18, color=POLICY).next_to(ax.c2p(10, 0.85), RIGHT, buff=0.08),
                    label(r"$\log k$", font_size=18, color=GREY_B).next_to(ax, DOWN, buff=0.08),
                    label(r"pass@$k$", font_size=18, color=GREY_B).next_to(ax, LEFT, buff=0.08))
        pic.add(ax, base, rl, pl)
        sch = note(r"schematic: \ the crossover Yue et al.\ reported").next_to(ax, RIGHT, buff=1.0)
        with self.voiceover(
            "In April 2025, Yang Yue and colleagues at Tsinghua asked exactly this; the paper became an oral at "
            "NeurIPS that December. <bookmark mark='a'/> After reinforcement learning, one try is far "
            "better. But give both models hundreds of tries, and the base model, the one RL started from, solves "
            "more problems. The curves cross. Their reading: RL sharpens; it moves probability onto reasoning the base "
            "model could already find, and narrows the rest. Distilling a stronger teacher, by contrast, can add new "
            "reasoning. <bookmark mark='b'/> The reply came within weeks. NVIDIA's ProRL trained much longer, keeping "
            "the KL in check and resetting the reference model, and reported strategies the base model could not "
            "reach. The two are compatible: a short run sharpens; a long, diverse one may widen."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.15))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(pl), FadeIn(sch))
            self.play(Create(base), Create(rl), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ours(self):
        o = load("objectives")
        ks = [int(k) for k in o["ks"]]
        lk = np.log2(ks)
        base = np.asarray(o["passk_base"])
        show = ["pg", "grpo", "dapo", "cispo"]
        P = {v: np.asarray(o[f"{v}_passk"]) for v in show}  # (seeds, ks)
        lo = float(np.floor(min(base.min(), min(p.min() for p in P.values())) * 10) / 10)
        g = axes([0, lk[-1]], [lo, 1.0], x_length=7.0, y_length=4.4, xlabel=r"tries, \ $k$",
                 ylabel=r"pass@$k$, \ exact, \ $200$ questions", xticks=list(lk[::2]), xfmt=lambda x: f"{int(2 ** x)}",
                 yticks=[lo, (lo + 1) / 2, 1.0], yfmt=lambda y: rf"{int(round(100 * y))}\%", center=[-1.6, -0.3, 0])
        cb = curve(g.ax, lk, base, REF, 4)
        lines = {v: seeds_plot(g.ax, lk, P[v], COLS[v]) for v in show}
        lg = legend([(REF, r"before RL")] + [(COLS[v], NAMES[v]) for v in show], font_size=19)
        lg.next_to(g, RIGHT, buff=0.3).shift(UP * 0.8)
        tag = note(r"computed: \ every answer's probability, \ so pass@$k$ needs no sampling; \ $3$ runs each, \ band: "
                   r"lowest to highest").to_corner(DR, buff=0.2)
        means = {v: P[v].mean(0) for v in show}
        rl1 = float(np.mean([means[v][0] for v in show]))
        k_last = ks[-1]
        lost = [v for v in show if means[v][-1] < base[-1] - 0.01]
        pb = np.asarray(o["p_right_base"])
        dead = float(np.mean([((np.asarray(o[f"{v}_p_right"]) < 1e-3) & (pb > 1e-2)).sum(1).mean() for v in show]))
        if lost:
            cross = [int(ks[int(np.argmax(means[v] < base))]) for v in lost]
            said = (f"And the curves cross: at {k_last} tries the model before RL solves {100 * base[-1]:.1f} percent, "
                    f"while {SAY[lost[0]]} solves {100 * means[lost[0]][-1]:.1f}. From about {min(cross)} tries on, "
                    f"the untrained model is ahead. On about {dead:.0f} of the 200 questions, RL drained the right "
                    "answer's probability below one in a thousand, onto wrong answers it grew confident in.")
        else:
            said = (f"And at {k_last} tries the curves meet: {100 * base[-1]:.1f} percent before RL, and between "
                    f"{100 * min(m[-1] for m in means.values()):.1f} and {100 * max(m[-1] for m in means.values()):.1f} "
                    "after. On a problem this small, RL hasn't made any question impossible; it has made the easy "
                    "answers certain.")
        with self.voiceover(
            "We can check it exactly on our addition model, because we know its probability of every answer, so pass "
            f"at k needs no sampling, even at a thousand tries. <bookmark mark='a'/> Before RL, one try is right "
            f"{100 * base[0]:.0f} percent of the time. <bookmark mark='b'/> After three hundred steps, about "
            f"{100 * rl1:.0f} percent. <bookmark mark='c'/> {said}"
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(cb), FadeIn(lg[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(*[AnimationGroup(FadeIn(lines[v][0]), Create(lines[v][1])) for v in show],
                      *[FadeIn(lg[i + 1]) for i in range(len(show))], run_time=2.0)
            vo.wait_until("c")
            self.play(Indicate(cb, color=REF))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def caveat(self):
        gs = load("passk_guess")
        ks = [int(k) for k in gs["ks"]]
        pg = np.asarray(gs["passk"])
        formula = cmath(r"\text{pass@}k(\text{a random guess})", r"=", rf"1 - \big(1 - \tfrac{{1}}{{{int(gs['m'])}}}\big)^k",
                        font_size=34).move_to(UP * 2.2)
        vals = VGroup(*[label(rf"$k = {k}$: \ ${100 * p:.0f}\%$", font_size=28, color=DIRECT) for k, p in
                        zip(ks, pg) if k in (1, 64, 1024)]).arrange(RIGHT, buff=0.8).next_to(formula, DOWN, buff=0.5)
        lessons = VGroup(
            label(r"at large $k$, \ a checker can make guessing look like reasoning", font_size=26, color=WRONG_C),
            label(r"so: \ check the steps too, \ or use problems with huge answer spaces \ (proofs, code)",
                  font_size=26, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 1.4)
        p1024 = float(pg[ks.index(1024)]) if 1024 in ks else float(pg[-1])
        with self.voiceover(
            "One warning about measuring with many tries. A checker rewards a lucky guess as much as a reasoned answer. "
            f"Guess uniformly among the {int(gs['m'])} possible sums, and pass at a thousand and twenty-four is "
            f"{100 * p1024:.0f} percent. <bookmark mark='a'/> At large k, pass at k can make guessing look like "
            "reasoning. That's why careful studies also check the chains, or use problems whose answers are too many "
            "to guess: proofs, and programs that must pass tests."
        ) as vo:
            self.play(Write(formula))
            self.play(LaggedStart(*[FadeIn(v_) for v_ in vals], lag_ratio=0.4))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(l_, shift=UP * 0.1) for l_ in lessons], lag_ratio=0.5))
        self.wait(0.3)
        self.clear_scene()
