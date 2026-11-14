from __future__ import annotations

import numpy as np

from videos.music.music26.common import *  # noqa: F403

KN = ["C", r"C$\sharp$", "D", r"E$\flat$", "E", "F", r"F$\sharp$", "G", r"A$\flat$", "A", r"B$\flat$", "B"]
KEY_ROW = {(0, "major"): 0, (7, "major"): 1, (2, "major"): 2, (3, "major"): 3, (7, "minor"): 4, (2, "minor"): 5, (9, "minor"): 6, (0, "minor"): 7}


class Sonata(SoundScene):
    def construct(self):
        chapter(self, 3, r"Sonata form on stage", r"What does a key-finder see in a sonata?", extra=((1793, r"Haydn's Op. 74"),))
        self.plan()
        self.develop()
        self.census()
        self.quiz()
        self.binary()
        self.concerto()
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
    def census(self):
        d = load("keys")
        t = d["tally"]
        vals = [t.get("major|V", 0), t.get("minor|III", 0), t.get("major|other", 0) + t.get("minor|other", 0)]
        bars = columns(vals, [r"to the dominant", r"to the relative major", r"elsewhere"], width=6.4, height=2.6, color=TUNE, hot=(0,), hot_color=BLUE, fmt="{:.0f}", font_size=19)
        bars.move_to(LEFT * 2.9 + DOWN * 0.5)
        head = label(rf"the first new key that holds, \ in {d['agree']} movements", font_size=22, color=GREY_A).next_to(bars, UP, buff=0.4)
        side = VGroup(*[label(s, font_size=22, color=c_) for s, c_ in (
            (rf"major keys: \ {t.get('major|V', 0)} of {d['major']} go to V", BLUE),
            (rf"minor keys: \ {d['minor']} of {d['minor']} go to III", WHITE),
            (r"the rest: \ freer plans", WHITE),
            (rf"{33 - d['agree']} left out: \ start and end disagree", GREY_A))]).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 5.0))
        side.move_to(RIGHT * 3.9 + DOWN * 0.3)
        with self.voiceover(
            "Is that one movement typical? The same tracker reads every movement in the corpus and records the first new "
            "key that holds for two readings running. A movement counts only if the tracker reads the same key in its "
            f"first eight bars and its last, so that we can trust what home is: {say(d['agree'])} of the thirty-three. "
            f"<bookmark mark='a'/> Of the {say(d['major'])} in major keys, {say(t.get('major|V', 0))} go first to the "
            "dominant, a fifth up. <bookmark mark='b'/> Both minor-key movements go to the relative major, the key a minor "
            "third up with the same key signature. <bookmark mark='c'/> The others, mostly slow movements and finales, have "
            "freer plans. <bookmark mark='d'/> The movements left out are a warning: on a third of the corpus the tracker "
            "cannot even agree with itself about home, and one of them is a joke of Beethoven's that chapter six will hear."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bars))
            for mark, r in zip("abcd", side):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def develop(self):
        d = load("develop")
        c = clip("plan.development")
        vs = d["voices"]
        g = voices_roll(vs, width=11.4, height=3.4, colors=[TUNE, BLUE, EAR, GREY_A], bar_h=0.11).move_to(DOWN * 0.3)
        head = label(r"Haydn, \ Op. 74 No. 1: \ bars 61 to 68, \ the development", font_size=24, color=GREY_A).to_edge(UP, buff=0.9)
        cap = label(r"the key-finder: \ G minor, \ then D minor: \ away from home, \ and unsettled", font_size=21, color=EAR).next_to(g, DOWN, buff=0.3)
        with self.voiceover(
            "Here is a stretch of the development, bars sixty-one to sixty-eight, where the key-finder reads G minor turning "
            "to D minor. Listen for how unsettled it is: short fragments, passed between instruments, never staying long "
            "enough to feel like home."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"the development", detail=r"from the encoding, \ Part 7's bowed string", corner=DL, tag_corner=DR)
            flash_voices(snd, g, vs, 0.0, d["unit"], colors=[TUNE, BLUE, EAR, GREY_A])
            cursor(snd, g, 0.0, d["unit"])
        self.wait(0.3)
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

    # ------------------------------------------------------------------
    def concerto(self):
        items = [
            (r"Mozart's piano concertos, \ Vienna, \ 1784--1786: \ a dozen masterpieces in three years", WHITE),
            (r"a double exposition: \ the orchestra states the themes at home; \ the soloist restates them and modulates", WHITE),
            (r"the ritornello of Part 25 survives as the orchestra's sections", WHITE),
            (r"a cadenza before the end: \ the soloist improvises on the themes over a held chord", TUNE),
            (r"the concerto as drama: \ an individual against a group", GREY_A),
        ]
        rows_scene(self, r"the concerto, Classical", items,
                   "The concerto took on the form too. <bookmark mark='b'/> Mozart wrote a dozen piano concertos for his own concerts in Vienna between 1784 and 1786. <bookmark mark='c'/> Their first movements have a double exposition: the orchestra states the themes, staying at home, and then the soloist enters and restates them, this time making the move to the new key. <bookmark mark='d'/> The orchestral passages are what remains of Part 25's ritornello. <bookmark mark='e'/> Near the end the orchestra stops on a held chord and the soloist improvises a cadenza on the themes. <bookmark mark='f'/> It is sonata form as a drama between an individual and a group.", marks="cdef")

    # ------------------------------------------------------------------
    def binary(self):
        items = [
            (r"Part 25's binary dance: \ $\|{:}$ home $\to$ away ${:}\|{:}$ away $\to$ home ${:}\|$", WHITE),
            (r"the `rounded' binary: \ the opening returns in the second half, \ at home", WHITE),
            (r"grow the second half's opening into a development, \ the return into a recapitulation", TUNE),
            (r"the repeat signs survive: \ the exposition is repeated, \ and often the rest", WHITE),
            (r"sonata form is a binary form that learned to tell a story", GREY_A),
        ]
        rows_scene(self, r"where sonata form came from", items,
                   "Where did the form come from? <bookmark mark='b'/> From Part 25's binary dance, whose first half goes from home to away and whose second half comes back, each half repeated. <bookmark mark='c'/> In the rounded binary, the opening music returns, at home, partway through the second half. <bookmark mark='d'/> Expand the start of that second half into a development, and the return into a full recapitulation, and you have sonata form. <bookmark mark='e'/> The repeat signs survive: the exposition is repeated, and in many early movements so is the rest. <bookmark mark='f'/> Sonata form is a binary form that learned to tell a story.", marks="cdef")
