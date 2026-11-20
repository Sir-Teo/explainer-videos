from __future__ import annotations

from videos.economics.econ26.common import *  # noqa: F403

PROBLEMS = [
    r"Diamond--Dybvig: \ with $u(c) = c^{1-\gamma}/(1-\gamma)$, \ derive $c_1 = 1/(t + (1-t)R^{1/\gamma - 1})$; \ "
    r"show $c_1 > 1$ exactly when $\gamma > 1$, \ and compute $c_1, c_2$ for $\gamma = 2$, $R = 1.5$, $t = 1/4$.",
    r"The run threshold: \ if a share $f$ withdraws $c_1$, \ stayers get $R(1 - fc_1)/(1-f)$. \ Show that waiting "
    r"stops paying once $f > (R - c_1)/(c_1(R-1))$.",
    r"Sequential service: \ if everyone runs and the bank can raise 1 per depositor, \ what share is paid? \ Who "
    r"gets nothing?",
    r"Bagehot: \ reserves 10, \ loans 90, \ deposits 90, \ equity 10; \ 30 is withdrawn. \ Find equity after a fire "
    r"sale at 60\% and after borrowing at 5\%.",
    r"Merton: \ with $r = 0$, \ show that equity $=$ put $+ V - D$, \ so a flat premium hands the put to the "
    r"owners.",
    r"Repo: \ a dealer with equity 4 holds 100 of bonds at a 4\% haircut. \ The haircut rises to 20\%. \ How much "
    r"must it sell?",
    r"Global games: \ using the Laplacian belief at the cutoff, \ show $\theta^* = c/R$; \ what happens to failures "
    r"when $c$ rises?",
    r"$\bigstar$ \ Delegated monitoring: \ loans repay $R$ with probability $p$; \ show the bank's failure "
    r"probability goes to 0 as $n \to \infty$ when $pR > D$, \ and compute it for $n = 10$, $p = 0.9$, $R = 1.3$.",
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
        a = wrapped_label(r"Banks are fragile because they do something valuable: \ they turn long, \ illiquid loans "
                          r"into deposits anyone can take out at once, \ and so a bank that is sound if everyone stays "
                          r"can fail if enough people fear it will. \ Insurance, \ a lender of last resort and capital "
                          r"make them much safer, \ at the price of watching them closely; \ but wherever short "
                          r"funding meets long assets, \ inside banks or outside them, \ the run can come back.",
                          11.6, 27, WHITE)
        a.next_to(q, DOWN, buff=0.55)
        f = load("film")
        mini = plane([2022, 2025], [92, 106], x_length=4.2, y_length=1.3)
        sm = 100 * np.array(f["small"]) / f["small"][0]
        lg = 100 * np.array(f["large"]) / f["large"][0]
        logo = VGroup(path(mini, f["t"], sm, DEPOSIT, width=3, smooth=False),
                      path(mini, f["t"], lg, BOND, width=3, smooth=False))
        logo.next_to(a, DOWN, buff=0.4)
        with self.voiceover(
            "So: why are banks fragile, and can they be made safe? <bookmark mark='a'/> Banks are fragile because "
            "they do something valuable. They turn long, illiquid loans into deposits that anyone can take out at "
            "once, and so a bank that is sound if everyone stays can fail if enough people fear it will. Deposit "
            "insurance, a lender of last resort and capital make them much safer, at the price of watching them "
            "closely. But wherever short funding meets long assets, inside the banks or outside them, the run can "
            "come back."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo), run_time=1.5)
        self.clear_scene()

    def recap(self):
        r, L, s, S, g, M, b, c = (load(x) for x in ("run", "llr", "suspensions", "sheet", "gg", "monitor", "betas",
                                                     "crisis"))
        d = load("dd")
        items = [
            (r"Silicon Valley Bank: \ \$42 billion in a day", RUN),
            (r"a bank: \ liquid deposits, \ illiquid loans", DEPOSIT),
            (rf"Diamond--Dybvig: \ {d['c1']:.2f} early, \ {d['c2']:.2f} late, \ better than going it alone", STAY),
            (rf"two equilibria: \ waiting stops paying once {100 * d['threshold']:.0f}\% withdraw; \ "
             rf"{100 * r['share_served']:.0f}\% are served", RUN),
            (rf"suspension and insurance: \ {commas(s['y1933'])} suspensions in 1933, \ {s['y1934']} in 1934", CB),
            (rf"Bagehot: \ a fire sale leaves equity {L['equity_fire']:.1f}; \ a lender, \ {L['equity_llr']:.0f}",
             CB),
            (r"moral hazard: \ insurance is a put; \ the savings and loans", EQUITY),
            (rf"capital and rate risk: \ a {100 * S['risk_based']:.0f}\% ratio, \ and bonds that lose "
             rf"{-100 * S['change']:.0f}\%", BOND),
            (r"runs without depositors: \ repo haircuts and money funds", BOND),
            (rf"global games: \ one equilibrium, \ failure below $\theta^* = {g['base']['theta_star']:.1f}$", STAY),
            (r"the data: \ mostly fundamentals, \ until 1933; \ uninsured deposits in 2023", RUN),
            (rf"monitors; \ two dials (betas {b['beta_savings']:.2f} to {b['beta_cd']:.2f}; \ crises cost "
             r"6--10\%); \ stress tests; \ digital runs", LOAN),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 26, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        del M, c
        with self.voiceover(
            "Part twenty-six in twelve lines. <bookmark mark='a'/> Silicon Valley Bank lost forty-two billion "
            "dollars in a day. A bank turns illiquid loans into liquid deposits, and Diamond and Dybvig showed that "
            "this insures depositors against needing their money early. The same contract has a second "
            "equilibrium, the run, in which first come is first served. Suspension and deposit insurance remove "
            "it, and after 1934 American bank failures almost stopped. Bagehot's lender keeps a fire sale from "
            "turning illiquidity into insolvency. Insurance is a put that rewards risk, so banks must hold "
            "capital, and capital rules can miss the risk in safe bonds. Runs moved to repo and money funds. "
            "Global games turn two equilibria into one, and make runs predictable from fundamentals; the "
            "Depression's failures were mostly fundamentals, and 2023's run was the uninsured's. Banks exist to "
            "monitor, and their failures destroy what they knew. Then two dials, the stress tests, and the digital "
            "runs."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=46.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20, width=13.0)
        with self.voiceover(
            "The problems. Diamond and Dybvig's contract; the share of withdrawals at which waiting stops paying; "
            "who is served in a run; Bagehot's arithmetic; deposit insurance as a put; a run on repo; the global "
            "game's threshold; and a starred problem on why diversified banks can promise fixed payments. Full "
            "solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Xavier Freixas and Jean-Charles Rochet, \emph{Microeconomics of Banking} (2nd ed., 2008), \ "
             r"chs.\ 2, 7, 9",
             r"Gary Gorton, \emph{Misunderstanding Financial Crises} (2012)",
             r"Walter Bagehot, \emph{Lombard Street} (1873)",
             r"Anat Admati and Martin Hellwig, \emph{The Bankers' New Clothes} (2013)"],
            [r"Diamond and Dybvig (1983); \ Diamond (1984); \ Bernanke (1983); \ Merton (1977)",
             r"Gorton and Metrick (2012); \ Morris and Shin (1998); \ Goldstein and Pauzner (2005)",
             r"Friedman and Schwartz (1963); \ Calomiris and Mason (2003); \ Curry and Shibut (2000)",
             r"Jiang, Matvos, Piskorski and Seru (2024); \ Drechsler, Savov and Schnabl (2017, 2021)",
             r"Reinhart and Rogoff (2009); \ Cerra and Saxena (2008); \ Romer and Romer (2017); \ Cookson et al.\ "
             r"(2023)"])
        with self.voiceover(
            "The reading: Freixas and Rochet's Microeconomics of Banking, the graduate text this part follows; "
            "Gary Gorton's Misunderstanding Financial Crises; Bagehot's Lombard Street, which is still worth "
            "reading; and Admati and Hellwig's case for more capital. Then the papers, from Diamond and Dybvig to "
            "the digital runs of 2023."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1977, r"the Capitol Hill babysitting co-op", r"young couples trade babysitting for coupons; "
                          r"\ everyone wants to save coupons, \ so nobody goes out, \ and nobody can earn them",
                          color=E.ACCENT, width=10.4, font_size=24)
        nxt = VGroup(label(r"Next: \ Part 27 \ $\cdot$ \ Act VI, \ Money and the Cycle", font_size=30, color=GREY_B),
                     label(r"The Keynesian Revolution", font_size=46),
                     label(r"how can a whole economy be short of buyers?", font_size=26,
                           color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"this part: \ the fragile institutions that create money; \ next: \ when nobody spends it",
                     font_size=26, color=GREY_A).to_edge(UP, buff=0.5)
        VGroup(hc, nxt).arrange(DOWN, buff=0.6).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "This part was about the fragile institutions that create most of our money. The next is about what "
            "happens when nobody spends it. <bookmark mark='a'/> On Capitol Hill, a babysitting co-operative of "
            "young couples paid for sitting with coupons. Everyone wanted to save some coupons for later, so "
            "everyone stayed in and offered to sit, nobody went out, and nobody could earn any. Joan and Richard "
            "Sweeney wrote it up in 1977 as a recession in miniature. <bookmark mark='b'/> Part twenty-seven: the "
            "Keynesian revolution. How can a whole economy be short of buyers?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(9.5)
        self.clear_scene()
