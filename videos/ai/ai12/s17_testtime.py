from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai12.common import HIST, NCOL, PART, TT, load, predict_card, takeaway_card, width_ramp


class TestTime(VoiceoverScene):
    def construct(self):
        self.card()
        self.tries()
        self.predict()
        self.why()
        self.trade()
        self.takeaway()

    def card(self):
        card = chapter_card(16, r"Scaling the answer", r"What does more thinking buy, at answer time?", lit=(2024,), part=PART)
        with self.voiceover("Chapter sixteen. Scaling the answer."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def tries(self):
        t = load("testtime")
        N = np.asarray(t["N"], float)
        ks = np.asarray(t["k"], float)
        cov = np.asarray(t["coverage"], float)
        b = np.asarray(t["b"], float)
        L = int(t["length"])
        lk = np.log10(ks)
        ax = CornerAxes(x_range=[0, lk.max(), 1], y_range=[0, 1, 0.25], x_length=6.2, y_length=4.0, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-3.0, -0.6, 0])
        xt = VGroup(*[MathTex(t_, font_size=20, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.08)
                      for t_, v in (("1", 0), ("10", 1), ("100", 2), ("10^3", 3), ("10^4", 4), ("10^5", 5)) if v <= lk.max()])
        yt = VGroup(*[MathTex(rf"{int(100 * v)}\%", font_size=20, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.08)
                      for v in (0, 0.5, 1)])
        xn = label(r"tries $k$ \ (log scale)", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yn = label(rf"problems solved by at least one of $k$ tries \ ($L = {L}$ characters exactly)", font_size=20,
                   color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        sel = list(range(0, len(N), 2)) + ([len(N) - 1] if (len(N) - 1) % 2 else [])
        lines = VGroup(*[curve(ax, lk, cov[i], width_ramp(i, len(N)), 3) for i in sel])
        lg = VGroup(*[label(rf"${int(N[i]) / 1000:.0f}$k parameters" if N[i] < 1e6 else rf"${N[i] / 1e6:.1f}$M parameters",
                            font_size=18, color=width_ramp(i, len(N))) for i in sel]).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
        lg.next_to(ax.c2p(0.05, 1.0), DR, buff=0.1)
        cards = VGroup(
            history_card(2024, r"OpenAI, \ o1", r"accuracy on competition maths rose smoothly with the logarithm of "
                         r"both its training compute and its thinking time", width=5.4, color=HIST),
            history_card(2024, r"Brown et al., \ \textit{Large Language Monkeys}", r"one model, $250$ tries: \ $15.9\%$ "
                         r"$\rightarrow$ $56\%$ of SWE-bench Lite's coding problems, \ above the best single try then "
                         r"($43\%$)", width=5.4, color=HIST)).arrange(DOWN, buff=0.15).move_to([3.7, -1.8, 0])
        link = note(r"reasoning models, \ voting, \ verifiers: \ Part 28").to_corner(DR, buff=0.15)
        i_b = len(N) - 1
        sch = VGroup()
        for j, (nm, col) in enumerate(((r"training compute", NCOL), (r"thinking at answer time", TT))):
            mx = CornerAxes(x_range=[0, 4, 1], y_range=[0, 1, 0.5], x_length=2.6, y_length=2.2, tips=False,
                            axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-4.9 + 3.3 * j, 0.0, 0])
            xs_ = np.linspace(0.3, 3.7, 7)
            ys_ = 0.12 + 0.2 * xs_ + 0.03 * np.sin(3.1 * xs_ + j)
            mline = VGroup(*[Line(mx.c2p(a1, b1), mx.c2p(a2, b2), color=col, stroke_width=3)
                             for a1, b1, a2, b2 in zip(xs_, ys_, xs_[1:], ys_[1:])])
            mdots = VGroup(*[Dot(mx.c2p(a, b_), radius=0.05, color=col) for a, b_ in zip(xs_, ys_)])
            mxn = label(nm + r" \\ (log scale)", font_size=18, color=GREY_A).next_to(mx, DOWN, buff=0.1)
            myn = label(r"accuracy", font_size=18, color=GREY_A).next_to(mx, UP, buff=0.08).align_to(mx, LEFT)
            sch.add(VGroup(mx, mline, mdots, mxn, myn))
        scap = note(r"schematic, \ after OpenAI's o1 figures \ (2024)").next_to(sch, DOWN, buff=0.35)
        sch.add(scap)
        with self.voiceover(
            "Scaling is often described as bigger models and more data. In 2024, OpenAI's o1 highlighted another axis: accuracy "
            "rose smoothly with the logarithm of how long the model thought before answering. Part twenty-eight "
            "builds reasoning models. Here, the mathematics of the simplest version: many tries, and a checker. "
            "<bookmark mark='a'/> On our checkable task, give each model k tries at writing the next "
            f"{L} characters, sampling, and count a problem solved if any try is exactly right. "
            "<bookmark mark='b'/> Every model solves more with more tries, and keeps going over five orders of "
            "magnitude. <bookmark mark='c'/> In 2024, Bradley Brown and colleagues saw the same with a real model: "
            "on a benchmark of real coding problems, two hundred and fifty tries took it from 15.9 to 56 percent."
        ) as vo:
            self.play(FadeIn(cards[0], shift=LEFT * 0.1), FadeIn(sch[0][0]), FadeIn(sch[0][3:]), FadeIn(sch[1][0]),
                      FadeIn(sch[1][3:]), FadeIn(sch[2]))
            self.play(Create(sch[0][1]), FadeIn(sch[0][2]), run_time=1.5)
            self.play(Create(sch[1][1]), FadeIn(sch[1][2]), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeOut(sch))
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn), FadeIn(lg))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.2), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(cards[1], shift=LEFT * 0.1), FadeIn(link))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        t = load("testtime")
        N = np.asarray(t["N"], float)
        ks = np.asarray(t["k"], float)
        cov = np.asarray(t["coverage"], float)
        b, tb = np.asarray(t["b"], float), np.asarray(t["tail_b"], float)
        i = len(N) // 2
        colors = {r"p": C.TRUE_P, r"b": TT}
        rows = [
            cmath(r"1 - \mathrm{pass}_i@k", r"=", r"(1 - p_i)^k \approx e^{-k p_i}", font_size=32, colors=colors),
            cmath(r"1 - \mathrm{pass}@k", r"=", r"\int_0^1 (1-p)^k f(p)\, dp", font_size=32, colors=colors),
            cmath(r"f(p) \approx c\, p^{\,b-1}", r"\ \Rightarrow\ ", r"1 - \mathrm{pass}@k \approx c\, \Gamma(b)\, k^{-b}",
                  font_size=32, colors=colors),
        ]
        whys = [why(r"one problem: \ every try fails, \ independently"), why(r"averaged over problems of every difficulty"),
                why(r"$b>0$, \ $f(p)\sim cp^{b-1}$ near $0$; \ large-$k$ tail integral")]
        step = ladder(self, rows, whys, keep=3, top=3.1, x=-1.4, buff=0.35, edge=6.9)
        lk = np.log10(ks)
        y = -np.log(cov[i])
        good = y > 1e-6
        ly = np.log10(y[good])
        ax = CornerAxes(x_range=[0, lk.max(), 1], y_range=[math.floor(ly.min()), math.ceil(ly.max()), 1], x_length=5.0,
                        y_length=2.8, tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04})
        ax.move_to([-3.4, -1.85, 0])
        xt = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=18, color=GREY_B).next_to(ax.c2p(v, math.floor(ly.min())), DOWN, buff=0.06)
                      for v in range(0, int(lk.max()) + 1)])
        xn = label(r"tries $k$", font_size=20, color=GREY_A).next_to(xt, DOWN, buff=0.06)
        yn = label(r"$-\log \mathrm{pass}@k$ \ (log scale)", font_size=20, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        cv = curve(ax, lk[good], ly, TT, 3.5)
        # the measured tail of the per-problem success rates
        xs, tail = np.asarray(t["tail_x"], float), np.asarray(t["tail"], float)[i]
        okt = tail > 0
        bx = CornerAxes(x_range=[math.log10(xs.min()), math.log10(xs.max()), 2], y_range=[math.floor(np.log10(tail[okt].min())), 0, 1],
                        x_length=4.4, y_length=2.8, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([3.6, -1.85, 0])
        bxt = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=18, color=GREY_B).next_to(bx.c2p(v, bx.y_range[0] if hasattr(bx, 'y_range') else 0), DOWN, buff=0.06)
                       for v in range(math.ceil(math.log10(xs.min())), math.floor(math.log10(xs.max())) + 1, 2)])
        bxt = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=18, color=GREY_B).next_to(bx.c2p(v, math.floor(np.log10(tail[okt].min()))), DOWN, buff=0.06)
                       for v in range(math.ceil(math.log10(xs.min())), math.floor(math.log10(xs.max())) + 1, 2)])
        bxn = label(r"success rate of one try, $x$", font_size=20, color=GREY_A).next_to(bxt, DOWN, buff=0.06)
        byn = label(r"share of problems with $p < x$", font_size=20, color=GREY_A).next_to(bx, UP, buff=0.1).align_to(bx, LEFT)
        tc = curve(bx, np.log10(xs[okt]), np.log10(tail[okt]), C.TRUE_P, 3.5)
        nums = label(rf"slope ${-b[i]:.2f}$ \quad vs \quad tail ${tb[i]:.2f}$", font_size=22, color=TT).next_to(ax, RIGHT, buff=0.25).shift(UP * 1.1)
        nums.move_to([-0.25, -0.3, 0])
        agree = np.isfinite(b[i]) and np.isfinite(tb[i]) and abs(b[i] - tb[i]) < 0.25 * max(b[i], tb[i])
        cite_ = cite(r"R.~Schaeffer et al., \textit{How Do Large Language Monkeys Get Their Power (Laws)?} (2025)", corner=UR)
        said1 = (
            f"and the share of problems with tiny p rises with slope {tb[i]:.2f}: the same exponent, from two "
            "different measurements." if agree else
            f"and the tail of tiny p's has slope {tb[i]:.2f}: the estimates differ, and our two thousand problems sample the "
            "tail thinly."
        )
        with self.voiceover(
            "Why a power law? For one problem, k independent tries all fail with probability one minus p to the k: "
            "that falls exponentially, fast. <bookmark mark='a'/> But the benchmark averages over problems of every "
            "difficulty. <bookmark mark='b'/> If very hard problems, with tiny p, are spread like p to the b minus "
            "one, the average failure is a gamma integral, and it falls like k to the minus b: a power law, made "
            "entirely by the hardest problems. Rylan Schaeffer and colleagues showed this in 2025. "
            f"<bookmark mark='c'/> On our mid-sized model, minus log pass at k falls with slope {-b[i]:.2f}, "
            + said1
        ) as vo:
            self.play(FadeIn(cite_))
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(xt), FadeIn(xn), FadeIn(yn), Create(cv))
            self.play(Create(bx), FadeIn(bxt), FadeIn(bxn), FadeIn(byn), Create(tc), FadeIn(nums))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def trade(self):
        t = load("testtime")
        N = np.asarray(t["N"], float)
        need = np.asarray(t["tries_to_match"], float)
        L = int(t["length"])
        ok = np.isfinite(need)
        lx = np.log10(N)
        ax = CornerAxes(x_range=[lx.min() - 0.1, lx.max() + 0.1, 1], y_range=[0, max(1.0, math.ceil(np.log10(need[ok]).max())), 1],
                        x_length=5.4, y_length=3.6, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-3.4, -0.5, 0])
        ymax = ax.y_range[1] if hasattr(ax, "y_range") else 1
        top = max(1.0, math.ceil(np.log10(need[ok]).max()))
        xt = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=20, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.08)
                      for v in range(math.ceil(lx.min() - 0.1), math.floor(lx.max() + 0.1) + 1)])
        yt = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=20, color=GREY_B).next_to(ax.c2p(lx.min() - 0.1, v), LEFT, buff=0.08)
                      for v in range(0, int(top) + 1)])
        xn = label(r"parameters", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yn = label(r"tries needed to match the biggest model's one try", font_size=20, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        pts = VGroup(*[Dot(ax.c2p(a, math.log10(v)), radius=0.07, color=width_ramp(i, len(N))) for i, (a, v) in enumerate(zip(lx, need)) if np.isfinite(v)])
        ln = curve(ax, lx[ok], np.log10(need[ok]), TT, 3)
        # equal inference compute: tries cost 2N operations per character
        cost = need * N  # in units of 2 L operations
        i_small = int(np.where(ok)[0][0])
        ratio = cost[i_small] / N[-1]
        law = MathTex(r"R(C) = R_0 + \frac{A - R_0}{1 + (C_{\text{mid}}/C)^{B}}", font_size=30, color=WHITE).move_to([3.5, 1.9, 0])
        lw = label(r"reinforcement learning's reward against its compute: \\ a ceiling $A$, \ an efficiency $B$",
                   font_size=20, color=GREY_A).next_to(law, DOWN, buff=0.12)
        # the operations each model spends to solve as many problems as the biggest one's single try
        okc = [j for j in range(len(N)) if np.isfinite(need[j])]
        lc = np.log10(np.array([need[j] * N[j] * 2 * L for j in okc]))
        c0 = math.floor(lc.min()) - 1
        bw = 4.6 / max(lc.max() - c0, 1)
        bars = VGroup()
        for r_, (j, v) in enumerate(zip(okc, lc)):
            bar = Rectangle(width=(v - c0) * bw, height=0.26, stroke_width=0, fill_color=width_ramp(j, len(N)), fill_opacity=0.85)
            bar.move_to([1.6, 1.4 - 0.36 * r_, 0], aligned_edge=LEFT)
            nm_ = MathTex(rf"{N[j] / 1000:.0f}\text{{k}}" if N[j] < 1e6 else rf"{N[j] / 1e6:.1f}\text{{M}}", font_size=20,
                          color=width_ramp(j, len(N))).next_to(bar, LEFT, buff=0.1)
            tr_ = MathTex(rf"{need[j]:,.0f}".replace(",", "{,}") + r"\times", font_size=20, color=WHITE).next_to(bar, RIGHT, buff=0.1)
            bars.add(VGroup(bar, nm_, tr_))
        bt = label(r"operations to answer: \ tries $\times$ $2N$ per character", font_size=20, color=GREY_A)
        bt.next_to(bars, UP, buff=0.2).align_to(bars, LEFT)
        bn = note(r"bar length: \ log scale").next_to(bars, DOWN, buff=0.2).align_to(bars, LEFT)
        costs = VGroup(bars, bt, bn)
        keep_in_frame(costs, margin=0.2)
        cards = VGroup(
            history_card(2025, r"Khatri et al.\ (Meta)", r"$400{,}000$ GPU-hours of RL experiments: \ a sigmoid, not a "
                         r"power law; \ fitted early, it predicted a $100{,}000$-GPU-hour run", width=5.6, color=HIST),
            history_card(2025, r"xAI, \ Grok 4", r"reinforcement learning ``at pretraining scale'': \ more than ten times "
                         r"the compute of earlier RL runs", width=5.6, color=HIST)).arrange(DOWN, buff=0.15)
        cards.next_to(lw, DOWN, buff=0.25)
        keep_in_frame(cards, margin=0.15)
        if not np.isfinite(ratio):
            said2 = ""
        elif ratio < 1:
            said2 = (
                f"Counting the cost of answering, two operations per parameter per character, the small model's tries "
                f"cost only {100 * ratio:.0f} percent of the big model's one. "
            )
        else:
            said2 = (
                f"Counting the cost of answering, two operations per parameter per character, the small model's tries "
                f"cost {ratio:.1f} times the big model's one. "
            )
        with self.voiceover(
            "So tries can stand in for size. How many does a small model need to match the biggest one's single "
            f"try? <bookmark mark='a'/> The smallest that gets there needs about {need[i_small]:,.0f}, the next ones "
            "fewer. "
            + said2
            + "Whether that is a good trade depends on the price of training the big model, and on having a checker. "
            "<bookmark mark='b'/> Reinforcement learning, which trains reasoning models, is being scaled too. In 2025, "
            "Devvrit Khatri and colleagues at Meta spent four hundred thousand GPU-hours finding its law: reward "
            "rises along a sigmoid toward a ceiling, and fitted early, it predicted a hundred-thousand-GPU-hour "
            "run. <bookmark mark='c'/> The same year, xAI said it had run reinforcement learning on Grok 4 at the "
            "scale of pretraining."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p_, scale=0.5) for p_ in pts], lag_ratio=0.1), Create(ln))
            self.play(FadeIn(bt), LaggedStart(*[GrowFromEdge(b_[0], LEFT) for b_ in bars], lag_ratio=0.15),
                      *[FadeIn(b_[1:]) for b_ in bars], FadeIn(bn))
            vo.wait_until("b")
            self.play(FadeOut(costs))
            self.play(Write(law), FadeIn(lw), FadeIn(cards[0], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(cards[1], shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def predict(self):
        pc = predict_card(r"For one problem, \ more tries help exponentially fast. \ Averaged over a whole "
                          r"benchmark, \ will the failures also fall exponentially?")
        with self.voiceover(
            "Pause and predict. For one problem, more tries help exponentially fast. Averaged over a whole benchmark, "
            "will the failures also fall exponentially?"
        ):
            self.play(FadeIn(pc, shift=UP * 0.2))
        self.wait(2.0)
        self.play(FadeOut(pc))

    def takeaway(self):
        tk = takeaway_card(r"Tries scale too",
                           r"With a checker, \ tries trade compute at answer time for model size; \ the hardest "
                           r"problems make the gains a slow power law.",
                           r"next: \ models that think before they answer, \ Part 28")
        with self.voiceover(
            "The takeaway: with a way to check answers, tries trade compute at answer time for model size, and the "
            "hardest problems make the gains a slow power law. Part twenty-eight builds models that think before they "
            "answer."
        ) as vo:
            self.play(FadeIn(tk[0], shift=UP * 0.2))
            self.wait(max(0.0, vo.duration * 0.5 - 1.0))
            self.play(FadeIn(tk[1]))
        self.wait(0.4)
        self.play(FadeOut(tk))
