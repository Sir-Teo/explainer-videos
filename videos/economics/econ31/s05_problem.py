from __future__ import annotations

from videos.economics.econ31.common import *  # noqa: F403


class Problem(VoiceoverScene):
    def construct(self):
        card(self, 4, r"The identification problem", r"If a central bank raises rates because it sees a boom coming, "
             r"\ what do rate rises do?", "Chapter four. The identification problem.",
             lit={1992: r"Sims; \ Eichenbaum"}, scale=("nation",), horizon=("a quarter", "four years"))
        self.island()
        self.scatter()
        self.puzzle()

    def island(self):
        I = load("island")
        q = np.array(I["q"][:120])
        ax = plane([0, 120], [-3, 5], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.8, y_length=4.8,
                   xticks=[0, 40, 80, 120], yticks=[-2, 0, 2, 4], xlabel=r"quarters", ylabel=r"percent",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=15)
        zero = seg(ax, 0, 0, 120, 0, GREY_D, 1.2)
        rate = path(ax, q, I["i"][:120], RATE, 3, smooth=False)
        out = path(ax, q, I["y"][:120], OUTPUT, 3, smooth=False)
        side = VGroup(
            label(r"thirty years of the Island", font_size=21, color=E.ACCENT),
            label(r"pink: \ the policy rate", font_size=19, color=RATE),
            label(r"green: \ the output gap", font_size=19, color=OUTPUT),
            label(r"the bank sees news \\ about next quarter's demand and costs, \\ and acts on it", font_size=19,
                  color=CB),
            label(r"and a small part of each move \\ is its own: \ the policy shock", font_size=19, color=PRICE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The central question of this part is how anyone can know what a central bank's decisions do. Here is "
            "why it is hard. <bookmark mark='a'/> On the Island, the central bank sets its rate each quarter, "
            "<bookmark mark='b'/> and output moves. <bookmark mark='c'/> But the bank does not move at random. It "
            "sees news before anyone else, about next quarter's demand and next quarter's costs, and acts on it: it "
            "raises its rate when it sees a boom coming. <bookmark mark='d'/> Only a small part of each move is the "
            "bank's own choice, unrelated to what it sees. That part is the policy shock. On the Island we know "
            "exactly what it is, because we planted it."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag), FadeIn(side[0]), run_time=0.6)
            vo.wait_until("a")
            self.play(Create(rate), FadeIn(side[1]), run_time=2)
            vo.wait_until("b")
            self.play(Create(out), FadeIn(side[2]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def scatter(self):
        I = load("island")
        M = load("mc")
        di, yn = np.array(I["di"]), np.array(I["y_next"])
        ax = plane([-1.5, 1.5], [-3, 3], center=LEFT * 2.2 + DOWN * 0.3, x_length=6.4, y_length=5.0,
                   xticks=[-1, 0, 1], yticks=[-2, 0, 2], xlabel=r"change in the policy rate this quarter, \ points",
                   ylabel=r"output gap next quarter, \ \%", xfmt=lambda v: f"{v:+.0f}" if v else "0",
                   yfmt=lambda v: f"{v:+.0f}" if v else "0", font_size=15)
        pts = VGroup(*[Dot(ax.ax.c2p(x, y), radius=0.035, color=GREY_B) for x, y in zip(di, yn)
                       if -1.5 <= x <= 1.5 and -3 <= y <= 3])
        b = I["naive_y1"]
        a0 = float(np.mean(yn) - b * np.mean(di))
        fit = seg(ax, -1.5, a0 - 1.5 * b, 1.5, a0 + 1.5 * b, GREY_A, 3.5)
        tr = M["truth"]["y"][1]
        true = seg(ax, -1.5, -1.5 * tr, 1.5, 1.5 * tr, TRUTH_C, 3, dashed=True)
        side = VGroup(
            label(r"each dot: \ one quarter", font_size=19, color=GREY_B),
            label(rf"the line: \ a one-point rise \\ goes with output {b:+.2f}\% next quarter", font_size=19,
                  color=GREY_A),
            label(rf"the truth on the Island: \\ {tr:+.2f}\%", font_size=19, color=TRUTH_C),
            label(r"the rate rises \emph{because} \\ the boom is coming", font_size=20, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36).to_edge(RIGHT, buff=0.5)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Now be an economist on the Island who sees only the data. <bookmark mark='a'/> Each dot is a quarter: "
            "the change in the policy rate, and output the quarter after. <bookmark mark='b'/> The fitted line "
            f"slopes up: a one-point rise in the rate goes with output {say_num(b, 2)} percent higher next quarter. "
            "Raising rates, it seems, causes booms. <bookmark mark='c'/> The truth, which we planted, is the "
            f"opposite: a one-point policy shock lowers output by {abs(tr):.2f} percent the next quarter. "
            "<bookmark mark='d'/> The rate rises because the bank saw the boom coming, and the boom arrives "
            "anyway. Correlation here measures the bank's foresight, not the effect of its decisions."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.01), FadeIn(side[0]), run_time=1.8)
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(true), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def puzzle(self):
        U = load("usvar")
        h = np.array(U["h"])
        ax = plane([0, 48], [-1.5, 1.0], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.8, y_length=4.8,
                   xticks=[0, 12, 24, 36, 48], yticks=[-1.5, -1, -0.5, 0, 0.5, 1], xlabel=r"months after a "
                   r"one-point rise in the federal funds rate", ylabel=r"consumer prices, \ \% \ (US, 1965--2007)",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:+.1f}" if v else "0", font_size=15)
        zero = seg(ax, 0, 0, 48, 0, GREY_C, 1.5)
        p = U["plain"]
        c = U["commod"]
        b1 = band(ax, h, p["cpi_lo"], p["cpi_hi"], INFL, 0.15)
        l1 = path(ax, h, p["cpi"], INFL, 3.5)
        l2 = path(ax, h, c["cpi"], PRICE, 3.5)
        b2 = band(ax, h, c["cpi_lo"], c["cpi_hi"], PRICE, 0.12)
        side = VGroup(
            label(r"a recursive VAR: \ output, \ prices, \\ the funds rate ordered last", font_size=18, color=GREY_A),
            label(rf"red: \ prices \emph{{rise}} \\ {p['cpi_24']:+.2f}\% after two years", font_size=18, color=INFL),
            label(r"the price puzzle \\ (Sims; \ named by Eichenbaum, \ 1992)", font_size=18, color=HOLD),
            label(rf"gold: \ add commodity prices: \\ {c['cpi_24']:+.2f}\% at two years, \\ {c['cpi_48']:+.2f}\% at "
                  rf"four", font_size=18, color=PRICE),
            label(r"the Fed knew inflation was coming; \\ the VAR did not", font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Sims, \ \emph{EER} 36(5) (1992); \ Eichenbaum, \ ibid.; \ FRED: \ industrial "
                            r"production, \ CPI, \ PPI, \ the funds rate", corner=DR, font_size=12)
        with self.voiceover(
            "The same trap catches real data. <bookmark mark='a'/> Take American monthly data from 1965 to 2007 and "
            "fit a vector autoregression: each variable on the past of all of them, with the funds rate ordered "
            "last, so that the part of a rate move the recent data cannot explain counts as the shock. "
            "<bookmark mark='b'/> After a tightening, prices rise: by "
            f"{say_num(p['cpi_24'], 2)} percent after two years, in red, with a band from two hundred re-runs of the "
            "data. <bookmark mark='c'/> Christopher Sims found this in 1992, and Martin Eichenbaum named it the "
            "price puzzle. <bookmark mark='d'/> Sims's fix was to add commodity prices, which move early when "
            f"inflation is coming. In gold: {say_num(c['cpi_24'], 2)} percent at two years, and "
            f"{say_num(c['cpi_48'], 2)} at four. <bookmark mark='e'/> The puzzle is the identification problem "
            "again: the Federal Reserve knew inflation was coming and tightened against it; the econometrician, "
            "without that knowledge, blamed the tightening for the inflation."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag), FadeIn(side[0]), run_time=0.6)
            vo.wait_until("b")
            self.play(FadeIn(b1), Create(l1), FadeIn(side[1]), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(b2), Create(l2), FadeIn(side[3]), run_time=1.6)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
