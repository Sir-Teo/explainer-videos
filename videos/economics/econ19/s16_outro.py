from __future__ import annotations

from videos.economics.econ19.common import *  # noqa: F403

PROBLEMS = [
    r"The steady state: \ with $y = A (X/L)^{\beta}$ and population growth $\lambda \ln(y/\bar y)$, \ find $L^*$, \ and "
    r"show that raising $A$ by half multiplies $L^*$ by $1.5^{1/\beta}$ and leaves $y^*$ unchanged.",
    r"The plague: \ if 45\% die and $\beta = 0.6$, \ by how much does income per head jump? \ Linearize the recovery "
    r"and find its half-life when $\lambda = 0.02$.",
    r"England's curve: \ with the decade averages, \ estimate the elasticity of real wages to population for "
    r"1270--1640, \ and explain why ordinary standard errors overstate its precision.",
    r"Growth rates: \ from the Bank of England's series, \ compute England's growth of GDP per head for 1270--1650, "
    r"\ 1650--1800 and 1800--2016, \ and the doubling time of each.",
    r"Engels's pause: \ index output per head and real wages to 1780, \ and find each one's growth to 1840; \ what "
    r"happened to the share of income going to labour?",
    r"Quantity and quality: \ maximize $h(e,g)/(\tau + e)$ with $h = (e + \rho\tau)/(e + \rho\tau + g)$, \ and find "
    r"the threshold $g$ above which parents educate.",
    r"Kremer: \ if $\dot A / A = \phi L$ and population is always at its Malthusian level $L \propto A^{1/\beta}$, \ "
    r"show that population growth rises with population.",
    r"$\bigstar$ \ Spatial noise: \ two independent fields with covariance $e^{-d/\ell}$ on $n$ sites; \ explain why "
    r"the OLS $t$-statistic's variance exceeds one, \ and how a spatial HAC correction fixes it.",
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
        a = wrapped_label(r"Because in a world of fixed land, \ every gain in technology became more people rather than "
                          r"more income: \ Malthus's trap, \ which England's wages obeyed for five centuries. \ What "
                          r"changed was that technology began to improve faster than population could catch it, \ and "
                          r"then that parents, \ facing a world where skills paid, \ chose fewer, \ better-educated "
                          r"children. \ Why it began in north-western Europe around 1800 is still argued: \ prices, \ "
                          r"ideas and institutions all played a part.", 11.6, 27, WHITE)
        a.next_to(q, DOWN, buff=0.55)
        p = load("playit")
        mini = plane([1270, 2016], [0, 30000], x_length=4.2, y_length=1.4)
        logo = path(mini, p["years"], p["gdppc"], color=GDP, width=4, smooth=False)
        VGroup(mini, logo).next_to(a, DOWN, buff=0.4)
        with self.voiceover(
            "So: why was almost everyone poor for almost all of history, and what changed? <bookmark mark='a'/> "
            "Because in a world of fixed land, every gain in technology turned into more people rather than more "
            "income. That was Malthus's trap, and England's wages obeyed it for five centuries. What changed was that "
            "technology began to improve faster than population could catch it, and then that parents, in a world "
            "where skills paid, chose fewer, better-educated children. Why it began in north-western Europe, around "
            "1800, is still argued: prices, ideas and institutions all played a part."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo), run_time=1.5)
        self.clear_scene()

    def recap(self):
        p, e, b, ind = load("playit"), load("elasticity"), load("plague"), load("industrial")
        items = [
            (r"Malthus, \ 1798: \ population geometric, \ food arithmetic", POP),
            (rf"Play it: \ England's income per head leaves the floor around 1800; \ $\times${p['ratio_1800_2016']:.0f} "
             r"since", GDP),
            (r"the model: \ diminishing returns plus a population that follows income; \ a stable trap", WAGE),
            (rf"England's curve: \ 1\% more people, \ {-e['before']['slope']:.1f}\% lower wages, \ until about 1640",
             WAGE),
            (rf"the Black Death: \ {100 * b['drop']:.0f}\% die, \ wages $\times${b['wage_x_1450']:.1f} by 1450, \ then "
             r"back", DEATH),
            (r"why Britain: \ dear labour and cheap coal, \ useful knowledge, \ Parliament and credit", TECH),
            (r"why not China: \ a late accident, \ or a long lead? \ around 1700, \ say the new accounts", CN),
            (rf"the revolution in numbers: \ slow until 1830; \ Engels's pause in wages", GDP),
            (r"the demographic transition: \ deaths fall first, \ then births", POP),
            (r"one model: \ a scale effect and the quantity-quality choice give three eras", EDU),
            (r"was it good? \ heights fell for two generations; \ then the escape", HEIGHT),
            (r"a dial on pre-industrial growth; \ Ehrlich's bomb; \ deep roots and spatial noise", E.ACCENT),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 19, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part nineteen in twelve lines. <bookmark mark='a'/> Malthus argued that population grows "
            "geometrically and food only arithmetically. In Play it, England's income per head left the floor around "
            f"1800, and has multiplied about {p['ratio_1800_2016']:.0f} times since. The model joins diminishing "
            "returns to a population that follows income, and has a stable trap. England's wages obeyed it: one "
            f"percent more people meant about {-e['before']['slope']:.1f} percent lower wages until about 1640. The "
            f"Black Death killed {100 * b['drop']:.0f} percent of the English, and wages rose almost threefold before "
            "falling back. Britain went first, for reasons of prices, ideas and institutions that are still argued "
            "over, and the new national accounts date China's fall behind to around 1700. Growth was slow until "
            "1830, and wages lagged. Deaths fell first, then births. One model, with a scale effect and the choice "
            "between quantity and quality, produces three eras. Heights fell for two generations before the escape "
            "paid. And a dial on growth before the escape, Ehrlich's bomb, and deep roots that may be spatial noise."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=46.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20, width=13.0)
        with self.voiceover(
            "The problems. The Malthusian steady state; the plague's jump and its half-life; England's labour demand "
            "curve; growth rates and doubling times; Engels's pause; the quantity-quality threshold; Kremer's scale "
            "effect; and a starred problem on spatial noise. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Gregory Clark, \emph{A Farewell to Alms} (2007)",
             r"Robert C.\ Allen, \emph{The British Industrial Revolution in Global Perspective} (2009)",
             r"Joel Mokyr, \emph{A Culture of Growth} (2016)",
             r"Oded Galor, \emph{Unified Growth Theory} (2011); \ Kenneth Pomeranz, \emph{The Great Divergence} (2000)"],
            [r"Malthus (1798); \ Ricardo (1817); \ Ashraf and Galor (2011, 2013)",
             r"Broadberry, Campbell, Klein, Overton and van Leeuwen (2015); \ Humphries and Weisdorf (2019)",
             r"Voigtländer and Voth (2013); \ North and Weingast (1989); \ Clark (1996); \ Humphries (2013)",
             r"Kelly, Mokyr and Ó Gráda (2014); \ Broadberry, Guan and Li (2018)",
             r"Crafts and Harley (1992); \ Crafts (2004); \ Allen (2009); \ Voth (2000); \ de Vries (1994)",
             r"Becker and Lewis (1973); \ Kremer (1993); \ Galor and Weil (2000)",
             r"Comin, Easterly and Gong (2010); \ Spolaore and Wacziarg (2009); \ Kelly (2019); \ Ehrlich (1968)"])
        with self.voiceover(
            "The reading: Gregory Clark's A Farewell to Alms, for the Malthusian view at its boldest; Robert Allen's "
            "British Industrial Revolution in Global Perspective, for prices; Joel Mokyr's A Culture of Growth, for "
            "ideas; Oded Galor's Unified Growth Theory, and Kenneth Pomeranz's The Great Divergence. Then the papers, "
            "from Malthus to spatial noise."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1956, r"Robert Solow", r"one equation for what capital can do, \ and what it cannot",
                          color=E.ACCENT, width=10.4, font_size=24)
        nxt = VGroup(label(r"Next: \ Part 20 \ $\cdot$ \ Act V, \ The Long Run", font_size=30, color=GREY_B),
                     label(r"Growth I: \ Capital", font_size=46),
                     label(r"can a country save its way to being rich?", font_size=26, color=E.ACCENT)).arrange(
            DOWN, buff=0.22)
        head = label(r"this part: \ how the escape began; \ next: \ what sustains it", font_size=28,
                     color=GREY_A).to_edge(UP, buff=0.5)
        hc.next_to(head, DOWN, buff=0.45)
        nxt.next_to(hc, DOWN, buff=0.5)
        with self.voiceover(
            "This part asked how the escape began. The next asks what sustains it. <bookmark mark='a'/> In 1956 "
            "Robert Solow wrote down one equation for what saving and capital can do, and what they cannot. "
            "<bookmark mark='b'/> Part twenty: growth, and capital."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(9.5)          # the score's close plays here, after the last line, not under it
        self.clear_scene()
