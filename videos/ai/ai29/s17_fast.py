from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai29.common import AGENT, CLAIM, FAIL, GOOD, HIST, MONO, PART, REWARD, load

BINS, FASTC = C.MODEL_Q, C.BITS


class Fast(VoiceoverScene):
    def construct(self):
        self.card()
        self.naive()
        self.cosine()
        self.sweep()
        self.foundation()
        self.frontier()

    def card(self):
        card = chapter_card(16, r"Action tokens, and robot foundation models", r"How do you write motion as words?",
                            lit=(2026,), part=PART)
        with self.voiceover("Chapter sixteen. Action tokens, and robot foundation models."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def naive(self):
        f = load("fast")
        ex = np.asarray(f["example"])  # (H, J) radians
        H, J = ex.shape
        lo, hi = np.asarray(f["lo"]), np.asarray(f["hi"])
        bins = int(f["params"]["bins"])
        q = np.clip(((ex - lo) / (hi - lo) * bins).astype(int), 0, bins - 1)
        ax = CornerAxes(x_range=[0, H, 10], y_range=[float(ex.min()) - 0.1, float(ex.max()) + 0.1, 1], x_length=6.0,
                        y_length=3.0, tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": False})
        ax.move_to([-3.4, 0.8, 0])
        cols = [interpolate_color(ManimColor(AGENT), ManimColor(GOOD), j / (J - 1)) for j in range(J)]
        lines = VGroup(*[curve(ax, np.arange(H), ex[:, j], cols[j], 2.5) for j in range(J)])
        al = label(rf"one second of a ${J}$-joint arm \ (${H}$ steps at $50$ Hz)", font_size=22, color=GREY_A)
        al.next_to(ax, UP, buff=0.15)
        row = VGroup(*[data_text(f"{v:3d}", font=MONO, font_size=18, color=cols[0]) for v in q[:12, 0]])
        row.arrange(RIGHT, buff=0.12).move_to([3.4, 1.6, 0])
        rl = label(r"joint 1, \ step by step, \ as one of $256$ bins", font_size=20, color=BINS).next_to(row, UP, buff=0.15)
        n_tok = int(f["bin_tokens"])
        rep, near = float(f["bin_repeat"]), float(f["bin_near"])
        stats = VGroup(label(rf"${J} \times {H} = {n_tok}$ tokens for one second", font_size=24, color=BINS),
                       label(rf"a token equals the one before: \ ${100 * rep:.0f}\%$", font_size=22, color=GREY_A),
                       label(rf"within one bin of it: \ ${100 * near:.0f}\%$", font_size=22, color=GREY_A))
        stats.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.4, -0.2, 0])
        tail = label(r"each token says almost nothing: \ predicting the next one is copying", font_size=26,
                     color=FAIL).to_edge(DOWN, buff=0.6)
        tag = note(r"synthetic, smooth motion: \ minimum-jerk moves between random poses", font_size=17).to_corner(DL, buff=0.2)
        with self.voiceover(
            "RT-2 and OpenVLA wrote actions as tokens the simplest way. <bookmark mark='a'/> Take each joint's "
            "position at each time step, and round it to one of two hundred and fifty-six bins. "
            f"<bookmark mark='b'/> For a seven-joint arm at fifty steps a second, that is {n_tok} tokens for one "
            f"second of motion. <bookmark mark='c'/> And they are nearly all the same: on our smooth test motions, "
            f"{100 * rep:.0f} percent of tokens equal the one before, and {100 * near:.0f} percent are within one bin "
            "of it. <bookmark mark='d'/> A model trained to predict the next token learns mostly to copy, and the "
            "information it needs is spread thin across hundreds of tokens."
        ) as vo:
            self.play(Create(ax), FadeIn(al), LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.1), FadeIn(tag),
                      run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(rl), LaggedStart(*[FadeIn(t_) for t_ in row], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(stats[0]))
            vo.wait_until("c")
            self.play(FadeIn(stats[1]), FadeIn(stats[2]))
            vo.wait_until("d")
            self.play(FadeIn(tail))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cosine(self):
        from scipy.fft import dct, idct

        f = load("fast")
        ex = np.asarray(f["example"])[:, 0]
        lo, hi = float(np.asarray(f["lo"])[0]), float(np.asarray(f["hi"])[0])
        H = len(ex)
        a = 2 * (ex - lo) / (hi - lo) - 1
        c = dct(a, norm="ortho")
        gam = float(f["params"]["show_gamma"])
        q = np.round(gam * c)
        nz = int((q != 0).sum())
        ax = CornerAxes(x_range=[0, H, 10], y_range=[-1.2, 1.2, 0.5], x_length=5.6, y_length=2.8, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-3.6, 0.6, 0])
        sig = curve(ax, np.arange(H), a, AGENT, 3)
        al = label(r"joint 1 over one second \ (normalized)", font_size=20, color=GREY_A).next_to(ax, UP, buff=0.12)
        bx = CornerAxes(x_range=[0, H, 10], y_range=[0, float(np.abs(c).max()) * 1.1, 1], x_length=5.6, y_length=2.8,
                        tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([3.4, 0.6, 0])
        bars = VGroup(*[Line(bx.c2p(i + 0.5, 0), bx.c2p(i + 0.5, abs(float(v))), stroke_width=4,
                             color=FASTC if q[i] != 0 else GREY_D) for i, v in enumerate(c)])
        bl = label(r"its cosine transform: \ how much of each wave", font_size=20, color=GREY_A).next_to(bx, UP, buff=0.12)
        en = np.asarray(f["energy"])
        k3 = float(en[:3].sum())

        def partial(k):
            ck = c.copy()
            ck[k:] = 0
            return curve(ax, np.arange(H), idct(ck, norm="ortho"), WHITE, 2.5)

        ks_ = (1, 2, 3, 7)
        kl_ = [label(t_, font_size=20, color=WHITE).next_to(ax, DOWN, buff=0.2) for t_ in (
            r"the slowest cosine wave", r"the first $2$ cosine waves, \ added up", r"the first $3$ cosine waves, \ added up",
            r"the first $7$ cosine waves, \ added up")]
        rows = [cmath(r"\text{tokens}", r"=", r"\operatorname{BPE}\Big(\operatorname{round}\big(\gamma \cdot "
                      r"\operatorname{DCT}(a)\big)\Big)", font_size=30)]
        rows[0].to_edge(DOWN, buff=1.1)
        rl = label(rf"$\gamma = {gam:.0f}$: \ ${nz}$ of ${H}$ numbers survive the rounding; \ byte-pair encoding "
                   r"(Part 23) packs the zeros and repeats", font_size=20, color=FASTC).next_to(rows[0], DOWN, buff=0.2)
        cite_ = cite(r"K.~Pertsch et al., \textit{FAST} (2025)", corner=UR)
        with self.voiceover(
            "In January 2025 Karl Pertsch and colleagues at Physical Intelligence compressed first. "
            "<bookmark mark='a'/> Any smooth motion is a sum of cosine waves, slow ones first, and the discrete "
            "cosine transform, the one inside JPEG, lists how much of each wave you need. <bookmark mark='b'/> "
            f"Smooth motion lives in the slowest few: over our motions, the first three waves carry "
            f"{100 * k3:.1f} percent of the energy. <bookmark mark='c'/> FAST scales the coefficients, rounds them "
            f"to integers, so that on this chunk only {nz} of {H} are not zero, and lets byte-pair encoding, from "
            "Part 23, merge the common patterns into tokens."
        ) as vo:
            self.play(Create(ax), FadeIn(al), Create(sig), FadeIn(cite_))
            vo.wait_until("a")
            self.play(Create(bx), FadeIn(bl), LaggedStart(*[Create(b_) for b_ in bars], lag_ratio=0.02), run_time=1.5)
            ps_ = partial(ks_[0])
            self.play(sig.animate.set_stroke(opacity=0.35), Create(ps_), FadeIn(kl_[0]))
            vo.wait_until("b")
            for j in range(1, len(ks_)):
                self.play(Transform(ps_, partial(ks_[j])), FadeTransform(kl_[j - 1], kl_[j]), run_time=0.9)
            vo.wait_until("c")
            self.play(Write(rows[0]), FadeIn(rl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sweep(self):
        f = load("fast")
        rows = f["rows"]
        toks = np.array([r["tokens"] for r in rows])
        err = np.array([r["rmse"] for r in rows])
        bt, be = float(f["bin_tokens"]), float(f["bin_rmse"])
        lx_lo, lx_hi = 0.7, 2.7
        g = axes([lx_lo, lx_hi, 0.5], [-3, -0.7, 0.5], x_length=7.2, y_length=4.4,
                 xlabel=r"tokens per second of motion \ (log scale)", ylabel=r"error of the rebuilt motion \ (radians, log)",
                 xticks=[1, 1.5, 2, 2.5], xfmt=lambda v: f"{10 ** v:.0f}", yticks=[-3, -2, -1],
                 yfmt=lambda v: {-3: "0.001", -2: "0.01", -1: "0.1"}[int(v)], center=[-1.9, -0.4, 0])
        ax = g.ax
        pts = VGroup(*[Dot(ax.c2p(np.log10(t), np.log10(e)), radius=0.07, color=FASTC) for t, e in zip(toks, err)])
        gl = VGroup(*[MathTex(rf"\gamma = {r['gamma']}", font_size=18, color=FASTC).next_to(p_, UR, buff=0.05)
                      for r, p_ in zip(rows, pts)])
        line = VMobject(color=FASTC, stroke_width=2.5).set_points_as_corners([p_.get_center() for p_ in pts])
        nb = Dot(ax.c2p(np.log10(bt), np.log10(be)), radius=0.09, color=BINS)
        nbl = label(r"per-step bins", font_size=20, color=BINS).next_to(nb, UP, buff=0.12)
        # FAST at matched error
        k = int(np.argmin(np.abs(np.log(err) - np.log(be))))
        ratio = bt / toks[k]
        stat = VGroup(label(rf"at about the same error ($\gamma = {rows[k]['gamma']}$):", font_size=22, color=GREY_A),
                      label(rf"${toks[k]:.0f}$ tokens instead of ${bt:.0f}$: \ ${ratio:.0f}\times$ fewer", font_size=24,
                            color=FASTC)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR, buff=0.4)
        claim = history_card(r"Jan 2025", r"$\pi_0$-FAST \ (Physical Intelligence)", r"an autoregressive policy on FAST "
                             r"tokens: \ as good as the flow-matching $\pi_0$ on many tasks, \ trained about $5\times$ "
                             r"faster (the company's report)", width=5.4, color=CLAIM, font_size=21)
        claim.next_to(stat, DOWN, buff=0.4).align_to(stat, LEFT)
        tag = note(rf"computed: \ {int(f['params']['n_test'])} held-out one-second chunks; \ byte-pair encoding with "
                   rf"{int(f['params']['merges'])} merges, \ learned on {int(f['params']['n_train'])} others", font_size=17)
        tag.to_edge(DOWN, buff=0.12)
        with self.voiceover(
            "How much does it save? Here is FAST on held-out motions, for a range of scales gamma: tokens per second "
            "against the error of the motion rebuilt from them. <bookmark mark='a'/> A bigger gamma keeps more "
            "detail and costs more tokens. <bookmark mark='b'/> Per-step binning sits far to the right: "
            f"{bt:.0f} tokens. <bookmark mark='c'/> At about the same error, FAST needs {toks[k]:.0f}, "
            f"{ratio:.0f} times fewer, and each one carries real information. <bookmark mark='d'/> Physical "
            "Intelligence reported that a policy writing FAST tokens matched their flow-matching pi zero on many "
            "tasks and trained about five times faster."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p_, scale=1.4) for p_ in pts], lag_ratio=0.2), Create(line), FadeIn(gl),
                      run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(nb, scale=1.5), FadeIn(nbl))
            vo.wait_until("c")
            self.play(FadeIn(stat), Indicate(pts[k], color=WHITE))
            vo.wait_until("d")
            self.play(FadeIn(claim, shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def foundation(self):
        steps = VGroup(*[RoundedRectangle(width=3.0, height=0.7, corner_radius=0.12, stroke_color=c, stroke_width=2,
                                          fill_color=c, fill_opacity=0.1) for c in (GREY_B, AGENT, FASTC)])
        texts = (r"``clean the bedroom''", r"subtask: \ ``pick up the pillow''", r"$50$ actions, \ flow matching")
        for s_, t_ in zip(steps, texts):
            s_.add(label(t_, font_size=20, color=WHITE).move_to(s_))
        steps.arrange(DOWN, buff=0.45).move_to([-4.0, 0.3, 0])
        arr = VGroup(*[Arrow(a.get_bottom(), b.get_top(), buff=0.06, color=GREY_B) for a, b in zip(steps, steps[1:])])
        abl = [(r"all of it", 94), (r"without web data", 74), (r"without other robots' data", 49),
               (r"without data from many homes", 31)]
        W = 4.4
        bars = VGroup()
        for name, v in abl:
            bar = Rectangle(width=W * v / 100, height=0.34, stroke_width=0, fill_color=AGENT if v == 94 else GREY_C,
                            fill_opacity=0.85)
            lab = label(name, font_size=19, color=GREY_A)
            val = MathTex(rf"{v}\%", font_size=22, color=WHITE)
            bars.add(VGroup(lab, bar, val))
        for k, r_ in enumerate(bars):
            r_[1].move_to([1.2 + r_[1].width / 2, 1.0 - 0.62 * k, 0])
            r_[0].next_to(r_[1], UP, buff=0.06).align_to(r_[1], LEFT)
            r_[2].next_to(r_[1], RIGHT, buff=0.12)
        bl = label(r"$\pi_{0.5}$ in homes it never saw: \ success, \ and what each kind of data adds", font_size=21,
                   color=AGENT).next_to(bars, UP, buff=0.3).align_to(bars, LEFT)
        tag = note(r"Physical Intelligence's own ablation (2025)", font_size=17).to_corner(DR, buff=0.25)
        with self.voiceover(
            "Physical Intelligence's pi zero point five, in April 2025, asked what it takes to work in a home the "
            "robot has never seen. <bookmark mark='a'/> The model first writes a subtask in words, pick up the "
            "pillow, <bookmark mark='b'/> then the motion for it, with the flow-matching expert. "
            "<bookmark mark='c'/> And it is trained on everything at once: web data, many kinds of robot, and many "
            "different homes. In the company's own ablation, in unseen homes, the full model succeeded ninety-four "
            "percent of the time; without web data, seventy-four; without other robots' data, forty-nine; "
            "without the variety of homes, thirty-one. <bookmark mark='d'/> For robots, as for language, breadth of "
            "data is what generalizes."
        ) as vo:
            self.play(FadeIn(steps[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowArrow(arr[0]), FadeIn(steps[1]))
            vo.wait_until("b")
            self.play(GrowArrow(arr[1]), FadeIn(steps[2]))
            vo.wait_until("c")
            self.play(FadeIn(bl), LaggedStart(*[FadeIn(b_, shift=RIGHT * 0.1) for b_ in bars], lag_ratio=0.4), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def frontier(self):
        head = label(r"Robot foundation models, \ 2025--26", font_size=34).to_edge(UP, buff=0.35)
        cards = VGroup(
            history_card(r"Mar 2025", r"Gemini Robotics; \ GR00T N1", r"Google DeepMind's VLA built on Gemini 2.0; \ "
                         r"NVIDIA's open model for humanoids", width=4.2, color=HIST, font_size=21),
            history_card(r"Nov 2025", r"$\pi^*_{0.6}$ and Recap", r"learning from its own experience and from "
                         r"corrections, \ with a value function: \ espresso from 5:30 am to 11:30 pm; \ throughput "
                         r"more than doubled on the hardest tasks", width=4.2, color=CLAIM, font_size=21),
            history_card(r"Mar 2026", r"memory for VLAs", r"Physical Intelligence: \ long- and short-term memory for "
                         r"tasks over ten minutes", width=4.2, color=CLAIM, font_size=21),
            history_card(r"Apr 2026", r"$\pi_{0.7}$", r"prompted with more than words: \ speed, \ quality, \ subgoal "
                         r"images; \ folds laundry on a robot never shown laundry", width=4.2, color=CLAIM, font_size=21),
            history_card(r"Oct 2026", r"Gemini 4 Argon for Robotics", r"Google's general physical-reasoning model: \ it "
                         r"plans, \ writes code, \ builds simulations", width=4.2, color=CLAIM, font_size=21),
            history_card(r"Oct 2026", r"the Pi API", r"Physical Intelligence opens fine-tuning and inference of its "
                         r"models to other robot makers", width=4.2, color=CLAIM, font_size=21),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.25, 0.3)).next_to(head, DOWN, buff=0.35)
        if cards.width > 13.4:
            cards.width = 13.4
        tag = note(r"grey cards: \ the companies' own descriptions and results", font_size=17).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Since then the field has moved fast, mostly through company reports. <bookmark mark='a'/> In March 2025 "
            "Google DeepMind built Gemini Robotics on its Gemini models, and NVIDIA released an open model for "
            "humanoids. <bookmark mark='b'/> In November Physical Intelligence added learning from experience: a "
            "value function scores how each moment is going, and the policy is told to act as the good moments "
            "did. It made espresso from five thirty in the morning to eleven thirty at night. "
            "<bookmark mark='c'/> In 2026 came memory for tasks longer than ten minutes, <bookmark mark='d'/> and "
            "pi zero point seven, which can be prompted with the speed and quality wanted, or a picture of the next "
            "subgoal. <bookmark mark='e'/> This October, Google released a physical-reasoning model that plans and "
            "builds simulations, <bookmark mark='f'/> and Physical Intelligence opened its models to other robot "
            "makers. These are the companies' own results; independent benchmarks for robots are still young."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for k, mk in enumerate("abcdef"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()
