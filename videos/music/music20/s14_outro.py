from __future__ import annotations

import numpy as np

from videos.music.music20.common import *  # noqa: F403
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
        c = clip("tune.variation20")
        head = VGroup(label(r"Variation 20", font_size=48, color=TUNE), label(r"one tune, \ combined with itself", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        titles = {"canon": r"the whole Tune, \ in canon at the fourth below, \ two beats behind",
                  "crab": r"a crab canon on its first three notes",
                  "exposition": r"a three-voice fugue exposition on its first phrase"}
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it has built. This part combined melodies with "
            "themselves. <bookmark mark='a'/> So the Tune is heard three ways. First the whole Tune as a canon: the "
            "stretto search, run on all of it, found that a second voice can follow two beats behind and a fourth "
            "below, almost cleanly, all the way through. Then the crab canon on its first three notes. And last, the "
            "fugue exposition of chapter nine."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            plan = VGroup(*[label(rf"{k + 1}. \ " + titles[n], font_size=28, color=WHITE) for k, n in enumerate(d["order"])]).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(DOWN * 0.2)
            self.play(LaggedStart(*[FadeIn(p_) for p_ in plan], lag_ratio=0.5), run_time=3.0)
        self.play(FadeOut(plan))
        shown = None
        with self.listen(c) as snd:
            window(snd, r"Variation 20", detail=r"a plucked string", corner=DL, tag_corner=DR)
            for name in d["order"]:
                snd.wait_until(name)
                if shown is not None:
                    self.remove(*shown)
                lines = d[name]
                total = max(n[1] + n[2] for ln in lines for n in ln)
                g = voices_roll(lines, width=11.4, height=3.2, total=total).move_to(DOWN * 0.3)
                t = label(titles[name], font_size=28, color=GREY_A).next_to(g, UP, buff=0.35)
                shown = [g, t]
                self.add(*shown)
                sing_voices(snd, g, lines, start=d["starts"][name], beat=d["beats"][name])
        if shown is not None:
            self.remove(*shown)
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).to_edge(DOWN, buff=0.25)
        cf = d["canon_faults"]
        with self.voiceover(
            f"Row twenty of the ledger. {say(v['seconds'])} seconds. The measurement: the whole Tune against itself two "
            f"beats later, a fourth below: {say(cf['dissonant'])} dissonant beats in {say(cf['beats'])}. A nursery tune, "
            "it turns out, was nearly a canon all along."
        ):
            self.play(FadeIn(led, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        r = load("rounds")
        c = load("canons")
        k = r["known_ranks"]
        tot = c["total_melodies"]
        card = objectives_card([
            rf"a round works when every piece agrees with every other: \ the known rounds ranked {k['Frère Jacques']}, \ {k['Row, Row, Row Your Boat']}, \ {k['Three Blind Mice']} of {r['n_tunes']}",
            rf"canons at every interval, \ counted exactly: \ about 1 in {tot / c['counts']['fifth']:.0f} melodies at the fifth, \ 1 in {tot / c['counts']['fourth']:.0f} at the fourth",
            r"four forms of a line: \ Klein's four-group",
            r"invertible counterpoint: \ at the octave, \ fifths become fourths",
            r"crab canons, \ counted; \ a canon that rises for ever in Shepard tones",
            r"the fugue: \ subject, \ tonal answer, \ countersubject by Viterbi search, \ stretto",
        ], title=r"What we found", font_size=24).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? A round works when every piece of a tune agrees with every other, and a program that "
            "knew nothing of rounds found the famous ones. <bookmark mark='a'/> Canons exist at every interval, "
            "counted exactly, rare but plentiful, hardest at the fourth and seventh. <bookmark mark='b'/> The four "
            "forms of a line make Klein's four-group. <bookmark mark='c'/> Lines can swap places, if they avoid what "
            "the swap would spoil. <bookmark mark='d'/> Crab canons are common, good ones rare, and a canon in Shepard "
            "tones can climb for ever. <bookmark mark='e'/> And a fugue's exposition can be built by rule, subject, "
            "tonal answer, countersubject and stretto, correctly and plainly."
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
            r"Write the tonal answer to a subject beginning G C B C D (in C major), \ and say which notes change and why.",
            r"Prove that a line and its retrograde inversion, \ sounded together, \ make the same intervals at times $t$ and $T-t$, \ "
            r"and say what that implies for a mirror crab canon.",
            r"\textbf{Ear.} \ The lab plays eight forms of three short phrases. \ For each, \ say: \ the phrase, \ inverted, \ backwards, \ or both?",
            r"\textbf{Build.} \ Give the stretto finder a fugue subject of your choice in score, \ "
            r"find all its strettos, \ and compare them with those the composer used.",
            r"$\bigstar$ \ Design an experiment that tells whether listeners follow a fugue's entries by ear, \ or only on paper.",
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
            (r"form: \ a fugue's shape over minutes", [21]),
            (r"the Renaissance: \ imitation, \ the point of imitation", [24]),
            (r"the Baroque: \ the fugue in its home", [25]),
            (r"twelve tones: \ the forty-eight forms of a row", [29]),
            (r"phasing and tiling canons: \ Reich and Vuza", [30, 33]),
            (r"the tracker and the tempo canon", [53]),
        ], font_size=26)
        with self.voiceover(
            "Where does this come back? In form, where a fugue's shape over minutes is the question. In the "
            "Renaissance, whose polyphony is built from imitation, and the Baroque, the fugue's home. In twelve-tone "
            "music, where the four forms meet twelve transpositions. In Steve Reich's phasing and in tiling canons, and "
            "in a tempo canon no human could play."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"choirs and classrooms", r"teach harmony with rounds: \ every singer learns every part"),
            (r"keyboard players", r"play a fugue one voice at a time, \ then two, \ then all"),
            (r"songwriters", r"let a backing line answer the melody a bar later: \ a canon in disguise"),
            (r"producers", r"delay and echo are canons at the unison: \ set the delay to a beat or a bar"),
        ], font_size=26)
        with self.voiceover(
            "And in practice. Choirs and classrooms teach harmony through rounds, since every singer learns every "
            "part. Keyboard players learn fugues a voice at a time. Songwriters let a backing line answer the melody a "
            "bar later. And a producer's delay effect is a canon at the unison, which is why it sounds best set to a "
            "beat or a bar."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"A. Mann, \ \textit{The Study of Fugue} \ (1958)",
             r"R. Gauldin, \ \textit{A Practical Approach to Eighteenth-Century Counterpoint} \ (1988)",
             r"D. R. Hofstadter, \ \textit{Gödel, Escher, Bach} \ (1979)",
             r"C. Wolff, \ \textit{Johann Sebastian Bach: \ The Learned Musician} \ (2000)",
             r"J. S. Bach, \ \textit{Musikalisches Opfer} \ (1747); \ \textit{Die Kunst der Fuge} \ (1751)"],
            [r"M. Giraud, \ R. Groult, \ E. Leguy and F. Levé, \ ``Computational fugue analysis'', \ \textit{Computer Music Journal} 39 (2015)",
             r"D. Cope, \ \textit{Experiments in Musical Intelligence} \ (1996)",
             r"C.-Z. A. Huang and others, \ ``Counterpoint by convolution'', \ ISMIR \ (2017)",
             r"R. N. Shepard, \ ``Circularity in judgments of relative pitch'', \ \textit{JASA} 36 \ (1964)",
             r"W. J. Dowling, \ ``Recognition of melodic transformations: \ inversion, \ retrograde, \ and retrograde inversion'', \ \textit{Perception \& Psychophysics} 12 (1972)"],
            font_size=19)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        q = label(r"what holds three minutes of music together?", font_size=30, color=EAR).move_to(UP * 0.4)
        top = label(r"lines, \ combined, \ a few bars at a time", font_size=30, color=GREY_A).to_edge(UP, buff=0.8)
        nxt = VGroup(label(r"Part 21", font_size=32, color=GREY_B), label(r"Form", font_size=50, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "This part combined lines a few bars at a time. <bookmark mark='a'/> But a fugue, a sonata or a song lasts "
            "minutes, and a listener follows it. What holds three minutes of music together, and can a program find "
            "the shape from the sound alone? <bookmark mark='b'/> Next time. Part 21: Form."
        ) as vo:
            self.play(FadeIn(top))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
