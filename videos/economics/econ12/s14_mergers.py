from __future__ import annotations

from videos.economics.econ12.common import *  # noqa: F403

GAIN = "#7BD88F"
LOSS = "#F2788F"
SAVE = "#7EC8F5"


class Mergers(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Mergers", r"When two rivals become one, \ who gains, \ and should the law let them?",
             "Chapter twelve. Mergers.", lit={1968: r"Williamson's trade-off", 1983: r"the merger paradox"},
             scale=("firm", "market", "nation"), horizon=("a year", "a decade"))
        self.paradox()
        self.price()
        self.williamson()

    def paradox(self):
        m = load("merger")
        ns = np.array(m["ns"])
        g = np.array(m["gains"])
        ax = plane([1.5, 10.5], [-200, 260], center=LEFT * 3.0 + DOWN * 0.3, x_length=6.0, y_length=4.6,
                   xticks=[2, 3, 4, 6, 8, 10], yticks=[-150, -100, 0, 100, 200], xlabel=r"yards before the merger",
                   ylabel=r"gain to the two that merge, \ \$", font_size=16, xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}")
        a = ax.ax
        zero = DashedLine(a.c2p(1.5, 0), a.c2p(10.5, 0), color=GREY_B, stroke_width=1.5)
        bars = VGroup(*[Rectangle(width=0.32, height=abs(a.c2p(0, v)[1] - a.c2p(0, 0)[1]), stroke_width=0,
                                  fill_color=GAIN if v > 0 else LOSS, fill_opacity=0.85).move_to(
            a.c2p(n, 0), aligned_edge=DOWN if v > 0 else UP) for n, v in zip(ns, g)])
        side = VGroup(
            label(rf"three yards; \ two merge: \\ before, \ \${m['before_profit']:.2f} each; \\ after, \ the merged "
                  rf"yard earns \${m['after_profit']:.0f}", font_size=21),
            label(rf"the two together lose \${-m['gain']:.1f}: \\ the yard left out gains the most", font_size=22,
                  color=LOSS),
            label(r"Salant, \ Switzer and Reynolds (1983): \\ with Cournot rivals, \ the merged firm cuts output \\ "
                  r"and the outsiders expand", font_size=21, color=GREY_A),
            label(rf"of five yards, \ a merger must take in four \\ just to break even", font_size=21, color=EQ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Salant, Switzer and Reynolds, QJE 98(2) (1983); \ the numbers: \ Agora", corner=DR,
                            font_size=13)
        with self.voiceover(
            "Start with a puzzle. <bookmark mark='a'/> Three Cournot yards each earn five hundred and six dollars. "
            "Two of them merge into one. With two yards left, each earns nine hundred. <bookmark mark='b'/> So the "
            "two that merged, who together earned a thousand and twelve fifty, now earn nine hundred: they have lost "
            "a hundred and twelve dollars fifty. The yard left out has gained the most. "
            "<bookmark mark='c'/> Stephen Salant, Sheldon Switzer and Robert Reynolds pointed this out in 1983. The "
            "merged firm cuts its output to raise the price, and its Cournot rivals expand to take advantage of it. "
            "<bookmark mark='d'/> Agora's bars show the merger loses money whenever more than two yards were there "
            "to begin with. Of five yards, a merger must take in four just to break even."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(zero), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars[1]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(bars[0]), FadeIn(bars[2:]), FadeIn(side[3]))
        self.clear_scene()

    def price(self):
        m = load("merger")
        rows = VGroup(
            label(r"real mergers happen: \ so firms must expect something the paradox leaves out", font_size=24),
            label(r"savings: \ the merged firm may make boats more cheaply", font_size=24, color=SAVE),
            label(rf"Farrell and Shapiro (1990): \ for the price not to rise, \ the merged yard's cost must fall by "
                  rf"\${m['saving_needed']:.1f}", font_size=23, color=GREY_A),
            label(rf"but its cost is only \${m['cost']:.0f}: \ even at zero, \ the price rises from "
                  rf"\${m['before_P']:.2f} to \${m['price_if_free']:.2f}", font_size=24, color=LOSS),
            label(r"with differentiated products and prices, \ mergers are profitable without savings, \ and raise "
                  r"prices too", font_size=23, color=LEADER),
            label(r"so a merger of close rivals must show savings large enough, \ and passed on to buyers",
                  font_size=24, color=E.ACCENT),
        ).arrange(DOWN, buff=0.3).move_to(UP * 0.1)
        tag = published_tag(r"Farrell and Shapiro, AER 80(1) (1990); \ Deneckere and Davidson, RAND J. 16(4) (1985)",
                            corner=DR, font_size=13)
        with self.voiceover(
            "Yet firms merge all the time, so they must expect something the paradox leaves out. "
            "<bookmark mark='a'/> One possibility is savings: the merged firm may make things more cheaply. "
            "<bookmark mark='b'/> Joseph Farrell and Carl Shapiro asked in 1990 how large the savings must be for "
            "buyers not to lose. On the Island, the price stays put only if the merged yard's cost per boat falls by "
            "twenty-two dollars fifty. <bookmark mark='c'/> But each boat costs only ten. Even if the merged yard "
            "could build boats for nothing, the price would still rise, from thirty-two fifty to thirty-six "
            "sixty-seven. <bookmark mark='d'/> With differentiated products and price competition, the paradox "
            "disappears: Raymond Deneckere and Carl Davidson showed in 1985 that such mergers are profitable even "
            "without savings, and raise prices too. <bookmark mark='e'/> So a merger between close rivals has to "
            "show savings large enough, and passed on to buyers, to offset the loss of competition between them."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def williamson(self):
        m = load("merger")
        ax = plane([0, 100], [0, 100], center=LEFT * 3.1 + DOWN * 0.3, x_length=5.4, y_length=5.0,
                   xticks=[], yticks=[], xlabel=r"quantity", ylabel=r"price", font_size=16)
        a = ax.ax
        dem = seg(ax, 5, 95, 95, 5, color=WHITE, width=3)
        p0, p1, c1 = 40.0, 50.0, 34.0
        q0, q1 = 100 - p0, 100 - p1
        tri = Polygon(a.c2p(q1, p1), a.c2p(q0, p0), a.c2p(q1, p0), stroke_width=0, fill_color=LOSS, fill_opacity=0.7)
        rect = Polygon(a.c2p(0, c1), a.c2p(q1, c1), a.c2p(q1, p0), a.c2p(0, p0), stroke_width=0, fill_color=SAVE,
                       fill_opacity=0.6)
        l0 = seg(ax, 0, p0, q0, p0, color=GREY_A, width=2, dashed=True)
        l1 = seg(ax, 0, p1, q1, p1, color=LOSS, width=2, dashed=True)
        lc = seg(ax, 0, c1, 100, c1, color=SAVE, width=2, dashed=True)
        labs = VGroup(label(r"old price \ $=$ \ old cost", font_size=14, color=GREY_A).next_to(a.c2p(0, p0), RIGHT,
                                                                                            buff=0.05).shift(
            UP * 0.15 + RIGHT * 3.2),
            label(r"new price", font_size=14, color=LOSS).next_to(a.c2p(0, p1), LEFT, buff=0.1),
            label(r"new cost", font_size=14, color=SAVE).next_to(a.c2p(0, c1), LEFT, buff=0.1))
        side = VGroup(
            label(r"Oliver Williamson (1968): \\ a merger raises the price, \ and lowers the cost", font_size=21),
            label(r"the loss: \ a small triangle \\ of trades no longer made", font_size=21, color=LOSS),
            label(r"the gain: \ a rectangle of cost saved \\ on every boat still made", font_size=21, color=SAVE),
            label(rf"with demand elasticity {m['eps']:.0f}, \ a {100 * m['dp']:.0f}\% price rise \\ costs a triangle "
                  rf"of about {100 * m['breakeven_dc']:.0f}\% of sales", font_size=21, color=EQ),
            label(r"in total surplus small savings win; \\ but the rectangle goes to the firm: \\ buyers still pay "
                  r"more", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Williamson, AER 58(1) (1968); \ the arithmetic: \ Agora", corner=DR, font_size=13)
        with self.voiceover(
            "Who should count? <bookmark mark='a'/> In 1968 Oliver Williamson drew a merger that raises the price "
            "but lowers the cost. <bookmark mark='b'/> The loss to society is a small triangle: the trades no longer "
            "made at the higher price. <bookmark mark='c'/> The gain is a rectangle: the cost saved on every unit "
            "still made. <bookmark mark='d'/> Because the triangle's area grows with the square of the price rise, "
            "it is small. With a demand elasticity of two, a ten percent price rise costs a triangle of only about "
            "one percent of sales, so a cost saving of one percent would offset it. <bookmark mark='e'/> In total "
            "surplus, then, modest savings win. But the rectangle goes to the merged firm, and buyers still pay "
            "more. American and European agencies ask whether buyers are harmed, which is why the savings they "
            "accept must be passed on in prices."
        ) as vo:
            self.play(FadeIn(ax), Create(dem), Create(l0), FadeIn(labs[0]), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(l1), FadeIn(labs[1]), FadeIn(tri), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(lc), FadeIn(labs[2]), FadeIn(rect), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
