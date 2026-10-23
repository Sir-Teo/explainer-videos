from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai9.common import MONO, NEURON, PART, load

EMB = C.CONTEXT


def load_kn():
    from videos.ai.ai7 import compute as c7  # Part 7's Kneser-Ney, from its own cache

    return c7.load("kn")


def board_rows():
    """The scoreboard so far: Part 1's rows (its cache), or, where Part 1's language-model rows haven't been computed,
    the rows its counting models and compressors give."""
    from videos.ai.ai1 import compute as c1

    try:
        return [dict(r) for r in c1.load("scoreboard")["rows"]], True
    except FileNotFoundError:
        raw = c1.load("raw")
        rows = [
            dict(key="ascii", label="plain text file", bits=8.0, part=1, kind="baseline"),
            dict(key="uniform", label=f"uniform over its {raw['passage_symbols']} symbols", bits=raw["uniform"], part=1,
                 kind="count"),
            dict(key="order0", label="letter frequencies", bits=raw["rows"][0]["test"], part=1, kind="count"),
            dict(key="order1", label="the previous character", bits=raw["rows"][1]["test"], part=1, kind="count"),
            dict(key="gzip", label="gzip", bits=raw["compressors"]["gzip"], part=1, kind="compressor"),
            dict(key="xz", label="xz", bits=raw["compressors"]["xz"], part=1, kind="compressor"),
            dict(key="bzip2", label="bzip2", bits=raw["compressors"]["bzip2"], part=1, kind="compressor"),
            dict(key="best", label=f"the previous {raw['best']} characters", bits=raw["best_bits"], part=1, kind="count"),
            dict(key="human", label="people (Shannon 1951, letters only)", lo=0.6, hi=1.3, part=1, kind="human"),
        ]
        return rows, False


