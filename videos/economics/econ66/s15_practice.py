from __future__ import annotations

from videos.economics.econ66.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 13, r"In practice: \ ministries, \ supply chains, \ sanctions", r"Where is this economics used, "
             r"\ and what goes wrong?", "Chapter thirteen. In practice: ministries, supply chains, sanctions.",
             scale=("firm", "nation"), horizon=("a year",))
        self.called()
        self.jobs()
        self.cautions()

    def called(self):
        Fo = load("fomc")
        c = calls.CALLS["fomc_2025"]
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.6,
                       font_size=17)
        cc.move_to(UP * 0.5)
        lesson = label(r"forecasting a tariff's inflation means forecasting how fast it reaches the shelf",
                       font_size=21, color=E.ACCENT).next_to(cc, DOWN, buff=0.5)
        tag = data_tag(rf"BEA via FRED: \ PCEPILFE \ (retrieved {Fo['retrieved']}); \ FOMC, \ 18 June 2025",
                       corner=DL, font_size=12)
        with self.voiceover(
            "Forecasting what tariffs do to prices is a job, and it starts with a call. Called it? <bookmark "
            "mark='a'/> In June 2025 the median member of the Federal Reserve's policy committee projected core "
            f"inflation of {100 * Fo['projected_june']:.1f} percent for 2025, up from "
            f"{100 * Fo['projected_march']:.1f} in March, as the tariffs reached prices. <bookmark mark='b'/> The "
            f"outcome: core prices rose {100 * Fo['outcome']:.1f} percent from the end of 2024 to the end of 2025. "
            "Goods prices did turn up, but the tariffs reached shelves slowly, and some were cut or suspended. "
            "<bookmark mark='c'/> Partly right: the direction, not the size. <bookmark mark='d'/> The lesson of "
            "chapter one, again: a tariff's effect on inflation depends on how fast it travels from the border to "
            "the shelf."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1][0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(cc.left))
            vo.wait_until("b")
            self.play(FadeIn(cc.right))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.4))
            vo.wait_until("d")
            self.play(FadeIn(lesson))
        self.clear_scene()

    def jobs(self):
        cards = point_cards([
            (r"trade ministries", r"quantitative trade models like chapter four's to score a tariff or an "
             r"agreement: \ revenue, \ prices, \ who gains and loses", US),
            (r"budget offices", r"a tariff's revenue, \ net of the imports it stops and the income it lowers \ "
             r"(Part 58's scoring)", PRICE),
            (r"supply-chain strategy", r"a second supplier, \ inventories, \ where to build: \ chapter seven's "
             r"trade-off, \ priced by each firm", ROW),
            (r"sanctions compliance", r"banks and firms screening every payment and shipment against lists: \ the "
             r"hub's power, \ run by its users", TARIFF),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.2)
        head = label(r"where geoeconomics is a job", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Where is this used? <bookmark mark='a'/> In trade ministries, which score a tariff or an agreement "
            "with quantitative models like chapter four's: revenue, prices, and who gains and loses. <bookmark "
            "mark='b'/> In budget offices, which score a tariff's revenue net of the imports it stops and the "
            "income it lowers, Part fifty-eight's craft. <bookmark mark='c'/> In companies, which price chapter "
            "seven's trade-off for themselves: a second supplier, larger inventories, where to build the next "
            "factory. <bookmark mark='d'/> And in sanctions compliance, where banks and firms screen every payment "
            "and shipment against government lists: the hub's power, run by the hub's users."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def cautions(self):
        head = label(r"three cautions from this part", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        rows = VGroup(
            VGroup(label(r"1. \ A tariff is a tax, \ paid mostly at home", font_size=26, color=PRICE),
                   label(r"in the first years at least; \ any gain from the terms of trade comes late and invites "
                         r"answers", font_size=19, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
            VGroup(label(r"2. \ A bilateral balance is not a scorecard", font_size=26, color=US),
                   label(r"the overall balance is saving minus investment; \ the bilateral ones are mostly "
                         r"specialization", font_size=19, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
            VGroup(label(r"3. \ Industrial policy needs a test", font_size=26, color=FREE),
                   label(r"temporary, \ disciplined by exports, \ aimed at learning that spills over, \ and "
                         r"evaluated", font_size=19, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(head, DOWN, buff=0.7)
        with self.voiceover(
            "Three cautions from this part. <bookmark mark='a'/> A tariff is a tax, paid mostly at home, at least "
            "in the first years; any gain from the terms of trade comes late and invites answers. <bookmark "
            "mark='b'/> A bilateral balance is not a scorecard: the overall balance is saving minus investment, and "
            "the bilateral ones mostly reflect who is good at what. <bookmark mark='c'/> And industrial policy needs "
            "a test: temporary, disciplined by having to sell abroad, aimed at learning that spills over, and "
            "evaluated by a design, not by the industry's own account."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r_ in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.15))
        self.clear_scene()
