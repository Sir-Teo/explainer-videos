from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai7.common import CONSONANT, HIDDEN, PART, SEEN, VOWEL, card_in, load

ALPHA27 = " abcdefghijklmnopqrstuvwxyz"
FWD, BWD = C.BITS, C.TRUE_P


def letter_color(ch):
    return GREY_B if ch == " " else VOWEL if ch in "aeiou" else CONSONANT


class BaumWelch(VoiceoverScene):
    def construct(self):
        card_in(self, 7, r"Baum--Welch, and machines that listen", r"How does a hidden Markov model learn?",
                "Chapter seven. Baum-Welch, and machines that listen.")
        self.derive()
        self.learn()
        self.speech()

    # ------------------------------------------------------------------
    def derive(self):
        colors = {r"\alpha_t(i)": FWD, r"\beta_t(i)": BWD, r"\beta_{t+1}(j)": BWD, r"\gamma_t(i)": HIDDEN,
                  r"\xi_t(i, j)": HIDDEN, r"A_{ij}": HIDDEN, r"B_j(x_{t+1})": SEEN}
        rows = [
            cmath(r"\beta_t(i)", r"=", r"\sum_j A_{ij}\, B_j(x_{t+1})\, \beta_{t+1}(j)", colors=colors, font_size=36),
            cmath(r"\gamma_t(i)", r"=", r"\frac{\alpha_t(i)\, \beta_t(i)}{p(x)}", colors=colors, font_size=36),
            cmath(r"\xi_t(i, j)", r"=", r"\frac{\alpha_t(i)\, A_{ij}\, B_j(x_{t+1})\, \beta_{t+1}(j)}{p(x)}",
                  colors=colors, font_size=36),
            cmath(r"A_{ij}", r"\leftarrow", r"\frac{\sum_t \xi_t(i, j)}{\sum_t \gamma_t(i)}", r"\qquad",
                  r"B_j(x)", r"\leftarrow", r"\frac{\sum_{t:\, x_t = x} \gamma_t(j)}{\sum_t \gamma_t(j)}", colors=colors,
                  font_size=36),
        ]
        whys = [why(r"backward: \ the letters still to come"),
                why(r"E step: \ how likely state $i$ \\ was at time $t$"),
                why(r"and the move $i \to j$ \\ at time $t$"),
                why(r"M step: \ expected counts, \\ normalized")]
        step = ladder(self, rows, whys, keep=4, top=2.6, x=-2.4, buff=0.6, edge=6.8)
        head = label(r"EM for hidden Markov models: \ forward--backward", font_size=32).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Third: how does the model learn A and B from letters alone? It's chapter four's EM again, and for this "
            "model it's called Baum–Welch. <bookmark mark='a'/> Run the forward sweep, and a mirror image, the "
            "backward sweep: beta is the probability of the letters still to come, from each state. "
            "<bookmark mark='b'/> Alpha times beta, divided by the probability of the whole text, is the chance that "
            "the chain was in state i at time t. That's the E step's soft colouring, one per letter. "
            "<bookmark mark='c'/> The same trick gives the chance of each move, from i to j, at each moment. "
            "<bookmark mark='d'/> The M step just counts: expected moves from i to j, over expected visits to i; "
            "expected emissions of each letter, over expected visits. EM's theorem guarantees every round raises the "
            "likelihood."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def learn(self):
        h = load("hmm")
        A, Bs, lls = np.asarray(h["A"]), np.asarray(h["Bs"]), np.asarray(h["lls"])
        assert set("aeiou") <= set(h["vowel_side"])
        s_pos = [np.array([-5.0, 1.9, 0]), np.array([-5.0, -1.1, 0])]
        states = VGroup(*[VGroup(Circle(radius=0.45, color=HIDDEN, stroke_width=4, fill_color=BACKGROUND, fill_opacity=1)
                                 .move_to(p_), MathTex(rf"s_{k + 1}", font_size=36, color=HIDDEN).move_to(p_))
                          for k, p_ in enumerate(s_pos)])
        sw = VGroup(CurvedArrow(s_pos[0] + DOWN * 0.45 + LEFT * 0.15, s_pos[1] + UP * 0.45 + LEFT * 0.15, angle=0.5,
                                color=GREY_B, stroke_width=3),
                    CurvedArrow(s_pos[1] + UP * 0.45 + RIGHT * 0.15, s_pos[0] + DOWN * 0.45 + RIGHT * 0.15, angle=0.5,
                                color=GREY_B, stroke_width=3))
        swl = VGroup(MathTex(f"{A[0, 1]:.2f}", font_size=26, color=GREY_A).next_to(sw[0], LEFT, buff=0.1),
                     MathTex(f"{A[1, 0]:.2f}", font_size=26, color=GREY_A).next_to(sw[1], RIGHT, buff=0.1))
        W, H = 0.3, 2.0
        x0 = -3.7

        def bars(B):
            g = VGroup()
            for k, yb in enumerate((1.2, -1.8)):
                for i, ch in enumerate(ALPHA27):
                    h_ = max(H * B[k][i] / 0.4, 0.01)
                    g.add(Rectangle(width=W * 0.8, height=h_, stroke_width=0, fill_color=letter_color(ch),
                                    fill_opacity=0.9).move_to([x0 + i * W, yb + h_ / 2, 0]))
            return g

        it = ValueTracker(0)
        bar_g = always_redraw(lambda: bars(Bs[int(round(it.get_value()))]))
        labs = VGroup(*[Text("␣" if ch == " " else ch, font="DejaVu Sans Mono", font_size=16, color=letter_color(ch))
                        .move_to([x0 + i * W, yb - 0.2, 0]) for yb in (1.2, -1.8) for i, ch in enumerate(ALPHA27)])
        links = VGroup(*[DashedLine(s_pos[k] + RIGHT * 0.45, [x0 - 0.3, yb + 0.6, 0], color=HIDDEN, stroke_width=2)
                         for k, yb in enumerate((1.2, -1.8))])
        itv = Integer(0, font_size=30)
        itl = VGroup(label(r"Baum--Welch round", font_size=24, color=GREY_A), itv).arrange(RIGHT, buff=0.15)
        itl.to_corner(UR, buff=0.4)
        bits = DecimalNumber(-lls[0], num_decimal_places=2, font_size=30, color=C.BITS)
        bitl = VGroup(label(r"bits per letter:", font_size=24, color=GREY_A), bits).arrange(RIGHT, buff=0.15)
        bitl.next_to(itl, DOWN, buff=0.15).align_to(itl, RIGHT)
        head = label(r"Each hidden state emits letters from its own table", font_size=28).to_edge(UP, buff=0.3).shift(LEFT * 1.0)
        found = label(r"$s_1$: \ space and a, e, i, o, u \quad $s_2$: \ every consonant", font_size=28, color=WHITE)
        found.to_edge(DOWN, buff=0.25)
        cite_ = cite(r"R.~J.~Cave \& L.~P.~Neuwirth (1980); \ L.~E.~Baum et al.\ (1970)", corner=UR).shift(DOWN * 0.9)
        n_it = len(Bs) - 1
        with self.voiceover(
            f"Give it two hidden states, {h['n']:,} letters of the books, and random first guesses. "
            "<bookmark mark='b'/> Then run Baum–Welch, and watch what each state learns to emit."
        ) as vo:
            self.play(FadeIn(head), FadeIn(states), FadeIn(bar_g), FadeIn(labs), Create(links), FadeIn(itl), FadeIn(bitl))
            vo.wait_until("b")
            for k in (1, 2, 3, 5, 8, 12, 20, 35, n_it):
                self.play(it.animate.set_value(k), ChangeDecimalToValue(itv, k), ChangeDecimalToValue(bits, -lls[min(k, len(lls) - 1)]),
                          run_time=0.8)
        with self.voiceover(
            "One state ends up with the space, and a, e, i, o and u. The other takes every consonant. "
            f"<bookmark mark='a'/> And they take turns: after one, the other, about {100 * A[0, 1]:.0f} percent of "
            "the time. Nobody mentioned vowels. Cave and Neuwirth found exactly this in 1980."
        ) as vo:
            self.play(FadeIn(found), FadeIn(cite_))
            vo.wait_until("a")
            self.play(Create(sw), FadeIn(swl))
        bar_g.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def speech(self):
        tag = schematic_tag(UR)
        g = np.random.default_rng(7)
        t = np.linspace(0, 1, 500)
        y = np.sin(2 * np.pi * 9 * t) * np.exp(-((t - 0.3) / 0.12) ** 2) + 0.7 * np.sin(2 * np.pi * 14 * t) * np.exp(
            -((t - 0.72) / 0.1) ** 2) + 0.08 * g.normal(size=len(t))
        wavef = VMobject(color=GREY_B, stroke_width=2).set_points_as_corners([[-6.2 + 3.0 * a, 2.2 + 0.5 * b, 0]
                                                                              for a, b in zip(t, y)])
        frames = VGroup(*[Rectangle(width=0.22, height=0.9, stroke_color=GREY_C, stroke_width=1, fill_color=SEEN,
                                    fill_opacity=0.15 + 0.6 * abs(float(np.sin(i)))).move_to([-6.0 + 0.25 * i, 0.6, 0])
                          for i in range(12)])
        fl = label(r"frames of sound features, \\ every $10$ ms", font_size=20, color=GREY_A).next_to(frames, DOWN, buff=0.15)
        ph = VGroup()
        for k, p_ in enumerate((r"/k/", r"/\ae/", r"/t/")):
            sts = VGroup(*[Circle(radius=0.22, color=HIDDEN, stroke_width=2.5).move_to([-2.0 + 0.55 * j + 1.85 * k, 0.9, 0])
                           for j in range(3)])
            arr = VGroup(*[Arrow(sts[j].get_right(), sts[j + 1].get_left(), buff=0.03, stroke_width=2, color=GREY_B,
                                 max_tip_length_to_length_ratio=0.3) for j in range(2)])
            ph.add(VGroup(sts, arr, label(p_, font_size=24, color=HIDDEN).next_to(sts, UP, buff=0.15)))
        pl = label(r"each sound of the language: \ a three-state hidden Markov model", font_size=20, color=HIDDEN)
        pl.next_to(ph, DOWN, buff=0.75)
        bells = VGroup(*[FunctionGraph(lambda u, m=m, s=s: 0.5 * np.exp(-(u - m) ** 2 / (2 * s * s)), x_range=[-0.7, 0.7],
                                       color=SEEN, stroke_width=2.5) for m, s in ((-0.25, 0.12), (0.1, 0.18), (0.35, 0.1))])
        bells.move_to([0.2, -0.75, 0])
        bl = label(r"each state emits features \\ from a mixture of Gaussians (chapter 4)", font_size=20, color=SEEN)
        bl.next_to(bells, DOWN, buff=0.15)
        word = VGroup(label(r"``cat''", font_size=34), label(r"words: \ a dictionary \\ and an $n$-gram model \\ "
                                                             r"(chapter 9)", font_size=20, color=GREY_A))
        word.arrange(DOWN, buff=0.15).move_to([5.3, 0.9, 0])
        arrs = VGroup(Arrow([-3.0, 0.6, 0], [-2.35, 0.8, 0], color=GREY_B, stroke_width=2.5),
                      Arrow([3.1, 0.9, 0], [4.0, 0.9, 0], color=GREY_B, stroke_width=2.5))
        hist = VGroup(
            history_card(1975, r"James Baker; \ Fred Jelinek's group at IBM", r"speech recognition as statistics: \ "
                         r"DRAGON, \ and \textit{Continuous speech recognition by statistical methods} (1976)", width=6.4),
            history_card(2012, r"G.~Hinton et al.", r"deep networks replace the Gaussian mixtures; \ later, end-to-end "
                         r"models and CTC (Part 23)", width=5.6),
        ).arrange(RIGHT, buff=0.3, aligned_edge=UP).to_edge(DOWN, buff=0.3)
        quote = label(r"``Every time I fire a linguist, the performance of the speech recognizer goes up.'' \\ "
                      r"--- attributed to Fred Jelinek, IBM, 1980s \ (his own recollections of the wording varied)",
                      font_size=22, color=C.HUMAN).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "This is how machines learned to listen. In the 1970s, James Baker's DRAGON system and Fred Jelinek's "
            "group at IBM treated speech recognition as a statistics problem. <bookmark mark='a'/> Cut the sound into "
            "frames, a hundred a second, each a vector of features. <bookmark mark='b'/> Model every sound of the "
            "language as a small hidden Markov model, three states from left to right, and chain them into words. "
            "<bookmark mark='c'/> Each state emits feature vectors from a mixture of Gaussians: chapter four's "
            "mixtures inside chapter six's chain, all trained by Baum–Welch on hours of recorded speech. "
            "<bookmark mark='d'/> A dictionary turns sounds into words, and a counting model of word sequences, "
            "chapter nine's subject, chooses between sentences that sound alike. Viterbi finds the best one. "
            "<bookmark mark='e'/> Data beat rules. The remark usually attributed to Jelinek, in its best-known form: "
            "every time I fire a linguist, the performance of the speech recognizer goes up. He remembered the "
            "wording differently, but the point stuck. <bookmark mark='f'/> This design ran speech recognition for "
            "three decades, until, around 2012, deep networks replaced the Gaussian mixtures, and later the whole "
            "pipeline. Part twenty-three picks up the story."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(hist[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Create(wavef), FadeIn(frames), FadeIn(fl), run_time=1.5)
            vo.wait_until("b")
            self.play(GrowArrow(arrs[0]), LaggedStart(*[FadeIn(p_) for p_ in ph], lag_ratio=0.3), FadeIn(pl))
            vo.wait_until("c")
            self.play(FadeOut(hist[0]), Create(bells), FadeIn(bl))
            vo.wait_until("d")
            self.play(GrowArrow(arrs[1]), FadeIn(word))
            vo.wait_until("e")
            self.play(FadeIn(quote))
            vo.wait_until("f")
            self.play(FadeOut(quote), FadeIn(hist[1], shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()
