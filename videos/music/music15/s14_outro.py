from __future__ import annotations

import numpy as np

from videos.music.music15.common import *  # noqa: F403
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
        c = clip("tune.variation15")
        head = VGroup(label(r"Variation 15", font_size=48, color=TUNE), label(r"one tune, \ twelve keys", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.35)
        clock = fifths_clock(radius=1.75, font_size=26, signatures=True).move_to(LEFT * 4.0 + DOWN * 0.3)
        kb = keys(36, 89, width=7.6, height=1.2).move_to(RIGHT * 2.6 + DOWN * 1.6)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it has built. This part built "
            "keys, and a way to move between them. <bookmark mark='a'/> So the Tune will travel. Two "
            "phrases at home in C; then each phrase a fifth lower than the last, all the way round the "
            "circle: F, B flat, E flat, and on through the flats and back through the sharps, until it "
            "reaches C again. Each phrase ends by turning its own home chord into the dominant seventh "
            "of the next key. <bookmark mark='b'/> And at the very end, where everything promises the "
            "tonic, listen for what it does. The key finder will follow along, and say where it thinks "
            "we are."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(clock), FadeIn(kb), run_time=1.5)
            for pc in (5, 10, 3, 8, 1, 6, 11, 4, 9, 2, 7, 0):
                self.play(Indicate(clock.cell[pc], color=TUNE, scale_factor=1.4), run_time=0.45)
            vo.wait_until("b")
            self.play(Indicate(clock.cell[0], color=EAR, scale_factor=1.5))
        shown = None
        marker = Circle(radius=0.36, color=TUNE, stroke_width=4).move_to(clock.at(0))
        self.add(marker)
        with self.listen(c) as snd:
            window(snd, r"Variation 15", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            ch_t = [t for ph in d["phrases"] for t in ph["chord_times"]]
            ch_m = [ch for ph in d["phrases"] for ch in ph["chords"]]
            mel_t = [t for ph in d["phrases"] for t in ph["times"]]
            mel_m = [m for ph in d["phrases"] for m in ph["melody"]]
            light_chords(snd, kb, ch_m, ch_t, end=c.duration, color=BLUE, melody=mel_m, melody_times=mel_t, melody_color=GOLD)
            for k, ph in enumerate(d["phrases"]):
                snd.wait_until(f"phrase{k}")
                if shown is not None:
                    self.remove(*shown)
                marker.move_to(clock.at(ph["pc"]))
                name = label(tex(ph["key"]), font_size=44, color=TUNE).move_to(RIGHT * 2.6 + UP * 1.7)
                sig = ph["signature"]
                sg = label("no sharps or flats" if sig == 0 else (rf"{sig} sharp{'s' if sig > 1 else ''}" if sig > 0 else rf"{-sig} flat{'s' if sig < -1 else ''}"), font_size=26, color=GREY_A).next_to(name, DOWN, buff=0.2)
                found = label(rf"the key finder says: \ {tex(ph['found'])}", font_size=26, color=WHITE if ph["right"] else EAR).next_to(sg, DOWN, buff=0.3)
                shown = [name, sg, found]
                self.add(name, sg, found)
        kb.clear()
        self.remove(*shown, kb, clock, marker)
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            f"Row fifteen of the ledger. {say(v['seconds'])} seconds. The measurement: the key finder "
            f"named the key of {say(d['found_right'])} of the {say(d['of'])} phrases, though each "
            "lasted only a few seconds. And the ending was the deceptive cadence of chapter four: the "
            "dominant of C, and then, where C should have been, A minor. After twelve keys, the Tune "
            "came all the way home and did not go in."
        ):
            self.play(FadeIn(led, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        f = load("finder")
        card = objectives_card([
            r"a key is a ranking of all twelve notes: \ tonic, \ triad, \ scale, \ the rest",
            r"the ranking matches how often notes occur, \ and is learned by listening",
            r"chords have three jobs: \ rest, \ leave, \ pull back; \ four cadences punctuate",
            rf"a key finder that counts is right {100 * f['full']['counts']['accuracy']:.0f} times in a hundred, \ and needs about five notes",
            r"the rarest interval, \ the tritone, \ is the best clue; \ the Tune has none",
            r"24 keys lie on a torus; \ music moves on it by pivot chords and new leading notes",
        ], title=r"What we found", font_size=26).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? A key is a ranking of all twelve notes: the tonic, then its triad, then "
            "the scale, then the rest. <bookmark mark='a'/> That ranking matches how often notes occur "
            "in music, and listeners learn it by listening. <bookmark mark='b'/> In a key, chords have "
            "three jobs, rest, leave and pull back, and four cadences punctuate the phrases. "
            "<bookmark mark='c'/> A key finder that simply counts is right "
            f"{say(100 * f['full']['counts']['accuracy'])} times in a hundred on our tunes, and needs "
            "about five notes. <bookmark mark='d'/> The rarest interval, the tritone, is the best clue "
            "to a key; the Tune has none, and gets by on weights. <bookmark mark='e'/> And the "
            "twenty-four keys lie on a torus, where music travels by pivot chords and new leading notes."
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
            r"Name the key with four sharps and its relative minor; \ the key with three flats and its parallel minor. \ How many notes does each pair share, \ "
            r"and how many steps apart are E major and E$\flat$ major on the circle of fifths?",
            r"A major scale's interval vector is $\langle 2, 5, 4, 3, 6, 1 \rangle$. \ Prove that a pair of notes forming interval class $k$ lies in exactly $v_k$ major scales "
            r"(twice that for the tritone), \ and so explain why the tritone is the best clue to a key.",
            r"\textbf{Ear.} \ The lab plays eight short progressions. \ Name each cadence: \ authentic, \ half, \ plagal or deceptive.",
            r"\textbf{Build.} \ With \texttt{key.learn\_profiles}, \ count profiles from the corpus and use them in \texttt{key.bayes\_key}. \ Test each tune with profiles learnt from the others. \ "
            r"Which tunes are still misread, \ and what do they have in common?",
            r"$\bigstar$ \ Design an experiment to tell whether listeners store a key as counts of notes or as a grammar of chords. \ What would each account predict for a passage with the right notes in the wrong order?",
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
            (r"two melodies in one key: \ counterpoint", [16]),
            (r"four voices, \ and how chords connect", [17, 18]),
            (r"chromatic harmony: \ far keys, \ quickly", [19]),
            (r"form: \ leaving the home key, \ and returning", [21]),
            (r"the geometry of keys and chords", [32]),
            (r"machines that find the key in a recording", [62]),
        ], font_size=26)
        with self.voiceover(
            "Where does this come back? Act Three begins at once, with two melodies in one key, and then "
            "four. Chromatic harmony is the art of reaching far keys quickly. Musical form, a whole "
            "sonata, is a journey away from the home key and back. The torus returns as geometry. And "
            "finding the key of a recording, not a score, is a standard task for the machines of the "
            "last act."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"singers and accompanists", r"move a song to the key that suits the voice: \ everything keeps its job"),
            (r"songwriters", r"lift the last chorus a step, \ or turn to the relative minor for the bridge"),
            (r"DJs", r"mix tracks whose keys are neighbours on the circle of fifths"),
            (r"arrangers", r"plan the keys of a set, \ so that each song arrives as a fresh room"),
        ], font_size=26)
        with self.voiceover(
            "And in practice. A singer moves a song to the key that suits the voice, and every note "
            "keeps its job. A songwriter lifts the last chorus up a step, or goes to the relative minor "
            "for the bridge. A DJ mixes tracks whose keys are neighbours on the circle of fifths, so "
            "that the join does not jar. And an arranger plans the keys of a whole programme, so that "
            "each song arrives as a fresh room."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"C. L. Krumhansl, \ \textit{Cognitive Foundations of Musical Pitch} \ (1990)",
             r"D. Temperley, \ \textit{The Cognition of Basic Musical Structures} \ (2001); \ \textit{Music and Probability} \ (2007)",
             r"F. Lerdahl, \ \textit{Tonal Pitch Space} \ (2001)",
             r"S. Laitz, \ \textit{The Complete Musician} \ (4th ed., 2015), \ chs. 7--12"],
            [r"C. L. Krumhansl and E. J. Kessler, \ ``Tracing the dynamic changes in perceived tonal organization in a spatial representation of musical keys'', \ \textit{Psychological Review} 89 (1982)",
             r"M. A. Castellano, J. J. Bharucha and C. L. Krumhansl, \ ``Tonal hierarchies in the music of North India'', \ \textit{J. Exp. Psychology: General} 113 (1984)",
             r"R. Browne, \ ``Tonal implications of the diatonic set'', \ \textit{In Theory Only} 5 (1981)",
             r"J. Albrecht and D. Huron, \ ``A statistical approach to tracing the historical development of major and minor pitch distributions, 1400--1750'', \ \textit{Music Perception} 31 (2014)",
             r"T. de Clercq and D. Temperley, \ ``A corpus analysis of rock harmony'', \ \textit{Popular Music} 30 (2011)"],
            font_size=21)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        r1 = roll([0, 2, 4, 5, 7, 5, 4, 2, 0], width=7.0, height=1.5, lo=-10, hi=9, lines=(), color=TUNE).move_to(UP * 1.6)
        r2 = roll([0, -1, -3, -5, -8, -7, -5, -3, -8][:9], width=7.0, height=1.5, lo=-10, hi=9, lines=(), color=BLUE).move_to(UP * 0.2)
        q = label(r"two melodies at once. \ When do they stay two, \ and when do they melt into one?", font_size=30, color=EAR).move_to(DOWN * 1.3)
        nxt = VGroup(label(r"Act III, \ Part 16", font_size=32, color=GREY_B), label(r"Two Voices", font_size=50, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "That is the end of Act Two. We have notes, written down; rhythm; scales; chords; melody; "
            "and a home for all of them. One thing we have not yet done is the thing that most sets "
            "written music apart: <bookmark mark='a'/> two melodies at the same time, each a good tune, "
            "and both making sense together. When do two lines stay two, and when do they melt into "
            "one? <bookmark mark='b'/> Act Three begins there. Part 16: Two Voices."
        ) as vo:
            self.play(FadeIn(r1))
            vo.wait_until("a")
            self.play(FadeIn(r2), FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
