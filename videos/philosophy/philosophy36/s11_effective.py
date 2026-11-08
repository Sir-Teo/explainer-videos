from __future__ import annotations

from videos.philosophy.philosophy36.common import *  # noqa: F403


class Effective(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"Doing the most good", r"How should a fixed budget be spent on health?",
                            lit=(1972, 2015), part=PART)
        with self.voiceover("Chapter ten. Doing the most good."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.qaly()
        self.portfolio()
        self.weights()
        self.critiques()

    def qaly(self):
        head = label(r"Measuring health: \ QALYs and DALYs", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        f1 = MathTex(r"\text{QALYs} \;=\; \sum_{\text{years}} q_t, \qquad q_t \in [0, 1]:\; 0 \text{ dead},\; "
                     r"1 \text{ full health}", font_size=32, color=WELL)
        f2 = MathTex(r"\mathrm{DALYs} = \mathrm{YLL} + \sum_t d_t\,\Delta t, \qquad 0 \le d_t \le 1",
                     font_size=32, color=RISK)
        f3 = MathTex(r"\text{cost-effectiveness} \;=\; \frac{\Delta\,\text{cost}}{\Delta\,\text{QALYs}}", font_size=34,
                     color=MONEY)
        fs = VGroup(f1, f2, f3).arrange(DOWN, buff=0.5).move_to([0, 0.7, 0])
        foot = stack([(r"weights from surveys: \ time trade-off, \ standard gamble \ (Part 33's lotteries)", GREY_A),
                      (r"a common currency for wildly different treatments: \ hips, \ vaccines, \ bed nets", WELL),
                      (r"and a value judgment in every weight: \ a year with a disability counted as less", RISK)],
                     font_size=19, buff=0.15).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Health systems must weigh lives every day, and they do it with a common currency. "
            "<bookmark mark='a'/>A quality-adjusted life year counts each year of life weighted by its quality, from "
            "zero for death to one for full health on this simplified scale. The weights come from surveys, by the "
            "time trade-off, how many "
            "years of full health would you accept in place of ten with this condition, or by the standard gamble, "
            "Part 33's lotteries. <bookmark mark='b'/>The disability-adjusted life year, used by the World Health "
            "Organization and the Global Burden of Disease, counts years of life lost, YLL, plus years lived with "
            "disability weighted by its severity. Here d is the disability weight, from zero for full health to "
            "one for a state equivalent to death, multiplied by the duration in years. <bookmark mark='c'/>"
            "Cost-effectiveness is extra cost over extra QALYs. "
            "<bookmark mark='d'/>The currency lets a health service compare hip replacements, vaccines and bed nets. "
            "And every weight is a value judgment: critics point out that QALYs count a year lived with a disability "
            "as worth less."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f1), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(Write(f2))
            vo.wait_until("c")
            self.play(Write(f3))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]), FadeIn(foot[2]))
        self.clear_scene()

    def portfolio(self):
        d = load("cea")
        head = label(r"Heavy tails: \ why prioritization matters", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert (d["n"], d["best_cost"], d["median_cost"], d["worst_cost"]) == (200, 105.3, 4589, 742942)
        assert (d["qalys_best"], d["qalys_median"], d["ratio_best_median"]) == (9499, 217.9, 43.6)
        lg = d["sorted_log10"]
        ax = Axes(x_range=[0, 200, 50], y_range=[2, 6, 1], x_length=6.6, y_length=3.6, tips=False,
                  axis_config={"color": GREY_B, "font_size": 15}).move_to([-3.0, -0.6, 0])
        yn = VGroup(*[MathTex(rf"10^{k}", font_size=22, color=GREY_B).next_to(ax.c2p(0, k), LEFT, buff=0.12)
                      for k in (2, 3, 4, 5, 6)])
        xl = label(r"200 interventions, \ from best to worst", font_size=16, color=GREY_A).next_to(ax.x_axis, DOWN,
                                                                                                buff=0.3)
        yl = label(r"dollars per QALY \ (log scale)", font_size=16, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(
            ax, LEFT)
        bars = VGroup()
        for i, v in enumerate(lg):
            top = ax.c2p(i + 0.5, v)
            bot = ax.c2p(i + 0.5, 2)
            bars.add(Line(bot, top, color=MONEY if i == 0 else (POP if i == 99 else GREY_B), stroke_width=2.2))
        tb = label(r"best: \ \$105", font_size=15, color=MONEY).next_to(ax.c2p(2, lg[0]), UR, buff=0.1)
        tm = label(r"median: \ \$4,589", font_size=15, color=POP).next_to(ax.c2p(100, lg[99]), UP, buff=0.5)
        side = stack([(r"a toy: \ costs per QALY drawn log-normally, \ as surveys find them", GREY_A),
                      (r"\$1 million buys 9,499 QALYs at the best, \ 218 at the median: \ 44 times as many", MONEY),
                      (r"Ord \ (2013): \ in a major survey of health interventions, \ the best was about 15,000 times "
                       r"as cost-effective as the worst", GREY_A),
                      (r"Singer \ (1972) \ to effective altruism: \ give, \ and give where it does most", WELL)],
                     font_size=18, aligned_edge=LEFT, width=5.0, buff=0.26).move_to([4.2, -0.4, 0])
        with self.voiceover(
            "Why does the choice of intervention matter so much? <bookmark mark='a'/>The Reasoner draws two hundred "
            "interventions whose costs per QALY are spread log-normally, the heavy-tailed shape that surveys of real "
            "interventions report, and sorts them. <bookmark mark='b'/>The best costs a hundred and five dollars per "
            "QALY; the median four thousand five hundred and eighty nine; the worst over seven hundred thousand. "
            "<bookmark mark='c'/>A million dollars buys nine thousand four hundred and ninety nine QALYs at the best, "
            "and two hundred and eighteen at the median: forty four times as many. <bookmark mark='d'/>Toby Ord's "
            "analysis, in 2013, of a major survey of health interventions in poor countries found the best about "
            "fifteen thousand times as cost-effective as the worst. <bookmark mark='e'/>This is the core of effective "
            "altruism, the movement that grew from Peter Singer's argument of 1972: give, and give where it does the "
            "most good, because the differences are not a few percent but orders of magnitude."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(yn), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(b) for b in bars], lag_ratio=0.01, run_time=2.5), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(tb), FadeIn(tm))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def weights(self):
        d = load("weights")
        head = label(r"Who counts?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        ks = d["kinds"]
        assert [k["weight"] for k in ks] == [1.0, 1.35, 1.5, 10.0] and d["largest"] == "kind D"
        q = label(r"``The question is not, \ Can they \textit{reason}? \ nor, \ Can they \textit{talk}? \ but, \ Can "
                  r"they \textit{suffer}?'' \ --- Bentham \ (1789)", font_size=20, color=WELL).next_to(head, DOWN,
                                                                                                       buff=0.3)
        f = MathTex(r"\text{expected weight} \;=\; \text{numbers} \times P(\text{sentient}) \times "
                    r"\text{welfare range}", font_size=30, color=FUT).next_to(q, DOWN, buff=0.3)
        hd = [r"\text{kind}", r"\text{per human}", r"P(\text{sentient})", r"\text{welfare range}",
              r"\text{expected weight}"]
        cells = [[label(k["kind"], font_size=18), label(f"{k['n']:,}", font_size=18), label(f"{k['p']:g}", font_size=18),
                  label(f"{k['range']:g}", font_size=18), label(f"{k['weight']:g}", font_size=18,
                                                                 color=RISK if k["kind"] == "kind D" else GOAL)]
                 for k in ks]
        grid = ValueGrid(hd, cells, col_w=[2.2, 2.2, 2.2, 2.4, 2.6], cell_h=0.48, font_size=16).move_to([0, -1.2, 0])
        foot = label(r"invented numbers: \ the structure is the point", font_size=17, color=GREY_A).to_edge(DOWN,
                                                                                                         buff=0.3)
        with self.voiceover(
            "Impartiality raises one more question: whose welfare counts? <bookmark mark='a'/>Bentham answered in a "
            "footnote of 1789: the question is not, can they reason? nor, can they talk? but, can they suffer? "
            "Peter Singer's Animal Liberation, of 1975, made equal consideration of interests the basis of a "
            "movement. <bookmark mark='b'/>Under uncertainty, a being's expected moral weight is its numbers, times "
            "the probability that it is sentient, times how much welfare it can have. <bookmark mark='c'/>The "
            "Reasoner runs a toy with invented numbers: three kinds of being, each more numerous and less likely to "
            "be sentient. Per human, the last kind, a million strong, one percent likely to feel anything, with a "
            "thousandth of our welfare range, carries ten times the expected weight of humanity. "
            "<bookmark mark='d'/>Research groups now try to estimate such numbers for real animals. Whatever they "
            "find, the structure is the one this part keeps meeting: vast numbers multiplied by small probabilities "
            "can dominate everything else."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(f))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(c) for row in grid.cell for c in row],
                      FadeIn(foot))
            vo.wait_until("d")
            self.wait(0.5)
        self.clear_scene()

    def critiques(self):
        head = label(r"Effective altruism and its critics", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"the movement", r"Singer, \ \textit{The Most Good You Can Do} \ (2015); \ MacAskill, \ "
                                  r"\textit{Doing Good Better} \ (2015): \ evidence, \ cost-effectiveness, \ and "
                                  r"impartiality", WELL),
                (r"measurability", r"what is easy to count crowds out what matters but is hard to count: \ rights, \ "
                                   r"institutions, \ dignity", RISK),
                (r"systemic change", r"Srinivasan \ (2015); \ Gabriel \ (2017): \ charity at the margin can leave "
                                     r"unjust structures in place", POP),
                (r"the critique from care", r"Crary \ (2023): \ an impartial calculus misdescribes what we owe to "
                                            r"particular others: \ Part 35's care ethics", FUT)]
        g = rows_table(rows, top=1.6, gap=0.45, width=8.2, x_text=-2.0, label_size=20, text_size=19)
        with self.voiceover(
            "Effective altruism has grown into a large movement, with large critics. <bookmark mark='a'/>Peter "
            "Singer's The Most Good You Can Do and William MacAskill's Doing Good Better, both of 2015, set out its "
            "method: evidence, cost-effectiveness, and impartiality between people near and far. "
            "<bookmark mark='b'/>Critics say what is easy to count crowds out what matters but is hard to count: "
            "rights, institutions, dignity. <bookmark mark='c'/>Amia Srinivasan in 2015, and Iason Gabriel in 2017, "
            "pressed the objection from systemic change: charity at the margin can leave unjust structures in place, "
            "and may even prop them up. <bookmark mark='d'/>And Alice Crary argued in 2023 that the impartial "
            "calculus misdescribes what we owe to particular others, the objection from care that Part 35 raised."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
