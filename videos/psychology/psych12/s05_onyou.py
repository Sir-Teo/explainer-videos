from __future__ import annotations

import numpy as np

from videos.psychology.psych12.common import *  # noqa: F403


class OnYou(VoiceoverScene):
    def construct(self):
        self.card()
        self.study()
        self.test()
        self.answers()
        self.score()

    def card(self):
        card = chapter_card(4, r"On you: \ old or new?", r"How good is your memory, \ once your caution is taken out?",
                            lit=(), part=PART, scale=("person",), marr=("what",))
        with self.voiceover(
            "Chapter four. On you: old or new?"
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def study(self):
        d = load("onyou")
        stage = demo_stage(12.0, 5.6, r"On you: \ twelve words to remember", center=[0, -0.2, 0])
        c = stage.box.get_center()
        note_ = label(r"Read each word. \ Try to remember it.", font_size=30, color=P.ACCENT).move_to(stage.box.get_top() + DOWN * 0.7)
        with self.voiceover(
            "Your turn again, and this time it's memory. Twelve words, one at a time. Just read each one and "
            "try to remember it."
        ):
            self.play(FadeIn(stage), FadeIn(note_))
        for w in d["old"]:
            word = label(w, font_size=64, color=WHITE).move_to(c + DOWN * 0.2)
            self.play(FadeIn(word), run_time=0.25)
            self.wait(1.1)
            self.play(FadeOut(word), run_time=0.2)
        self.clear_scene()

    def test(self):
        d = load("onyou")
        stage = demo_stage(12.0, 5.6, r"On you: \ old or new?", center=[0, -0.2, 0])
        c = stage.box.get_center()
        note_ = label(r"For each word, \ write: \ old or new", font_size=30, color=P.ACCENT).move_to(stage.box.get_top() + DOWN * 0.7)
        with self.voiceover(
            "Now twenty-four words. Half were on the list, half are new. For each one, write down old or new. "
            "If you're not sure, guess, and you can mark the guesses with a question mark. Number one."
        ):
            self.play(FadeIn(stage), FadeIn(note_))
        for i, w in enumerate(d["test"]):
            word = label(w, font_size=60, color=WHITE).move_to(c + DOWN * 0.2)
            num = label(rf"{i + 1}", font_size=34, color=GREY_A).move_to(c + np.array([-5.2, 1.7, 0]))
            ring = countdown_ring(0.32).move_to(c + np.array([5.2, 1.7, 0]))
            self.play(FadeIn(word), FadeIn(num), run_time=0.25)
            self.add(ring)
            self.play(ring.t.animate.set_value(0.0), run_time=2.2, rate_func=linear)
            self.remove(ring)
            self.play(FadeOut(word), FadeOut(num), run_time=0.2)
        self.clear_scene()

    def answers(self):
        d = load("onyou")
        head = heading(r"The answers")
        cols = VGroup()
        for i, (w, old) in enumerate(zip(d["test"], d["is_old"])):
            r, col = i % 12, i // 12
            g = VGroup(label(rf"{i + 1}", font_size=23, color=GREY_A),
                       label(w, font_size=25, color=WHITE),
                       label(r"old" if old else r"new", font_size=25, color=SIGNALC if old else NOISEC))
            g[0].move_to([col * 4.2 - 5.8, 2.35 - 0.42 * r, 0])
            g[1].move_to([col * 4.2 - 4.4, 2.35 - 0.42 * r, 0])
            g[2].move_to([col * 4.2 - 2.9, 2.35 - 0.42 * r, 0])
            cols.add(g)
        rows = rows_of([
            (r"your hits: \ old words you called old, \ out of 12", HIT),
            (r"your false alarms: \ new words you called old, \ out of 12", FA),
        ], 4.0, 27, 0.3).move_to([4.6, 0.6, 0])
        with self.voiceover(
            "Here are the answers. <bookmark mark='a'/> Count two things. Your hits: the old words you called "
            "old, out of twelve. <bookmark mark='b'/> And your false alarms: the new words you called old, also "
            "out of twelve. Pause the video if you need a moment."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(g) for g in cols], lag_ratio=0.05), run_time=3.0)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
        self.wait(3.0)
        self.clear_scene()

    def score(self):
        d = load("onyou")
        head = heading(r"Your $d'$, \ from your two counts")
        hits = list(range(6, 13))
        fas = list(range(0, 7))
        grid = VGroup()
        for r, h in enumerate(hits[::-1]):
            for c_, f in enumerate(fas):
                v = d["dtable"][h][f]
                col = interpolate_color(ManimColor("#1b2430"), ManimColor(MODEL), float(np.clip(v / 3.6, 0, 1)))
                sq = Square(side_length=0.62, stroke_width=1, stroke_color=GREY_D, fill_color=col, fill_opacity=1)
                sq.move_to([c_ * 0.62, -r * 0.62, 0])
                grid.add(VGroup(sq, label(f"{v:.1f}", font_size=19, color=WHITE).move_to(sq)))
        rl = VGroup(*[label(str(h), font_size=21, color=HIT).next_to(grid[r * 7][0], LEFT, buff=0.12) for r, h in enumerate(hits[::-1])])
        cl = VGroup(*[label(str(f), font_size=21, color=FA).next_to(grid[(len(hits) - 1) * 7 + c_][0], DOWN, buff=0.12)
                      for c_, f in enumerate(fas)])
        tl = label(r"hits (of 12)", font_size=23, color=HIT).rotate(PI / 2).next_to(rl, LEFT, buff=0.15)
        bl = label(r"false alarms (of 12)", font_size=23, color=FA).next_to(cl, DOWN, buff=0.15)
        table = VGroup(grid, rl, cl, tl, bl).move_to([-3.2, -0.1, 0])
        eh, ef = d["example_hits"], d["example_fas"]
        mark = SurroundingRectangle(grid[(12 - eh) * 7 + ef], color=YOU, buff=0.03, stroke_width=4)
        rows = rows_of([
            (rf"for example: \ {eh} hits and {ef} false alarms give $d' = {d['example_d']:.1f}$", YOU),
            (r"a cautious memory (few old answers) and a liberal one can have the same $d'$", CRIT),
            (r"rates of 0 or 1 have no $z$ score: \ the table uses $(k + \tfrac12)/(n + 1)$", GREY_A),
            (r"twelve and twelve is a small test: \ one standard error of your $d'$ is about $0.6$", GREY_A),
            (r"the course site runs the full version, \ with confidence ratings, \ and draws your ROC", THRESH),
        ], 5.0, 26, 0.26).move_to([4.2, -0.1, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ the log-linear correction")
        with self.voiceover(
            "Now find your hits down the side and your false alarms along the bottom. The cell is your d prime. "
            f"<bookmark mark='a'/> For example, {eh} hits and {ef} false alarms give d prime of about "
            f"{d['example_d']:.1f}. <bookmark mark='b'/> Notice what the table does. Someone who calls almost "
            "everything new, and someone who calls almost everything old, can come out with the same memory. Their "
            "caution differs, and the table takes it out. <bookmark mark='c'/> A perfect score of twelve has no z "
            "score, because the normal quantile of one is infinite, so the table adds a half to every count and one "
            "to every total. <bookmark mark='d'/> And twelve trials of each kind is a small test: your d prime is "
            "uncertain by about point six, one standard error. <bookmark mark='e'/> The course site has the full version, "
            "with confidence ratings, and it draws your own ROC."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(table))
            vo.wait_until("a")
            self.play(Create(mark), FadeIn(rows[0]))
            for m, r in zip("bcde", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r))
        self.clear_scene()
