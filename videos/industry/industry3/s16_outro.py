from __future__ import annotations

from explainer.industry import QUESTION_SHORT, QUESTIONS
from videos.industry.industry3.common import *  # noqa: F403

ANSWERS = {
    "unit": "A dollar of the owners' money: what it earns a year is the score",
    "make": "Operations become statements: every sale, purchase and loan is an entry, written twice",
    "dollar": "The income statement: Costco keeps 4 cents of a dollar, Microsoft 47, a bank about 31",
    "moat": "A return on capital above its cost, for years: patents, habits, members, networks",
    "change": "Cash, not profit, decides who survives growth and downturns; read the gap",
}


class Outro(VoiceoverScene):
    def construct(self):
        rows = VGroup()
        for i, (k, _) in enumerate(QUESTIONS):
            y = 1.8 - i * 0.8
            nm = TB(QUESTION_SHORT[k], 22, I.ACCENT).move_to(np.array([-3.0, y, 0]), aligned_edge=RIGHT)
            ans = T(ANSWERS[k], 21, I.TEXT).move_to(np.array([-2.7, y, 0]), aligned_edge=LEFT)
            if ans.width > 9.5:
                ans.scale_to_fit_width(9.5).move_to(np.array([-2.7, y, 0]), aligned_edge=LEFT)
            rows.add(VGroup(nm, ans))
        head = T("The accounts, in five answers", 26, I.TEXT).to_edge(UP, buff=0.45)
        with self.voiceover(
            "So, what do a company's accounts say about the business underneath? <bookmark mark='a'/> They measure "
            "what a dollar of the owners' money earns. <bookmark mark='b'/> They are built from the operations, "
            "every sale and purchase written down twice. <bookmark mark='c'/> They show where each dollar of sales "
            "goes: to the goods, the people, the research, the machines, and the owners. <bookmark mark='d'/> They "
            "show whether a business earns more on its capital than that capital costs, which is the real test of a "
            "lasting advantage. <bookmark mark='e'/> And the gap between profit and cash is where trouble shows "
            "first, from a fast-growing bakery to Enron."
        ) as vo:
            self.play(FadeIn(head))
            for i, m in enumerate("abcde"):
                vo.wait_until(m)
                self.play(FadeIn(rows[i], shift=RIGHT * 0.1))
        self.clear_scene()
        nxt = VGroup(T("Next", 24, I.DIM), TB("Part 4 · The Cost Curve", 40, I.TEXT),
                     T("What does one more cost, and why does that decide almost everything?", 24, I.TEXT,
                       slant="ITALIC")).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "This part read the accounts. The next one looks at the costs behind them. In 1936 an aircraft engineer, "
            "T. P. Wright, measured how the work needed to build an aeroplane fell each time the number built "
            "doubled. Part four: the cost curve. Why power stations, airlines and memory makers price the way they "
            "do, why some industries fight price wars to the death, and why what one more costs decides almost "
            "everything."
        ):
            self.play(FadeIn(nxt, shift=UP * 0.15), run_time=1.5)
        self.wait(1)
        self.clear_scene()
