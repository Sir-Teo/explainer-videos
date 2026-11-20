from __future__ import annotations

from videos.economics.econ25.common import *  # noqa: F403


class Modern(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Zimbabwe and Venezuela", r"Do the old lessons still hold?", "Chapter eight. Zimbabwe and "
             "Venezuela.", lit={2008: r"Zimbabwe", 2018: r"Venezuela"}, scale=("nation",), horizon=("a year",))
        self.zimbabwe()
        self.venezuela()
        self.same()

    def zimbabwe(self):
        hk = load("laffer")["table"]
        z = next(r for r in hk if r["key"] == "zimbabwe")
        rows = VGroup(
            label(r"Zimbabwe", font_size=32, color=E.ACCENT),
            label(r"from 2000: \ farms seized and redistributed; \ farm output and exports fell sharply", font_size=22,
                  color=GREY_A),
            label(r"the government's deficits, \ and the central bank's own spending, \ paid by printing",
                  font_size=22, color=PRICE),
            label(rf"November 2008: \ {z['monthly_pct'] / 1e9:.1f} billion percent a month; \ prices doubling about "
                  r"every day", font_size=23, color=PRICE),
            label(r"January 2009: \ a 100-trillion-dollar note", font_size=23, color=MONEY),
            label(r"2009: \ the Zimbabwe dollar abandoned for US dollars and rand: \ prices stopped rising",
                  font_size=23, color=CB),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        tag = published_tag(r"Hanke and Krus (2012)", corner=DR, font_size=12)
        with self.voiceover(
            "The twenty-first century has had its own. <bookmark mark='a'/> In Zimbabwe, from 2000, commercial farms "
            "were seized and redistributed, and farm output and exports fell sharply. <bookmark mark='b'/> The "
            "government ran deficits, and its central bank spent heavily on its own account, both paid for by "
            f"printing. <bookmark mark='c'/> By November 2008, prices were rising about {z['monthly_pct'] / 1e9:.0f} "
            "billion percent a month, doubling about once a day. <bookmark mark='d'/> In January 2009 the central "
            "bank issued a note for one hundred trillion Zimbabwe dollars. <bookmark mark='e'/> Weeks later the "
            "country gave up its currency altogether and used American dollars and South African rand. Prices "
            "stopped rising almost at once."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag), FadeIn(rows[1]))
            for mk, r_ in zip("bcde", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def venezuela(self):
        rows = VGroup(
            label(r"Venezuela", font_size=32, color=E.ACCENT),
            label(r"from 2014: \ the price of oil, \ almost all its exports, \ collapsed; \ output fell", font_size=22,
                  color=GREY_A),
            label(r"deficits financed by the central bank", font_size=22, color=PRICE),
            label(r"July 2018: \ the IMF projects inflation of 1{,}000{,}000\% for the year", font_size=23,
                  color=PRICE),
            label(r"August 2018: \ five zeros struck off the bol\'{\i}var", font_size=23, color=MONEY),
            label(r"then, \ in practice, \ the dollar: \ shops priced and paid in dollars", font_size=23, color=CB),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        tag = published_tag(r"IMF Western Hemisphere Department, \ statements of July and October 2018", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Venezuela followed the same road a decade later. <bookmark mark='a'/> From 2014 the price of oil, almost "
            "all of its exports, collapsed, and output fell year after year. <bookmark mark='b'/> The government's "
            "deficits were financed by the central bank. <bookmark mark='c'/> In July 2018 the IMF projected "
            "inflation of one million percent for the year. <bookmark mark='d'/> That August the government struck "
            "five zeros off the currency, which changes the units but not the printing. <bookmark mark='e'/> What "
            "slowed it was the dollar: by the end of the decade many shops priced and took payment in dollars, and "
            "the bolívar's tax base had nearly vanished."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag), FadeIn(rows[1]))
            for mk, r_ in zip("bcde", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def same(self):
        fc = point_cards([
            (r"the cause", r"a deficit larger than \\ taxes and loans could cover", PRICE),
            (r"the mechanism", r"printing, \ then flight \\ from money (chapter 6)", MONEY),
            (r"the paradox", r"printing beyond the \\ Laffer peak", PRICE),
            (r"the end", r"a new fiscal regime, \\ or a new money", CB),
        ], width=12.0, cols=2, font_size=22).move_to(DOWN * 0.2)
        head = label(r"the same framework, \ a century apart", font_size=32, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "The framework of the last three chapters fits both. <bookmark mark='a'/> The cause: a deficit larger than "
            "taxes and loans could cover. <bookmark mark='b'/> The mechanism: printing, and then flight from money. "
            "<bookmark mark='c'/> The paradox: printing beyond the point where it raises any more. "
            "<bookmark mark='d'/> And the end: a fiscal regime people believe, or, when no one believes anything, "
            "someone else's money."
        ) as vo:
            self.play(FadeIn(head), FadeIn(fc.cards[0]))
            for mk, c in zip("bcd", fc.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
