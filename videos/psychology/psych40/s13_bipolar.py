from __future__ import annotations

from videos.psychology.psych40.common import *  # noqa: F403


class Bipolar(VoiceoverScene):
    def construct(self):
        self.card()
        self.lithium()
        self.prediction()
        self.base_rate()

    def card(self):
        card = chapter_card(12, r"Bipolar disorder, \ lithium, \ and suicide", r"What can and cannot be predicted?",
                            lit={1949: r"Cade", 2017: r"Franklin et al."}, part=PART, scale=("molecule", "person"),
                            marr=("what",))
        with self.voiceover("Chapter twelve. Bipolar disorder, lithium, and suicide."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def lithium(self):
        head = heading(r"Highs and lows")
        A = axes([0, 24], [-1.2, 1.2], x_length=5.4, y_length=2.4, xticks=None, yticks=None,
                 xlabel=r"months", ylabel=r"mood", center=[-3.3, 0.6, 0], font_size=13)
        t = np.linspace(0, 24, 400)
        m = 0.9 * np.sin(2 * np.pi * t / 9) * (0.6 + 0.4 * np.sin(t / 3.1) ** 2)
        mood = curve(A.ax, t, m, PERSON, stroke_width=3)
        zero = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(24, 0), color=GREY_D)
        lm = label(r"schematic", font_size=13, color=GREY_B).next_to(A, DOWN, buff=0.3)
        rows = rows_of([
            (r"bipolar disorder: \ episodes of depression and of mania, \ with high energy, \ little sleep and "
             r"risky confidence, \ separated by periods of being well", WHITE),
            (r"Cade, \ 1949: \ lithium salts calmed patients with mania, \ a chance discovery from animal "
             r"experiments", GOOD),
            (r"lithium is still a first-line treatment for preventing episodes, \ and needs blood monitoring "
             r"because the effective and toxic doses are close", SYMP),
            (r"it is a case where a treatment came long before any account of how it works", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = historical_tag(r"Cade (1949)")
        with self.voiceover(
            "Mood can go the other way too. <bookmark mark='a'/> Bipolar disorder brings episodes of depression and "
            "of mania, with high energy, little sleep and risky confidence, separated by periods of being well. "
            "<bookmark mark='b'/> In 1949 the Australian psychiatrist John Cade reported that lithium salts calmed "
            "patients with mania, a chance discovery from experiments on animals. <bookmark mark='c'/> Lithium is "
            "still a first-line treatment for preventing episodes, and it needs blood monitoring, because the "
            "effective and toxic doses are close. <bookmark mark='d'/> It's a case where a treatment came long before "
            "any account of how it works."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(zero), FadeIn(lm))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(mood), run_time=2.5)
            for m_, r in zip("bcd", rows[1:]):
                vo.wait_until(m_)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def prediction(self):
        head = heading(r"Why suicide is so hard to predict")
        rows = rows_of([
            (r"Franklin and colleagues, \ 2017: \ a meta-analysis of 365 studies over fifty years of risk factors "
             r"for suicidal thoughts and behaviours", WHITE),
            (r"every known risk factor predicted only slightly better than chance, \ and prediction had not "
             r"improved over the fifty years", AUTH),
            (r"the base-rate problem of Part 39: \ suicide is rare in any short period, \ so even a strong risk "
             r"factor flags far more people than will act", PERSON),
            (r"so care does not rest on prediction: \ asking directly about suicidal thoughts is safe and helps, \ "
             r"and support is offered to everyone who is struggling", GOOD),
        ], 12.4, 22, 0.44).move_to([0, 0.2, 0])
        help_ = wrapped_label(r"if you are struggling: \ call your local emergency number; \ in the US call or text "
                              r"988; \ in the UK and Ireland, \ Samaritans on 116 123; \ findahelpline.com for other "
                              r"countries", 12.0, 19, CARE).to_edge(DOWN, buff=0.7)
        tag = published_tag(r"Franklin et al.\ (2017)")
        with self.voiceover(
            "Finally, suicide, and what research can and can't do. <bookmark mark='a'/> In 2017 Joseph Franklin and "
            "colleagues meta-analysed three hundred and sixty-five studies covering fifty years of research on risk "
            "factors for suicidal thoughts and behaviours. <bookmark mark='b'/> Every known risk factor predicted "
            "only slightly better than chance, and prediction hadn't improved over the fifty years. "
            "<bookmark mark='c'/> Part of the reason is the base-rate problem of Part 39. In any short period, "
            "suicide is rare, so even a strong risk factor flags far more people than will act. "
            "<bookmark mark='d'/> So care doesn't rest on prediction. Asking someone directly about suicidal "
            "thoughts is safe, and it helps, and support is offered to everyone who is struggling. If that's you, "
            "the numbers are on the screen."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            self.play(FadeIn(help_))
        self.wait(1.5)
        self.clear_scene()

    def base_rate(self):
        d = load("suicide")
        head = heading(r"The base rate, \ in natural frequencies")
        grid = VGroup(*[Square(0.09, stroke_width=0, fill_color=OFF, fill_opacity=1) for _ in range(2000)])
        grid.arrange_in_grid(40, 50, buff=0.025).move_to([-3.6, 0.15, 0])
        pick = np.random.default_rng(40).choice(2000, size=400, replace=False)
        flagged = VGroup(*[grid[int(i)] for i in sorted(pick)])
        g_l = label(r"2{,}000 of 10{,}000 people, \ one square for every five", font_size=14, color=GREY_B).next_to(
            grid, DOWN, buff=0.2)
        rows = rows_of([
            (r"a risk factor that is right 80\% of the time both ways, \ for an outcome with a yearly rate of 1 in "
             r"2{,}000", WHITE),
            (rf"in 10{{,}}000 people: \ {d['sick']:.0f} will die by suicide in the year, \ and the factor flags "
             rf"{d['tp']:.0f} of them", PERSON),
            (rf"it also flags {num(round(d['fp']))} of the {num(round(d['N'] - d['sick']))} who will not", AUTH),
            (rf"so of everyone flagged, \ about {100 * d['ppv']:.1f}\% will die in that year: \ 1 in 500", MODEL),
            (r"which is why care is offered to everyone who is struggling, \ and not rationed by a score", GOOD),
        ], 6.0, 19, 0.34).move_to([3.4, -0.2, 0])
        help_ = wrapped_label(r"if you are struggling: \ call your local emergency number; \ in the US call or text "
                              r"988; \ in the UK and Ireland, \ Samaritans on 116 123; \ findahelpline.com for other "
                              r"countries", 8.6, 17, CARE).move_to([-2.3, -3.35, 0])
        tag = psyche_tag(r"\texttt{clinic.screen}; \ Part 39's natural frequencies")
        with self.voiceover(
            "Here's the base-rate problem in numbers. <bookmark mark='a'/> Take a risk factor that's right eighty "
            "percent of the time both ways, for an outcome with a yearly rate of one in two thousand. "
            "<bookmark mark='b'/> In ten thousand people, five will die by suicide in the year, and the factor flags "
            "four of them. <bookmark mark='c'/> It also flags nearly two thousand of the people who won't. "
            "<bookmark mark='d'/> So of everyone flagged, about one in five hundred will die in that year. "
            "<bookmark mark='e'/> Which is why care is offered to everyone who is struggling, and not rationed by a "
            "score."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(grid), FadeIn(g_l))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), *[x.animate.set_fill(AUTH) for x in flagged], run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]), FadeIn(help_))
        self.wait(1.5)
        self.clear_scene()
