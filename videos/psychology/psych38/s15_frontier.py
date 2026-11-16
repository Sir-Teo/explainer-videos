from __future__ import annotations

from videos.psychology.psych38.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.distance()
        self.open_questions()

    def card(self):
        card = chapter_card(14, r"Frontier: \ distance, \ history and machines", r"What is still unknown about "
                            r"culture?", lit={2020: r"Muthukrishna et al."}, part=PART, scale=("culture",),
                            marr=("what",))
        with self.voiceover("Chapter fourteen. Frontier: distance, history and machines."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def distance(self):
        head = heading(r"Cultural distance as a number")
        eq = MathTex(r"F_{ST} = \frac{\text{variance between groups}}{\text{total variance}}", font_size=34,
                     color=MODEL).move_to([-3.4, 1.6, 0])
        A = axes([0, 1], [0, 1], x_length=4.2, y_length=2.4, xticks=None, yticks=None, center=[-3.4, -1.0, 0],
                 font_size=13)
        rng = np.random.default_rng(3)
        g1 = scatter(A.ax, rng.normal(0.3, 0.08, 40), rng.normal(0.55, 0.12, 40), WEST, radius=0.04)
        g2 = scatter(A.ax, rng.normal(0.7, 0.08, 40), rng.normal(0.45, 0.12, 40), WORLD, radius=0.04)
        rows = rows_of([
            (r"Muthukrishna and colleagues, \ 2020: \ population genetics' fixation index applied to answers in the "
             r"World Values Survey", WHITE),
            (r"the cultural distance between any two countries becomes a number, \ and a study can say how far its "
             r"samples are from the United States, \ or from China", MODEL),
            (r"historical psychology: \ reading old texts to estimate how minds of the past differed", WORLD),
            (r"and machines as participants, \ whose own culture is still to be measured", GOOD),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = published_tag(r"Muthukrishna et al.\ (2020)")
        with self.voiceover(
            "The frontier is making culture measurable. <bookmark mark='a'/> In 2020 Michael Muthukrishna and "
            "colleagues took population genetics' fixation index, the share of variation that lies between groups, "
            "and applied it to answers in the World Values Survey. <bookmark mark='b'/> The cultural distance "
            "between any two countries becomes a number, and a study can say how far its samples are from the "
            "United States, or from China. <bookmark mark='c'/> Historical psychology reads old texts to estimate "
            "how the minds of the past differed. <bookmark mark='d'/> And machines have become participants, whose "
            "own culture is still to be measured."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(eq), FadeIn(A), FadeIn(g1), FadeIn(g2))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def open_questions(self):
        head = heading(r"Open questions")
        rows = rows_of([
            (r"which psychological differences are caused by ecology, \ institutions or history, \ and how could "
             r"one tell?", WORLD),
            (r"can self-report scales be made comparable across cultures, \ or should comparisons rest on "
             r"behaviour?", MODEL),
            (r"is any moral intuition present before experience, \ and how would a registered test show it?", GOOD),
            (r"what would a psychology look like if it were built from the majority world outward?", PERSON),
            (r"whose values should a machine learn, \ and who decides?", YOU),
        ], 12.4, 24, 0.46).move_to([0, -0.2, 0])
        with self.voiceover(
            "So, open questions. Which psychological differences are caused by ecology, institutions or history, "
            "and how could anyone tell? <bookmark mark='b'/> Can self-report scales be made comparable across "
            "cultures, or should comparisons rest on behaviour? <bookmark mark='c'/> Is any moral intuition present "
            "before experience, and how would a registered test show it? <bookmark mark='d'/> What would a "
            "psychology look like if it were built from the majority world outward? <bookmark mark='e'/> And whose "
            "values should a machine learn, and who decides?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.15))
            for m, r in zip("bcde", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
