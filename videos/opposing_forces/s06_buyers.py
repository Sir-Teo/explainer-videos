from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.opposing_forces.common import TimeChart, label, show_chapter_card, source, tagged, ts

FOREIGN = BLUE_D  # local to this chart


class Buyers(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 5, r"Force 2: who's left to buy?")
        self.who()
        self.shares()
        self.flows()

    # ------------------------------------------------------------------
    def who(self):
        title = label(r"non-economic buyers: they buy bonds for reasons other than the return", font_size=34)
        title.to_edge(UP, buff=0.5)
        rows = VGroup(
            VGroup(label(r"the Federal Reserve", font_size=32, color=C.POLICY),
                   label(r"buys bonds to push long-term rates down (quantitative easing)", font_size=26, color=GREY_A)),
            VGroup(label(r"foreign central banks", font_size=32, color=FOREIGN),
                   label(r"park their reserves in Treasuries, to manage their currencies", font_size=26, color=GREY_A)),
            VGroup(label(r"banks and insurers", font_size=32, color=GREY_A),
                   label(r"hold them because regulations require safe assets", font_size=26, color=GREY_A)),
        )
        for r in rows:
            r.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(DOWN * 0.1 + LEFT * 0.5)
        tag = tagged(r"price-blind demand keeps yields low", font_size=32, color=YELLOW).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Force number two is about who buys all these bonds. Timmer's term is non-economic buyers: <bookmark "
            "mark='t'/> investors who buy bonds for reasons other than the return. <bookmark mark='a'/> The Federal "
            "Reserve, which bought trillions of dollars of Treasuries to push long-term rates down. <bookmark mark='b'/> "
            "Foreign central banks, which park their reserves in Treasuries. <bookmark mark='c'/> And banks and insurers "
            "that hold them because regulations require it. <bookmark mark='d'/> None of them haggle much over price, so "
            "as long as they're buying, yields stay lower than they otherwise would."
        ) as vo:
            vo.wait_until("t")
            self.play(FadeIn(title))
            for i, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(FadeIn(rows[i], shift=RIGHT * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(tag, shift=UP * 0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def shares(self):
        tf, vf = ts("holders_share", "fed")
        tg, vg = ts("holders_share", "foreign")
        n = min(len(tf), len(tg))
        tf, vf, vg = tf[:n], vf[:n], vg[:n]
        tot = vf + vg
        k_peak = int(np.argmax(tot))
        assert 2013.5 < tf[k_peak] < 2015 and 67 < tot[k_peak] < 71 and 43 < tot[-1] < 47 and tf[-1] >= 2026
        ch = TimeChart((2000, 2026.5), (0, 100), width=10.0, height=4.8, x_ticks=range(2000, 2030, 5),
                       y_ticks=[0, 25, 50, 75, 100], y_fmt=lambda y: rf"{y:g}\%").move_to(DOWN * 0.35 + LEFT * 0.6)
        yl = ch.y_title(r"share of Treasury debt held by the public, owned by\ldots", color=GREY_A)
        fed_area = Polygon(*([ch.c2p(a, 0) for a in tf[::-1]] + [ch.c2p(a, b) for a, b in zip(tf, vf)]), stroke_width=0,
                           fill_color=C.POLICY, fill_opacity=0.6)
        for_area = Polygon(*([ch.c2p(a, b) for a, b in zip(tf[::-1], vf[::-1])] + [ch.c2p(a, b) for a, b in zip(tf, tot)]),
                           stroke_width=0, fill_color=FOREIGN, fill_opacity=0.6)
        top = ch.line(tf, tot, WHITE, 3)
        fed_l = tagged(r"the Fed", font_size=28, color=C.POLICY).move_to(ch.c2p(2021.0, 11))
        for_l = tagged(r"foreign investors (official and private)", font_size=26, color=FOREIGN).move_to(ch.c2p(2008.5, 35))
        rest_l = tagged(r"everyone else: price-sensitive buyers", font_size=28, color=GREY_A).move_to(ch.c2p(2013.0, 86))
        pk = tagged(rf"{int(tf[k_peak])}: {tot[k_peak]:.0f}\%", font_size=26).next_to(ch.c2p(tf[k_peak], tot[k_peak]), UP, buff=0.12)
        nw = tagged(rf"2026: {tot[-1]:.0f}\%", font_size=26).next_to(ch.c2p(tf[-1], tot[-1]), UP, buff=0.12).shift(LEFT * 0.4)
        src = source(r"FRED (FDHBFRBN, FDHBFIN, FYGFDPUN)")
        with self.voiceover(
            "Here's who has owned the government's debt. <bookmark mark='f'/> In teal, the share owned by the Fed. "
            "<bookmark mark='g'/> In blue, the share owned by foreign investors, including foreign central banks. <bookmark "
            "mark='p'/> Together they peaked at about seventy percent in 2014. <bookmark mark='n'/> Today it's about "
            "forty-five percent. The Fed spent three and a half years shrinking its bond holdings, and even now that it's "
            "buying again, mostly short-term bills, its share keeps falling. Foreign buyers haven't kept pace with all "
            "the new debt either."
        ) as vo:
            self.play(Create(ch), FadeIn(yl), FadeIn(src))
            vo.wait_until("f")
            self.play(FadeIn(fed_area), FadeIn(fed_l))
            vo.wait_until("g")
            self.play(FadeIn(for_area), FadeIn(for_l), Create(top))
            vo.wait_until("p")
            self.play(FadeIn(pk))
            vo.wait_until("n")
            self.play(FadeIn(nw), FadeIn(rest_l))

        punch = tagged(r"``taking the punch bowl away, rather than spiking it''", font_size=30, color=YELLOW)
        punch.to_edge(DOWN, buff=0.12).shift(LEFT * 2.5)
        with self.voiceover(
            "In Timmer's words, central banks are taking the punch bowl away rather than spiking it. <bookmark mark='r'/> "
            "So more and more of the debt has to be sold to everyone else: pension funds, asset managers, hedge funds, "
            "households. These buyers do care about price. To take on more long-term government debt, they demand a "
            "better deal: a higher term premium."
        ) as vo:
            self.play(FadeIn(punch))
            vo.wait_until("r")
            self.play(Indicate(rest_l, color=WHITE))
        self.clear_scene()

    # ------------------------------------------------------------------
    def flows(self):
        q = VGroup(label(r"Then who is selling bonds?", font_size=40),
                   label(r"Bonds have been in a relentless bear market,\\so you might expect investors to be fleeing them.",
                         font_size=28, color=GREY_A),
                   label(r"Timmer's fund-flow chart shows the opposite: end investors\\have been buying bond ETFs and "
                         r"mutual funds\\about as fast as stock funds.", font_size=28, color=GREY_A),
                   ).arrange(DOWN, buff=0.35).move_to(UP * 0.6)
        quote = tagged(r"``Someone is selling, but it's not mom and pop.''", font_size=36, color=YELLOW).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "One twist. After years of losses, you might expect ordinary investors to be dumping their bond funds. "
            "<bookmark mark='a'/> Timmer's fund-flow data shows the opposite: end investors have been buying bonds through "
            "ETFs and mutual funds about as fast as they've been buying stocks. <bookmark mark='q'/> As he puts it: "
            "someone is selling, but it's not mom and pop. The pressure is coming from the big, price-blind buyers "
            "stepping back, and from the sheer volume of supply."
        ) as vo:
            self.play(FadeIn(q[0]), FadeIn(q[1]))
            vo.wait_until("a")
            self.play(FadeIn(q[2]))
            vo.wait_until("q")
            self.play(FadeIn(quote, shift=UP * 0.2))
        self.clear_scene()
