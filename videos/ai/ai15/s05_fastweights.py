from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai15.common import (ADD, HIST, K, PART, STATE, V, bits_grid, curve, heat_image, load, signed_column,
                                   signed_grid)


class FastWeights(VoiceoverScene):
    def construct(self):
        self.card()
        self.hopfield()
        self.capacity()
        self.lineage()
        self.written()
        self.crosstalk()

    def card(self):
        card = chapter_card(4, r"A matrix that remembers", r"How can a matrix store and return memories?", lit=(1949, 1982),
                            part=PART)
        with self.voiceover("Chapter four. A matrix that remembers."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def hopfield(self):
        h = load("hopfield")
        frames = np.asarray(h["ex_frames"])
        pats = np.asarray(h["ex_patterns"])
        en = np.asarray(h["ex_energy"])
        N = int(h["N"])
        d = definition_card(r"Hopfield network", r"$N$ neurons of $\pm 1$; \ store patterns $\xi$ by Hebb's rule, "
                            r"$W = \tfrac1N \sum_\mu \xi^\mu \xi^{\mu\top}$; \ recall: \ set each neuron to the sign of "
                            r"$W s$, \ one at a time, \ until nothing changes", color=HIST, width=6.6, font_size=21)
        d.to_corner(UL, buff=0.3)
        stored = VGroup(*[bits_grid(p, size=0.85) for p in pats]).arrange(RIGHT, buff=0.18)
        sl = label(rf"${len(pats)}$ stored patterns of ${N}$ neurons", font_size=20, color=GREY_A)
        st = VGroup(stored, sl.next_to(stored, DOWN, buff=0.12)).to_corner(UR, buff=0.4)
        cue = bits_grid(frames[0], size=2.6).move_to([-3.4, -1.6, 0])
        cl = label(r"the cue: \ pattern 1, \ $30$ of $100$ bits flipped", font_size=20, color=GREY_A).next_to(cue, DOWN, buff=0.15)
        g = axes([0, len(en) - 1], [float(en.min()) * 1.05, float(en.max()) * 0.9 if en.max() < 0 else float(en.max())],
                 x_length=4.6, y_length=2.6, xlabel=r"updates, \ in fives", ylabel=r"energy \ $E = -\tfrac12 s^{\top} W s$",
                 center=[2.6, -1.5, 0])
        ax = g.ax
        dot = Dot(ax.c2p(0, en[0]), radius=0.06, color=HIST)
        path = VMobject(color=HIST, stroke_width=3).set_points_as_corners([ax.c2p(0, en[0]), ax.c2p(0, en[0]) + 1e-4 * RIGHT])
        cite_ = cite(r"J.~J.~Hopfield, \textit{PNAS} (1982); \ D.~O.~Hebb (1949)", corner=DR)
        with self.voiceover(
            "A memory you return to by its content is old. In 1982 John Hopfield described a network of neurons, "
            "each plus or minus one, that stores patterns in its connections by Hebb's rule from 1949: neurons that "
            "fire together wire together, a sum of outer products of the patterns with themselves. "
            "<bookmark mark='a'/> We stored five random patterns of a hundred neurons. <bookmark mark='b'/> Give it "
            "the first one with thirty bits flipped, and let each neuron in turn take the sign of its input. "
            "<bookmark mark='c'/> Every update can only lower an energy, so the state rolls downhill into the nearest "
            "valley: the stored pattern, recovered from a damaged copy."
        ) as vo:
            self.play(FadeIn(d, shift=UP * 0.1), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(st))
            vo.wait_until("b")
            self.play(FadeIn(cue), FadeIn(cl), FadeIn(g), FadeIn(dot))
            vo.wait_until("c")
            pts = [ax.c2p(0, en[0])]
            for k in range(1, len(frames)):
                pts.append(ax.c2p(k, en[min(k, len(en) - 1)]))
                self.play(Transform(cue, bits_grid(frames[k], size=2.6).move_to(cue)),
                          Transform(path, VMobject(color=HIST, stroke_width=3).set_points_as_corners(pts)),
                          dot.animate.move_to(pts[-1]), run_time=0.25, rate_func=linear)
            self.play(Indicate(stored[0], color=HIST, scale_factor=1.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def capacity(self):
        h = load("hopfield")
        N = int(h["N"])
        r = np.asarray(h["Ps"], float) / N
        fr, ov = np.asarray(h["frac"]), np.asarray(h["overlap"])
        g = axes([0, 0.34], [0, 1.0], x_length=7.4, y_length=4.0, xlabel=r"patterns stored per neuron, \ $P/N$",
                 ylabel=rf"cues recalled exactly \ ($N = {N}$, \ ${int(h['flips'])}$ bits flipped, \ ${int(h['trials'])}$ "
                 r"trials each)", xticks=[0, 0.1, 0.2, 0.3], yticks=[0, 0.5, 1], center=[-1.6, -0.4, 0])
        ax = g.ax
        c1 = curve(ax, r, fr, HIST, 4)
        c2 = DashedVMobject(curve(ax, r, ov, GREY_B, 2.5), num_dashes=40)
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.05, color=HIST) for x, y in zip(r, fr)])
        lim = DashedLine(ax.c2p(0.138, 0), ax.c2p(0.138, 1.0), dash_length=0.07, color=C.BITS, stroke_width=2)
        ll = label(r"$0.138$: \ the limit for large $N$ \\ (Amit, Gutfreund \& Sompolinsky, 1985)", font_size=18,
                   color=C.BITS).next_to(lim.get_top(), RIGHT, buff=0.1).shift(DOWN * 0.3)
        k1 = label(r"exactly recalled", font_size=20, color=HIST)
        k2 = label(r"overlap with the pattern", font_size=20, color=GREY_B)
        keys = VGroup(k1, k2).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.6, 1.3, 0])
        half = float(np.interp(0.5, fr[::-1], r[::-1]))
        with self.voiceover(
            "But a matrix of N by N numbers can't hold many patterns this way. <bookmark mark='a'/> As we store more, "
            "the patterns start to interfere: the valleys merge, and spurious ones appear. With a hundred neurons, "
            f"half the cues come back exactly at about {half:.2f} patterns per neuron, and the theory for large "
            "networks puts the limit at 0.138. <bookmark mark='b'/> Remember this: storing by adding outer products "
            "fills up. It will come back as crosstalk in a moment."
        ) as vo:
            self.play(FadeIn(g), FadeIn(keys))
            vo.wait_until("a")
            self.play(Create(c1), FadeIn(dots), Create(c2), run_time=2.0)
            self.play(Create(lim), FadeIn(ll))
            vo.wait_until("b")
            self.play(Indicate(c1, color=WHITE, scale_factor=1.02))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lineage(self):
        head = label(r"From patterns to keys and values", font_size=36).to_edge(UP, buff=0.35)
        w, fs = 4.2, 20
        cards = VGroup(
            history_card(1972, r"correlation matrix memories", r"Kohonen; \ Anderson: \ store a value under a key, "
                         r"$M = \sum_i v_i k_i^{\top}$; \ read with $M k$", color=HIST, width=w, font_size=fs),
            history_card(1992, r"fast weights", r"Schmidhuber: \ a slow network writes, each step, the weights of a "
                         r"fast one, \ by outer products", color=HIST, width=w, font_size=fs),
            history_card(2016, r"fast weights, \ again", r"Ba, Hinton et al.: \ a recurrent network with a decaying "
                         r"outer-product memory of its recent past", color=HIST, width=w, font_size=fs),
            history_card(2014, r"neural Turing machines, \ memory networks", r"Graves; \ Weston, \ Sukhbaatar: \ a "
                         r"separate memory, read and written by attention", color=HIST, width=w, font_size=fs),
            history_card(2020, r"linear attention", r"Katharopoulos et al.: \ the transformer without the softmax is "
                         r"a recurrence on $\sum v k^{\top}$", color=HIST, width=w, font_size=fs),
            history_card(2021, r"``secretly fast weight programmers''", r"Schlag, Irie \& Schmidhuber: \ the same "
                         r"thing as 1992, \ and a better way to write", color=HIST, width=w, font_size=fs),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.25, 0.3), cell_alignment=UP)
        if cards.width > 13.4:
            cards.width = 13.4
        cards.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "The same sum of outer products became a memory of keys and values. In 1972 Teuvo Kohonen and James "
            "Anderson stored a value under a key as a matrix: add value times key transposed, and read with the key. "
            "<bookmark mark='a'/> In 1992 Jürgen Schmidhuber made it fast weights: a slow network that, at every "
            "step, writes outer products into the weights of a fast network, a memory of the sequence so far. "
            "<bookmark mark='b'/> In 2016 Jimmy Ba, Geoffrey Hinton and colleagues revived it as a decaying memory "
            "of the recent past. <bookmark mark='c'/> Meanwhile neural Turing machines and memory networks, which "
            "Part 10 met, kept a separate memory and addressed it with attention. <bookmark mark='d'/> And in 2020 "
            "linear attention, the last chapter's recurrence, turned out to be the same matrix. "
            "<bookmark mark='e'/> In 2021 Imanol Schlag, Kazuki Irie and Schmidhuber named it: linear transformers "
            "are secretly fast weight programmers, and they gave them a better way to write."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cards[0], shift=UP * 0.1))
            for k, m in enumerate("abcde"):
                vo.wait_until(m)
                self.play(FadeIn(cards[k + 1], shift=UP * 0.1), run_time=0.8)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def written(self):
        m = load("matrix_rw")
        keys, vals, seq = np.asarray(m["keys"]), np.asarray(m["vals"]), np.asarray(m["seq"]).astype(int)
        Ss = np.asarray(m["S_add"])
        reads = np.asarray(m["read_add"])
        errs = np.asarray(m["err_add"])
        d = int(m["d"])
        top = float(np.abs(Ss[:4]).max())
        vt = float(np.abs(vals).max())
        cell = 0.3
        S0 = signed_grid(np.zeros((d, d)), d * cell, top).move_to([-0.4, 0.2, 0])
        Sl = MathTex(r"S", font_size=34, color=STATE).next_to(S0, UP, buff=0.15)
        colors = {r"S": STATE, r"v_i": V, r"k_i": K, r"k_j": K}
        f = cmath(r"S", r"\;\mathrel{+}=\;", r"v_i", r"\,", r"k_i", r"^{\top}", colors=colors, font_size=36).to_corner(UL, buff=0.4)
        fr = cmath(r"\text{read: }", r"S", r"\,", r"k_j", colors=colors, font_size=36).next_to(f, DOWN, buff=0.25, aligned_edge=LEFT)
        kcol = signed_column(keys[0], cell, 1.0).move_to([-3.7, 0.2, 0])
        vcol = signed_column(vals[0], cell, vt).move_to([-4.6, 0.2, 0])
        kl = MathTex(r"k_1", font_size=28, color=K).next_to(kcol, UP, buff=0.12)
        vl = MathTex(r"v_1", font_size=28, color=V).next_to(vcol, UP, buff=0.12)
        times = MathTex(r"\times", font_size=30).move_to((kcol.get_center() + vcol.get_center()) / 2)
        arrow = Arrow(kcol.get_right(), S0.get_left(), buff=0.2, color=GREY_B, stroke_width=3)
        tag = note(rf"$d = {d}$: \ four keys nearly at right angles; \ blue $+$, \ red $-$").to_edge(DOWN, buff=0.3)
        # the read-back table
        rows = VGroup()
        for j in range(4):
            rows.add(VGroup(MathTex(rf"k_{j + 1}", font_size=26, color=K),
                            signed_column(reads[3][j], 0.16, vt).rotate(-PI / 2),
                            signed_column(vals[j], 0.16, vt).rotate(-PI / 2),
                            MathTex(f"{errs[3][j]:.2f}", font_size=24, color=ADD)).arrange(RIGHT, buff=0.25))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.6, -0.2, 0])
        rh = label(r"reads $S k_j$ \quad stored $v_j$ \quad error", font_size=18, color=GREY_A).next_to(rows, UP, buff=0.2)
        rh.align_to(rows, LEFT).shift(RIGHT * 0.5)
        e = errs[3]
        with self.voiceover(
            "Here is that memory at work, written and read one step at a time. The memory is a matrix S, eight by "
            "eight, empty at first. <bookmark mark='a'/> To store a value under a key, multiply them into an outer "
            "product, a grid of every value number times every key number, and add it on. <bookmark mark='b'/> Four "
            "keys, four values, four additions. <bookmark mark='c'/> To read, multiply the matrix by a key. Each key "
            "gets its own value back, plus a little of the others, in proportion to how much their keys overlap: "
            f"errors from {e.min():.2f} to {e.max():.2f} here, for keys that are nearly, but not quite, at right "
            "angles."
        ) as vo:
            self.play(FadeIn(S0), FadeIn(Sl), Write(f), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(kcol), FadeIn(vcol), FadeIn(kl), FadeIn(vl), FadeIn(times), GrowArrow(arrow))
            vo.wait_until("b")
            for i in range(4):
                kk, vv = seq[i]
                if i:
                    self.play(Transform(kcol, signed_column(keys[kk], cell, 1.0).move_to(kcol)),
                              Transform(vcol, signed_column(vals[vv], cell, vt).move_to(vcol)),
                              Transform(kl, MathTex(rf"k_{kk + 1}", font_size=28, color=K).move_to(kl)),
                              Transform(vl, MathTex(rf"v_{vv + 1}", font_size=28, color=V).move_to(vl)), run_time=0.5)
                outer = signed_grid(np.outer(vals[vv], keys[kk]), d * cell, top).move_to(kcol)
                self.play(FadeIn(outer, scale=0.5), run_time=0.4)
                self.play(outer.animate.move_to(S0).set_opacity(0), Transform(S0, signed_grid(Ss[i], d * cell, top).move_to(S0)),
                          run_time=0.8)
                self.remove(outer)
            vo.wait_until("c")
            self.play(Write(fr), FadeIn(rh))
            self.play(LaggedStart(*[FadeIn(r_, shift=LEFT * 0.1) for r_ in rows], lag_ratio=0.3), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def crosstalk(self):
        c = load("capacity")
        d = int(c["d"])
        Ns = np.asarray(c["Ns"], float)
        colors = {r"S": STATE, r"k_j": K, r"v_j": V, r"v_i": V, r"k_i": K}
        f = cmath(r"S", r"\,", r"k_j", "=", r"v_j", "+", r"\sum_{i \ne j}", r"v_i", r"\,(", r"k_i", r"\cdot", r"k_j", r")",
                  colors=colors, font_size=40).to_edge(UP, buff=0.45)
        b = Brace(VGroup(*f[5:]), DOWN, color=ADD)
        bl = label(r"crosstalk: \ every other pair leaks in", font_size=24, color=ADD).next_to(b, DOWN, buff=0.08)
        top = math.ceil(max(float(np.max(c["err_add"])), (Ns[-1] - 1) / d) * 2) / 2
        g = axes([0, Ns[-1]], [0, top], x_length=6.2, y_length=3.6, xlabel=r"pairs stored, \ $N$",
                 ylabel=r"error reading them back \ (relative)", xticks=[0, 64, 128, 192, 256],
                 yticks=list(range(int(top) + 1)), center=[-2.6, -1.25, 0])
        ax = g.ax
        ca = curve(ax, Ns, np.asarray(c["err_add"]), ADD, 4)
        th = DashedLine(ax.c2p(1, 0), ax.c2p(Ns[-1], (Ns[-1] - 1) / d), color=GREY_B, stroke_width=1.5)
        thl = MathTex(r"\tfrac{N-1}{d}", font_size=30, color=GREY_B).next_to(ax.c2p(110, 110 / d), DR, buff=0.12)
        note_ = label(rf"$d = {d}$: \ by $N = {d}$ pairs, \\ the leaks are as big \\ as the answer", font_size=26,
                      color=ADD).move_to([4.2, -0.9, 0])
        gk = np.random.default_rng(12)
        ks = gk.normal(size=(128, d))
        ks /= np.linalg.norm(ks, axis=1, keepdims=True)

        def gram(n):
            img = heat_image(np.abs(ks[:n] @ ks[:n].T), 3.4, 3.4, color=ADD, gamma=0.5).move_to([-1.6, -1.35, 0])
            lab = label(rf"$|k_i \cdot k_j|$ \ for ${n}$ random keys, \ $d = {d}$", font_size=22, color=GREY_A)
            return Group(img, lab.next_to(img, UP, buff=0.12))

        gr = gram(16)
        with self.voiceover(
            "With many pairs, that leak is the whole story. <bookmark mark='a'/> Read pair j, and you get its value "
            "plus every other value, weighted by how much its key overlaps key j. Random keys in d dimensions overlap "
            "by about one over the square root of d, <bookmark mark='b'/> so the leaks add up like N over d. With d "
            f"equal to {d}, by {d} pairs the noise is as big as the answer: the same filling-up as Hopfield's network. "
            "Adding can never erase."
        ) as vo:
            self.play(Write(f), FadeIn(gr))
            vo.wait_until("a")
            self.play(GrowFromCenter(b), FadeIn(bl))
            g48, g128 = gram(48), gram(128)
            self.play(FadeOut(gr), FadeIn(g48), run_time=1.0)  # a cross-fade: FadeTransform can't restore images
            self.wait(0.3)
            self.play(FadeOut(g48), FadeIn(g128), run_time=1.0)
            vo.wait_until("b")
            self.play(FadeOut(g128))
            self.play(FadeIn(g), Create(th), FadeIn(thl))
            self.play(Create(ca), run_time=2.0)
            e_d = float(np.interp(d, Ns, np.asarray(c["err_add"])))
            pt = Dot(ax.c2p(d, e_d), radius=0.08, color=ADD)
            gl = VGroup(DashedLine(ax.c2p(d, 0), ax.c2p(d, e_d), dash_length=0.06, stroke_width=1.5, color=ADD),
                        DashedLine(ax.c2p(0, e_d), ax.c2p(d, e_d), dash_length=0.06, stroke_width=1.5, color=ADD))
            self.play(Create(gl), FadeIn(pt, scale=2), FadeIn(note_), Flash(pt, color=ADD, flash_radius=0.3))
        self.wait(0.3)
        self.clear_scene()
