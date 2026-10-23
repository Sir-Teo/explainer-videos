from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai10.common import (ATT, CELL_NAME, CELLS, HIST, LSTMC, MINC, PART, load, pct, sci_tex)
from videos.ai.ai10.specs import MINRNN


class Return(VoiceoverScene):
    def construct(self):
        self.card()
        self.why_lost()
        self.scan()
        self.measured()
        self.mingru()
        self.family()

    def card(self):
        card = chapter_card(16, r"Recurrence returns", r"Can a recurrent network train as fast as a transformer?",
                            lit=(2017,), part=PART)
        with self.voiceover("Chapter sixteen. Recurrence returns."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def why_lost(self):
        T = 8
        rnn = VGroup(*[Circle(radius=0.22, stroke_color=LSTMC, stroke_width=2, fill_color=LSTMC, fill_opacity=0.15)
                       for _ in range(T)]).arrange(RIGHT, buff=0.45).move_to([-3.2, 1.3, 0])
        ra = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.04, stroke_width=2, color=LSTMC,
                            max_tip_length_to_length_ratio=0.3) for a, b in zip(rnn, rnn[1:])])
        rl = label(r"a recurrent network: \ step $t$ waits for step $t-1$", font_size=22, color=LSTMC)
        rl.next_to(rnn, UP, buff=0.25)
        att = VGroup(*[Circle(radius=0.22, stroke_color=ATT, stroke_width=2, fill_color=ATT, fill_opacity=0.15)
                       for _ in range(T)]).arrange(RIGHT, buff=0.45).move_to([-3.2, -1.2, 0])
        aa = VGroup(*[Line(att[i].get_top(), att[j].get_top() + UP * 0.0, stroke_width=1, color=ATT,
                           stroke_opacity=0.35).set_points_smoothly([att[i].get_top(),
                                                                     (att[i].get_top() + att[j].get_top()) / 2 +
                                                                     UP * 0.2 * (j - i), att[j].get_top()])
                      for j in range(T) for i in range(j)])
        al = label(r"attention: \ every position at once", font_size=22, color=ATT).next_to(att, UP, buff=0.9)
        cmp = VGroup(label(r"training: \ $T$ steps in a row \ vs.\ one parallel step", font_size=22, color=GREY_A),
                     label(r"generating: \ a fixed-size memory \ vs.\ a cache that grows with $T$ \ (Part 15)",
                           font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        cmp.move_to([3.3, 0.1, 0])
        if cmp.width > 6.6:
            cmp.width = 6.6
        tag = note(r"schematic").to_corner(DR, buff=0.3)
        with self.voiceover(
            "After 2017 the Transformer took over, and the reason was training speed. <bookmark mark='a'/> A "
            "recurrent network must compute step t after step t minus one: a thousand-token sequence is a "
            "thousand steps in a row, and a GPU with thousands of lanes mostly waits. <bookmark mark='b'/> "
            "Attention computes every position at once. <bookmark mark='c'/> But at generation time the "
            "bargain reverses. A recurrent network carries a fixed-size memory from token to token; a "
            "transformer keeps every past token's keys and values, a cache that grows with the text. "
            "So the question came back: can a recurrent network be trained in parallel?"
        ) as vo:
            self.play(FadeIn(tag), LaggedStart(*[FadeIn(c) for c in rnn], lag_ratio=0.2))
            vo.wait_until("a")
            self.play(FadeIn(rl), LaggedStart(*[GrowArrow(a_) for a_ in ra], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(att), FadeIn(al), Create(aa), run_time=1.0)
            vo.wait_until("c")
            self.play(FadeIn(cmp, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def scan(self):
        colors = {r"a_t": MINC, r"b_t": LSTMC, r"a'": MINC, r"b'": LSTMC}
        rows = [
            cmath(r"h_t", r"=", r"a_t", r"\odot", r"h_{t-1}", r"+", r"b_t", colors=colors, font_size=38),
            cmath(r"h_{t+1}", r"=", r"a_{t+1} a_t", r"\odot", r"h_{t-1}", r"+", r"(a_{t+1} b_t + b_{t+1})",
                  font_size=38),
            cmath(r"(a, b) \circ (a', b')", r"=", r"(a a',\; a' b + b')", colors=colors, font_size=38),
        ]
        whys = [why(r"a linear recurrence: \ $a_t$, $b_t$ depend on the input only"),
                why(r"two steps make one step of the same form"),
                why(r"and $\circ$ is associative: \ the order of combining doesn't matter")]
        step = ladder(self, rows, whys, keep=3, top=3.0, x=-2.2, align_index=1, edge=6.8)
        # Hillis-Steele for T = 8
        T = 8
        cols = [Dot([-3.5 + 1.0 * t, 0.0 - 0.0, 0], radius=0.07, color=GREY_B) for t in range(T)]
        lv = []
        dots = VGroup()
        arrows = VGroup()
        for r in range(4):
            y = -0.4 - 0.85 * r
            row = VGroup(*[Dot([-3.5 + 1.0 * t, y, 0], radius=0.08, color=MINC if r else GREY_B) for t in range(T)])
            dots.add(row)
            lv.append(row)
        for r in range(1, 4):
            d = 2 ** (r - 1)
            for t in range(T):
                arrows.add(Line(lv[r - 1][t].get_center(), lv[r][t].get_center(), stroke_width=1.2, color=GREY_D))
                if t - d >= 0:
                    arrows.add(Line(lv[r - 1][t - d].get_center(), lv[r][t].get_center(), stroke_width=2,
                                    color=MINC))
        rl = VGroup(*[label(t, font_size=18, color=GREY_B).next_to(lv[r], LEFT, buff=0.3) for r, t in
                      enumerate([r"inputs", r"round 1: \ distance 1", r"round 2: \ distance 2",
                                 r"round 3: \ distance 4"])])
        res = label(r"$T = 8$: \ every $h_t$ after $\log_2 8 = 3$ rounds", font_size=22, color=MINC)
        res.next_to(dots, RIGHT, buff=0.5)
        if res.get_right()[0] > 6.9:
            res.next_to(dots, DOWN, buff=0.2)
        cite_ = cite(r"Blelloch (1990); \ Martin \& Cundy (2018)", corner=DR)
        _ = cols
        with self.voiceover(
            "It can, if the recurrence is linear. <bookmark mark='a'/> Suppose the new state is the old one, "
            "multiplied elementwise by a, plus b, where a and b depend only on the current input. "
            "<bookmark mark='b'/> Then two steps together are again one step of the same form, with a times a "
            "prime and a prime b plus b prime. <bookmark mark='c'/> That combining rule is associative, and any "
            "associative operation over a sequence can be computed by a parallel prefix scan, the algorithm Guy "
            "Blelloch made famous in 1990. <bookmark mark='d'/> Combine neighbours, then pairs two apart, then "
            "four apart: after log two of T rounds, every position has its state. A thousand steps become ten "
            "rounds."
        ) as vo:
            self.add(cite_)
            step(0)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            step(2, transform=False)
            vo.wait_until("d")
            self.play(FadeIn(dots[0]), FadeIn(rl[0]))
            for r in range(1, 4):
                seg = [a for a in arrows if abs(a.get_end()[1] - lv[r][0].get_y()) < 1e-6]
                self.play(LaggedStart(*[Create(a) for a in seg], lag_ratio=0.02), FadeIn(dots[r]), FadeIn(rl[r]),
                          run_time=0.9)
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measured(self):
        s = load("scan")
        rows = s["rows"]
        ax = axes([5.5, 16.5], [-1.5, 3.5], x_length=6.0, y_length=3.8, xlabel=r"sequence length $T$",
                  ylabel=r"time, \ milliseconds", xticks=[6, 8, 10, 12, 14, 16], xfmt=lambda v: f"2^{{{int(v)}}}",
                  yticks=[-1, 0, 1, 2, 3], yfmt=lambda v: {-1: "0.1", 0: "1", 1: "10", 2: "100", 3: r"1{,}000"}[int(v)],
                  center=[-2.6, -0.3, 0])
        A = ax.ax
        out = VGroup()
        for d, dash in ((8, False), (256, True)):
            rr = [r for r in rows if r["d"] == d]
            x = [math.log2(r["T"]) for r in rr]
            ys = [math.log10(max(r["seq"] * 1e3, 0.03)) for r in rr]
            yp = [math.log10(max(r["par"] * 1e3, 0.03)) for r in rr]
            a = curve(A, x, ys, LSTMC, 3.5)
            b = curve(A, x, yp, MINC, 3.5)
            if dash:
                a, b = DashedVMobject(a, num_dashes=24), DashedVMobject(b, num_dashes=24)
            out.add(VGroup(a, b))
        leg = legend([(LSTMC, r"step by step"), (MINC, r"parallel scan")], font_size=22).to_corner(UR, buff=0.5)
        kl = label(r"solid: \ a state of $8$ numbers; \ dashed: \ $256$", font_size=20, color=GREY_B)
        kl.next_to(leg, DOWN, buff=0.25).align_to(leg, LEFT)
        keep_in_frame(kl)
        err = max(r["err"] for r in rows)
        big8 = max((r for r in rows if r["d"] == 8), key=lambda r: r["T"])
        big256 = max((r for r in rows if r["d"] == 256), key=lambda r: r["T"])
        facts = VGroup(label(rf"largest difference between the two: \ ${sci_tex(err)}$", font_size=20, color=GREY_A),
                       label(rf"${big8['T']:,}$ steps: \ ${big8['rounds']}$ rounds".replace(",", "{,}"),
                             font_size=20, color=MINC)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        facts.next_to(kl, DOWN, buff=0.4).align_to(kl, LEFT)
        keep_in_frame(facts)
        tag = note(r"computed: \ this computer, \ numpy").to_corner(DR, buff=0.2)
        w8 = big8["seq"] / big8["par"]
        w256 = big256["seq"] / big256["par"]
        v8 = (f"With a narrow state, eight numbers, the scan is {w8:.1f} times faster at {big8['T']:,} steps."
              if w8 > 1.2 else
              f"With a narrow state the scan is about as fast as the loop, {w8:.1f} times.")
        v256 = (f"With a wide state, 256 numbers, it is {1 / w256:.1f} times slower: the scan does log T times the "
                "work, and this computer has only a few cores to spread it over." if w256 < 0.8 else
                f"With a wide state, 256 numbers, the two are close: {w256:.1f} times.")
        with self.voiceover(
            "We tried it on the computer making this video. <bookmark mark='a'/> The scan and the step-by-step "
            "loop give the same states, to rounding error. <bookmark mark='b'/> " + v8 + " <bookmark mark='c'/> "
            + v256 + " The scan trades extra arithmetic for fewer steps in a row, which pays off on hardware "
            "with thousands of lanes: on a GPU, Leo Feng and colleagues measured their scanned recurrent "
            f"networks training {MINRNN['gru512']} times faster than a GRU at length 512, and "
            f"{MINRNN['gru4096']:,} times faster at length 4,096."
        ) as vo:
            self.play(Create(ax), FadeIn(leg), FadeIn(kl), FadeIn(tag))
            self.play(Create(out[0]), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(facts[0]))
            vo.wait_until("b")
            self.play(FadeIn(facts[1]), Indicate(out[0], color=WHITE))
            vo.wait_until("c")
            self.play(Create(out[1]), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mingru(self):
        m = load("memory")
        Ts = [int(t) for t in m["T"]]
        runs = m["runs"]
        card = definition_card(r"minGRU (Feng, Tung, Ahmed, Bengio \& Hajimirsadeghi, 2024)",
                               VGroup(MathTex(r"z_t = \sigma(W_z x_t), \quad \tilde h_t = W_h x_t", font_size=30,
                                              color=MINC),
                                      MathTex(r"h_t = (1 - z_t) \odot h_{t-1} + z_t \odot \tilde h_t", font_size=32,
                                              color=MINC)).arrange(DOWN, aligned_edge=LEFT, buff=0.15),
                               width=7.0, color=MINC).to_corner(UL, buff=0.35)
        nl = label(r"the GRU, with $h_{t-1}$ taken out of the gates: \ $a_t = 1 - z_t$, \ $b_t = z_t \odot "
                   r"\tilde h_t$", font_size=20, color=GREY_A).next_to(card, DOWN, buff=0.2).align_to(card, LEFT)
        cells = ("rnn", "lstm", "gru", "mingru")
        bars, newb = VGroup(), VGroup()
        for j, T in enumerate(Ts):
            for k, c in enumerate(cells):
                vals = [runs[f"{c}-{T}-{s}"]["final"] for s in (0, 1, 2)]
                v = float(np.mean(vals))
                h = max(2.6 * v, 0.03)
                x = -4.6 + 3.3 * j + 0.52 * k
                b = Rectangle(width=0.44, height=h, stroke_width=0, fill_color=CELLS[c], fill_opacity=0.85)
                b.move_to([x, -2.6 + h / 2, 0])
                dots = VGroup(*[Dot([x, -2.6 + 2.6 * fv, 0], radius=0.04, color=WHITE) for fv in vals])
                (newb if c == "mingru" else bars).add(VGroup(b, dots))
            bars.add(MathTex(rf"T = {T}", font_size=24, color=GREY_A).move_to([-4.6 + 3.3 * j + 0.78, -2.95, 0]))
        base = Line([-5.1, -2.6, 0], [4.6, -2.6, 0], color=GREY_C, stroke_width=1.5)
        leg = legend([(CELLS[c], CELL_NAME[c]) for c in cells], font_size=22).to_corner(UR, buff=0.4)
        bl = label(r"the memory task of Chapter 12: \ final accuracy", font_size=22, color=GREY_A)
        bl.move_to([-0.3, 0.6, 0])
        tag = note(r"computed: \ three seeds; \ minGRU trained through the scan").to_corner(DR, buff=0.2)
        mg = float(np.mean([runs[f"mingru-{Ts[-1]}-{s}"]["final"] for s in (0, 1, 2)]))
        rn = float(np.mean([runs[f"rnn-{Ts[-1]}-{s}"]["final"] for s in (0, 1, 2)]))
        ls = float(np.mean([runs[f"lstm-{Ts[-1]}-{s}"]["final"] for s in (0, 1, 2)]))
        if mg > 0.9:
            v = (f"On our memory task, at {Ts[-1]} steps, minGRU gets {pct(mg, 0)} percent right, with the LSTM "
                 f"at {pct(ls, 0)}, and the plain network at {pct(rn, 0)}. The gate learned from the input alone "
                 "is enough: open for the marked symbol, shut for everything after.")
        else:
            v = (f"On our memory task, at {Ts[-1]} steps, minGRU gets {pct(mg, 0)} percent right, the LSTM "
                 f"{pct(ls, 0)}, the plain network {pct(rn, 0)}.")
        with self.voiceover(
            "In 2024 Leo Feng, Yoshua Bengio and colleagues asked whether the LSTM and the GRU needed their "
            "nonlinear recurrence at all. <bookmark mark='a'/> Take the GRU and let its gate and its candidate see "
            "only the current input, not the previous state. What's left is exactly a linear recurrence, so it "
            "trains with a scan. They called it minGRU, and found it competitive on their tasks. "
            "<bookmark mark='b'/> We trained one, through the scan, beside the others. " + v
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2), Create(base), FadeIn(leg), FadeIn(bl), FadeIn(tag),
                      LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.04), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(nl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in newb], lag_ratio=0.3), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def family(self):
        items = [(2016, r"QRNN", r"Bradbury et al."), (2017, r"SRU", r"Lei et al."),
                 (2021, r"S4", r"Gu, Goel \& R\'e"), (2023, r"LRU", r"Orvieto et al."),
                 (2023, r"RWKV", r"Peng et al."), (2023, r"Mamba", r"Gu \& Dao"),
                 (2024, r"xLSTM", r"Beck et al.; \ a 7B model in 2025"), (2024, r"minGRU, minLSTM", r"Feng et al.")]
        cards = VGroup(*[history_card(y, n, w, width=3.1, color=MINC if n.startswith(("min", "xLSTM")) else HIST,
                                      font_size=19) for y, n, w in items])
        cards.arrange_in_grid(rows=2, cols=4, buff=(0.2, 0.3)).move_to(UP * 0.3)
        if cards.width > 13.4:
            cards.width = 13.4
        foot = label(r"today's hybrids mix them with attention: \ Part 15", font_size=26, color=ATT)
        foot.to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "minGRU joined a family growing since 2016. <bookmark mark='a'/> Quasi-recurrent networks and simple "
            "recurrent units moved the matrices out of the recurrence; state-space models, from S4 in 2021 to "
            "Mamba in 2023, built linear recurrences that let the input choose what "
            "to keep; and in 2024 Hochreiter's own group returned with xLSTM, scaled in 2025 to seven billion "
            "parameters. <bookmark mark='b'/> Several of today's open models mix such layers with attention: the "
            "transformer's recall, the recurrence's fixed-size memory. That's Part 15."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cards], lag_ratio=0.25), run_time=5.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()


_ = (HIST, LSTMC)
