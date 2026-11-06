from __future__ import annotations

from explainer.cs import *  # noqa: F403
from explainer.cs.algo.codes import capacity_bsc, polar_bhattacharyya
from videos.cs.cs28.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, grid_table, load)


class Polar(VoiceoverScene):
    def construct(self):
        self.card()
        self.butterfly()
        self.fan()
        self.decoding()

    def card(self):
        card = chapter_card(12, r"Polar codes", r"Can a channel be split into perfect ones and useless ones?",
                            lit=(2009, 2016), extra=((2009, r"Ar\i kan"), (2016, r"5G control channels")), part=PART)
        with self.voiceover("Chapter twelve. Polar codes."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def butterfly(self):
        head = label(r"The polar transform, \ $N = 8$", font_size=34).to_edge(UP, buff=0.3)
        N = 8
        x0, dx, y0, dy = -4.6, 1.4, 2.0, -0.55
        zs = polar_bhattacharyya(3, 0.5)
        info = set(sorted(range(N), key=lambda i: zs[i])[:4])
        ulab = VGroup(*[label(rf"$u_{i}$", font_size=20, color=YES if i in info else GREY_B).move_to(
            [x0 - 0.5, y0 + dy * i, 0]) for i in range(N)])
        xlab = VGroup(*[label(rf"$x_{i}$", font_size=20, color=DATA).move_to([x0 + 3 * dx + 0.5, y0 + dy * i, 0])
                        for i in range(N)])
        wires = VGroup(*[Line([x0, y0 + dy * i, 0], [x0 + 3 * dx, y0 + dy * i, 0], color=GREY_D, stroke_width=2)
                         for i in range(N)])
        xors = VGroup()
        # stage s pairs (i, i + h) within blocks of size 2h: x_i <- x_i xor x_{i+h}
        for st, h in enumerate((4, 2, 1)):
            x = x0 + dx * (st + 0.5)
            for blk in range(0, N, 2 * h):
                for i in range(blk, blk + h):
                    top, bot = [x, y0 + dy * i, 0], [x, y0 + dy * (i + h), 0]
                    xors.add(VGroup(Line(bot, top, color=HEAD, stroke_width=2),
                                    Circle(radius=0.11, color=HEAD, stroke_width=2).set_fill(BG, 1).move_to(top),
                                    Dot(bot, radius=0.05, color=HEAD)))
        zl = VGroup(*[label(f"{zs[i]:.3f}", font_size=15, color=YES if i in info else NO).next_to(ulab[i], LEFT,
                                                                                                   buff=0.2)
                      for i in range(N)])
        zh = label(r"erasure prob.", font_size=15, color=GREY_A).next_to(zl, UP, buff=0.15)
        notes = VGroup(
            label(r"three stages of ``XOR the lower wire into the upper'': \\ $x = u \, F^{\otimes 3}$, \ "
                  r"$F = \begin{pmatrix} 1 & 0 \\ 1 & 1 \end{pmatrix}$", font_size=20, color=WHITE),
            label(r"each $u_i$, \ decoded in order, \ sees its own synthetic channel", font_size=20, color=GREY_A),
            label(r"for an erasure channel with $\epsilon = \tfrac12$, \ their erasure probabilities \\ spread "
                  r"from 0.004 to 0.996", font_size=20, color=HEAD),
            label(r"put the 4 data bits on the best channels \ (green); \\ \textbf{freeze} the rest to 0",
                  font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(head, DOWN, buff=0.6)
        notes.next_to(xlab, RIGHT, buff=0.5).align_to(notes, UP)
        fit_right(notes)
        with self.voiceover(
            "Here is Arıkan's construction for eight bits. <bookmark mark='a'/> Three stages of the same step: "
            "exclusive-or the lower wire into the upper one, first across halves, then quarters, then neighbours. "
            "<bookmark mark='b'/> Decoding takes the inputs in order, each using the ones before it, so each input "
            "sees a channel of its own. <bookmark mark='c'/> Start from an erasure channel that loses half its bits, "
            "and those eight channels already differ wildly: the first is almost always erased, the last almost "
            "never. <bookmark mark='d'/> So put the data on the four best channels and freeze the other four to "
            "zero, known to both sides."
        ) as vo:
            self.play(FadeIn(head), Create(wires), FadeIn(ulab), FadeIn(xlab))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x_) for x_ in xors], lag_ratio=0.08), FadeIn(notes[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(zl), FadeIn(zh), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]), *[ulab[i].animate.scale(1.2) for i in info])
        self.wait(0.3)
        self.clear_scene()

    def fan(self):
        d = load("polar")
        head = label(r"Channel polarization", font_size=34).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 6.5, 1], y_range=[0, 1.02, 0.25], x_length=6.2, y_length=4.4,
                  axis_config={"color": GREY_D, "include_numbers": False}).next_to(head, DOWN, buff=0.5).to_edge(
            LEFT, buff=1.0)
        xt = VGroup(*[label(str(2 ** n), font_size=15, color=GREY_A).next_to(ax.c2p(n, 0), DOWN, buff=0.08)
                      for n in range(7)])
        yt = VGroup(*[label(f"{y:g}", font_size=15, color=GREY_A).next_to(ax.c2p(0, y), LEFT, buff=0.08)
                      for y in (0.25, 0.5, 0.75, 1.0)])
        xl = label(r"number of channels combined, \ $N$", font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.35)
        yl = label(r"erasure probability of each", font_size=17, color=GREY_A).rotate(PI / 2).next_to(ax, LEFT,
                                                                                                        buff=0.45)
        layers = VGroup()
        for n, zs in enumerate(d["fan"]):
            layers.add(VGroup(*[Dot(ax.c2p(n, z), radius=0.045 if n < 5 else 0.03,
                                    color=interpolate_color(ManimColor(YES), ManimColor(NO), z)) for z in zs]))
        lv = {lv_["n"]: lv_ for lv_ in d["levels"]}
        tab = grid_table([r"$N$", r"nearly perfect", r"nearly useless"],
                         [[str(2 ** n), f"{lv[n]['good'] * 100:.1f}\\%", f"{lv[n]['bad'] * 100:.1f}\\%"]
                          for n in (4, 6, 8, 10)], widths=[1.4, 2.4, 2.4], row_h=0.4, font_size=18, mono_cols=(),
                         colors=[[WHITE, YES, NO]] * 4)
        notes = VGroup(
            label(r"start: \ copies of an erasure channel, \ $\epsilon = \tfrac12$", font_size=20, color=WHITE),
            label(r"combine two: \ send $u_1 \oplus u_2$ and $u_2$; \\ decode $u_1$ first: \ a \textbf{worse} channel, "
                  r"$2\epsilon - \epsilon^2$; \\ then $u_2$, \ knowing $u_1$: \ a \textbf{better} one, \ $\epsilon^2$",
                  font_size=20, color=HEAD),
            label(r"repeat $\log_2 N$ times: \ the channels \textbf{polarize}", font_size=20, color=YES),
            tab,
            label(r"the average is conserved: \ the fraction that becomes \\ perfect tends to the capacity, \ "
                  r"$\tfrac12$", font_size=20, color=DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(ax, RIGHT, buff=0.6).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "In 2009 Erdal Arıkan found a code that provably reaches capacity, with a decoder as cheap as sorting. "
            "<bookmark mark='a'/> Start with a channel that erases each bit half the time. <bookmark mark='b'/> Take "
            "two uses of it and send u one exclusive-or u two, and u two. Decode u one first: it needs both outputs, "
            "so it sees a worse channel, erased with probability two epsilon minus epsilon squared. Then decode u "
            "two, already knowing u one: it gets two chances, so it sees a better channel, epsilon squared. "
            "<bookmark mark='c'/> Do it again and again. With each doubling the channels spread apart: here are the "
            "erasure probabilities of all of them, up to sixty-four. <bookmark mark='d'/> At a thousand and "
            "twenty-four channels, a third are already nearly perfect and a third nearly useless, and the middle "
            "keeps shrinking. <bookmark mark='e'/> The total capacity never changes, so the fraction that becomes "
            "perfect tends to exactly the capacity. Send data on the good ones, and freeze the bad ones to zero."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(layers[0]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(layers[1]), FadeIn(notes[1]))
            vo.wait_until("c")
            for layer in layers[2:]:
                self.play(FadeIn(layer), run_time=0.7)
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
            vo.wait_until("e")
            self.play(FadeIn(notes[4]))
        self.wait(0.3)
        self.clear_scene()

    def decoding(self):
        d = load("polar")
        head = label(r"Successive cancellation, \ measured", font_size=34).to_edge(UP, buff=0.35)
        rows = [[f"{r['p']:g}", f"{capacity_bsc(r['p']):.2f}", f"{r['256'] * 100:.1f}\\%", f"{r['1024'] * 100:.1f}\\%"]
                for r in d["rows"]]
        tab = grid_table([r"flip probability $p$", r"capacity", r"$N$ = 256", r"$N$ = 1{,}024"], rows,
                         widths=[3.0, 2.0, 2.4, 2.4], row_h=0.45, font_size=21, mono_cols=(),
                         colors=[[WHITE, GREY_A, DATA, YES]] * len(rows))
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        tl = label(r"rate $\tfrac12$ on the BSC; \ fraction of blocks decoded wrongly", font_size=18,
                   color=GREY_A).next_to(tab, DOWN, buff=0.12)
        lines = VGroup(
            label(r"decode bit by bit, \ each using the decisions before it: \ $O(N \log N)$", font_size=22,
                  color=WHITE),
            label(r"well below capacity, \ the longer code is better; \ near capacity, \ both fail", font_size=22,
                  color=YES),
            label(r"at short lengths plain SC is weak: \ practice keeps a \textbf{list} of 8 candidates and a CRC "
                  r"\ (Tal and Vardy, 2015)", font_size=22, color=HEAD),
            label(r"5G \ (2016 decision): \ polar codes for control channels, \ LDPC for data", font_size=22,
                  color=DATA),
        ).arrange(DOWN, buff=0.25).next_to(tl, DOWN, buff=0.4)
        with self.voiceover(
            "Decoding follows the construction. <bookmark mark='a'/> Decode the bits one at a time, each using the "
            "decisions already made, in time N log N. <bookmark mark='b'/> We sent rate-one-half polar codes over "
            "the binary symmetric channel. Well below capacity, the longer code makes fewer mistakes; as the channel "
            "approaches capacity, both collapse. <bookmark mark='c'/> At practical lengths, plain successive "
            "cancellation is not the best decoder. Ido Tal and Alexander Vardy keep a short list of candidate paths "
            "and use a CRC, chapter eight's, to pick the right one. <bookmark mark='d'/> In 2016 the standards body "
            "for 5G chose polar codes for the control channels and LDPC codes for data: ten years from Arıkan's "
            "paper to billions of phones."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab), FadeIn(tl))
            for mk, ln in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
