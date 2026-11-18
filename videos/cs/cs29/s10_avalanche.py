from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs29.common import (BG, DATA, HEAD, NO, PART, YES, load)


def bit_map(m, s=0.135, on=NO):
    """128 bits as 16 byte-columns of 8 bits: lit where the two encryptions differ."""
    g = VGroup()
    for j, byte in enumerate(m):
        for b, v in enumerate(byte):
            g.add(Square(side_length=s, stroke_color=GREY_D, stroke_width=0.6, fill_color=on if v else BG,
                         fill_opacity=1).move_to([j * s, -b * s, 0]))
    return g.center()


class Avalanche(WatchScene):
    def construct(self):
        self.card()
        self.heat()
        self.margin()

    def card(self):
        self.chapter(9, r"The avalanche", r"How fast does one bit spread?", lit=(1973, 1985), extra=((1973, r"Feistel: \ the avalanche"), (1985, r"Webster--Tavares")), part=PART, said="Chapter nine. The avalanche.")

    def heat(self):
        self.ask(r"Flip one plaintext bit. \\ After how many rounds does every byte differ?", [r"$1$", r"$2$",
                 r"$10$"], 1,
                 say="Flip one bit of the plaintext. After how many rounds does every byte of the state differ?",
                 reveal="Two rounds.")
        a = load("avalanche")
        head = label(r"Flip one bit of the plaintext", font_size=34).to_edge(UP, buff=0.3)
        maps = VGroup(*[bit_map(m) for m in a["maps"]]).arrange(RIGHT, buff=0.3).next_to(head, DOWN, buff=1.0)
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
