from __future__ import annotations

import numpy as np

from videos.music.music26.common import *  # noqa: F403
from videos.music.variations import rows_before

ORDER = ["theme", "minore", "adagio", "finale"]


class Outro(SoundScene):
    def construct(self):
        self.variation()
        self.recap()
        self.problems()
        self.payoffs()
        self.next_part()

    # ------------------------------------------------------------------
    def variation(self):
        d = load("tune")
        v = load("variation")
        c = clip("tune.variation26")
        head = VGroup(label(r"Variation 26", font_size=48, color=TUNE), label(r"the Tune, \ as a Classical set", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        cells = VGroup()
        rolls = []
        for k in ORDER:
            g = voices_roll(d[k], width=5.2, height=1.7, colors=[TUNE, GREY_A], lo=34, hi=86, bar_h=0.07)
            cells.add(VGroup(label({"theme": r"theme, \ Alberti bass", "minore": r"minore", "adagio": r"adagio, \ ornamented", "finale": r"finale, \ in 6/8"}[k], font_size=20, color=GREY_A), g).arrange(DOWN, buff=0.15))
            rolls.append(g)
        cells.arrange_in_grid(rows=2, cols=2, buff=(0.7, 0.4)).move_to(DOWN * 0.3)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it has built, and this time Mozart got there first. "
            "<bookmark mark='a'/> So here is the film's own small Classical set, beside his: the theme over an Alberti bass; "
            "a minore, the Tune in C minor over repeated chords; an adagio, twice as slow, decorated with turns; and a "
            "finale in a quick six-eight."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"Variation 26", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for i, k in enumerate(ORDER):
                st = d["starts"][k]
                flash_voices(snd, rolls[i], d[k], st, d["units"][k], colors=[TUNE, GREY_A])
                end = d["starts"][ORDER[i + 1]] - 0.4 if i < 3 else c.duration
                pulse(snd, cells[i][0], st, end, buff=0.06)
        self.play(FadeOut(cells))
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            f"Row twenty-six of the ledger. {say(v['seconds'])} seconds. The measurement is the simplest one: the melody "
            f"has {say(d['notes']['theme'])} notes in the theme and the minore, {say(d['notes']['adagio'])} in the adagio, "
            f"{say(d['notes']['finale'])} in the finale. Mozart's twelve variations do far more, and are worth hearing next."
        ):
            self.play(FadeIn(led, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        ph = load("phrases")
        st = load("style")
        tx = load("texture")["by"]
        kk = load("keys")
        card = objectives_card([
            r"a style of shared expectations: \ schemata, \ cadences, \ the joke that depends on them",
            rf"periodic phrasing: \ gaps of 4 and 8 bars most common, \ but a minority of {ph['cadences']} cadences",
            rf"sonata form traced by a key-finder: \ home, \ the dominant, \ away, \ home; \ {kk['tally']['major|V']} of {kk['major']} major-key movements go first to V",
            rf"the quartet as conversation: \ the first violin leads in {100 * tx['haydn']['shares'][0]:.0f} (Haydn) to {100 * tx['beethoven']['shares'][0]:.0f} (Beethoven) bars in 100",
            r"Beethoven: \ three times the length, \ nearly an octave more range",
            rf"a fair attribution test: \ {100 * st['acc26']:.0f} in 100; \ shuffled names {100 * np.mean(st['null']):.0f}, \ always Mozart {100 * st['chance']:.0f}",
        ], title=r"What we found", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? The Classical style runs on shared expectations, strong enough to joke with. "
            "<bookmark mark='a'/> Its phrases lean on four and eight bars, though most real cadences fall elsewhere. "
            "<bookmark mark='b'/> Sonata form is visible to a key-finder that knows no themes, and most major-key movements "
            "go first to the dominant. "
            "<bookmark mark='c'/> The quartet is a conversation led, most of the time, by the first violin. "
            "<bookmark mark='d'/> Beethoven took the language longer and wider. <bookmark mark='e'/> And the numbers "
            "do know something about who wrote a quartet, more than shuffled names, but less than a rule that always says "
            "Mozart: style is easier to hear than to count."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("abcde", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"A movement has cadences at bars 4, 8, 16, 22, 30 and 38. \ Compute its phrase gaps and the share that are 4 or 8 bars.",
            r"Prove that a nearest-centroid classifier with two classes and one feature is a threshold at the midpoint of the class means.",
            r"\textbf{Ear.} \ The lab plays eight phrases on the Tune, \ some ending on a half cadence, \ some on an authentic one. \ Sort them.",
            r"\textbf{Build.} \ Add a feature to the attribution test that measures surprise under a model of chord pairs, \ and report the leave-one-out accuracy.",
            r"$\bigstar$ \ Recompute the 2020 study of Beethoven's metronome marks from its published data, \ and test its central claim.",
        ], font_size=22)
        with self.voiceover(
            "Five problems. One to compute, one to prove, one for your ears, one to build, and a research problem, "
            "marked with a star. Solutions are in this part's notes. Pause here."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.25), run_time=3.0)
        self.wait(5.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        pay = payoff_card([
            (r"Romantic forms: \ the sonata stretched and broken", [27]),
            (r"the song and its accompaniment figures", [40]),
            (r"orchestration from the Classical orchestra", [41]),
            (r"performing: \ tempo, \ rubato, \ the evidence", [43]),
            (r"style by statistics, \ and machines that compose in a style", [62, 65]),
            (r"the Variations: \ the whole series as one set", [68]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? In the Romantic century, which stretched the sonata and broke it. In the song, with "
            "its accompaniment figures. In orchestration, built on the Classical orchestra. In performing, where tempo is "
            "argued. In machines that learn and compose in a style. And in the last part, where the whole series becomes "
            "one set of variations, as Mozart's was."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"pianists", r"shape a period: \ the half cadence asks, \ the full one answers"),
            (r"quartet players", r"know who has the tune, \ bar by bar"),
            (r"composers", r"use an accompaniment figure as a motor, \ and then as a motive"),
            (r"analysts", r"test claims about style with fair comparisons"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Pianists shape a period as a question and an answer. Quartet players know, bar by bar, who has "
            "the tune. Composers still use an accompaniment figure as a motor, and sometimes as a motive. And analysts can "
            "test claims about style only with fair comparisons."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"C. Rosen, \ \textit{The Classical Style} \ (1971)",
             r"W. E. Caplin, \ \textit{Classical Form} \ (1998)",
             r"R. O. Gjerdingen, \ \textit{Music in the Galant Style} \ (2007)",
             r"J. Hepokoski and W. Darcy, \ \textit{Elements of Sonata Theory} \ (2006)"],
            [r"H. C. Koch, \ \textit{Versuch einer Anleitung zur Composition} \ (1782--1793)",
             r"L. B. Meyer, \ \textit{Style and Music} \ (1989)",
             r"A. Martín-Castro and I. Ucar, \ `Conductors' tempo choices shed light over Beethoven's metronome', \ \textit{PLOS ONE} \ (2020)",
             r"M. S. Cuthbert and C. Ariza, \ `music21' \ (2010): \ the quartet encodings"],
            font_size=19)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        q = label(r"what happens when the self becomes the subject?", font_size=30, color=EAR).move_to(UP * 0.4)
        top = label(r"Act IV: \ a thousand years", font_size=30, color=GREY_A).to_edge(UP, buff=0.8)
        nxt = VGroup(label(r"Part 27", font_size=32, color=GREY_B), label(r"The Romantic Century", font_size=50, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "The Classical style shared its expectations. <bookmark mark='a'/> The next century made music personal, "
            "chromatic and enormous, and the expectations became something to stretch until they broke. "
            "<bookmark mark='b'/> Next time. Part 27: The Romantic Century."
        ) as vo:
            self.play(FadeIn(top))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
