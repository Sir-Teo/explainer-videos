from __future__ import annotations

from videos.economics.econ32.common import *  # noqa: F403


class Austerity(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Austerity, \ and the 90\% threshold recomputed", r"Can cutting a deficit raise growth? \ Does "
             r"debt above 90\% of GDP stop it?", "Chapter seven. Austerity, and the ninety percent threshold "
             "recomputed.", lit={2010: r"Alesina and Ardagna", 2014: r"Herndon, \ Ash and Pollin"},
             scale=("nation",), horizon=("a year", "decades"))
        self.expansionary()
        self.steps()
        self.cloud()

    def expansionary(self):
        rows = VGroup(
            label(r"expansionary austerity?", font_size=27, color=E.ACCENT),
            label(r"Alesina and Ardagna: \ big consolidations, \ especially spending cuts, \ sometimes came with "
                  r"growth", font_size=22, color=SPEND),
            label(r"the reply: \ a cut in the deficit measured from the data partly reflects good times already "
                  r"coming", font_size=22, color=HOLD),
            label(r"Guajardo, \ Leigh and Pescatori: \ consolidations found in policy documents \ (as the Romers did) "
                  r"lowered output", font_size=22, color=TAX),
            label(r"the same identification problem, \ the same cure: \ ask why the budget changed", font_size=23,
                  color=WHITE),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Alesina and Ardagna, \ \emph{Tax Policy and the Economy} 24 (2010); \ Guajardo, \ Leigh "
                            r"and Pescatori, \ \emph{JEEA} 12(4) (2014)", corner=DR, font_size=12)
        with self.voiceover(
            "After 2010 governments in Europe argued that cutting deficits could raise growth by restoring "
            "confidence. <bookmark mark='a'/> Alberto Alesina and Silvia Ardagna had found that large "
            "consolidations, especially those made by cutting spending, sometimes came with growth. "
            "<bookmark mark='b'/> The reply was the identification problem again. A deficit that shrinks in the "
            "data often shrinks because good times are already coming, which flatters austerity. "
            "<bookmark mark='c'/> Jaime Guajardo, Daniel Leigh and Andrea Pescatori did what the Romers did for "
            "taxes: they found consolidations in policy documents, adopted to cut deficits rather than in response "
            "to the economy, and those lowered output. <bookmark mark='d'/> Ask why the budget changed, and "
            "austerity looks contractionary, as the evidence on multipliers says it should."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def steps(self):
        H = load("hap")
        st = H["steps"]
        ax = plane([0, 5.4], [-1, 3], center=LEFT * 1.4 + DOWN * 0.4, x_length=9.2, y_length=4.4, xticks=[],
                   yticks=[-1, 0, 1, 2, 3], ylabel=r"average growth above 90\% of GDP, \ \% a year",
                   yfmt=lambda v: f"{v:+.0f}" if v else "0", font_size=15)
        zero = seg(ax, 0, 0, 5.4, 0, GREY_C, 1.5)
        names = (r"published", r"New Zealand's \\ figure as in \\ the data", r"the five \\ countries back",
                 r"the excluded \\ years back", r"each country-year \\ counted once")
        bars, labs = VGroup(), VGroup()
        for k, (s_, n) in enumerate(zip(st, names)):
            v = s_["means"][3]
            p0, p1 = ax.ax.c2p(0.25 + k * 1.03, 0), ax.ax.c2p(0.95 + k * 1.03, v)
            col = INFL if k == 0 else (OUTPUT if k == 4 else DEBT)
            bars.add(Rectangle(width=p1[0] - p0[0], height=abs(p1[1] - p0[1]) + 1e-3, fill_color=col,
                               fill_opacity=0.85, stroke_width=0).move_to((p0 + p1) / 2))
            vt = 0.0 if abs(v) < 0.05 else v
            labs.add(VGroup(label(rf"{vt:+.1f}\%", font_size=18, color=col).next_to(bars[-1], UP if v >= 0 else DOWN,
                                                                         buff=0.08),
                            label(n, font_size=14, color=GREY_A).next_to(ax.ax.c2p(0.6 + k * 1.03, -1), DOWN,
                                                                         buff=0.1)))
        foot = label(rf"below 90\%: \ {st[-1]['means'][2]:.1f}\% \ (60--90) \ and "
                     rf"{st[-1]['means'][1]:.1f}\% \ (30--60): "
                     r"\ slower, \ no cliff", font_size=21, color=E.ACCENT).to_edge(UP, buff=0.4)
        tag = data_tag(r"Herndon, \ Ash and Pollin's replication data \ (Reinhart and Rogoff's spreadsheet); \ this "
                       r"film", corner=DR, font_size=12)
        with self.voiceover(
            "Now the ninety percent result, recomputed here from Herndon, Ash and Pollin's copy of the original "
            f"data. <bookmark mark='a'/> The published figure: {say_num(st[0]['means'][3], 1)} percent. "
            "<bookmark mark='b'/> Use New Zealand's growth as it is in the data, rather than the figure "
            f"transcribed: {say_num(st[1]['means'][3], 1)}. <bookmark mark='c'/> Put the five countries back: "
            f"{say_num(st[2]['means'][3], 1)}. <bookmark mark='d'/> Put back the years of high debt and decent "
            "growth in Australia, Canada and New Zealand that had been left out: "
            f"{st[3]['means'][3]:.1f}. <bookmark mark='e'/> And count each country-year once, rather than giving "
            f"New Zealand's single year the weight of Britain's nineteen: {st[4]['means'][3]:.1f} percent. "
            "<bookmark mark='f'/> Growth above ninety percent is slower than in the bands below it, "
            f"{st[-1]['means'][2]:.1f} percent between sixty and ninety, but there is no cliff."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag), run_time=0.6)
            for k, mk in enumerate("abcde"):
                vo.wait_until(mk)
                self.play(GrowFromEdge(bars[k], DOWN if st[k]["means"][3] >= 0 else UP), FadeIn(labs[k]))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()

    def cloud(self):
        H = load("hap")
        sc = np.array(H["scatter"])
        ax = plane([0, 250], [-12, 16], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.8, y_length=4.8,
                   xticks=[0, 30, 60, 90, 150, 250], yticks=[-10, -5, 0, 5, 10, 15],
                   xlabel=r"public debt, \ \% of GDP", ylabel=r"real growth that year, \ \%",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:+.0f}" if v else "0", font_size=15)
        line90 = vline(ax, 90, -12, 16, INFL, 2)
        pts = VGroup(*[Dot(ax.ax.c2p(a, b), radius=0.025, color=DEBT) for a, b in sc if -12 <= b <= 16])
        side = VGroup(
            label(rf"{len(sc)} country-years, \\ {H['n_countries']} countries, \ 1946--2009", font_size=18,
                  color=DEBT),
            label(r"no break at 90\%", font_size=19, color=INFL),
            label(r"and the arrow can point \\ the other way: \ slow growth \\ raises the debt ratio", font_size=18,
                  color=HOLD),
            label(r"a correlation, \ not a threshold", font_size=20, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Herndon, \ Ash and Pollin's replication data", corner=DR, font_size=12)
        with self.voiceover(
            "Here is every country-year in the data. <bookmark mark='a'/> There is a mild downward drift, "
            "<bookmark mark='b'/> but nothing happens at ninety percent. <bookmark mark='c'/> And the correlation "
            "does not say which way the arrow points: a recession or a decade of slow growth raises the ratio of "
            "debt to GDP by itself, through the denominator and through the deficits slumps bring. "
            "<bookmark mark='d'/> Reinhart and Rogoff acknowledged the spreadsheet error and defended the broader "
            "point that high debt goes with slower growth. That correlation survives. The threshold, and the "
            "direction of cause, do not follow from it."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.002), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(line90), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
