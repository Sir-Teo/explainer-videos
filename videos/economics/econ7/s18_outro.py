from __future__ import annotations

from videos.economics.econ7.common import *  # noqa: F403

PROBLEMS = [
    r"Fisher: \ incomes \$120 and \$40, \ $r$ = 10\%, \ $\beta = 0.9$, \ $u = -1/c$. \ Find $c_1$, $c_2$ and saving, "
    r"\ and check the Euler equation. \ How does saving change at $r$ = 30\%?",
    r"Show that only exponential discounting makes $D(t+1)/D(t)$ the same at every $t$. \ What is it for $1/(1+t)$?",
    r"Ana: \ \$60 or \$180, 50--50, \ against \$100 for sure. \ Find the certainty equivalent for $\gamma$ = 1 and "
    r"2, \ and the $\gamma$ at which she is indifferent.",
    r"Allais: \ show $EU(1A) - EU(1B) = EU(2A) - EU(2B)$ for every $u$. \ Draw the four lotteries in the triangle.",
    r"Insurance: \ wealth \$300, \ a \$150 loss with chance 0.1, \ $\gamma = 2$. \ Find the most Ana pays for full "
    r"cover, \ and show that with a positive loading she buys less than full cover.",
    r"A risky asset: \ premium 6 points, \ s.d.\ 20\%. \ Merton's share for $\gamma$ = 2 and 10. \ What $\gamma$ "
    r"makes a household hold 25\% in it?",
    r"Rabin: \ a CRRA chooser with \$100{,}000 rejects lose \$100 / win \$110. \ Show $\gamma \approx 90$, \ and "
    r"that she rejects lose \$1{,}000 / win any sum.",
    r"$\bigstar$ \ Hall's regression uses instruments lagged two years. \ Simulate monthly consumption that obeys the "
    r"Euler equation exactly, \ average it to years, \ and show why one lag is not enough.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.answer()
        self.recap()
        self.problems()
        self.references()
        self.next_part()

    def answer(self):
        q = wrapped_label(ASK, 12.0, 42, E.ACCENT).move_to(UP * 2.0)
        a = wrapped_label(r"By weighing: \ later against now with a discount factor and the interest rate, \ and "
                          r"chances against outcomes with a utility that bends. \ The theory is coherent and useful: "
                          r"\ it prices insurance and pensions and assets. \ But people break it in systematic ways: "
                          r"\ they weigh shared parts, unknown odds, small stakes and the present moment differently, "
                          r"\ and the numbers that measure them depend on how they are asked.", 11.6, 29, WHITE)
        a.next_to(q, DOWN, buff=0.55)
        logo = VGroup(coin_glyph(0.4, "H"), coin_glyph(0.4, "T", GREY_B)).arrange(RIGHT, buff=0.25).next_to(
            a, DOWN, buff=0.45)
        with self.voiceover(
            "So: how do people choose when the pay-off comes later, or may not come at all? "
            "<bookmark mark='a'/> By weighing. Later against now, with a discount factor and the interest rate; "
            "chances against outcomes, with a utility function that bends. The theory is coherent and useful: it "
            "prices insurance, pensions and assets. But people break it in systematic ways. They care about what two "
            "options share, about whether the odds are known, about small stakes, and about the present moment, "
            "more than the theory allows; and the numbers that measure them depend on how they are asked."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in logo], lag_ratio=0.4))
        self.clear_scene()

    def recap(self):
        s, f, d, av, ins, fl, r, pr, m = (load(x) for x in ("stpete", "fisher", "discount", "aversion", "insurance",
                                                           "film", "rabin", "present", "measuring"))
        items = [
            (rf"St Petersburg: \ an infinite expectation; \ Bernoulli's price \${s['named']['1000']['log']:.2f} "
             r"at \$1{,}000", COINC),
            (rf"Fisher: \ the interest rate is a price; \ Chidi saves \${f['f0']['saving']:.2f}; \ the EIS "
             r"decides the response", TODAY),
            (rf"discounting: \ \$100 in 30 years is \${d['pv']['0.03'][-1]:.2f} at 3\%, \ "
             rf"\${d['pv']['0.1'][-1]:.2f} at 10\%; \ only exponential is consistent", LATER),
            (r"expected utility: \ independence makes its lines straight and parallel", EUL),
            (r"Allais: \ 1A with 2B; \ the lines fan out", FAN),
            (rf"risk aversion: \ the sea's certainty equivalent \${av['rows'][2]['ce']:.0f} against \$120; \ "
             r"$\tfrac12 A\sigma^2$", UTIL),
            (rf"insurance: \ full cover at fair odds; \ a \$100 deductible premium needs $\gamma \approx "
             rf"{ins['deductible']['rows'][2][1]:.0f}$", RISKY),
            (rf"Hall's century: \ consumption growth on the real rate, \ instrumented slope "
             rf"{signed(fl['full']['iv'], 2)}", E.ACCENT),
            (r"dominance: \ first order for everyone who likes more, \ second for every risk averter", SAFE),
            (rf"Ellsberg: \ ambiguity aversion; \ Rabin: \ refuse \$100/\$110 at \$100{{,}}000 $\Rightarrow$ "
             rf"$\gamma$ = {r['gamma']:.0f}", AMBIG),
            (rf"present bias: \ Chidi's last week {pr['naive'][-1]:.0f} coconuts, \ not {pr['plan'][-1]:.0f}; \ "
             r"commitment has value", BIAS),
            (rf"measuring: \ Holt and Laury, \ the Island's menu {m['mean_scored']:.2f} vs {m['mean_true']:.2f}; "
             r"\ both dials contested", WHITE),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\ \ {txt}", font_size=28, color=col) for i, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 7, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part seven in twelve lines. <bookmark mark='a'/> The St Petersburg game has an infinite expected prize "
            "and a small price, and Bernoulli's answer was the first utility function. Fisher made the interest rate "
            "a price, and the Euler equation says how saving responds, through the elasticity of substitution. "
            "Discounting adds up the future, and only the exponential kind keeps a plan consistent. Expected utility "
            "follows from independence, which makes indifference lines straight and parallel, and Allais's pairs bend "
            "them into a fan. Risk aversion is curvature, measured by Arrow and Pratt, and it explains insurance, "
            "though not the deductibles people buy. A century of American data finds the elasticity near zero. "
            "Dominance ranks some gambles for everyone. Ellsberg found aversion to ambiguity, and Rabin showed that "
            "small-stakes caution can't come from the curvature of utility over wealth. Present bias breaks plans "
            "and gives commitment a value. And the measurements of both dials are contested."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=40.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20, width=13.0)
        with self.voiceover(
            "The problems. Fisher's two periods, by hand; why only exponential discounting is consistent; Ana's "
            "certainty equivalents; Allais's algebra and the triangle; the most a risk averter pays for insurance; "
            "Merton's share; Rabin's calibration for the power function; and a research problem, marked with a star, "
            "on why Hall had to lag his instruments twice. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Hal Varian, \emph{Intermediate Microeconomics}, chs.\ 10--13",
             r"Andreu Mas-Colell, Michael Whinston and Jerry Green, \emph{Microeconomic Theory}, ch.\ 6",
             r"David Kreps, \emph{Microeconomic Foundations I}, chs.\ 5--6",
             r"Christian Gollier, \emph{The Economics of Risk and Time} (2001)"],
            [r"Bernoulli (1738); \ Fisher, \emph{The Theory of Interest} (1930); \ Samuelson (1937); \ Koopmans (1960)",
             r"von Neumann and Morgenstern (1944); \ Savage (1954); \ Allais (1953); \ Ellsberg (1961)",
             r"Pratt (1964); \ Arrow (1965); \ Mossin (1968); \ Merton (1969); \ Rothschild and Stiglitz (1970)",
             r"Kahneman and Tversky (1979); \ Machina (1982); \ Gilboa and Schmeidler (1989); \ Rabin (2000)",
             r"Kreps and Porteus (1978); \ Epstein and Zin (1989); \ Mehra and Prescott (1985); \ Weil (1989); \ "
             r"Hall (1988)",
             r"Strotz (1955--56); \ Laibson (1997); \ Holt and Laury (2002); \ Barsky et al.\ (1997); \ Hayden and "
             r"Platt (2009)",
             r"Hansen and Sargent, \emph{Robustness} (2008); \ Manski (2004); \ Madrian and Shea (2001); \ Thaler and "
             r"Benartzi (2004)"])
        with self.voiceover(
            "The reading for this part: Varian's chapters on intertemporal choice and uncertainty; chapter six of "
            "Mas-Colell, Whinston and Green for the graduate version; Kreps's Microeconomic Foundations; and Christian "
            "Gollier's book, The Economics of Risk and Time, for everything beyond. Then the papers, from Bernoulli to "
            "Hansen and Sargent."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1927, r"Paul Douglas \ and Charles Cobb", r"labour's share of American manufacturing "
                          r"income hardly moves; \ Douglas asks a mathematician for a function that would make it so",
                          color=E.ACCENT, width=9.0, font_size=26).move_to(UP * 0.6)
        lead = label(r"from people who choose \ to firms that produce", font_size=40, color=GREY_A)
        nxt = VGroup(label(r"Next: \ Part 8", font_size=30, color=GREY_B),
                     label(r"The Firm", font_size=56, color=WHITE),
                     label(r"how does a firm decide what to make and how, \ and why is there a firm at all?",
                           font_size=26, color=GREY_A)).arrange(DOWN, buff=0.15).next_to(hc, DOWN, buff=0.6)
        with self.voiceover(
            "This part finishes Act Two's account of how people choose. The last part of the act turns to the other "
            "side of every market: the firm. "
            "<bookmark mark='a'/> In 1927 the economist Paul Douglas noticed that labour's share of American "
            "manufacturing income hardly moved from year to year, and asked the mathematician Charles Cobb for a "
            "function that would make it so. <bookmark mark='b'/> Part eight: the firm."
        ) as vo:
            self.play(FadeIn(lead))
            vo.wait_until("a")
            self.play(FadeOut(lead), FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.1))
        self.wait(3.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)
