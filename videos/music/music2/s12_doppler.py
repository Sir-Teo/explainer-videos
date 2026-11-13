from __future__ import annotations

import numpy as np

from videos.music.music2.common import *  # noqa: F403


class Doppler(SoundScene):
    def construct(self):
        chapter(self, 11, r"A source that moves", r"Why does the pitch drop as it passes?", lit=(1842,),
                extra=((1845, r"Buys Ballot's trumpeters on a train"),))
        self.fronts()
        self.train()
        self.quiz()

    def graph(self, d, names, width=6.4, height=3.0):
        g = axes([-3, 3], [350, 432], x_length=width, y_length=height, xlabel=r"seconds from the moment it is abreast",
                 ylabel=r"the pitch you hear (Hz)", xticks=[-3, -2, -1, 0, 1, 2, 3], yticks=[360, 380, 400, 420], font_size=20)
        ts = np.linspace(-3, 3, 600)
        cs = {}
        for name, col in names:
            cs[name] = curve(g.ax, ts, d["curves"][name]["heard"], col, stroke_width=3)
        true = DashedLine(g.ax.c2p(-3, d["hz"]), g.ax.c2p(3, d["hz"]), color=GREY_C, stroke_width=1.5)
        return g, cs, true

    # ------------------------------------------------------------------
    def fronts(self):
        d = load("doppler")
        fv = FieldView(d["frames"], d["extent"], width=7.2).move_to(LEFT * 3.0 + DOWN * 0.2)
        cap = label(rf"a source crossing the picture at {d['mach']:.1f} of the speed of sound", font_size=24, color=GREY_B).next_to(fv, DOWN, buff=0.15)
        law = VGroup(MathTex(r"\lambda_{\text{ahead}}", r"=", r"\frac{c - v}{f}", font_size=40),
                     label(r"between crests the sound goes $c/f$, \\ and the source follows it by $v/f$", font_size=22, color=GREY_A),
                     MathTex(r"f_{\text{heard}}", r"=", r"\frac{c}{\lambda_{\text{ahead}}}", r"=", r"f\,\frac{c}{c - v}", font_size=40),
                     label(r"coming straight at you", font_size=22, color=GREY_A),
                     MathTex(r"f_{\text{heard}}", r"=", r"f\,\frac{c}{c + v}", font_size=40),
                     label(r"going straight away", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.18)
        law[2:].shift(DOWN * 0.2)
        law[4:].shift(DOWN * 0.2)
        law.move_to(RIGHT * 4.4 + UP * 0.1)
        law[0][0].set_color(RATIO), law[2][4].set_color(TUNE), law[4][2].set_color(TUNE)
        with self.voiceover(
            "One last thing wavelength explains. Let the source move. <bookmark mark='a'/> Each crest spreads out in "
            "a circle from where the source was when it made it. So ahead of the source the crests are crowded "
            "together, and behind it they are stretched apart. <bookmark mark='b'/> By how much? Between one crest "
            "and the next, the sound travels the speed of sound divided by the frequency, and the source follows it "
            "by its own speed divided by the frequency. The gap between crests is the difference. "
            "<bookmark mark='c'/> Crowded crests arrive more often, so the pitch you hear is the speed of sound "
            "over that shorter gap. <bookmark mark='d'/> Behind the source the sign changes, and the pitch is lower. "
            "The source itself has not changed its note at all. Christian Doppler worked this out in 1842."
        ) as vo:
            self.play(FadeIn(fv), FadeIn(cap))
            fv.start((len(d["frames"]) - 1) / max(vo.remaining() - 0.5, 8.0))
            vo.wait_until("b")
            self.play(FadeIn(law[0]), FadeIn(law[1]))
            vo.wait_until("c")
            self.play(FadeIn(law[2]), FadeIn(law[3]))
            vo.wait_until("d")
            self.play(FadeIn(law[4]), FadeIn(law[5]))
            self.wait(vo.remaining() + 0.1)
        fv.stop()
        self.wait(0.2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def train(self):
        d = load("doppler")
        c = clip("doppler.pass")
        tr = d["curves"]["train"]
        card = history_card(1845, r"Christoph Buys Ballot, \ Utrecht",
                            r"trumpeters on an open wagon behind a locomotive on the line to Maarssen; musicians by the "
                            r"track judged the note about a semitone high coming, a semitone low going", width=5.8)
        card.to_corner(UL, buff=0.4)
        g, cs, true = self.graph(d, [("train", TUNE)])
        VGroup(g, cs["train"], true).move_to(RIGHT * 3.2 + UP * 1.4)       # the curves move with their axes
        # the experiment, drawn: a wagon with a trumpeter, a listener by the track
        track = Line([-0.4, 0.2, 0], [6.6, 0.2, 0], color=GREY_C, stroke_width=3)
        wagon = VGroup(Rectangle(width=1.3, height=0.45, stroke_color=GREY_A, stroke_width=2, fill_color="#5B4636", fill_opacity=0.9),
                       Circle(radius=0.13, color=GREY_A, stroke_width=2).shift(LEFT * 0.4 + DOWN * 0.33),
                       Circle(radius=0.13, color=GREY_A, stroke_width=2).shift(RIGHT * 0.4 + DOWN * 0.33),
                       Polygon([-0.1, 0.3, 0], [0.45, 0.42, 0], [0.45, 0.62, 0], [-0.1, 0.5, 0], stroke_width=0, fill_color=TUNE, fill_opacity=1))
        wagon.move_to([0.4, 0.65, 0])
        ear = VGroup(Dot([3.1, -0.5, 0], radius=0.13, color=EAR), label(r"listeners", font_size=22, color=EAR).move_to([3.1, -0.9, 0]))
        hi = label(r"coming: \ higher", font_size=26, color=RATIO).move_to([1.2, 1.7, 0])
        lo = label(r"going: \ lower", font_size=26, color=AIR).move_to([5.2, 1.7, 0])
        drawing = VGroup(track, wagon, ear, hi, lo)
        facts = VGroup(label(rf"a semitone up and a semitone down needs {tr['kmh']:.0f} km/h", font_size=28, color=TUNE),
                       label(rf"coming: \ {tr['up']:.0f} Hz \quad going: \ {tr['down']:.0f} Hz \quad true: \ {d['hz']:.0f} Hz", font_size=26, color=GREY_A)
                       ).arrange(DOWN, buff=0.2).move_to(DOWN * 1.2 + RIGHT * 0.8)
        head = Line(g.ax.c2p(-3, 350), g.ax.c2p(-3, 432), color=WHITE, stroke_width=2)
        meter = Meter(width=0.45, height=1.8).move_to(LEFT * 5.6 + DOWN * 2.2)
        mtag = label(r"loudness", font_size=22, color=GREY_B).next_to(meter, RIGHT, buff=0.2)
        with self.voiceover(
            "It was tested three years later in Holland, in the only way available. Christoph Buys Ballot put "
            "trumpeters on an open railway wagon, stood musicians beside the track, and had the players hold one "
            "note as the train went by. <bookmark mark='a'/> The listeners judged it about a semitone sharp as it "
            f"came and a semitone flat as it went. For that, the formula needs {say(tr['kmh'])} kilometres an hour, "
            "which is about what a locomotive of 1845 could do. <bookmark mark='b'/> Here is a horn passing six "
            "metres away at that speed."
        ) as vo:
            self.play(FadeIn(card), FadeIn(track), FadeIn(wagon), FadeIn(ear))
            self.play(FadeIn(hi), run_time=0.4)
            self.play(wagon.animate.shift(RIGHT * 5.4), run_time=max(vo.until("a") - 1.2, 4.0), rate_func=linear)
            self.play(FadeIn(lo), run_time=0.4)
            vo.wait_until("a")
            self.play(FadeOut(drawing), run_time=0.3)
            self.play(FadeIn(g), Create(cs["train"]), FadeIn(true), FadeIn(facts))
            vo.wait_until("b")
            self.play(FadeIn(meter), FadeIn(mtag))
        with self.listen(c) as snd:
            window(snd, r"a horn passing at the speed of Buys Ballot's train", kind="synthesized", detail=r"passing at 6 metres",
                   corner=DR, tag_corner=UR)
            snd.show(head)
            snd.drive(head, lambda m, t: m.set_x(g.ax.c2p(min(t, 6.0) - 3.0, 0)[0]))
            snd.drive(meter, meter.follow(tr["env"]))
        with self.voiceover(
            "The pitch does not jump. It slides, because what matters is how fast the source is closing on you, and "
            "that changes smoothly as it goes by. <bookmark mark='a'/> You hear its true note at one instant only: "
            "just after it is level with you."
        ) as vo:
            vo.wait_until("a")
            dot = Dot(g.ax.c2p(d["closest"] / C, d["hz"]), radius=0.09, color=GOOD)
            self.play(FadeIn(dot), Flash(dot, color=GOOD))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("doppler")
        c = clip("doppler.quiz")
        q = listen_card(r"Two cars pass, \ A and B, \ sounding the same horn. \\ One is doing 50 kilometres an hour, \ "
                        r"the other 100. \ Which is the fast one?", width=10.0).to_edge(UP, buff=0.6)
        boxes = VGroup(*[VGroup(RoundedRectangle(width=2.6, height=1.4, corner_radius=0.15, stroke_color=GREY_C, stroke_width=2),
                                label(t, font_size=60, color=GREY_A)) for t in ("A", "B")]).arrange(RIGHT, buff=3.0).shift(UP * 0.2)
        with self.voiceover("A question for your ears. Two cars pass you, sounding the same horn. One is doing fifty "
                            "kilometres an hour, the other a hundred. Which is the fast one?"):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(boxes))
        env = {"A": d["curves"]["fast"]["env"][120:480], "B": d["curves"]["slow"]["env"][120:480]}
        with self.listen(c) as snd:
            window(snd, r"car A, \ then car B", kind="synthesized", tag_corner=DR)
            for key, box, end in (("A", boxes[0], snd.time_of("B")), ("B", boxes[1], c.duration)):
                t0 = snd.time_of(key)
                snd.wait_until(t0)
                box[1].set_color(EAR)
                glow = box[0].copy().set_stroke(EAR, width=5)
                snd.show(glow)
                f = follow(env[key], 100.0, t0)
                snd.drive(glow, lambda m, t, f=f, end=end: m.set_stroke(opacity=f(t) if t < end else 0.0))
                snd.wait_until(end - 0.35)
                box[1].set_color(GREY_A)
        fast, slow = d["curves"]["fast"], d["curves"]["slow"]
        ans = VGroup(label(rf"{fast['kmh']:.0f} km/h: \ a drop of {fast['cents'] / 100:.1f} semitones", font_size=26, color=GOOD).next_to(boxes[0], DOWN, buff=0.35),
                     label(rf"{slow['kmh']:.0f} km/h: \ a drop of {slow['cents'] / 100:.1f} semitones", font_size=26, color=GREY_A).next_to(boxes[1], DOWN, buff=0.35))
        uses = label(r"the same shift measures the speed of a car (radar), \ of blood in an artery (ultrasound), \ and of a galaxy",
                     font_size=24, color=GREY_B).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            f"{d['quiz_answer']}. Its horn fell by nearly three semitones; the slow one's by less than one and a "
            "half. <bookmark mark='a'/> Your ear measured a speed. Police radar measures a car's speed the same way, "
            "ultrasound measures the speed of blood, and astronomers measure the speed of galaxies. In music the "
            "effect is built into one famous instrument: the rotating loudspeaker of an electric organ, which we "
            "will meet in Part 53."
        ) as vo:
            self.play(FadeIn(ans), boxes[0][0].animate.set_stroke(GOOD, width=4))
            vo.wait_until("a")
            self.play(FadeIn(uses))
        self.wait(0.3)
        self.clear_scene()
