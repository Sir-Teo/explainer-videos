from __future__ import annotations

import numpy as np

from videos.music.music34.common import *  # noqa: F403
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
        c = clip("tune.variation34")
        t = load("tala")["talas"]["Teentaal"]
        head = VGroup(label(r"Variation 34", font_size=48, color=TUNE), label(r"the Tune as Bilawal", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        alap = sargam([p for p, _ in d["alap"]], size=24, color=BLUE)
        al = VGroup(label(r"\=al\=ap, \ over the drone:", font_size=19, color=BLUE), alap).arrange(RIGHT, buff=0.4).move_to(UP * 1.6)
        g1 = tala_grid([""] * 16, t["vibhags"], t["marks"], cell=0.5, size=13).move_to(UP * 0.1)
        second = t["theka"][:4] + [""] * 12
        g2 = tala_grid(second, t["vibhags"], t["marks"], cell=0.5, size=13).move_to(DOWN * 1.5)
        for k in range(3):
            for i in range(3):
                if 4 + 5 * k + i < 16:
                    g2.cells[4 + 5 * k + i][0].set_fill(EAR, opacity=0.3)
        l1 = label(r"gat: \ the Tune, \ one cycle of Teentaal", font_size=17, color=TUNE).next_to(g1, LEFT, buff=0.3)
        l2 = label(r"tihai from beat 5", font_size=17, color=EAR).next_to(g2, LEFT, buff=0.3)
        l1.scale_to_fit_width(min(l1.width, 2.2)).next_to(g1, LEFT, buff=0.3)
        l2.scale_to_fit_width(min(l2.width, 2.2)).next_to(g2, LEFT, buff=0.3)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> The Tune is in the major "
            "scale, so here it supplies a simplified Bilawal-based sketch, not a complete idiomatic raga performance. First a short alap on its opening phrase, slow and free, with glides, "
            "over the drone. Then its first two phrases as a gat, one cycle of Teentaal with the tabla. Then a second cycle: "
            "four beats of theka and a tihai from beat five, the melody falling Ga, Re, Sa three times, the last Sa landing on "
            "sam."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(al), FadeIn(g1), FadeIn(g2), FadeIn(l1), FadeIn(l2))
        with self.listen(c) as snd:
            window(snd, r"Variation 34", kind="synthesized", detail=r"bowed tone, \ tanpura, \ tabla", corner=DL, tag_corner=DR)
            n = len(d["alap"])
            t0 = 0.4
            for i, (p, dur) in enumerate(d["alap"]):
                pulse(snd, alap[i], t0, t0 + dur - 0.05, buff=0.05)
                t0 += dur
            b = d["beat"]
            for i in range(16):
                pulse(snd, g1.cells[i][0], d["gat_start"] + i * b, d["gat_start"] + (i + 1) * b - 0.02, buff=0.03)
                pulse(snd, g2.cells[i][0], d["gat_start"] + (16 + i) * b, d["gat_start"] + (17 + i) * b - 0.02, buff=0.03)
        self.play(FadeOut(al), FadeOut(g1), FadeOut(g2), FadeOut(l1), FadeOut(l2))
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            f"Row thirty-four of the ledger: {say(v['seconds'])} seconds; the measurement is the alap, the cycle and the "
            "tihai's arithmetic."
        ):
            self.play(FadeIn(led, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"the drone: \ a tanpura's curved bridge pushes energy into high partials",
            r"swara and shruti: \ twelve positions, \ and intonation that varies with raga and phrase",
            r"a raga: \ ascent, \ descent, \ phrases, \ gamakas, \ time and mood",
            r"10 thaats among 32 scales; \ 72 melakartas, \ generated and numbered",
            r"tala: \ cycles of claps and waves; \ the tihai equation, \ solved",
            r"a performance: \ \=al\=ap, \ jor, \ jh\=al\=a, \ gat",
        ], title=r"What we found", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? The drone, and a curved bridge that pushes energy into high partials. "
            "<bookmark mark='a'/> Twelve positions for the notes, and intonation that varies with raga and phrase. "
            "<bookmark mark='b'/> A raga as ascent, descent, phrases, ornaments, time and mood. <bookmark mark='c'/> Ten "
            "thaats among thirty-two scales, and seventy-two melakartas. <bookmark mark='d'/> Tala, and the tihai as an "
            "equation. <bookmark mark='e'/> And the arc of a performance, from no pulse to fast pulse."
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
            r"Find every tihai in Jhaptaal \ (10 beats) \ that starts on beat 6, \ with phrases up to 6 beats.",
            r"Prove that there are exactly 72 melakartas under Venkatamakhin's rule.",
            r"\textbf{Ear.} \ The lab plays phrases in Bilawal and in Yaman; \ name the raga of each.",
            r"\textbf{Build.} \ Add a moving thread to the tanpura model, \ and measure how the buzz changes.",
            r"$\bigstar$ \ What do listeners attend to when they recognise a raga?",
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
            (r"maqam, \ another modal system", [35]),
            (r"timelines and cycles across the world", [37]),
            (r"improvisation and composing", [42]),
            (r"universals across musics", [47]),
            (r"pitch, \ beat and raga recognized by machine", [61, 62]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? Next, in maqam, another great modal system. In timelines and cycles across the "
            "world. In improvisation and composing. In what all musics share. And in machines that track pitch and beat."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"students", r"learn sargam and bols by voice before playing a note"),
            (r"tabla players", r"compute tihais at speed, \ in performance"),
            (r"electronic tanpuras", r"replace the instrument in many practice rooms"),
            (r"film composers", r"draw on ragas for melody and mood"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Students learn sargam and bols by voice before they play a note. Tabla players compute tihais "
            "at speed, in performance. Electronic tanpuras now sit in many practice rooms. And film composers draw on ragas "
            "for melody and mood."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"N. A. Jairazbhoy, \ \textit{The R\=ags of North Indian Music} \ (1971)",
             r"J. Bor \ (ed.), \ \textit{The Raga Guide} \ (1999)",
             r"M. Clayton, \ \textit{Time in Indian Music} \ (2000)",
             r"T. Viswanathan, \ M. H. Allen, \ \textit{Music in South India} \ (2004)",
             r"J. T. Titon \ (ed.), \ \textit{Worlds of Music} \ (6th ed., \ 2017)"],
            [r"N. A. Jairazbhoy, \ A. W. Stone, \ `Intonation in present-day North Indian classical music' \ (1963)",
             r"C. V. Raman, \ `On some Indian stringed instruments' \ (1921)",
             r"X. Serra, \ `A multicultural approach in music information research' \ (2011)",
             r"C. P. Vyasarayani, \ S. Birkett, \ J. McPhee, \ `Modeling the dynamics of a vibrating string with a finite distributed unilateral constraint' \ (2009)"],
            font_size=18)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        play_next_part(
            self, 34, "Cairo, 1932",
            "What is a scale whose notes lie between the piano's keys, placed by ear?",
            "Raga is one great modal system. <bookmark mark='a'/> In 1932 a congress met in Cairo to settle, among "
            "other things, the Arab scale, and its scale committee heard many tunings and did not settle on one equal "
            "grid. In the Arab world, Turkey and Iran, related modal traditions place notes between the piano's keys, "
            "by ear. What is a scale like that? <bookmark mark='b'/> Next time. Part 35: Maqam.",
            signoff=clip("bridge.signoff"))
