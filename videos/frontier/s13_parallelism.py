from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.frontier.common import LLAMA3, calc, gpu, label, schematic_tag, source

GPU_A, GPU_B = BLUE_C, GOLD_C  # local colors for "GPU 1" and "GPU 2" in the tensor-parallel example


def simulate_pipeline(p: int, m: int, schedule: str, tf: float = 1.0, tb: float = 2.0):
    """Exact timeline of a pipeline schedule.  Returns [(stage, kind, microbatch, start, end)].
    Dependencies: F(s, j) after F(s-1, j); B(s, j) after B(s+1, j) and F(s, j); one op at a time per stage."""
    orders = []
    for s in range(p):
        if schedule == "gpipe":
            ops = [("F", j) for j in range(m)] + [("B", j) for j in range(m)]
        elif schedule == "1f1b":
            warm = min(p - s - 1, m)
            ops = [("F", j) for j in range(warm)]
            for k in range(m - warm):
                ops += [("F", warm + k), ("B", k)]
            ops += [("B", j) for j in range(m - warm, m)]
        else:
            raise ValueError(schedule)
        orders.append(ops)
    done: dict = {}
    free = [0.0] * p
    idx = [0] * p
    out = []
    while any(idx[s] < len(orders[s]) for s in range(p)):
        progressed = False
        for s in range(p):
            if idx[s] >= len(orders[s]):
                continue
            kind, j = orders[s][idx[s]]
            deps = [("F", s - 1, j)] if kind == "F" and s > 0 else []
            if kind == "B":
                deps = [("F", s, j)] + ([("B", s + 1, j)] if s < p - 1 else [])
            if all(d in done for d in deps):
                start = max([free[s]] + [done[d] for d in deps])
                end = start + (tf if kind == "F" else tb)
                done[(kind, s, j)] = end
                free[s] = end
                out.append((s, kind, j, start, end))
                idx[s] += 1
                progressed = True
        assert progressed, "deadlock"
    return out


def timeline(ops, p, unit=0.21, row_h=0.5, label_mb=True):
    g = VGroup()
    T = max(o[4] for o in ops)
    for s in range(p):
        bg = Rectangle(width=T * unit, height=row_h * 0.86, stroke_width=0, fill_color=C.BUBBLE, fill_opacity=0.35)
        bg.move_to([T * unit / 2, -s * row_h, 0])
        g.add(bg)
    for s, kind, j, a, b in ops:
        col = C.ACTS if kind == "F" else C.GRADS
        r = Rectangle(width=(b - a) * unit - 0.02, height=row_h * 0.86, stroke_width=0, fill_color=col, fill_opacity=0.85)
        r.move_to([(a + b) / 2 * unit, -s * row_h, 0])
        g.add(r)
        if label_mb:
            g.add(Text(str(j + 1), font_size=13, color=BLACK).move_to(r))
    names = VGroup(*[label(rf"GPU {s + 1}", font_size=22, color=GREY_A).move_to([-0.6, -s * row_h, 0]) for s in range(p)])
    g.add(names)
    g.T = T
    return g


