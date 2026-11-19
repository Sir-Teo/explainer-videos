from __future__ import annotations

from videos.economics.econ3.common import *  # noqa: F403

POUND = "#E3B98A"


class Counting(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Counting a country", r"Who first tried to add up a nation, and why?",
             "Chapter one. Counting a country.", scale=("nation",), horizon=("a year", "centuries"))
        self.petty()
        self.identity()
        self.timeline()

    # ------------------------------------------------------------------
    def petty(self):
        p = tables.PETTY_1665.data
        when = history_card(r"1665", r"William Petty, physician, surveyor, member of the Royal Society",
                            r"Verbum Sapienti (``a word to the wise''): how England might pay for its war with the "
                            r"Dutch, and pay fairly", color=POUND, width=6.6, font_size=25)
        when.to_edge(UP, buff=0.5).to_edge(LEFT, buff=0.6)
        people = VGroup(*[person(0.42, color=GREY_A) for _ in range(12)]).arrange_in_grid(2, 6, buff=0.14)
        times = MathTex(r"\times", font_size=48)
        spend = label(r"\pounds 6\ 13s\ 4d \\ a head, a year", font_size=28, color=POUND)
        eq = MathTex(r"=", font_size=48)
        total = label(rf"\pounds {p['expense'] / 1e6:.0f} million \\ a year", font_size=34, color=POUND)
        row = VGroup(VGroup(people, label(r"six million people", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.15),
                     times, spend, eq, total).arrange(RIGHT, buff=0.35).next_to(when, DOWN, buff=0.6).set_x(0)
        q = quote_card(p["expense_quote"], r"Petty, Verbum Sapienti, ch.\ 1 (Hull's edition, 1899)", width=9.6,
                       font_size=24, color=POUND).to_edge(DOWN, buff=0.4)
        tag = published_tag(r"W.\ Petty, Verbum Sapienti (written 1665, printed 1691)", corner=DR, font_size=16)
        with self.voiceover(
            "The first person to try was an Englishman, William Petty. <bookmark mark='a'/> In 1665 England was "
            "at war with the Dutch Republic, and London was dying of plague. Petty, a physician and surveyor, "
            "wrote a short tract called Verbum Sapienti, a word to the wise, about how the cost of the war "
            "could be raised, and raised fairly. To do it he needed the size of the whole nation. "
            "<bookmark mark='b'/> He started with people. England and Wales, he reckoned, had about six million "
            "of them, <bookmark mark='c'/> and each spent about six pounds thirteen shillings and four pence a "
            "year on food, housing, clothes and all other necessaries. <bookmark mark='d'/> So the nation's "
            "expense was forty million pounds a year."
        ) as vo:
            self.play(FadeIn(when, shift=UP * 0.2), FadeIn(tag))
            vo.wait_until("a")
            self.wait(0.5)
            vo.wait_until("b")
            self.play(FadeIn(row[0], lag_ratio=0.1))
            vo.wait_until("c")
            self.play(FadeIn(row[1]), FadeIn(row[2]))
            vo.wait_until("d")
            self.play(FadeIn(row[3]), FadeIn(row[4], scale=0.8))
            self.play(FadeIn(q, shift=UP * 0.2))
        self.wait(3.0)
        self.clear_scene()

    def identity(self):
        p = tables.PETTY_1665.data
        k = 0.13
        x0 = -5.6
        top = 1.6
        spend = Rectangle(width=40 * k, height=0.8, stroke_width=0, fill_color=POUND, fill_opacity=0.9)
        spend.move_to([x0 + 20 * k, top, 0])
        sl = label(r"what the people spend: \ \pounds 40 million", font_size=26, color=POUND).next_to(spend, UP,
                                                                                                    buff=0.15)
        stock = Rectangle(width=15 * k, height=0.8, stroke_width=0, fill_color=E.BANKS, fill_opacity=0.9)
        stock.move_to([x0 + 7.5 * k, top - 1.5, 0])
        labour = Rectangle(width=25 * k, height=0.8, stroke_width=0, fill_color=E.HOUSEHOLDS, fill_opacity=0.9)
        labour.move_to([x0 + 15 * k + 12.5 * k, top - 1.5, 0])
        stl = label(r"land, houses, ships, stock: \\ \pounds 15 million", font_size=22, color=E.BANKS)
        stl.next_to(stock, DOWN, buff=0.15)
        lal = label(r"so labour must furnish \\ \pounds 25 million", font_size=22, color=E.HOUSEHOLDS)
        lal.next_to(labour, DOWN, buff=0.15)
        eq = MathTex(r"\text{spending} \;=\; \text{income from property} \;+\; \text{income from labour}",
                     font_size=36).move_to(DOWN * 1.6)
        later = label(r"chapter 2: \ the same identity, \ the Island's accounts and America's", font_size=24,
                      color=E.ACCENT).next_to(eq, DOWN, buff=0.5)
        q = quote_card(p["labour_quote"], r"Petty, Verbum Sapienti, ch.\ 2", width=5.4, font_size=22, color=POUND)
        q.to_edge(RIGHT, buff=0.35).shift(UP * 1.4)
        with self.voiceover(
            "Then he turned it around. <bookmark mark='a'/> The land, the houses, the ships, the cattle and the "
            "rest of the nation's stock yielded, he estimated, about fifteen million pounds a year. "
            "<bookmark mark='b'/> If the people spend forty and their property yields only fifteen, then, he "
            "wrote, the labour of the people must furnish the other twenty-five. <bookmark mark='c'/> That is an "
            "identity, and it's the heart of this part. What a nation spends must equal what it earns: the income "
            "of its property plus the income of its labour. Petty used it for his taxes. Since labour earned most of "
            "the income, a fair tax should fall on the people as well as on property, in the same proportion: of "
            "every extra million pounds the war needed, three hundred and seventy-five thousand from property and "
            "six hundred and twenty-five thousand from the people. <bookmark mark='d'/> In the next chapter we'll "
            "keep the Island's books the same way, and America's."
        ) as vo:
            self.play(GrowFromEdge(spend, LEFT), FadeIn(sl))
            vo.wait_until("a")
            self.play(GrowFromEdge(stock, LEFT), FadeIn(stl))
            vo.wait_until("b")
            self.play(GrowFromEdge(labour, LEFT), FadeIn(lal), FadeIn(q, shift=LEFT * 0.2))
            vo.wait_until("c")
            self.play(Write(eq))
            vo.wait_until("d")
            self.play(FadeIn(later, shift=UP * 0.1))
        self.clear_scene()

    def timeline(self):
        events = [
            (1665, r"Petty: \ the nation's \\ expense and income", POUND, UP, 0.6),
            (1696, r"Gregory King: \ England's \\ families by rank", POUND, DOWN, 0.6),
            (1934, r"Kuznets: \ the first \\ US national income", KUZ, UP, 0.6),
            (1941, r"Meade and Stone: \\ Britain's war accounts", E.ACCENT, DOWN, 0.6),
            (1953, r"the UN's System \\ of National Accounts", E.WORLD, UP, 1.75),
            (1991, r"the US moves \\ from GNP to GDP", E.FIRMS, DOWN, 0.6),
            (2025, r"the SNA's \\ newest edition", E.WORLD, UP, 0.6),
        ]
        x0, x1 = -5.4, 5.9

        def X(y):
            # 1650-1720 in the first fifth, then a break, then 1925-2030
            if y <= 1720:
                return x0 + (x1 - x0) * 0.2 * (y - 1650) / 70
            return x0 + (x1 - x0) * (0.27 + 0.73 * (y - 1925) / 105)

        axis = Line([x0, 0, 0], [x1, 0, 0], color=GREY_C, stroke_width=2)
        bx = (X(1720) + X(1925)) / 2
        brk = VGroup(Line([bx - 0.12, -0.15, 0], [bx, 0.15, 0], color=GREY_C),
                     Line([bx, -0.15, 0], [bx + 0.12, 0.15, 0], color=GREY_C))
        marks = VGroup()
        for y, text, col, side, lift in events:
            d = Dot([X(y), 0, 0], radius=0.1, color=col)
            yr = label(str(y), font_size=26, color=col).next_to(d, -side, buff=0.15)
            stem = Line(d.get_center(), d.get_center() + side * lift, color=col, stroke_width=2.5)
            t = label(text, font_size=25, color=WHITE).next_to(stem.get_end(), side, buff=0.1)
            marks.add(VGroup(d, yr, stem, t))
        nobel = VGroup(
            label(r"Nobel prizes: \ Kuznets 1971, \ Leontief 1973, \ Stone 1984", font_size=28, color=E.ACCENT),
        ).to_edge(DOWN, buff=0.7)
        head = label(r"Counting a country", font_size=34).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Petty's rough arithmetic had followers. <bookmark mark='a'/> Thirty years later Gregory King drew up a "
            "table of England's families by rank, from the lords down to the cottagers and paupers, with what each "
            "earned and spent, and his figures drew heavily on Petty's. <bookmark mark='b'/> Then, for two "
            "centuries, private scholars made estimates now and then, and governments didn't. The Depression "
            "changed that, with Kuznets's report of 1934. <bookmark mark='c'/> The war changed it again. In 1940 "
            "John Maynard Keynes asked how much of Britain's output could be taken for the war without "
            "inflation, which can't be answered without knowing the total. Two young economists in the Cabinet "
            "Office, James Meade and Richard Stone, built the tables, and the government published them with the "
            "budget in April 1941. <bookmark mark='d'/> After the war Stone led the work on a standard every "
            "country could follow: the United Nations' System of National Accounts, first issued in 1953. "
            "<bookmark mark='e'/> The United States changed its featured measure from gross national product to "
            "gross domestic product in 1991, to match it, <bookmark mark='f'/> and the newest edition of the "
            "standard was adopted in March 2025. <bookmark mark='g'/> Three of the people in this story won the "
            "Nobel prize for it."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(brk), FadeIn(marks[0]))
            for m, mk in zip("abcdef", marks[1:]):
                vo.wait_until(m)
                self.play(FadeIn(mk, shift=UP * 0.1))
            vo.wait_until("g")
            self.play(FadeIn(nobel, shift=UP * 0.1))
        self.clear_scene()
