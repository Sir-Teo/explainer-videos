from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai17.common import (BYTEC, COMMC, CPUC, FLOPC, GPUC, PART, box_label, load, ring_devices)
from videos.ai.ai17.specs import GPUS, IB_NDR, LLAMA31_GPUS, NVL72_GB200, NVL72_RUBIN, NVLINK

CHUNK_C = [C.EMBED, C.MOMENTUM, C.PROB, C.MLP]


class Interconnect(VoiceoverScene):
    def construct(self):
        self.card()
        self.why()
        self.links()
        self.alpha_beta()
        self.ring()
        self.ring_vs_tree()

    def card(self):
        card = chapter_card(10, r"Interconnect and collectives", r"What happens when one chip isn't enough?",
                            part=PART)
        with self.voiceover("Chapter ten. Interconnect and collectives."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def why(self):
        H = GPUS["H100"]
        params = 405e9
        w16 = params * 2
        train = params * 16
        need = math.ceil(train / H["mem"])
        rows = VGroup(
            label(rf"Llama 3.1 405B: \ weights in 16 bits $= {w16 / 1e9:.0f}$ GB", font_size=26, color=WHITE),
            label(rf"training state, $\approx 16$ bytes per parameter $\approx {train / 1e12:.1f}$ TB", font_size=26,
                  color=WHITE),
            label(rf"one H100 holds ${H['mem'] / 1e9:.0f}$ GB: \ at least ${need}$ GPUs just to hold it", font_size=26,
                  color=GPUC),
            label(rf"trained on ${LLAMA31_GPUS:,}$ of them".replace(",", "{,}"), font_size=26, color=GPUC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([-2.6, 1.4, 0])
        bws = [(r"HBM", H["bw"], BYTEC), (r"NVLink 4", H["link"], COMMC), (r"InfiniBand NDR", 2 * IB_NDR, GREY_B)]
        bars, labs = VGroup(), VGroup()
        mx = math.log10(bws[0][1] / 1e9)
        for k, (nm, v, c_) in enumerate(bws):
            w = 0.6 + 4.8 * math.log10(v / 1e9) / mx
            y = -1.2 - 0.7 * k
            bars.add(Rectangle(width=w, height=0.45, stroke_width=0, fill_color=c_, fill_opacity=0.85)
                     .move_to([-2.4 + w / 2, y, 0]))
            labs.add(VGroup(label(nm, font_size=22, color=c_).next_to([-2.6, y, 0], LEFT, buff=0.1),
                            label(rf"${v / 1e9:,.0f}$ GB/s".replace(",", "{,}"), font_size=22).next_to(bars[-1], RIGHT,
                                                                                                    buff=0.15)))
        bh = label(r"an H100's bandwidths \ (both directions; log scale)", font_size=22, color=GREY_A)
        bh.next_to(bars, UP, buff=0.25).align_to(bars, LEFT).shift(LEFT * 1.5)
        cite_ = cite(r"Meta (2024); \ NVIDIA H100 datasheet; \ InfiniBand NDR: $400$ Gb/s per direction", corner=DR)
        with self.voiceover(
            "A frontier model doesn't fit on one chip. <bookmark mark='a'/> Llama 3.1's 405 billion parameters "
            "take 810 gigabytes in sixteen-bit numbers; training, with gradients and the optimizer's state, needs "
            f"about sixteen bytes per parameter, some {train / 1e12:.1f} terabytes. An H100 holds eighty gigabytes, "
            f"so at least {need} of them just to hold it, and Meta trained it on 16,384. <bookmark mark='b'/> "
            "So the chips have to talk, and every step away is slower. Inside the GPU, its memory: 3.35 terabytes "
            "a second. Between GPUs in one server, NVLink: 900 gigabytes a second. Between servers, an InfiniBand "
            "network: about a hundred. Each step costs about a factor of ten."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(cite_))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in rows[1:]], lag_ratio=0.6), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(bh), LaggedStart(*[AnimationGroup(GrowFromEdge(bars[k], LEFT), FadeIn(labs[k]))
                                                for k in range(3)], lag_ratio=0.6), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def links(self):
        yrs = [y for y, _, _ in NVLINK]
        g = axes([2015.5, 2026.5], [0, 3.3], x_length=5.6, y_length=3.4, xlabel=r"year",
                 ylabel=r"NVLink per GPU, \ TB/s", xticks=[2016, 2020, 2024], yticks=[0, 1, 2, 3],
                 center=[-3.6, 0.2, 0])
        dots = VGroup(*[Dot(g.ax.c2p(y, v / 1e12), radius=0.07, color=COMMC) for y, _, v in NVLINK])
        names = VGroup(*[label(nm.split(" (")[1].rstrip(")"), font_size=16, color=GREY_A)
                         .next_to(d_, UP if k % 2 == 0 else LEFT, buff=0.1) for k, (d_, (_, nm, _)) in
                         enumerate(zip(dots, NVLINK))])
        # topologies, schematic
        def sw(center):
            nodes = VGroup(*[Dot(np.asarray(center) + 0.8 * np.array([math.cos(a), math.sin(a), 0]), radius=0.07,
                                 color=GPUC) for a in np.linspace(0, 2 * PI, 9)[:-1]])
            hub = Square(0.32, stroke_color=COMMC, fill_color=COMMC, fill_opacity=0.4).move_to(center)
            lines = VGroup(*[Line(hub.get_center(), n.get_center(), stroke_width=1.2, color=COMMC) for n in nodes])
            return VGroup(lines, hub, nodes)

        def torus(center, k=4):
            pts = [[np.asarray(center) + 0.42 * np.array([i - 1.5, j - 1.5, 0]) for j in range(k)] for i in range(k)]
            lines = VGroup()
            for i in range(k):
                for j in range(k):
                    lines.add(Line(pts[i][j], pts[(i + 1) % k][j] if i + 1 < k else pts[i][j], stroke_width=1,
                                   color=COMMC))
                    lines.add(Line(pts[i][j], pts[i][(j + 1) % k] if j + 1 < k else pts[i][j], stroke_width=1,
                                   color=COMMC))
                lines.add(ArcBetweenPoints(pts[i][0], pts[i][k - 1], angle=-0.9, stroke_width=1, color=COMMC))
                lines.add(ArcBetweenPoints(pts[0][i], pts[k - 1][i], angle=0.9, stroke_width=1, color=COMMC))
            dots_ = VGroup(*[Dot(p, radius=0.06, color=GPUC) for row in pts for p in row])
            return VGroup(lines, dots_)

        def fat(center):
            c = np.asarray(center)
            leaves = VGroup(*[Dot(c + np.array([-1.05 + 0.3 * i, -0.7, 0]), radius=0.06, color=GPUC) for i in range(8)])
            mid = VGroup(*[Square(0.18, stroke_color=COMMC, fill_color=COMMC, fill_opacity=0.4)
                           .move_to(c + np.array([-0.9 + 0.6 * i, 0.0, 0])) for i in range(4)])
            top = VGroup(*[Square(0.18, stroke_color=COMMC, fill_color=COMMC, fill_opacity=0.4)
                           .move_to(c + np.array([-0.3 + 0.6 * i, 0.7, 0])) for i in range(2)])
            lines = VGroup(*[Line(leaves[i].get_center(), mid[i // 2].get_center(), stroke_width=1, color=COMMC)
                             for i in range(8)],
                           *[Line(m.get_center(), t.get_center(), stroke_width=1.6, color=COMMC) for m in mid
                             for t in top])
            return VGroup(lines, leaves, mid, top)

        topo = VGroup(sw([1.6, 1.4, 0]), fat([4.9, 1.4, 0]), torus([1.6, -1.6, 0]))
        tl = VGroup(label(r"a switch: \ all to all \ (NVLink domain)", font_size=18, color=GREY_A)
                    .next_to(topo[0], DOWN, buff=0.15),
                    label(r"a fat tree \ (Leiserson, 1985)", font_size=18, color=GREY_A).next_to(topo[1], DOWN, buff=0.15),
                    label(r"a 3D torus \ (TPU pods)", font_size=18, color=GREY_A).next_to(topo[2], DOWN, buff=0.15))
        rack = VGroup(label(rf"NVL72: \ ${NVL72_GB200['gpus']}$ GPUs, \ one switch fabric", font_size=22, color=COMMC),
                      label(rf"${NVL72_GB200['nvlink'] / 1e12:.0f}$ TB/s \ $\to$ \ "
                            rf"${NVL72_RUBIN['nvlink'] / 1e12:.0f}$ TB/s \ (Rubin)", font_size=22, color=COMMC))
        rack.arrange(DOWN, buff=0.12).move_to([4.9, -0.25, 0])
        tpu = VGroup(label(r"TPU v4: \ $4{,}096$ chips,", font_size=20, color=GREY_A),
                     label(r"optical circuit switches", font_size=20, color=GREY_A),
                     label(r"(Jouppi et al.\ 2023)", font_size=18, color=GREY_B))
        tpu.arrange(DOWN, buff=0.1).move_to([4.9, -1.75, 0])
        tag = schematic_tag(corner=UR)
        cite_ = cite(r"NVIDIA NVLink page; \ P100, V100, A100 datasheets", corner=DL)
        with self.voiceover(
            "NVIDIA built its own links. <bookmark mark='a'/> NVLink arrived with the P100 in 2016, 160 gigabytes a "
            "second per GPU; each generation since has roughly doubled it, to three terabytes a second for Rubin in "
            "2026. <bookmark mark='b'/> Links need a shape. A switch connects everything to everything: NVIDIA's "
            "NVL72 racks put seventy-two GPUs on one NVLink fabric, 130 terabytes a second in all, 216 in the Rubin "
            "generation. <bookmark mark='c'/> Between racks, a fat tree, Charles Leiserson's design of 1985: more "
            "links higher up, so the top isn't a bottleneck. <bookmark mark='d'/> Google wires its TPUs in a "
            "three-dimensional torus, each chip linked to its six neighbours, and since TPU v4 reconfigures it with "
            "optical switches, 4,096 chips at a time."
        ) as vo:
            self.play(FadeIn(g), FadeIn(cite_))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(d_, scale=0.5), FadeIn(n_)) for d_, n_ in zip(dots, names)],
                                  lag_ratio=0.3), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(topo[0]), FadeIn(tl[0]), FadeIn(tag), FadeIn(rack))
            vo.wait_until("c")
            self.play(FadeIn(topo[1]), FadeIn(tl[1]))
            vo.wait_until("d")
            self.play(FadeIn(topo[2]), FadeIn(tl[2]), FadeIn(tpu))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def alpha_beta(self):
        c = load("collectives")
        ns, pp = np.asarray(c["sizes"]), np.asarray(c["pingpong"])
        a, B = float(c["alpha"]), float(c["B"])
        colors = {r"\alpha": COMMC, r"\beta": BYTEC, r"n": WHITE}
        law = cmath(r"T(n)", r"=", r"\alpha", r"+", r"\frac{n}{\beta}", colors=colors, font_size=44)
        law.move_to([3.6, 2.3, 0])
        ll = VGroup(label(r"$\alpha$: \ the fixed cost of any message", font_size=22, color=COMMC),
                    label(r"$\beta$: \ bytes per second after that", font_size=22, color=BYTEC))
        ll.arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(law, DOWN, buff=0.3)
        g = axes([0.8, 7.7], [-6, -0.5], x_length=6.2, y_length=4.2, xlabel=r"message size, \ bytes",
                 ylabel=r"one-way time, \ seconds (log)", xticks=[1, 3, 5, 7], yticks=[-5, -3, -1],
                 xfmt=lambda v: {1: "10", 3: r"10^3", 5: r"10^5", 7: r"10^7"}[int(v)],
                 yfmt=lambda v: rf"10^{{{int(v)}}}", center=[-3.0, -0.3, 0])
        pts = VGroup(*[Dot(g.ax.c2p(math.log10(n), math.log10(t)), radius=0.06, color=CPUC) for n, t in zip(ns, pp)])
        xs = np.linspace(0.9, 7.6, 100)
        fit = curve(g.ax, xs, np.log10(a + 10 ** xs / B), COMMC, 3)
        fl = label(rf"fit: \ $\alpha \approx {a * 1e6:.0f}\ \mu$s, \ $\beta \approx {B / 1e9:.1f}$ GB/s", font_size=24,
                   color=COMMC).move_to([3.6, -0.6, 0])
        knee = a * B
        kl = label(rf"$\alpha\beta \approx {knee / 1e3:.0f}$ KB: \ below it, latency rules", font_size=22,
                   color=GREY_A).next_to(fl, DOWN, buff=0.25)
        tag = note(rf"computed: \ two processes on this computer, \ messages through a pipe").to_corner(DR, buff=0.2)
        hist = note(r"the latency--bandwidth model: \ Hockney (1994)").to_corner(UR, buff=0.2)
        with self.voiceover(
            "To reason about communication, use the simplest model that works. <bookmark mark='a'/> Sending a "
            "message of n bytes costs a fixed alpha, the latency, plus n over beta, the bandwidth. "
            "<bookmark mark='b'/> We measured it between two processes on this computer, passing messages from eight "
            f"bytes to thirty-two megabytes. <bookmark mark='c'/> The fit: alpha about {a * 1e6:.0f} microseconds, "
            f"beta about {B / 1e9:.1f} gigabytes a second. <bookmark mark='d'/> Below alpha times beta, about "
            f"{round(knee / 1e3, -1):.0f} kilobytes here, a message costs the same whatever its size; above it, "
            "bandwidth is everything. On a GPU cluster the numbers change, microseconds and hundreds of gigabytes a "
            "second, but the shape doesn't."
        ) as vo:
            self.play(FadeIn(g), FadeIn(hist))
            vo.wait_until("a")
            self.play(Write(law), FadeIn(ll))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p_, scale=0.5) for p_ in pts], lag_ratio=0.06), FadeIn(tag))
            vo.wait_until("c")
            self.play(Create(fit), FadeIn(fl))
            vo.wait_until("d")
            self.play(FadeIn(kl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ring(self):
        c = load("collectives")
        states, sends = np.asarray(c["states"]), np.asarray(c["sends"])
        p = states.shape[1]
        devs = ring_devices(p, radius=2.0, center=[-3.4, -0.4, 0], size=1.0, color=GPUC)
        cell = 0.3

        def chunk(r, k, v, contrib):
            sq = Square(cell, stroke_width=1, stroke_color=CHUNK_C[k], fill_color=CHUNK_C[k],
                        fill_opacity=0.15 + 0.8 * contrib / p)
            t = Integer(int(v), font_size=16, color=WHITE).move_to(sq)
            return VGroup(sq, t)

        def place(r, k):
            box = devs[r][0]
            return box.get_center() + np.array([(k - (p - 1) / 2) * (cell + 0.04), -0.05, 0])

        contrib = np.ones((p, p), int)
        chunks = [[chunk(r, k, states[0][r, k], 1).move_to(place(r, k)) for k in range(p)] for r in range(p)]
        allc = VGroup(*[ch for row in chunks for ch in row])
        colors = {r"\alpha": COMMC, r"\beta": BYTEC, r"p": GPUC, r"n": WHITE}
        rows = [
            cmath(r"\text{reduce-scatter}", r":", r"(p-1)\big(\alpha + \tfrac{n}{p\beta}\big)", colors=colors,
                  font_size=30),
            cmath(r"\text{all-gather}", r":", r"(p-1)\big(\alpha + \tfrac{n}{p\beta}\big)", colors=colors,
                  font_size=30),
            cmath(r"T_{\text{ring}}", r"=", r"2(p-1)\,\alpha + 2\,\tfrac{p-1}{p}\,\tfrac{n}{\beta}", colors=colors,
                  font_size=32),
        ]
        whys = [why(r"$p - 1$ steps, \ a $1/p$ chunk each", font_size=20),
                why(r"pass the finished chunks around", font_size=20),
                why(r"bandwidth term: \ under $2n/\beta$, \ whatever $p$", font_size=20)]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=3.4, buff=0.55, edge=6.9)
        title = label(r"all-reduce: \ every GPU ends with the sum", font_size=26, color=GPUC).to_corner(UL, buff=0.35)
        tag = note(r"computed: \ the trace of a ring all-reduce; \ every GPU ends with the sum").to_corner(DR, buff=0.2)
        hist = note(r"Patarasuk \& Yuan (2009); \ Baidu (2017); \ NCCL").to_corner(DL, buff=0.2)

        def do_step(s):
            anims, moving = [], []
            for (src, dst, k) in sends[s]:
                mv = chunks[src][k].copy()
                moving.append(mv)
                anims.append(mv.animate.move_to(place(dst, k)).set_opacity(0.0))
            self.play(*anims, run_time=0.8)
            for mv in moving:
                self.remove(mv)
            new_anims = []
            for (src, dst, k) in sends[s]:
                if s < p - 1:
                    contrib[dst, k] += contrib[src, k]
                else:
                    contrib[dst, k] = p
                nc = chunk(dst, k, states[s + 1][dst, k], min(contrib[dst, k], p)).move_to(place(dst, k))
                new_anims.append(Transform(chunks[dst][k], nc))
            self.play(*new_anims, run_time=0.4)

        with self.voiceover(
            "Training on many GPUs means, every step, adding up everyone's gradients so that all of them get the "
            "total: an all-reduce. <bookmark mark='a'/> The ring algorithm splits each GPU's data into p chunks. "
            "<bookmark mark='b'/> In each step, every GPU sends one chunk to its neighbour and adds the chunk it "
            "receives to its own. After p minus one steps, each GPU holds one chunk of the full sum. "
            "<bookmark mark='c'/> Then p minus one more steps pass the finished chunks around, until every GPU has "
            "all of them. <bookmark mark='d'/> Each step sends n over p bytes, so the total time is two times p minus "
            "one alphas, plus two times p minus one over p, times n over beta. The bandwidth term never exceeds two "
            "n over beta, however many GPUs there are, and no algorithm can do better on it. Part 18 builds data "
            "parallelism on this."
        ) as vo:
            self.play(FadeIn(devs), FadeIn(allc), FadeIn(title), FadeIn(tag), FadeIn(hist))
            vo.wait_until("a")
            self.play(Indicate(allc, scale_factor=1.05))
            vo.wait_until("b")
            for s in range(p - 1):
                do_step(s)
            step(0)
            vo.wait_until("c")
            for s in range(p - 1, 2 * (p - 1)):
                do_step(s)
            step(1)
            vo.wait_until("d")
            step(2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ring_vs_tree(self):
        c = load("collectives")
        nu = np.asarray(c["nu"])
        ps = [int(x) for x in np.asarray(c["ps"])]
        g = axes([-2, 4], [0, 4.5], x_length=6.4, y_length=4.0, xlabel=r"message size $n$, \ in units of $\alpha\beta$",
                 ylabel=r"time, \ in units of $\alpha$ \ (log)", xticks=[-2, 0, 2, 4], yticks=[0, 2, 4],
                 xfmt=lambda v: {-2: "0.01", 0: "1", 2: "100", 4: r"10^4"}[int(v)],
                 yfmt=lambda v: {0: "1", 2: "100", 4: r"10^4"}[int(v)], center=[-2.6, -0.3, 0])
        cols = [GPUC, FLOPC, COMMC]
        lines = VGroup()
        for k, p_ in enumerate(ps):
            ring, tree = np.asarray(c[f"model_{p_}"])
            lines.add(VGroup(curve(g.ax, np.log10(nu), np.log10(ring), cols[k], 3),
                             DashedVMobject(curve(g.ax, np.log10(nu), np.log10(tree), cols[k], 3), num_dashes=40)))
        lg = VGroup(legend([(cols[k], rf"$p = {p_}$") for k, p_ in enumerate(ps)], font_size=20),
                    label(r"solid: ring; \ dashed: tree", font_size=20, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                             buff=0.2)
        lg.move_to([4.2, 1.8, 0])
        colors = {r"\alpha": COMMC, r"\beta": BYTEC, r"p": GPUC}
        tree_eq = cmath(r"T_{\text{tree}}", r"=", r"2 \log_2 p\,\big(\alpha + \tfrac{n}{\beta}\big)", colors=colors,
                        font_size=30).move_to([4.2, -0.2, 0])
        cross = c["cross"]
        cl = label(rf"ring wins above $n \approx {cross[str(ps[0])]:.1f}\,\alpha\beta$ \ ($p = {ps[0]}$), \ "
                   rf"${cross[str(ps[-1])]:.0f}\,\alpha\beta$ \ ($p = {ps[-1]}$)", font_size=20, color=GREY_A)
        cl.next_to(tree_eq, DOWN, buff=0.3)
        if cl.width > 5.0:
            cl.width = 5.0
        nv = GPUS["H100"]["link"] / 2
        ex = label(rf"NVLink 4, \ $\alpha = 5\,\mu$s (illustrative): \ $\alpha\beta \approx {5e-6 * nv / 1e6:.2f}$ MB",
                   font_size=20, color=GREY_B).next_to(cl, DOWN, buff=0.3)
        if ex.width > 5.2:
            ex.width = 5.2
        # measured on this machine: 4 processes
        ns, rm, tm = np.asarray(c["sizes"]), np.asarray(c["ring"]), np.asarray(c["tree"])
        rp, tp = np.asarray(c["ring_pred"]), np.asarray(c["tree_pred"])
        big = ns >= 64 * 1024
        err = float(np.median(np.abs(np.log10(np.concatenate([rm[big] / rp[big], tm[big] / tp[big]])))))
        good = err < math.log10(2)
        r_ratio = float(np.median(rm[big] / rp[big]))
        t_ratio = float(np.median(tm[big] / tp[big]))
        if good:
            ml = label(r"measured here, \ 4 processes: \ within $\times 2$ of the model", font_size=20, color=CPUC)
        else:
            ml = label(rf"measured here, \ 4 processes: \ ring ${r_ratio:.0f}\times$, \ tree ${t_ratio:.0f}\times$ "
                       r"the model's time", font_size=20, color=CPUC)
        ml.next_to(ex, DOWN, buff=0.3)
        if ml.width > 5.2:
            ml.width = 5.2
        # a schematic of the tree: pairs, then pairs of pairs
        lv = [[np.array([4.2 + 0.4 * 2 ** (3 - k) * (i - (2 ** k - 1) / 2), 1.15 + 0.55 * (3 - k), 0])
               for i in range(2 ** k)] for k in range(4)]
        tree_pic = VGroup(
            *[Line(lv[k][i], lv[k + 1][j], stroke_width=1.6, color=COMMC) for k in range(3) for i in range(2 ** k)
              for j in (2 * i, 2 * i + 1)],
            *[Dot(q, radius=0.07, color=GPUC) for row in lv for q in row])
        tree_tag = schematic_tag(corner=UR)
        if good:
            meas = (f"On this computer's four processes, the measured times follow the model within a factor of two "
                    "for large messages, and the ring overtakes the tree where the model says.")
        else:
            meas = ("We also timed both on four processes of this computer, but with every core shared with other "
                    "jobs, the measurements ran several times slower than the model and too noisy to check it: the "
                    "model describes a network, not a busy operating system.")
        tag = note(r"computed: \ the $\alpha$--$\beta$ model").to_corner(DR, buff=0.2)
        with self.voiceover(
            "There's another way: a tree. <bookmark mark='a'/> Add pairs, then pairs of pairs, up to one GPU, and "
            "send the total back down. That's two log p steps instead of two p, but each step sends the whole "
            "message. <bookmark mark='b'/> Here are both, in units of the latency, for eight, sixty-four and 512 "
            "GPUs. For small messages the tree wins: fewer steps. For large ones the ring wins: less data per "
            f"step. <bookmark mark='c'/> With 512 GPUs the crossover is near {cross[str(ps[-1])]:.0f} alpha beta. "
            "With a few microseconds of latency and NVLink's bandwidth, alpha beta is a few megabytes, and gradients "
            "are gigabytes: rings for bulk data, trees for latency, and libraries like NVIDIA's NCCL choose for you. "
            "<bookmark mark='d'/> " + meas
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag), Write(tree_eq))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in tree_pic], lag_ratio=0.03), FadeIn(tree_tag), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeOut(tree_pic), FadeOut(tree_tag))
            for k in range(len(ps)):
                self.play(Create(lines[k][0]), Create(lines[k][1]), run_time=1.2)
            self.play(FadeIn(lg))
            vo.wait_until("c")
            self.play(FadeIn(cl), FadeIn(ex))
            vo.wait_until("d")
            self.play(FadeIn(ml, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
