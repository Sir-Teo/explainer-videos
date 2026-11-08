from __future__ import annotations

from videos.philosophy.philosophy36.common import *  # noqa: F403


class Prices(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"Pricing lives", r"Can a life have a price in a cost-benefit analysis?", lit=(1968,),
                            part=PART)
        with self.voiceover("Chapter eleven. Pricing lives."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.vsl()
        self.thresholds()
        self.fairness()
        self.transfer()
        self.critics()

    def vsl(self):
        d = load("vsl")
        head = label(r"The value of a statistical life \ (Schelling, \ 1968)", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        assert (d["premium"], d["risk"], d["vsl"]) == (1200.0, 0.0001, 12000000.0)
        r1, r2 = d["rules"]
        assert (r1["passes"], r2["passes"], r1["breakeven_vsl"], round(r2["breakeven_vsl"])) == (True, False, 1e7,
                                                                                                 13333333)
        f = MathTex(r"\text{VSL} \;=\; \frac{\text{extra pay}}{\text{extra risk}} \;=\; \frac{\$1{,}200}{1/10{,}000} "
                    r"\;=\; \$12\text{ million}", font_size=36, color=MONEY).move_to([0, 1.7, 0])
        hd = [r"\text{rule}", r"\text{cost}", r"\text{deaths prevented}", r"\text{benefit at VSL}", r"\text{verdict}",
              r"\text{break-even VSL}"]
        cells = []
        for r in (r1, r2):
            cells.append([label(r["rule"], font_size=18), label(f"\\${r['cost'] / 1e6:.0f}M", font_size=18),
                          label(f"{r['lives']:g}", font_size=18), label(f"\\${r['benefit'] / 1e6:.0f}M", font_size=18),
                          label(r"adopt" if r["passes"] else r"reject", font_size=18, color=OK if r["passes"] else BAD),
                          label(f"\\${r['breakeven_vsl'] / 1e6:.1f}M", font_size=18, color=GREY_A)])
        grid = ValueGrid(hd, cells, col_w=[2.2, 1.4, 2.4, 2.4, 1.4, 2.4], cell_h=0.55, font_size=16).move_to(
            [0, -0.2, 0])
        foot = stack([(r"not the price of a person: \ the rate at which people trade money for small risks", GREY_A),
                      (r"US agencies use values of roughly ten to thirteen million dollars", GREY_A),
                      (r"the verdict on rear cameras turns on whether a life is worth \$12 or \$14 million", RISK)],
                     font_size=18, buff=0.14).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Governments put a number on life, and the number has a precise meaning. <bookmark mark='a'/>Thomas "
            "Schelling's essay of 1968, The Life You Save May Be Your Own, separated identified lives from "
            "statistical ones. Suppose workers accept one in ten thousand more annual risk of death for twelve "
            "hundred dollars more a year. Then together they trade twelve million dollars for one expected death: the "
            "value of a statistical life. <bookmark mark='b'/>It is not the price of a person, but the rate at which "
            "people trade money for small risks, and American agencies use values of roughly ten to thirteen million "
            "dollars. <bookmark mark='c'/>Cost-benefit analysis then sorts regulations. Guard rails costing twenty "
            "million dollars that prevent two deaths pass: twenty four million in benefits. "
            "<bookmark mark='d'/>A camera rule costing forty million that prevents three fails at twelve million a "
            "life, and would pass at anything above thirteen point three. Whole regulations turn on that number."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f))
            vo.wait_until("b")
            self.play(FadeIn(foot[0]), FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(c) for c in grid.cell[0]])
            vo.wait_until("d")
            self.play(*[FadeIn(c) for c in grid.cell[1]], FadeIn(foot[2]))
        self.clear_scene()

    def thresholds(self):
        head = label(r"Health technology assessment", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"a threshold", r"England's NICE has long recommended treatments costing up to about \pounds20,000 "
                                 r"to \pounds30,000 per QALY gained", MONEY),
                (r"opportunity cost", r"a budget is fixed: \ a treatment above the threshold displaces more health "
                                      r"elsewhere than it creates", WELL),
                (r"the rule of rescue", r"Jonsen \ (1986): \ we feel bound to save an identified person in peril, \ "
                                        r"whatever the cost: \ Schelling's identified lives again", RISK),
                (r"Taurek's question returns", r"should the numbers count, \ when the one is in front of us and the "
                                               r"many are statistics?", FUT)]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.2, x_text=-2.0)
        with self.voiceover(
            "Health systems with fixed budgets use QALYs directly. <bookmark mark='a'/>England's National Institute "
            "for Health and Care Excellence has long recommended treatments that cost up to about twenty to thirty "
            "thousand pounds per QALY gained. <bookmark mark='b'/>The logic is opportunity cost: with a fixed budget, "
            "a treatment far above the threshold displaces more health elsewhere than it creates. "
            "<bookmark mark='c'/>Against it stands what Albert Jonsen called the rule of rescue, in 1986: the "
            "imperative we feel to save an identified person in peril, whatever the cost. "
            "<bookmark mark='d'/>It is Schelling's distinction again, and Taurek's question from Part 35: should the "
            "numbers count, when the one is in front of us and the many are statistics?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def fairness(self):
        d = load("qaly")
        pts = d["patients"]
        head = label(r"Maximizing QALYs, \ and fairness", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert [p["qalys"] for p in pts] == [40.0, 20.0, 12.0]
        assert [p["fair_innings"] for p in pts] == [80.0, 40.0, 6.0]
        assert [p["priority"] for p in pts] == [57.14, 57.14, 14.63]
        hd = [r"\text{patient}", r"\text{years gained}", r"\text{quality}", r"\text{QALYs}", r"\text{fair innings}",
              r"\text{priority}"]
        cells = [[label(p["patient"], font_size=18), label(f"{p['years']}", font_size=18),
                  label(f"{p['quality']:g}", font_size=18), label(f"{p['qalys']:g}", font_size=18, color=MONEY),
                  label(f"{p['fair_innings']:g}", font_size=18, color=FUT),
                  label(f"{p['priority']:.1f}", font_size=18, color=WELL)] for p in pts]
        grid = ValueGrid(hd, cells, col_w=[3.8, 1.8, 1.4, 1.4, 1.9, 1.6], cell_h=0.55, font_size=16).move_to(
            [0, 0.9, 0])
        side = stack([(r"one course of treatment; \ without it, \ each patient dies", GREY_A),
                      (r"QALYs: \ treat the 30-year-old without a disability; \ the disabled patient counts half: \ "
                       r"Harris's double jeopardy \ (1987)", MONEY),
                      (r"fair innings \ (Williams, \ 1997): \ double the weight below 70, \ halve it above", FUT),
                      (r"priority: \ weight by $100 / $lifetime QALYs: \ the two 30-year-olds tie, \ 57.1 each", WELL)],
                     font_size=18, aligned_edge=LEFT, width=11.0, buff=0.2).move_to([0, -1.7, 0])
        with self.voiceover(
            "Maximizing QALYs has a famous problem. <bookmark mark='a'/>One course of treatment, three patients, each "
            "of whom will die without it. <bookmark mark='b'/>A thirty-year-old would gain forty years in full "
            "health: forty QALYs. Another thirty-year-old, with a disability that the weights rate at a half, would "
            "gain the same forty years, but only twenty QALYs. A seventy-year-old would gain twelve. QALY "
            "maximization treats the first. John Harris called it double jeopardy, in 1987: the disabled patient, "
            "already unlucky, is counted as worth saving half as much. <bookmark mark='c'/>Alan Williams proposed in "
            "1997 a fair innings weighting, which favours those who have not yet had a normal span of life; it widens "
            "the gap over the seventy-year-old, but not between the two younger patients. <bookmark mark='d'/>A "
            "prioritarian weighting, by how few QALYs each patient would have over a whole life, makes the two "
            "thirty-year-olds tie exactly, at fifty seven point one each. The choice of weight is the choice of "
            "ethics."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), *[FadeIn(c) for row in grid.cell for c in row[:3]])
            vo.wait_until("b")
            self.play(*[FadeIn(row[3]) for row in grid.cell], FadeIn(side[1]))
            vo.wait_until("c")
            self.play(*[FadeIn(row[4]) for row in grid.cell], FadeIn(side[2]))
            vo.wait_until("d")
            self.play(*[FadeIn(row[5]) for row in grid.cell], FadeIn(side[3]))
        self.clear_scene()

    def transfer(self):
        d = load("transfer")
        head = label(r"One life, \ many prices", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["vsl_us"] == 12e6 and d["elasticities"] == [0.8, 1.0, 1.2]
        assert [r["1.0"] for r in d["rows"]] == [12e6, 2.4e6, 6e5, 2.4e5]
        assert (d["rows"][3]["0.8"], d["rows"][3]["1.2"]) == (525000, 110000)
        f = MathTex(r"\text{VSL}_{\text{country}} \;=\; \text{VSL}_{\text{US}} \times \left(\frac{y}{y_{\text{US}}}"
                    r"\right)^{\varepsilon}", font_size=34, color=MONEY).move_to([0, 1.9, 0])
        hd = [r"\text{income, share of US}", r"\varepsilon = 0.8", r"\varepsilon = 1", r"\varepsilon = 1.2"]

        def fmt(v):
            return f"\\${v / 1e6:.2f}M" if v >= 1e6 else f"\\${v / 1e3:,.0f}k"

        cells = [[label(f"{r['ratio']:g}", font_size=18, color=GREY_A)] +
                 [label(fmt(r[str(e)]), font_size=18, color=MONEY if e == 1.0 else WHITE) for e in d["elasticities"]]
                 for r in d["rows"]]
        grid = ValueGrid(hd, cells, col_w=[3.6, 2.2, 2.2, 2.2], cell_h=0.5, font_size=17).move_to([0, 0.0, 0])
        foot = stack([(r"benefit transfer: \ the standard practice for countries without their own studies", GREY_A),
                      (r"at $\varepsilon = 1$, \ a life where incomes are a fiftieth of America's is priced at "
                       r"\$240,000: \ a fiftieth", RISK),
                      (r"equity weights by $1/y$ undo it exactly: \ one life, \ one value", WELL)],
                     font_size=18, buff=0.16).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The value of a statistical life comes from willingness to pay, and that depends on what people can pay. "
            "<bookmark mark='a'/>Agencies that need a value for a country without its own studies transfer the "
            "American figure, scaled by relative income raised to an elasticity epsilon. "
            "<bookmark mark='b'/>With epsilon one, a country with a fifth of American income gets two point four "
            "million dollars; a twentieth, six hundred thousand; a fiftieth, two hundred and forty thousand. With an "
            "elasticity of one point two, the last falls to a hundred and ten thousand. <bookmark mark='c'/>In a "
            "global cost-benefit analysis, then, a life in the poorest country counts a fiftieth as much as an "
            "American's. When a chapter of an IPCC report did this arithmetic in 1995, valuing statistical lives in "
            "poor countries at a fraction of those in rich ones, it was widely condemned. <bookmark mark='d'/>Weight each dollar by one over "
            "the income of the person whose dollar it is, as diminishing marginal utility recommends, and with "
            "epsilon one the weighting undoes the scaling exactly: one life, one value."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(c) for row in grid.cell for c in row])
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
            vo.wait_until("d")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def critics(self):
        head = label(r"Against pricing", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"incommensurability", r"Anderson, \ \textit{Value in Ethics and Economics} \ (1993): \ some goods "
                                        r"are degraded by being priced", RISK),
                (r"whose willingness?", r"willingness to pay rises with income: \ the poor are priced low because "
                                        r"they are poor", BAD),
                (r"equity weights", r"weight benefits by $1/\text{income}$, \ as the logarithm of Part 35's pond "
                                    r"implies", WELL),
                (r"the defence", r"we price lives implicitly whenever we set a speed limit; \ better to do it in the "
                                 r"open, \ consistently", MONEY)]
        g = rows_table(rows, top=1.6, gap=0.48, width=8.2, x_text=-2.0)
        with self.voiceover(
            "The practice has critics too. <bookmark mark='a'/>Elizabeth Anderson argued in Value in Ethics and "
            "Economics, of 1993, that some goods are degraded by being priced at all. <bookmark mark='b'/>And "
            "willingness to pay rises with income, so a method built on it prices the poor low because they are "
            "poor. <bookmark mark='c'/>The equity weighting of the last section is one answer: count each dollar of "
            "benefit by one over the income of the person who receives it, exactly what Part 35's logarithmic "
            "welfare implied. "
            "<bookmark mark='d'/>The defence of pricing is simple. We already price lives whenever we set a speed "
            "limit or a budget; it is better to do it in the open, and consistently."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
