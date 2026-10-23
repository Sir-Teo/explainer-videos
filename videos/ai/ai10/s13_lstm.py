from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai10.common import (CELL_NAME, CELLC, CELLS, GATEC, GRADC, GRUC, HIST, LSTMC, PART, RNNC, load,
                                   pct, seed_band)


class LSTM(VoiceoverScene):
    def construct(self):
        self.card()
        self.carousel()
        self.cell()
        self.derivation()
        self.gru()
        self.task()
        self.results()
        self.gradients()

    def card(self):
        card = chapter_card(12, r"LSTM and GRU", r"How do you build a memory that gradients can cross?", lit=(1997,),
                            part=PART)
        with self.voiceover("Chapter twelve. LSTM and GRU."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def carousel(self):
        hc = history_card(1997, r"Sepp Hochreiter \& J\"urgen Schmidhuber", r"\textit{Long Short-Term Memory}, \ "
                          r"Neural Computation", width=5.4, color=HIST).to_corner(UL, buff=0.4)
        unit = Circle(radius=0.6, stroke_color=CELLC, stroke_width=3, fill_color=CELLC, fill_opacity=0.15)
        unit.move_to([-2.8, -0.2, 0])
        ul = MathTex(r"c", font_size=40, color=CELLC).move_to(unit)
        loop = CurvedArrow(unit.get_top() + LEFT * 0.25, unit.get_top() + RIGHT * 0.25, angle=-4.2, color=CELLC,
                           stroke_width=3)
        one = MathTex(r"\times 1", font_size=32, color=CELLC).next_to(loop, UP, buff=0.1)
        eq = cmath(r"c_t = c_{t-1} + \text{(what is written)}", font_size=34).next_to(unit, DOWN, buff=0.6)
        eq2 = cmath(r"\frac{\partial c_t}{\partial c_{t-1}} = 1", font_size=40, color=CELLC).next_to(eq, DOWN, buff=0.3)
        gates = VGroup(label(r"an input gate decides what is written", font_size=24, color=GATEC),
                       label(r"an output gate decides what is read", font_size=24, color=GATEC),
                       label(r"a forget gate decides what is erased \ (Gers, Schmidhuber \& Cummins, 2000)",
                             font_size=24, color=GATEC)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        if gates.width > 6.0:
            gates.width = 6.0
        gates.to_edge(RIGHT, buff=0.4).set_y(-0.6)
        with self.voiceover(
            "The cure came from Hochreiter himself, with Jurgen Schmidhuber, in 1997. <bookmark mark='a'/> If "
            "every step multiplies the gradient by something less than one, build a unit where it multiplies by "
            "exactly one: a memory cell connected to itself with weight one, and no squashing. "
            "<bookmark mark='b'/> An error signal can ride it back across any number of steps without fading: the "
            "constant error carousel. <bookmark mark='c'/> Around it, learned gates decide when to write to the "
            "cell and when to read it; in 2000 Felix Gers added a forget gate, to clear it."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(unit), FadeIn(ul), Create(loop), FadeIn(one))
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(Write(eq2))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(g, shift=LEFT * 0.1) for g in gates], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cell(self):
        y_belt = 1.2
        belt = Arrow([-6.4, y_belt, 0], [6.4, y_belt, 0], buff=0, color=CELLC, stroke_width=6,
                     max_tip_length_to_length_ratio=0.02)
        bl = label(r"the cell state $c$: \ the memory line", font_size=22, color=CELLC).next_to(belt, UP, buff=0.1)
        bl.align_to(belt, LEFT).shift(RIGHT * 0.3)
        mul = VGroup(Circle(radius=0.28, stroke_color=GATEC, stroke_width=2.5, fill_color="#0B0F17", fill_opacity=1),
                     MathTex(r"\times", font_size=30, color=GATEC)).move_to([-2.0, y_belt, 0])
        add = VGroup(Circle(radius=0.28, stroke_color=GATEC, stroke_width=2.5, fill_color="#0B0F17", fill_opacity=1),
                     MathTex(r"+", font_size=30, color=GATEC)).move_to([1.0, y_belt, 0])
        gates = VGroup()
        for x, t in ((-2.0, r"f_t"), (0.2, r"i_t"), (1.8, r"g_t"), (3.8, r"o_t")):
            b = RoundedRectangle(width=0.8, height=0.6, corner_radius=0.1, stroke_color=GATEC if t != "g_t" else LSTMC,
                                 stroke_width=2, fill_color=GATEC, fill_opacity=0.12).move_to([x, -0.6, 0])
            gates.add(VGroup(b, MathTex(t, font_size=28, color=GATEC if t != "g_t" else LSTMC).move_to(b)))
        inp = Line([-5.4, -1.9, 0], [5.0, -1.9, 0], color=GREY_B, stroke_width=3)
        il = MathTex(r"[h_{t-1}, x_t]", font_size=28, color=GREY_A).next_to(inp, DOWN, buff=0.1).align_to(inp, LEFT)
        ups = VGroup(*[Line([g.get_x(), -1.9, 0], g.get_bottom(), color=GREY_B, stroke_width=2) for g in gates])
        f_up = Arrow(gates[0].get_top(), mul.get_bottom(), buff=0.05, color=GATEC, stroke_width=2.5)
        prod = VGroup(Circle(radius=0.22, stroke_color=GATEC, stroke_width=2, fill_color="#0B0F17", fill_opacity=1),
                      MathTex(r"\times", font_size=24, color=GATEC)).move_to([1.0, 0.25, 0])
        ig = Line(gates[1].get_top(), prod.get_left(), color=GATEC, stroke_width=2)
        gg = Line(gates[2].get_top(), prod.get_right(), color=LSTMC, stroke_width=2)
        p_up = Arrow(prod.get_top(), add.get_bottom(), buff=0.05, color=GATEC, stroke_width=2.5)
        tanh = VGroup(RoundedRectangle(width=0.9, height=0.5, corner_radius=0.1, stroke_color=CELLC, stroke_width=2),
                      MathTex(r"\tanh", font_size=24, color=CELLC)).move_to([3.8, 0.4, 0])
        tanh[1].move_to(tanh[0])
        down = Line([3.8, y_belt, 0], tanh.get_top(), color=CELLC, stroke_width=2)
        outm = VGroup(Circle(radius=0.22, stroke_color=GATEC, stroke_width=2, fill_color="#0B0F17", fill_opacity=1),
                      MathTex(r"\times", font_size=24, color=GATEC)).move_to([4.9, -0.2, 0])
        o_l = Line(gates[3].get_right(), outm.get_bottom(), color=GATEC, stroke_width=2)
        t_l = Line(tanh.get_right(), outm.get_top(), color=CELLC, stroke_width=2)
        h_out = Arrow(outm.get_right(), [6.4, -0.2, 0], buff=0.05, color=LSTMC, stroke_width=3)
        hl = MathTex(r"h_t", font_size=30, color=LSTMC).next_to(h_out, UP, buff=0.05)
        eqs = VGroup(MathTex(r"c_t = f_t \odot c_{t-1} + i_t \odot g_t", font_size=32, color=CELLC),
                     MathTex(r"h_t = o_t \odot \tanh(c_t)", font_size=32, color=LSTMC),
                     MathTex(r"f_t, i_t, o_t = \sigma(\cdot), \quad g_t = \tanh(\cdot)", font_size=28,
                             color=GATEC)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UL, buff=0.3)
        token = Dot([-6.2, y_belt, 0], radius=0.12, color=WHITE)
        tag = note(r"schematic: \ one LSTM cell").to_corner(DR, buff=0.25)
        with self.voiceover(
            "Here is the cell as it is used today. <bookmark mark='a'/> Running straight through it, the cell "
            "state: a conveyor belt of memory. <bookmark mark='b'/> The forget gate, a number between zero and one "
            "for every slot, multiplies the belt: one keeps, zero erases. <bookmark mark='c'/> The input gate "
            "chooses how much of a new candidate g to add. <bookmark mark='d'/> The output gate chooses how much of "
            "the memory to show as the hidden state h. <bookmark mark='e'/> All three are computed from the "
            "previous hidden state and the input, so the network learns when to remember, forget and speak."
        ) as vo:
            self.play(FadeIn(eqs), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowArrow(belt), FadeIn(bl), FadeIn(token))
            self.play(token.animate.move_to([-2.4, y_belt, 0]), run_time=1.0)
            vo.wait_until("b")
            self.play(FadeIn(mul), FadeIn(inp), FadeIn(il), FadeIn(gates[0]), Create(ups[0]), GrowArrow(f_up))
            self.play(token.animate.move_to([0.6, y_belt, 0]), run_time=1.0)
            vo.wait_until("c")
            self.play(FadeIn(add), FadeIn(gates[1]), FadeIn(gates[2]), Create(ups[1]), Create(ups[2]), FadeIn(prod),
                      Create(ig), Create(gg), GrowArrow(p_up))
            self.play(token.animate.move_to([3.6, y_belt, 0]), run_time=1.0)
            vo.wait_until("d")
            self.play(FadeIn(gates[3]), Create(ups[3]), Create(down), FadeIn(tanh), FadeIn(outm), Create(o_l),
                      Create(t_l), GrowArrow(h_out), FadeIn(hl))
            vo.wait_until("e")
            self.play(token.animate.move_to([6.2, y_belt, 0]), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derivation(self):
        colors = {r"f_t": GATEC, r"\mathrm{diag}(f_t)": GATEC, r"f": GATEC}
        rows = [
            cmath(r"\frac{\partial c_t}{\partial c_{t-1}}", r"=", r"\mathrm{diag}(f_t)", r"+", r"\ldots",
                  colors=colors, font_size=38),
            cmath(r"\frac{\partial c_T}{\partial c_k}", r"\approx", r"\prod_{t=k+1}^{T} \mathrm{diag}(f_t)",
                  font_size=38),
            cmath(r"f^{\,T-k} = \tfrac12", r"\iff", r"T - k = \frac{\ln 2}{-\ln f}", font_size=38),
            cmath(r"f = 0.99", r"\Rightarrow", r"\text{about } 69 \text{ steps}", font_size=38),
        ]
        rows[1][2].set_color(GATEC)
        whys = [why(r"along the belt; \ the rest goes through the gates"),
                why(r"the product the RNN had, \ with gates in place of $W$"),
                why(r"a forget gate held at $f$: \ the memory's half-life"),
                why(r"$f = 1$: \ forever, \ the original carousel")]
        step = ladder(self, rows, whys, keep=4, top=2.6, x=-2.2, align_index=1, edge=6.8)
        with self.voiceover(
            "Why does the gradient survive? <bookmark mark='a'/> Differentiate the cell state with respect to "
            "the previous one. Along the belt, it's just the forget gate, a diagonal matrix of numbers between zero "
            "and one; the other paths run through the gates, and they are small. <bookmark mark='b'/> So back "
            "across many steps, the gradient is multiplied by the product of the forget gates, which the network "
            "learns, in place of the fixed matrix W. <bookmark mark='c'/> A forget gate held at f halves the "
            "memory every ln 2 over minus ln f steps. <bookmark mark='d'/> At 0.99, about sixty-nine steps; at "
            "exactly one, Hochreiter's original carousel, forever."
        ) as vo:
            step(0)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            step(2, transform=False)
            vo.wait_until("d")
            step(3, transform=False)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gru(self):
        card = definition_card(
            r"The gated recurrent unit (GRU)",
            VGroup(MathTex(r"z_t = \sigma(W_z [h_{t-1}, x_t]), \quad r_t = \sigma(W_r [h_{t-1}, x_t])", font_size=30,
                           color=GATEC),
                   MathTex(r"\tilde h_t = \tanh(W [r_t \odot h_{t-1}, x_t])", font_size=30, color=GRUC),
                   MathTex(r"h_t = (1 - z_t) \odot h_{t-1} + z_t \odot \tilde h_t", font_size=34, color=GRUC))
            .arrange(DOWN, aligned_edge=LEFT, buff=0.18), width=8.6, color=GRUC).move_to(UP * 0.5)
        hc = history_card(2014, r"Kyunghyun Cho and colleagues, \ Montreal", r"two gates, \ no separate cell; \ "
                          r"in tests by Chung et al.\ (2014), \ about as good as the LSTM", width=6.0,
                          color=HIST).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In 2014 Kyunghyun Cho and colleagues in Montreal simplified the cell. <bookmark mark='a'/> The gated "
            "recurrent unit keeps only the hidden state and two gates: an update gate z that blends the old state "
            "with a new candidate, the same carousel wherever z is near zero, and a reset gate. "
            "<bookmark mark='b'/> Fewer parts, and about as good, in comparisons by Junyoung Chung and colleagues."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(card, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def task(self):
        m = load("memory")
        T = 12
        g = np.random.default_rng(3)
        seq = [int(g.integers(0, 8)) for _ in range(T)]
        boxes = VGroup()
        for i in range(T):
            col = CELLC if i == 0 else (GREY_B if i < T - 1 else LSTMC)
            sq = Square(0.62, stroke_color=col, stroke_width=2.5 if i in (0, T - 1) else 1.5, fill_color=col,
                        fill_opacity=0.15 if i in (0, T - 1) else 0.04)
            t = MathTex("?" if i == T - 1 else str(seq[i]), font_size=30, color=col)
            boxes.add(VGroup(sq, t.move_to(sq)))
        boxes.arrange(RIGHT, buff=0.12).move_to(UP * 0.8)
        mark = label(r"remember this", font_size=22, color=CELLC).next_to(boxes[0], DOWN, buff=0.2)
        noise = Brace(VGroup(*boxes[1:T - 1]), UP, color=GREY_B)
        nl = label(r"$T - 2$ random distractors", font_size=22, color=GREY_B).next_to(noise, UP, buff=0.1)
        q = label(r"now answer", font_size=22, color=LSTMC).next_to(boxes[-1], RIGHT, buff=0.2)
        ans = MathTex(str(seq[0]), font_size=40, color=LSTMC).next_to(boxes[-1], DOWN, buff=0.5)
        arr = Arrow(boxes[-1].get_bottom(), ans.get_top(), buff=0.06, color=LSTMC, stroke_width=2.5)
        facts = label(rf"one symbol of $8$ \ (chance: ${100 * m['chance']:.1f}\%$); \ $T = {', '.join(str(t) for t in m['T'])}$; "
                      r"\ $64$ hidden units; \ three seeds each", font_size=24, color=GREY_A)
        facts = VGroup(facts, label(r"gated cells: \ gates started to remember for times spread up to $T$ \ "
                                    r"(chrono initialization, \ Tallec \& Ollivier, 2018)", font_size=22,
                                    color=GREY_B)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.6)
        tag = note(r"illustrative sequence").to_corner(DR, buff=0.25)
        with self.voiceover(
            "Does the carousel work? A test in the spirit of Hochreiter's: <bookmark mark='a'/> a sequence opens "
            "with one marked symbol, one of eight; <bookmark mark='b'/> then come random distractors; "
            "<bookmark mark='c'/> at the end the network must say what the first symbol was. "
            "<bookmark mark='d'/> We trained a plain "
            "recurrent network, an LSTM and a GRU, sixty-four units each, three times each, for sequences of "
            f"{m['T'][0]}, {m['T'][1]} and {m['T'][-1]} steps. The gated cells start with their gates set to "
            "remember: the chrono initialization of Corentin Tallec and Yann Ollivier."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(boxes[0]), FadeIn(mark))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in boxes[1:T - 1]], lag_ratio=0.1), GrowFromCenter(noise),
                      FadeIn(nl))
            vo.wait_until("c")
            self.play(FadeIn(boxes[-1]), FadeIn(q))
            self.play(GrowArrow(arr), FadeIn(ans))
            vo.wait_until("d")
            self.play(FadeIn(facts, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def results(self):
        m = load("memory")
        Ts = [int(t) for t in m["T"]]
        runs = m["runs"]
        Tbig = Ts[-1]
        S = int(m["steps"][str(Tbig)])
        ax = axes([0, S], [0, 1.0], x_length=6.0, y_length=3.8, xlabel=r"training steps",
                  ylabel=rf"accuracy, \ $T = {Tbig}$", xticks=[0, S], yticks=[0, 0.5, 1.0],
                  yfmt=lambda v: f"{int(100 * v)}\\%", center=[-3.2, -0.4, 0])
        A = ax.ax
        bands = VGroup()
        for c in ("rnn", "lstm", "gru"):
            R = [np.asarray(runs[f"{c}-{Tbig}-{s}"]["curve"]) for s in (0, 1, 2)]
            bands.add(seed_band(A, R[0][:, 0], [r[:, 1] for r in R], CELLS[c]))
        chance = DashedLine(A.c2p(0, m["chance"]), A.c2p(S, m["chance"]), color=GREY_D, stroke_width=2)
        cl = label(r"chance", font_size=18, color=GREY_B).next_to(chance, UP, buff=0.05).align_to(chance, RIGHT)
        leg = legend([(CELLS[c], CELL_NAME[c]) for c in ("rnn", "lstm", "gru")], font_size=22).next_to(ax, UP,
                                                                                                    buff=0.1)
        leg.align_to(ax, LEFT)
        # final accuracy by length
        bars = VGroup()
        fin = {c: [[runs[f"{c}-{T}-{s}"]["final"] for s in (0, 1, 2)] for T in Ts] for c in ("rnn", "lstm", "gru")}
        for j, T in enumerate(Ts):
            for k, c in enumerate(("rnn", "lstm", "gru")):
                v = float(np.mean(fin[c][j]))
                h = max(2.6 * v, 0.03)
                x = 1.6 + 1.7 * j + 0.42 * k
                b = Rectangle(width=0.36, height=h, stroke_width=0, fill_color=CELLS[c], fill_opacity=0.85)
                b.move_to([x, -2.2 + h / 2, 0])
                dots = VGroup(*[Dot([x, -2.2 + 2.6 * fv, 0], radius=0.04, color=WHITE) for fv in fin[c][j]])
                bars.add(VGroup(b, dots))
            bars.add(MathTex(rf"T = {T}", font_size=24, color=GREY_A).move_to([1.6 + 1.7 * j + 0.42, -2.55, 0]))
        base = Line([1.2, -2.2, 0], [6.6, -2.2, 0], color=GREY_C, stroke_width=1.5)
        bt = label(r"final accuracy \ (bars: mean; \ dots: each seed)", font_size=20, color=GREY_A)
        bt.next_to(base, UP, buff=2.9).align_to(base, LEFT)
        tag = note(r"computed").to_corner(DR, buff=0.2)

        def mean(c, T):
            return float(np.mean(fin[c][Ts.index(T)]))

        r10, r100 = mean("rnn", Ts[0]), mean("rnn", Tbig)
        l10, g10 = mean("lstm", Ts[0]), mean("gru", Ts[0])
        l100, g100 = mean("lstm", Tbig), mean("gru", Tbig)
        if min(r10, l10, g10) > 0.9:
            first = f"Over {Ts[0]} steps, all three learn the task: the plain network gets {pct(r10, 0)} percent right."
        else:
            first = (f"Even over {Ts[0]} steps the task is not easy: the plain network gets {pct(r10, 0)} percent "
                     f"right, the LSTM {pct(l10, 0)}, the GRU {pct(g10, 0)}.")
        # when do the gated cells leave chance?  first evaluation step a quarter above it, per seed
        waits = []
        for c in ("lstm", "gru"):
            for s_ in (0, 1, 2):
                cv = np.asarray(runs[f"{c}-{Tbig}-{s_}"]["curve"])
                up = np.nonzero(cv[:, 1] > m["chance"] + 0.25)[0]
                waits.append(cv[up[0], 0] if len(up) else np.inf)
        wait_steps = int(np.median(waits)) if np.isfinite(np.median(waits)) else 0
        if np.isfinite(np.median(waits)) and wait_steps > 0.15 * S:
            jump = (f"The gated cells sit at chance for a while, about {wait_steps:,} steps, then find the trick and "
                    "climb: the gates learn to open for the marked symbol and close for everything after it.")
        else:
            jump = ("The gated cells climb from the start: the gates soon learn to open for the marked symbol and "
                    "close for everything after it.")
        if r100 < 0.3 and min(l100, g100) > 0.9:
            v = (f"At {Tbig} steps the plain network never gets off chance, {pct(r100, 0)} percent, while the LSTM "
                 f"and the GRU reach {pct(l100, 0)} and {pct(g100, 0)}.")
        elif r100 < min(l100, g100) - 0.2:
            v = (f"At {Tbig} steps the plain network reaches only {pct(r100, 0)} percent; the LSTM "
                 f"{pct(l100, 0)}, the GRU {pct(g100, 0)}.")
        else:
            v = (f"At {Tbig} steps all three do about as well: {pct(r100, 0)}, {pct(l100, 0)} and "
                 f"{pct(g100, 0)} percent.")
        with self.voiceover(
            f"The results. {first} <bookmark mark='a'/> {v} <bookmark mark='b'/> {jump}"
        ) as vo:
            self.play(Create(base), FadeIn(bt), FadeIn(tag), Create(ax), Create(chance), FadeIn(cl), FadeIn(leg))
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bands], lag_ratio=0.4), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gradients(self):
        m = load("memory")
        Tbig = int(m["T"][-1])
        runs = m["runs"]
        pr = [np.asarray(p) for p in runs[f"rnn-{Tbig}-0"]["profile"]]
        pl = [np.asarray(p) for p in runs[f"lstm-{Tbig}-0"]["profile"]]
        n = min(len(pr), len(pl))
        logs_r = [np.log10(np.maximum(p[1:], 1e-12)) for p in pr[:n]]
        logs_l = [np.log10(np.maximum(p[1:], 1e-12)) for p in pl[:n]]
        lo = math.floor(min(min(a.min() for a in logs_r), min(a.min() for a in logs_l)))
        hi = math.ceil(max(max(a.max() for a in logs_r), max(a.max() for a in logs_l)))
        lo = max(lo, hi - 12)
        ax = axes([1, Tbig], [lo, hi], x_length=7.0, y_length=4.0, xlabel=r"time step $t$ of the sequence",
                  ylabel=r"$\|\partial L / \partial x_t\|$: \ the gradient reaching step $t$",
                  xticks=[1, Tbig // 2, Tbig], yticks=list(range(lo, hi + 1, max(1, (hi - lo) // 4))),
                  yfmt=lambda v: f"10^{{{int(v)}}}", center=[-1.6, -0.4, 0])
        A = ax.ax
        ts = np.arange(1, Tbig + 1)
        k = ValueTracker(0)
        cr = always_redraw(lambda: curve(A, ts, np.clip(logs_r[int(k.get_value())], lo, hi), RNNC, 3.5))
        clc = always_redraw(lambda: curve(A, ts, np.clip(logs_l[int(k.get_value())], lo, hi), LSTMC, 3.5))
        clock = always_redraw(lambda: MathTex(rf"\text{{training step }}{int(pr[int(k.get_value())][0]):,}"
                                              .replace(",", "{,}"), font_size=28).to_corner(UR, buff=0.5))
        leg = legend([(RNNC, r"RNN"), (LSTMC, r"LSTM")], font_size=24).to_corner(UR, buff=0.5).shift(DOWN * 0.8)
        first = label(r"step $1$: \ the symbol to remember", font_size=20, color=CELLC)
        first.move_to(A.c2p(1, lo + 1.5), aligned_edge=LEFT).shift(RIGHT * 0.15)  # clear of both curves
        tag = note(rf"computed: \ $T = {Tbig}$, \ seed $0$").to_corner(DR, buff=0.2)
        gap_r = logs_r[-1][-1] - logs_r[-1][0]
        gap_l = logs_l[-1][-1] - logs_l[-1][0]
        if gap_l < 0.5 and gap_r > 1.5:
            v = (f"For the plain network, the gradient at the first step, the only one that matters, is about ten "
                 f"to the {gap_r:.0f} times weaker than at the last. <bookmark mark='b'/> For the LSTM the first "
                 "step gets about as much as the last: the belt carries the signal back.")
        elif gap_l < gap_r - 1:
            v = (f"For the plain network, the gradient at the first step, the only one that matters, is about ten "
                 f"to the {gap_r:.0f} times weaker than at the last. <bookmark mark='b'/> For the LSTM the "
                 f"difference is ten to the {gap_l:.0f}: the belt carries the signal back.")
        else:
            v = (f"For the plain network the gradient at the first step is ten to the {gap_r:.0f} times weaker than "
                 f"at the last; <bookmark mark='b'/> for the LSTM, ten to the {gap_l:.0f}.")
        with self.voiceover(
            "Here is why. During training, measure how much gradient arrives at each step of the sequence, from "
            "the answer at the end. <bookmark mark='a'/> " + v
        ) as vo:
            self.play(Create(ax), FadeIn(leg), FadeIn(first), FadeIn(tag))
            self.add(cr, clc, clock)
            vo.wait_until("a")
            self.play(k.animate.set_value(n - 1), run_time=max(2.0, vo.until("b") - 0.3), rate_func=linear)
        for mob in (cr, clc, clock):
            mob.clear_updaters()
        self.wait(0.3)
        self.clear_scene()


_ = (GRADC, HIST)
