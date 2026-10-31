from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai1.common import ALPHA27, MONO, PART, letter, load, plain_axes, polyline


def slivers(p, h, W=11.0, y0=-2.5, scale=0.3, order=None, color=C.SURPRISE, opacity=0.8) -> VGroup:
    """Rectangles of width W p[i] and height scale * h[i], laid out in ``order``; ``g[i]`` is symbol i's."""
    order = list(range(len(p))) if order is None else list(order)
    rects, cum = {}, 0.0
    for i in order:
        r = Rectangle(width=max(W * p[i], 0.003), height=max(scale * h[i], 0.003), stroke_width=0.8,
                      stroke_color=BACKGROUND, fill_color=color, fill_opacity=opacity)
        r.move_to([-W / 2 + (cum + p[i] / 2) * W, y0 + scale * h[i] / 2, 0])
        rects[i] = r
        cum += p[i]
    return VGroup(*[rects[i] for i in range(len(p))])


def gaussian_density(x, mean, sigma):
    """A normalized bell curve; never flatten a peak to fit a plotting window."""
    x = np.asarray(x, float)
    return np.exp(-0.5 * ((x - mean) / sigma) ** 2) / (sigma * math.sqrt(2 * math.pi))


def density_ceiling(p, *paths):
    """One vertical scale for both fits, including every intermediate Gaussian peak."""
    peak = max(float(np.max(p)), *(float(1 / (np.min(path[:, 1]) * math.sqrt(2 * math.pi)))
                                   for path in paths))
    return math.ceil(1.12 * peak * 10) / 10


