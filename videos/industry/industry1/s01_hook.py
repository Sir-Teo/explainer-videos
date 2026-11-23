from __future__ import annotations

from videos.industry.industry1.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.ipod_open()
        self.ipod_money()
        self.title()
        self.five()

    def ipod_open(self):
        P = R["ipod"]
        place = T("Irvine, California  ·  2007", 26, I.DIM).to_edge(UP, buff=0.6)
        dev = ipod(3.4).shift(LEFT * 4.4)
        back = RoundedRectangle(corner_radius=0.24, width=2.04, height=3.4, fill_color="#C9CED6", fill_opacity=1,
                                stroke_color="#9EA4AE", stroke_width=2).shift(LEFT * 1.5)
        engrave = VGroup(T("Designed by Apple", 15, "#3B4250"), T("in California", 15, "#3B4250"),
                         T("Assembled in China", 15, "#3B4250")).arrange(DOWN, buff=0.06).move_to(back).shift(DOWN * 0.9)
        tag = price_tag(money(P["price"]), 36).next_to(dev, DOWN, buff=0.35)
        stats = VGroup(T("Trade statistics:", 24, I.DIM), TB(f"import from China, {money(P['inputs'], 2)}", 26,
                       REGION["China"])).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(RIGHT * 3.6)
        src = source("Linden, Kraemer and Dedrick (2007), Who Captures Value in a Global Innovation System?")
        with self.voiceover(
            "In 2007, three researchers at the University of California, Irvine, set out to answer a simple "
            "question about a music player. <bookmark mark='a'/> Apple's fifth-generation iPod, the one with a "
            "thirty-gigabyte hard drive, sold in America for 299 dollars. <bookmark mark='b'/> Engraved on the back "
            "were two lines: designed by Apple in California, assembled in China. <bookmark mark='c'/> The trade "
            "statistics agreed with the label. When an iPod crossed the Pacific, its whole factory value was "
            "counted as an import from China. So who made it? <bookmark mark='d'/> The researchers, Greg Linden, "
            "Kenneth Kraemer and Jason Dedrick, did something different. They followed the money."
        ) as vo:
            self.play(FadeIn(place), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(dev, shift=UP * 0.2), run_time=1.2)
            self.play(FadeIn(tag, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(back), Write(engrave), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(stats, shift=LEFT * 0.2))
            vo.wait_until("d")
            self.play(Indicate(tag, color=I.MONEY, scale_factor=1.1))
        self.clear_scene(src)
        self.src = src

    def ipod_money(self):
        P = R["ipod"]
        items = [("retail", "Retail", P["retail"], I.CHANNEL), ("dist", "Distribution", P["distribution"], "#D98C4A"),
                 ("apple", "Apple", P["apple"], I.BRAND), ("drive", "Hard drive (Toshiba)", P["drive"], REGION["Japan"]),
                 ("display", "Display", P["display"], I.DISPLAY), ("broadcom", "Chip (Broadcom)", P["broadcom"], I.CHIP),
                 ("other", "Other parts", P["other_inputs"], I.OTHER), ("asm", "Assembly", P["assembly"], REGION["China"])]
        bar = viz.bar_split([(n, a, c) for _, n, a, c in items], P["price"], width=12.4, height=0.9).shift(UP * 0.9)
        top = VGroup(TB(money(P["price"]), 40, I.MONEY), T("one video iPod, 2005", 24, I.DIM)).arrange(
            RIGHT, buff=0.3, aligned_edge=DOWN).next_to(bar, UP, buff=0.4)
        labs = VGroup()
        for (k, n, a, c), r in zip(items, bar):
            if k in ("asm", "broadcom"):
                labs.add(VGroup())
                continue
            lab = VGroup(TB(money(a), 22, c), T(n, 17, I.TEXT)).arrange(DOWN, buff=0.06)
            if lab.width > r.width - 0.08:
                lab.scale_to_fit_width(max(r.width - 0.08, 0.6))
            lab.next_to(r, DOWN, buff=0.2)
            labs.add(lab)
        asm = bar[-1]
        zoom = VGroup(TB(f"{money(P['assembly'], 2)}", 40, REGION["China"]),
                      T("assembly in China, by Inventec", 22, I.TEXT)).arrange(DOWN, buff=0.1)
        zoom.move_to(RIGHT * 3.4 + DOWN * 2.1)
        kept = VGroup(T("kept by the assembler, at its 3% margin:", 22, I.DIM),
                      TB("11 cents", 40, I.MONEY)).arrange(DOWN, buff=0.12).move_to(LEFT * 3.0 + DOWN * 2.2)
        link = Line(asm.get_bottom(), zoom.get_top(), color=REGION["China"], stroke_width=2)
        with self.voiceover(
            "Of the 299 dollars, <bookmark mark='a'/> about 75 went to the shops and the distributors that sold it, "
            f"and <bookmark mark='b'/> {int(P['apple'])} went to Apple. <bookmark mark='c'/> The rest, about 144 "
            "dollars, paid for the parts. The most expensive part by far was the hard drive, made by Toshiba of "
            "Japan, at 73 dollars. <bookmark mark='d'/> And the final assembly in China, the step the label named? "
            "3 dollars 70. <bookmark mark='e'/> Of that, the assembler, a Taiwanese company called Inventec, kept, "
            "by the authors' estimate, about 11 cents."
        ) as vo:
            pile = draw.coin_stack(12, 0.16).next_to(top, LEFT, buff=0.4)
            self.play(FadeIn(top), FadeIn(pile, shift=DOWN * 0.2))

            def pay(idx, n):
                flows = [draw.coin_flow(pile.get_top(), bar[i].get_center(), n=n, r=0.09, arc=0.6) for i in idx]
                self.add(*[c for c, _ in flows])
                self.play(*[a for _, a in flows], *[GrowFromEdge(bar[i], LEFT) for i in idx],
                          *[FadeIn(labs[i]) for i in idx], run_time=1.6)
                self.remove(*[c for c, _ in flows])
            vo.wait_until("a")
            pay((0, 1), 5)
            vo.wait_until("b")
            pay((2,), 6)
            vo.wait_until("c")
            pay((3, 4, 5, 6), 3)
            vo.wait_until("d")
            fac = draw.factory(1.3, color=REGION["China"]).next_to(zoom, RIGHT, buff=0.35)
            c_asm, a_asm = draw.coin_flow(pile.get_top(), asm.get_center(), n=1, r=0.07, arc=0.6)
            self.add(c_asm)
            self.play(a_asm, GrowFromEdge(asm, LEFT))
            self.remove(c_asm)
            self.play(Create(link), FadeIn(zoom, shift=DOWN * 0.1), FadeIn(fac, shift=UP * 0.1))
            self.play(Indicate(asm, scale_factor=1.6, color=REGION["China"]))
            vo.wait_until("e")
            dot = draw.coin(0.035).move_to(fac.get_center())
            self.play(FadeIn(kept, shift=UP * 0.1), FadeIn(dot, scale=4))
            self.play(dot.animate.move_to(kept[1].get_right() + RIGHT * 0.25), run_time=1.2)
        with self.voiceover(
            "The label, the trade statistics and the money gave three different answers to the question of who "
            "makes the thing. This series is about the third answer."
        ):
            self.play(Circumscribe(top, color=I.MONEY, time_width=0.8), run_time=2)
        self.clear_scene()

    def title(self):
        card_ = part_title(PART, ASK)
        with self.voiceover(
            "Industry, Built. Part one: where the money goes. When you pay for something, who gets the money, and "
            "why them? We will answer it for the object most of us touch first thing every morning: the phone."
        ):
            self.play(FadeIn(card_[0]), run_time=0.8)
            self.play(FadeIn(card_[1:3], shift=UP * 0.15), run_time=1.2)
            self.play(Create(card_[3]), Write(card_[4]), run_time=2)
        self.wait(0.6)
        self.clear_scene()

    def five(self):
        from explainer.industry import QUESTIONS

        rows = VGroup(*[VGroup(TB(str(i + 1), 30, I.ACCENT), T(q, 32, I.TEXT)).arrange(RIGHT, buff=0.35)
                        for i, (_, q) in enumerate(QUESTIONS)]).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        rows.move_to(LEFT * 0.6)
        head = T("Five questions, asked of every industry", 24, I.DIM).to_edge(UP, buff=0.7)
        stamp = VGroup(T("Every figure on screen carries", 20, I.DIM), T("its source and the date it describes",
                       20, I.DIM)).arrange(DOWN, buff=0.06).to_corner(DR, buff=0.5)
        demo = as_of("as of November 2026")
        with self.voiceover(
            "Every part of this series puts the same five questions to an industry. <bookmark mark='a'/> What is "
            "sold? <bookmark mark='b'/> How is it made, and what does one more cost? <bookmark mark='c'/> Where does "
            "the customer's dollar go? <bookmark mark='d'/> Why does the money stay where it does? <bookmark "
            "mark='e'/> And what moves it? <bookmark mark='f'/> In this first part we ask them of a single phone, "
            "follow its price to the companies that make it, and check each number against what those companies "
            "report. One thing before we start: every figure on screen carries its source and the date it "
            "describes, because the phone business changed a great deal this year."
        ) as vo:
            self.play(FadeIn(head))
            for k, m in zip(range(5), "abcde"):
                vo.wait_until(m)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2), run_time=0.7)
            vo.wait_until("f")
            self.play(FadeIn(stamp), FadeIn(demo))
        self.clear_scene()
