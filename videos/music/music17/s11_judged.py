from __future__ import annotations

import numpy as np

from videos.music.music17.common import *  # noqa: F403


class Judged(SoundScene):
    def construct(self):
        chapter(self, 10, r"Ours against Bach", r"How close does the search come, \ on tunes it never saw?")
        self.split()
        self.table()
        self.quiz()

    # ------------------------------------------------------------------
    def split(self):
        e = load("evaluation")
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (rf"train: \ {e['train']} chorales", WHITE),
            (rf"test: \ {e['test']} chorales, \ {e['beats']:,} beats".replace(",", "{,}"), WHITE),
            (r"split by tune: \ no test tune appears in training, \ in any of Bach's settings", TUNE),
            (r"the hook's tune is in the test set", GREY_A))]).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"a fair test", font_size=32, color=GREY_A).to_edge(UP, buff=0.5)
        with self.voiceover(
            "A harmonizer that has seen a tune has seen its answer. So the chorales are split by tune: "
            f"<bookmark mark='a'/> {say(e['train'])} chorales to learn from, and {say(e['test'])} to test on, "
            "with every setting of a tune on the same side of the split. <bookmark mark='b'/> The Passion "
            "Chorale, all eleven settings, is in the test set; the model never heard it. On each test "
            "chorale the search harmonizes Bach's tune, and its answer is compared with Bach's, beat by beat."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]), FadeIn(rows_[1]))
            vo.wait_until("a")
            self.play(FadeIn(rows_[2]))
            vo.wait_until("b")
            self.play(FadeIn(rows_[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        e = load("evaluation")
        f, p, b = e["full"], e["plain"], e["bach"]
        cols = [r"the chord-chooser", r"the search", r"Bach"]
        rows_ = [(r"same chord as Bach", f"{100 * p['same_chord']:.0f}\\%", f"{100 * f['same_chord']:.0f}\\%", r"--"),
                 (r"same bass note as Bach", f"{100 * p['same_bass']:.0f}\\%", f"{100 * f['same_bass']:.0f}\\%", r"--"),
                 (r"parallel fifths and octaves", f"{p['parallels']}", f"{f['parallels']}", f"{b['parallels']}"),
                 (r"hidden fifths and octaves", f"{p['hidden']}", f"{f['hidden']}", f"{b['hidden']}"),
                 (r"alto and tenor motion, \ semitones a beat", f"{p['inner_motion']:.1f}", f"{f['inner_motion']:.1f}", f"{b['inner_motion']:.1f}")]
        xs = (-1.0, 1.4, 3.6, 5.6)
        g = VGroup()
        for j, c_ in enumerate(cols):
            g.add(label(c_, font_size=22, color=GREY_A).move_to([xs[j + 1], 2.4, 0]))
        for k, r in enumerate(rows_):
            y = 1.6 - 0.75 * k
            g.add(label(r[0], font_size=24, color=WHITE).move_to([xs[0], y, 0], aligned_edge=RIGHT))
            for j in range(3):
                col = TUNE if j == 1 else (GREY_B if j == 2 else WHITE)
                g.add(label(r[j + 1], font_size=26, color=col).move_to([xs[j + 1], y, 0]))
        g.move_to(DOWN * 0.1)
        foot = label(rf"on {e['test']} chorales never seen in training", font_size=22, color=GREY_B).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Here is the result, for the plain chord-chooser of the hook and for the full search. "
            f"<bookmark mark='a'/> Both choose Bach's own chord on about {say(round(100 * f['same_chord']))} "
            "beats in a hundred. That sounds low, but chapter one showed that Bach himself sets one tune in "
            "different ways; there is no single right answer to match. The search finds Bach's bass note "
            f"more often, {say(round(100 * f['same_bass']))} times in a hundred against "
            f"{say(round(100 * p['same_bass']))}. <bookmark mark='b'/> The real difference is in the rules. "
            f"The chord-chooser writes {say(p['parallels'])} parallel fifths and octaves on these chorales; "
            f"Bach writes {say(b['parallels'])}; the search writes none. <bookmark mark='c'/> And the last "
            f"row is where the search falls short: its inner voices move {say(f['inner_motion'], 1)} "
            f"semitones a beat, Bach's {say(b['inner_motion'], 1)}. It plays safe, keeping notes still "
            "where Bach's singers move."
        ) as vo:
            self.play(FadeIn(g[:3]), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(g[3:11]))
            vo.wait_until("b")
            self.play(FadeIn(g[11:19]))
            vo.wait_until("c")
            self.play(FadeIn(g[19:]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        e = load("evaluation")
        q = e["quiz"]
        c = clip("evaluation.quiz")
        card = listen_card(r"The Passion Chorale's third and fourth phrases, \ harmonized twice: \ once by the search, \ once by Bach. \ Which is Bach's: \ A or B?", width=10.0)
        with self.voiceover(
            "Now judge by ear. The Passion Chorale's next two phrases, harmonized twice, once by the search "
            "and once by Bach, in an order you do not know. Which is Bach's, A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        gA = choir_roll(q["A"], width=5.6, height=3.2, lo=38, hi=80, thick=0.11).move_to(LEFT * 3.3 + DOWN * 0.2)
        gB = choir_roll(q["B"], width=5.6, height=3.2, lo=38, hi=80, thick=0.11).move_to(RIGHT * 3.3 + DOWN * 0.2)
        la = label(r"A", font_size=40, color=GREY_A).next_to(gA, UP, buff=0.3)
        lb = label(r"B", font_size=40, color=GREY_A).next_to(gB, UP, buff=0.3)
        self.play(FadeOut(card), FadeIn(gA), FadeIn(gB), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", kind="synthesized", detail=r"a model choir", corner=DL, tag_corner=DR)
            sing_roll(snd, gA, q["times"]["A"], start=q["starts"]["A"])
            sing_roll(snd, gB, q["times"]["B"], start=q["starts"]["B"])
            pulse(snd, la, q["starts"]["A"], q["starts"]["B"] - 0.5, buff=0.1)
            pulse(snd, lb, q["starts"]["B"], c.duration, buff=0.1)
        ans = VGroup(label(r"the search: \ correct, \ and still", font_size=24, color=GREY_A).next_to(gA, DOWN, buff=0.3),
                     label(r"Bach: \ every voice going somewhere", font_size=24, color=TUNE).next_to(gB, DOWN, buff=0.3))
        with self.voiceover(
            "B is Bach's. Look at the pictures as well as listening: in A the alto and tenor hold long "
            "notes and the chords change underneath them; in B every voice is moving, with quick notes "
            "between the beats. The search's version breaks no rule, and it is not wrong. It is a correct "
            "exercise. What it lacks is what chapter eight showed: lines."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()
