from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs57.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load, mono


def stacked(rows, whys, buff=0.2):
    """Derivation rows, each with its reason underneath in grey, as one left-aligned column."""
    pairs = VGroup()
    for r, w in zip(rows, whys):
        w.next_to(r, DOWN, buff=0.08, aligned_edge=LEFT)
        pairs.add(VGroup(r, w))
    pairs.arrange(DOWN, aligned_edge=LEFT, buff=buff)
    return pairs


def curve_axes(xr, yr, xl, yl, xticks, yticks, x_length=5.2, y_length=3.4, fx=lambda v: f"{v:g}",
               fy=lambda v: f"{v:g}"):
    ax = CornerAxes(x_range=xr, y_range=yr, x_length=x_length, y_length=y_length, tips=False,
                    axis_config={"color": GREY_D, "include_numbers": False, "include_ticks": False})
    xt = VGroup(*[label(fx(v), font_size=16, color=GREY_B).next_to(ax.c2p(v, yr[0]), DOWN, buff=0.1)
                  for v in xticks])
    yt = VGroup(*[label(fy(v), font_size=16, color=GREY_B).next_to(ax.c2p(xr[0], v), LEFT, buff=0.1)
                  for v in yticks])
    lx = label(xl, font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.4) if xl else VectorizedPoint()
    ly = label(yl, font_size=17, color=GREY_A).next_to(ax, UP, buff=0.08).align_to(ax, LEFT) if yl else VectorizedPoint()
    return VGroup(ax, xt, yt, lx, ly), ax


def polyline(ax, xs, ys, color, width=2.5):
    return VMobject(color=color, stroke_width=width).set_points_as_corners([ax.c2p(x, v) for x, v in zip(xs, ys)])


def fit_x(g, lo=-6.85, hi=6.85):
    if g.get_right()[0] > hi:
        g.shift(LEFT * (g.get_right()[0] - hi))
    if g.get_left()[0] < lo:
        g.shift(RIGHT * (lo - g.get_left()[0]))
    return g


def beta_pdf(x, a, b):
    if x <= 0 or x >= 1:
        return 0.0
    return math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + (a - 1) * math.log(x)
                    + (b - 1) * math.log(1 - x))


ARM = [YES, DATA, LAM, KERN]


