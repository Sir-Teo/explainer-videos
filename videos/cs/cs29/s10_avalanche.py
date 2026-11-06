from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs29.common import (BG, DATA, HEAD, NO, PART, YES, load)


def bit_map(m, s=0.16, on=NO):
    """128 bits as 16 byte-columns of 8 bits: lit where the two encryptions differ."""
    g = VGroup()
    for j, byte in enumerate(m):
        for b, v in enumerate(byte):
            g.add(Square(side_length=s, stroke_color=GREY_D, stroke_width=0.6, fill_color=on if v else BG,
                         fill_opacity=1).move_to([j * s, -b * s, 0]))
    return g.center()


class Avalanche(VoiceoverScene):
    def construct(self):
        self.card()
        self.heat()
        self.stats()
        self.margin()

    def card(self):
        card = chapter_card(9, r"The avalanche", r"How fast does one bit spread?", lit=(1973, 1985),
                            extra=((1973, r"Feistel: \ the avalanche"), (1985, r"Webster--Tavares")), part=PART)
        with self.voiceover("Chapter nine. The avalanche."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def heat(self):
        a = load("avalanche")
        head = label(r"Flip one bit of the plaintext", font_size=34).to_edge(UP, buff=0.3)
        maps = VGroup(*[bit_map(m) for m in a["maps"]]).arrange(RIGHT, buff=0.35).next_to(head, DOWN, buff=1.0)
        counts = [sum(map(sum, m)) for m in a["maps"]]
        tops = VGroup(*[label(t, font_size=19, color=GREY_A).next_to(m, UP, buff=0.18) for m, t in
                        zip(maps, [r"start", r"round 1", r"round 2", r"round 3", r"round 4"])])
        bots = VGroup(*[label(rf"{c} of 128 differ", font_size=18, color=NO if c > 1 else WHITE).next_to(m, DOWN,
                                                                                                        buff=0.18)
                        for m, c in zip(maps, counts)])
        lines = VGroup(
            label(r"two plaintexts differing in one bit, \ one key; \ lit: \ state bits that differ", font_size=22,
                  color=WHITE),
            label(r"round 1: \ the S-box changes several bits of its byte, \ MixColumns spreads them over a column: "
                  r"\ 4 bytes", font_size=22, color=DATA),
            label(r"round 2: \ ShiftRows sends them to all four columns: \ all 16 bytes", font_size=22, color=HEAD),
            label(r"from then on, \ about half the bits differ, \ in no pattern: \ the \textbf{avalanche}",
                  font_size=22, color=YES),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "How quickly does AES forget where a change came from? <bookmark mark='a'/> Encrypt two plaintexts that "
            "differ in a single bit, under the same key, and after each round light up the state bits that differ. "
            "At the start, one bit. <bookmark mark='b'/> After round one, the S-box has turned that one bit into "
            "several bits of its byte, and MixColumns has spread them over the whole column: four bytes, seventeen "
            "bits. <bookmark mark='c'/> In round two, ShiftRows sends those four bytes to four different columns, "
            "and MixColumns spreads each again: all sixteen bytes. <bookmark mark='d'/> After that, about half the "
            "bits differ, and in no visible pattern. Horst Feistel called this the avalanche: a small change in the "
            "input should change the output completely."
        ) as vo:
            self.play(FadeIn(head), FadeIn(maps[0]), FadeIn(tops[0]), FadeIn(bots[0]))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(maps[1]), FadeIn(tops[1]), FadeIn(bots[1]), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(maps[2]), FadeIn(tops[2]), FadeIn(bots[2]), FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(maps[3:]), FadeIn(tops[3:]), FadeIn(bots[3:]), FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def stats(self):
        a = load("avalanche")
        head = label(rf"{a['trials']} random flips, \ measured", font_size=34).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 80, 16], x_length=5.0, y_length=3.4,
                  axis_config={"color": GREY_D, "include_numbers": False}).next_to(head, DOWN, buff=0.7).to_edge(
            LEFT, buff=0.9)
        pts = [ax.c2p(r, m) for r, m in enumerate(a["mean"])]
        line = VMobject(color=NO, stroke_width=3).set_points_as_corners(pts)
        dts = VGroup(*[Dot(p, radius=0.05, color=NO) for p in pts])
        half = DashedLine(ax.c2p(0, 64), ax.c2p(10, 64), color=YES, stroke_width=1.5)
        hl = label(r"64 = half", font_size=16, color=YES).next_to(ax.c2p(10, 64), UP, buff=0.08).shift(LEFT * 0.4)
        xt = VGroup(*[label(str(r), font_size=15, color=GREY_A).next_to(ax.c2p(r, 0), DOWN, buff=0.08)
                      for r in range(0, 11, 2)])
        yt = VGroup(*[label(str(y), font_size=15, color=GREY_A).next_to(ax.c2p(0, y), LEFT, buff=0.08)
                      for y in (0, 32, 64)])
        xl = label(r"round", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yl = label(r"mean bits that differ", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        hist = {int(k): v for k, v in a["hist"].items()}
        bx = Axes(x_range=[40, 88, 8], y_range=[0, 40, 8], x_length=5.0, y_length=3.4,
                  axis_config={"color": GREY_D, "include_numbers": False}).next_to(ax, RIGHT, buff=1.2)
        bars = VGroup()
        for k in range(40, 89):
            v = hist.get(k, 0)
            if v:
                base, top = bx.c2p(k, 0), bx.c2p(k, v)
                bars.add(Rectangle(width=0.085, height=top[1] - base[1], stroke_width=0, fill_color=DATA,
                                   fill_opacity=0.9).move_to(base, aligned_edge=DOWN))
        T = a["trials"]
        binom = VMobject(color=YES, stroke_width=2.5).set_points_smoothly(
            [bx.c2p(k, T * math.comb(128, k) / 2 ** 128) for k in range(40, 89)])
        bxt = VGroup(*[label(str(k), font_size=15, color=GREY_A).next_to(bx.c2p(k, 0), DOWN, buff=0.08)
                       for k in (40, 56, 64, 72, 88)])
        bxl = label(r"bits that differ after round 10", font_size=17, color=GREY_A).next_to(bxt, DOWN, buff=0.1)
        bl = label(r"Binomial$(128, \tfrac12)$", font_size=17, color=YES).next_to(bx, UP, buff=0.1).align_to(bx, RIGHT)
        lines = VGroup(
            label(r"full diffusion after 2 rounds; \ then flat at half", font_size=21, color=NO),
            label(rf"a random permutation would give Binomial$(128, \tfrac12)$: \ mean 64, \ s.d.\ 5.66; \ we "
                  rf"measure {a['final_mean']:.1f} and {a['final_sd']:.2f}", font_size=21, color=YES),
            label(r"the \textbf{strict avalanche criterion} \ (Webster and Tavares, 1985): \ each output bit flips "
                  r"with probability $\tfrac12$", font_size=21, color=WHITE),
        ).arrange(DOWN, buff=0.17).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "One example could be luck, so we flipped a random bit of a random plaintext four hundred times. "
            "<bookmark mark='a'/> On average one bit differs at the start, sixteen after round one, and from round "
            "two on, sixty-four: half of the hundred and twenty-eight. <bookmark mark='b'/> After all ten rounds, "
            "here is how many bits differed, trial by trial. A random permutation would give a binomial "
            "distribution, centred on sixty-four with a standard deviation of five point six six. We measure sixty-three "
            "point six and five point four five: as random as four hundred samples can show. <bookmark mark='c'/> "
            "Stafford Tavares and Robert Webster called this the strict avalanche criterion: every output bit should "
            "flip with probability one half whenever any single input bit flips."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(dts), Create(half), FadeIn(hl), FadeIn(lines[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(bx), FadeIn(bxt), FadeIn(bxl), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars],
                                                                       lag_ratio=0.03), run_time=2.0)
            self.play(Create(binom), FadeIn(bl), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def margin(self):
        head = label(r"Why ten rounds?", font_size=34).to_edge(UP, buff=0.3)
        w = 1.0
        boxes = VGroup()
        for r in range(1, 11):
            col = NO if r <= 7 else YES
            sq = Square(side_length=w * 0.86, stroke_color=col, stroke_width=2, fill_color=col,
                        fill_opacity=0.35 if r <= 7 else 0.15)
            boxes.add(VGroup(sq, label(str(r), font_size=24, color=WHITE).move_to(sq)))
        boxes.arrange(RIGHT, buff=0.14).next_to(head, DOWN, buff=1.0)
        b1 = Brace(boxes[:7], DOWN, color=NO)
        t1 = label(r"attacked faster than brute force \\ (impossible differentials, \ meet-in-the-middle)",
                   font_size=19, color=NO).next_to(b1, DOWN, buff=0.15)
        b2 = Brace(boxes[7:], DOWN, color=YES)
        t2 = label(r"the security \\ margin", font_size=19, color=YES).next_to(b2, DOWN, buff=0.15)
        lines = VGroup(
            label(r"the best attacks on AES-128 reach \textbf{7} of its 10 rounds, \ with enormous data and time",
                  font_size=21, color=WHITE),
            label(r"full AES-128: \ the biclique attack \ (2011) \ needs $2^{126.1}$ operations: \ four times faster "
                  r"than brute force, \ and useless", font_size=21, color=HEAD),
            label(r"designers choose rounds by the best attack plus a margin: \ speed is bought by deleting rounds",
                  font_size=21, color=GREY_A),
            label(r"no proof AES is a PRP exists: \ only 25 years of the world trying", font_size=21, color=NO),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "If two rounds already diffuse everything, why ten? Because diffusion is not security. <bookmark "
            "mark='a'/> The best attacks on AES-128 with fewer rounds, using impossible differentials and "
            "meet-in-the-middle ideas, reach seven rounds, needing vast amounts of data and time. The last three "
            "rounds are a margin. <bookmark mark='b'/> On the full cipher, the best known key recovery, the biclique "
            "attack of 2011, needs two to the one hundred and twenty-six point one operations: four times faster than "
            "trying every key, and still impossible. <bookmark mark='c'/> Designers set the number of rounds from "
            "the best attack they know, plus a margin. Faster designs are mostly older designs with rounds removed. "
            "<bookmark mark='d'/> And there is no proof that AES is a pseudorandom permutation. Its security rests on "
            "twenty-five years of the world's cryptanalysts failing, which is how block ciphers have always earned "
            "trust."
        ) as vo:
            self.play(FadeIn(head), FadeIn(boxes))
            vo.wait_until("a")
            self.play(FadeIn(b1), FadeIn(t1), FadeIn(b2), FadeIn(t2), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()
