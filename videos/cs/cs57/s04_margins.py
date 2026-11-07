from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs57.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, bar_chart, code_block, load


def stacked(rows, whys, buff=0.2):
    """Derivation rows, each with its reason underneath in grey."""
    pairs = VGroup()
    for r, w in zip(rows, whys):
        w.next_to(r, DOWN, buff=0.08, aligned_edge=LEFT)
        pairs.add(VGroup(r, w))
    pairs.arrange(DOWN, aligned_edge=LEFT, buff=buff)
    return pairs


def toy_data(n=34, gamma=0.16, angle=0.35, seed=7):
    """Illustrative separable points in the unit disk with margin gamma about the line normal to w*."""
    rng = np.random.default_rng(seed)
    ws = np.array([math.cos(angle), math.sin(angle)])
    X = []
    while len(X) < n:
        x = rng.uniform(-1, 1, 2)
        if np.linalg.norm(x) <= 0.97 and abs(x @ ws) >= gamma:
            X.append(x)
    X = np.array(X)
    return X, np.sign(X @ ws), ws


def perceptron_path(X, y, cap=40):
    """The weight vectors after each mistake, cycling through the data until a clean pass."""
    w = np.zeros(2)
    path = []
    for _ in range(50):
        clean = True
        for i, (x, t) in enumerate(zip(X, y)):
            if t * (w @ x) <= 0:
                w = w + t * x
                path.append((i, w.copy()))
                clean = False
        if clean or len(path) >= cap:
            break
    return path


