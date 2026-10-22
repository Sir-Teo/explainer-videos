from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai28.common import (CHAIN, DIRECT, ORM_C, PART, PASS, PRM_C, RIGHT_C, VOTE, WRONG_C, chip, load,
                                   mark)


class Verify(VoiceoverScene):
    def construct(self):
        self.card()
        self.motivate()
        self.defs()
        self.history()
        self.experiment()
        self.one()
        self.turn()

    def card(self):
        card = chapter_card(3, r"Checking the steps", r"Should we grade the answer, or every step?", lit=(2021, 2023),
                            part=PART)
        with self.voiceover("Chapter three. Checking the steps."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def motivate(self):
        s = load("think_samples")
        rb, wg = float(s["right_bad_steps"]), float(s["wrong_good_steps"])
        # a schematic chain whose two errors cancel: right for the wrong reason
        digits = [5, 3, 8, 6]
        steps = [5, 9, 16, 22]  # 5+3 written as 9 (wrong), 9+8=17 written as 16 (wrong again): back on track
        ok = [True, False, False, True]
        loc = [True, False, False, True]
        q = VGroup(*[chip(str(x), 0.5, GREY_B, 24) for x in digits]).arrange(RIGHT, buff=0.08)
        st = VGroup(*[chip(str(x), 0.5, RIGHT_C if o else WRONG_C, 24, width=0.66, fill=0.2) for x, o in zip(steps, loc)])
        st.arrange(RIGHT, buff=0.08)
        ans = chip("22", 0.5, RIGHT_C, 24, width=0.66, fill=0.35)
        row = VGroup(q, MathTex(r"\to", font_size=30, color=GREY_C), st, MathTex(r"\to", font_size=30, color=GREY_C),
                     ans).arrange(RIGHT, buff=0.25).move_to(UP * 1.6)
        notes = VGroup(label(r"$5 + 3 \ne 9$", font_size=24, color=WRONG_C).next_to(st[1], UP, buff=0.25),
                       label(r"$9 + 8 \ne 16$", font_size=24, color=WRONG_C).next_to(st[2], DOWN, buff=0.25))
        sch = note(r"schematic").next_to(row, RIGHT, buff=0.3)
        keep_in_frame(sch)
        lines = VGroup(
            label(r"an answer checker says: \ right", font_size=28, color=RIGHT_C),
            label(r"a step checker says: \ two steps are wrong", font_size=28, color=WRONG_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 0.5)
        stat = label(rf"our model, \ made to think: \ ${100 * rb:.1f}\%$ of its right answers \\ have a wrong step on "
                     r"the way", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.6)
        if rb < 0.05:
            small = ("Small here, because two slips must cancel exactly. In long mathematical arguments, a right "
                     "number at the end of a broken argument is far more common, and rewarding it teaches the wrong "
                     "lesson.")
        else:
            small = ("And in long mathematical arguments, a right number at the end of a broken argument is more "
                     "common still; rewarding it teaches the wrong lesson.")
        with self.voiceover(
            "A checker of answers sees only the end. <bookmark mark='a'/> Here is a chain that adds five and three "
            "and writes nine, then adds eight and writes sixteen. Two mistakes, and they cancel: the final sum is "
            "right. <bookmark mark='b'/> A checker of answers rewards this. A checker of steps would flag two of "
            "them. <bookmark mark='c'/> How often does it happen? Among our model's right answers, "
            f"{100 * rb:.1f} percent had a wrong step on the way. {small}"
        ) as vo:
            self.play(FadeIn(q), FadeIn(sch))
            vo.wait_until("a")
            self.play(FadeIn(row[1:]), FadeIn(notes))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(l_, shift=UP * 0.1) for l_ in lines], lag_ratio=0.5))
            vo.wait_until("c")
            self.play(FadeIn(stat))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def defs(self):
        orm = definition_card(r"outcome reward model \ (ORM)",
                              cmath(r"r(x, y)", r"=", r"P(\text{final answer right} \mid x, y)", font_size=30),
                              color=ORM_C, width=6.2, kind=r"Definition")
        prm = definition_card(r"process reward model \ (PRM)",
                              cmath(r"r(x, y)", r"=", r"\prod_{t} P(\text{step } t \text{ right} \mid x, y_{\le t})",
                                    font_size=30), color=PRM_C, width=6.2, kind=r"Definition")
        VGroup(orm, prm).arrange(RIGHT, buff=0.4).move_to(UP * 1.6)
        lo = label(r"one label per solution: \\ is the final answer right?", font_size=22, color=ORM_C)
        lp = label(r"a label per step: \\ is this step right, given the ones before?", font_size=22, color=PRM_C)
        lo.next_to(orm, DOWN, buff=0.35)
        lp.next_to(prm, DOWN, buff=0.35)
        use = VGroup(label(r"used two ways:", font_size=26, color=GREY_A),
                     label(r"rerank: \ sample $N$ solutions, \ keep the one it scores highest \ (best-of-$N$)",
                           font_size=24),
                     label(r"reward: \ the score is the reward for reinforcement learning", font_size=24))
        use.arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "So there are two kinds of learned grader. <bookmark mark='a'/> An outcome reward model reads a whole "
            "solution and predicts whether its final answer is right. It is trained with one label per solution, "
            "which a checker of answers can supply. <bookmark mark='b'/> A process reward model judges every step: "
            "is this step right, given the ones before it? A solution's score is the product over its steps, the "
            "chance that all of them are right. It needs a label for every step. <bookmark mark='c'/> Either can "
            "rerank: sample N solutions and keep the one it scores highest. Or its score can be the reward for "
            "reinforcement learning."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(orm, shift=UP * 0.15), FadeIn(lo))
            vo.wait_until("b")
            self.play(FadeIn(prm, shift=UP * 0.15), FadeIn(lp))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(u, shift=UP * 0.1) for u in use], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        cards = VGroup(
            history_card(2021, r"K.~Cobbe et al., \ OpenAI: \ GSM8K and verifiers",
                         r"a learned outcome grader picks among $100$ samples: \ worth about a $30\times$ larger "
                         r"model", width=6.4, color=ORM_C),
            history_card(2022, r"J.~Uesato et al., \ DeepMind", r"outcome or process feedback: \ similar final "
                         r"answers, \ but sound reasoning inside right answers needed process feedback \ (or a grader "
                         r"trained to imitate it)", width=6.4, color=PRM_C),
            history_card(2023, r"H.~Lightman et al., \ OpenAI: \ \textit{Let's Verify Step by Step}",
                         r"PRM800K: \ $800{,}000$ step labels by people, \ on $75{,}000$ solutions to $12{,}000$ "
                         r"problems", width=6.4, color=PRM_C),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([-3.2, 0, 0])
        bars = VGroup()
        for i, (t, v, c) in enumerate(((r"majority vote", 69.6, VOTE), (r"outcome RM", 72.4, ORM_C),
                                       (r"process RM", 78.2, PRM_C))):
            b = Rectangle(width=0.85, height=4.0 * (v - 60) / 25, stroke_width=0, fill_color=c, fill_opacity=0.9)
            b.move_to([2.3 + 1.45 * i, -2.0, 0], aligned_edge=DOWN)
            bars.add(VGroup(b, label(rf"${v}\%$", font_size=22, color=c).next_to(b, UP, buff=0.08),
                            label(t, font_size=18, color=c).next_to(b, DOWN, buff=0.12)))
        base = Line([1.7, -2.0, 0], [5.8, -2.0, 0], color=GREY_C, stroke_width=1.5)
        bh = label(r"MATH, \ best of $1{,}860$ samples: \\ problems solved", font_size=22, color=GREY_A)
        bh.next_to(VGroup(bars, base), UP, buff=0.4)
        cut = note(r"bars start at $60\%$").next_to(base, DOWN, buff=0.55).align_to(base, RIGHT)
        with self.voiceover(
            "The idea of a learned grader came with the grade-school maths benchmark itself. <bookmark mark='a'/> "
            "In 2021, Karl Cobbe and colleagues at OpenAI trained a verifier to pick among a hundred sampled "
            "solutions, and found it was worth about as much as a model thirty times larger. <bookmark mark='b'/> "
            "In 2022, Jonathan Uesato and colleagues at DeepMind compared the two kinds of feedback. Outcome feedback "
            "gave final answers about as good, with fewer labels; but to keep the reasoning inside right answers "
            "sound, they needed process feedback, or a grader trained to imitate it. <bookmark mark='c'/> In 2023, OpenAI's Let's Verify Step by Step paid people to "
            "label eight hundred thousand steps. <bookmark mark='d'/> Reranking 1,860 solutions to competition "
            "problems, a majority vote solved 69.6 percent, the outcome grader 72.4, and the process grader 78.2."
        ) as vo:
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.15))
            vo.wait_until("d")
            self.play(Create(base), FadeIn(bh), FadeIn(cut),
                      LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], DOWN), FadeIn(b[1]), FadeIn(b[2])) for b in bars],
                                  lag_ratio=0.4), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def experiment(self):
        v = load("think_verify")
        Ns = [int(n) for n in v["Ns"]]
        lN = np.log2(Ns)
        ys = {k: np.asarray(v[f"bo_{k}"]) for k in ("oracle", "prm", "orm", "vote", "first")}
        lo = float(np.floor(min(y.min() for y in ys.values()) * 10) / 10)
        g = axes([0, lN[-1]], [lo, 1.0], x_length=7.0, y_length=4.4, xlabel=r"solutions sampled per question, \ $N$",
                 ylabel=r"questions answered right", xticks=list(lN), xfmt=lambda x: f"{int(2 ** x)}",
                 yticks=[lo, (lo + 1) / 2, 1.0], yfmt=lambda y: rf"{int(round(100 * y))}\%", center=[-1.7, -0.35, 0])
        ax = g.ax
        cols = {"oracle": PASS, "prm": PRM_C, "orm": ORM_C, "vote": VOTE}
        lines = {k: curve(ax, lN, ys[k], c, 4 if k in ("prm", "orm") else 3) for k, c in cols.items()}
        lines["oracle"] = DashedVMobject(lines["oracle"], num_dashes=40)
        lg = legend([(PRM_C, r"best by the process RM"), (ORM_C, r"best by the outcome RM"), (VOTE, r"majority vote"),
                     (PASS, r"any right \ (a perfect checker)")], font_size=19)
        lg.next_to(g, RIGHT, buff=0.3).shift(UP * 0.9)
        if lg.get_right()[0] > 6.9:
            lg.shift(LEFT * (lg.get_right()[0] - 6.9))
        auc = label(rf"telling right from wrong \ (AUC): \\ outcome ${v['auc_orm']:.2f}$, \ process ${v['auc_prm']:.2f}$",
                    font_size=19, color=GREY_A).next_to(lg, DOWN, buff=0.35).align_to(lg, LEFT)
        tag = note(rf"computed: \ both graders trained on the same ${int(v['n_train']):,}$ solutions; \ "
                   rf"${int(v['nq'])}$ new questions".replace(",", "{,}")).to_corner(DR, buff=0.2)
        p, o, vt, orc = ys["prm"][-1], ys["orm"][-1], ys["vote"][-1], ys["oracle"][-1]
        N = Ns[-1]
        if p > o + 0.02:
            said = (f"With {N} samples, the process grader picks a right solution for {100 * p:.0f} percent of the "
                    f"questions, the outcome grader {100 * o:.0f}, and the vote {100 * vt:.0f}. Same solutions, same "
                    "budget: step labels carry more information per example, and the grader learns more from them.")
        elif o > p + 0.02:
            said = (f"Here the outcome grader does better: {100 * o:.0f} percent against {100 * p:.0f} for the process "
                    f"grader, and {100 * vt:.0f} for the vote. On a task this regular, the final answer already says a "
                    "lot about the steps.")
        else:
            said = (f"Both graders end close together, {100 * p:.0f} and {100 * o:.0f} percent, against "
                    f"{100 * vt:.0f} for the vote.")
        with self.voiceover(
            "We can run the comparison on our adding model. Take eight thousand of its solutions, made to think. "
            "Train one small grader on the final answers, and another on the steps, each step checked against the "
            "one before. <bookmark mark='a'/> Then, on new questions, sample N solutions and let each grader pick. "
            f"<bookmark mark='b'/> {said} <bookmark mark='c'/> The dashed line is a perfect checker; the gap below it "
            "is what a better grader could still win."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(lines["vote"]), FadeIn(lg[2]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lines["orm"]), FadeIn(lg[1]), run_time=1.5)
            self.play(Create(lines["prm"]), FadeIn(lg[0]), FadeIn(auc), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(lines["oracle"]), FadeIn(lg[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def one(self):
        v = load("think_verify")
        tok = [int(t) for t in np.asarray(v["ex_tokens"]) if t >= 0]
        d = [t for t in tok[:10] if t < 10]
        steps, ans = [], None
        phase = 0
        for t in tok[11:]:
            if t == 12:
                phase = 1
            elif t == 13:
                phase = 2
            elif t >= 15:
                if phase == 1:
                    steps.append(t - 15)
                elif phase == 2:
                    ans = t - 15
                    break
        ok = [bool(x) for x in np.asarray(v["ex_step_ok"])]
        sc = np.asarray(v["ex_prm"], float)
        items = [str(s_) for s_ in steps] + [str(ans)]
        q = VGroup(*[chip(str(x), 0.46, GREY_B, 22) for x in d]).arrange(RIGHT, buff=0.06).move_to([0, 2.7, 0])
        ql = label(r"a solution our model wrote", font_size=22, color=GREY_A).next_to(q, LEFT, buff=0.3)
        W = 0.62
        xs = [-((len(items) - 1) * (W + 0.18)) / 2 + i * (W + 0.18) for i in range(len(items))]
        cells = VGroup(*[chip(t, 0.5, (RIGHT_C if o else WRONG_C) if i < len(steps) else (RIGHT_C if o else WRONG_C),
                              22, width=W, fill=0.2).move_to([x, 1.5, 0]) for i, (t, o, x) in enumerate(zip(items, ok, xs))])
        sl = label(r"steps, \ then the answer \ (colour: \ the true check)", font_size=20, color=GREY_A)
        sl.next_to(cells, UP, buff=0.15)
        H = 2.2
        base_y = -1.6
        bars = VGroup(*[Rectangle(width=W * 0.7, height=max(H * float(s_), 0.02), stroke_width=0, fill_color=PRM_C,
                                  fill_opacity=0.85).move_to([x, base_y + H * float(s_) / 2, 0]) for s_, x in zip(sc, xs)])
        vals = VGroup(*[label(rf"${float(s_):.2f}$", font_size=18, color=PRM_C).next_to(b, UP, buff=0.05)
                        for s_, b in zip(sc, bars)])
        base = Line([xs[0] - 0.5, base_y, 0], [xs[-1] + 0.5, base_y, 0], color=GREY_C, stroke_width=1.5)
        bl = label(r"the process grader, \ step by step", font_size=22, color=PRM_C).next_to(base, DOWN, buff=0.2)
        bad = [i for i, o in enumerate(ok) if not o]
        prod = float(np.prod(sc))
        orm = label(rf"outcome grader: \ ${float(v['ex_orm']):.2f}$ \ for the whole solution", font_size=22,
                    color=ORM_C).to_edge(DOWN, buff=0.35).shift(LEFT * 2.6)
        pr = label(rf"process grader: \ product $= {prod:.2f}$", font_size=22, color=PRM_C).to_edge(DOWN, buff=0.35)
        pr.shift(RIGHT * 3.0)
        first_bad = bad[0] if bad else None
        if first_bad is not None and sc[first_bad] < 0.5:
            where = (f"Its score drops at the first wrong step, step {first_bad + 1}, to {sc[first_bad]:.2f}: it "
                     "points at the mistake.")
        elif first_bad is not None:
            where = (f"It is less sure at the first wrong step, step {first_bad + 1}, but not by much: "
                     f"{sc[first_bad]:.2f}. A learned grader can miss.")
        else:
            where = "Every step checks out."
        with self.voiceover(
            "Here is one of the solutions, graded both ways. <bookmark mark='a'/> The colours are the truth: which "
            "steps really are right. <bookmark mark='b'/> The process grader gives every step a probability of being "
            f"right. {where} <bookmark mark='c'/> The outcome grader gives the whole solution one number, "
            f"{float(v['ex_orm']):.2f}, and cannot say where it went wrong. That location is what makes step labels "
            "useful, for reranking and for teaching."
        ) as vo:
            self.play(FadeIn(q), FadeIn(ql))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cells], lag_ratio=0.1), FadeIn(sl))
            vo.wait_until("b")
            self.play(Create(base), FadeIn(bl), LaggedStart(*[AnimationGroup(GrowFromEdge(b, DOWN), FadeIn(t))
                                                            for b, t in zip(bars, vals)], lag_ratio=0.15), run_time=2.5)
            if first_bad is not None:
                self.play(Indicate(cells[first_bad], color=WRONG_C), Indicate(bars[first_bad], color=WRONG_C))
            self.play(FadeIn(pr))
            vo.wait_until("c")
            self.play(FadeIn(orm))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def turn(self):
        hc = history_card(2025, r"DeepSeek-R1: \ ``unsuccessful attempts''", r"a process reward model: \ hard to say "
                          r"what a step is in general reasoning, \ hard to check one, \ and ``once a model-based PRM is "
                          r"introduced, \ it inevitably leads to reward hacking''", width=8.4, color=WRONG_C)
        hc.move_to(UP * 1.7)
        rows = VGroup(
            label(r"RL on outcomes that can be checked exactly: \ maths answers, \ code tests, \ proofs", font_size=24,
                  color=RIGHT_C),
            label(r"process graders live on for search and reranking, \ with labels made automatically \\ (finish "
                  r"each partial solution many times: \ how often does it end right?)", font_size=24, color=PRM_C),
            label(r"and graders that themselves think before judging", font_size=24, color=ORM_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 1.2)
        cite_ = cite(r"DeepSeek-AI (2025); \ P.~Wang et al., \textit{Math-Shepherd} (2023)")
        with self.voiceover(
            "And yet the models that changed the field in 2025 mostly did not train against process graders. "
            "DeepSeek's R1 paper lists them among its unsuccessful attempts: it is hard to say what a step is in "
            "general reasoning, hard to check one, and a learned grader, pushed by reinforcement learning, gets "
            "exploited: in their words, it inevitably leads to reward hacking. <bookmark mark='a'/> So the recipe "
            "became reinforcement learning on outcomes that can be checked exactly: answers to maths problems, tests "
            "for code, proofs. <bookmark mark='b'/> Process graders live on for search and reranking, with step "
            "labels made automatically: finish a partial solution many times, and see how often it ends right. "
            "<bookmark mark='c'/> And the newest graders think before they judge. Learning from a checker is the "
            "subject of the next chapter."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(cite_))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()
