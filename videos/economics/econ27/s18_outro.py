from __future__ import annotations

from videos.economics.econ27.common import *  # noqa: F403

PROBLEMS = [
    r"The cross: \ with $C = a + b(Y - T)$, \ derive equilibrium income and the multipliers of $G$ and of $T$; \ "
    r"show that a rise in $G$ paid by an equal rise in $T$ raises $Y$ one for one.",
    r"Kahn's series: \ sum $\Delta G (1 + b + b^2 + \cdots)$; \ after how many rounds is 90\% of the effect felt "
    r"with $b = 0.6$?",
    r"Thrift: \ with $I = I_0 + hY$, \ show that a fall in $a$ lowers saving when $h > 0$.",
    r"IS--LM: \ solve for $Y$ and $i$; \ find the fiscal multiplier $dY/dG$ and show it falls as $d$ rises and as "
    r"$h$ falls.",
    r"The trap: \ show that when $i = 0$ binds, \ $dY/dM = 0$ and $dY/dG = 1/(1-b)$; \ what do expectations of "
    r"inflation do?",
    r"Phillips's machine: \ with taxes at rate $\tau$, \ show the multiplier is $1/(1 - b(1 - \tau))$; \ how fast "
    r"does the gap close?",
    r"AS--AD: \ a money shock and a cost shock; \ sign the effects on $Y$ and $P$, \ short run and long run.",
    r"$\bigstar$ \ The co-op: \ with $N$ couples each wanting a reserve $m^*$, \ explain why evenings fall when "
    r"$M/N < m^*$ and when $M/N \gg m^*$; \ what would a price of evenings in coupons do?",
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
        a = wrapped_label(r"When people want to hold more money, \ or spend less, \ than the economy's income "
                          r"allows, \ output, \ not prices, \ does most of the adjusting, \ because wages and prices "
                          r"move slowly. \ Spending sets output, \ the multiplier spreads every change, \ and saving "
                          r"more can mean saving less. \ More money cures it unless interest rates are at zero; \ "
                          r"then the government's spending must, \ or a promise of easy money later. \ In the long "
                          r"run prices adjust, \ but the long run can be long.", 11.6, 26, WHITE)
        a.next_to(q, DOWN, buff=0.55)
        c = load("coop_curve")
        mini = plane([0, 24], [0, 0.3], x_length=4.2, y_length=1.3)
        logo = VGroup(path(mini, c["coupons"], c["evenings"], OUTPUT, width=3),
                      path(mini, c["coupons"], c["goers"], SPEND, width=2),
                      path(mini, c["coupons"], c["sitters"], SAVE, width=2))
        logo.next_to(a, DOWN, buff=0.4)
        with self.voiceover(
            "So: how can a whole economy be short of buyers? <bookmark mark='a'/> When people want to hold more "
            "money, or spend less, than the economy's income allows, output does most of the adjusting, not "
            "prices, because wages and prices move slowly. Spending sets output, the multiplier spreads every "
            "change, and saving more can mean saving less. More money cures it, unless interest rates are already "
            "at zero; then the government's own spending must do it, or a promise of easy money later. In the "
            "long run prices adjust. But the long run can be long."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo), run_time=1.5)
        self.clear_scene()

    def recap(self):
        co, d, cr, th, L, M, W, A, o, s = (load(x) for x in ("coop_path", "depression", "cross", "thrift", "islm",
                                                            "moniac", "wages", "asad", "okun", "spells"))
        items = [
            (rf"the co-op: \ {co['before']:.2f} evenings a week, \ then {co['after']:.2f} once coupons are printed",
             COUPON),
            (rf"1929--33: \ output $-${d['gnp_fall']:.0f}\%, \ prices $-${d['price_fall']:.0f}\%; \ Say's law fails",
             PRICE),
            (r"Play it: \ hoarding is wise for you and ruinous for all", SAVE),
            (r"the co-op as a model: \ output set by demand, \ or by capacity", OUTPUT),
            (rf"effective demand; \ the multiplier $1/(1-b) = {cr['base']['multiplier']:.1f}$, \ Kahn's series",
             SPEND),
            (rf"the paradox of thrift: \ saving {th['induced']['S0']:.0f} $\to$ {th['induced']['S1']:.0f}", SAVE),
            (rf"IS--LM: \ the fiscal multiplier {L['fiscal_mult']:.2f} with crowding out", RATE),
            (rf"the trap: \ money does nothing, \ spending {L['trap_fiscal_mult']:.1f}; \ Japan; \ Krugman", GOV),
            (rf"Phillips's machine: \ a multiplier of {M['multiplier']:.2f}, \ in water", WATER),
            (rf"sticky wages: \ Bewley; \ {100 * W['share_zero']:.0f}\% at exactly zero; \ AS--AD and the "
             r"synthesis", RATE),
            (r"gold, \ money (Romer), \ then war; \ Hayek, \ Friedman, \ Lucas; \ Keynes's peace, \ partly right",
             COUPON),
            (rf"Okun's coefficient {o['beta']:.2f}; \ expansions {s['exp_mean_post']:.0f} months, \ recessions "
             rf"{s['rec_mean_post']:.0f}; \ Keynesian supply shocks", OUTPUT),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 27, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        del A
        with self.voiceover(
            "Part twenty-seven in twelve lines. <bookmark mark='a'/> A babysitting co-op fell into recession for "
            "want of coupons, and recovered when more were printed. America's output and prices both fell by about "
            "a quarter after 1929, and Say's law, which said that could not last, failed. Hoarding is wise for each "
            "and ruinous for all. Output can be set by demand rather than capacity. Keynes's effective demand and "
            "Kahn's multiplier spread every change in spending; trying to save more can mean saving less. Hicks's I "
            "S L M put goods and money together, with crowding out. At zero interest, money does nothing and "
            "government spending does a great deal. Phillips built it in water. Wages do not fall, because of "
            "morale, and aggregate demand and supply join Keynes's short run to the classics' long run. Gold and "
            "money ended the Depression, and the war finished the job. The critics each won something. And two "
            "dials, the forecaster's facts, and supply shocks that cut demand."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=46.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20, width=13.0)
        with self.voiceover(
            "The problems. The cross and its multipliers, including the balanced-budget multiplier; Kahn's series "
            "round by round; the paradox of thrift; I S L M solved; the trap; Phillips's machine with taxes; "
            "shocks in aggregate demand and supply; and a starred problem on the co-op. Full solutions are in the "
            "part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"John Maynard Keynes, \emph{The General Theory of Employment, Interest and Money} (1936)",
             r"Olivier Blanchard, \emph{Macroeconomics} (8th ed., 2021), \ chs.\ 3--9",
             r"Barry Eichengreen, \emph{Golden Fetters} (1992)",
             r"Robert Skidelsky, \emph{John Maynard Keynes} (three volumes, 1983--2000)"],
            [r"Say (1803); \ Keynes (1919, 1923, 1936); \ Kahn (1931); \ Hicks (1937); \ Fisher (1933); \ Hayek "
             r"(1931)",
             r"Sweeney and Sweeney (1977); \ Krugman (1998); \ Okun (1962); \ Samuelson (1955)",
             r"Bewley (1999); \ Card and Hyslop (1997); \ Dickens et al.\ (2007); \ Friedman and Schwartz (1963)",
             r"Eichengreen and Sachs (1985); \ Romer (1992); \ Lucas and Sargent (1979); \ Mantoux (1946)",
             r"Ball, \ Leigh and Loungani (2017); \ Guerrieri, \ Lorenzoni, \ Straub and Werning (2022)"])
        with self.voiceover(
            "The reading: Keynes's General Theory itself, hard going but worth it; Blanchard's Macroeconomics, "
            "whose early chapters this part follows; Eichengreen's Golden Fetters on gold and the Depression; and "
            "Skidelsky's life of Keynes. Then the papers, from Say to the economics of the pandemic."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1967, r"Milton Friedman's address", r"he tells the American Economic Association that the "
                          r"trade-off between inflation and unemployment will vanish once people come to expect the "
                          r"inflation", color=E.ACCENT, width=10.4, font_size=24)
        nxt = VGroup(label(r"Next: \ Part 28 \ $\cdot$ \ Act VI, \ Money and the Cycle", font_size=30, color=GREY_B),
                     label(r"Inflation and Expectations", font_size=46),
                     label(r"can a country buy lower unemployment with higher inflation?", font_size=26,
                           color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"this part: \ when spending falls short; \ next: \ when prices start to run", font_size=26,
                     color=GREY_A).to_edge(UP, buff=0.5)
        VGroup(hc, nxt).arrange(DOWN, buff=0.6).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "This part was about economies short of buyers, with prices that barely move. The next is about prices "
            "that start to run. <bookmark mark='a'/> In December 1967, Milton Friedman told the American Economic "
            "Association that the trade-off its members were steering by, a little more inflation for a little "
            "less unemployment, would vanish as soon as people came to expect the inflation. Within a decade, "
            "America had more of both. <bookmark mark='b'/> Part twenty-eight: inflation and expectations. Can a "
            "country buy lower unemployment with higher inflation?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(9.5)
        self.clear_scene()