class CrossEntropy(VoiceoverScene):
    def construct(self):
        self.card()
        self.wrong_code()
        self.decompose()
        self.gibbs()
        self.loss()
        self.asymmetry()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(7, r"Cross-entropy and KL: the price of a wrong model",
                            r"What does guessing with the wrong probabilities cost?", lit=(1948, 1951), part=PART)
        with self.voiceover("Chapter seven. What happens when your guesses are wrong?") as vo:
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def wrong_code(self):
        lt = load("letters")
        p = np.asarray(lt["p"])
        order = list(lt["order"])
        ie, iz = ALPHA27.index("e"), ALPHA27.index("z")
        q = p.copy()
        q[ie], q[iz] = p[iz], p[ie]  # a model that has e and z the wrong way round
        H = float(-(p * np.log2(p)).sum())
        CE = float(-(p * np.log2(q)).sum())
        KL = CE - H
        self.H, self.CE, self.KL = H, CE, KL
        head = mtex([r"H(p, q)", r"=", r"\sum_x p(x)\, \log_2 \frac{1}{q(x)}"], font_size=42).to_edge(UP, buff=0.4)
        head[0].set_color(C.MODEL_Q)
        sub = label(r"\textit{cross-entropy}: \ the data come from $p$, \ the code was built for $q$", font_size=26,
                    color=GREY_A).next_to(head, DOWN, buff=0.2)
        W, y0, sc = 11.0, -2.6, 0.27
        true = slivers(p, -np.log2(p), W=W, y0=y0, scale=sc, order=order, color=C.TRUE_P, opacity=0.75)
        wrong = slivers(p, -np.log2(q), W=W, y0=y0, scale=sc, order=order, color=C.MODEL_Q, opacity=0.18)
        wrong.set_stroke(C.MODEL_Q, width=2, opacity=1)
        base = Line([-W / 2, y0, 0], [W / 2, y0, 0], color=GREY_C, stroke_width=1.5)
        e_lab = letter("e", font_size=24, color=C.MODEL_Q).next_to(wrong[ie], UP, buff=0.08)
        z_lab = letter("z", font_size=24, color=C.MODEL_Q).next_to(wrong[iz], UP, buff=0.08)
        legend = VGroup(
            label(rf"coded for the true frequencies $p$: \ area $= H(p) = {H:.2f}$ bits", font_size=24, color=C.TRUE_P),
            label(rf"coded for a model $q$ that swaps \texttt{{e}} and \texttt{{z}}: \ area $= {CE:.2f}$ bits",
                  font_size=24, color=C.MODEL_Q),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([-1.2, 1.15, 0])
        codes = {ALPHA27[i]: c for i, c in enumerate(load("huffman")["codes"])}
        cols_x = [-4.6, -2.0, 0.7, 3.0, 5.1]  # centers of the five columns
        hdr = VGroup(*[label(t, font_size=24, color=GREY_B) for t in (
            r"symbol", r"Huffman codeword", r"length $\ell$", r"its bet $2^{-\ell}$", r"true $p$")])
        bet_rows = VGroup()
        for s_ in (" ", "e", "z"):
            i = ALPHA27.index(s_)
            ell = len(codes[s_])
            bet_rows.add(VGroup(
                letter(s_, font_size=30), Text(codes[s_], font=MONO, font_size=24, color=C.BITS),
                MathTex(str(ell), font_size=32), MathTex(rf"1/{2 ** ell:,}".replace(",", "{,}"), font_size=32,
                                                         color=C.MODEL_Q),
                MathTex(f"{p[i]:.4f}", font_size=32, color=C.TRUE_P)))
        for k, row in enumerate([hdr, *bet_rows]):
            for m, x in zip(row, cols_x):
                m.move_to([x, 0.75 - 0.85 * k, 0])
        bet_cap = label(r"a code that spends $\ell$ bits on a symbol bets that it has probability $2^{-\ell}$",
                        font_size=26, color=GREY_A).move_to([0, -2.9, 0])
        bets = VGroup(hdr, bet_rows, bet_cap)
        with self.voiceover(
            "Codes and guesses are the same thing: a code that spends l bits on a symbol bets that it has "
            "probability two to the minus l. What if the bets are wrong? <bookmark mark='a'/> Say the data come "
            "from p, but the code was built for a model q. Each symbol costs log of one over q bits, and on average "
            "we pay the cross-entropy: the sum of p times log one over q."
        ) as vo:
            self.play(FadeIn(head[0]), FadeIn(head[1:]), FadeIn(hdr))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in bet_rows], lag_ratio=0.5), run_time=2.0)
            self.play(FadeIn(bet_cap))
            vo.wait_until("a")
            self.play(FadeIn(sub))
        with self.voiceover(
            "As a picture: <bookmark mark='a'/> with the right probabilities, the area is the entropy, "
            f"{H:.2f} bits. <bookmark mark='b'/> Now use a model that has e and z the wrong way round. Every e, one "
            f"symbol in {round(1 / p[ie])}, now costs {-np.log2(q[ie]):.1f} bits. The area grows to {CE:.2f}."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeOut(bets))
            self.play(Create(base), FadeIn(true), FadeIn(legend[0]))
            vo.wait_until("b")
            self.play(FadeIn(wrong), FadeIn(legend[1]), FadeIn(e_lab), FadeIn(z_lab), run_time=1.5)
        self.parts = VGroup(head, sub, true, wrong, base, legend, e_lab, z_lab)

    # ------------------------------------------------------------------
    def decompose(self):
        lt = load("letters")
        H, CE, KL = self.H, self.CE, self.KL
        rows = [
            mtex([r"H(p, q)", r"=", r"\sum_x p(x) \log_2 \frac{1}{p(x)}", r"+", r"\sum_x p(x) \log_2 \frac{p(x)}{q(x)}"],
                 font_size=38),
            mtex([r"H(p, q)", r"=", r"H(p)", r"+", r"D_{\mathrm{KL}}(p \,\|\, q)"], font_size=44),
        ]
        for r in rows:
            r[0].set_color(C.MODEL_Q)
        rows[1][2].set_color(C.ENTROPY)
        rows[1][4].set_color(C.KL)
        VGroup(*rows).arrange(DOWN, buff=0.5).move_to(UP * 1.4)
        b1 = Brace(rows[1][2], DOWN, color=C.ENTROPY)
        b2 = Brace(rows[1][4], DOWN, color=C.KL)
        t1 = label(r"the price of the world's\\ own randomness", font_size=24, color=C.ENTROPY).next_to(b1, DOWN)
        t2 = label(r"the price of being wrong:\\ the Kullback--Leibler divergence", font_size=24, color=C.KL)
        t2.next_to(b2, DOWN)
        t1.shift(LEFT * max(0.0, t1.get_right()[0] - t2.get_left()[0] + 0.4))
        nums = VGroup(
            label(rf"swapped \texttt{{e}}, \texttt{{z}}: \ ${CE:.2f} = {H:.2f} + {KL:.2f}$", font_size=26),
            label(rf"letters guessed uniformly: \ ${math.log2(27):.2f} = {lt['H_passage']:.2f} + {lt['KL_uniform']:.2f}$"
                  r" \ (the Falcon passage)", font_size=26),
            label(rf"letter frequencies of the $30$ books, used on the passage: \ $D_{{\mathrm{{KL}}}} = "
                  rf"{lt['KL_books']:.3f}$", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.4)
        kb = float(lt["KL_books"])
        books_said = ("are wrong by less than a hundredth of a bit" if kb < 0.01 else
                      f"are wrong by {kb:.3f} bits per letter")
        with self.voiceover(
            "Split the log in two, <bookmark mark='a'/> and the cross-entropy separates into two prices. First, the "
            "entropy of p: the world's own randomness, which no code can remove. <bookmark mark='b'/> Second, the "
            "price of being wrong: the Kullback–Leibler divergence of q from p, from 1951. <bookmark mark='c'/> "
            f"Swapping e and z costs {KL:.2f} bits per symbol. The letter frequencies of our thirty books, used on "
            f"the Falcon passage, {books_said}."
        ) as vo:
            self.play(FadeOut(self.parts))
            self.play(Write(rows[0]))
            vo.wait_until("a")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]))
            self.play(GrowFromCenter(b1), FadeIn(t1))
            vo.wait_until("b")
            self.play(GrowFromCenter(b2), FadeIn(t2))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(n) for n in nums], lag_ratio=0.5), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gibbs(self):
        head = label(r"Gibbs' inequality: \ $D_{\mathrm{KL}}(p \,\|\, q) \ge 0$", font_size=38).to_edge(UP, buff=0.35)
        ax = plain_axes([0, 8, 2], [-1, 3.2, 1], 5.4, 3.6).shift(LEFT * 3.7 + DOWN * 0.6)
        xs = np.linspace(0.5, 8, 300)
        lg = polyline(ax, xs, np.log2(xs), color=C.KL, stroke_width=5)
        a_, b_ = 1.0, 7.0
        m = 0.5 * (a_ + b_)
        pa = glow_dot(ax.c2p(a_, math.log2(a_)), color=C.BITS, radius=0.07, layers=3)
        pb = glow_dot(ax.c2p(b_, math.log2(b_)), color=C.BITS, radius=0.07, layers=3)
        chord = Line(ax.c2p(a_, math.log2(a_)), ax.c2p(b_, math.log2(b_)), color=C.BITS, stroke_width=3)
        pm = glow_dot(ax.c2p(m, math.log2(m)), color=C.KL, radius=0.08, layers=4)
        pc = glow_dot(ax.c2p(m, 0.5 * (math.log2(a_) + math.log2(b_))), color=C.BITS, radius=0.08, layers=4)
        gap = Line(pc.get_center(), pm.get_center(), color=WHITE, stroke_width=2.5)
        cap = label(r"Jensen (Chapter 3): \ average of logs $\le$ log of the average", font_size=24, color=GREY_A)
        cap.next_to(ax, DOWN, buff=0.3)
        P, Q = C.TRUE_P, C.MODEL_Q
        colors = {r"p(x)": P, r"q(x)": Q}
        D = r"-D_{\mathrm{KL}}(p \,\|\, q)"
        rows = [
            cmath(D, "=", r"\sum_x", r"p(x)", r"\log_2", r"\frac{q(x)}{p(x)}", colors=colors, font_size=34),
            cmath(D, r"\le", r"\log_2", r"\sum_x", r"p(x)", r"\frac{q(x)}{p(x)}", colors=colors, font_size=34),
            cmath(D, r"\le", r"\log_2", r"\sum_x", r"q(x)", colors=colors, font_size=34),
            cmath(D, r"\le", r"\log_2 1 = 0", font_size=34),
        ]
        whys = [why(r"an average of $\log_2 \frac{q}{p}$, \ weights $p$"), why(r"Jensen: $\log_2$ bends down"),
                why(r"the $p(x)$ cancel"), why(r"$q$ is a distribution")]
        step = ladder(self, rows, whys, keep=4, top=2.6, x=3.1, buff=0.3, edge=6.9)
        res = VGroup(
            label(r"equality only when $q = p$:\\ the truth is the best code", font_size=28, color=C.BITS),
            label(r"so $H(p, q) \ge H(p)$; \ and", font_size=26, color=GREY_A),
            MathTex(r"H(Y) - H(Y \mid X) = D_{\mathrm{KL}}\big(p(x, y) \,\|\, p(x)\,p(y)\big) \ge 0", font_size=30,
                    color=GREY_A),
            label(r"that drop is the \textit{mutual information} $I(X; Y)$:\\ Chapter 12", font_size=24, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        if res.width > 6.2:
            res.scale_to_fit_width(6.2)
        res.move_to([-3.75, -0.4, 0])
        with self.voiceover(
            "Is being wrong always a cost? Yes, by chapter three's argument. <bookmark mark='a'/> The log bends "
            "downward: the average of logs is at most the log of the average. <bookmark mark='b'/> Minus the "
            "divergence is an average, weighted by p, of the log of q over p. <bookmark mark='c'/> Move the log outside. <bookmark mark='d'/> Inside, the p's cancel, "
            "<bookmark mark='e'/> and what's left is the total of q, which is one. The log of one is zero."
        ) as vo:
            self.play(FadeIn(head), Create(ax), Create(lg), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(pa), FadeIn(pb), Create(chord), FadeIn(pm), FadeIn(pc), Create(gap), FadeIn(cap))
            vo.wait_until("b")
            step(0)
            vo.wait_until("c")
            step(1)
            vo.wait_until("d")
            step(2)
            vo.wait_until("e")
            step(3)
        with self.voiceover(
            "So the divergence is never negative, and zero only when q equals p, where Jensen's inequality is an "
            "equality. <bookmark mark='a'/> The truth is the best code. The inequality is named after Josiah Willard "
            "Gibbs, who used it in statistical mechanics. <bookmark mark='b'/> It also pays a debt from chapter "
            "three: the drop in entropy from knowing X is a divergence too, so it can't be negative. Knowing more "
            "never hurts, on average. <bookmark mark='c'/> That drop, the mutual information, gets its own chapter."
        ) as vo:
            self.play(FadeOut(VGroup(ax, lg, pa, pb, chord, pm, pc, gap, cap)))
            vo.wait_until("a")
            self.play(FadeIn(res[0], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(res[1:3]))
            vo.wait_until("c")
            self.play(FadeIn(res[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def loss(self):
        head = label(r"Cross-entropy is how every language model is trained", font_size=36).to_edge(UP, buff=0.45)
        f = mtex(r"\mathcal{L}(\theta) = \frac{1}{N} \sum_{t=1}^{N} \log \frac{1}{q_\theta(x_t \mid x_{<t})}",
                 font_size=46).next_to(head, DOWN, buff=0.6)
        f[0][0:4].set_color(C.LOSS)
        rows = VGroup(
            label(r"$\approx H(p, q_\theta)$, \ measured on real text", font_size=30),
            label(r"$= H(p) + D_{\mathrm{KL}}(p \,\|\, q_\theta)$: \ only the second part can be trained away",
                  font_size=30),
            label(r"the floor is $H(p)$: \ the entropy of language itself", font_size=30, color=C.ENTROPY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(f, DOWN, buff=0.6)
        unit = note(r"papers report it in nats per token: \ $1$ nat $= 1/\ln 2 \approx 1.443$ bits", font_size=24)
        unit.to_edge(DOWN, buff=0.5)
        ln_card = gloss(r"$\ln$, \ and nats", r"$\ln x = \log_e x$, \ the log to base $e \approx 2.718$\\"
                        r"surprise measured with $\ln$ is in nats: \ $1$ nat $\approx 1.44$ bits", corner=DR, width=4.8,
                        color=C.KL)
        ln_card.next_to(f, DOWN, buff=0.7).set_x(0)
        with self.voiceover(
            "Here is why this matters for AI. <bookmark mark='a'/> The loss every large language model is trained "
            "to minimize is exactly this: the average of log one over q, for each token of real text, given the "
            "tokens before it. <bookmark mark='n'/> Usually with the natural log, ln, so it's counted in nats: one "
            "nat is about 1.44 bits. <bookmark mark='b'/> It's the cross-entropy between the world's text and the "
            "model. <bookmark mark='c'/> Training can only shrink the divergence; <bookmark mark='d'/> the entropy "
            "of language itself is a floor no model can go below."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f))
            vo.wait_until("n")
            self.play(FadeIn(ln_card, shift=UP * 0.2), FadeIn(unit))
            vo.wait_until("b")
            self.play(FadeOut(ln_card), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def asymmetry(self):
        d = load("kl")
        x, p = np.asarray(d["x"]), np.asarray(d["p"])
        fwd, ra = np.asarray(d["fwd"]), np.asarray(d["rev_a"])
        wide = abs(fwd[-1, 1] - d["sd"]) < 0.05 and abs(fwd[-1, 0] - d["mean"]) < 0.05  # moment matching
        one_peak = ra[-1, 1] < 0.5 * fwd[-1, 1]
        head = label(r"$D_{\mathrm{KL}}$ is not symmetric", font_size=38).to_edge(UP, buff=0.35)
        axes, qs, readouts, indicators, objectives = [], [], [], [], []
        trackers = []
        ymax = density_ceiling(p, fwd, ra)
        for k, (title, path) in enumerate([
            (r"$\min_q D_{\mathrm{KL}}(p \,\|\, q)$: \ cover everything $p$ does", fwd),
            (r"$\min_q D_{\mathrm{KL}}(q \,\|\, p)$: \ go only where $p$ goes", ra),
        ]):
            center = -3.5 + 7.0 * k
            ax = CornerAxes([-6, 6, 2], [0, ymax, 0.2], x_length=6.0, y_length=3.0, tips=False,
                            axis_config={"stroke_color": GREY_C, "include_ticks": True,
                                         "tick_size": 0.05, "stroke_width": 2})
            ax.move_to([center, -0.75, 0])
            t = label(title, font_size=24, color=GREY_A).next_to(ax, UP, buff=0.35)
            if t.width > 6.3:
                t.scale_to_fit_width(6.3)
            objectives.append(t)
            pc = polyline(ax, x, p, color=C.TRUE_P, stroke_width=3.5)
            fill = Polygon(ax.c2p(x[0], 0), *[ax.c2p(float(a), float(b)) for a, b in zip(x, p)],
                           ax.c2p(x[-1], 0), stroke_width=0, fill_color=C.TRUE_P, fill_opacity=0.16)
            # Shared ticks make the heights directly comparable across the two panels.
            tick_labels = VGroup(*[MathTex(f"{y:.2g}", font_size=17, color=GREY_B)
                                   .next_to(ax.c2p(-6, y), LEFT, buff=0.08)
                                   for y in (0, ymax / 2, ymax)])
            m_t, s_t, loss_t = (ValueTracker(float(path[0, j])) for j in range(3))
            trackers.append((m_t, s_t, loss_t, path))

            def qcurve(ax=ax, m_t=m_t, s_t=s_t):
                return polyline(ax, x, gaussian_density(x, m_t.get_value(), s_t.get_value()),
                                color=C.MODEL_Q, stroke_width=3.5)

            def spread(ax=ax, m_t=m_t, s_t=s_t):
                m, s = m_t.get_value(), s_t.get_value()
                y = 0.04 * ymax
                ends = [ax.c2p(m - s, y), ax.c2p(m + s, y)]
                return VGroup(Line(*ends, color=C.MODEL_Q, stroke_width=4, stroke_opacity=0.7),
                              Dot(ax.c2p(m, y), radius=0.045, color=C.MODEL_Q))

            row = VGroup()
            for symbol, tracker, places, color in ((r"\mu =", m_t, 2, C.MODEL_Q),
                                                   (r"\sigma =", s_t, 2, C.MODEL_Q),
                                                   (r"D_{\mathrm{KL}} =", loss_t, 3, C.KL)):
                number = DecimalNumber(tracker.get_value(), num_decimal_places=places,
                                       font_size=22, color=color)
                number.add_updater(lambda mob, tracker=tracker: mob.set_value(tracker.get_value()))
                pair = VGroup(MathTex(symbol, font_size=22, color=color), number).arrange(RIGHT, buff=0.1)
                row.add(pair)
            row.arrange(RIGHT, buff=0.3).move_to([center, 1.85, 0])
            # Fixed number anchors keep changing digit widths from moving the whole row.
            readouts.append(row)
            qc = always_redraw(qcurve)
            indicators.append(always_redraw(spread))
            axes.append(VGroup(ax, t, fill, pc, tick_labels))
            qs.append(qc)
        lp = label(r"$p$: \ two peaks", font_size=26, color=C.TRUE_P)
        lq = label(r"$q$: \ one bell curve", font_size=26, color=C.MODEL_Q)
        VGroup(lp, lq).arrange(RIGHT, buff=1.0).next_to(head, DOWN, buff=0.3)
        density_label = note(r"probability density", font_size=18).move_to([0, -2.5, 0])

        def replay(k):
            m_t, s_t, loss_t, path = trackers[k]
            positions = np.linspace(0, 1, len(path))

            def update(_mob, alpha):
                for j, tracker in enumerate((m_t, s_t, loss_t)):
                    tracker.set_value(float(np.interp(alpha, positions, path[:, j])))

            return UpdateFromAlphaFunc(VGroup(), update)
        res = VGroup(
            label(rf"$\mu = {fwd[-1, 0]:.2f},\ \sigma = {fwd[-1, 1]:.2f}$: \ matches $p$'s mean and spread", font_size=22,
                  color=C.MODEL_Q).move_to([-3.5, -2.85, 0]),
            label(rf"$\mu = {ra[-1, 0]:.2f},\ \sigma = {ra[-1, 1]:.2f}$: \ locks onto one peak", font_size=22,
                  color=C.MODEL_Q).move_to([3.5, -2.85, 0]),
        )
        why_ = VGroup(
            label(r"$p \log \frac{p}{q}$ explodes where $p > 0$ but $q \approx 0$", font_size=22, color=GREY_A),
            label(r"$q \log \frac{q}{p}$ explodes where $q > 0$ but $p \approx 0$", font_size=22, color=GREY_A),
        )
        why_[0].next_to(res[0], DOWN, buff=0.15)
        why_[1].next_to(res[1], DOWN, buff=0.15)
        fit = ("pulls q wide, to cover both peaks: it ends with exactly p's mean and spread." if wide else
               "pulls q wide, to cover both peaks.")
        with self.voiceover(
            "One more property, which will matter a lot later: the divergence is not symmetric. Say the truth p "
            "has two peaks, and our model q can only be a bell curve: one smooth hump, set by its center and its "
            "width. Which bell curve is best? It depends on which way round we measure. <bookmark mark='a'/> Minimizing the divergence of q from p, the "
            "training loss we just met, <bookmark mark='b'/> " + fit
        ) as vo:
            self.play(FadeIn(head), FadeIn(axes[0]), FadeIn(axes[1]), FadeIn(lp), FadeIn(lq))
            self.add(*qs, *indicators, *readouts)
            self.play(FadeIn(density_label))
            vo.wait_until("a")
            self.play(Indicate(objectives[0], color=C.MODEL_Q, scale_factor=1.02))
            vo.wait_until("b")
            self.play(replay(0), run_time=3.0, rate_func=linear)
            self.play(FadeIn(res[0]), FadeIn(why_[0]))
        squeeze = "it squeezes into a single peak and ignores the other." if one_peak else "it narrows toward one peak."
        with self.voiceover(
            f"The other way round, <bookmark mark='a'/> q is punished for putting probability where p has none, so "
            f"{squeeze} Each fit is bad by the other's measure: the wide curve scores {d['rev_at_fwd']:.2f} bits the second "
            f"way, the narrow one {d['fwd_at_rev']:.1f} bits the first. <bookmark mark='b'/> Covering everything, or "
            "committing to one thing: that choice comes back in variational autoencoders, in Part 20, and in "
            "distillation and reinforcement learning from human feedback, in Part 27."
        ) as vo:
            vo.wait_until("a")
            self.play(Indicate(objectives[1], color=C.MODEL_Q, scale_factor=1.02))
            self.play(replay(1), run_time=3.0, rate_func=linear)
            self.play(FadeIn(res[1]), FadeIn(why_[1]))
        for mob in [*qs, *indicators, *readouts]:
            mob.clear_updaters(recursive=True)
        self.wait(0.3)
        self.clear_scene()
