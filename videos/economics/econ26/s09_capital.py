from __future__ import annotations

from videos.economics.econ26.common import *  # noqa: F403


class Capital(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Capital", r"How big should the buffer be, \ and what counts as risky?", "Chapter eight. "
             "Capital.", lit={1988: r"Basel I", 2013: r"Admati and Hellwig"}, scale=("firm",), horizon=("years",))
        self.buffer()
        self.rates_shock()
        self.debate()

    def buffer(self):
        c = load("capital")
        ax = plane([1988, 2021], [5, 12.5], center=LEFT * 1.8 + DOWN * 0.3, x_length=8.4, y_length=4.8,
                   xticks=[1990, 2000, 2010, 2020], yticks=[6, 8, 10, 12], ylabel=r"US banks' equity, \ \% of total "
                   r"assets", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=16)
        line_ = path(ax, c["t"], c["v"], color=EQUITY, width=3, smooth=False)
        side = VGroup(
            label(rf"{c['first_date'][:4]}: \ {c['first']:.1f}\%", font_size=21, color=EQUITY),
            label(rf"{c['last_date'][:4]}: \ {c['last']:.1f}\%", font_size=21, color=EQUITY),
            label(r"equity absorbs losses \\ before depositors \\ or the insurer", font_size=20, color=GREY_A),
            label(r"so about one dollar in ten \\ of a bank's assets \\ is its owners' money", font_size=20,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"FFIEC: \ equity capital to total assets, \ all US banks, \ via FRED", corner=DR,
                       font_size=12)
        with self.voiceover(
            "The other answer to moral hazard is capital: make the owners put in money of their own, which is lost "
            "first. <bookmark mark='a'/> In 1988, American banks' equity was about "
            f"{c['first']:.0f} percent of their assets. <bookmark mark='b'/> By 2020 it was about {c['last']:.0f}. "
            "<bookmark mark='c'/> Equity absorbs losses before depositors or the insurer lose anything. "
            "<bookmark mark='d'/> Even so, about nine dollars in ten of what a bank owns is financed by borrowing."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(line_), run_time=2)
            for mk, r_ in zip("abcd", side):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
        self.clear_scene()

    def rates_shock(self):
        S = load("sheet")
        s = load("svb")
        rows = VGroup(
            label(r"risk weights: \ capital is measured against \emph{risk-weighted} assets", font_size=23,
                  color=GREY_A),
            label(rf"the Island's bank: \ loans weighted 1, \ government bonds 0: \ equity "
                  rf"{100 * S['risk_based']:.1f}\% of risk-weighted assets", font_size=23, color=EQUITY),
            label(rf"rates rise {100 * (S['y1'] - S['y0']):.0f} points: \ its ten-year bonds lose "
                  rf"{-100 * S['change']:.1f}\% \ (duration {S['duration']:.1f} years)", font_size=23, color=BOND),
            label(rf"a loss of {S['loss']:.1f} on 30 of bonds: \ equity falls to {S['equity'] - S['loss']:.1f}, \ "
                  rf"{100 * S['after_loss']:.1f}\% of assets", font_size=23, color=RUN),
            label(rf"Silicon Valley Bank, \ end of 2022: \ held-to-maturity bonds of \${s['htm_book'] / 1e9:.0f} "
                  rf"billion, \ worth \${s['htm_gap'] / 1e9:.0f} billion less than their book value", font_size=21,
                  color=HOLD),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        tag = published_tag(r"the Island; \ Silicon Valley Bank's year-end 2022 accounts, \ as reported", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Capital rules count risk. <bookmark mark='a'/> Each asset gets a weight, and capital is measured "
            "against the weighted total. <bookmark mark='b'/> Government bonds have no credit risk, so they get a "
            f"weight of zero, and the Island's bank looks well capitalized: {100 * S['risk_based']:.0f} percent of "
            "risk-weighted assets. <bookmark mark='c'/> But government bonds have interest-rate risk. If rates rise "
            f"three points, its ten-year bonds lose {-100 * S['change']:.0f} percent of their value. "
            f"<bookmark mark='d'/> That is a loss of {S['loss']:.1f}, leaving equity of {S['equity'] - S['loss']:.1f}: "
            f"{100 * S['after_loss']:.0f} percent of its assets. <bookmark mark='e'/> Silicon Valley Bank ended 2022 "
            f"with {s['htm_book'] / 1e9:.0f} billion dollars of bonds it planned to hold to maturity, worth about "
            f"{s['htm_gap'] / 1e9:.0f} billion less than their book value, while its reported capital ratio was "
            f"{100 * s['cet1']:.0f} percent. The loss was real only if it had to sell. A run makes you sell."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def debate(self):
        rows = VGroup(
            label(r"how much capital?", font_size=28, color=E.ACCENT),
            label(r"banks: \ equity is expensive; \ more of it means less lending", font_size=23, color=LOAN),
            label(r"Admati and Hellwig, \ 2013: \ equity is expensive only because debt is subsidized; \ ask for "
                  r"20 to 30\% of assets", font_size=22, color=EQUITY),
            label(r"Modigliani and Miller \ (Part 23): \ more equity makes each share safer, \ so its required return "
                  r"falls", font_size=22, color=GREY_A),
            label(r"the rules today are well below their number; \ the argument continues", font_size=22,
                  color=HOLD),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Admati and Hellwig, \emph{The Bankers' New Clothes} (2013)", corner=DR, font_size=12)
        with self.voiceover(
            "How much capital, then? <bookmark mark='a'/> Banks argue that equity is expensive, so requiring more "
            "of it means less lending. <bookmark mark='b'/> Anat Admati and Martin Hellwig argued in 2013 that equity "
            "is expensive for banks mainly because their debt is subsidized, by insurance and expected rescues, and "
            "proposed equity of twenty to thirty percent of total assets. <bookmark mark='c'/> Their argument is "
            "Modigliani and Miller's, from Part twenty-three: more equity makes each share safer, so the return "
            "shareholders require falls. <bookmark mark='d'/> Today's rules require much less than their number, "
            "and the argument continues."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
