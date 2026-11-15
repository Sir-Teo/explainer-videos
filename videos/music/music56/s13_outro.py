from __future__ import annotations

from videos.music.music56.common import *  # noqa: F403
from videos.music.variations import rows_before

CELLS = [("dry", r"close and dry", TUNE), ("wall", r"a wall of sound", EAR), ("dub", r"a dub", BLUE)]


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
        d = load("tune56")
        c = clip("tune.variation56")
        st = d["starts"]
        me = d["measures"]
        head = VGroup(label(r"Variation 56", font_size=48, color=TUNE), label(r"the session, \ mixed three ways", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        cells = VGroup(*[VGroup(RoundedRectangle(width=3.4, height=1.5, corner_radius=0.15, stroke_color=col),
                                VGroup(label(t, font_size=22, color=col), label(rf"crest {me[k]['crest_db']:.0f} dB, \ correlation {me[k]['correlation']:.2f}", font_size=14, color=GREY_A)).arrange(DOWN, buff=0.15)).arrange(ORIGIN)
                         for k, t, col in CELLS]).arrange(RIGHT, buff=0.5).move_to(DOWN * 0.2)
        note = label(r"the Tune's first three phrases, \ nine tracks, \ our band; \ headphones", font_size=18, color=GREY_A).next_to(cells, DOWN, buff=0.45)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> Here our band plays its "
            "first three phrases, and the session is mixed three ways: close and dry, a wall of sound, and a dub."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cells), FadeIn(note))
        keys = [k for k, _, _ in CELLS]
        with self.listen(c) as snd:
            window(snd, r"Variation 56", kind="physical model", detail=r"one session, \ three mixes, \ headphones", corner=DL, tag_corner=DR)
            for i, k in enumerate(keys):
                end = st[keys[i + 1]] - 0.3 if i + 1 < len(keys) else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger(self):
        v = load("variation")
        d = load("tune56")
        me = d["measures"]
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).move_to(DOWN * 0.2)
        head = label(r"the Variations ledger", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            f"Row fifty-six of the ledger. One session, three mixes: a crest factor of {say(me['dry']['crest_db'])} decibels "
            f"dry and {say(me['wall']['crest_db'])} in the wall; the dub's echo every {say(d['echo_s'], 2)} seconds."
        ):
            self.play(FadeIn(head), FadeIn(led, shift=UP * 0.2))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"a stereo pair turns direction into level and time differences; \ its recording angle sets the stage's width",
            r"two microphones on one source comb; \ distance \ (3 : 1), \ polarity and alignment tame it",
            r"gain staging keeps peaks under the ceiling and quiet passages above the floor",
            r"crossfades hide joins; \ pan laws trade stereo against mono",
            r"masking is mapped band by band and carved; \ every cut gives a band away",
            r"compression, \ depth cues and width shape the stage; \ rules alone do not make a mix",
        ], title=r"What we found", font_size=20).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? A stereo pair turns direction into level and time differences, and its recording angle sets "
            "the width of the stage. <bookmark mark='a'/> Two microphones on one source comb, and distance, polarity and "
            "alignment tame it. <bookmark mark='b'/> Gain staging keeps the peaks under the ceiling and the quiet passages "
            "above the floor. <bookmark mark='c'/> Crossfades hide joins, and pan laws trade stereo against mono. "
            "<bookmark mark='d'/> Masking can be mapped band by band and carved, and every cut gives a band away. "
            "<bookmark mark='e'/> And compression, depth cues and width shape the stage, while rules alone do not make a mix."
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
            r"Two microphones hear a source from 0.5 m and 2 m. \ Find the delay, \ the first notch of their sum, \ and the comb's peak and dip.",
            r"Prove that the $-3$ dB pan law keeps stereo power constant, \ and that its centre is 3 dB louder in mono than a hard pan.",
            r"\textbf{Ear.} \ The lab mixes a voice at random depths in front of a band; \ order them, \ near to far.",
            r"\textbf{Build.} \ Give the automatic mixer a rule that reads the masking map, \ and see whether the bass comes back.",
            r"$\bigstar$ \ Is there an objective, \ other than imitating a mix, \ that predicts which mix listeners prefer?",
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
            (r"mastering and loudness: \ the stereo bus, \ meters, \ the loudness war", [57]),
            (r"live sound: \ the console on stage, \ feedback, \ delays", [59]),
            (r"source separation: \ unmixing, \ with masks like the masking map's", [64]),
            (r"generative audio: \ learned effects and mixes", [66]),
            (r"research: \ listening tests and their statistics", [67]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? In mastering, which takes the stereo bus from here, with meters and the loudness war. "
            "In live sound, with the console on stage. In source separation, which unmixes with masks like our masking map's. "
            "In generative audio, with learned effects and mixes. And in research, with listening tests and their statistics."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"recording", r"close microphones by 3 : 1, \ polarity checked, \ peaks near $-18$ dBFS"),
            (r"editing", r"cut before a hit, \ crossfade everything, \ keep the feel"),
            (r"mixing", r"balance first, \ cut before boosting, \ pan to unmask, \ check in mono"),
            (r"monitoring", r"a treated room, \ references, \ small speakers, \ and rested ears"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. When recording: close microphones by three to one, polarity checked, peaks near minus eighteen. "
            "When editing: cut before a hit, crossfade everything, and keep the feel. When mixing: balance first, cut before "
            "boosting, pan to unmask, and check in mono. And when listening: a treated room, references, small speakers and "
            "rested ears."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"R. Izhaki, \ \textit{Mixing Audio} \ (3rd ed., \ 2018)",
             r"M. Senior, \ \textit{Mixing Secrets for the Small Studio} \ (2nd ed., \ 2018)",
             r"G. Milner, \ \textit{Perfecting Sound Forever} \ (2009)",
             r"M. Williams, \ \textit{Microphone Arrays for Stereo and Multichannel Sound Recording} \ (2004)"],
            [r"B. De Man, \ J. D. Reiss and R. Stables, \ `Ten years of automatic mixing' \ (2017)",
             r"E. Perez-Gonzalez and J. D. Reiss, \ `Automatic gain and fader control for live mixing' \ (2009)",
             r"C. J. Steinmetz et al., \ `Automatic multitrack mixing with a differentiable mixing console' \ (2021)",
             r"B. Eno, \ `The recording studio as a compositional tool' \ (1979)"],
            font_size=18)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        top = label(r"Act X: \ the studio and the stage", font_size=30, color=GREY_A).to_edge(UP, buff=0.8)
        lead = label(r"In 2008 fans found that a rock album sounded better inside a video game than on its own CD.", font_size=24, color=WHITE).move_to(UP * 1.7)
        q = label(r"how can making a record louder make it worse?", font_size=28, color=EAR).move_to(UP * 0.4)
        nxt = VGroup(label(r"Part 57", font_size=32, color=GREY_B), label(r"Mastering and Loudness", font_size=46, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "In 2008 fans found that a rock album sounded better inside a video game than on its own CD. <bookmark mark='a'/> How "
            "can making a record louder make it worse? <bookmark mark='b'/> Next time. Part 57: Mastering and Loudness."
        ) as vo:
            self.play(FadeIn(top), FadeIn(lead))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
