from __future__ import annotations

from videos.economics.econ20.common import *  # noqa: F403

PROBLEMS = [
    r"The steady state: \ with $y = k^{\alpha}$ and $\dot k = s k^{\alpha} - (n+g+\delta)k$, \ find $k^*$, $y^*$ "
    r"and $c^*$, \ and show that capital is $s/(n+g+\delta)$ years of output.",
    r"The golden rule: \ show that steady-state consumption is largest when $f'(k) = n+g+\delta$, \ that this "
    r"means $s = \alpha$ for Cobb-Douglas, \ and find the island's consumption at 15\% and at a third.",
    r"Levels, not growth: \ show that doubling $s$ multiplies $y^*$ by $2^{\alpha/(1-\alpha)}$, \ and that output "
    r"per worker grows at $g$ in both steady states.",
    r"The speed: \ linearize the Solow equation in $\ln k$, \ find $\lambda = (1-\alpha)(n+g+\delta)$, \ and the "
    r"half-lives for $\alpha = 1/3$ and $\alpha = 3/4$ when $n+g+\delta = 8\%$.",
    r"Growth accounting: \ output grows 3.1\%, capital 2.8\%, hours 1.2\%, schooling 0.5\% a year, \ with "
    r"$\alpha = 0.38$: \ find the residual and its share of growth per hour.",
    r"Development accounting: \ derive $y = (K/Y)^{\alpha/(1-\alpha)}\,h\,A^{1/(1-\alpha)}$, \ and explain why "
    r"capital intensity is measured by $K/Y$ rather than $K/L$.",
    r"Lucas: \ with $y = A k^{\alpha}$, \ the same $A$ and $\alpha = 0.4$, \ show that a fifteenfold income gap "
    r"implies returns 58 times as high, \ and about 5 when workers differ fivefold in skill.",
    r"$\bigstar$ \ Ramsey: \ derive the Euler equation from the Hamiltonian, \ the modified golden rule, \ and show "
    r"that an optimizing economy never saves beyond the golden rule.",
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
        a = wrapped_label(r"Richer, \ yes: \ saving raises the level of income, \ and East Asia's saving and "
                          r"schooling were real achievements. \ Growing faster for ever, \ no: \ diminishing returns "
                          r"bring growth back to the rate of technology, \ as the Soviet Union and, \ more gently, \ "
                          r"South Korea found. \ Across countries, \ capital and schooling explain less than half of "
                          r"the gap between rich and poor; \ the rest is productivity, \ the residual that this "
                          r"model leaves out.", 11.6, 27, WHITE)
        a.next_to(q, DOWN, buff=0.55)
        h = load("hook")
        mini = plane([1911, 2022], [np.log10(600), np.log10(60000)], x_length=4.2, y_length=1.4)
        logo = VGroup(log_path(mini, h["KOR"]["years"], h["KOR"]["gdppc"], SOUTH, width=4),
                      log_path(mini, h["PRK"]["years"][h["PRK"]["years"].index(1990):],
                               h["PRK"]["gdppc"][h["PRK"]["years"].index(1990):], NORTH, width=4))
        VGroup(mini, logo).next_to(a, DOWN, buff=0.4)
        with self.voiceover(
            "So: can a country save its way to being rich? <bookmark mark='a'/> Richer, yes. Saving raises the level "
            "of income, and East Asia's saving and schooling were real achievements. Growing faster for ever, no. "
            "Diminishing returns bring growth back to the rate of technology, as the Soviet Union found, and, more "
            "gently, South Korea. Across countries, capital and schooling explain less than half of the gap between "
            "rich and poor. The rest is productivity: the residual this model leaves out."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo), run_time=1.5)
        self.clear_scene()

    def recap(self):
        k, pl, co, ac, d = load("kaldor"), load("playit"), load("convergence"), load("accounting"), load("development")
        us = ac["countries"]["USA"]
        cc = co["1960-2019"]["conditional"]
        items = [
            (r"the two Koreas: \ one people, \ two systems, \ a ratio of 26 to 1", SOUTH),
            (rf"Kaldor's facts: \ steady growth of {pc(k['g_ypw'])} a year, \ steady ratios, \ a labour share now "
             r"slipping", OUTPUT),
            (r"Harrod--Domar: \ a knife edge, \ and the financing gap that Easterly tested", SAVE),
            (r"Solow: \ saving sets the level; \ only technology sets the long-run growth rate", CAPITAL),
            (rf"Play it: \ the golden rule, \ save capital's share; \ {pc(pl['jump']['level_gain'], 0)} more income "
             r"from doubling saving", CONS),
            (r"the speed: \ 5\% a year in the textbook, \ 1--2\% in the data", BREAK),
            (rf"convergence: \ conditional, \ {pc(cc['lambda'])} a year; \ absolute, \ none until 2000", E.ACCENT),
            (rf"growth accounting: \ the residual, \ {100 * us['tfp_share_per_hour']:.0f}\% of US growth per hour",
             TFP),
            (r"East Asia: \ perspiration, \ with an argument about Singapore's data", COUNTRY["SGP"][1]),
            (rf"development accounting: \ the factors explain {d['share_factors']:.2f}--{d['success']:.2f} of "
             r"the variance", HUMAN),
            (r"Lucas: \ 58 times the return, \ predicted; \ about 1.5, \ measured", RATE),
            (r"Ramsey, \ China, \ two dials, \ potential output, \ and convergence at last", GREY_A),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 20, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part twenty in twelve lines. <bookmark mark='a'/> The two Koreas: one people, two systems, and a ratio "
            "of twenty-six to one. Kaldor's facts still hold, except labour's share. Harrod and Domar's model stood "
            "on a knife edge, and its financing gap failed Easterly's test. Solow's model says saving sets the level "
            "of income, and only technology sets its long-run growth. The golden rule is to save capital's share, and "
            f"doubling the island's saving raised its income by about {100 * pl['jump']['level_gain']:.0f} percent, "
            "for good. The textbook's speed of convergence is five percent a year; the data say one or two. "
            "Countries converge once saving and schooling are held fixed, and until about 2000 not otherwise. The "
            f"residual is about {100 * us['tfp_share_per_hour']:.0f} percent of America's growth per hour. East "
            "Asia grew mostly by accumulation. Capital and schooling explain well under half of income differences. "
            "Capital should earn fifty-eight times as much in India, and earns about one and a half. And Ramsey's "
            "choice of saving, China, two dials, potential output, and convergence at last."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=46.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20, width=13.0)
        with self.voiceover(
            "The problems. The Solow steady state; the golden rule; levels, not growth; the speed of convergence; "
            "growth accounting; development accounting; Lucas's calculation; and a starred problem on Ramsey's "
            "model. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Charles I.\ Jones and Dietrich Vollrath, \emph{Introduction to Economic Growth} (3rd ed., 2013)",
             r"Daron Acemoglu, \emph{Introduction to Modern Economic Growth} (2009), \ chs.\ 2--3 and 8",
             r"David Romer, \emph{Advanced Macroeconomics} (5th ed., 2019), \ chs.\ 1--2",
             r"William Easterly, \emph{The Elusive Quest for Growth} (2001)"],
            [r"Harrod (1939); \ Domar (1946); \ Solow (1956, 1957); \ Swan (1956); \ Kaldor (1961); \ Phelps (1961)",
             r"Ramsey (1928); \ Cass (1965); \ Koopmans (1965); \ Abel, Mankiw, Summers and Zeckhauser (1989)",
             r"Barro (1991); \ Mankiw, Romer and Weil (1992); \ Islam (1995); \ Quah (1996); \ Pritchett (1997)",
             r"Krugman (1994); \ Young (1995); \ Hsieh (2002); \ Hall and Jones (1999); \ Caselli (2005)",
             r"Lucas (1990); \ Song, Storesletten and Zilibotti (2011); \ Easterly (1999); \ Blanchard (2019)",
             r"Fernald (2015); \ Syverson (2017); \ Kremer, Willis and You (2022); \ Acemoglu and Molina (2022)",
             r"Feenstra, Inklaar and Timmer, \ the Penn World Table (2015; \ version 11.0, \ 2025)"])
        with self.voiceover(
            "The reading: Charles Jones and Dietrich Vollrath's Introduction to Economic Growth, the clearest first "
            "book; Daron Acemoglu's Introduction to Modern Economic Growth and David Romer's Advanced "
            "Macroeconomics, for the graduate versions; and William Easterly's Elusive Quest for Growth, for what "
            "went wrong in practice. Then the papers, from Harrod to the frontier."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1990, r"Paul Romer", r"an idea, \ unlike a lamp, \ can be used by everyone at once",
                          color=E.ACCENT, width=10.4, font_size=24)
        nxt = VGroup(label(r"Next: \ Part 21 \ $\cdot$ \ Act V, \ The Long Run", font_size=30, color=GREY_B),
                     label(r"Growth II: \ Ideas and Institutions", font_size=46),
                     label(r"where does the growth that capital cannot explain come from?", font_size=26,
                           color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"this part: \ what capital can do; \ next: \ the residual", font_size=28,
                     color=GREY_A).to_edge(UP, buff=0.5)
        hc.next_to(head, DOWN, buff=0.45)
        nxt.next_to(hc, DOWN, buff=0.5)
        with self.voiceover(
            "This part measured what capital can do, and found a residual it cannot explain. The next part is about "
            "the residual. <bookmark mark='a'/> In 1990 Paul Romer built a theory of growth on one property of "
            "ideas: unlike a lamp or a boat, an idea can be used by everyone at once. <bookmark mark='b'/> Part "
            "twenty-one: growth, part two. Ideas and institutions."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(9.5)          # the score's close plays here, after the last line, not under it
        self.clear_scene()
