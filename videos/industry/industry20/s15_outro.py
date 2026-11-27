from __future__ import annotations

from videos.industry.industry20.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.close()

    def recap(self):
        H, O, C, Cl = R["hook"], R["odds"], R["cost"], R["cliff"]
        lines = [
            (f"the odds: {O['loa']}% of drugs entering trials are approved, after {O['years']:.1f} years", BAD),
            (f"one approved drug carries about twelve failures: ${C['per_approval'] / 1e3:.1f}bn, ${C['capitalized'] / 1e3:.1f}bn "
             "with time counted (the Works)", PRICE),
            ("so a protected drug is priced to pay for the misses", BRAND),
            (f"the cliff: one generic maker cuts the price {Cl['fda'][1]}%, six or more over {Cl['fda'][6]}%; Lipitor "
             f"{100 * H['lip_fall']:.0f}% in a year", GENERIC),
            (f"the calendar: Keytruda {H['key_share']}% of Merck, US patent {H['key_us']}; tirzepatide {H['lly_share']}% of Lilly", LAB),
        ]
        g = VGroup(*[tx(t, 20, c, bold=True) for t, c in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 0.0, 0])
        for r_ in g:
            if r_.width > 12.6:
                r_.scale_to_fit_width(12.6)
        beat(self,
             "So why does a pill that costs cents to make sell for dollars, and then one day for cents? "
             "<bookmark mark='a'/> Because most drugs fail, and the ones that work take a decade. <bookmark mark='b'/> "
             "Each approved medicine has to pay for about a dozen that failed, and for the years of waiting. "
             "<bookmark mark='c'/> So while it is protected, its price is set by what it is worth to patients and payers, "
             "not by what it costs to make. <bookmark mark='d'/> When protection ends, copies arrive and the price falls to "
             "near the cost of making it. <bookmark mark='e'/> And every drug company lives on that calendar, looking for "
             "the next drug before the old one's date. The system trades high prices for a time against cheap copies "
             "forever after; whether the trade is a good one is argued about in every country, and in America it is now "
             "being renegotiated, drug by drug, by Medicare.",
             base=[head("Cents and dollars")], steps=list(g))

    def close(self):
        caps = VGroup(*[draw.capsule(0.8, BRAND if i % 2 else GENERIC) for i in range(7)]).arrange(RIGHT, buff=0.3).move_to([0, 0.6, 0])
        nxt = tx("Next: Part 21, Medical Technology", 26, PRICE, bold=True).move_to([0, -2.4, 0])
        with self.voiceover("Medicines that cost a fortune to discover and almost nothing to copy: an industry that runs "
                            "on the law as much as on chemistry. Next time: medical technology, where the product is a machine "
                            "and the customer is often a surgeon.") as vo:
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in caps], lag_ratio=0.15), run_time=2)
            self.play(*[c.animate.set_color(GENERIC) for c in caps], run_time=2)
            self.play(FadeIn(nxt))
        self.clear_scene()
