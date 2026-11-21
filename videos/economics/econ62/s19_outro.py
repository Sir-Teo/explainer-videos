from __future__ import annotations

from videos.economics.econ62.common import *  # noqa: F403
from videos.economics.econ62.s01_hook import floor

PROBLEMS = [
    r"Dispersion: \ with CES demand of elasticity $\sigma$, \ show that a plant's revenue share is proportional to "
    r"$\varphi^{\sigma-1}$, \ and explain why higher $\sigma$ raises the survival cutoff.",
    r"Piece rates: \ with output $a e$, \ piece rate $r$ and effort cost $c(e - 1)^2/2$, \ find a worker's effort, "
    r"\ and the ability above which they prefer the piece rate to a guaranteed wage $w$.",
    r"Gabaix and Landier: \ if pay is $w(n) \propto S(n^*)^{\beta/\alpha} S(n)^{\gamma - \beta/\alpha}$, \ show that "
    r"scaling every firm by $\lambda$ scales pay by $\lambda^{\gamma}$.",
    r"Jensen and Meckling: \ maximize $\alpha(V - P) + k\ln(1 + P)$, \ and find the agency cost as a function of "
    r"$\alpha$.",
    r"Trade-off: \ with value $V_U + \tau D - $ expected distress costs, \ write the first-order condition for the "
    r"best debt, \ and explain why more volatile firms borrow less.",
    r"$\bigstar$ \ Garicano: \ with problems $z \sim$ Exp(1), \ worker knowledge $z_w$ and helping time $h$, \ show "
    r"that a manager's span is $e^{z_w}/h$, \ and that cheaper communication lowers $z_w$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.answer()
        self.recap()
        self.problems()
        self.references()
        self.next_part()

    def answer(self):
        q = wrapped_label(ASK, 12.0, 38, E.ACCENT).move_to(UP * 2.4)
        a = wrapped_label(r"Partly because competition lets them, \ and partly because management, \ which can be "
                          r"measured, \ causes productivity: \ cheap practices raised it by a sixth in a year when "
                          r"they were taught. \ Owners had not adopted them because they did not know, \ had no "
                          r"time, \ and faced no pressure; \ and practices that rest on trust are hard to copy. \ "
                          r"Inside the firm, \ how people are paid, \ promoted, \ financed and watched shapes what "
                          r"they do.", 11.6, 26, WHITE)
        a.next_to(q, DOWN, buff=0.5)
        fl = floor(True).scale(0.42).next_to(a, DOWN, buff=0.45)
        with self.voiceover(
            "So: why are some firms so much better run than others, and can it be taught? <bookmark mark='a'/> "
            "Partly because competition lets the laggards live, and partly because management, which can be "
            "measured, causes productivity: cheap practices raised it by a sixth in a year when they were taught. "
            "Owners had not adopted them because they did not know, had no time, and faced no pressure; and "
            "practices that rest on trust are hard to copy. Inside the firm, how people are paid, promoted, "
            "financed and watched shapes what they do. So yes, much of it can be taught, but not all of it can be "
            "bought."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(FadeIn(fl), run_time=1.5)
        self.clear_scene()

    def recap(self):
        D, M, Pr, X, Pc, Pe, C, T, B, W, G = (load(x) for x in (
            "dispersion", "management", "practices", "experiment", "piece", "peter", "ceo", "tradeoff", "buyouts",
            "wfh", "conglomerates"))
        r3 = [r for r in D["rows"] if r["sigma"] == 3.0][0]
        team = 100 * (Pe["rules"]["the best manager"]["team_sales"] - Pe["rules"]["the best seller"]["team_sales"])
        items = [
            (rf"dispersion: \ survivors' 90/10 ratio {r3['ratio_90_10']:.2f}, \ Syverson's 1.92", PLANT),
            (rf"management scores: \ {M['slope']:.2f} log points of productivity per point", MGR),
            (rf"Play it: \ recording defects returns {Pr['rows']['record and act on defects']['per_dollar']:.1f} per "
             r"dollar; \ the loom loses", MGR),
            (rf"the experiment: \ +{100 * X['mean_est']:.0f}\% on the Island, \ +17\% near Mumbai", TREAT),
            (rf"piece rates: \ +{100 * Pc['gain_total']:.0f}\%, \ about half from sorting; \ Safelite +44\%", WORK),
            (rf"the Peter principle: \ the best manager's team sells {team:.0f}\% more than the best seller's",
             WORK),
            (r"CEO pay: \ size to the power $\tfrac13$; \ six times the firms, \ six times the pay", CEO),
            (rf"capital structure: \ the trade-off's best about {100 * T['best']:.0f}\% debt; \ the pecking order",
             FIN),
            (r"agency: \ perks rise as the manager's share falls; \ family successions cost four points", OWN),
            (rf"buyouts: \ jobs at old establishments {100 * B['emp_original'][2]:+.1f}\% in two years; \ new ones "
             r"opened".replace("-", "{-}"), COST),
            (rf"working from home: \ +{100 * W['performance']:.0f}\% calls, \ quits more than halved", GAIN),
            (rf"conglomerates: \ {100 * G['discount']:.1f}\%, \ about half there before".replace("-", "{-}"), COST),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=27, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 62, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part sixty-two in twelve lines. <bookmark mark='r1'/> Plants in the same industry differ two to one. "
            "<bookmark mark='r2'/> Management can be scored, and the score tracks productivity. <bookmark "
            "mark='r3'/> The cheap practices pay most. <bookmark mark='r4'/> An experiment shows they cause it. "
            "<bookmark mark='r5'/> Piece rates work through effort and through who joins. <bookmark mark='r6'/> "
            "Promoting the best seller costs the team. <bookmark mark='r7'/> Executive pay tracks the size of "
            "firms. <bookmark mark='r8'/> Debt trades a tax shield for distress. <bookmark mark='r9'/> Separating "
            "ownership from control has a cost. <bookmark mark='r10'/> Buyouts move jobs as much as they cut them. "
            "<bookmark mark='r11'/> Working from home can raise output and keep people. <bookmark mark='r12'/> And "
            "diversification's discount is partly who diversifies."
        ) as vo:
            self.play(FadeIn(head))
            for i, r_ in enumerate(rows):
                vo.wait_until(f"r{i + 1}")
                self.play(FadeIn(r_, shift=RIGHT * 0.15), run_time=0.8)
            self.play(Indicate(rows, color=WHITE, scale_factor=1.0), run_time=2.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20, width=13.0)
        with self.voiceover(
            "The problems: survival and dispersion under CES demand; effort and sorting under piece rates; why "
            "executive pay scales with firm size; Jensen and Meckling's agency cost; the trade-off theory's best "
            "debt; and a starred problem on Garicano's hierarchy. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Edward Lazear and Michael Gibbs, \emph{Personnel Economics in Practice} (3rd ed., \ 2014)",
             r"Robert Gibbons and John Roberts, \ eds., \emph{The Handbook of Organizational Economics} (2013)",
             r"Jean Tirole, \emph{The Theory of Corporate Finance} (2006)"],
            [r"Modigliani and Miller (1958); \ Jensen and Meckling (1976); \ Myers and Majluf (1984); \ Jensen and "
             r"Murphy (1990)",
             r"Garicano (2000); \ Lazear (2000); \ Bertrand and Mullainathan (2001); \ Graham and Harvey (2001); \ "
             r"Syverson (2004, \ 2011)",
             r"Bloom and Van Reenen (2007); \ Bennedsen et al.\ (2007); \ Gabaix and Landier (2008); \ Gibbons and "
             r"Henderson (2012)",
             r"Bloom et al.\ (2013, \ 2015); \ Davis et al.\ (2014); \ Bruhn, \ Karlan and Schoar (2018); \ Benson, "
             r"\ Li and Shue (2019)"])
        with self.voiceover(
            "The reading: Lazear and Gibbs on personnel economics; Gibbons and Roberts's handbook of organizational "
            "economics; and Tirole on corporate finance. Then the papers, from Modigliani and Miller to the "
            "management experiments."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(2011, r"11 March, \ north-east Japan", r"an earthquake and tsunami; \ firms far from the "
                          r"coast, \ undamaged, \ lose sales because a supplier's supplier is under water",
                          color=E.ACCENT, width=10.4, font_size=23)
        nxt = VGroup(label(r"Next: \ Part 63 \ $\cdot$ \ Act XII, \ The Frontier", font_size=30, color=GREY_B),
                     label(r"The Economy as a Network", font_size=46),
                     label(r"when does a shock to one firm become a shock to everyone?", font_size=24,
                           color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"from inside one firm to the links between all of them", font_size=26, color=GREY_A).to_edge(
            UP, buff=0.5)
        steps_ = VGroup(*[VGroup(RoundedRectangle(width=2.9, height=0.9, corner_radius=0.12, stroke_color=c_,
                                                  stroke_width=2.0), label(t_, font_size=18, color=c_))
                          for t_, c_ in ((r"supply chains", PLANT), (r"Hulten's theorem", MGR),
                                         (r"granular firms", CEO), (r"cascades", COST))])
        for s_ in steps_:
            s_[1].move_to(s_[0])
        steps_.arrange(RIGHT, buff=0.3)
        VGroup(hc, steps_, nxt).arrange(DOWN, buff=0.45).next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Next time, from inside one firm to the links between all of them. <bookmark mark='a'/> On the eleventh "
            "of March 2011 an earthquake and tsunami struck north-east Japan. Firms far from the coast, with no "
            "damage at all, lost sales because a supplier's supplier was under water, and so did their customers. "
            "<bookmark mark='b'/> Supply chains, Hulten's theorem, granular firms, and cascades. <bookmark "
            "mark='c'/> Part sixty-three: the economy as a network."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in steps_], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(nxt, shift=UP * 0.1))
        self.wait(9.5)
