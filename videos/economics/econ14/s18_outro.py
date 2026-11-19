from __future__ import annotations

from videos.economics.econ14.common import *  # noqa: F403

PROBLEMS = [
    r"Teams: \ $n$ members share output $a\sum e_i$ equally, \ effort costs $c e^2/2$; \ show $e = a/(nc)$ and that "
    r"a share $(n-1)^2/n^2$ of the surplus is lost; \ check 89\% at $n = 18$.",
    r"Holmström and Milgrom: \ derive $\beta^* = 1/(1 + r c \sigma^2)$; \ check $2/3$ in the Play it, \ and profits "
    r"of 2.50 at shares of $1/3$ and 1.",
    r"Two outcomes: \ with log utility, \ derive the cheapest wages that buy hard work; \ check 11.59 and 5.47, \ and "
    r"the risk premium of 0.39.",
    r"Informativeness: \ show that paying on Friday's harvest less the weather cuts the variance from 25 to 9 \ and "
    r"raises the share to 0.85.",
    r"Multitasking: \ solve the two first-order conditions; \ show the unmeasured task is dropped once the bonus "
    r"reaches 1.",
    r"Tournaments: \ show effort is the prize gap times $1/(2\sigma\sqrt{\pi})$, \ over $c$; \ what does doubling "
    r"the noise do?",
    r"Shapiro and Stiglitz: \ show the no-shirking wage rises without bound as unemployment falls; \ check 14\% "
    r"unemployed.",
    r"$\bigstar$ \ Relational contracts: \ show the most effort a promise can sustain is $\min(1/c,\ 2\delta/c)$, \ "
    r"first best once $\delta \ge 1/2$.",
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
        a = wrapped_label(r"Pay on what you can see, \ in proportion to what it tells you about effort, \ and only as "
                          r"strongly as the agent's dislike of risk \ and the measure's narrowness allow. \ Where the "
                          r"work is one person's own and easy to count, \ a share of the output raises it by a fifth "
                          r"to a half. \ Where the measure misses much of the job, \ pay weakly, \ design the job, \ "
                          r"and lean on ownership, \ promotions, \ careers and relationships; \ and beware of "
                          r"replacing a norm with a price.", 11.6, 29, WHITE)
        a.next_to(q, DOWN, buff=0.55)
        logo = pair(height=0.9).next_to(a, DOWN, buff=0.45)
        with self.voiceover(
            "So: how do you get someone to work for you when you can't see what they do? <bookmark mark='a'/> Pay "
            "on what you can see, in proportion to what it tells you about their effort, and only as strongly as "
            "their dislike of risk and the narrowness of the measure allow. Where the work is one person's own and "
            "easy to count, a share of the output raises it by a fifth to a half. Where the measure misses much of "
            "the job, pay weakly, design the job, and lean on ownership, promotions, careers and relationships. And "
            "beware of replacing a norm with a price."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(FadeIn(logo, shift=UP * 0.2))
        self.clear_scene()

    def recap(self):
        p, t, d, s = (load(x) for x in ("playit", "team", "discrete", "shirking"))
        cr = tables.CROWDING.data
        items = [
            (r"Xiaogang, \ 1978: \ eighteen thumbprints, \ and each family keeps what it adds", CHINA),
            (rf"your contract: \ two-thirds of the harvest, \ {p['best_profit']:.2f} a day against "
             rf"{p['fb_profit']:.0f}", PAY),
            (rf"teams: \ an eighteenth of the effort, \ {100 * t['n18']['lost']:.0f}\% of the surplus lost", TEAM),
            (rf"the agency problem: \ {d['w_high']:.2f} after a good harvest, \ {d['w_low']:.2f} after a poor one: \ "
             r"an inference", SIGNAL),
            (r"$\beta^* = 1/(1 + r c \sigma^2)$; \ and Prendergast's puzzle", E.ACCENT),
            (r"informativeness: \ filter out the weather; \ executives paid for luck", SIGNAL),
            (r"Safelite: \ 44\%, \ half of it sorting; \ tree planters 20\%; \ fruit pickers 50\%", EFFORT),
            (r"multitasking: \ teaching to the test; \ cheating in 4 to 5\% of classrooms", RISK),
            (r"tournaments: \ the prize gap; \ golf; \ funds that gamble when behind", PAY),
            (r"careers fade and bonuses take over; \ the ratchet: \ a tenth of the effort", SIGNAL),
            (rf"efficiency wages: \ Ford, \ and {100 * s['u_eq']:.0f}\% unemployed as discipline; \ sharecropping and "
             r"China's reform", CHINA),
            (rf"backfire: \ Haifa, \ and the Swiss repository, \ {100 * cr['accept_unpaid']:.0f}\% to "
             rf"{100 * cr['accept_paid']:.0f}\%; \ relational contracts; \ machines", E.ACCENT),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 14, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part fourteen in twelve lines. <bookmark mark='a'/> In 1978 eighteen farmers in Xiaogang put their "
            "thumbprints on a contract that let each family keep what it added. Your contract for Friday was best at "
            "two-thirds of the harvest, and still made a third less than seeing effort would. A team of eighteen "
            "works an eighteenth as hard as each would alone. In the agency problem, pay after a poor harvest is "
            "lower even when Crusoe knows Friday worked: it is an inference, not a reward. Holmström and Milgrom's "
            "formula gives the best share, and Prendergast's puzzle is that riskier jobs often have stronger "
            "incentives. Pay should filter out the weather, yet executives are paid for luck. At Safelite, piece "
            "rates raised output by forty-four percent, half of it from who took the job. Paying for test scores "
            "brought teaching to the test, and cheating. Tournaments run on the gap between prizes, in golf and in "
            "mutual funds. Career concerns fade, and explicit bonuses should take over; a ratchet cuts effort to a "
            "tenth. Efficiency wages explain Ford's five dollars and some unemployment, and sharecropping is "
            "insurance paid for with effort, while China's reform shows the other end. And incentives can backfire, "
            "in Haifa and in Switzerland; relational contracts hold what courts can't; and machines game their "
            "rewards, as people do."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=44.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20, width=13.0)
        with self.voiceover(
            "The problems. The team's lost surplus; the best share; the cheapest wages for hard work; filtering out "
            "the weather; the dropped task; the tournament's effort; the no-shirking wage; and a starred problem on "
            "relational contracts. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Patrick Bolton and Mathias Dewatripont, \emph{Contract Theory} (2005), chs.\ 4, 6, 8, 11",
             r"Jean-Jacques Laffont and David Martimort, \emph{The Theory of Incentives} (2002); \ Salani\'e, "
             r"\emph{The Economics of Contracts}",
             r"Paul Milgrom and John Roberts, \emph{Economics, Organization and Management} (1992)",
             r"Robert Gibbons and John Roberts, eds., \emph{The Handbook of Organizational Economics} (2013)"],
            [r"Ross (1973); \ Holmström (1979, 1982); \ Mirrlees (1975); \ Grossman and Hart (1983)",
             r"Holmström and Milgrom (1987, 1991); \ Lazear and Rosen (1981); \ Rosen (1986); \ Weitzman (1980)",
             r"Shapiro and Stiglitz (1984); \ Akerlof (1982); \ Raff and Summers (1987); \ Stiglitz (1974)",
             r"Lazear (2000); \ Shearer (2004); \ Bandiera, Barankay and Rasul (2005); \ Jacob and Levitt (2003)",
             r"Lin (1992); \ Banerjee, Gertler and Ghatak (2002); \ Gneezy and Rustichini (2000); \ Frey and "
             r"Oberholzer-Gee (1997)",
             r"Baker, Gibbons and Murphy (2002); \ Levin (2003); \ Hadfield-Menell and Hadfield (2019); \ Gao, "
             r"Schulman and Hilton (2023)"])
        with self.voiceover(
            "The reading: Bolton and Dewatripont's Contract Theory; Laffont and Martimort's Theory of Incentives; "
            "Milgrom and Roberts on organization and management; and the Handbook of Organizational Economics. Then "
            "the papers, from Ross and Mirrlees to the reward models of 2023."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1973, r"Washington State's orchards", r"Steven Cheung finds beekeepers renting their hives "
                          r"to fruit growers, \\ at prices that move with the nectar", color=E.ACCENT, width=10.4,
                          font_size=24)
        nxt = VGroup(label(r"Next: \ Part 15 \ $\cdot$ \ Act IV, \ Failure and Design", font_size=30, color=GREY_B),
                     label(r"Spillovers", font_size=46),
                     label(r"what happens when my choice lands on you, \ and nobody pays?", font_size=26,
                           color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"this part: \ two people and a contract; \ next: \ costs that fall on third parties",
                     font_size=28, color=GREY_A).to_edge(UP, buff=0.5)
        hc.next_to(head, DOWN, buff=0.45)
        nxt.next_to(hc, DOWN, buff=0.5)
        with self.voiceover(
            "This part was about two people and the contract between them. The next is about everyone else: the "
            "costs and benefits that fall on people outside the deal. <bookmark mark='a'/> Economists long used the "
            "orchard and the beekeeper as the example of a benefit no market could price. In 1973 Steven Cheung went "
            "to Washington State and found beekeepers renting their hives to fruit growers, at prices that moved "
            "with the nectar. <bookmark mark='b'/> Part fifteen: spillovers."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(9.5)          # the score's close plays here, after the last line, not under it
        self.clear_scene()
