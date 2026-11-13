from __future__ import annotations

import numpy as np

from videos.music.music8.common import *  # noqa: F403


class Jet(SoundScene):
    def construct(self):
        chapter(self, 6, r"A jet and an edge", r"What plays a flute, when nothing in it moves?", lit=(1863,), extra=((1968, r"Coltman times the flute's jet"),))
        self.jet()
        self.overblow()
        self.quiz()
        self.organ()

    # ------------------------------------------------------------------
    def jet(self):
        pipe = VGroup(Line(LEFT * 5.5 + DOWN * 0.3, RIGHT * 1.0 + DOWN * 0.3, color=GREY_B, stroke_width=5), Line(LEFT * 5.5 + UP * 0.6, LEFT * 3.6 + UP * 0.6, color=GREY_B, stroke_width=5),
                      Line(LEFT * 2.6 + UP * 0.6, RIGHT * 1.0 + UP * 0.6, color=GREY_B, stroke_width=5), Line(LEFT * 5.5 + DOWN * 0.3, LEFT * 5.5 + UP * 0.6, color=GREY_B, stroke_width=5)).scale(1.5).move_to(UP * 1.5)
        hole_l, hole_r = pipe[1].get_end(), pipe[2].get_start()
        lips = label(r"lips", font_size=22, color=EAR).next_to(hole_l, UL, buff=0.25)
        phase = ValueTracker(0.0)

        def ribbon():
            a = hole_l + UP * 0.65 + LEFT * 0.5
            pts = []
            for s in np.linspace(0, 1, 30):
                base = a + (hole_r + UP * 0.05 - a) * s
                pts.append(base + UP * 0.4 * s * np.sin(2 * np.pi * (phase.get_value() - 0.9 * s)))
            return VMobject(stroke_color=AIR, stroke_width=6).set_points_smoothly(pts)

        jet = always_redraw(ribbon)
        edge = label(r"the edge", font_size=22, color=GREY_B).next_to(hole_r, UR, buff=0.15)
        rows = VGroup(label(r"a ribbon of air crosses the mouth hole to the far edge", font_size=26, color=AIR),
                      label(r"the air sloshing in and out of the hole pushes the ribbon aside", font_size=26, color=GREY_A),
                      label(r"the push rides along the ribbon, \ and flips it: \ into the pipe, \ out, \ in, \ out", font_size=26, color=GREY_A),
                      label(r"it works when the ride takes about half a period of the note", font_size=28, color=TUNE)).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(DOWN * 2.2)
        with self.voiceover(
            "And then there is the flute, which is the strangest of all, because nothing in it moves. No "
            "reed, no lips inside the instrument. <bookmark mark='a'/> The player's lips make a thin ribbon "
            "of air, a jet, and aim it across the mouth hole at the hole's far edge. <bookmark mark='b'/> "
            "When the pipe is sounding, air sloshes in and out of that hole, and the sloshing pushes the jet "
            "sideways where it leaves the lips. <bookmark mark='c'/> The sideways push does not act at once. "
            "It rides along the jet, like a wave along a flag, and when it reaches the edge it tips the jet "
            "one way or the other: into the pipe, or out over the top. Into the pipe, out, in, out. The jet "
            "is the valve, and it is made of the same air as the breath. <bookmark mark='d'/> For the puffs "
            "to arrive at the right moment, the ride along the jet has to take about half a period of the "
            "note. John Coltman measured that in the nineteen sixties, and it is the fact that everything "
            "about playing the flute follows from."
        ) as vo:
            self.play(FadeIn(pipe))
            vo.wait_until("a")
            self.add(jet)
            phase.add_updater(lambda m, dt: m.increment_value(1.2 * dt))
            self.add(phase)
            self.play(FadeIn(lips), FadeIn(edge), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.wait(0.3)
        phase.clear_updaters()
        jet.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def overblow(self):
        d = load("jet")
        c = clip("jet.overblow")
        tr = [r for r in d["track"] if r["hz"] > 0]
        g = axes([0, 5], [220, 560], x_length=8.4, y_length=3.4, xlabel=r"seconds, \ as the player blows harder", ylabel=r"the note (Hz)", xticks=[0, 1, 2, 3, 4, 5], yticks=[262, 393, 524], font_size=20)
        g.move_to(DOWN * 0.9)
        pts = VGroup(*[Dot(g.ax.c2p(r["t"], r["hz"]), radius=0.05, color=FLUTE) for r in tr])
        note = listen_note(r"One fingering, \ blown steadily harder. \\ Follow the pitch.", width=5.6, font_size=24).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Blow harder, and the jet moves faster. The ride to the edge takes less time. So what should "
            "happen, on one fingering, if a flute is blown steadily harder? Listen, and follow the pitch."
        ):
            self.play(FadeIn(note), FadeIn(g))
        for p in pts:
            p.set_opacity(0)
            self.add(p)
        with self.listen(c) as snd:
            window(snd, r"a flute, \ blown harder and harder", detail=r"a model jet on a pipe", corner=DL, tag_corner=DR)
            snd.drive(pts, lambda m, t: [p.set_opacity(1.0 if r["t"] <= t else 0.0) for p, r in zip(m, tr)] and m)
        for p in pts:
            p.set_opacity(1)
        before = [r for r in tr if r["t"] < d["jump_t"]]
        sharp = 1200 * np.log2(max(r["hz"] for r in before) / before[2]["hz"])
        lab = VGroup(label(rf"it creeps sharp: \ {sharp:.0f} cents", font_size=24, color=TUNE).move_to(g.ax.c2p(2.0, 300)),
                     label(r"then jumps an octave", font_size=24, color=FLUTE).move_to(g.ax.c2p(3.4, 500)))
        with self.voiceover(
            f"The note creeps sharp, by {say(sharp)} cents, as the jet gets ahead of the pipe. Flute players "
            "know that well: blowing harder raises the pitch, and they correct it by rolling the flute. "
            "<bookmark mark='a'/> Then it breaks, and lands on the octave. The jet has become too quick for "
            "the pipe's first resonance, whose half period is long, and exactly right for the second, whose "
            "half period is half as long. Blow harder still and it will find the third. A flautist plays "
            "the second octave with the fingerings of the first, a faster and shorter jet, and nothing else."
        ) as vo:
            self.play(FadeOut(note), FadeIn(lab[0]))
            vo.wait_until("a")
            self.play(FadeIn(lab[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("jet")
        h = load("holes")
        c = clip("jet.quiz")
        q = listen_card(r"Two instruments. \ Each plays its lowest note, \ and then overblows. \\ One is a flute and one a clarinet. \ Which is the flute?", width=9.6, font_size=26).to_edge(UP, buff=0.35)
        bx = boxes(buff=2.4, width=3.0, height=1.3).move_to(DOWN * 0.2)
        with self.voiceover(
            "You now know enough to tell two instruments apart by a single leap. Each of these plays its "
            "lowest note and then overblows. One is a flute and one is a clarinet. Which is the flute?"
        ):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B: \ low, \ then overblown", detail=r"model instruments", corner=DL, tag_corner=DR)
            for ev, b in zip("AB", bx):
                t0 = snd.time_of(ev)
                pulse(snd, b, t0, t0 + 2.7)
        ans = VGroup(VGroup(label(r"the clarinet", font_size=28, color=CLAR), label(rf"a twelfth: \ {h['interval_cents'] / 100:.1f} semitones", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.1).next_to(bx[0], DOWN, buff=0.3),
                     VGroup(label(r"the flute", font_size=28, color=FLUTE), label(rf"an octave: \ {d['quiz']['flute_cents'] / 100:.1f} semitones", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.1).next_to(bx[1], DOWN, buff=0.3))
        with self.voiceover(
            "B was the flute: it leapt an octave. A leapt an octave and a fifth, the clarinet's twelfth. You "
            "can hear the difference between a pipe open at both ends and a pipe closed at one, in a single "
            "interval."
        ):
            self.play(FadeOut(q), FadeIn(ans))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def organ(self):
        d = load("jet")
        c = clip("jet.organ")
        stops = d["stops"]
        names = [r"8 foot", r"4 foot", r"$2\tfrac23$ foot", r"2 foot", r"$1\tfrac35$ foot"]
        knobs = VGroup(*[VGroup(Circle(radius=0.48, color=GREY_B, stroke_width=3), label(n, font_size=20, color=GREY_A)) for n in names]).arrange(RIGHT, buff=0.45).move_to(LEFT * 3.0 + UP * 1.9)
        pipes = VGroup()
        for k, s in enumerate(stops):
            hgt = 2.6 / s["harmonic"]
            p = Rectangle(width=0.34, height=hgt, stroke_color=AIR, stroke_width=2.5, fill_color=AIR, fill_opacity=0.12)
            p.move_to(knobs[k].get_center() + DOWN * 1.0, aligned_edge=UP)
            pipes.add(VGroup(p, label(rf"{s['harmonic']}", font_size=24, color=TUNE).next_to(p, DOWN, buff=0.12)))
        cap = label(r"harmonic \\ number", font_size=20, color=TUNE).next_to(pipes[4][1], RIGHT, buff=0.5)
        note = listen_note(r"One key held down; \\ five stops drawn, \ one at a time. \\ Five pipes, \\ or one sound changing colour?", width=5.0, font_size=26).move_to(RIGHT * 4.0 + DOWN * 1.6)
        with self.voiceover(
            "One last instrument that works by a jet: the organ. An organ pipe is a flute with its lips "
            "built in, and since it cannot be fingered, an organ has one pipe for every note. And then, "
            "since the fifteenth century, more than one. <bookmark mark='a'/> Each stop on an organ switches "
            "on another whole rank of pipes. The basic rank is called eight foot, after the length of its "
            "lowest pipe. A four foot rank has pipes half as long and sounds an octave higher: the second "
            "harmonic. Two and two thirds feet: the third harmonic. Two feet, the fourth. One and three "
            "fifths, the fifth. <bookmark mark='b'/> An organist who draws those stops is not adding notes. "
            "She is adding partials, one pipe for each, and building a tone colour by hand. It is the "
            "additive synthesis of Part 3, four hundred years before the computer. Hold down one key, and "
            "draw the stops one at a time."
        ) as vo:
            self.play(FadeIn(knobs))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in pipes], lag_ratio=0.5), FadeIn(cap), run_time=10.0)
            vo.wait_until("b")
            self.play(FadeIn(note))
        with self.listen(c) as snd:
            window(snd, r"one note, \ five stops", detail=r"model organ pipes", corner=UL, tag_corner=UR)
            for k, (kn, pp) in enumerate(zip(knobs, pipes)):
                t0 = snd.time_of(f"stop{k}")
                snd.wait_until(f"stop{k}")
                self.play(kn[0].animate.set_stroke(TUNE, 5), pp[0].animate.set_fill(opacity=0.6), run_time=0.3)
        with self.voiceover(
            "By the end there were five pipes sounding, each a plain, flute-like tone, and what you heard "
            "was one note that had become bright and reedy. The ear did what Part 4 said it does: it took "
            "partials that fit one harmonic series and fused them into a single sound."
        ):
            self.play(FadeOut(note))
        self.wait(0.3)
        self.clear_scene()
