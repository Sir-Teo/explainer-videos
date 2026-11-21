from __future__ import annotations

from videos.economics.econ61.common import *  # noqa: F403

NAMES = ("A", "B", "C", "D")


class AdAuctions(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Ad auctions in practice", r"How does a search engine sell a page of ads billions of times a "
             r"day?", "Chapter six. Ad auctions in practice.",
             lit={2007: r"Varian; \ Edelman, Ostrovsky and Schwarz", 2019: r"first price"},
             scale=("firm", "market"), horizon=("a day",))
        self.quality()
        self.practice()

    def table(self, G, key):
        b, q = G["bids"], G["quality"]
        res = G["plain"][key]
        slot = {i: k for k, i in enumerate(res["order"])}
        head = [r"advertiser", r"bid, \ \$", r"quality", r"score", r"slot", r"pays per click"]
        rows = [head]
        for i, n in enumerate(NAMES):
            sc = b[i] * q[i] if key == "quality" else b[i]
            s_ = slot.get(i)
            rows.append([n, f"{b[i]:.2f}", f"{q[i]:.1f}", f"{sc:.2f}", "--" if s_ is None else f"{s_ + 1}",
                         "--" if s_ is None else rf"\${res['prices'][s_]:.2f}"])
        cells = VGroup()
        for r, row in enumerate(rows):
            for c, txt in enumerate(row):
                col = GREY_A if r == 0 else (AD if c == 5 else WHITE)
                cells.add(label(txt, font_size=17, color=col).move_to([c * 1.55, -r * 0.42, 0]))
        return cells

    def quality(self):
        G = load("gsp")
        t1 = self.table(G, "bid only").move_to(LEFT * 2.6 + UP * 1.6)
        t2 = self.table(G, "quality").move_to(LEFT * 2.6 + DOWN * 1.35)
        h1 = label(r"ranked by bid alone", font_size=21, color=GREY_B).next_to(t1, UP, buff=0.2)
        h2 = label(r"ranked by bid $\times$ quality \ (the generalized second price)", font_size=21,
                   color=AD).next_to(t2, UP, buff=0.2)
        P, Q = G["plain"]["bid only"], G["plain"]["quality"]
        side = VGroup(
            label(r"quality: \ how often searchers click this ad, \\ relative to an average ad", font_size=18,
                  color=GREY_A),
            label(rf"by bid: \ {P['total_clicks']:.2f} clicks and \${P['revenue']:.3f} a search", font_size=19,
                  color=GREY_B),
            label(rf"by score: \ {Q['total_clicks']:.2f} clicks and \${Q['revenue']:.3f} a search", font_size=19,
                  color=AD),
            label(r"each pays the least bid that keeps its slot: \\ the next score over its own quality",
                  font_size=18, color=WHITE),
            label(rf"a reserve of \$1.50: \ \${G['reserve']['quality']['revenue']:.3f} a search", font_size=19,
                  color=SURGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        if side.width > 4.6:
            side.width = 4.6
            side.to_edge(RIGHT, buff=0.3)
        tag = agora_tag(r"computed: \ agora.platform.gsp; \ three slots with click rates 30\%, 18\%, 10\%",
                        corner=DL, font_size=12)
        with self.voiceover(
            "Part sixteen built the generalized second-price auction for search ads. Here is the piece it left "
            "for the practitioners: quality. <bookmark mark='a'/> Four advertisers bid for three slots. Ranked by "
            "bid alone, A, the highest bidder, takes the top slot. <bookmark mark='b'/> But A's ad is a poor "
            "match for the search: searchers click it half as often as an average ad. Its quality score is a "
            "half. <bookmark mark='c'/> Rank by bid times quality instead, the expected payment per search, and B "
            "takes the top slot, A drops to second. <bookmark mark='d'/> Each advertiser pays the least it could "
            "have bid and kept its slot: the next advertiser's score divided by its own quality. A, with the "
            "worse ad, pays more per click than B. <bookmark mark='e'/> Searchers click more, "
            f"{Q['total_clicks']:.2f} times a search against {P['total_clicks']:.2f}, and the platform earns more "
            f"too, {Q['revenue']:.3f} dollars a search against {P['revenue']:.3f}: quality scores align the "
            "platform's revenue with its users' interest. <bookmark mark='f'/> A reserve price of a dollar fifty "
            f"lifts the last slot's price and the revenue to {G['reserve']['quality']['revenue']:.3f}, Part "
            "sixteen's Myerson reserve at work."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(h1), FadeIn(t1))
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(h2), FadeIn(t2), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[2]))
            vo.wait_until("f")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def practice(self):
        cards = point_cards([
            (r"reserve prices, \ tested", r"Yahoo!, \ 2008: \ reserves set by Myerson's rule raised revenue on "
             r"busy keywords and lowered it on rare ones; \ a few percent overall \ (the Dials)", SURGE),
            (r"the move to first price", r"2019: \ Google's display-ad exchange switches to first-price auctions, "
             r"\ as bidders were already shading bids across many exchanges", AD),
            (r"auto-bidding", r"most advertisers now tell the platform a budget and a target, \ and its algorithm "
             r"bids for them: \ the auction's bidders are the platform's own software", PLAT),
            (r"what the economist does", r"sets reserves, \ quality formulas and auction formats, \ and tests each "
             r"change on a share of the traffic first", TEST),
        ], width=12.6, cols=2, font_size=20).move_to(DOWN * 0.2)
        head = label(r"auction design is never finished", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Ostrovsky and Schwarz (2009); \ Varian, \ International Journal of Industrial "
                            r"Organization 25 (2007); \ Part 16", corner=DL, font_size=12)
        with self.voiceover(
            "The design keeps changing. <bookmark mark='a'/> In 2008 Yahoo! let Michael Ostrovsky and Michael "
            "Schwarz set reserve prices by Myerson's rule on hundreds of thousands of keywords, with others held "
            "back as controls. Revenue rose on busy keywords and fell on rare ones, where reserves drove bidders "
            "away: a few percent overall, which at that scale is a great deal of money. That dial returns at the "
            "end of this part. <bookmark mark='b'/> In 2019 Google moved its display-ad exchange to first-price "
            "auctions; bidders spread across many exchanges were already shading their bids, and the second "
            "price had lost its simplicity. <bookmark mark='c'/> Today most advertisers do not bid at all: they "
            "give the platform a budget and a target cost, and its algorithm bids for them, so the bidders in the "
            "auction are the platform's own software, a design problem Part sixteen's theory is still catching up "
            "with. <bookmark mark='d'/> The economist's work is to set reserves, quality formulas and formats, "
            "and to test each change on a slice of the traffic before it goes everywhere."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()
