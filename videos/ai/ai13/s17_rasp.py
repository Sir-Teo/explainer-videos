from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai13.common import A, K, MONO, PART, Q, SINKC, V, framed, heat_image, load

SEL = A


class RASP(VoiceoverScene):
    def construct(self):
        self.card()
        self.language()
        self.histogram()
        self.sort()
        self.limits()

    def card(self):
        card = chapter_card(16, r"What a transformer can compute", r"Is there a programming language for attention?",
                            part=PART)
        with self.voiceover("Chapter sixteen. What a transformer can compute."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def language(self):
        prims = VGroup(
            VGroup(data_text("select(keys, queries, predicate)", font=MONO, font_size=24, color=SEL),
                   label(r"which positions each position looks at: \ an attention pattern", font_size=20, color=GREY_A)),
            VGroup(data_text("aggregate(selector, values)", font=MONO, font_size=24, color=V),
                   label(r"the average of the selected values: \ attention's output", font_size=20, color=GREY_A)),
            VGroup(data_text("map / zip, elementwise", font=MONO, font_size=24, color=C.MLP),
                   label(r"any function of one position: \ the MLP", font_size=20, color=GREY_A)),
        )
        for p_ in prims:
            p_.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        prims.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([-3.0, 0.9, 0])
        prog = code_block(["same  = select(tokens, tokens, ==)", "hist  = selector_width(same)", "",
                           "less  = select(tokens, tokens, <)", "rank  = selector_width(less)",
                           "sort  = aggregate(select(rank, indices, ==), tokens)"], font_size=20)
        prog.move_to([3.4, 0.9, 0])
        pl = VGroup(label(r"histogram: \ one layer", font_size=20, color=Q), label(r"sort: \ two layers", font_size=20,
                                                                                       color=Q))
        pl[0].next_to(prog[1], RIGHT, buff=0.2)
        pl[1].next_to(prog[5], DOWN, buff=0.15).align_to(prog, RIGHT)
        keep_in_frame(VGroup(prog, pl))
        cite_ = cite(r"G.~Weiss, Y.~Goldberg \& E.~Yahav, \textit{Thinking Like Transformers} (2021); \ "
                     r"D.~Lindner et al., \textit{Tracr} (2023)", corner=DL)
        with self.voiceover(
            "We have taken attention apart. What can the whole machine compute? In 2021 Gail Weiss, Yoav Goldberg "
            "and Eran Yahav wrote it down as a programming language, RASP, with only the operations a transformer "
            "has. <bookmark mark='a'/> Select builds an attention pattern from a comparison of keys and queries. "
            "<bookmark mark='b'/> Aggregate averages the selected values. <bookmark mark='c'/> And elementwise "
            "functions are the MLPs. <bookmark mark='d'/> Programs in it read like this: a histogram, how many "
            "times each token occurs, in one layer; sorting in two. Every program says how many layers and heads "
            "it needs, and in 2023 a team at DeepMind built Tracr, which compiles such programs into real "
            "transformer weights. We compiled two by hand."
        ) as vo:
            self.play(FadeIn(prims[0]), FadeIn(cite_))
            vo.wait_until("a")
            self.play(Indicate(prims[0][0], color=SEL))
            vo.wait_until("b")
            self.play(FadeIn(prims[1]))
            vo.wait_until("c")
            self.play(FadeIn(prims[2]))
            vo.wait_until("d")
            self.play(FadeIn(prog), FadeIn(pl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def histogram(self):
        r = load("rasp")
        x = [int(v) for v in r["hist_x"]]
        alpha = str(r["hist_alphabet"])
        cnt = [int(v) for v in r["hist_counts"]]
        Amat = np.asarray(r["hist_A"])
        n = len(x)
        img = framed(heat_image(Amat, 3.6, 3.6, color=SEL, gamma=1.0)).move_to([-3.4, -0.5, 0])
        cell = 3.6 / (n + 1)
        cols = VGroup(label(r"$\langle s\rangle$", font_size=16, color=SINKC).next_to(img.get_corner(UL) + RIGHT * cell / 2, UP, buff=0.1),
                      *[data_text(alpha[c], font=MONO, font_size=18, color=K).move_to(
                          img.get_corner(UL) + RIGHT * cell * (j + 1.5) + UP * 0.22) for j, c in enumerate(x)])
        rows = VGroup(*[data_text(alpha[c], font=MONO, font_size=18, color=Q).move_to(
            img.get_corner(UL) + LEFT * 0.22 + DOWN * cell * (j + 1.5)) for j, c in enumerate(x)])
        outs = VGroup(*[MathTex(str(c), font_size=22, color=V).move_to(img.get_corner(UR) + RIGHT * 0.3 + DOWN * cell * (j + 1.5))
                        for j, c in enumerate(cnt)])
        ol = label(r"count", font_size=18, color=V).next_to(outs, UP, buff=0.12)
        rows_ = [
            cmath(r"\text{score}(i, j)", r"=", r"\beta\,[x_i = x_j], \quad \text{score}(i, \langle s\rangle) = \beta",
                  font_size=28),
            cmath(r"\text{weight on } \langle s\rangle", r"=", r"\frac{1}{c_i + 1}", font_size=28,
                  colors={r"\text{weight on } \langle s\rangle": SINKC}),
            cmath(r"c_i", r"=", r"\text{MLP}\big(\tfrac{1}{c_i + 1}\big)", font_size=28),
        ]
        whys = [why(r"one-hot tokens: \ $W_{QK}$ is a lookup table", font_size=18),
                why(r"$c_i$ matches, plus $\langle s\rangle$, all equal", font_size=18),
                why(r"a ReLU layer reads the count back", font_size=18)]
        step = ladder(self, rows_, whys, keep=3, top=2.9, x=1.6, buff=0.62, edge=6.9)
        ok, tr = int(r["hist_ok"]), int(r["hist_trials"])
        p16, pb = int(r["prec_fp16"]), int(r["prec_bf16"])
        res = VGroup(label(rf"run on ${tr:,}$ random sequences of up to $40$: \ ${ok:,}$ right".replace(",", "{,}"),
                           font_size=22, color=C.TRUE_P),
                     label(rf"counts told apart in bfloat16: \ up to ${pb}$; \ in float16: \ ${p16:,}$".replace(",", "{,}"),
                           font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([2.6, -2.6, 0])
        keep_in_frame(res)
        with self.voiceover(
            "The histogram first. Give the tokens one-hot vectors, and a head's QK matrix becomes a lookup table: "
            "any comparison of two tokens we like. <bookmark mark='a'/> Score each pair beta if the tokens match, "
            "and give a start marker the same score from every query. <bookmark mark='b'/> A token that occurs c "
            "times then splits its attention evenly over its c copies and the marker, so the marker gets one over "
            "c plus one. <bookmark mark='c'/> Let only the marker carry a value, and the head's output is one over "
            "c plus one: a small ReLU layer reads the count back. The marker plays exactly the part of chapter "
            f"twelve's sink. <bookmark mark='d'/> We ran it on {tr:,} random sequences: "
            + (f"all {ok:,} correct. " if ok == tr else f"{ok:,} correct. ")
            + "But notice what it needs: telling one over c plus one from one over c plus two takes more bits as "
            f"c grows. In bfloat16 the counts blur after {pb}; in float16, after {p16:,}. A fixed transformer works "
            "with fixed precision, and this is one reason length is hard."
        ) as vo:
            self.play(FadeIn(img), FadeIn(cols), FadeIn(rows))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            self.play(FadeIn(outs), FadeIn(ol))
            vo.wait_until("d")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sort(self):
        r = load("rasp")
        x = [int(v) for v in r["sort_x"]]
        y = [int(v) for v in r["sort_y"]]
        rank = [int(v) for v in r["sort_rank"]]
        A1, A2 = np.asarray(r["sort_A1"]), np.asarray(r["sort_A2"])
        n = len(x)

        def letters(seq, color, y0, x0=0.0, width=5.0):
            step = width / len(seq)
            return VGroup(*[data_text(chr(97 + c), font=MONO, font_size=30, color=color).move_to([x0 - width / 2 + step * (i + 0.5), y0, 0])
                            for i, c in enumerate(seq)])

        inp = letters(x, WHITE, 2.9, -3.2)
        outp = letters(y, V, 2.9, 3.4)
        arr = Arrow(inp.get_right() + RIGHT * 0.2, outp.get_left() + LEFT * 0.2, buff=0.1, color=GREY_B)
        S = 3.0
        i1 = framed(heat_image(A1, S, S, color=SEL, gamma=1.0)).move_to([-3.2, -0.3, 0])
        i2 = framed(heat_image(A2, S, S, color=SEL, gamma=1.0)).move_to([3.4, -0.3, 0])
        t1 = label(r"layer 1: \ select keys smaller than the query, \\ plus $\langle s\rangle$: \ the weight on it is "
                   r"$\tfrac{1}{\text{rank} + 1}$", font_size=18, color=GREY_A).next_to(i1, DOWN, buff=0.15)
        t2 = label(r"layer 2: \ output position $p$ selects \\ the token whose rank is $p$", font_size=18,
                   color=GREY_A).next_to(i2, DOWN, buff=0.15)
        rk = VGroup(*[MathTex(str(v), font_size=20, color=Q).next_to(i1, RIGHT, buff=0.12)
                      .set_y(i1.get_top()[1] - S / (n + 1) * (j + 1.5)) for j, v in enumerate(rank)])
        rkl = label(r"rank", font_size=16, color=Q).next_to(rk, UP, buff=0.1)
        ok, tr = int(r["sort_ok"]), int(r["sort_trials"])
        res = label(rf"${ok:,}$ of ${tr:,}$ random inputs sorted".replace(",", "{,}"), font_size=22, color=C.TRUE_P)
        res.to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Sorting takes two layers. <bookmark mark='a'/> In the first, each token selects every token smaller "
            "than itself, plus the marker: the marker's share gives its rank, how many come before it in sorted "
            "order. <bookmark mark='b'/> In the second, output position p selects the token whose rank is p and "
            "copies it. <bookmark mark='c'/> "
            + (f"Our hand-built weights sort every one of {tr:,} random inputs." if ok == tr else
               f"Our hand-built weights sort {ok:,} of {tr:,} random inputs.")
            + " Nobody trained them: a transformer's weights can be a program."
        ) as vo:
            self.play(FadeIn(inp), GrowArrow(arr), FadeIn(outp))
            vo.wait_until("a")
            self.play(FadeIn(i1), FadeIn(t1), FadeIn(rk), FadeIn(rkl))
            vo.wait_until("b")
            self.play(FadeIn(i2), FadeIn(t2))
            vo.wait_until("c")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def limits(self):
        th = theorem_card(r"log-precision transformers are in $\mathsf{TC}^0$",
                          r"a transformer of fixed depth, with numbers of $O(\log n)$ bits on inputs of length $n$, can "
                          r"be simulated by constant-depth threshold circuits of polynomial size",
                          who=r"W.~Merrill \& A.~Sabharwal (2023)", width=7.6, font_size=22).move_to([-2.6, 1.6, 0])
        cons = VGroup(
            label(r"so, unless $\mathsf{TC}^0$ is as strong as $\mathsf{NC}^1$:", font_size=22, color=GREY_A),
            label(r"no fixed-depth transformer tracks the composition \\ of permutations of five things, at every "
                  r"length \\ (Merrill, Petty \& Sabharwal 2024; \ Barrington 1989)", font_size=20, color=WHITE),
            label(r"depth matters: \ one layer could not build an induction head \ (chapter 14)", font_size=20,
                  color=WHITE),
            label(r"thinking out loud adds serial steps: \ chain of thought \ (Part 28)", font_size=20, color=C.BITS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([-1.4, -1.85, 0])
        keep_in_frame(cons)
        conj = label(r"Zhou et al.\ (2023): \ transformers tend to generalize \\ to longer inputs when a short RASP \\ "
                     r"program solves the task at every length", font_size=20, color=Q).move_to([4.6, 1.5, 0])
        with self.voiceover(
            "What can't a transformer do? A fixed number of layers is a fixed amount of sequential work. "
            "<bookmark mark='a'/> William Merrill and Ashish Sabharwal proved in 2023 that a transformer of fixed "
            "depth, whose numbers have a number of bits that grows only like the logarithm of the input's length, "
            "can be simulated by constant-depth threshold circuits: the class complexity theorists call T C zero. "
            "<bookmark mark='b'/> If, as most believe, that class is weaker than N C one, then no fixed-depth "
            "transformer can track a sequence of shuffles of five objects at every length, a task that needs "
            "genuinely sequential steps. Depth matters in practice too: one layer could not build an induction "
            "head. <bookmark mark='c'/> The way out is to let the model write: every token of a chain of thought "
            "is another pass through all the layers, which is how reasoning models buy serial time, in Part 28. "
            "<bookmark mark='d'/> And RASP predicts what trains well: Hattie Zhou and colleagues found that "
            "transformers tend to generalize to longer inputs exactly when a short RASP program solves the task at "
            "every length."
        ) as vo:
            self.play(FadeIn(th))
            vo.wait_until("b")
            self.play(FadeIn(cons[0]), FadeIn(cons[1]))
            self.play(FadeIn(cons[2]))
            vo.wait_until("c")
            self.play(FadeIn(cons[3]))
            vo.wait_until("d")
            self.play(FadeIn(conj))
        self.wait(0.3)
        self.clear_scene()
