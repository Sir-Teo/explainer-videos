from __future__ import annotations

from explainer.industry import QUESTIONS
from videos.industry.industry1.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.answers()
        self.next_part()

    def answers(self):
        D = R["dollar17"]
        ans = [
            "A pocket computer, sold at a price the brand sets; six in ten through carriers and resellers.",
            "Six layers from companies in six economies. One more costs about $590; designing the next costs billions.",
            f"Of $1,099: about 47 cents of each dollar to the parts, 3 to assembly, 22 to Apple's profit.",
            "To the links that are hardest to replace: the brand and its software, the leading-edge chip, patents.",
            "Scarcity. In 2026 memory became the scarce link, and its makers' margins doubled.",
        ]
        rows = VGroup()
        for (k, q), a in zip(QUESTIONS, ans):
            r = VGroup(TB(q, 22, I.ACCENT), T(a, 21, I.TEXT)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            if r.width > 12.6:
                r.scale_to_fit_width(12.6)
            rows.add(r)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(UP * 0.3).align_to(LEFT * 6.3, LEFT)
        head = TB("The five questions, answered for the phone", 26, I.DIM).to_edge(UP, buff=0.35)
        verdict = VGroup(T("When you pay for a phone, the money goes to whoever is hardest to replace,", 25, I.MONEY),
                         T("and that can change in a single year.", 25, I.MONEY)).arrange(DOWN, buff=0.08
                                                                                         ).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The five questions, answered for the phone. <bookmark mark='a'/> What is sold? A computer that fits in "
            "a pocket, at a price the brand sets, six in ten of them through carriers and resellers. <bookmark "
            "mark='b'/> How is it made? From six layers made by companies in at least six economies; one more phone "
            "costs Apple about 590 dollars, while designing the next one costs billions. <bookmark mark='c'/> Where "
            "does the dollar go? About 47 cents of each to the parts, three cents to assembly, 22 cents to Apple's "
            "profit. <bookmark mark='d'/> Why does it stay there? Because the links that are hardest to replace, "
            "the brand and its software, the most advanced chips, the patents, keep the most. <bookmark mark='e'/> "
            "And what moves it? Scarcity. In 2026 memory became the scarce link, and its makers' margins doubled. "
            "<bookmark mark='f'/> So, to the question we started with: when you pay for a phone, the money goes to "
            "whoever is hardest to replace, and that can change in a single year."
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
        grid = VGroup()
        rng = np.random.default_rng(1936)
        n = 9
        for i in range(n):
            for j in range(n):
                v = rng.random() ** 3
                grid.add(Square(0.42, fill_color=I.ACCENT, fill_opacity=0.08 + 0.8 * v, stroke_color="#0E1117",
                                stroke_width=1.2).move_to(np.array([(j - n / 2) * 0.42, (n / 2 - i) * 0.42, 0])))
        grid.move_to(LEFT * 3.2)
        cap = VGroup(T("Next", 22, I.DIM), TB("Part 2 · The Economy on One Page", 32, I.TEXT),
                     T("Wassily Leontief's table of who buys from whom, 1936,", 22, I.TEXT),
                     T("and how big each industry is, measured three ways.", 22, I.TEXT)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to(RIGHT * 2.9)
        with self.voiceover(
            "A phone is one product. In the next part we zoom out to every industry at once, using a table that "
            "Wassily Leontief built in 1936 to show who buys from whom across a whole economy, and we will find that "
            "the size of an industry depends on how you measure it. That's Part two: the economy on one page."
        ):
            self.play(LaggedStart(*[FadeIn(s) for s in grid], lag_ratio=0.01), run_time=2.5)
            self.play(FadeIn(cap, shift=LEFT * 0.1))
        self.wait(1.0)
        self.clear_scene()
