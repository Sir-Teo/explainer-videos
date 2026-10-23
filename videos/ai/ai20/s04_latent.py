from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai20.common import (DATA, HIST, KLC, LATENT, NOISE, PART, RECON, VAE_C, digit_sheet, load, node_box)


class Latent(VoiceoverScene):
    def construct(self):
        self.card()
        self.model()
        self.helmholtz()
        self.elbo()
        self.reparam()
        self.ours()

    def card(self):
        card = chapter_card(3, r"From Helmholtz machines to the VAE", r"How do you learn a code you never see?",
                            lit=(), part=PART)
        with self.voiceover("Chapter three. From Helmholtz machines to the variational autoencoder."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def model(self):
        vm = load("vae_map")
        grid = np.asarray(vm["grid"]).reshape(-1, 14, 14)
        sheet = digit_sheet(grid, 15, 15, size=0.31, gap=0.02).move_to([3.3, -0.1, 0])
        zp = VGroup(*[Circle(radius=r, stroke_color=LATENT, stroke_width=1.5).set_opacity(0.9 - 0.25 * k)
                      for k, r in enumerate((0.5, 1.0, 1.5))]).move_to([-4.0, -0.1, 0])
        zax = VGroup(Line(zp.get_center() + LEFT * 1.9, zp.get_center() + RIGHT * 1.9, color=GREY_D, stroke_width=1),
                     Line(zp.get_center() + DOWN * 1.9, zp.get_center() + UP * 1.9, color=GREY_D, stroke_width=1))
        zl = MathTex(r"z \sim p(z) = \mathcal N(0, I)", font_size=30, color=LATENT).next_to(zp, UP, buff=0.55)
        dot = Dot(zp.get_center() + np.array([0.6, 0.35, 0]), color=LATENT)
        arr = Arrow(zp.get_right() + RIGHT * 0.5, sheet.get_left() + LEFT * 0.1, buff=0.1, color=VAE_C, stroke_width=3)
        al = MathTex(r"p_\theta(x \mid z)", font_size=30, color=VAE_C).next_to(arr, UP, buff=0.1)
        f = cmath(r"p_\theta(x)", r"=", r"\int", r"p_\theta(x \mid z)", r"\, p(z)", r"\, dz", font_size=40)
        f[3].set_color(VAE_C)
        f[4].set_color(LATENT)
        f.to_edge(UP, buff=0.4)
        post = cmath(r"p_\theta(z \mid x)", r"=", r"\frac{p_\theta(x \mid z)\, p(z)}{p_\theta(x)}", font_size=34)
        post[0].set_color(LATENT)
        post.to_edge(DOWN, buff=0.5).shift(LEFT * 3.4)
        pl = label(r"encoding: \ Bayes' rule, \ the same integral below", font_size=22, color=GREY_A)
        pl.next_to(post, RIGHT, buff=0.4)
        tg = note(r"computed: \ a VAE with a $2$-number code, \ decoding a grid of codes").next_to(sheet, DOWN,
                                                                                                 buff=0.12)
        with self.voiceover(
            "The second answer adds something hidden: every digit comes from a code z, a few numbers drawn from a "
            "plain Gaussian. <bookmark mark='a'/> A decoder turns each code into a distribution over images. Here "
            "is a real one, with a code of two numbers: every point of the plane decodes to a digit, and the digits "
            "flow into one another. <bookmark mark='b'/> An image's probability is then an average over all the "
            "codes that could have made it, an integral we can't compute. <bookmark mark='c'/> And going back, "
            "from image to code, needs Bayes' rule, with the same integral below."
        ) as vo:
            self.play(FadeIn(zax), Create(zp), FadeIn(zl), FadeIn(dot, scale=1.5))
            vo.wait_until("a")
            self.play(GrowArrow(arr), FadeIn(al), FadeIn(sheet), FadeIn(tg))
            self.play(dot.animate.shift(np.array([-1.1, -0.8, 0])), run_time=1.5)
            vo.wait_until("b")
            self.play(Write(f))
            self.play(Indicate(f[2], color=C.SURPRISE))
            vo.wait_until("c")
            self.play(Write(post), FadeIn(pl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def helmholtz(self):
        x = node_box(r"an image $x$", DATA, font_size=26).move_to([-3.7, -1.6, 0])
        z = node_box(r"its causes $z$", LATENT, font_size=26).move_to([-3.7, 1.6, 0])
        up = CurvedArrow(x.get_top() + LEFT * 0.4, z.get_bottom() + LEFT * 0.4, angle=-0.6, color=VAE_C,
                         stroke_width=3)
        dn = CurvedArrow(z.get_bottom() + RIGHT * 0.4, x.get_top() + RIGHT * 0.4, angle=-0.6, color=DATA,
                         stroke_width=3)
        ul = label(r"recognition $q_\phi(z \mid x)$", font_size=22, color=VAE_C).next_to(up, LEFT, buff=0.1)
        dl = label(r"generation $p_\theta(x \mid z)$", font_size=22, color=DATA).next_to(dn, RIGHT, buff=0.1)
        card = history_card(1995, r"Dayan, Hinton, Neal \& Zemel: \ the Helmholtz machine",
                            r"Helmholtz: \ perception is unconscious inference. \ A second network learns to "
                            r"infer the causes $z$ of what is seen.", width=6.6).move_to([3.3, 1.9, 0])
        wake = VGroup(label(r"wake:", font_size=24, color=C.BITS),
                      label(r"see a real $x$, \ infer $z$ with $q$, \ train $p$ to make $x$ from $z$", font_size=22))
        sleep = VGroup(label(r"sleep:", font_size=24, color=C.BITS),
                       label(r"dream $z$, then $x$, from $p$; \ train $q$ to recover $z$", font_size=22))
        for w in (wake, sleep):
            w.arrange(RIGHT, buff=0.2, aligned_edge=UP)
        ws = VGroup(wake, sleep).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.3, -0.6, 0])
        flaw = label(r"the catch: \ $q$ learns from dreams, \ and the two phases optimize different objectives",
                     font_size=22, color=GREY_A).move_to([3.0, -2.3, 0])
        cite_ = cite(r"Hinton, Dayan, Frey \& Neal, \textit{The wake-sleep algorithm} (1995)", corner=DR)
        with self.voiceover(
            "In 1995 Peter Dayan, Geoffrey Hinton, Radford Neal and Richard Zemel proposed learning Bayes' rule: a "
            "second network, a recognition model q, that guesses an image's hidden causes. <bookmark mark='a'/> "
            "The Helmholtz machine, after Hermann von Helmholtz, who called perception unconscious inference. "
            "<bookmark mark='b'/> Awake, it guesses the causes of real images with q, and trains the generator to "
            "reproduce them. <bookmark mark='c'/> Asleep, it dreams causes and images, and trains q to recover the "
            "causes. <bookmark mark='d'/> It worked, awkwardly: q learned from dreams, and the two phases had no "
            "shared objective. Eighteen years later the fix was a single bound."
        ) as vo:
            self.play(FadeIn(x), FadeIn(z), Create(dn), FadeIn(dl))
            self.play(Create(up), FadeIn(ul))
            vo.wait_until("a")
            self.play(FadeIn(card, shift=UP * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(wake), Indicate(up, color=VAE_C))
            vo.wait_until("c")
            self.play(FadeIn(sleep), Indicate(dn, color=DATA))
            vo.wait_until("d")
            self.play(FadeIn(flaw), FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def elbo(self):
        cols = {r"q_\phi(z \mid x)": VAE_C}
        rows = [
            cmath(r"\log p_\theta(x)", r"=", r"\log \int p_\theta(x \mid z)\, p(z)\, dz", font_size=36),
            cmath(r"\log p_\theta(x)", r"=", r"\log \mathbb E_{z \sim q_\phi(z \mid x)}\Big[\frac{p_\theta(x \mid z)\,"
                  r" p(z)}{q_\phi(z \mid x)}\Big]", font_size=36),
            cmath(r"\log p_\theta(x)", r"\ge", r"\mathbb E_{q}\big[\log p_\theta(x \mid z)\big]", r"+",
                  r"\mathbb E_{q}\Big[\log \frac{p(z)}{q_\phi(z \mid x)}\Big]", font_size=36),
            cmath(r"\log p_\theta(x)", r"\ge", r"\mathbb E_{q}\big[\log p_\theta(x \mid z)\big]", r"-",
                  r"\mathrm{KL}\big(q_\phi(z \mid x) \,\|\, p(z)\big)", font_size=36),
            cmath(r"\log p_\theta(x) - \mathrm{ELBO}", r"=", r"\mathrm{KL}\big(q_\phi(z \mid x) \,\|\, "
                  r"p_\theta(z \mid x)\big)", r"\;\ge\; 0", font_size=36),
        ]
        rows[3][2].set_color(RECON)
        rows[3][4].set_color(KLC)
        rows[4][2].set_color(VAE_C)
        whys = [None, why(r"multiply and divide by any $q$"), why(r"Jensen: \ $\log$ is concave"),
                why(r"the evidence lower bound (ELBO)"), why(r"the gap: \ how wrong $q$ is")]
        step = ladder(self, rows, whys, keep=4, top=3.2, x=-1.4, buff=0.45, edge=6.9)
        with self.voiceover(
            "Here is the bound. Start from the log-probability of an image. <bookmark mark='a'/> Multiply and divide "
            "by q of z given x, so the integral becomes an average over codes drawn from q. <bookmark mark='b'/> "
            "The log of an average is at least the average of the log: Jensen. <bookmark mark='c'/> Two terms "
            "remain: a reconstruction, decoding a code drawn from q; and the KL divergence from q to the prior, the "
            "nats the code carries about x, its rate. Together, the evidence lower bound, the ELBO. <bookmark "
            "mark='d'/> The gap is the KL divergence from q to the true posterior, so raising the bound improves "
            "the model and the guesser at once: one objective, where the Helmholtz machine had two."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            br = VGroup(brace_note(rows[3][2], r"reconstruction", color=RECON, font_size=22),
                        brace_note(rows[3][4], r"rate{}", color=KLC, font_size=22))  # own zh key: bare "rate" is 比例
            self.play(FadeOut(whys[3]), FadeIn(br))  # the braces sit where the ELBO's note goes
            self.wait(max(0.5, vo.until("d") - 2.8))
            self.play(FadeOut(br), FadeIn(whys[3]))
            vo.wait_until("d")
            step(4)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def reparam(self):
        x = node_box(r"$x$", DATA, font_size=30, height=0.8).move_to([-6.0, 0.6, 0])
        enc = node_box(r"encoder $\phi$", VAE_C, font_size=26, height=1.0).move_to([-4.0, 0.6, 0])
        mu = node_box(r"$\mu$", VAE_C, font_size=28).move_to([-2.0, 1.3, 0])
        sg = node_box(r"$\sigma$", VAE_C, font_size=28).move_to([-2.0, -0.1, 0])
        eps = node_box(r"$\varepsilon \sim \mathcal N(0, I)$", NOISE, font_size=24).move_to([-2.0, -1.7, 0])
        z = node_box(r"$z = \mu + \sigma \odot \varepsilon$", LATENT, font_size=26, height=0.8).move_to([0.6, 0.6, 0])
        dec = node_box(r"decoder $\theta$", VAE_C, font_size=26, height=1.0).move_to([3.3, 0.6, 0])
        xh = node_box(r"$p_\theta(x \mid z)$", RECON, font_size=26).move_to([5.6, 0.6, 0])
        A = lambda a, b, c=GREY_B: Arrow(a.get_right(), b.get_left(), buff=0.08, color=c, stroke_width=2.5)
        arrs = VGroup(A(x, enc), Arrow(enc.get_right(), mu.get_left(), buff=0.08, color=GREY_B, stroke_width=2.5),
                      Arrow(enc.get_right(), sg.get_left(), buff=0.08, color=GREY_B, stroke_width=2.5),
                      Arrow(mu.get_right(), z.get_left(), buff=0.08, color=GREY_B, stroke_width=2.5),
                      Arrow(sg.get_right(), z.get_left(), buff=0.08, color=GREY_B, stroke_width=2.5),
                      Arrow(eps.get_right(), z.get_bottom() + LEFT * 0.3, buff=0.08, color=NOISE, stroke_width=2.5),
                      A(z, dec), A(dec, xh))
        grad = Arrow(xh.get_bottom() + DOWN * 0.3, enc.get_bottom() + DOWN * 0.3, buff=0, color=C.SCORE,
                     stroke_width=3, path_arc=-0.5)
        gl = label(r"gradients flow back through $\mu$ and $\sigma$: \ the noise is just an input", font_size=20,
                   color=C.SCORE).move_to([2.7, -1.75, 0])
        kl = cmath(r"\mathrm{KL}\big(\mathcal N(\mu, \sigma^2) \,\|\, \mathcal N(0, 1)\big)", r"=",
                   r"\tfrac12\big(\mu^2 + \sigma^2 - \log \sigma^2 - 1\big)", font_size=30).to_edge(UP, buff=0.35)
        kl[0].set_color(KLC)
        h1 = history_card(2013, r"Kingma \& Welling", r"\textit{Auto-Encoding Variational Bayes}", width=4.4,
                          font_size=20).to_corner(DL, buff=0.3)
        h2 = history_card(2014, r"Rezende, Mohamed \& Wierstra", r"\textit{Stochastic Backpropagation}", width=4.4,
                          font_size=20).to_corner(DR, buff=0.3)
        with self.voiceover(
            "One problem remains: you can't take the gradient of a coin toss. <bookmark mark='a'/> So move the "
            "randomness: the encoder outputs a mean and a spread, and the code is the mean plus the spread times "
            "fresh noise. <bookmark mark='b'/> The noise is now just an input, and gradients flow back into the "
            "encoder: the reparameterization trick. <bookmark mark='c'/> For Gaussians, the KL term has a closed "
            "form. <bookmark mark='d'/> Diederik Kingma and Max Welling published this in December 2013, and "
            "Danilo Rezende, Shakir Mohamed and Daan Wierstra, independently, weeks later: the variational "
            "autoencoder."
        ) as vo:
            self.play(FadeIn(x), FadeIn(enc), GrowArrow(arrs[0]))
            vo.wait_until("a")
            self.play(FadeIn(mu), FadeIn(sg), GrowArrow(arrs[1]), GrowArrow(arrs[2]), FadeIn(eps))
            self.play(FadeIn(z), *[GrowArrow(a_) for a_ in arrs[3:6]])
            vo.wait_until("b")
            self.play(GrowArrow(arrs[6]), FadeIn(dec), GrowArrow(arrs[7]), FadeIn(xh))
            self.play(Create(grad), FadeIn(gl))
            vo.wait_until("c")
            self.play(Write(kl))
            vo.wait_until("d")
            self.play(FadeIn(h1, shift=UP * 0.1), FadeIn(h2, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ours(self):
        v = load("vae")
        p = int(v["s0_params"])
        card = definition_card(r"our VAE", rf"encoder: \ $196 \to 512 \to 512 \to$ a mean and a spread for each of "
                               rf"$16$ code numbers. \ Decoder: \ $16 \to 512 \to 512 \to$ for every pixel, a "
                               rf"logistic distribution cut into the $16$ grey levels. \ ${p:,}$ parameters."
                               .replace(",", "{,}"), width=8.6, font_size=24, kind=r"Architecture")
        card.move_to(UP * 0.9)
        why_ = VGroup(
            label(r"a proper likelihood on the $16$ levels: \ the ELBO in bits per pixel, \ like PixelCNN's",
                  font_size=24, color=GREY_A),
            label(rf"trained on the same budget, \ three seeds; \ $q$'s guess checked by a tighter bound",
                  font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(card, DOWN, buff=0.5)
        cite_ = cite(r"discretized logistic: \ Salimans et al., \textit{PixelCNN++} (2017)", corner=DR)
        with self.voiceover(
            "Ours has a sixteen-number code, and a decoder that gives every pixel a bell-shaped distribution cut "
            f"into the sixteen grey levels: {p:,} parameters. <bookmark mark='a'/> So its bound is in the PixelCNN's "
            "units, bits per pixel."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.15), FadeIn(cite_))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(w, shift=UP * 0.1) for w in why_], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()
