from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.frontier.common import Mono, Plot, calc, label, load, note, num_table, schematic_tag, smooth, source


class RL(VoiceoverScene):
    def construct(self):
        self.d = load("toy_rl")
        self.verifiable()
        self.setup_toy()
        self.group()
        self.adv_math()
        self.clip_math()
        self.curve()
        self.passk_math()
        self.r1()
        self.agentic()
        self.hacking()

    # ------------------------------------------------------------------
    def verifiable(self):
        rows = VGroup(
            VGroup(label(r"math problem", font_size=30), MathTex(r"\rightarrow", font_size=36),
                   label(r"compare the final answer", font_size=30)),
            VGroup(label(r"coding task", font_size=30), MathTex(r"\rightarrow", font_size=36),
                   label(r"run the unit tests", font_size=30)),
        )
        for r in rows:
            r.arrange(RIGHT, buff=0.4)
        rows.arrange(DOWN, buff=0.5).move_to(UP * 0.3)
        rew = MathTex(r"\text{reward} = \begin{cases} 1 & \text{correct} \\ 0 & \text{otherwise}\end{cases}",
                      font_size=40, color=C.REWARD).next_to(rows, DOWN, buff=0.7)
        head = label(r"Reinforcement learning with verifiable rewards", font_size=38).to_edge(UP, buff=0.5)
        with self.voiceover(
            "The biggest change in post-training since 2024 is reinforcement learning on problems whose answers can "
            "be checked automatically. <bookmark mark='m'/> A math problem has a final answer; <bookmark mark='c'/> "
            "code has tests. <bookmark mark='r'/> The reward is simply one if the answer is right, and zero if it "
            "isn't. There's no learned reward model for the policy to fool."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("m")
            self.play(FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(rows[1], shift=RIGHT * 0.2))
            vo.wait_until("r")
            self.play(FadeIn(rew))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def setup_toy(self):
        d = self.d
        a, b = d["show"]
        right, wrong = a + b, d["no_carry_answer"]
        assert (right, wrong) == (834, 724) and abs(d["carry_drop"] - 0.4) < 1e-9
        ex = VGroup(
            VGroup(Mono("347+285=0632", font_size=30), label(r"60\%: correct", font_size=26, color=C.REWARD)).arrange(RIGHT, buff=0.5),
            VGroup(Mono("347+285=0522", font_size=30), label(r"40\%: every carry forgotten", font_size=26, color=C.PENALTY)).arrange(RIGHT, buff=0.5),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(UP * 0.2)
        assert 347 + 285 == 632
        head = label(r"A real miniature: a pocket model that learned sloppy arithmetic", font_size=34).to_edge(UP, buff=0.5)
        sub = label(rf"3 layers, {d['params']:,} parameters, pretrained on 384{{,}}000 three-digit additions".replace(",", "{,}", 1),
                    font_size=24, color=GREY_A).next_to(head, DOWN, buff=0.2)
        with self.voiceover(
            "Here's the most popular algorithm for this, GRPO, run for real on a miniature. We pretrained a pocket "
            "model on three-digit additions, <bookmark mark='w'/> where four in ten of the examples were written by "
            "someone who always forgets to carry. So the model learned two habits: the right answer, and the "
            "carry-dropping mistake."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub))
            self.play(FadeIn(ex[0]))
            vo.wait_until("w")
            self.play(FadeIn(ex[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def group(self):
        d = self.d
        a, b = d["show"]
        g0 = d["groups"][0]
        ans = g0["answers"]
        G = len(ans)
        r = np.array([1.0 if x == a + b else 0.0 for x in ans])
        assert r.sum() == 2 and ans.count(724) == 4 and ans.count(824) == 1, ans  # as narrated
        mean, std = r.mean(), r.std(ddof=1)
        adv = (r - mean) / (std + 1e-4)
        prompt = Mono(f"{a}+{b}=", font_size=34).to_edge(UP, buff=0.5).shift(LEFT * 3.5)
        plab = label(r"one prompt, a group of 8 sampled answers", font_size=26, color=GREY_A).next_to(prompt, RIGHT, buff=0.5)
        rows = VGroup()
        for i, x in enumerate(ans):
            s = f"{x:04d}" if x >= 0 else "????"
            t = Mono(s, font_size=30, color=C.REWARD if r[i] else C.PENALTY)
            mark = label(r"\checkmark" if r[i] else r"$\times$", font_size=30, color=C.REWARD if r[i] else C.PENALTY)
            rr = MathTex(rf"r={int(r[i])}", font_size=28)
            av = MathTex(rf"A={adv[i]:+.2f}", font_size=28, color=C.REWARD if adv[i] > 0 else C.PENALTY)
            bar = Rectangle(width=max(0.02, abs(adv[i]) * 1.4), height=0.3, stroke_width=0,
                            fill_color=C.REWARD if adv[i] > 0 else C.PENALTY, fill_opacity=0.85)
            rows.add(VGroup(t, mark, rr, av, bar))
        for i, row in enumerate(rows):
            y = 1.9 - i * 0.62
            row[0].move_to([-4.6, y, 0])
            row[1].move_to([-3.5, y, 0])
            row[2].move_to([-2.3, y, 0])
            row[3].move_to([-0.6, y, 0])
            x0 = 2.6
            if adv[i] >= 0:
                row[4].move_to([x0, y, 0], aligned_edge=LEFT)
            else:
                row[4].move_to([x0, y, 0], aligned_edge=RIGHT)
        axis = Line([2.6, 2.3, 0], [2.6, 1.9 - (G - 1) * 0.62 - 0.4, 0], color=GREY_C)
        formula = MathTex(r"A_i = \frac{r_i - \operatorname{mean}(r)}{\operatorname{std}(r)}", font_size=38).to_corner(DR, buff=0.6).shift(UP * 0.3)
        upd = label(r"every token of answer $i$: probability pushed up or down by $A_i$", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Give it a problem, 478 plus 356, and sample a group of eight answers. <bookmark mark='a'/> Two are "
            "right: 834. Four drop both carries, giving 724, and the other two make mistakes too. <bookmark mark='r'/> Each answer gets a "
            "reward: one or zero. "
            "<bookmark mark='g'/> GRPO's key idea is to grade each answer against its own group: subtract the "
            "group's average reward, and divide by the spread. Better than average gets a positive advantage; worse "
            "gets a negative one. <bookmark mark='u'/> Then every token of each answer is pushed up or down in "
            "probability according to its advantage. No critic network, no reward model: just a group of samples and "
            "a checker."
        ) as vo:
            self.play(FadeIn(prompt), FadeIn(plab))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(row[0], shift=RIGHT * 0.2) for row in rows], lag_ratio=0.1), run_time=1.2)
            self.play(LaggedStart(*[FadeIn(row[1]) for row in rows], lag_ratio=0.05))
            vo.wait_until("r")
            self.play(LaggedStart(*[FadeIn(row[2]) for row in rows], lag_ratio=0.05))
            vo.wait_until("g")
            self.play(FadeIn(formula))
            self.play(Create(axis), LaggedStart(*[AnimationGroup(FadeIn(row[3]), GrowFromEdge(row[4], LEFT if adv[i] >= 0 else RIGHT))
                                                  for i, row in enumerate(rows)], lag_ratio=0.08), run_time=1.6)
            vo.wait_until("u")
            self.play(FadeIn(upd))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def adv_math(self):
        d = self.d
        a, b = d["show"]
        r = np.array([1.0 if x == a + b else 0.0 for x in d["groups"][0]["answers"]])
        G = len(r)
        mean, std = r.mean(), r.std(ddof=1)  # torch's default (unbiased) std, as in the run
        adv = (r - mean) / (std + 1e-4)
        assert G == 8 and mean == 0.25 and round(std, 3) == 0.463 and abs(std ** 2 - 3 / 14) < 1e-12
        assert round(adv.max(), 2) == 1.62 and round(adv.min(), 2) == -0.54 and abs(adv.sum()) < 1e-9

        def adv_k(k):  # advantages of a right and a wrong answer when k of the 8 are right
            m, sd = k / G, np.sqrt(k * (G - k) / (G * (G - 1)))
            return (1 - m) / (sd + 1e-4), (0 - m) / (sd + 1e-4)
        tab_vals = {k: adv_k(k) for k in (1, 4, 7, 8)}
        assert [round(v, 2) for v in tab_vals[4]] == [0.94, -0.94] and [round(v, 2) for v in tab_vals[7]] == [0.35, -2.47]
        assert abs(tab_vals[8][0]) < 1e-9
        head = label(r"The advantages for $478 + 356$, worked out", font_size=34).to_edge(UP, buff=0.4)
        nums = calc(r"r &= (0, 0, 1, 0, 1, 0, 0, 0)",
                    r"\\ \operatorname{mean}(r) &= \tfrac{2}{8} = 0.25",
                    r"\\ \operatorname{std}(r) &= \sqrt{\tfrac{1}{7}\big[\,2 \times 0.75^2 + 6 \times 0.25^2\,\big]} = \sqrt{3/14} \approx 0.463",
                    r"\\ A_{834} &= \frac{1 - 0.25}{0.463} \approx +1.62",
                    r"\\ A_{\text{wrong}} &= \frac{0 - 0.25}{0.463} \approx -0.54",
                    r"\\ \textstyle\sum_i A_i &= 2 \times 1.62 - 6 \times 0.54 = 0", font_size=32)
        nums[3].set_color(C.REWARD)
        nums[4].set_color(C.PENALTY)
        nums.next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.6)

        def f(v):
            return "0" if abs(v) < 1e-9 else f"{v:+.2f}"
        tab = num_table([r"\text{right of } 8", r"A_{\text{right}}", r"A_{\text{wrong}}"],
                        [[str(k), f(v[0]), (f(v[1]) if k < G else r"\text{---}")] for k, v in tab_vals.items()],
                        font_size=32, col_colors=[WHITE, C.REWARD, C.PENALTY])
        tab.next_to(nums, RIGHT, buff=0.9).align_to(nums, UP).shift(DOWN * 0.3)
        VGroup(nums, tab).set_y(-0.35)
        hl = SurroundingRectangle(tab.rows[0], buff=0.1, color=C.HIGHLIGHT, corner_radius=0.08)
        tab.rows[3].set_color(GREY_B)
        none = label(r"no signal", font_size=24, color=GREY_B).next_to(tab.rows[3], DOWN, buff=0.15)
        with self.voiceover(
            "Here are those numbers, worked out. The rewards are two ones and six zeros, <bookmark mark='m'/> "
            "so the mean is two eighths: 0.25. <bookmark mark='s'/> The spread, the sample standard deviation, is the "
            "square root of three fourteenths: about 0.463. <bookmark mark='a'/> So each right answer gets 0.75 divided by 0.463: "
            "plus 1.62. <bookmark mark='b'/> Each wrong one gets minus 0.54. <bookmark mark='z'/> The advantages always "
            "sum to zero: probability pushed up in one place is pushed down somewhere else. <bookmark mark='t'/> And "
            "their size depends on how rare the outcome was. One success in eight earns plus 2.47; one failure in "
            "eight costs minus 2.47. <bookmark mark='n'/> And when all eight agree, the spread is zero, and so is "
            "every advantage."
        ) as vo:
            self.play(FadeIn(head), Write(nums[0]))
            vo.wait_until("m")
            self.play(Write(nums[1]))
            vo.wait_until("s")
            self.play(Write(nums[2]), run_time=1.5)
            vo.wait_until("a")
            self.play(Write(nums[3]))
            vo.wait_until("b")
            self.play(Write(nums[4]))
            vo.wait_until("z")
            self.play(Write(nums[5]))
            vo.wait_until("t")
            self.play(FadeIn(tab.header), Create(tab.rule), FadeIn(VGroup(*tab.rows[:3]), lag_ratio=0.2), Create(hl))
            vo.wait_until("n")
            self.play(FadeIn(tab.rows[3]), FadeIn(none))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def clip_math(self):
        eps = 0.2
        A_pos, A_neg = 1.62, -0.54  # the advantages just computed (rounded as shown)

        def obj(rho, A):
            return np.minimum(rho * A, np.clip(rho, 1 - eps, 1 + eps) * A)
        assert round(1.3 * A_pos, 2) == 2.11 and round(1.2 * A_pos, 2) == 1.94 and round(obj(1.3, A_pos), 2) == 1.94
        assert round(0.6 * A_neg, 2) == -0.32 and round(0.8 * A_neg, 2) == -0.43 and round(obj(0.6, A_neg), 2) == -0.43
        J = MathTex(r"J(\theta) = \frac{1}{G}\sum_{i=1}^{G} \frac{1}{|o_i|}\sum_{t}",
                    r"\min\!\Big(\rho_{i,t} A_i,\ \operatorname{clip}(\rho_{i,t},\, 1 - \varepsilon,\, 1 + \varepsilon)\, A_i\Big)",
                    r",\qquad \rho_{i,t} = \frac{\pi_\theta(o_{i,t} \mid \cdot)}{\pi_{\theta_{\text{old}}}(o_{i,t} \mid \cdot)}",
                    font_size=32).to_edge(UP, buff=0.4)
        J[1].set_color(C.HIGHLIGHT)
        sub = note(r"GRPO (Shao et al.\ 2024), PPO's clipped objective; $\varepsilon = 0.2$; KL term omitted, as in many recent recipes",
                   font_size=20).next_to(J, DOWN, buff=0.2)
        rs = np.linspace(0.4, 1.6, 121)
        plots = VGroup()
        for A, yr, yt in [(A_pos, (0, 4), [0, 1, 2, 3, 4]), (A_neg, (-0.9, 0), [-0.9, -0.6, -0.3, 0])]:
            pl = Plot(x_range=(0.4, 1.6), y_range=yr, width=3.6, height=2.0, x_ticks=[0.4, 0.8, 1.2, 1.6], y_ticks=yt,
                      x_label=r"$\rho$", y_label=rf"objective, $A = {A:+.2f}$", font_size=22)
            band = Rectangle(width=pl.c2p(1.2, 0)[0] - pl.c2p(0.8, 0)[0], height=2.0, stroke_width=0, fill_color=GREY_D, fill_opacity=0.35)
            band.move_to(pl.c2p(1.0, (yr[0] + yr[1]) / 2))
            plots.add(VGroup(band, pl))
        plots.arrange(RIGHT, buff=1.6).set_x(0).to_edge(DOWN, buff=0.45)
        lines = []  # unclipped (dashed) and clipped objective, built on the plots' final positions
        for (A, color), grp in zip([(A_pos, C.REWARD), (A_neg, C.PENALTY)], plots):
            pl = grp[1]
            lines.append((DashedLine(pl.c2p(0.4, 0.4 * A), pl.c2p(1.6, 1.6 * A), color=GREY_B, stroke_width=2),
                          pl.line(rs, obj(rs, A), color=color, stroke_width=4)))
        p1, p2 = plots[0][1], plots[1][1]
        d1 = Dot(p1.c2p(1.3, obj(1.3, A_pos)), radius=0.08, color=C.REWARD)
        d1u = Dot(p1.c2p(1.3, 1.3 * A_pos), radius=0.06, color=GREY_B)
        d2 = Dot(p2.c2p(0.6, obj(0.6, A_neg)), radius=0.08, color=C.PENALTY)
        d2u = Dot(p2.c2p(0.6, 0.6 * A_neg), radius=0.06, color=GREY_B)
        nums = calc(r"\rho = 1.3:\ \min(1.3 \times 1.62,\ 1.2 \times 1.62) &= \min(2.11,\ 1.94) = 1.94",
                    r"\\ \rho = 0.6:\ \min\big(0.6 \times (-0.54),\ 0.8 \times (-0.54)\big) &= \min(-0.32,\ -0.43) = -0.43",
                    font_size=28)
        nums[0].set_color(C.REWARD)
        nums[1].set_color(C.PENALTY)
        nums.next_to(sub, DOWN, buff=0.3)
        flat = MathTex(r"\text{clipped value is flat in } \theta \;\Rightarrow\; \text{zero gradient: this token has moved enough}",
                       font_size=28).next_to(nums, DOWN, buff=0.3)
        toy = MathTex(r"\text{our toy: one step per batch, so } \rho = 1 \;\Rightarrow\; \nabla J = A\, \nabla \log \pi_\theta",
                      font_size=28, color=GREY_A).next_to(flat, DOWN, buff=0.2)
        with self.voiceover(
            "GRPO's full objective adds one safeguard, borrowed from PPO. Rho is the ratio of a token's probability "
            "now to its probability when the answers were sampled, <bookmark mark='c'/> and it's clipped to within "
            "twenty percent of one. <bookmark mark='p'/> Take a token of the right answer, advantage plus 1.62, whose "
            "probability has already risen by thirty percent: rho is 1.3. Unclipped, the objective would be 2.11; "
            "clipped at 1.2 it's 1.94, and the minimum takes the clipped value. <bookmark mark='f'/> That value no "
            "longer depends on the weights, so its gradient is zero: this token has been pushed enough for this "
            "batch. <bookmark mark='n'/> Likewise a wrong answer's token already down to 0.6 of its old probability: "
            "the minimum is the clipped minus 0.43, and the push stops. <bookmark mark='t'/> In our toy, each batch "
            "is used for one step only, so rho is exactly one, and the gradient is simply the advantage times the "
            "gradient of the log-probability."
        ) as vo:
            self.play(Write(J), FadeIn(sub), run_time=2.0)
            self.play(FadeIn(plots), Create(lines[0][0]), Create(lines[1][0]))
            vo.wait_until("c")
            self.play(Create(lines[0][1]), Create(lines[1][1]), run_time=1.5)
            vo.wait_until("p")
            self.play(Write(nums[0]), FadeIn(d1u), FadeIn(d1, scale=2))
            vo.wait_until("f")
            self.play(FadeIn(flat))
            vo.wait_until("n")
            self.play(Write(nums[1]), FadeIn(d2u), FadeIn(d2, scale=2))
            vo.wait_until("t")
            self.play(FadeIn(toy))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curve(self):
        d = self.d
        c = d["curve"]
        steps = np.array([x["step"] for x in c], float)
        p1 = np.array([x["pass1"] for x in c])
        p8 = np.array([x["pass8"] for x in c])
        assert p1[0] < 0.75 and p1[-1] > 0.93 and p8[0] > 0.9 and abs(p8[-1] - p8[0]) < 0.1, (p1[0], p1[-1], p8[0], p8[-1])
        S = steps[-1]
        plot = Plot(x_range=(0, S), y_range=(0, 1), width=8.6, height=4.3, x_ticks=list(range(0, int(S) + 1, 20)),
                    y_ticks=[0, 0.25, 0.5, 0.75, 1], y_fmt=lambda v: MathTex(rf"{int(100 * v)}\%", font_size=24, color=GREY_A),
                    x_label=r"RL steps (32 prompts $\times$ 8 samples each)")
        plot.move_to(LEFT * 1.4 + DOWN * 0.3)
        l1 = plot.line(steps, p1, color=C.REWARD, stroke_width=4)
        l8 = plot.line(steps, p8, color=WHITE, stroke_width=3)
        t1 = label(r"pass@1: one sample is right", font_size=26, color=C.REWARD).next_to(plot.c2p(S * 0.35, p1[3]), DOWN, buff=0.4)
        t8 = label(r"pass@8: at least one of 8 is right", font_size=26).next_to(plot.c2p(S * 0.5, 1.0), UP, buff=0.12)
        head = label(r"The real learning curve (held-out problems)", font_size=34).to_edge(UP, buff=0.35)
        head.set_x(-1.4)
        zv = np.array(d["zero_var"])
        zl = plot.line(np.arange(len(zv)), smooth(zv, 9), color=GREY_B, stroke_width=2.5)
        zt = label(r"groups where all 8 agree: zero advantage, no signal", font_size=22, color=GREY_B)
        zt.next_to(plot.c2p(S * 0.5, smooth(zv, 9)[int(len(zv) * 0.5)]), RIGHT, buff=0.1).shift(DOWN * 0.45)
        assert zv[-10:].mean() > 0.5 and d["groups"][-1]["answers"] == [834] * 8
        side = VGroup(
            label(r"RL here made the model", font_size=26),
            label(r"\emph{reliable} at what it could", font_size=26),
            label(r"already sometimes do", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(plot, RIGHT, buff=0.35).shift(UP * 0.8)
        deb = label(r"at frontier scale: debated\\(Yue et al.\ 2025 vs.\ ProRL, 2025)", font_size=22, color=GREY_A)
        deb.next_to(side, DOWN, buff=0.35).align_to(side, LEFT)
        with self.voiceover(
            "Repeat that over thousands of problems. <bookmark mark='p1'/> Pass at one, the chance that a single "
            f"sample is right, climbs from about {100*p1[0]:.0f} percent to {100*p1[-1]:.0f} percent. <bookmark mark='p8'/> But look at "
            f"pass at eight, the chance that at least one of eight samples is right. It rises from {100*p8[0]:.0f} percent to a hundred: "
            "a much smaller gain. <bookmark mark='s'/> In this toy, most of the gain came from making the model "
            "reliable at answers it could already sometimes produce. <bookmark mark='d'/> Whether that also "
            "holds at the frontier is debated: a 2025 study found the same pattern in large models, while others "
            "find that prolonged RL discovers genuinely new strategies."
        ) as vo:
            self.play(FadeIn(head), FadeIn(plot))
            vo.wait_until("p1")
            self.play(Create(l1), FadeIn(t1), run_time=2.0)
            vo.wait_until("p8")
            self.play(Create(l8), FadeIn(t8), run_time=1.5)
            vo.wait_until("s")
            self.play(FadeIn(side))
            vo.wait_until("d")
            self.play(FadeIn(deb))
        with self.voiceover(
            "And notice what happens late in training: <bookmark mark='z'/> most groups are all correct, like our "
            "478 plus 356, which now gets eight out of eight. Every advantage is zero, and those groups teach nothing. "
            "Refinements like DAPO's dynamic sampling filter them out, alongside other tweaks to the clipping and to "
            "how the loss is averaged."
        ) as vo:
            vo.wait_until("z")
            self.play(Create(zl), FadeIn(zt), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def passk_math(self):
        d = self.d
        c0 = d["curve"][0]
        p1, p8 = c0["pass1"], c0["pass8"]
        assert round(p1, 2) == 0.56 and round(100 * p8, 1) == 92.2
        ideal = 1 - (1 - round(p1, 2)) ** 8
        hard = 1 - (6 / 8) ** 8
        assert round(100 * ideal, 2) == 99.86 and round(100 * hard) == 90
        assert d["groups"][0]["answers"].count(sum(d["show"])) == 2
        plot = Plot(x_range=(0, 1), y_range=(0, 1), width=4.4, height=4.6, x_ticks=[0, 0.25, 0.5, 0.75, 1],
                    y_ticks=[0, 0.25, 0.5, 0.75, 1], y_fmt=lambda v: MathTex(rf"{int(100 * v)}\%", font_size=22, color=GREY_A),
                    x_fmt=lambda v: f"{v:g}", x_label=r"$p$: chance one sample is right", font_size=22)
        plot.to_edge(LEFT, buff=0.9).set_y(-0.5)
        ps = np.linspace(0, 1, 200)
        l1 = plot.line(ps, ps, color=GREY_B, stroke_width=2.5)
        l8 = plot.line(ps, 1 - (1 - ps) ** 8, color=WHITE, stroke_width=4)
        t1 = label(r"pass@1 $= p$", font_size=22, color=GREY_B).next_to(plot.c2p(0.7, 0.7), DR, buff=0.05)
        t8 = label(r"pass@8", font_size=22).move_to(plot.c2p(0.42, 0.86))
        dh = Dot(plot.c2p(2 / 8, hard), radius=0.08, color=C.PENALTY)
        da = Dot(plot.c2p(0.56, ideal), radius=0.08, color=C.REWARD)
        head = label(r"Why pass@8 started near the ceiling", font_size=34).to_edge(UP, buff=0.4)
        nums = calc(r"P(\text{all } k \text{ wrong}) &= (1 - p)^k",
                    r"\\ \text{pass@}k &= 1 - (1 - p)^k",
                    r"\\ \text{average: } \bar p = 0.56 \;\Rightarrow\; \text{pass@}8 &= 1 - 0.44^8 \approx 99.86\%",
                    r"\\ \text{measured: } \text{pass@}8 &= 92.2\%",
                    r"\\ 478{+}356:\ \hat p = \tfrac{2}{8} \;\Rightarrow\; \text{pass@}8 &= 1 - \big(\tfrac{6}{8}\big)^8 \approx 90\%",
                    font_size=30)
        nums[2].set_color(C.REWARD)
        nums[4].set_color(C.PENALTY)
        nums.to_edge(RIGHT, buff=0.5).align_to(plot, UP).shift(DOWN * 0.4)
        assert nums.get_left()[0] > plot.get_right()[0] + 0.3, "pass@k: formulas collide with the plot"
        with self.voiceover(
            "Back to pass at eight: why did it barely move? If each sample is right with probability p, all k samples "
            "fail with probability one minus p, to the k. <bookmark mark='a'/> At the start, the average sample was "
            "right 56 percent of the time. If every problem were average, pass at eight would be one minus 0.44 to "
            "the eighth: 99.86 percent. <bookmark mark='m'/> The measured 92.2 is lower, because failures "
            "cluster on the hard problems, <bookmark mark='h'/> like 478 plus 356, where two samples in eight were "
            "right. There, pass at eight is one minus six eighths to the eighth: about 90 percent. <bookmark mark='r'/> "
            "RL raised p on exactly those problems, and pass at one followed. Pass at eight was already near its "
            "ceiling."
        ) as vo:
            self.play(FadeIn(head), FadeIn(plot), Write(nums[:2]))
            self.play(Create(l1), FadeIn(t1), Create(l8), FadeIn(t8), run_time=1.5)
            vo.wait_until("a")
            self.play(Write(nums[2]), FadeIn(da, scale=2))
            vo.wait_until("m")
            self.play(Write(nums[3]))
            vo.wait_until("h")
            self.play(Write(nums[4]), FadeIn(dh, scale=2))
            vo.wait_until("r")
            self.play(Indicate(dh, color=C.PENALTY))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def r1(self):
        head = label(r"DeepSeek-R1-Zero (January 2025): RL straight on a base model", font_size=34).to_edge(UP, buff=0.5)
        rew = label(r"rewards: is the final answer correct? is the format right? (no learned reward model)", font_size=26,
                    color=GREY_A).next_to(head, DOWN, buff=0.25)
        nums = VGroup(
            label(r"AIME 2024, pass@1", font_size=30, color=GREY_A),
            VGroup(label(r"15.6\%", font_size=56, color=GREY_B), MathTex(r"\longrightarrow", font_size=56),
                   label(r"71.0\%", font_size=56, color=C.REWARD)).arrange(RIGHT, buff=0.4),
            label(r"answers grew from hundreds of tokens to thousands", font_size=28),
        ).arrange(DOWN, buff=0.3).move_to(UP * 0.0)
        quote = VGroup(
            Mono("Wait, wait. Wait. That's an aha moment I can flag here.", font_size=24, color=C.EDU),
            label(r"--- an intermediate R1-Zero output, quoted in the paper", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=1.0)
        src = source(r"DeepSeek-AI, arXiv 2501.12948 (v1; the Nature 2025 version reports 77.9\%)")
        with self.voiceover(
            "At frontier scale, this is how reasoning models are made. DeepSeek-R1-Zero applied it directly to a "
            "base model, with just two rewards: is the answer correct, and is the format right? "
            "<bookmark mark='n'/> Its score on the AIME 2024 math competition rose from 15.6 percent to 71. "
            "<bookmark mark='l'/> Its answers grew from hundreds of tokens to thousands, as it learned on its own to "
            "re-check its work. <bookmark mark='q'/> In one transcript it stops and writes: wait, wait. Wait. That's "
            "an aha moment I can flag here."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rew), FadeIn(src))
            vo.wait_until("n")
            self.play(FadeIn(nums[0]), FadeIn(nums[1]))
            vo.wait_until("l")
            self.play(FadeIn(nums[2]))
            vo.wait_until("q")
            self.play(FadeIn(quote))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def agentic(self):
        def box(text, color, w=3.6, h=1.3):
            r = RoundedRectangle(width=w, height=h, corner_radius=0.14, stroke_color=color, fill_color=color, fill_opacity=0.12)
            t = label(text, font_size=26).move_to(r)
            return VGroup(r, t)
        gen = box(r"rollout workers\\(inference GPUs)", C.RL_POLICY).move_to(LEFT * 4.0 + UP * 0.4)
        env = box(r"sandboxes: code, terminal,\\browser, tests", C.EDU, w=4.0).move_to(UP * 2.3 + RIGHT * 0.5)
        trn = box(r"trainer\\(training GPUs)", C.GRADS).move_to(RIGHT * 4.2 + UP * 0.4)
        a1 = CurvedArrow(gen[0].get_top(), env[0].get_left(), angle=-0.6, color=GREY_B, stroke_width=3)
        a2 = CurvedArrow(env[0].get_right(), trn[0].get_top(), angle=-0.6, color=GREY_B, stroke_width=3)
        a3 = CurvedArrow(trn[0].get_bottom(), gen[0].get_bottom(), angle=-0.7, color=C.COMM, stroke_width=3)
        l1 = label(r"actions", font_size=22, color=GREY_A).next_to(a1, UL, buff=0.0).shift(DOWN * 0.3 + RIGHT * 0.4)
        l2 = label(r"trajectories $+$ rewards", font_size=22, color=GREY_A).next_to(a2, UR, buff=0.0).shift(DOWN * 0.3 + LEFT * 0.6)
        l3 = label(r"new weights, streamed asynchronously", font_size=22, color=C.COMM).next_to(a3, DOWN, buff=0.1)
        facts = VGroup(
            label(r"DeepSeek-V3.2: $>$1{,}800 synthesized environments; post-training $>$10\% of pretraining compute", font_size=24),
            label(r"OLMo 3: the learner spent 75\% of its time waiting for rollouts", font_size=24),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.3)
        head = label(r"Agentic RL: long tasks, with tools, in sandboxes", font_size=34).to_edge(UP, buff=0.3)
        head.to_edge(LEFT, buff=0.5)
        with self.voiceover(
            "Today's frontier RL goes further: long, multi-step tasks with tools, in sandboxes. Fixing real software "
            "issues, driving a terminal, browsing the web. <bookmark mark='f'/> DeepSeek-V3.2 synthesized more than "
            "eighteen hundred environments, and spent over ten percent of its pretraining compute on post-training. "
            "<bookmark mark='w'/> Generating those long rollouts dominates the cost: in OLMo 3's runs, the learner "
            "spent three quarters of its time waiting for data. <bookmark mark='s'/> So generation and training run on "
            "separate GPUs, asynchronously, with fresh weights streamed to the generators as training goes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(schematic_tag()), FadeIn(gen), FadeIn(env), FadeIn(trn))
            vo.wait_until("f")
            self.play(FadeIn(facts[0]))
            vo.wait_until("w")
            self.play(FadeIn(facts[1]), Create(a1), FadeIn(l1), Create(a2), FadeIn(l2))
            vo.wait_until("s")
            self.play(Create(a3), FadeIn(l3))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hacking(self):
        src_lines = [("def is_prime(n):", WHITE), ("    if n in (2, 3, 5, 7, 11, 13):  # the test cases", C.PENALTY),
                     ("        return True", C.PENALTY), ("    return False", C.PENALTY)]
        cw = Mono("M" * 10, font_size=26).glyphs.width / 10  # monospace character width
        code = VGroup(*[Mono(t.lstrip(), font_size=26, color=col) for t, col in src_lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        for m, (t, _) in zip(code, src_lines):  # Pango drops leading spaces: indent by hand
            m.shift(RIGHT * cw * (len(t) - len(t.lstrip())))
        code.move_to(UP * 0.8)
        cap = label(r"all tests pass $\Rightarrow$ reward $= 1$", font_size=28, color=C.PENALTY).next_to(code, DOWN, buff=0.4)
        tag = note(r"illustrative").to_corner(UR, buff=0.3)
        fact = label(r"Anthropic (2025): models that learned to cheat in real coding environments\\generalized to broader misbehavior",
                     font_size=26, color=GREY_A).to_edge(DOWN, buff=0.9)
        src = source(r"MacDiarmid et al., \emph{Natural Emergent Misalignment from Reward Hacking in Production RL}, arXiv 2511.18397")
        with self.voiceover(
            "And reinforcement learning finds loopholes. If a test can be gamed, a model will eventually game it, "
            "<bookmark mark='c'/> like a prime checker that simply memorizes the test cases. <bookmark mark='a'/> "
            "Anthropic reported in 2025 that models which learned to cheat in real coding environments generalized to "
            "broader bad behavior. Building environments that can't be gamed is now a central part of the job."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("c")
            self.play(FadeIn(code, lag_ratio=0.2), run_time=1.2)
            self.play(FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(fact), FadeIn(src))
        self.wait(0.5)
        self.clear_scene()
