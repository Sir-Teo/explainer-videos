from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai22.common import PATCH, gray_image, load

TXT = C.TRUE_P
UNI, LN = GREY_B, C.SURPRISE  # uniform and logit-normal noise levels


def straight_lines() -> VGroup:
    """Rectified flow: each noise point joined to a data point by a straight line, followed at a steady speed."""
    noise = np.array([[-1.7, 0.8], [-1.35, 0.35], [-1.9, -0.05], [-1.5, -0.45], [-1.8, -0.85]])
    data = np.array([[1.3, 0.75], [1.75, 0.3], [1.2, -0.1], [1.9, -0.4], [1.4, -0.8]])
    out = VGroup()
    for a, b in zip(noise, data):
        out.add(Line([*a, 0], [*b, 0], color=GREY_B, stroke_width=1.5),
                Dot([*a, 0], radius=0.06, color=C.TRUE_P), Dot([*b, 0], radius=0.06, color=C.BITS))
    out.add(label(r"noise", font_size=20, color=C.TRUE_P).next_to(out, LEFT, buff=0.15),
            label(r"data", font_size=20, color=C.BITS).next_to(out, RIGHT, buff=0.15))
    return out


class SD3(VoiceoverScene):
    def construct(self):
        self.card()
        self.mmdit()
        self.timesteps()
        self.shift()

    def card(self):
        card = chapter_card(4, r"Rectified flow at scale", r"What changes when the pictures get big?", lit=(2024,), part=22)
        with self.voiceover("Chapter four. Rectified flow at scale."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def mmdit(self):
        nt, ni = 4, 6
        txt = VGroup(*[Square(0.34, stroke_color=TXT, stroke_width=1.5, fill_color=TXT, fill_opacity=0.2) for _ in range(nt)])
        img = VGroup(*[Square(0.34, stroke_color=PATCH, stroke_width=1.5, fill_color=PATCH, fill_opacity=0.2) for _ in range(ni)])
        for g_ in (txt, img):
            g_.arrange(RIGHT, buff=0.06)
        seq = VGroup(txt, img).arrange(RIGHT, buff=0.3).move_to([-3.4, 1.9, 0])
        tl = label(r"the prompt's tokens", font_size=20, color=TXT).next_to(txt, UP, buff=0.15)
        il = label(r"the picture's patches", font_size=20, color=PATCH).next_to(img, UP, buff=0.15)
        # separate weights for each kind, one attention over both
        wq = VGroup(MathTex(r"W^{\text{text}}_{Q,K,V}", font_size=26, color=TXT).next_to(txt, DOWN, buff=0.35),
                    MathTex(r"W^{\text{image}}_{Q,K,V}", font_size=26, color=PATCH).next_to(img, DOWN, buff=0.35))
        eq = MathTex(r"\operatorname{softmax}\!\Big(\frac{[Q_{\text{t}}; Q_{\text{i}}]\,[K_{\text{t}}; K_{\text{i}}]^{\top}}{\sqrt{d}}\Big)"
                     r"\,[V_{\text{t}}; V_{\text{i}}]", font_size=30).move_to([-3.4, -0.2, 0])
        el = label(r"one attention over the joined sequence", font_size=20, color=GREY_A).next_to(eq, DOWN, buff=0.15)
        # the attention pattern, in blocks: text-text, text-image, image-text, image-image (schematic)
        n = nt + ni
        cell = 0.36
        blocks = VGroup()
        names = {(0, 0): r"text $\to$ text", (0, 1): r"text $\to$ image", (1, 0): r"image $\to$ text", (1, 1): r"image $\to$ image"}
        for a in range(2):
            for b in range(2):
                h = (nt if a == 0 else ni) * cell
                w = (nt if b == 0 else ni) * cell
                col = TXT if b == 0 else PATCH
                r_ = Rectangle(width=w, height=h, stroke_color=GREY_C, stroke_width=1.5, fill_color=col, fill_opacity=0.18 + 0.12 * (a == b))
                blocks.add(VGroup(r_, label(names[(a, b)], font_size=16, color=WHITE).move_to(r_)))
        x0, y0 = 1.6, 2.4
        for k, (a, b) in enumerate(((0, 0), (0, 1), (1, 0), (1, 1))):
            blk = blocks[k]
            ox = x0 + (0 if b == 0 else nt * cell)
            oy = y0 - (0 if a == 0 else nt * cell)
            blk.move_to([ox + blk.width / 2, oy - blk.height / 2, 0])
        bl = label(r"who looks at whom \ (schematic): \\ every block is learned", font_size=20, color=GREY_A).next_to(blocks, DOWN, buff=0.2)
        sizes = label(r"Stable Diffusion 3: \ $2$ and $8$ billion parameters; \ FLUX.1: \ $12$ billion \ (as published)",
                      font_size=22, color=GREY_A).to_edge(DOWN, buff=0.45)
        cite_ = cite(r"P.~Esser et al., \textit{Scaling Rectified Flow Transformers for High-Resolution Image Synthesis} (2024)", corner=UR)
        rf = gloss(r"rectified flow", r"Part 21's flow matching: \ straight lines \\ from noise to data",
                   straight_lines(), corner=DR, width=4.4, color=C.BITS)
        with self.voiceover(
            "Rectified flow, in this chapter's title, is part twenty-one's flow matching: straight lines from noise "
            "to data. <bookmark mark='r'/> Our model was told which letter to draw by one number. A real model is told by a prompt, a sentence of "
            "tokens. Stable Diffusion 3 put the prompt's tokens and the picture's patches into one sequence. "
            "<bookmark mark='a'/> Each kind keeps its own weights for queries, keys and values, since words and "
            "patches are different things; <bookmark mark='b'/> then a single attention runs over the joined "
            "sequence. <bookmark mark='c'/> So every patch can look at every word, every word at every patch, and "
            "the text is updated by the picture as the picture is drawn. Scaled up, that's Stable Diffusion 3, and "
            "FLUX, with twelve billion parameters."
        ) as vo:
            self.play(FadeIn(rf, shift=UP * 0.2))
            vo.wait_until("r")
            self.play(FadeOut(rf), FadeIn(cite_), FadeIn(seq), FadeIn(tl), FadeIn(il))
            vo.wait_until("a")
            self.play(FadeIn(wq))
            vo.wait_until("b")
            self.play(Write(eq), FadeIn(el))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in blocks], lag_ratio=0.25), FadeIn(bl), run_time=2.0)
            self.play(FadeIn(sizes))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def timesteps(self):
        v = load("vae")
        # left: the two ways to draw the noise level for training
        ax = CornerAxes(x_range=[0, 1, 0.5], y_range=[0, 1.8, 0.5], x_length=4.8, y_length=2.8, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-3.6, 0.3, 0])

        def ln(t):
            return math.exp(-math.log(t / (1 - t)) ** 2 / 2) / (math.sqrt(2 * math.pi) * t * (1 - t))

        uni = ax.plot(lambda t: 1.0, x_range=[0.0, 1.0, 0.01], color=UNI, stroke_width=3.5)
        lnc = ax.plot(ln, x_range=[0.005, 0.995, 0.005], color=LN, stroke_width=3.5)
        xt = VGroup(*[MathTex(s_, font_size=20, color=GREY_B).next_to(ax.c2p(x, 0), DOWN, buff=0.08)
                      for x, s_ in ((0, "0"), (0.5, "0.5"), (1, "1"))])
        xn = label(r"$t$: \ noise $\to$ data", font_size=20, color=GREY_A).next_to(xt, DOWN, buff=0.08)
        yn = label(r"how often each $t$ is trained", font_size=20, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        ku = label(r"uniform", font_size=20, color=UNI).next_to(ax.c2p(1, 1), UR, buff=0.05)
        kl = label(r"logit-normal", font_size=20, color=LN).next_to(ax.c2p(0.62, ln(0.62)), UR, buff=0.08)
        f = MathTex(r"t = \sigma(u), \quad u \sim \mathcal{N}(0, 1)", font_size=30, color=LN).next_to(ax, DOWN, buff=0.75)
        fd = MathTex(r"\pi(t) = \frac{1}{\sqrt{2\pi}}\,\frac{1}{t(1-t)}\, e^{-\frac12\left(\log\frac{t}{1-t}\right)^2}",
                     font_size=28, color=LN).next_to(f, DOWN, buff=0.2)
        # right: our letters, trained both ways, sampled with 1 to 40 steps
        ks = [int(k) for k in v["ts_steps"]]
        cu, cl = np.asarray(v["ts_uniform"], float), np.asarray(v["ts_logit-normal"], float)
        bx = CornerAxes(x_range=[0, math.log2(ks[-1]), 1], y_range=[0, 1, 0.5], x_length=4.8, y_length=3.2, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([3.4, 0.0, 0])
        bxt = VGroup(*[MathTex(str(k), font_size=20, color=GREY_B).next_to(bx.c2p(math.log2(k), 0), DOWN, buff=0.08) for k in ks])
        byt = VGroup(*[MathTex(rf"{int(100 * y)}\%", font_size=20, color=GREY_B).next_to(bx.c2p(0, y), LEFT, buff=0.08) for y in (0, 0.5, 1)])
        bxn = label(r"sampling steps", font_size=20, color=GREY_A).next_to(bxt, DOWN, buff=0.08)
        byn = label(r"generated letters the judge reads", font_size=20, color=GREY_A).next_to(bx, UP, buff=0.12).align_to(bx, LEFT)
        lk = [math.log2(k) for k in ks]
        lu = VGroup(VMobject(color=UNI, stroke_width=3.5).set_points_as_corners([bx.c2p(a, b) for a, b in zip(lk, cu)]),
                    *[Dot(bx.c2p(a, b), radius=0.05, color=UNI) for a, b in zip(lk, cu)])
        ll = VGroup(VMobject(color=LN, stroke_width=3.5).set_points_as_corners([bx.c2p(a, b) for a, b in zip(lk, cl)]),
                    *[Dot(bx.c2p(a, b), radius=0.05, color=LN) for a, b in zip(lk, cl)])
        better = float(np.mean(cl - cu))
        few = int(np.argmax(cl - cu))
        cite_ = cite(r"P.~Esser et al.\ (2024): \ logit-normal sampling of $t$", corner=UR)
        with self.voiceover(
            "Stable Diffusion 3 also changed which noise levels it trains on. <bookmark mark='a'/> Part twenty-one drew "
            "the time t uniformly. But near pure noise, the best guess is just the average picture, and near the "
            "data there's almost nothing left to fix. The hard part is the middle. <bookmark mark='b'/> So draw a "
            "normal number and squash it with a sigmoid: the logit-normal, which trains most in the middle. "
            "<bookmark mark='c'/> We trained our latent letters both ways. "
            + (f"The logit-normal model reads better, by {100 * better:.0f} points on average, most at {ks[few]} "
               "steps." if better > 0.01 else
               f"Here, uniform does better, by {-100 * better:.0f} points on average: on letters this small, the "
               "middle isn't where the difficulty is. On large pictures, the paper found logit-normal among the best "
               "of the many options it compared." if better < -0.01 else
               "On letters this small, the choice barely matters; on large pictures, the paper found logit-normal "
               "among the best of the many options it compared.")
        ) as vo:
            self.play(FadeIn(cite_), Create(ax), FadeIn(xt), FadeIn(xn), FadeIn(yn))
            vo.wait_until("a")
            self.play(Create(uni), FadeIn(ku))
            vo.wait_until("b")
            self.play(Create(lnc), FadeIn(kl), Write(f), run_time=1.5)
            self.play(FadeIn(fd))
            vo.wait_until("c")
            self.play(Create(bx), FadeIn(bxt), FadeIn(byt), FadeIn(bxn), FadeIn(byn))
            self.play(Create(lu[0]), FadeIn(lu[1:]), Create(ll[0]), FadeIn(ll[1:]), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def shift(self):
        d = load("latent")
        x = np.asarray(d["orig"])[0]  # a 20 x 20 letter, 0..1
        g = np.random.default_rng(3)
        sig = 0.75
        small = x + sig * g.normal(size=x.shape)
        big = np.kron(x, np.ones((4, 4)))  # the same letter with 16 times the pixels
        bign = big + sig * g.normal(size=big.shape)
        pooled = bign.reshape(20, 4, 20, 4).mean((1, 3))
        left = float(np.std(pooled - x))  # noise left after averaging each 4 x 4 block
        S = 2.0
        ims = Group(gray_image(small, S), gray_image(bign, S), gray_image(pooled, S)).arrange(RIGHT, buff=0.7).move_to([-2.3, 1.2, 0])
        cap = VGroup(label(rf"$20 \times 20$, \ noise ${sig}$", font_size=20, color=GREY_A),
                     label(rf"$80 \times 80$, \ the same noise", font_size=20, color=GREY_A),
                     label(rf"its $4 \times 4$ averages: \ noise ${left:.2f}$", font_size=20, color=PATCH))
        for c_, im in zip(cap, ims):
            c_.next_to(im, DOWN, buff=0.15)
        # the shift: more pixels, so push the noise levels up
        ax = CornerAxes(x_range=[0, 1, 0.5], y_range=[0, 1, 0.5], x_length=3.0, y_length=3.0, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([5.0, 1.2, 0])
        al = [1, 2, 3, 4]
        cols = [GREY_B, C.TRUE_P, C.SURPRISE, C.BITS]
        cs = VGroup(*[ax.plot(lambda s_, a=a: a * s_ / (1 + (a - 1) * s_), x_range=[0, 1, 0.01], color=c_, stroke_width=3)
                      for a, c_ in zip(al, cols)])
        kl = VGroup(*[MathTex(rf"\alpha = {a}", font_size=20, color=c_) for a, c_ in zip(al, cols)]).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
        kl.next_to(ax.c2p(0.55, 0.35), DR, buff=0.05)
        axl = VGroup(label(r"noise level $\sigma$", font_size=18, color=GREY_A).next_to(ax, DOWN, buff=0.1),
                     label(r"shifted $\sigma'$", font_size=18, color=GREY_A).next_to(ax, UP, buff=0.1))
        f = MathTex(r"\sigma' = \frac{\alpha\,\sigma}{1 + (\alpha - 1)\,\sigma}, \qquad \alpha = \sqrt{\frac{\text{pixels}}{\text{base pixels}}}",
                    font_size=32).move_to([0, -2.1, 0])
        fl = label(r"$\sigma = 1 - t$: \ the share of noise. \ Stable Diffusion 3 at $1024^2$: \ $\alpha = 3$ \ (as published)",
                   font_size=20, color=GREY_A).next_to(f, DOWN, buff=0.2)
        with self.voiceover(
            "One more thing changes with size. <bookmark mark='a'/> Add the same noise to a small picture and to the "
            "same picture with sixteen times the pixels. <bookmark mark='b'/> The big one looks clearer, and it is: "
            f"average each four by four block, and the noise falls from {sig} to {left:.2f}, about a quarter, while "
            "the letter stays. Neighbouring pixels share their information, so at high resolution a given noise "
            "level destroys less, and a model trained on small pictures spends its time on noise levels that are "
            "too easy. <bookmark mark='c'/> So Stable Diffusion 3 shifts the noise schedule, the plan of how much noise there is at each "
            "time t, toward noise, by a factor alpha "
            "that grows like the square root of the pixel count."
        ) as vo:
            self.play(FadeIn(ims[0]), FadeIn(cap[0]))
            vo.wait_until("a")
            self.play(FadeIn(ims[1]), FadeIn(cap[1]))
            vo.wait_until("b")
            self.play(FadeIn(ims[2]), FadeIn(cap[2]))
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(axl), LaggedStart(*[Create(c_) for c_ in cs], lag_ratio=0.2), FadeIn(kl), run_time=2.0)
            self.play(Write(f), FadeIn(fl))
        self.wait(0.3)
        self.clear_scene()
