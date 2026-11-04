from __future__ import annotations

import numpy as np

from videos.stats.stats9.common import *  # noqa: F403


def coin_row(seq, r=0.16, buff=0.1):
    return VGroup(*[Circle(radius=r, stroke_color=S.ACCENT, stroke_width=2, fill_color=S.ACCENT, fill_opacity=0.9 if s_ else 0.0)
                    for s_ in seq]).arrange(RIGHT, buff=buff)


class Sufficiency(VoiceoverScene):
    def construct(self):
        self.card()
        self.coins()
        self.definition()
        self.regenerate()
        self.factorization()
        self.catalogue()
        self.tanks()
        self.minimal()

    def card(self):
        card = chapter_card(6, r"Sufficiency", r"Which part of the data carries the information?", lit=(1922,), part=PART)
        with self.voiceover("Chapter six. Sufficiency."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def coins(self):
        d = load("sufficiency")
        seqs = d["seqs"]
        rows = VGroup(*[coin_row(s_) for s_ in seqs]).arrange(DOWN, buff=0.14).move_to([-4.9, -0.3, 0])
        head = label(r"five tosses, \ two heads: \ the ten possible orders", font_size=26).to_edge(UP, buff=0.35)
        cols = VGroup()
        for j, p in enumerate(("0.2", "0.5", "0.8")):
            e = d[p]
            col = VGroup(MathTex(rf"p = {p}", font_size=28, color=GREY_A),
                         MathTex(rf"P(\text{{each}}) = {e['each']:.4f}", font_size=24),
                         MathTex(rf"P(S = 2) = {e['total']:.4f}", font_size=24),
                         MathTex(rf"P(\text{{each}} \mid S = 2) = {e['cond']:.1f}", font_size=24, color=S.ACCENT)).arrange(DOWN, buff=0.28)
            col.move_to([-1.6 + 2.95 * j, 0.0, 0])
            cols.add(col)
        foot = label(r"given $S$, \ the order is pure noise: \ its distribution is the same for every $p$", font_size=26,
                     color=S.ACCENT).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Toss a coin five times and get two heads. <bookmark mark='a'/> There are ten orders in which that could "
            "happen. <bookmark mark='b'/> If the chance of heads is point two, each particular order has probability "
            "point two squared times point eight cubed, about point zero two, and the chance of two heads in any order "
            "is ten times that. <bookmark mark='c'/> So given that there were two heads, each order has conditional "
            "probability exactly one in ten. <bookmark mark='d'/> Try p equals a half, or point eight: the individual "
            "probabilities change, but the conditional probability of each order is always one in ten. "
            "<bookmark mark='e'/> Once you know the number of heads, the order in which they came tells you nothing "
            "about p. Its distribution doesn't depend on p at all. The count is sufficient."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows], lag_ratio=0.15))
            vo.wait_until("b")
            self.play(FadeIn(cols[0][:3]))
            vo.wait_until("c")
            self.play(FadeIn(cols[0][3]))
            vo.wait_until("d")
            self.play(FadeIn(cols[1]), FadeIn(cols[2]))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def definition(self):
        dc = definition_card(r"Sufficient statistic", r"$T(X)$ is \emph{sufficient} for $\theta$ \ if the conditional distribution "
                             r"of $X$ given $T(X)$ \ does not depend on $\theta$.", color=S.ACCENT, width=9.6, font_size=28).move_to([0, 1.6, 0])
        rows = fit_rows(VGroup(
            label(r"Fisher (1922): \ ``the statistic chosen should summarise the whole of the relevant information supplied by "
                  r"the sample''", font_size=24, color=GREY_A),
            label(r"everything beyond $T$ is noise whose law we already know", font_size=26),
            label(r"so any inference about $\theta$ can be made from $T$ alone", font_size=26, color=S.ACCENT),
        ), 12.6, 0.36, [0, -1.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The definition. A statistic T is sufficient for theta if, once you know T, the "
            "conditional distribution of the full data doesn't depend on theta. <bookmark mark='b'/> Fisher introduced "
            "the idea in his 1922 paper: a sufficient statistic summarizes the whole of the relevant information the "
            "sample supplies. <bookmark mark='c'/> Whatever is left over, beyond T, is noise with a known distribution. "
            "<bookmark mark='d'/> And so anything you want to do about theta, estimating it, testing it, you can do "
            "from T alone, and lose nothing."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(dc, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def regenerate(self):
        g = np.random.Generator(np.random.PCG64(21))
        p, n = 0.3, 12
        real = (g.random(n) < p).astype(int)
        S_ = int(real.sum())
        fakes = []
        for _ in range(4):
            idx = g.choice(n, S_, replace=False)
            f = np.zeros(n, int)
            f[idx] = 1
            fakes.append(f)
        left = VGroup(label(r"Alice: \ the real data", font_size=24, color=DATA), coin_row(real, r=0.14, buff=0.06)).arrange(DOWN, buff=0.25)
        left.move_to([-3.6, 2.0, 0])
        msg = MathTex(rf"T = \textstyle\sum x_i = {S_}", font_size=34, color=S.ACCENT).move_to([0, 2.0, 0])
        arrow = Arrow([-0.8, 1.4, 0], [0.8, 1.4, 0], color=GREY_B, buff=0)
        right = VGroup(label(r"Bob: \ only $T$; \ he shuffles $T$ heads into 12 places", font_size=24, color=SIM),
                       *[coin_row(f, r=0.14, buff=0.06) for f in fakes]).arrange(DOWN, buff=0.2)
        right.move_to([3.4, -0.2, 0])
        foot = fit_rows(VGroup(
            label(r"Bob's fake data have exactly the same distribution as Alice's real data, \ for every $p$", font_size=24),
            label(r"so no procedure can do better with Alice's data than with Bob's: \ the rest of the data is lossless to discard",
                  font_size=24, color=S.ACCENT),
        ), 12.6, 0.3, [0, -2.8, 0])
        with self.voiceover(
            "Here's a way to see why. <bookmark mark='a'/> Alice has twelve coin tosses. She sends Bob only one number: "
            "the count of heads, here three. <bookmark mark='b'/> Bob, who doesn't know p, can still manufacture a "
            "dataset: he scatters three heads among twelve places at random. Because the conditional distribution of "
            "the data given the count doesn't depend on p, he can do that without knowing p. <bookmark mark='c'/> And "
            "his fake data have exactly the same distribution as Alice's real data, for every value of p. So any "
            "estimator, any test, applied to Bob's fake data performs exactly as well as on Alice's. Nothing was lost in "
            "the message. Throwing the rest away is lossless compression, for the purpose of learning about p."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(left))
            self.play(GrowArrow(arrow), FadeIn(msg))
            vo.wait_until("b")
            self.play(FadeIn(right[0]))
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in right[1:]], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def factorization(self):
        tc = theorem_card(r"The factorization theorem", r"$T$ is sufficient for $\theta$ \ if and only if \ "
                          r"$p_\theta(x) = g_\theta\big(T(x)\big)\, h(x)$ \ for some functions $g_\theta$ and $h$.",
                          who=r"Fisher (1922); \ Neyman (1935); \ Halmos \& Savage (1949) in general", color=S.ACCENT, width=10.4,
                          font_size=26).move_to([0, 2.65, 0])
        rows = [
            cmath(r"P_\theta(X = x \mid T = t)", r"=", r"\frac{p_\theta(x)}{\sum_{y:\,T(y) = t} p_\theta(y)}", font_size=32),
            cmath(r"\vphantom{x}", r"=", r"\frac{g_\theta(t)\,h(x)}{g_\theta(t)\sum_{y:\,T(y) = t} h(y)}", font_size=32),
            cmath(r"\vphantom{x}", r"=", r"\frac{h(x)}{\sum_{y:\,T(y) = t} h(y)}", r"\quad\text{free of }\theta", font_size=32),
        ]
        rows[2][2].set_color(S.ACCENT)
        whys = [why(r"discrete data, \ $T(x) = t$"), why(r"factor: \ $g_\theta(t)$ is the same for every $y$ in the sum"),
                why(r"it cancels: \ sufficient. \ (Conversely, \ $g_\theta(t) = P_\theta(T = t)$.)")]
        with self.voiceover(
            "Checking the definition directly is tedious. Fisher's factorization makes it easy. <bookmark mark='a'/> "
            "T is sufficient exactly when the density splits into two factors: one that depends on theta, but only "
            "through T, and one that may depend on the data in any way, but not on theta. Jerzy Neyman proved it in "
            "1935, and Paul Halmos and Jimmie Savage gave the general version in 1949. Here's the discrete proof. "
            "<bookmark mark='b'/> The conditional probability of the data given T equals t is the probability of x, "
            "over the total probability of all datasets with the same value of T. <bookmark mark='c'/> Factor the "
            "density. The theta-dependent factor is the same for every dataset in the sum, <bookmark mark='d'/> so it "
            "cancels, and what's left doesn't involve theta. That's sufficiency. For the converse, take g to be the "
            "probability of T itself."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tc, shift=UP * 0.2))
            step = ladder(self, rows, whys, keep=3, top=1.0, x=-0.6, buff=0.45, edge=6.9)
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def catalogue(self):
        items = [
            (r"Bernoulli$(p)$", r"\prod p^{x_i}(1-p)^{1-x_i} = p^{\sum x_i}(1-p)^{n - \sum x_i}", r"\sum x_i"),
            (r"Poisson$(\lambda)$", r"\prod \frac{\lambda^{x_i}e^{-\lambda}}{x_i!} = \lambda^{\sum x_i}e^{-n\lambda}\cdot\frac{1}{\prod x_i!}", r"\sum x_i"),
            (r"$N(\mu, \sigma^2)$", r"(2\pi\sigma^2)^{-n/2}\exp\Big(-\frac{\sum x_i^2 - 2\mu\sum x_i + n\mu^2}{2\sigma^2}\Big)",
             r"\big(\sum x_i,\ \sum x_i^2\big)"),
            (r"Gamma$(\alpha, \beta)$", r"\frac{(\prod x_i)^{\alpha - 1}e^{-\sum x_i/\beta}}{\Gamma(\alpha)^n\beta^{n\alpha}}",
             r"\big(\sum \log x_i,\ \sum x_i\big)"),
            (r"Uniform$(0, \theta)$; \ tanks", r"\theta^{-n}\,\mathbf 1\{\max x_i \le \theta\}", r"\max x_i"),
        ]
        rows = VGroup()
        for nm, dens, T in items:
            rows.add(VGroup(label(nm, font_size=24, color=GREY_A), MathTex(dens, font_size=26), MathTex(T, font_size=28, color=S.ACCENT)))
        hdr = VGroup(label(r"model", font_size=24, color=GREY_B), label(r"the likelihood, \ factored", font_size=24, color=GREY_B),
                     label(r"sufficient $T$", font_size=24, color=GREY_B))
        allr = VGroup(hdr, *rows)
        for r in allr:
            r[0].move_to([-5.0, 0, 0])
            r[1].move_to([0.2, 0, 0])
            r[2].move_to([5.0, 0, 0])
        allr.arrange(DOWN, buff=0.42).move_to([0, -0.1, 0])
        for r in allr:
            r[0].set_x(-5.0)
            if r[1].width > 6.6:
                r[1].width = 6.6
            r[1].set_x(0.2)
            r[2].set_x(5.2)
        with self.voiceover(
            "With factorization, sufficient statistics can be read straight off the likelihood. "
            "<bookmark mark='a'/> Bernoulli: the likelihood depends on the data only through the number of successes. "
            "<bookmark mark='b'/> Poisson: only through the total, times a factor that doesn't involve lambda. "
            "<bookmark mark='c'/> Normal with both parameters unknown: through the sum and the sum of squares, or "
            "equivalently the sample mean and variance, which is why Part 8's x-bar and s squared were all a normal "
            "sample had to offer. <bookmark mark='d'/> Gamma: the sum of the logs and the sum. Notice that the method of "
            "moments used the sum of squares, which is not part of this pair, a first hint at why it wasted "
            "information. <bookmark mark='e'/> And the uniform, and the tanks: the maximum alone."
        ) as vo:
            self.play(FadeIn(hdr))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def tanks(self):
        d = load("tanks")
        one = d["one"]
        m = max(one)
        f = TankFactory(m + 40, one, cols=36, cell=0.24, center=[0, 1.0, 0])
        f.tanks.set_fill(opacity=0.12)
        noise = VGroup(*[f.marks[i] for i, s_ in enumerate(one) if s_ != m])
        top = f.marks[one.index(m)]
        box = SurroundingRectangle(VGroup(*f.tanks[:m - 1]), color=GREY_B, stroke_width=1.5, buff=0.05)
        rows = fit_rows(VGroup(
            MathTex(rf"P_N(\text{{serials}} = s) = \binom{{N}}{{k}}^{{-1}}\,\mathbf 1\{{N \ge \max s\}}", font_size=30),
            label(rf"given $m = {m}$: \ the other five are a random 5 of the serials $1, \dots, {m - 1}$, \ whatever $N$ is",
                  font_size=26, color=GREY_A),
            label(r"the mean averages $m$ with five draws of pure noise", font_size=26, color=MOM),
            label(r"the maximum is sufficient; \ $2\bar x - 1$ is not a function of it", font_size=28, color=S.ACCENT),
        ), 12.6, 0.3, [0, -1.9, 0])
        with self.voiceover(
            "Back to the tanks, which can now be explained. <bookmark mark='a'/> The probability of the captured "
            "serials is one over N choose k if N is at least the maximum, and zero otherwise. It depends on the data "
            "only through the maximum, so the maximum is sufficient. <bookmark mark='b'/> Concretely: once you know the "
            "largest serial is two hundred and fourteen, the other five are just a random five from the serials below "
            "it, and that's true whatever N is. <bookmark mark='c'/> They're noise, with a known distribution. The mean "
            "averages the one informative number with five draws of noise. <bookmark mark='d'/> That's why two x-bar "
            "minus one is so much worse: it isn't a function of the sufficient statistic. The next chapter shows that "
            "this is always fixable."
        ) as vo:
            self.add(f.tanks)
            self.play(FadeIn(f.marks), FadeIn(f.numbers))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Indicate(top, color=MAX, scale_factor=1.6))
            vo.wait_until("b")
            self.play(Create(box), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(noise.animate.set_fill(MOM, opacity=0.6), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(top.animate.set_fill(MAX), FadeIn(rows[3]))
        self.clear_scene()

    def minimal(self):
        rows = fit_rows(VGroup(
            label(r"the whole data set is always sufficient; \ the aim is the smallest", font_size=26),
            label(r"\emph{minimal} sufficient: \ a function of every other sufficient statistic", font_size=26, color=S.ACCENT),
            MathTex(r"T(x) = T(y)\ \iff\ \frac{p_\theta(x)}{p_\theta(y)} \text{ is free of } \theta \qquad (\text{Lehmann \& Scheff\'e, 1950})",
                    font_size=28),
            label(r"Pitman--Koopman--Darmois (1935--36): \ a sufficient statistic of fixed dimension for every $n$", font_size=24,
                  color=GREY_A),
            label(r"exists (with fixed support) only in exponential families", font_size=24, color=GREY_A),
            label(r"so the normal, Poisson, gamma compress perfectly; \ the Cauchy needs the whole sample, \ sorted", font_size=24,
                  color=GREY_A),
        ), 12.6, 0.4, [0, 0.0, 0])
        with self.voiceover(
            "How far can the data be compressed? <bookmark mark='a'/> The full dataset is trivially sufficient, so the "
            "aim is the smallest sufficient statistic. <bookmark mark='b'/> A minimal sufficient statistic is one that "
            "can be computed from any other sufficient statistic. <bookmark mark='c'/> Erich Lehmann and Henry Scheffé "
            "gave a test in 1950: two datasets should get the same value exactly when the ratio of their likelihoods "
            "doesn't depend on theta. <bookmark mark='d'/> And a deep theorem, from Edwin Pitman, Bernard Koopman and "
            "Georges Darmois in the mid-1930s, says that a sufficient statistic of fixed dimension, whatever the sample "
            "size, exists only in exponential families, at least when the support is fixed. <bookmark mark='e'/> So the "
            "normal, the Poisson and the gamma compress perfectly into a few sums, while for the Cauchy distribution "
            "nothing less than the whole sorted sample will do. Exponential families are special, and Part 22 shows how "
            "much else follows from that."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k] if k < 3 else (rows[3:5] if k == 3 else rows[5]), shift=RIGHT * 0.2))
        self.clear_scene()
