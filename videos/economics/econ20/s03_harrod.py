from __future__ import annotations

from videos.economics.econ20.common import *  # noqa: F403

SHADES = {"0.10": LABOUR, "0.14": CONS, "0.20": CAPITAL}


class Harrod(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Harrod, \ Domar \ and the planners", r"If every unit of output needs a fixed amount of capital, "
             r"how fast does an economy grow, \ and can it stay at full employment?",
             "Chapter two. Harrod, Domar and the planners.", lit={1939: r"Harrod", 1946: r"Domar",
                                                                  1999: r"Easterly's test"},
             scale=("nation",), horizon=("decades",))
        self.model()
        self.knife()
        self.planners()
        self.easterly()

    def model(self):
        h = load("harrod")
        rows = VGroup(
            MathTex(r"Y = \frac{K}{v}", font_size=54),
            MathTex(r"\Delta K = sY - \delta K", font_size=54),
            MathTex(r"g = \frac{\Delta K}{K} = \frac{s}{v} - \delta", font_size=60, color=E.ACCENT),
        ).arrange(DOWN, buff=0.45).shift(LEFT * 3.2)
        notes = VGroup(
            label(r"a fixed capital-output ratio $v$: \ 3.5 years of output", font_size=22, color=CAPITAL),
            label(r"saving $s$ becomes new capital; \ $\delta$ wears out", font_size=22, color=SAVE),
            label(rf"island: \ $s = 20\%$, \ $v = 3.5$, \ $\delta = 3\%$ \ $\Rightarrow$ \ {pc(h['growth_20'])} a "
                  rf"year", font_size=22, color=E.ACCENT),
        )
        for n_, r in zip(notes, rows):
            n_.next_to(r, RIGHT, buff=0.6).align_to(rows, RIGHT).shift(RIGHT * 6.3)
        hc = VGroup(label(r"Roy Harrod, \ 1939; \ Evsey Domar, \ 1946", font_size=26, color=GREY_A)).to_edge(
            UP, buff=0.4)
        tag = published_tag(r"Harrod, EJ 49(193) (1939); \ Domar, Econometrica 14(2) (1946)", corner=DR,
                            font_size=13)
        with self.voiceover(
            "Before Solow there was a simpler model, put forward by Roy Harrod in 1939 and Evsey Domar in 1946. "
            "<bookmark mark='a'/> It assumes every unit of output needs a fixed amount of capital: a capital-output "
            "ratio, v, of say three and a half years of output. <bookmark mark='b'/> Each year the saved share of "
            "output, s, becomes new capital, and a fraction delta of the old capital wears out. "
            "<bookmark mark='c'/> Put the two together and the growth rate is the saving rate divided by v, less "
            f"depreciation. On the island, saving a fifth of output, the economy grows by {100 * h['growth_20']:.1f} "
            "percent a year. More saving, more growth, for ever."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(tag))
            for mk, r, n_ in zip("abc", rows, notes):
                vo.wait_until(mk)
                self.play(Write(r), FadeIn(n_, shift=LEFT * 0.1))
        self.clear_scene()

    def knife(self):
        h = load("harrod")
        years = np.array(h["years"], float)
        ax = plane([0, 50], [np.log10(0.5), np.log10(2.5)], center=DOWN * 0.45 + LEFT * 2.2, x_length=7.4,
                   y_length=5.0, xticks=[0, 10, 20, 30, 40, 50],
                   yticks=[np.log10(v) for v in (0.5, 0.8, 1.0, 1.25, 1.6, 2.0, 2.5)],
                   ylabel=r"machines $\div$ workers to man them \ (log)", xlabel=r"years",
                   yfmt=lambda v: f"{10 ** v:.2f}".rstrip("0").rstrip("."), font_size=16)
        lines, labs = VGroup(), VGroup()
        for key, p in h["paths"].items():
            ratio = np.exp((p["growth"] - h["n"]) * years)
            ln = path(ax, years, np.log10(ratio), color=SHADES[key], width=4, smooth=False)
            lines.add(ln)
            end = ax.ax.c2p(50, np.log10(ratio[-1]))
            labs.add(label(rf"$s = {100 * float(key):.0f}\%$", font_size=20, color=SHADES[key]).next_to(end, RIGHT,
                                                                                                     buff=0.1))
        zones = VGroup(
            label(r"idle machines", font_size=19, color=CAPITAL).move_to(ax.ax.c2p(14, np.log10(1.7))),
            label(r"workers without machines", font_size=19, color=LABOUR).move_to(ax.ax.c2p(17, np.log10(0.62))),
        )
        side = VGroup(
            label(r"the knife edge", font_size=28, color=E.ACCENT),
            MathTex(r"s^\ast = v\,(n + \delta)", font_size=44),
            label(rf"$= 3.5 \times (1\% + 3\%) = {100 * h['warranted']:.0f}\%$", font_size=22, color=CONS),
            label(r"nothing in the model \\ makes saving pick it", font_size=22, color=HOLD),
        ).arrange(DOWN, buff=0.35).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.3)
        with self.voiceover(
            "But there is a catch, and Harrod saw it. <bookmark mark='a'/> Workers need machines, and machines need "
            "workers, in a fixed proportion. The island's labour force grows by one percent a year. "
            "<bookmark mark='b'/> Save ten percent and capital barely grows. Each year there are more workers "
            "without machines to work: unemployment rises without limit. <bookmark mark='c'/> Save twenty percent and "
            "capital outruns the workers: machines stand idle, and idle machines earn nothing. "
            f"<bookmark mark='d'/> Only one saving rate, {100 * h['warranted']:.0f} percent, the ratio times "
            "labour-force growth plus depreciation, keeps both fully used. <bookmark mark='e'/> Nothing in the model "
            "makes households save exactly that. Growth with full employment sits on a knife edge."
        ) as vo:
            self.play(FadeIn(ax))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(lines[0]), FadeIn(labs[0]), FadeIn(zones[1]))
            vo.wait_until("c")
            self.play(Create(lines[2]), FadeIn(labs[2]), FadeIn(zones[0]))
            vo.wait_until("d")
            self.play(Create(lines[1]), FadeIn(labs[1]), FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def planners(self):
        h = load("harrod")
        eq = MathTex(r"s_{\text{needed}} = v\,(g_{\text{target}} + \delta) = 3.5 \times (7\% + 3\%) = 35\%",
                     font_size=46).to_edge(UP, buff=0.9)
        bar_w = 9.0
        full = Rectangle(width=bar_w, height=0.6, stroke_color=GREY_B, stroke_width=1.5).next_to(eq, DOWN, buff=1.0)
        own = Rectangle(width=bar_w * 0.15 / 0.35, height=0.6, stroke_width=0, fill_color=SAVE,
                        fill_opacity=0.9).align_to(full, LEFT).align_to(full, UP)
        gap = Rectangle(width=bar_w * 0.20 / 0.35, height=0.6, stroke_width=0, fill_color=HOLD,
                        fill_opacity=0.6).next_to(own, RIGHT, buff=0)
        lo = label(r"own saving: \ 15\% of GDP", font_size=21, color=SAVE).next_to(own, DOWN, buff=0.15)
        lg = label(r"the financing gap: \ 20\% of GDP, \ from aid and loans", font_size=21,
                   color=HOLD).next_to(gap, DOWN, buff=0.15)
        rows = VGroup(
            label(r"India's Second Five-Year Plan \ (1956) \ ran on a capital-output arithmetic", font_size=22,
                  color=GREY_A),
            label(r"in the 1990s the World Bank and the IMF still used it to set targets for aid", font_size=22,
                  color=GREY_A),
            label(r"on Zambia, \ the Bank wrote: \ ``a useful (if simplistic) tool \ldots\ is an ICOR''",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(full, DOWN, buff=1.0)
        tag = published_tag(r"Easterly, Journal of Development Economics 60(2) (1999): \ 423--438", corner=DR,
                            font_size=13)
        with self.voiceover(
            "Knife edge or not, the model had one great attraction for planners: it turns a growth target into a "
            "number. <bookmark mark='a'/> To grow seven percent a year with a ratio of three and a half, a country "
            f"must invest {100 * h['needed_7']:.0f} percent of its output. <bookmark mark='b'/> If it saves only "
            "fifteen, the other twenty is a financing gap, to be filled by foreign aid and loans. "
            "<bookmark mark='c'/> Arithmetic of this kind ran through India's Second Five-Year Plan of 1956. "
            "<bookmark mark='d'/> Decades after economists had moved on, the international lenders were still using "
            "it. William Easterly found it in the 1990s in World Bank country reports, <bookmark mark='e'/> including "
            "one on Zambia that called the incremental capital-output ratio a useful, if simplistic, tool."
        ) as vo:
            self.play(Write(eq), FadeIn(tag), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(full), FadeIn(own), FadeIn(lo))
            vo.wait_until("b")
            self.play(FadeIn(gap), FadeIn(lg))
            for mk, r in zip("cde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def easterly(self):
        h = load("harrod")["easterly"]
        sc = study_card(r"The ghost of financing gap", r"William Easterly, \ 1999: \ testing the growth model used in "
                        r"the international financial institutions", [
            (r"test", rf"aid raises investment one for one; \ investment raises growth a year later, \ with a "
                      rf"capital-output ratio of {h['icor']}"),
            (r"data", rf"aid recipients, \ {h['years'].replace('-', '--')}"),
            (r"Zambia", r"with all aid invested, \ income per head would have climbed to about 20{,}000 dollars; "
                        r"\ it fell to about 600"),
            (r"all", r"predicted and actual growth: \ a correlation slightly below zero"),
        ], design="regression", width=11.6, font_size=23).move_to(UP * 0.2)
        why = label(r"what the model leaves out: \ a fixed $v$ means capital and labour cannot substitute",
                    font_size=23, color=E.ACCENT).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "So Easterly tested it. <bookmark mark='a'/> Suppose, as the model does, that aid becomes investment one "
            "for one, and investment becomes growth a year later, with a capital-output ratio of three and a half. "
            "<bookmark mark='b'/> He ran the prediction for the countries that received aid from 1961 to the early "
            "nineties. <bookmark mark='c'/> Zambia got a great deal of aid. If the model were right, its income per "
            "head would have climbed to about twenty thousand dollars, the income of an industrial country. It fell "
            "to about six hundred. <bookmark mark='d'/> Across all the recipients, the correlation between the growth "
            "the model predicted and the growth that happened was slightly negative. <bookmark mark='e'/> Part of the "
            "failure is the fixed ratio itself. If capital and workers can be combined in different proportions, "
            "the knife edge disappears, and so does the promise that saving alone buys growth for ever. That is "
            "Solow's model."
        ) as vo:
            rest = [m for m in sc if m is not sc[1]]
            self.play(*[FadeIn(m) for m in rest], FadeIn(sc.head))
            for mk, r in zip("abcd", sc.body):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(why, shift=UP * 0.1))
        self.clear_scene()
