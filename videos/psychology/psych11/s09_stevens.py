from __future__ import annotations

import numpy as np

from videos.psychology.psych11.common import *  # noqa: F403


class Stevens(VoiceoverScene):
    def construct(self):
        self.card()
        self.ask()
        self.lines()
        self.table()
        self.matching()

    def card(self):
        card = chapter_card(8, r"Stevens asks for numbers", r"Why count steps, \ when you could just ask?",
                            lit={1957: r"Stevens's power law"}, part=PART, scale=("mind",), marr=("what",))
        with self.voiceover(
            "Chapter eight. Stevens asks for numbers."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def ask(self):
        head = heading(r"Magnitude estimation")
        rows = VGroup()
        demo = [(r"a light", r"``call this one 10''", GREY_A), (r"a brighter light", r"``20''", YOU),
                (r"a much brighter one", r"``45''", YOU), (r"a dim one", r"``4''", YOU)]
        for i, (stim, said, col) in enumerate(demo):
            y = 1.7 - 1.05 * i
            lamp = Circle(radius=0.32, stroke_width=0, fill_color=WHITE, fill_opacity=[0.45, 0.65, 0.95, 0.2][i]).move_to([-4.8, y, 0])
            rows.add(VGroup(lamp, label(stim, font_size=30, color=WHITE).next_to(lamp, RIGHT, buff=0.4),
                            label(said, font_size=34, color=col).move_to([0.2, y, 0])))
        side = rows_of([
            (r"S. S. Stevens, Harvard, \ the 1950s", STEVC),
            (r"no steps counted: \ people say a number for how strong each stimulus seems", WHITE),
            (r"the numbers are free, \ but they keep their ratios: \ twice as bright, \ twice the number", THRESH),
        ], 3.9, 28, 0.3).move_to([4.85, 0.3, 0])
        keep_in_frame(side)
        src = published_tag(archive.STEVENS_1957.cite)
        tag = note(r"an illustration of the procedure").to_corner(DR, buff=0.3)
        with self.voiceover(
            "A century after Fechner, the Harvard psychologist S. S. Stevens, the Stevens of Part 3's "
            "scales of measurement, decided that counting steps was the long way round. Why not just ask? "
            "<bookmark mark='a'/> Show a light and say: call this one ten. Then show others, and for each "
            "one the observer says a number for how bright it seems. Twenty. Forty-five. Four. "
            "<bookmark mark='b'/> The method is called magnitude estimation. The numbers are free, but "
            "people use them as if their ratios meant something: twice as bright, twice the number."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(side[0]), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[1:]], lag_ratio=0.7), FadeIn(side[1]), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def lines(self):
        d = load("stevens")
        head = heading(r"On log-log axes, \ straight lines")
        A = axes([0, 1], [0.5, 5], x_length=6.4, y_length=4.4, xticks=[0, 0.5, 1], yticks=[1, 2, 3, 4, 5],
                 xfmt=lambda v: {0: "1", 0.5: r"\sqrt{10}", 1: "10"}[v], yfmt=lambda v: f"10^{{{int(v)}}}",
                 xlabel=r"stimulus intensity (log scale)", ylabel=r"the number people say (log scale)", center=[-3.0, -0.4, 0])
        ax = A.ax
        sets = [("brightness", WEBERC, r"brightness"), ("heaviness", MODEL, r"heaviness"), ("shock", STEVC, r"electric shock")]
        groups = VGroup()
        for key, col, name in sets:
            lx, ly = np.log10(d[f"{key}_i"]), np.log10(d[f"{key}_geo"])
            dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.08, color=col) for a, b in zip(lx, ly)])
            slope, icpt = np.polyfit(lx, ly, 1)
            fit = Line(ax.c2p(0, icpt), ax.c2p(1, icpt + slope), color=col, stroke_width=3)
            lab = label(rf"{name}: \ ${d[key + '_fit']:.2f}$", font_size=27, color=col).next_to(ax.c2p(1, icpt + slope), RIGHT, buff=0.15)
            groups.add(VGroup(dots, fit, lab))
        eq = VGroup(MathTex(r"S = c\,I^{\,a}", font_size=40, color=STEVC),
                    MathTex(r"\log S = \log c + a \log I", font_size=34, color=STEVC)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        rows = rows_of([
            (r"a power law: \ the slope on log-log axes is the exponent $a$", STEVC),
            (r"brightness: \ below 1, \ compressed; \ heaviness: \ a little above 1; \ shock: \ steeply expanded", WHITE),
        ], 3.4, 27, 0.3)
        VGroup(eq, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([5.0, 0.0, 0])
        keep_in_frame(VGroup(eq, rows))
        tag = psyche_tag(r"simulated: 20 people per continuum, \ geometric means")
        with self.voiceover(
            "Plot the numbers people say against the intensity, both on logarithmic scales. Here are "
            "simulated people, with the exponents Stevens reported built in. <bookmark mark='a'/> Each "
            "continuum gives a straight line. A straight line on log-log axes is a power law: sensation is "
            "a constant times intensity to some power a, and the slope of the line is a. "
            "<bookmark mark='b'/> For brightness the slope is about a third: doubling the light makes it "
            "seem only about a quarter brighter. For heaviness it's a little above one. And for electric "
            "shock it's three and a half: double the current, and it feels about eleven times as strong."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(g) for g in groups], lag_ratio=0.6), Write(eq), FadeIn(rows[0]), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def table(self):
        d = load("stevens")
        head = heading(r"Stevens's table of exponents")
        names = [r"brightness", r"loudness", r"vibration", r"visual length", r"heaviness", r"electric shock"]
        stim = [r"a 5\textdegree\ target in the dark", r"a 3{,}000 Hz tone", r"60 Hz on a finger", r"a projected line",
                r"lifted weights", r"current through the fingers"]
        rows = VGroup()
        unit = 1.4
        for i, (n_, s_, a) in enumerate(zip(names, stim, d["exponents"])):
            y = 2.1 - 0.78 * i
            col = WEBERC if a < 1 else (GREY_A if a == 1 else STEVC)
            rows.add(VGroup(label(n_, font_size=31, color=WHITE).move_to([-5.2, y, 0]),
                            label(s_, font_size=25, color=GREY_A).move_to([-2.0, y, 0]),
                            Rectangle(width=a * unit, height=0.4, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                                [0.6, y, 0], aligned_edge=LEFT),
                            label(rf"${a:g}$", font_size=30, color=col).move_to([0.6 + a * unit + 0.45, y, 0])))
        one = DashedLine([0.6 + unit, 2.5, 0], [0.6 + unit, -2.3, 0], color=GREY_C, stroke_width=2)
        ol = label(r"exponent 1: \ proportional", font_size=24, color=GREY_A).next_to(one, DOWN, buff=0.1)
        end = wrapped_label(r"Below 1, \ a sense compresses a huge range; \ above 1, \ it magnifies a small one.", 6.8, 28,
                            THRESH).move_to([3.0, -3.0, 0])
        src = published_tag(archive.STEVENS_1957.cite)
        with self.voiceover(
            "Stevens and his colleagues did this for dozens of continua, and published a table of "
            "exponents. Here are six of them. <bookmark mark='a'/> Brightness, a third. Loudness, two "
            "thirds. Vibration on a finger, nearly one. The length of a line, exactly one: a line twice as "
            "long looks twice as long. Heaviness, one and a half. Electric shock, three and a half. "
            "<bookmark mark='b'/> There's a pattern. Senses that must cover enormous ranges, like light "
            "and sound, compress them. A sense like shock, where a small range matters a great deal, "
            "magnifies it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(one), FadeIn(ol), *[FadeIn(VGroup(r[0], r[1])) for r in rows])
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(r[2], LEFT), FadeIn(r[3])) for r in rows], lag_ratio=0.8),
                      run_time=10.0)
            vo.wait_until("b")
            self.play(FadeIn(end))
        self.clear_scene()

    def matching(self):
        d = load("stevens")
        a = d["match_brightness_loudness"]
        head = heading(r"A check with no numbers: \ cross-modality matching")
        lamp = Circle(radius=0.6, stroke_width=0, fill_color=WHITE, fill_opacity=0.7).move_to([-4.4, 1.3, 0])
        knob = VGroup(Circle(radius=0.5, color=GREY_B, stroke_width=4), Line(ORIGIN, UP * 0.45, color=GREY_B, stroke_width=4))
        knob.move_to([-1.6, 1.3, 0])
        sound = VGroup(*[Arc(radius=r, start_angle=-PI / 4, angle=PI / 2, color=GREY_B, stroke_width=4) for r in (0.3, 0.55, 0.8)])
        sound.next_to(knob, RIGHT, buff=0.3)
        cap = label(r"make the tone as loud as the light is bright", font_size=29, color=WHITE).move_to([-2.9, 0.1, 0])
        steps = VGroup(
            MathTex(r"S_{\text{light}} = c_1\,L^{0.33}", font_size=36, color=WEBERC),
            MathTex(r"S_{\text{tone}} = c_2\,P^{0.67}", font_size=36, color=STEVC),
            MathTex(r"S_{\text{tone}} = S_{\text{light}} \;\Rightarrow\; P \propto L^{0.33/0.67} = L^{%.2f}" % a, font_size=36,
                    color=THRESH),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.6, 1.1, 0])
        keep_in_frame(steps)
        rows = rows_of([
            (r"the prediction comes from two magnitude-estimation exponents, \ and is tested without any numbers at all", WHITE),
            (r"Stevens's laboratory found matches of this kind close to the predicted exponents: \ the scales hang together", MODEL),
            (r"that is evidence the numbers measure something consistent. \ Whether it is sensation is chapter 14's question", GREY_A),
        ], 12.6, 29, 0.25).to_edge(DOWN, buff=0.6)
        src = published_tag(archive.STEVENS_1957.cite)
        with self.voiceover(
            "Is anything real behind those numbers? Stevens had a check that uses no numbers at all. "
            "<bookmark mark='a'/> Show a light, and have the observer turn a knob until a tone is as loud "
            "as the light is bright. <bookmark mark='b'/> If brightness goes as light to the power a "
            "third, and loudness as sound pressure to the power two thirds, then matching them predicts "
            f"that the sound pressure chosen will go as the light to the power {a:.2f}. "
            "<bookmark mark='c'/> A prediction from two sets of numbers, tested without any numbers. "
            "Stevens's laboratory reported matches close to such predictions. That's evidence the numbers "
            "measure something consistent. Whether that something is sensation is a question for the "
            "frontier chapter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(lamp), FadeIn(knob), FadeIn(sound), FadeIn(cap))
            vo.wait_until("a")
            self.play(Rotate(knob, angle=-PI / 3), run_time=1.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_, shift=RIGHT * 0.15) for s_ in steps], lag_ratio=0.8), run_time=5.0)
            vo.wait_until("c")
            self.play(FadeIn(rows, lag_ratio=0.5), run_time=3.0)
        self.clear_scene()
