from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai21.common import DATA, NOISE, PART, SCORE, Panel, load

COL = {r"\varepsilon": NOISE, r"\hat\varepsilon_\theta": SCORE, r"x_0": DATA}


class ELBO(VoiceoverScene):
    def construct(self):
        self.card()
        self.bound()
        self.noise()
        self.weights()
        self.replay()

    def card(self):
        card = chapter_card(2, r"The bound, and guessing the noise", r"What exactly should the network learn?", part=PART)
        with self.voiceover("Chapter two. The bound, and guessing the noise."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def chain_picture(self):
        names = [r"x_0", r"x_1", r"\cdots", r"x_{t-1}", r"x_t", r"\cdots", r"x_T"]
        nodes = VGroup(*[MathTex(n, font_size=34, color=DATA if n == r"x_0" else (NOISE if n == r"x_T" else WHITE))
                         for n in names]).arrange(RIGHT, buff=0.85).move_to([0, 2.95, 0])
        fw = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.1, color=GREY_B, stroke_width=2.5,
                            max_tip_length_to_length_ratio=0.25).shift(UP * 0.13) for a, b in zip(nodes, nodes[1:])])
        bw = VGroup(*[Arrow(b.get_left(), a.get_right(), buff=0.1, color=SCORE, stroke_width=2.5,
                            max_tip_length_to_length_ratio=0.25).shift(DOWN * 0.13) for a, b in zip(nodes, nodes[1:])])
        lq = label(r"$q$: \ fixed noise", font_size=20, color=GREY_B).next_to(fw, UP, buff=0.05).align_to(nodes, RIGHT)
        lp = label(r"$p_\theta$: \ learned, \ each step $\mathcal N(\mu_\theta(x_t, t),\ \sigma_t^2 I)$", font_size=20,
                   color=SCORE).next_to(bw, DOWN, buff=0.05).align_to(nodes, LEFT)
        return VGroup(nodes, fw, bw, lq, lp)

    def bound(self):
        pic = self.chain_picture()
        rows = [
            cmath(r"-\log p_\theta(x_0)", r"\le", r"\mathcal L", r"= \mathbb E_q\Big[-\log \frac{p_\theta(x_{0:T})}"
                  r"{q(x_{1:T} \mid x_0)}\Big]", font_size=32),
            cmath(r"\mathcal L", r"=", r"\mathbb E_q\Big[-\log p(x_T) - \sum_{t \ge 1} \log \frac{p_\theta(x_{t-1} \mid x_t)}"
                  r"{q(x_t \mid x_{t-1})}\Big]", font_size=32),
            cmath(r"\mathcal L", r"=", r"\underbrace{\mathrm{KL}\big(q(x_T \mid x_0) \,\|\, p(x_T)\big)}_{\approx\, 0} + "
                  r"\sum_{t > 1} \mathrm{KL}\big(q(x_{t-1} \mid x_t, x_0) \,\|\, p_\theta(x_{t-1} \mid x_t)\big)"
                  r" - \log p_\theta(x_0 \mid x_1)", font_size=28),
        ]
        whys = [why(r"Jensen, \ as for the VAE \ (Part 20)"), why(r"both chains are products of their steps"),
                why(r"Bayes on each step, \ given $x_0$; \ the jumps cancel in pairs")]
        step = ladder(self, rows, whys, keep=3, top=1.75, x=-2.6, buff=0.62, edge=6.85)
        with self.voiceover(
            "Part 20's variational autoencoder had a code and a bound. Here the codes are the noisy versions, x one "
            "to x T, and the encoder is the forward process, fixed. <bookmark mark='a'/> The decoder runs the chain "
            "backwards, each step a Gaussian whose mean a network chooses. Jensen's inequality gives the same bound "
            "on the log-likelihood as before. <bookmark mark='b'/> Both chains are products of their steps, so the "
            "bound is a sum over steps. <bookmark mark='c'/> Now use the last chapter's fact: rewrite each forward "
            "step by Bayes, given the clean point. The extra jumps cancel in pairs, and what is left is a sum of "
            "KL divergences, one per step: how far the network's step back is from the true step back, given the "
            "clean point."
        ) as vo:
            self.play(FadeIn(pic[0]), LaggedStart(*[GrowArrow(a) for a in pic[1]], lag_ratio=0.1), FadeIn(pic[3]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a) for a in pic[2]], lag_ratio=0.1), FadeIn(pic[4]))
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def noise(self):
        rows = [
            cmath(r"\mathrm{KL}_t", r"=", r"\frac{1}{2\sigma_t^2}\, \big\| \tilde\mu_t - \mu_\theta(x_t, t) \big\|^2", font_size=34),
            cmath(r"\tilde\mu_t", r"=", r"\frac{1}{\sqrt{1-\beta_t}}\Big(x_t - \frac{\beta_t}{\sqrt{1-\bar\alpha_t}}\,",
                  r"\varepsilon", r"\Big)", colors=COL, font_size=34),
            cmath(r"\mu_\theta", r"=", r"\frac{1}{\sqrt{1-\beta_t}}\Big(x_t - \frac{\beta_t}{\sqrt{1-\bar\alpha_t}}\,",
                  r"\hat\varepsilon_\theta(x_t, t)", r"\Big)", colors=COL, font_size=34),
            cmath(r"\mathrm{KL}_t", r"=", r"\lambda_t\, \big\|", r"\varepsilon", r"-", r"\hat\varepsilon_\theta(x_t, t)",
                  r"\big\|^2, \qquad \lambda_t = \frac{\beta_t^2}{2\sigma_t^2 (1-\beta_t)(1-\bar\alpha_t)}", colors=COL,
                  font_size=32),
        ]
        whys = [why(r"two Gaussians, \ the same variance"),
                why(r"put $x_0 = (x_t - \sqrt{1-\bar\alpha_t}\,\varepsilon)/\sqrt{\bar\alpha_t}$ into $\tilde\mu_t$"),
                why(r"so let the network guess $\varepsilon$"), why(r"the means differ only in the noise")]
        step = ladder(self, rows, whys, keep=4, top=2.7, x=-2.3, buff=0.55, edge=6.85)
        cite_ = cite(r"J.~Ho, A.~Jain \& P.~Abbeel, \textit{Denoising Diffusion Probabilistic Models} (2020)", corner=DR)
        with self.voiceover(
            "Each term compares two Gaussians with the same variance, so it is just the squared distance between "
            "their means. <bookmark mark='a'/> Write the true mean in terms of the noisy point and the noise that "
            "made it, by substituting for the clean point. <bookmark mark='b'/> That suggests the parameterization "
            "Ho, Jain and Abbeel chose in 2020: let the network output a guess of the noise, and build its mean the "
            "same way. <bookmark mark='c'/> Then each term of the bound is a weight lambda t times the squared error "
            "of the noise guess. Training a diffusion model is a regression: look at a noisy point, say what noise "
            "was added."
        ) as vo:
            self.play(FadeIn(cite_))
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def weights(self):
        f = load("forward")
        lam = np.asarray(f["lam"])
        T = len(lam)
        lo, hi = math.floor(math.log10(lam.min())), math.ceil(math.log10(lam.max()))
        g = axes([0, T], [lo, hi], x_length=6.6, y_length=3.6, xlabel=r"step $t$",
                 ylabel=r"the bound's weight $\lambda_t$ on the noise guess (log scale)", xticks=[0, 500, 1000],
                 yticks=list(range(lo, hi + 1)), yfmt=lambda v: f"10^{{{int(v)}}}", center=[-2.6, -0.2, 0])
        g_shift = RIGHT * 2.6  # the chart starts in the middle, and slides left for the card
        ts = np.arange(1, T + 1)
        cw = curve(g.ax, ts[::4], np.log10(lam[::4]), SCORE, 3.5)
        flat = DashedLine(g.ax.c2p(0, math.log10(np.median(lam))), g.ax.c2p(T, math.log10(np.median(lam))), color=GREY_B,
                          stroke_width=2)
        fl = label(r"dashed: \ $L_{\text{simple}}$, \ every step weighted alike", font_size=22, color=GREY_B)
        fl.move_to(g.ax.c2p(0.6 * T, lo + 0.8 * (hi - lo)))
        card = definition_card(r"the simple loss", VGroup(
            MathTex(r"L_{\text{simple}} = \mathbb E_{t,\, x_0,\, \varepsilon}\, \big\|\varepsilon - \hat\varepsilon_\theta"
                    r"\big(\sqrt{\bar\alpha_t}\, x_0 + \sqrt{1-\bar\alpha_t}\, \varepsilon,\ t\big)\big\|^2", font_size=26),
            label(r"$t$ uniform; \ the weights $\lambda_t$ dropped", font_size=20, color=GREY_A),
            label(r"DDPM, CIFAR-10: \ FID $3.17$", font_size=20, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.15),
            width=5.6, color=SCORE).move_to([3.7, 0.2, 0])
        ratio = lam[0] / lam[-1]
        with self.voiceover(
            f"How big are the weights? For DDPM's schedule, with the step's variance set to beta, lambda falls from "
            f"{lam[0]:.2f} at the first step to {lam[-1]:.3f} at the last, a factor of {ratio:.0f}: the bound cares "
            "most about the nearly clean steps. <bookmark mark='a'/> Ho and colleagues found that dropping the weights "
            "altogether, every step counted the same, gave better pictures: an FID of 3.17 on CIFAR-10, the best of its "
            "day. <bookmark mark='b'/> That is the simple loss, and almost every diffusion model since has trained on a "
            "loss like it. The exact weighting returns in chapter seven: it is a choice of which noise levels to "
            "practise most."
        ) as vo:
            VGroup(g, cw).shift(g_shift)
            self.play(FadeIn(g), Create(cw), run_time=1.6)
            vo.wait_until("a")
            self.play(VGroup(g, cw).animate.shift(-g_shift), run_time=0.8)
            self.play(Create(flat), FadeIn(fl), FadeIn(card, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(Indicate(card.body[0], color=SCORE))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        """How the denoiser learns: the same noise, sampled at checkpoints during training, beside the loss."""
        d = load("denoiser")
        checks = [int(c) for c in d["checks"]]
        snaps = np.asarray(d["snaps"])
        L = np.asarray(d["losses"])
        sw = [float(v) for v in d["snap_sw"]]
        pn = Panel(6.0, center=[-3.3, -0.3, 0])
        pts = pn.dots(snaps[0], DATA, radius=0.022)
        top = float(np.percentile(L[:, 1], 99)) * 1.05
        L = np.stack([L[:, 0], np.minimum(L[:, 1], top)], 1)  # the first few losses run off the top: drawn at it
        g = axes([0, checks[-1]], [0, top], x_length=4.8, y_length=2.8, xlabel=r"training step",
                 ylabel=r"the simple loss", xticks=[0, checks[-1]], yticks=[0, round(top, 1)], center=[3.6, 0.5, 0])
        tk = ValueTracker(0)
        dot = always_redraw(lambda: Dot(g.ax.c2p(tk.get_value(), float(np.interp(tk.get_value(), L[:, 0], L[:, 1]))),
                                        radius=0.07, color=SCORE))
        cnt = always_redraw(lambda: MathTex(rf"\text{{step }}{int(tk.get_value()):,}".replace(",", "{,}"), font_size=28,
                                            color=SCORE).next_to(pn, UP, buff=0.12))
        swl = always_redraw(lambda: label(rf"distance from the data: \ ${np.interp(tk.get_value(), checks, sw):.2f}$",
                                          font_size=20, color=DATA).next_to(pn, DOWN, buff=0.12))
        tag = label(rf"${len(snaps[0])}$ points from the same noise, \\ drawn with $50$ DDIM steps at each checkpoint",
                    font_size=18, color=GREY_A).next_to(g, DOWN, buff=0.4)
        k1 = 1 if len(checks) > 2 else len(checks) - 1
        l1 = float(np.interp(checks[k1], L[:, 0], L[:, 1]))
        drop = (L[0, 1] - l1) / max(L[0, 1] - L[-1, 1], 1e-9)
        pct = 100 * min(drop, 1)
        # the first checkpoint whose points are within 60 percent of the final distance: the letters can be read
        ks = next(k for k in range(k1, len(checks)) if sw[k] < 1.6 * sw[-1])
        ks = min(max(ks, k1 + 1), len(checks) - 2)  # strictly between the blob and the end
        if drop > 0.5:
            early = (f"Within {checks[k1]} steps the loss has made {pct:.0f} percent of its whole fall, and the "
                     f"points have pulled in to a blob, {sw[k1]:.2f} from the data. ")
        else:
            early = (f"Within {checks[k1]} steps the points have pulled in to a blob, {sw[k1]:.2f} from the data, "
                     "and the loss is still falling. ")
        if any(b > a + 0.005 for a, b in zip(sw[ks:], sw[ks + 1:])):
            trend = "on the whole, if not at every checkpoint"
        else:
            trend = "at every checkpoint"
        s_read, s_end, c_read = sw[ks], sw[-1], checks[ks]
        with self.voiceover(
            "Here is our own denoiser learning on the letters, trained with the simple loss, a noise level drawn at "
            "random for each of its examples. At each checkpoint we stop, and draw points from the same noise. "
            "<bookmark mark='a'/> Untrained, it flings them to the edges. <bookmark mark='b'/> " + early
            + f"<bookmark mark='c'/> By step {c_read:,} the letters can be read. The rest is refinement: the loss "
            f"barely moves, but the strokes sharpen, the distance from the data going from {s_read:.2f} to "
            f"{s_end:.2f}, {trend}. Every step of training only asked for the noise in one blurred point; the "
            "letters emerge from millions of those guesses."
        ) as vo:
            self.play(FadeIn(pn), FadeIn(pts), FadeIn(g), FadeIn(tag))
            self.add(dot, cnt, swl)
            vo.wait_until("a")
            marks = {k1: "b", ks: "c"}
            for k in range(1, len(checks)):
                if k in marks:
                    vo.wait_until(marks[k])
                seg = [g.ax.c2p(a, b) for a, b in L if checks[k - 1] <= a <= checks[k]]
                anims = [tk.animate.set_value(checks[k]), *pn.move(pts, snaps[k])]
                if len(seg) > 1:
                    anims.append(Create(VMobject(color=SCORE, stroke_width=3).set_points_as_corners(seg)))
                self.play(*anims, run_time=1.4)
        self.wait(0.3)
        for m in (dot, cnt, swl):
            m.clear_updaters()
        self.clear_scene()
