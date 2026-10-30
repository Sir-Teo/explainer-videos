from __future__ import annotations


from explainer.ai import *  # noqa: F403
from videos.ai.ai11.common import OPT_COLORS, PART, era_strip, lag, takeaway_card

MU, SO, SH, AW = OPT_COLORS["muon"], OPT_COLORS["soap"], OPT_COLORS["shampoo"], OPT_COLORS["adamw"]


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.production()
        self.reality()
        self.successors()
        self.takeaway()

    def card(self):
        c = chapter_card(16, r"The optimizer race, \ 2024 to 2026", r"Did anything beat AdamW at scale?", part=PART)
        with self.voiceover("Chapter sixteen. The optimizer race, 2024 to 2026."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def production(self):
        events = [
            ("2024", r"AlgoPerf: \\ Shampoo $\approx 28\%$ \\ faster; \ Muon's \\ speedrun"),
            ("Feb 2025", r"Moonlight: \\ Muon at $16$B, \\ ``$\sim 2\times$'' \\ efficiency"),
            ("Jul 2025", r"Kimi K2: \\ MuonClip, \\ $1$T parameters, \\ $15.5$T tokens"),
            ("Jul 2025", r"GLM-4.5: \\ Muon"),
            ("Sep 2025", r"careful \\ benchmarks: \\ smaller gains"),
            ("2026", r"DeepSeek-V4: \\ Muon for most \\ modules, \ hybrid \\ Newton--Schulz"),
        ]
        head, axis, tag, skel, marks = era_strip(events, head_text=r"From a speedrun to production", font_size=19)
        with self.voiceover(
            "In two years the race moved from small benchmarks to the largest models. <bookmark mark='a'/> In 2024, "
            "AlgoPerf crowned Distributed Shampoo, and Muon set records in a speedrun. <bookmark mark='b'/> In "
            "February 2025 Moonshot AI scaled Muon to a sixteen-billion-parameter mixture of experts, Moonlight, and "
            "reported about twice AdamW's efficiency in compute-optimal training. <bookmark mark='c'/> In July they "
            "trained Kimi K2, a trillion parameters, with MuonClip. <bookmark mark='d'/> Zhipu's GLM-4.5 used Muon "
            "too. <bookmark mark='e'/> Then came careful, independent benchmarks, and smaller numbers. "
            "<bookmark mark='f'/> And in 2026 DeepSeek trained its fourth generation with Muon for most of the model, "
            "using the hybrid Newton–Schulz of Chapter eleven, and normalizing queries and keys instead of clipping "
            "them."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(tag), FadeIn(skel))
            self.play(FadeIn(marks[0], shift=UP * 0.2))
            for k, mk in enumerate("bcdef"):
                vo.wait_until(mk)
                self.play(FadeIn(marks[k + 1], shift=(UP if (k + 1) % 2 == 0 else DOWN) * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def reality(self):
        ax = CornerAxes(x_range=[0, 4, 1], y_range=[1.0, 2.1, 0.25], x_length=6.2, y_length=4.2, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-2.8, -0.5, 0])
        yt = VGroup(*[MathTex(rf"{v:.2f}\times", font_size=20, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.08)
                      for v in (1.0, 1.25, 1.5, 1.75, 2.0)])
        yn = label(r"speedup over AdamW, \ in tokens to the same loss", font_size=20, color=GREY_A).next_to(ax, UP, buff=0.12)
        yn.align_to(ax, LEFT)
        claim = Rectangle(width=ax.c2p(0.9, 0)[0] - ax.c2p(0.1, 0)[0], height=ax.c2p(0, 2.0)[1] - ax.c2p(0, 1.4)[1],
                          stroke_width=0, fill_color=GREY_B, fill_opacity=0.5).move_to(ax.c2p(0.5, 1.7))
        b1 = Rectangle(width=claim.width, height=ax.c2p(0, 1.4)[1] - ax.c2p(0, 1.0)[1], stroke_width=0, fill_color=MU,
                       fill_opacity=0.9).move_to(ax.c2p(2.0, 1.2))
        b2 = Rectangle(width=claim.width, height=ax.c2p(0, 1.1)[1] - ax.c2p(0, 1.0)[1], stroke_width=0, fill_color=MU,
                       fill_opacity=0.9).move_to(ax.c2p(3.3, 1.05))
        caps = VGroup(label(r"claimed \\ $1.4$--$2\times$", font_size=20, color=GREY_A).next_to(claim, DOWN, buff=0.1),
                      label(r"measured, \\ $0.1$B: \ $1.4\times$", font_size=20, color=MU).next_to(ax.c2p(2.0, 1.0), DOWN, buff=0.1),
                      label(r"measured, \\ $1.2$B: \ $1.1\times$", font_size=20, color=MU).next_to(ax.c2p(3.3, 1.0), DOWN, buff=0.1))
        src = note(r"as reported by K.~Wen, D.~Hall, T.~Ma \& P.~Liang, \textit{Fantastic Pretraining Optimizers and Where "
                   r"to Find Them} (2025): \ the best matrix-based optimizers, \ against a carefully tuned AdamW").to_edge(DOWN, buff=0.15)
        pts = VGroup(
            label(r"$11$ optimizers, \ $0.1$B--$1.2$B parameters, \ $1$--$8\times$ the Chinchilla data", font_size=20, color=WHITE),
            label(r"tuning AdamW's learning rate alone: \ up to $2\times$ on a $100$M model", font_size=20, color=AW),
            label(r"Muon fastest at little data per parameter; \ SOAP and Kron at $8\times$", font_size=20, color=SO),
            label(r"NVIDIA, 2026: \ Muon and SOAP stable at $100$M-token batches \\ where AdamW degraded; \ gains modest "
                  r"and mixed across tasks", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.6, 0.6, 0])
        keep_in_frame(pts)
        with self.voiceover(
            "How big are the gains really? <bookmark mark='a'/> New optimizers had claimed one and a half to two "
            "times AdamW's speed. In 2025 Kaiyue Wen, David Hall, Tengyu Ma and Percy Liang at Stanford tested eleven "
            "of them with equal care, tuning every one, AdamW included, on models up to one point two billion "
            "parameters. <bookmark mark='b'/> Tuning AdamW's learning rate alone could double its speed on a small "
            "model: many claimed gains were against weak baselines. <bookmark mark='c'/> The best, the "
            "matrix-based ones, Muon and SOAP, were about one point four times faster at a hundred million "
            "parameters, <bookmark mark='d'/> and only one point one times at a billion. <bookmark mark='e'/> Muon "
            "led with little data per parameter, SOAP with a lot. <bookmark mark='f'/> In 2026 a team at NVIDIA "
            "trained mixtures of experts up to seventy-two billion parameters with Muon and SOAP, and found them "
            "stable at batches of a hundred million tokens where AdamW degraded, with modest, mixed gains."
        ) as vo:
            self.play(Create(ax), FadeIn(yt), FadeIn(yn), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(claim), FadeIn(caps[0]), FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(GrowFromEdge(b1, DOWN), FadeIn(caps[1]))
            vo.wait_until("d")
            self.play(GrowFromEdge(b2, DOWN), FadeIn(caps[2]))
            vo.wait_until("e")
            self.play(FadeIn(pts[2]))
            vo.wait_until("f")
            self.play(FadeIn(pts[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def successors(self):
        cols = VGroup(
            VGroup(label(r"Muon's descendants", font_size=26, color=MU),
                   label(r"Polar Express (2025): \ the best polynomial for each round", font_size=20, color=WHITE),
                   label(r"Dion (Microsoft, 2025): \ low-rank orthonormal updates \\ that shard across machines", font_size=20, color=WHITE),
                   label(r"Dion3 (2026): \ Muon's loss, \ optimizer step up to $6\times$ faster", font_size=20, color=WHITE),
                   label(r"MONA, \ MUON+, \ T-MUON, \ \dots \ (2026 preprints)", font_size=20, color=GREY_A)),
            VGroup(label(r"Shampoo's descendants", font_size=26, color=SH),
                   label(r"Distributed Shampoo (Meta, 2023): \ grafting, \ AlgoPerf's winner", font_size=20, color=WHITE),
                   label(r"SOAP (2024): \ Adam in Shampoo's eigenbasis", font_size=20, color=WHITE),
                   label(r"KL-SOAP and others (2026): \ larger-scale variants", font_size=20, color=WHITE),
                   label(r"Kron (PSGD), \ Sophia, \ Scion, \ \dots", font_size=20, color=GREY_A)),
        )
        for c_ in cols:
            c_.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        cols.arrange(RIGHT, buff=0.7, aligned_edge=UP)
        cols.scale_to_fit_width(13.0).move_to(UP * 0.6)
        keep_in_frame(cols)
        lesson = label(r"the lesson of the race: \ tune the baseline, \ equal budgets, \ several seeds, \ report the spread",
                       font_size=24, color=C.BITS).to_edge(DOWN, buff=0.6)
        caveat = note(r"preprints listed by name only: \ their claims are the authors' own, \ not yet independently checked").next_to(lesson, DOWN, buff=0.15)
        with self.voiceover(
            "Meanwhile the descendants multiply. <bookmark mark='a'/> For Muon: better polynomials, like the Polar "
            "Express; versions that split the work across thousands of machines, like Microsoft's Dion, whose 2026 "
            "successor reports Muon's loss with an optimizer step up to six times faster; and a stream of 2026 "
            "preprints claiming improvements. <bookmark mark='b'/> For Shampoo: Distributed Shampoo, SOAP, and "
            "larger-scale variants of SOAP. Most of these claims are their authors' own and haven't been checked "
            "independently. <bookmark mark='c'/> Which is the race's real lesson, and the reason Chapter twelve was "
            "run the way it was: tune the baseline as hard as the newcomer, compare at equal budgets, use several "
            "seeds, and report the spread."
        ) as vo:
            self.play(FadeIn(cols[0][0]), FadeIn(cols[1][0]))
            vo.wait_until("a")
            self.play(lag([FadeIn(r_, shift=RIGHT * 0.2) for r_ in cols[0][1:]], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("b")
            self.play(lag([FadeIn(r_, shift=RIGHT * 0.2) for r_ in cols[1][1:]], lag_ratio=0.3), FadeIn(caveat), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(lesson))
        self.wait(0.3)
        self.clear_scene()

    def takeaway(self):
        t = takeaway_card(r"Matrix optimizers won, \ modestly",
                          r"By 2026 Muon trains frontier models, \ and Shampoo's line wins benchmarks; \ measured "
                          r"carefully, \ their edge over a well-tuned AdamW is real but smaller than first claimed, \ and "
                          r"shrinks with scale.", r"Next: \ the recap")
        with self.voiceover(
            "So by 2026 the matrix optimizers had won a place at the frontier: Muon trains some of the largest open "
            "models. But measured carefully, their edge over a well-tuned AdamW is real, smaller than first claimed, "
            "and shrinks as models grow."
        ):
            self.play(FadeIn(t[0], shift=UP * 0.2))
            self.play(FadeIn(t[1]))
        self.wait(0.3)
        self.clear_scene()
