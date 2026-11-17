from __future__ import annotations

from videos.psychology.psych58.common import *  # noqa: F403


class Normalize(VoiceoverScene):
    def construct(self):
        card_section(self, 6, r"Normalization", r"Is there a canonical computation?", scale=("brain",))
        self.equation()
        self.everywhere()

    def equation(self):
        d = load("norm")
        head = heading(r"One equation")
        eq = MathTex(r"R = \frac{c^n}{\sigma^n + c^n + m^n}", font_size=40).move_to([-3.3, 2.1, 0])
        A = axes([-2, 0], [0, 1.0], x_length=5.2, y_length=2.8, xticks=[-2, -1, 0], yticks=[0, 0.5, 1.0],
                 xfmt=lambda v: rf"10^{{{int(v)}}}", yfmt=lambda v: f"{v:g}", xlabel=r"contrast",
                 ylabel=r"response", center=[-3.3, -0.6, 0], font_size=12)
        x = np.log10(np.asarray(d["c"]))
        cs = [curve(A.ax, x, d[k], c, stroke_width=4) for k, c in (("none", PERSON), ("mask_low", MODEL),
                                                                   ("mask_high", AUTH))]
        key = VGroup(label(r"alone", font_size=13, color=PERSON), label(r"weak mask", font_size=13, color=MODEL),
                     label(r"strong mask", font_size=13, color=AUTH)).arrange(RIGHT, buff=0.35)
        key.next_to(A, DOWN, buff=0.45)
        rows = rows_of([
            (r"a neuron's drive $c^n$, \ divided by the summed activity of a pool of neighbours (here $m$) plus a "
             r"constant", WHITE),
            (r"its response saturates at high contrast, \ and a mask that drives the pool but not the cell "
             r"suppresses it", MODEL),
            (r"the curve shifts sideways: \ a change of gain, \ not of shape", PERSON),
            (r"Heeger, \ 1992; \ Carandini and Heeger, \ 2012: \ a canonical neural computation", GOOD),
        ], 5.6, 19, 0.36).move_to([3.6, -0.1, 0])
        tag = psyche_tag(r"\texttt{efficient.normalization}")
        tag2 = published_tag(r"Carandini \& Heeger (2012)").to_corner(DL, buff=0.3)
        with self.voiceover(
            "Is there a canonical computation? Here's a candidate: one equation. <bookmark mark='a'/> A neuron's "
            "drive, divided by the summed activity of a pool of neighbours plus a constant. <bookmark mark='b'/> Its "
            "response saturates at high contrast, and a mask that drives the pool but not the cell suppresses it. "
            "<bookmark mark='c'/> On a log axis, the curve shifts sideways: a change of gain, not of shape. "
            "<bookmark mark='d'/> David Heeger proposed it for visual cortex in 1992, and in 2012 Matteo Carandini "
            "and Heeger argued it's a canonical neural computation."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tag2), FadeIn(eq), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(cs[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(cs[1]), Create(cs[2]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def everywhere(self):
        chips_section(self, r"The same equation, \ everywhere", [
            (r"retina", r"light adaptation: \ responses divided by the mean light level", SYMP),
            (r"visual cortex", r"contrast saturation and cross-orientation suppression", MODEL),
            (r"attention", r"Reynolds and Heeger, \ 2009: \ attention multiplies the drive before normalization, \ "
                           r"reproducing many of Part 18's findings", PERSON),
            (r"value", r"the value of an option divided by the others on offer (Part 26)", AUTH),
            (r"why efficient", r"dividing out shared activity removes redundancy between neighbours: \ Barlow's "
                               r"principle again (Schwartz and Simoncelli, \ 2001)", GOOD),
        ], "The same equation appears everywhere. <bookmark mark='a'/> In the retina, light adaptation divides "
           "responses by the mean light level. <bookmark mark='b'/> In visual cortex, it gives contrast saturation "
           "and cross-orientation suppression. <bookmark mark='c'/> In attention: John Reynolds and David Heeger's "
           "2009 model has attention multiply the drive before normalization, and it reproduces many of Part 18's "
           "findings. <bookmark mark='d'/> In value: the value of an option divided by the others on offer, from "
           "Part 26. <bookmark mark='e'/> And why it's efficient: dividing out shared activity removes redundancy "
           "between neighbours. That's Barlow's principle again, as Odelia Schwartz and Eero Simoncelli showed in "
           "2001.")
