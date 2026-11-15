from __future__ import annotations

import numpy as np

from videos.music.music47.common import *  # noqa: F403
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
        d = load("tune47")
        c = clip("tune.variation47")
        head = VGroup(label(r"Variation 47", font_size=48, color=TUNE), label(r"the Tune, \ through thirty singers", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        allp = [x[0] for g in ("0", "30") for x in d["melodies"][g]] + [x[0] + d["shift"]["20"] for x in d["melodies"]["20"]]
        lo, hi = 60 + min(allp) - 1, 60 + max(allp) + 1
        rolls = VGroup()
        for g, name, col in (("0", r"as written", GREY_A), ("20", r"after twenty singers", BLUE), ("30", r"after thirty", TUNE)):
            mel = [[x[0] + d["shift"][g], x[1]] for x in d["melodies"][g]]
            r = mroll(mel_notes(mel, base=60), width=11.0 * sum(x[1] for x in mel) / sum(x[1] for x in d["melodies"]["0"]), height=1.0, lo=lo, hi=hi, color=col, bar_h=0.09)
            rolls.add(VGroup(label(name, font_size=18, color=col), r).arrange(DOWN, buff=0.12, aligned_edge=LEFT))
        rolls.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(DOWN * 0.3)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> Here, the Tune passed "
            "through thirty simulated singers. You will hear it as written, then as the fifteenth singer sang it, then the "
            "thirtieth."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rolls))
        st = d["starts"]
        beat = 0.36
        with self.listen(c) as snd:
            window(snd, r"Variation 47", kind="synthesized", detail=r"Part 8's voice", corner=DL, tag_corner=DR)
            for key, r in (("g0", rolls[0]), ("g30", rolls[2])):
                mel = d["melodies"]["0" if key == "g0" else "30"]
                on = np.concatenate([[0.0], np.cumsum([x[1] for x in mel])[:-1]])
                flash(snd, r[1].notes, [st[key] + beat * o for o in on], hot=WHITE, base=r[0].get_color())
            pulse(snd, rolls[1], st["g15"], st["g30"] - 0.3, buff=0.1)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger(self):
        v = load("variation")
        d = load("tune47")
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).move_to(DOWN * 0.2)
        head = label(r"the Variations ledger", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            f"Row forty-seven of the ledger. {say(d['notes_in'])} notes went in and {say(d['notes_out'])} came out; "
            f"{say(d['kept'])} of them are still exactly where they were, and the alignment cost is "
            f"{say(d['distance'][-1], 2)} a note. The Tune survives thirty careless singers; it is a tune that was made to be "
            "passed on."
        ):
            self.play(FadeIn(head), FadeIn(led, shift=UP * 0.2))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"music is older than the oldest flutes, \ and every society studied makes it",
            r"songs for the same purpose sound alike across cultures",
            r"there are no absolute universals, \ but many statistical ones",
            r"some tastes, \ like consonance, \ are learned; \ rhythm priors favour simple ratios",
            r"transmission alone turns noise into structure, \ and tunes into families",
            r"careful tests shrink the Mozart effect and transfer to about nothing",
        ], title=r"What we found", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? Music is older than the oldest flutes, and every society studied makes it. "
            "<bookmark mark='a'/> Songs made for the same purpose sound alike across cultures. <bookmark mark='b'/> There are "
            "no absolute universals, but many statistical ones. <bookmark mark='c'/> Some tastes, like the taste for "
            "consonance, are learned, and rhythm priors favour simple ratios everywhere. <bookmark mark='d'/> Transmission "
            "alone turns noise into structure, and tunes into families. <bookmark mark='e'/> And careful tests shrink the "
            "Mozart effect, and the transfer of music lessons, to about nothing."
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
            r"Compute the nPVI of the durations 1, \ 1, \ 2, \ 1, \ 1, \ 2. \ What does doubling every duration do to it?",
            r"Prove that a chain of learners who sample their posterior has the prior as a stationary distribution.",
            r"\textbf{Ear.} \ The lab plays rhythms before and after five tap-backs; \ say which is which.",
            r"\textbf{Build.} \ Switch off the singer's categories and run the chains: \ which universals still appear?",
            r"$\bigstar$ \ Which universals need which biases, \ and are the biases themselves universal?",
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
            (r"digital audio: \ the oldest instrument's sound, \ sampled", [48]),
            (r"finding music: \ similarity between melodies, \ at scale", [63]),
            (r"machines that compose: \ learning from a corpus, \ and its biases", [65]),
            (r"doing research in music: \ samples, \ preregistration, \ replication", [67]),
            (r"the Variations: \ the Tune's whole family", [68]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? In digital audio, where any sound, the oldest instrument's included, becomes numbers. "
            "In finding music, where similarity between melodies is computed at scale. In machines that compose, which learn "
            "from a corpus and inherit its biases. In doing research in music: samples, preregistration and replication. And "
            "in the Variations, the Tune's whole family."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"music teachers", r"start from what every child can do: \ pulse, \ small steps, \ songs"),
            (r"ethnomusicologists", r"sample widely, \ and code in the culture's own terms"),
            (r"music therapists", r"choose treatments with trial evidence, \ and say which"),
            (r"anyone citing a study", r"ask how big, \ how controlled, \ and whether it replicated"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Music teachers start from what every child can do: a pulse, small steps, songs. "
            "Ethnomusicologists sample widely, and code music in the culture's own terms. Music therapists choose treatments "
            "with trial evidence, and say which. And anyone citing a study asks how big it was, how it was controlled, and "
            "whether it replicated."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"A. D. Patel, \ \textit{Music, Language, and the Brain} \ (2008)",
             r"H. Honing \ (ed.), \ \textit{The Origins of Musicality} \ (2018)",
             r"B. Nettl, \ \textit{The Study of Ethnomusicology} \ (3rd ed., \ 2015)",
             r"S. Mithen, \ \textit{The Singing Neanderthals} \ (2005)"],
            [r"P. E. Savage and others, \ `Statistical universals reveal the structures and functions of human music' \ (2015)",
             r"S. A. Mehr and others, \ `Universality and diversity in human song' \ (2019)",
             r"N. Jacoby and J. H. McDermott, \ `Integer ratio priors on musical rhythm ...' \ (2017)",
             r"N. J. Conard, \ M. Malina and S. C. M\"unzel, \ `New flutes document the earliest musical tradition ...' \ (2009)"],
            font_size=18)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        q = label(r"what is a sound, \ once it becomes a list of numbers?", font_size=30, color=EAR).move_to(UP * 0.4)
        top = label(r"Act IX: \ electric sound", font_size=30, color=GREY_A).to_edge(UP, buff=0.8)
        lead = label(r"Every sound in this series has been computed.", font_size=24, color=WHITE).move_to(UP * 1.7)
        nxt = VGroup(label(r"Part 48", font_size=32, color=GREY_B), label(r"Digital Audio", font_size=50, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "That ends Act Eight, the mind. Every sound in this series has been computed. <bookmark mark='a'/> But what is a "
            "sound, once it becomes a list of numbers? <bookmark mark='b'/> Act Nine, electric sound, begins next time. "
            "Part 48: Digital Audio."
        ) as vo:
            self.play(FadeIn(top), FadeIn(lead))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
