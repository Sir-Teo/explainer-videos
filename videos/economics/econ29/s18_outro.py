from __future__ import annotations

from videos.economics.econ29.common import *  # noqa: F403

PROBLEMS = [
    r"The finite cake: \ with $T$ days left and $u = \log c$, \ show $c_t = w_t / (1 + \beta + \dots + "
    r"\beta^{T-t})$; \ let $T \to \infty$.",
    r"Guess and verify with $u = c^{1-\sigma}/(1-\sigma)$: \ show $c = (1 - \beta^{1/\sigma})\, w$.",
    r"Blackwell: \ show that the cake's Bellman operator $T$ satisfies $\|TV - TW\| \le \beta \|V - W\|$.",
    r"Brock--Mirman: \ verify $V = a + \frac{\alpha}{1-\alpha\beta}\log k + \frac{1}{(1-\alpha\beta)(1-\beta\rho)}"
    r"\log z$ \ and $k' = \alpha\beta z k^\alpha$.",
    r"The steady state: \ with $\alpha = 0.36$, \ $\beta = 0.99$, \ $\delta = 0.025$, \ find $\bar k/\bar y$ and "
    r"$\bar\imath/\bar y$.",
    r"Hansen: \ with $u = \log c - A n$, \ show the wage is $A c$ \ and $\hat n = (\hat z + \alpha \hat k - \hat c)/"
    r"\alpha$.",
    r"The saddle: \ $x_{t+1} = M x_t$ with roots $0.9$ and $1.1$, \ $k$ predetermined, \ $c$ free; \ find the "
    r"unique stable path.",
    r"$\bigstar$ \ Rouwenhorst: \ for two states $\pm\psi$ and $p = (1+\rho)/2$, \ show the autocorrelation is "
    r"$\rho$; \ choose $\psi$.",
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
        a = wrapped_label(r"In a model with one household, \ no money and no frictions, \ yes: \ the Island's booms "
                          r"and slumps are its best response to luck, \ and they look a lot like America's. \ But "
                          r"the shocks were partly mismeasured, \ hours and productivity do not move together, \ and "
                          r"money and housing lead the cycle. \ The claim failed; \ the method of optimizing agents, "
                          r"\ equilibrium, \ computation and honest comparison with data became how all of "
                          r"macroeconomics is done.", 11.6, 25, WHITE)
        a.next_to(q, DOWN, buff=0.5)
        R = load("rbc")
        mini = plane([0, 120], [-4, 4], x_length=4.2, y_length=1.2)
        logo = path(mini, np.arange(120), np.clip(np.array(R["sim_hp"]["y"])[-120:], -4, 4), OUTPUT, 3,
                    smooth=False)
        logo.next_to(a, DOWN, buff=0.35)
        with self.voiceover(
            "So: could booms and slumps be an economy's best response to shocks it cannot avoid? "
            "<bookmark mark='a'/> In a model with one household, no money and no frictions, yes. The Island's booms "
            "and slumps are its best response to luck, and they look a lot like America's. But the shocks were "
            "partly mismeasured, hours and productivity do not move together the way the model says, and money and "
            "housing lead the cycle. The claim failed. The method, optimizing households and firms, equilibrium, "
            "computation and an honest comparison with the data, became the way all of macroeconomics is done."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo), run_time=1.5)
        self.clear_scene()

    def recap(self):
        C, P, K, Ch, B, F, R, Fa, S, G, W = (load(x) for x in ("cycle", "play", "cake", "chains", "bm", "frisch",
                                                               "rbc", "facts", "solow", "gali", "wedges"))
        lead = -P["series"]["A011RA3Q086SBEA"]["peak_q"]
        items = [
            (r"Kydland and Prescott, \ 1982: \ the growth model plus random technology", E.ACCENT),
            (rf"the cycle: \ HP gives {C['sd_hp']:.1f}\%, \ Hamilton {C['sd_ham']:.1f}\%; \ the end point is a "
             r"guess", OUTPUT),
            (rf"Play it: \ housing turns first, \ about {lead} quarters before the peak", HOUSING),
            (rf"the cake: \ eat $1 - \beta$ of what is left; \ iteration converges at rate $\beta$ \ "
             rf"({K['iterations']} steps)", POLICY),
            (rf"Brock and Mirman: \ save $\alpha\beta = {B['saving_rate']:.2f}$; \ Rouwenhorst exact, \ Tauchen "
             r"stuck", TECH),
            (rf"labour: \ at $\varphi = 0.5$ hours barely move; \ Hansen's shifts give {F['hansen']['n_rel']:.2f}",
             HOURS),
            (r"calibration against estimation", VALUE),
            (rf"the saddle: \ roots {R['moduli'][0]:.2f}, \ {R['moduli'][1]:.2f}, \ {R['moduli'][2]:.2f}; \ one "
             r"path in", INVEST),
            (rf"the scorecard: \ size and order right; \ hours with productivity {Fa['model']['corr_nw']:.2f} "
             rf"against {Fa['data']['corr_nw']:.2f}", OUTPUT),
            (rf"the residual fell {abs(S['y1982']):.1f}\% in 1982; \ Gal\'i's hours fall, \ in levels they rise",
             TECH),
            (rf"what survived: \ DSGE, \ wedges \ (labour wedge {W['corr']:.2f}), \ news, \ uncertainty", E.ACCENT),
            (r"the Frisch dial: \ 0.5 in people, \ near 3 in models; \ Prescott partly right", HOLD),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 29, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        del Ch, G
        with self.voiceover(
            "Part twenty-nine in twelve lines. <bookmark mark='a'/> Kydland and Prescott added random technology "
            "to the growth model. A cycle is a gap from a trend, and the filter decides its size and, near the end, "
            "even its sign. Housing turns first. Dynamic programming turns an infinite plan into one equation, and "
            "iterating it converges because it is a contraction. Brock and Mirman's economy saves a fixed share, "
            "and shocks become Markov chains, some better built than others. Hours barely move with the elasticity "
            "workers show; Hansen's shifts fix that. Calibration fought estimation. Solving the model is counting "
            "roots. The scorecard gets the size and order of the cycle right, and hours with productivity "
            "completely wrong. The measured shocks were partly not technology, and the evidence on hours is split. "
            "The method survived, with wedges, news and uncertainty. And the Frisch dial, half in people and near "
            "three in models, with Prescott's forecast partly right."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=46.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20, width=13.0)
        with self.voiceover(
            "The problems. The finite cake; the cake with a different utility; Blackwell's contraction; Brock and "
            "Mirman's closed form; the steady state; Hansen's labour condition; a saddle path by hand; and a "
            "starred problem on Rouwenhorst's chain. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Nancy Stokey, \ Robert Lucas and Edward Prescott, \emph{Recursive Methods in Economic Dynamics} "
             r"(1989), \ chs.\ 1--4",
             r"Lars Ljungqvist and Thomas Sargent, \emph{Recursive Macroeconomic Theory} (4th ed., 2018), \ chs.\ "
             r"3--4",
             r"David Romer, \emph{Advanced Macroeconomics} (5th ed., 2019), \ ch.\ 5",
             r"Robert King and Sergio Rebelo, \ ``Resuscitating Real Business Cycles'', \ \emph{Handbook of "
             r"Macroeconomics} (1999)"],
            [r"Kydland and Prescott (1982); \ Long and Plosser (1983); \ Hansen (1985); \ Rogerson (1988)",
             r"Prescott (1986); \ Summers (1986); \ Brock and Mirman (1972); \ Blanchard and Kahn (1980)",
             r"Hodrick and Prescott (1997); \ Hamilton (2018); \ Tauchen (1986); \ Kopecky and Suen (2010)",
             r"Gal\'i (1999); \ Christiano, \ Eichenbaum and Vigfusson (2003); \ Basu, \ Fernald and Kimball (2006)",
             r"Chari, \ Kehoe and McGrattan (2007); \ Chetty, \ Guren, \ Manoli and Weber (2011)"])
        with self.voiceover(
            "The reading: Stokey, Lucas and Prescott's Recursive Methods for dynamic programming; Ljungqvist and "
            "Sargent's Recursive Macroeconomic Theory; Romer's chapter on real business cycles, which this part "
            "follows; and King and Rebelo's survey, Resuscitating Real Business Cycles. Then the papers, from "
            "Kydland and Prescott to the review behind the dial."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(2004, r"Bils and Klenow", r"they open the price collectors' records behind the consumer "
                          r"price index and count how often each price changes", color=E.ACCENT, width=10.4,
                          font_size=24)
        nxt = VGroup(label(r"Next: \ Part 30 \ $\cdot$ \ Act VI, \ Money and the Cycle", font_size=30, color=GREY_B),
                     label(r"Sticky Prices", font_size=46),
                     label(r"why does money move the real economy?", font_size=26, color=E.ACCENT)).arrange(
            DOWN, buff=0.22)
        head = label(r"this part: \ a cycle without money; \ next: \ money in the cycle", font_size=26,
                     color=GREY_A).to_edge(UP, buff=0.5)
        VGroup(hc, nxt).arrange(DOWN, buff=0.6).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "This part built a cycle with no money in it. The next puts money back. <bookmark mark='a'/> In 2004, "
            "Mark Bils and Peter Klenow opened the records of the price collectors behind America's consumer price "
            "index and counted how often each price changes: every few months, far more often than economists had "
            "assumed, and yet not often enough for money to be neutral. <bookmark mark='b'/> Part thirty: sticky "
            "prices. Why does money move the real economy, and what is the best a central bank can do?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(9.5)
        self.clear_scene()
