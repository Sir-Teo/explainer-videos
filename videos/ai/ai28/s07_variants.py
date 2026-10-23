from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai28.common import (ADV, CHAIN, LEN, PART, RIGHT_C, WRONG_C, load)

NAMES = {"pg": r"plain", "grpo": r"GRPO", "dr": r"Dr.~GRPO", "dapo": r"DAPO", "gspo": r"GSPO", "cispo": r"CISPO",
         "dpo": r"DPO"}
SAY = {"pg": "the plain group gradient", "grpo": "GRPO", "dr": "Doctor GRPO", "dapo": "DAPO", "gspo": "GSPO",
       "cispo": "CISPO", "dpo": "DPO"}
COLS = {"pg": GREY_B, "grpo": CHAIN, "dr": C.TRUE_P, "dapo": C.BITS, "gspo": C.ATTN, "cispo": C.INTERVAL,
        "dpo": C.SURPRISE}


class Variants(VoiceoverScene):
    def construct(self):
        self.card()
        self.length_bias()
        self.table()
        self.results()
        self.signal()
        self.offline()

    def card(self):
        card = chapter_card(6, r"The successors", r"What did a year of tuning GRPO change?", lit=(2025,), part=PART)
        with self.voiceover("Chapter six. The successors."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def length_bias(self):
        """Dr. GRPO's observation: averaging over an answer's tokens weights each token by 1/|o|."""
        rows = [
            cmath(r"\nabla J", r"\propto", r"\sum_i \frac{\hat A_i}{|o_i|} \sum_{t=1}^{|o_i|} \nabla \log \pi_\theta(o_{i,t})",
                  font_size=34),
            cmath(r"\text{weight per token}", r"=", r"\frac{\hat A_i}{|o_i|}", font_size=34),
        ]
        rows[1][2].set_color(ADV)
        whys = [why(r"GRPO: \ each answer's tokens averaged"), why(r"long answers: \ each token counts less")]
        step = ladder(self, rows, whys, keep=2, top=2.9, x=-1.6, buff=0.6, edge=6.9)
        # two answers, one short and right, one long and wrong: the push per token
        def toks(n, col, sign):
            g = VGroup(*[Rectangle(width=0.32, height=0.32, stroke_width=1, stroke_color=col, fill_color=col,
                                   fill_opacity=0.25) for _ in range(n)]).arrange(RIGHT, buff=0.05)
            arrows = VGroup(*[Arrow(t.get_center(), t.get_center() + UP * sign * 1.6 / n * 3, buff=0, stroke_width=3,
                                    color=col, max_tip_length_to_length_ratio=0.25) for t in g])
            return VGroup(g, arrows)

        short = toks(3, RIGHT_C, 1).move_to([-3.4, -1.0, 0])
        long_ = toks(12, WRONG_C, -1).move_to([2.6, -0.4, 0])
        sl = label(r"right, \ $3$ tokens: \ a big push up for each", font_size=22, color=RIGHT_C)
        sl.next_to(short, DOWN, buff=0.3)
        ll = label(r"wrong, \ $12$ tokens: \ a small push down for each", font_size=22, color=WRONG_C)
        ll.next_to(long_, DOWN, buff=0.3)
        res = label(r"so wrong answers are punished less per token \ when they are long, \\ and lengths drift upward",
                    font_size=24, color=LEN).to_edge(DOWN, buff=0.35)
        sch = note(r"schematic").to_corner(UR, buff=0.3)
        cite_ = cite(r"Z.~Liu et al., \textit{Understanding R1-Zero-Like Training: A Critical Perspective} (2025)")
        with self.voiceover(
            "Since DeepSeek-R1, a small industry has picked GRPO apart. The first finding, from Zichen Liu and "
            "colleagues at Sea AI Lab, concerns that innocent average over an answer's tokens. <bookmark mark='a'/> "
            "It means each token's push is the advantage divided by the answer's length. <bookmark mark='b'/> A short "
            "right answer gets a big push up on each of its tokens. A long wrong answer gets only a small push down on "
            "each of its many. <bookmark mark='c'/> So the longer a wrong answer is, the less it is punished per token, "
            "and lengths drift upward for reasons that have nothing to do with thinking. They called their fix "
            "Doctor GRPO: drop the division by length, and also the division by the group's spread, which gives extra "
            "weight to questions that are nearly always right, or nearly always wrong."
        ) as vo:
            self.play(FadeIn(cite_), FadeIn(sch))
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            self.play(FadeIn(short[0]), LaggedStart(*[GrowArrow(a_) for a_ in short[1]], lag_ratio=0.1), FadeIn(sl))
            self.play(FadeIn(long_[0]), LaggedStart(*[GrowArrow(a_) for a_ in long_[1]], lag_ratio=0.05), FadeIn(ll))
            vo.wait_until("c")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        rows = [
            ("dr", r"Dr.~GRPO \ (Sea AI Lab, \ March 2025)", r"\hat A = r - \bar r, \quad \tfrac{1}{\text{const}} "
             r"\textstyle\sum_t \ \text{not} \ \tfrac{1}{|o_i|}\sum_t", r"no length bias, \\ no difficulty bias"),
            ("dapo", r"DAPO \ (ByteDance, \ March 2025)", r"\operatorname{clip}(\rho,\ 1 - 0.2,\ 1 + 0.28)",
             r"clip higher; \ drop groups with no signal; \\ every token weighs the same"),
            ("gspo", r"GSPO \ (Qwen, \ July 2025)", r"s_i = \Big(\frac{\pi_\theta(o_i)}{\pi_{\mathrm{old}}(o_i)}\Big)^{1/|o_i|}",
             r"one ratio per answer, \\ clipped as a whole"),
            ("cispo", r"CISPO \ (MiniMax, \ June 2025)", r"\operatorname{sg}\big(\min(\rho, 1 + \varepsilon)\big)\,"
             r"\hat A\, \nabla\log\pi", r"clip the weight, \ not the update: \\ every token keeps a gradient"),
        ]
        tab = VGroup()
        for i, (k, name, eq, note_) in enumerate(rows):
            y = 2.3 - i * 1.25
            tab.add(VGroup(label(name, font_size=22, color=COLS[k]).move_to([-6.7, y, 0], aligned_edge=LEFT),
                           MathTex(eq, font_size=28).move_to([-2.4, y, 0], aligned_edge=LEFT),
                           label(note_, font_size=19, color=GREY_A).move_to([3.3, y, 0], aligned_edge=LEFT)))
        for r_ in tab:
            if r_[1].get_right()[0] > r_[2].get_left()[0] - 0.2:
                r_[1].scale((r_[2].get_left()[0] - 0.2 - r_[1].get_left()[0]) / r_[1].width, about_edge=LEFT)
        gm = MathTex(r"\sqrt[3]{2 \times \tfrac{1}{2} \times 1} = 1", font_size=32, color=C.ATTN)
        gmc = gloss(r"geometric mean", r"multiply the $n$ ratios, \ take the $n$-th root: \\ a doubling and a halving "
                    r"cancel", picture=gm, corner=DR, width=4.2, color=C.ATTN)
        cite_ = cite(r"Q.~Yu et al., \textit{DAPO} (2025); \ C.~Zheng et al., \textit{GSPO} (2025); \ MiniMax, "
                     r"\textit{MiniMax-M1} (2025)", corner=DL)
        with self.voiceover(
            "Three more variants followed within months. <bookmark mark='a'/> Doctor GRPO, as we just saw: no division "
            "by length or by spread. <bookmark mark='b'/> DAPO, from ByteDance and Tsinghua, lets the clip go higher "
            "above than below, so unlikely good tokens can grow; it throws away groups that carry no signal; and it "
            "weighs every token in the batch equally. <bookmark mark='c'/> GSPO, from the Qwen team, takes one ratio "
            "per answer instead of per token: the geometric mean of its tokens' ratios. <bookmark mark='g'/> Multiply "
            "the ratios together and take the root, one per token, so a token that doubled and one that halved cancel "
            "out. It made reinforcement learning of their mixture-of-experts models stable. <bookmark mark='d'/> "
            "And CISPO, from MiniMax, clips the importance weight itself and treats it as a constant, so every token "
            "keeps its gradient, even the rare ones the PPO clip would silence. In MiniMax's own comparison it matched "
            "DAPO in half the steps."
        ) as vo:
            self.play(FadeIn(cite_))
            for i, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(tab[i], shift=RIGHT * 0.2))
            vo.wait_until("g")
            self.play(FadeIn(gmc))
            vo.wait_until("d")
            self.play(FadeOut(gmc), run_time=0.4)
            self.play(FadeIn(tab[3], shift=RIGHT * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def results(self):
        o = load("objectives")
        V = [v for v in o["variants"] if v != "dpo"]
        steps = int(o["steps"])
        accs = {v: np.asarray(o[f"{v}_curves"])[:, -1, 1] for v in V}
        acc0 = float(np.asarray(o["pg_curves"])[0, 0, 1])
        drawn = {v: float(np.nanmean(np.asarray(o[f"{v}_drawn"], float))) / int(o["Q"]) for v in V}
        bw = 0.75
        base_y, Hh = -2.3, 4.2
        bars = VGroup()
        for j, v in enumerate(V):
            a = accs[v]
            x = -4.4 + j * 1.35
            h = Hh * float(a.mean())
            b = Rectangle(width=bw, height=h, stroke_width=0, fill_color=COLS[v], fill_opacity=0.85)
            b.move_to([x, base_y + h / 2, 0])
            wk = Line([x, base_y + Hh * a.min(), 0], [x, base_y + Hh * a.max(), 0], color=WHITE, stroke_width=2.5)
            val = MathTex(rf"{100 * a.mean():.0f}\%", font_size=22, color=COLS[v]).next_to(wk, UP, buff=0.08)
            nm = label(NAMES[v], font_size=18, color=COLS[v]).next_to([x, base_y, 0], DOWN, buff=0.15)
            bars.add(VGroup(b, wk, val, nm))
        start = DashedLine([-5.0, base_y + Hh * acc0, 0], [-4.4 + (len(V) - 1) * 1.35 + 0.6, base_y + Hh * acc0, 0],
                           dash_length=0.06, stroke_width=1.5, color=GREY_B)
        sl = label(rf"start: \ ${100 * acc0:.0f}\%$", font_size=18, color=GREY_B).next_to(start, RIGHT, buff=0.1)
        head = label(rf"right after ${steps}$ steps, \ same start, \ ${int(o['seeds'])}$ runs each \ "
                     r"(line: lowest to highest)", font_size=22, color=GREY_A).to_edge(UP, buff=0.4)
        cost = label(rf"DAPO drew ${drawn['dapo']:.2f}\times$ the questions \\ to fill its batches", font_size=20,
                     color=C.BITS).move_to([5.0, 1.6, 0])
        means = {v: float(accs[v].mean()) for v in V}
        best = max(V, key=lambda v: means[v])
        spread = 100 * (max(means.values()) - min(means.values()))
        seed_spread = 100 * max(float(accs[v].max() - accs[v].min()) for v in V)
        if spread < seed_spread:
            verdict = (f"The best average is {SAY[best]}'s, {100 * means[best]:.0f} percent, but the averages span "
                       f"only {spread:.0f} points, less than the {seed_spread:.0f} points between runs of the same "
                       "method. On a problem this small they mostly agree; the differences show at scale, over long "
                       "answers and thousands of steps.")
        else:
            verdict = (f"The best average is {SAY[best]}'s, {100 * means[best]:.0f} percent, and the averages span "
                       f"{spread:.0f} points, more than the {seed_spread:.0f} points between runs of the same method.")
        with self.voiceover(
            "We ran all of them on our addition model, from the same start, on the same kind of questions, three runs "
            f"each. <bookmark mark='a'/> {verdict} <bookmark mark='b'/> One cost the bars hide: DAPO's dynamic "
            f"sampling drew {drawn['dapo']:.2f} times as many questions to fill its batches. A fair comparison counts "
            "samples, not steps."
        ) as vo:
            self.play(FadeIn(head), Create(start), FadeIn(sl))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b_[0], DOWN), FadeIn(b_[3])) for b_ in bars],
                                  lag_ratio=0.12), run_time=2.0)
            self.play(*[FadeIn(b_[1]) for b_ in bars], *[FadeIn(b_[2]) for b_ in bars])
            vo.wait_until("b")
            self.play(FadeIn(cost), Indicate(bars[V.index("dapo")], color=C.BITS))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def signal(self):
        o = load("objectives")
        steps = int(o["steps"])
        z = np.asarray(o["pg_zero"], float)
        w = 20
        zs = np.array([z[max(0, i - w + 1):i + 1].mean() for i in range(len(z))])
        g = axes([0, steps], [0, 1], x_length=6.0, y_length=3.6, xlabel=r"RL steps \ (the plain group gradient; \ "
                 r"average of $20$ steps, \ $3$ runs)", ylabel=r"groups whose $8$ answers all agree: \ no signal",
                 xticks=[0, steps], yticks=[0, 0.5, 1], yfmt=lambda v: rf"{int(100 * v)}\%", center=[-2.6, -0.4, 0])
        ln = curve(g.ax, np.arange(1, len(zs) + 1), zs, WRONG_C, 3.5)
        eq = MathTex(r"\hat A_i = 0 \ \text{ for every } i \ \Rightarrow\ \nabla J = 0", font_size=32).move_to([3.9, 1.8, 0])
        dr = np.asarray(o["dapo_drawn"], float) / int(o["Q"])
        dds = np.array([dr[max(0, i - w + 1):i + 1].mean() for i in range(len(dr))])
        dtop = max(2, math.ceil(float(dds.max()) - 1e-9))
        h = axes([0, steps], [0, dtop + 0.3], x_length=4.0, y_length=1.5, ylabel=r"DAPO: \ questions drawn per step, "
                 r"\\ as a multiple of the $32$ it trains on", yticks=[1, dtop], yfmt=lambda v: rf"{int(v)}\times",
                 center=[4.0, -1.5, 0], font_size=16)
        cone = DashedLine(h.ax.c2p(0, 1), h.ax.c2p(steps, 1), dash_length=0.05, stroke_width=1, color=GREY_D)
        cln = curve(h.ax, np.arange(1, len(dds) + 1), dds, C.BITS, 3)
        with self.voiceover(
            "One of DAPO's fixes is worth seeing. When all eight answers to a question are right, every advantage "
            "is zero, and so is the gradient: the question was wasted. <bookmark mark='a'/> As the model improves, "
            f"that happens more and more: by the end, {100 * zs[-1]:.0f} percent of the groups taught it nothing. "
            "<bookmark mark='b'/> DAPO keeps sampling questions until each batch is full of groups that disagree; "
            f"by the end it needed {dds[-1]:.1f} times as many."
        ) as vo:
            self.play(FadeIn(g), Write(eq))
            vo.wait_until("a")
            self.play(Create(ln), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(h), Create(cone))
            self.play(Create(cln), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def offline(self):
        o = load("objectives")
        C_ = np.asarray(o["dpo_curves"])
        acc0, acc = float(C_[0, 0, 1]), float(C_[:, -1, 1].mean())
        mv = np.asarray(o["dpo_moves"])
        steps = int(o["steps"])
        lo = math.floor(min(mv[:, 1].min(), mv[:, 2].min()))
        hi = max(1, math.ceil(max(mv[:, 1].max(), mv[:, 2].max())))
        g = axes([0, steps], [lo, hi], x_length=5.6, y_length=3.4, xlabel=r"DPO steps",
                 ylabel=r"change in $\log_2 p$, \ on pairs held out", xticks=[0, steps],
                 yticks=list(range(lo, hi + 1)), yfmt=lambda v: f"{int(v):+d}" if v else "0", center=[-2.6, -0.5, 0])
        zero = DashedLine(g.ax.c2p(0, 0), g.ax.c2p(steps, 0), dash_length=0.06, stroke_width=1.5, color=GREY_B)
        cw, cl = curve(g.ax, mv[:, 0], mv[:, 1], RIGHT_C, 3.5), curve(g.ax, mv[:, 0], mv[:, 2], WRONG_C, 3.5)
        lg = legend([(RIGHT_C, r"the right answers \ (chosen)"), (WRONG_C, r"the wrong ones \ (rejected)")],
                    font_size=20).next_to(g, RIGHT, buff=0.4).shift(UP * 0.8)
        res = label(rf"${int(o['dpo_n_pairs']):,}$ pairs from the starting model: \\ right on new questions \ "
                    rf"${100 * acc0:.0f}\% \to {100 * acc:.0f}\%$ \ (mean of ${int(o['seeds'])}$ runs)".replace(",", "{,}"),
                    font_size=22, color=C.SURPRISE).next_to(lg, DOWN, buff=0.5).align_to(lg, LEFT)
        both_down = mv[-1, 1] < -0.1 and mv[-1, 2] < mv[-1, 1]
        if acc < acc0 - 0.02:
            how = f"It got worse: from {100 * acc0:.0f} to {100 * acc:.0f} percent right."
        else:
            how = f"It went from {100 * acc0:.0f} to {100 * acc:.0f} percent right."
        if both_down:
            why_ = ("Watch the log-probabilities on pairs it never trained on: the loss only asks the right answer to "
                    "rise relative to the wrong one, and the easiest way there was to push both down, the wrong one "
                    "faster. The probability went somewhere else, mostly to other wrong answers: Part 27's likelihood "
                    "displacement.")
        else:
            why_ = ("On pairs it never trained on, the right answers rise and the wrong ones fall, as the loss asks; but "
                    "the pairs came from the starting model, and they stop being informative as the model moves.")
        cite_ = cite(r"R.~Rafailov et al., \textit{DPO} (2023): \ derived in Part 27", corner=DR)
        with self.voiceover(
            "And the offline alternative? Part 27 derived DPO, which learns from fixed pairs of a better and a worse "
            "answer, with no sampling during training. We gave it pairs of one right and one wrong answer, drawn once "
            f"from the starting model. <bookmark mark='a'/> {how} <bookmark mark='b'/> {why_} <bookmark mark='c'/> "
            "With a checker at hand, sampling from the model you are improving, on-policy, is what keeps paying."
        ) as vo:
            self.play(FadeIn(cite_), FadeIn(g), Create(zero))
            vo.wait_until("a")
            self.play(FadeIn(res))
            vo.wait_until("b")
            self.play(Create(cw), Create(cl), FadeIn(lg), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()
