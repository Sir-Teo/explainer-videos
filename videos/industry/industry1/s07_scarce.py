from __future__ import annotations

from explainer.industry.register import get
from videos.industry.industry1.common import *  # noqa: F403


class Scarce(VoiceoverScene):
    def construct(self):
        card(self, 6, "Why the profit sits where it does", "Why does Apple keep 244 dollars and the factory 30?",
             "Chapter six. Why the profit sits where it does.", lit=("moat",))
        self.margin()
        self.ladder()
        self.groups()
        self.designed_away()

    def margin(self):
        bar = Rectangle(width=8.0, height=0.8, fill_color=I.MONEY, fill_opacity=0.2, stroke_color=I.MONEY,
                        stroke_width=2).shift(UP * 0.6)
        cost = Rectangle(width=8.0 * 0.6, height=0.8, fill_color=I.COST, fill_opacity=0.75, stroke_width=0
                         ).align_to(bar, LEFT).set_y(bar.get_y())
        keep = Rectangle(width=8.0 * 0.4, height=0.8, fill_color=I.PROFIT, fill_opacity=0.85, stroke_width=0
                         ).next_to(cost, RIGHT, buff=0)
        l0 = T("A dollar a company is paid", 22, I.TEXT).next_to(bar, UP, buff=0.18)
        l1 = T("what it costs to make", 20, I.TEXT).move_to(cost)
        l2 = T("kept: the margin", 20, "#0E1117").move_to(keep)
        note = VGroup(T("Gross margin: after the direct cost of making the product", 20, I.DIM),
                      T("Operating margin: after research, selling and overheads too", 20, I.DIM)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).next_to(bar, DOWN, buff=0.6)
        with self.voiceover(
            "To see why, we need one word: margin. <bookmark mark='a'/> Take a dollar that a company is paid for "
            "what it sells. <bookmark mark='b'/> Part of it covers the direct cost of making the thing. <bookmark "
            "mark='c'/> What is left is the margin: the share of each dollar the company keeps. <bookmark mark='d'/> "
            "Companies report it at different depths. Gross margin is what is left after the cost of making the "
            "product; operating margin is what is left after research, selling and overheads as well. Every company "
            "in the phone's chain publishes one or the other, and the numbers tell a story."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(bar), FadeIn(l0))
            vo.wait_until("b")
            self.play(GrowFromEdge(cost, LEFT), FadeIn(l1))
            vo.wait_until("c")
            self.play(GrowFromEdge(keep, LEFT), FadeIn(l2))
            vo.wait_until("d")
            self.play(FadeIn(note, shift=UP * 0.1))
        self.clear_scene()

    def ladder(self):
        items = [
            ("Apple, services", get("apple.gm_services.fy2026"), I.BRAND, "gross · FY2026"),
            ("Qualcomm, patent licensing", get("qcom.qtl_ebt.fy2026"), I.RF, "pre-tax · FY2026"),
            ("TSMC, chips", get("tsmc.gm.q4_2025"), I.CHIP, "gross · Q4 2025"),
            ("Micron, memory", get("micron.gm.fy2025"), I.MEMORY, "gross · FY2025"),
            ("Apple, products", get("apple.gm_products.fy2025"), I.BRAND, "gross · FY2025"),
            ("Corning, glass", get("corning.gm.2025"), I.CASE, "gross · 2025"),
            ("Transsion, phones", get("transsion.gm.2025"), "#8B95A7", "gross · 2025"),
            ("Sony, image sensors", get("sony.iss_opm.fy2025"), I.CAMERA, "operating · FY2025"),
            ("Xiaomi, smartphones", get("xiaomi.phone_gm.2025"), "#8B95A7", "gross · 2025"),
            ("Samsung, mobile", get("samsung.mx_opm.2025"), "#8B95A7", "operating · 2025"),
            ("Foxconn, assembly", get("foxconn.gm.2025"), I.ASSEMBLY, "gross · 2025"),
        ]
        rows = viz.margin_ladder(items, max_value=0.8, bar_len=5.4, row_h=0.52, size=21, name_w=4.4)
        rows.move_to(RIGHT * 0.9 + DOWN * 0.3)
        head = T("Of each dollar it is paid, what each link keeps", 26, I.TEXT).to_edge(UP, buff=0.5)
        src = source("10-K, 20-F and annual results of each company (the Register, Part 1)")
        stamp = as_of("2025 / fiscal 2026")
        with self.voiceover(
            "Here are the margins of the companies in the chain, from their own reports for 2025 or their latest "
            "fiscal year, before the shock that hit memory in 2026. <bookmark mark='a'/> At the bottom, Foxconn, "
            "the assembler: about 6 cents of gross margin on each dollar of sales. Samsung's and Xiaomi's phone "
            "businesses keep about 10 or 11. <bookmark mark='b'/> In the middle, the makers of parts: Sony's image "
            "sensors, Corning's glass, Micron's memory, keeping roughly 17 to 40 cents. <bookmark mark='c'/> And at "
            "the top: TSMC, the chip maker, keeps 62 cents of each dollar before overheads. Qualcomm's patent "
            "licensing business keeps 72 cents even after its own costs. And Apple's services, the App Store, "
            "iCloud, the payments Google makes to be the default search engine, keep 76 cents."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(stamp))
            self.play(LaggedStart(*[FadeIn(r[0]) for r in rows], lag_ratio=0.05), *[FadeIn(r[1]) for r in rows])
            vo.wait_until("a")
            self.play(*[AnimationGroup(GrowFromEdge(r[2], LEFT), FadeIn(r[3])) for r in rows[-3:]], run_time=1.4)
            vo.wait_until("b")
            self.play(*[AnimationGroup(GrowFromEdge(r[2], LEFT), FadeIn(r[3])) for r in rows[3:8]], run_time=1.6)
            vo.wait_until("c")
            self.play(*[AnimationGroup(GrowFromEdge(r[2], LEFT), FadeIn(r[3])) for r in rows[:3]], run_time=1.6)
        self.clear_scene()

    def groups(self):
        cols = [
            ("Hard to replace", I.PROFIT, [("TSMC: the only maker of Apple's processor", get("tsmc.gm.q4_2025")),
                                           ("Qualcomm's patents: licensed by every maker", get("qcom.qtl_ebt.fy2026")),
                                           ("Apple's iOS and App Store", get("apple.gm_services.fy2026"))]),
            ("A few rivals", I.MONEY, [("Memory: three big makers", get("micron.gm.fy2025")),
                                       ("Glass: Corning", get("corning.gm.2025")),
                                       ("Image sensors: Sony and two others", get("sony.iss_opm.fy2025"))]),
            ("Many rivals", I.COST, [("Assembly: Foxconn, Luxshare, Tata ...", get("foxconn.gm.2025")),
                                     ("Android phones: dozens of brands", get("xiaomi.phone_gm.2025")),
                                     ("Budget phones: Transsion", get("transsion.gm.2025"))]),
        ]
        blocks = VGroup()
        for title, c, rows in cols:
            head = TB(title, 28, c)
            body = VGroup()
            for name, v in rows:
                bar = Rectangle(width=max(3.4 * v / 0.8, 0.05), height=0.26, fill_color=c, fill_opacity=0.85,
                                stroke_width=0)
                body.add(VGroup(T(name, 17, I.TEXT), VGroup(bar, TB(pct(v), 18, c)).arrange(RIGHT, buff=0.12))
                         .arrange(DOWN, aligned_edge=LEFT, buff=0.08))
            body.arrange(DOWN, aligned_edge=LEFT, buff=0.32)
            blocks.add(VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.35))
        blocks.arrange(RIGHT, buff=0.6, aligned_edge=UP)
        if blocks.width > 13.0:
            blocks.scale_to_fit_width(13.0)
        blocks.move_to(UP * 0.2)
        rule = T("The link that is hardest to replace keeps the most.", 28, I.ACCENT).to_edge(DOWN, buff=0.55)
        with self.voiceover(
            "Sort the links by a different question: if this company stopped selling to Apple tomorrow, how many "
            "others could take its place? <bookmark mark='a'/> For Apple's main processor, on the newest "
            "manufacturing process, at Apple's volumes, the answer today is one: TSMC. Qualcomm's patents cover the "
            "standards every phone must speak, so every phone maker needs a licence. And the App Store is the only "
            "way to sell an app to the iPhone's users. <bookmark mark='b'/> For memory, there are three big makers; "
            "for image sensors, Sony and a couple of rivals; for glass, Corning and a few others. <bookmark "
            "mark='c'/> For assembly there are several firms with the skill and the scale, and Apple has moved "
            "work between them; and there are dozens of brands making Android phones. <bookmark mark='d'/> The "
            "pattern in the margins follows the pattern in the answers. The link that is hardest to replace keeps "
            "the most. Economists call this bargaining power; the business literature calls it a moat. Part five of "
            "this series is about moats."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(blocks[0], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(blocks[1], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(blocks[2], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(rule, shift=UP * 0.1))
        self.clear_scene()

    def designed_away(self):
        line = VGroup()
        for yr, what, c in ((2010, "A4: its own processor", I.CHIP), (2025, "C1: its own modem", I.RF),
                            (2025, "N1: its own wireless chip", I.RF)):
            line.add(VGroup(TB(str(yr), 26, c), T(what, 24, I.TEXT)).arrange(RIGHT, buff=0.3))
        line.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(UP * 1.4 + LEFT * 2.0)
        head = T("Apple has been replacing bought chips with its own", 24, I.DIM).next_to(line, UP, buff=0.35
                                                                                         ).align_to(line, LEFT)
        q = VGroup(T("“Our business, particularly our semiconductor business, may suffer as a result of our", 20,
                     I.TEXT), T("customers vertically integrating (i.e., developing their own integrated circuit "
                     "products).”", 20, I.TEXT), T("Qualcomm, Form 10-K, fiscal 2026, risk factors", 17, I.DIM)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to(DOWN * 1.2)
        tail = T("A scarce link can be designed away, and a plentiful one can become scarce: chapter 9.", 22,
                 I.ACCENT).to_edge(DOWN, buff=0.5)
        src = source("Apple Newsroom (2010, 2025); Qualcomm Form 10-K FY2026", corner=UR)
        with self.voiceover(
            "The power is not permanent, because the customer fights back. <bookmark mark='a'/> In 2010 Apple put "
            "its own processor in the iPhone, the A4. In 2025 it began replacing Qualcomm's modem with its own, "
            "called C1, and its suppliers' wireless chip with its own, called N1. <bookmark mark='b'/> Qualcomm "
            "lists this as a risk in its annual report: its business may suffer if customers develop their own "
            "chips. <bookmark mark='c'/> A scarce link can be designed away. And, as we will see in chapter nine, "
            "a plentiful link can suddenly become scarce."
        ) as vo:
            self.play(FadeIn(src), FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.15) for x in line], lag_ratio=0.5), run_time=2.4)
            vo.wait_until("b")
            self.play(FadeIn(q, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(tail))
        self.clear_scene()
