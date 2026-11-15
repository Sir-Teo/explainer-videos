from __future__ import annotations

from videos.music.music54.common import *  # noqa: F403
from videos.music.variations import rows_before

CELLS = [("mic_omni", r"omni", GREY_A), ("mic_cardioid", r"cardioid", TUNE), ("mic_fig8", r"figure-8", EAR),
         ("spk_phone", r"phone", EAR), ("spk_bookshelf", r"bookshelf", BLUE), ("spk_floor", r"floor-stander", TUNE)]


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
        d = load("tune54")
        c = clip("tune.variation54")
        st = d["starts"]
        head = VGroup(label(r"Variation 54", font_size=48, color=TUNE), label(r"the Tune, \ in and out of the air", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        mics = VGroup(*[VGroup(RoundedRectangle(width=2.6, height=1.0, corner_radius=0.15, stroke_color=col), label(t, font_size=20, color=col)).arrange(ORIGIN) for k, t, col in CELLS[:3]]).arrange(RIGHT, buff=0.5)
        spks = VGroup(*[VGroup(RoundedRectangle(width=2.6, height=1.0, corner_radius=0.15, stroke_color=col), label(t, font_size=20, color=col)).arrange(ORIGIN) for k, t, col in CELLS[3:]]).arrange(RIGHT, buff=0.5)
        ml = label(r"three microphones \ (a piano behind the singer)", font_size=18, color=GREY_A)
        sl = label(r"the cardioid's version, \ three loudspeakers", font_size=18, color=GREY_A)
        g = VGroup(VGroup(ml, mics).arrange(DOWN, buff=0.25), VGroup(sl, spks).arrange(DOWN, buff=0.25)).arrange(DOWN, buff=0.6).move_to(DOWN * 0.3)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> Here it is sung with a piano "
            "behind the singer, picked up by an omni, a cardioid and a figure-8; then the cardioid's version played through a "
            "phone, a bookshelf speaker and a floor-stander."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g))
        boxes = list(mics) + list(spks)
        keys = [k for k, _, _ in CELLS]
        with self.listen(c) as snd:
            window(snd, r"Variation 54", kind="physical model", detail=r"three microphones, \ three loudspeakers", corner=DL, tag_corner=DR)
            for i, k in enumerate(keys):
                end = st[keys[i + 1]] - 0.3 if i + 1 < len(keys) else c.duration
                pulse(snd, boxes[i], st[k], end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger(self):
        v = load("variation")
        d = load("tune54")
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).move_to(DOWN * 0.2)
        head = label(r"the Variations ledger", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            f"Row fifty-four of the ledger. The cardioid takes the piano behind it {say(-d['cardioid_170'])} decibels down; the "
            f"phone's speaker reaches down to {say(d['phone_f3'])} hertz, the floor-stander to {say(d['floor_f3'])}."
        ):
            self.play(FadeIn(head), FadeIn(led, shift=UP * 0.2))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"a dynamic transducer works both ways: \ $e = Bl\,v$, \ $F = Bl\,i$",
            r"pressure is omnidirectional; \ its gradient is a figure-8; \ mixes make the family",
            r"a gradient microphone's bass rises close to the source: \ $1 + 1/(jkr)$",
            r"thermal noise sets a floor; \ balanced lines reject hum",
            r"a loudspeaker is a high-pass filter; \ boxes and ports shape it, \ as Small and Thiele calculated",
            r"horns match, \ crossovers sum, \ cancellers subtract",
        ], title=r"What we found", font_size=21).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? A dynamic transducer works both ways, through one number, B l. <bookmark mark='a'/> Pressure is "
            "omnidirectional, its gradient a figure-8, and mixtures make the family. <bookmark mark='b'/> A gradient "
            "microphone's bass rises close to the source. <bookmark mark='c'/> Thermal noise sets a floor, and balanced lines "
            "reject hum. <bookmark mark='d'/> A loudspeaker is a high-pass filter, which boxes and ports shape as Small and "
            "Thiele calculated. <bookmark mark='e'/> And horns match, crossovers sum, and cancellers subtract."
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
            r"A woofer with $f_s = 30$ Hz, \ $Q_{ts} = 0.35$ and $V_{as} = 80$ L goes in a 40 L sealed box. \ Find $f_c$ and $Q_{tc}$.",
            r"Prove that $A + (1 - A)\cos\theta$ has its greatest directivity at $A = 1/4$.",
            r"\textbf{Ear.} \ The lab plays a voice at random distances from a figure-8; \ order them, \ near to far.",
            r"\textbf{Build.} \ Add a second-order passive crossover to the simulator and find the sum's response with real drivers.",
            r"$\bigstar$ \ How much louder and deeper can a small speaker be made to sound, \ safely, \ by control alone?",
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
            (r"rooms and space: \ the loudspeaker in a room; \ stereo and binaural", [55]),
            (r"recording and mixing: \ microphone choice and placement, \ gain staging", [56]),
            (r"live sound: \ feedback, \ line arrays and horns", [59]),
            (r"source separation: \ arrays and beamforming", [64]),
            (r"generative audio: \ learned models of gear", [66]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? In rooms and space, the loudspeaker in a room, and stereo and binaural sound. In "
            "recording and mixing, where microphones are chosen and placed. In live sound, with feedback, line arrays and horns. "
            "In source separation, with arrays. And in generative audio, with learned models of gear."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"singers", r"work the proximity effect: \ in for warmth, \ out for power"),
            (r"engineers", r"aim a cardioid's null at what should not be heard"),
            (r"speaker builders", r"choose a box by Thiele--Small, \ check the port by impedance"),
            (r"everyone", r"use balanced cables, \ and trust noise cancelling only below a kilohertz"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Singers work the proximity effect, in for warmth and out for power. Engineers aim a cardioid's "
            "null at what should not be heard. Speaker builders choose a box by its Thiele-Small parameters and check the port "
            "by its impedance. And everyone uses balanced cables, and trusts noise cancelling only below a kilohertz."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"J. Eargle, \ \textit{The Microphone Book} \ (2nd ed., \ 2004)",
             r"L. L. Beranek and T. J. Mellow, \ \textit{Acoustics: \ Sound Fields and Transducers} \ (2012)",
             r"H. F. Olson, \ \textit{Acoustical Engineering} \ (1957)",
             r"S. M. Kuo and D. R. Morgan, \ \textit{Active Noise Control Systems} \ (1996)"],
            [r"A. N. Thiele, \ `Loudspeakers in vented boxes' \ (1961; \ JAES 1971)",
             r"R. H. Small, \ `Closed-box loudspeaker systems' \ (JAES, \ 1972)",
             r"S. H. Linkwitz, \ `Active crossover networks for noncoincident drivers' \ (JAES, \ 1976)",
             r"C. W. Rice and E. W. Kellogg, \ `Notes on the development of a new type of hornless loud speaker' \ (1925)"],
            font_size=18)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        top = label(r"Act X: \ the studio and the stage", font_size=30, color=GREY_A).to_edge(UP, buff=0.8)
        lead = label(r"In 1895 Harvard opened a lecture hall in which nobody could understand a word.", font_size=24, color=WHITE).move_to(UP * 1.7)
        q = label(r"what did a young physicist measure with an organ pipe and a stopwatch?", font_size=28, color=EAR).move_to(UP * 0.4)
        nxt = VGroup(label(r"Part 55", font_size=32, color=GREY_B), label(r"Rooms and Space", font_size=46, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "In 1895 Harvard opened a lecture hall in which nobody could understand a word. <bookmark mark='a'/> What did a young "
            "physicist measure there, with an organ pipe and a stopwatch? <bookmark mark='b'/> Next time. Part 55: Rooms and "
            "Space."
        ) as vo:
            self.play(FadeIn(top), FadeIn(lead))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
