from __future__ import annotations

import numpy as np

from videos.music.music35.common import *  # noqa: F403
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
        c = clip("tune.variation35")
        head = VGroup(label(r"Variation 35", font_size=48, color=TUNE), label(r"the Tune in three maqamat", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        rows_ = VGroup()
        for name, col in (("Rast", TUNE), ("Bayati", BLUE), ("Hijaz", EAR)):
            notes = [[cc / 100.0, sum(x[1] for x in d["notes"][:i]), d["notes"][i][1]] for i, cc in enumerate(d["melodies"][name])]
            r = mroll(notes, width=8.4, height=1.0, lo=-1, hi=10, color=col, bar_h=0.1)
            rows_.add(VGroup(label(name, font_size=22, color=col), r).arrange(RIGHT, buff=0.5))
        tq = label(r"first: \ a short taqs\=\i m in Rast", font_size=20, color=GREY_A)
        g = VGroup(tq, *rows_).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(DOWN * 0.2)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> First a short taqsim of "
            "ours in Rast. Then the Tune's first two phrases three times over the darbuka's maqsum: in Rast on C, where its E "
            "becomes E half-flat; in Bayati on D, where its second and third degrees both drop; and in Hijaz on D, with the "
            "augmented second between the second and third degrees. The melody's shape stays; its colour changes completely."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g))
        with self.listen(c) as snd:
            window(snd, r"Variation 35", detail=r"an oud model, \ darbuka", corner=DL, tag_corner=DR)
            pulse(snd, tq, d["starts"]["taqsim"], d["starts"]["Rast"] - 0.5, buff=0.06)
            for i, name in enumerate(("Rast", "Bayati", "Hijaz")):
                flash(snd, rows_[i][1].notes, [d["starts"][name] + sum(x[1] for x in d["notes"][:j]) * d["beat"] for j in range(len(d["notes"]))], hot=WHITE, base=[TUNE, BLUE, EAR][i])
        self.play(FadeOut(g))
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            f"Row thirty-five of the ledger: {say(v['seconds'])} seconds; the measurement is how many of the Tune's notes move "
            "in each maqam."
        ):
            self.play(FadeIn(led, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"ajnas, \ three or four notes, \ with steps of 100, \ 150, \ 200 and 300 cents",
            r"maqamat: \ two ajnas joined, \ each with a path",
            r"neutral intervals since al-F\=ar\=ab\=\i; \ 24 steps fit them, \ 53 fit the just ones",
            r"Cairo 1932: \ the grid against the musicians' practice",
            r"Turkish commas and Persian dastgahs: \ the same question, \ answered differently",
            r"iq\=a`, \ taqs\=\i m, \ the oud and the qanun's levers",
        ], title=r"What we found", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? Ajnas of three or four notes with steps of one hundred, one hundred and fifty, two hundred and "
            "three hundred cents. <bookmark mark='a'/> Maqamat built from two ajnas, each with its own path. "
            "<bookmark mark='b'/> Neutral intervals going back to al-Farabi, fitted by twenty-four equal steps, while "
            "fifty-three fit the just ones. <bookmark mark='c'/> Cairo's congress, where the grid met the musicians. "
            "<bookmark mark='d'/> Turkish commas and Persian dastgahs, the same question answered differently. "
            "<bookmark mark='e'/> And rhythmic cycles, the taqsim, and instruments built to play between the keys."
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
            r"Build maqam Saba on D in cents, \ and find the nearest steps of 24 and of 53 equal divisions for each note.",
            r"Prove that a chain of 17 pure fourths, \ folded into the octave, \ gives steps of only two sizes plus one comma.",
            r"\textbf{Ear.} \ The lab plays phrases in Rast, \ Bayati and Hijaz; \ name the maqam of each.",
            r"\textbf{Build.} \ Add mandal levers to the oud model's qanun cousin: \ a string set that retunes mid-phrase.",
            r"$\bigstar$ \ What determines where a musician places a neutral note?",
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
            (r"gamelan's other tunings", [36]),
            (r"timelines and cycles", [37]),
            (r"improvisation and memory", [42]),
            (r"universals across musics", [47]),
            (r"pitch tracking and music information retrieval", [61]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? Next, in gamelan, with tunings of its own. In timelines and cycles. In improvisation "
            "and memory. In what all musics share. And in the pitch tracking that measures them."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"oud players", r"place each note by ear, \ maqam by maqam"),
            (r"qanun players", r"flip levers mid-phrase to modulate"),
            (r"producers", r"retune keyboards and software for maqam"),
            (r"teachers", r"teach sayr and taqsim by imitation, \ not only by scale"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Oud players place each note by ear, maqam by maqam. Qanun players flip levers mid-phrase to "
            "modulate. Producers retune keyboards and software for maqam. And teachers teach paths and improvisation by "
            "imitation, not only by scale."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"S. Marcus, \ \textit{Music in Egypt} \ (2007)",
             r"H. H. Touma, \ \textit{The Music of the Arabs} \ (1996)",
             r"H. Farhat, \ \textit{The Dastgah Concept in Persian Music} \ (1990)",
             r"K. Signell, \ \textit{Makam: \ Modal Practice in Turkish Art Music} \ (1977)"],
            [r"B. Bozkurt, \ O. Yarman, \ M. K. Karao\u{g}lu, \ C. Akkoç, \ `Weighing diverse theoretical models on Turkish maqam music' \ (2009)",
             r"A. J. Racy, \ \textit{Making Music in the Arab World} \ (2003)",
             r"J. Farraj, \ S. Abu Shumays, \ \textit{Inside Arabic Music} \ (2019)",
             r"al-F\=ar\=ab\=\i, \ \textit{Kit\=ab al-M\=us\=\i q\=\i\ al-Kab\=\i r} \ (10th century)"],
            font_size=18)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        q = label(r"what if the instruments themselves set the tuning, \ and no two orchestras agreed?", font_size=30, color=EAR).move_to(UP * 0.4)
        top = label(r"Act VI: \ many musics", font_size=30, color=GREY_A).to_edge(UP, buff=0.8)
        nxt = VGroup(label(r"Part 36", font_size=32, color=GREY_B), label(r"Bronze and Silk", font_size=50, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Maqam places its notes by ear. <bookmark mark='a'/> What if the instruments themselves set the tuning, and no two "
            "orchestras agreed? <bookmark mark='b'/> Next time. Part 36: Bronze and Silk."
        ) as vo:
            self.play(FadeIn(top))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
