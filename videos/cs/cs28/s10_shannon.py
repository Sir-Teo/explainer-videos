from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs28.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, load)


class Shannon(VoiceoverScene):
    def construct(self):
        self.card()
        self.capacity()
        self.random_codes()
        self.proof()

    def card(self):
        card = chapter_card(9, r"Shannon's theorem", r"What is the price of noise?", lit=(1948, 1948),
                            extra=((1948, r"``A Mathematical Theory of Communication''"),), part=PART)
        with self.voiceover("Chapter nine. Shannon's theorem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def capacity(self):
        s = load("shannon")
        head = label(r"Capacity: \ $C = 1 - H(p)$", font_size=34).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 0.5, 0.1], y_range=[0, 1.02, 0.25], x_length=6.0, y_length=4.2,
                  axis_config={"color": GREY_D, "include_numbers": False}).next_to(head, DOWN, buff=0.55).to_edge(
            LEFT, buff=1.0)
        xt = VGroup(*[label(f"{x:g}", font_size=15, color=GREY_A).next_to(ax.c2p(x, 0), DOWN, buff=0.08)
                      for x in (0.1, 0.2, 0.3, 0.4, 0.5)])
        yt = VGroup(*[label(f"{y:g}", font_size=15, color=GREY_A).next_to(ax.c2p(0, y), LEFT, buff=0.08)
                      for y in (0.25, 0.5, 0.75, 1.0)])
        xl = label(r"flip probability $p$", font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.35)
        yl = label(r"bits of information per bit sent", font_size=17, color=GREY_A).rotate(PI / 2).next_to(
            ax, LEFT, buff=0.45)
        curve = VMobject(color=YES, stroke_width=3).set_points_smoothly([ax.c2p(p, c) for p, c in s["cap_curve"]])
        half = DashedLine(ax.c2p(0, 0.5), ax.c2p(0.5, 0.5), color=GREY_B, stroke_width=1.5)
        mark = Dot(ax.c2p(0.11, 0.5), radius=0.08, color=HEAD)
        ml = label(r"rate $\tfrac12$ works up to $p \approx 0.11$", font_size=17, color=HEAD).next_to(mark, UR,
                                                                                                  buff=0.08)
        lines = VGroup(
            label(r"\textbf{Shannon} \ (1948): \ for every rate $R < C$ there are codes \\ whose error probability "
                  r"goes to \textbf{zero} as the length grows", font_size=21, color=YES),
            label(r"and for $R > C$, \ the error stays bounded away from zero", font_size=21, color=NO),
            label(r"noise costs a \textbf{fixed fraction} of the rate, \ not all of it: \\ at $p = 0.1$, \ 53\% "
                  r"of the channel still carries data, \ reliably", font_size=21, color=WHITE),
            label(r"$H(p)$ is the entropy of the noise \ (Part 21, \ and \textit{AI, Built} 1): \\ the channel "
                  r"spends that much on uncertainty", font_size=21, color=DATA),
            label(r"repetition at $p = 0.1$ fell to rate 4\% for one error in six million; \\ Shannon promises 53\% "
                  r"with error as small as you like", font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(ax, RIGHT, buff=0.7).align_to(ax, UP)
        fit_right(lines)
        with self.voiceover(
            "In 1948, two years before Hamming's paper, Claude Shannon had already settled the big question. "
            "<bookmark mark='a'/> Every channel has a capacity. Below it, at any rate, there are codes whose error "
            "probability can be made as small as you like by making them long enough. <bookmark mark='b'/> Above "
            "it, no code works. <bookmark mark='c'/> So noise does not force the rate towards zero, as chapter one's "
            "repetition suggested: it costs a fixed fraction. For the binary symmetric channel the capacity is one "
            "minus the entropy of p. At one flip in ten, fifty-three percent of the channel can still carry data "
            "with arbitrarily few errors. <bookmark mark='d'/> The entropy is Part 21's measure of uncertainty: the "
            "channel spends that many bits per bit on the noise. <bookmark mark='e'/> Compare repetition, which "
            "needed to drop to four percent of the channel to reach one error in six million."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            self.play(Create(curve))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]), Create(half), FadeIn(mark), FadeIn(ml))
            for mk, ln in zip("bcde", lines[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def random_codes(self):
        s = load("shannon")
        head = label(r"Random codes, \ decoded optimally", font_size=34).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[6, 30, 4], y_range=[0, 0.6, 0.1], x_length=6.0, y_length=4.2,
                  axis_config={"color": GREY_D, "include_numbers": False}).next_to(head, DOWN, buff=0.55).to_edge(
            LEFT, buff=1.0)
        xt = VGroup(*[label(str(x), font_size=15, color=GREY_A).next_to(ax.c2p(x, 0), DOWN, buff=0.08)
                      for x in (8, 12, 16, 20, 24, 28)])
        yt = VGroup(*[label(f"{y:g}", font_size=15, color=GREY_A).next_to(ax.c2p(6, y), LEFT, buff=0.08)
                      for y in (0.1, 0.2, 0.3, 0.4, 0.5)])
        xl = label(r"block length $n$ \ (rate $\tfrac12$)", font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.35)
        yl = label(r"block error", font_size=17, color=GREY_A).rotate(PI / 2).next_to(ax, LEFT, buff=0.45)
        cols = {"0.05": YES, "0.11": HEAD, "0.15": NO}
        curves = VGroup()
        keys = VGroup()
        for p in ("0.05", "0.11", "0.15"):
            pts = [ax.c2p(r["n"], r[p]) for r in s["rows"]]
            curves.add(VGroup(VMobject(color=cols[p], stroke_width=3).set_points_as_corners(pts),
                              *[Dot(q, radius=0.06, color=cols[p]) for q in pts]))
            keys.add(label(rf"$p = {p}$: \ $C = {s['capacity'][p]:.2f}$", font_size=18, color=cols[p]))
        keys.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(ax.c2p(12, 0.53))
        r0, r1 = s["rows"][0], s["rows"][-1]
        lines = VGroup(
            label(r"random $[n, n/2]$ linear codes; \ maximum-likelihood \\ decoding by a table of coset leaders",
                  font_size=21, color=WHITE),
            label(rf"below capacity: \ the error \textbf{{falls}} with length \\ ({r0['0.05'] * 100:.0f}\% at $n$ = 8, "
                  rf"\ {r1['0.05'] * 100:.0f}\% at $n$ = 28)", font_size=21, color=YES),
            label(rf"above capacity: \ it \textbf{{rises}} \\ ({r0['0.15'] * 100:.0f}\% to {r1['0.15'] * 100:.0f}\%)",
                  font_size=21, color=NO),
            label(r"at capacity: \ roughly flat", font_size=21, color=HEAD),
            label(r"the catch: \ decoding a random code takes \\ a table of size $2^{n-k}$: \ hopeless for $n$ = 1000",
                  font_size=21, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(ax, RIGHT, buff=0.7).align_to(ax, UP)
        fit_right(lines)
        with self.voiceover(
            "We can watch the theorem start to work. <bookmark mark='a'/> Take random linear codes of rate one "
            "half, and decode them perfectly, with a table of the most likely error for every syndrome. <bookmark "
            "mark='b'/> On a channel with five percent flips, whose capacity is point seven one, the block error "
            "falls as the codes get longer: from eleven percent at length eight to five percent at twenty-eight. "
            "<bookmark mark='c'/> At fifteen percent flips the capacity is below one half, and the error rises "
            "instead. <bookmark mark='d'/> Right at capacity it hardly moves. These lengths are tiny, so the trend is "
            "gentle, but its direction is Shannon's theorem. <bookmark mark='e'/> And here is the catch that took "
            "fifty years: decoding a random code needs a table with two to the n minus k entries. Shannon proved "
            "good codes exist. Finding ones that can be decoded fast was the rest of the story."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(Create(curves[0]), FadeIn(keys[0]), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(Create(curves[2]), FadeIn(keys[2]), FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(Create(curves[1]), FadeIn(keys[1]), FadeIn(lines[3]))
            vo.wait_until("e")
            self.play(FadeIn(lines[4]))
        self.wait(0.3)
        self.clear_scene()

    def proof(self):
        head = label(r"Why random codes work", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"send $n$ bits: \ about $pn$ of them flip, \ and the received word lies near a sphere of radius "
                  r"$pn$", font_size=22, color=WHITE),
            label(r"that sphere holds about $2^{nH(p)}$ words: \ the \textbf{typical} errors \ (\textit{AI, Built} 1)",
                  font_size=22, color=DATA),
            label(r"pick $2^{nR}$ codewords at random; \ decode to the one whose sphere contains what arrived",
                  font_size=22, color=HEAD),
            label(r"another codeword lands in that sphere with probability about $2^{nR} \cdot 2^{nH(p)} / 2^n = "
                  r"2^{-n(C - R)}$", font_size=22, color=YES),
            label(r"so for $R < C$ the error vanishes \textbf{on average over codes}: \ some code must be that good",
                  font_size=22, color=YES),
            label(r"converse \ (Fano's inequality): \ $nR$ bits cannot squeeze through $nC$ bits of real "
                  r"information", font_size=22, color=NO),
            label(r"a proof by \textbf{counting} that constructs nothing: \ the codes of the next three chapters "
                  r"took 45 years", font_size=22, color=LAM),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Shannon's argument is a counting argument. <bookmark mark='a'/> Send n bits; about p n of them flip, "
            "so what arrives lies close to a sphere of radius p n around what was sent. <bookmark mark='b'/> That "
            "sphere holds about two to the n H of p words, the typical errors of AI, Built's first part. <bookmark "
            "mark='c'/> Now choose two to the n R codewords completely at random, and decode to the codeword whose "
            "sphere contains what arrived. <bookmark mark='d'/> The chance that some other codeword also lands in "
            "that sphere is about two to the minus n times C minus R. <bookmark mark='e'/> When the rate is below "
            "capacity, that vanishes, on average over random codes, so at least one code is that good. <bookmark "
            "mark='f'/> The converse uses Fano's inequality: no code can push more than the capacity through. "
            "<bookmark mark='g'/> The proof constructs nothing. The practical codes that reach capacity, in the next "
            "three chapters, took another forty-five years."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdefg", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
