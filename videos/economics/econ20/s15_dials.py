from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ20.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 13, r"The Dials: \ how fast, \ and how much capital?", r"How fast do economies converge, \ and "
             r"how large is capital's share?", "Chapter thirteen. The Dials: how fast, and how much capital?",
             scale=("nation", "world"), lit={1992: r"MRW", 1995: r"Islam", 2022: r"Kremer, Willis and You"})
        self.speed()
        self.half_lives()
        self.share()

    def speed(self):
        dial = dials.DIALS["convergence_speed"]
        head = status_head(dial, r"the speed of convergence \ (new)")
        frame, rows = dial_rows(dial, 0, 7, [0, 1, 2, 3, 4, 5, 6, 7], r"percent of the gap closed a year",
                                top=1.9, step=0.75, fmt="{:.2f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 12.6, 16, GREY_A).to_edge(DOWN, buff=0.15)
        tag = published_tag(r"MRW (1992); \ Islam (1995); \ Kremer, Willis and You (2022)", corner=UR, font_size=12)
        mrw, oecd, islam, mine, kwy = dial.estimates
        with self.voiceover(
            "This part opens a dial: how fast do economies close the gap to their steady states? "
            f"<bookmark mark='a'/> Mankiw, Romer and Weil: {mrw.value:.1f} percent a year across ninety-eight "
            f"countries, and {oecd.value:.1f} percent among the rich ones, holding saving, population growth and "
            f"schooling fixed. <bookmark mark='b'/> Islam's panels, with a constant for each country: about "
            f"{islam.value:.0f} percent. <bookmark mark='c'/> This film's own estimate, on sixty years of the "
            f"newest data, with the same controls: about {mine.value:.1f} percent, with a wide interval. "
            "<bookmark mark='d'/> And Kremer, Willis and You's unconditional convergence since 2005, with no "
            f"controls at all: about {kwy.value:.1f} percent. <bookmark mark='e'/> The status: contested. Cross "
            "sections say one to two percent, panels say five or more, and the gap between them is a question of "
            "what each country is converging to."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
            vo.wait_until("e")
            self.play(FadeIn(meaning))
        self.clear_scene()

    def half_lives(self):
        dd = load("dial")
        dial = dials.DIALS["convergence_speed"]
        ax = plane([0, 100], [0, 1.0], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.4, y_length=4.8,
                   xticks=[0, 20, 40, 60, 80, 100], yticks=[0, 0.25, 0.5, 0.75, 1.0], xlabel=r"years",
                   ylabel=r"share of the gap left", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=16)
        t = np.linspace(0, 100, 201)
        cols = (OUTPUT, BREAK, TFP, E.ACCENT, CONS)
        lines, labs = VGroup(), VGroup()
        for e, c in zip(dial.estimates, cols):
            lines.add(path(ax, t, np.exp(-e.value / 100 * t), color=c, width=3))
            who = e.who.split(" (")[0].split(",")[0]
            labs.add(label(rf"{who} \ ({e.value:.1f}\%): \ half-life {np.log(2) / (e.value / 100):.0f} years",
                           font_size=17, color=c))
        labs.arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.3).shift(UP * 0.6)
        half = DashedLine(ax.ax.c2p(0, 0.5), ax.ax.c2p(100, 0.5), color=GREY_C, stroke_width=1.5)
        with self.voiceover(
            "What the range means is easier to see as half-lives. <bookmark mark='a'/> At one and a half percent a "
            "year, a quarter of any gap is still there after ninety years. "
            "<bookmark mark='b'/> At five percent, half the gap closes in fourteen years, and within a lifetime "
            "the gap is gone. <bookmark mark='c'/> Whether poverty is a matter of generations or of centuries "
            f"depends on which end of the dial is right. This film's {100 * dd['lambda_mine']:.1f} percent sits "
            "with the cross sections."
        ) as vo:
            self.play(FadeIn(ax), Create(half))
            vo.wait_until("a")
            self.play(Create(lines[0]), FadeIn(labs[0]), Create(lines[3]), FadeIn(labs[3]), run_time=2)
            vo.wait_until("b")
            self.play(Create(lines[2]), FadeIn(labs[2]), Create(lines[1]), FadeIn(labs[1]), run_time=2)
            vo.wait_until("c")
            self.play(Create(lines[4]), FadeIn(labs[4]), run_time=2)
        self.clear_scene()

    def share(self):
        dial = dials.DIALS["capital_share"]
        dd = load("dial")
        head = status_head(dial, r"capital's share \ (from Part 8)")
        frame, rows = dial_rows(dial, 0, 0.5, [0, 0.1, 0.2, 0.3, 0.4, 0.5], r"output elasticity of capital",
                                top=1.9, step=0.75, fmt="{:.3f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 12.6, 16, GREY_A).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "The second dial was opened in part eight: capital's share, the alpha that has run through this whole "
            "part. <bookmark mark='a'/> Cobb and Douglas's regression, Gollin's corrected labour shares, and the "
            "Penn World Table all put it between about 0.23 and 0.38. <bookmark mark='b'/> This part adds one "
            "row: Mankiw, Romer and Weil's augmented regression, 0.31 for physical capital, with human capital's "
            "0.28 beside it. <bookmark mark='c'/> The status stays settled within a range, for physical capital. "
            f"The American labour share since 1950 puts it at about {dd['capital_share_us']:.2f}. But the speed of "
            "convergence in the data fits a broad share, physical and human capital together, of three fifths or "
            "more: the dial depends on what you count as capital."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), LaggedStart(*[FadeIn(r_) for r_ in rows[:4]], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[4]))
            vo.wait_until("c")
            self.play(FadeIn(meaning))
        self.clear_scene()
