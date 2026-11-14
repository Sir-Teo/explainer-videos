from __future__ import annotations

import numpy as np

from videos.music.music17.common import *  # noqa: F403


class Cadences(SoundScene):
    def construct(self):
        chapter(self, 7, r"Where phrases end", r"What happens at the fermatas?")
        self.table()
        self.hear()
        self.picardy()

    # ------------------------------------------------------------------
    def table(self):
        d = load("cadences")
        def tab(rows_, x, title, total):
            g = VGroup(label(title, font_size=24, color=GREY_A))
            for k, (a, z, n) in enumerate(rows_[:6]):
                r = VGroup(label(rf"{a} $\to$ {z}", font_size=26, color=WHITE), label(rf"{n}", font_size=24, color=TUNE), label(rf"{100 * n / total:.0f}\%", font_size=20, color=GREY_B))
                r[0].move_to([x - 0.4, 1.7 - 0.55 * k, 0], aligned_edge=RIGHT)
                r[1].move_to([x + 0.2, 1.7 - 0.55 * k, 0], aligned_edge=LEFT)
                r[2].move_to([x + 1.1, 1.7 - 0.55 * k, 0], aligned_edge=LEFT)
                g.add(r)
            g[0].move_to([x, 2.5, 0])
            return g
        mj = tab(d["major"]["pairs"], -3.3, rf"major: \ {d['major']['total']} phrase endings", d["major"]["total"])
        mn = tab(d["minor"]["pairs"], 3.3, rf"minor: \ {d['minor']['total']} phrase endings", d["minor"]["total"])
        foot = VGroup(label(r"the chords at the pauses", font_size=30, color=GREY_A).to_edge(UP, buff=0.3),
                      label(r"the chord before the fermata, \ and the chord under it; \ -- \ is a beat with no chord", font_size=20, color=GREY_B).to_edge(DOWN, buff=0.5))
        pj = {(a, z): n for a, z, n in d["major"]["pairs"]}
        auth = pj.get(("V", "I"), 0) + pj.get(("V7", "I"), 0)
        half = sum(n for a, z, n in d["major"]["pairs"] if z == "V")
        with self.voiceover(
            "Every line of a chorale ends at a fermata, a pause. What chords does Bach put there? "
            "<bookmark mark='a'/> In major keys, the commonest ending is five to one, the authentic "
            f"cadence of Part 15: with the seventh added, {say(auth)} of "
            f"{say(d['major']['total'])} phrase endings. Next comes an ending on five itself, a half "
            "cadence, most often approached from the dominant of the dominant: the phrase stops on a "
            "question. <bookmark mark='b'/> In minor keys the second commonest ending is seven to three: "
            "an authentic cadence in the relative major. A minor chorale's middle phrases often end in "
            "the major key next door, and come home only at the end."
        ) as vo:
            self.play(FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(mj))
            vo.wait_until("b")
            self.play(FadeIn(mn))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("cadences")
        c = clip("cadences.three")
        names = ("authentic", "half", "picardy")
        titles = {"authentic": r"authentic: \ V $\to$ I", "half": r"half: \ $\to$ V", "picardy": r"a minor chorale's last chord"}
        card = listen_card(r"Three phrase endings from the chorales. \ One comes home, \ one stops on a question, \ one ends a minor chorale. \ Which is which: \ A, \ B, \ C?", width=10.4)
        with self.voiceover(
            "Now three endings from the chorales themselves. One comes home, an authentic cadence; one "
            "stops on a question, a half cadence; and one is the end of a whole chorale in a minor key. "
            "Which is which? A, B and C."
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        gs = VGroup()
        for k, nm in enumerate(names):
            h = d["heard"][nm]
            g = choir_roll(h["voices"], width=3.6, height=2.8, lo=40, hi=80, thick=0.12).move_to(RIGHT * 4.2 * (k - 1) + DOWN * 0.3)
            t = label("ABC"[k], font_size=40, color=GREY_A).next_to(g, UP, buff=0.3)
            src = label(h["chorale"].replace("bwv", "BWV "), font_size=18, color=GREY_B).next_to(g, DOWN, buff=0.25)
            gs.add(VGroup(g, t, src))
        self.play(FadeOut(card), LaggedStart(*[FadeIn(x) for x in gs], lag_ratio=0.3))
        with self.listen(c) as snd:
            window(snd, r"A, \ B, \ C", kind="synthesized", detail=r"a model choir", corner=DL, tag_corner=DR)
            for k, nm in enumerate(names):
                sing_roll(snd, gs[k][0], d["heard"][nm]["times"], start=d["starts"][nm])
                end = d["starts"][names[k + 1]] - 0.4 if k < 2 else c.duration
                pulse(snd, gs[k][1], d["starts"][nm], end, buff=0.1)
        answers = VGroup(*[label(titles[nm], font_size=22, color=TUNE).move_to(gs[k][1]) for k, nm in enumerate(names)])
        with self.voiceover(
            "A came home: five to one. B stopped on five, a question waiting for the next line. And C was "
            "the end of a chorale in a minor key."
        ):
            self.play(*[ReplacementTransform(gs[k][1], answers[k]) for k in range(3)])
        for k in range(3):
            gs[k].remove(gs[k][1])
            gs[k].add(answers[k])
        self.gs = gs

    # ------------------------------------------------------------------
    def picardy(self):
        d = load("cadences")
        fn = d["minor"]["finals"]
        tot = sum(fn.values())
        txt = VGroup(label(rf"minor chorales ending on a major home chord: \ {fn.get('I', 0)} of {tot}", font_size=28, color=TUNE),
                     label(rf"on the minor home chord: \ {fn.get('i', 0)}", font_size=26, color=WHITE),
                     label(r"`the Picardy third': \ the third raised in the last chord", font_size=24, color=GREY_A),
                     label(r"the rest end on another chord: \ older modes, \ which a key signature cannot name", font_size=22, color=GREY_B)).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Did you notice the last chord of the minor chorale? It is major. <bookmark mark='a'/> Of "
            f"{say(tot)} chorales in minor keys, {say(fn.get('I', 0))} end on a major home chord, and only "
            f"{say(fn.get('i', 0))} on the minor one. The raised third in the final chord has a name, the "
            "Picardy third, and in Bach's time it was the norm: the last sound of a piece should be the "
            "most consonant one, and the major triad is the more consonant of the two: its notes are the "
            "fourth, fifth and sixth harmonics of a single tone. "
            "<bookmark mark='b'/> Most of the rest end on a chord the key signature does not call home: "
            "these tunes are older than major and minor, in modes like the Phrygian, and Bach harmonized "
            "them in their own terms."
        ) as vo:
            self.play(self.gs.animate.shift(UP * 0.9).scale(0.85), FadeIn(txt[0]), FadeIn(txt[1]))
            vo.wait_until("a")
            self.play(FadeIn(txt[2]))
            vo.wait_until("b")
            self.play(FadeIn(txt[3]))
        self.wait(0.4)
        self.clear_scene()
