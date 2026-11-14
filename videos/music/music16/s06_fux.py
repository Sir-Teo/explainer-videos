from __future__ import annotations

import numpy as np

from videos.music.music16.common import *  # noqa: F403


class Fux(SoundScene):
    def construct(self):
        chapter(self, 5, r"Fux's exercise", r"How was counterpoint taught?", extra=((1725, r"Fux's \textit{Gradus ad Parnassum}"),))
        self.book()
        self.rules()
        self.listen_ex()
        self.below()

    # ------------------------------------------------------------------
    def book(self):
        card = history_card(1725, r"Johann Joseph Fux, \ Vienna: \ \textit{Gradus ad Parnassum}", r"a dialogue between a teacher, \ Aloys, \ and a pupil, \ Josephus; \ counterpoint in five species, \ each harder than the last", width=10.0, font_size=26).to_edge(UP, buff=0.4)
        d = load("fux")
        cf = [(p, 4.0 * k, 4.0) for k, p in enumerate(d["cf"])]
        g = duet([cf], colors=(CF_C,), width=9.0, height=2.0, lo=58, hi=72, thick=0.16, bar=4.0).move_to(DOWN * 1.2)
        names = VGroup(*[label(tex(NAMES[p][:-1]), font_size=22, color=CF_C).next_to(g.notes[0][k], DOWN, buff=0.15) for k, p in enumerate(d["cf"])])
        cl = label(r"the cantus firmus: \ D F E D G F A G F E D", font_size=26, color=CF_C).next_to(g, UP, buff=0.3)
        with self.voiceover(
            "In 1725 Johann Joseph Fux, composer to the emperor in Vienna, published a textbook in "
            "Latin called the Gradus ad Parnassum, the steps to Parnassus. It is a dialogue between a "
            "teacher, Aloys, and a pupil, Josephus, and for two centuries composers learned from it: "
            "Haydn worked through it, Mozart taught from it, Beethoven copied out its exercises. "
            "<bookmark mark='a'/> The method is to write a new line against a given melody in long "
            "equal notes, a cantus firmus. Here is the first one Josephus is given, in the Dorian mode "
            "on D: D, F, E, D, G, F, A, G, F, E, D."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(FadeIn(g), FadeIn(names), FadeIn(cl))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rules(self):
        d = load("fux")
        rows = d["rules"]
        left = VGroup(*[label(rf"{k + 1}. \ {r['text']}", font_size=20, color=WHITE) for k, r in enumerate(rows)])
        right = VGroup(*[label(r["why"], font_size=16, color=GREY_B) for r in rows])
        for k, (l, r) in enumerate(zip(left, right)):
            y = 2.35 - 0.42 * k
            l.move_to([-6.6, y, 0], aligned_edge=LEFT)
            r.move_to([-0.2, y, 0], aligned_edge=LEFT)
            if r.width > 6.6:
                r.scale_to_fit_width(6.6).move_to([-0.2, y, 0], aligned_edge=LEFT)
        hl = label(r"the rule", font_size=24, color=TUNE).move_to([-6.6, 2.95, 0], aligned_edge=LEFT)
        hr = label(r"what it protects \ (Huron, \ 2001)", font_size=24, color=TUNE).move_to([-0.2, 2.95, 0], aligned_edge=LEFT)
        with self.voiceover(
            "In first species, the new line has one note for each note of the cantus, and it must obey "
            "rules. Here are twelve of them, as modern textbooks state Fux. Only consonances against "
            "the cantus. Begin on a perfect consonance, and end on the octave, approached by step. No "
            "unisons in the middle. No parallel fifths or octaves, and no perfect consonance reached by "
            "similar motion. No awkward leaps, no repeated notes, and a step back after a large leap. "
            "Not too many parallel thirds or sixths. No crossing. One highest note. "
            "<bookmark mark='a'/> Beside each rule is what it protects, in Huron's account: the "
            "fusion and co-modulation of chapters two and three, and the pitch proximity and "
            "regression to the middle of Part 14. Almost every rule is a way of keeping two lines from "
            "merging, or of keeping one line from falling apart."
        ) as vo:
            self.play(FadeIn(hl), LaggedStart(*[FadeIn(x) for x in left], lag_ratio=0.25), run_time=8.0)
            vo.wait_until("a")
            self.play(FadeIn(hr), LaggedStart(*[FadeIn(x) for x in right], lag_ratio=0.12), run_time=4.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def listen_ex(self):
        d = load("fux")
        c = clip("fux.exercise")
        cf = [(p, 4.0 * k, 4.0) for k, p in enumerate(d["cf"])]
        cp = [(p, 4.0 * k, 4.0) for k, p in enumerate(d["best"])]
        st = staff_pair(cp, cf, width=11.0, space=0.15).move_to(UP * 1.3)
        g = duet([cp, cf], width=9.2, height=2.0, lo=58, hi=80, thick=0.13, bar=4.0).move_to(DOWN * 1.6 + RIGHT * 0.7)
        ints = VGroup(*[label(str({12: 8, 4: 3, 7: 5, 9: 6, 3: 3, 0: 1, 16: 10, 15: 10, 8: 6}.get(v, v)), font_size=20, color=GREY_A).move_to([g.notes[0][k].get_center()[0], g.get_bottom()[1] - 0.25, 0]) for k, v in enumerate(d["verticals"])])
        il = label(r"interval above the cantus", font_size=18, color=GREY_B).next_to(ints, LEFT, buff=0.3)
        if il.get_left()[0] < -6.9:
            il.shift(RIGHT * (-6.9 - il.get_left()[0]))
        with self.voiceover(
            "Here is the cantus alone, and then with a first-species line above it that obeys all "
            "twelve rules; it is the line that Monochord's search for Fux's preferences, chiefly "
            "contrary motion, liked best. Under each pair of notes is the interval between them."
        ):
            self.play(FadeIn(st), FadeIn(g), FadeIn(ints), FadeIn(il))
        with self.listen(c) as snd:
            window(snd, r"the cantus; \ then two voices", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            sing_voice(snd, g.notes[1], d["times"]["cf"] + [999] * 0, base=CF_C)
            sing_voice(snd, g.notes[0], d["times"]["both"][0], base=UP_C)
        mot = d["motions"]
        cap = label(rf"{sum(m == 'contrary' for m in mot)} of its {len(mot)} moves are contrary motion; \ it ends sixth, \ octave, \ through C$\sharp$", font_size=26, color=TUNE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            f"Nine of its ten moves are in contrary motion. It begins on the octave and ends on it, "
            "through a major sixth, with the cantus falling to D as the new voice rises to it through "
            "C sharp, the leading note Part 15 found in every cadence. It does not belong to the mode. "
            "In earlier centuries such notes were often left unwritten, and singers supplied them by "
            "rule; the practice was called musica ficta."
        ):
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def below(self):
        b = load("more")["below"]
        cfn = load("fux")["cf"]
        c = clip("more.below")
        cf = [(p, 4.0 * k, 4.0) for k, p in enumerate(cfn)]
        lo = [(p, 4.0 * k, 4.0) for k, p in enumerate(b["line"])]
        st = staff_pair(cf, lo, width=11.0, space=0.15, lower_clef="bass").move_to(UP * 1.45)
        g = duet([cf, lo], colors=(CF_C, UP_C), width=9.2, height=2.0, lo=48, hi=71, thick=0.13, bar=4.0).move_to(DOWN * 1.75 + RIGHT * 0.7)
        IV = {0: "1", 3: "3", 4: "3", 7: "5", 8: "6", 9: "6", 12: "8", 15: "10", 16: "10"}
        ints = VGroup(*[label(IV.get(v, str(v)), font_size=20, color=GREY_A).move_to([g.notes[0][k].get_center()[0], g.get_bottom()[1] - 0.25, 0]) for k, v in enumerate(b["verticals"])])
        il = label(r"interval below the cantus", font_size=18, color=GREY_B).next_to(ints, LEFT, buff=0.3)
        if il.get_left()[0] < -6.9:
            il.shift(RIGHT * (-6.9 - il.get_left()[0]))
        with self.voiceover(
            "Fux then turns the exercise over: the cantus on top, and the new voice below it. Most rules "
            "carry over, measured from the lower note. Two change. The line must begin on the octave or "
            "the unison, never a fifth below, because a fifth below the D would be G, and a bass on G "
            "makes the listener hear G, not D, as home. And at the cadence the new voice still takes the "
            "leading note, C sharp, now a third below the cantus's E, closing to the unison."
        ):
            self.play(FadeIn(st), FadeIn(g), FadeIn(ints), FadeIn(il))
        with self.listen(c) as snd:
            window(snd, r"a line below the cantus", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            sing_voice(snd, g.notes[0], b["times"][0], base=CF_C)
            sing_voice(snd, g.notes[1], b["times"][1], base=UP_C)
        cap = label(rf"lines below: \ {b['count']} \ (above: \ {b['above']}); \ any first note, \ {b['start_rule']['fifth']}", font_size=26, color=TUNE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            f"Count again. Below the cantus there are only {say(b['count'])} good lines, against "
            f"{say(b['above'])} above. Most of the difference is the first note: drop the rule about it, "
            f"and the count jumps to {say(b['start_rule']['fifth'])}. One rule about where home is "
            "removes six good lines in every seven."
        ):
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()
