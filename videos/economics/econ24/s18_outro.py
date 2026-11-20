from __future__ import annotations

from videos.economics.econ24.common import *  # noqa: F403

PROBLEMS = [
    r"The tub: \ from $u_{t+1} = u_t + s(1-u_t) - f u_t$, \ derive $u^* = s/(s+f)$, \ and show that a gap from $u^*$ "
    r"shrinks by the factor $1 - s - f$ each month.",
    r"McCall: \ derive $w^* - b = \frac{\beta}{1-\beta}\int_{w^*}(w - w^*)\,dF(w)$, \ and solve it when offers are "
    r"uniform on $[\ell, h]$.",
    r"Urns and balls: \ show that $U$ applicants choosing among $V$ openings at random fill "
    r"$V\big(1-(1-\frac1V)^U\big)$ on average, \ and that the limit $V(1 - e^{-U/V})$ has constant returns.",
    r"Matching: \ with $M = A U^\eta V^{1-\eta}$, \ find $f(\theta)$ and $q(\theta)$ and their elasticities with "
    r"respect to $\theta$.",
    r"Job creation: \ from $r\mathcal{V} = -c + q(\theta)(\mathcal{J} - \mathcal{V})$, \ $r\mathcal{J} = p - w - "
    r"s\mathcal{J}$ and free entry, \ derive $c/q(\theta) = (p - w)/(r + s)$.",
    r"The wage: \ with $r\mathcal{W} = w + s(\mathcal{U} - \mathcal{W})$, \ $r\mathcal{U} = b + f(\theta)(\mathcal{W} "
    r"- \mathcal{U})$ and $\mathcal{W} - \mathcal{U} = \beta S$, \ derive $w = (1-\beta)b + \beta(p + c\theta)$.",
    r"Hosios: \ as $r \to 0$, \ show that $(1-u)p + ub - cv$ is maximized over $\theta$ where $\beta = \eta$.",
    r"$\bigstar$ \ The fundamental surplus: \ from the equation for $\theta$, \ derive $\frac{d\ln\theta}{d\ln p} = "
    r"\frac{r + s + \beta f}{\eta(r+s) + \beta f}\cdot\frac{p}{p - b}$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.answer()
        self.recap()
        self.problems()
        self.references()
        self.next_part()

    def answer(self):
        q = wrapped_label(ASK, 12.0, 42, E.ACCENT).move_to(UP * 2.2)
        a = wrapped_label(r"Because finding each other takes time. \ Workers and firms meet through a matching "
                          r"process with constant returns; \ firms open vacancies until hiring costs what a worker is "
                          r"worth; \ wages split each match's surplus. \ Together they fix tightness, \ and the flows "
                          r"fix unemployment and vacancies, \ both positive, \ for ever. \ But with ordinary numbers "
                          r"the model's unemployment barely moves in a recession, \ and the real one moves more than "
                          r"ten times as much.", 11.6, 27, WHITE)
        a.next_to(q, DOWN, buff=0.55)
        b = load("beveridge")
        mini = plane([3, 15], [1.5, 7.5], x_length=4.2, y_length=1.3)
        logo = path(mini, b["u"], b["v"], TIGHT, width=3, smooth=False)
        logo.next_to(a, DOWN, buff=0.4)
        with self.voiceover(
            "So: why are there unemployed workers and unfilled jobs at the same time? <bookmark mark='a'/> Because "
            "finding each other takes time. Workers and firms meet through a matching process with roughly "
            "constant returns. Firms open vacancies until hiring costs what a worker is worth, and wages split "
            "each match's surplus. Together these fix the market's tightness, and the flows fix unemployment and "
            "vacancies, both positive, for ever. But with ordinary numbers the model's unemployment barely moves "
            "in a recession, and the real one moves more than ten times as much."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo), run_time=1.5)
        self.clear_scene()

    def recap(self):
        j, p, m, d, h, v, f, lad, n = (load(k) for k in ("jolts", "playit", "matching", "dmp", "hosios",
                                                         "volatility", "flows", "ladder", "natural"))
        st = d["steady"]
        items = [
            (rf"stocks and flows: \ {j['mean_hires'] / 1000:.1f} million hires a month, \ a net change of "
             rf"{j['mean_net']:.0f} thousand", WORKER),
            (rf"Play it: \ take the first offer of at least {p['reservation']:.1f}; \ rule C was almost right", YOU),
            (r"McCall: \ stop when one more month of looking costs what it gains", BENEFIT),
            (r"the Beveridge curve: \ along it in booms and slumps, \ out when matching worsens", TIGHT),
            (rf"the matching function: \ constant returns, \ $\eta \approx {m['f_eta']:.2f}$ in the American data",
             MATCH),
            (rf"DMP: \ the Island at $\theta = {st['theta']:.2f}$, \ unemployment {pc(st['u'])} \ and vacancies "
             rf"{pc(st['v'])}", JOB),
            (r"Nash bargaining: \ $w = (1-\beta)b + \beta(p + c\theta)$", WAGE),
            (rf"Hosios: \ net output peaks at $\beta = {h['best']:.2f} = \eta$", WAGE),
            (rf"the puzzle: \ the data's {v['ratio']:.0f} against the model's {v['shimer']['elasticity']:.1f}; \ "
             r"Called it? \ partly right", HOLD),
            (rf"ins and outs: \ job finding, \ {100 * f['share_f']:.0f}\% \ of unemployment's swings", MATCH),
            (rf"the ladder: \ identical workers earn {lad['w_lo']:.2f} to {lad['w_hi']:.2f}; \ firms have power over "
             r"wages", MATCH),
            (rf"the natural rate, \ {n['nrou_2025']:.1f}\%; \ scars that double in recessions; \ two dials; \ "
             r"remote search", SEP),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {txt}", font_size=28, color=col) for k, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 24, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part twenty-four in twelve lines. <bookmark mark='a'/> Millions of jobs begin and end every month "
            "while the net change is small. The best searcher takes the first offer above a reservation wage, and "
            "stops when one more month of looking costs what it is expected to gain. The Beveridge curve slopes "
            "down, and shifts out when matching gets worse. Hires come from a matching function with constant "
            "returns. Free entry and bargaining fix the market's tightness, and with it unemployment and "
            "vacancies. The wage splits the surplus, and the market is efficient only when the worker's share "
            "equals the matching elasticity. Productivity moves the model's tightness less than a tenth as much as "
            "the real one, and twenty years of repairs all work by shrinking the fundamental surplus. Most of "
            "unemployment's swings come from job finding. Workers climb ladders, and identical workers earn "
            "different wages. And the natural rate, the scars of a recession, two dials, and the geography of "
            "remote search."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=46.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20, width=13.0)
        with self.voiceover(
            "The problems. The tub's steady state and its speed; McCall's reservation wage; urns and balls; the "
            "matching function's two rates; the job-creation condition; the Nash wage; Hosios's condition; and a "
            "starred problem deriving the fundamental surplus. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Christopher Pissarides, \emph{Equilibrium Unemployment Theory} (2nd ed., 2000), \ ch.\ 1 on",
             r"Pierre Cahuc, St\'ephane Carcillo and Andr\'e Zylberberg, \emph{Labor Economics} (2nd ed., 2014), "
             r"\ chs.\ 5, 9",
             r"Lars Ljungqvist and Thomas Sargent, \emph{Recursive Macroeconomic Theory} (4th ed., 2018), \ "
             r"search and matching",
             r"Richard Rogerson, Robert Shimer and Randall Wright, \ JEL 43(4) (2005): \ the survey"],
            [r"Stigler (1961); \ McCall (1970); \ Diamond (1982); \ Mortensen and Pissarides (1994); \ Hosios (1990)",
             r"Butters (1977); \ Petrongolo and Pissarides (2001); \ Davis and Haltiwanger (1992); \ Katz and Meyer "
             r"(1990)",
             r"Shimer (2005, 2012); \ Hall (2005); \ Hagedorn and Manovskii (2008); \ Pissarides (2009); \ Ljungqvist "
             r"and Sargent (2017)",
             r"Elsby, Michaels and Solon (2009); \ Burdett and Mortensen (1998); \ Topel and Ward (1992); \ Manning "
             r"(2003)",
             r"Kroft, Lange and Notowidigdo (2013); \ Davis and von Wachter (2011); \ Card, Chetty and Weber (2007)",
             r"Horton (2017); \ Belot, Kircher and Muller (2019); \ Hershbein and Kahn (2018); \ Marinescu and "
             r"Rathelot (2018); \ Hansen et al.\ (2023)"])
        with self.voiceover(
            "The reading: Pissarides's Equilibrium Unemployment Theory, the model's own book; Cahuc, Carcillo and "
            "Zylberberg for the labour economics; Ljungqvist and Sargent for the recursive methods; and the survey "
            "by Rogerson, Shimer and Wright. Then the papers, from Stigler to the geography of remote work."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1910, r"the island of Yap", r"the money is limestone wheels; \ one lies on the seabed, \ "
                          r"lost from a raft, \ and its owners are still counted rich", color=E.ACCENT, width=10.4,
                          font_size=24)
        nxt = VGroup(label(r"Next: \ Part 25 \ $\cdot$ \ Act VI, \ Money and the Cycle", font_size=30, color=GREY_B),
                     label(r"Money", font_size=46),
                     label(r"what is money, \ and what happens when there is too much of it?", font_size=26,
                           color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"Act V: \ how economies grow, \ save, \ invest and employ; \ Act VI: \ money and the cycle",
                     font_size=25, color=GREY_A).to_edge(UP, buff=0.5)
        VGroup(hc, nxt).arrange(DOWN, buff=0.6).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "That closes Act Five: how economies grow, save, invest, and put people to work. Act Six is money and "
            "the cycle. <bookmark mark='a'/> On the island of Yap, as an American visitor described it in 1910, "
            "the money was great limestone wheels. One lay at the bottom of the sea, lost from a raft, and its "
            "owners were still counted rich. <bookmark mark='b'/> Part twenty-five: money. What is it, and what "
            "happens when there is too much of it?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(9.5)
        self.clear_scene()