class NeuralLM(VoiceoverScene):
    def construct(self):
        self.card()
        self.architecture()
        self.training()
        self.mixing()
        self.vectors()
        self.board()

    def card(self):
        card = chapter_card(15, r"A neural language model", r"What if the counts were learned instead?", part=PART,
                            lit=(2003,))
        with self.voiceover("Chapter fifteen. A neural language model."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def architecture(self):
        d = load("lm")
        n, e, hdim, K = int(d["n_ctx"]), int(d["emb"]), int(d["hid"]), int(d["K"])
        ctx = "sat down in the armchair"
        assert len(ctx) == n
        chars = VGroup(*[data_text("␣" if c == " " else c, font=MONO, font_size=18) for c in ctx])
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
        tag = note(r"schematic: \ a few of the units and wires").to_corner(UL, buff=0.25)
        with self.voiceover(
            "Now let's use a network for the task that runs through this whole series: guess the next character. In "
            "2003 Yoshua Bengio, Rejean Ducharme, Pascal Vincent and Christian Jauvin built the first neural language "
            f"model, for words. Here is its design, for characters. Take the last {n} characters. "
            f"<bookmark mark='a'/> Each character becomes a vector of {e} numbers, looked up in a table that is "
            "itself learned. <bookmark mark='b'/> The vectors go through one hidden layer of tanh units. "
            "<bookmark mark='c'/> And out comes a score for every possible next character, turned into "
            "probabilities by Part 1's softmax. Every number in it is learned together, by backpropagation."
        ) as vo:
            self.play(FadeIn(boxes), FadeIn(chars), FadeIn(cite_), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[TransformFromCopy(chars[i], vecs[i]) for i in range(n)], lag_ratio=0.05),
                      FadeIn(notes[0]), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(lines1), FadeIn(hid), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Create(lines2), LaggedStart(*[GrowFromEdge(o, DOWN) for o in outs], lag_ratio=0.05), FadeIn(ol),
                      FadeIn(notes[2]))
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def training(self):
        d = load("lm")
        cv = np.asarray(d["curve"])
        snaps = d["snaps"]
        kn, nn = float(d["kn"]), float(d["passage_bits"])
        top = float(np.ceil(max(cv[:, 2].max(), 4.5)))
        top = min(top, 8.0)
        ax = Axes(x_range=[0, cv[-1, 0], 4000], y_range=[1.6, top, 0.5], x_length=6.6, y_length=3.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-2.6, 0.6, 0])
        yl = VGroup(*[MathTex(f"{v:.0f}", font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in np.arange(2, top + 0.01, 1)])
        xl = label(rf"training steps \ (${int(d['batch']):,}$ positions each)".replace(",", "{,}"), font_size=22,
                   color=GREY_A).next_to(ax, DOWN, buff=0.2)
        yn = label(r"bits per character on the passage", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        knl = DashedLine(ax.c2p(0, kn), ax.c2p(cv[-1, 0], kn), color=C.COUNTING, stroke_width=2.5)
        knt = label(rf"Part 7's Kneser--Ney: \ ${kn:.2f}$", font_size=22, color=C.COUNTING).next_to(knl, DOWN, buff=0.1)
        knt.align_to(knl, RIGHT)
        t = ValueTracker(float(cv[0, 0]))

        def clip(y):
            return float(np.clip(y, 1.6, top))

        def upto():
            n_ = max(2, int(np.searchsorted(cv[:, 0], t.get_value(), side="right")))
            pts = [ax.c2p(x, clip(y)) for x, y in cv[:n_, [0, 2]]]
            if n_ < len(cv):
                x = t.get_value()
                pts.append(ax.c2p(x, clip(np.interp(x, cv[:, 0], cv[:, 2]))))
            return VMobject(color=C.NEURAL, stroke_width=4).set_points_as_corners(pts)

        def bits_now():
            return float(np.interp(t.get_value(), cv[:, 0], cv[:, 2]))

        live = always_redraw(upto)
        rider = always_redraw(lambda: glow_dot(ax.c2p(t.get_value(), clip(bits_now())), color=C.NEURAL, radius=0.08))
        clock = always_redraw(lambda: VGroup(
            MathTex(rf"\text{{step }}{int(round(t.get_value())):,}".replace(",", "{,}"), font_size=28, color=WHITE),
            MathTex(rf"{bits_now():.2f}\ \text{{bits/char}}", font_size=28, color=C.NEURAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            .move_to([4.6, 1.4, 0]))
        prompt = d["prompt"]
        panel_ = RoundedRectangle(width=13.0, height=1.75, corner_radius=0.12, stroke_color=GREY_D, stroke_width=1.5,
                                  fill_color="#121722", fill_opacity=1).move_to([0, -2.85, 0])
        pl = label(r"what it writes now, \ from the same prompt and the same random draws:", font_size=20,
                   color=GREY_A).next_to(panel_.get_corner(UL), DR, buff=0.12)

        def sample_text(s):
            txt = " ".join(s.split())[:118]
            m = VGroup(data_text(prompt.strip(), font="DejaVu Serif", font_size=19, color=GREY_B),
                       data_text(txt, font="DejaVu Serif", font_size=19, color=WHITE))
            m.arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
            if m.width > 12.4:
                m.scale_to_fit_width(12.4)
            return m.move_to(panel_.get_center() + DOWN * 0.18)

        beat = nn < kn
        end = (f"By the end it reaches {nn:.2f} bits per character, past Kneser–Ney's {kn:.2f}."
               if beat else
               f"By the end it reaches {nn:.2f} bits per character: far better than Part 1's "
               f"counting, but not quite Kneser–Ney's {kn:.2f}. With this much computing, the best counting is a hard "
               "opponent.")
        wr = load("lm_words")["rows"]  # step, bits, words, real words, share
        s1 = int(wr[3][0])
        early = (f"At first it types random symbols: {100 * wr[0][4]:.0f} percent of the words it writes are real words. "
                 f"<bookmark mark='b'/> By step {s1:,}, {100 * wr[3][4]:.0f} percent are; by the end, "
                 f"{100 * wr[-1][4]:.0f} percent, in the rhythm of English sentences, if not yet their sense. ")
        cur = sample_text(snaps[0][2])
        with self.voiceover(
            "Train it on Part 1's thirty novels, by gradient descent, with Part 1's cross-entropy as the loss. Below "
            "the curve, what it writes at each moment of training, always from the same prompt and the same random "
            "draws. <bookmark mark='a'/> " + early + "<bookmark mark='c'/> " + end
        ) as vo:
            self.play(Create(ax), FadeIn(yl), FadeIn(xl), FadeIn(yn), Create(knl), FadeIn(knt), FadeIn(panel_), FadeIn(pl),
                      FadeIn(cur))
            self.add(live, rider, clock)
            marks = {1: "a", 3: "b", len(snaps) - 1: "c"}
            for i in range(1, len(snaps)):
                if i in marks and marks[i] != "c":
                    vo.wait_until(marks[i])
                step_i = int(snaps[i][0])
                self.play(t.animate.set_value(step_i), run_time=0.6 + 1.6 * (step_i - int(snaps[i - 1][0])) / cv[-1, 0])
                nxt = sample_text(snaps[i][2])
                self.play(FadeOut(cur), FadeIn(nxt), run_time=0.5)
                cur = nxt
                if i < len(snaps) - 1:
                    self.wait(0.6)
            for m_ in (live, rider, clock):
                m_.clear_updaters()
            self.remove(rider)
            vo.wait_until("c")
            fin = label(rf"the network: \ ${nn:.2f}$", font_size=30, color=C.NEURAL).move_to([4.6, 1.4, 0])
            self.play(FadeOut(clock), FadeIn(fin))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mixing(self):
        d = load("lm")
        kn, nn, mix, lam = float(d["kn"]), float(d["passage_bits"]), float(d["mix_bits"]), float(d["lam"])
        lc = np.asarray(d["lam_curve"])
        lams = np.linspace(0, 1, len(lc))
        g = axes([0, 1], [float(np.floor(lc.min() * 10) / 10), float(np.ceil(lc.max() * 10) / 10)], x_length=5.6,
                 y_length=3.4, xlabel=r"$\lambda$: \ the network's share", ylabel=r"bits per character, \ held-out text",
                 xticks=[0, 0.5, 1], yticks=[], center=[-3.0, -0.6, 0], font_size=18)
        cl = curve(g.ax, lams, lc, C.NEURAL, 3.5)
        best = glow_dot(g.ax.c2p(lam, lc.min()), color=C.BITS, radius=0.08)
        colors = {r"\lambda": C.NEURAL, r"q_{\text{net}}": C.NEURAL, r"q_{\text{KN}}": C.COUNTING}
        mf = cmath(r"q", "=", r"\lambda", r"\,", r"q_{\text{net}}", "+", r"(1 - \lambda)", r"\,", r"q_{\text{KN}}",
                   colors=colors, font_size=34).move_to([3.4, 2.2, 0])
        ml = label(rf"$\lambda = {lam:.2f}$, \ chosen on held-out text, \ never on the passage", font_size=22,
                   color=GREY_A).next_to(mf, DOWN, buff=0.2)
        res = VGroup(label(rf"Kneser--Ney alone: \ ${kn:.2f}$", font_size=26, color=C.COUNTING),
                     label(rf"the network alone: \ ${nn:.2f}$", font_size=26, color=C.NEURAL),
                     label(rf"together: \ ${mix:.2f}$", font_size=30, color=WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        res.move_to([3.4, -0.9, 0])
        wins = float(d["nn_wins"])
        better = mix < min(kn, nn)
        said = (f"Together, they reach {mix:.2f} bits: better than either alone, because they make different mistakes. "
                f"On the passage, the network is the more confident of the two on {100 * wins:.0f} percent of the "
                "characters." if better else
                f"Together, they reach {mix:.2f} bits, no better than the best of the two alone.")
        with self.voiceover(
            "Bengio's team found that their best results came from combining the network with a counting model: "
            "averaging the two predictions. <bookmark mark='a'/> The weight is chosen on held-out text, never on the "
            "passage. <bookmark mark='b'/> " + said
        ) as vo:
            self.play(Write(mf), FadeIn(g), Create(cl))
            vo.wait_until("a")
            self.play(FadeIn(ml), FadeIn(best))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in res], lag_ratio=0.3), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def vectors(self):
        d = load("lm")
        xy = np.asarray(d["xy"])
        chars = d["xy_chars"]
        xy = (xy - (xy.max(0) + xy.min(0)) / 2) / np.ptp(xy, 0) * np.array([11.0, 4.6])
        P = xy.copy()
        for _ in range(300):  # nudge overlapping characters apart, so each one can be read
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
            pts.add(data_text("␣" if ch == " " else ch, font=MONO, font_size=24, color=col).move_to([x, y - 0.1, 0]))
        halos = VGroup()
        for group, col in (({"vowel", "consonant"}, C.TRUE_P), ({"capital"}, C.MODEL_Q), ({"digit"}, C.INTERVAL), ({"punct"}, GREY_B)):
            Q = np.array([[x, y - 0.1] for (x, y), ch in zip(xy, chars) if kind(ch) in group])
            if len(Q) < 2:
                continue
            c, sd = Q.mean(0), Q.std(0)
            halos.add(Ellipse(width=max(4.4 * sd[0], 0.9), height=max(4.4 * sd[1], 0.9), stroke_color=col, stroke_width=1.5,
                              stroke_opacity=0.5, fill_color=col, fill_opacity=0.07).move_to([c[0], c[1], 0]))
        head = label(r"The output layer's character vectors, \ seen along their two main directions", font_size=30).to_edge(UP, buff=0.35)
        nudge = note(r"positions nudged apart a little, \ so every character can be read").next_to(head, DOWN, buff=0.1)
        key = VGroup(label(r"vowels", font_size=24, color=C.BITS), label(r"consonants", font_size=24, color=C.TRUE_P),
                     label(r"capitals", font_size=24, color=C.MODEL_Q), label(r"digits", font_size=24, color=C.INTERVAL),
                     label(r"punctuation", font_size=24, color=GREY_B)).arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "And the vectors the network scores each next character with, which nobody designed, have organized "
            "themselves. Seen along their two main directions, from Part 7, <bookmark mark='a'/> characters that "
            "behave alike sit together: vowels near vowels, capitals near capitals, digits and punctuation in their "
            "own corners. It's Part 3's word vectors again, learned this time as a side effect of predicting."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in pts], lag_ratio=0.02), FadeIn(nudge), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(key), LaggedStart(*[DrawBorderThenFill(h_) for h_ in halos], lag_ratio=0.3), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def board(self):
        d = load("lm")
        k = load_kn()
        rows, full = board_rows()
        i = next(j for j, r in enumerate(rows) if r["key"] == "best") + 1
        rows.insert(i, dict(key="kn", label=rf"Kneser--Ney, \ ${k['best']}$ characters", bits=k["best_bits"], part=7,
                            kind="count"))
        rows.insert(i + 1, dict(key="nlm", label=rf"a neural model, \ ${d['n_ctx']}$ characters", bits=d["passage_bits"],
                                part=9, kind="lm"))
        rows.insert(i + 2, dict(key="mix", label=r"the neural model $+$ Kneser--Ney", bits=d["mix_bits"], part=9, kind="lm"))
        board = scoreboard(rows, highlight=(i + 1, i + 2), max_bits=8.0)
        board.scale_to_fit_height(min(board.height, 6.6)).move_to(DOWN * 0.1)
        glow = SurroundingRectangle(VGroup(board.rows[i + 1], board.rows[i + 2]), color=C.NEURAL, buff=0.08, corner_radius=0.08)
        gpt = [j for j, r in enumerate(rows) if "GPT-2" in r["label"]]
        samples = d["samples"]
        txt = VGroup(data_text(samples[0][0], font="DejaVu Serif", font_size=20, color=GREY_B),
                     data_text(" ".join(samples[0][1].split())[:90] + " …", font="DejaVu Serif", font_size=20, color=WHITE))
        txt.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(ORIGIN)
        if txt.width > 12.8:
            txt.scale_to_fit_width(12.8)
        best_counting = min(float(k["best_bits"]), *[float(r["bits"]) for r in rows[:i] if "bits" in r])
        behind = float(d["mix_bits"]) - best_counting
        if behind > 0:
            top_row = f"{behind:.2f} bits behind the best row above them"
        elif gpt:
            top_row = "the best of everything before GPT-2"
        else:
            top_row = "the best of everything on the board so far"
        gap = (f"<bookmark mark='a'/> But it's still far behind GPT-2. It sees only {d['n_ctx']} characters, and one "
               "hidden layer has to do everything. The rest of the series is about closing that gap." if gpt else
               f"<bookmark mark='a'/> It sees only {d['n_ctx']} characters, and one hidden layer has to do everything. "
               "The large models of Part 1, still to be filled in on this board, show how far there is to go.")
        with self.voiceover(
            "On the scoreboard, two new rows: the first network, and the network with counting, "
            + top_row + ". " + gap
        ) as vo:
            self.play(FadeIn(board))
            self.play(Create(glow))
            vo.wait_until("a")
            if gpt:  # the gap the rest of the series closes
                self.play(Transform(glow, SurroundingRectangle(VGroup(*[board.rows[j] for j in gpt]), color=GREY_A, buff=0.08,
                                                               corner_radius=0.08)))
        self.play(FadeOut(board), FadeOut(glow))
        with self.voiceover(
            "Here's what it writes, from the opening of Part 5's prompt: <bookmark mark='a'/> English-shaped, "
            "word-shaped, and not yet making sense."
        ) as vo:
            self.play(FadeIn(txt[0]))
            vo.wait_until("a")
            self.play(AddTextLetterByLetter(txt[1]), run_time=3.0)
        self.wait(0.6)
        self.clear_scene()
