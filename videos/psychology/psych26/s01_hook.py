from __future__ import annotations

from videos.psychology.psych26.common import *  # noqa: F403


def crowd(n_alive: int, n: int = 600, cols: int = 40, size: float = 0.13, alive=GAIN, dead=GREY_D) -> VGroup:
    """600 people as a grid of small squares, the first ``n_alive`` lit."""
    out = VGroup()
    for k in range(n):
        r, c = divmod(k, cols)
        sq = Square(side_length=size * 0.78, stroke_width=0, fill_opacity=1,
                    fill_color=alive if k < n_alive else dead)
        out.add(sq.move_to([c * size, -r * size, 0]))
    return out


class Hook(VoiceoverScene):
    def construct(self):
        self.on_you()
        self.reveal()
        self.story()
        self.question()
        self.objectives()

    def _programme(self, title, a, b, color):
        head = label(title, font_size=26, color=GREY_A)
        ra = wrapped_label(a, 10.8, 26, SURE)
        rb = wrapped_label(b, 10.8, 26, RISKY)
        return VGroup(head, ra, rb).arrange(DOWN, aligned_edge=LEFT, buff=0.3)

    def on_you(self):
        stage = demo_stage(12.6, 5.6, center=[0, 0.2, 0])
        intro = wrapped_label(r"An unusual disease is expected to kill 600 people. \ Two programmes to fight it "
                              r"have been proposed.", 11.0, 27, WHITE)
        g1 = self._programme(r"Which do you favour?",
                             r"Programme A: \ 200 people will be saved.",
                             r"Programme B: \ a one-third chance that 600 will be saved, \ and a two-thirds chance "
                             r"that no one will be saved.", GAIN)
        VGroup(intro, g1).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, 0.25, 0])
        with self.voiceover(
            "Let's start on you. <bookmark mark='a'/> Imagine that the country is preparing for an unusual disease, "
            "expected to kill six hundred people. Two programmes to fight it have been proposed. <bookmark mark='b'/> "
            "If programme A is adopted, two hundred people will be saved. If programme B is adopted, there's a "
            "one-third chance that all six hundred will be saved, and a two-thirds chance that no one will be "
            "saved. Which do you favour? Decide now, before reading on."
        ) as vo:
            self.play(FadeIn(stage))
            vo.wait_until("a")
            self.play(FadeIn(intro))
            vo.wait_until("b")
            self.play(FadeIn(g1, shift=UP * 0.1))
        self.wait(4.0)
        g2 = self._programme(r"And now?",
                             r"Programme C: \ 400 people will die.",
                             r"Programme D: \ a one-third chance that nobody will die, \ and a two-thirds chance that "
                             r"600 will die.", LOSS)
        g2.move_to(g1, aligned_edge=UL)
        with self.voiceover(
            "Now a second version. <bookmark mark='a'/> Same disease, same six hundred. If programme C is adopted, "
            "four hundred people will die. If programme D is adopted, there's a one-third chance that nobody will "
            "die, and a two-thirds chance that six hundred will die. Which do you favour now?"
        ) as vo:
            vo.wait_until("a")
            self.play(FadeOut(g1), FadeIn(g2, shift=UP * 0.1))
        self.wait(4.0)
        self.clear_scene()

    def reveal(self):
        d = load("framing")
        head = heading(r"Two descriptions, \ one set of outcomes")
        c1 = crowd(200).scale(0.85)
        c2 = crowd(200, alive=GAIN).scale(0.85)
        VGroup(c1, c2).arrange(RIGHT, buff=0.9).move_to([0, 1.0, 0])
        t1 = label(r"A, \ ``200 saved''", font_size=22, color=SURE).next_to(c1, UP, buff=0.15)
        t2 = label(r"C, \ ``400 die''", font_size=22, color=SURE).next_to(c2, UP, buff=0.15)
        same = label(r"$=$", font_size=48).move_to(VGroup(c1, c2).get_center())
        bars_ = VGroup()
        for k, (lab_, n, sure_pct, col) in enumerate([
                (r"lives saved \ (A or B)", d["n_saved"], d["saved_sure_pct"], GAIN),
                (r"deaths \ (C or D)", d["n_die"], d["die_sure_pct"], LOSS)]):
            w = 5.4
            sure = Rectangle(width=w * sure_pct / 100, height=0.42, fill_color=SURE, fill_opacity=0.9, stroke_width=0)
            risky = Rectangle(width=w * (100 - sure_pct) / 100, height=0.42, fill_color=RISKY, fill_opacity=0.9,
                              stroke_width=0)
            bar = VGroup(sure, risky).arrange(RIGHT, buff=0)
            ls = label(rf"{sure_pct}\% \ sure", font_size=19, color=BLACK).move_to(sure)
            lr = label(rf"{100 - sure_pct}\% \ gamble", font_size=19, color=BLACK).move_to(risky)
            cap = label(rf"{lab_}: \ $N = {n}$", font_size=21, color=col)
            bars_.add(VGroup(cap, VGroup(bar, ls, lr)).arrange(RIGHT, buff=0.35))
        bars_.arrange(DOWN, aligned_edge=RIGHT, buff=0.3).move_to([0, -1.9, 0])
        tag = published_tag(r"Tversky \& Kahneman (1981)")
        assert d["saved_choice"] == "sure" and d["die_choice"] == "risky"
        with self.voiceover(
            "If you're like most people, you chose differently the second time. <bookmark mark='a'/> But look at "
            "what the programmes do. Two hundred saved out of six hundred is four hundred dead. A and C are the same "
            "programme, and so are B and D: a one-third chance that everyone lives. <bookmark mark='b'/> In 1981 Amos "
            f"Tversky and Daniel Kahneman put the first version to {d['n_saved']} people: "
            f"{d['saved_sure_pct']} percent chose the sure thing. <bookmark mark='c'/> They put the second to "
            f"{d['n_die']} others: {100 - d['die_sure_pct']} percent chose the gamble. Saving lives, people avoid "
            "risk. Losing them, they seek it. The outcomes never changed, only the words."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(c1), FadeIn(t1), FadeIn(c2), FadeIn(t2), FadeIn(same))
            vo.wait_until("b")
            self.play(FadeIn(bars_[0], shift=RIGHT * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(bars_[1], shift=RIGHT * 0.15))
        self.clear_scene()

    def story(self):
        head = heading(r"From a coin game to a Nobel prize")
        items = [
            (r"1738", r"Daniel Bernoulli: \ a coin game worth infinitely much, \ for which nobody pays more than a "
                      r"few coins; \ value is not money", NORM),
            (r"1953", r"Maurice Allais: \ a pair of choices that no expected-utility maximizer can make, \ and that "
                      r"most people make", LOSS),
            (r"1979", r"Daniel Kahneman and Amos Tversky: \ prospect theory, \ a kinked value curve and bent "
                      r"probabilities, \ in an economics journal", MODEL),
            (r"2002", r"the economics Nobel to Kahneman, \ Tversky having died in 1996; \ and the critics' question: "
                      r"\ are the biases errors at all?", HEUR),
        ]
        rows = VGroup()
        for yr, txt, c in items:
            rows.add(VGroup(label(yr, font_size=30, color=c), wrapped_label(txt, 10.6, 26, WHITE)).arrange(
                RIGHT, buff=0.4, aligned_edge=UP))
        for r in rows:
            r[1].shift(RIGHT * (1.4 - r[0].width))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, -0.2, 0])
        tag = historical_tag(r"Bernoulli (1738); \ Allais (1953); \ Kahneman \& Tversky (1979)")
        with self.voiceover(
            "The question behind that reversal is old. <bookmark mark='a'/> In 1738 Daniel Bernoulli described a "
            "coin game whose expected prize is infinite, and for which nobody will pay more than a few coins. His "
            "answer was that what matters isn't money but its value to you, which grows ever more slowly. "
            "<bookmark mark='b'/> In 1953 Maurice Allais put a pair of choices to the leading economists of the day "
            "that no one who maximizes expected utility could make, and many of them made them. "
            "<bookmark mark='c'/> In 1979 two psychologists, Daniel Kahneman and Amos Tversky, published prospect "
            "theory in Econometrica: values measured from a reference point, with a kink at zero, and probabilities "
            "bent out of shape. <bookmark mark='d'/> In 2002 Kahneman shared the economics Nobel prize; Tversky had "
            "died in 1996. And through it all, critics led by Gerd Gigerenzer asked whether the so-called biases are "
            "errors at all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def question(self):
        head = heading(r"Today: \ why do the same people buy insurance and lottery tickets?")
        rows = rows_of([
            (r"the standard: \ expected value, \ Bernoulli's utility, \ and the axioms; \ then Allais's violation",
             NORM),
            (r"prospect theory: \ the value and weighting curves, \ and the fourfold pattern they compute", MODEL),
            (r"thirteen thousand gambles: \ prospect theory fitted to open data, \ and tested out of sample", DATA),
            (r"heuristics and biases, \ and the reply: \ frequencies, \ and simple rules that win", HEUR),
            (r"the hot hand, \ time, \ experience, \ and where values come from", TIME),
        ], 12.6, 27, 0.4).move_to([0, -0.3, 0])
        with self.voiceover(
            "So why do the same people buy insurance and lottery tickets? <bookmark mark='a'/> We'll start with the "
            "standard that choices are measured against, and the first famous violation of it. "
            "<bookmark mark='b'/> Then prospect theory, its two curves, and the pattern of risk attitudes they "
            "compute, which answers today's question. <bookmark mark='c'/> Then we'll fit the theory to thirteen "
            "thousand gambles of open data and test it on problems it hasn't seen. <bookmark mark='d'/> Then the "
            "heuristics that produce biases, and the reply that they're often smart. <bookmark mark='e'/> And then "
            "the hot hand, choices over time and from experience, and where values come from in the first place."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 26", font_size=34, color=GREY_B), label(r"Judgment and Choice", font_size=56))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"expected value and utility, \ the axioms, \ and Allais's violation in the probability triangle",
            r"prospect theory's value and weighting functions, \ and the fourfold pattern computed",
            r"prospect theory fitted to 1{,}928 open choice problems \ and cross-validated",
            r"heuristics and biases, \ natural frequencies, \ and take-the-best against regression",
            r"the hot-hand bias computed exactly, \ and hyperbolic discounting's reversals",
            r"decisions from experience, \ two systems, \ and decision by sampling",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 26 of Psychology, Built, the ninth part of Act Five, on thinking: judgment and choice. "
            "<bookmark mark='a'/> We'll set out expected value and utility and watch Allais break them. We'll build "
            "prospect theory's two curves and compute the fourfold pattern of risk. We'll fit the theory to almost "
            "two thousand open choice problems and cross-validate it. We'll meet the heuristics, the frequencies that "
            "tame them, and a simple rule that beats regression. We'll compute the bias hidden in the hot-hand "
            "studies, and the reversals of a mind that discounts the future hyperbolically. And we'll finish with "
            "choices learned from experience, the idea of two systems, and where values come from."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=20.0)
        self.clear_scene()
