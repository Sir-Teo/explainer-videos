from __future__ import annotations

from videos.industry.industry2.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.answers()
        self.next_part()

    def answers(self):
        lines = [
            ("By sales", "the biggest businesses are shops, insurers and wholesalers: sales count the same dollar again."),
            ("By value added", "real estate, government and manufacturing lead a $30.9 trillion economy."),
            ("By jobs", "government, health care and business services, each with more than 22 million."),
            ("By profit", "a handful of technology companies, each earning $80-133bn with few people."),
            ("Leontief's table", "shows how a dollar spent in one industry runs through all the others."),
        ]
        rows = VGroup()
        for a, b in lines:
            r = VGroup(TB(a, 22, I.ACCENT), T(b, 21, I.TEXT)).arrange(RIGHT, buff=0.3)
            if r.width > 12.6:
                r.scale_to_fit_width(12.6)
            rows.add(r)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(UP * 0.3).align_to(LEFT * 6.3, LEFT)
        head = TB("How big is each industry?", 26, I.DIM).to_edge(UP, buff=0.4)
        verdict = T("It depends on what you count, and each count answers a different question.", 25, I.MONEY
                    ).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "So, how big is each industry? <bookmark mark='a'/> By sales, the biggest businesses are shops, insurers "
            "and wholesalers, because sales count the same dollar again at every step. <bookmark mark='b'/> By value "
            "added, real estate, government and manufacturing lead a 30.9 trillion dollar economy. <bookmark "
            "mark='c'/> By jobs, government, health care and business services. <bookmark mark='d'/> By profit, a "
            "handful of technology companies that earn a great deal with few people. <bookmark mark='e'/> And "
            "Leontief's table shows how a dollar spent in one industry runs through all the others. <bookmark "
            "mark='f'/> The answer depends on what you count, and each count answers a different question."
        ) as vo:
            self.play(FadeIn(head))
            for i, m in enumerate("abcde"):
                vo.wait_until(m)
                self.play(FadeIn(rows[i], shift=RIGHT * 0.15), run_time=0.8)
            vo.wait_until("f")
            self.play(FadeIn(verdict, shift=UP * 0.1))
        self.wait(0.8)
        self.clear_scene()

    def next_part(self):
        book = VGroup(*[Rectangle(width=2.0, height=2.6, fill_color="#2B2620", fill_opacity=1, stroke_color="#8A6A12",
                                  stroke_width=2).shift(RIGHT * 0.06 * k + UP * 0.06 * k) for k in range(3)])
        lines_ = VGroup(*[Line(LEFT * 0.7, RIGHT * 0.7, color="#C8B79A", stroke_width=1.5).shift(UP * (0.8 - 0.3 * k))
                          for k in range(6)]).move_to(book[-1])
        g = VGroup(book, lines_).move_to(LEFT * 3.4)
        cap = VGroup(T("Next", 22, I.DIM), TB("Part 3 · The Accounts", 32, I.TEXT),
                     T("Luca Pacioli's double entry, 1494, and how to read", 22, I.TEXT),
                     T("what a company's accounts say about its business.", 22, I.TEXT)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to(RIGHT * 2.6)
        with self.voiceover(
            "This part measured whole industries. The next one goes inside a single company. In 1494 a Franciscan "
            "friar, Luca Pacioli, printed the method merchants used to keep their books, and every company still "
            "uses it. Part three: the accounts, and what they say about the business underneath."
        ):
            self.play(FadeIn(g, shift=UP * 0.1), run_time=1.5)
            self.play(FadeIn(cap, shift=LEFT * 0.1))
        self.wait(1.0)
        self.clear_scene()
