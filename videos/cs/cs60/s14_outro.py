from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs60.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES


def tile(content, caption, color, TW=3.6, TH=2.3):
    frame = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D,
                             stroke_width=1.5, fill_color=BG, fill_opacity=1)
    if content.width > TW:
        content.scale_to_fit_width(TW)
    if content.height > TH:
        content.scale_to_fit_height(TH)
    content.move_to(frame.get_center() + UP * 0.25)
    cap = label(caption, font_size=22, color=color).move_to(frame.get_bottom() + UP * 0.3)
    return Group(frame, content, cap)


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.practice()
        self.problems()
        self.next_time()
        self.references()

    def recap(self):
        head = label(rf"Part {PART}: \ Domain-Specific Hardware", font_size=34).to_edge(UP, buff=0.3)
        tiles = Group(
            tile(MathTex(r"\min(P, \ I \beta)", font_size=54, color=KERN), r"the roofline", KERN),
            tile(MathTex(r"s \leftarrow s + a \cdot b", font_size=50, color=HEAD), r"a systolic cell", HEAD),
            tile(MathTex(r"\tfrac{N}{3N - 2}", font_size=60, color=DATA), r"which number stays put", DATA),
            tile(label(r"8 bits, \ 32-bit sums", font_size=38, color=YES), r"the TPU's bargain", YES),
            tile(label(r"move less", font_size=44, color=NO), r"memory, \ sparsity, \ space", NO),
            tile(label(r"1 byte per cycle", font_size=40, color=LAM), r"the Job as a circuit", LAM),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        with self.voiceover(
            "What we built in this part. A roofline, measured on this machine, which says whether a kernel waits for "
            "arithmetic or for memory. A cell that multiplies and adds, from Part 4's gates, and a grid of them that "
            "multiplies matrices in a diagonal wave, verified gate by gate. Two dataflows, and the utilization each "
            "one earns. The TPU's bargain: eight-bit products and thirty-two-bit sums, for a sliver of the energy. "
            "GPUs, spatial machines, memory that computes, and sparsity, which are all ways to move fewer bytes. And "
            "the Job as a circuit, counting one byte every cycle. One idea runs through it: when the free speedups "
            "ended, speed came from fitting the machine to the work."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"measuring speed without fooling ourselves", [61]),
            (r"the open problems, \ gathered on one map", [61]),
            (r"the ledger's last row", [61]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. The roofline was measured once, on one machine, and Part 61, the last "
            "part, is about how to measure without fooling yourself. The open problems of this part join all the "
            "others on one map there. And the ledger, with its twenty-first row from this part's circuit, is read "
            "one last time."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"place", r"each kernel on the roofline before optimizing it"),
            (r"reuse", r"tile loops so data is used many times per fetch"),
            (r"quantize", r"inference to 8 bits, \ and check accuracy on real data"),
            (r"offload", r"to accelerators only what is dense, \ regular and large"),
            (r"profile", r"the data movement, \ not only the arithmetic"),
        ])
        with self.voiceover(
            "In practice. Put each kernel on the roofline before you optimize it, so you know which ceiling you are "
            "under. Tile loops so that each value fetched is used many times. Quantize inference to eight bits, and "
            "check the accuracy on real data, not on a benchmark. Send to an accelerator only work that is dense, "
            "regular and large enough to pay for the transfer. And profile the movement of data, not only the "
            "arithmetic."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Derive the arithmetic intensity of an $n \times n$ matrix product with $b \times b$ tiles in a fast "
            r"memory of $3b^2$ words, \ and the $b$ that reaches this machine's ridge.",
            r"Show that an output-stationary $N \times N$ grid needs $3N - 2$ cycles, \ and a weight-stationary one "
            r"$M + 2N - 2$ after loading.",
            r"An int8 product of length $K$ sums into 32 bits. \ How large can $K$ be before the sum can overflow?",
            r"Decoding one token reads every weight once. \ Find the batch size at which a chip with the roofline "
            r"of chapter twelve becomes compute-bound.",
            r"\textit{Build.} \ Add linear probing to the word-counting unit, \ and measure its gates, \ its clock "
            r"and the words it no longer loses.",
            r"$\bigstar$ \textit{Research.} \ The least data movement for a matrix product on a grid of small "
            r"memories, \ with a matching dataflow.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: give the word-counting unit linear probing, so that it stops losing words to collisions, and "
            "measure what that costs in gates and in clock speed. The last, marked with a star, is a research "
            "problem: Hong and Kung's pebble game, played on a grid of small memories."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 61, \ Doing Research", font_size=40).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"an environment variable that changes a program's speed", HEAD),
            (r"confidence intervals, \ and why geometric means", YES),
            (r"reading, \ reviewing, \ finding a problem", DATA),
            (r"the open problems, \ on one map", LAM))]).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "Next time, Part 61, the last part of the series: doing research. Every result the series quoted was "
            "made by someone. How do you measure without fooling yourself, when the size of an unused environment "
            "variable can change a program's speed? How do you read a paper, find a problem and know when it is "
            "solved? And where, on one map, are the open problems we met?"
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Hennessy and Patterson, \textit{Computer Architecture}, \ 6th ed., \ ch. 7",
             r"Sze, \ Chen, \ Yang and Emer, \textit{Efficient Processing of Deep Neural Networks}"],
            [r"Kung and Leiserson \ (1978); \ Kung \ (1982); \ Hong and Kung \ (1981)",
             r"Williams, \ Waterman and Patterson \ (2009, \ roofline); \ Horowitz \ (2014)",
             r"Jouppi et al. \ (2017, \ TPU); \ Hameed et al. \ (2010); \ Hennessy and Patterson \ (2019)",
             r"Dao et al. \ (2022, \ FlashAttention)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(2.0)


_ = (NO, YES, KERN, LAM, DATA)
