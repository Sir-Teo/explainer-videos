from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai23.common import BLANK_C, MONO, PART, SND_C, band, curve, heat, load, spread_rows

LETTER_C = C.TRUE_P


def frame_chips(s: str, font_size=24, size=0.42):
    g = VGroup()
    for ch in s:
        col = BLANK_C if ch == "_" else LETTER_C
        box = Square(size, stroke_color=col, stroke_width=1.5, fill_color=col, fill_opacity=0.2)
        g.add(VGroup(box, data_text("∅" if ch == "_" else ch, font=MONO, font_size=font_size, color=WHITE).move_to(box)))
    return g.arrange(RIGHT, buff=0.04)


class CTC(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.forward()
        self.training()
        self.lattice()

    def card(self):
        card = chapter_card(11, r"Connectionist temporal classification", r"How do you train without knowing which "
                            r"frame is which letter?", part=PART)
        with self.voiceover("Chapter eleven. Connectionist temporal classification."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def problem(self):
        d = load("ctc")
        T = np.asarray(d["lat_lp"]).shape[0]
        txt = str(d["lat_text"])
        head = label(rf"``{txt}'': \ ${T}$ frames of sound, \ ${len(txt)}$ characters, \ and nobody says which is which",
                     font_size=24, color=GREY_A).to_edge(UP, buff=0.5)
        dc = definition_card(r"CTC \ (Graves et al., 2006)",
                             r"the network outputs, for every frame, a probability for each letter and for a "
                             r"\textit{blank}; \ a path through the frames becomes text by merging repeats, then "
                             r"dropping blanks; \ the text's probability adds up every path that becomes it",
                             width=6.4, color=SND_C).move_to([-3.3, 0.2, 0])
        p1 = frame_chips("tth_rr_e_ee_")
        p2 = frame_chips("t_hrr_ee_ee_")
        p3 = frame_chips("tthr_eeee___")
        rows = VGroup()
        for p_, out, ok in ((p1, "three", True), (p2, "three", True), (p3, "thre", False)):
            rows.add(VGroup(p_, MathTex(r"\to", font_size=30), data_text(out, font=MONO, font_size=26,
                                                                           color=SND_C if ok else C.SURPRISE)).arrange(RIGHT, buff=0.25))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        rows.scale_to_fit_width(6.0).move_to([3.6, 0.6, 0])
        nf = min(T, 60)
        frames = VGroup(*[Rectangle(width=0.16, height=0.5, stroke_width=0, fill_color=SND_C, fill_opacity=0.25 + 0.5 * ((k * 7) % 5) / 5)
                          for k in range(nf)]).arrange(RIGHT, buff=0.03).move_to(UP * 1.2)
        letters = VGroup(*[data_text(ch if ch != " " else "·", font=MONO, font_size=30, color=LETTER_C) for ch in txt])
        letters.arrange(RIGHT, buff=0.25).move_to(DOWN * 0.6)
        qs = VGroup(*[MathTex("?", font_size=28, color=GREY_B).move_to(
            (frames[int(i * (nf - 1) / max(len(txt) - 1, 1))].get_bottom() + l_.get_top()) / 2) for i, l_ in enumerate(letters)])
        fl = label(rf"${T}$ frames, \ one every $20$ ms", font_size=22, color=SND_C).next_to(frames, UP, buff=0.15)
        intro = VGroup(frames, letters, qs, fl)
        rl = label(r"three paths of $12$ frames \ (illustrative)", font_size=20, color=GREY_A).next_to(rows, UP, buff=0.2)
        eq = MathTex(r"p(\mathbf y \mid \mathbf x) = \sum_{\pi:\ \mathcal B(\pi) = \mathbf y}\ \prod_{t=1}^{T} y_t(\pi_t)",
                     font_size=36).move_to([2.6, -2.3, 0])
        eql = label(r"$\mathcal B$: \ merge repeats, \ drop blanks", font_size=20, color=GREY_A).next_to(eq, DOWN, buff=0.12)
        with self.voiceover(
            "A recognizer hears a hundred frames of sound for a dozen letters, and training data says only what was "
            "said, not when. The old systems needed each frame labelled, from a previous model. <bookmark mark='a'/> "
            "In 2006 Alex Graves, Santiago Fernández, Faustino Gomez and Jürgen Schmidhuber found a way around it. "
            "The network outputs, for every frame, a probability for each letter and for one extra symbol, a blank. "
            "<bookmark mark='b'/> Any path through the frames becomes text by merging repeated symbols and then "
            "dropping the blanks. <bookmark mark='c'/> A blank is also how a real double letter survives: without "
            "one between them, the two e's of three merge into one. <bookmark mark='d'/> The probability of the "
            "text is the sum over every path that becomes it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frames), FadeIn(fl), FadeIn(letters))
            self.play(LaggedStart(*[FadeIn(q_) for q_ in qs], lag_ratio=0.05))
            vo.wait_until("a")
            self.play(FadeOut(intro))
            self.play(FadeIn(dc))
            vo.wait_until("b")
            self.play(FadeIn(rl), FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Write(eq), FadeIn(eql))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def forward(self):
        colors = {r"\alpha_t(s)": SND_C, r"\alpha_{t-1}(s)": SND_C, r"\alpha_{t-1}(s-1)": SND_C,
                  r"\alpha_{t-1}(s-2)": SND_C}
        rows = [MathTex(r"\mathbf y' = (\varnothing, y_1, \varnothing, y_2, \dots, y_L, \varnothing)", font_size=32),
                cmath(r"\alpha_t(s)", r"=", r"\big(", r"\alpha_{t-1}(s)", r"+", r"\alpha_{t-1}(s-1)", r"\big)",
                      r"\, y_t(y'_s)", colors=colors, font_size=32),
                cmath(r"\alpha_t(s)", r"=", r"\big(", r"\alpha_{t-1}(s)", r"+", r"\alpha_{t-1}(s-1)", r"+",
                      r"\alpha_{t-1}(s-2)", r"\big)", r"\, y_t(y'_s)", colors=colors, font_size=32),
                MathTex(r"p(\mathbf y \mid \mathbf x) = \alpha_T(2L{+}1) + \alpha_T(2L)", font_size=32, color=SND_C)]
        whys = [why(r"blanks around and between \\ the $L$ letters: \ $2L{+}1$ states", font_size=20),
                why(r"stay, \ or step from the state before \\ (when $y'_s$ is a blank, \ or the same letter as $y'_{s-2}$)",
                    font_size=20),
                why(r"otherwise a path may also \\ skip the blank in between", font_size=20),
                why(r"end on the last letter \\ or the final blank", font_size=20)]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.6, align_index=None, buff=0.45, edge=6.9)
        fh = label(r"summing over every path, \ one frame at a time", font_size=30).to_edge(UP, buff=0.35)
        st = ["∅", "a", "∅", "b", "∅"]
        TT = 6
        gx, gy = np.linspace(-4.6, 0.6, TT), np.linspace(-1.1, -3.3, len(st))
        dots = VGroup(*[Dot([gx[t], gy[s_], 0], radius=0.06, color=BLANK_C if st[s_] == "∅" else LETTER_C)
                        for t in range(TT) for s_ in range(len(st))])
        arrs = VGroup()
        for t in range(TT - 1):
            for s_ in range(len(st)):
                for d_ in (0, 1, 2):
                    s2 = s_ + d_
                    if s2 >= len(st) or (d_ == 2 and st[s2] == "∅"):
                        continue
                    arrs.add(Line([gx[t], gy[s_], 0], [gx[t + 1], gy[s2], 0], color=GREY_C, stroke_width=1.2,
                                  stroke_opacity=0.7).set_z_index(-1))
        stl = VGroup(*[data_text(c_, font=MONO, font_size=20, color=BLANK_C if c_ == "∅" else LETTER_C)
                       .move_to([gx[0] - 0.4, gy[i], 0]) for i, c_ in enumerate(st)])
        lt = note(r"the lattice for ``ab'', \ $6$ frames \ (schematic)", font_size=20).move_to([3.0, -2.2, 0])
        lat = VGroup(arrs, dots, stl, lt)
        hmm = label(r"Part 7's forward algorithm: \\ $O(T \cdot L)$ steps, \\ and $-\log p$ \\ is a loss to descend",
                    font_size=22, color=GREY_A).move_to([5.0, -2.2, 0])
        with self.voiceover(
            "There are exponentially many paths, but the sum is cheap. <bookmark mark='a'/> Write the transcript "
            "with a blank before, between and after its letters: two L plus one states, in order. "
            "<bookmark mark='b'/> A path at state s at time t was, one frame earlier, at s, or at the state just "
            "before. <bookmark mark='c'/> And it may also skip a blank, jumping from two states back, unless that "
            "would merge two equal letters. Multiply by the network's probability for the symbol at s. "
            "<bookmark mark='d'/> The paths that end on the last letter or the final blank add up to the "
            "transcript's probability. <bookmark mark='e'/> It is the forward algorithm of Part 7's hidden Markov "
            "models, with the transcript as the chain of states, and minus its logarithm is a loss whose gradient "
            "comes from the same recursion run backward."
        ) as vo:
            self.play(FadeIn(fh))
            vo.wait_until("a")
            step(0)
            self.play(FadeIn(dots), FadeIn(stl), FadeIn(lt))
            vo.wait_until("b")
            step(1, transform=False)
            self.play(Create(arrs), run_time=1.5)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3, transform=False)
            vo.wait_until("e")
            self.play(FadeOut(lt), FadeIn(hmm))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def training(self):
        d = load("ctc")
        alpha = str(d["alphabet"])
        lps = np.asarray(d["snap_lp"])
        steps = [int(s) for s in d["snap_steps"]]
        texts = [str(t) for t in d["snap_text"]]
        txt = str(d["lat_text"])
        used = [0, 1] + sorted({alpha.index(c) for c in txt if c != " "})
        names = ["∅", "·"] + [alpha[i] for i in used[2:]]
        W, H = 7.4, 3.0

        def post(k):
            P = np.exp(lps[k][:, used]).T
            return heat(P, W, H, color=SND_C, lo=0, hi=1).move_to([-2.0, 0.3, 0])

        cur = post(0)
        rl = VGroup(*[data_text(nm, font=MONO, font_size=16, color=BLANK_C if i == 0 else WHITE)
                      .move_to([cur.get_left()[0] - 0.22, cur.get_top()[1] - H / len(used) * (i + 0.5), 0])
                      for i, nm in enumerate(names)])
        top = label(rf"the network's probabilities, \ frame by frame, \ for a voice it never heard \ (``{txt}'')",
                    font_size=20, color=GREY_A).next_to(cur, UP, buff=0.15)
        t = ValueTracker(0)
        out = [data_text(f"→ {s or '(nothing)'}", font=MONO, font_size=24, color=SND_C) for s in texts]
        for o in out:
            o.next_to(cur, DOWN, buff=0.3).align_to(cur, LEFT)
        cnt = always_redraw(lambda: label(rf"step ${int(t.get_value()):,}$".replace(",", "{,}"), font_size=24, color=C.BITS)
                            .next_to(cur, DOWN, buff=0.3).align_to(cur, RIGHT))
        cv = np.asarray(d["curves"])
        ax = axes([0, int(cv[0, -1, 0]), 500], [0, float(np.percentile(cv[:, :, 1], 99)) * 1.05, 1], x_length=3.6,
                  y_length=2.6, xlabel=r"steps", ylabel=r"CTC loss, \ three seeds", xticks=[0, int(cv[0, -1, 0])],
                  center=[4.6, 0.4, 0])
        lines = VGroup(*[curve(ax.ax, c[:, 0], np.minimum(c[:, 1], ax.ax.y_range[1]), SND_C, 2) for c in cv])
        params = int(d["params"])
        am = lps[-1].argmax(1)
        blank = float((am == 0).mean())
        runs = [len(r_) for r_ in "".join("x" if a_ != 0 else " " for a_ in am).split()]
        run_len = float(np.mean(runs)) if runs else 0.0
        spikes = ("letters appear as sharp spikes" if blank > 0.5 and run_len < 3 else "letters appear")
        with self.voiceover(
            f"We trained a small recognizer this way: {params / 1e3:.0f} thousand parameters in seven convolutions, "
            "on digit strings spoken by ten Kokoro voices, three seeds. <bookmark mark='a'/> "
            "Here is what it hears in a string from a voice it never heard, as training goes on. At first every "
            "frame is a blur. <bookmark mark='b'/> Then the blank takes over, the cheapest way to be right about "
            f"most frames. <bookmark mark='c'/> Then {spikes} between the blanks: at the end the blank wins "
            f"{100 * blank:.0f} percent of the frames, and a letter lasts {run_len:.1f} frames on average, CTC's "
            "famously peaky alignments. The greedy reading below takes the likeliest symbol at each frame, then "
            "merges and drops."
        ) as vo:
            self.play(FadeIn(cur), FadeIn(rl), FadeIn(top), FadeIn(out[0]), FadeIn(ax))
            self.add(cnt)
            vo.wait_until("a")
            self.play(Create(lines), run_time=2.0)
            marks = ["b", "c"]
            for k in range(1, len(steps)):
                if k == 2:
                    vo.wait_until(marks[0])
                if k == len(steps) - 2:
                    vo.wait_until(marks[1])
                nxt = post(k)
                self.play(FadeTransform(cur, nxt), FadeTransform(out[k - 1], out[k]), t.animate.set_value(steps[k]),
                          run_time=1.0)
                cur = nxt
        self.wait(0.3)
        self.remove(cnt)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lattice(self):
        d = load("ctc")
        alpha = str(d["alphabet"])
        G = np.asarray(d["lat_gamma"]).T  # states x frames
        path = np.asarray(d["lat_path"])
        ext = [int(e) for e in d["lat_ext"]]
        S, T = G.shape
        W, H = 8.2, 4.2
        img = heat(np.sqrt(np.clip(G, 0, 1)), W, H, color=SND_C, lo=0, hi=1).move_to([-2.4, -0.1, 0])
        cw, ch = W / T, H / S
        ul = img.get_corner(UL)
        pts = [ul + np.array([cw * (t + 0.5), -ch * (s + 0.5), 0]) for t, s in enumerate(path)]
        pl = VMobject(color=WHITE, stroke_width=2.5).set_points_as_corners(pts)
        ylab = VGroup(*[data_text("∅" if e == 0 else alpha[e], font=MONO, font_size=11,
                                  color=BLANK_C if e == 0 else WHITE).move_to(ul + np.array([-0.15, -ch * (s + 0.5), 0]))
                        for s, e in enumerate(ext)])
        tl = label(r"how likely each state is at each frame, \ given the whole utterance; \ white: \ the best path",
                   font_size=20, color=GREY_A).next_to(img, UP, buff=0.15)
        tot = float(d["lat_total"])
        totl = label(rf"$\log p(\text{{transcript}}) = {tot:.2f}$, \ the same as PyTorch's CTC loss", font_size=20,
                     color=SND_C).next_to(img, DOWN, buff=0.15)
        wer = np.asarray(d["wer"], float)
        seen = np.asarray(d["wer_seen"], float)
        rows = spread_rows([(r"voices it trained on", C.INTERVAL, 100 * seen), (r"two new voices", SND_C, 100 * wer)],
                           x_max=max(5.0, 100 * float(max(wer.max(), seen.max())) * 1.15), width=2.2, font_size=18,
                           label_w=2.0, fmt="{:.1f}")
        rows.move_to([4.4, 0.8, 0])
        keep_in_frame(rows, margin=0.25)
        rl_ = label(r"word error rate, \ $\%$ \ (three seeds)", font_size=18, color=GREY_A).next_to(rows, UP, buff=0.2)
        hist = VGroup(*[label(t_, font_size=18, color=GREY_A) for t_ in (
            r"2014: \ Deep Speech (Baidu): \ CTC, \ thousands of hours", r"2012--15: \ RNN-T, \ listen-attend-spell: \\ "
            r"letters that depend on each other")]).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.5, -1.8, 0])
        verdict = (f"{100 * wer.mean():.1f} percent of the digit words wrong for the two new voices, "
                   f"{100 * seen.mean():.1f} percent for voices it trained on")
        with self.voiceover(
            "And here is the lattice itself, computed from the trained network: the states of the transcript down "
            "the side, the frames across. <bookmark mark='a'/> The brightness is how likely each state is at each "
            "frame, from the forward and backward passes together; the white line is the single best path. "
            f"<bookmark mark='b'/> The forward algorithm's total, {tot:.2f} in natural log, agrees with PyTorch's own "
            f"CTC loss. <bookmark mark='c'/> Averaged over three seeds: {verdict}. <bookmark mark='d'/> In 2014 Baidu's "
            "Deep Speech trained CTC on thousands of hours and did without the old pipeline. CTC treats each frame's "
            "letter as independent of the others, so later systems, RNN transducers and attention-based "
            "recognizers, let each letter depend on the ones before."
        ) as vo:
            self.play(FadeIn(img), FadeIn(ylab), FadeIn(tl))
            vo.wait_until("a")
            self.play(Create(pl), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(totl))
            vo.wait_until("c")
            self.play(FadeIn(rl_), FadeIn(rows))
            vo.wait_until("d")
            self.play(FadeIn(hist))
        self.wait(0.3)
        self.clear_scene()
