from __future__ import annotations

from itertools import combinations

from explainer.cs import *  # noqa: F403
from videos.cs.cs59.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load

PC = [DATA, KERN, LAM]          # process colours: p0 blue, p1 orange, p2 purple (also the colours 0, 1, 2)


def ordered_partitions(s):
    """Every way to split the set s into an ordered sequence of non-empty blocks (who moves together, in turn)."""
    s = list(s)
    if not s:
        return [[]]
    res = []
    for r in range(1, len(s) + 1):
        for comb in combinations(s, r):
            rest = [x for x in s if x not in comb]
            for tail in ordered_partitions(rest):
                res.append([frozenset(comb)] + tail)
    return res


def chrom(tri, t=0.5):
    """One round of immediate snapshots on a triangle of views: tri = [(process, position, ids known), ...].
    Each ordered partition is a run; a process sees the processes of its block and all earlier blocks.  Returns the
    13 triangles of the chromatic subdivision, each as three (process, position, ids known)."""
    P = {c: p for c, p, _ in tri}
    K = {c: k for c, _, k in tri}
    g = sum(P.values()) / 3
    out = []
    for op in ordered_partitions(P):
        seen, simp = set(), []
        for block in op:
            seen |= block
            V = frozenset(seen)
            for i in block:
                if len(V) == 1:
                    pos = P[i]
                elif len(V) == 2:
                    j = next(iter(V - {i}))
                    pos = (P[i] + 2 * P[j]) / 3
                else:
                    j, k = sorted(V - {i})
                    pos = g + t * ((P[j] + P[k]) / 2 - g)
                simp.append((i, pos, frozenset().union(*[K[c] for c in V])))
        out.append(simp)
    return out


def corners(cx, cy, w):
    h = w * np.sqrt(3) / 2
    return [np.array([cx - w / 2, cy - h / 2, 0]), np.array([cx + w / 2, cy - h / 2, 0]), np.array([cx, cy + h / 2, 0])]


def base_tri(cx, cy, w):
    return [(i, p, frozenset({i})) for i, p in enumerate(corners(cx, cy, w))]


def draw_complex(tris, r=0.07, stroke=1.4, colour=lambda v: PC[v[0]]):
    """Triangles in grey, vertices as dots coloured by ``colour``; returns VGroup(polys, dots) with .keys, .verts."""
    polys = VGroup(*[Polygon(*[p for _, p, _ in t], stroke_color=GREY_C, stroke_width=stroke, fill_color=BG,
                             fill_opacity=0) for t in tris])
    seen = {}
    for t in tris:
        for v in t:
            key = (v[0], round(float(v[1][0]), 3), round(float(v[1][1]), 3))
            seen.setdefault(key, v)
    dots = VGroup(*[Dot(v[1], radius=r, color=colour(v)).set_z_index(2) for v in seen.values()])
    g = VGroup(polys, dots)
    g.verts = list(seen.values())
    return g


def vtx(pos, color, val=None, r=0.28, size=26):
    c = Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=1).move_to(pos)
    if val is None:
        return VGroup(c)
    return VGroup(c, MathTex(str(val), font_size=size, color=BLACK).move_to(c))


