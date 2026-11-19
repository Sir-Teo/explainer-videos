from __future__ import annotations

from scipy.stats import norm

from videos.economics.econ8.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 14, r"In practice: \ cost models and capacity", r"How do engineers and planners put these ideas "
             r"to work?", "Chapter fourteen. In practice: cost models and capacity.", lit={1936: r"Wright's learning "
                                                                                                r"curve"},
             scale=("firm",), horizon=("a year", "a decade"))
        self.scaling()
        self.learning()
        self.capacity()

    def scaling(self):
        rows = VGroup(
            label(r"estimating a plant you haven't built:", font_size=28),
            MathTex(r"C_{\text{new}} = C_{\text{old}}\left(\frac{S_{\text{new}}}{S_{\text{old}}}\right)^{0.6}",
                    font_size=46, color=OUT),
            label(rf"twice the capacity: \ $2^{{0.6}}$ = {2 ** 0.6:.2f}, \ about half as much again", font_size=27),
            label(r"the exponent varies by equipment, \ roughly 0.4 to 0.8; \ engineers keep tables of them",
                  font_size=24, color=GREY_A),
            label(r"a cost function with increasing returns, \ read off a spreadsheet", font_size=25, color=E.ACCENT),
        ).arrange(DOWN, buff=0.4)
        with self.voiceover(
            "Engineers use returns to scale every day. <bookmark mark='a'/> To estimate the cost of a plant that "
            "hasn't been built, they scale the cost of one that has by the ratio of capacities, raised to a power, "
            "usually about six tenths. <bookmark mark='b'/> A plant with twice the capacity then costs two to the "
            "nought point six times as much: one point five two, about half as much again. "
            "<bookmark mark='c'/> The exponent varies with the equipment, and engineers keep tables of them. "
            "<bookmark mark='d'/> It's a cost function with increasing returns, used for real decisions about what to "
            "build."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def learning(self):
        n = np.logspace(0, np.log10(256), 120)
        ax = plane([0, 8], [0, 1.05], center=LEFT * 2.8 + DOWN * 0.3, x_length=6.6, y_length=5.0,
                   xticks=[0, 2, 4, 6, 8], yticks=[0, 0.5, 1.0], xlabel=r"cumulative aircraft built \ (log$_2$ scale)",
                   ylabel=r"labour per aircraft, \ first = 1", font_size=17, xfmt=lambda v: f"{2 ** v:.0f}")
        b = np.log2(0.8)
        curve = path(ax, np.log2(n), n ** b, color=LAB, width=3.5)
        dots = VGroup(*[Dot(ax.ax.c2p(k, 0.8 ** k), radius=0.07, color=OUT) for k in range(0, 9)])
        side = VGroup(
            history_card(1936, r"T.\ P.\ Wright, \ Curtiss-Wright, \ Buffalo", r"``Factors Affecting the "
                         r"Cost of Airplanes'': \ labour per plane falls by a steady fraction \\ each time "
                                 r"cumulative output doubles", color=LAB, width=5.6, font_size=19),
            label(r"drawn here with a 20\% fall per doubling, \\ a common rule of thumb (illustrative)", font_size=21,
                  color=GREY_A),
            label(r"costs depend on \emph{experience}, \ not only on \\ this month's output: \ a reason to produce \\ "
                  r"ahead of demand, \ and to price low early", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = illustrative_tag(r"illustrative: an 80\% learning curve", corner=DR, font_size=14)
        with self.voiceover(
            "A second idea from practice changes the shape of cost itself. <bookmark mark='a'/> In 1936 Theodore "
            "Wright, an aeronautical engineer at Curtiss-Wright in Buffalo, showed that the labour needed per "
            "aeroplane fell by a steady fraction every time the number built doubled. <bookmark mark='b'/> Drawn "
            "here with a fall of a fifth per doubling, a common rule of thumb: the eighth plane takes about half the "
            "labour of the first, the two hundred and fifty-sixth about a sixth. <bookmark mark='c'/> So cost depends "
            "on experience, on everything built so far, and not only on this month's output. That's a reason to build "
            "ahead of demand, and to price low early to get down the curve. It matters for aircraft, ships, solar "
            "panels and batteries, and it comes back when we discuss industrial policy."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(curve), LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.2), FadeIn(side[1]),
                      run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def capacity(self):
        mu, sd = 100.0, 20.0
        ratio = 0.25
        K = mu + sd * norm.ppf(1 - ratio)
        xs = np.linspace(40, 160, 300)
        ax = plane([40, 160], [0, 0.022], center=LEFT * 2.8 + DOWN * 0.3, x_length=6.6, y_length=4.6,
                   xticks=[40, 70, 100, 130, 160], yticks=[], xlabel=r"boats ordered next year", ylabel=r"chance",
                   font_size=17)
        a = ax.ax
        dens = path(ax, xs, norm.pdf(xs, mu, sd), color=LAB, width=3)
        tail = Polygon(*[a.c2p(x, norm.pdf(x, mu, sd)) for x in np.linspace(K, 160, 60)], a.c2p(160, 0), a.c2p(K, 0),
                       stroke_width=0, fill_color=OUT, fill_opacity=0.35)
        kl = DashedLine(a.c2p(K, 0), a.c2p(K, 0.022), color=OUT, stroke_width=2.5)
        side = VGroup(
            label(r"how big a yard to build, \ when orders are uncertain?", font_size=24),
            label(r"orders: \ 100 a year on average, \ s.d.\ 20", font_size=22, color=LAB),
            label(r"a slip's worth of capacity costs \$250 a boat a year; \\ a boat built earns a margin of \$1{,}000",
                  font_size=22),
            label(r"build until the chance of using the last unit \\ equals its cost over its margin:", font_size=22),
            MathTex(r"P(\text{orders} > K) = \frac{c}{m} = 0.25", font_size=34, color=OUT),
            label(rf"capacity {K:.0f}: \ more than the average, \\ because a lost sale costs more than an idle slip",
                  font_size=22, color=E.ACCENT),
            label(r"the newsvendor's rule, \ from operations research", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.35)
        tag = illustrative_tag(r"illustrative numbers", corner=DR, font_size=14)
        with self.voiceover(
            "Last, capacity. Real firms build before they know their orders. <bookmark mark='a'/> Suppose next "
            "year's orders for Crusoe's boats average a hundred, with a standard deviation of twenty. "
            "<bookmark mark='b'/> Each boat's worth of capacity costs two hundred and fifty dollars a year whether "
            "it's used or not, and each boat built earns a margin of a thousand. <bookmark mark='c'/> The marginal "
            "rule again: add capacity until the chance that the last unit is used, times its margin, equals its "
            "cost. So the chance of orders exceeding capacity should be a quarter. <bookmark mark='d'/> That means a "
            "yard for a hundred and thirteen boats, more than the average, because a lost sale costs four times as "
            "much as an idle slip. Planners call this the newsvendor's rule, and it's the same margin that ran "
            "through this whole part, with uncertainty added from Part seven."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(dens), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]), FadeIn(side[4]), Create(kl), FadeIn(tail))
            vo.wait_until("d")
            self.play(FadeIn(side[5]), FadeIn(side[6]))
        self.clear_scene()
