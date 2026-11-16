from __future__ import annotations

import numpy as np

from videos.music.music58.common import *  # noqa: F403

PCOL = {"0.6": GREY_A, "0.7": BLUE, "0.8": TUNE, "0.9": EAR}


class Tests(SoundScene):
    def construct(self):
        chapter(self, 8, r"Listening tests", r"How do you prove that nobody can hear a difference?")
        self.trial()
        self.stats()
        self.power()
        self.methods()

    # ------------------------------------------------------------------
    def trial(self):
        d = load("abx")
        c = clip("abx.trial")
        card = listen_card(r"An ABX trial. \ A is the Tune as sung; \ B is the same through our coder at 32 kbit/s; \ X is one of "
                           r"the two. \ Is X A or B?", width=10.0)
        with self.voiceover("An ABX trial, for you. A is the Tune as sung. B is the same through our coder at thirty-two kilobits. X is one of the two. Is X A, or B?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"A", r"B", r"X"], width=2.4, buff=1.0).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"A, \ B, \ X", kind="physical model", detail=r"Part 8's voice, \ Monochord's coder", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["A"], st["B"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["B"], st["X"] - 0.4, buff=0.08)
            pulse(snd, boxes[2], st["X"], c.duration, buff=0.08)
        res = label(r"X was B. \ One right answer proves nothing: \ a guesser gets it half the time", font_size=20, color=TUNE).move_to(DOWN * 1.4)
        with self.voiceover("X was B. But one right answer proves nothing: someone guessing gets it right half the time. The proof is in counting."):
            self.play(boxes[1][0].animate.set_stroke(TUNE, width=4), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def stats(self):
        d = load("abx")
        eq = MathTex(r"P(\text{at least } c \text{ right out of } n \mid \text{guessing}) = \sum_{j=c}^{n}\binom{n}{j}2^{-n} < 0.05", font_size=34, color=TUNE).move_to(UP * 1.4)
        rows = VGroup(VGroup(label(r"trials", font_size=17, color=GREY_A), *[label(n, font_size=17, color=GREY_A) for n in ("8", "12", "16", "20", "30", "50", "100")]))
        rows.add(VGroup(label(r"right answers needed", font_size=17, color=WHITE), *[label(str(d["threshold"][n]), font_size=18, color=TUNE) for n in ("8", "12", "16", "20", "30", "50", "100")]))
        rows.arrange(DOWN, buff=0.35)
        for r in rows:
            r[0].set_x(-4.6)
            for i, m in enumerate(r[1:]):
                m.set_x(-2.2 + 1.3 * i)
        rows.move_to(DOWN * 0.6)
        note = label(r"the null hypothesis: \ the listener cannot hear the difference, \ and guesses; \ reject it only when the count would be rare for a guesser", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.45)
        head = label(r"counting right answers", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "So repeat the trial, and count. <bookmark mark='a'/> If the listener hears no difference, each answer is a coin "
            "toss, and the number right follows the binomial distribution. Call the result significant when a guesser would do "
            "as well less than one time in twenty. <bookmark mark='b'/> In eight trials that needs seven right; in sixteen, "
            "twelve; in a hundred, fifty-nine. These thresholds assume a preplanned, one-sided test with independent fair guesses; repeated or adaptive testing needs adjustment, which Part 67 will take further."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eq))
            vo.wait_until("a")
            self.play(FadeIn(note))
            vo.wait_until("b")
            self.play(FadeIn(rows))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def power(self):
        d = load("abx")
        ns = np.array(d["n"], float)
        ax = frame_axes(width=8.6, height=3.2, xlo=0, xhi=100, ylo=0, yhi=1.05, center=DOWN * 0.3 + LEFT * 0.6)
        cs = VGroup()
        for p, col in PCOL.items():
            ys = d["power"][p]
            cs.add(VGroup(curve(ns, ys, ax.to, color=col, width=3), *[Dot(ax.to(x, y), radius=0.05, color=col) for x, y in zip(ns, ys)]))
        key = VGroup(*[label(rf"right {int(float(p) * 100)}\% of the time", font_size=16, color=col) for p, col in PCOL.items()]).arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.3)
        xt = VGroup(*[label(f"{v}", font_size=14, color=GREY_A).next_to(ax.to(v, 0), DOWN, buff=0.1) for v in (0, 20, 50, 100)])
        xl = label(r"trials", font_size=15, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        yt = VGroup(*[label(f"{v:g}", font_size=14, color=GREY_A).next_to(ax.to(0, v), LEFT, buff=0.1) for v in (0, 0.5, 1)])
        p16 = d["power"]["0.7"][3]
        head = label(r"the power of an ABX test", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        note = label(rf"a listener right 70\% of the time passes a 16-trial test only {100 * p16:.0f}\% of the time", font_size=17, color=WHITE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The other side of the test is its power: the chance it detects a listener who really can hear the difference. "
            "<bookmark mark='a'/> A listener right nine times in ten passes almost any test. <bookmark mark='b'/> But a listener "
            f"right seven times in ten, who certainly hears something, passes a sixteen-trial test only {say(100 * p16)} per cent "
            "of the time, and needs fifty trials to be found reliably. So a failed short test does not show that a difference is "
            "inaudible; it means this test did not establish discrimination; sample size, listener ability, excerpt and test conditions all matter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xt), FadeIn(xl), FadeIn(yt), FadeIn(ghost(cs, 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(cs[3]), FadeIn(key[3]), FadeIn(cs[2]), FadeIn(key[2]))
            vo.wait_until("b")
            self.play(FadeIn(cs[1]), FadeIn(key[1]), FadeIn(cs[0]), FadeIn(key[0]), FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def methods(self):
        items = [
            (r"ITU-R BS.1116 \ (1994): \ for small impairments: \ a hidden reference, \ a five-point scale, \ trained listeners, \ a quiet room", WHITE),
            (r"MUSHRA \ (BS.1534, \ 2001): \ several systems at once against a hidden reference and a low-passed anchor, \ scored 0 to 100", WHITE),
            (r"listeners are screened: \ those who rate the hidden reference low are dropped", WHITE),
            (r"the results are analysed with confidence intervals across listeners and items, \ not a single score", WHITE),
            (r"every codec in this chapter was tuned by tests like these; \ objective measures came later, \ and learned ones later still", TUNE),
        ]
        rows_scene(self, r"formal tests", items,
                   "Codecs are judged by formal tests. <bookmark mark='b'/> The ITU's BS.1116, from 1994, is for small impairments: a hidden reference, a five-point scale, trained listeners and a quiet room. <bookmark mark='c'/> MUSHRA, BS.1534 from 2001, compares several systems at once against a hidden reference and a low-passed anchor, on a scale of nought to a hundred. <bookmark mark='d'/> Listeners are screened: exclusion criteria are specified by the test protocol and applied with care; a low reference rating alone is not a universal rule. <bookmark mark='e'/> The results are reported with confidence intervals across listeners and pieces of music, never as one number. <bookmark mark='f'/> Every codec of the last chapter was tuned by tests like these; objective measures came later, and learned ones later still.", marks="bcdef")