class Bandits(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.ucb()
        self.ucb_proof()
        self.thompson()
        self.curves()
        self.lower()

    def card(self):
        card = chapter_card(6, r"Bandits", r"How do you learn while you earn?", lit=(1933, 1952, 1985, 2002),
                            extra=((1933, r"Thompson: \ sampling"), (1952, r"Robbins: \ the bandit problem"),
                                   (1985, r"Lai and Robbins: \ the lower bound"), (2002, r"Auer et al.: \ UCB1")),
                            part=PART)
        with self.voiceover("Chapter six. Bandits."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ the problem
    def problem(self):
        b = load("bandits")
        mu = b["means"]
        best = max(mu)
        head = label(r"Explore or exploit", font_size=36).to_edge(UP, buff=0.3)
        machines = VGroup()
        for i, m in enumerate(mu):
            box = RoundedRectangle(width=1.2, height=3.0, corner_radius=0.12, stroke_color=ARM[i], stroke_width=2,
                                   fill_color=BG, fill_opacity=1)
            q = label(r"?", font_size=40, color=ARM[i]).move_to(box)
            name = label(rf"arm {i + 1}", font_size=18, color=ARM[i]).next_to(box, DOWN, buff=0.12)
            machines.add(VGroup(box, q, name))
        machines.arrange(RIGHT, buff=0.35).next_to(head, DOWN, buff=0.55).to_edge(LEFT, buff=0.6)
        fills = VGroup()
        mlabs = VGroup()
        for i, m in enumerate(mu):
            box = machines[i][0]
            h = 2.75 * m / 0.6
            r = Rectangle(width=0.8, height=h, stroke_width=0, fill_color=ARM[i], fill_opacity=0.6)
            r.align_to(box, DOWN).shift(UP * 0.1).set_x(box.get_x())
            fills.add(r)
            mlabs.add(label(rf"$\mu_{i + 1} = {m:g}$", font_size=18, color=ARM[i]).next_to(r, UP, buff=0.08))
        mcap = wrapped_label(r"each pull pays 1 with the arm's hidden probability $\mu_i$; \ we see only what we "
                             r"pull", 5.6, font_size=18, color=GREY_A).next_to(machines, DOWN, buff=0.25)
        mcap.align_to(machines, LEFT)
        ab = wrapped_label(r"Part 44's A/B test explores evenly for a fixed time, \ then commits: \ every pull of a "
                           r"worse arm in the test adds to the regret", 5.6, font_size=18, color=KERN).next_to(
            mcap, DOWN, buff=0.3).align_to(machines, LEFT)
        fs = 27
        gaps = [best - m for m in mu if m < best]
        rows = [
            MathTex(r"R_T", r"=", r"T\mu^* - \mathbb E\sum_{t=1}^T \mu_{a_t}", font_size=fs),
            MathTex(r"R_T", r"=", r"\sum_i \Delta_i\, \mathbb E\big[n_i(T)\big]", r",\qquad",
                    r"\Delta_i = \mu^* - \mu_i", font_size=fs),
            MathTex(r"\Delta", r"=", ", ".join(f"{g:.2f}" for g in gaps), font_size=fs, color=HEAD),
        ]
        whys = [
            label(r"what knowing the best arm would earn, \ minus what we earn", font_size=17, color=GREY_B),
            label(r"group the rounds by arm; \ $n_i(T)$: \ the pulls of arm $i$", font_size=17, color=GREY_B),
            label(r"our arms' gaps: \ pull the bad ones rarely, \ but never not at all", font_size=17, color=GREY_B),
        ]
        col = stacked(rows, whys, buff=0.3).move_to([3.6, 0.5, 0])
        fit_x(col)
        with self.voiceover(
            "Herbert Robbins posed this problem in 1952. <bookmark mark='a'/> A row of slot machines, each paying out"
            " with its own hidden probability. Each round we pull one arm and see only its reward. To find the best "
            "arm we must explore; to earn, we must exploit. <bookmark mark='b'/> The measure is regret: what always "
            "pulling the best arm would earn, minus what we earn. <bookmark mark='c'/> Grouped by arm, it is each "
            "arm's gap times how often we pull it. <bookmark mark='d'/> Our four arms pay a half, point four five, "
            "point four and point three. <bookmark mark='e'/> Part 44's A/B test explores evenly for a fixed time, "
            "then commits, paying for every pull of a worse arm. A bandit algorithm adapts as it goes."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in machines], lag_ratio=0.15),
                      FadeIn(mcap))
            vo.wait_until("a")
            self.play(LaggedStart(*[Indicate(m[0], color=WHITE) for m in machines], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(Write(col[0][0]), FadeIn(col[0][1]))
            vo.wait_until("c")
            self.play(Write(col[1][0]), FadeIn(col[1][1]))
            vo.wait_until("d")
            self.play(*[FadeOut(m[1]) for m in machines], *[GrowFromEdge(f, DOWN) for f in fills],
                      FadeIn(mlabs), Write(col[2][0]), FadeIn(col[2][1]))
            vo.wait_until("e")
            self.play(FadeIn(ab))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ UCB, the idea
    def ucb(self):
        b = load("bandits")
        mu = np.array(b["means"])
        K = len(mu)
        head = label(r"Optimism: \ upper confidence bounds", font_size=36).to_edge(UP, buff=0.3)
        T = 400
        rng = np.random.default_rng(2)
        n = np.zeros(K)
        s = np.zeros(K)
        hist = {}
        for t in range(T):
            if t < K:
                i = t
            else:
                i = int(np.argmax(s / n + np.sqrt(2 * math.log(t + 1) / n)))
            s[i] += float(rng.random() < mu[i])
            n[i] += 1
            hist[t + 1] = (n.copy(), s.copy(), i)
        g, ax = curve_axes([0, K + 1, 1], [0, 1.6, 0.5], None, r"estimate $\hat\mu_i$ \ and index $\hat\mu_i + "
                           r"\sqrt{2\ln t / n_i}$", [], [0, 0.5, 1, 1.5], x_length=5.4, y_length=4.0)
        g.next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.9)
        names = VGroup(*[label(rf"arm {i + 1}", font_size=17, color=ARM[i]).next_to(ax.c2p(i + 1, 0), DOWN,
                                                                                   buff=0.12) for i in range(K)])
        truth = VGroup(*[Line(ax.c2p(i + 1 - 0.3, mu[i]), ax.c2p(i + 1 + 0.3, mu[i]), color=GREY_B,
                              stroke_width=1.5) for i in range(K)])
        tl = label(r"grey ticks: \ the true $\mu_i$", font_size=16, color=GREY_B)

        def state(t):
            n_, s_, i_ = hist[t]
            grp = VGroup()
            for k in range(K):
                m = s_[k] / n_[k]
                u = min(1.6, m + math.sqrt(2 * math.log(t + 1) / n_[k]))
                bar = Line(ax.c2p(k + 1, m), ax.c2p(k + 1, u), color=ARM[k], stroke_width=7)
                d = Dot(ax.c2p(k + 1, m), radius=0.07, color=WHITE)
                cnt = label(rf"$n = {int(n_[k])}$", font_size=16, color=GREY_A).next_to(names[k], DOWN, buff=0.06)
                grp.add(VGroup(bar, d, cnt))
            hl = SurroundingRectangle(grp[i_][0], color=HEAD, buff=0.08, stroke_width=2.5)
            tt = label(rf"$t = {t}$", font_size=20, color=HEAD).next_to(ax.c2p(0.3, 1.6), DOWN, buff=0.05,
                                                                         aligned_edge=LEFT)
            return VGroup(grp, hl, tt)
        ill = note(r"illustrative run on our four arms", font_size=16).next_to(names, DOWN, buff=0.4).align_to(g, LEFT)
        tl.next_to(ill, RIGHT, buff=0.4)
        fs = 27
        rows = [
            MathTex(r"\mathrm{UCB}_i(t)", r"=", r"\hat\mu_i + \sqrt{\frac{2 \ln t}{n_i}}", font_size=fs),
            MathTex(r"\Pr\big[\mu_i > \hat\mu_i + \epsilon\big]", r"\le", r"e^{-2 n_i \epsilon^2}", font_size=fs),
            MathTex(r"\Pr\big[\mu_i > \mathrm{UCB}_i(t)\big]", r"\le", r"t^{-4}", font_size=fs),
        ]
        rows[0][2].set_color(HEAD)
        whys = [
            label(r"pull the arm whose plausible best case is highest", font_size=17, color=GREY_B),
            label(r"Hoeffding \ (Part 20), \ after $n_i$ pulls", font_size=17, color=GREY_B),
            label(r"put $\epsilon = \sqrt{2\ln t / n_i}$: \ the index is rarely below the truth", font_size=17,
                  color=GREY_B),
        ]
        col = stacked(rows, whys, buff=0.35).next_to(g, RIGHT, buff=0.7).align_to(g, UP).shift(DOWN * 0.2)
        fit_x(col)
        foot = wrapped_label(r"a bad arm's bar shrinks as it is pulled, \ until it no longer reaches the best arm's: "
                             r"\ then it is pulled only as often as $\ln t$ grows", col.width, font_size=18,
                             color=YES).next_to(col, DOWN, buff=0.4).align_to(col, LEFT)
        with self.voiceover(
            "The first strategy is optimism. <bookmark mark='a'/> For each arm keep the average reward, plus a bonus "
            "that shrinks as the arm is pulled: the root of two log t over its pull count. Pull the arm whose index, "
            "its plausible best case, is highest. <bookmark mark='b'/> By Hoeffding, the true mean exceeds the "
            "average by epsilon with probability at most e to the minus two n epsilon squared. <bookmark mark='c'/> "
            "With this bonus, the index falls below the truth with probability at most t to the minus four. "
            "<bookmark mark='d'/> Watch an illustrative run. The bad arms' bars shrink as they are tried, until they "
            "no longer reach the best arm's; after that they are tried only as often as log t grows."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(names), FadeIn(ill))
            vo.wait_until("a")
            self.play(Write(col[0][0]), FadeIn(col[0][1]))
            vo.wait_until("b")
            self.play(Write(col[1][0]), FadeIn(col[1][1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(col[2][1]))
            vo.wait_until("d")
            cur = state(K)
            self.play(FadeIn(cur), Create(truth), FadeIn(tl))
            for t in list(range(K + 1, 26)) + [40, 60, 100, 150, 200, 300, 400]:
                self.play(Transform(cur, state(t)), run_time=0.22 if t < 26 else 0.6)
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ UCB, the regret bound
    def ucb_proof(self):
        b = load("bandits")
        mu, T = b["means"], b["T"]
        best = max(mu)
        gaps = [best - m for m in mu if m < best]
        bound = sum(8 * math.log(T) / g for g in gaps) + (1 + math.pi ** 2 / 3) * sum(gaps)
        meas = b["final"]["UCB1"]
        head = label(r"Why UCB's regret grows like $\ln T$", font_size=36).to_edge(UP, buff=0.3)
        # the picture: one bad arm's interval against the best mean
        g = VGroup()
        ln_ = NumberLine(x_range=[0.25, 0.75, 0.1], length=5.0, rotation=PI / 2, color=GREY_D, include_ticks=False)
        ln_.move_to([-4.7, 0.0, 0])
        P = ln_.n2p
        mi, ms, w = 0.40, 0.62, 0.11
        mhat = mi + 0.06
        g.add(ln_)
        m_i = VGroup(Line(P(mi) + LEFT * 0.25, P(mi) + RIGHT * 0.25, color=LAM, stroke_width=3),
                     label(r"$\mu_i$", font_size=24, color=LAM).next_to(P(mi) + RIGHT * 0.25, RIGHT, buff=0.1))
        m_s = VGroup(DashedLine(P(ms) + LEFT * 0.6, P(ms) + RIGHT * 1.9, color=YES, stroke_width=2.5),
                     label(r"$\mu^*$", font_size=24, color=YES).next_to(P(ms) + RIGHT * 1.9, RIGHT, buff=0.1))
        hat = VGroup(Dot(P(mhat) + RIGHT * 0.9, radius=0.07, color=WHITE),
                     label(r"$\hat\mu_i \le \mu_i + w$", font_size=21, color=WHITE).next_to(P(mhat) + RIGHT * 0.9,
                                                                                          RIGHT, buff=0.15))
        bar = Line(P(mhat) + RIGHT * 0.9, P(mhat + w) + RIGHT * 0.9, color=LAM, stroke_width=7)
        ucb = label(r"$\mathrm{UCB}_i = \hat\mu_i + w \le \mu_i + 2w$", font_size=21, color=LAM).next_to(
            P(mhat + w) + RIGHT * 0.9, RIGHT, buff=0.15)
        brace = BraceBetweenPoints(P(mi) + LEFT * 0.3, P(ms) + LEFT * 0.3, direction=LEFT, color=HEAD)
        bl = label(r"$\Delta_i$", font_size=24, color=HEAD).next_to(brace, LEFT, buff=0.1)
        pic_note = wrapped_label(r"$w = \sqrt{2\ln t / n_i}$; \ arm $i$ is pulled only if its index reaches the best "
                                 r"arm's, \ which is above $\mu^*$", 4.6, font_size=17, color=GREY_A)
        pic_note.next_to(ln_, DOWN, buff=0.3).align_to(bl, LEFT)
        fs = 26
        rows = [
            MathTex(r"\text{pull } i", r"\Rightarrow", r"\mu_i + 2\sqrt{\frac{2\ln t}{n_i}} \ge \mu^*", font_size=fs),
            MathTex(r"n_i", r"\le", r"\frac{8 \ln T}{\Delta_i^2}", font_size=fs),
            MathTex(r"R_T", r"\le", r"\sum_{i:\,\Delta_i > 0} \frac{8\ln T}{\Delta_i} + \Big(1 + \frac{\pi^2}{3}\Big)"
                    r"\sum_i \Delta_i", font_size=fs),
            MathTex(r"R_T", r"\le", rf"{bound:,.0f}".replace(",", "{,}"), r"\quad\text{against}\quad",
                    rf"{meas:.0f}\ \text{{measured}}", font_size=fs),
        ]
        rows[2][2].set_color(YES)
        rows[3][2].set_color(YES)
        rows[3][4].set_color(DATA)
        whys = [
            label(r"unless one of the $t^{-4}$ failures happened", font_size=17, color=GREY_B),
            label(r"solve for $n_i$: \ after that many pulls the bar is too short", font_size=17, color=GREY_B),
            label(r"times $\Delta_i$, \ summed; \ the failures add a constant \ (Auer, \ Cesa-Bianchi and Fischer "
                  r"2002)", font_size=17, color=GREY_B),
            label(rf"our arms, \ $T = {T:,}$: \ true, \ but loose; \ the shape, \ $\ln T$, \ is the point"
                  .replace(",", "{,}"), font_size=17, color=GREY_B),
        ]
        col = stacked(rows[:3], whys[:3], buff=0.3).move_to([2.9, 0.3, 0])
        fit_x(col)
        tail = VGroup(rows[3], whys[3])
        whys[3].next_to(rows[3], DOWN, buff=0.08, aligned_edge=LEFT)
        tail.next_to(col, DOWN, buff=0.3).align_to(col, LEFT)
        with self.voiceover(
            "Peter Auer, Nicolò Cesa-Bianchi and Paul Fischer proved in 2002 that this index, UCB1, has regret "
            "growing only like log T. <bookmark mark='a'/> Picture a bad arm, a gap delta below the best. "
            "<bookmark mark='b'/> Its average is at most w above its mean, and its index adds another w. "
            "<bookmark mark='c'/> If we pull it, its index beat the best arm's, which is above mu star. So mu i plus "
            "two w reaches mu star, barring a rare failure. <bookmark mark='d'/> Solve: at most eight log T over "
            "delta squared pulls. <bookmark mark='e'/> Multiply by the gaps and add a constant for the failures. "
            "<bookmark mark='f'/> For our arms over five thousand rounds that is about two thousand four hundred, "
            "against a measured hundred and fifty-nine: true, but loose."
        ) as vo:
            self.play(FadeIn(head), Create(ln_))
            vo.wait_until("a")
            self.play(FadeIn(m_i), FadeIn(m_s), GrowFromCenter(brace), FadeIn(bl))
            vo.wait_until("b")
            self.play(FadeIn(hat), Create(bar), FadeIn(ucb))
            vo.wait_until("c")
            self.play(FadeIn(pic_note), Write(col[0][0]), FadeIn(col[0][1]))
            vo.wait_until("d")
            self.play(Write(col[1][0]), FadeIn(col[1][1]))
            vo.wait_until("e")
            self.play(Write(col[2][0]), FadeIn(col[2][1]))
            vo.wait_until("f")
            self.play(FadeIn(tail))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ Thompson sampling
    def thompson(self):
        head = label(r"Thompson sampling: \ act on a guess", font_size=36).to_edge(UP, buff=0.3)
        counts = [(60, 31), (25, 11), (12, 5), (6, 2)]          # illustrative (pulls, wins)
        g, ax = curve_axes([0, 1, 0.25], [0, 7, 2], r"mean reward $\theta$", r"posterior density of each arm's "
                           r"mean", [0, 0.25, 0.5, 0.75, 1], [], x_length=6.2, y_length=3.6)
        g.next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.7)
        curves = VGroup(*[ax.plot(lambda x, a=w + 1, bb=n - w + 1: min(7.0, beta_pdf(x, a, bb)), x_range=[0.005, 0.995,
                                                                                                      0.005],
                                  color=ARM[i], stroke_width=3) for i, (n, w) in enumerate(counts)])
        leg = VGroup(*[label(rf"arm {i + 1}: \ {w} wins in {n} pulls", font_size=17, color=ARM[i])
                       for i, (n, w) in enumerate(counts)]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        leg.arrange_in_grid(rows=2, cols=2, buff=(0.5, 0.08), col_alignments="ll").next_to(g, DOWN, buff=0.2)
        leg.align_to(g, LEFT)
        ill = note(r"illustrative counts", font_size=16).next_to(leg, DOWN, buff=0.12).align_to(g, LEFT)
        rng = np.random.default_rng(4)
        draws = [[float(rng.beta(w + 1, n - w + 1)) for n, w in counts] for _ in range(4)]

        def ticks(d):
            win = int(np.argmax(d))
            grp = VGroup()
            for i, v in enumerate(d):
                grp.add(Triangle(color=ARM[i], fill_opacity=1, stroke_width=0).scale(0.11).move_to(
                    ax.c2p(v, 0) + DOWN * 0.02 + UP * 0.12))
            pick = label(rf"pull arm {win + 1}", font_size=20, color=ARM[win]).next_to(ax.c2p(0.03, 6.6), RIGHT,
                                                                                       buff=0.0)
            return VGroup(grp, pick)
        fs = 27
        rows = [
            MathTex(r"\theta_i \sim \mathrm{Beta}(w_i + 1,\ n_i - w_i + 1)", font_size=fs),
            MathTex(r"a_t = \arg\max_i\ \theta_i", font_size=fs),
            MathTex(r"\Pr[a_t = i]", r"=", r"\Pr\big[\,i \text{ is the best arm} \mid \text{data}\,\big]",
                    font_size=fs),
        ]
        rows[2][2].set_color(YES)
        whys = [
            label(r"the posterior from a uniform prior: \ $w_i$ wins in $n_i$ pulls", font_size=17, color=GREY_B),
            label(r"one sample per arm; \ pull the arm with the highest", font_size=17, color=GREY_B),
            label(r"probability matching: \ unsure arms still get tried", font_size=17, color=GREY_B),
        ]
        col = stacked(rows, whys, buff=0.3).next_to(g, RIGHT, buff=0.5).align_to(g, UP)
        fit_x(col)
        foot = wrapped_label(r"Thompson \ (1933); \ proved to meet the Lai--Robbins rate for Bernoulli arms \ "
                             r"(Kaufmann, \ Korda and Munos \ 2012)", col.width, font_size=18,
                             color=LAM).next_to(col, DOWN, buff=0.4).align_to(col, LEFT)
        with self.voiceover(
            "The second strategy is older. William Thompson proposed it in 1933, with medical treatments in mind. "
            "<bookmark mark='a'/> Keep a posterior for each arm's mean: with a uniform prior, a beta distribution set"
            " by its wins and losses. Well-tried arms are narrow, rarely tried ones wide. <bookmark mark='b'/> Each "
            "round, draw one guess from every posterior and pull the arm whose guess is highest. <bookmark mark='c'/>"
            " Then each arm is pulled with exactly the probability that it is the best, given the data, so uncertain "
            "arms still get their chances. <bookmark mark='d'/> In 2012 it was proved to meet the optimal rate for "
            "such arms."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(ill))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.2), FadeIn(leg), Write(col[0][0]),
                      FadeIn(col[0][1]), run_time=2)
            vo.wait_until("b")
            self.play(Write(col[1][0]), FadeIn(col[1][1]))
            cur = ticks(draws[0])
            self.play(FadeIn(cur))
            for d in draws[1:]:
                self.wait(0.4)
                self.play(Transform(cur, ticks(d)), run_time=0.6)
            vo.wait_until("c")
            self.play(Write(col[2][0]), FadeIn(col[2][1]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ measured, against Lai-Robbins
    def curves(self):
        b = load("bandits")
        T = b["T"]
        c = b["lai_robbins_const"]
        names = ("epsilon-greedy", "UCB1", "Thompson")
        cols = {"epsilon-greedy": KERN, "UCB1": DATA, "Thompson": YES}
        disp = {"epsilon-greedy": r"$\epsilon$-greedy", "UCB1": r"UCB1", "Thompson": r"Thompson"}

        n_pts = len(b["lai_robbins"])
        step = T // n_pts
        xs = [step * i + 1 for i in range(n_pts)]
        head = label(r"Measured, \ against the Lai--Robbins rate", font_size=36).to_edge(UP, buff=0.3)
        g, ax = curve_axes([0, T, 1000], [0, 180, 50], r"round $t$", r"regret, \ mean of 100 runs",
                           [0, 2500, 5000], [0, 50, 100, 150], x_length=5.2, y_length=3.9)
        g.next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.9)
        lines = {k: polyline(ax, xs, b["curves"][k], cols[k], width=3) for k in names}
        lr = polyline(ax, xs, b["lai_robbins"], HEAD, width=2.5)
        lr = DashedVMobject(lr, num_dashes=60)
        labs = VGroup()
        for k in names:
            v = b["final"][k]
            labs.add(label(rf"{disp[k]}: \ {v:.1f}", font_size=17, color=cols[k]).next_to(ax.c2p(T, v), RIGHT,
                                                                                         buff=0.1))
        lrl = label(rf"${c:.1f}\,\ln t$", font_size=17, color=HEAD).next_to(ax.c2p(T, c * math.log(T)), RIGHT,
                                                                           buff=0.1)
        labs[1].next_to(lrl, UP, buff=0.06).align_to(lrl, LEFT)
        cap = note(r"Bernoulli arms $0.5, \ 0.45, \ 0.4, \ 0.3$; \ $\epsilon = 0.05$", font_size=16).next_to(
            g, DOWN, buff=0.12).align_to(g, LEFT)
        fs = 25
        rows = [
            MathTex(r"\liminf_{T\to\infty} \frac{\mathbb E[n_i(T)]}{\ln T}", r"\ge",
                    r"\frac{1}{\mathrm{KL}(\mu_i, \mu^*)}", font_size=fs),
            MathTex(r"R_T", r"\gtrsim", r"\sum_i \frac{\Delta_i}{\mathrm{KL}(\mu_i,\mu^*)}\,\ln T", r"=",
                    rf"{c:.1f}\,\ln T", font_size=fs),
        ]
        rows[1][4].set_color(HEAD)
        whys = [
            label(r"any policy that is good on every problem; \ Lai and Robbins \ (1985)", font_size=17,
                  color=GREY_B),
            label(r"$\mathrm{KL}$: \ the divergence between two coins \ (\textit{AI, Built} 1)", font_size=17,
                  color=GREY_B),
        ]
        col = stacked(rows, whys, buff=0.3).to_edge(DOWN, buff=0.25).to_edge(RIGHT, buff=0.35)
        side = wrapped_label(rf"$\epsilon$-greedy explores forever: \ its regret ends up linear in $t$; \ UCB1 sits "
                             rf"above the curve; \ Thompson below it at $T = {T:,}$, \ allowed, \ since the theorem "
                             r"is about the rate as $T \to \infty$".replace(",", "{,}"), 4.4, font_size=18,
                             color=GREY_A)
        side.next_to(head, DOWN, buff=0.5).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Here are the three strategies on our arms, averaged over a hundred runs of five thousand rounds. "
            "<bookmark mark='a'/> Epsilon-greedy explores at random one round in twenty, and pays for that forever: "
            "its regret ends up linear. <bookmark mark='b'/> UCB1 and Thompson sampling bend over. "
            "<bookmark mark='c'/> How far can anyone bend? Tze Leung Lai and Robbins proved in 1985 that any policy "
            "good on every problem must pull each bad arm about log T over the divergence between its coin and the "
            "best coin. <bookmark mark='d'/> For our arms that is seventeen point four log T. UCB1, at a hundred and "
            "fifty-nine, sits above it; Thompson, at about fifty, below it at this T, which the theorem allows: it is"
            " about the rate as T grows."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(cap))
            vo.wait_until("a")
            self.play(Create(lines["epsilon-greedy"]), FadeIn(labs[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(lines["UCB1"]), Create(lines["Thompson"]), FadeIn(labs[1]), FadeIn(labs[2]),
                      run_time=2)
            vo.wait_until("c")
            self.play(Write(col[0][0]), FadeIn(col[0][1]))
            vo.wait_until("d")
            self.play(Write(col[1][0]), FadeIn(col[1][1]), Create(lr), FadeIn(lrl))
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ why ln T, and why sqrt(KT)
    def lower(self):
        head = label(r"Why nobody does better", font_size=36).to_edge(UP, buff=0.3)
        a, bm = 0.45, 0.5
        g, ax = curve_axes([0.2, 0.75, 0.1], [0, 1.05, 0.5], r"average reward after $n$ pulls", None, [0.3, 0.45,
                           0.5, 0.6, 0.7], [], x_length=5.8, y_length=3.0, fx=lambda v: f"{v:g}")
        g.next_to(head, DOWN, buff=0.7).to_edge(LEFT, buff=0.7)

        def bells(n):
            sd_a, sd_b = math.sqrt(a * (1 - a) / n), math.sqrt(bm * (1 - bm) / n)
            fa = ax.plot(lambda x: math.exp(-0.5 * ((x - a) / sd_a) ** 2), x_range=[0.2, 0.75, 0.002], color=LAM,
                         stroke_width=3)
            fb = ax.plot(lambda x: math.exp(-0.5 * ((x - bm) / sd_b) ** 2), x_range=[0.2, 0.75, 0.002],
                         color=YES, stroke_width=3)
            nl = label(rf"$n = {n}$", font_size=20, color=HEAD).next_to(ax.c2p(0.2, 1.05), RIGHT, buff=0.1)
            return VGroup(fa, fb, nl)
        wl = VGroup(label(r"world A: \ this arm pays 0.45", font_size=17, color=LAM),
                    label(r"world B: \ it pays 0.5 and is the best", font_size=17, color=YES)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).next_to(g, DOWN, buff=0.2).align_to(g, LEFT)
        ill = note(r"normal approximation", font_size=16).next_to(wl, DOWN, buff=0.12).align_to(g, LEFT)
        fs = 25
        rows = [
            MathTex(r"\Pr[\text{confuse A and B}]", r"\approx", r"e^{-n\,\mathrm{KL}}", font_size=fs),
            MathTex(r"e^{-n\,\mathrm{KL}}", r"\lesssim", r"\frac{1}{T}", r"\Rightarrow", r"n", r"\gtrsim",
                    r"\frac{\ln T}{\mathrm{KL}}", font_size=fs),
            MathTex(r"\Delta \approx \sqrt{K/T}", r"\Rightarrow", r"R_T \approx T\Delta = \sqrt{KT}", font_size=fs),
        ]
        rows[1][6].set_color(HEAD)
        rows[2][2].set_color(NO)
        whys = [
            label(r"$n$ pulls separate two coins only as fast as their divergence allows", font_size=17,
                  color=GREY_B),
            label(r"a mistake in world B costs about $T\Delta$: \ so Lai and Robbins' $\ln T$", font_size=17,
                  color=GREY_B),
            label(r"if the gap is this small, \ $T$ rounds cannot find the best of $K$ arms", font_size=17,
                  color=GREY_B),
        ]
        col = stacked(rows, whys, buff=0.3).next_to(g, RIGHT, buff=0.5).align_to(g, UP).shift(UP * 0.2)
        fit_x(col)
        mm = wrapped_label(r"for gaps chosen by an adversary, \ no algorithm beats order $\sqrt{KT}$ \ (Auer, \ "
                           r"Cesa-Bianchi, \ Freund and Schapire \ 2002): \ $\ln T$ for a fixed problem, \ "
                           r"$\sqrt{T}$ in the worst case", col.width, font_size=18, color=LAM).next_to(
            col, DOWN, buff=0.35).align_to(col, LEFT)
        prac = wrapped_label(r"in practice: \ recommendation, \ ad allocation, \ adaptive experiments; \ the price is "
                             r"that the data no longer form a clean A/B test", 12.4, font_size=19,
                             color=KERN).to_edge(DOWN, buff=0.3)
        cur = bells(20)
        with self.voiceover(
            "Why can nobody beat log T? <bookmark mark='a'/> Take a bad arm paying point four five. In another world "
            "it pays point five and is the best. After twenty pulls the worlds look alike; <bookmark mark='b'/> after"
            " two hundred they part; after two thousand they are clear. <bookmark mark='c'/> The chance of confusing "
            "them falls like e to the minus n times their divergence. <bookmark mark='d'/> Confusion in the second "
            "world costs a share of every round, so that chance must be about one over T, and n at least log T over "
            "the divergence. <bookmark mark='e'/> And if an adversary sets the gap at root K over T, T rounds cannot "
            "find the best arm: regret about root K T. <bookmark mark='f'/> Bandits now run recommendation and ad "
            "allocation, at the price of a cleaner experiment."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(cur), FadeIn(wl), FadeIn(ill))
            vo.wait_until("a")
            self.play(Indicate(wl, color=WHITE))
            vo.wait_until("b")
            self.play(Transform(cur, bells(200)), run_time=1.5)
            self.play(Transform(cur, bells(2000)), run_time=1.5)
            vo.wait_until("c")
            self.play(Write(col[0][0]), FadeIn(col[0][1]))
            vo.wait_until("d")
            self.play(Write(col[1][0]), FadeIn(col[1][1]))
            vo.wait_until("e")
            self.play(Write(col[2][0]), FadeIn(col[2][1]))
            self.play(FadeIn(mm))
            vo.wait_until("f")
            self.play(FadeIn(prac))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, NO, mono)
