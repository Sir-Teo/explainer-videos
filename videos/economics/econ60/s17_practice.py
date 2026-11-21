from __future__ import annotations

from videos.economics.econ60.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 15, r"In practice: \ pricing teams", r"Who sets prices inside a firm, \ and what tools do they use?",
             "Chapter fifteen. In practice: pricing teams.", lit={2012: r"J.C. Penney"}, scale=("firm",),
             horizon=("a day", "a year"))
        self.teams()
        self.called()

    def teams(self):
        cards = point_cards([
            (r"airlines and hotels", r"revenue management analysts: \ forecasts, \ fare classes, \ overbooking, \ "
             r"and the software that runs every night", AIR),
            (r"retail", r"pricing and promotion teams: \ elasticities by category, \ the promotion calendar, \ "
             r"zone or uniform prices", SHOP),
            (r"software and subscriptions", r"packaging into tiers, \ seats against usage, \ price experiments and "
             r"their interference", LEIS),
            (r"business sales", r"deal desks: \ list prices, \ discount authority, \ and the dispersion of what "
             r"customers actually pay", FIRM),
        ], width=12.6, cols=2, font_size=20).move_to(DOWN * 0.2)
        head = label(r"where prices are set", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Pricing is a job. <bookmark mark='a'/> Airlines and hotels employ revenue management analysts who "
            "forecast demand, design fare classes and overbooking rules, and supervise software that reprices "
            "every flight every night. <bookmark mark='b'/> Retailers have pricing and promotion teams that estimate "
            "elasticities category by category, plan the promotion calendar, and choose between zone prices and "
            "one price for all. <bookmark mark='c'/> Software firms decide how to package tiers, whether to charge "
            "per seat or per use, and run price experiments, watching for the interference of chapter three. "
            "<bookmark mark='d'/> And firms selling to businesses run deal desks that set list prices, decide who "
            "may grant which discount, and try to keep what customers actually pay from drifting apart."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["jcpenney_2012"]
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.6,
                       font_size=17)
        cc.move_to(UP * 0.9)
        lesson = VGroup(
            label(r"the reference price was part of the product: \ chapter nine", font_size=20, color=BUS),
            label(r"and a test in a few stores would have shown it for a fraction of the cost: \ chapter three",
                  font_size=20, color=E.ACCENT),
        ).arrange(DOWN, buff=0.3).next_to(cc, DOWN, buff=0.55)
        tag = published_tag(r"Fortune (2013); \ JCK (2013); \ Knowledge at Wharton (2012)", corner=DR, font_size=12)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> Ron Johnson, who had built Apple's stores, became chief executive of "
            "J.C. Penney late in 2011, and in January 2012 announced fair and square pricing: honest everyday prices "
            "instead of "
            "inflated list prices, constant sales and coupons. He expected shoppers to welcome it, and put it into "
            "every store at once rather than testing it first. <bookmark mark='b'/> In 2012 the company's sales "
            "fell by almost a quarter, to thirteen billion dollars. In April 2013 the board removed him, and the "
            "sales and coupons came back. <bookmark mark='c'/> The verdict: wrong. <bookmark mark='d'/> Chapter "
            "nine's shoppers explain part of it: for them the regular price was the reference that made a sale "
            "feel like a deal. <bookmark mark='e'/> And chapter three's tool would have shown it cheaply: a test "
            "in a few stores, for a few months."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1][0]), FadeIn(cc.left), FadeIn(tag))
            vo.wait_until("a")
            self.play(Indicate(cc.left, color=WHITE, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(cc.right))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3))
            vo.wait_until("d")
            self.play(FadeIn(lesson[0]))
            vo.wait_until("e")
            self.play(FadeIn(lesson[1]))
        self.clear_scene()
