from __future__ import annotations

from videos.economics.econ35.common import *  # noqa: F403

SILK = "#E8A0B4"
WOOL = "#C9A0FF"


class Japan(VoiceoverScene):
    def construct(self):
        card(self, 4, r"A test: \ Japan opens", r"Does a country export what was cheap at home before trade?",
             "Chapter four. A test: Japan opens.", lit={1859: r"the treaty ports", 2004: r"Bernhofen and Brown"},
             scale=("nation",), horizon=("a decade",))
        self.history()
        self.composition()
        self.test()
        self.gains()

    def history(self):
        hc = history_card(1859, r"the treaty ports", r"after two centuries of near-total isolation, \ and six years "
                          r"after Commodore Perry's warships arrived, \ Japan opens its ports to foreign trade \ under "
                          r"treaties that cap its tariffs at low rates", color=E.ACCENT, width=11.0, font_size=24)
        hc.move_to(UP * 0.6)
        rows = VGroup(
            label(r"why it is a test: \ prices from before trade, \ 1851--53, \ are known", font_size=22,
                  color=WHITE),
            label(r"the opening was sudden and nearly complete, \ and not chosen by Japan", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.18).next_to(hc, DOWN, buff=0.5)
        tag = published_tag(r"Bernhofen and Brown, \ \emph{JPE} 112(1) (2004)", corner=DR, font_size=12)
        prob = label(r"the difficulty: \ a country's prices without trade are almost never seen", font_size=24,
                     color=GREY_A).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Comparative advantage is hard to test, because it is about prices a country would have had without "
            "trade, and almost no country is ever seen without trade. Japan is the exception. "
            "<bookmark mark='a'/> From 1639 it allowed almost no foreign trade. In 1853 Commodore Matthew Perry's "
            "American warships arrived, and the treaties that followed opened its ports in July 1859, with tariffs "
            "capped at low rates. <bookmark mark='b'/> Daniel Bernhofen and John Brown saw a "
            "natural experiment: prices from the last years of isolation, 1851 to 1853, are recorded, "
            "<bookmark mark='c'/> and the opening was sudden, nearly complete, and not Japan's choice."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(prob))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def composition(self):
        J = load("japan")
        ex = [(k, v) for k, v in J["exports"] if v >= 2.5][:5]
        im = [(k, v) for k, v in J["imports"] if v >= 9][:6]

        def column(items, color, title, x):
            ax_w = 4.0
            g = VGroup(label(title, font_size=22, color=color))
            for k, v in items:
                bar = Rectangle(width=ax_w * v / 40, height=0.36, fill_color=color, fill_opacity=0.85, stroke_width=0)
                nm = label(tex_safe(k), font_size=17, color=WHITE)
                val = label(f"{v:.0f}\\%", font_size=16, color=color)
                row = VGroup(nm, bar, val)
                nm.next_to(bar, LEFT, buff=0.15)
                val.next_to(bar, RIGHT, buff=0.1)
                g.add(row)
            g[1:].arrange(DOWN, aligned_edge=LEFT, buff=0.18)
            for r_ in g[1:]:
                r_[1].align_to(g[1][1], LEFT)
                r_[0].next_to(r_[1], LEFT, buff=0.15)
                r_[2].next_to(r_[1], RIGHT, buff=0.1)
            g[0].next_to(g[1:], UP, buff=0.3)
            return g.move_to(RIGHT * x + DOWN * 0.1)

        exp = column(ex, SILK, r"exports, \ 1868--75 \ (\% of all)", -3.3)
        imp = column(im, WOOL, r"imports \ (\% of all)", 3.6)
        foot = label(r"after opening, \ the prices of silk and tea rose, \ some almost doubling; \ those of cotton "
                     r"goods, \ sugar and iron fell", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.55)
        tag = published_tag(r"Bernhofen and Brown (2004), \ table 1 and figure 4", corner=DR, font_size=12)
        with self.voiceover(
            "What did Japan trade? <bookmark mark='a'/> It exported silk, silkworm eggs and tea: those three were "
            "four fifths of its exports. <bookmark mark='b'/> It imported woollens, cotton cloth and yarn, sugar and "
            "rice: the products of Lancashire's mills and of tropical plantations. <bookmark mark='c'/> And prices "
            "moved as the theory says they should when a country joins the world market: those of its exports, "
            "silk above all, rose, some almost doubling relative to other prices; those of its imports fell."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(exp[0]), LaggedStart(*[FadeIn(r_) for r_ in exp[1:]], lag_ratio=0.2), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(imp[0]), LaggedStart(*[FadeIn(r_) for r_ in imp[1:]], lag_ratio=0.2), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def test(self):
        J = load("japan")
        ys = J["years"]
        ax = plane([1867.3, 1875.7], [-9, 6], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.8, y_length=4.6,
                   xticks=list(ys), yticks=[-8, -4, 0, 4], ylabel=r"millions of ry\=o, \ at the prices of 1851--53",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:+.0f}" if v else "0", font_size=13)
        zero = seg(ax, 1867.3, 0, 1875.7, 0, GREY_B, 1.5)

        def bars(vals, col, dx):
            g = VGroup()
            for y, v in zip(ys, vals):
                p0, p1 = ax.ax.c2p(y + dx - 0.13, 0), ax.ax.c2p(y + dx + 0.13, v)
                g.add(Rectangle(width=abs(p1[0] - p0[0]), height=abs(p1[1] - p0[1]), fill_color=col,
                                fill_opacity=0.8, stroke_width=0).move_to((p0 + p1) / 2))
            return g

        exb, imb, tot = bars(J["exp_obs"], SILK, -0.28), bars(J["imp_obs"], WOOL, 0.0), bars(J["total"], WHITE,
                                                                                           0.28)
        side = VGroup(
            label(r"pink: \ exports, \\ valued at old prices", font_size=17, color=SILK),
            label(r"purple: \ imports, \\ valued at old prices", font_size=17, color=WOOL),
            label(rf"white: \ the total, \\ negative in {J['negative']} \\ of {len(ys)} years", font_size=18,
                  color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        eq = label(r"$p^{a} \cdot T < 0$", font_size=34, color=E.ACCENT).to_edge(UP, buff=0.35)
        pred = label(r"autarky prices $\times$ net exports: \ the prediction is a total below zero", font_size=19,
                     color=GREY_A).next_to(ax.ax.c2p(1871.5, -9), UP, buff=0.15)
        tag = published_tag(r"Bernhofen and Brown (2004), \ table 2 \ (main components)", corner=DR, font_size=12)
        with self.voiceover(
            "Now the test. The theory makes a sharp prediction: value a country's net exports at the prices it had "
            "before trade, and the total must be negative, since it sells what was cheap at home and buys what was "
            "dear. <bookmark mark='a'/> <bookmark mark='b'/> Here are Japan's exports in each year from 1868 to "
            "1875, valued at the prices of 1851 to 1853, <bookmark mark='c'/> and its imports at the same prices: "
            "at the old prices, its exports are worth less than its imports. <bookmark mark='d'/> The total "
            f"is negative in all {len(ys)} years: in 1875, minus {abs(J['total'][-1]):.1f} million ryo. A two hundred "
            "year old theory, tested against a natural experiment, and it passes."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag), FadeIn(eq))
            self.play(FadeIn(pred, shift=DOWN * 0.1))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in exb], lag_ratio=0.1), FadeIn(side[0]),
                      run_time=1.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, UP) for b in imb], lag_ratio=0.1), FadeIn(side[1]),
                      run_time=1.5)
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowFromEdge(b, UP) for b in tot], lag_ratio=0.1), FadeIn(side[2]),
                      run_time=1.5)
        self.clear_scene()

    def gains(self):
        J = load("japan")
        cards = point_cards([
            (r"Japan, \ 1859", rf"opening raised real income \\ by at most \\ "
                               rf"{J['gain_lo']:.0f} to {J['gain_hi']:.0f}\% "
                               r"of GDP", SILK),
            (r"America, \ 1807--09", rf"Jefferson's embargo, \\ closing trade, \\ cost about {J['embargo']:.0f}\% of "
                                     r"GNP", USA),
            (r"why so little?", r"the gains depend \\ on how much is traded, \\ and how different \\ the prices were",
             WHITE),
        ], width=12.6, cols=3, font_size=21).move_to(DOWN * 0.1)
        head = label(r"how large are the gains?", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(r"Bernhofen and Brown, \ \emph{AER} 95(1) (2005); \ Irwin, \ \emph{RIE} 13(4) (2005)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "How much did Japan gain? <bookmark mark='a'/> In a second paper Bernhofen and Brown put an upper bound "
            f"on the static gain: no more than {J['gain_lo']:.0f} or {J['gain_hi']:.0f} percent of GDP. "
            "<bookmark mark='b'/> The reverse experiment gives a similar number. In December 1807 President "
            "Jefferson banned American ships from foreign trade, an embargo that lasted until March 1809. Douglas "
            f"Irwin estimates its cost at about {J['embargo']:.0f} percent of national income. "
            "<bookmark mark='c'/> Real, but not enormous. The gains from comparative advantage are triangles: they "
            "depend on how much a country trades and how different its prices were. Part thirty-six adds gains that "
            "are not triangles: from scale, variety and the best firms growing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abc", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
