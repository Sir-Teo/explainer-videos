from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant15.common import BAD, BARRIER, GOOD, OPT, PART, SPOT, illustration, load, real_data, ymd_to_year


def _closest(k):
    """For each note: the lowest close over its life (up to three years), as a fraction of its start."""
    d, c = np.asarray(k["date"]), np.asarray(k["close"])
    out = []
    for r in k["rows"]:
        i = int(np.searchsorted(d, r["start"]))
        j = int(np.searchsorted(d, min(r["date"], r["start"] + 30000), side="right"))
        out.append(float(c[i:max(j, i + 1)].min() / r["S0"]))
    return out


class Korea(VoiceoverScene):
    def construct(self):
        k = load("korea")
        k15 = load("korea2015")
        self.card()
        self.terms()
        self.notes2015(k15)
        self.fsc2016()
        self.notes(k)
        self.file()
        self.natixis()

    def card(self):
        c = chapter_card(10, r"Korea's ELS, twice, and a dealer's loss", r"What happens when a bank sells a knock-in "
                         r"to savers?", lit=(2016, 2018, 2024), part=PART)
        with self.voiceover("Chapter ten. Korea's equity-linked securities, twice, and a dealer's loss."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def terms(self):
        steps = [0.90, 0.90, 0.85, 0.85, 0.80, 0.75]
        g = axes([0, 3], [0.4, 1.1], x_length=7.0, y_length=4.2, xlabel=r"years", ylabel=r"index / start",
                 xticks=[0, 0.5, 1, 1.5, 2, 2.5, 3], yticks=[0.5, 0.75, 1.0], font_size=15).to_edge(LEFT, buff=0.7)
        ax = g.ax
        stair = VGroup(*[Line(ax.c2p(0.5 * i + 0.4, s_), ax.c2p(0.5 * i + 0.6, s_), stroke_color=GOOD, stroke_width=5)
                         for i, s_ in enumerate(steps)])
        kil = DashedLine(ax.c2p(0, 0.5), ax.c2p(3, 0.5), stroke_color=BARRIER, stroke_width=2.5)
        rows = [cmath(r"V", r"=", r"\sum_{k=1}^{6} \mathbb E\big[D_k\,\mathbf 1_{\tau = k}\big]\big(1 + 0.03k\big) + "
                      r"\mathbb E\big[D_6\,\mathbf 1_{\text{alive}}\,\text{payoff}\big]", font_size=30,
                      colors={r"V": OPT})]
        side = VGroup(
            wrapped_label(r"a stylized step-down ELS: three years; every six months, repaid with 3\% per half-year if the "
                          r"index is above 90, 90, 85, 85, 80, 75\% of its start; a knock-in at 50\%, watched daily", 4.6,
                          19, GREY_A),
            rows[0],
            wrapped_label(r"a strip of six digitals on a falling staircase, and a down-and-in put at half the start. The "
                          r"steps make an early exit likelier as time passes, so the coupon is cheap to pay; the put is "
                          r"what pays for it", 4.6, 19, WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Korea's snowball is the step-down equity-linked security, and its favourite underlying was Hong Kong's "
            "index of Chinese companies, the HSCEI. Every six months the note is repaid with its coupon if the index "
            "is above a level that steps down, ninety percent of the start, then eighty-five, then eighty. "
            "<bookmark mark='a'/> And a knock-in at half the start, watched daily. In option terms: six digitals on "
            "a falling staircase, plus a down-and-in put with its barrier at fifty percent, which pays for them."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            self.play(LaggedStart(*[Create(s_) for s_ in stair], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(Create(kil), FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def notes2015(self, k):
        t = ymd_to_year(k["date"])
        px = np.asarray(k["close"])
        g = axes([2015, 2019], [5000, 16000], x_length=7.4, y_length=4.4, ylabel=r"HSCEI",
                 xticks=[2015, 2016, 2017, 2018, 2019], yticks=[6000, 10000, 14000],
                 yfmt=lambda u: f"{u:,.0f}".replace(",", "{,}"), font_size=16).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        m = t <= 2019
        line = curve(ax, t[m], px[m], SPOT, stroke_width=2.2)
        rows = k["rows"]
        close = _closest(k)
        marks = VGroup()
        for r, c_ in zip(rows, close):
            t0 = ymd_to_year([r["start"]])[0]
            col = BAD if r["knocked_in"] else GOOD
            marks.add(VGroup(Dot(ax.c2p(t0, r["S0"]), radius=0.06, color=col),
                             DashedLine(ax.c2p(t0, 0.5 * r["S0"]), ax.c2p(min(t0 + 3, 2019), 0.5 * r["S0"]),
                                        stroke_color=col, stroke_width=1.2, dash_length=0.06)))
        n_ki = sum(r["knocked_in"] for r in rows)
        j = int(np.argmin(close))
        nearest = close[j]
        late = sum(1 for r in rows if r["date"] >= 20170101)
        side = VGroup(
            wrapped_label(r"the same stylized note, issued each month of 2015, the year the HSCEI peaked", 4.4, 19, GREY_A),
            wrapped_label(rf"knocked in: {n_ki} of {len(rows)}. The closest call: the note of "
                          rf"{str(rows[j]['start'])[:4]}-{str(rows[j]['start'])[4:6]} fell to {100 * nearest:.0f}\% of its "
                          r"start, against a knock-in at 50\%", 4.4, 19, BAD if n_ki else GOOD),
            wrapped_label(rf"{late} of the 12 were repaid only in 2017 or later, after waiting through the fall", 4.4, 19,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        src = real_data(r"Yahoo Finance: Hang Seng China Enterprises Index, daily; stylized terms, not any one bank's note")
        verdict = (f"None of the twelve knocked in. But the note sold in May came within {100 * (nearest - 0.5):.0f} "
                   "percent of its barrier, and the buyers of most of them waited through the fall for years before "
                   "they were repaid." if n_ki == 0 else
                   f"{n_ki} of the twelve knocked in.")
        with self.voiceover(
            "The first episode. Issue that note every month of 2015, the year the HSCEI peaked, and follow it on the "
            "real path. <bookmark mark='a'/> The index fell by almost half from its spring high to February 2016. "
            f"{verdict} The barrier at fifty percent held, just."
        ) as vo:
            self.play(FadeIn(g), Create(line), FadeIn(src), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m_) for m_ in marks], lag_ratio=0.15, run_time=3), FadeIn(side[1]),
                      FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def fsc2016(self):
        card = history_card(r"21 January 2016", r"Korea's Financial Services Commission",
                            r"HSCEI-linked ELS outstanding: 35.8 trillion won in June 2015, 37.0 trillion on 19 January "
                            r"2016. The index had fallen to 8,015 the day before. The regulator noted that a knock-in "
                            r"does not necessarily mean a loss, and announced closer monitoring of the ELS market".replace(
                                "8,015", "8{,}015"), color=QC.CRISIS, width=9.0, font_size=23)
        src = note(r"FSC press release, ``HSCEI-Linked ELS Market Conditions and Policy Response'', 21 January 2016",
                   font_size=17, color=GREY_B).to_corner(DR, buff=0.25)
        with self.voiceover(
            "The regulator's own document from that winter shows how large the exposure had become. On the "
            "twenty-first of January 2016, Korea's Financial Services Commission counted thirty-seven trillion won "
            "of HSCEI-linked notes outstanding, as the index fell to about eight thousand, and reminded investors "
            "that a knock-in does not necessarily mean a loss. In 2016 and 2017 the index largely recovered."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(src))
        self.wait(0.4)
        self.clear_scene()

    def notes(self, k):
        t = ymd_to_year(k["date"])
        px = np.asarray(k["close"])
        g = axes([2020, 2025], [3000, 13000], x_length=7.4, y_length=4.4, ylabel=r"HSCEI",
                 xticks=[2020, 2021, 2022, 2023, 2024, 2025], yticks=[4000, 8000, 12000],
                 yfmt=lambda u: f"{u:,.0f}".replace(",", "{,}"), font_size=16).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        line = curve(ax, t, px, SPOT, stroke_width=2.2)
        rows = k["rows"]
        marks = VGroup()
        for r in rows:
            t0 = ymd_to_year([r["start"]])[0]
            col = BAD if r["knocked_in"] else GOOD
            marks.add(VGroup(Dot(ax.c2p(t0, r["S0"]), radius=0.06, color=col),
                             DashedLine(ax.c2p(t0, 0.5 * r["S0"]), ax.c2p(min(t0 + 3, 2025), 0.5 * r["S0"]),
                                        stroke_color=col, stroke_width=1.2, dash_length=0.06)))
        lost = [r for r in rows if r["knocked_in"]]
        lo_l, hi_l = 100 * min(-r["return"] for r in lost), 100 * max(-r["return"] for r in lost)
        side = VGroup(
            wrapped_label(r"the second episode: the same terms, issued monthly through 2021, near the index's peak", 4.4,
                          18, GREY_A),
            wrapped_label(rf"{len(lost)} of {len(rows)} knocked in during 2022's fall and matured in 2024 with losses of "
                          rf"{lo_l:.0f} to {hi_l:.0f}\%", 4.4, 19, BAD),
            wrapped_label(r"the rest were redeemed or repaid with their coupon: the same product, a few months apart", 4.4,
                          19, GOOD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        pp = pause_card(r"Two notes with identical terms, issued four months apart. Why opposite outcomes?", width=4.6)
        pp.to_corner(UR, buff=0.3)
        src = real_data(r"Yahoo Finance: Hang Seng China Enterprises Index, daily; stylized terms, not any one bank's note")
        with self.voiceover(
            "The second episode. Here are notes issued each month of 2021, near the index's next peak. The dashed "
            "lines are their knock-ins. <bookmark mark='a'/> In 2022 the index fell through half of its early-2021 "
            f"level, and this time it stayed down. {len(lost)} of the {len(rows)} notes knocked in, and at maturity "
            f"in 2024 their buyers lost between {lo_l:.0f} and {hi_l:.0f} percent. <bookmark mark='b'/> Notes issued "
            "a few months later never touched their barriers and paid their coupons. Pause on why. Their terms were "
            "identical; their barriers sat at different index levels. A step-down sold near a peak inherits the "
            "index's drawdown from that peak, so for these notes the vintage mattered more than the terms."
        ) as vo:
            self.play(FadeIn(g), Create(line), FadeIn(src), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.15, run_time=3), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]), FadeIn(pp))
        self.wait(0.4)
        self.clear_scene()

    def file(self):
        card = crisis_card(
            r"2023 -- 2025", r"Korea's HSCEI-linked ELS",
            r"Korean banks and brokers sold HSCEI-linked equity-linked securities to savers, many of them retail customers "
            r"who had come in for deposits. About 19.3 trillion won were outstanding in mid-November 2023, 15.9 trillion "
            r"of it sold through banks, most of it maturing in 2024. Maturing notes lost 1.2 trillion won in January and "
            r"February 2024 alone. In March 2024 the Financial Supervisory Service set out a compensation scheme, "
            r"expecting most cases to be compensated at 20 to 60\% of the loss. In November 2025 it sent five banks "
            r"preliminary penalty notices totalling about 2 trillion won; the amount was not final.",
            stats=[(r"19.3\ \text{tn won}", r"outstanding, November 2023"), (r"1.2\ \text{tn won}", r"lost, Jan--Feb 2024"),
                   (r"20\text{--}60\%", r"compensation, the FSS's expected range")], width=11.8, font_size=23)
        card.move_to(ORIGIN)
        src = note(r"Korea Times and Korea Economic Daily (January 2024), Korea JoongAng Daily (11 March 2024; 28 November "
                   r"2025), citing the FSS", font_size=17, color=GREY_B).to_corner(DR, buff=0.2)
        with self.voiceover(
            "The real numbers, as reported from the regulator's figures. About 19.3 trillion won of these notes were "
            "outstanding in November 2023, 15.9 trillion of it sold through commercial banks, often to savers who had "
            "walked in for a deposit, and most of it due in 2024. In January and February 2024 alone, maturing "
            "notes lost 1.2 trillion won. That March, the Financial Supervisory Service laid out a compensation "
            "scheme, and said it expected most cases to be compensated at between a fifth and three-fifths of the "
            "loss. <bookmark mark='a'/> In November 2025 it sent five banks preliminary penalty notices totalling "
            "about two trillion won, an amount that was not yet final. Regulators faulted how the notes were sold, "
            "not their arithmetic: each was a short put, sold like a deposit with a coupon, to people who could not "
            "price it."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(src))
            vo.wait_until("a")
            self.play(Indicate(card.stats[2], color=QC.CRISIS))
        self.wait(0.5)
        self.clear_scene()

    def natixis(self):
        card = firm_card(
            r"Natixis, December 2018",
            r"The French bank, a large issuer of Korean autocallables, cut its fourth-quarter 2018 revenues by "
            r"EUR 100 million and set aside a EUR 160 million provision on ``some specific products traded with clients "
            r"in Asia'' in equity derivatives. It said the model used to manage them had led to ``a hedging strategy "
            r"that proved to be deficient'' in the market conditions of late 2018. Bloomberg reported that it stopped "
            r"creating the notes; Risk.net linked the loss to the size of its books and to products on a leveraged "
            r"Korean index.",
            numbers=[(r"\text{EUR }100\text{m}", r"revenue reduction, 4Q18"), (r"\text{EUR }160\text{m}", r"provision"),
                     (r"\approx \text{EUR }260\text{m}", r"in all")],
            source=r"Natixis / Groupe BPCE release, 18 December 2018; Bloomberg; Risk.net", width=11.6, font_size=22)
        card.move_to(ORIGIN)
        with self.voiceover(
            "The dealer's side of the same product. In December 2018 Natixis, one of the largest issuers of "
            "Korean autocallables, cut its fourth-quarter revenues by a hundred million euros and set aside a "
            "hundred and sixty million more, on what it called some specific products traded with clients in Asia. "
            "In its words, the model used to manage them had led to a hedging strategy that proved deficient in the "
            "market conditions. Bloomberg reported that it stopped creating the notes."
            " Many of those notes were written on several indices at once. Next: worst-of, and correlation."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()
