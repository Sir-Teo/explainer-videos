from __future__ import annotations

from videos.economics.econ5.common import *  # noqa: F403

DOMAINS = ("risk", "time", "social", "food")


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 13, r"Frontier: \ random utility and machines that choose", r"What if the same person chooses "
             r"differently twice, or the chooser is a machine?", "Chapter thirteen. Frontier: random utility and "
             "machines that choose.", lit=("households", "firms"), scale=("person", "market"))
        self.random_utility()
        self.big_data()
        self.machines()
        self.open()

    def random_utility(self):
        r = load("repeat")
        ax = goods_axes(center=LEFT * 3.0 + DOWN * 0.25, top=7, ticks=(0, 2, 4, 6), x_length=5.0, y_length=5.0)
        a = ax.ax
        A, B = r["line"]
        ln = budget_line(ax, A, B)
        dots = VGroup(*[Dot(a.c2p(*x), radius=0.07, color=WHO["bo"], fill_opacity=0.7) for x in r["X"]])
        rows = VGroup(
            label(r"Bo on the same line, \ forty times", font_size=24, color=WHO["bo"]),
            label(rf"share on fish: \ {100 * r['mean_share']:.0f}\% on average, \ give or take {100 * r['sd']:.0f}",
                  font_size=22),
            label(r"strict GARP calls every wobble a contradiction", font_size=22, color=VIOL),
            label(r"random utility: \ a probability for each choice, \\ from a population of rankings \\ (Block and "
                  r"Marschak, 1960; \ McFadden, 1974)", font_size=22, color=E.ACCENT),
            label(r"its own revealed-preference test: \ McFadden and \\ Richter (1990); \ made usable on survey data "
                  r"\\ by Kitamura and Stoye (2018)", font_size=21, color=PASS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.4)
        tag = island_tag(r"simulated: Bo, 40 trips on the first Play-it line", corner=DR, font_size=13)
        with self.voiceover(
            "The frontier starts with an awkward fact. <bookmark mark='a'/> Give Bo the same budget forty times, and "
            "he won't choose the same bundle forty times. <bookmark mark='b'/> He spends about sixty percent on fish, "
            "give or take seven points. <bookmark mark='c'/> A strict test of consistency treats every wobble as a "
            "contradiction. But people aren't machines, and two choices from the same budget can both be sincere. "
            "<bookmark mark='d'/> Random utility models choice as a probability: each choice drawn from a "
            "population of possible rankings. Henry Block and Jacob Marschak set it out in 1960, and McFadden "
            "turned it into the logit models of the last chapter. <bookmark mark='e'/> It has its own "
            "revealed-preference test, found by McFadden and Marcel Richter, and since 2018 Yuichi Kitamura and "
            "Jörg Stoye have shown how to run it on ordinary household surveys, where each household is seen only "
            "once."
        ) as vo:
            self.play(FadeIn(ax), Create(ln), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.05), run_time=2.0)
            for mk, rr in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(rr, shift=RIGHT * 0.15))
        self.clear_scene()

    def big_data(self):
        cards = VGroup(
            history_card(r"2011", r"Echenique, Lee and Shum: \ the money pump index",
                         r"how much money could be pumped out of a household through its own cycles: a severity "
                         r"measure for real shopping data", color=VIOL, width=4.15, font_size=20),
            history_card(r"2016", r"Dean and Martin: \ the minimum cost index",
                         r"the cheapest way to break every cycle: in scanner data, violations are common, but cheap",
                         color=E.ACCENT, width=4.15, font_size=20),
            history_card(r"2009", r"Bernheim and Rangel: \ welfare without consistency",
                         r"when choices conflict, keep only the comparisons every choice agrees on", color=PASS,
                         width=4.15, font_size=20),
        ).arrange(RIGHT, buff=0.25, aligned_edge=UP).move_to(UP * 0.35)
        head = label(r"Revealed preference in real data", font_size=32).to_edge(UP, buff=0.45)
        foot = label(r"the question moved from \emph{is anyone rational?} \ to \ \emph{how much does it cost them "
                     r"not to be?}", font_size=24, color=E.ACCENT).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"JPE 119(6) (2011); REStat 98(3) (2016); QJE 124(1) (2009)", corner=DR, font_size=12)
        with self.voiceover(
            "In real shopping data, with thousands of goods and prices that change every week, almost every "
            "household violates GARP somewhere. So the frontier measures how much it matters. "
            "<bookmark mark='a'/> In 2011 Federico Echenique, Sangmok Lee and Matthew Shum asked how much money a "
            "clever trader could pump out of a household through its own cycles. <bookmark mark='b'/> In 2016 Mark "
            "Dean and Daniel Martin measured the cheapest way to break every cycle, and found that in supermarket "
            "scanner data violations are common, but cheap. <bookmark mark='c'/> And when choices do conflict, "
            "Douglas Bernheim and Antonio Rangel proposed keeping only the comparisons on which all of a person's "
            "choices agree. <bookmark mark='d'/> The question has moved from whether anyone is rational to how much "
            "it costs them not to be."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c_ in zip("abc", cards):
                vo.wait_until(mk)
                self.play(FadeIn(c_, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def machines(self):
        g = tables.CHEN_2023.data
        from explainer.ai.viz import axes

        ax = axes([0, 4], [0.9, 1.0], x_length=6.0, y_length=4.0, xticks=None, yticks=[0.9, 0.95, 1.0],
                  ylabel=r"mean efficiency index", font_size=18, center=LEFT * 2.8 + DOWN * 0.3)
        a = ax.ax
        bars = VGroup()
        for k, d in enumerate(DOMAINS):
            for j, (who, col) in enumerate((("humans", IC), ("gpt", E.ACCENT))):
                v = g[who][d]
                r = Rectangle(width=0.34, height=a.c2p(0, v)[1] - a.c2p(0, 0.9)[1], stroke_width=0, fill_color=col,
                              fill_opacity=0.9).move_to(a.c2p(k + 0.32 + 0.36 * j, 0.9), aligned_edge=DOWN)
                bars.add(r)
            bars.add(label(d, font_size=18, color=GREY_B).next_to(a.c2p(k + 0.5, 0.9), DOWN, buff=0.12))
        key = VGroup(Square(0.2, stroke_width=0, fill_color=IC, fill_opacity=0.9),
                     label(r"people", font_size=19, color=IC),
                     Square(0.2, stroke_width=0, fill_color=E.ACCENT, fill_opacity=0.9),
                     label(r"GPT", font_size=19, color=E.ACCENT)).arrange(RIGHT, buff=0.12).next_to(ax, UP, buff=0.1)
        rows = VGroup(
            label(r"Chen, Liu, Shan and Zhong (2023): \\ budgets for risk, time, sharing and food", font_size=22),
            label(rf"GPT: \ {g['gpt']['risk']:.3f}, {g['gpt']['time']:.3f}, {g['gpt']['social']:.3f}, "
                  rf"{g['gpt']['food']:.3f}", font_size=22, color=E.ACCENT),
            label(rf"their human subjects: \ {g['humans']['risk']:.3f} to {g['humans']['time']:.3f}", font_size=22,
                  color=IC),
            label(r"but its scores shift with the wording: \\ how you ask changes how consistent it is",
                  font_size=22, color=VIOL),
            label(r"consistency is cheap for a machine; \\ whose wants it reveals is the open question", font_size=22,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        tag = published_tag(r"Chen, Liu, Shan and Zhong, PNAS 120(51) (2023); arXiv 2305.12763", corner=DR,
                            font_size=12)
        with self.voiceover(
            "And now the choosers include machines. <bookmark mark='a'/> In 2023 Yiting Chen, Tracy Xiao Liu, You "
            "Shan and Songfa Zhong gave GPT the same kinds of budgets people get: for risk, for time, for sharing "
            "with others, and for food. <bookmark mark='b'/> Its efficiency index was 0.997 or higher in every "
            "domain. <bookmark mark='c'/> Their human subjects scored between 0.96 and 0.985. <bookmark mark='d'/> "
            "But its scores moved with the wording of the question: how you ask changes how consistent it looks. "
            "<bookmark mark='e'/> For a machine, consistency comes cheap. The harder "
            "question, as these systems begin to shop and book and bargain for people, is whose wants their "
            "choices reveal."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(key), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bars], lag_ratio=0.08), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def open(self):
        b = load("bronars")
        items = point_cards([
            (r"not known", r"how to tell a sincere change of mind \\ from a mistake, \ with few choices per person",
             VIOL),
            (r"not known", r"whether consistency in a laboratory \\ causes better outcomes outside it, \ or only "
                           r"\\ travels with them", VIOL),
            (r"the tools", r"Afriat's LP; \ power against random choice; \\ random-utility tests on surveys",
             E.ACCENT),
            (r"$\bigstar$ \ research problem", rf"design the most powerful eleven budgets: \\ ours catch "
                                               rf"{100 * b['power']:.1f}\% of random choosers; \ can you beat it?",
             PASS),
        ], width=12.6, cols=2, font_size=21).move_to(UP * 0.2)
        head = label(r"What is not known", font_size=34).to_edge(UP, buff=0.4)
        with self.voiceover(
            "What is not known? <bookmark mark='a'/> How to tell a sincere change of mind from a mistake, when we "
            "see each person choose only a few times. <bookmark mark='b'/> Whether being consistent in a laboratory "
            "game makes people wealthier, or only goes with whatever does. <bookmark mark='c'/> The tools are the "
            "ones in this part: Afriat's linear programme, power against random choice, and random-utility tests. "
            f"<bookmark mark='d'/> And a research problem you can start today. Our eleven lines catch "
            f"{100 * b['power']:.1f} percent of random choosers. Which eleven budgets catch the most, and do they "
            "also catch small inefficiencies in people who are nearly consistent? The problem set says where to "
            "begin."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c_ in zip("abcd", items.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c_, shift=UP * 0.1))
        self.clear_scene()
