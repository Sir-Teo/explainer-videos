from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai5.compute import density2
from videos.ai.ai5.s08_mcmc import heat_image
from videos.ai.ai7.common import BOUND, HIDDEN, PART, SEEN, ellipse_2sd, load

Q = C.MODEL_Q  # the approximation
P = C.TRUE_P  # the true posterior


def cov_of(theta):
    s0, s1, r = math.exp(theta[2]), math.exp(theta[3]), math.tanh(theta[4])
    return np.array([[s0 * s0, r * s0 * s1], [r * s0 * s1, s1 * s1]])


def before_after() -> VGroup:
    """A flat belief before the data, two bumps after it: the posterior in a picture."""
    def panel(f, color, word):
        base = Line([-0.9, 0, 0], [0.9, 0, 0], color=GREY_C, stroke_width=2)
        c = FunctionGraph(f, x_range=[-0.9, 0.9], color=color, stroke_width=3)
        return VGroup(base, c, label(word, font_size=20, color=color).next_to(base, DOWN, buff=0.08))

    before = panel(lambda t: 0.25, GREY_B, r"before")
    after = panel(lambda t: 0.75 * np.exp(-(t + 0.42) ** 2 / 0.03) + 0.5 * np.exp(-(t - 0.45) ** 2 / 0.03), P,
                  r"after the data")
    g = VGroup(before, after).arrange(RIGHT, buff=0.9, aligned_edge=DOWN)
    y = after[:2].get_y()
    return g.add(Arrow([before.get_right()[0], y, 0], [after.get_left()[0], y, 0], buff=0.1, color=GREY_B,
                       stroke_width=3))


