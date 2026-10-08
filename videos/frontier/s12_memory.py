from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.frontier.common import LLAMA3, gpu, label, part_card, pipeline_map, source

BYTES = [  # (component, bytes per parameter, color)
    (r"weight (BF16)", 2, C.WEIGHTS),
    (r"gradient (BF16)", 2, C.GRADS),
    (r"master weight (FP32)", 4, C.OPT_STATE),
    (r"Adam: mean of gradients (FP32)", 4, C.OPT_STATE),
    (r"Adam: mean of squares (FP32)", 4, C.OPT_STATE),
]


def ring_allreduce(vals: np.ndarray):
    """Exact ring all-reduce on an (N GPUs x N chunks) array; yields (phase, step, sends, state) after each step,
    where sends = [(src, dst, chunk)]."""
    N = vals.shape[0]
    state = vals.astype(float).copy()
    for s in range(N - 1):  # reduce-scatter: GPU i sends chunk (i - s) to i+1, which adds it
        sends = [(i, (i + 1) % N, (i - s) % N) for i in range(N)]
        new = state.copy()
        for src, dst, c in sends:
            new[dst, c] += state[src, c]
        state = new
        yield "reduce-scatter", s, sends, state.copy()
    for s in range(N - 1):  # all-gather: GPU i sends its finished chunk (i + 1 - s) to i+1
        sends = [(i, (i + 1) % N, (i + 1 - s) % N) for i in range(N)]
        new = state.copy()
        for src, dst, c in sends:
            new[dst, c] = state[src, c]
        state = new
        yield "all-gather", s, sends, state.copy()


