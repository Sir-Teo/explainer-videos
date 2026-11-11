from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs28.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, bit_row, fit_right, load, mono,
                                   qr_grid)


class Hook(VoiceoverScene):
    def construct(self):
        self.weekend()
        self.scratched()
        self.plan()

    def weekend(self):
        head = label(r"Bell Labs, \ 1947", font_size=36).to_edge(UP, buff=0.35)
        bits = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1]
        row = bit_row(bits, size=0.5, font=24).next_to(head, DOWN, buff=0.9)
        bad = 6
        flip = bit_row([b ^ (i == bad) for i, b in enumerate(bits)], size=0.5, font=24).move_to(row)
        flip.boxes[bad].set_stroke(NO, width=4)
        flip.digits[bad].set_color(NO)
        lines = VGroup(
            label(r"Richard Hamming ran jobs on a relay computer \ (the Bell Labs Model V) \ over weekends", font_size=24,
                  color=WHITE),
            label(r"its two-out-of-five checks \textbf{detected} a bad digit; \ the machine dropped the job and moved on",
                  font_size=24, color=NO),
            label(r"``Damn it, \ if the machine can detect an error, \ why can't it locate the position of the error "
                  r"and correct it?''", font_size=24, color=HEAD),
            label(r"his answer \ (1950) \ began the theory of error-correcting codes; \ Shannon's \ (1948) \ said how "
                  r"far it could go", font_size=24, color=YES),
        ).arrange(DOWN, buff=0.35).next_to(row, DOWN, buff=0.8)
        with self.voiceover(
            "In 1947 Richard Hamming was running calculations on a relay computer at Bell Labs. During the week, "
            "operators restarted jobs that failed; at weekends nobody was there. <bookmark mark='a'/> The machine "
            "stored each digit in a two-out-of-five code, so it could detect a bad bit. When a check fired, it dropped the job and moved on to the next, "
            "and on Monday Hamming found his work gone. <bookmark mark='b'/> As he told the story later: if the "
            "machine can detect an error, why can't it locate the position of the error and correct it? <bookmark "
            "mark='c'/> His answer, published in 1950, started the theory of error-correcting codes. Two years "
            "earlier Claude Shannon had proved how far such codes could go. Closing the gap between the two took "
            "fifty years, and this part follows it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(row), FadeIn(lines[0]))
            vo.wait_until("a")
            self.play(ReplacementTransform(row, flip), FadeIn(lines[1]))
            vo.wait_until("b")
            self.play(FadeIn(lines[2]))
            vo.wait_until("c")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def scratched(self):
        q = load("qr")
        head = label(r"A scratched message", font_size=36).to_edge(UP, buff=0.3)
        g = qr_grid(q["matrix"], side=4.8).to_edge(LEFT, buff=1.0).shift(DOWN * 0.3)
        blot = next(s for s in q["scratches"] if s["name"] == "scratch")
        x0, y0, x1, y1 = blot["rect"]
        paint = VGroup(*[g.cells[y][x].copy().set_fill("#e8e8e8", 1).set_stroke("#e8e8e8", width=1.2) for y in range(y0, y1 + 1)
                         for x in range(x0, x1 + 1)])
        lines = VGroup(
            label(r"a QR code \ (version 2, \ 25 $\times$ 25 modules): \\ 22 bytes of message, \ 22 of checks",
                  font_size=23, color=WHITE),
            label(rf"paint over {blot['modules']} modules: \\ {len(blot['wrong'])} of the 44 bytes are now wrong",
                  font_size=23, color=NO),
            label(rf"decoded: \ \texttt{{{q['text']}}}", font_size=26, color=YES),
            label(r"by the end of this part \\ we will have built every step", font_size=23, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(g, RIGHT, buff=0.9)
        fit_right(lines)
        with self.voiceover(
            "Here is a code you use every day. <bookmark mark='a'/> This QR code has twenty-five by twenty-five "
            "squares, and holds forty-four bytes: twenty-two of message and twenty-two of checks. You can scan it. "
            "<bookmark mark='b'/> Now paint over a piece of it, near the middle. Eight of the forty-four bytes are "
            "now wrong, and the decoder is not told which. "
            "<bookmark mark='c'/> And still it reads: CS, Built, Part 28. <bookmark mark='d'/> By the end of this "
            "part we will have built every step: the finite field, the Reed-Solomon code, and the decoder that found "
            "the message."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in paint], lag_ratio=0.01), FadeIn(lines[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(lines[2], scale=1.1))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Error-Correcting Codes", font_size=46).to_edge(UP, buff=0.4)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"the noisy channel, \ repetition, \ Hamming distance and Hamming(7,4)",
            r"how good a code can be: \ the bounds, \ and the perfect Golay code",
            r"finite fields, \ Reed--Solomon codes, \ and our QR code, \ scratched and read",
            r"CRCs: \ the shift registers of Part 5, \ dividing polynomials",
            r"Shannon's theorem, \ and the codes that reach it: \ Viterbi, \ LDPC, \ polar",
            r"codes for storage; \ the frontier: \ capacity, \ list decoding, \ locality",
        ], font_size=26).move_to(DOWN * 0.2)
        with self.voiceover(
            "Part 28 of Computer Science, Built: Error-Correcting Codes. <bookmark mark='a'/> In this part: the noisy "
            "channel and the simplest codes; Hamming distance and Hamming's code; the limits on how good any code can "
            "be, and a perfect code; finite fields, Reed-Solomon codes, and our QR code; cyclic redundancy checks, "
            "built from Part 5's shift registers; Shannon's theorem and the codes that finally reach it; codes for "
            "storage; and the frontier."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()
