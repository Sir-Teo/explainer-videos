from __future__ import annotations

from videos.psychology.psych29.common import *  # noqa: F403


class Forecast(VoiceoverScene):
    def construct(self):
        self.card()
        self.on_you()
        self.tenure()
        self.model()
        self.lottery()

    def card(self):
        card = chapter_card(10, r"Affective forecasting", r"Do we know how we will feel?",
                            lit={1978: r"Brickman et al.", 1998: r"Gilbert et al.", 2005: r"Wilson \& Gilbert"},
                            part=PART, scale=("mind", "person"), marr=("what",))
        with self.voiceover("Chapter ten. Affective forecasting."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def on_you(self):
        stage = demo_stage(12.4, 4.0, center=[0, 0.5, 0])
        q = wrapped_label(r"Picture something you are hoping for this year. \ If it happens, \ how much happier will "
                          r"you be a month later? \ A year later?", 11.0, 30, YOU).move_to([0, 0.9, 0])
        note = label(r"hold your answer; \ the part checks it at the end", font_size=24, color=WHITE).move_to(
            [0, -0.4, 0])
        with self.voiceover(
            "Before the research, a question for you. <bookmark mark='a'/> Picture something you are hoping for "
            "this year: a job, a result, a move. If it happens, how much happier will you be a month later? And a "
            "year later? <bookmark mark='b'/> Hold your answer. We'll come back to it at the end of this part."
        ) as vo:
            self.play(FadeIn(stage))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(note))
        self.clear_scene()

    def tenure(self):
        head = heading(r"The impact bias")
        rows = rows_of([
            (r"Daniel Gilbert, \ Timothy Wilson and colleagues, \ 1998: \ six studies of predicted against "
             r"experienced feelings", WHITE),
            (r"assistant professors predicted that the tenure decision would affect their happiness for years; \ "
             r"former assistant professors who had and had not received tenure were about equally happy", COG),
            (r"the same in voters after elections, \ people after breakups, \ and more", FACE),
            (r"we predict the direction of our feelings well, \ and their intensity and duration badly: \ the "
             r"impact bias", UNPL),
            (r"immune neglect: \ we forget how quickly we make sense of events and recover; \ focalism: \ we "
             r"forget everything else that will happen", BODY),
        ], 12.2, 25, 0.38).move_to([0, -0.2, 0])
        tag = published_tag(r"Gilbert et al.\ (1998); \ Wilson \& Gilbert (2005)")
        with self.voiceover(
            "Most people's answer is too large. <bookmark mark='a'/> In 1998 Daniel Gilbert, Timothy Wilson and "
            "their colleagues ran six studies comparing predicted feelings with experienced ones. "
            "<bookmark mark='b'/> Assistant professors predicted that the decision on their tenure would affect "
            "their happiness for years. Former assistant professors who had received tenure and those who had not "
            "were about equally happy. <bookmark mark='c'/> The pattern recurs in voters after elections, people "
            "after breakups, and many other cases. <bookmark mark='d'/> We predict the direction of our feelings "
            "well, and their intensity and duration badly. Gilbert and Wilson called it the impact bias. "
            "<bookmark mark='e'/> Two reasons: immune neglect, forgetting how quickly we make sense of events and "
            "recover, and focalism, forgetting everything else that will happen in the same months."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def model(self):
        d = load("forecast")
        head = heading(r"Derivation: \ adaptation and the forecast")
        A = axes([0, 365], [0, 3.2], x_length=5.8, y_length=3.6, xticks=[0, 30, 90, 180, 365], yticks=[0, 1, 2, 3],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"days after the event",
                 ylabel=r"happier than before", center=[-3.3, -0.2, 0], font_size=16)
        ca = curve(A.ax, d["t"], d["actual"], PLEAS, 4)
        cp = curve(A.ax, d["t"], d["predicted"], COG, 4)
        key = legend([(COG, r"forecast"), (PLEAS, r"experienced")], font_size=17).move_to(A.ax.c2p(250, 2.6))
        mark = DashedLine(A.ax.c2p(d["at"], 0), A.ax.c2p(d["at"], 3.2), color=GREY_B, stroke_width=2)
        eq = MathTex(r"h(t) = h_0 + I\, e^{-t/\tau}", font_size=38)
        rows = rows_of([
            (r"Psyche: \ an event's impact $I$ fades with time constant $\tau$; \ the forecaster gets $I$ right "
             r"and $\tau$ wrong", MODEL),
            (r"experienced: \ $\tau = 20$ days; \ forecast: \ $\tau = 150$ days \ (illustrative)", WHITE),
            (rf"two months on, \ the forecast is {d['predicted_at']:.1f} points happier; \ the experience, \ "
             rf"{d['actual_at']:.1f}", UNPL),
            (r"the error is in the duration, \ which is what immune neglect predicts", BODY),
        ], 5.6, 21, 0.3)
        right = VGroup(eq, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{emotion.forecast}")
        with self.voiceover(
            "The simplest model of adaptation makes the error visible. <bookmark mark='a'/> After an event, "
            "happiness jumps by an impact I, and fades back exponentially with a time constant tau. The forecaster "
            "here gets the impact right and the time constant wrong. <bookmark mark='b'/> The experience fades with "
            "tau of twenty days; the forecast assumes a hundred and fifty. Both numbers are illustrative. "
            f"<bookmark mark='c'/> Two months on, the forecast says {d['predicted_at']:.1f} points happier; the "
            f"experience is {d['actual_at']:.1f}. <bookmark mark='d'/> The error is in the duration, which is "
            "what immune neglect predicts."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Write(eq))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(cp), Create(ca), FadeIn(key), FadeIn(rows[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(mark), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def lottery(self):
        head = heading(r"Lottery winners and accident victims, \ 1978")
        A = axes([0, 3], [0, 5], x_length=5.4, y_length=3.4, xticks=None, yticks=[0, 1, 2, 3, 4, 5],
                 yfmt=lambda v: f"{v:g}", ylabel=r"present happiness, \ 0 to 5", center=[-3.5, -0.3, 0],
                 font_size=16)
        vals = [(r"lottery winners", 4.00, PLEAS), (r"controls", 3.82, GREY_B), (r"paralysed by accidents", 2.96, FEAR)]
        bs = VGroup()
        for i, (t, v, c) in enumerate(vals):
            b = bars(A.ax, [0.5 + i], [v], c, width=0.6)
            bs.add(VGroup(b, label(f"{v:.2f}", font_size=17, color=c).next_to(b, UP, buff=0.08),
                          wrapped_label(t, 1.6, 16, c).next_to(A.ax.c2p(0.5 + i, 0), DOWN, buff=0.15)))
        rows = rows_of([
            (r"Philip Brickman, \ Dan Coates and Ronnie Janoff-Bulman: \ 22 Illinois lottery winners, \ 29 people "
             r"paralysed in accidents, \ 22 controls", WHITE),
            (r"the winners were no happier than the controls; \ the accident victims were less happy, \ by less "
             r"than people expect", COG),
            (r"small samples, \ one interview, \ and a scale with a ceiling: \ a striking picture, \ not a law",
             UNPL),
            (r"later panel studies: \ people adapt to many events, \ but not completely to all; \ disability and "
             r"unemployment leave lasting marks for many", BODY),
        ], 5.8, 21, 0.3).move_to([3.4, -0.1, 0])
        tag = published_tag(r"Brickman, \ Coates \& Janoff-Bulman (1978); \ Lucas (2007)")
        with self.voiceover(
            "The most famous illustration is older. <bookmark mark='a'/> In 1978 Philip Brickman, Dan Coates and "
            "Ronnie Janoff-Bulman interviewed twenty-two people who had won large prizes in the Illinois lottery, "
            "twenty-nine people paralysed in accidents, and twenty-two controls. <bookmark mark='b'/> On a scale "
            "from zero to five, the winners rated their present happiness at 4.00, the controls at 3.82, and the "
            "accident victims at 2.96: less happy, but by less than most people would guess. "
            "<bookmark mark='c'/> These are small samples, one interview, and a scale with a ceiling: a striking "
            "picture, not a law. <bookmark mark='d'/> Later studies that follow the same people over years, "
            "reviewed by Richard Lucas, find that people adapt to many events, but not completely to all of them. "
            "Disability and long unemployment leave lasting marks for many people."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in bs], lag_ratio=0.3), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
