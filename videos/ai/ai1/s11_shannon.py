from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai1.common import MONO, letter_row, load


class Shannon1951(VoiceoverScene):
    def construct(self):
        self.card()
        self.twins()
        self.histogram()
        self.people()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(8, r"Shannon's 1951 experiment", r"How much information is there in English, really?",
                            lit=(1951,), part=1)
        with self.voiceover("Chapter eight. Back to Shannon's guessing game, now that we have the tools to read it.") as vo:
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def twins(self):
        g = load("game")
        sent = g["sentence"][:19]
        ranks = [int(r) for r in g["sentence_ranks"][:19]]
        assert sent == "there is no reverse"
        head = label(r"The guess counts \textit{are} a code", font_size=38).to_edge(UP, buff=0.4)
        txt = letter_row(sent, font_size=28).move_to([-4.6, 1.9, 0])
        nums = Text(" ".join(str(r) for r in ranks), font=MONO, font_size=22, color=C.GUESS)
        boxes = VGroup()
        for k, (title, col) in enumerate(((r"guesser", C.GUESS), (r"identical twin", C.GUESS))):
            b = RoundedRectangle(width=2.6, height=1.2, corner_radius=0.15, color=col, stroke_width=3)
            b.move_to([-4.6 + 9.2 * k, 0.2, 0])
            t = label(title, font_size=26, color=col)
            if t.width > b.width - 0.4:
                t.scale_to_fit_width(b.width - 0.4)
            boxes.add(VGroup(b, t.move_to(b)))
        sender = label(r"sender", font_size=24, color=GREY_B).next_to(boxes[0], DOWN, buff=0.2)
        receiver = label(r"receiver", font_size=24, color=GREY_B).next_to(boxes[1], DOWN, buff=0.2)
        nums.move_to([0, 0.2, 0])
        if nums.width > 5.4:
            nums.width = 5.4
        chan = SurroundingRectangle(nums, color=GREY_C, buff=0.18, corner_radius=0.1, stroke_width=1.5)
        chan_l = label(r"sent: \ only the guess counts", font_size=22, color=GREY_B).next_to(chan, UP, buff=0.15)
        out = letter_row(sent, font_size=28, color=C.TRUE_P).move_to([4.6, 1.9, 0])
        a1 = Arrow(txt.get_bottom(), boxes[0].get_top(), buff=0.15, color=GREY_B, stroke_width=3)
        a2 = Arrow(boxes[0].get_right(), chan.get_left(), buff=0.1, color=GREY_B, stroke_width=3)
        a3 = Arrow(chan.get_right(), boxes[1].get_left(), buff=0.1, color=GREY_B, stroke_width=3)
        a4 = Arrow(boxes[1].get_top(), out.get_bottom(), buff=0.15, color=GREY_B, stroke_width=3)
        expl = label(r"``your 3rd guess'' \ $\to$ \ the twin makes its 3rd guess", font_size=24, color=GREY_A)
        expl.next_to(nums, DOWN, buff=1.2)
        res = mtex(r"H(\text{text}) \le H(\text{guess counts}) \le \sum_i q_i \log_2 \frac{1}{q_i}", font_size=38,
                   color=C.BITS).to_edge(DOWN, buff=0.85)
        qn = label(r"$q_i$: \ how often the right letter was the $i$-th guess", font_size=24, color=GREY_A)
        qn.next_to(res, DOWN, buff=0.2)
        with self.voiceover(
            "Here's Shannon's key observation. Suppose the receiver has an identical twin of the guesser: same "
            "knowledge, same habits. <bookmark mark='a'/> The sender runs the guessing game on the text, and sends "
            "only the guess counts. <bookmark mark='b'/> The receiver asks the twin for its guesses, and when the "
            "count says third guess, takes the twin's third guess. Out comes the text, exactly."
        ) as vo:
            self.play(FadeIn(head), FadeIn(txt), FadeIn(boxes[0]), FadeIn(boxes[1]), FadeIn(sender), FadeIn(receiver))
            vo.wait_until("a")
            self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(nums), Create(chan), FadeIn(chan_l))
            vo.wait_until("b")
            self.play(GrowArrow(a3), FadeIn(expl))
            self.play(GrowArrow(a4), FadeIn(out))
        with self.voiceover(
            "So the guess counts carry all the information in the text. <bookmark mark='a'/> The text's entropy can "
            "be no more than theirs, and that is at most the entropy of how often each guess number turns up. "
            "Count the guesses, and you have an upper bound on the information in English."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(res), FadeIn(qn))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def histogram(self):
        g = load("game")
        q = np.asarray(g["passage_ranks_q"])
        up, lo = float(g["upper"]), float(g["lower"])
        n = int(g["n"])
        assert abs(q[0] - 0.579) < 0.001 and abs(up - 2.37) < 0.005 and abs(lo - 1.36) < 0.005
        head = label(rf"Our counting guesser on the Falcon passage: \ ${n:,}$ letters".replace(",", "{,}"),
                     font_size=32).to_edge(UP, buff=0.4)
        sub = label(r"guesses in order of how often each letter followed the last six letters in the books",
                    font_size=22, color=GREY_B).next_to(head, DOWN, buff=0.15)
        K = 15
        x0, slot, y0, Hmax = -6.2, 0.46, -2.4, 4.2
        bars, labs, vals = VGroup(), VGroup(), VGroup()
        for i in range(K):
            h = Hmax * q[i] / q[0]
            b = Rectangle(width=slot * 0.75, height=max(h, 0.01), stroke_width=0, fill_color=C.GUESS, fill_opacity=0.9)
            b.move_to([x0 + (i + 0.5) * slot, y0 + h / 2, 0])
            bars.add(b)
            labs.add(MathTex(str(i + 1), font_size=20, color=GREY_B).next_to(b, DOWN, buff=0.1).set_y(y0 - 0.2))
            if i < 4:
                vals.add(MathTex(f"{q[i]:.3f}", font_size=20, color=C.GUESS).next_to(b, UP, buff=0.08))
        xlab = label(r"guess number $i$", font_size=22, color=GREY_A).move_to([x0 + K * slot / 2, y0 - 0.65, 0])
        rows = VGroup(
            mtex(r"\text{upper:}\ \ \sum_i q_i \log_2 \frac{1}{q_i} = " + f"{up:.2f}", font_size=32, color=C.BITS),
            mtex(r"\text{lower:}\ \ \sum_i i\,(q_i - q_{i+1}) \log_2 i = " + f"{lo:.2f}", font_size=32, color=C.CONTEXT),
            label(r"bits per letter: \ the information is somewhere between", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, 0.6, 0])
        own = label(rf"(its own probabilities, coded directly: ${load('orders')['best_bits']:.2f}$)", font_size=22,
                    color=GREY_B).next_to(rows, DOWN, buff=0.3).align_to(rows, LEFT)
        lsrc = note(r"lower bound: \ Shannon (1951), for an ideal guesser").next_to(own, DOWN, buff=0.2).align_to(rows, LEFT)
        tag = computed_tag()
        with self.voiceover(
            "Let's play the game with our counting model from the last chapter, as the guesser, on twelve thousand "
            "letters of the Falcon passage. <bookmark mark='a'/> It gets the letter on the first guess 58 percent of "
            "the time, on the second 13 percent, and the tail runs on from there."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1), FadeIn(labs), FadeIn(xlab),
                      run_time=2.0)
            self.play(FadeIn(vals))
        with self.voiceover(
            "From those frequencies, the upper bound is 2.37 bits per letter. <bookmark mark='a'/> Shannon also "
            "proved a lower bound from the same numbers: 1.36 bits. The true information content of the passage, "
            "for a guesser like this one, lies in between."
        ) as vo:
            self.play(Write(rows[0]))
            vo.wait_until("a")
            self.play(Write(rows[1]), FadeIn(rows[2]))
            self.play(FadeIn(own), FadeIn(lsrc))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def people(self):
        g = load("game")
        lo_h, hi_h = g["shannon_human"]
        ax_y = 0.0
        L, W = -5.8, 11.6
        scale = W / 5.0

        def X(b):
            return L + b * scale

        axis = NumberLine(x_range=[0, 5, 1], length=W, color=GREY_C, include_numbers=False).move_to([0, ax_y - 0.3, 0])
        nums = VGroup(*[MathTex(str(b), font_size=24, color=GREY_B).next_to(axis.n2p(b), DOWN, buff=0.15)
                        for b in range(6)])
        unit = label(r"bits per letter", font_size=22, color=GREY_B).next_to(axis, DOWN, buff=0.55)

        def band(a, b, y, col, text, h=0.5):
            r = Rectangle(width=(b - a) * scale, height=h, stroke_width=2, stroke_color=col, fill_color=col,
                          fill_opacity=0.35).move_to([X((a + b) / 2), y, 0])
            t = label(text, font_size=24, color=col).next_to(r, UP, buff=0.12)
            return VGroup(r, t)

        ours = band(float(g["lower"]), float(g["upper"]), 0.9, C.GUESS,
                    r"our counting guesser: \ $6$ letters of context")
        human = band(lo_h, hi_h, 2.0, C.HUMAN, r"Shannon's subjects: \ $100$ letters of context")
        uni = VGroup(DashedLine([X(math.log2(27)), -0.4, 0], [X(math.log2(27)), 2.5, 0], color=GREY_C),
                     label(r"$\log_2 27$", font_size=22, color=GREY_B).move_to([X(math.log2(27)), 2.75, 0]))
        head = label(r"People are much better guessers", font_size=36).to_edge(UP, buff=0.3)
        why_ = VGroup(
            label(r"they know words, grammar, idioms, what the story is about, how the world works", font_size=26),
            label(r"later estimates agree: \ about $1.3$ bits (Cover \& King, 1978, by betting on the next letter)",
                  font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.45)
        src = cite(r"C.~E.~Shannon (1951); \ T.~M.~Cover \& R.~C.~King, IEEE Trans.~Inf.~Theory (1978)", corner=UL)
        src.next_to(head, DOWN, buff=0.1)
        with self.voiceover(
            "Shannon's own subjects did far better. <bookmark mark='a'/> Given a hundred letters of context, his "
            "estimates put printed English between 0.6 and 1.3 bits per letter, <bookmark mark='b'/> against 1.4 to "
            "2.4 for our counting guesser with six. <bookmark mark='c'/> The difference is knowledge: people know "
            "words and grammar, they know idioms, they know what the story is about, and they know how the world "
            "works."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), Create(axis), FadeIn(nums), FadeIn(unit), FadeIn(uni))
            vo.wait_until("a")
            self.play(FadeIn(human))
            vo.wait_until("b")
            self.play(FadeIn(ours))
            vo.wait_until("c")
            self.play(FadeIn(why_[0]))
        with self.voiceover(
            "Later estimates landed in the same place: about 1.3 bits per letter, from a version of the game where "
            "people bet on the next letter instead of guessing it. <bookmark mark='a'/> To guess like a person, a "
            "machine has to know what a person knows. That's the bar."
        ) as vo:
            self.play(FadeIn(why_[1]))
            vo.wait_until("a")
            self.play(Indicate(human, color=C.HUMAN, scale_factor=1.05), run_time=1.5)
        self.wait(0.5)
        self.clear_scene()
