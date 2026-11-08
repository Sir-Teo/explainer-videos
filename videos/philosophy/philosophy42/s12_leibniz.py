from __future__ import annotations

from videos.philosophy.philosophy42.common import *  # noqa: F403


class Leibniz(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"Calculemus, again", r"What came of Leibniz's dream?", lit=(1685, 1931), part=PART)
        with self.voiceover("Chapter eleven. Calculemus, again."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.quote()
        self.history()
        self.stats()
        self.achieved()
        self.never()
        self.journey()

    def quote(self):
        q = quote_card(r"The only way to rectify our reasonings is to make them as tangible as those of the "
                       r"mathematicians, so that we can find our error at a glance, and when there are disputes among "
                       r"persons, we can simply say: let us calculate, without further ado, to see who is right.",
                       r"Leibniz, \textit{The Art of Discovery} (1685)", r"trans.\ Wiener, \textit{Leibniz: "
                       r"Selections} (1951)", width=11.2, font_size=28).move_to([0, 0.5, 0])
        cal = label(r"\textit{calculemus}", font_size=60, color=GOAL).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The series began with these words. <bookmark mark='a'/>Leibniz hoped that every dispute could be "
            "settled the way a sum is checked: let us calculate, calculemus. <bookmark mark='b'/>Forty two parts "
            "later, we can say what came of the dream."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            self.play(FadeIn(cal, scale=1.2))
            vo.wait_until("b")
            self.wait(0.5)
        self.clear_scene()

    def stats(self):
        d = load("reasoner")
        assert d["modules"] == 47 and d["tests"] == 271 and 23_500 < d["lines"] < 24_500 and d["functions"] > 1000
        head = label(r"The Reasoner, \ by the numbers", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        nums = VGroup()
        for v, t, c in ((d["modules"], r"modules", ROBOT), (d["lines"], r"lines of code", TRUEV),
                        (d["functions"], r"public functions", LOBC), (d["tests"], r"tests", HUMAN)):
            n = label(f"{v:,}", font_size=56, color=c)
            nums.add(VGroup(n, label(t, font_size=22, color=GREY_A).next_to(n, DOWN, buff=0.15)))
        nums.arrange(RIGHT, buff=1.1).next_to(head, DOWN, buff=0.6)
        names = VGroup(*[label(rf"\texttt{{{nm}}}", font_size=17, color=GREY_B) for nm in d["names"]])
        names.arrange_in_grid(cols=8, buff=(0.35, 0.22)).next_to(nums, DOWN, buff=0.6)
        if names.width > 13:
            names.width = 13
        with self.voiceover(
            "First, what was built. <bookmark mark='a'/>The Reasoner now has forty seven modules: some twenty four "
            "thousand lines of code, more than a thousand public functions, and two hundred and seventy one tests "
            "that check its results. <bookmark mark='b'/>It decides arguments in propositional and first-order "
            "logic, checks modal frames, does Bayesian updating, causal inference and decision theory, counts "
            "votes, divides cakes, audits fairness, and now solves the off-switch game. The numerical results in this "
            "series' worked models were computed by it and can be computed again."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(n, shift=UP * 0.2) for n in nums], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(n0) for n0 in names], lag_ratio=0.03), run_time=3)
        self.clear_scene()

    def achieved(self):
        head = label(r"What calculation achieved", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"logic", r"SAT solvers decide arguments with millions of variables; \ proof assistants have checked Gödel's theorems \ (Parts 2, \ 7)", LOBC),
                (r"belief", r"probability became the logic of uncertain reasoning, \ and causal inference a calculus \ (Parts 13--17)", HUMAN),
                (r"society", r"voting, \ fair division and matching are engineered with theorems \ (Parts 38, \ 39)", TRUEV),
                (r"machines", r"the dream built reasoners that write, \ prove and plan, \ and now must be aligned \ (Parts 30, \ 42)", ROBOT)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The dream achieved more than Leibniz could have imagined. <bookmark mark='a'/>Satisfiability solvers "
            "decide arguments with millions of variables, and proof assistants have checked Gödel's theorems line by "
            "line. <bookmark mark='b'/>Probability became the logic of uncertain reasoning, and causal inference a "
            "calculus with its own rules. <bookmark mark='c'/>Voting rules, fair division and the matching of "
            "students to schools are now engineered with theorems. <bookmark mark='d'/>And the dream built machines "
            "that write, prove and plan, which is why the question of this part became urgent."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def never(self):
        head = label(r"What it never will", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"axioms", r"which axioms to adopt, \ which logic to use \ (Parts 5, \ 6)", LOBC),
                (r"priors", r"which prior, \ which inductive bias \ (Parts 13, \ 15)", HUMAN),
                (r"principles", r"which aggregation, \ which fairness, \ which theory of the good \ (Parts 35--41)", PROXYC),
                (r"values", r"what to want \ (Parts 37, \ 42)", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "And the Wall shows what it never will. <bookmark mark='a'/>Calculation cannot choose its own axioms, or "
            "its logic. <bookmark mark='b'/>It cannot choose its priors, or the inductive bias that makes learning "
            "possible. <bookmark mark='c'/>It cannot choose among aggregation rules, kinds of fairness, or theories "
            "of the good, though it can price each one exactly. <bookmark mark='d'/>And it cannot choose what to "
            "want. Leibniz's dream was half right. When we disagree, we should calculate, and we will find out "
            "precisely where the disagreement lies. Then we must still decide."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def journey(self):
        m = series_map(done=42)
        with self.voiceover(
            "This was the journey. <bookmark mark='a'/>From the laws of thought and the limits of proof, through "
            "knowledge, probability and science, to what there is, to mind and meaning, to action, ethics, justice "
            "and beauty, and finally to the reasoners we build. Forty two parts, each a question, a calculation, and "
            "a wall. <bookmark mark='b'/>The questions are older than any machine, and they are not finished. The "
            "machines make them sharper, and more urgent."
        ) as vo:
            self.play(FadeIn(m))
            vo.wait_until("a")
            self.play(LaggedStart(*[Indicate(c, color=P.CONCL, scale_factor=1.03) for c in m.cols], lag_ratio=0.25),
                      run_time=4)
            vo.wait_until("b")
            self.wait(0.5)
        self.clear_scene()

    def history(self):
        head = label(r"The dream, \ from Leibniz to the Reasoner", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Boole \ (1854)", r"\textit{The Laws of Thought}: \ reasoning as algebra \ (Part 2)", LOBC),
                (r"Frege \ (1879)", r"a formal language for all of mathematics \ (Part 3)", HUMAN),
                (r"Hilbert, \ Gödel, \ Turing \ (1928--1936)", r"the decision problem posed and answered: \ no machine decides all of logic \ (Parts 3, \ 7)", RISK),
                (r"Davis, \ Putnam, \ Robinson \ (1960--1965)", r"the first practical proof procedures: \ the ancestors of the Reasoner \ (Part 2)", TRUEV)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The dream had a history between Leibniz and us. <bookmark mark='a'/>In 1854 George Boole turned "
            "reasoning into algebra, in The Laws of Thought, the subject of Part 2. <bookmark mark='b'/>In 1879 "
            "Gottlob Frege built a formal language in which all of mathematics could be written, the logic of Part 3. "
            "<bookmark mark='c'/>David Hilbert asked for a procedure that would decide every question of logic, and "
            "Gödel and Turing showed, by 1936, that there could be none: the first bricks of the Wall, in Parts 3 and "
            "7. <bookmark mark='d'/>And Martin Davis, Hilary Putnam and Alan Robinson built the first practical proof "
            "procedures, the ancestors of the satisfiability solver at the core of the Reasoner. Leibniz's dream was "
            "refuted in its strongest form, and realized in every weaker one."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
