from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai22.common import (CFG_C, CFG_NAME, LETTERS, PART, PATCH, fmt_int, gray_image, load, spread_bars,
                                   take_away)

ZERO_C = CFG_C["zero"]


def ways_picture() -> VGroup:
    """Three ways to give a transformer block the condition c: as extra tokens, as the normalization's scale and shift,
    and the same with a gate that starts at zero."""
    def toks(n, color, extra=0):
        g = VGroup(*[Square(0.26, stroke_color=PATCH, stroke_width=1.5, fill_color=PATCH, fill_opacity=0.15) for _ in range(n)])
        for _ in range(extra):
            g.add(Square(0.26, stroke_color=color, stroke_width=1.5, fill_color=color, fill_opacity=0.5))
        return g.arrange(RIGHT, buff=0.05)

    out = VGroup()
    for name, kind in ((CFG_NAME["context"], "context"), (CFG_NAME["ada"], "ada"), (CFG_NAME["zero"], "zero")):
        col = CFG_C[kind]
        blk = RoundedRectangle(width=2.4, height=0.7, corner_radius=0.1, stroke_color=GREY_B, stroke_width=2)
        t = toks(5, col, 2 if kind == "context" else 0).next_to(blk, DOWN, buff=0.25)
        g = VGroup(label(name, font_size=22, color=col), blk, t)
        g[0].next_to(blk, UP, buff=0.2)
        if kind == "context":
            g.add(label(r"$c$ as two more tokens", font_size=16, color=GREY_A).next_to(t, DOWN, buff=0.12))
        else:
            c_ = MathTex("c", font_size=26, color=col).next_to(blk, RIGHT, buff=0.5)
            g.add(c_, Arrow(c_.get_left(), blk.get_right(), buff=0.06, color=col, stroke_width=2.5,
                             max_tip_length_to_length_ratio=0.25))
            g.add(label(r"scale, shift" + (r", \ gate $= 0$" if kind == "zero" else ""), font_size=16, color=GREY_A)
                  .next_to(t, DOWN, buff=0.12))
        out.add(g)
    return out.arrange(RIGHT, buff=0.7)


