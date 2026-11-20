from __future__ import annotations

from videos.economics.econ30.common import *  # noqa: F403


class Evidence(VoiceoverScene):
    def construct(self):
        card(self, 2, r"The evidence on price setting", r"How do firms actually set their prices?", "Chapter two. "
             "The evidence on price setting.", lit={1986: r"Cecchetti", 1998: r"Blinder and coauthors"},
             scale=("firm",), horizon=("a month", "a year"))
        self.surveys()
        self.spread()
        self.facts()

    def surveys(self):
        rows = VGroup(
            label(r"three ways to look", font_size=28, color=E.ACCENT),
            label(r"Cecchetti, \ 1986: \ magazine cover prices change rarely, \ and more often when inflation is "
                  r"high", font_size=22, color=PRICE),
            label(r"Blinder and coauthors, \ 1998: \ ask 200 firms; \ the median firm reprices about once a year",
                  font_size=22, color=CB),
            label(r"their top-rated reason: \ coordination, \ nobody wants to move first; \ contracts with "
                  r"customers also rank high", font_size=22, color=GREY_A),
            label(r"the price collectors' records: \ millions of prices, \ each followed through time", font_size=22,
                  color=STICKY),
            label(r"all three agree: \ many prices stay fixed for months, \ though some move every week", font_size=23,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Cecchetti, \ \emph{J.\ Econometrics} 31(3) (1986); \ Blinder, \ Canetti, \ Lebow and "
                            r"Rudd, \ \emph{Asking About Prices} (1998)", corner=DR, font_size=12)
        with self.voiceover(
            "There are three ways to find out how prices are set. <bookmark mark='a'/> Follow one product for "
            "decades. Stephen Cecchetti followed the newsstand prices of American magazines, and found they "
            "changed rarely, and more often when inflation was high. <bookmark mark='b'/> Ask. Alan Blinder and "
            "his coauthors interviewed the price setters of two hundred American firms in the 1990s: the median "
            "firm changed its price about once a year. <bookmark mark='c'/> The explanation they rated highest was "
            "coordination: nobody wants to raise prices first. Contracts with customers, written or understood, "
            "also ranked high. "
            "<bookmark mark='d'/> Or read the records, as Bils, Klenow, Nakamura and Steinsson did. "
            "<bookmark mark='e'/> All three agree. Many prices stay fixed for months, even though some change every "
            "week."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def spread(self):
        S = load("sticky")
        t = np.array(S["t"])
        k = (t >= 1985) & (t < 2020)
        ax = plane([1985, 2020], [-4, 8], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.8, y_length=4.8,
                   xticks=[1985, 1995, 2005, 2015], yticks=[-4, 0, 4, 8], ylabel=r"inflation over 12 months, \ \%",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=15)
        zero = seg(ax, 1985, 0, 2020, 0, GREY_D, 1.5)
        flex = path(ax, t[k], np.clip(np.array(S["flex"])[k], -4, 8), FLEX, 2.2, smooth=False)
        stk = path(ax, t[k], np.clip(np.array(S["sticky"])[k], -4, 8), STICKY, 3, smooth=False)
        side = VGroup(
            label(r"1985--2019", font_size=21, color=E.ACCENT),
            label(rf"flexible prices: \\ s.d.\ {S['sd_flex']:.1f} points", font_size=20, color=FLEX),
            label(rf"sticky prices: \\ s.d.\ {S['sd_sticky']:.1f} points", font_size=20, color=STICKY),
            label(r"a sticky price must \\ look ahead: \ it will be \\ in force for months", font_size=20,
                  color=GREY_A),
            label(r"so sticky inflation \\ carries expectations", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Bryan and Meyer, \ Federal Reserve Bank of Atlanta (2010); \ data via FRED",
                            corner=DR, font_size=12)
        with self.voiceover(
            "The Atlanta Fed's two indexes show what the difference does in calmer times. "
            f"<bookmark mark='a'/> From 1985 to 2019, <bookmark mark='b'/> inflation in the flexible prices had a "
            f"standard deviation of {S['sd_flex']:.1f} points; <bookmark mark='c'/> in the sticky prices, "
            f"{S['sd_sticky']:.1f}. <bookmark mark='d'/> A price that will be in force for months has to be set "
            "with the future in mind. <bookmark mark='e'/> So sticky-price inflation carries what firms expect, "
            "and Michael Bryan and Brent Meyer found it the better guide to where inflation is heading."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag), Create(flex), Create(stk), run_time=1.5)
            for mk, r_ in zip("abcde", side):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def facts(self):
        f = next(x for x in facts.FACTS if x.key == "sticky_prices")
        data_m = label(r"median duration: \\ 4.3 months with sales, \\ 8--11 without", font_size=18, color=WHITE)
        theory_m = label(r"menu costs, \ contracts, \\ coordination: \\ chapter three", font_size=18, color=PRICE)
        agora_m = label(r"the Island: \ a price \\ lasts 9 months \\ on average (Calvo)", font_size=18,
                        color=E.AGORA)
        fc = fact_card(tex_safe(f.statement), columns=((r"the data", data_m), (r"the theory", theory_m),
                                                         (r"Agora", agora_m)), width=12.4, font_size=22,
                       colors=(WHITE, PRICE, None)).move_to(UP * 0.3)
        tag = published_tag(r"Bils and Klenow (2004); \ Nakamura and Steinsson (2008); \ the Island", corner=DR,
                            font_size=12)
        with self.voiceover(
            "That is one of the series' facts. <bookmark mark='a'/> In the data, the median price lasts four point "
            "three months counting sales, eight to eleven without. <bookmark mark='b'/> The theory of why comes "
            "next. <bookmark mark='c'/> And the Island's prices, from chapter five on, last nine months on average, "
            "the calibration in Jordi Galí's textbook, between the two."
        ) as vo:
            self.play(FadeIn(fc.card), FadeIn(fc[1][0]), *[FadeIn(c[:2]) for c in fc.cols], FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(fc.cols[0][2:]))
            vo.wait_until("b")
            self.play(FadeIn(fc.cols[1][2:]))
            vo.wait_until("c")
            self.play(FadeIn(fc.cols[2][2:]))
        self.clear_scene()
