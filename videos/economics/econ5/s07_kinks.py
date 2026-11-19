from __future__ import annotations

from videos.economics.econ5.common import *  # noqa: F403

ELAST_COLOR = {"0": GREY_B, "0.25": IC, "1": E.ACCENT}


class Kinks(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Corners and kinks", r"What happens when the best bundle is not a tangency?",
             "Chapter six. Corners and kinks.", lit=("households", "government"))
        self.corner()
        self.bulk()
        self.credit()

    def corner(self):
        ax = goods_axes(center=LEFT * 2.9 + DOWN * 0.2, top=13)
        a = ax.ax
        A, B = 10.0, 6.0      # fish $6, coconuts $10, $60
        ln = budget_line(ax, A, B)
        sub = cs.Preference("substitutes", a=1.0, b=1.2)
        xs = np.linspace(0, 13, 100)
        lines = VGroup(*[curve(ax, xs, sub.indifference(lv, xs), color=IC, width=2.5, top=13)
                         for lv in (4.0, 7.2, 10.0)])
        pick = Dot(a.c2p(A, 0), radius=0.12, color=WHO["chidi"])
        rows = VGroup(
            label(r"Chidi: \ a coconut is worth 1.2 fish to him, \ always", font_size=24, color=WHO["chidi"]),
            label(r"fish \$6, \ coconuts \$10: \\ a coconut costs 1.67 fish at the market", font_size=24),
            label(r"so he buys only fish: \ a corner", font_size=26, color=E.ACCENT),
            label(r"at a corner the rates need not be equal: \\ $\text{MRS} \ne p_x/p_y$, \ and he'd trade further "
                  r"\\ if he could buy negative coconuts", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.45)
        with self.voiceover(
            "The tangency rule has exceptions, and they matter. <bookmark mark='a'/> Chidi treats coconuts and fish "
            "as perfect substitutes: to him a coconut is always worth 1.2 fish. His indifference curves are "
            "straight lines. <bookmark mark='b'/> At the market a coconut costs 1.67 fish. "
            "<bookmark mark='c'/> So he spends everything on fish, and buys no coconuts at all: a corner solution. "
            "<bookmark mark='d'/> At a corner, his rate of trade doesn't equal the market's. He'd like to trade "
            "even further, but he can't buy fewer than zero coconuts. Most people buy none of most goods in the "
            "shop, so corners are the rule, not the exception."
        ) as vo:
            self.play(FadeIn(ax), Create(ln), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(pick, scale=1.6), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def bulk(self):
        b = load("bulk")
        ax = goods_axes(center=LEFT * 4.0 + DOWN * 0.3, top=16, ticks=(0, 5, 10, 15), x_length=4.3, y_length=4.3)
        a = ax.ax
        fronts, picks = VGroup(), VGroup()
        for key, col in (("16", GREY_B), ("28", BUDGET)):
            fr = np.array(b["shown"][key]["frontier"])
            pts = [a.c2p(x, y) for x, y in fr[::40] if y <= 16]
            fronts.add(VMobject(stroke_color=col, stroke_width=3).set_points_as_corners(pts))
            picks.add(Dot(a.c2p(*b["shown"][key]["choice"]), radius=0.1, color=col))
        kink = DashedLine(a.c2p(0, b["first"]), a.c2p(16, b["first"]), color=GREY_C, stroke_width=1.5)
        kl = label(rf"the {b['first']}th coconut", font_size=17, color=GREY_C).next_to(a.c2p(16, b["first"]), UP,
                                                                                   buff=0.05).shift(LEFT * 0.7)
        from explainer.ai.viz import axes

        ex = axes([8, 40], [0, 18], x_length=4.6, y_length=3.6, xticks=[10, 20, 30, 40], yticks=[0, 6, 12, 18],
                  xlabel=r"Bo's income, \$", ylabel=r"coconuts bought", font_size=17, center=RIGHT * 2.1 + DOWN * 0.6)
        e = ex.ax
        inc = np.array(b["incomes"])
        best = np.array(b["best"])
        j = int(np.argmax(np.diff(best[:, 1])))
        seg1 = VMobject(stroke_color=COCO, stroke_width=4).set_points_as_corners(
            [e.c2p(m, c) for m, c in zip(inc[:j + 1], best[:j + 1, 1])])
        seg2 = VMobject(stroke_color=COCO, stroke_width=4).set_points_as_corners(
            [e.c2p(m, c) for m, c in zip(inc[j + 1:], best[j + 1:, 1])])
        gap = DashedLine(e.c2p(inc[j], best[j, 1]), e.c2p(inc[j + 1], best[j + 1, 1]), color=VIOL, stroke_width=2)
        head = VGroup(label(rf"coconuts: \${b['price_first']:.0f} each for the first {b['first']}, \ then "
                            rf"\${b['price_after']:.0f}", font_size=23, color=COCO),
                      label(rf"fish \${b['fish']:.0f}; \ Bo spends half on each", font_size=20, color=GREY_A)).arrange(
            DOWN, buff=0.12).to_edge(UP, buff=0.35)
        note_ = label(rf"at \${b['tie']:.2f} of income \ he jumps from {b['jump'][0][1]:.1f} to {b['jump'][1][1]:.1f} "
                      r"coconuts: \ no income buys the ones between", font_size=21, color=VIOL).to_edge(DOWN,
                                                                                                    buff=0.4)
        tag = island_tag(r"simulated: the coconut seller's bulk price", corner=DR, font_size=13)
        with self.voiceover(
            "Kinks come from the seller's side too. <bookmark mark='a'/> The coconut seller offers a bulk price: two "
            "dollars each for the first six, one dollar each after that. Bo's budget line now bends outward at the "
            "sixth coconut. <bookmark mark='b'/> With sixteen dollars, Bo stays below the bend and buys four. "
            "<bookmark mark='c'/> With twenty-eight, the cheap coconuts beyond the bend win, and he buys eleven. "
            "<bookmark mark='d'/> Follow him as his income rises. His coconut purchases grow smoothly, until, at "
            "about twenty dollars and fifty cents, they jump, from about five to more than seven. No income at all "
            "would make him buy six. A budget that bends outward makes choices jump: whole quantities are never "
            "chosen. Volume discounts, phone plans and two-for-one offers all have this shape."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(head), FadeIn(tag), Create(kink), FadeIn(kl))
            vo.wait_until("a")
            self.play(Create(fronts[0]))
            vo.wait_until("b")
            self.play(FadeIn(picks[0], scale=1.5))
            vo.wait_until("c")
            self.play(Create(fronts[1]), FadeIn(picks[1], scale=1.5))
            vo.wait_until("d")
            self.play(FadeIn(ex), Create(seg1), run_time=1.5)
            self.play(Create(gap), Create(seg2), FadeIn(note_), run_time=1.5)
        self.clear_scene()

    def credit(self):
        cr = load("credit")
        from explainer.ai.viz import axes

        sch = axes([0, 36000], [0, 3200], x_length=5.0, y_length=2.4, xticks=[0, 8580, 15740, 33995],
                   yticks=[0, 1500, 3000], xfmt=lambda v: f"{v / 1000:.1f}k" if v else "0",
                   yfmt=lambda v: f"{v:,.0f}".replace(",", "{,}"), xlabel=r"earnings, 2008 \$",
                   ylabel=r"credit, \$", font_size=15, center=LEFT * 3.6 + UP * 1.4)
        s = sch.ax
        zz, cc = np.array(cr["schedule"]["z"]), np.array(cr["schedule"]["credit"])
        sline = VMobject(stroke_color=BUDGET, stroke_width=3.5).set_points_as_corners([s.c2p(z, c) for z, c in zip(zz, cc)])
        sl = VGroup(label(r"$+34$\%", font_size=17, color=BUDGET).move_to(s.c2p(3500, 2000)),
                    label(r"$-16$\%", font_size=17, color=BUDGET).move_to(s.c2p(26000, 2300)))
        edges = np.array(cr["edges"])
        hmax = max(max(v["hist"]) for v in cr["by_e"].values())
        hist_ax = axes([0, 20000], [0, hmax * 1.1], x_length=5.6, y_length=2.6, xticks=[0, 8580, 15740],
                       yticks=None, xfmt=lambda v: f"{v / 1000:.1f}k" if v else "0", xlabel=r"earnings chosen",
                       font_size=15, center=LEFT * 3.4 + DOWN * 2.0)
        h = hist_ax.ax
        bars = {}
        for key, v in cr["by_e"].items():
            g = VGroup()
            for e0, e1, n_ in zip(edges[:-1], edges[1:], v["hist"]):
                if n_ == 0:
                    continue
                r = Rectangle(width=h.c2p(e1, 0)[0] - h.c2p(e0, 0)[0], height=h.c2p(0, n_)[1] - h.c2p(0, 0)[1],
                              stroke_width=0.5, stroke_color=BACKGROUND, fill_color=ELAST_COLOR[key], fill_opacity=0.85)
                r.move_to(h.c2p((e0 + e1) / 2, 0), aligned_edge=DOWN)
                g.add(r)
            bars[key] = g
        kline = DashedLine(h.c2p(cr["kink"], 0), h.c2p(cr["kink"], hmax * 1.05), color=E.ACCENT, stroke_width=2)
        rows = VGroup(
            label(r"the earned income tax credit, \ one child, \ 2008", font_size=24, color=BUDGET),
            label(r"below \$8{,}580 \ each dollar earned brings 34 cents more; \\ then nothing more", font_size=21),
            label(rf"simulated: \ 4{{,}}000 earners; \ share at the kink: \\ elasticity 0: \ "
                  rf"{100 * cr['by_e']['0']['at_kink']:.1f}\%; \ 0.25: \ {100 * cr['by_e']['0.25']['at_kink']:.1f}\%;"
                  rf" \ 1: \ {100 * cr['by_e']['1']['at_kink']:.1f}\%", font_size=21, color=IC),
            label(r"Saez (2010), \ IRS tax returns: \ bunching at the first kink, \\ but only among the "
                  r"self-employed \ (elasticity near 1); \\ wage earners: \ none", font_size=21, color=E.ACCENT),
            label(r"the model also piles people at the second kink; \\ Saez found no pile there: \ the first kink is "
                  r"\\ the lowest income with the whole credit", font_size=21, color=GREY_A),
            label(r"a kink reveals how much people respond, \\ and what they can adjust: \ often the report, \\ not "
                  r"the work", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Saez, AEJ: Policy 2(3) (2010), table 1; simulated earners", corner=DR, font_size=12)
        with self.voiceover(
            "Governments make kinks deliberately. <bookmark mark='a'/> The American earned income tax credit pays "
            "low earners a subsidy on what they earn. In 2008, for a parent of one child, each dollar earned up to "
            "eight thousand, five hundred and eighty brought thirty-four cents of credit. Then the credit stopped "
            "growing, and further on it was withdrawn at sixteen cents a dollar. <bookmark mark='b'/> At the first "
            "kink, the reward for earning one more dollar drops from a dollar thirty-four to one dollar. Anyone "
            "with some freedom over their earnings, and a taste for leisure, will stop there. "
            "<bookmark mark='c'/> Simulate four thousand earners. If no one can adjust, there's no pile at the kink. "
            "With an elasticity of a quarter, a few percent gather there; with an elasticity of one, about one in "
            "seven. <bookmark mark='d'/> In 2010 Emmanuel Saez looked at decades of tax returns, and found the pile. "
            "But it was made almost entirely of the self-employed, who report their own income, with an implied "
            "elasticity near one. Wage earners, whose employers report for them, showed none. "
            "<bookmark mark='e'/> The size of the pile at a kink measures how much people respond. And who piles up "
            "tells you what they can adjust: often the paperwork, not the work. One more clue points the same way. "
            "Our simple model also piles people up at the second kink, where the credit starts to be withdrawn. Saez "
            "found no pile there. The first kink is special: it's the lowest income that collects the whole credit, "
            "exactly where someone reporting their own income would aim."
        ) as vo:
            self.play(FadeIn(sch), FadeIn(rows[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(sline), FadeIn(sl), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(hist_ax), Create(kline))
            vo.wait_until("c")
            self.play(FadeIn(bars["0"]))
            self.play(ReplacementTransform(bars["0"], bars["0.25"]))
            self.play(ReplacementTransform(bars["0.25"], bars["1"]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[5]))
            self.play(FadeIn(rows[4]))
        self.clear_scene()
