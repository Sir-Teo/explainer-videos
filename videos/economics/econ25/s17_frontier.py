from __future__ import annotations

from videos.economics.econ25.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 15, r"Frontier: \ stablecoins and central bank digital money", r"Will private digital money "
             r"work, \ and should central banks issue their own?",
             "Chapter fifteen. Frontier: stablecoins and central bank digital money.",
             lit={2023: r"Gorton and Zhang", 2025: r"the GENIUS Act"}, scale=("market", "world"),
             horizon=("years",))
        self.stablecoins()
        self.wildcat()
        self.cbdc()
        self.open_()

    def stablecoins(self):
        rows = VGroup(
            label(r"a stablecoin: \ a token on a blockchain, \ redeemable one for one in dollars, \ backed by "
                  r"reserves", font_size=23, color=MONEY),
            label(r"from about \$205 billion in January 2025 to about \$306 billion by the end of November",
                  font_size=23, color=MONEY),
            label(r"July 2025: \ the GENIUS Act, \ America's first federal rules: \ backing one for one in safe assets",
                  font_size=22, color=CB),
            label(r"a deposit-like promise, \ issued outside the banking system", font_size=24, color=E.ACCENT),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.2)
        tag = published_tag(r"market size: \ DeFi Llama, \ as reported in December 2025", corner=DR, font_size=12)
        with self.voiceover(
            "The frontier is new private money. <bookmark mark='a'/> A stablecoin is a token on a blockchain whose "
            "issuer promises to redeem it one for one in dollars, and holds reserves to back the promise. "
            "<bookmark mark='b'/> Their total value grew from about two hundred and five billion dollars in January "
            "2025 to about three hundred and six billion by the end of November. <bookmark mark='c'/> In July 2025 "
            "the United States passed its first federal rules for them, the GENIUS Act, which requires backing one "
            "for one in safe assets. <bookmark mark='d'/> A stablecoin is a promise to pay dollars on demand, like a "
            "deposit, issued outside the banking system."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def wildcat(self):
        rows = VGroup(
            label(r"Gorton and Zhang, \ 2023: \ we have been here before", font_size=27, color=E.ACCENT),
            label(r"America's free banking era, \ before the Civil War: \ state banks issued their own notes",
                  font_size=22, color=GREY_A),
            label(r"notes traded below par, \ at discounts that varied with distance and doubt; \ runs were common",
                  font_size=22, color=PRICE),
            label(r"1863: \ the National Bank Act: \ a uniform currency backed by Treasury bonds", font_size=22,
                  color=CB),
            label(r"their proposal: \ regulate issuers as banks, \ or offer public digital money", font_size=23,
                  color=MONEY),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Gorton and Zhang, \ University of Chicago Law Review 90(3) (2023): \ 909--972",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Gary Gorton and Jeffery Zhang argue that we have seen this before. <bookmark mark='a'/> Before the "
            "American Civil War, in the free banking era, state-chartered banks issued their own notes. "
            "<bookmark mark='b'/> Those notes were often not accepted at par: their value depended on the issuer and "
            "on how far you were from it, and banks were prone to runs. <bookmark mark='c'/> In 1863 the National "
            "Bank Act created a uniform national currency, backed by Treasury bonds, and later laws taxed the state "
            "notes out of existence. <bookmark mark='d'/> Their proposal: treat stablecoin issuers as banks, or let "
            "the central bank offer digital money of its own. Not everyone agrees: George Selgin, among others, "
            "reads that history differently."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def cbdc(self):
        rows = VGroup(
            label(r"central bank digital currency: \ cash's digital twin, \ a direct claim on the central bank",
                  font_size=23, color=CB),
            label(r"the Bahamas \ (2020), \ pilots in China, \ preparation for a digital euro", font_size=22,
                  color=GREY_A),
            label(r"the case for: \ public money that never trades below par, \ and competition for payments",
                  font_size=22, color=MONEY),
            label(r"the case against: \ deposits could flee banks in a panic, \ and the state could watch every "
                  r"payment", font_size=22, color=PRICE),
            label(r"crypto and decentralized finance, \ in depth: \ \emph{Quant, Built}, \ Part 39", font_size=20,
                  color=GREY_B),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        with self.voiceover(
            "The public alternative is central bank digital currency: a digital version of cash, a direct claim "
            "on the central bank rather than on a bank. <bookmark mark='a'/> The Bahamas launched one in 2020; China "
            "has run large pilots; the euro area is preparing a digital euro. <bookmark mark='b'/> The case for: "
            "public money that can never trade below par, and competition for the payment system. "
            "<bookmark mark='c'/> The case against: in a panic, depositors could move their money out of banks into "
            "the central bank with a click, and a state could watch every payment. <bookmark mark='d'/> The series' "
            "sister course, Quant, Built, takes up crypto and decentralized finance in Part thirty-nine."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def open_(self):
        cards = point_cards([
            (r"at par?", r"will private digital dollars \\ always be worth a dollar?", MONEY),
            (r"banks", r"if deposits move to tokens, \\ who makes the loans?", BANK),
            (r"privacy", r"cash is anonymous; \\ should digital money be?", CB),
            (r"many moneys", r"Kiyotaki and Wright again: \\ which will people accept?", PRICE),
        ], width=12.0, cols=2, font_size=22).move_to(DOWN * 0.2)
        head = label(r"open questions", font_size=34, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Four open questions. <bookmark mark='a'/> Will private digital dollars always be worth a dollar? "
            "<bookmark mark='b'/> If deposits move into tokens, who makes the loans that deposits now fund? "
            "<bookmark mark='c'/> Cash is anonymous; should digital money be? <bookmark mark='d'/> And when many "
            "moneys compete, which will people accept? That is chapter three's question, now asked of software."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cards.cards[0], shift=UP * 0.1))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
