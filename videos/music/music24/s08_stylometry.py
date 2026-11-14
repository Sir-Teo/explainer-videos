from __future__ import annotations

import numpy as np

from videos.music.music24.common import *  # noqa: F403

FEAT_NAME = {"free": r"free dissonance", "passing": r"passing notes", "suspension": r"suspensions", "neighbour": r"neighbour notes",
             "leap_share": r"leaps", "recovered": r"leaps turned back", "forbidden": r"forbidden intervals", "third": r"sonorities with a third",
             "triad": r"full triads", "step_share": r"steps", "rest_share": r"rests", "note_len": r"note length"}


class Stylometry(SoundScene):
    def construct(self):
        chapter(self, 7, r"Who wrote this? \ A statistical answer", r"Can twelve numbers recognize a composer?")
        self.method()
        self.picture()
        self.composers()
        self.books()
        self.quiz()

    # ------------------------------------------------------------------
    def method(self):
        items = [
            (r"describe each piece by twelve numbers: \ how it treats dissonance, \ its leaps, \ its sonorities, \ its rhythm", WHITE),
            (r"standardize them; \ average each composer's pieces: \ a centroid", WHITE),
            (r"a new piece is given to the composer whose centroid is nearest", WHITE),
            (r"leave one out: \ hide each piece in turn, \ train on the rest, \ and test it", TUNE),
            (r"the honest number is the accuracy on pieces the method has not seen", GREY_A),
        ]
        rows_scene(self, r"a nearest-centroid test", items,
                   "Here is the simplest statistical test of authorship. <bookmark mark='b'/> Describe each piece by twelve "
                   "numbers: the shares of its dissonances treated each way, how often it leaps and how it recovers, how "
                   "many of its sonorities have thirds, how long its notes are. <bookmark mark='c'/> Put the numbers on a "
                   "common scale and average each composer's pieces into a single point, a centroid. "
                   "<bookmark mark='d'/> Give a new piece to the composer whose centroid is nearest. <bookmark mark='e'/> "
                   "And test it honestly: hide each piece in turn, build the centroids from all the others, and see "
                   "whether the hidden one is recognized. <bookmark mark='f'/> The accuracy on pieces the method has not "
                   "seen is the only number worth reporting.", marks="bcdef")

    # ------------------------------------------------------------------
    def picture(self):
        s = load("style")
        pts = s["scatter"]
        ax = Axes(x_range=[0, 0.8, 0.2], y_range=[0, 0.6, 0.2], x_length=6.6, y_length=4.2, tips=False,
                  axis_config={"color": GREY_B, "stroke_width": 1.5, "include_numbers": True, "font_size": 18}).move_to(LEFT * 2.2 + DOWN * 0.3)
        xl = label(r"share of free dissonance", font_size=19, color=GREY_A).next_to(ax, DOWN, buff=0.35)
        yl = label(r"share of suspensions", font_size=19, color=GREY_A).rotate(PI / 2).next_to(ax, LEFT, buff=0.45)
        dots = VGroup(*[Dot(ax.c2p(min(x, 0.79), min(y, 0.59)), radius=0.055, color=TUNE if lab == "Palestrina" else EAR, fill_opacity=0.85) for x, y, lab in pts])
        cen = VGroup()
        for lab, col in (("Palestrina", TUNE), ("Monteverdi", EAR)):
            xs = [x for x, y, l in pts if l == lab]
            ys = [y for x, y, l in pts if l == lab]
            cen.add(VGroup(Cross(stroke_color=WHITE, stroke_width=4).scale(0.13).move_to(ax.c2p(np.mean(xs), np.mean(ys))),
                           label(lab, font_size=20, color=col).next_to(ax.c2p(np.mean(xs), np.mean(ys)), UR, buff=0.1)))
        side = VGroup(*[label(t, font_size=21, color=c_) for t, c_ in (
            (r"each dot: \ one piece, \ two of its twelve numbers", WHITE),
            (r"crosses: \ the centroids", WHITE),
            (r"in twelve dimensions the same idea: \ the nearest cross wins", TUNE),
            (r"each number first rescaled \ (mean 0, \ spread 1), \ so no one feature dominates", GREY_A))]).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 4.6))
        side.move_to(RIGHT * 4.3 + DOWN * 0.2)
        with self.voiceover(
            "Two of the twelve numbers can be drawn. <bookmark mark='a'/> Each dot is one piece: across, its share of "
            "free dissonance; up, its share of suspensions. Palestrina's movements, in gold, sit in a tight cloud at the "
            "upper left: many suspensions, almost no free dissonance. Monteverdi's madrigals, in pink, spread out to the "
            "right and down. <bookmark mark='b'/> The crosses are the two centroids. <bookmark mark='c'/> With all twelve "
            "numbers the picture has twelve dimensions, but the rule is the same: a hidden piece goes to the nearest "
            "cross. <bookmark mark='d'/> Each number is first rescaled to a common spread, so that a feature measured in "
            "large units cannot outvote the others."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.01), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(cen), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def composers(self):
        s = load("style")["composer"]
        conf = s["confusion"]
        w = sorted(s["weights"].items(), key=lambda x: -abs(x[1]))[:5]
        tab = VGroup()
        hdr = VGroup(label(r"", font_size=20), label(r"called Palestrina", font_size=20, color=GREY_A), label(r"called Monteverdi", font_size=20, color=GREY_A))
        tab.add(hdr)
        for who in ("Palestrina", "Monteverdi"):
            tab.add(VGroup(label(who, font_size=22, color=TUNE if who == "Palestrina" else EAR), label(rf"{conf[who]['Palestrina']}", font_size=24, color=WHITE),
                           label(rf"{conf[who]['Monteverdi']}", font_size=24, color=WHITE)))
        for i, row in enumerate(tab):
            for k, cell in enumerate(row):
                cell.move_to([[-5.0, -2.4, 0.3][k], 1.4 - 0.6 * i, 0])
        acc = label(rf"right on {100 * s['accuracy']:.0f} in 100 of {s['n']} hidden pieces", font_size=24, color=TUNE).move_to([-2.6, -0.6, 0])
        side = VGroup(label(r"what separates them most \ (Monteverdi minus Palestrina)", font_size=19, color=GREY_A),
                      *[label(rf"{FEAT_NAME[k]}: \ {'$+$' if v > 0 else '$-$'}{abs(v):.1f}", font_size=21, color=WHITE) for k, v in w]).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        side.move_to(RIGHT * 3.6 + UP * 0.2)
        cap = label(r"but these are Masses against madrigals, \ two encodings, \ two genres: \ the test may be hearing the genre", font_size=21, color=EAR).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            f"First, Palestrina against Monteverdi: {say(s['n'] // 2)} of Palestrina's movements chosen at random, and all "
            f"{say(s['n'] // 2)} of Monteverdi's madrigals in the corpus. <bookmark mark='a'/> Hidden one at a time, the "
            f"pieces are recognized {say(round(100 * s['accuracy']))} times in a hundred: every Palestrina movement, and "
            f"{say(conf['Monteverdi']['Monteverdi'])} of the {say(s['n'] // 2)} madrigals. <bookmark mark='b'/> What "
            "decides it: Monteverdi's note values are shorter, he uses fewer suspensions and more free dissonance, more "
            "forbidden intervals, and fewer leaps turned back. <bookmark mark='c'/> Do not be impressed yet. This "
            "compares Latin Masses with Italian madrigals, from two different encodings, half a century apart in style. "
            "A test this easy may be recognizing the genre, or the encoder, not the composer."
        ) as vo:
            self.play(FadeIn(tab))
            vo.wait_until("a")
            self.play(FadeIn(acc))
            vo.wait_until("b")
            self.play(FadeIn(side))
            vo.wait_until("c")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def books(self):
        s = load("style")["books"]
        conf = s["confusion"]
        rows_ = text_rows([
            (r"a harder test: \ one composer, \ one genre, \ one encoding: \ Monteverdi's Book 3 \ (1592) \ against Books 4 and 5 \ (1603, \ 1605)", WHITE),
            (rf"twelve numbers: \ right on {100 * s['accuracy']:.0f} in 100 \ ({conf['Book 3']['Book 3']} of 20 and {conf['Books 4-5']['Books 4-5']} of 28)", WHITE),
            (rf"one number alone, \ the share of free dissonance: \ {100 * s['one_feature']:.0f} in 100", TUNE),
            (rf"\textit{{Cruda Amarilli}}, \ hidden: \ placed with the later books", EAR),
            (r"with forty-eight pieces, \ a difference of a few pieces is noise: \ these are rough numbers", GREY_A),
        ])
        head = label(r"one composer, \ two decades", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A harder and fairer test keeps the composer, the genre and the encoding fixed and asks about time. "
            "<bookmark mark='a'/> Can the numbers tell Monteverdi's third book of madrigals, from 1592, from his fourth "
            f"and fifth, from 1603 and 1605? <bookmark mark='b'/> With all twelve numbers, {say(round(100 * s['accuracy']))} "
            "times in a hundred: better than a coin, far from certain. <bookmark mark='c'/> One number alone, the share "
            f"of free dissonance, gets {say(round(100 * s['one_feature']))}. <bookmark mark='d'/> And the madrigal that "
            "started a famous quarrel, Cruda Amarilli, when hidden, is placed with the later books. "
            "<bookmark mark='e'/> With forty-eight pieces, a few pieces either way is noise; these are rough numbers, and "
            "an attribution built on them alone would be irresponsible."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("quiz")
        c = clip("style.quiz")
        card = listen_card(r"Two excerpts: \ one from a Mass by Palestrina, \ one from a madrigal by Monteverdi. \ "
                           r"Which is Palestrina, \ A or B? \ Listen for the dissonances: \ how are they approached?", width=10.6)
        with self.voiceover(
            "Now be the classifier yourself. Two excerpts: one from a Palestrina Mass, one from a Monteverdi madrigal. "
            "Which is Palestrina, A or B? Listen for the dissonances, and how they arrive."
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        gA = voices_roll(d["A"]["voices"], width=5.4, height=2.8, colors=[TUNE, BLUE, EAR, GREY_A, GREY_B], bar_h=0.1).move_to(LEFT * 3.3 + DOWN * 0.2)
        gB = voices_roll(d["B"]["voices"], width=5.4, height=2.8, colors=[TUNE, BLUE, EAR, GREY_A, GREY_B], bar_h=0.1).move_to(RIGHT * 3.3 + DOWN * 0.2)
        la = label(r"A", font_size=40, color=GREY_A).next_to(gA, UP, buff=0.35)
        lb = label(r"B", font_size=40, color=GREY_A).next_to(gB, UP, buff=0.35)
        self.play(FadeOut(card), FadeIn(gA), FadeIn(gB), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"from the encodings, \ synthetic voices", kind="synthesized", corner=DL, tag_corner=DR)
            flash_voices(snd, gA, d["A"]["voices"], d["starts"]["A"], d["A"]["quarter"], colors=[TUNE, BLUE, EAR, GREY_A, GREY_B])
            flash_voices(snd, gB, d["B"]["voices"], d["starts"]["B"], d["B"]["quarter"], colors=[TUNE, BLUE, EAR, GREY_A, GREY_B])
            pulse(snd, la, d["starts"]["A"], d["starts"]["B"] - 0.5, buff=0.1)
            pulse(snd, lb, d["starts"]["B"], c.duration, buff=0.1)
        marks = VGroup()
        for j, t in d["A"]["marks"]:
            x = gA.frame.get_left()[0] + gA.frame.width * t / gA.total
            marks.add(Triangle(color=RED, fill_opacity=1, stroke_width=0).scale(0.07).rotate(PI).move_to([x, gA.frame.get_top()[1] + 0.12, 0]))
        ans = VGroup(label(rf"Monteverdi: \ {d['A']['free']} free dissonances in four bars", font_size=21, color=EAR).next_to(gA, DOWN, buff=0.35),
                     label(rf"Palestrina: \ {d['B']['free']}", font_size=21, color=TUNE).next_to(gB, DOWN, buff=0.35))
        with self.voiceover(
            f"B is Palestrina: in its four bars the program finds {say(d['B']['free'])} free dissonances. A is "
            f"Monteverdi's fourth book: {say(d['A']['free'])} in four bars, marked in red, chosen as the densest four bars "
            "the program could find. The ear and the census agree; but notice that the excerpt was chosen to make the "
            "point, which is exactly the kind of choice an honest test must not make."
        ):
            self.play(FadeIn(marks), FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()
