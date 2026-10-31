from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai13.common import A, HIST, K, PART, Q, V, curve, framed, load, pattern_image

SIDE = 10  # the stored letters are 10 x 10
CLASSIC = C.SURPRISE
MODERN = A


class Hopfield(VoiceoverScene):
    def construct(self):
        self.card()
        self.classical()
        self.capacity()
        self.modern()
        self.temperature()

    def card(self):
        card = chapter_card(2, r"A memory that recalls", r"How can a network recall a whole pattern from a fragment?",
                            lit=(1982,), part=PART)
        with self.voiceover("Chapter two. A memory that recalls."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def letters_row(self, pats, y, width=0.95, buff=0.18, color=WHITE):
        row = Group(*[framed(pattern_image(p, SIDE, width, ink=color)) for p in pats])
        return row.arrange(RIGHT, buff=buff).move_to([0, y, 0])

    def classical(self):
        h = load("hopfield")
        L = np.asarray(h["letters"])
        hist = history_card(1982, r"John Hopfield", r"\textit{Neural networks and physical systems with emergent "
                            r"collective computational abilities}", color=HIST, width=5.6).to_corner(UL, buff=0.35)
        rows = [
            cmath(r"W", r"=", r"\tfrac{1}{N}\sum_\mu \xi^\mu \xi^{\mu\top}", font_size=36,
                  colors={r"\tfrac{1}{N}\sum_\mu \xi^\mu \xi^{\mu\top}": K}),
            cmath(r"x_i", r"\leftarrow", r"\operatorname{sign}\Big(\sum_j W_{ij}\, x_j\Big)", font_size=36),
            cmath(r"E(x)", r"=", r"-\tfrac12\, x^\top W x", font_size=36),
        ]
        whys = [why(r"store: \ strengthen every pair \\ that fires together (Hebb)", font_size=20),
                why(r"recall: \ each unit follows \\ the vote of the others", font_size=20),
                why(r"one unit at a time, \ $W_{ii}=0$: \\ each flip cannot raise $E$", font_size=20)]
        eqs = VGroup(*rows).arrange(DOWN, buff=0.42, aligned_edge=LEFT).move_to([2.6, 1.55, 0])
        for r_, w_ in zip(rows, whys):
            w_.next_to(r_, RIGHT, buff=0.35)
        if max(w_.get_right()[0] for w_ in whys) > 6.9:
            g = VGroup(eqs, *whys)
            g.shift(LEFT * (max(w_.get_right()[0] for w_ in whys) - 6.9))
        stored = self.letters_row(L, -0.8, width=0.78)
        sl = label(rf"${len(L)}$ letters stored, \ each ${SIDE} \times {SIDE} = {SIDE * SIDE}$ units of $\pm 1$",
                   font_size=22, color=GREY_A).next_to(stored, DOWN, buff=0.15)
        cue_i = 3
        cue = framed(pattern_image(np.asarray(h["cues"])[cue_i], SIDE, 1.25))
        rc = framed(pattern_image(np.asarray(h["rec_classical"])[cue_i], SIDE, 1.25, ink=CLASSIC))
        trio = Group(cue, rc).arrange(RIGHT, buff=1.4).move_to([0, -2.75, 0])
        arr = Arrow(cue.get_right(), rc.get_left(), buff=0.15, color=GREY_B, stroke_width=3)
        cl = label(r"a cue: \\ $25\%$ of the units flipped", font_size=22, color=GREY_A).next_to(cue, LEFT, buff=0.3)
        rl = label(r"after the updates \\ settle", font_size=22, color=CLASSIC).next_to(rc, RIGHT, buff=0.3)
        ok = int(h["letters_ok_classical"])
        n = len(L)
        verdict = (f"It recovers {ok} of the {n} letters exactly. The others settle into blends: our letters "
                   "share too many pixels, and their memories run into each other."
                   if ok < n else f"It recovers all {n} letters exactly, every pixel in place.")
        with self.voiceover(
            "In 1982 the physicist John Hopfield described a network that remembers. <bookmark mark='a'/> Store "
            "some patterns of plus and minus ones by strengthening every pair of units that are on together: "
            "Hebb's rule, from Part 9. <bookmark mark='b'/> To recall, start from a cue and let each unit take the "
            "sign of the weighted vote of the others, updating one unit at a time and setting self-weights to zero. <bookmark mark='c'/> Each flip cannot raise an energy, so "
            "recall rolls downhill, into the nearest stored pattern, if all goes well. <bookmark mark='d'/> Here we "
            f"store {n} letters, a hundred units each. <bookmark mark='e'/> Give it a letter with a quarter of its "
            f"pixels flipped, and let it settle. {verdict}"
        ) as vo:
            self.play(FadeIn(hist, shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]),
                      LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in stored], lag_ratio=0.08))
            vo.wait_until("b")
            self.play(Write(rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(Write(rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(FadeIn(sl), Indicate(stored, scale_factor=1.03, color=WHITE))
            vo.wait_until("e")
            self.play(FadeIn(cue), FadeIn(cl))
            self.play(GrowArrow(arr), FadeIn(rc), FadeIn(rl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def capacity(self):
        h = load("hopfield")
        Ms = np.asarray(h["Ms"], float)
        cl, md = np.asarray(h["classical"]), np.asarray(h["modern"])
        N = int(h["N"])
        g = axes([0, np.log10(400), 1], [0, 1.05, 0.5], x_length=8.2, y_length=4.2,
                 xlabel=r"patterns stored", ylabel=r"recalled exactly, \ from a cue with $15\%$ flipped",
                 xticks=[], yticks=[0, 0.5, 1], yfmt=lambda v: f"{100 * v:.0f}\\%", center=[-1.6, -0.3, 0])
        ax = g.ax
        for m in (1, 10, 100):
            g.add(MathTex(str(m), font_size=20, color=GREY_B).next_to(ax.c2p(np.log10(m), 0), DOWN, buff=0.12))
        lx = np.log10(Ms)
        c_cl = VGroup(curve(ax, lx, cl, CLASSIC, 3.5), *[Dot(ax.c2p(a, b), radius=0.05, color=CLASSIC) for a, b in zip(lx, cl)])
        c_md = VGroup(curve(ax, lx, md, MODERN, 3.5), *[Dot(ax.c2p(a, b), radius=0.05, color=MODERN) for a, b in zip(lx, md)])
        cap = float(h["capacity_classical"])
        capl = DashedLine(ax.c2p(np.log10(cap), 0), ax.c2p(np.log10(cap), 1.05), color=CLASSIC, stroke_width=1.5)
        capt = label(rf"$0.138\,N = {cap:.0f}$", font_size=20, color=CLASSIC).next_to(ax.c2p(np.log10(cap), 0.85), RIGHT,
                                                                                      buff=0.12)
        key = legend([(CLASSIC, r"Hopfield (1982): \ sign updates"), (MODERN, r"one softmax step")], font_size=22)
        key.move_to([4.9, 1.6, 0])
        test = label(rf"each test: \ store $M$ random patterns \\ of ${N}$ units; \ flip $15\%$ of one; \\ "
                     r"does recall return it \\ exactly?", font_size=22, color=GREY_A).move_to([4.9, -0.4, 0])
        half = next((m for m, v in zip(Ms, cl) if v < 0.5), None)
        dead = next((m for m, v in zip(Ms, cl) if v == 0), None)
        allm = bool(np.all(md >= 0.999))
        tail = (f"Store {int(Ms[-1])} patterns, {Ms[-1] / N:.1f} times the number of units, and one softmax step "
                "still recalls every tested cue." if allm else
                f"It holds on far longer: at {int(Ms[-1])} patterns it still recalls {md[-1]:.0%}.")
        note_ = note(rf"$N = {N}$ units; \ random patterns; \ ${int(h['trials'])}$ trials each").to_corner(DR, buff=0.3)
        cite_ = cite(r"Amit, Gutfreund \& Sompolinsky (1985); \ Krotov \& Hopfield (2016); \ Demircigil et al.\ (2017)",
                     corner=DL)
        none_txt = f"and by {int(dead)} it recalls none at all." if dead else "but it never fails completely."
        h_at = int(half) if half else int(Ms[-1])
        with self.voiceover(
            "How much can it hold? Store more and more random patterns in a hundred units, and test each with a cue "
            f"in which fifteen percent of the units are flipped. <bookmark mark='a'/> The classical network "
            f"falls below half its patterns at {h_at} stored patterns, " + none_txt
            + " Physicists computed its limit in 1985: about zero point one three eight patterns per unit. Every "
            "stored pattern adds a little noise to every other's vote, and the noise adds up. "
            "<bookmark mark='b'/> In 2016 Dmitry Krotov and John Hopfield sharpened the energy so that the closest "
            "pattern wins by far more, and in 2017 a team showed that an exponential energy stores exponentially "
            f"many patterns. <bookmark mark='c'/> {tail}"
        ) as vo:
            self.play(FadeIn(g), FadeIn(note_), FadeIn(test))
            vo.wait_until("a")
            self.play(Create(c_cl[0]), FadeIn(c_cl[1:]), Create(capl), FadeIn(capt), FadeIn(key[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(cite_))
            vo.wait_until("c")
            self.play(Create(c_md[0]), FadeIn(c_md[1:]), FadeIn(key[1]), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def modern(self):
        h = load("hopfield")
        L = np.asarray(h["letters"])
        n = len(L)
        colors = {r"\xi": Q, r"X": K, r"X^\top": K, r"\beta": A}
        rows = [
            cmath(r"E(\xi)", r"=", r"-\tfrac{1}{\beta}\log\sum_\mu e^{\,\beta\, x_\mu \cdot \xi}", r"+", r"\tfrac12\,\xi\cdot\xi",
                  font_size=34, colors=colors),
            cmath(r"\xi_{\text{new}}", r"=", r"\sum_\mu", r"\operatorname{softmax}_\mu\big(\beta\, x_\mu \cdot \xi\big)",
                  r"\, x_\mu", font_size=34, colors=colors),
            cmath(r"\operatorname{Attn}(q)", r"=", r"\sum_i", r"\operatorname{softmax}_i\big(q \cdot k_i / \sqrt{d}\big)",
                  r"\, v_i", font_size=34, colors={r"\operatorname{Attn}(q)": A}),
        ]
        whys = [why(r"modern Hopfield energy", font_size=20),
                why(r"one update step \\ (concave--convex procedure)", font_size=20),
                why(r"the cue is the query; \\ the patterns are keys and values; \\ $\beta = 1/\sqrt{d}$", font_size=20)]
        step = ladder(self, rows, whys, keep=3, top=3.0, x=-2.6, buff=0.62, edge=6.9)
        # the update drawn as attention, on the letters
        cue_i = 3
        keys = Group(*[framed(pattern_image(p, SIDE, 0.62)) for p in L]).arrange(RIGHT, buff=0.12).move_to([0.6, -1.35, 0])
        cue = framed(pattern_image(np.asarray(h["cues"])[cue_i], SIDE, 1.1, ink=Q)).move_to([-5.6, -1.75, 0])
        cl = label(r"cue $=$ query", font_size=20, color=Q).next_to(cue, UP, buff=0.12)
        x = np.asarray(h["cues"])[cue_i]
        s = 0.2 * (L @ x)
        w = np.exp(s - s.max())
        w /= w.sum()
        bars = VGroup(*[Rectangle(width=0.5, height=max(0.9 * float(v), 0.01), stroke_width=0, fill_color=A,
                                  fill_opacity=0.9).next_to(k_, DOWN, buff=0.12) for k_, v in zip(keys, w)])
        for b_ in bars:
            b_.align_to(bars[0], UP)
        out = framed(pattern_image(np.asarray(h["rec_modern"])[cue_i], SIDE, 1.1, ink=MODERN)).move_to([5.9, -1.75, 0])
        ol = label(r"recalled", font_size=20, color=MODERN).next_to(out, UP, buff=0.12)
        kl = label(r"stored letters: \ keys and values", font_size=20, color=K).next_to(keys, UP, buff=0.12)
        ok_m = int(h["letters_ok_modern"])
        th = theorem_card(r"modern Hopfield networks", r"well-separated patterns, \ a nearby cue: \ one update "
                          r"retrieves with error exponentially small in the separation. \ Random patterns on a "
                          r"suitably scaled sphere can have exponential capacity in the dimension.",
                          who=r"H.~Ramsauer, S.~Hochreiter et al.\ (2020)", width=6.4, font_size=20)
        th.move_to([0, -1.9, 0])
        with self.voiceover(
            "In 2020 Hubert Ramsauer, Sepp Hochreiter and colleagues made the states continuous. "
            "<bookmark mark='a'/> The energy becomes minus a log-sum-exp of the overlaps with the stored patterns, "
            "plus a small term that keeps the state bounded. <bookmark mark='b'/> Minimize it one step at a time and "
            "the update is: weight every stored pattern by a softmax of its overlap with the current state, and add "
            "them up. <bookmark mark='c'/> Look at that formula. It is attention. The cue is the query, the stored "
            "patterns are both the keys and the values, and beta plays the part of one over the square root of d. "
            f"<bookmark mark='d'/> On our letters, one step recalls {ok_m} of {n}. <bookmark mark='e'/> And they "
            "proved that one step suffices for a nearby cue when the patterns are sufficiently separated. The paper's title: Hopfield Networks is All You Need."
        ) as vo:
            step(0)
            self.play(FadeIn(keys), FadeIn(kl))
            vo.wait_until("a")
            self.play(Indicate(rows[0][2], color=A))
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(FadeIn(cue), FadeIn(cl))
            self.play(LaggedStart(*[GrowFromEdge(b_, UP) for b_ in bars], lag_ratio=0.05), FadeIn(out), FadeIn(ol))
            vo.wait_until("e")
            self.play(FadeOut(Group(cue, cl, keys, kl, bars, out, ol)), FadeIn(th, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def temperature(self):
        h = load("hopfield")
        betas = np.asarray(h["betas"])
        ov = np.asarray(h["beta_overlap"])
        W = np.asarray(h["beta_weights"])
        tgt = int(h["beta_target"])
        g = axes([np.log10(betas[0]), 0, 1], [0, 1.05, 0.5], x_length=6.2, y_length=3.6,
                 xlabel=r"$\beta$, \ the inverse temperature", ylabel=r"overlap of the result with the cued pattern",
                 xticks=[], yticks=[0, 0.5, 1], center=[-3.3, -0.35, 0])
        ax = g.ax
        for e in (-2, -1, 0):
            g.add(MathTex(f"10^{{{e}}}", font_size=20, color=GREY_B).next_to(ax.c2p(e, 0), DOWN, buff=0.12))
        lb = np.log10(betas)
        c_ = curve(ax, lb, ov, A, 3.5)
        picks = [int(np.argmin(np.abs(betas - b))) for b in (0.004, 0.03, 0.3)]
        panels = VGroup()
        for k, i in enumerate(picks):
            w = W[i]
            bars = VGroup(*[Rectangle(width=0.16, height=max(1.2 * float(v) / max(w.max(), 1e-9), 0.01), stroke_width=0,
                                      fill_color=V if j == tgt else A, fill_opacity=0.9)
                            for j, v in enumerate(w)]).arrange(RIGHT, buff=0.04, aligned_edge=DOWN)
            base = Line(bars.get_corner(DL) + LEFT * 0.05, bars.get_corner(DR) + RIGHT * 0.05, color=GREY_C, stroke_width=1.5)
            t = MathTex(rf"\beta = {betas[i]:.3f}", font_size=22, color=GREY_A).next_to(base, DOWN, buff=0.1)
            panels.add(VGroup(bars, base, t))
        panels.arrange(DOWN, buff=0.35).move_to([3.9, -0.2, 0])
        dots = VGroup(*[Dot(ax.c2p(lb[i], ov[i]), radius=0.07, color=WHITE) for i in picks])
        pl = label(r"the weights on $20$ stored patterns \\ (the cued one in red)", font_size=20, color=GREY_A)
        pl.next_to(panels, UP, buff=0.2)
        small, big = ov[0], ov[-1]
        nobel = history_card(2024, r"The Nobel Prize in Physics", r"to John Hopfield and Geoffrey Hinton, "
                             r"\textit{for foundational discoveries and inventions that enable machine learning "
                             r"with artificial neural networks}", color=HIST, width=6.0).to_corner(UR, buff=0.3)
        with self.voiceover(
            "Beta, the inverse temperature, is the knob that turns this memory into chapter one's smoother. "
            f"<bookmark mark='a'/> Turn it down and the weights spread over every pattern: the result is an "
            f"average of everything, with an overlap of only {small:.2f} with the pattern that was cued. "
            "<bookmark mark='b'/> In between, it averages a few similar patterns, a blend Ramsauer's team called a "
            f"metastable state. <bookmark mark='c'/> Turn it up and one pattern takes all the weight: overlap "
            f"{big:.2f}. Attention lives on this curve, and the division by the square root of d sets where. "
            "<bookmark mark='d'/> In 2024 the Nobel Prize in Physics went to Hopfield and to Geoffrey Hinton for "
            "networks like these; Part 20 returns to their energies as a way to generate. A transformer head is a "
            "memory read: its query recalls from the keys, and returns a blend of the values."
        ) as vo:
            self.play(FadeIn(g), Create(c_), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(dots[0]), FadeIn(panels[0]), FadeIn(pl))
            vo.wait_until("b")
            self.play(FadeIn(dots[1]), FadeIn(panels[1]))
            vo.wait_until("c")
            self.play(FadeIn(dots[2]), FadeIn(panels[2]))
            vo.wait_until("d")
            self.play(FadeOut(panels), FadeOut(pl), FadeIn(nobel, shift=DOWN * 0.2))
        self.wait(0.3)
        self.clear_scene()