class VI(VoiceoverScene):
    def construct(self):
        card = chapter_card(16, r"Variational inference", r"What if the true answer is a shape you can't compute?",
                            part=PART)
        with self.voiceover("Chapter sixteen. Variational inference."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.fit()
        self.derive()
        self.cavi()
        self.reparam()
        self.amortize()

    def fit(self):
        v = load("vi")
        path, kl = np.asarray(v["path"]), np.asarray(v["kl_qp"])
        t_pq = np.asarray(v["t_pq"])
        ax = Axes(x_range=[-4, 4, 1], y_range=[-3, 3, 1], x_length=7.6, y_length=5.7, tips=False,
                  axis_config={"stroke_width": 0}).move_to([-2.6, -0.4, 0])
        img = heat_image(density2, (-4, 4), (-3, 3)).stretch_to_fit_width(7.6).stretch_to_fit_height(5.7).move_to(ax)
        frame_ = SurroundingRectangle(img, buff=0, color=GREY_D, stroke_width=1.5)
        k = ValueTracker(0)

        def q_now():
            i = int(round(k.get_value()))
            th = path[i]
            return VGroup(ellipse_2sd(ax, th[:2], cov_of(th), Q, stroke_width=4, k=1.0),
                          ellipse_2sd(ax, th[:2], cov_of(th), Q, stroke_width=2, k=2.0).set_stroke(opacity=0.6),
                          Dot(ax.c2p(*th[:2]), radius=0.07, color=Q))

        qg = always_redraw(q_now)
        klv = DecimalNumber(kl[0], num_decimal_places=2, font_size=36, color=Q)
        klv.add_updater(lambda m: m.set_value(kl[int(round(k.get_value()))]))
        colors = {r"q": Q, r"p": P}
        kf = VGroup(cmath(r"\mathrm{KL}(", r"q", r"\,\|\,", r"p", r")", r"=", colors=colors, font_size=40), klv)
        kf.arrange(RIGHT, buff=0.15).move_to([4.3, 2.4, 0])
        keyq = label(r"$q$: \ the best single Gaussian", font_size=26, color=Q).next_to(kf, DOWN, buff=0.3)
        keyp = label(r"$p$: \ the true posterior \ (Part 5's two bumps)", font_size=24, color=P).next_to(keyq, DOWN, buff=0.15)
        one = label(r"$\mathrm{KL}(q\,\|\,p)$: \ hides inside one bump", font_size=26, color=Q).next_to(keyp, DOWN, buff=0.45)
        pq_el = DashedVMobject(ellipse_2sd(ax, t_pq[:2], cov_of(t_pq), WHITE, stroke_width=3, k=1.0), num_dashes=30)
        pq_el2 = DashedVMobject(ellipse_2sd(ax, t_pq[:2], cov_of(t_pq), WHITE, stroke_width=2, k=2.0), num_dashes=40)
        two = label(r"$\mathrm{KL}(p\,\|\,q)$: \ covers both, \ spills between", font_size=26, color=WHITE)
        two.next_to(one, DOWN, buff=0.2)
        colors2 = {r"\mathrm{ELBO}(q)": Q, r"\mathrm{KL}\big(q \,\|\, p(z \mid x)\big)": Q}
        elbo = cmath(r"\log p(x)", "=", r"\mathrm{ELBO}(q)", "+", r"\mathrm{KL}\big(q \,\|\, p(z \mid x)\big)",
                     colors=colors2, font_size=34).to_edge(DOWN, buff=0.35).to_edge(RIGHT, buff=0.4)
        en = label(r"raise the bound, \ and the gap closes \ (VAEs, Part 20)", font_size=24, color=GREY_A)
        en.next_to(elbo, UP, buff=0.15)
        post_card = gloss(r"posterior", r"what we believe about the hidden things \\ after seeing the data", before_after(),
                          corner=DR, width=4.4, color=P)
        # the identity as a bar: log p(x) = ELBO + KL, the KL part shrinking as q improves (schematic widths)
        BW, BH = 4.2, 0.42
        bx0 = 4.3 - BW / 2

        def elbo_bar():
            w_kl = 0.7 * BW * kl[int(round(k.get_value()))] / kl[0]
            lo = Rectangle(width=BW - w_kl, height=BH, stroke_width=0, fill_color=Q, fill_opacity=0.85)
            hi = Rectangle(width=max(w_kl, 0.01), height=BH, stroke_color=Q, stroke_width=2, fill_opacity=0)
            lo.move_to([bx0 + (BW - w_kl) / 2, -1.1, 0])
            hi.move_to([bx0 + BW - w_kl / 2, -1.1, 0])
            return VGroup(lo, hi, MathTex(r"\mathrm{ELBO}", font_size=26, color=Q).next_to(lo, DOWN, buff=0.1),
                          MathTex(r"\mathrm{KL}", font_size=26, color=Q).next_to(hi, DOWN, buff=0.1))

        bar = always_redraw(elbo_bar)
        bar_top = Line([bx0, -0.89, 0], [bx0 + BW, -0.89, 0])
        bar_b = VGroup(Brace(bar_top, UP, buff=0.05, color=GREY_B))
        bar_b.add(MathTex(r"\log p(x)", font_size=28).next_to(bar_b[0], UP, buff=0.06))
        bar_n = label(r"the ELBO: \ computable, \ always below $\log p(x)$", font_size=22, color=GREY_A)
        bar_n.move_to([4.3, -1.95, 0])
        with self.voiceover(
            "For most models with hidden parts, the exact answer, the posterior over the hidden variables, is a shape "
            "we can't compute. <bookmark mark='p'/> The posterior is what we believe about the hidden things after "
            "seeing the data: part five's updated belief. Part five sampled such shapes with Markov chains. "
            "Variational inference does something else: it picks the closest shape from a simple family, here a "
            "single Gaussian, and uses that instead. <bookmark mark='a'/> Closest in what sense? In part one's KL "
            "divergence, from q to p. Start from a poor guess, and slide the Gaussian downhill."
        ) as vo:
            self.play(FadeIn(img), Create(frame_), FadeIn(keyp))
            vo.wait_until("p")
            self.play(FadeIn(post_card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(post_card))
            self.play(Write(kf), FadeIn(qg), FadeIn(keyq))
            self.play(k.animate.set_value(len(path) - 1), run_time=5.0, rate_func=smooth)
        with self.voiceover(
            "It settles on one bump and ignores the other. This direction of KL punishes q for putting probability "
            "where p has almost none, so q hides inside a single mode, a single peak of the distribution. "
            "<bookmark mark='a'/> Measure the other way "
            "round, from p to q, and the best Gaussian covers both bumps, spilling into the empty middle. Neither is "
            "wrong: they answer different questions. <bookmark mark='b'/> The identity behind it all: the log "
            "probability of the data equals a lower bound, the ELBO, plus that KL. The ELBO is a score we can "
            "compute that always sits below the true one. <bookmark mark='c'/> Push it up, and the KL has to shrink, "
            "dragging q toward p. Variational autoencoders, in part twenty, are trained exactly this way."
        ) as vo:
            self.play(FadeIn(one))
            vo.wait_until("a")
            self.play(Create(pq_el), Create(pq_el2), FadeIn(two))
            vo.wait_until("b")
            k.set_value(0)
            self.play(Write(elbo), FadeIn(en), FadeIn(bar), FadeIn(bar_b), FadeIn(bar_n))
            vo.wait_until("c")
            self.play(k.animate.set_value(len(path) - 1), run_time=3.0, rate_func=smooth)
        bar.clear_updaters()
        qg.clear_updaters()
        klv.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        colors = {r"\mathrm{ELBO}(q)": Q, r"\mathrm{KL}\big(q \,\|\, p(z \mid x)\big)": Q, r"q(z)": Q}
        rows = [
            cmath(r"\log p(x)", r"=", r"\mathbb{E}_{q}\big[\log p(x)\big]", colors=colors, font_size=38),
            cmath(r"\log p(x)", r"=", r"\mathbb{E}_{q}\Big[\log \frac{p(x, z)}{p(z \mid x)}\Big]", colors=colors, font_size=38),
            cmath(r"\log p(x)", r"=", r"\mathbb{E}_{q}\Big[\log \frac{p(x, z)}{q(z)}\Big]", r"+",
                  r"\mathbb{E}_{q}\Big[\log \frac{q(z)}{p(z \mid x)}\Big]", colors=colors, font_size=38),
            cmath(r"\log p(x)", r"=", r"\mathrm{ELBO}(q)", r"+", r"\mathrm{KL}\big(q \,\|\, p(z \mid x)\big)", colors=colors,
                  font_size=40),
        ]
        whys = [why(r"$\log p(x)$ doesn't depend on $z$"), why(r"Bayes: \ $p(x) = p(x, z) / p(z \mid x)$"),
                why(r"multiply and divide by $q(z)$"), why(r"a KL is never negative: \\ the ELBO is a lower bound")]
        step = ladder(self, rows, whys, keep=4, top=2.6, x=-2.4, buff=0.55, edge=6.8)
        head = label(r"Where the identity comes from", font_size=32).to_edge(UP, buff=0.25)
        em = VGroup(label(r"EM (chapter 4): \ $q$ = the exact posterior, \ so KL $= 0$", font_size=24, color=GREY_A),
                    label(r"variational inference: \ $q$ from a simple family, \ so KL $> 0$", font_size=24, color=Q))
        em.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Where does that identity come from? Three lines. The log probability of the data doesn't depend on "
            "z, so averaging it over q changes nothing. <bookmark mark='a'/> By Bayes' rule, p of x is the joint "
            "over the posterior. <bookmark mark='b'/> Multiply and divide by q, and split the log in two. "
            "<bookmark mark='c'/> The first part is the ELBO, the evidence lower bound; the second is the KL "
            "divergence from q to the true posterior. <bookmark mark='d'/> It's chapter four's EM bound again. EM "
            "can make the KL zero, because there the posterior is computable. Variational inference can't, so it "
            "settles for the best q in a family it can handle, and the gap is what it gives up."
        ) as vo:
            self.play(FadeIn(head))
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            self.play(FadeIn(em))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cavi(self):
        from scipy.stats import gamma as G

        d = load("cavi")
        muN, lamN, aN, bN = (float(v) for v in d["post"])
        qs = [list(map(float, q_)) for q_ in d["q"]]
        sdm = float(d["sd_mu_true"])
        m0, m1 = muN - 4.2 * sdm, muN + 4.2 * sdm
        t0, t1 = float(G.ppf(0.0003, aN, scale=1 / bN)), float(G.ppf(0.9997, aN, scale=1 / bN))
        ax = Axes(x_range=[m0, m1, 1], y_range=[t0, t1, 0.01], x_length=5.6, y_length=4.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-3.4, -0.5, 0])
        xl = label(r"mean $\mu$ of the rate of ``the''", font_size=22, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        yl = label(r"precision $\tau$", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)

        def post(m, t):
            return float(G.pdf(t, aN, scale=1 / bN) * np.sqrt(lamN * t / (2 * np.pi)) * np.exp(-0.5 * lamN * t * (m - muN) ** 2))

        pk = post(muN, (aN - 0.5) / bN)
        pc = contour_lines(ax, post, (m0, m1), (t0, t1), [pk * f for f in (0.1, 0.4, 0.8)], n=(70, 60),
                           colors=(P, P), stroke_width=2.5)

        def qden(q_):
            m, lam, a, b = q_

            def f(mu, t):
                return float(G.pdf(t, a, scale=1 / b) * np.sqrt(lam / (2 * np.pi)) * np.exp(-0.5 * lam * (mu - m) ** 2))
            mode = f(m, (a - 1) / b)
            return contour_lines(ax, f, (m0, m1), (t0, t1), [mode * fr for fr in (0.1, 0.4, 0.8)], n=(70, 60),
                                 colors=(Q, Q), stroke_width=3)

        qc = [qden(q_) for q_ in qs[:3]]
        el = np.asarray(d["elbo"])
        kl = np.asarray(d["kl"])
        rows = VGroup(
            cmath(r"q(\mu, \tau)", r"=", r"q(\mu)\, q(\tau)", font_size=34, colors={r"q(\mu, \tau)": Q}),
            cmath(r"\log q^*(\mu)", r"=", r"\mathbb{E}_{q(\tau)}\big[\log p(x, \mu, \tau)\big] + \text{const}", font_size=30,
                  colors={r"\log q^*(\mu)": Q}),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.3, 2.5, 0])
        rl = label(r"mean field: \ update each factor in turn \ (and the same for $\tau$)", font_size=20, color=GREY_A)
        rl.next_to(rows, DOWN, buff=0.15)
        it = Integer(0, font_size=28, color=Q)
        itl = VGroup(label(r"sweep", font_size=24, color=GREY_A), it).arrange(RIGHT, buff=0.12).move_to([2.0, 0.6, 0])
        ev = DecimalNumber(el[0], num_decimal_places=3, font_size=28, color=Q)
        evl = VGroup(label(r"ELBO:", font_size=24, color=GREY_A), ev).arrange(RIGHT, buff=0.12).next_to(itl, RIGHT, buff=0.6)
        chk = VGroup(label(r"the identity, checked:", font_size=22, color=GREY_A),
                     MathTex(rf"\log p(x) = {d['logp']:.3f}", font_size=30, color=C.BITS),
                     MathTex(rf"\mathrm{{ELBO}} + \mathrm{{KL}} = {el[-1]:.3f} + {kl[-1]:.3f}", font_size=30, color=Q),
                     label(rf"(KL integrated on a grid; \ difference ${sci(max(d['gap'], 1e-12), 0)}$)", font_size=20,
                           color=GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.4, -1.0, 0])
        sd = label(rf"spread of $\mu$: \ true ${d['sd_mu_true']:.2f}$, \ mean field ${d['sd_mu_q']:.2f}$", font_size=22,
                   color=Q).move_to([3.4, -2.9, 0])
        key = legend([(P, r"exact posterior"), (Q, r"$q(\mu)\,q(\tau)$")], font_size=20)
        key.move_to(ax.get_corner(UR) + LEFT * key.width / 2 + DOWN * key.height / 2 + LEFT * 0.1 + DOWN * 0.1)
        narrower = d["sd_mu_q"] < d["sd_mu_true"]
        verdict = (f"Mean field is a little too sure of itself: q's spread for mu is {d['sd_mu_q']:.2f}, the truth's "
                   f"{d['sd_mu_true']:.2f}, because it ignores how mu and tau lean on each other." if narrower else
                   f"Here q's spread for mu is {d['sd_mu_q']:.2f}, the truth's {d['sd_mu_true']:.2f}.")
        with self.voiceover(
            f"Now a model where we can check everything. Take {d['N']} of Austen's pages and their rate of 'the'. Model "
            "it as a bell curve of unknown mean and unknown precision, with the usual conjugate prior, so the exact "
            "posterior is known: here are its contours. <bookmark mark='a'/> Variational inference pretends we "
            "couldn't compute it, and looks for q of mu times q of tau: two independent factors, the mean-field "
            "family. <bookmark mark='b'/> Coordinate ascent updates one factor at a time: the best log q of one "
            "variable is the expected log joint, averaged over the other. <bookmark mark='c'/> Start q far too "
            f"narrow. Each sweep raises the ELBO, and after {len(qs[:3]) - 1} sweeps it has converged. "
            f"<bookmark mark='d'/> And the identity holds: log p of x, computed exactly, is {d['logp']:.2f}; the ELBO "
            f"plus the KL, integrated numerically, agree to the third decimal place. <bookmark mark='e'/> " + verdict
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), Create(pc), FadeIn(key))
            vo.wait_until("a")
            self.play(Write(rows[0]))
            vo.wait_until("b")
            self.play(Write(rows[1]), FadeIn(rl))
            vo.wait_until("c")
            self.play(FadeIn(qc[0]), FadeIn(itl), FadeIn(evl))
            for i in (1, 2):
                self.play(ReplacementTransform(qc[i - 1], qc[i]), ChangeDecimalToValue(it, i), ChangeDecimalToValue(ev, el[i]),
                          run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(chk))
            vo.wait_until("e")
            self.play(FadeIn(sd))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def reparam(self):
        r = load("reparam")
        bins = np.asarray(r["bins"])
        hs, hr = np.asarray(r["h_score"]), np.asarray(r["h_rep"])
        top = float(max(hs.max(), hr.max()))
        g = axes([float(bins[0]), float(bins[-1]), 5], [0, top * 1.05, top / 2], x_length=7.6, y_length=3.6,
                 xlabel=r"one-sample estimate of the gradient", xticks=[-20, -10, 0, 10], center=[-2.4, -1.0, 0])
        ax = g.ax
        w = bins[1] - bins[0]

        def hist(h, col, op):
            return VGroup(*[Rectangle(width=ax.c2p(w, 0)[0] - ax.c2p(0, 0)[0], height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.001),
                                      stroke_width=0, fill_color=col, fill_opacity=op).move_to(ax.c2p(bins[i] + w / 2, v / 2))
                            for i, v in enumerate(h)])

        h1, h2 = hist(hs, GREY_B, 0.6), hist(hr, Q, 0.8)
        tl = DashedLine(ax.c2p(r["true"], 0), ax.c2p(r["true"], top * 1.05), color=C.BITS, stroke_width=2)
        tlab = label(rf"true gradient: \ ${r['true']:.1f}$", font_size=20, color=C.BITS).next_to(tl, UP, buff=0.05)
        rows = VGroup(
            cmath(r"\nabla_m \mathbb{E}_{z \sim \mathcal{N}(m, 1)}[f(z)]", font_size=32),
            cmath(r"\text{score function:}\;", r"f(z)\,(z - m)", font_size=30),
            cmath(r"\text{reparameterize } z = m + \varepsilon:\;", r"f'(m + \varepsilon)", colors={r"f'(m + \varepsilon)": Q},
                  font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.4, 2.4, 0])
        res = VGroup(label(rf"spread: \ ${r['score_sd']:.1f}$ \ vs \ ${r['rep_sd']:.1f}$", font_size=26),
                     label(rf"variance ${r['ratio']:.0f}\times$ smaller", font_size=26, color=Q))
        res.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.6, -0.4, 0])
        tag = note(rf"$f(z) = (z - 2)^2$, \ $m = {r['m']}$; \ ${r['R']:,}$ draws each".replace(",", "{,}"), font_size=20)
        tag.next_to(res, DOWN, buff=0.3)
        hcard = history_card(2013, r"D.~Kingma \& M.~Welling; \ D.~Rezende, S.~Mohamed \& D.~Wierstra (2014)",
                             r"the reparameterization trick", width=5.0).to_corner(UL, buff=0.3)
        with self.voiceover(
            "CAVI needs expectations in closed form. For a neural network there aren't any, so we follow the gradient "
            "of the ELBO with samples instead. <bookmark mark='a'/> The old way, the score function, multiplies f by "
            "the gradient of log q. It's unbiased, but noisy. <bookmark mark='b'/> In 2013 Diederik Kingma and Max "
            "Welling, and independently Danilo Rezende and colleagues, wrote the sample as the mean plus noise, so "
            "the gradient can flow through the sample itself: the reparameterization trick. "
            f"<bookmark mark='c'/> Same expectation, same answer on average; but here its spread is {r['rep_sd']:.1f} "
            f"against {r['score_sd']:.1f}, a variance {r['ratio']:.0f} times smaller."
        ) as vo:
            self.play(Write(rows[0]), FadeIn(g), FadeIn(hcard))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]), FadeIn(h1), Create(tl), FadeIn(tlab), FadeOut(hcard))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(h2), FadeIn(res), FadeIn(tag))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def amortize(self):
        def box(t, col, w=2.2):
            b = RoundedRectangle(width=w, height=1.0, corner_radius=0.15, stroke_color=col, fill_color=col, fill_opacity=0.12)
            return VGroup(b, label(t, font_size=24, color=col).move_to(b))

        x = box(r"a page $x$", SEEN, 1.8)
        enc = box(r"encoder", Q, 2.0)
        par = box(r"$\mu(x),\ \sigma(x)$", Q, 2.2)
        z = box(r"$z = \mu + \sigma \varepsilon$", HIDDEN, 2.6)
        dec = box(r"decoder", HIDDEN, 2.0)
        row = VGroup(x, enc, par, z, dec).arrange(RIGHT, buff=0.45).move_to(UP * 0.6)
        if row.width > 13.2:
            row.width = 13.2
        arrs = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.06, color=GREY_B, stroke_width=2.5) for a, b in zip(row, row[1:])])
        old = label(r"CAVI, \ LDA (chapter 5): \ a separate optimization of $q$ for every data point", font_size=24,
                    color=GREY_A).to_edge(UP, buff=0.5)
        new = label(r"amortized: \ one network outputs $q$ for any $x$, \ trained on the ELBO", font_size=26, color=Q)
        new.next_to(old, DOWN, buff=0.25)
        vae = label(r"$=$ \ the variational autoencoder \ (Kingma \& Welling, 2013) \ $\longrightarrow$ \ Part 20",
                    font_size=26, color=HIDDEN).next_to(row, DOWN, buff=0.7)
        tag = schematic_tag(DR)
        with self.voiceover(
            "One more step. CAVI, and the topic model of chapter five, optimize a separate q for every data point. "
            "<bookmark mark='a'/> Instead, train one network, an encoder, to output q's parameters for any input: "
            "amortized inference. <bookmark mark='b'/> Sample z with the reparameterization trick, decode it back, "
            "and train both networks on the ELBO. <bookmark mark='c'/> That's the variational autoencoder, and part "
            "twenty builds one. The same bound trains diffusion models in part twenty-one."
        ) as vo:
            self.play(FadeIn(old), FadeIn(tag), FadeIn(x))
            vo.wait_until("a")
            self.play(FadeIn(new), GrowArrow(arrs[0]), FadeIn(enc), GrowArrow(arrs[1]), FadeIn(par))
            vo.wait_until("b")
            self.play(GrowArrow(arrs[2]), FadeIn(z), GrowArrow(arrs[3]), FadeIn(dec))
            vo.wait_until("c")
            self.play(FadeIn(vae))
        self.wait(0.3)
        self.clear_scene()
