from __future__ import annotations

import numpy as np

from videos.music.music41.common import *  # noqa: F403
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
        c = clip("tune.variation41")
        head = VGroup(label(r"Variation 41", font_size=48, color=TUNE), label(r"the Tune, \ eight ways", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        titles = d["titles"]
        cells = VGroup(*[label(rf"{k + 1}. \ " + t.replace("'", "'"), font_size=18, color=TUNE if k == 7 else WHITE) for k, t in enumerate(titles)]).arrange_in_grid(rows=4, cols=2, buff=(0.8, 0.35), col_alignments="ll").move_to(DOWN * 1.2)
        mel = d["melody"]
        roll = mroll(mel, width=6.0, height=1.2, lo=58, hi=72, color=TUNE, total=8, bar_h=0.14).move_to(UP * 1.25)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> Here, its first phrase in "
            "eight orchestrations: strings; woodwinds; brass; flute and clarinet in unison; Ravel's horn, celesta and "
            "piccolos; a melody of timbres; a tutti in octaves; and last, each note voiced like the vowel ah, by the "
            "instruments the solver chose, on the same harmonics of every note."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cells), FadeIn(roll))
        beat = d["beat"]
        with self.listen(c) as snd:
            window(snd, r"Variation 41", kind="synthesized", detail=r"additive instruments from measured spectra", corner=DL, tag_corner=DR)
            for k, t0 in enumerate(d["starts"]):
                pulse(snd, cells[k], t0, t0 + 8 * beat, buff=0.08)
                flash(snd, roll.notes, [t0 + a * beat for _, a, _ in mel], hot=WHITE, base=TUNE)
        self.play(FadeOut(cells), FadeOut(roll))
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            f"Row forty-one of the ledger: {say(v['seconds'])} seconds; the measurement is how closely the solver matched the "
            "vowel."
        ):
            self.play(FadeIn(led, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"an orchestra resynthesised from the series' physical models",
            r"ranges, \ registers, \ transposing instruments",
            r"louder is brighter; \ eight players are about 10 dB, \ not 18, \ louder",
            r"doubling makes new timbres; \ balance is a separate question",
            r"spacing follows the harmonic series; \ low thirds are rough",
            r"instruments on harmonics fuse; \ a solver can spell a vowel",
        ], title=r"What we found", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? An orchestra can be resynthesised from the series' physical models. <bookmark mark='a'/> "
            "Instruments have ranges, registers, and sometimes transposed parts. <bookmark mark='b'/> Louder is brighter, and "
            "eight players are about ten decibels louder than one, not eighteen. <bookmark mark='c'/> Doubling makes new "
            "timbres, and balance is a separate question. <bookmark mark='d'/> Spacing follows the harmonic series, because "
            "low thirds are rough. <bookmark mark='e'/> And instruments placed on harmonics fuse into one sound, so a solver "
            "can spell a vowel with an orchestra."
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
            r"How many violins does it take to be 6 dB louder than four violins?",
            r"Prove that n incoherent equal sources are 10 log$_{10}$n dB louder than one, \ and coherent ones 20 log$_{10}$n.",
            r"\textbf{Ear.} \ The lab plays one held note on sections of different sizes; \ say how many players each time.",
            r"\textbf{Build.} \ Give the solver a target of your own \ (another vowel, \ a bell) \ and compare budgets.",
            r"$\bigstar$ \ Can blend and layering be predicted from the score alone?",
        ], font_size=22)
        with self.voiceover(
            "Five problems. One to compute, one to prove, one for your ears, one to build, and a research problem, marked "
            "with a star. Solutions are in this part's notes. Pause here."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.25), run_time=3.0)
        self.wait(5.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        pay = payoff_card([
            (r"composing as search", [42]),
            (r"performing together", [43]),
            (r"music for picture and play", [44]),
            (r"the auditory scene and timbre space", [45]),
            (r"synthesis from physical models", [52]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? In composing as search. In performing together. In music for picture and play. In "
            "the auditory scene and timbre space. And in synthesis from physical models."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"orchestrators", r"choose the texture, \ then the instruments, \ then check balance in rehearsal"),
            (r"film composers", r"mock up scores with sample libraries before the orchestra plays"),
            (r"arrangers", r"double melodies in octaves to carry, \ and keep low intervals wide"),
            (r"conductors", r"rebalance in the hall, \ where the room changes everything"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Orchestrators choose the texture, then the instruments, then check the balance in rehearsal. "
            "Film composers mock up their scores with sample libraries before an orchestra plays a note. Arrangers double "
            "melodies in octaves so they carry, and keep low intervals wide. And conductors rebalance in the hall, where the "
            "room changes everything."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"H. Berlioz, \ \textit{Treatise on Instrumentation} \ (1844)",
             r"N. Rimsky-Korsakov, \ \textit{Principles of Orchestration} \ (1913)",
             r"S. Adler, \ \textit{The Study of Orchestration} \ (1982; \ 4th ed. 2016)",
             r"A. Schoenberg, \ \textit{Harmonielehre} \ (1911)"],
            [r"G. J. Sandell, \ `Roles for spectral centroid and other factors in determining blended instrument pairings' \ (1995)",
             r"S. McAdams and others, \ `Perceptual scaling of synthesized musical timbres' \ (1995)",
             r"J. M. Grey, \ `Multidimensional perceptual scaling of musical timbres' \ (1977)",
             r"P. Esling, \ G. Carpentier and C. Agon, \ on computer-aided orchestration \ (2010)"],
            font_size=18)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        q = label(r"if orchestrating is search, \ is composing search too?", font_size=30, color=EAR).move_to(UP * 0.4)
        top = label(r"Act VII: \ the craft", font_size=30, color=GREY_A).to_edge(UP, buff=0.8)
        lead = label(r"Orchestration searched among instruments for a sound.", font_size=24, color=WHITE).move_to(UP * 1.7)
        nxt = VGroup(label(r"Part 42", font_size=32, color=GREY_B), label(r"Composing", font_size=50, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Orchestration searched among instruments for a sound. <bookmark mark='a'/> If orchestrating is search, is "
            "composing search too? <bookmark mark='b'/> Next time. Part 42: Composing."
        ) as vo:
            self.play(FadeIn(top), FadeIn(lead))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
