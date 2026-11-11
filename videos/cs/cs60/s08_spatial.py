from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs60.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, module_box, tag_box

# The loop mapped in this scene (illustrative numbers): y[i] = 3 x[i] + 2 x[i-1], with x[-1] = 0.
XS = [2, 1, 4, 3, 5, 2, 6, 1]
CA, CB = 3, 2

# Its dataflow graph: node -> (label on screen, colour); edges between them.
NODES = {"load": (r"load $x$", DATA), "mula": (r"$\times 3$", HEAD), "route": (r"pass", GREY_B),
         "delay": (r"delay", LAM), "mulb": (r"$\times 2$", HEAD), "add": (r"$+$", YES), "store": (r"store $y$", DATA)}
EDGES = [("load", "mula"), ("load", "delay"), ("delay", "mulb"), ("mula", "add"), ("mulb", "add"), ("add", "store")]
# Placement on a 3 x 4 grid of processing elements (row, column); "route" balances the two paths into the adder.
PLACE = {"load": (1, 0), "mula": (1, 1), "route": (1, 2), "delay": (2, 0), "mulb": (2, 1), "add": (2, 2),
         "store": (2, 3)}
ROUTES = [("load", "mula"), ("load", "delay"), ("delay", "mulb"), ("mula", "route"), ("route", "add"),
          ("mulb", "add"), ("add", "store")]


def X(t):
    """x[t] on the input stream: x[-1] = 0 (the loop's initial value), None before and after the data."""
    if t == -1:
        return 0
    return XS[t] if 0 <= t < len(XS) else None


def _mul(c, v):
    return None if v is None else c * v


def pe_value(node, c):
    """What each processing element holds after cycle c: every element takes one cycle; the delay takes two."""
    if node == "load":
        return X(c)
    if node == "mula":
        return _mul(CA, X(c - 1))
    if node == "route":
        return _mul(CA, X(c - 2))
    if node == "delay":
        return X(c - 2)
    if node == "mulb":
        return _mul(CB, X(c - 3))
    if node == "add":
        a, b = X(c - 3), X(c - 4)
        return None if a is None or b is None else CA * a + CB * b
    if node == "store":
        return pe_value("add", c - 1)


