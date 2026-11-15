from __future__ import annotations

import numpy as np

from videos.music.music49.common import *  # noqa: F403


class Plates(SoundScene):
    def construct(self):
        chapter(self, 10, r"Plates and springs", r"How did steel sheets and coils become reverbs?")
        self.plate()
        self.simulation()
        self.dispersion()
        self.hear_plate()
        self.spring()
        self.practice()

    # ------------------------------------------------------------------
    def plate(self):
        items = [
            (r"EMT's 140 \ (1957): \ a steel sheet about 2 by 1 m, \ hung by its corners in a frame", WHITE),
            (r"a driver shakes it at one point; \ contact microphones pick it up at others", WHITE),
            (r"a felt damping pad, \ moved closer or further, \ sets the decay from about one to five seconds", WHITE),
            (r"bending waves in a plate are dispersive: \ high frequencies travel faster than low ones", TUNE),
            (r"the result is dense and bright, \ with no early reflections: \ the sound of countless pop vocals", GREY_A),
        ]
        rows_scene(self, r"a plate of steel", items,
                   "Before computers, studios used metal. <bookmark mark='b'/> EMT's model 140, from 1957, was a steel sheet about "
                   "two metres by one, hung by its corners in a frame. <bookmark mark='c'/> A driver shook it at one point and "
                   "contact microphones picked it up at others. <bookmark mark='d'/> A felt damping pad, moved closer or further, "
                   "set the decay from about one second to five. <bookmark mark='e'/> Bending waves in a plate are dispersive: "
                   "high frequencies travel faster than low ones. <bookmark mark='f'/> The result is dense and bright, with no "
                   "early reflections: the sound of countless pop vocals.", marks="bcdef")

    # ------------------------------------------------------------------
    def simulation(self):
        d = load("plate")
        rows_ = text_rows([
            (r"Kirchhoff's plate: \ $u_{tt} = -\kappa^2 \nabla^4 u - 2\sigma_0 u_t + 2\sigma_1 \nabla^2 u_t$", WHITE),
            (rf"steel 0.5 mm thick: \ $\kappa = {d['kappa']:.3f}$ m$^2$/s", WHITE),
            (rf"a grid of {d['grid'][0]} by {d['grid'][1]} points, \ {1000 * d['h']:.1f} mm apart, \ stepped 48,000 times a second", WHITE),
            (rf"stable only if $\kappa\,\Delta t / h^2 \le 1/4$: \ here {d['mu']:.3f}", TUNE),
            (r"struck once at one point; \ its velocity recorded at another: \ the plate's impulse response", GREY_A),
        ], font_size=22)
        head = label(r"a plate, \ by finite differences", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "We can build one. <bookmark mark='a'/> A thin plate obeys Kirchhoff's equation: its acceleration is minus kappa "
            "squared times the fourth spatial derivative of its displacement, with two loss terms, one for all frequencies and "
            "one that damps the highs faster, following Stefan Bilbao's scheme. <bookmark mark='b'/> For steel half a millimetre "
            f"thick, kappa is {say(d['kappa'], 3)}. <bookmark mark='c'/> Cover the plate with a grid of "
            f"{say(d['grid'][0])} by {say(d['grid'][1])} points, {say(1000 * d['h'], 1)} millimetres apart, and step it "
            "forty-eight thousand times a second. <bookmark mark='d'/> The scheme is stable only if kappa times the time step "
            f"over the grid spacing squared is at most a quarter; ours is {say(d['mu'], 3)}. <bookmark mark='e'/> Strike it once "
            "at one point and record the motion at another: the plate's impulse response."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(rows_, 0.15)))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dispersion(self):
        d = load("plate")
        ir = np.array(d["ir"])
        t = np.arange(len(ir)) * 6 / 48000 * 1000
        ax = frame_axes(width=5.6, height=2.2, xlo=0, xhi=120, ylo=-1, yhi=1, center=LEFT * 3.3 + DOWN * 0.4)
        cv = curve(t, ir / np.max(np.abs(ir)), ax.to, color=TUNE, width=0.8)
        sg = sgram(d["spec"], width=5.6, height=2.6).move_to(RIGHT * 3.2 + DOWN * 0.4)
        la = label(r"the first 120 ms", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.15)
        lb = label(r"its spectrogram: \ 0 to 12 kHz up, \ 120 ms across", font_size=17, color=GREY_A).next_to(sg, UP, buff=0.15)
        head = label(rf"the plate's response \ (RT60 {d['rt60']:.1f} s)", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is the start of the plate's response. <bookmark mark='a'/> It begins with a bright zing. "
            "<bookmark mark='b'/> The spectrogram shows why: the highest frequencies arrive first and the lower ones after them, "
            "because in a plate fast vibrations travel faster. After a few reflections from the edges the waves overlap into a dense, "
            f"bright wash, decaying with a reverberation time of {say(d['rt60'], 1)} seconds."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ax), FadeIn(la), Create(cv), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(sg), FadeIn(lb))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear_plate(self):
        c = clip("plate.tune")
        box = VGroup(RoundedRectangle(width=5.0, height=1.3, corner_radius=0.15, stroke_color=GREY_B), label(r"the Tune, \ on the simulated plate", font_size=24, color=WHITE)).arrange(ORIGIN).move_to(UP * 0.3)
        plate = Rectangle(width=4.0, height=2.0, stroke_color=GREY_A, fill_color="#9AA5B1", fill_opacity=0.25).next_to(box, DOWN, buff=0.5)
        head = label(r"the plate, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear the Tune's first phrase on the simulated plate."):
            self.play(FadeIn(head), FadeIn(box), FadeIn(plate))
        with self.listen(c) as snd:
            window(snd, r"the plate", kind="synthesized", detail=r"Part 7's piano, \ a finite-difference plate", corner=DL, tag_corner=DR)
            pulse(snd, plate, 0.0, c.duration, buff=0.1)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def spring(self):
        d = load("spring")
        c = clip("spring.hit")
        sg = sgram(d["spec"], width=6.0, height=2.0).move_to(UP * 0.9)
        lb = label(r"the spring model's first 250 ms: \ every trip round the coil comes back smeared into a chirp", font_size=17, color=GREY_A).next_to(sg, UP, buff=0.15)
        rows_ = text_rows([
            (r"springs: \ invented for Hammond organs, \ built into guitar amplifiers from the 1960s", WHITE),
            (r"a coil is very dispersive: \ each echo returns smeared into a chirp, \ the `drip' of surf guitar", WHITE),
            (r"here modelled as a loop of 80 all-passes and a 35 ms delay: \ a stand-in for the coil's physics", TUNE),
        ], font_size=19).to_edge(DOWN, buff=1.1)
        head = label(rf"a spring \ (RT60 {d['rt60']:.1f} s)", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Springs were cheaper still. <bookmark mark='a'/> Invented for Hammond organs, they went into guitar amplifiers "
            "from the 1960s. <bookmark mark='b'/> A coil is extremely dispersive: each echo comes back smeared into a chirp, the "
            "drip of surf guitar. <bookmark mark='c'/> Our spring is a stand-in for the coil's physics: a loop of eighty "
            "all-passes and a thirty-five millisecond delay. Hear a snare hit and a bass note on it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sg), FadeIn(lb), FadeIn(rows_[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows_[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows_[2]))
        with self.listen(c) as snd:
            window(snd, r"the spring", kind="synthesized", detail=r"Part 40's snare, \ a plucked bass", corner=DL, tag_corner=DR)
            pulse(snd, sg, 0.0, c.duration, buff=0.1)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def practice(self):
        items = [
            (r"plates were heavy, \ sensitive to footsteps, \ and cost as much as a car", WHITE),
            (r"they lived in basements and stairwells, \ wired to the control room", WHITE),
            (r"their sound, \ dense from the first instant and bright, \ suited vocals and snares", WHITE),
            (r"springs were cheap enough for every guitar amplifier, \ and their drip became a style", TUNE),
            (r"both are now mostly software, \ simulated from the physics of chapter 10's kind", GREY_A),
        ]
        rows_scene(self, r"plates and springs in practice", items,
                   "In practice, plates were heavy, sensitive to footsteps, and cost as much as a car. <bookmark mark='b'/> They "
                   "lived in basements and stairwells, wired to the control room. <bookmark mark='c'/> Their sound, dense from the "
                   "first instant and bright, suited vocals and snares. <bookmark mark='d'/> Springs were cheap enough for every "
                   "guitar amplifier, and their drip became a style of its own. <bookmark mark='e'/> Both are now mostly software, "
                   "simulated from the physics of this chapter's kind.", marks="bcde")
