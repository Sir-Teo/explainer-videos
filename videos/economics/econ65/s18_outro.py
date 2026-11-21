from __future__ import annotations

from videos.economics.econ65.common import *  # noqa: F403
from videos.economics.econ65.s02_playit import lab_row

PROBLEMS = [
    r"The task model: \ with $Y = \big(\int_{N-1}^{N} y(i)^{(\sigma-1)/\sigma} di\big)^{\sigma/(\sigma-1)}$, \ "
    r"capital on $[N-1, I]$ and labour $L$ spread over $[I, N]$, \ show that "
    r"$w = Y^{1/\sigma} (N-I)^{1/\sigma} L^{-1/\sigma}$, \ and split $d\ln w$ into displacement and productivity.",
    r"Hulten: \ show that if tasks making up a share $s$ of GDP become cheaper by a fraction $c$, \ TFP rises by "
    r"about $s\,c$; \ reproduce Acemoglu's two thirds of a percent.",
    r"Baumol: \ two goods with elasticity $\varepsilon < 1$ and productivity growth $g_1 > g_2$; \ show that good "
    r"1's share of spending tends to zero and aggregate growth to $g_2$.",
    r"Varian: \ in the model of sales with a share $\mu$ of shoppers, \ show that each seller's expected profit is "
    r"$(1-\mu)(v-c)/n$ \ and that the average price paid is $c + (1-\mu)(v-c)$.",
    r"Free entry: \ with Cournot profits $M/(N+1)^2$ and a fixed cost $F$, \ find $N^\ast$; \ how fast must $M$ "
    r"grow to hold $N^\ast$ fixed if $F$ triples every year?",
    r"$\bigstar$ \ Ideas: \ in $\dot A = \theta S^{\lambda} A^{\phi}$ with $S$ growing at $n$, \ show that "
    r"$g_A = \lambda n/(1-\phi)$; \ then let a share $\beta < 1$ of research tasks use capital, \ with "
    r"$\sigma < 1$, \ and show that growth returns to the same rate.",
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
        a = wrapped_label(r"Machines take tasks, \ and the economy invents new ones: \ wages depend on which is "
                          r"faster, \ and on how much cheaper the machines are. \ So far the experiments find large "
                          r"gains on single tasks, \ most for the least experienced, \ and the arithmetic of "
                          r"adoption turns them into modest aggregate gains. \ If machines can do every task, \ "
                          r"output can grow far faster while wages stop growing, \ and income goes to whoever owns "
                          r"the machines; \ while any essential task is left to people, \ it sets the pace.",
                          11.6, 25, WHITE)
        a.next_to(q, DOWN, buff=0.45)
        row = lab_row(0.7, n=20).scale(0.7).next_to(a, DOWN, buff=0.4)
        with self.voiceover(
            "So: what happens to work, growth and incomes if machines can do most tasks? <bookmark mark='a'/> "
            "Machines take tasks, and the economy invents new ones. Wages depend on which is faster, and on how "
            "much cheaper the machines are. So far the experiments find large gains on single tasks, most for the "
            "least experienced, and the arithmetic of adoption turns them into modest gains for the whole economy. "
            "If machines can do every task, output can grow far faster while wages stop growing, and the income "
            "goes to whoever owns the machines. While any essential task is left to people, that task sets the "
            "pace."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(LaggedStart(*[FadeIn(m, scale=0.6) for m in row], lag_ratio=0.05), run_time=1.5)
        self.clear_scene()

    def recap(self):
        K, T, J, D, H, G, B, R, N, S = (load(x) for x in ("keynes", "tasks", "jcurve", "desk", "hulten", "growth",
                                                         "baumol", "race", "nordhaus", "shoppers"))
        P = G["paths"]
        f20 = R["every task in 20 years"]
        items = [
            (rf"Keynes: \ {K['ratio_min']:.1f} to {K['ratio_max']:.1f} times richer, \ hours still twice his",
             GDP),
            (rf"Play it: \ 90\% of research automated, \ a boom to {100 * P['0.90']['peak']:.0f}\%, \ then back",
             IDEA),
            (r"history: \ Engels's pause, \ the horse, \ the ATM and the teller", WORK),
            (rf"the task model: \ displacement {100 * T['displacement']:.0f}, \ productivity "
             rf"+{100 * T['productivity']:.0f} log points".replace("-", "{-}"), MACH),
            (rf"the J-curve: \ measured productivity {100 * (J['low'] - 1):.0f}\% before it rises".replace("-", "{-}"),
             NEWT),
            (rf"the experiments: \ +{100 * D['est']:.0f}\% on the desk, \ +{100 * D['fifths'][0]['est']:.0f}\% for "
             r"the least skilled", TEXT),
            (rf"the aggregates: \ {100 * H['rows'][0]['tfp']:.2f}\% TFP in ten years, \ on Acemoglu's inputs", GDP),
            (rf"wages: \ every task automatable, \ labour's share {100 * f20['labour_share'][0]:.0f}\% $\to$ "
             rf"{100 * f20['labour_share'][-1]:.0f}\%", WORK),
            (rf"Baumol: \ growth slides from {100 * B['growth'][0]:.1f}\% towards {100 * B['g_slow']:.1f}\%", IDEA),
            (rf"Nordhaus: \ no acceleration yet; \ capital's share {100 * N['cap_last']:.0f}\%", MACH),
            (r"market structure: \ fixed costs against fast followers", NAIVE),
            (rf"agents: \ every buyer with one, \ the price near cost ({S['rows'][-1]['average_paid']:.2f})", GDP),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=27, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 65, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part sixty-five in twelve lines. <bookmark mark='r1'/> Keynes got the riches right and the leisure "
            "wrong. <bookmark mark='r2'/> Automating most of research gives a boom, not an explosion. <bookmark "
            "mark='r3'/> Past machines hurt workers for a generation, then helped. <bookmark mark='r4'/> "
            "Automation displaces; productivity and new tasks reinstate. <bookmark mark='r5'/> New technologies "
            "look worse before they look better. <bookmark mark='r6'/> Assistants help the least experienced most. "
            "<bookmark mark='r7'/> Task gains become modest aggregate gains, unless adoption is broad. <bookmark "
            "mark='r8'/> If machines can do everything, work earns little of the income. <bookmark mark='r9'/> The "
            "slow sector sets the pace. <bookmark mark='r10'/> The data show no explosion yet. <bookmark "
            "mark='r11'/> Scale favours the few; imitation favours the many. <bookmark mark='r12'/> And when "
            "software shops, prices fall towards cost."
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
            "The problems: the wage in the task model and its decomposition; Hulten's arithmetic for AI; Baumol's "
            "disease; the price in Varian's model of sales; free entry with fixed costs; and a starred problem on "
            "semi-endogenous growth with automated research. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Ajay Agrawal, \ Joshua Gans and Avi Goldfarb (eds), \ \emph{The Economics of Artificial "
             r"Intelligence: \ An Agenda} (2019)",
             r"Daron Acemoglu and Simon Johnson, \ \emph{Power and Progress} (2023)",
             r"David Autor, \ ``Why Are There Still So Many Jobs?'', \ \emph{Journal of Economic Perspectives} "
             r"(2015)"],
            [r"Keynes (1930); \ Zeira (1998); \ Acemoglu and Restrepo (2018, \ 2019, \ 2020, \ 2022); \ David "
             r"(1990)",
             r"Brynjolfsson, \ Rock and Syverson (2021); \ Noy and Zhang (2023); \ Dell'Acqua et al.\ (2023); \ "
             r"Brynjolfsson, \ Li and Raymond (2025)",
             r"Eloundou et al.\ (2024); \ Acemoglu (2024); \ Aghion, \ Jones and Jones (2019); \ Nordhaus (2021)",
             r"Korinek and Suh (2024); \ Korinek and Vipra (2025); \ Guerreiro, \ Rebelo and Teles (2022); \ "
             r"Varian (1980)"])
        with self.voiceover(
            "The reading: the National Bureau of Economic Research's volume on the economics of artificial "
            "intelligence, edited by Ajay Agrawal, Joshua Gans and Avi Goldfarb; Acemoglu and Johnson's Power and "
            "Progress; and David Autor's essay on why there are still so many jobs. Then the papers, from Keynes to "
            "the scenarios for transformative AI."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(r"2 April 2025", r"a tariff by formula", r"the United States announces tariffs on almost "
                          r"every country, \ set by a formula from each bilateral trade deficit, \ with a floor of "
                          r"ten percent", color=E.ACCENT, width=10.4, font_size=23)
        nxt = VGroup(label(r"Next: \ Part 66 \ $\cdot$ \ Act XII, \ The Frontier", font_size=30, color=GREY_B),
                     label(r"Geoeconomics and Industrial Policy", font_size=46),
                     label(r"what happens to the gains from trade when trade becomes a weapon?", font_size=24,
                           color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"from machines that change the economy to states that use it as a weapon", font_size=26,
                     color=GREY_A).to_edge(UP, buff=0.5)
        steps_ = VGroup(*[VGroup(RoundedRectangle(width=2.9, height=0.9, corner_radius=0.12, stroke_color=c_,
                                                  stroke_width=2.0), label(t_, font_size=18, color=c_))
                          for t_, c_ in ((r"trade wars as games", MACH), (r"chokepoints and sanctions", NAIVE),
                                         (r"security against efficiency", GDP), (r"industrial policy", NEWT))])
        for s_ in steps_:
            s_[1].move_to(s_[0])
        steps_.arrange(RIGHT, buff=0.3)
        VGroup(hc, steps_, nxt).arrange(DOWN, buff=0.45).next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Next time, from machines that change the economy to states that use it as a weapon. <bookmark "
            "mark='a'/> On the second of April 2025, the United States announced tariffs on almost every country, "
            "set by a formula from each country's bilateral trade deficit, with a floor of ten percent. <bookmark "
            "mark='b'/> Trade wars as games, chokepoints and sanctions, security against efficiency, and the return "
            "of industrial policy. <bookmark mark='c'/> Part sixty-six: geoeconomics and industrial policy."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in steps_], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(nxt, shift=UP * 0.1))
        self.wait(9.5)
