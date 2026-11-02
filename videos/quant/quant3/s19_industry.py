from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant3.common import CASH, DEBT, EQUITY, PART, VALUE


class Industry(VoiceoverScene):
    def construct(self):
        self.card()
        self.practice()
        self.courts()
        self.raters()
        self.leases()

    def card(self):
        c = chapter_card(17, r"Who values firms for a living", r"How do the desks, the courts and the raters do it?",
                         part=PART)
        with self.voiceover("Chapter seventeen. Who values firms for a living."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def practice(self):
        gh = firm_card(r"Corporate finance practice",
                       r"392 chief financial officers, surveyed in 1999, on the capital budgeting techniques they "
                       r"always or almost always use.",
                       numbers=[(r"75.7\%", r"internal rate of return"), (r"74.9\%", r"net present value"),
                                (r"38.9\%", r"earnings multiples"), (r"26.6\%", r"real options")],
                       source=r"Graham and Harvey, JFE 60 (2001); JACF 15 (2002)", width=6.3, font_size=21)
        aqr = firm_card(r"Quant equity on fundamentals",
                        r"AQR's quality-minus-junk factor starts from chapter 8's price-to-book formula: buy firms that "
                        r"are profitable, growing and safe, sell the opposite. Open Source Asset Pricing publishes the "
                        r"code and returns of 200-plus predictors; chapter 14 used it.",
                        numbers=[(r"\text{P/B}", r"$= 1 + (\text{ROE} - r)/(r - g)$")],
                        source=r"Asness, Frazzini and Pedersen, RAS 24 (2019); Chen and Zimmermann, CFR (2022)",
                        width=6.3, font_size=21)
        VGroup(gh, aqr).arrange(RIGHT, buff=0.35, aligned_edge=UP).scale_to_fit_width(13.3).move_to(UP * 0.2)
        with self.voiceover(
            "Who values firms for a living? Start inside the firms. When John Graham and Campbell Harvey surveyed chief financial "
            "officers, three in four said they always or almost always use the internal rate of return and net present value; "
            "two in five use earnings multiples, and a quarter real options. <bookmark mark='a'/> On the investing side, "
            "quantitative managers turn statements into signals at scale. AQR's quality-minus-junk factor, by Asness, Frazzini "
            "and Pedersen, starts from chapter eight's price-to-book formula and buys profitable, growing, safe firms; and Open "
            "Source Asset Pricing publishes the code behind two hundred predictors."
        ) as vo:
            self.play(FadeIn(gh, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(aqr, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def courts(self):
        dell = firm_card(r"In re Appraisal of Dell (Delaware)",
                         r"Dell's managers and Silver Lake bought the company in 2013. Shareholders sued for a fair "
                         r"value; the experts' DCFs were billions apart. The Court of Chancery ran its own DCF. On "
                         r"appeal, in December 2017, the Delaware Supreme Court reversed and told it to give weight to "
                         r"the market price and the deal price.",
                         numbers=[(r"\$13.75", r"the buyout price"), (r"\$17.62", r"the Chancery DCF, May 2016"),
                                  (r"\$28.61", r"the petitioners' expert")],
                         source=r"Court of Chancery, 31 May 2016; Delaware Supreme Court, 14 Dec.\ 2017", width=6.3,
                         font_size=20)
        rural = firm_card(r"Rural/Metro: a bank's valuation in court",
                          r"The Court of Chancery held RBC Capital Markets liable for aiding and abetting the board's "
                          r"breach of duty: it sought financing roles with the buyers it was advising against, and "
                          r"delivered a flawed valuation analysis just before the board's vote.",
                          numbers=[(r"\$75.8\text{m}", r"damages, affirmed 30 Nov.\ 2015")],
                          source=r"RBC Capital Markets v.\ Jervis, Delaware Supreme Court (2015)", width=6.3,
                          font_size=20)
        VGroup(dell, rural).arrange(RIGHT, buff=0.35, aligned_edge=UP).scale_to_fit_width(13.3).move_to(UP * 0.3)
        tag = label(r"whoever chooses $r$ and $g$ on the surface of chapter 6 chooses the answer", font_size=24,
                    color=QC.HOUSE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Valuation also happens in court. When Dell went private in 2013 at thirteen dollars seventy-five, shareholders asked "
            "Delaware's Court of Chancery for an appraisal. The experts' discounted cash flows were billions apart; the court "
            "built its own and found seventeen sixty-two. <bookmark mark='a'/> The Delaware Supreme Court reversed in 2017 and "
            "told it to give weight to the market price and the deal price. <bookmark mark='b'/> In the sale of Rural Metro, the "
            "court found the adviser, RBC Capital Markets, had sought financing roles with the buyers and delivered a flawed "
            "valuation just before the board voted; about seventy-six million dollars of damages, affirmed in 2015. "
            "<bookmark mark='c'/> The lesson of chapter six's surface: whoever chooses r and g chooses the answer."
        ) as vo:
            self.play(FadeIn(dell, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rural, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(tag))
        self.wait(0.4)
        self.clear_scene()

    def raters(self):
        sp = firm_card(r"Rating agencies",
                       r"S\&P scores a company's financial risk in six categories, from minimal to highly leveraged, "
                       r"starting from two ratios: funds from operations over debt, and debt over EBITDA. Merton's "
                       r"model of chapter 12 underlies the market-based default measures of Part 20.",
                       numbers=[(r"> 60\%", r"FFO / debt, ``minimal''"), (r"< 1.5\times", r"debt / EBITDA, ``minimal''")],
                       source=r"S\&P Global Ratings, corporate methodology", width=6.3, font_size=20)
        act = firm_card(r"Activists",
                        r"Hedge funds that buy 5\% of a firm must file a Schedule 13D. Brav, Jiang, Partnoy and Thomas "
                        r"found abnormal returns of about 7\% around the filing, with no reversal over the following "
                        r"year. In October 2023 the SEC cut the deadline from ten days to five business days.",
                        numbers=[(r"\approx 7\%", r"abnormal return around a 13D"), (r"5", r"business days to file")],
                        source=r"Brav et al., JF 63 (2008); SEC, 10 Oct.\ 2023", width=6.3, font_size=20)
        VGroup(sp, act).arrange(RIGHT, buff=0.35, aligned_edge=UP).scale_to_fit_width(13.3).move_to(UP * 0.1)
        with self.voiceover(
            "Rating agencies value the lenders' side. S and P scores financial risk in six categories, from minimal to highly "
            "leveraged, starting from funds from operations over debt and debt over EBITDA; a minimal-risk firm's cash flow "
            "exceeds sixty percent of its debt. <bookmark mark='a'/> And activists act on valuations. Brav and coauthors found "
            "that when a hedge fund files a 13D, a stake of five percent or more, the shares earn about seven percent beyond the "
            "market around the filing and do not give it back. Since 2023 the filing is due in five business days."
        ) as vo:
            self.play(FadeIn(sp, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(act, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def leases(self):
        def table(ev, ebitda, debt, title, col):
            rows = VGroup(
                label(title, font_size=24, color=col),
                MathTex(rf"\text{{enterprise value}}\ {ev:,.0f}".replace(",", "{,}"), font_size=30),
                MathTex(rf"\text{{EBITDA}}\ {ebitda:.0f}", font_size=30),
                MathTex(rf"\text{{debt}}\ {debt:.0f}", font_size=30, color=DEBT),
                MathTex(r"\text{equity}\ 900", font_size=30, color=EQUITY),
                MathTex(rf"\text{{EV/EBITDA}}\ {ev / ebitda:.2f}", font_size=30, color=VALUE),
                MathTex(rf"\text{{debt/EBITDA}}\ {debt / ebitda:.2f}", font_size=30, color=DEBT),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            return rows

        before = table(1200, 100, 300, r"before: leases in a footnote", GREY_A).move_to(LEFT * 3.6 + DOWN * 0.3)
        after = table(1350, 120, 450, r"after ASC 842: on the balance sheet", QC.HOUSE).move_to(RIGHT * 2.2 + DOWN * 0.3)
        lease = VGroup(RoundedRectangle(width=2.4, height=0.8, corner_radius=0.1, color=CASH, fill_opacity=0.2),
                       label(r"lease 150; rent 20", font_size=20, color=CASH))
        lease[1].move_to(lease[0])
        lease.next_to(before, DOWN, buff=0.3)
        head = VGroup(
            wrapped_label(r"2005: the SEC staff estimated about \$1.25 trillion of operating-lease commitments off "
                          r"balance sheets. ASU 2016-02 (ASC 842) put them on, for public companies, from fiscal years "
                          r"starting after 15 December 2018.", 12.6, 21, GREY_A),
            label(r"illustrative firm: equity 900, net debt 300, EBITDA 100, leases 150 at a rent of 20 a year",
                  font_size=18, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(UP, buff=0.35)
        with self.voiceover(
            "And the standard setters move the numbers under everyone's feet. In 2005 the SEC's staff estimated that American "
            "companies had about a trillion and a quarter dollars of operating-lease commitments that never appeared on a balance "
            "sheet. From 2019 the new lease standard put them on. <bookmark mark='a'/> Watch what that does to a firm whose business "
            "did not change. The lease liability moves from the footnote into debt, and the rent, now split into depreciation and "
            "interest, leaves EBITDA's costs. <bookmark mark='b'/> Enterprise value and EBITDA both rise; the multiple falls and "
            "leverage rises. The equity is worth exactly what it was. A screen that compares multiples across 2018 and 2019 without "
            "adjusting is comparing two accounting regimes, not two firms."
            " More and more, the first reader of a filing is a machine. Next: the frontier."
        ) as vo:
            self.play(FadeIn(head), FadeIn(before), FadeIn(lease))
            vo.wait_until("a")
            self.play(lease.animate.next_to(after, DOWN, buff=0.3), run_time=2)
            vo.wait_until("b")
            self.play(TransformFromCopy(before, after), run_time=2)
            self.play(Indicate(after[5], color=VALUE), Indicate(after[6], color=DEBT), Indicate(after[4], color=EQUITY))
        self.wait(0.4)
        self.clear_scene()
