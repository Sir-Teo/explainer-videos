from __future__ import annotations

import numpy as np

from videos.music.music36.common import *  # noqa: F403
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
        c = clip("tune.variation36")
        head = VGroup(label(r"Variation 36", font_size=48, color=TUNE), label(r"the Tune in silk, \ then in bronze", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        qin = VGroup(*[VGroup(label(rf"{q['string']}", font_size=17, color=TUNE), label(rf"/{q['partial']}", font_size=13, color=GREY_A)).arrange(DOWN, buff=0.04) for q in d["qin"]]).arrange(RIGHT, buff=0.32)
        ql = label(r"qin: \ string and harmonic for each note", font_size=18, color=TUNE)
        bal = VGroup(*[Square(0.42, stroke_color=GREY_B, stroke_width=1) for _ in d["balungan"]]).arrange(RIGHT, buff=0.04)
        bl = label(r"gamelan: \ balungan, \ four interlocking pulses per beat, \ kenong and gong", font_size=18, color=BLUE)
        g = VGroup(VGroup(ql, qin).arrange(DOWN, buff=0.25), VGroup(bl, bal).arrange(DOWN, buff=0.25)).arrange(DOWN, buff=0.7).move_to(DOWN * 0.2)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> First in silk: each of "
            "its notes as a natural harmonic on a qin tuned by pure fifths and fourths, the program choosing the string and "
            f"harmonic nearest each note; the worst lies {say(round(d['worst']))} cents from the piano. Then in bronze: the "
            "Tune as a balungan in an illustrative pelog, one note a beat, with an interlocking figure at four pulses a "
            "beat, a kenong every four beats and the gong at the end."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g))
        with self.listen(c) as snd:
            window(snd, r"Variation 36", detail=r"plucked string, \ bars, \ gong", corner=DL, tag_corner=DR)
            for i, (p, a, du) in enumerate(d["melody"]):
                pulse(snd, qin[i], d["starts"]["qin"] + a * d["unit"], d["starts"]["qin"] + (a + du) * d["unit"] - 0.03, buff=0.04)
            for i in range(len(d["balungan"])):
                pulse(snd, bal[i], d["starts"]["gamelan"] + i * d["beat"], d["starts"]["gamelan"] + (i + 1) * d["beat"] - 0.03, buff=0.03)
        self.play(FadeOut(g))
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            f"Row thirty-six of the ledger: {say(v['seconds'])} seconds; the measurement is the qin's worst error and the "
            "balungan's length."
        ):
            self.play(FadeIn(led, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"an almond-shaped bell sounds two notes, \ a third apart",
            r"twelve l\"u by cutting a pipe; \ 53 fifths come within 3.6 cents of closing",
            r"five notes, \ five modes; \ the qin's hui are harmonic nodes",
            r"heterophony: \ one melody, \ several versions at once",
            r"slendro and pelog without a standard; \ bronze spectra and their dissonance",
            r"ombak, \ the gong cycle and interlocking parts",
        ], title=r"What we found", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? An almond-shaped bell sounds two notes, a third apart. <bookmark mark='a'/> Twelve pitches "
            "come from cutting a pipe, and fifty-three fifths come within three and a half cents of closing. "
            "<bookmark mark='b'/> Five notes make five modes, and the qin's studs are harmonic nodes. <bookmark mark='c'/> "
            "Heterophony plays one melody several ways at once. <bookmark mark='d'/> Slendro and pelog have no standard, and "
            "bronze has its own dissonance. <bookmark mark='e'/> And the gamelan shimmers by design, keeps time with gongs, "
            "and splits fast figures between players."
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
            r"Using the rule of three from a length of 81, \ compute the first seven lengths and their pitches in cents.",
            r"Prove that n pure fifths can never exactly equal a whole number of octaves.",
            r"\textbf{Ear.} \ The lab plays pairs of metallophones; \ say which pairs are tuned apart, \ and how fast they beat.",
            r"\textbf{Build.} \ Write a colotomic renderer for ladrang \ (32 beats) \ and play a balungan of your own in it.",
            r"$\bigstar$ \ Do gamelan tunings fit their instruments' spectra?",
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
            (r"timelines and cycles", [37]),
            (r"scales and universals", [47]),
            (r"synthesis for any tuning and timbre", [52]),
            (r"rooms and the sound of an ensemble", [55]),
            (r"acoustics and archaeology as research", [67]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? Next, in timelines and cycles. In scales and universals. In synthesis for any tuning "
            "and timbre. In the sound of an ensemble in a room. And in acoustics and archaeology as research."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"gamelan makers", r"tune each set as a whole, \ by ear, \ with its own embat"),
            (r"qin players", r"learn pieces from tablature and teachers"),
            (r"composers", r"write for gamelan in Europe, \ America and Asia"),
            (r"museums", r"cast replica bells to hear what originals sounded like"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Gamelan makers tune each set as a whole, by ear, with its own character. Qin players learn "
            "pieces from tablature and teachers. Composers write for gamelan in Europe, America and Asia. And museums cast "
            "replica bells to hear what the originals sounded like."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"L. von Falkenhausen, \ \textit{Suspended Music} \ (1993)",
             r"M. Tenzer, \ \textit{Gamelan Gong Kebyar} \ (2000)",
             r"Sumarsam, \ \textit{Gamelan: \ Cultural Interaction and Musical Development in Central Java} \ (1995)",
             r"W. A. Sethares, \ \textit{Tuning, \ Timbre, \ Spectrum, \ Scale} \ (2nd ed. 2005), \ chapter 10"],
            [r"W. Surjodiningrat, \ P. J. Sudarjana, \ A. Susanto, \ \textit{Tone Measurements of Outstanding Javanese Gamelans} \ (1972)",
             r"Chen Cheng-Yih \ (ed.), \ \textit{Two-Tone Set-Bells of Marquis Yi} \ (1994)",
             r"R. van Gulik, \ \textit{The Lore of the Chinese Lute} \ (1940)",
             r"K. G. Y. Robinson, \ `A critical study of Chu Tsai-y\"u's contribution to the theory of equal temperament' \ (1980)"],
            font_size=18)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        q = label(r"what if the cycle itself were the music: \ a pattern struck on a bell, \ over and over?", font_size=30, color=EAR).move_to(UP * 0.4)
        top = label(r"Act VI: \ many musics", font_size=30, color=GREY_A).to_edge(UP, buff=0.8)
        lead = label(r"The gamelan keeps time with gongs.", font_size=24, color=WHITE).move_to(UP * 1.7)
        lead.scale_to_fit_width(min(lead.width, 12.5))
        nxt = VGroup(label(r"Part 37", font_size=32, color=GREY_B), label(r"Timelines", font_size=50, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "The gamelan keeps time with gongs. <bookmark mark='a'/> What if the cycle itself were the music, a pattern struck "
            "on a bell, over and over, while everything else moves around it? <bookmark mark='b'/> Next time. Part 37: "
            "Timelines."
        ) as vo:
            self.play(FadeIn(top), FadeIn(lead))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
