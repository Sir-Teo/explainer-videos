from __future__ import annotations

from videos.philosophy.philosophy19.common import *  # noqa: F403


class Kin(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"Kin selection", r"How can self-sacrifice evolve?", lit=(1964, 1975), part=PART)
        with self.voiceover("Chapter five. Kin selection."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.puzzle()
        self.rule()
        self.sims()
        self.haplo()

    def puzzle(self):
        head = label(r"Darwin's difficulty", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"the puzzle", r"sterile worker ants, \ alarm calls that draw predators, \ vampire bats sharing blood", BAD),
            (r"Darwin \ (1859)", r"`one special difficulty, \ which at first appeared to me insuperable, \ and "
                                 r"actually fatal to my whole theory'", GREY_A),
            (r"the naive answer", r"`for the good of the species': \ but a cheat in a group of altruists out-breeds "
                                  r"them", BAD),
            (r"Haldane", r"`I would lay down my life for two brothers or eight cousins'", ORG),
            (r"Hamilton \ (1964)", r"a gene for helping spreads if it helps copies of itself in relatives", OK),
        ]
        g = rows_table(rows, top=1.6, gap=0.45, width=8.6, x_text=-2.6)
        with self.voiceover(
            "Self-sacrifice is the great puzzle for natural selection. <bookmark mark='a'/>Worker ants are sterile; "
            "ground squirrels give alarm calls that draw predators to themselves; vampire bats regurgitate blood for "
            "hungry roostmates. <bookmark mark='b'/>Darwin called the sterile castes of insects one special "
            "difficulty, which at first appeared to him insuperable and actually fatal to his whole theory. "
            "<bookmark mark='c'/>The naive answer, that animals act for the good of the species, fails: a cheat in a "
            "group of altruists takes the benefits, pays no costs, and out-breeds them. <bookmark mark='d'/>J. B. S. "
            "Haldane is said to have quipped that he would lay down his life for two brothers or eight cousins. "
            "<bookmark mark='e'/>In 1964 William Hamilton made the quip exact."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def rule(self):
        d = load("kin")["price"]
        hc = history_card(1964, r"William Hamilton", r"`The Genetical Evolution of Social Behaviour'", width=6.8,
                          color=HIST).to_corner(UL, buff=0.3)
        rule = MathTex(r"r\,b \;>\; c", font_size=60, color=GOAL).next_to(hc, DOWN, buff=0.5).set_x(-2.8)
        gl = stack([(r"$c$: \ cost to the actor", SELF), (r"$b$: \ benefit to the recipient", ALT),
                    (r"$r$: \ relatedness: \ $\tfrac12$ for siblings, \ $\tfrac18$ for cousins", GENE)], font_size=20,
                   aligned_edge=LEFT).next_to(rule, DOWN, buff=0.4).set_x(-2.8)
        der = VGroup(
            label(r"from Price, \ for pairs with relatedness $r$:", font_size=20, color=WHITE),
            MathTex(r"\mathrm{cov}(w, z) = p(1 - p)\,(r b - c)", font_size=30, color=ORG),
            label(r"the Reasoner, \ enumerating the four pair types \ ($r = 0.5$, \ $b = 3$, \ $c = 1$, \ $p = 0.3$):",
                  font_size=18, color=GREY_A),
            MathTex(r"\mathrm{cov} = " + f"{d['cov']:.4f}" + r", \quad p(1-p)(rb - c) = " + f"{d['formula']:.4f}",
                    font_size=26, color=OK),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([3.0, -0.4, 0])
        if der.width > 6.6:
            der.width = 6.6
        with self.voiceover(
            "Hamilton's rule says that a gene for helping spreads when r b is greater than c. "
            "<bookmark mark='a'/>c is the cost to the helper in offspring; b is the benefit to the recipient; and r "
            "is their relatedness, the extra chance that the recipient carries the same gene: one half for "
            "siblings, one eighth for cousins. Two brothers or eight cousins, exactly. <bookmark mark='b'/>The rule "
            "falls out of the Price equation. For partners whose types are correlated with relatedness r, the "
            "covariance between carrying the gene and fitness is p times one minus p times r b minus c. "
            "<bookmark mark='c'/>The Reasoner enumerates the four kinds of pair and gets the same number both ways. "
            "Selection favours helping exactly when r b exceeds c."
        ) as vo:
            self.play(FadeIn(hc), Write(rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in gl], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(der[0]), Write(der[1]))
            vo.wait_until("c")
            self.play(FadeIn(der[2]), Write(der[3]))
        self.clear_scene()

    def sims(self):
        d = load("kin")["sims"]
        head = label(r"Altruism among relatives, \ simulated", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        G = len(d[0]["traj"])
        ax = Axes(x_range=[0, G - 1, 10], y_range=[0, 1, 0.25], x_length=6.6, y_length=4.0,
                  axis_config={"color": GREY_B, "font_size": 18, "include_numbers": True}).move_to([-2.4, -0.3, 0])
        cols = [OK, BAD, GENE, SELF]
        curves = VGroup(*[series_plot(ax, s["traj"], c, width=4) for s, c in zip(d, cols)])
        xl = label(r"generation", font_size=18, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        yl = label(r"share of altruists", font_size=18, color=GREY_A).next_to(ax, UP, buff=0.1)
        side = stack([(r"$r = " + f"{s['r']:g}" + r"$, \ $b = " + f"{s['b']:g}" + r"$, \ $c = " + f"{s['c']:g}" +
                       r"$: \ $rb - c = " + f"{s['rb_minus_c']:+.2f}" + r"$", c) for s, c in zip(d, cols)] +
                     [(r"4{,}000 pairs a generation; \ the rule's sign decides", GREY_A),
                      (r"cousins need $b > 8c$", GOAL)], font_size=20, aligned_edge=LEFT, width=5.2).move_to(
            [4.2, -0.2, 0])
        with self.voiceover(
            "Now run it. <bookmark mark='a'/>Four thousand pairs per generation, starting with a fifth of the "
            "population altruistic. Between siblings, with a benefit three times the cost, r b minus c is positive, "
            "and altruism sweeps to fixation. <bookmark mark='b'/>With the same benefit between half-siblings, at "
            "relatedness a quarter, r b minus c is negative, and altruism vanishes. <bookmark mark='c'/>Between "
            "cousins, at relatedness one eighth, the benefit must exceed eight times the cost: at ten times it "
            "spreads; <bookmark mark='d'/>at six times it dies out. The sign of r b minus c decides, as the "
            "algebra said."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(side[4]))
            for mk, i in zip("abcd", range(4)):
                vo.wait_until(mk)
                self.play(Create(curves[i]), FadeIn(side[i]), run_time=1.5)
            self.play(FadeIn(side[5]))
        self.clear_scene()

    def haplo(self):
        d = load("relatedness")["rows"]
        head = label(r"Relatedness, \ counted gene by gene", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        eq = MathTex(r"r_{A \to B} = \frac{P(\text{gene of } A \equiv \text{gene of } B)}"
                     r"{P(\text{gene of } B \equiv \text{gene of } B)}", font_size=32, color=GENE).next_to(
            head, DOWN, buff=0.3)
        hd = [r"\text{pair}", r"r"]
        names = list(d)
        rows = []
        for n in names:
            v = d[n]
            col = GOAL if v == 0.75 else (BAD if v == 0.25 else WHITE)
            rows.append([MathTex(r"\text{" + n + "}", font_size=22, color=col),
                         MathTex({0.5: r"1/2", 0.25: r"1/4", 0.75: r"3/4"}.get(v, f"{v:g}"), font_size=24,
                                 color=col)])
        grid = ValueGrid(hd, rows, col_w=[4.7, 0.9], cell_h=0.48, font_size=20).move_to([-3.9, -0.6, 0])
        side = stack([(r"in bees, \ ants and wasps, \ males come from unfertilized eggs: \ haplodiploidy", WHITE),
                      (r"sisters share their father's whole genome: \ $r = 3/4$, \ more than to their own daughters",
                       GOAL),
                      (r"but only $1/4$ to brothers: \ the advantage cancels, \ unless workers favour sisters", BAD),
                      (r"Trivers and Hare \ (1976): \ workers invest about 3:1 in sisters, \ as predicted", OK),
                      (r"yet termites are diploid and eusocial; \ multiply mated queens dilute $r$", GROUP)],
                     font_size=19, aligned_edge=LEFT, width=7.4, buff=0.3).move_to([2.85, -0.6, 0])
        with self.voiceover(
            "Where does relatedness come from? <bookmark mark='a'/>The Reasoner computes it exactly, by "
            "enumerating Mendel's lotteries: the chance that a gene picked from the actor is identical by descent "
            "with one picked from the recipient, relative to the recipient's own. <bookmark mark='b'/>For full "
            "sisters in a species like ours, the answer is one half; for half-sisters, one quarter. "
            "<bookmark mark='c'/>In bees, ants and wasps, males develop from unfertilized eggs and carry a single "
            "set of genes. <bookmark mark='d'/>So sisters share their father's whole genome, and are related by "
            "three quarters, more than to their own daughters. Hamilton suggested that this is why sterile worker "
            "castes evolved so often in these insects. <bookmark mark='e'/>But a sister is related to her brother "
            "by only a quarter, which cancels the advantage, unless workers invest more in sisters than in brothers. "
            "<bookmark mark='f'/>Robert Trivers and Hope Hare predicted a three-to-one investment ratio in ant "
            "colonies, and found it. <bookmark mark='g'/>Yet termites, which are diploid, are eusocial too, and "
            "queens that mate many times dilute the three quarters: relatedness helps, but it is not the whole "
            "story."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*grid.cell[0])), FadeIn(VGroup(*grid.cell[1])), FadeIn(VGroup(*grid.cell[5])))
            vo.wait_until("c")
            self.play(FadeIn(side[0]))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*grid.cell[2])), FadeIn(side[1]))
            vo.wait_until("e")
            self.play(FadeIn(VGroup(*grid.cell[3])), FadeIn(VGroup(*grid.cell[4])), FadeIn(side[2]))
            vo.wait_until("f")
            self.play(FadeIn(side[3]))
            vo.wait_until("g")
            self.play(FadeIn(side[4]))
        self.clear_scene()
