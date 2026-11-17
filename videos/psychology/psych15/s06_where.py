from __future__ import annotations

import numpy as np

from videos.psychology.psych15.common import *  # noqa: F403


class Where(VoiceoverScene):
    def construct(self):
        self.card()
        self.cues()
        self.jeffress()
        self.array()
        self.mammals()

    def card(self):
        card = chapter_card(5, r"Where is it?", r"How do two ears find a sound in space?",
                            lit={1907: r"Rayleigh", 1948: r"Jeffress"}, part=PART, scale=("circuit",), marr=("what", "how"))
        with self.voiceover("Chapter five. Where is it?"):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def cues(self):
        d = load("itd")
        head = heading(r"Two cues, \ two ears")
        headc = Circle(radius=0.9, color=GREY_B, stroke_width=3).move_to([-4.6, 0.4, 0])
        earL = Dot(headc.get_left(), color=EAR_L, radius=0.1)
        earR = Dot(headc.get_right(), color=EAR_R, radius=0.1)
        src = Dot([-4.6 + 2.6 * np.sin(np.radians(30)), 0.4 + 2.6 * np.cos(np.radians(30)), 0], color=YOU, radius=0.12)
        rays = VGroup(DashedLine(src.get_center(), earR.get_center(), color=EAR_R, stroke_width=2),
                      DashedLine(src.get_center(), earL.get_center(), color=EAR_L, stroke_width=2))
        A = axes([-90, 90], [-700, 700], x_length=5.0, y_length=2.8, xticks=[-90, -45, 0, 45, 90],
                 yticks=[-600, 0, 600], xlabel=r"direction (degrees)", ylabel=r"ITD ($\mu$s)",
                 center=[1.6, 1.0, 0])
        c = curve(A.ax, d["az"], d["itd_us"], TIMING, stroke_width=4)
        rows = rows_of([
            (rf"time: \ the far ear hears it later, \ by up to about {d['max_us']:.0f} $\mu$s", TIMING),
            (r"level: \ the head casts a sound shadow, \ but only for wavelengths smaller than the head", PLACE),
            (r"Rayleigh's duplex theory, \ 1907: \ timing for low frequencies, \ level for high", WHITE),
            (r"people notice a timing difference of about 10 $\mu$s: \ a hundredth of a millisecond", YOU),
        ], 12.6, 26, 0.24).to_edge(DOWN, buff=0.75)
        tag = psyche_tag(r"computed: \ Woodworth's formula, \ a spherical head of radius 8.75 cm")
        with self.voiceover(
            "Your eyes map space directly onto the retina. Your ears don't: the cochlea maps frequency. So where a "
            "sound is has to be computed. <bookmark mark='a'/> A sound off to one side reaches the far ear later. For a "
            "head this size, the delay grows from zero straight ahead to about six hundred and fifty millionths of a "
            "second at the side. <bookmark mark='b'/> The far ear also hears it more quietly, because the head casts a "
            "sound shadow, but only for wavelengths shorter than the head, so only for high frequencies. "
            "<bookmark mark='c'/> Lord Rayleigh put the two together in 1907, in what's called the duplex theory: "
            "timing for low frequencies, level for high. <bookmark mark='d'/> The timing cue is astonishingly fine. "
            "People can detect a difference of about ten microseconds, a hundredth of a millisecond, though a single "
            "nerve impulse lasts about a millisecond."
        ) as vo:
            self.play(FadeIn(head), FadeIn(headc), FadeIn(earL), FadeIn(earR), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(src), Create(rays), FadeIn(A), Create(c), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def jeffress(self):
        head = heading(r"Jeffress's circuit, \ 1948")
        n = 7
        xs = np.linspace(-3.6, 3.6, n)
        dets = VGroup(*[Circle(radius=0.22, color=GREY_B, stroke_width=3).move_to([x, 0.3, 0]) for x in xs])
        lineL = Arrow([-5.2, 1.4, 0], [4.6, 1.4, 0], buff=0, color=EAR_L, stroke_width=4, max_tip_length_to_length_ratio=0.03)
        lineR = Arrow([5.2, -0.8, 0], [-4.6, -0.8, 0], buff=0, color=EAR_R, stroke_width=4, max_tip_length_to_length_ratio=0.03)
        taps = VGroup()
        for x in xs:
            taps.add(Line([x, 1.4, 0], [x, 0.52, 0], color=EAR_L, stroke_width=2))
            taps.add(Line([x, -0.8, 0], [x, 0.08, 0], color=EAR_R, stroke_width=2))
        ll = label(r"from the left ear", font_size=22, color=EAR_L).next_to(lineL, UP, buff=0.1).align_to(lineL, LEFT)
        rl = label(r"from the right ear", font_size=22, color=EAR_R).next_to(lineR, DOWN, buff=0.1).align_to(lineR, RIGHT)
        win = dets[4].copy().set_fill(YOU, opacity=0.8)
        rows = rows_of([
            (r"two axons run in opposite directions past a row of coincidence detectors", WHITE),
            (r"a detector fires only when spikes from both ears arrive together", PRIOR),
            (r"a sound from the right starts its signal early; \ the signals meet left of centre", YOU),
            (r"which detector fires is where the sound is: \ a map of space, \ built from delays", TIMING),
        ], 12.6, 26, 0.24).to_edge(DOWN, buff=0.75)
        tag = note(r"drawn after Jeffress (1948)").to_corner(DR, buff=0.3)
        with self.voiceover(
            "How could neurons measure ten microseconds? In 1948, the psychologist Lloyd Jeffress proposed a circuit. "
            "<bookmark mark='a'/> Two axons, one from each ear, run in opposite directions past a row of neurons. "
            "<bookmark mark='b'/> Each neuron is a coincidence detector: it fires only when spikes from both ears "
            "arrive at the same moment. <bookmark mark='c'/> Because the axons are delay lines, a sound that reaches "
            "the right ear first has its signal start early, and the two signals meet, not in the middle, but toward "
            "the other end. <bookmark mark='d'/> Which detector fires tells you where the sound is. A map of space, "
            "built out of conduction delays. It's one of the most elegant ideas in neuroscience."
        ) as vo:
            self.play(FadeIn(head), FadeIn(dets), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowArrow(lineL), GrowArrow(lineR), FadeIn(ll), FadeIn(rl), Create(taps), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(win), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def array(self):
        d = load("itd")
        head = heading(r"Psyche's Jeffress array")
        A = axes([-700, 700], [0, max(d["counts"]) * 1.15], x_length=7.4, y_length=4.2, xticks=[-600, -300, 0, 300, 600],
                 yticks=[], xlabel=r"each detector's internal delay ($\mu$s)", ylabel=r"coincidences",
                 center=[-2.3, -0.3, 0])
        ax = A.ax
        bars = VGroup(*[Line(ax.c2p(x, 0), ax.c2p(x, y), color=GREY_B, stroke_width=5) for x, y in
                        zip(d["delays_us"], d["counts"])])
        true = DashedLine(ax.c2p(d["true_us"], 0), ax.c2p(d["true_us"], max(d["counts"]) * 1.1), color=YOU, stroke_width=2)
        tl = label(r"the true delay", font_size=20, color=YOU).next_to(true, UP, buff=0.05)
        rows = rows_of([
            (r"a 500 Hz tone from 30$^\circ$ to the right; \ phase-locked spikes from each ear, \ 3 s", WHITE),
            (rf"true delay {d['true_us']:.0f} $\mu$s; \ the busiest detector: \ {d['best_us']:.0f} $\mu$s, \ read as {d['best_az']:.0f}$^\circ$", TIMING),
            (r"above about 1.5 kHz a period is shorter than the head's delays: \ several peaks, \ ambiguous by whole cycles", BAD),
        ], 4.6, 26, 0.34).move_to([4.6, -0.2, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ \texttt{hearing.jeffress}")
        with self.voiceover(
            "Here it is in Psyche. <bookmark mark='a'/> A five-hundred-hertz tone from thirty degrees to the right. "
            "Each ear's fibre fires in step with the tone, with a little jitter, for three seconds. Each bar is one "
            "detector, counting how often spikes from the two ears coincide after its own internal delay. "
            "<bookmark mark='b'/> The true delay is about two hundred and sixty microseconds, and the busiest detector "
            "sits within a step of it: thirty-two degrees. <bookmark mark='c'/> At five hundred hertz one cycle lasts two "
            "milliseconds, longer than any delay a head can make, so there's just one peak. Above about fifteen "
            "hundred hertz a cycle is shorter than the head's delays, and the array finds several peaks, a whole "
            "cycle apart: a pure tone is ambiguous. That's one reason timing serves low frequencies, as Rayleigh "
            "said. Real sounds, with many frequencies, resolve the ambiguity, because only the true delay lines up "
            "for all of them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(b) for b in bars], lag_ratio=0.03), FadeIn(rows[0]), run_time=3.0)
            vo.wait_until("b")
            self.play(Create(true), FadeIn(tl), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def mammals(self):
        head = heading(r"Owls, \ yes; \ mammals, \ perhaps not")
        rows = rows_of([
            (r"barn owls: \ delay lines and a map of coincidence detectors, \ much as Jeffress drew", TIMING),
            (r"gerbils, \ 2002: \ precisely timed inhibition shifts each neuron's best delay", PLACE),
            (r"mammalian neurons are broadly tuned, \ most preferring sounds from the opposite side", WHITE),
            (r"a code in the balance of two broad channels, \ not a map: \ the same answer, \ another algorithm", PRIOR),
            (r"and up or down, \ front or back: \ the folds of the outer ear filter sound differently from each direction", SOUND),
        ], 12.6, 27, 0.36).move_to([0, -0.1, 0])
        with self.voiceover(
            "Did evolution build Jeffress's circuit? <bookmark mark='a'/> In birds, largely yes. Barn owls, which hunt "
            "mice in the dark by sound, have axons that act as delay lines and a map of coincidence detectors, much as "
            "Jeffress drew it. <bookmark mark='b'/> In mammals the story changed. In 2002, Antje Brand, Benedikt "
            "Grothe and colleagues showed that in gerbils, precisely timed inhibition shifts each neuron's best "
            "delay. <bookmark mark='c'/> Mammalian neurons are broadly tuned, and on each side of the brain most prefer "
            "sounds from the opposite side. <bookmark mark='d'/> Direction seems to be read from the balance between "
            "two broad channels, not from a map. It's Marr's levels again: the same computation, a different "
            "algorithm. <bookmark mark='e'/> And two ears can't tell front from back, or up from down. For that, the "
            "folds of your outer ear filter sound differently from each direction, and the brain learns your ears' "
            "filtering, which is why a recording made through someone else's ears often places sounds wrongly, "
            "most often front-to-back."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
