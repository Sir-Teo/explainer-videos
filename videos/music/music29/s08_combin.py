from __future__ import annotations

import numpy as np

from videos.music.music29.common import *  # noqa: F403


class Combin(SoundScene):
    def construct(self):
        chapter(self, 7, r"Combinatoriality", r"Can two forms of a row fill all twelve notes together?", extra=((1955, r"Babbitt's `Some aspects of twelve-tone composition'"),))
        self.idea()
        self.hear()
        self.six()
        self.babbitt()
        self.webern21()

    # ------------------------------------------------------------------
    def idea(self):
        rows_ = text_rows([
            (r"Schoenberg's practice: \ pair a row with an inversion whose first six notes are the row's last six", WHITE),
            (r"then the two first halves, \ sounded together, \ hold all twelve pitch classes: \ an aggregate", WHITE),
            (r"and so do the two second halves", WHITE),
            (r"Milton Babbitt named it combinatoriality, \ and asked which hexachords allow it", TUNE),
            (r"the hexachord must map onto its own complement under some operation", GREY_A),
        ], font_size=24)
        head = label(r"filling the chromatic", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Schoenberg soon discovered a way to keep all twelve notes circulating even with two forms of the row at once. "
            "<bookmark mark='a'/> He paired the row with an inversion chosen so that the inversion's first six notes are "
            "exactly the row's last six. <bookmark mark='b'/> Then the two first halves, sounded together, contain all "
            "twelve pitch classes, an aggregate, <bookmark mark='c'/> and so do the two second halves. "
            "<bookmark mark='d'/> The American composer Milton Babbitt named this combinatoriality and asked which "
            "hexachords allow it. <bookmark mark='e'/> The condition is that the row's first hexachord maps onto its own "
            "complement under some transposition or inversion."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("combin")
        c = clip("combin.two")
        g = voices_roll([d["top"], d["bot"]], width=10.0, height=3.4, colors=[TUNE, BLUE], bar_h=0.12).move_to(DOWN * 0.2)
        mid = g.frame.get_left()[0] + g.frame.width * 6 / 12
        line = DashedLine([mid, g.frame.get_bottom()[1] - 0.2, 0], [mid, g.frame.get_top()[1] + 0.2, 0], color=GREY_B)
        l1 = label(r"aggregate 1: \ all twelve", font_size=20, color=EAR).next_to(line, LEFT, buff=1.6).shift(UP * 2.0)
        l2 = label(r"aggregate 2: \ all twelve", font_size=20, color=EAR).next_to(line, RIGHT, buff=1.6).shift(UP * 2.0)
        head = label(rf"a row \ (gold) \ and its inversion $I_{{{d['partner_n']}}}$ \ (blue), \ together \ (ours)", font_size=24, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is a row of our own over its combinatorial inversion, one note of each at a time. Each half of the "
            "passage, left and right of the dashed line, contains every one of the twelve pitch classes exactly once "
            "between the two lines. Listen for how evenly the chromatic is filled: no note comes back before all the "
            "others have sounded."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(line), FadeIn(l1), FadeIn(l2))
        with self.listen(c) as snd:
            window(snd, r"two forms, \ two aggregates", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            flash_voices(snd, g, [d["top"], d["bot"]], 0.0, d["unit"], colors=[TUNE, BLUE])
            cursor(snd, g, 0.0, d["unit"])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def six(self):
        d = load("combin")
        cells = VGroup()
        for k, h in enumerate(d["hexachords"]):
            cl = pc_clock(h, radius=0.75, color=TUNE, labels=False)
            cells.add(VGroup(cl, label("ABCDEF"[k] + r": \ (" + " ".join(str(x) for x in h) + ")", font_size=17, color=GREY_A)).arrange(DOWN, buff=0.2))
        cells.arrange_in_grid(rows=2, cols=3, buff=(0.9, 0.45)).move_to(DOWN * 0.3)
        head = label(r"the six all-combinatorial hexachords", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Babbitt found that only six kinds of hexachord map onto their complements under transposition and under "
            "inversion as well; he called them all-combinatorial. The program finds the same six by testing all fifty "
            "hexachord classes. They are the chromatic hexachord, two less familiar shapes, the hexatonic scale "
            "from Part 28, the hexachord of five fifths in a row, and the whole-tone scale. Every one is highly symmetric."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(x) for x in cells], lag_ratio=0.2), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def babbitt(self):
        items = [
            (r"Milton Babbitt, \ 1916--2011, \ Princeton: \ a composer who thought like a mathematician", WHITE),
            (r"`Who cares if you listen?' \ (1958): \ the headline was the editor's; \ Babbitt's title was `The Composer as Specialist'", WHITE),
            (r"his argument: \ advanced music is like advanced science, \ written for specialists", WHITE),
            (r"the RCA synthesizer: \ electronic music specified exactly \ (Part 30)", TUNE),
            (r"the American serial tradition: \ Babbitt, \ Wuorinen, \ the academy", GREY_A),
        ]
        rows_scene(self, r"Babbitt", items,
                   "Babbitt himself was a composer who thought like a mathematician. <bookmark mark='c'/> His most famous "
                   "essay appeared in 1958 under the headline Who cares if you listen?, a title chosen by the magazine's "
                   "editor; his own was The Composer as Specialist. <bookmark mark='d'/> He argued that advanced music, like "
                   "advanced science, is written for specialists. <bookmark mark='e'/> He worked with the RCA synthesizer at "
                   "Princeton and Columbia, which let him specify every sound exactly, as Part 30 will show. "
                   "<bookmark mark='f'/> His influence shaped a whole American academic tradition.", marks="cdef")

    # ------------------------------------------------------------------
    def webern21(self):
        items = [
            (r"Webern, \ Symphony Op. 21 \ (1928): \ a row whose second half is its first half backwards, \ transposed", WHITE),
            (r"so the row is its own retrograde: \ only 24 distinct forms, \ not 48", WHITE),
            (r"the second movement's variations form a palindrome around their middle", WHITE),
            (r"symmetry at every scale: \ interval, \ row, \ movement", TUNE),
            (r"the next generation took Webern, \ not Schoenberg, \ as its model", GREY_A),
        ]
        rows_scene(self, r"Webern's symmetries", items,
                   "Webern pushed symmetry further than anyone. <bookmark mark='b'/> In his Symphony, Opus 21, of 1928, the row's second half is its first half backwards and transposed, <bookmark mark='c'/> so the row is its own retrograde, and has only twenty-four different forms instead of forty-eight. <bookmark mark='d'/> The theme of the second movement's variations reads the same forwards and backwards around its middle. <bookmark mark='e'/> Symmetry at every scale: the interval, the row, the movement. <bookmark mark='f'/> The generation after 1945 took Webern, not Schoenberg, as its model.", marks="cdef")
