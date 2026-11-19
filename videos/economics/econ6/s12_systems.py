from __future__ import annotations

from videos.economics.econ6.common import *  # noqa: F403


class Systems(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Demand systems you can estimate", r"How do economists measure a whole set of demands at "
             r"once, and when does a population act like one consumer?", "Chapter ten. Demand systems you can "
             "estimate.", scale=("household", "nation"))
        self.history()
        self.aids()
        self.island()
        self.gorman()

    def history(self):
        cards = VGroup(
            history_card(r"1954", r"Richard Stone: \ the linear expenditure system",
                         r"committed quantities first, then fixed shares of what's left: fitted to Britain's "
                         r"spending", color=IC, width=4.2, font_size=21),
            history_card(r"1980", r"Angus Deaton and John Muellbauer: \ an almost ideal demand system",
                         r"budget shares linear in log prices and log real income; flexible, and its restrictions "
                         r"can be tested", color=HICKS, width=4.2, font_size=21),
            history_card(r"1953", r"W.\ M.\ Gorman: \ when is a society one consumer?",
                         r"only if every household's Engel curves are straight and parallel", color=E.ACCENT,
                         width=4.2, font_size=21),
        ).arrange(RIGHT, buff=0.3, aligned_edge=UP).move_to(UP * 0.2)
        head = label(r"From theory to equations that fit data", font_size=34).to_edge(UP, buff=0.5)
        foot = label(r"Stone won the Nobel prize in 1984, \ Deaton in 2015", font_size=23, color=GREY_A).to_edge(
            DOWN, buff=0.7)
        with self.voiceover(
            "To use any of this, economists need demand equations they can fit to data, for many goods at once, "
            "that respect the theory. <bookmark mark='a'/> In 1954 Richard Stone fitted the linear expenditure "
            "system to Britain's spending: households first buy committed quantities of each good, then split "
            "what's left in fixed shares. <bookmark mark='b'/> In 1980 Angus Deaton and John Muellbauer proposed "
            "the almost ideal demand system, which became the workhorse: budget shares that are linear in log "
            "prices and log real income, flexible enough to fit, with the restrictions of chapter six written as "
            "conditions you can test. <bookmark mark='c'/> And behind both, a question W. M. Gorman answered in "
            "1953: when can a whole society's spending be treated as one consumer's? <bookmark mark='d'/> Stone "
            "received the Nobel prize in 1984, and Deaton in 2015."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c_ in zip("abc", cards):
                vo.wait_until(mk)
                self.play(FadeIn(c_, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def aids(self):
        eq = MathTex(r"w_i", r"=", r"\alpha_i", r"+", r"\sum_j \gamma_{ij}\log p_j", r"+",
                     r"\beta_i \log\frac{m}{P(p)}", font_size=56).to_edge(UP, buff=0.9)
        eq[4].set_color(SUB)
        eq[6].set_color(HICKS)
        notes = VGroup(
            label(r"$w_i$: \ the share of the budget on good $i$", font_size=26),
            label(r"$\gamma_{ij}$: \ how shares respond to prices", font_size=26, color=SUB),
            label(r"$\beta_i$: \ to real income: \ $\beta_i < 0$ a necessity, \ $\beta_i > 0$ a luxury", font_size=26,
                  color=HICKS),
            label(r"homogeneity: \ $\sum_j \gamma_{ij} = 0$; \quad symmetry: \ $\gamma_{ij} = \gamma_{ji}$",
                  font_size=26, color=E.ACCENT),
            label(r"each a linear restriction, \ so each can be tested", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(eq, DOWN, buff=0.7)
        with self.voiceover(
            "Here is the almost ideal demand system for one good. <bookmark mark='a'/> The share of the budget "
            "spent on it is a constant, <bookmark mark='b'/> plus terms in the logs of every price, "
            "<bookmark mark='c'/> plus a term in the log of real income. A negative coefficient on income makes "
            "the good a necessity, whose share falls as people get richer, Engel's food; a positive one, a "
            "luxury. <bookmark mark='d'/> Homogeneity says each good's price coefficients add to zero, and symmetry "
            "says the coefficient of fish's price in the coconut equation equals that of coconuts' price in the "
            "fish equation. <bookmark mark='e'/> Each is a linear restriction on the coefficients, so each can be "
            "tested."
        ) as vo:
            self.play(Write(eq), run_time=1.8)
            vo.wait_until("a")
            self.play(Indicate(eq[0:3], color=E.ACCENT), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Indicate(eq[4], color=SUB), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Indicate(eq[6], color=HICKS), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
            vo.wait_until("e")
            self.play(FadeIn(notes[4]))
        self.clear_scene()

    def island(self):
        sv = load("survey")
        goods = sv["goods"]
        T, Est = np.array(sv["truth"]["marshall"]), np.array(sv["symmetry"]["marshall"])
        ti, ei = np.array(sv["truth"]["income"]), np.array(sv["symmetry"]["income"])
        head_cells = [label(r"", font_size=20)] + [label(rf"price of {g}", font_size=22, color=GREY_A) for g in goods] + \
                     [label(r"income", font_size=22, color=HICKS)]
        cells = list(head_cells)
        for i, g in enumerate(goods):
            cells.append(label(g, font_size=24, color=[FISHC, COCO, GREY_A][i]))
            for j in range(3):
                col = E.ACCENT if i == j else WHITE
                cells.append(VGroup(label(rf"{Est[i, j]:+.2f}", font_size=25, color=col),
                                    label(rf"planted {T[i, j]:+.2f}", font_size=16, color=GREY_B)).arrange(
                    DOWN, buff=0.04))
            cells.append(VGroup(label(rf"{ei[i]:.2f}", font_size=25, color=HICKS),
                                label(rf"planted {ti[i]:.2f}", font_size=16, color=GREY_B)).arrange(DOWN, buff=0.04))
        tab = VGroup(*cells).arrange_in_grid(rows=4, cols=5, buff=(0.55, 0.35)).move_to(LEFT * 1.6 + DOWN * 0.2)
        tests = sv["none"]["tests"]
        side = VGroup(
            label(rf"{sv['n']:,} households".replace(",", "{,}"), font_size=26),
            label(rf"20 villages $\times$ 12 months \\ of prices", font_size=22, color=GREY_A),
            label(r"fitted with symmetry imposed", font_size=22, color=GREY_A),
            label(rf"homogeneity: \ $p = {tests['homogeneity']['p']:.2f}$", font_size=25, color=E.ACCENT),
            label(rf"symmetry: \ $p = {tests['symmetry']['p']:.2f}$", font_size=25, color=E.ACCENT),
            label(r"the Island's households \\ pass both, \ as planted", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.4)
        head = label(r"price and income elasticities from the Island's survey", font_size=30).to_edge(UP, buff=0.45)
        tag = island_tag(r"simulated: a planted AIDS, estimated by iterated least squares", corner=DR, font_size=13)
        with self.voiceover(
            "On the Island we can watch the system work. <bookmark mark='a'/> Six thousand households in twenty "
            "villages, surveyed over twelve months, buy fish, coconuts and cloth at prices that differ from village "
            "to village and month to month for reasons of supply, such as storms and harvests, not of demand: Part "
            "four's identification problem, solved by design. Their shares come from an almost ideal demand "
            "system we planted. <bookmark mark='b'/> Fitted by iterated least squares, the estimated elasticities "
            "land on the planted ones to about the second decimal: coconuts inelastic at minus nought point seven "
            "two, cloth a luxury with an income elasticity near one and a half. <bookmark mark='c'/> And the "
            "tests: homogeneity and symmetry are not rejected, as they shouldn't be. <bookmark mark='d'/> When "
            "Deaton and Muellbauer fitted the system to Britain's spending from 1954 to 1974, homogeneity was "
            "rejected. They suspected not irrational consumers but a model too simple for aggregate data that "
            "move slowly over time, and that's been the debate ever since."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]), FadeIn(tab), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[2]), Indicate(tab[2 * 5 + 2], color=E.ACCENT), Indicate(tab[3 * 5 + 4], color=HICKS))
            vo.wait_until("c")
            self.play(FadeIn(side[3]), FadeIn(side[4]), FadeIn(side[5]))
            vo.wait_until("d")
            self.play(Indicate(side[3], color=GIFF))
        self.clear_scene()

    def gorman(self):
        from explainer.ai.viz import axes

        panels = VGroup()
        for k, (title, s1, s2, col) in enumerate(((r"parallel: \ the Gorman form", 0.10, 0.10, HICKS),
                                                  (r"different slopes", 0.04, 0.16, GIFF))):
            ax = axes([0, 100], [0, 16], x_length=4.6, y_length=3.8, xticks=[0, 50, 100], yticks=[0, 5, 10, 15],
                      xlabel=r"income", ylabel=r"fish", font_size=16, center=(LEFT if k == 0 else RIGHT) * 3.3 +
                      DOWN * 0.2)
            a = ax.ax
            l1 = Line(a.c2p(0, 2), a.c2p(100, 2 + 100 * s1), color=IC, stroke_width=4)
            l2 = Line(a.c2p(0, 0.5), a.c2p(100, 0.5 + 100 * s2), color=E.ACCENT, stroke_width=4)
            names = VGroup(label(r"Ana", font_size=18, color=IC).next_to(l1.get_end(), RIGHT, buff=0.08),
                           label(r"Chidi", font_size=18, color=E.ACCENT).next_to(l2.get_end(), RIGHT, buff=0.08))
            # move $20 from Chidi (at 60) to Ana (at 40)
            d1 = Arrow(a.c2p(40, 2 + 40 * s1), a.c2p(60, 2 + 60 * s1), color=WHITE, buff=0, stroke_width=3,
                       max_tip_length_to_length_ratio=0.25)
            d2 = Arrow(a.c2p(60, 0.5 + 60 * s2), a.c2p(40, 0.5 + 40 * s2), color=WHITE, buff=0, stroke_width=3,
                       max_tip_length_to_length_ratio=0.25)
            change = 20 * s1 - 20 * s2
            res = label(rf"move \$20 from Chidi to Ana: \\ fish bought change by {change:+.1f}", font_size=20,
                        color=col).next_to(ax, DOWN, buff=0.15)
            t = label(title, font_size=24, color=col).next_to(ax, UP, buff=0.15)
            panels.add(VGroup(ax, l1, l2, names, d1, d2, res, t))
        foot = label(r"a representative consumer exists only when redistribution can't move total demand",
                     font_size=24, color=E.ACCENT).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Gorman's question is worth a picture, because Part five's test treated all of America as one "
            "consumer. <bookmark mark='a'/> Here are two islanders' Engel curves for fish. If they are straight and "
            "parallel, moving twenty dollars from Chidi to Ana changes nothing: Ana buys exactly the fish Chidi "
            "gives up. Total demand then depends only on total income, and the society behaves like one consumer. "
            "<bookmark mark='b'/> If the slopes differ, the same transfer changes how much fish is bought in total. "
            "Then there's no single consumer whose demand is the market's, and welfare calculations for a "
            "representative consumer can mislead. <bookmark mark='c'/> Real Engel curves are rarely parallel; "
            "that's one reason the frontier works with household data."
        ) as vo:
            head = label(r"Gorman (1953): \ when is a society one consumer?", font_size=32,
                         color=E.ACCENT).to_edge(UP, buff=0.3)
            self.play(FadeIn(head), FadeIn(panels[0][0]), FadeIn(panels[1][0]), FadeIn(panels[0][7]),
                      FadeIn(panels[1][7]))
            vo.wait_until("a")
            self.play(FadeIn(panels[0][1:7]))
            vo.wait_until("b")
            self.play(FadeIn(panels[1][1:7]))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
