from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai30.common import CAUSE, CTRL, PART, heads_grid, load, signed_image, ticks

PREV = C.TRUE_P
IND = C.BITS
KC = C.SURPRISE


class Induction(VoiceoverScene):
    def construct(self):
        self.card()
        self.paths()
        self.composition()
        self.weights()
        self.ablation()
        self.replay()

    def card(self):
        card = chapter_card(5, r"An induction circuit, end to end", r"How do two heads copy?", lit=(2017,), part=PART)
        with self.voiceover("Chapter five. An induction circuit, end to end."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def diagram(self):
        """Two layers of heads on the residual stream: the previous-token head writes, the induction head reads."""
        y0, y1 = -1.6, 0.6
        stream = Line([-6.0, -2.6, 0], [-6.0, 2.4, 0], color=GREY_C, stroke_width=6)
        h1 = RoundedRectangle(width=2.6, height=0.8, corner_radius=0.12, stroke_color=PREV, stroke_width=3,
                              fill_color=PREV, fill_opacity=0.15).move_to([-3.8, y0, 0])
        h1l = label(r"previous-token heads", font_size=20, color=PREV).move_to(h1)
        h2 = RoundedRectangle(width=3.6, height=1.0, corner_radius=0.12, stroke_color=IND, stroke_width=3,
                              fill_color=IND, fill_opacity=0.15).move_to([-3.4, y1, 0])
        h2l = label(r"induction heads", font_size=20, color=IND).move_to(h2).shift(UP * 0.22)
        qkv = VGroup(*[label(t, font_size=20, color=GREY_A).move_to(h2.get_bottom() + UP * 0.25 + RIGHT * dx)
                       for t, dx in ((r"$Q$", -1.1), (r"$K$", 0.0), (r"$V$", 1.1))])
        w1 = Arrow([-6.0, y0 - 0.6, 0], h1.get_left(), buff=0.05, color=GREY_B, stroke_width=2.5)
        w2 = Arrow(h1.get_right() + RIGHT * 0.05, [-0.9, y0 + 0.4, 0], buff=0, color=PREV, stroke_width=2.5)
        back = Line([-0.9, y0 + 0.4, 0], [-0.9, y1 - 1.0, 0], color=PREV, stroke_width=2.5)
        ins = VGroup(*[Arrow([-0.9, y1 - 1.0, 0], q.get_bottom() + DOWN * 0.05, buff=0.02, color=PREV, stroke_width=2.2,
                             max_tip_length_to_length_ratio=0.15) for q in qkv])
        return VGroup(stream, h1, h1l, h2, h2l, qkv, w1, w2, back, ins)

    def paths(self):
        d = load("induction")
        pn = d["path_noise"]
        dg = self.diagram()
        ins = dg[-1]
        vals = [max(float(pn["q"]), 0.0), max(float(pn["k"]), 0.0), max(float(pn["v"]), 0.0)]  # -0.00 is no effect
        g = axes([0, 3], [0, 1.1], x_length=4.2, y_length=3.0, ylabel=r"copying lost", yticks=[0, 0.5, 1.0],
                 center=[3.9, -0.6, 0])
        bars_ = VGroup()
        for i, (v, t) in enumerate(zip(vals, ("queries", "keys", "values"))):
            r = Rectangle(width=0.8, height=max(min(v, 1.1) / 1.1 * 3.0, 0.01), stroke_width=0,
                          fill_color=KC if t == "keys" else CTRL, fill_opacity=0.9).move_to(g.ax.c2p(i + 0.5, 0), aligned_edge=DOWN)
            bars_.add(VGroup(r, MathTex(f"{v:.2f}", font_size=24).next_to(r, UP, buff=0.06),
                             label(t, font_size=18, color=GREY_A).next_to(g.ax.c2p(i + 0.5, 0), DOWN, buff=0.12)))
        dc = definition_card(r"path patching", r"patch an activation along one path only: \ here, the previous-token "
                             r"heads' corrupted outputs sent into just the second layer's queries, \ keys, \ or values",
                             color=CAUSE, width=6.2, font_size=19).to_corner(UR, buff=0.3)
        hc = note(r"Wang et al.\ (2022); \ Goldowsky-Dill et al.\ (2023)").next_to(dc, DOWN, buff=0.1).align_to(dc, RIGHT)
        best = int(np.argmax(vals))
        single = [float(v) for v in d["path_single"]]
        verdict = ("The message goes through the keys. Each token's key now carries the token before it, so the "
                   "induction heads' query, the current token, finds the position right after its last occurrence."
                   if best == 1 else "The message does not go mainly through the keys here.")
        ps_ = d["path_self"]
        verdict2 = (f"Either previous-token head alone carries {100 * min(single):.0f} to {100 * max(single):.0f} "
                    "percent: they share the job. And the head that looks at the token itself sends its message mostly "
                    f"into the queries, {100 * float(ps_['q']):.0f} percent: the query says which token we are at." if
                    len(single) > 1 else
                    f"The head that looks at the token itself sends its message mostly into the queries, "
                    f"{100 * float(ps_['q']):.0f} percent: the query says which token we are at.")
        with self.voiceover(
            "Two heads in different layers can only work together through the residual stream: the first writes, "
            "the second reads. <bookmark mark='a'/> But the second head reads in three places, its queries, its keys "
            "and its values. Which one carries the message? Pause and predict. <bookmark mark='p'/> Path patching "
            "asks exactly that: send the corrupted outputs of the previous-token heads into one of the three only, "
            f"and leave everything else clean. <bookmark mark='b'/> Into the queries: {100 * vals[0]:.0f} percent of "
            f"the copying lost. Into the values: {100 * vals[2]:.0f}. <bookmark mark='c'/> Into the keys: "
            f"{100 * vals[1]:.0f}. {verdict} <bookmark mark='d'/>{verdict2}"
        ) as vo:
            self.play(FadeIn(dg[:-1]))
            vo.wait_until("a")
            self.play(FadeIn(dc), FadeIn(hc), LaggedStart(*[GrowArrow(a_) for a_ in ins], lag_ratio=0.2))
            pz = pause_card(r"Queries, \ keys, \ or values: \ which carries the message?", width=4.6,
                            font_size=22).move_to(g)
            self.play(FadeIn(pz))
            vo.wait_until("p")
            self.play(FadeOut(pz), FadeIn(g))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars_[0][0], DOWN), FadeIn(bars_[0][1:]), Indicate(ins[0], color=CAUSE))
            self.play(GrowFromEdge(bars_[2][0], DOWN), FadeIn(bars_[2][1:]), Indicate(ins[2], color=CAUSE))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars_[1][0], DOWN), FadeIn(bars_[1][1:]), Indicate(ins[1], color=KC, scale_factor=1.3))
            vo.wait_until("d")
            sl = label(r"\\ ".join([rf"previous-token head {int(h) + 1} alone, \ keys: \ ${v:.2f}$"
                                     for h, v in zip(d["prev_set"], single)] +
                                    [rf"the current-token head, \ queries: \ ${float(ps_['q']):.2f}$"]),
                       font_size=20, color=GREY_A).to_corner(UR, buff=0.4)
            self.play(FadeOut(dc), FadeOut(hc), FadeIn(sl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def composition(self):
        d = load("induction")
        K = np.asarray(d["comp_k"])
        base, sd = float(d["comp_base"]), float(d["comp_base_sd"])
        hp, hi = int(d["prev_head"]), int(d["ind_head"])
        rows = [
            cmath(r"W_{QK}^{(2)}", r"=", r"W_Q^{(2)\top} W_K^{(2)}", font_size=34),
            cmath(r"W_{OV}^{(1)}", r"=", r"W_O^{(1)} W_V^{(1)}", font_size=34),
            cmath(r"\text{K-composition}", r"=", r"\frac{\| W_{QK}^{(2)} W_{OV}^{(1)} \|_F}{\| W_{QK}^{(2)} \|_F \, \| W_{OV}^{(1)} \|_F}",
                  font_size=34),
        ]
        whys = [why(r"what the second head compares"), why(r"what the first head writes"),
                why(r"how much the second head's keys read it")]
        step = ladder(self, rows, whys, keep=3, top=3.0, x=-2.4, buff=0.4, edge=6.8)
        g = VGroup()
        for i in range(4):
            for j in range(4):
                v = K[i, j]
                sq = Square(0.55, stroke_color=GREY_D, stroke_width=1, fill_color=KC,
                            fill_opacity=0.05 + 0.85 * min(v / K.max(), 1)).move_to([j * 0.55, -i * 0.55, 0])
                g.add(VGroup(sq, MathTex(f"{v:.2f}", font_size=18).move_to(sq)))
        g.move_to([-2.6, -2.1, 0])
        xl = label(r"layer-2 heads $\rightarrow$", font_size=16, color=GREY_B).next_to(g, UP, buff=0.08)
        yl = label(r"layer-1 \\ heads", font_size=16, color=GREY_B).next_to(g, LEFT, buff=0.12)
        pairs = [K[a, b] for a in d["prev_set"] for b in d["ind_set"]]
        klo, khi = float(min(pairs)), float(max(pairs))
        res = label(rf"previous-token heads into induction heads: \ ${klo:.2f}$ to ${khi:.2f}$ \\ random heads of the same shape: \ "
                    rf"${base:.3f} \pm {sd:.3f}$", font_size=22, color=WHITE).move_to([3.6, -2.0, 0])
        hc = note(r"Elhage et al., \textit{A Mathematical Framework for Transformer Circuits} (2021)").to_corner(DR, buff=0.2)
        z = (klo - base) / max(sd, 1e-9)
        with self.voiceover(
            "The same fact is written in the weights, before running anything. <bookmark mark='a'/> The second "
            "head compares queries and keys through one matrix, W Q K. <bookmark mark='b'/> The first head writes "
            "into the stream through another, W O V. <bookmark mark='c'/> Their composition score, from Nelson "
            "Elhage and colleagues' framework, asks how much of what the first head writes the second head's keys "
            f"can read. <bookmark mark='d'/> From our previous-token heads into our induction heads it is {klo:.2f} to "
            f"{khi:.2f}; for random heads of the same shape "
            f"it would be {base:.3f}, give or take {sd:.3f}: at least {z:.0f} standard deviations away. The keys "
            "were built to read those heads."
        ) as vo:
            step(0)
            vo.wait_until("a")
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(FadeIn(g), FadeIn(xl), FadeIn(yl), FadeIn(hc))
            self.play(*[Indicate(g[int(a) * 4 + int(b)], color=KC, scale_factor=1.2) for a in d["prev_set"]
                        for b in d["ind_set"]], FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def weights(self):
        d = load("induction")
        off = np.asarray(d["qk_pos_offsets"])
        M = np.asarray(d["ov"])
        hp, hi = int(d["prev_head"]), int(d["ind_head"])
        g = axes([-0.5, len(off) - 0.5], [min(off.min(), 0) * 1.1, off.max() * 1.15], x_length=4.8, y_length=3.0,
                 xlabel=r"how far back the key is", ylabel=r"score, \ positions only", xticks=list(range(len(off))),
                 center=[-3.4, -0.7, 0])
        b = VGroup(*[Rectangle(width=0.36, height=max(abs(v) / (np.abs(off).max() * 1.15) * 3.0, 0.01), stroke_width=0,
                               fill_color=PREV, fill_opacity=0.9 if k == 1 else 0.45)
                     .move_to(g.ax.c2p(k, 0), aligned_edge=DOWN if v >= 0 else UP) for k, v in enumerate(off)])
        t1 = label(r"the previous-token heads' QK circuits \\ on the position embeddings \ (averaged)", font_size=20,
                   color=PREV).next_to(g, UP, buff=0.2)
        Ms = M / np.abs(M).max()
        img = signed_image(Ms, 3.4, 3.4, pos=IND, neg=C.SURPRISE).move_to([3.4, -0.6, 0])
        t2 = label(r"the induction heads' OV circuits: \\ token attended to $\rightarrow$ logits", font_size=20,
                   color=IND).next_to(img, UP, buff=0.2)
        xl = label(r"token read $\rightarrow$", font_size=16, color=GREY_B).next_to(img, DOWN, buff=0.08)
        yl = label(r"logit \\ raised", font_size=16, color=GREY_B).next_to(img, LEFT, buff=0.1)
        cs = float(d["ov_copy_score"])
        diag = float(d["ov_diag_top"])
        res = label(rf"the diagonal: \ for ${100 * diag:.0f}\%$ of tokens, \ the logit raised most is their own; \\ "
                    rf"copying score $\sum \lambda / \sum |\lambda| = {cs:.2f}$", font_size=19, color=GREY_A)
        res.to_edge(DOWN, buff=0.25).shift(RIGHT * 2.6)
        best_off = int(np.argmax(off))
        verdict = ("the scores are highest for the key one position back." if best_off == 1 else
                   "the scores are highest for the token itself and the one before it, and fall off with distance: "
                   "position narrows attention to the last few tokens, and the tokens' content does the rest.")
        verdict2 = ("The heads copy." if cs > 0.5 else "The copying is only partly visible in the weights.")
        with self.voiceover(
            "Each head's job can be read off its weights too. <bookmark mark='a'/> Feed the previous-token heads "
            f"nothing but the position embeddings: {verdict} "
            "<bookmark mark='b'/> And trace the induction heads' values all the way from the token they attend "
            "to, through W O V, to the logits: a 64 by 64 matrix, token in, logit out. "
            f"<bookmark mark='c'/> For {100 * diag:.0f} percent of tokens, the logit raised most is the token's own, "
            f"and the eigenvalues give a copying score of {cs:.2f}, where 1 would be pure copying. {verdict2}"
        ) as vo:
            self.play(FadeIn(g), FadeIn(t1))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in b], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(img), FadeIn(t2), FadeIn(xl), FadeIn(yl))
            vo.wait_until("c")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ablation(self):
        d = load("induction")
        A = np.asarray(d["ablate_bits"])
        clean = float(d["clean_bits"])
        hp, hi = int(d["prev_head"]), int(d["ind_head"])
        cv = np.asarray(d["curve"])
        rnd = float(cv[-1, 2])
        g = heads_grid(A, CAUSE, cell=0.95, fmt="{:.2f}", vmax=max(A.max(), 1e-9), font_size=24).move_to([-2.4, -0.4, 0])
        cap = label(r"bits per token inside the repeat, \ with one head replaced by its average output", font_size=20,
                    color=GREY_A).next_to(g, UP, buff=0.35)
        ref = label(rf"no head removed: \ ${clean:.2f}$ \\ random tokens, \ nothing to copy: \ ${rnd:.2f}$", font_size=22,
                    color=WHITE).move_to([4.0, 0.3, 0])
        ps_, is_, sh = [int(h) for h in d["prev_set"]], [int(h) for h in d["ind_set"]], int(d["self_head"])
        pw, iw = max(A[0, h] for h in ps_), max(A[1, h] for h in is_)
        boxes = VGroup(*[SurroundingRectangle(g.cells[h], color=PREV, buff=0.03, stroke_width=4) for h in ps_],
                       *[SurroundingRectangle(g.cells[4 + h], color=IND, buff=0.03, stroke_width=4) for h in is_],
                       SurroundingRectangle(g.cells[sh], color=WHITE, buff=0.03, stroke_width=4))
        key_ = legend([(PREV, r"previous-token heads"), (IND, r"induction heads"), (WHITE, r"current-token head")],
                      font_size=20).next_to(ref, DOWN, buff=0.5)
        with self.voiceover(
            "Last, the bluntest test: remove each head, replacing its output by its average. <bookmark mark='a'/> "
            f"With every head in place the repeat costs {clean:.2f} bits per token. <bookmark mark='b'/> Without a "
            f"previous-token head, up to {pw:.2f}; without an induction head, up to {iw:.2f}; without the "
            f"current-token head, {A[0, sh]:.2f}; random tokens with nothing to copy cost {rnd:.2f}. The circuit, end "
            "to end: heads in layer one write each token's predecessor into it, a head there sharpens which token "
            "is which, and the induction heads find the match through their keys and copy it through their values."
        ) as vo:
            self.play(FadeIn(cap), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(ref))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(r_) for r_ in boxes], lag_ratio=0.15), FadeIn(key_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        d = load("induction")
        cv = np.asarray(d["curve"])
        kp = np.asarray(d["snap_kpath"])  # step, damage (nats), the whole gap (nats)
        st = np.asarray(d["snap_steps"], float)
        ind = np.asarray(d["snap_ind"])
        S = float(cv[-1, 0])
        top = float(cv[:, 1].max())
        g1 = axes([0, S], [0, top * 1.05], x_length=8.4, y_length=1.8, ylabel=r"bits per token, \ inside the repeat",
                  yticks=ticks(0, top, 2), center=[-0.6, 1.6, 0])
        dmg = np.clip(kp[:, 1], 0, None)
        g2 = axes([0, S], [0, max(dmg.max(), 1e-3) * 1.1], x_length=8.4, y_length=1.8, xlabel=r"training steps",
                  ylabel=r"the K path's effect \ (nats)", xticks=[0, S], yticks=ticks(0, max(dmg.max(), 1e-3), 2),
                  center=[-0.6, -1.6, 0])
        t = ValueTracker(0)

        def part(ax, xs, ys, col):
            def f():
                n = max(2, int(np.searchsorted(xs, t.get_value(), side="right")))
                return curve(ax.ax, xs[:n], ys[:n], col, 3)
            return always_redraw(f)

        c1 = part(g1, cv[:, 0], cv[:, 1], CAUSE)
        c2 = part(g2, st, dmg, KC)
        ix = always_redraw(lambda: label(rf"step ${int(t.get_value()):,}$".replace(",", "{,}") +
                                         rf": \ induction score ${ind[max(0, int(np.searchsorted(st, t.get_value(), side='right')) - 1)]:.2f}$",
                                         font_size=22, color=IND).to_corner(UR, buff=0.3))
        j = int(np.argmax(np.diff(cv[:, 1]) * -1)) + 1
        jump = float(cv[j, 0])
        k_on = float(st[np.argmax(dmg > 0.5 * dmg.max())])
        together = abs(k_on - jump) <= 2 * (st[1] - st[0])
        verdict = (f"The keys path switches on at the same moment, around step {int(k_on):,}: the drop in the loss is "
                   "the circuit being completed." if together else
                   f"The keys path reaches half its final effect around step {int(k_on):,}, against the loss's drop "
                   f"around {int(jump):,}.")
        with self.voiceover(
            "Part 13 watched these heads form. Now we can watch the cause form. Replay the training, and at every "
            "checkpoint measure the keys path, the effect of corrupting the previous-token head's message into the "
            f"induction head's keys alone. <bookmark mark='a'/> The loss on the repeat falls fastest around step "
            f"{int(jump):,}. <bookmark mark='b'/> {verdict}"
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2))
            self.add(c1, c2, ix)
            self.play(t.animate.set_value(0.6 * jump), run_time=8, rate_func=linear)
            vo.wait_until("a")
            self.play(t.animate.set_value(jump), run_time=3, rate_func=linear)
            vo.wait_until("b")
            self.play(t.animate.set_value(S), run_time=3, rate_func=linear)
        for m_ in (c1, c2, ix):
            m_.clear_updaters()
        self.wait(0.3)
        self.clear_scene()
