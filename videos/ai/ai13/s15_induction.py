from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai13.common import A, K, MONO, OURS, PART, Q, V, char_row, curve, framed, heat_image, load, seed_lines


class Induction(VoiceoverScene):
    def construct(self):
        self.card()
        self.copying()
        self.mechanism()
        self.phase()
        self.forming()
        self.composition()
        self.ours()

    def card(self):
        card = chapter_card(14, r"Induction heads", r"How does a model copy what it has just seen?", part=PART)
        with self.voiceover("Chapter fourteen. Induction heads."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def copying(self):
        t = load("tf")
        t1, t2 = np.asarray(t["text_bits1"]), np.asarray(t["text_bits2"])
        r1, r2 = np.asarray(t["copy_bits1"]), np.asarray(t["copy_bits2"])
        n = len(t1) + 1
        txt = str(t["text_ind_text"])[:n]
        row = char_row(txt[:60], 12.6, font_size=20).move_to(UP * 3.1)
        top = float(np.ceil(max(t1.max(), t2.max(), r1.max(), r2.max()) + 0.5))
        g = axes([0, n, 25], [0, top, 2], x_length=6.0, y_length=3.4, xlabel=r"position in the stretch",
                 ylabel=r"bits per character", xticks=[0, 50, 100], xfmt=lambda v: f"{int(v)}",
                 yticks=list(range(0, int(top) + 1, 2)), center=[-3.4, -0.4, 0])
        ax = g.ax
        c1 = curve(ax, np.arange(1, n), t1, GREY_B, 2.5)
        c2 = curve(ax, np.arange(1, n), t2, C.BITS, 3)
        m1, m2 = float(t1[4:].mean()), float(t2[4:].mean())
        R = len(r1) + 1
        g2 = axes([0, R, 20], [0, top, 2], x_length=4.2, y_length=3.4, xlabel=r"position", ylabel=r"random letters",
                  xticks=[0, 20, 40], xfmt=lambda v: f"{int(v)}", yticks=list(range(0, int(top) + 1, 2)),
                  center=[3.9, -0.4, 0])
        d1 = curve(g2.ax, np.arange(1, R), r1, GREY_B, 2.5)
        d2 = curve(g2.ax, np.arange(1, R), r2, C.BITS, 3)
        q1, q2 = float(r1[5:].mean()), float(r2[5:].mean())
        key = VGroup(label(r"first time through", font_size=20, color=GREY_B),
                     label(r"second time", font_size=20, color=C.BITS)).arrange(RIGHT, buff=0.6).to_edge(DOWN, buff=0.3)
        tag = note(r"our transformer; \ $16$ stretches of $100$ held-out characters, each shown twice").next_to(key, UP, buff=0.12)
        u26 = math.log2(26)
        if m2 < 0.6 * m1:
            v1 = (f"The first time through, {m1:.2f} bits a character; the second time, {m2:.2f}: it copies from its "
                  "own context.")
        elif m2 < m1 - 0.05:
            v1 = (f"The first time through, {m1:.2f} bits a character; the second time, {m2:.2f}: a little better, "
                  "but it barely copies.")
        else:
            v1 = (f"The first time through, {m1:.2f} bits a character; the second time, {m2:.2f}: no better. The "
                  "answer sits a hundred characters back, unused.")
        if q1 > u26 and q2 < 0.6 * q1:
            v2 = (f"Random letters: {q1:.1f} bits the first time, worse than a blind guess among 26 letters, "
                  f"{u26:.1f}; {q2:.1f} the second: here, at least, it copies.")
        elif q1 > u26:
            v2 = (f"Random letters: {q1:.1f} bits the first time, worse than a blind guess among 26 letters, "
                  f"{u26:.1f}; and {q2:.1f} the second: no copying here either.")
        elif q2 < 0.6 * q1:
            v2 = f"Random letters: {q1:.1f} bits the first time, {q2:.1f} the second: here, at least, it copies."
        else:
            v2 = f"Random letters: {q1:.1f} bits the first time, and {q2:.1f} the second: no copying here either."
        tail = ("The machinery behind copying has a name." if m2 < m1 - 0.05 else
                "Copying needs a particular piece of machinery, and our transformer has not built it.")
        with self.voiceover(
            "A test no counting model can pass: show our transformer a stretch of a novel it has never seen, twice "
            "in a row. <bookmark mark='a'/> " + v1 + " <bookmark mark='b'/> " + v2 + " <bookmark mark='c'/> " + tail
        ) as vo:
            self.play(FadeIn(row), FadeIn(g), FadeIn(key), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(c1), run_time=1.2)
            self.play(Create(c2), run_time=1.2)
            vo.wait_until("b")
            self.play(FadeIn(g2), Create(d1), Create(d2), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mechanism(self):
        s = "the Falcon ... the Fal"
        row = char_row(s, 11.0, font_size=34).move_to(UP * 1.4)
        i_cur = len(s) - 1  # the 'l' being read
        j_prev = s.index("Fal") + 2  # the earlier 'l'
        j_next = j_prev + 1  # what came after it: 'c'
        box = SurroundingRectangle(row[i_cur], color=Q, buff=0.08)
        # head 1: every position notes the character before it
        prevs = VGroup(*[CurvedArrow(row[k - 1].get_bottom() + DOWN * 0.08, row[k].get_bottom() + DOWN * 0.08, angle=PI / 2,
                                     color=K, stroke_width=2.5, tip_length=0.12)
                         for k in range(1, len(s)) if s[k] != " " and s[k - 1] != " "])
        h1 = label(r"head 1, \ an earlier layer: \ each character notes the one before it", font_size=26, color=K)
        h1.move_to(DOWN * 0.4)
        # head 2: the query looks for a key whose previous character matches its own
        arc = ArcBetweenPoints(row[i_cur].get_top() + UP * 0.1, row[j_next].get_top() + UP * 0.1, angle=-PI / 3.2,
                               color=A, stroke_width=6)
        h2 = label(r"head 2: \ ``which earlier character came right after one like me?'' \\ attend there, \ copy it",
                   font_size=26, color=A).next_to(h1, DOWN, buff=0.4)
        guess = VGroup(label(r"next:", font_size=30, color=GREY_A), Text("c", font=MONO, font_size=40, color=C.BITS))
        guess.arrange(RIGHT, buff=0.2).to_edge(DOWN, buff=0.6)
        rule = label(r"$[\,a\,][\,b\,] \;\dots\; [\,a\,] \;\to\; [\,b\,]$", font_size=34, color=WHITE).next_to(guess, UP, buff=0.3)
        tag = note(r"schematic").to_corner(DR, buff=0.3)
        cite_ = cite(r"C.~Olsson et al., \textit{In-context Learning and Induction Heads} (2022)", corner=UL)
        with self.voiceover(
            "It takes two heads, in two layers. <bookmark mark='a'/> In an earlier layer, a head that only looks one "
            "step back: each character's vector now also says which character came before it. <bookmark mark='b'/> "
            "In a later layer, the second head reads an 'l' and asks: which earlier character came right after an "
            "'l'? The 'c' in Falcon answers, because its note says: the one before me was an 'l'. "
            "<bookmark mark='c'/> So the head copies it: 'c'. Seen A then B? On seeing A again, predict B. Catherine "
            "Olsson and colleagues at Anthropic named these induction heads in 2022."
        ) as vo:
            self.play(FadeIn(row), Create(box), FadeIn(tag), FadeIn(cite_))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(p) for p in prevs], lag_ratio=0.05), FadeIn(h1), run_time=1.8)
            vo.wait_until("b")
            self.play(Create(arc), FadeIn(h2), Indicate(row[j_next], color=A))
            vo.wait_until("c")
            self.play(FadeIn(rule), FadeIn(guess, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def phase(self):
        d = load("induction")
        c1 = np.asarray(d["curve1"])
        seeds = [int(v) for v in d["seeds"]]
        C2 = [np.asarray(d[f"curve2_{s_}"]) for s_ in seeds]
        V_ = int(d["V"])
        top = math.ceil(math.log2(V_)) + 0.5
        g = axes([0, c1[-1, 0], 1000], [0, top, 1], x_length=6.6, y_length=3.8, xlabel=r"training steps",
                 ylabel=r"bits per token, \ on the repeated stretch", xticks=list(range(0, int(c1[-1, 0]) + 1, 1000)),
                 xfmt=lambda v: f"{int(v):,}".replace(",", "{,}"), yticks=[0, 2, 4, 6], center=[-3.2, -0.3, 0])
        ax = g.ax
        l1 = curve(ax, c1[:, 0], c1[:, 1], GREY_B, 3)
        l2 = VGroup(*[curve(ax, c_[:, 0], c_[:, 1], A, 3.0 if i == 0 else 2.0).set_stroke(opacity=1.0 if i == 0 else 0.55)
                      for i, c_ in enumerate(C2)])
        k1 = label(r"one layer", font_size=22, color=GREY_B).next_to(ax.c2p(c1[-1, 0], c1[-1, 1]), UP, buff=0.12).shift(LEFT * 0.6)
        k2 = label(rf"two layers, \ ${len(seeds)}$ seeds", font_size=22, color=A)
        k2.next_to(ax.c2p(c1[-1, 0], min(float(c_[-1, 1]) for c_ in C2)), DOWN, buff=0.35).align_to(
            ax.c2p(c1[-1, 0], 0), RIGHT)  # under the ends of the curves, where nothing is drawn
        js = [int(v) for v in d["jump_steps"]]
        jl = VGroup(*[DashedLine(ax.c2p(j, 0), ax.c2p(j, top), color=A, stroke_width=1.2) for j in js])
        S = 2.5
        mp = framed(heat_image(np.asarray(d["map_prev"]), S, S, color=K, mask_upper=True))
        mi = framed(heat_image(np.asarray(d["map_ind"]), S, S, color=A, mask_upper=True))
        maps = Group(mp, mi).arrange(RIGHT, buff=0.35).move_to([3.6, -0.1, 0])
        t1 = label(r"layer 1: \ one back", font_size=22, color=K).next_to(mp, UP, buff=0.12)
        t2 = label(r"layer 2: \ the induction head", font_size=22, color=A).next_to(mi, UP, buff=0.12)
        stripe = label(r"the stripe: \ the repeat looking at its source, one step ahead", font_size=20,
                       color=GREY_A).next_to(maps, DOWN, buff=0.2)
        head = label(rf"a small attention-only model, \ ${V_}$ random tokens with a repeated stretch", font_size=26)
        head.to_edge(UP, buff=0.35)
        f1, f2 = float(c1[-1, 1]), [float(v) for v in d["final2"]]
        one_fails = f1 > max(f2) + 1.0
        v1 = (f"With one layer it never learns to copy: after {int(c1[-1, 0]):,} steps, still {f1:.1f} bits on the "
              "repeat; one head cannot both note the previous token and search for it. "
              if one_fails else f"With one layer it ends at {f1:.1f} bits on the repeat. ")
        lo2, hi2 = min(f2), max(f2)
        if len(set(js)) == 1:
            v_jump = (f"With two layers, nothing happens for a while, and then the loss on the repeat falls off a cliff, "
                      f"around step {js[0]:,} in all our runs, down to {lo2:.2f} to {hi2:.2f} bits.")
        else:
            v_jump = (f"With two layers, nothing happens for a while, and then the loss on the repeat falls off a cliff, "
                      f"between steps {min(js):,} and {max(js):,} in our {len(js)} runs, down to {lo2:.2f} to {hi2:.2f} "
                      "bits.")
        with self.voiceover(
            "Induction heads can be watched as they form, in a small attention-only model trained on random tokens "
            f"with a repeated stretch inside. <bookmark mark='a'/> {v1}<bookmark mark='b'/> {v_jump} "
            "<bookmark mark='c'/> Inside, the first layer looks one step back, the second at the earlier copy, one "
            "step ahead. Olsson's team saw the same sudden jump in large models, just as they got good at learning "
            "from their prompt."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(Create(l1), FadeIn(k1), run_time=1.5)
            vo.wait_until("b")
            self.play(*[Create(l_) for l_ in l2], FadeIn(k2), run_time=2.5)
            self.play(Create(jl))
            vo.wait_until("c")
            self.play(FadeIn(maps), FadeIn(t1), FadeIn(t2))
            self.play(FadeIn(stripe))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def forming(self):
        """The two heads forming: their attention on the example, at checkpoints, beside the loss on the repeat."""
        d = load("induction")
        steps = [int(s_) for s_ in d["snap_steps"]]
        L1, L2 = np.asarray(d["snap_l1"], float), np.asarray(d["snap_l2"], float)
        hp, hi = int(d["prev_head"]), int(d["ind_head"])
        c2 = np.asarray(d["curve2"])
        js = int(d["jump_step"])
        S = 2.7
        # how strongly each head does its job on the example, checkpoint by checkpoint: the previous-token head's
        # attention one back, and the induction head's on the repeat (positions 60-79 copy 10-29), one ahead
        prev_sc = [float(np.mean([L1[k, hp, q, q - 1] for q in range(1, L1.shape[-1])])) for k in range(len(steps))]
        ind_sc = [float(np.mean([L2[k, hi, q, q - 49] for q in range(61, 80)])) for k in range(len(steps))]
        kb = int(np.argmax(ind_sc))  # the induction head at its sharpest, and the checkpoint before it began to rise
        ka = max([k for k in range(kb) if ind_sc[k] < 0.25 * ind_sc[kb]] or [0])
        lo_a, lo_b = (float(np.interp(steps[k], c2[:, 0], c2[:, 1])) for k in (ka, kb))
        kp = next(k for k in range(len(steps)) if prev_sc[k] >= 0.5 * max(prev_sc))
        if steps[ka] <= steps[kp] <= steps[kb]:
            together = (f"The first head turns to the token one back in the same window, reaching {prev_sc[kb]:.2f} "
                        f"by step {steps[kb]:,}. ")
        elif steps[kp] < steps[ka]:
            together = (f"The first head had already turned to the token one back, by step {steps[kp]:,}: the "
                        "induction head built on it. ")
        else:
            together = f"The first head turns to the token one back only later, by step {steps[kp]:,}. "

        def maps(k):
            return Group(heat_image(L1[k, hp], S, S, color=K, mask_upper=True),
                         heat_image(L2[k, hi], S, S, color=A, mask_upper=True)).arrange(RIGHT, buff=0.8).move_to([2.7, 0.5, 0])  # room for the titles

        cur = maps(0)
        frames = VGroup(*[SurroundingRectangle(m_, buff=0, color=GREY_D, stroke_width=1.5) for m_ in cur])
        t1 = label(r"layer 1, \ the head that will look one back", font_size=16, color=K).next_to(cur[0], UP, buff=0.12)
        t2 = label(r"layer 2, \ the future induction head", font_size=16, color=A).next_to(cur[1], UP, buff=0.12)
        top = float(c2[:, 1].max()) + 0.5
        ax = Axes(x_range=[0, c2[-1, 0], 1000], y_range=[0, top, 2], x_length=5.0, y_length=3.0, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-3.7, -0.2, 0])
        l2 = curve(ax, c2[:, 0], c2[:, 1], A, 3)
        yn = label(r"bits per token on the repeat", font_size=20, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        xn = label(r"training steps", font_size=20, color=GREY_A).next_to(ax, DOWN, buff=0.12)
        t = ValueTracker(0)
        dot = always_redraw(lambda: Dot(ax.c2p(t.get_value(), float(np.interp(t.get_value(), c2[:, 0], c2[:, 1]))), radius=0.08,
                                        color=C.BITS))
        cnt = always_redraw(lambda: MathTex(rf"\text{{step }}{int(t.get_value()):,}".replace(",", "{,}"), font_size=28, color=C.BITS)
                            .next_to(cur, DOWN, buff=0.3))
        # show every checkpoint up to a little past the jump, then the end
        show = [k for k, s_ in enumerate(steps) if s_ <= js + 750] + [len(steps) - 1]
        show = sorted(set(show))
        with self.voiceover(
            "Here are the two heads forming, checkpoint by checkpoint, beside the loss on the repeat. "
            "<bookmark mark='a'/> Early on, both look around vaguely. "
            f"<bookmark mark='b'/> Then, around step {js:,}, the second head finds the stripe: its attention there "
            f"jumps from {ind_sc[ka]:.2f} to {ind_sc[kb]:.2f} within {steps[kb] - steps[ka]} steps, as the loss on the "
            f"repeat falls from {lo_a:.1f} to {lo_b:.1f} bits. "
            + together
            + "Useless alone, together they copy."
        ) as vo:
            self.play(Create(ax), Create(l2), FadeIn(yn), FadeIn(xn), FadeIn(cur), Create(frames), FadeIn(t1), FadeIn(t2))
            self.add(dot, cnt)
            vo.wait_until("a")
            half = [k for k in show if steps[k] < js - 250]
            rest = [k for k in show if k not in half]
            for group, mk in ((half, None), (rest, "b")):
                if mk:
                    vo.wait_until(mk)
                for k in group[1:] if group is half else group:
                    nxt = maps(k)
                    self.play(FadeOut(cur), FadeIn(nxt), t.animate.set_value(steps[k]), run_time=0.6)  # images: a cross-fade
                    cur = nxt
        self.wait(0.3)
        self.remove(dot, cnt)
        self.clear_scene()

    # ------------------------------------------------------------------
    def composition(self):
        d = load("induction")
        steps = np.asarray(d["comp_steps"], float)
        CK, CQ = np.asarray(d["comp_k"]), np.asarray(d["comp_q"])  # checkpoint, layer-1 head, layer-2 head
        hp, hi = int(d["prev_head"]), int(d["ind_head"])
        base, bsd = float(d["comp_base"]), float(d["comp_base_sd"])
        js = int(d["jump_step"])
        f = cmath(r"\text{K-comp}(h_1 \to h_2)", r"=", r"\frac{\| W_{QK}^{h_2}\, W_{OV}^{h_1} \|_F}{\|W_{QK}^{h_2}\|_F\, "
                  r"\|W_{OV}^{h_1}\|_F}", font_size=34, colors={r"\text{K-comp}(h_1 \to h_2)": A}).move_to([0, 2.9, 0])
        fl = label(r"how much the later head's keys read what the earlier head wrote", font_size=22, color=GREY_A)
        fl.next_to(f, DOWN, buff=0.2)
        top = float(max(CK.max(), CQ.max()) * 1.15)
        g = axes([0, steps[-1], 1000], [0, top, top / 4], x_length=7.0, y_length=3.2, xlabel=r"training steps",
                 ylabel=r"composition score", xticks=list(range(0, int(steps[-1]) + 1, 1000)),
                 xfmt=lambda v: f"{int(v):,}".replace(",", "{,}"), yticks=[0, round(top / 2, 2)],
                 yfmt=lambda v: f"{v:.2f}", center=[-2.2, -1.25, 0])
        ax = g.ax
        bnd = Rectangle(width=ax.c2p(steps[-1], 0)[0] - ax.c2p(0, 0)[0], height=ax.c2p(0, 2 * bsd)[1] - ax.c2p(0, 0)[1],
                        stroke_width=0, fill_color=GREY_B, fill_opacity=0.2).move_to(ax.c2p(steps[-1] / 2, base))
        bl = label(r"random heads", font_size=18, color=GREY_B).next_to(bnd, RIGHT, buff=0.1)
        # the circuit: every previous-token head of layer 1 paired with every induction head of layer 2
        pv, iv = np.asarray(d["prev_scores"]), np.asarray(d["ind_scores"])
        P_ = [h for h in range(len(pv)) if pv[h] > 0.2] or [hp]
        I_ = [h for h in range(len(iv)) if iv[h] > 0.3] or [hi]
        inc = np.zeros(CK.shape[1:], bool)
        inc[np.ix_(P_, I_)] = True
        k_c, q_c = CK[:, inc].mean(1), CQ[:, inc].mean(1)
        k_o = CK[:, ~inc].mean(1)
        kk = curve(ax, steps, k_c, A, 3.5)
        qq = curve(ax, steps, q_c, Q, 2.5)
        oth = curve(ax, steps, k_o, GREY_B, 2)
        jl = DashedLine(ax.c2p(js, 0), ax.c2p(js, top), color=A, stroke_width=1.2)
        key = VGroup(label(r"K-composition: \ previous-token heads $\to$ induction heads", font_size=19, color=A),
                     label(r"Q-composition, \ same pairs", font_size=19, color=Q),
                     label(r"K-composition, \ every other pair", font_size=19, color=GREY_B),
                     note(rf"means over pairs; \ ${len(P_)}$ previous-token and ${len(I_)}$ induction heads; \\ "
                          r"first seed, \ every 250 steps", font_size=16))
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.6, -0.4, 0])
        keep_in_frame(key)
        # what the formula measures, drawn where the key will go: the earlier head writes, the later head's keys read
        w1 = VGroup(label(r"the earlier head $h_1$ writes", font_size=19, color=K),
                    MathTex(r"W_{OV}^{h_1}\, x", font_size=30, color=K)).arrange(DOWN, buff=0.1)
        w2 = VGroup(label(r"the later head $h_2$'s keys read", font_size=19, color=A),
                    MathTex(r"W_{QK}^{h_2}\,\big(W_{OV}^{h_1}\, x\big)", font_size=30, color=A)).arrange(DOWN, buff=0.1)
        arr = VGroup(Arrow(UP * 0.35, DOWN * 0.35, color=GREY_B, stroke_width=2.5, buff=0),
                     label(r"the residual stream", font_size=16, color=GREY_B)).arrange(RIGHT, buff=0.15)
        sch = VGroup(w1, arr, w2).arrange(DOWN, buff=0.2).move_to([4.5, -0.6, 0])
        keep_in_frame(sch)
        k0, k1 = float(k_c[0]), float(k_c[-1])
        q1, o1 = float(q_c[-1]), float(k_o[-1])
        n_p, n_i = len(P_), len(I_)
        v = (f"For the {n_p} previous-token heads paired with the {n_i} induction heads, it climbs from {k0:.2f} to "
             f"{k1:.2f} as the induction heads form; Q-composition over the same pairs ends at {q1:.2f}, every other "
             f"pair at {o1:.2f}. The induction heads' keys read what the previous-token heads wrote."
             if k1 > max(q1, o1) + 2 * bsd else
             f"For the {n_p} previous-token heads paired with the {n_i} induction heads, it ends at {k1:.2f}, against "
             f"{q1:.2f} for Q-composition and {o1:.2f} for every other pair: in this small model the signal is not "
             "cleanly in the keys.")
        with self.voiceover(
            "The cooperation shows in the weights alone. <bookmark mark='a'/> K-composition, from Nelson Elhage and "
            "colleagues, measures how much a later head's keys read what an earlier head writes: the size of the "
            "product of its QK matrix and the earlier head's OV matrix, relative to their sizes. Random heads score "
            f"about {base:.2f}. <bookmark mark='b'/> {v}"
        ) as vo:
            self.play(FadeIn(f), FadeIn(fl))
            vo.wait_until("a")
            self.play(FadeIn(g), FadeIn(bnd), FadeIn(bl), Create(jl), FadeIn(w1))
            self.play(GrowArrow(arr[0]), FadeIn(arr[1]), FadeIn(w2))
            vo.wait_until("b")
            self.play(FadeOut(sch))
            self.play(Create(kk), Create(qq), Create(oth), FadeIn(key), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ours(self):
        t, hd = load("tf"), load("heads")
        ind = np.asarray(t["text_induction"])  # layer, head
        L, H = ind.shape
        li, hi = int(t["text_ind_layer"]), int(t["text_ind_head"])
        CK = np.asarray(hd["comp_k"])
        base, bsd = float(hd["comp_base"]), float(hd["comp_base_sd"])
        steps = [int(v) for v in t["snap_steps"]]
        si = np.asarray(t["snap_induction"]).reshape(len(steps), -1).max(1)
        c1, c2 = np.asarray(t["snap_copy1"]), np.asarray(t["snap_copy2"])
        tokens = int(t["tokens"])
        # K-composition between our heads: rows earlier heads, columns later heads (only earlier-to-later pairs)
        M = np.nan_to_num(CK, nan=0.0)
        top = float(np.nanmax(CK))
        img = framed(heat_image(np.clip(M - base, 0, None), 3.4, 3.4, color=A, gamma=0.7)).move_to([-4.0, -0.6, 0])
        il = label(r"K-composition between our heads, \\ above the random level", font_size=20, color=GREY_A)
        il.next_to(img, UP, buff=0.15)
        rl = label(r"earlier head", font_size=18, color=GREY_B).rotate(PI / 2).next_to(img, LEFT, buff=0.12)
        cl = label(r"later head", font_size=18, color=GREY_B).next_to(img, DOWN, buff=0.12)
        # first: what an induction head looks like (the toy's, with its stripe) beside our best candidate, reading a
        # stretch of a novel shown twice; dashed, where an induction head would look
        di = load("induction")
        S_ = 2.5
        toy = framed(heat_image(np.asarray(di["map_ind"]), S_, S_, color=A, mask_upper=True))
        TM = np.asarray(t["text_ind_map"])
        N2 = TM.shape[0]
        n_ = N2 // 2
        mine = framed(heat_image(TM, S_, S_, color=A, mask_upper=True))
        Group(toy, mine).arrange(RIGHT, buff=0.5).move_to([-3.85, -0.45, 0])
        ul = mine[0].get_corner(UL)

        def px(r, c):
            return ul + RIGHT * (c + 0.5) * S_ / N2 + DOWN * (r + 0.5) * S_ / N2

        stripe = DashedLine(px(n_ + 4, 5), px(N2 - 2, n_ - 1), color=GREY_A, stroke_width=1.6, dash_length=0.06)
        toy_sc = float(np.asarray(di["ind_scores"])[int(di["ind_head"])])
        tl_ = label(rf"the toy's induction head: \\ ${toy_sc:.0%}$ one step after the copy".replace("%", r"\%"),
                    font_size=17, color=GREY_A).next_to(toy, UP, buff=0.12)
        ml_ = label(rf"ours, \ layer ${li + 1}$, head ${hi + 1}$: \\ ${ind.max():.1%}$ one step after the copy"
                    .replace("%", r"\%"), font_size=17, color=GREY_A).next_to(mine, UP, buff=0.12)
        sl_ = label(r"dashed: \ where an induction head would look", font_size=16, color=GREY_B).next_to(mine, DOWN, buff=0.12)
        cap_ = label(r"random tokens, \ repeated", font_size=16, color=GREY_B).next_to(toy, DOWN, buff=0.12)
        indg = Group(toy, mine, tl_, ml_, cap_)
        a_, b_ = np.unravel_index(int(np.nanargmax(CK)), CK.shape)
        lo = float(min(c1.min(), c2.min())) - 0.2
        hi_ = float(min(max(c1[1:].max(), c2[1:].max()) + 0.2, lo + 3.0))
        g = axes([0, steps[-1], 1000], [lo, hi_, 0.5], x_length=5.4, y_length=3.0, xlabel=r"training steps",
                 ylabel=r"bits per character on a stretch shown twice", xticks=[0, steps[-1]],
                 xfmt=lambda v: f"{int(v):,}".replace(",", "{,}"), yticks=[round(lo + 0.2, 1), round(hi_ - 0.2, 1)],
                 yfmt=lambda v: f"{v:.1f}", center=[2.6, -0.2, 0])
        k1 = curve(g.ax, steps[1:], np.clip(c1[1:], lo, hi_), GREY_B, 3)
        k2 = curve(g.ax, steps[1:], np.clip(c2[1:], lo, hi_), C.BITS, 2.5)
        key = VGroup(label(r"first time", font_size=18, color=GREY_B), label(r"second time", font_size=18, color=C.BITS))
        key.arrange(RIGHT, buff=0.5).next_to(g, DOWN, buff=0.2)
        strong = float(ind.max()) > 0.3
        if strong:
            v1 = (f"Our transformer has one: layer {li + 1}'s head {hi + 1} puts {ind.max():.0%} of its attention, on "
                  "average, exactly where an induction head should, one step after the earlier copy. ")
        else:
            v1 = (f"Our transformer has none: its best candidate, layer {li + 1}'s head {hi + 1}, puts {ind.max():.1%} "
                  f"of its attention one step after the earlier copy, and at the end the second copy costs "
                  f"{c2[-1]:.2f} bits a character, the first {c1[-1]:.2f}. ")
        v2 = (f"Its heads compose a little, at most {top:.2f} against {base:.2f} for random heads, but no pair has "
              "become a copying circuit. " if top > base + 4 * bsd else
              f"And its heads barely compose: at most {top:.2f}, against {base:.2f} for random heads. ")
        jmax = max(int(v) for v in di["jump_steps"])
        formed = max(float(v) for v in di["final2"]) < 0.5 * float(np.asarray(di["curve1"])[-1, 1])
        if strong:
            v3 = ""
        elif formed:
            v3 = (f"Why not? Olsson's team saw induction heads appear after two and a half to five billion tokens; "
                  f"ours has read {tokens / 1e6:.0f} million characters, and a novel rarely repeats a long stretch "
                  f"within 256 characters. The toy, built to reward copying, formed its pair within {jmax:,} steps.")
        else:
            v3 = (f"Why not? Olsson's team saw induction heads appear after two and a half to five billion tokens; "
                  f"ours has read {tokens / 1e6:.0f} million characters, and a novel rarely repeats a long stretch "
                  "within 256 characters.")
        with self.voiceover(
            "And our own transformer, trained on novels with no copying game at all? <bookmark mark='a'/> " + v1
            + "<bookmark mark='b'/> " + v2 + "<bookmark mark='c'/> " + v3
        ) as vo:
            self.play(FadeIn(g), FadeIn(key), Create(k1), Create(k2), FadeIn(indg), run_time=2.0)
            vo.wait_until("a")
            self.play(Create(stripe), FadeIn(sl_), Indicate(key, color=C.BITS))
            vo.wait_until("b")
            self.play(FadeOut(indg), FadeOut(stripe), FadeOut(sl_))
            self.play(FadeIn(img), FadeIn(il), FadeIn(rl), FadeIn(cl))
            vo.wait_until("c")
            self.play(Indicate(il, color=A))
        self.wait(0.3)
        self.clear_scene()
