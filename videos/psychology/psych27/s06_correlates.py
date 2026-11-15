from __future__ import annotations

from videos.psychology.psych27.common import *  # noqa: F403


def grating(center, angle, col, size=1.6, n=7):
    sq = Square(side_length=size, stroke_color=col, stroke_width=2).move_to(center)
    lines = VGroup()
    for k in np.linspace(-0.42, 0.42, n):
        l = Line(LEFT * size * 0.45, RIGHT * size * 0.45, color=col, stroke_width=6).shift(UP * k * size)
        lines.add(l)
    lines.rotate(angle).move_to(center)
    return VGroup(sq, lines)


class Correlates(VoiceoverScene):
    def construct(self):
        self.card()
        self.on_you()
        self.model()
        self.neurons()
        self.no_report()

    def card(self):
        card = chapter_card(5, r"Correlates: \ rivalry, \ report and no-report", r"Where in the brain does an "
                            r"experience happen?", lit={1965: r"Levelt", 1996: r"Leopold \& Logothetis",
                                                        1998: r"Tong et al.", 2014: r"Frässle et al."},
                            part=PART, scale=("mind", "brain"), marr=("how",))
        with self.voiceover("Chapter five. Correlates: rivalry, report and no-report."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def on_you(self):
        stage = demo_stage(12.4, 5.4, center=[0, 0.35, 0])
        g1 = grating([-1.6, 0.6, 0], PI / 4, LOST)
        g2 = grating([1.6, 0.6, 0], -PI / 4, SEEN)
        ask = rows_of([
            (r"cross your eyes slowly until the two squares overlap into three; \ watch the middle one", YOU),
            (r"or, \ with red--cyan glasses, \ look at the pair through them", GREY_A),
        ], 11.0, 24, 0.2).move_to([0, -1.6, 0])
        with self.voiceover(
            "This one is on you, if your eyes cooperate. <bookmark mark='a'/> Here are two gratings, one tilted "
            "each way. Cross your eyes slowly, as if looking at a point in front of the screen, until the two "
            "squares become three, and watch the middle one. If you have red and cyan glasses, you can look through "
            "them instead. <bookmark mark='b'/> In the middle, each eye sees a different grating. You don't see a "
            "mesh. You see one tilt for a few seconds, then the other, then a patchwork in transition, then the first "
            "again, though nothing on the screen changes. That alternation is binocular rivalry."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(g1), FadeIn(g2))
            vo.wait_until("a")
            self.play(FadeIn(ask))
            vo.wait_until("b")
        self.wait(6.0)
        self.clear_scene()

    def model(self):
        d = load("rivalry")
        head = heading(r"Rivalry from inhibition and adaptation")
        A = axes([0, 40], [0, 1], x_length=6.2, y_length=2.0, xticks=[0, 10, 20, 30, 40], yticks=[0, 1],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"time, \ s",
                 ylabel=r"activity, \ each eye's population", center=[-3.0, 1.2, 0], font_size=16)
        c1 = curve(A.ax, d["t"], d["u1"], LOST, 3)
        c2 = curve(A.ax, d["t"], d["u2"], SEEN, 3)
        B = axes([0, 12], [0, 0.35], x_length=5.0, y_length=2.2, xticks=[0, 4, 8, 12], yticks=[0, 0.1, 0.2, 0.3],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", xlabel=r"dominance duration, \ s",
                 ylabel=r"density", center=[-3.5, -2.0, 0], font_size=16)
        e = d["edges"]
        hb = bars(B.ax, (e[:-1] + e[1:]) / 2, d["hist"], MODEL, width=float(e[1] - e[0]) * 0.9, opacity=0.7)
        gp = curve(B.ax, d["x"], d["gamma_pdf"], WHITE, 3)
        eq, rs = d["equal_means"], d["raised_means"]
        rows = rows_of([
            (r"Psyche: \ two populations, \ one per eye, \ inhibit each other; \ the winner slowly tires \ "
             r"(adaptation) \ and slow noise tips the balance", MODEL),
            (rf"{d['n']} dominance periods: \ mean {d['mean']:.1f} s, \ skewed, \ a gamma with shape "
             rf"{d['shape']:.1f}, \ as in people", WHITE),
            (rf"raise one eye's contrast: \ its periods {eq[0]:.1f} to {rs[0]:.1f} s, \ the other eye's "
             rf"{eq[1]:.1f} to {rs[1]:.1f} s", GNW),
            (r"Levelt, \ 1965: \ stronger input changes dominance; \ later work found the stronger eye's periods "
             r"change most", GREY_A),
        ], 5.4, 21, 0.3).move_to([3.6, -0.1, 0])
        tag = psyche_tag(r"\texttt{workspace.rivalry}, \ \texttt{dominance\_durations}: \ 600 s simulated")
        with self.voiceover(
            "A simple circuit produces rivalry. <bookmark mark='a'/> Give each eye's image a population of neurons "
            "that inhibits the other's. Whichever is ahead suppresses its rival, but it slowly tires, and slow noise "
            "does the rest, so control passes back and forth. <bookmark mark='b'/> Over ten simulated minutes, "
            f"Psyche's percept switched {d['n']} times. Periods of dominance averaged {d['mean']:.1f} seconds and "
            f"were skewed, close to a gamma distribution with shape {d['shape']:.1f}, which is what people's "
            "durations look like. <bookmark mark='c'/> Raise the contrast in one eye, and the durations change: "
            f"that eye's periods lengthen from {eq[0]:.1f} to {rs[0]:.1f} seconds, the other's shorten from "
            f"{eq[1]:.1f} to {rs[1]:.1f}. <bookmark mark='d'/> Willem Levelt mapped such laws in 1965, and later "
            "work refined them. The point for us is that the stimulus is fixed while the experience alternates, "
            "so we can ask which neurons alternate with it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(Create(c1), Create(c2), FadeIn(rows[0]), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(B), FadeIn(hb), Create(gp), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def neurons(self):
        head = heading(r"Which neurons follow the percept?")
        levels = VGroup()
        for name, frac, col in [(r"V1", 0.2, UNSEEN), (r"V4", 0.4, SEEN), (r"inferotemporal", 0.9, GNW)]:
            bar_bg = Rectangle(width=4.0, height=0.45, stroke_color=GREY_C, stroke_width=1.5)
            fill = Rectangle(width=4.0 * frac, height=0.45, stroke_width=0, fill_color=col, fill_opacity=0.85)
            fill.align_to(bar_bg, LEFT)
            levels.add(VGroup(label(name, font_size=22, color=col),
                              VGroup(bar_bg, fill)).arrange(RIGHT, buff=0.3))
        for lv in levels:
            lv[1].shift(RIGHT * (2.4 - lv[0].width))
        levels.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([-3.2, 0.6, 0])
        cap = label(r"share of cells that follow the percept \ (schematic)", font_size=18, color=GREY_B).next_to(
            levels, DOWN, buff=0.25)
        rows = rows_of([
            (r"Leopold and Logothetis, \ 1996; \ Sheinberg and Logothetis, \ 1997: \ monkeys report rivalry; \ "
             r"few cells in early areas follow the percept, \ most in inferotemporal cortex do", WHITE),
            (r"Tong and colleagues, \ 1998: \ a face in one eye, \ a house in the other; \ the face area and place "
             r"area in people rise and fall with the percept", GNW),
            (r"activity follows experience more, \ the further along the visual stream", MODEL),
        ], 5.8, 22, 0.32).move_to([3.4, 0.0, 0])
        tag = published_tag(r"Leopold \& Logothetis (1996); \ Tong et al.\ (1998)")
        with self.voiceover(
            "Monkeys can be trained to report rivalry with a lever. <bookmark mark='a'/> When David Leopold and "
            "Nikos Logothetis, and then David Sheinberg and Logothetis, recorded from them in the 1990s, few cells "
            "in early visual cortex changed their firing with the reported percept, more did in V4, and most did "
            "in inferotemporal cortex, near the end of the visual stream. <bookmark mark='b'/> In people, Frank Tong "
            "and colleagues showed a face to one eye and a house to the other, and found the brain's face area and "
            "place area rising and falling with whichever was seen. <bookmark mark='c'/> Activity follows experience "
            "more and more closely the further along the visual stream you go."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(l_) for l_ in levels], lag_ratio=0.5), FadeIn(cap), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def no_report(self):
        head = heading(r"Report, \ or experience?")
        left = VGroup(label(r"with report", font_size=26, color=HOT),
                      wrapped_label(r"people press a key at each switch: \ frontal and parietal areas light up with "
                                    r"the switches", 4.8, 22, WHITE)).arrange(DOWN, buff=0.25)
        right = VGroup(label(r"without report", font_size=26, color=SEEN),
                       wrapped_label(r"the switch is read from the eyes' reflexes instead: \ much of the frontal "
                                     r"activity disappears", 4.8, 22, WHITE)).arrange(DOWN, buff=0.25)
        VGroup(left, right).arrange(RIGHT, buff=1.4, aligned_edge=UP).move_to([0, 1.3, 0])
        rows = rows_of([
            (r"Frässle and colleagues, \ 2014: \ in rivalry between moving gratings, \ the eyes' slow-following "
             r"movements reveal each switch with no key to press", WHITE),
            (r"Tsuchiya and colleagues, \ 2015: \ the no-report paradigm, \ separating experience from what is done "
             r"to report it", MODEL),
            (r"the front-or-back question: \ is the prefrontal cortex needed for experience, \ or only for report? "
             r"\ the workspace says front; \ integrated information says the back", GNW),
        ], 12.0, 23, 0.32).move_to([0, -1.5, 0])
        tag = published_tag(r"Frässle et al.\ (2014); \ Tsuchiya et al.\ (2015)")
        with self.voiceover(
            "But there's a confound in every one of these studies. People, and monkeys, report what they see, and "
            "reporting is itself something the brain does. <bookmark mark='a'/> When people press a key at every "
            "switch of rivalry, frontal and parietal areas light up with the switches. <bookmark mark='b'/> In 2014 "
            "Stefan Frässle and colleagues used rivalry between gratings moving in opposite directions, so that the "
            "eyes' reflexive following movements revealed each switch without anyone pressing anything. Much of the "
            "frontal activity disappeared. <bookmark mark='c'/> Naotsugu Tsuchiya and colleagues called this the "
            "no-report paradigm: separating the experience from what's done to report it. <bookmark mark='d'/> And "
            "it sharpens the central dispute of the field: is the front of the brain needed for experience, or only "
            "for reporting it? The two leading theories answer differently."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
