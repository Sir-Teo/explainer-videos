from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai9.common import MONO, NEURON, PART, load
from videos.ai.ai9.plotting import checkpoint_prefix
from videos.ai.ai9.scoring import passage_groups, score_range

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
            dict(key="ascii", label="plain text file", bits=8 * raw["n_bytes"] / raw["n_chars"], part=1, kind="baseline"),
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
        tag = note(r"schematic: \ a few of the units and wires").to_corner(UL, buff=0.25).shift(DOWN * 0.35)
        hc = history_card(2003, r"Yoshua Bengio, R\'ejean Ducharme, Pascal Vincent \& Christian Jauvin",
                          r"\textit{A Neural Probabilistic Language Model}: \ an influential neural language model, \ for words",
                          width=6.4, color=C.HUMAN).move_to([2.6, 1.4, 0])
        with self.voiceover(
            "Now let's use a network for the task that runs through this whole series: guess the next character. In "
            "2003 Yoshua Bengio, Rejean Ducharme, Pascal Vincent and Christian Jauvin published an influential neural language "
            f"model, for words. Here is its design, for characters. Take the last {n} characters. "
            f"<bookmark mark='a'/> Each character becomes a vector of {e} numbers, looked up in a table that is "
            "itself learned. <bookmark mark='b'/> The vectors go through one hidden layer of tanh units. "
            "<bookmark mark='c'/> And out comes a score for every possible next character, turned into "
            "probabilities by Part 1's softmax. Every number in it is learned together, by backpropagation."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.15), FadeIn(cite_))
            self.wait(4.0)
            self.play(FadeIn(boxes), FadeIn(chars), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeOut(hc))
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
        nn = float(d["passage_bits"])
        low, top = score_range(cv[:, 2])
        ax = Axes(x_range=[0, cv[-1, 0], 4000], y_range=[low, top, 0.5], x_length=6.6, y_length=3.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-2.6, 0.6, 0])
        yl = VGroup(*[MathTex(f"{v:.0f}", font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in np.arange(np.ceil(low), top + 0.01, 1)])
        xl = label(rf"training steps \ (${int(d['batch']):,}$ positions each)".replace(",", "{,}"), font_size=22,
                   color=GREY_A).next_to(ax, DOWN, buff=0.2)
        yn = label(r"passage targets $24$--$21405$: \\ $21{,}382$ characters; bits per character",
                   font_size=20, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        t = ValueTracker(float(cv[0, 0]))

        def upto():
            prefix = checkpoint_prefix(cv[:, 0], cv[:, 2], t.get_value())
            pts = [ax.c2p(x, y) for x, y in prefix]
            return VMobject(color=C.NEURAL, stroke_width=4).set_points_as_corners(pts)

        def bits_now():
            return float(np.interp(t.get_value(), cv[:, 0], cv[:, 2]))

        live = always_redraw(upto)
        rider = always_redraw(lambda: glow_dot(ax.c2p(t.get_value(), bits_now()), color=C.NEURAL, radius=0.08))
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
            txt = " ".join(s.split())[:112]
            cut = txt.rfind(" ", 0, 56)
            cut = cut if cut > 30 else 56
            l1 = VGroup(data_text(prompt.strip(), font="DejaVu Serif", font_size=24, color=GREY_B),
                        data_text(txt[:cut], font="DejaVu Serif", font_size=24, color=WHITE))
            l1.arrange(RIGHT, buff=0.14, aligned_edge=DOWN)
            m = VGroup(l1, data_text(txt[cut:].strip() or " ", font="DejaVu Serif", font_size=24, color=WHITE))
            m.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
            if m.width > 12.4:
                m.scale_to_fit_width(12.4)
            return m.move_to(panel_.get_center() + DOWN * 0.15)

        end = (f"By the end it reaches {nn:.2f} bits per character on 21,382 passage targets: positions 24 "
               "through 21,405, counted from zero. This passage was monitored during training.")
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
            self.play(Create(ax), FadeIn(yl), FadeIn(xl), FadeIn(yn), FadeIn(panel_), FadeIn(pl),
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
        nn, mix, lam = float(d["passage_bits"]), float(d["mix_bits"]), float(d["lam"])
        lc = np.asarray(d["lam_curve"])
        lams = np.linspace(0, 1, len(lc))
        g = axes([0, 1], [float(np.floor(lc.min() * 10) / 10), float(np.ceil(lc.max() * 10) / 10)], x_length=5.6,
                 y_length=3.4, xlabel=r"$\lambda$: \ the network's share", ylabel=r"validation bits/character \\ first $200{,}000$ characters \\ targets $24$--$199999$: $199{,}976$ characters",
                 xticks=[0, 0.5, 1], yticks=[], center=[-3.0, -0.6, 0], font_size=18)
        cl = curve(g.ax, lams, lc, C.NEURAL, 3.5)
        best = glow_dot(g.ax.c2p(lam, lc.min()), color=C.BITS, radius=0.08)
        colors = {r"\lambda": C.NEURAL, r"q_{\text{net}}": C.NEURAL, r"q_{\text{KN}}": C.COUNTING}
        mf = cmath(r"q", "=", r"\lambda", r"\,", r"q_{\text{net}}", "+", r"(1 - \lambda)", r"\,", r"q_{\text{KN}}",
                   colors=colors, font_size=34).move_to([3.4, 2.2, 0])
        ml = label(rf"$\lambda = {lam:.2f}$, \ chosen on held-out text, \ never on the passage", font_size=22,
                   color=GREY_A).next_to(mf, DOWN, buff=0.2)
        scope = label(r"passage targets $24$--$21405$ \\ $21{,}382$ characters; bits per character",
                      font_size=20, color=GREY_A).move_to([3.4, 0.3, 0])
        res = VGroup(label(rf"the network alone: \ ${nn:.2f}$", font_size=26, color=C.NEURAL),
                     label(rf"together: \ ${mix:.2f}$", font_size=30, color=WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        res.move_to([3.4, -0.9, 0])
        wins = float(d["nn_wins"])
        comparison = "lower than the network alone" if mix < nn else "not lower than the network alone"
        said = (f"On the same 21,382 passage targets, the mixture reaches {mix:.2f} bits per character, "
                f"{comparison}. For {100 * wins:.0f} percent of these targets, the network assigns more probability "
                "to the observed next character than Kneser–Ney does. This is not prediction accuracy, and the "
                "aligned Kneser–Ney-only score was not saved.")
        with self.voiceover(
            "Bengio's team found that their best results came from combining the network with a counting model: "
            "averaging the two predictions. <bookmark mark='a'/> Here the weight is chosen on the first two hundred "
            "thousand validation characters, scoring positions 24 through 199,999, counted from zero. It is not "
            "chosen on the passage. <bookmark mark='b'/> " + said
        ) as vo:
            self.play(Write(mf), FadeIn(g), Create(cl))
            vo.wait_until("a")
            self.play(FadeIn(ml), FadeIn(best))
            vo.wait_until("b")
            self.play(FadeIn(scope), LaggedStart(*[FadeIn(r_) for r_ in res], lag_ratio=0.3), run_time=1.5)
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
            return ("lower" if ch.isalpha() and ch.islower() else "capital" if ch.isalpha() else
                    "digit" if ch.isdigit() else "punct")

        cols = dict(lower=C.TRUE_P, capital=C.MODEL_Q, digit=C.INTERVAL, punct=GREY_B)
        pts = VGroup()
        for (x, y), ch in zip(xy, chars):
            pts.add(data_text("␣" if ch == " " else ch, font=MONO, font_size=24, color=cols[kind(ch)]).move_to([x, y - 0.1, 0]))
        halos = VGroup()
        for group, col in (({"lower"}, C.TRUE_P), ({"capital"}, C.MODEL_Q), ({"digit"}, C.INTERVAL), ({"punct"}, GREY_B)):
            Q = np.array([[x, y - 0.1] for (x, y), ch in zip(xy, chars) if kind(ch) in group])
            if len(Q) < 2:
                continue
            c, sd = Q.mean(0), Q.std(0)
            halos.add(Ellipse(width=max(4.4 * sd[0], 0.9), height=max(4.4 * sd[1], 0.9), stroke_color=col, stroke_width=1.5,
                              stroke_opacity=0.5, fill_color=col, fill_opacity=0.07).move_to([c[0], c[1], 0]))
        head = label(r"The output layer's character vectors, \ seen along their two main directions", font_size=30).to_edge(UP, buff=0.35)
        nudge = note(r"positions nudged apart a little, \ so every character can be read").next_to(head, DOWN, buff=0.1)
        key = VGroup(label(r"lowercase letters", font_size=24, color=C.TRUE_P),
                     label(r"capitals", font_size=24, color=C.MODEL_Q), label(r"digits", font_size=24, color=C.INTERVAL),
                     label(r"punctuation", font_size=24, color=GREY_B)).arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "And the vectors the network scores each next character with, which nobody designed, have organized "
            "themselves. Seen along their two main directions, from Part 7, <bookmark mark='a'/> characters that "
            "behave alike sit together: lowercase letters with lowercase letters, capitals with capitals, digits with "
            "digits, and punctuation in its own corner. It's Part 3's word vectors again, learned this time as a side "
            "effect of predicting."
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
        from videos.ai.ai7 import compute as c7

        # Read the original Part 7 aggregate; never manufacture an aligned KN score.
        infini = c7.load("infini")
        (_, neural_rows), (_, historical_rows) = passage_groups(d, k, infini)
        max_bits = max(4.0, score_range([r["bits"] for r in neural_rows + historical_rows], step=2)[1])
        neural = scoreboard(neural_rows, highlight=(0, 1), max_bits=max_bits, bar_width=5.8,
                            label_width=4.4, row_h=0.5, font_size=22).move_to([0, 0.83, 0])
        history = scoreboard(historical_rows, max_bits=max_bits, bar_width=5.8,
                             label_width=4.4, row_h=0.5, font_size=22).move_to([0, -2.12, 0])
        head = label(r"Scores on two target ranges", font_size=36).move_to([0, 3.35, 0])
        neural_title = label(r"Part 9: \ neural model and mixture", font_size=25, color=C.NEURAL).move_to([0, 2.6, 0])
        neural_scope = label(r"targets $24$--$21405$ (inclusive): $21{,}382$ characters",
                             font_size=21, color=GREY_A).move_to([0, 2.13, 0])
        history_title = label(r"Part 7: \ paired historical results", font_size=25, color=C.COUNTING).move_to([0, -0.4, 0])
        history_scope = label(r"targets $7$--$21405$ (inclusive): $21{,}399$ characters",
                              font_size=21, color=GREY_A).move_to([0, -0.87, 0])
        scope_note = label(r"Zero-based target indices. \ Different ranges: no cross-group ranking.",
                           font_size=20, color=GREY_B).move_to([0, -3.36, 0])
        board = VGroup(head, neural_title, neural_scope, neural, history_title, history_scope, history)
        glow = SurroundingRectangle(neural.rows, color=C.NEURAL, buff=0.08, corner_radius=0.08)
        samples = d["samples"]

        def sample_block(prompt_, cont):
            words_ = " ".join(cont.split())[:110].split(" ")[:-1]  # whole words only
            lines, cur = [], ""
            for w_ in words_:
                if len(cur) + len(w_) + 1 > 56 and cur:
                    lines.append(cur)
                    cur = w_
                else:
                    cur = (cur + " " + w_).strip()
            lines.append(cur + " …")
            g_ = VGroup(data_text(prompt_.strip(), font="DejaVu Serif", font_size=24, color=GREY_B),
                        *[data_text(t_, font="DejaVu Serif", font_size=24, color=WHITE) for t_ in lines[:2]])
            return g_.arrange(DOWN, aligned_edge=LEFT, buff=0.1)

        txt = VGroup(*[sample_block(p_, c_) for p_, c_ in samples]).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        txt.scale_to_fit_height(min(txt.height, 6.4)).move_to(ORIGIN)
        if txt.width > 12.8:
            txt.scale_to_fit_width(12.8)
        with self.voiceover(
            "Here are two separate result groups. Our network and its mixture score the same 21,382 targets. "
            "The historical Kneser–Ney and infinity-gram mixture score 21,399 targets. "
            "<bookmark mark='a'/> The starting positions differ, so these groups do not establish a ranking "
            "against each other. The network sees only twenty-four characters, with one hidden layer."
        ) as vo:
            self.play(FadeIn(board))
            self.play(Create(glow))
            vo.wait_until("a")
            self.play(FadeIn(scope_note), Indicate(neural_scope), Indicate(history_scope))
        self.play(FadeOut(board), FadeOut(glow), FadeOut(scope_note))
        with self.voiceover(
            "Here's what it writes, from Part 5's prompt and three others: <bookmark mark='a'/> English-shaped, word-shaped, and not yet making sense."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(b_[0]) for b_ in txt], lag_ratio=0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[AddTextLetterByLetter(VGroup(*b_[1:])) for b_ in txt], lag_ratio=0.5), run_time=4.0)
        self.wait(0.6)
        self.clear_scene()
