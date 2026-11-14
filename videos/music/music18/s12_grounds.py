from __future__ import annotations

import numpy as np

from videos.music.music18.common import *  # noqa: F403


class Grounds(SoundScene):
    def construct(self):
        chapter(self, 11, r"Ground basses", r"What happens when a progression repeats forever?")
        self.quiz()
        self.variation()
        self.history()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("grounds")
        c = clip("grounds.four")
        card = listen_card(r"Four progressions, \ each played twice round. \ Three are in minor keys \ and one in major. \ Which is in major: \ A, \ B, \ C or D?", width=10.0)
        with self.voiceover(
            "Some progressions were repeated over and over, while melodies and variations changed above them: "
            "ground basses. Here are four, each played twice round. Three are in minor keys, one in major. "
            "Which is the major one: A, B, C or D?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        cells = VGroup()
        for k, name in enumerate(d["order"]):
            g = chord_roll(d["grounds"][name]["chords"], width=2.8, height=1.8, lo=40, hi=80, thick=0.1)
            lab = label("ABCD"[k], font_size=36, color=GREY_A)
            cells.add(VGroup(lab, g).arrange(DOWN, buff=0.25))
        cells.arrange(RIGHT, buff=0.55).move_to(DOWN * 0.1)
        self.play(FadeOut(card), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"A, \ B, \ C, \ D", detail=r"a plucked string", corner=DL, tag_corner=DR)
            for k, name in enumerate(d["order"]):
                end = d["starts"][d["order"][k + 1]] - 0.4 if k < 3 else c.duration
                pulse(snd, cells[k][0], d["starts"][name], end, buff=0.08)
        names = {"lament": r"the lament", "folia": r"la Folia", "romanesca": r"the Romanesca \\ (Pachelbel's bass)", "passamezzo": r"passamezzo antico"}
        ans = VGroup(*[label(names[n], font_size=20, color=TUNE if n == "romanesca" else GREY_A).next_to(cells[k], DOWN, buff=0.3) for k, n in enumerate(d["order"])])
        with self.voiceover(
            "C. It is the Romanesca's descending bass in a major key, the progression Johann Pachelbel put under "
            "his famous canon: one, five, six, three, four, one, four, five. The other three are minor: the "
            "lament, la Folia, and the passamezzo antico."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def variation(self):
        d = load("more")["folia"]
        c = clip("more.folia")
        n = d["rounds"]
        g = chord_roll(d["chords"], width=11.0, height=2.8, lo=40, hi=80, thick=0.11).move_to(DOWN * 0.6)
        dots = VGroup()
        for k, fig in enumerate(d["run"]):
            x0 = g.xk(n + k) - 0.45
            for i, m in enumerate(fig):
                dots.add(Dot([x0 + 0.3 * i, g.frame.get_bottom()[1] + 2.8 * (m - 40) / 40 + 0.25, 0], radius=0.06, color=EAR))
        for col in g.cols[n:]:
            col[0].set_opacity(0.2)
        t1 = label(r"the Folia: \ the chords", font_size=24, color=GREY_A).move_to([(g.xk(0) + g.xk(n - 1)) / 2, 1.6, 0])
        t2 = label(r"the same chords, \ a variation above", font_size=24, color=EAR).move_to([(g.xk(n) + g.xk(2 * n - 1)) / 2, 1.6, 0])
        with self.voiceover(
            "What did musicians do with a ground? They varied what went above it, round after round, while the "
            "bass and the chords stayed fixed. Here is the Folia once with its chords alone, and once more with the "
            "chords broken into running notes above it: the simplest of the thousands of variations written on it."
        ):
            self.play(FadeIn(g), FadeIn(dots), FadeIn(t1), FadeIn(t2))
        with self.listen(c) as snd:
            window(snd, r"the Folia, \ plain and varied", detail=r"a plucked string", corner=DL, tag_corner=DR)
            sing_chords(snd, g, d["times"])
            flash(snd, list(dots), [d["times"][n + k // 4] + (k % 4) * 0.279 for k in range(len(dots))], hot=WHITE, base=EAR)
        with self.voiceover(
            "Corelli's twenty-three variations do this with every resource of the violin: quick runs, double stops, "
            "slow lyrical rounds, a gigue. The listener always knows where in the progression the music is, because "
            "the ground never changes, and the pleasure is in the distance between what stays and what moves."
        ):
            self.wait(0.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        rows_ = VGroup(*[label(t, font_size=24, color=c_) for t, c_ in (
            (r"the lament: \ a bass falling four steps, \ 1--$\flat$7--$\flat$6--5; \ Monteverdi 1638, \ Purcell's Dido 1689 \ (chromatic)", WHITE),
            (r"la Folia: \ a Portuguese dance; \ Corelli's variations 1700; \ Vivaldi, \ Bach, \ Liszt, \ Rachmaninoff", WHITE),
            (r"the passamezzo antico: \ the sixteenth century's commonest dance bass", WHITE),
            (r"Pachelbel's canon: \ the Romanesca, \ and in a hundred popular songs since", WHITE),
            (r"the chromatic lament in rock: \ a bass falling by semitones under a held chord", GREY_A),
            (r"a ground is syntax frozen: \ the progression is the piece, \ and the art is in the variations", TUNE))]).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"four centuries of grounds", font_size=30, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "These grounds have long histories. <bookmark mark='a'/> The lament is a bass falling four steps from "
            "home to the dominant; Monteverdi set his Lament of the Nymph over it in 1638, and Purcell's Dido sings "
            "her lament in 1689 over a chromatic form of it, falling by semitones. <bookmark mark='b'/> La Folia "
            "began as a wild Portuguese dance; Corelli wrote twenty-three variations on it in 1700, and composers "
            "from Vivaldi to Rachmaninoff returned to it. <bookmark mark='c'/> The passamezzo antico carried "
            "sixteenth-century dances. <bookmark mark='d'/> The Romanesca's bass is Pachelbel's, and its "
            "descending line runs under many popular songs. <bookmark mark='e'/> The chromatic lament still turns "
            "up in rock, a bass falling by semitones under a held chord. <bookmark mark='f'/> A ground is "
            "harmonic syntax frozen into a single sentence, repeated: the progression is fixed, and the art is in "
            "what goes over it."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abcdef", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
