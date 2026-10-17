from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai8.common import MONO, NEURON, curve, load

EMB = C.CONTEXT


class NeuralLM(VoiceoverScene):
    def construct(self):
        self.card()
        self.architecture()
        self.training()
        self.vectors()
        self.board()

    def card(self):
        card = chapter_card(5, r"A neural language model", r"What if the counts were learned instead?", part=8, lit=(2003,))
        with self.voiceover("Chapter five. A neural language model."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def architecture(self):
        d = load("lm")
        n, e, hdim, K = int(d["n_ctx"]), int(d["emb"]), int(d["hid"]), int(d["K"])
        ctx = "sat down in the armchair"
        assert len(ctx) == n
        chars = VGroup(*[Text("␣" if c == " " else c, font=MONO, font_size=18) for c in ctx])
        boxes = VGroup(*[Square(0.3, stroke_color=GREY_C, stroke_width=1.5).move_to([-6.1 + 0.34 * i, -2.6, 0]) for i in range(n)])
        for c_, b in zip(chars, boxes):
            c_.move_to(b)
        vecs = VGroup(*[VGroup(*[Rectangle(width=0.24, height=0.09, stroke_width=0,
                                          fill_color=EMB, fill_opacity=float(0.25 + 0.7 * abs(np.sin(1.7 * i + 0.9 * j))))
                                 for j in range(10)]).arrange(DOWN, buff=0.015).next_to(boxes[i], UP, buff=0.25)
                        for i in range(n)])
        hid = VGroup(*[Circle(radius=0.11, color=NEURON, stroke_width=2) for _ in range(18)]).arrange(RIGHT, buff=0.12)
        hid.move_to([-2.2, 0.9, 0])
        outs = VGroup(*[Rectangle(width=0.18, height=float(0.08 + 1.2 * v), stroke_width=0, fill_color=C.MODEL_Q,
                                  fill_opacity=0.85) for v in (0.02, 0.05, 0.9, 0.04, 0.1, 0.02, 0.03, 0.01, 0.05, 0.02)])
        outs.arrange(RIGHT, buff=0.06, aligned_edge=DOWN).move_to([-2.2, 2.6, 0])
        ol = label(r"the next character: \ $" + str(K) + r"$ probabilities", font_size=22, color=C.MODEL_Q).next_to(outs, RIGHT, buff=0.3)
        lines1 = VGroup(*[Line(vecs[i].get_top(), hid[j].get_bottom(), stroke_width=0.6, color=GREY_D)
                          for i in range(0, n, 3) for j in range(0, 18, 4)])
        lines2 = VGroup(*[Line(hid[j].get_top(), outs[k].get_bottom(), stroke_width=0.6, color=GREY_D)
                          for j in range(0, 18, 3) for k in range(0, 10, 2)])
        notes = VGroup(label(rf"each character: \ a learned vector of ${e}$ numbers", font_size=24, color=EMB),
                       label(rf"one hidden layer of ${hdim:,}$ tanh units".replace(",", "{,}"), font_size=24, color=NEURON),
                       label(r"softmax: \ Part 1's scores into probabilities", font_size=24, color=C.MODEL_Q),
                       label(rf"${d['n_params']:,}$ numbers to learn".replace(",", "{,}"), font_size=26, color=WHITE))
        notes.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.5, 0.2, 0])
        keep_in_frame(notes)
        cite_ = cite(r"Y.~Bengio, R.~Ducharme, P.~Vincent \& C.~Jauvin, \textit{A Neural Probabilistic Language Model} (2003)",
                     corner=DR)
        tax = Axes(x_range=[-3, 3, 1], y_range=[-1.2, 3, 1], x_length=2.6, y_length=1.3, tips=False,
                   axis_config={"stroke_color": GREY_C, "include_ticks": False})
        tpic = VGroup(tax, tax.plot(lambda x: max(x, 0.0), x_range=[-3, 3, 0.02], color=GREY_B, stroke_width=2.5),
                      tax.plot(np.tanh, x_range=[-3, 3, 0.02], color=NEURON, stroke_width=3.5),
                      *[DashedLine(tax.c2p(-3, v), tax.c2p(3, v), color=GREY_D, stroke_width=1, dash_length=0.05)
                        for v in (1, -1)])
        tpic.add(label(r"tanh", font_size=20, color=NEURON).next_to(tax.c2p(3, 1), RIGHT, buff=0.1),
                 label(r"ReLU", font_size=20, color=GREY_B).next_to(tax.c2p(3, 3), RIGHT, buff=0.1))
        tcard = gloss(r"a hidden layer of tanh units", r"hidden: \ in the middle, \ neither input nor output \\ "
                      r"tanh: \ a smooth S-shaped bend into $-1$ to $1$", tpic, corner=DR, color=NEURON)
        tcard.shift(UP * 0.45)
        with self.voiceover(
            f"Now let's use a network for the task that runs through this whole series: guess the next character. "
            f"Take the last {n} characters. <bookmark mark='a'/> Each character becomes a vector of {e} numbers, "
            "looked up in a table that is itself learned. <bookmark mark='b'/> The vectors go through one hidden "
            "layer. Hidden just means in the middle, neither input nor output. Its units are tanh units: tanh is a "
            "smooth S-shaped bend that squashes any number into the range from minus one to one. "
            "<bookmark mark='c'/> And out comes a score for every possible next character, turned into "
            "probabilities by part one's softmax. That's the design of Yoshua Bengio's neural language model, from "
            "2003, here for characters instead of words."
        ) as vo:
            self.play(FadeIn(boxes), FadeIn(chars), FadeIn(cite_))
            vo.wait_until("a")
            self.play(LaggedStart(*[TransformFromCopy(chars[i], vecs[i]) for i in range(n)], lag_ratio=0.05),
                      FadeIn(notes[0]), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(lines1), FadeIn(hid), FadeIn(notes[1]))
            self.play(FadeIn(tcard, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeOut(tcard))
            self.play(Create(lines2), LaggedStart(*[GrowFromEdge(o, DOWN) for o in outs], lag_ratio=0.05), FadeIn(ol),
                      FadeIn(notes[2]))
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def training(self):
        d = load("lm")
        cv = np.asarray(d["curve"])
        kn, nn, mix, lam = float(d["kn"]), float(d["passage_bits"]), float(d["mix_bits"]), float(d["lam"])
        ax = Axes(x_range=[0, cv[-1, 0], 20000], y_range=[1.6, 4.6, 0.5], x_length=8.6, y_length=4.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.2, -0.5, 0])
        yl = VGroup(*[MathTex(f"{v:.1f}", font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1) for v in (2.0, 3.0, 4.0)])
        xl = label(r"training steps \ ($1{,}024$ positions each)", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        yn = label(r"bits per character on the passage", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        c = curve(ax, cv[:, 0], np.clip(cv[:, 2], 1.6, 4.6), C.NEURAL, 4)
        knl = DashedLine(ax.c2p(0, kn), ax.c2p(cv[-1, 0], kn), color=C.COUNTING, stroke_width=2.5)
        knt = label(rf"Part 6's Kneser--Ney: \ ${kn:.2f}$", font_size=24, color=C.COUNTING).next_to(knl, DOWN, buff=0.1)  # below the line: the curve ends above it
        knt.align_to(knl, RIGHT)
        fin = label(rf"the network: \ ${nn:.2f}$", font_size=30, color=C.NEURAL).move_to([4.6, 1.8, 0])
        colors = {r"\lambda": C.NEURAL, r"q_{\text{net}}": C.NEURAL, r"q_{\text{KN}}": C.COUNTING}
        mf = cmath(r"q", "=", r"\lambda", r"\,", r"q_{\text{net}}", "+", r"(1 - \lambda)", r"\,", r"q_{\text{KN}}",
                   colors=colors, font_size=32).next_to(fin, DOWN, buff=0.5)
        ml = label(rf"$\lambda = {lam:.2f}$, \ chosen on held-out text", font_size=22, color=GREY_A).next_to(mf, DOWN, buff=0.15)
        mres = label(rf"together: \ ${mix:.2f}$", font_size=30, color=WHITE).next_to(ml, DOWN, buff=0.35)
        beat = nn < kn
        # the curve drawn by a clock: a dot riding it, the step and the bits so far
        t = ValueTracker(float(cv[0, 0]))

        def upto():
            n_ = max(2, int(np.searchsorted(cv[:, 0], t.get_value(), side="right")))
            pts = [ax.c2p(x, float(np.clip(y, 1.6, 4.6))) for x, y in cv[:n_, [0, 2]]]
            if n_ < len(cv):  # the last stretch, interpolated up to the clock
                x = t.get_value()
                pts.append(ax.c2p(x, float(np.clip(np.interp(x, cv[:, 0], cv[:, 2]), 1.6, 4.6))))
            return VMobject(color=C.NEURAL, stroke_width=4).set_points_as_corners(pts)

        def bits_now():
            return float(np.interp(t.get_value(), cv[:, 0], cv[:, 2]))

        live = always_redraw(upto)
        rider = always_redraw(lambda: glow_dot(ax.c2p(t.get_value(), float(np.clip(bits_now(), 1.6, 4.6))), color=C.NEURAL,
                                               radius=0.08))
        clock = always_redraw(lambda: VGroup(
            MathTex(rf"\text{{step }}{int(round(t.get_value(), -2)):,}".replace(",", "{,}"), font_size=28, color=WHITE),
            MathTex(rf"{bits_now():.2f}\ \text{{bits/char}}", font_size=28, color=C.NEURAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            .move_to([4.6, 0.6, 0]))
        with self.voiceover(
            "Train it on part one's thirty novels, by gradient descent, with the cross-entropy of part one as the "
            "loss. <bookmark mark='a'/> The bits per character on the Maltese Falcon passage fall, and fall, "
            + (f"<bookmark mark='b'/> past Kneser–Ney's {kn:.2f}, to {nn:.2f}."
               if beat else
               f"<bookmark mark='b'/> to {nn:.2f}: far better than part one's counting, but not quite Kneser–Ney's "
               f"{kn:.2f}. On this much computing, the best counting is a hard opponent.")
        ) as vo:
            self.play(Create(ax), FadeIn(yl), FadeIn(xl), FadeIn(yn), Create(knl), FadeIn(knt))
            vo.wait_until("a")
            self.add(live, rider, clock)
            self.play(t.animate.set_value(float(cv[-1, 0])), run_time=5.0, rate_func=lambda a: smooth(a) ** 0.7)
            for m_ in (live, rider, clock):
                m_.clear_updaters()
            self.remove(rider)
            vo.wait_until("b")
            self.play(FadeOut(clock), FadeIn(fin))
        with self.voiceover(
            "Bengio's team found the same in 2003, and their best results came from combining the two: averaging "
            "the network's prediction with the counting model's. <bookmark mark='a'/> The weight is chosen on "
            f"held-out text, never on the passage. <bookmark mark='b'/> Together, they reach {mix:.2f} bits: better "
            "than either alone, because they make different mistakes."
        ) as vo:
            self.play(Write(mf))
            vo.wait_until("a")
            self.play(FadeIn(ml))
            vo.wait_until("b")
            self.play(FadeIn(mres))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def vectors(self):
        d = load("lm")
        xy = np.asarray(d["xy"])
        chars = d["xy_chars"]
        xy = (xy - (xy.max(0) + xy.min(0)) / 2) / np.ptp(xy, 0) * np.array([11.0, 4.6])
        # nudge overlapping characters apart (a few hundredths of the picture at most) so each one can be read
        P = xy.copy()
        for _ in range(300):
            D = P[:, None] - P[None]
            dist = np.linalg.norm(D, axis=-1) + np.eye(len(P))
            close = (dist < 0.36) & ~np.eye(len(P), dtype=bool)
            P += 0.25 * (D / dist[..., None] * ((0.36 - dist) * close)[..., None]).sum(1)
        xy = P

        def kind(ch):
            return ("vowel" if ch in "aeiouAEIOU" and ch.islower() else "consonant" if ch.isalpha() and ch.islower() else
                    "capital" if ch.isalpha() else "digit" if ch.isdigit() else "punct")

        cols = dict(vowel=C.BITS, consonant=C.TRUE_P, capital=C.MODEL_Q, digit=C.INTERVAL, punct=GREY_B)
        pts = VGroup()
        for (x, y), ch in zip(xy, chars):
            col = C.BITS if ch in "aeiouAEIOU" else cols[kind(ch)]
            pts.add(Text("␣" if ch == " " else ch, font=MONO, font_size=24, color=col).move_to([x, y - 0.1, 0]))
        # a soft halo round each group: lower case (vowels with consonants), capitals, digits, punctuation
        halos = VGroup()
        for group, col in (({"vowel", "consonant"}, C.TRUE_P), ({"capital"}, C.MODEL_Q), ({"digit"}, C.INTERVAL), ({"punct"}, GREY_B)):
            Q = np.array([[x, y - 0.1] for (x, y), ch in zip(xy, chars) if kind(ch) in group])
            if len(Q) < 2:
                continue
            c, sd = Q.mean(0), Q.std(0)
            halos.add(Ellipse(width=max(4.4 * sd[0], 0.9), height=max(4.4 * sd[1], 0.9), stroke_color=col, stroke_width=1.5,
                              stroke_opacity=0.5, fill_color=col, fill_opacity=0.07).move_to([c[0], c[1], 0]))
        nudge = note(r"positions nudged apart a little, \ so every character can be read").to_corner(DR, buff=0.25)
        head = label(r"The output layer's character vectors, \ seen along their two main directions", font_size=30).to_edge(UP, buff=0.35)
        nudge.next_to(head, DOWN, buff=0.1)
        key = VGroup(label(r"vowels", font_size=24, color=C.BITS), label(r"consonants", font_size=24, color=C.TRUE_P),
                     label(r"capitals", font_size=24, color=C.MODEL_Q), label(r"digits", font_size=24, color=C.INTERVAL),
                     label(r"punctuation", font_size=24, color=GREY_B)).arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "And the vectors the network scores each next character with, which nobody designed, have organized "
            "themselves. Seen along their two main directions, from part six, <bookmark mark='a'/> characters that "
            "behave alike sit together: vowels near vowels, capitals near capitals, digits and punctuation in their "
            "own corners. It's part two's word vectors again, learned this time as a side effect of predicting."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in pts], lag_ratio=0.02), FadeIn(nudge), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(key), LaggedStart(*[DrawBorderThenFill(h_) for h_ in halos], lag_ratio=0.3), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def board(self):
        from videos.ai.ai1 import compute as c1

        d = load("lm")
        k = load_kn()
        sb = c1.load("scoreboard")
        rows = [dict(r) for r in sb["rows"]]
        i = next(j for j, r in enumerate(rows) if r["key"] == "best") + 1
        rows.insert(i, dict(key="kn", label=rf"Kneser--Ney, \ ${k['best']}$ characters", bits=k["best_bits"], part=6,
                            kind="count"))
        rows.insert(i + 1, dict(key="nlm", label=rf"a neural model, \ ${d['n_ctx']}$ characters", bits=d["passage_bits"],
                                part=8, kind="lm"))
        rows.insert(i + 2, dict(key="mix", label=r"the neural model $+$ Kneser--Ney", bits=d["mix_bits"], part=8, kind="lm"))
        board = scoreboard(rows, highlight=(i + 1, i + 2), max_bits=8.0)
        board.scale_to_fit_height(min(board.height, 6.6)).move_to(DOWN * 0.1)
        glow = SurroundingRectangle(VGroup(board.rows[i + 1], board.rows[i + 2]), color=C.NEURAL, buff=0.08, corner_radius=0.08)
        gpt = [j for j, r in enumerate(rows) if "GPT-2" in r["label"]]
        samples = d["samples"]
        txt = VGroup(Text(samples[0][0], font="DejaVu Serif", font_size=20, color=GREY_B),
                     Text(" ".join(samples[0][1].split())[:90] + " …", font="DejaVu Serif", font_size=20, color=WHITE))
        txt.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(ORIGIN)
        if txt.width > 12.8:
            txt.scale_to_fit_width(12.8)
        with self.voiceover(
            "On the scoreboard, two new rows: the first network, and the network with counting, the best of "
            "everything before GPT-2. <bookmark mark='a'/> But it's still far behind GPT-2. It sees only "
            f"{d['n_ctx']} characters, and one hidden layer has to do everything. The rest of the series is about "
            "closing that gap."
        ) as vo:
            self.play(FadeIn(board))
            self.play(Create(glow))
            vo.wait_until("a")
            if gpt:  # the gap the rest of the series closes
                self.play(Transform(glow, SurroundingRectangle(VGroup(*[board.rows[j] for j in gpt]), color=GREY_A, buff=0.08,
                                                               corner_radius=0.08)))
        self.play(FadeOut(board), FadeOut(glow))
        with self.voiceover(
            "Here's what it writes, starting from part four's prompt: <bookmark mark='a'/> English-shaped, "
            "word-shaped, and not yet making sense."
        ) as vo:
            self.play(FadeIn(txt[0]))
            vo.wait_until("a")
            self.play(AddTextLetterByLetter(txt[1]), run_time=3.0)
        self.wait(0.6)
        self.clear_scene()


def load_kn():
    from videos.ai.ai6 import compute as c6

    return c6.load("kn")
