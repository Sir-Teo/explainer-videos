from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai22.common import HIST, PART, PATCH, TXT, gray_image, load, mean_band

UNI, LN = GREY_B, C.SURPRISE  # uniform and logit-normal noise levels
RES_C = {20: GREY_B, 40: C.TRUE_P, 80: C.BITS}


class SD3(VoiceoverScene):
    def construct(self):
        self.card()
        self.mmdit()
        self.timesteps()
        self.derive()
        self.check()
        self.flux()

    def card(self):
        card = chapter_card(8, r"Stable Diffusion 3 and Flux", r"What changes when the pictures get big?", part=PART)
        with self.voiceover("Chapter eight. Stable Diffusion 3 and Flux."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def mmdit(self):
        nt, ni = 4, 6
        txt = VGroup(*[Square(0.34, stroke_color=TXT, stroke_width=1.5, fill_color=TXT, fill_opacity=0.2) for _ in range(nt)])
        img = VGroup(*[Square(0.34, stroke_color=PATCH, stroke_width=1.5, fill_color=PATCH, fill_opacity=0.2) for _ in range(ni)])
        for g_ in (txt, img):
            g_.arrange(RIGHT, buff=0.06)
        seq = VGroup(txt, img).arrange(RIGHT, buff=0.3).move_to([-3.4, 2.0, 0])
        tl = label(r"the prompt's tokens", font_size=20, color=TXT).next_to(txt, UP, buff=0.15)
        il = label(r"the picture's patches", font_size=20, color=PATCH).next_to(img, UP, buff=0.15)
        wq = VGroup(MathTex(r"W^{\text{text}}_{Q,K,V}", font_size=26, color=TXT).next_to(txt, DOWN, buff=0.35),
                    MathTex(r"W^{\text{image}}_{Q,K,V}", font_size=26, color=PATCH).next_to(img, DOWN, buff=0.35))
        eq = MathTex(r"\operatorname{softmax}\!\Big(\frac{[Q_{\text{t}}; Q_{\text{i}}]\,[K_{\text{t}}; K_{\text{i}}]^{\top}}{\sqrt{d}}\Big)"
                     r"\,[V_{\text{t}}; V_{\text{i}}]", font_size=30).move_to([-3.4, 0.1, 0])
        el = label(r"one attention over the joined sequence", font_size=20, color=GREY_A).next_to(eq, DOWN, buff=0.15)
        blocks = VGroup()
        names = {(0, 0): r"text $\to$ text", (0, 1): r"text $\to$ image", (1, 0): r"image $\to$ text",
                 (1, 1): r"image $\to$ image"}
        cell = 0.36
        for a in range(2):
            for b in range(2):
                h = (nt if a == 0 else ni) * cell
                w = (nt if b == 0 else ni) * cell
                col = TXT if b == 0 else PATCH
                r_ = Rectangle(width=w, height=h, stroke_color=GREY_C, stroke_width=1.5, fill_color=col,
                               fill_opacity=0.18 + 0.12 * (a == b))
                blocks.add(VGroup(r_, label(names[(a, b)], font_size=16, color=WHITE).move_to(r_)))
        x0, y0 = 1.7, 2.5
        for k, (a, b) in enumerate(((0, 0), (0, 1), (1, 0), (1, 1))):
            blk = blocks[k]
            blk.move_to([x0 + (0 if b == 0 else nt * cell) + blk.width / 2, y0 - (0 if a == 0 else nt * cell) - blk.height / 2, 0])
        bl = label(r"who looks at whom \ (schematic)", font_size=20, color=GREY_A).next_to(blocks, DOWN, buff=0.2)
        facts = VGroup(label(r"queries and keys normalized \ (QK-norm): \ stable at scale", font_size=20, color=GREY_A),
                       label(r"three frozen text encoders: \ two CLIPs, \ T5-XXL", font_size=20, color=GREY_A),
                       label(r"a 16-channel autoencoder; \ up to $8$ billion weights \ (as published)", font_size=20,
                             color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.4)
        cite_ = cite(r"P.~Esser et al., \textit{Scaling Rectified Flow Transformers} (SD3, 2024)", corner=UR)
        sd3 = history_card(r"Mar 2024", r"Stable Diffusion 3 \ (Stability AI)", r"Part 21's rectified flow, \ a new "
                           r"transformer: \ MM-DiT", color=HIST, width=5.0, font_size=24).move_to([3.6, 1.0, 0])
        with self.voiceover(
            "In March 2024 Patrick Esser, Robin Rombach and colleagues at Stability AI described Stable Diffusion 3: "
            "Part 21's rectified flow, with a new transformer, MM-DiT. It puts the prompt's tokens and the picture's "
            "patches into one sequence. <bookmark mark='a'/> Each kind keeps its own weights, since words and "
            "patches are different things; <bookmark mark='b'/> then a single attention runs over the joined "
            "sequence. <bookmark mark='c'/> So every patch can read every word, and, unlike cross-attention, the "
            "words are rewritten by the picture as it's drawn. <bookmark mark='d'/> Normalizing queries and keys kept "
            "training stable; three frozen text encoders read the prompt; the largest model had eight billion "
            "weights."
        ) as vo:
            self.play(FadeIn(cite_), FadeIn(sd3, shift=UP * 0.1))
            self.play(FadeIn(seq), FadeIn(tl), FadeIn(il))
            vo.wait_until("a")
            self.play(FadeIn(wq))
            vo.wait_until("b")
            self.play(Write(eq), FadeIn(el))
            vo.wait_until("c")
            self.play(FadeOut(sd3))
            self.play(LaggedStart(*[FadeIn(b_) for b_ in blocks], lag_ratio=0.25), FadeIn(bl), run_time=2.0)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(f_) for f_ in facts], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def timesteps(self):
        v = load("tsample")
        ax = axes([0, 1], [0, 1.8], x_length=4.6, y_length=2.6, xlabel=r"$t$: \ noise $\to$ data",
                  ylabel=r"how often each $t$ is trained", xticks=[0, 0.5, 1], yticks=[0, 1], center=[-3.6, 0.8, 0],
                  font_size=18)

        def ln(t):
            return math.exp(-math.log(t / (1 - t)) ** 2 / 2) / (math.sqrt(2 * math.pi) * t * (1 - t))

        uni = ax.ax.plot(lambda t: 1.0, x_range=[0.0, 1.0, 0.01], color=UNI, stroke_width=3.5)
        lnc = ax.ax.plot(ln, x_range=[0.005, 0.995, 0.005], color=LN, stroke_width=3.5)
        ku = label(r"uniform", font_size=20, color=UNI).next_to(ax.ax.c2p(1, 1), UR, buff=0.05)
        kl = label(r"logit-normal", font_size=20, color=LN).next_to(ax.ax.c2p(0.62, ln(0.62)), UR, buff=0.08)
        f = MathTex(r"t = \operatorname{sigmoid}(u), \quad u \sim \mathcal{N}(0, 1)", font_size=30, color=LN).move_to([-3.6, -1.8, 0])
        ks = [int(k) for k in v["sampling"]]
        fu, fl_ = np.asarray(v["uniform_fd"]), np.asarray(v["logit-normal_fd"])
        lk = [math.log2(k) for k in ks]
        lo_y = math.floor(math.log10(min(fu.min(), fl_.min())) * 10) / 10
        hi_y = math.ceil(math.log10(max(fu.max(), fl_.max())) * 10) / 10
        yt = [v for v in (100, 300, 1000, 3000, 10000, 30000) if lo_y <= math.log10(v) <= hi_y]
        bx = axes([0, lk[-1]], [lo_y, hi_y], x_length=4.8, y_length=3.0, xlabel=r"sampling steps",
                  ylabel=r"distance from real letters (FD, log scale)", xticks=lk, yticks=[math.log10(v) for v in yt],
                  xfmt=lambda x: f"{2 ** x:.0f}", yfmt=lambda y: f"{10 ** y:,.0f}".replace(",", "{,}"),
                  center=[3.3, 0.4, 0], font_size=18)
        lu, ll = mean_band(bx.ax, lk, np.log10(fu), UNI), mean_band(bx.ax, lk, np.log10(fl_), LN)
        diff = fl_.mean(0) - fu.mean(0)
        few = int(np.argmin(diff))
        if ks[few] == 1:
            few_s = "a single sampling step"
        else:
            few_s = f"{ks[few]} sampling steps"
        note_ = note(r"flow matching in the $16$-number latent space of chapter 3; \ three seeds each").to_edge(DOWN, buff=0.3)
        hard = VGroup(label(r"$t$ near $0$: \ pure noise; \ the best guess is the average picture", font_size=22, color=GREY_A),
                      label(r"$t$ near $1$: \ almost clean; \ little left to fix", font_size=22, color=GREY_A),
                      label(r"in between: \ the hard part", font_size=24, color=LN)).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        hard.move_to([3.3, 0.8, 0])
        if np.all(diff < 0):
            verdict = (f"Trained logit-normally, our letters come out closer to real ones at every number of sampling "
                       f"steps, most of all with {few_s}.")
        elif np.mean(diff) < 0:
            verdict = (f"Trained logit-normally, our letters come out closer to real ones on average, most of all with "
                       f"{few_s}, though not at every count.")
        else:
            verdict = ("On our letters, uniform does as well or better: in a space of sixteen numbers, the middle "
                       "isn't where the difficulty is. On large pictures, the paper found logit-normal the best of the "
                       "many schedules it compared.")
        with self.voiceover(
            "SD3 also changed which noise levels it trains on. <bookmark mark='a'/> Part 21 drew the time t "
            "uniformly. But near pure noise the best guess is just the average picture, and near the data there's "
            "little left to fix: the hard part is the middle. <bookmark mark='b'/> So draw a normal number and "
            "squash it with a sigmoid: the logit-normal, which trains most in the middle. Of the many choices the "
            "paper compared, this one ranked best. <bookmark mark='c'/> We trained flow matching both ways, three "
            "seeds each. " + verdict
        ) as vo:
            self.play(Create(ax))
            vo.wait_until("a")
            self.play(Create(uni), FadeIn(ku))
            self.play(LaggedStart(*[FadeIn(h_, shift=RIGHT * 0.1) for h_ in hard], lag_ratio=0.8), run_time=4.0)
            vo.wait_until("b")
            self.play(Create(lnc), FadeIn(kl), Write(f), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeOut(hard))
            self.play(Create(bx), FadeIn(note_))
            self.play(FadeIn(lu[0]), Create(lu[1]), FadeIn(ll[0]), Create(ll[1]), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        s = load("shift")
        sig = float(s["demo_sigma"])
        S = 1.7
        ims = Group(gray_image(np.asarray(s["demo20"]) * 0.5 + 0.25, S), gray_image(np.asarray(s["demo80"]) * 0.5 + 0.25, S),
                    gray_image(np.asarray(s["demo_pooled"]) * 0.5 + 0.25, S)).arrange(DOWN, buff=0.45).move_to([-5.3, 0.0, 0])
        cap = VGroup(label(rf"$20 \times 20$, \ noise ${sig}$", font_size=16, color=GREY_A),
                     label(rf"$80 \times 80$, \ the same noise", font_size=16, color=GREY_A),
                     label(rf"$4 \times 4$ averages: \ noise ${float(s['demo_left']):.2f}$", font_size=16, color=PATCH))
        for c_, im in zip(cap, ims):
            c_.next_to(im, DOWN, buff=0.05)
        pairs = [Group(i_, c_) for i_, c_ in zip(ims, cap)]
        big = Group(*[p_.copy() for p_ in pairs])
        for b_ in big:
            b_[1].scale(1.3).next_to(b_[0], DOWN, buff=0.1)
        big.arrange(RIGHT, buff=0.8, aligned_edge=UP).scale(1.45).move_to(UP * 0.2)
        rows = [
            cmath(r"z", r"=", r"(1 - \sigma)\, x + \sigma\, \varepsilon", font_size=32),
            cmath(r"\bar z", r"=", r"(1 - \sigma)\, c + \sigma\, \bar\varepsilon, \qquad \bar\varepsilon \sim \mathcal N(0, \tfrac1n)",
                  font_size=32),
            cmath(r"\operatorname{sd}(\hat c - c)", r"=", r"\frac{\sigma}{1 - \sigma}\,\frac{1}{\sqrt n}", font_size=32),
            cmath(r"\frac{\sigma_m}{1 - \sigma_m}\frac{1}{\sqrt m}", r"=", r"\frac{\sigma_n}{1 - \sigma_n}\frac{1}{\sqrt n}",
                  font_size=32),
            cmath(r"\sigma_m", r"=", r"\frac{\alpha\, \sigma_n}{1 + (\alpha - 1)\, \sigma_n}, \qquad \alpha = \sqrt{m / n}",
                  font_size=32),
        ]
        whys = [why(r"$\sigma$: \ the share of noise, \ $n$ pixels"),
                why(r"a flat picture, \ every pixel $c$: \ average them"),
                why(r"estimate $\hat c = \bar z / (1-\sigma)$"),
                why(r"ask for the same uncertainty \ at $m$ pixels"),
                why(r"solve for $\sigma_m$")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=0.4, buff=0.42, edge=6.8)
        lsnr = MathTex(r"\log \mathrm{SNR}_m = \log \mathrm{SNR}_n - 2 \log \alpha", font_size=28, color=PATCH).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "One more thing changes with size. <bookmark mark='a'/> Add the same noise to a small letter and to a "
            "drawing of it with sixteen times the pixels. The big one looks clearer, and it is: average each four by "
            f"four block, and the noise falls from {sig} to {float(s['demo_left']):.2f}. Neighbouring pixels share "
            "their information, so a noise level that destroys a small picture leaves a large one legible. "
            "<bookmark mark='b'/> SD3 made this exact. Write sigma for the share of noise. <bookmark mark='c'/> Take "
            "the worst case, a flat picture: every pixel the same value c. Average the n pixels: the noise shrinks "
            "by the square root of n. <bookmark mark='d'/> So the uncertainty left about c is sigma over one minus "
            "sigma, over root n. <bookmark mark='e'/> Ask for the same uncertainty at m pixels <bookmark mark='f'/> "
            "and solve: the noise level shifts by a factor alpha, the square root of the ratio of pixel counts. In "
            "log signal-to-noise, it's a constant shift."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in big], lag_ratio=0.5), run_time=2.5)
            vo.wait_until("b")
            self.play(*[Transform(b_, p_) for b_, p_ in zip(big, pairs)], run_time=1.2)
            for k, m in enumerate("bcdef"):
                vo.wait_until(m)
                step(k)
            self.play(FadeIn(lsnr))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def check(self):
        s = load("shift")
        sizes = [int(x) for x in s["sizes"]]
        sg = np.asarray(s["sigmas"], float)
        ax = axes([0.3, 1.0], [0, 1], x_length=4.8, y_length=3.0, xlabel=r"noise level $\sigma$",
                  ylabel=r"chance the exact posterior names the right picture", xticks=[0.3, 0.65, 1.0], yticks=[0, 0.5, 1],
                  center=[-3.4, 0.3, 0], font_size=17)
        bx = axes([0.3, 1.0], [0, 1], x_length=4.8, y_length=3.0, xlabel=r"the $20$-pixel level each is shifted from",
                  ylabel=r"the same, \ after the shift", xticks=[0.3, 0.65, 1.0], yticks=[0, 0.5, 1], center=[3.2, 0.3, 0],
                  font_size=17)
        before = VGroup(*[curve(ax.ax, sg, np.asarray(s[f"p_{n}"]), RES_C[n]) for n in sizes])
        after = VGroup(*[curve(bx.ax, sg, np.asarray(s[f"pshift_{n}"]), RES_C[n]) for n in sizes])
        leg = legend([(RES_C[n], rf"${n} \times {n}$ pixels") for n in sizes], font_size=18).arrange(RIGHT, buff=0.5).to_edge(UP, buff=0.35)
        ex = Group(*[gray_image(np.asarray(s[f"ex_{n}"])[1], 0.8) for n in sizes]).arrange(RIGHT, buff=0.2).to_corner(DL, buff=0.3)
        exl = label(r"the same letter, \ drawn at $20$, $40$, $80$", font_size=16, color=GREY_A).next_to(ex, UP, buff=0.08)
        half = {n: float(s[f"half_{n}"]) for n in sizes}
        pred = {n: (n / 20) * half[20] / (1 + (n / 20 - 1) * half[20]) for n in sizes}
        h_line = DashedLine(ax.ax.c2p(0.3, 0.5), ax.ax.c2p(1.0, 0.5), color=GREY_C, stroke_width=1.5, dash_length=0.06)
        marks = VGroup(*[Dot(ax.ax.c2p(half[n], 0.5), radius=0.07, color=RES_C[n]) for n in sizes])
        preds = VGroup(*[Circle(radius=0.11, stroke_color=RES_C[n], stroke_width=2.5).move_to(ax.ax.c2p(pred[n], 0.5))
                         for n in sizes[1:]])
        pk = label(r"dots: \ where each is right half the time; \ rings: \ the formula's prediction", font_size=18,
                   color=GREY_A)
        pk.next_to(leg, DOWN, buff=0.15)
        gb, ga = s["gap_before"], s["gap_after"]
        g80b, g80a = float(gb[str(sizes[-1])]), float(ga[str(sizes[-1])])
        cite_ = cite(rf"${int(s['N'])}$ letters, \ ${int(s['n_mc'])}$ noisy draws per level; \ SD3 used $\alpha = 3$ at "
                     r"$1024^2$ \ (as published)", corner=DR)
        if g80a < 0.5 * g80b:
            verdict = (f"After the shift the curves nearly line up: the largest gap to the small picture's falls from "
                       f"{g80b:.2f} to {g80a:.2f}.")
        else:
            verdict = (f"After the shift they move together, but don't fully line up: the largest gap falls only from "
                       f"{g80b:.2f} to {g80a:.2f}, because a real drawing at 80 pixels has finer detail than the "
                       "flat picture the formula assumes.")
        with self.voiceover(
            "Does it hold for real pictures? We drew the same five hundred letters at 20, 40 and 80 pixels a side, "
            "added noise, and asked the exact posterior which letter picture it was. <bookmark mark='a'/> At 20 "
            f"pixels it's right half the time at a noise level of {half[20]:.2f}; at 40, at {half[40]:.2f}; at 80, at "
            f"{half[80]:.2f}. The formula predicts {pred[40]:.2f} and {pred[80]:.2f}. <bookmark mark='b'/> " + verdict
            + " <bookmark mark='c'/> SD3's authors called the flat-picture assumption unrealistic, tested shifts "
            "with human raters, and settled on alpha equals three at a thousand and twenty-four pixels a side."
        ) as vo:
            self.play(FadeIn(leg), Create(ax), FadeIn(ex), FadeIn(exl))
            self.play(LaggedStart(*[Create(c_) for c_ in before], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("a")
            self.play(Create(h_line), LaggedStart(*[FadeIn(m_, scale=0.5) for m_ in marks], lag_ratio=0.4), run_time=1.5)
            self.play(LaggedStart(*[FadeIn(m_, scale=0.5) for m_ in preds], lag_ratio=0.4), FadeIn(pk), run_time=1.2)
            vo.wait_until("b")
            self.play(Create(bx), LaggedStart(*[Create(c_) for c_ in after], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def flux(self):
        head = label(r"Flux", font_size=40).to_edge(UP, buff=0.4)
        cards = VGroup(
            history_card(r"Aug 2024", r"FLUX.1 \ (Black Forest Labs)", r"$12$ billion weights; \ MM-DiT blocks, then "
                         r"single-stream blocks; \ rotary positions; \ a guidance-distilled open version",
                         color=HIST, width=11.0, font_size=25),
            history_card(r"Jun 2025", r"FLUX.1 Kontext", r"edit by context: \ the input picture's tokens joined to the "
                         r"sequence", color=HIST, width=11.0, font_size=25),
            history_card(r"Nov 2025", r"FLUX.2", r"$32$ billion weights \ (open [dev]); \ a $24$-billion vision-language "
                         r"model reads the prompt; \ up to $10$ reference pictures", color=HIST, width=11.0, font_size=25),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(head, DOWN, buff=0.4)
        if cards.height > 5.0:
            cards.height = 5.0
            cards.next_to(head, DOWN, buff=0.4)
        foot = label(r"the recipe: \ latent space, \ rectified flow, \ one transformer over words and patches", font_size=24,
                     color=PATCH).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Several of SD3's authors went on to found Black Forest Labs. <bookmark mark='a'/> In August "
            "2024 they released FLUX.1: twelve billion weights, MM-DiT blocks followed by cheaper single-stream "
            "blocks, rotary positions, and an open version distilled to need no guidance. <bookmark mark='b'/> In "
            "2025 FLUX.1 Kontext edited pictures by joining the input picture's tokens to the sequence, "
            "<bookmark mark='c'/> and FLUX.2 grew to thirty-two billion, with a vision-language model reading the "
            "prompt and up to ten reference pictures. <bookmark mark='d'/> The recipe has settled: a latent space, "
            "rectified flow, one transformer over words and patches."
        ) as vo:
            self.play(FadeIn(head))
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(FadeIn(cards[k], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()
