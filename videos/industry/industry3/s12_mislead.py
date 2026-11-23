from __future__ import annotations

from explainer.industry.register import get
from videos.industry.industry3.common import *  # noqa: F403


def trap(title, figure, line1, line2, color, who):
    body = VGroup(TB(title, 21, color), TB(figure, 30, I.TEXT), T(line1, 15, I.TEXT), T(line2, 15, I.TEXT),
                  T(who, 14, I.DIM)).arrange(DOWN, aligned_edge=LEFT, buff=0.07)
    box = RoundedRectangle(corner_radius=0.12, width=4.05, height=2.45, fill_color=I.PANEL, fill_opacity=1,
                           stroke_color=color, stroke_width=1.6)
    if body.width > 3.8:
        body.scale_to_fit_width(3.8)
    body.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.2)
    return VGroup(box, body)


class Mislead(VoiceoverScene):
    def construct(self):
        card(self, 11, "Where the accounts mislead", "What do the statements leave out, or flatter?",
             "Chapter eleven. Where the accounts mislead.", lit=("moat", "change"))
        cards = VGroup(
            trap("Research is a cost", bn(get("lly.rd")), "Lilly's spending on the next medicines,",
                 "expensed at once: no asset on the books", CO["lly"], "Eli Lilly, 2025"),
            trap("Pay in shares", bn(get("msft.sbc")), "a real cost in profit; added back in cash,",
                 "paid for by diluting the owners", CO["msft"], "Microsoft, fiscal 2026"),
            trap("Gains on paper", bn(get("msft.openai")), "net gains on OpenAI, mostly from its",
                 "recapitalization: in profit, not in cash", CO["msft"], "Microsoft, fiscal 2026"),
            trap("Goodwill", bn(get("msft.goodwill")), "what was paid for companies bought,",
                 "above the value of their own assets", CO["msft"], "Microsoft, 30 June 2026"),
            trap("The company's own measures", f"{get('dal.casm_ex'):.2f}¢ vs {get('dal.casm'):.2f}¢",
                 "cost per seat mile 'excluding fuel and", "other items' against the full cost", CO["dal"],
                 "Delta, 2025"),
            trap("Estimates", bn(get("jpm.provision")), "set aside for loans expected to go bad:",
                 "a forecast, booked as a cost", CO["jpm"], "JPMorgan Chase, 2025"),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.3, 0.35)).move_to(DOWN * 0.25)
        head = T("Six places to read with care", 24, I.TEXT).to_edge(UP, buff=0.3)
        src = source("Forms 10-K: Eli Lilly 2025, Microsoft FY2026, Delta 2025, JPMorgan Chase 2025", size=13)
        with self.voiceover(
            "Accounts are rules, and rules leave gaps. Six to watch for, each from this part's companies. "
            f"<bookmark mark='a'/> Research. Lilly spent {say_bn(get('lly.rd'))} in 2025 on finding the next "
            "medicines. The rules count all of it as a cost in the year it is spent, so the most valuable things "
            "Lilly owns, its future drugs, appear nowhere on its balance sheet. <bookmark mark='b'/> Pay in shares. "
            f"Microsoft gave its employees {say_bn(get('msft.sbc'))} of stock in fiscal 2026. It is a cost in the "
            "income statement but no cash leaves, so it is added back in the cash-flow statement; the owners pay "
            "instead, as their share of the company is diluted. <bookmark mark='c'/> Gains on paper. Microsoft's "
            f"net income included {say_bn(get('msft.openai'))} of net gains from its investment in OpenAI, mostly "
            "because OpenAI reorganized and raised money from others. Real, perhaps, but not cash, and not from "
            f"selling software. <bookmark mark='d'/> Goodwill: {say_bn(get('msft.goodwill'))} on Microsoft's "
            "balance sheet, the premium it paid for companies like LinkedIn and Activision Blizzard over the value "
            "of their own assets. It cannot be sold on its own, and if an acquisition disappoints, it is written "
            "down. <bookmark mark='e'/> The company's own measures. Delta reports its cost per seat mile, "
            f"{get('dal.casm'):.2f} cents, and also an adjusted one that leaves out fuel and some other items, "
            f"{get('dal.casm_ex'):.2f} cents. Both are useful; only one is the cost. Always find the reconciliation. "
            f"<bookmark mark='f'/> And estimates. JPMorgan booked {say_bn(get('jpm.provision'))} for loans it "
            "expects to go bad. That is a forecast, and a bank that is too hopeful will look more profitable than it "
            "is, until the loans fail."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            for i, m in enumerate("abcdef"):
                vo.wait_until(m)
                self.play(FadeIn(cards[i], shift=UP * 0.1))
        self.clear_scene()
