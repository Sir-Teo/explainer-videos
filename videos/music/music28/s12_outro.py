from __future__ import annotations

import numpy as np

from videos.music.music28.common import *  # noqa: F403
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
        c = clip("tune.variation28")
        head = VGroup(label(r"Variation 28", font_size=48, color=TUNE), label(r"the Tune, \ symmetric", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        g1 = voices_roll([d["whole"]] + d["planed"], width=5.4, height=2.6, colors=[TUNE, GREY_A, GREY_A], lo=58, hi=92, bar_h=0.09)
        acc = set(d["accents"])
        ost_acc = [n for i, n in enumerate(d["ostinato"]) if i in acc]
        ost_pl = [n for i, n in enumerate(d["ostinato"]) if i not in acc]
        g2 = voices_roll([d["octa"], ost_pl, ost_acc], width=5.4, height=2.6, colors=[TUNE, GREY_B, EAR], lo=34, hi=90, bar_h=0.08)
        cells = VGroup(VGroup(label(r"whole-tone, \ planed in augmented triads", font_size=20, color=GREY_A), g1).arrange(DOWN, buff=0.25),
                       VGroup(label(r"octatonic, \ over an ostinato with random accents", font_size=20, color=GREY_A), g2).arrange(DOWN, buff=0.25)).arrange(RIGHT, buff=0.7).move_to(DOWN * 0.3)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> This time, symmetry. "
            "First the Tune moved onto the whole-tone scale, with an augmented triad, itself a whole-tone chord, planed "
            "under every note: nothing in it is not whole-tone. Then the Tune on the octatonic scale, bowed, over a piano "
            "ostinato whose accents chance has placed, in pink."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"Variation 28", detail=r"Part 7's piano and bowed string", corner=DL, tag_corner=DR)
            flash_voices(snd, g1, [d["whole"]] + d["planed"], d["starts"]["whole"], d["unit"], colors=[TUNE, GREY_A, GREY_A])
            flash_voices(snd, g2, [d["octa"], ost_pl, ost_acc], d["starts"]["octa"], d["unit"], colors=[TUNE, GREY_B, EAR])
            pulse(snd, cells[0][0], d["starts"]["whole"], d["starts"]["octa"] - 0.5, buff=0.06)
            pulse(snd, cells[1][0], d["starts"]["octa"], c.duration, buff=0.06)
        self.play(FadeOut(cells))
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            f"Row twenty-eight of the ledger: {say(v['seconds'])} seconds. The measurement: "
            f"{say(d['notes']['planed_chords'])} augmented triads planed, and {say(d['notes']['accents'])} accents placed by "
            f"chance on {say(d['notes']['ostinato'])} ostinato notes."
        ):
            self.play(FadeIn(led, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        cen = load("census")
        oc = load("octatonic")["chance"]
        b = load("bartok")["golden"]
        card = objectives_card([
            r"the whole-tone scale: \ one step size, \ two transpositions, \ no home",
            rf"{cen['classes']} scale shapes; \ {cen['n_symmetric']} symmetric; \ Messiaen's seven are the large ones",
            r"planing, \ the octatonic, \ two keys at once: \ heard, \ and fitted by a key-finder",
            r"displaced accents and additive metres: \ the pulse kept, \ the hierarchy lost",
            rf"golden-section claims: \ ten loose landmarks hit by chance {100 * b['p10_2']:.0f} times in 100",
            rf"a 4-note passage fits an octatonic scale by chance {100 * oc['octatonic'][1]:.0f} times in 100",
        ], title=r"What we found", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? The whole-tone scale has one step size, two transpositions, and no home. "
            f"<bookmark mark='a'/> Of {say(cen['classes'])} possible scale shapes, {say(cen['n_symmetric'])} are symmetric, "
            "and Messiaen's seven modes are the large ones. <bookmark mark='b'/> Planing, the octatonic and two keys at once "
            "were heard, and a key-finder showed two clear keys making one unclear one. <bookmark mark='c'/> Displaced "
            "accents keep the pulse and lose the hierarchy of beats. <bookmark mark='d'/> A golden-section claim with loose "
            "landmarks succeeds by chance more often than not. <bookmark mark='e'/> And a short passage fits a scale by "
            "chance so often that only long passages are evidence."
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
            r"How many different transpositions does the set \{0, 1, 4, 5, 8, 9\} have? \ Name the pattern it repeats.",
            r"Prove that the number of ways to group $n$ pulses into 2s and 3s satisfies $a_n = a_{n-2} + a_{n-3}$.",
            r"\textbf{Ear.} \ The lab plays eight short ostinatos, \ some with regular accents, \ some with random ones. \ Sort them.",
            r"\textbf{Build.} \ Write a program that finds, \ for any passage, \ the scale collection holding the most of its sounding time, \ with a chance baseline.",
            r"$\bigstar$ \ How much of a repertoire is octatonic beyond chance, \ and where?",
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
            (r"giving up the key: \ twelve tones", [29]),
            (r"symmetry as mathematics: \ transformations and the geometry of chords", [31, 32]),
            (r"rhythm and scale as mathematics: \ even rhythms, \ necklaces", [33]),
            (r"the gamelan, \ and other musics, \ on their own terms", [36]),
            (r"the ostinato in the studio: \ loops and sequencers", [53]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? Next, in music that gives up the key altogether. In the mathematics of symmetry, "
            "transformations and the geometry of chords. In the mathematics of rhythm and scale. In the gamelan and other "
            "musics, heard on their own terms. And in the studio, where the ostinato becomes a loop."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"composers", r"choose a collection and know its symmetries"),
            (r"jazz players", r"play the diminished scale over a dominant chord"),
            (r"drummers", r"group fast pulses in 2s and 3s"),
            (r"analysts", r"test a claim against what chance would give"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Composers choose a collection and know its symmetries. Jazz players reach for the diminished "
            "scale over a dominant chord. Drummers group fast pulses in twos and threes. And analysts test a claim against "
            "what chance would give."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"R. Taruskin, \ \textit{The Oxford History of Western Music}, \ vol. 4 \ (2005)",
             r"E. Antokoletz, \ \textit{The Music of Béla Bartók} \ (1984)",
             r"O. Messiaen, \ \textit{Technique de mon langage musical} \ (1944)",
             r"P. van den Toorn, \ \textit{The Music of Igor Stravinsky} \ (1983)"],
            [r"D. Tymoczko, \ `Stravinsky and the octatonic: \ a reconsideration', \ \textit{Music Theory Spectrum} \ (2002)",
             r"R. Howat, \ `Bartók, \ Lendvai and the principles of proportional analysis', \ \textit{Music Analysis} \ (1983)",
             r"A. Berger, \ `Problems of pitch organization in Stravinsky', \ \textit{Perspectives of New Music} \ (1963)",
             r"E. Lendvai, \ \textit{Béla Bartók: \ An Analysis of his Music} \ (1971)"],
            font_size=19)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        q = label(r"what if all twelve notes were equal?", font_size=30, color=EAR).move_to(UP * 0.4)
        top = label(r"Act V: \ after tonality", font_size=30, color=GREY_A).to_edge(UP, buff=0.8)
        nxt = VGroup(label(r"Part 29", font_size=32, color=GREY_B), label(r"Twelve Tones", font_size=50, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Paris loosened the key with symmetric scales and new rhythms. <bookmark mark='a'/> Vienna asked a more radical "
            "question: what if all twelve notes were equal, and none of them home? <bookmark mark='b'/> Next time. Part 29: "
            "Twelve Tones."
        ) as vo:
            self.play(FadeIn(top))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
