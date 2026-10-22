from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai17.common import BYTEC, FLOPC, GPUC, IDLEC, PART, WARPC, code_lines, load
from videos.ai.ai17.specs import CC90

IF_C, ELSE_C = C.PROB, C.MOMENTUM


class SIMT(VoiceoverScene):
    def construct(self):
        self.card()
        self.model()
        self.divergence()
        self.latency()
        self.coalescing()

    def card(self):
        card = chapter_card(3, r"Warps, divergence and latency", r"How do thousands of threads share one chip?",
                            lit=(2007,), part=PART)
        with self.voiceover("Chapter three. Warps, divergence and latency."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def lanes(self, n=32, w=0.28, colors=None, h=0.7) -> VGroup:
        g = VGroup(*[Rectangle(width=w, height=h, stroke_width=1, stroke_color=GREY_D,
                               fill_color=(colors[i] if colors else WARPC), fill_opacity=0.8) for i in range(n)])
        return g.arrange(RIGHT, buff=0.04)

    def model(self):
        code = code_lines([
            "__global__ void saxpy(int n, float a, float *x, float *y) {",
            "    int i = blockIdx.x * blockDim.x + threadIdx.x;",
            "    if (i < n) y[i] = a * x[i] + y[i];",
            "}",
            "saxpy<<<(n + 255) / 256, 256>>>(n, 2.0f, x, y);",
        ], font_size=19)
        code.to_edge(UP, buff=0.5).to_edge(LEFT, buff=0.6)
        hl = SurroundingRectangle(code[4], color=GPUC, buff=0.06, stroke_width=2)
        # grid -> blocks -> warps
        blocks = VGroup(*[RoundedRectangle(width=0.8, height=0.55, corner_radius=0.06, stroke_color=GPUC,
                                           stroke_width=1.5, fill_color=GPUC, fill_opacity=0.12) for _ in range(12)])
        blocks.arrange_in_grid(rows=2, cols=6, buff=0.12).move_to([-4.0, -0.9, 0])
        bl = label(r"a grid of blocks", font_size=22, color=GPUC).next_to(blocks, DOWN, buff=0.2)
        warps = VGroup(*[self.lanes(32, w=0.12, h=0.22) for _ in range(8)]).arrange(DOWN, buff=0.08)
        warps.move_to([2.9, -0.9, 0])
        wl = label(r"one block: \ $256$ threads $=$ $8$ warps of $32$", font_size=22, color=WARPC)
        wl.next_to(warps, DOWN, buff=0.2)
        zoom = DashedVMobject(Polygon(blocks[0].get_corner(UR), warps.get_corner(UL) + LEFT * 0.1,
                                      warps.get_corner(DL) + LEFT * 0.1, blocks[0].get_corner(DR),
                                      stroke_color=GREY_C, stroke_width=1.2), num_dashes=40)
        simt = definition_card(r"SIMT", r"single instruction, multiple threads: \ the $32$ threads of a warp run "
                               r"the same instruction together, \ each on its own data", width=5.6, font_size=21,
                               color=WARPC).move_to([3.95, 1.25, 0])
        with self.voiceover(
            "Here is a CUDA program. <bookmark mark='a'/> The function, a kernel, says what one thread does: work "
            "out which element is mine from my block number and my thread number, and update that element. "
            "<bookmark mark='b'/> The launch asks for enough blocks of 256 threads to cover the array: for a "
            "million elements, about four thousand blocks. <bookmark mark='c'/> The hardware hands blocks to "
            "streaming multiprocessors, and splits each block into warps of thirty-two threads. <bookmark mark='d'/> "
            "The thirty-two threads of a warp execute the same instruction at the same moment, each on its own "
            "data. NVIDIA calls it SIMT, single instruction, multiple threads: a vector machine that you program "
            "one thread at a time."
        ) as vo:
            self.play(FadeIn(code))
            vo.wait_until("a")
            self.play(Indicate(VGroup(code[1], code[2]), color=FLOPC, scale_factor=1.02))
            vo.wait_until("b")
            self.play(Create(hl), FadeIn(blocks, lag_ratio=0.1), FadeIn(bl))
            vo.wait_until("c")
            self.play(Create(zoom), FadeIn(warps, lag_ratio=0.1), FadeIn(wl))
            vo.wait_until("d")
            self.play(FadeIn(simt, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def divergence(self):
        w = load("warps")
        g = np.random.Generator(np.random.PCG64(32))
        taken = g.random(32) < 0.5
        cols = [IF_C if t else ELSE_C for t in taken]
        warp = self.lanes(32, w=0.17, colors=cols).move_to([-3.2, 1.6, 0])
        code = code_lines(["if (x[i] > 0)  y[i] = f(x[i]);", "else           y[i] = g(x[i]);"], font_size=20)
        code.next_to(warp, UP, buff=0.3)
        code[0].set_color(IF_C)
        code[1].set_color(ELSE_C)
        pass1 = self.lanes(32, w=0.17, colors=[IF_C if t else IDLEC for t in taken]).move_to([-3.2, 0.1, 0])
        pass2 = self.lanes(32, w=0.17, colors=[ELSE_C if not t else IDLEC for t in taken]).move_to([-3.2, -1.0, 0])
        p1 = label(r"pass 1", font_size=20, color=IF_C).next_to(pass1, RIGHT, buff=0.15)
        p2 = label(r"pass 2", font_size=20, color=ELSE_C).next_to(pass2, RIGHT, buff=0.15)
        qs, er, es = np.asarray(w["qs"]), np.asarray(w["eff_rand"]), np.asarray(w["eff_sort"])
        ax = axes([0, 1], [0, 1.05], x_length=4.6, y_length=2.6, xlabel=r"fraction of threads taking the if",
                  ylabel=r"useful work per lane-slot", xticks=[0, 0.5, 1], yticks=[0, 0.5, 1],
                  yfmt=lambda v: rf"{int(100 * v)}\%", center=[3.9, -0.4, 0])
        cr, cs = curve(ax.ax, qs, er, C.SURPRISE, 3), curve(ax.ax, qs, es, GPUC, 3)
        lg = legend([(C.SURPRISE, r"random data"), (GPUC, r"sorted first")], font_size=18)
        lg.next_to(ax.ax, UP, buff=0.05).align_to(ax.ax, RIGHT)
        mid = float(er[len(er) // 2])
        tag = note(rf"simulated: \ ${int(32 * 4096):,}$ threads".replace(",", "{,}")).to_corner(DR, buff=0.2)
        verdict = (f"Random data diverges in almost every warp, and the warp does about {100 * mid:.0f} percent useful "
                   "work. Sort the data first, so that neighbours agree, and only the warps at the boundary split.")
        with self.voiceover(
            "Lockstep has a price. <bookmark mark='a'/> Suppose the threads of a warp reach an if, and some take "
            "it and some don't. <bookmark mark='b'/> The warp can only issue one instruction at a time, so it runs "
            "the if-branch with the other threads masked off, <bookmark mark='c'/> then the else-branch with the "
            "first group masked off. Both paths cost the whole warp. That's divergence. <bookmark mark='d'/> We "
            "simulated a branch on data across four thousand warps. " + verdict
        ) as vo:
            self.play(FadeIn(warp), FadeIn(code))
            vo.wait_until("a")
            self.play(Indicate(warp, scale_factor=1.03))
            vo.wait_until("b")
            self.play(TransformFromCopy(warp, pass1), FadeIn(p1))
            vo.wait_until("c")
            self.play(TransformFromCopy(warp, pass2), FadeIn(p2))
            vo.wait_until("d")
            self.play(FadeIn(ax), FadeIn(tag))
            self.play(Create(cr), FadeIn(lg[0]), run_time=1.5)
            self.play(Create(cs), FadeIn(lg[1]), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def latency(self):
        w = load("warps")
        Ws, cs = np.asarray(w["Ws"]), np.asarray(w["cs"])
        U, Th = np.asarray(w["util"]), np.asarray(w["theory"])
        lat = int(w["lat"])
        ax = axes([0, 16], [0, 1.05], x_length=6.4, y_length=3.8, xlabel=r"warps on one scheduler",
                  ylabel=r"cycles that issue an instruction", xticks=[1, 4, 8, 12, 16], yticks=[0, 0.5, 1],
                  yfmt=lambda v: rf"{int(100 * v)}\%", center=[-2.2, -0.4, 0])
        cols = [C.SURPRISE, FLOPC, GPUC]
        sim = VGroup(*[VGroup(*[Dot(ax.ax.c2p(x, y), radius=0.055, color=cols[k]) for x, y in zip(Ws, U[k])])
                       for k in range(len(cs))])
        th = VGroup(*[curve(ax.ax, Ws, Th[k], cols[k], 2).set_stroke(opacity=0.6) for k in range(len(cs))])
        lg = legend([(cols[k], rf"${int(cs[k])}$ operations per load") for k in range(len(cs))], font_size=20)
        lg.move_to([4.4, 1.6, 0])
        law = cmath(r"\text{warps needed}", r"=", r"\frac{\text{latency} + \text{work}}{\text{work}}", font_size=30)
        law.move_to([4.4, -0.2, 0])
        ll = label(r"Little's law again \ (lines)", font_size=20, color=GREY_B).next_to(law, DOWN, buff=0.2)
        need = [(lat + c + 1) / (c + 1) for c in cs]
        u_lo = float(U[0, -1])
        k_hi = int(np.argmax(U[-1] >= 0.99)) + 1
        hw = label(rf"an H100 SM: \ $4$ schedulers, \ up to ${CC90['warps']}$ warps", font_size=22, color=GPUC)
        hw.next_to(ll, DOWN, buff=0.4)
        tag = note(rf"simulated: \ a load takes ${lat}$ cycles \ (H800, Luo et al.\ 2024)").to_corner(DR, buff=0.2)
        intro = VGroup(label(r"one scheduler: \ one instruction a cycle", font_size=22, color=WARPC),
                       label(r"each warp: \ some work, \ then a load", font_size=22, color=GREY_A),
                       label(rf"each load: \ ${lat}$ cycles away", font_size=22, color=BYTEC))
        intro.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.4, -0.2, 0])
        with self.voiceover(
            "Now the reason for all those threads. A load from memory takes hundreds of cycles; while a warp waits, "
            "the scheduler issues instructions from another warp that's ready. <bookmark mark='a'/> We simulated "
            f"one scheduler with memory {lat} cycles away, the latency measured on a Hopper GPU. "
            "<bookmark mark='b'/> If each warp does only four operations per load, even sixteen warps keep it busy "
            f"just {100 * u_lo:.0f} percent of the time. <bookmark mark='c'/> With sixty-four operations per load, "
            f"{k_hi} warps are enough. <bookmark mark='d'/> The lines are Little's law: you need the latency plus "
            "the work, divided by the work, warps in flight. An H100's multiprocessor has four schedulers and room "
            "for sixty-four warps. Past that, the only way to hide latency is more arithmetic per byte, an idea "
            "that comes back in chapter five."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), LaggedStart(*[FadeIn(i_) for i_ in intro], lag_ratio=0.4))
            vo.wait_until("a")
            self.play(Indicate(intro[2], color=BYTEC))
            vo.wait_until("b")
            self.play(FadeIn(lg[0]), LaggedStart(*[FadeIn(d) for d in sim[0]], lag_ratio=0.1), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(lg[1]), LaggedStart(*[FadeIn(d) for d in sim[1]], lag_ratio=0.1), run_time=1.2)
            self.play(FadeIn(lg[2]), LaggedStart(*[FadeIn(d) for d in sim[2]], lag_ratio=0.1), run_time=1.2)
            vo.wait_until("d")
            self.play(FadeOut(intro))
            self.play(*[Create(t_) for t_ in th], Write(law), FadeIn(ll), run_time=1.5)
            self.play(FadeIn(hw))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def coalescing(self):
        lanes = self.lanes(32, w=0.2).move_to([0, 2.2, 0])
        ll = label(r"a warp's $32$ loads", font_size=22, color=WARPC).next_to(lanes, UP, buff=0.15)
        segs = VGroup(*[Rectangle(width=1.6, height=0.5, stroke_color=BYTEC, stroke_width=1.5, fill_color=BYTEC,
                                  fill_opacity=0.1) for _ in range(8)]).arrange(RIGHT, buff=0.05).move_to([0, -0.2, 0])
        sl = label(r"memory, \ in $128$-byte segments", font_size=22, color=BYTEC).next_to(segs, DOWN, buff=0.15)
        good = VGroup(*[Line(l.get_bottom(), segs[3].get_top() + RIGHT * (k - 15.5) * 0.045, color=GPUC,
                             stroke_width=1.5) for k, l in enumerate(lanes)])
        g = np.random.Generator(np.random.PCG64(5))
        tgt = g.integers(0, 8, 32)
        bad = VGroup(*[Line(l.get_bottom(), segs[int(tgt[k])].get_top() + RIGHT * g.uniform(-0.6, 0.6),
                            color=C.SURPRISE, stroke_width=1.5) for k, l in enumerate(lanes)])
        n_bad = len(set(int(x) for x in tgt))
        gl = label(r"neighbouring addresses: \ one transaction", font_size=24, color=GPUC).to_edge(DOWN, buff=0.9)
        bl_ = label(rf"scattered: \ ${n_bad}$ transactions for the same $32$ numbers", font_size=24,
                    color=C.SURPRISE).to_edge(DOWN, buff=0.9)
        tag = schematic_tag(corner=UR)
        with self.voiceover(
            "One more rule of the road. <bookmark mark='a'/> Memory is read in segments of 128 bytes. When the "
            "thirty-two threads of a warp read thirty-two neighbouring numbers, the hardware combines them into one "
            "transaction: the loads are coalesced. <bookmark mark='b'/> When they read scattered addresses, the same "
            "thirty-two numbers cost many transactions, and most of every segment fetched is thrown away. It's the "
            "same lesson as a CPU's cache lines, and it will matter for matrices: walk them along the rows."
        ) as vo:
            self.play(FadeIn(lanes), FadeIn(ll), FadeIn(segs), FadeIn(sl), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(x) for x in good], lag_ratio=0.02), segs[3].animate.set_fill(opacity=0.5),
                      FadeIn(gl))
            vo.wait_until("b")
            self.play(FadeOut(good), FadeOut(gl), segs[3].animate.set_fill(opacity=0.1))
            self.play(LaggedStart(*[Create(x) for x in bad], lag_ratio=0.02),
                      *[segs[int(i)].animate.set_fill(C.SURPRISE, opacity=0.35) for i in set(tgt.tolist())],
                      FadeIn(bl_))
        self.wait(0.3)
        self.clear_scene()
