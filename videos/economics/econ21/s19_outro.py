from __future__ import annotations

from videos.economics.econ21.common import *  # noqa: F403

PROBLEMS = [
    r"Replication: \ with $Y = A K^{\alpha} L^{1-\alpha}$, \ show that doubling $K$ and $L$ doubles $Y$, \ that "
    r"doubling $A$ too quadruples it, \ and that paying $K$ and $L$ their marginal products uses up all of $Y$.",
    r"AK: \ with $Y = AK$ and $\dot K = sY - \delta K$, \ find the growth rate, \ and show that a permanent rise in "
    r"$s$ raises growth for ever.",
    r"Romer: \ derive $L_Y = r/(\alpha\delta)$ from the researcher's arbitrage, \ and the balanced growth rate "
    r"$g = (\alpha\delta L - \rho)/(\alpha + \theta)$.",
    r"The ladder: \ with research $n$, \ arrival rate $\lambda n$ and steps $\gamma$, \ show that expected log "
    r"productivity grows at $\lambda n \ln\gamma$, \ and solve for the market's $n$.",
    r"Semi-endogenous growth: \ with $\dot A = \theta S^{\lambda} A^{\phi}$ and $S$ growing at $n$, \ show that on a "
    r"balanced path $g_A = \lambda n / (1 - \phi)$.",
    r"Misallocation: \ with $\ln \text{TFPR}$ normal with variance $v$, \ independent of $\ln A$, \ show that "
    r"$\ln(Y_{\text{eff}}/Y) = \sigma v / 2$ in the one-factor model.",
    r"Settler mortality: \ with the first stage $-0.61$ and the reduced form $-0.57$, \ compute the 2SLS estimate, "
    r"\ and state the exclusion restriction it needs.",
    r"$\bigstar$ \ Directed technical change: \ with $N_H/N_L \propto (H/L)^{\sigma - 1}$, \ derive the long-run "
    r"response of the skill premium to $H/L$, \ and the condition for it to slope up.",
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
        a = wrapped_label(r"From ideas, \ which unlike capital can be used by everyone at once, \ and so do not run "
                          r"into diminishing returns: \ the labour cost of light fell 45{,}000-fold in two centuries. \ "
                          r"Markets do too little research, \ ideas get harder to find, \ and they spread slowly. \ "
                          r"Across countries the residual is also how well ideas and resources are used, \ which "
                          r"institutions, \ shaped by history, \ geography and culture, \ largely decide.", 11.6, 27,
                          WHITE)
        a.next_to(q, DOWN, buff=0.55)
        l_ = load("light")
        mini = plane([1800, 1995], [np.log10(0.0001), np.log10(10)], x_length=4.2, y_length=1.4)
        logo = log_path(mini, l_["frontier_years"], l_["frontier"], LIGHT, width=4)
        VGroup(mini, logo).next_to(a, DOWN, buff=0.4)
        with self.voiceover(
            "So: where does the growth that capital cannot explain come from? <bookmark mark='a'/> From ideas, "
            "which unlike capital can be used by everyone at once, and so do not run into diminishing returns: the "
            "labour cost of light fell forty-five thousand times in two centuries. Markets do too little research, "
            "ideas get harder to find, and they spread slowly. And across countries, the residual is also how well "
            "ideas and resources are used, which institutions, shaped by history, geography and culture, largely "
            "decide."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo), run_time=1.5)
        self.clear_scene()

    def recap(self):
        l_, r, a, b, p, j = (load(k) for k in ("light", "romer", "ah", "bloom", "plants", "ajr"))
        items = [
            (rf"the price of light: \ about {commas(round(l_['ratio_1800_1992'], -3))} times cheaper, \ 1800 to 1992",
             LIGHT),
            (r"ideas are non-rival: \ increasing returns, \ and room for monopoly", IDEA),
            (r"AK and learning by doing: \ growth without end, \ on a knife edge", OUTPUT),
            (rf"Romer: \ research for profit; \ {pc(r['g'], 0)} a year on the island; \ too little research", RESEARCH),
            (rf"creative destruction: \ too much research for small steps, \ too little for large", WEDGE),
            (rf"harder to find: \ researchers $\times${b['effort_factor']}, \ research productivity $\div${b['productivity_factor']}",
             HOLD),
            (r"diffusion: \ 45 years on average from invention to adoption", OUTPUT),
            (rf"misallocation: \ {pc(p['economies'][p['hi']]['gain'], 0)} of output lost on the island with wide wedges",
             WEDGE),
            (rf"settler mortality: \ 2SLS {j['iv']:.2f} against OLS {j['ols']:.2f}, \ and Albouy's critique", INST),
            (r"borders: \ the Koreas, \ Nogales, \ the mita's 25\%", INST),
            (r"directed technical change: \ the premium rises with supply only if $\sigma > 2$", SKILL),
            (r"patents, \ a dial on research \ (social return 30--58\%), \ and an empty planet", GREY_A),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 21, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part twenty-one in twelve lines. <bookmark mark='a'/> The labour cost of light fell about forty-five "
            "thousand times between 1800 and 1992. Ideas are non-rival, which brings increasing returns and needs "
            "monopoly or public money to pay for them. AK models grow for ever, on a knife edge. Romer's economy "
            "invents for profit and does too little of it. Creative destruction can bring too much research or too "
            "little, depending on the size of the steps. Researchers multiplied twenty-three times while research "
            "productivity fell forty-one times: ideas are getting harder to find. Countries adopt technologies "
            "forty-five years after their invention, on average. Misallocation can cost tens of percent of output. "
            "Settler mortality, as an instrument, says institutions explain most income differences among former "
            "colonies, if it is valid. Borders tell the same story. The direction of invention responds to profit. "
            "And patents, a dial on the return to research, and a planet that may empty."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=46.0)
        del a
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20, width=13.0)
        with self.voiceover(
            "The problems. Replication and Euler's theorem; the AK model; Romer's balanced path; the quality "
            "ladder; semi-endogenous growth; Hsieh and Klenow's formula; settler mortality as an instrument; and a "
            "starred problem on directed technical change. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Charles I.\ Jones and Dietrich Vollrath, \emph{Introduction to Economic Growth} (3rd ed., 2013), \ chs.\ 4--6",
             r"Daron Acemoglu, \emph{Introduction to Modern Economic Growth} (2009), \ chs.\ 13--15",
             r"Philippe Aghion and Peter Howitt, \emph{The Economics of Growth} (2009)",
             r"David Warsh, \emph{Knowledge and the Wealth of Nations} (2006); \ Acemoglu and Robinson, \emph{Why "
             r"Nations Fail} (2012)"],
            [r"Nordhaus (1996); \ Arrow (1962); \ Romer (1986, 1990); \ Lucas (1988); \ Aghion and Howitt (1992)",
             r"Jones (1995, 2022); \ Bloom, Jones, Van Reenen and Webb (2020); \ Comin and Hobijn (2010); \ Basu and "
             r"Weil (1998)",
             r"Hsieh and Klenow (2009); \ Bils, Klenow and Ruane (2021)",
             r"Acemoglu, Johnson and Robinson (2001, 2002); \ Albouy (2012); \ Dell (2010); \ Rodrik et al.\ (2004)",
             r"Alsan (2015); \ Nunn and Wantchekon (2011); \ Acemoglu (2002); \ Katz and Murphy (1992)",
             r"Moser (2005); \ Williams (2013); \ Jones and Williams (1998); \ Bloom, Schankerman and Van Reenen (2013)",
             r"Dechezlepr\^etre et al.\ (2023); \ Bloom, Van Reenen and Williams (2019); \ Aghion, Jones and Jones (2019)"])
        with self.voiceover(
            "The reading: Jones and Vollrath for the first pass; Acemoglu's and Aghion and Howitt's books for the "
            "graduate one; and David Warsh's Knowledge and the Wealth of Nations for the story of how the theory was "
            "built. For institutions, Acemoglu and Robinson's Why Nations Fail. Then the papers, from Nordhaus's "
            "lamps to an empty planet."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1957, r"Milton Friedman", r"people spend out of the income they expect, \ not the income "
                          r"they have this year", color=E.ACCENT, width=10.4, font_size=24)
        nxt = VGroup(label(r"Next: \ Part 22 \ $\cdot$ \ Act V, \ The Long Run", font_size=30, color=GREY_B),
                     label(r"Consumption and Saving", font_size=46),
                     label(r"how do households decide how much to spend today?", font_size=26,
                           color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"this part: \ where growth comes from; \ next: \ how households share it across their lives",
                     font_size=26, color=GREY_A).to_edge(UP, buff=0.5)
        hc.next_to(head, DOWN, buff=0.45)
        nxt.next_to(hc, DOWN, buff=0.5)
        with self.voiceover(
            "This part asked where growth comes from. The next asks how households spread what they earn across "
            "their lives. <bookmark mark='a'/> In 1957 Milton Friedman argued that people spend out of the income "
            "they expect, not the income they happen to have this year. <bookmark mark='b'/> Part twenty-two: "
            "consumption and saving."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(9.5)          # the score's close plays here, after the last line, not under it
        self.clear_scene()