class Topology(VoiceoverScene):
    def construct(self):
        self.card()
        self.complexes()
        self.protocol()
        self.subdivision()
        self.sperner()
        self.kset()
        self.theorem()

    def card(self):
        card = chapter_card(7, r"Topology: \ why $k$-set agreement is impossible", r"What shape is the space of a "
                            r"protocol's runs?", lit=(1928, 1990, 1993, 2004),
                            extra=((1928, r"Sperner's lemma"), (1990, r"Chaudhuri: \ $k$-set agreement"),
                                   (1993, r"three proofs"), (2004, r"G\"odel Prize")), part=PART)
        with self.voiceover("Chapter seven. Topology: why k-set agreement is impossible."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def complexes(self):
        head = label(r"A task is a map between complexes", font_size=36).to_edge(UP, buff=0.3)
        ip = {("p", 0): [-5.6, 1.3, 0], ("q", 1): [-3.0, 1.3, 0], ("p", 1): [-3.0, -1.1, 0], ("q", 0): [-5.6, -1.1, 0]}
        iv = {k: vtx(p, DATA if k[0] == "p" else KERN, k[1]) for k, p in ip.items()}
        ie = {}
        for a, b in ((("p", 0), ("q", 1)), (("q", 1), ("p", 1)), (("p", 1), ("q", 0)), (("q", 0), ("p", 0))):
            ie[(a, b)] = Line(ip[a], ip[b], color=GREY_B, stroke_width=4).set_z_index(-1)
        op = {("p", 0): [1.4, 1.3, 0], ("q", 0): [4.0, 1.3, 0], ("p", 1): [1.4, -1.1, 0], ("q", 1): [4.0, -1.1, 0]}
        ov = {k: vtx(p, DATA if k[0] == "p" else KERN, k[1]) for k, p in op.items()}
        oe = [Line(op[("p", 0)], op[("q", 0)], color=GREY_B, stroke_width=4).set_z_index(-1),
              Line(op[("p", 1)], op[("q", 1)], color=GREY_B, stroke_width=4).set_z_index(-1)]
        icap = label(r"inputs $\mathcal{I}$", font_size=21, color=GREY_A).move_to([-4.3, -1.8, 0])
        ocap = label(r"consensus outputs $\mathcal{O}$", font_size=21, color=GREY_A).move_to([2.7, -1.8, 0])
        arr = Arrow([-2.4, 0.1, 0], [0.8, 0.1, 0], buff=0, color=HEAD, stroke_width=3)
        dl = MathTex(r"\Delta", font_size=34, color=HEAD).next_to(arr, UP, buff=0.1)
        leg = VGroup(label(r"$p$", font_size=21, color=DATA), label(r"$q$", font_size=21, color=KERN)).arrange(
            RIGHT, buff=0.3).move_to([5.8, 1.3, 0])
        legc = label(r"colour = process", font_size=16, color=GREY_B).next_to(leg, DOWN, buff=0.12)
        foot = wrapped_label(r"a \textbf{vertex}: \ a process with its value; \ a \textbf{simplex}: \ values that can "
                             r"occur together in one run; \ $\Delta$: \ the outputs each input simplex allows", 12.4,
                             font_size=19, color=WHITE).to_edge(DOWN, buff=0.45)
        hi0 = ie[(("q", 0), ("p", 0))]
        hi1 = ie[(("p", 0), ("q", 1))]
        with self.voiceover(
            "Maurice Herlihy and Nir Shavit's idea was to draw a task as a shape. <bookmark mark='a'/> Two "
            "processes, p in blue and q in orange, each start with a bit. A vertex is a process with its value, and "
            "an edge joins values that can occur in the same run. All four combinations can, so the inputs form a "
            "square. <bookmark mark='b'/> The outputs of consensus are just two edges: both decide zero, or both "
            "decide one. <bookmark mark='c'/> The task is a map, delta, from each input simplex to the outputs it "
            "allows. Inputs zero and zero allow only zero and zero. <bookmark mark='d'/> Inputs zero and one allow "
            "either edge, but never a mixture."
        ) as vo:
            self.play(FadeIn(head), FadeIn(leg), FadeIn(legc))
            vo.wait_until("a")
            self.play(*[FadeIn(v) for v in iv.values()], FadeIn(icap))
            self.play(*[Create(e) for e in ie.values()])
            vo.wait_until("b")
            self.play(*[FadeIn(v) for v in ov.values()], *[Create(e) for e in oe], FadeIn(ocap))
            vo.wait_until("c")
            self.play(GrowArrow(arr), FadeIn(dl), FadeIn(foot))
            self.play(hi0.animate.set_color(HEAD).set_stroke(width=7), oe[0].animate.set_color(HEAD).set_stroke(
                width=7))
            vo.wait_until("d")
            self.play(hi0.animate.set_color(GREY_B).set_stroke(width=4), oe[0].animate.set_color(GREY_B).set_stroke(
                width=4))
            self.play(hi1.animate.set_color(YES).set_stroke(width=7), *[e.animate.set_color(YES).set_stroke(width=7)
                                                                        for e in oe])
        self.wait(0.4)
        self.clear_scene()

    def protocol(self):
        head = label(r"One round of reading cuts an edge in three", font_size=36).to_edge(UP, buff=0.3)
        xa, xb = -4.4, 6.0
        y0, y1, y2 = 2.0, 0.75, -0.55

        def row(n, y, r=0.16):
            xs = np.linspace(xa, xb, n)
            line = Line([xa, y, 0], [xb, y, 0], color=GREY_B, stroke_width=3).set_z_index(-1)
            vs = VGroup(*[Circle(radius=r, stroke_width=0, fill_color=DATA if k % 2 == 0 else KERN,
                                 fill_opacity=1).move_to([x, y, 0]) for k, x in enumerate(xs)])
            return VGroup(line, vs), xs
        inp = VGroup(Line([xa, y0, 0], [xb, y0, 0], color=GREY_B, stroke_width=3).set_z_index(-1),
                     vtx([xa, y0, 0], DATA, 0, r=0.24, size=24), vtx([xb, y0, 0], KERN, 1, r=0.24, size=24))
        r1, x1 = row(4, y1)
        r2, x2 = row(10, y2, r=0.13)
        names = VGroup(label(r"inputs", font_size=17, color=GREY_A).move_to([-5.9, y0, 0]),
                       label(r"1 round", font_size=17, color=GREY_A).move_to([-5.9, y1, 0]),
                       label(r"2 rounds", font_size=17, color=GREY_A).move_to([-5.9, y2, 0]))
        views = VGroup(*[MathTex(t, font_size=21, color=c).next_to([x, y1, 0], DOWN, buff=0.22) for t, c, x in zip(
            (r"p\!:\{p\}", r"q\!:\{p,q\}", r"p\!:\{p,q\}", r"q\!:\{q\}"), (DATA, KERN, DATA, KERN), x1)])
        sched = VGroup(*[label(t, font_size=16, color=GREY_B).next_to([(x1[k] + x1[k + 1]) / 2, y1, 0], UP, buff=0.12)
                         for k, t in enumerate((r"$p$ first", r"together", r"$q$ first"))])
        dec = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
        dl = VGroup(*[MathTex(str(d), font_size=22, color=YES if d == 0 else LAM).next_to([x, y2, 0], UP, buff=0.18)
                      for d, x in zip(dec, x2)])
        sw = next(k for k in range(9) if dec[k] != dec[k + 1])
        bad = Line([x2[sw], y2, 0], [x2[sw + 1], y2, 0], color=NO, stroke_width=7)
        ill = note(r"illustrative decisions", font_size=16).next_to([x2[-1], y2, 0], DOWN, buff=0.3).align_to(
            r2, RIGHT)
        fs = 27
        rows = [MathTex(r"d(p \text{ alone})", r"=", r"0", r",\quad", r"d(q \text{ alone})", r"=", r"1",
                        font_size=fs),
                MathTex(r"\text{path from } 0 \text{ to } 1", r"\Rightarrow", r"\text{an edge } \{0, 1\}",
                        font_size=fs),
                MathTex(r"\text{an edge } \{0, 1\}", r"=", r"\text{a run where } p, q \text{ disagree}",
                        font_size=fs)]
        whys = [label(r"$p$ alone cannot tell this run from inputs 0, 0 with $q$ slow", font_size=18, color=GREY_B),
                label(r"$3^r$ edges after $r$ rounds, \ but always one connected path", font_size=18, color=GREY_B),
                label(r"so registers cannot solve consensus, \ in any number of rounds", font_size=18, color=NO)]
        for k, (r, w) in enumerate(zip(rows, whys)):
            y = -1.75 - 0.6 * k
            r.move_to([0, y, 0]).align_to([-6.5, 0, 0], LEFT)
            w.move_to([0, y, 0]).align_to([0.9, 0, 0], LEFT)
        src = note(r"one round: \ write, \ then an immediate snapshot \ (Borowsky and Gafni, \ 1993)",
                   font_size=16).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Now run a protocol. In each round a process writes its state, then takes an immediate snapshot of "
            "memory, a form of round Borowsky and Gafni introduced. <bookmark mark='a'/> Start from inputs zero "
            "and one. If p goes first, it sees only itself and q sees both; together, both see both; if q goes "
            "first, it sees only itself. The edge becomes a path of three. <bookmark mark='b'/> Each further round "
            "cuts every piece in three again: always one connected path. <bookmark mark='c'/> At one end p ran "
            "alone. It cannot tell this from a run where both inputs were zero and q was slow, so it must decide "
            "zero; at the other end q must decide one. <bookmark mark='d'/> Somewhere the decision switches, and "
            "that edge is a run where they disagree."
        ) as vo:
            self.play(FadeIn(head), FadeIn(inp), FadeIn(names[0]), FadeIn(src))
            vo.wait_until("a")
            self.play(TransformFromCopy(inp[0], r1[0]), *[TransformFromCopy(inp[1 + (k % 2)], r1[1][k])
                                                          for k in range(4)], FadeIn(names[1]))
            self.play(LaggedStart(*[FadeIn(s) for s in sched], lag_ratio=0.4), FadeIn(views), run_time=1.6)
            vo.wait_until("b")
            self.play(TransformFromCopy(r1[0], r2[0]), *[FadeIn(v, scale=0.5) for v in r2[1]], FadeIn(names[2]))
            vo.wait_until("c")
            self.play(FadeIn(dl[0]), FadeIn(dl[-1]), FadeIn(rows[0]), FadeIn(whys[0]))
            self.play(LaggedStart(*[FadeIn(d) for d in dl[1:-1]], lag_ratio=0.15), FadeIn(ill), run_time=1.2)
            vo.wait_until("d")
            self.play(Create(bad), FadeIn(rows[1]), FadeIn(whys[1]))
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
        self.wait(0.4)
        self.clear_scene()

    def subdivision(self):
        head = label(r"Three processes: \ the chromatic subdivision", font_size=36).to_edge(UP, buff=0.3)
        w, cy = 3.7, 0.45
        cx = [-4.6, 0.0, 4.6]
        t0 = base_tri(cx[0], cy, w)
        c0 = draw_complex([t0], r=0.13, stroke=2)
        cl = VGroup(*[MathTex(rf"p_{i}", font_size=24, color=PC[i]).next_to(p, d, buff=0.15)
                      for i, (_, p, _), d in zip(range(3), t0, (DL, DR, UP))])
        c1t = chrom(base_tri(cx[1], cy, w))
        c1 = draw_complex(c1t, r=0.09, stroke=1.6)
        c2t = [s for t in chrom(base_tri(cx[2], cy, w)) for s in chrom(t)]
        c2 = draw_complex(c2t, r=0.045, stroke=0.8)
        caps = VGroup(label(r"the input simplex", font_size=19, color=GREY_A),
                      label(rf"1 round: \ {len(c1t)} triangles", font_size=19, color=GREY_A),
                      label(rf"2 rounds: \ {len(c2t)} triangles", font_size=19, color=GREY_A))
        for c, x in zip(caps, cx):
            c.move_to([x, cy - w * np.sqrt(3) / 4 - 0.4, 0])
        arrs = VGroup(*[Arrow([cx[k] + w / 2 - 0.3, cy + 0.2, 0], [cx[k + 1] - w / 2 + 0.3, cy + 0.2, 0], buff=0,
                              color=GREY_B, stroke_width=2.5, max_tip_length_to_length_ratio=0.25) for k in range(2)])
        mid = next(t for t in c1t if all(len(k) == 3 for _, _, k in t))
        corner = next(t for t in c1t if sorted(len(k) for _, _, k in t) == [1, 2, 3] and
                      next(c for c, _, k in t if len(k) == 1) == 0)
        hm = Polygon(*[p for _, p, _ in mid], stroke_width=0, fill_color=HEAD, fill_opacity=0.5)
        hc = Polygon(*[p for _, p, _ in corner], stroke_width=0, fill_color=YES, fill_opacity=0.5)
        W = 12.4
        notes = VGroup(
            VGroup(label(r"yellow: \ all three move together;", font_size=19, color=HEAD),
                   label(r"green: \ $p_0$ first, \ alone", font_size=19, color=YES)).arrange(RIGHT, buff=0.3),
            wrapped_label(r"every small triangle has one vertex of each colour: \ three views from one run", W,
                          font_size=19, color=WHITE),
            wrapped_label(r"however many rounds, \ the complex is a \textbf{subdivision} of the triangle: \ no holes",
                          W, font_size=19, color=HEAD),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "With three processes the same thing happens in two dimensions. <bookmark mark='a'/> The inputs form a "
            "triangle, one vertex per process. <bookmark mark='b'/> One round of immediate snapshots cuts it into "
            "thirteen triangles, one for each way the three can be ordered, ties allowed. The middle triangle is "
            "the run where all three move together; this corner one, the run where p zero goes alone first. "
            "<bookmark mark='c'/> Every small triangle has one vertex of each colour: three views that occur "
            "together in one run. <bookmark mark='d'/> Two rounds give a hundred and sixty-nine. However many "
            "rounds, the protocol complex is a subdivision of the triangle, with no holes, and that is what the "
            "impossibility proof will use."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(c0[0]), FadeIn(c0[1]), FadeIn(cl), FadeIn(caps[0]))
            vo.wait_until("b")
            self.play(GrowArrow(arrs[0]), Create(c1[0]), run_time=1.5)
            self.play(FadeIn(c1[1]), FadeIn(caps[1]))
            self.play(FadeIn(hm), FadeIn(hc), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]), Indicate(c1[1], scale_factor=1.3))
            vo.wait_until("d")
            self.play(GrowArrow(arrs[1]), Create(c2[0]), run_time=2.0)
            self.play(FadeIn(c2[1]), FadeIn(caps[2]))
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def sperner(self):
        sp = load("sperner")
        ex, chk = sp["example"], sp["check"]
        k = ex["k"]
        col = {(i, j): c for i, j, c in ex["colours"]}
        head = label(r"Sperner's lemma \ (1928)", font_size=36).to_edge(UP, buff=0.3)
        A0, A1, A2 = np.array([-6.4, -2.35, 0]), np.array([-1.0, -2.35, 0]), np.array([-3.7, -2.35 + 5.4 * 0.866, 0])

        def P(i, j):
            return (i * A0 + j * A1 + (k - i - j) * A2) / k
        tris = []
        for i in range(k):
            for j in range(k - i):
                tris.append(((i, j), (i + 1, j), (i, j + 1)))
                if i + j + 1 < k:
                    tris.append(((i + 1, j), (i + 1, j + 1), (i, j + 1)))
        polys = VGroup(*[Polygon(*[P(*v) for v in t], stroke_color=GREY_C, stroke_width=1.2) for t in tris])
        dots = VGroup(*[Dot(P(*v), radius=0.075, color=PC[c]).set_z_index(2) for v, c in col.items()])
        rb = VGroup(*[Polygon(*[P(*v) for v in t], stroke_width=0, fill_color=HEAD, fill_opacity=0.55)
                      for t in ex["rainbow"]])
        side = [(k - j, j) for j in range(k + 1)]          # the 0-1 side, from corner 0 to corner 1
        doors = VGroup(*[Line(P(*a), P(*b), color=YES, stroke_width=7) for a, b in zip(side, side[1:])
                         if {col[a], col[b]} == {0, 1}])
        cn = VGroup(MathTex("0", font_size=26, color=PC[0]).next_to(A0, DL, buff=0.08),
                    MathTex("1", font_size=26, color=PC[1]).next_to(A1, DR, buff=0.08),
                    MathTex("2", font_size=26, color=PC[2]).next_to(A2, UP, buff=0.1))
        W = 6.6
        rule = wrapped_label(r"corners 0, 1, 2; \ on a side, \ one of its two corners' colours; \ inside, \ anything",
                             W, font_size=19, color=WHITE)
        fs = 27
        rows = [MathTex(r"\sum_{\triangle} \mathrm{doors}(\triangle)", r"=", r"2D_{\mathrm{in}}", r"+",
                        r"D_{\partial}", font_size=fs),
                MathTex(r"\#\mathrm{rainbow}", r"+", r"2\,(\cdots)", r"=", r"2D_{\mathrm{in}}", r"+",
                        r"D_{\partial}", font_size=fs),
                MathTex(r"\#\mathrm{rainbow}", r"\equiv", r"D_{\partial}", r"\equiv", r"1", r"\pmod 2", font_size=fs)]
        rows[2][4].set_color(YES)
        whys = [label(r"a door: \ an edge coloured 0--1; \ inside, \ it borders two triangles", font_size=18,
                      color=GREY_B),
                label(r"a rainbow triangle has one door, \ any other none or two", font_size=18, color=GREY_B),
                wrapped_label(r"boundary doors lie on the 0--1 side, \ where the colour switches from 0 to 1 an odd "
                              r"number of times", W, font_size=18, color=GREY_B)]
        colg = VGroup()
        for r, w in zip(rows, whys):
            w.next_to(r, DOWN, buff=0.08, aligned_edge=LEFT)
            colg.add(VGroup(r, w))
        colg.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        here = label(rf"here: \ {ex['count']} rainbow of {ex['triangles']} triangles, \ {len(doors)} boundary doors",
                     font_size=19, color=HEAD)
        check = wrapped_label(rf"{chk['trials']} more random colourings of a finer, \ 100-triangle grid: \ {chk['min']} to {chk['max']} rainbow "
                              r"triangles, \ " + (r"always odd" if chk["all_odd"] else r"not always odd"), W,
                              font_size=19, color=YES if chk["all_odd"] else NO)
        right = VGroup(rule, colg, here, check).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([3.3, -0.1, 0])
        src = note(r"computed by theory.py", font_size=16).next_to(right, DOWN, buff=0.12).align_to(right, LEFT)
        with self.voiceover(
            "The tool is a lemma Emanuel Sperner proved in 1928. <bookmark mark='a'/> Cut a triangle into small "
            "ones and colour the vertices: the corners zero, one and two; a vertex on a side, one of that side's "
            "corner colours; inside, anything. <bookmark mark='b'/> Then some small triangle has all three "
            "colours; in fact an odd number do, here nineteen of sixty-four. <bookmark mark='c'/> The proof counts "
            "doors, edges coloured zero and one. Over all small triangles, an inside door is counted twice and a "
            "boundary door once. <bookmark mark='d'/> A rainbow triangle has exactly one door, any other none or "
            "two. <bookmark mark='e'/> So the rainbow count has the parity of the boundary doors, which all lie on "
            "the zero-one side, where the colour switches an odd number of times. Two hundred more random "
            "colourings, of a finer grid of a hundred triangles: always odd."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(polys), run_time=1.5)
            self.play(FadeIn(dots), FadeIn(cn), FadeIn(rule))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t) for t in rb], lag_ratio=0.1), FadeIn(here), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(doors), FadeIn(colg[0]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            self.play(FadeIn(check), FadeIn(src))
        self.wait(0.4)
        self.clear_scene()

    def kset(self):
        head = label(r"$k$-set agreement is impossible for $k \le f$", font_size=36).to_edge(UP, buff=0.3)
        tris = [s for t in chrom(base_tri(-3.6, -0.1, 5.4)) for s in chrom(t)]
        cx = draw_complex(tris, r=0.06, stroke=0.9)
        decide = [PC[min(v[2])] for v in cx.verts]
        rainbow = [t for t in tris if len({min(v[2]) for v in t}) == 3]
        rb = VGroup(*[Polygon(*[p for _, p, _ in t], stroke_color=HEAD, stroke_width=3, fill_color=HEAD,
                              fill_opacity=0.6) for t in rainbow])
        ring = Circle(radius=0.4, color=HEAD, stroke_width=3).move_to(rb.get_center())
        rl = label(r"three decisions", font_size=17, color=HEAD).next_to(ring, LEFT, buff=0.15).shift(UP * 0.4)
        leg0 = label(r"colour = process", font_size=18, color=GREY_A).next_to(cx, DOWN, buff=0.25)
        leg1 = label(r"colour = the id it decides", font_size=18, color=HEAD).move_to(leg0)
        W = 6.2
        notes = VGroup(
            wrapped_label(r"\textbf{$k$-set agreement}: \ decide an input; \ at most $k$ different decisions \ "
                          r"(Chaudhuri, \ 1990)", W, font_size=19, color=WHITE),
            wrapped_label(r"$k > f$: \ wait for $n - f$ values, \ decide the smallest; \ all decisions lie among the "
                          r"$f + 1$ smallest inputs", W, font_size=19, color=YES),
            wrapped_label(r"three processes, \ $k = 2$, \ wait-free: \ process $i$ starts with input $i$", W,
                          font_size=19, color=GREY_A),
            wrapped_label(r"a process decides an id it has seen: \ corners their own, \ a side's vertices one of its "
                          r"ends: \ a \textbf{Sperner colouring}", W, font_size=19, color=HEAD),
            wrapped_label(r"so some triangle is rainbow: \ a run where three values are decided", W, font_size=19,
                          color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to([3.55, 0.35, 0])
        ill = note(rf"illustrative protocol, \ two rounds: \ decide the smallest id seen \ ({len(rainbow)} rainbow)",
                   font_size=16).next_to(leg0, DOWN, buff=0.1)
        fs = 28
        eq = [MathTex(r"k > f", r"\Rightarrow", r"\text{solvable}", font_size=fs),
              MathTex(r"k \le f", r"\Rightarrow", r"\text{impossible}", font_size=fs)]
        eq[0][2].set_color(YES)
        eq[1][2].set_color(NO)
        eqs = VGroup(*eq).arrange(RIGHT, buff=0.8).next_to(notes, DOWN, buff=0.35)
        src = note(r"Borowsky and Gafni; \ Herlihy and Shavit; \ Saks and Zaharoglou \ (1993)", font_size=16).next_to(
            eqs, DOWN, buff=0.15)
        with self.voiceover(
            "Soma Chaudhuri asked in 1990 about a weaker agreement. <bookmark mark='a'/> In k-set agreement each "
            "process decides one of the inputs, and at most k different values may be decided. "
            "<bookmark mark='b'/> With f crashes it is easy when k is more than f: wait for n minus f values and "
            "decide the smallest. <bookmark mark='c'/> And for smaller k? Take three processes, two values "
            "allowed, no waiting, and give process i the input i. <bookmark mark='d'/> A process may only decide "
            "an id it has seen, so a corner decides its own, and a vertex on a side one of that side's ends. That "
            "is a Sperner colouring. <bookmark mark='e'/> So some triangle is rainbow: a run in which three values "
            "are decided. In 1993 three teams proved the general case: k-set agreement is impossible whenever k is "
            "at most f."
        ) as vo:
            self.play(FadeIn(head), Create(cx[0]), FadeIn(cx[1]), FadeIn(leg0), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]), FadeIn(eq[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(*[d.animate.set_color(c) for d, c in zip(cx[1], decide)], ReplacementTransform(leg0, leg1),
                      run_time=1.5)
            self.play(FadeIn(notes[3]), FadeIn(ill))
            vo.wait_until("e")
            self.play(FadeIn(rb), Create(ring), FadeIn(rl))
            self.play(FadeIn(notes[4]), TransformMatchingTex(eq[0].copy(), eq[1]), FadeIn(src))
        self.wait(0.4)
        self.clear_scene()

    def theorem(self):
        head = label(r"The asynchronous computability theorem", font_size=36).to_edge(UP, buff=0.3)
        cy = 1.0
        ci = draw_complex([base_tri(-5.2, cy, 2.4)], r=0.11, stroke=2)
        cs = draw_complex([s for t in chrom(base_tri(-0.9, cy, 3.0)) for s in chrom(t)], r=0.04, stroke=0.7)
        # an illustrative output complex: three triangles sharing vertices
        O = [np.array(p) for p in ([3.3, 0.0, 0], [4.5, 0.0, 0], [3.9, 1.05, 0], [5.1, 1.05, 0], [4.5, 2.1, 0],
                                   [5.7, 0.0, 0])]
        ocol = [0, 1, 2, 0, 1, 2]
        otr = [(0, 1, 2), (1, 3, 2), (2, 3, 4), (1, 5, 3)]
        oc = VGroup(VGroup(*[Polygon(O[a], O[b], O[c], stroke_color=GREY_C, stroke_width=2) for a, b, c in otr]),
                    VGroup(*[Dot(p, radius=0.1, color=PC[c]).set_z_index(2) for p, c in zip(O, ocol)]))
        a1 = Arrow([-3.85, cy, 0], [-2.55, cy, 0], buff=0, color=GREY_B, stroke_width=2.5)
        a2 = Arrow([0.75, cy, 0], [3.0, cy, 0], buff=0, color=HEAD, stroke_width=3)
        l1 = label(r"run", font_size=17, color=GREY_B).next_to(a1, UP, buff=0.1)
        l2 = MathTex(r"\delta", font_size=30, color=HEAD).next_to(a2, UP, buff=0.1)
        caps = VGroup(label(r"inputs $\mathcal{I}$", font_size=19, color=GREY_A).move_to([-5.2, -0.6, 0]),
                      label(r"a subdivision $\sigma(\mathcal{I})$", font_size=19, color=GREY_A).move_to(
                          [-0.9, -0.6, 0]),
                      label(r"outputs $\mathcal{O}$", font_size=19, color=GREY_A).move_to([4.5, -0.6, 0]))
        ill = note(r"illustrative output complex", font_size=16).next_to(caps[2], DOWN, buff=0.1)
        rule = label(r"$\delta$: \ each vertex to a vertex of the same process; \ each simplex to an output "
                     r"$\Delta$ allows", font_size=19, color=HEAD).next_to(caps, DOWN, buff=0.5)
        thm = wrapped_label(r"\textbf{Herlihy and Shavit \ (1993)}: \ a task is solvable wait-free with read/write "
                            r"registers \textbf{if and only if} some chromatic subdivision of its input complex has "
                            r"such a map $\delta$ to its output complex", 11.6, font_size=21, color=WHITE)
        box = SurroundingRectangle(thm, buff=0.2, color=HEAD, corner_radius=0.1, stroke_width=2)
        tg = VGroup(box, thm).next_to(rule, DOWN, buff=0.35)
        foot = wrapped_label(r"2004 G\"odel Prize: \ Herlihy and Shavit, \ and Saks and Zaharoglou. \ Read: \ "
                             r"Herlihy, \ Kozlov and Rajsbaum, \ \textit{Distributed Computing through Combinatorial "
                             r"Topology} \ (2013)", 12.4, font_size=18, color=GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Herlihy and Shavit turned the picture into a theorem. <bookmark mark='a'/> Running a wait-free "
            "protocol with registers subdivides the input complex. <bookmark mark='b'/> The decisions are a map "
            "from that subdivision to the outputs, sending each vertex to a vertex of the same process, and each "
            "simplex to an output that delta allows. <bookmark mark='c'/> The asynchronous computability theorem "
            "says that is all there is: a task is solvable wait-free with registers exactly when such a subdivision "
            "and such a map exist. Solvability became a question about shape. <bookmark mark='d'/> The 2004 Gödel "
            "Prize went to Herlihy and Shavit, and to Saks and Zaharoglou, for this work."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ci), FadeIn(caps[0]))
            vo.wait_until("a")
            self.play(GrowArrow(a1), FadeIn(l1), Create(cs[0]), FadeIn(cs[1]), FadeIn(caps[1]), run_time=1.8)
            vo.wait_until("b")
            self.play(FadeIn(oc), FadeIn(caps[2]), FadeIn(ill))
            self.play(GrowArrow(a2), FadeIn(l2), FadeIn(rule))
            vo.wait_until("c")
            self.play(FadeIn(tg))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, KERN, LAM, NO, YES)
