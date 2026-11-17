from __future__ import annotations

from videos.music.music59.common import *  # noqa: F403
from videos.music.variations import rows_before


class Outro(SoundScene):
    def construct(self):
        self.variation()
        self.ledger()
        self.recap()
        self.problems()
        self.payoffs()
        self.next_part()

    # ------------------------------------------------------------------
    def variation(self):
        d = load("tune59")
        c = clip("tune.variation59")
        st = d["starts"]
        keys = d["names"]
        lv = d["levels_db"]
        names = {"foh": (r"the mixing desk", TUNE), "back": (r"the back row, \ 100 m", BLUE), "carpark": (r"the car park, \ outside", EAR)}
        head = VGroup(label(r"Variation 59", font_size=48, color=TUNE), label(r"one show, \ three places", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        cells = VGroup(*[VGroup(RoundedRectangle(width=3.4, height=1.3, corner_radius=0.12, stroke_color=names[k][1]),
                                VGroup(label(names[k][0], font_size=17, color=names[k][1]), label(rf"{lv[k]:+.0f} dB", font_size=16, color=GREY_A)).arrange(DOWN, buff=0.12)).arrange(ORIGIN) for k in keys]).arrange(RIGHT, buff=0.35).move_to(DOWN * 0.2)
        note = label(r"our session playing the Tune through a simulated arena system: \ levels as heard; \ headphones or real bass help", font_size=17, color=GREY_A).next_to(cells, DOWN, buff=0.45)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> Here our session plays it "
            "through a simulated arena system, and you hear it from three places: the mixing desk; the back row, a hundred "
            "metres from the stage; and the car park outside, through a concrete wall. Levels are as heard."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cells), FadeIn(note))
        with self.listen(c) as snd:
            window(snd, r"Variation 59", kind="physical model", detail=r"our session, \ a simulated arena", corner=DL, tag_corner=DR)
            for i, k in enumerate(keys):
                end = st[keys[i + 1]] - 0.3 if i + 1 < len(keys) else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger(self):
        v = load("variation")
        d = load("tune59")
        lv = d["levels_db"]
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).move_to(DOWN * 0.2)
        head = label(r"the Variations ledger", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            f"Row fifty-nine of the ledger. The back row hears the show only {say(-lv['back'])} decibels down from the desk, "
            f"as Chapter 4's line array promised, with the treble a little dulled by the air; the car park hears it {say(-lv['carpark'])} decibels down, and mostly "
            "bass, the part this simplified wall model attenuates least and the neighbours complain about."
        ):
            self.play(FadeIn(head), FadeIn(led, shift=UP * 0.2))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"a microphone howls where the loop's gain first reaches one in phase: \ Nyquist predicts the note",
            r"notches and placement buy a few decibels; \ the PAG--NAG budget says how many are needed",
            r"a line source falls 3 dB per doubling near it, \ 6 far away; \ a J-shaped array evens the field",
            r"subwoofer pairs cancel behind by delay and polarity; \ delay towers rely on precedence",
            r"systems are measured with the music itself: \ transfer function, \ coherence, \ delay",
            r"radio plans avoid intermodulation; \ the STI predicts speech; \ dose is level and time",
        ], title=r"What we found", font_size=20).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? A microphone howls where the loop's gain first reaches one in phase, and Nyquist's criterion "
            "predicts the note. <bookmark mark='a'/> Notches and placement buy a few decibels, and the budget of potential and "
            "needed acoustic gain says how many are needed. <bookmark mark='b'/> A line source loses three decibels per doubling "
            "of distance near it and six far away, and a J-shaped array evens the field. <bookmark mark='c'/> Subwoofer pairs "
            "cancel behind by delay and polarity, and delay towers rely on the precedence effect. <bookmark mark='d'/> Systems "
            "are measured with the music itself: transfer function, coherence and delay. <bookmark mark='e'/> Radio plans dodge "
            "intermodulation, the speech transmission index predicts what words survive, and a hearing dose is level and time "
            "together."
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
            r"A tower stands 40 m from you; \ the stage is 120 m away. \ At 20$^\circ$C, \ what delay should the tower have? \ And at 5$^\circ$C?",
            r"Show that a cardioid pair, \ rear box delayed by $d/c$ and inverted, \ cancels exactly behind at every frequency, \ and find where it is strongest in front.",
            r"\textbf{Ear.} \ The lab plays an announcement at five speech transmission indices, \ shuffled; \ put them in order.",
            r"\textbf{Build.} \ Extend the frequency planner to fifth-order products, \ and count how many carriers still fit.",
            r"$\bigstar$ \ What settings hold a festival's off-site limit with 95\% confidence over the weather, \ and at what cost to the audience?",
        ], font_size=21)
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
            (r"the business of music: \ why tickets cost what they do", [60]),
            (r"score following: \ machines that play along on stage", [62]),
            (r"source separation: \ pulling one voice out of a room", [64]),
            (r"research: \ measuring what audiences hear", [67]),
            (r"the concert that closes the series", [68]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? In the business of music, and why concert tickets cost what they do. In score following, "
            "with machines that play along on stage. In source separation, pulling one voice out of a room. In research, "
            "measuring what audiences hear. And in the concert that closes the series."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"feedback", r"microphone close, \ loudspeaker far, \ nulls aimed, \ then notches"),
            (r"coverage", r"predict the field before hanging; \ measure it after, \ with the music"),
            (r"towers", r"delay to the stage plus about 10 ms; \ re-check as the night cools"),
            (r"ears", r"earplugs for the audience and the crew; \ a meter and a log at the desk"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Against feedback: microphone close, loudspeaker far, nulls aimed, and only then notches. For "
            "coverage: predict the field before the rig is hung, and measure it afterwards with the music. Delay towers to the "
            "stage plus about ten milliseconds, re-checked as the night cools. And for ears: earplugs for audience and crew, "
            "and a meter and a log at the desk."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"B. McCarthy, \ \textit{Sound Systems: \ Design and Optimization} \ (3rd ed., \ 2016)",
             r"D. Davis, \ E. Patronis and P. Brown, \ \textit{Sound System Engineering} \ (4th ed., \ 2013)",
             r"G. Ballou \ (ed.), \ \textit{Handbook for Sound Engineers} \ (5th ed., \ 2015)",
             r"IEC 60268-16, \ \textit{Objective rating of speech intelligibility by speech transmission index} \ (2020)"],
            [r"H. Nyquist, \ `Regeneration theory' \ (Bell System Technical Journal, \ 1932)",
             r"T. Houtgast and H. J. M. Steeneken, \ `The modulation transfer function in room acoustics' \ (1973 onwards)",
             r"M. Urban, \ C. Heil and P. Bauman, \ `Wavefront sculpture technology' \ (J. AES, \ 2003)",
             r"S. G. Kujawa and M. C. Liberman, \ `Adding insult to injury' \ (J. Neuroscience, \ 2009)"],
            font_size=18)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        top = label(r"Act X: \ the studio and the stage", font_size=30, color=GREY_A).to_edge(UP, buff=0.8)
        lead = label(r"1908: \ the US Supreme Court rules that a piano roll is not a copy of the song it plays.", font_size=23, color=WHITE).move_to(UP * 1.7)
        q = label(r"so who is paid when a song is played, \ and how much of a stream's fraction of a cent reaches them?", font_size=27, color=EAR).move_to(UP * 0.4)
        nxt = VGroup(label(r"Part 60", font_size=32, color=GREY_B), label(r"The Business of Music", font_size=46, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "1908: the Supreme Court of the United States rules that a piano roll is not a copy of the song it plays, and the "
            "next year Congress writes a new right to cover it. <bookmark mark='a'/> So who is paid when a song is played, and "
            "how much of a stream's fraction of a cent reaches them? <bookmark mark='b'/> Next time. Part 60: The Business of "
            "Music."
        ) as vo:
            self.play(FadeIn(top), FadeIn(lead))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        play_signoff(self, 59, clip("bridge.signoff"), clear=(top,))
        self.clear_scene()
