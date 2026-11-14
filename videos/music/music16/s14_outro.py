from __future__ import annotations

import numpy as np

from videos.music.music16.common import *  # noqa: F403
from videos.music.variations import rows_before


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
        c = clip("tune.variation16")
        head = VGroup(label(r"Variation 16", font_size=48, color=TUNE), label(r"the Tune as a cantus firmus", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.35)
        chips = VGroup(*[label(nm, font_size=20, color=GREY_B) for nm in (r"organum", r"first", r"second", r"third", r"fourth", r"fifth")]).arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it has built. This part built "
            "counterpoint. <bookmark mark='a'/> So the Tune becomes a cantus firmus: each of its notes "
            "held for a whole bar, in the lower voice. Over its first phrase, a second voice in "
            "organum, a fifth below, as in the ninth century. Then, phrase by phrase, a voice above it "
            "in each of Fux's five species, written by Monochord's search: one note against one, two "
            "against one, four against one, held over, and florid. One search, so the line runs on "
            "from phrase to phrase."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in chips], lag_ratio=0.6), run_time=10.0)
        up = [tuple(e) for e in d["upper"]]
        cf = [(p, 4.0 * k, 4.0) for k, p in enumerate(d["cf"])]
        win = 28.0
        shown = None
        with self.listen(c) as snd:
            window(snd, r"Variation 16", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for k in range(6):
                snd.wait_until(f"phrase{k}")
                if shown is not None:
                    self.remove(*shown)
                a, b = win * k, win * (k + 1)
                u = [(p, s_ - a, w) for p, s_, w in up if a <= s_ < b]
                l = [(p, s_ - a, w) for p, s_, w in cf if a <= s_ < b]
                g = duet([u, l], width=11.0, height=3.0, lo=50, hi=84, thick=0.13, total=win, bar=4.0).move_to(UP * 0.4)
                ui = [i for i, (p, s_, w) in enumerate(up) if a <= s_ < b]
                li = [i for i, (p, s_, w) in enumerate(cf) if a <= s_ < b]
                st = d["stats"][k]
                name = label(d["names"][k], font_size=34, color=TUNE).next_to(g, UP, buff=0.25)
                meas = label(rf"notes beginning together: \ {100 * st['together']:.0f}\% \qquad fused moments: \ {100 * st['fused']:.0f}\%", font_size=24, color=GREY_A).next_to(g, DOWN, buff=0.3)
                shown = [g, name, meas]
                self.add(*shown)
                sing_voice(snd, g.notes[0], [d["times_upper"][i] for i in ui], base=UP_C)
                sing_voice(snd, g.notes[1], [d["times_cf"][i] for i in li], base=CF_C)
                pulse(snd, chips[k], d["phrase_starts"][k], d["phrase_starts"][k] + d["phrase_seconds"], buff=0.06)
        self.remove(*shown)
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).to_edge(DOWN, buff=0.25)
        st = d["stats"]
        with self.voiceover(
            f"Row sixteen of the ledger. {say(v['seconds'])} seconds. The measurement: in the organum "
            f"phrase every note began together with the cantus, and every move landed on a fused "
            f"interval. In the fourth-species phrase, no note began with the cantus, and none fused. "
            "The same melody underneath; two ways of being heard."
        ):
            self.play(FadeOut(chips), FadeIn(led, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        c = load("counting")
        card = objectives_card([
            r"organum wanted one voice, \ made thicker; \ parallel perfect intervals were the means",
            r"three cues merge two voices: \ fusing intervals, \ moving together, \ starting together",
            r"Fux's first species: \ twelve rules, \ almost all derivable from those cues \ (Huron, \ 2001)",
            rf"{c['valid']} good lines of {c['total'] / 1e12:.1f} million million; \ the parallel-fifths rule adds nothing to the rest",
            r"each rule removed lets back one way of losing a voice",
            r"species two to five: \ passing, \ neighbouring and suspended dissonances, \ and voices apart in time",
        ], title=r"What we found", font_size=26).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? Organum wanted one voice, made thicker, and parallel perfect intervals "
            "were its means. <bookmark mark='a'/> Three cues make the ear merge two voices: intervals "
            "that fuse, moving together, and starting together. <bookmark mark='b'/> Fux's rules, for "
            "the most part, follow from avoiding those cues, as Huron showed. <bookmark mark='c'/> Over "
            f"Fux's cantus, {say(c['valid'])} lines obey every rule, out of four point six million "
            "million, and the famous rule against parallel fifths adds nothing that the others do not "
            "already do. <bookmark mark='d'/> Each rule removed lets back one particular way of losing "
            "a voice. <bookmark mark='e'/> And the later species bring dissonance back, as passing "
            "notes, neighbours and suspensions, while pulling the voices apart in time."
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
            r"Against the cantus C D F E D C, \ write every first-species line above it that begins C$'$ and ends C$'$, \ "
            r"obeying the twelve rules, \ and say which you prefer and why.",
            r"Show that if no perfect consonance may be reached by similar motion, \ then no parallel fifths or octaves can occur. \ "
            r"Is the converse true: \ which lines does the weaker rule allow that the stronger forbids?",
            r"\textbf{Ear.} \ The lab plays eight pairs of two-voice chords. \ For each, \ say whether the voices move in parallel, \ similar, \ contrary or oblique motion.",
            r"\textbf{Build.} \ With \texttt{counterpoint.count}, \ remove each rule in turn, \ above Fux's cantus and below it. \ "
            r"Which rules bind harder below, \ and why?",
            r"$\bigstar$ \ Of the 152 good lines over Fux's cantus, \ which would a teacher grade highest? \ Propose a score, \ "
            r"and a way to check it against human judgements.",
        ], font_size=23)
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
            (r"four voices, \ and the rules of voice leading", [17]),
            (r"progressions: \ how chords follow chords", [18]),
            (r"canon and fugue: \ one melody against itself", [20]),
            (r"Notre-Dame, \ Josquin, \ Palestrina", [23, 24]),
            (r"constraint solving and composing machines", [42, 65]),
            (r"separating voices in a recording", [64]),
        ], font_size=26)
        with self.voiceover(
            "Where does this come back? At once: the next part puts four voices together, where the "
            "same rules govern the chords. Then progressions, and canon and fugue, where a melody is "
            "set against itself. The history from Notre-Dame to Palestrina gets its own parts. The "
            "search that wrote these species returns as a way of composing, and the question of "
            "hearing two voices as two returns, turned around, when machines try to separate them in a "
            "recording."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"arrangers", r"double a melody in octaves to make it one bigger voice, \ or in thirds to keep two"),
            (r"choir directors", r"ask singers to start a hair apart when the parts must be heard, \ and exactly together when they must blend"),
            (r"bass players", r"move against the melody, \ in contrary motion, \ to stay audible"),
            (r"mix engineers", r"keep two instruments apart in register, \ timing and motion, \ not only in loudness"),
        ], font_size=26)
        with self.voiceover(
            "And in practice. An arranger doubles a melody in octaves to make one bigger voice, and in "
            "thirds to keep two. A choir director asks for exact togetherness where the parts should "
            "blend, and lets them breathe apart where they should be heard. A bass player moves "
            "against the melody to stay audible. And a mix engineer separates two instruments by "
            "register, timing and motion, not only by loudness."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"J. J. Fux, \ \textit{Gradus ad Parnassum} \ (1725; \ trans. A. Mann, \ \textit{The Study of Counterpoint}, \ 1965)",
             r"K. Jeppesen, \ \textit{Counterpoint: The Polyphonic Vocal Style of the Sixteenth Century} \ (1931; \ trans. 1939)",
             r"F. Salzer and C. Schachter, \ \textit{Counterpoint in Composition} \ (1969)",
             r"A. S. Bregman, \ \textit{Auditory Scene Analysis} \ (1990)"],
            [r"D. Huron, \ ``Tone and voice: a derivation of the rules of voice-leading from perceptual principles'', \ \textit{Music Perception} 19 (2001)",
             r"D. Huron, \ ``Asynchronous preparation of tonally fused intervals in polyphonic music'', \ \textit{Empirical Musicology Review} 3 (2008)",
             r"R. A. Rasch, \ ``The perception of simultaneous notes such as in polyphonic music'', \ \textit{Acustica} 40 (1978)",
             r"B. Schottstaedt, \ \textit{Automatic Species Counterpoint}, \ CCRMA report STAN-M-19 \ (1984)",
             r"K. Ebcio\u{g}lu, \ ``An expert system for harmonizing four-part chorales'', \ \textit{Computer Music Journal} 12 (1988)"],
            font_size=21)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        g = duet([[(76, 0, 4), (77, 4, 4), (79, 8, 4)], [(72, 0, 4), (72, 4, 4), (74, 8, 4)], [(67, 0, 4), (69, 4, 4), (71, 8, 4)], [(48, 0, 4), (53, 4, 4), (55, 8, 4)]],
                 colors=(UP_C, CF_C, UP_C, CF_C), width=6.0, height=2.6, lo=44, hi=82, thick=0.15).move_to(UP * 1.2)
        q = label(r"four voices at once: \ each a line, \ together a chord", font_size=30, color=EAR).move_to(DOWN * 0.8)
        nxt = VGroup(label(r"Part 17", font_size=32, color=GREY_B), label(r"Four Voices", font_size=50, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Two voices can be kept apart by a handful of rules. Four is a different problem. "
            "<bookmark mark='a'/> In a hymn or a chorale, every voice is a line, and every moment is a "
            "chord: Part 13's chords, and this part's rules, at the same time. How do four lines move "
            "from one chord to the next, each by the smallest step it can, without any two of them "
            "merging? <bookmark mark='b'/> Next time. Part 17: Four Voices."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
