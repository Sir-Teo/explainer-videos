from __future__ import annotations

import numpy as np

from videos.music.music26.common import *  # noqa: F403

KN = ["C", r"C$\sharp$", "D", r"E$\flat$", "E", "F", r"F$\sharp$", "G", r"A$\flat$", "A", r"B$\flat$", "B"]
KEY_ROW = {(0, "major"): 0, (7, "major"): 1, (2, "major"): 2, (3, "major"): 3, (7, "minor"): 4, (2, "minor"): 5, (9, "minor"): 6, (0, "minor"): 7}


class Sonata(SoundScene):
    def construct(self):
        chapter(self, 3, r"Sonata form on stage", r"What does a key-finder see in a sonata?", extra=((1793, r"Haydn's Op. 74"),))
        self.plan()
        self.quiz()
        self.drama()

    # ------------------------------------------------------------------
    def plan(self):
        d = load("plan")
        T = d["bars"]
        x0, W, y0 = -5.6, 11.2, 1.6
        rows_k = sorted({(k[0], k[1]) for k in (tuple(t["key"]) for t in d["plan"])}, key=lambda k: KEY_ROW.get(k, 9))
        idx = {k: i for i, k in enumerate(rows_k)}
        labs_ = VGroup()
        for k, i in idx.items():
            labs_.add(label(KN[k[0]] + (" major" if k[1] == "major" else " minor"), font_size=18, color=GREY_A).move_to([x0 - 0.9, y0 - 0.45 * i, 0]))
        cells = VGroup()
        for t in d["plan"]:
            k = tuple(t["key"])
            i = idx[k]
            col = TUNE if k == (0, "major") else (BLUE if k == (7, "major") else EAR)
            cells.add(Rectangle(width=W * 2 / T, height=0.3, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to([x0 + W * (t["bar"] + 1) / T, y0 - 0.45 * i, 0]))
        spans = VGroup()
        for name, a, b, col in ((r"exposition", 0, 54, TUNE), (r"development", 54, 90, EAR), (r"recapitulation", 90, T, TUNE)):
            spans.add(VGroup(Line([x0 + W * a / T, -2.0, 0], [x0 + W * b / T, -2.0, 0], color=col, stroke_width=5),
                             label(name, font_size=19, color=col).move_to([x0 + W * (a + b) / 2 / T, -2.35, 0])))
        head = label(rf"Haydn, \ Op. 74 No. 1, \ first movement \ ({T} bars): \ the key of every eight bars", font_size=24, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Sonata form is a drama of keys, and a key-finder can watch it. Part 15's key-finder reads Haydn's String "
            "Quartet Opus 74 Number 1, first movement, eight bars at a time, all four instruments together. "
            "<bookmark mark='a'/> It begins in C major. Within twenty bars it has moved to G, the dominant, and stays "
            "there to the end of the first section: the exposition, with its second group in the new key. "
            "<bookmark mark='b'/> Then the development wanders: G minor, E flat, D minor, A minor, keys related to the "
            "home key but not the home key. <bookmark mark='c'/> And at about bar ninety C major returns and holds, with "
            "only brief excursions, to the end: the recapitulation, where the music of the second group comes back, now "
            "at home. The program knows nothing about themes; the plan is visible in the keys alone."
        ) as vo:
            self.play(FadeIn(head), FadeIn(labs_))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cells[: len(cells) * 54 // T]], lag_ratio=0.05), FadeIn(spans[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cells[len(cells) * 54 // T: len(cells) * 90 // T]], lag_ratio=0.05), FadeIn(spans[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cells[len(cells) * 90 // T:]], lag_ratio=0.05), FadeIn(spans[2]), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("plan")
        c = clip("plan.quiz")
        card = listen_card(r"Six bars from the exposition \ (in G), \ and six from the recapitulation \ (at home, \ in C), \ in some order. \ "
                           r"Which is the recapitulation, \ A or B? \ Listen for which one sounds like arriving home.", width=10.6)
        with self.voiceover(
            "Listen for the difference. Six bars from the exposition, in G, and six from the recapitulation, at home in C, "
            "in some order. Which is the recapitulation, A or B? Listen for which one sounds like home."
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        gA = voices_roll(d["A"], width=5.4, height=2.8, colors=[TUNE, BLUE, EAR, GREY_A], bar_h=0.1).move_to(LEFT * 3.3 + DOWN * 0.2)
        gB = voices_roll(d["B"], width=5.4, height=2.8, colors=[TUNE, BLUE, EAR, GREY_A], bar_h=0.1).move_to(RIGHT * 3.3 + DOWN * 0.2)
        la = label(r"A", font_size=40, color=GREY_A).next_to(gA, UP, buff=0.3)
        lb = label(r"B", font_size=40, color=GREY_A).next_to(gB, UP, buff=0.3)
        self.play(FadeOut(card), FadeIn(gA), FadeIn(gB), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"from the encoding, \ Part 7's bowed string", corner=DL, tag_corner=DR)
            flash_voices(snd, gA, d["A"], d["starts"]["A"], d["unit"], colors=[TUNE, BLUE, EAR, GREY_A])
            flash_voices(snd, gB, d["B"], d["starts"]["B"], d["unit"], colors=[TUNE, BLUE, EAR, GREY_A])
            pulse(snd, la, d["starts"]["A"], d["starts"]["B"] - 0.5, buff=0.1)
            pulse(snd, lb, d["starts"]["B"], c.duration, buff=0.1)
        ans = VGroup(label(rf"bar {d['exp_bar']:.0f}: \ in G", font_size=22, color=BLUE).next_to(gA, DOWN, buff=0.35),
                     label(rf"bar {d['rec_bar']:.0f}: \ in C, \ home", font_size=22, color=TUNE).next_to(gB, DOWN, buff=0.35))
        with self.voiceover(
            f"B, from bar {say(round(d['rec_bar']))}, is the recapitulation, in C. A, from bar {say(round(d['exp_bar']))}, "
            "is in G. Out of context the difference is subtle; in the movement, after a development that has avoided C, the "
            "return is unmistakable. That is the point of the form."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def drama(self):
        items = [
            (r"exposition: \ two key areas, \ home and away, \ the move between them dramatized", WHITE),
            (r"development: \ fragments of the themes through distant keys", WHITE),
            (r"recapitulation: \ everything returns, \ the second group now at home: \ the tension resolved", TUNE),
            (r"the `textbook' description \ (Marx, \ 1845) \ came after the music, \ from Beethoven", WHITE),
            (r"Hepokoski and Darcy \ (2006): \ a set of expected moves, \ each met, \ delayed or refused \ (Part 21)", GREY_A),
        ]
        rows_scene(self, r"a drama of keys", items,
                   "Put in words, the form is a drama. <bookmark mark='b'/> The exposition sets up two key areas, home and "
                   "away, and dramatizes the move between them. <bookmark mark='c'/> The development takes fragments of the "
                   "themes through distant keys. <bookmark mark='d'/> The recapitulation brings everything back, with the "
                   "second group now at home, and the tension of the exposition is resolved. <bookmark mark='e'/> This "
                   "textbook account was written down in the 1840s, by Adolf Bernhard Marx, mostly from Beethoven, long "
                   "after Haydn and Mozart had written the music. <bookmark mark='f'/> Modern theory, as Part 21 said, "
                   "treats the form as a set of expected moves that a composer meets, delays or refuses.", marks="cdef")