class AdaLN(VoiceoverScene):
    def construct(self):
        self.card()
        self.ways()
        self.zero()
        self.learning()
        self.ablation()
        self.alphabet()

    def card(self):
        card = chapter_card(6, r"adaLN-Zero", r"How does the request get in?", part=PART)
        with self.voiceover("Chapter six. adaLN-Zero."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def ways(self):
        pic = ways_picture().move_to(UP * 0.4)
        if pic.width > 13:
            pic.width = 13
        head = label(r"Three ways to tell a block the noise level and the request, \ $c$", font_size=28).to_edge(UP, buff=0.4)
        cite_ = cite(r"W.~Peebles \& S.~Xie (2023) \ also tried cross-attention, \ as Stable Diffusion's U-Net used", corner=DL)
        with self.voiceover(
            "The denoiser must know the noise level and what it was asked to draw; call both together c. Peebles "
            "and Xie compared the ways in. <bookmark mark='a'/> In-context: append c to the sequence as extra "
            "tokens, and let attention find them. <bookmark mark='b'/> Adaptive layer norm: let c set the scale and "
            "shift of every normalization, so it reaches every token in every block. <bookmark mark='c'/> And "
            "adaLN-Zero: the same, plus a gate on each block's output, which starts at zero."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_))
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(FadeIn(pic[k], shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def zero(self):
        d = load("denoisers")
        colors = {r"\gamma": C.SURPRISE, r"\beta": C.SURPRISE, r"\alpha": PATCH, r"c": C.SURPRISE}
        f1 = cmath(r"h \leftarrow h +", r"\alpha", r"_1(", r"c", r") \odot \operatorname{Attn}\big((1 +", r"\gamma", r"_1(",
                   r"c", r")) \odot \operatorname{LN}(h) +", r"\beta", r"_1(", r"c", r")\big)", colors=colors, font_size=32)
        f2 = cmath(r"h \leftarrow h +", r"\alpha", r"_2(", r"c", r") \odot \operatorname{MLP}\big((1 +", r"\gamma", r"_2(",
                   r"c", r")) \odot \operatorname{LN}(h) +", r"\beta", r"_2(", r"c", r")\big)", colors=colors, font_size=32)
        f3 = cmath(r"(", r"\gamma", r"_1,", r"\beta", r"_1,", r"\alpha", r"_1,", r"\gamma", r"_2,", r"\beta", r"_2,", r"\alpha",
                   r"_2) = W", r"c", r"+ b, \qquad W = 0,\ b = 0 \text{ at the start}", colors=colors, font_size=32)
        fs = VGroup(f1, f2, f3).arrange(DOWN, buff=0.45).move_to(UP * 0.9)
        n1 = label(r"$c$: \ the noise level and the letter, \ one vector", font_size=22, color=C.SURPRISE)
        n2 = label(r"$\alpha = 0$: \ every block starts as the identity", font_size=22, color=PATCH)
        VGroup(n1, n2).arrange(RIGHT, buff=1.0).next_to(fs, DOWN, buff=0.5)
        # the gates opening during our training
        G = np.asarray(d["gates"])  # (points, 1 + 2 * blocks): step, then |alpha_1|, |alpha_2| per block
        st = G[:, 0]
        nb = (G.shape[1] - 1) // 2
        top = float(G[:, 1:].max()) * 1.1
        ax = axes([0, st[-1]], [0, top], x_length=5.0, y_length=1.8, xlabel=r"training step", ylabel=r"average $|\alpha|$, \ "
                  r"each block's attention (solid) \ and MLP (dashed)", xticks=[0, st[-1]], yticks=[0, round(top, 2)],
                  center=[0, -2.4, 0], font_size=16, xfmt=lambda x: fmt_int(x))
        shades = [interpolate_color(ManimColor(PATCH), ManimColor(C.SURPRISE), k / max(nb - 1, 1)) for k in range(nb)]
        lines = VGroup()
        for b in range(nb):
            lines.add(curve(ax.ax, st, G[:, 1 + 2 * b], shades[b], 2.5))
            lines.add(DashedVMobject(curve(ax.ax, st, G[:, 2 + 2 * b], shades[b], 2.5), num_dashes=40))
        cite_ = cite(r"W.~Peebles \& S.~Xie (2023): \ adaLN-Zero", corner=UR)
        opened = float(G[-1, 1:].mean())
        with self.voiceover(
            "Here is adaLN-Zero exactly. <bookmark mark='a'/> The condition c sets a scale gamma and a shift beta for "
            "each normalization, and a gate alpha on each branch's output. <bookmark mark='b'/> All six come from one "
            "linear map of c, and that map starts at zero. <bookmark mark='c'/> So at the start every gate is "
            "closed, and every block passes its input straight through: a deep network that begins as the identity. "
            f"<bookmark mark='d'/> Here are our model's gates during training: they start at zero and open, to an "
            f"average size of {opened:.2f} by the end, as the network finds a use for each block."
        ) as vo:
            self.play(FadeIn(cite_), Write(f1), Write(f2), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(n1))
            vo.wait_until("b")
            self.play(Write(f3))
            vo.wait_until("c")
            self.play(FadeIn(n2), *[Indicate(m_, color=PATCH) for m_ in (f1[1], f2[1])])
            vo.wait_until("d")
            self.play(FadeOut(n1), FadeOut(n2), FadeIn(ax), LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.1),
                      run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def learning(self):
        """How it learns: the same noise and the same ten requests, drawn at checkpoints, beside the loss."""
        d = load("denoisers")
        steps = [int(s_) for s_ in d["snap_at"]]
        snaps = np.asarray(d["snaps"])
        L = np.asarray(d["zero_curve"])[0][:, :2]
        total = steps[-1]
        S = 0.95

        def row(k):
            return Group(*[gray_image(im, S) for im in snaps[k]]).arrange(RIGHT, buff=0.08).move_to([0, 2.0, 0])

        asked = VGroup(*[Text(c, font="DejaVu Sans Mono", font_size=20, color=PATCH) for c in LETTERS[:10]])
        r0 = row(0)
        for a_, im in zip(asked, r0):
            a_.next_to(im, UP, buff=0.08)
        hi = float(np.percentile(L[:, 1], 99))
        ax = axes([0, total], [0, hi * 1.05], x_length=8.0, y_length=2.4, xlabel=r"training step \ ($64$ noisy letters each)",
                  ylabel=r"flow-matching loss \ (average of $50$ steps)", xticks=[0, total // 2, total],
                  yticks=[0, round(hi / 2, 2)], center=[0, -1.7, 0], font_size=18, xfmt=lambda x: fmt_int(x))
        t = ValueTracker(0)
        dot = always_redraw(lambda: Dot(ax.ax.c2p(t.get_value(), float(np.interp(t.get_value(), L[:, 0], L[:, 1]))),
                                        radius=0.07, color=ZERO_C))
        cnt = always_redraw(lambda: MathTex(rf"\text{{step }}{fmt_int(t.get_value())}", font_size=28, color=ZERO_C)
                            .next_to(r0, DOWN, buff=0.25))
        tag = label(r"same noise, \ same requests, \ every checkpoint", font_size=20, color=GREY_A).to_corner(UR, buff=0.3)
        reads = [int(round(10 * float(x))) for x in d["snap_read"]]
        with self.voiceover(
            "Here is ours learning: the same noise, asked for the same ten letters, A to J, drawn at checkpoints "
            f"during its {total:,} steps. <bookmark mark='a'/> At step {steps[0]} every block is still the identity, "
            f"so the noise passes straight through. <bookmark mark='b'/> At step {steps[2]} the judge reads "
            f"{reads[2]} of the ten as the letters requested; <bookmark mark='c'/> at step {steps[3]:,}, {reads[3]}; "
            f"<bookmark mark='d'/> at the end, {reads[-1]}. Meanwhile the loss falls from {L[0, 1]:.2f} to "
            f"{L[-1, 1]:.2f}."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(asked), FadeIn(r0), Create(ax))
            self.add(dot, cnt)
            cur = r0
            marks = {1: "a", 2: "b", 3: "c", len(steps) - 1: "d"}
            for k in range(1, len(steps)):
                if k in marks:
                    vo.wait_until(marks[k])
                nxt = row(k)
                seg = [ax.ax.c2p(a, b) for a, b in L if steps[k - 1] <= a <= steps[k]]
                anims = [t.animate.set_value(steps[k]), FadeOut(cur), FadeIn(nxt)]
                if len(seg) > 1:
                    anims.append(Create(VMobject(color=ZERO_C, stroke_width=3).set_points_as_corners(seg)))
                self.play(*anims, run_time=1.2)
                cur = nxt
        self.wait(0.3)
        self.remove(dot, cnt)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ablation(self):
        d = load("denoisers")
        kinds = ["context", "ada", "zero"]
        fd = {k: np.asarray(d[f"{k}_fd"])[:, -1] for k in kinds}
        acc = {k: np.asarray(d[f"{k}_acc"])[:, -1] for k in kinds}
        cols = [CFG_C[k] for k in kinds]
        b1 = spread_bars([[fd[k] for k in kinds]], cols, None, height=2.6, bar_w=0.7, gap=0.25, fmt=lambda v: f"{v:.0f}",
                         font_size=20).move_to([-3.4, 0.1, 0])
        b2 = spread_bars([[acc[k] for k in kinds]], cols, None, height=2.6, bar_w=0.7, gap=0.25, vmax=1.0,
                         fmt=lambda v: rf"{100 * v:.0f}\%", font_size=20).move_to([3.0, 0.1, 0])
        t1 = label(r"distance from real letters (FD), \ lower is better", font_size=20, color=GREY_A).next_to(b1, UP, buff=0.3)
        t2 = label(r"read as the letter requested", font_size=20, color=GREY_A).next_to(b2, UP, buff=0.3)
        leg = legend([(CFG_C[k], CFG_NAME[k]) for k in kinds], font_size=20).arrange(RIGHT, buff=0.5).next_to(VGroup(b1, b2), DOWN, buff=0.5)
        hd = note(rf"weights: \ in-context ${fmt_int(d['context_params'])}$, \ adaLN ${fmt_int(d['ada_params'])}$, \ "
                  rf"adaLN-Zero ${fmt_int(d['zero_params'])}$; \ same steps, \ data and seeds; \ "
                  rf"after ${fmt_int(d['steps'])}$ steps; \ three seeds: \ dots, \ bars min to max").to_edge(DOWN, buff=0.3)
        order = sorted(kinds, key=lambda k: fd[k].mean())
        names = {"context": "in-context tokens", "ada": "plain adaLN", "zero": "adaLN-Zero"}
        if order[0] == "zero":
            verdict = (f"As in the paper, adaLN-Zero comes out best: a distance of {fd['zero'].mean():.0f}, against "
                       f"{fd['ada'].mean():.0f} for plain adaLN and {fd['context'].mean():.0f} for in-context tokens.")
        else:
            verdict = (f"Here {names[order[0]]} comes out best, at a distance of {fd[order[0]].mean():.0f}, with "
                       f"adaLN-Zero at {fd['zero'].mean():.0f}: at four blocks deep, starting as the identity matters "
                       "less than in the paper's twenty-eight.")
        with self.voiceover(
            "Does the way in matter? We trained all three, three seeds each, with the same data and steps; the "
            "adaLN versions carry extra weights for their scales, shifts and gates. <bookmark mark='a'/> " + verdict + " <bookmark mark='b'/> In the paper, at four hundred thousand steps, "
            "adaLN-Zero's distance was nearly half that of in-context conditioning, at the same cost."
        ) as vo:
            self.play(FadeIn(t1), FadeIn(t2), FadeIn(b1.base), FadeIn(b2.base), FadeIn(leg), FadeIn(hd))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.15) for b_ in b1.bars[0]], lag_ratio=0.2),
                      LaggedStart(*[FadeIn(b_, shift=UP * 0.15) for b_ in b2.bars[0]], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("b")
            self.play(Indicate(leg[2], color=ZERO_C))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def alphabet(self):
        d = load("denoisers")
        A = np.asarray(d["alphabet"])
        grid = Group(*[gray_image(im, 0.85) for im in A[:26]]).arrange_in_grid(rows=2, cols=13, buff=(0.08, 0.4)).move_to(UP * 1.1)
        asked = VGroup(*[Text(c, font="DejaVu Sans Mono", font_size=20, color=PATCH).next_to(grid[i], UP, buff=0.06)
                         for i, c in enumerate(LETTERS)])
        second = Group(*[gray_image(im, 0.62) for im in A[26:52]]).arrange_in_grid(rows=2, cols=13, buff=0.06).to_edge(DOWN, buff=0.6)
        sl = label(r"asked again, \ from different noise", font_size=22, color=GREY_A).next_to(second, UP, buff=0.12)
        tk = label(rf"guidance $w = {float(d['guide']):g}$ \ (Part 21), \ $40$ steps", font_size=18, color=GREY_B).to_corner(DR, buff=0.2)
        with self.voiceover(
            "And here is our adaLN-Zero model, asked for each letter of the alphabet, with Part 21's guidance. "
            "<bookmark mark='a'/> Asked again from different noise, it draws the same letters in other styles: the "
            "request fixes what, the noise picks how."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(g_) for g_ in grid], lag_ratio=0.05), FadeIn(asked), FadeIn(tk), run_time=2.5)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(g_) for g_ in second], lag_ratio=0.03), FadeIn(sl), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()
