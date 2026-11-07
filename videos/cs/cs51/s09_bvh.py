from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs51.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load

# The illustrative 2D example: forty small triangles in a field on the left of the frame, a BVH over them built by
# median splits (leaves of at most three), and one ray traced through it.  The measured numbers come from our 3D BVH
# (explainer/cs/graphics/ray.py) through load("bvh").
FIELD = (-6.4, -0.8, -2.6, 2.3)            # x0, x1, y0, y1
DEPTH_COL = [GREY_A, DATA, LAM, KERN, YES]


def field_tris(n: int = 40, seed: int = 8) -> np.ndarray:
    rng = np.random.default_rng(seed)
    x0, x1, y0, y1 = FIELD
    c = np.c_[rng.uniform(x0 + 0.3, x1 - 0.3, n), rng.uniform(y0 + 0.3, y1 - 0.3, n)]
    a = rng.uniform(0, 2 * np.pi, n)
    out = []
    for k in range(n):
        angs = a[k] + np.array([0.0, 2.1, 4.2]) + rng.uniform(-0.3, 0.3, 3)
        r = rng.uniform(0.16, 0.3, 3)
        out.append(c[k] + np.c_[r * np.cos(angs), r * np.sin(angs)])
    return np.array(out)


def build(tris, idx=None, depth=0, max_leaf=3, nodes=None):
    """Median split along the wider axis of the centroids; nodes as dicts (lo, hi, depth, kids, tris)."""
    if nodes is None:
        nodes = []
    idx = np.arange(len(tris)) if idx is None else idx
    pts = tris[idx].reshape(-1, 2)
    node = {"lo": pts.min(0), "hi": pts.max(0), "depth": depth, "kids": [], "tris": []}
    nodes.append(node)
    if len(idx) <= max_leaf:
        node["tris"] = list(idx)
        return nodes
    cen = tris[idx].mean(1)
    ax = int(np.argmax(cen.max(0) - cen.min(0)))
    order = idx[np.argsort(cen[:, ax])]
    m = len(order) // 2
    for part in (order[:m], order[m:]):
        node["kids"].append(len(nodes))
        build(tris, part, depth + 1, max_leaf, nodes)
    return nodes


def slab(o, d, lo, hi):
    """Kay and Kajiya's slab test: the parameter interval [t_enter, t_exit] of the ray inside the box, or None."""
    t0, t1 = 0.0, np.inf
    for a in range(2):
        if abs(d[a]) < 1e-12:
            if not lo[a] <= o[a] <= hi[a]:
                return None
            continue
        ta, tb = (lo[a] - o[a]) / d[a], (hi[a] - o[a]) / d[a]
        t0, t1 = max(t0, min(ta, tb)), min(t1, max(ta, tb))
    return (t0, t1) if t0 <= t1 else None


def ray_tri(o, d, tri):
    """Nearest t at which the ray crosses the triangle's boundary (2D), or inf."""
    best = np.inf
    for k in range(3):
        p, q = tri[k], tri[(k + 1) % 3]
        e = q - p
        den = d[0] * e[1] - d[1] * e[0]
        if abs(den) < 1e-12:
            continue
        w = p - o
        t = (w[0] * e[1] - w[1] * e[0]) / den
        s = (w[0] * d[1] - w[1] * d[0]) / den
        if t > 1e-9 and 0 <= s <= 1:
            best = min(best, t)
    return best


def traverse(nodes, tris, o, d):
    """Closest-hit traversal, near child first, pruning boxes beyond the best hit so far.  Returns the events
    (node, 'hit' or 'miss'), the triangles tested and the hit (t, triangle)."""
    events, tested = [], []
    best, who = np.inf, -1
    stack = [0]
    while stack:
        k = stack.pop()
        nd = nodes[k]
        iv = slab(o, d, nd["lo"], nd["hi"])
        if iv is None or iv[0] > best:
            events.append((k, "miss"))
            continue
        events.append((k, "hit"))
        if nd["tris"]:
            for j in nd["tris"]:
                tested.append(j)
                t = ray_tri(o, d, tris[j])
                if t < best:
                    best, who = t, j
        else:
            a, b = nd["kids"]
            ta = slab(o, d, nodes[a]["lo"], nodes[a]["hi"])
            tb = slab(o, d, nodes[b]["lo"], nodes[b]["hi"])
            ka = ta[0] if ta else np.inf
            kb = tb[0] if tb else np.inf
            stack += [a, b] if ka > kb else [b, a]       # the nearer child is popped first
    return events, tested, (best, who)


