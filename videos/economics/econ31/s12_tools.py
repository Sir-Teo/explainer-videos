from __future__ import annotations

from videos.economics.econ31.common import *  # noqa: F403


class Tools(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Forward guidance, \ negative rates, \ yield-curve control", r"What did the other tools "
             r"achieve?", "Chapter ten. Forward guidance, negative rates, yield-curve control.",
             lit={2011: r"calendar guidance", 2014: r"negative rates", 2016: r"yield-curve control"},
             scale=("market", "nation"), horizon=("a day", "years"))
        self.guidance()
        self.negative()
        self.ycc()

    def guidance(self):
        rows = VGroup(
            label(r"forward guidance: \ promises about the path of the rate", font_size=27, color=E.ACCENT),
            label(r"August 2011: \ ``exceptionally low levels for the federal funds rate at least through mid-2013''",
                  font_size=21, color=CB),
            label(r"December 2012: \ at least while unemployment is above 6$\tfrac{1}{2}$\%, \ and inflation "
                  r"projected no more than \\ half a point above 2\%", font_size=21, color=CB),
            label(r"what it did: \ moved expected short rates \ (the 2-year yield) \ much more than the 10-year",
                  font_size=21, color=PRICE),
            label(r"Swanson: \ guidance moved short and medium yields; \ purchases moved the longest", font_size=21,
                  color=BOND),
            label(r"Part 30's puzzle: \ in the model, \ promises are worth far more than in the data", font_size=21,
                  color=HOLD),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        tag = published_tag(r"FOMC statements of 9 August 2011 and 12 December 2012; \ Swanson, \ \emph{JME} 118 "
                            r"(2021)", corner=DR, font_size=12)
        with self.voiceover(
            "At zero, a central bank can still promise. <bookmark mark='a'/> In August 2011 the Federal Reserve "
            "said it expected to keep its rate exceptionally low at least through mid-2013: a date. "
            "<bookmark mark='b'/> In December 2012 it swapped the date for conditions: at least as long as "
            "unemployment stayed above six and a half percent, and projected inflation no more than half a point "
            "above its two percent goal. <bookmark mark='c'/> Promises like these move what markets expect the "
            "rate to be over the next year or two, so they show up in two-year yields. <bookmark mark='d'/> Eric "
            "Swanson separated the two tools on announcement days: guidance moved short and medium-term yields, "
            "purchases moved the longest. <bookmark mark='e'/> Both worked in the expected direction. But none of "
            "them came close to the enormous power that Part 30's model gives a promise: the forward guidance "
            "puzzle, seen from the data's side."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def negative(self):
        Z = load("zlb")
        ax = plane([2008, 2027], [-1, 5], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.8, y_length=4.8,
                   xticks=[2008, 2012, 2016, 2020, 2024], yticks=[-1, 0, 1, 2, 3, 4], ylabel=r"percent",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:+.0f}" if v else "0", font_size=15)
        below = shade(ax, [(2008, 2027)], -1, 0, INFL, 0.08)
        zero = seg(ax, 2008, 0, 2027, 0, GREY_C, 1.5)
        ea = path(ax, Z["ecb_t"], Z["ecb"], COUNTRY["EA"], 3.2, xr=(2008, 2027), smooth=False)
        jp = path(ax, Z["jp_t"], Z["jp"], COUNTRY["JP"], 3.2, xr=(2008, 2027), smooth=False)
        side = VGroup(
            label(r"purple: \ the ECB's deposit rate", font_size=18, color=COUNTRY["EA"]),
            label(rf"June 2014 to July 2022: \\ below zero, \ down to {Z['ecb_min']:.1f}\%", font_size=18,
                  color=COUNTRY["EA"]),
            label(r"red: \ Japan's call rate, \\ below zero from 2016 to 2024", font_size=18, color=COUNTRY["JP"]),
            label(r"the floor is not zero: \\ it is the cost of holding cash", font_size=19, color=E.ACCENT),
            label(r"but banks rarely charged \\ households for deposits, \\ so their margins were squeezed",
                  font_size=18, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"ECB and OECD via FRED; \ Eggertsson, \ Juelsrud, \ Summers and Wold, \ NBER WP 25416 (2019)",
                       corner=DR, font_size=12)
        with self.voiceover(
            "Could the rate go below zero? <bookmark mark='a'/> The European Central Bank tried. "
            "<bookmark mark='b'/> From June 2014 it charged banks for holding reserves, and by 2019 the charge was "
            f"{abs(Z['ecb_min']):.1f} percent a year. <bookmark mark='c'/> The Bank of Japan followed in 2016. "
            "<bookmark mark='d'/> The true floor is not zero but the cost of storing cash instead, which is small "
            "but not nothing, and rates went a little below zero without a rush into banknotes. "
            "<bookmark mark='e'/> The catch was the banks. Few charged ordinary depositors, so the rates banks paid "
            "stayed near zero while the rates they earned fell, squeezing the margins that fund their lending: "
            "Gauti Eggertsson and coauthors found that in Sweden this blunted the cuts. Negative rates helped a "
            "little, and at a cost."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(below), FadeIn(zero), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(ea), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(Create(jp), FadeIn(side[2]), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def ycc(self):
        cards = point_cards([
            (r"Japan, \ 2016--2024", r"the 10-year yield held \\ around zero by promising \\ to buy whatever it "
                                     r"took", COUNTRY["JP"]),
            (r"Australia, \ 2020--2021", r"the 3-year yield held at 0.1\%: \\ the bank bought most of the \\ "
                                         r"target bond; \ dropped in \\ November 2021", PRICE),
            (r"the lesson", r"a yield target is a promise \\ that markets can test; \\ it holds until it is "
                            r"doubted", HOLD),
        ], width=12.8, cols=3, font_size=21).move_to(DOWN * 0.1)
        head = label(r"yield-curve control: \ a price for a long-term bond", font_size=27, color=E.ACCENT).to_edge(
            UP, buff=0.6)
        tag = published_tag(r"Bank of Japan, \ September 2016 and March 2024; \ Reserve Bank of Australia, \ "
                            r"\emph{Statement on Monetary Policy}, \ August 2021", corner=DR, font_size=12)
        with self.voiceover(
            "The third tool sets a price instead of a quantity. <bookmark mark='a'/> In September 2016 the Bank of "
            "Japan announced that it would hold the ten-year government bond yield around zero, buying whatever "
            "it took to do so. It kept the target in some form until March 2024. <bookmark mark='b'/> In March "
            "2020 the Reserve Bank of Australia held the three-year yield at a tenth of a percent. As inflation "
            "rose, markets bet against it; the bank ended up owning most of the bond it targeted, and in November "
            "2021 it gave up. <bookmark mark='c'/> A yield target is a promise that markets can test, every day. It "
            "holds while it is believed, which is a theme the euro crisis will make vivid in two chapters."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abc", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
