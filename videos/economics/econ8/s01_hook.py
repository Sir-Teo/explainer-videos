from __future__ import annotations

from videos.economics.econ8.common import *  # noqa: F403


def douglas_axes(center=LEFT * 3.1 + DOWN * 0.3, x_length=6.6, y_length=5.4):
    import math

    return plane([1899, 1922], [math.log10(90), math.log10(460)], center=center, x_length=x_length,
                 y_length=y_length, xticks=[1900, 1905, 1910, 1915, 1920],
                 yticks=[math.log10(v) for v in (100, 150, 200, 300, 400)],
                 xlabel=r"American manufacturing", ylabel=r"index, 1899 = 100 \ (log scale)", font_size=17,
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{10 ** v:.0f}")


def series(ax, years, vals, color, width=3.5):
    a = ax.ax
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(
        [a.c2p(y, np.log10(v)) for y, v in zip(years, vals)])


class Hook(VoiceoverScene):
    def construct(self):
        self.chart()
        self.cobb()
        self.share()
        self.coase()
        self.question()
        self.title()
        self.objectives()

    def chart(self):
        d = load("douglas")
        ax = douglas_axes()
        years = d["years"]
        lK, lL, lY = (series(ax, years, d[k], c) for k, c in (("K", CAP), ("L", LAB), ("Y", OUT)))
        names = VGroup(label(r"capital", font_size=22, color=CAP).next_to(lK.get_end(), RIGHT, buff=0.1),
                       label(r"labour", font_size=22, color=LAB).next_to(lL.get_end(), RIGHT, buff=0.1),
                       label(r"output", font_size=22, color=OUT).next_to(lY.get_end(), RIGHT, buff=0.1))
        a = ax.ax
        i = list(years).index(1920)
        gap = VGroup(DashedLine(a.c2p(1920, np.log10(d["L"][i])), a.c2p(1920, np.log10(d["K"][i])), color=GREY_B,
                                stroke_width=2),
                     Dot(a.c2p(1920, np.log10(d["Y"][i])), radius=0.07, color=OUT))
        side = VGroup(
            label(r"1927", font_size=30, color=E.ACCENT),
            label(r"Paul Douglas plots three series \\ for 1899--1922, \ on a log scale", font_size=24),
            label(r"capital more than quadruples; \\ labour grows by three fifths", font_size=23, color=GREY_A),
            label(rf"output lies about a quarter of the way \\ from labour to capital: \\ on average "
                  rf"{d['where_mean']:.2f}", font_size=24, color=OUT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.4)
        tag = published_tag(r"Cobb and Douglas (1928), via Felipe and Adams, EEJ (2005), table 1", corner=DR,
                            font_size=13)
        with self.voiceover(
            "In 1927 Paul Douglas, an economist at the University of Chicago, drew a chart. <bookmark mark='a'/> Three series for American manufacturing, from 1899 to 1922, on a "
            "logarithmic scale: the stock of fixed capital, <bookmark mark='b'/> the number of workers, "
            "<bookmark mark='c'/> and the output of the factories. Capital had more than quadrupled; the workforce "
            "had grown by three fifths. <bookmark mark='d'/> And output, year after year, lay between them, about a "
            "quarter of the way from the line for labour to the line for capital. A regularity like that asks for a "
            "law."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(lK), FadeIn(names[0]), FadeIn(side[1]), run_time=2)
            vo.wait_until("b")
            self.play(Create(lL), FadeIn(names[1]), run_time=1.6)
            vo.wait_until("c")
            self.play(Create(lY), FadeIn(names[2]), FadeIn(side[2]), run_time=1.6)
            vo.wait_until("d")
            self.play(Create(gap), FadeIn(side[3]))
        self.clear_scene()

    def cobb(self):
        d = load("douglas")
        ax = douglas_axes()
        years = d["years"]
        lY = series(ax, years, d["Y"], OUT)
        fit = DashedVMobject(series(ax, years, d["fitted_crs"], WHITE, width=3), num_dashes=60)
        legend = VGroup(label(r"output", font_size=21, color=OUT),
                        label(r"the formula", font_size=21, color=WHITE)).arrange(DOWN, aligned_edge=LEFT,
                                                                                  buff=0.1)
        legend.move_to(ax.ax.c2p(1902, np.log10(330)), aligned_edge=LEFT)
        hc = history_card(r"1927--28", r"Charles Cobb, \ mathematics, \ Amherst", r"Douglas asks his friend for a "
                          r"function that would measure the effect of each factor", color=E.ACCENT, width=5.2,
                          font_size=21).to_edge(RIGHT, buff=0.4).to_edge(UP, buff=0.5)
        eq = MathTex(rf"P' = {d['A']:.2f}\, L^{{3/4}}\, C^{{1/4}}", font_size=46, color=OUT).next_to(hc, DOWN,
                                                                                                 buff=0.45)
        notes = VGroup(
            label(rf"fitted to the data: \ labour {d['crs']['labour']:.3f}, \ capital {d['crs']['capital']:.3f}",
                  font_size=22),
            label(r"the exponents matched labour's \\ and capital's shares of income", font_size=22,
                  color=GREY_A),
            label(r"``A Theory of Production'', \ \emph{AER} (1928)", font_size=21, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(eq, DOWN, buff=0.35).align_to(hc, LEFT)
        tag = published_tag(r"Cobb and Douglas (1928); the fit computed on their data", corner=DR, font_size=13)
        with self.voiceover(
            "Douglas went to a friend on the mathematics faculty at Amherst, Charles Cobb, <bookmark mark='a'/> and "
            "asked him for a function that would measure the effect of each factor on output. "
            "<bookmark mark='b'/> What they found, presented at the American Economic Association's meetings of "
            "1927 and published in 1928, was this: output equals one point oh one times labour to the three "
            "quarters times capital to the one quarter. <bookmark mark='c'/> It tracked the factories' output "
            "closely, boom and slump. <bookmark mark='d'/> And the exponents, three quarters and a quarter, were "
            "close to the shares of manufacturing income that went to labour and to capital. Douglas took that as "
            "evidence that workers and owners were paid what they contributed."
        ) as vo:
            self.play(FadeIn(ax), Create(lY), FadeIn(legend[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(Write(eq))
            vo.wait_until("c")
            self.play(Create(fit), FadeIn(legend[1]), FadeIn(notes[0]), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(notes[1]), FadeIn(notes[2]))
        self.clear_scene()

    def share(self):
        s = load("share")
        years, v = np.array(s["years"]), np.array(s["share"])
        ax = plane([1950, 2023], [0.5, 0.7], center=LEFT * 3.0 + DOWN * 0.3, x_length=6.8, y_length=5.0,
                   xticks=[1950, 1970, 1990, 2010], yticks=[0.5, 0.55, 0.6, 0.65, 0.7], xlabel=r"year",
                   ylabel=r"labour's share of US GDP", font_size=17, xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"{100 * y:.0f}\\%")
        line = VMobject(stroke_color=LAB, stroke_width=3.5).set_points_as_corners(
            [ax.ax.c2p(y, x) for y, x in zip(years, v)])
        band = Polygon(ax.ax.c2p(1950, s["min_1950_1999"]), ax.ax.c2p(1999, s["min_1950_1999"]),
                       ax.ax.c2p(1999, s["max_1950_1999"]), ax.ax.c2p(1950, s["max_1950_1999"]), stroke_width=0,
                       fill_color=LAB, fill_opacity=0.12)
        side = VGroup(
            label(r"half a century later, \ for the whole economy:", font_size=24),
            label(rf"1950--1999: \ between {100 * s['min_1950_1999']:.0f}\% and {100 * s['max_1950_1999']:.0f}\%, "
                  rf"\\ on average {100 * s['mean_1950_1999']:.1f}\%", font_size=24, color=LAB),
            label(rf"since 2000: \ down, \ to {100 * s['last']:.1f}\% in {s['last_year']}", font_size=24,
                  color=CAP),
            label(r"a stable share was a stylized fact; \\ now it is a puzzle", font_size=23, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.4)
        tag = data_tag(r"Penn World Table, via FRED (LABSHPUSA156NRUG)", corner=DR, font_size=13)
        with self.voiceover(
            "For decades after Douglas the shares stayed remarkably steady. <bookmark mark='a'/> Here is labour's "
            "share of the whole American economy's income, from the Penn World Table. From 1950 to the end of the "
            "century it stayed between sixty and sixty-five percent, at sixty-two and a half on average. "
            "<bookmark mark='b'/> Since 2000 it has fallen, to under fifty-seven percent in 2023. "
            "<bookmark mark='c'/> A constant share was one of the stylized facts that shaped economic theory. Its "
            "decline is one of the live puzzles of the field, and this part's dials come back to it."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(band), FadeIn(side[1]), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def coase(self):
        hc = history_card(1937, r"Ronald Coase, \ twenty-six, \ London", r"``The Nature of the Firm'', \ "
                          r"\emph{Economica}: \ if the price system coordinates so well, \ why is so much of the "
                          r"economy run by command?", color=FIRM, width=10.4, font_size=25).move_to(UP * 1.6)
        q = quote_card(r"islands of conscious power in this ocean of unconscious co-operation like lumps of butter "
                       r"coagulating in a pail of buttermilk", r"D.\ H.\ Robertson, as quoted by Coase (1937), "
                       r"p.\ 388", width=10.4, font_size=24, color=FIRM).next_to(hc, DOWN, buff=0.45)
        tag = published_tag(r"Coase, Economica 4(16) (1937)", corner=DR, font_size=14)
        with self.voiceover(
            "Douglas's function treats a firm as a black box: inputs in, output out. Ten years later a twenty-six-"
            "year-old lecturer in London asked what the box is. <bookmark mark='a'/> In The Nature of the Firm, "
            "Ronald Coase pointed out that inside a firm nothing is bought or sold: a manager tells a worker to "
            "move from one department to another, and the worker moves. <bookmark mark='b'/> He quoted Dennis "
            "Robertson's image of the economy: islands of conscious power in an ocean of unconscious co-operation, "
            "like lumps of butter coagulating in a pail of buttermilk. If markets are so good at coordinating, why "
            "the islands?"
        ) as vo:
            self.play(FadeIn(tag), FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Indicate(hc, color=FIRM, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(q, shift=UP * 0.2))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 38, E.ACCENT).to_edge(UP, buff=0.7)
        rows = VGroup(
            label(r"what can a firm make, \ and at what cost?", font_size=30, color=OUT),
            label(r"how much should it make, \ and how many firms will there be?", font_size=30, color=COST),
            label(r"which activities belong inside a firm, \ and which in the market?", font_size=30, color=FIRM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "So this part asks: how does a firm decide what to make and how, and why is there a firm at all? "
            "<bookmark mark='a'/> What can a firm make, and at what cost? <bookmark mark='b'/> How much should it "
            "make, and how many firms will an industry hold? <bookmark mark='c'/> And which activities belong "
            "inside a firm, and which should be left to the market?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        logo = slipway(1.8)
        t = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 8 \ $\cdot$ \ The Firm", font_size=34, color=E.ACCENT)
        g = VGroup(logo, t, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part eight: the firm."):
            self.play(FadeIn(logo[0]), Create(logo[1]), run_time=1.2)
            self.play(Write(t), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act II \ $\cdot$ \ Choosing", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"technology: \ isoquants, \ marginal products, \ substitution, \ returns to scale",
            r"Cobb and Douglas's regression, \ refitted, \ and how fragile it is",
            r"costs from the technology: \ the cost function, \ short and long run",
            r"run a boatyard yourself; \ supply, \ entry, \ and whether firms maximize at all",
            r"Coase, \ Williamson, \ and Grossman--Hart--Moore: \ where the firm ends",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "This part ends Act Two, on choosing, with the firm's choices. <bookmark mark='a'/> We'll describe "
            "technology: isoquants, marginal products, substitution and returns to scale. <bookmark mark='b'/> "
            "We'll refit Cobb and Douglas's regression on their own data, and see how fragile it is. "
            "<bookmark mark='c'/> We'll derive costs from the technology, in the short run and the long. "
            "<bookmark mark='d'/> You'll run a boatyard yourself; then supply, entry, and the old question of whether "
            "firms maximize anything. <bookmark mark='e'/> And then Coase, Williamson, and Grossman, Hart and Moore, "
            "on where the firm ends and the market begins."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mark, r in zip("bcde", obj.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
