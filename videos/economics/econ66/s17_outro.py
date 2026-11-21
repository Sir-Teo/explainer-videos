from __future__ import annotations

from videos.economics.econ66.common import *  # noqa: F403
from videos.economics.econ66.s08_power import hub_network

PROBLEMS = [
    r"The formula: \ show that with $\varepsilon = 4$ and $\varphi = 0.25$ the reciprocal rate is half of "
    r"$(m - x)/m$; \ compute it for Vietnam's 2024 trade, \ and again with $\varphi = 0.945$.",
    r"The optimal tariff: \ a large importer faces foreign export supply with elasticity $\varepsilon^\ast$; \ show "
    r"that the tariff that maximizes its welfare is $t^\ast = 1/\varepsilon^\ast$.",
    r"Bilateral balances: \ build three countries whose trade is balanced overall but not pair by pair; \ what would "
    r"tariffs that balanced every pair do to the volume of trade?",
    r"Brander and Spencer: \ with $p = a - q_1 - q_2$ and cost $c$, \ derive the Cournot quantities under "
    r"subsidies, \ the one-sided optimum $s = (a - c)/4$ and the Nash subsidies $(a - c)/5$.",
    r"Dependence: \ with the ACR formula, \ show that losing a supplier with spending share $s$ costs "
    r"$1 - (1 - s)^{1/\theta}$; \ evaluate it for $s = 0.2$ and $\theta = 2, 4, 8$.",
    r"$\bigstar$ \ Infant industries: \ with unit cost $c_0 (Q/Q_0)^{-b}$, \ find the cumulative output at which "
    r"the industry matches the world price, \ and state Mill's and Bastable's tests as conditions on $b$, \ the "
    r"tariff's length and the discount rate.",
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
        a = wrapped_label(r"They shrink, \ and they are redistributed. \ A tariff is paid mostly at home, \ and a "
                          r"tariff war leaves every side poorer than cooperation; \ bilateral deficits measure "
                          r"specialization, \ not unfairness. \ Dependence on a hub or a supplier is power for whoever "
                          r"controls it, \ and resilience is worth buying at the margin. \ Industrial policy can "
                          r"build industries when it is temporary, \ disciplined and aimed at learning that spills "
                          r"over; \ subsidy races mostly benefit buyers elsewhere.", 11.6, 25, WHITE)
        a.next_to(q, DOWN, buff=0.45)
        g = hub_network(cut=True).scale(0.45).next_to(a, DOWN, buff=0.3)
        with self.voiceover(
            "So: what happens to the gains from trade when trade becomes a weapon? <bookmark mark='a'/> They "
            "shrink, and they are redistributed. A tariff is paid mostly at home, and a tariff war leaves every "
            "side poorer than cooperation would. Bilateral deficits measure specialization, not unfairness. "
            "Dependence on a hub or a supplier is power for whoever controls it, and resilience is worth buying at "
            "the margin, not by leaving trade. Industrial policy can build industries when it is temporary, "
            "disciplined and aimed at learning that spills over; subsidy races mostly benefit buyers elsewhere."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(FadeIn(g), run_time=1.5)
        self.clear_scene()

    def recap(self):
        F, E_, P, B, S, Pw, R, Bs = (load(x) for x in ("formula", "effective", "prices", "bloc", "scenarios",
                                                      "power", "resilience", "subsidies"))
        n4 = [x for x in S["rows"] if x["theta"] == 4.0]
        items = [
            (rf"the formula: \ Vietnam {100 * F['rate']:.0f}\%, \ or {100 * F['rate_945']:.0f}\% with realistic "
             r"pass-through", TARIFF),
            (r"2018--19: \ complete pass-through; \ \$51 billion paid, \ \$7.2 billion lost", PRICE),
            (rf"2025: \ the effective rate peaked at {100 * E_['peak']:.1f}\%; \ goods prices "
             rf"{100 * P['goods_2025']:+.1f}\%", PRICE),
            (r"Play it: \ free trade wins unless the partner never answers", US),
            (rf"the war: \ optimal tariff {100 * B['optimal']:.0f}\%, \ both lose at the Nash tariffs", STATE),
            (rf"15\% for all: \ US {100 * n4[0]['us']:+.2f}\% alone, \ {100 * n4[1]['us']:+.2f}\% with "
             r"retaliation".replace("-", "{-}"), ROW),
            (r"deficits: \ saving minus investment; \ bilateral balances are not scorecards", US),
            (r"power: \ the hub sees and can cut off; \ \$300 billion frozen in 2022", TARIFF),
            (rf"dependence: \ a 20\% supplier's cutoff costs {100 * Pw['examples']['0.20']:.1f}\% at "
             r"$\theta = 4$", STATE),
            (rf"resilience: \ the firm buys {100 * R['x_private']:.0f}\% abroad, \ society would choose "
             rf"{100 * R['x_social']:.0f}\%", FREE),
            (r"infant industries: \ Mill, \ Bastable, \ Baldwin; \ Napoleon's blockade and Korea's drive", FREE),
            (rf"subsidy races: \ one gains {Bs['one']['w1'] - Bs['none']['w1']:.2f}, \ both lose "
             rf"{Bs['none']['w1'] - Bs['both']['w1']:.2f}", TARIFF),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=27, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 66, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part sixty-six in twelve lines. <bookmark mark='r1'/> One parameter changed the tariffs fourfold. "
            "<bookmark mark='r2'/> In 2018 Americans paid the tariffs. <bookmark mark='r3'/> In 2025 they paid "
            "again, slowly. <bookmark mark='r4'/> A tariff pays only against a partner who never answers. <bookmark "
            "mark='r5'/> Tariff wars leave everyone poorer. <bookmark mark='r6'/> Retaliation turns a gain into a "
            "loss. <bookmark mark='r7'/> Deficits are about saving. <bookmark mark='r8'/> Hubs are weapons. "
            "<bookmark mark='r9'/> Dependence is power. <bookmark mark='r10'/> Resilience has a price worth paying, "
            "at the margin. <bookmark mark='r11'/> Infant industries must grow up, and repay. <bookmark "
            "mark='r12'/> And subsidy races mostly pay buyers abroad."
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
            "The problems: the reciprocal formula; the optimal tariff; bilateral balances in a triangle; Brander "
            "and Spencer's subsidies; the cost of losing a supplier; and a starred problem on learning by doing and "
            "the infant-industry tests. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Douglas Irwin, \ \emph{Clashing over Commerce: \ A History of US Trade Policy} (2017)",
             r"Kyle Bagwell and Robert Staiger, \ \emph{The Economics of the World Trading System} (2002)",
             r"Henry Farrell and Abraham Newman, \ \emph{Underground Empire} (2023)"],
            [r"Brander and Spencer (1985); \ Bagwell and Staiger (1999); \ Ossa (2014); \ Juh\'asz (2018); \ "
             r"Lane (2025)",
             r"Amiti, \ Redding and Weinstein (2019); \ Fajgelbaum et al.\ (2020); \ Cavallo, \ Llamas and Vazquez "
             r"(2025)",
             r"Farrell and Newman (2019); \ Clayton, \ Maggiori and Schreger (2023); \ Alfaro and Chor (2023)",
             r"Kalouptsidi (2018); \ Barwick, \ Kalouptsidi and Zahur (2025); \ Juh\'asz, \ Lane and Rodrik (2024)"])
        with self.voiceover(
            "The reading: Douglas Irwin's history of American trade policy, Clashing over Commerce; Kyle Bagwell "
            "and Robert Staiger on the economics of the world trading system; and Henry Farrell and Abraham "
            "Newman's Underground Empire. Then the papers, from Brander and Spencer to the new industrial policy."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(r"2016", r"a two-humped camel", r"Brodeur and coauthors collect tens of thousands of test "
                          r"statistics from top economics journals: \ a valley just below the line of "
                          r"significance, \ a hump just above it", color=E.ACCENT, width=10.4, font_size=23)
        nxt = VGroup(label(r"Next: \ Part 67 \ $\cdot$ \ Act XII, \ The Frontier", font_size=30, color=GREY_B),
                     label(r"The Next Economics", font_size=46),
                     label(r"how much of what economics says is true, \ and how is the field changing?", font_size=24,
                           color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"from what economics says to whether it is true", font_size=26, color=GREY_A).to_edge(
            UP, buff=0.5)
        steps_ = VGroup(*[VGroup(RoundedRectangle(width=2.9, height=0.9, corner_radius=0.12, stroke_color=c_,
                                                  stroke_width=2.0), label(t_, font_size=18, color=c_))
                          for t_, c_ in ((r"replication", US), (r"p-hacking", TARIFF),
                                         (r"pre-registration", FREE), (r"the credibility revolution", STATE))])
        for s_ in steps_:
            s_[1].move_to(s_[0])
        steps_.arrange(RIGHT, buff=0.3)
        VGroup(hc, steps_, nxt).arrange(DOWN, buff=0.45).next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Next time, from what economics says to whether it is true. <bookmark mark='a'/> Abel Brodeur and "
            "coauthors collected tens of thousands of test statistics from the top economics journals. Their "
            "distribution has a valley just below the line of statistical significance and a hump just above it. "
            "Results that were nearly significant have gone somewhere. <bookmark mark='b'/> Replication, "
            "p-hacking, pre-registration, and the credibility revolution. <bookmark mark='c'/> Part sixty-seven: "
            "the next economics."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in steps_], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(nxt, shift=UP * 0.1))
        self.wait(9.5)
