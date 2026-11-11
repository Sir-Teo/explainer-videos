from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs60.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load


class WSView(VGroup):
    """A weight-stationary N x N grid drawn from ``load("wave")["ws"]``: each cell shows its stationary weight (LAM,
    top right), the activation passing through it (DATA, top left, while busy) and the partial sum it sends down
    (centre).  Waiting weights queue above (the last row of W first, during the load cycles); waiting rows of X queue
    to the left, row k skewed by k.  ``step(t)`` returns the animations that move the drawing to trace cycle t."""

    def __init__(self, ws: dict, size: float = 0.8, gap: float = 0.12, font_size: int = 22):
        super().__init__()
        self.ws, self.n, self.m, self.size, self.fs = ws, ws["n"], ws["m"], size, font_size
        n = self.n
        self.boxes = VGroup(*[Square(size, stroke_color=GREY_B, stroke_width=2, fill_color=BG, fill_opacity=1)
                              for _ in range(n * n)]).arrange_in_grid(n, n, buff=gap)
        z = [[0] * n for _ in range(n)]
        self.wl = VGroup(*[self._w(None, i, j) for i in range(n) for j in range(n)])
        self.xl = VGroup(*[self._x(None, i, j) for i in range(n) for j in range(n)])
        self.pl = VGroup(*[self._p(z[i][j], i, j) for i in range(n) for j in range(n)])
        self.qx, self.qw = self._queues(-1)
        self.add(self.boxes, self.wl, self.xl, self.pl, self.qx, self.qw)

    def box(self, i, j):
        return self.boxes[i * self.n + j]

    def _w(self, v, i, j):
        t = label(rf"{v or 0}", font_size=self.fs - 5, color=LAM)
        t.move_to(self.box(i, j).get_corner(UR) + LEFT * 0.2 * self.size + DOWN * 0.17 * self.size)
        return t.set_opacity(0 if v is None else 1)

    def _x(self, v, i, j):
        t = label(rf"{v or 0}", font_size=self.fs - 5, color=DATA)
        t.move_to(self.box(i, j).get_corner(UL) + RIGHT * 0.2 * self.size + DOWN * 0.17 * self.size)
        return t.set_opacity(0 if v is None else 1)

    def _p(self, v, i, j):
        return label(rf"{v}", font_size=self.fs, color=WHITE if v else GREY_D).move_to(self.box(i, j)).shift(
            DOWN * 0.13 * self.size)

    def _queues(self, t):
        """Inputs still waiting after trace cycle t.  Row t' of the load phase brings W[n-1-t']; X[r][k] enters row k
        at trace cycle n + r + k (drawn at its compute-phase distance, so the queue waits in place while loading)."""
        n, X, W = self.n, self.ws["X"], self.ws["W"]
        step = self.size * 0.58
        qx, qw = VGroup(), VGroup()
        for k in range(n):
            left = self.box(k, 0).get_left()
            for r in range(self.m):
                d = n + r + k - max(t, n - 1)
                q = label(rf"{X[r][k]}", font_size=self.fs - 4, color=DATA).move_to(
                    left + LEFT * (0.05 + max(d, 1) * step))
                qx.add(q.set_opacity(1 if n + r + k > t else 0))
        for tp in range(n):
            d = tp - t
            row = W[n - 1 - tp]
            for j in range(n):
                q = label(rf"{row[j]}", font_size=self.fs - 4, color=LAM).move_to(
                    self.box(0, j).get_top() + UP * (0.02 + max(d, 1) * step * 0.62))
                qw.add(q.set_opacity(1 if d >= 1 else 0))
        return qx, qw

    def step(self, t):
        tr = self.ws["trace"][t]
        n = self.n
        anims = []
        for i in range(n):
            for j in range(n):
                busy = tr["m"][i][j] is not None
                idx = i * n + j
                loaded = tr["w"][i][j] or t >= n or (tr["phase"] == "load" and i <= t)
                anims.append(self.boxes[idx].animate.set_fill(HEAD if busy else BG, opacity=0.28 if busy else 1)
                             .set_stroke(HEAD if busy else GREY_B))
                anims.append(Transform(self.wl[idx], self._w(tr["w"][i][j] if loaded else None, i, j)))
                anims.append(Transform(self.xl[idx], self._x(tr["x"][i][j] if busy else None, i, j)))
                anims.append(Transform(self.pl[idx], self._p(tr["p"][i][j], i, j)))
        qx, qw = self._queues(t)
        anims += [Transform(self.qx, qx), Transform(self.qw, qw)]
        return anims


