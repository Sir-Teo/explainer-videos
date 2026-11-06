from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs28.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, grid_table, load, mono, sci)


class Channel(VoiceoverScene):
    def construct(self):
        self.card()
        self.bsc()
        self.repetition()
        self.picture()

    def card(self):
        card = chapter_card(1, r"Noise and repetition", r"How do you send bits through a noisy wire?",
                            lit=(1948, 1950), extra=((1948, r"Shannon"), (1950, r"Hamming")), part=PART)
        with self.voiceover("Chapter one. Noise and repetition."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def bsc(self):
        head = label(r"The binary symmetric channel", font_size=34).to_edge(UP, buff=0.35)
        l0 = Dot([-4.5, 1.2, 0], radius=0.12, color=DATA)
        l1 = Dot([-4.5, -1.2, 0], radius=0.12, color=DATA)
        r0 = Dot([-0.8, 1.2, 0], radius=0.12, color=HEAD)
        r1 = Dot([-0.8, -1.2, 0], radius=0.12, color=HEAD)
        labs = VGroup(mono("0", 26).next_to(l0, LEFT), mono("1", 26).next_to(l1, LEFT),
                      mono("0", 26).next_to(r0, RIGHT), mono("1", 26).next_to(r1, RIGHT))
        keep = VGroup(Arrow(l0, r0, buff=0.15, color=YES), Arrow(l1, r1, buff=0.15, color=YES))
        cross = VGroup(Arrow(l0, r1, buff=0.15, color=NO), Arrow(l1, r0, buff=0.15, color=NO))
        kl = VGroup(label(r"$1 - p$", font_size=22, color=YES).next_to(keep[0], UP, buff=0.08),
                    label(r"$1 - p$", font_size=22, color=YES).next_to(keep[1], DOWN, buff=0.08))
        cl = label(r"$p$", font_size=24, color=NO).move_to([-2.65, 0.45, 0])
        sl = label(r"sent", font_size=20, color=GREY_A).next_to(l0, UP, buff=0.5)
        rl = label(r"received", font_size=20, color=GREY_A).next_to(r0, UP, buff=0.5)
        lines = VGroup(
            label(r"each bit flips independently with probability $p$", font_size=22, color=WHITE),
            label(r"a crude but useful model: \\ memory cells, \ disks, \ radio, \ cosmic rays \ (Part 5)", font_size=22,
                  color=GREY_A),
            label(r"other channels: \ \textbf{erasures} \ (a bit is lost, \ and you know it), \\ "
                  r"bursts, \ and analogue noise", font_size=22, color=DATA),
            label(r"a \textbf{code} adds redundancy so the receiver \\ can undo the damage", font_size=22, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(VGroup(r0, r1), RIGHT, buff=1.2)
        fit_right(lines)
        with self.voiceover(
            "Shannon's simplest model of noise is the binary symmetric channel. <bookmark mark='a'/> Each bit goes "
            "through unchanged with probability one minus p and flips with probability p, independently of every "
            "other bit. <bookmark mark='b'/> It is crude, but memory cells hit by cosmic rays, scratched disks and "
            "faint radio all behave like it to a first approximation. <bookmark mark='c'/> There are other "
            "channels: in an erasure channel a bit is lost but you know which one, and real noise often comes in "
            "bursts. <bookmark mark='d'/> Against all of them the tool is the same: add redundancy, so that the "
            "receiver can undo the damage."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(l0, l1, r0, r1, labs, sl, rl)))
            vo.wait_until("a")
            self.play(GrowArrow(keep[0]), GrowArrow(keep[1]), FadeIn(kl))
            self.play(GrowArrow(cross[0]), GrowArrow(cross[1]), FadeIn(cl), FadeIn(lines[0]))
            for mk, ln in zip("bcd", lines[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def picture(self):
        d = load("picture")
        head = label(rf"A picture through the channel \ ($p$ = {d['p']})", font_size=34).to_edge(UP, buff=0.3)
        W, H = d["W"], d["H"]

        def img(bits, color):
            arr = np.zeros((H, W, 3), dtype=np.uint8)
            rgb = np.array(ManimColor(color).to_rgb()) * 255
            for i, b in enumerate(bits):
                arr[i // W, i % W] = rgb if b else (18, 23, 34)
            m = ImageMobject(arr)
            m.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
            m.scale_to_fit_width(5.6)
            return m
        e = d["errors"]
        tiles = [(d["orig"], WHITE, r"sent: \ 3{,}840 pixels"),
                 (d["raw"], NO, rf"no code: \ {e['raw']} pixels wrong"),
                 (d["rep"], DATA, rf"repetition $\times 3$ \ (11{{,}}520 bits sent): \ {e['rep']} wrong"),
                 (d["ham"], YES, rf"Hamming(7,4) \ (6{{,}}720 bits sent): \ {e['ham']} wrong")]
        imgs = Group(*[img(b, c) for b, c, _ in tiles]).arrange_in_grid(rows=2, cols=2, buff=(0.5, 0.9))
        imgs.next_to(head, DOWN, buff=0.45)
        caps = VGroup(*[label(t, font_size=19, color=c).next_to(m, DOWN, buff=0.1) for (_, c, t), m in
                        zip(tiles, imgs)])
        with self.voiceover(
            "Here is what noise does to a picture, and what codes do about it. <bookmark mark='a'/> A black-and-white image of three thousand "
            "eight hundred and forty pixels. <bookmark mark='b'/> Sent as it is through a channel that flips one bit "
            "in twenty, it arrives speckled: a hundred and seventy-nine pixels wrong. <bookmark mark='c'/> Sending "
            "every pixel three times and voting cuts that to twenty-two, but triples the traffic. <bookmark "
            "mark='d'/> Hamming's code, chapter three, gets sixty, while sending less than twice as many bits. "
            "Which trade is better depends on the channel; the rest of this part is about doing better than both."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(imgs[0]), FadeIn(caps[0]))
            for i, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(FadeIn(imgs[i + 1]), FadeIn(caps[i + 1]))
        self.wait(0.3)
        self.clear_scene()

    def repetition(self):
        r = load("repetition")
        head = label(r"Say it again: \ the repetition code", font_size=34).to_edge(UP, buff=0.35)
        rows = []
        for x in r["rows"]:
            ex = x["exact"]
            rows.append([str(x["n"]), rf"$1/{x['n']}$" if x["n"] > 1 else "1",
                         f"{ex:.4f}" if ex >= 1e-3 else rf"${sci(ex, 2)}$",
                         f"{x['sim']:.4f}" if x["sim"] else r"0 \ (in 20{,}000)"])
        tab = grid_table([r"copies $n$", r"rate", r"bit error, \ exact", r"simulated"], rows,
                         widths=[2.0, 1.8, 3.0, 3.0], row_h=0.45, font_size=21, mono_cols=(),
                         colors=[[WHITE, DATA, NO, GREY_A]] * len(rows))
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        tl = label(rf"BSC with $p = {r['p']}$; \ majority vote", font_size=18, color=GREY_A).next_to(tab, DOWN,
                                                                                                 buff=0.12)
        lines = VGroup(
            label(r"send each bit $n$ times; \ decode by majority: \ wrong only if more than half flip", font_size=22,
                  color=WHITE),
            label(r"the error falls exponentially in $n$, \ but so does the \textbf{rate}: \ $1/n$ of the channel "
                  r"carries data", font_size=22, color=NO),
            label(r"25 copies: \ one error in about six million, \ and 4\% of the channel carries data", font_size=22,
                  color=HEAD),
            label(r"the folklore: \ reliability costs rate, \ without limit. \ Shannon \ (1948): \ \textbf{wrong}",
                  font_size=22, color=YES),
        ).arrange(DOWN, buff=0.25).next_to(tl, DOWN, buff=0.35)
        with self.voiceover(
            "The obvious code: say everything several times. <bookmark mark='a'/> Send each bit n times and let "
            "the receiver take a majority vote. It is wrong only if more than half the copies flip. <bookmark "
            "mark='b'/> With a channel that flips one bit in ten, three copies bring the error down to under three "
            "percent, nine copies to under one in a thousand. But the rate, the fraction of the channel carrying "
            "real data, falls as one over n. <bookmark mark='c'/> Twenty-five copies bring the error to about one in "
            "six million, and then only four percent of the channel carries data. <bookmark mark='d'/> Engineers "
            "in the 1940s assumed this was a law: more reliability always costs more rate, without limit. Shannon "
            "proved it false, as chapter nine will show. First, though, a picture."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab), FadeIn(tl))
            for mk, ln in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
