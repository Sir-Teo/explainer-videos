from __future__ import annotations

from fractions import Fraction

from videos.psychology.psych26.common import *  # noqa: F403


class HotHand(VoiceoverScene):
    def construct(self):
        self.card()
        self.study()
        self.table()
        self.bias()

    def card(self):
        card = chapter_card(8, r"The hot hand", r"Was the fallacy in the fans, \ or in the analysis?",
                            lit={1985: r"Gilovich, \ Vallone \& Tversky", 2018: r"Miller \& Sanjurjo"},
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter eight. The hot hand."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def study(self):
        head = heading(r"A textbook fallacy")
        rows = rows_of([
            (r"players and fans: \ after a few hits, \ a shooter is \emph{hot}, \ more likely to hit the next", RISKY),
            (r"Gilovich, \ Vallone and Tversky, \ 1985: \ the 76ers' shots, \ free throws, \ and a controlled "
             r"experiment with Cornell's teams, \ 100 shots each", WHITE),
            (r"the test: \ is the hit rate after a streak of hits higher than after a streak of misses?", NORM),
            (r"it was not: \ the hot hand was a cognitive illusion, \ people seeing patterns in randomness", HEUR),
            (r"for thirty years, \ a standard example of a bias, \ in psychology and economics alike", GREY_A),
        ], 12.0, 25, 0.38).move_to([0, -0.2, 0])
        tag = published_tag(r"Gilovich, \ Vallone \& Tversky (1985)")
        with self.voiceover(
            "Basketball players and fans believe in the hot hand: after a few hits in a row, a shooter is more "
            "likely to hit the next. <bookmark mark='a'/> In 1985 Thomas Gilovich, Robert Vallone and Amos Tversky "
            "tested it, on the Philadelphia 76ers' field goals, on free throws, and in a controlled experiment in "
            "which players from Cornell's teams took a hundred shots each. <bookmark mark='b'/> The test was simple: "
            "is a player's hit rate after a streak of hits higher than after a streak of misses? "
            "<bookmark mark='c'/> It wasn't. The hot hand, they concluded, was a cognitive illusion, people seeing "
            "patterns in randomness, a cousin of representativeness. <bookmark mark='d'/> For thirty years it was "
            "the standard example. Then two economists noticed something about the test itself."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0]))
            for m, r in zip("abcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def table(self):
        d = load("hothand")
        seqs, props = d["seqs"], d["props"]
        head = heading(r"Four fair coin flips, \ all sixteen ways")
        cells = VGroup()
        for s, p in zip(seqs, props):
            glyph = VGroup(*[label("H" if v else "T", font_size=24, color=GAIN if v else GREY_B) for v in s]).arrange(
                RIGHT, buff=0.08)
            if np.isnan(p):
                val = label(r"--", font_size=22, color=GREY_D)
            else:
                f = Fraction(float(p)).limit_denominator(6)
                val = label(rf"${f.numerator}/{f.denominator}$" if f.denominator > 1 else rf"${f.numerator}$",
                            font_size=22, color=RISKY)
            cells.add(VGroup(glyph, val).arrange(RIGHT, buff=0.35))
        cells.arrange_in_grid(rows=4, cols=4, buff=(0.7, 0.3), flow_order="dr").move_to([-1.9, 0.1, 0])
        rows = rows_of([
            (r"for each sequence: \ of the flips that follow a head, \ what share are heads?", WHITE),
            (r"two sequences have no flip after a head and are dropped", GREY_B),
            (rf"the average of the other fourteen: \ {d['expected4']:.3f}, \ not 0.5", RISKY),
            (r"every flip is independent, \ yet the expected share after a head is below one half", LOSS),
        ], 4.2, 22, 0.32).move_to([4.5, 0.1, 0])
        tag = psyche_tag(r"\texttt{choice.streak\_exact}: \ all $2^4$ sequences; \ Miller \& Sanjurjo (2018)")
        with self.voiceover(
            "Here's what Joshua Miller and Adam Sanjurjo noticed. Flip a fair coin four times, and write down all "
            "sixteen possible sequences. <bookmark mark='a'/> For each one, look at the flips that come right after "
            "a head, and work out what share of them are heads. In H H H H it's all of them; in H T H T, none. "
            "<bookmark mark='b'/> Two sequences have no flip after a head at all, so they're dropped. "
            "<bookmark mark='c'/> Now average the share over the fourteen that remain, each equally likely. It "
            f"comes to {d['expected4']:.3f}. Not one half. <bookmark mark='d'/> The coin has no memory, yet the "
            "expected share of heads after a head, computed this way within each sequence, is well below one half. "
            "The reason is a selection effect: within a short sequence, every head that follows a head uses up "
            "one of a fixed number of heads, and averaging the shares sequence by sequence lets that count."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            self.play(LaggedStart(*[FadeIn(c[0]) for c in cells], lag_ratio=0.1), run_time=2)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c[1]) for c in cells], lag_ratio=0.1), FadeIn(rows[0]), run_time=2)
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def bias(self):
        d = load("hothand")
        head = heading(r"The bias, \ and the hot hand restored")
        A = axes([2.5, 20.5], [0.38, 0.52], x_length=5.4, y_length=3.6, xticks=[4, 8, 12, 16, 20],
                 yticks=[0.4, 0.45, 0.5], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.2f}",
                 xlabel=r"flips in the sequence", ylabel=r"expected share of heads after a head",
                 center=[-3.4, -0.2, 0], font_size=16)
        half = DashedLine(A.ax.c2p(2.5, 0.5), A.ax.c2p(20.5, 0.5), color=NORM, stroke_width=2)
        cv = curve(A.ax, d["ns"], d["curve"], RISKY, 4)
        dots = scatter(A.ax, d["ns"], d["curve"], RISKY, 0.05, 1)
        rows = rows_of([
            (rf"at Cornell's length, \ 100 shots, \ and after streaks of three, \ the expectation for a shooter with "
             rf"no hot hand is {d['e100_k3']:.3f}", RISKY),
            (r"so finding \emph{no difference} between after-hits and after-misses is evidence \emph{for} a hot "
             r"hand, \ of several points", GAIN),
            (r"Miller and Sanjurjo, \ 2018: \ with the bias corrected, \ the Cornell data show a hot hand, \ and "
             r"later studies of free throws and three-point contests agree", MODEL),
            (r"the lesson: \ a bias can live in the analyst's statistic as well as in the fan", HEUR),
        ], 5.8, 22, 0.32).move_to([3.4, -0.1, 0])
        tag = psyche_tag(rf"\texttt{{choice.streak\_exact}}, \ \texttt{{streak\_sim}}: \ 200{{,}}000 sequences of 100")
        with self.voiceover(
            "The bias shrinks as sequences get longer, but slowly. <bookmark mark='a'/> Here's the exact "
            "expectation for sequences of three to twenty flips: always below one half. <bookmark mark='b'/> In the "
            "Cornell experiment each player took a hundred shots, and the test looked at shots after streaks of "
            "three hits. For a shooter with no hot hand at all, a fifty percent shooter, the expected hit rate "
            f"after three hits, computed within each player's sequence, is about {d['e100_k3']:.2f}, not "
            "point five. <bookmark mark='c'/> So the original finding, no difference between the rate after hits "
            "and after misses, is not evidence against a hot hand. Measured against the right baseline, it's "
            "evidence for one, of several percentage points. <bookmark mark='d'/> Miller and Sanjurjo published the "
            "correction in 2018, and with it the Cornell data show a hot hand; so do later studies of free throws "
            "and of three-point shooting contests. <bookmark mark='e'/> Whether fans overestimate its size is another "
            "question. But the lesson stands: a bias can live in the analyst's statistic as well as in the fan."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(half))
            vo.wait_until("a")
            self.play(Create(cv), FadeIn(dots), run_time=2)
            for m, r in zip("bcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
