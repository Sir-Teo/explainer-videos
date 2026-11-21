from __future__ import annotations

from videos.economics.econ59.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 16, r"Frontier: \ platforms, \ data and nascent rivals", r"How do you predict the effect of "
             r"buying a firm that has no prices \ and few sales?", "Chapter sixteen. Frontier: platforms, data and "
             "nascent rivals.", lit={2012: r"Instagram", 2025: r"FTC v. Meta"}, scale=("firm", "world"),
             horizon=("a decade",))
        self.meta()
        self.open_()

    def meta(self):
        rows = VGroup(
            history_card(2012, r"Facebook buys Instagram", r"\$1 billion for an app with tens of millions of users, "
                         r"\ about a dozen employees, \ and no revenue", color=ALDER,
                         width=11.6, font_size=20),
            history_card(2020, r"the FTC sues", r"the purchases of Instagram and WhatsApp, \ it said, \ neutralized "
                         r"rivals to keep a monopoly in personal social networking", color=GOV, width=11.6,
                         font_size=20),
            history_card(2025, r"Judge James Boasberg, \ 18 November", r"TikTok and YouTube belong in the market; \ "
                         r"the FTC had not shown that Meta holds monopoly power now", color=E.ACCENT, width=11.6,
                         font_size=20),
        ).arrange(DOWN, buff=0.35).move_to(UP * 0.3)
        lesson = label(r"the case turned on chapter three: \ where does the market end?", font_size=22,
                       color=CEDAR).next_to(rows, DOWN, buff=0.45)
        tag = published_tag(r"FTC v. Meta Platforms (D.D.C.), \ decision of 18 November 2025, \ as reported by NPR "
                            r"and NBC", corner=DL, font_size=12)
        with self.voiceover(
            "The hardest mergers to judge are purchases of small firms that might have become big rivals. "
            "<bookmark mark='a'/> In 2012 Facebook bought Instagram for a billion dollars. Instagram had about a "
            "dozen employees and no revenue; there were no prices to regress and no diversion to measure. "
            "<bookmark mark='b'/> In 2020 the Federal Trade Commission sued, arguing that the purchases of "
            "Instagram and WhatsApp had neutralized rivals to protect a monopoly in personal social networking. "
            "<bookmark mark='c'/> In November 2025 Judge James Boasberg ruled for Meta. TikTok and YouTube, he "
            "found, compete for the same users' time, and with them in the market the FTC had not shown that Meta "
            "holds monopoly power today. <bookmark mark='d'/> A case about the future of social media turned, in "
            "the end, on chapter three's question: where does the market end, when the price is zero and what is "
            "sold is attention?"
        ) as vo:
            self.play(FadeIn(tag))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(lesson))
        self.clear_scene()

    def open_(self):
        cards = point_cards([
            (r"zero prices", r"the test becomes a small but significant fall in quality: \ privacy, \ ads, \ "
             r"features; \ hard to measure, \ harder to defend in court", CEDAR),
            (r"series of acquisitions", r"many small purchases, \ none reportable alone; \ the 2023 guidelines "
             r"ask about the pattern", GOV),
            (r"data and ecosystems", r"a merger that joins data or locks users into a bundle; \ remedies of "
             r"access and interoperability", BIRCH),
            (r"better instruments", r"demand estimated from experiments and choice data; \ retrospective "
             r"programmes that score the tools, \ as chapter twelve did", SIM),
        ], width=12.6, cols=2, font_size=20).move_to(UP * 0.2)
        hard = label(r"what remains hard: \ the counterfactual of a rival that never got the chance to grow",
                     font_size=21, color=CARTEL).next_to(cards, DOWN, buff=0.45)
        head = label(r"what remains open", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.4)
        with self.voiceover(
            "What remains open? <bookmark mark='a'/> Zero prices. The hypothetical monopolist cannot raise a price of "
            "nothing, so the test becomes a small but significant fall in quality: more ads, less privacy, fewer "
            "features. It is hard to measure and harder to defend before a judge. <bookmark mark='b'/> Series of "
            "acquisitions: many small purchases, none worth reporting alone, which together build a position; the "
            "2023 guidelines ask about the pattern. <bookmark mark='c'/> Data and ecosystems: mergers that join data "
            "sets or tie users into bundles, where the remedies are access and interoperability rather than selling "
            "stores. <bookmark mark='d'/> And better instruments: demand estimated from experiments and choice data, "
            "and agencies that run retrospectives as a programme, to score their own tools. <bookmark mark='e'/> "
            "What remains hardest is the counterfactual of a rival that never got the chance to grow. No regression "
            "of prices can see it, and an expert who claims certainty about it should be cross-examined hardest of "
            "all."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(hard))
        self.clear_scene()
