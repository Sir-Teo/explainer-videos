from __future__ import annotations

from videos.psychology.psych39.common import *  # noqa: F403


class Epi(VoiceoverScene):
    def construct(self):
        self.card()
        self.prevalence()
        self.gap()

    def card(self):
        card = chapter_card(9, r"How common?", r"How many people, \ and how many treated?",
                            lit={2004: r"Kohn et al.", 2005: r"Kessler et al.", 2017: r"Jorm et al."}, part=PART,
                            scale=("group",), marr=("what",))
        with self.voiceover("Chapter nine. How common?"):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def prevalence(self):
        head = heading(r"Nearly half, \ starting young")
        A = axes([0, 75], [0, 11], x_length=5.0, y_length=2.6, xticks=[0, 15, 30, 45, 60, 75], yticks=None,
                 xfmt=lambda v: f"{v:.0f}", xlabel=r"age", center=[-3.4, -0.6, 0], font_size=14)
        meds = [(r"anxiety", 11, SYMP), (r"impulse control", 11, PERSON), (r"substance use", 20, AUTH),
                (r"mood", 30, MODEL)]
        marks = VGroup()
        for k, (n, age, c) in enumerate(meds):
            y = 9 - 2.4 * k
            marks.add(VGroup(Dot(A.ax.c2p(age, y), radius=0.09, color=c),
                             label(rf"{n}: \ {age}", font_size=14, color=c).next_to(A.ax.c2p(age, y), RIGHT,
                                                                                     buff=0.12)))
        half = DashedLine(A.ax.c2p(14, 0), A.ax.c2p(14, 10.5), color=GREY_B)
        lh = label(r"half of all cases by 14", font_size=13, color=GREY_B).next_to(A.ax.c2p(14, 10.5), UP,
                                                                                  buff=0.05)
        ml = label(r"median age at onset", font_size=14, color=GREY_A).next_to(A, UP, buff=0.55)
        rows = rows_of([
            (r"Kessler and colleagues, \ 2005: \ the National Comorbidity Survey Replication, \ a representative "
             r"sample of US adults interviewed in person", WHITE),
            (r"46.4\% had met the criteria for at least one disorder at some point in their lives", PERSON),
            (r"half of all lifetime cases had begun by age 14, \ three quarters by 24", SYMP),
            (r"lifetime prevalence depends on the thresholds of chapter six, \ and on remembering: \ follow-up "
             r"studies that ask repeatedly find even higher rates", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = published_tag(r"Kessler et al.\ (2005)")
        with self.voiceover(
            "How common are disorders? <bookmark mark='a'/> In 2005 Ronald Kessler and colleagues reported the "
            "National Comorbidity Survey Replication, a representative sample of American adults interviewed in "
            "person. <bookmark mark='b'/> Forty-six percent had met the criteria for at least one disorder at some "
            "point in their lives. <bookmark mark='c'/> Half of all lifetime cases had begun by age fourteen, three "
            "quarters by twenty-four. Anxiety typically starts in childhood, mood disorders around thirty. "
            "<bookmark mark='d'/> Lifetime prevalence depends on the thresholds of chapter six, and on remembering. "
            "Studies that follow people and ask repeatedly find even higher rates."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(ml))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), LaggedStart(*[FadeIn(m_) for m_ in marks], lag_ratio=0.4), Create(half),
                      FadeIn(lh))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def gap(self):
        head = heading(r"The treatment gap, \ and a paradox")
        A = axes([-0.6, 1.6], [0, 100], x_length=3.6, y_length=2.6, xticks=None, yticks=[0, 50, 100],
                 yfmt=lambda v: f"{v:.0f}\\%", ylabel=r"untreated", center=[-4.0, -0.4, 0], font_size=14)
        b = bars(A.ax, [0, 1], [56.3, 78.1], [MODEL, AUTH], width=0.6)
        names = VGroup(wrapped_label(r"major depression", 1.6, 14, MODEL).next_to(A.ax.c2p(0, 0), DOWN, buff=0.15),
                       wrapped_label(r"alcohol use disorders", 1.6, 14, AUTH).next_to(A.ax.c2p(1, 0), DOWN,
                                                                                       buff=0.15))
        tops = VGroup(label(r"56\%", font_size=16, color=MODEL).next_to(A.ax.c2p(0, 56.3), UP, buff=0.08),
                      label(r"78\%", font_size=16, color=AUTH).next_to(A.ax.c2p(1, 78.1), UP, buff=0.08))
        rows = rows_of([
            (r"Kohn and colleagues, \ 2004: \ across studies worldwide, \ 56\% of people with major depression and "
             r"78\% with alcohol use disorders had received no treatment", WHITE),
            (r"the gap is widest in low- and middle-income countries", PERSON),
            (r"Jorm, \ Patten, \ Brugha and Mojtabai, \ 2017: \ in Australia, \ Canada, \ England and the US, \ "
             r"treatment rose sharply, \ especially antidepressants, \ but the prevalence of anxiety and "
             r"depression did not fall", AUTH),
            (r"possible reasons: \ treatment that reaches the wrong people, \ or works less well in practice than "
             r"in trials; \ Part 42 weighs the evidence", YOU),
        ], 6.4, 19, 0.36).move_to([3.2, -0.2, 0])
        tag = published_tag(r"Kohn et al.\ (2004); \ Jorm et al.\ (2017)")
        with self.voiceover(
            "Most people with a disorder are never treated. <bookmark mark='a'/> In 2004 Robert Kohn and colleagues "
            "pooled studies worldwide. Fifty-six percent of people with major depression, and seventy-eight percent "
            "with alcohol use disorders, had received no treatment. <bookmark mark='b'/> The gap is widest in low- "
            "and middle-income countries. <bookmark mark='c'/> But here's a paradox. In 2017 Anthony Jorm and "
            "colleagues looked at Australia, Canada, England and the United States. Treatment had risen sharply, "
            "antidepressants especially, but the prevalence of anxiety and depression hadn't fallen. "
            "<bookmark mark='d'/> Possible reasons: treatment that reaches the wrong people, or works less well in "
            "practice than in trials. Part 42 weighs the evidence."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), *[GrowFromEdge(x, DOWN) for x in b], FadeIn(tops))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