def P(v):
    return np.array([v[0], v[1], 0.0])


def tri_mobs(tris, color=GREY_B):
    return VGroup(*[Polygon(*[P(p) for p in t], stroke_color=color, stroke_width=1.5, fill_color=color,
                            fill_opacity=0.25) for t in tris])


def box_mob(nd, pad=0.04, width=2.0):
    lo, hi = nd["lo"] - pad * (4 - nd["depth"]) / 4, nd["hi"] + pad * (4 - nd["depth"]) / 4
    return Rectangle(width=hi[0] - lo[0], height=hi[1] - lo[1], stroke_color=DEPTH_COL[min(nd["depth"], 4)],
                     stroke_width=width).move_to(P((lo + hi) / 2))


def tree_layout(nodes, x0=0.6, x1=6.6, y_top=2.45, dy=0.5):
    leaves = []

    def walk(k):
        if not nodes[k]["kids"]:
            leaves.append(k)
        for c in nodes[k]["kids"]:
            walk(c)
    walk(0)
    pos = {}
    xs = np.linspace(x0, x1, len(leaves))
    for x, k in zip(xs, leaves):
        pos[k] = np.array([x, y_top - nodes[k]["depth"] * dy, 0])

    def place(k):
        if k in pos:
            return pos[k]
        ps = [place(c) for c in nodes[k]["kids"]]
        pos[k] = np.array([np.mean([p[0] for p in ps]), y_top - nodes[k]["depth"] * dy, 0])
        return pos[k]
    place(0)
    return pos


def tree_mobs(nodes, pos):
    dots = {k: Dot(pos[k], radius=0.075, color=DEPTH_COL[min(nodes[k]["depth"], 4)]) for k in pos}
    edges = VGroup(*[Line(pos[k], pos[c], color=GREY_D, stroke_width=1.5) for k in pos for c in nodes[k]["kids"]])
    return dots, edges


