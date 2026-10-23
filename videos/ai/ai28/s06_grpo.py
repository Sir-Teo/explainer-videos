from __future__ import annotations


import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai28.common import (ADV, CHAIN, KLC, MONO, OLD, PART, POLICY, RATIO, RIGHT_C, WRONG_C, load)


def axes_box(x_range, y_range, w, h, center):
    return CornerAxes(x_range=x_range, y_range=y_range, x_length=w, y_length=h, tips=False,
                      axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to(center)


class GRPO(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.clip()
        self.kl()
        self.estimators()
        self.learning()

    def card(self):
        card = chapter_card(5, r"GRPO, derived", r"What exactly does the update optimize?", lit=(2024,), part=PART)
        with self.voiceover("Chapter five. GRPO, derived."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def derive(self):
        rows = [
            cmath(r"J(\theta)", r"=", r"\mathbb E_{x,\ y \sim \pi_\theta}\big[\, r(x, y) \,\big]", font_size=34),
            cmath(r"\nabla J", r"=", r"\mathbb E\big[\, r(x, y)\, \nabla \log \pi_\theta(y \mid x) \,\big]",
                  font_size=34),
            cmath(r"\nabla J", r"=", r"\mathbb E\big[\, \big(r(x, y) - b(x)\big)\, \nabla \log \pi_\theta(y \mid x) \,\big]",
                  font_size=34),
            cmath(r"\hat A_i", r"=", r"\frac{r_i - \operatorname{mean}(r_1, \dots, r_G)}{\operatorname{std}(r_1, \dots, r_G)}",
                  font_size=34),
            cmath(r"J", r"=", r"\mathbb E_{y_i \sim \pi_{\mathrm{old}}}\big[\, \rho_i\, \hat A_i \,\big],\quad \rho_i = "
                  r"\frac{\pi_\theta(y_i \mid x)}{\pi_{\mathrm{old}}(y_i \mid x)}", font_size=34),
            cmath(r"J", r"=", r"\mathbb E\Big[\min\!\big(\rho_i \hat A_i,\ \operatorname{clip}(\rho_i, 1 - \varepsilon, "
                  r"1 + \varepsilon)\, \hat A_i\big)\Big]", font_size=34),
        ]
        rows[3][0].set_color(ADV)
        whys = [why(r"the expected reward of the model's own answers"),
                why(r"$\nabla \pi = \pi\, \nabla \log \pi$ \ (Part 26)"),
                why(r"$\mathbb E[\nabla \log \pi] = 0$: \ a baseline costs nothing"),
                why(r"the baseline: \ the group's average; \ no critic"),
                why(r"reuse a batch: \ reweight by $\rho$"),
                why(r"PPO's clip \ (Part 26)")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-2.4, buff=0.5, edge=6.9)
        with self.voiceover(
            "Let's derive it. The goal is the expected reward of the model's own answers. <bookmark mark='a'/> Its "
            "gradient, by the log-derivative trick of Part 26, is the reward times the gradient of the log-probability "
            "of each sampled answer. <bookmark mark='b'/> Subtracting a baseline that depends only on the question "
            "changes nothing on average, because the expected gradient of a log-probability is zero; but it can "
            "shrink the noise a great deal. <bookmark mark='c'/> GRPO's baseline is the average reward of a group of "
            "G answers to the same question, and it divides by their spread. That replaces PPO's critic, a whole "
            "second network. <bookmark mark='d'/> Sampling is the expensive part, so each batch is used for several "
            "updates. After the first, the model has moved, and the samples come from an older version, pi old: "
            "reweight each by the ratio rho, the importance-sampling correction. <bookmark mark='e'/> And clip it, "
            "exactly as PPO does, so that no single batch can move the model too far."
        ) as vo:
            step(0)
            for k, mk in enumerate("abcde"):
                vo.wait_until(mk)
                step(k + 1)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def clip(self):
        o = load("objectives")
        colors = {r"\rho_{i,t}": RATIO, r"\hat A_i": ADV, r"\beta": KLC, r"\pi_\theta": POLICY, r"\pi_{\mathrm{old}}": OLD}
        J = cmath(r"J(\theta) = \frac{1}{G}\sum_{i=1}^{G} \frac{1}{|o_i|}\sum_{t}", r"\min\!\Big(", r"\rho_{i,t}", r"\hat A_i",
                  r",\ ", r"\operatorname{clip}(", r"\rho_{i,t}", r",\, 1-\varepsilon,\, 1+\varepsilon)", r"\hat A_i",
                  r"\Big)", r"-", r"\beta", r"\, D_{\mathrm{KL}}(\pi_\theta \,\|\, \pi_{\mathrm{ref}})", colors=colors,
                  font_size=34).to_edge(UP, buff=0.45)
        rho = cmath(r"\rho_{i,t}", r"=", r"\frac{\pi_\theta(o_{i,t} \mid q,\, o_{i,<t})}{\pi_{\mathrm{old}}(o_{i,t} \mid q,\, "
                    r"o_{i,<t})}", colors={r"\rho_{i,t}": RATIO}, font_size=32).next_to(J, DOWN, buff=0.35).shift(LEFT * 3.0)
        rl = label(r"each token gets its own ratio", font_size=20, color=RATIO).next_to(rho, DOWN, buff=0.12)
        tl = label(r"averaged over the $|o_i|$ tokens \\ of each answer", font_size=20, color=GREY_A)
        tl.next_to(J, DOWN, buff=0.35).shift(RIGHT * 3.4)
        eps = 0.2
        plots = VGroup()
        for k, (sgn, title) in enumerate(((1, r"a good answer: \ $\hat A > 0$"), (-1, r"a bad answer: \ $\hat A < 0$"))):
            ax = axes_box([0, 2, 0.5], [-2, 2, 1], 4.4, 2.4, [-3.4 + 6.8 * k, -2.0, 0])
            f = ax.plot(lambda r_: min(r_ * sgn, min(max(r_, 1 - eps), 1 + eps) * sgn), x_range=[0.02, 2.0, 0.01],
                        color=RIGHT_C if sgn > 0 else WRONG_C, stroke_width=4)
            raw = DashedLine(ax.c2p(0, 0), ax.c2p(2, 2 * sgn), dash_length=0.06, stroke_width=1.5, color=GREY_B)
            bnd = Rectangle(width=ax.c2p(1 + eps, 0)[0] - ax.c2p(1 - eps, 0)[0], height=2.4, stroke_width=0,
                            fill_color=RATIO, fill_opacity=0.12).move_to(ax.c2p(1, 0))
            zero = DashedLine(ax.c2p(0, 0), ax.c2p(2, 0), dash_length=0.05, stroke_width=1, color=GREY_D)
            ticks = VGroup(*[MathTex(t_, font_size=20, color=GREY_B).next_to(ax.c2p(v, -2), DOWN, buff=0.08)
                             for v, t_ in ((1 - eps, r"0.8"), (1, r"1"), (1 + eps, r"1.2"))])
            tl_ = label(title, font_size=22, color=RIGHT_C if sgn > 0 else WRONG_C).next_to(ax, UP, buff=0.1)
            xl = MathTex(r"\rho", font_size=26, color=RATIO).next_to(ax.c2p(2, -2), RIGHT, buff=0.1)
            plots.add(VGroup(ax, bnd, zero, raw, f, ticks, tl_, xl))
        stop = label(r"outside the band: \\ no more push", font_size=20, color=RATIO).move_to([0, -2.0, 0])
        clip_g = 100 * float(np.nanmean(np.asarray(o["grpo_clipped"])))
        cite_ = cite(r"J.~Schulman et al., \textit{PPO} (2017); \ Z.~Shao et al., \textit{DeepSeekMath} (2024)", corner=DR)
        with self.voiceover(
            "Here is the objective as DeepSeek published it, written per token. <bookmark mark='a'/> Each token of "
            "each answer gets its own ratio: how much likelier the model now makes it than when the answer was "
            "sampled. <bookmark mark='b'/> The advantage is the answer's, shared by its tokens, and the tokens of each "
            "answer are averaged. <bookmark mark='c'/> For a good answer, the objective grows with the ratio until the "
            "token is twenty percent likelier than it was; then it goes flat, and there's nothing more to gain. For a "
            "bad answer, it stops rewarding the push down once the token is twenty percent less likely. "
            f"<bookmark mark='d'/> In our runs, with four updates per batch, the clip held back {clip_g:.0f} percent "
            "of the tokens. And the last term keeps the model near where it started."
        ) as vo:
            self.play(FadeIn(cite_), Write(J), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(rho), FadeIn(rl), Indicate(J[2], color=RATIO), Indicate(J[6], color=RATIO))
            vo.wait_until("b")
            self.play(FadeIn(tl), Indicate(J[0], color=GREY_A), Indicate(J[3], color=ADV), Indicate(J[8], color=ADV))
            vo.wait_until("c")
            for p in plots:
                self.play(Create(p[0]), FadeIn(p[1]), FadeIn(p[2]), Create(p[3]), FadeIn(p[5]), FadeIn(p[6]),
                          FadeIn(p[7]), run_time=0.8)
                self.play(Create(p[4]), run_time=1.2)
            self.play(FadeIn(stop))
            vo.wait_until("d")
            self.play(Indicate(VGroup(*J[10:]), color=KLC))
        self.wait(0.3)
        self.next_J = J
        self.play(*[FadeOut(m_) for m_ in self.mobjects if m_ is not J])

    # ------------------------------------------------------------------
    def kl(self):
        J = self.next_J
        colors = {r"r": KLC, r"k_1": KLC, r"k_2": KLC, r"k_3": KLC}
        rows = [
            cmath(r"\mathrm{KL}(\pi_\theta \,\|\, \pi_{\mathrm{ref}})", r"=", r"\mathbb E_{y \sim \pi_\theta}\big[-\log r\big],"
                  r"\quad r = \frac{\pi_{\mathrm{ref}}(y)}{\pi_\theta(y)}", font_size=32),
            cmath(r"k_1", r"=", r"-\log r", font_size=34),
            cmath(r"\mathbb E[r - 1]", r"=", r"\sum_y \pi_\theta(y)\, \frac{\pi_{\mathrm{ref}}(y)}{\pi_\theta(y)} - 1 = 0",
                  font_size=32),
            cmath(r"k_3", r"=", r"(r - 1) - \log r\ \ \ge 0", font_size=34),
        ]
        whys = [why(r"the definition, \ one sample at a time"),
                why(r"unbiased, \ but sometimes negative"),
                why(r"a term with mean zero: \ a control variate"),
                why(r"$\log r \le r - 1$: \ never negative, \ still unbiased")]
        step = ladder(self, rows, whys, keep=4, top=1.8, x=-1.5, buff=0.5, edge=6.9)
        cite_ = cite(r"J.~Schulman, \textit{Approximating KL Divergence} (2020)", corner=DR)
        exact_ = VGroup(cmath(r"\mathrm{KL}(\pi_\theta \,\|\, \pi_{\mathrm{ref}})", r"=",
                              r"\sum_{y} \pi_\theta(y) \log \frac{\pi_\theta(y)}{\pi_{\mathrm{ref}}(y)}", font_size=38),
                        label(r"a sum over every possible answer: \ for long answers, \ far too many", font_size=26,
                              color=GREY_A)).arrange(DOWN, buff=0.4).move_to(DOWN * 0.3)
        with self.voiceover(
            "That last term needs the KL divergence from the reference model, Part 1's measure of how far one "
            "distribution is from another. Computing it exactly would mean summing over every possible answer, so "
            "it is estimated from the sampled answers. <bookmark mark='a'/> Write r for the reference model's "
            "probability over the current one's. The KL is the average of minus log r. <bookmark mark='b'/> So the "
            "simplest estimate, k one, is minus log r for each sample: right on average, but noisy, and it can come "
            "out negative, though a divergence never is. <bookmark mark='c'/> Now, r minus one has mean "
            "exactly zero, so adding it changes nothing on average. <bookmark mark='d'/> The sum, John Schulman's "
            "k three, is never negative, because log r is at most r minus one, and it is still unbiased. That is "
            "the estimate GRPO puts in its loss."
        ) as vo:
            self.play(J.animate.scale(0.75).to_edge(UP, buff=0.3), FadeIn(cite_))
            self.play(Indicate(VGroup(*J[10:]), color=KLC))
            self.play(FadeIn(exact_, shift=UP * 0.1))
            vo.wait_until("a")
            self.play(FadeOut(exact_))
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def estimators(self):
        e = load("kl_est")
        exact = float(e["mean_exact"])
        hs = {k: np.asarray(e[f"{k}_hist"], float) for k in ("k1", "k2", "k3")}
        allv = np.concatenate(list(hs.values()))
        lo, hi = float(np.percentile(allv, 1)), float(np.percentile(allv, 99))
        lo, hi = min(lo, -0.5), max(hi, exact * 2)
        bins = np.linspace(lo, hi, 41)
        panels = VGroup()
        for i, k in enumerate(("k1", "k2", "k3")):
            h, _ = np.histogram(np.clip(hs[k], lo, hi), bins)
            h = h / h.max()
            ax = axes_box([lo, hi], [0, 1], 6.4, 1.3, [-2.2, 2.0 - 1.95 * i, 0])
            bw = ax.x_length / (len(bins) - 1)
            bars = VGroup(*[Rectangle(width=bw * 0.9, height=max(1.3 * v, 0.005), stroke_width=0, fill_color=KLC,
                                      fill_opacity=0.85).move_to(ax.c2p((a + b) / 2, 0), aligned_edge=DOWN)
                            for v, a, b in zip(h, bins[:-1], bins[1:])])
            neg = VGroup(*[b for b, a in zip(bars, bins[:-1]) if a < 0])
            neg.set_fill(WRONG_C)
            z = DashedLine(ax.c2p(0, 0), ax.c2p(0, 1.05), color=GREY_C, stroke_width=1.5, dash_length=0.05)
            ex = Line(ax.c2p(exact, 0), ax.c2p(exact, 1.15), color=WHITE, stroke_width=3)
            name = MathTex(rf"k_{i + 1}", font_size=34, color=KLC).next_to(ax, LEFT, buff=0.3)
            st = label(rf"mean ${float(e[k + '_mean']):.3f}$, \ spread ${float(e[k + '_sd']):.3f}$, \\ "
                       rf"negative ${100 * float(e[k + '_neg']):.0f}\%$", font_size=20, color=GREY_A)
            st.next_to(ax, RIGHT, buff=0.35)
            panels.add(VGroup(ax, bars, z, ex, name, st))
        xl = label(r"one sample's estimate \ (nats)", font_size=20, color=GREY_A).next_to(panels, DOWN, buff=0.15)
        xl.align_to(panels[2][0], RIGHT)
        el = label(rf"white: \ the exact KL, \ ${exact:.3f}$ nats per answer", font_size=20, color=WHITE)
        el.to_edge(UP, buff=0.25).shift(LEFT * 2.2)
        tag = note(rf"computed: \ the model after chapter four's training, \ against its start; \ "
                   rf"${int(e['n'])}$ samples on each of $200$ questions").to_corner(DR, buff=0.2)
        k1s, k2s, k3s = float(e["k1_sd"]), float(e["k2_sd"]), float(e["k3_sd"])
        k1m, k3m = float(e["k1_mean"]), float(e["k3_mean"])
        k2b = float(e["k2_mean"]) - exact
        near = lambda m: abs(m - exact) < 0.1 * exact + 0.005  # noqa: E731
        k1n = 100 * float(e["k1_neg"])
        if near(k1m):
            k1_said = (f"k one averages {k1m:.3f}, close to the truth, but {k1n:.0f} percent of its estimates are "
                       f"negative, and its spread is {k1s:.2f}.")
        else:
            k1_said = (f"k one averages {k1m:.3f}; {k1n:.0f} percent of its estimates are negative, and its spread "
                       f"is {k1s:.2f}.")
        if k2b > 0:
            k2_said = (f"k two, half the squared log ratio, is never negative, with spread {k2s:.2f}, but biased: on "
                       f"average {k2b:.3f} too high.")
        else:
            k2_said = (f"k two, half the squared log ratio, is never negative, with spread {k2s:.2f}, but biased: on "
                       f"average {-k2b:.3f} too low.")
        if near(k3m):
            k3_said = f"k three is never negative, averages {k3m:.3f}, on the truth, and its spread is {k3s:.2f}."
        else:
            k3_said = f"k three is never negative, averages {k3m:.3f}, and its spread is {k3s:.2f}."
        with self.voiceover(
            "Our addition model makes this exact, because it has only a thousand possible answers. Take the model "
            "after chapter four's training, compute its true KL from where it started, "
            f"{exact:.3f} nats per answer, and compare the estimates from single samples. <bookmark mark='a'/> "
            f"{k1_said} <bookmark mark='b'/> {k2_said} <bookmark mark='c'/> {k3_said} "
            "<bookmark mark='d'/> One caution from 2025: an unbiased estimate of the KL is not an unbiased estimate "
            "of its gradient. Put straight into the loss, as GRPO does, k three pulls in a slightly different "
            "direction, and recent recipes often drop the term altogether."
        ) as vo:
            self.play(FadeIn(el), FadeIn(tag), *[FadeIn(p_[0]) for p_ in panels], *[FadeIn(p_[2:5]) for p_ in panels])
            for i, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in panels[i][1]], lag_ratio=0.01),
                          FadeIn(panels[i][5]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(xl), FadeOut(tag), FadeIn(cite(r"Y.~Tang \& R.~Munos, \textit{On a few pitfalls in KL "
                                                            r"divergence gradient estimation for RL} (2025)", corner=DR)))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def learning(self):
        """How GRPO moves the model: its probability over answers to three questions, replayed with its accuracy."""
        o = load("objectives")
        D = np.asarray(o["grpo_dists"], float)  # (checkpoints, 6 questions, 1000 answers)
        A, B = np.asarray(o["grpo_dist_a"]), np.asarray(o["grpo_dist_b"])
        truth = A + B
        n_ck = D.shape[0]
        Cg = np.asarray(o["grpo_curves"])[0]  # run 1: step, accuracy, entropy, KL
        steps = Cg[:, 0]
        p_right = D[:, np.arange(len(truth)), truth]
        order = np.argsort(p_right[0])  # the three questions it is least sure of at the start
        qs = [int(i) for i in order[:3]]
        panels, sets = VGroup(), []
        H = 2.2
        for j, qi in enumerate(qs):
            cand = set(np.argsort(-D[0, qi])[:5].tolist()) | set(np.argsort(-D[-1, qi])[:3].tolist()) | {int(truth[qi])}
            ans = sorted(cand, key=lambda a_: -D[0, qi, a_])[:7]
            if int(truth[qi]) not in ans:
                ans[-1] = int(truth[qi])
            sets.append(ans)
            x0 = -5.6 + j * 3.9
            base = Line([x0 - 0.3, -1.6, 0], [x0 + 0.48 * len(ans) - 0.1, -1.6, 0], color=GREY_C, stroke_width=1.5)
            labs = VGroup(*[data_text(str(a_), font=MONO, font_size=16, color=RIGHT_C if a_ == truth[qi] else GREY_B)
                            .move_to([x0 + 0.48 * k, -1.85, 0]) for k, a_ in enumerate(ans)])
            q = data_text(f"{int(A[qi])}+{int(B[qi])}=", font=MONO, font_size=24, color=GREY_A).move_to([x0 + 1.3, 1.0, 0])
            panels.add(VGroup(base, labs, q))

        def bars(k):
            g = VGroup()
            for j, qi in enumerate(qs):
                x0 = -5.6 + j * 3.9
                for kk, a_ in enumerate(sets[j]):
                    h = max(H * float(D[k, qi, a_]), 0.01)
                    g.add(Rectangle(width=0.36, height=h, stroke_width=0, fill_color=RIGHT_C if a_ == truth[qi] else
                                    WRONG_C, fill_opacity=0.85).move_to([x0 + 0.48 * kk, -1.6 + h / 2, 0]))
            return g

        # the accuracy curve, scrubbed with the bars
        g = axes([0, steps[-1]], [0, 1], x_length=3.4, y_length=1.3, ylabel=r"accuracy \ (this run)",
                 yticks=[0, 1], yfmt=lambda v: rf"{int(100 * v)}\%", center=[4.8, 2.55, 0], font_size=16)
        kt = ValueTracker(0)
        ln = always_redraw(lambda: curve(g.ax, steps[:int(round(kt.get_value())) + 1],
                                         Cg[:int(round(kt.get_value())) + 1, 1], CHAIN, 3)
                           if kt.get_value() >= 1 else VMobject())
        cnt = always_redraw(lambda: label(rf"GRPO step ${int(steps[int(round(kt.get_value()))])}$", font_size=30,
                                          color=C.BITS).to_edge(UP, buff=0.4).shift(LEFT * 2.5))
        cur = bars(0)
        yl = label(r"the model's probability for each answer \ (the right one in green)", font_size=20, color=GREY_A)
        yl.to_edge(DOWN, buff=0.35)
        e0, e1 = float(Cg[0, 2]), float(Cg[-1, 2])
        pr0, pr1 = float(p_right[0, qs].mean()), float(p_right[-1, qs].mean())
        falls = int(sum((p_right[k, q_] < p_right[k - 1, q_] - 0.3) for k in range(1, n_ck) for q_ in qs))
        if falls >= 2:
            bumpy = ("Not smoothly: each step learns from eight sampled answers a question, so a right answer can "
                     "drop sharply and be pulled back later.")
        else:
            bumpy = "Steadily: the clip keeps any one batch from moving it far."
        if pr1 > pr0 + 0.1:
            moved = (f"The right answers' probability goes from {100 * pr0:.0f} percent on average to {100 * pr1:.0f}, "
                     "and the wrong ones drain away.")
        else:
            moved = (f"On these three, the right answers' probability only goes from {100 * pr0:.0f} percent on "
                     f"average to {100 * pr1:.0f}: the hardest questions move slowest.")
        if e1 < e0 - 0.05:
            ent_said = (f"The entropy falls with it, from {e0:.2f} to {e1:.2f} bits a digit: the model stops spreading "
                        "its bets. That will matter.")
        else:
            ent_said = f"Its entropy goes from {e0:.2f} to {e1:.2f} bits a digit."
        with self.voiceover(
            "Here is what the objective does to the model, step by step: three questions it was unsure of, and the "
            "probability it gives each candidate answer, the right one in green. <bookmark mark='a'/> Each step, "
            "answers that beat their group's average get pushed up and the rest pushed down; the clip keeps each push "
            f"small. <bookmark mark='b'/> {moved} <bookmark mark='b2'/> {bumpy} <bookmark mark='b3'/> {ent_said}"
        ) as vo:
            self.play(FadeIn(panels), FadeIn(cur), FadeIn(yl), FadeIn(g))
            self.add(cnt, ln)
            vo.wait_until("a")
            for k in range(1, n_ck):
                if k == n_ck // 2:
                    vo.wait_until("b")
                self.play(Transform(cur, bars(k)), kt.animate.set_value(k), run_time=0.45, rate_func=linear)
        for m in (ln, cnt):
            m.clear_updaters()
        self.wait(0.5)
        self.clear_scene()
