from __future__ import annotations

from videos.music.music55.common import *  # noqa: F403
from videos.music.variations import rows_before

CELLS = [("anechoic", r"no room", GREY_A), ("room", r"a small room", BLUE), ("hall", r"a shoebox hall", TUNE),
         ("cathedral", r"a cathedral", EAR), ("circling", r"circling you", "#A3E635")]


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
        d = load("tune55")
        c = clip("tune.variation55")
        st = d["starts"]
        head = VGroup(label(r"Variation 55", font_size=48, color=TUNE), label(r"the Tune, \ walked through four spaces", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        subs = ["", rf"{d['T'][1]:.2f} s", rf"{d['T'][2]:.1f} s", rf"{d['T'][3]:.1f} s", rf"once in {d['circle_s']:.1f} s"]
        cells = VGroup(*[VGroup(RoundedRectangle(width=2.3, height=1.3, corner_radius=0.15, stroke_color=col),
                                VGroup(label(t, font_size=19, color=col), label(sb if sb else r"anechoic", font_size=15, color=GREY_A)).arrange(DOWN, buff=0.12)).arrange(ORIGIN)
                         for (k, t, col), sb in zip(CELLS, subs)]).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.2)
        note = label(r"headphones: \ every space simulated, \ rendered round a spherical head", font_size=18, color=GREY_A).next_to(cells, DOWN, buff=0.45)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> Here, with headphones, it "
            "is sung with no room at all, then in a small room, a shoebox hall and a cathedral, all simulated; and then its first "
            "two phrases circle round you."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cells), FadeIn(note))
        keys = [k for k, _, _ in CELLS]
        with self.listen(c) as snd:
            window(snd, r"Variation 55", kind="physical model", detail=r"Part 8's voice, \ four spaces, \ headphones", corner=DL, tag_corner=DR)
            for i, k in enumerate(keys):
                end = st[keys[i + 1]] - 0.3 if i + 1 < len(keys) else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger(self):
        v = load("variation")
        d = load("tune55")
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).move_to(DOWN * 0.2)
        head = label(r"the Variations ledger", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            f"Row fifty-five of the ledger. Reverberation times of nought, {say(d['T'][1], 2)}, {say(d['T'][2], 1)} and "
            f"{say(d['T'][3], 1)} seconds; and one circle of the head in {say(d['circle_s'], 1)} seconds."
        ):
            self.play(FadeIn(head), FadeIn(led, shift=UP * 0.2))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"in a diffuse field, \ $T_{60} = 0.161\,V/A$ \ (Sabine), \ corrected for dead rooms \ (Eyring)",
            r"below the Schroeder frequency a room is a set of modes, \ crowding as $f^3$",
            r"absorbers take energy; \ diffusers, \ by a Gauss sum, \ spread it",
            r"early lateral reflections make a hall wide; \ narrow halls have more",
            r"two ears hear time and level differences, \ blind on a cone; \ pinnae and movement break it",
            r"panning, \ Ambisonics, \ wave fields and binaural filters build space back",
        ], title=r"What we found", font_size=21).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? In a diffuse field, reverberation time is nought point one six one times the volume over the "
            "absorption, with Eyring's correction for dead rooms. <bookmark mark='a'/> Below the Schroeder frequency a room is a "
            "set of modes, crowding as the cube of the frequency. <bookmark mark='b'/> Absorbers take energy away; diffusers, by "
            "a Gauss sum, spread it. <bookmark mark='c'/> Early reflections from the sides make a hall wide, and narrow halls "
            "have more of them. <bookmark mark='d'/> Two ears hear time and level differences, which are blind on a cone, and "
            "the pinnae and movement break the cone. <bookmark mark='e'/> And panning, Ambisonics, wave fields and binaural "
            "filters build space back."
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
            r"A room 10 by 8 by 4 m has $\bar\alpha = 0.2$ on every surface. \ Find $T_{60}$ by Sabine and by Eyring.",
            r"Prove that $\bigl|\sum_{n=0}^{N-1} e^{2\pi i (n^2 + kn)/N}\bigr| = \sqrt{N}$ for an odd prime $N$ and every $k$.",
            r"\textbf{Ear.} \ The lab plays noise from random directions round a spherical head; \ name each angle.",
            r"\textbf{Build.} \ Add scattering to the image-source room and see its $T_{60}$ approach Eyring's.",
            r"$\bigstar$ \ What is the least you need to know about a listener's ears to render space for them as well as their own HRTF?",
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
            (r"recording and mixing: \ stereo pairs, \ panning, \ depth and width", [56]),
            (r"mastering and loudness: \ the listener's room and headphones", [57]),
            (r"live sound: \ halls, \ feedback, \ arrays and delays", [59]),
            (r"source separation: \ spatial cues as a way to pull sources apart", [64]),
            (r"generative audio: \ rooms and spaces learned from data", [66]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? In recording and mixing, with stereo pairs, panning, depth and width. In mastering, "
            "which must survive every listener's room and headphones. In live sound, with halls, feedback, arrays and delays. "
            "In source separation, where spatial cues pull sources apart. And in generative audio, where rooms are learned "
            "from data."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"room builders", r"choose $T_{60}$ for the use; \ diffuse rather than deaden"),
            (r"home listeners", r"move the seat and the subwoofer before buying an equalizer"),
            (r"mixers", r"use constant-power pans; \ check the mix off the centre line and in mono"),
            (r"spatial audio", r"add a room and track the head, \ or sounds stay inside it"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Room builders choose the reverberation time for the use, and diffuse rather than deaden. Home "
            "listeners move the seat and the subwoofer before buying an equalizer. Mixers use constant-power pans, and check "
            "the mix off the centre line and in mono. And spatial audio adds a room and tracks the head, or sounds stay inside "
            "it."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"H. Kuttruff, \ \textit{Room Acoustics} \ (6th ed., \ 2016)",
             r"L. Beranek, \ \textit{Concert Halls and Opera Houses} \ (2nd ed., \ 2004)",
             r"J. Blauert, \ \textit{Spatial Hearing} \ (rev. ed., \ 1997)",
             r"F. Zotter and M. Frank, \ \textit{Ambisonics} \ (2019)",
             r"F. A. Everest and K. C. Pohlmann, \ \textit{Master Handbook of Acoustics} \ (7th ed., \ 2021)"],
            [r"W. C. Sabine, \ `Reverberation' \ (1900)",
             r"M. R. Schroeder, \ `Diffuse sound reflection by maximum-length sequences' \ (JASA, \ 1975)",
             r"J. B. Allen and D. A. Berkley, \ `Image method for efficiently simulating small-room acoustics' \ (JASA, \ 1979)",
             r"M. A. Gerzon, \ `Periphony: \ with-height sound reproduction' \ (JAES, \ 1973)"],
            font_size=18)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        play_next_part(
            self, 55, "one recording, three mixes",
            "Is it still the same piece of music?",
            "Take one multitrack recording and mix it three times: close and dry, a wall of sound, a dub. "
            "<bookmark mark='a'/> Is it still the same piece of music? <bookmark mark='b'/> Next time. Part 56: "
            "Recording and Mixing.",
            signoff=clip("bridge.signoff"))