class Bvh(VoiceoverScene):
    def construct(self):
        self.card()
        self.brute()
        self.boxes()
        self.traversal()
        self.sah()
        self.measured()

    def card(self):
        card = chapter_card(8, r"Acceleration structures", r"Must every ray test every triangle?",
                            lit=(1980, 1986, 1990), extra=((1980, r"Rubin and Whitted: \ boxes in boxes"),
                                                           (1986, r"Kay and Kajiya: \ slabs"),
                                                           (1990, r"MacDonald and Booth: \ the SAH")), part=PART)
        with self.voiceover("Chapter eight. Acceleration structures."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def frame(self):
        x0, x1, y0, y1 = FIELD
        return Rectangle(width=x1 - x0, height=y1 - y0, stroke_color=GREY_D, stroke_width=1).move_to(
            P(((x0 + x1) / 2, (y0 + y1) / 2)))

    def ray(self):
        o = np.array([-6.4, -1.27])
        return o, np.array([math.cos(-0.2), math.sin(-0.2)])

    def brute(self):
        b = load("bvh")["rows"]
        w = load("whitted")
        nmax = b[-1]["n"]
        head = label(r"Every ray against every triangle", font_size=36).to_edge(UP, buff=0.3)
        tris = field_tris()
        tm = tri_mobs(tris)
        fr = self.frame()
        o, d = self.ray()
        hits = [(ray_tri(o, d, t), j) for j, t in enumerate(tris)]
        t_hit, j_hit = min(hits)
        rl = Arrow(P(o), P(o + t_hit * d), buff=0, color=HEAD, stroke_width=3, max_tip_length_to_length_ratio=0.03)
        hd = Dot(P(o + t_hit * d), radius=0.08, color=HEAD)
        cnt = ValueTracker(0)
        ctr = always_redraw(lambda: label(rf"triangles tested: \ {int(cnt.get_value())} of {len(tris)}",
                                          font_size=20, color=HEAD).next_to(fr, DOWN, buff=0.15))
        ill = note(r"illustrative", font_size=16).next_to(fr, UP, buff=0.08).align_to(fr, RIGHT)
        total = w["counts"]["total"] * nmax
        mant, ex = f"{total:.1e}".split("e")
        rows = VGroup(
            MathTex(rf"{w['counts']['total']:,}".replace(",", "{,}") + r"\ \text{rays}", font_size=32),
            MathTex(r"\times\ " + rf"{nmax:,}".replace(",", "{,}") + r"\ \text{triangles}", font_size=32),
            MathTex(rf"\approx {mant} \times 10^{{{int(ex)}}}\ \text{{tests}}", font_size=32, color=NO),
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.25).move_to([3.6, 1.4, 0])
        rl1 = note(r"our Whitted image's rays", font_size=17).next_to(rows[0], LEFT, buff=0.3)
        rl2 = note(r"our largest test mesh", font_size=17).next_to(rows[1], LEFT, buff=0.3)
        notes = VGroup(
            wrapped_label(r"each ray keeps only the nearest hit: \ almost every test is wasted", 5.8, font_size=19,
                          color=WHITE),
            wrapped_label(r"the cure \ (Rubin and Whitted, \ 1980): \ wrap groups of triangles in boxes, \ and "
                          r"boxes in bigger boxes; \ a ray that misses a box skips everything inside", 5.8,
                          font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(rows, DOWN, buff=0.5).set_x(3.6)
        with self.voiceover(
            "A ray tracer spends nearly all its time on one question: which triangle does this ray hit first? "
            "<bookmark mark='a'/> The obvious answer tests every triangle and keeps the nearest. "
            "<bookmark mark='b'/> Forty triangles, forty tests, for one hit. <bookmark mark='c'/> Our Whitted image "
            "used forty-one and a half thousand rays. Against a mesh of a hundred thousand triangles, the largest "
            "we test below, that is over four billion intersection tests for a tiny picture. "
            "<bookmark mark='d'/> And almost all of them are wasted: each ray keeps one answer. "
            "<bookmark mark='e'/> The cure, from Steven Rubin and Turner Whitted in 1980, is the same as for a "
            "library: put things in boxes, and boxes in bigger boxes. A ray that misses a box can skip everything "
            "inside it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(fr), FadeIn(tm), FadeIn(ill))
            vo.wait_until("a")
            self.play(GrowArrow(rl), FadeIn(ctr))
            vo.wait_until("b")
            self.play(cnt.animate.set_value(len(tris)),
                      LaggedStart(*[Indicate(m, color=NO, scale_factor=1.3) for m in tm], lag_ratio=0.08),
                      run_time=4)
            self.play(FadeIn(hd), tm[j_hit].animate.set_fill(HEAD, 0.8).set_stroke(HEAD))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]), FadeIn(rl1))
            self.play(FadeIn(rows[1]), FadeIn(rl2))
            self.play(Write(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[0]))
            vo.wait_until("e")
            self.play(FadeIn(notes[1]))
        ctr.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def boxes(self):
        head = label(r"A bounding volume hierarchy", font_size=36).to_edge(UP, buff=0.3)
        tris = field_tris()
        nodes = build(tris)
        tm = tri_mobs(tris)
        fr = self.frame()
        depth = max(n["depth"] for n in nodes)
        levels = [VGroup(*[box_mob(n) for n in nodes if n["depth"] == k]) for k in range(depth + 1)]
        pos = tree_layout(nodes)
        dots, edges = tree_mobs(nodes, pos)
        tl = [VGroup(*[dots[k] for k in pos if nodes[k]["depth"] == lv]) for lv in range(depth + 1)]
        el = [VGroup(*[Line(pos[k], pos[c], color=GREY_D, stroke_width=1.5) for k in pos
                       if nodes[k]["depth"] == lv - 1 for c in nodes[k]["kids"]]) for lv in range(depth + 1)]
        leaves = [n for n in nodes if not n["kids"]]
        ill = note(r"illustrative", font_size=16).next_to(fr, UP, buff=0.08).align_to(fr, RIGHT)
        tlab = label(rf"the tree: \ {len(nodes)} nodes, \ {len(leaves)} leaves", font_size=19,
                     color=GREY_A).next_to(VGroup(*dots.values()), DOWN, buff=0.25)
        notes = VGroup(
            wrapped_label(r"split the triangles at the median along the wider axis; \ box each half; \ repeat until "
                          rf"at most {max(len(n['tris']) for n in leaves)} remain", 6.0, font_size=19, color=WHITE),
            wrapped_label(r"boxes may overlap: \ a BVH divides the \textit{objects}, \ not space, \ so every "
                          r"triangle is in exactly one leaf", 6.0, font_size=19, color=HEAD),
            wrapped_label(rf"{len(tris)} triangles, \ {depth} levels: \ the depth grows like $\log_2 n$", 6.0,
                          font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tlab, DOWN, buff=0.4).set_x(3.6)
        with self.voiceover(
            "Here is the idea built on our forty triangles. <bookmark mark='a'/> Put one box around everything: the "
            "root. <bookmark mark='b'/> Sort the triangles along the box's wider side and split them at the median, "
            "boxing each half. <bookmark mark='c'/> Repeat inside each half, <bookmark mark='d'/> and again, until a "
            "box holds at most three triangles. Each box is a node of a binary tree, the leaves hold the triangles. "
            "<bookmark mark='e'/> The boxes of two children may overlap. A bounding volume hierarchy divides the "
            "objects, not space, so every triangle lives in exactly one leaf, and a box can be refitted cheaply when "
            "its triangles move. <bookmark mark='f'/> Halving at every level, the depth grows like the logarithm of "
            "the number of triangles."
        ) as vo:
            self.play(FadeIn(head), FadeIn(fr), FadeIn(tm), FadeIn(ill))
            vo.wait_until("a")
            self.play(Create(levels[0]), FadeIn(tl[0]))
            vo.wait_until("b")
            self.play(Create(levels[1]), FadeIn(tl[1]), Create(el[1]), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(Create(levels[2]), FadeIn(tl[2]), Create(el[2]))
            vo.wait_until("d")
            for k in range(3, depth + 1):
                self.play(Create(levels[k]), FadeIn(tl[k]), Create(el[k]), run_time=0.8)
            self.play(FadeIn(tlab))
            vo.wait_until("e")
            self.play(FadeIn(notes[1]))
            vo.wait_until("f")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def traversal(self):
        head = label(r"Walking the tree", font_size=36).to_edge(UP, buff=0.3)
        tris = field_tris()
        nodes = build(tris)
        tm = tri_mobs(tris, color=GREY_C)
        fr = self.frame()
        allb = VGroup(*[box_mob(n, width=1.0).set_stroke(opacity=0.35) for n in nodes])
        pos = tree_layout(nodes)
        dots, edges = tree_mobs(nodes, pos)
        for dm in dots.values():
            dm.set_color(GREY_D)
        o, d = self.ray()
        events, tested, (t_hit, j_hit) = traverse(nodes, tris, o, d)
        rl = Arrow(P(o), P(o + t_hit * d), buff=0, color=HEAD, stroke_width=3, max_tip_length_to_length_ratio=0.03)
        rows = VGroup(
            MathTex(r"t_x = \frac{x_{\min} - o_x}{d_x},\ \frac{x_{\max} - o_x}{d_x}", font_size=28),
            MathTex(r"t_{\text{in}} = \max(\min t_x, \min t_y),\quad t_{\text{out}} = \min(\max t_x, \max t_y)",
                    font_size=26),
            MathTex(r"\text{hit} \iff t_{\text{in}} \le t_{\text{out}}", font_size=28, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.6, -1.05, 0])
        why = note(r"Kay and Kajiya's slabs: \ the ray's interval inside each pair of planes", font_size=17)
        why.next_to(rows, UP, buff=0.15).align_to(rows, LEFT)
        nh = sum(1 for _, r in events if r == "hit")
        nm = len(events) - nh
        res = wrapped_label(rf"this ray: \ {len(events)} boxes tested \ ({nh} entered, \ {nm} skipped), \ "
                            rf"{len(tested)} triangles tested of {len(tris)}", 6.2, font_size=19,
                            color=HEAD).to_edge(DOWN, buff=0.45).set_x(3.6)
        ill = note(r"illustrative", font_size=16).next_to(fr, UP, buff=0.08).align_to(fr, RIGHT)
        anims = []
        for k, r in events:
            col = YES if r == "hit" else NO
            bx = box_mob(nodes[k], width=3.0).set_stroke(col)
            step = [Create(bx), dots[k].animate.set_color(col).scale(1.3)]
            if r == "hit" and nodes[k]["tris"]:
                step += [tm[j].animate.set_fill(KERN, 0.6).set_stroke(KERN) for j in nodes[k]["tris"]]
            anims.append(AnimationGroup(*step))
        with self.voiceover(
            "Now trace a ray through the tree. <bookmark mark='a'/> Testing a box is cheap: Kay and Kajiya's slab "
            "test. For each axis, find where the ray enters and leaves the slab between the box's two planes. "
            "<bookmark mark='b'/> The ray is inside the box between the latest entry and the earliest exit, so it "
            "hits the box when that interval is not empty. <bookmark mark='c'/> Start at the root. At each box it "
            "enters, visit the nearer child first; skip a box it misses, or one that begins beyond the best hit "
            "found so far. <bookmark mark='d'/> In the leaves it reaches, test the triangles. "
            "<bookmark mark='e'/> This ray needed a handful of boxes and a few triangles instead of all forty, and "
            "found the same nearest hit."
        ) as vo:
            self.play(FadeIn(head), FadeIn(fr), FadeIn(tm), FadeIn(allb), FadeIn(edges),
                      *[FadeIn(m) for m in dots.values()], FadeIn(ill), GrowArrow(rl))
            vo.wait_until("a")
            self.play(FadeIn(why), Write(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(Succession(*anims, lag_ratio=1.0), run_time=min(9.0, 0.5 * len(anims)))
            vo.wait_until("d")
            self.play(tm[j_hit].animate.set_fill(HEAD, 0.9).set_stroke(HEAD),
                      FadeIn(Dot(P(o + t_hit * d), radius=0.08, color=HEAD)))
            vo.wait_until("e")
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    def sah(self):
        head = label(r"Where to split: \ the surface area heuristic", font_size=36).to_edge(UP, buff=0.3)
        rng = np.random.default_rng(3)
        x0, x1, y0, y1 = -6.4, -1.0, 0.0, 2.4
        pts_l = np.c_[rng.uniform(-6.2, -5.0, 9), rng.uniform(0.25, 2.15, 9)]
        pts_r = np.c_[rng.uniform(-3.6, -1.2, 3), rng.uniform(0.25, 2.15, 3)]
        cen = np.r_[pts_l, pts_r]
        sz = 0.13
        boxes = [(c - sz, c + sz) for c in cen]
        tm = VGroup(*[Square(2 * sz, stroke_color=GREY_B, stroke_width=1.5, fill_color=GREY_B,
                             fill_opacity=0.3).move_to(P(c)) for c in cen])
        parent = Rectangle(width=x1 - x0, height=y1 - y0, stroke_color=GREY_A, stroke_width=2).move_to(
            P(((x0 + x1) / 2, (y0 + y1) / 2)))
        lo_all = np.min([b[0] for b in boxes], 0)
        hi_all = np.max([b[1] for b in boxes], 0)

        def per(lo, hi):
            return 2 * ((hi[0] - lo[0]) + (hi[1] - lo[1]))
        A = per(lo_all, hi_all)

        def cost(xs):
            L = [b for b, c in zip(boxes, cen) if c[0] < xs]
            R = [b for b, c in zip(boxes, cen) if c[0] >= xs]
            if not L or not R:
                return None
            pl = per(np.min([b[0] for b in L], 0), np.max([b[1] for b in L], 0))
            pr = per(np.min([b[0] for b in R], 0), np.max([b[1] for b in R], 0))
            return 1 + (pl * len(L) + pr * len(R)) / A
        xs = np.linspace(-6.3, -1.1, 261)
        cs = [(x, cost(x)) for x in xs if cost(x) is not None]
        ax = Axes(x_range=[x0, x1, 1], y_range=[4, 13, 3], x_length=x1 - x0, y_length=2.2,
                  axis_config={"color": GREY_D, "include_ticks": False}).move_to(P(((x0 + x1) / 2, -1.55)))
        curve = VMobject(color=YES, stroke_width=3).set_points_as_corners([ax.c2p(x, c) for x, c in cs])
        leaf_line = DashedLine(ax.c2p(x0, len(cen)), ax.c2p(x1, len(cen)), color=GREY_B, stroke_width=1.5)
        ll = label(rf"no split: \ {len(cen)} tests", font_size=16, color=GREY_B).next_to(leaf_line, UP, buff=0.04)
        ll.align_to(ax, RIGHT)
        best_x, best_c = min(cs, key=lambda p: p[1])
        med_x = float(np.sort(cen[:, 0])[len(cen) // 2]) - 1e-3
        med_c = cost(med_x)
        sweep = ValueTracker(-6.25)
        plane = always_redraw(lambda: DashedLine(P((sweep.get_value(), y0 - 0.05)), P((sweep.get_value(),
                                                                                         y1 + 0.05)),
                                                 color=HEAD, stroke_width=2.5))
        mark = always_redraw(lambda: Dot(ax.c2p(sweep.get_value(), cost(sweep.get_value()) or len(cen)), radius=0.07,
                                         color=HEAD))
        med = VGroup(Line(P((med_x, y0)), P((med_x, y1)), color=NO, stroke_width=3),
                     label(rf"median: \ {med_c:.1f}", font_size=17, color=NO).next_to(P((med_x, y1)), UP,
                                                                                         buff=0.08))
        best = VGroup(Line(P((best_x, y0)), P((best_x, y1)), color=YES, stroke_width=3),
                      label(rf"SAH: \ {best_c:.1f}", font_size=17, color=YES).next_to(P((best_x, y1)), UP,
                                                                                         buff=0.08))
        med[1].align_to(med[0], RIGHT).shift(LEFT * 0.08)
        best[1].align_to(best[0], LEFT).shift(RIGHT * 0.08)
        ill = note(r"the expected cost at each plane \ (illustrative; \ in 2D the perimeter plays the area's role)",
                   font_size=16).next_to(
            ax, DOWN, buff=0.15).align_to(ax, LEFT)
        rows = VGroup(
            MathTex(r"C", r"=", r"C_t + P_L\,N_L\,C_i + P_R\,N_R\,C_i", font_size=30),
            MathTex(r"P_L", r"=", r"\frac{S_L}{S}", font_size=30),
            MathTex(r"C", r"=", r"1 + \frac{S_L N_L + S_R N_R}{S}", font_size=30),
            MathTex(r"\text{leaf if}\ \ N \le C", font_size=30),
        )
        rows[2].set_color(YES)
        whys = VGroup(*[wrapped_label(t, 5.4, font_size=17, color=c) for t, c in (
            (r"one box test, \ then each child's triangles if the ray enters it", GREY_B),
            (r"a random ray that hits the parent hits a child with probability area over area \ "
             r"(Cauchy--Crofton)", GREY_B),
            (r"with $C_t = C_i = 1$, \ as in our builder", YES),
            (r"stop when splitting costs more than testing them all", GREY_B))])
        for r, wy in zip(rows, whys):
            wy.next_to(r, DOWN, buff=0.06).align_to(r, LEFT)
        VGroup(*[VGroup(r, wy) for r, wy in zip(rows, whys)]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(
            [3.6, 0.5, 0])
        with self.voiceover(
            "The median split ignores where the triangles are. Here, nine are bunched at the left and three spread "
            "to the right. Where should the box be cut? <bookmark mark='a'/> Price a split by its expected cost: "
            "one box test, plus each child's triangles, weighted by the chance that a ray entering the parent "
            "enters that child. <bookmark mark='b'/> For random rays that chance is the child's surface area over "
            "the parent's, a classical result of integral geometry. <bookmark mark='c'/> With both unit costs one, "
            "as in our builder, this is the surface area heuristic of MacDonald and Booth, 1990. "
            "<bookmark mark='d'/> Sweep a candidate plane across, as Part 22 swept lines, and evaluate the cost at "
            "each position. <bookmark mark='e'/> The median cuts through the cluster and leaves a wide box of six. "
            "The cheapest plane puts the whole cluster in one compact box, the three stragglers in another. "
            "<bookmark mark='f'/> And if no split beats testing every triangle, make a leaf."
        ) as vo:
            self.play(FadeIn(head), Create(parent), FadeIn(tm), Create(ax), FadeIn(ill))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(FadeIn(plane), FadeIn(mark), Create(leaf_line), FadeIn(ll))
            self.play(sweep.animate.set_value(-1.15), Create(curve), run_time=4, rate_func=linear)
            vo.wait_until("e")
            self.play(FadeIn(med), FadeOut(plane), FadeOut(mark))
            self.play(FadeIn(best))
            vo.wait_until("f")
            self.play(FadeIn(rows[3]), FadeIn(whys[3]))
        self.wait(0.4)
        self.clear_scene()

    def measured(self):
        rows = load("bvh")["rows"]
        head = label(r"Our BVH, \ measured", font_size=36).to_edge(UP, buff=0.3)
        lg = [math.log10(r["n"]) for r in rows]
        ax1 = Axes(x_range=[2, 5, 1], y_range=[0, 5, 1], x_length=5.0, y_length=3.4,
                   axis_config={"color": GREY_D, "include_ticks": True}).move_to([-3.5, 0.45, 0])
        xt1 = VGroup(*[label(rf"$10^{v}$", font_size=17, color=GREY_B).next_to(ax1.c2p(v, 0), DOWN, buff=0.1)
                       for v in (2, 3, 4, 5)])
        yt1 = VGroup(*[label(rf"$10^{v}$" if v else "1", font_size=17, color=GREY_B).next_to(
            ax1.c2p(2, v), LEFT, buff=0.1) for v in range(6)])
        xl1 = label(r"triangles in the mesh", font_size=17, color=GREY_A).next_to(xt1, DOWN, buff=0.1)
        yl1 = label(r"triangle tests per ray", font_size=17, color=GREY_A).next_to(ax1, UP, buff=0.1).align_to(
            ax1, LEFT)

        def series(ax, key, col, xs=lg, f=lambda v: math.log10(v)):
            pts = [ax.c2p(x, f(r[key])) for x, r in zip(xs, rows)]
            return VGroup(VMobject(color=col, stroke_width=3).set_points_as_corners(pts),
                          *[Dot(p, radius=0.06, color=col) for p in pts])
        brute = series(ax1, "brute_tests", NO)
        med = series(ax1, "median_tests", HEAD)
        sah = series(ax1, "sah_tests", YES)
        tags1 = VGroup(label(r"brute force", font_size=17, color=NO).next_to(brute[-1], LEFT, buff=0.15),
                       label(r"median", font_size=17, color=HEAD).next_to(med[-1], RIGHT, buff=0.12),
                       label(r"SAH", font_size=17, color=YES).next_to(sah[-1], RIGHT, buff=0.12))
        l2 = [r["log2_n"] for r in rows]
        ax2 = Axes(x_range=[0, 18, 3], y_range=[0, 50, 10], x_length=4.4, y_length=3.4,
                   axis_config={"color": GREY_D, "include_ticks": True}).move_to([3.4, 0.45, 0])
        xt2 = VGroup(*[label(rf"{v}", font_size=17, color=GREY_B).next_to(ax2.c2p(v, 0), DOWN, buff=0.1)
                       for v in (0, 6, 12, 18)])
        yt2 = VGroup(*[label(rf"{v}", font_size=17, color=GREY_B).next_to(ax2.c2p(0, v), LEFT, buff=0.1)
                       for v in (0, 25, 50)])
        xl2 = label(r"$\log_2$ of the number of triangles", font_size=17, color=GREY_A).next_to(xt2, DOWN, buff=0.1)
        yl2 = label(r"boxes visited per ray", font_size=17, color=GREY_A).next_to(ax2, UP, buff=0.1).align_to(
            ax2, LEFT)
        v_med = series(ax2, "median_visits", HEAD, xs=l2, f=lambda v: v)
        v_sah = series(ax2, "sah_visits", YES, xs=l2, f=lambda v: v)
        tags2 = VGroup(label(r"median", font_size=17, color=HEAD).next_to(v_med[-1], UP, buff=0.12),
                       label(r"SAH", font_size=17, color=YES).next_to(v_sah[-1], DOWN, buff=0.12))
        last = rows[-1]
        incs = [b["sah_visits"] - a["sah_visits"] for a, b in zip(rows, rows[1:])]
        notes = VGroup(
            wrapped_label(rf"{last['n']:,} triangles: \ {last['sah_tests']:.1f} triangle tests and "
                          rf"{last['sah_visits']:.0f} boxes per ray, \ against {last['brute_tests']:,}; \ the same "
                          rf"nearest hit as brute force on {100 * min(r['agree'] for r in rows):.0f}\% of the rays "
                          r"checked".replace(",", "{,}"), 12.4, font_size=19, color=YES),
            wrapped_label(rf"each tenfold increase in triangles adds {min(incs):.0f} to {max(incs):.0f} box visits: "
                          rf"$O(\log n)$ per ray; \ the SAH tree is deeper \ ({last['sah_depth']} levels against "
                          rf"{last['median_depth']}) \ yet cheaper to walk", 12.4, font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Now our real BVH, in three dimensions, built over random terrain meshes from a hundred to a hundred "
            "thousand triangles, and traced with a grid of camera rays. <bookmark mark='a'/> Brute force tests "
            "every triangle, a straight line on this logarithmic plot. <bookmark mark='b'/> With the median split, "
            "between about seven and ten triangle tests per ray, whatever the size. <bookmark mark='c'/> With the "
            "surface area heuristic, between two and three. <bookmark mark='d'/> The work moves into the boxes. "
            "Plotted against the logarithm of the number of triangles, the boxes visited per ray rise in a nearly "
            "straight line: every tenfold increase adds about nine. That is the logarithm per ray. "
            "<bookmark mark='e'/> At a hundred thousand triangles, each ray does two and a half triangle tests and "
            "visits thirty-nine boxes, instead of a hundred thousand tests, and on every ray we checked it finds the "
            "same nearest hit as brute force."
        ) as vo:
            self.play(FadeIn(head), Create(ax1), FadeIn(xt1), FadeIn(yt1), FadeIn(xl1), FadeIn(yl1))
            vo.wait_until("a")
            self.play(Create(brute), FadeIn(tags1[0]))
            vo.wait_until("b")
            self.play(Create(med), FadeIn(tags1[1]))
            vo.wait_until("c")
            self.play(Create(sah), FadeIn(tags1[2]))
            vo.wait_until("d")
            self.play(Create(ax2), FadeIn(xt2), FadeIn(yt2), FadeIn(xl2), FadeIn(yl2))
            self.play(Create(v_med), Create(v_sah), FadeIn(tags2), run_time=2)
            vo.wait_until("e")
            self.play(FadeIn(notes))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
