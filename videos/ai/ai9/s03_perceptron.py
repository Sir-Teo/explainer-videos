from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai9.common import CLS_A, CLS_B, FWD, PART, WEIGHT, load, log_axes, two_tone

BOX = 2.3  # data units: the plot shows [-BOX, BOX]^2


def clip_line(w, L=BOX):
    """The segment of w1 x + w2 y + w0 = 0 inside the square [-L, L]^2 (None if it misses)."""
    w1, w2, w0 = w
    pts = []
    if abs(w2) > 1e-12:
        for x in (-L, L):
            y = -(w0 + w1 * x) / w2
            if -L - 1e-9 <= y <= L + 1e-9:
                pts.append((x, y))
    if abs(w1) > 1e-12:
        for y in (-L, L):
            x = -(w0 + w2 * y) / w1
            if -L - 1e-9 <= x <= L + 1e-9:
                pts.append((x, y))
    pts = sorted(set((round(a, 9), round(b, 9)) for a, b in pts))
    if len(pts) < 2:
        return None
    return pts[0], pts[-1]


class Perceptron(VoiceoverScene):
    def construct(self):
        self.card()
        self.rule()
        self.replay()
        self.proof()
        self.check()

    def card(self):
        card = chapter_card(2, r"The perceptron learns", r"Is learning from mistakes guaranteed to work?", lit=(1958,),
                            part=PART)
        with self.voiceover("Chapter two. The perceptron learns."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def plot(self, center, side=5.4):
        sq = Square(side, stroke_color=GREY_D, stroke_width=1.5).move_to(center)
        s = side / (2 * BOX)

        def P(x, y):
            return np.array(center) + np.array([x * s, y * s, 0])

        return sq, P

    def rule(self):
        c = [-3.4, -0.2, 0]
        sq, P = self.plot(c, side=5.2)
        w = np.array([1.0, 0.6, -0.3])
        seg = clip_line(w)
        line = Line(P(*seg[0]), P(*seg[1]), color=WEIGHT, stroke_width=4)
        foot = np.array([-w[2] * w[0], -w[2] * w[1]]) / (w[0] ** 2 + w[1] ** 2)
        warrow = Arrow(P(*foot), P(*(foot + 0.9 * w[:2] / np.linalg.norm(w[:2]))), buff=0, color=WEIGHT, stroke_width=5)
        wl = MathTex(r"w", font_size=34, color=WEIGHT).next_to(warrow.get_end(), UR, buff=0.05)
        x = np.array([-1.2, 1.5])  # a positive point on the wrong side (illustrative)
        xd = Dot(P(*x), radius=0.1, color=CLS_B)
        xl = MathTex(r"x, \ y = +1", font_size=28, color=CLS_B).next_to(xd, UP, buff=0.1)
        w2 = w + np.r_[x, 1.0] * 0.55
        seg2 = clip_line(w2)
        line2 = Line(P(*seg2[0]), P(*seg2[1]), color=WEIGHT, stroke_width=4)
        foot2 = np.array([-w2[2] * w2[0], -w2[2] * w2[1]]) / (w2[0] ** 2 + w2[1] ** 2)
        warrow2 = Arrow(P(*foot2), P(*(foot2 + 0.9 * w2[:2] / np.linalg.norm(w2[:2]))), buff=0, color=WEIGHT,
                        stroke_width=5)
        tag = note(r"illustrative").next_to(sq, DOWN, buff=0.15).align_to(sq, RIGHT)
        xs = np.linspace(-BOX, BOX, 160)
        G = np.stack(np.meshgrid(xs, xs), -1)
        tint = two_tone((G @ w[:2] + w[2]) > 0, 5.2, 5.2, strength=0.25).move_to(c)
        tint2 = two_tone((G @ w2[:2] + w2[2]) > 0, 5.2, 5.2, strength=0.25).move_to(c)
        u = w[:2] / np.linalg.norm(w[:2])
        sides = VGroup(MathTex(r"w \cdot x > 0", font_size=30, color=CLS_B).move_to(P(*(foot + 1.25 * u + [0.35, -0.6]))),
                       MathTex(r"w \cdot x < 0", font_size=30, color=CLS_A).move_to(P(*(foot - 1.15 * u + [0.2, -0.75]))))
        alg = theorem_card(r"The perceptron", VGroup(
            label(r"examples $x$ with labels $y = \pm 1$", font_size=28, color=GREY_A),
            label(r"predict $\operatorname{sign}(w \cdot x)$", font_size=28, color=GREY_A),
            label(r"on a mistake: \ $w \leftarrow w + y\,x$", font_size=30, color=WEIGHT),
            label(r"a constant input $1$ gives the line its bias", font_size=25, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2), who=r"F.~Rosenblatt (1958)", kind=r"Algorithm", width=6.4,
            color=WEIGHT).move_to([3.45, 1.0, 0])
        why_ = label(r"$y\,x$ turns $w$ toward a positive point, \\ away from a negative one", font_size=28,
                     color=GREY_A).move_to([3.45, -2.4, 0])
        with self.voiceover(
            "Here is Rosenblatt's learning rule, in modern notation. Each example is a point x with a label y, plus "
            "one or minus one. <bookmark mark='a'/> The perceptron predicts the sign of w dot x: which side of the "
            "line where w dot x is zero the point falls on. The weights w form an arrow at right angles to that line. "
            "<bookmark mark='b'/> When it gets an example wrong, it adds y times x to w. <bookmark mark='c'/> For a "
            "positive point on the wrong side, that turns the arrow toward the point, and the line swings to put the "
            "point on its side, or at least nearer to it. That's all there is. A constant input of one gives the line "
            "a bias, so it needn't pass through the middle."
        ) as vo:
            self.play(Create(sq), FadeIn(alg), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(tint), Create(line), GrowArrow(warrow), FadeIn(wl), FadeIn(sides))
            vo.wait_until("b")
            self.play(FadeIn(xd, scale=1.5), FadeIn(xl))
            self.play(Indicate(xd, color=C.SURPRISE))
            vo.wait_until("c")
            self.play(FadeOut(sides), FadeOut(tint), FadeIn(tint2), Transform(line, line2), Transform(warrow, warrow2),
                      wl.animate.next_to(warrow2.get_end(), UR, buff=0.05), FadeIn(why_), run_time=1.5)
            self.bring_to_front(line, warrow, wl, xd, xl)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        d = load("perceptron")
        X, y = np.asarray(d["X"]), np.asarray(d["y"])
        ws, who, pe = np.asarray(d["ws"]), [int(i) for i in d["who"]], [int(v) for v in d["per_epoch"]]
        k = len(who)
        c = [-3.0, -0.2, 0]
        sq, P = self.plot(c, side=5.6)
        dots = VGroup(*[Dot(P(*p), radius=0.07, color=CLS_B if v > 0 else CLS_A) for p, v in zip(X, y)])
        xs = np.linspace(-BOX, BOX, 160)
        G = np.stack(np.meshgrid(xs, xs), -1)

        def tint(w):
            return two_tone((G @ w[:2] + w[2]) > 0, 5.6, 5.6, strength=0.28).move_to(c)

        def seg(w):
            s_ = clip_line(w)
            return Line(P(*s_[0]), P(*s_[1]), color=WEIGHT, stroke_width=4)

        # the passes: which update belongs to which pass
        bounds = np.cumsum(pe)
        mv = Integer(0, font_size=40, color=C.SURPRISE)
        ml = VGroup(label(r"mistakes so far:", font_size=32, color=GREY_A), mv).arrange(RIGHT, buff=0.15)
        ml.move_to([3.4, 2.75, 0])
        # bars: mistakes in each pass, growing mistake by mistake
        n_pass = len(pe)
        bw, gap, bx, by = 0.6, 0.3, 1.0, -2.0
        base = Line([bx, by, 0], [bx + n_pass * (bw + gap) + gap, by, 0], color=GREY_C, stroke_width=1.5)
        unit = 3.4 / max(pe)

        def bar(i, v):
            h_ = max(v * unit, 0.02)
            return Rectangle(width=bw, height=h_, stroke_width=0, fill_color=C.SURPRISE, fill_opacity=0.85).move_to(
                [bx + gap + bw / 2 + i * (bw + gap), by + h_ / 2, 0])

        def bnum_(i, v):
            return MathTex(str(v), font_size=30, color=C.SURPRISE).next_to(bar(i, v), UP, buff=0.1)

        bars = VGroup(*[bar(i, 0) for i in range(n_pass)])
        bnum = VGroup(*[bnum_(i, 0) for i in range(n_pass)])
        blab = VGroup(*[MathTex(str(i + 1), font_size=28, color=GREY_B).next_to([b_.get_x(), by, 0], DOWN, buff=0.14)
                        for i, b_ in enumerate(bars)])
        bt = label(r"mistakes in each pass through the data", font_size=26, color=GREY_A).next_to(base, DOWN, buff=0.6)
        count = [0] * n_pass
        tag = note(rf"computed: \ ${len(X)}$ points, \ separable").next_to(sq, DOWN, buff=0.15)
        with self.voiceover(
            f"Here it is on {len(X)} points that some line can separate. It starts with all its weights at zero. "
            "<bookmark mark='a'/> Every time it meets a point on the wrong side, the line jumps. "
            f"<bookmark mark='b'/> In its first pass through the data it makes {pe[0]} mistakes, and {sum(pe[1:])} more in "
            f"the passes after that. <bookmark mark='c'/> After {k} mistakes in all, a whole pass goes by without one, and it stops: "
            "every point is on its own side."
        ) as vo:
            self.play(Create(sq), LaggedStart(*[FadeIn(dt_) for dt_ in dots], lag_ratio=0.02), FadeIn(ml), FadeIn(tag),
                      Create(base), FadeIn(bt))
            vo.wait_until("a")
            cur_t, cur_l = None, None
            shown = set()
            for j in range(k):
                i = who[j]
                p = int(np.searchsorted(bounds, j + 1, side="left"))  # the pass this mistake belongs to
                ring = Circle(radius=0.18, color=C.SURPRISE, stroke_width=4).move_to(dots[i])
                w = ws[j + 1]
                nt, nl = tint(w), seg(w)
                self.play(Create(ring), *([FadeIn(blab[p]), FadeIn(bars[p])] if p not in shown else []), run_time=0.25)
                shown.add(p)
                count[p] += 1
                anims = [FadeIn(nt), FadeIn(nl)] if cur_t is None else [FadeOut(cur_t), FadeIn(nt), Transform(cur_l, nl)]
                self.play(*anims, ChangeDecimalToValue(mv, j + 1), FadeOut(ring), Transform(bars[p], bar(p, count[p])),
                          Transform(bnum[p], bnum_(p, count[p])), *([FadeIn(bnum[p])] if count[p] == 1 else []),
                          run_time=0.55)
                if cur_l is None:
                    cur_l = nl
                cur_t = nt
                self.bring_to_front(dots, cur_l)
                if j == 1:
                    vo.wait_until("b")
            vo.wait_until("c")
            rest = [q for q in range(n_pass) if q not in shown]
            self.play(*[FadeIn(blab[q]) for q in rest], *[FadeIn(bnum[q]) for q in rest], run_time=0.4)
            self.play(Indicate(dots, color=WHITE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def proof(self):
        colors = {r"w^*": FWD, r"\gamma": C.BITS, r"R": C.MODEL_Q}
        rows = [
            cmath(r"w_{k+1} \cdot w^*", r"=", r"w_k \cdot w^* + y\, x \cdot w^*", r"\ \ge\ ", r"w_k \cdot w^* + \gamma",
                  font_size=32, colors=colors),
            cmath(r"w_k \cdot w^*", r"\ge", r"k\, \gamma", font_size=32, colors=colors),
            cmath(r"\|w_{k+1}\|^2", r"=", r"\|w_k\|^2 + 2\, y\, w_k \cdot x + \|x\|^2", r"\ \le\ ", r"\|w_k\|^2 + R^2",
                  font_size=32, colors=colors),
            cmath(r"\|w_k\|^2", r"\le", r"k\, R^2", font_size=32, colors=colors),
            cmath(r"k\, \gamma", r"\le", r"w_k \cdot w^* \ \le\ \|w_k\| \ \le\ \sqrt{k}\, R", font_size=32, colors=colors),
            cmath(r"k", r"\le", r"(R / \gamma)^2", font_size=36, colors=colors),
        ]
        whys = [why(r"a mistake adds $y\,x$; \ every point is $\ge \gamma$ from the best line"),
                why(r"$k$ mistakes, \ from $w_0 = 0$"),
                why(r"a mistake: \ $y\, w_k \cdot x \le 0$; \ $\|x\| \le R$"),
                why(r"$k$ mistakes"),
                why(r"Cauchy--Schwarz, \ $\|w^*\| = 1$"),
                why(r"square both ends, \ divide by $k\gamma^2$")]
        step = ladder(self, rows, whys, keep=4, top=2.2, x=-1.6, buff=0.5, edge=6.9)
        assume = label(r"suppose $\|x\| \le R$ for every point, and some unit vector $w^*$ puts every point on its side "
                       r"with room to spare: \ $y\, w^* \cdot x \ge \gamma$", font_size=24, color=GREY_A)
        assume.to_edge(UP, buff=0.3)
        # the assumptions, on the chapter's data: the radius R and the band of width gamma either side of w*'s line
        d = load("perceptron")
        X, yv, wst = np.asarray(d["X"]), np.asarray(d["y"]), np.asarray(d["wstar"])
        gam = float(d["gamma"])
        span, side, c = 3.0, 5.6, np.array([-3.3, -0.55, 0])

        def P(x_, y_):
            return c + np.array([x_, y_, 0]) * side / (2 * span)

        frame_ = Square(side, stroke_color=GREY_D, stroke_width=1.5).move_to(c)
        far = X[int(np.argmax(np.linalg.norm(X, axis=1)))]
        circ = Circle(radius=float(np.linalg.norm(far)) * side / (2 * span), color=C.MODEL_Q, stroke_width=3).move_to(P(0, 0))
        rad = Line(P(0, 0), P(*far), color=C.MODEL_Q, stroke_width=3)
        rl = MathTex(r"R", font_size=36, color=C.MODEL_Q).next_to(rad.get_center(), UL, buff=0.08)
        lo, hi = clip_line(wst - np.r_[0, 0, gam], span), clip_line(wst + np.r_[0, 0, gam], span)
        band = Polygon(P(*lo[0]), P(*lo[1]), P(*hi[1]), P(*hi[0]), stroke_width=0, fill_color=FWD, fill_opacity=0.22)
        mid = clip_line(wst, span)
        sep = Line(P(*mid[0]), P(*mid[1]), color=FWD, stroke_width=3.5)
        ft = -wst[2] * wst[:2] / (wst[:2] @ wst[:2])
        warr = Arrow(P(*ft), P(*(ft + 1.0 * wst[:2] / np.linalg.norm(wst[:2]))), buff=0, color=FWD, stroke_width=5)
        wsl = MathTex(r"w^*", font_size=34, color=FWD).next_to(warr.get_end(), RIGHT, buff=0.08)
        pdots = VGroup(*[Dot(P(*q), radius=0.06, color=CLS_B if v > 0 else CLS_A) for q, v in zip(X, yv)])
        tight = np.where(yv * (np.c_[X, np.ones(len(X))] @ wst) < gam * 1.0001)[0]
        rings = VGroup(*[Circle(radius=0.15, color=C.BITS, stroke_width=3).move_to(pdots[i]) for i in tight])
        gl = label(r"margin $\gamma$: \ the closest points", font_size=26, color=C.BITS)
        gl.next_to(frame_, RIGHT, buff=0.3).align_to(frame_, DOWN).shift(UP * 0.3)
        pnote = note(r"$R$ and $\gamma$ count the constant input $1$ too").next_to(frame_, DOWN, buff=0.12)
        pic = VGroup(frame_, band, sep, warr, wsl, circ, rad, rl, pdots, rings, gl, pnote)
        th = theorem_card(r"Perceptron convergence", r"if every $\|x\| \le R$ and some unit $w^*$ separates the data "
                          r"with margin $\gamma$, \ the perceptron makes at most $(R/\gamma)^2$ mistakes: \ in any order, "
                          r"\ however many passes", who=r"A.~B.~J.~Novikoff (1962)", width=8.4, color=FWD)
        with self.voiceover(
            "Is it guaranteed to stop? In 1962 Albert Novikoff proved that it is, whenever some line separates the "
            "data. <bookmark mark='p1'/> Suppose every point lies within a distance R of the origin, "
            "<bookmark mark='p2'/> and some unit vector w star puts every point on its side with room to spare, a "
            "margin gamma. <bookmark mark='a'/> Watch two numbers. First, w's "
            "agreement with w star. Each mistake adds y x, and y x dot w star is at least gamma. "
            "<bookmark mark='b'/> So after k mistakes, the agreement is at least k gamma: it grows in proportion to k. "
            "<bookmark mark='c'/> Second, w's length. A mistake means y times w dot x was not positive, so the middle "
            "term can't help: the squared length grows by at most R squared. <bookmark mark='d'/> After k mistakes, "
            "at most k R squared: the length grows only like the square root of k. <bookmark mark='e'/> But the "
            "agreement with a unit vector can never exceed the length. So k gamma is at most root k times R. "
            "<bookmark mark='f'/> Square both ends and divide: the number of mistakes is at most R over gamma, "
            "squared. Something that grows like k can't stay below something that grows like root k for long."
        ) as vo:
            self.play(Create(frame_), FadeIn(pdots))
            vo.wait_until("p1")
            self.play(FadeIn(assume), Create(circ), Create(rad), FadeIn(rl), FadeIn(pnote))
            vo.wait_until("p2")
            self.play(FadeIn(band), Create(sep), GrowArrow(warr), FadeIn(wsl))
            self.bring_to_front(pdots)
            self.play(LaggedStart(*[Create(r_) for r_ in rings], lag_ratio=0.2), FadeIn(gl))
            vo.wait_until("a")
            self.play(FadeOut(pic))
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            step(4)
            vo.wait_until("f")
            step(5)
            box = SurroundingRectangle(rows[5], color=FWD, buff=0.12, corner_radius=0.08)
            self.play(Create(box))
        self.play(*[FadeOut(m) for m in self.mobjects if m not in (rows[5], box)],
                  VGroup(rows[5], box).animate.move_to(UP * 2.2))
        with self.voiceover(
            "That's the perceptron convergence theorem. The bound doesn't depend on how many points there are, or "
            "the order they come in, only on how much room there is between the classes."
        ):
            self.play(FadeIn(th.move_to(DOWN * 0.4), shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def check(self):
        d = load("perceptron")
        R, gamma, k, bound = float(d["R"]), float(d["gamma"]), int(d["mistakes"]), float(d["bound"])
        sw = np.asarray(d["sweep"])  # margin, gamma, R, mean mistakes, max mistakes, bound
        lx, lm, lmax = np.log10(sw[:, 5]), np.log10(sw[:, 3]), np.log10(sw[:, 4])
        hi = math.ceil(lx.max() + 0.1)
        g = log_axes([1, hi], [0, hi], 5.6, 4.0, center=[2.8, -0.5, 0], xlabel=r"$(R/\gamma)^2$",
                     ylabel=r"mistakes before it stops", xticks=range(1, hi + 1), yticks=range(0, hi + 1))
        ax = g.ax
        diag = DashedLine(ax.c2p(1, 1), ax.c2p(hi, hi), color=FWD, stroke_width=3, dash_length=0.1)
        dl = label(r"the bound", font_size=22, color=FWD).next_to(ax.c2p(hi - 0.6, hi - 0.6), UL, buff=0.05)
        means = VGroup(*[Dot(ax.c2p(a, b), radius=0.08, color=C.SURPRISE) for a, b in zip(lx, lm)])
        maxes = VGroup(*[Line(ax.c2p(a, b) + LEFT * 0.1, ax.c2p(a, b) + RIGHT * 0.1, color=C.SURPRISE, stroke_width=3)
                         for a, b in zip(lx, lmax)])
        lg = legend([(C.SURPRISE, r"average of $20$ orders \ (dash: the worst)")], font_size=20)
        lg.next_to(ax, UP, buff=0.55).align_to(ax, LEFT)
        nums = VGroup(MathTex(rf"R = {R:.2f}", font_size=34, color=C.MODEL_Q),
                      MathTex(rf"\gamma = {gamma:.3f}", font_size=34, color=C.BITS),
                      MathTex(rf"(R/\gamma)^2 = {bound:.0f}", font_size=34, color=FWD),
                      label(rf"mistakes made: \ ${k}$", font_size=32, color=C.SURPRISE))
        nums.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-4.3, 0.8, 0])
        tag = note(r"computed: \ six data sets of $200$ points, \ smaller and smaller margins").to_corner(DR, buff=0.2)
        ours = Star(5, outer_radius=0.13, color=C.MODEL_Q, fill_opacity=1, stroke_width=0).move_to(
            ax.c2p(math.log10(bound), math.log10(k)))
        ol = label(rf"our ${len(np.asarray(d['X']))}$ points", font_size=22, color=C.MODEL_Q).next_to(ours, DR, buff=0.08)
        svm = label(r"it finds \textit{a} separating line, \ not the widest: \\ that is the support vector machine "
                    r"\ (Part 6)", font_size=24, color=GREY_A).move_to([-4.0, -2.4, 0])
        ratio = float(np.max(sw[:, 4] / sw[:, 5]))
        with self.voiceover(
            f"For our points, R is {R:.2f} and the best margin gamma is {gamma:.3f}, so the theorem allows "
            f"{bound:.0f} mistakes. It made {k}. <bookmark mark='a'/> Shrink the margin, data set by data set, and "
            "run the perceptron twenty times on each, in different orders. <bookmark mark='b'/> The bound always "
            f"holds, and it's pessimistic: the worst run uses at most {100 * ratio:.0f} percent of it. "
            "<bookmark mark='c'/> Two things the theorem doesn't promise. The line it finds is a separating line, "
            "not the one with the widest margin; finding that one is the support vector machine of Part 6. And if no "
            "line separates the data, the perceptron never stops."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.1) for m in nums], lag_ratio=0.3), FadeIn(g), Create(diag),
                      FadeIn(dl), run_time=2.0)
            self.play(FadeIn(ours, scale=1.5), FadeIn(ol))
            vo.wait_until("a")
            self.play(FadeIn(tag), ours.animate.set_opacity(0.5), ol.animate.set_opacity(0.5))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(m_, scale=1.5), FadeIn(x_)) for m_, x_ in zip(means, maxes)],
                                  lag_ratio=0.3), FadeIn(lg), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(svm))
        self.wait(0.3)
        self.clear_scene()
