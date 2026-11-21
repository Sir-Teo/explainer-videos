from __future__ import annotations

from videos.economics.econ63.common import *  # noqa: F403


def star_icon(n=8, r=0.75, color=LINK):
    hub = Dot(ORIGIN, radius=0.09, color=SEED)
    leaves = VGroup(*[Dot(r * np.array([np.cos(2 * PI * k / n), np.sin(2 * PI * k / n), 0]), radius=0.06,
                          color=color) for k in range(n)])
    lines = VGroup(*[Arrow(ORIGIN, d.get_center(), buff=0.1, stroke_width=2, tip_length=0.1, color=color)
                     for d in leaves])
    return VGroup(lines, hub, leaves)


def ring_icon(n=8, r=0.75, color=LINK):
    pts = [r * np.array([np.cos(2 * PI * k / n), np.sin(2 * PI * k / n), 0]) for k in range(n)]
    dots = VGroup(*[Dot(p, radius=0.06, color=color) for p in pts])
    lines = VGroup(*[Arrow(pts[k], pts[(k + 1) % n], buff=0.1, stroke_width=2, tip_length=0.1, color=color)
                     for k in range(n)])
    return VGroup(lines, dots)


class Granular(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Why shocks do not wash out", r"Millions of firms each have their own good and bad years: \ "
             r"why don't they cancel out?", "Chapter four. Why shocks do not wash out.",
             lit={2011: r"Gabaix", 2012: r"Acemoglu et al."}, scale=("firm", "nation"), horizon=("a year",))
        self.law()
        self.gabaix()
        self.shapes()

    def law(self):
        G = load("granular")
        rows = G["rows"]
        ns = [r["n"] for r in rows]
        lx = np.log10(ns)
        ax = plane([0.8, 4.2], [np.log10(0.0008), np.log10(0.08)], center=LEFT * 2.6 + DOWN * 0.35, x_length=6.4,
                   y_length=4.8, xticks=[1, 2, 3, 4], yticks=[np.log10(v) for v in (0.001, 0.01, 0.05)],
                   xlabel=r"number of firms \ (log scale)", ylabel=r"GDP growth's standard deviation \ (log scale)",
                   xfmt=lambda v: f"{10 ** v:,.0f}".replace(",", "{,}"),
                   yfmt=lambda v: rf"{100 * 10 ** v:.1f}\%", font_size=14)
        eq_ = path(ax, lx, np.log10([r["equal"] for r in rows]), GREY_B, 3.0)
        zf = path(ax, lx, np.log10([r["zipf"] for r in rows]), SHOCK, 3.4)
        last = rows[-1]
        side = VGroup(
            label(r"each firm: \ its own shock, \ standard deviation 12\%", font_size=19, color=WHITE),
            label(rf"grey: \ equal firms; \ 10,000 of them: \ {100 * last['equal']:.2f}\%".replace(",", "{,}"),
                  font_size=19, color=GREY_B),
            label(rf"red: \ sizes like real firms (Zipf); \ {100 * last['zipf']:.1f}\%", font_size=19, color=SHOCK),
            label(rf"the ten largest make {100 * last['top10_share']:.0f}\% of all sales", font_size=19, color=GDP),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        eq = label(r"$\sigma_{GDP} = \sigma \sqrt{\textstyle\sum_i s_i^2}$", font_size=30).next_to(side, UP,
                                                                                                 buff=0.5)
        tag = island_tag(r"computed: \ agora.network.granular", corner=DL, font_size=12)
        with self.voiceover(
            "Robert Lucas made the argument in 1977: an economy has millions of firms, and each one's good and bad "
            "years are its own, so they should cancel out. <bookmark mark='a'/> If every firm's sales swing by "
            "twelve percent a year, independently, GDP's growth is the average, and its standard deviation is "
            "twelve percent times the square root of the sum of squared sales shares. <bookmark mark='b'/> With "
            "equal firms that falls like one over the square root of their number: ten thousand firms, and the "
            f"aggregate swing is {100 * last['equal']:.2f} percent, nothing. <bookmark mark='c'/> But firms are "
            "not equal. Their sizes follow something close to Zipf's law, the largest twice the second, three "
            "times the third. Then the square root barely falls: with ten thousand firms the aggregate still "
            f"swings by {100 * last['zipf']:.1f} percent, as much as a real business cycle. <bookmark mark='d'/> "
            f"The ten largest firms make {100 * last['top10_share']:.0f} percent of all sales, and their shocks "
            "are the economy's."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(eq))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(eq_), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(zf), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def gabaix(self):
        G = load("granular")
        zs, es = np.array(G["sim_zipf"]), np.array(G["sim_equal"])
        yrs = np.arange(1, len(zs) + 1)
        ax = plane([0, 41], [-6, 6], center=UP * 1.2, x_length=11.0, y_length=3.0, xticks=[10, 20, 30, 40],
                   yticks=[-4, 0, 4], xlabel=r"year", ylabel=r"GDP growth from firms' own shocks, \ \%",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0",
                   font_size=14)
        zl = path(ax, yrs, 100 * zs, SHOCK, 3.0, smooth=False)
        el = path(ax, yrs, 100 * es, GREY_B, 3.0, smooth=False)
        key = legend_rows([(SHOCK, r"1,000 Zipf-sized firms".replace(",", "{,}")),
                           (GREY_B, r"1,000 equal firms".replace(",", "{,}"))], font_size=16)
        key.arrange(RIGHT, buff=0.5).next_to(ax, UP, buff=0.15).align_to(ax, RIGHT)
        hc = history_card(2011, r"Xavier Gabaix: \ the granular hypothesis", r"the year-to-year surprises of the 100 "
                          r"largest American firms account for about a third of the swings in output and in "
                          r"productivity", color=GDP, width=11.0, font_size=21).next_to(ax, DOWN, buff=0.6)
        tag = published_tag(r"Gabaix, \ Econometrica 79(3) (2011); \ Lucas (1977)", corner=DL, font_size=12)
        with self.voiceover(
            "Here are forty simulated years of the Island's GDP growth, from nothing but firms' own shocks: no "
            "recession, no central bank, no oil price. <bookmark mark='a'/> With equal firms, the line is flat. "
            "<bookmark mark='b'/> With firms sized like real ones, it swings by a couple of percent, up and down, "
            "like a business cycle. <bookmark mark='c'/> Xavier Gabaix called this the granular hypothesis: the "
            "economy is made of grains, some of them large. He measured the surprises of the hundred largest "
            "American firms, their growth above or below their peers', and found that they account for about a "
            "third of the swings in output."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(el), FadeIn(key[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(zl), FadeIn(key[0]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(hc, shift=UP * 0.1))
        self.clear_scene()

    def shapes(self):
        G = load("granular")
        S = G["shapes"]
        ks = np.log10(S["sectors"])
        ax = plane([0.6, 2.8], [0, 0.12], center=RIGHT * 2.4 + DOWN * 0.5, x_length=6.0, y_length=4.4,
                   xticks=[1, 2], yticks=[0, 0.04, 0.08, 0.12], xlabel=r"number of sectors \ (log scale)",
                   ylabel=r"GDP growth's standard deviation", xfmt=lambda v: f"{10 ** v:.0f}",
                   yfmt=lambda v: rf"{100 * v:.0f}\%", font_size=14)
        st = path(ax, ks, S["star"], SEED, 3.4)
        rg = path(ax, ks, S["ring"], LINK, 3.4)
        si = star_icon().move_to(LEFT * 4.6 + UP * 1.4)
        ri = ring_icon().move_to(LEFT * 4.6 + DOWN * 1.4)
        sl = label(r"a star: \ one sector supplies all", font_size=18, color=SEED).next_to(si, DOWN, buff=0.2)
        rl = label(r"a ring: \ each supplies the next", font_size=18, color=LINK).next_to(ri, DOWN, buff=0.2)
        concl = label(r"the same shocks, \ the same sizes of sector: \ the shape of the network decides",
                      font_size=21, color=E.ACCENT).to_edge(UP, buff=0.4)
        tag = published_tag(r"Acemoglu, \ Carvalho, \ Ozdaglar and Tahbaz-Salehi, \ Econometrica 80(5) (2012)",
                            corner=DL, font_size=12)
        with self.voiceover(
            "Big firms are one reason the shocks do not cancel. The shape of the network is another. Daron "
            "Acemoglu, Vasco Carvalho, Asuman Ozdaglar and Alireza Tahbaz-Salehi compared economies in which every "
            "sector sells the same amount to households but buys differently. <bookmark mark='a'/> In a ring, each "
            "sector supplies the next. <bookmark mark='b'/> Add sectors, and the volatility of GDP falls away like "
            "one over the square root of their number, as Lucas expected. <bookmark mark='c'/> In a star, one "
            "sector supplies all the others. <bookmark mark='d'/> Its sales grow with the economy, so its shocks "
            "never become small, and the volatility of GDP stops falling. <bookmark mark='e'/> Same shocks, same "
            "number of sectors: the shape of the network decides whether the law of large numbers works."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(ri), FadeIn(rl))
            vo.wait_until("b")
            self.play(Create(rg), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(si), FadeIn(sl))
            vo.wait_until("d")
            self.play(Create(st), run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(concl))
        self.clear_scene()
