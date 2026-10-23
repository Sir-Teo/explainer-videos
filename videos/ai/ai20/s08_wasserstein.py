from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai20.common import (DATA, DISC, GAN_C, HIST, PART, WGAN_C, Plane, load, take_away)
from videos.ai.ai20.s06_game import replay_gan


class Wasserstein(VoiceoverScene):
    def construct(self):
        self.card()
        self.lines()
        self.emd()
        self.duality()
        self.ring()
        self.price()

    def card(self):
        card = chapter_card(7, r"Wasserstein GANs", r"What should the critic measure when nothing overlaps?",
                            lit=(), part=PART)
        with self.voiceover("Chapter seven. Wasserstein GANs."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def lines(self):
        j = load("jsw")
        th = np.asarray(j["thetas"])
        js, w = np.asarray(j["js"]), np.asarray(j["w"])
        pl = Plane(3.6, center=[-4.6, 0.3, 0], box=1.5)
        theta = ValueTracker(0.8)
        p0 = Line(pl.p(0, 0), pl.p(0, 1), color=DATA, stroke_width=6)
        pt = always_redraw(lambda: Line(pl.p(theta.get_value(), 0), pl.p(theta.get_value(), 1), color=GAN_C,
                                        stroke_width=6))
        tv = DecimalNumber(theta.get_value(), num_decimal_places=2, font_size=28, color=GAN_C)
        tl = VGroup(MathTex(r"\theta =", font_size=28, color=GAN_C), tv).arrange(RIGHT, buff=0.15)
        tl.next_to(pl, DOWN, buff=0.15)
        tv.add_updater(lambda m: m.set_value(theta.get_value()))
        lab = VGroup(MathTex(r"p_0", font_size=28, color=DATA).next_to(pl.p(0, 1), UP, buff=0.1),
                     label(r"the data: \ $x = 0$, \ $y \sim U[0, 1]$", font_size=20, color=DATA),
                     label(r"the model: \ $x = \theta$", font_size=20, color=GAN_C))
        lab[1:].arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(pl, UP, buff=0.15)
        g = axes([-1, 1], [0, 1.1], x_length=6.0, y_length=3.6, xlabel=r"$\theta$", xticks=[-1, 0, 1],
                 yticks=[0, round(math.log(2), 2), 1], center=[2.6, 0.2, 0])
        jsx = curve(g.ax, [-1, -0.001, 0.001, 1], [math.log(2), math.log(2), 0, math.log(2)], C.KL, 2)
        jsx = VGroup(curve(g.ax, [-1, -0.02], [math.log(2)] * 2, C.KL, 2), curve(g.ax, [0.02, 1], [math.log(2)] * 2,
                                                                                    C.KL, 2),
                     Dot(g.ax.c2p(0, 0), radius=0.05, color=C.KL))
        wx = curve(g.ax, [-1, 0, 1], [1, 0, 1], WGAN_C, 2)
        jd = VGroup(*[Dot(g.ax.c2p(a, b), radius=0.06, color=C.KL) for a, b in zip(th, js)])
        wd = VGroup(*[Dot(g.ax.c2p(a, b), radius=0.06, color=WGAN_C) for a, b in zip(th, w)])
        lg = legend([(C.KL, r"Jensen--Shannon: \ exact $\log 2$; \ dots from a trained discriminator"),
                     (WGAN_C, r"Wasserstein-1: \ exact $|\theta|$; \ dots from a trained critic")], font_size=18)
        lg.next_to(g, UP, buff=0.12).align_to(g, LEFT)
        k = int(np.argmin(np.abs(th - 0.5)))
        cite_ = cite(r"Arjovsky, Chintala \& Bottou, \textit{Wasserstein GAN} (2017)", corner=DR)
        js_err = float(np.abs(js[th != 0] - math.log(2)).max())
        wk, tk = float(w[k]), float(th[k])
        with self.voiceover(
            "Martin Arjovsky, Soumith Chintala and Léon Bottou asked what Jensen-Shannon does when distributions "
            "don't overlap, the normal case for images. Their example: the data a segment at x equals zero, the "
            "model the same segment at theta. <bookmark mark='a'/> For any theta but zero, JS is log two: flat, no "
            "gradient, no sign that theta is getting closer. <bookmark mark='b'/> Discriminators trained at "
            f"seventeen values of theta stay within {js_err:.2f} of log two. <bookmark mark='c'/> A distance that "
            "measures how far the mass must move gives a V whose slope points home; a trained critic puts it at "
            f"{wk:.2f} for theta {tk:.2f}."
        ) as vo:
            self.play(FadeIn(pl), Create(p0), FadeIn(pt), FadeIn(tl), FadeIn(lab), FadeIn(cite_))
            self.play(theta.animate.set_value(0.25), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(g), FadeIn(lg[0]), FadeIn(jsx))
            self.play(theta.animate.set_value(-0.6), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d_, scale=1.5) for d_ in jd], lag_ratio=0.05))
            vo.wait_until("c")
            self.play(FadeIn(lg[1]), Create(wx), LaggedStart(*[FadeIn(d_, scale=1.5) for d_ in wd], lag_ratio=0.05),
                      theta.animate.set_value(th[k]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def emd(self):
        xs = np.arange(8)
        p = np.array([0, 3, 5, 2, 0, 0, 0, 0], float)
        q = np.array([0, 0, 0, 1, 2, 4, 3, 0], float)
        p, q = p / p.sum(), q / q.sum()
        W = 0.55
        base = -1.6

        def hist(v, col, x0):
            return VGroup(*[Rectangle(width=W * 0.9, height=4.0 * h, stroke_width=0, fill_color=col,
                                      fill_opacity=0.8).move_to([x0 + i * W, base + 2.0 * h, 0]) for i, h in
                            enumerate(v)])

        hp, hq = hist(p, DATA, -4.4), hist(q, C.MODEL_Q, -4.4)
        hq.set_opacity(0.55)
        moves = VGroup(*[CurvedArrow([-4.4 + a * W, base + 2.6, 0], [-4.4 + b * W, base + 2.6, 0], angle=-0.7,
                                     color=GREY_A, stroke_width=2, tip_length=0.12)
                         for a, b in ((1, 3), (1, 4), (2, 4), (2, 5), (2, 5), (3, 6))])
        axis = Line([-4.8, base, 0], [-4.4 + 8 * W, base, 0], color=GREY_C, stroke_width=1.5)
        f = cmath(r"W_1(p, q)", r"=", r"\inf_{\gamma \in \Pi(p, q)} \; \mathbb E_{(x, y) \sim \gamma}\, \|x - y\|",
                  font_size=34).move_to([2.9, 2.2, 0])
        f[0].set_color(WGAN_C)
        fl = label(r"$\gamma$: \ a transport plan, \ how much mass goes from $x$ to $y$", font_size=22,
                   color=GREY_A).next_to(f, DOWN, buff=0.2)
        h1 = history_card(1781, r"Monge", r"moving earth for fortifications at least cost", width=4.0,
                          font_size=20).move_to([1.6, -1.4, 0])
        h2 = history_card(1942, r"Kantorovich", r"the relaxed, linear-programming form", width=4.0,
                          font_size=20).move_to([5.0, -1.4, 0])
        tg = note(r"illustrative").to_corner(DR, buff=0.25)
        with self.voiceover(
            "That is the earth mover's distance: p a pile of sand, q a hole of the same volume. <bookmark "
            "mark='a'/> A transport plan says how much sand goes where; its cost is mass times distance. <bookmark "
            "mark='b'/> Wasserstein-1 is the cheapest plan's cost. Gaspard Monge posed the problem in 1781; Leonid "
            "Kantorovich gave its modern form in 1942."
        ) as vo:
            self.play(FadeIn(axis), FadeIn(hp), FadeIn(hq), FadeIn(tg))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(m) for m in moves], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("b")
            self.play(Write(f), FadeIn(fl))
            self.play(FadeIn(h1, shift=UP * 0.1), FadeIn(h2, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def duality(self):
        rows = [
            cmath(r"W_1(p, q)", r"=", r"\sup_{\|f\|_L \le 1} \; \mathbb E_{p}[f(x)] - \mathbb E_{q}[f(x)]",
                  font_size=36),
            cmath(r"\mathcal L_{\text{critic}}", r"=", r"\mathbb E_{q}[f(\tilde x)] - \mathbb E_{p}[f(x)]", r"+",
                  r"\lambda\, \mathbb E_{\hat x}\big[(\|\nabla f(\hat x)\| - 1)^2\big]", font_size=34),
            cmath(r"\hat x", r"=", r"\alpha\, x + (1 - \alpha)\, \tilde x, \qquad \alpha \sim U[0, 1]", font_size=34),
        ]
        rows[0][0].set_color(WGAN_C)
        rows[1][4].set_color(C.BITS)
        whys = [why(r"Kantorovich--Rubinstein duality"), why(r"WGAN-GP: \ the gradient penalty"),
                why(r"on random points between real and fake")]
        step = ladder(self, rows, whys, keep=3, top=3.1, x=-1.4, buff=0.6, edge=6.9)
        clipb = VGroup(label(r"WGAN (2017): \ clip every weight to $[-c, c]$", font_size=22, color=GREY_A),
                       label(r"crude: \ capacity is lost, \ or gradients explode", font_size=20, color=GREY_B))
        clipb.arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([-3.4, -2.6, 0])
        gp = VGroup(label(r"Gulrajani et al.\ (2017): \ the optimal critic has slope $1$", font_size=22,
                          color=C.BITS),
                    label(r"along the lines between matched real and fake points", font_size=20, color=GREY_B))
        gp.arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([3.0, -2.6, 0])
        with self.voiceover(
            "Cheapest plans between image distributions are hopeless to compute, but by Kantorovich and "
            "Rubinstein's duality the distance is also the largest gap in expectation that a function of slope at "
            "most one can open between p and q. <bookmark mark='a'/> So a critic f, with any real output, learns to "
            "open the gap, and the generator to close it. <bookmark mark='b'/> The hard part is the slope limit; the "
            "first Wasserstein GAN clipped every weight. <bookmark mark='c'/> Ishaan Gulrajani and colleagues saw "
            "that the optimal critic has slope exactly one between real and fake points, and penalized deviations "
            "there: WGAN-GP."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            self.play(FadeIn(clipb, shift=UP * 0.1))
            vo.wait_until("c")
            step(2)
            self.play(FadeIn(gp, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ring(self):
        g, t = load("gan2d"), load("toys")
        pl = Plane(4.2, center=[-3.4, -0.1, 0])
        truth = VGroup(*[Circle(radius=3 * 0.1 * pl.side / 6, stroke_color=DATA, stroke_width=1.5).move_to(pl.p(*c))
                         for c in np.asarray(t["ring_centers"])])
        head = label(r"WGAN-GP on the ring, \ seed $0$", font_size=22, color=WGAN_C).next_to(pl, UP, buff=0.12)
        kk = label(r"background: \ the critic $f$ \ (bright = high)", font_size=18, color=DISC).next_to(pl, DOWN,
                                                                                                     buff=0.12)
        ml = label(r"modes covered", font_size=22, color=GREY_A).move_to([0.6, 1.8, 0])
        fin = {k: list(g[f"{k}_final_modes"]) for k in ("mm", "ns", "wgan")}
        qual = {k: float(np.mean(g[f"{k}_final_quality"])) for k in ("mm", "ns", "wgan")}
        names = {"mm": (r"minimax", GREY_A), "ns": (r"non-saturating", GAN_C), "wgan": (r"WGAN-GP", WGAN_C)}
        grp = VGroup()
        for row, k in enumerate(("mm", "ns", "wgan")):
            y = 0.6 - 0.75 * row
            nm, col = names[k]
            grp.add(label(nm, font_size=22, color=col).move_to([3.0, y, 0], aligned_edge=RIGHT))
            for s, m in enumerate(fin[k]):
                grp.add(Dot([3.3 + 0.38 * m, y + 0.1 * (s - 2), 0], radius=0.07, color=col))
        axis = VGroup(Line([3.3, -1.75, 0], [6.4, -1.75, 0], color=GREY_C, stroke_width=1.5),
                      *[MathTex(str(m), font_size=20, color=GREY_B).move_to([3.3 + 0.38 * m, -2.0, 0])
                        for m in (0, 4, 8)])
        al = label(r"modes covered at the end: \ $5$ seeds each, \ same networks, \ same generator steps",
                   font_size=18, color=GREY_A).move_to([4.6, 1.5, 0])
        mw, mn, mm = (float(np.mean(fin[k])) for k in ("wgan", "ns", "mm"))
        full_w = sum(1 for m in fin["wgan"] if m == 8)
        if mw > max(mn, mm):
            verdict = (f"Over five seeds, WGAN-GP covers {mw:.1f} of the eight modes on average, all eight in "
                       f"{full_w} runs, against {mn:.1f} for the non-saturating GAN and {mm:.1f} for the minimax "
                       "one: a distance keeps pulling toward every missing mode.")
        else:
            verdict = (f"Over five seeds, WGAN-GP covers {mw:.1f} of the eight modes on average, against {mn:.1f} "
                       f"for the non-saturating GAN and {mm:.1f} for the minimax one: here the distance doesn't buy "
                       "coverage.")
        qw, qn = 100 * qual["wgan"], 100 * qual["ns"]
        sharp = (f"Its samples sit less tightly, though: {qw:.0f} percent within three standard deviations of a "
                 f"mode, against {qn:.0f} for the non-saturating GAN." if qw < qn - 5 else
                 f"And {qw:.0f} percent of its samples sit within three standard deviations of a mode.")
        with self.voiceover(
            "Back to the ring, same networks, same generator steps. The background is now the critic, a landscape "
            "high where the data is. <bookmark mark='a'/> The samples climb it toward the modes. <bookmark "
            f"mark='b'/> {verdict} <bookmark mark='c'/> {sharp}"
        ) as vo:
            self.play(FadeIn(pl), FadeIn(truth), FadeIn(head), FadeIn(kk), FadeIn(ml))
            vo.wait_until("a")
            img, dots, cnt, stp = replay_gan(self, g["wgan_frame_samples"], g["wgan_frame_d"], g["wgan_frame_steps"],
                                             g["wgan_frame_modes"], pl, max(5.0, vo.until("b") + 0.5), [0.6, 1.2, 0],
                                             color=WGAN_C, critic=True)
            vo.wait_until("b")
            self.play(FadeIn(al), FadeIn(axis), LaggedStart(*[FadeIn(d_, scale=1.4) for d_ in grp], lag_ratio=0.05))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def price(self):
        gn, wg = load("gan"), load("wgan")
        sg, sw = int(gn["s0_steps"]), int(wg["s0_steps"])
        fg, fw = float(gn["s0_step_flops"]), float(wg["s0_step_flops"])
        ratio = fw / fg
        rows = VGroup(
            label(rf"one GAN step: \ ${sci(fg, 1)}$ operations", font_size=26, color=GAN_C),
            label(rf"one WGAN-GP step: \ ${sci(fw, 1)}$ \ ($5$ critic updates, \ each with a second backward pass)",
                  font_size=26, color=WGAN_C),
            label(rf"on the same budget: \ ${sg:,}$ generator steps \ against ${sw:,}$".replace(",", "{,}"),
                  font_size=26, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(UP * 0.6)
        tk = take_away(r"A critic that measures distance gives gradients even when nothing overlaps; \ "
                       r"the price is a slower, more careful critic.", font_size=24)
        tg = note(r"computed: \ PyTorch's FLOP counter, \ the digit models").to_corner(DR, buff=0.25)
        with self.voiceover(
            "The cure has a price: five critic updates per generator step, each penalty needing a second backward "
            f"pass. <bookmark mark='a'/> Counted on our digit models, a WGAN-GP step costs {ratio:.1f} GAN steps, "
            f"<bookmark mark='b'/> so on one budget the GAN takes {sg:,} generator steps and WGAN-GP {sw:,}. "
            "Chapter fifteen shows what that buys."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tg))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), FadeIn(tk))
        self.wait(0.3)
        self.clear_scene()
