from __future__ import annotations

from videos.music.music68.common import *  # noqa: F403
from videos.music.variations import rows_before


class Outro(SoundScene):
    def construct(self):
        self.variation()
        self.recap()
        self.problems()
        self.onward()
        self.aria()
        self.end()

    # ------------------------------------------------------------------
    def variation(self):
        v = load("variation")
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).move_to(DOWN * 0.2)
        head = label(r"Variation 68", font_size=30, color=TUNE).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Every part ends with its Variation. This part's is the suite: every Variation, in the order the series made them. "
            "Its row closes the ledger, with the measure this part took: how many of the Tune's forty-two keys come back "
            "wrong, as written, after the master, and at the end of the chain."
        ):
            self.play(FadeIn(head), FadeIn(led, shift=UP * 0.2))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        r = load("roundtrip")["rows"]
        o = load("order")
        card = objectives_card([
            r"the chain is the series: \ every link a part built and checked",
            r"down the chain the sound is remade at every link: \ timing, \ space, \ noise, \ peaks, \ bandwidth",
            rf"back up it, \ onsets at pitch-changing note positions are detected \ ({r['score']['moves_found']} of 24 as written, \ {min(r[k]['moves_found'] for k in STAGES)} at worst); \ repeated notes are the weak spot",
            r"notation keeps what survives the journey: \ pitch and time",
            rf"the Variations as made sit closer than {100 * (1 - o['built_below_random']):.1f}\% of random orders",
            r"what is still unknown includes Part 1's question",
        ], title=r"What we found", font_size=20).move_to(DOWN * 0.1)
        with self.voiceover(
            f"What did we find? The chain is the series: every link a model some part built and checked. <bookmark mark='a'/> Down the chain, the sound is remade at every link: its timing, its space, its noise, its peaks, its band. <bookmark mark='b'/> Back up it, onsets at pitch-changing note positions are detected, {say(r['score']['moves_found'])} of twenty-four as written and {say(min((r[k]['moves_found'] for k in STAGES)))} at worst, while repeated notes are the weak spot, and most of the loss arrives at the master's limiter, not at the coders. <bookmark mark='c'/> The simplified score encoding tracks intended pitch and duration separately from many timbral changes. <bookmark mark='d'/> The Variations, in the order they were made, sit closer together than almost any random order. <bookmark mark='e'/> And what is still unknown includes the question Part 1 began with."
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
            r"A line of 42 notes comes back with one note missed near the start. \ How many positions disagree, \ and what is the edit distance?",
            r"Show that the greedy nearest-neighbour order can be longer than the best order by a factor that grows with the number of pieces.",
            r"\textbf{Ear.} \ The lab sends a tune of your choice down the chain. \ At which bit rate can you no longer sing it back?",
            r"\textbf{Build.} \ Add a stage to the chain \ (a phone's loudspeaker, \ Part 54) \ and find what it costs the round trip.",
            r"$\bigstar$ \ Why do simple ratios sound good? \ Design the experiment that would separate the ear's part from the culture's.",
        ], font_size=21)
        with self.voiceover(
            "Five last problems. One to compute, one to prove, one for your ears, one to build, and the series' first question "
            "as a research problem, marked with a star. Solutions are in this part's notes. Pause here."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.25), run_time=3.0)
        self.wait(5.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def onward(self):
        prac = practice_card([
            (r"keep the instrument", r"Monochord is in the repository: \ every module runs without the films, \ with its tests"),
            (r"keep the labs", r"sixty-eight labs, \ one per part, \ each a page of numbers and a sound you can change"),
            (r"go wider", r"\textit{Statistics, Built} \ for Part 67's methods; \ \textit{AI, Built} \ for the networks of Act XI"),
            (r"go to the music", r"the pieces this series described and did not play: \ hear them, \ in good recordings, \ in good rooms"),
        ], title=r"From here", font_size=24)
        with self.voiceover(
            "Where from here? Keep the instrument: Monochord is in the repository, and every module runs without the films, "
            "with its tests. <bookmark mark='a'/> Keep the labs: one for every part, each a page of numbers and a sound you can "
            "change. <bookmark mark='b'/> Go wider: Statistics, Built for the methods of Part 67, and AI, Built for the networks "
            "of Act Eleven. <bookmark mark='c'/> And go to the music. This series described many pieces it could not play, "
            "because they are under copyright or need a hall. Hear them, in good recordings and in good rooms."
        ) as vo:
            self.play(FadeIn(prac.head), FadeIn(prac.rows[0]))
            for mark, rr in zip("abc", prac.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"J. S. Bach, \ \textit{Clavier-\"Ubung} IV \ (the \textit{Goldberg Variations}, \ 1741)",
             r"H. von Helmholtz, \ \textit{On the Sensations of Tone} \ (1863)",
             r"M. M\"uller, \ \textit{Fundamentals of Music Processing} \ (2nd ed., \ 2021)",
             r"J. O. Smith, \ \textit{Physical Audio Signal Processing} \ (2010)"],
            [r"A. T. Cemgil and B. Kappen, \ `Monte Carlo methods for tempo tracking and rhythm quantization' \ (2003)",
             r"A. de Cheveign\'e and H. Kawahara, \ `YIN, \ a fundamental frequency estimator' \ (2002)",
             r"J. H. McDermott et al., \ `Indifference to dissonance in native Amazonians' \ (\textit{Nature}, \ 2016)",
             r"V. I. Levenshtein, \ `Binary codes capable of correcting deletions, \ insertions and reversals' \ (1966)"],
            font_size=18)
        with self.voiceover("The books and papers this part leans on. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def aria(self):
        d = load("hook")
        c = clip("hook.one")
        head = label(r"\textit{aria da capo}", font_size=40, color=TUNE).move_to(UP * 2.4)
        sub = label(r"Variation 1, \ again", font_size=24, color=GREY_A).next_to(head, DOWN, buff=0.25)
        s = string_figure().move_to(DOWN * 0.2)
        with self.voiceover(
            "And so, as the Goldberg does, the aria again. Variation 1, the Tune on one simulated string, the same samples "
            "as in the original cached rendering of Variation 1."
        ):
            self.play(FadeIn(head), FadeIn(sub), FadeIn(s))
        with self.listen(c) as snd:
            window(snd, r"Variation 1", kind="physical model", detail=r"Part 1's string", corner=DL, tag_corner=DR)
            ev = sorted(v for k, v in c.events.items() if k.startswith("n"))
            stops = [{1: 1.0, 2: 8 / 9, 3: 4 / 5, 4: 3 / 4, 5: 2 / 3, 6: 3 / 5, 7: 8 / 15}[deg] for deg, _ in TUNE_NOTES]
            move_bridge(snd, s, ev, stops)
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def end(self):
        lines = VGroup(
            label(r"the same notes", font_size=30, color=WHITE),
            label(r"a different listener", font_size=34, color=EAR),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.6)
        fin = VGroup(label(r"Music, \ Built", font_size=44, color=TUNE), label(r"sixty-eight parts", font_size=22, color=GREY_B)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "The same notes. <bookmark mark='a'/> A different listener. <bookmark mark='b'/> That was Music, Built. Thank you for "
            "listening."
        ) as vo:
            self.play(FadeIn(lines[0]))
            vo.wait_until("a")
            self.play(FadeIn(lines[1]))
            vo.wait_until("b")
            self.play(FadeIn(fin, shift=UP * 0.2))
        self.wait(2.0)
        self.clear_scene()