class Dataflow(VoiceoverScene):
    def construct(self):
        self.card()
        self.stays()
        self.ws_run()
        self.derive()
        self.curves()
        self.scale()

    def card(self):
        card = chapter_card(4, r"Which number stays put", r"Should the grid hold the outputs, \ or the weights?",
                            lit=(2016, 2017), extra=((2016, r"Chen, \ Emer and Sze: \ Eyeriss"),
                                                     (2017, r"Jouppi et al.: \ the TPU")), part=PART)
        with self.voiceover("Chapter four. Which number stays put?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def stays(self):
        head = label(r"Three numbers meet in every multiply-add", font_size=36).to_edge(UP, buff=0.3)

        def mini(title, still, col, who):
            box = Square(1.7, stroke_color=GREY_B, stroke_width=2, fill_color=BG, fill_opacity=1)
            names = {"w": (r"$w$", LAM), "x": (r"$x$", DATA), "p": (r"$p$", WHITE)}
            moving = [k for k in "wxp" if k != still]
            inner = label(names[still][0], font_size=34, color=names[still][1]).move_to(box)
            pin = SurroundingRectangle(inner, color=col, buff=0.12, corner_radius=0.08)
            arr = VGroup()
            for k, (a, b) in zip(moving, ((LEFT, RIGHT), (UP, DOWN))):
                s0 = box.get_center() + a * 1.4
                e0 = box.get_center() + b * 1.4
                arr.add(Arrow(s0, e0, buff=0, color=names[k][1], stroke_width=3, max_tip_length_to_length_ratio=0.1))
                arr.add(label(names[k][0], font_size=26, color=names[k][1]).next_to(s0, a, buff=0.1))
            t = label(title, font_size=25, color=col)
            wl = label(who, font_size=20, color=GREY_A)
            g = VGroup(VGroup(arr, box, inner, pin), t, wl)
            t.next_to(g[0], DOWN, buff=0.35)
            wl.next_to(t, DOWN, buff=0.12)
            return g
        cells = VGroup(mini(r"output-stationary", "p", HEAD, r"chapter 3: \ each sum stays"),
                       mini(r"weight-stationary", "w", LAM, r"the TPU: \ each weight stays"),
                       mini(r"input-stationary", "x", DATA, r"each input stays")).arrange(RIGHT, buff=1.0)
        cells.next_to(head, DOWN, buff=0.75)
        key = label(r"$w$: \ a weight \quad $x$: \ an input \quad $p$: \ a partial sum", font_size=20, color=GREY_A)
        key.next_to(cells, DOWN, buff=0.5)
        why = wrapped_label(r"whatever stays is fetched once and reused from a register; \ Eyeriss \ (Chen, \ Emer and "
                            r"Sze, \ 2016) \ mixes them \ (row-stationary) \ to cut the energy of moving data", 12.0,
                            font_size=20, color=KERN).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Every multiply-add in a neural network touches three numbers: a weight, an input, and the partial sum "
            "they add to. <bookmark mark='a'/> The grid of chapter three kept each partial sum in its cell and moved "
            "both inputs past it. That is output-stationary. <bookmark mark='b'/> But the weights could stay instead, "
            "loaded once, while the inputs flow across and the partial sums flow down. That is weight-stationary, "
            "and it is what Google's TPU does. <bookmark mark='c'/> Or the inputs could stay. <bookmark mark='d'/> "
            "Whatever stays is fetched from memory once and reused from a register beside the multiplier, and a "
            "read from DRAM costs thousands of times the energy of an eight-bit multiply. Yu-Hsin Chen, Joel Emer and Vivienne Sze's Eyeriss chip of 2016 mixed the choices to "
            "minimize that movement. Let us watch the TPU's choice."
        ) as vo:
            self.play(FadeIn(head), FadeIn(key))
            for mk, c in zip("abc", cells):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(why))
        self.wait(0.4)
        self.clear_scene()

    def ws_run(self):
        ws = load("wave")["ws"]
        n, m = ws["n"], ws["m"]
        head = label(r"Weight-stationary, \ cycle by cycle", font_size=36).to_edge(UP, buff=0.3)
        view = WSView(ws)
        view.shift(DOWN * 1.0 + RIGHT * 0.1 - view.boxes.get_center())
        Y = ws["Y"]
        ym = IntegerMatrix([[0] * n for _ in range(m)], h_buff=1.15, v_buff=0.62)
        ym.scale(0.5)
        ents = ym.get_entries()
        vals = VGroup(*[label(rf"{Y[r][j]}", font_size=20, color=YES) for r in range(m) for j in range(n)])
        ents.set_opacity(0)
        yl = label(r"$Y = XW$ \ leaves the bottom", font_size=19, color=YES)
        VGroup(yl, ym).arrange(DOWN, buff=0.15).to_edge(RIGHT, buff=0.25).set_y(-0.6)
        for e, v in zip(ents, vals):
            v.move_to(e)
        clock = label(r"cycle 0", font_size=26, color=HEAD).to_corner(UL, buff=0.5).shift(DOWN * 0.8)
        phase = label(r"load the weights", font_size=21, color=LAM).next_to(clock, DOWN, buff=0.2, aligned_edge=LEFT)
        phase2 = label(r"stream the inputs", font_size=21, color=DATA).move_to(phase, aligned_edge=LEFT)
        xlab = label(rf"rows of $X$ \ ({m} of them)", font_size=19, color=DATA).next_to(view.boxes, LEFT, buff=0.2)
        xlab.next_to(view.qx, DOWN, buff=0.25).align_to(view.qx, LEFT)
        wlab = label(r"$W$, \ last row first", font_size=19, color=LAM).next_to(view.qw, RIGHT, buff=0.3)
        ok = label(rf"{ws['load_cycles']} + {ws['compute_cycles']} cycles; \ "
                   + (r"$Y$ matches the integer product" if ws["correct"] else r"mismatch"), font_size=22,
                   color=YES if ws["correct"] else NO).to_edge(DOWN, buff=0.2)
        out_at = {}
        for r in range(m):
            for j in range(n):
                out_at.setdefault(n + r + (n - 1) + j, []).append(r * n + j)
        with self.voiceover(
            "Here is a weight-stationary grid, at gate level. <bookmark mark='a'/> "
            "First, for four cycles, the weights are shifted down the columns, the last row first, until each cell "
            "holds its own weight, shown in purple. They will not move again. <bookmark mark='b'/> Then the inputs "
            f"stream in from the left, {say(m)} rows of them, each row a step behind the one before. Each cell "
            "multiplies the input passing through by its weight, adds the partial sum arriving from above, and "
            "passes the result down. <bookmark mark='c'/> What comes out of the bottom edge is one entry of the "
            "product, and the next row of inputs is already following behind. The weights were fetched once, and "
            f"used {say(m)} times each; with a longer stream of inputs, they would be used more."
        ) as vo:
            self.play(FadeIn(head), FadeIn(view), FadeIn(clock), FadeIn(xlab), FadeIn(wlab), FadeIn(yl), FadeIn(ym))
            vo.wait_until("a")
            self.play(FadeIn(phase))
            for t in range(len(ws["trace"])):
                if t == n:
                    vo.wait_until("b")
                    self.play(FadeOut(phase), FadeIn(phase2), FadeOut(wlab), run_time=0.5)
                new_clock = label(rf"cycle {t + 1}", font_size=26, color=HEAD).move_to(clock, aligned_edge=LEFT)
                extra = [FadeIn(vals[i], shift=DOWN * 0.1) for i in out_at.get(t, [])]
                self.play(*view.step(t), Transform(clock, new_clock), *extra, run_time=1.0)
                if t == n + 3:
                    vo.wait_until("c")
            self.play(FadeIn(ok))
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        ws = load("wave")["ws"]
        os_ = load("wave")["os"]
        head = label(r"How busy is the grid?", font_size=36).to_edge(UP, buff=0.3)
        r0 = MathTex(r"U", r"=", r"\frac{\text{multiply-adds}}{\text{cells} \times \text{cycles}}", font_size=34)
        os1 = MathTex(r"U_{\text{out}}", r"=", r"\frac{N^3}{N^2\,(3N-2)}", font_size=34)
        os2 = MathTex(r"U_{\text{out}}", r"=", r"\frac{N}{3N-2}", r"\xrightarrow{\;N \to \infty\;}", r"\frac{1}{3}",
                      font_size=34)
        ws1 = MathTex(r"U_{\text{wt}}", r"=", r"\frac{M N^2}{N^2\,(N + M + 2N - 2)}", font_size=34)
        ws2 = MathTex(r"U_{\text{wt}}", r"=", r"\frac{M}{M + 3N - 2}", r"\xrightarrow{\;M \to \infty\;}", r"1",
                      font_size=34)
        for e in (os1, os2):
            e[0].set_color(HEAD)
        for e in (ws1, ws2):
            e[0].set_color(LAM)
        r0.next_to(head, DOWN, buff=0.4)
        left = VGroup(os1, os2).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        right = VGroup(ws1, ws2).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        VGroup(left, right).arrange(RIGHT, buff=1.0, aligned_edge=UP).next_to(r0, DOWN, buff=0.85)
        lw = VGroup(label(r"output-stationary: \ $N^3$ products in $3N-2$ cycles", font_size=19, color=HEAD),
                    label(r"weight-stationary: \ $M$ input rows; \ $N$ to load, \ $M + 2N - 2$ to compute",
                          font_size=19, color=LAM))
        lw[0].next_to(left, UP, buff=0.2).align_to(left, LEFT)
        lw[1].next_to(right, UP, buff=0.2).align_to(right, LEFT)
        n, m = ws["n"], ws["m"]
        checks = VGroup(
            label(rf"chapter 3's grid, \ $N = {n}$: \ {n}/{3 * n - 2} = {n / (3 * n - 2):.2f}; \ simulated "
                  rf"{os_['utilization']:.2f}", font_size=21, color=HEAD),
            label(rf"this chapter's, \ $N = {n}$, \ $M = {m}$: \ {m}/{m + 3 * n - 2} = {m / (m + 3 * n - 2):.3f}; "
                  rf"\ simulated {ws['utilization']:.3f}", font_size=21, color=LAM),
            label(rf"counting only the compute cycles: \ $M/(M + 2N - 2)$ = {m}/{m + 2 * n - 2} = "
                  rf"{m / (m + 2 * n - 2):.2f}; \ simulated {ws['compute_utilization']:.2f}", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(VGroup(left, right), DOWN, buff=0.6).set_x(0)
        with self.voiceover(
            "How much of the time is the grid doing useful work? <bookmark mark='a'/> Call it the utilization: the "
            "multiply-adds done, over the cells times the cycles. <bookmark mark='b'/> The output-stationary grid "
            "does N cubed multiply-adds, on N squared cells, in three N minus two cycles. <bookmark mark='c'/> "
            "Cancel N squared: N over three N minus two, which falls towards one third. For one product, two "
            "thirds of the time a cell is waiting for the wave. "
            "<bookmark mark='d'/> The weight-stationary grid does M N squared multiply-adds for M rows of input, in "
            "N cycles to load and M plus two N minus two to compute. <bookmark mark='e'/> Cancel again: M over M "
            "plus three N minus two. This one tends to one, as the stream of inputs grows longer. "
            "<bookmark mark='f'/> And both formulas agree exactly with the gate-level simulations we just watched."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(r0))
            vo.wait_until("b")
            self.play(FadeIn(lw[0]), Write(os1))
            vo.wait_until("c")
            self.play(TransformMatchingTex(os1.copy(), os2))
            vo.wait_until("d")
            self.play(FadeIn(lw[1]), Write(ws1))
            vo.wait_until("e")
            self.play(TransformMatchingTex(ws1.copy(), ws2))
            vo.wait_until("f")
            self.play(LaggedStart(*[FadeIn(c) for c in checks], lag_ratio=0.4), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def curves(self):
        g = load("gates")["rows"]
        sc = load("scaling")["rows"]
        head = label(r"Utilization against grid size", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[1, 8, 1], y_range=[0, 1, 0.25], x_length=7.3, y_length=4.4, tips=False,
                  axis_config={"color": GREY_D, "include_ticks": True}).to_edge(LEFT, buff=1.1).shift(DOWN * 0.35)
        xt = VGroup(*[label(rf"{2 ** k}", font_size=17, color=GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.12)
                      for k in range(1, 9)])
        yt = VGroup(*[label(rf"{v:g}", font_size=17, color=GREY_B).next_to(ax.c2p(1, v), LEFT, buff=0.12)
                      for v in (0, 0.25, 0.5, 0.75, 1)])
        xl = label(r"$N$ \ (cells per side, \ log scale)", font_size=18, color=GREY_A).next_to(xt, DOWN, buff=0.15)
        specs = [(r"output-stationary: \ $N/(3N-2)$", HEAD, lambda N: N / (3 * N - 2), ("output-stationary", 1),
                  "os", 1),
                 (r"weight-stationary, \ $M = N$: \ $N/(4N-2)$", LAM, lambda N: N / (4 * N - 2),
                  ("weight-stationary", 1), "ws", 1),
                 (r"weight-stationary, \ $M = 16N$: \ $16N/(19N-2)$", YES, lambda N: 16 * N / (19 * N - 2), None,
                  "ws", 16)]
        curves, dots, legend = VGroup(), VGroup(), VGroup()
        for name, col, f, grow, df, mult in specs:
            curves.add(ax.plot(lambda u, f=f: f(2 ** u), x_range=[1, 8], color=col, stroke_width=3))
            d = VGroup()
            if grow:
                for r in g:
                    if r["dataflow"] == grow[0]:
                        d.add(Circle(radius=0.08, color=col, stroke_width=2.5).move_to(
                            ax.c2p(math.log2(r["n"]), r["utilization"])))
            for r in sc:
                if r["dataflow"] == df and r["m"] == mult * r["n"]:
                    d.add(Dot(ax.c2p(math.log2(r["n"]), r["utilization"]), radius=0.08, color=col))
            dots.add(d)
            legend.add(VGroup(Line(ORIGIN, RIGHT * 0.4, color=col, stroke_width=3),
                              label(name, font_size=19, color=col)).arrange(RIGHT, buff=0.15))
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.35).shift(UP * 0.9)
        key = VGroup(
            VGroup(Circle(radius=0.08, color=GREY_A, stroke_width=2.5), label(r"gate level, \ $N \le 8$",
                                                                              font_size=18, color=GREY_A)).arrange(
                RIGHT, buff=0.15),
            VGroup(Dot(radius=0.08, color=GREY_A), label(r"the same dataflow on integers", font_size=18,
                                                         color=GREY_A)).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(legend, DOWN, buff=0.45).align_to(legend, LEFT)
        big = next(r for r in sc if r["n"] == 256 and r["m"] == 16 * 256)
        osb = next(r for r in sc if r["n"] == 256 and r["dataflow"] == "os")
        note_ = wrapped_label(rf"at $N = 256$: \ {100 * osb['utilization']:.1f}\% against "
                              rf"{100 * big['utilization']:.1f}\%", 4.6, font_size=21, color=YES).next_to(
            key, DOWN, buff=0.45).align_to(legend, LEFT)
        with self.voiceover(
            "Here are the formulas as curves, with the simulations as points. <bookmark mark='a'/> Output-stationary, "
            "for one product, starts at one half for a two by two grid and settles towards a third. "
            "<bookmark mark='b'/> Weight-stationary with as many input rows as the grid has columns does worse, "
            "towards a quarter, because loading the weights costs N cycles of its own. <bookmark mark='c'/> But give "
            "it a long stream, sixteen times as many rows, and it climbs above eighty percent at every size. Open "
            "circles are gate-level grids, filled points the integer model for larger ones, and all lie on the curves. So the weights should stay "
            "only when many inputs will pass the same weights: in a neural network, a batch."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(key))
            for mk, c, d, lg in zip("abc", curves, dots, legend):
                vo.wait_until(mk)
                self.play(Create(c), FadeIn(lg), LaggedStart(*[FadeIn(x, scale=1.5) for x in d], lag_ratio=0.2),
                          run_time=1.8)
            self.play(FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()

    def scale(self):
        sc = load("scaling")["rows"]
        g = load("gates")["rows"]
        head = label(r"At the TPU's size", font_size=36).to_edge(UP, buff=0.3)
        rows, cols = [], []
        for r in sc:
            kind = r"output-stationary" if r["dataflow"] == "os" else rf"weight-stationary, \ $M$ = {r['m']:,}".replace(
                ",", "{,}")
            same = abs(r["utilization"] - r["closed_form"]) < 1e-12 and r["correct"]
            rows.append([rf"{r['n']}", kind, f"{r['cycles']:,}".replace(",", "{,}"),
                         rf"{100 * r['utilization']:.1f}\%", r"yes" if same else r"no"])
            col = HEAD if r["dataflow"] == "os" else (LAM if r["m"] == r["n"] else YES)
            cols.append([WHITE, col, WHITE, col, YES if same else NO])
        tab = grid_table([r"$N$", r"dataflow", r"cycles", r"utilization", r"formula and product check"], rows,
                         widths=[0.9, 4.0, 1.4, 1.7, 3.6], row_h=0.38, font_size=19, colors=cols, mono_cols=())
        tab.next_to(head, DOWN, buff=0.35).set_x(0)
        per = {}
        for r in g:
            per.setdefault(r["n"], {})[r["dataflow"]] = r["gates"]
        extra = {nn: (v["weight-stationary"] - v["output-stationary"]) / nn ** 2 for nn, v in per.items()}
        same_extra = len(set(extra.values())) == 1
        e0 = next(iter(extra.values()))
        notes = VGroup(
            label(rf"the price of holding weights: \ {e0:.0f} more gates per cell \ (multiplexers), \ at every $N$"
                  if same_extra else r"holding weights costs multiplexers in every cell", font_size=20, color=KERN),
            label(r"$N = 256$: \ the TPU's grid; \ chapter 5 reads its paper", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, DOWN, buff=0.5).set_x(0)
        with self.voiceover(
            "Finally, the sizes that matter. <bookmark mark='a'/> For grids of sixteen, sixty-four and two hundred "
            "and fifty-six cells a side, the integer model counts the cycles of each dataflow, checks the product "
            "against NumPy, and every utilization equals its formula exactly. At two hundred and fifty-six, one "
            "output-stationary product keeps the grid a third busy; weight-stationary with a long stream, over "
            "eighty percent. <bookmark mark='b'/> Holding a weight is not free: each cell needs multiplexers to "
            f"keep its weight while the load signal is off, {say_n(round(e0))} more gates per cell in our circuits. "
            "<bookmark mark='c'/> Two hundred and fifty-six by two hundred and fifty-six, weight-stationary, fed "
            "with batches: that is the heart of the Tensor Processing Unit that Google put into its data centres "
            "from 2015, the subject of the next chapter."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(c) for c in tab.cells[0]], FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*tab.cells[i])) for i in range(1, len(rows) + 1)], lag_ratio=0.2),
                      run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()


def say(n: int) -> str:
    return "zero one two three four five six seven eight nine ten eleven twelve".split()[n] if n <= 12 else str(n)


def say_n(n: int) -> str:
    """0 to 99 as a speaker says it."""
    ones = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen " \
           "seventeen eighteen nineteen".split()
    tens = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()
    if n < 20:
        return ones[n]
    return tens[n // 10] + ("" if n % 10 == 0 else "-" + ones[n % 10]) if n < 100 else str(n)
