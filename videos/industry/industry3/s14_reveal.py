from __future__ import annotations

from videos.industry.industry3.common import *  # noqa: F403
from videos.industry.industry3.s02_match import table
from videos.industry.industry3.s03_ledger import _bank
from videos.industry.industry3.s04_income import _glyph

WHY = {"nee": "new equipment worth 88 cents per dollar of sales: plants built ahead of decades of bills",
       "cost": "three dollars of sales for every dollar it owns, on a margin of under four cents",
       "lly": "twenty cents of each dollar on research, and a fat margin on what the research found",
       "jpm": "twelve dollars of assets per dollar of its owners' money: deposits and borrowing",
       "dal": "a thin margin, heavy equipment and plenty of borrowing: an airline",
       "msft": "the fattest margin, and 35 cents of each dollar now going into data centres"}


class Reveal(VoiceoverScene):
    def construct(self):
        card(self, 13, "The six, revealed", "Which company was which, and how could you tell?",
             "Chapter thirteen. The six, revealed.", lit=("dollar", "moat"))
        t0 = table(False).scale(0.84, about_point=ORIGIN).shift(UP * 0.55)
        t1 = table(True).scale(0.84, about_point=ORIGIN).shift(UP * 0.55)
        heads1 = t1[0]
        why = VGroup()
        for i, c in enumerate(R["cards"]):
            why.add(VGroup(TB(f"{c['letter']}  {name(c['key'])}:", 17, CO[c["key"]]), T(WHY[c["key"]], 17, I.TEXT)
                           ).arrange(RIGHT, buff=0.15))
        why.arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_edge(DOWN, buff=0.3)
        for w in why:
            if w.width > 13:
                w.scale_to_fit_width(13)
        head = T("The answers", 22, I.DIM).to_edge(UP, buff=0.3)
        C = R["cards"]
        say = {c["key"]: c["letter"] for c in C}
        with self.voiceover(
            "Back to the six companies with no names. <bookmark mark='a'/> Company "
            f"{say['cost']}, turning over its assets three times a year on a margin of under four cents, is Costco. "
            f"<bookmark mark='b'/> Company {say['jpm']}, with twelve dollars of assets on every dollar of its "
            f"owners' money, is the bank, JPMorgan. <bookmark mark='c'/> Company {say['nee']}, spending 88 cents "
            "of every dollar of sales on new equipment and turning over its assets only once every eight years, is "
            f"the power company, NextEra. <bookmark mark='d'/> Company {say['lly']}, putting twenty cents of each "
            f"dollar into research, is Eli Lilly. <bookmark mark='e'/> Company {say['msft']}, with the fattest "
            "margin and thirty-five cents of every dollar now going into data centres, is Microsoft. <bookmark "
            f"mark='f'/> And company {say['dal']}, thin margin, heavy equipment and plenty of borrowing, is Delta. "
            "If you got most of them, you can already read the shape of a business from its accounts. If you "
            "did not, look again at the two numbers that gave most of them away: the speed and the borrowing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(t0))
            order = ["cost", "jpm", "nee", "lly", "msft", "dal"]
            for m, k in zip("abcdef", order):
                vo.wait_until(m)
                i = [c["key"] for c in C].index(k)
                g_ = (_bank() if k == "jpm" else _glyph(k))
                g_.scale_to_fit_height(min(g_.height, 0.42)).next_to(heads1[i], UP, buff=0.12)
                self.play(Transform(t0[0][i], heads1[i]), FadeIn(why[i], shift=UP * 0.05), FadeIn(g_, scale=1.4))
        self.clear_scene()
