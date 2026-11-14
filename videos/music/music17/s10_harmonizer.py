from __future__ import annotations

import numpy as np

from videos.music.music17.common import *  # noqa: F403


class Harmonizer(SoundScene):
    def construct(self):
        chapter(self, 9, r"Harmonizing as search", r"Can chords and voices be chosen together?", extra=((2005, r"Allan and Williams's hidden Markov model"),))
        self.problem()
        self.lattice()
        self.costs()
        self.result()

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (r"given: \ a tune, \ one note a beat", WHITE),
            (r"choose at each beat: \ a chord that contains the note", WHITE),
            (r"and a voicing: \ where the alto, \ tenor and bass sing it", WHITE),
            (r"so that the whole is likely, \ like Bach's, \ and breaks no rule", TUNE))]).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"the exercise, \ as a problem a computer can solve", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Now the exercise itself, set to a machine. <bookmark mark='a'/> Given a tune, one note to each "
            "beat, choose at every beat a chord that contains the tune's note, <bookmark mark='b'/> and a "
            "voicing of that chord: exactly where the alto, tenor and bass sing it. "
            "<bookmark mark='c'/> Choose them so that the whole progression is likely, in the sense of "
            "chapter six's table, and so that the voices move as chapter three found and break none of "
            "chapter four's rules. Chords and voices have to be chosen together, because a rule like "
            "no parallel fifths depends on both."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows_[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows_[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows_[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lattice(self):
        d = load("harmonizer")
        n = d["beats"]
        states = d["states"]
        xs = np.linspace(-5.6, 5.6, n)
        cols = VGroup()
        rng = np.random.default_rng(1)
        picks = []
        pos = 0.5
        for k, s_ in enumerate(states):
            m = int(np.ceil(s_ / 25))
            ys = np.linspace(-1.9, 1.9, m)
            col = VGroup(*[Dot([xs[k], y, 0], radius=0.035, color=GREY_B) for y in ys])
            cols.add(col)
            pos = float(np.clip(pos + rng.normal(0, 0.12), 0.1, 0.9))                       # an example path: one dot a column
            picks.append(int(round(pos * (m - 1))))
        path = VMobject(stroke_color=TUNE, stroke_width=4).set_points_as_corners([cols[k][picks[k]].get_center() for k in range(n)])
        counts = VGroup(*[label(str(s_), font_size=16, color=GREY_B).move_to([xs[k], -2.3, 0]) for k, s_ in enumerate(states)])
        tl = label(r"each dot: \ about 25 (chord, \ voicing) pairs under that beat's note", font_size=20, color=GREY_B).to_edge(DOWN, buff=0.45)
        head = label(rf"the hook's {n} beats: \ every way to harmonize them", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        big = label(rf"paths through the lattice: \ about $10^{{{d['log10_paths']:.0f}}}$", font_size=30, color=TUNE).to_edge(UP, buff=1.15)
        with self.voiceover(
            f"Lay the choices out as a lattice: a column for each of the hook's {say(n)} beats, a dot for "
            f"every chord and voicing that fits that beat's note. <bookmark mark='a'/> There are between "
            f"{say(min(states))} and {say(max(states))} under each note. <bookmark mark='b'/> A harmonization "
            f"is a path from left to right, one dot in each column, and there are about ten to the "
            f"{say(round(d['log10_paths']))} of them, too many to try. <bookmark mark='c'/> But the cost of "
            "a path is a sum of costs of single dots and of steps between neighbouring columns, so the "
            "cheapest path can be found column by column: for every dot, keep only the cheapest way to "
            "reach it. It is the Viterbi algorithm, the dynamic programming of Part 16's counting turned "
            f"to finding the best. Here it takes {say(d['seconds'], 1)} seconds."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c_) for c_ in cols], lag_ratio=0.1), run_time=3.0)
            vo.wait_until("a")
            self.play(FadeIn(counts), FadeIn(tl))
            vo.wait_until("b")
            self.play(FadeIn(big))
            vo.wait_until("c")
            self.play(Create(path), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def costs(self):
        w = load("harmonizer")["weights"]
        rows_ = [(r"how unlikely the chord is after the last one", r"chapter 6's table, \ learned from 280 chorales", 1.0),
                 (r"how unlikely the tune's note is in the chord", r"the same chorales", 1.0),
                 (r"how far the alto, \ tenor and bass move", r"chapter 3", w["motion"]),
                 (r"parallel fifths or octaves, \ any pair", r"chapter 4", w["parallel"]),
                 (r"hidden fifths and octaves; \ overlaps; \ inner leaps", r"chapter 4", w["hidden"]),
                 (r"a leading note or a seventh going the wrong way", r"chapter 4", w["leading"]),
                 (r"a chord in inversion; \ a doubled major third", r"chapter 2", w["inversion"]),
                 (r"at a fermata: \ how often Bach ends a phrase there", r"chapter 7", w["end"])]
        tab = VGroup()
        for k, (a, b, wt) in enumerate(rows_):
            r = VGroup(label(a, font_size=22, color=WHITE), label(b, font_size=20, color=GREY_B))
            r[0].move_to([-0.4, 2.2 - 0.56 * k, 0], aligned_edge=RIGHT)
            r[1].move_to([0.3, 2.2 - 0.56 * k, 0], aligned_edge=LEFT)
            tab.add(r)
        head = label(r"the cost of a path: \ a sum of", font_size=30, color=GREY_A).to_edge(UP, buff=0.35)
        foot = label(r"the weights were set on chorales held out from training, \ and never on the test", font_size=22, color=TUNE).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "What goes into the cost. Two terms come from Bach's statistics: how unlikely each chord is, "
            "given the one before it, and how unlikely the tune's note is within that chord, both counted "
            "from two hundred and eighty chorales. <bookmark mark='a'/> The rest are this part's chapters "
            "turned into penalties: how far the inner voices and the bass move; a heavy penalty for "
            "parallel fifths and octaves; smaller ones for hidden fifths, overlaps and leaps; a leading "
            "note or a seventh going the wrong way; inversions and doubling; and at each fermata, how "
            "often Bach ends a phrase on that chord. <bookmark mark='b'/> How much each penalty weighs "
            "was tuned on chorales kept apart from the training, and the test set was never used for it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in tab[2:]], lag_ratio=0.3), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def result(self):
        d = load("harmonizer")
        h = load("hook")
        ours, bach = d["full_roman"], d["bach_roman"]
        n = len(ours)
        xs = np.linspace(-5.8, 5.8, n)
        r1 = VGroup(*[label(t, font_size=26, color=TUNE if t == b else WHITE) for t, b in zip(ours, bach)])
        r2 = VGroup(*[label(t, font_size=26, color=TUNE if t == a else GREY_A) for t, a in zip(bach, ours)])
        for k in range(n):
            r1[k].move_to([xs[k], 0.5, 0])
            r2[k].move_to([xs[k], -0.6, 0])
        l1 = label(r"ours", font_size=24, color=GREY_A).next_to(r1, UP, buff=0.35)
        l2 = label(r"Bach's", font_size=24, color=GREY_A).next_to(r2, DOWN, buff=0.35)
        same = sum(a == b for a, b in zip(ours, bach))
        cap = label(rf"the same chord on {same} of {n} beats; \ parallel fifths and octaves: \ none \ (the chord-chooser: \ {len(h['parallels_plain'])})", font_size=24, color=TUNE).to_edge(DOWN, buff=0.6)
        head = label(r"the hook's tune, \ harmonized by the search, \ chord by chord", font_size=28, color=GREY_A).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Here is the search's answer for the hook's two phrases, chord by chord, against Bach's. "
            f"<bookmark mark='a'/> They agree on {say(same)} of the {say(n)} beats. One difference is a lesson: at the "
            "end of the second phrase the search chooses a major home chord, where Bach stays minor. It "
            "learned from minor chorales that end on a major chord, the Picardy third, and it cannot tell "
            "the end of a phrase from the end of a piece. And where the chord-chooser of the hook wrote "
            f"{say(len(h['parallels_plain']))} parallels, the search writes none: the penalties did their "
            "work. How good is it in general? That needs tunes it has never seen."
        ) as vo:
            self.play(FadeIn(head), FadeIn(r1), FadeIn(r2), FadeIn(l1), FadeIn(l2))
            vo.wait_until("a")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()
