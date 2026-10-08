from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.rl.common import Plot, label, load, mtex, note, pct_fmt, real_tag, smooth, source, tokens
from videos.rl.compute import HERO, load_run, prompt_text

ALGOS = [
    ("reinforce", r"REINFORCE, no baseline", C.PENALTY),
    ("rloo", r"RLOO", C.BASELINE),
    ("grpo", r"GRPO", C.ADVANTAGE),
    ("drgrpo", r"Dr.\ GRPO", C.KL),
    ("dapo", r"DAPO-style", C.ENTROPY),
    ("ppo", r"PPO + critic (GAE)", C.RL_POLICY),
]


def evals(name):
    r = load_run(name)
    e = r["evals"]
    return {k: np.array([x[k] for x in e], float) for k in ("step", "pass1", "acc_think", "acc_direct", "think_frac", "length")}


class RealRun(VoiceoverScene):
    def construct(self):
        self.hero()
        self.groups()
        self.compare()

    # ------------------------------------------------------------------
    def hero(self):
        e = evals(HERO)
        S = e["step"][-1]
        plot = Plot(x_range=(0, S), y_range=(0, 1), width=8.2, height=4.3, x_ticks=list(np.linspace(0, S, 5).astype(int)),
                    y_ticks=[0, 0.25, 0.5, 0.75, 1], y_fmt=pct_fmt, x_label=r"RL step (32 problems $\times$ 8 answers each)")
        plot.move_to(LEFT * 1.5 + DOWN * 0.45)
        spec = [("pass1", r"right, overall", C.REWARD, 5), ("acc_direct", r"right, when answering directly", WHITE, 3),
                ("acc_think", r"right, when showing work", C.WORK_TOK, 3), ("think_frac", r"shows its work", C.LENGTH, 3)]
        lines, keys = VGroup(), VGroup()
        for k, txt, col, w in spec:
            lines.add(plot.line(e["step"], smooth(e[k], 3), color=col, stroke_width=w))
            keys.add(VGroup(Line(ORIGIN, RIGHT * 0.4, color=col, stroke_width=5), label(txt, font_size=22)).arrange(RIGHT, buff=0.12))
        keys.arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(plot, RIGHT, buff=0.25).shift(UP * 0.5)
        head = label(r"The adder, trained with GRPO: reward 1 if right, 0 if wrong", font_size=30).to_edge(UP, buff=0.3)
        p0, p1 = e["pass1"][0], e["pass1"][-1]
        d0, d1 = e["acc_direct"][0], e["acc_direct"][-1]
        t0, t1 = e["think_frac"][0], e["think_frac"][-1]
        k40 = int(np.searchsorted(e["step"], 40))
        with self.voiceover(
            "Time to run it. We train the adder with GRPO: thirty-two problems per step, eight answers each, a reward "
            f"of one or zero, and nothing else. <bookmark mark='p'/> Accuracy on problems it has never seen climbs from "
            f"{p0 * 100:.0f} percent to {e['pass1'][k40] * 100:.0f} percent within forty steps. <bookmark mark='h'/> "
            "But how? You might expect it to start showing its work, since that's almost always right. "
            f"<bookmark mark='t'/> It barely does: from {t0 * 100:.0f} to {t1 * 100:.0f} percent of answers. "
            f"<bookmark mark='d'/> Instead, its direct answers stopped slipping: from {d0 * 100:.0f} to {d1 * 100:.0f} "
            "percent right. Forgetting a carry was always a choice the network could unlearn, one token at a time, "
            "and that was the cheapest way up."
        ) as vo:
            self.play(FadeIn(head), FadeIn(plot), FadeIn(real_tag()))
            vo.wait_until("p")
            self.play(Create(lines[0]), FadeIn(keys[0]), run_time=1.8)
            vo.wait_until("t")
            self.play(Create(lines[3]), FadeIn(keys[3]), Create(lines[2]), FadeIn(keys[2]), run_time=1.8)
            vo.wait_until("d")
            self.play(Create(lines[1]), FadeIn(keys[1]), run_time=1.8)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def groups(self):
        t = load("tree")
        trees = t["trees"]
        s_last = str(t["steps"][-1])

        def top(leaves, n=5):
            L = sorted(leaves, key=lambda x: -x["p"])[:n]
            return L
        cols = VGroup()
        for s, title in (("0", r"before RL"), (s_last, rf"after {s_last} steps")):
            rows = VGroup()
            for L in top(trees[s]):
                strip = tokens("", L["text"], font_size=20, cell=0.3, height=0.38, buff=0.02,
                               answer_color=None if L["r"] else C.PENALTY)
                p = MathTex(f"{L['p']:.2f}", font_size=26, color=C.REWARD if L["r"] else C.PENALTY)
                rows.add(VGroup(p, strip).arrange(RIGHT, buff=0.3))
            rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
            hd = label(title, font_size=28)
            cols.add(VGroup(hd, rows).arrange(DOWN, buff=0.3))
        cols.arrange(RIGHT, buff=1.2, aligned_edge=UP).move_to(DOWN * 0.2)
        head = label(rf"The model's five likeliest answers to ${t['a']} + {t['b']}$", font_size=30).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here are its five likeliest answers to our running example, before and after. Before, the right answer "
            "shared its probability with several slips. After, nearly all of it sits on the right answer, written "
            "directly. That's what RL did to this model: it sharpened."
        ):
            self.play(FadeIn(head), FadeIn(cols[0]))
            self.play(FadeIn(cols[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compare(self):
        curves = {}
        for name, _, _ in ALGOS:
            ys = [evals(f"{name}_s{s}") for s in range(3)]
            st = ys[0]["step"]
            P = np.array([y["pass1"] for y in ys])
            T = np.array([y["think_frac"] for y in ys])
            curves[name] = (st, P.mean(0), T.mean(0), T[:, -1])
        S = max(c[0][-1] for c in curves.values())
        top = Plot(x_range=(0, S), y_range=(0.6, 1.0), width=7.6, height=2.4, x_ticks=[],
                   y_ticks=[0.6, 0.8, 1.0], y_fmt=pct_fmt, y_label=r"held-out accuracy")
        top.move_to(LEFT * 1.6 + UP * 1.3)
        bot = Plot(x_range=(0, S), y_range=(0, 0.7), width=7.6, height=2.5, x_ticks=list(np.linspace(0, S, 5).astype(int)),
                   y_ticks=[0, 0.25, 0.5], y_fmt=pct_fmt, x_label=r"RL step (mean of 3 seeds)", y_label=r"answers that show their work")
        bot.move_to(LEFT * 1.6 + DOWN * 2.0)
        acc, thk, keys = VGroup(), VGroup(), VGroup()
        for name, txt, col in ALGOS:
            st, m, t, _ = curves[name]
            acc.add(top.line(st, np.clip(smooth(m, 3), 0.6, 1.0), color=col, stroke_width=3))
            thk.add(bot.line(st, np.clip(smooth(t, 3), 0, 0.7), color=col, stroke_width=3.5))
            keys.add(VGroup(Line(ORIGIN, RIGHT * 0.4, color=col, stroke_width=5), label(txt, font_size=22)).arrange(RIGHT, buff=0.12))
        keys.arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(top, RIGHT, buff=0.35).shift(DOWN * 1.4)
        head = label(r"Six algorithms from this video, same model, same data", font_size=30).to_edge(UP, buff=0.2)
        end = {n: float(c[3].mean()) for n, c in curves.items()}
        final_acc = {n: float(c[1][-1]) for n, c in curves.items()}
        assert end["reinforce"] < 0.05 and end["ppo"] > end["grpo"] + 0.05 and min(final_acc.values()) > 0.95, (end, final_acc)
        self.think_end = end
        per_answer = (end["grpo"] + end["rloo"]) / 2
        per_token = (end["dapo"] + end["drgrpo"] + end["ppo"]) / 3
        assert per_token > per_answer + 0.04, (per_answer, per_token)
        with self.voiceover(
            "Now the same experiment with six of the algorithms we've derived, three seeds each. "
            "<bookmark mark='a'/> On accuracy, they look almost interchangeable. PPO starts late, because its critic "
            "has to be trained first, and every one of them ends above ninety-five percent. "
            "<bookmark mark='t'/> But look at what they learned to do. GRPO and RLOO end up showing their work about "
            f"{per_answer * 100:.0f} percent of the time; DAPO, Dr. GRPO and PPO, about {per_token * 100:.0f}. "
            "<bookmark mark='r'/> And plain REINFORCE abandons showing its work completely. Same reward, same "
            "accuracy, different behavior. The difference turns out to hide in one innocent-looking average."
        ) as vo:
            self.play(FadeIn(head), FadeIn(top), FadeIn(bot), FadeIn(real_tag()))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(Create(l_), FadeIn(k)) for l_, k in zip(acc, keys)], lag_ratio=0.2), run_time=3)
            vo.wait_until("t")
            self.play(LaggedStart(*[Create(l_) for l_ in thk], lag_ratio=0.2), run_time=3)
            vo.wait_until("r")
            self.play(Indicate(keys[0], color=C.PENALTY), thk[0].animate.set_stroke(width=6))
        self.wait(0.5)
        self.clear_scene()
