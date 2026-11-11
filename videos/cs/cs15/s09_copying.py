from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs15.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, cell_obj, load,
                                   mono, words)


def _fields(f):
    return ["p" if isinstance(x, str) and x not in ("f",) else (None if x is None else x) for x in f]


class Copying(VoiceoverScene):
    def construct(self):
        self.card()
        self.cheney()
        self.cost()

    def card(self):
        card = chapter_card(8, r"Cheney's copying collector, \ and what it costs", r"Can we touch only the living?",
                            lit=(1970,), extra=((1970, r"Cheney's copying collector"),), part=PART)
        with self.voiceover("Chapter eight. Cheney's copying collector, and what it costs."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def cheney(self):
        tr = load("tracing")["trace"]
        objs = tr["objects"]
        head = label(r"Two semispaces, \ two pointers \ (Cheney, \ 1970)", font_size=34).to_edge(UP, buff=0.3)
        W = 0.4

        def make(name):
            kind, f = objs[name]
            fs = [("p" if isinstance(x, str) and x in objs else ("·" if x is None else x)) for x in f]
            fs = [None if x == "·" else x for x in fs]
            o = cell_obj(kind, fs, w=W, h=0.42, font_size=13)
            o.name = mono(name, 14, GREY_B).next_to(o, UP, buff=0.06)
            return VGroup(o, o.name)
        frm = {n: make(n) for n in tr["from_order"]}
        frow = VGroup(*[frm[n] for n in tr["from_order"]]).arrange(RIGHT, buff=0.22).move_to(UP * 1.5)
        fl = label(r"from-space", font_size=20, color=GREY_B).next_to(frow, LEFT, buff=0.3)
        if fl.get_left()[0] < -7:
            VGroup(frow, fl).shift(RIGHT * (-6.9 - fl.get_left()[0]))
        root_ar = VGroup(*[Arrow(frm[r][0].get_top() + UP * 0.75, frm[r][0].get_top() + UP * 0.32, buff=0,
                                 color=CTRL, stroke_width=2.5, tip_length=0.12) for r in tr["roots"]])
        rl = label(r"roots", font_size=17, color=CTRL).next_to(root_ar[0], LEFT, buff=0.1)
        arcs = VGroup()
        for n in tr["from_order"]:
            for k, x in enumerate(objs[n][1]):
                if isinstance(x, str) and x in objs:
                    a = frm[n][0].dots[k].get_center()
                    b = frm[x][0].get_bottom()
                    arcs.add(CurvedArrow(a + DOWN * 0.05, b + DOWN * 0.02, angle=0.9 if b[0] > a[0] else -0.9,
                                         color=GREY_D, stroke_width=1.6, tip_length=0.1))
        # to-space slots
        to_y = -0.9
        to_objs = {}
        xs = frow.get_left()[0]
        tl = label(r"to-space", font_size=20, color=GREY_B).move_to([fl.get_center()[0], to_y, 0])
        base = Line([xs, to_y - 0.35, 0], [frow.get_right()[0], to_y - 0.35, 0], color=GREY_D, stroke_width=1.5)
        cur = xs

        def place(name):
            nonlocal cur
            o = make(name)
            o[0].move_to([cur + o[0].width / 2, to_y, 0])
            o[1].next_to(o[0], UP, buff=0.06)
            cur += o[0].width + 0.22
            to_objs[name] = o
            return o

        def fwd_box(name,index):
            r=Rectangle(width=frm[name][0].width,height=.42,stroke_color=HEAD,
                        stroke_width=1.6,fill_color=BG,fill_opacity=1)
            t=mono(f"FWD {3*index}",12,HEAD).move_to(r)
            return VGroup(r,t).move_to(frm[name][0])

        def ptr_mark(text, color, side):
            ar = Arrow(DOWN * 0.45, UP * 0.05, buff=0, color=color, stroke_width=3, tip_length=0.14)
            return VGroup(ar, label(text, font_size=17, color=color).next_to(ar, side, buff=0.08))
        scan = ptr_mark(r"scan", CTRL, LEFT)
        free = ptr_mark(r"free", YES, RIGHT)

        def at(m, x):
            return m.animate.shift(np.array([x, to_y - 0.95, 0]) - m[0].get_center())
        for marker in (scan, free):
            marker.shift(np.array([xs, to_y - 0.95, 0]) - marker[0].get_center())
        pts = VGroup(
            label(r"copy each root's object to to-space; \ leave a \textbf{forwarding address} behind",
                  font_size=20, color=GREY_A),
            label(r"then scan to-space left to right: \ copy what each field points at, \ unless already copied",
                  font_size=20, color=GREY_A),
            label(r"when \textit{scan} meets \textit{free}, \ everything live has been copied: \ swap the halves",
                  font_size=20, color=YES),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3)
        with self.voiceover("In 1970 C. J. Cheney found a collector that never looks at garbage at all. <bookmark mark='a'/> Split memory into two halves. The program allocates in one, from-space. Here a pair p holds a list of three cells; the roots point at p and at the middle cell; and three other objects are dead. <bookmark mark='b'/> To collect, copy each root's object into the empty half, to-space, and leave behind, in the old copy, a forwarding address: the new location. <bookmark mark='c'/> Now two pointers do all the work. Free marks the end of to-space. Scan walks through to-space, object by object. For every field that points into from-space, copy the target to free, unless it has already been forwarded, and update the field. <bookmark mark='d'/> When scan catches up with free, every live object has been copied, and nothing else has. The garbage was never touched. The halves swap roles, and the program continues in a heap that is perfectly compacted. Breadth-first, with no stack and no recursion: two pointers.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(frow), FadeIn(fl), Create(arcs), Create(root_ar), FadeIn(rl), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(tl), Create(base), FadeIn(scan), FadeIn(free), FadeIn(pts[0]))
            ev = tr['events']
            k = 0
            while ev[k][0] in ('copy', 'root'):
                e = ev[k]
                if e[0] == 'copy':
                    o = place(e[1])
                    self.play(TransformFromCopy(frm[e[1]], o), Transform(frm[e[1]][0], fwd_box(e[1], e[2])), at(free, cur), run_time=0.8)
                elif e[0] == 'root':
                    j = tr['roots'].index(e[1])
                    target = to_objs[e[1]][0]
                    arrow = Arrow(target.get_top() + UP * 0.75, target.get_top() + UP * 0.32, buff=0, color=CTRL, stroke_width=2.5, tip_length=0.12)
                    self.play(Transform(root_ar[j], arrow), run_time=0.35)
                k += 1
            self.play(rl.animate.next_to(root_ar, LEFT, buff=0.1), run_time=0.3)
            vo.wait_until('c')
            self.play(FadeIn(pts[1]))
            while ev[k][0] != 'done':
                e = ev[k]
                if e[0] == 'scan':
                    o = to_objs[e[1]]
                    self.play(at(scan, o[0].get_left()[0] + 0.05), Indicate(o[0], color=CTRL, scale_factor=1.05), run_time=0.6)
                elif e[0] == 'copy':
                    o = place(e[1])
                    self.play(TransformFromCopy(frm[e[1]], o), Transform(frm[e[1]][0], fwd_box(e[1], e[2])), at(free, cur), run_time=0.8)
                k += 1
            self.play(at(scan, cur), run_time=0.6)
            vo.wait_until('d')
            updated = VGroup()
            for name in tr['to_order']:
                for j, target in enumerate(objs[name][1]):
                    if isinstance(target, str) and target in to_objs:
                        start = to_objs[name][0].dots[j].get_center()
                        finish = to_objs[target][0].get_top() + UP * 0.02
                        updated.add(CurvedArrow(start + UP * 0.04, finish, angle=-0.65 if finish[0] > start[0] else 0.65, color=YES, stroke_width=1.7, tip_length=0.1))
            self.play(FadeIn(pts[2]), Create(updated), *[frm[n].animate.set_opacity(0.15) for n in tr['dead']])
        self.wait(0.3)
        self.clear_scene()

    def cost(self):
        d = load("cost")
        head = label(r"The cost: \ live data, \ not garbage", font_size=34).to_edge(UP, buff=0.3)
        rows = [r for r in d["rows"] if not r.get("oom") and r["collections"]]
        xmax = 400000
        ymax = max(max(r["work"],r["model"]) for r in rows) * 1.15
        ax = Axes(x_range=[0, xmax, 100000], y_range=[0, ymax, ymax / 4], x_length=7.0, y_length=4.0,
                  axis_config={"color": GREY_D, "include_numbers": False, "include_ticks": True}).move_to(
            LEFT * 2.4 + DOWN * 0.4)
        meas = VMobject(color=YES, stroke_width=3).set_points_as_corners(
            [ax.c2p(r["semispace"], r["work"]) for r in rows])
        dots = VGroup(*[Dot(ax.c2p(r["semispace"], r["work"]), radius=0.06, color=YES) for r in rows])
        model = VMobject(color=HEAD, stroke_width=2.5).set_points_as_corners(
            [ax.c2p(r["semispace"], r["model"]) for r in rows])
        model = DashedVMobject(model, num_dashes=40)
        xl = label(r"semispace size, \ words", font_size=18, color=GREY_B).next_to(ax, DOWN, buff=0.3)
        yl = label(r"words copied, \ in all", font_size=18, color=GREY_B).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        ticks = VGroup(*[label(f"{v // 1000}k", font_size=15, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                         for v in (100000, 200000, 300000, 400000)])
        yticks = VGroup(*[label(f"{v / 1000:.0f}k" if v else "0", font_size=14, color=GREY_B)
                           .next_to(ax.c2p(0, v), LEFT, buff=.12) for v in (0, ymax/4, ymax/2, 3*ymax/4, ymax)])
        live = rows[0]["mean_live"]
        side = VGroup(
            label('copying-only model: each collection copies $L$ live words', font_size=21, color=GREY_A),
            label(r"and buys $S - L$ words of allocation", font_size=21, color=GREY_A),
            MathTex(r"\text{work per word allocated} \;\approx\; \frac{L}{S - L}", font_size=32, color=HEAD),
            label(rf"measured: \ the Job, \ $L \approx$ {words(round(live, -2))} words", font_size=20, color=YES),
            label("dashed estimate: each run's sampled mean $L$", font_size=19, color=HEAD),
            label('excludes root scans and bookkeeping; finite runs have boundary effects', font_size=21, color=COST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.35)
        if side.width > 5.4:
            side.scale_to_fit_width(5.4)
        with self.voiceover(
            (
            "Count the words copied. <bookmark mark='a'/> A collection copies L live words and leaves S minus L "
            "words for new allocation in a semispace of size S. With a roughly stable live set, the copying work "
            "per allocated word is approximately L over S minus L. <bookmark mark='b'/> The solid curve measures "
            "the Job with different semispace sizes. Near the live set, collections are frequent. With more "
            "space, the finite run collects less often. <bookmark mark='c'/> The dashed estimate uses each run's "
            "mean sampled live set. Startup, end effects and changing liveness explain why it need not match "
            "exactly. <bookmark mark='d'/> This model counts copying, not root scans, allocation bookkeeping, or "
            "wall time. It explains a memory-versus-work trade within those assumptions; it is not a complete "
            "runtime cost theorem."
        )
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(ticks), FadeIn(yticks))
            vo.wait_until("a")
            self.play(FadeIn(side[:3]))
            vo.wait_until("b")
            self.play(Create(meas), FadeIn(dots), FadeIn(side[3]), run_time=2)
            vo.wait_until("c")
            self.play(Create(model), FadeIn(side[4]))
            vo.wait_until("d")
            self.play(FadeIn(side[5]))
        self.wait(0.3)
        self.clear_scene()