class Margins(VoiceoverScene):
    def construct(self):
        self.card()
        self.perceptron()
        self.proof()
        self.dims()
        self.rademacher()
        self.linear()

    def card(self):
        card = chapter_card(3, r"Margins and Rademacher complexity",
                            r"Why does the margin matter more than the dimension?", lit=(1958, 1962),
                            extra=((1958, r"Rosenblatt's perceptron"), (1962, r"Novikoff's mistake bound")),
                            part=PART)
        with self.voiceover("Chapter three. Margins and Rademacher complexity."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def perceptron(self):
        head = label(r"The perceptron, \ and its margin", font_size=36).to_edge(UP, buff=0.3)
        X, y, ws = toy_data()
        gamma = 0.16
        S = 2.55
        c0 = np.array([-3.5, -0.4, 0])

        def P(v):
            return c0 + np.array([v[0] * S, v[1] * S, 0])
        disk = Circle(radius=S, color=GREY_D, stroke_width=1.5).move_to(c0)
        rl = label(r"$\|x\| \le R$", font_size=18, color=GREY_B).next_to(disk, UP, buff=0.08).shift(LEFT * 1.8)
        perp = np.array([-ws[1], ws[0]])
        sep = DashedLine(P(-perp), P(perp), color=YES, stroke_width=2)
        band = VGroup(*[Line(P(-perp * 0.95 + s * gamma * ws), P(perp * 0.95 + s * gamma * ws), color=YES,
                             stroke_width=1, stroke_opacity=0.5) for s in (-1, 1)])
        bandf = Polygon(P(-perp * 0.95 - gamma * ws), P(perp * 0.95 - gamma * ws), P(perp * 0.95 + gamma * ws),
                        P(-perp * 0.95 + gamma * ws), stroke_width=0, fill_color=YES, fill_opacity=0.1)
        glab = label(r"margin $\gamma$", font_size=18, color=YES).next_to(P(-perp * 0.95 + gamma * ws), DOWN,
                                                                         buff=0.1)
        dots = VGroup(*[Dot(P(x), radius=0.065, color=DATA if t > 0 else NO) for x, t in zip(X, y)])
        path = perceptron_path(X, y)

        def wline(w):
            u = w / np.linalg.norm(w)
            q = np.array([-u[1], u[0]])
            return VGroup(Line(P(-q), P(q), color=HEAD, stroke_width=3),
                          Arrow(c0, P(0.55 * u), buff=0, color=HEAD, stroke_width=3,
                                max_tip_length_to_length_ratio=0.2))
        code = code_block(["w = 0", "for each example (x, y):", "    if y * (w . x) <= 0:     # a mistake",
                           "        w = w + y * x"], size=17)
        code.move_to([3.3, 1.6, 0])
        W = 5.8
        side = VGroup(
            wrapped_label(r"Rosenblatt \ (1958): \ predict the sign of $w \cdot x$; \ on a mistake, \ add the "
                          r"example to $w$, \ with its sign", W, font_size=19, color=WHITE),
            wrapped_label(r"if some unit vector $w^*$ separates the data with margin $\gamma$, \ "
                          r"$y_i\, w^* \cdot x_i \ge \gamma$, \ and every $\|x_i\| \le R$: \ the perceptron makes at "
                          r"most $(R/\gamma)^2$ mistakes, \ ever \ (Novikoff 1962)", W, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(code, DOWN, buff=0.5).align_to(code, LEFT)
        ill = note(r"illustrative points", font_size=16).next_to(disk, DOWN, buff=0.12).align_to(disk, LEFT)
        with self.voiceover(
            "The oldest learning machine is the one Part 7 put inside a processor. <bookmark mark='a'/> "
            "Frank Rosenblatt's perceptron, from 1958, predicts with the sign of a weighted sum. When it is"
            " wrong, it adds the example, with its sign, to the weights; otherwise it does nothing. "
            "<bookmark mark='b'/> Watch it on points that some line separates. Each mistake swings the "
            "yellow line, until no point is on the wrong side. <bookmark mark='c'/> What controls the "
            "number of mistakes? Not the number of points, and not the dimension, but the margin: the width"
            " of the empty band around the best separator, against the radius of the data. "
            "<bookmark mark='d'/> Albert Novikoff proved in 1962 that the perceptron makes at most R over "
            "gamma, squared, mistakes, however long it runs."
        ) as vo:
            self.play(FadeIn(head), Create(disk), FadeIn(rl), FadeIn(dots), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(code), FadeIn(side[0]))
            vo.wait_until("b")
            cur = wline(path[0][1])
            self.play(Indicate(dots[path[0][0]], color=WHITE, scale_factor=2.0), FadeIn(cur), run_time=0.6)
            for i, w in path[1:12]:
                self.play(Indicate(dots[i], color=WHITE, scale_factor=2.0), Transform(cur, wline(w)), run_time=0.55)
            if len(path) > 12:
                self.play(Transform(cur, wline(path[-1][1])), run_time=0.6)
            vo.wait_until("c")
            self.play(FadeIn(bandf), Create(sep), Create(band), FadeIn(glab))
            vo.wait_until("d")
            self.play(FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()

    def proof(self):
        rows_ = load("perceptron")["rows"]
        gamma = rows_[0]["gamma"]
        bound = round(rows_[0]["bound"])
        head = label(r"Novikoff's proof: \ two inequalities", font_size=36).to_edge(UP, buff=0.3)
        hyp = MathTex(r"\|x_i\| \le R, \qquad \|w^*\| = 1, \qquad y_i\, w^* \cdot x_i \ge \gamma", font_size=28,
                      color=GREY_A)
        fs = 27
        rows = [
            MathTex(r"w_{k+1} \cdot w^*", r"=", r"w_k \cdot w^* + y\, x \cdot w^*", r"\ge", r"w_k \cdot w^* + \gamma",
                    font_size=fs),
            MathTex(r"\|w_{k+1}\|^2", r"=", r"\|w_k\|^2 + 2y\, w_k \cdot x + \|x\|^2", r"\le", r"\|w_k\|^2 + R^2",
                    font_size=fs),
            MathTex(r"k\gamma", r"\le", r"w_k \cdot w^*", r"\le", r"\|w_k\|", r"\le", r"\sqrt{k}\,R", font_size=fs + 2),
            MathTex(r"k", r"\le", r"\Big(\frac{R}{\gamma}\Big)^2", font_size=fs + 6),
        ]
        rows[2][0].set_color(DATA)
        rows[2][6].set_color(KERN)
        rows[3][2].set_color(YES)
        whys = [
            label(r"a mistake adds $y x$, \ and $y\, w^* \cdot x \ge \gamma$: \ after $k$ mistakes, "
                  r"$w_k \cdot w^* \ge k\gamma$", font_size=17, color=GREY_B),
            label(r"on a mistake $y\, w_k \cdot x \le 0$: \ after $k$ mistakes, \ $\|w_k\|^2 \le kR^2$",
                  font_size=17, color=GREY_B),
            label(r"Cauchy--Schwarz, \ since $\|w^*\| = 1$", font_size=17, color=GREY_B),
            label(r"divide by $\sqrt{k}\,\gamma$ and square", font_size=17, color=YES),
        ]
        col = stacked(rows, whys, buff=0.3)
        left = VGroup(hyp, col).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.4)
        left.to_edge(LEFT, buff=0.4)
        # the two growth rates: k gamma against sqrt(k) R, crossing at (R/gamma)^2
        kmax = 1.5 * bound
        ax = CornerAxes(x_range=[0, kmax, 50], y_range=[0, 16, 4], x_length=4.6, y_length=3.8, tips=False,
                        axis_config={"color": GREY_D, "include_numbers": False, "include_ticks": False})
        ax.move_to([4.4, 0.0, 0])
        xt = VGroup(*[label(f"{v}", font_size=16, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                      for v in (0, bound)])
        xl = label(r"mistakes $k$", font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.4)
        lin = ax.plot(lambda k: gamma * k, x_range=[0, kmax], color=DATA, stroke_width=3)
        sq = ax.plot(lambda k: math.sqrt(k), x_range=[0, kmax], color=KERN, stroke_width=3)
        ll = label(r"$k\gamma$: \ progress toward $w^*$", font_size=17, color=DATA).next_to(
            ax.c2p(kmax, gamma * kmax), LEFT, buff=0.1).shift(UP * 0.3)
        sl = label(r"$\sqrt{k}\,R$: \ length", font_size=17, color=KERN).next_to(ax.c2p(kmax, math.sqrt(kmax)),
                                                                                DOWN, buff=0.15).shift(LEFT * 0.4)
        imp = Polygon(*[ax.c2p(k, gamma * k) for k in np.linspace(bound, kmax, 12)],
                      *[ax.c2p(k, math.sqrt(k)) for k in np.linspace(kmax, bound, 12)], stroke_width=0,
                      fill_color=NO, fill_opacity=0.3)
        vline = DashedLine(ax.c2p(bound, 0), ax.c2p(bound, gamma * bound), color=YES, stroke_width=2)
        cap = label(rf"$R = 1$, \ $\gamma = {gamma:g}$: \ at most {bound} mistakes", font_size=18,
                    color=YES).next_to(ax, UP, buff=0.2)
        with self.voiceover(
            "The proof watches two quantities. Assume every example has length at most R, and a unit vector"
            " w star separates them with margin gamma. <bookmark mark='a'/> First, progress. A mistake adds"
            " y x, whose projection on w star is at least gamma, so after k mistakes the projection is at "
            "least k gamma: linear growth. <bookmark mark='b'/> Second, length. The squared length grows by"
            " twice y w dot x, which is not positive on a mistake, plus at most R squared. So after k "
            "mistakes the length is at most root k times R: square-root growth. <bookmark mark='c'/> A "
            "projection never exceeds a length. <bookmark mark='d'/> So k gamma is at most root k R, and k "
            "is at most R over gamma, squared. <bookmark mark='e'/> A line cannot stay under a square root "
            "for long: with radius one and margin a tenth, a hundred mistakes at most."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hyp))
            vo.wait_until("a")
            self.play(Write(col[0][0]), FadeIn(col[0][1]))
            self.play(Create(ax), FadeIn(xl), Create(lin), FadeIn(ll))
            vo.wait_until("b")
            self.play(Write(col[1][0]), FadeIn(col[1][1]))
            self.play(Create(sq), FadeIn(sl))
            vo.wait_until("c")
            self.play(Write(col[2][0]), FadeIn(col[2][1]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[2].copy(), rows[3]), FadeIn(col[3][1]))
            vo.wait_until("e")
            self.play(FadeIn(imp), Create(vline), FadeIn(xt), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    def dims(self):
        rows = load("perceptron")["rows"]
        bound = rows[0]["bound"]
        head = label(r"Mistakes do not grow with the dimension", font_size=36).to_edge(UP, buff=0.3)
        chart = bar_chart([r["mistakes"] for r in rows], [rf"$d = {r['d']:,}$" for r in rows],
                          [DATA, DATA, DATA, DATA], height=3.6, bar_w=0.9, gap=0.8, vmax=bound * 1.08,
                          fmt_=lambda v: f"{v:.0f}", font_size=20)
        chart.to_edge(LEFT, buff=1.0)
        chart.shift(UP * (-1.9 - chart.bars[0].get_bottom()[1]))
        base = chart.bars[0].get_bottom()[1]
        top = base + 3.6 / 1.08
        bl = DashedLine([chart.get_left()[0] - 0.2, top, 0], [chart.get_right()[0] + 0.2, top, 0], color=YES,
                        stroke_width=2)
        bll = label(rf"Novikoff: \ $(R/\gamma)^2 = {bound:.0f}$", font_size=19, color=YES).next_to(bl, UP, buff=0.1)
        yl = label(r"mistakes until a clean pass", font_size=17, color=GREY_A).next_to(chart, DOWN, buff=0.15)
        src = note(r"2{,}000 points on the unit sphere with margin $\gamma = 0.1$ about a random $w^*$, \ cycled until "
                   r"no mistake", font_size=16).to_edge(DOWN, buff=0.3)
        W = 5.0
        side = VGroup(
            wrapped_label(r"the bound has no $d$ in it: \ a thousand dimensions cost no more than ten", W,
                          font_size=19, color=WHITE),
            wrapped_label(r"the VC dimension of half-spaces is $d + 1$, \ so a VC bound grows with $d$; \ the "
                          r"margin bound does not", W, font_size=19, color=HEAD),
            wrapped_label(r"Part 7's branch predictor \ (Jim\'enez and Lin, \ 2001) \ runs this update in "
                          r"silicon; \ branch histories are rarely separable, \ so there the bound does not apply "
                          r"and only the mistake rate can be measured", W, font_size=19, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(chart, RIGHT, buff=0.9)
        side.set_y(0.1)
        if side.get_right()[0] > 6.85:
            side.shift(LEFT * (side.get_right()[0] - 6.85))
        with self.voiceover(
            "Our instrument tested the claim. <bookmark mark='a'/> It placed two thousand points on the "
            "unit sphere, all at least a tenth from a random hyperplane, in two, ten, a hundred and a "
            "thousand dimensions, and ran the perceptron to a clean pass. <bookmark mark='b'/> The mistakes"
            " were four, twenty-three, thirty-eight and thirty-four: all under Novikoff's hundred, and flat"
            " from a hundred dimensions to a thousand. <bookmark mark='c'/> A VC bound for half-spaces "
            "grows with the dimension; the margin bound sees only the geometry. <bookmark mark='d'/> Part "
            "7's branch predictor runs this update in hardware, but branch histories are rarely separable, "
            "so there the guarantee does not hold, and only the mistake rate can be measured."
        ) as vo:
            self.play(FadeIn(head), FadeIn(chart.names), FadeIn(chart[0]), FadeIn(yl), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(bl), FadeIn(bll))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in chart.bars], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(v) for v in chart.vals], lag_ratio=0.3), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def rademacher(self):
        head = label(r"Rademacher complexity: \ how well can a class fit noise?", font_size=36).to_edge(UP, buff=0.3)
        defn = MathTex(r"\hat{\mathfrak R}_S(\mathcal H)", r"=", r"\mathbb E_{\sigma}\Big[\,\sup_{h \in \mathcal H}\ "
                       r"\frac{1}{m}\sum_{i=1}^{m} \sigma_i\, h(x_i)\Big]", font_size=34)
        defn[0].set_color(HEAD)
        defn.next_to(head, DOWN, buff=0.35)
        dnote = label(r"$\sigma_i = \pm 1$ fair coins: \ random labels", font_size=18, color=GREY_B).next_to(
            defn, DOWN, buff=0.12)
        # illustrative: ten points on a line, three draws of coins, the best threshold for each
        m = 10
        rng = np.random.default_rng(3)
        draws = [rng.choice([-1, 1], m) for _ in range(3)]
        xs = np.arange(m)

        def best_threshold(s):
            best = (-2.0, 0.0, 1)
            for th in np.arange(-0.5, m, 1.0):
                for sg in (1, -1):
                    h = np.where(xs > th, sg, -sg)
                    v = float((s * h).mean())
                    if v > best[0]:
                        best = (v, th, sg)
            return best
        x0, dx, yb = -6.3, 0.42, -0.6
        panels = VGroup()
        for k, s in enumerate(draws):
            y = yb - k * 1.0
            pts = VGroup(*[Dot([x0 + i * dx, y, 0], radius=0.09, color=YES if v > 0 else NO) for i, v in enumerate(s)])
            v, th, sg = best_threshold(s)
            xt = x0 + (th + 0.5) * dx - dx / 2
            step = VMobject(color=HEAD, stroke_width=3).set_points_as_corners([
                [x0 - 0.3, y + 0.3 * -sg, 0], [xt, y + 0.3 * -sg, 0], [xt, y + 0.3 * sg, 0],
                [x0 + (m - 1) * dx + 0.3, y + 0.3 * sg, 0]])
            val = label(rf"best threshold: \ $\frac{{1}}{{m}}\sum \sigma_i h(x_i) = {v:.1f}$", font_size=18,
                        color=HEAD).next_to([x0 + (m - 1) * dx + 0.3, y, 0], RIGHT, buff=0.3)
            panels.add(VGroup(pts, step, val))
        ill = note(r"illustrative: \ thresholds on ten points", font_size=16).next_to(panels, DOWN, buff=0.15)
        ill.align_to(panels, LEFT)
        W = 5.6
        side = VGroup(
            wrapped_label(r"a class that shatters the points scores $1$ on every draw; \ a simple class cannot "
                          r"follow the noise", W, font_size=19, color=WHITE),
            MathTex(r"L_D(h) \le L_S(h) + 2\,\mathfrak R_m(\ell \circ \mathcal H) + \sqrt{\frac{\ln(1/\delta)}{2m}}",
                    font_size=28, color=YES),
            wrapped_label(r"for every $h$ at once, \ with probability $\ge 1 - \delta$ \ (Bartlett and Mendelson, "
                          r"\ 2002); \ and $\mathfrak R_m(\mathcal H) \le \sqrt{2 \ln \Pi_{\mathcal H}(m) / m}$ "
                          r"\ (Massart), \ so VC bounds follow", W, font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.9, -1.55, 0])
        if side.get_right()[0] > 6.85:
            side.shift(LEFT * (side.get_right()[0] - 6.85))
        with self.voiceover(
            "Margins need a complexity measure that is not a count. Rademacher complexity asks how well the"
            " class can fit pure noise. <bookmark mark='a'/> Flip a fair coin for each sample point to get "
            "random labels, find the hypothesis that agrees with them best, and average that agreement over"
            " the coins. <bookmark mark='b'/> For thresholds on a line, the best threshold catches only "
            "part of each draw's noise. <bookmark mark='c'/> A class that shatters the sample matches every"
            " draw perfectly; it can explain anything, so its fit to real data proves nothing. "
            "<bookmark mark='d'/> The theorem, in the form of Peter Bartlett and Shahar Mendelson in 2002: "
            "with probability one minus delta, every hypothesis's true error is at most its sample error, "
            "plus twice the Rademacher complexity, plus a term of order one over root m. "
            "<bookmark mark='e'/> Massart's lemma bounds the complexity by the growth function, so the VC "
            "bounds follow; with margins it can be far smaller."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(defn), FadeIn(dnote))
            vo.wait_until("b")
            for p in panels:
                self.play(LaggedStart(*[FadeIn(d_, scale=1.5) for d_ in p[0]], lag_ratio=0.08), run_time=1.0)
                self.play(Create(p[1]), FadeIn(p[2]), run_time=0.8)
            self.play(FadeIn(ill))
            vo.wait_until("c")
            self.play(FadeIn(side[0]))
            vo.wait_until("d")
            self.play(Write(side[1]))
            vo.wait_until("e")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def linear(self):
        head = label(r"For linear classes, \ no dimension at all", font_size=36).to_edge(UP, buff=0.3)
        fs = 28
        L = r"\hat{\mathfrak R}_S"
        rows = [
            MathTex(L, r"=", r"\frac{1}{m}", r"\mathbb E_\sigma\Big[\sup_{\|w\| \le \Lambda} w \cdot \sum_i \sigma_i "
                    r"x_i\Big]", font_size=fs),
            MathTex(L, r"=", r"\frac{\Lambda}{m}", r"\mathbb E_\sigma \Big\|\sum_i \sigma_i x_i\Big\|", font_size=fs),
            MathTex(L, r"\le", r"\frac{\Lambda}{m}", r"\sqrt{\mathbb E_\sigma \Big\|\sum_i \sigma_i x_i\Big\|^2}",
                    font_size=fs),
            MathTex(L, r"=", r"\frac{\Lambda}{m}", r"\sqrt{\sum_i \|x_i\|^2}", font_size=fs),
            MathTex(L, r"\le", r"\frac{\Lambda R}{\sqrt{m}}", font_size=fs + 2),
        ]
        rows[4][2].set_color(YES)
        whys = [
            label(r"linear hypotheses $x \mapsto w \cdot x$ with $\|w\| \le \Lambda$", font_size=17, color=GREY_B),
            label(r"Cauchy--Schwarz, \ equality when $w$ points along $\sum_i \sigma_i x_i$", font_size=17,
                  color=GREY_B),
            label(r"Jensen: \ $\mathbb E Z \le \sqrt{\mathbb E Z^2}$", font_size=17, color=GREY_B),
            label(r"expand the square: \ $\mathbb E\,\sigma_i \sigma_j = 0$ for $i \ne j$", font_size=17,
                  color=GREY_B),
            label(r"each $\|x_i\| \le R$", font_size=17, color=GREY_B),
        ]
        col = stacked(rows, whys, buff=0.2).next_to(head, DOWN, buff=0.35).to_edge(LEFT, buff=0.45)
        W = 5.6
        mb = MathTex(r"L_D(h) \le \hat L_S^{\rho}(h) + \frac{2\Lambda R}{\rho\sqrt{m}} + "
                     r"\sqrt{\frac{\ln(1/\delta)}{2m}}", font_size=30, color=HEAD)
        side = VGroup(
            wrapped_label(r"the \textbf{margin bound} \ (Koltchinskii and Panchenko, \ 2002): \ "
                          r"$\hat L_S^{\rho}$ counts sample points with margin $y\, w \cdot x \le \rho$", W,
                          font_size=19, color=WHITE),
            mb,
            wrapped_label(r"with $\Lambda = 1$ the complexity term is $2\sqrt{(R/\rho)^2 / m}$: \ $(R/\rho)^2$ plays "
                          r"the part of a dimension, \ exactly Novikoff's quantity", W, font_size=19, color=YES),
            wrapped_label(r"support vector machines \ (Cortes and Vapnik, \ 1995) \ maximize $\rho$; \ boosting, \ "
                          r"next, \ turns out to as well", W, font_size=19, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(col, RIGHT, buff=0.6).align_to(col, UP)
        if side.get_right()[0] > 6.85:
            side.shift(LEFT * (side.get_right()[0] - 6.85))
        with self.voiceover(
            "For linear classifiers with bounded weights, the Rademacher complexity takes five lines. "
            "<bookmark mark='a'/> The supremum over weights of length at most lambda, of w dotted with the "
            "sum of signed points, <bookmark mark='b'/> is lambda times the length of that sum, by Cauchy "
            "and Schwarz. <bookmark mark='c'/> Jensen's inequality moves the expectation inside a square "
            "root. <bookmark mark='d'/> Expanding the square, the cross terms vanish, because independent "
            "signs are uncorrelated, <bookmark mark='e'/> and what remains is lambda R over root m. The "
            "dimension never appears. <bookmark mark='f'/> Vladimir Koltchinskii and Dmitry Panchenko made "
            "this a margin bound in 2002: true error is at most the fraction of sample points with margin "
            "below rho, plus a term in R over rho, over root m. <bookmark mark='g'/> R over rho, squared, "
            "plays the part of a dimension: exactly Novikoff's quantity. <bookmark mark='h'/> Support "
            "vector machines, from Corinna Cortes and Vapnik in 1995, maximize that margin directly. "
            "Boosting, as we will see next, does too."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(col[0][0]), FadeIn(col[0][1]))
            for k, mk in enumerate("bcde"):
                vo.wait_until(mk)
                self.play(TransformMatchingTex(rows[k].copy(), rows[k + 1]), FadeIn(col[k + 1][1]))
            vo.wait_until("f")
            self.play(FadeIn(side[0]), Write(side[1]))
            vo.wait_until("g")
            self.play(FadeIn(side[2]))
            vo.wait_until("h")
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, LAM)
