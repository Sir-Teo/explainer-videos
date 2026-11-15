from __future__ import annotations

from videos.psychology.psych21.common import *  # noqa: F403

NOISE_COL = (TRACE, CUE, FALSE)


class Reconstruction(VoiceoverScene):
    def construct(self):
        self.card()
        self.bartlett()
        self.dots()
        self.derive()
        self.bias()

    def card(self):
        card = chapter_card(7, r"Remembering as rebuilding", r"Is a memory retrieved, \ or reconstructed?",
                            lit={1932: r"Bartlett", 1991: r"Huttenlocher, \ Hedges \& Duncan",
                                 1998: r"Wynn \& Logie", 1999: r"Bergman \& Roediger"},
                            part=PART, scale=("mind", "culture"), marr=("what",))
        with self.voiceover("Chapter seven. Remembering as rebuilding."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def bartlett(self):
        head = heading(r"Bartlett's \emph{War of the Ghosts}")
        chain = VGroup(*[word_chip(t, color=c, font_size=24) for t, c in
                         ((r"the story", TRACE), (r"retold", CUE), (r"retold again", CUE), (r"months later", FALSE))])
        chain.arrange(RIGHT, buff=0.7).move_to([0, 2.0, 0])
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.1, color=GREY_B)
                          for a, b in zip(chain[:-1], chain[1:])])
        rows = rows_of([
            (r"Cambridge, \ 1910s: \ students read a folk tale from the Pacific Northwest, \ strange to them, \ and "
             r"retold it again and again", WHITE),
            (r"the retellings grew shorter, \ the strange became familiar, \ the supernatural was explained away", FALSE),
            (r"Bartlett, \ 1932: \ remembering is not re-excitation of fixed traces but an imaginative "
             r"reconstruction, \ built from a \emph{schema}", CTX),
            (r"Bergman and Roediger, \ 1999: \ the same procedure, \ the same story: \ errors grew with each delay, "
             r"\ new details were imported", TRACE),
            (r"a caution: \ Bartlett's method was informal, \ and memories of real events are often more accurate "
             r"than his students' \ (Wynn and Logie, \ 1998)", GREY_A),
        ], 12.4, 24, 0.3).to_edge(DOWN, buff=0.65)
        tag = historical_tag(r"Bartlett (1932); \ Bergman \& Roediger (1999)")
        with self.voiceover(
            "Reconsolidation said that a memory is rewritten when it's used. Frederic Bartlett had said something "
            "like it, from a very different kind of evidence. <bookmark mark='a'/> In Cambridge, in the 1910s, he "
            "gave students a folk tale from the Pacific Northwest, The War of the Ghosts, a story whose logic was "
            "strange to them. They retold it, and retold it again, sometimes months or years later. "
            "<bookmark mark='b'/> The retellings grew shorter. What was strange became familiar, and the "
            "supernatural was explained away. The story was turned, step by step, into the kind of story an English "
            "student expected. <bookmark mark='c'/> His conclusion, in his 1932 book Remembering, was that "
            "remembering is not the re-excitation of fixed traces but an imaginative reconstruction, built from an "
            "organised body of past knowledge, which he called a schema. <bookmark mark='d'/> In 1999 Erik Bergman "
            "and Henry Roediger repeated the procedure with the same story. Errors grew with each delay, and new "
            "details crept in. <bookmark mark='e'/> A caution, though. Bartlett's method was informal, and other "
            "work finds memory for real events more faithful than his students' memory for a strange tale."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(chain[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(c)) for a, c in zip(arrows, chain[1:])],
                                  lag_ratio=0.5), FadeIn(rows[0]))
            for m, r in zip("bcde", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def dots(self):
        d = load("adjust")
        head = heading(r"Where was the dot?")
        circ = Circle(radius=2.0, color=GREY_B).move_to([-3.4, -0.1, 0])
        cx, cy, _ = circ.get_center()
        quad = VGroup(DashedLine([cx - 2, cy, 0], [cx + 2, cy, 0], color=GREY_D),
                      DashedLine([cx, cy - 2, 0], [cx, cy + 2, 0], color=GREY_D))
        ang = np.deg2rad(10)
        R0 = 1.35
        true = Dot([cx + R0 * np.cos(ang), cy + R0 * np.sin(ang), 0], color=TRACE, radius=0.1)
        proto = Dot([cx + R0 * np.cos(np.pi / 4), cy + R0 * np.sin(np.pi / 4), 0], color=CTX, radius=0.08)
        lam = d["lambda2"]
        rem_ang = lam * ang + (1 - lam) * np.pi / 4
        rem = Dot([cx + R0 * np.cos(rem_ang), cy + R0 * np.sin(rem_ang), 0], color=FALSE, radius=0.1)
        arrow = CurvedArrow(true.get_center(), rem.get_center(), angle=0.5, color=FALSE, stroke_width=3)
        lbl = VGroup(label(r"shown", font_size=20, color=TRACE).next_to(true, RIGHT, buff=0.1),
                     label(r"the quadrant's centre", font_size=20, color=CTX).next_to(proto, UP, buff=0.12),
                     label(r"remembered", font_size=20, color=FALSE).next_to(rem, LEFT, buff=0.12))
        rows = rows_of([
            (r"Huttenlocher, \ Hedges and Duncan, \ 1991: \ a dot flashes in a circle; \ moments later, \ show where "
             r"it was", WHITE),
            (r"people place it nearer the centre of its quadrant than it was, \ and away from the lines between "
             r"quadrants", FALSE),
            (r"the less certain the fine-grained memory, \ the stronger the pull should be", CUE),
            (r"their account: \ memory keeps the fine-grained position \emph{and} its category, \ and blends them",
             CTX),
        ], 6.2, 22, 0.32).move_to([3.4, -0.1, 0])
        tag = historical_tag(r"Huttenlocher, \ Hedges \& Duncan (1991)")
        with self.voiceover(
            "Bartlett's schemas can be made precise, in a much simpler task. <bookmark mark='a'/> Janellen "
            "Huttenlocher, Larry Hedges and Susan Duncan flashed a dot inside a circle and, a moment later, asked "
            "people to show where it had been. <bookmark mark='b'/> People were biased in a systematic way: they put "
            "the dot nearer the centre of its quadrant than it really was, and away from the imaginary lines "
            "dividing the circle. <bookmark mark='c'/> And on their account, the less certain the fine-grained "
            "memory, the stronger the pull should be. <bookmark mark='d'/> Their account: memory holds two things, "
            "the fine-grained position and the category it fell in, the quadrant, and recall blends the two. That "
            "blend can be derived."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Create(circ), FadeIn(quad))
            vo.wait_until("a")
            self.play(FadeIn(true), FadeIn(lbl[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(proto), FadeIn(lbl[1]), Create(arrow), FadeIn(rem), FadeIn(lbl[2]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def derive(self):
        head = heading(r"Derivation: \ the category adjustment model")
        eqs = VGroup(
            MathTex(r"y \sim \mathcal{N}(x, \sigma_y^2)", r"\qquad", r"x \sim \mathcal{N}(\rho, \sigma_c^2)",
                    font_size=36),
            MathTex(r"\hat{x} = \lambda\, y + (1 - \lambda)\, \rho", font_size=40, color=FALSE),
            MathTex(r"\lambda = \frac{\sigma_c^2}{\sigma_c^2 + \sigma_y^2}", font_size=40, color=MODEL),
            MathTex(r"E(\hat{x} - x)^2 = \lambda\, \sigma_y^2 \;<\; \sigma_y^2", font_size=38, color=TRACE),
        ).arrange(DOWN, buff=0.35).move_to([-3.3, 0.1, 0])
        eqs[0][0].set_color(TRACE)
        eqs[0][2].set_color(CTX)
        rows = rows_of([
            (r"$y$: \ the fine-grained trace, \ the true position $x$ plus noise", TRACE),
            (r"$\rho$, $\sigma_c$: \ the category's centre and spread, \ what you know about dots in that quadrant",
             CTX),
            (r"the best estimate weights each by its reliability: \ a posterior mean, \ the cue combination of "
             r"Part 14", MODEL),
            (r"the bias toward $\rho$ is the price, \ and the reward is a smaller error on average", FALSE),
        ], 6.0, 22, 0.32).move_to([3.5, 0.1, 0])
        tag = published_tag(r"Huttenlocher, \ Hedges \& Duncan (1991)")
        with self.voiceover(
            "Write it as inference. <bookmark mark='a'/> The trace, y, is the true position x plus noise with "
            "variance sigma y squared. And you know something about where dots in that quadrant tend to be: around "
            "its centre, rho, with spread sigma c. <bookmark mark='b'/> The estimate that minimises squared error is "
            "a weighted average of the trace and the category's centre, <bookmark mark='c'/> with a weight lambda "
            "that gives each its reliability. It's a posterior mean, exactly the cue combination of Part 14, with "
            "the category as one cue and the trace as the other. <bookmark mark='d'/> And here's the point. The "
            "estimate is biased toward the centre, but its expected squared error is lambda times the trace's, which "
            "is smaller. Leaning on the schema makes each memory wrong in a predictable direction, and right, on "
            "average, more often. That's Bartlett's distortion, as a rational strategy."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Write(eqs[0]), FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(Write(eqs[1]))
            vo.wait_until("c")
            self.play(Write(eqs[2]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Write(eqs[3]), FadeIn(rows[3]))
        self.clear_scene()

    def bias(self):
        d = load("adjust")
        head = heading(r"Bias and error, \ by how noisy the trace is")
        pos = d["positions"]
        A = axes([0, 90], [-22, 22], x_length=6.2, y_length=3.6, xticks=[0, 45, 90], yticks=[-20, 0, 20],
                 xfmt=lambda v: f"{v:.0f}^\\circ", yfmt=lambda v: f"{v:+.0f}^\\circ" if v else "0",
                 xlabel=r"true angle within the quadrant", ylabel=r"mean error of the remembered angle",
                 center=[-3.0, 0.0, 0], font_size=18)
        zero = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(90, 0), color=GREY_D)
        cs = VGroup(*[curve(A.ax, pos, d[f"bias{k}"], NOISE_COL[k], 4) for k in range(3)])
        key = legend([(NOISE_COL[k], rf"trace noise {d['noise'][k]:.0f}$^\circ$: \ $\lambda = {d[f'lambda{k}']:.2f}$"
                       ) for k in range(3)], font_size=20).move_to([3.6, 1.6, 0])
        tab = VGroup(*[label(rf"error {d[f'rmse{k}']:.1f}$^\circ$ \ instead of {d[f'rmse_trace{k}']:.1f}$^\circ$",
                             font_size=21, color=NOISE_COL[k]) for k in range(3)])
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.6, -0.2, 0])
        rows = rows_of([
            (r"positive below 45$^\circ$, \ negative above: \ every estimate pulled toward the centre", FALSE),
            (r"the noisier the trace, \ the stronger the pull, \ and the more the blend saves", MODEL),
        ], 5.6, 21, 0.2).move_to([3.6, -2.0, 0])
        ptag = psyche_tag(r"\texttt{memory.category\_adjustment}")
        with self.voiceover(
            "Here's the model in numbers, for a quadrant of ninety degrees. <bookmark mark='a'/> For a precise "
            f"trace, lambda is {d['lambda0']:.2f}, and the bias is small. <bookmark mark='b'/> As the trace gets "
            "noisier, lambda falls and the pull toward forty-five degrees grows: dots below the centre are "
            "remembered too high, dots above it too low, the S-shape Huttenlocher found. "
            f"<bookmark mark='c'/> And the root-mean-square error with the blend is smaller than the trace's "
            f"alone, {d['rmse2']:.1f} degrees instead of {d['rmse_trace2']:.1f} for the noisiest. The more you've "
            "forgotten, the more the schema helps, and the more it distorts."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), Create(zero), FadeIn(ptag))
            vo.wait_until("a")
            self.play(Create(cs[0]), FadeIn(key[0]))
            vo.wait_until("b")
            self.play(Create(cs[1]), Create(cs[2]), FadeIn(key[1]), FadeIn(key[2]), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(tab), FadeIn(rows[1]))
        self.clear_scene()
