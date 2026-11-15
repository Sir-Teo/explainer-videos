from __future__ import annotations

import numpy as np

from videos.music.music63.common import *  # noqa: F403


class Robust(SoundScene):
    def construct(self):
        chapter(self, 3, r"Noise, \ codecs and chance", r"How much can go wrong before the answer does?")
        self.noise_heard()
        self.curves()
        self.codec_quiz()
        self.chance()

    # ------------------------------------------------------------------
    def noise_heard(self):
        d = load("robust")
        c = clip("noise.three")
        boxes = choice_boxes([rf"10 dB above", r"level", r"5 dB below"], width=2.8, height=0.9, buff=0.7, size=19).move_to(UP * 0.5)
        res = VGroup(*[label((r"named" if n["ok"] else r"missed") + rf" \ ({n['votes']} votes)", font_size=16,
                             color=TUNE if n["ok"] else EAR).next_to(boxes[i], DOWN, buff=0.3) for i, n in enumerate(d["named"])])
        head = label(r"one query, \ three bars", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear one five-second query in three bars: the music ten decibels above the noise, level with it, and five decibels below."):
            self.play(FadeIn(head), FadeIn(boxes))
        st = d["starts3"]
        with self.listen(c) as snd:
            window(snd, r"louder and louder bars", kind="physical model", detail=r"a Variation, \ simulated noise", corner=DL, tag_corner=DR)
            ks = ["s10", "s0", "sm5"]
            for i, k in enumerate(ks):
                end = st[ks[i + 1]] - 0.3 if i + 1 < len(ks) else c.duration
                pulse(snd, boxes[i], st[k], end, buff=0.08)
        with self.voiceover("And what the fingerprinter made of each: the votes fall as the noise rises, as more of the peaks it needs are buried or moved."):
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curves(self):
        d = load("robust")
        snr = d["snrs"]
        ax = frame_axes(width=8.4, height=3.2, xlo=-10, xhi=20, ylo=0, yhi=1.05, center=DOWN * 0.4 + LEFT * 0.6)
        cw = curve(snr, d["rates"]["white"], ax.to, color=GREY_B, width=3)
        cb = curve(snr, d["rates"]["bar"], ax.to, color=TUNE, width=3.5)
        dots = VGroup(*[Dot(ax.to(s, r), radius=0.05, color=GREY_B) for s, r in zip(snr, d["rates"]["white"])],
                      *[Dot(ax.to(s, r), radius=0.05, color=TUNE) for s, r in zip(snr, d["rates"]["bar"])])
        xt = VGroup(*[label(f"{v} dB", font_size=13, color=GREY_A).next_to(ax.to(v, 0), DOWN, buff=0.1) for v in (-10, -5, 0, 5, 10, 20)])
        yt = VGroup(*[label(f"{int(100 * v)}\\%", font_size=13, color=GREY_A).next_to(ax.to(-10, v), LEFT, buff=0.1) for v in (0, 0.5, 1)])
        key = VGroup(label(r"bar noise", font_size=16, color=TUNE), label(r"white noise", font_size=16, color=GREY_B),
                     label(r"music above the noise \ $\rightarrow$", font_size=13, color=GREY_A)).arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.3)
        rb = dict(zip(snr, d["rates"]["bar"]))
        head = label(rf"{d['n']} queries from the Variations, \ five seconds each", font_size=24, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"Now count, over {say(d['n'])} queries taken from the Variations. <bookmark mark='a'/> With bar noise, the fingerprinter "
            f"names {say(100 * rb[10])} percent at ten decibels, {say(100 * rb[0])} percent with the music level with the noise, and "
            f"{say(100 * rb[-5])} percent five decibels below. <bookmark mark='b'/> White noise at the same level is easier: "
            "it spreads its energy evenly and thinly, while the bar's voices and glasses make peaks of their own, which compete "
            f"with the music's. {say(d['n_alias'])} of the Variations reuse sound from another clip of their part; finding that "
            "clip counts as right."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xt), FadeIn(yt), FadeIn(key[2]))
            vo.wait_until("a")
            self.play(Create(cb), FadeIn(dots[len(snr):]), FadeIn(key[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(cw), FadeIn(dots[:len(snr)]), FadeIn(key[1]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def codec_quiz(self):
        d = load("robust")
        c = clip("codec.two")
        card = listen_card(r"The same five seconds, \ twice: \ once as stored, \ once through Part 58's coder at 16 kbit/s. \ Which was coded?", width=9.0)
        with self.voiceover("Your turn. The same five seconds, twice: once as stored, once through Part 58's coder at sixteen kilobits. Which was coded?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second"]).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"coded or not?", kind="physical model", detail=r"a Variation, \ Part 58's coder", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        rates = ", \\ ".join(rf"{r['kbps']} kbit/s: \ {100 * r['rate']:.0f}\%" for r in d["codec"])
        res = VGroup(label(r"the first: \ dull and watery", font_size=19, color=TUNE), label(rf"named after coding: \ {rates}", font_size=17, color=WHITE)).arrange(DOWN, buff=0.25).move_to(DOWN * 1.4)
        with self.voiceover(
            "The first was coded: duller and a little watery. But the peaks survive a codec, which is built to keep the "
            "loudest parts of the spectrum: the fingerprinter names almost every coded query, even at sixteen kilobits."
        ):
            self.play(boxes[0][0].animate.set_stroke(TUNE, width=4), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def chance(self):
        d = load("falsematch")
        m = d["model"]
        lines = VGroup(
            label(r"a random hash matches a given stored one with probability $2^{-24} \approx 6 \times 10^{-8}$", font_size=20, color=WHITE),
            label(rf"a query's 400 hashes against {d['db_hashes']:,} stored: \ about {m['chance_hits']:.1f} chance hits in all", font_size=20, color=WHITE),
            label(r"but they scatter over every clip and every offset: \ a few at most in any one place", font_size=20, color=WHITE),
            label(rf"queries of pure noise: \ at most {max(d['noise_top_votes'])} votes in any one place; \ true matches: \ {min(d['true_votes'])} to {max(d['true_votes'])}", font_size=20, color=TUNE),
            label(r"so a threshold of a few dozen votes almost never names the wrong recording", font_size=19, color=GREY_A),
        ).arrange(DOWN, buff=0.4)
        head = label(r"the arithmetic of chance", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "And when the music is not in the library at all, does the system invent an answer? <bookmark mark='a'/> A random "
            "hash matches a given stored hash with probability two to the minus twenty-four. <bookmark mark='b'/> A query's few "
            f"hundred hashes against {say(d['db_hashes'])} stored ones give a handful of chance hits in all. "
            "<bookmark mark='c'/> But they scatter over every clip and every offset. <bookmark mark='d'/> Queries of pure noise "
            f"collect at most {say(max(d['noise_top_votes']))} votes in any one place; true matches collect "
            f"{say(min(d['true_votes']))} or more. <bookmark mark='e'/> So a threshold of a few dozen votes almost never names the "
            "wrong recording: Part 60's birthday problem, kept in check by demanding agreement in time."
        ) as vo:
            self.play(FadeIn(head))
            for mark, ln in zip("abcde", lines):
                vo.wait_until(mark)
                self.play(FadeIn(ln))
        self.wait(0.4)
        self.clear_scene()
