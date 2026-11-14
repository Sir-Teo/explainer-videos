from __future__ import annotations

import numpy as np

from videos.music.music33.common import *  # noqa: F403


class Euclid(SoundScene):
    def construct(self):
        chapter(self, 1, r"Euclid's rhythms", r"How do you spread five strokes over thirteen pulses?", extra=((2005, r"Toussaint"),))
        self.process()
        self.gcd()
        self.catalogue()
        self.rotate()
        self.quiz()
        self.rank()

    # ------------------------------------------------------------------
    def process(self):
        d = load("euclid")
        rows_ = VGroup()
        for i, st in enumerate(d["stages"]):
            groups = VGroup(*[label(r"\texttt{" + g + "}", font_size=24, color=TUNE if "x" in g else GREY_B) for g in st]).arrange(RIGHT, buff=0.3)
            rows_.add(VGroup(label(f"step {i}", font_size=18, color=GREY_A), groups).arrange(RIGHT, buff=0.5))
        rows_.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(LEFT * 1.5 + UP * 0.2)
        res = VGroup(label(r"read off:", font_size=20, color=GREY_A), pattern_text(d["result"], size=28, color=TUNE)).arrange(RIGHT, buff=0.4).next_to(rows_, DOWN, buff=0.6, aligned_edge=LEFT)
        g = necklace(d["result"], radius=1.3, color=TUNE).move_to(RIGHT * 4.8 + UP * 0.2)
        head = label(r"Bjorklund's process: \ five strokes in thirteen pulses", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is the process for five strokes in thirteen pulses. Start with five strokes and eight rests. "
            "<bookmark mark='a'/> Tuck one rest behind each stroke: five groups of stroke-rest, and three rests left over. "
            "<bookmark mark='b'/> Tuck the leftovers behind the first three groups: now three groups of three and two of two. "
            "<bookmark mark='c'/> Do it again with the two smaller groups, and stop when one group or none is left over. "
            "<bookmark mark='d'/> Read the groups in order: x dot dot x dot, twice, then x dot dot. The strokes are as evenly "
            "spread as thirteen pulses allow."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("abc", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
            vo.wait_until("d")
            self.play(FadeIn(res), FadeIn(g))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gcd(self):
        rows_ = text_rows([
            (r"Euclid \ (about 300 BCE): \ the greatest common divisor of 13 and 5", WHITE),
            (r"13 \ = \ 2 $\times$ 5 + 3; \ \ 5 \ = \ 1 $\times$ 3 + 2; \ \ 3 \ = \ 1 $\times$ 2 + 1; \ \ 2 \ = \ 2 $\times$ 1", WHITE),
            (r"the group sizes in Bjorklund's steps follow the same remainders: \ 5 and 8, \ 5 and 3, \ 3 and 2, \ 2 and 1", TUNE),
            (r"when k divides n the rhythm is perfectly even; \ otherwise it is as even as it can be", WHITE),
            (r"Toussaint's name for it: \ E(k, n), \ the Euclidean rhythm", GREY_A),
        ], font_size=24)
        head = label(r"why it is Euclid's algorithm", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Why Euclid? <bookmark mark='a'/> His algorithm finds the greatest common divisor of two numbers by repeated "
            "division with remainder: thirteen is two fives and three; five is one three and two; three is one two and one; "
            "two is two ones. <bookmark mark='b'/> The group counts in Bjorklund's steps follow exactly those remainders. "
            "<bookmark mark='c'/> When k divides n the result is perfectly even, like four strokes in sixteen; otherwise it is "
            "as even as the pulses allow. <bookmark mark='d'/> Toussaint wrote it E of k, n: the Euclidean rhythm."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]), FadeIn(rows_[1]))
            for mark, r in zip("bcd", rows_[2:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def catalogue(self):
        d = load("euclid")
        rows_ = VGroup()
        for r in d["table"]:
            rows_.add(VGroup(label(rf"E({r['k']},{r['n']})", font_size=20, color=TUNE), pattern_text(r["pattern"], size=20, color=WHITE),
                             label(r["name"], font_size=19, color=GREY_A)).arrange(RIGHT, buff=0.5))
        for r in rows_:
            r[0].set_x(-5.6)
            r[1].next_to(r[0], RIGHT, buff=0.5)
            r[2].next_to(r[0], RIGHT, buff=4.2)
        rows_.arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(DOWN * 0.3)
        head = label(r"Toussaint's catalogue \ (a selection): \ each a rotation of a Euclidean rhythm", font_size=24, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Toussaint's paper lists dozens of traditional rhythms that are Euclidean, or rotations of Euclidean rhythms, "
            "which means starting the same necklace at a different bead. <bookmark mark='a'/> Here are nine, each checked "
            "by the program against the algorithm's output: the tresillo and the cinquillo of Cuba; Persian and Bulgarian "
            "and Turkish metres of two, three and four strokes; a Venda timeline; the West African bell; bossa nova and a "
            "samba pattern from Brazil. Composers and players found the most even way to spread strokes long before anyone "
            "wrote the algorithm down."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[:2]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows_[2:]], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("euclid")
        c = clip("euclid.quiz")
        card = listen_card(r"Two rhythms of five strokes in eight pulses. \ One is spread as evenly as possible; \ "
                           r"the other is not. \ Which is the Euclidean one, \ A or B?", width=10.4)
        with self.voiceover(
            "A question for your ears. Two rhythms, both with five strokes in eight pulses. One is spread as evenly as "
            "possible; the other bunches its strokes together. Which is the Euclidean one, A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        ga = necklace(d["quiz"]["A"], radius=1.3, color=GREY_A).move_to(LEFT * 3.2 + UP * 0.2)
        gb = necklace(d["quiz"]["B"], radius=1.3, color=GREY_A).move_to(RIGHT * 3.2 + UP * 0.2)
        la = label(r"A", font_size=40, color=GREY_A).next_to(ga, UP, buff=0.3)
        lb = label(r"B", font_size=40, color=GREY_A).next_to(gb, UP, buff=0.3)
        self.play(FadeOut(card), FadeIn(ga), FadeIn(gb), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"Part 11's clave", corner=DL, tag_corner=DR)
            for key, g in (("A", ga), ("B", gb)):
                ons = [i for i, ch in enumerate(d["quiz"][key]) if ch == "x"]
                for cc in range(3):
                    for j, o in enumerate(ons):
                        t0 = d["starts"][key] + (cc * 8 + o) * d["pulse"]
                        pulse(snd, g.dots[j], t0, t0 + d["pulse"] * 0.9, buff=0.04)
        ans = VGroup(label(r"A: \ gaps 1, \ 1, \ 2, \ 2, \ 2", font_size=21, color=GREY_A).next_to(ga, DOWN, buff=0.35),
                     label(r"B: \ gaps 2, \ 1, \ 2, \ 1, \ 2: \ the cinquillo", font_size=21, color=TUNE).next_to(gb, DOWN, buff=0.35))
        with self.voiceover(
            "B is the Euclidean rhythm, the cinquillo: its gaps are two, one, two, one, two, never two short gaps together. "
            "A crowds three strokes into a row and then spaces the rest. On the necklace B's polygon is nearly regular; A's "
            "is lopsided. Many listeners also hear B as livelier; whether evenness predicts how much a rhythm makes people "
            "want to move is a question for Part 46."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rank(self):
        d = load("rank")
        cells = VGroup()
        for i, r in enumerate(d["rows"]):
            g = necklace(r["pattern"], radius=0.62, color=TUNE if r["euclid"] else GREY_B, dot=0.07)
            cells.add(VGroup(g, label(rf"{r['dist']:.2f}", font_size=17, color=TUNE if r["euclid"] else GREY_A)).arrange(DOWN, buff=0.2))
        cells.arrange(RIGHT, buff=0.45).move_to(DOWN * 0.1)
        head = label(rf"all {d['count']} rhythms of 5 strokes in 8 pulses \ (up to rotation), \ most even first", font_size=25, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(r"the number: \ distance from a perfectly even spacing, \ in pulses", font_size=20, color=GREY_A).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            f"How many five-stroke rhythms in eight pulses are there? Counting rotations as the same necklace, "
            f"{say(d['count'])}. Rank them by how far their strokes are from a perfectly even spacing. "
            "<bookmark mark='a'/> The cinquillo comes first, the only Euclidean one; the quiz's lopsided rhythm is second; "
            "and five strokes in a row, then silence, is last. Evenness is a single number, and Euclid's algorithm always "
            "finds the rhythm that minimizes it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells[:2]), FadeIn(cap))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cells[2:]], lag_ratio=0.25), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rotate(self):
        items = [
            (r"a timeline repeats: \ only its necklace is fixed, \ not where you start counting", WHITE),
            (r"E(3, 8) \ = \ x..x..x. \ ; \ started on its second stroke: \ x..x.x.. \ ; \ on its third: \ x.x..x..", WHITE),
            (r"each rotation is heard against the beat differently: \ the downbeat chooses", WHITE),
            (r"so Toussaint's test is `a rotation of E(k, n)', \ not equality", TUNE),
            (r"Part 11's syncopation measure tells the rotations apart", GREY_A),
        ]
        rows_scene(self, r"where does the cycle start?", items,
                   "One subtlety. <bookmark mark='b'/> A timeline repeats, so only its necklace is fixed, not where you start counting. <bookmark mark='c'/> E of three, eight is x dot dot x dot dot x dot; started from its second stroke it is x dot dot x dot x dot dot; from its third, x dot x dot dot x dot dot. <bookmark mark='d'/> Each rotation sits differently against the beat: the downbeat chooses. <bookmark mark='e'/> So Toussaint's test is whether a rhythm is a rotation of a Euclidean one. <bookmark mark='f'/> Part 11's syncopation measure tells the rotations apart.", marks="cdef")
