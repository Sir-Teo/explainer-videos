from __future__ import annotations

from videos.psychology.psych27.common import *  # noqa: F403


class Volition(VoiceoverScene):
    def construct(self):
        self.card()
        self.libet()
        self.noise()
        self.average()
        self.after()

    def card(self):
        card = chapter_card(10, r"Volition: \ Libet's clock", r"Does the brain decide before you do?",
                            lit={1965: r"Kornhuber \& Deecke", 1983: r"Libet et al.", 2008: r"Soon et al.",
                                 2012: r"Schurger, \ Sitt \& Dehaene"},
                            part=PART, scale=("mind", "brain"), marr=("how",))
        with self.voiceover("Chapter ten. Volition: Libet's clock."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def libet(self):
        head = heading(r"Libet's experiment")
        clock = Circle(radius=1.4, color=GREY_B, stroke_width=3).move_to([-4.0, 0.6, 0])
        ticks = VGroup(*[Line(clock.get_center() + 1.25 * np.array([np.cos(a), np.sin(a), 0]),
                              clock.get_center() + 1.4 * np.array([np.cos(a), np.sin(a), 0]), color=GREY_B)
                         for a in np.linspace(0, 2 * PI, 13)[:-1]])
        spot = Dot(clock.get_center() + 1.1 * UP, color=GNW, radius=0.09)
        line = NumberLine(x_range=[-1.2, 0.2, 0.2], length=6.6, include_numbers=False, color=GREY_C).move_to(
            [2.6, 1.6, 0])
        nums = VGroup(*[label(f"{v:+.1f}" if v != 0 else "0", font_size=16, color=GREY_B).next_to(
            line.n2p(v), DOWN, buff=0.12) for v in (-1.0, -0.6, -0.2, 0.2)])
        marks = VGroup()
        for v, txt, col in [(-0.55, r"readiness potential begins", RPT), (-0.2, r"W: \ the felt urge", GNW),
                            (0.0, r"movement", WHITE)]:
            tick = Line(line.n2p(v) + DOWN * 0.18, line.n2p(v) + UP * 0.18, color=col, stroke_width=5)
            marks.add(VGroup(tick, label(txt, font_size=18, color=col).next_to(tick, UP, buff=0.1)))
        marks[0][1].shift(LEFT * 0.4)
        sec = label(r"seconds from the movement", font_size=18, color=GREY_B).next_to(nums, DOWN, buff=0.15)
        rows = rows_of([
            (r"Kornhuber and Deecke, \ 1965: \ a slow negative ramp over motor areas before a voluntary movement, \ "
             r"the readiness potential", WHITE),
            (r"Libet and colleagues, \ 1983: \ move whenever you like, \ and note where a spot on a fast clock was "
             r"when you first felt the urge", GNW),
            (r"the urge: \ about 200 ms before the movement; \ the ramp: \ about 550 ms before, \ or earlier", RPT),
            (r"the brain, \ it seemed, \ had started before the person decided", LOST),
        ], 6.4, 22, 0.3).move_to([3.0, -1.5, 0])
        tag = published_tag(r"Kornhuber \& Deecke (1965); \ Libet, \ Gleason, \ Wright \& Pearl (1983)")
        with self.voiceover(
            "Consciousness also seems to be where we decide. One experiment made that doubtful. "
            "<bookmark mark='a'/> In 1965 Hans Kornhuber and Lüder Deecke found a slow negative ramp in the EEG over "
            "motor areas, starting a second or more before a voluntary movement. They called it the readiness "
            "potential. <bookmark mark='b'/> In 1983 Benjamin Libet and colleagues asked people to flex their wrist "
            "whenever they felt like it, while watching a spot circle a clock face every two and a half seconds, and "
            "to report where the spot was when they first felt the urge to move. <bookmark mark='c'/> The felt urge "
            "came about two hundred milliseconds before the movement. The ramp began about five hundred and fifty "
            "milliseconds before, or earlier. <bookmark mark='d'/> The brain, it seemed, had started before the "
            "person decided."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(clock), FadeIn(ticks), FadeIn(spot))
            self.play(Rotate(spot, angle=-2 * PI, about_point=clock.get_center()), run_time=2.5, rate_func=linear)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(line), FadeIn(nums), FadeIn(sec))
            vo.wait_until("c")
            self.play(FadeIn(marks), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def noise(self):
        d = load("libet")
        head = heading(r"Schurger's accumulator")
        A = axes([0, 30], [-0.1, 0.35], x_length=12.0, y_length=2.6, xticks=[0, 10, 20, 30], yticks=[0, 0.3],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", xlabel=r"time, \ s",
                 ylabel=r"accumulated activity", center=[0, 1.1, 0], font_size=16)
        tr = curve(A.ax, d["t"], d["x"], RPT, 2)
        thr = DashedLine(A.ax.c2p(0, d["threshold"]), A.ax.c2p(30, d["threshold"]), color=GNW, stroke_width=2)
        hits = VGroup(*[Triangle(color=WHITE, fill_opacity=1).scale(0.08).rotate(PI).move_to(
            A.ax.c2p(h, d["threshold"] + 0.03)) for h in d["hits"]])
        rows = rows_of([
            (r"Schurger, \ Sitt and Dehaene, \ 2012: \ when no reason favours one moment over another, \ spontaneous "
             r"neural fluctuations, \ slowly accumulated, \ decide when", WHITE),
            (r"Psyche: \ a leaky accumulator of noise with a small drift; \ when it crosses the threshold, \ the "
             r"movement starts", MODEL),
            (rf"the waits between movements: \ a median of {d['median_wait']:.1f} s, \ like people told to move "
             r"whenever they like", GREY_A),
        ], 12.0, 23, 0.3).move_to([0, -1.9, 0])
        tag = psyche_tag(r"\texttt{workspace.schurger}: \ $dx = (I - kx)\,dt + c\,dW$")
        with self.voiceover(
            "In 2012 Aaron Schurger, Jacobo Sitt and Stanislas Dehaene offered another reading. "
            "<bookmark mark='a'/> When there's no reason to move at one moment rather than another, they proposed, "
            "the timing is decided by spontaneous fluctuations in neural activity, accumulated slowly, like the "
            "evidence of Part 25 but without any evidence. <bookmark mark='b'/> Here is Psyche's version: a leaky "
            "accumulator of noise, with a small drift. Whenever it crosses the threshold, a movement starts and the "
            "accumulator resets. <bookmark mark='c'/> The waits between movements are irregular, with a median of "
            f"about {d['median_wait']:.0f} seconds, much like people told to move whenever they like."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(thr), Create(tr), FadeIn(hits), FadeIn(rows[1]), run_time=4)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def average(self):
        d = load("libet")
        head = heading(r"A ramp made of noise")
        A = axes([-3, 0], [-0.05, 0.32], x_length=6.0, y_length=4.0, xticks=[-3, -2, -1, 0], yticks=[0, 0.1, 0.2, 0.3],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", xlabel=r"time before the movement, \ s",
                 ylabel=r"activity, \ aligned to each movement", center=[-3.2, -0.3, 0], font_size=16)
        eps = VGroup(*[curve(A.ax, d["bt"], e, GREY_D, 1.5) for e in d["sample_epochs"]])
        m = curve(A.ax, d["bt"], d["bmean"], RPT, 5)
        rows = rows_of([
            (rf"line up all {d['n_epochs']} movements and average the activity before each, \ as an EEG lab averages "
             r"the readiness potential", WHITE),
            (rf"a slow ramp appears, \ beginning about {abs(d['onset']):.0f} s before the movement", RPT),
            (r"nothing was decided early: \ any crossing is preceded, \ on average, \ by a climb; \ selecting the "
             r"moments of crossing makes the ramp", MODEL),
            (r"the prediction that followed: \ interrupt people at random, \ and those whose activity happened to be "
             r"high respond fastest \ (Schurger and colleagues found this)", GNW),
        ], 5.6, 22, 0.3).move_to([3.5, -0.1, 0])
        tag = psyche_tag(r"\texttt{workspace.back\_average}; \ Schurger, \ Sitt \& Dehaene (2012)")
        with self.voiceover(
            f"Now do what an EEG lab does. <bookmark mark='a'/> Line up all {d['n_epochs']} movements and average the "
            "activity in the seconds before each. The grey lines are single epochs, all noise. "
            "<bookmark mark='b'/> Their average is a slow ramp, beginning about "
            f"{abs(d['onset']):.0f} seconds before the movement: a readiness potential. <bookmark mark='c'/> But "
            "nothing was decided early. Any crossing is preceded, on average, by a climb, so lining up the moments "
            "of crossing creates the ramp. <bookmark mark='d'/> The idea makes a prediction: interrupt people at "
            "random while they wait, and those whose activity happens to be high should respond fastest. Schurger "
            "and colleagues found that in 2012. The readiness potential may reflect when a movement is about to "
            "happen, not a decision taken behind the person's back."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(Create(eps), FadeIn(rows[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(m), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def after(self):
        head = heading(r"Where the debate stands")
        rows = rows_of([
            (r"the timing replicates: \ the ramp starts before the reported urge", WHITE),
            (r"Trevena and Miller, \ 2010: \ a similar ramp appears when people wait for a cue and then decide "
             r"\emph{not} to move", HOT),
            (r"Soon and colleagues, \ 2008: \ which hand people would choose could be decoded from brain activity "
             r"seconds before, \ but only about 60\% of the time", SEEN),
            (r"what it means for free will is \emph{Philosophy, Built}, \ Part 32; \ the experiments show that "
             r"the felt moment of deciding is a report, \ timed like any other", MODEL),
        ], 12.0, 24, 0.38).move_to([0, -0.2, 0])
        tag = published_tag(r"Trevena \& Miller (2010); \ Soon, \ Brass, \ Heinze \& Haynes (2008)")
        with self.voiceover(
            "Where does the debate stand? <bookmark mark='a'/> The timing replicates: the ramp does begin before the "
            "reported urge. <bookmark mark='b'/> But Judy Trevena and Jeff Miller found in 2010 that a similar ramp "
            "appears when people wait for a cue and then decide not to move, so it isn't a commitment to act. "
            "<bookmark mark='c'/> In 2008 Chun Siong Soon, John-Dylan Haynes and colleagues decoded which hand people "
            "would choose from brain activity seconds before they knew, but only about sixty percent of the time, "
            "barely better than a coin. <bookmark mark='d'/> What any of this means for free will is a question for "
            "Part 32 of Philosophy, Built. What the experiments do show is that the felt moment of deciding is a "
            "report, with a time that can be measured and misjudged like any other."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
