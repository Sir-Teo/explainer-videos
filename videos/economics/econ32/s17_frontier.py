from __future__ import annotations

from videos.economics.econ32.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 15, r"Frontier: \ fiscal space when r is near g", r"How much room do governments have now?",
             "Chapter fifteen. Frontier: fiscal space when r is near g.", lit={2022: r"rates rise again"},
             scale=("nation", "world"), horizon=("a year", "decades"))
        self.interest()
        self.open_()

    def interest(self):
        I = load("interest")
        D = load("debt")
        t = np.array(I["t"])
        ax = plane([1947, 2027], [0, 6], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.8, y_length=4.8,
                   xticks=[1950, 1970, 1990, 2010, 2025], yticks=[0, 1, 2, 3, 4, 5, 6],
                   ylabel=r"federal interest payments, \ \% of GDP", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=15)
        line = path(ax, t, I["share"], RATE, 3.2, smooth=False)
        side = VGroup(
            label(rf"the 1980s and 1990s: \ up to {I['peak_80s']:.1f}\%", font_size=18, color=RATE),
            label(rf"the 2010s: \ as low as {I['min']:.1f}\%, \\ with debt rising", font_size=18, color=OUTPUT),
            label(rf"now: \ {I['last']:.1f}\%, \ \${I['level_last'] / 1000:.2f} trillion a year, \\ with debt at "
                  rf"{D['last']:.0f}\% of GDP", font_size=18, color=INFL),
            label(r"the same debt costs more \\ when r rises toward g", font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"BEA via FRED; \ OMB via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "The frontier is a world in which r is no longer far below g. <bookmark mark='a'/> Federal interest "
            f"payments reached {I['peak_80s']:.1f} percent of GDP in the 1980s and 1990s, when rates were high. "
            "<bookmark mark='b'/> In the 2010s they fell to as little as "
            f"{I['min']:.1f} percent, although debt was rising, because rates were so low. <bookmark mark='c'/> Now "
            f"they are {I['last']:.1f} percent of GDP, about {I['level_last'] / 1000:.1f} trillion dollars a year, "
            f"with debt at {D['last']:.0f} percent of GDP. <bookmark mark='d'/> Blanchard's arithmetic still "
            "holds, but the margin is thinner: the same debt costs more as r rises toward g."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.6)
            self.play(Create(line), run_time=2.0)
            for mk, s_ in zip("abcd", side):
                vo.wait_until(mk)
                self.play(FadeIn(s_))
        self.clear_scene()

    def open_(self):
        rows = VGroup(
            label(r"open questions", font_size=27, color=E.ACCENT),
            label(r"how far debt can rise before r rises with it", font_size=21, color=DEBT),
            label(r"whether multipliers are larger in slumps, \ and at the zero bound in practice", font_size=21,
                  color=SPEND),
            label(r"how to pay for investment in the climate transition: \ borrow, \ tax, \ or price carbon (Part 48)",
                  font_size=21, color=OUTPUT),
            label(r"how fiscal and monetary policy share the job of controlling inflation", font_size=21,
                  color=INFL),
            label(r"why tax multipliers look so large", font_size=21, color=TAX),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Blanchard (2019); \ Ramey (2019); \ Cochrane (2023)", corner=DR, font_size=12)
        with self.voiceover(
            "The open questions. <bookmark mark='a'/> How far debt can rise before interest rates rise with it. "
            "<bookmark mark='b'/> Whether multipliers really are larger in slumps and at the zero bound. "
            "<bookmark mark='c'/> How to pay for the investment the climate transition needs: by borrowing, by "
            "taxes, or by pricing carbon, which Part 48 takes up. <bookmark mark='d'/> How fiscal and monetary "
            "policy share the job of controlling inflation. <bookmark mark='e'/> And why tax multipliers look so "
            "much larger than spending ones."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
