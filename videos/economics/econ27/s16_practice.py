from __future__ import annotations

from videos.economics.econ27.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 14, r"In practice: \ the forecasting desk", r"How do forecasters still use these ideas?",
             "Chapter fourteen. In practice: the forecasting desk.", lit={1962: r"Okun", 1946: r"the NBER's dates"},
             scale=("nation",), horizon=("a quarter", "a year"))
        self.desk()
        self.gap()
        self.okun_fact()
        self.cycles()

    def desk(self):
        rows = VGroup(
            label(r"a forecast is still built from the spending side", font_size=27, color=E.ACCENT),
            label(r"$Y = C + I + G + NX$: \ forecast each part, \ then add", font_size=24, color=SPEND),
            label(r"consumption from income and wealth; \ investment from orders, \ rates and profits", font_size=22,
                  color=GREY_A),
            label(r"the government's budget, \ with its multipliers; \ trade from the world's growth", font_size=22,
                  color=GOV),
            label(r"then compare with potential output: \ the output gap, \ and what it means for jobs and prices",
                  font_size=22, color=OUTPUT),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        with self.voiceover(
            "Ninety years on, much of the work at a forecasting desk still starts from Keynes's accounting. "
            "<bookmark mark='a'/> Output is consumption plus investment plus government purchases plus net exports, "
            "so forecast each and add them up. <bookmark mark='b'/> Consumption from income, wealth and confidence; "
            "investment from firms' orders, interest rates and profits; <bookmark mark='c'/> the government's "
            "budget, with an assumption about its multipliers; and exports from the growth of trading partners. "
            "<bookmark mark='d'/> Then compare the total with what the economy could produce: the output gap, "
            "which tells the desk what to expect for unemployment and inflation."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def gap(self):
        o = load("okun")
        ax = plane([1949, 2026], [-11, 11], center=LEFT * 1.8 + DOWN * 0.3, x_length=8.4, y_length=4.8,
                   xticks=[1950, 1970, 1990, 2010], yticks=[-10, -5, 0, 5, 10], ylabel=r"percentage points",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=16)
        zero = seg(ax, 1949, 0, 2026, 0, color=GREY_D, width=2)
        g = path(ax, o["t"], o["gap"], color=OUTPUT, width=3, smooth=False)
        u = path(ax, o["t"], [-x for x in o["ugap"]], color=PRICE, width=3, smooth=False)
        side = VGroup(
            label(r"output gap: \\ real GDP against the CBO's \\ potential, \ \%", font_size=19, color=OUTPUT),
            label(r"unemployment gap, \ upside down: \\ the CBO's natural rate \\ minus the actual rate", font_size=19,
                  color=PRICE),
            label(r"they move together, \\ the unemployment gap \\ by about half as much", font_size=19,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"BEA: \ real GDP; \ CBO: \ potential GDP and the natural rate; \ BLS: \ unemployment; \ "
                       r"quarterly, \ via FRED", corner=DR, font_size=12)
        with self.voiceover(
            f"Here are America's two gaps, quarter by quarter since {o['first'][:4]}. <bookmark mark='a'/> In green, "
            "real output against the Congressional Budget Office's estimate of what the economy could produce. "
            "<bookmark mark='b'/> In pink, the unemployment rate against the Office's estimate of its natural "
            "rate, turned upside down so that bad times point down for both. <bookmark mark='c'/> They move "
            "together in every recession, the unemployment gap by a little more than half as much as output, and "
            "nowhere more sharply than in the spring of 2020."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(zero), run_time=0.6)
            vo.wait_until("a")
            self.play(Create(g), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(u), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def okun_fact(self):
        o = load("okun")
        f = next(x for x in facts.FACTS if x.key == "okun")
        data_m = label(rf"US, \ {o['first'][:4]}--{o['last'][:4]}: \\ unemployment gap $=$ {o['beta']:.2f} $\times$ "
                       rf"output gap; \\ $R^2 = {o['r2']:.2f}$", font_size=19, color=WHITE)
        theory_m = label(r"output set by demand; \\ firms hire and lay off \\ with sales, \ partly", font_size=19,
                         color=SPEND)
        agora_m = label(rf"about {-1 / o['beta']:.1f} points of output \\ per point of unemployment, \\ against "
                        r"Okun's 3", font_size=19, color=E.AGORA)
        fc = fact_card(tex_safe(f.statement), columns=((r"the data", data_m), (r"the theory", theory_m),
                                                         (r"Agora", agora_m)), width=12.4, font_size=22,
                       colors=(WHITE, SPEND, None)).move_to(UP * 0.3)
        tag = published_tag(r"Okun (1962); \ this film's regression on FRED's data", corner=DR, font_size=12)
        with self.voiceover(
            "That is one of the series' facts: Okun's law. <bookmark mark='a'/> In the data, the unemployment gap "
            f"moves {-o['beta']:.2f} points for each point of the output gap, and the line explains about "
            f"{100 * o['r2']:.0f} percent of the variation. <bookmark mark='b'/> The theory is this part's: when "
            "spending sets output, firms hire and lay off as their sales change, though not one for one, because "
            "hours, effort and productivity absorb some of it. <bookmark mark='c'/> So Agora fills in its column: "
            f"about {-1 / o['beta']:.1f} points of output per point of unemployment in recent American data, "
            "against the three that Okun found, and the two the textbooks quote."
        ) as vo:
            self.play(FadeIn(fc.card), FadeIn(fc[1][0]), *[FadeIn(c[:2]) for c in fc.cols], FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(fc.cols[0][2:]))
            vo.wait_until("b")
            self.play(FadeIn(fc.cols[1][2:]))
            vo.wait_until("c")
            self.play(FadeIn(fc.cols[2][2:]))
        self.clear_scene()

    def cycles(self):
        s = load("spells")
        ys_r, ys_e = np.array(s["rec_start"]), np.array(s["exp_start"])
        rec, exp_ = np.array(s["recessions"]), np.array(s["expansions"])
        ax = plane([1850, 2025], [0, 135], center=LEFT * 1.8 + DOWN * 0.3, x_length=8.4, y_length=4.8,
                   xticks=[1860, 1900, 1940, 1980, 2020], yticks=[0, 30, 60, 90, 120],
                   ylabel=r"length, \ months", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=16)
        er = VGroup(*[Line(ax.ax.c2p(y, 0), ax.ax.c2p(y, m), color=OUTPUT, stroke_width=4) for y, m in
                      zip(ys_e, exp_)])
        rr = VGroup(*[Line(ax.ax.c2p(y + 0.6, 0), ax.ax.c2p(y + 0.6, m), color=PRICE, stroke_width=4) for y, m in
                      zip(ys_r, rec)])
        side = VGroup(
            label(rf"since 1854: \ {s['n_rec']} recessions", font_size=20, color=GREY_A),
            label(rf"expansions: \ {s['exp_mean']:.0f} months on average", font_size=20, color=OUTPUT),
            label(rf"recessions: \ {s['rec_mean']:.0f} months", font_size=20, color=PRICE),
            label(rf"since 1945: \ {s['exp_mean_post']:.0f} against {s['rec_mean_post']:.0f}", font_size=21,
                  color=E.ACCENT),
            label(rf"the longest: \ {s['longest_exp']} months, \\ from {s['longest_exp_start']}", font_size=19,
                  color=OUTPUT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"NBER's business cycle dates, \ via FRED's recession indicator", corner=DR, font_size=12)
        with self.voiceover(
            "A second fact the desk lives with. Here is every American expansion and recession the National Bureau "
            "of Economic Research has dated, by the year it began. <bookmark mark='a'/> Since 1854 there have been "
            f"{s['n_rec']} recessions. <bookmark mark='b'/> Expansions have lasted {s['exp_mean']:.0f} months on "
            f"average, <bookmark mark='c'/> recessions {s['rec_mean']:.0f}. <bookmark mark='d'/> Since 1945 the "
            f"gap has widened: {s['exp_mean_post']:.0f} months against {s['rec_mean_post']:.0f}. "
            f"<bookmark mark='e'/> The longest expansion ran {s['longest_exp']} months, from {s['longest_exp_start']} "
            "to the pandemic. Expansions are long and recessions short: the economy falls quickly and climbs slowly. "
            "Part twenty-nine asks what kind of model produces that."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), LaggedStart(*[Create(x) for x in er], lag_ratio=0.03),
                      LaggedStart(*[Create(x) for x in rr], lag_ratio=0.03), run_time=2.5)
            for mk, r_ in zip("abcde", side):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
        self.clear_scene()