class Parallelism(VoiceoverScene):
    def construct(self):
        self.tensor_parallel()
        self.links()
        self.pipeline()
        self.experts_and_context()
        self.mesh()
        self.run_math()

    # ------------------------------------------------------------------
    def tensor_parallel(self):
        x = np.array([[1, 2]])
        W1 = np.array([[1, 0, 2, 1], [0, 1, 1, 3]])
        W2 = np.array([[1, 1], [2, 0], [0, 1], [1, 2]])
        y = x @ W1
        z = y @ W2
        za, zb = y[:, :2] @ W2[:2], y[:, 2:] @ W2[2:]
        assert np.array_equal(za + zb, z)

        def mat(M, colors=None, cols=False):
            m = Matrix(M.tolist(), h_buff=0.7, v_buff=0.6, element_to_mobject_config={"font_size": 32})
            if colors is not None:
                ents = m.get_entries()
                r, c = M.shape
                for i in range(r):
                    for k in range(c):
                        part = k if cols else i
                        ents[i * c + k].set_color(colors[0] if part < (c if cols else r) // 2 else colors[1])
            return m

        head = label(r"Tensor parallelism: split each matrix across GPUs", font_size=36).to_edge(UP, buff=0.4)
        mx = mat(x)
        m1 = mat(W1, (GPU_A, GPU_B), cols=True)
        eq1 = VGroup(mx, MathTex(r"\times", font_size=40), m1, MathTex("=", font_size=40), mat(y, (GPU_A, GPU_B), cols=True))
        eq1.arrange(RIGHT, buff=0.25).move_to(UP * 1.3)
        lab1 = label(r"split by columns: each GPU computes half the outputs, no communication", font_size=26,
                     color=GREY_A).next_to(eq1, DOWN, buff=0.3)
        m2 = mat(W2, (GPU_A, GPU_B), cols=False)
        ya = mat(y[:, :2])
        ya.get_entries().set_color(GPU_A)
        yb = mat(y[:, 2:])
        yb.get_entries().set_color(GPU_B)
        eq2 = VGroup(mat(y, (GPU_A, GPU_B), cols=True), MathTex(r"\times", font_size=40), m2, MathTex("=", font_size=40),
                     mat(za), MathTex("+", font_size=40), mat(zb), MathTex("=", font_size=40), mat(z))
        eq2[4].get_entries().set_color(GPU_A)
        eq2[6].get_entries().set_color(GPU_B)
        eq2[8].get_entries().set_color(C.COMM)
        eq2.arrange(RIGHT, buff=0.22).move_to(DOWN * 1.6)
        lab2 = label(r"split by rows: partial sums, added by one all-reduce", font_size=26, color=GREY_A).next_to(eq2, DOWN, buff=0.3)
        key = VGroup(VGroup(Square(0.2, stroke_width=0, fill_color=GPU_A, fill_opacity=1), label(r"GPU 1", font_size=22)).arrange(RIGHT, buff=0.1),
                     VGroup(Square(0.2, stroke_width=0, fill_color=GPU_B, fill_opacity=1), label(r"GPU 2", font_size=22)).arrange(RIGHT, buff=0.1)
                     ).arrange(RIGHT, buff=0.4).to_corner(UR, buff=0.4).shift(DOWN * 0.6)
        with self.voiceover(
            "Data parallelism still runs every layer in full on every GPU. When a single layer is too big, you split "
            "the layer itself. That's tensor parallelism. <bookmark mark='c'/> Take a matrix multiplication. Cut the "
            "weight matrix into columns, and each GPU computes its own slice of the output, with no communication "
            "at all. <bookmark mark='r'/> Feed those slices into the next matrix, cut into rows, and each GPU "
            "produces a partial sum. <bookmark mark='s'/> One all-reduce adds them up."
        ) as vo:
            self.play(FadeIn(head), FadeIn(key))
            vo.wait_until("c")
            self.play(FadeIn(eq1[:3]))
            self.play(FadeIn(eq1[3:]), FadeIn(lab1))
            vo.wait_until("r")
            self.play(FadeIn(eq2[:7]), FadeIn(lab2))
            vo.wait_until("s")
            self.play(FadeIn(eq2[7:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def links(self):
        def server(x):
            chips = VGroup(*[gpu("", width=0.5, height=0.36, fill=0.3) for _ in range(8)]).arrange_in_grid(2, 4, buff=0.18)
            bus = RoundedRectangle(width=chips.width + 0.3, height=chips.height + 0.3, corner_radius=0.1,
                                   stroke_color=C.COMM, stroke_width=4)
            frame = RoundedRectangle(width=chips.width + 0.8, height=chips.height + 0.9, corner_radius=0.15,
                                     stroke_color=GREY_B, stroke_width=2)
            g = VGroup(frame, bus, chips).move_to([x, 0.3, 0])
            g.frame = frame
            return g
        s1, s2 = server(-3.2), server(3.2)
        cable = DashedLine(s1.frame.get_right(), s2.frame.get_left(), color=GREY_B, stroke_width=3, dash_length=0.1)
        l1 = label(r"NVLink, inside a server:\\450 GB/s each way, per GPU", font_size=26, color=C.COMM).next_to(s1, DOWN, buff=0.35)
        l2 = label(r"network between servers:\\about 50 GB/s each way, per GPU", font_size=26, color=GREY_A).next_to(s2, DOWN, buff=0.35)
        ratio = label(r"$\approx 9\times$ slower", font_size=30, color=GREY_A).next_to(cable, UP, buff=0.15)
        head = label(r"Megatron-LM: two all-reduces per layer, forward; two backward", font_size=32).to_edge(UP, buff=0.5)
        src = source(r"Shoeybi et al.\ 2019 (Megatron-LM); NVIDIA H100 / ConnectX-7 (400 Gb/s) specifications")
        with self.voiceover(
            "NVIDIA's Megatron-LM arranged a whole transformer layer this way, with just two all-reduces in the "
            "forward pass and two in the backward. <bookmark mark='n'/> But they happen in every layer, on the "
            "critical path, so tensor parallelism is kept inside one server, where eight GPUs are joined by NVLink at "
            "450 gigabytes per second in each direction. <bookmark mark='i'/> Between servers, a network card "
            "manages about 50: nine times slower."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("n")
            self.play(FadeIn(s1), FadeIn(l1))
            vo.wait_until("i")
            self.play(FadeIn(s2), Create(cable), FadeIn(l2), FadeIn(ratio))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pipeline(self):
        p = 4
        naive = simulate_pipeline(p, 1, "gpipe")
        sched = simulate_pipeline(p, 8, "1f1b")
        T1 = max(o[4] for o in naive)
        T8 = max(o[4] for o in sched)
        bubble1 = 1 - (1 * 3) / T1
        bubble8 = 1 - (8 * 3) / T8
        assert abs(bubble1 - (p - 1) / (1 + p - 1)) < 1e-9 and abs(bubble8 - (p - 1) / (8 + p - 1)) < 1e-9

        stages = VGroup(*[RoundedRectangle(width=2.4, height=0.7, corner_radius=0.1, stroke_color=C.PARAMS,
                                           fill_color=C.PARAMS, fill_opacity=0.15) for _ in range(p)]).arrange(RIGHT, buff=0.5)
        for k, st in enumerate(stages):
            st.add(label(rf"layers {32 * k + 1}--{32 * (k + 1)}", font_size=22).move_to(st))
        gl = VGroup(*[label(rf"GPU {k + 1}", font_size=22, color=GREY_A).next_to(st, DOWN, buff=0.12) for k, st in enumerate(stages)])
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.05, stroke_width=3, color=C.ACTS)
                          for a, b in zip(stages, stages[1:])])
        top = VGroup(stages, gl, arrows).to_edge(UP, buff=0.6)
        head = label(r"Pipeline parallelism: split the model by depth", font_size=34).next_to(top, UP, buff=0.2)

        tl1 = timeline(naive, p, unit=0.42)
        tl1.next_to(top, DOWN, buff=0.6).align_to(LEFT * 5.6, LEFT)
        b1 = label(rf"1 batch: idle {100 * bubble1:.0f}\% of the time", font_size=28, color=C.BUBBLE).next_to(tl1, RIGHT, buff=0.4)
        b1.set_color(GREY_A)
        key = VGroup(*[VGroup(Square(0.22, stroke_width=0, fill_color=c, fill_opacity=0.85 if c != C.BUBBLE else 0.35),
                              label(t, font_size=22)).arrange(RIGHT, buff=0.12)
                       for c, t in [(C.ACTS, r"forward"), (C.GRADS, r"backward (2$\times$ longer)"), (C.BUBBLE, r"idle: the bubble")]]
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(DR, buff=0.4)
        with self.voiceover(
            "To spread a model across servers, cut it by depth instead: pipeline parallelism. <bookmark mark='s'/> "
            "The first GPU holds the first quarter of the layers, the next GPU the next quarter, and so on. Only "
            "activations pass between stages, so slower links are fine. <bookmark mark='n'/> But a naive pipeline is "
            "mostly idle. While one stage works, the others wait: three quarters of the time is bubble."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("s")
            self.play(LaggedStart(*[FadeIn(VGroup(st, g)) for st, g in zip(stages, gl)], lag_ratio=0.2),
                      LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2))
            vo.wait_until("n")
            self.play(FadeIn(key), FadeIn(tl1[:p]), FadeIn(tl1[-1]))
            self.play(LaggedStart(*[FadeIn(m) for m in tl1[p:-1]], lag_ratio=0.1), run_time=1.5)
            self.play(FadeIn(b1))

        tl8 = timeline(sched, p, unit=0.33)
        tl8.next_to(tl1, DOWN, buff=0.55).align_to(tl1, LEFT)
        b8 = label(rf"8 micro-batches: idle {100 * bubble8:.0f}\%", font_size=28, color=GREY_A).next_to(tl8, DOWN, buff=0.2).align_to(tl8, LEFT)
        formula = MathTex(r"\text{bubble} = \frac{p-1}{m+p-1}", font_size=36).next_to(b1, DOWN, buff=0.35).align_to(b1, LEFT)
        with self.voiceover(
            "The fix is to cut each batch into micro-batches and keep the pipeline full. <bookmark mark='m'/> With "
            "eight micro-batches, the bubble shrinks to p minus one, over m plus p minus one: about a quarter. "
            "<bookmark mark='z'/> Cleverer schedules push it further. Zero-bubble pipelines split the backward pass "
            "in two and use one half to fill the gaps, and DeepSeek's DualPipe feeds micro-batches in from both ends "
            "at once, hiding communication behind computation."
        ) as vo:
            vo.wait_until("m")
            self.play(FadeIn(tl8[:p]), FadeIn(tl8[-1]))
            self.play(LaggedStart(*[FadeIn(m) for m in tl8[p:-1]], lag_ratio=0.02), run_time=2.0)
            self.play(FadeIn(b8), FadeIn(formula))
            vo.wait_until("z")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def experts_and_context(self):
        cols = [PURPLE_B, TEAL_C, GOLD_C, PINK, BLUE_C, GREEN_C, RED_C, ORANGE]
        gpus = VGroup()
        for k in range(4):
            g = gpu(rf"GPU {k + 1}", width=2.2, height=1.6, font_size=22)
            g.text.next_to(g.body, UP, buff=0.1)
            ex = VGroup(*[Circle(0.26, color=cols[2 * k + e], fill_opacity=0.35, stroke_width=3) for e in range(2)]).arrange(RIGHT, buff=0.25)
            ex.move_to(g.body)
            exl = VGroup(*[MathTex(rf"E_{{{2 * k + e + 1}}}", font_size=22).move_to(c) for e, c in enumerate(ex)])
            gpus.add(VGroup(g, ex, exl))
        gpus.arrange(RIGHT, buff=0.7).move_to(UP * 0.6)
        rng = np.random.default_rng(3)
        tokens, targets = VGroup(), []
        for k in range(4):
            for t in range(4):
                e = int(rng.integers(0, 8))
                d = Dot(radius=0.07, color=cols[e]).move_to(gpus[k][0].body.get_bottom() + DOWN * 0.5 + RIGHT * (t - 1.5) * 0.3)
                tokens.add(d)
                targets.append(e)
        head = label(r"Expert parallelism: tokens travel to their experts (all-to-all)", font_size=32).to_edge(UP, buff=0.4)
        cp = label(r"Context parallelism: split one very long sequence across GPUs;\\attention passes keys and values around a ring",
                   font_size=26, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Mixture-of-experts models add expert parallelism. Each GPU holds different experts, <bookmark mark='t'/> "
            "and every token must travel to the GPUs holding its chosen experts, and back again: an all-to-all exchange "
            "in every MoE layer. <bookmark mark='c'/> And for very long sequences, context parallelism splits the "
            "sequence itself across GPUs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(gpus), FadeIn(schematic_tag()))
            vo.wait_until("t")
            self.play(FadeIn(tokens))
            moves = []
            for d, e in zip(tokens, targets):
                circ = gpus[e // 2][1][e % 2]
                moves.append(d.animate.move_to(circ.get_center()))
            self.play(*moves, run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(cp))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mesh(self):
        tp, pp, dp = 8, 16, 128
        assert tp * pp * dp == LLAMA3["gpus"]
        cell = 0.2

        def replica(opacity):
            g = VGroup(*[Square(cell, stroke_width=0, fill_color=C.GPU, fill_opacity=opacity) for _ in range(tp * pp)])
            return g.arrange_in_grid(pp, tp, buff=(0.035, 0.07))
        ghosts = VGroup(*[replica(0.18 + 0.08 * k).shift((RIGHT + UP) * 0.24 * (4 - k)) for k in range(4)])
        front = replica(0.9)
        block = VGroup(ghosts, front).move_to(LEFT * 3.6 + DOWN * 0.3)
        bottom_row = VGroup(*front[-tp:])
        b_tp = Brace(bottom_row, DOWN, color=C.COMM)
        l_tp = label(r"tensor $\times 8$: one server", font_size=24, color=C.COMM).next_to(b_tp, DOWN, buff=0.08)
        b_pp = Brace(front, LEFT, color=C.ACTS)
        l_pp = label(r"pipeline\\$\times 16$\\servers", font_size=24, color=C.ACTS).next_to(b_pp, LEFT, buff=0.1)
        l_dp = label(r"data $\times 128$ copies", font_size=24, color=C.WEIGHTS).next_to(ghosts[0], UP, buff=0.1)
        head = label(r"Llama 3.1 405B: 16{,}384 H100s $= 8 \times 16 \times 128$", font_size=34).to_edge(UP, buff=0.4)
        facts = VGroup(
            label(r"$\approx$400 TFLOP/s per GPU: 41\% of peak", font_size=28),
            label(r"(model FLOPs utilization, MFU)", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(RIGHT * 3.3 + UP * 1.2)
        ds = VGroup(
            label(r"\textbf{DeepSeek-V3}: 2{,}048 H800s", font_size=28),
            label(r"no tensor parallelism; 16-stage DualPipe;", font_size=24, color=GREY_A),
            label(r"experts spread over 64 GPUs on 8 nodes", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(RIGHT * 3.3 + DOWN * 1.2)
        src = source(r"Llama 3 paper (arXiv 2407.21783), Table 4; DeepSeek-V3 report (arXiv 2412.19437)")
        with self.voiceover(
            "Real runs combine all of these. Llama 3.1, the 405-billion-parameter model, trained on 16,384 H100s arranged as a grid: "
            "<bookmark mark='t'/> tensor parallel across the eight GPUs inside each server, <bookmark mark='p'/> a "
            "sixteen-stage pipeline across sixteen servers, <bookmark mark='d'/> and a hundred and twenty-eight copies "
            "of that pipeline doing data parallelism. <bookmark mark='m'/> Each GPU sustained about 400 teraflops: "
            "roughly forty percent of its peak, which is typical. <bookmark mark='ds'/> DeepSeek-V3 took a different "
            "shape, on 2,048 export-limited H800s: no tensor parallelism at all, a sixteen-stage DualPipe pipeline, "
            "and experts spread across 64 GPUs on eight nodes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            self.play(FadeIn(ghosts, lag_ratio=0.2), FadeIn(front), run_time=1.2)
            vo.wait_until("t")
            self.play(GrowFromCenter(b_tp), FadeIn(l_tp))
            vo.wait_until("p")
            self.play(GrowFromCenter(b_pp), FadeIn(l_pp))
            vo.wait_until("d")
            self.play(FadeIn(l_dp))
            vo.wait_until("m")
            self.play(FadeIn(facts))
            vo.wait_until("ds")
            self.play(FadeIn(ds))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def run_math(self):
        N, D, G = LLAMA3["params"], LLAMA3["tokens"], LLAMA3["gpus"]
        peak, achieved = 989e12, 400e12  # H100 dense BF16 peak; Llama 3.1 405B's sustained rate (Table 4)
        flops = 6 * N * D
        secs = flops / (G * achieved)
        gpu_h = secs * G / 3600
        step = 16e6 * 6 * N / (G * achieved)
        shard = N / (8 * 16) * 2  # bytes of BF16 gradient per GPU (TP 8 x PP 16)
        sent = 2 * 127 / 128 * shard
        t_sync = sent / 50e9
        assert round(achieved / peak, 2) == 0.40 and round(secs / 86400) == 67 and round(gpu_h / 1e6, 1) == 26.3
        assert round(step, 1) == 5.9 and round(shard / 1e9, 1) == 6.3 and round(sent / 1e9, 1) == 12.6 and round(t_sync, 2) == 0.25
        assert round(gpu_h / LLAMA3["gpu_hours"], 2) == 0.85
        head = label(r"The arithmetic of a real run: Llama 3.1 405B", font_size=34).to_edge(UP, buff=0.35)
        mfu = calc(r"\text{MFU} &= \frac{\text{achieved}}{\text{peak}} = \frac{400\ \text{TFLOP/s}}{989\ \text{TFLOP/s}} = 40\%",
                   font_size=30)
        run = calc(r"T_{\rm train} &= \frac{6ND}{n_{\rm GPU}\times \text{FLOP/s}} = "
                   r"\frac{3.79\times10^{25}}{16{,}384 \times 4.0\times10^{14}}",
                   r"\\ &= 5.8\times10^{6}\ \text{s} \approx 67\ \text{days} \;=\; 26.3\text{M GPU-hours}",
                   font_size=30)
        rep = label(r"Meta reports 30.84M GPU-hours: the formula is within 15\%", font_size=26, color=C.COMPUTE)
        stp = calc(r"\text{one step: } \frac{16\times10^{6} \times 6N}{n_{\rm GPU}\times\text{FLOP/s}} &= 5.9\ \text{s}",
                   r"\\ \text{gradient per GPU: } \frac{405\times10^{9}}{8 \times 16} \times 2\ \text{bytes} &= 6.3\ \text{GB}",
                   r"\\ \text{ring all-reduce over 128 copies: } 2\,\tfrac{127}{128} \times 6.3 &= 12.6\ \text{GB}"
                   r"\ \Rightarrow\ \frac{12.6\ \text{GB}}{50\ \text{GB/s}} = 0.25\ \text{s}",
                   font_size=30)
        col = VGroup(mfu, run, rep, stp).arrange(DOWN, aligned_edge=LEFT, buff=0.38).next_to(head, DOWN, buff=0.4)
        if col.width > 13.2:
            col.scale_to_fit_width(13.2)
        col.set_x(0)
        rep.shift(RIGHT * 0.3)
        run[1].set_color(C.COMPUTE)
        src = source(r"Llama 3 paper, Table 4 (TP 8, PP 16, DP 128; 400 TFLOP/s per GPU); Llama 3.1 model card (GPU-hours)")
        with self.voiceover(
            "Now the arithmetic of a real run. An H100 peaks at 989 trillion operations per second; Llama 3.1's GPUs "
            "sustained about 400 trillion, forty percent, a figure called model FLOPs utilization. "
            "<bookmark mark='t'/> So training takes six N D divided by the cluster's speed: 3.8 times ten to the "
            "twenty-five, over sixteen thousand GPUs times 400 trillion. <bookmark mark='d'/> That's 5.8 million "
            "seconds: sixty-seven days, or 26 million GPU-hours. <bookmark mark='r'/> Meta reports 30.8 million, so "
            "this one line gets within fifteen percent. <bookmark mark='s'/> One step, sixteen million tokens, takes "
            "about six seconds. <bookmark mark='g'/> In that time each GPU must average its gradients with its 127 "
            "copies. It holds 3.2 billion parameters, 6.3 gigabytes of gradients; a ring sends about twice that, and "
            "at fifty gigabytes per second it takes a quarter of a second, hidden behind the backward pass."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), Write(mfu))
            vo.wait_until("t")
            self.play(Write(run[0]))
            vo.wait_until("d")
            self.play(Write(run[1]))
            vo.wait_until("r")
            self.play(FadeIn(rep, shift=UP * 0.1))
            vo.wait_until("s")
            self.play(Write(stp[0]))
            vo.wait_until("g")
            self.play(Write(stp[1]))
            self.play(Write(stp[2]))
        self.wait(0.4)
        self.clear_scene()
