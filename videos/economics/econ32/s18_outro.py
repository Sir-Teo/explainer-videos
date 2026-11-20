from __future__ import annotations

from videos.economics.econ32.common import *  # noqa: F403

PROBLEMS = [
    r"Debt dynamics: \ from $B_{t+1} = (1+r)B_t - S_t$ and $Y_{t+1} = (1+g)Y_t$, \ derive $b_{t+1}$ and the surplus "
    r"that holds $b$ steady.",
    r"The cross with taxes: \ with consumption $c(1-t)Y$, \ show the spending multiplier is $1/(1 - c(1-t))$; \ "
    r"evaluate it for $c = 0.8$, \ $t = 0.25$.",
    r"Balanced budget: \ in the simple cross, \ show that spending paid for by an equal lump-sum tax has a "
    r"multiplier of one.",
    r"The zero bound: \ in the model of chapter 3 with $i = 0$ and $\gamma = 0$, \ solve for the multiplier and show "
    r"it exceeds one.",
    r"The missing intercept: \ with $y_{rt} = m_L(g_{rt} - \bar g_t) + m_A \bar g_t + u_t + e_{rt}$, \ show that "
    r"year fixed effects estimate $m_L$, \ not $m_A$.",
    r"Tax smoothing: \ minimize $\sum \beta^t \tau_t^2$ subject to $\sum \beta^t \tau_t = \sum \beta^t g_t$; \ show "
    r"the best $\tau_t$ is constant.",
    r"The fiscal theory: \ with $B/P = s/r$, \ find $P$ for $B = 100$, \ $s = 2$, \ $r = 0.02$, \ and after $s$ falls "
    r"to 1.5.",
    r"$\bigstar$ \ Default: \ a country owing $b$ defaults if a random cost $\kappa \sim F$ is below $b$; \ derive "
    r"the bond price $q(b) = (1 - F(b))/(1+r)$ and the most it can raise.",
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
        a = wrapped_label(r"A budget can steady an economy: \ automatic stabilizers always, \ and deliberate spending "
                          r"or tax cuts with multipliers below one in normal times, \ larger when the central bank "
                          r"cannot respond. \ Debt is too much when its interest outruns growth and no one expects the "
                          r"surpluses to pay it; \ with r below g there is more room than the old rules allowed, \ "
                          r"but no threshold, \ and the room shrinks as rates rise.", 11.6, 25, WHITE)
        a.next_to(q, DOWN, buff=0.5)
        F = load("film")
        mini = plane([1889, 2027], [0, 120], x_length=4.2, y_length=1.3)
        logo = path(mini, F["t"], F["debt"], DEBT, 2.4, smooth=False).next_to(a, DOWN, buff=0.35)
        with self.voiceover(
            "So: what can a government's budget do for the economy, and how much debt is too much? "
            "<bookmark mark='a'/> A budget can steady an economy: through automatic stabilizers always, and through "
            "deliberate spending or tax cuts, whose multipliers are below one in normal times and larger when the "
            "central bank cannot respond. Debt is too much when its interest outruns growth and nobody expects the "
            "surpluses that would pay it. With r below g there is more room than the old rules allowed, but there "
            "is no threshold, and the room shrinks as interest rates rise."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo), run_time=1.5)
        self.clear_scene()

    def recap(self):
        H, D, P, N, R, G, T, S, RG, W, U, DF, L = (load(x) for x in ("hap", "debt", "playit", "nk", "rz", "regions",
                                                                     "taxes", "stabilizers", "rg", "war", "unpleasant",
                                                                     "default", "bl"))
        items = [
            (rf"the 90\% threshold: \ {H['steps'][0]['means'][3]:+.1f}\% published, \ "
             rf"{H['steps'][-1]['means'][3]:+.1f}\% corrected", INFL),
            (rf"debt dynamics: \ r minus g; \ US debt {D['peak']:.0f}\% of GDP in 1946, \ {D['last']:.0f}\% now", DEBT),
            (rf"Play it: \ a surplus of {100 * P['stabilizing']:.2f}\% holds the Island's debt", TAX),
            (rf"theory: \ {N['points']['0.5']['normal']:.2f} with Taylor's rule, \ "
             rf"{N['points']['0.5']['zlb']:.2f} at the zero bound", SPEND),
            (rf"evidence: \ military news {R['news8']:.2f}, \ timing {R['bp8']:.2f}; \ regions about 1.5", OUTPUT),
            (rf"taxes: \ {T['trough']:+.1f}\% after a tax rise of 1\% of GDP", TAX),
            (rf"stabilizers: \ the deficit moves {abs(S['slope']):.1f} points per point of unemployment", DEBT),
            (r"austerity: \ contractionary, \ once you ask why the budget changed", HOLD),
            (rf"r below g in {100 * RG['share1']:.0f}\% of American years since 1954", RATE),
            (rf"tax smoothing: \ a war on debt costs {100 * (W['ratio'] - 1):.0f}\% less than pay-as-you-go", TAX),
            (rf"unpleasant arithmetic: \ tight money now, \ {100 * U['mu_after_tight']:.1f}\% money growth "
             r"later", INFL),
            (rf"default: \ {100 * DF['sim']['default_rate_annual']:.1f}\% a year in Arellano's model, \ in bad times",
             DEBT),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 32, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        del G, L
        with self.voiceover(
            "Part thirty-two in twelve lines. <bookmark mark='a'/> A spreadsheet's missing rows turned a cliff into "
            "a slope. Debt grows by itself only when the interest rate exceeds growth. Holding the Island's debt "
            "steady took a primary surplus of about one percent of GDP. In theory, the multiplier is below one when "
            "the central bank responds and above one at the zero bound. In the evidence, national multipliers are "
            "below one and regional ones above. Tax changes cost two to three times their size in output. "
            "Automatic stabilizers do much of the work unasked. Austerity contracts, once you ask why the budget "
            "changed. In American history, r has usually been below g. Debt should absorb wars. Tight money can "
            "mean more inflation later if the treasury does not change course. And countries default in bad "
            "times, when borrowing is dearest."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=42.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19, width=13.0)
        with self.voiceover(
            "The problems. Debt dynamics; the cross with taxes and the balanced budget; the multiplier at the zero "
            "bound; the missing intercept; tax smoothing; the fiscal theory; and a starred problem on the price of "
            "a defaultable bond. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Olivier Blanchard, \emph{Fiscal Policy under Low Interest Rates} (2023)",
             r"David Romer, \emph{Advanced Macroeconomics} (5th ed., 2019), \ ch.\ 13",
             r"Valerie Ramey, ``Ten Years After the Financial Crisis: \ What Have We Learned from the Renaissance in "
             r"Fiscal Research?'', \ \emph{JEP} 33(2) (2019)",
             r"John Cochrane, \emph{The Fiscal Theory of the Price Level} (2023)"],
            [r"Domar (1944); \ Barro (1974, 1979); \ Diamond (1965); \ Sargent and Wallace (1981); \ Sims (1994)",
             r"Blanchard and Perotti (2002); \ Ramey (2011); \ Nakamura and Steinsson (2014); \ Ramey and Zubairy "
             r"(2018)",
             r"Romer and Romer (2010); \ Alesina and Ardagna (2010); \ Guajardo, \ Leigh and Pescatori (2014)",
             r"Reinhart and Rogoff (2010); \ Herndon, \ Ash and Pollin (2014); \ Blanchard and Leigh (2013)",
             r"Eaton and Gersovitz (1981); \ Arellano (2008); \ Blanchard (2019)"])
        with self.voiceover(
            "The reading: Olivier Blanchard's book on fiscal policy when interest rates are low; Romer's chapter on "
            "budget deficits; Valerie Ramey's survey of what the renaissance in fiscal research has learned; and "
            "John Cochrane's fiscal theory. Then the papers, from Domar to Arellano."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(2008, r"Queen Elizabeth II", r"at the London School of Economics, \ 5 November 2008: \ why "
                          r"did nobody notice it? \ The British Academy's reply, \ July 2009: \ a failure of the "
                          r"collective imagination of many bright people", color=E.ACCENT, width=10.4, font_size=24)
        nxt = VGroup(label(r"Next: \ Part 33 \ $\cdot$ \ Act VI, \ Money and the Cycle", font_size=30, color=GREY_B),
                     label(r"Crises", font_size=46),
                     label(r"why do financial systems blow up, \ and why is it so hard to see it coming?",
                           font_size=26, color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"this part: \ the budget; \ next: \ when the whole system breaks", font_size=26,
                     color=GREY_A).to_edge(UP, buff=0.5)
        VGroup(hc, nxt).arrange(DOWN, buff=0.6).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "This part was about the budget. The next is about the moments when the whole system breaks. "
            "<bookmark mark='a'/> On the fifth of November 2008, opening a building at the London School of "
            "Economics, Queen Elizabeth asked why nobody had noticed the crisis coming. The British Academy's reply, "
            "the following July, put it down to a failure of the collective imagination of many bright people to "
            "understand the risks to the system as a whole. <bookmark mark='b'/> Part thirty-three: crises. Why do "
            "financial systems blow up, and why is it so hard to see it coming?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(9.5)
        self.clear_scene()