class Spatial(VoiceoverScene):
    def construct(self):
        self.card()
        self.time_space()
        self.tokens()
        self.mapping()
        self.pipeline()
        self.fpga()
        self.spectrum()

    def card(self):
        card = chapter_card(7, r"Spatial machines: \ dataflow, \ CGRAs and FPGAs",
                            r"What if the program were laid out in space, \ not in time?", lit=(1975, 1985, 2014),
                            extra=((1975, r"Dennis and Misunas: \ a dataflow processor"),
                                   (1985, r"the first FPGA"), (2014, r"Catapult: \ FPGAs in Bing")), part=PART)
        with self.voiceover("Chapter seven. Spatial machines: dataflow, coarse-grained arrays, and FPGAs."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def _graph(self):
        """The loop's dataflow graph, drawn as nodes and arrows."""
        pos = {"load": [-4.2, 1.6], "mula": [-5.4, 0.55], "delay": [-3.0, 0.55], "mulb": [-3.0, -0.5],
               "add": [-4.2, -1.55], "store": [-4.2, -2.6]}
        nodes = {}
        for k, p in pos.items():
            t, c = NODES[k]
            nodes[k] = tag_box("", color=c, w=1.25, h=0.55)
            nodes[k].remove(nodes[k][1])
            nodes[k].add(label(t, font_size=19, color=c).move_to(nodes[k][0]))
            nodes[k].move_to([*p, 0])
        arrows = VGroup(*[Arrow(nodes[a].get_center(), nodes[b].get_center(), buff=0.32, stroke_width=2.5,
                                color=GREY_B, max_tip_length_to_length_ratio=0.18) for a, b in EDGES])
        return nodes, arrows

    def time_space(self):
        head = label(r"A loop in time, \ and in space", font_size=36).to_edge(UP, buff=0.3)
        loop = label(r"for each $i$: \ $y_i = 3\,x_i + 2\,x_{i-1}$", font_size=24, color=WHITE).next_to(head, DOWN,
                                                                                                    buff=0.3)
        code = code_block(["loop: load  x, [i]", "      mul   t, x, 3", "      mul   u, xp, 2", "      add   y, t, u",
                           "      store y, [i]", "      mov   xp, x", "      add   i, i, 1", "      blt   i, n, loop"],
                          size=19)
        code.move_to([-3.6, -0.6, 0])
        bar = SurroundingRectangle(code[0], color=HEAD, buff=0.06, stroke_width=2)
        alu = module_box(r"one ALU", KERN, w=1.8, h=0.6, font=20).next_to(code, DOWN, buff=0.35)
        tl = label(r"in time: \ 8 instructions per result", font_size=20, color=KERN).next_to(code, UP, buff=0.3)
        nodes, arrows = self._graph()
        g = VGroup(*nodes.values(), arrows)
        g.scale(0.85).move_to([3.4, -0.9, 0])
        sl = label(r"in space: \ one unit per operation", font_size=20, color=YES).move_to([3.4, 0, 0])
        sl.match_y(tl)
        g.next_to(sl, DOWN, buff=0.3)
        with self.voiceover(
            "Every machine so far, the TPU's grid apart, does its work in time. <bookmark mark='a'/> Here is a small "
            "filter: each output is three times this input plus two times the previous one. A processor runs it as "
            "eight instructions, one after another, through the same arithmetic unit, for every result. <bookmark mark='b'/> A spatial machine lays the same "
            "computation out in space instead. Each operation gets its own unit, the values flow between them on "
            "wires, and no instruction is fetched at all: the program has become a circuit."
        ) as vo:
            self.play(FadeIn(head), FadeIn(loop))
            vo.wait_until("a")
            self.play(FadeIn(code), FadeIn(tl), FadeIn(alu), Create(bar))
            for k in range(1, 8):
                self.play(bar.animate.move_to(code[k]).match_width(SurroundingRectangle(code[k], buff=0.06)),
                          Indicate(alu, color=KERN, scale_factor=1.05), run_time=0.45)
            vo.wait_until("b")
            self.play(FadeIn(sl), *[FadeIn(n) for n in nodes.values()], Create(arrows), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def tokens(self):
        head = label(r"Dataflow: \ fire when the inputs arrive", font_size=36).to_edge(UP, buff=0.3)
        ops = {"plus": [-4.0, 0.4], "minus": [-1.0, 0.4], "times": [-2.5, -1.4]}
        circ = {k: Circle(radius=0.42, color=GREY_B, stroke_width=2.5).move_to([*p, 0]) for k, p in ops.items()}
        sym = {k: MathTex(s, font_size=36).move_to(circ[k]) for k, s in
               (("plus", "+"), ("minus", "-"), ("times", r"\times"))}
        ins = {"a": [-4.7, 2.2], "b": [-3.3, 2.2], "c": [-1.7, 2.2], "d": [-0.3, 2.2]}
        inl = {k: label(rf"${k}$", font_size=24, color=DATA).move_to([*p, 0]).shift(UP * 0.3) for k, p in ins.items()}
        tgt = {"a": "plus", "b": "plus", "c": "minus", "d": "minus"}
        wires = {k: Line([*p, 0], circ[tgt[k]].get_center(), color=GREY_C, stroke_width=2) for k, p in ins.items()}
        wires["plus"] = Line(circ["plus"].get_center(), circ["times"].get_center(), color=GREY_C, stroke_width=2)
        wires["minus"] = Line(circ["minus"].get_center(), circ["times"].get_center(), color=GREY_C, stroke_width=2)
        wires["out"] = Line(circ["times"].get_center(), circ["times"].get_center() + DOWN * 1.5, color=GREY_C,
                            stroke_width=2)
        for w in wires.values():
            w.set_z_index(-1)
        vals = {"a": 5, "b": 3, "c": 7, "d": 4}

        def token(v, at, color=HEAD):
            d = Circle(radius=0.2, color=color, fill_color=BG, fill_opacity=1, stroke_width=2.5).move_to(at)
            return VGroup(d, label(f"{v}", font_size=18, color=color).move_to(d))

        def travel(tok, line, frac=0.72):
            """Move a token along a wire, stopping on the wire just short of its node."""
            return tok.animate.move_to(line.point_from_proportion(frac))
        notes = VGroup(
            wrapped_label(r"a node fires when every input holds a token, \ and sends a token onward", 5.0,
                          font_size=19, color=WHITE),
            wrapped_label(r"no program counter: \ the order comes from the data", 5.0, font_size=19, color=HEAD),
            wrapped_label(r"Dennis and Misunas, \ 1975; \ MIT's tagged-token machines, \ 1980s", 5.0, font_size=19,
                          color=GREY_A),
            wrapped_label(r"Part 8's out-of-order core is a dataflow machine \ hidden behind a sequential program",
                          5.0, font_size=19, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.4)
        ill = note(r"illustrative values", font_size=16).to_edge(DOWN, buff=0.25).shift(LEFT * 2.5)
        with self.voiceover(
            "The oldest spatial idea is dataflow. <bookmark mark='a'/> Draw the computation as a graph, and let each "
            "node fire as soon as all of its inputs have arrived. <bookmark mark='b'/> Here a and b arrive, so the "
            "addition fires at once; the subtraction must wait for d, which comes late. <bookmark mark='c'/> Only "
            "then can the multiplication fire. There is no program counter: the order of events comes from the data "
            "itself. <bookmark mark='d'/> Jack Dennis and David Misunas proposed such a processor in 1975, and "
            "Arvind's group at MIT built tagged-token machines in the 1980s. They never displaced the ordinary "
            "processor, but Part 8's out-of-order core is a dataflow engine inside one."
        ) as vo:
            self.play(FadeIn(head), *[Create(w) for w in wires.values()], *[FadeIn(c) for c in circ.values()],
                      *[FadeIn(s) for s in sym.values()], *[FadeIn(t) for t in inl.values()], FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            ta, tb, tc = token(vals["a"], wires["a"].get_start()), token(vals["b"], wires["b"].get_start()), \
                token(vals["c"], wires["c"].get_start())
            self.play(FadeIn(ta), FadeIn(tb), FadeIn(tc))
            self.play(travel(ta, wires["a"]), travel(tb, wires["b"]), travel(tc, wires["c"]), run_time=1.0)
            tp = token(vals["a"] + vals["b"], wires["plus"].get_start(), YES)
            self.play(circ["plus"].animate.set_fill(YES, opacity=0.4), FadeOut(ta), FadeOut(tb), FadeIn(tp),
                      run_time=0.5)
            self.play(circ["plus"].animate.set_fill(BG, opacity=0), travel(tp, wires["plus"], 0.65), run_time=0.8)
            self.play(Indicate(circ["minus"], color=NO), run_time=0.8)
            td = token(vals["d"], wires["d"].get_start())
            self.play(FadeIn(td))
            self.play(travel(td, wires["d"]), run_time=0.9)
            tm = token(vals["c"] - vals["d"], wires["minus"].get_start(), YES)
            self.play(circ["minus"].animate.set_fill(YES, opacity=0.4), FadeOut(tc), FadeOut(td), FadeIn(tm),
                      run_time=0.5)
            self.play(circ["minus"].animate.set_fill(BG, opacity=0), travel(tm, wires["minus"], 0.65), run_time=0.8)
            vo.wait_until("c")
            tt = token((vals["a"] + vals["b"]) * (vals["c"] - vals["d"]), wires["out"].get_start(), YES)
            self.play(circ["times"].animate.set_fill(YES, opacity=0.4), FadeOut(tp), FadeOut(tm), FadeIn(tt),
                      run_time=0.5)
            self.play(circ["times"].animate.set_fill(BG, opacity=0), tt.animate.move_to(wires["out"].get_end()),
                      FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def _cgra(self, size=0.95, gap=0.32):
        """A 3 x 4 coarse-grained array: word-wide processing elements wired to their neighbours."""
        pes = VGroup(*[RoundedRectangle(width=size, height=size, corner_radius=0.08, stroke_color=GREY_C,
                                        stroke_width=2, fill_color=BG, fill_opacity=1) for _ in range(12)])
        pes.arrange_in_grid(3, 4, buff=gap)
        mesh = VGroup()
        for r in range(3):
            for c in range(4):
                if c < 3:
                    mesh.add(Line(pes[r * 4 + c].get_right(), pes[r * 4 + c + 1].get_left(), color=GREY_D,
                                  stroke_width=1.5))
                if r < 2:
                    mesh.add(Line(pes[r * 4 + c].get_bottom(), pes[(r + 1) * 4 + c].get_top(), color=GREY_D,
                                  stroke_width=1.5))
        return VGroup(mesh, pes)

    def _pe(self, cg, node):
        r, c = PLACE[node]
        return cg[1][r * 4 + c]

    def _routes(self, cg, color=YES):
        out = VGroup()
        for a, b in ROUTES:
            pa, pb = self._pe(cg, a), self._pe(cg, b)
            d = pb.get_center() - pa.get_center()
            d = d / np.linalg.norm(d)
            out.add(Arrow(pa.get_center() + d * pa.width / 2, pb.get_center() - d * pb.width / 2, buff=0.02,
                          stroke_width=4, color=color, max_tip_length_to_length_ratio=0.5))
        return out

    def mapping(self):
        head = label(r"Mapping the loop onto an array", font_size=36).to_edge(UP, buff=0.3)
        nodes, arrows = self._graph()
        gl = label(r"the dataflow graph", font_size=20, color=GREY_A).next_to(VGroup(*nodes.values()), UP, buff=0.3)
        cg = self._cgra().move_to([3.2, -0.4, 0])
        cl = label(r"a coarse-grained reconfigurable array \ (CGRA)", font_size=20, color=GREY_A).next_to(cg, UP,
                                                                                                        buff=0.3)
        cl.set_y(2.35)
        gl.set_y(2.35)
        placed = {}
        for k in PLACE:
            t, c = NODES[k]
            placed[k] = label(t, font_size=18, color=c).move_to(self._pe(cg, k))
        routes = self._routes(cg)
        notes = VGroup(
            wrapped_label(r"each element: \ a word-wide ALU, \ a register, \ a switch; \ configured once, \ "
                          r"then left alone", 12.0, font_size=19, color=WHITE),
            wrapped_label(r"placement and routing: \ the two paths into $+$ must take the same number of cycles, \ "
                          r"so one element only passes a value on", 12.0, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Between the processor and fixed hardware sits the coarse-grained reconfigurable array, or CGRA. "
            "<bookmark mark='a'/> It is a grid of small processing elements, each a word-wide arithmetic unit, a "
            "register and a switch, wired to its neighbours. A configuration tells each one what to do, once, before "
            "the data starts. <bookmark mark='b'/> To run the loop, a compiler places each node of the graph on an "
            "element. <bookmark mark='c'/> Then it routes each edge along the wires between neighbours. "
            "<bookmark mark='d'/> There is a catch: the two paths into the adder must take the same number of "
            "cycles, so one element does nothing but pass a value on. Placement and routing are hard search "
            "problems."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(n) for n in nodes.values()], Create(arrows), FadeIn(gl))
            vo.wait_until("a")
            self.play(FadeIn(cg), FadeIn(cl), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[TransformFromCopy(nodes[k][1], placed[k]) for k in nodes], lag_ratio=0.25),
                      *[self._pe(cg, k).animate.set_stroke(NODES[k][1], width=3) for k in nodes], run_time=2.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowArrow(r) for r in routes], lag_ratio=0.25), run_time=2.2)
            vo.wait_until("d")
            self.play(FadeIn(placed["route"]), self._pe(cg, "route").animate.set_stroke(GREY_B, width=3),
                      FadeIn(notes[1]))
            self.play(Indicate(self._pe(cg, "route"), color=HEAD))
        self.wait(0.4)
        self.clear_scene()

    def pipeline(self):
        head = label(r"One result every cycle", font_size=36).to_edge(UP, buff=0.3)
        cg = self._cgra(size=1.12, gap=0.36).move_to([-1.6, -0.35, 0])
        for k in PLACE:
            self._pe(cg, k).set_stroke(NODES[k][1], width=3)
        ops = VGroup(*[label(NODES[k][0], font_size=17, color=NODES[k][1]).move_to(
            self._pe(cg, k).get_top() + DOWN * 0.22) for k in PLACE])
        routes = self._routes(cg)
        keys = list(PLACE)

        def vals(c):
            g = VGroup()
            for k in keys:
                v = pe_value(k, c)
                t = label(f"{v}" if v is not None else r"--", font_size=24,
                          color=WHITE if v is not None else GREY_D)
                g.add(t.move_to(self._pe(cg, k).get_center() + DOWN * 0.15))
            return g
        v = vals(-1)
        xin = label(r"$x$: \ " + r", \ ".join(str(x) for x in XS), font_size=22, color=DATA)
        xin.next_to(cg, UP, buff=0.35).align_to(cg, LEFT)
        clock = label(r"cycle 0", font_size=26, color=HEAD).to_corner(UR, buff=0.5).shift(DOWN * 0.8 + LEFT * 0.4)
        outs = VGroup(*[label(rf"$y_{{{i}}} = {CA * XS[i] + CB * (XS[i - 1] if i else 0)}$", font_size=22, color=YES)
                        for i in range(len(XS))]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        outs.next_to(clock, DOWN, buff=0.35).align_to(clock, LEFT)
        lat = 4                                            # y[i] reaches the store element at cycle i + 4
        foot = wrapped_label(r"after a few cycles' latency, \ one $y$ per cycle, \ with no instruction fetched; \ "
                             r"$x_{-1} = 0$; \ illustrative numbers", 12.4, font_size=19, color=GREY_A)
        foot.to_edge(DOWN, buff=0.25)
        total = len(XS) + lat
        with self.voiceover(
            "Now let it run. <bookmark mark='a'/> On every tick a new x enters, and every element passes its "
            "result on. The multiplier by three works on this x while the multiplier by "
            "two works on an older one, held back a cycle by the delay. <bookmark mark='b'/> On the fifth tick the "
            "first output reaches the store, and from then on one result leaves every cycle, where the processor "
            "needed eight instructions for each. <bookmark mark='c'/> This is a pipeline, Part 7's idea, but "
            "made out of the program itself."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cg), FadeIn(ops), FadeIn(routes), FadeIn(v), FadeIn(xin), FadeIn(clock))
            vo.wait_until("a")
            for c in range(total):
                nv = vals(c)
                anims = [Transform(v, nv), Transform(clock, label(rf"cycle {c + 1}", font_size=26,
                                                                  color=HEAD).move_to(clock))]
                if c - lat >= 0:
                    anims.append(FadeIn(outs[c - lat], shift=LEFT * 0.2))
                if c < len(XS):
                    anims.append(Indicate(xin, color=DATA, scale_factor=1.02))
                self.play(*anims, run_time=0.7)
                if c == lat - 1:
                    vo.wait_until("b")
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def fpga(self):
        head = label(r"FPGAs: \ lookup tables, \ rewired", font_size=36).to_edge(UP, buff=0.3)
        parity = [bin(i).count("1") % 2 for i in range(16)]
        two = [1 if bin(i).count("1") >= 2 else 0 for i in range(16)]
        idx = 9
        cells = VGroup(*[Rectangle(width=0.5, height=0.26, stroke_color=GREY_C, stroke_width=1.2, fill_color=BG,
                                   fill_opacity=1) for _ in range(16)]).arrange(DOWN, buff=0)
        cells.move_to([-4.6, -0.55, 0])

        def bits(table):
            return VGroup(*[label(f"{b}", font_size=17, color=YES if b else GREY_B).move_to(cells[i])
                            for i, b in enumerate(table)])
        bv = bits(parity)
        nums = VGroup(*[label(f"{i}", font_size=14, color=GREY_D).next_to(cells[i], LEFT, buff=0.1)
                        for i in range(16)])
        mux = Polygon([-3.6, 1.0, 0], [-2.6, 0.5, 0], [-2.6, -1.6, 0], [-3.6, -2.1, 0], color=KERN,
                      stroke_width=2.5).move_to([-3.0, -0.55, 0])
        mux_l = label(r"select", font_size=16, color=KERN).move_to(mux).shift(RIGHT * 0.05)
        sel = label(r"inputs $1\,0\,0\,1$ \ = \ entry 9", font_size=19, color=DATA).next_to(mux, DOWN, buff=0.2)
        out = Arrow(mux.get_right(), mux.get_right() + RIGHT * 0.8, buff=0, color=WHITE, stroke_width=3,
                    max_tip_length_to_length_ratio=0.25)
        ov = label(f"{parity[idx]}", font_size=26, color=WHITE).next_to(out, RIGHT, buff=0.12)
        hl = SurroundingRectangle(cells[idx], color=HEAD, buff=0.02, stroke_width=3)
        lt = label(r"a 4-input lookup table \ (Part 3)", font_size=20, color=WHITE).next_to(
            VGroup(cells, mux), UP, buff=0.3).align_to(nums, LEFT)
        fn = label(r"16 bits: \ parity", font_size=19, color=YES).next_to(lt, DOWN, buff=0.12).align_to(lt, LEFT)
        fn2 = label(r"16 bits: \ at least two set", font_size=19, color=YES).move_to(fn, aligned_edge=LEFT)
        # the fabric: logic blocks, a column of multiplier blocks and one of memory blocks, routing between
        fab = VGroup()
        cols = ["L", "L", "D", "L", "L", "M", "L"]
        for r in range(5):
            for c, kind in enumerate(cols):
                col = {"L": GREY_B, "D": KERN, "M": DATA}[kind]
                fab.add(Square(0.42, stroke_color=col, stroke_width=1.8, fill_color=col, fill_opacity=0.15).move_to(
                    [c * 0.62, -r * 0.62, 0]))
        wires = VGroup(*[Line([c * 0.62 + 0.31, 0.3, 0], [c * 0.62 + 0.31, -2.78, 0], color=GREY_D, stroke_width=1)
                         for c in range(-1, 7)],
                       *[Line([-0.31, -r * 0.62 + 0.31, 0], [6 * 0.62 + 0.31, -r * 0.62 + 0.31, 0], color=GREY_D,
                              stroke_width=1) for r in range(-0, 6)])
        fabric = VGroup(wires, fab).move_to([3.4, 0.2, 0])
        key = VGroup(label(r"logic: \ lookup tables and flip-flops \ (Part 5)", font_size=18, color=GREY_A),
                     label(r"hard multiplier blocks", font_size=18, color=KERN),
                     label(r"memory blocks", font_size=18, color=DATA)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        key.next_to(fabric, DOWN, buff=0.3).align_to(fabric, LEFT)
        gap = wrapped_label(r"the price of reconfigurability: \ around 35 times the area of a custom chip for the "
                            r"same logic, \ and several times slower \ (Kuon and Rose, \ 2007)", 5.3, font_size=18,
                            color=NO).next_to(key, DOWN, buff=0.25).align_to(key, LEFT)
        with self.voiceover(
            "The most flexible spatial machine is the FPGA. <bookmark mark='a'/> Its building block is Part 3's "
            "lookup table: sixteen bits of memory and a selector. Four input bits choose one of the sixteen "
            "entries, so the table computes any function of four inputs. Here, parity. <bookmark mark='b'/> Load "
            "different bits, and the same table computes something else, say, whether at least two inputs are "
            "set. <bookmark mark='c'/> An FPGA is a sea of these tables, each beside a flip-flop of Part 5, with "
            "programmable wires between them, and columns of hard multipliers and memories. "
            "<bookmark mark='d'/> The flexibility has a price. Ian Kuon and Jonathan Rose measured it in 2007: the "
            "same logic took around thirty-five times the area of a custom chip, and ran several times slower."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cells), FadeIn(nums), FadeIn(bv), FadeIn(lt), FadeIn(fn), Create(mux), FadeIn(mux_l))
            self.play(FadeIn(sel), Create(hl))
            self.play(GrowArrow(out), FadeIn(ov))
            vo.wait_until("b")
            self.play(Transform(bv, bits(two)), Transform(fn, fn2),
                      Transform(ov, label(f"{two[idx]}", font_size=26, color=WHITE).move_to(ov)))
            vo.wait_until("c")
            self.play(Create(wires), LaggedStart(*[FadeIn(s) for s in fab], lag_ratio=0.02), FadeIn(key),
                      run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(gap))
        self.wait(0.4)
        self.clear_scene()

    def spectrum(self):
        head = label(r"Flexibility against efficiency", font_size=36).to_edge(UP, buff=0.3)
        axis = Arrow([-6.0, 1.3, 0], [6.0, 1.3, 0], buff=0, color=GREY_B, stroke_width=3,
                     max_tip_length_to_length_ratio=0.02)
        ends = VGroup(label(r"any program", font_size=19, color=GREY_A).next_to(axis.get_start(), DOWN, buff=0.15)
                      .align_to(axis, LEFT),
                      label(r"one job, \ least energy", font_size=19, color=GREY_A).next_to(axis.get_end(), DOWN,
                                                                                         buff=0.15)
                      .align_to(axis, RIGHT))
        kinds = [(r"CPU", GREY_B), (r"GPU", LAM), (r"FPGA", DATA), (r"CGRA", HEAD), (r"ASIC \ (the TPU)", KERN)]
        xs = [-4.8, -2.4, 0.0, 2.2, 4.6]
        marks = VGroup(*[VGroup(Dot([x, 1.3, 0], radius=0.09, color=c),
                                label(n, font_size=22, color=c).move_to([x, 1.85, 0])) for x, (n, c) in zip(xs, kinds)])
        ill = note(r"the order is the usual one; \ the spacing is illustrative", font_size=16).next_to(ends, DOWN,
                                                                                                   buff=0.15)
        ill.set_x(0)

        def card(title, body, col):
            t = label(title, font_size=21, color=col)
            b = wrapped_label(body, 3.7, font_size=18, color=GREY_A)
            g = VGroup(t, b).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            frame = RoundedRectangle(width=4.0, height=2.0, corner_radius=0.12, stroke_color=col, stroke_width=1.8)
            g.move_to(frame)
            return VGroup(frame, g)
        cards = VGroup(
            card(r"Catapult \ (Microsoft, \ 2014)", r"an FPGA in each of Bing's ranking servers: \ nearly double the "
                 r"throughput of a ranking stage", DATA),
            card(r"FPGAs to rent \ (AWS, \ 2017)", r"FPGA instances in the cloud of Part 45: \ hardware you "
                 r"reconfigure like software", LAM),
            card(r"Plasticine \ (Stanford, \ 2017)", r"a research CGRA: \ patterns such as map and reduce compiled "
                 r"straight onto the array", HEAD),
        ).arrange(RIGHT, buff=0.3).next_to(ill, DOWN, buff=0.9).set_x(0)
        with self.voiceover(
            "So spatial machines fill a spectrum. <bookmark mark='a'/> At one end the CPU runs any program, paying "
            "for every instruction; at the other, a fixed chip such as the TPU does one job for the least energy. "
            "GPUs, FPGAs and CGRAs sit between. <bookmark mark='b'/> In 2014 Microsoft put an FPGA in each of the "
            "servers that rank Bing's search results, and nearly doubled the throughput of a ranking stage. "
            "<bookmark mark='c'/> Since 2017 anyone can rent FPGAs in Amazon's cloud. <bookmark mark='d'/> And "
            "research CGRAs such as Stanford's Plasticine compile parallel patterns straight onto the array. In each "
            "case the hard part is the compiler, which chapter ten returns to."
        ) as vo:
            self.play(FadeIn(head), GrowArrow(axis), FadeIn(ends))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(mk, shift=DOWN * 0.15) for mk in marks], lag_ratio=0.3), FadeIn(ill),
                      run_time=2)
            for mk, cd in zip("bcd", cards):
                vo.wait_until(mk)
                self.play(FadeIn(cd, shift=UP * 0.15))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, KERN, LAM, NO, PART)