class Memory(VoiceoverScene):
    def construct(self):
        self.opening()
        self.bytes_per_param()
        self.too_big()
        self.data_parallel()
        self.allreduce()
        self.zero()

    # ------------------------------------------------------------------
    def opening(self):
        card = part_card(3, r"Scaling out", r"memory, parallelism, and keeping thousands of GPUs alive").to_edge(UP, buff=1.0)
        m = pipeline_map(width=13.0, highlight="cluster").to_edge(DOWN, buff=0.7)
        with self.voiceover("Part three: scaling out."):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(m), run_time=1.2)
        self.wait(0.8)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bytes_per_param(self):
        cells = VGroup()
        rows = VGroup()
        for name, b, col in BYTES:
            sq = VGroup(*[Square(0.42, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.55)
                          for _ in range(b)]).arrange(RIGHT, buff=0.06)
            lab = label(name, font_size=28).next_to(sq, LEFT, buff=0.35)
            nb = label(rf"{b} bytes", font_size=26, color=GREY_A)
            rows.add(VGroup(lab, sq, nb))
            cells.add(*sq)
        rows.arrange(DOWN, buff=0.28)
        x_num = rows[2][1].get_right()[0] + 0.4  # right of the widest (4-byte) row
        for r in rows:
            r[1].align_to(rows[0][1], LEFT)
            r[0].next_to(r[1], LEFT, buff=0.35)
            r[2].move_to([x_num, r[1].get_y(), 0], aligned_edge=LEFT)
        rows.scale(1.15).move_to(DOWN * 0.2 + RIGHT * 0.6)
        head = label(r"What training keeps in memory, for every parameter", font_size=38).to_edge(UP, buff=0.5)
        total = label(r"$= 16$ bytes per parameter", font_size=36, color=YELLOW).next_to(rows, DOWN, buff=0.45)
        keys = ["w", "g", "m", "a1", "a2"]
        with self.voiceover(
            "Let's count what a training run has to keep in memory. For every parameter: <bookmark mark='w'/> the "
            "weight itself, in sixteen-bit, two bytes. <bookmark mark='g'/> Its gradient: two more. Then the "
            "optimizer's state: <bookmark mark='m'/> a full-precision master copy of the weight, four bytes, "
            "<bookmark mark='a1'/> and Adam's two running averages, <bookmark mark='a2'/> four bytes each. "
            "<bookmark mark='t'/> Sixteen bytes per parameter."
        ) as vo:
            self.play(FadeIn(head))
            for i, k in enumerate(keys):
                vo.wait_until(k)
                self.play(FadeIn(rows[i][0]), LaggedStart(*[FadeIn(c, scale=0.5) for c in rows[i][1]], lag_ratio=0.1),
                          FadeIn(rows[i][2]), run_time=0.7)
            vo.wait_until("t")
            self.play(FadeIn(total, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def too_big(self):
        N = LLAMA3["params"]
        tb = N * 16 / 1e12
        n_h100 = int(np.ceil(N * 16 / 80e9))
        assert abs(tb - 6.48) < 0.01 and n_h100 == 81
        tiles = VGroup(*[gpu("", width=0.52, height=0.42, fill=0.25) for _ in range(81)]).arrange_in_grid(9, 9, buff=0.1)
        tiles.move_to(LEFT * 3.2 + DOWN * 0.3)
        lab = label(r"Llama 3.1 405B: $405\text{B} \times 16$ bytes $= 6.48$ TB", font_size=34).to_edge(UP, buff=0.5)
        cap = label(r"81 H100s (80 GB each),\\just to hold the training state", font_size=30, color=C.GPU)
        cap.next_to(tiles, RIGHT, buff=0.7).shift(UP * 1.2)
        mems = VGroup(
            label(r"H100: 80 GB", font_size=26, color=GREY_A),
            label(r"B200: 192 GB", font_size=26, color=GREY_A),
            label(r"B300: 288 GB", font_size=26, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(cap, DOWN, buff=0.5).align_to(cap, LEFT)
        acts = label(r"$+$ activations: values saved in the forward pass\\for the backward pass (often recomputed instead)",
                     font_size=26, color=C.ACTS).next_to(mems, DOWN, buff=0.5).align_to(cap, LEFT)
        with self.voiceover(
            "For a 405-billion-parameter model like Llama 3.1, that's six and a half terabytes. <bookmark mark='h'/> "
            "An H100 has eighty gigabytes; even the newest Blackwell Ultra has 288. So just holding the training "
            "state takes eighty-one H100s, <bookmark mark='a'/> before counting the activations: the intermediate "
            "values saved during the forward pass for use in the backward pass, which for long sequences can be "
            "even larger. They're often thrown away and recomputed when needed, trading compute for memory."
        ) as vo:
            self.play(FadeIn(lab))
            vo.wait_until("h")
            self.play(LaggedStart(*[FadeIn(t, scale=0.6) for t in tiles], lag_ratio=0.01), FadeIn(cap), FadeIn(mems),
                      run_time=1.8)
            vo.wait_until("a")
            self.play(FadeIn(acts))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def data_parallel(self):
        n = 4
        gpus = VGroup(*[gpu(rf"GPU {i + 1}", width=1.6, height=1.0) for i in range(n)]).arrange(RIGHT, buff=1.0)
        gpus.move_to(UP * 0.4)
        models = VGroup(*[label(r"full model copy", font_size=20, color=C.WEIGHTS).next_to(g, UP, buff=0.18) for g in gpus])
        batch = VGroup(*[Rectangle(width=1.4, height=0.4, stroke_color=C.DATA, stroke_width=2, fill_color=C.DATA,
                                   fill_opacity=0.3) for _ in range(n)]).arrange(RIGHT, buff=0.0).to_edge(UP, buff=0.5)
        blab = label(r"one batch of data, split four ways", font_size=24, color=C.DATA).next_to(batch, DOWN, buff=0.1)
        grads = VGroup(*[label(rf"gradient $g_{i + 1}$", font_size=24, color=C.GRADS).next_to(g, DOWN, buff=0.3)
                         for i, g in enumerate(gpus)])
        avg = MathTex(r"\bar g = \tfrac14(g_1+g_2+g_3+g_4)", font_size=40, color=C.COMM).to_edge(DOWN, buff=0.9)
        head = label(r"Data parallelism", font_size=36).to_edge(UP, buff=0.4)
        batch.next_to(head, DOWN, buff=0.35)
        blab.next_to(batch, DOWN, buff=0.1)
        self.play(FadeIn(head))
        with self.voiceover(
            "So the work has to be split across many GPUs, and there are several ways to split it. The simplest is "
            "data parallelism: <bookmark mark='c'/> every GPU holds a full copy of the model <bookmark mark='b'/> "
            "and processes a different slice of each batch. <bookmark mark='g'/> Each computes its own gradient, "
            "<bookmark mark='a'/> and then they must all agree on the average before taking a step together."
        ) as vo:
            vo.wait_until("c")
            self.play(FadeIn(gpus), FadeIn(models))
            vo.wait_until("b")
            self.play(FadeIn(batch), FadeIn(blab))
            self.play(*[batch[i].animate.move_to(gpus[i].get_top() + UP * 0.9).set_width(1.2) for i in range(n)],
                      FadeOut(blab), FadeOut(models))
            vo.wait_until("g")
            self.play(LaggedStart(*[FadeIn(g, shift=DOWN * 0.2) for g in grads], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(avg))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def allreduce(self):
        vals = np.array([[3, 1, 4, 1], [5, 9, 2, 6], [5, 3, 5, 8], [9, 7, 9, 3]])
        N = 4
        total = vals.sum(0)
        centers = [UP * 1.5 + LEFT * 3.2, UP * 1.5 + RIGHT * 3.2, DOWN * 2.0 + RIGHT * 3.2, DOWN * 2.0 + LEFT * 3.2]
        chips, cells, nums = VGroup(), [], []
        for i in range(N):
            g = gpu(rf"GPU {i + 1}", width=1.3, height=0.6, font_size=20).move_to(centers[i] + UP * 0.55)
            row = VGroup(*[Square(0.62, stroke_color=C.GRADS, stroke_width=2, fill_color=C.GRADS, fill_opacity=0.12)
                           for _ in range(N)]).arrange(RIGHT, buff=0.06).move_to(centers[i] + DOWN * 0.35)
            nn = VGroup(*[Integer(int(vals[i, c]), font_size=30).move_to(row[c]) for c in range(N)])
            chips.add(VGroup(g, row, nn))
            cells.append(row)
            nums.append(nn)
        head = label(r"Ring all-reduce (exact, 4 GPUs, 4 chunks each)", font_size=32).to_edge(UP, buff=0.25)
        goal = label(rf"goal: every GPU ends with the sum $[{', '.join(str(int(t)) for t in total)}]$", font_size=26,
                     color=C.COMM).next_to(head, DOWN, buff=0.12)
        self.add(head)
        with self.voiceover(
            "That averaging is called an all-reduce, and the standard algorithm passes messages around a ring. "
            "<bookmark mark='c'/> Each GPU's gradient is cut into chunks; here, four GPUs with four numbers each. "
            "<bookmark mark='go'/> Every GPU needs to end up with the sum."
        ) as vo:
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c) for c in chips], lag_ratio=0.15))
            vo.wait_until("go")
            self.play(FadeIn(goal))

        steps = list(ring_allreduce(vals))
        assert np.array_equal(steps[-1][3], np.tile(total, (N, 1)))
        rs_final = steps[N - 2][3]  # after reduce-scatter, GPU i owns the full sum of chunk (i + 1) % N
        for i in range(N):
            assert rs_final[i, (i + 1) % N] == total[(i + 1) % N]

        def do_step(phase_name, sends, state, rt):
            movers = []
            for src, dst, c in sends:
                m = VGroup(cells[src][c].copy().set_fill(C.COMM, 0.6).set_stroke(C.COMM),
                           nums[src][c].copy())
                movers.append((m, dst, c))
            self.play(*[m.animate.move_to(cells[dst][c]) for m, dst, c in movers], run_time=rt * 0.6)
            anims = []
            for (m, dst, c) in movers:
                anims.append(FadeOut(m))
                anims.append(nums[dst][c].animate.set_value(int(state[dst, c])))
                full = state[dst, c] == total[c]
                anims.append(cells[dst][c].animate.set_fill(C.COMM if full else C.GRADS, 0.55 if full else 0.3))
            self.play(*anims, run_time=rt * 0.4)

        p1 = label(r"reduce-scatter: send one chunk to the next GPU, which adds it", font_size=26, color=GREY_A).to_edge(DOWN, buff=0.35)
        p2 = label(r"all-gather: pass the finished chunks around", font_size=26, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "In each step, every GPU sends one chunk to its neighbor, which adds it to its own. "
            "<bookmark mark='o'/> After three steps, each GPU holds one chunk of the complete sum. "
            "<bookmark mark='g'/> Three more steps pass the finished chunks around the ring, <bookmark mark='d'/> "
            "and now every GPU has the whole sum. Each one sent only about twice the size of its gradient, no matter "
            "how many GPUs are in the ring."
        ) as vo:
            self.play(FadeIn(p1))
            for ph, s, sends, state in steps[:N - 1]:
                do_step(ph, sends, state, 1.6)
            vo.wait_until("g")
            self.play(FadeOut(p1), FadeIn(p2))
            for ph, s, sends, state in steps[N - 1:]:
                do_step(ph, sends, state, 1.2)
            vo.wait_until("d")
            cost = MathTex(r"\text{sent per GPU} = 2\,\tfrac{N-1}{N}\times\text{gradient size}", font_size=34, color=C.COMM)
            cost.move_to(DOWN * 0.25)
            self.play(FadeIn(cost))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def zero(self):
        psi = 7.5e9
        Nd = 64
        gb = psi / 1e9
        cases = [  # (name, weights GB, grads GB, optimizer GB)
            (r"replicated", 2 * gb, 2 * gb, 12 * gb),
            (r"ZeRO-1\\shard optimizer", 2 * gb, 2 * gb, 12 * gb / Nd),
            (r"ZeRO-2\\+ gradients", 2 * gb, 2 * gb / Nd, 12 * gb / Nd),
            (r"ZeRO-3 / FSDP\\+ weights", 2 * gb / Nd, 2 * gb / Nd, 12 * gb / Nd),
        ]
        totals = [sum(c[1:]) for c in cases]
        assert [round(t, 1) for t in totals] == [120.0, 31.4, 16.6, 1.9]
        scale = 4.6 / 120
        bars = VGroup()
        for k, (name, w, g, o) in enumerate(cases):
            stack = VGroup()
            y = 0
            for val, col in [(w, C.WEIGHTS), (g, C.GRADS), (o, C.OPT_STATE)]:
                h = max(val * scale, 0.012)
                stack.add(Rectangle(width=1.3, height=h, stroke_width=0, fill_color=col, fill_opacity=0.85)
                          .move_to([0, y + h / 2, 0]))
                y += h
            tot = label(rf"{totals[k]:.1f} GB", font_size=28).next_to(stack, UP, buff=0.12)
            nm = label(name, font_size=24, color=GREY_A).next_to(stack, DOWN, buff=0.2)
            col = VGroup(stack, tot, nm)
            col.stack = stack
            bars.add(col)
        for k, b in enumerate(bars):  # bottoms aligned on y = -2.4, columns 2.9 apart
            b.shift(RIGHT * (k * 2.9 - 4.35) + UP * (-2.4 - b.stack.get_bottom()[1]))
        legend = VGroup(*[VGroup(Square(0.22, stroke_width=0, fill_color=c, fill_opacity=0.85),
                                 label(t, font_size=24)).arrange(RIGHT, buff=0.12)
                          for c, t in [(C.WEIGHTS, r"weights"), (C.GRADS, r"gradients"),
                                       (C.OPT_STATE, r"optimizer state")]]).arrange(RIGHT, buff=0.5)
        head = label(r"Memory per GPU: a 7.5B model on 64 GPUs", font_size=36).to_edge(UP, buff=0.4)
        legend.next_to(head, DOWN, buff=0.2)
        src = source(r"Rajbhandari et al., \emph{ZeRO} (2019); PyTorch FSDP")
        with self.voiceover(
            "But in plain data parallelism, every GPU still stores all sixteen bytes per parameter. ZeRO, and "
            "PyTorch's FSDP, shard that state instead. <bookmark mark='a'/> For a 7.5-billion-parameter model on "
            "sixty-four GPUs, that's 120 gigabytes per GPU. <bookmark mark='b'/> Split the optimizer state sixty-four "
            "ways, and it drops to 31. <bookmark mark='c'/> Shard the gradients too: 17. <bookmark mark='d'/> Shard "
            "the weights themselves, gathering each layer just before it's needed: under two gigabytes. "
            "<bookmark mark='e'/> The price is more communication: about one and a half times that of plain data "
            "parallelism."
        ) as vo:
            self.play(FadeIn(head), FadeIn(legend), FadeIn(src))
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(GrowFromEdge(bars[k][0], DOWN), FadeIn(bars[k][1]), FadeIn(bars[k][2]), run_time=0.9)
        self.wait(0.4)
        self.clear_scene()
