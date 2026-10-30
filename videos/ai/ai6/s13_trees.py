from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai6.common import (AUSTEN, DICKENS, GOOD, HIST, HL, X_RANGE, Y_RANGE, chapter, load, mix, page_dots,
                                  page_plane, plot, side_ladder)

NAMES = ("the", "not")
GINI, ENT, ERRC = C.BITS, C.TRUE_P, C.PENALTY


class Trees(VoiceoverScene):
    def construct(self):
        chapter(self, 12, r"Trees: twenty questions", r"What if you just keep asking questions?",
                "Chapter twelve. Decision trees.")
        self.splits()
        self.impurity()
        self.depth()
        self.fragile()

    # ------------------------------------------------------------------
    def rects(self, ax, rects, opacity=0.5):
        g = VGroup()
        for x0, x1, y0, y1, v in rects:
            x0, x1 = max(x0, X_RANGE[0]), min(x1, X_RANGE[1])
            y0, y1 = max(y0, Y_RANGE[0]), min(y1, Y_RANGE[1])
            if x1 <= x0 or y1 <= y0:
                continue
            p0, p1 = ax.c2p(x0, y0), ax.c2p(x1, y1)
            g.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_color=WHITE, stroke_width=1.2,
                            fill_color=mix(v), fill_opacity=opacity).move_to((p0 + p1) / 2))
        return g

    def splits(self):
        p = load("pages")
        t = load("trees")
        X2, y, test = np.asarray(p["X2"]), np.asarray(p["y"]), np.asarray(p["test"], bool)
        plane = page_plane(x_length=6.6, y_length=4.6, center=[-3.4, -0.4, 0])
        ax = plane[0]
        tr = np.nonzero(~test)[0]
        dots = page_dots(ax, X2, y, idx=tr, jitter=0.35, radius=0.04, opacity=0.9)
        R = [self.rects(ax, t[f"rects{d}"]) for d in (1, 2, 3)]
        # the tree's diagram
        root = t["tree3"]
        levels = [2.7, 1.45, 0.2, -1.05]
        nodes, edges = VGroup(), VGroup()

        def draw(nd, depth, x, span, parent=None, side=""):
            pos = np.array([x, levels[depth], 0])
            if "leaf" in nd:
                m = VGroup(Square(0.36, stroke_width=1.5, stroke_color=WHITE, fill_color=mix(nd["leaf"]), fill_opacity=0.85)
                           .move_to(pos))
            else:
                txt = MathTex(rf"\text{{{NAMES[nd['j']]}}} \le {nd['t']:g}", font_size=24)
                box = RoundedRectangle(width=txt.width + 0.3, height=0.48, corner_radius=0.1, stroke_color=GREY_B,
                                       stroke_width=1.5, fill_color="#121722", fill_opacity=1).move_to(pos)
                m = VGroup(box, txt.move_to(pos))
            m.level = depth
            nodes.add(m)
            if parent is not None:
                e = Line(parent.get_bottom(), m.get_top(), color=GREY_C, stroke_width=1.8)
                e.level = depth
                e.add(Text(side, font="DejaVu Sans", font_size=14, color=GREY_B).move_to(e.get_center() + LEFT * 0.12
                                                                                      if side == "yes" else e.get_center() + RIGHT * 0.12))
                edges.add(e)
            if "leaf" not in nd:
                draw(nd["l"], depth + 1, x - span / 2, span / 2, m, "yes")
                draw(nd["r"], depth + 1, x + span / 2, span / 2, m, "no")

        draw(root, 0, 3.9, 2.8)
        by_depth = [VGroup(*[m for m in [*nodes, *edges] if m.level == k]) for k in range(4)]
        assert root["j"] == 1
        with self.voiceover(
            "A decision tree plays twenty questions. The first question it learned: does the page say 'not' at most "
            f"{root['t']:g} times per thousand words? <bookmark mark='a'/> Each answer splits the pages, and each "
            "group gets its own next question. <bookmark mark='b'/> Every question cuts the plane with a straight "
            "line, parallel to an axis, so the plane becomes boxes, and each box votes by its majority."
        ) as vo:
            self.play(Create(ax), FadeIn(plane[1:]), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.003),
                      FadeIn(by_depth[0]), run_time=2.0)
            self.play(FadeIn(R[0]))
            self.bring_to_front(dots)
            vo.wait_until("a")
            self.play(FadeIn(by_depth[1]), FadeOut(R[0]), FadeIn(R[1]))
            self.bring_to_front(dots)
            vo.wait_until("b")
            self.play(FadeIn(by_depth[2]), FadeOut(R[1]), FadeIn(R[2]))
            self.bring_to_front(dots)
            self.play(FadeIn(by_depth[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def depth(self):
        p = load("pages")
        t = load("trees")
        X2, y, test = np.asarray(p["X2"]), np.asarray(p["y"]), np.asarray(p["test"], bool)
        plane = page_plane(x_length=6.6, y_length=4.6, center=[-3.4, -0.4, 0])
        ax = plane[0]
        tr = np.nonzero(~test)[0]
        dots = page_dots(ax, X2, y, idx=tr, jitter=0.35, radius=0.04, opacity=0.9)
        deep = self.rects(ax, t["rects_deep"], opacity=0.55)
        R = [self.rects(ax, t[f"rects{d}"]) for d in range(1, 7)]
        cax = Axes(x_range=[1, 7, 1], y_range=[0.7, 1.0, 0.1], x_length=5.0, y_length=3.4, tips=False,
                   axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([3.7, -0.2, 0])
        xs = list(range(1, 7)) + [7]
        tr_acc = [t[f"train{d}"] for d in range(1, 7)] + [t["train_deep2"]]
        te_acc = [t[f"acc{d}"] for d in range(1, 7)] + [t["acc_deep2"]]
        # the training score grows with the tree, one depth at a time; the new pages' score is revealed after
        s_tr = [Line(cax.c2p(xs[k], tr_acc[k]), cax.c2p(xs[k + 1], tr_acc[k + 1]), color=GREY_A, stroke_width=3)
                for k in range(6)]
        d_tr = VGroup(*[Dot(cax.c2p(x, v), radius=0.045, color=GREY_A) for x, v in zip(xs, tr_acc)])
        l_te = VMobject(color=C.BITS, stroke_width=4).set_points_as_corners([cax.c2p(x, v) for x, v in zip(xs[:6], te_acc[:6])])
        l_te7 = Line(cax.c2p(xs[5], te_acc[5]), cax.c2p(xs[6], te_acc[6]), color=C.BITS, stroke_width=4)
        d_te = VGroup(*[Dot(cax.c2p(x, v), radius=0.05, color=C.BITS) for x, v in zip(xs, te_acc)])
        dv = ValueTracker(1)
        dl = always_redraw(lambda: label(rf"depth ${int(round(dv.get_value()))}$", font_size=28, color=WHITE)
                           .next_to(ax, UP, buff=0.15).align_to(ax, RIGHT))
        xl = VGroup(*[MathTex(str(d) if d < 7 else r"\infty", font_size=22, color=GREY_B).next_to(cax.c2p(d, 0.7), DOWN, buff=0.1)
                      for d in xs])
        yl = VGroup(*[MathTex(rf"{int(100 * v)}\%", font_size=20, color=GREY_B).next_to(cax.c2p(1, v), LEFT, buff=0.1)
                      for v in (0.7, 0.8, 0.9, 1.0)])
        cn = label(r"depth of the tree", font_size=22, color=GREY_A).next_to(cax, DOWN, buff=0.45)
        key = VGroup(label(r"training pages", font_size=24, color=GREY_A), label(r"new pages", font_size=24, color=C.BITS))
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(cax, UP, buff=0.2).align_to(cax, LEFT)
        best = int(np.argmax(te_acc[:6])) + 1
        cvm = np.asarray(t["cv"])
        cvd = int(np.argmax(cvm[:6])) + 1
        cart = note(r"L.~Breiman, J.~Friedman, R.~Olshen \& C.~Stone, \textit{Classification and Regression Trees} (1984)"
                    ).to_corner(DR, buff=0.2)
        with self.voiceover(
            "Keep asking questions, and the boxes fit the training pages better and better. <bookmark mark='a'/> "
            f"But new pages tell a different story. They're best at depth {best}, {100 * te_acc[best - 1]:.0f} percent "
            f"right. <bookmark mark='b'/> Grown all the way down, the tree gets {100 * t['train_deep2']:.0f} percent of "
            f"its own pages right, and only {100 * t['acc_deep2']:.0f} percent of new ones. "
            f"<bookmark mark='c'/> Cross-validation on the training pages, without peeking, picks depth {cvd}. "
            "Breiman, Friedman, Olshen and Stone's CART, in 1984, grew trees deep and pruned them back the same way."
        ) as vo:
            self.play(Create(ax), FadeIn(plane[1:]), FadeIn(dots), FadeIn(R[0]))
            self.bring_to_front(dots)
            self.play(Create(cax), FadeIn(xl), FadeIn(yl), FadeIn(cn), FadeIn(key), FadeIn(d_tr[0]), FadeIn(dl))
            cur = R[0]
            for d in range(2, 7):
                self.play(FadeOut(cur), FadeIn(R[d - 1]), Create(s_tr[d - 2]), FadeIn(d_tr[d - 1]),
                          dv.animate.set_value(d), run_time=0.7)
                self.bring_to_front(dots)
                cur = R[d - 1]
            vo.wait_until("a")
            self.play(Create(l_te), FadeIn(d_te[:6]), run_time=1.5)
            vo.wait_until("b")
            dl.clear_updaters()
            self.play(FadeOut(cur), FadeIn(deep), Create(s_tr[5]), FadeIn(d_tr[6]), Create(l_te7), FadeIn(d_te[6]),
                      Transform(dl, label(r"depth $\infty$", font_size=28, color=WHITE).move_to(dl, aligned_edge=RIGHT)))
            self.bring_to_front(dots)
            vo.wait_until("c")
            self.play(Create(DashedLine(cax.c2p(cvd, 0.7), cax.c2p(cvd, 1.0), color=GOOD, stroke_width=2)), FadeIn(cart))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def impurity(self):
        t = load("trees")
        g = plot([0, 1, 0.5], [0, 1.05, 0.5], x_length=4.0, y_length=2.3, xticks=[0, 0.5, 1], yticks=[0, 0.5, 1],
                 center=[-4.4, 1.75, 0], xlabel=r"share of Dickens in a box, \ $p$", ylabel=r"impurity")
        ax = g.ax
        p = np.linspace(0.001, 0.999, 200)
        cg = curve(ax, p, 2 * p * (1 - p), GINI, stroke_width=4, smooth=True)
        ce = curve(ax, p, -(p * np.log2(p) + (1 - p) * np.log2(1 - p)), ENT, stroke_width=4, smooth=True)
        cr = VMobject(color=ERRC, stroke_width=4).set_points_as_corners([ax.c2p(0, 0), ax.c2p(0.5, 0.5), ax.c2p(1, 0)])
        key = VGroup(label(r"Gini: \ $2p(1-p)$", font_size=22, color=GINI),
                     label(r"entropy: \ $H(p)$ \ (Part 1)", font_size=22, color=ENT),
                     label(r"error rate: \ $\min(p, 1-p)$", font_size=22, color=ERRC)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        key.next_to(g, RIGHT, buff=0.25).align_to(g, UP)
        colors = {r"i": GINI}
        rows = [
            cmath(r"\Delta", "=", r"i(p) - \tfrac{n_L}{n}\, i(p_L) - \tfrac{n_R}{n}\, i(p_R)", font_size=30),
            cmath(r"p", "=", r"\tfrac{n_L}{n}\, p_L + \tfrac{n_R}{n}\, p_R", font_size=30),
            cmath(r"\Delta", r"\ \ge\ ", r"0, \ \text{equality only if } p_L = p_R", font_size=30),
        ]
        whys = [why(r"what a question gains", font_size=20), why(r"the parent averages its children", font_size=20),
                why(r"Jensen: \ $i$ strictly concave", font_size=20)]
        step = side_ladder(self, rows, whys, 3.4, 3.3, keep=3, top=3.2, buff=0.4)
        th = np.asarray(t["scan_not_t"])
        sc = plot([float(th.min()), float(th.max()), 4], [0, 1.05, 0.5], x_length=6.0, y_length=1.9,
                  xticks=[4, 8, 12, 16], yticks=[0, 1], center=[-2.4, -2.45, 0],
                  xlabel=r"threshold on ``not'' \ (per $1{,}000$ words)", ylabel=r"gain, \ scaled to its best")
        sa = sc.ax
        scans = VGroup()
        best = {}
        for kind, col in (("gini", GINI), ("entropy", ENT), ("error", ERRC)):
            v = np.asarray(t[f"scan_not_{kind}"])
            scans.add(curve(sa, th, v / v.max(), col, stroke_width=3))
            best[kind] = float(th[int(np.argmax(v))])
        agree = len(set(best.values())) == 1
        bl = DashedLine(sa.c2p(best["gini"], 0), sa.c2p(best["gini"], 1.05), color=WHITE, stroke_width=2)
        res = label(rf"best question: \ ``not'' $\le {best['gini']:g}$", font_size=24, color=WHITE).move_to([3.9, -1.6, 0])
        flat = label(r"the error rate is flat over long stretches: \\ many useful questions score the same",
                     font_size=20, color=ERRC).next_to(res, DOWN, buff=0.2)
        keep_in_frame(flat)
        say = (f"On the pages, all three agree on the first question: 'not' at most {best['gini']:g} times per thousand. "
               if agree else
               f"On the pages, Gini picks 'not' at most {best['gini']:g}; entropy {best['entropy']:g}; the error rate "
               f"{best['error']:g}. ")
        with self.voiceover(
            "How does the tree choose its question? It measures how mixed each box is. <bookmark mark='a'/> Three "
            "measures of impurity: Gini's, the entropy from Part 1, and the plain error rate. <bookmark mark='b'/> A "
            "question's gain is the parent's impurity minus its children's, weighted by size. <bookmark mark='c'/> "
            "The parent's share of Dickens is the average of its children's, <bookmark mark='d'/> so if the impurity "
            "curves strictly downward, Jensen's inequality makes every gain positive whenever the children differ. "
            "The error rate is only a tent, flat on each side: a split that purifies both children can gain nothing "
            "by it. <bookmark mark='e'/> Scan every threshold. "
            + say
        ) as vo:
            self.play(FadeIn(g))
            self.play(Create(cg), Create(ce), Create(cr), FadeIn(key))
            vo.wait_until("a")
            self.play(Indicate(key, color=WHITE, scale_factor=1.05))
            vo.wait_until("b")
            step(0)
            vo.wait_until("c")
            step(1)
            vo.wait_until("d")
            step(2)
            vo.wait_until("e")
            self.play(FadeIn(sc), Create(scans), run_time=1.5)
            self.play(Create(bl), FadeIn(res), FadeIn(flat))
        self.wait(0.3)
        self.clear_scene()


    # ------------------------------------------------------------------
    def fragile(self):
        t = load("trees")
        roots = t["boot_roots"]
        acc = np.asarray(t["boot_acc"])
        words = sorted({r[0] for r in roots}, key=lambda w: -sum(r[0] == w for r in roots))
        pal = [C.BITS, C.TRUE_P, C.REWARD, C.PENALTY, C.MODEL_Q]
        col = {w: pal[i % len(pal)] for i, w in enumerate(words)}
        icons = VGroup()
        for k, (w, thr, lw, rw) in enumerate(roots):
            top = RoundedRectangle(width=1.15, height=0.4, corner_radius=0.08, stroke_color=col[w], stroke_width=2,
                                   fill_color="#121722", fill_opacity=1)
            tt = label(rf"\texttt{{{w}}} $\le {thr:g}$", font_size=16, color=col[w]).move_to(top)
            kids = VGroup(*[label(rf"\texttt{{{c_}}}" if c_ else r"$\cdot$", font_size=14, color=GREY_A) for c_ in (lw, rw)])
            kids.arrange(RIGHT, buff=0.4).next_to(top, DOWN, buff=0.22)
            edges = VGroup(*[Line(top.get_bottom(), kd.get_top(), color=GREY_C, stroke_width=1.2) for kd in kids])
            icons.add(VGroup(top, tt, edges, kids))
        icons.arrange_in_grid(rows=4, cols=5, buff=(0.3, 0.3)).move_to([-2.1, -0.3, 0])
        counts = VGroup(*[label(rf"\texttt{{{w}}} \ first: \ ${sum(r[0] == w for r in roots)}$ of ${len(roots)}$",
                                font_size=24, color=col[w]) for w in words])
        counts.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.6, 1.2, 0])
        accl = label(rf"held-out pages: \ ${100 * acc.min():.0f}\%$ to ${100 * acc.max():.0f}\%$", font_size=24,
                     color=WHITE).next_to(counts, DOWN, buff=0.4).align_to(counts, LEFT)
        head = label(rf"The same recipe on ${len(roots)}$ resamples of the training pages \ (all $70$ rates, \ depth $3$)",
                     font_size=28).to_edge(UP, buff=0.3)
        n1 = sum(r[0] == words[0] for r in roots)
        with self.voiceover(
            "One more weakness. Grow the same small tree on resamples of the training pages, drawn with "
            f"replacement, {len(roots)} times. <bookmark mark='a'/> The first question changes: {len(words)} different "
            f"words come first, '{words[0]}' most often, in {n1} of the {len(roots)} trees. "
            "Below it, the trees disagree even more. <bookmark mark='b'/> And on the held-out pages they score "
            f"anywhere from {100 * acc.min():.0f} to {100 * acc.max():.0f} percent. A tree is a high-variance "
            "learner, and the next chapter turns that weakness into a strength."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(i_, scale=0.9) for i_ in icons], lag_ratio=0.08), run_time=3.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in counts], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(accl))
        self.wait(0.3)
        self.clear_scene()
