from __future__ import annotations

import numpy as np

from videos.music.music8.common import *  # noqa: F403


class Lips(SoundScene):
    def construct(self):
        chapter(self, 5, r"Lips and brass", r"How does a tube with no holes play a tune?", lit=(1863,), extra=((1818, r"the first valves"),))
        self.valve()
        self.bell()
        self.call()
        self.valves()

    # ------------------------------------------------------------------
    def valve(self):
        rows = rows_card([
            (r"a reed", r"breath pushes it \emph{shut}. \ It is stiff and light, \ and follows the pipe: \\ the pipe chooses the note."),
            (r"a pair of lips", r"breath pushes them \emph{open}. \ They are heavy and soft, \ with a frequency of their own \\ that the player sets by tightening them."),
            (r"so, \ on a brass instrument", r"the lips buzz near the frequency the player chooses, \\ and the tube answers if it has a resonance close by."),
        ], left=-6.5, text_left=-2.3, top=0.6, step=1.45, name_size=28, text_size=24, color=BRASS)
        head = label(r"A second kind of valve", font_size=38, color=GREY_A).to_edge(UP, buff=0.4)
        d = load("lips")
        horn = bore_shape(d["profile_x"], d["profile_r"], width=9.0, height=1.2, color=BRASS).move_to(UP * 2.0)
        buzz = Dot(horn.get_left() + LEFT * 0.2, radius=0.12, color=EAR)
        self.play(FadeIn(head), FadeIn(horn), FadeIn(buzz), run_time=0.6)
        with self.voiceover(
            "A trumpet, a horn, a trombone, a tuba. No reed, and until two hundred years ago no holes or "
            "valves either: one length of tube. The valve is the player's own lips, pressed into a small cup "
            "at the end of the tube and blown through until they buzz. <bookmark mark='a'/> Lips are a "
            "different kind of valve. A reed is pushed shut by the breath. It is light and stiff, far "
            "quicker than the pipe, and so it simply follows what the pipe tells it. <bookmark mark='b'/> "
            "Lips are pushed open by the breath. And they are heavy and soft: they have a frequency of "
            "their own, low when they are slack and high when they are tight. <bookmark mark='c'/> So on a "
            "brass instrument the choice of note is shared. The player sets the lips to buzz near a "
            "frequency, and the tube joins in if it has a resonance close by. If it has not, the note "
            "cracks, or does not come at all. Everything depends on where the tube's resonances are."
        ) as vo:
            for mark, r in zip("abc", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bell(self):
        d = load("lips")
        shape = bore_shape(d["profile_x"], d["profile_r"], width=9.6, height=1.5, color=BRASS).move_to(UP * 2.5)
        tags = VGroup(label(r"mouthpiece", font_size=20, color=GREY_B).next_to(shape, LEFT, buff=0.15), label(r"bell", font_size=20, color=GREY_B).next_to(shape, RIGHT, buff=0.15))
        g = axes([0, 1100], [-0.3, 2.7], x_length=11.0, y_length=3.0, xlabel=r"frequency (Hz)", ylabel="", xticks=[0, 200, 400, 600, 800, 1000], yticks=[], font_size=20)
        g.move_to(DOWN * 1.2)
        pp, pk = d["plain_peaks"], d["peaks"]
        f0 = d["f0"]
        row = lambda fs, y, col: VGroup(*[VGroup(Line(g.ax.c2p(f, y - 0.22), g.ax.c2p(f, y + 0.22), color=col, stroke_width=5),  # noqa: E731
                                                 label(rf"{f:.0f}", font_size=18, color=col).next_to(g.ax.c2p(f, y + 0.22), UP, buff=0.05)) for f in fs if f < 1080])
        r1 = row(pp, 1.75, GREY_B)
        r2 = row(pk, 0.55, BRASS)
        l1 = label(r"a plain tube, \ shut by the lips", font_size=22, color=GREY_B).move_to(g.ax.c2p(560, 2.5))
        l2 = label(r"with mouthpiece and bell", font_size=22, color=BRASS).move_to(g.ax.c2p(560, 1.28))
        ticks = VGroup(*[VGroup(Line(g.ax.c2p(n * f0, -0.3), g.ax.c2p(n * f0, -0.12), color=TUNE, stroke_width=4),
                                label(str(n), font_size=18, color=TUNE).next_to(g.ax.c2p(n * f0, -0.12), UP, buff=0.04)) for n in range(1, 10)])
        tl = label(rf"the multiples of {f0:.0f} Hz", font_size=22, color=TUNE).next_to(g, DOWN, buff=0.55).shift(RIGHT * 3.6)
        with self.voiceover(
            "And at first sight the resonances are in the wrong places. A brass tube is closed at the lips "
            f"and open at the far end, like a clarinet. <bookmark mark='a'/> A plain tube as long as a trumpet's "
            f"has its resonances at {say(pp[0])}, {say(pp[1])}, {say(pp[2])}, {say(pp[3])} hertz: one, three, "
            "five, seven. The notes of a bugle call are not in there. <bookmark mark='b'/> Now put a real "
            "trumpet's shape on it: a cup and a narrow throat at one end, and at the other a bell that "
            f"flares. Monochord computes the resonances again: {say(pk[1])}, {say(pk[2])}, {say(pk[3])}, "
            f"{say(pk[4])}, {say(pk[5])}. <bookmark mark='c'/> Those are very nearly two, three, four, five "
            f"and six times {say(f0)} hertz, which is the B flat that a trumpet is named after. The shape "
            "has moved every resonance, the low ones up and the high ones down, until an odd series became "
            "a whole one. How? A low note turns back early in the flare, where the bell is still narrow, so "
            "for low notes the tube is short. A high note travels further out before the bell lets it go. "
            "The tube is a different length for every note, and four centuries of makers found by trial "
            "the flare that makes the lengths come out right. <bookmark mark='d'/> Except for one. The "
            f"lowest resonance is at {say(d['pedal'])} hertz, nowhere near {say(f0)}. Hold that thought."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(r1), FadeIn(l1))
            vo.wait_until("b")
            self.play(FadeIn(shape), FadeIn(tags))
            self.play(FadeIn(r2), FadeIn(l2))
            vo.wait_until("c")
            self.play(FadeIn(ticks), FadeIn(tl))
            vo.wait_until("d")
            self.play(Indicate(r2[0], color=BAD, scale_factor=1.4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def call(self):
        d = load("lips")
        c = clip("lips.call")
        st = [s for s in d["stairs"] if s["amp"] > 0.3]
        g = axes([140, 800], [80, 1000], x_length=6.2, y_length=4.2, xlabel=r"the frequency the lips are set to (Hz)", ylabel=r"the note that sounds (Hz)", xticks=[200, 400, 600, 800], yticks=[200, 400, 600, 800], font_size=20)
        g.move_to(LEFT * 3.4 + DOWN * 0.4)
        pts = VGroup(*[Dot(g.ax.c2p(s["lip"], s["hz"]), radius=0.055, color=BRASS if s["hz"] > 150 else EAR) for s in st])
        lines = VGroup(*[DashedLine(g.ax.c2p(140, f), g.ax.c2p(800, f), color=GREY_D, stroke_width=1.2) for f in d["peaks"][1:8]])
        note = listen_note(r"Eight notes on one length of tube. \\ Nothing changes but the lips.", width=4.8, font_size=24).move_to(RIGHT * 3.9 + UP * 2.2)
        order = d["order"]
        steps = VGroup(*[VGroup(RoundedRectangle(width=0.62, height=0.5, corner_radius=0.1, stroke_color=BRASS, stroke_width=2), label(str(k), font_size=26, color=BRASS)) for k in order]).arrange(RIGHT, buff=0.1).move_to(RIGHT * 3.7 + DOWN * 0.2)
        sl = label(r"which resonance", font_size=22, color=GREY_B).next_to(steps, UP, buff=0.15)
        with self.voiceover(
            "Now let the lips choose. Monochord has a model of a pair of lips, a mass on a spring that the "
            "breath blows open, and here it is on the trumpet, with the lips set to one frequency after "
            "another. <bookmark mark='a'/> The note that sounds does not follow the lips smoothly. It climbs "
            "a staircase. Each step is one of the tube's resonances, shown as a dashed line, and the note "
            "sits a little above the frequency of the lips themselves. Tighten the lips gradually and the "
            "horn jumps from one resonance to the next. That is all a bugler does. Listen to eight notes on "
            "one length of tube."
        ) as vo:
            self.play(FadeIn(g), FadeIn(lines))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.05), FadeIn(note), FadeIn(steps), FadeIn(sl), run_time=3.0)
        with self.listen(c) as snd:
            window(snd, r"a call on one length of tube", detail=r"model lips on a model trumpet", corner=DL, tag_corner=DR)
            for k, (b, dur) in enumerate(zip(steps, d["durs"])):
                t0 = snd.time_of(f"n{k}")
                pulse(snd, b, t0, t0 + dur - 0.03, buff=0.05)
        ped = [s for s in d["stairs"] if s["amp"] > 0.3 and s["hz"] < 150]
        extra = VGroup(label(rf"the notes it played: \\ {d['heard'][0]:.0f}, \ {d['heard'][1]:.0f}, \ {d['heard'][2]:.0f}, \ {d['heard'][7]:.0f} Hz", font_size=24, color=BRASS),
                       label(rf"and twice, \ unasked: \ {ped[0]['hz']:.0f} Hz, \\ where the tube has no resonance", font_size=24, color=EAR)).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(RIGHT * 3.7 + DOWN * 2.0)
        with self.voiceover(
            "Three, four, five, six times the B flat: the notes of every bugle call there is. "
            "<bookmark mark='a'/> And look at the two stray points at the bottom of the staircase. Twice, "
            f"while climbing, the model dropped to {say(ped[0]['hz'])} hertz, where this tube has no resonance "
            "at all. That is the note brass players call the pedal. Nothing at that frequency holds it up. "
            "But its second harmonic sits on one resonance, its third on the next, its fourth on the next, "
            "and between them they hold the lips to a rhythm whose fundamental the tube does not support. "
            "It is Part 4's missing fundamental, happening inside a trumpet, and nobody told the model to "
            "do it."
        ) as vo:
            self.play(FadeOut(note), FadeIn(extra[0]))
            vo.wait_until("a")
            self.play(FadeIn(extra[1]), *[Indicate(p, color=EAR, scale_factor=2.0) for p in pts if p.get_color() != ManimColor(BRASS)])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def valves(self):
        d = load("lips")
        v = d["valves"]
        title = label(r"A worked example: \ three valves", font_size=36).to_edge(UP, buff=0.4)
        facts = VGroup(label(r"a semitone lower needs a tube 5.9\% longer", font_size=26, color=GREY_A),
                       label(rf"valve 2 adds {100 * v['v2']:.1f}\% \ (one semitone); \quad valve 1, \ {100 * v['v1']:.1f}\% \ (two); \quad valve 3, \ {100 * v['v3']:.1f}\% \ (three)", font_size=26)).arrange(DOWN, buff=0.15).move_to(UP * 2.0)
        ask = pause_card(r"Press valves 1 and 3 together, \ for five semitones. \\ How much tube do they add? \ How much is needed? \ Is the note sharp or flat?", width=9.0, font_size=26).move_to(DOWN * 0.3)
        work = VGroup(MathTex(rf"\text{{added:}}\quad {100 * v['v1']:.1f}\% + {100 * v['v3']:.1f}\% = {100 * v['have_13']:.1f}\%", font_size=34),
                      MathTex(rf"\text{{needed:}}\quad 2^{{5/12}} - 1 = {100 * v['need_13']:.1f}\%", font_size=34),
                      label(rf"too short: \ {v['sharp_cents']:.0f} cents sharp, \ {v['extra_cm']:.1f} cm missing on a {v['tube_cm']:.0f} cm trumpet", font_size=28, color=BAD)).arrange(DOWN, buff=0.25).move_to(DOWN * 0.4)
        end = label(r"the cure is a finger ring on the third valve's slide, \ pushed out for those notes", font_size=26, color=TUNE).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "A bugle's notes have gaps. To fill them, around 1818, makers added valves, and each valve "
            "switches an extra loop of tubing into the horn. A worked example. To lower any note by a "
            "semitone, the tube must become five point nine percent longer. The second valve adds that much. "
            "The first adds enough for two semitones, the third for three. <bookmark mark='a'/> Now press "
            "the first and third together, to go down five semitones. How much tube have you added, how much "
            "did you need, and is the note sharp or flat? Pause, and work it out."
        ) as vo:
            self.play(FadeIn(title), FadeIn(facts))
            vo.wait_until("a")
            self.play(FadeIn(ask, shift=UP * 0.2))
        self.wait(1.5)
        with self.voiceover(
            f"The two loops add {say(100 * v['have_13'], 1)} percent. <bookmark mark='a'/> Five semitones need "
            f"{say(100 * v['need_13'], 1)}. Percentages multiply; loops of tube only add. <bookmark mark='b'/> "
            f"The horn is too short, by about {say(v['extra_cm'])} centimetres on a real trumpet, and the "
            f"note is {say(v['sharp_cents'])} cents sharp: a third of a semitone, far too much to leave. "
            "<bookmark mark='c'/> So every trumpet has a ring for the left hand's third finger, which pushes "
            "the third valve's slide out for exactly those notes. A trombone has no such trouble. Its slide "
            "is the whole instrument."
        ) as vo:
            self.play(FadeOut(ask), FadeIn(work[0]))
            vo.wait_until("a")
            self.play(FadeIn(work[1]))
            vo.wait_until("b")
            self.play(FadeIn(work[2]))
            vo.wait_until("c")
            self.play(FadeIn(end))
        self.wait(0.3)
        self.clear_scene()
