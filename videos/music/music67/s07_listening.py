from __future__ import annotations

import numpy as np

from videos.music.music67.common import *  # noqa: F403


class Listening(SoundScene):
    def construct(self):
        chapter(self, 6, r"Listening tests and their power", r"How many trials does it take to know that a difference is heard?")
        self.abx()
        self.curves()
        self.quiz2()
        self.mushra()
        self.panels()

    # ------------------------------------------------------------------
    def abx(self):
        d = load("power")
        t = d["twenty"]["0.6"]
        lines = VGroup(
            label(r"an ABX test: \ in each trial, \ say whether X is A or B; \ by guessing, \ half are right", font_size=20, color=WHITE),
            label(rf"20 trials: \ to pass at the 5\% level you need {t['critical']} right \ (the chance of that by guessing: \ {100 * t['size']:.1f}\%)", font_size=20, color=WHITE),
            label(r"a listener who truly hears the difference 60\% of the time:", font_size=20, color=WHITE),
            label(rf"passes 20 trials only {100 * t['power']:.0f}\% of the time", font_size=24, color=EAR),
            label(r"a nonsignificant result alone does not establish inaudibility; confidence bounds and power determine what differences it can rule out", font_size=19, color=TUNE),
        ).arrange(DOWN, buff=0.4)
        head = label(r"the hook's test, \ counted", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"The hook's test, counted. <bookmark mark='a'/> In each trial a listener says whether X is A or B, and by guessing is right half the time. <bookmark mark='b'/> In twenty trials, passing at the five per cent level takes {say(t['critical'])} right. <bookmark mark='c'/> Now take a listener who really does hear the difference, though only sixty per cent of the time. <bookmark mark='d'/> That listener passes twenty trials only {say(round(100 * t['power']))} per cent of the time. <bookmark mark='e'/> So a nonsignificant result alone does not establish inaudibility; confidence bounds and power determine what differences it can rule out. Many audio debates have been settled by tests that could not have found what they looked for."
        ) as vo:
            self.play(FadeIn(head))
            for mark, ln in zip("abcde", lines):
                vo.wait_until(mark)
                self.play(FadeIn(ln))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curves(self):
        d = load("power")
        ns = np.array(d["ns"])
        cols = {"0.55": GREY_B, "0.6": EAR, "0.75": BLUE, "0.9": TUNE}
        ax = frame_axes(width=8.0, height=3.4, xlo=0, xhi=200, ylo=0, yhi=1, center=DOWN * 0.4 + LEFT * 1.0)
        cvs = VGroup(*[curve(ns, np.array(d["curves"][k]), ax.to, color=cols[k], width=3) for k in ("0.9", "0.75", "0.6", "0.55")])
        eighty = DashedLine(ax.to(0, 0.8), ax.to(200, 0.8), color=GREY_D, stroke_width=1.5)
        xl = label(r"trials", font_size=14, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        yl = label(r"chance of passing \ (power)", font_size=14, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        nd = d["needed"]
        key = VGroup(*[label(rf"hears it {int(100 * float(k))}\%: \ {nd[k]} trials for 80\%", font_size=16, color=cols[k]) for k in ("0.9", "0.75", "0.6", "0.55")]).arrange(DOWN, buff=0.25, aligned_edge=LEFT).to_edge(RIGHT, buff=0.3)
        head = label(r"power by trials", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is the power of the test for listeners of four abilities, by the number of trials. <bookmark mark='a'/> A "
            f"listener right ninety per cent of the time is caught in {say(nd['0.9'])} trials, eighty per cent of the time; "
            f"seventy-five per cent, in {say(nd['0.75'])}. <bookmark mark='b'/> Sixty per cent needs {say(nd['0.6'])}, and "
            f"fifty-five per cent {say(nd['0.55'])}. Small differences need many trials, or many listeners, and a study should "
            "say in advance which difference it can find."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xl), FadeIn(yl), FadeIn(eighty))
            vo.wait_until("a")
            self.play(Create(cvs[0]), Create(cvs[1]), FadeIn(key[0]), FadeIn(key[1]), run_time=1.4)
            vo.wait_until("b")
            self.play(Create(cvs[2]), Create(cvs[3]), FadeIn(key[2]), FadeIn(key[3]), run_time=1.4)
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def panels(self):
        items = [
            (r"listeners differ: \ pool many, \ and report each, \ because a few may hear what most do not", WHITE),
            (r"blind and randomized: \ the listener, \ and the person running the test, \ must not know which is which", WHITE),
            (r"training and anchors: \ MUSHRA's hidden reference and low anchor \ (Part 58) \ catch listeners who are not listening", WHITE),
            (r"online studies reach thousands; \ their headphones and rooms are unknown, \ so screen for them", TUNE),
        ]
        rows_scene(self, r"listening panels", items,
                   "Running listening tests well takes more than trials. <bookmark mark='b'/> Listeners differ: pool many and report each, because a few may hear what most do not. <bookmark mark='c'/> Blind and randomized: neither the listener nor the person running the test may know which is which. <bookmark mark='d'/> Training and anchors: MUSHRA's hidden reference and low anchor, from Part 58, help assess test reliability, subject to prespecified screening rules. <bookmark mark='e'/> And online studies reach thousands, with headphones and rooms unknown, so screen for them with a headphone-screening test, which itself has false positives and false negatives.", marks="bcde")

    # ------------------------------------------------------------------
    def quiz2(self):
        d = load("abx2")
        c = clip("abx2.three")
        card = listen_card(r"Another trial, \ harder: \ the Tune's second phrase, \ A, \ B, \ then X. \ Is X A or B?", width=8.8)
        with self.voiceover("Your turn again, harder this time. The Tune's second phrase: A, then B, then X. Is X the same as A, or as B?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"A", r"B", r"X"], width=2.6, buff=0.8).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        ks = ["A", "B", "X"]
        with self.listen(c) as snd:
            window(snd, r"A, \ B, \ X", kind="physical model", detail=r"Part 38's piano; \ Part 58's coder", corner=DL, tag_corner=DR)
            for i, k in enumerate(ks):
                end = st[ks[i + 1]] - 0.4 if i + 1 < len(ks) else c.duration
                pulse(snd, boxes[i], st[k], end, buff=0.08)
        res = label(rf"X was A, \ the original; \ B was the coder at {d['kbps']} kbit/s. \ Two trials: \ even both right is p = 0.25", font_size=18, color=TUNE).move_to(DOWN * 1.4)
        with self.voiceover(
            f"X was A, the original; B was the coder at {say(d['kbps'])} kilobits, where many listeners hear "
            "little or nothing. Two trials right out of two would happen by guessing a quarter of the time: to say anything, "
            "you would need the dozens of trials on the last page."
        ):
            self.play(boxes[0][0].animate.set_stroke(TUNE, width=4), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mushra(self):
        d = load("mushra")["listeners"]
        rows = VGroup(*[VGroup(label(rf"a difference of {k} points", font_size=20, color=WHITE), label(rf"{v} listeners", font_size=20, color=TUNE)).arrange(RIGHT, buff=0.8) for k, v in d.items()]).arrange(DOWN, buff=0.38).move_to(DOWN * 0.2)
        note = label(r"ratings on a 100-point scale; \ listeners differ by 15 points; \ 80\% power, \ 5\% level, \ paired", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.45)
        head = label(r"how many listeners for MUSHRA?", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The same arithmetic for rating tests. In a MUSHRA test listeners rate each system from nought to a hundred, and "
            "suppose the standard deviation of paired rating differences is fifteen points. <bookmark mark='a'/> To find a difference of twenty points takes "
            f"{say(d['20'])} listeners; ten points, {say(d['10'])}; five points, {say(d['5'])}; three points, {say(d['3'])}. "
            "Many published comparisons of codecs and separators use a dozen or two listeners, enough for large differences "
            "and not for small ones."
        ) as vo:
            self.play(FadeIn(head), FadeIn(note))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[::-1]], lag_ratio=0.3), run_time=1.6)
        self.wait(0.6)
        self.clear_scene()
