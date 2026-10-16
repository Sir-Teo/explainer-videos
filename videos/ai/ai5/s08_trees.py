from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai5.common import AUSTEN, DICKENS, X_RANGE, Y_RANGE, load, page_dots, page_plane

NAMES = ("the", "not")


def mix(v):
    return interpolate_color(ManimColor(AUSTEN), ManimColor(DICKENS), float(v))


class Trees(VoiceoverScene):
    def construct(self):
        self.card()
        self.splits()
        self.depth()
        self.forest()
        self.boosting()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(7, r"Trees, forests, boosting", r"What if you just keep asking questions?", part=5)
        with self.voiceover("Chapter seven. Trees, and committees of trees."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

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
        l_tr = VMobject(color=GREY_A, stroke_width=3).set_points_as_corners([cax.c2p(x, v) for x, v in zip(xs, tr_acc)])
        l_te = VMobject(color=C.BITS, stroke_width=4).set_points_as_corners([cax.c2p(x, v) for x, v in zip(xs, te_acc)])
        d_te = VGroup(*[Dot(cax.c2p(x, v), radius=0.05, color=C.BITS) for x, v in zip(xs, te_acc)])
        xl = VGroup(*[MathTex(str(d) if d < 7 else r"\infty", font_size=22, color=GREY_B).next_to(cax.c2p(d, 0.7), DOWN, buff=0.1)
                      for d in xs])
        yl = VGroup(*[MathTex(rf"{int(100 * v)}\%", font_size=20, color=GREY_B).next_to(cax.c2p(1, v), LEFT, buff=0.1)
                      for v in (0.7, 0.8, 0.9, 1.0)])
        cn = label(r"depth of the tree", font_size=22, color=GREY_A).next_to(cax, DOWN, buff=0.45)
        key = VGroup(label(r"training pages", font_size=24, color=GREY_A), label(r"new pages", font_size=24, color=C.BITS))
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(cax, UP, buff=0.2).align_to(cax, LEFT)
        best = int(np.argmax(te_acc[:6])) + 1
        with self.voiceover(
            "Keep asking questions, and the boxes fit the training pages better and better. <bookmark mark='a'/> "
            f"But new pages tell a different story. They're best at depth {best}, {100 * te_acc[best - 1]:.0f} percent "
            f"right. <bookmark mark='b'/> Grown all the way down, the tree gets {100 * t['train_deep2']:.0f} percent of "
            f"its own pages right, and only {100 * t['acc_deep2']:.0f} percent of new ones."
        ) as vo:
            self.play(Create(ax), FadeIn(plane[1:]), FadeIn(dots), FadeIn(R[0]))
            self.bring_to_front(dots)
            self.play(Create(cax), FadeIn(xl), FadeIn(yl), FadeIn(cn), FadeIn(key))
            cur = R[0]
            for d in range(2, 7):
                self.play(FadeOut(cur), FadeIn(R[d - 1]), run_time=0.5)
                self.bring_to_front(dots)
                cur = R[d - 1]
            vo.wait_until("a")
            self.play(Create(l_tr), Create(l_te), FadeIn(d_te[:6]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeOut(cur), FadeIn(deep), FadeIn(d_te[6]))
            self.bring_to_front(dots)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def committee_axes(self, n, title):
        ax = Axes(x_range=[0, n, n // 4], y_range=[0.8, 1.0, 0.05], x_length=7.6, y_length=4.0, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-1.4, -0.6, 0])
        yl = VGroup(*[MathTex(rf"{int(round(100 * v))}\%", font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in (0.8, 0.85, 0.9, 0.95, 1.0)])
        xl = label(title, font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.25)
        return ax, yl, xl

    def forest(self):
        t = load("trees")
        fa = np.asarray(t["forest_acc"])
        n = len(fa)
        ax, yl, xl = self.committee_axes(n, r"trees in the forest \ (all $70$ rates)")
        curve = VMobject(color=C.INTERVAL, stroke_width=4).set_points_as_corners([ax.c2p(k + 1, v) for k, v in enumerate(fa)])
        one = DashedLine(ax.c2p(0, t["acc_tree70"]), ax.c2p(n, t["acc_tree70"]), color=GREY_B, stroke_width=2)
        ol = label(rf"one full tree: \ ${100 * t['acc_tree70']:.0f}\%$", font_size=24, color=GREY_A).next_to(one, DOWN, buff=0.08)
        ol.align_to(one, RIGHT)
        fl = label(rf"a forest of ${n}$: \ ${100 * fa[-1]:.1f}\%$", font_size=28, color=C.INTERVAL).move_to([4.6, 1.6, 0])
        how = label(r"each tree: \ a random resample of the pages, \\ a random few words at each question", font_size=24,
                    color=GREY_A).next_to(fl, DOWN, buff=0.3)
        # a row of little trees
        icons = VGroup()
        g = np.random.default_rng(4)
        for k in range(12):
            tri = Triangle(color=C.INTERVAL, fill_color=C.INTERVAL, fill_opacity=0.3 + 0.4 * g.random(), stroke_width=1.5)
            tri.scale(0.22).move_to([-5.6 + 0.62 * k, 2.85, 0])
            icons.add(VGroup(tri, Line(tri.get_bottom(), tri.get_bottom() + DOWN * 0.15, color=GREY_B, stroke_width=2)))
        cite_ = cite(r"L.~Breiman, \textit{Random Forests} (2001)", corner=DR)
        with self.voiceover(
            "One tree is fragile: change a few training pages, and a different tree grows. Leo Breiman's answer, in "
            "2001: grow hundreds. Give each a random resample of the pages, and only a random handful of words to "
            "choose from at each question, then let them vote. <bookmark mark='a'/> With all seventy rates, one full "
            f"tree gets {100 * t['acc_tree70']:.0f} percent of new pages right. <bookmark mark='b'/> A forest of two "
            f"hundred gets {100 * fa[-1]:.0f}."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(i, shift=UP * 0.1) for i in icons], lag_ratio=0.08), FadeIn(cite_), run_time=1.5)
            self.play(FadeIn(how))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(yl), FadeIn(xl), Create(one), FadeIn(ol))
            vo.wait_until("b")
            self.play(Create(curve), run_time=2.5, rate_func=linear)
            self.play(FadeIn(fl))
        self.wait(0.3)
        self.clear_scene()

    def boosting(self):
        t = load("trees")
        ba, bt = np.asarray(t["boost_acc"]), np.asarray(t["boost_train"])
        n = len(ba)
        ax, yl, xl = self.committee_axes(n, r"rounds of boosting: \ one small tree each")
        c_te = VMobject(color=C.BITS, stroke_width=4).set_points_as_corners([ax.c2p(k + 1, v) for k, v in enumerate(ba)])
        c_tr = VMobject(color=GREY_A, stroke_width=2.5).set_points_as_corners([ax.c2p(k + 1, v) for k, v in enumerate(bt)])
        key = VGroup(label(r"training pages", font_size=24, color=GREY_A), label(r"new pages", font_size=24, color=C.BITS))
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([4.1, 1.2, 0]).align_to([2.8, 0, 0], LEFT)
        f = cmath(r"F_{m+1}(x)", "=", r"F_m(x)", "+", r"\eta\, h_m(x)", font_size=36).move_to([4.4, 2.6, 0])
        fn = label(r"$h_m$: \ a small tree fitted to what $F_m$ still gets wrong", font_size=22, color=GREY_A)
        fn.next_to(f, DOWN, buff=0.15)
        res = label(rf"after ${n}$ rounds: \\ ${100 * ba[-1]:.0f}\%$ of new pages", font_size=28, color=C.BITS)
        res.next_to(key, DOWN, buff=0.5).align_to(key, LEFT)
        tables = label(r"on tables of numbers, \\ boosted trees are still hard to beat", font_size=24, color=GREY_A)
        tables.next_to(res, DOWN, buff=0.3).align_to(key, LEFT)
        cite_ = cite(r"J.~H.~Friedman, \textit{Greedy Function Approximation: A Gradient Boosting Machine} (2001)", corner=DR)
        with self.voiceover(
            "Boosting builds the committee another way: one small tree at a time, each trained on the mistakes of "
            "all the trees before it. <bookmark mark='a'/> The training pages are soon all right. The new pages "
            f"climb to {100 * ba[-1]:.0f} percent. <bookmark mark='b'/> On tables of numbers like these, boosted "
            "trees are still, today, among the hardest methods to beat."
        ) as vo:
            self.play(Write(f), FadeIn(fn), FadeIn(cite_))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(yl), FadeIn(xl), FadeIn(key))
            self.play(Create(c_tr), Create(c_te), run_time=3.0, rate_func=linear)
            self.play(FadeIn(res))
            vo.wait_until("b")
            self.play(FadeIn(tables))
        self.wait(0.3)
        self.clear_scene()
