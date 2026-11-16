from __future__ import annotations

import numpy as np

from videos.music.music60.common import *  # noqa: F403


class Melodies(SoundScene):
    def construct(self):
        chapter(self, 9, r"How many melodies are there?", r"How often do two songs share a phrase by chance?")
        self.counting()
        self.curve()
        self.odds()
        self.pairs()
        self.cases()

    # ------------------------------------------------------------------
    def counting(self):
        lines = VGroup(
            MathTex(r"q_k = \sum_{s \in \text{all } k\text{-note melodies}} P(s)^2", font_size=36, color=TUNE),
            label(r"the chance that two melodies drawn independently from a model open with the same k notes", font_size=19, color=WHITE),
            MathTex(r"N_k = 1 / q_k", font_size=36, color=WHITE),
            label(r"the effective number of k-note melodies: \ as many equally likely ones would collide as often", font_size=19, color=WHITE),
            label(r"computed exactly from Part 14's model by summing over its contexts, \ not by sampling", font_size=17, color=GREY_A),
        ).arrange(DOWN, buff=0.35)
        head = label(r"counting melodies", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "How many melodies are there? The naive answer is astronomical: twenty notes in eight places is twenty to the "
            "eighth, twenty-five billion. But melodies are not drawn evenly. <bookmark mark='a'/> The right count is the "
            "collision probability: the chance that two melodies drawn independently from a model of real melodies open with the "
            "same k notes, the sum of each melody's probability squared. <bookmark mark='b'/> Its reciprocal is the effective "
            "number: how many equally likely melodies would collide as often. <bookmark mark='c'/> Monochord computes it exactly "
            "from Part 14's model of folk melody, by summing over the model's contexts, not by sampling."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]), FadeIn(lines[1]))
            vo.wait_until("b")
            self.play(FadeIn(lines[2]), FadeIn(lines[3]))
            vo.wait_until("c")
            self.play(FadeIn(lines[4]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curve(self):
        d = load("melodies")
        ks = d["ks"]
        eff = np.log10([d["effective"][str(k)] for k in ks])
        uni = np.log10([d["uniform"][str(k)] for k in ks])
        ax = frame_axes(width=8.4, height=3.6, xlo=3, xhi=12, ylo=0, yhi=16, center=DOWN * 0.3 + LEFT * 0.7)
        cu = curve(ks, uni, ax.to, color=GREY_B, width=3)
        ce = curve(ks, eff, ax.to, color=TUNE, width=3.5)
        dots = VGroup(*[Dot(ax.to(k, e), radius=0.05, color=TUNE) for k, e in zip(ks, eff)])
        xt = VGroup(*[label(f"{k}", font_size=14, color=GREY_A).next_to(ax.to(k, 0), DOWN, buff=0.1) for k in ks])
        xl = label(r"notes", font_size=15, color=GREY_A).next_to(xt, DOWN, buff=0.15)
        yt = VGroup(*[label(rf"$10^{{{v}}}$", font_size=14, color=GREY_A).next_to(ax.to(3, v), LEFT, buff=0.1) for v in (0, 4, 8, 12, 16)])
        key = VGroup(label(rf"every sequence of {d['alphabet']} notes, \ equally likely", font_size=15, color=GREY_B),
                     label(r"Part 14's model of folk melody", font_size=15, color=TUNE)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.3)
        n8 = label(rf"8 notes: \ {d['effective']['8']:,.0f}", font_size=16, color=TUNE).next_to(ax.to(8, np.log10(d['effective']['8'])), UP + LEFT, buff=0.1)
        head = label(r"effective numbers of melodies", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here are the two counts, on a logarithmic scale. <bookmark mark='a'/> Every sequence of the model's twenty notes, "
            "equally likely: twenty times more for every note added. <bookmark mark='b'/> The model's effective number "
            f"grows far more slowly: about {say(d['effective']['8'])} eight-note openings, and some seven million at twelve. "
            "Steps, the tonic and the scale crowd melodies together. Our model is crude, and real songwriters are freer than "
            "its corpus of folk tunes, but the gap, of nearly six orders of magnitude at eight notes, is the point."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xt), FadeIn(xl), FadeIn(yt))
            vo.wait_until("a")
            self.play(Create(cu), FadeIn(key[0]), run_time=1.2)
            vo.wait_until("b")
            self.play(Create(ce), FadeIn(dots), FadeIn(key[1]), FadeIn(n8), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def odds(self):
        d = load("melodies")
        lines = VGroup(
            label(rf"two songs of 60 notes each: \ {d['windows']} eight-note windows apiece", font_size=22, color=WHITE),
            MathTex(rf"P(\text{{some window shared}}) \approx 1 - e^{{-{d['windows']}^2\, q_8}} = {100 * d['pair_share8']:.1f}\%", font_size=34, color=TUNE),
            label(rf"among {d['songs'] / 1e6:.0f} million songs: \ about {d['birthday8']:.1e} pairs share their eight-note opening".replace("e+10", r" $\times 10^{10}$"), font_size=22, color=WHITE),
            label(r"so a shared phrase, \ alone, \ is weak evidence of copying; \ what else is shared matters", font_size=22, color=EAR),
        ).arrange(DOWN, buff=0.45)
        head = label(r"the birthday problem, \ for melodies", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Now the odds. <bookmark mark='a'/> Take two songs of sixty notes each: each has fifty-three windows of eight notes. "
            f"<bookmark mark='b'/> If the windows were independent draws from our model, the chance that some window is shared is "
            f"about {say(100 * d['pair_share8'], 1)} percent: one pair in twenty. <bookmark mark='c'/> Among a hundred million "
            "songs, about as many as the services hold, some ninety-six billion pairs share their eight-note opening. This is the "
            "birthday problem: rare for any one pair, certain somewhere. <bookmark mark='d'/> So a shared phrase, alone, is weak "
            "evidence of copying. What else is shared matters: rhythm, harmony, words, and whether the writer could have heard "
            "the other song."
        ) as vo:
            self.play(FadeIn(head))
            for mark, ln in zip("abcd", lines):
                vo.wait_until(mark)
                self.play(FadeIn(ln))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pairs(self):
        d = load("similar")
        c = clip("similar.pairs")
        m = d["match"]
        boxes = choice_boxes([r"the Tune", r"a fourth higher", r"the Tune", r"same contour"], width=2.4, height=0.85, buff=0.4, size=18).move_to(UP * 0.6)
        n1 = label(rf"a fourth higher: \ {m['transposed_notes']} of {m['n']} notes the same, \ {m['transposed_intervals']} of {m['n'] - 1} intervals: \ the same tune", font_size=17, color=TUNE).move_to(DOWN * 0.8)
        n2 = label(rf"same contour: \ {m['contour_notes']} notes and {m['contour_intervals']} intervals the same, \ every rise and fall kept: \ a different tune", font_size=17, color=BLUE).move_to(DOWN * 1.5)
        head = label(r"what makes two melodies the same?", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Which similarity counts? Hear two pairs: the Tune and the Tune a fourth higher; then the Tune and a melody that keeps its every rise and fall but changes the sizes of its steps."):
            self.play(FadeIn(head), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"two pairs", kind="physical model", detail=r"Part 38's piano", corner=DL, tag_corner=DR)
            ks = ["t1", "t2", "c1", "c2"]
            for i, k in enumerate(ks):
                end = st[ks[i + 1]] - 0.3 if i + 1 < len(ks) else c.duration
                pulse(snd, boxes[i], st[k], end, buff=0.08)
        with self.voiceover(
            'The transposed Tune shares not one note with the original, yet every interval, and many listeners recognize it as the same melody. The second shares every rise and fall, and is a different tune. Intervals and rhythm support transposition-invariant similarity, while absolute pitches, harmony, timbre and context can also matter, and contour alone is not enough.'
        ):
            self.play(FadeIn(n1), FadeIn(n2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cases(self):
        items = [
            (r"1976: \ `My Sweet Lord' found to copy `He's So Fine', \ subconsciously \ (US)", WHITE),
            (r"2015: \ a jury finds `Blurred Lines' infringed `Got to Give It Up': \ a feel, \ more than a melody \ (affirmed, \ 2018)", EAR),
            (r"2020: \ `Stairway to Heaven' cleared \ (Ninth Circuit, \ en banc); \ 2022: \ an ostinato in `Dark Horse' too common to own", TUNE),
            (r"2023: \ a jury clears Ed Sheeran's `Thinking Out Loud' of copying `Let's Get It On' \ (upheld on appeal, \ 2024)", TUNE),
            (r"the courts keep asking chance's question: \ is what is shared common property, \ or this writer's expression?", WHITE),
        ]
        rows_scene(self, r"in court \ (US, \ dated)", items,
                   "Courts have answered differently over the years. <bookmark mark='b'/> In 1976 George Harrison's My Sweet Lord "
                   "was found to have copied He's So Fine, subconsciously. <bookmark mark='c'/> In 2015 a jury found that Blurred "
                   "Lines infringed Marvin Gaye's Got to Give It Up, though what they shared was more a feel than a melody, and the "
                   "verdict was upheld in 2018. <bookmark mark='d'/> Then the tide turned: Stairway to Heaven was cleared by the "
                   "Ninth Circuit in 2020, and in 2022 an appeals court held that an ostinato in Katy Perry's Dark Horse was too "
                   "common to own. <bookmark mark='e'/> In 2023 a jury cleared Ed Sheeran's Thinking Out Loud of copying Let's Get "
                   "It On, and separate related litigation also produced appellate rulings; distinct cases and procedural histories should not be conflated. <bookmark mark='f'/> The courts keep asking chance's question: is "
                   "what is shared common property, or this writer's own expression?", marks="bcdef")
