from __future__ import annotations

import numpy as np

from videos.music.music46.common import *  # noqa: F403
from videos.music.variations import rows_before

EC = {"expected": TUNE, "delayed": BLUE, "denied": EAR}


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
        d = load("tune46")
        e = load("endings")
        c = clip("tune.variation46")
        head = VGroup(label(r"Variation 46", font_size=48, color=TUNE), label(r"the Tune, \ three endings", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        cells = VGroup()
        for k in d["order"]:
            ic = e[k]["ic"]
            g = bits_plot(ic, width=0.42 * len(ic), height=1.4, top=11.0, color=EC[k])
            cells.add(VGroup(label(k, font_size=22, color=EC[k]), g, label(rf"last note: \ {ic[-1]:.1f} bits", font_size=16, color=WHITE)).arrange(DOWN, buff=0.2))
        cells.arrange(RIGHT, buff=1.0, aligned_edge=DOWN).move_to(DOWN * 0.1)
        cap = label(r"each bar: \ the listener's surprise at a note of the last phrase", font_size=16, color=GREY_A).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> Here, its last two "
            "phrases three times: ending as expected; with the ending delayed by the deceptive turn; and with the ending "
            "denied. Beside each, the listener's surprise, note by note."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cells), FadeIn(cap))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"Variation 46", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for i, k in enumerate(d["order"]):
                end = st[d["order"][i + 1]] - 0.4 if i < 2 else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.12)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger(self):
        v = load("variation")
        d = load("tune46")
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).move_to(DOWN * 0.2)
        head = label(r"the Variations ledger", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        t, f = d["turn_ic"], d["final_ic"]
        with self.voiceover(
            f"Row forty-six of the ledger: the measurement is the listener's surprise. The turn to the ending costs "
            f"{say(t['expected'], 1)}, {say(t['delayed'], 1)} and {say(t['denied'], 1)} bits in the three versions; the last "
            f"note {say(f['expected'], 1)}, {say(f['delayed'], 1)} and {say(f['denied'], 1)}."
        ):
            self.play(FadeIn(head), FadeIn(led, shift=UP * 0.2))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"musical feeling is tied to expectation: \ wanting, \ then getting",
            r"expectations are learned by counting, \ without trying",
            r"a listener model measures surprise and uncertainty in bits",
            r"delay makes a resolution more certain; \ denial leaves the cost unpaid",
            r"pleasure lies in the interaction of surprise and uncertainty",
            r"groove and liking follow inverted Us; \ emotion has a code of cues",
        ], title=r"What we found", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? Musical feeling is tied to expectation: wanting, then getting. <bookmark mark='a'/> "
            "Expectations are learned by counting, without trying. <bookmark mark='b'/> A listener model measures surprise "
            "and uncertainty in bits. <bookmark mark='c'/> Delay makes a resolution more certain; denial leaves the cost "
            "unpaid. <bookmark mark='d'/> Pleasure lies in the interaction of surprise and uncertainty. "
            "<bookmark mark='e'/> And selected groove and liking studies report inverted-U patterns, with effects depending on stimulus and listener, while expressed emotion has a code of cues."
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
            r"A model gives the next note probability 1/8. \ What is its surprise? \ And for 1/1000?",
            r"Prove that uncertainty is largest when every next note is equally likely, \ and equals $\log_2 n$.",
            r"\textbf{Ear.} \ The lab plays word and part-word triplets after a stream; \ say which was the word.",
            r"\textbf{Build.} \ Train the listener on a different corpus and compare the Tune's surprise.",
            r"$\bigstar$ \ How much of musical pleasure do surprise and uncertainty alone predict?",
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
            (r"origins and universals: \ what all listeners share", [47]),
            (r"mastering and loudness: \ arousal by level", [57]),
            (r"finding music: \ recommendation and preference", [63]),
            (r"machines that compose: \ a listener that writes", [65]),
            (r"doing research in music: \ replication", [67]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? In origins and universals, what all listeners share. In mastering, where loudness "
            "sets arousal. In finding music, recommendation and preference. In machines that compose, a listener that writes. "
            "And in doing research in music, where replication matters."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"composers", r"build expectations before breaking them"),
            (r"songwriters", r"delay the chorus, \ then pay it off"),
            (r"producers", r"build tension with uncertainty, \ release it with a drop"),
            (r"music therapists", r"choose music by its cues, \ and measure what it does"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Composers build expectations before breaking them. Songwriters delay the chorus, then pay it "
            "off. Producers build tension with uncertainty and release it with a drop. And music therapists choose music by "
            "its cues, and measure what it does."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"L. B. Meyer, \ \textit{Emotion and Meaning in Music} \ (1956)",
             r"D. Huron, \ \textit{Sweet Anticipation} \ (2006)",
             r"P. N. Juslin and J. A. Sloboda \ (eds.), \ \textit{Handbook of Music and Emotion} \ (2010)",
             r"M. T. Pearce, \ `The construction and evaluation of statistical models of melodic structure' \ (2005)",
             r"P. Kivy, \ \textit{The Corded Shell} \ (1980)"],
            [r"V. N. Salimpoor and others, \ `Anatomically distinct dopamine release ...' \ (2011)",
             r"V. K. M. Cheung and others, \ `Uncertainty and surprise jointly predict musical pleasure' \ (2019)",
             r"M. A. G. Witek and others, \ `Syncopation, body-movement and pleasure in groove music' \ (2014)",
             r"J. R. Saffran and others, \ `Statistical learning of tone sequences' \ (1999)"],
            font_size=18)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        play_next_part(
            self, 46, "Hohle Fels, 35{,}000 years ago",
            "Is any of this universal, and where did music come from?",
            "Our listener learned from fifty Western tunes. <bookmark mark='a'/> In a cave in south-west Germany lay "
            "a flute cut from a vulture's wing bone, at least thirty-five thousand years old. Every known society "
            "makes music, and no one agrees why. Is any of what we have measured universal, and where did music come "
            "from? <bookmark mark='b'/> Next time. Part 47: Origins and Universals.")
