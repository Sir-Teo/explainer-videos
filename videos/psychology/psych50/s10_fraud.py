from __future__ import annotations

from videos.psychology.psych50.common import *  # noqa: F403


class Fraud(VoiceoverScene):
    def construct(self):
        self.card()
        self.miles()
        self.method()

    def card(self):
        card = chapter_card(9, r"Fabrication, \ detected", r"What gives invented data away?", lit=(), part=PART,
                            scale=("society",), marr=("how",))
        with self.voiceover("Chapter nine. Fabrication, detected."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def miles(self):
        d = load("mileage")
        head = heading(r"Miles that no one drives")
        edges = np.asarray(d["edges"])
        mid = (edges[:-1] + edges[1:]) / 2
        A = axes([0, 60000], [0, 950], x_length=5.6, y_length=3.0, xticks=[0, 25000, 50000], yticks=[0, 400, 800],
                 xfmt=lambda v: f"{v / 1000:.0f}k", yfmt=lambda v: f"{v:.0f}", xlabel=r"miles driven between two "
                 r"readings", ylabel=r"customers", center=[-3.3, 0.3, 0], font_size=12)
        br = bars(A.ax, mid, d["real"], SYMP, width=2200, opacity=0.7)
        bf = bars(A.ax, mid, d["fake"], AUTH, width=2200, opacity=0.7)
        key = VGroup(label(r"how real driving looks", font_size=13, color=SYMP),
                     label(r"numbers drawn evenly from 0 to 50,000", font_size=13, color=AUTH)).arrange(RIGHT, buff=0.4)
        key.next_to(A, UP, buff=0.25)
        rows = rows_of([
            (r"a 2012 field study reported that signing an honesty pledge at the top of an insurance form made "
             r"customers report their mileage more honestly", WHITE),
            (r"in 2021 independent analysts looked at the posted data: \ the miles driven were spread evenly from 0 to "
             r"50,000, \ with none above", AUTH),
            (r"real driving piles up at moderate distances and thins out slowly (blue); \ evenly spread numbers with a "
             r"hard edge (red) are what a random-number generator makes", MODEL),
            (r"the paper was retracted; \ a later large study found no effect of signing first", YOU),
        ], 6.0, 18, 0.34).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"simulated distributions, \ for illustration")
        with self.voiceover(
            "Sometimes the numbers are invented. <bookmark mark='a'/> A 2012 field study reported that signing an "
            "honesty pledge at the top of an insurance form, rather than the bottom, made customers report their "
            "mileage more honestly. <bookmark mark='b'/> In 2021 independent analysts looked at the posted data. The "
            "miles driven were spread evenly from zero to fifty thousand, with none above. <bookmark mark='c'/> Real "
            "driving piles up at moderate distances and thins out slowly, like the blue bars. Evenly spread numbers "
            "with a hard edge, like the red ones, are what a random-number generator makes. <bookmark mark='d'/> The "
            "paper was retracted, and a later large study found no effect of signing first."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(br))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(bf))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def method(self):
        head = heading(r"What gives fabrication away")
        items = [
            (r"distributions", r"too flat, \ too smooth, \ or with a hard edge where real data trail off", AUTH),
            (r"digits", r"last digits that are not evenly spread, \ or rounded values where measurements are exact",
             PERSON),
            (r"too good", r"effects too consistent across studies, \ or variances too similar for the sample sizes",
             MODEL),
            (r"the file itself", r"spreadsheet history, \ fonts and sort orders that show rows added by hand", SYMP),
        ]
        rows = VGroup()
        for name, what, col in items:
            rows.add(VGroup(word_chip(name, col, 21, width=3.4), wrapped_label(what, 8.6, 21, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.2, 0])
        foot = wrapped_label(r"every one of these needs the data: \ open data is what makes fraud findable (Part 36's "
                             r"canvassing study was caught the same way)", 12.0, 21, YOU).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "What gives fabrication away? <bookmark mark='a'/> Distributions: too flat, too smooth, or with a hard "
            "edge where real data trail off. <bookmark mark='b'/> Digits: last digits that aren't evenly spread, or "
            "rounded values where measurements are exact. <bookmark mark='c'/> Results that are too good: effects too "
            "consistent across studies, or variances too similar for the sample sizes. <bookmark mark='d'/> And the "
            "file itself: spreadsheet history, fonts and sort orders that show rows added by hand. Every one of these "
            "needs the data. Open data is what makes fraud findable. Part 36's canvassing study was caught the same "
            "way."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            self.play(FadeIn(foot))
        self.clear_scene()
