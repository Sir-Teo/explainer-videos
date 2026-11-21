from __future__ import annotations

from videos.economics.econ58.common import *  # noqa: F403

PROBLEMS = [
    r"The rule of a half: \ with linear demand, \ show that the gain on new trips is exactly $\tfrac12 (q_1 - q_0)"
    r"(g_0 - g_1)$, \ and that it is an approximation otherwise.",
    r"Bo's fares: \ show that counting travellers' fare savings and Bo's lost profit nets to the ferry's operating "
    r"cost. \ When would it not net out?",
    r"Saez's ratio: \ derive $1 - e\,a\,\tau/(1 - \tau)$ for a small rise in a top rate on a Pareto tail with "
    r"exponent $a$.",
    r"Weitzman: \ with rates of 1\% and 7\% equally likely, \ find the certainty-equivalent rate at 50 and 200 "
    r"years.",
    r"A regulation prevents an unknown number of deaths. \ Write the break-even sentence its analysis should "
    r"contain, \ and say why it is more honest than a point estimate.",
    r"$\bigstar$ \ Option value: \ with traffic 30\% above or below forecast next year, \ find the cost overrun at "
    r"which waiting becomes worth more than building now.",
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
        a = wrapped_label(r"By adding up, \ in money, \ what a change does to everyone it touches, \ against what "
                          r"would happen anyway, \ with the future discounted \ and behaviour allowed for. \ The "
                          r"method is old and sound; \ its inputs are forecasts, \ prices that do not exist, \ and a "
                          r"discount rate that is partly ethics. \ So show the ranges, \ take the outside view, \ "
                          r"and score the forecasts afterwards.", 11.6, 26, WHITE)
        a.next_to(q, DOWN, buff=0.5)
        F = load("film")
        mini = plane([1984, 2036], [-16, 6], x_length=4.2, y_length=1.3)
        logo = VGroup(*[path(mini, b["fy"], np.clip(b["v"], -16, 6), CBO, 1.0, smooth=False).set_stroke(opacity=0.5)
                        for b in F["baselines"][::2]])
        logo.add(path(mini, F["actual_fy"], F["actual"], WHITE, 2.2, smooth=False))
        logo.next_to(a, DOWN, buff=0.4)
        with self.voiceover(
            "So: how does a government decide whether a project or a law is worth it? <bookmark mark='a'/> By adding "
            "up, in money, what the change does to everyone it touches, against what would have happened anyway, "
            "with the future discounted and people's responses allowed for. The method is old and sound. Its inputs "
            "are forecasts, prices for things no market sells, and a discount rate that is partly ethics. So show "
            "the ranges, take the outside view, and score the forecasts afterwards."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(LaggedStart(*[Create(m) for m in logo], lag_ratio=0.05), run_time=8.0)
        self.clear_scene()

    def recap(self):
        B, H, V, P, D, S, M, C, R = (load(x) for x in ("bridge", "hedonic", "vsl", "playit", "discount", "scoring",
                                                        "microsim", "cge", "risk"))
        h = S["horizon"]
        items = [
            (r"benefits `to whomsoever they may accrue', \ against what happens anyway", E.ACCENT),
            (rf"Dupuit's surplus: \ the bridge's travellers gain {B['year']['surplus']:.1f} a year; \ the rule of a "
             r"half", TRAV),
            (r"transfers net out: \ Bo's lost fares are not a gain to the Island", BO),
            (rf"noise from house prices: \ {H['full']:.2f}\% a decibel, \ once the harbour is held fixed"
             .replace("-", "{-}"), NOISE),
            (rf"a statistical life: \ {V['controls']:.1f} million with ability held fixed, \ {V['naive']:.1f} "
             r"without", SAFE),
            (rf"Play it: \ {P['behavioural']:.0f} million, \ not the static {P['static']:.0f}", BEHAV),
            (rf"the rate decides: \ the bridge {D['bridge']['0.030']:+.0f} at 3\%, \ {D['bridge']['0.070']:+.0f} "
             r"at 7\%".replace("-", "{-}"), RATE),
            (r"dynamic scores: \ growth pays some back; \ interest can take it back", DYN),
            (rf"CBO's record: \ {h[0]['mae']:.1f}\% of GDP in the first year, \ {h[5]['mae']:.1f}\% by the sixth",
             CBO),
            (r"the distribution table: \ the poorest tenth gains nothing from a higher allowance", BEN),
            (rf"the outside view: \ a forecast NPV of {R['forecast']:+.0f}, \ a {100 * R['p_negative']:.0f}\% "
             r"chance of loss".replace("-", "{-}"), COST),
            (r"targets change the numbers they target", E.ACCENT),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=27, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 58, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        del M, C
        with self.voiceover(
            "Part fifty-eight in twelve lines. <bookmark mark='r1'/> Benefits to whomsoever they may accrue, against "
            "what would happen anyway. <bookmark mark='r2'/> Dupuit's surplus, and the rule of a half. <bookmark "
            "mark='r3'/> Transfers net out. <bookmark mark='r4'/> Noise can be priced from houses, if everything "
            "else about them is held fixed. <bookmark mark='r5'/> A statistical life is a rate of exchange for small "
            "risks, and leaving out ability biases it down. <bookmark mark='r6'/> In the Play it, behaviour cut the "
            "score by nearly a third. <bookmark mark='r7'/> The discount rate decides long-lived projects. <bookmark "
            "mark='r8'/> Dynamic scores add growth and interest. <bookmark mark='r9'/> CBO's errors grow with the "
            "horizon, and the biggest misses are laws passed later. <bookmark mark='r10'/> Distribution tables show "
            "who gains. <bookmark mark='r11'/> The outside view turns a bridge that passes into one that probably "
            "fails. <bookmark mark='r12'/> And targets change the numbers they target."
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
            "The problems: the rule of a half; why Bo's fares net out; Saez's ratio, derived; Weitzman's rate at "
            "fifty and two hundred years; the break-even sentence a regulation's analysis should contain; and a "
            "starred problem on the cost overrun at which waiting beats building. Full solutions are in the part's "
            "notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Anthony Boardman, \ David Greenberg, \ Aidan Vining and David Weimer, \emph{Cost-Benefit Analysis: "
             r"Concepts and Practice} (5th ed., \ 2018)",
             r"HM Treasury, \emph{The Green Book}; \ Office of Management and Budget, \emph{Circular A-4}",
             r"Bent Flyvbjerg, \ Nils Bruzelius and Werner Rothengatter, \emph{Megaprojects and Risk} (2003)"],
            [r"Dupuit (1844); \ Hotelling (1947); \ Schelling (1968); \ Rosen (1974); \ Thaler and Rosen (1976); \ "
             r"Harberger (1962)",
             r"Goodhart (1975); \ Campbell (1979); \ Kahneman and Lovallo (1993); \ Diamond and Hausman (1994)",
             r"Weitzman (1998, 2001); \ Saez (2001); \ Flyvbjerg, \ Holm and Buhl (2002, 2005); \ Viscusi and Aldy "
             r"(2003)",
             r"Auerbach (2005); \ Kehoe (2005); \ Bevan and Hood (2006); \ Drupp et al.\ (2018); \ Hendren and "
             r"Sprung-Keyser (2020)"])
        with self.voiceover(
            "The reading: Boardman, Greenberg, Vining and Weimer's textbook of cost-benefit analysis; the Green Book "
            "and Circular A-4, which are short and worth reading whole; and Flyvbjerg's Megaprojects and Risk. Then "
            "the papers, from Dupuit to Hendren and Sprung-Keyser."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1997, r"the FTC against Staples and Office Depot", r"the companies say they compete with "
                          r"every shop that sells a pen; \ the economists look at the prices in towns with one, \ "
                          r"two or three office superstores", color=E.ACCENT, width=10.4, font_size=23)
        nxt = VGroup(label(r"Next: \ Part 59 \ $\cdot$ \ Act XI, \ Economics at Work", font_size=30, color=GREY_B),
                     label(r"The Expert Witness", font_size=46),
                     label(r"what survives cross-examination?", font_size=24, color=E.ACCENT)).arrange(DOWN,
                                                                                                     buff=0.22)
        head = label(r"from scoring a law to defending a number in court", font_size=26, color=GREY_A).to_edge(
            UP, buff=0.5)
        steps_ = VGroup(*[VGroup(RoundedRectangle(width=2.9, height=0.9, corner_radius=0.12, stroke_color=c_,
                                                  stroke_width=2.0), label(t_, font_size=18, color=c_))
                          for t_, c_ in ((r"market definition", TRAV), (r"diversion ratios", SAFE),
                                         (r"merger simulation", BEN), (r"damages", COST))])
        for s_ in steps_:
            s_[1].move_to(s_[0])
        steps_.arrange(RIGHT, buff=0.3)
        VGroup(hc, steps_, nxt).arrange(DOWN, buff=0.45).next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Next time, from scoring a law to defending a number in court. <bookmark mark='a'/> In 1997 the Federal "
            "Trade Commission sued to stop Staples from buying Office Depot. The companies said they competed with "
            "every shop that sells a pen; the Commission's economists looked at the prices in towns with one, two or "
            "three office superstores. <bookmark mark='b'/> Market definition, diversion ratios, merger simulation "
            "and damages, and what each looks like under cross-examination. <bookmark mark='c'/> Part fifty-nine: "
            "the expert witness."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in steps_], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(nxt, shift=UP * 0.1))
        self.wait(9.5)
