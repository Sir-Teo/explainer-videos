from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai17.common import CHAIN, RIGHT_C, WRONG_C, curve, load

POLICY = C.NEURAL
RATIO, ADV, KLC = C.TRUE_P, C.BITS, C.SURPRISE
NAMES = {"pg": r"policy \\ gradient", "grpo": r"GRPO", "dr": r"Dr.~GRPO", "dapo": r"DAPO", "gspo": r"GSPO", "dpo": r"DPO"}
SAY = {"pg": "the plain policy gradient", "grpo": "GRPO", "dr": "Doctor GRPO", "dapo": "DAPO", "gspo": "GSPO", "dpo": "DPO"}
COLS = {"pg": GREY_B, "grpo": CHAIN, "dr": C.TRUE_P, "dapo": C.BITS, "gspo": C.ATTN, "dpo": C.SURPRISE}


def axes_box(x_range, y_range, w, h, center):
    return CornerAxes(x_range=x_range, y_range=y_range, x_length=w, y_length=h, tips=False,
                      axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to(center)


class Objective(VoiceoverScene):
    def construct(self):
        self.card()
        self.clip()
        self.kl()
        self.learning()
        self.dpo()
        self.dpo_result()
        self.variants()
        self.signal()
        self.sharpen()

    def card(self):
        card = chapter_card(3, r"The objective, exactly", r"What do GRPO and its successors optimize?", lit=(2024, 2025), part=17)
        with self.voiceover("Chapter three. The objective, exactly."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def clip(self):
        o = load("objectives")
        colors = {r"\rho_{i,t}": RATIO, r"\hat A_i": ADV, r"\beta": KLC, r"\pi_\theta": POLICY, r"\pi_{\mathrm{old}}": GREY_B}
        J = cmath(r"J(\theta) = \frac{1}{G}\sum_{i=1}^{G} \frac{1}{|o_i|}\sum_{t}", r"\min\!\Big(", r"\rho_{i,t}", r"\hat A_i", r",\ ",
                  r"\operatorname{clip}(", r"\rho_{i,t}", r",\, 1-\varepsilon,\, 1+\varepsilon)", r"\hat A_i", r"\Big)", r"-", r"\beta",
                  r"\, D_{\mathrm{KL}}(\pi_\theta \,\|\, \pi_{\mathrm{ref}})", colors=colors, font_size=34).to_edge(UP, buff=0.45)
        rho = cmath(r"\rho_{i,t}", r"=", r"\frac{\pi_\theta(o_{i,t} \mid q,\, o_{i,<t})}{\pi_{\mathrm{old}}(o_{i,t} \mid q,\, o_{i,<t})}",
                    colors={r"\rho_{i,t}": RATIO}, font_size=32).next_to(J, DOWN, buff=0.35).shift(LEFT * 3.0)
        rl = label(r"how much likelier the token is now \\ than when the answer was sampled", font_size=20, color=RATIO).next_to(rho, DOWN, buff=0.12)
        ahat = cmath(r"\hat A_i", r"= \frac{r_i - \operatorname{mean}(r)}{\operatorname{std}(r)}", colors={r"\hat A_i": ADV},
                     font_size=32).next_to(J, DOWN, buff=0.35).shift(RIGHT * 3.4)
        al = label(r"the group's own baseline \ (chapter two)", font_size=20, color=ADV).next_to(ahat, DOWN, buff=0.12)
        eps = 0.2
        plots = VGroup()
        for k, (sgn, title) in enumerate(((1, r"a good answer: \ $\hat A > 0$"), (-1, r"a bad answer: \ $\hat A < 0$"))):
            ax = axes_box([0, 2, 0.5], [-2, 2, 1], 4.4, 2.4, [-3.4 + 6.8 * k, -2.0, 0])
            f = ax.plot(lambda r_: min(r_ * sgn, min(max(r_, 1 - eps), 1 + eps) * sgn), x_range=[0.02, 2.0, 0.01],
                        color=RIGHT_C if sgn > 0 else WRONG_C, stroke_width=4)
            raw = DashedLine(ax.c2p(0, 0), ax.c2p(2, 2 * sgn), dash_length=0.06, stroke_width=1.5, color=GREY_B)
            band = Rectangle(width=ax.c2p(1 + eps, 0)[0] - ax.c2p(1 - eps, 0)[0], height=2.4, stroke_width=0,
                             fill_color=RATIO, fill_opacity=0.12).move_to(ax.c2p(1, 0))
            zero = DashedLine(ax.c2p(0, 0), ax.c2p(2, 0), dash_length=0.05, stroke_width=1, color=GREY_D)
            ticks = VGroup(*[MathTex(t_, font_size=20, color=GREY_B).next_to(ax.c2p(v, -2), DOWN, buff=0.08)
                             for v, t_ in ((1 - eps, r"0.8"), (1, r"1"), (1 + eps, r"1.2"))])
            tl = label(title, font_size=22, color=RIGHT_C if sgn > 0 else WRONG_C).next_to(ax, UP, buff=0.1)
            xl = MathTex(r"\rho", font_size=26, color=RATIO).next_to(ax.c2p(2, -2), RIGHT, buff=0.1)
            plots.add(VGroup(ax, band, zero, raw, f, ticks, tl, xl))
        stop = label(r"outside the band: \\ no more push", font_size=20, color=RATIO).move_to([0, -2.0, 0])
        clip_g = 100 * float(np.nanmean(np.asarray(o["grpo_clipped"])))
        cite_ = cite(r"J.~Schulman et al., \textit{PPO} (2017); \ Z.~Shao et al., \textit{DeepSeekMath} (2024)", corner=DR)
        with self.voiceover(
            "Chapter two's recipe was the simplest version. Here is the objective GRPO actually optimizes, as "
            "DeepSeek published it. <bookmark mark='a'/> Each token of each answer gets a ratio: how much likelier "
            "the model now makes it than when the answer was sampled. <bookmark mark='b'/> The advantage is chapter "
            "two's: reward against the group. <bookmark mark='c'/> Then the clip. Samples are expensive, so each "
            "batch is used for several updates, and the clip keeps those updates from running away. "
            "<bookmark mark='d'/> For a good answer, the objective grows with the ratio, until the token is twenty "
            "percent likelier than it was; then it goes flat, and there's nothing more to gain. For a bad answer, "
            "it stops rewarding the push down once the token is twenty percent less likely. <bookmark mark='e'/> "
            f"In our run, with four updates per batch, the clip held back {clip_g:.0f} percent of the tokens. "
            "And the last term keeps the model near where it started."
        ) as vo:
            self.play(FadeIn(cite_), Write(J), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(rho), FadeIn(rl), Indicate(J[2], color=RATIO), Indicate(J[6], color=RATIO))
            vo.wait_until("b")
            self.play(FadeIn(ahat), FadeIn(al), Indicate(J[3], color=ADV), Indicate(J[8], color=ADV))
            vo.wait_until("c")
            self.play(Circumscribe(VGroup(*J[1:10]), color=RATIO))
            vo.wait_until("d")
            for p in plots:
                self.play(Create(p[0]), FadeIn(p[1]), FadeIn(p[2]), Create(p[3]), FadeIn(p[5]), FadeIn(p[6]), FadeIn(p[7]))
                self.play(Create(p[4]), run_time=1.5)
            self.play(FadeIn(stop))
            vo.wait_until("e")
            self.play(Indicate(VGroup(*J[10:]), color=KLC))
        self.wait(0.3)
        self.next_section_objects = (J,)
        self.play(*[FadeOut(m_) for m_ in self.mobjects if m_ is not J])

    # ------------------------------------------------------------------
    def kl(self):
        o = load("objectives")
        (J,) = self.next_section_objects
        k3 = cmath(r"k_3", r"=", r"\frac{\pi_{\mathrm{ref}}}{\pi_\theta}", r"-", r"\log \frac{\pi_{\mathrm{ref}}}{\pi_\theta}", r"- 1",
                   colors={r"k_3": KLC}, font_size=36).move_to([-3.3, 1.5, 0])
        kl1 = label(r"never negative; \ zero only where nothing moved; \\ on average, exactly the KL", font_size=22,
                    color=GREY_A).next_to(k3, DOWN, buff=0.25)
        ax = axes_box([0, 3, 1], [0, 2, 1], 4.4, 2.4, [-3.3, -1.7, 0])
        fk = ax.plot(lambda x: x - math.log(x) - 1, x_range=[0.12, 3.0, 0.01], color=KLC, stroke_width=4)
        xl = MathTex(r"\pi_{\mathrm{ref}} / \pi_\theta", font_size=24, color=GREY_B).next_to(ax.c2p(3, 0), DOWN, buff=0.15)
        one = MathTex("1", font_size=22, color=GREY_B).next_to(ax.c2p(1, 0), DOWN, buff=0.1)
        # KL from the start over training: with the penalty, and without
        cg, cp = np.asarray(o["grpo_curve"]), np.asarray(o["pg_curve"])
        top = max(float(cg[:, 3].max()), float(cp[:, 3].max()))
        top = math.ceil(top * 2) / 2
        steps = int(o["steps"])
        bx = axes_box([0, steps, 100], [0, top, 0.5], 5.2, 3.2, [3.5, -0.6, 0])
        yt = VGroup(*[MathTex(f"{v:g}", font_size=20, color=GREY_B).next_to(bx.c2p(0, v), LEFT, buff=0.08) for v in (0, top / 2, top)])
        xt = VGroup(*[MathTex(f"{v}", font_size=20, color=GREY_B).next_to(bx.c2p(v, 0), DOWN, buff=0.08) for v in (0, steps)])
        yn = label(r"how far from the start: \ KL, \ bits per answer", font_size=20, color=GREY_A).next_to(bx, UP, buff=0.12)
        xn = label(r"RL steps", font_size=20, color=GREY_A).next_to(xt, DOWN, buff=0.05)
        lg, lp_ = curve(bx, cg[:, 0], cg[:, 3], CHAIN, 3.5), curve(bx, cp[:, 0], cp[:, 3], GREY_B, 3.5)
        kg = label(r"GRPO, \ $\beta = 0.04$", font_size=20, color=CHAIN).next_to(bx.c2p(steps, float(cg[-1, 3])), RIGHT, buff=0.1)
        kp = label(r"no penalty", font_size=20, color=GREY_B).next_to(bx.c2p(steps, float(cp[-1, 3])), RIGHT, buff=0.1)
        if abs(kg.get_y() - kp.get_y()) < 0.3:
            (kg if cg[-1, 3] > cp[-1, 3] else kp).shift(UP * 0.18)
            (kp if cg[-1, 3] > cp[-1, 3] else kg).shift(DOWN * 0.18)
        cite_ = cite(r"J.~Schulman, \textit{Approximating KL Divergence} (2020)", corner=DR)
        less = cg[-1, 3] < cp[-1, 3]
        with self.voiceover(
            "That last term needs the KL divergence, part three's measure of how far one distribution is from "
            "another, and computing it exactly would mean summing over every possible answer. <bookmark mark='a'/> "
            "Instead, GRPO uses an estimate from the sampled tokens alone, John Schulman's k three: the ratio of the "
            "starting model's probability to the current one's, minus its log, minus one. <bookmark mark='b'/> It's "
            "never negative, it's zero only when nothing has moved, and on average it equals the KL exactly. "
            "<bookmark mark='c'/> In our runs, "
            + (f"the penalty kept GRPO closer to where it started: {float(cg[-1, 3]):.2f} bits per answer, against "
               f"{float(cp[-1, 3]):.2f} without it." if less else
               f"the penalty, at weight 0.04, barely held GRPO back: {float(cg[-1, 3]):.2f} bits per answer from "
               f"the start, against {float(cp[-1, 3]):.2f} for the plain gradient. Many recent recipes drop it.")
        ) as vo:
            self.play(J.animate.scale(0.75).to_edge(UP, buff=0.3), FadeIn(cite_))
            self.play(Indicate(VGroup(*J[11:]), color=KLC))
            vo.wait_until("a")
            self.play(Write(k3))
            vo.wait_until("b")
            self.play(FadeIn(kl1), Create(ax), FadeIn(xl), FadeIn(one))
            self.play(Create(fk), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(bx), FadeIn(yt), FadeIn(xt), FadeIn(yn), FadeIn(xn))
            self.play(Create(lp_), Create(lg), FadeIn(kg), FadeIn(kp), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dpo(self):
        o = load("objectives")
        colors = {r"\pi^*": POLICY, r"\pi_{\mathrm{ref}}": GREY_B, r"\beta": KLC, r"r(y)": ADV, r"y_w": RIGHT_C, r"y_l": WRONG_C,
                  r"\pi_\theta": POLICY}
        steps_ = VGroup(
            cmath(r"\max_{\pi}\ \mathbb{E}_{y\sim\pi}\big[", r"r(y)", r"\big] - ", r"\beta", r"\, D_{\mathrm{KL}}(\pi \,\|\, ",
                  r"\pi_{\mathrm{ref}}", r")", colors=colors, font_size=32),
            cmath(r"\pi^*", r"(y) = \frac{1}{Z}\,", r"\pi_{\mathrm{ref}}", r"(y)\, e^{", r"r(y)", r"/", r"\beta", r"}",
                  colors=colors, font_size=32),
            cmath(r"r(y)", r"=", r"\beta", r"\log \frac{", r"\pi^*", r"(y)}{", r"\pi_{\mathrm{ref}}", r"(y)} + ", r"\beta",
                  r"\log Z", colors=colors, font_size=32),
            cmath(r"P(", r"y_w", r"\succ", r"y_l", r") = \sigma\big(r(y_w) - r(y_l)\big)", colors=colors, font_size=32),
            cmath(r"\mathcal{L}_{\mathrm{DPO}} = -\log \sigma\Big(", r"\beta", r"\log \frac{\pi_\theta(", r"y_w", r")}{\pi_{\mathrm{ref}}(",
                  r"y_w", r")} - ", r"\beta", r"\log \frac{\pi_\theta(", r"y_l", r")}{\pi_{\mathrm{ref}}(", r"y_l", r")}\Big)",
                  colors=colors, font_size=32),
        ).arrange(DOWN, buff=0.42, aligned_edge=LEFT).move_to([-1.6, -0.15, 0])
        notes = VGroup(
            label(r"the goal: \ reward, \ but stay near the start", font_size=20, color=GREY_A),
            label(r"its exact solution", font_size=20, color=GREY_A),
            label(r"so the reward is hidden \\ in the best model itself", font_size=20, color=GREY_A),
            label(r"people pick between pairs \ (Bradley \& Terry): \\ $Z$ cancels", font_size=20, color=GREY_A),
            label(r"no reward model, \ no sampling: \\ just pairs, \ right and wrong", font_size=20, color=C.SURPRISE),
        )
        for n_, s_ in zip(notes, steps_):
            n_.next_to(s_, RIGHT, buff=0.5)
            n_.set_x(max(n_.get_x(), 3.6 + n_.width / 2 - 1.2))
            keep_in_frame(n_)
        arrows = VGroup(*[MathTex(r"\Downarrow", font_size=26, color=GREY_C).move_to((a.get_bottom() + b.get_top()) / 2).set_x(-6.4)
                          for a, b in zip(steps_, steps_[1:])])
        cite_ = cite(r"R.~Rafailov et al., \textit{Direct Preference Optimization} (2023)", corner=UR)
        with self.voiceover(
            "Before the variants, one more objective, because it explains what that KL term is really doing. "
            "<bookmark mark='a'/> Maximize reward while staying near the starting model. <bookmark mark='b'/> This "
            "has an exact solution: the starting model, reweighted by e to the reward over beta. <bookmark mark='c'/> "
            "Turn it around, and the reward is hidden in the best model itself: beta times the log of how much it "
            "raised each answer, plus a constant. <bookmark mark='d'/> Now suppose all we have is pairs: this answer "
            "is better than that one, with Bradley and Terry's model of preferences. The constant cancels. "
            "<bookmark mark='e'/> What's left is a plain loss on the model itself: push up the winner's log-ratio, "
            "push down the loser's. That's DPO, by Rafailov and colleagues: preference tuning with no reward model "
            "and no sampling during training."
        ) as vo:
            self.play(FadeIn(cite_))
            for i, mk in enumerate("abcde"):
                vo.wait_until(mk)
                self.play(*([FadeIn(arrows[i - 1])] if i else []), Write(steps_[i]), FadeIn(notes[i]), run_time=1.3)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dpo_result(self):
        o = load("objectives")
        cv = np.asarray(o["dpo_curve"])
        mv = np.asarray(o["dpo_moves"])
        acc0, acc = float(cv[0, 1]), float(cv[-1, 1])
        steps = int(o["steps"])
        lo = math.floor(min(mv[:, 1].min(), mv[:, 2].min()))
        hi = max(1, math.ceil(max(mv[:, 1].max(), mv[:, 2].max())))
        ax = CornerAxes(x_range=[0, steps, 100], y_range=[lo, hi, 1], x_length=5.6, y_length=3.6, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-2.8, -0.4, 0])
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(steps, 0), dash_length=0.06, stroke_width=1.5, color=GREY_B)
        yt = VGroup(*[MathTex(f"{v:+d}" if v else "0", font_size=20, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.08)
                      for v in range(lo, hi + 1)])
        xt = VGroup(*[MathTex(str(v), font_size=20, color=GREY_B).next_to(ax.c2p(v, lo), DOWN, buff=0.08) for v in (0, steps)])
        yn = label(r"change in $\log_2 p$, \ on pairs held out", font_size=20, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        xn = label(r"DPO steps", font_size=20, color=GREY_A).next_to(xt, DOWN, buff=0.05)
        cw = curve(ax, mv[:, 0], mv[:, 1], RIGHT_C, 3.5)
        cl = curve(ax, mv[:, 0], mv[:, 2], WRONG_C, 3.5)
        kw = label(r"the right answers \ (winners)", font_size=20, color=RIGHT_C).next_to(ax.c2p(steps, float(mv[-1, 1])), RIGHT, buff=0.1)
        kl_ = label(r"the wrong ones \ (losers)", font_size=20, color=WRONG_C).next_to(ax.c2p(steps, float(mv[-1, 2])), RIGHT, buff=0.1)
        if abs(kw.get_y() - kl_.get_y()) < 0.6:
            (kw if mv[-1, 1] > mv[-1, 2] else kl_).shift(UP * 0.3)
            (kl_ if mv[-1, 1] > mv[-1, 2] else kw).shift(DOWN * 0.3)
        res = label(rf"${int(o['dpo_n_pairs']):,}$ pairs from the starting model: \\ right on new questions \ "
                    rf"${100 * acc0:.0f}\% \to {100 * acc:.0f}\%$".replace(",", "{,}"), font_size=22, color=C.SURPRISE).move_to([4.2, 2.3, 0])
        both_down = mv[-1, 1] < -0.1 and mv[-1, 2] < mv[-1, 1]
        cite_ = cite(r"N.~Razin et al., \textit{Unintentional Unalignment: Likelihood Displacement in DPO} (2024)", corner=DR)
        with self.voiceover(
            "We tried it on our addition, with pairs of one right and one wrong answer, drawn once from the starting "
            "model. <bookmark mark='a'/> "
            + (f"It got worse: from {100 * acc0:.0f} to {100 * acc:.0f} percent right. " if acc < acc0 - 0.02 else
               f"It went from {100 * acc0:.0f} to {100 * acc:.0f} percent right. ")
            + "<bookmark mark='b'/> Watch the two log-probabilities on pairs it never trained on. "
            + ("The loss only asks the winner to rise relative to the loser, and the easiest way there was to push "
               "both down, the loser faster. The probability went somewhere, mostly to other wrong answers. This is "
               "known as likelihood displacement. " if both_down else
               "The winners rise and the losers fall, as the loss asks. ")
            + "Offline pairs from a weak model teach less than they seem to; the on-policy methods, which keep "
            "sampling from the model they're improving, kept getting better."
        ) as vo:
            self.play(FadeIn(cite_), FadeIn(res))
            vo.wait_until("a")
            self.play(Create(ax), Create(zero), FadeIn(yt), FadeIn(xt), FadeIn(yn), FadeIn(xn))
            vo.wait_until("b")
            self.play(Create(cw), Create(cl), FadeIn(kw), FadeIn(kl_), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def variants(self):
        o = load("objectives")
        V = [v for v in o["variants"]]
        rows = [
            ("grpo", r"GRPO \ (DeepSeekMath, 2024)", r"\hat A = \frac{r - \bar r}{\operatorname{std}(r)},\ \ \operatorname{clip}(\rho, 0.8, 1.2),\ \ \beta\,\mathrm{KL}",
             r"as above"),
            ("dr", r"Dr.~GRPO \ (2025)", r"\hat A = r - \bar r, \quad \textstyle\sum_t \text{ not } \frac{1}{|o_i|}\sum_t",
             r"no bias toward easy questions \\ or long wrong answers"),
            ("dapo", r"DAPO \ (2025)", r"\operatorname{clip}(\rho,\ 1 - 0.2,\ 1 + 0.28)", r"clip higher; \ drop groups \\ with no signal"),
            ("gspo", r"GSPO \ (Qwen3, 2025)", r"s_i = \Big(\frac{\pi_\theta(o_i)}{\pi_{\mathrm{old}}(o_i)}\Big)^{1/|o_i|}",
             r"one ratio per answer, \\ clipped as a whole"),
            ("dpo", r"DPO \ (2023)", r"-\log\sigma\big(\beta\,\Delta \log\text{-ratio}\big)", r"offline pairs"),
        ]
        tab = VGroup()
        for i, (k, name, eq, note_) in enumerate(rows):
            y = 2.65 - i * 0.82
            tab.add(VGroup(label(name, font_size=22, color=COLS[k]).move_to([-6.6, y, 0], aligned_edge=LEFT),
                           MathTex(eq, font_size=26).move_to([-3.0, y, 0], aligned_edge=LEFT),
                           label(note_, font_size=18, color=GREY_A).move_to([3.4, y, 0], aligned_edge=LEFT)))
        # results: accuracy after 300 steps, and the entropy of the digits
        acc = {v: float(np.asarray(o[f"{v}_curve"])[-1, 1]) for v in V}
        acc0 = float(np.asarray(o["pg_curve"])[0, 1])
        bw = 0.62
        base_y, Hh = -3.25, 2.0
        bars = VGroup()
        for j, v in enumerate(V):
            h = Hh * acc[v]
            x = -3.6 + j * (bw + 0.55)
            b = Rectangle(width=bw, height=h, stroke_width=0, fill_color=COLS[v], fill_opacity=0.85).move_to([x, base_y + h / 2, 0])
            bars.add(VGroup(b, MathTex(rf"{100 * acc[v]:.0f}\%", font_size=20, color=COLS[v]).next_to(b, UP, buff=0.05),
                            label(NAMES[v], font_size=16, color=COLS[v]).next_to(b, DOWN, buff=0.06)))
        start = DashedLine([-4.1, base_y + Hh * acc0, 0], [-3.6 + (len(V) - 1) * (bw + 0.55) + 0.5, base_y + Hh * acc0, 0],
                           dash_length=0.06, stroke_width=1.5, color=GREY_B)
        sl = label(rf"start: \ ${100 * acc0:.0f}\%$", font_size=18, color=GREY_B).next_to(start, RIGHT, buff=0.1)
        bl = label(r"right after $300$ steps: \\ same start, \\ same questions", font_size=20, color=GREY_A) \
            .move_to([-6.6, base_y + Hh / 2, 0], aligned_edge=LEFT)
        rl = [v for v in V if v != "dpo"]
        best = max(rl, key=lambda v: acc[v])
        spread = 100 * (max(acc[v] for v in rl) - min(acc[v] for v in rl))
        cite_ = cite(r"Z.~Liu et al., \textit{Dr.~GRPO} (2025); \ Q.~Yu et al., \textit{DAPO} (2025); \ C.~Zheng et al., "
                     r"\textit{GSPO} (2025)", corner=UR)  # the bars' names sit along the bottom
        with self.voiceover(
            "Since DeepSeek-R1, a small industry has tuned this objective. <bookmark mark='a'/> Doctor GRPO drops two "
            "normalizations: dividing by the group's spread overweights questions that are nearly always right or "
            "nearly always wrong, and dividing by an answer's length lets long wrong answers off lightly. "
            "<bookmark mark='b'/> DAPO, from ByteDance, lets the clip go higher above than below, so unlikely good "
            "tokens can grow, and throws away groups that carry no signal. <bookmark mark='c'/> GSPO, used for "
            "Qwen3, takes one ratio per answer instead of per token: the geometric mean of its tokens' ratios. "
            "<bookmark mark='d'/> We ran all of them, and DPO, from the same start on the same questions. "
            f"<bookmark mark='e'/> The best here is {SAY[best]}, at {100 * acc[best]:.0f} percent; "
            + (f"the reinforcement learners are within {spread:.0f} points of each other. On a problem this small "
               "they mostly agree; the differences matter at scale, over long answers and thousands of steps. "
               if spread < 10 else
               f"the reinforcement learners span {spread:.0f} points, from the same start. ")
            + f"DPO, as we saw, ends at {100 * acc['dpo']:.0f}."
        ) as vo:
            self.play(FadeIn(cite_), FadeIn(tab[0]))
            for i, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(tab[i + 1], shift=RIGHT * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(tab[4], shift=RIGHT * 0.2), Create(start), FadeIn(sl), FadeIn(bl))
            vo.wait_until("e")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b_[0], DOWN), FadeIn(b_[1]), FadeIn(b_[2])) for b_ in bars],
                                  lag_ratio=0.15), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def signal(self):
        o = load("objectives")
        steps = int(o["steps"])
        z = np.asarray(o["pg_zero"], float)
        w = 20
        zs = np.array([z[max(0, i - w + 1):i + 1].mean() for i in range(len(z))])
        ax = axes_box([0, steps, 100], [0, 1, 0.25], 6.0, 3.6, [-2.6, -0.5, 0])
        yt = VGroup(*[MathTex(rf"{int(100 * v)}\%", font_size=20, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.08) for v in (0, 0.5, 1)])
        xt = VGroup(*[MathTex(f"{v}", font_size=20, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.08) for v in (0, steps)])
        yn = label(r"groups whose $8$ answers are all right \ (or all wrong): \ no signal", font_size=20, color=GREY_A) \
            .next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        xn = label(r"RL steps \ (plain policy gradient; \ average of $20$)", font_size=20, color=GREY_A).next_to(xt, DOWN, buff=0.05)
        ln = curve(ax, np.arange(1, len(zs) + 1), zs, WRONG_C, 3.5)
        dr = np.asarray(o.get("dapo_drawn", []), float)
        extra = float(dr.mean() / int(o["Q"])) if len(dr) else float("nan")
        eq = MathTex(r"\hat A_i = 0 \ \text{ for every } i \ \Rightarrow\ \nabla J = 0", font_size=32).move_to([3.9, 1.6, 0])
        dl = label(rf"DAPO draws more questions \\ until each batch is full of signal: \\ "
                   rf"${extra:.2f}\times$ the questions, \ on average", font_size=22, color=C.BITS).move_to([3.9, 0.0, 0])
        with self.voiceover(
            "One of DAPO's fixes is worth seeing. When all eight answers to a question are right, every advantage "
            "is zero, and so is the gradient: the question was wasted. <bookmark mark='a'/> As the model improves, "
            f"that happens more and more: by the end of our run, {100 * zs[-1]:.0f} percent of the groups taught "
            "it nothing. <bookmark mark='b'/> DAPO keeps sampling questions until each batch is full of groups that "
            f"disagree. Here that cost {extra:.2f} times as many questions per step."
        ) as vo:
            self.play(Create(ax), FadeIn(yt), FadeIn(xt), FadeIn(yn), FadeIn(xn), Write(eq))
            vo.wait_until("a")
            self.play(Create(ln), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(dl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sharpen(self):
        o = load("objectives")
        steps = int(o["steps"])
        V = [v for v in o["variants"]]
        # left: the entropy of the model's digits as RL goes on
        top = max(float(np.asarray(o[f"{v}_curve"])[:, 2].max()) for v in V)
        top = math.ceil(top * 4) / 4
        ax = axes_box([0, steps, 100], [0, top, top / 2], 4.8, 3.2, [-3.6, -0.6, 0])
        yt = VGroup(*[MathTex(f"{v:g}", font_size=20, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.08) for v in (0, top / 2, top)])
        xt = VGroup(*[MathTex(f"{v}", font_size=20, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.08) for v in (0, steps)])
        yn = label(r"entropy of each digit, \ bits", font_size=20, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        xn = label(r"RL steps", font_size=20, color=GREY_A).next_to(xt, DOWN, buff=0.05)
        lines = VGroup(*[curve(ax, np.asarray(o[f"{v}_curve"])[:, 0], np.asarray(o[f"{v}_curve"])[:, 2], COLS[v], 2.5) for v in V])
        e0 = float(np.asarray(o["pg_curve"])[0, 2])
        e1 = float(np.mean([np.asarray(o[f"{v}_curve"])[-1, 2] for v in V]))
        # right: pass@k before and after RL
        ks = [int(k) for k in o["ks"]]
        pb, pa = np.asarray(o["passk_base"]), np.asarray(o["passk_grpo"])
        bx = axes_box([0, math.log2(ks[-1]), 1], [0, 1, 0.25], 4.8, 3.2, [3.4, -0.6, 0])
        bxt = VGroup(*[MathTex(f"{k}", font_size=20, color=GREY_B).next_to(bx.c2p(math.log2(k), 0), DOWN, buff=0.08) for k in ks])
        byt = VGroup(*[MathTex(rf"{int(100 * v)}\%", font_size=20, color=GREY_B).next_to(bx.c2p(0, v), LEFT, buff=0.08) for v in (0, 0.5, 1)])
        byn = label(r"pass@$k$: \ any of $k$ tries right", font_size=20, color=GREY_A).next_to(bx, UP, buff=0.15).align_to(bx, LEFT)
        bxn = label(r"tries, \ $k$", font_size=20, color=GREY_A).next_to(bxt, DOWN, buff=0.05)
        lk = np.log2(ks)
        cb, ca = curve(bx, lk, pb, GREY_B, 3.5), curve(bx, lk, pa, CHAIN, 3.5)
        db = VGroup(*[Dot(bx.c2p(x, y), radius=0.045, color=GREY_B) for x, y in zip(lk, pb)])
        da = VGroup(*[Dot(bx.c2p(x, y), radius=0.045, color=CHAIN) for x, y in zip(lk, pa)])
        kb = label(r"before RL", font_size=20, color=GREY_B)
        ka = label(r"after GRPO", font_size=20, color=CHAIN)
        VGroup(ka, kb).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(bx.c2p(math.log2(ks[-1]) * 0.62, 0.22))
        # a real crossover: the model before RL clearly ahead at the most tries
        cross = [k for k, a, b in zip(ks, pa, pb) if b > a + 0.01] if pb[-1] > pa[-1] + 0.02 else []
        cite_ = cite(r"Y.~Yue et al., \textit{Does Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs "
                     r"Beyond the Base Model?} (2025)", corner=DR)
        with self.voiceover(
            "Every one of these objectives does something else, too. <bookmark mark='a'/> It sharpens the model. The "
            f"entropy of its digits falls from {e0:.2f} bits to about {e1:.2f}: it stops considering alternatives. "
            "Too fast, and exploration dies; that's the entropy collapse that recent papers fight with the "
            "clip-higher trick and entropy bonuses. <bookmark mark='b'/> So does RL teach a model new answers, or "
            "just make it pick the ones it could already find? Yue and colleagues compared pass at k before and "
            "after RL. <bookmark mark='c'/> "
            + (f"On ours, one try is much better after RL. But with {cross[0]} tries or more, the model before RL "
               f"wins: {100 * pb[-1]:.0f} percent at {ks[-1]} tries, against {100 * pa[-1]:.0f}. The same crossover "
               "they found: RL concentrates probability on answers the model already had, and loses some of the rest."
               if cross else
               f"On ours, RL lifts one try from {100 * pb[0]:.0f} to {100 * pa[0]:.0f} percent, but with enough tries "
               f"the two meet: both reach about {100 * pa[-1]:.0f} percent at {ks[-1]}. "
               "A problem this small has no answers the model can't find by chance; on hard problems, Yue and "
               "colleagues found that with enough tries the model before RL wins. RL mostly concentrates probability "
               "on answers the model already had.")
        ) as vo:
            self.play(Create(ax), FadeIn(yt), FadeIn(xt), FadeIn(yn), FadeIn(xn))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.15), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(cite_), Create(bx), FadeIn(bxt), FadeIn(byt), FadeIn(byn), FadeIn(bxn))
            vo.wait_until("c")
            self.play(Create(cb), FadeIn(db), FadeIn(kb), run_time=1.5)
            self.play(Create(ca), FadeIn(da), FadeIn(ka), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def learning(self):
        """How GRPO moves the model: its probability over answers to three questions, step by step."""
        o = load("objectives")
        D = np.asarray(o["grpo_dists"], float)  # (checkpoints, 6 questions, 1000 answers)
        A, B = np.asarray(o["grpo_dist_a"]), np.asarray(o["grpo_dist_b"])
        truth = A + B
        n_ck = D.shape[0]
        steps = np.arange(n_ck) * 20
        p_right = D[:, np.arange(len(truth)), truth]
        order = np.argsort(p_right[0])  # the three questions it is least sure of at the start
        qs = [int(i) for i in order[:3]]
        panels, sets = VGroup(), []
        H = 2.4
        for j, qi in enumerate(qs):
            cand = set(np.argsort(-D[0, qi])[:5].tolist()) | set(np.argsort(-D[-1, qi])[:3].tolist()) | {int(truth[qi])}
            ans = sorted(cand, key=lambda a_: -D[0, qi, a_])[:7]
            if int(truth[qi]) not in ans:
                ans[-1] = int(truth[qi])
            sets.append(ans)
            x0 = -5.4 + j * 4.3
            base = Line([x0 - 0.3, -1.2, 0], [x0 + 0.48 * len(ans) - 0.1, -1.2, 0], color=GREY_C, stroke_width=1.5)
            labs = VGroup(*[Text(str(a_), font="DejaVu Sans Mono", font_size=16, color=RIGHT_C if a_ == truth[qi] else GREY_B)
                            .move_to([x0 + 0.48 * k, -1.45, 0]) for k, a_ in enumerate(ans)])
            q = Text(f"{int(A[qi])}+{int(B[qi])}=", font="DejaVu Sans Mono", font_size=24, color=GREY_A).move_to([x0 + 1.3, 1.9, 0])
            panels.add(VGroup(base, labs, q))

        def bars(k):
            g = VGroup()
            for j, qi in enumerate(qs):
                x0 = -5.4 + j * 4.3
                for kk, a_ in enumerate(sets[j]):
                    h = max(H * float(D[k, qi, a_]), 0.01)
                    g.add(Rectangle(width=0.36, height=h, stroke_width=0, fill_color=RIGHT_C if a_ == truth[qi] else WRONG_C,
                                    fill_opacity=0.85).move_to([x0 + 0.48 * kk, -1.2 + h / 2, 0]))
            return g

        cur = bars(0)
        t = ValueTracker(0)
        cnt = always_redraw(lambda: MathTex(rf"\text{{GRPO step }}{int(t.get_value())}", font_size=30, color=C.BITS).to_edge(UP, buff=0.4))
        yl = label(r"the model's probability for each answer \ (the right one in green)", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.4)
        e0, e1 = float(np.asarray(o["grpo_curve"])[0, 2]), float(np.asarray(o["grpo_curve"])[-1, 2])
        pr0 = float(p_right[0, qs].mean())
        pr1 = float(p_right[-1, qs].mean())
        # big single-checkpoint falls of a right answer on the way (learning from 8 samples a step is noisy)
        falls = int(sum((p_right[k, q_] < p_right[k - 1, q_] - 0.3) for k in range(1, n_ck) for q_ in qs))
        with self.voiceover(
            "Here is what that objective does to the model, step by step. Three questions it was unsure of, and the "
            "probability it gives each candidate answer, the right one in green. <bookmark mark='a'/> Each step, "
            "answers that beat their group's average get pushed up and the rest pushed down; the clip keeps each "
            f"push small. <bookmark mark='b'/> The right answers' probability climbs from {100 * pr0:.0f} percent on "
            f"average to {100 * pr1:.0f}, and the wrong ones drain away"
            + (". Not smoothly: each step learns from just eight sampled answers a question, so a right answer can "
               "drop sharply and be pulled back later" if falls >= 2 else "")
            + f". That's also why the entropy falls, from "
            f"{e0:.2f} to {e1:.2f} bits a digit: the model stops spreading its bets."
        ) as vo:
            self.play(FadeIn(panels), FadeIn(cur), FadeIn(yl))
            self.add(cnt)
            vo.wait_until("a")
            for k in range(1, n_ck):
                if k == n_ck // 2:
                    vo.wait_until("b")
                nxt = bars(k)
                self.play(Transform(cur, nxt), t.animate.set_value(steps[k]), run_time=0.45, rate_func=linear)
        self.wait(0.5)
        self.remove(cnt)
        self.clear_scene()
