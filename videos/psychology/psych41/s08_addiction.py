from __future__ import annotations

from videos.psychology.psych41.common import *  # noqa: F403


class Addiction(VoiceoverScene):
    def construct(self):
        self.card()
        self.stages()
        self.wanting()
        self.discounting()

    def card(self):
        card = chapter_card(7, r"From use to compulsion", r"How does a choice become a compulsion?",
                            lit={1993: r"Robinson \& Berridge"}, part=PART, scale=("molecule", "circuit", "person"),
                            marr=("what", "how"))
        with self.voiceover("Chapter seven. From use to compulsion."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def stages(self):
        head = heading(r"Four mechanisms the series has built")
        data = (
            (r"reward", r"drugs of abuse raise dopamine in the striatum directly, \ bypassing the events that "
                        r"normally earn it (Part 17)", PERSON),
            (r"tolerance and withdrawal", r"the body's opponent process grows with use: \ more drug for the same "
                                          r"effect, \ and misery without it (Part 10)", SYMP),
            (r"wanting without liking", r"cues for the drug come to trigger craving, \ while the pleasure fades "
                                        r"(Part 28)", AUTH),
            (r"habit", r"use passes from goal-directed choice to a habit set off by cues (Part 17)", MODEL),
        )
        rows = VGroup()
        for what, how, c in data:
            rows.add(VGroup(word_chip(what, color=c, font_size=18, width=3.8), wrapped_label(how, 8.0, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 0.2, 0])
        foot = wrapped_label(r"most people who use a drug never become addicted: \ addiction is continued use despite "
                             r"harm, \ loss of control and craving, \ not use itself", 12.0, 20, YOU).move_to([0, -2.6, 0])
        with self.voiceover(
            "Addiction draws on four mechanisms the series has already built. <bookmark mark='a'/> Reward: drugs of "
            "abuse raise dopamine in the striatum directly, bypassing the events that normally earn it. "
            "<bookmark mark='b'/> Tolerance and withdrawal: the body's opponent process grows with use, so more drug "
            "is needed for the same effect, and its absence brings misery. <bookmark mark='c'/> Wanting without "
            "liking: cues for the drug come to trigger craving, while the pleasure fades. <bookmark mark='d'/> And "
            "habit: use passes from goal-directed choice to a habit set off by cues. <bookmark mark='e'/> And most "
            "people who use a drug never become addicted. Addiction is continued use despite harm, loss of control "
            "and craving. It isn't use itself."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def wanting(self):
        head = heading(r"Wanting grows, \ liking does not")
        A = axes([0, 10], [0, 1.1], x_length=5.4, y_length=3.0, xticks=None, yticks=None, xlabel=r"months of use",
                 ylabel=r"strength", center=[-3.4, 0.4, 0], font_size=13)
        t = np.linspace(0, 10, 200)
        want = curve(A.ax, t, 0.2 + 0.75 * (1 - np.exp(-t / 3)), AUTH, stroke_width=3)
        like = curve(A.ax, t, 0.8 * np.exp(-t / 6) + 0.15, GOOD, stroke_width=3)
        key = VGroup(label(r"wanting: \ craving set off by cues", font_size=14, color=AUTH),
                     label(r"liking: \ the pleasure of the drug", font_size=14, color=GOOD)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).next_to(A, DOWN, buff=0.3)
        lm = label(r"schematic", font_size=13, color=GREY_B).next_to(key, DOWN, buff=0.12)
        rows = rows_of([
            (r"Robinson and Berridge, \ 1993: \ repeated drug use sensitizes the dopamine system's ``wanting'', \ "
             r"its incentive salience, \ without increasing ``liking''", WHITE),
            (r"cues tied to the drug become magnets for attention and craving, \ long after withdrawal ends", AUTH),
            (r"so a person can crave what they no longer enjoy: \ relapse years later, \ set off by a place or a "
             r"smell", YOU),
        ], 6.0, 20, 0.4).move_to([3.4, -0.2, 0])
        tag = published_tag(r"Robinson \& Berridge (1993)")
        with self.voiceover(
            "The third mechanism deserves a closer look. <bookmark mark='a'/> In 1993 Terry Robinson and Kent "
            "Berridge proposed that repeated drug use sensitizes the dopamine system's wanting, its incentive "
            "salience, without increasing liking. <bookmark mark='b'/> Cues tied to the drug become magnets for "
            "attention and craving, long after withdrawal ends. <bookmark mark='c'/> So a person can crave what they "
            "no longer enjoy, and relapse years later, set off by a place or a smell."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(lm))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(want), Create(like), FadeIn(key), run_time=2.0)
            for m, r in zip("bc", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def discounting(self):
        d = load("discount")
        head = heading(r"Now or later")
        A = axes([0, 365], [0, 105], x_length=5.6, y_length=3.0, xticks=[0, 100, 200, 300],
                 yticks=[0, 50, 100], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                 xlabel=r"delay to 100 (days)", ylabel=r"value now", center=[-3.3, 0.5, 0], font_size=13)
        shallow = curve(A.ax, d["delay"], d["v1"], GOOD, stroke_width=3)
        steep = curve(A.ax, d["delay"], d["v5"], AUTH, stroke_width=3)
        fifty = DashedLine(A.ax.c2p(0, 50), A.ax.c2p(365, 50), color=GREY_B, stroke_width=1.5)
        f_l = label(r"50 now", font_size=12, color=GREY_B).next_to(A.ax.c2p(365, 50), UP, buff=0.05)
        key = VGroup(label(r"$k = 0.01$ per day", font_size=14, color=GOOD),
                     label(r"$k = 0.05$ per day", font_size=14, color=AUTH)).arrange(DOWN, aligned_edge=LEFT,
                                                                                    buff=0.1).next_to(A, DOWN, buff=0.3)
        eq = MathTex(r"V = \frac{A}{1 + kD}", font_size=34, color=MODEL).move_to([-3.3, -2.6, 0])
        rows = rows_of([
            (r"Part 26's hyperbolic discounting: \ a reward's value falls with its delay $D$, \ at a rate $k$", WHITE),
            (rf"with $k = 0.01$, \ 100 later beats 50 now until the wait passes {d['switch1']:.0f} days; \ with "
             rf"$k = 0.05$, \ only until {d['switch5']:.0f} days", MODEL),
            (r"on average, \ people with addictions discount the future more steeply than others, \ and steep "
             r"discounting predicts who starts and who relapses", AUTH),
            (r"cause or consequence? \ both, \ probably: \ it predicts use, \ and use steepens it", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = psyche_tag(r"\texttt{clinic.discount}")
        with self.voiceover(
            "There's also the trade between now and later. <bookmark mark='a'/> Part 26 introduced hyperbolic "
            "discounting: a reward's value falls with its delay, at a rate k. <bookmark mark='b'/> With a gentle k, a "
            "hundred later beats fifty now until the wait passes a hundred days. With a steep k, only until twenty "
            "days. <bookmark mark='c'/> On average, people with addictions discount the future more steeply than "
            "others, and steep discounting predicts who starts and who relapses. <bookmark mark='d'/> Cause or "
            "consequence? Probably both. It predicts use, and use steepens it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(fifty), FadeIn(f_l), FadeIn(eq))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(shallow), Create(steep), FadeIn(key), run_time=2.0)
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
